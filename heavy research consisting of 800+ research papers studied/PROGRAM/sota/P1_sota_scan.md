# P1 SOTA SCAN — end-to-end disaster / fire early-warning SYSTEMS
# Phase P1, Task 1. Scope: system-level state of the art for multi-sensor early-warning
# pipelines (not individual components — those are P2+). Targets only; NO claims about our
# own system (honesty rule 16). Evidence tags: [FT]/[ABS]/[LV]. This scan is seeded from the
# baseline corpus + the pre-existing report and is extended as P1 reading proceeds.

## Phase: P1 — Baseline papers and system model
## Date: 2026-10-05

## 1. State of the art for end-to-end hazard early-warning systems
Operational / published system archetypes relevant to TRINETRA:
- **LHASA v1/v2 (NASA)** — global Landslide Hazard Assessment for Situational Awareness.
  Decision-tree (v1) → machine-learning + susceptibility (v2) over satellite rainfall (GPM
  IMERG) + static susceptibility. Baseline PDFs present: lhasa1, lhasa2, lhasa2_stanley2021,
  lhasa_forecast_khan, lhasa_kirschbaum2018. [to read FT in P1] This is the single most
  directly comparable operational SYSTEM — our architecture must be positioned against it.
- **I–D threshold systems** (Caine-type) — intensity–duration rainfall thresholds driving
  regional landslide warnings. Simple, operational, interpretable. (WS1; P7.)
- **GLOF hazard screening** — e.g. 2608.12422 [FT]: free-satellite InSAR deformation +
  antecedent weather, spatial-CV, strong-baseline discipline; explicitly a prioritisation
  aid, NOT a predictor. Sets the honesty bar.
- **Flood/precip nowcasting** benchmarks (TrajGRU/HKO-7 lineage) — short-horizon radar/precip
  prediction (WS3; P2/P3).

## 2. Published numbers to meet or beat (targets table) — filled as read
| Task | System/method | Metric | Published value | Protocol | Paper | Tag |
|------|---------------|--------|-----------------|----------|-------|-----|
| GLOF/landslide site+time | gradient-boosted baseline + 3-rule tree | ROC-AUC | weather-timing 0.73/0.83/0.82; susceptibility honest 0.76/0.71/0.54 | spatial-CV, whole-tile withheld, matched controls | 2608.12422 | [FT] |
| Landslide nowcast (global) | LHASA v2 | (to extract) | (to extract FT) | event-based | lhasa2_stanley2021 | [queued] |

## 3. Achievable under OUR limits (Kaggle + ₹2000 hardware)
- A LHASA-class rainfall+susceptibility pipeline is clearly within Kaggle compute (tabular /
  light-CNN). Deep multimodal fusion is feasible only at modest scale; 2608.12422 is the
  cautionary anchor that deep models may not beat gradient-boosting here.
- Edge inference (River-Eye LSPIV, LoRa node) must run on MCU/Pi-class hardware — rules out
  heavy backbones at the edge; favors classical CV + tiny models (WS4/WS7).

## 4. Baselines we MUST use first (fair-comparison requirement)
- **Persistence** (tomorrow = today) for any temporal forecast.
- **Gradient-boosted trees** (XGBoost/LightGBM) for any susceptibility/anomaly tabular task.
- **3-rule decision tree** (ruggedness + monsoon rainfall) — reproduces lake-hazard baseline.
- **I–D threshold** for rainfall-triggered landslides.
- **LHASA v1 decision-tree logic** as an operational reference.
Every deep model must beat ALL applicable baselines UNDER tile-withheld spatial-CV before any
skill is claimed (ties R-01, FM-01, CR-02).

## 5. Gaps the SOTA does NOT cover (feeds gap map + contributions)
- No published system fuses InSAR-SSL anomaly + physics gate + offline-RL alarm policy +
  conformal calibration into one offline-first, India-Himalaya, ≤₹2000-node pipeline (the
  TRINETRA thesis). Whether that integration beats a well-tuned LHASA-class baseline is an
  OPEN empirical question — the central contribution claim to validate honestly (P19).
- Operational systems rarely report calibrated uncertainty or cry-wolf/trust-aware
  thresholds; TRINETRA's conformal + trust-aware reward is a genuine gap (WS6/WS5).

## NOTE
Rows marked [queued] are filled when the corresponding baseline paper is read FT during P1.
