"""ws1b_eo.encoder — frozen EO foundation-model encoder interface (M3, Class data-driven).

The real encoder is a pretrained geospatial foundation model (e.g. Prithvi/SatMAE-class) run FROZEN; it
requires torch + model weights, which are not available in this environment. Calling the real path raises
MissingDependency (Rule 16: never fabricate embeddings). A deterministic numpy `hashing_fallback` is
provided ONLY for wiring/tests and is explicitly flagged as NOT a learned representation.
"""
from __future__ import annotations

import numpy as np

from ..common.exceptions import MissingDependency


class EOEncoder:
    """Interface for a frozen EO encoder: image/datacube patch -> embedding vector."""

    def __init__(self, model_name: str = "prithvi-frozen", dim: int = 256):
        self.model_name = model_name
        self.dim = dim

    def embed(self, patch) -> np.ndarray:
        raise MissingDependency(
            f"EO encoder {self.model_name!r} needs torch + pretrained weights (not installed). "
            "Install extras [deep] and provide weights; see DESIGN/CR-01 encoder trade study."
        )

    def hashing_fallback(self, patch, seed: int = 0) -> np.ndarray:
        """Deterministic pseudo-embedding for PLUMBING/TESTS ONLY — not a learned feature. Do not use
        for any reported result."""
        a = np.asarray(patch, float).ravel()
        rng = np.random.default_rng(abs(hash((a.tobytes(), seed))) % (2**32))
        proj = rng.normal(size=(self.dim, a.size)) if a.size else np.zeros((self.dim, 1))
        v = proj @ (a if a.size else np.zeros(1))
        n = np.linalg.norm(v) + 1e-9
        return v / n
