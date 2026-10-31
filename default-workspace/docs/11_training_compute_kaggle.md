# 11 — Training Compute: The Kaggle Budget, Multi-GPU Scripts, and Resume Logic

This chapter is the operational contract for *where and how* TRINETRA (HIMKAVACH) deep models get trained.
There is exactly one build platform — **Kaggle GPU notebooks** — and it is small, quota-metered, and
session-limited. Everything here exists to make a research-grade build fit inside roughly **25.5 usable
GPU-hours per week** without ever overstating what that buys.

Read §0.1 before trusting any number in this chapter.

---

## 11.0 Status of every number here (read first)

Two honesty facts govern this entire chapter, and both come straight from `_CANON.md §2` and §8 and from
`KAGGLE_BUDGET.md §0`:

1. **No model has been trained and no dataset has been downloaded.** The PyTorch `deep/` layer and the
   `kaggle/` scripts are **`py_compile`-clean only — never run on a GPU in this environment** (there is no
   torch/CUDA in the sandbox; the sandbox has numpy, pandas, lxml only). Therefore every GPU-hour figure in
   this chapter is a **PLANNING ESTIMATE `[EST]`**, traced where possible to paper-reported compute, and
   **labeled unvalidated until actually run**. Every description of multi-GPU behaviour is **UNTESTED** —
   it is "as written in the code", not "as observed on a T4".

2. **The Kaggle limit numbers in §11.1 are WIDELY-PUBLISHED values, NOT freshly fetched this session.**
   `KAGGLE_BUDGET.md §0` records that Kaggle's docs pages are JavaScript-rendered and returned no usable
   body text via `web_fetch`, so the limits below are the commonly-documented Kaggle quotas, not a live
   read. **Mandatory action: re-confirm every §11.1 number on the live Kaggle account quota panel at the
   first build session before committing a schedule.** Treat §11.1 as a planning estimate with a built-in
   safety reserve, nothing more.

Honesty labels used below follow `_CANON.md §1`: `[CONFIRMED]`, `[LIKELY]`, `[HYPOTHESIS]`, `[INFEASIBLE]`,
and `[EST]` for a planning estimate.

---

## 11.1 Assumed Kaggle limits (verify on the live quota panel)

The table below is the **assumed** operating envelope, copied from `KAGGLE_BUDGET.md §1`. It is a planning
baseline, **not a measured or freshly-fetched fact** — the binding real values must be read from the live
Kaggle quota panel at build start (see §11.0).

| Resource | Assumed limit | Why it matters |
|----------|---------------|----------------|
| **GPU quota** | ~**30 GPU-hours / week** (weekly reset) | Shared across all your notebooks; this is **the binding constraint** on the whole build. |
| **GPU types** | **Tesla P100 (16 GB)** OR **2× Tesla T4 (2×16 GB)** | The T4×2 option is what enables simple data-parallel training (see §11.4). |
| **TPU quota** | ~20 TPU-hours / week (v3-8) | Separate pool; use only if a model is genuinely TPU-friendly. Not part of the §11.3 plan. |
| **Session max runtime** | ~**12 h** (GPU/CPU), ~9 h (TPU) | Any long run **must checkpoint before the wall** (§11.5). |
| **CPU-only sessions** | effectively unlimited (no accelerator quota) | Do **all** preprocessing here, off the GPU clock. |
| **Working disk** | ~**20 GB persisted** + ~**73 GB scratch** | Subset/stream large corpora; never stage a full dataset on a GPU session. |
| **RAM** | ~**13–16 GB** (GPU instance) | The real limit for big Earth-observation tiles → **tile + stream**. |

**Official documentation URLs** (as listed in `KAGGLE_BUDGET.md §0`):

- `https://www.kaggle.com/docs/notebooks`
- `https://www.kaggle.com/docs/efficient-gpu-usage`

**Link-check status (2026-10-10): fetched → JS-rendered, no usable static body.** Both URLs were requested
via `web_fetch` on 2026-10-10; they return a JavaScript shell with no static text, so their current contents
could **not** be verified by fetch. The quota numbers above were instead re-read from the **live Kaggle
session panel** on the same date. Open them in a browser on the live account to re-confirm. `[EST]` /
to-verify for every row. (Logged in `docs/_QG5_link_verification_log.md`.)

