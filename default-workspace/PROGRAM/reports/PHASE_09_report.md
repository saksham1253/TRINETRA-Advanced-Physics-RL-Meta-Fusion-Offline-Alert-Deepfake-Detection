# PHASE_09_report — WS8a ANOMALY DETECTION (RESEARCH-ONLY)

Phase P9 (MASTER_PROMPT anomaly-detection phase; WS8). Status: COMPLETE to gate (continuous mode —
completion record, not a halt). Research + design + protocol + literature only; nothing built or measured.
No own-system performance claim (Rule 16). Rule 19: anomaly outputs ADVISORY (abstain/escalate/health-
warning/tier-change), never autonomous evacuation. Privacy (§ethics): no profiling of individuals/accounts.

## Objective
Decide where anomaly detection belongs in TRINETRA, which families are in scope and at what priority, how it
is evaluated honestly, how it is architected (edge→gateway→server), and ground every choice in SOTA
literature — as the SAFETY NET for what the supervised detectors (P8 CCTV; P7/P7G physics) and sensors do not
cover (unknown hazards, sensor faults/drift, OOD inputs, tampering, spoofed alerts).

## What was produced
- PROGRAM/sota/P9_sota_scan.md — SOTA per family + the documented evaluation-integrity crisis + realistic
  build bar.
- ws8_anomaly/scope_decision.md — family-by-family in/out + priority + trigger + miss-vs-false-alarm cost +
  budget worth; lead-vs-support rule.
- ws8_anomaly/evaluation_protocol.md — PRE-REGISTERED: strict event-level + delay-aware metrics (PATE,
  VUS-PR), point-adjust BANNED as primary, leakage-free time/site/device-grouped splits, EVT/conformal
  thresholding, mandatory simple baselines as the complexity gate, stress tests, per-family acceptance
  targets (process targets, not results).
- ws8_anomaly/design.md — topology (ESP32 statistical+tiny-AE → gateway video-anomaly/OOD/physics-residual/
  network → server data-quality), per-family detectors, score normalization/calibration, false-alarm-
  controlled thresholding, interfaces to fusion (P14)/alerting (P12)/dashboard (P13), alert-fatigue
  controls, drift/normal-refresh policy, the layer's own failure modes.
- ws8_anomaly/build_plan.md — priority order + Kaggle GPU-hour estimates (~6-8 of ~30, shared) + data/edge
  plan.
- ws8_anomaly/literature_brief.md — P9 section appended (prior P4 brief left intact).
- ws8_anomaly/literature_map.md — 35 NEW primary arXiv papers (ABS) across 6 families + synthesis.

## Scope decision (priorities)
- PRIORITY 1: (b) sensor time-series (sensor-fault/drift vs real-event) + (c) OOD/model-health (abstain on
  new camera/site/weather). Cheap, high-value, edge/gateway-feasible, directly serve fire/geo EWS.
- PRIORITY 2: (d) physics-residual (reuse P7/P7G, feeds fusion + anti-spoof integrity gate); (a) video
  anomaly (SUPPORT-only, escalate/abstain, never autonomous alarm); (e) network/alert anomaly (signing+
  replay from P6 + rate rules, feeds P12).
- PRIORITY 3: (g) data-quality anomaly over our own datasets (build hygiene → P16).
- DEFERRED / doc-only: (f) social-media surge (aggregate burst only, privacy-first).

## Key literature findings (source-reported; Rule 16)
- EVALUATION INTEGRITY is the governing lesson: point-adjust awards near-perfect F1 to random scores
  (2607.11969, 2311.11235, 2409.13053, 2511.18739); best-of-N inflates affiliation + ALL ROC metrics incl.
  VUS-ROC → prefer VUS-PR, disclose N (2607.11969); Micro-AUROC ≠ temporal localization, report Within-AUROC
  (2608.21854); train-test overlap in 355/690 OddBench datasets (2609.29580). PATE is the delay-aware metric
  fitting an early-warning objective (2405.12096).
- SIMPLE BASELINES FIRST: PCA ≥ OmniAnomaly on SMD without point-adjust (2603.18985); static TSAD beats
  streaming/adaptive in most settings (2609.39215); on-device z-score hit P=R=1.00 at ~3.3 KB SRAM
  (2604.08581). Deep models must EARN their place on strict metrics with CIs.
- PHYSICS-RESIDUAL: CPS invariants both detect and gate against replay-poisoning (2609.34804); a TS
  foundation model can be a model-free residual generator (2606.06347).
- EDGE: tiny-AE on ESP32-S3 (recall 84%, ~180 KB, 9 ms — 2606.02256), NAS sizing (2010.11267), dual
  supervised+unsupervised edge IDS budgets (2610.07489); video anomaly stays on the gateway.

## Honesty & limits (§0.5)
- All 35 primaries are ABS (0 FT). web_search unavailable (no API key); arXiv throttled worked (no 429s this
  run). IDs/numbers subagent-reported, NOT each independently re-fetched (residual risk, disclosed).
- Datasets D55-D67 are [D]; most licenses "not visible in abstract" → INDICATIVE; the public benchmarks carry
  documented flaws (point-adjust, trivial anomalies, leakage) → method-development ONLY. REAL operating-point
  numbers (false-alarms/sensor-day, detection delay) require our OWN normal-only CCTV + IoT data collected in
  the build. No detector built or measured; acceptance criteria are process targets.
- Full-text metric extraction (exact VUS-PR/PATE/SWaT tables) is an OPEN action if deep numbers are needed.

## Open actions carried
Full-text read of the top eval papers (2607.11969, 2603.18985, 2608.21854, 2405.12096) for exact numbers;
confirm dataset licenses (iTrust SWaT/WADI request, NAB AGPL, UrbanSound8K CC BY-NC); design the own-data
normal-reference collection; privacy-preserving video-anomaly feature spec; pick the specific deep TS model
(if any) to pit against baselines — all to P10.

## Gate
PROGRAM/gate_messages/PHASE_09_gate.md. Auto-proceeding to P10 (anomaly-detection implementation specs).
