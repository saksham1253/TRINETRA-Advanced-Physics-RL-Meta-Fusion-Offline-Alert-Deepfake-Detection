"""Bootstrap-stats tests (eval._stats): normal cdf/ppf, BCa interval, stationary bootstrap."""
import unittest

import numpy as np

from trinetra.eval._stats import norm_cdf, norm_ppf, bca_interval, stationary_bootstrap_indices


class TestNormal(unittest.TestCase):
    def test_cdf_ppf_inverse(self):
        for p in [0.025, 0.1, 0.5, 0.9, 0.975]:
            self.assertAlmostEqual(norm_cdf(norm_ppf(p)), p, places=4)

    def test_known_quantiles(self):
        self.assertAlmostEqual(norm_ppf(0.975), 1.959964, places=3)
        self.assertAlmostEqual(norm_cdf(0.0), 0.5, places=6)


class TestBCa(unittest.TestCase):
    def test_bca_brackets_statistic(self):
        rng = np.random.default_rng(0)
        data = rng.normal(5.0, 1.0, 200)
        boot = np.array([rng.choice(data, len(data)).mean() for _ in range(2000)])
        jk = np.array([np.delete(data, k).mean() for k in range(len(data))])
        lo, hi = bca_interval(boot, data.mean(), jk, alpha=0.05)
        self.assertLess(lo, data.mean())
        self.assertGreater(hi, data.mean())
        self.assertLess(lo, 5.0 + 1e-6)
        self.assertGreater(hi, 5.0 - 1e-6)


class TestStationaryBootstrap(unittest.TestCase):
    def test_length_and_range(self):
        rng = np.random.default_rng(1)
        idx = stationary_bootstrap_indices(50, avg_block=5, rng=rng)
        self.assertEqual(len(idx), 50)
        self.assertTrue(idx.min() >= 0 and idx.max() < 50)


if __name__ == "__main__":
    unittest.main()
