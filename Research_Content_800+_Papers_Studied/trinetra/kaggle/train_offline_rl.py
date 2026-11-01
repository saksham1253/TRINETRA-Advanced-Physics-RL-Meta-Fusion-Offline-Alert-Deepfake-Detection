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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="/kaggle/working")
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--gamma", type=float, default=0.0)
    ap.add_argument("--batch", type=int, default=256, help="RL nets are tiny -> use a big batch, 1 GPU")
    args = ap.parse_args()

    set_seed(0); setup_perf(); device = get_device()
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

    for _ in range(cfg.epochs):
        for b in dl:
            b = _to_device(b, device)
            opt.zero_grad()
            out = policy.cql_loss(b["s"], b["a"], b["r"], b["s_next"], b["done"])
            out["loss"].backward()
            torch.nn.utils.clip_grad_norm_(policy.online.parameters(), cfg.grad_clip)
            opt.step(); policy.polyak_update()
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
    # baseline = the logged behavior policy's realized reward
    verdict = ope_admission(behavior_probs, target_probs, rewards, baseline_rewards=rewards)
    report = {
        "name": "offline_rl",
        "ope_value_target": verdict.value_target, "ope_value_baseline": verdict.value_baseline,
        "ess": verdict.ess, "feasible": verdict.feasible, "deploy_learned": verdict.deploy_learned,
        "note": ("DEPLOY learned policy (OPE-admitted); still shielded upward at inference"
                 if verdict.deploy_learned else
                 "KEEP RuleBaselinePolicy — OPE did not admit the learned policy (Rule 19 fail-safe)"),
    }
    with open(os.path.join(args.out, "offline_rl_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
