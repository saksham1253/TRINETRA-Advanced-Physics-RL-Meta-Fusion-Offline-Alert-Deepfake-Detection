# ws7_iot/literature_map.md — P6 quota reading map (fire-detection IoT node)

Phase P6 · 2026-10-07/09 · RESEARCH-ONLY. ≥15 NEW quota MET: **20 NEW sources** read this phase (1
FT-PARTIAL + 19 ABS). ALL metrics are SOURCE-REPORTED, never ours (§0.5 / Rule 16). Reading was done via
a dedicated reading pass (arXiv abstracts + one HTML body). HONEST GAP (§0.5, D-010): `web_search` had no
API key this session → MDPI Sensors/Fire/Electronics and NFPA/BS/IS standards could NOT be fetched, so
four requested topics remain UNCOVERED and are carried to backlog: (a) rate-of-rise vs fixed-temperature
heat-detector engineering (standards); (b) ESP32-CAM embedded-vision FPS/accuracy; (c) smoke optical-
extinction/obscuration physics; (d) MQ-2/MQ-135 datasheet-level warm-up/cross-sensitivity. arXiv itself
is thin for on-device sensor-fusion fire detection (documented in P6_sota_scan.md).

## Reading table (20 NEW)
| # | ID | Title (short) | Depth | Theme | Source-reported headline (NOT ours) | Node implication |
|---|----|---------------|-------|-------|-------------------------------------|------------------|
| 1 | 2409.12635 | EFA-YOLO flame detection | ABS | vision | 1.4M params, 4.6 GFLOPs, 22.19 ms/img on **desktop CPU** (not MCU) | camera-stage accuracy ceiling + shrink target; INT8 needed for ESP32-CAM |
| 2 | 2508.14597 | Reliable Smoke Detection (optical-flow+Swin+uncertainty) | ABS | vision | calibrated aleatoric+epistemic uncertainty; no params/latency | too heavy; borrow "emit uncertainty + temporal persistence before alarm" |
| 3 | 2512.03257 | PyroFocus two-stage wildfire | ABS | vision/arch | cheap classify → FRP only when needed; no MCU numbers | two-stage gate pattern: cheap sensors wake the camera CNN |
| 4 | 2512.12199 | Thermal-RGB fusion micro-UAV | ABS | fusion/edge | rule-based, sub-50 ms on embedded SoC (sim) | precomputed-LUT RGB+thermal rule fusion is ESP32-feasible IF thermal added |
| 5 | 2310.06224 | Context-aware status updating (AoI, CO fire) | ABS | comms | up to 100× vs periodic, 10× vs random (sim) | value-aware reporting: raise rate as CO/temp trend dangerous |
| 6 | 2608.23192 | Energy-Proportional Multimodal Vision IoT Node (ETH) | **FT-PARTIAL** | arch/power | 222 µW idle, 28.7 mJ/cycle, 82.7 ms, ~11 FPS, ~3-mo on 1.85 Wh @1% duty; HM0360@25fps alone = 13.5 mW | STRONGEST template: cheap always-on trigger gates camera; duty cycle, not CNN, dominates energy |
| 7 | 2608.21646 | Power-Performance Characterization of TinyML | ABS | TinyML | per-abstraction-layer energy/latency cost model | budget TFLite-Micro interpreter overhead on ESP32; fuse ops |
| 8 | 2609.30272 | ENAS hardware-aware NAS for MCUs | ABS | TinyML | 79.4% acc STM32H743; **peak activation RAM = binding constraint** | optimize our model for peak SRAM, not params/FLOPs (ESP32-S3 ~512 KB) |
| 9 | 2610.06241 | Few-shot prototype head on PSoC6 (ECG) | ABS | TinyML | 1,314-param 1-D CNN, 11.39 ms, 5.2 KB flash, 22.2 KB SRAM | tiny 1-D CNN on sensor time-series fits MCU; on-device prototype calibration, no backprop |
| 10 | 2608.25646 | LDAC-Net drift-robust low-cost MOX gas | ABS | gas sensor | 68.2% SmellNet / 70.6% eNose-Drift under drift (source) | MQ sensors drift → per-window baseline norm + multi-lag delta features (ESP32-cheap) |
| 11 | 2507.17071 | Sensor-drift compensation via KD (e-nose) | ABS | gas sensor | KD +up to 18% acc vs DRCA; warns over-compensation hides variance | make drift correction SLOW; alarm on fast transients mid-adaptation |
| 12 | 2511.00348 | Ultralow-power standoff acoustic leak detection | ABS | comms/power | 20–200 µW; detects 0.15 L/min leak >10 m behind walls | classify on-device, transmit only a few bytes = biggest battery lever |
| 13 | 2406.16917 | GreenShield CNN forest monitoring | ABS | low-cost BOM | Arduino + DHT11 + flame + gas/smoke + GSM, adaptive threshold; **no FA metrics** | validates DHT+flame+MQ BOM + adaptive thresholds; FA gap → we must test nuisances |
| 14 | 2610.11236 | Low-cost indoor AQ calibration dataset+model | ABS | calibration | 6-mo, 5 loc dataset; 4 eval scenarios incl drift + event-shift | evaluate node for cross-location transfer, drift, abrupt nuisance events |
| 15 | 2604.21527 | Temporal DL calibration of low-cost AQ sensors | ABS | calibration | NO2 22.11% / PM10 12.42% / PM2.5 9.1% expanded uncertainty (source) | feed temp+humidity INTO gas interpretation (cross-sensitivity) |
| 16 | 2511.19810 | RESPIRE outlier-resistant CO calibration (INDIA) | ABS | calibration/India | 4 India sites, 2 seasons, 6 sensor packages; provable outlier resistance | India reality: calibration must survive season/site/unit; outliers normal; robust fit + re-cal |
| 17 | 2605.26159 | DCP compact safety-first device protocol | ABS | security | <50-byte frame, optional 16-B HMAC; 27.6 KB flash / 0.6 KB RAM ESP32; rejects 100% cap-escalation | 16-B HMAC + monotonic nonce fits ESP32; no unauthenticated endpoints |
| 18 | 2605.19793 | Motion-coupled (batteryless) sensing + LoRa | ABS | power/comms | one actuation powers wake-sense-LoRa; 99.3% tx (5,945 events) | one event-triggered LoRa uplink (not streaming) is energy-sane |
| 19 | 2608.00409 | SIC-aided decentralized LoRa resource alloc | ABS | comms | tx success 64.0→71.1%, 293.9→328.3 bit/J vs UCB1 (source) | adaptive SF/power (tiny bandit) improves alarm delivery in dense nets |
| 20 | 2208.00210 | Multi-Category Visual Smoke DB | ABS | dataset | 70,196 imgs, smoke TYPES (complete/incomplete/direct); algos underperform | multi-class smoke labels needed so steam/clean-exhaust ≠ alarm |

