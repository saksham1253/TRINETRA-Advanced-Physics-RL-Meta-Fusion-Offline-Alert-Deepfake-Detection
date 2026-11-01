# 18 — Reproduce From Scratch: The Zero-to-Results Runbook

This is the strictly ordered runbook that takes a new engineer from an empty machine to the **only results
TRINETRA (HIMKAVACH) can actually produce today**: the numpy core passing **128 unit tests + 6 CI gates**
and an **end-to-end advisory decision** from `demo.py`. Every command below is real and copy-pasteable.

Read §18.0 before running anything — it tells you exactly what is reproducible and what is not.

---

## 18.0 What this runbook can and cannot give you (read first)

This project has two layers (`_CANON.md §0`, `00_README_START_HERE.md §0.1`), and this runbook treats them
very differently:

- **The numpy core** (physics gates, fusion math, conformal, cost-loss, baselines, safety shield, decision
  function, CAP builder) is **pure numpy + stdlib** and is **fully reproducible on this machine right now**.
  Everything in STEPS 1–3 below was executed in this environment and the checkpoints are the **real
  observed output** `[CONFIRMED]`.
- **The deep / GPU / Kaggle layer** (PyTorch `deep/` models + `kaggle/` training scripts) is
  **`py_compile`-clean only and was never run on a GPU here** — there is no torch/CUDA/GPU and no dataset in
  this sandbox (`_CANON.md §2`: available libraries are numpy, pandas, lxml only). Every GPU/training/dataset
  step in STEPS 4–5 is therefore marked **UNTESTED**; its commands are "what a future user *would* run",
  taken verbatim from each script's real `argparse`, and all runtimes are planning estimates `[EST]`.

> **No TRINETRA model has been trained and no dataset has been downloaded** (`_CANON.md §0`). Nothing in this
> runbook produces a measured accuracy, skill, latency, recall, false-alarm, or cost number for TRINETRA. The
> `demo.py` hindcast even prints `admitted=False` on its own synthetic data — that is the honesty gate working,
> not a result. See the honesty box in §18.9.

Honesty labels follow `_CANON.md §1`: `[CONFIRMED]`, `[LIKELY]`, `[HYPOTHESIS]`, `[INFEASIBLE]`, plus `[EST]`
for a planning estimate and **UNTESTED** for anything not executed in this environment.

---

## 18.1 PREREQUISITES

### Operating system
- Developed and validated on **Windows** (this environment). The numpy core is pure Python + numpy and is
  OS-independent `[LIKELY]`; only the exact interpreter path below is Windows-specific.

### Python version
- **`requires-python = ">=3.11"`** (from `trinetra/pyproject.toml`). Use Python 3.11 or newer.

### Exact interpreter used here (so you can reproduce the checkpoints byte-for-byte)
```
C:\Users\Dell\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe
```
On Windows, set UTF-8 output first so unittest's summary renders cleanly:
```powershell
$env:PYTHONIOENCODING = "utf-8"
```
(`_CANON.md §2` records this interpreter + env var as what produced the 128-tests / 6-gates result.)

### The two install tiers

| Tier | Install | What it unlocks | Runs here? |
|------|---------|-----------------|------------|
| **CORE** | `pip install -e .` (declares `numpy, pandas, lxml` per `pyproject.toml`) | The **entire numpy pipeline**: all 128 unit tests, all 6 CI gates, and the end-to-end `demo.py` advisory decision. The code itself needs only **numpy + stdlib** (`trinetra/README.md`). | **Yes — [CONFIRMED]** |
| **DEEP** | `pip install -r requirements-deep.txt` (torch 2.3.1, torchvision, scikit-learn, xgboost, timm, einops, pytorch-lightning, d3rlpy, rasterio, tqdm, pyyaml; `numpy==1.26.4`, `pandas==2.2.2` pinned) | The PyTorch `deep/` models + the `kaggle/` training scripts. **Needs a GPU** (CUDA build is chosen by the Kaggle image, not pinned). | **No — UNTESTED** (no torch/GPU here, `_CANON.md §2`) |

