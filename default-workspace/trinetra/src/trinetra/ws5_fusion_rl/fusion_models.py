"""ws5_fusion_rl.fusion_models — FM-1 (default/fallback) + the fusion dispatcher.

FM-1 precision/reliability-weighted linear mean (Class B) is the DEFAULT and the FALLBACK whenever a
Class-C operator (PHARAOH) is disabled or unavailable (Rule 20). The dispatcher reads configs/fusion and
reports whether a Class-C path was used. FM-2..FM-6 are registered as names with FM-1 fallback stubs until
each is validated (honest: not implemented beyond interface here).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..common.config import Config
from ..common.types import ExpertOutput, PhysicsClass
from .nf import effective_weight, nf3_conflict_to_uncertainty, nf4_salience
from .pharaoh import pharaoh_fuse


@dataclass
class FusionResult:
    p: float                 # fused risk in [0,1]
    u_star: float            # NF-3 conflict-aware uncertainty
    salience: float          # NF-4
    model: str
    used_classC: bool
    diagnostics: dict = field(default_factory=dict)


def fm1_precision_weighted(experts: list[ExpertOutput], tau: float = 0.5) -> float:
    """Class B. Weighted arithmetic mean with effective weights w~_i."""
    avail = [e for e in experts if e.available]
    if not avail:
        return 0.0
    w = np.array([effective_weight(e, tau) for e in avail], float)
    p = np.array([e.p for e in avail], float)
    s = w.sum()
    if s <= 0:
        return float(p.mean())
    return float((w / s * p).sum())


def fuse(experts: list[ExpertOutput], cfg: Config | None = None) -> FusionResult:
    cfg = cfg or Config()
    tau = cfg.get("fusion.tau", 0.5)
    lam = cfg.get("fusion.lambda", 0.3)
    model = cfg.get("fusion.model", "FM-1")
    pharaoh_on = bool(cfg.get("fusion.operator.pharaoh", False))

    avail = [e for e in experts if e.available]
    ps = [e.p for e in avail]
    ws = [effective_weight(e, tau) for e in avail]
    u = [e.u for e in avail]
    used_classC = any(e.cls == PhysicsClass.C for e in avail)
    diag = {}

    if pharaoh_on and len(avail) >= 2 and model != "GMF":
        r = pharaoh_fuse(avail)
        p = r["p"]; diag["pharaoh"] = {k: r[k] for k in ("rho", "salience")}
        used_classC = True
        model = "PHARAOH"
    elif model == "GMF":
        from .gmf import gmf_fuse
        g = gmf_fuse(avail, tau, use_pharaoh_base=pharaoh_on)
        p = g.p; diag["gmf"] = {"base": g.base, "residual": g.residual}
        used_classC = used_classC or pharaoh_on
        model = "GMF"
    else:
        p = fm1_precision_weighted(avail, tau)
        model = "FM-1"

    u_star = nf3_conflict_to_uncertainty(ps, u, ws, lam) if avail else 1.0
    S = nf4_salience(avail)
    return FusionResult(p=float(np.clip(p, 0, 1)), u_star=u_star, salience=S,
                        model=model, used_classC=used_classC, diagnostics=diag)
