# TRINETRA — kaunsa code kya karta hai, models aapas me kaise jude hain, aur frontend tak data kaise jaata hai (Hinglish)

Team Sankat Mochak. Is file me koi naya number nahi hai; saare numbers `master/MASTER_RESULTS.md` me hain (OUR RESULTS, prototype pack).

## 1. Ek line me poora system

> **Data → har hazard ka expert (CNN / CLIP / physics) → probability p → FUSION (FM-1) → physics SHIELD → cost-loss threshold p\*
> → alert level (ADVISORY / WATCH / WARNING) → operator approve kare → siren / LoRa / CAP message.** Frontend console yahi poora flow
> dikhata hai, asli model scores ke saath.

```
 Kaggle datasets ──► data_adapters/build_npz.py, build_geo.py, build_eo.py   (images/CSV → .npz, spatial blocks)
                         │
     ┌───────────────────┼─────────────────────┬──────────────────────┬────────────────────┐
     ▼                   ▼                     ▼                      ▼                    ▼
  A: fire_cnn        B: CLIP zero-shot     C: deepfake           P: landslide physics   D: EO heads
  + colorhist        + CLIP probe          (AuthenticityNet)     Caine, FS, ΔFS,        (Landslide4Sense,
  + video validator                                              Geo-PINN, GLOF          Sen1Floods11)
     │                   │                     │                      │
     └───────► X: cross-modal stack ◄──────────┘                      ▼
               S: confuser-aware retrain                     geo meta-fusion (FM-1 + shield)
                         │                                            │
                         ▼                                            ▼
               fire meta-fusion (stack)  ─────►  F: fusion + offline RL  ◄────┘
                                                 │
                                                 ▼
                       ws5_fusion_rl.decide()  (EK hi decision function, saare hazards ke liye)
                                                 │
                       ws3_alert: CAP message, siren, LoRa mesh, DTN queue (operator approval ke baad)
                                                 │
                       Z: final_bundle.py → master.json + graphs → frontend console (src/console)
```

## 2. Har account / notebook kya chalata hai

| Account | Notebook | Code jo chalta hai | Output |
|---|---|---|---|
| A | `TRINETRA_A_final_fixed` | `kaggle/train_classifier.py --model fire` (fire CNN, 5-fold spatial CV, 3 seeds), `baseline_colorhist.py`, `eval_video.py` | `fire/`, `colorhist/`, `video/` |
| B | `TRINETRA_B_final` | `kaggle/eval_zeroshot.py` (CLIP ViT-L-14 text prompts = zero-shot; embedding par logistic = clip_probe) | `zeroshot/`, `clip_probe/` |
| C | `TRINETRA_C_final` | `train_classifier.py --model deepfake` (CIFAKE train, faces + AI-art held-out) | `deepfake/` |
| D | `TRINETRA_D_v2` | `train_classifier.py --model eo` on `l4s.npz`, `s1f.npz` (+ `heph.npz`) | `eo_l4s/`, `eo_s1f/` |
| P | `TRINETRA_P_final` | unit tests, `geo_physics_hindcast.py`, `glof_physics_check.py`, `rl_env_eval.py`, `train_geo_pinn.py`, `geo_meta_fusion.py` | `geo/` |
| F | `TRINETRA_F_phase2_fixed / final_fixed` | `build_fusion_cache.py`, `train_fusion_head.py`, `make_rl_logs.py`, `train_offline_rl.py`, `merge_all_results.py` | `fusion/`, `rl/`, `master/` |
| X | `TRINETRA_X_crossmodal_final` | `crossmodal_fusion.py` (har FireSense frame + har confuser par teeno experts + stack + temporal validator) + stress | `crossmodal/`, `stress/` |
| S | `TRINETRA_S_stress_final` | `stress_train.py` (hard negatives ke saath retrain, leave-one-confuser-set-out) | `stress/` |
| **Z** | **`TRINETRA_Z_FINAL`** | **`final_bundle.py`**: fire meta-fusion dobara, master merge, saare graphs, docs, ek zip | **`TRINETRA_FINAL.zip`** |

## 3. Code ke main folders (TRINETRA/trinetra/src/trinetra)

| Folder | Kya hai (simple) | Main functions |
|---|---|---|
| `common/` | Config (saare default numbers), types (`ExpertOutput`, `Decision`, `Hazard`) | `Config`, `ExpertOutput(p, u, c, r)` |
| `ws1a_firephys/` | aag ki physics: flame height (Heskestad), plume temperature (McCaffrey), Byram number, flicker frequency | `fire_gate()`, `flame_height_heskestad()` |
| `ws1b_geophys/` | landslide physics: factor of safety, Iverson pressure head, Caine line, Fukuzono inverse velocity, noisy-OR gate | `factor_of_safety()`, `caine_threshold()`, `geo_gate()` |
| `ws1b_eo/` | satellite (EO) model ka wrapper | – |
| `ws2_deepfake/` | fake photo check: model + reliability down-weight | `authenticity_adjusted_reliability()` |
| `ws3_alert/` | alert bhejna: CAP XML, siren bus, LoRa last-mile planner, DTN queue, operator approval | `last_mile.plan()`, `SirenBus`, `cap.py` |
| `ws4_cctv/` | camera ke liye temporal validator (aag kai frames tak dikhe tabhi maano) | `TemporalValidator` |
| `ws5_fusion_rl/` | **models jodne wala dil**: FM-1 fusion, PHARAOH, GMF, BLUE, shield, decide(), RL env | `fuse()`, `decide()`, `ShieldSignals` |
| `ws6_robust/` | drift monitor, conformal calibration | – |
| `ws7_iot/` | IoT sensor (scope ke bahar, sirf code hai) | – |
| `ws8_anomaly/` | anomaly ensemble (sensor time-series) | `anomaly_ensemble()` |
| `deep/` | PyTorch models: `fire_cnn.py`, `deepfake_net.py`, `eo_encoder.py`, `geo_pinn.py`, `offline_rl.py`, `fusion_head.py`; `oof_utils.py` (calibration, OOF save) | – |
| `eval/` | honest evaluation: spatial block k-fold, ECE, value score, climatology baseline, `real_win` gate | `spatial_block_kfold()`, `real_win()` |
| `pipeline/` | **orchestrator**: fire/geo cycle chala ke experts → `decide()`; offline (cloud down) dispatch | `run_fire_cycle()`, `run_geo_cycle()` |

