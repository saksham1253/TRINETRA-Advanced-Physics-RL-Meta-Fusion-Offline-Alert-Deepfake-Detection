"""trinetra.common.types — canonical data contracts (DESIGN/LLD.md §0, COMPONENT_DESIGN.md §2).

Dependency-light: dataclasses + enums only. Every probabilistic artifact carries a physics class
(A/B/C) and a trust marker; the system is advisory and fails safe to UNCERTAIN (Rule 19).
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum, IntEnum
from typing import Any

SCHEMA_VERSION = "1.0"


class Level(IntEnum):
    """Ordered advisory alert level. Ordering lets the shield take max() to only RAISE."""
    GREEN = 0
    YELLOW = 1
    ORANGE = 2
    RED = 3

    @property
    def label(self) -> str:
        return self.name

    @classmethod
    def raise_to(cls, a: "Level", b: "Level") -> "Level":
        return cls(max(int(a), int(b)))


class Hazard(str, Enum):
    LANDSLIDE = "LANDSLIDE"
    FLASHFLOOD = "FLASHFLOOD"
    CLOUDBURST = "CLOUDBURST"
    GLOF = "GLOF"
    FIRE = "FIRE"


class PhysicsClass(str, Enum):
    """Rule 20 labels. C = novel hypothesis, UNVALIDATED."""
    A = "A"            # established / validated
    B = "B"            # derived from A, validation route exists
    C = "C"            # novel hypothesis, unvalidated
    DATA = "data"      # data-driven (no physics class)
    ADVISORY = "advisory"


class Reliability(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    UNRELIABLE = "Unreliable"


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class ExpertOutput:
    """One expert's calibrated verdict (DESIGN/LLD.md §0)."""
    p: float                      # calibrated probability in [0,1]
    source: str
    u: float = 0.0                # uncertainty in [0,1]
    c: float = 1.0                # physics-consistency in [0,1] (NF-1)
    r: float = 1.0                # reliability/trust in [0,1] (NF-2)
    cls: PhysicsClass = PhysicsClass.DATA
    available: bool = True

    def __post_init__(self) -> None:
        for name in ("p", "u", "c", "r"):
            v = getattr(self, name)
            if not (0.0 <= float(v) <= 1.0):
                raise ValueError(f"ExpertOutput.{name} must be in [0,1], got {v!r} from {self.source}")


@dataclass
class Evidence:
    """Timestamped per-zone observation bundle (anti-leak: all feature t <= decision time)."""
    zone_id: str
    t: datetime
    eo: dict | None = None
    vision: dict | None = None
    iot: dict | None = None
    quality: dict = field(default_factory=dict)       # per-modality reliability in [0,1]
    provenance: dict = field(default_factory=dict)    # source ids, versions, seed, fold_id
    window: dict | None = None                        # {"start":..., "end":...}
    missing: list[str] = field(default_factory=list)  # modalities absent this window
    schema_version: str = SCHEMA_VERSION


@dataclass
class ShieldResult:
    floor: Level
    raised: bool
    reason: str | None


@dataclass
class ConformalResult:
    pred_set: list[str]
    coverage_target: float
    reliability: Reliability


@dataclass
class Decision:
    """Advisory decision handed to a human operator (COMPONENT_DESIGN.md §2.4). Never auto-dispatched."""
    zone_id: str
    t: datetime
    hazard: Hazard
    level: Level
    risk: float
    conformal: ConformalResult
    shield: ShieldResult
    contributions: list[ExpertOutput] = field(default_factory=list)
    uncertain: bool = False               # Rule 19 fail-safe: abstain + escalate
    advisory: bool = True                 # ALWAYS true; human-in-the-loop
    used_classC: bool = False             # Rule 20 transparency
    model_versions: dict = field(default_factory=dict)
    trace_id: str | None = None
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["t"] = self.t.isoformat()
        d["hazard"] = self.hazard.value
        d["level"] = self.level.name
        d["conformal"] = {
            "set": self.conformal.pred_set,
            "coverage_target": self.conformal.coverage_target,
            "reliability": self.conformal.reliability.value,
        }
        d["shield"] = {
            "floor": self.shield.floor.name,
            "raised": self.shield.raised,
            "reason": self.shield.reason,
        }
        d["contributions"] = [
            {"source": e.source, "p": e.p, "u": e.u, "c": e.c, "r": e.r,
             "cls": e.cls.value, "available": e.available}
            for e in self.contributions
        ]
        return d
