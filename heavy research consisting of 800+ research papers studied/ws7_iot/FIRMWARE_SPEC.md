# ws7_iot/FIRMWARE_SPEC.md — firmware SPECIFICATION (no code) for the fire-detection node (P13, WS7b)

Phase P13 · DOCUMENTS ONLY. MASTER_PROMPT P13 task 2. Nothing is built, flashed, or tested now (Rule 16).
Builds on ws7_iot/design.md (P6). Library/version choices are to be PINNED at build time. Literature-sourced
specifics (calibration curves, TinyML footprints, radio measurement method) fold in from the P13 reading
quota (ws7_iot/literature_map.md P13 section + PROGRAM/sota/P13_sota_scan.md); each marked [quota] below.
Rule 19: this node is an ADVISORY sensor complementing certified alarms under human oversight.

## 1. Target & toolchain (to pin at build)
- MCU: ESP32 DevKit (Type A sensor node) / ESP32-CAM OV2640 (Type B camera node), per design.md.
- Framework candidates to evaluate (pin ONE at build): ESP-IDF (FreeRTOS, best control of watchdog/
  brownout/power) vs Arduino-ESP32 (faster to build). RECOMMENDATION: ESP-IDF for the reliability features
  in §7; Arduino acceptable for an early breadboard.
- TinyML runtime (Type B / fused-feature classifier): TensorFlow Lite for Microcontrollers or ESP-DL —
  choose by measured flash/RAM fit at build [quota: TinyML/quantization on ESP32].

## 2. Module decomposition
1. SENSOR DRIVERS: MQ-2 (ADC), optional MQ-135 (ADC), IR flame (digital/ADC), DHT22 or BME280 (temp/
   humidity[/pressure]). Each driver exposes raw + engineering-unit + validity flag.
2. SIGNAL CONDITIONING: warm-up gating, moving-average/median de-noise, humidity/temperature compensation
   for the MQ sensors [quota: sensor calibration/compensation], per-unit gain/offset from NVS.
3. FEATURE/PHYSICS LAYER: fixed over-temperature threshold AND rate-of-rise dT/dt; smoke/gas rising-rate;
   flame-flicker confirmation (ties to P7 physics constants).
4. FUSION LAYER: multi-sensor corroboration with per-sensor confidence → calibrated hazard level (NOT a raw
   boolean), feeding hysteresis; emits fused confidence + uncertainty.
5. ANOMALY/SENSOR-HEALTH LAYER: stuck/flatline/out-of-range/drift detection → down-weight faulty sensors
   (P10 edge spec: on-device SSL vs iForest/OCSVM/LOF). Fault must degrade gracefully, never silently alarm
   or go blind.
6. ALERTING: local buzzer + strobe (immediate on confirmed local alarm); signed messages to peers/dashboard.
7. LOCAL DASHBOARD: served from the device (SoftAP), content in §5.
8. STORAGE/LOGGING: ring-buffer event + sample log to flash/SD (§6).
9. RADIO: ESP-NOW (peer-to-peer, no router) and/or LoRa; signed-message transport (§8 of design.md).
10. POWER/DUTY-CYCLE MANAGER: sleep scheduling, on-battery behavior, low-battery annunciation (design.md §6).
11. SUPERVISOR: watchdog, brownout, fault handling, safe-state (§7).

## 3. State machine (top-level)
`BOOT → SELFTEST → WARMUP (sensor burn-in gate) → MONITOR ⇄ PRE-ALARM ⇄ ALARM`, with orthogonal
`FAULT`/`ON-BATTERY`/`LOW-BATTERY` status flags that modify behavior but do not stop monitoring.
- SELFTEST: verify each sensor responds + radio init + key present; failures → FAULT flag, continue with
  remaining sensors.
- WARMUP: suppress gas-based alarms until burn-in elapsed (design.md §7); heat/flame watch active.
- MONITOR → PRE-ALARM: when fusion hazard crosses the lower hysteresis threshold.
- PRE-ALARM → ALARM: when corroboration + dwell (persistence) satisfied → local annunciation + signed alert.
- ALARM → MONITOR: only after hazard clears the lower threshold for a dwell time (hysteresis prevents
  chatter). Latching option for human acknowledgement (Rule 19).
- FAIL-SAFE: a dead/stuck node is reported by peers as "offline/unknown", never "all clear" (design.md §6).

## 4. Timing & duty cycling
- Fast loop (flame/heat): high rate (sub-second) always on — fast fires. Slow loop (gas/humidity): lower
  rate, duty-cycled to save power. Exact rates pinned at build from measured current + sensor time constants
  [quota: low-power radio + field-test methodology]. Rate-of-rise window sized to sensor response time
  (DHT22 ~2 s; BME280 faster) — recorded in CALIBRATION_PROTOCOL.md.

## 5. Local dashboard content (served offline from the device)
Live sensor curves; current state (MONITOR/PRE-ALARM/ALARM); alert tier (ties to WS3 architecture.md);
fused confidence + uncertainty; per-sensor anomaly & health flags (P10 edge spec); event log; node/battery/
radio status; last-signed-message status. AUTH REQUIRED (security): WPA2 SoftAP with non-default password +
signed messages; an unauthenticated open dashboard is explicitly rejected (design.md §4).

## 6. Local logging / data formats
- Append-only event log (state transitions, alarms, faults, battery/radio events) + periodic sample log
  (timestamp, raw + engineering values, per-sensor validity, fused hazard, uncertainty) to flash/SD ring
  buffer. CSV/line-delimited JSON (pin at build). This is the data the TEST_PROTOCOL analyzes and the format
  INTEGRATION_NOTES.md feeds to fusion (P14).

## 7. Reliability: watchdog, brownout, ADC/Wi-Fi interaction, faults [quota]
- WATCHDOG: hardware task watchdog resets a hung firmware; the supervisor pets it only when the monitor loop
  is healthy. Document expected reset behavior.
- BROWNOUT: enable the ESP32 brownout detector; on brownout, save state + annunciate low-power, enter safe
  shutdown; recover to SELFTEST on power return.
- ADC vs Wi-Fi: ESP32 ADC2 is unusable while Wi-Fi is active — assign all analog sensors (MQ-2/MQ-135/flame-
  ADC) to ADC1, OR gate Wi-Fi during ADC reads; this is a documented known pitfall to design around [quota:
  embedded firmware reliability]. Pin the ADC channel map accordingly (see HARDWARE_BUILD.md pin map).
- FAULTS: every sensor read is validity-checked; NVS/key errors, radio errors, and sensor faults set status
  flags surfaced on the dashboard and to peers; the node never hides a fault.

## 8. Signed alert messages (MCU-feasible) — inherits design.md §5
HMAC-SHA256 or hardware AES-CMAC over payload with a per-deployment pre-shared key in NVS; monotonic counter
+ timestamp + nonce for replay protection; receivers reject non-increasing counters / stale timestamps / seen
nonces. Message schema (CAP-aligned, see WS3 threat_model.md): {node_id, seq, ts, state, hazard, uncertainty,
health, nonce, mac}. Acceptance (TEST_PROTOCOL): receiver REJECTS a spoofed and a replayed message.

## 9. Honesty
Specification only; no code, no measurement. Every reliability/calibration/TinyML choice is to be backed by a
cited quota paper (ws7_iot/literature_map.md P13) or a datasheet; numbers appear only as targets/"to be filled
after the build". Library versions pinned at build time.
