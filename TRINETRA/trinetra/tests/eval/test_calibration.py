"""Calibration metric + recalibrator tests (eval.calibration)."""
import unittest

import numpy as np

from trinetra.eval import (
    expected_calibration_error, maximum_calibration_error, reliability_curve,
    brier_decomposition, IsotonicCalibrator, PlattCalibrator,
)


class TestCalibrationMetrics(unittest.TestCase):
    def test_perfectly_calibrated_low_ece(self):
        rng = np.random.default_rng(0)
        p = rng.uniform(0, 1, 20000)
        y = (rng.uniform(0, 1, 20000) < p).astype(int)   # outcomes drawn AT the stated prob
        self.assertLess(expected_calibration_error(p, y, n_bins=10), 0.03)

    def test_miscalibrated_high_ece(self):
        p = np.full(1000, 0.9)
        y = np.zeros(1000, int)                           # says 0.9 but never happens
        self.assertGreater(expected_calibration_error(p, y), 0.8)
        self.assertGreater(maximum_calibration_error(p, y), 0.8)

    def test_reliability_curve_shapes(self):
        conf, acc, cnt = reliability_curve(np.linspace(0, 1, 100), np.r_[np.zeros(50), np.ones(50)], 10)
        self.assertEqual(len(conf), 10)
        self.assertEqual(int(cnt.sum()), 100)

    def test_brier_decomposition_adds_up(self):
        rng = np.random.default_rng(1)
        p = rng.uniform(0, 1, 5000); y = (rng.uniform(0, 1, 5000) < p).astype(int)
        d = brier_decomposition(p, y, 10)
        recon = d["reliability"] - d["resolution"] + d["uncertainty"]
        self.assertAlmostEqual(recon, d["brier"], places=1)


class TestRecalibrators(unittest.TestCase):
    def test_isotonic_reduces_ece(self):
        rng = np.random.default_rng(2)
        raw = rng.uniform(0, 1, 4000)
        y = (rng.uniform(0, 1, 4000) < raw ** 2).astype(int)   # true prob is raw^2 -> raw is miscalibrated
        cal = IsotonicCalibrator().fit(raw, y).predict(raw)
        self.assertLess(expected_calibration_error(cal, y), expected_calibration_error(raw, y))

    def test_isotonic_monotone(self):
        rng = np.random.default_rng(3)
        raw = rng.uniform(0, 1, 2000); y = (rng.uniform(0, 1, 2000) < raw).astype(int)
        c = IsotonicCalibrator().fit(raw, y)
        xs = np.linspace(0, 1, 50); pred = c.predict(xs)
        self.assertTrue(np.all(np.diff(pred) >= -1e-9))        # non-decreasing

    def test_platt_outputs_probabilities(self):
        rng = np.random.default_rng(4)
        raw = rng.uniform(0, 1, 2000); y = (rng.uniform(0, 1, 2000) < raw).astype(int)
        pred = PlattCalibrator().fit(raw, y).predict(raw)
        self.assertTrue((pred >= 0).all() and (pred <= 1).all())


if __name__ == "__main__":
    unittest.main()
