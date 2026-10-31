# KEY TECHNICAL QUESTIONS — DRAFT (Phase P0, Task 0.8)
#
# Drafted WITHOUT searching (P0 is quota-exempt and does no new reading). These are the
# questions the literature program (P1–P18) must answer with evidence. Each is phrased so a
# paper can CONFIRM / REFUTE / QUALIFY it. Locked and prioritized in P1. Grouped by the 14
# search axes (A1–A14) and the workstreams. Life-safety framing (Rule 19) applies throughout:
# the goal is real benefit to people in Uttarakhand & Himachal, not a benchmark score.

## Cross-cutting (highest priority — these gate everything)
- Q0.1 Evaluation: what is the correct spatial-CV protocol (tile-withheld) so reported skill
  is not inflated by trained-on-neighbourhood leakage? What simple baselines (persistence,
  gradient-boosted, 3-rule decision tree) must every deep model beat first?
  (Seed: 2608.12422, 2509.18176. Ties FM-01/FM-02, CR-02.)
- Q0.2 Honesty: for each proposed component, is there full-text (not abstract-only) evidence
  it works in a setting close to ours (Himalaya, free data, cheap sensors)? Where only
  far-domain evidence exists, is it a labeled transfer hypothesis?
- Q0.3 Parsimony: where does a simpler method match a complex one within uncertainty, so we
  should prefer the simpler one? (CR-02, CR-03, FM-12.)

## WS1 physics (A1, A3, A4, A11)
- Q1.1 Infinite-slope FS and Iverson transient infiltration: what are the correct forms, and
  do the pre-existing report's slope term (Bug #3), suction-stress sign (Bug #2), inverse-
  velocity α (Bug #4), and Bayes threshold (Bug #1) survive re-derivation? CLASS A/B/C?
- Q1.2 Intensity–Duration thresholds for the Indian Himalaya: what are the VERIFIED
  constants (Caine/Dahal-Hasegawa/Garhwal, Bug #15), and is a single threshold even valid vs
  a region-conditioned distribution? (CR-02 argues distribution.)
- Q1.3 Can sparse noisy sensor data be assimilated into the slope-hydrology state (EnKF /
  diffusion assimilation) rather than a one-shot FS computation? (Seed 2107.07687, 2510.08488.)
- Q1.4 GLOF / dam-break / runout: which free-data signals (InSAR moraine deformation +
  antecedent weather) actually discriminate which lake and when? (Seed 2608.12422.)

## WS1/WS8 remote sensing + anomaly (A1, A2, A8, A14)
- Q2.1 Does a bespoke RS/SAR SSL encoder beat a general-purpose vision encoder on OUR tasks
  at achievable scale, and should it reconstruct features (HOG/NDI) not raw pixels on SAR?
  (CR-01; seed 2510.17014, 2310.18653.)
- Q2.2 What anomaly formulation (forecast-residual, Deep SVDD, isolation forest, XGBoost)
  best flags rare hazard onset without a too-tight normal boundary (high FA)? (Seed
  2501.15196, 2308.09296, 2510.09452.)
- Q2.3 How do we detect out-of-distribution sensor regimes on TIME SERIES so the forecaster
  does not emit a confident-but-wrong alarm? (Seed 2502.15901; FM-07.)
- Q2.4 How is cross-region/seasonal drift (Uttarakhand↔Himachal, calm↔monsoon) detected and
  safely adapted without destabilising a life-safety model? (Seed 2205.13723, 2411.15204.)

## WS6 uncertainty / robustness (A7, A14)
- Q3.1 Which conformal method stays valid under autocorrelation, missingness, and alarms
  that change behaviour (endogenous shift)? What coverage can we actually guarantee? (Seed
  2303.12783, 2406.05405; CR-04; FM-03.)
- Q3.2 How do we report calibrated aleatoric + epistemic uncertainty on every forecast
  rather than a bare point estimate? (Seed 2208.05875.)

## WS5 RL + fusion (A5, A6, A12)
- Q4.1 Is multi-stage offline RL justified, or does a one-step / TD3-BC baseline match it at
  lower variance given few disaster episodes? Can we even do valid OPE? (CR-03; seed
  2106.08909, 2506.00505, 2203.04236; FM-08.)
- Q4.2 What safety-shield rules (FS<1→Orange, tilt>5°/day→Red, 24h rain>150mm→Orange,
  GLOF→Red) are realizable (non-contradictory) and how is that proven? (Seed 2507.23603;
  FM-05.)
- Q4.3 Does the gated meta-fusion head achieve genuine per-modality expert specialization,
  or does routing collapse to a standing committee? How do we audit it? (CR-05; seed
  2601.03425, 2604.00801.)
- Q4.4 How should the reward encode cry-wolf/trust erosion so a false alarm costs more than a
  flat penalty? (Seed 2104.11422, 2311.10228; FM-09; R-10.)

## WS7 IoT + WS3 alerting (A9, A10, A13)
- Q5.1 Can a ≤₹2000 node (MCU + LoRa IN865–867 + tilt/moisture/piezo/rain + solar) be
  specified from VERIFIED Indian listings, and what does it measure usefully? (OQ-05; FM-10.)
- Q5.2 How should solar nodes duty-cycle so they still transmit hazard data during storms
  (lowest solar, highest need)? (Seed 1511.08331, 2311.01743; FM-10.)
- Q5.3 Which comms family (LoRa + DTN store-carry-forward) keeps alerts flowing when storms
  cut the backhaul? (Seed 1308.2907, 2603.15945; FM-11.)
- Q5.4 How do faulty/compromised sensors get detected before they fabricate or mask a
  hazard? (Seed 1509.06065; FM-04.)
- Q5.5 River-Eye LSPIV: how is surface-velocity/discharge estimated with uncertainty and
  gap-filling under occlusion/night/turbidity on cheap cameras? (Seed 2507.20102, 2312.06461.)

## WS3/WS4 decision + CCTV (A13)
- Q6.1 How is "people-at-risk" calibrated to ACTUAL evacuation compliance (stochastic, not
  guaranteed) for the disruption cost? (Seed 2311.10228, 2210.08975.)
- Q6.2 What explanation (XAI) does a disaster manager need to audit WHY an alarm fired, for
  governance and SACHET/CAP acceptance? (Seed 2101.09429, 2604.04265.)

## Deployment (A13, P19)
- Q7.1 What India-specific regulatory/privacy/standards constraints govern a real deployment
  (LoRa band, CCTV data, NDMA/SDMA integration), as research notes flagged for expert review?
- Q7.2 What is genuinely novel/publishable here vs already in the field (gap map → honest
  contribution claims)?

# NOTE: this is a DRAFT. P1 locks the final list, assigns priority scores, and maps each
# question to the papers that answer it (building analysis/10_reading_queue.csv priorities).
