"""trinetra.deep.oof_utils — out-of-fold (OOF) artifacts + leakage-safe calibration (numpy only).

Added 2026-10-31 (hackathon v2, see docs/CODE_CHANGE_LOG.md). Every trainer writes `<name>_oof.npz` with the
SAME schema so fusion (kaggle/build_fusion_cache.py) and RL logs can be built from it:

    prob (N,)  raw OOF probability          prob_cal (N,) cross-fitted temperature-calibrated probability
    y    (N,)  label                         block (N,)    group key
    [test_prob, test_prob_cal, test_y, test_block]  fold-ensemble predictions on an untouched test set
    meta  json string (name, seed, folds, run_id, T per fold)

Calibration is CROSS-FITTED: the temperature applied to group-fold k is fitted only on the OOF rows of the
other folds, so calibration never sees the rows it is applied to (no optimistic ECE).
"""
from __future__ import annotations

import json
import os
import time

import numpy as np

_EPS = 1e-6


def logit(p):
    p = np.clip(np.asarray(p, float), _EPS, 1 - _EPS)
    return np.log(p / (1 - p))


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.asarray(z, float)))


def fit_temperature(prob, y) -> float:
    """1-D temperature T minimizing binary NLL of sigmoid(logit(p)/T). Grid + golden refinement (robust, no torch)."""
    z, y = logit(prob), np.asarray(y, float)
    m = ~np.isnan(z)
    z, y = z[m], y[m]
    if len(z) < 10 or y.min() == y.max():
        return 1.0

    def nll(T):
        q = np.clip(sigmoid(z / T), _EPS, 1 - _EPS)
        return float(-(y * np.log(q) + (1 - y) * np.log(1 - q)).mean())

    grid = np.exp(np.linspace(np.log(0.05), np.log(20), 60))
    T0 = grid[int(np.argmin([nll(t) for t in grid]))]
    lo, hi = T0 / 1.15, T0 * 1.15
    g = (np.sqrt(5) - 1) / 2
    for _ in range(40):
        a, b = hi - g * (hi - lo), lo + g * (hi - lo)
        if nll(a) < nll(b):
            hi = b
        else:
            lo = a
    return float((lo + hi) / 2)


def crossfit_calibrate(prob, y, fold_of_row):
    """Return (prob_cal, temps): rows of fold k use T fitted on all other folds' rows."""
    prob = np.asarray(prob, float)
    out = np.full_like(prob, np.nan)
    temps = {}
    for k in np.unique(fold_of_row):
        if k < 0:
            continue
        tr = (fold_of_row != k) & (fold_of_row >= 0) & ~np.isnan(prob)
        T = fit_temperature(prob[tr], np.asarray(y)[tr])
        temps[int(k)] = T
        te = fold_of_row == k
        out[te] = sigmoid(logit(prob[te]) / T)
    return out, temps


def discrimination(prob, y) -> dict:
    """Threshold-free metrics (numpy): ROC-AUC (rank form), PR-AUC (average precision), recall at FPR<=5% and <=1%.
    Needed because the cost-loss value score is ~0 on BALANCED curated sets when p* = 0.048 (see docs/14)."""
    p = np.asarray(prob, float); y = np.asarray(y, int)
    m = ~np.isnan(p); p, y = p[m], y[m]
    pos, neg = (y == 1).sum(), (y == 0).sum()
    if pos == 0 or neg == 0:
        return {}
    order = np.argsort(p, kind="mergesort"); ranks = np.empty(len(p)); ranks[order] = np.arange(1, len(p) + 1)
    for v in np.unique(p):                       # average ranks for ties
        t = p == v
        ranks[t] = ranks[t].mean()
    auc = (ranks[y == 1].sum() - pos * (pos + 1) / 2) / (pos * neg)
    o = np.argsort(-p, kind="mergesort"); ys = y[o]
    tp = np.cumsum(ys); fp = np.cumsum(1 - ys)
    ap = float((tp[ys == 1] / (np.arange(1, len(ys) + 1)[ys == 1])).sum() / pos)
    out = {"roc_auc": float(auc), "pr_auc": ap, "n": int(len(y)), "pos_rate": float(pos / len(y))}
    for f in (0.05, 0.01):
        thr_ok = fp / neg <= f
        out[f"recall_at_fpr{int(f * 100):02d}"] = float((tp[thr_ok] / pos).max()) if thr_ok.any() else 0.0
    return out


def stress_summary(prob, y, T: float = 1.0, p_star: float = 5.0 / 105.0) -> dict:
    """False-alarm behaviour on a confuser/negative set (fog, sandstorm, candles, normal scenes).
    Rows with y=1 (if any) give recall; rows with y=0 give false-alarm rates at 0.5 and at p*."""
    prob = np.asarray(prob, float); pc = sigmoid(logit(prob) / T)
    y = np.zeros(len(prob), int) if y is None else np.asarray(y, int)
    neg, pos = y == 0, y == 1
    out = {"n": int(len(prob)), "n_neg": int(neg.sum()), "n_pos": int(pos.sum()), "temperature": float(T)}
    if neg.any():
        out.update(mean_prob_neg_cal=float(pc[neg].mean()), fa_rate_at_0p5_cal=float((pc[neg] >= 0.5).mean()),
                   fa_rate_at_pstar_cal=float((pc[neg] >= p_star).mean()), fa_rate_at_0p5_raw=float((prob[neg] >= 0.5).mean()))
    if pos.any():
        out.update(recall_at_0p5_cal=float((pc[pos] >= 0.5).mean()))
    return out


def run_id(module: str, seed: int) -> str:
    return f"{module}-{time.strftime('%Y%m%d-%H%M')}-{seed}"


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def save_oof(path: str, *, name: str, seed: int, folds: int, prob, y, block, fold_of_row,
             test_prob=None, test_y=None, test_block=None, extra_meta: dict | None = None) -> dict:
    """Write the standard OOF artifact (see module docstring). Returns the meta dict."""
    y = np.asarray(y, float)
    prob_cal, temps = crossfit_calibrate(prob, y, np.asarray(fold_of_row))
    meta = {"name": name, "seed": seed, "folds": folds, "run_id": run_id(name, seed), "temperatures": temps,
            **(extra_meta or {})}
    metrics = {f"oof_{k}": v for k, v in discrimination(prob, y).items()}
    if test_prob is not None and test_y is not None and len(np.asarray(test_y)):
        metrics.update({f"test_{k}": v for k, v in discrimination(test_prob, test_y).items()})
    meta["metrics"] = metrics
    arrays = dict(prob=np.asarray(prob, float), prob_cal=prob_cal, y=y, block=np.asarray(block).astype(str),
                  meta=np.asarray(json.dumps(meta)))
    if test_prob is not None:
        T_all = fit_temperature(prob, y)
        meta["temperature_all_oof"] = T_all
        arrays.update(test_prob=np.asarray(test_prob, float), test_prob_cal=sigmoid(logit(test_prob) / T_all),
                      test_y=np.asarray(test_y, float) if test_y is not None else np.array([]),
                      test_block=np.asarray(test_block).astype(str) if test_block is not None else np.array([]),
                      meta=np.asarray(json.dumps(meta)))
    np.savez_compressed(path, **arrays)
    print(f"[oof] {path} run_id={meta['run_id']} n={len(y)} T={temps}")
    return meta
