"""ws5_fusion_rl.hierarchical — two-layer (hierarchical) meta-fusion (DESIGN/ws5_fusion §hierarchical).

Layer 1 (intra-workstream): fuse the experts WITHIN each workstream/hazard group into ONE group-level
expert, propagating uncertainty (NF-3), intra-group agreement -> consistency, reliability-weighted trust,
and a conservative class label (the weakest-guarantee member dominates, so Class-C novelty is never hidden).

Layer 2 (cross-workstream meta-fusion): the group experts are fed to the SAME single decision function
`decide()` — no second decision path is introduced. This gives a clean hierarchy:
    sensors/models --FM--> workstream expert --meta-FM/decide--> advisory decision.

Why hierarchical: it stops a crowd of correlated sensors inside one workstream from swamping an independent
workstream (double-counting), and it keeps per-workstream reliability/consistency interpretable for the
operator. The math reuses the audited NF/FM primitives; nothing new is fabricated.
"""
from __future__ import annotations

from datetime import datetime

import numpy as np

from ..common.config import Config
from ..common.types import Decision, ExpertOutput, Hazard, PhysicsClass, utcnow
from .nf import effective_weight, weighted_dispersion, nf3_conflict_to_uncertainty
from .fusion_models import fuse
from .decision import decide
from .shield import ShieldSignals
from .correlation import correlation_adjusted_weights, blue_fuse, redundancy_matrix

# Conservative class precedence: the WEAKEST-guarantee / most-novel member labels the group (transparency).
_CLASS_PRECEDENCE = [PhysicsClass.C, PhysicsClass.ADVISORY, PhysicsClass.DATA, PhysicsClass.B, PhysicsClass.A]


def _group_class(experts: list[ExpertOutput], used_classC: bool) -> PhysicsClass:
    present = {e.cls for e in experts}
    if used_classC:
        return PhysicsClass.C          # a Class-C operator (PHARAOH) was used inside the group
    for c in _CLASS_PRECEDENCE:
        if c in present:
            return c
    return PhysicsClass.DATA


def fuse_group(name: str, experts: list[ExpertOutput], cfg: Config | None = None, *,
               corr=None, redundant_groups: list[set[str]] | None = None,
               rho: float = 0.8) -> ExpertOutput:
    """Fuse one workstream's experts into a single group-level ExpertOutput with propagated metadata.

    If `corr` (a correlation matrix over the AVAILABLE experts) or `redundant_groups` (source-name sets
    that co-move) is given, within-group fusion is correlation-aware (BLUE/GLS) so redundant sensors do not
    double-count. Otherwise the configured FM (FM-1/GMF/PHARAOH) is used.
    """
    cfg = cfg or Config()
    tau = cfg.get("fusion.tau", 0.5)
    lam = cfg.get("fusion.lambda", 0.3)
    avail = [e for e in experts if e.available]
    if not avail:
        return ExpertOutput(p=0.0, source=name, u=1.0, c=0.0, r=0.0,
                            cls=PhysicsClass.DATA, available=False)

    use_corr = corr is not None or redundant_groups is not None
    if use_corr:
        R = corr if corr is not None else redundancy_matrix([e.source for e in avail], redundant_groups, rho)
        w = correlation_adjusted_weights(avail, R, tau)        # length == len(avail) (all available here)
        p = blue_fuse(avail, R, tau)
        used_classC = any(e.cls == PhysicsClass.C for e in avail)
    else:
        fr = fuse(avail, cfg)
        p = fr.p
        w = np.array([effective_weight(e, tau) for e in avail], float)
        used_classC = fr.used_classC

    sw = float(np.sum(w))
    disp = weighted_dispersion([e.p for e in avail], w)        # intra-group disagreement
    u_star = nf3_conflict_to_uncertainty([e.p for e in avail], [e.u for e in avail], w, lam)
    c_group = float(np.clip(1.0 - 2.0 * disp, 0.0, 1.0))       # agreement -> consistency
    r_group = float(np.sum(w * np.array([e.r for e in avail])) / sw) if sw > 0 \
        else float(np.mean([e.r for e in avail]))
    cls_group = _group_class(avail, used_classC)

    return ExpertOutput(p=float(np.clip(p, 0, 1)), source=name,
                        u=float(np.clip(u_star, 0, 1)), c=c_group,
                        r=float(np.clip(r_group, 0, 1)), cls=cls_group, available=True)


def hierarchical_fuse(groups: dict[str, list[ExpertOutput]], cfg: Config | None = None, *,
                      redundancy: dict[str, list[set[str]]] | None = None,
                      rho: float = 0.8) -> list[ExpertOutput]:
    """Layer-1: map each {workstream_name: [experts]} to one group-level expert.

    `redundancy` optionally maps a group name -> list of redundant source-name sets, enabling
    correlation-aware within-group fusion for that group."""
    cfg = cfg or Config()
    redundancy = redundancy or {}
    return [fuse_group(name, exps, cfg, redundant_groups=redundancy.get(name), rho=rho)
            for name, exps in groups.items()]


def decide_hierarchical(groups: dict[str, list[ExpertOutput]],
                        shield: ShieldSignals | None, cfg: Config | None = None, *,
                        hazard: Hazard = Hazard.LANDSLIDE, zone_id: str = "zone",
                        t: datetime | None = None,
                        redundancy: dict[str, list[set[str]]] | None = None,
                        rho: float = 0.8) -> Decision:
    """Full hierarchy: Layer-1 group fusion (optionally correlation-aware) -> Layer-2 meta-fusion via the
    single decision function."""
    cfg = cfg or Config()
    group_experts = hierarchical_fuse(groups, cfg, redundancy=redundancy, rho=rho)
    return decide(group_experts, shield, cfg, hazard=hazard, zone_id=zone_id, t=t or utcnow())
