"""eval.baselines — mandatory baselines a model must BEAT before any performance claim (Rule 16, G2).

All numpy/stdlib (no sklearn). A new model is only admitted if it shows a 'real win' (eval.real_win) over
EVERY one of these on SPATIAL-CV folds with a cost-aware score. Baselines:
  - base_rate_climatology : constant = base rate
  - persistence           : predict the previous time step's label
  - physics_rule          : FS<1 (or threshold feature) -> alarm (domain rule, no learning)
  - logistic_numpy        : L2 logistic regression trained by gradient descent (learned baseline)
"""
from __future__ import annotations

import numpy as np


def base_rate_climatology(y_train, n_test: int):
    """Predict the training base rate for every test sample."""
    s = float(np.asarray(y_train, float).mean()) if len(y_train) else 0.0
    return np.full(n_test, s, dtype=float)


def persistence(prev_labels):
    """Predict the previous observed label as a probability (0/1)."""
    return np.asarray(prev_labels, float)


def physics_rule(feature, threshold: float, invert: bool = False):
    """Alarm probability from a hard domain rule, e.g. FS<1 => alarm (invert for 'below threshold')."""
    f = np.asarray(feature, float)
    hit = (f < threshold) if invert else (f > threshold)
    return hit.astype(float)


class LogisticNumpy:
    """Minimal L2-regularized logistic regression (gradient descent). Standardizes features internally."""

    def __init__(self, l2: float = 1e-3, lr: float = 0.1, epochs: int = 500, seed: int = 0):
        self.l2 = l2; self.lr = lr; self.epochs = epochs; self.seed = seed
        self.w = None; self.b = 0.0; self.mu = None; self.sd = None

    def fit(self, X, y):
        X = np.asarray(X, float); y = np.asarray(y, float)
        self.mu = X.mean(0); self.sd = X.std(0) + 1e-8
        Xs = (X - self.mu) / self.sd
        n, d = Xs.shape
        rng = np.random.default_rng(self.seed)
        self.w = rng.normal(0, 0.01, d); self.b = 0.0
        for _ in range(self.epochs):
            z = Xs @ self.w + self.b
            p = 1.0 / (1.0 + np.exp(-z))
            g = p - y
            self.w -= self.lr * (Xs.T @ g / n + self.l2 * self.w)
            self.b -= self.lr * float(g.mean())
        return self

    def predict_proba(self, X):
        Xs = (np.asarray(X, float) - self.mu) / self.sd
        return 1.0 / (1.0 + np.exp(-(Xs @ self.w + self.b)))
