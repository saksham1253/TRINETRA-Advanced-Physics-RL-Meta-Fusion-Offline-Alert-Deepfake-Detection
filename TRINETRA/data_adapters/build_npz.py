"""data_adapters/build_npz.py — convert SMALL prototype datasets into the exact .npz contracts that the
EXISTING trainers expect (trinetra/kaggle/README.md §2). New file only; no existing code is modified.

Contracts (from trinetra/src/trinetra/deep/datamodules.py, read 2026-10-31):
  fire     : images (N,T,C,H,W) float32 in [0,1], labels (N,2) [fire, smoke], block (N,) str
  deepfake : images (N,C,H,W)   float32 in [0,1], labels (N,)  1 = fake,       block (N,) str
  telemetry: X (N,C,T) float32, y (N,) 0/1 (window contains alarm), block (N,) str

`block` is the GROUP key used by spatial_cv_indices -> eval.spatial_block_kfold. For images we put a
leakage-safe group there (video/source prefix or perceptual-hash cluster), NOT lat/lon. That is a
documented re-use of the field (see docs/09c_DATASET_SUBSETS_AND_SPLITS.md).

Usage (Kaggle notebook, CPU session is enough):
  python data_adapters/build_npz.py folder   --root /kaggle/input/fire-dataset/fire_dataset \
         --map fire_images=fire non_fire_images=none --task fire --size 128 --max-per-class 1500 \
         --out /kaggle/working/fire.npz --manifest data_manifests/fire_dataset_subset.csv
  python data_adapters/build_npz.py yolo     --root /kaggle/input/smoke-fire-detection-yolo/data \
         --classes 0=smoke 1=fire --task fire --size 128 --max-images 4000 --out /kaggle/working/dfire.npz
  python data_adapters/build_npz.py iot      --csv /kaggle/input/smoke-detection-dataset/smoke_detection_iot.csv \
         --label "Fire Alarm" --time UTC --window 30 --stride 10 --out /kaggle/working/tele.npz
  python data_adapters/build_npz.py check    --npz /kaggle/working/fire.npz       # contract + leakage check
  python data_adapters/build_npz.py subset   --npz /kaggle/working/fire.npz --keep train val \
         --out /kaggle/working/fire_trainval.npz   # trainers k-fold this; keep 'test' groups untouched

Status: UNTESTED on the real datasets (authoring sandbox has no dataset access). Tested on synthetic
files by data_adapters/test_build_npz.py. Column/folder names marked [verify] are from dataset pages or
memory and must be confirmed on first run (the script fails loudly if they are missing).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import random
import re
import sys
from pathlib import Path

import numpy as np

IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
SEED = 0


# ----------------------------------------------------------------------------------------------- utils
def _load_rgb(path: Path, size: int) -> np.ndarray:
    from PIL import Image  # available on Kaggle images; imported lazily so `iot`/`check` need no PIL

    with Image.open(path) as im:
        im = im.convert("RGB").resize((size, size))
        return np.asarray(im, dtype=np.float32) / 255.0  # (H,W,C)


def ahash(img_hwc: np.ndarray, n: int = 8) -> int:
    """Average-hash on an 8x8 grey thumbnail (perceptual hash for near-duplicate grouping)."""
    g = img_hwc.mean(axis=2)
    h, w = g.shape
    g = g[: h - h % n, : w - w % n].reshape(n, h // n, n, w // n).mean(axis=(1, 3))
    bits = (g > g.mean()).flatten()
    return int("".join("1" if b else "0" for b in bits), 2)


def _hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


AUG_RE = re.compile(r"(?:_aug_?\d+|\s\(\d+\)|_copy\d*)$", re.I)
SEQ_RE = re.compile(r"^([A-Za-z][A-Za-z_\-]*?)[_\-]?(\d+)$")
SEQ_BUCKET = 0          # set by --seq-bucket: consecutive numbered frames (AoF00123, frame_456) share a group


def group_key_from_name(name: str) -> str | None:
    """Video/source prefix heuristics, e.g. 'vid12_frame0003.jpg' -> 'vid12', 'WEB10495.jpg' -> None.
    Augmented copies ('fake_12_aug_3', 'x (2)') map to their source image so they never straddle splits.
    With SEQ_BUCKET>0, 'AoF06723' -> 'AoF#134' (frames numbered consecutively from one camera stay together)."""
    stem = Path(name).stem
    base = AUG_RE.sub("", stem)
    if base != stem:
        return "aug:" + base.lower()
    if SEQ_BUCKET > 0:
        m = SEQ_RE.match(stem)
        if m:
            return f"seq:{m.group(1).lower()}#{int(m.group(2)) // SEQ_BUCKET}"
    m = re.match(r"^(.*?)(?:[_\-\s]?(?:frame|frm|f|img)?[_\-\s]?\d{2,})$", stem, re.I)
    if m and m.group(1) and not m.group(1).isdigit() and len(m.group(1)) >= 3:
        prefix = m.group(1).rstrip("_- ")
        # pure dataset-wide prefixes (WEB, AoF, PublicDataset) are not video ids -> fall back to hashing
        if prefix.upper() not in {"WEB", "AOF", "PUBLICDATASET", "IMG", "IMAGE", "FIRE", "SMOKE", "NOFIRE"}:
            return prefix
    return None


def assign_groups(names: list[str], hashes: list[int], max_dist: int = 6) -> list[str]:
    """Group = filename video prefix if present, else a perceptual-hash cluster (greedy, Hamming<=max_dist).
    Near-duplicates therefore always share a group and can never straddle train/test (rule 14)."""
    groups: list[str] = [""] * len(names)
    reps: list[tuple[int, str]] = []
    for i, (n, h) in enumerate(zip(names, hashes)):
        g = group_key_from_name(n)
        if g is None:
            for rh, rg in reps:
                if _hamming(h, rh) <= max_dist:
                    g = rg
                    break
            if g is None:
                g = f"ph{len(reps):05d}"
                reps.append((h, g))
        groups[i] = g
    return groups


def split_groups(groups: list[str], fracs=(0.7, 0.15, 0.15), seed: int = SEED) -> dict[str, str]:
    uniq = sorted(set(groups))
    random.Random(seed).shuffle(uniq)
    n = len(uniq)
    a, b = int(fracs[0] * n), int((fracs[0] + fracs[1]) * n)
    return {g: ("train" if i < a else "val" if i < b else "test") for i, g in enumerate(uniq)}


def write_manifest(path: str | None, rows: list[dict]) -> None:
    if not path:
        return
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"[manifest] {len(rows)} rows -> {path}")


def _save(out: str, **arrays) -> None:
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out, **arrays)
    print(f"[npz] {out} :: " + ", ".join(f"{k}{tuple(v.shape)}" for k, v in arrays.items()))


def _to_contract(imgs: list[np.ndarray], lab: list, task: str):
    X = np.stack(imgs).transpose(0, 3, 1, 2).astype(np.float32)  # (N,C,H,W)
    if task == "fire":
        return X[:, None], np.asarray(lab, np.float32).reshape(-1, 2)  # (N,1,C,H,W), (N,2)
    return X, np.asarray(lab, np.float32).reshape(-1)  # deepfake: (N,C,H,W), (N,)


# ---------------------------------------------------------------------------------------- builders
FIRE_LABELS = {"fire": [1, 0], "smoke": [0, 1], "fire+smoke": [1, 1], "none": [0, 0]}
FAKE_LABELS = {"fake": 1, "real": 0}


def _label_vec(name: str, task: str):
    table = FIRE_LABELS if task == "fire" else FAKE_LABELS
    if name not in table:
        raise SystemExit(f"label {name!r} not valid for task {task}; use one of {sorted(table)}")
    return table[name]


def _match(rel: Path, key: str) -> bool:
    """key 'fire' matches a path PART named fire; key 'Training/fire' or 'fire/pos' matches a sub-path."""
    if "/" in key:
        return f"/{key.strip('/')}/" in f"/{rel.parent.as_posix()}/"
    return key in rel.parts[:-1]


def build_folder(a) -> None:
    """Class-per-folder datasets (FIRE Dataset, DeepFire, CIFAKE, weather confusers). --map folder=label.
    Verified layouts (Kaggle file API, 2026-10-31) are listed in docs/09d_DATASET_LAYOUTS.md."""
    mapping = dict(m.split("=", 1) for m in a.map)
    root = Path(a.root)
    items: list[tuple[Path, str]] = []
    allimgs = sorted(p for p in root.rglob("*") if p.suffix.lower() in IMG_EXT)
    for folder, label in mapping.items():
        files = [p for p in allimgs if _match(p.relative_to(root), folder)]
        if not files:
            raise SystemExit(f"no images under {root} with a path part named {folder!r} [verify layout]")
        random.Random(SEED).shuffle(files)
        items += [(p, label) for p in files[: a.max_per_class]]
    _finish_images(a, items, source=root.name)


def build_yolo(a) -> None:
    """YOLO txt datasets (D-Fire Kaggle mirror, wildfire-smoke YOLO). Image-level multi-label from boxes."""
    root = Path(a.root)
    if a.classes == ["auto"]:
        cls = yolo_names(root)
        print(f"[yolo] classes from data.yaml: {cls}")
    else:
        cls = {int(k): v for k, v in (c.split("=", 1) for c in a.classes)}
    imgs = sorted(p for p in root.rglob("*") if p.suffix.lower() in IMG_EXT)
    random.Random(SEED).shuffle(imgs)
    items: list[tuple[Path, str]] = []
    for p in imgs[: a.max_images]:
        lbl = Path(str(p.with_suffix(".txt")).replace(f"{os.sep}images{os.sep}", f"{os.sep}labels{os.sep}"))
        names = set()
        if lbl.exists():
            for line in lbl.read_text().splitlines():
                if line.strip():
                    names.add(cls.get(int(float(line.split()[0])), "none"))
        names.discard("none")
        items.append((p, "fire+smoke" if names == {"fire", "smoke"} else (names.pop() if names else "none")))
    _finish_images(a, items, source=root.name)


def yolo_names(root: Path) -> dict:
    """Parse `names:` from the dataset's data.yaml (list or dict form) without pyyaml; map to fire/smoke/none."""
    ys = sorted(root.rglob("data.yaml")) or sorted(root.parent.rglob("data.yaml"))
    if not ys:
        raise SystemExit("no data.yaml found; pass --classes 0=smoke 1=fire explicitly")
    txt = ys[0].read_text()
    names: list[str] = []
    m = re.search(r"names\s*:\s*\[(.*?)\]", txt, re.S)
    if m:
        names = [x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip()]
    else:
        for line in txt.split("names", 1)[-1].splitlines()[1:]:
            mm = re.match(r"\s*(?:-\s*|\d+\s*:\s*)['\"]?([^'\"#]+?)['\"]?\s*$", line)
            if not mm:
                break
            names.append(mm.group(1).strip())
    if not names:
        raise SystemExit(f"could not parse names in {ys[0]}")
    def canon(n):
        n = n.lower()
        return "fire" if ("fire" in n or "flame" in n) else ("smoke" if "smoke" in n else "none")
    return {i: canon(n) for i, n in enumerate(names)}


