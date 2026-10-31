# P2 SOTA SCAN — Literature Foundation I
# (fire/smoke/CCTV detection; video anomaly detection; evaluation/leakage/metrics;
#  robustness/distribution-shift/corruption; uncertainty/calibration/conformal/selective/OOD;
#  edge/latency/deployment vision)
# MASTER_PROMPT §0.9 (SOTA scan = first task of the phase). Evidence tags [FT]/[FT-PARTIAL]/[ABS]/[LV].
# NO claims about our own system (Rule 16). Numbers below are AS-PUBLISHED, each with its protocol.

## Phase: P2 — Literature Foundation I
## Date: 2026-10-06
## Method: arXiv export API (quoted-phrase + AND), novelty-checked vs ledger + novelty_index.
##   Highest-relevance hits promoted to ar5iv/arXiv-HTML full-text (FT-PARTIAL, D-008 caveat).

---

## 1. Fire / smoke / wildfire detection — current best + known flaws

### State of the art (as published)
- **Gradient-boosted satellite fire detection beats operational products.** 2610.01994 [ABS→queue]:
  CatBoost on GOES-ABI (300k+ VIIRS-matched detections) beats the operational GOES FDC by
  F1 +0.16–0.38 across 5 regions, incl. nighttime (FDC recall ~0.03); earlier detection on
  26/51 historic events. DIRECTLY reinforces CR-02 (simple gradient-boosting beats complex/
  operational baselines under honest eval).
- **Evidential / uncertainty-aware smoke severity.** 2605.15894 [ABS→queue]: EfficientNet-B3 +
  CBAM + evidential (Dirichlet) head on 16,298 satellite patches; 93.8% weighted acc, ECE=0.0274;
  selective prediction (keep 50% most-certain) → 96.7%. Shows epistemic-uncertainty gating as
  a false-alarm reducer (ties E-07 cost-loss + selective prediction theme).
- **On-device VLM for fire understanding.** 2609.05782 [ABS→queue]: teacher→student KD compresses
  fire-understanding VLMs for embedded sensors; semantic context reduces false alarms. Edge-vision
  relevance (WS4 River-Eye node constraints).
