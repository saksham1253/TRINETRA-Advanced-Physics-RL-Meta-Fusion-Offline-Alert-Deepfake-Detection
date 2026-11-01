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
from trinetra.deep.oof_utils import save_oof, ensure_dir, fit_temperature, sigmoid, logit, stress_summary  # noqa: E402
from trinetra.eval import expected_calibration_error, value_score                       # noqa: E402


EO_KW: dict = {}


def build(model_name: str):
    if model_name == "fire":
        m = FireSmokeNet(FireNetConfig())

        def step(model, b):
            out = model(b["x"]); return model.loss(out, b["y"])

        def prob(model, b):            # positive = fire channel 0 (use --target any for fire OR smoke)
            p = model(b["x"])["prob"]
            return p.max(dim=1).values if TARGET == "any" else p[:, 0]
        return m, step, prob
    if model_name == "eo":
        # BUGFIX (B-26): EOConfig() defaulted to in_chans=6; Landslide4Sense has 14 bands, Sen1Floods11 2. Channels now
        # come from the data (set in main) and the backbone/pretrained flags are configurable.
        m = EODownstream(EOConfig(**EO_KW))

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


TARGET = "fire"


@torch.no_grad()
def predict(model, prob, X: np.ndarray, idx, device, bs: int = 256) -> np.ndarray:
    """Batched inference (the original per-sample loop was slow on 4k-image folds)."""
    out = []
    for s in range(0, len(idx), bs):
        xb = torch.tensor(X[idx[s:s + bs]]).to(device)
        out.append(prob(model, {"x": xb}).float().cpu().numpy().reshape(-1))
    return np.concatenate(out) if out else np.array([])


def _labels(Y):
    if Y is None:
        return None
    if Y.ndim > 1:
        return (Y.max(axis=1) if TARGET == "any" else Y[:, 0]).astype(int)
    return Y.astype(int)


def main():
    global TARGET
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=["fire", "eo", "deepfake"])
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="/kaggle/working")
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--batch", type=int, default=64, help="PER-GPU batch (effective = batch * n_gpus)")
    ap.add_argument("--parallel", default="auto", choices=["auto", "dp", "none"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--num-workers", type=int, default=4)
    ap.add_argument("--test", default=None, help="untouched held-out .npz (same contract); fold-ensemble scored")
    ap.add_argument("--eo-backbone", default="resnet18", help="timm backbone for --model eo")
    ap.add_argument("--eo-pretrained", type=int, default=1, help="1 = ImageNet weights via timm (internet), 0 = random")
    ap.add_argument("--eo-freeze", type=int, default=1)
    ap.add_argument("--stress", nargs="*", default=[], help="negative/confuser .npz files: report false-alarm rates")
    ap.add_argument("--target", default="fire", choices=["fire", "any"], help="fire model: fire channel or fire-or-smoke")
    args = ap.parse_args()
    TARGET = args.target
    ensure_dir(args.out)

    set_seed(args.seed); setup_perf(); device = get_device()
    cfg = TrainConfig(epochs=args.epochs, batch_size=args.batch, parallel=args.parallel, seed=args.seed,
                      k_folds=args.folds, num_workers=args.num_workers)
    print(f"[trinetra] GPUs visible={n_gpus()} | DataParallel={cfg.use_dp()} | "
          f"effective_batch={cfg.effective_batch()} lr={cfg.effective_lr():.2e}")
    ds = ImageFolderNPZ(args.data)
    if args.model == "eo":
        EO_KW.update(in_chans=int(ds.X.shape[1]), backbone=args.eo_backbone, pretrained=bool(args.eo_pretrained),
                     freeze=bool(args.eo_freeze))
    oof_prob = np.full(len(ds), np.nan); oof_block = np.array(ds.block)
    fold_of_row = np.full(len(ds), -1)
    test = ImageFolderNPZ(args.test) if args.test else None
    test_probs = []
    stress = {Path(f).stem: ImageFolderNPZ(f) for f in args.stress}
    stress_probs = {k: [] for k in stress}
    tag = f"{args.model}_s{args.seed}"

    for fold, (tr, va) in enumerate(spatial_cv_indices(ds, cfg.k_folds, cfg.seed)):
        model, step, prob = build(args.model)
        tl = make_loader(ds, cfg, shuffle=True, indices=tr)
        print(f"[fold] {tag} fold {fold + 1}/{cfg.k_folds}: train n={len(tr)} val n={len(va)}", flush=True)
        train_one_fold(model, step, tl, cfg, device, tag=f"{tag} fold {fold + 1}/{cfg.k_folds}")
        model.eval().to(device)
        va = np.asarray(va)
        oof_prob[va] = predict(model, prob, ds.X, va, device)
        fold_of_row[va] = fold
        if test is not None:
            test_probs.append(predict(model, prob, test.X, np.arange(len(test)), device))
        for k, sd in stress.items():
            stress_probs[k].append(predict(model, prob, sd.X, np.arange(len(sd)), device))
        torch.save(model.state_dict(), os.path.join(args.out, f"{tag}_fold{fold}.pt"))

    y = _labels(ds.y)
    if y is not None:
        meta = save_oof(os.path.join(args.out, f"{tag}_oof.npz"), name=args.model, seed=args.seed,
                        folds=cfg.k_folds, prob=oof_prob, y=y, block=oof_block, fold_of_row=fold_of_row,
                        test_prob=np.mean(test_probs, 0) if test_probs else None,
                        test_y=_labels(test.y) if test is not None else None,
                        test_block=test.block if test is not None else None,
                        extra_meta={"data": args.data, "target": TARGET, "epochs": args.epochs})
        X = oof_prob.reshape(-1, 1)                 # 1-feature baseline over the model's own score
        report = admit_model(args.model, AdmissionInputs(
            y_true=y, p_model=oof_prob, block_ids=oof_block, X_baseline=X))
        oof = np.load(os.path.join(args.out, f"{tag}_oof.npz"))
        m = ~np.isnan(oof["prob_cal"])
        report["ece_crossfit_calibrated"] = expected_calibration_error(oof["prob_cal"][m], y[m])
        report["value_score_calibrated"] = value_score(y[m], oof["prob_cal"][m], 5.0, 100.0)["value_score"]
        if test is not None and len(oof["test_y"]):
            report["test_ece_calibrated"] = expected_calibration_error(oof["test_prob_cal"], oof["test_y"].astype(int))
            report["test_n"] = int(len(oof["test_y"]))
        report.update(meta["metrics"])
        if stress:
            T_all = fit_temperature(oof_prob, y)
            report["stress"] = {k: stress_summary(np.mean(v, 0), _labels(stress[k].y), T_all) for k, v in stress_probs.items()}
        report["run_id"] = meta["run_id"]; report["seed"] = args.seed
        with open(os.path.join(args.out, f"{tag}_report.json"), "w") as f:
            json.dump(report, f, indent=2)
        print(json.dumps(report, indent=2))
    else:
        print("No labels -> admission gate skipped (Rule 16).")


if __name__ == "__main__":
    main()
