"""ws1b_geophys.gate — geo physics gate: combine FS / Iverson / Fukuzono / Caine into one advisory
ExpertOutput (Class A/B). DESIGN/LLD.md §2, COMPONENT_DESIGN.md §5.

Transparent, monotone mappings only (no learned weights here — fusion/RL live in ws5). The gate NEVER
emits a public alert; it produces a probability + consistency for the fusion head.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..common.types import ExpertOutput, PhysicsClass
from .caine import caine_exceedance
from .fs import factor_of_safety, pore_pressure_from_head
from .fukuzono import FukuzonoFit
from .iverson import pressure_head


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


@dataclass
class GeoInputs:
    # slope/soil
    c_prime: float; phi_prime_deg: float; gamma: float; z: float; beta_deg: float
    sigma_s: float = 0.0
    # Iverson infiltration (optional; if provided, drives u_w)
    D0: float | None = None; K_z: float | None = None; I_z: float | None = None
    t_hours: float | None = None; psi_steady: float = 0.0
    u_w: float = 0.0
    # rainfall I-D
    I_mm_h: float | None = None; D_hours: float | None = None
    caine_a: float = 14.0; caine_b: float = 0.39
    # creep monitoring
    fukuzono: FukuzonoFit | None = None; now_hours: float | None = None


@dataclass
class GeoResult:
    FS: float
    caine_ratio: float | None
    t_failure: float | None
    p_phys: float
    expert: ExpertOutput


def geo_gate(gi: GeoInputs, k_fs: float = 4.0) -> GeoResult:
    # 1) pore pressure: from Iverson transient head if infiltration given, else supplied u_w
    u_w = gi.u_w
    if gi.D0 is not None and gi.K_z and gi.I_z is not None and gi.t_hours is not None:
        psi = float(pressure_head(gi.z, gi.t_hours, gi.D0, gi.K_z, gi.I_z, gi.beta_deg, gi.psi_steady))
        u_w = float(pore_pressure_from_head(psi))

    FS = float(factor_of_safety(gi.c_prime, gi.phi_prime_deg, gi.gamma, gi.z, gi.beta_deg,
                                u_w=u_w, sigma_s=gi.sigma_s))
    p_fs = float(_sigmoid(k_fs * (1.0 - FS)))        # FS=1 -> 0.5 ; FS<1 -> >0.5

    # 2) Caine I-D exceedance (soft)
    caine_ratio = None; p_caine = 0.0
    if gi.I_mm_h is not None and gi.D_hours is not None:
        _, ratio = caine_exceedance(gi.I_mm_h, gi.D_hours, gi.caine_a, gi.caine_b)
        caine_ratio = float(ratio)
        p_caine = float(np.clip((caine_ratio - 0.5), 0.0, 1.0))

    # 3) Fukuzono proximity to failure (soft)
    t_f = None; p_fk = 0.0
    if gi.fukuzono is not None and gi.now_hours is not None and np.isfinite(gi.fukuzono.t_failure):
        t_f = float(gi.fukuzono.t_failure)
        lead = t_f - gi.now_hours
        if lead > 0:
            p_fk = float(np.clip(1.0 - lead / 48.0, 0.0, 1.0)) * float(np.clip(gi.fukuzono.r2, 0, 1))

    # Conservative fusion of physics sub-signals: noisy-OR keeps it monotone and never under-warns.
    comps = [p_fs, p_caine, p_fk]
    p_phys = float(1.0 - np.prod([1.0 - c for c in comps]))

    # Consistency: do the independent physics signals agree? (used by NF-1 downstream)
    active = [c for c in comps if c > 0]
    c_consistency = float(1.0 - np.std(active)) if len(active) >= 2 else 1.0
    c_consistency = float(np.clip(c_consistency, 0.0, 1.0))

    expert = ExpertOutput(
        p=float(np.clip(p_phys, 0.0, 1.0)), source="geo_phys",
        u=float(np.clip(0.5 * (1 - c_consistency) + 0.1, 0.0, 1.0)),
        c=c_consistency, r=1.0, cls=PhysicsClass.A,
    )
    return GeoResult(FS=FS, caine_ratio=caine_ratio, t_failure=t_f, p_phys=p_phys, expert=expert)