def _finish_images(a, items, source: str) -> None:
    imgs, labs, names, hashes, kept = [], [], [], [], []
    for p, label in items:
        try:
            im = _load_rgb(p, a.size)
        except Exception as e:  # corrupt files exist in several Kaggle sets; skip and log
            print(f"[skip] {p}: {e}", file=sys.stderr)
            continue
        imgs.append(im); labs.append(_label_vec(label, a.task)); names.append(p.name); hashes.append(ahash(im))
        kept.append((p, label))
    if not imgs:
        raise SystemExit("no readable images")
    groups = assign_groups(names, hashes)
    groups = [f"{source}:{g}" for g in groups]
    splits = split_groups(groups)
    X, Y = _to_contract(imgs, labs, a.task)
    _save(a.out, images=X, labels=Y, block=np.asarray(groups), split=np.asarray([splits[g] for g in groups]),
          ahash=np.asarray(hashes, dtype=np.uint64), name=np.asarray(names))
    write_manifest(a.manifest, [
        {"sample_id": i, "path": str(p), "label": lab, "group": g, "split": splits[g],
         "sha1": hashlib.sha1(str(p).encode()).hexdigest()[:12]}
        for i, ((p, lab), g) in enumerate(zip(kept, groups))
    ])


def build_iot(a) -> None:
    """Tabular sensor CSV (Kaggle Smoke Detection Dataset) -> sliding windows X (N,C,T).

    Sessions: a new session starts when `--counter` resets or the time gap > --gap seconds. The session id
    is the group, so overlapping windows from one session never land in different splits (rule 14).
    Column names [verify]: 'UTC', 'CNT', 'Fire Alarm' as listed on the Kaggle page."""
    with open(a.csv, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("empty csv")
    cols = list(rows[0].keys())
    for need in (a.label, a.time):
        if need not in cols:
            raise SystemExit(f"column {need!r} not in {cols} [verify]")
    drop = {a.label, a.time, a.counter, ""} | {c for c in cols if c.lower().startswith("unnamed")}
    feat = [c for c in cols if c not in drop]
    rows.sort(key=lambda r: float(r[a.time]))
    F = np.array([[float(r[c]) for c in feat] for r in rows], np.float32)
    y = np.array([int(float(r[a.label])) for r in rows], np.int64)
    t = np.array([float(r[a.time]) for r in rows])
    cnt = np.array([float(r[a.counter]) for r in rows]) if a.counter in cols else None
    sess = np.zeros(len(rows), np.int64)
    for i in range(1, len(rows)):
        new = (t[i] - t[i - 1] > a.gap) or (cnt is not None and cnt[i] < cnt[i - 1])
        sess[i] = sess[i - 1] + int(new)
    Xw, yw, gw = [], [], []
    for s in np.unique(sess):
        idx = np.where(sess == s)[0]
        for st in range(0, len(idx) - a.window + 1, a.stride):
            w = idx[st: st + a.window]
            Xw.append(F[w].T); yw.append(int(y[w].max())); gw.append(f"session{s:04d}")
    if not Xw:
        raise SystemExit("no windows built: lower --window or raise --gap")
    X = np.stack(Xw).astype(np.float32)
    splits = split_groups(gw)
    split_arr = np.asarray([splits[g] for g in gw])
    # Standardize each feature with TRAIN-split statistics only (eCO2 ~ 1e3-1e4 vs humidity ~ 50 would
    # otherwise dominate the autoencoder loss). Test/val windows never contribute to the stats.
    trm = split_arr == "train"
    ref = X[trm] if trm.any() else X
    mu = ref.mean(axis=(0, 2)); sd = ref.std(axis=(0, 2)) + 1e-6
    if a.standardize:
        X = ((X - mu[None, :, None]) / sd[None, :, None]).astype(np.float32)
    _save(a.out, X=X, y=np.asarray(yw, np.float32), block=np.asarray(gw),
          split=split_arr, features=np.asarray(feat), feat_mean=mu.astype(np.float32), feat_std=sd.astype(np.float32))
    print(f"[iot] sessions={len(set(gw))} windows={len(Xw)} positive_frac={np.mean(yw):.3f} features={feat}")


def _video_one(a) -> None:
    """Worker (own process): decode ONE video with OpenCV and save frames (T,C,H,W) float32 to --out (.npy).
    Runs isolated because a corrupt .avi can crash OpenCV's FFmpeg backend natively (malloc abort, exit -6)."""
    import cv2
    cv2.setNumThreads(1)
    cap = cv2.VideoCapture(a.path); frames = []; i = 0
    while True:
        ok, fr = cap.read()
        if not ok or fr is None or len(frames) >= a.max_frames:
            break
        if i % a.every == 0:
            fr = cv2.resize(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB), (a.size, a.size)).astype(np.float32) / 255.0
            frames.append(fr.transpose(2, 0, 1))
        i += 1
    cap.release()
    np.save(a.out, np.stack(frames) if frames else np.zeros((0, 3, a.size, a.size), np.float32))


