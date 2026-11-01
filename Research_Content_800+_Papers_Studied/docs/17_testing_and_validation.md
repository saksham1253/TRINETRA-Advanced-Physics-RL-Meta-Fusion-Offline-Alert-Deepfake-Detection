# 17 — Testing and Validation

This chapter documents the TRINETRA (HIMKAVACH) test harness: what it tests, how to run it, the exact
output a healthy run produces, and how the tests lock down the correctness invariants and safety posture the
project depends on. Read `_CANON.md §2` alongside this chapter — it is the arbiter for the numbers quoted
here, and this chapter agrees with it exactly.

Everything in this chapter was **run in this environment** on the numpy core. Where a claim is a run result
it is tagged `[CONFIRMED]`; where it is an inference about code behaviour not separately executed it is
tagged `[LIKELY]`; design intent not re-measured is `[HYPOTHESIS]`.

---

## 17.1 Test philosophy — what these tests are, and what they are *not*

The single most important thing to understand before reading a single assertion: **nothing in TRINETRA has
been trained, and no dataset has been downloaded** (`_CANON.md §0`). Therefore the test suite does **not**,
and cannot, measure skill — there is no accuracy, recall, false-alarm rate, lead time, or AUROC produced by
TRINETRA to measure. Any such number anywhere in the documentation is **source-reported** from someone
else's paper on their own data, never ours.

What the suite *does* test falls into two families, and the two files you run map onto them one-to-one:

