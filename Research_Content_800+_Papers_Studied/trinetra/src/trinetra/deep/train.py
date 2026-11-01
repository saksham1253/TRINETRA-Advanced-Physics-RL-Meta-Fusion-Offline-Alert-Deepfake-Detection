"""trinetra.deep.train — unified trainer: seeds, MULTI-GPU, spatial-CV, AMP, calibration, eval admission.

Tuned for Kaggle **T4 x2**: by default it uses both GPUs via `nn.DataParallel`, scales the batch size and
(linearly) the LR by the GPU count, enables cuDNN autotuning + fp16 AMP, and uses pinned, persistent-worker
DataLoaders. For maximum throughput a DistributedDataParallel launcher is provided in `trinetra.deep.ddp`.

The trainer is model-agnostic: pass a model, a `step_fn(model, batch)->{'loss',...}`, and a dataset exposing
a `.block` array; it runs spatial-block CV (shared with eval.spatial_block_kfold), trains each fold,
temperature-calibrates validation logits, and runs the eval admission gate. NO performance number is
reported unless the gate admits the model (Rule 16). Deep probabilities only ever become fusion experts.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset

from ..eval import spatial_block_kfold, value_score, real_win, ReportGuard, LogisticNumpy, base_rate_climatology
from ..eval import expected_calibration_error, maximum_calibration_error, brier_decomposition


def set_seed(seed: int = 0):
    random.seed(seed); np.random.seed(seed)
    torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)


def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def n_gpus() -> int:
    return torch.cuda.device_count() if torch.cuda.is_available() else 0


def setup_perf():
    """cuDNN autotuning + TF32/fp16-friendly matmul. Call once at the start of a training script."""
    if torch.cuda.is_available():
        torch.backends.cudnn.benchmark = True
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        try:
            torch.set_float32_matmul_precision("high")
        except Exception:
            pass


@dataclass
class TrainConfig:
    epochs: int = 20
    batch_size: int = 64             # PER-GPU base; effective batch = batch_size * n_gpus when scaling
    lr: float = 3e-4
    weight_decay: float = 1e-4
    grad_clip: float = 1.0
    amp: bool = True
    seed: int = 0
    k_folds: int = 5
    num_workers: int = 4
    parallel: str = "auto"           # "auto"|"dp"|"none" (DDP via trinetra.deep.ddp)
    scale_batch_by_gpus: bool = True
    scale_lr_by_gpus: bool = True    # linear LR scaling rule (Goyal et al. 2017)
    pin_memory: bool = True

    def use_dp(self) -> bool:
        return self.parallel in ("auto", "dp") and n_gpus() > 1

    def effective_batch(self) -> int:
        return self.batch_size * (max(n_gpus(), 1) if self.scale_batch_by_gpus else 1)

    def effective_lr(self) -> float:
        return self.lr * (max(n_gpus(), 1) if self.scale_lr_by_gpus else 1.0)


def make_loader(dataset, cfg: TrainConfig, shuffle: bool, indices=None) -> DataLoader:
    """DataLoader tuned for Kaggle GPUs: effective (GPU-scaled) batch, pinned memory, persistent workers.

    drop_last is enabled for shuffled (training) loaders so DataParallel splits batches evenly across GPUs,
    BUT only when there are at least two full batches — otherwise a small fold could drop its only batch and
    train on nothing. Falls back to keeping all data for tiny splits."""
    ds = Subset(dataset, indices) if indices is not None else dataset
    nw = cfg.num_workers
    eff = cfg.effective_batch()
    drop_last = shuffle and len(ds) >= 2 * eff
    return DataLoader(
        ds, batch_size=eff, shuffle=shuffle, num_workers=nw,
        pin_memory=cfg.pin_memory and torch.cuda.is_available(),
        persistent_workers=nw > 0, drop_last=drop_last,
    )


class _LossModule(nn.Module):
    """Wraps (model, step_fn) so DataParallel can parallelize the WHOLE loss computation across GPUs.

    DataParallel scatters the batch tensors along dim 0 to each GPU, runs step_fn per replica, and gathers
    the per-replica losses; the caller takes .mean(). This is the standard DP pattern and lets custom
    losses (PINN PDE residual, Deep-SVDD, cost-sensitive BCE) run multi-GPU without touching step_fn."""

    def __init__(self, model, step_fn):
        super().__init__()
        self.model = model
        self.step_fn = step_fn

    def forward(self, batch):
        return self.step_fn(self.model, batch)["loss"].reshape(1)   # (1,) so DP gather -> (n_gpus,)


class TemperatureScaler(nn.Module):
    """Single-parameter temperature calibration on logits (Guo et al.). Fit on validation logits."""

    def __init__(self):
        super().__init__()
        self.log_T = nn.Parameter(torch.zeros(1))

    def forward(self, logits):
        return logits / torch.exp(self.log_T)

    def fit(self, logits, targets, iters: int = 200):
        logits = logits.detach(); targets = targets.detach().float()
        opt = torch.optim.LBFGS([self.log_T], lr=0.1, max_iter=iters)
        bce = nn.BCEWithLogitsLoss()

        def closure():
            opt.zero_grad(); loss = bce(self.forward(logits).squeeze(-1), targets)
            loss.backward(); return loss
        opt.step(closure)
        return self


def train_one_fold(model, step_fn, train_loader, cfg: TrainConfig, device) -> None:
    """Train `model` in place. Uses both GPUs via DataParallel when available (cfg.use_dp())."""
    model.to(device).train()
    runner = _LossModule(model, step_fn).to(device)
    if cfg.use_dp():
        runner = nn.DataParallel(runner)                 # splits each batch across all visible GPUs
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],
                            lr=cfg.effective_lr(), weight_decay=cfg.weight_decay)
    use_amp = cfg.amp and device.type == "cuda"
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
    for _ in range(cfg.epochs):
        for batch in train_loader:
            batch = _to_device(batch, device)
            opt.zero_grad()
            with torch.cuda.amp.autocast(enabled=use_amp):
                loss = runner(batch).mean()              # .mean() reduces the per-GPU losses
            scaler.scale(loss).backward()
            scaler.unscale_(opt)
            torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
            scaler.step(opt); scaler.update()


def _to_device(batch, device):
    out = {}
    for k, v in batch.items():
        out[k] = v.to(device) if torch.is_tensor(v) else v
    return out


@dataclass
class AdmissionInputs:
    y_true: np.ndarray
    p_model: np.ndarray
    block_ids: np.ndarray
    X_baseline: np.ndarray            # features for the logistic baseline
    C_FA: float = 5.0
    C_miss: float = 100.0


def admit_model(name: str, a: AdmissionInputs, seed: int = 0) -> dict:
    """Run the FULL honesty gate: beat climatology + logistic on spatial blocks with CI. Returns a report.

    No caller may advertise a metric unless report['admitted'] is True (Rule 16)."""
    guard = ReportGuard(spatial_cv=True)
    clim = base_rate_climatology(a.y_true, len(a.y_true))
    logit = LogisticNumpy(seed=seed).fit(a.X_baseline, a.y_true).predict_proba(a.X_baseline)
    for bname, p_base in [("climatology", clim), ("logistic", logit)]:
        guard.add_baseline_verdict(
            bname, real_win(a.y_true, a.p_model, p_base, a.block_ids, a.C_FA, a.C_miss, seed=seed))
    report = guard.summary()
    report["value_score_model"] = value_score(a.y_true, a.p_model, a.C_FA, a.C_miss)["value_score"]
    # Calibration diagnostics (eval.calibration): reported alongside the gate so a deployment can require a
    # calibration bound, not just discrimination. These are DIAGNOSTIC — they never relax the admission gate.
    mask = ~np.isnan(a.p_model)
    if mask.any():
        report["calibration"] = {
            "ece": expected_calibration_error(a.p_model[mask], a.y_true[mask]),
            "mce": maximum_calibration_error(a.p_model[mask], a.y_true[mask]),
            **brier_decomposition(a.p_model[mask], a.y_true[mask]),
        }
    report["name"] = name
    return report


def spatial_cv_indices(dataset, k: int, seed: int):
    """Yield (train_idx, val_idx) using the dataset's .block array via eval.spatial_block_kfold."""
    blocks = np.array([dataset[i]["block"] for i in range(len(dataset))]) \
        if not hasattr(dataset, "block") else np.asarray(dataset.block)
    yield from spatial_block_kfold(blocks, k=k, seed=seed)
