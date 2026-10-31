# ws5_rl/literature_map.md — RL design literature map (WS5)

Phase P15. HONEST: all ABS; IDs/years arXiv-ID-derived + subagent-reported (reader 4ab11480; 12 fetches), NOT
re-fetched (residual risk, §0.5); all numbers SOURCE-REPORTED (Rule 16). Backs ws5_rl/{rl_design,
environment_spec, rl_evaluation_plan}.md + P15 SOTA scan. Running body-level deep FT NEW total UNCHANGED at
100 (ABS breadth).

## P15 section — 21 NEW primary arXiv

### T1 RL / optimization for evacuation, emergency response, resource allocation
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2603.17319 | PIER physics-informed offline RL (maritime routing) | offline RL from logs + decoupled post-hoc safety shield, no online sim; 9× fewer catastrophic fuel cases (4.8%→0.5%), CI [2.9%,15.7%], forecast-independent vs A*. Authors claim transfer to wildfire evacuation. |
| 2602.14676 | GREAT-EER graph-RL bus evacuation | NP-hard Bus Evacuation Orienteering; deep-RL+graph, routes in fractions of a second, MILP optimality bound. The non-RL baseline/bound WS5 must beat; fast enough for a human dispatcher. |
| 2601.06664 | RL-DMF evacuation-traffic prediction | RL feature-selection + dynamic multi-graph fusion; 95% next-1h (RMSE 293.9) / 90% next-6h on unseen Hurricane Milton. RL as advisory decision-support, not control. |
| 2509.19972 | Leader-follower crowd control | single RL "leader" + artificial forces (Vicsek); naive RL underperforms, hybrid robust. CAUTION: physics-hybrid beats naive RL; open env (cinemere/evacuation). |
| 2502.17701 | FLARE behavioral evacuation LLM+RL | behavioral-theory + CoT + memory RL predicts evacuate/stay; +20.47% over theory models, cross-event. Human-behavior realism for the environment. |

### T2 fire-spread & crowd simulators / environments
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2609.36315 | PyroStack dataset | 6994 US wildfires 2012-24, multi-band hourly, 12-h fire progression. Reuse as validation data + non-RL physics baseline; wrap into a fire-spread env. |
| 2610.07431 | FireGen Monte-Carlo wildfire sim | point-process + ellipse perimeters + lognormal burned area. Stochastic scenario generator / non-RL baseline. |
| 2610.09438 | Ctrl-CWM controllable crowd world-model | encoder+actor+critic+planner; runtime user costs WITHOUT retraining; beats SOTA on crowd-realism/collision. Reusable operator-controllable crowd sim (model-based, advisory-fit). |

### T3 reward design & reward hacking
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2610.11281 | Envelope sampling vs reward hacking | recalibrate surrogate reward with few ground-truth labels, bounded post-trained regret; mitigates hacking where base-sample recalibration fails. Audit evacuation reward proxies with scarce expert labels. |
| 2610.11464 | Who Verifies the Verifier | inspectable deterministic detectors + anchored reference set + outer judge; KEY: downstream task score CANNOT certify a verifier (remove anchors → vacuous always-pass). Human-auditable reward governance. |

### T4 safe & constrained RL
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2610.12432 | FAITH feasibility-aware safety filter | model-free safety filter; minimum-predicted-peak-harm when no safe action; 99.95% safety (humanoid) retaining 97% return; real Unitree G1. The infeasible-emergency fallback behavior. |
| 2610.12420 | Unified safety-critical Bellman operator | joint performance+safety value, two-timescale; near-zero test-time violations. At-all-times (not on-average) safety target. |
| 2610.11739 | Distributed constrained MARL (6G) | guarantee hard constraint structurally in phase 1, MARL optimizes rest; +40% throughput, 100% constraint satisfaction, beats optimization+learning baselines. Resource allocation with hard safety/coverage constraints. |

### T5 multi-agent RL
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2610.05961 | Interpretable football action valuation | MPE-inspired, successor-feature + linear reward-weight Q decomposition; context-sensitive per-player value vs independent-RL baseline. Interpretable per-responder contribution for a human overseer. |

### T6 model-based & offline RL (small compute)
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2610.11175 | Higher-order action supervision | plug-in first-order action-dynamics loss w/ guarantees; OOD gains low-data on D4RL/OGBench. Lightweight offline-RL robustness for small-compute logged-data regime. |
| 2610.11085 | DaCe-DT data-centric offline multi-task | prompt masking + retrieval + return calibration; +11.73%/+13.34% (optimal/suboptimal data). Learn from messy heterogeneous emergency logs. |
| 2610.12135 | Q-Shaped Options (HRL) | per-level value/Q/policy; learns control-relevant action abstraction; non-zero where all baselines fail on offline goal-conditioned. Temporal abstraction for long-horizon evacuation. |
| 2610.07899 | VAN-Flow variance-averse offline RL | distributional critic + variance-averse operator + flow-matching actor; largest gains in long-horizon/high-variance (40+ tasks). Prefers RELIABLE low-variance actions — life-safety risk posture. |

### T7 GPU-accelerated / vectorized environments
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2610.08225 | Crazyflow (JAX) | differentiable JAX physics+control, order-of-magnitude speedups, "train deployable RL in seconds", degraded-feedback modeling. Template for a fast GPU-vectorized evacuation/sensor env on small compute. |
| 2610.07686 | BluffJAX | JAX imperfect-information games, hundreds of M samples/sec. GPU-vectorized env engineering patterns; imperfect-info fits partial sensor coverage. |

### T9 sim-to-real transfer & domain randomization
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2610.05819 | PAMORT multi-objective quadruped | preference-vector weighting locomotion vs stability, online preference adaptation; real Go2 zero-shot 0.850 vs 0.675 baseline. Sim-to-real + human-tunable safety-vs-task trade-off. |

### Synthesis (P15) — see rl_design.md
1. SIMULATORS: REUSE Ctrl-CWM / cinemere (crowd) + PyroStack / FireGen (fire) + FLARE (behavior); BUILD a thin
   Gymnasium/PettingZoo JAX-vectorized wrapper (Crazyflow/BluffJAX patterns). No off-the-shelf disaster-evac
   env (GAP).
2. SAMPLE-EFFICIENT: offline-first (PIER, DaCe-DT) + higher-order supervision + hierarchical options +
   variance-averse — matches small-compute/no-live-training reality.
3. SAFE/REWARD: FAITH minimum-peak-harm fallback + unified-Bellman at-all-times safety + structurally-
   guaranteed constrained MARL + anchor-guarded reward verifier + envelope-sampling recalibration.
4. EVALUATION: bootstrap CIs + rliable (IQM/performance profiles) — WS5 imports rliable (RL-emergency
   literature under-adopts it); explicit non-RL baseline contrasts; worst-case (not average) safety reporting.

## Tally (P15)
P15 NEW quota = 21 primary arXiv (≥15 MET). Depth all ABS (0 FT) — running body-level deep FT NEW total
UNCHANGED at 100.
