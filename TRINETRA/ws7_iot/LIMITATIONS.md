# ws7_iot/LIMITATIONS.md — honest "what the prototype will and will not prove" (P13, WS7b)

Phase P13 · DOCUMENTS ONLY. MASTER_PROMPT P13 task 6. §0.5 hard honesty / Rule 16 / Rule 19.

## What the prototype WILL (plausibly) prove — after the build, from our own logs
- That a ≤ ₹2000 multi-sensor ESP32 node can detect safe fire-like stimuli and annunciate locally, fully
  OFFLINE (no internet).
- That MULTI-SENSOR FUSION suppresses nuisance false alarms better than a single sensor, on our safe-stimuli
  test set (relative comparison, our data).
- That signed messages with replay protection REJECT a spoofed and a replayed message.
- That the node FAILS SAFE: a faulty sensor is down-weighted; a dead node reads "offline", never "all clear".
- Measured (own, first real numbers): local-alert latency, ESP-NOW/LoRa reach vs distance, and the per-device
  edge figures the P9/P10/P12 specs flagged as "other-hardware".

## What the prototype will NOT prove
- It is NOT a certified fire alarm and does NOT meet any fire-safety standard; it is ADVISORY, complementing
  certified alarms under human oversight (Rule 19).
- It will NOT be tested on real dangerous/structural fire (SAFETY.md forbids it) — so real-fire sensitivity/
  lead-time are NOT established; only safe-stimulus proxies.
- Small-sample tests give indicative, not population-level, performance; no claim generalizes beyond the
  tested conditions/units.
- Cheap sensors drift and are cross-sensitive; long-term reliability/field-robustness is NOT proven by a
  short demo.
- Vision (Type B) smoke-vs-steam confusion and low-light limits are NOT solved, only characterized.
- Radio ranges depend on terrain; demo-site numbers do NOT transfer to arbitrary deployments.
- Nothing in this research run is a measured result; all numbers come later from the build.

## Standing caveats carried
Datasheet/literature numbers are SOURCE-REPORTED; India radio-band legality (LoRa 865–867 MHz) flagged for
expert/legal review; the node must never be presented as a life-safety replacement.
