"""eval.real_win — paired bootstrap 'real win' test (gate G2 / F-17). DESIGN eval protocol.

A model only 'really wins' over a baseline if the paired cost difference (baseline_cost - model_cost)
is positive with its bootstrap confidence interval LOWER bound above zero. We bootstrap over SPATIAL BLOCKS
(not individual samples) to respect spatial autocorrelation, and use a BCa interval (bias- & skew-corrected)
so the verdict is not fooled by a skewed bootstrap distribution. No p-hacking: the verdict is CI-based.
"""
from __future__ import annotations

import numpy as np

from .value_score import alarms_from_prob
from ._stats import bca_interval


def _per_sample_cost(y, a, C_FA, C_miss):
    y = np.asarray(y, int); a = np.asarray(a, int)
    return np.where((a == 1) & (y == 0), C_FA,
                    np.where((a == 0) & (y == 1), C_miss, 0.0)).astype(float)


def real_win(y_true, p_model, p_baseline, block_ids, C_FA: float, C_miss: float,
             n_boot: int = 2000, alpha: float = 0.05, seed: int = 0,
             ci_method: str = "bca") -> dict:
    """Return verdict dict. 'real_win' True iff CI lower bound of (baseline-model) cost diff > 0.

    ci_method: 'bca' (default, bias/skew-corrected) or 'percentile'."""
    y = np.asarray(y_true, int); blocks = np.asarray(block_ids)
    a_m = alarms_from_prob(p_model, C_FA, C_miss)
    a_b = alarms_from_prob(p_baseline, C_FA, C_miss)
    c_m = _per_sample_cost(y, a_m, C_FA, C_miss)
    c_b = _per_sample_cost(y, a_b, C_FA, C_miss)
    diff = c_b - c_m                                   # positive => model cheaper (better)

    uniq = np.array(sorted(set(blocks.tolist())))
    rng = np.random.default_rng(seed)
    idx_by_block = {b: np.where(blocks == b)[0] for b in uniq}
    block_means = np.array([diff[idx_by_block[b]].mean() for b in uniq])   # statistic per block

    boot = np.empty(n_boot)
    for i in range(n_boot):
        pick = rng.choice(len(uniq), size=len(uniq), replace=True)         # block bootstrap
        boot[i] = block_means[pick].mean()

    theta_hat = float(block_means.mean())
    if ci_method == "bca":
        # jackknife over blocks (leave-one-block-out means) for the acceleration term
        jk = np.array([np.delete(block_means, k).mean() for k in range(len(uniq))])
        lo, hi = bca_interval(boot, theta_hat, jk, alpha)
    else:
        lo, hi = np.quantile(boot, [alpha / 2, 1 - alpha / 2])
    return {
        "mean_cost_saving_per_sample": float(diff.mean()),
        "ci_low": float(lo), "ci_high": float(hi), "ci_level": 1 - alpha,
        "ci_method": ci_method, "n_blocks": int(len(uniq)),
        "real_win": bool(lo > 0.0),     # honest: must clear zero at the lower CI bound
    }
