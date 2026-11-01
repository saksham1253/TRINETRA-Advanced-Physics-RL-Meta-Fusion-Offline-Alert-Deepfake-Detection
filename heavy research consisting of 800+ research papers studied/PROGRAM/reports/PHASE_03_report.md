# PHASE P3 REPORT — Literature Foundation II

Date: 2026-10-07 · Phase: P3 (authorized "GO PHASE P3", 2026-10-06) · Status at exit: COMPLETE → AWAITING GATE

---

## 1. Objective (from §P3 / MASTER_PROMPT §0.11)
Build the SECOND HALF of the foundation NEW-paper set (P2+P3 together, trajectory toward ≥250 ≤400
verified NEW at ≥60% Tier-2+). SOTA scan FIRST; full §0.8 search; convert the reading queue + remaining
axes + re-studied baseline backlog into deep reads; close axis gaps A3/A4/A9/A13; rebalance themes away
from hazard-core (P2 exit directive) THEN — on explicit user mid-phase redirection — **pivot back to
hazard-core and use non-arXiv sources**; interim syntheses every ~5 batches; maintain all registers +
novelty index + contradiction register + citation graph; read ≥15 NEW quota papers ON TOP of baseline
(OQ-02), heavy phase ~30–40; ≥60% Tier-2+. RESEARCH-ONLY (§0.1A). No own-system claims (Rule 16).
STOP at the P3 gate — one phase only.

### Authorization-scope note (honest)
User directives that shaped P3, in order received:
1. "GO PHASE P3" — authorizes P3 only; STOP at gate.
2. "stop at 40 and go for hazard-core … use different websites as well" — cap ~40 NEW; pivot to
   hazard-core (landslide/flood/GLOF/InSAR/precip); use NON-arXiv sources (D-010).
3. "continue and if you want more papers … find more papers if needed if not needed then no problem"
   — discretion to EXCEED ~40 iff papers are genuinely outstanding/SOTA; no obligation to pad.
4. Compulsory future phase registered: a dedicated ZERO-SHOT CLASSIFICATION phase (**P14Z**), ≥10 papers,
   between P14 and P15 — REGISTERED in planning docs; EXECUTION DEFERRED (not authorized yet).

Outcome: **43 NEW deep reads** — past the ~40 soft cap under directive #3, stopped at an honest
convergence point (hazard-core arXiv veins exhausted; see §7), NOT padded (§0.5).

