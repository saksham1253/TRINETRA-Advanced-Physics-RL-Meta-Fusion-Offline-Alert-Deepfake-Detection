"""ws1b_geophys.fs — infinite-slope Factor of Safety (Class A). DESIGN/LLD.md §2, M1.

FS = [ c' + (sigma'_n) * tan(phi') ] / ( gamma * z * sin(beta) * cos(beta) )
with effective normal stress   sigma'_n = gamma * z * cos^2(beta) - u_w + sigma_s
where sigma_s >= 0 is suction (apparent-cohesion) stress that VANISHES at saturation (Se->1 => sigma_s->0),
recovering the classic saturated effective-stress infinite-slope form.

Correctness invariants (tests/physics_golden): FS strictly increasing in suction sigma_s; at sigma_s=0 FS
equals the saturated form; FS decreases as pore pressure u_w rises.
"""
from __future__ import annotations

import numpy as np

GAMMA_W = 9.81  # kN/m^3, unit weight of water


def pore_pressure_from_head(psi_m: float | np.ndarray, gamma_w: float = GAMMA_W):
    """Pore water pressure u_w [kPa] from pressure head psi [m]. Positive head => positive u_w."""
    return gamma_w * np.asarray(psi_m, dtype=float)


def factor_of_safety(
    c_prime: float,        # effective cohesion [kPa]
    phi_prime_deg: float,  # effective friction angle [deg]
    gamma: float,          # soil unit weight [kN/m^3]
    z: float,              # vertical depth to slip surface [m]
    beta_deg: float,       # slope angle [deg]
    u_w: float = 0.0,      # pore water pressure [kPa]
    sigma_s: float = 0.0,  # suction stress [kPa], >=0, ->0 at saturation
):
    """Return FS (dimensionless). FS<1 => unstable. Pure numpy; array-broadcastable."""
    beta = np.radians(beta_deg)
    phi = np.radians(phi_prime_deg)
    denom = gamma * z * np.sin(beta) * np.cos(beta)
    if np.any(denom <= 0):
        raise ValueError("driving stress must be positive (check gamma,z,beta>0)")
    sigma_n_eff = gamma * z * np.cos(beta) ** 2 - u_w + sigma_s
    return (c_prime + sigma_n_eff * np.tan(phi)) / denom


def factor_of_safety_saturated(c_prime, phi_prime_deg, gamma, z, beta_deg, u_w=0.0):
    """Saturated form (sigma_s = 0) — the limit the general form must reproduce (golden test)."""
    return factor_of_safety(c_prime, phi_prime_deg, gamma, z, beta_deg, u_w=u_w, sigma_s=0.0)
