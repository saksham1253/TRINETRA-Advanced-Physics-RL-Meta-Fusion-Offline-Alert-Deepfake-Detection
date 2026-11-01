"""Independent BASELINE for the fire classifier (GAP G-06): colour-histogram + numpy logistic regression,
same group folds as the CNN. The CNN's own admission gate only compares against a logistic fit on the CNN's
own score; this gives a model-independent bar the CNN must clearly beat. CPU only, minutes.

Run: python kaggle/baseline_colorhist.py --data /kaggle/working/fire.npz --out /kaggle/working [--target any]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from trinetra.eval import spatial_block_kfold, LogisticNumpy, value_score, expected_calibration_error  # noqa: E402
from trinetra.deep.oof_utils import save_oof                                                         # noqa: E402


def features(X, bins=8):
    """Per-image RGB histograms + simple 'fire colour' stats (R>G>B fraction, brightness)."""
    if X.ndim == 5:
        X = X[:, X.shape[1] // 2]
    N = len(X); F = []
    for i in range(N):
        img = X[i]
        h = [np.histogram(img[c], bins=bins, range=(0, 1))[0] / img[c].size for c in range(3)]
        r, g, b = img[0], img[1], img[2]
        firey = ((r > g) & (g > b) & (r > 0.5)).mean()
        F.append(np.concatenate(h + [[firey, img.mean(), img.std()]]))
    F = np.asarray(F, float)
    return (F - F.mean(0)) / (F.std(0) + 1e-9)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True); ap.add_argument("--out", default="/kaggle/working")
    ap.add_argument("--target", default="fire", choices=["fire", "any"])
    ap.add_argument("--folds", type=int, default=5); ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    d = np.load(a.data, allow_pickle=True)
    Y = d["labels"]; y = ((Y.max(1) if a.target == "any" else Y[:, 0]) if Y.ndim > 1 else Y).astype(int)
    blk = d["block"].astype(str); Xf = features(d["images"])
    p = np.full(len(y), np.nan); fold = np.full(len(y), -1)
    for k, (tr, va) in enumerate(spatial_block_kfold(blk, k=a.folds, seed=a.seed)):
        tr, va = np.asarray(tr), np.asarray(va)
        p[va] = LogisticNumpy(seed=a.seed).fit(Xf[tr], y[tr]).predict_proba(Xf[va]); fold[va] = k
    meta = save_oof(os.path.join(a.out, f"colorhist_s{a.seed}_oof.npz"), name="colorhist", seed=a.seed, folds=a.folds,
             prob=p, y=y, block=blk, fold_of_row=fold, extra_meta={"data": a.data, "target": a.target})
    m = ~np.isnan(p)
    rep = {"name": "colorhist_baseline", "seed": a.seed, "value_score": value_score(y[m], p[m], 5.0, 100.0)["value_score"],
           "ece": expected_calibration_error(p[m], y[m]), "n": int(m.sum()),
           "note": "BASELINE. The CNN must beat this beyond seed spread before any claim.", **meta["metrics"]}
    json.dump(rep, open(os.path.join(a.out, f"colorhist_s{a.seed}_report.json"), "w"), indent=2)
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()
