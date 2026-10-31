# PHASE_10_report — WS8b ANOMALY DETECTION IMPLEMENTATION SPEC & EXPERIMENT PLAN (RESEARCH-ONLY)

Phase P10 (MASTER_PROMPT L532). Status: COMPLETE to gate (continuous mode — completion record, not a halt).
Ready-to-build specs; nothing implemented/run/measured (Rule 16). Rule 19 advisory; §ethics privacy.

## Objective
Turn the P9 anomaly design into a complete, ready-to-build specification per in-scope family, every default
grounded in evidence.

## What was produced
- ws8_anomaly/spec/sota_targets.md — SOTA scan update + reproduce-first baselines & their source-reported
  numbers + the cited DEFAULT-RECIPE REGISTRY (§3) + fair-comparison requirements + 23-paper quota list +
  "what changed".
- ws8_anomaly/spec/ per-family build specs:
  - family_b_sensor_timeseries.md (PRIORITY 1) — statistical/classical bank first; deep only if it beats it;
    conformal/EVT thresholding; overlapping-window + anti-convergence-collapse recipe.
  - family_c_ood_health.md (PRIORITY 1) — Mahalanobis/kNN/energy OOD + drift + label-free health wrapper;
    abstain gate.
  - family_d_physics_residual.md (P2) — residuals of P7/P7G models as detector + anti-spoof integrity gate;
    fallback-to-parent; TS-foundation fallback (NOT naive zero-shot — negative result 2607.12454).
  - family_a_video_anomaly.md (P2, SUPPORT-only) — tiny U-Net future-frame/forward-consistency, Gray→RGB,
    score-matching ANTICIPATION, SSL→LLM escalation; Within-AUROC/region metrics; never autonomous alarm.
  - family_e_network_alert.md (P2, lightweight) — crypto (P6) + surprisal IDS + per-protocol Z-score; feeds
    P12 threat model.
- ws8_anomaly/spec/edge_spec.md — ESP32 statistical stack + optional INT8 tiny model / HDC; source-reported
  envelopes flagged as other-hardware; P13 measurement list.
- ws8_anomaly/spec/integration_spec.md — anomaly-event schema; interfaces to P14/P12/P13; end-to-end
  scenarios (abstain/escalate/health/spoof); alert-fatigue budget + logged suppression; offline degradation.
- ws8_anomaly/failure_analysis.md — expected misses/false-flags, indistinguishable-from-benign cases,
  evaluation-driven failures, privacy/misuse risks, carried to P16.
- ws8_anomaly/literature_map.md — P10 section (23 NEW primary arXiv, ABS); 19 [P10] ledger rows; Audit #17
  PASS.

## Key implementation decisions grounded in the quota (source-reported, Rule 16)
- THRESHOLDING = conformal p-values + FDR control (2605.13642 `nonconform`; factorwise 2609.29580) and/or
  EVT PoT + dual-threshold hysteresis (2601.21293), fit on validation; look-elsewhere correction when
  scanning many sensors (2606.13780) — replacing hand-picked thresholds.
- RECONSTRUCTION DETECTORS: overlapping inference windows (avg +28% rel.; can reorder rankings — 2606.09874);
  do NOT train to convergence — early-stop or Kernel-Anchored Regularizer (2610.02345).
- SIMPLE BASELINES upgraded: RIFT seed-stable IF replacement (2610.12244); matrix-profile sketch (2311.03393);
  SSL-latent + IF/OCSVM/LOF edge baseline (2610.03649). Deep models must beat these under the strict protocol.
- CALIBRATION is first-class: conformal risk-control head (~1.9 AUROC, ~29% FPR reduction — 2609.14234);
  single-pass evidential uncertainty (2610.10116); CLEAR post-hoc OOD calibrator (2610.01384).
- EDGE: QAT 4-bit (INT8 for MCU) + HW-aware search (2505.17662); HDC binary-ops MCU detector (2606.13754).
- VIDEO (support): FoGA tiny/155 FPS (2601.18135); Uni-DSM anticipation = early warning (2610.11149);
  HyCoVAD SSL→LLM cost-controlled escalation (2509.22544).
- NEGATIVE RESULT HONORED: naive zero-shot forecasting foundation models fail on PERSISTENT anomalies
  (2607.12454) → not used as the sustained-fault detector.

## Honesty & limits (§0.5)
All 23 primaries ABS (0 FT); IDs/numbers subagent-reported, not independently re-fetched (residual risk).
Edge energy/latency figures are FPGA/Jetson/other-hardware — our MCU numbers MUST be measured in P13.
Reproduce-first baselines + acceptance criteria are PLANS/process targets, not results. Public benchmarks
carry documented flaws (method-dev only); real operating-point numbers need our own normal-only data. A few
spec files still carry the literal "[recipe-cite — P10 reader]" tag text pointing at the now-populated
registry (cosmetic; the citations exist in sota_targets.md §3).

## Open actions carried
Full-text reads for exact recipe numbers (POT risk level, AE latent dims, conformal α) when building;
deepen MCU-specific edge + deep-SVDD one-class recipes (reader flagged these as thin); confirm dataset
licenses; design own-data normal-reference collection; the P13 edge measurement campaign.

## Gate
PROGRAM/gate_messages/PHASE_10_gate.md. Auto-proceeding to P11 (WS2 deepfake & misinformation).
