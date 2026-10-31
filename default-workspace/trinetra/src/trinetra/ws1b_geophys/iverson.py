"""ws1b_geophys.iverson — Iverson (2000) transient pressure-head response (Class A). M1.

CRITICAL (bug-guard, DESIGN/LLD.md §2): slope enters the transient term ONLY through the diffusivity
    D1 = D0 / cos^2(beta)
There is NO extra cos^2(beta)/cos(beta) multiplier on the transient term. The core transient response is
    R(Z, t) = sqrt(4 * D1 * t) * ierfc( Z / sqrt(4 * D1 * t) )
and the pressure-head rise for a surface flux I_z (<= K_z) over the wetting period is
    psi_transient(Z, t) = (I_z / K_z) * R(Z, t)
with   ierfc(x) = exp(-x^2)/sqrt(pi) - x * erfc(x).

erfc comes from stdlib `math` (scipy is unavailable here).
"""
from __future__ import annotations

import math

import numpy as np

_erfc = np.vectorize(math.erfc, otypes=[float])


def ierfc(x):
    """Integral of the complementary error function. ierfc(0) = 1/sqrt(pi)."""
    x = np.asarray(x, dtype=float)
    return np.exp(-x * x) / math.sqrt(math.pi) - x * _erfc(x)


def diffusivity_D1(D0: float, beta_deg: float) -> float:
    """D1 = D0 / cos^2(beta). The ONLY place slope enters the transient response."""
    return D0 / (math.cos(math.radians(beta_deg)) ** 2)


def _transient_core(Z, t, D1, I_z, K_z):
    """Slope-free core: callers pass D1 (already slope-adjusted). Guarantees no extra cos(beta)."""
    Z = np.asarray(Z, dtype=float)
    t = np.asarray(t, dtype=float)
    arg = np.sqrt(4.0 * D1 * np.where(t > 0, t, np.nan))
    R = arg * ierfc(np.divide(Z, arg, out=np.full_like(Z * 1.0, 0.0), where=arg > 0))
    R = np.where(t > 0, R, 0.0)
    return (I_z / K_z) * R


def transient_head(Z, t, D0, K_z, I_z, beta_deg):
    """Transient pressure-head rise psi(Z,t) [m]. Slope enters ONLY via D1 = D0/cos^2(beta)."""
    D1 = diffusivity_D1(D0, beta_deg)
    return _transient_core(Z, t, D1, I_z, K_z)


def pressure_head(Z, t, D0, K_z, I_z, beta_deg, psi_steady=0.0):
    """Total head = steady background + transient response."""
    return psi_steady + transient_head(Z, t, D0, K_z, I_z, beta_deg)


def _response_R(Z, tau, D1):
    """Slope-adjusted ierfc response R(Z, tau) = sqrt(4 D1 tau) * ierfc(Z / sqrt(4 D1 tau)); 0 for tau<=0.

    This is the UNIT response (no I/K factor), used as the linear kernel for superposition."""
    Z = np.asarray(Z, float); tau = np.asarray(tau, float)
    arg = np.sqrt(4.0 * D1 * np.where(tau > 0, tau, np.nan))
    R = arg * ierfc(np.divide(Z, arg, out=np.full_like(Z * 1.0 + tau * 0.0, 0.0), where=arg > 0))
    return np.where(tau > 0, R, 0.0)


def transient_head_multipulse(Z, t_eval, step_times, step_intensities, D0, K_z, beta_deg):
    """Transient head for a PIECEWISE-CONSTANT rainfall history, by linear superposition (Iverson/Baum).

    The linearized Iverson response is linear in the surface flux, so a rainfall history expressed as
    absolute-intensity steps {(t_k, I_k)} superposes as

        psi(Z, t) = sum_k ((I_k - I_{k-1}) / K_z) * R(Z, t - t_k) * H(t - t_k),   I_{-1} = 0

    where R is the unit ierfc response and H the step. A FINITE pulse of intensity I over [0, T] is just the
    two steps (0, I) and (T, 0), giving the classic psi = (I/Kz)[R(Z,t) - R(Z,t-T)] recovery after rain
    stops. Slope enters ONLY via D1 = D0/cos^2(beta) (bug-guard preserved).

    Args:
        step_times:       increasing pulse-onset times t_k.
        step_intensities: ABSOLUTE surface flux I_k (<= K_z) active from t_k until the next step.
    Returns psi(Z, t_eval) with the same broadcast shape as Z and t_eval.
    """
    D1 = diffusivity_D1(D0, beta_deg)
    order = np.argsort(np.asarray(step_times, float))
    times = np.asarray(step_times, float)[order]
    inten = np.asarray(step_intensities, float)[order]
    t_eval = np.asarray(t_eval, float)

    psi = np.zeros(np.broadcast(np.asarray(Z, float), t_eval).shape, float)
    i_prev = 0.0
    for tk, ik in zip(times, inten):
        dI = ik - i_prev
        psi = psi + (dI / K_z) * _response_R(Z, t_eval - tk, D1)
        i_prev = ik
    return psi