def _frames_ffmpeg(path: Path, every: int, size: int, max_frames: int):
    """Fallback decoder: the ffmpeg CLI (separate process) emits raw RGB frames; same every-N-th selection."""
    import shutil, subprocess
    if not shutil.which("ffmpeg"):
        return None
    vf = f"select=not(mod(n\\,{every})),scale={size}:{size}:flags=bilinear"
    cmd = ["ffmpeg", "-v", "error", "-err_detect", "ignore_err", "-i", str(path), "-vf", vf, "-fps_mode", "passthrough",
           "-frames:v", str(max_frames), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=600)
    except subprocess.TimeoutExpired:
        return None
    n = len(r.stdout) // (size * size * 3)
    if n == 0:
        return None
    arr = np.frombuffer(r.stdout[: n * size * size * 3], np.uint8).reshape(n, size, size, 3)
    return (arr.astype(np.float32) / 255.0).transpose(0, 3, 1, 2)


def _read_video_safe(v: Path, a):
    """Decode in a child process (OpenCV); if it crashes or yields nothing, retry with ffmpeg; else None (skip)."""
    import subprocess, tempfile
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "frames.npy"
        cmd = [sys.executable, os.path.abspath(__file__), "_video1", "--path", str(v), "--every", str(a.every),
               "--size", str(a.size), "--max-frames", str(a.max_frames), "--out", str(out)]
        try:
            rc = subprocess.run(cmd, capture_output=True, timeout=600).returncode
        except subprocess.TimeoutExpired:
            rc = "timeout"
        if rc == 0 and out.exists():
            fr = np.load(out)
            if len(fr):
                return fr, "opencv"
    fr = _frames_ffmpeg(v, a.every, a.size, a.max_frames)
    if fr is not None:
        print(f"[video] {v.name}: OpenCV failed (exit {rc}) -> ffmpeg fallback ok", flush=True)
        return fr, "ffmpeg"
    print(f"[video] {v.name}: unreadable (OpenCV exit {rc}, ffmpeg failed) -> skipped", flush=True)
    return None, None


