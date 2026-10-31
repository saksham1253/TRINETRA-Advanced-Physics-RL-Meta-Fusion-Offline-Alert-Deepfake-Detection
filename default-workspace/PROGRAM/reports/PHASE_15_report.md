# PHASE_15_report — WS5 REINFORCEMENT-LEARNING DESIGN (DESIGN / ON-PAPER)

Phase P15 (MASTER_PROMPT L671). Status: COMPLETE to gate (continuous mode). Nothing trained/simulated
(Rule 16). Rule 19: RL output is ADVISORY decision-support for a human dispatcher — never autonomous control.

## Objective
Design the RL component (environment, reward, training plan within the later Kaggle budget), with the
discipline that RL must beat strong non-RL baselines to earn a place.

## Deliverables
- ws5_rl/rl_design.md — use-cases (evacuation routing/allocation, alert sequencing, sensor control) admitted
  only if they beat MILP/optimizer baselines; reward design + anti-reward-hacking governance; safe/constrained
  RL as a prerequisite (minimum-peak-harm fallback, at-all-times safety, structurally-guaranteed constraints);
  offline-first small-compute learning regime; MARL where genuinely multi-agent; advisory interfaces (Rule 19).
- ws5_rl/environment_spec.md — REUSE-over-BUILD: Ctrl-CWM / cinemere crowd + PyroStack / FireGen fire + FLARE
  behavior; build a thin Gymnasium/PettingZoo JAX-vectorized wrapper (Crazyflow/BluffJAX patterns).
- ws5_rl/rl_evaluation_plan.md — PRE-REGISTERED acceptance (beat best non-RL baseline cross-scenario by a
  margin exceeding seed/trial variance; rliable aggregate metrics; worst-case safety-violation reporting;
  reward-integrity check) + ablations + stress tests.
- PROGRAM/sota/P15_sota_scan.md — SOTA + process targets.

## Quota (15 required → MET)
21 NEW primary arXiv (ABS): PIER/GREAT-EER/RL-DMF/leader-follower/FLARE; PyroStack/FireGen/Ctrl-CWM;
envelope-sampling/verifier-of-verifier; FAITH/unified-Bellman/constrained-MARL; football MARL; higher-order-
supervision/DaCe-DT/Q-shaped-options/VAN-Flow; Crazyflow/BluffJAX; PAMORT. 0 FT; running body-level deep FT
NEW unchanged at 100.

## Key decisions (evidence-backed)
RL earns its place only vs strong non-RL baselines (2602.14676 MILP bound; naive-RL-underperforms 2509.19972);
offline-first from logs on small compute (2603.17319, 2610.11085); safe/constrained prerequisite with
minimum-peak-harm fallback (2610.12432) + at-all-times safety (2610.12420) + structural constraints
(2610.11739); low-variance risk posture (2610.07899); reward integrity via anchor-guarded verifier (2610.11464,
2610.11281); rliable evaluation imported (methodology gap).

## Honesty & limits
Design/on-paper only; nothing trained. All numbers source-reported on non-disaster benchmarks (transfer
hypotheses). No off-the-shelf disaster-evac env (build gap). Honest default is a NON-RL optimizer.

## Gate
PROGRAM/gate_messages/PHASE_15_gate.md. Auto-proceeding to P16 (robustness) — reader (23 papers) ALREADY
PIPELINED and in hand.