## Consolidated design implications (→ folded into design.md)
1. Two-tier wake-on-event: cheap always-on sensors (MQ gas + DHT temp/humidity + flame/PIR) gate the
   power-hungry ESP32-CAM CNN — image sensor + duty cycle, not the CNN, dominate battery life ([6],[3],[12]).
2. Optimize any on-ESP32 model for PEAK ACTIVATION RAM, not params/FLOPs ([8]); a useful 1-D sensor-CNN
   fits ~5 KB flash / ~22 KB SRAM ([9]).
3. Camera CNNs (EFA-YOLO 1.4M/22ms-desktop) are shrink targets, treat mAP as upper bound ([1],[6]).
4. Gas processing = per-window baseline normalization + multi-lag rate-of-change features, NOT raw MQ
   readings — main lever vs drift AND nuisance false alarms, ESP32-cheap ([10],[11]).
5. Feed temp+humidity INTO gas interpretation (cross-sensitivity) ([15]); MQ warm-up required.
6. Drift compensation SLOW/conservative so it can't mask a slow fire-gas rise; alarm on fast transients
   mid-adaptation ([11]) — the ML echo of classic rate-of-rise heat logic.
7. False-alarm suppression = temporal persistence + confidence margin ([2]) + multi-class smoke
   discrimination ([20]) + cross-modal voting (gas+temp+flame+camera), never single-channel.
