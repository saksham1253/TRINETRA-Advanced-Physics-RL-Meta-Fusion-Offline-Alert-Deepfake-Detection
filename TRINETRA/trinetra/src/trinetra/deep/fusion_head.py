"""trinetra.deep.fusion_head — learned GMF residual head (Class B, ws5) with a numpy export bridge.

The meta-fusion base (gated precision-weighted mean, or PHARAOH when enabled) is physics/reliability-driven
and always present. This small head learns only a BOUNDED residual correction on top of that base, from
transparent features [base, dispersion, salience]. Two safety properties are preserved:
  1. the residual is hard-clipped to +/- cap downstream (ws5_fusion_rl.gmf.bounded_residual), so a
     mis-trained head can never dominate the physics-anchored base;
  2. `export_numpy` serializes the trained head to a PURE-NUMPY closure, so inference runs in the offline
     base runtime (no torch on the edge gateway) and plugs straight into `gmf_fuse(..., head=closure)`.
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn

FEATURES = ("base", "dispersion", "salience")


class GMFHead(nn.Module):
    """[base, dispersion, salience] -> raw residual (tanh-bounded to [-1,1]; final cap applied in numpy)."""

    def __init__(self, hidden: int = 16):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(len(FEATURES), hidden), nn.Tanh(),
            nn.Linear(hidden, 1), nn.Tanh())

    def forward(self, feats):       # feats: (B, 3)
        return self.net(feats).squeeze(-1)

    def feature_tensor(self, base, dispersion, salience):
        return torch.stack([base, dispersion, salience], dim=1)

    def train_step(self, base, dispersion, salience, residual_target, cap: float = 0.1):
        """Supervise the residual toward (y - base), clipped to +/- cap (the admissible correction)."""
        feats = self.feature_tensor(base, dispersion, salience)
        pred = self.forward(feats) * cap
        return nn.functional.mse_loss(pred, torch.clamp(residual_target, -cap, cap))


def export_numpy(head: GMFHead, cap: float = 0.1):
    """Serialize GMFHead to a pure-numpy callable f(feats_dict)->raw_residual for offline inference.

    The returned closure matches the `head` signature expected by ws5_fusion_rl.gmf.bounded_residual.
    """
    sd = head.state_dict()
    W1 = sd["net.0.weight"].cpu().numpy(); b1 = sd["net.0.bias"].cpu().numpy()
    W2 = sd["net.2.weight"].cpu().numpy(); b2 = sd["net.2.bias"].cpu().numpy()

    def closure(feats: dict) -> float:
        x = np.array([feats["base"], feats["dispersion"], feats["salience"]], float)
        h = np.tanh(W1 @ x + b1)
        raw = float(np.tanh(W2 @ h + b2)[0])
        return raw * cap        # bounded_residual still re-clips to +/- cap (defense in depth)

    return closure


EXPERT_FEATURES = ("p", "u", "c", "r")   # per-expert features fed to the attention head


class AttentionFusionHead(nn.Module):
    """Learned ATTENTION meta-fusion over a variable set of workstream/group experts (Class B).

    Hierarchical fusion (ws5_fusion_rl.hierarchical) produces one expert per workstream. This head learns,
    with attention, HOW MUCH to listen to each workstream given its [p, u, c, r], instead of a fixed
    precision weight. Two safety properties are kept so it stays advisory and physics-anchored (R19/R20):

      * BASE is a CONVEX (softmax-attention) combination of the experts' probabilities, so it is bounded in
        [min_i p_i, max_i p_i] — attention can re-weight but can NOT invent a probability outside the
        experts' own range.
      * A small residual is added, hard-bounded to +/- cap, then the sum is clipped to [0,1]. A mis-trained
        head therefore cannot push the fused risk far from what the experts actually said.

    Unavailable experts are masked out of the softmax (they get zero attention)."""

    def __init__(self, feat_dim: int = len(EXPERT_FEATURES), hidden: int = 16, cap: float = 0.1):
        super().__init__()
        self.cap = float(cap)
        self.score = nn.Sequential(nn.Linear(feat_dim, hidden), nn.Tanh(), nn.Linear(hidden, 1))
        self.residual = nn.Sequential(nn.Linear(feat_dim, hidden), nn.Tanh(), nn.Linear(hidden, 1), nn.Tanh())

    def forward(self, x, mask=None):
        """x: (B, N, F) expert features; mask: (B, N) bool (True=available). Returns dict."""
        logits = self.score(x).squeeze(-1)                      # (B, N)
        if mask is not None:
            logits = logits.masked_fill(~mask, float("-inf"))
        attn = torch.softmax(logits, dim=1)                     # convex weights over experts
        p_experts = x[..., 0]                                   # feature 0 is each expert's probability p
        base = (attn * p_experts).sum(dim=1)                    # in [min p_i, max p_i] (convex)
        context = (attn.unsqueeze(-1) * x).sum(dim=1)           # attention-pooled context (B, F)
        residual = self.residual(context).squeeze(-1) * self.cap
        p = torch.clamp(base + residual, 0.0, 1.0)
        return {"p": p, "base": base, "residual": residual, "attn": attn}

    def loss(self, out, target, c_fa: float = 5.0, c_miss: float = 100.0):
        """Cost-sensitive BCE on the fused probability (miss costs >> false-alarm, per the cost model)."""
        p = torch.clamp(out["p"], 1e-6, 1 - 1e-6)
        w_pos = c_miss / (c_fa + c_miss); w_neg = c_fa / (c_fa + c_miss)
        bce = -(w_pos * target * torch.log(p) + w_neg * (1 - target) * torch.log(1 - p))
        return bce.mean()


def export_attention_numpy(head: "AttentionFusionHead"):
    """Serialize AttentionFusionHead to a pure-numpy closure for the offline gateway (no torch).

    closure(experts) where experts is a list of dicts with keys p,u,c,r,available -> fused probability."""
    sd = head.state_dict()
    sW1 = sd["score.0.weight"].cpu().numpy(); sb1 = sd["score.0.bias"].cpu().numpy()
    sW2 = sd["score.2.weight"].cpu().numpy(); sb2 = sd["score.2.bias"].cpu().numpy()
    rW1 = sd["residual.0.weight"].cpu().numpy(); rb1 = sd["residual.0.bias"].cpu().numpy()
    rW2 = sd["residual.2.weight"].cpu().numpy(); rb2 = sd["residual.2.bias"].cpu().numpy()
    cap = head.cap

    def closure(experts: list) -> float:
        avail = [e for e in experts if e.get("available", True)]
        if not avail:
            return 0.0
        X = np.array([[e["p"], e["u"], e["c"], e["r"]] for e in avail], float)   # (N, 4)
        logits = (np.tanh(X @ sW1.T + sb1) @ sW2.T + sb2).ravel()               # (N,)
        a = np.exp(logits - logits.max()); a = a / a.sum()                       # softmax
        base = float((a * X[:, 0]).sum())
        context = (a[:, None] * X).sum(axis=0)                                   # (4,)
        resid = float(np.tanh(np.tanh(context @ rW1.T + rb1) @ rW2.T + rb2)[0]) * cap
        return float(np.clip(base + resid, 0.0, 1.0))

    return closure
