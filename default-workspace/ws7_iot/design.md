# ws7_iot/design.md — Preliminary design of the low-cost fire-detection IoT node (P6)

STATUS: RESEARCH-ONLY preliminary design (Phase P6). No firmware, no hardware. Numbers are targets/
planning values from datasheets and literature, never our own measurements. The on-device anomaly &
sensor-fault layer is only SKETCHED here and is specified in P10. Rule 19: this node is an ADVISORY
sensor that complements certified alarms under human oversight — never an autonomous life-safety device.

Project-scope note (§0.5): per MASTER_PROMPT line 3 the project is "disaster / fire detection and
response ... IoT ...". This document is the FIRE-detection node (WS7a).

---

## 1. Node architecture decision (count vs sensor quality)
Evidence-driven choice: a small number of RICHER nodes rather than many single-sensor nodes, because the
dominant failure mode of cheap fire detectors is FALSE ALARMS, and the literature consistently shows
false-alarm suppression needs MULTI-sensor fusion (smoke + gas + heat ± vision), not more single sensors.
Two complementary node types share one firmware base:
- **Type A — Sensor node** (primary, cheapest): ESP32 DevKit + smoke/gas (MQ-2) + flame (IR) + temp/
  humidity (DHT22 or BME280) + buzzer/strobe + radio. Does multi-sensor fusion + rate-of-rise logic.
- **Type B — Camera node** (optional, where budget allows): ESP32-CAM (OV2640) running a tiny flame/smoke
  classifier (EFA-YOLO-class, ~1.4M params) for VISUAL confirmation to cut false alarms.
Recommended prototype: 1× Type A as the baseline (fits well under ₹2000); add 1× Type B only if the
verified BOM leaves room (decided in BOM.md / HARDWARE_BUDGET.md from verified prices).

## 2. Sensing layer
| Modality | Part (candidate) | Why | Known weakness (→ handled in logic) |
|----------|------------------|-----|-------------------------------------|
| Smoke/combustible gas | MQ-2 (analog) | cheapest smoke+LPG/smoke proxy | drift, warm-up, humidity/temp cross-sensitivity, no absolute calibration |
| Air quality / CO proxy | MQ-135 (optional) | cheap VOC/CO2 proxy | not a true CO sensor; cross-sensitive |
| Flame | IR flame sensor (760–1100 nm) | detects flame flicker/IR fast | sunlight/IR false triggers; narrow FOV |
| Temperature + humidity | DHT22/AM2302 or BME280 | rate-of-rise + fixed-threshold heat logic; humidity compensates gas sensor | DHT22 slow (~2 s), limited range; BME280 better + pressure |
| Vision (Type B) | OV2640 on ESP32-CAM | visual confirmation, false-alarm cut | low light, smoke-vs-steam confusion, compute/RAM limits |
Operating-range requirement for India (verify per datasheet in BOM): components must tolerate ~0–50 °C and
high humidity; MQ sensors need humidity/temperature compensation in software.

## 3. On-device logic (fusion + physics, all runnable on ESP32)
Layered, cheapest-first (each layer gates the next → saves power and cuts false alarms):
1. **Threshold + rate-of-rise (physics, cheap):** fixed over-temperature AND rate-of-rise (dT/dt) heat
   logic (classic fire-alarm engineering); smoke/gas rising-rate thresholds. Rate-of-rise catches fast
   fires before an absolute threshold; fixed threshold catches slow smouldering — use BOTH.
2. **Multi-sensor fusion (false-alarm suppression):** require corroboration across modalities (e.g.
   smoke↑ AND (heat-rate↑ OR flame-IR)) before escalating, with per-sensor confidence. Tunable so that a
   single noisy sensor cannot alarm alone (the main false-alarm defense).
3. **Tiny ML (optional, Type B / or a small MCU classifier on fused features):** a quantized classifier
   for fire-vs-nuisance; model size/RAM budgeted in P6 quota reading (EFA-YOLO-class is feasible on an
   ESP32-CAM per source-reported 1.4M params / tens-of-ms CPU — source numbers, not ours).
4. **Anomaly & sensor-fault layer (SKETCH → specified in P10):** detect stuck/flatline/out-of-range/
   drifting sensors and down-weight them in fusion (ties to on-device SSL anomaly 2610.03649 vs iForest/
   OCSVM/LOF). A faulty sensor must degrade gracefully, never silently alarm or silently go blind.
Output of logic = a calibrated hazard level + per-sensor health, NOT a raw boolean, so the alerting layer
can apply hysteresis and the (later) system-level conformal/physics shield.

