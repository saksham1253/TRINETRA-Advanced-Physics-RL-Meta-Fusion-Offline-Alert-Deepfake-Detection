# 21 — FAQ & Troubleshooting

This chapter answers the questions a real user hits when they first read, run, extend, or try to deploy
TRINETRA (HIMKAVACH). It is a Q&A guide, cross-referenced to the chapter that owns each topic. It agrees
with `_CANON.md` exactly; where it quotes a run result, that result was observed in this environment and is
tagged `[CONFIRMED]`.

**Honesty labels (from `_CANON.md §1`):** `[CONFIRMED]` = measured by us here or verified in a cited source;
`[LIKELY]` = plausible, needs our validation; `[HYPOTHESIS]` = our unvalidated idea; `[INFEASIBLE]` = ruled
out; `[EST]` = planning estimate; **UNTESTED** = not executed in this environment.

**The one fact that resolves most confusion up front:** the **numpy core** runs here — `python run_tests.py`
→ **128 tests OK**, `python scripts/ci_gates.py` → **ALL 6 CI GATES PASSED**, `python demo.py` → an
end-to-end advisory decision — all `[CONFIRMED]`. The **torch / GPU / Kaggle** layer and **all datasets** are
**NOT runnable here** (no torch/CUDA/GPU, no data; sandbox has numpy, pandas, lxml only — `_CANON.md §2`).
Every answer in the KAGGLE/GPU section is therefore `[LIKELY]`/`[HYPOTHESIS]` guidance, not observed
behaviour; where an error string appears it is a **likely message** and is marked as such.

---

## 21.1 GENERAL FAQ

### Q. Is there any trained model, or any measured accuracy / skill / recall / latency / cost number?
**No. Nothing has been trained and nothing has been measured — by design.** `_CANON.md §0` and
`00_README_START_HERE.md §0.1` state it plainly, and `FINAL_REPORT.md` says verbatim: *"Nothing was built,
trained, or measured."* No TRINETRA model has been trained and no dataset has been downloaded, so there is
**no** TRINETRA accuracy, skill, recall, false-alarm, lead-time, latency, or cost figure anywhere. The only
"admitted" signal that exists is produced on **synthetic** demo data and it reads `admitted=False` (see
§21.2 and `18_reproduce_from_scratch.md §18.4`). This is the deliberate honesty-first state of a life-safety
project, not a documentation gap. `[CONFIRMED]`

### Q. Then why are all the performance numbers in the docs from other papers?
Two reasons, both deliberate. (1) **Rule 16 honesty (R16, `_CANON.md §5`):** no own performance claim may be
made before the spatial-CV eval admission gate passes, and since no model has been trained, that gate has
never been cleared — so there is no own number to quote. (2) **The research program never built or trained
anything** (`_CANON.md §0`); its job was to decide *what to build and why*, grounded in 631 arXiv references.
Every performance figure attributed to a *paper* is **SOURCE-REPORTED** on that paper's own data and is kept
visibly separate from "Our measurement: …" (`_CANON.md §1`). Full reference detail is in chapter 19; the
science posture is in chapter 12. `[CONFIRMED]`

### Q. Is this production-ready?
**No.** It is a **research program plus a reference-code implementation**. The numpy core runs and is tested,
but the system is **advisory-only and human-in-the-loop** by hard rule (R19), nothing has been trained, no
dataset or license has been verified, and the IoT cost/compute gates are not yet live-verified
(`_CANON.md §8`). Treat it as a correctness-proven skeleton and a decision/design record, not a deployable
product. See chapter 22 (limitations) and chapter 15 (deployment/ops) for what remains before any field use.
`[CONFIRMED]` for the code status; the "not production-ready" verdict follows from R16/R19 and the untrained
state.

### Q. Can it send alerts automatically?
**No — never, by rule.** R19 (`_CANON.md §5`) makes the system **advisory, human-in-the-loop, fail-safe to
"uncertain/offline"**, and this is enforced in code, not just documentation: `Config().require_human_approval()`
is hard-wired `True`, and `build_cap(...)` raises `SafetyViolation` if you try to build a public CAP message
without a human approval token. The CI gate **G-advisory** fails the build if either guarantee is removed, and
the banned token `advisory=False` is blocked by **G-legacy** (`17_testing_and_validation.md §17.4`). The one
autonomous actuation permitted is a **local siren / DTN rebroadcast** on the offline edge path — never a
public alert. Alerting detail is in chapter 08. `[CONFIRMED]` (gate observed passing here).

