# PHASE P5 — GATE MESSAGE

Phase: P5 (Dataset Registry + Compute Budget Plan) · Date: 2026-10-07 · Status: COMPLETE, all 8 tasks
done, exit audit clean. Authorization: the P4/P5 authorization plus your standing "if you complete phase
P5 you can start with P6 because I am going to sleep now" → I am NOT stopping; I continue into P6 and will
STOP at the P6 gate awaiting "GO PHASE P7". This message is informational.

---

## What P5 produced
- `PROGRAM/sota/P5_sota_scan.md` — benchmarks/leaderboards per workstream + 6 dataset-selection takeaways.
- `DATASETS.md` — the one living registry: 26 datasets (D01–D26) + 10 further flood sets catalogued;
  QUICK LINKS with COST + LICENSE + a verification legend ([V]/[V*]/[D]); full per-dataset entries;
  dataset→model/workstream matrix; 5-step cross-evaluation plan; registration/early-access list.
- `KAGGLE_BUDGET.md` — populated plan: 25.5 usable GPU-h/week (≥15% reserve), per-WS allocation (21
  GPU-h), seed/rigor policy, scheduling/checkpoint rules, cut-list.
- 15 NEW quota reads (dataset/benchmark/efficiency) → ledger [P5] rows + `P5_reading_progress.md` +
  `PROGRAM/phase_papers/P5_papers.csv`.
- `analysis/11_reading_audit.md` Audit #11 — 3/26 (11.5%) dataset entries re-verified, 0 material errors.
- `PROGRAM/logs/P5_dataset_verification.md` — per-dataset fetch verdicts.
- Report: `PROGRAM/reports/PHASE_05_report.md`.

## The things you should know (honest flags, §0.5)
1. **Free-only held.** Every selected dataset is free (several need only free registration). No paid set
   is selected. The core sensor backbone (Sentinel-1/2, GPM IMERG, SMAP, ERA5-Land, MODIS, ITS_LIVE) is
   fully free and global.
2. **Indian-conditions data is real but thin + partly unverified.** The one FULLY-verified India set is
   the India Flood Inventory–Impacts (IIT-Delhi+IMD, CC BY 4.0). The most valuable in-region landslide/
   GLOF inventories (HMAGLOFDB, Bhuvan/NRSC Uttarakhand-2013/J&K/Sikkim/Wayanad, Kerala-2018, INDOFLOODS)
   are discovery-only — I will fetch their portals directly in P6/P7 and confirm license before building.
3. **Kaggle numbers are verify-at-session-start.** Kaggle's docs are JS-rendered and didn't yield text
   via fetch; the budget uses the widely-published ~30 GPU-h/week with a safety reserve, flagged to
   re-confirm from your account quota panel at the first build session.
4. **`web_search` had no API key this session** → discovery used a DuckDuckGo-HTML proxy; all load-bearing
   facts were confirmed by direct page fetch where possible, and the rest are marked UNVERIFIED.

## EARLY-ACTION items you could start now (optional, while I continue)
- Create free accounts: **NASA Earthdata Login**, **Copernicus Data Space Ecosystem**, **Copernicus CDS**
  (+ CDS API key). These gate IMERG/SMAP/MODIS/ITS_LIVE and Sentinel/ERA5-Land downloads.
- The one potentially-slow item: **Bhuvan/NRSC-ISRO** access for the Indian landslide inventories — if a
  government request is needed, starting it early de-risks the build.

## STOP / CONTINUE
Per your "start P6" instruction I continue directly into **P6 (WS7a IoT research — component selection,
≤₹2,000 BOM incl. GST, safety protocol; research + selection only, no building)**. I will surface the
verified BOM and the hazardous-stimulus safety protocol at the P6 gate, then STOP awaiting
**"GO PHASE P7"**.
