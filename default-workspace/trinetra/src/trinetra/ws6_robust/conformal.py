"""ws6_robust.conformal — split conformal prediction + weighted CP for covariate shift (gate G3/M4).

DESIGN/LLD.md §6. We provide (a) standard split-conformal with finite-sample marginal coverage, (b) a
weighted variant (WCPS) that reweights calibration residuals by a train->test likelihood ratio to keep
coverage honest under covariate shift. We report the REALIZED coverage; we never call the bound a
"guarantee" (it holds only under exchangeability / correct weights, and is voided under concept drift —
see drift_monitor).
"""
from __future__ import annotations

import numpy as np


def conformal_quantile(cal_scores, alpha: float = 0.1) -> float:
    """Finite-sample adjusted (1-alpha) quantile of calibration nonconformity scores."""
    s = np.sort(np.asarray(cal_scores, float))
    n = len(s)
    if n == 0:
        return float("inf")
    k = int(np.ceil((n + 1) * (1 - alpha))) - 1
    k = min(max(k, 0), n - 1)
    return float(s[k])


def regression_interval(point_pred, cal_residuals, alpha: float = 0.1):
    """Symmetric split-conformal interval half-width q; returns (lo, hi) arrays for point_pred."""
    q = conformal_quantile(np.abs(cal_residuals), alpha)
    p = np.asarray(point_pred, float)
    return p - q, p + q


def weighted_conformal_quantile(cal_scores, cal_weights, alpha: float = 0.1,
                                test_weight: float = 1.0) -> float:
    """WCPS: weighted (1-alpha) quantile of calibration scores for a single test point.

    cal_weights ~ likelihood ratio p_test(x)/p_train(x). Includes the test point's own weight mass at +inf
    (standard weighted-CP construction).
    """
    s = np.asarray(cal_scores, float); w = np.asarray(cal_weights, float)
    order = np.argsort(s)
    s = s[order]; w = w[order]
    total = w.sum() + test_weight
    cum = np.cumsum(w) / total
    idx = np.searchsorted(cum, 1 - alpha, side="left")
    if idx >= len(s):
        return float("inf")
    return float(s[idx])


def classification_set(class_scores: dict, q: float) -> list:
    """Prediction set = {label : nonconformity_score(label) <= q}. class_scores maps label->score."""
    return [lbl for lbl, sc in class_scores.items() if sc <= q]


def empirical_coverage(lo, hi, y_true) -> float:
    """Realized marginal coverage of intervals [lo,hi] over y_true (for honesty reporting)."""
    lo = np.asarray(lo, float); hi = np.asarray(hi, float); y = np.asarray(y_true, float)
    return float(np.mean((y >= lo) & (y <= hi)))


class AdaptiveConformal:
    """Adaptive Conformal Inference (Gibbs & Candes 2021) — keeps LONG-RUN coverage under arbitrary drift.

    Concept drift voids static split-CP (see module docstring). ACI fixes this online: after each outcome
    it nudges the working miss-rate alpha_t toward the target using the realized error, so the time-average
    coverage -> 1-alpha regardless of distribution shift. gamma is the learning rate.

        alpha_{t+1} = clip( alpha_t + gamma * (alpha_target - err_t) , 0, 1 )
        err_t = 1 if y_t fell OUTSIDE the interval built with alpha_t, else 0.

    This is a genuine robustness guarantee TYPE (long-run, not per-step), and we report it as such."""

    def __init__(self, alpha_target: float = 0.1, gamma: float = 0.02):
        self.alpha_target = float(alpha_target)
        self.gamma = float(gamma)
        self.alpha_t = float(alpha_target)
        self._errs: list[int] = []

    def quantile(self, cal_scores) -> float:
        """Current (1-alpha_t) calibration quantile with the adapted alpha_t."""
        return conformal_quantile(cal_scores, min(max(self.alpha_t, 1e-6), 1.0))

    def step(self, covered: bool) -> float:
        """Record whether the just-issued interval covered the truth; update and return the next alpha."""
        err = 0 if covered else 1
        self._errs.append(err)
        self.alpha_t = float(np.clip(self.alpha_t + self.gamma * (self.alpha_target - err), 0.0, 1.0))
        return self.alpha_t

    @property
    def realized_coverage(self) -> float:
        return float(1.0 - np.mean(self._errs)) if self._errs else float("nan")


class MondrianConformal:
    """Mondrian / class-conditional conformal: a SEPARATE calibration quantile per group (e.g. per hazard).

    Marginal coverage can hide severe miscoverage for a rare but critical class (e.g. GLOF). Mondrian-CP
    conditions on a group label so EACH group gets its own (1-alpha) coverage — the honest guarantee for a
    multi-hazard safety system where every hazard must be covered, not just the average."""

    def __init__(self, alpha: float = 0.1):
        self.alpha = float(alpha)
        self._q: dict = {}

    def fit(self, groups, cal_scores) -> "MondrianConformal":
        groups = np.asarray(groups); scores = np.asarray(cal_scores, float)
        for g in np.unique(groups):
            self._q[g] = conformal_quantile(scores[groups == g], self.alpha)
        return self

    def quantile(self, group):
        """Group-specific quantile; falls back to the max (most conservative) for an unseen group."""
        if group in self._q:
            return self._q[group]
        return max(self._q.values()) if self._q else float("inf")

    def group_coverage(self, groups, lo, hi, y_true) -> dict:
        """Per-group realized coverage, for the honesty report."""
        groups = np.asarray(groups); lo = np.asarray(lo, float); hi = np.asarray(hi, float)
        y = np.asarray(y_true, float)
        out = {}
        for g in np.unique(groups):
            mask = groups == g
            out[g] = float(np.mean((y[mask] >= lo[mask]) & (y[mask] <= hi[mask])))
        return out


def conformal_risk_threshold(cal_scores, cal_labels, target_risk: float = 0.05,
                             n_grid: int = 200) -> float:
    """Conformal Risk Control (Angelopoulos et al. 2022) for a MISS-rate loss.

    Picks the LOWEST alarm threshold lambda such that the finite-sample-corrected empirical miss-rate on
    calibration data stays <= target_risk. Loss_i(lambda) = 1 if (event AND score < lambda) else 0 — i.e.
    a true event that would NOT be alarmed at lambda. The RCPS/CRC bound adds the (B/n) slack so the
    guarantee is conservative. Returns lambda_hat; alarm when risk_score >= lambda_hat controls misses.

    This replaces an ad-hoc level multiplier with a threshold that provably bounds the miss-risk — the
    quantity that actually matters for a life-safety alarm."""
    s = np.asarray(cal_scores, float); y = np.asarray(cal_labels, int)
    n = len(s)
    if n == 0:
        return 0.0
    B = 1.0                                           # loss is bounded in [0,1]
    corrected = target_risk - B / (n + 1)             # finite-sample slack (conservative)
    if corrected <= 0:
        return 0.0                                    # cannot certify -> alarm on everything (fail-safe)
    los, his = s.min(), s.max()
    grid = np.linspace(los, his, n_grid)
    best = los
    for lam in grid:                                  # lower lambda = more alarms = fewer misses
        misses = np.mean((y == 1) & (s < lam))
        if misses <= corrected:
            best = lam
        else:
            break
    return float(best)
