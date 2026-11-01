# TRINETRA — FINAL (all runs merged)

Team Sankat Mochak. Every number is OUR RESULT on the prototype pack (not comparable to full-benchmark papers).

## Contents

| path | what |
|---|---|
| `master/MASTER_RESULTS.md` | headline scorecard (one row per expert, admitted / deploy verdicts) |
| `master/RESULTS.md` | every model, every metric, mean over seeds |
| `master/master.json` | same, machine-readable (deck / console read this) |
| `DETAILS_ALL_COMPARES.md` | every comparison table: fire + geo meta-fusion, cross-modal, stress, fusion |
| `figures/results/` | measured-result graphs (R0 overview … R9 stress) |
| `figures/physics/` | physics explainer graphs, computed with the repo's own functions |
| `figures/extra/` | G01-G14 extra result graphs (seeds, confusers, landslide features, GLOF, RL, confusion matrices) |
| `GRAPHS_EXPLAINED.md` | har graph + Hinglish explanation (`figures/figures.json` = same, frontend ke liye) |
| `docs/20_FINAL/` | DATASETS_USED.csv/.tsv, DATASET_FEATURES_LANDSLIDE.csv/.tsv, CODE_AND_INTEGRATION_HINGLISH.md |
| `docs/19_TRINETRA_EXPLAINED/` | Hinglish book; `PHYSICS_FROM_ZERO/` = derivations from zero |
| `master/tree/` | raw per-run reports and OOF files used |

## Runs

- **A** (fire CNN + colour baseline + video): final, `208063b0_out_A_final.zip`
- **B** (CLIP zero-shot + probe): final, `c443cff4_out_B_final (1).zip`
- **C** (deepfake): final, `dcb480c7_out_C_final.zip`
- **F** (fusion + offline RL): final, `60f8f99a_out_F_final.zip`
- **S** (confuser-aware stress retrain): final, `b54dc175_out_S_final.zip`
- **X** (cross-modal fire fusion): final, `4c8ecc31_out_X_final (1).zip`
- **missing**: D (EO heads (Landslide4Sense, Sen1Floods11)), P (physics + geo meta-fusion + Geo-PINN)

Fire meta-fusion: fresh fire meta-fusion on attached runs: fire A seeds [0, 1, 2], zeroshot/clip_probe F/F.

## Figures

- `figures/extra/G01_auc_per_seed.png`
- `figures/extra/G02_metrics_compare.png`
- `figures/extra/G03_generalisation.png`
- `figures/extra/G04_confuser_false_alarms.png`
- `figures/extra/G05_video_validator.png`
- `figures/extra/G06_fire_meta_rules.png`
- `figures/extra/G07_geo_fusion_rules.png`
- `figures/extra/G08_landslide_features.png`
- `figures/extra/G09_caine_scatter.png`
- `figures/extra/G10_glof_power_laws.png`
- `figures/extra/G11_rl_env_policies.png`
- `figures/extra/G12_offline_rl_gain.png`
- `figures/extra/G13_score_distributions.png`
- `figures/extra/G14_confusion_matrices.png`
- `figures/physics/01_fs_vs_pore_pressure.png`
- `figures/physics/02_iverson_pressure_head.png`
- `figures/physics/03_caine_threshold.png`
- `figures/physics/04_fukuzono_inverse_velocity.png`
- `figures/physics/05_fire_physics.png`
- `figures/physics/06_plume_temperature.png`
- `figures/physics/07_cost_loss_and_prior_shift.png`
- `figures/physics/08_lora_range_airtime.png`
- `figures/physics/09_fresnel_real_terrain.png`
- `figures/physics/10_noisy_or.png`
- `figures/results/R0_scorecard_all_auc.png`
- `figures/results/R1_fire_roc_oof_and_heldout.png`
- `figures/results/R2_calibration.png`
- `figures/results/R3_alert_flood_vs_base_rate.png`
- `figures/results/R4_landslide_auc.png`
- `figures/results/R5_rl_heldout.png`
- `figures/results/R6_generalisation_gap.png`
- `figures/results/R7_crossmodal_video.png`
- `figures/results/R8_crossmodal_confusers.png`
- `figures/results/R9_stress_retrain.png`

## Scorecard (copy of master/MASTER_RESULTS.md)