1. **Correctness / golden tests** (`python run_tests.py` → the `tests/` tree, stdlib `unittest`). These pin
   down the *math and the contracts* of the pure-numpy core: that a physics formula reduces to its known
   closed-form limit, that a fusion weight vector sums to one, that a conformal interval achieves its
   nominal coverage on exchangeable data, that a bug the research phase caught stays fixed. They are
   deterministic and seed-pinned. They assert *properties and limits* ("saturated FS equals the saturated
   closed form to 12 places", "α=2 inverse-velocity recovers the true failure time"), not learned
   performance. This is the right kind of test for an untrained system: you can prove a formula is correct
   without ever having a dataset.

2. **CI honesty-and-safety gates** (`python scripts/ci_gates.py` → six fail-closed invariants). These are
   **not performance tests either** — the file says so in its own docstring. They are *tripwires* that fail
   the build if a safety or honesty rule from `_CANON.md §5` is violated in code: human approval must be
   hard-wired, Class-C novel terms must default OFF, raw video must not egress, look-ahead feature
   timestamps must be rejected, the LoRa frame must fit its byte budget, and no banned buggy-code token may
   reappear in `src/`.

The design principle (R16, `_CANON.md §5`) is that a system in a life-safety domain earns the right to make
a performance claim only after passing a spatial-CV admission gate — and since no model has been trained,
TRINETRA has not earned any such claim. The tests enforce that discipline rather than papering over it: see
the `ReportGuard` tests in §17.4, which literally refuse to emit a headline number until spatial CV and
baselines are present.

---

## 17.2 How to run — exact commands and the observed output

The numpy core needs only Python + numpy. Run from the `trinetra/` directory with the bundled interpreter.
The `PYTHONIOENCODING` line matters on Windows: `unittest` writes its progress and summary to **stderr**, and
without a UTF-8 stream the console can mangle or truncate that output.

```powershell
cd trinetra
$env:PYTHONIOENCODING = "utf-8"
& "C:\Users\Dell\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" run_tests.py
& "C:\Users\Dell\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" scripts\ci_gates.py
```

### 17.2.1 Observed output of `run_tests.py` [CONFIRMED, this environment]

The final lines of the real run were:

```
----------------------------------------------------------------------
Ran 128 tests in 0.468s
OK
[exit code: 1]
```
> The `0.468s` is one representative run; wall-clock duration varies slightly run-to-run (e.g. 0.468–0.477 s).
> The load-bearing facts are the `Ran 128 tests` count, the `OK`, and the explained spurious `[exit code: 1]`
> (unittest writes its summary to stderr — see below), not the exact seconds.

**`Ran 128 tests ... OK`** is the pass signal. Read §17.6 before you react to the `[exit code: 1]` — it is a
harness artifact of `unittest` writing to stderr, **not** a failure. The real pass/fail signal is the final
word `OK` (all passed) or a `FAILED (...)` line (something broke).

### 17.2.2 Observed output of `scripts/ci_gates.py` [CONFIRMED, this environment]

```
  [PASS] G-advisory
  [PASS] G-classC
  [PASS] G-security
  [PASS] G-leak
  [PASS] G-iot
  [PASS] G-legacy
------------------------------------------------------------
ALL 6 CI GATES PASSED
```

This run exited 0. The six gate names are fixed by the `@gate(...)` decorators in `scripts/ci_gates.py`
(lines 39–100): `G-advisory`, `G-classC`, `G-security`, `G-leak`, `G-iot`, `G-legacy`.

Both results match `_CANON.md §2` exactly: 128 tests OK, all 6 CI gates passed.

---

## 17.3 Suite-by-suite inventory (correctness / golden tests)

The 128 tests live under `tests/` in topic directories, each run through stdlib `unittest` discovered by
`run_tests.py` (it inserts `src/` and the repo root onto `sys.path`, then discovers `test_*.py`). The total
of **128 tests, OK** is `[CONFIRMED]` from the runner; the per-suite descriptions below are drawn directly
from reading each file, and each line names the production module the suite guards.

### 17.3.1 Physics golden — geo (`tests/physics_golden/test_geophys.py`)
Guards `trinetra.ws1b_geophys` (FS, Iverson, Fukuzono, Caine). These encode the exact correctness invariants
the research flagged as bugs in the original report (see the module docstring and §17.7):
- **FS saturated limit** (`test_saturated_limit`): `factor_of_safety(..., sigma_s=0.0)` must equal
  `factor_of_safety_saturated(...)` to **12 decimal places** — the general unsaturated form must collapse
  exactly to the saturated closed form as suction stress → 0.
- **FS monotonicity** (`test_monotonic_in_suction`, `test_decreasing_in_pore_pressure`): more matric suction
  ⇒ more stable (higher FS); more pore-water pressure ⇒ less stable (lower FS). These are directional
  physics sanity checks.
- **Iverson slope-only-through-D1** (`test_slope_only_through_D1`): the single most load-bearing physics
  test. `transient_head(...)` with slope β must equal the slope-free core `_transient_core` evaluated at
  `D1 = D0/cos²β` to 12 places, **and must NOT equal** the buggy variant that multiplies the response by an
  extra `cos²β`. This is the regression lock for the headline hazard bug (§17.7).
- **Iverson boundary** (`test_ierfc_at_zero`: `ierfc(0)=1/√π`; `test_transient_zero_at_t0`: head is 0 at
  t=0): the special-function and initial-condition anchors.
- **Fukuzono α=2 ⇒ 1/v linear** (`test_recover_tf_alpha2`): with inverse velocity falling linearly to zero
  at t_f=100, `inverse_velocity_fit(..., alpha=2.0)` recovers t_f to 4 places with R²>0.999.
- **Caine I–D exceedance direction** (`test_exceedance_direction`): a high-intensity point exceeds the
  intensity–duration threshold and a low-intensity one does not, with a strictly larger exceedance ratio.

### 17.3.2 Physics golden — Iverson multi-pulse (`tests/physics_golden/test_iverson_multipulse.py`)
Guards `trinetra.ws1b_geophys.iverson.transient_head_multipulse` (rainfall-pulse superposition):
- Single step equals `transient_head` (12 places); a finite pulse recovers (head drops) after rain stops but
  stays positive; **superposition linearity** (two onset pulses == sum of each standalone contribution, 10
  places); intensity monotonicity. These confirm the response is a correct linear-system superposition.

### 17.3.3 Physics golden — Fukuzono prediction interval (`tests/physics_golden/test_fukuzono_ci.py`)
Guards `trinetra.ws1b_geophys.fukuzono`:
- Noiseless 1/v line recovers t_f=10 (6 places) with near-zero standard error; added noise widens the
  interval and the point estimate is bracketed by `t_failure_low < t_failure < t_failure_high`; recency
  half-life weighting leaves a clean line's estimate unchanged (stays finite/sane). This is the uncertainty
  quantification contract around the inverse-velocity failure-time prediction.

### 17.3.4 Physics golden — fire (`tests/physics_golden/test_firephys.py`)
Guards `trinetra.ws1a_firephys` and the Rule-20 flag-gating of Class-C novel terms:
- **Established (Class A)**: Heskestad flame height increases with heat-release rate; Strouhal puffing
  frequency decreases with fire diameter (the 1.5/√D law); gray-body radiance↔temperature round-trips (6
  places); Byram convection number is larger in low wind (plume-dominated) than high wind.
- **Novel ND (Class C)**: aliasing identity (no aliasing when fs>2·f_true; 7 Hz flicker at 10 Hz sampling
  aliases to 3 Hz); ND2 smoke-transmittance uncertainty **grows as smoke thickens** — the model fails toward
  "uncertain", not toward false confidence.
- **Flag-gating**: Class-C `nd3` path is **OFF by default** (`used_classC` False) and only turns on when the
  config flag is explicitly set; a windy regime lowers the fire-gate consistency score. This is the code-level
  proof of Rule 20.

### 17.3.5 Fusion — PHARAOH / FM-1 / shield (`tests/fusion/test_fusion.py`)
Guards `trinetra.ws5_fusion_rl` fusion dispatch and the safety shield (gate G4):
- PHARAOH power mean (ρ≥1) is ≥ the arithmetic mean (the anti-complacency corollary — fusion can only raise
  risk, never dilute a loud expert); PHARAOH order rises with expert disagreement and salience.
- **Dispatch default is FM-1, not Class-C**: `fuse(..., Config())` returns model `"FM-1"` with
  `used_classC` False; PHARAOH is reached only when its flag is set, and then `used_classC` is True. No
  experts ⇒ maximum uncertainty (`u_star == 1.0`).
- **Shield floor**: a single node cannot reach RED (`tilt_rate=9` alone stays below RED); **corroborated**
  tilt across 3 nodes reaches RED; FS<1 raises at least ORANGE; nothing triggered ⇒ GREEN. This is the
  monotone "shield can only raise, never lower" safety invariant.

### 17.3.6 Fusion — GMF bounded residual (`tests/fusion/test_gmf.py`)
Guards gated-mixture fusion:
- Gate weights sum to 1; with no learned head the residual is exactly 0 (output equals the base precision
  mean); **a rogue head returning ±999 is hard-clipped to ±residual_cap** (0.1); dispatch to `"GMF"` with
  PHARAOH off is Class-B not C; empty experts are safe (p=0). An **exported numpy head JSON** (the format
  `kaggle/train_fusion_head.py` writes) loads via `load_numpy_head` and stays bounded even with large export
  weights, and the fused probability stays in [0,1]. This proves a trained head can only ever nudge, never
  override, the physics base — torch-free.

### 17.3.7 Fusion — hierarchical / correlation-aware BLUE (`tests/fusion/test_hierarchical.py`)
Guards two-layer fusion and the double-counting fix:
- Independent equal-quality experts get equal weights summing to 1; a **redundant pair (ρ=0.8) does not
  double-count** — the independent expert out-weighs each redundant one and beats the naive 1/3; as ρ→1 the
  redundant pair collapses to ~one effective vote; weights stay non-negative (no hedging). Group fusion
  reduces a group to a single expert, lowers consistency on disagreement, propagates the weakest physics
  class, and the end-to-end `decide_hierarchical` flow stays advisory with Class-C transparency propagating
  to the decision. Three identical geo alarms collapse to the shared 0.9, not an amplified value.

### 17.3.8 Fusion — deep-model adapters (`tests/fusion/test_adapters.py`)
Guards `deep_expert(...)` adapters (torch-free: they convert a deep model's scalar output into an
`ExpertOutput`, no torch imported):
- Deepfake reliability is **hard-capped ≤0.4** (Rule 19 low-trust) and labelled `PhysicsClass.DATA`; a
  geo-PINN is Class-B; probabilities are clamped to [0,1]; an unknown source raises `KeyError`; a full
  `decide(...)` flow with a low-trust deepfake expert does not let it dominate (risk stays <0.8) while the
  FS<1 shield floor still applies. This proves deep outputs enter the system under the same trust and class
  discipline as everything else — even though the deep models themselves are not run here (§17.5).

### 17.3.9 Decision — single decision function (`tests/decision/test_decision.py`)
Guards `conformal_level` and `decide` (gate G3, Rule 19):
- Conformal bands are monotone at p\*=0.0476: risk 0.0→GREEN, 0.1→YELLOW, 0.3→ORANGE, 0.9→RED.
- **Shield can only raise**: GREEN fused risk + FS<1 ⇒ final ≥ ORANGE with `shield.raised` True; every
  decision is `advisory`; **no experts ⇒ fail-safe `uncertain`** (abstain and escalate, never a silent
  all-clear); high-conflict experts ⇒ `uncertain`; Class-C flagged when PHARAOH on; the decision
  serialises to a dict carrying `level`, `shield`, `advisory=True`.

### 17.3.10 Eval harness (`tests/eval/test_eval.py`)
Guards `trinetra.eval` (gate G2 — the admission machinery):
- **Spatial-block CV** never lets a block span train and test (no spatial leakage); temporal split keeps all
  training times before test times; `assert_no_time_leak` raises `LeakageError` on a future timestamp.
- **Cost-loss value score**: p\* = C_FA/(C_FA+C_miss) = 5/105; a perfect forecast scores 1.0; a constant
  climatology-equivalent forecast scores ≤0 (no credit for a non-informative predictor).
- **real-win**: an informative model wins the bootstrap comparison and a noise model does not.
- **ReportGuard** (R16 in code): refuses to emit a headline number without spatial CV, without baselines, or
  when a baseline is not beaten; only an *admitted* guard (both baselines beaten with positive CI floors)
  returns a headline. `LogisticNumpy` learns a separable problem to >0.9 accuracy (the baseline learner
  works, torch-free).

### 17.3.11 Eval — bootstrap stats (`tests/eval/test_stats.py`)
Guards `trinetra.eval._stats`: normal CDF/PPF are mutual inverses and hit known quantiles (z₀.₉₇₅≈1.95996);
the **BCa interval** brackets the true mean; the **stationary (block) bootstrap** returns an index array of
the right length and range. These underwrite the honest confidence intervals used by the admission gate — a
pure-numpy reimplementation because scipy is unavailable.

### 17.3.12 Eval — calibration (`tests/eval/test_calibration.py`)
Guards `trinetra.eval.calibration`: ECE is low on perfectly calibrated outcomes and high (>0.8) when the
model claims 0.9 but nothing happens; the reliability curve has the right bin shapes; the Brier
decomposition reconstructs the Brier score; **isotonic recalibration reduces ECE** and is monotone; Platt
scaling outputs valid probabilities. Calibration is the property that lets an advisory *level* mean what it
says — critical when a human acts on it.

### 17.3.13 Robust — conformal + drift + degradation (`tests/robust/test_robust.py`)
Guards `trinetra.ws6_robust` (gate G3/M4): conformal marginal coverage lands within ±0.03 of 1−α on
exchangeable data; regression intervals cover ≥0.85; PSI is ~0 for same distribution and flags a mean shift;
CUSUM detects a step change; **missing-modality degradation** marks an absent source unavailable and inflates
its peers' uncertainty rather than pretending the signal is still there.

### 17.3.14 Robust — advanced conformal (`tests/robust/test_conformal_advanced.py`)
Guards adaptive/Mondrian/risk-control conformal:
- **ACI under drift**: with the residual scale drifting upward, Adaptive Conformal Inference tracks ~90%
  realized coverage (between 0.82 and 0.97) where static CP would under-cover.
- **ACI sign**: a *miss* **decreases** αₜ, which **raises** the (1−α) quantile and **widens** the next
  interval — the correct self-correction (the test asserts the post-miss quantile is ≥ the baseline).
- **Mondrian** per-group quantiles differ (GLOF wider than LANDSLIDE) and an unseen group gets the most
  conservative (max) quantile. **Conformal risk control** picks a threshold that bounds the realized miss
  rate near the 0.03 target.

### 17.3.15 Interfaces — anomaly / CCTV / EO / RL-OPE / deepfake (`tests/interfaces/test_interfaces.py`)
Guards the M2/M3/M5/M9 interfaces, including the **honest-stub contract** for torch-only paths:
- Anomaly ensemble scores injected outliers higher; forecast-residual spikes at the jump sample.
- CCTV `TemporalValidator` requires persistence (3 confirming frames) and rejects a single glint; the real
  `EdgeDetector().detect(...)` **raises `MissingDependency`** (torch absent).
- EO encoder's real `.embed(...)` raises `MissingDependency`; its deterministic hashing fallback is
  reproducible and unit-norm.
- RL: the rule baseline acts correctly; the learned `OfflineRLPolicy().fit(...)` raises `MissingDependency`;
  the **positivity/OPE feasibility gate** blocks an under-explored logging policy and admits a learned policy
  only when feasible *and* better.
- Deepfake authenticity reliability never exceeds 0.4 (Rule 19); fake cues raise p_fake; the real
  `DeepfakeDetector().score(...)` raises `MissingDependency`. These `MissingDependency` assertions are how
  the suite proves "no fake results": a path that genuinely needs torch fails loudly instead of inventing a
  number.

### 17.3.16 Alerting (`tests/alert/test_alert.py`)
Guards `trinetra.ws3_alert` (M8, Rule 19): a CAP message is **refused without an approval token** and with a
bogus token (`SafetyViolation`); only after `approve(...)` returns a real token does `build_cap` emit signed
CAP XML (`<severity>Severe</severity>`, the zone id, the word `advisory`, an `hmac-sha256:` signature). GREEN
has no public CAP and cannot be approved. Severity mapping is pinned (RED→Extreme/Immediate/Observed,
ORANGE→Severe/Expected/Likely, YELLOW→Minor/Future/Possible). The operator console text says `ADVISORY` and
`human operator must review`. DTN binary-spray hands off half the copies and clears on delivery.

### 17.3.17 IoT (`tests/iot/test_iot.py`)
Guards `trinetra.ws7_iot` (M7, gate G5): the LoRa frame is ≤51 B and round-trips (seq, edge level, tilt,
rain, temp recovered within tolerance); readings sign/verify, tamper is detected, replays and stale
sequence numbers are rejected, out-of-range battery is flagged; the node-local edge screen escalates to
`LOCAL_SIREN` on two cues, `WATCH` on one, `NONE` when quiet. This is the offline-first alert path (C1)
proven to fit the radio budget.

---

## 17.4 The six CI gates (`scripts/ci_gates.py`) — honesty and safety tripwires

These are **fail-closed invariants**, not performance tests: any one failing exits non-zero and fails the
build. Each maps to a numbered rule/constraint in `_CANON.md §5`. All six passed this environment
`[CONFIRMED]` (§17.2.2).

| Gate | Violation it blocks | Pass criterion (from the code) |
|------|---------------------|--------------------------------|
| **G-advisory** | Autonomous public alert without a human (Rule 19) | `Config().require_human_approval()` is hard-wired `True`, **and** `build_cap(decision, approval_token=None, ...)` raises `SafetyViolation`. If a CAP could be built without an approval token, the gate fails. |
| **G-classC** | A novel, unvalidated Class-C term being ON by default (Rule 20) | `fusion.operator.pharaoh` is `False` **and** every `firephys.nd1..nd7` flag is `False` in the default config. |
| **G-security** | Endpoint exfiltration / raw-video egress (C6/C7) | An empty allow-list rejects *all* endpoints (`EndpointNotAllowed`), **and** `assert_no_video_egress({... "clip": raw bytes})` raises `SafetyViolation`. |
| **G-leak** | Look-ahead data leakage into a decision (G6) | `assert_no_time_leak([1,2,11], decision_time=10)` raises `LeakageError` — a feature timestamped after the decision time is rejected. |
| **G-iot** | A LoRa frame that overflows the radio budget (G5/C-offline) | `FRAME_LEN <= 51` bytes. |
| **G-legacy** | A previously-fixed buggy code pattern reappearing in `src/` | No file under `src/` contains any `BANNED_TOKENS` — currently `"EXTRA_COSBETA_ON_TRANSIENT"`, `"advisory = False"`, `"advisory=False"`. |

The last gate, **G-legacy**, is a textual regression lock: it scans every `*.py` under `src/` and fails if a
banned substring reappears. `EXTRA_COSBETA_ON_TRANSIENT` is the sentinel for the Iverson transient bug
(§17.7); `advisory=False` would be an attempt to turn off the advisory posture. This is a cheap, blunt, and
effective second line of defence behind the numeric golden tests.

---

## 17.5 Coverage — what is and is not exercised here, and why

**Covered and run here (numpy core) [CONFIRMED]:** all 128 unit/golden/contract tests above, plus the 6 CI
gates. That is the complete deterministic/numerical core: geo and fire physics, all fusion operators (FM-1,
GMF, hierarchical/BLUE, PHARAOH), the safety shield, the single decision function, conformal (static, ACI,
Mondrian, CRC), calibration and recalibration, the bootstrap stats, the eval admission harness, the LoRa
codec, signing/replay, the CAP builder, and the deep→expert adapters (torch-free). The sandbox provides
**numpy, pandas, lxml only** — no torch/scipy/sklearn/yaml (`_CANON.md §2`) — which is exactly why the stats,
logistic baseline, and recalibrators are reimplemented in pure numpy and *are* tested.

**Not run here, and honestly marked so:**

- **The PyTorch `deep/` layer** (EO foundation encoder, CCTV fire CNN, deepfake net, deep anomaly heads,
  offline-RL training — the 6 trainable models). **No test module under `tests/` exercises these models**
  (confirmed by enumerating the test tree). `_CANON.md §2` records them as **`py_compile` clean, not run on
  a GPU**. I did **not** independently re-run `py_compile` in this task, so I carry that as a
  **[CONFIRMED by _CANON]** fact rather than my own measurement — mark these models **UNTESTED-here
  (no torch in sandbox)**. What *is* tested here is the *boundary* around them: the interface tests
  (§17.3.15) assert that each torch-only entry point raises `MissingDependency` instead of fabricating a
  result, and the adapter tests (§17.3.8) assert their *outputs* would enter fusion under the right class and
  trust caps.
- **GPU training / Kaggle scripts**: multi-GPU (T4×2) ready but **not executed on a GPU** in this
  environment (`_CANON.md §2`). The *exported-head* consumption path, however, *is* tested torch-free via
  `load_numpy_head` (§17.3.6), so the handoff from a (hypothetically) trained head back into the numpy core
  is validated even though the training itself is not.

The honest summary: the parts that can be proven correct without data or a GPU are proven; the parts that
genuinely need torch/GPU are compile-checked only and are tested *at their boundary* for fail-loud behaviour.

---

## 17.6 Expected outputs and reading a real pass vs the spurious exit code

A future runner should expect **exactly**:
- `run_tests.py` → a stream of `... ok` lines on stderr, then `Ran 128 tests in <~0.5s>` and a final `OK`.
- `scripts/ci_gates.py` → `[PASS]` for each of `G-advisory, G-classC, G-security, G-leak, G-iot, G-legacy`,
  then `ALL 6 CI GATES PASSED` (exit 0).

**The exit-code trap.** `run_tests.py` returns `0` only when `result.wasSuccessful()` (line 23), but
`unittest.TextTestRunner` writes its entire report — including `OK` — to **stderr**. Under this harness a
command whose stderr is non-empty can surface a trailing **`[exit code: 1]`** marker even on a clean,
all-passing run; that is what happened here (§17.2.1). **Do not read that marker as a failure.** The
authoritative signals, in order:

1. The final line is `OK` and the count line reads `Ran 128 tests` → **real pass**, regardless of the
   `[exit code: 1]` marker.
2. The final line is `FAILED (failures=N, errors=M)`, or the count differs from 128 → **real failure**;
   scroll up for the `FAIL:`/`ERROR:` tracebacks.
3. For the gates, trust the literal `ALL 6 CI GATES PASSED` line and exit 0; any `[FAIL] <gate>` line or
   `CI GATES FAILED: n/6` is a genuine safety-gate failure that must block the build.

If you see `OK` but a count other than 128, something was added or skipped — reconcile it against
`_CANON.md §2` before trusting it.

---

## 17.7 How the tests lock the hazard-correctness bug fixes (cross-ref chapter 13)

Chapter 13 (robustness, bugs, fixes) documents the correctness defects the research phase caught. The two
load-bearing ones are **double-locked** so they cannot silently regress:

- **Iverson transient slope factor.** The original report applied an *extra* `cos²β` factor to the transient
  pressure-head response. The corrected physics puts slope in **only** through the diffusivity
  `D1 = D0/cos²β`. Two independent locks:
  1. **Numeric golden** `test_slope_only_through_D1` (§17.3.1): asserts `transient_head(...)` equals the
     slope-free core at `D1` to 12 places **and** `assertNotAlmostEqual` against the buggy
     `core·cos²β` variant. A reintroduced extra factor fails this test immediately.
  2. **Textual gate** `G-legacy` (§17.4): the banned token `EXTRA_COSBETA_ON_TRANSIENT` cannot appear in
     `src/`, so even a commented-out or flagged re-introduction trips the CI gate.
- **Advisory-only posture.** `decide` always sets `advisory=True`, the shield can only *raise* a level, no
  experts fail-safes to `uncertain`, and CAP refuses to build without a human approval token. These are
  held by `test_decision.py` + `test_alert.py` (§17.3.9, §17.3.16) **and** by `G-advisory` plus the banned
  `advisory=False` token in `G-legacy`. To regress the safety posture you would have to defeat both a unit
  test and a CI gate.

The pattern — a precise numeric property test **plus** a blunt textual tripwire — is deliberate: the golden
test proves the current code is correct, the gate makes the specific wrong pattern un-mergeable. When you
read a before/after in chapter 13, the "after" is the state these tests pin.

---

## 17.8 How to add a new test when you extend the code (cross-ref chapter 16)

Chapter 16 (code guide) is the map of which module lives where; this section is the mechanics of keeping it
tested. The harness is intentionally dependency-free, so adding a test is cheap:

1. **Pick the directory** under `tests/` matching the code's workstream (`physics_golden/`, `fusion/`,
   `decision/`, `eval/`, `robust/`, `interfaces/`, `alert/`, `iot/`). Create a `test_*.py` — the filename
   must match the `test_*.py` glob or `run_tests.py` will not discover it. Each dir already has an
   `__init__.py`; keep that convention for new subdirs.
