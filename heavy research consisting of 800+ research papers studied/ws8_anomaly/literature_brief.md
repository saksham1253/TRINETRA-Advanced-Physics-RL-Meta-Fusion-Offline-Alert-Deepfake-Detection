# WS8 — ANOMALY DETECTION — literature brief (P4, 2026-10-07)
Owner phases: P9/P10. Scope: SSL encoders, anomaly scoring, InSAR/SAR change, OOD, GLOF/landslide precursors.

## Most relevant papers
- **2610.03649** On-board SSL anomaly detection (marine EO, OBPDC/Phi-sat-2). SSL encoder → latent → ML
  anomaly detector benchmarked vs Isolation Forest, One-Class SVM, Local Outlier Factor; lightweight/edge.
  → corroborates our exact stack (SSL masked encoder → latent → Deep-SVDD/iForest ensemble) + edge-feasibility.
- **2509.18176** CNN-LSTM InSAR deformation forecasting vs LightGBM/LASSO — baselines DEFAULT TO PERSISTENCE;
  tensorize sparse PS-InSAR points, forecast single-step, SHAP-explain. → WS8 InSAR-forecast blueprint.
- **2512.24117** Himalayan GLOF S1 segmentation pipeline (IoU 0.9130; ASF-API ingest; Docker/REST) — WS8
  reference architecture; §6 caveat = GRD ~900 m² floor misses sub-resolution precursors (FM-27).
- **2502.15901** TS-OOD (most vision OOD methods FAIL on time series) + **2605.31155** hyperspherical TF OOD.
- **2609.34836** MW-Nowcast residual ensemble (residual doctrine for the forecasting-residual anomaly path).

## Key claims → references
- SSL masked encoder → classical-anomaly ensemble (Deep-SVDD + iForest + OCSVM/LOF), edge-sized. → DC-15.
- Learn a bounded residual on a temporal backbone; mandatory persistence baseline. → DC-06 (2509.18176).
- OOD on time series needs TS-specific methods; you cannot lift a vision OOD detector. → FM-07 (2502.15901).
- GLOF area-change can be below the SAR resolution floor → emit 'below-detection-floor' flag, add lake-level/
  temperature/seismic precursors + physics gate. → FM-27 (2512.24117 §6).
- Anomaly stack must not degrade when a modality drops (worst-case). → DC-05/DC-09.

## Open questions
- Himalayan InSAR slope-creep transfer from urban-subsidence InSAR (2509.18176 domain gap).
- Multi-step (lead-time) forecasting vs the single-step baselines.
- Fusing S1 BURST (10–20 m) + S2/NISAR/Landsat for 1–2 day revisit to beat the GRD floor (FM-27).

---

# WS8 — P9 brief (2026-10-10, continuous-execution mode) — appended, prior P4 brief above left intact

The P4 brief above is carried forward (SSL encoder → classical-anomaly ensemble; InSAR/GLOF/TS-OOD leads).
This P9 section distills the full-phase decision knowledge. Specific IDs + source-reported numbers are in
ws8_anomaly/literature_map.md. No own-system performance claim (Rule 16).

## The governing lesson: evaluation integrity
A large fraction of published anomaly SOTA is an artifact of lenient evaluation:
- Time-series: the "point-adjust" protocol is so lenient that RANDOM scores can beat SOTA; use range-based/
  affiliation/event-based + delay-aware metrics and the UCR Anomaly Archive (built to replace flawed SMAP/
  MSL/SMD/Yahoo).
- Video: frame-level AUC saturates, hides early detection, rewards trivial anomalies → region/track metrics.
- Thresholds tuned on test, leaky random splits, synthetic-injection-only evidence are pervasive.
→ evaluation_protocol.md bans point-adjust as primary; mandates strict event-level + delay-aware at a fixed
  false-alarm budget, leakage-free time/site/device-grouped splits, and simple-baselines-first as the gate.

## Family briefs (what we will build and why)
- SENSOR TIME-SERIES (priority 1): statistical (z-score/EWMA/CUSUM/ARIMA-resid) + isolation forest + matrix-
  profile are strong cheap edge baselines; deep (LSTM-AE, USAD, Anomaly-Transformer, TranAD, GDN/MTAD-GAT)
  must beat them under strict eval. Job: sensor-fault/drift vs real-event for the IoT node.
- OOD / MODEL-HEALTH (priority 1): Mahalanobis/kNN/energy/ViM on P8-vision & P14-fusion features; abstain/
  "needs review" on new camera/site/weather. NB TS-OOD ≠ vision-OOD (2502.15901) — use TS-specific OOD.
- PHYSICS-RESIDUAL (priority 2): residuals of admitted fire (EF/B) + geo (GH/GB) models as consistency/
  anomaly scores feeding fusion, fallback-to-parent (CPS literature: model-residual + CUSUM).
- VIDEO ANOMALY (priority 2, SUPPORT only): pretrained-feature kNN / reconstruction / future-frame; high FA
  → escalate/abstain only, never autonomous alarm; covers supervised blind spots (unknown hazard/tamper).
- NETWORK/ALERT (priority 2, lightweight): signed messages + replay counters (P6) + rate/behavior anomaly →
  P12 threat model.
- SOCIAL surge (deferred, doc-only): aggregate burst only; no profiling (§ethics).

## Thresholding/calibration we will use
EVT (Peaks-Over-Threshold) and/or CONFORMAL anomaly detection to hit a target false-alarm rate on
validation (never test); per-detector score normalization; temporal persistence/dwell-time against single-
spike false alarms.

## Edge reality
ESP32 node: statistical + rate-of-rise + tiny-AE/iForest on windowed features (KB memory, ms latency);
video anomaly on the gateway only.

## Open questions carried to P10
Which deep TS model (if any) earns its place over simple baselines; normal-reference refresh cadence;
conformal-vs-EVT per family; exact MCU memory/latency envelope; privacy-preserving video-anomaly features.
