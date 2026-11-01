"""ws8_anomaly â€” unsupervised anomaly ensemble (Class data-driven, M2). Pure numpy.

Three cheap, transparent detectors whose normalized scores are averaged:
  - forecast_residual : AR(1) one-step forecast; standardized residual magnitude
  - iforest_lite      : isolation-style mean split-depth over random axis-aligned cuts
  - mahalanobis_lite  : robust distance to the training centroid in standardized space
Heavy deep detectors (Deep SVDD, autoencoders) require torch and live behind the same interface; this
numpy ensemble is the always-available baseline, admitted only via eval/ (Rule 16).
"""
from __future__ import annotations

import numpy as np


def forecast_residual_score(series, phi: float | None = None):
    """AR(1) one-step residual z-scores. If phi is None it is estimated by least squares."""
    x = np.asarray(series, float)
    if len(x) < 3:
        return np.zeros_like(x)
    x0, x1 = x[:-1], x[1:]
    if phi is None:
        phi = float(np.dot(x0, x1) / (np.dot(x0, x0) + 1e-9))
    pred = phi * x0
    resid = x1 - pred
    z = np.abs(resid - resid.mean()) / (resid.std() + 1e-9)
    return np.concatenate([[0.0], z])


def iforest_lite_score(X, n_trees: int = 100, sample: int = 64, seed: int = 0):
    """Mean isolation depth over random axis-aligned cuts; shallower isolation => more anomalous."""
    X = np.asarray(X, float)
    n, d = X.shape if X.ndim == 2 else (len(X), 1)
    X = X.reshape(n, d)
    rng = np.random.default_rng(seed)
    depths = np.zeros(n)
    for _ in range(n_trees):
        idx = rng.choice(n, size=min(sample, n), replace=False)
        depths += _tree_depth(X, X[idx], rng, 0, int(np.ceil(np.log2(max(sample, 2)))))
    depths /= n_trees
    s = -depths
    return (s - s.min()) / (np.ptp(s) + 1e-9)


def _tree_depth(X, sub, rng, depth, max_depth):
    out = np.full(len(X), depth, float)
    if depth >= max_depth or len(sub) <= 1:
        return out
    f = rng.integers(0, X.shape[1])
    lo, hi = sub[:, f].min(), sub[:, f].max()
    if hi <= lo:
        return out
    thr = rng.uniform(lo, hi)
    left_mask = X[:, f] < thr
    sub_left = sub[sub[:, f] < thr]; sub_right = sub[sub[:, f] >= thr]
    out[left_mask] = _tree_depth(X[left_mask], sub_left, rng, depth + 1, max_depth)
    out[~left_mask] = _tree_depth(X[~left_mask], sub_right, rng, depth + 1, max_depth)
    return out


def mahalanobis_lite_score(X):
    """Standardized Euclidean distance to the centroid (diagonal covariance approx)."""
    X = np.asarray(X, float)
    X = X.reshape(len(X), -1)
    mu = X.mean(0); sd = X.std(0) + 1e-9
    d = np.sqrt(((X - mu) / sd) ** 2).sum(1) if X.shape[1] else np.zeros(len(X))
    return (d - d.min()) / (np.ptp(d) + 1e-9)


def anomaly_ensemble(X, series=None, weights=(1.0, 1.0, 1.0)):
    """Average of normalized detector scores -> p in [0,1]. series optional (for forecast residual)."""
    X = np.asarray(X, float).reshape(len(X), -1)
    scores = [iforest_lite_score(X), mahalanobis_lite_score(X)]
    w = list(weights[:2])
    if series is not None:
        fr = forecast_residual_score(series)
        fr = (fr - fr.min()) / (np.ptp(fr) + 1e-9)
        scores.append(fr); w.append(weights[2])
    S = np.average(np.vstack(scores), axis=0, weights=w)
    return np.clip(S, 0.0, 1.0)

