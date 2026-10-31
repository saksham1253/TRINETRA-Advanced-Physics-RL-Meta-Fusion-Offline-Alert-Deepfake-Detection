# P5 SOTA SCAN — Benchmarks, Leaderboards & Datasets per Workstream

Phase P5 · Date 2026-10-07 · RESEARCH-ONLY (§0.1A). This scan precedes dataset selection (§P5 task 1).
It records, per workstream, the datasets/benchmarks that currently define SOTA evaluation, the common
leaderboards/protocols, and the honest gaps for OUR Himalayan life-safety setting. Every arXiv ID here
was surfaced live via the arXiv API this session (see search ledger in PART C). Cost/license are
VERIFIED in DATASETS.md (never assumed here).

Cross-cutting finding carried from P4 (DC-01): several standard benchmarks use RANDOM TILE splits that
leak spatially; GEOID-Flood (2608.02315) and 2610.08227 both make the same point. Our evaluation default
is event-/tile-level block CV with a buffer — this scan flags, per benchmark, whether its native split
is leakage-safe.

---

## WS1 — Physics / hydrology / InSAR deformation (hazard-core)
SOTA eval anchors:
- InSAR deformation forecasting: 2509.18176 (CNN-LSTM, Sentinel-1), Thalia 2505.17782 (global InSAR
  deformation datacubes + benchmark; atmospheric-delay artifacts explicitly modelled), 2606.07374
  (coherence regression from detected SAR, GEE-available ARD → cheap coherence features).
- Flood hydraulics surrogates: 2507.15614 (HEC-RAS Geo-FNO), CAMELS/CAMELS-hourly streamflow (lead).
- Precipitation nowcasting benchmarks: SEVIR, MeteoNet, MRMS, KNMI radar, HKO-7; current SOTA methods
  PG-FMM 2609.37487 (heavy-rain CSI +58.9%), JWS 2610.12189 (17× faster inference), NowcastDiT
  2609.37038, QWRF-Net 2608.01626 (extreme-event subset), IRENE 2609.17175 (ConvGRU ensemble, afCRPS).
- Glacier/GLOF: CryoNet 2605.21527 (central-Himalaya debris-glacier + glacial-lake multimodal mapping),
  2512.24117 (Himalayan glacial-lake SAR, IoU 0.9130), HMAGLOFDB (589 dated outbursts, via 2608.12422).
Leaderboard/protocol: CRPS/CSI at rain thresholds for nowcasting; IoU/F1 for segmentation; skill-over-
persistence for deformation (C-03). GAP: no public Uttarakhand/Himachal multi-hazard forecasting
benchmark with event-level splits — our evaluation set must be assembled from these components.

## WS2 — Misinformation / deepfake / crisis media
SOTA eval anchors: RA-Bench 2608.14391 (AI-generated crisis-video, no detector generalizes);
HUMAID / HUMAID-NER 2609.16964 (60k disaster tweets, span + event labels); CrisisMMD/CrisisNLP (lead,
multimodal crisis social media). Leaderboard/protocol: span-F1 + event-macro-F1 (HUMAID-NER reports
0.841 / 0.761). GAP: crisis-media benchmarks are English/global and detectors FAIL on exactly the
content that matters (Rule 19) → WS2 signals are LOW-TRUST advisory into GMF, never autonomous.

## WS3 — Alerting / forecasting / networks
SOTA eval anchors: nowcasting benchmarks (shared with WS1); CAMELS-hourly for streamflow; HKO-7.
Leaderboard/protocol: lead-time vs CRPS; reliability diagrams. GAP (C-12): human warning-compliance
numbers are NON-arXiv (NHESS/IJDRR) — one hard number so far (46% evac compliance, 2109.07745).