> CORE is enough for STEPS 1–3. You do **not** need the DEEP tier, a GPU, or any dataset for the quick-start
> results. The `pyproject.toml` core line declares `numpy, pandas, lxml`; the test/CI/demo code paths
> exercised in STEPS 2–3 use **only numpy + stdlib** (`trinetra/README.md`, `_CANON.md §2`).
>
> **Exact CORE runtime that produced the only `[CONFIRMED]` result (recorded 2026-10-10 via
> `python -c "import sys,numpy,pandas,lxml"`):** Python **3.12.14**, **numpy 2.3.5**, **pandas 3.0.1**,
> **lxml 6.1.3**, on Windows-11 (10.0.26300). The 128 tests + 6 CI gates passed on exactly this stack. The
> code targets `requires-python>=3.11` and is numpy-2.x-clean (it uses `np.ptp(arr)` not the removed
> `arr.ptp()`), so any numpy ≥2.0 should reproduce; numpy **1.x will NOT** because of that API change
> (see ch21). Pin `numpy>=2.0` for byte-faithful reproduction of the CONFIRMED run.

---

## 18.2 STEP 1 — Get the repo and do the CORE editable install  `[CONFIRMED]`

```powershell
# 1. Obtain the code: clone your repo, or copy the `trinetra/` folder onto the machine.
#    Then enter the package root (the folder that contains pyproject.toml, run_tests.py, demo.py).
cd trinetra

# 2. (recommended) create + activate a clean virtual env on Python >= 3.11
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell

# 3. CORE editable install — pulls numpy/pandas/lxml only; NO torch, NO GPU needed.
pip install -e .
```

**Checkpoint:** `pip install -e .` completes without error and `python -c "import trinetra, numpy"` prints
nothing (success). `[CONFIRMED]` — the core imports with numpy + stdlib only.

> Note: `run_tests.py`, `scripts/ci_gates.py`, and `demo.py` each insert `src/` onto `sys.path` themselves,
> so they also run straight from the repo root **without** `pip install -e .` as long as numpy is importable.
> The editable install is the clean, canonical way; the direct-run path is the fallback.

---

## 18.3 STEP 2 — Run the test suite + CI gates  `[CONFIRMED]`

```powershell
$env:PYTHONIOENCODING = "utf-8"
python run_tests.py            # stdlib unittest discovery over tests/ (pytest not required)
python scripts/ci_gates.py     # 6 fail-closed SAFETY/HONESTY gates
```

**Checkpoint — this is the EXACT output observed in this environment** (last lines):

```
----------------------------------------------------------------------
Ran 128 tests in 0.477s

OK
```
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

You should see **`Ran 128 tests ... OK`** and **`ALL 6 CI GATES PASSED`**. `[CONFIRMED]`

> **Known quirk:** `run_tests.py` may show a spurious `[exit code: 1]` after `OK` because `unittest` writes
> its summary to **stderr**; the real pass signal is the final line **`OK`** (also noted in
> `00_README_START_HERE.md §0.4`). `ci_gates.py` exits 0 cleanly.

The 6 gates are safety/honesty invariants, **not** performance tests (`scripts/ci_gates.py` header):
`G-advisory` (CAP refuses to build without a human approval token — Rule 19), `G-classC` (PHARAOH + ND-1..7
default OFF — Rule 20), `G-security` (empty endpoint allow-list rejects all; raw video cannot egress —
C6/C7), `G-leak` (future feature timestamps rejected — G6), `G-iot` (LoRa frame ≤ 51 B — G5), `G-legacy`
(no banned buggy-code tokens in `src/`).

---

## 18.4 STEP 3 — Run the end-to-end advisory demo  `[CONFIRMED]`

```powershell
$env:PYTHONIOENCODING = "utf-8"
python demo.py                 # == python -m trinetra.pipeline.demo (demo.py just adds src/ to sys.path)
```

**Checkpoint — the real observed output** (synthetic evidence; no performance claim):

