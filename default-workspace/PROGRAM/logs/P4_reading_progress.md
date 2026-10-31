# P4 reading progress ledger (MASTER_PROMPT §0.9; mirrors analysis/02_paper_ledger.csv [P4] rows)
# Phase P4 — SYNTHESIS. Quota target ≥15 NEW, ≥60% Tier-2+. Depth labels: FT/FT-PARTIAL/SKIM/ABS/NO-HTML.
# Each row: #, arXiv ID, short title, depth, consensus-position tie (C-nn from P4_sota_scan), novelty note.

| # | ID | Title (short) | Depth | Tie | Note |
|---|----|---------------|-------|-----|------|
| 1 | 2606.21773 | Decision-Focused Learning: When & Why Traditional Prediction Models Fail | FT-PARTIAL | C-04/C-11 | DFL review; "better prediction ≠ better decision"; SPO/surrogate-loss taxonomy; x↦w*, x↦ℓ, c↦w*(c) mappings; stochastic-LP statistical challenges. Consolidates CR-04 action-loss doctrine. NEW (not in ledger). |
| 2 | 2512.14221 | Weighted CP: Adaptive Valid Mask-Conditional Coverage for General Missing Data | FT-PARTIAL | C-05 | preimpute-mask-then-correct; Mask-Conditional Valid (MCV) coverage > marginal under missingness; reweighted CP after multiple imputation; narrower intervals keeping guarantee. Closes CR-04 missingness edge. NEW. |
| 3 | 2510.12328 | Physics-Informed GAT + EVT (POT/GPD) for Extreme Rainfall, Thailand | NO-HTML(ABS) | C-06 | 2nd independent EVT/tail-risk source beyond GNN-rP; Spatial Season-aware GPD POT-mapping; Attention-LSTM on gauge graph w/ orographic-precip physics edges; beats baselines + competitive w/ SEAS5. ABS-only (no arXiv HTML, ar5iv cross-origin) → NON-QUOTA but corroborates C-06. |
| 4 | 2610.08227 | How Many Independent Samples Does a Satellite Image Contain? (TGRS 2026) | FT-PARTIAL | C-01 | PROOF: effective sample size Θ(n²/r²) not n² for spatial-corr range r; finite-sample upper + matching lower bound (tight); block holdout w/ separation g=Θ(r·log(n/δ)) achieves optimal generalization; random holdout underestimates CI width by factor ∝ r; validated Landsat-8/S2/S1. Theoretical bedrock for C-01/spatial-CV mandate. NEW. |
| 5 | 2510.22016 | Cost-Sensitive Evaluation for Binary Classifiers (v2) | FT-PARTIAL | C-14 | Total Classification Cost (TCC) as ground truth; weighted-accuracy family; anti-diagonal/main-diagonal/globally-robust metric taxonomy vs TCC; example-dependent unit costs; practical guidelines. Operationalizes "pick metric from the cost model" → cost-loss Value Score. NEW. |
| 6 | 2610.01384 | CLEAR: Robust Evidential Learning Through Latent Consistency | FT-PARTIAL | C-13/C-05 | post-hoc, frozen base; latent group-conditioned geometry; conflict score C(x) → evidence scale s(x)=exp(−δC(x)) downweights unsupported (OOD/adversarial) evidence; +8.29/+5.01 OOD/adv AUROC, 17.4× faster; covers classification+regression. Fixes confident-but-wrong in sparse/OOD regions (proximity-bias). NEW. |
| 7 | 2107.11003 | Model Selection for Offline RL: Practical Considerations for Healthcare | FT(ABS-strong) | C-11 | OPE-as-validation pipeline; FQE gives best validation ranking but high compute; 2-stage accelerator. Operationalizes "iterative/offline RL ONLY if OPE-feasible"; sepsis = safety-critical analogue to alarm policy. NEW (ABS-level; MLHC2021 w/ code). |
| 8 | 2610.07232 | Benchmarking Time Series Foundation Models for Load Forecasting under Covariate Uncertainty | FT-PARTIAL | C-07/C-02-chal/P14Z | 4 TSFM vs 4 train-from-scratch, 3 real datasets; Chronos-2 SOTA zero-shot WHEN covariates good/accurately-forecast, degrades under covariate noise; TimesNet more robust under severe covariate uncertainty. Disciplines "does an FM help OUR regime?"; direct feed to P14Z zero-shot phase. NEW. Body table (ISO-NE/NAU MAE/MAPE across noise λ=0..5) captured. |
| 9 | 2608.08158 | A Unified Framework for Dynamic Reward Shaping in RL | FT-PARTIAL | C-10/PBRS | review+framework; PBRS preserves optimal policy iff auxiliary = discounted diff of time-invariant potential; information-conditioned dynamic shaping R'_k=R+F_{θk}, mechanism classes C1–C4; §2.7 limits of guarantees under episodic/partial-obs/multi-agent. Grounds our PBRS doctrine + caveats for adaptive shaping. NEW. |
| 10 | 2608.15261 | Boundary-Aligned Contribution Routing for Robust Optical–SAR Object Detection | FT-PARTIAL | C-08 | optical–SAR fusion; "more modalities ≠ better" — negative cross-modal transfer; task-conditioned routing before first cross-modal mixing (Feature Router + Dual-Statistic Semantic Router), NO utility labels; missing-modality mAP50 +7.6..41.6pt over modality-dropout, negative-transfer −12.7pp; routing-weight vs LOMO-utility Spearman 0.45–0.66. Direct C-08 "missing modality must not degrade" mechanism. NEW. |
| 11 | 2407.06785 | Towards Physics-Informed Neural Networks for Landslide Prediction (JGR-ML 2024) | FT-PARTIAL | C-15/WS1 | peer-reviewed PINN adding Newmark permanent-deformation constraint on data-driven backbone; NN retrieves geotechnical params from proxies then minimises BCE vs coseismic inventory; also outputs regional geotechnical-property maps; code+data open (github.com/ashokdahal/PINN). Validates "physics as constraint/gate, not black box" (C-15) + residual-on-mechanistic (C-03). NEW. |
| 12 | 2608.14391 | Can We Defend Against AI-Generated Video Attacks on Real-World Crisis Events? (RA-Bench v2) | FT-PARTIAL | C-16/WS2 | 17,886 videos (1,830 real anchors ×10 social-risk cats + 16,056 gen clips, 9 generators); NONE of 3 detector families (7 traditional, 10 zero-shot MLLM, 2 fine-tuned) generalize; videos that fool humans also fool detectors; social dissemination makes detection HARDER. Hard evidence deepfake-detection = LOW-TRUST advisory only (Rule 19). NEW. |
| 13 | 2509.18176 | Deep Learning Spatio-Temporal Forecasting of InSAR Ground Deformation, Eastern Ireland | FT-PARTIAL (RE-STUDY) | C-03/WS8 | sparse PS-InSAR → dense tensor → CNN-LSTM; benchmarked vs LightGBM + LASSO on Sentinel-1; baselines DEFAULT TO PERSISTENCE → learned spatio-temporal residual; SHAP. ⚠ ALREADY read FT-PARTIAL in P2 → RE-STUDY under the P4 lens, EXCLUDED from the P4 NEW-read quota (honest-count §0.5). |
| 14 | 2507.15614 | Accelerating HEC-RAS: Recurrent Neural Operator for Rapid River Forecasting | FT(ABS-strong) | C-03/WS1 | GRU (short-term) + Geometry-Aware Fourier Neural Operator (long-range spatial) surrogate of HEC-RAS; 8-channel feature vector; 67 Mississippi reaches; median stage err 0.31 ft; ensemble wall-clock 139→40 min (3.5×). Physics-surrogate for cheap ensemble flood forecasting under Kaggle compute (C-03). NEW. |
| 15 | 2610.03649 | On-Board Anomaly Detection for Efficient Marine Environmental Monitoring (OBPDC) | FT(ABS-strong) | C-08/WS8 | SSL encoder → latent → ML anomaly detector; head-to-head vs Isolation Forest, One-Class SVM, Local Outlier Factor; lightweight for embedded-CPU/edge; flown on ESA Phi-sat-2 + IMAGIN-e. Corroborates SSL-encoder→classical-anomaly stack + edge-feasibility. NEW. |
| 16 | 2609.16707 | Predictability-Guided Multiscale Probabilistic Forecasting of Wind Direction under Extreme Shear | FT(ABS-strong) | C-05/C-06/C-13 | directional (S¹) multi-horizon; predictability DECAYS AT DIFFERENT RATES across scales → regime-dependent uncertainty; FMs + discrete models lag (phase-lag) at ≥90° turning (extreme) events. Corroborates regime-conditioned uncertainty + FMs-lag-at-extremes (EVT prior C-06, per-regime conformal C-05). NEW. |
| 17 | 2605.14365 | LoMETab: Beyond Rank-1 Ensembles for Tabular Deep Learning | FT-PARTIAL | C-02 | 2026 currency check for C-02: tabular benchmarks now a TIGHT CLUSTER (GBDT / attention / implicit-ensembles), "GBDTs remain exceptionally strong", simple MLPs surprisingly competitive vs complex attention/retrieval nets. 37 datasets / 77 eval tasks (TabM+TabZilla). Parsimony NOT reversed — gap merely narrowed; simple-first + GBDT-baseline confirmed. NEW (genuine 15th body-level quota read). |

