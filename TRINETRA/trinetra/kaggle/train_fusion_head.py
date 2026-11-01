"""Kaggle kernel: train the learned GMF residual head, then EXPORT it to a numpy closure for the offline
gateway (no torch at the edge).

Input cache .npz keys: base, dispersion, salience, y  (collect these from the fused validation set by
running the numpy fusion on each sample's experts and recording the three features + the true label).

Run:  python kaggle/train_fusion_head.py --data /kaggle/working/fusion_cache.npz --out /kaggle/working
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

from trinetra.deep.fusion_head import GMFHead, export_numpy                # noqa: E402
from trinetra.deep.train import set_seed, get_device                       # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="/kaggle/working")
    ap.add_argument("--cap", type=float, default=0.1)
    ap.add_argument("--epochs", type=int, default=300)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)   # BUGFIX: torch.save crashed when --out did not exist
    set_seed(0); device = get_device()
    d = np.load(args.data)
    base = torch.tensor(d["base"], dtype=torch.float32, device=device)
    disp = torch.tensor(d["dispersion"], dtype=torch.float32, device=device)
    sal = torch.tensor(d["salience"], dtype=torch.float32, device=device)
    y = torch.tensor(d["y"], dtype=torch.float32, device=device)
    residual_target = y - base                      # residual learns the gap base->label (bounded)

    head = GMFHead().to(device)
    opt = torch.optim.AdamW(head.parameters(), lr=1e-3, weight_decay=1e-4)
    for _ in range(args.epochs):
        opt.zero_grad()
        loss = head.train_step(base, disp, sal, residual_target, cap=args.cap)
        loss.backward(); opt.step()

    torch.save(head.state_dict(), os.path.join(args.out, "gmf_head.pt"))

    # Export to numpy so the OFFLINE base runtime can run gmf_fuse(..., head=closure) without torch.
    sd = head.state_dict()
    export = {
        "cap": args.cap,
        "W1": sd["net.0.weight"].cpu().numpy().tolist(), "b1": sd["net.0.bias"].cpu().numpy().tolist(),
        "W2": sd["net.2.weight"].cpu().numpy().tolist(), "b2": sd["net.2.bias"].cpu().numpy().tolist(),
    }
    with open(os.path.join(args.out, "gmf_head_numpy.json"), "w") as f:
        json.dump(export, f, indent=2)

    # sanity: the exported closure must match the torch head on a few points
    closure = export_numpy(head, cap=args.cap)
    with torch.no_grad():
        for i in range(min(5, len(base))):
            feats = {"base": float(base[i]), "dispersion": float(disp[i]), "salience": float(sal[i])}
            t_val = float(head(head.feature_tensor(base[i:i + 1], disp[i:i + 1], sal[i:i + 1]))[0]) * args.cap
            n_val = closure(feats)
            assert abs(t_val - n_val) < 1e-5, f"export mismatch: {t_val} vs {n_val}"
    print("GMF head trained + exported to numpy (torch/numpy parity verified).")


if __name__ == "__main__":
    main()
