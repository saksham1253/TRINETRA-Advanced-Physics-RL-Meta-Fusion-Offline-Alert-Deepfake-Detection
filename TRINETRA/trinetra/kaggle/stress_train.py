"""CONFUSER-AWARE retraining after the cross-modal run (account S): does training on hard negatives cut false alarms on a
confuser type the model has NEVER seen, without losing real fires?

Design (leave-one-stress-set-out, LOSO). Confuser sets C = stress_weather, stress_small_flames, stress_scenes (all y = 0).
For each held-out set h in C:
  probe_base : logistic probe on frozen CLIP embeddings of fire.npz only (= the clip_probe expert)
  probe_conf : same probe, trained on fire.npz + the OTHER confuser sets as extra negatives (sample weight --neg-weight)
  stack_base : logistic stack (kaggle/fire_meta_fusion.features) on OOF rows [fire_cnn, zeroshot, probe_base]
  stack_conf : stack fitted on OOF rows + the other confuser rows; their probe scores are NESTED out-of-set (the probe that
               scores confuser set j never saw j), so the stack is not fitted on in-sample probe scores
  Every model is calibrated with a temperature fitted on its own OOF fire rows (block folds, as eval_zeroshot.py).
Operating points on h: fixed 0.5, cost-loss p* = 5/105, and thr90 = the threshold that gives recall 0.90 on that model's OOF
fire positives (equal-recall comparison, the fair one). Real-fire checks: ROC-AUC and recall@thr90 on the held-out DeepFire
test set (and heldout_firedataset / heldout_homefire if present).
Gate per held-out set: FA@thr90(conf) < FA@thr90(base) with a 95 % block-bootstrap CI below 0 AND DeepFire AUC drop <= 0.01.
Outputs (--out): stress_s<seed>_report.json (name "stress"), stress_s<seed>_compare.md, stress_s<seed>_rows.npz,
emb_cache_<model>.npz (CLIP embeddings reused across seeds).
Run: python kaggle/stress_train.py --data npz/fire.npz --test npz/deepfire.npz --stress npz/stress_*.npz \
        --heldout npz/heldout_firedataset.npz npz/heldout_homefire.npz --fire-models out_A_session/fire --out out/stress --seed 0
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src")); sys.path.insert(0, str(HERE))

from eval_zeroshot import PROMPTS, concept_text_features, embed, labels, load_images, zs_prob   # noqa: E402
from fire_meta_fusion import features                                                          # noqa: E402
from trinetra.deep.oof_utils import discrimination, ensure_dir, fit_temperature, logit, sigmoid  # noqa: E402
from trinetra.eval import LogisticNumpy, spatial_block_kfold                                   # noqa: E402

P_STAR = 5.0 / 105.0
CONFUSERS = ("stress_weather", "stress_small_flames", "stress_scenes")


def fit_probe(X, y, C, w=None):
    from sklearn.linear_model import LogisticRegression
    return LogisticRegression(C=C, max_iter=3000).fit(X, y, sample_weight=w)


def thr_at_recall(p, y, recall=0.90):
    pos = np.sort(p[y == 1])
    return float(pos[int(np.floor((1 - recall) * len(pos)))]) if len(pos) else 0.5


def cal(p, T):
    return sigmoid(logit(np.clip(p, 1e-6, 1 - 1e-6)) / T)


def boot_fa_diff(pa, pb, ta, tb, blocks, n=2000, seed=0):
    """Block bootstrap of FA(a at ta) - FA(b at tb) on an all-negative set; returns mean and 95 % CI."""
    rng = np.random.default_rng(seed)
    ub = np.unique(blocks); idx = {b: np.where(blocks == b)[0] for b in ub}
    da = (pa >= ta).astype(float) - (pb >= tb).astype(float)
    sums = np.array([da[idx[b]].sum() for b in ub]); cnt = np.array([len(idx[b]) for b in ub])
    bs = []
    for _ in range(n):
        k = rng.integers(0, len(ub), len(ub)); bs.append(sums[k].sum() / cnt[k].sum())
    return {"mean": float(da.mean()), "ci95": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True); ap.add_argument("--test", default=None)
    ap.add_argument("--stress", nargs="*", default=[]); ap.add_argument("--heldout", nargs="*", default=[])
    ap.add_argument("--fire-models", default=None, help="A run fire/ folder (fire_s<seed>_oof.npz + fold checkpoints)")
    ap.add_argument("--out", default="/kaggle/working/out/stress"); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--folds", type=int, default=5); ap.add_argument("--probe-C", type=float, default=1.0)
    ap.add_argument("--neg-weight", type=float, default=1.0, help="sample weight of each confuser negative")
    ap.add_argument("--model", default="ViT-L-14"); ap.add_argument("--pretrained", default="laion2b_s32b_b82k")
    ap.add_argument("--prompts", default="v2", choices=sorted(PROMPTS)); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    ensure_dir(a.out)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # ---------------- embeddings (cached across seeds) + zero-shot scores
    cache = os.path.join(a.out, f"emb_cache_{a.model.replace('/', '_')}{'_dry' if a.dry_run else ''}.npz")
    sets = {"fire": a.data, **({"test": a.test} if a.test and os.path.exists(a.test) else {})}
    sets.update({Path(f).stem: f for f in a.stress + a.heldout if os.path.exists(f)})
    E, Y, B, ZS = {}, {}, {}, {}
    if os.path.exists(cache):
        d = np.load(cache, allow_pickle=True)
        for k in sets:
            if f"E:{k}" in d.files:
                E[k], Y[k], B[k], ZS[k] = d[f"E:{k}"], d[f"Y:{k}"], d[f"B:{k}"], d[f"Z:{k}"]
        print(f"[stress] embeddings from cache {cache}: {sorted(E)}")
    if set(sets) - set(E):
        import open_clip
        model, _, _ = open_clip.create_model_and_transforms(a.model, pretrained=None if a.dry_run else a.pretrained)
        tok = open_clip.get_tokenizer(a.model); model = model.to(device).eval()
        pcfg = getattr(model.visual, "preprocess_cfg", {}) or {}
        mean = pcfg.get("mean", (0.48145466, 0.4578275, 0.40821073)); std = pcfg.get("std", (0.26862954, 0.26130258, 0.27577711))
        size = model.visual.image_size[0] if isinstance(model.visual.image_size, (tuple, list)) else model.visual.image_size
        text, tags = concept_text_features(model, tok, device, PROMPTS[a.prompts])
        scale = float(model.logit_scale.exp()) if hasattr(model, "logit_scale") else 100.0
        for k, f in sets.items():
            if k in E:
                continue
            X, Yr, blk = load_images(f)
            E[k] = embed(model, X, mean, std, device, size); Y[k] = labels(Yr, "any") if Yr is not None else np.zeros(len(X), int)
            B[k] = np.asarray(blk).astype(str); ZS[k] = zs_prob(E[k], text, tags, scale, "any"); del X
            print(f"[stress] embedded {k}: {E[k].shape}, positives {int(Y[k].sum())}", flush=True)
        np.savez_compressed(cache, **{f"{p}:{k}": v for k in E for p, v in (("E", E[k]), ("Y", Y[k]), ("B", B[k]), ("Z", ZS[k]))})
    y, blk = Y["fire"].astype(int), B["fire"]
    conf = [c for c in CONFUSERS if c in E and Y[c].sum() == 0]
    if len(conf) < 2:
        raise SystemExit(f"need at least 2 all-negative confuser sets, found {conf}")
    fold_of_row = np.full(len(y), -1)
    for k, (_, va) in enumerate(spatial_block_kfold(blk, k=a.folds, seed=a.seed)):
        fold_of_row[np.asarray(va)] = k

    # ---------------- fire CNN scores (A weights): OOF on fire rows, fold-ensemble on every other set
    fire = {}
    if a.fire_models:
        oofp = os.path.join(a.fire_models, f"fire_s{a.seed}_oof.npz")
        if os.path.exists(oofp):
            o = np.load(oofp, allow_pickle=True)
            if np.array_equal(o["block"].astype(str), blk) and np.array_equal(o["y"].astype(int), y):
                from crossmodal_fusion import fire_cnn_scorer, _images
                score = fire_cnn_scorer(a.fire_models, a.seed, device)
                fire["fire"] = o["prob"].astype(float)
                for k, f in sets.items():
                    if k != "fire":
                        fire[k] = score(_images(f))
                print("[stress] fire_cnn: A OOF aligned with fire.npz; other sets scored with the fold ensemble")
            else:
                print("[stress] fire_cnn OOF rows do not match fire.npz (rebuilt data?): stacks use zeroshot + probe only")
    use_cnn = "fire" in fire

    def probe_scores(neg_sets, score_sets):
        """Probe trained on fire rows (+ confuser negatives): OOF on fire rows, full fit on score_sets."""
        Xn = np.vstack([E[s] for s in neg_sets]) if neg_sets else np.zeros((0, E["fire"].shape[1]))
        wn = np.full(len(Xn), a.neg_weight)
        oof = np.full(len(y), np.nan)
        for k in sorted(set(fold_of_row.tolist()) - {-1}):
            tr, va = fold_of_row != k, fold_of_row == k
            m = fit_probe(np.vstack([E["fire"][tr], Xn]), np.concatenate([y[tr], np.zeros(len(Xn), int)]), a.probe_C,
                          np.concatenate([np.ones(tr.sum()), wn]))
            oof[va] = m.predict_proba(E["fire"][va])[:, 1]
        full = fit_probe(np.vstack([E["fire"], Xn]), np.concatenate([y, np.zeros(len(Xn), int)]), a.probe_C, np.concatenate([np.ones(len(y)), wn]))
        return oof, {s: full.predict_proba(E[s])[:, 1] for s in score_sets}

    others = [k for k in sets if k != "fire"]
    rows, folds_out = {}, []
    for h in conf:
        train_neg = [c for c in conf if c != h]
        oof_b, sc_b = probe_scores([], others)
        oof_c, sc_c = probe_scores(train_neg, others)
        # nested out-of-set probe scores for the confuser rows used to fit stack_conf
        nested = {}
        for j in train_neg:
            _, s = probe_scores([c for c in train_neg if c != j], [j]); nested[j] = s[j]
        Tb, Tc = fit_temperature(oof_b, y), fit_temperature(oof_c, y)
        models = {"zeroshot": (ZS["fire"], {s: ZS[s] for s in others}), "probe_base": (oof_b, sc_b), "probe_conf": (oof_c, sc_c)}
        if use_cnn:
            models["fire_cnn"] = (fire["fire"], {s: fire[s] for s in others})
        # stacks
        cols = (["fire_cnn"] if use_cnn else []) + ["zeroshot"]
        def stack_rows(probe_oof, probe_sets, extra_neg=None):
            P = np.column_stack([models[c][0] for c in cols] + [probe_oof])
            Yy = y.copy()
            if extra_neg:
                Pn = np.vstack([np.column_stack([models[c][1][j] for c in cols] + [extra_neg[j]]) for j in extra_neg])
                P = np.vstack([P, Pn]); Yy = np.concatenate([Yy, np.zeros(len(Pn), int)])
            st = LogisticNumpy(seed=a.seed).fit(features(P), Yy)
            oofP = np.column_stack([models[c][0] for c in cols] + [probe_oof])
            oof_stack = np.full(len(y), np.nan)          # stack OOF on fire rows via the same block folds
            for k in sorted(set(fold_of_row.tolist()) - {-1}):
                tr = np.concatenate([fold_of_row != k, np.ones(len(Yy) - len(y), bool)])
                m = LogisticNumpy(seed=a.seed).fit(features(P[tr]), Yy[tr])
                oof_stack[fold_of_row == k] = m.predict_proba(features(oofP[fold_of_row == k]))
            out = {s: st.predict_proba(features(np.column_stack([models[c][1][s] for c in cols] + [probe_sets[s]]))) for s in others}
            return oof_stack, out
        models["stack_base"] = stack_rows(oof_b, sc_b)
        models["stack_conf"] = stack_rows(oof_c, sc_c, nested)
        res = {}
        for name, (oof, sc) in models.items():
            T = fit_temperature(oof[~np.isnan(oof)], y[~np.isnan(oof)])
            oc = cal(oof, T); t90 = thr_at_recall(oc[~np.isnan(oc)], y[~np.isnan(oc)])
            ph = cal(sc[h], T)
            r = {"T": T, "thr90": t90, "oof_auc": discrimination(oof, y).get("roc_auc"),
                 "fa_0p5": float((ph >= 0.5).mean()), "fa_pstar": float((ph >= P_STAR).mean()), "fa_thr90": float((ph >= t90).mean())}
            for s in [k for k in others if k not in conf]:
                ps = cal(sc[s], T); ys = Y[s].astype(int)
                if ys.sum() and (1 - ys).sum():
                    r[f"{s}_auc"] = discrimination(ps, ys)["roc_auc"]
                if ys.sum():
                    r[f"{s}_recall_thr90"] = float((ps[ys == 1] >= t90).mean())
                if (1 - ys).sum():
                    r[f"{s}_fa_thr90"] = float((ps[ys == 0] >= t90).mean())
            res[name] = r
            rows[f"{h}:{name}"] = ph
        gates = {}
        for base, new in (("probe_base", "probe_conf"), ("stack_base", "stack_conf")):
            Tb_, Tn_ = res[base]["T"], res[new]["T"]
            d = boot_fa_diff(cal(models[new][1][h], Tn_), cal(models[base][1][h], Tb_), res[new]["thr90"], res[base]["thr90"], B[h], seed=a.seed)
            auc_drop = (res[base].get("test_auc", np.nan) - res[new].get("test_auc", np.nan)) if "test_auc" in res[base] else np.nan
            gates[new] = {"fa_thr90_diff": d, "test_auc_drop": float(auc_drop) if np.isfinite(auc_drop) else None,
                          "pass": bool(d["ci95"][1] < 0 and (not np.isfinite(auc_drop) or auc_drop <= 0.01))}
        folds_out.append({"heldout_confuser": h, "trained_on_confusers": train_neg, "n_heldout": int(len(Y[h])),
                          "n_blocks_heldout": int(len(set(B[h].tolist()))), "models": res, "gates": gates})
        print(f"[stress] held-out {h}: FA@thr90 probe {res['probe_base']['fa_thr90']:.3f} -> {res['probe_conf']['fa_thr90']:.3f}, "
              f"stack {res['stack_base']['fa_thr90']:.3f} -> {res['stack_conf']['fa_thr90']:.3f}", flush=True)

    mean = lambda f: float(np.mean([f(x) for x in folds_out]))  # noqa: E731
    rep = {"name": "stress", "seed": a.seed, "run_id": f"stress-s{a.seed}", "design": "leave-one-confuser-set-out; equal recall 0.90 on OOF fire positives",
           "confusers": conf, "fire_cnn_in_stack": use_cnn, "neg_weight": a.neg_weight, "folds": folds_out,
           "fa_thr90_probe_base_mean": mean(lambda x: x["models"]["probe_base"]["fa_thr90"]),
           "fa_thr90_probe_conf_mean": mean(lambda x: x["models"]["probe_conf"]["fa_thr90"]),
           "fa_thr90_stack_base_mean": mean(lambda x: x["models"]["stack_base"]["fa_thr90"]),
           "fa_thr90_stack_conf_mean": mean(lambda x: x["models"]["stack_conf"]["fa_thr90"]),
           "test_auc_probe_base": mean(lambda x: x["models"]["probe_base"].get("test_auc", np.nan)),
           "test_auc_probe_conf": mean(lambda x: x["models"]["probe_conf"].get("test_auc", np.nan)),
           "admitted": all(g["pass"] for x in folds_out for k, g in x["gates"].items() if k == "probe_conf"),
           "stack_conf_admitted": all(g["pass"] for x in folds_out for k, g in x["gates"].items() if k == "stack_conf"),
           "note": "admitted = confuser-aware probe cuts false alarms on EVERY unseen confuser set (CI) without a DeepFire AUC drop > 0.01"}
    json.dump(rep, open(os.path.join(a.out, f"stress_s{a.seed}_report.json"), "w"), indent=2, default=float)
    np.savez_compressed(os.path.join(a.out, f"stress_s{a.seed}_rows.npz"), **rows)
    L = [f"# Confuser-aware retraining (leave-one-confuser-set-out) · seed {a.seed}", "",
         f"Confuser sets: {', '.join(conf)} · fire_cnn in stack: {use_cnn} · negative weight {a.neg_weight}", "",
         "| held-out confuser | model | FA @0.5 | FA @p* | FA @recall-0.90 thr | DeepFire AUC | DeepFire recall @thr |", "|---|---|---|---|---|---|---|"]
    for x in folds_out:
        for n, r in x["models"].items():
            L.append(f"| {x['heldout_confuser']} | {n} | {r['fa_0p5']:.3f} | {r['fa_pstar']:.3f} | {r['fa_thr90']:.3f} | "
                     f"{r.get('test_auc', float('nan')):.3f} | {r.get('test_recall_thr90', float('nan')):.3f} |")
        for n, g in x["gates"].items():
            L.append(f"| {x['heldout_confuser']} | gate {n} | FA diff {g['fa_thr90_diff']['mean']:+.3f} (CI {g['fa_thr90_diff']['ci95'][0]:+.3f} to "
                     f"{g['fa_thr90_diff']['ci95'][1]:+.3f}) | AUC drop {g['test_auc_drop']} | **{'PASS' if g['pass'] else 'FAIL'}** | | |")
    L += ["", f"Mean FA at equal recall: probe {rep['fa_thr90_probe_base_mean']:.3f} -> {rep['fa_thr90_probe_conf_mean']:.3f}; "
          f"stack {rep['fa_thr90_stack_base_mean']:.3f} -> {rep['fa_thr90_stack_conf_mean']:.3f}. Admitted (probe): {rep['admitted']}."]
    open(os.path.join(a.out, f"stress_s{a.seed}_compare.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
