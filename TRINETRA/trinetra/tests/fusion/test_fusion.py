"""Fusion + shield invariants (gate G4). PHARAOH is Class-C and must stay opt-in with an FM-1 fallback."""
import unittest

import numpy as np

from trinetra.common.config import Config
from trinetra.common.types import ExpertOutput, PhysicsClass, Level
from trinetra.ws5_fusion_rl import (
    pharaoh_mean, pharaoh_order, fuse, fm1_precision_weighted, nf4_salience,
    shield_floor, ShieldSignals,
)


def _experts():
    return [
        ExpertOutput(p=0.30, source="geo_phys", u=0.2, c=1.0, r=0.9, cls=PhysicsClass.A),
        ExpertOutput(p=0.50, source="anomaly", u=0.3, c=0.8, r=0.7, cls=PhysicsClass.DATA),
        ExpertOutput(p=0.40, source="rl_policy", u=0.25, c=0.9, r=0.6, cls=PhysicsClass.ADVISORY),
    ]


class TestPharaoh(unittest.TestCase):
    def test_ge_arithmetic_mean_for_rho_ge_1(self):
        # Anti-complacency safety corollary: power mean (rho>=1) >= arithmetic mean.
        ps = [0.1, 0.4, 0.9]; w = [1.0, 1.0, 1.0]
        amean = float(np.mean(ps))
        for rho in [1.0, 1.5, 2.0, 4.0, 8.0]:
            self.assertGreaterEqual(pharaoh_mean(ps, w, rho) + 1e-12, amean)

    def test_order_rises_with_disagreement_and_salience(self):
        agree = pharaoh_order([0.4, 0.41, 0.4], [1, 1, 1], salience=0.9)
        disagree = pharaoh_order([0.05, 0.5, 0.95], [1, 1, 1], salience=0.9)
        self.assertGreater(disagree, agree)
        self.assertGreaterEqual(agree, 1.0)


class TestFuseDispatch(unittest.TestCase):
    def test_default_is_fm1_not_classC(self):
        res = fuse(_experts(), Config())
        self.assertEqual(res.model, "FM-1")
        self.assertFalse(res.used_classC)

    def test_pharaoh_opt_in(self):
        cfg = Config(); cfg.data["fusion"]["operator"]["pharaoh"] = True
        res = fuse(_experts(), cfg)
        self.assertEqual(res.model, "PHARAOH")
        self.assertTrue(res.used_classC)

    def test_no_experts_max_uncertainty(self):
        res = fuse([], Config())
        self.assertEqual(res.u_star, 1.0)


class TestShield(unittest.TestCase):
    def test_single_node_cannot_reach_red(self):
        s = ShieldSignals(tilt_rate_deg_per_day=9.0, nodes_agree=1)
        self.assertLess(shield_floor(s).floor, Level.RED)

    def test_corroborated_tilt_reaches_red(self):
        s = ShieldSignals(tilt_rate_deg_per_day=9.0, nodes_agree=3)
        self.assertEqual(shield_floor(s).floor, Level.RED)

    def test_fs_below_one_raises_orange(self):
        self.assertEqual(shield_floor(ShieldSignals(FS=0.8)).floor, Level.ORANGE)

    def test_green_when_nothing_triggers(self):
        self.assertEqual(shield_floor(ShieldSignals()).floor, Level.GREEN)


if __name__ == "__main__":
    unittest.main()