### Q. Why can't I just alert people by their IP address?
Because **IP-address-based alerting is `[INFEASIBLE]`** for life-safety targeting — this is a load-bearing
verdict the docs must carry un-softened (`_CANON.md §6`, source `FINAL_REPORT.md §4`). Consumer IP
geolocation resolves only to ISP/city granularity (often tens of km), is corrupted by CGNAT / VPN / DHCP,
does not map to a premises, and cannot address a specific person at risk. Public-IP exposure is instead
treated as a **security** concern (authenticated endpoints, allow-list C6). The full argument and the verdict
live in **chapter 08** (`08_ws3_offline_alerting.md`). `[INFEASIBLE]`

### Q. Which workstream is which? I keep seeing WS1a, WS1b, WS5, and also "WS1 physics".
Three numbering schemes exist and they are mapped explicitly in **`_CANON.md §3`**. Short version: the
user-facing **doc chapter frame** uses six workstreams (WS1 physics+meta-fusion, WS2 deepfake/media, WS3
offline alerting, WS4 CCTV, WS5 RL, WS6 robustness/bugs); the **internal artifacts** split finer (WS1a
fire-physics, WS1b geo-physics, WS5 fusion, WS7 IoT, WS8 anomaly, eval); and the **code packages** are
`ws1a_firephys/`, `ws1b_geophys/`, `ws5_fusion_rl/`, `ws6_robust/`, `ws7_iot/`, `ws8_anomaly/`, `eval/`, etc.
Always state which scheme a sentence uses. The canonical table is in `_CANON.md §3`. `[CONFIRMED]`

---

## 21.2 RUNNING THE CODE (numpy core — all answers `[CONFIRMED]` here)

### Q. `run_tests.py` prints `[exit code: 1]` at the end — did the tests fail?
**No — this is a known, benign quirk, not a failure.** `run_tests.py` returns `0` only when
`result.wasSuccessful()` (line 23), but `unittest.TextTestRunner` writes its **entire** report — including the
final `OK` — to **stderr**. Under this harness a command with non-empty stderr can surface a trailing
`[exit code: 1]` marker even on a clean, all-passing run.

The **authoritative** pass/fail signals (`17_testing_and_validation.md §17.6`), in order:
1. Final line is `OK` **and** the count line reads `Ran 128 tests` → **real pass**, regardless of
   `[exit code: 1]`.
2. Final line is `FAILED (failures=N, errors=M)`, or the count is not 128 → **real failure** (scroll up for
   `FAIL:` / `ERROR:` tracebacks).

The exact observed output in this environment was:
```
----------------------------------------------------------------------
Ran 128 tests in 0.468s
OK
[exit code: 1]
```
`Ran 128 tests ... OK` is the pass. (`scripts/ci_gates.py` is unaffected — it exits `0` cleanly and prints
`ALL 6 CI GATES PASSED`.) `[CONFIRMED]`

### Q. I get a `UnicodeEncodeError` (or garbled/truncated output) on Windows when running the tests.
Set UTF-8 output **before** running, so `unittest`'s stderr summary renders cleanly:
```powershell
$env:PYTHONIOENCODING = "utf-8"
python run_tests.py
```
`unittest` writes its progress and summary to stderr; without a UTF-8 stream the Windows console can mangle or
truncate it. This is the exact env var that produced the recorded 128-tests / 6-gates result
(`_CANON.md §2`, `00_README_START_HERE.md §0.4`, `18_reproduce_from_scratch.md §18.1`). `[CONFIRMED]`

