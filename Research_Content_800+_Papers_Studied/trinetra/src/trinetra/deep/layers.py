"""trinetra.deep.layers — reusable torch building blocks (train on Kaggle)."""
from __future__ import annotations

import torch
import torch.nn as nn


class MLP(nn.Module):
    """Configurable MLP with SiLU + optional layernorm/dropout."""

    def __init__(self, sizes: list[int], act=nn.SiLU, norm: bool = False, dropout: float = 0.0,
                 out_act: nn.Module | None = None):
        super().__init__()
        layers: list[nn.Module] = []
        for i in range(len(sizes) - 1):
            layers.append(nn.Linear(sizes[i], sizes[i + 1]))
            if i < len(sizes) - 2:
                if norm:
                    layers.append(nn.LayerNorm(sizes[i + 1]))
                layers.append(act())
                if dropout > 0:
                    layers.append(nn.Dropout(dropout))
        if out_act is not None:
            layers.append(out_act)
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


class Chomp1d(nn.Module):
    """Trim right padding so a causal conv stays causal (no look-ahead -> no temporal leakage)."""

    def __init__(self, chomp: int):
        super().__init__()
        self.chomp = chomp

    def forward(self, x):
        return x[:, :, : -self.chomp].contiguous() if self.chomp > 0 else x


class TemporalBlock(nn.Module):
    """Dilated causal conv block (TCN). Causal => respects the anti-leak invariant (gate G6)."""

    def __init__(self, c_in: int, c_out: int, kernel: int, dilation: int, dropout: float = 0.1):
        super().__init__()
        pad = (kernel - 1) * dilation
        self.conv1 = nn.utils.weight_norm(nn.Conv1d(c_in, c_out, kernel, padding=pad, dilation=dilation))
        self.chomp1 = Chomp1d(pad)
        self.conv2 = nn.utils.weight_norm(nn.Conv1d(c_out, c_out, kernel, padding=pad, dilation=dilation))
        self.chomp2 = Chomp1d(pad)
        self.act = nn.SiLU()
        self.drop = nn.Dropout(dropout)
        self.down = nn.Conv1d(c_in, c_out, 1) if c_in != c_out else None

    def forward(self, x):
        y = self.drop(self.act(self.chomp1(self.conv1(x))))
        y = self.drop(self.act(self.chomp2(self.conv2(y))))
        res = x if self.down is None else self.down(x)
        return self.act(y + res)


class TCN(nn.Module):
    """Stack of dilated causal conv blocks -> (B, C_out, T)."""

    def __init__(self, c_in: int, channels: list[int], kernel: int = 3, dropout: float = 0.1):
        super().__init__()
        blocks = []
        prev = c_in
        for i, ch in enumerate(channels):
            blocks.append(TemporalBlock(prev, ch, kernel, dilation=2 ** i, dropout=dropout))
            prev = ch
        self.net = nn.Sequential(*blocks)

    def forward(self, x):   # x: (B, C_in, T)
        return self.net(x)


class ConvBNAct(nn.Module):
    def __init__(self, c_in, c_out, k=3, s=1, p=1):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(c_in, c_out, k, s, p, bias=False), nn.BatchNorm2d(c_out), nn.SiLU())

    def forward(self, x):
        return self.block(x)
