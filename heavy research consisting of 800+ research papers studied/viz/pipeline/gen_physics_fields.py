#!/usr/bin/env python
"""viz/pipeline/gen_physics_fields.py  —  L6 SIMULATED physics fields from the REAL trinetra numpy core.

Honesty contract (mission HARD RULES):
  * Every value here is COMPUTED by running our own `trinetra/` physics code with EXPLICIT parameters.
  * This is SIMULATED output, never an observation and never a measured skill. The emitted JSON carries
    "kind":"SIMULATED", the exact parameters, the model function names, and a scenario-location disclaimer.
  * The scenario ignition point is an ILLUSTRATIVE location inside the AOI, NOT a claim that a real fire was
    at that coordinate. Real fire locations come from FIRMS (a separate REAL layer, L5).

Run (sandbox-verified interpreter):
  python viz/pipeline/gen_physics_fields.py
Writes: viz/render/public/data/l6_physics.json  (small, browser-fetchable by the Cesium app).
"""
from __future__ import annotations

import json
import math
import os
import sys
from datetime import datetime, timezone

import numpy as np

# --- import the REAL project physics (numpy-only, runs in this sandbox) ---------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.abspath(os.path.join(HERE, "..", ".."))
TRINETRA_SRC = os.path.join(WORKSPACE, "trinetra", "src")
sys.path.insert(0, TRINETRA_SRC)

from trinetra.ws1a_firephys import established_ef as ef  # noqa: E402
from trinetra.ws1b_geophys import fs as geo_fs            # noqa: E402
from trinetra.ws1b_geophys import iverson                 # noqa: E402
from trinetra.ws1b_geophys import caine                   # noqa: E402

OUT = os.path.join(WORKSPACE, "viz", "render", "public", "data", "l6_physics.json")

# AOI (Uttarakhand Himalaya 2021 forest-fire season) — illustrative scenario ignition point (AOI-interior).
AOI = {"bbox": [78.5, 29.5, 80.2, 30.8], "name": "Uttarakhand Himalaya 2021 pre-monsoon fire season"}
IGNITION = {"lon": 79.30, "lat": 30.10, "note": "ILLUSTRATIVE scenario point inside AOI; NOT a real fire coord"}


def fire_plume():
    """Heskestad plume + flame-height + puffing + Byram regime for a physically sane forest-fire scenario."""
    T_inf = 293.0          # K  (~20 C ambient)
    Q_c_total = 50_000.0   # kW total convective HRR (50 MW moderate forest-fire segment)
    D_m = 10.0             # m  effective fire-source diameter (keeps Heskestad flame height physical)
    U_ms = 5.0             # m/s near-surface wind (ERA5-Land-scale; see L4)
    Q_c_per_m = 1000.0     # kW/m convective HRR per unit fire-line length (50 MW over ~50 m line)
    kappa_sigma = 0.05     # 1/m smoke extinction coefficient (illustrative)

    L_flame = ef.flame_height_heskestad(Q_c_total, D_m)      # m
    f_puff = ef.strouhal_puffing_frequency(D_m)              # Hz
    N_c = ef.byram_convection_number(Q_c_per_m, U_ms)        # dimensionless (>~2 plume, <~1 wind-driven)

    # vertical centerline excess-temperature profile dT0(z) in the far field (z > flame height)
    z = np.linspace(max(L_flame, 1.0) + 1.0, 300.0, 60)
    dT = np.array([ef.plume_centerline_dT(Q_c_total, float(zi), z0_m=0.0, T_inf=T_inf) for zi in z])
    T = T_inf + dT                                           # K
    # cumulative smoke transmittance along the rising column (Beer-Lambert over path length from source)
    tau = np.array([ef.beer_lambert_transmittance(kappa_sigma, float(zi)) for zi in z])
    smoke_opacity = (1.0 - tau)                              # 0..1, used for volume opacity

    return {
        "kind": "SIMULATED",
        "models": ["Heskestad plume_centerline_dT", "flame_height_heskestad",
                   "strouhal_puffing_frequency", "byram_convection_number", "beer_lambert_transmittance"],
        "module": "trinetra.ws1a_firephys.established_ef",
        "params": {"T_inf_K": T_inf, "Q_c_total_kW": Q_c_total, "D_m": D_m, "U_ms": U_ms,
                   "Q_c_per_m_kW": Q_c_per_m, "kappa_sigma_per_m": kappa_sigma},
        "scalars": {"flame_height_m": round(float(L_flame), 3),
                    "puffing_frequency_Hz": round(float(f_puff), 4),
                    "byram_convection_number": round(float(N_c), 4),
                    "regime": "plume-dominated" if N_c > 2 else ("wind-dominated" if N_c < 1 else "transitional")},
        "profile": {"units": {"z": "m AGL", "dT": "K", "T": "K", "smoke_opacity": "0-1"},
                    "z": [round(float(v), 2) for v in z],
                    "dT": [round(float(v), 4) for v in dT],
                    "T": [round(float(v), 3) for v in T],
                    "smoke_opacity": [round(float(v), 4) for v in smoke_opacity]},
        "colormap": "inferno (temperature); low-chroma + opacity (smoke)",
    }


