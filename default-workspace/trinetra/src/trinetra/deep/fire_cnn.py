"""trinetra.deep.fire_cnn — Model 2: spatiotemporal fire/smoke detector (Class A + data, ws1a/ws4).

Per-frame CNN encoder -> temporal GRU -> {fire, smoke} logits, plus an auxiliary flicker-frequency head
regularized toward the Strouhal law f ~ 1.5/sqrt(D) (physics aux loss). The temporal pathway is the key
false-alarm suppressor (sun glint / headlights are single-frame; real fire flickers persistently). The
established-physics gate (Heskestad/Byram) still runs at inference; novel ND flicker terms stay Class-C and
are injected only via the gated aux weight (default 0).
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn

from .layers import ConvBNAct
from .losses import strouhal_consistency_loss


@dataclass
class FireNetConfig:
    in_ch: int = 3
    base: int = 32
    gru_hidden: int = 128
    n_classes: int = 2          # [fire, smoke] (multi-label)
    strouhal_weight: float = 0.0   # Class-C novel flicker term -> OFF by default (Rule 20)


class FrameEncoder(nn.Module):
    def __init__(self, in_ch: int, base: int):
        super().__init__()
        self.net = nn.Sequential(
            ConvBNAct(in_ch, base), nn.MaxPool2d(2),
            ConvBNAct(base, base * 2), nn.MaxPool2d(2),
            ConvBNAct(base * 2, base * 4), nn.MaxPool2d(2),
            ConvBNAct(base * 4, base * 4), nn.AdaptiveAvgPool2d(1),
        )
        self.out_dim = base * 4

    def forward(self, x):           # (B, C, H, W) -> (B, out_dim)
        return self.net(x).flatten(1)


class FireSmokeNet(nn.Module):
    """(B, T, C, H, W) -> multi-label logits + flicker-frequency estimate."""

    def __init__(self, cfg: FireNetConfig = FireNetConfig()):
        super().__init__()
        self.cfg = cfg
        self.encoder = FrameEncoder(cfg.in_ch, cfg.base)
        self.gru = nn.GRU(self.encoder.out_dim, cfg.gru_hidden, batch_first=True)
        self.head = nn.Linear(cfg.gru_hidden, cfg.n_classes)
        self.flicker = nn.Linear(cfg.gru_hidden, 1)   # Hz estimate for Strouhal consistency

    def forward(self, x):           # x: (B, T, C, H, W)
        B, T, C, H, W = x.shape
        feats = self.encoder(x.reshape(B * T, C, H, W)).reshape(B, T, -1)
        seq, hN = self.gru(feats)
        h = hN.squeeze(0)
        logits = self.head(h)
        flick = torch.relu(self.flicker(h)).squeeze(-1)
        return {"logits": logits, "prob": torch.sigmoid(logits), "flicker_hz": flick}

    def loss(self, out: dict, targets, plume_size_m=None, pos_weight=None) -> dict:
        bce = nn.functional.binary_cross_entropy_with_logits(
            out["logits"], targets.float(), pos_weight=pos_weight)
        total = bce
        strou = torch.tensor(0.0, device=out["logits"].device)
        if self.cfg.strouhal_weight > 0 and plume_size_m is not None:   # Class-C, gated
            strou = strouhal_consistency_loss(out["flicker_hz"], plume_size_m)
            total = total + self.cfg.strouhal_weight * strou
        return {"loss": total, "bce": bce.detach(), "strouhal": strou.detach()}
