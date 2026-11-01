# 19b_REFERENCES_fusion_uncertainty_eval -- TRINETRA reference catalogue (part of chapter 19)

> Row-level truth: `analysis/02_paper_ledger.csv`. Index, counts, MUST-READ TOP-30, dataset cross-index and BibTeX live in `docs/19_REFERENCES_FULL.md`.

> **Residual-identifier risk (per _CANON SS7):** every identifier below is a real ledger row, but identifiers were *subagent-reported during a web_search outage and were NOT independently re-fetched this pass*. No entry claims a resolved identifier unless its Verification line says so.

> Read-depth tags are copied verbatim from the ledger: FT / FT-PARTIAL / ABS / ABS-CANONICAL / FT-REF.


---

## Theme: Fusion / uncertainty / calibration / conformal  (`REF-FUS-*`, 70 entries)

_Primary consumer: WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation. The ledger axis/WS code that mapped each paper into this theme is printed per entry for traceability._

#### REF-FUS-001 | 2604.00801
- arXiv/DOI: arXiv:2604.00801
- Authors: Liu; Han; Yan; Tresp; Ma
- Title: Routing-Free Mixture-of-Experts
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: eliminates router/TopK/load-balance instability
- Takeaway for TRINETRA: Standard MoE routers impose rigid inductive bias + need load-balancing hacks; Routing-Free MoE removes external routers/Softmax/Top-K/load-balancing, letting each expert self-activate via continuous gradient flow with a unified adaptive bal...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-002 | 2601.03425
- arXiv/DOI: arXiv:2601.03425
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: The Illusion of Specialization: Domain-Invariant Standing Committee in Mixture-of-Experts
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: MoE routing collapses to a fixed expert coalition
- Takeaway for TRINETRA: COMMITTEEAUDIT shows MoE models do NOT achieve the assumed domain specialization: a compact domain-INVARIANT 'standing committee' of experts captures most routing mass across domains/layers/budgets.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-003 | 2004.01764
- arXiv/DOI: arXiv:2004.01764
- Authors: Kerwin; Bastian
- Title: Stacked Generalizations in Imbalanced Fraud Data Sets using Resampling Methods
- Year / Venue: 2020 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: stacking + resampling under imbalance
- Takeaway for TRINETRA: Two-step stacked generalization (base learners -> meta/super learner) improves over individuals especially when combined with resampling on heavily IMBALANCED data; weakest base learners improve most; essentially enhanced cross-validation b...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-004 | 2509.03315
- arXiv/DOI: arXiv:2509.03315
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: The super learner for time-to-event outcomes: A tutorial
- Year / Venue: 2026 / arXiv (stat.ME)
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: super-learner theory: oracle, CV ensemble
- Takeaway for TRINETRA: Tutorial on the SUPER LEARNER (van der Laan): a cross-validation-based ensemble with an oracle property - asymptotically performs as well as the best candidate (or combination) in a pre-specified library, here for censored time-to-event ris...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-005 | 2603.10392
- arXiv/DOI: arXiv:2603.10392
- Authors: Gonzales; Mizuta; Leung; Ratliff
- Title: Safe Probabilistic Planning for Human-Robot Interaction using Conformal Risk Control
- Year / Venue: 2026 / arXiv (cs.RO)
- Read depth: ABS | local note: no | ledger axis/WS: A7 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: CBF + conformal risk control = formal safety margins
- Takeaway for TRINETRA: Combines control barrier functions (CBFs) with CONFORMAL RISK CONTROL to give formal probabilistic constraint-satisfaction guarantees while handling complex (human) behaviour; an algorithm dynamically adjusts conformal safety margins by int...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-006 | 2512.12844
- arXiv/DOI: arXiv:2512.12844
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Selective Conformal Risk Control (SCRC)
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A7 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: conformal prediction + selective abstention, two-stage
- Takeaway for TRINETRA: Conformal prediction gives distribution-free coverage but often oversized sets; SCRC integrates it with SELECTIVE CLASSIFICATION in two stages: (1) select confident samples, (2) apply conformal risk control on the selected subset for calibr...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-007 | 2512.01384
- arXiv/DOI: arXiv:2512.01384
- Authors: Kim; Choi; Aashik Rasool; Oh
- Title: CLAPS: Aleatoric-Epistemic Scaling via Last-Layer Laplace for Conformal Regression
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A7 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: conformal interval width adapts to aleatoric+epistemic
- Takeaway for TRINETRA: Conformal regression gives marginal coverage but doesn't say how interval WIDTH should adapt across inputs; existing locally-adaptive methods capture only aleatoric noise, ignoring uncertainty from weak training support; CLAPS uses heterosc...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-008 | 2401.13697
- arXiv/DOI: arXiv:2401.13697
- Authors: Zhao; Poria; Li; Chen; Tang
- Title: Toward Robust Multimodal Learning using Multimodal Foundational Models (TRML)
- Year / Venue: 2024 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: generate virtual modality to replace missing one
- Takeaway for TRINETRA: Real multimodal data is often INCOMPLETE; CLIP-style foundation models can't directly handle modality absence; TRML generates VIRTUAL modalities to replace missing ones and aligns their semantic space with the real ones via a missing-modali...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-009 | 2310.03986
- arXiv/DOI: arXiv:2310.03986
- Authors: Kim; Kim
- Title: Robust Multimodal Learning with Missing Modalities via Parameter-Efficient Adaptation
- Year / Venue: 2024 / ECCV 2024
- Read depth: ABS | local note: yes | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: predict missing-modality embedding via prompt tuning
- Takeaway for TRINETRA: Parameter-efficient fine-tuning of unimodal pretrained models + self-supervised joint-embedding so the model PREDICTS the embedding of a missing modality at inference via prompt tuning, using available modalities; robust across varied missi...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-010 | 2405.06479
- arXiv/DOI: arXiv:2405.06479
- Authors: Ying; Guo; Khamaru; Hung
- Title: Uncertainty Quantification With Multiple Sources
- Year / Venue: 2026 / arXiv (stat.ME)
- Read depth: ABS | local note: no | ledger axis/WS: A7 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: multi-source weighted conformal under covariate shift
- Takeaway for TRINETRA: Weighted conformal prediction (WCP) handles covariate shift but relies on train/test covariate OVERLAP, which breaks in MULTI-SOURCE settings with varying covariate distributions; proposes two WCP extensions under a shared-conditional assum...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-011 | 2310.03545
- arXiv/DOI: arXiv:2310.03545
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Distribution-free risk assessment of regression-based machine learning algorithms
- Year / Venue: 2023 / arXiv (stat.ML)
- Read depth: ABS | local note: no | ledger axis/WS: A7 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: conformal failure-probability for regression intervals
- Takeaway for TRINETRA: Targets the RISK-ASSESSMENT task: computing the probability that the true label lies within an interval around a regression model's prediction, critical for high-risk medicine/engineering; solves it with conformal prediction giving interval...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-012 | 2011.06125
- arXiv/DOI: arXiv:2011.06125
- Authors: Boussioux; Zeng; Guenais; Bertsimas
- Title: Hurricane Forecasting: A Novel Multimodal Machine Learning Framework (Hurricast)
- Year / Venue: 2022 / AMS Weather & Forecasting
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: meta-fusion head
- Takeaway for TRINETRA: Combines deep encoder-decoder spatiotemporal features + gradient-boosted trees; consensus-model inclusion beats NHC official. Direct precedent for TRINETRA's encoder->XGBoost + stacked meta-fusion; evidence stacking helps operational skill.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-013 | 2406.05405
- arXiv/DOI: arXiv:2406.05405
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Robust Conformal Prediction Using Privileged Information
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A7 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: conformal calibration
- Takeaway for TRINETRA: Naive conformal fails under missing/noisy training variables; builds coverage robust to such corruption. TRINETRA's sensor dropouts (brownout, Bug #8) break i.i.d.; this is a fix path for the conformal overclaim (Bug #13).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-014 | 2511.11567
- arXiv/DOI: arXiv:2511.11567
- Authors: Binny; Dixit
- Title: Who Moved My Distribution? Conformal Prediction for Interactive Multi-Agent Systems
- Year / Venue: 2025 / arXiv (eess.SY)
- Read depth: ABS | local note: no | ledger axis/WS: A7 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: conformal / endogenous shift
- Takeaway for TRINETRA: Iterative conformal adapts to endogenous distribution shift (acting changes the distribution). TRINETRA alarms change human behavior (evacuation) -> endogenous shift on future data; marginal conformal coverage not preserved.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-015 | 2410.10397
- arXiv/DOI: arXiv:2410.10397
- Authors: Akretche; LeBlanc; Marchand
- Title: Tighter Risk Bounds for Mixtures of Experts
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: MoE gating / generalization
- Takeaway for TRINETRA: Generalization risk bounds for one-out-of-n (hard) gating MoE; log dependence on #experts. Theory backing TRINETRA's gated meta-fusion generalization; argues for sparse hard gating over dense gating (design choice justification).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-016 | 2604.20551
- arXiv/DOI: arXiv:2604.20551
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: On Bayesian Softmax-Gated Mixture-of-Experts Models
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: MoE gating / model selection
- Takeaway for TRINETRA: Posterior contraction + model-selection consistency for softmax-gated MoE incl. learnable #experts. Grounds choosing #experts in TRINETRA's GMF head + Bayesian treatment of gate; supports principled expert-count selection.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-017 | 2208.05875
- arXiv/DOI: arXiv:2208.05875
- Authors: Qian; Zhang; Zhao; Zheng; Yu
- Title: Uncertainty Quantification for Traffic Forecasting: A Unified Approach (DeepSTUQ)
- Year / Venue: 2022 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A7 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: calibration / UQ
- Takeaway for TRINETRA: Separates aleatoric vs epistemic UQ for spatio-temporal forecasting + Temperature-Scaling post-calibration.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-018 | 2602.04904
- arXiv/DOI: arXiv:2602.04904
- Authors: Wang; Qin
- Title: DCER: Dual-Stage Compression and Energy-Based Reconstruction for Multimodal Fusion
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: missing-modality fusion
- Takeaway for TRINETRA: Energy-based reconstruction recovers missing modalities + yields intrinsic uncertainty (rho>0.72 w/ error); U-shaped robustness.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-019 | 2505.17501
- arXiv/DOI: arXiv:2505.17501
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: RoHyDR: Robust Hybrid Diffusion Recovery for Incomplete Multimodal
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: missing-modality fusion
- Takeaway for TRINETRA: Diffusion-based recovery of missing modalities at unimodal/multimodal/feature/semantic levels. Second method for TRINETRA to degrade gracefully when a sensor layer drops out rather than failing (robustness alternative to DCER).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-020 | 2303.12783
- arXiv/DOI: arXiv:2303.12783
- Authors: Auer; Gauch; Klotz; Hochreiter
- Title: Conformal Prediction for Time Series with Modern Hopfield Networks (HopCPT)
- Year / Venue: 2023 / NeurIPS 2023
- Read depth: ABS | local note: no | ledger axis/WS: A7 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: conformal under autocorrelation
- Takeaway for TRINETRA: Autocorrelation in time series VIOLATES conformal exchangeability; HopCPT copes with+leverages temporal structure.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-021 | 2502.05709
- arXiv/DOI: arXiv:2502.05709
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Flow-based Conformal Prediction for Multi-dimensional Time Series
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A7 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: conformal multi-dim
- Takeaway for TRINETRA: Conformal for multi-dim TS via flow + classifier-free guidance; non-asymptotic marginal + finite-sample conditional coverage despite non-exchangeability. Rigorous CP option for TRINETRA's multi-sensor vector forecasts (fix path, Bug #13).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-022 | 2402.01379
- arXiv/DOI: arXiv:2402.01379
- Authors: Fdez-Diaz; Quevedo; Montanes
- Title: Regularized boosting as meta-learner in HPO stacking ensemble
- Year / Venue: 2024 / Neurocomputing
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: stacked-generalization meta-learner
- Takeaway for TRINETRA: Stacking meta-learners can suffer MULTICOLLINEARITY among base-model predictions; boosting meta-learner removes it; Caruana method also robust.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-023 | 2512.01750
- arXiv/DOI: arXiv:2512.01750
- Authors: Zhang; Yu; He; Song; Zhang; Letaief
- Title: Multimodal Mixture-of-Experts for ISAC in Low-Altitude Wireless Networks
- Year / Venue: 2025 / arXiv (eess.SP)
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: reliability-aware MoE gating + sparse MoE
- Takeaway for TRINETRA: Each modality gets a dedicated expert; a lightweight gate assigns fusion weights by the INSTANTANEOUS informativeness+reliability of each modality; sparse variant activates a subset of experts to cut compute under energy limits.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-024 | 2603.01511
- arXiv/DOI: arXiv:2603.01511
- Authors: Wu; Zhou; Wang; Zhang; Lin; Lv; U; Zheng
- Title: Multimodal Mixture-of-Experts with Retrieval Augmentation for Protein Active Site Identification (MERA)
- Year / Venue: 2026 / arXiv (cs.AI)
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: Dempster-Shafer reliability fusion
- Takeaway for TRINETRA: Flags that performance DEGRADES when unreliable modalities dominate fusion; fixes it with Dempster-Shafer evidence-theory fusion quantifying modality trustworthiness via belief masses + learnable discounting.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-025 | 2410.04833
- arXiv/DOI: arXiv:2410.04833
- Authors: Gordon; Lang; Ressijac; Davies
- Title: Multimodal Fusion Strategies for Mapping Biophysical Landscape Features
- Year / Venue: 2024 / ECCV 2024 Workshop (CV4Ecology)
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: early vs late vs MoE fusion (remote sensing)
- Takeaway for TRINETRA: Empirically compares Early, Late, and Mixture-of-Experts fusion for thermal+RGB+LiDAR geospatial orthomosaics: macro performance similar (late-fusion AUC 0.698) but PER-CLASS recall differs sharply - early fusion best for some targets, MoE...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-026 | 2505.19190
- arXiv/DOI: arXiv:2505.19190
- Authors: Xin; Yun; Peng; Choi; Ballard; Chen; Long
- Title: I2MoE: Interpretable Multimodal Interaction-aware Mixture-of-Experts
- Year / Venue: 2025 / ICML 2025
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: interaction-aware interpretable MoE
- Takeaway for TRINETRA: MoE with interaction experts + weakly-supervised interaction losses that explicitly model heterogeneous cross-modal interactions (complement/contradict/independent) + a reweighting model giving sample- and dataset-level interpretation.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-027 | 2204.07653
- arXiv/DOI: arXiv:2204.07653
- Authors: Xu; Dimasaka; Wald; Noh
- Title: Bayesian Updating of Seismic Ground Failure via Causal Graphical Models and Satellite Imagery
- Year / Venue: 2022 / 17WCEE 2021
- Read depth: ABS | local note: no | ledger axis/WS: A12 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: causal-graph Bayesian multi-hazard fusion
- Takeaway for TRINETRA: Causal-graph Bayesian network fuses geospatial susceptibility proxies + ShakeMap + damage-proxy-maps (InSAR surface change) to jointly update posteriors of UNOBSERVED landslides/liquefaction/building-damage; stochastic variational inference...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-028 | 2509.10348
- arXiv/DOI: arXiv:2509.10348
- Authors: Aperstein; Tzahar; Gottlib; Verber; Shagan Damti; Apartsin
- Title: Multi-pathology Chest X-ray Classification with Rejection Mechanisms
- Year / Venue: 2025 / arXiv (eess.IV)
- Read depth: ABS | local note: no | ledger axis/WS: A7 | phase: n/r
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: selective prediction / abstention + per-class thresholds
- Takeaway for TRINETRA: High-stakes multi-LABEL classifier with two abstention mechanisms (entropy-based + confidence-interval-based rejection) + quantile calibration of rejection thresholds using GLOBAL vs CLASS-SPECIFIC strategies; abstaining on uncertain cases...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-029 | 2610.02777
- arXiv/DOI: arXiv:2610.02777
- Authors: Liu; Kang; Miao; Wang
- Title: Efficient conformal prediction intervals for time series: Online PID-Expert aggregation
- Year / Venue: 2026 / arXiv (stat.ME)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A7 | phase: P2
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P2] conformal under shift (T5/CR-04)
- Takeaway for TRINETRA: PID-Expert online aggregation narrows conformal intervals while holding coverage; rolling analysis shows local coverage-efficiency degradation right after abrupt distribution shifts — i.e.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-030 | 2609.38936
- arXiv/DOI: arXiv:2609.38936
- Authors: Liang; et al.
- Title: Signal-Routed Temperature Scaling for small-budget risk-conditioned calibration
- Year / Venue: 2026 / arXiv
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A7 | phase: P2
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P2] calibration capacity (WS6)
- Takeaway for TRINETRA: SRTS-BCE: 10-param risk-conditioned (K=3) calibrator; at n=250 beats high-capacity heads. Use low-capacity calibrators for tiny hazard-validation sets. Reinforces FM-20 + ProCal.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-031 | 2603.17319
- arXiv/DOI: arXiv:2603.17319
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PIER: Physics-Informed Offline RL with Decoupled Post-hoc Shield
- Year / Venue: 2026 / arXiv
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A12 | phase: P3 | re-cited 2x
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P3] offline/safe-RL WS5; strengthens CR-03
- Takeaway for TRINETRA: IQL + decoupled post-hoc shield; mean −10% but KEY = kills worst-case tail (max −70%, extreme 4.8%→0.5%, variance 3.5x lower); FORECAST-INDEPENDENT (local obs) vs A* degrading 4.5x.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-032 | 2609.38655
- arXiv/DOI: arXiv:2609.38655
- Authors: Tsai; Zahed; Shen; Xie; Lan; Obaid; Hariri; Rastgoftar
- Title: Forward-Invariant Policy Classes for Safe RL in Multicopter Control
- Year / Venue: 2026 / arXiv (eess.SY)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A12 | phase: P3
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P3] safe-RL WS5 (action-library half)
- Takeaway for TRINETRA: Safety-by-construction: finite library of feedback controllers sharing a common Lyapunov certificate → forward invariance under arbitrary switching; any learned policy inherits certificate.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-033 | 2608.19836
- arXiv/DOI: arXiv:2608.19836
- Authors: Brorholt; Galesloot; Jansen; Larsen; Schilling
- Title: Adaptive Probabilistic Shielding by Learning MDPs for Safe RL
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A12 | phase: P3
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P3] safe-RL WS5 (adaptive-shield half)
- Takeaway for TRINETRA: Transition graph known, probabilities LEARNED online; shield conservative early, tightens as estimate sharpens (interval-MDP).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-034 | 2609.15297
- arXiv/DOI: arXiv:2609.15297
- Authors: Stahlhofen; Hermes; Kochs; Vieth; Hammer
- Title: Admissable: Training RL Agents against Adversarial Missingness
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A12 | phase: P3
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P3] robust-RL/missing-modality; sharpens CR-07
- Takeaway for TRINETRA: Formalizes adversarial feature missingness (adversary occludes k MOST-important state features to minimize return); between ℓ∞ perturbations and missing-data.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-035 | 2511.15838
- arXiv/DOI: arXiv:2511.15838
- Authors: Zhu; Guo; Feng; Simeone
- Title: Attention-Based Feature Online Conformal Prediction for Time Series (AFOCP)
- Year / Venue: 2025 / arXiv (cs.LG/cs.IT/eess.SP)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A7 | phase: P3
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P3] feature-space online CP; interval efficiency under shift
- Takeaway for TRINETRA: AFOCP upgrades Online Conformal Prediction: (1) calibrate nonconformity in FEATURE space of pre-trained net (compact sets, suppress nuisance), (2) attention adaptively weights history by relevance (handles non-stationarity/shift).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-036 | 2608.30205
- arXiv/DOI: arXiv:2608.30205
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Diffusion-Based Refinement for Kilometer-Scale Probabilistic Precipitation Nowcasting (exPreCast-ENS)
- Year / Venue: 2026 / arXiv (cs.LG/physics.ao-ph)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A7 | phase: P3
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P3] HAZARD-CORE WHEN layer: conditional residual diffusion, deterministic->probabilistic ensemble
- Takeaway for TRINETRA: exPreCast-ENS: conditional RESIDUAL diffusion turns a deterministic 4km radar nowcaster into a 1km PROBABILISTIC ensemble while correcting systematic bias + spatial redistribution.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-037 | 2007.02038
- arXiv/DOI: arXiv:2007.02038
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Low-Rank Fusion Transformers for Multimodal Sequences
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] low-rank factorized fusion matches larger models with fewer params
- Takeaway for TRINETRA: Multimodal. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-038 | 2204.00102
- arXiv/DOI: arXiv:2204.00102
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Dynamic Multimodal Fusion (DynMM)
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] gating-based data-dependent fusion cuts compute ~46.5% at ~equal acc
- Takeaway for TRINETRA: Grounds FM-5/RL gating. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-039 | 2306.02050
- arXiv/DOI: arXiv:2306.02050
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Provable Dynamic Fusion for Low-Quality Multimodal Data (QMF)
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] uncertainty-estimation yields provably robust quality-aware fusion
- Takeaway for TRINETRA: Grounds FM-1/uncertainty-weighting. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-040 | 2210.17444
- arXiv/DOI: arXiv:2210.17444
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Multimodal Information Bottleneck
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] IB regularization filters noise; SOTA sentiment/emotion
- Takeaway for TRINETRA: Multimodal. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-041 | 2306.16645
- arXiv/DOI: arXiv:2306.16645
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Deep Equilibrium Multimodal Fusion
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] fixed-point DEQ fusion models intra/inter-modal correlations
- Takeaway for TRINETRA: Multimodal. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-042 | 2403.20280
- arXiv/DOI: arXiv:2403.20280
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Sparsely Multimodal Data Fusion (Modal Channel Attention)
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] MCA beats Zorro/EAO on sparse 4-modality via uniform fusion embeddings
- Takeaway for TRINETRA: Missing-modality. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-043 | 2101.08954
- arXiv/DOI: arXiv:2101.08954
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Bayesian Hierarchical Stacking
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] stacking asymptotically optimal; input-varying weights improve
- Takeaway for TRINETRA: Grounds FM-3. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-044 | 2406.15664
- arXiv/DOI: arXiv:2406.15664
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Flat Posterior Does Matter for Bayesian Model Averaging
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] FP-BMA enforces flatness, improving BMA generalization
- Takeaway for TRINETRA: BMA. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-045 | 2510.22054
- arXiv/DOI: arXiv:2510.22054
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Input Adaptive Bayesian Model Averaging (IA-BMA)
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] input-conditional weights more accurate/calibrated
- Takeaway for TRINETRA: Grounds FM-3 adaptive. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-046 | 2505.21857
- arXiv/DOI: arXiv:2505.21857
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Revisiting BMA in the Era of Foundation Models
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] BMA over frozen-feature heads + cheaper OMA scheme
- Takeaway for TRINETRA: BMA. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-047 | 2103.08195
- arXiv/DOI: arXiv:2103.08195
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: BMA for Causality Estimation
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] averaging causal effects over models is Bayes-optimal
- Takeaway for TRINETRA: BMA. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-048 | 2106.12652
- arXiv/DOI: arXiv:2106.12652
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Black Box Variational Bayesian Model Averaging
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] VI-BMA avoids MCMC pitfalls; model-agnostic
- Takeaway for TRINETRA: BMA. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-049 | 2511.16924
- arXiv/DOI: arXiv:2511.16924
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: CBMA: Improving Conformal Prediction through BMA
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] BMA+conformal converges to optimal-efficiency sets under model uncertainty
- Takeaway for TRINETRA: Grounds FM-3 conformal. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-050 | 2503.03213
- arXiv/DOI: arXiv:2503.03213
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Convergence Rates for Softmax Gating MoE
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] param/expert estimation bounds under softmax/sparse/hierarchical gating
- Takeaway for TRINETRA: MoE theory. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-051 | 2405.13997
- arXiv/DOI: arXiv:2405.13997
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Sigmoid Gating More Sample Efficient than Softmax (MoE)
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] sigmoid gating higher sample efficiency + faster expert estimation
- Takeaway for TRINETRA: Grounds FM-5 gate. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-052 | 2305.03288
- arXiv/DOI: arXiv:2305.03288
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Demystifying Softmax Gating in Gaussian MoE
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] Voronoi loss resolves identifiability; MLE convergence rates
- Takeaway for TRINETRA: MoE theory. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-053 | 2410.02935
- arXiv/DOI: arXiv:2410.02935
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Expert Estimation in Hierarchical MoE: Beyond Softmax
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] Laplace gating accelerates expert convergence in HMoE (multimodal)
- Takeaway for TRINETRA: Grounds FM-5. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-054 | 2608.29235
- arXiv/DOI: arXiv:2608.29235
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Uncertainty-Aware Multimodal Anti-UAV via Evidential + Conflict-Discounted Belief
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] EDL+discounted belief fusion converts conflict to uncertainty; ECE 0.057
- Takeaway for TRINETRA: Grounds FM-2. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-055 | 2412.01215
- arXiv/DOI: arXiv:2412.01215
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: EsurvFusion: Evidential Multimodal Survival Fusion
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] Gaussian random fuzzy numbers + reliability-discounting decision fusion
- Takeaway for TRINETRA: Grounds FM-2. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-056 | 2408.13123
- arXiv/DOI: arXiv:2408.13123
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Evidential Deep Partial Multi-View Classification w/ Discount Fusion
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] conflict-aware evidential fusion weights reliability under missing views
- Takeaway for TRINETRA: Evidential. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-057 | 2510.11171
- arXiv/DOI: arXiv:2510.11171
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Multiview Manifold Evidential Fusion (PolSAR)
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] Dempster-Shafer belief-mass fusion of manifold views
- Takeaway for TRINETRA: Evidential. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-058 | 2406.18327
- arXiv/DOI: arXiv:2406.18327
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Multi-modal Evidential Fusion Network (PET/CT MEFN)
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] D-S uncertainty-calibrated decision fusion improves DSC 3.1-3.2%
- Takeaway for TRINETRA: Evidential. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-059 | 2110.01440
- arXiv/DOI: arXiv:2110.01440
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Arithmetic Average Density Fusion Part I
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] AA fusion covariance-consistency; links to covariance intersection/union
- Takeaway for TRINETRA: Grounds FM-1/FM-4. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-060 | 2307.14741
- arXiv/DOI: arXiv:2307.14741
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Optimality of Split Covariance Intersection Fusion
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] SCI optimal conservative covariance bound for 2 estimators
- Takeaway for TRINETRA: Grounds FM-4. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-061 | 2501.07915
- arXiv/DOI: arXiv:2501.07915
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Revisiting Split Covariance Intersection: Correlated Components
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] extends SCI to correlated error components; optimal conservative bounds
- Takeaway for TRINETRA: Grounds FM-4. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-062 | 2603.16768
- arXiv/DOI: arXiv:2603.16768
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Overlapping Covariance Intersection (OCI)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] generalized CI with multi-source structural correlation; SDP-optimal
- Takeaway for TRINETRA: Grounds FM-4. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-063 | 2603.23853
- arXiv/DOI: arXiv:2603.23853
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: SCoOP: Semantic-Consistent Opinion Pooling
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] uncertainty-weighted linear opinion pooling over multi-VLM; AUROC 0.866
- Takeaway for TRINETRA: Grounds PHARAOH operator. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-064 | 2106.01770
- arXiv/DOI: arXiv:2106.01770
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Bayesian Classifier Fusion with Explicit Correlation
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] correlated-Dirichlet generalizes independent opinion pool; Bayes-optimal
- Takeaway for TRINETRA: Opinion pooling. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-065 | 1106.1638
- arXiv/DOI: arXiv:1106.1638
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Combining Predictive Distributions
- Year / Venue: 2011 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] prediction-space theory of linear/log-linear/beta opinion pools + calibration
- Takeaway for TRINETRA: Grounds PHARAOH operator. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-066 | 1207.4144
- arXiv/DOI: arXiv:1207.4144
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Generative Bayesian Model for Aggregating Experts' Probabilities
- Year / Venue: 2012 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] weighted log opinion pool w/ bias/calibration/dependence; external-Bayesian
- Takeaway for TRINETRA: Opinion pooling. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-067 | 2006.15099
- arXiv/DOI: arXiv:2006.15099
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Conductance-based Dendrites Perform Reliability-Weighted Opinion Pooling
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] neuron dynamics implement Bayes-optimal reliability-weighted cue integration
- Takeaway for TRINETRA: Grounds NF-2/PHARAOH. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-068 | 2206.04568
- arXiv/DOI: arXiv:2206.04568
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Byzantine-Resilient Decentralized Robust Aggregation (IOS)
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] iterative outlier-scissor aggregation w/ provable guarantees
- Takeaway for TRINETRA: Robust aggregation (P16 tie). Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-069 | 2506.23183
- arXiv/DOI: arXiv:2506.23183
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A Practical and Secure Byzantine Robust Aggregator
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] quasi-linear-time robust aggregator; nullifies 10 poisoning attacks
- Takeaway for TRINETRA: Robust aggregation. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-FUS-070 | 1811.03761
- arXiv/DOI: arXiv:1811.03761
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: RSA: Byzantine-Robust Stochastic Aggregation
- Year / Venue: 2018 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-FUSION | phase: P22
- Uses (workstream/chapter): WS5 meta-fusion (ch 06), ch 10 shield, ch 12 evaluation
- Core method: [P22] regularization-based robust aggregation under unknown #Byzantine, non-iid
- Takeaway for TRINETRA: Robust aggregation. Source-reported. NEW. P22 fusion.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass


