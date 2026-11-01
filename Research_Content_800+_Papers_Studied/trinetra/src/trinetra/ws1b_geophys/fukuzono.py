"""ws1b_geophys.fukuzono — inverse-velocity failure-time forecast with UNCERTAINTY (Class A/B). M1.

Fukuzono/Voight:  1/v = A*(alpha-1)*(t_f - t).
  alpha = 2  => 1/v LINEAR in t ; t_f = x-intercept.
  alpha != 2 => v^(1-alpha) linear in t (regime flag).

Upgrades over a bare OLS intercept:
  - RECENCY-WEIGHTED least squares (exponential half-life): the latest creep points — which dominate an
    imminent failure — are weighted up, as recommended in operational inverse-velocity practice.
  - PREDICTION INTERVAL on t_f via the regression covariance + delta method (inverse-prediction CI). An
    operator gets `t_f in [low, high]`, not a false point certainty — essential for an advisory call (R19).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class FukuzonoFit:
    t_failure: float          # forecast failure time (same units as input t)
    alpha: float
    slope: float
    r2: float                 # weighted linear fit quality on the linearized variable
    regime_note: str
    t_failure_low: float = float("nan")    # prediction-interval lower bound on t_f
    t_failure_high: float = float("nan")   # prediction-interval upper bound on t_f
    se_t_failure: float = float("nan")      # standard error of t_f (delta method)


def _wls(x, y, w):
    """Weighted least squares y ~ m x + b. Returns m, b, r2_w, and the 2x2 covariance of (m, b)."""
    x = np.asarray(x, float); y = np.asarray(y, float); w = np.asarray(w, float)
    W = np.diag(w)
    X = np.vstack([x, np.ones_like(x)]).T          # columns: [slope, intercept]
    XtW = X.T @ W
    cov_beta_unit = np.linalg.inv(XtW @ X)          # (X^T W X)^-1
    beta = cov_beta_unit @ (XtW @ y)
    m, b = float(beta[0]), float(beta[1])
    yhat = m * x + b
    resid = y - yhat
    dof = max(len(x) - 2, 1)
    sigma2 = float((w * resid ** 2).sum() / dof)    # weighted residual variance
    cov_beta = sigma2 * cov_beta_unit               # Cov([m, b])
    wmean = float((w * y).sum() / w.sum())
    ss_res = float((w * resid ** 2).sum())
    ss_tot = float((w * (y - wmean) ** 2).sum()) or 1e-12
    return m, b, 1.0 - ss_res / ss_tot, cov_beta


def _recency_weights(t, halflife):
    t = np.asarray(t, float)
    if halflife is None or halflife <= 0:
        return np.ones_like(t)
    return np.power(0.5, (t.max() - t) / halflife)   # 1 at the latest sample, decaying backward


def inverse_velocity_fit(times, velocities, alpha: float = 2.0, *, weights=None,
                         recency_halflife: float | None = None, z: float = 1.96) -> FukuzonoFit:
    """Fit the linearized inverse-velocity relation and forecast t_f with a prediction interval.

    weights          : explicit per-sample weights (overrides recency).
    recency_halflife : exponential half-life (in t-units) up-weighting recent points.
    z                : normal quantile for the interval (1.96 ~ 95%).
    """
    t = np.asarray(times, float)
    v = np.asarray(velocities, float)
    if np.any(v <= 0):
        raise ValueError("velocities must be positive")
    y = (1.0 / v) if abs(alpha - 2.0) < 1e-9 else np.power(v, 1.0 - alpha)
    note = "alpha=2: 1/v linear" if abs(alpha - 2.0) < 1e-9 else f"alpha={alpha}: v^(1-alpha) linear"

    w = np.asarray(weights, float) if weights is not None else _recency_weights(t, recency_halflife)
    m, b, r2, cov = _wls(t, y, w)

    if abs(m) < 1e-12:
        return FukuzonoFit(float("inf"), alpha, m, r2, note)
    t_f = -b / m
    # delta method: t_f = -b/m ; d/db = -1/m, d/dm = b/m^2 = -t_f/m
    g = np.array([-t_f / m, -1.0 / m])              # gradient wrt (m, b)
    var_tf = float(g @ cov @ g)
    se = float(np.sqrt(max(var_tf, 0.0)))
    return FukuzonoFit(t_failure=float(t_f), alpha=alpha, slope=m, r2=r2, regime_note=note,
                       t_failure_low=float(t_f - z * se), t_failure_high=float(t_f + z * se),
                       se_t_failure=se)
