"""trinetra.deep.offline_rl — Model 6: conservative offline-RL alarm policy (Class advisory, ws5).

Discrete-action Conservative Q-Learning (CQL). Actions = {HOLD, WATCH, ALARM}. Trained purely offline from
logged (state, action, cost-reward, next_state) tuples — no live exploration (unsafe in a disaster system).
CQL's conservative penalty pushes Q down on out-of-distribution actions so the learned policy stays near the
support of the logging policy (positivity). The policy is ADVISORY and is ALWAYS composed with the monotone
shield floor at deployment (ws5_fusion_rl.shield) so it can only be overridden UPWARD toward safety, never
used to silence a hazard (Rule 19). Deployment is admitted only after the OPE gate (ws5_fusion_rl.ope_*).

Set gamma=0 for the one-step contextual-bandit variant (recommended when transitions are weakly Markov).
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn

from .layers import MLP

ACTIONS = ("HOLD", "WATCH", "ALARM")


@dataclass
class CQLConfig:
    state_dim: int = 16
    n_actions: int = 3
    hidden: tuple = (256, 256)
    gamma: float = 0.0          # 0 => one-step bandit; >0 => sequential
    cql_alpha: float = 1.0      # conservative penalty weight
    tau: float = 0.005          # target net Polyak rate


class QNet(nn.Module):
    def __init__(self, cfg: CQLConfig):
        super().__init__()
        self.q = MLP([cfg.state_dim, *cfg.hidden, cfg.n_actions], norm=True)

    def forward(self, s):
        return self.q(s)


class CQLPolicy(nn.Module):
    """Conservative Q policy. `cql_loss` is the training objective; `act` is shielded at deployment."""

    def __init__(self, cfg: CQLConfig = CQLConfig()):
        super().__init__()
        self.cfg = cfg
        self.online = QNet(cfg)
        self.target = QNet(cfg)
        self.target.load_state_dict(self.online.state_dict())
        for p in self.target.parameters():
            p.requires_grad_(False)

    def cql_loss(self, s, a, r, s_next, done) -> dict:
        q = self.online(s)
        q_sa = q.gather(1, a.long().unsqueeze(1)).squeeze(1)
        with torch.no_grad():
            q_next = self.target(s_next).max(dim=1).values
            target = r + self.cfg.gamma * (1.0 - done.float()) * q_next
        bellman = nn.functional.mse_loss(q_sa, target)
        # CQL conservative term: logsumexp_a Q(s,a) - Q(s, a_data)
        conservative = (torch.logsumexp(q, dim=1) - q_sa).mean()
        loss = bellman + self.cfg.cql_alpha * conservative
        return {"loss": loss, "bellman": bellman.detach(), "conservative": conservative.detach()}

    @torch.no_grad()
    def polyak_update(self):
        for tp, op in zip(self.target.parameters(), self.online.parameters()):
            tp.data.mul_(1 - self.cfg.tau).add_(self.cfg.tau * op.data)

    @torch.no_grad()
    def q_values(self, s):
        return self.online(s)

    @torch.no_grad()
    def act(self, s, shield_floor_idx: int = 0) -> torch.Tensor:
        """Greedy action, then raised to the shield floor (monotone, safety-upward only, Rule 19)."""
        greedy = self.online(s).argmax(dim=1)
        floor = torch.full_like(greedy, shield_floor_idx)
        return torch.maximum(greedy, floor)

    @torch.no_grad()
    def action_probs(self, s, temperature: float = 1.0):
        """Softmax over Q as a stochastic target policy for OPE (feeds ws5_fusion_rl.ope_admission)."""
        return torch.softmax(self.online(s) / temperature, dim=1)
