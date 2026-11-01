# ws8_anomaly/spec/integration_spec.md — anomaly ↔ fusion/alerting/dashboard integration (P10, WS8b)

RESEARCH-ONLY. Interfaces + data formats delivering anomaly scores and health flags to meta-fusion (P14),
alert decision policy (P12) and dashboard (P13); end-to-end behavior as scenarios; alert-fatigue budget
logic. No own-system performance claim (Rule 16). Rule 19: advisory outputs only.

## 1. Common anomaly-event message (schema)
Each detector emits a record:
```
{ ts, source_id (node/camera/model), family (B|C|D|A|E), raw_score, calibrated_score ∈ [0,1],
  uncertainty, operating_point_flag (bool), kind (event|sensor_fault|drift|ood|tamper|spoof|health),
  persistence_count, context (channel/region/model refs), parent_ref (for residuals), explanation (opt) }
```
Transport: offline-first; node→gateway over the P6 mesh (signed); gateway buffers when disconnected.

## 2. → META-FUSION (P14)
Each calibrated_score enters fusion as an INPUT or an ABSTENTION trigger. Correlated detectors (a Layer-2
physics residual and its Layer-1 parent; family-D residual and family-B on the same channel) carry
parent_ref / correlation tags so fusion does NOT double-count. OOD (family C) can DOWN-WEIGHT or gate the
vision/fusion decision. Fusion owns the final calibrated hazard probability; anomaly scores are evidence,
not verdicts.

## 3. → ALERT POLICY (P12)
Anomaly outputs can (i) RAISE/LOWER the alert TIER, (ii) trigger ABSTAIN / human review, (iii) raise a
SENSOR-HEALTH or SPOOF warning (distinct from a hazard alarm). They NEVER autonomously issue an evacuation
alert (Rule 19). The alert-fatigue budget (below) governs escalation.

## 4. → DASHBOARD (P13)
Live anomaly + health/tamper/spoof flags, per-source event log, score timelines, current operating points,
and suppressed-detector status (with reason). Human-review queue for ABSTAIN/ESCALATE items.

## 5. End-to-end scenarios
- ABSTAIN: new camera at a new site → family-C OOD high → vision decision down-weighted, item queued for
  review, NO alarm.
- ESCALATE: video anomaly (family A) + sensor rate-of-rise (family B) co-fire with persistence → tier raised,
  human review requested; fire alarm only if P8/fusion confirms.
- HEALTH WARNING: family-B sensor-fault flag → "sensor needs service", not a hazard alarm.
- SPOOF: family-E replay detected (crypto + behavioral) → message rejected, spoof warning to P12, node-health
  flag.

## 6. Alert-fatigue budget logic
Per-site false-alarm budget (q alerts/day, set in P12); dwell-time/persistence before escalation;
de-duplication of concurrent flags for one event; tiered routing (health ≠ hazard); automatic SUPPRESSION of
a chronically-flagging detector pending human review, with the suppression itself LOGGED and surfaced on the
dashboard (so suppression can't silently hide a real hazard).

## 7. Degradation / offline behavior
If the gateway/learned part is down, the node runs the statistical stack and buffers events; fusion falls
back to parent models; alerts degrade to local sounder + stored log (P12/P13 own the offline alert path).

## 8. Verification checklist
[ ] schema fixed + versioned  [ ] correlated detectors tagged for P14  [ ] no autonomous evacuation path
(Rule 19)  [ ] alert-fatigue budget + logged suppression  [ ] offline buffering + graceful degradation
[ ] health/spoof flags distinct from hazard alarms.
