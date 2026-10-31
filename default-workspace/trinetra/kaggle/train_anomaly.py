"""Kaggle kernel: train DeepAnomaly (TCN AE + Deep-SVDD + forecast) on NORMAL telemetry; score + gate.

Run:  python kaggle/train_anomaly.py --data /kaggle/input/trinetra-telemetry/tele.npz --out /kaggle/working
Train on normal windows only; events become out-of-distribution and score high.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from trinetra.deep.datamodules import WindowNPZDataset                     # noqa: E402
from trinetra.deep.anomaly_deep import DeepAnomaly, AnomalyConfig          # noqa: E402
from trinetra.deep.train import (                                          # noqa: E402
    TrainConfig, set_seed, get_device, train_one_fold, admit_model, AdmissionInputs,
    spatial_cv_indices, make_loader, setup_perf, n_gpus,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="/kaggle/working")
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--batch", type=int, default=64, help="PER-GPU batch (effective = batch * n_gpus)")
    ap.add_argument("--parallel", default="auto", choices=["auto", "dp", "none"])
    args = ap.parse_args()

    set_seed(0); setup_perf(); device = get_device()
    cfg = TrainConfig(epochs=args.epochs, batch_size=args.batch, parallel=args.parallel)
    print(f"[trinetra] GPUs visible={n_gpus()} | DataParallel={cfg.use_dp()} | "
          f"effective_batch={cfg.effective_batch()} lr={cfg.effective_lr():.2e}")
    ds = WindowNPZDataset(args.data)
    n_feat = ds.X.shape[1]
    oof_score = np.full(len(ds), np.nan); oof_block = np.array(ds.block)

    def step(model, b):
        return model.loss(b["x"])

    for fold, (tr, va) in enumerate(spatial_cv_indices(ds, cfg.k_folds, cfg.seed)):
        model = DeepAnomaly(AnomalyConfig(n_feat=n_feat))
        # train on NORMAL only (y==0) within the train split, if labels exist
        tr_normal = [i for i in tr if ds.y is None or ds.y[i] == 0]
        tl = make_loader(ds, cfg, shuffle=True, indices=tr_normal)
        model.to(device).init_center(tl, device)
        train_one_fold(model, step, tl, cfg, device)
        model.eval()
        with torch.no_grad():
            for i in va:
                oof_score[i] = float(model.anomaly_score(ds[i]["x"][None].to(device)).squeeze())
        torch.save(model.state_dict(), os.path.join(args.out, f"anomaly_fold{fold}.pt"))

    if ds.y is not None:
        y = ds.y.astype(int)
        # normalize score to [0,1] as a probability-like signal for the gate
        s = oof_score; p = (s - np.nanmin(s)) / (np.nanmax(s) - np.nanmin(s) + 1e-9)
        report = admit_model("deep_anomaly", AdmissionInputs(
            y_true=y, p_model=p, block_ids=oof_block, X_baseline=p.reshape(-1, 1)))
        with open(os.path.join(args.out, "anomaly_report.json"), "w") as f:
            json.dump(report, f, indent=2)
        print(json.dumps(report, indent=2))
    else:
        print("Unsupervised run complete; no labels -> admission gate skipped (Rule 16).")


if __name__ == "__main__":
    main()
