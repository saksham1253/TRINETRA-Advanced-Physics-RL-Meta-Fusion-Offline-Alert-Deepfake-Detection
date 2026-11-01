"""trinetra.common — shared types, config, security, tracing."""
from .types import (
    SCHEMA_VERSION, Level, Hazard, PhysicsClass, Reliability,
    ExpertOutput, Evidence, Decision, ShieldResult, ConformalResult, utcnow,
)
from .config import Config, load_config, DEFAULTS
from .exceptions import (
    TrinetraError, MissingDependency, SafetyViolation, LeakageError,
    EndpointNotAllowed, SchemaError,
)
from .security import check_endpoint, assert_no_video_egress
from .tracing import new_trace_id, audit

__all__ = [
    "SCHEMA_VERSION", "Level", "Hazard", "PhysicsClass", "Reliability",
    "ExpertOutput", "Evidence", "Decision", "ShieldResult", "ConformalResult", "utcnow",
    "Config", "load_config", "DEFAULTS",
    "TrinetraError", "MissingDependency", "SafetyViolation", "LeakageError",
    "EndpointNotAllowed", "SchemaError",
    "check_endpoint", "assert_no_video_egress", "new_trace_id", "audit",
]
