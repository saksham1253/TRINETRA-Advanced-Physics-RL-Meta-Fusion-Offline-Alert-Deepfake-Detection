<div align="center">

# TRINETRA

### Multi-hazard early warning for the Indian Himalaya — camera AI + physics + a cost-based alarm rule

**Team Sankat Mochak** · Research prototype · Advisory only · Not field-validated

`fire` · `smoke` · `landslide` · `GLOF` · `fake-media check` · `LoRa + DTN last mile`

</div>

---

## In one line

> **Sees a disaster early. Checks it against physics. Warns only when it is worth it — and still reaches the village when the internet is down.**

Every number below was **measured by us** on public datasets with **spatial block cross-validation** (whole locations / video sequences kept
out of training), mostly over **3 seeds**. A model enters the live system only if it beats simple baselines with a 95% confidence interval.

## Headline results

| Result | What it means |
|---|---|
| **−55% false alarms** on unseen look-alikes (stack 0.35 → 0.16 at equal 90% recall); DeepFire AUC kept 0.998 → 0.997 | Confuser-aware retraining **admitted 3/3 seeds** — our first learned upgrade that passed the gate |
| **0.758 ROC-AUC** on 184 real Indian landslides, **zero training** | A 1980 physics law (Caine) + NASA rainfall already works; FM-1 fusion with rain → 0.779 |
| **+0.47** video score (detection − false alarm) with 3 models + temporal check | Best single model +0.32, our CNN alone +0.01 (49 FireSense videos, small n) |
| **0.999 ROC-AUC** on a fire dataset never used in training | Trained on D-Fire, tested on DeepFire after de-duplication |
| Deepfake 0.961 → **0.450** on new generators · RL **not deployed** (held-out LCB −0.08) · stacking **not admitted** | We report failures too; the simple rules stay in charge |

---

## System overview

```mermaid
%%{init: {'theme':'dark','themeVariables':{'background':'#0d0a09','primaryColor':'#211916','primaryTextColor':'#f7efe8','primaryBorderColor':'#ff6a1a','lineColor':'#ff8a3d','secondaryColor':'#17110f','tertiaryColor':'#17110f','fontFamily':'Inter, sans-serif'}}}%%
flowchart LR
  subgraph IN["Inputs"]
    CAM["CCTV / camera frames"]
    RAIN["NASA POWER rainfall"]
    DEM["Terrain DEM (slope, elevation)"]
    MEDIA["Shared photos / news"]
    LAKE["Glacial lake inventory"]
  end
  subgraph EXP["Experts (each outputs p, u, c, r)"]
    CNN["Fire CNN"]
    ZS["CLIP zero-shot"]
    CP["CLIP probe<br/>(confuser-aware, S)"]
    VAL["Temporal video validator"]
    FP["Fire physics<br/>flame · plume · flicker · Byram"]
    GP["Landslide physics<br/>FS · Iverson ψ · Caine · Fukuzono"]
    DF["Deepfake check<br/>(low-trust down-weighter)"]
    GL["GLOF power laws"]
  end
  subgraph DEC["One decision path"]
    FUSE["FM-1 fusion<br/>w = r·c·e^(−u/τ)"]
    SH["Physics shield<br/>(can only RAISE)"]
    PS["Cost-loss threshold<br/>p* = C_FA/(C_FA+C_miss) = 0.048"]
    LVL["Level: Watch / Warning / Emergency"]
  end
  subgraph OUT["Last mile"]
    OP["Operator approval"]
    CAP["CAP → SACHET / SMS / cell broadcast"]
    LORA["LoRa mesh + DTN"]
    SIR["Village siren"]
  end
  CAM --> CNN & ZS & CP --> VAL --> FUSE
  CAM --> FP --> SH
  RAIN --> GP
  DEM --> GP --> SH
  GP --> FUSE
  MEDIA --> DF --> FUSE
  LAKE --> GL --> SH
  FUSE --> PS --> LVL
  SH --> LVL
  LVL --> OP --> CAP
  OP --> LORA --> SIR
```

## The decision, step by step

