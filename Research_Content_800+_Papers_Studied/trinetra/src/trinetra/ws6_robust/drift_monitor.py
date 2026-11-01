"""ws6_robust.drift_monitor — distribution-shift + concept-drift detection (gate G3/M4).

If the input distribution drifts (PSI high) or a sequential change is detected (CUSUM), the conformal
coverage bound is no longer trustworthy; callers must flag reliability='Unreliable' and the decision layer
fails toward 'uncertain' (Rule 19). Pure numpy.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def population_stability_index(reference, current, bins: int = 10, eps: float = 1e-6) -> float:
    """PSI between a reference and current sample. Rule of thumb: >0.1 moderate, >0.2 significant shift."""
    ref = np.asarray(reference, float); cur = np.asarray(current, float)
    edges = np.quantile(ref, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    r = np.histogram(ref, edges)[0] / max(len(ref), 1) + eps
    c = np.histogram(cur, edges)[0] / max(len(cur), 1) + eps
    return float(np.sum((c - r) * np.log(c / r)))


@dataclass
class CusumState:
    g_pos: float = 0.0
    g_neg: float = 0.0


def cusum_update(state: CusumState, x: float, target: float, k: float = 0.5, h: float = 5.0):
    """One CUSUM step. Returns (state, drift_flag). k=slack, h=decision threshold."""
    s = CusumState(
        g_pos=max(0.0, state.g_pos + (x - target) - k),
        g_neg=min(0.0, state.g_neg + (x - target) + k),
    )
    return s, bool(s.g_pos > h or s.g_neg < -h)


@dataclass
class DriftReport:
    psi: float
    psi_drift: bool
    note: str


def check_drift(reference, current, psi_threshold: float = 0.2) -> DriftReport:
    psi = population_stability_index(reference, current)
    drift = psi > psi_threshold
    return DriftReport(psi=psi, psi_drift=drift,
                       note=("DRIFT: conformal coverage void -> reliability=Unreliable" if drift
                             else "stable"))
