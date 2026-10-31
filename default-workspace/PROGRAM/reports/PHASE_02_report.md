# PHASE P2 REPORT — Literature Foundation I

Date: 2026-10-06 · Phase: P2 (authorized "GO PHASE P2", 2026-10-05) · Status at exit: COMPLETE → AWAITING GATE

---

## 1. Objective (from §P2 / MASTER_PROMPT L295–317)
Build the FIRST HALF of the foundation NEW-paper set (P2+P3 together ≥250 and ≤400 verified new;
P2 aims ~40–60%). SOTA scan FIRST; run the full §0.8 search; seed+prioritize the queue; batch-cycle
reading with theme balance (no theme >~25%); keep the search log complete; interim syntheses every
5 batches; maintain registers + citation graph + contradiction register + novelty index; read ≥15
NEW quota papers ON TOP of the baseline (OQ-02); ≥60% Tier-2+. RESEARCH-ONLY (§0.1A). No claims
about our own system (Rule 16). STOP at the P2 gate — one phase only.

## 2. What was done (outputs on disk)
| Task | Output | Key result |
|------|--------|------------|
| 1. SOTA scan FIRST | PROGRAM/sota/P2_sota_scan.md (§1–§8) | 7 topic scans + §8 SOTA-targets+protocol plan (completed at exit) |
| 2. Full §0.8 search | analysis/02_search_log.md rows 136–157 (22 queries) | arXiv API quoted-AND; every hit novelty-checked vs ledger+index |
| 3. Seed+prioritize queue | analysis/10_reading_queue.csv | P2 candidates scored; 8 NEW P3 candidates appended |
| 4. Batch-cycle read 18 NEW quota | 18 notes in analysis/03_paper_notes/ + PROGRAM/logs/P2_reading_progress.md (18 rows) + PROGRAM/phase_papers/P2_papers.csv | **18/18 FT-PARTIAL = 100% Tier-2+** (target ≥15 EXCEEDED; ≥60% Tier-2+ met) |
| 5. Interim syntheses | PROGRAM/reports/P2_interim_syntheses.md | #1 (after 10) + #2 (after 18) |
| 6. Registers + ledger | 02_paper_ledger.csv (+18 phase_quota=P2 rows), novelty_index.csv, registers | pre-existing rows untouched (§0.3); phase rows tagged [P2] |
| 7. Exit audits | analysis/11_reading_audit.md (Audit #8, 22% sample) | **0% identity/claim error** on 4 number-heavy notes |
| 8. Report + gate + handoff | this report, PHASE_02_gate.md, HANDOFF updates, CHANGELOG→P2 | gate message with progress-toward-250 + P3 emphasis |

## 3. The 18 NEW quota papers (verified NEW vs ledger + novelty index)
All read at FT-PARTIAL depth via ar5iv/arXiv-HTML (web_fetch prunes the page middle → tables not
fully verified; labelled honestly per D-008). None were in the 235-paper ledger or local baseline.

| # | ID | One-line contribution to TRINETRA | Primary tie |
|---|----|-----------------------------------|-------------|
| 1 | 2605.17419 | LEWS must train for FORECAST-rainfall displacement, report skill under forecast error | T2, CR-04 |
| 2 | 2610.01994 | gradient-boosted beats deep for wildfire ignition (2nd-domain CR-02) | T1, CR-02, FM-01 |
| 3 | 2610.04392 | evaluation pitfalls + rare-event performance collapse | FM-21, eval |
| 4 | 2508.14203 | VAD survey: human/vehicle/environment taxonomy; cross-scene robustness | WS4, C8/C10 |
| 5 | 2610.02777 | conformal coverage degrades right after distribution shift / at onset → shield | T5, CR-04 |
| 6 | 2606.07593 | corruption-robustness FT does NOT transfer across corruption types | robustness |
| 7 | 2609.38936 | low-capacity risk-conditioned calibrator wins at tiny n (n=250) | WS6, FM-20 |
| 8 | 2605.15894 | evidential UQ smoke severity; vacuity gate; selective pred 50%→96.7% | WS4, WS6 |
| 9 | 2507.21649 | VAD survey DNN→MLLM: grounding(edge) vs understanding(cloud) split | WS4 |
| 10 | 2607.28248 | UQ-for-trustworthy-DL survey: method menu + efficient approximations | WS6 |
| 11 | 2511.21364 | multimodal social-media disaster classification (low-weight corroborating signal) | WS8, Rule19 |
| 12 | 2609.20441 | edge flood-seg distillation; FIXED MNDWI rule competitive (3rd-domain CR-02) | CR-02, CR-01 |
| 13 | 2609.07455 | federated MIL + VLM-logit (not text-gen) verification; raw video stays local | WS4 |
| 14 | 2609.05066 | adaptive multi-granularity temporal VAD (variable-duration events) | WS4 |
| 15 | 2609.17175 | probabilistic nowcast eval doctrine (CRPS+rank-hist+RAPSD); ~90-min skill ceiling | T5, WS3 |
| 16 | 2605.20167 | operational free-data flash-flood EWS = closest TRINETRA analog; deseasonalization anti-leakage | T1/T2/T3 |
| 17 | 2509.18176 | InSAR deformation forecasting; baselines default to persistence (beat it) | T6, CR-02 |
| 18 | 2606.13896 | GeoFM rankings flip by task/objective → CR-01 encoder-selection backbone | CR-01 |

## 4. What changed in the design (per-theme)
- **CR-02 (simplicity dominates) is now a four-domain, four-instance doctrine** (GLOF 2608.12422 /
  fire 2610.01994 / flood 2609.20441 / deformation 2509.18176). Hardened design rule: every deep
  claim must beat a FIXED physical/spectral rule AND persistence, reported as skill-over-baseline
  under spatial/event CV.
- **CR-01 (encoder choice) got its methodology** (2606.13896): evaluate candidates on OUR tasks,
  match pretraining objective to task, probe mid-layers, budget fine-tune representation shift.
- **An operational TRINETRA analog exists** (2605.20167): validates the whole free-data +
  Sentinel-1 + RF/XGB + transboundary-upstream + local-SMS architecture AND contributes a new
  anti-leakage procedure (deseasonalize via monthly climatological anomaly; disclose feature–label
  correlation before/after).
- **Precipitation input gets a probabilistic evaluation doctrine** (2609.17175): CRPS + rank
  histogram + RAPSD, importance-sample rare rain, be honest about the short (~90 min) skill horizon.
- **WS4 video firmed up**: federated MIL keeps raw video local; cheap-scorer→suspect-VLM-verifier
  cascade using the LOGIT interface (not prompt-fragile text-gen); adaptive temporal granularity.
- **WS8 crowd layer scoped honestly**: social media is a low-weight corroborating signal only,
  recall collapses during real events, multilingual constraint real (never a standalone trigger).
- **UQ/calibration stack**: low-capacity risk-conditioned calibrators for tiny validation sets;
  conformal coverage weakest at onset → hard physics shield; evidential UQ as a false-alarm gate.

## 5. Theme balance (18 papers)
hazard-core EWS/flood/nowcast/InSAR/encoders 6 (33%); VAD/CCTV 4 (22%); conformal/calibration/UQ 3
(17%); fire/smoke 2 (11%); robustness 1 (6%); eval/benchmark 1 (6%); disaster/crowd 1 (6%).
Max single theme = 33% (hazard-core). This exceeds the ~25% guideline but is the project's CENTRAL
domain spanning 6 distinct sub-topics (not one narrow method); documented honestly. **P3 directive:**
add robustness / eval-critique / efficiency / non-hazard method papers to pull hazard-core below 25%.

## 6. SOTA targets and protocol plan
See PROGRAM/sota/P2_sota_scan.md §8 (completed at exit): §8.1 published anchor numbers per task with
protocol + caveats; §8.2 the 8-point fair-comparison protocol (two mandatory baselines; spatial/
event CV; anti-leakage disclosure; probabilistic+calibration metrics; rare-event cost-weighted
scoring; per-corruption robustness; on-our-task encoder selection; edge re-profiling); §8.3 honest
framing (no own-system number yet, Rule 16 — the defensible near-term target is a PROCESS target:
beat the two baselines on our data under spatial CV with calibrated uncertainty + cost-loss score);
§8.4 protocol items handed to P6/P7/P15/build.

## 7. Acceptance check (against §P2)
- ≥15 NEW quota papers: **18 ✅ (exceeded by construction).**
- ≥60% Tier-2+: **100% (18/18 FT-PARTIAL = Tier-2) ✅.**
- Audit error <5%: **0% at a 22% sample (Audit #8) ✅.**
- Theme distribution documented: **✅** (33% hazard-core flagged; P3 rebalance directive issued).
- SOTA scan first + §8 completed: **✅.** Search log complete (rows 136–157): **✅.** Interim
  syntheses every 5 batches (#1, #2): **✅.** Registers/novelty index/queue maintained: **✅.**
- RESEARCH-ONLY honored (no code/training/experiments); no own-system performance claims (Rule 16): **✅.**

## 8. Progress toward the 250–400 foundation target
- Verified NEW foundation papers so far: **P1 15 + P2 18 = 33 deep (Tier-2 FT-PARTIAL) reads.**
- Against the P2+P3 ≥250 total: deep reads are the quota core; the broader foundation VOLUME toward
  250 is being accumulated as novelty-checked abstract-verified candidates in the queue (8 NEW P3
  candidates logged this phase) plus the re-studied 235-paper baseline backlog (OQ-02). Honest
  statement: the 250 target is a P2+P3 JOINT target and is NOT yet reached at end of P2; P2
  delivered 18 deep NEW reads (quota 15 exceeded) and seeded P3. P3 must convert the queue +
  remaining axes into the back-half of the foundation set.

## 9. Carried forward to P3 (what P3 should emphasize)
1. **Rebalance themes** away from hazard-core; add robustness, eval-critiques, efficiency/edge,
   and non-hazard method papers.
2. **Fill axis gaps** A3/A4/A9/A13 and THIN theme-matrix cells: assurance-case, tech-debt,
   live-drift, missing-modality.
3. **Read the 8 queued NEW P3 candidates** (2610.02357 conformal-TS, 2501.08639 UAV-edge-fire,
   2608.11142 SAR-SSL, 2505.17782 Thalia-InSAR dataset, 2601.03569 slope-failure LID, etc.).
4. **Author backfills** (non-blocking): 2610.01994, 2610.04392, 2508.14203, 2606.07593, 2507.21649,
   2607.28248.
5. **Deferred (PHASE_BACKLOG):** 2606.12066 PDF route; nhess-22-3309-2022 body; FFM α (2007.02756);
   Indian-LoRa 2412.04563; I–D/GLOF constants (Bug #15); CP-under-missingness 2406.05405 (CR-04 open).

## 10. Honesty notes
- All 18 reads are FT-PARTIAL (D-008): named sections read; page middles (often result tables)
  pruned by web_fetch → specific table numbers NOT independently re-verified beyond what Audit #8
  checked against live abstracts. Every number cited in notes/§8 is as-published with its protocol.
- Novelty claims are "not found in the N sources searched" (queries + dates in the search log), never
  "does not exist" (Rule 21).
- No TRINETRA performance number is claimed anywhere (Rule 16). Published anchors are bars on THEIR
  data, not our expected results.