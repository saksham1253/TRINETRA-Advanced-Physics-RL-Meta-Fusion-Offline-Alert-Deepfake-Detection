"""ws5_fusion_rl.rl — offline-RL alarm policy: rule baseline + OPE admission gate (M5, Rule 19 advisory).

DESIGN/LLD.md §5. The learned offline-RL policy (one-step / TD3+BC / CQL / IQL) requires d3rlpy+torch and
is interface-only here (raises MissingDependency). What IS implemented in numpy:
  - RuleBaselinePolicy : the fixed-threshold policy a learned policy must BEAT.
  - OPE: weighted importance sampling value + a positivity/ESS feasibility gate.
A learned policy is deployed ONLY if its OPE lower bound >= the rule baseline AND positivity holds
(FM-22 gate). Otherwise the baseline is used. The policy is ADVISORY; the shield still bounds it.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..common.exceptions import MissingDependency


class RuleBaselinePolicy:
    """Alarm iff the fused risk exceeds a fixed threshold (the honest fallback / OPE comparator)."""

    def __init__(self, threshold: float = 0.0476):
        self.threshold = threshold

    def act(self, risk: float) -> int:
        return int(risk >= self.threshold)


class OfflineRLPolicy:
    """Interface for a learned offline-RL policy. Training/inference needs d3rlpy+torch -> stub raises."""

    def __init__(self, algo: str = "one_step"):
        self.algo = algo

    def fit(self, dataset):
        raise MissingDependency(
            f"offline-RL algo {self.algo!r} needs d3rlpy+torch (not installed). "
            "Until trained+OPE-admitted, the system uses RuleBaselinePolicy (Rule 19 fail-safe)."
        )


def wis_value(behavior_probs, target_probs, rewards):
    """Weighted importance sampling value estimate for one-step (contextual-bandit) OPE.

    Returns (value, effective_sample_size). Clips ratios for stability."""
    b = np.asarray(behavior_probs, float); t = np.asarray(target_probs, float)
    r = np.asarray(rewards, float)
    w = np.clip(t / np.clip(b, 1e-6, None), 0, 1e3)
    sw = w.sum()
    if sw <= 0:
        return 0.0, 0.0
    value = float((w * r).sum() / sw)
    ess = float((sw ** 2) / (np.sum(w ** 2) + 1e-12))
    return value, ess


def ope_feasible(behavior_probs, min_prob: float = 1e-2, min_ess_frac: float = 0.1) -> bool:
    """Positivity + effective-sample-size gate. OPE is untrustworthy if the logging policy almost never
    took some actions (positivity violation) or the ESS collapses."""
    b = np.asarray(behavior_probs, float)
    if b.size == 0 or b.min() < min_prob:
        return False
    w = 1.0 / np.clip(b, min_prob, None)
    ess = (w.sum() ** 2) / (np.sum(w ** 2) + 1e-12)
    return bool(ess >= min_ess_frac * len(b))


@dataclass
class OPEVerdict:
    value_target: float
    value_baseline: float
    ess: float
    feasible: bool
    deploy_learned: bool


def ope_admission(behavior_probs, target_probs, rewards, baseline_rewards) -> OPEVerdict:
    """Admit the learned policy only if OPE is feasible AND its estimated value >= the baseline's."""
    v_t, ess = wis_value(behavior_probs, target_probs, rewards)
    v_b = float(np.mean(baseline_rewards))
    feasible = ope_feasible(behavior_probs)
    return OPEVerdict(value_target=v_t, value_baseline=v_b, ess=ess,
                      feasible=feasible, deploy_learned=bool(feasible and v_t >= v_b))
