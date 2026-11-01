# PROGRAM/sota/P18_sota_scan.md — Wave-1 feature implementation SOTA scan + targets

Phase P18 · RESEARCH-ONLY. MASTER_PROMPT P18 SOTA scan for each approved Wave-1 feature. All numbers SOURCE-
REPORTED (ABS) on vision/IoT/medical/molecular/air-quality benchmarks (NOT our system → transfer hypotheses).
IDs + per-paper detail in PROGRAM/reports/PHASE_18_report.md literature map. No own-system claim (Rule 16).

## 1. Current best implementation + reported gains (by feature)
- F-11 EDGE DETECTOR: HGO-YOLO 87.4% mAP@0.5 / 56 FPS CPU / 4.6 MB (2503.07371); FRS-YOLO occlusion-robust
  attention (2512.24622); quantized YOLOv4-Tiny 28.2 ms Pi5 (2506.09300); QAT+AMP+TensorRT within ~1.225%
  (2401.08105); edge-TL NEGATIVE result — TL/newer backbone don't help edge latency, YOLOv5n ~2× YOLO11n
  (2501.08639).
- F-12 TEMPORAL VALIDATION: event-validation FA 52%→4% <100 ms/frame (2607.03131); temporal smoke stacking
  ~100% video-level (2307.00104, overfit flag); FAR-bounded online threshold selection (2010.07110); density-
  weighted voting (2503.09960).
- F-13 CONFORMAL UNDER SHIFT: sketched WCP (2610.09208); W-CRC efficiency bound (2501.11413); KMM-CP coverage
  gap −>50% (2603.26415); vanilla split CP collapses 90%→65.3% PICP under moderate shift (2604.22787).
- F-14 LABEL-FREE DRIFT: DriftLens best 15/17, ≥5× faster (2406.17813); Request-and-Reverify fewer labels
  (1806.10131); conformal test-performance estimation (2207.05796); drift-detector compute benchmark
  (2304.08319).
- F-15 SENSOR DRIFT: environment-vs-instrument decomposition (2406.17488); Veli reference-free Bayesian +
  AQ-SDR benchmark (2508.02724); global multi-unit calibration (2310.18118); LSTM temporal calibration
  (2604.21527).

## 2. TARGETS section (process targets, NOT results, Rule 16)
- F-11: meet edge latency/energy ceiling at matched cross-camera recall; measure SMOKE-specific INT8 recall drop.
- F-12: pre-register FAR-driven threshold; report false-alarm reduction AGAINST detection-latency/recall cost.
- F-13: realized PICP ≈ nominal on cross-site split with weighting; reliability-flag gating via KS thresholds.
- F-14: detection-delay↔false-alarm curve under injected drift; monitor BOTH input-drift and calibration-drift;
  fit edge compute ceiling.
- F-15: decompose env vs instrument before recalibration; post-correction error gain > variance on held-out
  sensor-days.
- ALL: HELD-OUT cross-camera/cross-site split + inferential-reproducibility significance gate (2302.04054).

## 3. Honesty & gaps
All ABS/source-reported; domains differ from fixed CCTV + low-cost gas/air → transfer risk per feature. High
headlines (87.4% CPU mAP, 52%→4% FAR, ~100% video, PICP-collapse) are single-domain. Full-text reads needed
for exact hyperparameters (2503.07371, 2607.03131, 2610.09208, 2406.17813, 2406.17488). Nothing built/measured.