```mermaid
%%{init: {'theme':'dark','themeVariables':{'background':'#0d0a09','primaryColor':'#211916','primaryTextColor':'#f7efe8','primaryBorderColor':'#ff6a1a','lineColor':'#ff8a3d'}}}%%
flowchart TD
  A["Each expert i gives p_i (probability), u_i (uncertainty),<br/>c_i (physics consistency), r_i (reliability)"] --> B["Weight w_i = r_i · c_i · exp(−u_i / τ), τ = 0.5"]
  B --> C["Fused risk p = Σ w_i p_i / Σ w_i"]
  C --> D{"p ≥ p* ?<br/>p* = 5 / (5 + 100) = 0.048"}
  D -- no --> E["No alert"]
  D -- "p* … 4p*" --> F["WATCH"]
  D -- "4p* … 10p*" --> G["WARNING"]
  D -- "≥ 10p*" --> H["EMERGENCY"]
  S["Physics shield: FS &lt; 1, Caine ratio &gt; 1, multi-node agreement,<br/>tilt, 24 h rain, GLOF drop"] -- "floor (max)" --> F & G & H
  E & F & G & H --> O["Human operator approves any public alert"]
```

## Landslide physics chain (zero training)

```mermaid
%%{init: {'theme':'dark','themeVariables':{'background':'#0d0a09','primaryColor':'#211916','primaryTextColor':'#f7efe8','primaryBorderColor':'#ff6a1a','lineColor':'#ff8a3d'}}}%%
flowchart LR
  R["Rain (NASA POWER)<br/>1, 3, 7, 15, 30 day windows"] --> I["Iverson diffusion<br/>∂ψ/∂t = D₁ ∂²ψ/∂Z²<br/>D₁ = D₀ / cos²β"]
  I --> U["Pore pressure<br/>u = γ_w · ψ"]
  U --> FS["Infinite-slope FS<br/>(c′ + (γz cos²β − u) tanφ′) / (γz sinβ cosβ)"]
  R --> CA["Caine threshold<br/>I = 14.82 · D^−0.39"]
  FS --> G["Geo gate (noisy-OR)<br/>p = 1 − Π(1 − p_i)"]
  CA --> G
  D["DEM slope, elevation"] --> FS
  G --> SH["Shield floor + FM-1 expert"]
```

## Offline last mile: LoRa + DTN

```mermaid
%%{init: {'theme':'dark','themeVariables':{'background':'#0d0a09','actorBkg':'#211916','actorTextColor':'#f7efe8','actorBorder':'#ff6a1a','signalColor':'#ff8a3d','signalTextColor':'#f7efe8','noteBkgColor':'#17110f','noteTextColor':'#f7efe8'}}}%%
sequenceDiagram
  participant D as TRINETRA decision
  participant O as Operator
  participant G as Gateway (15 m mast)
  participant R as Ridge relay (12 m)
  participant V as Village siren (6 m)
  D->>O: WARNING, zone Z
  O->>G: approve
  alt internet up
    G->>G: CAP → SACHET / SMS (~1 min)
  else internet down
    G->>R: 24-byte alert, SF10, 0.37 s airtime (copies 8 → 4)
    R->>V: store-carry-forward (Spray-and-Wait, copies 4 → 2)
    V->>V: siren 120 dB @ 30 m (~1.6 km radius)
    Note over G,V: ~1.24 s per hop · 10-minute deadline per village
  end
  G-->>G: internet returns → flush DTN queue to SACHET
```

## Kaggle training pipeline (how the results were made)

```mermaid
%%{init: {'theme':'dark','themeVariables':{'background':'#0d0a09','primaryColor':'#211916','primaryTextColor':'#f7efe8','primaryBorderColor':'#ff6a1a','lineColor':'#ff8a3d'}}}%%
flowchart LR
  DS[("happyparsi/trinetra-dataset<br/>18 public datasets")] --> A["A · fire CNN + colour baseline + video"]
  DS --> B["B · CLIP zero-shot + probe"]
  DS --> C["C · deepfake"]
  DS --> Dd["D · EO heads<br/>(Landslide4Sense, Sen1Floods11)"]
  NASA[("NASA GLC + POWER<br/>HMAGLOFDB")] --> P["P · physics hindcast, GLOF,<br/>Geo-PINN, geo meta-fusion, RL env"]
  A & B & C --> F["F · fusion + offline RL"]
  A --> X["X · cross-modal stack on video"]
  X --> S["S · confuser-aware retrain"]
  A & B & C & F & P & X & S --> Z["Z · final_bundle.py<br/>meta-fusion · master merge · 34 graphs · docs"]
  Z --> FE["Judge page + 3D console"]
```

