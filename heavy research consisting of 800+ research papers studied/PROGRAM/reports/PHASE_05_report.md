# PHASE P5 REPORT — Dataset Registry + Compute Budget Plan

Date: 2026-10-07 · Phase: P5 (same authorization as P4: "GO PHASE P4 and if it is done GO PHASE P5 as
well"; plus the standing "if you complete P5 you can start P6") · Status at exit: COMPLETE → AWAITING
GATE (then continuing into P6 per the extended authorization).

---

## 1. Objective (from §P5)
Turn the literature + hazard scope into a concrete, VERIFIED, FREE-ONLY data + compute plan: SOTA scan of
benchmarks/leaderboards per workstream; one living DATASETS.md (all workstreams, Indian-conditions
representation, per-dataset license/access/known-issues/split/verification, QUICK LINKS + COST, free-only
rule); dataset→model matrix + cross-eval plan + registration-needed flags; KAGGLE_BUDGET.md (verified
limits, ~30 GPU-h incl. ≥15% reserve, per-WS allocation, seed policy, cut-list); ≥15 NEW quota reads
(dataset/benchmark/efficiency, Tier-3+); audit 10% of dataset entries. RESEARCH-ONLY; no downloads; no
own-system claims (Rule 16). STOP at the P5 gate.

## 2. What was done (outputs on disk)
| Task | Output | Key result |
|------|--------|------------|
| 1. SOTA scan per WS | PROGRAM/sota/P5_sota_scan.md | benchmarks/leaderboards per WS1–WS8 + 6 selection takeaways |
| 2+3. DATASETS.md | DATASETS.md (D01–D26 + 10 catalogued flood sets) | QUICK LINKS + COST + LICENSE + verification legend; FULL entries |
| 4. Matrix + cross-eval + registration | DATASETS.md (matrix, cross-eval plan, registration section) | dataset→model/WS matrix; 5-step cross-eval; early-access list |
| 5. KAGGLE_BUDGET.md | KAGGLE_BUDGET.md (P5 populated plan) | 25.5 usable GPU-h/wk, per-WS 21 GPU-h, seed policy, cut-list |
| 6. ≥15 NEW quota | PROGRAM/logs/P5_reading_progress.md + PROGRAM/phase_papers/P5_papers.csv + 15 ledger [P5] rows | 15 NEW (FT-PARTIAL ×2 + ABS ×13) |
| 7. Dataset audit | analysis/11_reading_audit.md Audit #11 | 3/26 re-verified (11.5%), 0 material errors, flags intact |
| 8. Report + gate + state | this report, PHASE_05_gate.md, PHASE_STATE/PROGRESS/CHANGELOG, HANDOFF | — |
| (support) verification mirror | PROGRAM/logs/P5_dataset_verification.md | per-dataset fetch verdicts [V]/[V*]/[D] |

## 3. Headline results
- **26 datasets catalogued, VERIFIED free-only.** 13 fully verified on direct authoritative fetch [V],
  5 exist-with-one-fact-open [V*], 8 discovery-only [D]. NO paid dataset is selected (free-only held).
- **Indian-conditions coverage is real but thin and partly unverified.** The one fully-verified
  India-specific set is D22 India Flood Inventory–Impacts (IIT-Delhi+IMD, CC BY 4.0, 1967–2023). GLOF/
  landslide in-region data (D15 HMAGLOFDB, D18 LMHLD-Gorkha, D23 Kerala, D24 Bhuvan, D25 INDOFLOODS) is
  valuable but mostly [D] discovery-only → direct portal fetch owed in P6/P7 before building.
- **Core sensor backbone is all free + global** (Sentinel-1/2, GPM IMERG, SMAP, ERA5-Land CC-BY, MODIS,
  ITS_LIVE) — the physical substrate of TRINETRA is fully available at zero cost (free registration).
- **Compute is feasible under ~25.5 usable GPU-h/week IFF PEFT-first + adapt-not-pretrain + CPU-for-
  preprocessing + cheap-many-seed baselines.** Literature (2604.16663 PEFT −95%; 2512.02055 tuned U-Net
  beats GFM on recall; 2605.28174 small-corpus GFM) says we should not need from-scratch FM training.
- **15 NEW quota reads** confirm the evaluation frontier (worst-group/leakage-safe splits/corruption/
  cost-loss) that our P4 design defaults (DC-01/02/05) already target.

## 4. The 15 NEW quota reads
Flood (5): GEOID-Flood 2608.02315, UFO 2604.23066, FloodsNet/TerraMind 2512.02055, Explainable-SAR-flood
2606.16302, (+ GEOID Table-1 census). Landslide (2): GDCLD-benchmark 2604.16663, LMHLD 2502.19866.
InSAR/glacier (3): Thalia 2505.17782, CryoNet 2605.21527, coherence-from-GRD 2606.07374. Nowcasting (2):
PG-FMM 2609.37487, JWS 2610.12189. Benchmark-methodology (2): FairRSFM 2610.05790 (FT-PARTIAL),
label-noise benchmark 2603.00604. Crisis-NLP (1): HUMAID-NER 2609.16964. Efficiency/missing-modality:
FLORO 2605.28174. Depth: 2 FT-PARTIAL + 13 ABS (Tier-3+ is appropriate for a dataset/benchmark phase per
§0.9; the dataset table/abstract is the load-bearing content). Running body-level NEW reads: 93.

## 5. Honest limitations (§0.5)
- Kaggle limit numbers could NOT be freshly fetched (JS-rendered docs) → §1 of KAGGLE_BUDGET.md is a
  verify-at-session-start estimate with a safety reserve.
- `web_search` had no API key this session → dataset discovery used DuckDuckGo-HTML as a proxy;
  everything load-bearing was confirmed by direct `web_fetch` where possible, and UNVERIFIED items are
  flagged, not hidden.
- 8 datasets are [D] discovery-only (incl. the most India-specific landslide inventories) → the first
  action in P6/P7 is to fetch Bhuvan/NRSC + the Indian Zenodo pages directly and confirm license/size.
- ABS-level reads dominate the P5 quota — honest and expected for a cataloguing phase; they are reported
  separately from the body-level Tier-2+ trajectory (no padding of the foundation count).

## 6. Acceptance check (§P5)
- SOTA scan FIRST — ✅ (P5_sota_scan.md). · One living DATASETS.md, free-only, verified, Indian-conditions
  noted — ✅. · Per-dataset license/access/known-issues/split/verification — ✅. · Dataset→model matrix +
  cross-eval + registration flags — ✅. · KAGGLE_BUDGET.md with reserve + per-WS + seed policy + cut-list —
  ✅. · ≥15 NEW quota — ✅ (15). · 10% dataset audit — ✅ (Audit #11). · No downloads, no own-system claims —
  ✅.

## 7. Carried / deferred to later phases
- Direct fetch + license confirmation of D11 GLOFNet, D15 HMAGLOFDB, D20 GDCLD, D21 Thalia, D23/D24/D25
  Indian inventories (P6/P7, before any build).
- Confirm Kaggle live quota (first build session).
- Indian-language/code-mixed crisis-media GAP (WS2) — research-note risk.
- P14Z dataset needs (OmniRS5M etc.) revisited at P14Z.

## 8. Exit
SOTA ✅ · registry ✅ · budget ✅ · quota ✅ · audit ✅ · report ✅ · gate next → then CONTINUE into P6
(IoT/BOM/safety) per the extended authorization; STOP at the P6 gate awaiting "GO PHASE P7".