- **A**: A final (208063b0_out_A_final.zip)
- **B**: B final (c443cff4_out_B_final (1).zip)
- **C**: C final (dcb480c7_out_C_final.zip)
- **F**: F final (60f8f99a_out_F_final.zip)
- **P**: repo results/ (geo, GLOF, RL env, Geo-PINN)
- **S**: S final (b54dc175_out_S_final.zip)
- **X**: X final (4c8ecc31_out_X_final (1).zip)
- **Z fire meta-fusion (fresh)**: re-run in Z on the attached runs

## Scorecard

| hazard | expert | metric | value | admitted / deploy | note |
|---|---|---|---|---|---|
| Fire / smoke (CCTV) | fire_cnn | ROC-AUC OOF / held-out | 0.768 / 0.972 | 0/3 | 3 seed(s) |
| Fire / smoke (CCTV) | colorhist | ROC-AUC OOF / held-out | 0.681 | - | 3 seed(s) |
| Fire / smoke (zero-shot) | zeroshot | ROC-AUC OOF / held-out | 0.917 / 1.000 | 0/1 | 1 seed(s) |
| Fire / smoke (few-shot CLIP) | clip_probe | ROC-AUC OOF / held-out | 0.962 / 0.998 | 0/1 | 1 seed(s) |
| Fire META-FUSION (stack: fire_cnn + zeroshot + clip_probe + colorhist) | fire_meta_fusion | ROC-AUC OOF / held-out; stack − best single AUC | 0.951 / 0.999; -0.008 | 0/3 | REAL pairing; 3 seed(s) |
| Fake media | deepfake | ROC-AUC OOF / held-out | 0.961 / 0.450 | 0/3 | 3 seed(s) |
| Fire video (temporal validator) | video | false-alarm videos raw → validated | 0.893 → 0.853 | - | small n: quote counts |
| Landslide (physics, zero training) | caine_ratio | ROC-AUC spatial OOF | 0.758 | physics (no gate needed) | 184 real events, 101 blocks |
| GLOF (lake area → volume) | glof_physics | exponent b (95% CI) | 1.13 (0.71-1.50) | fit | n 21 |
| RL alarm policy (C_miss 100) | cql_learned vs physics_rule | return CQL / rule / oracle | -22.5 / -22.8 / -22.9 | deploy False | LCB -0.30; SIMULATOR |
| RL alarm policy (C_miss 1000) | cql_learned vs physics_rule | return CQL / rule / oracle | -200.9 / -200.0 / -200.0 | deploy False | LCB -10.28; SIMULATOR |
| RL alarm policy (C_miss 5000) | cql_learned vs physics_rule | return CQL / rule / oracle | -486.8 / -478.1 / -478.5 | deploy False | LCB -31.93; SIMULATOR |
| Landslide (Geo-PINN) | geo_pinn | ROC-AUC OOF / held-out | 0.716 | 0/1 | 1 seed(s) |
| Landslide META-FUSION (physics + rain, FM-1) | geo_fusion | ROC-AUC OOF (calibrated FM-1) | 0.779 | 0/3 | REAL pairing; 3 seed(s) |
| RL on fused alerts | offline_rl | gain vs rule (LCB) | +0.615 (+0.237) | deploy 3/3 |  |
| RL on REAL-paired fire meta-fusion | offline_rl_real | gain vs rule (LCB) | +1.076 (+0.773) | deploy 3/3 | 3 seed(s); OPE in-sample (optimistic) |
| RL HELD-OUT (block folds, true reward) | offline_rl_heldout | CQL gain vs rule / vs tuned rule (LCB) | +0.485 (-0.081) / -0.015 (-0.433) | deploy 0/3 | 3 seed(s); replaces the in-sample OPE number |
| Fire CROSS-MODAL (per-frame stack + temporal validator, FireSense) | crossmodal | video J (detect − FA): stack / clip_probe / fire_cnn | +0.467 / +0.320 / +0.008 | - | 3 seed(s); small n (49 videos) |
| Fire CONFUSER-AWARE retrain (leave-one-confuser-set-out) | stress | FA at equal recall 0.90: probe base → conf / stack base → conf; DeepFire AUC base → conf | 0.427 → 0.319 / 0.346 → 0.157; 0.998 → 0.997 | 3/3 | 3 seed(s) |
| Fusion (all experts) | p_zeroshot | value score (best rule) / FM-1 | 0.108 / 0.005 | - | SYNTHETIC pairing of real OOF scores |

## Headline

- Admitted learned experts: **1** (stress).
- Landslide physics with zero training: ROC-AUC **0.758** (184 real events, 101 blocks).
- RL: built, trained and tested online in the physics simulator at every cost ratio; the physics rule is within noise of the oracle, so the gate kept the rule (C_miss 100: deploy False; C_miss 1000: deploy False; C_miss 5000: deploy False).