```
==============================================================================
TRINETRA / HIMKAVACH — end-to-end ADVISORY demo (synthetic, no performance claims)
==============================================================================

[Fukuzono] forecast failure t_f ≈ 35.7 h (r2=0.973)

--- OPERATOR BRIEFING -------------------------------------------------------
[ADVISORY] zone=UK-CHX-07 hazard=LANDSLIDE level=RED risk=0.889
  conformal set=['ORANGE', 'RED'] target=0.90 reliability=Medium
  shield: raised=True floor=RED reason=tilt_rate>5deg/day corroborated by 3 nodes; 24h rain>150mm on high-susceptibility slope
  uncertain=False  used_classC=False  fusion=FM-1
  contributions:
    - geo_phys: p=1.00 u=0.17 c=0.85 r=1.00 cls=A avail=True
    - anomaly: p=0.67 u=0.30 c=0.80 r=0.70 cls=data avail=True
  --> ACTION REQUIRED: human operator must review and approve before any public alert.

--- OFFLINE PATH (cloud down) -----------------------------------------------
node edge flag = LOCAL_SIREN (tilt_rate>=siren AND rain>=watch (two cues))
siren events   = [('node_edge', 'LOCAL_SIREN'), ('shield', 'RED')]
DTN pending    = ['UK-CHX-07:2026-10-10T11:43:23.897473+00:00']
note           = local siren + DTN rebroadcast; public CAP deferred to human (Rule 19)

--- HUMAN-GATED PUBLIC ALERT ------------------------------------------------
<?xml version='1.0' encoding='UTF-8'?>
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">
  <identifier>urn:trinetra:UK-CHX-07:20261010T114323Z</identifier>
  <sender>TRINETRA-SDMA-UK</sender>
  ... (CAP 1.2 XML: event=LANDSLIDE urgency=Immediate severity=Extreme certainty=Observed, advisory=true) ...

--- HINDCAST (honesty gate) -------------------------------------------------
noise model : admitted=False  value_scores={'model': -0.097, 'climatology': 0.0, 'logistic': 0.583}
informative : admitted=False  value_scores={'model': 0.045, 'climatology': 0.0, 'logistic': 0.583}

Note: 'admitted' only means it beat baselines on spatial-CV with CI on THIS synthetic data.
```

**What this checkpoint proves (and does not):**
- It demonstrates the **full advisory pipeline wiring** end-to-end: a Fukuzono inverse-velocity forecast, a
  fused + conformal + shielded **advisory RED** decision (`used_classC=False`, `fusion=FM-1` — the Class-A/B
  default path per `_CANON.md §4`), the offline siren/DTN fallback, a **human-gated** CAP 1.2 message, and
  the hindcast honesty gate. `[CONFIRMED]` the code path runs.
- It is **not** a performance result. The evidence is synthetic, and the hindcast deliberately prints
  **`admitted=False`** for both models — exactly the Rule-16 behaviour: nothing may claim skill until it
  beats climatology + logistic baselines on spatial-CV with a CI on real data.

---

## 18.5 STEP 4 — Kaggle GPU training path  **(UNTESTED here — no torch/GPU/datasets)**

> **UNTESTED.** None of the commands in this step were executed in this environment: there is no
> torch/CUDA/GPU and no dataset here (`_CANON.md §2`). The flags below are read **verbatim from each script's
> real `argparse`**; the runtimes are planning estimates `[EST]`. Do not read any of this as "observed".
> **Before scheduling any of it, re-confirm your live Kaggle quota first** — see **chapter 11**
> (`11_training_compute_kaggle.md`), which is the operational contract for the ~25.5 usable GPU-h/week budget.

### 18.5.1 Set up the Kaggle session (`trinetra/kaggle/README.md §1`)
1. New Notebook/Script → **Settings → Accelerator = GPU T4 ×2** (or P100), **Internet = On** (first run only,
   so pip can resolve `requirements-deep.txt`).
2. Add this repo as a **Kaggle Dataset** (or from GitHub) so `src/` is importable.
3. Attach your datasets; loaders default to `/kaggle/input/<slug>` (`deep.datamodules.KagglePaths`).

Install the DEEP tier (first run only):
```bash
pip install -r requirements-deep.txt
```

### 18.5.2 Per-script training commands — REAL flags from each `argparse`

All training scripts share the GPU-scaling flags (from `train.py` `TrainConfig` + `kaggle/README.md §2b/§3`):
`--batch N` is the **PER-GPU** batch (effective batch = `N × n_gpus`, LR scaled linearly, Goyal 2017), and
`--parallel {auto,dp,none}` (`auto` = DataParallel when `n_gpus()>1`; `dp` forces it; `none` forces
single-GPU). On startup each script prints a banner like
`[trinetra] GPUs visible=2 | DataParallel=True | effective_batch=128 lr=6.00e-04`.