## 4. Models aapas me kaise jude hain (integration, step by step)

1. **Har model ek hi format bolta hai:** `ExpertOutput(p, u, c, r, source, cls)`.
   - `p` = probability (0-1), `u` = uncertainty, `c` = physics consistency, `r` = reliability (deepfake shak ho to kam).
   - Deep model ka score `ws5_fusion_rl/adapters.py: deep_expert()` se `ExpertOutput` banta hai. Physics `fire_gate()` / `geo_gate()` se.
2. **FM-1 fusion (`fusion_models.fuse`)**: weighted average of probabilities. Jis expert ki uncertainty kam aur reliability/consistency
   zyada, uska weight zyada: `w_i = r_i · c_i · exp(−u_i / τ)` (τ = 0.5, `nf.py: effective_weight`), `p_fused = Σ w_i p_i / Σ w_i`.
   Jo expert available nahi (camera band), uska weight 0. Saath me `u*` (fused uncertainty) nikalta hai.
3. **Physics shield (`shield.py`)**: agar physics bole "khatra" (e.g. FS < 1 ya Caine ratio > 1), to level kam se kam WATCH. Shield
   **sirf level badha sakta hai, kabhi ghata nahi sakta.**
4. **Decision (`decision.decide`)**: `level = max(conformal level at p*, shield floor)`. `p* = C_FA / (C_FA + C_miss) = 5/105 = 0.048`.
   Uncertainty zyada ho to reliability LOW aur prediction-set chauda.
5. **Meta-fusion (stack)**: Kaggle par humne check kiya ki kya learned stacking FM-1 se behtar hai. Fire: stack ≈ clip_probe (gate:
   NOT admitted). Landslide: FM-1 calibrated 0.779 vs Caine 0.758. Isliye **live system FM-1 + shield hi use karta hai**; stack sirf report.
5b. **Cross-modal + confuser-aware (X, S)**: FireSense videos par per-frame stack + temporal validator ne (detect − false alarm) +0.47
   diya, clip_probe akele +0.32. S ne CLIP probe ko weather / candle / scenes ke hard negatives ke saath retrain kiya: unseen confuser par
   false alarm (barabar recall 0.90) 0.43 → 0.32, stack 0.35 → 0.16, DeepFire AUC sirf 0.998 → 0.997. **Gate 3/3 seeds ADMITTED**:
   live fire camera expert ke liye yahi confuser-aware probe use karna chahiye.
6. **RL**: offline RL (CQL) ko rule ke against gate kiya; held-out par lower bound < 0, isliye **deploy nahi, rule chalta hai**.
7. **Alert**: decision → `ws3_alert` → operator approve kare tabhi CAP public message. Internet band ho to `offline_dispatch()` local siren
   + DTN queue + LoRa mesh (`last_mile.plan`, Fresnel/terrain check).

**Ek jagah sab kuch chalake dekhna:** `python TRINETRA/trinetra/demo.py` (orchestrator ke fire + geo cycle, synthetic inputs).

## 5. Frontend se link

| Kya | Kahan |
|---|---|
| Measured results table (About modal) | `src/console/panels/Modals.tsx` → `TRINETRA/results/master_merged/master.json` |
| Final graphs gallery (About modal) | `public/results/figures/*.png` + `src/console/data/final_figures.json` |
| Camera scores (simulation) | `src/console/data/evidence_bank.json` (asli OOF image scores, `tools/export_evidence_bank.py`) |
| Fusion + decision (browser me) | `src/console/engine/` (Python formulas TypeScript me, `golden.test.ts` Python ke against check) |
| Live mode | `tools/mock_gateway.py --port 8765` (repo ka Python `fuse()` + `decide()` stream karta hai) |

**Final zip ko frontend me daalna (ek command):**
```
python3 tools/import_final.py TRINETRA_FINAL.zip
```
Ye `master.json`, `MASTER_RESULTS.md`, `RESULTS.md` ko `TRINETRA/results/master_merged/` me, saare graphs `public/results/figures/` me, aur
graph list + Hinglish explanation `src/console/data/final_figures.json` me daal deta hun. Dev server hot-reload se console turant update.

## 6. Datasets
`DATASETS_USED.csv` / `.tsv` (18 datasets: hazard, account, role, model, input features, label, kitni rows, split, license) aur
`DATASET_FEATURES_LANDSLIDE.csv` / `.tsv` (landslide event table ke har column ka matlab + unit).

## 7. Graphs
`GRAPHS_EXPLAINED.md` (FINAL zip me): har graph ka naam, file, aur 3-4 line Hinglish explanation (R0-R9, G01-G14, physics 01-10).
