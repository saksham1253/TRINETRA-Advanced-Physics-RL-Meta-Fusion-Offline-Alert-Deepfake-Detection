# 03 — CODE MAP (paths relative to `trinetra/src/trinetra/`; read from code 2026-10-31)
Status key: **works** = covered by passing tests here; **untested** = torch code, `py_compile` only per repo; **stub** = raises `MissingDependency`.

| Module | File | Key functions / classes | Inputs, then outputs | Config | Data format | Status |
|--------|------|------------------------|-----------------|--------|-------------|--------|
| Types | `common/types.py` | `ExpertOutput(p,source,u,c,r,cls,available)`, `Level` GREEN..RED, `Decision` | n/a | n/a | n/a | works |
| Config | `common/config.py` | `Config.get`, `p_star = C_FA/(C_FA+C_miss)` | gives p* = 5/105 = 0.0476 | `configs/default.json` | JSON | works |
| Fire physics A | `ws1a_firephys/established_ef.py` | `flame_height_heskestad`, `strouhal_puffing_frequency`, `plume_centerline_dT`, `byram_convection_number`, `graybody_*`, `beer_lambert_transmittance` | SI scalars, then scalars | n/a | n/a | works (coeff-verify tags) |
| Fire physics C | `ws1a_firephys/novel_nd.py` | ND-1..ND-7 | flags all OFF | `configs/firephys.json` | n/a | works, OFF |
| Fire gate | `ws1a_firephys/gate.py` | `fire_gate(FireInputs)` multiplies consistency by `clip(N_c/2,0.3,1)` | detector conf, Q, U, then `ExpertOutput(FIRE)` | firephys | n/a | works |
| Geo physics | `ws1b_geophys/{fs,iverson,fukuzono,caine,gate}.py` | FS, Iverson head, inverse-velocity, I-D threshold | rain, slope, then risk | n/a | n/a | works |
| NF formulas | `ws5_fusion_rl/nf.py` | `effective_weight = r*c*exp(-u/tau)`, NF-1..NF-4 | experts, then weights, U*, S | fusion.tau, lambda | n/a | works |
| Fusion | `ws5_fusion_rl/fusion_models.py` | `fm1_precision_weighted`, `fuse` dispatcher | experts, then `FusionResult(p,u_star,salience)` | `configs/fusion.json` (FM-1, pharaoh=false) | n/a | works |
| PHARAOH (C) | `ws5_fusion_rl/pharaoh.py` | power mean, `rho = 1 + kappa*D*S` clamped [1,8] | experts, then p | flag | n/a | works, OFF |
| GMF | `ws5_fusion_rl/gmf.py` | base + bounded residual head (JSON) | experts + head, then p | model=GMF | `gmf_head_numpy.json` | works |
| BLUE / hierarchy | `correlation.py`, `hierarchical.py` | `w ∝ Σ⁻¹1`, `fuse_group`, `decide_hierarchical` | grouped experts | n/a | n/a | works |
| Shield | `ws5_fusion_rl/shield.py` | `shield_floor(ShieldSignals)` (only RAISES) | FS<1, multi-node fire... | n/a | n/a | works |
| Decision | `ws5_fusion_rl/decision.py` | `decide`, `conformal_level` cuts p*, 4p*, 10p* | experts, then `Decision(level, uncertain, pred_set)` | calib.alpha | n/a | works |
| RL | `ws5_fusion_rl/rl.py` | `RuleBaselinePolicy(0.0476)`, `wis_value`, `ope_admission` | logs, then verdict | n/a | n/a | works; `OfflineRLPolicy` stub |
| Robust | `ws6_robust/{conformal,drift_monitor,missing_modality}.py` | split-CP, WCPS, ACI, Mondrian, CRC, PSI/CUSUM | scores, then sets/flags | n/a | n/a | works |
| Eval | `eval/*.py` | `spatial_block_kfold`, baselines, `value_score`, `real_win` (BCa), ECE, isotonic, `ReportGuard` | y, p, blocks, then report | cost | n/a | works |
| Anomaly (numpy) | `ws8_anomaly/__init__.py` | iForest-style + residual ensemble | windows, then score | n/a | arrays | works |
| CCTV | `ws4_cctv/__init__.py` | `EdgeDetector` (stub), `TemporalValidator` | per-frame conf, then confirmed event | n/a | n/a | validator works |
| Alert | `ws3_alert/{cap,dtn,siren,operator}.py` | CAP 1.2 XML, refuses without `APPROVED:` token | Decision, then CAP | alert.require_human_approval | XML | works |
| IoT | `ws7_iot/*.py` | LoRa codec IN865, `edge_screen` | readings, then bytes | n/a | n/a | works |
| Pipeline | `pipeline/{orchestrator,hindcast,demo}.py` | `run_fire_cycle`, `run_geo_cycle` | evidence, then Decision | all | n/a | works (synthetic) |
| Deep: fire | `deep/fire_cnn.py` | `FireSmokeNet` CNN, GRU, [fire,smoke]; Strouhal aux weight 0 | `images (N,T,C,H,W)` | n/a | `trinetra-fire/*.npz` | untested |
| Deep: anomaly | `deep/anomaly_deep.py` | TCN-AE + Deep-SVDD + forecast | `X (N,C,T)` | n/a | `trinetra-telemetry` | untested |
| Deep: deepfake | `deep/deepfake_net.py` | RGB+FFT two-stream, max_reliability 0.4 | `images (N,C,H,W)` | n/a | `trinetra-media` | untested |
| Deep: RL | `deep/offline_rl.py` | `CQLPolicy`, ACTIONS HOLD/WATCH/ALARM | `s,a,r,s_next,done,behavior_prob` | gamma=0 | `trinetra-rl-logs` | untested |
| Deep: fusion head | `deep/fusion_head.py` | `GMFHead`, `AttentionFusionHead`, `export_numpy` | base, dispersion, salience, y | cap 0.1 | `fusion_cache.npz` | untested |
| Deep: train | `deep/train.py` | DataParallel T4x2, AMP, `TemperatureScaler`, `admit_model` | n/a | n/a | n/a | untested |
| Deep: geo/EO | `deep/geo_pinn.py`, `deep/eo_encoder.py` | PINN, frozen EO encoder | geo npz / EO tiles | n/a | `trinetra-geo/-eo` | untested |