### Q. `ModuleNotFoundError: No module named 'numpy'` (or `trinetra`).
The core needs **numpy + stdlib**. Install the CORE tier from the package root:
```powershell
cd trinetra
pip install -e .          # declares numpy, pandas, lxml (pyproject.toml)
```
The code paths exercised by the tests, CI gates, and demo use **only numpy + stdlib** (`trinetra/README.md`,
`_CANON.md §2`). Note: `run_tests.py`, `scripts/ci_gates.py`, and `demo.py` each insert `src/` onto
`sys.path` themselves, so they also run straight from the repo root **without** `pip install -e .` as long as
numpy is importable (`18_reproduce_from_scratch.md §18.2`). If you see `ModuleNotFoundError: trinetra`, you
are running from the wrong directory — `cd` into the folder that contains `pyproject.toml` / `run_tests.py`.
`[CONFIRMED]`

### Q. `ImportError: No module named 'torch'` (or `MissingDependency`) when I touch a deep model.
**Expected — this is the design working, not a bug.** torch is confined to the quarantined `trinetra.deep`
package; the numpy core never imports it (`16_code_guide.md §16.3`). Every torch-only entry point raises
`MissingDependency` **on purpose** rather than fabricating a result — e.g. `EdgeDetector().detect(...)`,
`EOEncoder().embed(...)`, `DeepfakeDetector().score(...)`, `OfflineRLPolicy().fit(...)`
(`17_testing_and_validation.md §17.3.15`). The interface tests actually *assert* these raises as the proof
that "no path invents a number." To run a deep model you need the DEEP tier on a GPU box:
```bash
pip install -r requirements-deep.txt   # torch 2.3.1, torchvision, sklearn, xgboost, timm, d3rlpy, ...
```
This tier is **UNTESTED here** (no torch/GPU in the sandbox, `_CANON.md §2`); see chapters 05, 10, 11 and
`18_reproduce_from_scratch.md §18.5`. `[CONFIRMED]` that the stubs raise here; the DEEP install itself is
UNTESTED.

### Q. I hit an `AttributeError: 'numpy.ndarray' object has no attribute 'ptp'` on numpy 2.0.
numpy 2.0 removed the array **method** `arr.ptp()`. Use the **free function** `np.ptp(arr)` instead. The core
already does this throughout (`ws8_anomaly.iforest_lite_score` / `mahalanobis_lite_score` /
`anomaly_ensemble`), which is why it stays numpy-2.0 clean (`16_code_guide.md §16.7.3`). If you add code,
keep using `np.ptp(...)`. `[CONFIRMED — the fix is present in source]`

### Q. How do I run the demo, and what should I see?
From the `trinetra/` folder:
```powershell
$env:PYTHONIOENCODING = "utf-8"
python demo.py          # == python -m trinetra.pipeline.demo
```
Observed output (synthetic evidence — **no performance claim**, `18_reproduce_from_scratch.md §18.4`): a
Fukuzono inverse-velocity forecast `t_f ≈ 35.7 h (r2=0.973)`; a fused + conformal + shielded **advisory RED**
decision for zone `UK-CHX-07`, `risk=0.889`, `used_classC=False`, `fusion=FM-1`; the offline siren/DTN
fallback; a **human-gated** CAP 1.2 message; and the hindcast honesty gate printing `admitted=False` for both
the noise and the informative model. The `admitted=False` is **the Rule-16 gate working** on synthetic data,
not a failure — nothing may claim skill until it beats climatology + logistic baselines on spatial-CV with a
CI. `[CONFIRMED]`

---

## 21.3 KAGGLE / GPU (not runnable here — guidance is `[LIKELY]`/`[HYPOTHESIS]`, error strings are **likely messages**)

> None of the commands below were executed in this environment: there is no torch/CUDA/GPU and no dataset
> (`_CANON.md §2`). Flags are read verbatim from each script's real `argparse`
> (`18_reproduce_from_scratch.md §18.5`); runtimes and failure strings are planning-level guidance only. The
> operational contract for the ~25.5 usable GPU-h/week budget and resume logic is **chapter 11**
> (`11_training_compute_kaggle.md`); the Kaggle failure/fix table is also in chapter 11 §11.6.

### Q. Training dies with a CUDA out-of-memory error. [LIKELY]
Likely message (CUDA OOM): `RuntimeError: CUDA out of memory. Tried to allocate ...`. Mitigations, in order:
- Lower **`--batch N`**, which is the **per-GPU** batch (effective batch = `N × n_gpus`, LR scaled linearly,
  Goyal 2017; `kaggle/README.md §2b`). Halving `--batch` roughly halves per-GPU activation memory.
