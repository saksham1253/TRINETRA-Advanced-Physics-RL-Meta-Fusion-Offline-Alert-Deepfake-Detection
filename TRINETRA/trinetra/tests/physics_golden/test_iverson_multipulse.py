"""Iverson multi-pulse superposition golden tests (ws1b_geophys.iverson)."""
import unittest

import numpy as np

from trinetra.ws1b_geophys.iverson import transient_head, transient_head_multipulse


D0, K_z, beta = 1e-4, 1e-5, 30.0
I = 5e-6


class TestIversonMultipulse(unittest.TestCase):
    def test_single_step_matches_transient_head(self):
        Z, t = 1.0, 3600.0
        single = transient_head(Z, t, D0, K_z, I, beta)
        multi = transient_head_multipulse(Z, t, [0.0], [I], D0, K_z, beta)
        self.assertAlmostEqual(float(single), float(multi), places=12)

    def test_finite_pulse_recovers_after_rain_stops(self):
        Z = 1.0
        T = 3600.0
        steps_t, steps_I = [0.0, T], [I, 0.0]       # rain on [0,T], then off
        during = transient_head_multipulse(Z, T, steps_t, steps_I, D0, K_z, beta)
        single_during = transient_head(Z, T, D0, K_z, I, beta)
        self.assertAlmostEqual(float(during), float(single_during), places=10)  # equal up to T
        after = transient_head_multipulse(Z, 2 * T, steps_t, steps_I, D0, K_z, beta)
        single_after = transient_head(Z, 2 * T, D0, K_z, I, beta)
        self.assertLess(float(after), float(single_after))     # recovery: less than if rain had continued
        self.assertGreater(float(after), 0.0)

    def test_superposition_linearity(self):
        Z, t = 1.0, 7200.0
        # two onset times combined == sum of each pulse's standalone contribution (linear response)
        combined = transient_head_multipulse(Z, t, [0.0, 3600.0], [I, 2 * I], D0, K_z, beta)
        p1 = transient_head_multipulse(Z, t, [0.0], [I], D0, K_z, beta)              # step +I at 0
        p2 = transient_head_multipulse(Z, t, [3600.0], [I], D0, K_z, beta)           # step +I at 3600
        self.assertAlmostEqual(float(combined), float(p1 + p2), places=10)

    def test_intensity_monotone(self):
        Z, t = 1.0, 3600.0
        lo = transient_head_multipulse(Z, t, [0.0], [I], D0, K_z, beta)
        hi = transient_head_multipulse(Z, t, [0.0], [2 * I], D0, K_z, beta)
        self.assertGreater(float(hi), float(lo))


if __name__ == "__main__":
    unittest.main()
