"""Calibration + drift + degradation tests (gate G3/M4)."""
import unittest

import numpy as np

from trinetra.ws6_robust import (
    conformal_quantile, regression_interval, empirical_coverage,
    population_stability_index, check_drift, CusumState, cusum_update,
    apply_missing_modality,
)
from trinetra.common.types import ExpertOutput, PhysicsClass


class TestConformal(unittest.TestCase):
    def test_marginal_coverage_approx(self):
        rng = np.random.default_rng(0)
        alpha = 0.1
        # Exchangeable data: residuals ~ N(0,1). Calibrate then test coverage ~ 1-alpha.
        cal = rng.normal(size=2000)
        q = conformal_quantile(np.abs(cal), alpha)
        test = rng.normal(size=5000)
        cov = np.mean(np.abs(test) <= q)
        self.assertGreater(cov, 1 - alpha - 0.03)
        self.assertLess(cov, 1 - alpha + 0.03)

    def test_interval_covers(self):
        rng = np.random.default_rng(1)
        cal_res = rng.normal(size=1000)
        lo, hi = regression_interval(np.zeros(500), cal_res, alpha=0.1)
        y = rng.normal(size=500)
        self.assertGreater(empirical_coverage(lo, hi, y), 0.85)


class TestDrift(unittest.TestCase):
    def test_psi_zero_for_same_dist(self):
        rng = np.random.default_rng(0)
        x = rng.normal(size=5000)
        self.assertLess(population_stability_index(x, rng.normal(size=5000)), 0.05)

    def test_psi_flags_shift(self):
        rng = np.random.default_rng(0)
        ref = rng.normal(0, 1, 5000)
        cur = rng.normal(3, 1, 5000)
        rep = check_drift(ref, cur)
        self.assertTrue(rep.psi_drift)

    def test_cusum_detects_step(self):
        st = CusumState(); flagged = False
        for x in [0.0] * 20 + [3.0] * 20:
            st, f = cusum_update(st, x, target=0.0, k=0.5, h=5.0)
            flagged = flagged or f
        self.assertTrue(flagged)


class TestMissingModality(unittest.TestCase):
    def test_absent_marked_unavailable_and_others_more_uncertain(self):
        experts = [
            ExpertOutput(p=0.4, source="geo_phys", u=0.2, cls=PhysicsClass.A),
            ExpertOutput(p=0.5, source="anomaly", u=0.2, cls=PhysicsClass.DATA),
            ExpertOutput(p=0.3, source="fire_phys", u=0.2, cls=PhysicsClass.A),
        ]
        out = apply_missing_modality(experts, present_sources={"geo_phys", "anomaly"})
        by = {e.source: e for e in out}
        self.assertFalse(by["fire_phys"].available)
        self.assertGreater(by["geo_phys"].u, 0.2)   # uncertainty inflated by the missing peer


if __name__ == "__main__":
    unittest.main()
