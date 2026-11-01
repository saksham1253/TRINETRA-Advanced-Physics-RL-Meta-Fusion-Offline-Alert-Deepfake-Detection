"""data_adapters/make_rl_logs.py — build the offline-RL log .npz that trinetra/kaggle/train_offline_rl.py
expects (keys s, a, r, s_next, done, behavior_prob; datamodules.RLTransitionDataset), from ANY labeled
per-sample feature/score file. New file; no existing code is modified.

WHY: the repo's RL is OFFLINE (CQL, deep/offline_rl.py, ACTIONS = HOLD/WATCH/ALARM, gamma=0 => one-step
contextual bandit). There is NO simulator in the repo, so logged decisions must be built. Here the
"logging policy" is the repo's RuleBaselinePolicy (threshold on fused risk) made stochastic with epsilon
so every action has probability >= eps/3 (needed for the OPE positivity gate in ws5_fusion_rl.rl).

REWARD (TARGET/ASSUMPTION, not from a paper; documented in docs/07_RL_AND_META_FUSION_HINGLISH.md):
  costs come from configs/default.json  C_FA = 5, C_miss = 100.
  HOLD : y=1 -> -C_miss         y=0 -> 0
  WATCH: y=1 -> -watch_miss*C_miss  y=0 -> -watch_fa*C_FA     (defaults 0.5 and 0.2; flags below)
  ALARM: y=1 -> 0               y=0 -> -C_FA

Input .npz: feats (N,D) float (e.g. per-expert calibrated probs + u_star + salience), risk (N,) fused risk,
y (N,) 0/1 label, optional block (N,) groups. Output is one-step (s_next = s, done = 1).
Run: python data_adapters/make_rl_logs.py --inp fused_val.npz --out /kaggle/working/logs.npz --eps 0.3
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ACTIONS = ("HOLD", "WATCH", "ALARM")  # must match trinetra.deep.offline_rl.ACTIONS


def rule_action(risk: np.ndarray, p_star: float) -> np.ndarray:
    """Same cut points as ws5_fusion_rl.decision.conformal_level: <p* HOLD, <4p* WATCH, else ALARM."""
    return np.where(risk < p_star, 0, np.where(risk < 4 * p_star, 1, 2))


def reward(a: np.ndarray, y: np.ndarray, C_FA: float, C_miss: float, watch_miss: float, watch_fa: float):
    r = np.zeros(len(a), np.float32)
    r[(a == 0) & (y == 1)] = -C_miss
    r[(a == 1) & (y == 1)] = -watch_miss * C_miss
    r[(a == 1) & (y == 0)] = -watch_fa * C_FA
    r[(a == 2) & (y == 0)] = -C_FA
    return r


def build(feats, risk, y, C_FA=5.0, C_miss=100.0, eps=0.3, watch_miss=0.5, watch_fa=0.2, seed=0):
    rng = np.random.default_rng(seed)
    p_star = C_FA / (C_FA + C_miss)  # identical to common.config.p_star
    greedy = rule_action(risk, p_star)
    explore = rng.random(len(risk)) < eps
    a = np.where(explore, rng.integers(0, 3, len(risk)), greedy)
    bprob = np.where(a == greedy, 1 - eps + eps / 3, eps / 3).astype(np.float32)
    r = reward(a, y.astype(int), C_FA, C_miss, watch_miss, watch_fa)
    s = feats.astype(np.float32)
    return dict(s=s, a=a.astype(np.int64), r=r, s_next=s.copy(), done=np.ones(len(s), np.float32),
                behavior_prob=bprob)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--eps", type=float, default=0.3)
    ap.add_argument("--watch-miss", type=float, default=0.5); ap.add_argument("--watch-fa", type=float, default=0.2)
    ap.add_argument("--config", default=str(Path(__file__).resolve().parents[1] / "trinetra/configs/default.json"))
    a = ap.parse_args(argv)
    cost = json.load(open(a.config))["cost"]
    d = np.load(a.inp, allow_pickle=True)
    logs = build(d["feats"], d["risk"], d["y"], cost["C_FA"], cost["C_miss"], a.eps, a.watch_miss, a.watch_fa)
    if "block" in d.files:
        logs["block"] = d["block"]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)   # BUGFIX: crashed if folder missing
    np.savez_compressed(a.out, **logs)
    print(f"[rl-logs] n={len(logs['s'])} state_dim={logs['s'].shape[1]} action_freq="
          f"{np.bincount(logs['a'], minlength=3).tolist()} min_bprob={logs['behavior_prob'].min():.3f} -> {a.out}")


if __name__ == "__main__":
    main()
