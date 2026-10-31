"""ws1a_firephys.gate — fire physics gate: fuse detector confidence with physics plausibility (Class A)
plus optional Class-C soft features (flag-gated). DESIGN/COMPONENT_DESIGN.md §5.

The gate NEVER triggers a public alarm. It emits an advisory ExpertOutput(FIRE) with a physics-consistency
that DOWN-WEIGHTS implausible regimes (e.g. wind-dominated, non-fire) and reports whether any Class-C
feature was used (Rule 20 transparency).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..common.config import Config
from ..common.types import ExpertOutput, PhysicsClass
from .established_ef import byram_convection_number
from .novel_nd import nd1_dealiased_flicker, nd2_transmittance_temperature, nd3_ignition_index


@dataclass
class FireInputs:
    detector_conf: float                 # [0,1] from CCTV detector + temporal validator (WS4)
    multi_node_agree: bool = False       # IoT smoke+heat corroboration (>=2 nodes)
    # physics regime (optional)
    Q_c_kW_per_m: float | None = None
    wind_U_ms: float | None = None
    # Class-C soft features (used only if the matching config flag is on)
    nd1: dict | None = None              # {f_obs_hz, fs_hz, D_prior_m}
    nd2: dict | None = None              # {L_obs, tau_s, T_smoke_K}
    nd3_terms: list | None = None        # [(w, scale, rate), ...]


@dataclass
class FireResult:
    p_fire: float
    consistency: float
    used_classC: bool
    diagnostics: dict = field(default_factory=dict)
    expert: ExpertOutput = None  # type: ignore


def fire_gate(fi: FireInputs, cfg: Config | None = None) -> FireResult:
    cfg = cfg or Config()
    diag: dict = {}
    c = 1.0
    used_c = False

    # (A) Byram regime plausibility — down-weight non-fire / wind-dominated regimes.
    if fi.Q_c_kW_per_m is not None and fi.wind_U_ms is not None:
        N_c = byram_convection_number(fi.Q_c_kW_per_m, max(fi.wind_U_ms, 1e-3))
        diag["byram_Nc"] = N_c
        c *= float(np.clip(N_c / 2.0, 0.3, 1.0))   # Nc>=2 plume-dominated => full consistency

    # (C soft) ND-1 de-aliased flicker consistency
    if fi.nd1 and cfg.get("firephys.nd1", False):
        r = nd1_dealiased_flicker(**fi.nd1); used_c = True
        diag["nd1"] = r.__dict__; c *= float(np.clip(0.5 + 0.5 * r.consistency, 0.5, 1.0))

    # (C soft) ND-2 smoke-transmittance temperature (adds uncertainty if smoke thick)
    extra_u = 0.0
    if fi.nd2 and cfg.get("firephys.nd2", False):
        r = nd2_transmittance_temperature(**fi.nd2); used_c = True
        diag["nd2"] = r.__dict__
        extra_u = float(np.clip(r.sigma_K / 500.0, 0.0, 0.4))  # thicker smoke => more uncertain

    # (C soft) ND-3 ignition index -> small confidence boost only
    p = float(np.clip(fi.detector_conf, 0.0, 1.0))
    if fi.nd3_terms and cfg.get("firephys.nd3", False):
        pi = nd3_ignition_index(fi.nd3_terms); used_c = True
        diag["nd3_pi_ig"] = pi
        p = float(np.clip(p + 0.1 * np.tanh(pi), 0.0, 1.0))

    # IoT corroboration raises consistency (independent modality agreement).
    if fi.multi_node_agree:
        c = float(np.clip(c + 0.1, 0.0, 1.0))

    u = float(np.clip(0.15 + 0.4 * (1.0 - c) + extra_u, 0.0, 1.0))
    expert = ExpertOutput(p=p, source="fire_phys", u=u, c=float(np.clip(c, 0.0, 1.0)),
                          r=1.0, cls=PhysicsClass.A)
    return FireResult(p_fire=p, consistency=c, used_classC=used_c, diagnostics=diag, expert=expert)
