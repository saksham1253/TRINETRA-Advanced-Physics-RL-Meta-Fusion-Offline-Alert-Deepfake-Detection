"""M0 eval-harness tests (gate G2): spatial-CV integrity, cost-loss score, real-win, honesty guard."""
import unittest

import numpy as np

from trinetra.eval import (
    spatial_block_kfold, temporal_split, assert_no_time_leak,
    p_star, value_score, alarms_from_prob,
    base_rate_climatology, LogisticNumpy, real_win,
    ReportGuard, ReportGuardError,
)
from trinetra.common.exceptions import LeakageError


class TestSplits(unittest.TestCase):
    def test_blocks_never_span_train_and_test(self):
        blocks = np.array([f"z{i%6}" for i in range(120)])
        for train, test in spatial_block_kfold(blocks, k=3, seed=1):
            train_blocks = set(blocks[train]); test_blocks = set(blocks[test])
            self.assertEqual(train_blocks & test_blocks, set())   # no spatial leakage

    def test_temporal_no_future_in_train(self):
        t = np.arange(100)
        tr, te = temporal_split(t, 0.7)
        self.assertLess(t[tr].max(), t[te].min())

    def test_leak_guard(self):
        with self.assertRaises(LeakageError):
            assert_no_time_leak([1, 2, 11], decision_time=10)


class TestValueScore(unittest.TestCase):
    def test_p_star(self):
        self.assertAlmostEqual(p_star(5.0, 100.0), 5.0 / 105.0, places=9)

    def test_perfect_forecast_scores_one(self):
        y = np.array([0, 1, 0, 1, 1, 0])
        res = value_score(y, p_pred=y.astype(float), C_FA=5, C_miss=100)
        self.assertAlmostEqual(res["value_score"], 1.0, places=9)   # zero cost => VS=1

    def test_useless_forecast_not_positive(self):
        rng = np.random.default_rng(0)
        y = (rng.random(400) < 0.1).astype(int)
        res = value_score(y, p_pred=np.full(400, 0.1), C_FA=5, C_miss=100)
        self.assertLessEqual(res["value_score"], 0.0 + 1e-9)        # constant ~ climatology


class TestRealWin(unittest.TestCase):
    def test_better_model_wins_worse_does_not(self):
        rng = np.random.default_rng(0)
        n = 600
        blocks = np.array([f"z{i%20}" for i in range(n)])
        signal = rng.random(n)
        y = (signal > 0.8).astype(int)                    # event when signal high
        p_good = signal                                   # informative
        p_bad = rng.random(n)                             # noise
        good = real_win(y, p_good, p_bad, blocks, C_FA=5, C_miss=100, n_boot=500, seed=1)
        bad = real_win(y, p_bad, p_good, blocks, C_FA=5, C_miss=100, n_boot=500, seed=1)
        self.assertTrue(good["real_win"])
        self.assertFalse(bad["real_win"])


class TestReportGuard(unittest.TestCase):
    def test_refuses_without_spatial_cv(self):
        g = ReportGuard(spatial_cv=False)
        with self.assertRaises(ReportGuardError):
            g.headline("value_score", 0.5)

    def test_refuses_without_baselines(self):
        g = ReportGuard(spatial_cv=True)
        with self.assertRaises(ReportGuardError):
            g.headline("value_score", 0.5)

    def test_not_admitted_blocks_claim(self):
        g = ReportGuard(spatial_cv=True)
        g.add_baseline_verdict("persistence", {"real_win": False, "ci_low": -0.1})
        self.assertFalse(g.admit())
        with self.assertRaises(ReportGuardError):
            g.headline("value_score", 0.5)

    def test_admitted_allows_claim(self):
        g = ReportGuard(spatial_cv=True)
        g.add_baseline_verdict("persistence", {"real_win": True, "ci_low": 0.2})
        g.add_baseline_verdict("logistic", {"real_win": True, "ci_low": 0.1})
        self.assertTrue(g.admit())
        self.assertIn("value_score", g.headline("value_score", 0.42))


class TestLogistic(unittest.TestCase):
    def test_learns_separable(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(300, 2))
        y = (X[:, 0] + X[:, 1] > 0).astype(int)
        clf = LogisticNumpy(epochs=800).fit(X, y)
        acc = ((clf.predict_proba(X) > 0.5).astype(int) == y).mean()
        self.assertGreater(acc, 0.9)


if __name__ == "__main__":
    unittest.main()
