# ws8_anomaly/spec/family_b_sensor_timeseries.md — BUILD SPEC: multivariate sensor time-series anomaly (P10, WS8b)

PRIORITY 1. RESEARCH-ONLY build spec (nothing implemented/measured). All external numbers SOURCE-REPORTED
(Rule 16). Metrics follow ws8_anomaly/evaluation_protocol.md (point-adjust BANNED as primary). Where a precise
numeric default needs a primary citation it is sourced from the DEFAULT-RECIPE REGISTRY in
ws8_anomaly/spec/sota_targets.md §3 (P10 reader delivered 23 papers; placeholders now RESOLVED there).

## 1. Method and why (evidence)
Core job: distinguish SENSOR-FAULT / DRIFT from a REAL hazard event on the IoT node's streams (MQ-2/MQ-135
gas, temperature, humidity, optionally CO, PM, flame-IR, acoustic). Decision from evidence:
- SIMPLE BASELINES ARE FIRST-CLASS, not strawmen: PCA ≥ OmniAnomaly on SMD once point-adjust is removed
  (2603.18985); static detectors beat streaming/adaptive in most settings (2609.39215); on-device z-score
  reached P=R=1.00 on a real appliance task at ~3.3 KB SRAM (2604.08581). → the DEFAULT detector is a bank
  of statistical + classical detectors; a deep model is admitted ONLY if it beats them on strict event-level
  / delay-aware metrics with non-overlapping CIs.
- If a deep model is justified, candidates are reconstruction/forecasting (LSTM-AE / USAD / TranAD) and
  attention (Anomaly-Transformer) — but reproduction studies warn their reported gains are often
  point-adjust artifacts, so they are CANDIDATES to be tested, not defaults. Uncertainty-aware scoring
  (probabilistic state-space + graph, 2609.34161) reduces benign-fluctuation false alarms.

## 2. Inputs and outputs
- INPUT: per-sensor time series at the node's sample rate (design: 1 Hz raw, aggregated to 0.1-1 Hz
  windows), multivariate vector x_t ∈ R^d (d = number of channels), plus sensor-health metadata.
- OUTPUT: per-window anomaly score s_t ∈ [0,1] (calibrated), a binary flag at the operating point, a
  sensor-fault/stuck/drift flag per channel, and an uncertainty. Emitted to fusion (P14) and alert policy
  (P12) per integration_spec.md.

## 3. Data needed and splits
- Public (method dev ONLY, documented flaws): SMD (D58), SWaT/WADI (D63), NASA SMAP/MSL (D59), TSB-AD/
  TSB-drift (D62), UCR archive (D61). All [D].
- OWN DATA (for real operating-point numbers): node logs under NORMAL operation across diurnal/seasonal
  cycles + a labelled set of real/controlled events (test smoke, heat source) — collected in the build.
- SPLITS (evaluation_protocol §3): TIME-ORDERED (train earlier, test later); DEVICE/SESSION-GROUPED (no node
  or session in both train & test); fit scalers on train only (no normal-period leakage). Three tiers:
  in-distribution → cross-session/time → cross-device/site.

## 4. Normal-reference data policy
Maintain a rolling per-channel NORMAL reference capturing daily + seasonal cycles; fit on confirmed-normal
periods only; refresh on a bounded cadence with a change-point guard so a slow real anomaly is NOT absorbed
as new normal (design §7). Minimum normal history before a node arms: set in build (design default ≥ 2 weeks
spanning a weekday/weekend + day/night cycle); log every refresh.

## 5. Features
Per channel + cross-channel over sliding windows (default window W = 60 s, stride 10 s — [recipe-cite]):
level, slope/rate-of-rise, short/long EWMA, variance, min/max, inter-channel ratios (gas/temp), spectral/
MFCC for the acoustic channel, and physics-residual features from P7 fire models (EF/B) as extra channels.
Rate-of-rise of temperature + gas is a domain-critical fire feature.

## 6. Model architecture + hyperparameter defaults (with sources)
- BASELINE BANK (always built): per-channel z-score (robust: median/MAD), EWMA (λ default 0.1-0.3), CUSUM
  (k = 0.5σ, h = 4-5σ — classic SPC defaults [recipe-cite]), Isolation Forest (n_estimators 100,
  max_samples 256 — standard), LOF (k = 20), matrix-profile discord (window = event timescale), PCA
  reconstruction (retain 95% variance). Scores combined by rank-normalization (design §3).