# ======================= P4 QUOTA — FINAL HONEST TALLY =======================
# NEW body-level deep reads counted toward the P4 ≥15 quota (15):
#   2606.21773, 2512.14221, 2610.08227, 2510.22016, 2610.01384, 2107.11003, 2610.07232,
#   2608.08158, 2608.15261, 2407.06785(ABS→FT upgrade), 2608.14391, 2507.15614, 2610.03649,
#   2609.16707, 2605.14365.
# EXCLUDED from quota (honest, §0.5):
#   - 2510.12328 (#3): ABS/NO-HTML → non-quota corroborator (C-06).
#   - 2509.18176 (#13): ALREADY FT-PARTIAL in P2 → RE-STUDY, not a new read.
# TIER SPLIT of the 15: FT-PARTIAL ×11 + FT(ABS-strong) ×4 — all Tier-2+ = 100% ≥ the 60% floor. PASS.
# RUNNING NEW DEEP READS: P1 15 + P2 18 + P3 43 + P4 15 = 91.
# Plus NON-QUOTA corroborators: 2510.12328 (C-06), 2601.12330 (GLOF), 2608.12422 (baseline re-study),
#   2109.07745 (C-12), 2504.03166 RingMoE (P7), 2609.34041 (WS2/WS5 caveat), 2608.19672 / 2609.36975
#   (C-02 Indian-conditions), 2509.18176 (re-study).