---

## Scorecard (all measured results)

| Hazard | Model | Metric | Value | Gate |
|---|---|---|---|---|
| Fire / smoke (CCTV) | fire_cnn | ROC-AUC OOF / held-out | 0.768 / 0.972 | 0/3 |
| Fire / smoke (CCTV) | colorhist | ROC-AUC OOF / held-out | 0.681 | – |
| Fire / smoke (zero-shot) | zeroshot | ROC-AUC OOF / held-out | 0.917 / 1.000 | 0/1 |
| Fire / smoke (few-shot CLIP) | clip_probe | ROC-AUC OOF / held-out | 0.962 / 0.998 | 0/1 |
| Fire META-FUSION (stack: fire_cnn + zeroshot + clip_probe + colorhist) | fire_meta_fusion | ROC-AUC OOF / held-out; stack − best single AUC | 0.951 / 0.999; -0.008 | 0/3 |
| Fake media | deepfake | ROC-AUC OOF / held-out | 0.961 / 0.450 | 0/3 |
| Fire video (temporal validator) | video | false-alarm videos raw → validated | 0.893 → 0.853 | – |
| Landslide (physics, zero training) | caine_ratio | ROC-AUC spatial OOF | 0.758 | physics (no gate needed) |
| GLOF (lake area → volume) | glof_physics | exponent b (95% CI) | 1.13 (0.71-1.50) | fit |
| RL alarm policy (C_miss 100) | cql_learned vs physics_rule | return CQL / rule / oracle | -22.5 / -22.8 / -22.9 | deploy False |
| RL alarm policy (C_miss 1000) | cql_learned vs physics_rule | return CQL / rule / oracle | -200.9 / -200.0 / -200.0 | deploy False |
| RL alarm policy (C_miss 5000) | cql_learned vs physics_rule | return CQL / rule / oracle | -486.8 / -478.1 / -478.5 | deploy False |
| Landslide (Geo-PINN) | geo_pinn | ROC-AUC OOF / held-out | 0.716 | 0/1 |
| Landslide META-FUSION (physics + rain, FM-1) | geo_fusion | ROC-AUC OOF (calibrated FM-1) | 0.779 | 0/3 |
| RL on fused alerts | offline_rl | gain vs rule (LCB) | +0.615 (+0.237) | deploy 3/3 |
| RL on REAL-paired fire meta-fusion | offline_rl_real | gain vs rule (LCB) | +1.076 (+0.773) | deploy 3/3 |
| RL HELD-OUT (block folds, true reward) | offline_rl_heldout | CQL gain vs rule / vs tuned rule (LCB) | +0.485 (-0.081) / -0.015 (-0.433) | deploy 0/3 |
| Fire CROSS-MODAL (per-frame stack + temporal validator, FireSense) | crossmodal | video J (detect − FA): stack / clip_probe / fire_cnn | +0.467 / +0.320 / +0.008 | – |
| Fire CONFUSER-AWARE retrain (leave-one-confuser-set-out) | stress | FA at equal recall 0.90: probe base → conf / stack base → conf; DeepFire AUC base → conf | 0.427 → 0.319 / 0.346 → 0.157; 0.998 → 0.997 | 3/3 |
| Fusion (all experts) | p_zeroshot | value score (best rule) / FM-1 | 0.108 / 0.005 | – |

*Gate* = admitted / deploy verdict across seeds (Rule 16: must beat climatology and logistic baselines on cost-weighted value with a 95% CI).
Source: `results/master_merged/MASTER_RESULTS.md`. D (EO heads) output was not available for the final merge.

---

## Graphs

