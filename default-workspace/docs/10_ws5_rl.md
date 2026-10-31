# 10 — WS5: Offline-RL Advisory Alarm Policy, OPE Admission Gate, and Safety Shield

> Workstream scheme (per `_CANON.md §3`): this is the **user-frame WS5 = RL**, backed by code packages
> `trinetra/src/trinetra/ws5_fusion_rl/rl.py` (numpy core) and `trinetra/src/trinetra/deep/offline_rl.py`
> (PyTorch Model 6), with the Kaggle trainer `trinetra/kaggle/train_offline_rl.py`. The internal research
> artifacts live in `ws5_rl/` (phase P15). Do not confuse this WS5 with the *internal* "WS5 fusion" that
> `_CANON.md` also lists under the WS1 doc-frame — the package name `ws5_fusion_rl` carries both the fusion
> head and the RL policy, which is why the folder is dual-named.

> **Reality check first (read before any number below).** No TRINETRA RL policy has been trained, and no RL
> logs have been collected or downloaded. Per `_CANON.md §0`/`§2`: the numpy baseline + OPE gate in `rl.py`
> runs and is covered by the 128-test suite `[CONFIRMED]`; `deep/offline_rl.py` and the Kaggle trainer are
> **`py_compile`-clean only — never executed on a GPU here** `[CONFIRMED` that it compiles; the *training*
> is `not measured]`. Every quantitative claim about an algorithm in this chapter is **source-reported** from
> a cited paper on *that paper's own* (mostly D4RL / robotics / driving) benchmark — never a TRINETRA result.
> Where you expect a TRINETRA number, the honest answer is **"not measured."**

---

## 10.1 The problem — sequential alarm/escalation/maintenance under cost asymmetry

TRINETRA's decision layer must repeatedly answer a small but high-stakes question: given the current fused
hazard picture, **what alarm level do we advise the human dispatcher to consider** — and when do we escalate,
hold, or schedule maintenance? This is a *sequential decision problem under a sharply asymmetric cost model*.
A missed hazard in a life-safety mountain-disaster setting is catastrophic; a false alarm is costly
(cry-wolf fatigue, wasted dispatch) but recoverable. The canonical cost ratio carried by this project is
`C_FA = 5`, `C_miss = 100` (a missed event is ~20× worse than a false alarm), which fixes the optimal
alarm operating point at the probability threshold

```
p* = C_FA / (C_FA + C_miss) = 5 / 105 ≈ 0.0476
```