**Geo-PINN** — `kaggle/train_geo_pinn.py` (flags: `--data` (required), `--out` default `/kaggle/working`,
`--epochs` default **30**, `--D0` default **2e-4**, `--beta_deg` default **35.0**, `--batch` default **64**,
`--parallel` default **auto**). Slope enters **only** via `D1 = diffusivity_D1(D0, beta_deg)` — the
`D1 = D0/cos²β` bug-guard (`_CANON.md §4`).
```bash
python kaggle/train_geo_pinn.py --data /kaggle/input/trinetra-geo/geo.npz --out /kaggle/working
# optional: --epochs 30 --D0 2e-4 --beta_deg 35.0 --batch 64 --parallel auto
```
> Geo-PINN caveat (`kaggle/README.md §2b`, chapter 11 §11.4.4): its physics loss uses `autograd.grad` inside
> the forward; DataParallel *usually* works but on a thread/autograd error rerun with **`--parallel none`**
> or use the DDP launcher.

**Classifier (fire | eo | deepfake)** — `kaggle/train_classifier.py` (flags: `--model` (required, choices
`fire,eo,deepfake`), `--data` (required), `--out` default `/kaggle/working`, `--epochs` default **20**,
`--batch` default **64**, `--parallel` default **auto**).
```bash
python kaggle/train_classifier.py --model fire     --data /kaggle/input/trinetra-fire/fire.npz   --out /kaggle/working
python kaggle/train_classifier.py --model eo       --data /kaggle/input/trinetra-eo/eo.npz       --out /kaggle/working
python kaggle/train_classifier.py --model deepfake --data /kaggle/input/trinetra-media/media.npz --out /kaggle/working
```

**Deep anomaly** — `kaggle/train_anomaly.py` (flags: `--data` (required), `--out` default `/kaggle/working`,
`--epochs` default **25**, `--batch` default **64**, `--parallel` default **auto**). Trains on **NORMAL
windows only** (`y==0`); events become out-of-distribution and score high.
```bash
python kaggle/train_anomaly.py --data /kaggle/input/trinetra-telemetry/tele.npz --out /kaggle/working
```

**Offline-RL** — `kaggle/train_offline_rl.py` (flags: `--data` (required), `--out` default `/kaggle/working`,
`--epochs` default **50**, `--gamma` default **0.0**, `--batch` default **256**). **Deliberately 1 GPU**
(`scale_batch_by_gpus=False`): the Q-net is tiny, so scatter/gather would cost more than it saves; it uses a
large batch instead. Prints `offline-RL uses 1 GPU (tiny net)`.
```bash
python kaggle/train_offline_rl.py --data /kaggle/input/trinetra-rl-logs/logs.npz --out /kaggle/working
# optional: --epochs 50 --gamma 0.0 --batch 256
```

**Fusion head (GMF)** — `kaggle/train_fusion_head.py` (flags: `--data` (required; `.npz` with keys
`base,dispersion,salience,y`), `--out` default `/kaggle/working`, `--cap` default **0.1**, `--epochs`
default **300**). Learns the bounded residual head, then **exports it to numpy** and asserts torch/numpy
parity (`abs(t_val-n_val) < 1e-5`) before writing.
```bash
python kaggle/train_fusion_head.py --data /kaggle/working/fusion_cache.npz --out /kaggle/working
```

### 18.5.3 Checkpoint / resume  (UNTESTED; chapter 11 §11.5)
- Checkpoint to `/kaggle/working` **every ≤30 min AND before the ~11 h wall** (one hour margin before the
  ~12 h session kill); **resume on restart**. A run that misses the wall loses all its spent quota.
- Resume anchors written per fold/model: `geo_pinn_fold{fold}.pt`, `{model}_fold{fold}.pt`,
  `anomaly_fold{fold}.pt`, `offline_rl.pt`, `gmf_head.pt`.
- Prefer **commit / batch runs** over interactive (idle timeout wastes quota).

### 18.5.4 The admission-gate report JSON — the only thing that may claim skill (UNTESTED)
Each script with labels runs `admit_model(...)` on spatial-CV and writes a `*_report.json` honesty report
(`train_geo_pinn.py`, `train_classifier.py`, `train_anomaly.py` → `admit_model`; `train_offline_rl.py` →
`ope_admission` → `offline_rl_report.json`). **Deploy a model ONLY if `"admitted": true`** (Rule 16, enforced
in `train.py`); offline-RL deploys the learned policy only if `deploy_learned` is true (else it keeps the
rule baseline — Rule 19 fail-safe). Copy to the edge runtime: `*.pt` checkpoints, `*_report.json`, and
`gmf_head_numpy.json` (the numpy-serialized GMF head so the torch-free offline gateway can run it).
These reports are **not produced in this environment** — UNTESTED.

---

## 18.6 STEP 5 — Datasets  **(UNTESTED — NONE downloaded, licenses unverified)**

