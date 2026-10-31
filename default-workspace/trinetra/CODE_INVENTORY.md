# TRINETRA — Code Inventory (handoff)

What has been built so far, file by file. Two execution tiers:
- **NUMPY CORE** — runs anywhere (edge/gateway/CI), stdlib + numpy only. 128 unit tests pass, 6 CI gates pass.
- **DEEP (torch)** — trains on Kaggle GPU; verified here by `py_compile` only (no torch in the authoring
  sandbox). Produces calibrated probabilities that feed the numpy core; never issues alerts.

Totals: **src ≈ 3362 LOC**, **tests ≈ 917 LOC (128 tests)**, **kaggle ≈ 316 LOC**.

Everything is advisory and honesty-gated: R16 (no performance claim before the eval admission gate), R19
(human-in-the-loop, fail-safe to uncertain, shield only raises), R20 (Class A/B/C labels; Class-C novel
terms default OFF with an A/B fallback), R21 (novelty = search claim only).

---

## 1. common/ — contracts & infrastructure (numpy core)
| File | LOC | What it does |
|------|----:|--------------|
| `common/types.py` | 118 | Canonical dataclasses/enums: `Level`, `Hazard`, `PhysicsClass` (A/B/C/DATA/ADVISORY), `ExpertOutput` (p,u,c,r,cls,available), `Evidence`, `Decision`, `ConformalResult`, `ShieldResult`. Every artifact carries a physics class + trust marker. |
| `common/config.py` | 61 | Layered JSON config (`configs/*.json`), `p_star = C_FA/(C_FA+C_miss)`, dotted-key `get`. |
| `common/security.py` | 32 | Endpoint allow-list (C6), no-raw-video-egress guard (C7), approval-token checks. |
| `common/tracing.py` / `exceptions.py` | 16/16 | Trace ids; `SafetyViolation`, `MissingDependency`, etc. |

## 2. ws1b_geophys/ — landslide/flood/GLOF physics (Class A/B, numpy core)
| File | LOC | What it does |
|------|----:|--------------|
| `fs.py` | 34 | Infinite-slope Factor of Safety; saturated limit; pore-pressure from head. Golden-tested monotonicities. |
| `iverson.py` | 68 | Iverson (2000) transient pressure head; **slope enters ONLY via `D1=D0/cos²β`** (bug-guard). **NEW:** `transient_head_multipulse` — linear **superposition over a piecewise-constant rainfall history** (finite-pulse recovery `R(t)−R(t−T)`). |
| `fukuzono.py` | 71 | Inverse-velocity failure-time (α=2). **NEW:** recency-weighted WLS + **prediction interval on t_f** (delta method) so the forecast carries uncertainty. |
| `caine.py` | 16 | Caine intensity–duration rainfall threshold (a=14, b=0.39). |
| `gate.py` | 71 | Combines FS/Iverson/Fukuzono/Caine into a geo risk gate (noisy-OR style), with class labels. |

## 3. ws1a_firephys/ — fire physics (numpy core)
| File | LOC | What it does |
|------|----:|--------------|
| `established_ef.py` | 41 | Heskestad flame height, Byram fireline intensity, gray-body radiation (Class A). |
| `novel_nd.py` | 62 | Novel ND flicker/Strouhal (Class C) — **default OFF**, uncertainty grows with smoke. |
| `gate.py` | 64 | Fire risk gate; Class-C contributions flag-gated with A/B fallback. |

