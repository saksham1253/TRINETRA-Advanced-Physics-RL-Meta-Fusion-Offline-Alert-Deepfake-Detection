# CODE CHANGE LOG
| Date | File | Why | Research reason | Test command | Status | Revert |
|------|------|-----|-----------------|--------------|--------|--------|
| 2026-10-31 | `data_adapters/build_npz.py` (NEW) | trainers need `.npz` contracts; no loader existed (G-02, G-04, G-07) | leakage-safe group splits (rule 14) | `python data_adapters/test_build_npz.py` | TESTED (synthetic) | delete file |
| 2026-10-31 | `data_adapters/test_build_npz.py` (NEW) | adapter smoke test | n/a | same | TESTED | delete |
| 2026-10-31 | `data_adapters/make_rl_logs.py` (NEW) | offline RL needs logs (G-03) | OPE positivity needs eps-exploration | see `07` §B | TESTED (synthetic + `ope_admission`) | delete |
| 2026-10-31 | `docs/tools/*.py` (NEW) | regenerate link CSVs | n/a | `python docs/tools/build_paper_links.py` | TESTED | delete |
| 2026-10-31 | `trinetra/src/trinetra/deep/oof_utils.py` (NEW) | OOF artifact + cross-fit temperature + AUC/recall (B-03, B-04, B-13) | Guo 2017 temperature scaling; leakage-safe cross-fit | `python kaggle/smoke_test_all.py` | TESTED | delete + revert trainers |
| 2026-10-31 | `kaggle/train_classifier.py` (EDIT) | mkdir, seed/folds/test args, batched predict, OOF save, calibrated metrics (B-01,03-06,08). **Output names now `<model>_s<seed>_*`** | rule 14 held-out | smoke test | TESTED (CPU) | `git checkout` original f8fee17 |
| 2026-10-31 | `kaggle/train_anomaly.py` (EDIT) | same + per-fold score normalization (B-07) | n/a | smoke (unit run) | TESTED (CPU) | git checkout |
| 2026-10-31 | `kaggle/train_offline_rl.py` (EDIT) | honest OPE vs RuleBaselinePolicy + bootstrap LCB (B-02); legacy verdict kept in report | 2311.14110 OPE feasibility | smoke | TESTED (CPU) | git checkout |
| 2026-10-31 | `kaggle/train_fusion_head.py`, `train_geo_pinn.py` (EDIT, 1 line) | mkdir (B-01) | n/a | run | TESTED | git checkout |
| 2026-10-31 | `src/trinetra/deep/train.py` (EDIT, 3 lines) | drop non-tensors before DataParallel (B-09) | n/a | CPU path tested; DP UNTESTED | partial | git checkout |
| 2026-10-31 | `src/trinetra/ws5_fusion_rl/adapters.py` (EDIT, additive) | new sources zeroshot/iot/colorhist + `authenticity_adjusted_reliability` (B-10, B-11) | D-011 low-weight zero-shot | 128 unit tests OK | TESTED | git checkout |
| 2026-10-31 | `kaggle/eval_zeroshot.py`, `baseline_colorhist.py`, `build_fusion_cache.py`, `collect_results.py`, `smoke_test_all.py`, `run_hackathon.sh` (NEW) | complete the chain to results | docs/08 experiment | smoke | TESTED (zero-shot with --dry-run only) | delete |
| 2026-10-31 | `data_adapters/build_npz.py` (EDIT) iot standardize; `make_rl_logs.py` mkdir | B-14, B-16 | n/a | adapter tests | TESTED | git |
| 2026-10-31 | `data_adapters/build_npz.py` (EDIT, new commands) | `video`, `dedupe`, `--classes auto`, `--seq-bucket`, aug grouping, path-style `--map`, `ahash` stored (B-17..B-22) | rule 14 leakage | `python data_adapters/test_build_npz.py` | TESTED | git |
| 2026-10-31 | `kaggle/train_classifier.py`, `eval_zeroshot.py` (EDIT) | `--stress` false-alarm sets | nuisance stress (prompt 8E f) | smoke | TESTED | git |
| 2026-10-31 | `kaggle/eval_video.py` (NEW) | raw vs TemporalValidator on FireSense | ws4_cctv design | smoke (synthetic AVI) | TESTED | delete |
| 2026-10-31 | `kaggle/run_hackathon.sh` (EDIT) | verified folder names, new datasets, dedupe, `video` stage | docs/09d | `bash -n` + smoke | build stage UNTESTED on real data | git |
| 2026-10-31 | `data_adapters/build_geo.py` (NEW) | GLC + POWER + Copernicus DEM -> physics table + Geo-PINN npz (B-23, B-27, B-28) | case-control design; back-analysis | real run (736 rows) | TESTED | delete |
| 2026-10-31 | `data_adapters/build_eo.py` (NEW) | L4S / Sen1Floods11 / Hephaestus -> EO npz | group by hash / event / frameID | synthetic h5/tif/png | TESTED | delete |
| 2026-10-31 | `kaggle/geo_physics_hindcast.py`, `glof_physics_check.py`, `rl_env_eval.py` (NEW) | real-data physics + GLOF + RL results | docs/04 | real runs | TESTED | delete |
| 2026-10-31 | `src/trinetra/ws5_fusion_rl/env_landslide.py` (NEW) | physics RL environment (Iverson + FS + real rain) | Iverson 2000; cost-loss | real rain seasons | TESTED | delete |
| 2026-10-31 | `kaggle/train_classifier.py` (EDIT) | EO channels/backbone flags (B-26) | n/a | 14-band run | TESTED | git |
| 2026-10-31 | `kaggle/train_geo_pinn.py` (EDIT) | OOF save + seed (B-29) | n/a | real run | TESTED | git |
| 2026-10-31 | `kaggle/collect_results.py`, `run_hackathon.sh` (EDIT) | geo/GLOF/RL sections; `geo` and `eo` stages | n/a | geo stage run | TESTED (geo), eo UNTESTED on real data | git |
| 2026-10-31 | `run_hackathon.sh`, `build_eo.py` (EDIT) | small EO caps; reserve Bolivia and sample events round-robin | prototype-data + leakage rules | `bash -n`; selector smoke test | TESTED (selector), real EO UNTESTED | git |
| 2026-10-31 | `profile_tables.py`, `build_tpd_index.py`, `test_tpd.py` (NEW) | deterministic TPD profiling, provenance index and checksum | conversion honesty / TPD-0.1 | `python data_adapters/test_tpd.py`; `sha256sum -c data_manifests/tpd_index.csv.sha256` | TESTED | delete generated index + scripts |
| 2026-10-31 | `stage_kaggle_archives.py`, `prepare_kaggle_training_data.sh` (NEW) | team pack may contain nested ZIP/TAR files and unknown mount names; inventory IMERG/LULC too | adapt data to code; reject archive traversal/links | `python data_adapters/test_kaggle_prep.py`; `bash -n` | archive/discovery TESTED synthetic | delete files |
| 2026-10-31 | `validate_ready_pack.py` (NEW) | block bad NPZ shapes, non-finite values and group leakage before GPU use | conversion F7 | compile check; run inside prepare script | runtime PENDING KAGGLE (local NumPy absent) | delete file |
| 2026-10-31 | `run_hackathon.sh` (EDIT) | accept uploaded GLC/GLOF CSV; train EO directly from shared NPZs with multi-seed `eo-train` | avoid rebuilding raw EO on every account | `bash -n`; fake-runner route test for seeds 0,1 | TESTED routing; GPU UNTESTED | revert hunk |
| 2026-10-31 | `run_hackathon.sh` (EDIT) | `build`: every dataset optional (log + continue), held-out dedupe only if D-Fire exists, `CIFAKE_N`; `fire`/`zeroshot`: DeepFire test optional | team pack layout not fully known; one missing set must not kill the run | fake-runner: fire without DeepFire, build with no data exits 0 | TESTED routing | revert hunk |
| 2026-10-31 | `TRINETRA_kaggle_runner.ipynb`, `exports/trinetra_code.zip` (NEW) | one notebook per account (ACCOUNT/PHASE switches) + code package for Kaggle | parallel 4-account plan | cells compile | runtime PENDING KAGGLE | delete |
| 2026-10-31 | `run_hackathon.sh` (EDIT) | new `physics` stage (unit/golden tests + geo); `geo` loops `GEO_SEEDS` for hindcast + Geo-PINN, `PINN_EPOCHS` | multi-seed physics results | `bash -n` | runtime PENDING KAGGLE | revert hunk |
After all edits: `run_tests.py` 128/128 OK, `ci_gates.py` 6/6 PASS, `smoke_test_all.py` PASS (2026-10-31).
<!-- END -->
