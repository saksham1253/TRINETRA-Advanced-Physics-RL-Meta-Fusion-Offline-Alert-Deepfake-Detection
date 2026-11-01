"""ws7_iot.sensor_reading — SensorReading contract, validation, and message authentication (M7).

COMPONENT_DESIGN.md §2.1. Signing: Ed25519 is specified for the real node (provisioned at flashing), but
the `cryptography` library is not available in this environment, so we authenticate with HMAC-SHA256 as an
HONEST PLACEHOLDER (clearly labelled). Replay protection is by (node_id, seq) with a monotonic window.
"""
from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass, field, asdict

SCHEMA_VERSION = "1.0"


@dataclass
class SensorReading:
    node_id: str
    zone_id: str
    t: str                       # ISO8601 UTC
    seq: int
    batt_mV: int
    readings: dict               # tilt_deg, tilt_rate_dps, soil_vwc, piezo_kPa, rain_mm_15m, temp_C, ...
    health: dict = field(default_factory=dict)
    edge_flag: dict = field(default_factory=lambda: {"level": "NONE", "rule": None})
    rssi: int = 0
    snr: float = 0.0
    fw: str = "0.3.1"
    sig: str | None = None
    schema_version: str = SCHEMA_VERSION

    def signing_bytes(self) -> bytes:
        d = asdict(self); d.pop("sig", None)
        return json.dumps(d, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign_reading(r: SensorReading, key: bytes) -> SensorReading:
    """Attach an HMAC-SHA256 tag (placeholder for Ed25519). Returns the same object for chaining."""
    r.sig = "hmac-sha256:" + hmac.new(key, r.signing_bytes(), hashlib.sha256).hexdigest()
    return r


def verify_reading(r: SensorReading, key: bytes) -> bool:
    if not r.sig or not r.sig.startswith("hmac-sha256:"):
        return False
    expect = hmac.new(key, r.signing_bytes(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(r.sig.split(":", 1)[1], expect)


class ReplayGuard:
    """Reject out-of-order / replayed frames per node by sequence number (anti-replay, C6)."""

    def __init__(self):
        self._last: dict[str, int] = {}

    def accept(self, node_id: str, seq: int) -> bool:
        last = self._last.get(node_id, -1)
        if seq <= last:
            return False
        self._last[node_id] = seq
        return True


REQUIRED_READING_KEYS = ("tilt_deg", "tilt_rate_dps", "soil_vwc", "rain_mm_15m", "temp_C")


def validate_reading(r: SensorReading) -> list[str]:
    """Return a list of validation problems ([] = valid). Does not raise (callers decide)."""
    problems = []
    if r.schema_version != SCHEMA_VERSION:
        problems.append(f"schema_version {r.schema_version} != {SCHEMA_VERSION}")
    if r.seq < 0:
        problems.append("seq must be >= 0")
    if not (2000 <= r.batt_mV <= 5000):
        problems.append(f"batt_mV out of plausible range: {r.batt_mV}")
    for k in REQUIRED_READING_KEYS:
        if k not in r.readings:
            problems.append(f"missing reading: {k}")
    lvl = r.edge_flag.get("level")
    if lvl not in ("NONE", "WATCH", "LOCAL_SIREN"):
        problems.append(f"invalid edge_flag.level: {lvl}")
    return problems
