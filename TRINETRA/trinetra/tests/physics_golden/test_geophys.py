"""Golden-case tests for the geo physics gate (gate G1). DESIGN/LLD.md §2.

These encode the correctness invariants the research flagged as bugs in the original report:
  - FS saturated limit (sigma_s -> 0) and monotonicity in suction / pore pressure
  - Iverson transient term: slope enters ONLY via D1 = D0/cos^2(beta) (no extra cos(beta))
  - Fukuzono: alpha=2 => 1/v linear => recover t_f
  - Caine I-D exceedance direction
"""
import math
import unittest

import numpy as np

from trinetra.ws1b_geophys import (
    factor_of_safety, factor_of_safety_saturated, inverse_velocity_fit,
    caine_exceedance, transient_head, diffusivity_D1, ierfc,
)
from trinetra.ws1b_geophys.iverson import _transient_core


class TestFS(unittest.TestCase):
    base = dict(c_prime=5.0, phi_prime_deg=32.0, gamma=18.0, z=2.0, beta_deg=30.0)

    def test_saturated_limit(self):
        # sigma_s -> 0 must equal the saturated form exactly
        fs_general = factor_of_safety(**self.base, u_w=10.0, sigma_s=0.0)
        fs_sat = factor_of_safety_saturated(**self.base, u_w=10.0)
        self.assertAlmostEqual(float(fs_general), float(fs_sat), places=12)

    def test_monotonic_in_suction(self):
        fs_lo = factor_of_safety(**self.base, u_w=5.0, sigma_s=0.0)
        fs_hi = factor_of_safety(**self.base, u_w=5.0, sigma_s=8.0)
        self.assertGreater(float(fs_hi), float(fs_lo))   # more suction => more stable

    def test_decreasing_in_pore_pressure(self):
        fs_dry = factor_of_safety(**self.base, u_w=0.0)
        fs_wet = factor_of_safety(**self.base, u_w=15.0)
        self.assertGreater(float(fs_dry), float(fs_wet))


class TestIverson(unittest.TestCase):
    def test_ierfc_at_zero(self):
        self.assertAlmostEqual(float(ierfc(0.0)), 1.0 / math.sqrt(math.pi), places=12)

    def test_transient_zero_at_t0(self):
        val = transient_head(Z=1.0, t=0.0, D0=1e-4, K_z=1e-5, I_z=5e-6, beta_deg=25.0)
        self.assertAlmostEqual(float(val), 0.0, places=12)

    def test_slope_only_through_D1(self):
        # The slope-dependent transient_head must equal the slope-FREE core evaluated at D1=D0/cos^2 beta.
        Z, t, D0, Kz, Iz, beta = 1.5, 3600.0, 2e-4, 1e-5, 8e-6, 35.0
        via_api = float(transient_head(Z, t, D0, Kz, Iz, beta))
        D1 = diffusivity_D1(D0, beta)
        via_core = float(_transient_core(np.array(Z), np.array(t), D1, Iz, Kz))
        self.assertAlmostEqual(via_api, via_core, places=12)
        # And it must NOT equal a buggy version with an extra cos^2(beta) factor on the response.
        buggy = via_core * math.cos(math.radians(beta)) ** 2
        self.assertNotAlmostEqual(via_api, buggy, places=6)


class TestFukuzono(unittest.TestCase):
    def test_recover_tf_alpha2(self):
        t_f_true = 100.0
        t = np.linspace(0, 90, 10)
        inv_v = 0.5 * (t_f_true - t)          # 1/v linear, hits 0 at t_f
        v = 1.0 / inv_v
        fit = inverse_velocity_fit(t, v, alpha=2.0)
        self.assertAlmostEqual(fit.t_failure, t_f_true, places=4)
        self.assertGreater(fit.r2, 0.999)


class TestCaine(unittest.TestCase):
    def test_exceedance_direction(self):
        exc_hi, ratio_hi = caine_exceedance(I_mm_h=30.0, D_hours=3.0, a=14.0, b=0.39)
        exc_lo, ratio_lo = caine_exceedance(I_mm_h=2.0, D_hours=3.0, a=14.0, b=0.39)
        self.assertTrue(bool(exc_hi)); self.assertFalse(bool(exc_lo))
        self.assertGreater(float(ratio_hi), float(ratio_lo))


if __name__ == "__main__":
    unittest.main()
