"""pipeline.hindcast — hindcast-harness skeleton (M10, gate G2 headline).

Replays a historical event under the FULL protocol (spatial-CV baselines + cost-loss + real-win) and emits
an HONEST report via eval.ReportGuard. Rule 16: performance may be claimed ONLY for events that clear the
admission gate; everything else is reported as 'NOT ADMITTED'. Real event datasets are provided via DVC
pointers (data/); this skeleton wires the flow and runs on supplied arrays.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..eval import ReportGuard, real_win, value_score, LogisticNumpy, base_rate_climatology


@dataclass
class HindcastResult:
    event: str
    report: dict
    value_scores: dict


def run_hindcast(event: str, X, y, block_ids, p_model, C_FA: float = 5.0, C_miss: float = 100.0,
                 seed: int = 0) -> HindcastResult:
    """Compare a model's probabilities against baselines on spatial blocks; gate any performance claim."""
    y = np.asarray(y, int)
    guard = ReportGuard(spatial_cv=True)

    # baselines
    clim = base_rate_climatology(y, len(y))
    logit = LogisticNumpy(seed=seed).fit(X, y).predict_proba(X)
    for name, p_base in [("climatology", clim), ("logistic", logit)]:
        verdict = real_win(y, p_model, p_base, block_ids, C_FA, C_miss, n_boot=500, seed=seed)
        guard.add_baseline_verdict(name, verdict)

    vs = {
        "model": value_score(y, p_model, C_FA, C_miss)["value_score"],
        "climatology": value_score(y, clim, C_FA, C_miss)["value_score"],
        "logistic": value_score(y, logit, C_FA, C_miss)["value_score"],
    }
    return HindcastResult(event=event, report=guard.summary(), value_scores=vs)
