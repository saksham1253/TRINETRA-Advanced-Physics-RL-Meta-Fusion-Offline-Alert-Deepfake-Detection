# ws7_iot/INTEGRATION_NOTES.md — how IoT streams feed fusion & alerting (P13, WS7b)

Phase P13 · DOCUMENTS ONLY. MASTER_PROMPT P13 task 7. Data formats + interfaces only; nothing built (Rule 16).
Ties the node to P14 meta-fusion, P12 alerting, and the P11 deepfake/trust policy. Rule 19: IoT alarms are
CORROBORATING evidence under human oversight, not an autonomous public alert.

## 1. What the node emits (per FIRMWARE_SPEC §6 schema)
Signed message {node_id, seq, ts, state, hazard (calibrated level, NOT raw boolean), per-sensor engineering
values + validity/health flags, fused confidence + uncertainty, nonce, mac}. Both a periodic sample record
and event records (state transitions, faults).

## 2. → Meta-fusion (P14)
- The node's calibrated hazard + uncertainty + per-sensor health become INPUT CHANNELS to the P14 fusion
  layer, alongside CCTV detection (P8), physics priors (P7), and anomaly scores (P9/P10).
- Per P14 reading: convert the node score to a COMMON CALIBRATED SCALE (conformal p-value / proper-score-
  calibrated posterior) BEFORE weighted/evidential fusion — do NOT fuse raw scores (2105.07346 scoring-bias
  warning; 2609.38196 conformal reweighting).
- Missing/degraded node streams must be handled gracefully (Kalman late-fusion marginalization 2509.25452;
  missing-modality robustness 2309.15529) and the FUSED output recalibrated (2101.05397: calibrated members
  ≠ calibrated ensemble; 2605.12517: missing input breaks calibration).
- Sensor-health flags let fusion DOWN-WEIGHT a faulty node (BMA fault flagging 1301.4795), not drop it blind.

## 3. → Alert decision policy (P12)
- The node's hazard+uncertainty feed the WS3 confidence→tier decision policy (architecture.md §6): local Tier
  1 annunciation fires immediately on a confirmed LOCAL alarm (works even offline/radio-down); wider tiers
  require corroboration + human oversight (Rule 19).
- Signed + replay-protected messages satisfy the WS3 threat_model authentication requirement; cross-node
  corroboration mirrors the cell-broadcast cross-cell spoof check.

## 4. → Deepfake/trust policy (P11)
- An IoT alarm is a CORROBORATING physical signal for a social-media disaster report: in the P11 trust
  pipeline it raises corroboration for a claim co-located in time/place, but a social report NEVER
  auto-triggers a public alert (human-in-the-loop). The node provides ground-truth-ish physical evidence that
  helps distinguish a real event from out-of-context/synthetic media.

## 5. Data-format discipline
One versioned schema across node→fusion→alert→dashboard; engineering units + validity flags mandatory;
timestamps NTP-synced where available (2601.03867); all inter-component messages signed. Pin the exact
serialization (line-delimited JSON / CBOR) at build.

## 6. Honesty
Interfaces/formats only; no integration executed. The common-calibrated-scale-before-fusion rule and the
missing-input recalibration are design decisions imported from the P14 reading (source-reported), to be
validated in the build.
