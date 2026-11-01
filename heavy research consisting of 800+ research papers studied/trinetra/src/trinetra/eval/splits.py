"""eval.splits — SPATIAL cross-validation (gate G2). DESIGN/SYSTEM_DESIGN_PROMPT.md eval protocol.

Random k-fold leaks spatial autocorrelation and inflates skill. We split by SPATIAL BLOCK (whole zones /
grid blocks go to one fold), so a model is always tested on unseen terrain. Also a strictly temporal split
(train past, test future) to prevent look-ahead leakage.
"""
from __future__ import annotations

import numpy as np


def spatial_block_kfold(block_ids, k: int = 5, seed: int = 0):
    """Yield (train_idx, test_idx) where each whole block_id lands in exactly one test fold.

    block_ids: array-like of a spatial grouping key per sample (e.g., zone/catchment/grid-block id).
    """
    block_ids = np.asarray(block_ids)
    uniq = np.array(sorted(set(block_ids.tolist())))
    rng = np.random.default_rng(seed)
    rng.shuffle(uniq)
    fold_of = {b: i % k for i, b in enumerate(uniq)}
    folds = np.array([fold_of[b] for b in block_ids])
    for f in range(k):
        test = np.where(folds == f)[0]
        train = np.where(folds != f)[0]
        if len(test) and len(train):
            yield train, test


def temporal_split(times, train_frac: float = 0.7):
    """Train on the earliest train_frac of time, test on the rest (no look-ahead)."""
    times = np.asarray(times)
    order = np.argsort(times)
    cut = int(len(order) * train_frac)
    return order[:cut], order[cut:]


def assert_no_time_leak(feature_times, decision_time):
    """Raise if any feature timestamp is after the decision time (gate G6 anti-leak)."""
    from ..common.exceptions import LeakageError
    ft = np.asarray(feature_times)
    if np.any(ft > decision_time):
        raise LeakageError("feature timestamp(s) occur after decision_time (look-ahead leakage)")