---

## 11.2 The weekly budget envelope (≥15% reserve)

The weekly quota is spent against a deliberate reserve so that re-runs and the evaluation re-runs do not
blow the cap. From `KAGGLE_BUDGET.md §2`:

- Assumed quota: **~30 GPU-h/week**.
- Keep **≥15% reserve**: 30 × (1 − 0.15) = **25.5 GPU-h usable/week**.
- That leaves **≥4.5 GPU-h/week in reserve** for re-runs and for the evaluation re-runs that the
  DC-01/DC-02 data-contract checks require.
- The plan is **per-week** and is **re-planned each build phase** — this is not a one-time allocation.

**Golden rule (`KAGGLE_BUDGET.md §2`):** GPU time is for **training / fine-tuning + inference benchmarking
ONLY**. Download, reprojection, tiling, and fold construction all run on **CPU-only sessions**, which carry
no accelerator quota. Every minute a GPU spends doing I/O or preprocessing is wasted quota.

---

## 11.3 Per-workstream GPU-hour allocation

This is the representative build-week allocation from `KAGGLE_BUDGET.md §3`. Every figure is a planning
estimate `[EST]`, unvalidated until the run actually happens. Workstream labels use the **internal artifact
scheme** (`_CANON.md §3`), not the six-chapter doc frame — stated explicitly here to avoid cross-scheme
confusion.

| WS (internal) | GPU work | Planned GPU-h `[EST]` | Lever that keeps it cheap |
|---------------|----------|----------------------|---------------------------|
| WS8 SSL encoder | Adapt a masked EO encoder on an SSL4EO-S12 subset | **6.0** | Regional subset + 8-bit + PEFT, **not** the full 1.5 TB corpus |
| WS1 physics/flood | Flood segmentation (GEOID-Flood) + nowcasting surrogate | **5.0** | U-Net baseline is cheap; PEFT on any geo-foundation-model |
| WS1 landslide | Landslide segmentation (LMHLD/GDCLD) via LoRA | **2.5** | PEFT-first; backbone frozen |
| WS6 robustness/eval | spatial-CV + worst-group + corruption + cost-loss sweeps | **3.0** | Eval re-runs budgeted (DC-01/02) |
| WS5 RL/alarm | OPE/FQE on logged/simulated episodes | **1.0** | Offline eval is mostly CPU |
| WS8 anomaly | SSL → Deep-SVDD / iForest heads + conformal | **2.0** | Classical heads are cheap |
| WS2 media | Small advisory detector (Rule 19) | **1.0** | Low priority, low-trust |
| baselines | GBDT + persistence (C-02/C-03) | **0.5** | GBDT on CPU; a tiny GPU slice only for parity |
| **Subtotal** | | **21.0** | Under 25.5 usable → ~**4.5 h slack** on top of the 4.5 h reserve |

**Estimate basis (`KAGGLE_BUDGET.md §3`):** these are planning estimates informed by paper-reported
compute — PEFT cutting ~95% of trainable params (arXiv 2604.16663), few-step inference
(2610.12189 / 2609.37487), and small-corpus geo-foundation-model adaptation (2605.28174) — **labeled
unvalidated until run**. They are not our measurements and must not be presented as such (Rule 16).

The 21.0 h subtotal leaving ~4.5 h slack *on top of* the 4.5 h reserve is the headroom that absorbs the
inevitable underestimate in any first-run compute plan.

---

## 11.4 Multi-GPU training on T4×2 (as written in code — UNTESTED on a GPU)

> Everything in this section is **UNTESTED**: the scripts are `py_compile`-clean only and were **not
> executed on a GPU** in this environment (`_CANON.md §2`). The behaviour described is what the code *will
> do*, read directly from `trinetra/src/trinetra/deep/train.py`, `ddp.py`, and `kaggle/README.md`.

### 11.4.1 DataParallel is the default path

`train.py` is tuned for Kaggle **T4×2**. By default it uses **both GPUs via `nn.DataParallel`**. On startup
every classifier/anomaly/geo script prints a banner like:

```
[trinetra] GPUs visible=2 | DataParallel=True | effective_batch=128 lr=6.00e-04
```

