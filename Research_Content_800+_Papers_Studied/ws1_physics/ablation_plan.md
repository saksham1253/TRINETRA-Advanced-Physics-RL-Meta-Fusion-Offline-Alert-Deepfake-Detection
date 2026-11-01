# ws1_physics/ablation_plan.md — fusion ablation & stress-test plan + pre-registered acceptance (P14, WS1b)

Phase P14 · RESEARCH-ONLY. MASTER_PROMPT P14 tasks 3+5. Pre-registered BEFORE any build; nothing run (Rule 16).
Governs how "fusion works" is decided, so it cannot be rationalized after seeing results (§0.5).

## 1. PRE-REGISTERED ACCEPTANCE CRITERIA (decided NOW)
"Fusion works" in the build phase IFF ALL hold:
- PRIMARY: the fused model beats the BEST SINGLE source on a CROSS-SITE / CROSS-CAMERA held-out split (train
  on some sites, test on unseen sites — the deployment-relevant generalization), measured by a PROPER SCORING
  RULE (log-loss or Brier; CRPS/energy score for distributional outputs), by a margin that EXCEEDS the
  seed-variance band.
- SEED VARIANCE: report ≥N seeds (N pinned at build, ≥5) with confidence intervals; the improvement must be
  larger than the overlap of CIs (not a single lucky seed).
- CALIBRATION: the fused output is at least as well-calibrated as the best single source (proper-calibration-
  error bound, 2203.07835), AND no worse under each missing-source pattern (per-availability recalibration,
  2605.12517).
- SAFETY: at matched detection sensitivity, the fused model's FALSE-ALARM rate ≤ best single source; the
  abstain/escalate path measurably reduces confident wrong calls.
If fusion does NOT clear this bar, the honest outcome is "use the best single source + abstention" — recorded
plainly, not hidden.

## 2. Ablations (on-paper plan; run in build)
- Single-model (each source alone) baseline.
- Leave-one-out (remove each source) + greedy forward/backward selection.
- Grouped-by-phenomenon-family (fire vs geo-hazard vs sensor) and ALL PAIRS if N small.
- WITH vs WITHOUT physics inputs; WITH vs WITHOUT anomaly inputs.
- PARENT (Layer-1) vs EXTENSION (Layer-2) vs both-grouped (tests the double-counting guard, fusion_design §1.3).
- Fused vs best-single (the headline comparison).
- Fuser variants: evidential DST vs stacking meta-model vs weighted-conformal (fusion_design §2 Stage C).

## 3. Stress tests (robustness)
- SENSOR NOISE sweep; MISSING MODALITIES (drop vision / drop IoT / drop physics) → check accuracy AND
  calibration (2605.12517).
- ADVERSARIAL / spoofed inputs (one source attacked) → bounded influence (2103.00883) and conflict handling
  (2508.08075).
- DISTRIBUTION SHIFT: new camera, new site, new weather/season → online-conformal coverage holds (2307.16895).
- RARE EVENTS: recall-at-fixed-low-FPR under scarcity (2105.07346 bias caution).
- CORRELATED FAILURES: induce a shared failure in parent+extension → the grouping must prevent overconfidence.

## 4. Statistics
Multi-seed with CIs; cross-site splits (never shuffled-frame splits — leakage); proper-scoring-rule primary,
calibration-error diagnostic only; report effect sizes; negative/NULL results reported (§0.5).

## 5. Interfaces tested
Fused probability + uncertainty + abstain/escalate flag + source-availability vector delivered to the P12
alert decision policy and the P11 verification policy; confirm the abstain path triggers human review (Rule 19).

## 6. Honesty
Plan only; nothing executed. Acceptance criteria are fixed here to prevent post-hoc goalpost-moving; the build
phase reports against THESE criteria, including an honest "fusion did not beat the best single source" if that
is the result.
