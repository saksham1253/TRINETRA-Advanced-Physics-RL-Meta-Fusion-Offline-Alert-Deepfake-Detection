# 05a — MODELS (deep layer): the six PyTorch models + the two learned fusion heads

> Companion to `05_MODELS.md` (index, opening table, closing meta-fusion). **Every model here is
> `py_compile`-clean only and was NOT run on a GPU in this environment** (`_CANON.md §2`). All torch snippets
> are therefore **UNTESTED** (no torch/CUDA in the sandbox). All architecture/shape/loss statements are taken
> **verbatim from the code read for this chapter** (`trinetra/src/trinetra/deep/*.py`); where the code does
> not fix a value it reads **"not specified in code."** No TRINETRA accuracy/latency number exists — every
> such field is **"not measured."**

Shared infrastructure (`deep/layers.py`, read for this chapter), reused below so each model section can refer
to it without repetition:
- **`MLP(sizes, act=SiLU, norm=False, dropout=0.0, out_act=None)`** — linear stack; inserts `LayerNorm` (if
  `norm`) + `SiLU` + optional `Dropout` between hidden layers; no activation after the final linear.
- **`ConvBNAct(c_in,c_out,k=3,s=1,p=1)`** — `Conv2d(bias=False) → BatchNorm2d → SiLU`.
- **`Chomp1d`, `TemporalBlock`, `TCN`** — dilated **causal** 1-D conv stack (weight-norm convs, right-pad
  trimmed by `Chomp1d`, residual + `SiLU`, dilation `2**i` per block). Causal ⇒ no look-ahead (anti-leak
  invariant, gate G6).

Shared training infrastructure (`deep/train.py`, read for this chapter) — applies to models 1–6 and the
heads; details repeated per-model only where they differ:
- `set_seed(seed=0)` seeds `random`, `numpy`, `torch`, `torch.cuda` (all GPUs).
- `TrainConfig`: `epochs=20, batch_size=64 (per-GPU base), lr=3e-4, weight_decay=1e-4, grad_clip=1.0,
  amp=True, seed=0, k_folds=5, num_workers=4, parallel="auto", scale_batch_by_gpus=True,
  scale_lr_by_gpus=True, pin_memory=True`.
- Multi-GPU: `nn.DataParallel` by default on **T4×2** (`_LossModule` wraps model+step so the whole loss runs
  per-replica); effective batch = `batch_size × n_gpus`; **linear-LR scaling** `lr × n_gpus` (Goyal et al.
  2017, named in code); AMP via `torch.cuda.amp` + `GradScaler`; `AdamW` over `requires_grad` params;
  `clip_grad_norm_(grad_clip)`; `setup_perf()` enables cuDNN benchmark + TF32.
- DDP path (`deep/ddp.py`): `mp.spawn` one process/GPU, `DistributedSampler`, NCCL all-reduce, rank-0 save.
- Admission (`admit_model`): spatial-block CV → `ReportGuard` requires a bootstrap **real-win** over
  **climatology AND numpy logistic** on the cost-loss (C_FA=5, C_miss=100) with CI lower bound > 0 (R16); it
  also reports ECE/MCE/Brier **diagnostics** (never relaxes the gate). Temperature scaling via
  `TemperatureScaler` (single `log_T`, LBFGS on validation logits — Guo et al., named in code).

**GPU-hour budget (planning, `_CANON.md §8`):** Kaggle ~30 GPU-h/week, keep ≥15% reserve → ~25.5 usable;
session ~12 h; P100 (16 GB) or 2×T4. Per-model GPU-h splits below are **[EST] / planning** — nothing has been
run, so no measured wall-clock exists.

---

## 1. GeoPINN — physics-informed slope-hydrology network (Class B)

**File:** `deep/geo_pinn.py` · **WS:** ws1b_geophys · **Trained?** no · **Runs here?** no (torch).

### (1) Name / role / inputs → outputs
A physics-informed NN that learns the transient pressure-head field `ψ(Z,t; forcing, soil)` under the
linearized Iverson/Richards diffusion, then maps the physical state to a calibrated landslide probability.
**Role:** *corroborating* evidence that sits beside — never replaces — the deterministic FS/Iverson hard gate,
which still runs at inference (`MODEL_CARDS.md §1`, `geo_pinn.py` docstring).

- **In:** `Z (B,1)`, `t (B,1)`, `rain (B,1)`, `static (B,6)` = `[c', φ, γ, z, β, susceptibility]`.
- **Out (`forward`):** `{logit (B,1), prob=σ(logit), psi (B,1), fs (B,1)}`.

### (2) Selection rationale + alternatives
Why a PINN (code docstring): failure labels are scarce, so the **PDE residual + FS physics supply a dense,
label-free training signal** that keeps the net on the physically admissible manifold and improves
extrapolation to unseen rainfall forcing.

Alternatives considered (from `_CANON.md §6`, `model_set_decision.md`):
- **Full fire/geo PINN as a deployed on-device solver → [INFEASIBLE]** (stiffness, loss-weight imbalance,
  spectral bias, non-identifiability). Decision: physics enters as **soft features/priors with a Class-A
  fallback**, not as a live solver. Our result: **not measured**.
- **Pure data-driven classifier (logistic / GBDT):** the mandatory `eval` baseline is exactly a
  `LogisticNumpy` the model must beat on spatial-CV — kept as the baseline, not the deployed model.
- **Deterministic FS/Iverson only:** retained as the **hard gate**; PINN added only as corroboration. Our
  comparative skill vs any of these: **not measured** (nothing trained).

### (3) Full formulation (as in code)
Field network: `MLP([3 + 6, 128, 128, 128, 1], norm=True)` maps `[Z, t, rain, static] → ψ`.
Risk head: `MLP([2 + 1 + 6, 64, 32, 1], norm=True)` maps `[ψ, tanh(ψ), FS, static] → logit`.

Differentiable FS (`losses.factor_of_safety_torch`, mirrors the numpy `ws1b_geophys.fs`):
```
FS = ( c' + σ'_n · tan φ' ) / ( γ · z · sin β · cos β ),   σ'_n = γ z cos²β − u_w + σ_s
u_w = γ_w · max(ψ, 0),   γ_w = 9.81
```
PDE residual (`losses.richards_iverson_residual`) — linearized Iverson/Richards diffusion:
```
residual = ψ_t − D1 · ψ_ZZ          (target 0)
```
with `ψ_t, ψ_Z, ψ_ZZ` from `torch.autograd.grad` (create_graph). **Slope enters ONLY via `D1`**
(`D1 = D0/cos²β`, bug-guard mirrored from the numpy gate — `_CANON.md §4`, `geo_pinn.py` §).
Physics loss (`physics_loss`):
```
L_phys = physics_weight · mean(residual²)  +  fs_weight · mean( 1[FS<1] · (1 − prob)² )
```
The second term is a **label-free hinge**: when FS<1 the risk prob should be high (physics-anchored
supervision). Total objective (`geo_pinn_step`):
```
loss = physics_weight · L_phys  +  (data_weight · BCE(logit, label))   # BCE only where labels exist
```
Config defaults (`GeoPINNConfig`): `n_static=6, hidden=(128,128,128), dropout=0.0, physics_weight=1.0,
fs_weight=0.5, data_weight=1.0`.

