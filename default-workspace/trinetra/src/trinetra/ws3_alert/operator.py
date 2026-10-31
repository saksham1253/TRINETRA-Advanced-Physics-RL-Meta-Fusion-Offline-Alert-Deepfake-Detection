"""ws3_alert.operator — operator decision-support + human approval gate (M8, Rule 19).

The system is ADVISORY: it presents a decision to a human and can only proceed to a public CAP alert after
the operator explicitly approves, producing an approval token that `build_cap` requires. Local sirens for
imminent physical danger are handled by the offline path/shield, but PUBLIC messaging is always human-gated.
"""
from __future__ import annotations

from ..common.types import Decision, Level


def present(decision: Decision) -> str:
    """Render a concise, honest operator briefing (never auto-sends anything)."""
    c = decision.conformal
    lines = [
        f"[ADVISORY] zone={decision.zone_id} hazard={decision.hazard.value} "
        f"level={decision.level.name} risk={decision.risk:.3f}",
        f"  conformal set={c.pred_set} target={c.coverage_target:.2f} reliability={c.reliability.value}",
        f"  shield: raised={decision.shield.raised} floor={decision.shield.floor.name} "
        f"reason={decision.shield.reason}",
        f"  uncertain={decision.uncertain}  used_classC={decision.used_classC}  "
        f"fusion={decision.model_versions.get('fusion')}",
        "  contributions:",
    ]
    for e in decision.contributions:
        lines.append(f"    - {e.source}: p={e.p:.2f} u={e.u:.2f} c={e.c:.2f} r={e.r:.2f} "
                     f"cls={e.cls.value} avail={e.available}")
    lines.append("  --> ACTION REQUIRED: human operator must review and approve before any public alert.")
    return "\n".join(lines)


def approve(decision: Decision, operator_id: str, acknowledge_advisory: bool = True) -> str:
    """Produce an approval token for a decision. The human must acknowledge it is advisory.

    Returns a token string 'APPROVED:<operator_id>'. Callers pass this to build_cap.
    """
    if not acknowledge_advisory:
        raise ValueError("operator must acknowledge the advisory nature before approving")
    if decision.level == Level.GREEN:
        raise ValueError("nothing to approve: level is GREEN (no public alert)")
    return f"APPROVED:{operator_id}"
