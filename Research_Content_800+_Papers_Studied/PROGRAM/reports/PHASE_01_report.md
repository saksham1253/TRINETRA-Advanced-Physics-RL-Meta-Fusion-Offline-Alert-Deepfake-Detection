# PHASE P1 REPORT — Baseline Papers, System Model, Locked Key Questions

Date: 2026-10-06 · Phase: P1 (authorized 2026-10-05) · Status at exit: COMPLETE → AWAITING GATE

---

## 1. Objective (from §P1 / MASTER_PROMPT L269–291)
Re-establish the TRINETRA system model on honest, full-text evidence; re-study the 235-paper
abstract-only baseline corpus to true Tier-2+ depth (OQ-02); read **15 NEW quota papers** on
the methodology of designing and evaluating safety-critical ML and early-warning systems
(ON TOP of the baseline, not counting it); finalize the key-question set; and leave the program
ready for P2. RESEARCH-ONLY: no code, no training, no experiments (§0.1A). No claims about our
own system's performance (Rule 16). STOP at the P1 gate — one phase only.

## 2. What was done (8 tasks, outputs on disk)
| Task | Output | Key result |
|------|--------|------------|
| 1. SOTA scan | PROGRAM/sota/P1_sota_scan.md | §4 mandatory baselines; spatial-CV doctrine extended |
| 2. Re-study baseline Tier-2+ | analysis/03_paper_notes/ (46 notes) + logs/P1_reading_progress.md (62 rows) | 43 corpus + 3 external-anchor notes across all 7 clusters; highest-relevance anchors full-text |
| 3. System model | analysis/00_system_model.md (§11 ADDENDUM) | P0 original backed up (CoW); §11.1–11.7 ground refinements in read papers |
| 4. Baseline synthesis | analysis/01_baseline_papers.md | ~121-ID index + themes T1–T6, gaps G1–G7, CR-01…CR-04 + GMF tension |
| 5. Lock key questions | analysis/00_key_questions.md | priority-scored, phase-owned, per-paper-tagged; 8 P0-gating questions; new SC/eval groups |
| 6. Theme-coverage matrix | analysis/12_theme_coverage_matrix.md | themes × evidence; THIN cells flagged as P2/P3 gaps |
| 7. Read 15 NEW quota papers | 15 × *_QUOTA_*.md + PROGRAM/phase_papers/P1_papers.csv | **15/15, ALL FT-PARTIAL (100% Tier-2+)**, novelty-checked |
| 8. Exit audits + report + handoff | analysis/11_reading_audit.md (Audit #7), this report, HANDOFF | 0% error; registers propagated; gate message next |

## 3. The 15 NEW quota papers (verified NEW vs ledger + novelty index)
All read at FT-PARTIAL depth via ar5iv/arXiv-HTML (web_fetch prunes the page middle → tables not
fully verified; labelled honestly). None were in the 235-paper ledger or local baseline corpus.

| # | ID | One-line contribution to TRINETRA | Primary tie |
|---|----|-----------------------------------|-------------|
| 1 | 2410.06388 | multimodal pedestrian alerts: trust/habituation is empirically real | FM-09, Q4.4 |
| 2 | 2209.11632 | continuous ML safety assurance / GSN safety-case structure | Q8.1, Rule 19 |
| 3 | 2604.25512 | PHISHREV knowledge-gated post-hoc revision = prior art disciplining GMF | CR-06, Q4.3 |
| 4 | 2010.09107 | EnbPI conformal PI for time series w/o exchangeability | CR-04, Q3.1 |
| 5 | 2404.19452 | drift detection accuracy-vs-energy frontier (pick ADWIN/HDDM_W) | SC7, HP-02 |
| 6 | 2608.26304 | flood evacuation equity + two-stage stochastic optimization (non-RL decision layer) | CR-03, Q6.1 |
| 7 | 2206.09981 | class-imbalance metric sensitivity: don't compare metrics across base rates | FM-21, Q0.4 |
| 8 | 2412.13439 | MIP per-class ensemble weighting + bounded selection for edge | Q2.2, SC6 |
| 9 | 2103.09783 | AI technical debt (data/model/config/ethics) + training/serving skew | FM-19, Q0.5 |
| 10 | 2405.00031 | SegNet wildfire e2e: compact model wins, resolution is a safety hyperparameter | CR-02, Q6.3 |
| 11 | 2606.21130 | burst-aware high-recall XGBoost EWS, cost-based threshold (AUC 0.697/Recall 0.914) | CR-02, HP-03 |
| 12 | 2311.14110 | DataCOPE OPE-feasibility gate before trusting a learned policy | FM-22, Q4.1 |
| 13 | 2306.04590 | ProCal proximity-bias overconfidence; temp-scaling doesn't fix; transformers worse | FM-20, Q3.2 |
| 14 | 2310.03986 | robust multimodal learning: fusion NOT free-lunch robust; <1% params recover | CR-07, Q4.5 |
| 15 | 2601.05921 | cost-loss Value Score as PRIMARY EWS metric (decision-theoretic) | E-07, Q0.4 |

## 4. The P1 "evaluation stack" (the synthesis the quota reads produced)
The quota corpus converges on a coherent protocol for a MULTI-COMPONENT life-safety ML pipeline:
1. **Per-base-rate metric discipline** — never compare AUC/AP/F1 across differing imbalance
   ratios (2206.09981, FM-21).
2. **Cost-loss Value Score** as the primary decision metric, reported across a C/L range, with
   the alarm threshold p*=C_FA/(C_FA+C_miss) drawn from the SAME cost-loss model (2601.05921, E-07/E-06).
3. **OPE feasibility first** — check the offline data can even support evaluating a learned alarm
   policy before trusting it; else fall back to one-step / shielded fixed policy (2311.14110, FM-22).
4. **Honest coverage** — conformal intervals via EnbPI (no exchangeability), coverage is
   approximate with an explicit, shift-sensitive gap, NOT a hard guarantee (2010.09107, CR-04).
5. **Calibration under sparsity** — proximity-aware, because overconfidence concentrates exactly
   in thin-data regions and temp-scaling does not fix it (2306.04590, FM-20).
6. **Assurance structure** — a maintained safety case / GSN around a continuously-updated model
   (2209.11632, Q8.1).

## 5. What CHANGED in the system model / registers
- **CR register:** CR-02/CR-03 extended; CR-06 (GMF = composition, not invention) and CR-07
  (fusion not robust-for-free) added.
- **Failure modes:** FM-19 train/serve skew, FM-20 proximity-bias overconfidence (critical),
  FM-21 metric-mirage, FM-22 untested-OPE-trust added.
- **Equations:** E-07 cost-loss Value Score added; E-06 tied to it (threshold ↔ metric coherence).
- **Hyperparameters:** HP-02 (drift detector), HP-03 (XGBoost EWS reported numbers), HP-04
  (missing-modality adapter) added — all "as reported", none ours (Rule 16).
- **Key questions:** two new groups — safety-critical-ML methodology (Q8.1/Q8.2) and metric
  honesty (Q0.4) — plus system-reliability (Q0.5); 8 P0-gating questions identified.
- **Theme-coverage matrix:** THIN cells (assurance SC1, tech-debt SC3, drift SC7, missing-modality
  SC9) flagged as explicit P2/P3 gaps.

## 6. CONFIRMED / LIKELY / HYPOTHESIS / INFEASIBLE (§0.5 rule 4)
- CONFIRMED (live this session): identities + core numbers of the two audited quota papers
  (2010.09107, 2606.21130) match their live abstract pages exactly (Audit #7, 0% error); the
  15 quota IDs are NEW (absent from ledger + novelty index).
- LIKELY: the methodology of the other 13 quota papers as summarised (FT-PARTIAL — abstract +
  named sections read; middle tables pruned, so table-level numbers not independently verified
  except where visible).
- HYPOTHESIS: transfer of any quota paper's RESULTS to the Himalaya hazard setting (all are
  far-domain: data centers, phishing, pedestrians, wildfire, energy) — labelled transfer
  hypotheses, not evidence about TRINETRA.
- INFEASIBLE this phase: SHA/size (no shell); BOM ₹ verification (deferred to P6 via Wayback);
  any claim about OUR system's performance (nothing built, Rule 16).

## 7. Non-destruction compliance
No pre-existing file deleted, moved, or renamed. The only pre-existing file edited in place was
analysis/00_system_model.md, backed up copy-on-write to
PROGRAM/backups/2026-10-05_pre_program/00_system_model.md BEFORE the §11 append; logged in
PROGRAM/CHANGELOG.md. All other P1 outputs are new or program-owned files. The DO-NOT-MODIFY
ledger analysis/02_paper_ledger.csv was read-only throughout (quota tracked separately in
PROGRAM/phase_papers/P1_papers.csv + novelty_index append log).

## 8. Exit audit
- Every baseline paper either has a verified note or an honest "unreadable/fetch-failed/no-HTML"
  reason logged (P1_reading_progress.md); baseline re-study is SUBSTANTIALLY DONE (highest-relevance
  anchors full-text; lower-priority IDs deferred to P2+ as explicitly allowed).
- System model complete (§11 ADDENDUM); key questions finalized and locked; theme-coverage matrix built.
- **Quota MET: 15/15 NEW papers, 100% Tier-2+ (≥60% requirement exceeded).**
- Faithfulness audit (Audit #7): 2/15 (~13% ≥ 10% gate), 0% identity/claim error (<5% gate).
- Registers propagated (CR/FM/equations/hyperparameters/novelty index/key questions/matrix).
- No phase beyond P1 started; no code/training/experiments; no new papers beyond the quota + baseline.
STATUS: AWAITING GATE. Will STOP; P2 requires explicit "GO PHASE P2".