2. **Use stdlib `unittest` only** — subclass `unittest.TestCase`, no `pytest`, no `hypothesis` (not
   installed here). Import from `trinetra....`; `run_tests.py` has already put `src/` on `sys.path`.
3. **Assert a property, limit, or contract — never a trained-performance number.** Follow the house style:
   a known closed-form limit (FS saturated), a mathematical identity (superposition linearity), a monotone
   direction (more suction ⇒ higher FS), a bound (residual clipped to ±cap), a sign (ACI widens after a
   miss), or a fail-loud contract (`MissingDependency`, `SafetyViolation`, `LeakageError`). Seed every RNG
   (`np.random.default_rng(0)`) so the test is deterministic.
4. **If you fix a bug, add BOTH locks** (§17.7): a numeric golden test that would have caught it, and — if
   the bug has a recognisable code signature — a new entry in `BANNED_TOKENS` in `scripts/ci_gates.py` so
   `G-legacy` blocks its return. If you add a new safety rule, add a new `@gate("G-...")` function; the
   gate count in the final line is computed from `len(CHECKS)`, so the summary updates itself.
5. **If you add a torch-only path**, do **not** add a test that needs torch. Instead test the *stub
   contract* (the real call raises `MissingDependency`) and, if it produces fusion input, test its numpy
   adapter the way `test_adapters.py` does.
6. **Run both commands** (§17.2) and confirm the count rose and the final line is still `OK` with all 6
   gates passing. Then update `_CANON.md §2` and `CODE_INVENTORY.md` so the documented test count stays the
   single source of truth — a count that disagrees with `_CANON` is itself a documentation bug (per the
   honesty contract in chapter 00).

The guiding rule for extensions is the same as for the whole suite: you may test that the math is correct and
the safety rails hold; you may **not** add a test that asserts a skill number, because TRINETRA has not been
trained and has no skill to assert.
