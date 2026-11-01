# HARDWARE_BUDGET.md — ≤ ₹2000 prototype budget (P6, recomputed from verified listings)

STATUS: RESEARCH-ONLY. No purchase. Totals RECOMPUTED from VERIFIED line items in ws7_iot/BOM.md
(electronicscomp.com, live 2026-10-09, ex-GST; GST-inclusive = ex-GST × 1.18, confirmed on the LoRa page
MRP). **No price is estimated.** Items without a reachable price are shown as a separate UNVERIFIED-PENDING
set and are NOT folded into a single invented total (§0.5 / OQ-05). Single-source caveat applies (robu/
amazon unreadable, Wayback offline → no second source this session).

## Verified-parts recompute (arithmetic shown)
### Build A — camera confirmation node
| Part | ₹ ex-GST |
|------|---------:|
| ESP32-CAM-MB + OV2640 + USB programmer | 421.00 |
| MQ2 gas/smoke module | 68.00 |
| IR flame module (760–1100 nm) | 29.00 |
| Active buzzer module | 24.00 |
| TP4056 charger (protected) | 16.00 |
| 18650 holder | 46.00 |
| **Subtotal ex-GST** | **604.00** |
| **+18% GST** | 108.72 |
| **Total incl-GST** | **712.72** |

### Build B — primary sensor-fusion node (recommended)
| Part | ₹ ex-GST |
|------|---------:|
| ESP32-S2-DevKitM-1 | 703.00 |
| MQ2 gas/smoke module | 68.00 |
| IR flame module | 29.00 |
| DHT22/AM2302 | 119.00 |
| Active buzzer module | 24.00 |
| LoRa Ra-02 (⚠ 433 MHz; replace per band flag) | 389.00 |
| TP4056 charger (protected) | 16.00 |
| MT3608 boost | 34.00 |
| 18650 holder | 46.00 |
| Jumper wires (M-F 2pc) | 9.00 |
| **Subtotal ex-GST** | **1437.00** |
| **+18% GST** | 258.66 |
| **Total incl-GST** | **1695.66** |

## UNVERIFIED-PENDING add-ons (price not reachable this session → NOT in totals above)
18650 **cell**, weatherproof **enclosure**, breadboard/zero-PCB, India-legal **Ra-01H 868 MHz** LoRa (if
long-range needed), optional 6 V solar panel, optional MQ-135/BME280/MLX90614. These must be priced from a
second seller / Wayback before purchase (gate action). Rough slack check (NOT a committed estimate): Build
B verified total is ₹1695.66 incl-GST, leaving **₹304.34** under the ₹2000 cap to absorb a cell + enclosure
— the two typically-cheapest missing items — so a ≤₹2000 node is plausible, to be CONFIRMED once those two
lines are verified. (Build A leaves ₹1287 of headroom, comfortably absorbing them.)

## Contingency & cut-list
- **Contingency:** keep ≥10% (₹200) of the ₹2000 cap unspent for shipping, a spare sensor, and price drift.
  Build B at ₹1695.66 leaves ₹304 → within contingency only if cell+enclosure are cheap; if not, apply cuts.
- **Cut-list (apply in order if over ₹2000 after adding cell+enclosure):**
  1. Drop LoRa Ra-02 (−₹389 ex-GST) → use ESP32 **built-in Wi-Fi/ESP-NOW (₹0)** — also fixes the 433 MHz
     India-band problem. (Biggest single saving; recommended default anyway for a cheap local node.)
  2. Drop MT3608 (−₹34) if powering from USB/3.3 V directly.
  3. Use DHT11 instead of DHT22 (cheaper; lower accuracy — acceptable for rate-of-rise).
  4. Swap ESP32-S2 (₹703) for a generic ESP32 DevKit V1/WROOM-32 (usually <₹703 [UNVERIFIED]).
  With cut #1 alone, Build B drops to ₹1048 ex-GST = **₹1236.64 incl-GST**, leaving ample room for cell +
  enclosure under ₹2000.

## Assumed-owned (NOT costed in the node budget)
USB cable, 5 V adapter, computer for flashing, soldering kit, multimeter, hand tools.

## Bottom line (honest)
From VERIFIED single-source prices alone, a fire-detection node is **feasible under ₹2000 incl-GST**:
Build A (camera) ₹712.72 and Build B (sensor-fusion) ₹1695.66, both before a cell + enclosure. Confirming
the final ≤₹2000 figure requires pricing the 18650 cell + enclosure (and an India-legal radio) from a
second source — the one open procurement action carried to the P6 gate. Nothing here is estimated.

## P13 re-verification note (2026-10-10) — task 8
HONEST STATUS: a FRESH price re-verification could NOT be performed this session — web_search has no API key
(disclosed program-wide) and the P6 price-verification subagent (1204ea37) is finished; I did not re-fetch
live Indian listings. The P6 VERIFIED single-source prices (Build A ₹712.72, Build B ₹1695.66 incl-GST, as
of their P6 capture dates) therefore STAND AS-OF-P6 and are NOT re-confirmed as current.
- Prices change: before buying, RE-PRICE every line at build time from at least two current Indian sources
  (record date + URL), especially the 18650 cell + enclosure + any radio (the carried open procurement
  action) and the ESP32 variant (ESP32-S2 ₹703 vs a generic DevKit, UNVERIFIED-cheaper).
- The ≤₹2000 feasibility conclusion is unchanged in STRUCTURE (cut-list #1 — drop LoRa, use built-in
  ESP-NOW/Wi-Fi — keeps Build B at ₹1236.64 incl-GST with room for cell+enclosure), but the exact total is
  only valid as of the P6 capture and MUST be re-verified at build.
- No price in this file is our own estimate; any figure not re-confirmed this session is explicitly marked
  AS-OF-P6. The build-time re-pricing + the cell/enclosure/India-legal-radio second-source quote remain the
  open procurement actions.
