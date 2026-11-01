"""ws1a_firephys.established_ef — established fire-physics blocks (Class A). M1.

A faithful, computable SUBSET of the EF-01..EF-20 inventory (DESIGN + ws1_physics/*_P21.md). Each function
is Class A and carries [coeff-verify] where a literature coefficient must be confirmed against a primary
source (SFPE Handbook / Heskestad / McCaffrey) before driving any live output.
"""
from __future__ import annotations

import math

import numpy as np

STEFAN_BOLTZMANN = 5.670374419e-8  # W m^-2 K^-4


def flame_height_heskestad(Q_kW: float, D_m: float) -> float:
    """Mean flame height L [m].  L = 0.235 * Q^(2/5) - 1.02 * D   (Heskestad). [coeff-verify] EF."""
    return 0.235 * (Q_kW ** 0.4) - 1.02 * D_m


def strouhal_puffing_frequency(D_m: float) -> float:
    """Pool-fire puffing frequency f [Hz] ~ 1.5 * D^(-1/2) (EF-16). [coeff-verify]."""
    return 1.5 / math.sqrt(D_m)


def plume_centerline_dT(Q_c_kW: float, z_m: float, z0_m: float = 0.0, T_inf: float = 293.0) -> float:
    """Heskestad centerline excess temperature dT0 [K] in the far field (z>flame). [coeff-verify] EF.

    dT0 = 9.1 * (T_inf / (g * cp^2 * rho_inf^2))^(1/3) * Q_c^(2/3) * (z - z0)^(-5/3)
    """
    g, cp, rho = 9.81, 1.0, 1.2
    dz = max(z_m - z0_m, 1e-6)
    return 9.1 * (T_inf / (g * cp ** 2 * rho ** 2)) ** (1.0 / 3.0) * (Q_c_kW ** (2.0 / 3.0)) * dz ** (-5.0 / 3.0)


def byram_convection_number(Q_c_kW_per_m: float, U_ms: float, rho: float = 1.2, cp: float = 1.0,
                            T_inf: float = 293.0, g: float = 9.81) -> float:
    """Dimensionless Byram convection number N_c ~ buoyant power / flow power (EF-13 regime check).

    N_c > ~2 => plume-dominated (buoyant); N_c < ~1 => wind-dominated. Used to reject non-fire regimes.
    """
    denom = rho * cp * T_inf * (U_ms ** 3)
    if denom <= 0:
        return float("inf")
    return (2.0 * g * Q_c_kW_per_m) / denom


def graybody_radiance(T_K: float, emissivity: float = 1.0) -> float:
    """Stefan-Boltzmann gray-body radiant exitance [W/m^2] used as an IR-radiance proxy (EF-14 context)."""
    return emissivity * STEFAN_BOLTZMANN * T_K ** 4


def graybody_temperature(radiance: float, emissivity: float = 1.0) -> float:
    """Invert gray-body radiance to temperature [K]."""
    r = max(radiance, 0.0)
    return (r / (emissivity * STEFAN_BOLTZMANN)) ** 0.25


def beer_lambert_transmittance(kappa_sigma: float, path_m: float) -> float:
    """Smoke/soot transmittance tau = exp(-(kappa+sigma)*L) (EF-14/EF-15 simplified)."""
    return math.exp(-kappa_sigma * path_m)