- **Assumptions / regime:** linearized 1-D vertical diffusion of pressure head; slope-parallel seepage;
  `z ≪ slope length` (inherited from the infinite-slope / Iverson parents, `08_equations_register.md`
  E-01/E-02, GH-01/GH-02). `MODEL_CARDS.md §1`: "linearized 1-D diffusion; not a substitute for the hard
  gate; needs site soil params."
- **Boundary/initial conditions:** **not specified in code** (the net learns `ψ` over sampled `(Z,t)`
  collocation points supplied in the batch; no explicit BC/IC term appears in `geo_pinn.py`/`losses.py`).
- **Limiting cases:** as `ψ→0`, `u_w→0` and FS → the dry infinite-slope value; the FS form reduces to the
  saturated effective-stress form at `σ_s=0` (matches `fs.py`). Dimensional check: FS is dimensionless
  (kPa/kPa); `residual` has units of `ψ_t` (m/s) once `D1` carries m²/s — consistent with a diffusion PDE.

### (4) Architecture diagram + tensor shapes (UNTESTED)
```
 Z(B,1) t(B,1) rain(B,1) static(B,6)
        │        concat → (B,9)
        ▼
   field MLP [9→128→128→128→1]  (LayerNorm+SiLU between)         → ψ (B,1)
        │
        ├── u_w = 9.81·max(ψ,0) ─┐
        │                        ▼
        │           factor_of_safety_torch(c',φ,γ,z,β,u_w)        → FS (B,1)
        ▼
   feats = [ψ, tanh(ψ), FS, static]  → (B, 2+1+6 = 9)
        ▼
   risk MLP [9→64→32→1]  → logit (B,1) → σ → prob (B,1)
```

### (5) I/O spec, normalization, units
Inputs are physical: `Z` depth [m], `t` time [s or h — unit not fixed in code; must match `D1` units],
`rain` surface flux/intensity, `static` = `[c' kPa, φ deg, γ kN/m³, z m, β deg, susceptibility (unitless)]`.
`u_w` in kPa (`γ_w = 9.81 kN/m³ · ψ[m]`). **Input normalization: not specified in code** (no scaler in
`geo_pinn.py`/`datamodules.GeoSeriesDataset`; `static` is consumed raw). Output `prob ∈ [0,1]`.

### (6) Training recipe (as in code / planning)
- Dataset: `datamodules.GeoSeriesDataset` (`.npz` with `Z,t,rain,static[6]`, optional `label`, `lat,lon` →
  spatial `block`). Label key emitted only when labels exist (physics-only pretraining supported).
- Step: `geo_pinn_step` rebuilds `Z,t` as **leaf tensors** via `detach().requires_grad_(True)` so
  `autograd.grad` works under both single-GPU and DataParallel (DP scatter makes inputs non-leaf) — code
  comment flags this as the fix that makes the PINN "safe to train on Kaggle T4×2."
- Optimizer/schedule/precision: shared `TrainConfig` (AdamW, lr 3e-4 ×n_gpus, wd 1e-4, grad-clip 1.0, AMP,
  20 epochs, 5-fold spatial-CV). **LR schedule beyond linear GPU scaling: not specified in code.**
- Early stopping / checkpointing: **not specified in code** (`train.py` trains a fixed epoch count; no
  early-stop or checkpoint logic in the files read). Seeds via `set_seed`.
- GPU-h: **[EST] planning only**, part of the ≤30 GPU-h/week budget; **not measured**.

### (7) Hyperparameter table (values from code only)
| HP | Value | Rationale (from code/docstring) | Sensitivity |
|----|-------|---------------------------------|-------------|
| hidden | (128,128,128) | field-net capacity | not measured |
| risk hidden | (64,32) | small head on physical state | not measured |
| physics_weight | 1.0 | weight on PDE residual | not measured |
| fs_weight | 0.5 | weight on FS<1 hinge | not measured |
| data_weight | 1.0 | weight on data BCE | not measured |
| dropout | 0.0 | — | not measured |
| lr / wd / epochs | 3e-4 / 1e-4 / 20 | shared TrainConfig | not measured |

PINN loss-weight sensitivity is a known failure axis (`_CANON.md §6`) but is **not measured** here.

### (8) Code (from repo; UNTESTED)
Model definition (`geo_pinn.py`, abridged):
```python
class GeoPINN(nn.Module):
    def __init__(self, cfg=GeoPINNConfig()):
        self.field = MLP([3 + cfg.n_static, *cfg.hidden, 1], norm=True, dropout=cfg.dropout)
        self.risk  = MLP([2 + 1 + cfg.n_static, 64, 32, 1], norm=True, dropout=cfg.dropout)
    def forward(self, Z, t, rain, static):
        psi = self.field(torch.cat([Z, t, rain, static], dim=1))
        u_w = 9.81 * torch.clamp(psi, min=0.0)
        fs  = factor_of_safety_torch(*(static[:, i:i+1] for i in range(5)), u_w)
        logit = self.risk(torch.cat([psi, torch.tanh(psi), fs, static], dim=1))
        return {"logit": logit, "prob": torch.sigmoid(logit), "psi": psi, "fs": fs}
```
Training-loop objective (`geo_pinn_step`, abridged):
```python
Z = batch["Z"].detach().requires_grad_(True); t = batch["t"].detach().requires_grad_(True)
out  = model(Z, t, batch["rain"], batch["static"])
phys = model.physics_loss(Z, t, batch["rain"], batch["static"], D1)
loss = model.cfg.physics_weight * phys
if batch.get("label") is not None:
    loss = loss + model.cfg.data_weight * bce(out["logit"].squeeze(-1), batch["label"].float())
```
Inference (UNTESTED): `prob = model(Z,t,rain,static)["prob"]` → `deep_expert("geo_pinn", prob)` →
ExpertOutput(Class B, reliability default 0.90, cap 1.00; `adapters._POLICY`).

