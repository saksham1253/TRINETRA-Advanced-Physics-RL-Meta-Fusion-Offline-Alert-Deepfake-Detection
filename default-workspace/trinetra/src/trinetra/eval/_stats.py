"""eval._stats — bootstrap statistics helpers: normal cdf/ppf, BCa intervals, stationary bootstrap.

Pure numpy/math (no scipy). Used to give the admission tests sharper, better-calibrated confidence
intervals than plain percentile bootstrap:
  - BCa (bias-corrected & accelerated, Efron 1987): corrects for bias and skew in the bootstrap
    distribution; its coverage error is O(1/n) vs O(1/sqrt(n)) for the percentile method.
  - stationary bootstrap (Politis & Romano 1994): geometric-length blocks for autocorrelated TIME series,
    so temporal dependence is not destroyed by i.i.d. resampling.
"""
from __future__ import annotations

import math

import numpy as np


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_ppf(p: float) -> float:
    """Inverse standard-normal CDF via Acklam's rational approximation (|err| < 1.2e-9)."""
    if p <= 0.0:
        return -math.inf
    if p >= 1.0:
        return math.inf
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


def bca_interval(boot, theta_hat: float, jackknife, alpha: float = 0.05):
    """BCa confidence interval from a bootstrap sample `boot`, the observed statistic `theta_hat`, and
    leave-one-out jackknife statistics. Falls back to percentile if acceleration is undefined."""
    boot = np.asarray(boot, float); jk = np.asarray(jackknife, float)
    prop = float(np.mean(boot < theta_hat))
    prop = min(max(prop, 1e-6), 1 - 1e-6)
    z0 = norm_ppf(prop)                                     # bias correction
    jbar = jk.mean()
    num = float(np.sum((jbar - jk) ** 3))
    den = 6.0 * (float(np.sum((jbar - jk) ** 2)) ** 1.5)
    a = num / den if den != 0 else 0.0                      # acceleration (skew)
    zlo, zhi = norm_ppf(alpha / 2), norm_ppf(1 - alpha / 2)

    def adj(z):
        denom = 1 - a * (z0 + z)
        return norm_cdf(z0 + (z0 + z) / denom) if denom != 0 else norm_cdf(z0 + z)

    plo, phi = adj(zlo), adj(zhi)
    return float(np.quantile(boot, plo)), float(np.quantile(boot, phi))


def stationary_bootstrap_indices(n: int, avg_block: float, rng) -> np.ndarray:
    """One stationary-bootstrap resample of indices 0..n-1 with geometric block lengths (mean avg_block)."""
    if n == 0:
        return np.empty(0, int)
    p = 1.0 / max(avg_block, 1.0)
    out = []
    i = rng.integers(0, n)
    while len(out) < n:
        out.append(i)
        if rng.random() < p:
            i = rng.integers(0, n)                          # start a new block
        else:
            i = (i + 1) % n                                 # extend current block (wrap)
    return np.array(out[:n], int)