### Results
| <img src="TRINETRA/figures_final/results/R9_stress_retrain.png" width="420"/> | <img src="TRINETRA/figures_final/results/R7_crossmodal_video.png" width="420"/> |
| **R9** Hard-negative retrain cuts false alarms on unseen look-alikes | **R7** Three models + temporal check beat one on video |
| <img src="TRINETRA/figures_final/results/R4_landslide_auc.png" width="420"/> | <img src="TRINETRA/figures_final/results/R1_fire_roc_oof_and_heldout.png" width="420"/> |
| **R4** Landslide: physics with zero training | **R1** Fire ROC: our folds vs a never-seen dataset |
| <img src="TRINETRA/figures_final/results/R0_scorecard_all_auc.png" width="420"/> | <img src="TRINETRA/figures_final/results/R6_generalisation_gap.png" width="420"/> |
| **R0** Every ROC-AUC in one chart | **R6** Who survives a new data source |
| <img src="TRINETRA/figures_final/results/R2_calibration.png" width="420"/> | <img src="TRINETRA/figures_final/results/R3_alert_flood_vs_base_rate.png" width="420"/> |
| **R2** Calibration after temperature scaling | **R3** Base-rate correction (proposal) |
| <img src="TRINETRA/figures_final/results/R5_rl_heldout.png" width="420"/> | <img src="TRINETRA/figures_final/results/R8_crossmodal_confusers.png" width="420"/> |
| **R5** RL on held-out folds | **R8** False alarms per confuser set |

### Deeper analysis
| <img src="TRINETRA/figures_final/extra/G09_caine_scatter.png" width="420"/> | <img src="TRINETRA/figures_final/extra/G08_landslide_features.png" width="420"/> |
| **G09** Caine line on real Indian events | **G08** Landslide days vs normal days |
| <img src="TRINETRA/figures_final/extra/G04_confuser_false_alarms.png" width="420"/> | <img src="TRINETRA/figures_final/extra/G06_fire_meta_rules.png" width="420"/> |
| **G04** Where false alarms come from | **G06** Ways of combining fire models |
| <img src="TRINETRA/figures_final/extra/G10_glof_power_laws.png" width="420"/> | <img src="TRINETRA/figures_final/extra/G11_rl_env_policies.png" width="420"/> |
| **G10** GLOF power laws (HMAGLOFDB) | **G11** RL simulator policies |
| <img src="TRINETRA/figures_final/extra/G13_score_distributions.png" width="420"/> | <img src="TRINETRA/figures_final/extra/G14_confusion_matrices.png" width="420"/> |
| **G13** Score distributions | **G14** Confusion matrices |

### Physics explainers (computed with the repo's own functions)
| <img src="TRINETRA/figures_final/physics/01_fs_vs_pore_pressure.png" width="420"/> | <img src="TRINETRA/figures_final/physics/02_iverson_pressure_head.png" width="420"/> |
| FS falls as pore pressure rises | Iverson pressure-head diffusion |
| <img src="TRINETRA/figures_final/physics/05_fire_physics.png" width="420"/> | <img src="TRINETRA/figures_final/physics/07_cost_loss_and_prior_shift.png" width="420"/> |
| Flame height, Byram number, flicker | Where p* comes from |
| <img src="TRINETRA/figures_final/physics/08_lora_range_airtime.png" width="420"/> | <img src="TRINETRA/figures_final/physics/09_fresnel_real_terrain.png" width="420"/> |
| LoRa range vs airtime | Fresnel zone on real Chamoli terrain |

All 34 graphs with Hinglish explanations: [`results/final/GRAPHS_EXPLAINED.md`](TRINETRA/results/final/GRAPHS_EXPLAINED.md).

---

## What did not work (and why we keep it in the README)

| Attempt | Result | Decision |
|---|---|---|
| Deepfake detector (CIFAKE) | 0.961 on its source, **0.450** on new generators | Kept only as a low-trust down-weighter; never raises or cancels an alarm |
| Learned alarm policy (offline RL, CQL) | +1.08 in-sample, held-out lower bound **−0.08** | Not deployed; cost rule stays |
| Stacking all fire models | −0.008 AUC vs best single model | Not admitted; FM-1 kept |
| Geo-PINN | 0.716 AUC < Caine 0.758 < rain logistic 0.781 | Research only |

---

## Run it

```bash
# from the repository root
pnpm install
pnpm demo:offline        # judge page on http://localhost:4173  ·  live 3D console at /#console
pnpm gateway             # optional: live mode, streams the repo's Python fuse() + decide()
python3 TRINETRA/trinetra/demo.py # Python end-to-end: fire + geo cycles through the single decide()
```
Re-make every result from the Kaggle outputs: `TRINETRA_Z_FINAL.ipynb` (CPU, 5–10 min) or
`python TRINETRA/trinetra/kaggle/final_bundle.py --zips out_*.zip --out FINAL`, then `python3 tools/import_final.py TRINETRA_FINAL.zip`.

