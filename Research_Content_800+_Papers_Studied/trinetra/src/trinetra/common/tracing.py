"""trinetra.common.tracing — lightweight trace ids + append-only JSONL audit (Rule 19 explainability)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def new_trace_id() -> str:
    return "tr-" + uuid.uuid4().hex[:16]


def audit(record: dict[str, Any], path: str | Path = "data/audit.jsonl") -> None:
    """Append one JSON line to an audit log so every advisory can be traced sensor->decision->alert."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    record = {"_ts": datetime.now(timezone.utc).isoformat(), **record}
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, default=str) + "\n")