**New (this session, outside `src/`):** `data_adapters/build_npz.py` (folder / yolo / iot / check / subset),
`data_adapters/make_rl_logs.py`. Both were tested on synthetic files.

## Results chain (added 2026-10-31, all smoke-tested on CPU)
| File | Does | Output |
|------|------|--------|
| `deep/oof_utils.py` | OOF artifact, cross-fit temperature, ROC/PR-AUC, recall@FPR | `*_oof.npz` |
| `kaggle/train_classifier.py` (edited) | fire / deepfake CNN, `--seed --folds --test --target any` | `<m>_s<seed>_{oof.npz,report.json,fold*.pt}` |
| `kaggle/eval_zeroshot.py` | open_clip zero-shot, confuser prompts | `zeroshot_s0_*` |
| `kaggle/baseline_colorhist.py` | independent colour baseline | `colorhist_s*_*` |
| `kaggle/build_fusion_cache.py` | SYNTHETIC-PAIRING fusion; FM-1 vs PHARAOH vs median vs max; deepfake attack sim | `fusion_cache.npz`, `fusion_compare.{json,md}` |
| `kaggle/train_offline_rl.py` (edited) | CQL + honest OPE vs rule baseline | `offline_rl_s*_report.json` |
| `kaggle/collect_results.py` | all reports into one table | `results/RESULTS.md`, `results.json` |
| `kaggle/smoke_test_all.py`, `run_hackathon.sh` | whole chain on synthetic data / per-stage runner | PASS line |
<!-- END -->
