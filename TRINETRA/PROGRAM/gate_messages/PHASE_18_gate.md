# PHASE_18_gate — COMPLETION RECORD (feature specs & measurement plans, Wave-1)

CONTINUOUS-EXECUTION MODE: COMPLETION RECORD, not a halt. Auto-proceeding to P19.

PHASE: P18 — FEATURE SPECIFICATIONS & MEASUREMENT PLANS (MASTER_PROMPT P18) for Wave-1 F-11..F-17. RESEARCH-
ONLY; nothing implemented/measured. STATUS: COMPLETE.

DELIVERED: features/wave1_specs.md (F-11..F-17 full specs + measurement plans); PROGRAM/sota/P18_sota_scan.md;
21 [P18] ledger rows; DATASETS D106-D107 [D]; Audit #26 PASS; PROGRAM/reports/PHASE_18_report.md (incl. 21-
paper literature map).

QUOTA: 21 NEW primary arXiv (ABS), all distinct from prior cites, across 5 feature families (A edge detector,
B temporal validation, C conformal-under-shift, D label-free drift, E sensor drift). ≥15 required → MET. 0 FT;
running body-level deep FT NEW unchanged at 100.

SPECS: each feature has design+plug-in, config/build flags, I/O, hyperparameter defaults w/ sources, ablation
design, metrics, PRE-REGISTERED decision rule, cost, and risks/new failure modes (fed to the P16 robustness
catalogue). Binding cautions baked in: edge-TL NEGATIVE result (accuracy tricks may not help edge latency,
2501.08639); split-CP coverage collapse 90%→65.3% PICP under moderate shift (never claim 1−α cross-site
without weighting, 2604.22787); representation drift ≠ calibration drift (monitor both, 2406.17813); decompose
environmental vs instrumental drift before recalibration (2406.17488).

DECISION RULES: keep a feature only if its improvement exceeds seed/trial variance on a HELD-OUT CROSS-CAMERA/
CROSS-SITE split, confirmed by the inferential-reproducibility significance gate (2302.04054); honest negatives
are reportable outcomes.

RULE 16/19: nothing built/measured; monitors/auto-adapt advisory; no own-system claim.

HONEST LIMITS: specs only; ABS/source-reported on non-fire/other-domain benchmarks (transfer risk per
feature); exact hyperparameters need full-text reads (2503.07371, 2607.03131, 2610.09208, 2406.17813,
2406.17488); IDs subagent-reported not re-fetched.

NON-DESTRUCTION (§0.3): created wave1_specs + P18 SOTA scan + report; appended ledger/audit/DATASETS;
FEATURES.md untouched this phase. Nothing overwritten.

NEXT: P19 — INDIA DEPLOYMENT PATHWAY, STANDARDS/REGULATION, PILOT DESIGN, RESEARCH-CONTRIBUTION PLAN
(MASTER_PROMPT P19). Reader (25 papers) ALREADY IN HAND; india_context.md already drafted. Auto-proceeding.
