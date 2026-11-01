"""pipeline.orchestrator — geo/fire/offline loops that assemble experts and call the single decision (M10).

Ties the modules together WITHOUT adding a second decision path: every loop builds a list of ExpertOutput
and calls ws5_fusion_rl.decide(). Offline dispatch handles the cloud-down path (local siren + DTN mesh),
and public CAP is still produced ONLY after operator approval (Rule 19).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import numpy as np

from ..common.config import Config
from ..common.types import Decision, ExpertOutput, Hazard, PhysicsClass, utcnow
from ..ws1a_firephys import FireInputs, fire_gate
from ..ws1b_geophys import GeoInputs, geo_gate
from ..ws5_fusion_rl import ShieldSignals, decide
from ..ws8_anomaly import anomaly_ensemble
from ..ws3_alert import DTNQueue, SirenBus


def _anomaly_expert(feature_matrix, series=None) -> ExpertOutput:
    s = anomaly_ensemble(feature_matrix, series=series)
    p = float(np.clip(s[-1], 0.0, 1.0))          # latest-sample anomaly as alarm evidence
    return ExpertOutput(p=p, source="anomaly", u=0.3, c=0.8, r=0.7, cls=PhysicsClass.DATA)


def run_geo_cycle(geo_inputs: GeoInputs, shield: ShieldSignals, feature_matrix,
                  series=None, cfg: Config | None = None, zone_id: str = "zone",
                  t: datetime | None = None) -> Decision:
    cfg = cfg or Config()
    gr = geo_gate(geo_inputs)
    experts = [gr.expert, _anomaly_expert(feature_matrix, series)]
    return decide(experts, shield, cfg, hazard=Hazard.LANDSLIDE, zone_id=zone_id, t=t or utcnow())


def run_fire_cycle(fire_inputs: FireInputs, shield: ShieldSignals, feature_matrix,
                   cfg: Config | None = None, zone_id: str = "zone",
                   t: datetime | None = None) -> Decision:
    cfg = cfg or Config()
    fr = fire_gate(fire_inputs, cfg)
    experts = [fr.expert, _anomaly_expert(feature_matrix)]
    return decide(experts, shield, cfg, hazard=Hazard.FIRE, zone_id=zone_id, t=t or utcnow())


@dataclass
class OfflineActions:
    siren_fired: bool
    dtn_queued: bool
    note: str


def offline_dispatch(decision: Decision, node_edge_level: str, dtn: DTNQueue,
                     siren: SirenBus) -> OfflineActions:
    """Cloud-down path (C1): node LOCAL_SIREN + shield floor drive a local siren and queue a DTN rebroadcast.
    No public alert is sent here — that still waits for a human (Rule 19)."""
    fired = False
    if node_edge_level == "LOCAL_SIREN":
        siren.fire(decision.zone_id, "LOCAL_SIREN", source="node_edge"); fired = True
    if decision.shield.raised:
        siren.fire(decision.zone_id, decision.shield.floor.name, source="shield"); fired = True
    msg_id = f"{decision.zone_id}:{decision.t.isoformat()}"
    dtn.enqueue(msg_id, str(decision.to_dict()).encode("utf-8"))
    return OfflineActions(siren_fired=fired, dtn_queued=True,
                          note="local siren + DTN rebroadcast; public CAP deferred to human (Rule 19)")