Full tables: `RESULTS.md` (same folder).


## Build log

```
## 1. runs
- A: final (208063b0_out_A_final.zip)
- B: final (c443cff4_out_B_final (1).zip)
- C: final (dcb480c7_out_C_final.zip)
- F: final (60f8f99a_out_F_final.zip)
- S: final (b54dc175_out_S_final.zip)
- X: final (4c8ecc31_out_X_final (1).zip)
- missing: D (EO heads (Landslide4Sense, Sen1Floods11)), P (physics + geo meta-fusion + Geo-PINN)
## 2. fire meta-fusion
- zeroshot from B: OOF aligned
- zeroshot from F: OOF + held-out aligned
- zeroshot from X: OOF + held-out aligned
- clip_probe from B: OOF aligned
- clip_probe from F: OOF + held-out aligned
- clip_probe from X: OOF + held-out aligned
$ /usr/bin/python3 /workspaces/default/code/TRINETRA/trinetra/kaggle/fire_meta_fusion.py --fire /tmp/FIN/FINAL/_work/fire_meta_inputs/A/fire_s0_oof.npz --zeroshot /tmp/FIN/FINAL/_work/fire_meta_inputs/F/zeroshot_s0_oof.npz --clip /tmp/FIN/FINAL/_work/fire_meta_inputs/F/clip_probe_s0_oof.npz --out /tmp/FIN/FINAL/_work/fire_meta --seed 0 --colorhist /tmp/FIN/FINAL/_work/fire_meta_inputs/A/colorhist_s0_oof.npz
[time] 32s · exit 0
$ /usr/bin/python3 /workspaces/default/code/TRINETRA/trinetra/kaggle/fire_meta_fusion.py --fire /tmp/FIN/FINAL/_work/fire_meta_inputs/A/fire_s1_oof.npz --zeroshot /tmp/FIN/FINAL/_work/fire_meta_inputs/F/zeroshot_s0_oof.npz --clip /tmp/FIN/FINAL/_work/fire_meta_inputs/F/clip_probe_s0_oof.npz --out /tmp/FIN/FINAL/_work/fire_meta --seed 1 --colorhist /tmp/FIN/FINAL/_work/fire_meta_inputs/A/colorhist_s1_oof.npz
[time] 31s · exit 0
$ /usr/bin/python3 /workspaces/default/code/TRINETRA/trinetra/kaggle/fire_meta_fusion.py --fire /tmp/FIN/FINAL/_work/fire_meta_inputs/A/fire_s2_oof.npz --zeroshot /tmp/FIN/FINAL/_work/fire_meta_inputs/F/zeroshot_s0_oof.npz --clip /tmp/FIN/FINAL/_work/fire_meta_inputs/F/clip_probe_s0_oof.npz --out /tmp/FIN/FINAL/_work/fire_meta --seed 2 --colorhist /tmp/FIN/FINAL/_work/fire_meta_inputs/A/colorhist_s2_oof.npz
[time] 31s · exit 0
- fresh fire meta-fusion on attached runs: fire A seeds [0, 1, 2], zeroshot/clip_probe F/F
## 3. master merge
$ /usr/bin/python3 /workspaces/default/code/TRINETRA/trinetra/kaggle/merge_all_results.py --zips 208063b0_out_A_final.zip 4c8ecc31_out_X_final (1).zip 60f8f99a_out_F_final.zip b54dc175_out_S_final.zip c443cff4_out_B_final (1).zip dcb480c7_out_C_final.zip --out /tmp/FIN/FINAL/master --dirs /tmp/FIN/FINAL/_work/fire_meta
[time] 0s · exit 0
- dropped 66 model checkpoints / embedding caches from the bundle
## 4. figures
$ /usr/bin/python3 /workspaces/default/code/tools/make_figures.py --results /tmp/FIN/FINAL/_work/results --fig-out /tmp/FIN/FINAL/figures/results --phys-out /tmp/FIN/FINAL/figures/physics --x-zip 4c8ecc31_out_X_final (1).zip b54dc175_out_S_final.zip
[time] 3s · exit 0
   /tmp/FIN/FINAL/figures/results/R0_scorecard_all_auc.png
- extra graphs: 14 made, skipped none
- GRAPHS_EXPLAINED.md: 34 graphs
## 5. docs
## 6. index + zip
```
Built in 1.7 min.
