# ws7_iot/CALIBRATION_PROTOCOL.md — per-sensor calibration protocol (P13, WS7b)

Phase P13 · DOCUMENTS ONLY. MASTER_PROMPT P13 task 4. A protocol to RUN AT BUILD TIME; nothing calibrated now
(Rule 16). Compensation methods are backed by the P13 calibration quota [quota] (ws7_iot/literature_map.md
P13); where the literature does NOT support a compensation, we do NOT invent one. Governed by ws7_iot/SAFETY.md.

## 1. General sequence (every unit, logged)
Record per-unit serial, date, ambient T/RH, firmware version. Burn-in → baseline → per-unit gain/offset →
compensation fit → verification. Store resulting constants in NVS (FIRMWARE_SPEC §2). Re-baseline schedule in
§6 (gas sensors drift).

## 2. MQ-2 / MQ-135 (metal-oxide gas/smoke)
- BURN-IN: 24–48 h powered in clean air on first use (datasheet + design.md §7); gas-based alarms suppressed
  until elapsed (WARMUP state).
- BASELINE R0: in clean air at known T/RH, record the sensor resistance → R0 using the datasheet Rs/R0 curve.
- TEMPERATURE/HUMIDITY COMPENSATION: apply the datasheet (or literature [quota]) correction of Rs/R0 vs
  T/RH using the DHT22/BME280 reading; fit per-unit if the quota method supports it, else use datasheet
  curve. DOCUMENT which was used; do NOT claim a compensation the literature doesn't support.
- PER-UNIT GAIN/OFFSET: because cheap MQ units vary, record each unit's clean-air baseline and scale.
- VERIFY: expose to a safe known stimulus (incense smoke at safe distance, SAFETY.md) and confirm monotonic
  response + recovery; record response/recovery time (feeds rate-of-rise window, FIRMWARE §4).

## 3. IR flame sensor
- Set threshold OUTDOORS in daylight to find the sunlight IR false-trigger level; set the operating threshold
  above it (design.md §7). Record FOV/distance sensitivity with a safe flame at a safe distance (SAFETY.md).

## 4. Temperature / humidity (DHT22 or BME280)
- OFFSET-CALIBRATE temperature against a reference thermometer; record offset. BME280 preferred (faster,
  wider range, pressure). Record the sensor time constant → sets the dT/dt rate-of-rise window.
- Fixed over-temperature + rate-of-rise constants come from fire-alarm engineering / P7 physics (recorded
  there), NOT invented here.

## 5. Fusion & anomaly thresholds
- Fusion corroboration thresholds + hysteresis set from the characterization data (TEST_PROTOCOL §2) at build;
  the anomaly/sensor-fault bounds (stuck/flatline/out-of-range/drift) come from the P10 edge spec.

## 6. Re-calibration schedule
Gas sensors drift → periodic clean-air re-baseline (interval set at build from observed drift); log every
re-baseline. Flame/temp re-checked on relocation or seasonal change. This cadence ties to the P9/P10 "normal
reference data policy".

## 7. Honesty
Protocol only; no sensor was calibrated. Compensation choices are datasheet- or quota-backed; unsupported
compensations are explicitly NOT applied. All constants filled in at build time and logged.
