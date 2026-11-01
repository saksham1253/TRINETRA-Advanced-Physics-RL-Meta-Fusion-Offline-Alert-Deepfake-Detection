"""ws5_fusion_rl.adapters — convert deep-model outputs into fusion ExpertOutput (torch-free, Rule 19/20).

The deep models (trinetra.deep) run on Kaggle/edge and produce a scalar probability. These adapters wrap that
probability into an ExpertOutput with the CORRECT Class label and a reliability CAP appropriate to the
source, so everything flows through the single decision function `decide()`. Keeping this torch-free means
the offline gateway can assemble experts from cached model scores without importing torch.

Reliability caps encode trust policy:
  - geo_phys / fire_phys (Class A physics-informed) : high trust
  - EO / anomaly / cctv   (Class data)              : medium trust
  - deepfake              (Class data, LOW trust)   : hard-capped at 0.4 (never gates a life-safety alert)
"""
from __future__ import annotations

import numpy as np

from ..common.types import ExpertOutput, PhysicsClass

# per-source (default reliability, hard cap, class)
_POLICY = {
    "geo_pinn":   (0.90, 1.00, PhysicsClass.B),    # physics-informed NN (B: learned, physics-regularized)
    "geo_phys":   (1.00, 1.00, PhysicsClass.A),    # pure deterministic physics gate
    "fire_cnn":   (0.80, 0.95, PhysicsClass.DATA),
    "fire_phys":  (1.00, 1.00, PhysicsClass.A),
    "eo":         (0.70, 0.90, PhysicsClass.DATA),
    "anomaly":    (0.70, 0.90, PhysicsClass.DATA),
    "cctv":       (0.75, 0.90, PhysicsClass.DATA),
    "deepfake":   (0.30, 0.40, PhysicsClass.DATA),  # LOW trust, hard-capped (Rule 19)
}


def deep_expert(source: str, prob: float, *, uncertainty: float = 0.3, consistency: float = 1.0,
                available: bool = True, reliability: float | None = None) -> ExpertOutput:
    """Wrap a deep model's probability as an ExpertOutput with source-appropriate class + reliability cap."""
    if source not in _POLICY:
        raise KeyError(f"unknown expert source {source!r}; add it to adapters._POLICY")
    default_r, cap_r, cls = _POLICY[source]
    r = default_r if reliability is None else reliability
    r = float(np.clip(r, 0.0, cap_r))                        # enforce the trust cap
    p = float(np.clip(prob, 0.0, 1.0))
    return ExpertOutput(p=p, source=source, u=float(np.clip(uncertainty, 0.0, 1.0)),
                        c=float(np.clip(consistency, 0.0, 1.0)), r=r, cls=cls, available=available)
