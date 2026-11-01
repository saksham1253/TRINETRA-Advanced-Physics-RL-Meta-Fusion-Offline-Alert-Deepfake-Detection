"""data_adapters/build_eo.py — Earth-observation sets -> the EO head contract used by
`kaggle/train_classifier.py --model eo` (ImageFolderNPZ: images (N,C,H,W) float32, labels (N,), block (N,) group key).
New file; existing loaders untouched. Patch-level labels (the EO head is a classifier, not a segmenter).

  l4s          Landslide4Sense (Sentinel-2 B1-B12 + slope + DEM = 14 bands, 128x128 .h5; keys 'img', 'mask')
               label = landslide-pixel fraction > --min-frac ; group = perceptual hash of RGB (patches have no coords)
  sen1floods11 Sen1Floods11 hand-labelled (S1Hand *.tif VV,VH dB; LabelHand *.tif -1/0/1)
               label = flooded fraction of valid pixels > --min-frac ; group = flood EVENT (file prefix, e.g. Bolivia)
               -> use `--holdout-event Bolivia` (the dataset's standard cross-region test) to write a separate test npz
  hephaestus   Hephaestus InSAR cropped patches (+ annotation JSONs): label = any deformation class ; group = frameID
               (one frame = one location; patches of a frame must never straddle splits)
Per-band standardization uses TRAIN-split statistics only (stored as band_mean/band_std).
Needs: h5py (l4s), tifffile+imagecodecs (sen1floods11), pillow (hephaestus). All on Kaggle or `pip install`.
Verified sources 2026-10-31: github.com/iarai/Landslide4Sense-2022 (layout, 3799/245/800 patches, 14 bands);
Kaggle mirrors in docs/09e; github.com/Orion-AI-Lab/Hephaestus (MIT, annotation schema). Layout inside the Kaggle
mirrors is [verify] where the file API listing was truncated.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_npz as B  # noqa: E402  (reuse ahash, grouping, splits, _save)


def _resize(x: np.ndarray, size: int) -> np.ndarray:
    """(C,H,W) -> (C,size,size) by block-mean (integer factor) or nearest index (otherwise)."""
    C, H, W = x.shape
    if H == size and W == size:
        return x
    if H % size == 0 and W % size == 0:
        return x.reshape(C, size, H // size, size, W // size).mean(axis=(2, 4))
    ri = (np.arange(size) * H / size).astype(int); ci = (np.arange(size) * W / size).astype(int)
    return x[:, ri][:, :, ci]


def _rgb_hash(x: np.ndarray, rgb=(0, 1, 2)) -> int:
    v = np.stack([x[i] for i in rgb], -1)
    v = (v - np.nanmin(v)) / (np.nanmax(v) - np.nanmin(v) + 1e-9)
    return B.ahash(np.nan_to_num(v))


def _round_robin(paths, group_key, limit):
    """Select a deterministic cap without exhausting one sorted group first."""
    grouped = {}
    for path in paths:
        grouped.setdefault(group_key(path), []).append(path)
    selected = []
    while len(selected) < limit:
        added = False
        for key in sorted(grouped):
            if grouped[key]:
                selected.append(grouped[key].pop(0))
                added = True
                if len(selected) == limit:
                    break
        if not added:
            break
    return selected


def _finish(a, X, y, groups, extra=None):
    X = np.nan_to_num(np.stack(X).astype(np.float32)); y = np.asarray(y, np.float32)
    splits = B.split_groups(groups)
    sp = np.asarray([splits[g] for g in groups])
    tr = sp == "train"
    mu = X[tr].mean(axis=(0, 2, 3)); sd = X[tr].std(axis=(0, 2, 3)) + 1e-6
    X = (X - mu[None, :, None, None]) / sd[None, :, None, None]
    B._save(a.out, images=X, labels=y, block=np.asarray(groups), split=sp,
            band_mean=mu.astype(np.float32), band_std=sd.astype(np.float32), **(extra or {}))
    print(f"[eo] n={len(y)} pos_frac={y.mean():.3f} groups={len(set(groups))} channels={X.shape[1]}")
    return mu, sd


def build_l4s(a):
    import h5py
    root = Path(a.root)
    imgs = sorted(root.rglob("image_*.h5"), key=lambda p: int(re.findall(r"\d+", p.stem)[-1]))[: a.max_n]
    if not imgs:
        raise SystemExit(f"no image_*.h5 under {root} [verify layout: TrainData/img/image_#.h5, TrainData/mask/mask_#.h5]")
    X, y, H = [], [], []
    for p in imgs:
        m = Path(str(p).replace(f"{p.parent.name}/image_", f"{'mask' if p.parent.name == 'img' else p.parent.name}/mask_"))
        if not m.exists():
            m = p.parent.parent / "mask" / p.name.replace("image_", "mask_")
        with h5py.File(p, "r") as f:
            x = np.asarray(f["img"], np.float32)              # (128,128,14)
        x = _resize(np.transpose(x, (2, 0, 1)), a.size)
        lab = np.nan
        if m.exists():
            with h5py.File(m, "r") as f:
                lab = float((np.asarray(f["mask"]) > 0).mean() > a.min_frac)
        X.append(x); y.append(lab); H.append(_rgb_hash(x, (3, 2, 1)))   # B4,B3,B2
    keep = ~np.isnan(np.asarray(y, float))
    if not keep.all():
        print(f"[l4s] {int((~keep).sum())} patches without masks dropped (test split has no labels)")
    X = [x for x, k in zip(X, keep) if k]; y = [v for v, k in zip(y, keep) if k]; H = [h for h, k in zip(H, keep) if k]
    groups = [f"l4s:{g}" for g in B.assign_groups([f"p{i}" for i in range(len(H))], H)]
    _finish(a, X, y, groups)


def build_sen1floods11(a):
    import tifffile
    root = Path(a.root)
    candidates = sorted(p for p in root.rglob("*S1Hand*.tif"))
    event_key = lambda p: p.name.split("_")[0]
    if a.holdout_event:
        held = [p for p in candidates if event_key(p) == a.holdout_event]
        train = [p for p in candidates if event_key(p) != a.holdout_event]
        held_n = min(len(held), max(1, a.max_n // 5))
        s1 = _round_robin(train, event_key, max(0, a.max_n - held_n)) + held[:held_n]
    else:
        s1 = _round_robin(candidates, event_key, a.max_n)
    if not s1:
        raise SystemExit(f"no *S1Hand*.tif under {root} [verify: v1.1/data/flood_events/HandLabeled/S1Hand]")
    X, y, G, Xt, yt, Gt = [], [], [], [], [], []
    for p in s1:
        lab_p = next(iter(root.rglob(p.name.replace("S1Hand", "LabelHand"))), None)
        if lab_p is None:
            continue
        x = np.asarray(tifffile.imread(p), np.float32)
        x = x if x.shape[0] in (2, 3) else np.transpose(x, (2, 0, 1))
        lab = np.asarray(tifffile.imread(lab_p))
        valid = lab >= 0
        if valid.mean() < 0.5:
            continue
        frac = float((lab[valid] == 1).mean())
        event = p.name.split("_")[0]
        tgt = (Xt, yt, Gt) if (a.holdout_event and event == a.holdout_event) else (X, y, G)
        tgt[0].append(_resize(np.nan_to_num(x[:2], nan=-30.0), a.size)); tgt[1].append(float(frac > a.min_frac)); tgt[2].append(f"event:{event}")
    mu, sd = _finish(a, X, y, G)
    if Xt:
        Xt = (np.stack(Xt) - mu[None, :, None, None]) / sd[None, :, None, None]
        out_t = a.out.replace(".npz", f"_{a.holdout_event}_test.npz")
        B._save(out_t, images=Xt.astype(np.float32), labels=np.asarray(yt, np.float32), block=np.asarray(Gt), split=np.asarray(["test"] * len(yt)))


def build_hephaestus(a):
    from PIL import Image
    root = Path(a.root)
    ann = {}
    for j in Path(a.annotations).rglob("*.json") if a.annotations else []:
        try:
            d = json.loads(j.read_text())
            ann[str(d["uniqueID"])] = d
        except Exception:
            continue
    imgs = sorted(p for p in root.rglob("*") if p.suffix.lower() in {".png", ".jpg", ".tif", ".tiff"})[: a.max_n]
    X, y, G = [], [], []
    for p in imgs:
        uid = re.findall(r"\d+", p.stem)
        d = ann.get(uid[0]) if uid else None
        if d is not None:
            labels = [l for l in d.get("label", []) if l]
            lab = float(any(l != "Non_Deformation" for l in labels)); grp = f"frame:{d.get('frameID', 'na')}"
            if d.get("corrupted") or d.get("processing_error"):
                continue
        else:   # fall back to folder name: 0 / Non_Deformation / non_deformation -> 0
            parent = p.parent.name.lower()
            lab = 0.0 if (parent in {"0", "non_deformation", "nondeformation"} or "non" in parent) else 1.0
            grp = None
        with Image.open(p) as im:
            x = np.asarray(im.convert("RGB").resize((a.size, a.size)), np.float32) / 255.0
        X.append(np.transpose(x, (2, 0, 1))); y.append(lab); G.append(grp or f"ph:{B.ahash(x)}")
    if not X:
        raise SystemExit("no Hephaestus images found [verify layout of Hephaestus_Classification.zip]")
    if not ann:
        print("[hephaestus] WARNING: no annotations -> groups by image hash, NOT by frame (leakage risk); pass --annotations")
    _finish(a, X, y, G)


def main(argv=None):
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    for name in ("l4s", "sen1floods11", "hephaestus"):
        p = sp.add_parser(name)
        p.add_argument("--root", required=True); p.add_argument("--out", required=True)
        p.add_argument("--size", type=int, default=64); p.add_argument("--max-n", type=int, default=5000)
        p.add_argument("--min-frac", type=float, default=0.001 if name == "l4s" else 0.05)
        if name == "sen1floods11":
            p.add_argument("--holdout-event", default="Bolivia")
        if name == "hephaestus":
            p.add_argument("--annotations", default=None)
    a = ap.parse_args(argv)
    {"l4s": build_l4s, "sen1floods11": build_sen1floods11, "hephaestus": build_hephaestus}[a.cmd](a)


if __name__ == "__main__":
    main()
