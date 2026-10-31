"""Single decision function invariants (gate G3, Rule 19)."""
import unittest

from trinetra.common.config import Config
from trinetra.common.types import ExpertOutput, PhysicsClass, Level, Hazard
from trinetra.ws5_fusion_rl import decide, ShieldSignals, conformal_level


class TestConformalLevel(unittest.TestCase):
    def test_bands_monotone(self):
        p = 0.0476
        self.assertEqual(conformal_level(0.0, p), Level.GREEN)
        self.assertEqual(conformal_level(0.1, p), Level.YELLOW)
        self.assertEqual(conformal_level(0.3, p), Level.ORANGE)
        self.assertEqual(conformal_level(0.9, p), Level.RED)


class TestDecide(unittest.TestCase):
    def test_shield_can_only_raise(self):
        # Low fused risk (GREEN) but FS<1 shield => final at least ORANGE.
        experts = [ExpertOutput(p=0.01, source="geo_phys", u=0.1, cls=PhysicsClass.A)]
        d = decide(experts, ShieldSignals(FS=0.7), Config(), hazard=Hazard.LANDSLIDE)
        self.assertGreaterEqual(d.level, Level.ORANGE)
        self.assertTrue(d.shield.raised)

    def test_always_advisory(self):
        d = decide([ExpertOutput(p=0.9, source="x", u=0.1)], None, Config())
        self.assertTrue(d.advisory)

    def test_failsafe_uncertain_when_no_experts(self):
        d = decide([], None, Config())
        self.assertTrue(d.uncertain)   # abstain + escalate, never silent

    def test_uncertain_on_high_conflict(self):
        experts = [
            ExpertOutput(p=0.02, source="a", u=0.9, cls=PhysicsClass.A),
            ExpertOutput(p=0.98, source="b", u=0.9, cls=PhysicsClass.DATA),
        ]
        d = decide(experts, None, Config())
        self.assertTrue(d.uncertain)

    def test_classC_flagged_when_pharaoh_on(self):
        cfg = Config(); cfg.data["fusion"]["operator"]["pharaoh"] = True
        experts = [
            ExpertOutput(p=0.3, source="a", u=0.2, cls=PhysicsClass.A),
            ExpertOutput(p=0.4, source="b", u=0.2, cls=PhysicsClass.DATA),
        ]
        d = decide(experts, None, cfg)
        self.assertTrue(d.used_classC)

    def test_to_dict_roundtrip(self):
        d = decide([ExpertOutput(p=0.5, source="a", u=0.2)], ShieldSignals(FS=0.9), Config())
        js = d.to_dict()
        self.assertIn("level", js)
        self.assertIn("shield", js)
        self.assertEqual(js["advisory"], True)


if __name__ == "__main__":
    unittest.main()
