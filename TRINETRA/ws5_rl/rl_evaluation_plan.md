# ws5_rl/rl_evaluation_plan.md — RL evaluation & acceptance plan (P15, WS5)

Phase P15 · RESEARCH-ONLY, pre-registered. Nothing run (Rule 16). Governs whether the RL component earns a
place in the build.

## 1. PRE-REGISTERED ACCEPTANCE (decided NOW)
RL is admitted to the build IFF ALL hold:
- PRIMARY: the RL policy beats the BEST STRONG NON-RL baseline (MILP/optimization/greedy/statistical — e.g.
  the GREAT-EER MILP bound 2602.14676) on a pre-registered cross-SCENARIO metric (time-to-safety / people-
  evacuated at matched resources), by a margin exceeding seed/trial variance.
- STATISTICS: report ≥N seeds (N≥5, pinned at build) with confidence intervals and rliable-style aggregate
  metrics (IQM, performance profiles, stratified bootstrap) — imported explicitly because the P15 reading
  shows few RL papers adopt rliable (methodology GAP). No single-seed headline numbers.
- SAFETY: WORST-CASE (not average) hard-constraint violation rate reported; the safety filter + minimum-peak-
  harm fallback (2610.12432) demonstrably bounds harm under infeasible scenarios; at-all-times safety target
  (2610.12420).
- REWARD INTEGRITY: reward hacking checked with an anchor-guarded inspectable verifier (2610.11464); downstream
  task score alone does NOT certify the reward.
If RL does NOT clear this bar, the honest outcome is "use the non-RL optimizer" — recorded plainly.

## 2. Ablations / comparisons
RL vs best non-RL optimizer (headline); offline vs model-based; with vs without safety filter; with vs without
hierarchical options; single-objective vs multi-objective preference control; sensitivity to simulator
fidelity (sim-to-real gap).

## 3. Stress tests
Partial observability / degraded sensor coverage; distribution shift (new map/scenario); rare high-consequence
events; adversarial / spoofed inputs feeding the state; reward-proxy miscalibration.

## 4. Rule 19
Evaluate the ADVISORY interface: confirm RL outputs are ranked options to a human, never actuation; confirm
the human-override and the explicit minimum-peak-harm fallback paths.

## 5. Honesty
Plan only; nothing executed. Acceptance fixed here to prevent post-hoc goalpost-moving; an honest "non-RL
optimizer wins" is an acceptable, reportable outcome.
