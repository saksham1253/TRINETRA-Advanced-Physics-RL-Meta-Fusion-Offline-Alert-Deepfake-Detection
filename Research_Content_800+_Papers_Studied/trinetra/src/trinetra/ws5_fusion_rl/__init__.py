"""ws5_fusion_rl — meta-fusion (GMF + PHARAOH + FM), safety shield, and the single decision function.

Default/fallback is FM-1 (Class B). PHARAOH (Class C) is opt-in via configs/fusion. The shield is a hard
monotone floor; the decision is advisory and fails safe to 'uncertain' (Rule 19)."""
from .nf import (
    nf1_consistency, nf2_reliability, nf3_conflict_to_uncertainty, nf4_salience,
    effective_weight, weighted_dispersion,
)
from .pharaoh import pharaoh_mean, pharaoh_order, pharaoh_fuse
from .gmf import gmf_fuse, gated_weights, bounded_residual, GMFResult, load_numpy_head
from .adapters import deep_expert
from .fusion_models import fuse, fm1_precision_weighted, FusionResult
from .shield import shield_floor, ShieldSignals
from .decision import decide, conformal_level
from .correlation import correlation_adjusted_weights, blue_fuse, redundancy_matrix
from .hierarchical import fuse_group, hierarchical_fuse, decide_hierarchical
from .rl import (
    RuleBaselinePolicy, OfflineRLPolicy, wis_value, ope_feasible, ope_admission, OPEVerdict,
)

__all__ = [
    "RuleBaselinePolicy", "OfflineRLPolicy", "wis_value", "ope_feasible", "ope_admission", "OPEVerdict",
    "correlation_adjusted_weights", "blue_fuse", "redundancy_matrix",
    "fuse_group", "hierarchical_fuse", "decide_hierarchical",
    "nf1_consistency", "nf2_reliability", "nf3_conflict_to_uncertainty", "nf4_salience",
    "effective_weight", "weighted_dispersion",
    "pharaoh_mean", "pharaoh_order", "pharaoh_fuse",
    "gmf_fuse", "gated_weights", "bounded_residual", "GMFResult", "load_numpy_head", "deep_expert",
    "fuse", "fm1_precision_weighted", "FusionResult",
    "shield_floor", "ShieldSignals", "decide", "conformal_level",
]
