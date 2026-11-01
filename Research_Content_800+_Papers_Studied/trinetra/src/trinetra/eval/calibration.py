"""eval.calibration — calibration metrics + recalibrators (ECE/MCE, reliability curve, isotonic, Platt).

An honest alarm system must report HOW WELL its probabilities are calibrated, not just discrimination
(AUC). A model that says "0.9" should be right ~90% of the time. We provide:
  - expected / maximum calibration error (ECE/MCE) and a reliability curve,
  - isotonic regression (PAV, pure numpy) — the nonparametric recalibrator,
  - Platt scaling (1-D logistic) — the parametric recalibrator for small calibration sets,
  - Brier score + its calibration/refinement decomposition.
These feed the ReportGuard so a deployment can require a calibration bound alongside the Value Score (R16).
"""
from __future__ import annotations

import numpy as np


def reliability_curve(probs, y_true, n_bins: int = 10):
    """Return (bin_conf, bin_acc, bin_count) over `n_bins` equal-width probability bins."""
    p = np.asarray(probs, float); y = np.asarray(y_true, float)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    conf, acc, cnt = [], [], []
    for i in range(n_bins):
        lo, hi = edges[i], edges[i + 1]
        m = (p >= lo) & (p < hi if i < n_bins - 1 else p <= hi)
        cnt.append(int(m.sum()))
        conf.append(float(p[m].mean()) if m.any() else np.nan)
        acc.append(float(y[m].mean()) if m.any() else np.nan)
    return np.array(conf), np.array(acc), np.array(cnt)


def expected_calibration_error(probs, y_true, n_bins: int = 10) -> float:
    """ECE = sum_bin (n_bin/N) * |acc_bin - conf_bin|."""
    conf, acc, cnt = reliability_curve(probs, y_true, n_bins)
    n = np.sum(cnt)
    if n == 0:
        return 0.0
    mask = cnt > 0
    return float(np.sum(cnt[mask] / n * np.abs(acc[mask] - conf[mask])))


def maximum_calibration_error(probs, y_true, n_bins: int = 10) -> float:
    """MCE = max_bin |acc_bin - conf_bin| over non-empty bins."""
    conf, acc, cnt = reliability_curve(probs, y_true, n_bins)
    mask = cnt > 0
    return float(np.max(np.abs(acc[mask] - conf[mask]))) if mask.any() else 0.0


def brier_decomposition(probs, y_true, n_bins: int = 10) -> dict:
    """Murphy decomposition: Brier = reliability - resolution + uncertainty."""
    p = np.asarray(probs, float); y = np.asarray(y_true, float)
    brier = float(np.mean((p - y) ** 2))
    conf, acc, cnt = reliability_curve(p, y, n_bins)
    n = np.sum(cnt); base = float(y.mean()) if len(y) else 0.0
    mask = cnt > 0
    reliability = float(np.sum(cnt[mask] / n * (conf[mask] - acc[mask]) ** 2)) if n else 0.0
    resolution = float(np.sum(cnt[mask] / n * (acc[mask] - base) ** 2)) if n else 0.0
    uncertainty = base * (1 - base)
    return {"brier": brier, "reliability": reliability, "resolution": resolution,
            "uncertainty": uncertainty}


class IsotonicCalibrator:
    """Nonparametric isotonic (monotone) recalibration via Pool-Adjacent-Violators (PAV). Pure numpy."""

    def __init__(self):
        self.x_thresh = None
        self.y_level = None

    def fit(self, probs, y_true) -> "IsotonicCalibrator":
        p = np.asarray(probs, float); y = np.asarray(y_true, float)
        order = np.argsort(p, kind="mergesort")
        x = p[order]; v = y[order].astype(float)
        w = np.ones_like(v)
        # PAV: merge adjacent blocks that violate monotonicity
        vals = list(v); wts = list(w); xs = list(x)
        i = 0
        while i < len(vals) - 1:
            if vals[i] > vals[i + 1]:
                nw = wts[i] + wts[i + 1]
                nv = (vals[i] * wts[i] + vals[i + 1] * wts[i + 1]) / nw
                vals[i:i + 2] = [nv]; wts[i:i + 2] = [nw]; xs[i:i + 2] = [xs[i + 1]]
                if i > 0:
                    i -= 1
            else:
                i += 1
        self.x_thresh = np.array(xs); self.y_level = np.array(vals)
        return self

    def predict(self, probs):
        p = np.asarray(probs, float)
        idx = np.searchsorted(self.x_thresh, p, side="left")
        idx = np.clip(idx, 0, len(self.y_level) - 1)
        return self.y_level[idx]


class PlattCalibrator:
    """Parametric 1-D logistic recalibration: sigmoid(a*logit(p)+b). Good for small calibration sets."""

    def __init__(self, iters: int = 200, lr: float = 0.1):
        self.a = 1.0; self.b = 0.0; self.iters = iters; self.lr = lr

    @staticmethod
    def _logit(p, eps=1e-6):
        p = np.clip(np.asarray(p, float), eps, 1 - eps)
        return np.log(p / (1 - p))

    def fit(self, probs, y_true) -> "PlattCalibrator":
        z = self._logit(probs); y = np.asarray(y_true, float)
        for _ in range(self.iters):
            s = 1.0 / (1.0 + np.exp(-(self.a * z + self.b)))
            ga = float(np.mean((s - y) * z)); gb = float(np.mean(s - y))
            self.a -= self.lr * ga; self.b -= self.lr * gb
        return self

    def predict(self, probs):
        z = self._logit(probs)
        return 1.0 / (1.0 + np.exp(-(self.a * z + self.b)))
