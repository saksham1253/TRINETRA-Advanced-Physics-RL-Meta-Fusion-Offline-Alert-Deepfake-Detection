# CH11 — MASTER TABLES (read from code and configs, 2026-10-31). Paths are relative to `trinetra/src/trinetra/` unless they start with `kaggle/`, `data_adapters/` or `configs/`.

## (a) THRESHOLDS
| Name | Value | Where | Controls | Kam karoge | Zyada karoge | Evidence |
|---|---|---|---|---|---|---|
| C_FA, C_miss | 5, 100 | configs/default.json | cost of false alarm / miss | p* rises, fewer alarms | p* falls, more alarms | RL sweep C_miss 100/1000/5000 (results/rl_env) |
| p* | 0.0476 | common/config.p_star | first alarm cut (YELLOW) | more alarms | fewer alarms | derived from costs |
| Level cuts | p*, 4p*, 10p* | ws5_fusion_rl/decision.conformal_level | YELLOW / ORANGE / RED | earlier escalation | later | ad hoc (GAP G-12); CRC can replace |
| uncertain_threshold | U* > 0.6 | decision.decide | "needs human review" | more abstain | fewer | design |
| Reliability bands | U* < 0.2 / 0.4 / 0.6 | decision._reliability_from_uncertainty | HIGH/MED/LOW/UNRELIABLE | — | — | design |
| Pred-set widening | U* 0.2, 0.5 | decision._pred_set | width of level set | — | — | design |
| Shield FS | FS < 1 → ORANGE | ws5_fusion_rl/shield.py | raise-only floor | — | — | needs calibrated FS (B-23) |
| Shield tilt | > 5 °/day and ≥ 2 nodes → RED | shield.py | floor | — | — | design |
| Shield rain | 24 h > 150 mm and high susceptibility → ORANGE | shield.py | floor | — | — | design |
| Shield GLOF | lake drop + downstream jump → RED | shield.py | floor | — | — | design |
| Caine a, b | 14, 0.39 | ws1b_geophys/gate.GeoInputs | I–D line | more exceedance | less | real events AUC 0.758 (results/geo_large) |
| geo_gate k_fs | 4.0 | ws1b_geophys/gate.geo_gate | FS → p sigmoid steepness | softer | sharper | design |
| p_caine | clip(ratio − 0.5, 0, 1) | gate.geo_gate | Caine soft term | — | — | design |
| Fukuzono lead | 48 h | gate.geo_gate | proximity term | — | — | design |
| Fire Byram consistency | clip(N_c / 2, 0.3, 1) | ws1a_firephys/gate.fire_gate | down-weight wind-dominated | — | — | design |
| TemporalValidator | window 5, min 3, thr 0.5 | ws4_cctv/__init__.py | persistence check | more false alarms | slower detection | video eval pending |
| eval_video thr | 0.5 (calibrated prob) | kaggle/eval_video.py | frame alarm | — | — | pending |
| Drift PSI | > 0.2 | ws6_robust/drift_monitor.check_drift | drift flag | more flags | fewer | standard rule of thumb |
| CUSUM | k = 0.5, h = 5.0 | drift_monitor.cusum_update | drift flag | — | — | design |
| Conformal α | 0.1 | ws6_robust/conformal.py, configs calib.alpha | 90% coverage target | wider sets | narrower | — |
| ACI γ | 0.02 | conformal.AdaptiveConformal | adaptation speed | slower | faster, noisier | — |
| CRC target risk | 0.05 | conformal.conformal_risk_threshold | miss-risk bound | — | — | — |
| RL deploy gate | paired 95% LCB > 0 | kaggle/train_offline_rl.py, rl_env_eval.py | deploy learned policy | — | — | B-02, B-25 |
| Admission gate | beat climatology + logistic, block-bootstrap CI | deep/train.admit_model | "admitted" | — | — | eval/real_win (BCa) |
| Dedupe | aHash Hamming ≤ 4 (cross-dataset), ≤ 6 (grouping) | data_adapters/build_npz.py | leakage control | more duplicates kept | over-grouping | design |
| Seq bucket | 50 frames | run_hackathon.sh build | consecutive-frame groups | — | — | B-19 |

