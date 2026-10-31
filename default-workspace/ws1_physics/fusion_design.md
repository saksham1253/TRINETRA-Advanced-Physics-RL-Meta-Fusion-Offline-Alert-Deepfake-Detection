# ws1_physics/fusion_design.md — calibrated meta-fusion design (P14, WS1b)

Phase P14 · RESEARCH-ONLY, on-paper analysis. MASTER_PROMPT P14 task 4. Nothing trained/measured (Rule 16).
Every method choice traces to a SOURCE-REPORTED paper in the P14 reading (ws1_physics/literature_map.md P14
section / PROGRAM/sota/P14_sota_scan.md). Rule 19: the fused output is advisory; it feeds the P12 alert policy
and P11 verification policy under human oversight, never an autonomous public alert.

## 0. What is being fused
Heterogeneous per-source outputs: Layer-1/Layer-2 PHYSICS model predictions (P7/P7G) with their declared
correlation (an extension and its parent are highly correlated BY CONSTRUCTION), the learned CCTV detector
(P8) + zero-shot hazard scores (P14Z), multi-sensor IoT node hazard (P6/P13), and anomaly scores + sensor-
health flags (P9/P10). Each source emits a PREDICTION + an UNCERTAINTY.

## 1. Design principles (each evidence-backed)
1. CALIBRATE THE FUSED OUTPUT, NOT ONLY THE MEMBERS. Calibrated members do NOT imply a calibrated ensemble,
   and a calibrated ensemble cannot beat the average of its calibrated members (2101.05397). ⇒ post-hoc
   calibrate the fuser (temperature/isotonic), measured by a proper score.
2. COMMON CALIBRATED SCALE BEFORE FUSION. Convert each heterogeneous output to a common scale — conformal
   p-values / proper-score-calibrated posteriors — BEFORE weighted/evidential combination; do NOT fuse raw
   scores (2105.07346 scoring-bias; 2609.38196 conformal reweighting; 2408.02841/2203.07835 proper scores).
3. DON'T DOUBLE-COUNT CORRELATED MODELS. A Layer-2 physics extension and its Layer-1 parent are correlated by
   construction → group them and fuse the GROUP as one evidence source (or down-weight by estimated
   correlation), consistent with the redundancy-aware robust-estimation pattern (2103.00883) and
   evidence-theoretic conflict handling (2508.08075 open-world DST).
4. NO SINGLE MODEL DOMINATES; BAD MODELS ARE SUPPRESSED. Use conformal-p-value / nonconformity-driven dynamic
   reweighting to down-weight unreliable members (2609.38196 CAGE); redundancy + bounded-error robust
   estimation isolates a faulty/attacked input (2103.00883); evidential conflict elimination (2508.08075).
5. GRACEFUL DEGRADATION UNDER MISSING / OUT-OF-REGIME MODELS. Recursive-Bayesian late fusion marginalizes a
   dropped stream (Kalman late fusion 2509.25452, up to 70% error reduction + robustness to intermittent
   sensors); missing-modality-robust fusion with robust losses (2309.15529); and CRUCIALLY, a dropped input
   breaks CALIBRATION not just accuracy (2605.12517) → the fuser must RE-CALIBRATE conditioned on which
   sources are present (per-availability-pattern calibration).
6. ABSTAIN / ESCALATE WHEN EVIDENCE IS WEAK. Anomaly scores + sensor-health flags act as ABSTENTION TRIGGERS;
   a controllable abstention budget (PID-controlled abstention fraction 2104.08236; UQ-driven selective
   prediction HUQ-2 2502.18050; threshold-based agentic abstention 2601.01008) sets an explicit "I don't
   know → escalate to human / request corroboration" rate.
7. ONLINE COVERAGE UNDER DRIFT. Wrap the fused streaming score in online conformal prediction with a PID
   controller for distribution-free coverage under seasonality/shift (2307.16895); per-source calibrated
   intervals via ensemble conformalized quantile regression (2202.08756).
8. SCALE TO N WITHOUT OVERFITTING. Prefer a parsimonious fuser (grouped evidential / learned stacking
   meta-model that is itself a strong calibrator, 2501.10089; MoE + temperature scaling, 2410.09570) over a
   high-capacity combiner; regularize; validate by SESSION/SITE split.

## 2. Chosen fuser (candidate, to validate in build)
A GROUPED, UNCERTAINTY-AWARE, CALIBRATED fuser:
- Stage A — per-source calibration: each source → calibrated posterior / conformal p-value (temperature or
  isotonic; EnCQR intervals for regressors).
- Stage B — grouping: correlated sources (Layer-2 + its Layer-1 parent; near-duplicate detectors) grouped so
  the group contributes once.
- Stage C — evidential/weighted combination: open-world Dempster-Shafer (2508.08075) OR a differentiable
  evidential fusion layer (2108.05422) OR a learned stacking meta-model (2501.10089), with conformal-driven
  dynamic weights (2609.38196); redundancy-based robust estimate for same-variable sensors (2103.00883).
- Stage D — fused calibration + abstention: calibrate the FUSED output (2101.05397), apply the abstention
  budget (2104.08236/2502.18050), wrap in online conformal (2307.16895).
- Stage E — interface: emit fused probability + uncertainty + abstain/escalate flag + which sources were
  present/down-weighted (for the P12 policy, P11 verification, and the dashboard).

## 3. On-paper analysis (theoretical behavior)
- CORRELATED ERRORS: grouping + correlation-aware weighting prevents a parent+extension pair from
  over-counting; without it, naive averaging would inflate confidence in the shared failure mode (the
  2101.05397 member-vs-ensemble caution formalizes why fused calibration is required).
- MISSING INPUTS: late-fusion marginalization keeps a prediction; per-availability-pattern recalibration
  prevents the silent miscalibration 2605.12517 documents.
- MISCALIBRATION / ONE BAD MODEL: conformal reweighting (2609.38196) + redundancy robust estimate
  (2103.00883) bound a single bad/attacked source's influence; evidential conflict elimination (2508.08075)
  handles disagreement.
- WEAK EVIDENCE: abstention budget routes to human/corroboration rather than forcing a fire/no-fire call —
  the safety-preferred behavior (Rule 19).

## 4. Evaluation metric discipline (decided here, used in build)
Score fused posteriors with PROPER SCORING RULES (log-loss / Brier / CRPS; ENERGY SCORE for physics-simulator
distributions, 2609.04988). Do NOT use ECE as the PRIMARY metric — ECE ignores discrimination and standard
estimators are biased/inconsistent (2408.02841, 2203.07835); use calibration error (proper-calibration-error
bound) only as a DEVELOPMENT DIAGNOSTIC. Report prediction-interval coverage for conformal wrappers.

## 5. Honesty
Design + on-paper analysis only; no fuser trained or measured. All method claims source-reported; the chosen
fuser is a CANDIDATE to validate against the pre-registered acceptance criteria (ablation_plan.md). The
specific improvement that will count as "fusion works" is pre-registered in ablation_plan.md §1, NOT claimed
here.
