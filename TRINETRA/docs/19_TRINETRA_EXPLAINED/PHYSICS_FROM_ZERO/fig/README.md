# Figures — kya hai aur kaise banaaye

Sab figures `python3 tools/make_figures.py` se bante hain (repo root se; `matplotlib` chahiye). Cross-modal/stress figures ke liye
Kaggle ka zip do: `python3 tools/make_figures.py --x-zip out_X_final.zip`.

## WORKED EXAMPLES (physics curves from repo functions, NOT results)
| File | Kya dikhata hai | Chapter |
|---|---|---|
| 01_fs_vs_pore_pressure.png | FS vs ψ, alag slope angles | P01 |
| 02_iverson_pressure_head.png | baarish ke baad ψ(t) | P01 |
| 03_caine_threshold.png | Caine I–D line | P01 |
| 04_fukuzono_inverse_velocity.png | 1/v se failure time | P01 |
| 05_fire_physics.png | flame height, Byram, flicker + aliasing | P02 |
| 06_plume_temperature.png | ΔT vs height | P02 |
| 07_cost_loss_and_prior_shift.png | p\* aur base-rate shift | P03 |
| 08_lora_range_airtime.png | range vs airtime (ASSUMED n) | P04 |
| 09_fresnel_real_terrain.png | synthetic nodes on REAL Chamoli DEM | P04 |
| 10_noisy_or.png | noisy-OR | P01/P03 |

## OUR RESULTS (`TRINETRA/results/figures/`, from real result files)
| File | Source | Caveat |
|---|---|---|
| R1_fire_roc_oof_and_heldout.png | fire_meta OOF + held-out | held-out near-saturated |
| R2_calibration.png | fire_meta | per-image |
| R3_alert_flood_vs_base_rate.png | real OOF + PROPOSED prior shift | correction not in repo |
| R4_landslide_auc.png | geo_large s0 | case-control, 736 rows |
| R5_rl_heldout.png | offline_rl_heldout | fixed rules retained |
| R6_generalisation_gap.png | master_merged | OOF vs held-out |
| R7–R9 | needs `out_X_final.zip` | generated only after the Kaggle run |
