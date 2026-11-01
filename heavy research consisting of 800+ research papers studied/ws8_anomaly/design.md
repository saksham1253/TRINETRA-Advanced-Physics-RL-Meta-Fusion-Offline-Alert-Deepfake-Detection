# ws8_anomaly/design.md — anomaly-layer architecture (P9, WS8a)

Phase P9 · RESEARCH-ONLY. Architecture of the anomaly layer: per-family detectors, feature sources, score
normalization/calibration, false-alarm-controlled thresholding, how scores feed meta-fusion (P14) and the
alert decision policy (P12), alert-fatigue controls, drift/refresh policy, the edge-feasible subset, privacy
rules, and the layer's OWN failure modes. No code; design only. Rule 19 advisory; §ethics privacy.

## 1. Topology (where each detector runs)
- ON-NODE (ESP32-class): statistical sensor-stream detectors only (z-score / EWMA / CUSUM / rate-of-rise +
  a tiny autoencoder or iForest-lite on windowed features) + sensor-fault/stuck/drift checks. KB memory,
  ms latency (literature-based expectations in literature_map.md). Emits sensor-health flag + local anomaly
  score; works fully offline.
- GATEWAY (Pi/phone-class): video anomaly (pretrained-feature kNN / reconstruction) for detector blind
  spots + OOD/model-health monitors on vision/fusion features + physics-residual scoring (P7/P7G models) +
  network/alert anomaly. Aggregates node scores.
- OFFLINE/SERVER (build-time only): data-quality anomaly over our own datasets; drift analysis.

## 2. Per-family detectors (feature source → method → output)
- (b) Sensor TS: windowed sensor features → statistical + tiny-AE/iForest → anomaly score + health flag.
- (c) OOD/health: penultimate features of P8 vision / P14 fusion → Mahalanobis or kNN density → OOD score
  → abstain/"needs review" gate.
- (d) Physics-residual: residuals of admitted fire (EF/B) & geo (GH/GB) models → normalized residual score
  → consistency signal (fallback-to-parent, never a hard constraint).
- (a) Video: pretrained-feature kNN / reconstruction / prediction error → region/track score → ESCALATE
  (support only), with temporal persistence confirmation.
- (e) Network/alert: signed-message + replay-counter check (from P6) + simple rate/behavior anomaly → reject
  / node-health flag.
- (f) Social (deferred, doc-only): aggregate burst signal only; NO individual/account profiling.

## 3. Score normalization & calibration across detectors
Each detector outputs a raw score + an uncertainty. Normalize to a common scale via per-detector validation-
set calibration (e.g. probability-integral transform / rank normalization), then calibrate to a false-alarm
rate using EVT (POT tail fit) or CONFORMAL anomaly detection for a target FA budget. This lets heterogeneous
detectors be compared and fused without one dominating.

## 4. Thresholding with false-alarm control
Primary: set thresholds for a TARGET false-alarms-per-camera/sensor-day budget using EVT/conformal on
validation (never test). Expose the operating point + a hysteresis / dwell-time so a single noisy spike does
not alarm (temporal persistence).

## 5. Interfaces
- → META-FUSION (P14): each anomaly score enters as an INPUT or an ABSTENTION TRIGGER; correlated detectors
  (e.g. a Layer-2 physics residual and its Layer-1 parent) are flagged so fusion does not double-count.
- → ALERT POLICY (P12): anomaly scores can (i) raise/lower the alert TIER, (ii) trigger ABSTAIN / human
  review, (iii) raise a SENSOR-HEALTH warning — governed by the alert-fatigue budget.
- → DASHBOARD (P13): live anomaly + sensor-health flags, event log.

## 6. Alert-fatigue controls
Per-site false-alarm budget; dwell-time/persistence before escalation; de-duplication of concurrent anomaly
flags; tier-based routing (health warning ≠ hazard alarm); automatic suppression of a chronically-flagging
detector pending human review (with the suppression itself logged).

## 7. Drift monitoring & "normal" refresh policy
Maintain a rolling NORMAL reference (per camera/sensor), refreshed on a schedule that respects daily/seasonal
cycles; monitor feature-space drift (ADWIN/page-hinkley-style) and re-fit normalizers on a cadence; log every
refresh. Define how much normal data and how often (set in P10 spec).

## 8. Edge-feasible subset (ESP32)
Statistical detectors + rate-of-rise + tiny-AE/iForest on sensor windows; fixed-point; bounded buffers;
watchdog-safe. Memory/latency expectations from TinyML-anomaly papers (literature_map). Video anomaly is NOT
on the node.

## 9. Privacy rules (§ethics)
No profiling of individuals or social accounts; video anomaly operates on scene dynamics, not identity;
social-media family is aggregate-burst only and deferred. Face/person data minimization handed to P8/P13
privacy design.

## 10. The anomaly layer's OWN failure modes
- Will flag many benign novelties → default ABSTAIN/ESCALATE, never autonomous alarm (Rule 19).
- Normal-reference poisoning (a slow real anomaly treated as new normal) → cap refresh rate + change-point
  guard. Sensor drift mimics/masks events → cross-sensor + physics-residual corroboration. Adversarial
  evasion/tamper → the tamper detector + signed messages. Degrades to the simple statistical baseline if the
  learned part is unavailable.

## Honesty
Design only; nothing built or measured. Evidence for every choice (simple-baselines-first, EVT/conformal
thresholds, pretrained-feature OOD, TinyML feasibility) is SOURCE-REPORTED in literature_map.md.
