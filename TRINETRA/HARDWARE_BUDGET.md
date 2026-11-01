# HARDWARE_BUDGET — IoT node cost plan (MASTER_PROMPT §0.10; detailed in P6)
# RESEARCH-ONLY: procurement RESEARCH only. No purchases in this program.

## Finding after live-price survey (2026-10-31)

The old **≤ ₹2,000 per installed node target is infeasible**. ESP32 DevKitC (₹748) + 868 MHz LoRa (₹1,011) already total ₹1,759 before sensors, solar, enclosure, wiring, GST/shipping or field installation.

Revised planning rates:

- rugged installed slope node: ~₹8,000;
- shared industrial rain station: ~₹40,000;
- edge gateway: ~₹35,000;
- priority-corridor network (500 slope nodes, 50 rain stations, 95 gateways, redundant servers/integration): ₹1.5–3.0 crore first year.

Full survey, URLs, fiscal baseline and savings scenarios: `docs/27_UTTARAKHAND_IOT_EWS_COST_BENEFIT.md`.

## Current status (2026-10-31)

- ElectronicsComp listings were reachable and dated prices were captured for MCU, LoRa, IMU, soil moisture, BME280, solar panel/manager, battery, industrial rain gauge and Raspberry Pi gateway.
- Enclosure, UPS, antenna/civil works, production server/security and installation remain procurement allowances, not verified quotes.
- Before purchase: obtain a GeM/tender quotation and two vendor quotations per line.

## BOM skeleton (components only; ₹ to be filled with [LV] verified prices in P6)
| Node | Component | Qty | Unit ₹ [EST] | Source (to verify) | Tag |
|------|-----------|-----|--------------|--------------------|-----|
| Ground IoT | MCU (ESP32 DevKitC) | 1 | 748 | ElectronicsComp, 2026-10-31 | [LV] |
| Ground IoT | LoRa module 868 MHz E32 | 1 | 1,011 | ElectronicsComp, 2026-10-31 | [LV] |
| Ground IoT | MPU6050 IMU | 1 | 122 | ElectronicsComp, 2026-10-31 | [LV] |
| Ground IoT | Capacitive soil moisture | 1 | 61 | ElectronicsComp, 2026-10-31 | [LV] |
| Ground IoT | BME280 | 1 | 295 | ElectronicsComp, 2026-10-31 | [LV] |
| Ground IoT | 6V/5W solar panel | 1 | 899 | ElectronicsComp, 2026-10-31 | [LV] |
| Ground IoT | 6000 mAh LiFePO4 + protection | 1 | 312 | ElectronicsComp, 2026-10-31 | [LV] |
| Ground IoT | Solar power manager | 1 | 889 | ElectronicsComp, 2026-10-31 | [LV] |
| Ground IoT | Enclosure, antenna, wiring, installation | 1 | 3,500 | procurement allowance | [EST] |
| Shared rain station | Industrial tipping-bucket gauge | 1 | 31,499 | ElectronicsComp, 2026-10-31 | [LV] |
| Gateway | Raspberry Pi 5 8 GB + PSU | 1 | 20,498 | ElectronicsComp, 2026-10-31 | [LV] |
| Gateway | LoRa, storage, UPS, enclosure, installation | 1 | 14,500 | procurement allowance | [EST] |

## Rule

- Retail listings prove the ₹2,000 gate is infeasible; they are not tender prices.
- Rain gauge is shared across a local cluster rather than repeated on each slope.
- No benefit or savings claim until a shadow pilot records uptime, warning lead time, operator action and covered-vs-comparison losses.
