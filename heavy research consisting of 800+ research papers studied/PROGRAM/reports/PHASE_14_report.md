# PHASE_14_report — WS1b META-FUSION DESIGN (DESIGN / ON-PAPER)

Phase P14 (MASTER_PROMPT L645). Status: COMPLETE to gate (continuous mode). Nothing trained/measured (Rule 16).
Rule 19: the fused output is advisory; it feeds the P12 alert policy and P11 verification policy under human
oversight.

## Objective
Design the calibrated fusion of admitted physics models + learned detectors + sensors + anomaly scores, with
the evaluation plan for the build phase.

## Deliverables
- ws1_physics/fusion_design.md — grouped, uncertainty-aware, calibrated fuser: per-source calibration →
  grouping of correlated sources (Layer-2 extension + Layer-1 parent fused once) → evidential/weighted
  conformal-reweighted combination → fused-output calibration + abstention budget + online conformal →
  interface (fused prob + uncertainty + abstain/escalate + source-availability). On-paper analysis of
  correlated errors, missing inputs, miscalibration, one-bad-model, weak evidence.
- ws1_physics/ablation_plan.md — PRE-REGISTERED acceptance (fused beats best single on CROSS-SITE split by a
  proper-scoring-rule margin exceeding seed variance; calibrated; FA ≤ best single at matched sensitivity) +
  ablations (single/LOO/greedy/family/all-pairs/with-without physics+anomaly/parent-vs-extension) + stress
  tests (noise/missing/adversarial/shift/rare/correlated-failure) + statistics discipline.
- PROGRAM/sota/P14_sota_scan.md — SOTA landscape + process targets.

## Quota (15 required → MET)
22 NEW primary arXiv (ABS), 8 topics: fusion (open-world DST, weighted DST, Kalman late, MoE+temperature),
abstention (PID budget, HUQ-2, agentic), conformal (PID control, CAGE reweighting, EnCQR), ensembles/
calibration (members≠ensemble, stacking calibrator), correlated/missing (missing-modality, latent completion,
redundancy robust), anomaly+supervised (multi-view weights, scoring-bias bound), proper scoring (proper-cal
bound, PSR-not-ECE, energy score for sims), safety-critical (InterFuser, DST PET/CT layer). 0 FT; running
body-level deep FT NEW unchanged at 100.

## Key design decisions (evidence-backed)
Calibrate the FUSED output not just members (2101.05397); common calibrated scale (conformal/proper) before
fusion (2105.07346, 2609.38196); group correlated parent+extension (2103.00883, 2508.08075); conformal
reweighting + redundancy bound a bad source (2609.38196, 2103.00883); per-availability recalibration under
missing inputs (2605.12517, 2509.25452); abstention budget routes weak evidence to humans (2104.08236,
2502.18050); proper scoring rules primary, ECE demoted to diagnostic (2408.02841, 2203.07835), energy score
for physics sims (2609.04988).

## Honesty & limits
Design/on-paper only; the fuser is a CANDIDATE, "fusion works" is a FUTURE pre-registered test (ablation_plan
§1), with an honest "use best single + abstention" fallback if it fails the bar. ABS depth; IDs subagent-
reported not re-fetched.

## Gate
PROGRAM/gate_messages/PHASE_14_gate.md. Auto-proceeding to P14Z (zero-shot classification) — reader (16
papers) ALREADY PIPELINED and in hand.
