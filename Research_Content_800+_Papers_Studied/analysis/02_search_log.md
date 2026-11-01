# 02 — Search Log

Method: queries issued against the official arXiv API (`https://export.arxiv.org/api/query`),
which returns real arXiv IDs + abstracts (honest existence verification + faithful
abstract-level notes). Semantic Scholar API used opportunistically (rate-limited without key).
For highest-relevance hits I fetch the `/abs/` page or the local-corpus comparison to read
full-text. Space-separated terms default to OR on arXiv; I use `abs:%22phrase%22+AND+...`
for precision. Every harvested paper is deduped against the local 110-paper corpus and against
prior ledger rows (by arXiv ID / DOI / title).

read_depth legend: FT = full-text read; ABS = abstract-only (verified real, abstract read).

## Axes (from 00_system_model.md §10)
A1 InSAR time-series forecasting / precursor detection
A2 EO foundation models / SSL for remote sensing
A3 Rainfall I–D thresholds (Himalaya/global)
A4 Transient infiltration physics (Iverson/TRIGRS/Richards)
A5 Offline RL (distribution shift, conservatism, OPE)
A6 Safe RL / shielding / constrained MDP
A7 Conformal prediction & risk control
A8 Rare-event / imbalance / calibration / EWS verification
A9 Video anomaly detection (edge) / LSPIV river velocimetry
A10 LoRa/LPWAN mountains / DTN / energy harvesting
A11 GLOF / dam-break / debris-flow runout
A12 Multimodal / stacked / meta fusion / MoE gating / model selection
A13 Evacuation / decision under uncertainty / cost-loss / value of warnings
A14 Distribution shift / concept drift / OOD / deployed-ML monitoring

