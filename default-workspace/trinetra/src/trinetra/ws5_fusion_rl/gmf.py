"""ws5_fusion_rl.gmf — Gated Mixture Fusion with a bounded residual head (Class B, M6 centerpiece).

DESIGN/ws5_fusion/. GMF = (1) a GATE that turns per-expert effective weights into a normalized mixture,
(2) a base mixture mean, (3) a BOUNDED residual correction over that base. The residual is the only place
a learned head could nudge the output, and it is HARD-CLIPPED to +/- `residual_cap` so a mis-trained head
can never dominate physics (safety). Without a trained head the residual defaults to 0 => GMF reduces to
the precision-weighted mean (graceful, honest). PHARAOH may supply the base instead of the arithmetic mean
when enabled, but the bound still applies.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..common.types import ExpertOutput
from .nf import effective_weight, weighted_dispersion, nf4_salience
from .pharaoh import pharaoh_mean, pharaoh_order


@dataclass
class GMFResult:
    p: float
    base: float
    residual: float
    gate: list          # normalized mixture weights (per available expert)


def gated_weights(experts: list[ExpertOutput], tau: float = 0.5):
    """Mixture gate: normalized effective weights w~_i / sum w~_j."""
    w = np.array([effective_weight(e, tau) for e in experts], float)
    s = w.sum()
    return (w / s) if s > 0 else np.full(len(w), 1.0 / max(len(w), 1))


def bounded_residual(base: float, experts, residual_cap: float = 0.1, head=None) -> float:
    """Residual correction, hard-clipped to +/- residual_cap. `head(features)->raw` is an optional learned
    function; without it the residual is 0 (no silent adjustment)."""
    if head is None:
        return 0.0
    ps = [e.p for e in experts]
    w = gated_weights(experts)
    feats = {"dispersion": weighted_dispersion(ps, w), "salience": nf4_salience(experts), "base": base}
    raw = float(head(feats))
    return float(np.clip(raw, -residual_cap, residual_cap))


def gmf_fuse(experts: list[ExpertOutput], tau: float = 0.5, residual_cap: float = 0.1,
             use_pharaoh_base: bool = False, head=None) -> GMFResult:
    avail = [e for e in experts if e.available]
    if not avail:
        return GMFResult(p=0.0, base=0.0, residual=0.0, gate=[])
    gate = gated_weights(avail, tau)
    ps = np.array([e.p for e in avail], float)
    if use_pharaoh_base:
        rho = pharaoh_order(ps, gate, nf4_salience(avail))
        base = pharaoh_mean(ps, gate, rho)
    else:
        base = float((gate * ps).sum())
    res = bounded_residual(base, avail, residual_cap, head)
    return GMFResult(p=float(np.clip(base + res, 0.0, 1.0)), base=base, residual=res, gate=gate.tolist())


def load_numpy_head(path_or_dict):
    """Load a GMF residual head exported by kaggle/train_fusion_head.py into a PURE-NUMPY closure.

    Lets the offline gateway (no torch) run `gmf_fuse(..., head=load_numpy_head('gmf_head_numpy.json'))`.
    Accepts a path to the JSON or an already-parsed dict.
    """
    import json

    d = path_or_dict
    if isinstance(path_or_dict, str):
        with open(path_or_dict) as f:
            d = json.load(f)
    W1 = np.asarray(d["W1"], float); b1 = np.asarray(d["b1"], float)
    W2 = np.asarray(d["W2"], float); b2 = np.asarray(d["b2"], float)
    cap = float(d.get("cap", 0.1))

    def closure(feats: dict) -> float:
        x = np.array([feats["base"], feats["dispersion"], feats["salience"]], float)
        h = np.tanh(W1 @ x + b1)
        return float(np.tanh(W2 @ h + b2)[0]) * cap

    return closure
