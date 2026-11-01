# 19a_REFERENCES_physics_pinn -- TRINETRA reference catalogue (part of chapter 19)

> Row-level truth: `analysis/02_paper_ledger.csv`. Index, counts, MUST-READ TOP-30, dataset cross-index and BibTeX live in `docs/19_REFERENCES_FULL.md`.

> **Residual-identifier risk (per _CANON SS7):** every identifier below is a real ledger row, but identifiers were *subagent-reported during a web_search outage and were NOT independently re-fetched this pass*. No entry claims a resolved identifier unless its Verification line says so.

> Read-depth tags are copied verbatim from the ledger: FT / FT-PARTIAL / ABS / ABS-CANONICAL / FT-REF.


---

## Theme: Physics / combustion / geo-hazard physics  (`REF-PHY-*`, 155 entries)

_Primary consumer: WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility. The ledger axis/WS code that mapped each paper into this theme is printed per entry for traceability._

#### REF-PHY-001 | 2107.07687
- arXiv/DOI: arXiv:2107.07687
- Authors: Chen; Sanz-Alonso; Willett
- Title: Auto-differentiable Ensemble Kalman Filters
- Year / Venue: 2021 / arXiv (stat.ML)
- Read depth: ABS | local note: no | ledger axis/WS: A4 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: EnKF + ML to learn unknown dynamics
- Takeaway for TRINETRA: AD-EnKF blends ensemble Kalman filtering (scales to high-dim state recovery) with automatic differentiation to train surrogate models of UNKNOWN dynamics; beats EM/particle-filter hybrids on Lorenz-96, easy to implement.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-002 | 2412.14318
- arXiv/DOI: arXiv:2412.14318
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Long-time accuracy of ensemble Kalman filters for chaotic and machine-learned dynamical systems
- Year / Venue: 2024 / arXiv (math/stat)
- Read depth: ABS | local note: no | ledger axis/WS: A4 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: EnKF long-horizon error bounds; ML-surrogate caveat
- Takeaway for TRINETRA: Establishes conditions under which EnKF estimation error stays small over LONG horizons for partially-observed chaotic systems (Navier-Stokes, Lorenz), including with ML surrogate dynamics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-003 | 2510.08488
- arXiv/DOI: arXiv:2510.08488
- Authors: Yang; Ji; Lonzarich; Song; Shen
- Title: Diffusion-Based Probabilistic Modeling for Hourly Streamflow Prediction and Assimilation (h-Diffusion)
- Year / Venue: 2025 / arXiv (physics.geo-ph)
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: hourly probabilistic streamflow + data assimilation
- Takeaway for TRINETRA: HOURLY flood peaks are distinctly higher than daily - critical for warnings; MTS-LSTM lacks probabilistic forecasts/assimilation.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-004 | 2512.12183
- arXiv/DOI: arXiv:2512.12183
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: HydroDiffusion: Diffusion-Based Probabilistic Streamflow Forecasting with a State Space Backbone
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: diffusion + state-space long-range streamflow
- Takeaway for TRINETRA: Improves on LSTM-backbone diffusion streamflow models (single-step objectives, poor long-range) with a STATE-SPACE (Mamba-style) backbone for coherent multi-lead probabilistic forecast trajectories + strong early flood-warning skill.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-005 | 2401.13877
- arXiv/DOI: arXiv:2401.13877
- Authors: Wang; Lu; Qin; Huang; Kong; Shen
- Title: AscDAMs: Advanced SLAM-based channel detection and mapping system
- Year / Venue: 2024 / NHESS
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: SLAM channel mapping for debris-flow gullies
- Takeaway for TRINETRA: High-resolution channel topography/deposit conditions are the prior challenge for channelized debris-flow study; satellite/drone struggle to see interior of long-deep gullies (Wenchuan region); SLAM fails there due to atypical features + vi...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-006 | 2505.08553
- arXiv/DOI: arXiv:2505.08553
- Authors: Nguyen; Bhattacharya; Wong; Didry; Phan; Tamisier; Matgen
- Title: Towards Digital Twin in Flood Forecasting with Data Assimilation of Satellite EO (Alzette)
- Year / Venue: 2025 / Remote Sensing (MDPI)
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: particle-filter DA of Sentinel-1 into LISFLOOD-FP, 30-day
- Takeaway for TRINETRA: Digital-Twin flood PoC assimilates Sentinel-1 flood-probability maps via a PARTICLE-FILTER data-assimilation process into a high-res LISFLOOD-FP hydrodynamic model + GloFAS products, giving daily forecasts up to 30 days with reduced uncerta...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-007 | 2512.23964
- arXiv/DOI: arXiv:2512.23964
- Authors: Acosta; Herath; Lim; Saha; Rasnayaka; Marshall
- Title: DUALFloodGNN: Physics-informed Graph Neural Network for Operational Flood Modeling
- Year / Venue: 2026 / IJCAI-ECAI 2026
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: physics-informed GNN, fast accurate flood hydrodynamics
- Takeaway for TRINETRA: Physics-based flood models are accurate but too slow for operations; DUALFloodGNN embeds physical constraints at GLOBAL and LOCAL scales via explicit loss terms, jointly predicts node water-volume + edge flow in a shared message-passing net...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-008 | 2606.04143
- arXiv/DOI: arXiv:2606.04143
- Authors: Gebre; Talreja; Hashemi-Beni
- Title: Physics-Informed Machine Learning for Short-Term Flood Prediction
- Year / Venue: 2026 / IGARSS 2026
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: Trend-Alignment physics loss on LSTM, data-scarce+extreme
- Takeaway for TRINETRA: Pure data-driven LSTMs give physically inconsistent flood predictions and fail in data-scarce/extreme settings; proposes a PIML framework adding a Trend-Alignment constraint (penalizes directional inconsistency between precipitation and dis...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-009 | 2510.10546
- arXiv/DOI: arXiv:2510.10546
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: GLOFNet -- A Multimodal Dataset for GLOF Monitoring and Prediction
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: yes | ledger axis/WS: A11 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: multimodal GLOF dataset: Sentinel-2 + ITS_LIVE + physical precursors
- Takeaway for TRINETRA: GLOFs are rare but destructive; predictive research is hindered by FRAGMENTED, UNIMODAL data and most prior work only does POST-EVENT mapping; GLOFNet is a multimodal dataset focused on Shisper Glacier (Karakoram) integrating Sentinel-2 mul...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-010 | 2608.12422
- arXiv/DOI: arXiv:2608.12422
- Authors: Kahn; Arjel; Adhikari; Sherpa; Pope
- Title: Which Site, and When: A Free-Satellite-Data Test of Himalayan Glacial Lake Bursts, Landslides, and Ice Floods
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: yes | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: CRITICAL reality-check: honest spatial-CV collapses AUC; DL does not beat GB
- Takeaway for TRINETRA: Nearly a direct reality-check for TRINETRA's whole thesis. Uses the SAME free signals (InSAR moraine-dam deformation = WHICH lake; antecedent satellite weather = WHEN) for three hazards (moraine/ice-dam bursts, rainfall landslides, small gl...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-011 | 2606.29134
- arXiv/DOI: arXiv:2606.29134
- Authors: Thasma; Ho; Mostafavi
- Title: Beyond Backscatter: AlphaEarth Land-Cover Priors for Rapid SAR Flood Segmentation Across Foundation Backbones
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: single-temporal SAR flood ambiguity; land-context priors; per-event eval mandatory
- Takeaway for TRINETRA: Rapid flood mapping: optical often unusable during floods, and SINGLE-TEMPORAL SAR is AMBIGUOUS - new inundation, permanent water, and other smooth surfaces give similar backscatter.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-012 | 2307.07123
- arXiv/DOI: arXiv:2307.07123
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Improved Flood Insights: Diffusion-Based SAR to EO Image Translation
- Year / Venue: 2023 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: diffusion SAR->EO translation for flood interpretability
- Takeaway for TRINETRA: Proposes a diffusion-based SAR->EO (optical) image translation to make SAR flood observations more human-interpretable, since SAR is hard to read and optical is cloud-blocked during floods.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-013 | 10.1109/IGARSS46834.2022.9883132
- arXiv/DOI: DOI:10.1109/IGARSS46834.2022.9883132
- Authors: Yadav; Nascetti; Ban
- Title: Bi-temporal SAR flood detection network (Sen1Floods11)
- Year / Venue: 2022 / IGARSS 2022
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: bi-temporal SAR beats uni-temporal flood detection by 6% IoU
- Takeaway for TRINETRA: A bi-temporal SAR flood-detection network evaluated on Sen1Floods11; combining PRE+POST event SAR with an effective architecture beats the uni-temporal SOTA by 6% IoU.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-014 | 2310.04428
- arXiv/DOI: arXiv:2310.04428
- Authors: Sharma
- Title: Avalanche Prediction and Dynamics using Temperature Variance Grain Size Variance and Flow Regimes
- Year / Venue: 2023 / arXiv (physics.geo-ph)
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: SVM avalanche forecasting from met+snowpack; MPM flow regimes
- Takeaway for TRINETRA: Combines Material Point Method (MPM) modelling of snow-avalanche flow regimes with SVM forecasting using meteorological + snowpack variables (snowfall, accumulation, rain interaction, snowdrift, snowpack mechanics, temperature profile); not...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-015 | 1901.04695
- arXiv/DOI: arXiv:1901.04695
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Statistical models for short and long term forecasts of snow depth
- Year / Venue: 2019 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: zero-inflated gamma regression for snow depth forecasting
- Takeaway for TRINETRA: Statistical snow-depth forecast models: short-term (given reliable temp+precip forecasts) with covariates entered NONLINEARLY following snowfall/aging/melting physics, and because many observations are zero snow depth, uses a ZERO-INFLATED...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-016 | 2305.05218
- arXiv/DOI: arXiv:2305.05218
- Authors: Choi; Kumar
- Title: Graph Neural Network-based surrogate model for granular flows
- Year / Venue: 2023 / arXiv (physics.geo-ph)
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: GNN surrogate learns granular-flow (landslide/debris-flow) dynamics, fast forward model
- Takeaway for TRINETRA: GNN surrogate for granular-flow dynamics (landslides, debris flows), modelling the dynamic particle rearrangement and complex solid<->fluid-like transitions; learns next-step evolution from current graph state, giving a fast differentiable...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-017 | 2509.10362
- arXiv/DOI: arXiv:2509.10362
- Authors: Wang; Wu; Bi
- Title: Spatial Modeling and Risk Zoning of Global Extreme Precipitation via Graph Neural Networks and r-Pareto Processes
- Year / Venue: 2025 / arXiv (stat.AP)
- Read depth: ABS | local note: yes | ledger axis/WS: A3 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: GNN + r-Pareto EVT risk-zoning on IMERG; nonstationary spatial tail dependence
- Takeaway for TRINETRA: Hybrid GNN + r-Pareto-process (GNN-rP) framework for spatial EXTREME-precipitation modelling + risk zoning; learns nonlinear NONSTATIONARY dependence from precipitation-derived spatial graphs and applies a data-driven TAIL functional for jo...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-018 | 2105.13133
- arXiv/DOI: arXiv:2105.13133
- Authors: Boujoudar; Beljadid; Taik
- Title: Modeling of unsaturated flow through porous media using meshless methods
- Year / Venue: 2021 / arXiv (math.NA)
- Read depth: ABS | local note: no | ledger axis/WS: A4 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: meshless RBF + Kirchhoff + Picard for Richards eqn infiltration
- Takeaway for TRINETRA: Solves the RICHARDS equation (unsaturated water flow in soils) with a MESHLESS localized radial-basis-function method + Kirchhoff transformation, Picard iterations for the nonlinearity; the difficulty is the nonlinear unsaturated hydraulic...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-019 | 1507.07837
- arXiv/DOI: arXiv:1507.07837
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A study on iterative methods for solving Richards' equation
- Year / Venue: 2015 / arXiv (math.NA)
- Read depth: ABS | local note: no | ledger axis/WS: A4 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: linearization/iterative schemes (Newton/Picard/L-scheme) for degenerate Richards eqn
- Takeaway for TRINETRA: Studies LINEARIZATION methods (backward-Euler in time, Galerkin FE in space) for efficiently solving the Richards equation - a DEGENERATE elliptic-parabolic equation for saturated/unsaturated porous-media flow; compares iterative schemes (e...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-020 | 2102.06491
- arXiv/DOI: arXiv:2102.06491
- Authors: Zoumpekas; Puig; Salamo; Garcia-Selles; Blanco Nunez; Guinau
- Title: End-to-End Intelligent Framework for Rockfall Detection
- Year / Venue: 2021 / Int. J. Intelligent Systems (DOI 10.1002/int.22557)
- Read depth: ABS | local note: yes | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: ML pipeline detects rockfall clusters in TLS point clouds; EXTREME imbalance needs heavy resampling
- Takeaway for TRINETRA: End-to-end ML framework to detect rockfall events in Terrestrial-Laser-Scanner point clouds (replacing tedious manual multi-temporal visual comparison); because rockfall is EXTREMELY imbalanced, it benchmarks many resampling techniques + mo...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-021 | 2210.12853
- arXiv/DOI: arXiv:2210.12853
- Authors: Ko; Lee; Hwang; Shin
- Title: Deep-Learning-Based Precipitation Nowcasting with Ground Weather Station Data and Radar Data
- Year / Venue: 2022 / SSTDM-22
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: fuse SPARSE ground-station obs with radar -> +5.7% CSI heavy-rain 1-6h nowcast
- Takeaway for TRINETRA: Most DL precip-nowcasting uses only radar/satellite images and ignores SPARSE ground-station observations; proposes ASOC, an attentive module capturing temporal dynamics + contextual relations among multiple weather stations, bolt-on to any...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-022 | 2106.15119
- arXiv/DOI: arXiv:2106.15119
- Authors: Rundeddu; Lizarraga; Buscarnera
- Title: Hybrid stochastic-mechanical modeling of precipitation thresholds of shallow landslide initiation
- Year / Venue: 2021 / arXiv (physics.geo-ph)
- Read depth: ABS | local note: no | ledger axis/WS: A4 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: derives ID thresholds from physics + stochastic params (not empirical fit); Ks/slope/suction sensitivities
- Takeaway for TRINETRA: Proposes a HYBRID STOCHASTIC-MECHANICAL approach to compute rainfall intensity-duration (ID) thresholds for shallow-landslide initiation from a physically-based triggering model with selected parameters treated as correlated ALEATORY variab...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-023 | 1706.03458
- arXiv/DOI: arXiv:1706.03458
- Authors: Shi; Gao; Lausen; Wang; Yeung; Wong; Woo
- Title: Deep Learning for Precipitation Nowcasting: A Benchmark and A New Model (TrajGRU)
- Year / Venue: 2017 / NIPS 2017
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: precip nowcasting input
- Takeaway for TRINETRA: TrajGRU learns location-variant recurrence, beats ConvLSTM; HKO benchmark + eval protocol.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-024 | 2203.13263
- arXiv/DOI: arXiv:2203.13263
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Precipitation Nowcasting using Deep Neural Network
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: precip nowcasting input
- Takeaway for TRINETRA: DNN precipitation nowcasting (fast vs NWP). Secondary reference for TRINETRA's near-real-time rainfall input; nowcasting is faster but shorter-horizon than NWP (lead-time tradeoff informs RL reward).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-025 | 1911.05219
- arXiv/DOI: arXiv:1911.05219
- Authors: Raman; Liu
- Title: An investigation of the Brumadinho Dam Break with HEC-RAS simulation
- Year / Venue: 2019 / arXiv (physics.comp-ph)
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: dam-break / runout inundation
- Takeaway for TRINETRA: HEC-RAS mudflow model on SRTM DEM reproduces observed Brumadinho tailings-dam flood extent.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-026 | 2209.08729
- arXiv/DOI: arXiv:2209.08729
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Data-driven and ML-based prediction of wave propagation behavior in dam-break flood
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: dam-break surrogate
- Takeaway for TRINETRA: Reservoir-computing (RC-ESN) surrogate for 1D dam-break Saint-Venant dynamics from minimal data.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-027 | 2605.02153
- arXiv/DOI: arXiv:2605.02153
- Authors: Talreja; Gebre; Hashemi Beni
- Title: Cross-Polarization Fusion of VV and VH SAR Observations for Improved Flood Mapping
- Year / Venue: 2026 / IGARSS 2026
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: SAR flood extent
- Takeaway for TRINETRA: VV+VH fusion beats single-pol SAR for flood mapping, esp. vegetated/heterogeneous terrain. TRINETRA should fuse both Sentinel-1 polarizations for flood-extent, not single-pol; concrete accuracy gain + Himalaya vegetation relevance.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-028 | 2411.04153
- arXiv/DOI: arXiv:2411.04153
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Urban Flood Mapping Using Satellite SAR Data: A Review
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: SAR flood review
- Takeaway for TRINETRA: Review of SAR urban-flood methods/datasets; SAR all-weather day-night advantage + method-selection guidance. Scopes TRINETRA's SAR flood-mapping choices + known failure modes (layover/shadow in terrain) relevant to Himalayan valleys.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-029 | 2605.17419
- arXiv/DOI: arXiv:2605.17419
- Authors: Ozeki; Rizk; Yamaguchi
- Title: Learning Displacement-Robust Representations for Landslide Early Warning under Rainfall Forecast Uncertainty (RMCL)
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: yes | ledger axis/WS: A3 | phase: n/r | re-cited 4x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: LEWS forecast-uncertainty robustness
- Takeaway for TRINETRA: MOST landslide predictors assume ACCURATE rainfall; operational LEWS use FORECASTS with spatial displacement that degrades accuracy.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-030 | 2401.13695
- arXiv/DOI: arXiv:2401.13695
- Authors: Choi; Kumar
- Title: Inverse analysis of granular flows using differentiable graph neural network simulator
- Year / Venue: 2024 / arXiv (physics.geo-ph)
- Read depth: ABS | local note: yes | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: runout surrogate (BASELINE-dup)
- Takeaway for TRINETRA: NOTE: already in local corpus; deduped, NOT counted as new. Differentiable GNS for granular-flow inverse runout; baffle design. Listed only to mark dedup.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-031 | 2404.15860
- arXiv/DOI: arXiv:2404.15860
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Modeling liquefaction-induced runout of a tailings dam using hybrid FEM-MPM
- Year / Venue: 2024 / arXiv (physics.geo-ph)
- Read depth: ABS | local note: yes | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: runout physics
- Takeaway for TRINETRA: Hybrid finite-element + material-point method for liquefaction-induced flow-slide runout. High-fidelity runout reference relevant to TRINETRA's debris/mud runout modeling (physics-gate validation anchor; MPM for large deformation).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-032 | 2508.01426
- arXiv/DOI: arXiv:2508.01426
- Authors: Ni; Zhang; Liu
- Title: UniExtreme: A Universal Foundation Model for Extreme Weather Forecasting
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: extreme-weather FM
- Takeaway for TRINETRA: FM with learnable Beta-distribution spectral filters + region-specific Event-Prior Augmentation; beats SOTA on extreme + general weather.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-033 | 1904.07213
- arXiv/DOI: arXiv:1904.07213
- Authors: Corral; Berenguer; Sempere-Torres; Poletti; Silvestro; Rebora
- Title: Comparison of two early warning systems for regional flash flood hazard forecasting
- Year / Venue: 2019 / J. Hydrology
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: flash-flood EWS comparison
- Takeaway for TRINETRA: Compares rainfall-based (ERICHA) vs distributed rainfall-runoff (Flood-PROOFS) flash-flood EWS on Liguria; agree for large catchments/return periods, DIVERGE for small catchments.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-034 | 2012.11154
- arXiv/DOI: arXiv:2012.11154
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FlowDB: a large scale precipitation, river, and flash flood dataset
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: flash-flood dataset
- Takeaway for TRINETRA: Large-scale precip+river+flash-flood dataset (no prior dataset existed for ML flash-flood forecasting).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-035 | 2510.13012
- arXiv/DOI: arXiv:2510.13012
- Authors: Benfanich; Bourgault; Beljadid
- Title: A finite element method using a bounded auxiliary variable for solving the Richards equation
- Year / Venue: 2025 / J. Comp. Physics
- Read depth: ABS | local note: no | ledger axis/WS: A4 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: Richards eq. numerics
- Takeaway for TRINETRA: Stable FEM for Richards equation handling BOTH dry and fully-saturated zones + LAYERED soils without regularization; van Genuchten/Haverkamp.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-036 | 2602.11194
- arXiv/DOI: arXiv:2602.11194
- Authors: Movasat; Tomac
- Title: Predicting post-wildfire mudflow onset using ML on multi-parameter experimental data
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: debris-flow onset timing + I-D sensitivity
- Takeaway for TRINETRA: Flume experiments + ML (MLR/LR/SVC/K-means/PCA) on rain-intensity, slope, water-entry value, grain-size D50 to predict debris-flow onset.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-037 | 2512.09251
- arXiv/DOI: arXiv:2512.09251
- Authors: Maurya; Kaushik; Tellman
- Title: GLACIA: Instance-Aware Positional Reasoning for Glacial Lake Segmentation via Multimodal LLM
- Year / Venue: 2025 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: MLLM glacial-lake seg + interpretable reasoning
- Takeaway for TRINETRA: First framework coupling an LLM with segmentation for glacial-lake mapping: produces masks PLUS human-interpretable spatial-reasoning text + a GLake-Pos QA dataset; mIoU 87.30 beats CNNs (78.6-79.0), ViTs (69-82), geo-FMs (76-87), reasoning...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-038 | 2609.17175
- arXiv/DOI: arXiv:2609.17175
- Authors: Camilletti; Franch; Tomasi; Cristoforetti
- Title: IRENE: Convolutional GRU Ensemble for Radar Precipitation Nowcasting over Italy
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A3 | phase: P2
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P2] probabilistic nowcast eval (T5)
- Takeaway for TRINETRA: Multi-scale ConvGRU encoder-forecaster + stochastic ensemble; afCRPS loss; beats STEPS/DGMR on CRPS at all leads + better rank histograms. MAE edge only first 90min.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-039 | 2605.20167
- arXiv/DOI: arXiv:2605.20167
- Authors: Koli; Jely; Alim; Hossen
- Title: HaorFloodAlert: 72-Hour ML Early Warning System for Flash Floods in Bangladesh Haor Wetlands
- Year / Venue: 2026 / arXiv (cs.AI)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A3 | phase: P2 | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P2] operational TRINETRA analog (T1/T2/T3)
- Takeaway for TRINETRA: Free data (Sentinel-1 + rainfall + soil moisture + modeled upstream Barak/India signal ~36h lead), RF+XGBoost, LOOCV 77 real-SAR events 90.9% acc/0.939 AUC, live 10-day run raised alert ~3 days early, Bengali SMS/WhatsApp last-mile, public...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-040 | 2610.06241
- arXiv/DOI: arXiv:2610.06241
- Authors: Silva; Silva; Moreira; Luz
- Title: Few-Shot Prototype-Head On-Device ECG Personalization on PSoC6
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A11 | phase: P3 | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P3] IoT/TinyML WS7
- Takeaway for TRINETRA: 1314-param 1D-CNN frozen feature extractor + closed-form class-mean prototypes in 32-D; NO backprop/optimizer; 11.39ms/beat, 5.2KB flash, 22.2KB SRAM on PSoC6 M4F; macro-F1 0.635→0.797 @10-shot.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-041 | 2609.18555
- arXiv/DOI: arXiv:2609.18555
- Authors: Lawenda; Krasicka; Caballero; Torres; Szustak
- Title: Interpretable Patch-Based DL for Wildfire Spread from Ensemble Simulations
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A4 | phase: P3
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P3] physics/interp CR-02 5th domain
- Takeaway for TRINETRA: DL surrogate of Rothermel/FARSITE sim; only fuel-load strong (r=0.27, −21% err); conv models rely on front-DISTANCE geometry (occlusion: fire-mask importance 0.121→0.248), env channels flat; terrain+fuel+wind alone MCC 0.42 (second-order);...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-042 | 2608.06876
- arXiv/DOI: arXiv:2608.06876
- Authors: Haider; Kundroo; Eom; Park; Chen; Kim
- Title: FedVAR: Prototype-Aligned Federated Framework for Video Anomaly Recognition
- Year / Venue: 2026 / Future Generation Computer Systems
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A11 | phase: P3
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P3] privacy/federated WS4; normal=geometry cluster
- Takeaway for TRINETRA: Weakly-supervised federated VAR on frozen VLM; fixes semantic misalignment via a global normality PROTOTYPE that re-centers each client's visual+textual features; raw video stays local; non-IID/unseen-domain/novel-class.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-043 | 2609.27202
- arXiv/DOI: arXiv:2609.27202
- Authors: Park; Bae; Ramachandran Prabhu; Saha; Li
- Title: Reliable Federated TinyML Deployment for IoT Security
- Year / Venue: 2026 / arXiv (cs.CR)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A11 | phase: P3
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P3] WS7 node security + federated privacy
- Takeaway for TRINETRA: Federated Learning + TinyML (KD+structured-pruning+quantization) for on-device IoT intrusion detection on MCU class; raw data stays local.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-044 | 2605.01679
- arXiv/DOI: arXiv:2605.01679
- Authors: Sana
- Title: Class-Aware Adaptive Differential Privacy for Sensor-Based Fall Detection (CA-ADP)
- Year / Venue: 2026 / arXiv (cs.CR)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A11 | phase: P3
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P3] privacy/DP + rare-event doctrine
- Takeaway for TRINETRA: Class-Aware Adaptive DP: scale DP-SGD gradient noise by batch class composition — LESS noise on rare critical class (fall), full noise on majority (ADL); noise range [σ(1-α),σ]; formal (ε,δ)-DP + privacy-utility analysis.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-045 | 2203.13313
- arXiv/DOI: arXiv:2203.13313
- Authors: Laurenti; Tinti; Galasso; Franco; Marone
- Title: Deep Learning for Laboratory Earthquake Prediction & AR Forecasting of Fault-Zone Stress
- Year / Venue: 2022 / EPSL 598 117825
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A4 | phase: P3
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P3] precursor forecasting seminal; Fukuzono 1/v + forecast-residual
- Takeaway for TRINETRA: AE energy = fingerprint of fault shear stress. LSTM+CNN predict labquakes under creep/aperiodic/slow-fast. Two targets: TTsF (onset) + TTeF (end).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-046 | 2012.13849
- arXiv/DOI: arXiv:2012.13849
- Authors: Rouet-Leduc; Jolivet; Dalaison; Johnson; Hulbert
- Title: Autonomous Extraction of mm-scale Deformation in InSAR Time Series Using Deep Learning
- Year / Venue: 2020 / Nature Communications (10.1038/s41467-021-26254-3)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A3 | phase: P3
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P3] InSAR precursor seminal; denoising-AE anomaly primitive
- Takeaway for TRINETRA: Deep auto-encoder untangles ground deformation from atmospheric propagation-delay noise in InSAR time series, AUTONOMOUSLY (no fault location/slip prior).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-047 | 2512.24117
- arXiv/DOI: arXiv:2512.24117
- Authors: Adhikari; Regmi; Shrestha
- Title: Targeted Semantic Segmentation of Himalayan Glacial Lakes Using Time-Series SAR: Towards Automated GLOF Early Warning
- Year / Venue: 2025 / arXiv (eess.IV/cs.CV)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A11 | phase: P3 | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P3] WS8 BULLSEYE: Himalayan GLOF EWS pipeline, Sentinel-1 SAR, temporal-first
- Takeaway for TRINETRA: End-to-end automated DL pipeline for targeted monitoring of HIGH-RISK HIMALAYAN glacial lakes via time-series Sentinel-1 SAR.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-048 | 2607.26854
- arXiv/DOI: arXiv:2607.26854
- Authors: Shukla; Panja; Chakraborty; Hens
- Title: TREA-Net: A Transferable Residual Epidemiological Adaptation Network for Dengue Incidence Forecasting
- Year / Venue: 2026 / arXiv (cs.LG/q-bio.QM)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A3 | phase: P3
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P3] METHOD BORROW: mechanistic-prior + gated-residual + two-scalar transfer + conformal + zero-shot FM; data-scarce early warning
- Takeaway for TRINETRA: Lightweight portable EW framework for DATA-SCARCE regions. ETSIR mechanistic prior + NN-invariant GATED RESIDUAL neural correction (predict structure mechanistically, learn gated residual) + multi-source training + TWO-SCALAR (gamma,beta) t...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-049 | 2609.14821
- arXiv/DOI: arXiv:2609.14821
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Decision-Oriented Uncertainty Quantification for Risk Control in Earth System Spatiotemporal Foundation Models
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A4 | phase: P3
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P3] FLAGSHIP: decision-oriented UQ = our cost-sensitive-alarm doctrine, published
- Takeaway for TRINETRA: Makes UQ DECISION-ORIENTED (tuned to downstream decision cost) for EO spatiotemporal foundation models.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-050 | 2606.21773
- arXiv/DOI: arXiv:2606.21773
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Decision-Focused Learning: When and Why Traditional Prediction Models Fail
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A4 | phase: P4
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P4] RESOLVES C-04/C-11: 'better prediction != better decision' consolidated
- Takeaway for TRINETRA: DFL review/framework: taxonomy of SPO (smart predict-then-optimize) and surrogate losses; mappings x->w* (end-to-end), x->l (predictive), c->w*(c) (optimize-given-cost); statistical challenges of stochastic-LP objectives.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-051 | 2512.14221
- arXiv/DOI: arXiv:2512.14221
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Weighted Conformal Prediction Provides Adaptive and Valid Mask-Conditional Coverage for General Missing Data Mechanisms
- Year / Venue: 2025 / arXiv (stat.ML)
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A4 | phase: P4
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P4] CLOSES CR-04 missingness edge: mask-conditional valid CP
- Takeaway for TRINETRA: Weighted/reweighted conformal after multiple imputation gives Mask-Conditional Valid (MCV) coverage under GENERAL (not just MCAR) missingness; preimpute-mask-then-correct; MCV coverage > marginal coverage when a modality is absent, with nar...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-052 | 2510.12328
- arXiv/DOI: arXiv:2510.12328
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-Informed GAT with Season-aware GPD/POT for Extreme Rainfall Forecasting (Thailand)
- Year / Venue: 2025 / arXiv (ABS/NO-HTML)
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: P4
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P4] NON-QUOTA 2nd EVT source: closes C-06 single-point-of-failure
- Takeaway for TRINETRA: Physics-Informed Graph Attention Network + Attention-LSTM on a gauge graph with orographic-precipitation physics edges; Spatial Season-aware Generalized-Pareto POT tail mapping; competitive with ECMWF SEAS5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-053 | 2610.07232
- arXiv/DOI: arXiv:2610.07232
- Authors: Authors (UCSC)
- Title: Benchmarking Time Series Foundation Models for Load Forecasting Under Covariate Uncertainty
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A3 | phase: P4
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P4] FEEDS P14Z + stress-tests C-07/C-02: FMs help ONLY with good covariates
- Takeaway for TRINETRA: 4 TSFM (incl Chronos-2) vs 4 train-from-scratch (incl TimesNet, Informer) on 3 real datasets (ISO-NE, NAU, CAISO) with injected covariate-forecast noise lambda in {0,0.5,1,5}.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-054 | 2608.15261
- arXiv/DOI: arXiv:2608.15261
- Authors: Zhang; Wang; Wang; Li; Zuo
- Title: Boundary-Aligned Contribution Routing for Robust Optical-SAR Object Detection
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A11 | phase: P4
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P4] C-08 mechanism: more modalities != better; route before mixing
- Takeaway for TRINETRA: Optical-SAR fusion with task-conditioned contribution routing applied BEFORE the first cross-modal feature-value mixing (Feature Router near input + Dual-Statistic Semantic Router for dual-backbone late fusion); learned from detection super...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-055 | 2609.16707
- arXiv/DOI: arXiv:2609.16707
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Predictability-Guided Multiscale Probabilistic Forecasting of Wind Direction under Extreme Shear
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT | local note: no | ledger axis/WS: A3 | phase: P4
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P4] C-13/C-06: predictability decays per scale; FMs lag at the extremes
- Takeaway for TRINETRA: Directional (S^1) multi-horizon probabilistic forecasting under extreme wind-shear; shows predictability DECAYS AT DIFFERENT RATES across temporal scales -> uncertainty is regime- and scale-dependent; foundation and discrete models suffer m...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-056 | 2604.16663
- arXiv/DOI: arXiv:2604.16663
- Authors: Kowsher; Zhan; Chen
- Title: A Benchmark Study of Segmentation Models and Adaptation Strategies for Landslide Detection
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: P5
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P5] WS1/WS6: PEFT (LoRA/AdaLoRA) = -95% trainable params ~ full-FT accuracy
- Takeaway for TRINETRA: On GDCLD (Globally Distributed Coseismic Landslide Dataset): CNN vs transformer-seg vs large pretrained FMs under one training/eval protocol; full-FT vs LoRA vs AdaLoRA; transformers strong; LoRA/AdaLoRA reduce trainable params up to 95% wi...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-057 | 2409.12635
- arXiv/DOI: arXiv:2409.12635
- Authors: Pan; Wang; Huan
- Title: EFA-YOLO: An Efficient Feature Attention Model for Fire and Flame Detection
- Year / Venue: 2024 / arXiv (cs.CV) CC-BY
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: P6 | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P6] vision: lightweight flame detector
- Takeaway for TRINETRA: SOURCE-REPORTED 1.4M params / 4.6 GFLOPs / 22.19 ms per image on DESKTOP CPU (not MCU); claimed mAP + ~88x speed + 94.6% fewer params vs YOLOv5/8/9/10.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-058 | 2508.14597
- arXiv/DOI: arXiv:2508.14597
- Authors: Mahala; Khan; Kumar
- Title: Reliable Smoke Detection via Optical-Flow-Guided Feature Fusion and Transformer Uncertainty
- Year / Venue: 2025 / arXiv (cs.CV) CC-BY
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: P6 | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P6] vision: uncertainty for early smoke
- Takeaway for TRINETRA: Monocular smoke detection fusing optical-flow motion + appearance (GMM) into a Shifted-Windows Transformer with aleatoric+epistemic uncertainty head; claims better generalization/robustness; no params/latency in abstract.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-059 | 2512.03257
- arXiv/DOI: arXiv:2512.03257
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PyroFocus: Deep Learning for Real-Time Wildfire Detection in Multispectral RS Imagery
- Year / Venue: 2025 / arXiv (cs.CV/AI/LG)
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: P6
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P6] vision/arch: two-stage onboard
- Takeaway for TRINETRA: 3-class (no/active/post fire) + two-stage pipeline (cheap classify then FRP regression/seg only when needed) for onboard edge; abstract gives no concrete latency/accuracy/hardware.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-060 | 2512.12199
- arXiv/DOI: arXiv:2512.12199
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Thermal-RGB Fusion for Micro-UAV Wildfire Perimeter Tracking
- Year / Venue: 2025 / arXiv (cs.CV/AI) CC-BY
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: P6
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P6] fusion/edge: rule-based thermal+RGB
- Takeaway for TRINETRA: Classical fusion: thermal adaptive-threshold hot masks + RGB gradient filtering to suppress texture false positives; targets sub-50 ms on embedded SoC (small-scale sim).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-061 | 2608.23192
- arXiv/DOI: arXiv:2608.23192
- Authors: (ETH Zurich authors)
- Title: An Energy-Proportional Multimodal and Context-Aware Vision IoT Node
- Year / Venue: 2026 / arXiv (eess.IV)
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A3 | phase: P6
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P6] arch/power: STRONGEST node template
- Takeaway for TRINETRA: Dual-camera wake-on-motion: always-on event camera (GENX320) triggers an RGB imager (HM0360) + GAP9 RISC-V running quantized TinyissimoYOLOv12 (1M params).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-062 | 2406.16917
- arXiv/DOI: arXiv:2406.16917
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: GreenShield: CNN-Based Real-Time Forest Monitoring and Response
- Year / Venue: 2024 / arXiv (eess.SP)
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: P6
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P6] low-cost BOM: closest match + adaptive threshold
- Takeaway for TRINETRA: Arduino node: DHT11 (temp+humidity) + flame sensor + gas/smoke + GSM, 'adaptive threshold' + alerts (buzzer/notify); abstract gives NO accuracy/latency/false-alarm numbers and the CNN claim is unsubstantiated in abstract.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-063 | 2404.11439
- arXiv/DOI: arXiv:2404.11439
- Authors: Börger; Belt; Arnold
- Title: A Waypoint Based Approach to Visibility in Performance Based Fire Safety Design
- Year / Venue: 2024 / arXiv (CC BY 4.0)
- Read depth: FT | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] smoke optics: Jin's law V=C/σ camera-contrast forward model
- Takeaway for TRINETRA: Formalizes what a camera sees through smoke via Jin's law V=C/σ (C≈2-4 reflecting, 5-10 emitting; FDS defaults 3/8) with path-integrated extinction σ̄=∫σdl/L.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-064 | 2202.06567
- arXiv/DOI: arXiv:2202.06567
- Authors: Coenen; Kolb; Sánchez; Williams
- Title: Observed Dependence of Liquid-Pool-Fire Characteristics on Swirl Magnitude
- Year / Venue: 2019 / Combustion and Flame
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7 | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] swirl suppresses puffing → EF-08 breaks
- Takeaway for TRINETRA: 3.2/5.1 cm heptane-ethanol pools, 9 swirl levels: moderate swirl suppresses global puffing instability (→ helical fire-whirl), burning rate rises then falls.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-065 | 2206.08501
- arXiv/DOI: arXiv:2206.08501
- Authors: Dabrowski; et al.
- Title: Towards Data Assimilation in Level-Set Wildfire Models Using Bayesian Filtering
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7 | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] level-set lacks native DA/UQ
- Takeaway for TRINETRA: Adds Bayesian filtering so observations can be assimilated + uncertainty quantified — capabilities bare level-set lacks; error grows uncorrected without it. Documents the spread-model weakness; filtering mitigation. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-066 | 2302.04960
- arXiv/DOI: arXiv:2302.04960
- Authors: Yoo; Wikle
- Title: Using Echo State Networks to Inform Physical Models for Fire Front Propagation
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] learn ROS s inside level-set with UQ
- Takeaway for TRINETRA: Reservoir net learns the nonlinear normal-direction front speed inside a level-set framework (calibrated UQ, efficient); validated synthetic + 2017 Thomas/Haypress fires. Physics-guided-feature pattern targeting over-parameterized ROS.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-067 | 2210.14978
- arXiv/DOI: arXiv:2210.14978
- Authors: Yoo; Wikle
- Title: A Bayesian Spatio-Temporal Level Set Dynamic Model for Fire Front Propagation
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] probabilistic level-set front with UQ
- Takeaway for TRINETRA: Couples mechanistic level-set with a stochastic spatio-temporal front-velocity model in a Bayesian hierarchy for forecasting with UQ (Thomas/Haypress). Mitigates deterministic over-parameterized ROS. Source-reported. NEW. literature_map #7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-068 | 1601.06272
- arXiv/DOI: arXiv:1601.06272
- Authors: Kaur; Mentrelli; Bosseur; Filippi; Pagnini
- Title: Turbulence and Fire-Spotting Effects into Wildland Fire Simulators
- Year / Venue: 2016 / Commun. Nonlinear Sci. Numer. Simulat.
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] deterministic ROS misses turbulence/spotting
- Takeaway for TRINETRA: Front = deterministic drift + random fluctuating PDF component encoding turbulence & firebrand spotting (level-set LSM + Lagrangian DEVS); reproduces flank/back fire, no-fuel-zone jumps, secondary ignitions.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-069 | 2606.11676
- arXiv/DOI: arXiv:2606.11676
- Authors: Zhenirovskyy; et al.
- Title: Neural-Parameterized Cellular Automata for Wildfire Spread
- Year / Venue: 2026 / Ecological Informatics
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7 | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] CNN generates per-cell CA spread params
- Takeaway for TRINETRA: Probabilistic 3-state CA whose spread/wind/slope params are generated per-cell by a multi-scale CNN; keeps CA interpretability, gradient calibration. Reported IoU>0.6 over 72h on six western-US fires.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-070 | 2510.09708
- arXiv/DOI: arXiv:2510.09708
- Authors: Weinhouse; Augustin
- Title: Leveraging Cellular Automata for Real-Time Wildfire Spread Modeling in California
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] cheap CA baseline; over-spread failure
- Takeaway for TRINETRA: Lightweight CA from NDVI/wind/slope open data; vs 2025 Pacific Palisades burn scar recall 0.860 precision 0.605 F1 0.711 ~1.22s. Cheap-CA accuracy/operability trade; low precision = over-spread failure mode (baseline to beat).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-071 | 2309.02615
- arXiv/DOI: arXiv:2309.02615
- Authors: Shaddy; et al.
- Title: Generative Algorithms for Fusion of Physics-Based Wildfire Spread Models with Satellite Data
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7 | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] cWGAN physics-informed DA from satellite
- Takeaway for TRINETRA: Conditional Wasserstein GAN on WRF-SFIRE sims infers fire-arrival-time from satellite active-fire detections to init coupled forecasts (UQ via samples). Four CA fires: mean Sørensen 0.81, ignition-time err 32 min.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-072 | 1101.5745
- arXiv/DOI: arXiv:1101.5745
- Authors: Mandel; Beezley; Kochanski
- Title: An Overview of the Coupled Atmosphere-Wildland Fire Model WRF-Fire
- Year / Venue: 2011 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] canonical level-set + two-way coupling
- Takeaway for TRINETRA: WRF-Fire: level-set fire module takes wind, returns sensible/latent heat fluxes to the atmosphere each step (two-way coupling). Canonical operational spread architecture; shows the heat-flux feedback a physics model should respect.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-073 | 2001.04536
- arXiv/DOI: arXiv:2001.04536
- Authors: Wang; Teng; Perdikaris
- Title: Understanding and Mitigating Gradient Pathologies in PINNs
- Year / Venue: 2020 / arXiv
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] stiffness → unbalanced gradients → LR annealing
- Takeaway for TRINETRA: Numerical stiffness makes the physics-residual gradients dominate/vanish vs data/BC terms → training stalls; learning-rate annealing rescaling loss weights by running gradient stats + resilient architecture gives reported 50-100x accuracy g...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-074 | 2602.19265
- arXiv/DOI: arXiv:2602.19265
- Authors: Khodakarami; Oommen; Ahmadi; Beekenkamp; Karniadakis
- Title: Spectral Bias in Physics-Informed and Operator Learning: Analysis and Mitigation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] spectral bias is dynamical not just representational
- Takeaway for TRINETRA: Frequency-resolved study across PINNs/PIKANs/operators: low-freq learned far faster; 2nd-order optimizers change spectral learning order and recover high-freq earlier; spectral-aware losses help operators free.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-075 | 2206.14862
- arXiv/DOI: arXiv:2206.14862
- Authors: Farhani; Kazachek; Wang
- Title: Momentum Diminishes the Effect of Spectral Bias in PINNs
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] momentum + width reduce high-freq bias
- Takeaway for TRINETRA: NTK analysis: SGD-with-momentum (and Adam) substantially reduce spectral bias; sufficient width critical for high-freq convergence. Cheap optimizer-side mitigation before architectural changes. Source-reported. NEW. literature_map #18.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-076 | 2412.05994
- arXiv/DOI: arXiv:2412.05994
- Authors: Kang; Oh; Hong; Park
- Title: Physics-Informed Gaussians as Adaptive Parametric Mesh Representations
- Year / Venue: 2024 / ICLR 2025
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] learnable Gaussian features for sharp gradients
- Takeaway for TRINETRA: Trainable Gaussian feature embeddings (adaptive mesh) + light NN attack MLP spectral bias; competitive accuracy with fewer collocation points. Efficient sharp smoke/flame gradient representation. Source-reported. NEW. literature_map #19.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-077 | 2505.10949
- arXiv/DOI: arXiv:2505.10949
- Authors: Xu; Liu; Nassereldine; Xiong
- Title: FP64 is All You Need: Rethinking Failure Modes in PINNs
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7] FP32 precision stalls masquerade as failure modes
- Takeaway for TRINETRA: FP32 L-BFGS prematurely satisfies its convergence test → net frozen in spurious failure phase; FP64 lets vanilla PINNs solve, revealing a 3-stage dynamic. Check numerical precision/tolerance before blaming the model. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-078 | 2601.03569
- arXiv/DOI: arXiv:2601.03569
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Local Intrinsic Dimensionality of Ground Motion Data for Early Detection of Slope Failure
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P7G
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7G] unsupervised slope-failure detection
- Takeaway for TRINETRA: st-LID: unsupervised spatiotemporal local-intrinsic-dimensionality + kinematic velocity + Bayesian spatial fusion; src-reported better precision+lead-time than unsupervised baselines. Suits label-scarce slopes. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-079 | 1103.1678
- arXiv/DOI: arXiv:1103.1678
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Real-time inclinometer using accelerometer MEMS
- Year / Venue: 2011 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P7G
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7G] canonical low-cost buried-MEMS tilt EWS
- Takeaway for TRINETRA: Single MEMS accelerometer on buried pipe senses sub-surface displacement; WEAKNESS: no quantitative accuracy/false-alarm metric reported ('accurate enough'). Cheap-hardware reference needing independent calibration. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-080 | 2601.12330
- arXiv/DOI: arXiv:2601.12330
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: IceWatch: Forecasting GLOFs using Multimodal Deep Learning
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P7G
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7G] multimodal GLOF forecasting robust to cloud/missing data
- Takeaway for TRINETRA: Sentinel-2 CNN (RiskFlow) + ITS_LIVE velocity (TerraFlow) + MODIS LST (TempFlow), physics-informed, cross-validated; src-reported robust to noise/missing info (no single headline metric). Fixes optical-only cloud weakness. Source-reported.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-081 | 2412.02723
- arXiv/DOI: arXiv:2412.02723
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DYffCast: Regional Precipitation Nowcasting Using IMERG Satellite Data
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P7G
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7G] satellite-only precipitation nowcast (no radar)
- Takeaway for TRINETRA: DYffusion generative framework, 4h IMERG nowcast, MSE+MAE+LPIPS loss; src-reported highest CSI across thresholds + LPIPS<0.2 beating 4 competitors. Attractive where Himalaya lacks ground radar. Source-reported. NEW. literature_map L8.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-082 | 1306.1529
- arXiv/DOI: arXiv:1306.1529
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Scaling Properties of Rainfall-Induced Landslides Predicted by TRIGRS
- Year / Venue: 2014 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P7G
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7G] TRIGRS reproduces I-D + size-frequency but needs dense params
- Takeaway for TRINETRA: Physically-based TRIGRS + synthetic rainfall (Upper Tiber); src-reported reproduces landslide size-frequency power laws + mean I-D thresholds.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-083 | 1209.5256
- arXiv/DOI: arXiv:1209.5256
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Infiltration effects on a 2D molecular dynamics model of landslides
- Year / Venue: 2012 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P7G
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7G] pore-pressure physics matters but hard to parameterize
- Takeaway for TRINETRA: 2D MD/DEM deep-landslide model w/ pore-pressure filtration + Mohr-Coulomb; WEAKNESS: arbitrary Lennard-Jones-like potential 'in absence of experimental data' → only qualitative. Source-reported. NEW. literature_map L11.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-084 | 1208.6116
- arXiv/DOI: arXiv:1208.6116
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A computational toy model for shallow landslides: Molecular Dynamics approach
- Year / Venue: 2012 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P7G
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7G] validates Fukuzono inverse-velocity failure-time (cheap EWS tool)
- Takeaway for TRINETRA: 2D MD/DEM shallow-landslide via speed threshold + rainfall-driven Mohr-Coulomb friction loss; src-reported Gutenberg-Richter/Omori power laws + reproduces Fukuzono inverse surface-velocity failure-time.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-085 | 2609.32971
- arXiv/DOI: arXiv:2609.32971
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Distributed Hydrological Modeling in the Feature Space
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P7G
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7G] topology-aware routing strong in UNGAUGED basins
- Takeaway for TRINETRA: Feature-space routing: topology-aware state-space operator embedding river-network connectivity, fair-CRPS probabilistic discharge; src-reported SOTA on EFAS, improves ungauged skill to 10-day lead at 1-arcmin/6h.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-086 | 2607.23237
- arXiv/DOI: arXiv:2607.23237
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Context-Aware Concept Distillation for Trustworthy Flood Prediction
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P7G
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7G] interpretable flood LSTM surrogate (black-box-trust)
- Takeaway for TRINETRA: Distills opaque flood LSTMs into hydrology-aware interpretable surrogates via unsupervised 'Hydrological Language' + residual hypernetwork on static basin traits; src-reported median NSE 0.70 across 5,203 basins beating black-box MLP on uns...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-087 | 2607.21200
- arXiv/DOI: arXiv:2607.21200
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Transformer-based Diffusion Models for Hydrological Time Series Imputation and Forecasting
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P7G
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7G] handles gappy/drifting gauge records
- Takeaway for TRINETRA: Transformer diffusion for joint imputation+forecasting at 6 NE-France sites (15+ yr); src-reported outperforms baselines under variable missing data. Handles gappy sensor-drift-prone low-cost networks. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-088 | 2607.16080
- arXiv/DOI: arXiv:2607.16080
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-Based Deep Spatiotemporal Radar Nowcasting with Multi-Variable U-Net
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P7G
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P7G] runs on standard computer in seconds -> low-cost flash-flood
- Takeaway for TRINETRA: Radar-only encoder-decoder U-Net (multi-elevation reflectivity + Doppler + kinematic channels) to 90-min lead over Mumbai monsoon; src-reported CSI 0.437/0.332/0.193 at >=10/20/30 dBZ, beats persistence, nowcasts in seconds on a standard co...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-089 | 2508.08075
- arXiv/DOI: arXiv:2508.08075
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FNBT: Full Negation Belief Transformation for Open-World Information Fusion (DST)
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T1
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T1] fuse models over DIFFERENT frames of discernment; conflict elimination
- Takeaway for TRINETRA: Full-negation mass transform; src-reported proves invariance/heritability, resolves Zadeh, beats baselines. Fuse heterogeneous physics/vision/IoT. Source-reported. NEW. literature_map P14-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-090 | 2112.03044
- arXiv/DOI: arXiv:2112.03044
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Fusion Detection via Distance-Decay IoU and weighted Dempster-Shafer
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T1
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T1] decision-level DST fusion of two detectors, no paired data
- Takeaway for TRINETRA: Optical+SAR; src-reported +20.13% AP over optical-only. Score/decision-level evidence-weighted fusion template. Source-reported. NEW. literature_map P14-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-091 | 2509.25452
- arXiv/DOI: arXiv:2509.25452
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Infrastructure Sensor Vehicle Data Generation via Multi-Sensor (Kalman late) Fusion
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T1
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T1] Kalman late fusion robust to intermittent/degraded streams
- Takeaway for TRINETRA: camera+LiDAR; src-reported up to 70% longitudinal-error reduction, lateral 1-3 m. Marginalizes a dropped IoT stream. Source-reported. NEW. literature_map P14-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-092 | 2410.09570
- arXiv/DOI: arXiv:2410.09570
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: GETS: Ensemble Temperature Scaling for Calibration in GNNs
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T1/T4] MoE gating + temperature scaling, ~25% ECE reduction
- Takeaway for TRINETRA: input+model ensemble in graph MoE; src-reported across 10 benchmarks, fewer params. Candidate gating+calibration layer. Source-reported. NEW. literature_map P14-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-093 | 2104.08236
- arXiv/DOI: arXiv:2104.08236
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Controlled Abstention Neural Networks for Skillful Predictions (regression)
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T2
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T2] controllable abstain-fraction via PID (forecasts of opportunity)
- Takeaway for TRINETRA: abstention loss folds UQ into training; src-reported beats post-hoc UQ on climate regression. Explicit abstain budget for a safety-critical scorer. Source-reported. NEW. literature_map P14-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-094 | 2502.18050
- arXiv/DOI: arXiv:2502.18050
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Uncertainty-aware Abstention in Medical Diagnosis (HUQ-2)
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T2
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T2] UQ-driven selective prediction, reported SOTA reliability tradeoff
- Takeaway for TRINETRA: hybrid UQ across binary/multi-label/multi-class; src-reported. Abstention gate for fused scores. Source-reported. NEW. literature_map P14-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-095 | 2601.01008
- arXiv/DOI: arXiv:2601.01008
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Explainable Agentic Uncertainty-Aware Abstention for Stroke Imaging
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T2
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T2] threshold-based agentic abstention + explanation (design principles)
- Takeaway for TRINETRA: perception+UQ+decision agents; src-reported abstain emerges on ambiguous inputs (no new accuracy benchmark). Blueprint for threshold abstention + explanation. Source-reported. NEW. literature_map P14-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-096 | 2307.16895
- arXiv/DOI: arXiv:2307.16895
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Conformal PID Control for Time Series Prediction
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T3
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T3] online conformal coverage under drift via PID
- Takeaway for TRINETRA: src-reported improved coverage vs CDC ensemble forecaster; validated electricity/market/temp. Distribution-free coverage on top of any fuser. Source-reported. NEW. literature_map P14-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-097 | 2609.38196
- arXiv/DOI: arXiv:2609.38196
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Conformal Adversarial Generative Ensemble (CAGE)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T3/T6] conformal p-values dynamically reweight ensemble members
- Takeaway for TRINETRA: down-weights unreliable members; src-reported beats traditional ensembles on outliers/noise. Conformal-driven weighting + bad-detector suppression. Source-reported. NEW. literature_map P14-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-098 | 2202.08756
- arXiv/DOI: arXiv:2202.08756
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Ensemble Conformalized Quantile Regression (EnCQR)
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T3
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T3] distribution-free valid intervals for non-stationary series
- Takeaway for TRINETRA: bootstrap-ensemble QR, no exchangeability; src-reported sharper valid PIs. Per-source calibrated intervals before fusion. Source-reported. NEW. literature_map P14-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-099 | 2101.05397
- arXiv/DOI: arXiv:2101.05397
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Should Ensemble Members Be Calibrated?
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T4
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T4] CORE: calibrated members != calibrated ensemble
- Takeaway for TRINETRA: src-reported proof + CIFAR-100; ensemble <= avg of calibrated members. CALIBRATE THE FUSED OUTPUT. Source-reported. NEW. literature_map P14-T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-100 | 2501.10089
- arXiv/DOI: arXiv:2501.10089
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Classifier Ensemble for Efficient Uncertainty Calibration of DNNs
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T4
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T4] metamodel/stacking ensemble cuts ECE/MCE, no separate calibration set
- Takeaway for TRINETRA: src-reported outperforms traditional ensembles in calibration, fewer params. Learned stacking = strong calibrator. Source-reported. NEW. literature_map P14-T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-101 | 2309.15529
- arXiv/DOI: arXiv:2309.15529
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Missing-modality Enabled Multi-modal Fusion Architecture for Medical Data
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T5
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T5] fusion robust to modalities missing at inference
- Takeaway for TRINETRA: bi-modal transformer modules + multivariate losses; src-reported strong on MIMIC-IV/CXR. Degrades gracefully when a stream absent. Source-reported. NEW. literature_map P14-T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-102 | 2605.12517
- arXiv/DOI: arXiv:2605.12517
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Bridging the Missing-Modality Gap: Text-Only Calibration of VLMs (LIM)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T5
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T5] missing input breaks CALIBRATION not just accuracy; latent completion recovers
- Takeaway for TRINETRA: LIM cross-attention predicts imagined latent, frozen backbone; src-reported better acc + lower calibration error. Per-availability recalibration. Source-reported. NEW. literature_map P14-T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-103 | 2103.00883
- arXiv/DOI: arXiv:2103.00883
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A Secure Sensor Fusion Framework for CAVs under Sensor Attacks
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T5
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T5] redundancy -> bounded-error robust estimate + attack isolation
- Takeaway for TRINETRA: same-variable redundant sensors; src-reported bounded error independent of attack. Correlated/duplicated-input + adversarial case. Source-reported. NEW. literature_map P14-T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-104 | 2212.05478
- arXiv/DOI: arXiv:2212.05478
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Mul-GAD: Semi-supervised Graph Anomaly Detection via Multi-view Aggregation
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T6
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T6] view-level + feature-level fusion with learned per-view weights
- Takeaway for TRINETRA: src-reported better detection/generalization on 5 datasets. Blend anomaly-score channels with learned weights. Source-reported. NEW. literature_map P14-T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-105 | 2105.07346
- arXiv/DOI: arXiv:2105.07346
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Understanding the Effect of Bias in Deep Anomaly Detection
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T6
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T6] bounds relative scoring bias when adding labeled anomalies
- Takeaway for TRINETRA: first finite-sample rates; src-reported characterizes when labeled-anomaly fusion helps vs hurts. Bound bias before fusing; optimize recall@fixed-FPR. Source-reported. NEW. literature_map P14-T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-106 | 2203.07835
- arXiv/DOI: arXiv:2203.07835
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Better Uncertainty Calibration via Proper Scores
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T7] proper-calibration-error bound; common ECE estimators biased
- Takeaway for TRINETRA: src-reported theory + experiments. Statistically sound calibration MEASUREMENT. Source-reported. NEW. literature_map P14-T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-107 | 2408.02841
- arXiv/DOI: arXiv:2408.02841
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Evaluating Posterior Probabilities: Decision Theory, Proper Scoring Rules, Calibration
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T7] use proper scoring rules not ECE to assess posteriors
- Takeaway for TRINETRA: ECE ignores discrimination; src-reported calibration loss as diagnostic only. Evaluation discipline for WS1b. Source-reported. NEW. literature_map P14-T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-108 | 2609.04988
- arXiv/DOI: arXiv:2609.04988
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Strictly Proper Scoring-Rule Theory for Calibrating Stochastic Car-Following Models
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T7] ENERGY SCORE best for calibrating stochastic physics simulators
- Takeaway for TRINETRA: strict-propriety theory; src-reported energy score best held-out distributional prediction. Calibrate physics fire-spread sims with a proper score. Source-reported. NEW. literature_map P14-T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-109 | 2207.14024
- arXiv/DOI: arXiv:2207.14024
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Safety-Enhanced Autonomous Driving Using Interpretable Sensor Fusion Transformer (InterFuser)
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T8
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T8] safety-critical fusion w/ interpretable intermediate features + unknown-object detection
- Takeaway for TRINETRA: src-reported #1 CARLA leaderboard. Unknown-object ~ unseen fire signature; interpretable evidence. Source-reported. NEW. literature_map P14-T8.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-110 | 2108.05422
- arXiv/DOI: arXiv:2108.05422
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Deep PET/CT Fusion with Dempster-Shafer Theory for Lymphoma Segmentation
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1b | phase: P14-T8
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P14-T8] end-to-end differentiable evidential (DST) fusion layer
- Takeaway for TRINETRA: single-modality UNets + DST layer + concordance loss; src-reported Dice 0.726. Template for fusing vision+physics with explicit uncertainty. Source-reported. NEW. literature_map P14-T8.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-111 | 2501.08343
- arXiv/DOI: arXiv:2501.08343
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Ceiling Height of Wildland Fire Plumes in Sheared BL Flow
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] LES+modified-Byram scaling captures plume bending in sheared crossflow
- Takeaway for TRINETRA: Grounds EF-13/ND-5/ND-6. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-112 | 2510.13196
- arXiv/DOI: arXiv:2510.13196
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Buoyant Plume Dynamics over Plant Canopies via LES
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] canopy drag delays rise-to-bent transition; counter-rotating vortex pairs
- Takeaway for TRINETRA: Wind-tilt regime. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-113 | 2510.14423
- arXiv/DOI: arXiv:2510.14423
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Forest Canopy Structure Impact on Buoyant Plume (PALM LES)
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] gap-canopy maximizes TKE; buoyant production dominates shear
- Takeaway for TRINETRA: Plume regime. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-114 | 2510.13189
- arXiv/DOI: arXiv:2510.13189
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Scaling Analysis for Buoyant Plumes over Wildland Fires
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] near-surface plume slope ~1/4 power-law vs turbulence-intensity group
- Takeaway for TRINETRA: Buoyancy scaling for ND-3. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-115 | 2505.06638
- arXiv/DOI: arXiv:2505.06638
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: 3D Smoke Plume Dispersion via Multi-View Drone Swarm
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] multi-drone stereo reconstructs 3D plume concentration field
- Takeaway for TRINETRA: Smoke optics. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-116 | 2608.12223
- arXiv/DOI: arXiv:2608.12223
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Soret Diffusion & Radiative Heat Loss on Buoyant Flame Kernels (ultra-lean H2)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] R_f^2~Kt; Soret raises K, radiation lowers it; toroidal vortex breakup
- Takeaway for TRINETRA: Radiation effect. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-117 | 2406.08589
- arXiv/DOI: arXiv:2406.08589
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FireBench: High-fidelity Ensemble LES (Swirl-Fire)
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] 117 runs @1.35B pts; critical Froude number delineates plume- vs convection-driven fire
- Takeaway for TRINETRA: Grounds EF-13/ND-6 regime gate. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-118 | 1206.3345
- arXiv/DOI: arXiv:1206.3345
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Evaluation of WRF-Sfire with FireFlux Field Data
- Year / Venue: 2012 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] reproduces head-fire ROS + plume temp; over-predicts vertical velocity >10m
- Takeaway for TRINETRA: Simulator caveat. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-119 | 2302.01913
- arXiv/DOI: arXiv:2302.01913
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Fire Smoke Dispersion In/Outside Warehouse (CFD)
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] 25 runs; wind raised vent mass flow 78-158%; urban-canyon vortices trap smoke
- Takeaway for TRINETRA: Smoke transport. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-120 | 2401.08874
- arXiv/DOI: arXiv:2401.08874
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Single-Domain Buoyant Reacting Plume & Ignition in Porous Media
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] RT/KH-like instabilities; interface geometry alters ignition time/location
- Takeaway for TRINETRA: Ignition physics. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-121 | 2408.06205
- arXiv/DOI: arXiv:2408.06205
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Wildfire Spread & Spotfire Merger via Conformal Mapping
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] pyrogenic+ambient wind ROS; fast operational front matching
- Takeaway for TRINETRA: Offline spread sim (C-01). Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-122 | 2412.18931
- arXiv/DOI: arXiv:2412.18931
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Approximated Model of Wildfire Propagation on Slope
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] Rothermel+Huygens for inclined-terrain spread
- Takeaway for TRINETRA: Grounds EF-20. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-123 | 2609.09773
- arXiv/DOI: arXiv:2609.09773
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Nonlinear Flame Describing Function & Mean-Shift Kinematics
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] G-equation; mean flame-height shift governs FDF saturation (master curve)
- Takeaway for TRINETRA: Grounds EF-19/ND-1. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-124 | 1203.1396
- arXiv/DOI: arXiv:1203.1396
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Gas Compression on Finger Flame Acceleration in Tubes
- Year / Venue: 2012 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] small-Mach theory: compressibility reduces acceleration; tulip flame
- Takeaway for TRINETRA: Flame dynamics (tangential). Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-125 | 2001.05367
- arXiv/DOI: arXiv:2001.05367
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Kinetic Similarity between Extinction Strain Rate & Laminar Flame Speed
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] ESR and LFS kinetic sensitivity directions parallel across fuels/phi/P
- Takeaway for TRINETRA: Kinetics. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-126 | 1106.3698
- arXiv/DOI: arXiv:1106.3698
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: High-Speed Turbulence-Flame Interaction: Turbulent Flame Speed
- Year / Venue: 2011 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] DNS; S_T set by flame-area increase; cusp mechanism at Ka>20
- Takeaway for TRINETRA: Turbulent combustion. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-127 | 2509.13106
- arXiv/DOI: arXiv:2509.13106
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: 3D Morphology of Cellular H2/O2/N2 Flames on Porous-Plug Burner
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] 200+ cases; cellular wavenumbers below linear prediction; stabilize near lean limit
- Takeaway for TRINETRA: Flame structure. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-128 | 2303.17446
- arXiv/DOI: arXiv:2303.17446
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PMMA Pyrolysis Simulation Micro- to Real-Scale
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] multi-reaction+radiative flux reproduces TGA/MCC/cone; real-scale diverges
- Takeaway for TRINETRA: Pyrolysis (parked). Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-129 | 2105.11397
- arXiv/DOI: arXiv:2105.11397
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Autonomous Kinetic Modeling of Biomass Pyrolysis via CRNN
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] CRNN+neural-ODE recovers interpretable Arrhenius kinetics from TGA
- Takeaway for TRINETRA: Pyrolysis ML. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-130 | 2203.04639
- arXiv/DOI: arXiv:2203.04639
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Phases and Time-Scales of Ignition & Burning of Live Fuels
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] 4 burning phases incl droplet ejection; LFMC-dependent transition
- Takeaway for TRINETRA: Live-fuel. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-131 | 2102.11060
- arXiv/DOI: arXiv:2102.11060
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Effect of Precursors & Radiation on Soot in Turbulent Diffusion Flame
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] WSGGM non-gray radiation; soot radiative loss lowers flame temp
- Takeaway for TRINETRA: Grounds EF-15/ND-2. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-132 | 1406.4058
- arXiv/DOI: arXiv:1406.4058
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Ignition via Radiative Preheating of Suspended Particles
- Year / Venue: 2015 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] radiation-heated particle clouds trigger Zeldovich-gradient ignition
- Takeaway for TRINETRA: Radiation ignition. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-133 | 2206.01529
- arXiv/DOI: arXiv:2206.01529
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Urban Boundary Layer Turbulence on Firebrand Transport
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] LES; urban topography compacts spotting map, raises landing temp
- Takeaway for TRINETRA: Grounds EF-18/ND-7 advection. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-134 | 2411.13275
- arXiv/DOI: arXiv:2411.13275
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Extreme Firebrand Transport by Atmospheric Waves
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] waves increase spotting distance >=1 order via particle synchronization
- Takeaway for TRINETRA: Firebrand. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-135 | 2506.15891
- arXiv/DOI: arXiv:2506.15891
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: High-Speed Thermal Imaging of Disk-shaped Firebrands
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] 960fps two-color pyrometry; firebrand temp oscillates 50-480Hz vs speed
- Takeaway for TRINETRA: IR/firebrand. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-136 | 2201.07931
- arXiv/DOI: arXiv:2201.07931
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Large-Scale Jet Flames' Geometrical Features from IR Images (UNet)
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] attention-UNet segments IR radiation zones; height/area approximation
- Takeaway for TRINETRA: IR detection physics. Source-reported. NEW. P21 fire-physics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-137 | 2509.03347
- arXiv/DOI: arXiv:2509.03347
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-informed ML for combustion: A review
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] taxonomy of PIML across kinetics/reacting-flows via soft/hard constraints
- Takeaway for TRINETRA: Review. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-138 | 2504.12580
- arXiv/DOI: arXiv:2504.12580
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: ChemKANs for Combustion Chemistry Modeling
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] KAN-ODE 344-param models H2 combustion ~2x speedup, robust to 15% noise
- Takeaway for TRINETRA: Surrogate. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-139 | 1910.09098
- arXiv/DOI: arXiv:1910.09098
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Learning Stochastic Advection-Diffusion-Reaction from Sparse Measurements
- Year / Venue: 2019 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] sPINN solves forward+inverse nonlinear ADR; Bayesian-opt hyperparams
- Takeaway for TRINETRA: Grounds EF-17/ND-4/ND-7. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-140 | 1911.11380
- arXiv/DOI: arXiv:1911.11380
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-Informed Super-Resolution GAN for Subgrid Turbulent Reactive Flows
- Year / Venue: 2019 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] unsupervised GAN subfilter LES closure; good a priori/posteriori
- Takeaway for TRINETRA: Turbulence closure. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-141 | 2210.16206
- arXiv/DOI: arXiv:2210.16206
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PIESRGAN for Turbulent Premixed Combustion / Flame-Kernel DNS
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] GAN subfilter reproduces DNS on coarser meshes
- Takeaway for TRINETRA: Turbulence. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-142 | 2210.16219
- arXiv/DOI: arXiv:2210.16219
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PIESRGAN for Finite-Rate-Chemistry / Lean Premixed Gas Turbine
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] extends PIESRGAN to reacting finite-rate chemistry
- Takeaway for TRINETRA: Turbulence. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-143 | 2211.12341
- arXiv/DOI: arXiv:2211.12341
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Gradient Info & Regularization for Gene Expression Programming Closure
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] adaptive-symbol GEP rediscovers Sutherland law + flame-speed closures
- Takeaway for TRINETRA: Symbolic closure. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-144 | 2008.02862
- arXiv/DOI: arXiv:2008.02862
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Regularized Operator Inference ROM for Single-Injector Combustion
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] non-intrusive quadratic ROM ~1e6x speedup, stable long-time
- Takeaway for TRINETRA: ROM for offline sim. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-145 | 1908.03620
- arXiv/DOI: arXiv:1908.03620
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Learning Physics-Based ROM for Single-Injector Combustion
- Year / Venue: 2019 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] POD+variable transforms expose quadratic structure; >5 orders speedup
- Takeaway for TRINETRA: ROM. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-146 | 2510.15954
- arXiv/DOI: arXiv:2510.15954
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Fire-EnSF: Wildfire Spread Data Assimilation via Ensemble Score Filter
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] diffusion score-based filter for high-dim nonlinear wildfire DA
- Takeaway for TRINETRA: DA for fusion. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-147 | 0709.0086
- arXiv/DOI: arXiv:0709.0086
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A Wildland Fire Model with Data Assimilation
- Year / Venue: 2008 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] coupled energy/fuel PDEs + regularized EnKF corrects ignition location
- Takeaway for TRINETRA: DA grounding. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-148 | 2603.26975
- arXiv/DOI: arXiv:2603.26975
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Probabilistic Forecasting of Wildfire Spread via Conditional Flow Matching
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] learns conditional distribution of fire arrival times; ensemble forecasts
- Takeaway for TRINETRA: Stochastic spread. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-149 | 2012.00640
- arXiv/DOI: arXiv:2012.00640
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Adjoint-Based Sensitivity Analysis of Steady Char Burnout
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] discrete+continuous adjoints quantify combustion-parameter sensitivities
- Takeaway for TRINETRA: Inverse/sensitivity. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-150 | 2503.11729
- arXiv/DOI: arXiv:2503.11729
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Information Loss on Composition Measurement in Stiff Reacting Systems
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] Bayesian NUTS inference; manifold rank reduction causes inference failures
- Takeaway for TRINETRA: UQ caveat. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-151 | 2504.17900
- arXiv/DOI: arXiv:2504.17900
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Model Error Covariance Estimation for Weak-Constraint 4D-Var DA
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] weak-constraint 4D-Var as regularized inverse; validated on 1D smoke-transport
- Takeaway for TRINETRA: DA covariance caveat. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-152 | 2307.05602
- arXiv/DOI: arXiv:2307.05602
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Auxiliary PINNs for Forward/Inverse/Coupled Radiative Transfer
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] APINN solves Boltzmann RTE + coupled radiation-conduction; inverse albedo
- Takeaway for TRINETRA: RTE. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-153 | 2605.23971
- arXiv/DOI: arXiv:2605.23971
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-Guided Concentration Inference from Resistance Transients (CO sensor)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] physics descriptors+FFT/DWT; MAE~1.48ppm, R2~0.992
- Takeaway for TRINETRA: Grounds B-06/ND-2 sensor physics. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-154 | 2607.18544
- arXiv/DOI: arXiv:2607.18544
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics Closure for Machine Olfaction: Maxwell-Stefan Graph Solver
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] embeds Maxwell-Stefan transport+adsorption+sensor ODEs for gas unmixing
- Takeaway for TRINETRA: Sensor physics. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PHY-155 | 2506.10404
- arXiv/DOI: arXiv:2506.10404
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Generative Algorithms for Wildfire Progression Reconstruction
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05 models, ch 13 feasibility
- Core method: [P21] cGAN infers fire arrival time from VIIRS/GOES; avg Sorensen-Dice 0.81
- Takeaway for TRINETRA: DA/inverse. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass


