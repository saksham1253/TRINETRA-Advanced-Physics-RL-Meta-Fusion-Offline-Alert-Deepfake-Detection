# TRINETRA — MASTER RESULTS (all accounts merged)

Every number is OUR RESULT on the prototype pack (not comparable to full-benchmark papers). Admitted = beat climatology and logistic baselines on cost-weighted value with a 95% CI (Rule 16).

## Runs used (one phase per account)

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