## (b) HYPERPARAMETERS
| Module | Parameter | Value | Where |
|---|---|---|---|
| All deep trainers | lr, weight decay, grad clip | 3e-4, 1e-4, 1.0 | deep/train.TrainConfig |
| | batch per GPU, epochs, folds, AMP | 64, 20, 5, on (CUDA) | TrainConfig / CLI |
| | multi-GPU | DataParallel, LR scaled ×n_gpus | TrainConfig.effective_lr |
| Fire CNN | base channels, GRU hidden, classes, Strouhal weight | 32, 128, 2, 0.0 (Class C OFF) | deep/fire_cnn.FireNetConfig |
| Deepfake | base, max reliability | 32, 0.4 | deep/deepfake_net.DeepfakeConfig |
| EO head | backbone, pretrained, freeze, head | resnet18 (CLI), 1, 1, MLP(256, 64) | kaggle/train_classifier.py, deep/eo_encoder.EOConfig |
| Zero-shot | model, weights, templates, trust cap | ViT-B-32, laion2b_s34b_b79k, 6, 0.5 | kaggle/eval_zeroshot.py, adapters._POLICY |
| Geo-PINN | static dims, hidden, physics/fs/data weights | 6, (128,128,128), 1.0/0.5/1.0 | deep/geo_pinn.GeoPINNConfig |
| | D0 (scaled), β | 4.32 m²/day, 40° | run_hackathon.sh geo (B-28) |
| Anomaly (deep) | n_feat, channels, emb, weights | data, (32,32,64), 32, 1/1/0.5 | deep/anomaly_deep.AnomalyConfig |
| CQL | hidden, γ, cql_α, τ | (256,256), 0 (bandit) / 0.95 (env), 1.0, 0.005 | deep/offline_rl.CQLConfig, rl_env_eval.py |
| RL env eval | episodes, log episodes, eps, epochs, batch | 300, 400, 0.3, 30, 512 | kaggle/rl_env_eval.py |
| Fusion head | residual cap, epochs | 0.1, 300 | kaggle/train_fusion_head.py |
| Fusion cache | n per seed, pos rate, seeds, fake frac | 5000, 0.2, 0..4, 0.1 (run_hackathon) | kaggle/build_fusion_cache.py |
| Hindcast | cell, folds | 0.1°, 5 | kaggle/geo_physics_hindcast.py |

## (c) FORMULA PARAMETERS
| Formula | Constant | Value | Source |
|---|---|---|---|
| FM-1 weight | τ | 0.5 | configs/fusion.json |
| NF-3 | λ | 0.3 | configs/fusion.json |
| NF-1 | σ | 0.25 | ws5_fusion_rl/nf.nf1_consistency |
| NF-2 | λ forget, r_min, drift penalty | 0.9, 0.1, 0.5 | nf.nf2_reliability |
| PHARAOH | κ, ρ clamp | 2, [1, 8] | ws5_fusion_rl/pharaoh.py (OFF) |
| Source trust (default, cap) | geo_phys 1.0/1.0 · fire_cnn 0.8/0.95 · cctv 0.75/0.9 · eo 0.7/0.9 · anomaly 0.7/0.9 · zeroshot 0.4/0.5 · colorhist 0.5/0.6 · deepfake 0.3/0.4 | ws5_fusion_rl/adapters._POLICY |
| Infinite slope | φ′, γ, z | 32°, 19 kN/m³, 2 m (ASSUMPTION) | data_adapters/build_geo.SOIL |
| Back-analysis | FS_dry target | 1.2 (ASSUMPTION) | build_geo.FS_DRY_TARGET |
| Iverson | K_z, D0, ψ0 | 1e-5 m/s, 5e-5 m²/s, 0 m (ASSUMPTION) | build_geo.SOIL |
| Heskestad | 0.235, 1.02 | coeff-verify | ws1a_firephys/established_ef.py |
| Strouhal puffing | 1.5 | coeff-verify | established_ef.py |
| RL hazard | β (fitted), α (calibrated) | 24.3 on ΔFS; α so a slope fails 30%/season | results/rl_env (fit), `--season-fail` ASSUMPTION |
| GLOF fits | exponents | V–A b 1.13, Q–V d 0.54 | results/glof (Class B) |

## (d) FORMULA INDEX
| ID | Formula | Class | Chapter | Code | Validation |
|---|---|---|---|---|---|
| F1 | Infinite-slope FS | A | CH05 | ws1b_geophys/fs.py | used in real hindcast |
| F2 | Iverson multipulse ψ, D1 = D0/cos²β | A | CH05 | iverson.py | used in real hindcast |
| F3 | Caine I_thr = aD^-b | A | CH05 | caine.py | AUC 0.758 real (C3) |
| F4 | Fukuzono 1/v | A | CH05 | fukuzono.py | not tested on data |
| F5 | Heskestad, Strouhal, Byram, gray-body, Beer-Lambert | A | CH05 | established_ef.py | not tested on data |
| F6 | ΔFS (c′-free) | B | CH06 | build_geo.py | AUC 0.750 real (C3) |
| F7 | Back-analysed c′ | B | CH06 | build_geo.backcalc_cohesion | geo gate AUC 0.712 real |
| F8 | GLOF V = aA^b, Qp = cV^d | B (fit) | CH06 | kaggle/glof_physics_check.py | fits with CI (results/glof) |
| F9 | FM-1, effective weight | B | CH08 | fusion_models.py, nf.py | unit tests |
| F10 | NF-1..NF-4, U* | B | CH08 | nf.py | unit tests |
| F11 | PHARAOH power mean | C | CH06 | pharaoh.py | OFF; power-mean inequality |
| F12 | p* cost-loss | A | CH08 | config.p_star | — |
| F13 | Temperature scaling, cross-fit | A | CH08 | deep/oof_utils.py | ECE on synthetic; real pending |
| F14 | RL hazard σ(α + βΔFS) | B/ASSUMPTION | CH09 | env_landslide.py | β fitted on real events |
| F15 | ND-1..ND-7 flicker etc. | C | CH06 | ws1a_firephys/novel_nd.py | OFF |

**Discrepancies found:** Caine global constant in docs is 14.82 (from memory) vs 14 in code. RL baseline threshold 0.0476 = p* (consistent).
Level cuts are ad hoc (G-12). No acceptance targets are found in the repo.
<!-- END -->