- **Baseline anchor already read:** 2405.00031 (SegNet drone wildfire, P1 QUOTA#10) — resolution as
  a safety hyperparameter; compact CNN competitive.

### Known flaws of fire/smoke benchmarks
- In-dataset-only evaluation is rampant; cross-site/cross-camera generalization rarely tested
  (same failure family as FM-01 spatial leakage). Smoke datasets skew to clear daytime scenes.
- Nighttime / low-visibility recall collapse (2610.01994 documents it for the operational product).

### Realistic bar under OUR limits
- A gradient-boosted / compact-CNN fire-or-smoke detector is clearly within Kaggle compute and
  MCU/Pi-class edge inference. Heavy VLMs are out at the edge (confirms WS4 doctrine).
- MUST baseline against gradient-boosting + the operational product analogue, under cross-site CV.

---

## 2. Video anomaly detection (CCTV / surveillance) — current best + known flaws

### State of the art (as published)
- **Field is fragmenting DNN → MLLM.** Two 2025 surveys to mine:
  2508.14203 [ABS→queue] (VAD via deep learning: human/vehicle/environment; online/active/
  continual) and 2507.21649 [ABS→queue] (DNN→MLLM unified framework). Seed the queue.
- **Weakly-supervised VAD** (video-level labels only) is the dominant practical paradigm:
  2610.05129 [ABS→queue] (representation–behavior alignment, 0.012% params), 2609.07455
  [ABS→queue] (federated, parser-free VLM verification). Benchmarks: UCF-Crime, XD-Violence,
  ShanghaiTech.
- **Baseline anchors already read:** HF²-VAD (2108.06852), MemAE (1904.02639) — reconstruction/
  memory-based one-class VAD lineage (background from P0/P1).

### Known flaws of VAD benchmarks
- UCF-Crime / ShanghaiTech frame-AUC is saturated and criticized; "anomaly" is dataset-specific
  and rarely matches a deployment's hazard definition. Cross-dataset transfer is weak.
- VLM-based methods trade huge compute for explanation — impractical at a ₹2000 edge node.

### Realistic bar under OUR limits
- Edge VAD must be a compact reconstruction/forecast-residual or classical-feature detector,
  NOT an MLLM. River-Eye LSPIV is a physics-grounded alternative to generic VAD (WS4).

---

## 3. Evaluation / leakage / metric critiques — current best practice

### State of the art (as published)
- **Leakage-controlled evaluation is now its own research thread.** 2610.04927 (MLE-InsightBench,
  leakage as a validity threat in agentic ML) and leakage-controlled clinical ML (2610.xxxx CKD)
  show held-out-by-construction protocols. Directly supports FM-01 doctrine.
- **Application-driven, saturation-aware AD benchmarks.** 2610.04392 [ABS→queue] (VAND 4.0:
  hidden-test, efficiency as a first-class metric, rare-defect collapse spillage ~53 AP / missing
  ~27 AP; DINOv3 backbones dominate shift robustness). A model for how to design an honest,
  deployment-driven benchmark + the rare-event collapse warning (ties FM-21 metric mirage).
- **Baseline anchors already read:** 2206.09981 (imbalance metric sensitivity, QUOTA#7),
  2601.05921 (cost-loss Value Score, QUOTA#15 → E-07, PRIMARY EWS metric).

### Known flaws
- Benchmark saturation hides deployment gaps; rare-class performance is where systems fail and
  where metrics are least reliable (2610.04392, 2206.09981).

### Realistic bar under OUR limits
- Report cost-loss Value Score (E-07) + per-regime base-rate-matched metrics; hidden/held-out
  spatial test; efficiency (latency, memory, power) as a first-class metric.

---

## 4. Robustness / distribution-shift / corruption

### State of the art (as published)
- **Corruption-robustness does NOT transfer across corruption classes.** 2606.07593 [ABS→queue]:
  adversarial/corruption fine-tuning of ViTs improves on seen corruptions but fails to transfer
  to unseen ones; sparse representations unchanged. Direct warning: training on known perturbations
  will not cover field conditions we did not anticipate (FM robustness).
- **Biologically-inspired front-ends** give cumulative corruption robustness (VOneNet/EVNet lineage,
  2409.xxxx) — a cheap architectural robustness lever.
- **Shift robustness tracked in AD benchmarks** (2610.04392: "robustness to distribution shift
  remains a key open challenge; DINOv3 backbones dominate").

### Known flaws / open problems
- No single training-time fix covers all shift types; evaluation must enumerate the shifts we
  actually expect (sensor dropout, seasonal, cross-site, weather) rather than generic corruptions.

### Realistic bar under OUR limits
- Enumerate expected shifts; test each explicitly; prefer architectural + conformal/OOD guards
  over hoping corruption-training transfers.

---

## 5. Uncertainty / calibration / conformal / selective prediction / OOD

### State of the art (as published)
- **Conformal prediction for time series is an active, UNSOLVED-coverage area.** 2610.02777
  [ABS→queue] (PID-Expert online aggregation; local coverage degrades right after abrupt shifts —
  the exact TRINETRA failure window). Plus queued HopCPT (2303.12783), ACI/AgACI (2202.07282),
  EnbPI already read (2010.09107, QUOTA#4). Confirms CR-04: coverage is approximate + shift-sensitive.
- **Calibrator capacity is a finite-sample design choice.** 2609.38936 [ABS→queue]: with only a
  few-thousand-example calibration split, scalar temperature underfits structured miscalibration;
  routed low-capacity calibrators win at small budgets. Reinforces 2306.04590 (QUOTA#13, proximity
  bias) — temperature scaling is NOT a universal fix (FM-20).
- **OOD on time series mostly fails** (2502.15901, already in ledger ABS; TS-OOD benchmark).
- **Evidential UQ caveats** (2402.09056 ledger: epistemic estimates only relative).

### Known flaws
- Marginal coverage ≠ conditional coverage; calibration measured on-distribution says nothing
  under shift; OOD detectors from vision don't lift onto sensor streams.

### Realistic bar under OUR limits
- Per-zone/per-regime conformal (Mondrian) with honest coverage reporting; selective prediction /
  abstention as a safety lever; OOD validated per-modality, not borrowed from vision.

---

## 6. Edge / latency / deployment vision

### State of the art (as published)
- **Efficient segmentation/detection backbones for cameras/drones** (ArmFormer 2510.xxxx: 80.6%
  mIoU @ 82 FPS, 3.66M params; YOLOv8/v11 under adverse weather in developing countries 2606.12066
  [ABS→queue]). Shows the compact-model frontier that fits River-Eye / embedded vision.
- **Efficiency as a first-class benchmark metric** (2610.04392): throughput + memory + power co-reported.

### Realistic bar under OUR limits
- River-Eye LSPIV + a compact detector (YOLOv8-n / tiny segmenter) on Pi-class hardware; validate
  under adverse weather (fog, rain, night) because developing-country/field conditions degrade it.

---

## 7. Baselines we MUST use first (fair-comparison, carried from P1 + extended)
- Persistence (temporal), gradient-boosted trees (tabular/satellite — 2610.01994 shows these beat
  operational products), 3-rule tree (lake hazards, 2608.12422), reconstruction/forecast-residual
  one-class (VAD), operational-product analogue (GOES-FDC-style / LHASA) where one exists.
- Every deep claim must clear these under cross-site/spatial CV with the cost-loss Value Score (E-07).

## 8. SOTA targets + protocol plan — COMPLETED at phase exit 2026-10-06
(Published numbers we may need to meet/beat + the protocol a fair comparison requires. NO own-system
claims — Rule 16. Every number is AS-PUBLISHED on its own dataset/protocol; it is NOT a TRINETRA
result and does NOT transfer without re-measurement on our data under our CV.)

### 8.1 Published SOTA anchor numbers (per task, with protocol) — the "bar"
| Task | Published anchor | Number (as-published) | Protocol / dataset | Caveat before we cite it as a target |
|---|---|---|---|---|
| Flood segmentation (edge) | 2609.20441 | water IoU: student 0.787 / teacher 0.822; MNDWI rule competitive on 2 external benchmarks | Sen1Floods11 test; STURM-Flood/WorldFloods-v2 external | External benchmarks = generalization tests; a FIXED spectral rule matches both → beat MNDWI first |
| Flood-seg edge footprint | 2609.20441 | 1.5 MB INT8, 5.57 ms/512², ~14 MB RAM | Jetson Xavier NX, TensorRT | Our node may be cheaper than Xavier NX; re-profile on target HW |
| Flash-flood EWS (operational) | 2605.20167 | 90.9% acc / 89.2% F1 / AUC 0.939; alert ~3 days early | LOOCV over 77 real-SAR events, Bangladesh haor | Different basin/hazard; LOOCV-over-events; must re-measure on Himalaya w/ spatial+event CV |
| Wildfire ignition | 2610.01994 | GBT beats operational GOES-FDC by F1 +0.16–0.38 | 5 regions, VIIRS-matched | Satellite fire ≠ our ground CCTV smoke; shows "beat the operational product" bar |
| Smoke severity + UQ | 2605.15894 | 93.8% wtd acc, ECE 0.0274; selective 50%→96.7% | 16,298 patches, in-dataset | In-dataset only; cross-region drop untested → treat as ceiling not target |
| Precip nowcasting | 2609.17175 | lower CRPS than STEPS+DGMR at all leads; MAE edge only ≤90 min | Italy radar composite | Radar-dense Italy; Himalaya is GPM/forecast-sparse → transfer is HYPOTHESIS |
| InSAR deformation forecast | 2509.18176 | CNN-LSTM > LightGBM/LASSO; baselines default to persistence | eastern Ireland, Sentinel-1, single-step | Must beat PERSISTENCE and report skill-over-persistence; multi-horizon untested |
| WSVAD (CCTV) | 2609.05066 / 2507.21649 survey | near-SOTA frame-AUC (UCF-Crime) / AP (XD-Violence) | in-dataset UCF/XD | frame-AUC optimistic (FM-21); cross-scene transfer weak → not a deployment target as-is |

### 8.2 The PROTOCOL any fair comparison must satisfy (synthesized across P2 reads)
1. **Two mandatory baselines, always:** (a) a FIXED physical/spectral rule (MNDWI for water
   2609.20441; FS/physics gate for slopes; threshold for alarms) AND (b) PERSISTENCE for any
   forecast (2509.18176, 2609.17175). Report **skill-over-baseline**, never raw metric alone. (CR-02)
2. **Spatial + event-held-out CV, not random split** (2608.12422 GLOF; 2605.20167 LOOCV-over-events).
   Random pixel/frame splits leak and inflate (FM-01).
3. **Anti-leakage preprocessing + disclosure:** deseasonalize seasonal inputs via monthly
   climatological anomaly and REPORT feature–label correlation before/after (2605.20167: r
   0.570→−0.031). Group chips→maps→events to prevent scene leakage (2609.20441).
4. **Probabilistic + calibration metrics, not just point accuracy:** CRPS + rank histogram (+RAPSD
   for spatial fields) for forecasts (2609.17175); ECE + selective-prediction curve for classifiers
   (2605.15894); conformal coverage with the caveat that coverage degrades right after distribution
   shift / at hazard onset (2610.02777) → back with a hard physics shield.
5. **Rare-event-aware + cost-weighted scoring:** frame-AUC/accuracy are optimistic under extreme
   imbalance (FM-21, 2610.04392); report the cost-loss Value Score (E-07) and recall at fixed
   false-alarm budget (2606.21130).
6. **Robustness must be measured per-corruption, not assumed:** augmenting for one corruption does
   NOT transfer to others (2606.07593) → test fog/rain/night/low-light each explicitly, don't claim
   general weather-robustness from one augmentation.
7. **Encoder selection by on-OUR-task evaluation, not leaderboard:** GeoFM rankings flip by task and
   pretraining objective; probe mid-layers; budget fine-tune representation shift (2606.13896) →
   structures the CR-01 trade study (P7).
8. **Edge numbers re-profiled on target hardware** at INT8 with QAT, reporting MB + ms + runtime RAM
   (2609.20441 template), not just FLOPs.

### 8.3 What this means for TRINETRA targets (honest framing, Rule 16)
- We do NOT yet have any TRINETRA performance number and will not claim one until built (Rule 16).
- The published anchors above are **comparison bars on THEIR data**, not our expected results.
- The DEFENSIBLE near-term target is: *match or beat the two mandatory baselines (fixed rule +
  persistence) on OUR Himalayan data under spatial/event CV, with calibrated uncertainty and a
  cost-loss score* — a process target, not a leaderboard number. Everything else is a hypothesis
  pending the build phases.

### 8.4 Protocol items handed to specific later phases
- P6: edge HW re-profiling + BOM price re-verification (Wayback).
- P7: CR-01 encoder trade study using 2606.13896 methodology (on-our-task + layerwise probe + CKA).
- P15: full cry-wolf / alert-fatigue ODE (2104.11422) + socio-meteorology.
- Build phases: implement §8.2 protocol as the standing evaluation harness spec (research design doc
  only in research-only phases).
