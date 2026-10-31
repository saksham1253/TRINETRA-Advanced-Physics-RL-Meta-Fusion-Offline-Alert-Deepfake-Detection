# HARDWARE_BUDGET — IoT node cost plan (MASTER_PROMPT §0.10; detailed in P6)
# RESEARCH-ONLY: procurement RESEARCH only. No purchases in this program.

## Hard constraint
- ≤ ₹2000 per node, INCLUSIVE of GST + shipping, with ~10% contingency.
- Prices must come from VERIFIED live Indian listings with the date seen.

## Current status (2026-10-05, P0)
- Indian supplier pages returned HTTP 403 (Cloudflare) this session → ALL ₹ figures are
  [EST] (estimates), NOT verified listings. The ≤₹2000 gate CANNOT be enforced yet.
- Hard verification deferred to P6 against ≥2 live listings per component (OQ-05).

## BOM skeleton (components only; ₹ to be filled with [LV] verified prices in P6)
| Node | Component | Qty | Unit ₹ [EST] | Source (to verify) | Tag |
|------|-----------|-----|--------------|--------------------|-----|
| Ground IoT | MCU (ESP32-class) | 1 | TBD | — | [EST] |
| Ground IoT | LoRa module (IN865–867 MHz) | 1 | TBD | — | [EST] |
| Ground IoT | Tilt / IMU sensor | 1 | TBD | — | [EST] |
| Ground IoT | Soil-moisture sensor | 1 | TBD | — | [EST] |
| Ground IoT | Rain gauge (tipping bucket) | 1 | TBD | — | [EST] |
| Ground IoT | Piezometer (water level) | 1 | TBD | — | [EST] |
| Ground IoT | Solar panel + battery + charge ctrl | 1 | TBD | — | [EST] |
| Ground IoT | Enclosure (IP-rated) + misc | 1 | TBD | — | [EST] |
| River-Eye | Camera module | 1 | TBD | — | [EST] |

## Rule
- A node's BOM total is INFEASIBLE-to-confirm until every line is [LV] from a dated listing.
- If total exceeds ₹2000, record it and propose cheaper substitutions with evidence.
