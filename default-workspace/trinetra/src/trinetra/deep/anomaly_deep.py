"""trinetra.deep.anomaly_deep — Model 3: deep multivariate time-series anomaly (Class data, ws8).

A causal TCN encoder feeds three heads whose scores are fused:
  - reconstruction : TCN decoder; high reconstruction error => anomalous
  - forecast       : one-step-ahead predictor; high forecast residual => anomalous
  - Deep-SVDD      : embedding distance to a learned hypersphere center c
Causal convolutions mean no look-ahead (anti-leak invariant, gate G6). Unsupervised: trained on NORMAL
telemetry so events become out-of-distribution. The numpy ensemble (ws8_anomaly) remains the always-on
fallback; this is the admitted-only upgrade.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn

from .layers import TCN
from .losses import deep_svdd_loss


@dataclass
class AnomalyConfig:
    n_feat: int = 8
    channels: tuple = (32, 32, 64)
    emb_dim: int = 32
    recon_weight: float = 1.0
    forecast_weight: float = 1.0
    svdd_weight: float = 0.5


class DeepAnomaly(nn.Module):
    def __init__(self, cfg: AnomalyConfig = AnomalyConfig()):
        super().__init__()
        self.cfg = cfg
        self.encoder = TCN(cfg.n_feat, list(cfg.channels))
        enc_out = cfg.channels[-1]
        self.to_emb = nn.Conv1d(enc_out, cfg.emb_dim, 1)
        self.decoder = TCN(cfg.emb_dim, list(cfg.channels[::-1]) + [cfg.n_feat])
        self.forecast = nn.Conv1d(enc_out, cfg.n_feat, 1)
        self.register_buffer("center", torch.zeros(cfg.emb_dim))

    def forward(self, x):           # x: (B, n_feat, T)
        enc = self.encoder(x)
        emb = self.to_emb(enc)                      # (B, emb, T)
        recon = self.decoder(emb)
        pred_next = self.forecast(enc)              # aligned one-step forecast
        return {"recon": recon, "pred_next": pred_next, "emb": emb}

    @torch.no_grad()
    def init_center(self, loader, device, eps: float = 0.1):
        """Deep-SVDD center = mean embedding over normal data (set once before training the SVDD head)."""
        self.eval()
        acc, n = torch.zeros(self.cfg.emb_dim, device=device), 0
        for batch in loader:
            x = batch["x"].to(device)
            emb = self.forward(x)["emb"].mean(dim=2)   # pool over time
            acc += emb.sum(0); n += emb.shape[0]
        c = acc / max(n, 1)
        c[(c.abs() < eps)] = eps                       # avoid trivial zero center
        self.center.copy_(c)

    def loss(self, x) -> dict:
        out = self.forward(x)
        recon = nn.functional.mse_loss(out["recon"], x)
        # one-step forecast: predict x[:, :, 1:] from features up to t
        fc = nn.functional.mse_loss(out["pred_next"][:, :, :-1], x[:, :, 1:])
        svdd = deep_svdd_loss(out["emb"].mean(dim=2), self.center)
        total = (self.cfg.recon_weight * recon + self.cfg.forecast_weight * fc
                 + self.cfg.svdd_weight * svdd)
        return {"loss": total, "recon": recon.detach(), "forecast": fc.detach(), "svdd": svdd.detach()}

    @torch.no_grad()
    def anomaly_score(self, x):
        """Per-sample score in R+ (higher = more anomalous): recon err + forecast err + SVDD distance."""
        out = self.forward(x)
        recon_e = ((out["recon"] - x) ** 2).mean(dim=(1, 2))
        fc_e = ((out["pred_next"][:, :, :-1] - x[:, :, 1:]) ** 2).mean(dim=(1, 2))
        svdd_d = ((out["emb"].mean(dim=2) - self.center) ** 2).sum(dim=1)
        return recon_e + fc_e + svdd_d
