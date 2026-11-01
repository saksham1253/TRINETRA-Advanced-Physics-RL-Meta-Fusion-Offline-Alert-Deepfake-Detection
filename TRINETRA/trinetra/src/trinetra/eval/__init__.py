"""eval — M0 admission harness: spatial-CV, baselines, cost-loss Value Score, real-win, report guard.

This module is the FOUNDATION (built first per REPO_BLUEPRINT M0): nothing downstream may claim performance
until it passes here on spatial-CV against all baselines (Rule 16)."""
from .splits import spatial_block_kfold, temporal_split, assert_no_time_leak
from .value_score import p_star, value_score, realized_cost, alarms_from_prob, climatology_cost
from .baselines import base_rate_climatology, persistence, physics_rule, LogisticNumpy
from .real_win import real_win
from .calibration import (
    reliability_curve, expected_calibration_error, maximum_calibration_error,
    brier_decomposition, IsotonicCalibrator, PlattCalibrator,
)
from .report import ReportGuard, ReportGuardError

__all__ = [
    "spatial_block_kfold", "temporal_split", "assert_no_time_leak",
    "p_star", "value_score", "realized_cost", "alarms_from_prob", "climatology_cost",
    "base_rate_climatology", "persistence", "physics_rule", "LogisticNumpy",
    "real_win", "ReportGuard", "ReportGuardError",
    "reliability_curve", "expected_calibration_error", "maximum_calibration_error",
    "brier_decomposition", "IsotonicCalibrator", "PlattCalibrator",
]
