"""ws5_fusion_rl.nf — NF-1..NF-4 fusion sub-formulas (DESIGN/ws5_fusion/novel_formulas_P22.md).

NF-1 physics-consistency c_i, NF-2 drift-decayed reliability r_i(t), NF-3 conflict->uncertainty,
NF-4 credible-alarm salience S. NF-1/NF-4 are the Class-C-adjacent pieces used as SOFT weights; they only
re-weight experts, never fabricate a probability. All bounded to [0,1] (except U* which is [0,1] too).
"""
from __future__ import annotations

import math

import numpy as np

from ..common.types import ExpertOutput


def nf1_consistency(p_i: float, phi_physics: float, sigma: float = 0.25, eps: float = 1e-6) -> float:
    """c_i = exp( -((p_i - phi)_+)^2 / (2(sigma^2+eps)) ). Penalizes claiming MORE alarm than physics
    supports; agreeing-or-below physics is fully consistent."""
    over = max(p_i - phi_physics, 0.0)
    return float(math.exp(-(over ** 2) / (2.0 * (sigma ** 2 + eps))))


def nf2_reliability(r_prev: float, outcome_ok: bool, drift_flag: bool = False,
                    lam: float = 0.9, r_min: float = 0.1, drift_penalty: float = 0.5) -> float:
    """Exponential-forgetting reliability update. Good outcome nudges up, bad nudges down; a drift flag
    multiplies down. Clamped to [r_min, 1]."""
    target = 1.0 if outcome_ok else 0.0
    r = lam * r_prev + (1.0 - lam) * target
    if drift_flag:
        r *= drift_penalty
    return float(np.clip(r, r_min, 1.0))


def weighted_dispersion(ps, weights) -> float:
    """D = sqrt( sum w_i (p_i - pbar)^2 ), weights normalized. In [0, 0.5]-ish for p in [0,1]."""
    ps = np.asarray(ps, float); w = np.asarray(weights, float)
    s = w.sum()
    if s <= 0:
        return 0.0
    w = w / s
    pbar = float((w * ps).sum())
    return float(math.sqrt(max((w * (ps - pbar) ** 2).sum(), 0.0)))


def nf3_conflict_to_uncertainty(ps, u, weights, lam: float = 0.3) -> float:
    """U* = sum w_i u_i + lam * D(p). More disagreement => more uncertainty (fail toward 'uncertain')."""
    u = np.asarray(u, float); w = np.asarray(weights, float)
    s = w.sum() or 1.0
    wn = w / s
    base = float((wn * u).sum())
    D = weighted_dispersion(ps, weights)
    return float(np.clip(base + lam * D, 0.0, 1.0))


def _psi(p: float) -> float:
    """Increasing alarm-salience shaping in [0,1]."""
    return float(p)


def nf4_salience(experts: list[ExpertOutput]) -> float:
    """S = max_i [ r_i * c_i * psi(p_i) ] over AVAILABLE experts — is any trustworthy alarm credible?"""
    vals = [e.r * e.c * _psi(e.p) for e in experts if e.available]
    return float(max(vals)) if vals else 0.0


def effective_weight(e: ExpertOutput, tau: float = 0.5) -> float:
    """w~_i = availability * reliability r_i * consistency c_i * exp(-u_i / tau)  (COMPONENT_DESIGN §8.1)."""
    if not e.available:
        return 0.0
    return float(e.r * e.c * math.exp(-e.u / max(tau, 1e-6)))
