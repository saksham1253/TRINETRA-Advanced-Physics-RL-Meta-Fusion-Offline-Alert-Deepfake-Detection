# ws8_anomaly/evaluation_protocol.md — PRE-REGISTERED anomaly evaluation protocol (P9, WS8a)

Phase P9 · RESEARCH-ONLY. Pre-registered BEFORE any build (§0.5 anti-HARKing). Fixes metrics, splits,
thresholding, anomaly-rate realism, synthetic-injection rules, strict-vs-lenient policy, seeds/CIs,
ablations, mandatory simple baselines, stress tests, and per-family acceptance criteria. These are PROCESS/
validation targets, NOT results (Rule 16). Primary numbers are STRICT scores only.

## 1. Metrics (primary = strict, event-level)
- EVENT-LEVEL detection with DETECTION DELAY: an event is detected if the score crosses threshold within a
  tolerance window of the true event; report median/90th-percentile delay.
- FALSE ALARMS per camera-day (video) / per sensor-day (time-series) at a FIXED false-alarm budget.
- Precision-Recall AUC and range-based / affiliation / event-based F1 (NOT point-adjust as a primary).
- Calibration of anomaly scores (reliability diagram / ECE where scores are probabilistic).
- Performance AT A FIXED false-alarm budget (operating point), reported as the headline, plus a full
  score-threshold curve.
- Report ≥5 seeds with confidence intervals for every learned method.

## 2. BANNED / demoted protocols (eval-integrity)
- POINT-ADJUST F1 is BANNED as a primary metric (literature shows random scores beat SOTA under it); may be
  reported ONLY to compare with published work, clearly LABELED, with the strict event-level score beside it.
- Thresholds tuned on TEST are banned — thresholds come from validation or a documented statistical rule.
- Random frame-level splits are banned (leakage).
- Synthetic injection as the ONLY evidence is banned.

## 3. Splits (leakage-free)
- TIME-ORDERED splits (train = earlier, test = later); never shuffle frames/timesteps across the boundary.
- SITE/CAMERA/SENSOR-GROUPED splits: no camera/site/sensor/session appears in both train and test (video
  anomaly groups by camera+site; time-series by device/session).
- NORMAL-PERIOD leakage ban: statistics of the test normal period must NOT inform training/normalization
  (fit scalers on train only).
- Three generalization tiers (as in P8): in-distribution → cross-session/time → cross-site/camera/device.

## 4. Threshold selection
- On a validation split OR by a documented statistical rule (EVT / POT tail fit, or conformal anomaly
  detection for a target false-alarm rate), fixed BEFORE seeing test. Report the rule and the resulting
  operating point.

## 5. Anomaly-rate realism & synthetic injection
- Evaluate at REALISTIC anomaly rates (rare); do not rebalance to 50/50.
- Synthetic anomalies: clearly labeled SYNTHETIC, varied in type AND magnitude, never the only evidence;
  record the literature's injection-bias warnings; real/held-out anomalies are the primary evidence.

## 6. Mandatory SIMPLE BASELINES (run FIRST — gate for complexity)
Time-series: z-score, EWMA, CUSUM, ARIMA-residual, isolation forest, kNN/LOF on windowed features, matrix
profile. Video: frame-difference / optical-flow energy, kNN on pretrained features, PCA/AE reconstruction.
OOD: max-softmax, Mahalanobis/kNN on penultimate features. A deep model is admitted to the build ONLY if it
beats the best simple baseline on the STRICT event-level/delay-aware metric with non-overlapping CIs.

## 7. Stress tests (per family)
New camera/site; lighting & weather change; sensor aging/drift; nuisance sources (steam, dust, cooking,
headlights, swaying vegetation); gradual drift; adversarial & tamper cases (occlusion, blinding, replay).
Report degradation curves, not a single number.

## 8. Per-family acceptance criteria (build-phase gates; targets not results)
| Family | Primary metric | Acceptance target (to be met in build, vs simple baseline) |
|--------|----------------|------------------------------------------------------------|
| (b) sensor TS | event detection delay + FA/sensor-day | detect real events within target delay at ≤ budget FA/sensor-day AND beat best simple baseline (strict, CIs) |
| (c) OOD/health | OOD AUROC + abstention quality | reliably abstains on cross-site/weather OOD without harming in-dist accuracy; beats max-softmax |
| (d) physics-residual | residual AUROC as fusion input | adds non-redundant signal over its parent model; improves fusion (P14) |
| (a) video anomaly | region/track-based + FA/camera-day | usable as SUPPORT (escalation) at a tolerable FA/camera-day under group splits; NOT an autonomous alarm |
| (e) network/alert | spoof/replay rejection rate + FA | rejects signed-message spoof/replay (from P6) + flags node misbehavior at low FA |

## 9. Seeds, ablations, reporting
≥5 seeds + CIs; ablations (feature source, with/without physics inputs, with/without calibration, parent vs
extension, fused vs best single); report strict scores as primary, any lenient score labeled and secondary.

## Honesty
Nothing here is measured. All target numbers are build-phase gates. The protocol's reason-for-being is the
documented anomaly-eval-integrity crisis (point-adjust inflation, test-tuned thresholds, trivial benchmarks,
leakage) catalogued in PROGRAM/sota/P9_sota_scan.md and ws8_anomaly/literature_map.md.
