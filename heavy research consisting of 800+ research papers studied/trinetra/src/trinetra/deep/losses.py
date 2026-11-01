"""trinetra.deep.losses — physics-informed + honesty-aware training losses (train on Kaggle).

The physics-informed terms encode Class-A equations as soft constraints (PDE residuals / dimensionless
consistency). They regularize the data loss; they do NOT replace the hard deterministic physics gate, which
still runs at inference (ws1b_geophys / ws1a_firephys). Novel Class-C physics terms are gated by a weight
that defaults to 0 (Rule 20).
"""
from __future__ import annotations

import math

import torch
import torch.nn.functional as F


def richards_iverson_residual(psi, Z, t, D1: float):
    """PDE residual of the linearized Iverson/Richards diffusion:  psi_t - D1 * psi_ZZ = 0.

    psi: (N,1) network output; Z,t: (N,1) inputs with requires_grad=True. Slope enters ONLY via D1
    (bug-guard mirrored from the numpy gate). Returns the residual tensor for an MSE penalty.
    """
    psi_t = torch.autograd.grad(psi, t, torch.ones_like(psi), create_graph=True, retain_graph=True)[0]
    psi_Z = torch.autograd.grad(psi, Z, torch.ones_like(psi), create_graph=True, retain_graph=True)[0]
    psi_ZZ = torch.autograd.grad(psi_Z, Z, torch.ones_like(psi_Z), create_graph=True, retain_graph=True)[0]
    return psi_t - D1 * psi_ZZ


def factor_of_safety_torch(c_prime, phi_deg, gamma, z, beta_deg, u_w, sigma_s=0.0):
    """Differentiable infinite-slope FS (matches ws1b_geophys.fs). Enables an 'FS<1 => high risk' penalty."""
    beta = math.radians(beta_deg) if isinstance(beta_deg, (int, float)) else torch.deg2rad(beta_deg)
    phi = math.radians(phi_deg) if isinstance(phi_deg, (int, float)) else torch.deg2rad(phi_deg)
    sinb = math.sin(beta) if isinstance(beta, float) else torch.sin(beta)
    cosb = math.cos(beta) if isinstance(beta, float) else torch.cos(beta)
    tanp = math.tan(phi) if isinstance(phi, float) else torch.tan(phi)
    denom = gamma * z * sinb * cosb
    sigma_n_eff = gamma * z * cosb ** 2 - u_w + sigma_s
    return (c_prime + sigma_n_eff * tanp) / denom


def strouhal_consistency_loss(pred_flicker_hz, plume_size_m, coeff: float = 1.5):
    """Penalize predicted flicker that deviates from Strouhal f ~ coeff / sqrt(D) (fire aux, Class A)."""
    target = coeff / torch.sqrt(torch.clamp(plume_size_m, min=1e-3))
    return F.mse_loss(pred_flicker_hz, target)


def deep_svdd_loss(z, center):
    """Deep SVDD: minimize squared distance of embeddings to a fixed hypersphere center c."""
    return torch.mean(torch.sum((z - center) ** 2, dim=1))


def cost_sensitive_bce(logits, targets, c_fa: float, c_miss: float, eps: float = 1e-7):
    """Cost-sensitive BCE: misses weighted by C_miss, false alarms by C_FA (aligns training to the
    decision cost-loss used in eval/). Keeps the learner honest about the asymmetric cost."""
    p = torch.sigmoid(logits).clamp(eps, 1 - eps)
    pos = -c_miss * targets * torch.log(p)             # penalize missing an event
    neg = -c_fa * (1 - targets) * torch.log(1 - p)     # penalize false alarm
    return torch.mean(pos + neg)


def brier_score(prob, targets):
    """Brier score (calibration-friendly proper scoring rule)."""
    return torch.mean((prob - targets) ** 2)