def landslide_fs():
    """Infinite-slope Factor of Safety vs slope angle, dry vs a rainfall scenario (Iverson transient head)."""
    c_prime, phi_prime, gamma, z_depth = 5.0, 32.0, 18.0, 2.0  # kPa, deg, kN/m3, m
    # rainfall scenario -> Iverson transient pressure head -> pore pressure
    D0, K_z, I_z, t_s = 1e-4, 1e-5, 5e-6, 6 * 3600.0           # m2/s, m/s, m/s, s (6 h of rain)
    beta = np.arange(10.0, 46.0, 1.0)                          # slope angle grid [deg]

    fs_dry, fs_wet, uw_list = [], [], []
    for b in beta:
        psi = float(iverson.transient_head(z_depth, t_s, D0, K_z, I_z, float(b)))  # m head
        u_w = float(geo_fs.pore_pressure_from_head(psi))                            # kPa
        fs_d = float(geo_fs.factor_of_safety(c_prime, phi_prime, gamma, z_depth, float(b), u_w=0.0))
        fs_w = float(geo_fs.factor_of_safety(c_prime, phi_prime, gamma, z_depth, float(b), u_w=u_w))
        fs_dry.append(round(fs_d, 4)); fs_wet.append(round(fs_w, 4)); uw_list.append(round(u_w, 4))

    # Caine (1980) I-D threshold exceedance — a,b REQUIRE LOCAL CALIBRATION; values here are ILLUSTRATIVE ONLY.
    a_illus, b_illus = 14.82, 0.39   # illustrative placeholder coefficients (NOT locally calibrated)
    I_scn, D_scn = 8.0, 6.0          # mm/h over 6 h scenario
    exceeded, ratio = caine.caine_exceedance(I_scn, D_scn, a_illus, b_illus)

    return {
        "kind": "SIMULATED",
        "models": ["fs.factor_of_safety", "iverson.transient_head", "caine.caine_exceedance"],
        "module": "trinetra.ws1b_geophys",
        "params": {"c_prime_kPa": c_prime, "phi_prime_deg": phi_prime, "gamma_kN_m3": gamma,
                   "z_depth_m": z_depth, "D0_m2_s": D0, "K_z_m_s": K_z, "I_z_m_s": I_z, "rain_hours": 6},
        "fs_vs_slope": {"units": {"beta": "deg", "FS": "dimensionless (<1 unstable)", "u_w": "kPa"},
                        "beta_deg": [float(b) for b in beta],
                        "FS_dry": fs_dry, "FS_wet": fs_wet, "pore_pressure_kPa": uw_list},
        "caine": {"a_b_status": "ILLUSTRATIVE placeholder coefficients — NOT locally calibrated (see caine.py)",
                  "a": a_illus, "b": b_illus, "scenario_I_mm_h": I_scn, "scenario_D_h": D_scn,
                  "threshold_exceeded": bool(exceeded), "I_over_Ithreshold": round(float(ratio), 4)},
        "colormap": "viridis (FS / risk); translucent band for uncertainty",
    }


def main():
    doc = {
        "provenance": {
            "layer": "L6 — WS1 physics + fusion",
            "kind": "SIMULATED",
            "origin": "Computed by running the REAL TRINETRA numpy physics core (trinetra/src).",
            "disclaimer": "SIMULATED physics fields with explicit parameters. NOT an observation, NOT a "
                          "measured model skill. No model was trained (see FINAL_REPORT.md).",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "generator": "viz/pipeline/gen_physics_fields.py",
            "aoi": AOI, "ignition_point": IGNITION,
        },
        "fire_plume": fire_plume(),
        "landslide": landslide_fs(),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
    s = doc["fire_plume"]["scalars"]
    print("wrote", OUT)
    print(f"  fire: flame_height={s['flame_height_m']} m, puffing={s['puffing_frequency_Hz']} Hz, "
          f"Nc={s['byram_convection_number']} ({s['regime']})")
    ls = doc["landslide"]["fs_vs_slope"]
    print(f"  landslide: FS_dry[10deg]={ls['FS_dry'][0]} FS_wet[10deg]={ls['FS_wet'][0]} ... "
          f"FS_wet[45deg]={ls['FS_wet'][-1]}")
    print(f"  caine: exceeded={doc['landslide']['caine']['threshold_exceeded']} "
          f"ratio={doc['landslide']['caine']['I_over_Ithreshold']}")


if __name__ == "__main__":
    main()