---

## Theme: Physics-informed ML (PINN / neural operators)  (`REF-PINN-*`, 19 entries)

_Primary consumer: WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict. The ledger axis/WS code that mapped each paper into this theme is printed per entry for traceability._

#### REF-PINN-001 | 2406.16236
- arXiv/DOI: arXiv:2406.16236
- Authors: Brecht; Cardoso-Bihlo; Bihlo
- Title: Physics-informed neural networks for tsunami inundation modeling
- Year / Venue: 2024 / arXiv (physics.comp-ph)
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: PINN/DeepONet meshless shallow-water inundation
- Takeaway for TRINETRA: Solves shallow-water equations for tsunami propagation + inundation with PINNs (meshless, simplifies inundation modelling); PINNs need retraining per initial condition, so they add DEEP OPERATOR NETS (DeepONet) that learn the solution OPERA...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-002 | 2104.00615
- arXiv/DOI: arXiv:2104.00615
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-informed neural networks for the shallow-water equations on the sphere
- Year / Venue: 2022 / arXiv (physics.ao-ph)
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: PINN SWE, multi-model for long horizons
- Takeaway for TRINETRA: PINNs for shallow-water on the sphere (meteorological context); documents PINN TRAINING DIFFICULTIES over long time intervals and proposes a simple MULTI-MODEL approach (sequence of nets, one per sub-interval) plus encoding boundary conditi...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-003 | 2507.15021
- arXiv/DOI: arXiv:2507.15021
- Authors: Radfar; Maghsoodifar; Moftakhari; Moradkhani
- Title: Integrating Newton's Laws with deep learning for enhanced physics-informed compound flood modelling
- Year / Venue: 2025 / arXiv (physics.geo-ph)
- Read depth: ABS | local note: yes | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: ALPINE PINN: FULL shallow-water (mass+both momentum) compound-flood emulator; physics helps MOST at peak
- Takeaway for TRINETRA: ALPINE (All-in-one Physics-Informed Neural Emulator) enforces COMPLETE shallow-water dynamics (mass conservation + BOTH momentum equations, not partial constraints) for COMPOUND floods (surge+tide+rainfall+river discharge interacting); Conv...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-004 | 2501.11372
- arXiv/DOI: arXiv:2501.11372
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-Informed Neural Networks for Solving the Two-Dimensional Shallow Water Equations with Terrain Topography and Rainfall Source Terms
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: 2D shallow-water PINN with terrain + rainfall source terms
- Takeaway for TRINETRA: PINN solving the 2D shallow-water equations WITH terrain topography and RAINFALL source terms - i.e. rainfall-driven overland/flash flooding on real terrain.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-005 | 2407.06785
- arXiv/DOI: arXiv:2407.06785
- Authors: Dahal; Lombardo
- Title: Towards physics-informed neural networks for landslide prediction
- Year / Venue: 2024 / JGR: Machine Learning & Computation
- Read depth: ABS | local note: no | ledger axis/WS: A3 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: PINN + Newmark geotechnical retrieval
- Takeaway for TRINETRA: PINN for regional coseismic landslide prediction: adds a Newmark permanent-deformation constraint so the net explicitly RETRIEVES geotechnical parameters from cheap proxy variables, then minimizes loss vs a coseismic inventory; yields both...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-006 | 2610.04828
- arXiv/DOI: arXiv:2610.04828
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Label-Free PINN Strength-Reduction Factor-of-Safety at Scale
- Year / Venue: 2026 / arXiv
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A4 | phase: P3
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P3] PIML/slope WS1 (new FM)
- Takeaway for TRINETRA: Label-free PINN SRM FoS within 2-3% RMS of Abaqus, million random fields/s via operator. 3% FoS error → up to 2x error in 1e-3 failure prob (methods disagree 2.6-8.3x).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-007 | 2608.12422-RESTUDY
- arXiv/DOI: arXiv:2608.12422
- Authors: Kahn; Arjel; Adhikari; Sherpa; Pope
- Title: Which Site and When (BASELINE RE-STUDY ABS->FT-PARTIAL per OQ-02; original ABS row #82 UNCHANGED)
- Year / Venue: 2026 / arXiv (cs.LG/stat.AP)
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A11 | phase: n/r
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P3-RESTUDY baseline, NON-QUOTA] THE reality-check: honest spatial-CV + GB baseline wins
- Takeaway for TRINETRA: Re-studied 2026-10-07 to Tier-2+ depth (NOT new quota; quota stays 33). Free-data prediction test on OUR hazards+region (Nepal): GLOF bursts/landslides/small-floods, 3-hazard-2-question-never-blended, 589 HMAGLOFDB outbursts + thousands lan...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-008 | 2208.03542
- arXiv/DOI: arXiv:2208.03542
- Authors: Sitte; Doan
- Title: Velocity Reconstruction in Puffing Pool Fires with Physics-Informed Neural Networks
- Year / Venue: 2022 / Physics of Fluids (CC BY 4.0)
- Read depth: FT | local note: no | ledger axis/WS: WS1 | phase: P7 | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P7] PINN soft-sensor infers velocity from T/ρ
- Takeaway for TRINETRA: HFM PINN maps (x,r,t)->[ρ,p,T,u,v] with data loss on measurable fields + reacting-NS residual; ground truth fireFoam (flame T≈1750K).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-009 | 2212.00970
- arXiv/DOI: arXiv:2212.00970
- Authors: Dabrowski; et al.
- Title: Bayesian Physics-Informed Neural Networks for Spatio-Temporal Modelling of Wildfires
- Year / Venue: 2022 / Spatial Statistics (CC BY)
- Read depth: FT | local note: no | ledger axis/WS: WS1 | phase: P7 | re-cited 2x
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P7] level-set PINN; temporal-continuity failure + UQ
- Takeaway for TRINETRA: Solves level-set front PDE ∂u/∂t+s‖∇u‖+W·∇u=0 (ROS per Rothermel) with a Bayesian PINN; standard MSE loss FAILS temporal continuity under abrupt wind change → adds forecast-likelihood cost + B-PINN UQ.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-010 | 2502.18738
- arXiv/DOI: arXiv:2502.18738
- Authors: Xia; Cheng
- Title: PyTorchFire: GPU-Accelerated Differentiable Cellular Automata Wildfire Simulator
- Year / Venue: 2025 / Environ. Model. Softw.
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P7] differentiable CA for calibratable params
- Takeaway for TRINETRA: Differentiable CA enabling gradient-descent real-time parameter calibration vs observed perimeters; ms/step, better generalization than a supervised surrogate. Differentiable-physics (not PINN) mitigation for non-identifiable CA params.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-011 | 2109.01050
- arXiv/DOI: arXiv:2109.01050
- Authors: Krishnapriyan; Gholami; Zhe; Kirby; Mahoney
- Title: Characterizing Possible Failure Modes in Physics-Informed Neural Networks
- Year / Venue: 2021 / NeurIPS 2021
- Read depth: FT | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P7] PINN soft-constraint landscape failure + fixes
- Takeaway for TRINETRA: Vanilla PINNs hit ~100% rel error (1D convection β>10) / ~93% (reaction-diffusion) despite closed-form solutions — an OPTIMIZATION (ill-conditioned loss) not expressivity problem (Hessian analysis).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-012 | 2203.07404
- arXiv/DOI: arXiv:2203.07404
- Authors: Wang; Sankaran; Perdikaris
- Title: Respecting Causality is All You Need for Training PINNs
- Year / Venue: 2022 / arXiv
- Read depth: FT | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P7] causality violation → causal weighting
- Takeaway for TRINETRA: Continuous-time PINNs minimize residual at later times before IC resolved (NTK diagnosis); vanilla fails Allen-Cahn (49.87% err).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-013 | 2501.17281
- arXiv/DOI: arXiv:2501.17281
- Authors: Seiler; Lei; Protopapas
- Title: Stiff Transfer Learning for Physics-Informed Neural Networks
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P7] stiffness via one-shot transfer learning
- Takeaway for TRINETRA: Train a Multi-Head PINN in a low-stiffness regime then one-shot transfer to high stiffness; reported accuracy/speed beating PINN baselines, efficiency comparable to implicit solvers.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-014 | 2609.13171
- arXiv/DOI: arXiv:2609.13171
- Authors: Koyamada
- Title: A Derivative-Fidelity Failure Mode in Physics-Informed Neural Networks
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1 | phase: P7
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P7] good values != good derivatives (QA check)
- Takeaway for TRINETRA: MLPs trained on sin/exp show small value error but much larger 2nd-derivative error (worst at high curvature); provides a diagnostic protocol.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-015 | 2108.05415
- arXiv/DOI: arXiv:2108.05415
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-Aware NN Flame Closure for Combustion Instability
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P21] NN sub-grid flamelet-table replacement verified in LES
- Takeaway for TRINETRA: PINN closure. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-016 | 2509.08094
- arXiv/DOI: arXiv:2509.08094
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PINNs in Clean Combustion (review)
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P21] surveys mesh-free PINN flame dynamics/turbulent combustion/instability
- Takeaway for TRINETRA: Review. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-017 | 2207.05748
- arXiv/DOI: arXiv:2207.05748
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-Informed Deep Neural Operator Networks
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P21] review of DeepONet/FNO/graph operators as physics-informed PDE surrogates
- Takeaway for TRINETRA: Grounds ADR surrogate. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-018 | 2009.13291
- arXiv/DOI: arXiv:2009.13291
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-Informed Neural Networks for Simulating Radiative Transfer
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P21] PINN minimizes RTE residual; error estimates + inverse RTE solver
- Takeaway for TRINETRA: Grounds EF-14/ND-2. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-PINN-019 | 2505.23190
- arXiv/DOI: arXiv:2505.23190
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DeepRTE: Pre-trained Attention Neural Operator for Radiative Transfer
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS1a-PHYS | phase: P21
- Uses (workstream/chapter): WS1 physics gate (ch 06), ch 05, ch 13 feasibility verdict
- Core method: [P21] mesh-free RTE neural operator w/ Green's-function pretraining; zero-shot
- Takeaway for TRINETRA: RTE operator. Source-reported. NEW. P21 advanced.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass
