"""trinetra.common.security — endpoint allow-list + no-raw-video-egress (constraints C6/C7).

Fail-closed: an outbound endpoint not on the allow-list raises; serializing a video blob onto a
cloud/alert channel raises. CI (scripts/ci_gates.py) exercises these.
"""
from __future__ import annotations

from urllib.parse import urlparse

from .exceptions import EndpointNotAllowed, SafetyViolation

# Video-like payload keys that must never leave a node/gateway (privacy, C7).
_VIDEO_KEYS = {"video", "raw_video", "frame", "frames", "clip", "rtsp", "mjpeg"}


def check_endpoint(url: str, allowlist: list[str]) -> str:
    """Return url if its host is on the allow-list, else raise (C6)."""
    host = (urlparse(url).hostname or "").lower()
    allowed = {h.lower() for h in allowlist}
    if host and host in allowed:
        return url
    raise EndpointNotAllowed(
        f"endpoint host {host!r} not in allow-list {sorted(allowed)} (constraint C6)"
    )


def assert_no_video_egress(payload: dict) -> None:
    """Raise if a dict destined for an off-node channel carries raw video (C7)."""
    def _scan(node, path=""):
        if isinstance(node, dict):
            for k, v in node.items():
                if k.lower() in _VIDEO_KEYS and v is not None:
                    raise SafetyViolation(
                        f"raw video field {path + k!r} must not egress a node/gateway (constraint C7)"
                    )
                _scan(v, path + k + ".")
        elif isinstance(node, (list, tuple)):
            for i, v in enumerate(node):
                _scan(v, f"{path}[{i}].")
    _scan(payload)