## 4. ws5_fusion_rl/ — fusion, hierarchy, shield, decision, RL (numpy core)
| File | LOC | What it does |
|------|----:|--------------|
| `nf.py` | 52 | NF-1 physics-consistency, NF-2 drift-decayed reliability, NF-3 conflict→uncertainty, NF-4 salience, effective weights. |
| `pharaoh.py` | 38 | PHARAOH power-mean operator (Class C), `ρ=1+κ·DS`; opt-in only. |
| `fusion_models.py` | 62 | FM-1 precision-weighted mean (default/fallback) + dispatcher (FM-1 / GMF / PHARAOH), reports `used_classC`. |
| `gmf.py` | 67 | Gated-mixture fusion with **bounded residual** (hard-clipped ±cap); `load_numpy_head` loads a trained head from JSON for offline use. |
| `correlation.py` | 67 | **NEW:** correlation-aware **BLUE/GLS** weights (`w*∝Σ⁻¹1`) so redundant sensors don't double-count; non-negative-clipped for safety. |
| `hierarchical.py` | 88 | **NEW:** two-layer fusion — `fuse_group` (intra-workstream → one expert, propagates u/c/r/class) + `decide_hierarchical` (feeds the single decision fn). Optional per-group redundancy. |
| `adapters.py` | 35 | **NEW:** torch-free `deep_expert(source, prob, …)` → `ExpertOutput` with correct Class + reliability cap (deepfake hard-capped 0.4). |
| `shield.py` | 37 | Monotone safety floor (can only RAISE level); FS<1 etc. force a minimum level. |
| `decision.py` | 83 | **THE single decision function**: `level = max(conformal_level(risk,p*), shield_floor)`. **NEW:** accepts calibrated `level_thresholds` (from Conformal Risk Control). |
| `rl.py` | 62 | `RuleBaselinePolicy`, `OfflineRLPolicy`, WIS off-policy value, `ope_admission` (positivity + ESS + value≥baseline). |

## 5. ws6_robust/ — calibration under shift & drift (numpy core)
| File | LOC | What it does |
|------|----:|--------------|
| `conformal.py` | 124 | Split-CP + WCPS (covariate shift). **NEW:** `AdaptiveConformal` (ACI, long-run coverage under drift), `MondrianConformal` (per-hazard coverage), `conformal_risk_threshold` (RCPS/CRC miss-risk bound). |
| `drift_monitor.py` | 38 | PSI + CUSUM drift detection; voids CP guarantees when drift fires. |
| `missing_modality.py` | 23 | Graceful degradation (C8): absent modality → unavailable + others more uncertain. |

## 6. eval/ — admission harness (numpy core, the M0 foundation)
| File | LOC | What it does |
|------|----:|--------------|
| `splits.py` | 34 | Spatial-block k-fold, temporal split, anti-time-leak assertion (G6). |
| `value_score.py` | 39 | Cost-loss value score, `p*`, alarms-from-prob, climatology cost. |
| `baselines.py` | 44 | Mandatory baselines: climatology, persistence, physics-rule, `LogisticNumpy`. |
| `real_win.py` | 46 | Paired block-bootstrap "real win". **NEW:** BCa interval default. |
| `_stats.py` | 68 | **NEW:** `norm_cdf/ppf` (Acklam), `bca_interval`, `stationary_bootstrap_indices`. |
| `calibration.py` | 95 | **NEW:** ECE/MCE, reliability curve, Brier decomposition, `IsotonicCalibrator` (PAV), `PlattCalibrator`. |
| `report.py` | 50 | `ReportGuard` — refuses to emit a headline metric unless spatial-CV real-win over all baselines passes (R16). |

## 7. Other workstreams (numpy core)
| File | LOC | What it does |
|------|----:|--------------|
| `ws8_anomaly/__init__.py` | 67 | Lightweight isolation-forest-style + residual anomaly ensemble (always-on fallback). |
| `ws4_cctv/__init__.py` | 40 | CCTV detector interface + confidence→ExpertOutput mapping. |
| `ws1b_eo/__init__.py` | 28 | EO change/hazard interface. |
| `ws2_deepfake/__init__.py` | 31 | Authenticity interface (low trust). |
| `ws7_iot/*` | 11–65 | LoRa codec (IN865–867), `sensor_reading`, edge-screen pre-filter (≤₹2000 node). |
| `ws3_alert/*` | 9–67 | CAP builder (refuses without `APPROVED:` token), operator console, siren, DTN store-and-forward. |

