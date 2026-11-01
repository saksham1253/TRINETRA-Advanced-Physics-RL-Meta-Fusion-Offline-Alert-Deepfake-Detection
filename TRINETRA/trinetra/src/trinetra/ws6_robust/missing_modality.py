"""ws6_robust.missing_modality — graceful degradation adapter (constraint C8 / CR-07).

A dropped sensor/modality must LOWER trust and WIDEN uncertainty, never silently fabricate confidence.
Marks absent experts unavailable and inflates the uncertainty of the rest, so the decision layer widens its
conformal set and tends toward 'uncertain' (Rule 19).
"""
from __future__ import annotations

import numpy as np

from ..common.types import ExpertOutput


def apply_missing_modality(experts: list[ExpertOutput], present_sources: set[str],
                           penalty: float = 0.15) -> list[ExpertOutput]:
    """Return a new expert list: absent sources -> available=False; present -> u increased by penalty
    per missing peer (bounded)."""
    n_missing = sum(1 for e in experts if e.source not in present_sources)
    out = []
    for e in experts:
        if e.source not in present_sources:
            out.append(ExpertOutput(p=e.p, source=e.source, u=1.0, c=e.c, r=e.r,
                                    cls=e.cls, available=False))
        else:
            u = float(np.clip(e.u + penalty * n_missing, 0.0, 1.0))
            out.append(ExpertOutput(p=e.p, source=e.source, u=u, c=e.c, r=e.r,
                                    cls=e.cls, available=True))
    return out