### (9) Uncertainty & calibration
Confidence = `σ(logit)`. Calibrated post-hoc by `TemperatureScaler` on validation logits (Guo et al.). ECE/
MCE/Brier reported as diagnostics in `admit_model`. What is passed to fusion: a single `prob`, wrapped by
`deep_expert` with Class B and reliability ≤ 1.0; the fusion layer attaches `u` (default 0.3 in `deep_expert`
unless overridden). No aleatoric/epistemic split is produced in code. `[CONFIRMED by code]`.

### (10) Failure modes
- **Validity regime:** linearized 1-D diffusion; invalid for strongly 2-D/3-D flow, macropore/fracture flow,
  or non-linear van Genuchten regimes (parents are Class A/B with regime limits). → down-weighted, never the
  hard gate.
- **OOD:** unseen soil/rainfall far from training support; PINN extrapolation is unreliable (the stated
  reason it is corroboration-only).
- **Adversarial / numerical:** autograd-based residual is sensitive to loss weighting (spectral bias). The
  leaf-tensor fix (`geo_pinn_step`) prevents a known DataParallel crash → linked to chapter 13.
- **Mitigations:** hard FS gate + shield (`FS<1`→ORANGE) run regardless; residual bounded role; Class-B
  fallback to deterministic Iverson.

### (11) Ablations / results
Our numbers: **not measured** (not trained). Paper anchors (source-reported, kept separate): PINN method
(Raissi et al. 2019 — classic, **no arXiv ID in this repo ledger**); Iverson 2000 (WRR) for the transient
physics; spatial-block CV mandated to avoid overstated skill (2608.22293 `[ABS]`, `_CANON.md §6`). No
TRINETRA ablation has been run.

### (12) Literature-backed improvement ideas
- Antecedent-moisture-aware probabilistic rainfall threshold as an extra physics prior (`08_…register` GB-03,
  "CORE EWS"). `[HYPOTHESIS]`
- Probabilistic infinite-slope `P_f = Φ(−β_rel)` to emit a calibrated failure probability instead of a point
  FS (`08_…register` GB-01). `[HYPOTHESIS]`
- Causal/curriculum PINN training to combat spectral bias. `[HYPOTHESIS]`

### (13) Reference IDs (→ chapter 19)
Iverson 2000 WRR; standard infinite-slope geotech; Lu & Likos (suction stress); Raissi et al. 2019 (PINN);
2608.22293 `[ABS]` (spatial CV). Classic refs carry **no arXiv ID in this repo**.

---

## 2. FireSmokeNet — spatiotemporal fire/smoke detector (Class A-aux + data)

**File:** `deep/fire_cnn.py` · **WS:** ws1a_firephys / ws4_cctv · **Trained?** no · **Runs here?** no (torch).

### (1) Role / I/O
Per-frame CNN encoder → temporal GRU → multi-label `{fire, smoke}` logits + an auxiliary flicker-frequency
head. The **temporal pathway is the key false-alarm suppressor** (sun glint/headlights are single-frame; real
fire flickers persistently). The Heskestad/Byram physics gate still runs at inference.
- **In:** clip `x (B, T, C, H, W)`, default `C=3`.
- **Out:** `{logits (B,2), prob=σ(logits), flicker_hz (B,)}`.

### (2) Selection rationale + alternatives
- **Single-frame CNN:** rejected as the sole detector — cannot suppress transient glint/headlight false
  alarms. Kept conceptually as the frame encoder, wrapped by the GRU.
- **3-D CNN / video transformer:** heavier; not chosen (GPU budget C3; `_CANON.md §8`). CNN→GRU is the
  lighter spatiotemporal choice in code. Our comparison: **not measured**.
- **Pure physics (Heskestad/Byram) gate:** retained as the owning physics gate; the net adds learned
  appearance/temporal features. Novel ND flicker term stays Class-C OFF (Rule 20). Our skill: **not measured**.

### (3) Formulation (as in code)
`FrameEncoder` (`ConvBNAct` blocks + MaxPool, final `AdaptiveAvgPool2d(1)`):
```
ConvBNAct(C,32)→Pool→ConvBNAct(32,64)→Pool→ConvBNAct(64,128)→Pool→ConvBNAct(128,128)→AdaptiveAvgPool2d(1)
out_dim = base*4 = 128
```
Temporal + heads:
```
feats = encoder(x.reshape(B·T,C,H,W)).reshape(B,T,128)
seq,hN = GRU(input=128, hidden=128, batch_first=True)
h = hN.squeeze(0)                 # (B,128) last hidden state
logits = Linear(128,2)(h)         # [fire, smoke]
flicker_hz = relu(Linear(128,1)(h)).squeeze(-1)
```
Loss (`loss`): multi-label `BCEWithLogits(logits, targets)` (+ optional `pos_weight`), plus the **Class-C,
default-OFF** Strouhal aux:
```
total = BCE  +  strouhal_weight · strouhal_consistency_loss(flicker_hz, plume_size_m)
strouhal_consistency_loss = MSE( flicker_hz , 1.5 / sqrt(max(D,1e-3)) )    # f ≈ 1.5/√D  (Class A EF-08)
```
`FireNetConfig`: `in_ch=3, base=32, gru_hidden=128, n_classes=2, strouhal_weight=0.0` (OFF by default —
Rule 20). Dimensional check: Strouhal target `[Hz] = 1/√(m)` only with the implicit `1.5 m^½·Hz` coefficient
(SI-inconsistent constant, flagged `[coeff-verify]` in `established_ef.py`).

### (4) Architecture diagram + shapes (UNTESTED)
```
x (B,T,C,H,W)
   └ reshape (B·T,C,H,W) → FrameEncoder → (B·T,128) → reshape (B,T,128)
        └ GRU → hN (1,B,128) → h (B,128)
             ├ Linear(128,2) → logits (B,2) → σ → prob (B,2)=[p_fire,p_smoke]
             └ Linear(128,1) → relu → flicker_hz (B,)
```

### (5) I/O spec, normalization, units
Images expected as float tensors; **normalization/augmentation: not specified in code** (dataset
`ImageFolderNPZ` casts to float32, no transform pipeline in the files read). `flicker_hz` in Hz; `plume_size_m`
in metres. Outputs are per-class probabilities in [0,1].

### (6) Training recipe
Shared `TrainConfig` (AdamW, AMP, DataParallel, 5-fold spatial-CV, temperature calibration). Dataset
`ImageFolderNPZ` (`images`,`labels`,`block`). `pos_weight` supported for class imbalance. Augmentation/
early-stopping/checkpointing: **not specified in code**. GPU-h: **[EST] planning**; **not measured**.

