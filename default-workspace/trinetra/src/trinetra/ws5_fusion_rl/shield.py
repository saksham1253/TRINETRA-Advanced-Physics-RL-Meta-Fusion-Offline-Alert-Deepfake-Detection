"""ws5_fusion_rl.shield — hard deterministic safety shield (DESIGN/COMPONENT_DESIGN.md §5, Rule 19).

The shield is POST-POSED (applied after the learner/fusion) and MONOTONE: it can only RAISE the level,
never lower it. It is hard-coded (no training). A single faulty/uncorroborated node CANNOT reach RED —
spatial corroboration is required. Totality: it always returns a defined Level for any input.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..common.types import Level, ShieldResult


@dataclass
class ShieldSignals:
    FS: float | None = None                 # factor of safety (geo)
    tilt_rate_deg_per_day: float | None = None
    nodes_agree: int = 0                     # how many independent nodes corroborate
    rain_24h_mm: float | None = None
    high_susceptibility: bool = False
    glof_lake_drop: bool = False
    downstream_stage_jump: bool = False
    fire_multi_node: bool = False            # smoke+heat agreement across >=2 nodes


def shield_floor(s: ShieldSignals) -> ShieldResult:
    floor = Level.GREEN
    reasons: list[str] = []

    if s.FS is not None and s.FS < 1.0:
        floor = Level.raise_to(floor, Level.ORANGE); reasons.append(f"FS<1 (FS={s.FS:.2f})")

    if (s.tilt_rate_deg_per_day is not None and s.tilt_rate_deg_per_day > 5.0 and s.nodes_agree >= 2):
        floor = Level.raise_to(floor, Level.RED)
        reasons.append(f"tilt_rate>5deg/day corroborated by {s.nodes_agree} nodes")

    if s.rain_24h_mm is not None and s.rain_24h_mm > 150.0 and s.high_susceptibility:
        floor = Level.raise_to(floor, Level.ORANGE)
        reasons.append(f"24h rain>{150}mm on high-susceptibility slope")

    if s.glof_lake_drop and s.downstream_stage_jump:
        floor = Level.raise_to(floor, Level.RED)
        reasons.append("GLOF lake-level drop + downstream stage jump")

    if s.fire_multi_node:
        floor = Level.raise_to(floor, Level.ORANGE)
        reasons.append("fire corroborated by multiple nodes (smoke+heat)")

    return ShieldResult(floor=floor, raised=floor > Level.GREEN,
                        reason="; ".join(reasons) if reasons else None)
