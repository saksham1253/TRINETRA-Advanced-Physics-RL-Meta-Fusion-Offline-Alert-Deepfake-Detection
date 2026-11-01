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
from trinetra.deep.oof_utils import save_oof, ensure_dir                    # noqa: E402


@torch.no_grad()
def score(model, X, idx, device, bs: int = 512):
    out = []
    for s in range(0, len(idx), bs):
        out.append(model.anomaly_score(torch.tensor(X[idx[s:s + bs]]).to(device)).float().cpu().numpy().reshape(-1))
    return np.concatenate(out) if out else np.array([])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="/kaggle/working")
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--batch", type=int, default=64, help="PER-GPU batch (effective = batch * n_gpus)")
    ap.add_argument("--parallel", default="auto", choices=["auto", "dp", "none"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--num-workers", type=int, default=4)
    ap.add_argument("--test", default=None, help="untouched held-out .npz (same contract)")
    args = ap.parse_args()
    ensure_dir(args.out)

    set_seed(args.seed); setup_perf(); device = get_device()
    cfg = TrainConfig(epochs=args.epochs, batch_size=args.batch, parallel=args.parallel, seed=args.seed,
                      k_folds=args.folds, num_workers=args.num_workers)
    print(f"[trinetra] GPUs visible={n_gpus()} | DataParallel={cfg.use_dp()} | "
          f"effective_batch={cfg.effective_batch()} lr={cfg.effective_lr():.2e}")
    ds = WindowNPZDataset(args.data)
    n_feat = ds.X.shape[1]
    oof_score = np.full(len(ds), np.nan); oof_block = np.array(ds.block)
    fold_of_row = np.full(len(ds), -1)
    test = WindowNPZDataset(args.test) if args.test else None
    test_scores = []
    tag = f"anomaly_s{args.seed}"

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
        va = np.asarray(va)
        raw = score(model, ds.X, va, device)
        # BUGFIX: scores of different fold models are on different scales. Normalize each fold by the
        # 99th percentile of its OWN training-normal scores before pooling (was: one global min-max).
        ref = score(model, ds.X, np.asarray(tr_normal), device)
        scale = float(np.percentile(ref, 99)) + 1e-9 if len(ref) else 1.0
        oof_score[va] = raw / scale
        fold_of_row[va] = fold
        if test is not None:
            test_scores.append(score(model, test.X, np.arange(len(test)), device) / scale)
        torch.save(model.state_dict(), os.path.join(args.out, f"{tag}_fold{fold}.pt"))

    if ds.y is not None:
        y = ds.y.astype(int)
        # squash the normalized score to (0,1): score == training-normal p99 maps to 0.5
        p = 1.0 / (1.0 + np.exp(-4.0 * (oof_score - 1.0)))
        tp = (1.0 / (1.0 + np.exp(-4.0 * (np.mean(test_scores, 0) - 1.0)))) if test_scores else None
        meta = save_oof(os.path.join(args.out, f"{tag}_oof.npz"), name="anomaly", seed=args.seed, folds=cfg.k_folds,
                        prob=p, y=y, block=oof_block, fold_of_row=fold_of_row, test_prob=tp,
                        test_y=test.y.astype(int) if (test is not None and test.y is not None) else None,
                        test_block=test.block if test is not None else None, extra_meta={"data": args.data})
        report = admit_model("deep_anomaly", AdmissionInputs(
            y_true=y, p_model=p, block_ids=oof_block, X_baseline=p.reshape(-1, 1)))
        report.update(meta["metrics"])
        report["run_id"] = meta["run_id"]; report["seed"] = args.seed
        with open(os.path.join(args.out, f"{tag}_report.json"), "w") as f:
            json.dump(report, f, indent=2)
        print(json.dumps(report, indent=2))
    else:
        print("Unsupervised run complete; no labels -> admission gate skipped (Rule 16).")


if __name__ == "__main__":
    main()
