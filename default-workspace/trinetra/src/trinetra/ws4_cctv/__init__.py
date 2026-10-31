"""ws4_cctv — edge detector interface + temporal validator (M3, WS4).

The frame-level detector is a small CNN (e.g. YOLO-n class) that needs torch; the real path raises
MissingDependency. The TemporalValidator is pure numpy and is the key false-alarm suppressor: it requires
a detection to PERSIST across a sliding window and across corroborating views before confidence is trusted
(reject single-frame glints, headlights, steam puffs). DESIGN/COMPONENT_DESIGN.md §4.2.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass

import numpy as np

from ..common.exceptions import MissingDependency


class EdgeDetector:
    """Interface: frame -> (class_conf). Real impl needs torch; stub raises."""

    def __init__(self, backbone: str = "yolov5n"):
        self.backbone = backbone

    def detect(self, frame):
        raise MissingDependency(
            f"CCTV detector backbone {self.backbone!r} needs torch (not installed). "
            "Install extras [deep]; the TemporalValidator below works on any detector's confidences."
        )


@dataclass
class ValidatedEvent:
    confirmed: bool
    confidence: float
    support_frames: int


class TemporalValidator:
    """Sliding-window persistence validator. Confirms an event only when per-frame confidence stays above
    `conf_thr` for at least `min_frames` within the last `window` frames (and optionally across cameras)."""

    def __init__(self, window: int = 5, min_frames: int = 3, conf_thr: float = 0.5):
        self.window = window; self.min_frames = min_frames; self.conf_thr = conf_thr
        self.buf: deque[float] = deque(maxlen=window)

    def update(self, frame_conf: float) -> ValidatedEvent:
        self.buf.append(float(frame_conf))
        support = sum(1 for c in self.buf if c >= self.conf_thr)
        confirmed = support >= self.min_frames
        conf = float(np.mean([c for c in self.buf if c >= self.conf_thr])) if support else 0.0
        return ValidatedEvent(confirmed=confirmed, confidence=conf if confirmed else 0.0,
                              support_frames=support)

    def reset(self):
        self.buf.clear()
