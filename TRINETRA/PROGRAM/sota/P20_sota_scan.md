# PROGRAM/sota/P20_sota_scan.md — final SOTA + reporting-standards scan (P20)

RESEARCH NOTES. MASTER_PROMPT P20.1. Refreshes the reporting/evaluation standards our targets must meet and
confirms the handoff targets are phrased as PROCESS targets (Rule 16), not promised results. All numbers
SOURCE-REPORTED. IDs + detail in PROGRAM/reports/PHASE_20_report.md.

## 1. Reporting & evaluation standards our handoff must satisfy (source-reported)
- SIGNIFICANCE: report IQM + stratified-bootstrap CIs + performance profiles over many seeds, not point
  estimates (rliable 2108.13264) — binds every "win" (with the P17 inferential-reproducibility gate 2302.04054).
- DOCUMENTATION: model cards with disaggregated performance + intended/out-of-scope use (1810.03993);
  datasheets for every dataset (1803.09010); MI-CLAIM-GEN-style minimum-information checklist for a safety-
  critical advisory system (2403.02558); reproducibility checklists (2003.12206, 2306.09562, 2207.04821).
- CALIBRATION (central to our uncertainty-gated alerts): recalibration is often LESS calibrated than reported
  and ECE is biased (verified calibration 1909.10155); ECE drawbacks + alternatives (2501.19047); proximity
  bias persists after temperature scaling (2306.04590); decision-theoretic calibration loss (2404.13503).
- CONTAMINATION/LEAKAGE: taxonomy + score-side disclosure (2608.29463); per-benchmark contamination measures
  (2310.18018); paired confidence test finds near-universal contamination (2406.18326); multilingual
  contamination (2410.16186); watermark benchmarks pre-release (2502.17259); temporal-signal fragility
  (2509.00072).
- METRIC CRITIQUE: evaluation scores are perishable, need metadata/expiry (2607.26191); leaderboards are
  gameable, rankings not robust (2106.05532).

## 2. Final SOTA targets (process targets, Rule 16 — NOT our results)
Per-task published numbers remain SOURCE-REPORTED on their own datasets; our handoff targets are stated as
"match/approach X under our protocol with the protocol differences spelled out", never "we achieve X". All
targets tables in the workstream designs already carry this phrasing; no number is presented as ours.

## 3. Honesty
These standards are adopted as the REPORTING CONTRACT for the build phase. Nothing is measured here. The
dominant risk the standards guard against — inflated/contaminated/overclaimed results — is exactly what this
program's hard-honesty rules (§0.5, Rule 16/18) already enforce.