## 2. What was done (outputs on disk)
| Task | Output | Key result |
|------|--------|------------|
| 1. SOTA scan FIRST + living | PROGRAM/sota/P3_sota_scan.md (§1–§8) | safe-RL/eval, anomaly/OOD, physics/PIML, media-forensics, IoT, + §6 HAZARD-CORE SOTA, §7 axis-exhaustion ledger |
| 2. Full §0.8 search | analysis/02_search_log.md rows 158–219 (62 queries) | arXiv API quoted-AND + non-arXiv (NHESS/Cryosphere/MDPI); every hit novelty-checked |
| 3. Queue conversion | analysis/10_reading_queue.csv | P3 harvest scored; #38–#43 statuses + P14Z/P7 parks logged |
| 4. Batch-read 43 NEW quota | 43 notes in analysis/03_paper_notes/ + PROGRAM/logs/P3_reading_progress.md + PROGRAM/phase_papers/P3_papers.csv | **43/43 FT-PARTIAL = 100% Tier-2+** (target ≥15 and ~30–40 EXCEEDED; ≥60% Tier-2+ met) |
| 5. Interim syntheses | PROGRAM/reports/P3_interim_syntheses.md | #1, #2, #3 (reads 37–43) |
| 6. Registers + ledger | 02_paper_ledger.csv (+43 [P3] rows), novelty_index.csv, contradiction register, equations/claims | pre-existing rows untouched (§0.3); phase rows tagged [P3] |
| 7. Exit audits | analysis/11_reading_audit.md (Audit #9, ~21% sample) | **0% identity/claim error**; 1 body-number re-verify item flagged (non-blocking) |
| 8. Report + gate + handoff | this report, PHASE_03_gate.md, HANDOFF update, CHANGELOG, REFERENCES grouping | gate with progress-trajectory + P14Z registration |

## 3. The 43 NEW quota papers (verified NEW vs ledger + novelty index)
All read FT-PARTIAL via ar5iv/arXiv-HTML (web_fetch prunes page middle → body tables not fully
verified; labelled honestly per D-008). None were in the 235-paper ledger or local baseline.

| # | ID | One-line contribution to TRINETRA | Theme |
|---|----|-----------------------------------|-------|
| 1 | 2604.24404 | 5G public-warning broadcasts are unauthenticated/spoofable → sign CAP + authenticate mesh | alerting/security |
| 2 | 2603.17319 | PIER physics-informed offline RL (IQL) + decoupled shield; kills tail not mean; forecast-independent | RL/safe-RL |
| 3 | 2610.06453 | NCL: FMs reconstruct anomalies too well → error-score collapse; constrain to normal subspace | anomaly/TSAD |
| 4 | 2610.04828 | label-free PINN slope FoS within 2–3% of FEM; use FoS as GATE not probability (3% err → 2× tail-prob err) | physics/PIML |
| 5 | 2610.06241 | prototype-head on-device adaptation, NO backprop, 5.2KB/22KB/11ms on PSoC6 | IoT/TinyML |
| 6 | 2610.03380 | interpretable deepfake: photometric/textural/geometric/compression + LSTM; auditable (Rule 19) | media-forensics |
| 7 | 2609.38655 | safety-by-construction: Lyapunov-certified controller library → forward invariance | safe-RL |
| 8 | 2608.19836 | adaptive probabilistic shield: graph known, probs learned online; conservative→tighten | safe-RL |
| 9 | 2609.18555 | fire-spread DL uses front-distance geometry; only fuel-load strong; cross-region loss (CR-02 5th domain) | wildfire/interp |
| 10 | 2610.03369 | DRL failure attribution REVERSES 30↔100 seeds; MoE "fix" masks spec failure; all RL lose to TWAP | deep-RL eval |
| 11 | 2602.14676 | GREAT-EER graph-RL bus evacuation <1s; cites Blatten 2025 precautionary-evac SAVE precedent | RL/evacuation |
| 12 | 2608.16654 | IsoMaxPlus distance-logits: free OOD + ECE 0.0095→0.0026, no outliers/tuning | OOD/UQ |
| 13 | 2610.00363 | DL-AD railway survey: 4-axis taxonomy × 4 paradigms + edge-cloud deploy framework | anomaly survey |
| 14 | 2507.07841 | (anomaly/robustness batch) — see note | anomaly |
| 15 | 2608.06876 | FedVAR federated video anomaly; privacy-preserving (raw stays local) | WS4/privacy |
| 16 | 2609.39337 | (robustness/eval batch) — see note | robustness |
| 17 | 2605.23504 | (anomaly/UQ batch) — see note | anomaly/UQ |
| 18 | 2007.05848 | crisis-informatics misinformation; low-trust corroboration (Rule 19) | disaster/crowd |
| 19 | 2609.31142 | (eval/robustness batch) — see note | eval |
| 20 | 2609.15297 | (calibration/UQ batch) — see note | UQ/calibration |
| 21 | 2609.38552 | (safe-RL/eval batch) — see note | RL |
| 22 | 2606.00690 | (anomaly/physics batch) — see note | anomaly |
| 23 | 2610.06317 | (robustness/OOD batch) — see note | OOD |
| 24 | 2609.27202 | (anomaly/TSAD batch) — see note | TSAD |
| 25 | 2605.06643 | (physics/PIML batch) — see note | physics |
| 26 | 2605.01679 | (physics/forensics batch) — see note | physics/forensics |
| 27 | 2511.20936 | (IoT/edge batch) — see note | IoT/edge |
| 28 | 2203.13313 | (anomaly/seminal batch) — see note | anomaly |
| 29 | 2511.05471 | TUPANN satellite-only (GOES+IMERG) motion+intensity + differentiable WARP advection; cross-region transfer | precip nowcast |
| 30 | 2012.13849 | (anomaly/seminal batch) — see note | anomaly |
| 31 | 2604.16265 | (physics/robustness batch) — see note | physics |
| 32 | 2609.34836 | MW-Nowcast: deterministic structure + flow-matching RESIDUAL; beats PySTEPS for extremes; REV cost-loss | precip nowcast |
| 33 | 2511.15838 | (robustness/eval batch) — see note | robustness |
| 34 | 2606.04634 | (anomaly/UQ batch) — see note | anomaly/UQ |
| 35 | 2607.24683 | (eval/calibration batch) — see note | calibration |
| 36 | 2005.03221 | InSAR-DL ancestor (Anantrasirichai/Biggs): national S1 velocity CNN; sparse/noisy/scarce-label recipe | InSAR/landslide |
| 37 | 2605.17419 | RMCL: displacement-robust landslide EWS under rainfall-FORECAST uncertainty; +37% precision, Japan 19 | LEWS |
| 38 | 2512.24117 | GLOF: Himalayan glacial-lake S1-SAR segmentation IoU 0.9130; "temporal-first"; Dockerised ASF pipeline | GLOF/WS8 |
| 39 | 2607.26854 | TREA-Net: gated RESIDUAL + two-scalar data-rich→scarce transfer + conformal −29.6%; TiRex zero-shot best | residual/transfer |
| 40 | 2609.14821 | Decision-Oriented UQ: action-loss≠predictive coverage; regret −18.7%, utility +11.6%; sharpens CR-04 | decision-UQ |
| 41 | 2608.30205 | exPreCast-ENS: residual diffusion 4km→1km ensemble; recovers 38–47% missed heavy-rain px, ~95% retained | precip nowcast |
| 42 | 2608.11142 | SAR2Agri: first SSL on SAR-INTENSITY; SICKLE 84.9% IoU, +15.3pt vs optical; maps SAR-FM field for P7 | SAR-SSL |
| 43 | 2509.10362 | GNN-rP: GNN + r-Pareto EVT extreme-precip risk zoning; FIRST EVT paper; compound rain→flood+landslide | EVT/tail-risk |

(Rows marked "see note" have full FT-PARTIAL notes in analysis/03_paper_notes/ and one-line takeaways in
PROGRAM/logs/P3_reading_progress.md; this table foregrounds the hazard-core + doctrine-shaping reads.)

## 4. What changed in the design (the P3 payoff)
- **THREAD I — RESIDUAL doctrine is now the best-supported design principle (5× independent):**
  MW-Nowcast (2609.34836), DRUM (2412.11942 ABS), Nowcasting-Nets (2108.06868 ABS), TREA-Net (2607.26854),
  exPreCast-ENS (2608.30205) all converge: learn a BOUNDED RESIDUAL/refinement on a deterministic or
  mechanistic BACKBONE, don't forecast from scratch. → GMF bounded-residual head + SSL forecast-residual
  InSAR encoder, both now strongly externally supported. SAR2Agri (2608.11142) TD/FF temporal pretext is
  the SSL analogue.
- **THREAD K — the alarm stack is now complete on paper:** exPreCast-ENS gives the predictive DISTRIBUTION
  → 2609.14821 Decision-Oriented UQ calibrates to ACTION-LOSS (not predictive) coverage → our p*=0.0476
  cost-loss threshold selects the alarm. CR-04 sharpened: the gate must report BOTH predictive and
  action-loss coverage.
- **THREAD J — EVT/tail-risk opened (new axis):** GNN-rP (2509.10362) is the first extreme-value-theory
  paper in the corpus. Our hazards ARE tail events. Add peaks-over-threshold/r-Pareto tail modeling to the
  WHEN layer + people-at-risk, with JOINT exceedance for compound failure. GUARD: EVT tails are unstable
  with few exceedances in data-sparse mountains → wide-uncertainty PRIOR / zoning only, never a hard
  real-time threshold.
- **SAR-FIRST for the monsoon cloud problem (2 independent votes):** SAR2Agri (+15.3 pt over optical) and
  2512.24117 (GLOF IoU 0.9130 on S1-SAR). CR-01 encoder trade study (P7) now has named SAR-specific
  contenders: TerraMind, Copernicus-FM, SAR-JEPA, SARMAE, SAR-W-MixMAE, SAMBA (Mamba, edge-budget), OceanSAR.
- **Forecast-uncertainty-robust rain→landslide training:** RMCL (2605.17419) — we feed FORECAST rain
  (IMERG nowcast), not observed rain; train displacement/motion-robust representations.
- **RL alarm policy hardening:** PIER physics-informed offline RL + decoupled shield (2603.17319),
  Lyapunov-certified action library (2609.38655), adaptive probabilistic shield (2608.19836); evaluate
  with ≥100 seeds + tail/dispersion reporting + the two-baseline rule (2610.03369 eval critique → RB-13).
- **Interpretable WS2 + privacy WS4:** interpretable deepfake features (2610.03380) and federated video
  anomaly (2608.06876) keep the auditability + raw-data-local properties required by Rule 19.

## 5. Theme balance (43 papers)
P3 deliberately rebalanced toward robustness / eval-critique / safe-RL / anomaly / IoT in the first ~32
reads (per the P2 exit directive), THEN pivoted back to hazard-core (reads ~29–43) under the user's
mid-phase directive. Approximate distribution: safe-RL/eval ~20% · anomaly/OOD/UQ ~25% · hazard-core
(GLOF/landslide/InSAR/precip/EVT) ~28% · physics/PIML ~10% · media-forensics ~7% · IoT/edge ~7% ·
disaster/crowd ~3%. Hazard-core at ~28% reflects the authorized mid-phase pivot and spans 6 sub-topics;
flagged honestly.

## 6. SOTA + hazard-core findings
See PROGRAM/sota/P3_sota_scan.md. New in P3: §6 HAZARD-CORE SOTA (GLOF/landslide/precip/EVT/decision-UQ/
SAR-FM with as-published anchor numbers + caveats), §7 the ARXIV AXIS-EXHAUSTION LEDGER (honest coverage
signal), §8 non-arXiv journal route (D-010). Design implications are process targets only (Rule 16).

## 7. Why 43 is an honest stopping point (not padding, §0.5)
Hazard-core arXiv veins are mined/thin (from the search log + §7 ledger):
GLOF = 8 total hits (mostly unrelated math); landslide-displacement-forecasting = 1 (already read);
InSAR+DL+landslide = 1; GNN+landslide = 5; RL+evacuation = 5; cloudburst+Himalaya = 0.
Rich veins that WERE mined: flood+foundation-model = 47 (2609.14821 flagship), precip-nowcasting+diffusion
= 31 (NowcastDiT/PixelFlowCast parked), SAR+FM+SSL = 17 (SAMBA/OceanSAR parked→P7), flash-flood+ML = 19.
The remaining hazard-core SOTA lives in journals (NHESS, The Cryosphere, Remote Sensing, Frontiers),
reachable via the D-010 multi-source policy in later phases. zero-shot+RS = 50 hits are PARKED for the
compulsory P14Z phase (not read in P3 — not authorized).

## 8. Acceptance check (against §P3)
- ≥15 NEW quota papers (heavy phase ~30–40): **43 ✅ (exceeded; past ~40 under user directive #3).**
- ≥60% Tier-2+: **100% (43/43 FT-PARTIAL = Tier-2) ✅.**
- Audit error <5%: **0% at a ~21% sample (Audit #9) ✅** (1 body-number re-verify flagged, non-blocking).
- Theme distribution documented: **✅** (rebalance-then-authorized-pivot explained).
- SOTA scan first + living (§1–§8): **✅.** Search log complete (rows 158–219): **✅.** Interim
  syntheses (#1,#2,#3): **✅.** Registers/novelty index/contradiction register/queue maintained: **✅.**
- Non-arXiv sources used per directive (D-010): **✅** (policy applied; NHESS/Cryosphere/MDPI routes logged).
- RESEARCH-ONLY honored (no code/training/experiments/downloads); no own-system claims (Rule 16): **✅.**
- Non-destruction (§0.3): pre-existing rows/files untouched; phase rows appended + tagged [P3]: **✅.**

## 9. Progress toward the 250–400 foundation target (honest, D-009/D-010)
- Verified NEW deep (Tier-2 FT-PARTIAL) reads: **P1 15 + P2 18 + P3 43 = 76.**
- Non-quota baseline re-studies to Tier-2+ (OQ-02): 2606.16795 (WaveDINO), 2608.12422 ("Which Site/When")
  + the broader 235-paper abstract-verified backlog available for promotion.
- ABS/no-HTML non-quota leads logged, NOT counted: 2412.11942, 2108.06868, 2608.19672, 2510.10546, +4 parks.
- Honest statement: the ≥250 figure is a CUMULATIVE P2+P3+later target combining deep NEW reads + the
  re-studied baseline-235 + continuing promotions; it is reported as a TRAJECTORY, never padded. The 76
  deep NEW reads are the quota core; the volume toward 250 accrues as the baseline-235 promotions and the
  harvest pool convert in P4+ and later literature-touching phases.

## 10. Carried forward (PHASE_BACKLOG + harvest pool)
1. **P14Z (COMPULSORY, registered):** dedicated zero-shot/open-vocab classification phase, ≥10 papers,
   between P14 and P15. Parked: TiRex (zero-shot TS FM), OmniRSCLIP 2609.03391 (+OmniRS5M), RS-scene survey.
2. **P7 CR-01 SAR-FM trade study:** TerraMind/Copernicus-FM/SAR-JEPA/SARMAE/SAR-W-MixMAE/SAMBA/OceanSAR.
3. **Harvest pool (arXiv-confirmed, unread):** 2606.00270, 2610.08192, 2609.39413, 2608.26304, 2610.02413,
   2610.05726, 2609.17763, 2609.16314, 2610.01005, 2606.27704, 2209.07620, NowcastDiT 2609.37038,
   PixelFlowCast, GTS_Forecaster 2509.10560, GNS granular-flow, WS2 watermark (2610.06339/FlowMark/2610.05215).
4. **Non-arXiv journal route (D-010):** NHESS/The Cryosphere/Remote Sensing/Frontiers for GLOF/landslide SOTA.
5. **Body-number re-verify (non-blocking):** 2609.14821 extreme-precip regret −23.4% + 5 body figures vs full PDF in P14/P14Z.
6. **Author backfills (non-blocking):** reconcile "(per note)" author rows into the ledger in P4.
7. **Still open from earlier phases:** CP under drift/missingness (2406.05405, CR-04); 2606.12066 PDF route;
   I–D/GLOF constants (Bug #15); BOM ₹ verification (P6); Indian-LoRa 2412.04563.

## 11. Honesty notes
- All 43 reads are FT-PARTIAL (D-008): named sections read; page middles (often result tables) pruned by
  web_fetch → body-table numbers NOT independently re-verified beyond Audit #9's abstract-level checks.
  Every cited number is as-published with its protocol. The one body-only figure used prominently
  (2609.14821 −23.4%) is explicitly flagged body-pending in Audit #9.
- Novelty claims are "not found in the N sources searched" with queries + dates in the search log, never
  "does not exist" (Rule 21).
- No TRINETRA performance number is claimed anywhere (Rule 16). Published anchors are bars on THEIR data,
  not our expected results. The defensible target remains a PROCESS target: beat two baselines on our
  Himalayan data under spatial CV, with calibrated uncertainty + a cost-loss score.
- Life-safety (Rule 19): zero-shot/crowd/social/deepfake signals are LOW-TRUST advisory inputs into
  GMF + conformal + monotone shield, NEVER autonomous alarm triggers; the system complements, never
  replaces, certified official warning systems (CWC/IMD/SACHET), under human oversight.

---
### STATUS: P3 COMPLETE. STOPPING at the gate. Awaiting explicit **GO PHASE P4**.
