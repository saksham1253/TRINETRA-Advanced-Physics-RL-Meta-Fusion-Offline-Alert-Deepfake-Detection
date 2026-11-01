# 14 — RESULTS LOG (the ONLY source of numbers for docs, deck and demo)
Rule: add a row only from a `*_report.json` or log the team pasted. Old (original-dataset) and new (prototype-pack) results
are never mixed. The `pack` column says which.

| Run ID | Module | Dataset + manifest | Pack | Split | Seed | Metrics | admitted | HW | Date | Artifact |
|--------|--------|--------------------|------|-------|------|---------|----------|----|------|----------|
| ci-20261031-0804-na | code health | n/a | n/a | n/a | n/a | 128/128 unit tests OK; 6/6 CI gates PASS | n/a | CPU sandbox | 2026-10-31 | this session |
| demo-20261031-0804-0 | pipeline demo | SYNTHETIC hindcast | synthetic | spatial-CV | 0 | value score model -0.097 (noise) / 0.045 (informative) vs logistic 0.583 | False | CPU | 2026-10-31 | `python demo.py` |
| smoke-20261031-0833 | whole chain | SYNTHETIC images + zero-shot `--dry-run` | synthetic | group 3-fold | 0,1 | pipeline PASS only. **Numbers meaningless, never present** | n/a | CPU | 2026-10-31 | `kaggle/smoke_test_all.py` |
| geo_physics-20261031-s0 | landslide physics hindcast | NASA GLC India 29-33N 76-81E + POWER + Copernicus DEM (results/geo_large) | prototype (real) | spatial-block CV 0.1°, 101 blocks | 0 | AUC: Caine 0.758, dFS 0.750, geo gate 0.712, rain logit 0.781, physics logit 0.773, hybrid 0.780 (ECE 0.030); physics−rain −0.007 [−0.024, +0.011] | n/a | CPU | 2026-10-31 | results/geo_large |
| geo_physics-small-s0 | same, Chamoli tile 30-31N 79-80E | 112 rows, 28 events | prototype (real) | 15 blocks | 0 | physics−rain +0.095 [+0.052, +0.144]; geo gate 0.762 | n/a | CPU | 2026-10-31 | results/geo_small |
| glof_physics | GLOF relations | ICIMOD HMAGLOFDB v4 | real | n/a | n/a | V–A b 1.13 [0.71, 1.50] n 21 R² 0.72; Q–V d 0.54 [0.36, 0.79] n 31 R² 0.36 | n/a | CPU | 2026-10-31 | results/glof |
| rl_env_cmiss100-s0 | landslide RL | simulator + 360 real rain seasons | SIMULATOR | 300 eval episodes | 0 | hold −22.7, alarm −540.5, physics rule −22.8, oracle −22.9, CQL −22.5 (LCB −0.30) | not deployed | CPU | 2026-10-31 | results/rl_env |
| rl_env_cmiss1000-s0 | landslide RL | simulator + 360 real rain seasons | SIMULATOR | 300 eval episodes | 0 | hold −226.7, rule −200.0, oracle −200.0, CQL −200.9 (LCB −10.28) | not deployed | CPU | 2026-10-31 | results/rl_env |
| rl_env_cmiss5000-s0 | landslide RL | simulator + 360 real rain seasons | SIMULATOR | 300 eval episodes | 0 | hold −1133.3, alarm −540.5, rule −478.1, oracle −478.5, CQL −486.8 (LCB −31.93) | not deployed | CPU | 2026-10-31 | results/rl_env |
| geo_pinn-s0 | Geo-PINN | geo.npz (736 rows) | prototype (real) | spatial-block 5 folds | 0 | OOF AUC 0.716, PR-AUC 0.463, recall@FPR5% 0.228, ECE 0.099 | False | CPU | 2026-10-31 | results/geo_pinn |
| zeroshot-20261031-1712-0 | zero-shot CLIP ViT-B-32 laion2b, fire-or-smoke | D-Fire 3,000 (train+val), DeepFire held-out deduped, 5 stress sets | prototype (real) | group CV OOF n 2,546 + held-out n 1,039 | 0 (deterministic) | OOF AUC 0.891, recall@FPR5% 0.609, held-out AUC 0.999; ECE 0.240 → 0.178 cal; value score −0.051; FA@0.5: weather 62%, small flames 80%, scenes 27%, home-fire negatives 45% (n 33) | False | Kaggle T4×2 | 2026-10-31 | results/zeroshot_phase2 |
| zeroshot-20261031-1732-0 | same, final pack | D-Fire 4,000 | prototype (real) | group CV OOF n 3,410 + held-out n 1,023 | 0 (deterministic) | OOF AUC 0.889, recall@FPR5% 0.607, held-out AUC 0.999; ECE 0.236 → 0.173 cal; value score −0.042; same stress false-alarm rates | False | Kaggle T4×2 | 2026-10-31 | results/zeroshot_final |

Zero-shot reading: good ranking (AUC 0.889) but poor calibration; at p* = 0.048 every non-fire image alarms, so it loses to the baselines on value score (B-13) and is NOT admitted. It stays a low-trust fusion input (cap 0.5); confusers (candles, weather) are its main failure.

Vision models still running: fire CNN (A), media (C), EO (D), fusion (F).

**How real results get here:** each account runs `kaggle/run_hackathon.sh <stage>`, then account D runs `fuse`, which calls
`kaggle/collect_results.py`. Paste `out/results/RESULTS.md` + `results.json` to the AI (or copy them to `TRINETRA/results/`). The dashboard
reads them via `python docs/tools/build_dashboard_data.py`.

**Reading the metrics (B-13):** with C_FA=5 and C_miss=100, p* = 0.048. On a balanced curated set, a model whose non-fire images get
p≈0.2 still "alarms" on them, so the value score is ≈0 even when ROC-AUC is high. Present ROC-AUC / recall@FPR5% for discrimination,
ECE for calibration, and value score only with this explanation. It is honest, not a failure.
<!-- END -->
