# PROGRESS — program-level progress tracker (MASTER_PROMPT §0.3)
# New root file. The pre-existing analysis/PROGRESS.md (old 6-phase scheme) is left untouched.
# This tracks the P0–P20 program. Updated at every phase start/checkpoint/end.

## Phase P0 — Setup, inventory, backup, state reconciliation, plan  [PRE-AUTHORIZED]
STATUS: COMPLETE → GATE PASSED (user authorized P1 2026-10-05).

Tasks:
- [x] 0.0 Save MASTER_PROMPT.md (827 lines, verified)
- [x] 0.1 folder_inventory.md + file_manifest.csv (26 rows; SHA/size/mtime INFEASIBLE)
- [x] 0.2 BACKUP_MANIFEST.md + copy-on-write policy (no in-place edits in P0)
- [x] 0.3 ENVIRONMENT_CHECK.md (tool capability probes)
- [x] 0.4 analysis/00_context_recovered.md
- [x] 0.5 Reconciliation: novelty_index.csv (235 unique ABS), reconciliation audit (7th,
          0% error), RESUME_STATE_2026-10-05.md, DECISIONS.md (OLD→NEW phase map)
- [x] 0.6 Standard layout (§0.10) initialized non-destructively: control files, root
          registries, analysis registers, HANDOFF, sota/ + phase_papers/ templates,
          workstream + DEPLOYMENT stubs
- [x] 0.7 PHASE_PLAN.md (recommended sequence + dependency graph + 1 alternative),
          RISK_REGISTER.md, LEAD_TIME_ITEMS.md
- [x] 0.8 analysis/00_key_questions_draft.md (no searching)
- [x] 0.9 Exit audit + PROGRAM/reports/PHASE_00_report.md + gate message → STOP

VERIFIED CORPUS: 250 ledger data rows − 1 dedup marker − 14 redundant = 235 unique new
papers, ALL abstract-only (read_depth=ABS), 0 full-text.

## Phases P1–P20 — P1 COMPLETE; P2 COMPLETE (gate delivered); P3–P20 NOT STARTED
## (each requires explicit "GO PHASE Pn")

## Phase P3 — Literature Foundation II  [AUTHORIZED 2026-10-06 "GO PHASE P3"]
STATUS: COMPLETE → GATE DELIVERED (PROGRAM/gate_messages/PHASE_03_gate.md). 43 NEW quota reads.
Scope (D-009): depth-first + honest shortfall; working target ≈50 NEW FT-PARTIAL Tier-2+ reads across
all P3 themes (user: "get around 50 new papers in depth covering the P3 themes in detail and continue").
Counting convention locked (D-009): headline foundation set = program-era NEW (P2+P3); deep-read count,
baseline-235 re-study, and tier split reported separately; no padding (§0.5). 250@≥60%-Tier-2+ not
honestly reachable under research-only tools → honest shortfall will be reported at gate.
Theme-rebalance directive (from P2 exit): steer AWAY from hazard-core TOWARD robustness/eval-critique/
efficiency/non-hazard; fill axes A3/A4/A9/A13 + widen P1 THIN cells.

Tasks:
- [x] 1. SOTA scan → PROGRAM/sota/P3_sota_scan.md (§1–§8 incl. §6 hazard-core + §7 axis-exhaustion)
- [x] 2. Search + log queries (02_search_log.md rows 158–219) + harvest pool → 10_reading_queue.csv
- [x] 3. Batch-cycle reading — 43 NEW FT-PARTIAL Tier-2+ (one note each). DONE = 43:
         2604.24404, 2603.17319, 2610.06453, 2610.04828, 2610.06241, 2610.03380, 2609.38655,
         2608.19836, 2609.18555, 2610.03369, 2602.14676, 2608.16654, 2610.00363, 2507.07841,
         2608.06876, 2609.39337, 2605.23504, 2007.05848, 2609.31142, 2609.15297, 2609.38552,
         2606.00690, 2610.06317, 2609.27202, 2605.06643, 2605.01679, 2511.20936, 2203.13313,
         2511.05471, 2012.13849, 2604.16265, 2609.34836, 2511.15838, 2606.04634, 2607.24683, 2005.03221, 2605.17419, 2512.24117, 2607.26854, 2609.14821, 2608.30205, 2608.11142, 2509.10362
         (+ baseline re-studies non-quota: 2606.16795 WaveDINO, 2608.12422 "Which Site and When")
         (NO-HTML, not counted: 2111.12209, 2601.07268, 2512.17785; Tier-3 ABS-leaning, not counted: 2610.04151)
