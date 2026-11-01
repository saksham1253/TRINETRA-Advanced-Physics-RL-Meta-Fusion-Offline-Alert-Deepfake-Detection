# features/wave1_specs.md — Wave-1 feature specifications & measurement plans (P18)

Phase P18 · RESEARCH-ONLY. MASTER_PROMPT P18. Ready-to-build specs for the Wave-1 features APPROVED at the P17
gate (F-11..F-17). NOTHING is implemented or measured (Rule 16). All numbers SOURCE-REPORTED (ABS). Rule 19:
advisory, human-in-the-loop; any monitor/auto-adapt stays advisory. Every spec pre-registers a decision rule;
the shared "real-win" gate is the inferential-reproducibility test (2302.04054) + a HELD-OUT CROSS-CAMERA/
CROSS-SITE split. Shift-monitoring (P16) and calibration (P14) bind here.

Build-time follow-up (honest): hyperparameter specifics beyond abstracts need full-text reads of the highest-
value PDFs flagged by the P18 reader (2503.07371, 2607.03131, 2610.09208, 2406.17813, 2406.17488).

---
## F-11 — Efficient edge CCTV fire/smoke detector
- DESIGN / PLUG-IN: compact YOLO-family detector as the P8 perception front-end feeding P14 fusion. Candidate
  blocks: EFA-YOLO EAConv/EADown (2409.12635); GhostConv backbone + parameter-sharing head (HGO-YOLO
  2503.07371); detachable cross-dimensional attention + dynamic foreground sampler for smoke occlusion
  (FRS-YOLO 2512.24622).
- CONFIG/BUILD FLAGS: backbone variant (yolov5n|efa|ghost), compression ratio, attention on/off, quantization
  mode {none, PTQ-INT8, QAT+AMP+TensorRT}, PTQ calibration-set size, per-tensor vs per-channel.
- I/O: in = RGB frame; out = boxes {flame,smoke} + confidences.
- HYPERPARAMS (defaults w/ sources): GhostConv ratio + OptiConvDetect shared-channel split (2503.07371); QAT vs
  PTQ + TensorRT precision mode (2401.08105 keeps within ~1.225%; PTQ-only recipe 2506.09300 28.2 ms Pi5);
  prefer YOLOv5n over YOLO11n on CPU-only (2501.08639).
- ABLATION: backbone×quantization grid on SAME cross-camera split, feature on/off, same seeds; stress = night/
  low-contrast, compression, smoke-only.
- METRICS: mAP@0.5 + recall AT MATCHED precision, latency/energy on target edge HW, SMOKE-SPECIFIC recall.
- DECISION RULE (pre-registered): keep a variant only if cross-camera mAP/recall gain > seed variance AND it
  meets the edge latency/energy ceiling; a win on one dataset that hurts cross-camera is NOT a win.
- COST: single-GPU retrain; CPU-real-time inference (low).
- RISKS / NEW FAILURE MODES: INT8 PTQ disproportionately hurts diffuse smoke recall (measure it, 2506.09300);
  accuracy tricks (TL, newer backbone) may not help the edge-latency objective (negative result 2501.08639);
  aerial/mixed-class training may not transfer to fixed CCTV (2512.24622, 2503.07371). Feeds robustness
  catalogue (P16): adversarial patches on this detector.

---
## F-12 — Temporal multi-frame event validation (false-alarm reduction)
- DESIGN / PLUG-IN: post-processor over frame-level detections → events; sits between P8 detector and P12
  alert tiering. Multi-frame confirmation + confidence-weighted voting + cascaded filtering (2607.03131).