- **Tile / stream** large inputs (EO patches, CCTV clips) instead of loading whole tensors.
- Use **gradient accumulation** to keep an effective batch while shrinking the per-step footprint.
- fp16 **AMP** is already on by default on the T4s, so you do not need to enable it manually.
`[LIKELY]` — not reproduced here.

### Q. Only one GPU shows up when I expected two T4s. [LIKELY]
On startup each script prints a banner like `GPUs visible=2 | DataParallel=True | effective_batch=128
lr=6.00e-04` (`18_reproduce_from_scratch.md §18.5.2`). If it says `GPUs visible=1`:
- Check **Settings → Accelerator = GPU T4 ×2** in the Kaggle session (`kaggle/README.md §1`); a P100 session
  is single-GPU by design.
- To *intentionally* run single-GPU, pass **`--parallel none`** (forces single-GPU); `--parallel dp` forces
  DataParallel, `--parallel auto` (default) uses DataParallel only when `n_gpus()>1`.
- Note **offline-RL is deliberately 1 GPU** (`scale_batch_by_gpus=False`; the Q-net is tiny, so scatter/gather
  costs more than it saves) and prints `offline-RL uses 1 GPU (tiny net)` — that is expected, not a fault.
`[LIKELY]`.

### Q. Geo-PINN throws a DataParallel autograd `RuntimeError`. [LIKELY]
The Geo-PINN physics loss uses `autograd.grad` **inside** the forward pass; DataParallel runs this per-replica
and *usually* works (`kaggle/README.md §2b`, chapter 13). The known-good fix — rebuilding `Z,t` as autograd
leaves inside `geo_pinn_step` via `detach().requires_grad_()` so autograd works under DataParallel — is
**already in the code** (`16_code_guide.md §16.5.8`, `GeoPINN`). So you should not hit it on the shipped path.
If a *custom change* reintroduces the error (a likely message would be a thread/autograd `RuntimeError` about
differentiating a non-leaf or a backward-through-replica failure), rerun with **`--parallel none`** or use the
DDP launcher (`trinetra.deep.ddp`). The root-cause write-up is in **chapter 13** (bugs/fixes). `[LIKELY]`.

### Q. My Kaggle session died at around 12 hours and I lost everything. [LIKELY]
Kaggle sessions are killed at ~12 h; a run that misses the wall **loses all its spent quota**
(`18_reproduce_from_scratch.md §18.5.3`). Protect every run:
- **Checkpoint to `/kaggle/working` every ≤30 min AND before the ~11 h wall** (one-hour margin), and
  **resume on restart**. Resume anchors are written per fold/model (`geo_pinn_fold{fold}.pt`,
  `{model}_fold{fold}.pt`, `anomaly_fold{fold}.pt`, `offline_rl.pt`, `gmf_head.pt`).
- Prefer **commit / batch runs** over interactive (idle timeout wastes quota).
The full resume contract is **chapter 11 §11.5**. `[LIKELY]`.

### Q. I ran out of my weekly GPU quota. [LIKELY]
The planning budget is ~**30 GPU-h/week**, kept to ~**25.5 usable** with a ≥15% reserve (`_CANON.md §8`);
these are **widely-published, not freshly fetched** numbers — **re-confirm them on the live Kaggle quota
panel first**. To live within it, follow **chapter 11**'s per-workstream GPU-hour budget and cut-list
(e.g. WS1 flood 5.0, landslide 2.5, anomaly 2.0, RL 1.0, media 1.0 GPU-h `[EST]`,
`18_reproduce_from_scratch.md §18.7`): train the highest-value models first, use checkpoint/resume so no quota
is wasted on a killed session, and drop the lowest-priority runs from the cut-list when the reserve is tight.
`[LIKELY]`/`[EST]`.

---

## 21.4 RESULTS / SCIENCE