---

## Theme: Evaluation / leakage / cost-loss / decision / baselines  (`REF-EVAL-*`, 58 entries)

_Primary consumer: ch 12 evaluation, ch 24 decision log. The ledger axis/WS code that mapped each paper into this theme is printed per entry for traceability._

#### REF-EVAL-001 | 2104.11422
- arXiv/DOI: arXiv:2104.11422
- Authors: Sawada; Kanai; Kotani
- Title: Socio-meteorology: flood prediction social preparedness and cry wolf effects
- Year / Venue: 2021 / arXiv (physics.geo-ph/soc-ph)
- Read depth: ABS | local note: yes | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: cry-wolf: false alarms destroy trust & preparedness
- Takeaway for TRINETRA: Builds a socio-hydrological model coupling flood, social collective MEMORY, collective TRUST in the warning system, and preparedness actions; realistically reproduces the CRY-WOLF effect (many false alarms undermine credibility and suppress...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-002 | 2604.04265
- arXiv/DOI: arXiv:2604.04265
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Governance-Constrained Agentic AI: Blockchain-Enforced Human Oversight for Safety-Critical Wildfire Monitoring
- Year / Venue: 2026 / arXiv (cs.AI)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: human-in-loop oversight for autonomous alerts
- Takeaway for TRINETRA: Argues purely AUTONOMOUS alert dissemination in safety-critical disasters risks false-alarming, governance failure, and lack of verifiable responsibility; proposes structurally-defined human control + cryptographically-verifiable accountabi...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-003 | 2311.11491
- arXiv/DOI: arXiv:2311.11491
- Authors: Leblanc; Germain
- Title: On the Relationship Between Interpretability and Explainability in Machine Learning
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: interpretability vs explainability are complementary
- Takeaway for TRINETRA: Position paper: interpretability (inherently-readable models) and explainability (post-hoc explanations of black boxes) are NOT substitutes - each mitigates the other's shortcomings, and high-stakes decisions need both.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-004 | 2101.09429
- arXiv/DOI: arXiv:2101.09429
- Authors: Islam; Eberle; Ghafoor; Ahmed
- Title: Explainable Artificial Intelligence Approaches: A Survey
- Year / Venue: 2021 / arXiv (cs.AI/LG)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: XAI method taxonomy for high-stakes adoption
- Takeaway for TRINETRA: Survey of XAI methods (local/global, model-agnostic/specific) and the open challenge that black-box opacity blocks AI adoption in high-stakes domains; recommends paths to human-centred AI.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-005 | 2509.11789
- arXiv/DOI: arXiv:2509.11789
- Authors: Aderinola; Palmerini; D'Ascanio; Chiari; Klenk; Becker; Caulfield; Ifrim
- Title: Watch Your Step: Cost-Sensitive Accelerometer Fall Detection in Real-World Streaming
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: cost-sensitive threshold tuning, miss>>FA, Recall 1.0
- Takeaway for TRINETRA: Real-time streaming fall detection WITHOUT prior knowledge of events; introduces cost-sensitive learning that tunes the DECISION THRESHOLD using a cost function reflecting that missed falls are costlier than false alarms; achieves Recall 1....
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-006 | 2605.11348
- arXiv/DOI: arXiv:2605.11348
- Authors: Jeong; Vishnubhatla; Jiang; Harrison; Raglin; Liu
- Title: LLMs for Causal Relations Extraction in Social Media: Validation Framework for Disaster Intelligence
- Year / Venue: 2026 / arXiv (cs.CL)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: LLM causal graphs vs model priors - risk flagged
- Takeaway for TRINETRA: Tests whether LLMs can extract causal relations from informal/fragmented disaster social-media posts; proposes an expert-grounded eval comparing LLM causal graphs to reference graphs from disaster reports AND assesses whether extracted rela...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-007 | 2410.20707
- arXiv/DOI: arXiv:2410.20707
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DisasterQA: A Benchmark for Assessing LLM Performance in Disaster Response
- Year / Venue: 2024 / arXiv (cs.CL)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: LLMs often confidently wrong on disaster advice
- Takeaway for TRINETRA: Benchmark evaluating LLM disaster-response knowledge; central question is whether LLMs SHOULD be used for advice/decision-making in a disaster; finds accuracy/confidence issues that caution against uncritical reliance.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-008 | 2503.14621
- arXiv/DOI: arXiv:2503.14621
- Authors: Farayola; Akintola; Fagbohun; Oforgu; Kayode; Chimezie; Kadri; Oludotun; Ogbeide; Michael
- Title: Reducing False Ventricular Tachycardia Alarms in ICU Settings: A Machine Learning Approach
- Year / Venue: 2025 / ICMLT 2025
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: ML false-alarm suppression, ROC-AUC>0.96, alarm fatigue
- Takeaway for TRINETRA: Tackles ICU false-arrhythmia alarms that cause ALARM FATIGUE and compromise safety; uses the VTaC benchmark of annotated VT alarms, extracts time + frequency-domain waveform features, trains DL to classify TRUE vs FALSE alarms; ROC-AUC>0.96...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-009 | 2109.07745
- arXiv/DOI: arXiv:2109.07745
- Authors: Zhao; Xu; Lovreglio; Kuligowski; Nilsson; Cova; Wu; Yan
- Title: Estimating Wildfire Evacuation Decision and Departure Timing Using Large-Scale GPS Data
- Year / Venue: 2021 / arXiv (cs.CY)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: evacuation compliance ~46%, self/shadow evacuees dominate
- Takeaway for TRINETRA: Uses large-scale GPS data to infer wildfire evacuation behaviour (2019 Kincade Fire); classifies self-evacuees, shadow evacuees, evacuees-under-warning, ordered-evacuees; finds self+shadow evacuees were >HALF of all evacuees, and total evac...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-010 | 2512.14683
- arXiv/DOI: arXiv:2512.14683
- Authors: Bertsimas; Ma; Villalobos Carballo; Singh; Laskowski; Mather; Kombert; Haronian
- Title: Early Warning Index for Patient Deteriorations in Hospitals
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: human-in-loop multimodal EWS, SHAP, 3 risk tiers, deployed
- Takeaway for TRINETRA: Multimodal ML Early Warning Index predicts aggregate risk (ICU admission, rapid-response dispatch, mortality) from structured+unstructured EHR; KEY design = HUMAN-IN-THE-LOOP: clinicians help set alert THRESHOLDS and interpret outputs, enha...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-011 | 2605.08198
- arXiv/DOI: arXiv:2605.08198
- Authors: Yesmin
- Title: FairHealth: Open-Source Python Library for Trustworthy Healthcare AI in Low-Resource Settings
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: fairness+explainability+equity toolkit for LMIC, disaster-aid module
- Takeaway for TRINETRA: Open-source library for trustworthy ML in low-resource/LMIC settings (e.g. Bangladesh); modules for federated learning w/ homomorphic encryption, INTERSECTIONAL FAIRNESS metrics, fuzzy-SHAP explainability for LOW-BANDWIDTH decision support,...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-012 | 2505.14510
- arXiv/DOI: arXiv:2505.14510
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: BACON: A fully explainable AI model with graded logic for decision making problems
- Year / Venue: 2025 / arXiv (cs.AI)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: fully-explainable, human-tunable graded-logic decision model
- Takeaway for TRINETRA: Argues that high-stakes autonomous decisions (healthcare/security/finance/robotics) need models that are not only accurate but FULLY EXPLAINABLE and HUMAN-TUNABLE for end-to-end transparency; introduces BACON, a graded-logic decision model....
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-013 | 2405.11533
- arXiv/DOI: arXiv:2405.11533
- Authors: Goren; Galil; El-Yaniv
- Title: Hierarchical Selective Classification
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: abstain by COARSENING prediction under uncertainty; hierarchical risk-coverage guarantee
- Takeaway for TRINETRA: Extends selective classification to a HIERARCHICAL setting: instead of a binary predict/reject, the model REDUCES SPECIFICITY under uncertainty (backs off to a coarser class), using the class hierarchy; formalizes hierarchical risk+coverage...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-014 | 2406.04745
- arXiv/DOI: arXiv:2406.04745
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Confidence-aware Contrastive Learning for Selective Classification
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: generalization bound shows FEATURE-level optimization improves selective classification; CCL-SC
- Takeaway for TRINETRA: Provides a GENERALIZATION BOUND for selective classification showing that optimizing FEATURE layers (not just the classification head) improves selective performance; proposes CCL-SC (confidence-aware contrastive learning) that similarizes...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-015 | 2210.08975
- arXiv/DOI: arXiv:2210.08975
- Authors: Einstein; Moss; Kochenderfer
- Title: Prioritizing emergency evacuations under compounding levels of uncertainty
- Year / Venue: 2022 / IEEE GHTC
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: evacuation / alarm policy
- Takeaway for TRINETRA: MDP evacuation-prioritization under 3 nested uncertainty levels; optimized MDP beats 8 heuristics; extra model-uncertainty layers add complexity w/o gain.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-016 | 2311.10228
- arXiv/DOI: arXiv:2311.10228
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Data-Driven Bayesian Network Models of Hurricane Evacuation Decision Making
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: people-at-risk / human response
- Takeaway for TRINETRA: Bayesian networks model real evacuation decisions from hurricane questionnaires; compliance is probabilistic, not guaranteed.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-017 | 2608.04225
- arXiv/DOI: arXiv:2608.04225
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Evacuation Planning for Disaster Preparedness: An Adaptive Robust Optimization Approach
- Year / Venue: 2026 / arXiv (math.OC)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: evacuation under uncertainty
- Takeaway for TRINETRA: First adaptive-robust model jointly optimizing shelter location + route + supply prepositioning under worst-case evacuee uncertainty.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-018 | 2103.15156
- arXiv/DOI: arXiv:2103.15156
- Authors: Meng; Dong
- Title: Ridesharing Evacuation Model of Disaster Response
- Year / Venue: 2021 / IISE 2020
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: evacuation logistics
- Takeaway for TRINETRA: MIP ridesharing evacuation; counterintuitively, more vehicles for carless isn't always most efficient; strategy varies by disaster scale.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-019 | 2412.05777
- arXiv/DOI: arXiv:2412.05777
- Authors: Tang; Wang; Delle Monache
- Title: Strategizing Equitable Transit Evacuations: A Data-Driven Reinforcement Learning Approach
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: equitable evacuation RL
- Takeaway for TRINETRA: Models bus evacuation as an MDP solved by RL using real GTFS transit + OSM networks; dynamically reroutes buses to minimize total evacuation time WHILE prioritizing equity-priority communities; beats rule-based/random.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-020 | 2602.14676
- arXiv/DOI: arXiv:2602.14676
- Authors: Lischka; Kulcsar
- Title: GREAT-EER: Graph Edge Attention Network for Emergency Evacuation Responses (Bus Evacuation Orienteering Problem)
- Year / Venue: 2026 / arXiv (cs.AI)
- Read depth: ABS | local note: yes | ledger axis/WS: A13 | phase: n/r | re-cited 3x
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: evacuation routing + MILP bound
- Takeaway for TRINETRA: Defines NP-hard Bus Evacuation Orienteering Problem (evacuate max people in fixed time); DRL+graph-learning gives sub-second routes, with an MILP formulation to BOUND the optimality gap + estimate how many vehicles meet a quota.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-021 | 2502.17701
- arXiv/DOI: arXiv:2502.17701
- Authors: Chen; Wang; Sun; Zhao; Xu
- Title: From Perceptions to Decisions: Wildfire Evacuation Decision Prediction with Behavioral-Theory-informed LLMs (FLARE)
- Year / Venue: 2025 / arXiv (cs.AI)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: evacuee behavior modeling
- Takeaway for TRINETRA: FLARE integrates behavioral theory + CoT reasoning + memory-based RL to predict INDIVIDUAL evacuation decisions (comply vs stay); +20% over theory-informed baselines, cross-event generalizable; notes conflicting individual preferences + imp...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-022 | 2601.06664
- arXiv/DOI: arXiv:2601.06664
- Authors: Rafi; Hasan
- Title: Reinforcement Learning-Guided Dynamic Multi-Graph Fusion for Evacuation Traffic Prediction (RL-DMF)
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: evacuation traffic forecasting
- Takeaway for TRINETRA: RL-guided dynamic multi-graph fusion forecasts evacuation traffic flow; 95% acc @1h, 90% @6h on 12 Florida hurricanes incl. unseen Milton 2024; RL-based feature masking for interpretability.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-023 | 2103.03413
- arXiv/DOI: arXiv:2103.03413
- Authors: Tsai; Rastogi; Kitanidis; Field
- Title: Routing algorithms as tools for integrating social distancing with emergency evacuation
- Year / Venue: 2021 / Scientific Reports
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: n/r
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: evacuation routing (CVRP) RL
- Takeaway for TRINETRA: Casts evacuation as Capacitated Vehicle Routing solved by Deep RL vs Sweep algorithm; DRL gives more efficient routing but the gain cannot offset added constraints (social distancing) as vehicle capacity nears household size.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-024 | 2511.21364
- arXiv/DOI: arXiv:2511.21364
- Authors: Islam; Hossen; Arif; Al Noman; Rahman
- Title: BanglaMM-Disaster: multimodal transformer framework for disaster classification in Bangla
- Year / Venue: 2025 / IEEE SPICSCON 2025
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A13 | phase: P2
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P2] crowd layer (T2/Rule19)
- Takeaway for TRINETRA: 5037 Bangla social posts (caption+image), 9 classes; early fusion 83.76% (text-dominant). Treat social media as low-weight corroborating signal, never standalone alarm; multilingual constraint; recall collapses during real events.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-025 | 2007.05848
- arXiv/DOI: arXiv:2007.05848
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Fighting Disaster Misinformation in Latin America (#Verificado19S Mexico 2017 Earthquake)
- Year / Venue: 2020 / arXiv (cs.CY/cs.SI)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A13 | phase: P3
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P3] crisis informatics WS2/WS3 (T3)
- Takeaway for TRINETRA: Mixed-methods study of citizen-led cross-platform verification (#Verificado19S). Users: Twitter to triage needs/news → WhatsApp/Messenger to mobilize OFFLINE action; a trusted bridging org (neither govt nor pure-crowd) kept info credible.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-026 | 2609.38552
- arXiv/DOI: arXiv:2609.38552
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Fairness Theatre: Post-Hoc Fairness Interventions in Vendor-Controlled Early Warning Systems
- Year / Venue: 2026 / arXiv (cs.LG/cs.CY)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A13 | phase: P3
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P3] bias-fairness/EWS governance (Rule 19)
- Takeaway for TRINETRA: Procured black-box EWS leave only output-tweaking; post-hoc fairness fixes can be 'theatre' (look fair, don't change outcomes); most need group labels+outcomes at config, results hinge on chosen constraint+accuracy floor.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-027 | 2610.08227
- arXiv/DOI: arXiv:2610.08227
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: How Many Independent Samples Does a Satellite Image Contain?
- Year / Venue: 2026 / IEEE TGRS 2026
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A13 | phase: P4
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P4] PROVES C-01: spatial-CV is a theorem not a best-practice
- Takeaway for TRINETRA: Finite-sample upper + matching lower bound: effective sample size of a spatially-correlated image (range r) is Theta(n^2/r^2), NOT n^2; block holdout with separation g=Theta(r*log(n/delta)) achieves optimal generalization; random holdout UN...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-028 | 2510.22016
- arXiv/DOI: arXiv:2510.22016
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Cost-Sensitive Evaluation for Binary Classifiers
- Year / Venue: 2025 / arXiv (cs.LG) v2
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A13 | phase: P4
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P4] FORMALIZES C-14: Total Classification Cost as the selection criterion
- Takeaway for TRINETRA: Total Classification Cost (TCC) is the ideal model-selection criterion; weighted-accuracy family and its relation to TCC; metric taxonomy (anti-diagonal / main-diagonal / globally-robust) w.r.t.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-029 | 2605.14365
- arXiv/DOI: arXiv:2605.14365
- Authors: Choi; Park; Kwon; Jeong
- Title: LoMETab: Beyond Rank-1 Ensembles for Tabular Deep Learning
- Year / Venue: 2026 / arXiv (cs.LG) CC BY 4.0
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A13 | phase: P4
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P4] C-02 CURRENCY (2026): DL-vs-GBDT gap narrowed to a TIGHT CLUSTER, GBDT still exceptionally strong
- Takeaway for TRINETRA: Tabular-DL method paper that OPENS with the current (May 2026) consensus: 'recent tabular benchmarks increasingly show a tight performance CLUSTER rather than a clear hierarchy' among GBDT, attention-based, and implicit ensembles (TabM); 'G...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-030 | 2610.05790
- arXiv/DOI: arXiv:2610.05790
- Authors: Hossain; Vaghasiya; Dwivedi; Kurmi; Banerjee
- Title: FairRSFM: A Biome-Aware Benchmark and Debiasing Framework for Remote Sensing Foundation Models
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A13 | phase: P5
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P5] WS4/WS6: aggregate RS metrics HIDE geographic/biome disparities
- Takeaway for TRINETRA: Biome-aware benchmark over GEO-Bench (m-EuroSAT/m-BigEarthNet/m-SA-Crop-Type) + MMEarth20K; frozen-backbone, 3 seeds; worst-group + Normalized Failure Range + ECE + EOdd/DPM.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-031 | 2603.00604
- arXiv/DOI: arXiv:2603.00604
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Data-Centric Benchmark for Label Noise Estimation and Ranking in RS Binary Building Segmentation
- Year / Venue: 2026 / arXiv (cs.CV) v2
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: P5
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P5] WS6: estimate+rank LABEL NOISE before trusting a dataset
- Takeaway for TRINETRA: Data-centric benchmark for methods that ESTIMATE and RANK label noise in remote-sensing binary building segmentation ground truth.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-032 | 2605.28174
- arXiv/DOI: arXiv:2605.28174
- Authors: Rodriguez; Angulo Morales; Alwahas; Elias Lara; Thoker; Johansen; Ghanem; Maestre; McCabe
- Title: FLORO: A Multimodal Geospatial Foundation Model for Ecological RS Across Sensors and Scales
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: P5
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P5] WS8/WS6: availability-aware (missing-modality) small-corpus GFM
- Takeaway for TRINETRA: Masked-AE GFM pretrained on a SMALL but diverse corpus (S1+S2+SkySat+elevation+UAV) with AVAILABILITY-AWARE inputs flagging which bands/modalities are present -> unified input space under sensor variability (= our missing-modality mask, DC-...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-033 | 2608.21646
- arXiv/DOI: arXiv:2608.21646
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Power-Performance Characterization of TinyML Systems
- Year / Venue: 2026 / arXiv (cs.LG) orig ICCD 2022
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: P6
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P6] TinyML: per-layer energy/latency cost
- Takeaway for TRINETRA: Systematic power/latency characterization of TinyML across MCUs/models/libraries/OS, with a per-abstraction-layer cost model.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-034 | 2609.30272
- arXiv/DOI: arXiv:2609.30272
- Authors: (EdgeIntelligenceLab)
- Title: ENAS: Hardware-Aware NAS for TinyML on Resource-Constrained MCUs
- Year / Venue: 2026 / arXiv (cs.LG) OSS
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: P6
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P6] TinyML: peak activation RAM = binding constraint
- Takeaway for TRINETRA: GPU-free NAS with static feasibility + cell-based search on 8 MCUs (20 KB-1 MB SRAM); SOURCE-REPORTED 79.4% acc on STM32H743 + 2.41x/1.70x search speedups; key: ENAS models use much lower PEAK ACTIVATION RAM, 'the binding constraint for MCU...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-035 | 2608.25646
- arXiv/DOI: arXiv:2608.25646
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: LDAC-Net: Learnable Multi-Lag Differencing for Drift-Robust Low-Cost MOX Gas Sensors
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: P6
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P6] gas sensor: MQ-family drift handling
- Takeaway for TRINETRA: Learnable multi-lag differencing + window-conditioned affine normalization for slow transients/drift/offset in low-cost MOX (MQ-2/MQ-135 family).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-036 | 2507.17071
- arXiv/DOI: arXiv:2507.17071
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Sensor Drift Compensation in E-Nose Gas Recognition via Knowledge Distillation
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: P6
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P6] gas sensor: drift compensation double-edged
- Takeaway for TRINETRA: On UCI Gas Sensor Array Drift; KD drift compensation beats DRCA by up to 18% acc / 15% F1 over 30 partitions; warns prior methods OVER-compensate and lose class variance.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-037 | 2604.21527
- arXiv/DOI: arXiv:2604.21527
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A Temporal Deep Learning Framework for Calibration of Low-Cost Air Quality Sensors
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: P6 | re-cited 2x
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P6] calibration: temp/humidity cross-sensitivity
- Takeaway for TRINETRA: LSTM calibration of low-cost PM2.5/PM10/NO2 vs reference (OxAria), beating RF via temporal deps + lagged features + harmonic time encodings.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-038 | 2511.19810
- arXiv/DOI: arXiv:2511.19810
- Authors: Kar et al.
- Title: RESPIRE: Outlier-Resistant Semi-Parametric Transferable Calibration of Low-Cost AQ Sensors
- Year / Venue: 2025 / arXiv (cs.LG/stat.ML) OSS
- Read depth: ABS | local note: no | ledger axis/WS: A13 | phase: P6
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P6] calibration/INDIA: season/site/unit transfer
- Takeaway for TRINETRA: INDIA + CO specific: calibrates low-cost CO sensors from a large multi-site/multi-season/multi-sensor mobile AQ deployment (4 sites, 2 seasons, 6 packages); provable outlier resistance + explainable overfitting flags.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-039 | 2006.07484
- arXiv/DOI: arXiv:2006.07484
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: dagger: Reproducible ML Experiment Orchestration
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: tooling | phase: P17-T7
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P17-T7] tracks the state-tree of multi-stage experiments for provenance/reuse
- Takeaway for TRINETRA: FEATURES F-17 Wave-1; src-reported qualitative. Experiment tracking/reproducibility. Source-reported. NEW. P17_scout_notes T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-040 | 2302.04054
- arXiv/DOI: arXiv:2302.04054
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Towards Inferential Reproducibility: LMEM + GLRT for ML Comparisons
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: tooling | phase: P17-T7
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P17-T7] model nondeterminism as variance via LMEM + GLRT + reliability coefficient
- Takeaway for TRINETRA: FEATURES F-17 Wave-1; src-reported. The 'real-win' significance gate every feature passes. Source-reported. NEW. P17_scout_notes T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-041 | 2108.13264
- arXiv/DOI: arXiv:2108.13264
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Deep Reinforcement Learning at the Edge of the Statistical Precipice (rliable)
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] point estimates over few runs mislead; use IQM + stratified-bootstrap CIs + performance profiles
- Takeaway for TRINETRA: R-significance; src-reported. Binds every 'win' with 2302.04054 gate. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-042 | 1810.03993
- arXiv/DOI: arXiv:1810.03993
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Model Cards for Model Reporting
- Year / Venue: 2018 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] short docs reporting disaggregated performance + intended/out-of-scope use
- Takeaway for TRINETRA: R-model-card; src-reported. Build-phase documentation standard. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-043 | 1803.09010
- arXiv/DOI: arXiv:1803.09010
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Datasheets for Datasets
- Year / Venue: 2018 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] every dataset ships a datasheet (motivation/composition/collection/uses)
- Takeaway for TRINETRA: R-datasheet; src-reported. For every collected dataset + candidate benchmark. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-044 | 1909.10155
- arXiv/DOI: arXiv:1909.10155
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Verified Uncertainty Calibration
- Year / Venue: 2019 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] Platt/temperature scaling less calibrated than reported, ECE unmeasurable; scaling-binning + low-variance ECE
- Takeaway for TRINETRA: R-calibration; src-reported. Central to uncertainty-gated alerts. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-045 | 2608.29463
- arXiv/DOI: arXiv:2608.29463
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Benchmark Contamination: A Taxonomy Organized by Defeated Mitigation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] 5-type contamination taxonomy + 4-field disclosure; inter-coder reliability collapses under skew (kappa~0.21)
- Takeaway for TRINETRA: O-contamination; src-reported (ID date-stamp unusual, mild caution). Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-046 | 2403.02558
- arXiv/DOI: arXiv:2403.02558
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: MI-CLAIM-GEN: Minimum-Information Reporting for Generative Clinical AI
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] extends MI-CLAIM with training/eval, interpretability, reproducibility, cohort, ethics items
- Takeaway for TRINETRA: R-checklist; src-reported. Template for a safety-critical advisory reporting checklist. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-047 | 2003.12206
- arXiv/DOI: arXiv:2003.12206
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Improving Reproducibility in Machine Learning Research (NeurIPS Reproducibility Program)
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] code-submission policy + reproducibility challenge + ML Reproducibility Checklist
- Takeaway for TRINETRA: R-checklist; src-reported. Reproducibility process to adopt. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-048 | 2306.09562
- arXiv/DOI: arXiv:2306.09562
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Reproducibility in NLP: What Have We Learned from the Checklist?
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] 10405 responses: reporting rose; only 46% claim open-source code; more Yes correlates w/ acceptance
- Takeaway for TRINETRA: R-checklist; src-reported. Evidence checklists improve reporting. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-049 | 2310.18018
- arXiv/DOI: arXiv:2310.18018
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: NLP Evaluation in Trouble: Measuring LLM Data Contamination per Benchmark
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] position: define contamination levels, per-benchmark measures, flag papers
- Takeaway for TRINETRA: O-contamination; src-reported. Inflated scores -> wrong conclusions. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-050 | 2406.18326
- arXiv/DOI: arXiv:2406.18326
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PaCoST: Paired Confidence Significance Testing for Benchmark Contamination
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] paired confidence test on benchmark vs matched; nearly all models/benchmarks suspected contaminated
- Takeaway for TRINETRA: O-contamination/metric-critique; src-reported. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-051 | 2410.16186
- arXiv/DOI: arXiv:2410.16186
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A Benchmark Contamination Report for Multilingual Benchmarks
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] black-box test over 7 benchmarks x 7 LLMs; almost all show contamination signs
- Takeaway for TRINETRA: O-contamination; src-reported. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-052 | 2502.17259
- arXiv/DOI: arXiv:2502.17259
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Detecting Benchmark Contamination Through Watermarking
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] watermark benchmarks pre-release; detect training radioactivity (p=1e-3 for +5% ARC-Easy)
- Takeaway for TRINETRA: O-contamination; src-reported. Pre-release watermarking for our candidate benchmark (C-05). Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-053 | 2509.00072
- arXiv/DOI: arXiv:2509.00072
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Test of Time: Rethinking the Temporal Signal of Contamination
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] post-cutoff decay sensitive to question construction; LLM-transformed questions erase temporal pattern
- Takeaway for TRINETRA: O-contamination/shift; src-reported. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-054 | 2501.19047
- arXiv/DOI: arXiv:2501.19047
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Understanding Model Calibration: A Visual Exploration of ECE
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] re-highlights ECE drawbacks, motivates alternative calibration measures
- Takeaway for TRINETRA: R-calibration/metric-critique; src-reported. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-055 | 2306.04590
- arXiv/DOI: arXiv:2306.04590
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Proximity-Informed Calibration (ProCal/PIECE)
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: yes | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] proximity bias across 504 ImageNet models persists after temp scaling; proximity-informed ECE + correction
- Takeaway for TRINETRA: R-calibration; src-reported. Calibration must account for proximity bias. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-056 | 2404.13503
- arXiv/DOI: arXiv:2404.13503
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Calibration Error for Decision Making
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] decision-theoretic Calibration Decision Loss; separations from ECE
- Takeaway for TRINETRA: R-calibration/metric-critique; src-reported. Decision-relevant calibration for alert gating. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-057 | 2607.26191
- arXiv/DOI: arXiv:2607.26191
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Position: Evaluation Scores Are Perishable Knowledge Claims
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] averaging mixed signals -> trust inflation; scores need metadata/scope/expiry; HELM mean vs weakest-link top-5 disjoint
- Takeaway for TRINETRA: O-metric-critique/uncertainty-honesty; src-reported. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-EVAL-058 | 2106.05532
- arXiv/DOI: arXiv:2106.05532
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: How Robust Are Model Rankings? A Leaderboard Customization Approach
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: REPORTING | phase: P20
- Uses (workstream/chapter): ch 12 evaluation, ch 24 decision log
- Core method: [P20] difficulty-weighting shows leaderboards adversarially gameable; top models not always best
- Takeaway for TRINETRA: O-metric-critique; src-reported. Don't over-trust single-number rankings. Source-reported. NEW. P20 reporting scan.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass
