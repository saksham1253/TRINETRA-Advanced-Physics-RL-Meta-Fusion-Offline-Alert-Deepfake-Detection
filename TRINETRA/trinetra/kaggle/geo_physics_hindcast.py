"""Physics hindcast on REAL landslide events (CPU, minutes). Input: geo_events.csv from data_adapters/build_geo.py.

Scores compared (all OOF under spatial-block CV, blocks = --cell-deg grid):
  climatology           base rate
  caine_ratio           Caine (1980) I-D exceedance, repo constants a=14, b=0.39 (Class A, NO fitting)
  dFS (Iverson+FS)      rain-driven drop in factor of safety at the same site (Class A model, assumed soil)
  geo_gate              repo ws1b_geophys.geo_gate noisy-OR (FS + Caine) with BACK-ANALYSED c' (FS_dry = 1.2 per site)
  logit_rain            logistic on antecedent rain sums (DATA baseline)
  logit_physics         logistic on [log Caine ratio, dFS]
  logit_hybrid          logistic on rain + physics features
Verdicts: block-bootstrap 95% CI of ROC-AUC(hybrid) - ROC-AUC(rain baseline); repo eval.real_win (cost-loss at p*).
Case-control design -> base rate is artificial; ROC-AUC/recall@FPR are the honest headline (docs/09e).
Run: python kaggle/geo_physics_hindcast.py --events geo/geo_events.csv --out out/geo
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from trinetra.eval import spatial_block_kfold, LogisticNumpy, real_win, value_score, expected_calibration_error  # noqa: E402
from trinetra.deep.oof_utils import discrimination                                                           # noqa: E402
from trinetra.ws1b_geophys.gate import GeoInputs, geo_gate                                                   # noqa: E402

RAIN = ["rain_1d", "rain_3d", "rain_7d", "rain_15d", "rain_30d", "rain_max3"]


def oof_logit(X, y, blocks, k, seed):
    p = np.full(len(y), np.nan)
    for tr, te in spatial_block_kfold(blocks, k=k, seed=seed):
        tr, te = np.asarray(tr), np.asarray(te)
        if len(set(y[tr])) < 2:
            continue
        p[te] = LogisticNumpy(seed=seed).fit(X[tr], y[tr]).predict_proba(X[te])
    return p


def auc(p, y):
    return discrimination(p, y).get("roc_auc", np.nan)


def block_boot_auc_diff(pa, pb, y, blocks, n=1000, seed=0):
    rng = np.random.default_rng(seed); ub = np.unique(blocks); idx = {b: np.where(blocks == b)[0] for b in ub}
    d = []
    for _ in range(n):
        s = np.concatenate([idx[b] for b in rng.choice(ub, len(ub))])
        if len(set(y[s])) < 2:
            continue
        d.append(auc(pa[s], y[s]) - auc(pb[s], y[s]))
    d = np.asarray(d)
    return {"mean": float(np.nanmean(d)), "ci95": [float(np.nanpercentile(d, 2.5)), float(np.nanpercentile(d, 97.5))], "n_boot": int(len(d))}


def main(argv=None):
    import pandas as pd
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", required=True); ap.add_argument("--out", default="out/geo")
    ap.add_argument("--cell-deg", type=float, default=0.1); ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    df = pd.read_csv(a.events).dropna(subset=RAIN + ["caine_ratio"]).reset_index(drop=True)
    y = df.label.values.astype(int)
    blocks = np.array([f"{int(np.floor(la / a.cell_deg))}_{int(np.floor(lo / a.cell_deg))}" for la, lo in zip(df.lat, df.lon)])
    has_fs = df.dfs.notna().values
    scores = {"caine_ratio": df.caine_ratio.values}
    if has_fs.all():
        scores["dFS_iverson"] = df.dfs.values
        gate = []
        for r in df.itertuples():
            c = float(r.c_backcalc_kpa) if "c_backcalc_kpa" in df.columns and np.isfinite(r.c_backcalc_kpa) else 5.0
            gi = GeoInputs(c_prime=c, phi_prime_deg=32.0, gamma=19.0, z=2.0, beta_deg=float(r.slope_p90_deg),
                           u_w=9.81 * max(float(r.psi_m), 0.0), I_mm_h=max(float(r.caine_I_mmh), 1e-6), D_hours=float(r.caine_D_h))
            gate.append(geo_gate(gi).p_phys)
        scores["geo_gate_repo"] = np.asarray(gate)
    Xr = np.log1p(df[RAIN].values)
    phys_cols = [np.log(np.clip(df.caine_ratio.values, 1e-4, None))] + ([df.dfs.values] if has_fs.all() else [])
    Xp = np.stack(phys_cols, 1)
    scores["logit_rain"] = oof_logit(Xr, y, blocks, a.folds, a.seed)
    scores["logit_physics"] = oof_logit(Xp, y, blocks, a.folds, a.seed)
    scores["logit_hybrid"] = oof_logit(np.hstack([Xr, Xp]), y, blocks, a.folds, a.seed)
    rep = {"name": "geo_physics", "seed": a.seed, "n": int(len(y)), "n_pos": int(y.sum()), "n_blocks": int(len(set(blocks))),
           "design": "case-control (controls = same place, other monsoon days)", "scores": {}}
    for k, p in scores.items():
        m = ~np.isnan(p)
        rep["scores"][k] = {**discrimination(p[m], y[m]), "n_scored": int(m.sum())}
        if k.startswith("logit"):
            rep["scores"][k]["ece"] = expected_calibration_error(p[m], y[m])
            rep["scores"][k]["value_score"] = value_score(y[m], p[m], 5.0, 100.0)["value_score"]
    m = ~np.isnan(scores["logit_hybrid"]) & ~np.isnan(scores["logit_rain"])
    rep["hybrid_minus_rain_auc"] = block_boot_auc_diff(scores["logit_hybrid"][m], scores["logit_rain"][m], y[m], blocks[m], seed=a.seed)
    rep["physics_minus_rain_auc"] = block_boot_auc_diff(scores["logit_physics"][m], scores["logit_rain"][m], y[m], blocks[m], seed=a.seed)
    rw = real_win(y[m], scores["logit_hybrid"][m], scores["logit_rain"][m], blocks[m], 5.0, 100.0, seed=a.seed)
    rep["real_win_hybrid_vs_rain_costloss"] = {k: (v if isinstance(v, (int, float, bool, str)) else str(v)) for k, v in rw.items()}
    # headline fields for collect_results
    rep["oof_roc_auc"] = rep["scores"]["logit_hybrid"]["roc_auc"]; rep["oof_recall_at_fpr05"] = rep["scores"]["logit_hybrid"]["recall_at_fpr05"]
    rep["physics_only_caine_auc"] = rep["scores"]["caine_ratio"]["roc_auc"]
    if "dFS_iverson" in rep["scores"]:
        rep["physics_only_dfs_auc"] = rep["scores"]["dFS_iverson"]["roc_auc"]
    rep["note"] = ("Soil parameters ASSUMED; absolute FS uncalibrated. Physics adds value only if the CI of hybrid-minus-rain "
                   "AUC excludes 0. Small n -> wide CIs.")
    json.dump(rep, open(os.path.join(a.out, f"geo_physics_s{a.seed}_report.json"), "w"), indent=2)
    print(json.dumps({k: v for k, v in rep.items() if k != "scores"}, indent=2))
    for k, v in rep["scores"].items():
        print(f"  {k:16s} AUC={v.get('roc_auc', float('nan')):.3f}  PR-AUC={v.get('pr_auc', float('nan')):.3f}  recall@FPR5%={v.get('recall_at_fpr05', float('nan')):.3f}")


if __name__ == "__main__":
    main()
