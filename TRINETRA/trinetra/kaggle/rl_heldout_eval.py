"""HELD-OUT check of the offline-RL alarm policy (replaces the in-sample OPE number).

train_offline_rl.py trains CQL and scores it by WIS-OPE on the SAME logs, which is optimistic. Here the labeled
fused cache (feats, risk, y, block) is split by WHOLE blocks into k folds. For each fold the logs are built from
the TRAIN rows only (data_adapters/make_rl_logs.build, same epsilon-rule logging policy and rewards), CQL is
trained on them, and on the TEST rows every policy is scored with the TRUE realized reward (labels known, so no
OPE is needed):
  cql          greedy CQL action
  rule         fixed cut points on fused risk: < p* HOLD, < 4p* WATCH, else ALARM (repo RuleBaselinePolicy)
  rule_tuned   the two cut points grid-searched on the TRAIN rows (a strong, cheap non-RL baseline)
  always_alarm / always_hold, oracle (ALARM iff y=1)
Deploy verdict: CQL must beat BOTH rules with a 95% block-bootstrap lower bound > 0 (mean reward per row).
Run: python kaggle/rl_heldout_eval.py --cache results/fire_meta/fire_meta_cache.npz --out results/offline_rl_heldout --seed 0
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "data_adapters"))

from make_rl_logs import build, reward                                      # noqa: E402
from trinetra.deep.offline_rl import CQLPolicy, CQLConfig, ACTIONS          # noqa: E402
from trinetra.deep.train import set_seed                                    # noqa: E402
from trinetra.eval import spatial_block_kfold                               # noqa: E402

C_FA, C_MISS, WATCH_MISS, WATCH_FA = 5.0, 100.0, 0.5, 0.2
P_STAR = C_FA / (C_FA + C_MISS)


def cut(risk, lo, hi):
    return np.where(risk < lo, 0, np.where(risk < hi, 1, 2))


def tune_rule(risk, y):
    grid = np.unique(np.quantile(risk, np.linspace(0, 1, 61)))
    best = (-np.inf, P_STAR, 4 * P_STAR)
    for i, lo in enumerate(grid):
        for hi in grid[i:]:
            v = reward(cut(risk, lo, hi), y, C_FA, C_MISS, WATCH_MISS, WATCH_FA).mean()
            if v > best[0]:
                best = (v, float(lo), float(hi))
    return best[1], best[2]


def train_cql(logs, epochs, seed, batch=256):
    set_seed(seed)
    pol = CQLPolicy(CQLConfig(state_dim=logs["s"].shape[1], n_actions=len(ACTIONS), gamma=0.0))
    opt = torch.optim.AdamW(pol.online.parameters(), lr=1e-3, weight_decay=1e-4)
    T = {k: torch.tensor(logs[k]) for k in ("s", "a", "r", "s_next", "done")}
    n = len(T["s"]); g = torch.Generator().manual_seed(seed)
    for _ in range(epochs):
        for idx in torch.randperm(n, generator=g).split(batch):
            opt.zero_grad()
            out = pol.cql_loss(T["s"][idx], T["a"][idx], T["r"][idx], T["s_next"][idx], T["done"][idx])
            out["loss"].backward(); torch.nn.utils.clip_grad_norm_(pol.online.parameters(), 1.0)
            opt.step(); pol.polyak_update()
    pol.eval()
    return pol


def block_lcb(diff, blocks, n=2000, seed=0):
    ub = np.unique(blocks); m = np.array([diff[blocks == b].sum() for b in ub]); c = np.array([(blocks == b).sum() for b in ub])
    rng = np.random.default_rng(seed); bs = []
    for _ in range(n):
        k = rng.integers(0, len(ub), len(ub)); bs.append(m[k].sum() / c[k].sum())
    return float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True); ap.add_argument("--out", default="results/offline_rl_heldout")
    ap.add_argument("--folds", type=int, default=5); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--epochs", type=int, default=50); ap.add_argument("--eps", type=float, default=0.3)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    d = np.load(a.cache, allow_pickle=True)
    X, risk, y, blocks = d["feats"].astype(np.float32), d["risk"].astype(float), d["y"].astype(int), d["block"].astype(str)
    acts = {k: np.full(len(y), -1) for k in ("cql", "rule", "rule_tuned")}
    cuts = []
    for k, (tr, te) in enumerate(spatial_block_kfold(blocks, k=a.folds, seed=a.seed)):
        logs = build(X[tr], risk[tr], y[tr], C_FA, C_MISS, a.eps, WATCH_MISS, WATCH_FA, seed=a.seed + k)
        pol = train_cql(logs, a.epochs, a.seed + k)
        with torch.no_grad():
            acts["cql"][te] = pol.q_values(torch.tensor(X[te])).argmax(1).numpy()
        acts["rule"][te] = cut(risk[te], P_STAR, 4 * P_STAR)
        lo, hi = tune_rule(risk[tr], y[tr]); cuts.append([lo, hi])
        acts["rule_tuned"][te] = cut(risk[te], lo, hi)
        print(f"[rl-heldout] seed {a.seed} fold {k + 1}/{a.folds} done · tuned cuts {lo:.3f}/{hi:.3f}", flush=True)
    acts["always_alarm"] = np.full(len(y), 2); acts["always_hold"] = np.zeros(len(y), int); acts["oracle"] = np.where(y == 1, 2, 0)
    R = {k: reward(v, y, C_FA, C_MISS, WATCH_MISS, WATCH_FA).astype(float) for k, v in acts.items()}
    pol_tab = {}
    for k, v in acts.items():
        pos, neg = y == 1, y == 0
        pol_tab[k] = {"reward_per_row": float(R[k].mean()), "miss_rate": float((v[pos] == 0).mean()),
                      "watch_rate": float((v == 1).mean()), "alarm_rate_on_negatives": float((v[neg] == 2).mean()),
                      "action_freq": np.bincount(v, minlength=3).tolist()}
    gains = {}
    for base in ("rule", "rule_tuned"):
        diff = R["cql"] - R[base]
        lo, hi = block_lcb(diff, blocks, seed=a.seed)
        gains[base] = {"mean": float(diff.mean()), "ci95": [lo, hi]}
    deploy = all(g["ci95"][0] > 0 for g in gains.values())
    rep = {"name": "offline_rl_heldout", "seed": a.seed, "n": int(len(y)), "n_blocks": int(len(set(blocks))),
           "evaluation": "block-held-out folds, TRUE realized reward from labels (no OPE)", "cache": a.cache,
           "policies": pol_tab, "gain_vs_rule": gains["rule"], "gain_vs_rule_tuned": gains["rule_tuned"],
           "gain_vs_rule_mean": gains["rule"]["mean"], "gain_vs_rule_lcb95": gains["rule"]["ci95"][0],
           "gain_vs_tuned_rule_mean": gains["rule_tuned"]["mean"], "gain_vs_tuned_rule_lcb95": gains["rule_tuned"]["ci95"][0],
           "tuned_cuts_per_fold": cuts, "deploy_learned": deploy,
           "note": "DEPLOY: CQL beats both rules on held-out blocks" if deploy else
                   "KEEP the rule: CQL does not beat both rules on held-out blocks (95% LCB)"}
    json.dump(rep, open(os.path.join(a.out, f"offline_rl_heldout_s{a.seed}_report.json"), "w"), indent=2)
    print(json.dumps({k: rep[k] for k in ("gain_vs_rule", "gain_vs_rule_tuned", "deploy_learned")}, indent=1))
    for k, v in pol_tab.items():
        print(f"  {k:13s} reward/row {v['reward_per_row']:+.3f} miss {v['miss_rate']:.3f} FA-alarm {v['alarm_rate_on_negatives']:.3f} watch {v['watch_rate']:.3f}")


if __name__ == "__main__":
    main()
