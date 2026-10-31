# 05 — MODELS: every model, its formulation, I/O, training recipe, calibration

> **Read `_CANON.md` first.** This chapter agrees with it exactly. Two numbers you must carry into every
> paragraph below:
> 1. **No TRINETRA model has been trained and no dataset has been downloaded.** Every accuracy / skill /
>    latency / cost figure attributed to TRINETRA is **"not measured."** Numbers attributed to a *paper* are
>    that paper's result on that paper's data, kept visibly separate (`_CANON.md §1`).
> 2. The PyTorch `deep/` models are **`py_compile`-clean only** — they were **NOT run on a GPU** in this
>    environment (no torch/CUDA in the authoring sandbox, `_CANON.md §2`). The numpy core (physics + fusion +
>    decision + conformal) **runs**: `python run_tests.py` → **128 tests OK**, `python scripts/ci_gates.py`
>    → **ALL 6 CI GATES PASSED** `[CONFIRMED]`. Any torch code snippet in this chapter is therefore
>    **UNTESTED** (cannot execute torch here).

Honesty labels used throughout: `[CONFIRMED]` / `[LIKELY]` / `[HYPOTHESIS]` / `[INFEASIBLE]` (`_CANON.md §1`).
"Paper X reports …" (source-reported) is always separated from "Our code implements …" (verifiable from the
files read for this chapter). Where a field cannot be filled from code or a cited source, it reads
**"not specified in code"** or **"not measured"** — never invented.

This chapter is split for length:
- **`05a_MODELS.md`** — the six trainable PyTorch models (Geo-PINN, FireSmokeNet, EODownstream,
  DeepAnomaly, AuthenticityNet, CQLPolicy) and the two learned fusion heads (GMFHead, AttentionFusionHead).
- **`05b_MODELS.md`** — the numpy physics models (infinite-slope FS, Iverson transient head, Fukuzono 1/v,
  Caine I–D, Heskestad / Byram / Strouhal / gray-body fire physics) and the numpy fusion / decision / shield
  / conformal pieces (NF-1..4, FM-1, PHARAOH, GMF, BLUE/GLS, hierarchical, adapters, RL/OPE, conformal
  calibration, the single decision function, the shield).
- **This file (`05_MODELS.md`)** — the opening all-models comparison table, then the closing end-to-end
  meta-fusion explanation, the all-models comparison table (annotated), and the "which model when" guide.

---

## 0. Opening comparison table — ALL models

Class legend (`MODEL_CARDS.md`): **A** deterministic/established physics · **B** physics-informed or
physics-regularized learning · **C** novel term (flag-gated OFF, A/B fallback — Rule 20) · **data**
data-driven · **advisory** RL policy. "Trained?" is **no** for every row (nothing trained — `_CANON.md §0`).
"Runs?" distinguishes the numpy core (executes, tested) from the torch layer (compile-verified only).

