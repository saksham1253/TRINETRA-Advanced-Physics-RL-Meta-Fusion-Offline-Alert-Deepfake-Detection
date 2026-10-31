"""trinetra.deep.deepfake_net — Model 5: two-stream media authenticity detector (Class data, LOW trust, ws2).

Spatial stream (RGB) + frequency stream (2D-FFT log-magnitude, which exposes GAN/upsampling fingerprints)
are fused into an authenticity logit. This is the LEAST-trusted expert: at inference it enters fusion with
a small reliability r and can NEVER gate a life-safety alert (Rule 19). It only corroborates/suppresses the
confidence attached to media-sourced reports (e.g. crowd-submitted clips).
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn

from .layers import ConvBNAct


@dataclass
class DeepfakeConfig:
    in_ch: int = 3
    base: int = 32
    max_reliability: float = 0.4    # hard cap on trust surfaced to fusion (Rule 19)


def _fft_logmag(x):
    """2D FFT log-magnitude per channel (frequency-domain fingerprint stream)."""
    f = torch.fft.fft2(x, norm="ortho")
    mag = torch.log1p(torch.abs(torch.fft.fftshift(f, dim=(-2, -1))))
    return mag


class _Stream(nn.Module):
    def __init__(self, in_ch, base):
        super().__init__()
        self.net = nn.Sequential(
            ConvBNAct(in_ch, base), nn.MaxPool2d(2),
            ConvBNAct(base, base * 2), nn.MaxPool2d(2),
            ConvBNAct(base * 2, base * 4), nn.AdaptiveAvgPool2d(1))
        self.out_dim = base * 4

    def forward(self, x):
        return self.net(x).flatten(1)


class AuthenticityNet(nn.Module):
    """Returns p_fake (prob the media is manipulated). Trust surfaced to fusion is capped."""

    def __init__(self, cfg: DeepfakeConfig = DeepfakeConfig()):
        super().__init__()
        self.cfg = cfg
        self.spatial = _Stream(cfg.in_ch, cfg.base)
        self.freq = _Stream(cfg.in_ch, cfg.base)
        self.head = nn.Sequential(
            nn.Linear(self.spatial.out_dim + self.freq.out_dim, 128), nn.SiLU(),
            nn.Dropout(0.3), nn.Linear(128, 1))

    def forward(self, x):           # x: (B, C, H, W) in [0,1]
        s = self.spatial(x)
        fr = self.freq(_fft_logmag(x))
        logit = self.head(torch.cat([s, fr], dim=1))
        p_fake = torch.sigmoid(logit).squeeze(-1)
        return {"logit": logit.squeeze(-1), "p_fake": p_fake}

    def loss(self, out, is_fake_targets):
        return nn.functional.binary_cross_entropy_with_logits(out["logit"], is_fake_targets.float())
