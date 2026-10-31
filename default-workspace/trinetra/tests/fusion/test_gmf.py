"""GMF (gated mixture fusion) invariants (M6)."""
import unittest

import numpy as np

from trinetra.common.config import Config
from trinetra.common.types import ExpertOutput, PhysicsClass
from trinetra.ws5_fusion_rl import gmf_fuse, gated_weights, fuse, load_numpy_head


def _experts():
    return [
        ExpertOutput(p=0.20, source="geo_phys", u=0.2, c=1.0, r=0.9, cls=PhysicsClass.A),
        ExpertOutput(p=0.60, source="anomaly", u=0.3, c=0.8, r=0.7, cls=PhysicsClass.DATA),
        ExpertOutput(p=0.40, source="fire_phys", u=0.25, c=0.9, r=0.6, cls=PhysicsClass.A),
    ]


class TestGMF(unittest.TestCase):
    def test_gate_sums_to_one(self):
        w = gated_weights(_experts())
        self.assertAlmostEqual(float(np.sum(w)), 1.0, places=9)

    def test_no_head_means_zero_residual(self):
        r = gmf_fuse(_experts())
        self.assertEqual(r.residual, 0.0)
        self.assertAlmostEqual(r.p, r.base, places=12)

    def test_residual_is_hard_bounded(self):
        # A rogue head returning a huge value must be clipped to +/- cap.
        r = gmf_fuse(_experts(), residual_cap=0.1, head=lambda f: 999.0)
        self.assertLessEqual(r.residual, 0.1 + 1e-9)
        r2 = gmf_fuse(_experts(), residual_cap=0.1, head=lambda f: -999.0)
        self.assertGreaterEqual(r2.residual, -0.1 - 1e-9)

    def test_dispatch_selects_gmf(self):
        cfg = Config(); cfg.data["fusion"]["model"] = "GMF"
        res = fuse(_experts(), cfg)
        self.assertEqual(res.model, "GMF")
        self.assertFalse(res.used_classC)   # GMF with pharaoh off is Class-B, not C

    def test_empty_experts_safe(self):
        r = gmf_fuse([])
        self.assertEqual(r.p, 0.0)

    def test_numpy_head_export_loads_and_stays_bounded(self):
        # Exported-head JSON (as kaggle/train_fusion_head.py writes). Pure numpy; no torch needed.
        exported = {
            "cap": 0.1,
            "W1": [[0.5, -0.3, 0.2], [0.1, 0.4, -0.6], [-0.2, 0.3, 0.5], [0.4, -0.1, 0.2]],
            "b1": [0.0, 0.1, -0.1, 0.0],
            "W2": [[10.0, -10.0, 5.0, 2.0]],   # large weights -> raw would blow up; cap must bound it
            "b2": [3.0],
        }
        head = load_numpy_head(exported)
        r = gmf_fuse(_experts(), residual_cap=0.1, head=head)
        self.assertLessEqual(abs(r.residual), 0.1 + 1e-9)   # bounded despite large export weights
        self.assertTrue(0.0 <= r.p <= 1.0)


if __name__ == "__main__":
    unittest.main()