| # | Model | Role in pipeline | Class | Inputs → outputs | Trained? | Runs here? | Code file |
|---|-------|------------------|-------|------------------|----------|-----------|-----------|
| 1 | **GeoPINN** | Corroborating landslide evidence beside the deterministic FS/Iverson gate | B | `(Z, t, rain, static[c',φ,γ,z,β,suscept])` → `{logit, prob, ψ, FS}` | no | no (torch) | `deep/geo_pinn.py` |
| 2 | **FireSmokeNet** | Spatiotemporal fire/smoke detection (CCTV); temporal false-alarm suppressor | A-aux + data | clip `(B,T,C,H,W)` → `{fire,smoke} prob, flicker_hz` | no | no (torch) | `deep/fire_cnn.py` |
| 3 | **EODownstream** | EO hazard/change probability from a FROZEN foundation encoder | data | multispectral patch `(B,C,H,W)` → `{logit, prob}` | no | no (torch) | `deep/eo_encoder.py` |
| 4 | **DeepAnomaly** | Multivariate telemetry anomaly (unsupervised, normal-only) | data | window `(B,n_feat,T)` → scalar anomaly score | no | no (torch) | `deep/anomaly_deep.py` |
| 5 | **AuthenticityNet** | Media-authenticity (deepfake) — LOW-trust advisory only | data (LOW) | image `(B,C,H,W)` → `p_fake` | no | no (torch) | `deep/deepfake_net.py` |
| 6 | **CQLPolicy** | Offline-RL advisory alarm policy (HOLD/WATCH/ALARM), shielded, OPE-gated | advisory | state `(B,d)` → `{Q-values, shielded action, action probs}` | no | no (torch) | `deep/offline_rl.py` |
| 7 | **GMFHead** | Bounded learned residual on the gated-mixture fusion base | B | `[base, dispersion, salience]` → bounded residual | no | no (torch) | `deep/fusion_head.py` |
| 8 | **AttentionFusionHead** | Learned attention over workstream experts (convex base + bounded residual) | B | `(B,N,4)` expert feats `[p,u,c,r]` (+mask) → fused `p` | no | no (torch) | `deep/fusion_head.py` |
| 9 | **Infinite-slope FS** | Hard deterministic landslide stability gate (feeds shield) | A | `(c',φ',γ,z,β,u_w,σ_s)` → FS (dimensionless) | n/a (closed form) | **yes** ✅ | `ws1b_geophys/fs.py` |
| 10 | **Iverson transient head** | Transient pore-pressure head → `u_w` for FS | A | `(Z,t,D0,K_z,I_z,β[,history])` → ψ [m] | n/a | **yes** ✅ | `ws1b_geophys/iverson.py` |
| 11 | **Fukuzono 1/v** | Creep failure-time forecast with prediction interval | A/B | `(times, velocities, α)` → `t_f` + CI | n/a | **yes** ✅ | `ws1b_geophys/fukuzono.py` |
| 12 | **Caine I–D** | Rainfall intensity–duration landslide threshold | A/B (empirical) | `(I, D, a, b)` → exceedance + ratio | n/a | **yes** ✅ | `ws1b_geophys/caine.py` |
| 13 | **Geo gate** | Noisy-OR combiner of FS/Iverson/Fukuzono/Caine → one geo ExpertOutput | A/B | `GeoInputs` → `GeoResult(FS, …, p_phys, expert)` | n/a | **yes** ✅ | `ws1b_geophys/gate.py` |
| 14 | **Heskestad flame height** | Flame-height physics (consistency/feature) | A | `(Q̇[kW], D[m])` → L [m] | n/a | **yes** ✅ | `ws1a_firephys/established_ef.py` |
| 15 | **Byram convection number** | Plume- vs wind-dominated regime check (reject non-fire) | A | `(Q̇_c, U)` → N_c (dimensionless) | n/a | **yes** ✅ | `ws1a_firephys/established_ef.py` |
| 16 | **Strouhal puffing freq** | Pool-fire flicker frequency `f≈1.5/√D` | A (EF) / C-when-learned | `D[m]` → f [Hz] | n/a | **yes** ✅ | `ws1a_firephys/established_ef.py` |
| 17 | **Gray-body radiation** | Stefan–Boltzmann radiance ↔ temperature; Beer–Lambert transmittance | A | `(T,ε[,path])` → radiance / T / τ | n/a | **yes** ✅ | `ws1a_firephys/established_ef.py` |
| 18 | **Novel ND fire terms** | De-aliased flicker, smoke-transmittance T, ignition index | **C (default OFF)** | per-term dicts → soft consistency/feature | n/a | **yes** ✅ | `ws1a_firephys/novel_nd.py` |
| 19 | **Fire gate** | Fuse detector confidence + physics plausibility → fire ExpertOutput | A (+C gated) | `FireInputs` → `FireResult(p_fire, consistency, expert)` | n/a | **yes** ✅ | `ws1a_firephys/gate.py` |
| 20 | **NF-1..NF-4** | Consistency / reliability / conflict→uncertainty / salience primitives | B (C-adjacent) | per-expert `(p,u,c,r)` → weights, `U*`, `S` | n/a | **yes** ✅ | `ws5_fusion_rl/nf.py` |
| 21 | **FM-1 precision mean** | DEFAULT + fallback fusion (reliability-weighted mean) | B | experts → fused `p` | n/a | **yes** ✅ | `ws5_fusion_rl/fusion_models.py` |
| 22 | **PHARAOH power-mean** | Adaptive-order power mean (anti-complacency) | **C (default OFF)** | experts → fused `p`, ρ | n/a | **yes** ✅ | `ws5_fusion_rl/pharaoh.py` |
| 23 | **GMF (numpy)** | Gated-mixture base + bounded residual (runs exported head) | B | experts (+head) → `p, base, residual, gate` | n/a | **yes** ✅ | `ws5_fusion_rl/gmf.py` |
| 24 | **BLUE/GLS correlation** | Correlation-aware within-group weights (anti-double-count) | B | experts (+corr) → non-neg weights, fused `p` | n/a | **yes** ✅ | `ws5_fusion_rl/correlation.py` |
| 25 | **Hierarchical fusion** | Two-layer: intra-WS group expert → single `decide()` | B | `{group:[experts]}` → group experts / Decision | n/a | **yes** ✅ | `ws5_fusion_rl/hierarchical.py` |
| 26 | **Deep adapter** | Map a deep model's prob → ExpertOutput with class + reliability cap | n/a | `(source, prob, …)` → ExpertOutput | n/a | **yes** ✅ | `ws5_fusion_rl/adapters.py` |
| 27 | **RL baseline + OPE** | Rule baseline + WIS/positivity/ESS OPE admission gate | advisory | logged `(b,t,r)` → OPE verdict | n/a | **yes** ✅ | `ws5_fusion_rl/rl.py` |
| 28 | **Conformal calibration** | Split-CP, WCPS, ACI, Mondrian, CRC miss-risk threshold | n/a | cal scores → quantile / threshold | n/a | **yes** ✅ | `ws6_robust/conformal.py` |
| 29 | **Decision function** | THE single decision: `level = max(conformal_level, shield_floor)` | n/a | experts (+shield) → `Decision` | n/a | **yes** ✅ | `ws5_fusion_rl/decision.py` |
| 30 | **Shield** | Monotone safety floor (can only RAISE level) | A | `ShieldSignals` → `ShieldResult(floor)` | n/a | **yes** ✅ | `ws5_fusion_rl/shield.py` |

