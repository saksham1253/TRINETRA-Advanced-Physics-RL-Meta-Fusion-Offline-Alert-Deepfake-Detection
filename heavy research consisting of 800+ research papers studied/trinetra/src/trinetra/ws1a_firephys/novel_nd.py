"""ws1a_firephys.novel_nd — NOVEL fire-physics candidates (Class C, UNVALIDATED). M1.

Rule 20/21: these are hypotheses NOT found in our limited search; they are DEFAULT-OFF (configs/firephys)
and, when used, enter fusion only as SOFT features with a Class-A fallback and a visible class flag.
Nothing here is claimed to work or to beat anything. Each returns a value + an uncertainty that GROWS as
conditions degrade, so the system fails toward "uncertain" (Rule 19).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .established_ef import graybody_radiance, graybody_temperature, strouhal_puffing_frequency


# ---------------------------------------------------------------- ND-1 de-aliased flicker
def aliased_frequency(f_true_hz: float, fs_hz: float) -> float:
    """Frequency a true flicker f_true appears at when sampled at fs (fs may be < 2*f_true)."""
    if fs_hz <= 0:
        raise ValueError("fs must be > 0")
    k = round(f_true_hz / fs_hz)
    return abs(f_true_hz - fs_hz * k)


@dataclass
class ND1Result:
    f_true_pred_hz: float
    f_alias_pred_hz: float
    consistency: float      # in [0,1]; how well observed aliased peak matches a Strouhal prediction
    cls: str = "C"


def nd1_dealiased_flicker(f_obs_hz: float, fs_hz: float, D_prior_m: float,
                          sigma_hz: float = 0.3) -> ND1Result:
    """Given an observed (possibly aliased) flicker peak on a low-fps camera, test consistency with the
    Strouhal-predicted true flicker for a plume of size D_prior. Returns a soft consistency, NOT a trigger.
    """
    f_pred = strouhal_puffing_frequency(D_prior_m)
    f_alias_pred = aliased_frequency(f_pred, fs_hz)
    consistency = float(math.exp(-((f_obs_hz - f_alias_pred) ** 2) / (2.0 * sigma_hz ** 2)))
    return ND1Result(f_true_pred_hz=f_pred, f_alias_pred_hz=f_alias_pred, consistency=consistency)


# ---------------------------------------------------------------- ND-2 smoke-transmittance temperature
@dataclass
class ND2Result:
    T_fire_hat_K: float
    sigma_K: float          # uncertainty; GROWS as transmittance tau_s -> 0 (ill-conditioned)
    cls: str = "C"


def nd2_transmittance_temperature(L_obs: float, tau_s: float, T_smoke_K: float,
                                  emissivity: float = 1.0, sigma_L_frac: float = 0.05) -> ND2Result:
    """Recover true plume temperature behind smoke from observed radiance.

    Model:  L_obs = tau_s * B(T_fire) + (1 - tau_s) * B(T_smoke)   =>   B(T_fire) = (L_obs - (1-tau_s)B_smoke)/tau_s
    Uncertainty is propagated and BLOWS UP as tau_s -> 0 (fail-safe to 'uncertain').
    """
    tau_s = float(np.clip(tau_s, 1e-3, 1.0))
    B_smoke = graybody_radiance(T_smoke_K, emissivity)
    B_fire = (L_obs - (1.0 - tau_s) * B_smoke) / tau_s
    T_fire = graybody_temperature(B_fire, emissivity)
    # dT/dL = (1/(4 e sigma T^3)); observed-radiance error ~ sigma_L_frac*L_obs, amplified by 1/tau_s
    dL = sigma_L_frac * abs(L_obs) / tau_s
    denom = max(4.0 * emissivity * 5.670374419e-8 * T_fire ** 3, 1e-12)
    sigma_K = dL / denom
    return ND2Result(T_fire_hat_K=T_fire, sigma_K=float(sigma_K))


# ---------------------------------------------------------------- ND-3 dimensionless ignition index
def nd3_ignition_index(terms: list[tuple[float, float, float]]) -> float:
    """Pi_ig = sum_i w_i * scale_i * rate_i, a scene-invariant early-warning scalar.

    `terms` = list of (weight w_i, dimensionless scale_i = t*/X_i*, normalized rate_i = dX_i/dt).
    Returns a non-negative index; higher => faster coordinated heat/gas/radiation rise. Soft feature only.
    """
    val = sum(w * s * r for (w, s, r) in terms)
    return float(max(val, 0.0))
