"""Golden/contract tests for the fire physics layer (gate G1 + Rule 20 flag-gating)."""
import math
import unittest

from trinetra.common.config import Config
from trinetra.ws1a_firephys import (
    flame_height_heskestad, strouhal_puffing_frequency, byram_convection_number,
    graybody_radiance, graybody_temperature, aliased_frequency,
    nd2_transmittance_temperature, fire_gate, FireInputs,
)


class TestEstablished(unittest.TestCase):
    def test_flame_height_increases_with_Q(self):
        self.assertLess(flame_height_heskestad(100, 0.5), flame_height_heskestad(1000, 0.5))

    def test_strouhal_decreases_with_size(self):
        self.assertGreater(strouhal_puffing_frequency(0.3), strouhal_puffing_frequency(2.0))

    def test_graybody_roundtrip(self):
        T = 900.0
        self.assertAlmostEqual(graybody_temperature(graybody_radiance(T)), T, places=6)

    def test_byram_regime(self):
        plume = byram_convection_number(500.0, 1.0)
        wind = byram_convection_number(500.0, 10.0)
        self.assertGreater(plume, wind)   # low wind => more plume-dominated


class TestNovelND(unittest.TestCase):
    def test_aliasing_identity(self):
        # If fs > 2*f_true, no aliasing: observed == true.
        self.assertAlmostEqual(aliased_frequency(2.0, 30.0), 2.0, places=9)
        # Undersampled: 7 Hz flicker at 10 Hz sampling aliases to 3 Hz.
        self.assertAlmostEqual(aliased_frequency(7.0, 10.0), 3.0, places=9)

    def test_nd2_uncertainty_grows_as_smoke_thickens(self):
        thin = nd2_transmittance_temperature(L_obs=5e4, tau_s=0.8, T_smoke_K=400.0)
        thick = nd2_transmittance_temperature(L_obs=5e4, tau_s=0.05, T_smoke_K=400.0)
        self.assertGreater(thick.sigma_K, thin.sigma_K)   # fail toward 'uncertain'


class TestFireGateFlagGating(unittest.TestCase):
    def test_classC_off_by_default(self):
        fi = FireInputs(detector_conf=0.8, nd3_terms=[(1.0, 1.0, 1.0)])
        res = fire_gate(fi, Config())            # default config: nd3 OFF
        self.assertFalse(res.used_classC)

    def test_classC_on_when_flag_set(self):
        cfg = Config(); cfg.data["firephys"]["nd3"] = True
        fi = FireInputs(detector_conf=0.8, nd3_terms=[(1.0, 1.0, 2.0)])
        res = fire_gate(fi, cfg)
        self.assertTrue(res.used_classC)

    def test_wind_regime_lowers_consistency(self):
        calm = fire_gate(FireInputs(detector_conf=0.9, Q_c_kW_per_m=500.0, wind_U_ms=1.0))
        windy = fire_gate(FireInputs(detector_conf=0.9, Q_c_kW_per_m=500.0, wind_U_ms=12.0))
        self.assertGreater(calm.consistency, windy.consistency)


if __name__ == "__main__":
    unittest.main()
