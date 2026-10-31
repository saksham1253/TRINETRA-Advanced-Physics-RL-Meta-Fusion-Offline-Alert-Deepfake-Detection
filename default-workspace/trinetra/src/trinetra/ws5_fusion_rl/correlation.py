"""ws5_fusion_rl.correlation — correlation-aware (BLUE/GLS) weighting for within-group fusion.

Problem: inside one workstream, several sensors/models are REDUNDANT (e.g. two soil probes on the same
slope). Plain weighting counts them as independent votes -> a correlated cluster swamps a genuinely
independent source (double-counting). Fix: treat the experts as correlated estimators and use the
minimum-variance linear combination (Aitken/GLS, a.k.a. BLUE):  w* ∝ Σ⁻¹ 1, where Σ encodes each expert's
variance (from its effective weight) and the pairwise correlation R.

Property (proved in tests): as the correlation ρ between a redundant pair → 1, their COMBINED weight → that
of a single independent expert of equal quality (the cluster stops over-counting).

SAFETY OVERRIDE (honesty > statistical optimality): pure BLUE can assign NEGATIVE 'hedging' weights, which
could pull the fused alarm BELOW every input — unacceptable for a life-safety monotone fusion (Rule 19). So
we clip weights to be non-negative and renormalize. We document this as a deliberate, conservative deviation
from the unconstrained optimum.
"""
from __future__ import annotations

import numpy as np

from ..common.types import ExpertOutput
from .nf import effective_weight


def redundancy_matrix(sources: list[str], redundant_groups: list[set[str]] | None,
                      rho: float = 0.8) -> np.ndarray:
    """Build a correlation matrix R: experts sharing a redundancy group get correlation `rho`, else 0.

    Diagonal is 1. `redundant_groups` is a list of source-name sets known to co-move (same slope, same
    camera cluster, etc.). With None/empty, R = I (treat all as independent)."""
    n = len(sources)
    R = np.eye(n)
    if not redundant_groups:
        return R
    idx = {s: i for i, s in enumerate(sources)}
    for grp in redundant_groups:
        members = [idx[s] for s in grp if s in idx]
        for a in members:
            for b in members:
                if a != b:
                    R[a, b] = rho
    return R


def correlation_adjusted_weights(experts: list[ExpertOutput], corr: np.ndarray | None = None,
                                 tau: float = 0.5, ridge: float = 1e-3) -> np.ndarray:
    """Non-negative minimum-variance (GLS/BLUE) weights over AVAILABLE experts, correlation-aware.

    Variance_i ∝ 1 / effective_weight_i (a more trustworthy expert has lower variance). Returns weights
    that sum to 1 over the available experts (zeros for unavailable). Falls back to normalized effective
    weights if Σ is ill-conditioned."""
    avail_mask = np.array([e.available for e in experts], bool)
    out = np.zeros(len(experts), float)
    avail = [e for e in experts if e.available]
    if not avail:
        return out

    w_eff = np.array([max(effective_weight(e, tau), 1e-9) for e in avail], float)
    var = 1.0 / w_eff
    sd = np.sqrt(var)

    R = np.eye(len(avail)) if corr is None else np.asarray(corr, float)
    if R.shape != (len(avail), len(avail)):
        R = np.eye(len(avail))                        # shape guard -> independence
    Sigma = np.outer(sd, sd) * R + ridge * np.eye(len(avail))

    try:
        raw = np.linalg.solve(Sigma, np.ones(len(avail)))
    except np.linalg.LinAlgError:
        raw = w_eff.copy()                            # fallback: plain precision weights

    raw = np.clip(raw, 0.0, None)                     # SAFETY: no negative/hedging weights (Rule 19)
    s = raw.sum()
    raw = raw / s if s > 0 else w_eff / w_eff.sum()
    out[avail_mask] = raw
    return out


def blue_fuse(experts: list[ExpertOutput], corr: np.ndarray | None = None, tau: float = 0.5) -> float:
    """Correlation-aware fused probability = sum of BLUE weights * expert probabilities."""
    w = correlation_adjusted_weights(experts, corr, tau)
    p = np.array([e.p for e in experts], float)
    s = w.sum()
    return float((w * p).sum() / s) if s > 0 else 0.0
