"""ws2_deepfake — media authenticity scorer (M9, LOW-TRUST advisory).

DESIGN: deepfake/misinfo verdicts are the LEAST-trusted input and enter fusion with a small reliability r
(never gate a life-safety alert on them, Rule 19). The strong detector needs torch; the numpy
`heuristic_authenticity` combines simple transparent cues into a soft score and is explicitly low-trust.
"""
from __future__ import annotations

import numpy as np

from ..common.exceptions import MissingDependency
from ..common.types import ExpertOutput, PhysicsClass


class DeepfakeDetector:
    """Interface for a learned authenticity model (needs torch) -> stub raises."""

    def __init__(self, model_name: str = "ffpp-xception"):
        self.model_name = model_name

    def score(self, media):
        raise MissingDependency(
            f"deepfake detector {self.model_name!r} needs torch (not installed). "
            "Use heuristic_authenticity() as a low-trust fallback only."
        )


def heuristic_authenticity(cues: dict) -> float:
    """Soft authenticity probability in [0,1] from transparent cues (higher = more likely authentic).

    cues: {'noise_consistency':0..1,'metadata_intact':0/1,'compression_grade':0..1,'temporal_coherence':0..1}
    """
    keys = ["noise_consistency", "metadata_intact", "compression_grade", "temporal_coherence"]
    vals = [float(np.clip(cues.get(k, 0.5), 0, 1)) for k in keys]
    return float(np.clip(np.mean(vals), 0.0, 1.0))


def authenticity_expert(cues: dict, reliability: float = 0.3) -> ExpertOutput:
    """Wrap authenticity as a LOW-reliability expert: p = probability the corroborating media is FAKE."""
    auth = heuristic_authenticity(cues)
    p_fake = 1.0 - auth
    return ExpertOutput(p=p_fake, source="deepfake", u=0.5, c=1.0,
                        r=float(np.clip(reliability, 0.0, 0.4)), cls=PhysicsClass.DATA)
