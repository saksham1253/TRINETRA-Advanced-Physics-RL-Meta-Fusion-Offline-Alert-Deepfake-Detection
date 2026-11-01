# PHASE P4 REPORT — Synthesis

Date: 2026-10-07 · Phase: P4 (authorized "GO PHASE P4 and if it is done GO PHASE P5 as well", 2026-10-07)
· Status at exit: COMPLETE → AWAITING GATE (then continue into P5 per the same authorization)

---

## 1. Objective (from §P4 / MASTER_PROMPT)
Turn the whole literature (235-paper ABS baseline + 76 program-era deep reads from P1–P3) into usable,
design-driving knowledge: cluster by theme + component; map consensus vs disagreement; name techniques
the field shows beat ours; expose gaps; finalize the contradiction register with resolving studies;
promote the failure-mode catalogue to full; produce a ranked "what would change our design" list;
write per-workstream briefs; update key-questions; read ≥15 NEW quota papers chosen to resolve the
contradictions/gaps the synthesis exposes; full ledger audit (random 10% + traceability). RESEARCH-ONLY;
no own-system claims (Rule 16). STOP at the P4 gate.

## 2. What was done (outputs on disk)
| Task | Output | Key result |
|------|--------|------------|
| 1. SOTA currency scan of consensus positions | PROGRAM/sota/P4_sota_scan.md (PART A + post-quota update + PART B + PART C ledger) | 16/16 consensus positions current; 6 RESOLVED, 8 REINFORCED, 2 SUPPORTED; none refuted |
| 2. Synthesis (theme + component clusters, consensus/disagreement, better-than-ours, gaps) | analysis/04_synthesis.md (program-era section, APPEND-ONLY after legacy 546 lines) | 16 C-nn positions, 2 live tensions, 8 gaps, 9 better-than-ours techniques |
| 3. Contradiction register finalized w/ resolving studies | analysis/06_contradiction_register.md (P4 closure block) | CR-01..CR-07 each given resolving study + build experiment; NEW CR-08 (FMs for our regime) |
| 4. Failure-mode catalogue → FULL | analysis/05_failure_mode_catalogue.md (FM-28..FM-40 added) | +13 modes: leakage/eval/numerical/calibration/media/physics-transfer, each paper-linked |
| 5. "What would change our design" ranked | analysis/07_design_changes.md (NEW) | DC-01..DC-20, ranked, each w/ evidence+workstream+phase; top-3 flagged for user |
| 6. Per-workstream briefs | ws1..ws8/literature_brief.md (8 NEW) | most-relevant papers + key claims + open questions per WS |
| 7. Key-questions update | analysis/00_key_questions.md (P4 block, D-012) | 8 answered, open items carried, 5 new questions (Q9.1–Q9.5) |
| 8. Read ≥15 NEW quota + record | PROGRAM/logs/P4_reading_progress.md + PROGRAM/phase_papers/P4_papers.csv + 15 ledger [P4] rows | **15 NEW deep reads, 100% Tier-2+** |
| 9. Full ledger audit (random 10% + traceability) | analysis/11_reading_audit.md (Audit #10) | 0% identity error (25 checks); 100% synthesis traceability; 1 count-correction logged |
| 10. Handoff + state files | BUILD_HANDOFF, PHASE_STATE, PROGRESS, CHANGELOG, DECISIONS (D-012) | updated |

## 3. The 15 NEW quota reads (synthesis-driven)
Chosen to resolve the contradictions/gaps the synthesis itself exposed (per §P4 quota topics):
1. 2606.21773 DFL — resolves C-04/C-11 (decision vs prediction).
2. 2512.14221 mask-conditional CP — closes CR-04 missingness edge (C-05).
3. 2610.08227 "independent samples in a satellite image" — PROVES C-01 (spatial-CV theorem).
4. 2510.22016 Total Classification Cost — formalizes C-14 (cost-sensitive metric).
5. 2610.01384 CLEAR — supports C-13 (post-hoc fix for sparse/OOD overconfidence).
6. 2107.11003 offline-RL model selection — operationalizes C-11 (OPE-gated RL).
7. 2610.07232 TSFM under covariate noise — stress-tests C-07/C-02, feeds P14Z (new CR-08).
8. 2608.08158 dynamic reward shaping — grounds C-10 PBRS + its limits.
9. 2608.15261 optical-SAR routing — C-08 mechanism (route before mixing).
10. 2407.06785 landslide PINN (ABS→FT upgrade) — reinforces C-15/C-03.
11. 2608.14391 RA-Bench crisis-video — life-safety anchor for C-16 (no detector generalizes).
12. 2507.15614 HEC-RAS Geo-FNO surrogate — C-03 (cheap ensembles).
13. 2610.03649 on-board SSL anomaly — C-08/WS8 (SSL→classical, edge).
14. 2609.16707 predictability-per-scale — C-13/C-06 (FMs lag at extremes).
15. 2605.14365 LoMETab — C-02 2026 currency check (parsimony NOT reversed; GBDT still strong).

Depth: 11 FT-PARTIAL + 4 FT(ABS-strong) = 100% Tier-2+ (≥60% floor met).

## 4. Honest-count correction (§0.5)
During the exit audit, 2509.18176 was found to have been double-counted: it was already read FT-PARTIAL
in P2 (ledger ~line 269). It is therefore EXCLUDED from the P4 NEW quota and reclassified as a RE-STUDY;
2605.14365 (LoMETab) was read as the genuine 15th. Net P4 NEW deep reads = 15. Also: 2510.12328 is
ABS/NO-HTML → non-quota corroborator (C-06). The correction is logged in the ledger, reading-progress
tally, SOTA PART C, and Audit #10. Running program-era deep NEW reads: P1 15 + P2 18 + P3 43 + P4 15 = 91.

## 5. Headline synthesis findings
- The evaluation spine is now PROVEN, not merely best-practice: spatial-CV (2610.08227), cost-sensitive
  metric (2510.22016), action-loss + mask-conditional + online conformal (three independent papers).
- The parsimony result (C-02) survived its 2026 currency check (2605.14365): the DL-vs-GBDT gap has
  narrowed to a tight cluster but GBDT is still exceptionally strong and the competitive neural models
  are the simple ones — our GBDT-baseline + simple-first + residual-on-backbone doctrine holds.
- A NEW, honest tension (CR-08): foundation models help only when covariates are accurate (2610.07232);
  our monsoon covariates are noisy → P14Z must pre-register a TSFM-vs-from-scratch benchmark.
- Life-safety anchor hardened: no deepfake detector generalizes on crisis video (2608.14391) → media/
  crowd/zero-shot are low-trust advisory, never autonomous (Rule 19/C-16).

## 6. Top design changes (full ranked list in analysis/07_design_changes.md)
P0 (gate-blocking): DC-01 spatial-CV buffer · DC-02 cost-loss metric · DC-03 action-loss+mask-conditional+
online conformal · DC-04 media=low-trust advisory · DC-05 worst-case missing-modality eval.
P1: DC-06 bounded residual · DC-07 EVT prior · DC-08 physics-as-gate · DC-09 utility routing ·
DC-10 staged policy/OPE gate · DC-11 potential-based shaping.
THREE surfaced for user decision in the gate: DC-01, DC-02, DC-03 (cheapest now, most expensive to retrofit).

## 7. Acceptance check (§P4)
- Every synthesis claim traces to a note with a table/equation/page ref — ✅ (Audit #10 Part B, 100%).
- Contradictions + gaps documented — ✅ (CR-01..CR-08 + G1..G8).
- Design-change list ranked — ✅ (DC-01..DC-20).
- Quota met — ✅ (15 NEW, 100% Tier-2+).
- No own-system performance claims — ✅ (Rule 16 honored; process targets only).

## 8. Carried / deferred (non-blocking)
- 2609.14821 body numbers (−23.4% regret etc.) → re-verify vs PDF before load-bearing use in P14/P14Z.
- C-12 human-compliance numbers → non-arXiv NHESS/IJDRR in P13/P15 (one hard number so far: 2109.07745).
- G2 cross-zone conformal coupling (P14); G3 River-Eye LSPIV accuracy (P6/P8); G7 rockfall (P7).
- P14Z (compulsory zero-shot phase, D-011) — registered, executes at its authorized turn.
- Author backfills for a few "(per note)" rows — cosmetic ledger cleanup.

## 9. Exit
Quota audit ✅ · audit ✅ · report ✅ · gate message next (with the top design changes for user decision)
· then CONTINUE into P5 per the standing authorization; STOP at the P5 gate awaiting "GO PHASE P6".
