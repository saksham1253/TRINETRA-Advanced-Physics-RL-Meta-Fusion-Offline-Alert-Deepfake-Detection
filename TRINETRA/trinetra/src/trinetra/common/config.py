"""trinetra.common.config — JSON config loader with safe-by-default feature flags (REPO_BLUEPRINT §3).

pyyaml is unavailable in this environment, so configs are JSON. Flags default to the SAFE path:
FM-1 fusion, PHARAOH off, ND* off, one-step RL, no quantization. Opting into heavier/novel paths
requires explicit config + the owning gate (Rule 20).
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_CONFIG_DIR = Path(__file__).resolve().parents[3] / "configs"

# ---- Safe defaults (mirror REPO_BLUEPRINT.md §3) --------------------------------------------------
DEFAULTS: dict[str, Any] = {
    "seeds": [0, 1, 2, 3, 4],
    "cost": {"C_FA": 5.0, "C_miss": 100.0},   # p* = C_FA/(C_FA+C_miss) ≈ 0.0476
    "fusion": {"model": "FM-1", "operator": {"pharaoh": False}, "tau": 0.5, "lambda": 0.3},
    "firephys": {f"nd{i}": False for i in range(1, 8)},
    "geophys": {"caine_a": 14.0, "caine_b": 0.39, "fukuzono_alpha": 2.0},
    "rl": {"algo": "one_step", "ope_gate": True},
    "calib": {"alpha": 0.1, "wcps": True},
    "cctv": {"backbone": "yolov5n", "quant": "none", "window": 5, "far_target": 0.05},
    "iot": {"lora_band": "IN865_867", "duty_cycle_pct": 1.0},
    "alert": {"require_human_approval": True},     # Rule 19 — immutable to True at runtime
    "security": {"endpoint_allowlist": []},
}


@dataclass
class Config:
    data: dict[str, Any] = field(default_factory=lambda: json.loads(json.dumps(DEFAULTS)))

    def get(self, dotted: str, default: Any = None) -> Any:
        node: Any = self.data
        for part in dotted.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    @property
    def p_star(self) -> float:
        c = self.get("cost", {})
        return c["C_FA"] / (c["C_FA"] + c["C_miss"])

    def require_human_approval(self) -> bool:
        # Rule 19: this is hard-wired True; config cannot disable the human gate.
        return True


def _deep_merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(*names: str, config_dir: str | os.PathLike | None = None) -> Config:
    """Load default.json then merge each named JSON config (without extension) on top."""
    cdir = Path(config_dir) if config_dir else _CONFIG_DIR
    data = json.loads(json.dumps(DEFAULTS))
    for name in ("default", *names):
        p = cdir / f"{name}.json"
        if p.exists():
            with p.open("r", encoding="utf-8") as fh:
                data = _deep_merge(data, json.load(fh))
    return Config(data=data)
