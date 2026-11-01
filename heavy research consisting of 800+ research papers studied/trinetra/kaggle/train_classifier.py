"""Kaggle kernel: train a classifier model (fire | eo | deepfake) with spatial-CV + calibration + gate.

Run:  python kaggle/train_classifier.py --model fire --data <.npz> --out /kaggle/working
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

from trinetra.deep.datamodules import ImageFolderNPZ                       # noqa: E402
from trinetra.deep.fire_cnn import FireSmokeNet, FireNetConfig            # noqa: E402
from trinetra.deep.eo_encoder import EODownstream, EOConfig               # noqa: E402
from trinetra.deep.deepfake_net import AuthenticityNet, DeepfakeConfig    # noqa: E402
from trinetra.deep.train import (                                          # noqa: E402
    TrainConfig, set_seed, get_device, train_one_fold, TemperatureScaler,
    admit_model, AdmissionInputs, spatial_cv_indices, make_loader, setup_perf, n_gpus,
)


def build(model_name: str):
    if model_name == "fire":
        m = FireSmokeNet(FireNetConfig())

        def step(model, b):
            out = model(b["x"]); return model.loss(out, b["y"])

        def prob(model, b):            # positive = fire channel 0
            return model(b["x"])["prob"][:, 0]
        return m, step, prob
    if model_name == "eo":
        m = EODownstream(EOConfig())

        def step(model, b):
            out = model(b["x"]); return {"loss": model.loss(out, b["y"])}

        def prob(model, b):
            return model(b["x"])["prob"].squeeze(-1)
        return m, step, prob
    if model_name == "deepfake":
        m = AuthenticityNet(DeepfakeConfig())

        def step(model, b):
            out = model(b["x"]); return {"loss": model.loss(out, b["y"])}

        def prob(model, b):
            return model(b["x"])["p_fake"]
        return m, step, prob
    raise SystemExit(f"unknown model {model_name!r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=["fire", "eo", "deepfake"])
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="/kaggle/working")
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--batch", type=int, default=64, help="PER-GPU batch (effective = batch * n_gpus)")
    ap.add_argument("--parallel", default="auto", choices=["auto", "dp", "none"])
    args = ap.parse_args()

    set_seed(0); setup_perf(); device = get_device()
    cfg = TrainConfig(epochs=args.epochs, batch_size=args.batch, parallel=args.parallel)
    print(f"[trinetra] GPUs visible={n_gpus()} | DataParallel={cfg.use_dp()} | "
          f"effective_batch={cfg.effective_batch()} lr={cfg.effective_lr():.2e}")
    ds = ImageFolderNPZ(args.data)
    oof_prob = np.full(len(ds), np.nan); oof_block = np.array(ds.block)

    for fold, (tr, va) in enumerate(spatial_cv_indices(ds, cfg.k_folds, cfg.seed)):
        model, step, prob = build(args.model)
        tl = make_loader(ds, cfg, shuffle=True, indices=tr)
        train_one_fold(model, step, tl, cfg, device)
        model.eval().to(device)
        with torch.no_grad():
            for i in va:
                b = {"x": ds[i]["x"][None].to(device)}
                oof_prob[i] = float(prob(model, b).squeeze())
        torch.save(model.state_dict(), os.path.join(args.out, f"{args.model}_fold{fold}.pt"))

    if ds.y is not None:
        y = (ds.y[:, 0] if ds.y.ndim > 1 else ds.y).astype(int)
        X = oof_prob.reshape(-1, 1)                 # 1-feature baseline over the model's own score
        report = admit_model(args.model, AdmissionInputs(
            y_true=y, p_model=oof_prob, block_ids=oof_block, X_baseline=X))
        with open(os.path.join(args.out, f"{args.model}_report.json"), "w") as f:
            json.dump(report, f, indent=2)
        print(json.dumps(report, indent=2))
    else:
        print("No labels -> admission gate skipped (Rule 16).")


if __name__ == "__main__":
    main()
