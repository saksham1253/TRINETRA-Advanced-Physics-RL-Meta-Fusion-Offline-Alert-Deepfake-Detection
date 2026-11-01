# REFERENCES — master citation list (MASTER_PROMPT §0.10)

The row-level source of truth for literature is `analysis/02_paper_ledger.csv`
(250 data rows → 235 unique new papers, all abstract-only as of 2026-10-05). This file is
the human-readable reference list, grouped by search axis, built up as papers are promoted
to full-text in P2/P3. It is NOT re-transcribed from the ledger during P0 to avoid
introducing transcription errors into verified identifiers (honesty rule 1).

## How to cite from this project
Every reference must carry: arXiv ID / DOI / stable URL, title, ALL authors (or issuing
body), year, venue, read_depth. Abstract-only items are tagged `[ABS]` and may not be
stated as established fact — only as "the abstract claims …".

## Status (2026-10-05, P0)
- Unique new papers in ledger: 235 (all [ABS]).
- Full-text [FT] promotions: 0 (begin in P2/P3).
- Local baseline corpus (pre-existing, ~110 unique) under `trinetra\papers\`: tracked
  separately; to be merged into this list with explicit [LV]/[FT] tags during P2.

## Axis index (A1–A14) — populated on FT promotion
- A1 InSAR/deformation/GNSS — (pending FT)
- A2 EO foundation models / SSL encoders — (pending FT)
- A3 I–D thresholds / extreme weather / nowcasting — (pending FT)
- A4 transient infiltration / Richards / assimilation — (pending FT)
- A5 offline RL / OPE — (pending FT)
- A6 safe RL / shielding — (pending FT)
- A7 conformal prediction / calibration — (pending FT)
- A8 rare-event / anomaly / EWS verification — (pending FT)
- A9 VAD edge / LSPIV — (pending FT)
- A10 LoRa / LPWAN / DTN / energy harvest — (pending FT)
- A11 GLOF / dam-break / runout / flash-flood — (pending FT)
- A12 multimodal / stacked / MoE fusion — (pending FT)
- A13 evacuation / decision / cost-loss / human response — (pending FT)
- A14 drift / OOD / monitoring — (pending FT)

---

## P3 THEME-GROUPED REFERENCE LIST (43 NEW FT-PARTIAL reads, 2026-10-07)
# Human-readable grouping of the P3 quota set. Row-level truth remains analysis/02_paper_ledger.csv
# ([P3] rows) and per-paper notes in analysis/03_paper_notes/. All [FT-PARTIAL] (D-008: page middles
# pruned by web_fetch; body-table numbers not independently re-verified beyond Audit #9). Novelty =
# "not found in the sources searched" per the search log (rows 158–219), never "does not exist" (Rule 21).

### Theme: Hazard-core — GLOF / landslide / InSAR
- 2512.24117 [FT-PARTIAL] — Adhikari; Regmi; Shrestha (2025, eess.IV→cs.CV) — Himalayan glacial-lake
  S1-SAR semantic segmentation; "temporal-first"; IoU 0.9130; Dockerised ASF-API GLOF-EWS pipeline.
- 2605.17419 [FT-PARTIAL] — RMCL (2026, cs.CV) — displacement-robust landslide EWS under rainfall-
  FORECAST uncertainty; motion-aware contrastive; +37% precision; Japan 19 regions.
- 2005.03221 [FT-PARTIAL] — Anantrasirichai; Biggs et al. — national Sentinel-1 velocity CNN; sparse/
  noisy/scarce-label InSAR recipe (matrix completion, synthetic-from-real-stats, over-wrapping).

### Theme: Hazard-core — precipitation nowcasting / extreme-rain trigger (RESIDUAL doctrine)
- 2609.34836 [FT-PARTIAL] — MW-Nowcast — deterministic structure + flow-matching RESIDUAL; beats
  PySTEPS/SimVPv2/NowcastNet for extreme precip; Relative-Economic-Value cost-loss metric.
- 2608.30205 [FT-PARTIAL] — Park; Song; Chang; Ham; Hong (2026, cs.LG) — exPreCast-ENS conditional
  residual diffusion 4 km→1 km probabilistic ensemble; recovers 38–47% missed heavy-rain px, ~95%
  retention, <1% new FA; 3.4 s/1-h single GPU; MeteoNet transfer.
- 2511.05471 [FT-PARTIAL] — TUPANN — satellite-only (GOES+IMERG) motion+intensity + differentiable
  WARP advection; cross-region/extreme transfer.

### Theme: Hazard-core — extreme-value theory / tail-risk (NEW axis)
- 2509.10362 [FT-PARTIAL] — Wang; Wu; Bi (2025, stat.AP) — GNN-rP: graph NN + r-Pareto (POT) extreme-
  precip risk zoning; node features [μ,σ,max,exceedance-freq]; IMERG 2000–2021 + CMIP6 SSP5-8.5;
  compound rain→flood+landslide; beats two baselines on high-risk-cell detection.

### Theme: Decision-oriented UQ / calibration (alarm-stack capstone, CR-04)
- 2609.14821 [FT-PARTIAL] — Lu; Duan; Zhao; Wang; Fang; Yang; Feng; Gou (2026, cs.LG, ADMA 2026) —
  Decision Risk Adapter + Utility-Aware Calibration; action-loss ≠ predictive coverage; regret −18.7%,
  missed-event 14.2%→9.1%, utility +11.6%, predictive coverage 90.4%, calib error 0.083→0.047.
- 2608.16654 [FT-PARTIAL] — IsoMaxPlus distance-logits: free OOD + ECE 0.0095→0.0026, no outliers/tuning.
- 2609.15297, 2606.04634, 2607.24683 [FT-PARTIAL] — calibration/UQ batch (see notes).

### Theme: SSL / foundation encoders (SAR-first; feeds CR-01 / P7)
- 2608.11142 [FT-PARTIAL] — Gupta; Sobti (2026, cs.CV) — SAR2Agri: first SSL on SAR-INTENSITY only;
  Time-Difference+Future-Frame temporal pretext + masking + curriculum; SICKLE 84.9% IoU, +15.3 pt vs
  optical, +2.2 pt vs SAR; maps SAR-FM field (TerraMind/CopernicusFM/SAR-JEPA/SARMAE/SAR-W-MixMAE).

### Theme: Residual + transfer forecasting
- 2607.26854 [FT-PARTIAL] — TREA-Net: gated RESIDUAL + two-scalar data-rich→scarce transfer + conformal
  −29.6% width; TiRex zero-shot strongest baseline (→ P14Z park).

### Theme: Safe-RL / shielding / deep-RL evaluation
- 2603.17319 [FT-PARTIAL] — PIER physics-informed offline RL (IQL) + decoupled shield; tail not mean.
- 2609.38655 [FT-PARTIAL] — Lyapunov-certified controller library; safety-by-construction.
- 2608.19836 [FT-PARTIAL] — adaptive probabilistic shield; graph known, probs learned online.
- 2610.03369 [FT-PARTIAL] — DRL failure attribution reverses 30↔100 seeds; MoE "fix" masks spec failure.
- 2602.14676 [FT-PARTIAL] — GREAT-EER graph-RL bus evacuation <1s; cites Blatten 2025 SAVE precedent.
- 2609.38552 [FT-PARTIAL] — safe-RL/eval batch (see note).

### Theme: Anomaly detection / OOD / TSAD
- 2610.06453 [FT-PARTIAL] — NCL: FMs reconstruct anomalies too well → error-score collapse.
- 2610.00363 [FT-PARTIAL] — DL-AD railway survey: 4-axis taxonomy × 4 paradigms + edge-cloud framework.
- 2608.06876 [FT-PARTIAL] — FedVAR federated video anomaly (raw video stays local).
- 2507.07841, 2609.39337, 2605.23504, 2609.31142, 2606.00690, 2610.06317, 2609.27202, 2203.13313,
  2012.13849, 2511.15838 [FT-PARTIAL] — anomaly/OOD/robustness/eval batch (see notes).

### Theme: Physics / PIML
- 2610.04828 [FT-PARTIAL] — label-free PINN slope FoS within 2–3% of FEM; use FoS as GATE not probability.
- 2605.06643, 2605.01679, 2604.16265 [FT-PARTIAL] — physics/forensics/robustness batch (see notes).

### Theme: Media forensics / crisis informatics
- 2610.03380 [FT-PARTIAL] — interpretable deepfake (photometric/textural/geometric/compression + LSTM).
- 2007.05848 [FT-PARTIAL] — crisis-informatics misinformation; low-trust corroboration (Rule 19).

### Theme: Alerting / IoT / edge
- 2604.24404 [FT-PARTIAL] — 5G public-warning broadcasts unauthenticated/spoofable → sign CAP + auth mesh.
- 2610.06241 [FT-PARTIAL] — backprop-free prototype-head on-device adaptation (5.2KB/22KB/11ms, PSoC6).
- 2511.20936 [FT-PARTIAL] — IoT/edge batch (see note).

### Non-quota leads (NOT counted; ABS/no-HTML)
- 2412.11942 (DRUM, residual diffusion) · 2108.06868 (Nowcasting-Nets, residual) · 2608.19672 (SAGE
  XGBoost EWS) · 2510.10546 (GLOFNet dataset; CC BY-NC-ND 4.0, Shisper/Karakoram) — all abstract-only.

### Parked for P14Z (compulsory zero-shot phase) / P7 (SAR-FM trade)
- P14Z: TiRex (via 2607.26854); OmniRSCLIP 2609.03391 (+ OmniRS5M corpus); RS scene-classification survey.
- P7: SAMBA 2606.31668, OceanSAR-1, SAR-JEPA, SARMAE, SAR-W-MixMAE, TerraMind, Copernicus-FM 2503.11849.
