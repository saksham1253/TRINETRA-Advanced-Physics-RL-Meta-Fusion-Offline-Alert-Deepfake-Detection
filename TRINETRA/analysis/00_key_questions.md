# KEY TECHNICAL QUESTIONS — FINALIZED (Phase P1, Task 5)
#
# Locks the P0 draft (analysis/00_key_questions_draft.md). Each question is phrased so a paper
# can CONFIRM / REFUTE / QUALIFY it, carries a PRIORITY (P0=gating, P1=high, P2=normal), the
# PHASE expected to answer it, and the SEED/EVIDENCE paper IDs. P1 additions are tagged
# [+P1] and cite the 15 NEW quota papers read 2026-10-06. Life-safety framing (Rule 19)
# applies throughout: the goal is real benefit to people in Uttarakhand & Himachal, not a
# benchmark score. Nothing here asserts OUR system works (Rule 16) — these are OPEN questions.
#
# PRIORITY LEGEND:  P0 = gates all downstream work (answer first);
#                   P1 = high (answer within the owning phase);  P2 = normal.
# Each entry: [PRIORITY | owning-phase] question (seeds; ties).

## Cross-cutting (P0 — these gate everything)
- Q0.1 [P0 | P5/P7] Evaluation protocol: what is the correct tile-withheld spatial-CV so skill
  is not inflated by trained-on-neighbourhood leakage, and which simple baselines (persistence,
  gradient-boosted, 3-rule tree) must every deep model beat first?
  Seeds: 2608.12422, 2509.18176. [+P1] reinforced by 2405.00031 (compact>large; resolution is
  a safety hyperparameter), 2606.21130 (XGBoost EWS: high recall 0.914 at modest AUC 0.697).
  Ties FM-01/FM-02/FM-12, CR-02.
- Q0.2 [P0 | all] Honesty of evidence: for each component, is there full-text (not abstract-only)
  evidence it works in a setting close to ours (Himalaya, free data, cheap sensors)? Where only
  far-domain evidence exists, is it a LABELED transfer hypothesis? (Read-depth honesty, §0.5.)
- Q0.3 [P0 | all] Parsimony: where does a simpler method match a complex one within uncertainty,
  so we prefer the simpler? CR-02, CR-03, FM-12. [+P1] 2311.14110 (don't trust a learned policy
  unless OPE is feasible), 2608.26304 (classical two-stage stochastic optimization may replace RL
  in the decision layer).
- Q0.4 [P0 | P5] **[+P1] Metric honesty:** which metrics may be compared across zones/seasons of
  DIFFERENT base rates, and which may NOT? What is the single PRIMARY decision metric?
  Seeds: 2206.09981 (metric value is a function of imbalance → never rank across ratios),
  2601.05921 (cost-loss Value Score as primary EWS metric, reported across a C/L range), E-06/E-07.
  Ties FM-21.
- Q0.5 [P1 | P9/P16] **[+P1] System reliability / tech-debt:** what AI-system technical debt
  (data, model, config, ethics debt; training/serving skew) must be controlled so the pipeline
  does not silently degrade in the field? Seeds: 2103.09783. Ties FM-19.