### (7) Hyperparameters (code only)
| HP | Value | Rationale | Sensitivity |
|----|-------|-----------|-------------|
| base channels | 32 | encoder width | not measured |
| gru_hidden | 128 | temporal state | not measured |
| n_classes | 2 (multi-label) | fire+smoke | not measured |
| strouhal_weight | 0.0 (OFF) | Class-C gated (Rule 20) | not measured |

### (8) Code (repo; UNTESTED)
```python
def forward(self, x):           # x: (B,T,C,H,W)
    B,T,C,H,W = x.shape
    feats = self.encoder(x.reshape(B*T,C,H,W)).reshape(B,T,-1)
    seq,hN = self.gru(feats); h = hN.squeeze(0)
    logits = self.head(h); flick = torch.relu(self.flicker(h)).squeeze(-1)
    return {"logits": logits, "prob": torch.sigmoid(logits), "flicker_hz": flick}
```
Inference → `deep_expert("fire_cnn", p_fire)` → ExpertOutput(Class DATA, r default 0.80, cap 0.95).

### (9) Uncertainty & calibration
Per-class `σ(logit)`; temperature-scaled; ECE/MCE/Brier diagnostics. GRU temporal persistence is the implicit
confidence mechanism for flicker. Passed to fusion: `p_fire` as a DATA expert (cap 0.95). `[CONFIRMED by code]`.

### (10) Failure modes
Night/IR domain shift, smoke-only vs flame-only ambiguity, aliased flicker on low-fps CCTV (the exact failure
B-05 targets, `model_set_decision.md`). Mitigations: temporal GRU, physics gate, Class-C flicker term OFF
until validated → chapter 13.

### (11) Ablations / results
Our numbers: **not measured**. Paper anchors: Strouhal/puffing `f≈1.5/√D` (Cetegen & Ahmed 1993, classic);
EF-08 inventory `[coeff-verify]`. No TRINETRA ablation run.

### (12) Improvement ideas
Aliasing-aware flicker feature (B-05) as a learned-vs-physics consistency input `[HYPOTHESIS]`; IR/thermal
second stream `[HYPOTHESIS]`; swap GRU for a small temporal transformer if budget allows `[HYPOTHESIS]`.

### (13) Reference IDs
Cetegen & Ahmed 1993 (puffing); Heskestad 1983; Byram (convection number) — classic, no repo arXiv.

---

## 3. EODownstream — frozen EO foundation encoder + head (Class data)

**File:** `deep/eo_encoder.py` · **WS:** ws1b (EO) · **Trained?** head only (planned) · **Runs here?** no.

### (1) Role / I/O
A pretrained geospatial foundation model is used **FROZEN** as a feature extractor; a small trainable MLP head
maps patch embeddings to a hazard-susceptibility/change logit.
- **In:** multispectral patch `x (B, C, H, W)`, default `in_chans=6` (e.g. S2 subset).
- **Out:** `{logit (B,1), prob=σ(logit)}`.

### (2) Rationale + alternatives
- **Full fine-tune of the encoder:** rejected — blows the GPU budget (C3) and overfits scarce labels; code
  freezes the encoder deliberately.
- **Train a CNN from scratch:** rejected for the same reasons (label scarcity).
- **FM weights vs timm substitute:** code injects a real FM via `encoder_factory`, else falls back to a
  **timm backbone** (`resnet50` default) as a "transparent, clearly-labelled substitute" — the chosen encoder
  **must be recorded in the eval report** (Rule 16, docstring + `MODEL_CARDS.md §3`). Our result: **not measured**.

### (3) Formulation (as in code)
```
encoder = encoder_factory() OR timm.create_model(backbone, pretrained, in_chans, num_classes=0, global_pool="avg")
if freeze: encoder.parameters().requires_grad_(False); encoder.eval() even in train()  # fixed BN stats
head = MLP([feat_dim, 256, 64, 1], norm=True, dropout=0.1)
forward: feats = encoder(x) under set_grad_enabled(not freeze); logit = head(feats); prob = σ(logit)
loss = BCEWithLogits(logit.squeeze(-1), targets, pos_weight)
```
`EOConfig`: `backbone="resnet50", in_chans=6, pretrained=True, freeze=True, head_hidden=(256,64), n_out=1`.
Note (code): overriding `train()` keeps the frozen encoder in `eval()` so BatchNorm running stats stay fixed.

### (4) Architecture diagram + shapes (UNTESTED)
```
x (B,6,H,W) → [FROZEN encoder] → feats (B, feat_dim)   # feat_dim = encoder.num_features
            → head MLP [feat_dim→256→64→1] → logit (B,1) → σ → prob (B,1)
```
`feat_dim` is backbone-dependent (**not fixed in code**; `resnet50` → 2048 by timm convention, not asserted
in-repo).