## Query ledger (chronological)
| # | axis | query (decoded) | source | returned | new kept |
|---|------|------------------|--------|----------|----------|
| 1 | A1 | InSAR landslide deformation forecasting (OR) | arXiv | 12 | 5 |
| 2 | A2 | "masked autoencoder" AND "remote sensing" | arXiv | 42 | 3 (FG-MAE 2310.18653, CSMAE 2401.07782, FireRisk 2303.07035) |
| 3 | A11 | "dam break" AND "flood" AND "simulation" | arXiv | 14 | 2 (1911.05219 Brumadinho, 2209.08729 RC-ESN) |
| 4 | A12 | "multimodal fusion" AND "missing modality" | arXiv | 37 | 2 (DCER 2602.04904, RoHyDR 2505.17501) |
| 5 | A4 | "unsaturated soil" AND "slope stability" | arXiv | 1 | 0 (only baseline 1305.4803) |
| 6 | A6 | "safe reinforcement learning" AND "constraint" | arXiv | 176 | 2 (COSRL survey 2601.05152, CAPSULE 2604.23576) |
| 7 | A7 | "conformal prediction" AND "time series" | arXiv | 100 | 2 (HopCPT 2303.12783, Flow-CP 2502.05709) |
| 8 | A11 | "flood mapping" AND "SAR" AND "deep learning" | arXiv | 7 | 2 (VV-VH 2605.02153, review 2411.04153) |
| 9 | A3 | "early warning system" AND "landslide" | arXiv | 11 | 1 (RMCL 2605.17419) + runout-emulation noted |
| 10 | A2 | "foundation model" AND "earth observation" | arXiv | 182 | 3 (agri-gap 2608.30392, REOBench 2505.16793, PhilEO 2401.04824) |
| 11 | A8 | "isolation forest" AND "anomaly" | arXiv | 186 | 2 (DIFFI 2007.11117, ABIForest 2210.02558) |
| 12 | A1 | "MEMS" AND "tilt" AND "landslide" | arXiv | 0 | 0 |
| 13 | A11 | "debris flow" AND "runout" | arXiv | 4 | 1 (FEM-MPM 2404.15860; 2401.13695 dedup) |
| 14 | A9 | "video anomaly detection" AND "weakly supervised" | arXiv | 72 | 2 (UCF-Crime-DVS 2503.12905, GCL 2203.03962) |
| 15 | A14 | "concept drift" AND "streaming" AND "detection" | arXiv | 149 | 2 (Meta-ADD 2105.01419, learner-based 2606.20216) |
| 16 | A12 | "stacking" AND "ensemble" AND "meta-learner" | arXiv | 36 | 1 (boosting-meta 2402.01379 — multicollinearity) |
| 17 | A3 | "rainfall threshold" AND "landslide" | arXiv | 0 | 0 (phrase too tight) |
| 18 | A10 | "LoRaWAN" AND "coverage" | arXiv | 25 | 2 (DtS 2409.20408, D2D 1703.01985) |
| 19 | A8 | "extreme event" AND "deep learning" AND "prediction" | arXiv | 47 | 2 (when/where 2203.17155, UniExtreme 2508.01426) |
| 20 | A1 | "GNSS" AND "deformation" AND "monitoring" | arXiv | 10 | 2 (GNSS-RTK 2301.05977, crustal 2607.16264) |
| 21 | A13 | "evacuation" AND "optimization" AND "disaster" | arXiv | 23 | 2 (robust-opt 2608.04225, ridesharing 2103.15156) |
| 22 | A2 | "self-supervised" AND "time series" AND "representation" | arXiv | 222 | 2 (Series2Vec 2312.03998, ExtraMAE 2201.07006) |
| 23 | A8 | "class imbalance" AND "rare" AND "classification" | arXiv | 127 | 2 (PFN-imbalance 2605.21742, SeismoFlow 2007.12229) |
| 24 | A14 | "offline reinforcement learning" AND "distribution shift" | arXiv | 131 | 1 (AFAPE 2312.01530; 2305.03360 dedup) |
| 25 | A12 | "mixture of experts" AND "gating" | arXiv | 636 | 0 (2410.10397, 2604.20551 already ledgered) |
| 26 | A9 | "optical flow" AND "river" AND "velocity" | arXiv | 0 | 0 |
| 27 | A1 | "InSAR" AND "time series" AND "deep learning" | arXiv | 2 | 2 (forest 2511.04362, forecasting 2509.18176) |
| 28 | A5 | "reward shaping" AND "reinforcement learning" | arXiv | 578 | 2 (PBRS 2502.01307, subgoal 2104.06411) |
| 29 | A11 | "cloudburst" OR ("flash flood" AND "forecasting") | arXiv | 30 | 2 (EWS-compare 1904.07213, FlowDB 2012.11154) |
| 30 | A8 | "deep svdd" OR ("one-class" AND "deep learning") | arXiv | 120 | 1 (FlowSVDD 2108.04907) |
| 31 | A7 | "conformal" AND "distribution shift" | arXiv | 186 | 0 (2511.11567, 2406.05405 already ledgered) |
| 32 | A13 | "evacuation" AND "reinforcement learning" | arXiv | — | logged earlier; equity/compliance (2502.17701, 2412.05777) |
| 33 | A12 | "mixture of experts" AND "multimodal" AND "fusion" | arXiv | 101 | (RICH — mined waves 16-17) |
| 34 | A9 | "surface velocity" AND "river" | arXiv | 3 | (LSPIV-adjacent; discharge-conversion risk 1607.04139 etc.) |
| 35 | A9 | "LSPIV" OR "image velocimetry" (river) | arXiv | low | 0 new (space near-exhausted) |
| 36 | A3 | "early warning" AND "debris flow" AND "rainfall" | arXiv | 0 | 0 |
| 37 | A3 | "intensity-duration" AND "debris flow" | arXiv | 1 | 0 (phrase too tight) |
| 38 | A8 | "uncertainty quantification" AND "early warning" | arXiv | 8 | mined |
| 39 | A1 | "precipitation nowcasting" AND "deep learning" | arXiv | 48 | (RICH; later refined w/ transformer, wave 20) |
| 40 | A4 | "physics-informed" AND "landslide" | arXiv | 2 | mined |
| 41 | A7 | "selective prediction" AND "deep learning" | arXiv | 21 | (RICH; feeds SCRC 2512.12844) |
| 42 | A11 | "flood mapping" AND "SAR" AND "deep learning" (batch-13) | arXiv | 7 | (see #8) |
| 43 | A11 | "glacial lake" AND "outburst" | arXiv | 5 | near-exhausted |
| 44 | A10 | "TinyML" AND "anomaly detection" | arXiv | 15 | mined |
| 45 | A10 | "sensor fault" AND "detection" AND "wireless sensor" | arXiv | 4 | mined (1509.06065) |
| 46 | A6 | "runtime assurance" AND "reinforcement learning" | arXiv | 6 | mined (2310.04288) |
| 47 | A7 | "conformal prediction" AND "time series" (batch-15 redo) | arXiv | 100 | (see #7) |
| 48 | A14 | "out-of-distribution" AND "time series" AND "detection" | arXiv | 29 | mined (wave 16) |
| 49 | A10 | "LoRaWAN" AND "disaster" | arXiv | 3 | mined |
| 50 | A1 | "InSAR" AND "atmospheric correction" | arXiv | 2 | mined |
| 51 | A5 | "off-policy evaluation" AND "offline reinforcement learning" | arXiv | 23 | mined (wave 16) |
| 52 | A13 | "false alarm" AND "early warning" AND "trust" | arXiv | 3 | mined (2104.11422 cry-wolf) |
| 53 | A12 | "mixture of experts" AND "routing" AND "load balancing" | arXiv | 95 | mined (2604.00801, 2601.03425) |
| 54 | A12 | "stacked generalization" OR "super learner" | arXiv | 133 | mined (2004.01764, 2509.03315) |
| 55 | A4 | "ensemble Kalman filter" AND "data assimilation" AND "machine learning" | arXiv | 23 | mined (2107.07687, 2412.14318) |
| 56 | A13 | "explainability" AND "high-stakes" AND "decision" | arXiv | 219 | 2 (2311.11491, 2101.09429) |
| 57 | A1 | "graph neural network" AND "landslide susceptibility" | arXiv | 0 | 0 |
| 58 | A14 | "test-time adaptation" AND "distribution shift" | arXiv | 322 | 2 (2205.13723 DLTTA, 2411.15204 DART) |
| 59 | A11 | "streamflow" AND "LSTM" AND "flood" | arXiv | 4 | 2 (2510.08488 h-Diffusion, 2512.12183 HydroDiffusion) |
| 60 | A10 | "energy harvesting" AND "wireless sensor" AND "duty cycle" | arXiv | 8 | 2 (1511.08331 VoI-MAB, 1010.4385 Wiselib) |
| 61 | A8 | "earthquake early warning" AND "deep learning" | arXiv | 12 | 3 (2006.01332, 2412.00264 DetEQ, 2312.15218) |
| 62 | A10 | "sensor placement" AND "information" AND "monitoring" | arXiv | 31 | 2 (2303.09750 RL-placement, 2303.00028 sparse-GP) |
| 63 | A11 | "debris flow" AND "seismic" AND "detection" | arXiv | 1 | 1 (2401.13877 AscDAMs SLAM) |
| 64 | A8 | "calibration" AND "distribution shift" AND "uncertainty" | arXiv | 171 | 1 (2504.17719 DGP) |
| 65 | A8 | "extreme value theory" AND "neural network" AND "rare" | arXiv | 3 | 2 (2310.03220, 2411.13496 DI-GNN) |
| 66 | A1 | "precipitation nowcasting" AND "transformer" | arXiv | 26 | 2 (2609.37038 NowcastDiT, 2402.04290 CasCast) |
| 67 | A7 | "conformal risk control" | arXiv | 89 | 2 (2603.10392 CBF+CRC, 2512.12844 SCRC) |
| 68 | A13 | "cost-sensitive" AND "decision" AND "alarm" | arXiv | 3 | 1 (2509.11789 fall-detection cost-threshold) |
| 69 | A12 | "missing modality" AND "robust" AND "multimodal" | arXiv | 199 | 2 (2401.13697 TRML, 2310.03986 PE-adaptation) |
| 70 | A8 | "aleatoric" AND "heteroscedastic" AND "regression" | arXiv | 19 | 2 (2512.01384 CLAPS, 2406.09262 DDPN) |
| 71 | A8 | "Bayesian model averaging" AND "deep" | arXiv | 16 | 1 (2001.04567 SGLD-BMA seismic UQ) |
| 72 | A11 | "physics-informed neural network" AND "shallow water" | arXiv | 20 | 2 (2406.16236 tsunami PINN/DeepONet, 2104.00615 sphere) |
| 73 | A11 | "digital twin" AND "flood" | arXiv | 12 | 1 (2505.08553 Alzette particle-filter DA) |
| 74 | A13 | "large language model" AND "disaster" AND "decision" | arXiv | 46 | 2 (2605.11348 causal-LLM, 2410.20707 DisasterQA) |
| 75 | A11 | "spatiotemporal" AND "graph neural network" AND "flood" | arXiv | 3 | 1 (2512.23964 DUALFloodGNN) |
| 76 | A2 | "soil moisture" AND "landslide" AND "satellite" | arXiv | 2 | 2 (2509.17942 StefaLand, 2211.10338 SAR-density) |
| 77 | A10 | "delay tolerant" AND "routing" AND "disaster" | arXiv | 12 | 2 (2603.15945 Epidemic-vs-SnW, 1903.02611 HRSON) |
| 78 | A9 | "quantization" AND "microcontroller" AND "inference" | arXiv | 61 | 2 (2306.00001 TinyissimoYOLO, 2105.13331 MCU-quant) |
| 79 | A11 | "infrasound" AND "debris flow" | arXiv | 0 | 0 (empty space) |
| 80 | A14 | "online learning" AND "concept drift" AND "sensor" | arXiv | 1 | 1 (2608.24288 SNN drift compensation) |
| 81 | A2 | "domain adaptation" AND "remote sensing" AND "cross-region" | arXiv | 0 | 0 (phrase too tight) |
| 82 | A11 | "rainfall-runoff" AND "LSTM" AND "ungauged" | arXiv | 0 | 0 (phrase too tight) |
| 83 | A13 | "alarm fatigue" AND "machine learning" | arXiv | 8 | 1 (2503.14621 false-VT-alarm ML) |
| 84 | A8 | "positive unlabeled" AND "anomaly detection" | arXiv | 8 | 1 (2405.18929 deep PU-SVDD contaminated) |
| 85 | A14 | "unsupervised domain adaptation" AND "segmentation" AND "satellite" | arXiv | 6 | 2 (2210.10732 OpenEarthMap, 2212.12103 UDA self-train) |
| 86 | A13 | "warning" AND "compliance" AND "evacuation" | arXiv | 1 | 1 (2109.07745 wildfire GPS 46% compliance) |
| 87 | A11 | "ungauged basins" AND "deep learning" | arXiv | 2 | 2 (2503.09947 water-quality-trust, 2606.04143 PIML-flood) |
| 88 | A14 | "reject option" AND "classification" AND "safety" | arXiv | 2 | 2 (2207.12545 p-DkNN, 2105.03876 selective-hyptest) |
| 89 | A11 | "spatial cross-validation" AND "machine learning" | arXiv | 13 | 1 (2110.09497 EVT+GB+spatial-CV wildfire) |
| 90 | A8 | "imbalanced regression" AND "deep" | arXiv | 21 | 2 (2509.23240 LatentDiff, 2306.06599 VIR) |
| 91 | A8 | "evidential deep learning" AND "uncertainty" | arXiv | 125 | 2 (2309.13207 EDL-earth-system, 2604.06387 EDL-aquatic) |
| 92 | A13 | "trustworthy" AND "machine learning" AND "disaster" | arXiv | 2 | 1 (2605.08198 FairHealth) |
| 93 | A14 | "change point detection" AND "streaming" AND "time series" | arXiv | 8 | 2 (2508.18045 Riemannian-CPD, 2005.05385 PD-CPD) |
| 94 | A13 | "human-in-the-loop" AND "early warning" | arXiv | 1 | 1 (2512.14683 hospital-EWI) |
| 95 | A1 | "graph attention" AND "landslide susceptibility" | arXiv | 0 | 0 (empty space) |
| 96 | A1 | "precipitation nowcasting" AND "transformer" | arXiv | 26 | 0 (all top hits DEDUP: 2609.37038, 2402.04290 already logged) |
| 97 | A14 | "test-time adaptation" AND "distribution shift" | arXiv | 322 | 0 (top hits DEDUP 2205.13723; rest LLM/VLM out-of-scope) |
| 98 | A8 | "calibration" AND "distribution shift" AND "uncertainty" | arXiv | 171 | 0 (top hits DEDUP 2504.17719; 2205.14334 LLM-verbalized too tangential) |
| 99 | A12 | "missing modality" AND "robust" AND "multimodal" | arXiv | 199 | 0 (top hits DEDUP 2401.13697, 2310.03986 already logged) |
| NOTE | — | Wave-27 lesson: relevance-sorted tops of the "rich" 100–322-hit spaces OVERLAP my Wave 18–21 harvest. To reach NEW papers in these spaces, must use MORE SPECIFIC domain+method phrasing (below), not generic method terms. | — | — | — |
| 100 | A10 | "LoRa" AND "mesh" AND "monitoring" | arXiv | 4 | 2 (2312.08387 JMAC multi-hop, 2507.07841 HaLert HaLow) |
| 101 | A1 | "ground deformation" AND "forecasting" AND "deep learning" | arXiv | 1 | 0 (2509.18176 dedup) |
| 102 | A11 | "seismic" AND "debris flow" AND "early warning" | arXiv | 0 | 0 (empty space) |
| 103 | A7 | "conformal prediction" AND "regression" AND "covariate shift" | arXiv | 8 | 2 (2405.06479 multi-source-WCP, 2310.03545 risk-assessment) |
| RATE-LIMIT | — | 4-query parallel burst → arXiv HTTP 429 + 30s timeouts. LESSON: fire ONE Atom query at a time. | — | — | — |
| 104 | A11 | "glacial lake" AND "deep learning" | arXiv | 5 | 2 (2510.10546 GLOFNet, 2608.12422 free-satellite reality-check LANDMARK) |
| 104b | A11 | au:Kahn AND au:Pope AND abs:"Nepal" (ID recovery for 2608.12422 from pruned middle) | arXiv | 1 | (ID confirmed 2608.12422, NOT guessed) |
| 105 | A6 | "constrained Markov decision process" AND "safe" | arXiv | 97 | 2 (2305.16147 CoCoRL, 2602.20729 Fuz-RL) |
| 106 | A11 | "flood" AND "segmentation" AND "SAR" | arXiv | 16 | 3 (2606.29134 AlphaEarth-priors, 2307.07123 diffusion-SAR->EO, IGARSS-2022 bi-temporal via DOI) |
| 107 | A11 | "snow avalanche" AND "machine learning" | arXiv | 0 | 0 (empty) |
| 108 | A11 | "avalanche" AND "forecasting" AND "snow" | arXiv | 6 | 2 (2310.04428 SVM+MPM, 1901.04695 zero-inflated-gamma snow) |
| 109 | A8 | "data assimilation" AND "deep learning" AND "hydrology" | arXiv | 2 | 2 (2510.10799 linreg-beats-LSTM-TWS, 1707.06611 first-LSTM-hydrology-SMAP) |
| 110 | A5 | "off-policy evaluation" AND "offline reinforcement learning" | arXiv | 23 | 2 (2106.08909 one-step-no-OPE, 2206.02000 HVE) |
| 111 | A9 | "microcontroller" AND "quantization" AND "inference" | arXiv | 62 | 1 (2306.00001 TinyissimoYOLO; 2105.13331 dedup) |
| 112 | A13 | "explainable" AND "high-stakes" AND "decision" | arXiv | 219 | 1 (2505.14510 BACON; rest LLM-reasoning OUT OF SCOPE, not logged) |
| 113 | A11 | "physics-informed" AND "shallow water" AND "flood" | arXiv | 5 | 2 (2507.15021 ALPINE, 2501.11372 2D-SWE-PINN) |
| 114 | A8 | "deep ensembles" AND "uncertainty" AND "calibration" | arXiv | 127 | 1 (2006.08573 NES; 6D-pose + Hydra pruned/tangential) |
| 115 | A2 | "domain adaptation" AND "SAR" AND "remote sensing" | arXiv | 6 | 2 (1906.01379 ImageNet->SAR-poor, 2512.05140 FlowEO) |
| 116 | A9 | "knowledge distillation" AND "edge devices" AND "efficient" | arXiv | 95 | 2 (2402.02781 dual-KD-SED, 2604.27178 KD-monitoring) |
| 117 | A11 | "graph neural network" AND "landslide" | arXiv | 5 | 1 (2305.05218 GNN-granular-flow; 2401.13695 dedup) |
| 117b | A3 | au:Wang AND au:Bi AND abs:"extreme value" AND abs:"risk" (ID recovery) | arXiv | 1 | 1 (2509.10362 GNN+r-Pareto confirmed, NOT guessed) |
| 118 | A12 | "mixture of experts" AND "routing" AND "load balancing" | arXiv | 95 | 1 (2604.00801 Routing-Free-MoE; 2601.03425 dedup) |
| 119 | A10 | "federated learning" AND "wireless sensor" AND "environmental monitoring" | arXiv | 0 | 0 (empty) |
| 120 | A10 | "federated learning" AND "IoT" AND "anomaly detection" | arXiv | 35 | 2 (2602.24209 unsup-FL-hetero-IoT, FedIoT via DOI; quantum one out-of-scope) |
| 121 | A13 | "selective classification" AND "deep neural" | arXiv | 14 | 2 (2405.11533 hierarchical-SC, 2406.04745 CCL-SC; 2017 Geifman NOT guessed) |
| 122 | A10 | "sensor placement" AND "information" AND "monitoring" | arXiv | 31 | 1 (2303.09750 RL-info-gain-placement; 2303.00028 dedup) |
| 123 | A10 | "delay tolerant" AND "disaster" AND "network" | arXiv | 15 | 1 (1408.0104 opportunistic-forwarding; 1803.00275 dedup) |
| 124 | A14 | "change point detection" AND "multivariate" AND "streaming" | arXiv | 6 | 2 (2201.07125 WATCH, 2602.07252 distribution-valued-CPD) |
| 125 | A4 | "Richards equation" AND "unsaturated" | arXiv | 34 | 2 (2105.13133 meshless-RBF, 1507.07837 iterative-linearization) |
| 126 | A11 | "rockfall" AND "detection" | arXiv | 3 | 1 (2102.06491 TLS-ML rockfall, scope-gap; 1810.09409 partial) |
| 127 | A3 | "precipitation nowcasting" AND "radar" AND "deep learning" | arXiv | 25 | 1 (2210.12853 ASOC ground+radar +5.7% CSI) |
| 128 | A4 | "ensemble Kalman filter" AND "machine learning" | arXiv | 31 | 1 (2107.07687 AD-EnKF; 2412.14318 dedup) |
| 129 | A11 | "debris flow" AND "seismic" AND "early warning" / "debris flow" AND "monitoring" | arXiv | 0 / 1 | 0 (both empty/off-scope granular-restitution) |
| 130 | A1 | "InSAR" AND "deformation" AND "forecasting" | arXiv | 1 | 1 (2509.18176 CNN-LSTM InSAR — candidate #1 anchor CONFIRMED w/ authors) |
| 131 | A8 | "conformal prediction" AND "distribution shift" AND "time series" | arXiv | 13 | 2 (2601.18509 CP-TS-survey, 2202.07282 ACI/AgACI) |
| 132 | A14 | "test-time adaptation" AND "distribution shift" | arXiv | 322 | 1 (2205.13723 DLTTA; VLM/AI-text ones off-domain) |
| 133 | A8 | "evidential deep learning" AND "regression" | arXiv | 13 | 1 (2402.09056 EDL-epistemic-only-relative CAVEAT; 2309.13207 dedup) |
| 134 | A5 | "off-policy evaluation" AND "offline reinforcement learning" AND "selection" | arXiv | 6 | 2 (2110.14000 BVFT, 2311.18206 SCOPE-RL — both verified live) |
| 135 | A4 | "rainfall" AND "intensity-duration" AND "landslide" | arXiv | 1 | 1 (2106.15119 hybrid stochastic-mechanical ID thresholds — #15 DIRECT; paper #250) |
| --- PHASE P2 (2026-10-06) — Literature Foundation I. All hits novelty-checked vs ledger + novelty_index. --- |
| 136 | A9 | "wildfire detection" AND "deep learning" | arXiv | 20 | 2 (2610.01994 CatBoost>GOES-FDC, 2605.15894 evidential smoke severity) |
| 137 | A9 | "video anomaly detection" AND "weakly supervised" | arXiv | 82 | 2 (2610.05129 RBA, 2609.07455 federated VLM-verify) |
| 138 | A7 | "conformal prediction" AND "distribution shift" | arXiv | 116 | 1 (2610.02777 PID-Expert online CP, local coverage post-shift) |
| 139 | A8 | "data leakage" AND "machine learning" AND "evaluation" | arXiv | 191 | 1 (2610.04927 MLE-InsightBench leakage-as-validity-threat) |
| 140 | A9 | "fire detection" AND "false alarm" | arXiv | 9 | 1 (2609.05782 on-device VLM fire KD; 2610.01994 dedup) |
| 141 | A14 | "distribution shift" AND "robustness" AND "benchmark" | arXiv | 781 | 1 (2610.04392 VAND4.0 hidden-test AD benchmark, efficiency-first) |
| 142 | A8 | "selective prediction" AND "deep learning" | arXiv | 24 | 0 (2609.39429 glioma UQ off-domain; 2605.15894 dedup) |
| 143 | A14 | "out-of-distribution detection" AND "survey" | arXiv | 19 | 1 (2607.28248 UQ-for-trustworthy-DL methods+measures survey) |
| 144 | A9 | "video anomaly detection" AND "survey" | arXiv | 13 | 2 (2508.14203 VAD survey human/vehicle/env, 2507.21649 DNN→MLLM) |
| 145 | A9 | "edge deployment" AND "object detection" AND "real-time" | arXiv | 18 | 1 (2606.12066 YOLOv8/v11 adverse-weather developing-countries) |
| 146 | A8 | "evaluation metrics" AND "anomaly detection" AND "pitfalls" | arXiv | 0 | 0 (empty — reformulate next batch) |
| 147 | A8 | "early warning system" AND "machine learning" AND "landslide" | arXiv | 7 | 2 (2605.17419 LEWS rainfall-displacement-robust RMCL, 2601.03569 LID slope-failure) |
| 148 | A7 | "calibration" AND "temperature scaling" AND "limitations" | arXiv | 45 | 1 (2609.38936 signal-routed temp-scaling, small-budget calibrator capacity) |
| 149 | A14 | "image classification" AND "common corruptions" AND "robustness" | arXiv | 19 | 1 (2606.07593 ViT corruption-FT does-not-transfer across corruption classes) |
| 150 | A3 | "precipitation nowcasting" AND "evaluation" | arXiv | 40 | 1 (2609.17175 IRENE ConvGRU ensemble vs STEPS/DGMR, afCRPS) |
| 151 | A13 | "disaster response" AND "deep learning" AND "social media" | arXiv | 7 | 1 (2511.21364 BanglaMM multimodal disaster, low-resource South Asia) |
| 152 | A9 | "flood" AND "segmentation" AND "remote sensing" | arXiv | 30 | 1 (2609.20441 edge flood-seg distillation; MNDWI rule competitive=CR-02) |
| 153 | A3 | "early warning" AND "landslide" AND "deep learning" | arXiv | 5 | 0 (2605.17419 dedup; others off-domain/toolbox) |
| 154 | A9 | "surveillance" AND "anomaly detection" AND "weakly supervised" | arXiv | 37 | 2 (2609.07455 federated parser-free VLM WSVAD, 2609.05066 adaptive multi-granularity WSVAD) |
| 155 | A3 | "early warning system" AND "flash flood" | arXiv | 2 | 1 (2605.20167 HaorFloodAlert operational EWS, TRINETRA analog) |
| 156 | A2 | "self-supervised" AND "remote sensing" AND "foundation model" | arXiv | 61 | 1 (2606.13896 GeoFM downstream transfer study=CR-01; others queued) |
| 157 | A1 | "InSAR" AND "deep learning" AND "deformation" | arXiv | 12 | 1 (2509.18176 InSAR deformation forecasting, persistence-baseline=CR-02) |
| # ===== P3 BATCH-1 (phase P3; Literature Foundation II; 2026-10-06) ===== | | | | | |
| 158 | A11 | "LoRa" AND "disaster" AND "early warning" | arXiv | 0 | 0 (too narrow — broaden to LoRa+flood / LoRa+mesh next batch) |
| 159 | A5 | "deepfake detection" AND "generalization" | arXiv | 779 | 2 (2610.06339 BabelFake multilingual AV benchmark, 2610.03380 interpretable forensic+temporal) |
| 160 | A4 | "physics-informed neural network" AND "failure modes" | arXiv | 44 | 2 (2610.04828 label-free PINN slope reliability FS±2-3%, ModSync PINN capacity-failure) |
| 161 | A14 | "out-of-distribution detection" AND "survey" | arXiv | 19 | 1 (2608.16654 IsoMaxPlus+MC-dropout OOD/UQ, TNR@TPR95 +90%, ECE 0.0095→0.0026) |
| 162 | A12 | "reinforcement learning" AND "evacuation" | arXiv | 19 | 2 (2603.17319 PIER physics-informed offline RL + post-hoc shield, forecast-independent; 2602.14676 GREAT-EER graph evacuation) |
| 163 | A11 | "TinyML" AND "microcontroller" AND "detection" | arXiv | 35 | 2 (2610.06241 prototype-head on PSoC6, 1314-param 1D-CNN; 2609.27202 federated TinyML IoT security) |
| 164 | A6 | "public warning system" AND "cell broadcast" | arXiv | 1 | 1 (2604.24404 5G PWS spoofing testbed + cross-cell verification) |
| 165 | A10 | "multi-sensor" AND "fire detection" AND "false alarm" | arXiv | 0 | 0 (too narrow — broaden to fire+WSN / sensor-fusion next batch) |
| 166 | A9 | "time series" AND "anomaly detection" AND "benchmark" | arXiv | 289 | 1 (2610.06453 NCL: foundation models reconstruct anomalies too well — AD failure mode) |
| 167 | A5 | "content provenance" AND "watermarking" | arXiv | 24 | 1 (2610.04151 C2PA soft-bindings benchmark; watermark FP 5.9-15.3%, x86/ARM bit drift) |
| 168 | A3 | "LoRa" AND "flood monitoring" | arXiv | 1 | 0 (2410.15794 Habaek water-seg off-theme; no LoRa-EWS hit) |
| 169 | A12 | "safe reinforcement learning" AND "shield" | arXiv | 43 | 2 (2609.38655 forward-invariant certified policy class; 2608.19836 adaptive probabilistic shield, learned MDP) |
| 170 | A10 | "wireless sensor network" AND "forest fire" | arXiv | 7 | 1 (2111.12209 LoRa WSN fire 5km urban/10km rural; 2209.07620 fuzzy WSN fire+Lamport-sig security) |
| 171 | A8 | "deep reinforcement learning" AND "reproducibility" AND "evaluation" | arXiv | 47 | 1 (2610.03369 MoE/DRL seed-luck, attribution reverses 30↔100 seeds; RoAd-RL adversarial benchmark queued) |
| 172 | A4 | "wildfire spread" AND "physics" AND "machine learning" | arXiv | 14 | 1 (2609.18555 interpretable fire-spread; conv models use front-distance; fuel-load only strong var=CR-02; 2609.17763 auditable queued) |
| 173 | A13 | "crisis informatics" AND "misinformation" | arXiv | 1 | 1 (2007.05848 #19S Mexico earthquake, Global-South social-media verification, citizen fact-check) |
| 174 | A9 | "anomaly detection" AND "survey" AND "deep learning" | arXiv | 74 | 1 (2610.00363 DL-AD railway structured survey, 4-axis taxonomy × 4 paradigms + deploy framework) |
| 175 | A6 | "disaster" AND "mesh network" AND "communication" | arXiv | 11 | 1 (2507.07841 HaLert HaLow+LoRa+SDN post-disaster comms, field-tested; 2006 SOS self-org protocol queued) |
| 176 | A11 | "federated learning" AND "Internet of Things" AND "anomaly" | arXiv | 31 | 1 (2608.06876 FedVAR prototype-aligned federated video-anomaly, non-IID/unseen-domain) |
| 177 | A2/A9 | "time series" AND "anomaly detection" AND "self-supervised" | arXiv | 65 | 2 (2609.39337 WinoTS wavelet self-distillation; VACE Mahalanobis+velocity-bank "simple beats larger-budget"=CR-02; 2609.16314 cross-modal SSL fault-det queued) |
| 178 | A6 | "cell broadcast" AND "emergency alert" | arXiv | 1 | 1 (2604.24404 ONLY hit, confirms cell-broadcast/PWS arXiv near-empty; authors Abou Hasna/Chendeb/El Falou; cross-cell verification defense) |
| 179 | A8 | "reinforcement learning" AND "adversarial" AND "robustness" AND "benchmark" | arXiv | 147 | 2 (2609.31142 JevAdvBench untrusted-state typed-decision robustness; 2609.15297 Admissable adversarial-MISSINGNESS RL on MuJoCo = missing-modality CR, READ) |
| 180 | A13/A14 | "early warning" AND "fairness" AND "machine learning" | arXiv | 4 | 2 (2609.38552 Fairness Theatre vendor-controlled EWS post-hoc fairness fails; 2610.01005 tolerance-based fairness auditing, violation-cert vs sensitivity-screening, early-warning settings, COMPAS — queued) |
| 181 | A12/A8 | "reinforcement learning" AND "GPU" AND "vectorized" AND "simulation" | arXiv | 13 | 0 deep (training-efficiency enablers logged: GzDRL 2609.13243 reproducible Gazebo RL; rl-triton 2608.17641 Triton GPU kernels unified associative-scan for 7 RL credit-assignment algos; MAVEN GPU-vec meta-RL — robotics-adjacent, queue only) |
| 182 | A14/A9 | "conformal prediction" AND "distribution shift" AND "time series" | arXiv | 14 | 1 (2606.00690 DistMatch adaptive-binning seq-CP under shift, READ; 2610.02777 PID-Expert=already P2; Stocker 2511.xxxxx serial-dependence CP survey queued) |
| 183 | A6 | "false alarm" AND "warning" AND "trust" AND "evacuation" | arXiv | 0 | 0 (empty — alert-fatigue/cry-wolf human-trust not on arXiv under these terms; carry 2104.11422 cry-wolf ODE for P15) |
| 184 | A11 | "TinyML" AND "security" AND "edge" | arXiv | 16 | 1 (2609.27202 federated TinyML intrusion detection, cosine-LR stability 46.7→93.85% recall; AdvScan 2606.27704 power-analysis AE detection queued) |
| 185 | A5 | "watermarking" AND "generative" AND "detection" AND "robust" | arXiv | 362 | 1 (2610.06317 Impossibility→Auditable Compliance, EU AI Act Art.50, label-conditional conformal 3-way verdict; NeuMark-Native 2610.05215 + trigger-tag-attack queued) |
| 186 | A14/A8 | "out-of-distribution detection" AND "benchmark" AND "evaluation" → au:Hao Dong multimodal | arXiv | 105→4 | 1 (2605.06643 MMDG-Bench: ERM≈specialized, all degrade on missing-modality/corruption; MultiOOD NeurIPS24 lineage; Vmem-φ SNN-OOD + 2610.02413 probe-suffix queued) |
| 187 | A11/A13 | "differential privacy" AND "sensor" AND "deep learning" | arXiv | 4 | 1 (2605.01679 CA-ADP class-aware adaptive DP fall-detection, formal (ε,δ), protect minority-class gradient; ConvXformer 2510.19352 DP-inertial + AAAI24 face de-ID logged) |
| 188 | A9 | "video anomaly detection" AND "survey" | arXiv | 13 | 0 new (2508.14203 + 2507.21649 already P2; NSVAD ACM-CSUR 2024 Jing Liu et al. logged as seminal VAD survey) |
| 189 | A2/A11 | "water level" AND "camera" AND "flood" (strict +"deep learning"=0) | arXiv | 1 | 1 (2511.20936 passive LTE-power water-level, two-ray+CWT+lightweight NN, 0.8cm RMSE, survives probe loss — new low-cost river modality) |
| 190a | A4 | "debris flow" AND "seismic" AND "detection" | arXiv | 1 | 0 new (2401.13877 AscDAMs SLAM channel mapping NHESS-24-3075 — logged, geomorphology not precursor-detection) |
| 190 | A4/A6 | "acoustic" AND "early warning" AND "deep learning" | arXiv | 1 | 1 (2203.13313 Laurenti EPSL22: AE=stress fingerprint, AR forecast TTsF/TTeF, TTsF harder with creep — precursor/1v doctrine) |
| 191 | A1/A4 | "precipitation nowcasting" AND "deep learning" AND "extreme" | arXiv | 12 | 1 (2511.05471 TUPANN satellite-only GOES+IMERG physics-aligned nowcasting; REE-TTT 2601.01605 TTT + MTLDM latent-diffusion queued) |
| 192a | A3 | "InSAR" AND "time series" AND "deep learning" AND "deformation" | arXiv | 3 | 0 new (2509.18176 already P3; 2402.17069 elite-pixel-selection queued; 2012.13849 → author search) |
| 192 | A3/A4 | au:Rouet-Leduc AND "InSAR" | arXiv | 1 | 1 (2012.13849 Nature-Comms autoencoder untangles mm-scale deformation from atmospheric noise, 2mm detection, no fault prior — seminal InSAR precursor-extraction) |
| 193 | A1/A8 | "landslide" AND "susceptibility" AND "uncertainty" | arXiv | 5 | 1 (2604.16265 FL-MHSM Kerala+Nepal, soft-gating MoE > EF/LF, Brier calibration, zone-wise; 2601.07268 AlphaEarth-embeddings + Lombardo-Tanyas Bayesian-credible-interval queued) |
| 193a | A1 | 2601.07268 AlphaEarth-embeddings landslide susceptibility | arXiv HTML | — | NO-HTML both arxiv.org + ar5iv → ABS-only, NOT counted (queued) |
| 194 | A1/A4 | "flash flood" AND "forecasting" AND "machine learning" | arXiv | 9 | 1 (2609.34836 MW-Nowcast 6h ensemble extreme-precip, det-structure+generative-residual flow-matching, cost-loss/relative-economic-value metric, doubles warning time; Vicens-Miquel 2512.xxxxx residual-UQ 12h queued) |
| R1 | A1/A3 | 2606.16795 WaveDINO (re-open prior ABS entry) | arXiv HTML | — | BASELINE RE-STUDY (OQ-02): promoted ABS→FT-PARTIAL; InSAR atmospheric correction, note written; NOT a new-quota read (quota stays 32) |
| 195 | A7 | "conformal prediction" AND "time series" AND "distribution shift" | arXiv | 14 | 1 (2511.15838 AFOCP feature-space + attention OCP, up-to-88% narrower intervals, coverage preserved; 2610.02777 PID-Expert + 2606.00690 DistMatch already read) |
| 195a | A7 | ti:"Online Conformal Prediction" AND "feature space" | arXiv | 1 | 1 (→ 2511.15838 AFOCP id resolution, Simeone group) |
| 196 | A11 | "glacial lake" AND "outburst" AND "deep learning" | arXiv | 4 | 1 re-study (2608.12422 "Which Site and When" — OQ-02 BASELINE re-study to FT-PARTIAL, THE cornerstone CR-02 reality-check; neighbours IceWatch 2601.12330 + GLOFNet dataset 2510.xxxxx queued) |
| R2 | A11/A1/A4 | 2608.12422 "Which Site and When" (re-open prior ABS entry) | arXiv HTML | — | BASELINE RE-STUDY (OQ-02): promoted ABS→FT-PARTIAL; full note written; NOT a new-quota read (quota stays 33) |
| 197 | A3/A13 | "flood" AND "evacuation" AND "decision" | arXiv | 9 | triage: 2512.17785 (anticipatory flashflood warning, landscape-vuln + precip-forecast) = NO-HTML both hosts → ABS-only, NOT counted; 2608.26304 (two-stage stochastic evac optim, already CR-04-linked); Borowski/Stathopoulos social-influence evacuation = ABS human-response lead (crisis-informatics) |
| 198 | A5/A6 | "safe reinforcement learning" AND "shielding" AND "guarantee" | arXiv | 20 | 1 (2606.04634 Explainably Safe RL — hierarchical decision-tree shield explanations, risk categories, probabilistic guarantees; neighbour 2606.00270 Robust Shielding queued) |
| 199 | A14/A12 | "missing modality" AND "sensor" AND "robust" | arXiv | 48 | 1 (2607.24683 Co4Miss, Mena/Ienco — co-learning for missing ARBITRARY modalities, Co-Miss/FullCo, RS benchmarks; neighbour MacJEPA 2610.08192 temporal-outage queued-low) |
| 199a | A14 | ti:"Co4Miss" OR all:"Co4Miss" | arXiv | 1 | 1 (→ 2607.24683 id resolution) |
| 200 | A1/A3 | "InSAR" AND "deep learning" AND "landslide" | arXiv | 1 | 1 (2005.03221 Anantrasirichai/Biggs 2020 — FOUNDATIONAL InSAR-DL ancestor of WaveDINO; near-empty result set itself confirms thin InSAR+DL+landslide literature gap → SOTA open-gap note) |
| 201 | A1/A13 | "disaster" AND "misinformation" AND "social media" | arXiv | 8 | triage only (crisis-informatics already covered); top hits 2508.08592 (multimodal fact-check/OOC detection, ACM-MM25 GC), 2409.00004 (bias in social-media disaster-response) — logged as alert-integrity leads, not read |
| R3 | A11 | 2601.12330 IceWatch GLOF-forecast (re-open attempt) | arXiv/ar5iv | — | NO-HTML both hosts → ABS-only, NOT counted (quota stays 36) |
| R4 | A3 | 2402.17069 SAR elite-pixel selection (re-open attempt) | arXiv/ar5iv | — | arxiv.org/html 404 + ar5iv "Fatal error / No content" → NO-HTML/corrupted, NOT counted |
| 202 | A3/A7 | "flood forecasting" AND "uncertainty" AND "deep learning" | arXiv | 3 | 2412.11942 DRUM (diffusion probabilistic flood forecast, GRL 2025, doi 10.1029/2025GL115705) = NO-HTML both hosts → ABS-only NOTED (non-quota, see 2412.11942_DRUM_ABS.md); forecast-ceiling evidence. Others: CAS-Canglong SST (off-axis), Chandra Bayesian flood-prob (ABS lead) |
| 203 | A1/A3 | NHESS open-access browse (landslide/debris-flow EWS, non-arXiv per D-010) | nhess.copernicus.org | many | full-text body buried under site chrome (web_fetch middle-prune); art.26/4723 post-fire CA debris-flow = off-axis (California, not Himalaya) → not read. NHESS nav burns fetches; deprioritized vs targeted DOIs |
| 204 | A3/A7 | "flash flood" AND "nowcasting" | arXiv | 4 | top = MW-Nowcast 2609.34836 (already read #32); 2108.06868 Nowcasting-Nets (IMERG + PERSISTENCE baseline + RESIDUAL head, TGRS 2022) = NO-HTML both hosts → ABS-only NOTED (non-quota, see 2108.06868_NowcastingNets_ABS.md); 3rd independent corroboration of residual+persistence doctrine |
| 205 | A11/A1 | "glacial lake" AND "segmentation" AND "deep learning" | arXiv | 1 | 2512.24117 Himalayan GLOF-lake S1-SAR temporal-first segmentation (Adhikari 2025) = HTML OK → FT-PARTIAL READ #38 (WS8 bullseye). Single-hit result confirms thin GLOF-segmentation-DL literature (SOTA open-gap) |
| 206 | A1/A3 | "cloudburst" AND "Himalaya" | arXiv | 0 | ZERO hits → SOTA GAP: no arXiv DL/ML work on Himalayan cloudbursts specifically. Confirms cloudburst nowcasting is a genuine open niche (our WHEN layer has little direct prior art for this hazard) |
| 207 | A3 | "landslide susceptibility" AND "transfer learning" | arXiv | 0 | ZERO hits → cross-region susceptibility transfer under-studied on arXiv (gap; reinforces our domain-shift concern) |
| 208 | A3/A8 | "landslide susceptibility" AND "deep learning" | arXiv | 6 | 2608.19672 SAGE-XGBoost (data-scarcity; XGBoost+graph-embeddings BEATS deep rep-learning; AUC~0.97/0.95; +33pp over Spatial XGBoost) = NO-HTML both hosts → ABS-only NOTED (non-quota, see 2608.19672_SAGE_XGBoost_ABS.md), strong T1/GB-baseline corroboration; 2604.16265 FL-MHSM already read #(P3); SGCN-LSTM 2023 (ABS lead) |
| 209 | A4/A3 | "early warning" AND "conformal prediction" | arXiv | 5 | 2607.26854 TREA-Net (mechanistic prior + gated residual + two-scalar transfer + CP width -29.6% at coverage + TiRex ZERO-SHOT strongest baseline; data-scarce EW) = HTML OK → FT-PARTIAL READ #39; dengue domain but METHOD borrow (4th residual-doctrine corroboration; feeds P14Z zero-shot). Others: Conformal-Slip-Monitoring 2607.02124 (traction loss; adjacent), Luo 2021 robot CP (off-axis) |
| 210 | A1/A3 | "InSAR" AND "deep learning" AND "landslide" | arXiv | 1 | ONLY hit = 2005.03221 Anantrasirichai/Biggs (already read #36). Re-confirms thin InSAR+DL+landslide arXiv literature (SOTA open-gap; most such work is in NHESS/Remote-Sensing journals not arXiv) |
| 211 | A7/A11 | "flood" AND "foundation model" | arXiv | 47 | RICH axis. 2609.20441 Prithvi→EfficientViT edge-distillation ALREADY READ (note exists); 2609.14821 Decision-Oriented UQ for EO spatiotemporal FM (action-loss coverage; extreme-precip regret −23.4%) = HTML OK → FT-PARTIAL READ #40 (FLAGSHIP, our alarm-UQ doctrine); HASTE/Microsoft (damage mapping, open-source) + more in pool. 47-total shows flood-FM is a hot SOTA axis to mine further |
| 212 | A7/A3 | "precipitation nowcasting" AND "diffusion" | arXiv | 31 | HAZARD-CORE WHEN axis. 2608.30205 exPreCast-ENS conditional residual diffusion (4km→1km probabilistic ensemble + bias correction; real flood case studies; recovers 46.5% backbone-missed heavy rain at 0.73% new FA) = HTML OK → FT-PARTIAL READ #41 (5th residual-doctrine corroboration). PARKED to pool: NowcastDiT 2609.37038 (Diffusion-Transformer + RL timestep rewards, SOTA SEVIR/MRMS), PixelFlowCast (flow-matching SEVIR) |
| 213 | A8/P14Z | "zero-shot" AND "remote sensing" AND "classification" | arXiv | 50 | ZERO-SHOT axis (seeds NEW P14Z phase). Top hit OmniRSCLIP 2609.03391 (multi-source SAR/MSI/HSI CLIP, SSBD arbitrary-channel adaptation, OmniRS5M corpus, zero-shot classification) → PARKED to P14Z backlog (NOT read for P3 quota per scope); RS scene-classification survey (JKSU 2026) also noted. 50-total confirms zero-shot RS is a mature axis to mine in P14Z |
| 214 | A11 | "GLOF" OR "glacial lake outburst" | arXiv | 8 | AXIS EXHAUSTED (only 8 total; rest are unrelated math "GLOF"=generalized log orthogonal functions). Relevant ones ALL covered: 2608.12422 (baseline re-study R2), 2512.24117 (#38), 2510.10546 GLOFNet (ABS). Confirms SOTA gap: GLOF ML literature on arXiv is TINY → journal venues (NHESS/The Cryosphere/Remote Sensing) hold the rest |
| 215 | A3 | "landslide" AND "displacement" AND "forecasting" | arXiv | 1 | AXIS EXHAUSTED (only 1 total = 2605.17419 RMCL, already read #37). Confirms SOTA gap: operational landslide-displacement forecasting via DL barely on arXiv |
| 216 | A7 | "flash flood" AND "machine learning" | arXiv | 19 | Top hit MW-Nowcast 2609.34836 ALREADY READ (#R baseline / already noted). Modest axis; remaining mostly streamflow/hydro-ML not Himalaya-specific. No new quota read taken |
| 217 | A1/A2 | "SAR" AND "foundation model" AND "self-supervised" | arXiv | 17 | CR-01 GOLDMINE. SAR2Agri 2608.11142 (SAR-intensity SSL, temporal pretext TD/FF + masking + curriculum; SICKLE 84.9% IoU, +15.3pt vs optical) = HTML OK → FT-PARTIAL READ #42. Maps SAR-FM landscape for P7 encoder trade: TerraMind, CopernicusFM, SAR-JEPA, SARMAE, SAR-W-MixMAE, SAMBA 2606.31668 (Mamba), OceanSAR-1 — all PARKED→P7. 17-total = rich SAR-FM axis |
| 218 | A3 | "graph neural network" AND "landslide" | arXiv | 5 | SMALL axis. GNN-rP 2509.10362 (GNN + r-Pareto EVT tail-risk for extreme-precip risk zoning; IMERG+CMIP6; compound rain→flood+landslide; beats 2 baselines) = HTML OK → FT-PARTIAL READ #43 (FIRST EVT/tail-risk paper, opens new thread). PARKED→pool: GTS_Forecaster 2509.10560 (geodetic GNSS/SSH DL forecasting toolbox), GNS granular-flow GNN surrogate (Choi&Kumar 2023, debris-flow dynamics) |
| 219 | A5 | "reinforcement learning" AND "evacuation" AND "disaster" | arXiv | 5 | SMALL axis. Top hit GREAT-EER 2602.14676 (Bus Evacuation Orienteering, deep-RL+graph, San Francisco) ALREADY READ (P3). Others off-axis (UAV edge-compute 2501.15305, air-traffic evac 2021). No new quota read; confirms thin RL-evacuation arXiv coverage (WS5 gap) |
