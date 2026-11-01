# ws8_anomaly/scope_decision.md — where anomaly detection belongs (P9, WS8a)

Phase P9 · RESEARCH-ONLY. Decides, with evidence, which anomaly families are IN scope and at what priority,
what counts as an anomaly, what the detector triggers, cost-of-miss vs cost-of-false-alarm, budget worth,
and the relation to the supervised detectors. Rule 19: anomaly outputs are ADVISORY (abstain/escalate/
health-warning/tier-change); they NEVER autonomously trigger evacuation. Privacy: no profiling of
individuals or accounts (§ethics).

## Guiding principle
Anomaly detection here is the SAFETY NET for what the supervised detectors (P8 CCTV fire/smoke; P7/P7G
physics) and sensors DON'T cover: unknown hazards, novel failure modes, sensor faults/drift, out-of-
distribution inputs, and tampering. It LEADS only where no supervised model exists (e.g. sensor-fault vs
real-event, camera tamper); otherwise it SUPPORTS (raises/lowers tier, abstains, escalates to human review).

## Family-by-family decision
| Family | In scope? | Priority | What = anomaly (examples) | Trigger | Miss vs false-alarm cost | Budget worth |
|--------|-----------|----------|---------------------------|---------|--------------------------|--------------|
| (b) Sensor time-series | YES | **P1 (highest)** | gas/smoke/temp spike unlike any trained class; stuck/noisy/drifting sensor; impossible rate-of-change | health-warning / escalate / raise tier | miss of a real event = high; false alarm = medium (alert fatigue) | HIGH — cheap, edge-feasible, core EWS value |
| (c) OOD / model-health | YES | **P1** | new camera/site/weather makes vision/fusion inputs OOD; feature-space drift | abstain / "needs review" / lower confidence | silent wrong prediction = high | HIGH — cheap (Mahalanobis/kNN on features) |
| (d) Physics-residual | YES | **P2** | large residual of admitted fire/geo physics models | consistency flag → fusion input | depends; supports fusion | MEDIUM — reuses P7/P7G, no new data |
| (a) Video anomaly | YES (support) | **P2** | unusual scene event, unknown hazard, camera failure/tamper/occlusion | escalate / flag (NOT autonomous alarm) | false alarm = high (VAD noisy) → support only | MEDIUM — gateway only, high FA risk |
| (e) Network / alert anomaly | YES (lightweight) | **P2** | spoofed/replayed/DoS messages, node misbehavior | reject message / node-health flag | spoofed alert = high | MEDIUM — mostly signing+replay (P6) + rate rules |
| (g) Data-quality (our datasets) | YES | **P3** | label noise, duplicates, leakage in our own training data | pipeline warning (build-time) | affects all models | MEDIUM — build-hygiene, feeds P16 robustness |
| (f) Social-media surge | DEFERRED / doc-only | **P4** | abnormal surge / coordinated amplification about an event | aggregate corroboration signal ONLY | low direct safety value; high privacy risk | LOW — privacy-first, aggregate-only, likely documentation-only |

## Relation to supervised detectors (when lead / when support)
- LEAD: sensor-fault-vs-real-event (no supervised model), camera-tamper/failure, OOD-input gating. Here the
  anomaly layer is the primary signal (→ health warning / abstain / escalate).
- SUPPORT: fire/smoke detection — the supervised P8 detector leads; the anomaly layer only (i) covers its
  known blind spots (early/occluded/unknown) by escalating for human review, and (ii) feeds fusion.
- OPEN-SET expectation: expect the anomaly layer to flag MANY benign novelties (new truck, weather, cleaning)
  → it must default to ABSTAIN/ESCALATE, not ALARM, and be governed by an alert-fatigue budget (P12).

## Data that exists / could be collected
- (b): public multivariate/sensor-fault benchmarks (SMD, SWaT/WADI, NASA SMAP/MSL — all with documented
  flaws) + our OWN normal-operation IoT logs (to be collected in the build, normal-only reference policy in
  evaluation_protocol.md). (a): UCSD/Avenue/ShanghaiTech/UCF-Crime/XD-Violence (flawed; support-only) + our
  own normal CCTV footage. (c): OOD via held-out cameras/sites/weather. (d): physics residuals from P7/P7G.
  (e): CICIDS-type traces + our own mesh logs. (f): crisis-tweet/coordinated-behavior sets (privacy-gated).

## Budget verdict (Kaggle ≤~30 GPU-h shared; edge ESP32)
- Spend most anomaly budget on (b)+(c)+(d) — cheap, high-value, edge/gateway-feasible. (a) video anomaly:
  modest gateway budget, support-only. (e): near-zero GPU (rules + light model). (f): none (doc-only).
- On-node (ESP32): statistical + tiny sensor-stream detector only; video anomaly on the gateway.

## Honesty
No detector built or measured; this is a scope decision. All SOTA numbers that justify priorities are
SOURCE-REPORTED and carried in literature_map.md. The simple-baselines-first mandate (SOTA scan §8) applies
to every in-scope family.
