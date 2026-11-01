"""Kaggle kernel: train Conservative-Q offline-RL alarm policy; admit ONLY via OPE gate (Rule 19).

Run:  python kaggle/train_offline_rl.py --data /kaggle/input/trinetra-rl-logs/logs.npz --out /kaggle/working
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from trinetra.deep.datamodules import RLTransitionDataset                  # noqa: E402
from trinetra.deep.offline_rl import CQLPolicy, CQLConfig, ACTIONS         # noqa: E402
from trinetra.deep.train import TrainConfig, set_seed, get_device, _to_device, setup_perf, n_gpus  # noqa: E402
from trinetra.ws5_fusion_rl import ope_admission                          # noqa: E402
from trinetra.ws5_fusion_rl.rl import wis_value                           # noqa: E402
from trinetra.deep.oof_utils import ensure_dir                             # noqa: E402


def rule_actions(risk: np.ndarray, p_star: float) -> np.ndarray:
    """RuleBaselinePolicy extended to 3 actions with decision.conformal_level cut points (p*, 4p*)."""
    return np.where(risk < p_star, 0, np.where(risk < 4 * p_star, 1, 2))


def paired_bootstrap_lcb(b, t_learn, t_rule, r, n_boot=500, alpha=0.05, seed=0):
    """Lower (alpha) quantile of WIS(learned) - WIS(rule) under row bootstrap."""
    rng = np.random.default_rng(seed)
    n = len(r); d = []
    for _ in range(n_boot):
        i = rng.integers(0, n, n)
        d.append(wis_value(b[i], t_learn[i], r[i])[0] - wis_value(b[i], t_rule[i], r[i])[0])
    return float(np.quantile(d, alpha)), float(np.mean(d))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="/kaggle/working")
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--gamma", type=float, default=0.0)
    ap.add_argument("--batch", type=int, default=256, help="RL nets are tiny -> use a big batch, 1 GPU")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--risk-col", type=int, default=0, help="state column holding fused risk (make_rl_logs puts it at 0)")
    ap.add_argument("--p-star", type=float, default=5.0 / 105.0, help="C_FA/(C_FA+C_miss) from configs/default.json")
    ap.add_argument("--n-boot", type=int, default=500)
    args = ap.parse_args()
    ensure_dir(args.out)

    set_seed(args.seed); setup_perf(); device = get_device()
    cfg = TrainConfig(epochs=args.epochs, batch_size=args.batch, scale_batch_by_gpus=False)
    # NOTE: the Q-net is tiny (state_dim x 3 actions). Multi-GPU scatter/gather overhead would be LARGER
    # than the compute, so RL deliberately runs on ONE GPU with a large batch instead of DataParallel.
    print(f"[trinetra] GPUs visible={n_gpus()} | offline-RL uses 1 GPU (tiny net) | batch={cfg.batch_size}")
    ds = RLTransitionDataset(args.data)
    state_dim = ds.s.shape[1]
    policy = CQLPolicy(CQLConfig(state_dim=state_dim, n_actions=len(ACTIONS), gamma=args.gamma)).to(device)
    opt = torch.optim.AdamW(policy.online.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
    dl = DataLoader(ds, batch_size=cfg.batch_size, shuffle=True,
                    pin_memory=torch.cuda.is_available(), num_workers=cfg.num_workers)

    import time
    t0 = time.time()
    for ep in range(cfg.epochs):
        tot, nb = 0.0, 0
        for b in dl:
            b = _to_device(b, device)
            opt.zero_grad()
            out = policy.cql_loss(b["s"], b["a"], b["r"], b["s_next"], b["done"])
            out["loss"].backward()
            torch.nn.utils.clip_grad_norm_(policy.online.parameters(), cfg.grad_clip)
            opt.step(); policy.polyak_update()
            tot += float(out["loss"].detach()); nb += 1
        if (ep + 1) % 5 == 0 or ep + 1 == cfg.epochs:      # progress line so long runs never look frozen
            el = time.time() - t0
            print(f"[rl] seed {args.seed} epoch {ep + 1}/{cfg.epochs} CQL loss {tot / max(nb, 1):.4f} · "
                  f"{el:.0f}s · ETA {el / (ep + 1) * (cfg.epochs - ep - 1):.0f}s", flush=True)
    torch.save(policy.state_dict(), os.path.join(args.out, "offline_rl.pt"))

    # ---- OPE admission gate (ws5_fusion_rl.ope_admission): deploy ONLY if feasible AND >= baseline ----
    policy.eval()
    with torch.no_grad():
        s = torch.tensor(ds.s, device=device)
        target_probs_all = policy.action_probs(s).cpu().numpy()
    taken = ds.a
    target_probs = target_probs_all[np.arange(len(taken)), taken]
    behavior_probs = ds.bprob if ds.bprob is not None else np.full(len(taken), 1.0 / len(ACTIONS))
    rewards = ds.r
    # legacy verdict (kept for comparability): learned vs the logging policy's realized reward
    verdict = ope_admission(behavior_probs, target_probs, rewards, baseline_rewards=rewards)
    # BUGFIX: the legacy gate compared against the LOGGING policy and admitted on noise-level differences.
    # The real comparator is RuleBaselinePolicy, evaluated by WIS on the SAME logs, with a paired-bootstrap
    # lower confidence bound that must exceed 0.
    rule_a = rule_actions(ds.s[:, args.risk_col], args.p_star)
    rule_probs = (taken == rule_a).astype(float)          # deterministic rule -> pi(a_logged|s) in {0,1}
    v_rule, ess_rule = wis_value(behavior_probs, rule_probs, rewards)
    lcb, mean_gain = paired_bootstrap_lcb(behavior_probs, target_probs, rule_probs, rewards, args.n_boot, seed=args.seed)
    deploy = bool(verdict.feasible and lcb > 0)
    report = {
        "name": "offline_rl", "seed": args.seed,
        "ope_value_target": verdict.value_target, "ope_value_baseline": verdict.value_baseline,
        "ess": verdict.ess, "feasible": verdict.feasible,
        "legacy_deploy_vs_logging_policy": verdict.deploy_learned,
        "ope_value_rule_baseline": v_rule, "ess_rule": ess_rule,
        "gain_vs_rule_mean": mean_gain, "gain_vs_rule_lcb95": lcb,
        "deploy_learned": deploy,
        "note": ("DEPLOY learned policy (OPE-admitted); still shielded upward at inference"
                 if deploy else
                 "KEEP RuleBaselinePolicy — OPE did not admit the learned policy (Rule 19 fail-safe)"),
    }
    with open(os.path.join(args.out, f"offline_rl_s{args.seed}_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
