# PHASE P6 REPORT — IoT fire-detection node: SOTA, BOM, budget, safety, design

Phase: P6 (WS7a — low-cost multi-sensor + camera fire-detection IoT node). Mode: RESEARCH-ONLY (no code,
no firmware, no hardware built, no purchase). Date: 2026-10-07…2026-10-09.

## Task completion (MASTER_PROMPT L401–460)
| # | Task | Status | Evidence |
|---|------|--------|----------|
| 1 | SOTA scan (low-cost multi-sensor + TinyML fire detection) | ✅ | PROGRAM/sota/P6_sota_scan.md |
| 2 | Read via engine; add datasheets/standards to ledger (non-quota) | ◑ partial | ledger rows [P6]; datasheet fetches BLOCKED (403/404) → logged as gap, carried to backlog |
| 3 | On-device physics rules (rate-of-rise, fusion, time-constants) as hypotheses | ✅ | ws7_iot/design.md §3 + §7 |
| 4 | Open multi-sensor fire + nuisance datasets + baselines | ✅ | DATASETS.md D27–D30; literature_map "datasets found" |
| 5 | Component selection + BOM ≤₹2000 (verified Indian prices) | ✅ (within single-source limit) | ws7_iot/BOM.md, HARDWARE_BUDGET.md, SHOPPING_LIST.md |
| 6 | BOM.md + HARDWARE_BUDGET.md (recomputed, cut-list, assumed-owned) | ✅ | ws7_iot/BOM.md, ws7_iot/HARDWARE_BUDGET.md |
| 7 | SAFETY.md safe-stimulus protocol | ✅ | ws7_iot/SAFETY.md |
| 8 | design.md preliminary design + acceptance criteria | ✅ | ws7_iot/design.md |
| Q | ≥15 NEW quota reads + SOTA scan | ✅ 20 NEW | literature_map.md, P6_papers.csv, P6_reading_progress.md |
| A | Exit audit | ✅ | Audit #12 (reading) + #12b (BOM price) in analysis/11_reading_audit.md |

## Headline results (all SOURCE-REPORTED or VERIFIED-listing; none are our own measurements — Rule 16)
- **A ≤₹2000 fire-detection node is feasible from VERIFIED prices.** Build A (ESP32-CAM camera node)
  = ₹712.72 incl-GST; Build B (ESP32-S2 sensor-fusion node) = ₹1695.66 incl-GST — both before an 18650
  cell + enclosure (still unverified). With the LoRa→ESP-NOW cut, Build B drops to ₹1236.64 incl-GST,
  leaving ample room. Prices: electronicscomp.com, live 2026-10-09, ex-GST ×1.18 (GST math confirmed via
  the LoRa MRP line). Independently re-verified MQ2 ₹68 + LoRa ₹389 (Audit #12b).
- **Design direction (from 20 NEW reads):** two-tier wake-on-event (cheap always-on gas/temp/flame gate
  the power-hungry camera — duty cycle, not the CNN, dominates energy, ETH node 2608.23192); optimise any
  on-ESP32 model for **peak activation RAM** not params (ENAS 2609.30272); gas as **baseline-normalised
  multi-lag deltas** with temp/humidity fed in (LDAC-Net 2608.25646, 2604.21527); **slow** drift
  compensation so it can't mask a real rise (2507.17071); multi-class smoke so steam/exhaust ≠ alarm
  (2208.00210); **16-byte HMAC + monotonic nonce** auth, no unauthenticated endpoints (DCP 2605.26159);
  classify on-device, send a few-byte uplink (2511.00348/2605.19793); India calibration must survive
  season/site/unit, outliers normal (RESPIRE 2511.19810).
- **Material verification finding:** the cheap LoRa Ra-02 is **433 MHz** → NOT India's 865–867 MHz band;
  defaulted the design to ESP-NOW/Wi-Fi (₹0) and flagged an India-legal 868 MHz radio as an option.

## Honest limitations (§0.5)
- **Prices: single source** (robu.in = Cloudflare 403; amazon.in = JS-rendered; **Wayback Machine was
  offline/503 all session**) → no second source and no archived prices. Final ≤₹2000 figure needs the
  18650 cell + enclosure (+ India-legal radio) priced from a 2nd source — carried to the gate.
- **Specs seller-stated, not datasheet-verified** (datasheet hosts returned 403/404). Task-2 datasheet
  ingestion is therefore partial.
- **Reading: arXiv-only, mostly abstract** (1 FT-PARTIAL + 19 ABS); `web_search` had no API key →
  MDPI/IEEE/standards unreachable, leaving 4 topics uncovered (rate-of-rise heat-detector engineering,
  ESP32-CAM FPS, smoke optical-extinction physics, MQ datasheet characterization) → backlog.
- No own-system performance claim is made; acceptance criteria (design.md §8) are PROCESS targets to be
  met at build time, not results.

## Acceptance check
All P6 deliverables exist on disk; quota (20 ≥ 15) met and audited; non-destruction (§0.3) honoured
(only program-era files I authored were updated; legacy docs untouched); hard-honesty/no-padding (§0.5)
and Rule 16 observed. P6 is COMPLETE → STOP at the gate.
