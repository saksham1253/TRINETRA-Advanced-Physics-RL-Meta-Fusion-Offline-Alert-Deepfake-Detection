"""eval.report — the admission-gate report + honesty guard (Rule 16, gate G2).

NO performance claim may be emitted unless it is accompanied by (a) a spatial-CV protocol, (b) a comparison
against EVERY mandatory baseline, and (c) a confidence interval. `ReportGuard.headline()` raises otherwise.
`admit()` returns True only if the model shows a 'real win' over all baselines; until then the system is
explicitly 'NOT ADMITTED — no performance may be claimed' (prints that, honestly).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

from ..common.exceptions import TrinetraError


class ReportGuardError(TrinetraError):
    """Attempted to emit a performance claim without baseline + CI + spatial-CV."""


@dataclass
class ReportGuard:
    spatial_cv: bool = False
    baselines: dict = field(default_factory=dict)   # name -> real_win verdict dict
    metrics: dict = field(default_factory=dict)

    def add_baseline_verdict(self, name: str, verdict: dict) -> None:
        if "real_win" not in verdict or "ci_low" not in verdict:
            raise ReportGuardError(f"baseline verdict for {name!r} missing real_win/CI")
        self.baselines[name] = verdict

    def headline(self, metric_name: str, value: float) -> str:
        """Emit a headline performance number ONLY if the gate conditions hold (Rule 16)."""
        if not self.spatial_cv:
            raise ReportGuardError("cannot report performance without spatial-CV (G2)")
        if not self.baselines:
            raise ReportGuardError("cannot report performance without baseline comparisons (G2)")
        if not self.admit():
            raise ReportGuardError(
                "NOT ADMITTED: model does not show a real win over all baselines; "
                "per Rule 16 no performance may be claimed yet"
            )
        self.metrics[metric_name] = value
        return f"{metric_name} = {value:.4f} (spatial-CV; beats all baselines with CI)"

    def admit(self) -> bool:
        """Admitted iff spatial-CV AND a real win over EVERY mandatory baseline."""
        return bool(self.spatial_cv and self.baselines
                    and all(v.get("real_win") for v in self.baselines.values()))

    def summary(self) -> dict:
        return {
            "spatial_cv": self.spatial_cv,
            "admitted": self.admit(),
            "baselines": {k: {"real_win": v.get("real_win"), "ci_low": v.get("ci_low")}
                          for k, v in self.baselines.items()},
            "metrics": self.metrics,
            "note": ("ADMITTED — performance claims permitted" if self.admit()
                     else "NOT ADMITTED — no performance may be claimed (Rule 16)"),
        }

    def __str__(self) -> str:
        return json.dumps(self.summary(), indent=2)