Full per-model sections (all 13 required fields each) are in `05a_MODELS.md` (rows 1–8) and `05b_MODELS.md`
(rows 9–30). The closing meta-fusion / comparison / decision-guide below ties them together.

---

## CLOSING A. End-to-end meta-fusion (how the models combine into one advisory level)

This is the integration contract. All source is from `ws5_fusion_rl/` and `ws6_robust/` (read for this
chapter). The pipeline has **exactly one decision path** (`decision.py` docstring):

```
                 physics gates (ws1a/ws1b)         deep models (deep/, trained on Kaggle)
                 ──────────────────────────         ─────────────────────────────────────
   geo_gate ──► ExpertOutput(geo_phys, Class A)      geo_pinn ─┐
   fire_gate ─► ExpertOutput(fire_phys, Class A)      fire_cnn  ├─ deep_expert(source, prob)  (adapters.py)
                                                       eo        │  → ExpertOutput with class + reliability cap
                                                       anomaly   │     (deepfake HARD-capped r ≤ 0.4)
                                                       deepfake ─┘
                             │                                   │
                             └──────────────┬────────────────────┘
                                            ▼
           (optional) hierarchical.fuse_group per workstream  ──►  one ExpertOutput per group
             • within-group weights = effective_weight (NF) OR BLUE/GLS (correlation.py) if redundancy given
             • propagates u (NF-3), c (agreement), r (reliability-weighted), class (weakest-guarantee wins)
                                            ▼
                        fusion_models.fuse(experts, cfg)   (dispatcher)
             • default/fallback  : FM-1 precision-weighted mean          (Class B)
             • if fusion.model=GMF: gmf_fuse → base + bounded residual    (Class B; residual=0 w/o a head)
             • if operator.pharaoh: PHARAOH power-mean (ρ=1+κ·D·S)         (Class C, OFF by default)
             → FusionResult(p, u_star = NF-3 conflict uncertainty, salience = NF-4, model, used_classC)
                                            ▼
                        decision.decide(experts, shield_signals, cfg)
             • point = conformal_level(fused.p, p*, level_thresholds)      p* = C_FA/(C_FA+C_miss) = 0.0476
             • floor = shield_floor(shield_signals)   (monotone; can only RAISE)
             • level = Level.raise_to(point, floor)
             • uncertain = (no experts) OR (u_star > 0.6) OR drift   → abstain + escalate, never silent
             → Decision(level, risk, conformal set, shield, uncertain, advisory=True, used_classC)
```

**Gating.** Per expert, the effective (gating) weight is (`nf.effective_weight`, UNTESTED-free — this is
numpy, runs):

```
w~_i = available_i · r_i · c_i · exp( −u_i / τ ),   τ = 0.5 default
```

so an expert is down-weighted by low reliability `r`, low physics-consistency `c`, or high uncertainty `u`.
FM-1 normalizes these to a convex combination of the experts' probabilities. GMF uses the same weights for
its gate, then adds a residual that is **hard-clipped to ±`residual_cap` (default 0.1)** and defaults to **0**
when no trained head is loaded — so with no head, GMF ≡ FM-1 (verified by construction, `gmf.py`).