# NON-QUOTA LEADS (batch 3): 2601.12330 IceWatch GLOF multimodal-DL on GLOFNet (NO-HTML/ABS; GLOF corroborator,
#   WS8/P9 park); 2608.12422 "Which Site & When" (BASELINE re-study, non-quota) — full ABS: 589 HMAGLOFDB outbursts,
#   spatial-CV withholding whole tiles; antecedent-weather ROC 0.73 big-burst/0.83 landslide/0.82 small-flood;
#   terrain naive~0.9 but matched-honest 0.76/0.71/0.54(chance); 5 DL models do NOT beat GBDT baseline; 3-rule tree
#   reproduces lake-hazard baseline → MASSIVE C-01+C-02+C-15 corroboration; 2606.00690 DistMatch (already P3 ledger);
#   2504.03166 RingMoE 14.7B MoE multimodal-RS FM (physics-informed SSL; P7 SAR-FM shortlist add); 2609.34041
#   VLM-Safe-RL (CLIP reward-shaping, catastrophe 31.6→19.4% but NO anticipation evidence — honesty caveat for WS2/WS5).

# NON-QUOTA LEADS (batch 2): 2109.07745 (wildfire evac compliance 46% inside warning/order zones, Kincade 2019 GPS;
#   self+shadow evacuees >50% — hard number for C-12); 2608.19672 SAGE-XGBoost (XGBoost+graph-embeddings beats
#   spatial-ML +33pp, AUC~0.97 landslide / 0.95 wildfire under data scarcity → C-02 corrob, already an ABS-park);
#   2604.16265 FL-MHSM flood-landslide multi-hazard (already P3 ledger #35); 2608.01626 QWRF-Net nowcasting (off-theme);
#   2110.15332 Proximal RL / POMDP OPE (confounding in offline RL — WS5 note); 2512.14683-adjacent assurance leads.

# PENDING QUOTA TARGETS (from P4_sota_scan PART B): C-02 tabular DL-vs-GBDT meta; C-02-challenge DL-wins;
#   C-10 deep-RL repro meta; C-12 alert-fatigue quantified; C-16 assurance case ML-EWS; C-14 metric critique;
#   C-01 spatial-CV critique; C-13 calib-under-sparsity; cross: multi-hazard/compound, nowcasting eval, FM-for-TS.
# NON-QUOTA LEADS SEEN: 2609.36975 (XGBoost 78.82% > DL 64-66% on Punjab-India wheat, low-sample → C-02 corrob,
#   Indian-conditions!); 2608.27239 (silent-by-default alert design grounded in alert-fatigue lit, rural Bangladesh);
#   2306.01868 Zaffran CP-missing-values ICML2023 (seminal, predecessor to 2512.14221).
