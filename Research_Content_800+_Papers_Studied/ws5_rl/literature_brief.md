# WS5 — RL ALARM POLICY — literature brief (P4, 2026-10-07)
Owner phase: P15. Scope: decision/alarm policy, offline RL, reward shaping, safety shield, OPE.

## Most relevant papers
- **2606.21773** DFL review — a well-posed decision loss can beat a bigger stack ("better prediction ≠ better
  decision"); SPO/surrogate-loss taxonomy. → staged policy, DFL first.
- **2107.11003** Model Selection for Offline RL (MLHC 2021, code: MLD3/OfflineRL_ModelSelection) — use FQE/OPE
  to RANK policies offline; iterative RL ONLY if OPE is feasible. Sepsis = safety-critical analogue.
- **2608.08158** Dynamic reward-shaping framework — PBRS preserves the optimal policy iff the auxiliary term
  is the discounted diff of a time-invariant potential; §2.7 limits under episodic/partial-obs/multi-agent.
- **2610.03369** RL eval hygiene — ≥100 seeds + tail/dispersion + two-baseline rule.
- **2609.34041** VLM-Safe-RL caveat — a catastrophe-rate drop with NO anticipation evidence = hollow safety.
- **2110.15332** Proximal RL / POMDP OPE — confounding caveat for offline evaluation.
- Shield: Alshiekh 1708.08611 (reactive shield); unrealizability check 2507.23603; predictive/latent shields.

## Key claims → references
- Staged policy: fixed threshold → one-step offline RL → iterative only if OPE-feasible. → DC-10 (C-11).
- Reward shaping stays potential-based and time-invariant (or prove the exception); alarm MDP is partially
  observed. → DC-11 (2608.08158 §2.7).
- Probe anticipation/lead-time explicitly, not just final catastrophe count. → DC-16 (2609.34041).
- Reward must cost FA > a flat penalty (cry-wolf). → DC-18 (THIN).
- Eval: ≥100 seeds + tail/dispersion + two baselines (RB-13). → DC (eval hygiene).

## Open questions
- Is OPE trustworthy on our few disaster episodes? (FM-08) — gate any RL step on it.
- Shield realizability under conflicting FS/tilt/rain/GLOF rules (FM-05) — check before deploy.
- Human-compliance term in the reward (C-12 thin) — source in P13/P15.
