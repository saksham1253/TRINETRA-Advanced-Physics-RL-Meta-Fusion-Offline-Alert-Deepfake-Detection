"""Interface/behavior tests for anomaly, CCTV validator, EO encoder, RL/OPE, deepfake (M2/M3/M5/M9)."""
import unittest

import numpy as np

from trinetra.ws8_anomaly import anomaly_ensemble, forecast_residual_score, iforest_lite_score
from trinetra.ws4_cctv import TemporalValidator, EdgeDetector
from trinetra.ws1b_eo import EOEncoder
from trinetra.ws2_deepfake import authenticity_expert, DeepfakeDetector, heuristic_authenticity
from trinetra.ws5_fusion_rl import RuleBaselinePolicy, OfflineRLPolicy, ope_admission, ope_feasible
from trinetra.common.exceptions import MissingDependency


class TestAnomaly(unittest.TestCase):
    def test_outliers_score_higher(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(200, 3))
        X[-5:] += 8.0                                   # inject outliers
        s = anomaly_ensemble(X)
        self.assertGreater(s[-5:].mean(), s[:-5].mean())

    def test_forecast_residual_spikes_on_jump(self):
        x = np.concatenate([np.zeros(30), [10.0], np.zeros(9)])
        z = forecast_residual_score(x)
        self.assertEqual(int(np.argmax(z)), 30)         # residual spikes at the jump sample (x[30]=10)


class TestCCTVValidator(unittest.TestCase):
    def test_requires_persistence(self):
        v = TemporalValidator(window=5, min_frames=3, conf_thr=0.5)
        self.assertFalse(v.update(0.9).confirmed)       # 1 frame
        self.assertFalse(v.update(0.9).confirmed)       # 2 frames
        self.assertTrue(v.update(0.9).confirmed)        # 3 frames -> confirmed

    def test_single_glint_rejected(self):
        v = TemporalValidator(window=5, min_frames=3, conf_thr=0.5)
        for c in [0.9, 0.0, 0.0, 0.0]:
            ev = v.update(c)
        self.assertFalse(ev.confirmed)

    def test_detector_requires_torch(self):
        with self.assertRaises(MissingDependency):
            EdgeDetector().detect(frame=None)


class TestEO(unittest.TestCase):
    def test_real_encoder_requires_torch(self):
        with self.assertRaises(MissingDependency):
            EOEncoder().embed(patch=np.zeros((8, 8)))

    def test_fallback_is_deterministic_unit_norm(self):
        enc = EOEncoder(dim=32)
        a = enc.hashing_fallback(np.arange(16.0))
        b = enc.hashing_fallback(np.arange(16.0))
        self.assertTrue(np.allclose(a, b))
        self.assertAlmostEqual(float(np.linalg.norm(a)), 1.0, places=6)


class TestRLOPE(unittest.TestCase):
    def test_rule_baseline(self):
        pol = RuleBaselinePolicy(threshold=0.05)
        self.assertEqual(pol.act(0.9), 1)
        self.assertEqual(pol.act(0.01), 0)

    def test_learned_requires_dep(self):
        with self.assertRaises(MissingDependency):
            OfflineRLPolicy().fit(dataset=None)

    def test_positivity_gate_blocks(self):
        # a logging policy that almost never explores one action => OPE infeasible
        self.assertFalse(ope_feasible(np.full(100, 1e-4)))
        self.assertTrue(ope_feasible(np.full(100, 0.5)))

    def test_admission_requires_feasible_and_better(self):
        rng = np.random.default_rng(0)
        b = np.full(200, 0.5)
        rewards = rng.normal(1.0, 0.1, 200)
        v = ope_admission(b, target_probs=np.full(200, 0.5), rewards=rewards,
                          baseline_rewards=rewards - 0.5)
        self.assertTrue(v.feasible)
        self.assertTrue(v.deploy_learned)


class TestDeepfake(unittest.TestCase):
    def test_low_trust_reliability(self):
        e = authenticity_expert({"noise_consistency": 0.2})
        self.assertLessEqual(e.r, 0.4)                  # never high-trust (Rule 19)

    def test_fake_cues_raise_p_fake(self):
        auth_hi = authenticity_expert({"noise_consistency": 0.9, "metadata_intact": 1,
                                       "compression_grade": 0.9, "temporal_coherence": 0.9})
        auth_lo = authenticity_expert({"noise_consistency": 0.1, "metadata_intact": 0,
                                       "compression_grade": 0.1, "temporal_coherence": 0.1})
        self.assertLess(auth_hi.p, auth_lo.p)           # less authentic => higher p_fake

    def test_detector_requires_torch(self):
        with self.assertRaises(MissingDependency):
            DeepfakeDetector().score(media=None)


if __name__ == "__main__":
    unittest.main()
