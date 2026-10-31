# PHASE_13_report — WS7b IoT DESIGN & BUILD MANUAL (DOCUMENTS ONLY)

Phase P13 (MASTER_PROMPT L617). Status: COMPLETE to gate (continuous mode — completion record, not a halt).
Nothing built, flashed, or tested (Rule 16). Rule 19: the node is an ADVISORY sensor under human oversight.

## Objective
Write the complete design & build manual so the prototype can be built later without further research.

## What was produced (ws7_iot/)
- FIRMWARE_SPEC.md — modules, BOOT→SELFTEST→WARMUP→MONITOR⇄PRE-ALARM⇄ALARM state machine with orthogonal
  FAULT/ON-BATTERY/LOW-BATTERY flags, timing/duty-cycle, local logging + dashboard content, offline op,
  signed+replay-protected messages, watchdog/brownout/ADC-vs-Wi-Fi fault handling (no code).
- HARDWARE_BUILD.md — ESP32 pin map (ADC1 rule), power design, enclosure/mounting, step-by-step assembly,
  expected readings + troubleshooting table.
- CALIBRATION_PROTOCOL.md — per-sensor (MQ burn-in/baseline/T-RH compensation/per-unit gain-offset; flame
  outdoor threshold; temp offset + rate-of-rise window); re-calibration schedule.
- TEST_PROTOCOL.md — characterization, safe-stimuli detection, the core single-vs-rate-of-rise-vs-fusion-vs-
  TinyML-vs-physics-vs-anomaly comparison, networking (latency/reach/node-removal/spoof+replay), small-sample
  statistics, logging format. All protocol, none executed.
- DEMONSTRATION_PLAN.md + LIMITATIONS.md — 3-5 min repeatable demo script, backup plan, architecture-figure
  spec, photo list, and the honest will/won't-prove statement.
- INTEGRATION_NOTES.md — data formats feeding P14 fusion / P12 alerting / P11 deepfake-corroboration.
- PROGRAM/sota/P13_sota_scan.md — baselines + targets; HARDWARE_BUDGET.md P13 re-verification note.

## Quota (15 required → MET)
20 NEW primary arXiv (ABS), 7 topics: calibration/compensation (reference-free, GWR, duty-cycle-aware,
variational-Bayes drift+fault, edge temporal model, classic gas+dust+T/RH array); TinyML/quantization (8-bit
near-lossless default, 2-bit via QGT at 81 KB, 32-64 KB RAM model choice, ESP32-S3 on-device patterns);
firmware reliability (core-separation + static scheduling, state-machine faults + NTP + env hardening + >90%
completeness); field-test methodology; distributed fault detection (BMA); low-power radio measurement (RSSI/
SNR, T/RH affects even ranging). 0 FT; running body-level deep FT NEW unchanged at 100.

## Honesty & limits (§0.5)
DOCUMENTS-ONLY; all numbers source-reported or datasheet targets ("to be filled after the build"). NO fire-
detection-labeled public IoT dataset exists (GAP → own-data collection). Watchdog/brownout/ADC-vs-Wi-Fi +
small-sample statistics are thin on arXiv → that guidance is DOCUMENTED ESP-IDF platform behavior
(engineering fact), flagged. BOM RE-VERIFICATION is HONESTLY PARTIAL: live prices could not be re-fetched
(web_search keyless); P6 prices stand AS-OF-P6; build-time re-pricing required. India radio-band legality
flagged for expert review. Vision FPS baselines are above-ESP32 hardware.

## Open actions carried
Build-time re-pricing + cell/enclosure/India-legal-radio second-source quote; collect own fire-sensor data;
measure the on-device latency/RAM/flash/current + radio ranges (closes P9/P10/P12 "other-hardware" figures);
confirm India LoRa band legality.

## Gate
PROGRAM/gate_messages/PHASE_13_gate.md. Auto-proceeding to P14 (WS1b meta-fusion) — whose reading quota (22
papers, reader 41253dff) was PIPELINED and is ALREADY in hand.
