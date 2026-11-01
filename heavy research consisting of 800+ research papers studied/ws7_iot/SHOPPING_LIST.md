# ws7_iot/SHOPPING_LIST.md — verified shopping list (P6, RESEARCH-ONLY — the user buys, not me)

STATUS: RESEARCH-ONLY. I never purchase. This is the list the user can act on. Prices = electronicscomp.com,
live **2026-10-09**, **ex-GST** (add 18% for GST-inclusive). Single source this session (see BOM.md limits).
All URLs prefix `https://www.electronicscomp.com`.

## RECOMMENDED PURCHASE — Build B (sensor-fusion node), with the LoRa→ESP-NOW cut applied
Rationale: ESP-NOW/Wi-Fi is built into the ESP32 (₹0) and avoids the 433 MHz India-band problem of the
Ra-02; drop LoRa unless long-range is required.

| Buy | Part | URL (prefix above) | ₹ ex-GST |
|-----|------|--------------------|---------:|
| 1 | ESP32-S2-DevKitM-1 | /espressif-esp32-s2-devkitm-1-development-board | 703.00 |
| 1 | MQ2 gas/smoke module | /mq2-flammable-gas-smoke-sensor-module-india | 68.00 |
| 1 | IR flame module (760–1100 nm) | /flame-sensor-infrared-receiver-ignition-source-detection-module | 29.00 |
| 1 | DHT22/AM2302 | /dht22-am2302-digital-temperature-and-humidity-sensor | 119.00 |
| 1 | Active buzzer module 3.3–5 V | /active-buzzer-module-5v-india | 24.00 |
| 1 | TP4056 Type-C charger (protected) | /tp4056-1a-li-ion-battery-charging-board-type-c-connector-with-current-protection | 16.00 |
| 1 | MT3608 boost module | /mt3608-2a-max-dc-dc-step-up-power-module-booster-power-module | 34.00 |
| 1 | 18650 holder (5×7) | /5-x-7-18650-battery-holder-with-185mm-bore-diameter | 46.00 |
| 1 | Jumper wires (M-F, buy a pack) | /jumper-wire-male-female-connector | 9.00 |
| | **Subtotal ex-GST** | | **1048.00** |
| | **Total incl-GST (×1.18)** | | **1236.64** |

## STILL TO PRICE before buying (no number yet — verify from a 2nd seller / Wayback)
- 18650 Li-ion **cell** (protected) — needed for battery operation.
- Small weatherproof/junction **enclosure**.
- (If long range needed) India-legal **Ra-01H 868 MHz** LoRa instead of the 433 MHz Ra-02.
- Optional: 6 V solar panel; MQ-135; BME280; MLX90614 thermopile.

## OPTIONAL — Build A (camera confirmation node), if also wanted
| Buy | Part | URL | ₹ ex-GST |
|-----|------|-----|---------:|
| 1 | ESP32-CAM-MB + OV2640 + USB programmer | /esp32-cam-mb-wifi-bluetooth-development-board-with-ov2640-camera-micro-usb-connection-to-serial | 421.00 |
| | (reuse MQ2/flame/buzzer/TP4056/holder) | | — |
| | **Camera-node subtotal ex-GST** | | 604.00 |
| | **incl-GST** | | 712.72 |

## ASSUMED ALREADY OWNED (do not re-buy unless missing)
USB cable, 5 V phone adapter, a computer to flash firmware, soldering iron + solder, multimeter, hand tools.

## BUYER NOTES (honest)
- Prices are single-source and GST-exclusive; confirm live price + shipping at checkout (site offers 10%
  prepaid coupon "GET10" — not assumed in totals).
- Buy the **protected** TP4056 variant and a **protected** 18650 cell (SAFETY.md §4).
- Do NOT buy a 433 MHz radio for India deployment; prefer ESP-NOW/Wi-Fi or an 865–867 MHz module (verify
  WPC/licence-exempt rules — SAFETY.md §6).
- This node is an advisory research prototype, NOT a certified fire alarm (Rule 19 / SAFETY.md §1).
