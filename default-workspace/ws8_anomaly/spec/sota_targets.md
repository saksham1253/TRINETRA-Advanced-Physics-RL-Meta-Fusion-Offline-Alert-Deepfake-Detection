# ws8_anomaly/spec/sota_targets.md — SOTA scan update, published targets, quota list, default-recipe registry (P10, WS8b)

RESEARCH-ONLY. MASTER_PROMPT P10 tasks 1, 6, 7. All numbers SOURCE-REPORTED ("not ours", Rule 16); all 23
P10 papers are ABS depth (abstracts only; not independently re-fetched → disclosed residual risk). This file
is the citable DEFAULT-RECIPE registry the per-family specs point to (so "every default has a source").

## 1. SOTA scan update (newer than P9; implementation-level)
No result overturns the P9 scope/priorities. New since-P9 implementation evidence sharpens the recipes:
- Thresholding has matured to CONFORMAL + EVT (not hand-picked thresholds): `nonconform` conformal p-values
  + FDR control (2605.13642); EVT PoT + dual-threshold hysteresis + trimmed-tail fit on streaming scores
  (2601.21293); factorwise split-conformal to hit a nominal FPR (2609.29580).
- Reconstruction baselines remain strongly competitive on the rigorous TSB-AD/UCR, and INFERENCE WINDOWING
  (overlapping vs disjoint) can matter as much as architecture (2606.09874).
- Zero-shot forecasting foundation models FAIL on persistent anomalies (2607.12454) — a direct caution
  against a naive TimesFM detector; they are change-point detectors.
- Edge anomaly now has concrete integer-only recipes (QAT 4-8 bit + HW-aware search, 2505.17662) and
  MCU-friendly HDC (2606.13754).
- Video anomaly has tiny/fast edge recipes (~2M params, 155 FPS, 2601.18135) and a cost-controlled SSL→LLM
  escalation pattern (2509.22544), plus ANTICIPATION (early-warning) via self-distilled score matching
  (2610.11149) — aligned with our early-warning goal.

## 2. Published baselines to reproduce FIRST + the numbers they should reach (their own protocols, source-reported)
These are the detectors we reproduce before building anything new; targets are THEIR reported numbers under
THEIR protocols — a fair comparison requires matching protocol/splits/metric (see §4).
- PCA / Isolation Forest / LOF / OCSVM on ADBench + TSB-AD + SMD (simple-baseline floor; PCA ≥ OmniAnomaly
  w/o point-adjust, 2603.18985 [P9]).
- Reconstruction AE / DLinear / TimesNet / Transformer on TSB-AD with OVERLAPPING inference windows
  (2606.09874) — reproduce the +28% overlapping-vs-disjoint effect.
- RIFT vs IF on ADBench (seed-stable IF replacement; comparable accuracy, lower variance — 2610.12244).
- Matrix-profile discord (sketch) on water-treatment/transport (≥50× throughput — 2311.03393).
- CPS: SWaT/WADI with ASTRO F1 0.990/0.788 [P9 2605.25135] and PhaseNet++ SWaT F1 90.98% [P9 2605.00929]
  (watch cross-protocol comparability — their caveat).
- Video: FoGA (155 FPS, 2601.18135), VADMamba++ (2604.00360), HyCoVAD 72.5% frame-AUC on ComplexVAD
  (2509.22544) — but report Within-AUROC/region metrics, NOT Micro-AUROC alone (2608.21854 [P9]).

## 3. DEFAULT-RECIPE REGISTRY (cited) — referenced by the family specs
### Thresholding / false-alarm (family A/all)
- EVT Peaks-Over-Threshold + dual-threshold hysteresis + trimmed-tail fit on streaming scores → tunable,
  auditable alarm-rate budget. [2601.21293]
- Split-conformal calibration → p-values → Benjamini-Hochberg FDR control at a target level (instead of a
  fixed threshold); `nonconform` is the reference implementation path wrapping any PyOD/sklearn detector.
  [2605.13642]
- Factorwise split-conformal to hit a nominal FPR; AUDIT train/test row overlap before trusting AUROC.
  [2609.29580]
- Multi-entity shared model: per-feature thresholds from validation residual quantiles. [2605.00482]
- Multiple-testing / look-elsewhere correction when scanning many sensors/regions (uncalibrated scanning
  fabricates false significances). [2606.13780]
### Deep MTAD training (family B, if a deep model earns its place)
- Reconstruction detectors: OVERLAPPING inference windows (avg +28% rel.); multi-seed + fixed tuning on
  TSB-AD. [2606.09874]
- EMA target encoder + masked query-prediction auxiliary score fused with reconstruction error (catches
  dependency-shift anomalies reconstruction misses). [2603.12916]
- Channel-aware contrastive weighting by per-channel reconstruction-error relevance. [2605.23139]
- Wavelet self-distillation pretrain + frozen linear-probe head (strong cheap baseline; time-freq aug beats
  spatial aug). [2609.39337]
- Cross-modal reconstruct-each-from-others + adaptive test-time threshold (multi-modal + OOD robustness).
  [2609.16314]