**Uncertainty propagation.** NF-3 (`nf.nf3_conflict_to_uncertainty`):

```
U* = Σ w_i u_i  +  λ · D(p),   D(p) = weighted dispersion of the p_i,   λ = 0.3 default
```

Disagreement between experts (`D`) *raises* the fused uncertainty, so conflict drives the system toward
"uncertain," not toward a confident wrong answer. `U*` sets the `Reliability` enum
(`decision._reliability_from_uncertainty`: <0.2 HIGH, <0.4 MEDIUM, <0.6 LOW, else UNRELIABLE; drift forces
UNRELIABLE) and widens the provisional conformal prediction set (`decision._pred_set`).

**Missing / out-of-regime behavior.** `ExpertOutput.available=False` experts are dropped from every sum
(FM-1, GMF, NF, hierarchical). If **no** expert is available, `fuse` returns `p=0` and `decide` sets
`uncertain=True` (`decision.decide`: `uncertain = (not avail) or …`). Physics gates fail safe: Iverson
returns 0 head for `t≤0`; Caine returns NaN threshold for `D≤0`; `nd2_transmittance_temperature` lets its
uncertainty `σ_K` **blow up as transmittance τ_s → 0** (ill-conditioned ⇒ "uncertain"). Graceful modality
degradation is handled in `ws6_robust/missing_modality.py` (C8). `[CONFIRMED by code]`.

**Bounded residual (the central safety property).** Only the GMF/attention residual can nudge the fused
value, and it is clipped to ±cap, so a mis-trained head **cannot dominate the physics-anchored base**
(`gmf.bounded_residual`, `fusion_head.AttentionFusionHead`). The attention base is additionally **convex**
(softmax over experts) so it stays within `[min_i p_i, max_i p_i]` — attention can re-weight but cannot
invent a probability outside the experts' own range. `[CONFIRMED by code]`.

**Shield (deterministic, monotone, un-trained).** `shield.shield_floor` raises a floor from hard signals:
`FS<1` → ORANGE; corroborated `tilt_rate>5°/day` (≥2 nodes) → RED; `rain_24h>150 mm` on high-susceptibility
slope → ORANGE; GLOF lake-drop + downstream stage-jump → RED; fire multi-node → ORANGE. The decision takes
`max(point, floor)` — the shield can **only raise** the level, never lower it (Rule 19). A single
uncorroborated node cannot reach RED (spatial corroboration required). `[CONFIRMED by code]`.

**Calibrated thresholds.** `decision.conformal_level` maps risk to a level at cut points `(p*, 4p*, 10p*)`
by default, or at **calibrated** cut points from `ws6_robust.conformal_risk_threshold` (RCPS/CRC) when a
calibration set exists — provably bounding the miss-rate instead of using an ad-hoc multiplier.

**Advisory invariant.** Every output is a `Decision(advisory=True)` for a human operator; **no path issues a
public alert** (R19). The deepfake expert's reliability is hard-capped at 0.4 in `adapters._POLICY`, so it can
never gate a life-safety decision. `[CONFIRMED by code]`.

---

## CLOSING B. All-models comparison table (annotated)

"Our result" is **not measured** for every learned model (nothing trained). Paper results are source-reported
and labeled; classic physics references are journal papers with **no arXiv ID in this repo's ledger** (the
ledger is EO/ML-weighted; `REFERENCES.md`). Full citations → chapter 19.