## Repository map

| Path | What |
|---|---|
| `src/judge/` · `src/console/` | Judge page (default) and 3D command console (`/#console`), React + Vite |
| `tools/` | figure, data-pack and gateway scripts (`make_figures.py`, `import_final.py`, `mock_gateway.py`) |
| `TRINETRA/trinetra/src/trinetra/` | Python package: `ws1a_firephys`, `ws1b_geophys`, `ws2_deepfake`, `ws3_alert` (CAP, siren, LoRa, DTN), `ws5_fusion_rl` (FM-1, shield, decide, RL env), `deep/` (PyTorch models), `eval/`, `pipeline/orchestrator.py` |
| `TRINETRA/trinetra/kaggle/` | training + evaluation scripts, `final_bundle.py`, `extra_figures.py`, `merge_all_results.py` |
| `TRINETRA/exports/kaggle_notebooks/` | self-contained Kaggle notebooks A, B, C, D, F, P, X, S, Z + run order |
| `TRINETRA/results/` | measured reports; `master_merged/` = final scorecard |
| `TRINETRA/figures_final/` | all final graphs |
| `TRINETRA/docs/19_TRINETRA_EXPLAINED/` | Hinglish book; `PHYSICS_FROM_ZERO/` = physics derivations from zero (P00–P06) |
| `TRINETRA/docs/20_FINAL/` | `DATASETS_USED.csv/.tsv`, landslide feature table, code + integration guide, LoRa + DTN brief with costs |

## Datasets
18 public datasets (D-Fire, DeepFire, FIRE, Home-fire, Weather, Candle flames, Intel scenes, FireSense, CIFAKE, StyleGAN faces, AI-art,
NASA Global Landslide Catalog, NASA POWER, terrain DEM, HMAGLOFDB v4, Landslide4Sense, Sen1Floods11, Hephaestus). Features, labels,
sizes, splits and licences: [`docs/20_FINAL/DATASETS_USED.csv`](TRINETRA/docs/20_FINAL/DATASETS_USED.csv). Bundle on Kaggle: `happyparsi/trinetra-dataset`.

## Cost (planning, not a tender)
One valley (1 gateway + 3 ridge relays + 5 village sirens) ≈ **₹1.2–1.4 lakh**. Uttarakhand priority network ≈ **₹1.5–3.0 crore** in
year one = 0.15–0.29% of the state's annual disaster-management allocation. Details: [`docs/20_FINAL/LORA_DTN_HINGLISH.md`](TRINETRA/docs/20_FINAL/LORA_DTN_HINGLISH.md).

---

## Team Sankat Mochak — roles

| Member | Role | Owns |
|---|---|---|
| **Member 1 (team lead)** | **Physics Research Lead** | All physics models and their derivations: landslide (FS, Iverson, Caine, Fukuzono, geo gate), fire (Heskestad, McCaffrey, Byram, flicker), decision physics (cost-loss p*, noisy-OR, shield), radio (link budget, Fresnel), GLOF power laws, Geo-PINN loss; `PHYSICS_FROM_ZERO/` book; physics graphs; physics unit tests / golden values; physics Q&A for judges |
| **Member 2** | ML & Evaluation Lead | Fire CNN, CLIP zero-shot / probe, deepfake, confuser-aware retrain (S), cross-modal stack (X); Kaggle notebooks and run order; spatial-CV protocol, calibration, admission gate; scorecard and result graphs |
| **Member 3** | Fusion, Alerts & Field Systems Lead | FM-1 fusion, shield and `decide()`; offline RL gate; CAP / SACHET path; LoRa + DTN last mile, relay placement, hardware BOM and cost model; IoT plan and safety / legal review |
| **Member 4** | Product, Demo & Story Lead | Judge page and 3D console, live gateway demo, slides and live-flow animation; datasets catalogue; README, demo runbook, final pitch and timing |

---

<sub>TRINETRA is a research prototype. Advisory only; not an official warning system. Every public alert needs human approval. All map
locations in the demo are synthetic. Results are on small public datasets and are not field-validated.</sub>
