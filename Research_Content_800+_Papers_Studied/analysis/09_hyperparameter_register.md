# HYPERPARAMETER REGISTER (MASTER_PROMPT §0.8)
# Training recipes, losses, schedules, batch sizes, augmentations, compute — WITH paper IDs,
# for later planning (feeds KAGGLE_BUDGET.md). Populated as papers reach full-text in P2/P3.
# Nothing here is "our setting" — every row is "as reported by paper X" or "planning default".

| ID | Component | Recipe item | Value (as reported) | Paper ID | Compute reported | Notes |
|----|-----------|-------------|---------------------|----------|------------------|-------|
| HP-01 | Node energy-mgmt RL (Q-learning) | γ / α / ε-schedule | γ=0.99, α=0.1, ε 1→0.1 (Δ=0.0004); episode 24h, wait 15min, train 15 days | 1909.01968 | 60-node, 2-wk real deploy; 0.1% downtime; −33% duty-cycle vs 3 prior RL | tabular Q-learning sufficed (CR-02); WS7 duty-cycle controller option |
| HP-02 | Concept-drift detector (planning default) | detector choice | ADWIN or HDDM_W preferred (accuracy-vs-energy frontier) | 2404.19452 (QUOTA#5) | edge/embedded energy-profiled | drift monitor for FM-07/FM-14; pick lowest-energy detector that holds accuracy on our stream; re-profile on-device in build phase |
| HP-03 | Burst-aware EWS classifier (reported) | model + threshold | XGBoost, cost-based decision threshold; AUC 0.697, AP 0.670, Recall 0.914 (as reported) | 2606.21130 (QUOTA#11) | tabular EWS, high-recall regime | credible gradient-boosted EWS workhorse (CR-02); recall prioritised via cost threshold (ties E-06/E-07); their numbers, NOT ours (Rule 16) |
| HP-04 | Missing-modality adaptation (reported) | extra parameters | <1% additional params recovers most performance under missing modalities | 2310.03986 (QUOTA#14) | multimodal | lightweight adapter for FM-15/CR-07; fusion is NOT free-lunch robust |

## RL reward design (pre-existing project design — to re-ground in P15)
- miss = -100; FA = -5 (red) / -1 (yellow-orange); lead = +2/h capped 12h;
  disruption = -0.01/person-hour; level-change = -0.5; gamma ≈ 0.99/h.
- Source: pre-existing TRINETRA design (NOT from a single paper); to be evidence-grounded
  against 2104.11422 (cry-wolf/trust) and 2205.12070 (imbalanced RL reward) in P15.
