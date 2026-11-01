# PROGRAM/sota/P13_sota_scan.md — low-cost IoT fire-detection prototypes SOTA scan (WS7b)

Phase P13 · DOCUMENTS ONLY. MASTER_PROMPT P13 task 1. The published baselines our later measurements will be
compared with + a targets section (process targets, not results — Rule 16). All numbers SOURCE-REPORTED;
detail + IDs in ws7_iot/literature_map.md P13 section.

## 1. Published low-cost multi-sensor fire-detection prototypes (baselines)
- Incipient-fire e-nose (1708.08750): gas+dust+T/RH array → feature-select → PCA → PCA-PNN classifier;
  SOURCE-REPORTED robust "regardless of T/RH, drift, concentration". CLOSEST comparator to our Type A node;
  its test conditions (5 fire sources × 3 materials, odor profiles) are the kind of comparison our
  TEST_PROTOCOL §4 mirrors.
- IoT forest-fire use case (2407.09117): real distributed low-cost nodes (SEA-HAZEMON); preliminary
  real-deployment efficacy + design guidelines — the field-reality baseline.
- Compact fire-vision CNNs (2010.08833): 95% full-frame / 97% superpixel, 40/18 fps CPU, 49 fps Xavier-NX —
  an UPPER-BOUND reference (hardware above ESP32 class); our Type B must fit a far smaller budget.

## 2. Calibration / TinyML / reliability baselines (what good practice looks like)
- Calibration: reference-free/unsupervised (1805.11999, 2508.02724), per-location GWR (2510.05646),
  duty-cycle-aware (2112.09072), edge temporal model + 4-scenario eval (2610.11236), classic robust array
  pipeline (1708.08750).
- TinyML footprints: 8-bit near-lossless (2110.10486, 2203.05492); 2-bit only via QGT (81 KB, −3%,
  2103.06231); ESP32-class working set ~32-64 KB RAM (2412.09289); ESP32-S3 on-device patterns (2604.23012).
- Reliability/field: core-separate + static scheduling + zero-copy IPC (2607.23220); state-machine faults +
  NTP + local-first SD + env hardening + >90% data-completeness KPI (2601.03867); BMA fault flagging
  (1301.4795); radio measurement w/ T/RH covariates (2509.23125, 2412.01609); field-trial honesty (2003.08647).

## 3. TARGETS section (for the later build — process targets, NOT results, Rule 16)
- COST: ≤ ₹2000 verified (HARDWARE_BUDGET.md).
- CALIBRATION: implement T/RH + drift compensation per CALIBRATION_PROTOCOL (quota-backed); evaluate against
  reference/transfer/drift/event scenarios (2610.11236) — report compensated vs raw on OUR logs.
- FUSION: beat single-sensor false-alarm rate at matched sensitivity (TEST_PROTOCOL §4) — the primary endpoint.
- TinyML (Type B): fit the chosen model in ESP32 flash/SRAM at 8-bit (near-lossless default); report measured
  RAM/flash/latency.
- RELIABILITY: deterministic sampling under Wi-Fi/LoRa load (core-separation); watchdog/brownout handled;
  >90% data-completeness analog over a field window.
- RADIO: measure ESP-NOW/LoRa reach vs distance with RSSI/SNR + T/RH covariates (closes WS3 GAPs + P12
  "other-hardware" figures).
- All targets are compared to the §1 baselines AFTER the build; nothing is measured now.

## 4. Honest gaps
No fire-detection-LABELED public IoT sensor dataset found (GAP → collect our own normal + safe-stimulus logs,
TEST_PROTOCOL). Watchdog/brownout/ADC-vs-Wi-Fi + formal small-sample statistics are thin on arXiv → the
FIRMWARE_SPEC §7 guidance there is DOCUMENTED ESP-IDF platform behavior (engineering fact), flagged plainly.
Vision FPS baselines are above-ESP32 hardware. India radio-band legality flagged for expert review.