(`_CANON.md §4`). That same `0.0476` is the default threshold of the implemented `RuleBaselinePolicy`
(`rl.py:22`), so the rule baseline and the cost model are deliberately the *same* operating point expressed
two ways. The teaching point: the decision is not "classify risk accurately" but "**act under a loss where
the two error types are priced 20:1**," and a policy that is merely more accurate can still be worse if it
trades a cheap false alarm for an expensive miss (`FEATURES.md`/`FINAL_REPORT.md`: *"better prediction ≠
better decision,"* decision-focused-learning review 2606.21773).

**Why reinforcement learning at all, and why *offline*?** Three forces push toward RL and simultaneously
forbid the usual way of doing it:

1. **The decision is sequential and stateful.** Alarm/escalation/maintenance choices interact over time
   (escalating now changes what "hold" means later; deferred maintenance degrades future sensing). A policy
   that reasons about downstream consequences, not just the instantaneous label, is the natural object.
2. **We cannot explore in a live life-safety system.** Online RL *learns by trying actions and observing
   outcomes* — ethically and legally impossible when the "environment" is a populated valley. You cannot
   issue a real alarm to see what reward you get. This is the defining constraint of the whole workstream.
3. **We only have logged / simulated data.** The honest regime is therefore **offline (batch) RL**: learn a
   policy *purely* from a fixed dataset of `(state, action, reward, next_state)` tuples produced by some
   logging/behavior policy, with **no new interaction**. The canonical hazard of this regime is
   *distributional shift* — the learned policy wants to visit `(state, action)` pairs the logging policy
   rarely took, where bootstrapped value estimates are unreliable (offline-RL survey, Levine et al.
   2005.01643). Everything downstream (conservatism, the OPE gate, the shield) exists to tame that hazard.

The governing posture, carried verbatim from the canon and the research program, is **Rule 19: the RL output
is ADVISORY — ranked options surfaced to a human dispatcher, NEVER actuation** (`_CANON.md §5`;
`ws5_rl/rl_design.md §0`,`§7`; `FINAL_REPORT.md §1 WS5`). The policy may *recommend*; a human alone decides on
public dissemination.

---

## 10.2 The environment / MDP design — and the explicit BUILD GAP

### 10.2.1 The MDP as specified (design only — nothing simulated)

`ws5_rl/environment_spec.md` and `rl_design.md` specify, on paper, the Markov decision process the later build
would construct. **Nothing here is built or simulated** (research Rule 16); it is a specification.

- **State** (`environment_spec.md §2`): the fused risk estimate **and its uncertainty**, plus — for the full
  evacuation framing — population/crowd distribution, road-network graph, resource positions, sensor/camera
  coverage, and time. Partial observability (imperfect sensor coverage) is treated as the *realistic* case,
  not an edge case. In the *implemented* code the state is an abstract `state_dim`-vector (default 16;
  `CQLConfig.state_dim=16` in `offline_rl.py:26`) whose columns are the fused-risk / uncertainty / resource /
  time features — the code does not hard-code their semantics, it consumes whatever the logged dataset
  provides (`RLTransitionDataset`, `datamodules.py:99`).
- **Actions.** Two action framings coexist, and the gap between them is worth understanding:
  - The *implemented Model-6* action set is **discrete `{HOLD, WATCH, ALARM}`** — three alarm/escalation
    levels (`offline_rl.py:21`, `ACTIONS`). Ordering them `HOLD < WATCH < ALARM` is what makes the shield
    (10.5) a *monotone* "raise toward safety" operation.
  - The *numpy baseline* `RuleBaselinePolicy.act` is **binary** (`0 = hold`, `1 = alarm`; `rl.py:25-26`).
    `[LIKELY]` the 3-level CQL policy and the binary rule baseline are reconciled by mapping
    `{HOLD}→0, {WATCH,ALARM}→1` at the OPE comparison, but the code does not state the mapping explicitly —
    flagged as an open consistency point (see 10.9).
  - The *full research framing* additionally contemplates routing/allocation/dispatch and
    sensor/camera-control actions (`rl_design.md §0`), but those are the evacuation-env ambition, not the
    implemented alarm policy.
- **Reward.** Derived from the **cost-loss model** — penalize misses far more than false alarms, with hard
  safety-constraint terms and a *low-variance* preference (`environment_spec.md §2`; `rl_design.md §3`,
  variance-averse posture 2610.07899). The reward must price false alarms above a flat penalty to avoid
  cry-wolf (literature brief DC-18). In the implemented trainer the reward is simply the logged `r` column
  (`RLTransitionDataset.r`); the cost-loss shaping is a *data-generation* responsibility, not something the
  Q-net invents.
- **Termination:** evacuation complete / timeout / infeasible — where "infeasible" triggers a
  **minimum-predicted-peak-harm fallback** (FAITH 2610.12432) rather than undefined behavior.

### 10.2.2 The BUILD GAP (explicit, load-bearing)

**There is no off-the-shelf disaster-evacuation RL environment.** This is stated three times across the
artifacts and must not be softened: `environment_spec.md §1` ("no off-the-shelf disaster-evacuation env
surfaced in the throttled search"), `rl_design.md §2` ("HONEST GAP"), and `FINAL_REPORT.md §1 WS5` /
`§13` ("Build the disaster-evacuation RL environment (no off-the-shelf env exists — BUILD GAP)"). The
research position is **REUSE-over-BUILD**: wrap existing components rather than author a simulator from
scratch — crowd dynamics (Ctrl-CWM 2610.09438, or the open cinemere/evacuation Vicsek env 2509.19972),
fire-spread (PyroStack data 2609.36315 + FireGen stochastic sim 2610.07431), human evacuate/stay behavior
(FLARE 2502.17701), and JAX vectorization patterns (Crazyflow 2610.08225, BluffJAX 2610.07686) — with the
**only genuine build task** being a thin Gymnasium/PettingZoo wrapper unifying them. Every reuse candidate's
license and code availability is **`[LIKELY]` / to-be-VERIFIED at build**, not confirmed. Simulator outputs
are to be treated as *hypotheses* and validated against real fire progression (PyroStack) and real evacuation
behavior (FLARE) before any policy is trusted (`environment_spec.md §3`, sim-to-real caution 2610.05819).

---

## 10.3 The implemented policy — code, layer by layer

### 10.3.1 `deep/offline_rl.py` — Conservative Q-Learning (Model 6, PyTorch)

The implemented learner is **discrete-action Conservative Q-Learning (CQL)** (`offline_rl.py`, module
docstring; algorithm from Kumar et al. 2006.04779). It is `py_compile`-clean and **never GPU-trained here**
`[CONFIRMED]`. Walking the code as written:

- **`CQLConfig`** (`:24-31`): `state_dim=16`, `n_actions=3`, `hidden=(256,256)`, **`gamma=0.0`**,
  `cql_alpha=1.0`, `tau=0.005`. The default `gamma=0.0` is the design's single most important choice: it
  **collapses the MDP to a one-step contextual bandit** (docstring: *"Set gamma=0 for the one-step
  contextual-bandit variant (recommended when transitions are weakly Markov)"*). This is how the code
  reconciles "we implemented CQL" with the literature's "prefer one-step on small, narrow data" (10.5) —
  CQL *with γ=0* is a conservative one-step learner; `γ>0` turns on sequential bootstrapping only if the data
  justify it.
- **`QNet`** (`:34-40`): a single `MLP([state_dim, 256, 256, n_actions], norm=True)` — the Q-head maps a
  state vector to one Q-value per action. This is a **tiny network** (state × two 256-wide layers × 3
  actions); its size is the justification for single-GPU training (10.6).
- **`CQLPolicy`** (`:43-86`): holds an `online` QNet and a frozen `target` QNet (Polyak-averaged).
  - **`cql_loss`** (`:55-65`) is the training objective and the heart of the method:
    - `q_sa = Q(s)[a]` — the Q-value of the action actually taken in the data.
    - `target = r + γ·(1−done)·max_a' Q_target(s_next, a')` — the standard Bellman backup, computed under
      `no_grad` from the target net; with `γ=0` this is just the immediate reward `r`.
    - `bellman = MSE(q_sa, target)` — fit the taken-action value.
    - `conservative = mean(logsumexp_a Q(s,a) − q_sa)` — **the CQL penalty**. `logsumexp` is a soft-max over
      *all* actions; subtracting the data action's value and pushing the whole term down forces Q to be
      *low on out-of-distribution actions* and *relatively higher on observed actions*. This is exactly
      Kumar et al.'s mechanism for a **lower-bounded, conservative** Q that will not hallucinate value for a
      never-observed alarm action in a rare disaster state (`2006.04779` note, "Relevance to us").
    - `loss = bellman + cql_alpha · conservative`.
  - **`polyak_update`** (`:67-70`): `target ← (1−τ)·target + τ·online`, the slow target-net tracking that
    stabilizes bootstrapping.
  - **`act`** (`:72-81`): greedy `argmax_a Q(s)` **then raised to the shield floor** via
    `torch.maximum(greedy, shield_floor_idx)` — this is the post-posed safety shield in code (10.5).
  - **`action_probs`** (`:83-86`): `softmax(Q(s)/temperature)` — a *stochastic* target policy, needed so the
    OPE importance ratios in `rl.py` are well defined.

### 10.3.2 `ws5_fusion_rl/rl.py` — numpy baseline, policy interface, OPE, admission gate

This is the **runnable, test-covered numpy core** `[CONFIRMED]` (no torch dependency). It deliberately
implements *everything except the learned network itself*, so the honest fallback and the admission logic
work even in an environment with only numpy.

- **`RuleBaselinePolicy`** (`:19-26`): "alarm iff fused risk ≥ `threshold`," default `threshold=0.0476`
  (= `p*`). This is the **fixed-threshold policy a learned policy must BEAT**, and the fail-safe the system
  reverts to. Teaching point: the comparator is not a strawman — it is the Bayes-optimal threshold for the
  stated cost ratio, so beating it is a genuine bar.
- **`OfflineRLPolicy`** (`:29-39`): an *interface stub*. `fit()` raises `MissingDependency` with the message
  that the learned algo *"needs d3rlpy+torch (not installed). Until trained+OPE-admitted, the system uses
  RuleBaselinePolicy (Rule 19 fail-safe)."* This is intentional: in the numpy sandbox there is no trained
  policy, so the code *forces* the fail-safe rather than silently pretending.
- **`wis_value(behavior_probs, target_probs, rewards)`** (`:42-54`): **Weighted Importance Sampling** value
  estimate for one-step (contextual-bandit) OPE. It forms ratios `w = clip(t/clip(b,1e-6,None), 0, 1e3)`,
  returns `value = Σ(w·r)/Σw` and the **effective sample size** `ess = (Σw)² / Σ(w²)`. The ratio clipping
  and the ESS are the honest-statistics guardrails: WIS is only as trustworthy as its weights are
  well-behaved.
- **`ope_feasible(behavior_probs, …)`** (`:57-65`): the **positivity + ESS gate**. Returns `False` if any
  logged action probability is below `min_prob=1e-2` (a *positivity violation* — the logging policy almost
  never took some action, so no amount of reweighting can estimate its value) or if the ESS falls below
  `min_ess_frac=0.1` of the sample count (the estimate rests on too few effective samples). This is the
  gate that makes OPE *refuse to answer* when it cannot answer honestly (ties research FM-08,
  `literature_brief.md`).
- **`ope_admission(...)` → `OPEVerdict`** (`:68-83`): the deploy gate. It computes the target value
  `v_t` (via `wis_value`), the baseline value `v_b = mean(baseline_rewards)`, checks `feasible`, and sets

  ```
  deploy_learned = feasible AND v_t >= v_b
  ```

  i.e. **deploy the learned policy only if OPE is feasible AND its estimated value is at least the
  baseline's.** Otherwise the verdict keeps the rule baseline. This is Rule 19's fail-safe compiled into a
  boolean.

### 10.3.3 `kaggle/train_offline_rl.py` — how the two halves meet

The trainer (`train_offline_rl.py`, 81 lines, `py_compile`-clean, **not GPU-run** `[CONFIRMED]`) wires the
PyTorch learner to the numpy gate: it builds `CQLPolicy` from the data's `state_dim`, trains with AdamW +
gradient clipping + `polyak_update` per step (default `gamma=0.0`, `epochs=50`, `batch=256`), saves
`offline_rl.pt`, then — crucially — runs the **same `ope_admission` from `ws5_fusion_rl`** on the learned
policy's `action_probs` against the logged behavior probabilities and realized rewards. The report JSON
records `deploy_learned`; its own note strings make the gate explicit: *"DEPLOY learned policy
(OPE-admitted); still shielded upward at inference"* vs *"KEEP RuleBaselinePolicy — OPE did not admit the
learned policy (Rule 19 fail-safe)."* The baseline rewards passed in are the **logged behavior policy's own
realized rewards** (`train_offline_rl.py:66`) — a conservative choice (10.9).

### 10.3.4 The post-posed hard shield (floor can only raise)

The shield is **post-posed** (Alshiekh et al. 1708.08611, Fig. 2): the learned policy picks an action
*normally*, and the shield **corrects it only upward toward safety**. In code this is one line —
`torch.maximum(greedy, shield_floor_idx)` in `CQLPolicy.act` (`offline_rl.py:79-81`) — and it is *monotone*:
because actions are ordered `HOLD(0) < WATCH(1) < ALARM(2)`, the shield can only **raise** the alarm level to
a physics/sensor-derived floor, **never lower it**. This is the formal expression of *"it can only be
overridden UPWARD toward safety, never used to silence a hazard"* (`offline_rl.py` docstring; `_CANON.md §4`
`level = max(conformal_level(risk, p*), shield_floor)`). The shield floor is set by hard physics predicates
(e.g. FS<1, tilt>5°/day, 24h-rain>150mm, GLOF signature — see the shielding note and chapter 06), which are
*independent of the learned model*, satisfying Rule 19's requirement for hard guardrails that do not depend
on a learned component. **Realizability caveat `[LIKELY]`:** `FEATURES.md` F-06 requires the shield to be
*realizability-checked* (2507.23603) — i.e. the conjunction of physics predicates must not be contradictory
(FM-05, conflicting FS/tilt/rain/GLOF rules). The numpy `rl.py` does not implement the shield object itself;
the shield is the `shield_floor_idx` argument + the physics layer (chapter 06). Flagged as a composition
point in 10.9.

---

## 10.4 The honest OPE / valuation protocol (deploy gate)

The *implemented* gate (10.3.2) is deliberately a **minimal one-step WIS + positivity/ESS** check — exactly
what is defensible in a numpy-only, no-trained-policy environment. The *pre-registered research-grade
valuation protocol* is broader and is specified in `TRINETRA_Workstreams.md` (WS2 evaluation task 4,
"Honest RL valuation") and `ws5_rl/rl_evaluation_plan.md`. It uses **real arXiv method references**, carried
exactly as named (these four are cited in `TRINETRA_Workstreams.md:53-56`; they have **no local paper note**,
so no numbers are attributed to them here — method names only):

- **Policy selection by BVFT** (Batch Value-Function Tournament, **arXiv 2110.14000**): choose among candidate
  policies *offline*, by a value-function tournament, rather than by online return — because we cannot tune
  online.
- **Risk evaluation by SCOPE-RL** (**arXiv 2311.18206**): report **CVaR@5% (worst-case tail)**, worst-case
  return, and the *full return distribution*, not just the mean — the correct posture when the tail is a
  mass-casualty event.
- **A one-step offline baseline reported alongside** (**arXiv 2106.08909**, Brandfonbrener et al.) and
  **arXiv 2206.02000** as the companion valuation reference.
- **Deploy-gate:** *"deploy only if the OPE lower bound ≥ rule baseline"* (`TRINETRA_Workstreams.md:55`) —
  the research statement of the same `v_t ≥ v_b` gate the code implements, strengthened to a *lower bound*.
- **Feedback-aware OPE** (**arXiv 2312.01530**, `TRINETRA_Workstreams.md:56`): model
  evacuation/alarm/maintenance *feedback* in the OPE, because the action changes the future data.

Supporting method anchors from the paper notes: use **FQE/OPE to RANK policies offline, iterate only if OPE
is feasible** (Model-Selection-for-Offline-RL 2107.11003, `literature_brief.md`); OPE is a *named open
problem* in the field (offline-RL survey 2005.01643), so the whole RL approach is **gated on OPE quality**,
not assumed to work. This valuation plumbing — BVFT selection, SCOPE-RL CVaR, one-step comparator,
feedback-aware OPE, lower-bound deploy gate — is **spec/plan only; `not measured`.**

---

## 10.5 Algorithm alternatives considered (evidence + decision)

The research program treated the offline-RL algorithm as an explicit comparison, **CR-03** (multi-stage/
iterative vs simple one-step), with source-reported evidence. All numbers below are the cited paper's own
results on *their* benchmarks (D4RL locomotion unless noted) — **not TRINETRA measurements**:

| Candidate | What it is | Source-reported evidence (that paper's benchmark) | Role here |
|-----------|-----------|---------------------------------------------------|-----------|
| **CQL** (2006.04779) | Conservative Q, lower-bounds OOD-action value | abstract claims 2–5× higher return vs prior offline methods; strongest on multimodal data (exact D4RL rows not seen, `[ABS/FT-PARTIAL]`) | **Implemented** Model 6; conservatism is the safety mechanism |
| **TD3+BC** (2106.06860) | TD3 + a behavior-cloning term + state normalization | Hopper-Medium 99.5±1.0 vs CQL 72.0; Walker2d-Medium 79.7±1.8 vs CQL 30.1; HalfCheetah-Medium 42.8±0.3 vs CQL 37.4; "~2× faster" | Minimalist parsimony baseline; `FEATURES.md` F-06 names it "baseline-first" |
| **IQL** (2110.06169) | Expectile value, *never queries OOD actions* | claims SOTA on D4RL (exact rows pruned, `[FT-PARTIAL]`) | Attractive for safety (cannot be seduced by unobserved (state,alarm) pairs) |
| **One-step** (2106.08909) | One step of improvement on an on-policy Q^β, **no OPE** | one-step beats multi/iterative on most mujoco-medium (halfcheetah-m 55.6 vs 40.8 vs 47.4; walker2d-m 85.6 vs 75.9 vs 75.4; hopper-m 83.3 vs 53.0 vs 54.2); **iterative wins only on large, well-covered (random) data** | The decisive argument for small/narrow data |
| SAC (1801.01290) / PPO (1707.06347) | Online max-entropy / on-policy PG | SAC: stable across seeds; PPO: multiple epochs per batch (ABS-only, body unreadable) | **Online** — only a *simulator-stage-4* option; dangerous on a live alarm system → effectively ruled out |

**The decision, and why.** The literature's parsimony lesson is strong and consistent: on **small,
narrow-coverage** data (which disaster logs certainly are — few real events), **OPE is unreliable, so
iterative actor-critic methods that repeatedly do OPE amplify its variance** (2106.08909 diagnosis;
reinforced by TD3+BC's "simple rivals CQL" result and the survey's OPE open-problem). That is why:

- The **default is one-step** (`CQLConfig.gamma=0.0` makes the implemented CQL a *one-step* conservative
  learner — the code embodies "prefer simple" without discarding the conservatism machinery).
- CQL was chosen as the implemented *form* because its conservative penalty is a clean, single-coefficient
  way to keep a discrete-action policy inside the logging support — the property that matters most for a
  safety policy — and it degrades gracefully to one-step at `γ=0`.
- Escalation to full iterative CQL/IQL (`γ>0`) is **conditional on demonstrating large coverage** — which
  we probably cannot (2106.08909 guidance; `literature_brief.md` staged policy: *fixed threshold → one-step
  offline RL → iterative only if OPE-feasible*).
- Online methods (SAC/PPO) are **ruled out for deployment** because they require exploration in a live
  life-safety system; PPO is "the Stage-4 online fine-tuning option in a simulator, if at all" (PPO note).

Note a documented **design-vs-code divergence `[LIKELY]`**: `FEATURES.md` F-06 lists the component as
"Offline RL alarm policy (**TD3-BC** baseline-first)" citing 2106.08909/2506.00505, while the *implemented*
Model 6 is **CQL**. These are consistent in spirit (both are "simple, support-respecting offline RL"), and
the staged plan permits either; but a reader comparing F-06 to `offline_rl.py` should know the implemented
algorithm is CQL (one-step by default), not TD3+BC. See 10.9.

---

## 10.6 Compute budget — the ~30 GPU-h Kaggle frame and why RL is ~1.0 GPU-h on one GPU

Project-wide, Kaggle is assumed **~30 GPU-h/week**, kept to **~25.5 usable** after a ≥15% reserve
(`_CANON.md §8`; `KAGGLE_BUDGET.md`). Within that envelope, **WS5 RL/alarm is budgeted at ≈ 1.0 GPU-h**,
with the explicit lever *"OPE/FQE on logged/sim episodes … offline eval mostly CPU"* (`KAGGLE_BUDGET.md:57`).
In other words RL is a *small* line item precisely because its expensive part (OPE, policy valuation) is
**CPU, offline** — the WIS/ESS/BVFT/SCOPE-RL evaluation in 10.3–10.4 is numpy/CPU work, not GPU work.

The training itself runs on **ONE GPU** by deliberate design, documented in `train_offline_rl.py:36-38`:

> *"the Q-net is tiny (state_dim × 3 actions). Multi-GPU scatter/gather overhead would be LARGER than the
> compute, so RL deliberately runs on ONE GPU with a large batch instead of DataParallel."*

Hence `scale_batch_by_gpus=False` and a large `batch=256`. The teaching point: **model size, not dataset
size, decides the parallelization strategy here** — a two-layer 256-wide MLP with three outputs is so small
that data-parallel communication would dominate, so the correct engineering choice is a single GPU with a
big batch. This also keeps WS5 comfortably inside the ≤30 GPU-h/week constraint (**C3**, `_CANON.md §5`).
These budget figures are **planning-level**, re-confirmed on the live quota panel at build (`_CANON.md §8`).

---

## 10.7 Results

**Not measured.** No TRINETRA RL policy has been trained; no RL logs have been collected; no OPE verdict,
return, CVaR, or constraint-violation rate exists for TRINETRA. The numpy OPE gate and rule baseline *run*
and are covered by the 128-test suite (`[CONFIRMED]` they execute correctly), but that confirms *the gate
logic*, not *a policy's value*. Every performance figure in this chapter (the D4RL numbers in 10.5, the
PIER/FAITH/GREAT-EER figures in the research artifacts) is **source-reported from the cited paper on that
paper's own benchmark** and must never be read as a TRINETRA result (`_CANON.md §0`,`§1`). The honest
headline is: *the RL component is specified, partially implemented (numpy gate + compile-clean CQL), and
gated — it has not been evaluated.*

---

## 10.8 Failure modes and mitigations

The research program catalogues the RL-specific failure modes; each has a concrete mitigation already
reflected in the design or code:

- **Reward inversion / reward hacking.** A proxy reward that is cheap to game can drive the policy to a
  degenerate "silence everything" or "alarm always" solution. *Mitigations:* keep reward
  **potential-based and time-invariant** or prove the exception (PBRS, 2608.08158 §2.7, in a partially
  observed MDP); price false alarms above a flat penalty to block cry-wolf (DC-18); audit proxy rewards with
  scarce expert labels via envelope sampling with bounded regret (2610.11281); and govern the reward with an
  **anchor-guarded inspectable verifier** — *a downstream task score CANNOT certify the reward/verifier*
  (2610.11464). The code-level backstop is that the reward is the *logged* `r`, not a learned signal the
  policy can manipulate.
- **Distribution shift (OOD actions).** The core offline-RL failure (2005.01643). *Mitigations:* CQL's
  conservative penalty pushes Q down on OOD actions (10.3.1); IQL's "never query OOD actions" is the
  alternative; one-step improvement avoids iterative error exploitation (2106.08909).
- **OPE positivity violation / ESS collapse → fail-safe.** If the logging policy almost never took some
  action, or weights concentrate, OPE cannot honestly estimate value. *Mitigation — implemented:*
  `ope_feasible` returns `False` (positivity `min_prob=1e-2`, ESS `min_ess_frac=0.1`), so `ope_admission`
  sets `deploy_learned=False` and the system **keeps `RuleBaselinePolicy`** (`rl.py:57-83`). The fail-safe
  is not a slogan — it is the default return path when OPE is untrustworthy.
- **Shield unrealizability / conflicting predicates (FM-05).** Hard physics predicates could contradict each
  other, making no action satisfy the floor. *Mitigation:* realizability-check the shield before deploy
  (2507.23603, `FEATURES.md` F-06); provide a **minimum-predicted-peak-harm fallback** when no safe action
  exists (FAITH 2610.12432).
- **Hollow safety / sim-to-real gap.** A catastrophe-rate drop with no *anticipation* evidence is hollow
  (2609.34041); simulator success need not transfer. *Mitigations:* probe lead-time/anticipation explicitly
  (DC-16); validate against real fire progression (PyroStack) and behavior (FLARE); report **worst-case**
  (not average) constraint violations and rliable-style aggregates with many seeds (`rl_evaluation_plan.md`).
- **Naive RL underperforming a good baseline.** *"RL beats baselines only sometimes; naive RL
  underperforms"* (2509.19972; `FINAL_REPORT.md §7`). *Mitigation:* the whole admission regime — RL must
  **beat a strong non-RL baseline** (MILP bound, GREAT-EER 2602.14676) *and* clear the OPE gate, else the
  honest outcome recorded is "use the non-RL optimizer" (`rl_evaluation_plan.md §1`).

The common thread: **every failure mode degrades to the rule baseline or a bounded-harm fallback**, never to
a silent or unbounded action — the compiled meaning of Rule 19.

---

## 10.9 Open consistency points for the handover

Flagged plainly (per the honesty contract, `00_README §0.5`):

1. **Action-cardinality mismatch.** `offline_rl.py` uses 3 actions `{HOLD,WATCH,ALARM}`; `rl.py`'s
   `RuleBaselinePolicy.act` is binary `{0,1}`. The OPE comparison in `train_offline_rl.py` compares a
   3-action target against a behavior whose default uniform prob is `1/len(ACTIONS)` — the HOLD/WATCH/ALARM
   → binary mapping used when comparing to the rule baseline is **not explicit in code**. `[LIKELY]`
   reconciled by `{WATCH,ALARM}→alarm`, but a reader should verify at build.
2. **CQL vs TD3-BC labeling.** `FEATURES.md` F-06 says "TD3-BC baseline-first"; the implemented Model 6 is
   **CQL** (one-step at `γ=0`). Consistent in spirit; worth a one-line reconciliation in `FEATURES.md`.
3. **Shield object not in numpy core.** The monotone floor lives in `CQLPolicy.act` (torch); `rl.py` has no
   standalone shield class and the realizability check (2507.23603) is specified, **not implemented**.
4. **Baseline = logged behavior reward.** `ope_admission` is called with `baseline_rewards=rewards`
   (the behavior policy's own realized reward). This is a *conservative, self-consistent* comparator
   (`v_b = mean(logged r)`), but it is the *behavior* baseline, not necessarily the *rule baseline's*
   simulated reward — a deliberate but documentable choice.

---

## 10.10 References → chapter 19

Full bibliographic detail, verification status, and BibTeX live in **chapter 19** (`19_REFERENCES_FULL.md`);
row-level provenance in `analysis/02_paper_ledger.csv`; per-paper notes in `analysis/03_paper_notes/`. IDs
used in this chapter:

- **Offline-RL algorithms:** CQL **2006.04779**; TD3+BC **2106.06860**; IQL **2110.06169**; one-step
  **2106.08909**; offline-RL survey **2005.01643**; SAC **1801.01290**; PPO **1707.06347** (`[ABS]` — body
  unreadable, flagged in its note).
- **Safety shield:** Alshiekh et al. **1708.08611** (post-posed shielding); realizability check **2507.23603**
  (via `FEATURES.md` F-06); CAPSULE **2604.23576** (F-06).
- **OPE / valuation protocol:** BVFT **2110.14000**; SCOPE-RL **2311.18206**; one-step valuation **2106.08909**
  / **2206.02000**; feedback-aware OPE **2312.01530**; model-selection-for-offline-RL **2107.11003**
  (named-method refs from `TRINETRA_Workstreams.md`; **no local note / no numbers attributed**).
- **Non-RL baseline + env + reward/safety (research artifacts):** MILP/GREAT-EER **2602.14676**; RL-DMF
  **2601.06664**; naive-RL-underperforms **2509.19972**; PIER **2603.17319**; FAITH **2610.12432**; unified
  safety Bellman **2610.12420**; constrained MARL **2610.11739**; reward-hacking **2610.11281**/**2610.11464**;
  variance-averse **2610.07899**; PBRS **2608.08158**; eval-hygiene **2609.34041**/**2610.03369**; env reuse
  Ctrl-CWM **2610.09438**, cinemere **2509.19972**, PyroStack **2609.36315**, FireGen **2610.07431**, FLARE
  **2502.17701**, Crazyflow **2610.08225**, BluffJAX **2610.07686**, sim-to-real **2610.05819**;
  decision-focused-learning **2606.21773**.

> **Identifier caveat (`_CANON.md §7`):** these arXiv IDs are mostly subagent-reported and **not
> independently re-fetched** — a disclosed residual risk. Treat every source-reported number as that paper's
> claim on its own data, kept visibly separate from TRINETRA (which measured nothing here).
