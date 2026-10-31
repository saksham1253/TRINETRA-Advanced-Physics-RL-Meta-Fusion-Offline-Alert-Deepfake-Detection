# PHASE_18_report — FEATURE SPECIFICATIONS & MEASUREMENT PLANS (Wave-1 F-11..F-17)

Phase P18 (MASTER_PROMPT P18). Status: COMPLETE to gate (continuous mode). Nothing implemented/measured
(Rule 16). Rule 19: advisory, human-in-the-loop; monitors/auto-adapt stay advisory.

## Objective
For the Wave-1 features approved at the P17 gate, write ready-to-build specifications + measurement plans with
pre-registered decision rules. Nothing built.

## Deliverables
- features/wave1_specs.md — full specs for F-11 (edge detector), F-12 (temporal event validation), F-13
  (conformal under shift), F-14 (label-free drift/calibration monitoring), F-15 (IoT sensor drift correction),
  F-16 (IR optical-flow physics feature), F-17 (tooling + real-win gate). Each: design + plug-in, config/build
  flags, I/O, hyperparameter defaults w/ sources, ablation design, metrics, PRE-REGISTERED decision rule,
  cost, risks + new failure modes (fed to the P16 robustness catalogue).
- PROGRAM/sota/P18_sota_scan.md — per-feature SOTA + process targets.

## Quota (15 required → MET)
21 NEW primary arXiv (ABS), all DISTINCT from previously-cited features: A edge detector ×5 (incl. negative
edge-TL result 2501.08639), B temporal validation ×4, C conformal-under-shift ×4 (incl. PICP-collapse case
2604.22787), D label-free drift ×4, E sensor drift ×4. 0 FT; running body-level deep FT NEW unchanged at 100.

### P18 literature map (21 papers → feature)
A/F-11: 2503.07371 HGO-YOLO; 2512.24622 FRS-YOLO; 2506.09300 quantized-YOLOv4-tiny/Pi5; 2401.08105 QAT+
  TensorRT/Jetson; 2501.08639 edge-TL NEGATIVE result.
B/F-12: 2607.03131 event-validation (primary, FA 52%→4%); 2307.00104 temporal smoke (overfit flag); 2010.07110
  FAR-bounded online threshold; 2503.09960 density-weighted voting.
C/F-13: 2610.09208 sketched WCP; 2501.11413 W-CRC efficiency bound; 2603.26415 KMM-CP; 2604.22787 split-CP
  coverage-collapse case study.
D/F-14: 2406.17813 DriftLens; 1806.10131 Request-and-Reverify HHT; 2207.05796 conformal test-perf estimation;
  2304.08319 drift-detector compute benchmark.
E/F-15: 2406.17488 env-vs-instrument decomposition (THE pitfall); 2508.02724 Veli reference-free + AQ-SDR
  (D106); 2310.18118 global multi-unit calibration; 2604.21527 LSTM temporal calibration.

## Key pre-registration decisions (per feature)
F-11: measure SMOKE-specific INT8 recall drop; don't assume TL/newer backbone help edge latency (2501.08639).
F-12: FAR-driven threshold; report false-alarm reduction AGAINST detection-latency/recall cost.
F-13: realized PICP vs nominal under injected shift; never claim 1−α cross-site without weighting (2604.22787).
F-14: detection-delay↔false-alarm curve; monitor input-drift AND calibration-drift; fit edge compute ceiling.
F-15: decompose env vs instrument before recalibration (2406.17488); blind corrector must not explain away a
  real event.
F-17: every "win" must pass the LMEM+GLRT significance gate on a cross-camera split.

## Honesty & limits
Specs only; nothing built/measured. All ABS/source-reported on non-fire/other-domain benchmarks → transfer
risk per feature. Exact hyperparameters need full-text reads (2503.07371, 2607.03131, 2610.09208, 2406.17813,
2406.17488). IDs subagent-reported not re-fetched.

## Gate
PROGRAM/gate_messages/PHASE_18_gate.md. Auto-proceeding to P19 (India deployment) — reader (25 papers) IN HAND.