- OPTIONAL DEEP (only if it beats the bank): compact AE/forecaster sized for edge (PaAno+ 2606.20055 is the
  compact TSB-AD-evaluated template; FirstDiff 2608.15727 one-step diffusion for latency). MANDATORY recipe
  rules from reproduction studies: use OVERLAPPING inference windows (avg +28% rel., can reorder rankings —
  2606.09874); do NOT train reconstruction/residual detectors to convergence — early-stop or add Kernel-
  Anchored Regularizer KAR (2610.02345); optionally add an EMA-target masked query-prediction score for
  dependency-shift anomalies (2603.12916) and channel-relevance-weighted contrastive aug (2605.23139); do
  NOT use a naive zero-shot forecasting FM for persistent anomalies (2607.12454). Hyperparameter defaults
  per sota_targets.md §3, frozen before test.

## 7. Training and thresholding recipe
- Train baselines/deep on confirmed-NORMAL windows only (one-class). 
- THRESHOLD: Peaks-Over-Threshold / EVT with dual-threshold hysteresis + trimmed-tail fit on streaming
  scores (2601.21293) OR split-conformal → p-values → Benjamini-Hochberg FDR control (2605.13642,
  `nonconform` reference impl; factorwise variant 2609.29580) to hit a TARGET false-alarm rate, fit on
  VALIDATION (never test); default target = the P12 alert-fatigue budget. For the shared multi-node model,
  per-feature thresholds from validation residual quantiles (2605.00482); apply a look-elsewhere/multiple-
  testing correction when scanning many sensors (2606.13780). Add temporal persistence/dwell-time (≥ N
  consecutive windows) before escalation (design §4). See sota_targets.md §3 for the full cited registry.

## 8. Score calibration
Per-detector PIT / rank-normalization on validation → common [0,1] scale; then EVT/conformal map to a
false-alarm rate; report a reliability diagram / ECE for the probabilistic path (evaluation_protocol §1).

## 9. Metrics + exact evaluation procedure
Primary (strict): event-level detection + detection DELAY (median / 90th pct), false-alarms per sensor-day at
the fixed budget, VUS-PR, PATE (delay-aware), ≥5 seeds + CIs. Point-adjust may appear ONLY labelled and
beside the strict score. Procedure = evaluation_protocol.md §1-§4.

## 10. Simple baselines to implement FIRST (gate)
z-score, EWMA, CUSUM, Isolation Forest, LOF, matrix-profile, PCA (above). A deep model is admitted ONLY if it
beats the best of these on strict event-level/delay-aware metrics with non-overlapping CIs (2603.18985,
2609.39215).

## 11. Ablations
Feature source (raw vs +physics-residual vs +acoustic); window/stride; detector family; with/without
calibration; static vs periodic-retrain vs online (expect static competitive, 2609.39215); parent-baseline
vs deep.

## 12. Stress tests
Sensor aging/drift; stuck/flat-line; dropout/missing; cross-sensor nuisance (cooking fumes, humidity swings,
dust); gradual drift vs step event; cross-device transfer. Report degradation curves.

## 13. Acceptance criteria (process targets, not results — Rule 16)
Detects controlled real events within the target delay at ≤ budget false-alarms/sensor-day AND beats the best
simple baseline on strict metrics with CIs; sensor-fault flag separable from real-event flag; runs within the
edge envelope (edge_spec.md).

## 14. Known pitfalls (failure_analysis.md + lit)
Point-adjust inflation (2607.11969); benchmark anomalies "even random functions detect" (2311.11235); slow
real anomaly absorbed into normal reference; drift masquerading as event (needs cross-sensor + physics
corroboration); label noise (2606.02256).

## 15. GPU hours / Kaggle fit
Baselines CPU-only. Optional deep model ≈ 2-3 Kaggle GPU-h incl. 5 seeds + ablations (build_plan.md). All
ESTIMATES.

## 16. Verification checklist
[ ] baselines implemented + beaten before any deep model shipped  [ ] thresholds fit on validation only
[ ] group/time splits enforced, scalers train-only  [ ] strict metrics primary, point-adjust not primary
[ ] ≥5 seeds + CIs  [ ] sensor-fault vs event separation shown  [ ] edge envelope met  [ ] every default
cited  [ ] normal-reference refresh logged + change-point guard tested.
