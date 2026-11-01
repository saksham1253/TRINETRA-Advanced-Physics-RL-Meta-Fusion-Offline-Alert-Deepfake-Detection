# ws7_iot/BOM.md — Bill of Materials, low-cost fire-detection IoT node (P6)

STATUS: RESEARCH-ONLY procurement PLAN (Phase P6). No purchase, no build. Target ≤ **₹2000 incl. GST**/node.

## PRICE-VERIFICATION HONESTY (§0.5 / OQ-05)
- All verified prices are from **electronicscomp.com, live 2026-10-09**, shown **EXCLUDING 18% GST**.
  The site's "MRP (inclusive of all taxes)" line equals ex-GST × 1.18 exactly (e.g. MQ2 ₹68 → MRP ₹93.22? 
  no: ₹68×1.18=₹80.24; the ₹93.22 MRP is a higher list price — see note), so **GST-inclusive selling price
  = ex-GST × 1.18** (confirmed on the LoRa page: ₹389 × 1.18 = ₹459.02 = its MRP). Totals here are
  RECOMPUTED from these verified line items, never estimated.
- **LIMITS (not hidden):** single source only (robu.in = Cloudflare 403; amazon.in = JS-rendered; Wayback
  Machine was OFFLINE/503 this session → no second source, no archived prices). No manufacturer datasheet
  opened (alldatasheet/sparkfun/sensirion returned 403/404) → temp/humidity/voltage specs are
  **seller-stated, not datasheet-verified** [spec-seller-stated]. These gaps are carried to the P6 gate.
- Items I could NOT reach a price for are listed as **[UNVERIFIED]** with NO invented number; they are
  excluded from the verified total and shown as a separate pending set.

## Independent re-verification (this agent, 2026-10-09)
MQ2 module **₹68.00 ex-GST** (Product Code EC-0176, "Rs.68.00 (Excluding 18% GST)") ✓ and LoRa Ra-02
**₹389.00 ex-GST** (EC-4955) ✓ fetched directly → match the pricing agent. See Audit #12b.

## ⚠ DESIGN FLAG from verification: LoRa band
The verified Ra-02 (SX1278) page lists **Frequency Range 410–525 MHz** (a 433 MHz module). India's licence-
exempt LoRa ISM band is **865–867 MHz** → the 433 MHz Ra-02 is **not the India-legal choice**. Use the
**Ra-01H (868 MHz)** variant [UNVERIFIED price] OR, preferably for a cheap node, the ESP32's **built-in
Wi-Fi/ESP-NOW (₹0)**. Radio legality flagged for expert/legal review (SAFETY.md §6).

---

