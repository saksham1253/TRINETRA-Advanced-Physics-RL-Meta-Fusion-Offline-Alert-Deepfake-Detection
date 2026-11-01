# PHASE P4 — GATE MESSAGE

Phase: P4 (Synthesis) · Date: 2026-10-07 · Status: COMPLETE, all 10 tasks done, exit audit clean.
Authorization in force: "GO PHASE P4 and if it is done GO PHASE P5 as well" → I now CONTINUE into P5
to its gate, then STOP awaiting "GO PHASE P6". This gate message is informational for P4; no new
authorization is required to proceed into P5.

---

## What P4 produced
- `analysis/04_synthesis.md` — program-era synthesis (append-only after the legacy 546 lines): 16
  consensus positions clustered by theme + workstream, 2 live tensions, 8 gaps, 9 "better-than-ours" techniques.
- `analysis/06_contradiction_register.md` — CR-01..CR-07 finalized with resolving studies + build
  experiments; NEW CR-08 (do foundation models help OUR noisy-covariate regime?).
- `analysis/05_failure_mode_catalogue.md` — promoted to full: FM-28..FM-40 added (leakage/eval/numerical/
  calibration/media/physics-transfer), each paper-linked.
- `analysis/07_design_changes.md` — DC-01..DC-20 ranked, each with evidence + workstream + implementing phase.
- `ws1..ws8/literature_brief.md` — 8 per-workstream briefs.
- `analysis/00_key_questions.md` — P4 update (8 answered, items carried, Q9.1–Q9.5 new); logged D-012.
- 15 NEW quota reads (100% Tier-2+): ledger [P4] rows + `PROGRAM/logs/P4_reading_progress.md` +
  `PROGRAM/phase_papers/P4_papers.csv`.
- `analysis/11_reading_audit.md` Audit #10 — 0% identity error (25 checks), 100% synthesis traceability.
- Report: `PROGRAM/reports/PHASE_04_report.md`.

## Honest notes (§0.5)
- One count-correction: 2509.18176 was already read in P2 → excluded from the P4 quota and reclassified
  as a re-study; 2605.14365 (LoMETab) read as the genuine 15th. Net P4 NEW = 15. Running total = 91.
- 2609.14821 body figures remain FT-PARTIAL body-pending (re-verify vs PDF before load-bearing P14/P14Z use).
- No claims about our own system's performance (Rule 16).

## THE DECISION I'd like you to be aware of (not blocking — P5 proceeds either way)
The three P0, gate-blocking design changes the literature now forces. They are cheap to adopt now and
very expensive to retrofit later, so I am treating them as locked DEFAULTS going into the build phases
unless you object:

1. **DC-01 — Spatial-CV with a correlation-range buffer is the ONLY admissible evaluation.** 2610.08227
   proves random/in-dataset splits understate confidence intervals by a factor proportional to the
   spatial-correlation range. Every headline number will be reported under tile-withheld block CV with a
   buffer ≥ estimated range, plus a random-vs-block CI-width leakage diagnostic.
2. **DC-02 — Primary metric = cost-loss Value Score (Total Classification Cost), not F1/AUC.** 2510.22016.
   Models are ranked by miss≫FA cost (p*=0.0476), never across base rates by a base-rate-dependent metric.
3. **DC-03 — Conformal must be action-loss-calibrated AND mask-conditional AND online.** 2609.14821 +
   2512.14221 + 2610.02777. The GMF conformal layer reports both predictive and action-loss coverage,
   per zone and per present-sensor mask.

If you disagree with any of these three, tell me and I will revise before they harden in P6+. Otherwise
they stand as defaults.

## STOP / CONTINUE
Per your standing authorization I am NOT stopping here — I continue directly into **P5 (Dataset Registry
+ Compute Budget Plan)** and will STOP at the P5 gate awaiting **"GO PHASE P6"**. (P6 is also the phase
where you said you want the verified ≤₹2,000 BOM so you can order parts early — I will surface which
datasets need early access requests at the P5 gate, and the BOM at P6.)