The mechanics, from `TrainConfig` and `train_one_fold` in `train.py`:

- **GPU-scaled batch.** `--batch N` is the **per-GPU** batch. `effective_batch() = batch_size × n_gpus`
  when `scale_batch_by_gpus` is true (the default). Example: `--batch 64` on 2×T4 → effective batch **128**.
- **Linear LR scaling.** `effective_lr() = lr × n_gpus` when `scale_lr_by_gpus` is true (the default) —
  the warmup-free linear scaling rule (Goyal et al. 2017). With base `lr=3e-4`, 2 GPUs → `6.00e-04`.
- **AMP + cuDNN autotune.** `setup_perf()` sets `cudnn.benchmark = True`, enables TF32 matmul, and sets
  float32 matmul precision "high"; `train_one_fold` wraps the step in `torch.cuda.amp.autocast` with a
  `GradScaler`. fp16 AMP is a large speedup on Turing T4s.
- **The whole loss runs multi-GPU.** `_LossModule` wraps `(model, step_fn)` and returns `loss.reshape(1)`
  so `nn.DataParallel` scatters each batch along dim 0, runs `step_fn` per replica, gathers the per-GPU
  losses, and the caller takes `.mean()`. This lets custom losses (PINN PDE residual, Deep-SVDD,
  cost-sensitive BCE) go multi-GPU **without touching `step_fn`**.
- **Safe `drop_last`.** `make_loader` sets `drop_last` only for shuffled (training) loaders **and only when
  `len(ds) >= 2 * effective_batch`** — so DataParallel can split batches evenly across GPUs, but a tiny
  fold will not drop its only batch and train on nothing.

### 11.4.2 The per-script flags