### Q. My trained result differs from the number the paper reported. Is something wrong?
**Probably not.** Paper numbers are **source-reported on the paper's own data and split** (`_CANON.md §1`),
not on yours. Two structural reasons your number will differ — and usually be **lower**:
- **Different data / region / split.** You are evaluating on your data with **mandatory spatial-block CV**
  (train/val never share a spatial cell); the paper may have used random CV, which **overstates** skill. The
  grounded source `arXiv 2608.12422` shows naive terrain ROC-AUC ~0.90 collapsing to 0.76/0.71/0.54 under
  matched spatial-CV (`_CANON.md §6`, `analysis/07_claims_table.csv` C001–C003).
- **The admission bar is stricter.** A number only "counts" for TRINETRA if it passes the **real-win gate**
  (beats every baseline on spatial-CV with a bootstrap CI whose lower bound > 0). See **chapter 12**
  (`12_evaluation_and_results.md`). A lower-but-admitted number is the honest one. `[CONFIRMED]` for the
  protocol; your specific number is **UNTESTED here**.

### Q. My model doesn't beat the baseline. Did I fail?
**No — that is a valid, reportable scientific outcome, and the system is built to accept it.** The eval
harness compares against mandatory non-learned baselines (climatology, persistence, physics-rule) plus a
pure-numpy logistic learner, and `real_win` only returns `True` when the CI lower bound on the cost saving is
> 0 (`16_code_guide.md §16.5.6`, chapter 12). If your model loses, **report that** — and critically, **do not
tune on the test fold** to manufacture a win; that destroys the spatial-CV guarantee. An honest "did not beat
baseline" is a result; a tuned-on-test "win" is a Rule-16 violation. `[CONFIRMED]` for the gate behaviour.

### Q. My conformal coverage isn't exactly 90%.
Conformal coverage is **marginal and approximate**, and it degrades **under distribution shift** — exact
finite-sample coverage holds only under exchangeability. On exchangeable data the core lands within ±0.03 of
1−α (`17_testing_and_validation.md §17.3.13`). Under shift, use the adaptive variants the code already ships:
**WCPS** (weighted CP for covariate shift), **ACI** (Adaptive Conformal Inference — tracks ~90% long-run
coverage under drift), **Mondrian** (per-hazard group coverage), and **conformal risk control** (bounds the
realized miss rate). Also check the **drift monitor** (PSI/CUSUM) — a fired drift flag **voids** the CP
guarantee and should drop reliability to `Unreliable`. Details in **chapter 12**
(`16_code_guide.md §16.5.5`). `[CONFIRMED]` for the implemented behaviour.

### Q. `ReportGuard` refuses to print my metric / raises `ReportGuardError`. Is that a bug?
**No — that is R16 enforcement working.** `ReportGuard.headline()` **refuses** to emit a headline number
unless (a) spatial-CV was used, (b) baselines are registered, and (c) a **real win over every** baseline is
recorded (`16_code_guide.md §16.5.6`, `17_testing_and_validation.md §17.3.10`). The refusal means your result
has **not passed the admission gate**, so it may not be reported as skill — exactly the intended behaviour in
a life-safety domain. Add the missing spatial-CV / baselines, or accept that the metric is not admissible yet.
See chapter 12 for the full admission protocol. `[CONFIRMED]`.

---

## 21.5 EXTENDING THE CODE

All recipes below are from **chapter 16** (`16_code_guide.md §16.8`); honor §16.7.2 (new dataclass fields get
defaults; new function params are keyword-only after `*`) so the 128 tests keep passing, and keep every
Class-C path default-OFF (Rule 20). Add a matching test every time (`17_testing_and_validation.md §17.8`).

### Q. How do I add a new dataset?
Document the dataset's provenance / structure / license / splits in **chapter 04** (`04_DATASETS.md`), then
wire it for training per the **chapter 16** recipe: add a Kaggle `.npz` entry in `deep/datamodules.py`
(`KagglePaths` + a `Dataset` class exposing a `.block` array), and build `block` from lat/lon via
`datamodules.spatial_block(lat, lon)` so **train/val never share a spatial cell** (mandatory spatial-block CV,
`_CANON.md §6`, `kaggle/README.md §2`). The expected per-model `.npz` key layouts are in `kaggle/README.md §2`
and `18_reproduce_from_scratch.md §18.6`. **Licenses are not verified anywhere in this project — confirm each
dataset's license at download time before use** (`18_reproduce_from_scratch.md §18.6`). `[CONFIRMED]` for the
recipe; datasets themselves are **UNTESTED / not downloaded**.

