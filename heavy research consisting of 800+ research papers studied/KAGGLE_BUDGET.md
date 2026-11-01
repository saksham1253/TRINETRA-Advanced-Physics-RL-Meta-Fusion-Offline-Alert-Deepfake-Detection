# KAGGLE_BUDGET — planning-level compute budget (MASTER_PROMPT §0.10)
# RESEARCH-ONLY: this is a PLAN, not a run. No training happens in this program.

## Hard constraints (from master program)
- Build compute = Kaggle ONLY.
- Weekly budget ≈ 25–30 GPU-hours/week.
- Keep ≥15% reserve (so plan to ≈21–25.5 GPU-h/week usable).
- Kaggle session limits (verify in P5): ~30 GPU-h/week quota, ~9–12 h max session,
  P100/T4x2 class accelerators.

## Allocation plan (filled per workstream in P5+; placeholder now)
| WS | Component | Est. GPU-h | Source of estimate | Fits weekly? |
|----|-----------|-----------|--------------------|--------------|
| _(populated P5+)_ | | | from hyperparameter_register | |

## Rules
- Every estimate traces to a paper's reported compute (09_hyperparameter_register.md) or is
  labeled "planning estimate, unvalidated".
- Running total must respect the weekly cap with reserve; if a plan exceeds it, record the
  overflow and propose a smaller-footprint alternative (distillation, fewer seeds, subset).

---

# ===================== P5 POPULATED COMPUTE PLAN (2026-10-07) =====================

## 0. VERIFICATION STATUS (hard honesty, §0.5)
Kaggle's docs pages (https://www.kaggle.com/docs/notebooks, https://www.kaggle.com/docs/efficient-gpu-usage)
are JS-rendered and returned NO usable body text via web_fetch this session → the numbers in §1 are the
WIDELY-PUBLISHED Kaggle limits as commonly documented, NOT freshly fetched from a static page.
**ACTION: re-confirm every §1 number from the live Kaggle account quota panel at the first build session
before committing a schedule.** §1 is a planning estimate with a built-in safety reserve.

## 1. ASSUMED KAGGLE LIMITS (verify at session start)
| Resource | Assumed limit | Notes |
|----------|---------------|-------|
| GPU quota | ~30 GPU-hours / week (weekly reset) | shared across notebooks; the binding constraint |
| GPU types | Tesla P100 (16 GB) OR 2× Tesla T4 (2×16 GB) | T4×2 enables simple data-parallel |
| TPU quota | ~20 TPU-hours / week (v3-8) | separate pool; only if model is TPU-friendly |
| Session max runtime | ~12 h (GPU/CPU), ~9 h (TPU) | long runs MUST checkpoint before the wall |
| CPU-only | effectively unlimited (no accelerator quota) | do ALL preprocessing here, off the GPU clock |
| Working disk | ~20 GB persisted + ~73 GB scratch | subset/stream large corpora |
| RAM | ~13–16 GB (GPU instance) | real limit for big EO tiles → tile + stream |

## 2. BUDGET ENVELOPE (≥15% reserve)
- Usable GPU: 30 × (1 − 0.15) = **25.5 GPU-h usable/week**; **≥4.5 GPU-h reserve** for re-runs + the
  eval re-runs DC-01/DC-02 require. Plan is PER-WEEK, re-planned each build phase.
- Golden rule: GPU time = training/fine-tune + inference benchmarking ONLY. Download/reproject/tile/
  fold-construction run on CPU-only sessions.

## 3. PER-WORKSTREAM GPU ALLOCATION (representative build-week; re-planned per phase)
| WS | GPU work | Planned GPU-h | Lever |
|----|----------|---------------|-------|
| WS8 SSL encoder | adapt masked EO encoder on SSL4EO-S12 subset | 6.0 | regional subset + 8-bit + PEFT, not full 1.5 TB |
| WS1 physics/flood | flood seg (GEOID-Flood) + nowcasting surrogate | 5.0 | U-Net baseline cheap; PEFT on any GFM |
| WS1 landslide | landslide seg (LMHLD/GDCLD) via LoRA | 2.5 | PEFT-first; backbone frozen |
| WS6 robustness/eval | spatial-CV + worst-group + corruption + cost-loss sweeps | 3.0 | eval re-runs budgeted (DC-01/02) |
| WS5 RL/alarm | OPE/FQE on logged/sim episodes | 1.0 | offline eval mostly CPU |
| WS8 anomaly | SSL→Deep-SVDD/iForest heads + conformal | 2.0 | classical heads cheap |
| WS2 media | small advisory detector (Rule 19) | 1.0 | low priority, low-trust |
| baselines | GBDT + persistence (C-02/C-03) | 0.5 | GBDT on CPU; tiny GPU for parity |
| **Subtotal** | | **21.0** | under 25.5 usable → ~4.5 h slack on top of 4.5 h reserve |
Estimate basis: planning estimates informed by paper-reported compute (PEFT −95% params 2604.16663;
few-step inference 2610.12189/2609.37487; small-corpus GFM 2605.28174), labeled unvalidated until run.

## 4. SEED / RIGOR POLICY (reconciling RB-13's ≥100 seeds with the budget)
- ≥100 seeds → applied to CHEAP models carrying the statistical claims (GBDT, persistence, small U-Net,
  conformal/anomaly heads: seconds–minutes each, CPU/trivial GPU).
- 3–5 seeds → expensive FM/SSL runs; report dispersion + CI; state the FM comparison is seed-limited
  (no overclaim, Rule 16).
- Headline skill claim (beat two baselines under spatial-CV w/ calibrated cost-loss) rests on the
  many-seed cheap models → the ≥100-seed mandate is met where it is load-bearing.

## 5. SCHEDULING / CHECKPOINT / EFFICIENCY
- Checkpoint to /kaggle/working every ≤30 min and before the ~11 h wall; resume on restart.
- Prefer commit/batch runs over interactive (idle-timeout wastes quota).
- Mixed precision (fp16/bf16); gradient accumulation; tile EO to fit 13–16 GB RAM; cache preprocessed
  tensors as Kaggle Datasets (built in CPU sessions).
- PEFT-first (LoRA/AdaLoRA); frozen-backbone probing to RANK models before any full fine-tune; few-step
  generative inference for nowcasting.

## 6. CUT-LIST (dropped first if quota is tighter than assumed)
1. WS2 media fine-tune (stay zero-shot/rule-based). 2. Full SSL pretrain → adapt a public checkpoint
(SSL4EO-S12/TerraMind/Prithvi) with PEFT. 3. GLOF deep models → ITS_LIVE-velocity + HMAGLOFDB threshold
rules. 4. Nowcasting ensemble → single few-step model. 5. FM-comparison breadth (keep ONE FM).
NEVER cut: GBDT + persistence baselines, spatial-CV, cost-loss eval, conformal calibration (cheap + they
are the credibility of every number; DC-01/02/03).

## 7. STORAGE PLAN
Build sensor cubes per-event in CPU sessions, save as compact Kaggle Datasets; never stage full 1.5 TB
SSL4EO / 110 GiB BigEarthNet on a GPU session; use HF/regional mirrors; keep weekly working set ≤~20 GB.

## 8. HONEST BOTTOM LINE
~25.5 usable GPU-h/week is ENOUGH for the research-grade build IFF we (a) adapt existing checkpoints with
PEFT not pretrain, (b) push non-training work to CPU, (c) rank models frozen before fine-tuning, (d)
anchor rigor on cheap many-seed baselines. It is NOT enough to train several large FMs from scratch — and
the literature (2512.02055, 2604.16663, 2605.28174) says we should not need to.
