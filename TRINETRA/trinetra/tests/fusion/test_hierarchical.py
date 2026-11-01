"""Hierarchical (two-layer) + correlation-aware (BLUE/GLS) fusion tests (M6).

Covers: double-counting fix (redundant sensors don't swamp an independent one), the ρ→1 limit (a redundant
pair -> one effective vote), metadata propagation (uncertainty/consistency/class), the single-decision-
function flow, and Class-C transparency propagation.
"""
import unittest

import numpy as np

from trinetra.common.config import Config
from trinetra.common.types import ExpertOutput, PhysicsClass, Hazard, Level
from trinetra.ws5_fusion_rl import (
    correlation_adjusted_weights, blue_fuse, redundancy_matrix,
    fuse_group, hierarchical_fuse, decide_hierarchical, ShieldSignals,
)


def _eq_experts(ps, sources, cls=PhysicsClass.DATA):
    # equal-quality experts (same u/c/r) so weight differences come ONLY from correlation structure
    return [ExpertOutput(p=p, source=s, u=0.2, c=1.0, r=0.9, cls=cls) for p, s in zip(ps, sources)]


class TestCorrelationWeights(unittest.TestCase):
    def test_independent_matches_precision_weights(self):
        exps = _eq_experts([0.3, 0.6, 0.9], ["a", "b", "c"])
        w = correlation_adjusted_weights(exps, corr=None)   # identity corr
        self.assertAlmostEqual(float(w.sum()), 1.0, places=9)
        self.assertTrue(np.allclose(w, w[0]))               # equal quality + independent => equal weights

    def test_redundant_pair_does_not_double_count(self):
        # a,b are redundant (rho=0.8); c is independent. All equal quality.
        exps = _eq_experts([0.5, 0.5, 0.5], ["a", "b", "c"])
        R = redundancy_matrix(["a", "b", "c"], [{"a", "b"}], rho=0.8)
        w = correlation_adjusted_weights(exps, R)
        wa, wb, wc = w
        self.assertAlmostEqual(wa, wb, places=6)
        self.assertGreater(wc, wa)                          # independent expert out-weighs each redundant one
        self.assertGreater(wc, 1 / 3)                       # and beats the naive equal 1/3 (double-count fixed)

    def test_rho_to_one_pair_becomes_one_vote(self):
        exps = _eq_experts([0.5, 0.5, 0.5], ["a", "b", "c"])
        R = redundancy_matrix(["a", "b", "c"], [{"a", "b"}], rho=0.999)
        w = correlation_adjusted_weights(exps, R)
        pair = w[0] + w[1]
        self.assertAlmostEqual(pair, w[2], places=2)        # pair total ~ one independent vote

    def test_weights_nonnegative(self):
        exps = _eq_experts([0.1, 0.9], ["a", "b"])
        R = redundancy_matrix(["a", "b"], [{"a", "b"}], rho=0.95)
        w = correlation_adjusted_weights(exps, R)
        self.assertTrue((w >= 0).all())                     # safety: no hedging/negative weights


class TestBlueFuse(unittest.TestCase):
    def test_blue_fuse_in_range(self):
        exps = _eq_experts([0.2, 0.8, 0.5], ["a", "b", "c"])
        p = blue_fuse(exps, redundancy_matrix(["a", "b", "c"], [{"a", "b"}], 0.8))
        self.assertTrue(0.2 <= p <= 0.8)


class TestFuseGroup(unittest.TestCase):
    def test_group_reduces_to_single_expert(self):
        g = fuse_group("geo", _eq_experts([0.4, 0.5, 0.6], ["x", "y", "z"]), Config())
        self.assertEqual(g.source, "geo")
        self.assertTrue(0.4 <= g.p <= 0.6)
        self.assertTrue(g.available)

    def test_disagreement_lowers_consistency(self):
        agree = fuse_group("g", _eq_experts([0.5, 0.5, 0.5], ["a", "b", "c"]), Config())
        disagree = fuse_group("g", _eq_experts([0.05, 0.5, 0.95], ["a", "b", "c"]), Config())
        self.assertGreater(agree.c, disagree.c)

    def test_classC_propagates(self):
        exps = _eq_experts([0.3, 0.7], ["a", "b"], cls=PhysicsClass.C)
        g = fuse_group("g", exps, Config())
        self.assertEqual(g.cls, PhysicsClass.C)

    def test_class_precedence_weakest_wins(self):
        exps = [
            ExpertOutput(p=0.3, source="a", u=0.2, cls=PhysicsClass.A),
            ExpertOutput(p=0.4, source="b", u=0.2, cls=PhysicsClass.DATA),
        ]
        self.assertEqual(fuse_group("g", exps, Config()).cls, PhysicsClass.DATA)


class TestHierarchicalDecision(unittest.TestCase):
    def test_end_to_end_through_single_decision_fn(self):
        groups = {
            "geo": _eq_experts([0.2, 0.25, 0.22], ["tilt", "soil1", "soil2"]),
            "fire": _eq_experts([0.05], ["cam"]),
        }
        # geo sensors are mutually redundant (same slope) -> correlation-aware so they don't triple-count
        d = decide_hierarchical(groups, ShieldSignals(FS=0.8), Config(),
                                hazard=Hazard.LANDSLIDE, zone_id="UK-07",
                                redundancy={"geo": [{"tilt", "soil1", "soil2"}]})
        self.assertEqual(len(d.contributions), 2)            # two group-level experts reached the decision
        self.assertIn(d.level.name, {"GREEN", "YELLOW", "ORANGE", "RED"})
        self.assertTrue(d.advisory)

    def test_classC_group_sets_used_classC_on_decision(self):
        groups = {"geo": _eq_experts([0.6, 0.6], ["a", "b"], cls=PhysicsClass.C)}
        d = decide_hierarchical(groups, None, Config(), zone_id="z")
        self.assertTrue(d.used_classC)                       # transparency propagates to the decision

    def test_redundant_group_vs_flat_double_count(self):
        # 3 identical geo alarms vs 1 calm fire. Hierarchical should NOT let geo count as 3 independent.
        groups = {
            "geo": _eq_experts([0.9, 0.9, 0.9], ["a", "b", "c"]),
            "fire": _eq_experts([0.0], ["cam"]),
        }
        g_experts = hierarchical_fuse(groups, Config(),
                                      redundancy={"geo": [{"a", "b", "c"}]})
        geo = [e for e in g_experts if e.source == "geo"][0]
        self.assertAlmostEqual(geo.p, 0.9, places=6)         # group collapses to the shared signal, not amplified


if __name__ == "__main__":
    unittest.main()
