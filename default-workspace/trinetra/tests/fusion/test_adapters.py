"""Deep-model -> ExpertOutput adapter tests (torch-free): class labels + reliability caps + decide() flow."""
import unittest

from trinetra.common.config import Config
from trinetra.common.types import PhysicsClass, Hazard
from trinetra.ws5_fusion_rl import deep_expert, decide, ShieldSignals


class TestDeepExpertAdapters(unittest.TestCase):
    def test_deepfake_reliability_hard_capped(self):
        e = deep_expert("deepfake", prob=0.9, reliability=0.99)
        self.assertLessEqual(e.r, 0.4)                 # trust cap enforced (Rule 19)
        self.assertEqual(e.cls, PhysicsClass.DATA)

    def test_geo_pinn_is_class_b(self):
        e = deep_expert("geo_pinn", prob=0.7)
        self.assertEqual(e.cls, PhysicsClass.B)
        self.assertLessEqual(e.r, 1.0)

    def test_prob_clamped(self):
        self.assertEqual(deep_expert("anomaly", prob=1.5).p, 1.0)
        self.assertEqual(deep_expert("anomaly", prob=-0.2).p, 0.0)

    def test_unknown_source_rejected(self):
        with self.assertRaises(KeyError):
            deep_expert("mystery_model", prob=0.5)

    def test_flows_through_decide(self):
        experts = [
            deep_expert("geo_pinn", prob=0.2, uncertainty=0.2),
            deep_expert("anomaly", prob=0.6, uncertainty=0.3),
            deep_expert("deepfake", prob=0.8),         # low-trust; must not dominate
        ]
        d = decide(experts, ShieldSignals(FS=0.7), Config(), hazard=Hazard.LANDSLIDE, zone_id="z")
        self.assertIn(d.level.name, {"YELLOW", "ORANGE", "RED"})   # shield floor from FS<1 applies
        # deepfake low reliability should keep its influence small: risk not pulled to ~0.8
        self.assertLess(d.risk, 0.8)


if __name__ == "__main__":
    unittest.main()