def build_video(a) -> None:
    """Videos (FireSense .avi) -> clips (N,T,C,H,W) taking every `--every`-th frame; group = video file.
    --clip 1 gives a per-frame series (with `frame_idx`) for kaggle/eval_video.py (temporal validator).
    Each video is decoded in its own process, so one corrupt file is skipped instead of killing the whole build."""
    mapping = dict(m.split("=", 1) for m in a.map)
    root = Path(a.root)
    vids = sorted(p for p in root.rglob("*") if p.suffix.lower() in {".avi", ".mp4", ".mov", ".mkv"})
    X, L, G, F = [], [], [], []
    skipped = []
    for k, v in enumerate(vids, 1):
        rel = v.relative_to(root)
        lab = next((lb for key, lb in mapping.items() if _match(rel, key)), None)
        if lab is None:
            continue
        frames, how = _read_video_safe(v, a)
        if frames is None:
            skipped.append(rel.as_posix()); continue
        for s0 in range(0, len(frames) - a.clip + 1, a.clip):
            X.append(frames[s0:s0 + a.clip]); L.append(_label_vec(lab, "fire"))
            G.append(f"video:{rel.as_posix()}"); F.append(s0 * a.every)
        print(f"[video] {k}/{len(vids)} {rel} label={lab} frames={len(frames)} ({how})", flush=True)
    if skipped:
        print(f"[video] skipped {len(skipped)} unreadable file(s): {skipped}", flush=True)
    if not X:
        raise SystemExit("no clips built [verify --map keys against folder names]")
    splits = split_groups(G)
    _save(a.out, images=np.stack(X).astype(np.float32), labels=np.asarray(L, np.float32), block=np.asarray(G),
          split=np.asarray([splits[g] for g in G]), frame_idx=np.asarray(F))


