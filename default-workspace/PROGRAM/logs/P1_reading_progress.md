# P1 READING PROGRESS — crash-resumable ledger (Phase P1)
# Append/update as each paper is read. read_depth: FT / FT-PARTIAL / SKIM / ABS / FETCH-FAIL.
# BASELINE rows do NOT count toward the 15-paper quota; QUOTA rows do.
# Note file: analysis/03_paper_notes/<id>_<tag>.md

## Totals (update each batch)
- Baseline corpus size: ~121 unique (128 PDFs − 7 dup IDs; 8 named non-arXiv).
- Baseline-corpus papers read so far: 41 (IDs confirmed present in analysis/01_baseline_papers.md)
  (incl. 1 FETCH-DEFERRED: nhess-22-3309-2022, title/DOI verified, body not yet read)
- External design-anchor papers read (NOT in local corpus, NOT quota): 3
- P1 NEW-paper QUOTA read so far: **15 of 15 — QUOTA COMPLETE** (2410.06388, 2209.11632, 2604.25512, 2010.09107, 2404.19452, 2608.26304, 2206.09981, 2412.13439, 2103.09783, 2405.00031, 2606.21130, 2311.14110, 2306.04590, 2310.03986, 2601.05921)
- Read-depth mix: 15/15 FT-PARTIAL (Tier-2+ full-text via ar5iv/arXiv-HTML) = 100% Tier-2+ (requirement ≥60% met).
  = 1707.08114 (MTL survey), 1708.08611 (safe-RL shielding), 2106.08909 (one-step offline RL).
  Genuinely full-text; cited as design anchors (WS5/WS8). Logged for honesty; counted neither
  as baseline-corpus nor as the 15 NEW quota.
- Quota (NEW, discovered via P1 search) read so far: 0 / 15
- Notes written (total): 22
- Audit done: not yet (run at >=10% of new notes)
- FULL-TEXT UNAVAILABLE (no ar5iv/arxiv HTML): 1707.06347 (PPO; image PDF)→ABS;
  2510.10546 (GLOFNet; no HTML)→ABS.
- DISCARDED guessed IDs (resolved to wrong-domain NLP, no note written, no fabrication):
  2010.12421 (TweetEval), 2101.10038 (SpanEmo). Lesson: only read IDs listed in the real
  baseline index; do not guess arXiv IDs.