## 4. Alerting layer (fully offline)
- **Local annunciation first:** on-board buzzer + bright LED strobe fire immediately on a confirmed local
  alarm (works even if radio is down).
- **Local network, NO internet:** ESP32 hosts a SoftAP + a tiny local dashboard (HTML served from the
  device) reachable by a phone/laptop on-site; OR nodes talk peer-to-peer via **ESP-NOW** (connectionless,
  low-latency, no router) for multi-node; **LoRa** for long-range/low-power links where nodes are far
  apart. Choice per deployment; all three are internet-free.
- **SECURITY (flagged, security_awareness):** the local dashboard and any node-to-node link are, by
  default, exposed services → they MUST NOT be left unauthenticated. Minimum: WPA2 on the SoftAP with a
  non-default password, AND signed messages (next section). An unauthenticated open AP serving a fire
  dashboard is explicitly rejected.

## 5. Signed messages + replay protection (lightweight, MCU-feasible)
- Each inter-node / node-to-dashboard message is authenticated with an **HMAC-SHA256** (or the ESP32
  hardware-accelerated AES-CMAC) over the payload using a pre-shared key provisioned at setup.
- **Replay protection:** every message carries a monotonic counter + timestamp + fresh nonce; receivers
  reject non-increasing counters / stale timestamps / seen nonces. This defeats record-and-replay of a
  fake "all clear" or a fake "alarm".
- Keys are per-deployment, stored in NVS, never hard-coded in shipped source; rotate on compromise.
- Acceptance test (later): demonstrate the receiver REJECTS a spoofed and a replayed message.

## 6. Offline mode & power design (incl. power cuts — the Indian reality)
- **Fully offline by design:** no cloud dependency; all detection, annunciation, and local alerting work
  with zero internet. Internet (if ever added) is an optional, authenticated uplink, never a dependency.
- **Power:** single 18650 Li-ion (protected) + TP4056 charger; boost/LDO (MT3608/AMS1117) to 3.3/5 V;
  optional small 5–6 V solar panel trickle-charges the cell → the node rides through grid power cuts.
- **Power-cut behavior:** on mains loss the node continues on battery; it should send a "on-battery" status
  (signed) and reduce duty cycle (sleep sensors between reads, keep flame/heat watch) to extend runtime;
  on low battery it annunciates locally and flags low-power state before shutdown. The node must FAIL
  SAFE/known: a dead node is reported as "offline/unknown" by peers, never assumed "all clear".
- Budget the sleep/active duty cycle so a single 18650 gives a usefully long autonomy (quantified at build
  time from measured current, not estimated here).

## 7. Calibration procedure (as a protocol, run at build time)
- MQ-2/MQ-135: 24–48 h burn-in on first use; then baseline in clean air; apply the datasheet Rs/R0 curve;
  software temperature+humidity compensation from the DHT22/BME280 reading. Record baseline per sensor.
- Flame sensor: set threshold outdoors in daylight to find sunlight false-trigger level; set above it.
- Temperature: offset-calibrate against a reference thermometer; set rate-of-rise and fixed thresholds
  from fire-alarm-engineering guidance (recorded in the physics/established-formula work, P7).
- Re-baseline periodically (gas sensors drift). Calibration is a documented protocol here; actual
  calibration happens in the build phase.

## 8. Acceptance criteria for the later prototype (pre-registered)
1. **Cost ≤ ₹2000** with verified Indian listings (BOM.md / HARDWARE_BUDGET.md).
2. **Fully offline** demonstration (no internet) of detection → local alarm → local dashboard/peer alert.
3. **False-alarm-suppression comparison** with repeated trials: multi-sensor fusion vs single-sensor,
   on the approved safe stimuli vs nuisance sources (steam, cooking smoke, sunlight) — report counts with
   confidence, from our own logs (SAFETY.md governs the tests).
4. **Alert latency** (stimulus → local annunciation) and **radio reach** (ESP-NOW/LoRa range) measured and
   reported with conditions.
5. **Signed-message spoof + replay rejection** demonstrated.
6. **Graceful degradation:** induced sensor fault is detected and down-weighted; a dead node reads as
   "offline", not "safe".
All claims come from our own build-phase logs; nothing is claimed as a result in this research run.

## 9. Open items carried to later phases
- Exact tiny-ML model + RAM/flash budget on ESP32-CAM → finalize with P6 quota reading + P10/P14 build.
- Anomaly/sensor-fault layer full spec → P10.
- Physics thresholds (rate-of-rise constants, ceiling-jet transport delay, sensor time-constants) → P7.
- India radio-band/power legal confirmation (LoRa 865–867 MHz) → flagged for expert/legal review.
