# PROGRAM/sota/P9_sota_scan.md — anomaly detection SOTA scan (WS8a)

Phase P9 · RESEARCH-ONLY. SOTA per anomaly family, with the benchmark/metric/protocol each number is tied
to, the published CRITICISMS of those numbers, and the realistic bar for a build under our limits (Kaggle
≤~30 GPU-h shared; ESP32-class edge; offline-first; India). No own-system performance claim (Rule 16); every
external number is SOURCE-REPORTED. Literature IDs/numbers to be filled from ws8_anomaly/literature_map.md
(reading subagent 45bd70cb running); this scan is the framing + known-SOTA skeleton.

## 0. Cross-cutting message (the single most important finding)
The anomaly-detection literature has a well-documented EVALUATION-INTEGRITY problem: many headline numbers
come from protocols that inflate scores (the "point-adjust" trick on time-series, thresholds tuned on the
test set, trivial/mislabeled benchmarks, random frame-level splits that leak, and synthetic-injection setups
that are too easy). Several widely-cited critiques show that under strict protocols SIMPLE baselines (a
single feature + threshold, EWMA/CUSUM, isolation forest, kNN on pretrained features) match or beat complex
deep models. → Our build MUST run simple baselines FIRST and treat strict scores as the only primary number.

## 1. Video anomaly detection (VAD) — WS8 family (a)
- SOTA families: (i) one-class / reconstruction (autoencoders, memory-augmented AE), (ii) frame-prediction
  (future-frame prediction error), (iii) weakly-supervised (video-level labels, MIL ranking — UCF-Crime,
  XD-Violence), (iv) self-supervised / transformation / jigsaw, (v) pretrained-feature + kNN / density,
  (vi) VLM / open-vocabulary anomaly scoring (recent).
- Canonical benchmarks: UCSD Ped1/Ped2, CUHK Avenue, ShanghaiTech, Street Scene; weakly-sup: UCF-Crime,
  XD-Violence. Metric: frame-level AUC (micro/macro) — itself criticized.
- Criticisms (SOTA scan must carry): frame-AUC saturates and hides temporal/early-detection quality; many
  benchmarks have trivial anomalies (running, cycling) and label noise; cross-dataset generalization is
  poor; Street Scene authors argued existing metrics are misleading → region/track-based metrics.
- Realistic bar for us: VAD is for the SUPERVISED fire/smoke detector's BLIND SPOTS (unknown hazards,
  camera tamper/failure, unusual scene events) — NOT a primary fire detector. Expect high false-alarm rates;
  use as a SUPPORT/abstain-escalate signal with temporal confirmation, not an autonomous trigger.

## 2. Multivariate time-series / sensor anomaly — WS8 family (b)
- SOTA families: statistical (z-score, EWMA, CUSUM, ARIMA residuals), isolation-based (iForest), density/
  distance (LOF, kNN), matrix-profile, deep reconstruction/prediction (LSTM-AE, USAD, OmniAnomaly, Anomaly
  Transformer, TranAD), graph-based (GDN, MTAD-GAT), foundation-model-for-TS (recent).
- Benchmarks: SMD, SMAP/MSL (NASA), SWaT/WADI (water-treatment CPS), PSM, NAB, and the UCR Anomaly Archive
  (built explicitly to replace flawed benchmarks). Metric: the "point-adjust" F1 is the notorious inflator.
- Criticisms (central): Kim et al. and others show point-adjust lets even RANDOM scores beat SOTA; SMAP/MSL/
  SMD have mislabels and trivial anomalies; UCR archive + range-based / affiliation / event-based + delay-
  aware metrics are the recommended fixes. Many deep models do NOT beat simple baselines under honest eval.
- Realistic bar for us: THIS is the highest-value family — our IoT node's sensor streams (gas/smoke/temp/
  humidity) need sensor-fault-vs-real-event discrimination and drift detection. A lightweight statistical/
  iForest detector with EVT/conformal thresholding is likely the right build; deep models must EARN their
  keep against it.

## 3. OOD / model-health / drift — WS8 family (c)
- SOTA: max-softmax baseline, ODIN, energy-based, Mahalanobis on features, ViM, KNN-OOD; open-set
  recognition; concept-drift detectors (ADWIN, DDM/EDDM, page-hinkley); test-time adaptation.
- Criticisms: OOD benchmarks often conflate near-OOD vs far-OOD; many methods tuned on the OOD set; results
  sensitive to backbone. Drift detection needs labels or proxies that are scarce in deployment.
- Realistic bar: monitor the vision/fusion models' inputs for OOD (new camera/site/weather) → abstain /
  lower-confidence / "needs review" rather than silent wrong predictions. Cheap: Mahalanobis/kNN on the
  detector's penultimate features.

## 4. Physics-residual anomaly — WS8 family (d)  [ties to P7/P7G]
- Idea: the admitted physics models (fire EF-xx, geo GH-xx) produce residuals; large residuals = anomaly/
  OOD-of-physics. CPS anomaly-detection literature (SWaT/WADI) uses model-based residuals + CUSUM.
- Realistic bar: residual-based scores as an INPUT to fusion (P14) and a consistency check, with fallback-
  to-parent — consistent with the physics-as-feature/consistency stance (never hard constraints).

## 5. Network / alert anomaly — WS8 family (e)  [ties to P12 alerting]
- SOTA: intrusion-detection (CICIDS-type), replay/spoofing detection in CPS, node-misbehavior. For our mesh
  (ESP-NOW/BLE), the practical layer is signed messages + replay counters (from P6) + simple rate/behavior
  anomaly, NOT a heavy IDS.
- Realistic bar: lightweight behavioral anomaly + the P6 HMAC/replay-protection; feeds P12 threat model.

## 6. Social-media surge / coordinated amplification — WS8 family (f)
- SOTA: burst detection, coordinated-behavior detection. STRONG privacy/ethics constraint (MASTER_PROMPT
  §ethics, Rule: no profiling individuals/accounts). Realistic bar: LOW priority, aggregate-only burst
  signals, no individual profiling; likely documentation-only for this project.

## 7. Edge / TinyML anomaly — WS8 family (edge)
- SOTA: tiny autoencoders, statistical detectors, iForest variants on MCUs; reported KB-scale memory and
  ms-scale latency. ESP32-class feasible for statistical + tiny-AE on sensor streams; NOT for video.
- Realistic bar: on-node = statistical/rate-of-rise + tiny sensor-stream detector; video anomaly runs on
  the gateway, not the node.

## 8. "What the literature says about simple baselines" (to expand from quota)
Multiple critique papers (time-series point-adjust; VAD metric critiques; OOD backbone-sensitivity) converge
on: under strict, leakage-free protocols, simple baselines are frequently competitive. MANDATE: simple
baselines first; deep models only if they beat them on strict event-level/delay-aware metrics with CIs.

## 9. Realistic build bar (summary)
- PRIORITIZE: (b) sensor time-series + (c) OOD/model-health + (d) physics-residual — all cheap, high-value,
  edge/gateway-feasible, directly serve fire/geo early-warning.
- SUPPORT role: (a) video anomaly on gateway for detector blind spots (tamper/unknown hazard), abstain/
  escalate only.
- LIGHTWEIGHT: (e) network/alert anomaly via signing+replay+rate rules.
- DOCUMENTATION-ONLY / deferred: (f) social media (privacy-first, aggregate burst only).
- Primary metrics (all families): event-level detection + detection DELAY + false-alarms per camera-/sensor-
  day at a FIXED false-alarm budget, strict scoring, ≥5 seeds with CIs. NO point-adjust as a primary number.
