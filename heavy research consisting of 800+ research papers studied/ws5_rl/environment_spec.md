# ws5_rl/environment_spec.md — RL environment specification (P15, WS5)

Phase P15 · RESEARCH-ONLY, on-paper. Nothing built/simulated (Rule 16). Specifies the environment the later
build would construct; REUSE-over-BUILD. All sources SOURCE-REPORTED.

## 1. Reuse-vs-build decision (from the P15 reading)
| Component | Reuse candidate | Source | Note |
|-----------|-----------------|--------|------|
| Crowd dynamics | Ctrl-CWM controllable crowd world-model | 2610.09438 | model-based, operator-injectable runtime costs; verify license/code |
| Crowd (small-scale) | cinemere/evacuation (Vicsek leader-follower) | 2509.19972 | open-source; limited to leader-guidance framing |
| Human evacuate/stay behavior | FLARE | 2502.17701 | inject realistic behavior; code public |
| Fire-spread data/benchmark | PyroStack (6994 fires, hourly, 12-h progression) | 2609.36315 | validation data / non-RL baseline; wrap into an env |
| Fire-spread stochastic sim | FireGen (Monte-Carlo) | 2610.07431 | scenario generator / stochastic baseline |
| Vectorization engineering | Crazyflow (JAX), BluffJAX | 2610.08225, 2610.07686 | not disaster-specific; copy GPU/JAX env patterns for many-seed studies |
BUILD (gap): a thin Gymnasium/PettingZoo wrapper unifying the above — no off-the-shelf disaster-evacuation env
surfaced in the throttled search.

## 2. Env interface (spec only)
- STATE: fire-front estimate + uncertainty (from fire env), population/crowd distribution, network/road graph,
  resource positions, sensor/camera coverage, time. Partial observability (imperfect sensor coverage) is the
  realistic case (imperfect-information framing, 2610.07686).
- ACTION (advisory): proposed routing/allocation/dispatch options — surfaced to a human, NOT actuated.
- REWARD: time-to-safety / people-evacuated / coverage, with HARD safety-constraint terms; low-variance
  preferred (2610.07899); proxy reward auditable + recalibratable (2610.11281).
- TERMINATION: evacuation complete / timeout / infeasible (triggers minimum-peak-harm fallback, 2610.12432).

## 3. Fidelity & sim-to-real caution
Domain randomization + explicit sim-to-real plan (2610.05819 shows zero-shot transfer is possible but must be
tested). Treat all simulator outputs as hypotheses; validate against PyroStack real progression (2609.36315)
and real evacuation behavior (FLARE 2502.17701) before trusting any policy.

## 4. Honesty
Specification only; no env built. Licenses/code availability of reuse candidates to be VERIFIED at build.