> **UNTESTED.** **No dataset has been downloaded** in this environment (`_CANON.md §0`), so there is no EDA,
> no split construction, and no verified license here.

- The `kaggle/README.md §2` `.npz` layout (what you must *build* from raw sources) is: Geo-PINN `trinetra-geo`
  (`Z,t,rain,static[,label,lat,lon]`); Fire/smoke `trinetra-fire` (`images (N,T,C,H,W), labels (N,2), block`);
  EO head `trinetra-eo` (`images (N,C,H,W), labels (N,), block`); Deep anomaly `trinetra-telemetry`
  (`X (N,C,T)[, y, block]`, NORMAL only); Deepfake `trinetra-media` (`images (N,C,H,W), labels (N,), block`);
  Offline-RL `trinetra-rl-logs` (`s,a,r,s_next,done,behavior_prob`). Build `block` from lat/lon via
  `datamodules.spatial_block(lat, lon)` so train/val never share a cell (mandatory spatial-block CV,
  `_CANON.md §6`).
- **Dataset provenance, structure, licenses, splits, and download code are documented in chapter 04**
  (`04_DATASETS.md`; sources `DATASETS.md`, `DATASETS_CATALOGUE.md` per `_CANON.md §9`). Licenses are
  **not verified here** — confirm each dataset's license at download time before use.

---

## 18.7 EXPECTED RUNTIMES

| Step | Command | Runtime | Label |
|------|---------|---------|-------|
| Test suite | `python run_tests.py` | **~0.47 s** (observed; wall-clock varies run-to-run, e.g. 0.468–0.477 s; `Ran 128 tests ... OK`) | `[CONFIRMED]` |
| CI gates | `python scripts/ci_gates.py` | **< 1 s** (observed; all 6 PASS, sub-second) | `[CONFIRMED]` |
| Demo | `python demo.py` | **< 1 s** (observed; advisory RED + CAP + hindcast) | `[CONFIRMED]` |
| CORE install | `pip install -e .` | seconds–minutes (network-dependent) | `[CONFIRMED]` runnable here |
| DEEP install | `pip install -r requirements-deep.txt` | minutes (Kaggle, first run) | `[EST]`, UNTESTED |
| Geo-PINN / classifiers / anomaly / RL / fusion training | STEP 4 commands | GPU-hours — **planning only**; see chapter 11 §11.3 (e.g. WS1 flood 5.0, landslide 2.5, anomaly 2.0, RL 1.0, media 1.0 GPU-h `[EST]`) | **UNTESTED**, `[EST]` |

Local steps = **observed seconds** `[CONFIRMED]`. All GPU steps are **planning estimates** `[EST]` only —
nothing was trained; see chapter 11 for the full per-workstream GPU-hour allocation and the mandatory
"re-confirm the live quota first" caveat.

---

## 18.8 TROUBLESHOOTING

For "error X — what now?", "my result differs from a paper", "how do I add a dataset", OOM / idle-timeout /
quota failures on Kaggle, and the `run_tests.py` stderr `[exit code: 1]` quirk, see **chapter 21**
(`21_faq_troubleshooting.md`). Kaggle-specific failure/fix table is also in chapter 11 §11.6.

---

## 18.9 Honesty box — what you CAN and CANNOT reproduce today

**You CAN reproduce right now (local, no GPU, no datasets) — `[CONFIRMED]` by running:**
- `python run_tests.py` → **`Ran 128 tests in 0.477s` / `OK`**.
- `python scripts/ci_gates.py` → **`ALL 6 CI GATES PASSED`**.
- `python demo.py` → the **end-to-end advisory decision** (Fukuzono `t_f ≈ 35.7 h`; fused + shielded
  **advisory RED**, `risk=0.889`, human-gated CAP; hindcast honestly `admitted=False`).

**You CANNOT reproduce today — not measured, not run here:**
- **Any skill / accuracy / recall / false-alarm / latency / cost number** for TRINETRA — **none exist**; the
  only "admitted" signal anywhere is on synthetic demo data and it reads `admitted=False`.
- **Any trained model** — the PyTorch `deep/` + `kaggle/` layer is `py_compile`-clean only and was **never
  run on a GPU** here (no torch/CUDA/GPU).
- **Any dataset EDA / split / license verification** — **no dataset has been downloaded**.

This is the deliberate, honesty-first state of a life-safety project (`_CANON.md §0`,
`00_README_START_HERE.md §0.1`), not a documentation gap.
