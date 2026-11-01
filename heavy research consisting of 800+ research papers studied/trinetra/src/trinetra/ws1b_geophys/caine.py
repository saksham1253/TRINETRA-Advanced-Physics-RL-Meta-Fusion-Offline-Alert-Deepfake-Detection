"""ws1b_geophys.caine — rainfall intensity-duration landslide threshold (Class A). M1.

Caine (1980):  I = a * D^(-b)   with I in mm/h and D in h.
Coefficients (a,b) MUST be locally re-fit (config geophys.caine_a / caine_b), never a borrowed global
constant used as live truth (honesty note). Returns exceedance + a soft margin for fusion.
"""
from __future__ import annotations

import numpy as np


def caine_threshold(D_hours, a: float, b: float):
    """Threshold intensity [mm/h] for duration D [h]."""
    D = np.asarray(D_hours, float)
    return a * np.power(np.where(D > 0, D, np.nan), -b)


def caine_exceedance(I_mm_h, D_hours, a: float, b: float):
    """Return (exceeded: bool-array, ratio: I / I_threshold). ratio>1 => above the ID line."""
    thr = caine_threshold(D_hours, a, b)
    ratio = np.asarray(I_mm_h, float) / thr
    return ratio > 1.0, ratio