## VERIFIED LINE ITEMS (electronicscomp.com, 2026-10-09, prices ex-GST)
| Code | Part | Purpose | Why over alternatives (evidence) | Specs [seller-stated] | ₹ ex-GST | ₹ incl-GST (×1.18) | Verdict |
|------|------|---------|----------------------------------|-----------------------|---------:|-------------------:|---------|
| EC-0176 | MQ2 gas/smoke module (analog+digital) | smoke + LPG/propane/H₂ proxy; "can be used for fire detection" | cheapest smoke proxy; MOX family is the studied low-cost case (lit #10/#11) | 5 V; analog+digital; on-board pot threshold | 68.00 | 80.24 | VERIFIED✓ (re-checked) |
| EC-4955 | LoRa Ra-02 SX1278 | long-range offline uplink (see band flag) | long range −148 dBm; but 433 MHz ≠ India band → prefer ESP-NOW/Ra-01H | SPI, 410–525 MHz, 2.5–3.7 V, −10…+85 °C | 389.00 | 459.02 | VERIFIED✓ (re-checked) |
| — | ESP32-CAM-MB + OV2640 + USB programmer | camera node MCU+cam (Type B) | cheapest MCU+camera combo; INT8 tiny model only (lit #1/#8) | ESP32, OV2640 2 MP, micro-USB prog | 421.00 | 496.78 | VERIFIED |
| — | ESP32-S2-DevKitM-1 | sensor-node MCU + Wi-Fi/ESP-NOW | single-core S2 cheapest Espressif devkit here; Wi-Fi+ADC+GPIO | ESP32-S2, Wi-Fi, USB-OTG | 703.00 | 829.54 | VERIFIED |
| — | ESP32-S3-DevKitC-1-N8 | MCU if on-device TinyML/camera later | S3 has vector ops + more RAM (peak-SRAM is the bind, lit #8) | ESP32-S3, 8 MB flash | 1101.00 | 1299.18 | VERIFIED |
| — | MQ2 bare sensor | (alt to module) | module preferred (has pot + comparator) | — | 69.00 | 81.42 | VERIFIED |
| — | IR flame module (760–1100 nm) | fast flame cue | cheapest flame detector; complements slow gas/heat | digital+analog out | 29.00 | 34.22 | VERIFIED |
| — | KY-026 flame module | (alt flame) | adjustable; equivalent | digital+analog | 41.00 | 48.38 | VERIFIED |
| — | DHT22/AM2302 bare | temp+humidity: rate-of-rise + gas compensation | DHT22 cheapest with usable accuracy; feeds gas comp (lit #15) | −40…+80 °C, 0–100 %RH [seller] | 119.00 | 140.42 | VERIFIED |
| — | DHT22 module | (alt, wired module) | module easier to wire | same | 135.00 | 159.30 | VERIFIED |
| — | Active buzzer module 3.3–5 V | local annunciation (radio-independent) | mandatory cheap local alarm | active, 3.3–5 V | 24.00 | 28.32 | VERIFIED |
| — | TP4056 Type-C charger (with protection) | safe Li-ion charging | protected variant required (SAFETY.md §4) | 1 A, 4.2 V, protection | 16.00 | 18.88 | VERIFIED |
| — | MT3608 2 A boost module | 5 V rail from battery | cheapest standard boost | DC-DC step-up, 2 A max | 34.00 | 40.12 | VERIFIED |
| — | 18650 holder (5×7) | battery mount | standard | holder only (CELL not incl.) | 46.00 | 54.28 | VERIFIED |
| — | Jumper wire M-M / M-F (per 2 pc) | wiring | — | — | 6.40 / 9.00 | 7.55 / 10.62 | VERIFIED |

## UNVERIFIED (needed but no price reachable this session — NO number invented)
18650 **cell** (holder is verified, cell is not); weatherproof/junction **enclosure**; breadboard/zero-PCB;
siren/LED strobe (buzzer is verified); **Ra-01H 868 MHz** LoRa (India-legal variant); MQ-135; BMP280/BME280;
MLX90614 thermopile; AMG8833/MLX90640 thermal array; PMS5003/SDS011 particulate; generic ESP32 DevKit
V1/WROOM-32; 6 V solar panel. → to price via a second seller / Wayback once reachable (gate action).

## ASSUMED-OWNED (NOT in the ₹2000 node budget — listed separately, §P6)
USB cable; 5 V phone charger/adapter; computer to flash firmware; soldering iron + solder; multimeter;
basic hand tools. Standard maker-kit items assumed owned; a separate one-time cost if a buyer lacks them.

## RECOMMENDED BUILDS (totals in HARDWARE_BUDGET.md; computed from verified lines only)
- **Build A — camera node** (verified parts): ESP32-CAM ₹421 + MQ2 module ₹68 + flame IR ₹29 + buzzer ₹24
  + TP4056 ₹16 + holder ₹46 = **₹604 ex-GST = ₹712.72 incl GST** (+ unverified cell + enclosure).
- **Build B — sensor node** (verified parts): ESP32-S2 ₹703 + MQ2 ₹68 + flame ₹29 + DHT22 ₹119 + buzzer ₹24
  + LoRa Ra-02 ₹389 + TP4056 ₹16 + MT3608 ₹34 + holder ₹46 + jumpers ₹9 = **₹1437 ex-GST = ₹1695.66 incl
  GST** (+ unverified cell + enclosure; replace 433 MHz LoRa per band flag).
- Node-count vs sensor-quality (design.md §1): one richer Type-A fusion node beats many single-sensor nodes
  for false-alarm control → spend the budget on fusion, not quantity.
