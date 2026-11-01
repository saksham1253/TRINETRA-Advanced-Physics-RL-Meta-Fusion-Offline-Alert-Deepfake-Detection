"""LANDSLIDE META-FUSION on REAL paired data: the HLD pipeline (experts + physics consistency + FM-1 averaging +
uncertainty + physics shield), evaluated on the same NASA-GLC events used by geo_physics_hindcast.py.

Unlike kaggle/build_fusion_cache.py (fire domain, SYNTHETIC pairing), every expert here scores the SAME row
(same place, same day), so this measures real fusion, not only fusion maths.

Experts per row (all out-of-fold on the same spatial-block folds; probabilities via a 1-D monotone logistic map
fitted on the OTHER folds only, so the physics formulas themselves are never fitted):
  rain      DATA  logistic on log1p(rain_1d..rain_30d, rain_max3)
  caine     A     Caine I-D ratio (no fit)
  dfs       A     Iverson + infinite-slope FS drop dFS with back-analysed c' (no fit)
  geo_gate  A     repo ws1b_geophys geo gate p_phys
  geo_pinn  B     Geo-PINN OOF probability (only if its rows align exactly with this table)
Physics consistency (NF-1): phi = mean(caine, dfs); data/learned experts get c_i = nf1_consistency(p_i, phi);
physics experts c = 1. Uncertainty u_i = 0.5 * H2(p_i) (same ASSUMPTION as the fire fusion, docs/07).
Rules compared: FM-1 (repo fuse(), default config), PHARAOH, plain mean, median, max, physics-only mean,
FM-1 + shield (FS_backcalc < 1 => p >= ORANGE cut 4p*, as ws5_fusion_rl/shield.py), rain-only, and a stacked logistic (rain + physics features).
Gate (Rule 16): calibrated FM-1 must beat climatology AND the rain-only model on cost-weighted value with a
95% block-bootstrap CI. Report: geo_fusion_s<seed>_report.json (+ compare .md/.json, OOF npz).
Run: python kaggle/geo_meta_fusion.py --events geo/events/geo_events.csv --pinn geo/pinn/geo_pinn_s0_oof.npz --out geo/fusion
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from trinetra.common.config import Config                                                     # noqa: E402
from trinetra.deep.oof_utils import discrimination, save_oof, crossfit_calibrate               # noqa: E402
from trinetra.eval import (spatial_block_kfold, expected_calibration_error, value_score,       # noqa: E402
                           base_rate_climatology, LogisticNumpy, real_win)
from trinetra.ws1b_geophys.gate import GeoInputs, geo_gate                                     # noqa: E402
from trinetra.ws5_fusion_rl.adapters import deep_expert                                        # noqa: E402
from trinetra.ws5_fusion_rl.fusion_models import fuse                                          # noqa: E402
from trinetra.ws5_fusion_rl.nf import nf1_consistency                                          # noqa: E402
from trinetra.ws5_fusion_rl.pharaoh import pharaoh_fuse                                        # noqa: E402

RAIN = ["rain_1d", "rain_3d", "rain_7d", "rain_15d", "rain_30d", "rain_max3"]
C_FA, C_MISS = 5.0, 100.0
P_STAR = C_FA / (C_FA + C_MISS)


def oof_logit(X, y, folds, seed):
    p = np.full(len(y), np.nan)
    for tr, te in folds:
        tr, te = np.asarray(tr), np.asarray(te)
        if len(set(y[tr].tolist())) < 2:
            continue
        p[te] = LogisticNumpy(seed=seed).fit(X[tr], y[tr]).predict_proba(X[te])
    return p


def h2(p):
    p = min(max(float(p), 1e-6), 1 - 1e-6)
    return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def metrics(p, y):
    m = ~np.isnan(p); p, y = p[m], y[m]
    a = p >= P_STAR
    return {**discrimination(p, y), "ece": expected_calibration_error(p, y),
            "value_score": value_score(y, p, C_FA, C_MISS)["value_score"],
            "miss_rate": float((~a & (y == 1)).sum() / max(1, (y == 1).sum())),
            "false_alarm_rate": float((a & (y == 0)).sum() / max(1, (y == 0).sum())), "n": int(m.sum())}


def block_boot_auc_diff(pa, pb, y, blocks, n=1000, seed=0):
    rng = np.random.default_rng(seed); ub = np.unique(blocks); idx = {b: np.where(blocks == b)[0] for b in ub}
    d = []
    for _ in range(n):
        s = np.concatenate([idx[b] for b in rng.choice(ub, len(ub))])
        if len(set(y[s].tolist())) < 2:
            continue
        d.append(discrimination(pa[s], y[s])["roc_auc"] - discrimination(pb[s], y[s])["roc_auc"])
    d = np.asarray(d)
    return {"mean": float(np.nanmean(d)), "ci95": [float(np.nanpercentile(d, 2.5)), float(np.nanpercentile(d, 97.5))]}


def main(argv=None):
    import pandas as pd
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", required=True); ap.add_argument("--pinn", default=None)
    ap.add_argument("--out", default="out/geo/fusion"); ap.add_argument("--cell-deg", type=float, default=0.1)
    ap.add_argument("--folds", type=int, default=5); ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    base = pd.read_csv(a.events)

    # Geo-PINN rows = rows with fs (data_adapters/build_geo.py: ok = df.dropna(subset=["fs"])), same order
    base["p_pinn"] = np.nan; pinn_status = "not provided"
    if a.pinn and os.path.exists(a.pinn):
        d = np.load(a.pinn, allow_pickle=True)
        pp = np.where(np.isnan(d["prob_cal"]), d["prob"], d["prob_cal"]); py = d["y"].astype(int)
        mfs = base.fs.notna().values
        if mfs.sum() == len(pp) and np.array_equal(base.label.values[mfs].astype(int), py):
            base.loc[mfs, "p_pinn"] = pp; pinn_status = f"aligned ({len(pp)} rows)"
        else:
            pinn_status = f"NOT aligned (pinn {len(pp)} rows vs {int(mfs.sum())}); excluded"
    df = base.dropna(subset=RAIN + ["caine_ratio", "dfs"]).reset_index(drop=True)
    y = df.label.values.astype(int)
    blocks = np.array([f"{int(np.floor(la / a.cell_deg))}_{int(np.floor(lo / a.cell_deg))}" for la, lo in zip(df.lat, df.lon)])
    folds = [(np.asarray(tr), np.asarray(te)) for tr, te in spatial_block_kfold(blocks, k=a.folds, seed=a.seed)]
    fold_of_row = np.full(len(y), -1)
    for k, (_, te) in enumerate(folds):
        fold_of_row[te] = k

    gate = []
    for r in df.itertuples():
        c = float(r.c_backcalc_kpa) if np.isfinite(r.c_backcalc_kpa) else 5.0
        gi = GeoInputs(c_prime=c, phi_prime_deg=32.0, gamma=19.0, z=2.0, beta_deg=float(r.slope_p90_deg),
                       u_w=9.81 * max(float(r.psi_m), 0.0), I_mm_h=max(float(r.caine_I_mmh), 1e-6), D_hours=float(r.caine_D_h))
        gate.append(geo_gate(gi).p_phys)
    gate = np.clip(np.asarray(gate, float), 1e-6, 1 - 1e-6)

    Xr = np.log1p(df[RAIN].values)
    lc = np.log(np.clip(df.caine_ratio.values, 1e-4, None)).reshape(-1, 1)
    ld = df.dfs.values.reshape(-1, 1)
    lg = np.log(gate / (1 - gate)).reshape(-1, 1)
    E = {"rain": oof_logit(Xr, y, folds, a.seed),
         "caine": oof_logit(lc, y, folds, a.seed),          # monotone map only: AUC equals the raw Caine ratio
         "dfs": oof_logit(ld, y, folds, a.seed),
         "geo_gate": oof_logit(lg, y, folds, a.seed)}
    use_pinn = bool(df.p_pinn.notna().all())
    if use_pinn:
        E["geo_pinn"] = df.p_pinn.values.astype(float)
    stacked = oof_logit(np.hstack([Xr, lc, ld]), y, folds, a.seed)
    SRC = {"rain": "rain", "caine": "geo_phys", "dfs": "geo_phys", "geo_gate": "geo_phys", "geo_pinn": "geo_pinn"}
    PHYS = {"caine", "dfs", "geo_gate"}

    cfg = Config()
    out = {k: np.full(len(y), np.nan) for k in ("fm1", "u_star", "pharaoh", "mean", "median", "max", "physics_mean")}
    for i in range(len(y)):
        ps = {k: float(v[i]) for k, v in E.items() if not np.isnan(v[i])}
        if len(ps) < 2:
            continue
        phi = float(np.mean([ps[k] for k in ("caine", "dfs") if k in ps]))
        ex = [deep_expert(SRC[k], p, uncertainty=0.5 * h2(p),
                          consistency=1.0 if k in PHYS else nf1_consistency(p, phi)) for k, p in ps.items()]
        f = fuse(ex, cfg)
        out["fm1"][i], out["u_star"][i] = f.p, f.u_star
        out["pharaoh"][i] = pharaoh_fuse(ex)["p"]
        v = list(ps.values())
        out["mean"][i], out["median"][i], out["max"][i] = np.mean(v), np.median(v), np.max(v)
        out["physics_mean"][i] = np.mean([ps[k] for k in PHYS if k in ps])
    fm1_cal, _ = crossfit_calibrate(out["fm1"], y, fold_of_row)
    # repo shield (ws5_fusion_rl/shield.py): FS < 1 raises the level to at least ORANGE, i.e. p >= 4 p*
    orange = 4 * P_STAR
    shield = np.where(df.fs_backcalc.values < 1.0, np.maximum(fm1_cal, orange), fm1_cal)

    rules = {"FM-1 (calibrated)": fm1_cal, "FM-1 raw": out["fm1"], "FM-1 + physics shield": shield,
             "PHARAOH": out["pharaoh"], "plain mean": out["mean"], "median": out["median"], "max": out["max"],
             "physics-only mean": out["physics_mean"], "stacked logistic (rain+physics)": stacked,
             **{f"single: {k}": v for k, v in E.items()}}
    table = {k: metrics(v, y) for k, v in rules.items()}

    m = ~np.isnan(fm1_cal) & ~np.isnan(E["rain"])
    clim = base_rate_climatology(y[m], int(m.sum()))
    verdicts = {"climatology": real_win(y[m], fm1_cal[m], clim, blocks[m], C_FA, C_MISS, seed=a.seed),
                "rain_only_oof": real_win(y[m], fm1_cal[m], E["rain"][m], blocks[m], C_FA, C_MISS, seed=a.seed)}
    admitted = all(bool(v.get("real_win")) for v in verdicts.values())
    auc_diff = block_boot_auc_diff(fm1_cal[m], E["rain"][m], y[m], blocks[m], seed=a.seed)
    auc_diff_st = block_boot_auc_diff(fm1_cal[m], stacked[m], y[m], blocks[m], seed=a.seed)

    meta = save_oof(os.path.join(a.out, f"geo_fusion_s{a.seed}_oof.npz"), name="geo_fusion", seed=a.seed, folds=a.folds,
                    prob=out["fm1"], y=y, block=blocks, fold_of_row=fold_of_row,
                    extra_meta={"experts": list(E), "pinn": pinn_status, "pairing": "REAL (same rows)"})
    best = max(table, key=lambda k: table[k].get("roc_auc", float("nan")) if not math.isnan(table[k].get("roc_auc", float("nan"))) else -1)
    rep = {"name": "geo_fusion", "seed": a.seed, "run_id": meta["run_id"], "pairing": "REAL (same place, same day for every expert)",
           "n": int(len(y)), "n_pos": int(y.sum()), "n_blocks": int(len(set(blocks))), "experts": list(E), "pinn": pinn_status,
           "admitted": admitted, "gate_input": "FM-1 cross-fit calibrated OOF",
           "baselines": {k: {kk: (vv if isinstance(vv, (int, float, bool, str)) else str(vv)) for kk, vv in v.items()} for k, v in verdicts.items()},
           "oof_roc_auc": table["FM-1 (calibrated)"]["roc_auc"], "oof_pr_auc": table["FM-1 (calibrated)"]["pr_auc"],
           "oof_recall_at_fpr05": table["FM-1 (calibrated)"]["recall_at_fpr05"],
           "value_score_model": table["FM-1 (calibrated)"]["value_score"], "ece_crossfit_calibrated": table["FM-1 (calibrated)"]["ece"],
           "fm1_minus_rain_auc": auc_diff, "fm1_minus_stacked_auc": auc_diff_st, "best_rule_by_auc": best,
           "mean_u_star": float(np.nanmean(out["u_star"])), "frac_uncertain_u_gt_0p6": float(np.nanmean(out["u_star"] > 0.6)),
           "rules": table, "note": "case-control design: base rate is artificial; AUC/recall are the headline, value score is indicative"}
    json.dump(rep, open(os.path.join(a.out, f"geo_fusion_s{a.seed}_report.json"), "w"), indent=2, default=float)
    L = [f"# Landslide meta-fusion (REAL pairing) · seed {a.seed} · n {rep['n']} ({rep['n_pos']} events, {rep['n_blocks']} blocks)", "",
         f"Experts: {', '.join(E)} · Geo-PINN: {pinn_status} · gate (calibrated FM-1 vs climatology and rain-only, cost CI): "
         f"**{'ADMITTED' if admitted else 'NOT ADMITTED'}**", "",
         "| rule | ROC-AUC | PR-AUC | recall@FPR5% | ECE | value score | miss rate @p* | false alarms @p* |", "|---|---|---|---|---|---|---|---|"]
    for k, t in table.items():
        L.append(f"| {k} | {t['roc_auc']:.3f} | {t['pr_auc']:.3f} | {t['recall_at_fpr05']:.3f} | {t['ece']:.3f} | {t['value_score']:.3f} "
                 f"| {t['miss_rate']:.3f} | {t['false_alarm_rate']:.3f} |")
    L += ["", f"FM-1 − rain AUC {auc_diff['mean']:+.3f} (95% CI {auc_diff['ci95'][0]:+.3f} to {auc_diff['ci95'][1]:+.3f}); "
          f"FM-1 − stacked {auc_diff_st['mean']:+.3f} (CI {auc_diff_st['ci95'][0]:+.3f} to {auc_diff_st['ci95'][1]:+.3f}). "
          f"Mean U* {rep['mean_u_star']:.3f}; {rep['frac_uncertain_u_gt_0p6']:.1%} of rows flagged uncertain (U* > 0.6)."]
    open(os.path.join(a.out, f"geo_fusion_s{a.seed}_compare.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
