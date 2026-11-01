"""eval.value_score — cost-loss decision value (gate G2). DESIGN eval protocol + research P-notes.

Decision-theoretic cost-loss convention (matches configs cost.C_FA / cost.C_miss):
    cost(alarm, no event)  = C_FA
    cost(alarm, event)     = 0      (acted; loss avoided)
    cost(no alarm, event)  = C_miss
    cost(no alarm, no event)= 0
Optimal alarm threshold  p* = C_FA / (C_FA + C_miss).

Value Score (relative to climatology):  VS = 1 - E_forecast / E_climate   (1=perfect, <=0=no skill).
Reporting a bare accuracy/AUC without this cost-aware score is BLOCKED by eval.report (Rule 16 honesty).
"""
from __future__ import annotations

import numpy as np


def p_star(C_FA: float, C_miss: float) -> float:
    return C_FA / (C_FA + C_miss)


def realized_cost(y_true, alarms, C_FA: float, C_miss: float) -> float:
    """Total cost of a 0/1 alarm vector against 0/1 outcomes under the cost-loss convention."""
    y = np.asarray(y_true, int); a = np.asarray(alarms, int)
    false_alarms = np.sum((a == 1) & (y == 0))
    misses = np.sum((a == 0) & (y == 1))
    return float(false_alarms * C_FA + misses * C_miss)


def alarms_from_prob(p_pred, C_FA: float, C_miss: float):
    """Alarm iff forecast probability exceeds the optimal threshold p*."""
    thr = p_star(C_FA, C_miss)
    return (np.asarray(p_pred, float) >= thr).astype(int)


def climatology_cost(y_true, C_FA: float, C_miss: float) -> float:
    """Best constant policy cost: min(always-alarm, never-alarm)."""
    y = np.asarray(y_true, int); n = len(y); s = y.mean() if n else 0.0
    always = (1 - s) * n * C_FA        # alarm every time: pay C_FA on every non-event
    never = s * n * C_miss             # never alarm: pay C_miss on every event
    return float(min(always, never))


def value_score(y_true, p_pred, C_FA: float, C_miss: float) -> dict:
    """Return {value_score, E_forecast, E_climate, p_star, n, base_rate}. E_perfect=0 in this convention."""
    y = np.asarray(y_true, int)
    a = alarms_from_prob(p_pred, C_FA, C_miss)
    Ef = realized_cost(y, a, C_FA, C_miss)
    Ec = climatology_cost(y, C_FA, C_miss)
    vs = 1.0 - (Ef / Ec) if Ec > 0 else 0.0
    return {"value_score": float(vs), "E_forecast": Ef, "E_climate": Ec,
            "p_star": p_star(C_FA, C_miss), "n": int(len(y)), "base_rate": float(y.mean() if len(y) else 0.0)}
