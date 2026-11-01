"""ws3_alert.siren — local siren actuation bus (M8, offline physical warning).

Local sirens are the ONE autonomous actuation allowed (co-located, physical, bounded by the shield / Tier-0
rule). Public messaging stays human-gated. This bus just records/dispatches a siren command; integration
with GPIO/relay is firmware-side.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class SirenEvent:
    zone_id: str
    level: str
    source: str                       # 'node_edge' | 'shield' | 'operator'
    t: str


@dataclass
class SirenBus:
    log: list[SirenEvent] = field(default_factory=list)

    def fire(self, zone_id: str, level: str, source: str) -> SirenEvent:
        ev = SirenEvent(zone_id=zone_id, level=level, source=source,
                        t=datetime.now(timezone.utc).isoformat())
        self.log.append(ev)
        return ev