## Log
| # | id | set | read_depth | note file | date | sections actually seen |
|---|----|-----|-----------|-----------|------|------------------------|
| 1 | 2110.06169 | baseline/rl | FT-PARTIAL | 2110.06169_IQL.md | 2026-10-05 | abstract, §1, Lemma2+Cor2.1 |
| 2 | 2006.04779 | baseline/rl | FT-PARTIAL | 2006.04779_CQL.md | 2026-10-05 | abstract, §1, §3 Eq1/Eq2, AppD tail |
| 3 | 2005.01643 | baseline/rl | FT-PARTIAL | 2005.01643_offlineRL_survey.md | 2026-10-05 | abstract, §1, DP/Bellman formalism |
| 4 | 1801.01290 | baseline/rl | FT-PARTIAL | 1801.01290_SAC.md | 2026-10-05 | abstract, §1, Algorithm 1, Eq.13 |
| 5 | 2106.06860 | baseline/rl | FT-PARTIAL | 2106.06860_TD3BC.md | 2026-10-05 | abstract, §1, D4RL results table |
| 6 | 1707.06347 | baseline/rl | ABS | 1707.06347_PPO.md | 2026-10-05 | abstract only (no HTML) |
| 7 | 2304.07193 | baseline/sat | FT-PARTIAL | 2304.07193_DINOv2.md | 2026-10-05 | abstract, §1, distill ablation table |
| 8 | 2308.11929 | baseline/sat | FT-PARTIAL | 2308.11929_dynamic_LSA_InSAR.md | 2026-10-05 | abstract, §1, §3.3 InSAR, §3.3.2 |
| 9 | 2510.10546 | baseline/sat | ABS | 2510.10546_GLOFNet_dataset.md | 2026-10-05 | abstract only (no HTML) |
| 10 | 2401.13695 | baseline/phys | FT-PARTIAL | 2401.13695_GNS_inverse_runout.md | 2026-10-05 | abstract, §1, Table 2, FD-vs-AD |
| 11 | 2009.07415 | baseline/mm | FT-PARTIAL | 2009.07415_MetaAAD.md | 2026-10-05 | abstract, §I, PPO Eq.2 loss |
| 12 | 2608.12422 | baseline/sat+mm | FT-PARTIAL | 2608.12422_which_site_when.md | 2026-10-05 | abstract, intro, methods, results framing |
| 13 | 2205.09884 | baseline/mm | FT-PARTIAL | 2205.09884_RL_model_selection.md | 2026-10-05 | abstract, §I, §IV-E2 reward ablation TblIII |
| 14 | 2507.15021 | baseline/phys | FT-PARTIAL | 2507.15021_ALPINE_PINN_flood.md | 2026-10-05 | abstract, §1, scheduled-sampling/noise/BPTT |
| 15 | 2311.01564 | baseline/sat | FT-PARTIAL | 2311.01564_InSAR_ElForn.md | 2026-10-05 | abstract, intro (deep-seated physics) |
| 16 | 2102.06491 | baseline/cctv | FT-PARTIAL | 2102.06491_rockfall_e2e.md | 2026-10-05 | abstract, §1, §3.9 Nemenyi, §3.10 |
| 17 | 2306.12826 | baseline/iot | FT-PARTIAL | 2306.12826_lowcost_DGPS_ublox.md | 2026-10-05 | abstract, §I, §I-A, §I-B |
| 18 | 2402.12095 | baseline/sat | FT-PARTIAL | 2402.12095_MajorTOM_EO_dataset.md | 2026-10-05 | abstract, §1, Fig.1 caption |
| 19 | 1707.08114 | EXT-anchor/mm | FT-PARTIAL | 1707.08114_MTL_survey.md | 2026-10-05 | abstract, §I, §II-A feature-learning |
| 20 | 2107.07511 | baseline/root(conformal) | FT-PARTIAL | 2107.07511_conformal_intro.md | 2026-10-05 | abstract, TOC, §1.1, §2.1 APS, §2.2 CQR |
| 21 | 1708.08611 | EXT-anchor/rl | FT-PARTIAL | 1708.08611_safe_RL_shielding.md | 2026-10-05 | abstract, §1, Fig1/2, MDP-abstraction def |
| 22 | 2106.08909 | EXT-anchor/rl | FT-PARTIAL | 2106.08909_onestep_offlineRL.md | 2026-10-05 | abstract, §1, Table2 reverse-KL |
| 23 | 2108.06852 | baseline/cctv | FT-PARTIAL | 2108.06852_HF2VAD_video_anomaly.md | 2026-10-05 | abstract, §1, Eq.9 fusion, §4.1 MNIST |
| 24 | 2404.15860 | baseline/phys | ABS | 2404.15860_FEM_MPM_tailings_runout.md | 2026-10-05 | abstract only (no HTML) |
| 25 | 2204.06097 | baseline/phys | ABS | 2204.06097_ML_surrogate_slope_stability.md | 2026-10-05 | abstract only (no HTML) |
| 26 | 2201.06837 | baseline/sat | FT-PARTIAL | 2201.06837_SNN_landslide_susceptibility.md | 2026-10-05 | abstract, intro, conclusion/data-avail |
| 27 | 2106.10652 | baseline/iot | ABS | 2106.10652_TinyML_ESP32.md | 2026-10-05 | abstract only (no HTML) |
| 28 | 2311.00566 | baseline/mm+sat | ABS | 2311.00566_CROMA_radar_optical_SSL.md | 2026-10-05 | abstract only (ar5iv fatal / no HTML) |
| 29 | 2010.14934 | baseline/iot | FT-PARTIAL | 2010.14934_beekeeping_energy_IoT.md | 2026-10-05 | abstract, §1 (energy-budget framing) |
| 30 | 2112.11965 | baseline/iot | ABS | 2112.11965_passive_RFID_geoscience.md | 2026-10-05 | abstract only (no HTML; journal ver exists) |
| 31 | 2307.04016 | baseline/iot | FT-PARTIAL | 2307.04016_LTE_solar_urban_sensornet.md | 2026-10-05 | abstract, §1 criteria, refs (+spill middle) |
| 32 | 2007.02756 | baseline/phys | ABS | 2007.02756_FFM_GPS_CampiFlegrei.md | 2026-10-05 | abstract (2-sentence; CC0; Voight co-author) |
| 33 | nhess-22-3309-2022 | baseline/sat | FETCH-DEFERRED | nhess-22-3309-2022_chamoli_precollapse.md | 2026-10-05 | title/venue/DOI verified; body not yet read |
| 34 | 2509.10560 | baseline/phys+sat | FT-PARTIAL | 2509.10560_GTS_Forecaster_geodetic.md | 2026-10-05 | abstract, §1, Table 2 TG forecasting |
| 35 | 2206.00515 | baseline/mm+sat | FT-PARTIAL | 2206.00515_Landslide4Sense_benchmark.md | 2026-10-05 | abstract, §I, dataset+protocol, refs (+spill) |
| 36 | 2503.11849 | baseline/mm+sat | FT-PARTIAL | 2503.11849_Copernicus_FM.md | 2026-10-05 | abstract, §1, Fig1, §5 Bench Table 3 |
| 37 | 2412.04563 | baseline/iot | ABS | 2412.04563_LoRa_rural_Nepal.md | 2026-10-05 | abstract only (no HTML; Nepal mountain terrain) |
| 38 | 1904.02639 | baseline/cctv | FT-PARTIAL | 1904.02639_MemAE_anomaly.md | 2026-10-05 | abstract, §1, Fig1 mechanism, Fig4 MNIST |
| 39 | 2211.07044 | baseline/mm+sat | FT-PARTIAL | 2211.07044_SSL4EO_S12_dataset.md | 2026-10-05 | abstract, §I, Table XI data-scale ablation |
| 40 | 2104.11009 | baseline/phys | FT-PARTIAL | 2104.11009_PIML_hydrology_Narmada.md | 2026-10-05 | abstract, keypoints, §1, Table 2 |
| 41 | 2404.10135 | baseline/phys+sat | ABS | 2404.10135_LSTM_precip_merge_SierraNevada.md | 2026-10-05 | abstract only (ar5iv fatal / no HTML) |
| 42 | 1806.05035 | baseline/phys | FT-PARTIAL | 1806.05035_probabilistic_dam_breach_bayesian.md | 2026-10-05 | abstract, §1, sediment-transport formulation |
| 43 | 2212.12038 | baseline/sat+phys | FT-PARTIAL | 2212.12038_community_detection_InSAR.md | 2026-10-05 | abstract, §I, §IV.1 community structures |
| 44 | 1909.01968 | baseline/rl+iot | FT-PARTIAL | 1909.01968_ACES_energy_harvesting_RL.md | 2026-10-05 | abstract, §1, §3.4 + Table 3 Q-learning HPs |
| 45 | 2412.14123 | baseline/mm+sat | FT-PARTIAL | 2412.14123_AnySat_EO_model.md | 2026-10-05 | abstract, §1, Fig1, SSL/JEPA background |
| 46 | 2210.04218 | baseline/cctv+mm | FT-PARTIAL | 2210.04218_FloodTransformer_segmentation.md | 2026-10-05 | abstract, §1 context (India flood stats) |
| 47 | 2410.06388 | QUOTA#1/A8 | FT-PARTIAL | 2410.06388_QUOTA_alert_fatigue_pedestrian.md | 2026-10-06 | NEW quota; abstract,§1,results; alert-fatigue |
| 48 | 2209.11632 | QUOTA#2/method | FT-PARTIAL | 2209.11632_QUOTA_continuous_ML_safety_assurance.md | 2026-10-06 | NEW quota; abstract,§I,§II; GSN safety case |
| 49 | 2604.25512 | QUOTA#3/method | FT-PARTIAL | 2604.25512_QUOTA_posthoc_reasoning_phishing.md | 2026-10-06 | NEW quota; abstract,§I; confidence-gated post-hoc |
| 50 | 2104.11422 | ABS/A13 | ABS | 2104.11422_ABS_socio_meteorology_crywolf.md | 2026-10-06 | ABS-only (no HTML); cry-wolf trust model; non-quota |
| 51 | 2010.09107 | QUOTA#4/A7 | FT-PARTIAL | 2010.09107_QUOTA_EnbPI_conformal_timeseries.md | 2026-10-06 | NEW quota; abstract,§1,theory,algo; EnbPI |
| 52 | 2404.19452 | QUOTA#5/A14 | FT-PARTIAL | 2404.19452_QUOTA_drift_detection_energy.md | 2026-10-06 | NEW quota; abstract,§I,results table; drift+energy |
| 53 | 2608.26304 | QUOTA#6/A13 | FT-PARTIAL | 2608.26304_QUOTA_flood_evacuation_equity.md | 2026-10-06 | NEW quota; abstract,§1,§3 model; evacuation equity |
| 54 | 2206.09981 | QUOTA#7/A8 | FT-PARTIAL | 2206.09981_QUOTA_imbalance_metric_sensitivity.md | 2026-10-06 | NEW quota; abstract,§1,framework; metric sensitivity |
| 55 | 2412.13439 | QUOTA#8/A8 | FT-PARTIAL | 2412.13439_QUOTA_MIP_ensemble_rare_event.md | 2026-10-06 | NEW quota; abstract,§intro,tables; MIP ensemble |
| 56 | 2103.09783 | QUOTA#9/method | FT-PARTIAL | 2103.09783_QUOTA_technical_debt_AI_systems.md | 2026-10-06 | NEW quota; abstract,§I,tables; AI technical debt |
| 57 | 2405.00031 | QUOTA#10/WS4 | FT-PARTIAL | 2405.00031_QUOTA_segnet_wildfire_detection.md | 2026-10-06 | NEW quota; abstract,§I,arch search; wildfire e2e |
| 58 | 2606.21130 | QUOTA#11/A8 | FT-PARTIAL | 2606.21130_QUOTA_burst_aware_EWS_threshold.md | 2026-10-06 | NEW quota; abstract,§I; high-recall EWS threshold |
| 59 | 2311.14110 | QUOTA#12/A5 | FT-PARTIAL | 2311.14110_QUOTA_datacope_ope_evaluation.md | 2026-10-06 | NEW quota; abstract,§1,setup; DataCOPE OPE feasibility |
| 60 | 2306.04590 | QUOTA#13/A7 | FT-PARTIAL | 2306.04590_QUOTA_proximity_calibration.md | 2026-10-06 | NEW quota; abstract,§1,§3,Thm5.1; proximity calibration |
| 61 | 2310.03986 | QUOTA#14/A12 | FT-PARTIAL | 2310.03986_QUOTA_missing_modality_robust_fusion.md | 2026-10-06 | NEW quota; abstract,§1,§4; missing-modality fusion |
| 62 | 2601.05921 | QUOTA#15/A8 | FT-PARTIAL | 2601.05921_QUOTA_cost_loss_value_score.md | 2026-10-06 | NEW quota; abstract,§1,§2.1,refs; cost-loss Value Score |

# EXT-anchor = genuine full-text read but NOT in local baseline corpus and NOT a NEW-quota
# paper; a cited design anchor (WS5/WS8). Counted separately (see Totals).

## Reading order (priority; existing corpus to depth FIRST per D-007 #2)
NEXT UP:
- RL cluster (CR-03): 2005.01643 (offline survey), 1707.06347 (PPO), 1801.01290 (SAC),
  1706.02275 (MADDPG), 2009.07415 (Meta-AAD), 2205.09884 (RL model-selection).
- Satellite/LHASA cluster: lhasa* (resolve DOIs), 2608.12422 (FT done in P0-probe; formalize),
  2304.07193 (DINOv2), satellite SSL encoders.
- Physics cluster (WS1): 2401.13695 + Iverson/transient-infiltration set.
- CCTV/IoT/multimodal clusters by WS.
Then 15 NEW quota papers (end-to-end safety-critical ML eval; disaster-system surveys;
alert-fatigue/false-alarm; multi-component pipeline evaluation).
