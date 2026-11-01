# PROGRAM/sota/P15_sota_scan.md — RL for emergency response SOTA scan (WS5)

Phase P15 · RESEARCH-ONLY. MASTER_PROMPT P15 task 1. SOTA + targets. All numbers SOURCE-REPORTED (Rule 16);
detail + IDs in ws5_rl/literature_map.md P15 section. No own-system claim.

## 1. SOTA landscape (how RL-for-emergency-response is done now)
- EVACUATION / ROUTING / ALLOCATION: GREAT-EER deep-RL+graph bus-evacuation, near-optimal in fractions of a
  second with an MILP optimality bound (2602.14676); PIER physics-informed OFFLINE RL + post-hoc safety
  shield, source-reported 9× fewer catastrophic cases, CI [2.9%,15.7%] (2603.17319); RL-DMF RL-guided feature
  selection for evacuation-traffic prediction, 95%/90% next-1h/6h on unseen Hurricane Milton (2601.06664);
  leader-follower crowd control where naive RL underperforms a physics hybrid (2509.19972); FLARE behavioral
  evacuate/stay prediction +20.47% over theory models (2502.17701).
- SIMULATORS/ENVS: PyroStack fire-spread benchmark (2609.36315); FireGen Monte-Carlo wildfire sim (2610.07431);
  Ctrl-CWM controllable crowd world-model (2610.09438); Crazyflow/BluffJAX JAX-vectorized env patterns
  (2610.08225, 2610.07686).
- SAFE/CONSTRAINED: FAITH safety filter w/ minimum-peak-harm fallback, 99.95% safety / 97% return (2610.12432);
  unified performance+safety Bellman, near-zero test-time violations (2610.12420); constrained MARL, 100%
  constraint satisfaction (2610.11739).
- REWARD HACKING: envelope sampling recalibration with bounded regret (2610.11281); anchor-guarded inspectable
  verifier — downstream score can't certify a reward (2610.11464).
- SAMPLE-EFFICIENT (small compute): DaCe-DT offline multi-task +11.73%/+13.34% (2610.11085); higher-order
  action supervision low-data OOD gains (2610.11175); Q-shaped options for long-horizon (2610.12135); variance-
  averse offline RL (2610.07899); PAMORT sim-to-real zero-shot 0.850 vs 0.675 (2610.05819).

## 2. TARGETS section (process targets, NOT results, Rule 16)
- RL admitted ONLY if it beats the best strong NON-RL baseline (MILP/optimizer) on a cross-scenario metric by
  a margin exceeding seed/trial variance (rl_evaluation_plan §1).
- Offline-first learning on logged data; no live training; small-compute recipes.
- Safe/constrained with minimum-peak-harm fallback and at-all-times safety target; worst-case violation
  reporting.
- rliable-style evaluation (IQM, performance profiles, many seeds + CIs) imported explicitly.
- Reward integrity via anchor-guarded inspectable verifier.
- Advisory-only interface (Rule 19); human dispatcher in the loop; no actuation.

## 3. Honesty & gaps
All source-reported on driving/robotics/LLM benchmarks, NOT a disaster system → transfer hypotheses. No
off-the-shelf Gymnasium/PettingZoo disaster-evacuation env (build gap). rliable protocol under-adopted in the
RL-emergency literature → WS5 imports it. The honest default remains a NON-RL optimizer.
