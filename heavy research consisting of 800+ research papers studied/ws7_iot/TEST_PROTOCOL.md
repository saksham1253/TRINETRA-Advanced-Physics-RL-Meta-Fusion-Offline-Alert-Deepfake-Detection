# ws7_iot/TEST_PROTOCOL.md — test protocol for the later build (P13, WS7b)

Phase P13 · DOCUMENTS ONLY. MASTER_PROMPT P13 task 5. ALL protocol, NONE executed (Rule 16). Governed by
ws7_iot/SAFETY.md (only safe stimuli; no real structural fire). Statistics suit SMALL samples [quota: field-
test methodology & small-sample statistics]. Every results slot = "to be filled after the build". This node
is ADVISORY (Rule 19) — tests characterize it, they do not certify a life-safety device.

## 1. Data-logging format (shared with FIRMWARE_SPEC §6)
Per-trial: timestamp, raw + engineering values per sensor, per-sensor validity/health, fused hazard,
uncertainty, state transitions, alert tier, battery/radio status; session + stimulus + ambient T/RH + unit
serial as metadata. Session-based splits (train/tune/test by SESSION, never by shuffled samples) to avoid
leakage [quota].

## 2. Sensor characterization
Warm-up curve; noise floor (quiet baseline); response & recovery times per sensor; humidity/temperature
dependence (vary ambient); repeatability (repeated identical trials); drift (long idle logging). Report
distributions + CIs, not single points.

## 3. Detection tests with SAFE stimuli (SAFETY.md)
Stimuli: steam, cooking-like vapor, dust puff, incense smoke at a safe distance, warm objects — NO real
dangerous fire. Nuisance/negative set: sunlight on flame sensor, cooking without fire, humidity swings.
REPEATED trials per condition; randomize order; session-based splits. Record per-condition detection + time-
to-annunciation.

## 4. Comparison design (the core experiment)
Head-to-head on the SAME logged trials: (a) single-sensor fixed threshold; (b) rate-of-rise; (c) multi-sensor
fusion; (d) TinyML classifier; (e) physics-informed logic; (f) the P10 anomaly layer. Primary endpoint =
false-alarm suppression on nuisance set at matched detection sensitivity (the dominant failure mode, design.md
§1). Report confusion counts + CIs; use small-sample methods [quota] (exact/bootstrap CIs, paired tests
across sessions, not asymptotic approximations).

## 5. Networking tests
Latency (stimulus → local annunciation; node → peer/dashboard); packet loss; REACH vs DISTANCE for ESP-NOW
and LoRa (measure real ranges — closes the WS3 GAPS Zigbee/ESP-NOW/802.11s and the P12 "other-hardware"
figures); node-removal / partition behavior (fail-safe "offline", not "all clear"); SPOOFED + REPLAYED
message rejection (FIRMWARE §8). Follow a low-power-radio measurement methodology [quota] (fixed Tx power,
logged RSSI/SNR, LoS vs obstructed, repeated runs).

## 6. Camera-path test (Type B, if budget allows)
Tiny flame/smoke classifier on ESP32-CAM: latency, RAM/flash fit, false-alarm reduction vs sensor-only, on
safe stimuli; smoke-vs-steam confusion characterized.

## 7. On-device figure measurement (closes carried gaps)
Measure the per-device latency/RAM/flash/current the P9/P10 edge specs flagged as "other-hardware" and the
WS3 radio ranges — these become the first REAL (own) numbers, reported with conditions, in the build phase.

## 8. Statistics (small-sample) [quota]
Pre-register endpoints; report effect sizes + CIs (bootstrap/exact), not just p-values; account for repeated
measures per unit; state n per condition; no cherry-picking. Negative/NULL results reported plainly (§0.5).

## 9. Honesty
No test executed; no number measured. All results sections are "to be filled after the build". Tests
CHARACTERIZE an advisory prototype; they do not certify it against any fire-safety standard.
