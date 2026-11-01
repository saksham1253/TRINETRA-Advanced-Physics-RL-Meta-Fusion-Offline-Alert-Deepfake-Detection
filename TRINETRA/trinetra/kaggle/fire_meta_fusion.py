"""FIRE META-FUSION on REAL paired data (stacked generalization, Wolpert 1992) + fused cache for offline RL.

Why: kaggle/build_fusion_cache.py pairs experts SYNTHETICALLY. But fire_cnn, zeroshot, clip_probe and colorhist
all score the SAME 3410 OOF images (same block ids, same order, same labels) and the same 1023 held-out images,
so a real stack is possible: every expert sees the same image. This script checks that alignment and refuses
to run if it does not hold.

Level-1 features per image: logit(p_raw) of each expert, plus disagreement (sd of expert probabilities) and
range (max - min). Meta-learner: L2 logistic (eval.LogisticNumpy), trained out-of-fold on a FRESH block-grouped
5-fold split (whole blocks in one fold). Held-out: meta fitted on ALL OOF rows, applied to the held-out experts.
Compared rules: stacked meta, FM-1 (repo fuse()), plain mean, max, and every single expert (calibrated).
Gate (Rule 16): calibrated stacked meta must beat climatology AND the best single expert on cost-weighted value
with a 95% block-bootstrap CI. Balanced curated set + p* = 0.048 => value score is near 0 for everyone (docs/14),
so AUC / recall@FPR5% with a block-bootstrap CI vs the best single expert is reported as the headline too.
Caveat: OOF level-0 predictions were produced on the experts' own folds; this is standard stacking, but the
cleanest number is the HELD-OUT one (different dataset, never seen by any level).

Outputs (--out): fire_meta_fusion_s<seed>_report.json, fire_meta_fusion_s<seed>_oof.npz,
                 fire_meta_fusion_s<seed>_compare.md, fire_meta_cache.npz (feats, risk, y, block; REAL pairing)
                 -> data_adapters/make_rl_logs.py --inp fire_meta_cache.npz -> kaggle/train_offline_rl.py
Run: python kaggle/fire_meta_fusion.py --fire out_A/fire/fire_s0_oof.npz --zeroshot .../zeroshot_s0_oof.npz \
        --clip .../clip_probe_s0_oof.npz [--colorhist .../colorhist_s0_oof.npz] --out out/fire_meta --seed 0
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
from trinetra.deep.oof_utils import discrimination, save_oof, crossfit_calibrate, fit_temperature, logit, sigmoid  # noqa: E402
from trinetra.eval import (spatial_block_kfold, expected_calibration_error, value_score,       # noqa: E402
                           base_rate_climatology, LogisticNumpy, real_win)
from trinetra.ws5_fusion_rl.adapters import deep_expert                                        # noqa: E402
from trinetra.ws5_fusion_rl.fusion_models import fuse                                          # noqa: E402

C_FA, C_MISS = 5.0, 100.0
P_STAR = C_FA / (C_FA + C_MISS)
SRC = {"fire_cnn": "fire_cnn", "zeroshot": "zeroshot", "clip_probe": "clip_probe", "colorhist": "colorhist"}


def load(path):
    d = np.load(path, allow_pickle=True)
    out = {k: d[k] for k in d.files if k != "meta"}
    out["meta"] = json.loads(str(d["meta"])) if "meta" in d.files else {}
    return out


def h2(p):
    p = min(max(float(p), 1e-6), 1 - 1e-6)
    return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def features(P):
    """P (N,K) raw probabilities -> level-1 features."""
    L = logit(np.clip(P, 1e-6, 1 - 1e-6))
    return np.hstack([L, P.std(1, keepdims=True), (P.max(1) - P.min(1))[:, None]])


def fm1(Pcal, names, cfg):
    out, u = np.full(len(Pcal), np.nan), np.full(len(Pcal), np.nan)
    for i, row in enumerate(Pcal):
        f = fuse([deep_expert(SRC[n], float(p), uncertainty=0.5 * h2(p)) for n, p in zip(names, row)], cfg)
        out[i], u[i] = f.p, f.u_star
    return out, u


def metrics(p, y):
    m = ~np.isnan(p); p, y = p[m], y[m]
    a = p >= P_STAR
    return {**discrimination(p, y), "ece": expected_calibration_error(p, y),
            "value_score": value_score(y, p, C_FA, C_MISS)["value_score"],
            "miss_rate": float((~a & (y == 1)).sum() / max(1, (y == 1).sum())),
            "false_alarm_rate": float((a & (y == 0)).sum() / max(1, (y == 0).sum()))}


def boot_diff(pa, pb, y, blocks, key, n=1000, seed=0):
    rng = np.random.default_rng(seed); ub = np.unique(blocks); idx = {b: np.where(blocks == b)[0] for b in ub}
    d = []
    for _ in range(n):
        s = np.concatenate([idx[b] for b in rng.choice(ub, len(ub))])
        if len(set(y[s].tolist())) < 2:
            continue
        d.append(discrimination(pa[s], y[s])[key] - discrimination(pb[s], y[s])[key])
    d = np.asarray(d)
    return {"mean": float(d.mean()), "ci95": [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
            "significant": bool(np.percentile(d, 2.5) > 0)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fire", required=True); ap.add_argument("--zeroshot", required=True); ap.add_argument("--clip", required=True)
    ap.add_argument("--colorhist", default=None, help="OOF only (no held-out rows); excluded from the held-out stack")
    ap.add_argument("--out", default="out/fire_meta"); ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    E = {"fire_cnn": load(a.fire), "zeroshot": load(a.zeroshot), "clip_probe": load(a.clip)}
    if a.colorhist:
        E["colorhist"] = load(a.colorhist)
    ref = E["fire_cnn"]
    for n, d in E.items():                                   # REAL pairing or nothing
        if not (np.array_equal(d["block"], ref["block"]) and np.array_equal(d["y"], ref["y"])):
            raise SystemExit(f"{n}: OOF rows are not aligned with fire_cnn (block/y differ) -> cannot stack for real")
    names = list(E)
    test_names = [n for n in names if len(E[n].get("test_y", [])) and np.array_equal(E[n]["test_block"], ref["test_block"])]
    y, blocks = ref["y"].astype(int), ref["block"].astype(str)
    P = np.column_stack([E[n]["prob"] for n in names]).astype(float)
    Pc = np.column_stack([np.where(np.isnan(E[n]["prob_cal"]), E[n]["prob"], E[n]["prob_cal"]) for n in names]).astype(float)

    folds = [(np.asarray(tr), np.asarray(te)) for tr, te in spatial_block_kfold(blocks, k=a.folds, seed=a.seed)]
    fold_of_row = np.full(len(y), -1)
    for k, (_, te) in enumerate(folds):
        fold_of_row[te] = k
    X = features(P)
    meta_raw = np.full(len(y), np.nan)
    for tr, te in folds:
        meta_raw[te] = LogisticNumpy(seed=a.seed).fit(X[tr], y[tr]).predict_proba(X[te])
    meta_cal, _ = crossfit_calibrate(meta_raw, y, fold_of_row)
    cfg = Config()
    fm, u_star = fm1(Pc, names, cfg)
    fm_cal, _ = crossfit_calibrate(fm, y, fold_of_row)
    rules = {"stacked meta (calibrated)": meta_cal, "stacked meta raw": meta_raw, "FM-1 (calibrated)": fm_cal,
             "plain mean": Pc.mean(1), "max": Pc.max(1), **{f"single: {n}": Pc[:, j] for j, n in enumerate(names)}}
    table = {k: metrics(v, y) for k, v in rules.items()}
    singles = {n: table[f"single: {n}"]["roc_auc"] for n in names}
    best_single = max(singles, key=singles.get)
    p_best = Pc[:, names.index(best_single)]
    clim = base_rate_climatology(y, len(y))
    verdicts = {"climatology": real_win(y, meta_cal, clim, blocks, C_FA, C_MISS, seed=a.seed),
                f"best_single:{best_single}": real_win(y, meta_cal, p_best, blocks, C_FA, C_MISS, seed=a.seed)}
    admitted = all(bool(v["real_win"]) for v in verdicts.values())
    auc_vs_best = boot_diff(meta_cal, p_best, y, blocks, "roc_auc", seed=a.seed)
    rec_vs_best = boot_diff(meta_cal, p_best, y, blocks, "recall_at_fpr05", seed=a.seed)

    # ---- held-out (different dataset): meta fitted on ALL OOF rows of the experts that have held-out scores
    held = {}
    test_prob = test_y = test_block = None
    if test_names:
        ti = [names.index(n) for n in test_names]
        Pt = np.column_stack([E[n]["test_prob"] for n in test_names]).astype(float)
        Ptc = np.column_stack([E[n]["test_prob_cal"] for n in test_names]).astype(float)
        test_y, test_block = ref["test_y"].astype(int), ref["test_block"].astype(str)
        Xo = features(P[:, ti])
        m = LogisticNumpy(seed=a.seed).fit(Xo, y)
        T = fit_temperature(m.predict_proba(Xo), y)
        test_prob = m.predict_proba(features(Pt))
        held_rules = {"stacked meta (calibrated)": sigmoid(logit(test_prob) / T), "FM-1": fm1(Ptc, test_names, cfg)[0],
                      "plain mean": Ptc.mean(1), "max": Ptc.max(1), **{f"single: {n}": Ptc[:, j] for j, n in enumerate(test_names)}}
        held = {k: metrics(v, test_y) for k, v in held_rules.items()}
        held["_experts"] = test_names
        held["_coef"] = dict(zip([f"logit_{n}" for n in test_names] + ["sd", "range"], map(float, m.w)))

    meta = save_oof(os.path.join(a.out, f"fire_meta_fusion_s{a.seed}_oof.npz"), name="fire_meta_fusion", seed=a.seed,
                    folds=a.folds, prob=meta_raw, y=y, block=blocks, fold_of_row=fold_of_row,
                    test_prob=test_prob, test_y=test_y, test_block=test_block,
                    extra_meta={"experts": names, "expert_run_ids": {n: E[n]["meta"].get("run_id") for n in names},
                                "pairing": "REAL (same image for every expert)"})
    t = table["stacked meta (calibrated)"]
    rep = {"name": "fire_meta_fusion", "seed": a.seed, "run_id": meta["run_id"], "pairing": "REAL (same image for every expert)",
           "experts": names, "expert_run_ids": meta["expert_run_ids"], "n": int(len(y)), "n_blocks": int(len(set(blocks))),
           "spatial_cv": True, "admitted": admitted, "gate_input": "stacked meta, cross-fit calibrated OOF",
           "baselines": verdicts, "best_single": best_single,
           "oof_roc_auc": t["roc_auc"], "oof_pr_auc": t["pr_auc"], "oof_recall_at_fpr05": t["recall_at_fpr05"],
           "oof_recall_at_fpr01": t["recall_at_fpr01"], "value_score_model": t["value_score"], "ece_crossfit_calibrated": t["ece"],
           "meta_minus_best_auc": auc_vs_best, "meta_minus_best_auc_mean": auc_vs_best["mean"], "meta_minus_best_recall_fpr05": rec_vs_best,
           "mean_u_star_fm1": float(np.nanmean(u_star)), "rules": table, "heldout": held,
           "note": "balanced curated pack: AUC/recall are the headline, value score is indicative (p*=0.048)"}
    if held:
        h = held["stacked meta (calibrated)"]
        rep.update(test_roc_auc=h["roc_auc"], test_pr_auc=h["pr_auc"], test_recall_at_fpr05=h["recall_at_fpr05"],
                   test_ece_calibrated=h["ece"])
    json.dump(rep, open(os.path.join(a.out, f"fire_meta_fusion_s{a.seed}_report.json"), "w"), indent=2, default=float)

    # ---- fused cache for offline RL (REAL pairing); column 0 = risk, as make_rl_logs/train_offline_rl expect
    dis = Pc.std(1)
    feats = np.column_stack([meta_cal, *[Pc[:, j] for j in range(len(names))], u_star, dis])
    np.savez_compressed(os.path.join(a.out, "fire_meta_cache.npz"), feats=feats, risk=meta_cal, y=y.astype(float), block=blocks,
                        feat_names=np.array(["meta_cal", *names, "u_star", "disagreement"]), synthetic_pairing=np.array(False))

    L = [f"# Fire meta-fusion (REAL pairing) · seed {a.seed} · n {rep['n']} images, {rep['n_blocks']} blocks", "",
         f"Experts: {', '.join(names)} · gate (calibrated stack vs climatology and best single `{best_single}`, cost CI): "
         f"**{'ADMITTED' if admitted else 'NOT ADMITTED'}**", "",
         "## OOF (block-grouped CV)", "",
         "| rule | ROC-AUC | PR-AUC | recall@FPR5% | ECE | value score | miss @p* | false alarm @p* |", "|---|---|---|---|---|---|---|---|"]
    row = lambda k, t: (f"| {k} | {t['roc_auc']:.3f} | {t['pr_auc']:.3f} | {t['recall_at_fpr05']:.3f} | {t['ece']:.3f} | "  # noqa: E731
                        f"{t['value_score']:.3f} | {t['miss_rate']:.3f} | {t['false_alarm_rate']:.3f} |")
    L += [row(k, v) for k, v in table.items()]
    L += ["", f"Stack − best single AUC {auc_vs_best['mean']:+.3f} (95% CI {auc_vs_best['ci95'][0]:+.3f} to {auc_vs_best['ci95'][1]:+.3f}); "
          f"recall@FPR5% {rec_vs_best['mean']:+.3f} (CI {rec_vs_best['ci95'][0]:+.3f} to {rec_vs_best['ci95'][1]:+.3f})."]
    if held:
        L += ["", f"## Held-out ({len(test_y)} images, different dataset; experts {', '.join(test_names)})", "",
              "| rule | ROC-AUC | PR-AUC | recall@FPR5% | ECE | value score | miss @p* | false alarm @p* |", "|---|---|---|---|---|---|---|---|"]
        L += [row(k, v) for k, v in held.items() if not k.startswith("_")]
        L += ["", "Meta weights (standardized): " + ", ".join(f"{k} {v:+.2f}" for k, v in held["_coef"].items())]
    open(os.path.join(a.out, f"fire_meta_fusion_s{a.seed}_compare.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