## WS1 physics (A1, A3, A4, A11)
- Q1.1 [P1 | P7] Do the report's slope term (Bug #3), suction-stress sign (Bug #2), inverse-
  velocity α (Bug #4) and Bayes threshold (Bug #1) survive re-derivation? CLASS A/B/C each?
  [+P1] Bug #1 threshold p*=C_FA/(C_FA+C_miss) must come from the SAME cost-loss model as the
  Value Score verification metric (2601.05921, E-07) — threshold and score must agree.
- Q1.2 [P1 | P7] Verified I–D constants for the Indian Himalaya (Caine/Dahal-Hasegawa/Garhwal,
  Bug #15), and is a single threshold valid vs a region-conditioned DISTRIBUTION? (CR-02.)
- Q1.3 [P2 | P7] Can sparse noisy sensor data be assimilated into slope-hydrology state (EnKF /
  diffusion assimilation) rather than a one-shot FS? Seeds 2107.07687, 2510.08488.
- Q1.4 [P1 | P7] GLOF/dam-break/runout: which free-data signals (InSAR moraine deformation +
  antecedent weather) discriminate which lake and when? Seed 2608.12422.

## WS1/WS8 remote sensing + anomaly (A1, A2, A8, A14)
- Q2.1 [P1 | P7] Does a bespoke RS/SAR SSL encoder beat a general-purpose vision encoder on OUR
  tasks at achievable scale (feature-recon on SAR, not raw pixels)? CR-01 four contenders
  {DINOv2 2304.07193, CROMA 2311.00566, Copernicus-FM 2503.11849, AnySat 2412.14123}.
  [+P1] 2306.04590: transformers are MORE prone to proximity-bias miscalibration than CNNs →
  a calibration-reliability cost against transformer encoders (feeds CR-01/CR-02, FM-20).
- Q2.2 [P1 | P7] Which anomaly formulation (forecast-residual, Deep SVDD, isolation forest,
  XGBoost) flags rare onset without a too-tight normal boundary? Seeds 2501.15196, 2308.09296.
  [+P1] 2412.13439 (MIP per-class ensemble weighting + bounded selection for edge),
  2606.21130 (cost-thresholded XGBoost high-recall EWS).
- Q2.3 [P1 | P7/P16] OOD detection on TIME SERIES so the forecaster does not emit a confident-
  but-wrong alarm. Seed 2502.15901; FM-07. [+P1] 2404.19452 (low-energy drift detector
  ADWIN/HDDM_W as the online monitor; accuracy-vs-energy frontier).
- Q2.4 [P1 | P16] Cross-region/seasonal drift (Uttarakhand↔Himachal, calm↔monsoon) detection +
  SAFE adaptation of a life-safety model. Seeds 2205.13723, 2411.15204. [+P1] 2404.19452.

## WS6 uncertainty / robustness (A7, A14)
- Q3.1 [P0 | P7/P16] Which conformal method stays valid under autocorrelation, missingness, and
  endogenous shift (alarms change behaviour)? What coverage can we ACTUALLY guarantee?
  Seeds 2303.12783, 2406.05405; CR-04; FM-03. [+P1] BASELINE FOUND: 2010.09107 EnbPI (ensemble
  OOB-residual intervals, no exchangeability/splitting/retraining, explicit coverage-gap bound).
  Still OPEN under abrupt drift + missingness (2406.05405 unread).
- Q3.2 [P1 | P7] Report calibrated aleatoric + epistemic uncertainty on EVERY forecast, not a
  bare point estimate. Seed 2208.05875. [+P1] 2306.04590 ProCal: standard temp-scaling does NOT
  fix proximity-bias overconfidence in sparse regions → calibration must be proximity-aware and
  must flag low-density inputs (FM-20).

## WS5 RL + fusion (A5, A6, A12)
- Q4.1 [P1 | P15] Is multi-stage offline RL justified, or does a one-step / TD3-BC baseline match
  it at lower variance given few disaster episodes, and can we even do valid OPE? CR-03; seeds
  2106.08909, 2506.00505. [+P1] 2311.14110 DataCOPE: run an OPE-FEASIBILITY gate before trusting
  any learned policy; if infeasible, fall back to one-step / shielded fixed policy (FM-22).
- Q4.2 [P1 | P15] Which safety-shield rules (FS<1→Orange, tilt>5°/day→Red, 24h rain>150mm→Orange,
  GLOF→Red) are realizable (non-contradictory) and how is that proven? Seed 2507.23603; FM-05.
- Q4.3 [P1 | P15] Does the gated meta-fusion (GMF) head achieve genuine per-modality specialization
  or collapse to a standing committee? CR-05; seeds 2601.03425, 2604.00801. [+P1] **GMF novelty
  is now DISCIPLINED (CR-06):** 2604.25512 (PHISHREV knowledge-gated post-hoc revision) + stacking
  (Wolpert-1992) + Meta-AAD + RL model-selection are prior art → reframe GMF as a COMPOSITION of
  known parts, novelty = "not found in N sources searched" for the specific per-zone Mondrian-
  conformal + monotone-shield combination.
- Q4.4 [P0 | P15] How should the reward encode cry-wolf/trust erosion so a false alarm costs more
  than a flat penalty? Seeds 2104.11422 (trust ODE), 2311.10228; FM-09; R-10. [+P1] 2410.06388
  (multimodal pedestrian alerts: trust/habituation measured empirically — alert fatigue is a
  real, modellable human-response failure, not an abstraction).
- Q4.5 [P1 | P15] **[+P1] Missing-modality robustness:** does fusion survive a dropped sensor
  layer, and at what cost? Seeds 2310.03986 (fusion is NOT free-lunch robust; <1% extra params
  recovers most performance). Ties CR-07, FM-15.

## WS7 IoT + WS3 alerting (A9, A10, A13)
- Q5.1 [P1 | P6] Can a ≤₹2000 node (MCU + LoRa IN865–867 + tilt/moisture/piezo/rain + solar) be
  specified from VERIFIED Indian listings, and what does it measure usefully? OQ-05; FM-10.
- Q5.2 [P1 | P6/P15] Solar-node duty-cycling that still transmits during storms (lowest solar,
  highest need). Seeds 1511.08331, 2311.01743, 1909.01968 (ACES Q-learning, HP-01); FM-10.
  [+P1] 2404.19452 (choose the lowest-ENERGY drift detector that holds accuracy — same
  accuracy-vs-energy discipline applies to on-node compute budgets).
- Q5.3 [P1 | P6] Which comms family (LoRa + DTN store-carry-forward) keeps alerts flowing when
  storms cut the backhaul? Seeds 1308.2907, 2603.15945; FM-11.
- Q5.4 [P1 | P6/P16] How are faulty/compromised sensors detected before they fabricate or mask a
  hazard? Seed 1509.06065; FM-04. [+P1] 2103.09783 (training/serving skew + config debt is a
  silent-degradation sibling of sensor fault; audit both — FM-19).
- Q5.5 [P2 | P6] River-Eye LSPIV: surface-velocity/discharge with uncertainty and gap-filling
  under occlusion/night/turbidity on cheap cameras. Seeds 2507.20102, 2312.06461.

## WS3/WS4 decision + CCTV (A13)
- Q6.1 [P1 | P15] How is "people-at-risk" calibrated to ACTUAL evacuation compliance (stochastic,
  not guaranteed) for the disruption cost? Seeds 2311.10228, 2210.08975. [+P1] 2608.26304
  (flood evacuation EQUITY + two-stage stochastic optimization — compliance and equity belong in
  the decision objective, and a stochastic program is a non-RL alternative), 2410.06388 (trust).
- Q6.2 [P1 | P19] What explanation (XAI) does a disaster manager need to audit WHY an alarm fired,
  for governance and SACHET/CAP acceptance? Seeds 2101.09429, 2604.04265.
- Q6.3 [P2 | P5] **[+P1] e2e disaster-detection reference designs:** what do recent end-to-end
  detection→response pipelines (compact models, resolution-as-safety-hyperparameter) teach about
  our pipeline shape? Seeds 2405.00031 (SegNet wildfire e2e). Ties CR-02.

## Safety-critical ML methodology (A8 — [+P1] new group)
- Q8.1 [P0 | P5/P9] **[+P1]** What assurance structure (safety case / GSN, continuous assurance)
  should a life-safety ML EWS carry, and how is it maintained as the model updates? Seeds
  2209.11632 (continuous ML safety assurance, GSN safety-case). Ties Rule 19, Q0.5, R-register.
- Q8.2 [P1 | P5] **[+P1]** What evaluation methodology validates a MULTI-COMPONENT ML pipeline
  (not just one model) — per-base-rate protocol, cost-loss Value Score, OPE-feasibility, coverage,
  calibration-under-sparsity? Seeds 2206.09981, 2601.05921, 2311.14110, 2010.09107, 2306.04590.
  (This is the P1 "evaluation stack" assembled from the quota reads.) Ties Q0.4, Q3.1, Q4.1.

## Deployment (A13, P19)
- Q7.1 [P1 | P19] India-specific regulatory/privacy/standards constraints (LoRa band, CCTV data,
  NDMA/SDMA integration), as research notes flagged for expert review.
- Q7.2 [P0 | all] What is genuinely novel/publishable here vs already in the field (honest gap
  map)? [+P1] 2604.25512 already disciplines the GMF claim (CR-06) — apply the same "absence in
  N sources searched" test to every claimed contribution.

# PRIORITY SUMMARY (gating P0 questions, answer first):
#   Q0.1 spatial-CV + baselines; Q0.2 evidence honesty; Q0.3 parsimony; Q0.4 metric honesty;
#   Q3.1 valid conformal coverage; Q4.4 cry-wolf reward; Q8.1 assurance structure; Q7.2 novelty.
# These eight gate the credibility of everything downstream and must be settled before any
# performance claim (Rule 16).
#
# LOCKED 2026-10-06 (P1). Changes after this require a DECISIONS.md entry.

<!-- ===================== P4 UPDATE (2026-10-07, append-only; D-012) ===================== -->
# MASTER_PROMPT §P4 task 7: answers found / still open / new questions. The locked set above is
# preserved verbatim; this block records resolution status after 91 program-era deep reads.
# Logged as DECISIONS.md D-012 (key-questions change after the P1 lock).

## ANSWERED in the literature (now design decisions in analysis/07_design_changes.md)
- Q0.1 spatial-CV + baselines → **ANSWERED, now PROVEN.** 2610.08227 (effective N=Θ(n²/r²); buffer
  g=Θ(r·log(n/δ)); random holdout CI underestimate ∝ r). Decision DC-01. Residual: estimate r per region.
- Q0.3 parsimony → **ANSWERED.** DL does not reliably beat GBDT; only a learned residual on a mechanistic
  backbone wins (2608.12422, 2609.36975 Indian, THREAD I 7×). Decisions DC-02/DC-06.
- Q0.4 metric honesty → **ANSWERED.** Total Classification Cost / cost-loss Value Score; metric value ∝ base
  rate (2510.22016). Decision DC-02.
- Q3.1 valid conformal coverage → **ANSWERED.** Approximate-under-stability; must be action-loss AND
  mask-conditional AND online (2609.14821, 2512.14221, 2610.02777). Decision DC-03. Resolves CR-04.
- Q4.x decision layer → **ANSWERED.** Staged policy fixed→one-step offline RL→iterative-only-if-OPE-feasible
  (2606.21773 DFL, 2107.11003 OPE). Decision DC-10. Resolves C-11.
- Q (reward shaping) → **ANSWERED.** Potential-based + time-invariant or prove the exception (2608.08158).
  Decision DC-11.
- Q (missing modality) → **ANSWERED.** Worst-case drop-k eval + utility routing (2609.15297, 2608.15261,
  2605.06643, 2607.24683). Decisions DC-05/DC-09. Resolves CR-07.
- Q8.1 assurance / low-trust media → **PARTLY ANSWERED.** 2608.14391 (no deepfake detector generalizes) makes
  the low-trust-advisory rule evidence-backed (DC-04); the GSN/continuous-assurance structure itself is still
  thinly sourced on arXiv → carry to P11/P13 (non-arXiv assurance literature).

## STILL OPEN (carried forward with owner phase)
- Q0.2 evidence honesty — ongoing discipline (every number traces to a note; Rule 21). Permanent.
- Q4.4 cry-wolf reward — THIN (one hard number 2109.07745=46% compliance); human-compliance model needs
  non-arXiv NHESS/IJDRR evidence. Owner P13/P15. (DC-18)
- Q6.2 XAI for alarm audit — seeds only; owner P19.
- Q7.1 India regulatory/privacy — research notes, owner P19.
- Q7.2 novelty honesty — GMF reframed as a COMPOSITION (CR-06/DC-17); apply the same test to every claim.
- G2 cross-zone conformal coupling (research item, P14); G3 ₹2k River-Eye LSPIV accuracy (P6/P8);
  G7 rockfall hazard coverage (P7).

## NEW QUESTIONS raised by the P4 reads
- Q9.1 [P14Z] **Do foundation models actually help OUR regime?** 2610.07232 shows a TSFM is SOTA zero-shot
  only with accurate covariates and DEGRADES under covariate noise (ours is noisy). Pre-registered benchmark
  vs a robust from-scratch model + residual, under DC-01 CV, scored by DC-02. New contradiction CR-08.
- Q9.2 [P7] **Does a coseismic-landslide PINN structure transfer to a rainfall/pore-pressure trigger?**
  (2407.06785 is coseismic; borrow structure, swap physics). FM-39.
- Q9.3 [P14] **How is action-loss + mask-conditional + online conformal composed into ONE calibrator**
  without the three objectives fighting each other? (DC-03 integration question.)
- Q9.4 [P7/P14] **Where do we have a calibrated solver/gauge to train a physics surrogate, and what do we
  do in ungauged catchments?** (2507.15614; DC-14/FM-40.)
- Q9.5 [P15] **How do we probe the alarm policy's ANTICIPATION (lead-time), not just its catastrophe count?**
  (2609.34041 hollow-safety caveat; DC-16.)