| Model | Needs training? | Our measured result | Representative source (status) | Deploy gate |
|-------|-----------------|----------------------|-------------------------------|-------------|
| GeoPINN | yes (Kaggle) | **not measured** | PINN method = Raissi et al. 2019 (classic, no repo arXiv); Iverson 2000 WRR physics | `admit_model` spatial-CV real-win |
| FireSmokeNet | yes | **not measured** | CNN+GRU video; Strouhal from Cetegen & Ahmed 1993 | `admit_model` |
| EODownstream | yes (head only) | **not measured** | EO FMs (Prithvi/SatMAE/Clay) named in code docstring, no repo arXiv | `admit_model` + record encoder |
| DeepAnomaly | yes (normal-only) | **not measured** | Deep-SVDD = Ruff et al. 2018 (classic, no repo arXiv) | per-site threshold calibration |
| AuthenticityNet | yes | **not measured** | two-stream RGB+FFT; low-trust (`_CANON.md §6`) | r≤0.4 cap; never gates |
| CQLPolicy | yes (offline) | **not measured** | CQL = Kumar et al. 2020 (**arXiv 2006.04779**; note-only, not a ledger row) | `ope_admission` (positivity+ESS+value) |
| GMFHead / AttentionFusionHead | yes | **not measured** | learned residual/attention fusion | residual ±cap; convex base |
| Infinite-slope FS | no (closed form) | 128-test golden monotonicities **pass** `[CONFIRMED]` | standard geotech; Lu & Likos suction | drives shield `FS<1` |
| Iverson head | no | multipulse/bug-guard golden tests **pass** `[CONFIRMED]` | Iverson 2000 WRR | feeds FS as `u_w` |
| Fukuzono 1/v | no | CI/delta-method tests **pass** `[CONFIRMED]` | Fukuzono 1985 / Voight 1988 | advisory lead-time |
| Caine I–D | no | golden tests **pass** `[CONFIRMED]`; coeffs must be re-fit locally | Caine 1980; distribution view 2608.12422 `[ABS]` | soft; coeffs config-driven |
| Heskestad/Byram/Strouhal/gray-body | no | golden tests **pass** `[CONFIRMED]` | Heskestad 1983, Byram, Cetegen&Ahmed 1993 | consistency/feature only |
| FM-1 / NF / GMF / PHARAOH / BLUE / hierarchical | no | fusion tests **pass** `[CONFIRMED]` | cost-loss 2601.05921 `[ABS]`; spatial-CV 2608.22293 `[ABS]` | PHARAOH/GMF-C OFF by default |
| Conformal (CP/ACI/Mondrian/CRC) | no (calibrates) | CP/ACI/Mondrian/CRC tests **pass** `[CONFIRMED]` | Gibbs & Candès 2021 (ACI); Angelopoulos et al. 2022 (CRC) | voided under drift |
| Decision / Shield / RL-OPE | no | decision/shield/OPE tests **pass** `[CONFIRMED]` | cost-loss decision theory | single path; shield raises only |

---

## CLOSING C. "Which model when" — decision guide

- **Landslide / slope, you have soil params + rainfall:** run the **numpy geo gate** (FS + Iverson + Caine
  [+ Fukuzono if creep velocities exist]) — it always runs offline and drives the hard shield (`FS<1`). Add
  **GeoPINN** as *corroborating* evidence only (never a substitute for the hard gate; `MODEL_CARDS.md §1`).
- **Creep instrument with a rising trend:** **Fukuzono 1/v** for a failure-time forecast — but report the
  **prediction interval**, not a point (advisory, R19). Needs ≥ a few positive velocities.
- **CCTV fire/smoke:** **FireSmokeNet** (temporal GRU kills single-frame glint/headlight false alarms);
  **fire gate** supplies the Heskestad/Byram physics plausibility. Keep the Strouhal/ND Class-C terms OFF
  unless validated.
- **Satellite change / susceptibility:** **EODownstream** (frozen encoder + small head) — cheap under the
  GPU budget; record which encoder was used (Rule 16).
- **IoT telemetry stream, no labels:** **DeepAnomaly** (trained on normal only) as the admitted upgrade; the
  always-on fallback is the **numpy ws8 ensemble** (`CODE_INVENTORY §7`).
- **Crowd-sourced / social media clip:** **AuthenticityNet** to *down-weight* suspect media — it can only
  suppress confidence, never trigger (r ≤ 0.4).
- **Turning a fused risk into HOLD/WATCH/ALARM:** the **RuleBaselinePolicy** (threshold = p* = 0.0476) is the
  default; **CQLPolicy** is used *only* if `ope_admission` admits it (positivity + ESS + value ≥ baseline),
  and it is always raised to the shield floor.
- **Combining several experts:** default **FM-1**; use **hierarchical + BLUE/GLS** when a workstream has
  redundant sensors (anti-double-count); turn on **GMF** residual only with a validated exported head; keep
  **PHARAOH** OFF unless its anti-complacency behavior is explicitly wanted and validated.
- **Reporting any number:** nothing may be advertised until `train.admit_model` (spatial-block CV real-win
  over climatology AND logistic, bootstrap CI lower bound > 0) admits the model (R16) — and today that gate
  has **not been run on real data** (no datasets).

See `05a_MODELS.md` and `05b_MODELS.md` for the full per-model treatment.
