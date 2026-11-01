"""Kaggle kernel: ZERO-SHOT fire/smoke expert with open_clip (GAP G-01; ws4_cctv/zero_shot_design.md D-011),
plus an optional FEW-SHOT linear probe on the same CLIP image embeddings.

v2 (2026-10-31, after the phase-2 run in docs/14):
  * default backbone ViT-L-14 / laion2b_s32b_b82k (v1 was ViT-B-32); images are scored at the model's native size,
    so build the fire pack at SIZE=224 (upscaling 128-px images loses detail);
  * concept-level prompts: every concept (e.g. "a candle flame", "lightning in the sky") gets its OWN text vector and
    the softmax runs over all concepts; v1 averaged all "not fire" prompts into one vector, which cannot reject a
    specific look-alike. The v2 list names known confuser CATEGORIES a priori (no labels used), so stress-set
    false-alarm rates are NOT blind; the report says so (prompt_version / stress_note);
  * the admission gate is applied to the cross-fit CALIBRATED out-of-fold probability (temperature fitted on the
    other folds only), which is how the expert is deployed; the v1 raw-probability verdict is kept as `gate_raw`;
  * --probe: logistic regression on frozen CLIP embeddings, trained with the SAME spatial/group folds (true OOF),
    saved as its own expert `clip_probe` with its own admission report. It uses labels, so it is NOT zero-shot.

Outputs: <out>/zeroshot_s<seed>_{oof.npz,report.json} and, with --probe, <probe-out>/clip_probe_s<seed>_{oof.npz,report.json}.
Run (internet ON the first time to download weights, ~1.7 GB for ViT-L-14):
  python kaggle/eval_zeroshot.py --data fire.npz --test deepfire.npz --stress stress_*.npz --out out/zeroshot \
         --probe --probe-out out/clip_probe
  --dry-run uses random weights (pipeline check only; numbers meaningless).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from trinetra.deep.oof_utils import save_oof, ensure_dir, fit_temperature, stress_summary  # noqa: E402
from trinetra.deep.train import admit_model, AdmissionInputs, set_seed      # noqa: E402
from trinetra.eval import spatial_block_kfold, expected_calibration_error  # noqa: E402

TEMPLATES = ["a photo of {}.", "a CCTV camera image of {}.", "a blurry photo of {}.", "a photo of {} at night.",
             "a security camera frame showing {}.", "a low resolution photo of {}.", "a close-up photo of {}.",
             "a wide-angle photo of {}."]

PROMPTS = {
    "v1": {
        "fire": ["fire", "flames", "a building on fire", "a forest fire", "burning vehicle"],
        "smoke": ["smoke", "thick grey smoke rising", "a smoke plume", "wildfire smoke on a hillside"],
        "none": ["a normal street", "a normal room", "a forest", "fog", "steam from a pipe", "clouds", "a sunset",
                 "dust in the air", "car headlights at night", "festival lights", "mist over a valley", "an empty field"],
    },
    "v2": {
        "fire": ["fire", "flames", "a building on fire", "a house fire", "a forest fire", "a wildfire spreading",
                 "a burning car", "a fire at night", "a fire inside a room", "a kitchen fire", "a large blaze"],
        "smoke": ["smoke", "thick grey smoke rising", "black smoke from a fire", "a smoke plume",
                  "wildfire smoke on a hillside", "smoke filling a room"],
        # a-priori look-alikes and normal scenes; each is its own concept (not averaged)
        "none": ["a normal street", "a normal room", "an empty kitchen", "an office", "a forest", "a mountain landscape",
                 "city buildings", "an empty field", "fog", "mist over a valley", "smog over a city", "a sandstorm",
                 "dust in the air", "rain", "lightning in the sky", "dark storm clouds", "clouds", "a sunset",
                 "an orange sunset sky", "steam from a pipe", "steam from a cup", "car headlights at night",
                 "street lights at night", "festival lights", "a candle flame", "a lit candle on a table",
                 "a lighter flame", "a lit matchstick", "a birthday cake with candles", "orange autumn leaves",
                 "an orange object"],
    },
}


def load_images(path):
    d = np.load(path, allow_pickle=True)
    X = d["images"]
    if X.ndim == 5:                       # (N,T,C,H,W) -> middle frame
        X = X[:, X.shape[1] // 2]
    Y = d["labels"] if "labels" in d.files else None
    blk = d["block"].astype(str) if "block" in d.files else np.array(["0_0"] * len(X))
    return X.astype(np.float32), Y, blk


def labels(Y, target):
    if Y is None:
        return None
    if Y.ndim == 1:
        return Y.astype(int)
    return (Y.max(1) if target == "any" else Y[:, 0]).astype(int)


@torch.no_grad()
def concept_text_features(model, tokenizer, device, prompts):
    """One normalized vector per concept (mean over templates). Returns (feats (K,D), tags (K,) in fire/smoke/none)."""
    feats, tags = [], []
    for tag, names in prompts.items():
        for n in names:
            toks = tokenizer([t.format(n) for t in TEMPLATES]).to(device)
            f = F.normalize(model.encode_text(toks).float(), dim=-1).mean(0)
            feats.append(F.normalize(f, dim=-1)); tags.append(tag)
    return torch.stack(feats), np.array(tags)


@torch.no_grad()
def embed(model, X, mean, std, device, size, bs=64):
    """Normalized CLIP image embeddings (N,D), fp16 autocast on GPU."""
    out = []
    m = torch.tensor(mean, device=device).view(1, 3, 1, 1); s = torch.tensor(std, device=device).view(1, 3, 1, 1)
    use_amp = device.type == "cuda"
    for i in range(0, len(X), bs):
        x = torch.tensor(X[i:i + bs], device=device)
        if x.shape[-1] != size or x.shape[-2] != size:
            x = F.interpolate(x, size=(size, size), mode="bicubic", align_corners=False).clamp(0, 1)
        with torch.autocast("cuda", dtype=torch.float16, enabled=use_amp):
            e = model.encode_image((x - m) / s)
        out.append(F.normalize(e.float(), dim=-1).cpu().numpy())
    return np.concatenate(out)


def zs_prob(E, text, tags, scale, target):
    """Hazard probability = softmax mass on fire (+ smoke) concepts, softmax over ALL concepts."""
    logits = scale * (torch.tensor(E) @ text.cpu().T)
    P = torch.softmax(logits, dim=-1).numpy()
    haz = (tags == "fire") | ((tags == "smoke") if target == "any" else False)
    return P[:, haz].sum(1)


def _fit_probe(Xtr, ytr, C):
    from sklearn.linear_model import LogisticRegression
    return LogisticRegression(C=C, max_iter=3000).fit(Xtr, ytr)


def _gate(name, y, prob_raw, prob_cal, blk):
    """Admission on the cross-fit calibrated probability (deployed form); raw verdict kept for comparison."""
    prob_raw = np.where(np.isnan(prob_raw), np.nanmean(prob_raw), prob_raw)
    pc = np.where(np.isnan(prob_cal), prob_raw, prob_cal)
    rep = admit_model(name, AdmissionInputs(y_true=y, p_model=pc, block_ids=blk, X_baseline=pc.reshape(-1, 1)))
    raw = admit_model(name, AdmissionInputs(y_true=y, p_model=prob_raw, block_ids=blk, X_baseline=prob_raw.reshape(-1, 1)))
    rep["gate_input"] = "crossfit_calibrated_oof"
    rep["gate_raw"] = {"admitted": raw.get("admitted"), "value_score_model": raw.get("value_score_model"),
                       "baselines": raw.get("baselines")}
    return rep


def _finish(name, tag, out, seed, folds, y, blk, fold_of_row, prob, test, stress_sets, score_fn, meta_extra, dry_run,
            video=None):
    """Save OOF + admission report for one expert. score_fn(X) -> raw hazard prob for held-out / stress images.
    Also writes <tag>_rows.npz with PER-ROW raw probabilities on every stress set and on the video frames
    (keys stress:<set>:prob / :y, video:prob / :y / :block / :frame_idx, T_all) so kaggle/crossmodal_fusion.py
    can stack experts on confusers and run the temporal validator on every expert's frame stream."""
    tp = ty = tb = None
    if test is not None:
        Xt, ty, tb = test; tp = score_fn(Xt)
    meta = save_oof(os.path.join(out, f"{tag}_oof.npz"), name=name, seed=seed, folds=folds, prob=prob, y=y,
                    block=blk, fold_of_row=fold_of_row, test_prob=tp, test_y=ty, test_block=tb, extra_meta=meta_extra)
    oof = np.load(os.path.join(out, f"{tag}_oof.npz"))
    report = _gate(name, y, prob, oof["prob_cal"], blk)
    m = ~np.isnan(oof["prob_cal"])
    report.update(meta["metrics"])
    report.update(run_id=meta["run_id"], seed=seed, dry_run=dry_run, **{k: v for k, v in meta_extra.items() if k not in ("data", "dry_run")},
                  ece_raw=expected_calibration_error(prob, y),
                  ece_crossfit_calibrated=expected_calibration_error(oof["prob_cal"][m], y[m]))
    if test is not None and ty is not None:
        report["test_ece_calibrated"] = expected_calibration_error(oof["test_prob_cal"], ty)
    T_all = fit_temperature(prob[~np.isnan(prob)], y[~np.isnan(prob)])
    rows = {"T_all": np.asarray(T_all)}
    if stress_sets:
        report["stress"] = {}
        for sname, (Xs, ys) in stress_sets.items():
            ps = score_fn(Xs)
            report["stress"][sname] = stress_summary(ps, ys, T_all)
            rows[f"stress:{sname}:prob"] = np.asarray(ps, float); rows[f"stress:{sname}:y"] = np.asarray(ys, float)
    if video is not None:
        Ev, yv, bv, fv = video
        rows.update({"video:prob": np.asarray(score_fn(Ev), float), "video:y": np.asarray(yv, float),
                     "video:block": np.asarray(bv).astype(str), "video:frame_idx": np.asarray(fv)})
    np.savez_compressed(os.path.join(out, f"{tag}_rows.npz"), **rows)
    with open(os.path.join(out, f"{tag}_report.json"), "w") as f:
        json.dump(report, f, indent=2, default=float)
    print(json.dumps({k: report[k] for k in ("name", "admitted", "oof_roc_auc", "oof_recall_at_fpr05", "test_roc_auc",
                                             "value_score_model", "ece_crossfit_calibrated") if k in report}, indent=2, default=float))
    return report


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True); ap.add_argument("--out", default="/kaggle/working")
    ap.add_argument("--test", default=None)
    ap.add_argument("--model", default="ViT-L-14"); ap.add_argument("--pretrained", default="laion2b_s32b_b82k")
    ap.add_argument("--prompts", default="v2", choices=sorted(PROMPTS))
    ap.add_argument("--target", default="any", choices=["fire", "any"])
    ap.add_argument("--folds", type=int, default=5); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--probe", action="store_true", help="also train a few-shot logistic probe on CLIP embeddings")
    ap.add_argument("--probe-out", default=None); ap.add_argument("--probe-C", type=float, default=1.0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--stress", nargs="*", default=[], help="confuser .npz files -> false-alarm rates")
    ap.add_argument("--video", default=None, help="FireSense frames .npz (build_npz.py video): per-frame scores -> <tag>_rows.npz")
    a = ap.parse_args(argv)
    import open_clip

    ensure_dir(a.out); set_seed(a.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, _, _ = open_clip.create_model_and_transforms(a.model, pretrained=None if a.dry_run else a.pretrained)
    tokenizer = open_clip.get_tokenizer(a.model)
    model = model.to(device).eval()
    pcfg = getattr(model.visual, "preprocess_cfg", {}) or {}
    mean = pcfg.get("mean", (0.48145466, 0.4578275, 0.40821073)); std = pcfg.get("std", (0.26862954, 0.26130258, 0.27577711))
    size = model.visual.image_size[0] if isinstance(model.visual.image_size, (tuple, list)) else model.visual.image_size
    text, tags = concept_text_features(model, tokenizer, device, PROMPTS[a.prompts])
    scale = float(model.logit_scale.exp()) if hasattr(model, "logit_scale") else 100.0
    print(f"[zeroshot] model={a.model}/{a.pretrained} size={size} prompts={a.prompts} concepts={len(tags)} device={device}")

    X, Y, blk = load_images(a.data)
    print(f"[zeroshot] train/OOF images {X.shape} (native {X.shape[-1]} px -> {size} px)")
    px_in = int(X.shape[-1])
    E = embed(model, X, mean, std, device, size); del X
    y = labels(Y, a.target)
    fold_of_row = np.full(len(E), -1)
    for k, (_, va) in enumerate(spatial_block_kfold(blk, k=a.folds, seed=a.seed)):
        fold_of_row[np.asarray(va)] = k

    test = None
    if a.test:
        Xt, Yt, tb = load_images(a.test); test = (embed(model, Xt, mean, std, device, size), labels(Yt, a.target), tb); del Xt
    stress = {}
    for sf in a.stress:
        Xs, Ys, _ = load_images(sf); stress[Path(sf).stem] = (embed(model, Xs, mean, std, device, size), labels(Ys, a.target)); del Xs

    video = None
    if a.video and os.path.exists(a.video):
        dv = np.load(a.video, allow_pickle=True)
        Xv, Yv, bv = load_images(a.video)
        fv = dv["frame_idx"] if "frame_idx" in dv.files else np.arange(len(Xv))
        video = (embed(model, Xv, mean, std, device, size), labels(Yv, a.target), bv, fv); del Xv
        print(f"[zeroshot] video frames embedded: {len(fv)} frames, {len(set(bv.tolist()))} videos")
    common = {"model": a.model, "pretrained": None if a.dry_run else a.pretrained, "target": a.target, "data": a.data,
              "image_px_in": px_in, "image_px_model": int(size), "prompt_version": a.prompts,
              "stress_note": ("v2 prompts name confuser categories a priori (candle, lightning, fog, sandstorm, rain ...); "
                              "stress false-alarm rates are therefore not blind") if a.prompts == "v2" else "v1 prompts"}
    zs_fn = lambda Em: zs_prob(Em, text, tags, scale, a.target)          # noqa: E731
    _finish("zeroshot", f"zeroshot_s{a.seed}", a.out, a.seed, a.folds, y, blk, fold_of_row, zs_fn(E), test, stress,
            zs_fn, {**common, "dry_run": a.dry_run}, a.dry_run, video=video)

    if a.probe:
        pout = a.probe_out or os.path.join(a.out, "..", "clip_probe"); ensure_dir(pout)
        oof = np.full(len(E), np.nan)
        for k in sorted(set(fold_of_row.tolist()) - {-1}):
            tr, va = fold_of_row != k, fold_of_row == k
            if len(set(y[tr].tolist())) < 2:
                continue
            oof[va] = _fit_probe(E[tr], y[tr], a.probe_C).predict_proba(E[va])[:, 1]
        full = _fit_probe(E[~np.isnan(oof)], y[~np.isnan(oof)], a.probe_C)   # held-out / stress use a full-data fit
        pr_fn = lambda Em: full.predict_proba(Em)[:, 1]                      # noqa: E731
        _finish("clip_probe", f"clip_probe_s{a.seed}", pout, a.seed, a.folds, y, blk, fold_of_row, oof, test, stress,
                pr_fn, {**common, "probe_C": a.probe_C, "few_shot": True,
                        "note": "logistic probe on frozen CLIP embeddings; uses labels (NOT zero-shot); same group folds"},
                a.dry_run, video=video)


if __name__ == "__main__":
    main()
