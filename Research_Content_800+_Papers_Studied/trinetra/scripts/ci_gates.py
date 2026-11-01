"""scripts/ci_gates.py — fail-closed CI invariants (REPO_BLUEPRINT §4). Run: python scripts/ci_gates.py

These are SAFETY/HONESTY gates, not performance tests. Any failure exits non-zero. Checks:
  G-advisory  : human-approval is hard-wired; CAP refuses without an approval token (Rule 19)
  G-classC    : Class-C paths (PHARAOH, ND*) default OFF (Rule 20)
  G-security  : endpoint allow-list is fail-closed; raw video cannot egress (C6/C7)
  G-leak      : look-ahead feature timestamps are rejected (G6)
  G-iot       : LoRa frame within the <=51 B budget (G5)
  G-legacy    : no banned legacy/buggy code tokens present in src/
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trinetra.common.config import Config                                   # noqa: E402
from trinetra.common.security import check_endpoint, assert_no_video_egress  # noqa: E402
from trinetra.common.exceptions import (                                     # noqa: E402
    EndpointNotAllowed, SafetyViolation, LeakageError,
)
from trinetra.eval import assert_no_time_leak                                # noqa: E402
from trinetra.ws7_iot import FRAME_LEN                                       # noqa: E402

# Banned substrings that would signal a reintroduced bug (e.g. extra cos factor on Iverson transient).
BANNED_TOKENS = ["EXTRA_COSBETA_ON_TRANSIENT", "advisory = False", "advisory=False"]

CHECKS: list[tuple[str, callable]] = []


def gate(name):
    def deco(fn):
        CHECKS.append((name, fn)); return fn
    return deco


@gate("G-advisory")
def _advisory():
    assert Config().require_human_approval() is True, "human approval must be hard-wired True"
    from trinetra.common.types import Hazard, Level, Decision, ConformalResult, ShieldResult, Reliability, utcnow
    from trinetra.ws3_alert import build_cap
    d = Decision(zone_id="z", t=utcnow(), hazard=Hazard.LANDSLIDE, level=Level.ORANGE, risk=0.3,
                 conformal=ConformalResult(["ORANGE"], 0.9, Reliability.MEDIUM),
                 shield=ShieldResult(Level.ORANGE, True, "x"))
    try:
        build_cap(d, approval_token=None, sender="x")
    except SafetyViolation:
        return
    raise AssertionError("CAP must refuse to build without a human approval token")


@gate("G-classC")
def _classc():
    c = Config()
    assert c.get("fusion.operator.pharaoh") is False, "PHARAOH must default OFF"
    for i in range(1, 8):
        assert c.get(f"firephys.nd{i}") is False, f"ND-{i} must default OFF"


@gate("G-security")
def _security():
    try:
        check_endpoint("https://evil.example.com/x", allowlist=[])
    except EndpointNotAllowed:
        pass
    else:
        raise AssertionError("empty allow-list must reject all endpoints")
    try:
        assert_no_video_egress({"zone": "z", "clip": b"rawbytes"})
    except SafetyViolation:
        pass
    else:
        raise AssertionError("raw video must not be allowed to egress")


@gate("G-leak")
def _leak():
    try:
        assert_no_time_leak([1, 2, 11], decision_time=10)
    except LeakageError:
        return
    raise AssertionError("future feature timestamps must be rejected")


@gate("G-iot")
def _iot():
    assert FRAME_LEN <= 51, f"LoRa frame {FRAME_LEN} B exceeds 51 B budget"


@gate("G-legacy")
def _legacy():
    hits = []
    for p in (ROOT / "src").rglob("*.py"):
        txt = p.read_text(encoding="utf-8")
        for tok in BANNED_TOKENS:
            if tok in txt and "BANNED_TOKENS" not in txt.splitlines()[0:0] and p.name != "ci_gates.py":
                hits.append(f"{p.name}:{tok}")
    assert not hits, f"banned legacy tokens present: {hits}"


def main() -> int:
    failures = []
    for name, fn in CHECKS:
        try:
            fn(); print(f"  [PASS] {name}")
        except Exception as e:  # noqa: BLE001
            failures.append((name, e)); print(f"  [FAIL] {name}: {e}")
    print("-" * 60)
    if failures:
        print(f"CI GATES FAILED: {len(failures)}/{len(CHECKS)}")
        return 1
    print(f"ALL {len(CHECKS)} CI GATES PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
