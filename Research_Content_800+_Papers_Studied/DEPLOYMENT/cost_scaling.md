# DEPLOYMENT/cost_scaling.md — cost & scaling research notes (P19)

RESEARCH NOTES. Rule 18: no unsupported impact/cost-effectiveness claims. Prices are INDICATIVE and must be
re-quoted WITH DATES at build (ties P6/P13 re-pricing backlog). arXiv cannot verify current prices → treat all
figures as [UNVERIFIED / to re-quote].

## 1. Per-node cost (prototype vs real deployment)
- PROTOTYPE TARGET: INR 2000 per ground node (program hard cap; P6 BOM staged AS-OF-P6, re-price at build).
- REAL DEPLOYMENT adds (unpriced here, [UNVERIFIED]): weatherproof enclosure, battery/solar + charge
  management, mounting, certified radio module, installation labour, SIM/connectivity, spares.
- COST DRIVERS from literature: recurring recalibration is a major OPEX driver for low-cost sensors
  (2310.18118 global-law calibration reduces it; 2506.09186 schedules it) → F-15 directly targets this cost.

## 2. Per-site cost
Cameras (often reuse existing CCTV — avoids capex), an edge compute box (CPU-real-time detector F-11 keeps this
cheap), gateway/connectivity, and the human-review station (advisory stage). Reusing existing municipal/private
CCTV is the biggest cost lever (no new camera capex).

## 3. Recurring costs
Connectivity (cellular/backhaul), power, maintenance + recalibration visits (minimize via blind/global
calibration F-15 and uncertainty-driven scheduling), spare parts, human-review staffing.

## 4. Cost-effectiveness
NO cost-effectiveness claim is made (Rule 18): a credible claim needs verified prices + verified averted-loss
data + a published methodology (staged-rollout cost accounting, e.g. cost-per-completed-task framing 2608.08528
as a transferable template). What is UNKNOWN: real per-site TCO, averted-loss valuation, maintenance frequency
in Indian field conditions → to be found via a costed pilot + official statistics.

## 5. Honesty
All figures indicative/[UNVERIFIED]; re-quote with dates at build; no verified cost-effectiveness yet.
