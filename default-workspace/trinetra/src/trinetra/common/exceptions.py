"""trinetra.common.exceptions — explicit, honest failure modes (no silent fallbacks)."""
from __future__ import annotations


class TrinetraError(Exception):
    """Base error."""


class MissingDependency(TrinetraError):
    """A heavy optional library (torch / sklearn / xgboost / d3rlpy) is required but not installed.

    Raised instead of returning fabricated results (Rule 16: never claim a result we cannot produce).
    """


class SafetyViolation(TrinetraError):
    """A hard safety invariant (Rule 19) would be violated — fail closed."""


class LeakageError(TrinetraError):
    """A feature timestamp is after the decision time (anti-leak, gate G6)."""


class EndpointNotAllowed(TrinetraError):
    """Outbound endpoint is not on the allow-list (constraint C6)."""


class SchemaError(TrinetraError):
    """A contract/schema validation failed."""