## 8. pipeline/ — orchestration (numpy core)
| File | LOC | What it does |
|------|----:|--------------|
| `orchestrator.py` | 52 | Evidence → per-workstream experts → fusion → single decision. |
| `hindcast.py` | 32 | Replay historical evidence for backtesting. |
| `demo.py` | 75 | End-to-end advisory demo (`python demo.py`). |

## 9. deep/ — trainable torch models (Kaggle; py_compile-verified)
| File | LOC | What it does |
|------|----:|--------------|
| `layers.py` | 66 | MLP, causal `Chomp1d`/`TemporalBlock`/`TCN`, ConvBNAct. |
| `losses.py` | 46 | Richards/Iverson PDE residual, differentiable FS, Strouhal consistency, Deep-SVDD, cost-sensitive BCE, Brier. |
| `geo_pinn.py` | 67 | **Model 1** physics-informed NN (autograd PDE residual, FS head). Class B. |
| `fire_cnn.py` | 58 | **Model 2** CNN→GRU fire/smoke + Strouhal aux (Class-C OFF). |
| `eo_encoder.py` | 50 | **Model 3** frozen EO foundation encoder + head. |
| `anomaly_deep.py` | 68 | **Model 4** TCN autoencoder + Deep-SVDD + forecast residual. |
| `deepfake_net.py` | 49 | **Model 5** two-stream (RGB+FFT) authenticity, low trust. |
| `offline_rl.py` | 67 | **Model 6** Conservative Q-Learning policy (shielded, OPE-gated). |
| `fusion_head.py` | 99 | `GMFHead` (bounded residual) + **NEW `AttentionFusionHead`** (attention over workstream experts; convex base + bounded residual) + numpy export bridges. |
| `datamodules.py` | 87 | Kaggle dataset paths + Dataset classes + spatial-block assignment. |
| `train.py` | ~190 | Seeds, **multi-GPU (DataParallel, T4×2)** with GPU-scaled batch + linear-LR scaling + safe `drop_last`, cuDNN/AMP perf setup, spatial-CV, temperature calibration, `admit_model` (eval gate **+ ECE/MCE/Brier calibration diagnostics**). |
| `ddp.py` | 70 | **DistributedDataParallel launcher** (mp.spawn, DistributedSampler, rank-0 save) — max-throughput multi-GPU path. |

## 10. kaggle/ — training kernels (run on Kaggle)
`README.md` + `train_geo_pinn.py`, `train_classifier.py` (fire/eo/deepfake), `train_anomaly.py`,
`train_offline_rl.py` (OPE gate), `train_fusion_head.py` (+numpy export). `requirements-deep.txt` pins torch
2.3.1 etc.

## 11. scripts/, configs/, firmware/, tests/
- `scripts/ci_gates.py` (6 honesty/safety gates), `scripts/bom_price_check.py` (both nodes ≤₹2000).
- `configs/default.json`, `firephys.json`, `fusion.json`.
- `firmware/FIRMWARE_SPEC.md`.
- `tests/` — 128 tests: physics golden (FS/Iverson/multipulse/Fukuzono-CI/Caine/fire), fusion
  (FM/GMF/adapters/**hierarchical+correlation**), robust (CP/**ACI/Mondrian/CRC**/drift/missing), eval
  (value-score/real-win/**calibration/stats**), decision, iot, alert, interfaces.
- `MODEL_CARDS.md` — per-model honesty cards.

---

## How to run
```bash
python run_tests.py          # 128 unit tests (numpy core)
python scripts/ci_gates.py   # 6 honesty/safety gates
python demo.py               # end-to-end advisory demo
# deep models: see kaggle/README.md (train on Kaggle GPU, copy artifacts back)
```

## What is NOT done (honest)
- No model is trained yet → **no accuracy/skill claim is valid** until datasets are collected and the eval
  admission gate passes on spatial-CV (R16). Dataset collection is the user's team's next task.
- Deep torch code is `py_compile`-clean but not runtime-executed here; shape/CUDA issues will surface on
  Kaggle and need iteration.
