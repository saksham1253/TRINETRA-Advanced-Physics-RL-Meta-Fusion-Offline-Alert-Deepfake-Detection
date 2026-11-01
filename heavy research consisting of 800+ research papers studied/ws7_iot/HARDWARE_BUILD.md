# ws7_iot/HARDWARE_BUILD.md — hardware documents & assembly manual (P13, WS7b)

Phase P13 · DOCUMENTS ONLY. MASTER_PROMPT P13 task 3. Nothing built. Builds on ws7_iot/{design.md, BOM.md,
HARDWARE_BUDGET.md} (P6). Pin maps/wiring are TEXT + TABLE specifications a designer turns into a schematic/
PCB; a one-page wiring diagram is specified for a designer (see DEMONSTRATION_PLAN.md figure spec). No
measurement claims. Expected readings are datasheet/literature targets, never our own measurements.

## 1. Bill of materials (reference — authoritative in BOM.md / HARDWARE_BUDGET.md)
Type A sensor node (prototype baseline, ≤ ₹2000 verified): ESP32 DevKit; MQ-2 (smoke/combustible gas);
IR flame sensor; DHT22 or BME280 (temp/humidity[/pressure]); active buzzer; bright LED/strobe; 18650 Li-ion
(protected) + holder; TP4056 charger; MT3608/AMS1117 regulation; optional small solar panel; perfboard/
jumpers/enclosure. Optional Type B: ESP32-CAM (OV2640). Optional radio: LoRa module (SX127x/SX1262) for
long-range; ESP-NOW needs no extra hardware. EXACT parts + prices re-verified in HARDWARE_BUDGET.md (task 8).

## 2. Pin map (ESP32 DevKit, Type A) — ADC1 rule from FIRMWARE_SPEC §7
| Signal | ESP32 pin (candidate) | Notes |
|--------|-----------------------|-------|
| MQ-2 analog out (AO) | GPIO36 (ADC1_CH0 / VP) | ADC1 ONLY (ADC2 dies with Wi-Fi); divide 5V AO to ≤3.3V with a resistor divider |
| MQ-135 analog out (optional) | GPIO39 (ADC1_CH3 / VN) | ADC1; same divider caution |
| IR flame (digital) | GPIO34 (input-only) or any GPIO | if analog flame, use an ADC1 channel |
| DHT22 data | GPIO4 (with 10 kΩ pull-up) | single-wire; OR BME280 on I2C |
| BME280 (if used) | I2C SDA GPIO21 / SCL GPIO22 | 3.3V; preferred over DHT22 |
| Buzzer | GPIO25 | via transistor if current > GPIO limit |
| LED/strobe | GPIO26 | via transistor/MOSFET for a bright strobe |
| LoRa (optional) | SPI: SCK GPIO18, MISO GPIO19, MOSI GPIO23, CS GPIO5, RST/DIO per module | 3.3V logic |
| Battery voltage sense | GPIO35 (ADC1) | via divider; for on-battery/low-battery logic |
Pins are CANDIDATES to finalize at build (avoid strapping pins GPIO0/2/12/15 for inputs that float). Input-
only pins (34–39) have NO internal pull-ups — add external pull-ups where needed.

## 3. Power design
Single protected 18650 → TP4056 (charge) → boost (MT3608 to 5V for MQ heaters) + LDO (AMS1117 to 3.3V for
ESP32/sensors); optional 5–6V solar trickle. MQ sensor HEATERS dominate current — budget them explicitly;
duty-cycle gas sensors (FIRMWARE_SPEC §4) to extend 18650 autonomy. Autonomy figure = measured at build, NOT
estimated here. Add bulk + decoupling caps near the ESP32 (Wi-Fi current spikes cause brownouts — FIRMWARE
§7). Common ground for all analog sensors; keep ADC lines short.

## 4. Enclosure & mounting (within budget)
Ventilated enclosure so smoke/gas reach the sensors while shielding from rain/direct sun (flame-sensor
sunlight false-trigger, design.md §7); mount per fire-detection siting guidance (ceiling/high on wall away
from vents/windows — ties to P7 ceiling-jet/transport-delay physics). Strobe visible; buzzer unobstructed.
Cable strain relief; battery accessible. Specify an IP-rated box for outdoor/industrial pilots.

## 5. Step-by-step assembly (follow later at build)
1. Flash/verify a bare ESP32 (blink) before adding sensors. 2. Wire power subsystem (TP4056 + regulators);
verify 3.3V/5V rails under load BEFORE connecting the MCU. 3. Add DHT22/BME280 (I2C scan / read). 4. Add MQ-2
on ADC1 with divider; begin 24–48 h burn-in (CALIBRATION_PROTOCOL). 5. Add flame sensor; set outdoor
threshold. 6. Add buzzer + strobe; test annunciation. 7. Add radio (ESP-NOW first; LoRa if used). 8. Load
firmware modules incrementally (sensor → fusion → alerting → dashboard → radio). 9. Provision per-deployment
HMAC key into NVS. 10. Full self-test. Each step has a PASS check and a troubleshooting row (§6).

## 6. Expected readings & troubleshooting (datasheet/literature targets — NOT our results)
| Symptom | Likely cause | Action |
|---------|--------------|--------|
| MQ-2 reads max/flat | not burned-in / divider wrong / on ADC2 w/ Wi-Fi | wait burn-in; check divider; move to ADC1 |
| DHT22 NaN/timeouts | missing pull-up / too-fast polling (~2 s min) | add 10 kΩ pull-up; slow the loop |
| Random reboots | brownout from Wi-Fi current spike | add caps; stronger supply; enable brownout handling |
| Flame false triggers in daylight | sunlight IR | raise threshold outdoors; shade sensor |
| ADC noise/garbage when Wi-Fi on | sensor on ADC2 | reassign to ADC1 (FIRMWARE §7) |
| Peers show node "offline" | watchdog reset / power loss | check logs; this is FAIL-SAFE behavior, not "all clear" |

## 7. Honesty
All pin assignments, currents, and readings are datasheet/literature TARGETS to confirm at build; the ADC1/
Wi-Fi and brownout cautions are documented pitfalls (quota-backed in FIRMWARE_SPEC/literature_map). No board
was built or measured. BOM cost authoritative in HARDWARE_BUDGET.md (re-verified in P13 task 8).
