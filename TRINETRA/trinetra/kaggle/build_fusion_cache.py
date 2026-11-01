"""Build the fusion cache from per-model OOF artifacts and COMPARE averaging rules (docs/08 experiment).

!!! SYNTHETIC PAIRING !!!  No dataset in the prototype pack has the same scene seen by camera + IoT + media
check at once. So a fused "event" is built by drawing, for a sampled label y, one OOF row WITH THAT LABEL from
each source. This tests the fusion MATH on real per-source score distributions; it does NOT measure real
multi-sensor correlation. Every output is tagged `synthetic_pairing=true`.

Inputs : standard `*_oof.npz` (deep/oof_utils.py): --fire (fire_cnn) [--zeroshot] [--colorhist] [--iot] [--deepfake]
         (hackathon scope 2026-10-31: IoT is FUTURE WORK, so the default run is fire_cnn + zeroshot [+ deepfake])
Outputs: fusion_cache.npz   keys base, dispersion, salience, y            -> kaggle/train_fusion_head.py
                            keys feats, risk, y (+ block)                 -> data_adapters/make_rl_logs.py
         fusion_compare.json / .md  FM-1 vs PHARAOH vs median vs max, mean ± sd over seeds
Deepfake: p_fake down-weights media experts, r' = r(1 - p_fake) (adapters.authenticity_adjusted_reliability);
--fake-frac f injects "fake fire video" attacks on y=0 events (media experts high, p_fake drawn from fakes).
Uncertainty per expert: u = 0.5 * H2(p) (normalized binary entropy). ASSUMPTION, documented in docs/07.

Run: python kaggle/build_fusion_cache.py --fire fire_s0_oof.npz --zeroshot zeroshot_s0_oof.npz \
        [--deepfake deepfake_s0_oof.npz --fake-frac 0.1] --out /kaggle/working
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from trinetra.common.config import Config                                          # noqa: E402
from trinetra.ws5_fusion_rl.adapters import deep_expert, authenticity_adjusted_reliability, _POLICY  # noqa: E402
from trinetra.ws5_fusion_rl.fusion_models import fuse                               # noqa: E402
from trinetra.ws5_fusion_rl.nf import effective_weight, weighted_dispersion         # noqa: E402
from trinetra.ws5_fusion_rl.pharaoh import pharaoh_fuse                             # noqa: E402
from trinetra.eval import value_score, expected_calibration_error                   # noqa: E402

MEDIA = {"fire_cnn", "zeroshot", "colorhist"}   # image-based experts: down-weighted by p_fake


def load(path):
    d = np.load(path, allow_pickle=True)
    p = d["prob_cal"].astype(float)
    p = np.where(np.isnan(p), d["prob"], p)              # rows without a calibration fold fall back to raw
    m = ~np.isnan(p)
    return p[m], d["y"][m].astype(int)


def h2(p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return float(-(p * np.log2(p) + (1 - p) * np.log2(1 - p)))


def draw(rng, p, y, label):
    idx = np.where(y == label)[0]
    if len(idx) == 0:
        raise SystemExit(f"source has no rows with label {label}; cannot pair")
    return float(p[rng.choice(idx)])


def build(sources: dict, deepfake, n: int, pos_rate: float, fake_frac: float, seed: int, cfg: Config):
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n):
        y = int(rng.random() < pos_rate)
        attack = (deepfake is not None) and y == 0 and rng.random() < fake_frac
        p_fake = draw(rng, *deepfake, 1 if attack else 0) if deepfake is not None else 0.0
        experts, ps = [], {}
        for name, (p, yy) in sources.items():
            lab = 1 if (attack and name in MEDIA) else y        # fake fire video: media looks like fire
            pi = draw(rng, p, yy, lab)
            r = _POLICY[name][0]
            if name in MEDIA:
                r = authenticity_adjusted_reliability(r, p_fake)
            experts.append(deep_expert(name, pi, uncertainty=0.5 * h2(pi), reliability=r))
            ps[name] = pi
        f = fuse(experts, cfg)
        w = [effective_weight(e, cfg.get("fusion.tau", 0.5)) for e in experts]
        pv = [e.p for e in experts]
        rows.append(dict(y=y, attack=attack, p_fake=p_fake, fm1=f.p, u_star=f.u_star, salience=f.salience,
                         dispersion=weighted_dispersion(pv, w), pharaoh=pharaoh_fuse(experts)["p"],
                         median=float(np.median(pv)), max=float(np.max(pv)), **{f"p_{k}": v for k, v in ps.items()}))
    return rows


def metrics(y, p, C_FA, C_miss):
    p_star = C_FA / (C_FA + C_miss)
    a = (p >= p_star).astype(int)
    return {"value_score": value_score(y, p, C_FA, C_miss)["value_score"], "ece": expected_calibration_error(p, y),
            "miss_rate": float(((a == 0) & (y == 1)).sum() / max(1, (y == 1).sum())),
            "false_alarm_rate": float(((a == 1) & (y == 0)).sum() / max(1, (y == 0).sum()))}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fire", required=True); ap.add_argument("--iot", help="FUTURE WORK (not in hackathon scope)")
    ap.add_argument("--zeroshot"); ap.add_argument("--colorhist"); ap.add_argument("--deepfake")
    ap.add_argument("--n", type=int, default=5000); ap.add_argument("--pos-rate", type=float, default=0.2)
    ap.add_argument("--fake-frac", type=float, default=0.0)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    ap.add_argument("--out", default="/kaggle/working")
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    cfg = Config()
    C_FA, C_miss = cfg.get("cost.C_FA", 5.0), cfg.get("cost.C_miss", 100.0)
    sources = {"fire_cnn": load(a.fire)}
    for name, path in (("zeroshot", a.zeroshot), ("colorhist", a.colorhist), ("iot", a.iot)):
        if path:
            sources[name] = load(path)
    if len(sources) < 2:
        raise SystemExit("fusion needs >= 2 hazard sources (e.g. --fire and --zeroshot)")
    deepfake = load(a.deepfake) if a.deepfake else None

    rules = ["fm1", "pharaoh", "median", "max"] + [f"p_{k}" for k in sources]
    per_seed = {r: [] for r in rules}
    for s in a.seeds:
        rows = build(sources, deepfake, a.n, a.pos_rate, a.fake_frac, s, cfg)
        y = np.array([r["y"] for r in rows])
        for rule in rules:
            per_seed[rule].append(metrics(y, np.array([r[rule] for r in rows]), C_FA, C_miss))
        if s == a.seeds[0]:
            g = lambda k: np.array([r[k] for r in rows], float)  # noqa: E731
            feats = np.stack([g("fm1"), g("u_star"), g("salience"), g("dispersion")] + [g(f"p_{k}") for k in sources], 1)
            np.savez_compressed(os.path.join(a.out, "fusion_cache.npz"), base=g("fm1"), dispersion=g("dispersion"),
                                salience=g("salience"), y=g("y"), feats=feats, risk=g("fm1"), attack=g("attack"),
                                feat_names=np.array(["fm1", "u_star", "salience", "dispersion"] + [f"p_{k}" for k in sources]),
                                synthetic_pairing=np.array(True))
    summary = {}
    for rule, ms in per_seed.items():
        summary[rule] = {k: {"mean": float(np.mean([m[k] for m in ms])), "sd": float(np.std([m[k] for m in ms]))} for k in ms[0]}
    out = {"synthetic_pairing": True, "sources": list(sources), "deepfake": bool(deepfake), "fake_frac": a.fake_frac,
           "n_per_seed": a.n, "pos_rate": a.pos_rate, "seeds": a.seeds, "C_FA": C_FA, "C_miss": C_miss, "rules": summary}
    json.dump(out, open(os.path.join(a.out, "fusion_compare.json"), "w"), indent=2)
    lines = ["| rule | value score | ECE | miss rate @p* | false-alarm rate @p* |", "|---|---|---|---|---|"]
    for rule, m in summary.items():
        f = lambda k: f"{m[k]['mean']:.3f} ± {m[k]['sd']:.3f}"  # noqa: E731
        lines.append(f"| {rule} | {f('value_score')} | {f('ece')} | {f('miss_rate')} | {f('false_alarm_rate')} |")
    md = "SYNTHETIC PAIRING (see docstring). " + f"sources={list(sources)} fake_frac={a.fake_frac}\n\n" + "\n".join(lines)
    open(os.path.join(a.out, "fusion_compare.md"), "w").write(md + "\n")
    print(md)


if __name__ == "__main__":
    main()
