"""ws5_fusion_rl.pharaoh — PHARAOH adaptive-order weighted power mean (Class C, UNVALIDATED).

DESIGN/ws5_fusion/novel_aggregation_operator_P22.md.  F_rho(p;w) = ( sum w_i p_i^rho )^(1/rho),  sum w_i=1.
Adaptive order  rho(t) = 1 + kappa * D * S  (D=disagreement, S=credible-alarm salience) so the mean bends
toward 'max' (anti-complacency) ONLY when a reliable, physics-consistent alarm is credible.

SAFETY COROLLARY (property to validate, tested numerically): for rho >= 1, F_rho >= arithmetic mean, so
PHARAOH never under-states relative to a plain average. DEFAULT-OFF (configs/fusion operator.pharaoh);
fallback is FM-1 arithmetic/precision mean. Not claimed to work or beat anything (Rule 21).
"""
from __future__ import annotations

import numpy as np

from .nf import weighted_dispersion, nf4_salience


def pharaoh_order(ps, weights, salience: float, kappa: float = 2.0) -> float:
    """rho(t) = 1 + kappa * D * S, clamped to [1, 8] for numerical sanity."""
    D = weighted_dispersion(ps, weights)
    rho = 1.0 + kappa * D * float(salience)
    return float(np.clip(rho, 1.0, 8.0))


def pharaoh_mean(ps, weights, rho: float) -> float:
    """Weighted power mean of order rho. Weights are normalized internally; p in [0,1]."""
    ps = np.asarray(ps, float); w = np.asarray(weights, float)
    s = w.sum()
    if s <= 0:
        return 0.0
    w = w / s
    rho = max(float(rho), 1e-9)
    val = float((w * np.power(np.clip(ps, 0.0, 1.0), rho)).sum()) ** (1.0 / rho)
    return float(np.clip(val, 0.0, 1.0))


def pharaoh_fuse(experts, kappa: float = 2.0) -> dict:
    """Full PHARAOH fuse over a list of ExpertOutput using effective weights. Returns value + diagnostics."""
    from .nf import effective_weight
    avail = [e for e in experts if e.available]
    if not avail:
        return {"p": 0.0, "rho": 1.0, "salience": 0.0, "note": "no available experts"}
    ps = [e.p for e in avail]
    w = [effective_weight(e) for e in avail]
    S = nf4_salience(avail)
    rho = pharaoh_order(ps, w, S, kappa)
    p = pharaoh_mean(ps, w, rho)
    return {"p": p, "rho": rho, "salience": S, "weights": w, "ps": ps}