8. Comms: classify on-device, send few-byte status, one event-triggered uplink, value-aware rate
   ([12],[18],[5]); adaptive LoRa params in dense nets ([19]).
9. Security from day one: 16-B HMAC + monotonic nonce (~sub-1 KB RAM, ~28 KB flash on ESP32) ([17]); no
   unauthenticated endpoints.
10. India reality: calibration must survive season/site/dust/unit variation; outliers normal; periodic
    re-calibration + robust fit ([16]); evaluate for transfer/drift/abrupt-event ([14]).

## Open datasets found (added to DATASETS.md as D27–D30, under §0.9A rules)
- Multi-Category Visual Smoke DB — 70,196 imgs, multi-class smoke — arXiv:2208.00210 (license per paper).
- UCI Gas Sensor Array Drift — MOX e-nose drift benchmark — https://archive.ics.uci.edu/dataset/224/ (UCI).
- Low-Cost Indoor AQ Calibration dataset — 6-mo, 5 loc — arXiv:2610.11236 (per paper).
- RESPIRE India CO calibration — code/data pointers https://github.com/purushottamkar/respire — arXiv:2511.19810.
- (reusable code, not dataset) DCP ESP32 HMAC firmware — https://github.com/device-context-protocol/dcp — MIT.

## Novelty / honesty
No claim here is ours; all are source-reported. The node design borrows PATTERNS (two-tier gating, delta/
baseline gas features, HMAC+nonce, few-byte uplink), each attributed. Four heat-detector/vision-FPS/smoke-
optics/MQ-datasheet topics remain UNCOVERED (web_search gap) → PROGRAM backlog + chase in P7/standards.

---

## P13 section — build-manual quota (WS7b) — 20 NEW primary arXiv (reader 12b95018; 9 fetches)
HONEST: all ABS; IDs/years arXiv-ID-derived + subagent-reported, NOT re-fetched (residual risk, §0.5); all
numbers SOURCE-REPORTED (Rule 16). These back the choices in FIRMWARE_SPEC/HARDWARE_BUILD/CALIBRATION/
TEST_PROTOCOL. Running body-level deep FT NEW total UNCHANGED at 100 (ABS breadth).

### T1 calibration / compensation for cheap sensors
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 1912.06384 | Low-cost AQ sensor calibration survey | canonical failure modes: cross-sensitivity, environmental coupling (T/RH), drift; periodic ML re-cal mitigates. The checklist CALIBRATION_PROTOCOL must address. |
| 1805.11999 | Reference-free network calibration | unbiased cross-calibration without a trusted reference node; estimators reach derived lower bounds. ⇒ a field of nodes cross-calibrates. |
| 2112.09072 | Duty-cycle vs calibration trade-off | duty cycle 0.1 (response ~2 min) / 0.01-0.02 (fast) retains calibrated quality vs mains node. Couples power budget to accuracy (FIRMWARE §4). |
| 2510.05646 | GWR calibration | geographically-weighted regression = lightweight per-location gain/offset, post-install. |
| 2508.02724 | Veli reference-free (variational Bayes) | disentangles signal/noise, absorbs drift + erratic/faulty sensors, no co-location; AQ-SDR benchmark. Addresses drift + fault together. |
| 2610.11236 | Lightweight indoor-AQ calibration + dataset | 6-month/5-loc; 4 scenarios (reference-efficient/location-transfer/drift/event); edge-deployable temporal model. Template + eval protocol. |

### T2 fire detection + field practice
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 1708.08750 | Incipient-fire e-nose classifier | gas+dust+T/RH array → feature-select → PCA → PCA-PNN; robust "regardless of T/RH, drift, concentration". CLOSEST match to the WS7b node pipeline. |
| 2407.09117 | IoT forest-fire practical use case (SEA-HAZEMON) | real distributed low-cost nodes; design guidelines + efficacy reality-check. |
| 2010.08833 | Compact fire CNNs (NasNet-A/ShuffleNetV2-OnFire) | 95% full-frame / 97% superpixel; 40/18 fps CPU, 49 fps Xavier-NX. UPPER-BOUND reference (above ESP32 class). |