- Reconstruction/residual AEs: do NOT train to convergence — early-stop or add Kernel-Anchored Regularizer
  (KAR); KCM is a training-free closed-form baseline. [2610.02345]
- Do NOT use naive zero-shot forecasting FMs for persistent anomalies (use as change-point detectors only).
  [2607.12454]
### Score calibration / uncertainty (family C)
- Conformal risk-control head → threshold-free, coverage-guaranteed scores (isolable ~1.9 AUROC, ~29% FPR
  reduction). [2609.14234]
- Mondrian/weighted conformal post-hoc calibration to repair calibration-vs-deployment drift. [2606.13780]
- CLEAR post-hoc latent-conflict calibrator, no retraining, for OOD/adversarial. [2610.01384]
- Single-pass evidential (Dirichlet) uncertainty, Wasserstein objective, order tuned per backbone (2nd CNN /
  3rd transformer) — cheaper than MC-dropout/ensembles. [2610.10116]
### Classic / simple (family B/D baselines)
- RIFT / RIFT-ensemble as deterministic, seed-stable IF replacement. [2610.12244]
- Matrix-profile discord with sketch (cost independent of #channels; dynamic channel add/delete). [2311.03393]
- SSL-latent-compression + IF/OCSVM/LOF as bandwidth-frugal edge baseline + send-only-anomalous alerting.
  [2610.03649]
### Edge / TinyML (edge_spec)
- QAT 4-bit (8-bit INT8 for MCUs) + Optuna hardware-aware HP search → integer-only accelerator; 0.033
  mJ/inference, ms latency (FPGA — MCU to be measured). [2505.17662]
- Hyperdimensional Computing, binary ops, MCU-friendly (encoding is the real contributor, +5.4% ROC-AUC).
  [2606.13754]
- Achievable budget reference: sub-1 MB, <7 ms Jetson p99 + EVT dual-threshold. [2601.21293]
### Video (family A, support-only)
- Tiny U-Net future-frame + forward-consistency loss, fuse immediate+forward errors (~2M params, up to 155
  FPS). [2601.18135]
- Gray→RGB single-proxy reconstruction (drops optical flow) + fuse prediction/quantized-feature errors.
  [2604.00360]
- Denoising-score-matching likelihood + motion-aware weighting; SDSM for label-free ANTICIPATION (early
  warning). [2610.11149]
- SSL pre-screen → LLM validate suspect frames only (cost-controlled escalation) + their adaptive
  thresholding protocol. [2509.22544]
- Weakly-supervised MIL + Proximity-Aware Top-k for where+when localization without boxes. [2606.29498]

## 4. Fair-comparison requirements (protocol differences to watch)
- MATCH splits (time/group), the metric (prefer VUS-PR / PATE / Within-AUROC; NEVER point-adjust as primary),
  the thresholding rule (conformal/EVT on validation), and the inference windowing (overlapping) across all
  compared methods — otherwise deep-vs-simple comparisons are invalid (2603.18985, 2606.09874, 2605.00929).
- AUDIT dataset train/test overlap before trusting AUROC (2609.29580).
- Report seeds + CIs; for reconstruction/residual detectors report the early-stop/KAR setting (2610.02345).

## 5. Quota list — 23 NEW P10 primary arXiv papers (ABS)
A: 2601.21293, 2605.13642, 2609.29580, 2605.00482 · B: 2606.09874, 2603.12916, 2605.23139, 2609.39337,
2607.12454, 2609.16314 · C: 2609.14234, 2606.13780, 2610.01384, 2610.10116 · D: 2610.12244, 2610.02345,
2311.03393, 2610.03649 · E(edge): 2505.17662, 2606.13754 · F(video): 2601.18135, 2604.00360, 2610.11149,
2509.22544, 2606.29498. (Counted = 23 distinct; 2610.03649 also appeared in the P4 WS8 brief but was NOT
previously counted in a quota, so it is counted once here as a NEW primary read.)
Depth: all ABS (0 FT). Running body-level deep FT NEW total UNCHANGED at 100.

## 6. What the quota changed (task 7)
- Thresholding switched from "pick a threshold" to CONFORMAL p-values + FDR / EVT-hysteresis as the DEFAULT
  (family_b §7, family_c §6, integration alert-fatigue).
- Added the "train-to-convergence is a bug" rule for reconstruction/residual detectors (family_b §6/§11,
  family_d).
- Hardened the deep-vs-simple protocol (overlapping windows; row-overlap audit; no naive zero-shot FM for
  persistent anomalies).
- Edge path gained concrete recipes (QAT+HW-search, HDC) replacing generic placeholders (edge_spec §2/§3).
- Video path gained tiny-fast + anticipation + cost-controlled-escalation recipes (family_a §5).

## 7. Honesty
All numbers source-reported from abstracts; not independently re-fetched (residual risk). Edge figures are
on FPGA/Jetson/other hardware — our MCU numbers MUST be measured in P13. Reproduce-first baselines are a
plan, not a result; nothing was built or run.
