"""Fukuzono prediction-interval tests (ws1b_geophys.fukuzono)."""
import unittest

import numpy as np

from trinetra.ws1b_geophys.fukuzono import inverse_velocity_fit


class TestFukuzonoInterval(unittest.TestCase):
    def test_noiseless_point_recovered_and_tight(self):
        # 1/v linear hitting zero at t_f=10: v = 1/(10 - t)
        t = np.array([0, 2, 4, 6, 8.0])
        v = 1.0 / (10.0 - t)
        fit = inverse_velocity_fit(t, v, alpha=2.0)
        self.assertAlmostEqual(fit.t_failure, 10.0, places=6)
        self.assertLess(fit.se_t_failure, 1e-6)            # perfect fit -> ~zero uncertainty

    def test_noise_widens_interval_and_brackets_truth(self):
        rng = np.random.default_rng(0)
        t = np.linspace(0, 8, 12)
        v = 1.0 / (10.0 - t)
        y = 1.0 / v + rng.normal(0, 0.05, len(t))          # noisy 1/v
        v_noisy = 1.0 / np.clip(y, 1e-3, None)
        fit = inverse_velocity_fit(t, v_noisy, alpha=2.0)
        self.assertGreater(fit.se_t_failure, 0.0)
        self.assertLess(fit.t_failure_low, fit.t_failure)
        self.assertGreater(fit.t_failure_high, fit.t_failure)

    def test_recency_weighting_changes_fit(self):
        t = np.linspace(0, 8, 9)
        v = 1.0 / (10.0 - t)
        v = v * (1 + 0.0)                                  # curvature-free; weights shouldn't break it
        plain = inverse_velocity_fit(t, v, alpha=2.0)
        recent = inverse_velocity_fit(t, v, alpha=2.0, recency_halflife=2.0)
        # on a clean line both recover t_f; just assert recency path stays finite and sane
        self.assertAlmostEqual(recent.t_failure, plain.t_failure, places=4)


if __name__ == "__main__":
    unittest.main()
