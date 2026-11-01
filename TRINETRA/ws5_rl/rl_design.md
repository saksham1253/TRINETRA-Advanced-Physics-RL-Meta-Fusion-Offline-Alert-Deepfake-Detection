# ws5_rl/rl_design.md — reinforcement-learning component design (P15, WS5)

Phase P15 · RESEARCH-ONLY, on-paper. MASTER_PROMPT P15. Nothing is trained or simulated now (Rule 16). Rule
19: any RL output is ADVISORY decision-support for a human dispatcher — NEVER autonomous control of
evacuation, alerts, or resources. Every design choice traces to a SOURCE-REPORTED paper in the P15 reading
(ws5_rl/literature_map.md P15 section / PROGRAM/sota/P15_sota_scan.md).

## 0. Scope & the honest baseline question
Candidate RL use-cases: (a) evacuation ROUTING / resource allocation, (b) alert-dispatch sequencing, (c)
active sensor/camera control. GOVERNING DISCIPLINE: RL is admitted ONLY if it beats STRONG NON-RL baselines
(MILP/optimization/greedy/statistical) on a pre-registered metric — the RL-for-evacuation literature itself
benchmarks against near-optimal non-RL methods (GREAT-EER vs MILP bound 2602.14676; RL-DMF vs SOTA predictors
2601.06664; constrained-MARL vs optimization 2610.11739), and naive RL can UNDERPERFORM a physics-hybrid
(2509.19972). The default assumption is "use the optimizer unless RL demonstrably wins".

## 1. Where RL plausibly adds value (evidence-backed)
- EVACUATION ROUTING under uncertainty/dynamics where re-solving a MILP each step is too slow: GREAT-EER gives
  near-optimal routes in fractions of a second with an MILP optimality bound (2602.14676) — RL/graph-learning
  as a FAST APPROXIMATION to an optimizer the human can still audit.
- DECISION-SUPPORT / interpretability layer rather than direct control: RL-guided feature selection for
  evacuation-traffic prediction (2601.06664); interpretable per-agent valuation (2610.05961). Advisory-fit.
- HUMAN-BEHAVIOR realism in the environment: FLARE behavioral evacuate/stay prediction (2502.17701) to make
  any simulator realistic.

## 2. Environment (design; see environment_spec.md)
REUSE-over-BUILD per the reading: crowd dynamics via Ctrl-CWM controllable crowd world-model (2610.09438) or
the open cinemere/evacuation Vicsek env (2509.19972); fire via PyroStack benchmark data (2609.36315) +
FireGen stochastic simulator (2610.07431) wrapped as a fire-spread env; inject realistic human behavior with
FLARE (2502.17701). BUILD only a thin Gymnasium/PettingZoo wrapper using Crazyflow/BluffJAX-style JAX
vectorization (2610.08225, 2610.07686) for many-seed studies on small compute. HONEST GAP: no off-the-shelf
Gymnasium/PettingZoo disaster-evacuation env surfaced — the wrapper is a build task.

## 3. Reward design & reward hacking (safety-critical)
- Design reward proxies experts can AUDIT; recalibrate cheap/proxy rewards with scarce expert labels via
  envelope sampling with bounded regret (2610.11281).
- Anti-reward-hacking governance: inspectable deterministic drawback-detectors + anchored reference set + outer
  judge; KEY WARNING — a downstream task score CANNOT certify a reward/verifier (anchor guards essential, else
  the verifier collapses to always-pass) (2610.11464).
- Risk posture: prefer RELIABLE low-variance actions over lucky high-return ones (variance-averse offline RL,
  2610.07899) — the correct posture for life-safety advice.

## 4. Safe / constrained RL (prerequisite for even advisory use)
- Safety filter with a MINIMUM-PREDICTED-PEAK-HARM fallback when no action is safe (FAITH 2610.12432, source-
  reported 99.95% safety retaining 97% return) — exactly the behavior under an infeasible emergency.
- At-all-times (not on-average) safety via a unified performance+safety Bellman operator (2610.12420).
- Structurally GUARANTEE hard constraints first, optimize the rest (constrained MARL 2610.11739, source-
  reported 100% constraint satisfaction) — for resource allocation with hard coverage/safety constraints.
- Online safety-vs-task trade-off tuning a human overseer can set (multi-objective preference vector,
  2610.05819).

## 5. Learning regime (small compute, no live training)
OFFLINE-first from logs (no online simulator needed): physics-calibrated offline RL + decoupled post-hoc
safety shield (PIER 2603.17319); data-centric offline multi-task for messy heterogeneous logs (DaCe-DT
2610.11085); higher-order action supervision for low-data OOD robustness (2610.11175); hierarchical options
for long-horizon evacuation (2610.12135); model-based planning that adapts at runtime WITHOUT retraining
(Ctrl-CWM 2610.09438).

## 6. Multi-agent (if used)
MARL only where genuinely multi-agent (many responders/zones); use interpretable reward-decomposed valuation
for per-agent explanation to the overseer (2610.05961); guarantee hard constraints structurally to avoid
action-space blow-up (2610.11739).

## 7. Interfaces (Rule 19)
RL emits RANKED ADVISORY options + expected outcome + uncertainty + the constraints each satisfies/violates,
to a HUMAN dispatcher; it never actuates. Fused detection confidence (P14) and alert policy (P12) gate whether
an RL recommendation is even surfaced. The safety filter's minimum-peak-harm fallback is shown explicitly.

## 8. Evaluation plan → see rl_evaluation_plan.md
Pre-register: beat strong NON-RL baselines on a cross-scenario metric; many seeds + confidence intervals +
rliable-style aggregate metrics (IQM, performance profiles) — the reading's methodology GAP is that few papers
adopt rliable, so WS5 imports it explicitly; report worst-case (not average) safety-constraint violations.

## 9. Honesty & limits
Design/on-paper only; nothing trained. All numbers source-reported on driving/robotics/LLM benchmarks, NOT a
disaster system → transfer hypotheses to re-test. The honest default is a NON-RL optimizer; RL must earn its
place against it. "No off-the-shelf disaster-evacuation RL env" is a documented build gap.
