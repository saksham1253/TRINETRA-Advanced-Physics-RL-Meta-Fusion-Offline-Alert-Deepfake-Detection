"""Alerting tests (M8, Rule 19): human-gated CAP, severity mapping, operator approval, DTN."""
import unittest

from trinetra.common.config import Config
from trinetra.common.types import ExpertOutput, PhysicsClass, Hazard, Level
from trinetra.common.exceptions import SafetyViolation
from trinetra.ws5_fusion_rl import decide, ShieldSignals
from trinetra.ws3_alert import build_cap, cap_fields_for_level, present, approve, DTNQueue


def _orange_decision():
    experts = [ExpertOutput(p=0.01, source="geo_phys", u=0.1, cls=PhysicsClass.A)]
    return decide(experts, ShieldSignals(FS=0.7), Config(), hazard=Hazard.LANDSLIDE, zone_id="UK-CHX-07")


class TestHumanGate(unittest.TestCase):
    def test_cap_refused_without_approval(self):
        d = _orange_decision()
        with self.assertRaises(SafetyViolation):
            build_cap(d, approval_token=None, sender="SDMA-UK")

    def test_cap_refused_with_bogus_token(self):
        d = _orange_decision()
        with self.assertRaises(SafetyViolation):
            build_cap(d, approval_token="totally-not-approved", sender="SDMA-UK")

    def test_cap_built_after_approval(self):
        d = _orange_decision()
        token = approve(d, operator_id="SDMA-UK-14")
        xml = build_cap(d, approval_token=token, sender="SDMA-UK", key=b"k")
        self.assertIn("<severity>Severe</severity>", xml)
        self.assertIn("UK-CHX-07", xml)
        self.assertIn("advisory", xml)
        self.assertIn("signature hmac-sha256:", xml)

    def test_green_has_no_public_cap(self):
        self.assertIsNone(cap_fields_for_level(Level.GREEN))

    def test_approve_green_rejected(self):
        experts = [ExpertOutput(p=0.001, source="geo_phys", u=0.1, cls=PhysicsClass.A)]
        d = decide(experts, None, Config(), zone_id="z")
        self.assertEqual(d.level, Level.GREEN)
        with self.assertRaises(ValueError):
            approve(d, "op")


class TestSeverityMapping(unittest.TestCase):
    def test_mapping(self):
        self.assertEqual(cap_fields_for_level(Level.RED), ("Extreme", "Immediate", "Observed"))
        self.assertEqual(cap_fields_for_level(Level.ORANGE), ("Severe", "Expected", "Likely"))
        self.assertEqual(cap_fields_for_level(Level.YELLOW), ("Minor", "Future", "Possible"))


class TestOperatorConsole(unittest.TestCase):
    def test_present_mentions_advisory(self):
        txt = present(_orange_decision())
        self.assertIn("ADVISORY", txt)
        self.assertIn("human operator must review", txt)


class TestDTN(unittest.TestCase):
    def test_spray_and_deliver(self):
        q = DTNQueue(L=8)
        q.enqueue("m1", b"payload")
        self.assertIn("m1", q.pending())
        given = q.relay("m1")
        self.assertEqual(given, 4)            # binary spray hands off half
        q.deliver("m1")
        self.assertNotIn("m1", q.pending())


if __name__ == "__main__":
    unittest.main()