### T3 TinyML / quantization on MCU
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2203.05492 | Sub-8-bit PTQ empirical study | component-level PTQ pipeline guidance with small calibration set, no retraining data. |
| 2103.06231 | Quantization-Guided Training (QGT) | 81 KB model @2-bit, 17.7× smaller, −3% acc. 2-bit reachable only WITH QGT. |
| 2110.10486 | Quantized latent-replay continual learning | 8-bit ≈ lossless (−0.26%@3000), 4× less memory; 7-bit −5%; vs STM32-L4 baseline. On-device adaptation recipe. |
| 2412.09289 | Quant+distill transformer / compact Mamba | quantized transformer fits 64 KB RAM; Mamba fits 32 KB uncompressed. RAM-budgeted model choice for ESP32. |
| 2604.23012 | On-device vision on ESP32-S3 | 3-class 64×64 trains ~9 min on-device, 6.3 FPS inference; PSRAM-aware memory + 3-tier boot weight resolution. Exact-target firmware/memory patterns. |

### T4 firmware reliability
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2607.23220 | ESP32-S3 dual-core flight firmware | core-separate sensing vs comms, static RTOS scheduling, zero-copy mutex IPC → jitter-free determinism. Keep sampling deterministic while Wi-Fi/LoRa runs. |
| 2601.03867 | ESP32 field DAQ (tropical/LMIC) | interrupt-driven acq + state-machine fault handling + NTP sync + local-first SD + humidity/salt-spray hardening; >90% data-completeness KPI over 6-month campaigns; V-model + FAIR. Near-complete reliability + field playbook. |

### T5 field-test methodology
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2003.08647 | LoRa field trials (Hamburg, RIOT) | field-trial methodology + honest limitation reporting for low-power wireless. |

### T6 on-device anomaly / sensor-fault
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 1301.4795 | Distributed fault detection in WSN | folds error probabilities into event detection + Bayesian model averaging to flag faulty sensors. Suppress single-bad-sensor false alarms (ties P10 edge spec). |

### T7 low-power radio measurement
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2412.01609 | LoRa + TinyML channel hopping | measures RSSI/SNR/packet-loss; TinyML channel selection +63% RSSI / +44% SNR vs random. Measurement methodology + MCU-runnable optimization. |
| 2509.23125 | LoRa 2.4 GHz ToF ranging outdoors | 3×3 grid/400 m²/3 weeks + T/RH; T/RH significantly affect ranging → compensate even the radio. Multi-week gridded field-measurement template. |

### Synthesis (P13)
- CALIBRATION: compensate cross-sensitivity + T/RH + drift [1912.06384]; reference-free/unsupervised
  [1805.11999, 2508.02724], per-location GWR [2510.05646], duty-cycle-aware [2112.09072], edge temporal model
  + 4-scenario eval [2610.11236]; classic gas+dust+T/RH array pipeline robust to T/RH+drift [1708.08750].
- TinyML: ESP32-class working set ~32-64 KB RAM [2412.09289]; 8-bit near-lossless default [2110.10486,
  2203.05492]; 2-bit only via QGT (81 KB, −3%) [2103.06231]; ESP32-S3 on-device patterns [2604.23012]; vision
  FPS numbers are upper-bound (above ESP32) [2010.08833].
- RELIABILITY/FIELD: core-separate + static scheduling + zero-copy IPC [2607.23220]; state-machine faults +
  NTP + local-first SD + env hardening + >90% completeness KPI [2601.03867]; field-trial honesty [2003.08647];
  T/RH covariates in radio field tests [2509.23125]; BMA fault flagging [1301.4795].
- HONEST GAP (reader-flagged): watchdog/brownout/ADC-vs-Wi-Fi interaction and formal small-sample statistics
  are THINLY represented on arXiv — the FIRMWARE_SPEC §7 / HARDWARE_BUILD §2 guidance on these is DOCUMENTED
  ESP-IDF PLATFORM BEHAVIOR (ESP32 ADC2-unusable-with-Wi-Fi, brownout detector, task watchdog), engineering
  fact rather than a cited paper; flagged plainly. No fire-detection-labeled IoT sensor dataset found (GAP).
