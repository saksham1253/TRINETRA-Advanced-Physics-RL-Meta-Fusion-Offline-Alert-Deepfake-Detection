"""trinetra.deep.geo_pinn — Model 1: physics-informed slope-hydrology network (Class A/B, ws1b).

A PINN that learns the transient pressure-head field psi(Z, t; forcing, soil) under the linearized
Iverson/Richards diffusion, then maps the physical state to a calibrated landslide-probability expert.

Why PINN: labels (actual failures) are scarce; the PDE residual + FS physics supply a dense, label-free
training signal that keeps the network on the physically admissible manifold and improves extrapolation to
unseen rainfall forcing. Slope angle enters ONLY through D1 = D0 / cos^2(beta) (bug-guard mirrored from the
deterministic gate). The hard FS<1 gate still runs at inference; this network is corroborating evidence.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn

from .layers import MLP
from .losses import richards_iverson_residual, factor_of_safety_torch


@dataclass
class GeoPINNConfig:
    n_static: int = 6          # c', phi, gamma, z, beta, susceptibility
    hidden: tuple = (128, 128, 128)
    dropout: float = 0.0
    physics_weight: float = 1.0
    fs_weight: float = 0.5
    data_weight: float = 1.0


class GeoPINN(nn.Module):
    """psi(Z, t) field net conditioned on static slope features; plus a risk head on the physical state."""

    def __init__(self, cfg: GeoPINNConfig = GeoPINNConfig()):
        super().__init__()
        self.cfg = cfg
        # field network: inputs [Z, t, rain_intensity] + static -> psi
        self.field = MLP([3 + cfg.n_static, *cfg.hidden, 1], norm=True, dropout=cfg.dropout)
        # risk head: [psi, psi normalized, FS, static] -> landslide logit
        self.risk = MLP([2 + 1 + cfg.n_static, 64, 32, 1], norm=True, dropout=cfg.dropout)

    def psi(self, Z, t, rain, static):
        return self.field(torch.cat([Z, t, rain, static], dim=1))

    def forward(self, Z, t, rain, static):
        psi = self.psi(Z, t, rain, static)
        # FS from the differentiable infinite-slope eq. using predicted pore pressure u_w = gamma_w * psi
        gamma_w = 9.81
        c_prime, phi_deg, gamma, z, beta_deg = (static[:, i:i + 1] for i in range(5))
        u_w = gamma_w * torch.clamp(psi, min=0.0)
        fs = factor_of_safety_torch(c_prime, phi_deg, gamma, z, beta_deg, u_w)
        feats = torch.cat([psi, torch.tanh(psi), fs, static], dim=1)
        logit = self.risk(feats)
        return {"logit": logit, "prob": torch.sigmoid(logit), "psi": psi, "fs": fs}

    def physics_loss(self, Z, t, rain, static, D1):
        """PDE residual MSE + 'FS<1 should map to high risk' hinge. Z,t must require grad."""
        psi = self.psi(Z, t, rain, static)
        res = richards_iverson_residual(psi, Z, t, D1)
        pde = torch.mean(res ** 2)

        out = self.forward(Z, t, rain, static)
        # hinge: when FS<1, risk prob should be high (physics-anchored supervision, label-free)
        unstable = (out["fs"] < 1.0).float()
        fs_pen = torch.mean(unstable * (1.0 - out["prob"]) ** 2)
        return self.cfg.physics_weight * pde + self.cfg.fs_weight * fs_pen


def geo_pinn_step(model: GeoPINN, batch: dict, D1: float, bce: nn.Module) -> dict:
    """One optimization objective: data BCE (where labels exist) + physics residual. Returns loss dict.

    Z,t are rebuilt as leaf tensors via detach().requires_grad_(True) so autograd.grad works in BOTH the
    single-GPU path AND under DataParallel (where the scattered input is a NON-leaf and requires_grad_ on it
    would raise). This is what makes the PINN safe to train on Kaggle T4 x2."""
    Z = batch["Z"].detach().requires_grad_(True)
    t = batch["t"].detach().requires_grad_(True)
    rain, static = batch["rain"], batch["static"]
    out = model(Z, t, rain, static)

    phys = model.physics_loss(Z, t, rain, static, D1)
    loss = model.cfg.physics_weight * phys
    if "label" in batch and batch["label"] is not None:
        data = model.cfg.data_weight * bce(out["logit"].squeeze(-1), batch["label"].float())
        loss = loss + data
    else:
        data = torch.tensor(0.0, device=loss.device)
    return {"loss": loss, "data": data.detach(), "physics": phys.detach(), "prob": out["prob"].detach()}
