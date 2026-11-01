"""Video-level evaluation of the trained fire CNN WITH vs WITHOUT the temporal validator (ws4_cctv).

Input: per-frame series built by `data_adapters/build_npz.py video --clip 1 --every K` (FireSense .avi; block =
video id; frame_idx = source frame number). For every video it runs the fold-ensemble CNN per frame
(calibrated with the temperature fitted on the training OOF), then:
  RAW       : alarm if ANY frame prob >= thr
  VALIDATED : alarm if TemporalValidator(window, min_frames, thr) confirms at any point (persistence check)
Reports video-level detection rate (positive videos), false-alarm rate (negative videos) and first-alarm frame.
Run: python kaggle/eval_video.py --frames npz/firesense_frames.npz --models out/fire --seed 0 --out out/video
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

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from trinetra.deep.fire_cnn import FireSmokeNet, FireNetConfig        # noqa: E402
from trinetra.deep.oof_utils import fit_temperature, sigmoid, logit, ensure_dir  # noqa: E402
from trinetra.ws4_cctv import TemporalValidator                        # noqa: E402


@torch.no_grad()
def frame_probs(models, X, device, target, bs=256):
    out = []
    for i in range(0, len(X), bs):
        xb = torch.tensor(X[i:i + bs]).to(device)
        ps = []
        for m in models:
            p = m(xb)["prob"]
            ps.append((p.max(1).values if target == "any" else p[:, 0]).cpu().numpy())
        out.append(np.mean(ps, 0))
    return np.concatenate(out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", required=True); ap.add_argument("--models", required=True)
    ap.add_argument("--model-name", default="fire"); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--target", default="any", choices=["fire", "any"])
    ap.add_argument("--thr", type=float, default=0.5); ap.add_argument("--window", type=int, default=5)
    ap.add_argument("--min-frames", type=int, default=3); ap.add_argument("--out", default="/kaggle/working/out/video")
    a = ap.parse_args(argv)
    ensure_dir(a.out)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    ckpts = sorted(glob.glob(os.path.join(a.models, f"{a.model_name}_s{a.seed}_fold*.pt")))
    if not ckpts:
        raise SystemExit(f"no checkpoints {a.model_name}_s{a.seed}_fold*.pt in {a.models}")
    models = []
    for c in ckpts:
        m = FireSmokeNet(FireNetConfig()); m.load_state_dict(torch.load(c, map_location=device)); models.append(m.to(device).eval())
    oof = np.load(os.path.join(a.models, f"{a.model_name}_s{a.seed}_oof.npz"), allow_pickle=True)
    T = fit_temperature(oof["prob"], oof["y"])
    d = np.load(a.frames, allow_pickle=True)
    X = d["images"]; Y = d["labels"]; vid = d["block"].astype(str); fidx = d["frame_idx"] if "frame_idx" in d.files else np.arange(len(X))
    p = sigmoid(logit(frame_probs(models, X, device, a.target)) / T)
    rows = []
    for v in sorted(set(vid)):
        idx = np.where(vid == v)[0]; idx = idx[np.argsort(fidx[idx])]
        y = int((Y[idx].max(1) if a.target == "any" else Y[idx, 0]).max())
        pv = p[idx]
        raw_hits = np.where(pv >= a.thr)[0]
        tv = TemporalValidator(window=a.window, min_frames=a.min_frames, conf_thr=a.thr)
        val_hits = [k for k, q in enumerate(pv) if tv.update(float(q)).confirmed]
        rows.append({"video": v, "label": y, "n_frames": len(idx), "max_prob": float(pv.max()),
                     "raw_alarm": int(len(raw_hits) > 0), "validated_alarm": int(len(val_hits) > 0),
                     "raw_first_frame": int(fidx[idx][raw_hits[0]]) if len(raw_hits) else -1,
                     "validated_first_frame": int(fidx[idx][val_hits[0]]) if val_hits else -1,
                     "raw_alarm_frames": int(len(raw_hits)), "validated_alarm_frames": int(len(val_hits))})
    pos = [r for r in rows if r["label"] == 1]; neg = [r for r in rows if r["label"] == 0]
    rate = lambda rs, k: float(np.mean([r[k] for r in rs])) if rs else None  # noqa: E731
    rep = {"name": "video_temporal", "seed": a.seed, "n_videos": len(rows), "n_pos": len(pos), "n_neg": len(neg),
           "thr": a.thr, "window": a.window, "min_frames": a.min_frames, "temperature": T,
           "detect_rate_raw": rate(pos, "raw_alarm"), "detect_rate_validated": rate(pos, "validated_alarm"),
           "false_alarm_video_rate_raw": rate(neg, "raw_alarm"), "false_alarm_video_rate_validated": rate(neg, "validated_alarm"),
           "false_alarm_frames_raw": int(sum(r["raw_alarm_frames"] for r in neg)),
           "false_alarm_frames_validated": int(sum(r["validated_alarm_frames"] for r in neg)),
           "note": "video-level, FireSense; small n -> report counts, not just rates"}
    with open(os.path.join(a.out, f"video_s{a.seed}_per_video.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    json.dump(rep, open(os.path.join(a.out, f"video_s{a.seed}_report.json"), "w"), indent=2)
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()