### (5) I/O spec, normalization, units
Multispectral reflectance patches; **channel count set per dataset** (`in_chans`). Normalization: **not
specified in code** (depends on the FM's expected preprocessing — a documented gap). Output `prob∈[0,1]`.

### (6) Training recipe
Only the head trains (encoder frozen). Shared `TrainConfig`; `pos_weight` for imbalance; dropout 0.1 in head;
spatial-CV; temperature calibration. Augmentation/early-stop/checkpoint: **not specified in code**. GPU-h:
small (head-only) **[EST]**; **not measured**.

### (7) Hyperparameters
| HP | Value | Rationale | Sensitivity |
|----|-------|-----------|-------------|
| backbone | resnet50 (timm) | transparent substitute | not measured |
| in_chans | 6 | S2 subset default | not measured |
| freeze | True | budget + anti-overfit | not measured |
| head_hidden | (256,64) | small head | not measured |
| head dropout | 0.1 | regularize small head | not measured |

### (8) Code (repo; UNTESTED)
```python
self.encoder = timm.create_model(cfg.backbone, pretrained=cfg.pretrained, in_chans=cfg.in_chans,
                                 num_classes=0, global_pool="avg"); feat_dim = self.encoder.num_features
if cfg.freeze: [p.requires_grad_(False) for p in self.encoder.parameters()]
self.head = MLP([feat_dim, *cfg.head_hidden, cfg.n_out], norm=True, dropout=0.1)
```
Inference → `deep_expert("eo", prob)` → ExpertOutput(Class DATA, r 0.70, cap 0.90).

### (9) Uncertainty & calibration
`σ(logit)`; temperature-scaled; ECE/MCE/Brier diagnostics; fusion sees `prob` as DATA (cap 0.90).

### (10) Failure modes
Encoder-preprocessing mismatch, band/sensor shift, label scarcity. Mitigation: freezing + record encoder +
spatial-CV. The timm substitute must be flagged in the report so skill isn't attributed to a real FM.

### (11) Ablations / results
Our numbers: **not measured**. Paper anchors: EO foundation models (Prithvi / SatMAE / Clay, named in code
docstring; **no repo arXiv IDs**). No TRINETRA result.

### (12) Improvement ideas
LoRA/partial unfreeze if budget allows `[HYPOTHESIS]`; multi-temporal change head `[HYPOTHESIS]`; spatial-block
CV already mandated (2608.22293 `[ABS]`).

### (13) Reference IDs
Prithvi / SatMAE / Clay (EO FMs); 2608.22293 `[ABS]` (spatial CV). → chapter 19.

---

## 4. DeepAnomaly — TCN autoencoder + Deep-SVDD + forecast (Class data)

**File:** `deep/anomaly_deep.py` · **WS:** ws8_anomaly · **Trained?** no · **Runs here?** no (torch).

### (1) Role / I/O
Causal-TCN encoder feeding three fused heads: reconstruction, one-step forecast, and Deep-SVDD distance.
**Unsupervised**, trained on **NORMAL** telemetry only so events become out-of-distribution. The numpy ws8
ensemble is the always-on fallback.
- **In:** telemetry window `x (B, n_feat, T)`, default `n_feat=8`.
- **Out (`forward`):** `{recon (B,n_feat,T), pred_next (B,n_feat,T), emb (B,emb,T)}`; `anomaly_score(x)` →
  scalar per sample.

### (2) Rationale + alternatives
- **Supervised classifier:** rejected — labelled anomalies are scarce; unsupervised normal-only is the design.
- **Single head (recon-only AE, or SVDD-only):** code fuses three signals so a failure of one head is
  caught by another. Our comparison: **not measured**.
- **Numpy isolation-forest/residual ensemble:** kept as the **fallback** (`ws8_anomaly`); DeepAnomaly is the
  "admitted-only upgrade" (`MODEL_CARDS.md §4`). Causal convs ⇒ no look-ahead (G6).

### (3) Formulation (as in code)
```
encoder = TCN(n_feat, [32,32,64])                      # dilated causal blocks, dilation 2**i
to_emb  = Conv1d(64, emb_dim=32, 1)                    # (B,32,T)
decoder = TCN(32, [64,32,32, n_feat])                  # channels reversed + n_feat
forecast= Conv1d(64, n_feat, 1)                        # one-step forecast from encoder features
center  = buffer(emb_dim)                              # Deep-SVDD hypersphere center
```
Losses (`loss`):
```
recon    = MSE(recon, x)
forecast = MSE(pred_next[:,:,:-1], x[:,:,1:])          # predict x_{t+1} from features up to t
svdd     = deep_svdd_loss(emb.mean(dim=2), center) = mean Σ_j (z−c)²
total    = recon_weight·recon + forecast_weight·forecast + svdd_weight·svdd
```
`init_center` sets `c` = mean embedding over normal data (floored to ±eps to avoid a trivial zero center),
called once before SVDD training. `anomaly_score(x) = recon_err + forecast_err + SVDD_distance` (per sample,
R⁺, higher = more anomalous). `AnomalyConfig`: `n_feat=8, channels=(32,32,64), emb_dim=32, recon_weight=1.0,
forecast_weight=1.0, svdd_weight=0.5`. Causality (anti-leak): `Chomp1d` trims right padding each block.

### (4) Architecture diagram + shapes (UNTESTED)
```
x (B,8,T) → TCN[8→32→32→64] (causal) → enc (B,64,T)
   ├ to_emb Conv1d(64→32) → emb (B,32,T) → decoder TCN[32→64→32→32→8] → recon (B,8,T)
   ├ forecast Conv1d(64→8) → pred_next (B,8,T)   (compared to x shifted by 1)
   └ emb.mean(dim=2) → (B,32) → SVDD distance to center c (32,)
score = recon_err + forecast_err + ||emb̄ − c||²
```

### (5) I/O spec, normalization, units
`x` = multivariate sensor window `(B, n_feat, T)`; units are sensor-native (telemetry). **Normalization: not
specified in code** (`WindowNPZDataset` casts float32, no scaler). Score is unnormalized R⁺; the adapter/gate
must map it to [0,1] (`MODEL_CARDS §4`: "→ normalized prob for the gate"; mapping fn **not in the files read**).

### (6) Training recipe
Normal-only data; `init_center` before SVDD; shared `TrainConfig` (AdamW, AMP, DataParallel). **Threshold must
be calibrated per site** (`MODEL_CARDS §4`). Early-stop/checkpoint/augmentation: **not specified in code**.
GPU-h: **[EST]**; **not measured**.

### (7) Hyperparameters
| HP | Value | Rationale | Sensitivity |
|----|-------|-----------|-------------|
| channels | (32,32,64) | TCN depth/width | not measured |
| emb_dim | 32 | SVDD embedding | not measured |
| recon/forecast/svdd weight | 1.0 / 1.0 / 0.5 | balance 3 heads | not measured |
| svdd eps | 0.1 | avoid trivial center | not measured |

### (8) Code (repo; UNTESTED)
```python
def loss(self, x):
    out = self.forward(x)
    recon = F.mse_loss(out["recon"], x)
    fc    = F.mse_loss(out["pred_next"][:,:,:-1], x[:,:,1:])
    svdd  = deep_svdd_loss(out["emb"].mean(dim=2), self.center)
    return {"loss": recon_w*recon + fc_w*fc + svdd_w*svdd, ...}
```
Inference → `anomaly_score` → normalized prob → `deep_expert("anomaly", prob)` (Class DATA, r 0.70, cap 0.90).

### (9) Uncertainty & calibration
No probabilistic head; the raw score is a distance/error sum. Calibration = per-site threshold + (where used)
the fusion adapter's `u`. ECE/Brier are not meaningful on the raw score until it is mapped to a probability
(**mapping not in files read**). `[CONFIRMED by code]` for the score; mapping **not specified in code**.

### (10) Failure modes
Non-stationary "normal" (drift) → false anomalies; threshold mis-set per site; multivariate correlations the
TCN can't capture. Mitigations: numpy ensemble fallback always on; drift monitor voids CP guarantees
(`ws6_robust/drift_monitor.py`); causal convs for no leakage → chapter 13.

### (11) Ablations / results
Our numbers: **not measured**. Paper anchor: Deep-SVDD (Ruff et al. 2018 — classic, no repo arXiv); TCN causal
conv design. No TRINETRA result.

### (12) Improvement ideas
Probabilistic/quantile forecast head for calibrated anomaly probability `[HYPOTHESIS]`; per-feature
attribution for operator triage `[HYPOTHESIS]`; online center update under slow drift `[HYPOTHESIS]`.

### (13) Reference IDs
Ruff et al. 2018 (Deep-SVDD); TCN (Bai et al. 2018) — classic, no repo arXiv. → chapter 19.

---

## 5. AuthenticityNet — two-stream deepfake detector (Class data, LOW trust)

**File:** `deep/deepfake_net.py` · **WS:** ws2_deepfake · **Trained?** no · **Runs here?** no (torch).

### (1) Role / I/O
Spatial (RGB) + frequency (2-D FFT log-magnitude) two-stream CNN → authenticity logit. The **least-trusted
expert**: enters fusion with small reliability and **can NEVER gate a life-safety alert** (Rule 19). It only
corroborates/suppresses confidence on media-sourced reports.
- **In:** image `x (B, C, H, W)` in [0,1], default `C=3`.
- **Out:** `{logit (B,), p_fake=σ(logit) (B,)}`.

### (2) Rationale + alternatives
- **RGB-only CNN:** rejected as sole stream — misses GAN/upsampling spectral fingerprints; FFT stream added.
- **Frequency-only:** rejected — loses spatial semantics; both streams fused.
- **Trusting the detector to trigger:** **[INFEASIBLE]** for life-safety (`_CANON.md §6`: deepfake/zero-shot/
  social signals = low-trust advisory, must be corroborated) → hard reliability cap 0.4. Our result: **not
  measured**.

### (3) Formulation (as in code)
```
_fft_logmag(x) = log1p(| fftshift( fft2(x, norm="ortho") ) |)      # per-channel frequency fingerprint
spatial = _Stream(C,32); freq = _Stream(C,32)                      # each: ConvBNAct×3 + AdaptiveAvgPool2d(1), out_dim=128
head = Linear(128+128,128) → SiLU → Dropout(0.3) → Linear(128,1)
forward: logit = head(cat[spatial(x), freq(_fft_logmag(x))]); p_fake = σ(logit)
loss = BCEWithLogits(logit, is_fake_targets)
```
`DeepfakeConfig`: `in_ch=3, base=32, max_reliability=0.4` (the trust cap surfaced to fusion, Rule 19).

### (4) Architecture diagram + shapes (UNTESTED)
```
x (B,3,H,W) ─┬─ spatial _Stream → (B,128)
             └─ FFT log-mag → freq _Stream → (B,128)
          concat (B,256) → Linear(256,128)→SiLU→Drop(0.3)→Linear(128,1) → logit (B,1)→σ→p_fake (B,)
```

### (5) I/O spec, normalization, units
Image in [0,1] (code comment); **no explicit normalization transform in code** beyond the [0,1] assumption.
FFT uses orthonormal norm. Output `p_fake∈[0,1]` = P(media manipulated).

### (6) Training recipe
Shared `TrainConfig`; BCE over RGB+FFT streams. Augmentation/early-stop/checkpoint: **not specified in code**.
GPU-h: **[EST]**; **not measured**.

### (7) Hyperparameters
| HP | Value | Rationale | Sensitivity |
|----|-------|-----------|-------------|
| base | 32 | per-stream width | not measured |
| head dropout | 0.3 | regularize fusion head | not measured |
| max_reliability | 0.4 | hard trust cap (Rule 19) | enforced in adapter |

### (8) Code (repo; UNTESTED)
```python
def forward(self, x):           # x in [0,1]
    s  = self.spatial(x)
    fr = self.freq(_fft_logmag(x))
    logit = self.head(torch.cat([s, fr], dim=1))
    return {"logit": logit.squeeze(-1), "p_fake": torch.sigmoid(logit).squeeze(-1)}
```
Inference → `deep_expert("deepfake", p_fake)` → ExpertOutput(Class DATA, r default 0.30, **cap 0.40**).

### (9) Uncertainty & calibration
`σ(logit)`; temperature-scalable; but the **reliability cap 0.4** is the governing trust control, not
calibration. Fusion sees `p_fake` with r ≤ 0.4, so NF effective weight `r·c·exp(−u/τ)` is structurally small.
`[CONFIRMED by code]`.

### (10) Failure modes
Novel generators (OOD), compression artifacts mimicking FFT fingerprints, adversarial post-processing. By
design the cap bounds the damage: it can suppress but not trigger. → chapter 13.

### (11) Ablations / results
Our numbers: **not measured**. Paper anchor: FFT/frequency-domain GAN fingerprint detection (two-stream
family; **no specific arXiv ID recorded in this repo** — described generically in `_CANON.md §6`). No TRINETRA
result.

### (12) Improvement ideas
Add temporal/physiological cues for video `[HYPOTHESIS]`; provenance/C2PA signal fusion `[HYPOTHESIS]`;
calibrated abstention when OOD `[HYPOTHESIS]`.

### (13) Reference IDs
Two-stream RGB+frequency deepfake detection (generic); `_CANON.md §6` low-trust verdict. → chapter 19.

---

## 6. CQLPolicy — conservative offline-RL alarm policy (Class advisory)

**File:** `deep/offline_rl.py` · **WS:** ws5_fusion_rl · **Trained?** no · **Runs here?** no (torch). (The
numpy baseline + OPE gate in `ws5_fusion_rl/rl.py` DO run — covered in `05b_MODELS.md §27`.)

### (1) Role / I/O
Discrete-action Conservative Q-Learning. Actions `{HOLD, WATCH, ALARM}`. Trained purely offline from logged
`(s, a, r, s', done)` — no live exploration (unsafe in a disaster system). **Advisory**, always composed with
the monotone shield floor at deployment (can only be overridden UPWARD), deployed only after the OPE gate.
- **In:** state `s (B, state_dim)`, default `state_dim=16`.
- **Out:** `q_values(s) (B,3)`; `act(s, shield_floor_idx)` → shielded action `(B,)`; `action_probs(s,temp)` →
  softmax target policy for OPE.

### (2) Rationale + alternatives
- **Online RL:** **[INFEASIBLE]** here — live exploration in a life-safety system is unsafe (docstring).
- **Behavior cloning only:** would copy the logging policy's mistakes; CQL's conservative penalty keeps the
  policy near support **and** can improve on it, gated by OPE.
- **Rule baseline (threshold policy):** kept as the honest fallback and the OPE comparator — learned policy is
  deployed only if it beats it (`rl.ope_admission`). `gamma=0` ⇒ one-step contextual bandit (recommended when
  transitions are weakly Markov). Our value: **not measured**.

### (3) Formulation (as in code)
```
QNet = MLP([state_dim, 256, 256, n_actions], norm=True)      # online + target (Polyak)
cql_loss(s,a,r,s',done):
   q_sa  = Q_online(s)[a]
   target= r + gamma·(1−done)·max_a Q_target(s')
   bellman = MSE(q_sa, target)
   conservative = mean( logsumexp_a Q(s,a) − q_sa )           # push down OOD-action Q
   loss = bellman + cql_alpha · conservative
polyak_update: target = (1−tau)·target + tau·online
act(s, floor): a = max( argmax_a Q_online(s), floor )          # monotone safety-upward (Rule 19)
action_probs(s,temp) = softmax(Q_online(s)/temp)               # stochastic target policy for OPE
```
`CQLConfig`: `state_dim=16, n_actions=3, hidden=(256,256), gamma=0.0 (one-step bandit), cql_alpha=1.0,
tau=0.005`.

### (4) Architecture diagram + shapes (UNTESTED)
```
s (B,16) → QNet MLP[16→256→256→3] → Q (B,3)   (online)
                                   ↘ target QNet (Polyak τ=0.005, grads off)
act: argmax over 3 → max with shield_floor_idx → shielded action (B,)
```

### (5) I/O spec, normalization, units
State `s` = fused-risk/context features (`state_dim=16`; exact feature list **not specified in code** — the
dataset supplies `s`). Actions are indices 0/1/2 ↔ HOLD/WATCH/ALARM. Rewards are cost-shaped (logged).
Normalization: **not specified in code**.

### (6) Training recipe
`RLTransitionDataset` (`s,a,r,s_next,done,behavior_prob`). CQL loss + Polyak target updates. Deploy gate:
`ope_admission` (positivity + ESS + value ≥ baseline) — else keep `RuleBaselinePolicy` (R19). The learned
`OfflineRLPolicy.fit` in numpy **raises `MissingDependency`** (needs d3rlpy+torch); the torch CQL here is the
trainable version. Early-stop/checkpoint: **not specified in code**. GPU-h: small **[EST]**; **not measured**.

### (7) Hyperparameters
| HP | Value | Rationale | Sensitivity |
|----|-------|-----------|-------------|
| hidden | (256,256) | Q-net capacity | not measured |
| gamma | 0.0 | one-step bandit default | not measured |
| cql_alpha | 1.0 | conservative penalty weight | not measured |
| tau | 0.005 | target Polyak rate | not measured |
| RuleBaseline threshold | 0.0476 (= p*) | OPE comparator | not measured |

### (8) Code (repo; UNTESTED)
```python
def cql_loss(self, s, a, r, s_next, done):
    q = self.online(s); q_sa = q.gather(1, a.long().unsqueeze(1)).squeeze(1)
    with torch.no_grad():
        target = r + self.cfg.gamma*(1-done.float())*self.target(s_next).max(1).values
    bellman = F.mse_loss(q_sa, target)
    conservative = (torch.logsumexp(q, 1) - q_sa).mean()
    return {"loss": bellman + self.cfg.cql_alpha*conservative, ...}
```
Deployment composition: `act()` greedy ∨ shield floor; OPE admission in `rl.ope_admission` (05b §27).

### (9) Uncertainty & calibration
No probabilistic calibration; conservatism (CQL penalty) is the uncertainty control, keeping Q low on OOD
actions. The shield + OPE gate are the deployment-time safety/uncertainty mechanisms. `[CONFIRMED by code]`.

### (10) Failure modes
Distribution shift from the logging policy (positivity violation), reward mis-specification, weak-Markov
transitions. Mitigations: `gamma=0` bandit option, CQL penalty, OPE positivity/ESS gate, shield floor
(monotone upward), rule-baseline fallback → chapter 13.

### (11) Ablations / results
Our value estimate: **not measured** (no logs trained). Paper anchor: CQL (Kumar et al. 2020, **arXiv
2006.04779** — QG2-verified; note-only, not a ledger row); WIS/OPE (classic). No TRINETRA result.

### (12) Improvement ideas
IQL/one-step as alternatives (the `rl.py` interface names them) `[HYPOTHESIS]`; distributional Q for risk-aware
action `[HYPOTHESIS]`; pessimistic OPE lower bound as the deploy criterion `[HYPOTHESIS]`.

### (13) Reference IDs
CQL (Kumar et al. 2020, **arXiv 2006.04779**); IQL (**arXiv 2110.06169**); WIS/OPE; shielded RL (`_CANON.md §6` A6). → chapter 19.

---

## 7. GMFHead — learned bounded residual on the gated-mixture base (Class B)

**File:** `deep/fusion_head.py` · **WS:** ws5_fusion_rl · **Trained?** no · **Runs here?** no (torch). The
numpy GMF that *consumes* the exported head DOES run (05b §23).

### (1) Role / I/O
The meta-fusion base (gated precision-weighted mean, or PHARAOH when enabled) is always present; this small
head learns only a **bounded residual correction** from transparent features `[base, dispersion, salience]`.
- **In:** `feats (B,3)` = `[base, dispersion, salience]`.
- **Out:** raw residual (B,), tanh-bounded to [−1,1]; final cap applied in numpy.

### (2) Rationale + alternatives
- **Replace the physics base with a learned fusion:** rejected — a mis-trained head could dominate physics.
  So the head is **residual-only**, hard-clipped to ±cap (default 0.1), and defaults to 0 (GMF ≡ FM-1) with no
  head loaded.
- **Larger feature set:** code deliberately uses only 3 transparent features for auditability. Our result:
  **not measured**.

### (3) Formulation (as in code)
```
net = Linear(3,16) → Tanh → Linear(16,1) → Tanh        # output in [-1,1]
forward(feats) = net(feats).squeeze(-1)
train_step: pred = forward(feats)·cap; loss = MSE(pred, clamp(residual_target, -cap, cap))   # target = y - base
export_numpy: serialize (W1,b1,W2,b2,cap) to a pure-numpy closure f(feats_dict)->raw·cap
```
Downstream (`ws5_fusion_rl.gmf.bounded_residual`) re-clips to ±cap (defense in depth), and
`gmf_fuse` returns `p = clip(base + residual, 0, 1)`.

### (4) Architecture diagram + shapes (UNTESTED)
```
[base,dispersion,salience] (B,3) → Linear(3,16)→Tanh→Linear(16,1)→Tanh → raw (B,) → ×cap → clip(±cap) → residual
p = clip(base + residual, 0, 1)
```

### (5) I/O spec, normalization, units
Features are already in natural ranges (`base`∈[0,1], `dispersion`∈[0,~0.5], `salience`∈[0,1] from NF-4). No
extra normalization. Output residual ∈ [−cap, cap].

### (6) Training recipe
Supervise residual toward `(y − base)` clipped to ±cap; MSE. Shared `TrainConfig` (small net). Exported to
`gmf_head_numpy.json` by `kaggle/train_fusion_head.py` for torch-free offline inference. GPU-h: negligible
**[EST]**; **not measured**.

### (7) Hyperparameters
| HP | Value | Rationale | Sensitivity |
|----|-------|-----------|-------------|
| hidden | 16 | tiny residual net | not measured |
| cap | 0.1 (default) | bound residual (safety) | governs max influence |

### (8) Code (repo; UNTESTED)
```python
class GMFHead(nn.Module):
    def __init__(self, hidden=16):
        self.net = nn.Sequential(nn.Linear(3,hidden), nn.Tanh(), nn.Linear(hidden,1), nn.Tanh())
    def forward(self, feats): return self.net(feats).squeeze(-1)
def export_numpy(head, cap=0.1):
    # closure: raw = tanh(W2 @ tanh(W1@x+b1) + b2); return raw*cap   (numpy, torch-free)
```
Numpy consumer: `gmf.load_numpy_head('gmf_head_numpy.json')` → closure → `gmf_fuse(..., head=closure)`
(**runs**, 05b §23).

### (9) Uncertainty & calibration
No calibration of its own; it corrects the already-fused base. Safety property: residual bounded ⇒ a
mis-trained head cannot move the output more than ±cap. `[CONFIRMED by code]`.

### (10) Failure modes
Over-fit residual (bounded by cap), feature drift. Mitigation: hard ±cap re-clip in numpy; residual 0 when no
head. → chapter 13.

### (11) Ablations / results
Our numbers: **not measured**. No paper number applies to this bespoke head.

### (12) Improvement ideas
Monotonicity constraint on the residual w.r.t. base `[HYPOTHESIS]`; per-hazard caps `[HYPOTHESIS]`.

### (13) Reference IDs
Residual-correction / gated-mixture fusion (design-internal, `DESIGN/ws5_fusion/`). → chapter 19.

---

## 8. AttentionFusionHead — learned attention over workstream experts (Class B)

**File:** `deep/fusion_head.py` · **WS:** ws5_fusion_rl · **Trained?** no · **Runs here?** no (torch). Numpy
export closure runs offline.

### (1) Role / I/O
Learned **attention** meta-fusion over a variable set of workstream/group experts: learns how much to listen
to each expert given its `[p, u, c, r]`, instead of a fixed precision weight.
- **In:** `x (B, N, 4)` expert features `[p,u,c,r]`; optional `mask (B,N)` (True=available).
- **Out:** `{p (B,), base (B,), residual (B,), attn (B,N)}`.

### (2) Rationale + alternatives
- **Fixed precision weights (FM-1):** kept as the default/fallback; attention adds learned re-weighting.
- **Unconstrained learned fusion:** rejected — could invent a probability outside the experts' range; so the
  **base is a convex softmax-attention combination** (bounded to `[min_i p_i, max_i p_i]`) plus a ±cap
  residual, then clipped to [0,1]. Unavailable experts are masked out of the softmax. Our result: **not
  measured**.

### (3) Formulation (as in code)
```
score    = Linear(4,16) → Tanh → Linear(16,1)            # per-expert logit
logits   = score(x).squeeze(-1); if mask: masked_fill(~mask, -inf)
attn     = softmax(logits, dim=1)                        # convex weights over experts
base     = Σ_i attn_i · p_i                              # p = feature 0; base ∈ [min p_i, max p_i]
context  = Σ_i attn_i · x_i                              # attention-pooled (B,4)
residual = (Linear(4,16)→Tanh→Linear(16,1)→Tanh)(context) · cap
p        = clip(base + residual, 0, 1)
loss     = cost-sensitive BCE: w_pos=C_miss/(C_FA+C_miss), w_neg=C_FA/(C_FA+C_miss),  C_FA=5, C_miss=100
```
`cap=0.1` default. Cost weights encode miss ≫ false-alarm (the project cost model, p*=0.0476).

### (4) Architecture diagram + shapes (UNTESTED)
```
x (B,N,4) ─ score MLP → logits (B,N) ─mask→ softmax → attn (B,N)
   ├ base = Σ attn·p   (convex, ∈[min p, max p])
   └ context = Σ attn·x (B,4) → residual MLP (…→Tanh) ·cap → residual (B,)
p = clip(base + residual, 0,1)
```

### (5) I/O spec, normalization, units
Features already in [0,1] (`p,u,c,r` from `ExpertOutput`). No extra normalization. Output `p∈[0,1]`.

### (6) Training recipe
Cost-sensitive BCE on fused probability; shared `TrainConfig`. Exported by `export_attention_numpy` to a
torch-free closure `closure(experts:list[dict])->p` (masks unavailable; softmax; convex base; ±cap residual).
GPU-h: negligible **[EST]**; **not measured**.

### (7) Hyperparameters
| HP | Value | Rationale | Sensitivity |
|----|-------|-----------|-------------|
| feat_dim | 4 ([p,u,c,r]) | per-expert features | not measured |
| hidden | 16 | small score/residual nets | not measured |
| cap | 0.1 | bounded residual (safety) | governs max deviation |
| C_FA / C_miss | 5 / 100 | cost model (p*=0.0476) | sets loss asymmetry |

### (8) Code (repo; UNTESTED)
```python
def forward(self, x, mask=None):
    logits = self.score(x).squeeze(-1)
    if mask is not None: logits = logits.masked_fill(~mask, float("-inf"))
    attn = torch.softmax(logits, dim=1)
    base = (attn * x[...,0]).sum(1)                       # convex over experts' p
    context = (attn.unsqueeze(-1) * x).sum(1)
    residual = self.residual(context).squeeze(-1) * self.cap
    return {"p": torch.clamp(base + residual, 0, 1), "base": base, "residual": residual, "attn": attn}
```
Offline: `export_attention_numpy(head)` → `closure(experts)` (numpy; **runs** without torch).

### (9) Uncertainty & calibration
Convex base + bounded residual keep the fused probability inside/near the experts' own range (a structural
calibration guard). Masking removes unavailable experts. No separate calibration head. `[CONFIRMED by code]`.

### (10) Failure modes
Attention collapse onto one expert (mitigated: base stays convex and residual is bounded); mis-trained
residual (bounded by cap). → chapter 13.

### (11) Ablations / results
Our numbers: **not measured**. No external paper number applies directly.

### (12) Improvement ideas
Multi-head attention over experts `[HYPOTHESIS]`; entropy regularization on `attn` to avoid collapse
`[HYPOTHESIS]`; per-hazard temperature `[HYPOTHESIS]`.

### (13) Reference IDs
Attention fusion / MoE-style gating (`_CANON §3` A12 multimodal fusion). → chapter 19.
