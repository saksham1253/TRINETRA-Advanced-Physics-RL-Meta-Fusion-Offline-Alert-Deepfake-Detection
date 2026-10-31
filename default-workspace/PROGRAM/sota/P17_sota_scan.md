# PROGRAM/sota/P17_sota_scan.md — feature-scouting SOTA scan (continual improvement)

Phase P17 · RESEARCH-ONLY. MASTER_PROMPT P17. Current best buildable FEATURE techniques + reported gains, for
the FEATURES.md register. All numbers SOURCE-REPORTED (Rule 16) on vision/IoT benchmarks (NOT our system →
transfer hypotheses). Detail + IDs in PROGRAM/reports/P17_scout_notes.md. No own-system claim.

## 1. SOTA by feature area (source-reported)
- EFFICIENT CCTV DETECTION: EFA-YOLO 1.4M params / 22.19 ms CPU, ~88× faster than mainstream YOLO (2409.12635);
  Light-YOLOv5 +3.3% mAP / −27% params / 91 FPS (2208.13422); MobileViT-S KD compact + fast (2502.20979);
  WISE weak-sup 0.12M params tile-F1 0.964 (2609.18227); two-stage UAV cascade (2508.16739).
- TEMPORAL/MULTIMODAL CUES: STCNet two-stream +6.2% on RISE smoke (2011.04863); obscured-flame 3D-conv Dice
  85.88% (2307.00104, overfit red flag); SmokeyNet camera+weather better time-to-detection (2212.14143);
  unsupervised IR optical-flow 95.39% frame no labels (1909.12937); thermal/IR fusion mAP@0.5 95% Jetson Nano
  (2307.04223).
- LABEL EFFICIENCY: FireMatch SSL 76.92%/91.81% (2311.05168); SIAVC SSL 88.76%/89.13% + ECA9 dataset
  (2405.14506).
- FUSION/CALIBRATION ADD-ONS: WCPS covariate-shift conformal (2404.15018); self-calibrating CP (2402.07307);
  noise-aware conformal NACP (2501.12749).
- ALERTING/OPS: temporal event validation FA 52%→4% <100 ms/frame (2607.03131); STUDD label-free drift
  (2103.00903); CUSUM calibration monitor (2510.25573); conformal sets improve operator accuracy RCT
  (2401.13744).
- IoT: GP drift correction −up to 90% MSE + calibration scheduling (2506.09186); PRNet blind calibration
  (1707.03682); env-vs-instrument drift separation (2406.17488).
- EXPERIMENT TOOLING: dagger provenance (2006.07484); inferential-reproducibility LMEM+GLRT real-win test
  (2302.04054).

## 2. TARGETS section (process targets, NOT results, Rule 16)
- Wave-1 adopts (cheap, measurable, low engineering): EFA-YOLO (F-11), temporal event validation (F-12),
  post-hoc conformal under shift (F-13), label-free drift monitors (F-14), GP IoT drift correction (F-15),
  IR optical-flow feature (F-16), tooling (F-17).
- Every candidate gated by: held-out CROSS-CAMERA/CROSS-SITE eval + inferential-reproducibility significance
  test (2302.04054); improvement must exceed seed/trial variance; a benchmark-local win that hurts cross-
  camera is NOT a win.
- Hard constraints enforced: Kaggle GPU budget, INR 2000 prototype cap, offline operation, privacy, Rule 19,
  free-only datasets.

## 3. Honesty & gaps
All ABS/source-reported on non-fire or single-dataset benchmarks → re-test. Micro-arch mAP gains, >98% single-
split headlines, framerate/codec-sensitive temporal cues, pseudo-label confirmation bias, and conformal
coverage breaking under shift are explicit "not-a-real-win" risks. No feature is built or measured here.
