"""CROSS-MODAL fire fusion: per-frame / per-confuser stack of fire_cnn + zeroshot + clip_probe, then the temporal
validator (ws4_cctv.TemporalValidator) on EVERY stream -> video-level detection / false alarms, and confuser false
alarms per expert vs the stack vs a 2-of-3 vote.

Why: on the same-image OOF set the stack did not beat clip_probe (results/fire_meta). Fusion can only add
information where experts disagree on hard negatives (confusers) or across TIME (video). This measures exactly that.

Inputs
  --fire-models DIR   fire_s<seed>_fold*.pt + fire_s<seed>_oof.npz (account A output)
  --zs-dir / --clip-dir  zeroshot_s0_oof.npz + zeroshot_s0_rows.npz, clip_probe_s0_oof.npz + clip_probe_s0_rows.npz
                      (eval_zeroshot.py --video ... writes the *_rows.npz with per-row stress + per-frame scores)
  --frames            firesense_frames.npz (build_npz.py video; block = video id, frame_idx)
  --stress            the same confuser .npz files given to eval_zeroshot.py (only needed for fire_cnn scores)
Stack: L2 logistic on [logit p_i, sd, range] (same features as fire_meta_fusion.py) fitted on the REAL-paired
OOF rows (fire_cnn seed + zeroshot + clip_probe). If this session's zeroshot OOF rows are not aligned with the
attached fire OOF (fire.npz rebuilt differently), the repo copies in results/fire_meta/inputs are used.
Every expert stream is calibrated with its own OOF temperature; the stack with the temperature of its OOF output.
Output: crossmodal_s<seed>_report.json, crossmodal_s<seed>_compare.md, crossmodal_s<seed>_per_video.csv
Run: python kaggle/crossmodal_fusion.py --fire-models out/fire --zs-dir out/zeroshot --clip-dir out/clip_probe \
        --frames npz/firesense_frames.npz --stress npz/stress_*.npz --seed 0 --out out/crossmodal
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import sys
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src")); sys.path.insert(0, str(HERE))

from fire_meta_fusion import features                                       # noqa: E402
from trinetra.deep.oof_utils import fit_temperature, logit, sigmoid, ensure_dir  # noqa: E402
from trinetra.eval import LogisticNumpy                                    # noqa: E402
from trinetra.ws4_cctv import TemporalValidator                             # noqa: E402

P_STAR = 5.0 / 105.0
REPO_INPUTS = HERE.parents[1] / "results" / "fire_meta" / "inputs"
EXPERTS = ("fire_cnn", "zeroshot", "clip_probe")


def _images(path):
    """Images in the fire CNN layout (N, T, C, H, W); 4-D sets get T = 1 (same as build_npz.py --clip 1)."""
    X = np.load(path, allow_pickle=True)["images"]
    return (X[:, None] if X.ndim == 4 else X).astype(np.float32)


def fire_cnn_scorer(models_dir, seed, device):
    from eval_video import frame_probs                                      # lazy: needs the fire CNN code only
    from trinetra.deep.fire_cnn import FireSmokeNet, FireNetConfig
    ckpts = sorted(glob.glob(os.path.join(models_dir, f"fire_s{seed}_fold*.pt")))
    if not ckpts:
        raise SystemExit(f"no fire_s{seed}_fold*.pt in {models_dir} (attach the A run output)")
    ms = []
    for c in ckpts:
        m = FireSmokeNet(FireNetConfig()); m.load_state_dict(torch.load(c, map_location=device)); ms.append(m.to(device).eval())
    return lambda X: frame_probs(ms, X, device, "any")


def load_oof(p):
    d = np.load(p, allow_pickle=True)
    return d["prob"].astype(float), d["y"].astype(int), d["block"].astype(str)


def fit_stack(fire_oof, zs_oof, clip_oof):
    """Returns (stack model, stack T, per-expert T dict, pairing note)."""
    F, Z, C = load_oof(fire_oof), load_oof(zs_oof), load_oof(clip_oof)
    if not all(np.array_equal(F[2], o[2]) and np.array_equal(F[1], o[1]) for o in (Z, C)):
        raise ValueError("OOF rows not aligned")
    P = np.column_stack([F[0], Z[0], C[0]]); y = F[1]
    ok = ~np.isnan(P).any(1); P, y = P[ok], y[ok]
    m = LogisticNumpy(seed=0).fit(features(P), y)
    T = fit_temperature(m.predict_proba(features(P)), y)
    Te = {n: fit_temperature(P[:, j], y) for j, n in enumerate(EXPERTS)}
    return m, T, Te, int(ok.sum())


def streams(raw, m, T, Te, thr):
    """raw: {expert: raw prob array} -> {stream: calibrated prob array} incl. stack, mean and 2-of-3 vote."""
    cal = {n: sigmoid(logit(np.clip(raw[n], 1e-6, 1 - 1e-6)) / Te[n]) for n in EXPERTS}
    P = np.column_stack([raw[n] for n in EXPERTS])
    out = {**cal, "stack": sigmoid(logit(np.clip(m.predict_proba(features(P)), 1e-6, 1 - 1e-6)) / T),
           "mean": np.mean([cal[n] for n in EXPERTS], 0)}
    votes = np.sum([cal[n] >= thr for n in EXPERTS], 0)
    out["vote_2of3"] = np.where(votes >= 2, np.maximum.reduce([cal[n] for n in EXPERTS]), np.minimum.reduce([cal[n] for n in EXPERTS]))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fire-models", required=True); ap.add_argument("--zs-dir", required=True); ap.add_argument("--clip-dir", required=True)
    ap.add_argument("--frames", required=True); ap.add_argument("--stress", nargs="*", default=[])
    ap.add_argument("--seed", type=int, default=0); ap.add_argument("--thr", type=float, default=0.5)
    ap.add_argument("--window", type=int, default=5); ap.add_argument("--min-frames", type=int, default=3)
    ap.add_argument("--out", default="/kaggle/working/out/crossmodal")
    a = ap.parse_args(argv)
    ensure_dir(a.out)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    fire_oof = os.path.join(a.fire_models, f"fire_s{a.seed}_oof.npz")
    zs_oof, clip_oof = os.path.join(a.zs_dir, "zeroshot_s0_oof.npz"), os.path.join(a.clip_dir, "clip_probe_s0_oof.npz")
    try:
        m, T, Te, n_fit = fit_stack(fire_oof, zs_oof, clip_oof); pairing = "this session's zeroshot/clip OOF (aligned)"
    except (ValueError, FileNotFoundError) as e:
        print(f"[crossmodal] {e}; using repo copies in {REPO_INPUTS}")
        m, T, Te, n_fit = fit_stack(REPO_INPUTS / f"fire_s{a.seed}_oof.npz", REPO_INPUTS / "zeroshot_s0_oof.npz",
                                    REPO_INPUTS / "clip_probe_s0_oof.npz")
        pairing = "repo results/fire_meta/inputs OOF (A final + F final)"
    print(f"[crossmodal] stack fitted on {n_fit} REAL-paired OOF rows ({pairing}); T={T:.3f}; weights {np.round(m.w, 2).tolist()}")
    score_cnn = fire_cnn_scorer(a.fire_models, a.seed, device)
    zr = np.load(os.path.join(a.zs_dir, "zeroshot_s0_rows.npz"), allow_pickle=True)
    cr = np.load(os.path.join(a.clip_dir, "clip_probe_s0_rows.npz"), allow_pickle=True)

    # ---------------- confusers / held-out sets (per-row) ----------------
    stress = {}
    for sf in a.stress:
        name = Path(sf).stem; k = f"stress:{name}:prob"
        if k not in zr.files or k not in cr.files:
            print(f"[crossmodal] {name}: no per-row CLIP scores (re-run eval_zeroshot.py) -> skipped"); continue
        y = zr[f"stress:{name}:y"].astype(int)
        raw = {"fire_cnn": score_cnn(_images(sf)), "zeroshot": zr[k], "clip_probe": cr[k]}
        S = streams(raw, m, T, Te, a.thr); neg, pos = y == 0, y == 1
        stress[name] = {"n": int(len(y)), "n_neg": int(neg.sum()), "n_pos": int(pos.sum()), "streams": {
            s: {"fa_rate_at_thr": float((p[neg] >= a.thr).mean()) if neg.any() else None,
                "fa_rate_at_pstar": float((p[neg] >= P_STAR).mean()) if neg.any() else None,
                "recall_at_thr": float((p[pos] >= a.thr).mean()) if pos.any() else None} for s, p in S.items()}}
        print(f"[crossmodal] {name}: FA@{a.thr} " + ", ".join(f"{s} {v['fa_rate_at_thr']:.3f}" for s, v in stress[name]["streams"].items()
                                                              if v["fa_rate_at_thr"] is not None))

    # ---------------- video: per-frame streams -> raw vs temporal-validated alarms per video ----------------
    d = np.load(a.frames, allow_pickle=True)
    vid = d["block"].astype(str); fidx = d["frame_idx"] if "frame_idx" in d.files else np.arange(len(vid))
    if "video:prob" not in zr.files or not np.array_equal(zr["video:block"], vid):
        raise SystemExit("zeroshot rows have no video scores aligned with --frames (run eval_zeroshot.py --video)")
    Y = d["labels"]; yf = (Y.max(1) if Y.ndim > 1 else Y).astype(int)
    raw = {"fire_cnn": score_cnn(_images(a.frames)), "zeroshot": zr["video:prob"], "clip_probe": cr["video:prob"]}
    S = streams(raw, m, T, Te, a.thr)
    rows, video = [], {}
    for s, p in S.items():
        res = []
        for v in sorted(set(vid)):
            idx = np.where(vid == v)[0]; idx = idx[np.argsort(fidx[idx])]
            pv = p[idx]; tv = TemporalValidator(window=a.window, min_frames=a.min_frames, conf_thr=a.thr)
            val = [k for k, q in enumerate(pv) if tv.update(float(q)).confirmed]
            raw_hits = np.where(pv >= a.thr)[0]
            r = {"stream": s, "video": v, "label": int(yf[idx].max()), "n_frames": int(len(idx)),
                 "raw_alarm": int(len(raw_hits) > 0), "validated_alarm": int(len(val) > 0),
                 "raw_alarm_frames": int(len(raw_hits)), "validated_alarm_frames": int(len(val)),
                 "validated_first_frame": int(fidx[idx][val[0]]) if val else -1}
            res.append(r); rows.append(r)
        P_, N_ = [r for r in res if r["label"] == 1], [r for r in res if r["label"] == 0]
        mean = lambda rs, k: float(np.mean([r[k] for r in rs])) if rs else None  # noqa: E731
        video[s] = {"detect_raw": mean(P_, "raw_alarm"), "detect_validated": mean(P_, "validated_alarm"),
                    "fa_video_raw": mean(N_, "raw_alarm"), "fa_video_validated": mean(N_, "validated_alarm"),
                    "fa_frames_validated": int(sum(r["validated_alarm_frames"] for r in N_)),
                    "detected_videos_validated": int(sum(r["validated_alarm"] for r in P_)),
                    "false_alarm_videos_validated": int(sum(r["validated_alarm"] for r in N_)),
                    "n_pos": len(P_), "n_neg": len(N_)}
    # balanced video-level score: Youden J = detect - false alarm (validated); small n -> counts are in the table too
    best = max(video, key=lambda s: video[s]["detect_validated"] - video[s]["fa_video_validated"])
    rep = {"name": "crossmodal", "seed": a.seed, "stack_pairing": pairing, "stack_n_fit": n_fit, "thr": a.thr,
           "window": a.window, "min_frames": a.min_frames, "video": video, "stress": stress, "best_video_stream_by_J": best,
           "stack_video_J": video["stack"]["detect_validated"] - video["stack"]["fa_video_validated"],
           "clip_video_J": video["clip_probe"]["detect_validated"] - video["clip_probe"]["fa_video_validated"],
           "fire_cnn_video_J": video["fire_cnn"]["detect_validated"] - video["fire_cnn"]["fa_video_validated"],
           "detect_rate_validated": video["stack"]["detect_validated"],
           "false_alarm_video_rate_validated": video["stack"]["fa_video_validated"],
           "n_videos": video["stack"]["n_pos"] + video["stack"]["n_neg"],
           "note": "FireSense 49 videos: small n, quote counts; stress sets are confusers (negatives) unless n_pos > 0"}
    json.dump(rep, open(os.path.join(a.out, f"crossmodal_s{a.seed}_report.json"), "w"), indent=2)
    with open(os.path.join(a.out, f"crossmodal_s{a.seed}_per_video.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    L = [f"# Cross-modal fire fusion · seed {a.seed} · stack on {n_fit} REAL-paired OOF rows ({pairing})", "",
         f"## Video (FireSense, temporal validator window {a.window}, min {a.min_frames} frames, thr {a.thr})", "",
         "| stream | detect raw | detect validated | FA videos raw | FA videos validated | detected / FA videos (validated) | FA frames |",
         "|---|---|---|---|---|---|---|"]
    for s, v in video.items():
        L.append(f"| {s} | {v['detect_raw']:.3f} | {v['detect_validated']:.3f} | {v['fa_video_raw']:.3f} | {v['fa_video_validated']:.3f} "
                 f"| {v['detected_videos_validated']}/{v['n_pos']} · {v['false_alarm_videos_validated']}/{v['n_neg']} | {v['fa_frames_validated']} |")
    L += ["", f"Best stream by (detect − FA), validated: **{best}**.", "", f"## Confusers / held-out sets (false-alarm rate at {a.thr} and at p*)", "",
          "| set | " + " | ".join(S) + " |", "|---|" + "---|" * len(S)]
    for name, st in stress.items():
        cell = lambda v: "-" if v["fa_rate_at_thr"] is None else f"{v['fa_rate_at_thr']:.3f} / {v['fa_rate_at_pstar']:.3f}"  # noqa: E731
        L.append(f"| {name} (neg {st['n_neg']}, pos {st['n_pos']}) | " + " | ".join(cell(st["streams"][s]) for s in S) + " |")
    open(os.path.join(a.out, f"crossmodal_s{a.seed}_compare.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
