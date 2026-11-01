"""Advanced conformal tests (ws6_robust.conformal): ACI drift coverage, Mondrian per-group, CRC miss-risk."""
import unittest

import numpy as np

from trinetra.ws6_robust import AdaptiveConformal, MondrianConformal, conformal_risk_threshold
from trinetra.ws6_robust.conformal import conformal_quantile


class TestAdaptiveConformal(unittest.TestCase):
    def test_long_run_coverage_under_drift(self):
        # residual scale DRIFTS upward over time; static CP would under-cover, ACI should track ~90%.
        rng = np.random.default_rng(0)
        aci = AdaptiveConformal(alpha_target=0.1, gamma=0.05)
        cal = np.abs(rng.normal(0, 1.0, 200))             # initial calibration residual magnitudes
        covered_flags = []
        for t in range(3000):
            scale = 1.0 + 3.0 * t / 3000.0                # growing spread (concept drift)
            q = aci.quantile(cal)
            new_resid = abs(rng.normal(0, scale))
            covered = new_resid <= q
            covered_flags.append(covered)
            aci.step(covered)
            cal = np.r_[cal[1:], new_resid]               # slide calibration window with drift
        realized = np.mean(covered_flags[500:])           # after warmup
        self.assertGreater(realized, 0.82)
        self.assertLess(realized, 0.97)

    def test_alpha_moves_after_miss_to_widen(self):
        # ACI: alpha_{t+1} = alpha_t + gamma*(alpha_target - err). A miss (err=1) DECREASES alpha, which
        # raises the (1-alpha) quantile => the next interval WIDENS. That is the correct self-correction.
        aci = AdaptiveConformal(alpha_target=0.1, gamma=0.1)
        a0 = aci.alpha_t
        aci.step(covered=False)
        self.assertLess(aci.alpha_t, a0)
        cal = np.abs(np.linspace(0, 1, 100))
        q_after = aci.quantile(cal)
        aci2 = AdaptiveConformal(alpha_target=0.1, gamma=0.1)
        self.assertGreaterEqual(q_after, aci2.quantile(cal))   # wider (>=) after the miss


class TestMondrian(unittest.TestCase):
    def test_per_group_quantiles_differ(self):
        groups = np.array(["LANDSLIDE"] * 100 + ["GLOF"] * 100)
        scores = np.r_[np.abs(np.linspace(0, 1, 100)), np.abs(np.linspace(0, 5, 100))]
        m = MondrianConformal(alpha=0.1).fit(groups, scores)
        self.assertLess(m.quantile("LANDSLIDE"), m.quantile("GLOF"))

    def test_unseen_group_is_conservative(self):
        m = MondrianConformal(0.1).fit(np.array(["A", "B"]), np.array([1.0, 9.0]))
        self.assertEqual(m.quantile("ZZZ"), max(m._q.values()))


class TestConformalRiskControl(unittest.TestCase):
    def test_threshold_controls_miss_rate(self):
        rng = np.random.default_rng(1)
        n = 4000
        y = (rng.uniform(0, 1, n) < 0.2).astype(int)
        # score correlates with the label so a low threshold catches most events
        score = np.clip(0.1 + 0.6 * y + rng.normal(0, 0.2, n), 0, 1)
        lam = conformal_risk_threshold(score, y, target_risk=0.03)
        realized_miss = np.mean((y == 1) & (score < lam))
        self.assertLessEqual(realized_miss, 0.05)          # miss-risk bounded near target


if __name__ == "__main__":
    unittest.main()
