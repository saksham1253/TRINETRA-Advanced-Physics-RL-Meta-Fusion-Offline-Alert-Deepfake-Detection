# PROGRAM/sota/P14_sota_scan.md — uncertainty-aware multi-source fusion & calibration SOTA (WS1b)

Phase P14 · RESEARCH-ONLY. MASTER_PROMPT P14 task 1. SOTA + targets section. All numbers SOURCE-REPORTED
(Rule 16); detail + IDs in ws1_physics/literature_map.md P14 section. No own-system claim.

## 1. SOTA landscape (how good fusion/calibration is done now)
- FUSION FAMILIES: evidential Dempster-Shafer incl. OPEN-WORLD/heterogeneous frames (2508.08075) and
  differentiable DST layers inside deep nets (2108.05422); weighted DST decision fusion without paired data
  (2112.03044); recursive-Bayesian Kalman LATE fusion robust to dropped sensors (2509.25452); MoE gating +
  temperature scaling (2410.09570); learned stacking meta-model as calibrator (2501.10089); interpretable
  safety-critical transformer fusion (2207.14024).
- UNCERTAINTY / ABSTENTION: controllable abstention-fraction loss (2104.08236); UQ selective prediction
  HUQ-2 (2502.18050); threshold-based agentic abstention + explanation (2601.01008).
- CONFORMAL: online conformal + PID control under drift (2307.16895); conformal-p-value dynamic model
  reweighting (2609.38196); ensemble conformalized quantile regression (2202.08756).
- CALIBRATION: calibrated members ≠ calibrated ensemble (2101.05397); metamodel/stacking reduces ECE/MCE
  (2501.10089); MoE+temperature ~25% ECE reduction (2410.09570).
- CORRELATED/MISSING: redundancy + bounded-error robust estimation under attack (2103.00883); missing-
  modality-robust fusion (2309.15529); missing input breaks CALIBRATION, latent completion recovers it
  (2605.12517).
- ANOMALY+SUPERVISED FUSION: multi-view learned weighting (2212.05478); conformal reweighting (2609.38196);
  scoring-bias caution when injecting labeled anomalies (2105.07346).
- PROPER SCORING: proper-calibration-error bound (2203.07835); score posteriors with proper scores not ECE
  (2408.02841); strictly-proper ENERGY SCORE for stochastic physics simulators (2609.04988).

## 2. TARGETS section (process targets, NOT results, Rule 16)
- Fused model beats best single source on a CROSS-SITE split by a proper-scoring-rule margin exceeding
  seed-variance (pre-registered, ablation_plan §1).
- Fused output calibrated (proper-calibration-error bound) and no worse under each missing-source pattern.
- Correlated parent+extension grouped so they do not over-count; one bad/attacked source bounded.
- Abstention budget set explicitly; abstain path routes to human/corroboration (Rule 19).
- Online-conformal coverage holds under camera/site/weather shift.
- Evaluation uses proper scoring rules primary + calibration-error diagnostic only.

## 3. Honesty
All source-reported; nothing trained/measured. The chosen grouped-uncertainty-aware-calibrated fuser is a
CANDIDATE validated against pre-registered criteria in the build. ECE is explicitly demoted to a diagnostic.