- [x] 4. Maintain registers (claims/equations/hyperparameter/contradiction/novelty index) + RISKS RB-13+
- [x] 5. Interim syntheses every ~5 batches (PROGRAM/reports/P3_interim_syntheses.md) — #1,#2,#3 done
- [x] 6. P3 deliverables: P3_papers.csv, P3_reading_progress.md, ledger rows tagged [P3]
- [x] 7. Final foundation-set theme-grouped REFERENCES.md (P3 section) + distribution in PHASE_03_report §3/§5
- [x] 8. Exit audit (#9, 9/43 ≈21% sample, 0% error) → PHASE_03_report.md → PHASE_03_gate.md → STOP

## Phase P2 — Literature Foundation I  [AUTHORIZED 2026-10-06 "GO PHASE P2"]
STATUS: COMPLETE → GATE DELIVERED (PROGRAM/gate_messages/PHASE_02_gate.md).
Objective: first ~40-60% of the NEW-paper foundation set (P2+P3 together = 250-400 verified new
papers). Quota of 15 NEW EXCEEDED (18 read); 100% Tier-2+ (>=60% met); theme balance documented
(hazard-core 33% flagged for P3 rebalance; all others <=22%).

Tasks:
- [x] 1. SOTA scan → PROGRAM/sota/P2_sota_scan.md (fire/smoke/CCTV + eval/robustness) incl §8 targets+protocol
- [x] 2. Seed + log search queries (02_search_log.md rows 136-157, 22 queries) + reading queue (+8 P3 candidates)
- [x] 3. Batch-cycle reading — 18 NEW read (all FT-PARTIAL Tier-2; quota 15 EXCEEDED):
         2605.17419, 2610.01994, 2610.04392, 2508.14203, 2610.02777, 2606.07593, 2609.38936,
         2605.15894, 2507.21649, 2607.28248, 2511.21364, 2609.20441, 2609.07455, 2609.05066,
         2609.17175, 2605.20167, 2509.18176, 2606.13896
- [x] 4. Maintain registers (claims/equations/hyperparameter/contradiction/novelty index/citation graph)
- [x] 5. Interim syntheses every 5 batches (PROGRAM/reports/P2_interim_syntheses.md — #1 after 10, #2 after 18)
- [x] 6. P2 deliverables: P2_papers.csv, P2_reading_progress.md, ledger rows tagged [P2]
- [x] 7. PHASE_02_report.md incl "SOTA targets and protocol plan"
- [x] 8. Exit audits (Audit #8, 4/18 ≈22%, 0% error) → PHASE_02_gate.md → STOP

## Phase P1 — Baseline papers + system model + lock key questions  [AUTHORIZED 2026-10-05]
STATUS: COMPLETE → GATE DELIVERED (PROGRAM/gate_messages/PHASE_01_gate.md).
User OQ-01..OQ-06 answered (see PROGRAM/OPEN_QUESTIONS.md, DECISIONS D-007/D-008).
Quota = 15 NEW papers ON TOP of a proper Tier-2+ RE-STUDY of the 235-paper baseline (OQ-02).
Full-text route = ar5iv/arXiv-HTML via web_fetch (D-008).

Tasks:
- [x] 1. SOTA scan → PROGRAM/sota/P1_sota_scan.md
- [~] 2. Re-study baseline corpus at TRUE Tier-2+ — SUBSTANTIALLY DONE: 46 notes
         (43 corpus + 3 external anchors) across all 7 clusters
         (ledger: PROGRAM/logs/P1_reading_progress.md, 62 rows)
- [x] 3. analysis/00_system_model.md (backed up P0 original; appended §11 ADDENDUM)
- [x] 4. analysis/01_baseline_papers.md overview/themes/gaps
- [x] 5. analysis/00_key_questions.md (finalized/locked)
- [x] 6. theme-coverage matrix (analysis/12_theme_coverage_matrix.md)
- [x] 7. read 15+ NEW quota papers — DONE 15/15, ALL FT-PARTIAL (100% Tier-2+)
         (notes: analysis/03_paper_notes/*_QUOTA_*.md; PROGRAM/phase_papers/P1_papers.csv)
- [x] 8. HANDOFF + exit audits + PHASE_01_report.md → gate message → STOP

## Phase P4 — Synthesis  [AUTHORIZED 2026-10-07 "GO PHASE P4 and if it is done GO PHASE P5 as well"]
STATUS: COMPLETE → GATE DELIVERED (PROGRAM/gate_messages/PHASE_04_gate.md). 15 NEW quota reads (100% Tier-2+).
Tasks:
- [x] 1. SOTA currency scan of consensus positions → P4_sota_scan.md PART A update (16/16 current)
- [x] 2. analysis/04_synthesis.md program-era section (theme+component clusters, consensus/disagreement, gaps)
- [x] 3. 06_contradiction_register.md finalized w/ resolving studies + NEW CR-08
- [x] 4. 05_failure_mode_catalogue.md → FULL (FM-28..FM-40)
- [x] 5. analysis/07_design_changes.md — DC-01..DC-20 ranked
- [x] 6. ws1..ws8/literature_brief.md (8 briefs)
- [x] 7. 00_key_questions.md P4 update (D-012)
- [x] 8. 15 NEW quota reads + P4_papers.csv + ledger [P4] rows + P4_reading_progress.md
- [x] 9. Audit #10 (random 10% = 25 checks, 0% error; 100% synthesis traceability; count-correction logged)
- [x] 10. HANDOFF + report + gate + PHASE_STATE/PROGRESS/CHANGELOG/DECISIONS

## Phase P5 — Dataset registry + compute budget  [COMPLETE 2026-10-07]
STATUS: all 8 tasks done → gate delivered (PHASE_05_gate.md). CONTINUING into P6 per the extended
authorization ("if you complete P5 you can start P6").
- [x] 1. SOTA scan of benchmarks/leaderboards per workstream → P5_sota_scan.md
- [x] 2+3. DATASETS.md populated: 26 verified datasets (D01–D26) + QUICK LINKS + COST + LICENSE +
      verification legend + full entries; FREE-ONLY held (no paid selected)
- [x] 4. dataset→model/WS matrix + 5-step cross-eval plan + registration/early-access list
- [x] 5. KAGGLE_BUDGET.md populated: 25.5 usable GPU-h/wk (≥15% reserve), per-WS 21 GPU-h, seed policy, cut-list
- [x] 6. 15 NEW quota reads (FT-PARTIAL ×2 + ABS ×13) + P5_papers.csv + ledger [P5] rows + P5_reading_progress.md
- [x] 7. Audit #11: 3/26 (11.5%) dataset entries re-verified, 0 material errors
- [x] 8. HANDOFF + PHASE_05_report + PHASE_05_gate + PHASE_STATE/PROGRESS/CHANGELOG
      (+ P5_dataset_verification.md verification mirror)

## Phase P7 — WS1a physics model set + derivations on paper (FIRE physics)  [COMPLETE 2026-10-09]
STATUS: COMPLETE → GATE DELIVERED (PROGRAM/gate_messages/PHASE_07_gate.md). RESEARCH-ONLY (paper
derivations; no code/build). STOPPING; P8 needs explicit "GO PHASE P8".

Tasks (MASTER_PROMPT L437–454):
- [x] 1. SOTA scan (physics-informed/guided fire + fire-growth/smoke-transport) → PROGRAM/sota/P7_sota_scan.md
- [x] 2. Recover originals + candidate phenomena map → established_formula_inventory.md
- [x] 3a. Layer-1 inventory (statement/source/validity/assumptions/KNOWN WEAKNESSES) → EF-01..12
- [x] 3b. Layer-2 extensions (parent+weakness+full derivation) → derivations/B-01,B-02,B-05,B-06
- [x] 3c. Lineage table + reduces-to-parent → formula_class_table.md
- [x] 3d. Admission A/B/C + N (12 A + 4 B + 2 C) → model_set_decision.md
- [x] +. LAYER1_outlines.md, validation_plan.md, verification_checklists.md (+ independent recheck), novelty_log.md
- [x] +. Equations-register P7 section; DATASETS.md D31–D34 [D]
- [x] Q. ≥15 NEW quota → 22 NEW (5 FT + 1 FT-PARTIAL + 16 ABS); literature_map.md / P7_papers.csv / P7_reading_progress.md
- [x] A. Exit audit → Audit #13 PASS
- [x] R. PHASE_07_report.md + PHASE_07_gate.md + PHASE_STATE/PROGRESS/CHANGELOG

RESULT: model set N-by-evidence = 12 Class-A (EF-01..12) + 4 Class-B (B-01/B-02/B-05/B-06, each reduces to
parent, independently re-derived, 0 errors) + 2 Class-C (offline simulators); live on-device fire-PINN
REJECTED (PINN failure-mode evidence). Physics enters as features/priors/consistency + offline simulator.
HONEST: web_search no API key → arXiv-only; classic correlations ABS-CANONICAL (NOT quota), [coeff-verify] +
expert review required; physics datasets D31–D34 [D] not portal-verified. SCOPE: FIRE physics per
MASTER_PROMPT L429; geo-hazard seed eqns scoped to a separate workstream (intact) — confirm at gate.

## Next step
P7 COMPLETE (running body-level deep NEW P1..P7 = 100). STOPPING at the P7 gate. P8 requires explicit
"GO PHASE P8" (silence ≠ permission). Open gate actions: confirm [coeff-verify] constants vs primary sources
+ expert review; portal-verify physics datasets; (carried) P6 2nd-source pricing; P14Z (D-011) still deferred.

## Phase P6 — IoT node research + BOM (≤₹2,000 incl GST) + safety protocol  [COMPLETE 2026-10-09]
STATUS: COMPLETE → GATE DELIVERED (PROGRAM/gate_messages/PHASE_06_gate.md). RESEARCH + COMPONENT-SELECTION
ONLY (no building/purchasing/operation). STOPPING; P7 needs explicit "GO PHASE P7".

Tasks (MASTER_PROMPT L401–460):
- [x] 1. SOTA scan (low-cost multi-sensor + TinyML fire detection) → PROGRAM/sota/P6_sota_scan.md
- [◑] 2. Read via engine; datasheets/standards to ledger — PARTIAL (datasheet hosts 403/404 → gap logged)
- [x] 3. On-device physics rules (rate-of-rise/fusion/time-constants) as hypotheses → ws7_iot/design.md
- [x] 4. Open fire + nuisance datasets + baselines → DATASETS.md D27–D30
- [x] 5. Component selection + BOM ≤₹2000 (verified Indian prices, single-source honest)
- [x] 6. ws7_iot/BOM.md + HARDWARE_BUDGET.md (recomputed totals + cut-list + assumed-owned) + SHOPPING_LIST.md
- [x] 7. ws7_iot/SAFETY.md (safe-stimulus protocol)
- [x] 8. ws7_iot/design.md (preliminary design + acceptance criteria)
- [x] Q. ≥15 NEW quota → 20 NEW (1 FT-PARTIAL + 19 ABS); literature_map.md / P6_papers.csv / P6_reading_progress.md
- [x] A. Exit audit → Audit #12 (reading, 0 err) + #12b (BOM price, re-verified MQ2 ₹68 + LoRa ₹389, 0 err)
- [x] R. PHASE_06_report.md + PHASE_06_gate.md + PHASE_STATE/PROGRESS/CHANGELOG

RESULT: ≤₹2000 node feasible from VERIFIED prices (Build A camera ₹712.72, Build B sensor-fusion ₹1695.66
incl-GST, before cell+enclosure). HONEST: prices single-source (Wayback offline, robu/amazon unreadable);
specs seller-stated; 4 reading topics uncovered (web_search no key). FINDING: LoRa Ra-02 is 433 MHz ≠ India
865–867 MHz → defaulted to ESP-NOW. SCOPE: FIRE-detection node per MASTER_PROMPT L3 (confirm at gate).

(P6 close-out: running body-level deep NEW P1..P6 = 94; gate delivered. Superseded by P7 above.)

## Phase P7 — WS1a FIRE physics model set & derivations  [COMPLETE → gate]
STATUS: COMPLETE. 12 A + 4 B + 2 C fire models; Layer-2 B-01/02/05/06 reduce-to-parent (indep. rechecked);
22 NEW arXiv quota; Audit #13 PASS. Running body-level deep NEW = 100.

## Phase P8 — WS4 CCTV fire/smoke DETECTION  [COMPLETE → gate record (continuous mode)]
STATUS: COMPLETE.
- [x] SOTA scan PROGRAM/sota/P8_sota_scan.md
- [x] ws4_cctv/failure_taxonomy.md (nuisance classes A–F)
- [x] ws4_cctv/evaluation_protocol.md (leakage-safe GROUP splits + TTD + false-alarms/camera-day + ≥5-seed CIs)
- [x] ws4_cctv/model_selection.md (two-stage cascade: on-node INT8 gate → gateway small-YOLO → temporal → fusion)
- [x] ws4_cctv/plan.md (edge, label-scarcity, privacy/adversarial, interfaces)
- [x] ws4_cctv/literature_map.md — 41 NEW arXiv (ABS; ≥15 aim 30-40 → exceeded)
- [x] DATASETS D35-D44 [D]; 17 [P8] ledger rows (full 41 in literature_map); Audit #14 PASS
- [x] PHASE_08_report.md + PHASE_08_gate.md + state updates
RESULT: paper design + protocol + literature. HONEST: ABS-only depth (0 FT); IDs subagent-reported;
web_search no key + arXiv rate-limited; datasets [D]/licenses unverified; tamper/spoof/privacy + nuisance
(steam/cloud/fog) + FASDD/MIVIA + deployable open-vocab = open actions. Network-exposed gateway endpoint
REQUIRES auth (flagged). Running body-level deep FT NEW unchanged at 100.

## Phase P7G — WS1b GEO-HAZARD physics model set & derivations  [COMPLETE → gate record (continuous mode)]
STATUS: COMPLETE (NEW inserted phase; spec PROGRAM/PHASE_P7G_SPEC.md).
- [x] established_formula_inventory.md (GH-01..GH-13)
- [x] derivations/LAYER2_derivations.md (GB-01..GB-05; reduce-to-parent; INDEPENDENTLY rechecked 0 errors)
- [x] formula_class_table.md; model_set_decision.md (N=13 A + 5 B + 3 C); validation_plan.md;
      verification_checklists.md; novelty_log.md (Rule 21 — no novelty)
- [x] literature_map.md — 17 NEW primary arXiv (ABS) + 18 FT-REF; 17 [P7G] ledger rows
- [x] equations-register geo section (pending seed resolved); DATASETS D45-D54 [D]; Audit #15 PASS
- [x] PHASE_07G_report.md + PHASE_07G_gate.md + state updates
RESULT: GB-03 antecedent-aware probabilistic rainfall threshold = CORE landslide EWS. Rule 19 advisory-only.
HONEST: coefficients [coeff-verify] (forms verified, values not) + expert review; CENTRAL DATA GAP —
ungauged Himalayan catchments lack local inventories/gauged records → GB-03/04/05 advisory-only until
calibrated. Running body-level deep FT NEW unchanged at 100.

## Phase P9 — ANOMALY DETECTION (WS8a)  [COMPLETE → gate record (continuous mode)]
STATUS: COMPLETE.
- [x] SOTA scan PROGRAM/sota/P9_sota_scan.md (eval-integrity crisis + realistic bar)
- [x] ws8_anomaly/scope_decision.md (family in/out + priority + lead-vs-support)
- [x] ws8_anomaly/evaluation_protocol.md (PRE-REGISTERED; point-adjust banned as primary; PATE/VUS-PR +
      Within-AUROC + leakage-free splits + simple-baselines-first + per-family targets)
- [x] ws8_anomaly/design.md (edge→gateway→server topology; score calibration; interfaces to P12/P13/P14)
- [x] ws8_anomaly/build_plan.md (priority order + Kaggle ~6-8 GPU-h + data/edge plan)
- [x] ws8_anomaly/literature_brief.md (P9 section appended; prior P4 brief intact)
- [x] ws8_anomaly/literature_map.md — 35 NEW primary arXiv (ABS) across 6 families
- [x] DATASETS D55-D67 [D]; 20 [P9] ledger rows (full 35 in literature_map); Audit #16 PASS
- [x] PHASE_09_report.md + PHASE_09_gate.md + state updates
RESULT: anomaly = SAFETY NET for supervised-detector blind spots. P1 = sensor-TS + OOD/health; P2 =
physics-residual + video(support-only) + network/alert; deferred = social (privacy). Rule 19 advisory.
HONEST: ABS-only (0 FT); web_search no key; IDs subagent-reported; datasets [D]; REAL false-alarm/delay
numbers require build-time own-data collection. Running body-level deep FT NEW unchanged at 100.

## Phase P10 — ANOMALY-DETECTION IMPLEMENTATION SPECS (WS8b)  [COMPLETE → gate record (continuous mode)]
STATUS: COMPLETE.
- [x] ws8_anomaly/spec/sota_targets.md (SOTA update + reproduce-first baselines + cited DEFAULT-RECIPE
      REGISTRY + fair-comparison requirements + quota list)
- [x] ws8_anomaly/spec/family_{a_video,b_sensor_timeseries,c_ood_health,d_physics_residual,e_network_alert}.md
- [x] ws8_anomaly/spec/edge_spec.md + integration_spec.md
- [x] ws8_anomaly/failure_analysis.md
- [x] literature_map.md P10 section — 23 NEW primary arXiv (ABS, none reuse P9); 19 [P10] ledger rows;
      Audit #17 PASS
- [x] PHASE_10_report.md + PHASE_10_gate.md + state updates
RESULT: ready-to-build specs. Conformal+FDR/EVT-hysteresis thresholding; overlapping windows + anti-
convergence-collapse; RIFT/matrix-profile baselines; calibration first-class; edge QAT/HDC; video support-
only; zero-shot-FM negative result honored. Rule 19 advisory. HONEST: ABS-only (0 FT); edge figures other-
hardware → P13 measurement; own-data needed for real operating points. Running body-level deep FT NEW
unchanged at 100.

## Phase P11 — DEEPFAKE & MISINFORMATION (WS2)  [COMPLETE → gate record (continuous mode)]
STATUS: COMPLETE.
- [x] PROGRAM/sota/P11_sota_scan.md (cross-generator + degraded framing + provenance limits)
- [x] ws2_deepfake/system_design.md (trust/corroboration pipeline + trust tiers + EXPLICIT cost matrix
      t*=C_FP/(C_FP+C_FN), human-in-the-loop)
- [x] ws2_deepfake/{literature_map,evaluation_protocol,robustness_plan,physics_plausibility,experiment_plan}.md
- [x] 20 NEW primary arXiv (ABS, all 9 families; ≥15 MET, ~40 stretch NOT reached — disclosed); DATASETS
      D68-D88 [D] (CCDF D77 ⚑); 20 [P11] ledger rows; Audit #18 PASS
- [x] PHASE_11_report.md + PHASE_11_gate.md + state updates
RESULT: detection alone fails vs frontier generators (DF26/CCDF/SLED-1400) → external corroboration + human-
in-the-loop mandatory; watermarks/C2PA removable → provenance positive-only; out-of-context recycled real
media = dominant threat. NO deceptive media created. HONEST: ABS-only; no fire-specific synthetic corpus
(GAP); Indian-language claim set (GAP). Running body-level deep FT NEW unchanged at 100.

## Phase P12 — OFFLINE LOCAL-AREA ALERTING (WS3)  [COMPLETE → gate record (continuous mode)]
STATUS: COMPLETE.
- [x] VERDICT: IP-address targeting INFEASIBLE (topological not geographic; NAT/CGNAT/mobile) → proximity +
      authority broadcast → ws3_alerting/feasibility_analysis.md
- [x] PROGRAM/sota/P12_sota_scan.md
- [x] ws3_alerting/architecture.md (tiered siren→LAN/mesh/BLE→cellular→DTN; confidence→tier policy; Rule 19)
- [x] ws3_alerting/{threat_model, simulation_spec(ns-3, nothing simulated), literature_map}.md
- [x] 20 NEW primary arXiv (ABS, families A-G; ≥15 MET, ~40 stretch NOT reached — disclosed); DATASETS
      D89-D94 [D]; 20 [P12] ledger rows; Audit #19 PASS
- [x] PHASE_12_report.md + PHASE_12_gate.md + state updates
RESULT: no single channel suffices → tiered graceful-degradation; cell broadcast reaches phones but
UNAUTHENTICATED + authority-operated; owned tiers = siren + LoRa/Meshtastic mesh + BLE flood; DTN backstop.
HONEST GAPS: Zigbee/ESP-NOW/802.11s + India regulatory specifics TO-VERIFY (P13/standards). Running body-
level deep FT NEW unchanged at 100.

## Phase P13 — IoT DEVICE DESIGN & BUILD MANUAL (WS7b)  [COMPLETE → gate record (continuous mode)]
STATUS: COMPLETE (DOCUMENTS ONLY).
- [x] PROGRAM/sota/P13_sota_scan.md (baselines + targets)
- [x] ws7_iot/FIRMWARE_SPEC.md (state machine, timing, logging, dashboard, signed+replay msgs, watchdog/
      brownout/ADC-vs-Wi-Fi) — no code
- [x] ws7_iot/{HARDWARE_BUILD, CALIBRATION_PROTOCOL, TEST_PROTOCOL, DEMONSTRATION_PLAN, LIMITATIONS,
      INTEGRATION_NOTES}.md
- [x] HARDWARE_BUDGET.md P13 re-verification note (HONESTLY PARTIAL — prices AS-OF-P6)
- [x] 20 NEW primary arXiv (ABS, 7 topics; ≥15 MET); DATASETS D95-D98 [D]; 20 [P13] ledger rows; Audit #20 PASS
- [x] PHASE_13_report.md + PHASE_13_gate.md + state updates
RESULT: self-contained build+test manual; e-nose fire comparator; 8-bit near-lossless TinyML; core-separation
reliability; T/RH+drift reference-free compensation. Rule 19 advisory + fail-safe. HONEST: no fire-labeled IoT
dataset (GAP); watchdog/brownout = documented ESP-IDF behavior; BOM re-price at build. Running body-level deep
FT NEW unchanged at 100.

## Phase P14 — META-FUSION DESIGN (WS1b)  [COMPLETE → gate record]
22 NEW primary arXiv (ABS, 8 topics; ≥15 MET). ws1_physics/{fusion_design, ablation_plan}.md + P14 SOTA scan;
literature_map P14 section; 22 [P14] ledger rows; Audit #21 PASS; PHASE_14_report.md + gate. Grouped
uncertainty-aware CALIBRATED fuser; calibrate-the-fused-output; common-scale-before-fusion; group correlated
parent+extension; conformal reweighting bounds a bad source; per-availability recalibration; abstention→human;
proper scores primary (ECE demoted). PRE-REGISTERED acceptance (beat best single cross-site by proper-score
margin > seed variance). Rule 19 advisory. Running body-level deep FT NEW unchanged at 100.

## Phase P14Z — ZERO-SHOT / OPEN-VOCAB HAZARD RECOGNITION (inserted)  [COMPLETE → gate record]
16 NEW primary arXiv (ABS; ≥10 MET). ws4_cctv/zero_shot_design.md (D-011: ZS = calibrated LOW-WEIGHT
complement; trained P8 primary; fire-domain trained>ZS; mandatory calibration-before-fusion) + P14Z SOTA scan;
literature_map P14Z; 16 [P14Z] ledger rows; DATASETS D99-D101 [D]; Audit #22 PASS; PHASE_14Z_report.md + gate.

## Phase P15 — RL DESIGN (WS5)  [COMPLETE → gate record]
21 NEW primary arXiv (ABS; ≥15 MET). ws5_rl/{rl_design, environment_spec, rl_evaluation_plan, literature_map}
.md + P15 SOTA scan; 21 [P15] ledger rows; DATASETS D102-D105 [D]; Audit #23 PASS; PHASE_15_report.md + gate.
RL ADVISORY + must beat non-RL baselines; offline-first small-compute; safe/constrained prerequisite (min-peak-
harm fallback, at-all-times safety, structural constraints); reward integrity (anchor-guarded verifier).

## Phase P16 — ROBUSTNESS/SECURITY/FAILURE-MODE (WS6)  [STARTING]
Reader (23 papers, e7c17e5e) PIPELINED and in hand: adversarial patches, corruption/shift, poisoning, sensor
spoofing, jamming, drift monitoring, detector evasion. Writing robustness catalogue + defense/monitoring plan.
Auto-proceeding.

## Phases P16 → P20 — COMPLETE (continuous mode)
- P16 ROBUSTNESS/SECURITY (WS6): 23 NEW arXiv; robustness_catalogue + defense/monitoring + eval plan; Audit
  #24 PASS. Cross-sensor corroboration = most transferable defense; uncertainty-entropy alert gate.
- P17 FEATURE REGISTRY: 22 NEW arXiv; FEATURES.md F-11..F-26 (Wave-1 F-11..F-17 approved); Audit #25 PASS.
- P18 FEATURE SPECS (Wave-1): 21 NEW arXiv; features/wave1_specs.md; Audit #26 PASS; DATASETS D106-D107.
- P19 INDIA DEPLOYMENT: 25 NEW arXiv; 11 DEPLOYMENT docs (context/standards/stakeholders/pilot/barriers/cost/
  release/contributions/publication/limits/litmap); Audit #27 PASS; DATASETS D108-D112. All regulatory facts
  [UNVERIFIED], flagged for expert review.
- P20 FINAL QUALITY GATES + FINAL_REPORT.md: 18 NEW arXiv (reporting standards); Audit #28 PASS (ledger 631
  unique/681 rows, 7.3% re-citations corrected; all phases ≥15; 250-min met ~436 new).

*** PROGRAM COMPLETE (P0→P20, incl. P7G, P14Z). FINAL_REPORT.md delivered. Research-only; nothing built. ***

## ADDENDUM PHASES P21-P23 — COMPLETE (user added 2026-10-10; goal goal-340c51ff-...)
- P21 FIRE-HAZARD PHYSICS DEEP-DIVE: 56 NEW papers (>=50 target MET). EF-13..EF-20 established extensions +
  7 NOVEL Class-C derivations ND-1..ND-7 (dealiased flicker; smoke-transmittance temp; dimensionless ignition
  index; physics-residual score; wind-tilt flame height; radiative-convective scalar; advection-coherence).
  Files in ws1_physics/*_P21.md. Audit #29 PASS.
- P22 META-FUSION PHYSICS + RL + MULTIMODAL: 54 NEW papers. 6 derived fusion models (FM-1..FM-6) + NOVEL
  PHARAOH adaptive-order aggregation operator + 4 novel formulas (NF-1..NF-4) + advisory RL/multimodal note.
  Files in ws5_fusion/. Audit #30 PASS.
- P23 FREE-DATASET HUNT: 52 free datasets (D113-D164) in DATASETS_CATALOGUE.md + portal scan; Audit #31 PASS.
Specs: PROGRAM/MASTER_PROMPT_ADDENDUM.md (MASTER_PROMPT.md untouched). All Class-C novel work UNVALIDATED
(novelty = limited-search claim; web_search unavailable); advisory/human-in-loop; no performance claimed.

*** ADDENDUM PROGRAM COMPLETE (P21-P23). Research-only; nothing built/measured; all novel formulas Class-C. ***