- CONFIG/BUILD FLAGS: confirmation window length (#frames), vote-weight function, cascade thresholds, FAR
  target.
- I/O: in = per-frame detections + confidences; out = confirmed EVENT + event confidence + latency stamp.
- HYPERPARAMS (defaults w/ sources): window length + vote weights + cascade thresholds (2607.03131, FA
  52%→4% src-reported); FAR-driven threshold selection from a target false-alarm rate rather than hand-tuning
  (2010.07110); optional density-weighted base-learner routing (2503.09960).
- ABLATION: sweep confirmation window; measure false-alarm reduction AGAINST induced detection latency and
  recall loss (the headline FAR drop HIDES latency cost — mandatory).
- METRICS: false-alarms/day, time-to-detection (latency), recall at matched sensitivity, event-level precision.
- DECISION RULE: keep only if false-alarm reduction holds cross-site at matched sensitivity WITHOUT raising
  missed-event rate or pushing latency past the alert deadline.
- COST: very low (post-processor, no retrain).
- RISKS: longer window ⇒ later alert; FAR guarantees assume stationary nominal distribution — breaks under
  shift (2010.07110) → pair with F-14 monitor. Rule 19: still advisory into human review.

---
## F-13 — Post-hoc conformal calibration under covariate shift
- DESIGN / PLUG-IN: calibrates the P14 fused output (and/or F-11 detector) into valid prediction sets/
  intervals; the shift-robust layer of the fusion calibration stack.
- CONFIG/BUILD FLAGS: method {WCPS 2404.15018, self-calib Venn-Abers 2402.07307, noise-aware NACP 2501.12749,
  sketched 2610.09208, KMM 2603.26415}, target α, weight/sketch estimator, KS reliability-flag thresholds.
- I/O: in = scores + calibration set (possibly noisy/shifted); out = calibrated sets/intervals + reliability
  flag {High/Med/Low/Unreliable}.
- HYPERPARAMS (defaults w/ sources): likelihood-ratio reweighting (2404.15018); sketch map T with leakage
  Δ_T≈0 (2610.09208); KMM kernel/bandwidth + overlap-selection (2603.26415); calibration-set size vs assumed
  shift (2501.11413); per-feature KS thresholds gating reliability (2604.22787).
- ABLATION: inject graded covariate shift; realized coverage (PICP) vs nominal; weighted vs unweighted.
- METRICS: PICP vs nominal, set size/efficiency, coverage gap under shift.
- DECISION RULE: keep only if realized coverage stays valid on the cross-site split; NEVER claim 1−α coverage
  cross-site without weighting (vanilla split CP collapsed 90%→65.3%, 2604.22787).
- COST: low, post-hoc (density/weight estimate).
- RISKS: coverage drops by the leakage term if the sketch discards a label-relevant shift direction
  (2610.09208); selective KMM abstains on low-overlap regions — exactly the novel fire conditions we care about
  (2603.26415); concept drift (P(Y|X) change) voids covariate-shift bounds (2501.11413) → F-14.

---
## F-14 — Label-free drift & calibration monitoring (advisory)
- DESIGN / PLUG-IN: runtime monitor on P8/P14 outputs; raises an ADVISORY recalibration/review flag (Rule 19 —
  never autonomous retrain-and-act). Student-teacher drift (STUDD 2103.00903) + CUSUM calibration chart
  (2510.25573) + representation-distance drift (DriftLens 2406.17813).
- CONFIG/BUILD FLAGS: reference-window construction + size, distance/CUSUM thresholds, label-request budget,
  on-device runtime ceiling.
- I/O: in = streaming outputs (+ occasional labels); out = drift/miscalibration ADVISORY + representative
  drift samples.
- HYPERPARAMS (defaults w/ sources): reference window + distance threshold (2406.17813); CUSUM dynamic limits
  (2510.25573); two-tier unlabeled alarm + label-request budget (Request-and-Reverify 1806.10131); black-box
  conformal test-performance estimator score (2207.05796); runtime/throughput ceiling (2304.08319).
- ABLATION: detection-delay ↔ false-alarm-rate curve under injected drift; input-drift vs calibration-drift
  monitors separately.
- METRICS: detection delay, monitor false-alarm rate, runtime on edge.
- DECISION RULE: keep only if delay/false-alarm beats a fixed-threshold baseline on replayed drift AND fits the
  edge compute budget.
- COST: very low (aux model + chart, model-agnostic).
- RISKS: representation drift ≠ performance/calibration drift (2406.17813) → monitor BOTH; confidence-based
  layer-1 is miscalibrated under the very shift being detected (1806.10131) → never rely on softmax alone;
  accuracy-chosen detector may blow the edge budget (2304.08319).

---
## F-15 — IoT sensor drift correction + calibration scheduling
- DESIGN / PLUG-IN: on the WS7 node / gateway; corrects low-cost gas/air sensor drift and schedules
  recalibration before data enters fusion. GP drift model + uncertainty-driven schedule (2506.09186); blind
  CNN recovery (PRNet 1707.03682); reference-free Bayesian disentanglement (Veli 2508.02724).
- CONFIG/BUILD FLAGS: corrector {GP, PRNet-blind, Veli-VI, LSTM-supervised, global-law}, environmental
  covariates in drift model, recalibration-schedule objective, #reference-co-located units.
- I/O: in = raw sensor stream (+T/RH); out = drift-corrected values + uncertainty + recalibration advisory.
- HYPERPARAMS (defaults w/ sources): environmental covariates T/RH entered into drift decomposition
  (2406.17488); latent-noise prior/disentanglement (2508.02724); #co-located units + fabrication tolerance for
  a global law (2310.18118); LSTM lookback + lag/harmonic features if supervised (2604.21527).
- ABLATION: before each scheduled recalibration, DECOMPOSE drift into environmental vs instrumental
  (2406.17488); corrected error on held-out sensor-days; blind vs supervised vs global-law.
- METRICS: post-correction MSE/R² on held-out sensor-days, calibration-budget used, uncertainty width.
- DECISION RULE: keep only if post-correction error improvement > seed/trial variance on HELD-OUT sensor-days.
- COST: low-moderate (GP scales with data; cheap inference).
- RISKS: recalibrating against environment-driven apparent drift wastes budget + injects error (2406.17488 —
  THE pitfall); blind corrector may "explain away" a true event as noise (2508.02724); global law silently
  mis-corrects an outlier/drifting unit (2310.18118) → pair with F-14 per-unit monitor; supervised LSTM needs
  co-located reference and overfits site seasonality (2604.21527).

---
## F-16 — Unsupervised IR optical-flow / flicker physics feature (label-free cold-start)
- DESIGN / PLUG-IN: classical-CV feature (optical flow + divergence + intensity, MRF/MAP) giving a label-free
  flame/smoke-motion signal into P14 fusion; also a cold-start detector before any trained model (1909.12937).
- CONFIG/BUILD FLAGS: flow method, divergence threshold, MRF neighborhood, frame rate assumptions.
- I/O: in = IR/RGB video; out = motion-based flame/smoke mask + confidence.
- HYPERPARAMS: flow + divergence + intensity fusion weights, MRF/MAP clustering params (1909.12937, 95.39%
  frame src-reported no labels).
- ABLATION: with vs without the flow feature on cross-site video; sensitivity to framerate/codec/PTZ.
- METRICS: added signal (ΔAUC/Δrecall) over RGB-only at matched FA; robustness to framerate/compression.
- DECISION RULE: keep only if it adds signal over RGB-only on the cross-site split; drop if framerate/codec/PTZ
  variance erases the gain.
- COST: very low (no GPU/labels).
- RISKS: optical-flow/flicker is framerate-, codec-, and PTZ-motion-sensitive — a curated-video gain can hurt
  on compressed CCTV; nuisance motion (steam, moving foliage) false positives → corroborate (P14/P16).

---
## F-17 — Experiment tooling + inferential-reproducibility ("real-win") gate
- DESIGN / PLUG-IN: cross-cutting build-infra; provenance tracking (dagger 2006.07484) + the significance gate
  every other feature passes (LMEM + GLRT variance analysis, 2302.04054).
- CONFIG/BUILD FLAGS: experiment-state tracking on; LMEM random effects (seed, camera, site); GLRT α.
- I/O: in = per-run metrics across seeds/cameras; out = significance verdict (is the gain > noise?) + reliability coefficient.
- HYPERPARAMS: random-effect structure + reliability-coefficient threshold (2302.04054).
- ABLATION: n/a (enabler); validate that it correctly rejects seed-noise "improvements".
- METRICS: variance components, GLRT p-value, reliability coefficient.
- DECISION RULE: a feature is "a real win" ONLY if its improvement is significant under this test on a held-out
  cross-camera split; otherwise rejected regardless of headline number.
- COST: very low (library adoption + analysis layer). No model impact.
- RISKS: none to the model; prevents the program-wide trap of promoting benchmark-local or seed-noise gains.

---
## Measurement-plan summary (all Wave-1)
Same split, same seeds, feature on vs off, stress conditions; HELD-OUT CROSS-CAMERA/CROSS-SITE evaluation
mandatory; proper scoring + calibration (P14) and worst-case/shift reporting (P16); every "win" confirmed by
F-17. Honest negatives are reportable outcomes. Nothing trained/measured in this phase.
