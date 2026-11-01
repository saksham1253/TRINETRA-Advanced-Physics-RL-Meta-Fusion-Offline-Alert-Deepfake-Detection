# NUMBERS REGISTER (every number on the deck). Source of truth: `src/deck/numbers.json`.

| id | value | meaning | source | label | slide |
|---|---|---|---|---|---|
| uk_dm_5yr | ₹5,178 cr | Uttarakhand disaster-management allocation, 2021–26 | `TRINETRA/results/uttarakhand_cost_benefit.json` | OFFICIAL | 1 |
| uk_dm_annual | ₹1,035.6 cr/yr | annual average disaster-management allocation | `TRINETRA/results/uttarakhand_cost_benefit.json` | DERIVED | 1 |
| uk_rr_annual | ₹724.9 cr/yr | response/relief + recovery/reconstruction comparison envelope | `TRINETRA/results/uttarakhand_cost_benefit.json` | DERIVED | 1 |
| uk_network_cost | ₹1.5–3.0 cr | first-year priority network: 500 slope nodes, 50 rain stations, 95 gateways, redundant servers/integration | `TRINETRA/results/uttarakhand_cost_benefit.json` | PLANNING | 1 |
| uk_avoidable_low | ₹3.6 cr/yr | potential gross avoided public burden, low scenario | `TRINETRA/results/uttarakhand_cost_benefit.json` | SCENARIO | 1 |
| uk_avoidable_base | ₹18.8 cr/yr | potential gross avoided public burden, base scenario | `TRINETRA/results/uttarakhand_cost_benefit.json` | SCENARIO | 1 |
| uk_2013_cost | ₹3,964.1 cr | Uttarakhand 2013 disaster damage and recovery needs (JRDNA) | `TRINETRA/results/uttarakhand_cost_benefit.json` | OFFICIAL | 1 |
| uk_2013_roads | ₹2,710.3 cr | roads and bridges in Uttarakhand 2013 JRDNA | `TRINETRA/results/uttarakhand_cost_benefit.json` | OFFICIAL | 1 |
| tests | 128/128 | unit tests passing after all fixes | `trinetra/run_tests.py` | OUR RESULT | 7 |
| gates | 6/6 | honesty/safety CI gates | `trinetra/scripts/ci_gates.py` | OUR RESULT | 7 |
| bugs | 31 | code/data bugs found by running the code and fixed | `docs/BUG_STATUS.md` | OUR RESULT | 7 |
| datasets | 54 | datasets in the prototype pack (link-checked) | `docs/09b_dataset_links.csv` | OUR RESULT | 1, 4, 7 |
| papers | 797 | unique papers indexed; 157 links checked, 8 title mismatches | `docs/11_paper_links.csv` | OUR RESULT | 1, 7 |
| geo_events | 184 | real rain-triggered landslide events (NASA GLC, 29-33N 76-81E) | `results/geo_large/geo_meta.json` | OUR RESULT | 1, 3, 4, 7 |
| geo_rows | 736 | events + 552 same-site control monsoon days; 101 spatial blocks | `results/geo_large` | OUR RESULT | 3, 4 |
| auc_caine | 0.758 | ROC-AUC, Caine I-D physics, no fitting (spatial-block OOF) | `results/geo_large/geo_physics_s0_report.json` | OUR RESULT | 3, 7 |
| auc_dfs | 0.750 | ROC-AUC, dFS Iverson+FS physics, no fitting | `results/geo_large` | OUR RESULT | 3 |
| auc_gate | 0.712 | ROC-AUC, repo geo gate with back-analysed c' | `results/geo_large` | OUR RESULT | 3 |
| auc_rain | 0.781 | ROC-AUC, logistic on rain (data baseline) | `results/geo_large` | OUR RESULT | 3, 7 |
| auc_phys_logit | 0.773 | ROC-AUC, logistic on physics features | `results/geo_large` | OUR RESULT | 3 |
| auc_hybrid | 0.780 | ROC-AUC, logistic rain + physics | `results/geo_large` | OUR RESULT | 3, 7 |
| ece_hybrid | 0.030 | ECE of the hybrid model (OOF) | `results/geo_large` | OUR RESULT | 4, 7 |
| phys_minus_rain_L | -0.007 [-0.024, +0.011] | AUC physics-minus-rain, 95% block-bootstrap CI (large set): no proven gain | `results/geo_large` | OUR RESULT | 3, 7 |
| phys_minus_rain_S | +0.095 [+0.052, +0.144] | same on the small Chamoli tile (112 rows, 15 blocks): did not survive more data | `results/geo_small/geo_physics_s0_report.json` | OUR RESULT | 3, 7 |
| glof_av | b = 1.13 [0.71, 1.50] | GLOF V = a*A^b, n = 21, R2(log) 0.72 | `results/glof/glof_physics_report.json` | OUR RESULT | 3 |
| glof_vq | d = 0.54 [0.36, 0.79] | GLOF Qp = c*V^d, n = 31, R2(log) 0.36 | `results/glof/glof_physics_report.json` | OUR RESULT | 3 |
| rl_seasons | 360 | real monsoon rain seasons in the RL simulator (NASA POWER) | `results/rl_env/rl_env_cmiss100_s0_report.json` | OUR RESULT | 5 |
| rl_beta | 24.3 | hazard slope on dFS fitted on the real events | `results/rl_env` | OUR RESULT | 5 |
| rl100_alarm | -540.5 | return, always-alarm (C_miss = 100) | `results/rl_env` | OUR RESULT (SIMULATOR) | 5 |
| rl100_rule | -22.8 | return, physics rule (C_miss = 100) | `results/rl_env` | OUR RESULT (SIMULATOR) | 5 |
| rl100_cql | -22.5 | return, CQL shielded; 95% LCB of gain -0.30, so not deployed | `results/rl_env` | OUR RESULT (SIMULATOR) | 5, 7 |
| rl_high_cost | C_miss 1000: hold -226.7, rule -200.0, CQL -200.9 (LCB -10.3). C_miss 5000: hold -1133.3, rule -478.1, CQL -486.8 (LCB -31.9) | high-miss-cost sensitivity; physics rule = oracle; CQL not deployed at any cost | `results/rl_env/rl_env_cmiss1000_s0_report.json, rl_env_cmiss5000_s0_report.json` | OUR RESULT (SIMULATOR) | 5, 7 |
| pstar | 0.0476 | p* = C_FA/(C_FA+C_miss), C_FA = 5, C_miss = 100 | `trinetra/configs/default.json` | CONFIG | 5 |
| ex_w | 0.603 / 0.655 / 0.147 | effective weights CCTV / sensor stream (generic) / media check | `docs/07 §A (computed with repo code)` | WORKED EXAMPLE | 5 |
| ex_p | 0.6335 | FM-1 fused risk; U* 0.2465; level RED; PHARAOH 0.6456 | `docs/07 §A` | WORKED EXAMPLE | 5 |
| vision | RESULT PENDING | fire CNN, zero-shot, deepfake, EO metrics on real data | `kaggle/run_hackathon.sh fire|zeroshot|deepfake|eo` | PENDING | 4, 7 |
| targets | TBD | acceptance targets (false alarms per camera-day, time to detection): NOT FOUND IN REPO | `-` | TBD | 1 |
| wfc | 84.48% F1 | WildFireCan-MMD: trained custom model beats zero-shot VLMs (abstract) | `2504.13231 via ws4_cctv/zero_shot_design.md` | PAPER REPORTS | 6 |
| evaclip | 82.0% top-1 | EVA-CLIP zero-shot ImageNet (abstract) | `2303.15389 via ws4_cctv/zero_shot_design.md` | PAPER REPORTS | 6 |
| rl100_hold | -22.7 | return, always-hold (C_miss = 100) | `results/rl_env` | OUR RESULT (SIMULATOR) | 5 |
| rl100_caine | -26.4 | return, Caine rule (C_miss = 100) | `results/rl_env` | OUR RESULT (SIMULATOR) | 5 |
| rl100_oracle | -22.9 | return, oracle with true hazard (C_miss = 100) | `results/rl_env` | OUR RESULT (SIMULATOR) | 5 |
| auc_pinn | 0.716 | ROC-AUC, Geo-PINN (trained, physics loss), spatial OOF; NOT admitted (did not beat baselines with CI); ECE 0.099 | `results/geo_pinn/geo_pinn_s0_report.json` | OUR RESULT | 3, 7 |
| zs_auc | 0.889 | ROC-AUC, zero-shot CLIP ViT-B-32 fire-or-smoke, D-Fire group-CV OOF, n 3,410 (final run; phase2 0.891, n 2,546) | `TRINETRA/results/zeroshot_final/zeroshot_s0_report.json` | OUR RESULT | 5, 6 |
| zs_recall05 | 0.607 | recall at 5% false-alarm rate, zero-shot OOF (D-Fire) | `TRINETRA/results/zeroshot_final/zeroshot_s0_report.json` | OUR RESULT | 5, 6 |
| zs_heldout_auc | 0.999 | ROC-AUC on held-out DeepFire forest images (deduped vs D-Fire, n 1,023); an easy set, not a field claim | `TRINETRA/results/zeroshot_final/zeroshot_s0_report.json` | OUR RESULT | 5, 6 |
| zs_ece | 0.236 → 0.173 | ECE raw → after cross-fit temperature calibration (OOF); still poorly calibrated | `TRINETRA/results/zeroshot_final/zeroshot_s0_report.json` | OUR RESULT | 5, 6 |
| zs_admit | NOT ADMITTED | did not beat climatology or a recalibrated-logistic baseline on cost-weighted value score with CI (p* = 0.048) | `TRINETRA/results/zeroshot_final/zeroshot_s0_report.json` | OUR RESULT | 5, 6 |
| zs_fa_weather | 62% | false alarms at p = 0.5 on 1,000 weather images (fog/smog, sandstorm, lightning, rain) | `TRINETRA/results/zeroshot_final/zeroshot_s0_report.json` | OUR RESULT | 5, 6 |
| zs_fa_flames | 80% | false alarms at p = 0.5 on 600 candle / lighter / matchstick flames | `TRINETRA/results/zeroshot_final/zeroshot_s0_report.json` | OUR RESULT | 5, 6 |
| zs_fa_scenes | 27% | false alarms at p = 0.5 on 800 normal street / building / forest / mountain scenes | `TRINETRA/results/zeroshot_final/zeroshot_s0_report.json` | OUR RESULT | 5, 6 |

<!-- END -->