def _hashes_of(d) -> np.ndarray:
    if "ahash" in d.files:
        return d["ahash"].astype(np.uint64)
    X = d["images"]
    X = X[:, X.shape[1] // 2] if X.ndim == 5 else X
    return np.asarray([ahash(x.transpose(1, 2, 0)) for x in X], dtype=np.uint64)


def dedupe(a) -> None:
    """Drop rows of --test whose perceptual hash is within --max-dist of ANY --train row (cross-dataset leakage:
    D-Fire 'WEB'/'PublicDataset' images and DeepFire are both web-scraped, so the same photo can be in both)."""
    tr = np.load(a.train, allow_pickle=True); te = np.load(a.test, allow_pickle=True)
    ht = _hashes_of(tr); hs = _hashes_of(te)
    tset = [int(h) for h in ht]
    keep = np.ones(len(hs), bool)
    for i, h in enumerate(hs):
        h = int(h)
        keep[i] = min(_hamming(h, t) for t in tset) > a.max_dist
    n = len(te["block"])
    _save(a.out, **{k: (te[k][keep] if (te[k].ndim and len(te[k]) == n) else te[k]) for k in te.files})
    print(f"[dedupe] removed {int((~keep).sum())}/{len(keep)} near-duplicates of train (max_dist={a.max_dist})")


# ------------------------------------------------------------------------------------------ checks
CONTRACTS = {
    "fire": {"images": 5, "labels": 2, "block": 1},
    "deepfake": {"images": 4, "labels": 1, "block": 1},
    "telemetry": {"X": 3, "block": 1},
}


NON_ROW_KEYS = {"features", "feat_mean", "feat_std", "band_mean", "band_std"}


def check(a) -> int:
    d = np.load(a.npz, allow_pickle=True)
    keys = set(d.files)
    kind = "telemetry" if "X" in keys else ("fire" if d["images"].ndim == 5 else "deepfake")
    ok = True
    for k, nd in CONTRACTS[kind].items():
        if k not in keys or d[k].ndim != nd:
            print(f"[FAIL] {kind}: key {k!r} missing or ndim!={nd}"); ok = False
    n = len(d["block"])
    for k in keys - NON_ROW_KEYS:
        if len(d[k]) != n:
            print(f"[FAIL] length mismatch {k}: {len(d[k])} vs {n}"); ok = False
    if "split" in keys:
        seen: dict[str, set] = {}
        for g, s in zip(d["block"], d["split"]):
            seen.setdefault(str(g), set()).add(str(s))
        leaks = [g for g, s in seen.items() if len(s) > 1]
        print(f"[leak-check] groups={len(seen)} groups_in_2+_splits={len(leaks)}")
        ok &= not leaks
    print(("[OK] " if ok else "[FAIL] ") + f"{a.npz} kind={kind} n={n}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sp = ap.add_subparsers(dest="cmd", required=True)
    f = sp.add_parser("folder"); f.add_argument("--root", required=True); f.add_argument("--map", nargs="+", required=True)
    y = sp.add_parser("yolo"); y.add_argument("--root", required=True)
    y.add_argument("--classes", nargs="+", required=True, help="'auto' (read data.yaml) or 0=smoke 1=fire")
    y.add_argument("--max-images", type=int, default=4000)
    for p in (f, y):
        p.add_argument("--task", choices=["fire", "deepfake"], default="fire")
        p.add_argument("--size", type=int, default=128)
        p.add_argument("--max-per-class", type=int, default=1500)
        p.add_argument("--out", required=True); p.add_argument("--manifest")
        p.add_argument("--seq-bucket", type=int, default=0, help="group consecutive numbered frames in buckets of N")
    i = sp.add_parser("iot"); i.add_argument("--csv", required=True); i.add_argument("--label", default="Fire Alarm")
    i.add_argument("--time", default="UTC"); i.add_argument("--counter", default="CNT")
    i.add_argument("--window", type=int, default=30); i.add_argument("--stride", type=int, default=10)
    i.add_argument("--gap", type=float, default=60.0); i.add_argument("--out", required=True)
    i.add_argument("--no-standardize", dest="standardize", action="store_false")
    c = sp.add_parser("check"); c.add_argument("--npz", required=True)
    v = sp.add_parser("video"); v.add_argument("--root", required=True); v.add_argument("--map", nargs="+", required=True)
    v.add_argument("--every", type=int, default=15); v.add_argument("--clip", type=int, default=8)
    v.add_argument("--size", type=int, default=128); v.add_argument("--max-frames", type=int, default=400)
    v.add_argument("--out", required=True)
    w = sp.add_parser("_video1"); w.add_argument("--path", required=True); w.add_argument("--every", type=int, required=True)
    w.add_argument("--size", type=int, required=True); w.add_argument("--max-frames", type=int, required=True)
    w.add_argument("--out", required=True)
    dd = sp.add_parser("dedupe"); dd.add_argument("--train", required=True); dd.add_argument("--test", required=True)
    dd.add_argument("--out", required=True); dd.add_argument("--max-dist", type=int, default=4)
    s = sp.add_parser("subset"); s.add_argument("--npz", required=True); s.add_argument("--keep", nargs="+", required=True)
    s.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    global SEQ_BUCKET
    SEQ_BUCKET = getattr(a, "seq_bucket", 0) or 0
    if a.cmd == "video":
        build_video(a); return 0
    if a.cmd == "_video1":
        _video_one(a); return 0
    if a.cmd == "dedupe":
        dedupe(a); return 0
    if a.cmd == "folder":
        build_folder(a)
    elif a.cmd == "yolo":
        build_yolo(a)
    elif a.cmd == "iot":
        build_iot(a)
    elif a.cmd == "subset":
        d = np.load(a.npz, allow_pickle=True)
        m = np.isin(d["split"].astype(str), a.keep)
        _save(a.out, **{k: (d[k] if k in NON_ROW_KEYS else d[k][m]) for k in d.files})
    else:
        return check(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