### Q. How do I plug in a new model / expert?
Follow `16_code_guide.md §16.8.1`:
1. Implement the torch model under `src/trinetra/deep/<model>.py` (mirror `fire_cnn.py`: a `@dataclass`
   config, an `nn.Module` returning `{"logit"/"prob", …}`, a `.loss(...)`); keep it torch-only.
2. Register its **trust policy** in `ws5_fusion_rl/adapters.py` `_POLICY` as `(default_r, cap_r,
   PhysicsClass)`; at runtime `deep_expert("<source>", prob)` yields an `ExpertOutput` with the right class
   and a reliability cap (unknown sources raise `KeyError`, by design).
3. Add a Kaggle kernel under `kaggle/` and the dataset entry in `deep/datamodules.py`.
4. The expert then flows through `decide()` **unchanged** — no decision-path edits (single decision path).
5. **Add a test** in `tests/interfaces/` that the torch stub raises `MissingDependency`, and in
   `tests/fusion/` (like `test_adapters.py::test_flows_through_decide`) that `deep_expert("<source>", p)` has
   the right `cls` / capped `r` and flows through `decide()`. `[CONFIRMED]` for the recipe.

### Q. How do I add a new physics relation, a new fusion option, or a new eval baseline?
All three are in **chapter 16 §16.8**:
- **Physics relation (§16.8.2):** add the function to `ws1b_geophys/` or `ws1a_firephys/` (pure numpy, with a
  Class label and `[coeff-verify]`); if Class C it must be **default-OFF behind a `firephys.ndX` /
  `geophys.*` flag with a Class-A/B fallback**. Wire it into the package `gate.py` as a **soft** sub-signal
  (noisy-OR for geo; consistency/uncertainty for fire) — never a hard trigger. If you also add a
  differentiable PINN version in `deep/losses.py`, keep the **slope-only-via-D1 bug-guard**. Test: a
  limit/monotonicity golden in `tests/physics_golden/`, plus `test_classC_off_by_default` if Class C.
- **Fusion option (§16.8.3):** implement the operator in `ws5_fusion_rl/`, register it in
  `fusion_models.fuse()`'s dispatcher behind a `fusion.model` value (or an `operator.*` flag if Class C —
  default OFF), make sure it reports `used_classC` and **can never lower the shield floor**, and keep **FM-1
  as the fallback** when disabled or with <2 experts. Test: a property test in `tests/fusion/` plus
  `test_default_is_fm1_not_classC`.
- **Eval baseline (§16.8.4):** add it to `eval/baselines.py` (numpy/stdlib only, like `LogisticNumpy`), then
  register it as a mandatory comparator in both `pipeline/hindcast.run_hindcast` and
  `deep/train.admit_model` (call `guard.add_baseline_verdict(name, real_win(...))`). Because `ReportGuard`
  requires a real win over **every** baseline, adding one makes the gate strictly harder — exactly the intent
  (R16). Test: extend `tests/eval/` (`test_better_model_wins_worse_does_not`, `test_not_admitted_blocks_claim`).
`[CONFIRMED]` for the recipes.

---

## 21.6 Where to go next
- Zero-to-run runbook, exact commands, expected output: **chapter 18** (`18_reproduce_from_scratch.md`).
- Test suites, the `[exit code: 1]` quirk, how to add a test: **chapter 17** (`17_testing_and_validation.md`).
- Repo map, API reference, extension recipes: **chapter 16** (`16_code_guide.md`).
- Kaggle budget, resume logic, failure/fix table: **chapter 11** (`11_training_compute_kaggle.md §11.6`).
- Evaluation protocol, spatial-CV, admission gate: **chapter 12** (`12_evaluation_and_results.md`).
- The IP-address `[INFEASIBLE]` verdict and offline alerting: **chapter 08** (`08_ws3_offline_alerting.md`).
- Bugs and fixes (incl. Iverson cos²β guard, Geo-PINN DataParallel): **chapter 13** (`13_robustness_bugs_fixes.md`).
