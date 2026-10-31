# ws8_anomaly/failure_analysis.md — anomaly layer failure analysis on paper (P10, WS8b)

RESEARCH-ONLY failure-mode analysis (MASTER_PROMPT P10 task 5): what the anomaly layer is expected to MISS or
FALSELY FLAG, which anomalies are INDISTINGUISHABLE from benign change, and privacy/misuse risks, with
citations. No own-system claim (Rule 16). Rule 19 advisory. Feeds the P16 robustness audit.

## A. Expected MISSES (false negatives)
- FM-A1 Slow/stealthy onset absorbed into the normal reference (a slowly-developing smolder/creep learned as
  "new normal"). Mitigation: bounded refresh rate + change-point guard (design §7); physics-residual
  corroboration. Residual risk HIGH for very slow events.
- FM-A2 Novel hazard with a signature inside the normal manifold (anomaly not separable in the chosen
  features). Mitigation: multi-modal corroboration (sensor+video+physics); feature review.
- FM-A3 Stealthy spoofing crafted to stay below threshold (optimal stealthy-attack policy exists vs a
  chi-square detector, 2606.06347). Mitigation: physics-invariant gate (2609.34804) + crypto (P6).
- FM-A4 On complex video, cheap pretrained-feature scoring misses subtle anomalies that only heavier models
  catch — accepted because video anomaly is SUPPORT-only; the supervised P8 detector leads.
- FM-A5 Edge statistical stack misses multivariate-only anomalies (no single channel crosses threshold).
  Mitigation: gateway multivariate detector; cross-channel features.

## B. Expected FALSE FLAGS (false positives)
- FM-B1 Benign novelty (new equipment, cleaning, cooking, weather, new truck) → the layer flags many benign
  novelties by design. Mitigation: default ABSTAIN/ESCALATE not ALARM (Rule 19); persistence; alert-fatigue
  budget (integration_spec §6).
- FM-B2 Background/scene shortcut: video detector flags the scene, not the event (2608.12045). Mitigation:
  patch-level/background-bias audit; camera-grouped splits.
- FM-B3 Benign operational regime shift inflates network-IDS FPR (2609.29745). Mitigation: control-plane/
  regime-aware thresholds set on benign shifts.
- FM-B4 Sensor drift/aging mistaken for an event. Mitigation: drift detector + sensor-fault flag separate
  from event flag; cross-sensor + physics corroboration.
- FM-B5 Physics-model misspecification (out-of-validity-range) → residual false alarms. Mitigation: validity-
  range gating + fallback-to-parent.
- FM-B6 OOD over-abstention → alert fatigue / missed real events during abstain. Mitigation: abstain-rate
  budget; near/far-OOD separation.

## C. Anomalies INDISTINGUISHABLE from benign change (honest)
- Slow seasonal/diurnal drift vs slow real degradation (both gradual) — fundamentally ambiguous without a
  ground-truth label or a physics anchor.
- A single-channel gas rise from cooking vs an early fire at the same magnitude/rate — needs multi-modal
  context (video, multiple sensors, location priors); the anomaly layer alone cannot separate them reliably.
- A valid-key compromised node's legitimate-looking messages — crypto passes; only behavioral + physics
  corroboration helps, imperfectly.
- In ungauged Himalayan catchments, a real precursor vs normal monsoon variability — the P7G data gap makes
  this advisory-only with wide uncertainty (Rule 19).

## D. Evaluation-driven failure (measuring the wrong thing)
- Believing an inflated point-adjust / Micro-AUROC number and shipping a detector that does not actually
  localize/time events (2607.11969, 2608.21854). Mitigation: the pre-registered strict protocol.
- Train-test leakage making a detector look better than it is (OddBench overlap in 355/690, 2609.29580).
  Mitigation: group/time splits + dataset-overlap audit (family-C data-quality / P16).

## E. Privacy and misuse risks (§ethics)
- Video anomaly on people → surveillance/profiling risk. Mitigation: operate on scene DYNAMICS not identity;
  no face/biometric features; data minimization (hand to P8/P13 privacy design). NO individual tracking.
- Social-media surge family → profiling individuals/accounts risk → DEFERRED, aggregate-burst only, no
  per-account analysis.
- Health/anomaly flags about specific households could be sensitive → access control + aggregation on the
  dashboard (P13).
- Misuse: an attacker suppressing alerts via spoof/flood → crypto + physics gate + logged suppression.

## F. Carried to P16
All FM-* above enter the P16 robustness failure-mode catalogue with prioritized fix/test plans; the
indistinguishable-cases (C) are flagged as RESIDUAL risks requiring human-in-the-loop + wide uncertainty, not
engineering fixes.
