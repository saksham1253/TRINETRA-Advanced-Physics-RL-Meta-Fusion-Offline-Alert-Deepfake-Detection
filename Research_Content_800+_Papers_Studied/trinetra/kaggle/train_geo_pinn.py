"""Kaggle kernel: train Geo-PINN with spatial-CV + physics loss + honesty admission gate.

Run:  python kaggle/train_geo_pinn.py --data /kaggle/input/trinetra-geo/geo.npz --out /kaggle/working
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

from trinetra.deep.geo_pinn import GeoPINN, GeoPINNConfig, geo_pinn_step  # noqa: E402
from trinetra.deep.datamodules import GeoSeriesDataset                     # noqa: E402
from trinetra.deep.train import (                                          # noqa: E402
    TrainConfig, set_seed, get_device, train_one_fold, TemperatureScaler,
    admit_model, AdmissionInputs, spatial_cv_indices, make_loader, setup_perf, n_gpus,
)
from trinetra.ws1b_geophys import diffusivity_D1                           # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="/kaggle/working")
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--D0", type=float, default=2e-4)
    ap.add_argument("--beta_deg", type=float, default=35.0)
    ap.add_argument("--batch", type=int, default=64, help="PER-GPU batch (effective = batch * n_gpus)")
    ap.add_argument("--parallel", default="auto", choices=["auto", "dp", "none"])
    args = ap.parse_args()

    set_seed(0); setup_perf()
    device = get_device()
    cfg = TrainConfig(epochs=args.epochs, batch_size=args.batch, parallel=args.parallel)
    print(f"[trinetra] GPUs visible={n_gpus()} | DataParallel={cfg.use_dp()} | "
          f"effective_batch={cfg.effective_batch()} lr={cfg.effective_lr():.2e}")
    ds = GeoSeriesDataset(args.data)
    D1 = diffusivity_D1(args.D0, args.beta_deg)      # slope enters ONLY via D1 (bug-guard)
    bce = torch.nn.BCEWithLogitsLoss()

    def step(model, batch):
        return geo_pinn_step(model, batch, D1=D1, bce=bce)

    oof_prob = np.full(len(ds), np.nan)
    oof_block = np.array(ds.block)
    for fold, (tr, va) in enumerate(spatial_cv_indices(ds, cfg.k_folds, cfg.seed)):
        model = GeoPINN(GeoPINNConfig())
        tl = make_loader(ds, cfg, shuffle=True, indices=tr)
        train_one_fold(model, step, tl, cfg, device)
        model.eval()
        with torch.no_grad():
            for i in va:
                b = ds[i]
                out = model(b["Z"][None].to(device), b["t"][None].to(device),
                            b["rain"][None].to(device), b["static"][None].to(device))
                oof_prob[i] = float(out["prob"].squeeze())
        torch.save(model.state_dict(), os.path.join(args.out, f"geo_pinn_fold{fold}.pt"))

    if ds.label is not None:
        y = ds.label.astype(int)
        X = ds.static
        report = admit_model("geo_pinn", AdmissionInputs(
            y_true=y, p_model=oof_prob, block_ids=oof_block, X_baseline=X))
        with open(os.path.join(args.out, "geo_pinn_report.json"), "w") as f:
            json.dump(report, f, indent=2)
        print(json.dumps(report, indent=2))
    else:
        print("No labels present -> physics-only pretraining done; admission gate skipped (Rule 16: "
              "no performance may be claimed without labels + spatial-CV).")


if __name__ == "__main__":
    main()