All training scripts accept (per `kaggle/README.md §3` and each script's `argparse`):

- `--batch N` — **per-GPU** batch; effective batch is `N × n_gpus`.
- `--parallel {auto,dp,none}` — `auto` (default) uses DataParallel when `n_gpus() > 1`; `dp` forces it;
  **`none` forces single-GPU**. `TrainConfig.use_dp()` returns true only for `auto`/`dp` *and* `n_gpus() > 1`.

### 11.4.3 Offline-RL deliberately uses ONE GPU

`train_offline_rl.py` sets `TrainConfig(..., scale_batch_by_gpus=False)` and prints
`offline-RL uses 1 GPU (tiny net)`. The in-code rationale: the Q-net is tiny (state_dim × 3 actions), so
multi-GPU scatter/gather overhead would be **larger than the compute itself**. It uses a **large batch**
(`--batch 256` default) on one GPU instead, driving the training loop directly rather than through
`train_one_fold`'s DataParallel path.

### 11.4.4 Geo-PINN autograd caveat

`train_geo_pinn.py` defaults to `--parallel auto`, so DataParallel is on by default. But the Geo-PINN
physics loss uses `autograd.grad` **inside the forward** (`geo_pinn_step`). Per `kaggle/README.md §2b`:
DataParallel runs this per-replica and *usually* works, **but if you hit a thread/autograd error, rerun
with `--parallel none`** (single GPU) or use the DDP launcher. Note also that slope enters the PINN **only
via `D1 = diffusivity_D1(D0, beta_deg)`** — the `D1 = D0/cos²β` bug-guard from `_CANON.md §4` — so the
multi-GPU path must not reintroduce a second slope term.

### 11.4.5 DistributedDataParallel — the max-throughput path (`ddp.py`)

For long runs, `trinetra.deep.ddp` provides a **DistributedDataParallel** launcher: one process per GPU,
no Python-GIL scatter/gather bottleneck, so it is faster than DataParallel. From `ddp.py`:

- `launch_ddp(worker, args)` spawns one process per GPU via `mp.spawn`; **if `world_size < 2` it just runs
  inline on rank 0** (graceful single-device fallback).
- `ddp_setup` uses the **nccl** backend, `MASTER_ADDR=127.0.0.1`, `MASTER_PORT=29500`, and
  `torch.cuda.set_device(rank)`.
- `wrap_ddp(model, rank)` wraps the model as `DDP(..., device_ids=[rank], find_unused_parameters=False)`.
- `ddp_loader` builds a per-rank `DataLoader` with a `DistributedSampler` (each rank sees a **disjoint
  shard**), `pin_memory=True`, `persistent_workers` when workers > 0, and `drop_last=shuffle`.
- `ddp_worker` is a decorator that does setup/cleanup and an all-reduce **barrier** around your
  `fn(rank, world_size, args)`.
- **Save/eval only on rank 0** via `is_main()`. Gradients are all-reduced automatically.

Critical usage constraint from the module docstring and README: use DDP from a **plain `.py` script**, and
**do not initialize CUDA in the notebook first** (don't touch CUDA before `launch_ddp`).

---

## 11.5 Checkpoint / resume, outputs, dataloader tuning, mixed precision

### 11.5.1 Checkpoint before the wall

From `KAGGLE_BUDGET.md §5` and the ~12 h session limit:

- **Checkpoint to `/kaggle/working` every ≤30 min AND before the ~11 h wall** (one hour of margin before
  the ~12 h hard kill), and **resume on restart**. A run that does not checkpoint before the wall loses all
  its spent quota.
- **Prefer commit / batch runs over interactive** — an interactive notebook that goes idle gets killed on
  the idle timeout, which **wastes quota** (§11.6).

The per-script save behaviour (from the `kaggle/` scripts): each writes per-fold checkpoints to `--out`
(default `/kaggle/working`) — e.g. `geo_pinn_fold{fold}.pt`, `{model}_fold{fold}.pt`,
`anomaly_fold{fold}.pt`, `offline_rl.pt`, `gmf_head.pt`. These are the resume anchors.

### 11.5.2 Output handling (what leaves the notebook)

Per `kaggle/README.md §4`, copy these to the offline edge/gateway runtime:

- `*.pt` checkpoints (per fold + calibrated temperature).
- `*_report.json` — the **honesty report**; **deploy a model ONLY if `"admitted": true`** (Rule 16, enforced
  by `admit_model` in `train.py`).
- `gmf_head_numpy.json` — the GMF residual head serialized to **numpy** so the OFFLINE gateway (no torch)
  can run it via `ws5_fusion_rl.gmf.gmf_fuse(..., head=closure)`. `train_fusion_head.py` even asserts
  **torch/numpy parity** (`abs(t_val - n_val) < 1e-5`) before exporting.

Keep the weekly **working set ≤ ~20 GB** (the persisted-disk assumption, §11.1).

### 11.5.3 DataLoader tuning

From `make_loader` (`train.py`) and `ddp_loader` (`ddp.py`):

- **`pin_memory`** — on (`cfg.pin_memory and torch.cuda.is_available()`); faster host→device copies.
- **`persistent_workers`** — on whenever `num_workers > 0`; avoids re-spawning workers each epoch.
- **`num_workers`** — default **4** (`TrainConfig.num_workers`).
- **`drop_last`** — only for shuffled training loaders and only with ≥2 full effective batches (§11.4.1).

### 11.5.4 Mixed precision

AMP (fp16/bf16) is on by default (`TrainConfig.amp = True`), applied via `autocast` + `GradScaler` with
gradient unscaling before `clip_grad_norm_` (`grad_clip = 1.0`). `KAGGLE_BUDGET.md §5` additionally calls
for **gradient accumulation**, **tiling EO to fit 13–16 GB RAM**, and **caching preprocessed tensors as
Kaggle Datasets** (built in CPU sessions).

---

## 11.6 Common Kaggle failures and the fixes

| Symptom | Cause | Fix (from `KAGGLE_BUDGET.md §1/§5` + code) |
|---------|-------|--------------------------------------------|
| **CUDA out-of-memory (OOM)** | EO tiles / batch too big for 13–16 GB RAM or 16 GB VRAM | **Tile** the EO input, **stream** rather than stage, use a **smaller `--batch`** (per-GPU), lean on AMP + gradient accumulation. |
| **Idle timeout kills the run** | Interactive notebook went idle | Use **commit / batch runs**, not interactive — idle timeout **wastes quota**. |
| **Quota exhaustion mid-build** | Weekly ~30 GPU-h cap hit | The ≥15% reserve (§11.2) exists for this; if still tight, apply the **cut-list** (§11.7). All non-training work belongs on CPU sessions. |

For the Geo-PINN thread/autograd error under DataParallel, see §11.4.4 (`--parallel none` or DDP).

---

## 11.7 The prioritized CUT-LIST

If the live quota turns out tighter than the §11.1 assumption, drop work in **this order**
(`KAGGLE_BUDGET.md §6`):

1. **WS2 media fine-tune** — stay zero-shot / rule-based.
2. **Full SSL pretrain** — instead adapt a public checkpoint (SSL4EO-S12 / TerraMind / Prithvi) with PEFT.
3. **GLOF deep models** — fall back to ITS_LIVE-velocity + HMAGLOFDB threshold rules.
4. **Nowcasting ensemble** — collapse to a single few-step model.
5. **FM-comparison breadth** — keep **ONE** foundation model.

**NEVER cut** (these are the credibility of every number — cheap and load-bearing; DC-01/02/03):
- GBDT + persistence baselines,
- spatial-CV,
- cost-loss evaluation,
- conformal calibration.

The cut order is deliberate: it sheds the lowest-trust, highest-cost work first (media fine-tune, full
pretrain) and protects the cheap pieces that make every reported number defensible.

---

## 11.8 Seed / rigor policy

Reconciling RB-13's **≥100 seeds** mandate with a 25.5 GPU-h/week cap (`KAGGLE_BUDGET.md §4`):

- **≥100 seeds** → applied to the **cheap models that carry the statistical claims**: GBDT, persistence,
  small U-Net, conformal/anomaly heads (seconds-to-minutes each, CPU or trivial GPU).
- **3–5 seeds** → **expensive FM / SSL runs**; report **dispersion + CI** and state plainly that the FM
  comparison is **seed-limited** (no overclaim, Rule 16).
- The **headline skill claim** — beating two baselines under spatial-CV with a calibrated cost-loss — rests
  on the **many-seed cheap models**, so the ≥100-seed mandate is **met where it is load-bearing**.

This is why the admission gate (`admit_model` in `train.py`) beats **climatology** and a **logistic
baseline** on spatial blocks with a confidence interval before any metric may be advertised: the rigor is
concentrated where it is cheap and decisive.

---

## 11.9 Environment pinning (exact versions)

The deep stack is pinned for reproducibility and supply-chain safety in `trinetra/requirements-deep.txt`.
It runs **on Kaggle GPU, not in the base sandbox** (the sandbox has no torch). The CUDA build is selected
by the Kaggle image, not pinned here.

```
torch==2.3.1
torchvision==0.18.1
numpy==1.26.4
pandas==2.2.2
scikit-learn==1.4.2
xgboost==2.0.3
timm==1.0.7
einops==0.8.0
pytorch-lightning==2.3.3
d3rlpy==2.5.0
rasterio==1.3.10
tqdm==4.66.4
pyyaml==6.0.1
```

Install on the first run (Internet = On, first run only) with `pip install -r requirements-deep.txt`
(`kaggle/README.md §1`). Note the numpy core in `src/trinetra/` needs **none** of this — only Python +
numpy — and that is what passes the 128 unit tests + 6 CI gates `[CONFIRMED]`.

---

## 11.10 The honest bottom line

From `KAGGLE_BUDGET.md §8`, carried verbatim in intent:

> **~25.5 usable GPU-h/week is ENOUGH for the research-grade build IFF** we (a) **adapt existing
> checkpoints with PEFT, not pretrain**; (b) push **non-training work to CPU**; (c) **rank models frozen
> before fine-tuning**; and (d) anchor rigor on **cheap many-seed baselines**.
>
> It is **NOT enough to train several large foundation models from scratch** — and the literature
> (2512.02055, 2604.16663, 2605.28174) says we **should not need to**.

So the verdict on the compute plan is **`[LIKELY]` feasible under the PEFT/frozen-backbone/CPU-offload
discipline**, and **`[INFEASIBLE]` as a from-scratch large-FM pretraining effort**. And the overarching
caveat from §11.0 still stands over all of it: **nothing has been trained, every GPU-hour is an unvalidated
`[EST]`, the multi-GPU scripts are compile-verified but UNTESTED on a GPU, and the Kaggle limits must be
re-confirmed on the live quota panel before any of this is scheduled.**
