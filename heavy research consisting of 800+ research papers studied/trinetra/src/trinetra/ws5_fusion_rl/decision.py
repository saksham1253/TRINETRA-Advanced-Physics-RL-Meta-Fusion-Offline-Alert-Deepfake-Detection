"""ws5_fusion_rl.decision — THE single decision function (DESIGN/HLD.md §2.3, Rule 19).

    level = max( conformal_level(fused_risk, p*) ,  shield_floor )

Exactly one decision path exists. The shield can only RAISE. The result is ADVISORY and, when the
conflict-aware uncertainty U* is high, carries uncertain=True (abstain + escalate to a human) — but it is
NEVER silent. A provisional conformal set + reliability flag are produced here; a calibrated set from
ws6_robust can be substituted when a calibration set is available.
"""
from __future__ import annotations

from datetime import datetime

from ..common.config import Config
from ..common.types import (
    ConformalResult, Decision, ExpertOutput, Hazard, Level, PhysicsClass, Reliability, utcnow,
)
from .fusion_models import fuse
from .shield import ShieldSignals, shield_floor

_ORDER = [Level.GREEN, Level.YELLOW, Level.ORANGE, Level.RED]


def conformal_level(risk: float, p_star: float, thresholds=None) -> Level:
    """Map calibrated risk to an alert level.

    By default the escalation points are the cost-loss alarm point p* and its (4x, 10x) multiples. If
    `thresholds=(t_yellow, t_orange, t_red)` is supplied (e.g. from ws6_robust.conformal_risk_threshold,
    which bounds the realized miss-risk), those calibrated cut points are used instead of the ad-hoc ones."""
    if thresholds is None:
        t_y, t_o, t_r = p_star, 4.0 * p_star, 10.0 * p_star
    else:
        t_y, t_o, t_r = thresholds
    if risk < t_y:
        return Level.GREEN
    if risk < t_o:
        return Level.YELLOW
    if risk < t_r:
        return Level.ORANGE
    return Level.RED


def _reliability_from_uncertainty(u_star: float, drift: bool) -> Reliability:
    if drift:
        return Reliability.UNRELIABLE
    if u_star < 0.2:
        return Reliability.HIGH
    if u_star < 0.4:
        return Reliability.MEDIUM
    if u_star < 0.6:
        return Reliability.LOW
    return Reliability.UNRELIABLE


def _pred_set(point: Level, u_star: float) -> list[str]:
    """Contiguous set of levels around the point estimate; widens with uncertainty (provisional)."""
    i = _ORDER.index(point)
    half = 0 if u_star < 0.2 else (1 if u_star < 0.5 else 2)
    lo, hi = max(0, i - half), min(len(_ORDER) - 1, i + half)
    return [lv.name for lv in _ORDER[lo:hi + 1]]


def decide(
    experts: list[ExpertOutput],
    shield_signals: ShieldSignals | None = None,
    cfg: Config | None = None,
    *,
    hazard: Hazard = Hazard.LANDSLIDE,
    zone_id: str = "UNKNOWN",
    t: datetime | None = None,
    drift: bool = False,
    uncertain_threshold: float = 0.6,
    trace_id: str | None = None,
    level_thresholds=None,
) -> Decision:
    cfg = cfg or Config()
    t = t or utcnow()
    shield_signals = shield_signals or ShieldSignals()

    fused = fuse(experts, cfg)
    p_star = cfg.p_star

    avail = [e for e in experts if e.available]
    point = conformal_level(fused.p, p_star, level_thresholds)
    sh = shield_floor(shield_signals)
    level = Level.raise_to(point, sh.floor)

    uncertain = (not avail) or (fused.u_star > uncertain_threshold) or drift

    used_classC = fused.used_classC or any(e.cls == PhysicsClass.C for e in experts)

    conf = ConformalResult(
        pred_set=_pred_set(level, fused.u_star),
        coverage_target=1.0 - cfg.get("calib.alpha", 0.1),
        reliability=_reliability_from_uncertainty(fused.u_star, drift),
    )
    return Decision(
        zone_id=zone_id, t=t, hazard=hazard, level=level, risk=fused.p,
        conformal=conf, shield=sh, contributions=list(experts),
        uncertain=uncertain, advisory=True, used_classC=used_classC,
        model_versions={"fusion": fused.model}, trace_id=trace_id,
    )