## WS4 — CCTV / vision / scene
SOTA eval anchors: RS pretraining corpora (MillionAID, FireRisk, BigEarthNet, EuroSAT); GEO-Bench and
PANGAEA as the frozen-backbone evaluation suites; FairRSFM 2610.05790 adds a biome-group-robustness
protocol over GEO-Bench + MMEarth. Leaderboard/protocol: macro-F1 / mIoU, now with worst-GROUP metrics
(FairRSFM) and corruption-robustness (REOBench). GAP: no Himalayan-village CCTV benchmark; River-Eye
LSPIV accuracy is unmeasured (G3 → P6/P8).

## WS5 — RL / alarm policy
SOTA eval anchors: offline-RL model-selection (FQE/OPE, 2107.11003); PBRS theory (2608.08158);
DFL/decision-loss (2606.21773). No hazard-specific RL benchmark exists → evaluation is OPE on logged/
simulated episodes with cost-loss (DC-02) + regret vs a threshold policy. GAP: safe-RL anticipation
evidence is thin (2609.34041 caveat).

## WS6 — Robustness / evaluation / efficiency
SOTA eval anchors: spatial-CV theorem (2610.08227); cost-sensitive eval TCC (2510.22016); REOBench
(corruptions); FairRSFM (group robustness); data-centric label-noise benchmark 2603.00604; FLORO
2605.28174 and GDCLD-benchmark 2604.16663 (LoRA/AdaLoRA = −95% trainable params ≈ full-FT accuracy →
Kaggle-budget lever). Leaderboard/protocol: worst-group + corruption + cost-weighted; parameter-
efficiency (PEFT) as a first-class axis for us. 
LoMETab 2605.14365: tabular benchmarks a tight cluster, GBDT still strong → GBDT baseline mandatory.

## WS7 — IoT / edge / TinyML (deep in P6)
SOTA eval anchors: on-board SSL anomaly 2610.03649 (vs iForest/OCSVM/LOF, edge-feasible); LoRa links
(Indian-LoRa 2412.04563 lead). Full treatment in P6.

## WS8 — Anomaly / SSL encoders / multimodal fusion
SOTA eval anchors: SSL EO corpora (SSL4EO-S12, Copernicus-Pretrain, Major-TOM, GeoPlex); anomaly
baselines iForest/OCSVM/LOF/Deep-SVDD; optical-SAR routing 2608.15261; FLORO availability-aware fusion
2605.28174; GEOID-Flood modality-ablation (optical-SAR fusion best for transient flood). Leaderboard/
protocol: AUROC/AUPRC + missing-modality mAP drop (DC-05 worst-case). GAP: anomaly eval must be done
under spatial-CV + worst-case missing-modality masks, which standard RS benchmarks do not enforce.

---

## SOTA-scan takeaways feeding P5 dataset selection
1. FLOOD is the best-served hazard for free, ML-ready, multimodal data (GEOID-Flood, Sen1Floods11,
   ETCI, WorldFloods, MMFlood, Kuro Siwo, CAU-Flood, S1GFloods, STURM-Flood, UFO, FloodsNet).
2. LANDSLIDE has solid open datasets (Landslide4Sense, LMHLD, GDCLD, Bijie, Nepal) but most are
   detection/segmentation on imagery, NOT time-to-failure forecasting (our harder task).
3. GLOF/glacier is thinnest and least Indian-specific (GLOFNet=Karakoram, 2512.24117/CryoNet=Nepal/
   central-Himalaya) → transfer-learning + domain-shift evaluation is unavoidable (register as risk).
4. The field is converging on FROZEN-BACKBONE + WORST-GROUP + CORRUPTION-ROBUST evaluation (GEO-Bench,
   PANGAEA, FairRSFM, REOBench) — our protocol (DC-01/DC-02/DC-05) is aligned with this frontier.
5. PEFT (LoRA/AdaLoRA, −95% trainable params) is the key lever to fit SOTA backbones in the Kaggle
   budget (2604.16663) → KAGGLE_BUDGET.md adopts PEFT-first.
6. Many native splits LEAK spatially; we re-split every adopted dataset to event-/region-level block CV.
