# 19 — REFERENCES (FULL) — TRINETRA / HIMKAVACH master citation list
> **This is the index.** The per-entry catalogue is split across four theme files (this chapter would exceed ~1800 lines in one file):
> - [`19a_REFERENCES_physics_pinn.md`](19a_REFERENCES_physics_pinn.md) — physics/combustion + PINN
> - [`19b_REFERENCES_fusion_uncertainty_eval.md`](19b_REFERENCES_fusion_uncertainty_eval.md) — fusion/uncertainty/calibration + evaluation/leakage/baselines
> - [`19c_REFERENCES_perception_deepfake_cctv.md`](19c_REFERENCES_perception_deepfake_cctv.md) — deepfake/media-forensics + CCTV fire-smoke + datasets/EO/remote-sensing
> - [`19d_REFERENCES_alerting_iot_rl_robustness.md`](19d_REFERENCES_alerting_iot_rl_robustness.md) — alerting/networks/DTN/LoRa/IoT + RL/OPE/safe-RL + robustness/safety/drift

## 0. Counts and the residual-identifier-risk disclosure (READ FIRST)
**Canonical counts (from `_CANON.md` §7, as recorded by the research program):**
- **631** unique arXiv IDs in the ledger (681 ID-bearing rows; ~7.3% legitimate cross-phase re-citations).
- **~436** new papers verified across phases P1–P20 (250-minimum met).
- **128** per-paper notes in `analysis/03_paper_notes/`.

**What THIS pass actually found in the live artifacts (2026-10-10), traceable to the files:**
- `analysis/02_paper_ledger.csv` currently parses to **845 physical lines**; after dropping comment/section banner lines → **841 data rows → 775 unique identifiers** catalogued here.
- **59** identifiers are re-cited (appear in >1 ledger row); each entry shows `re-cited Nx`.
- `analysis/03_paper_notes/` holds **128 note files → 127 unique IDs** (two files, `2608.12422.md` and `2608.12422_which_site_when.md`, both describe 2608.12422). Of these, **72** are rows in the ledger and **55** are local-note / baseline-corpus papers that are **NOT** ledger rows (listed in §5).

> ⚠️ **Discrepancy with `_CANON.md` §7 (disclosed, not hidden):** the canon states 631 unique arXiv IDs / 681 ID-bearing rows; the live ledger file catalogued here yields **775 unique IDs across 841 data rows**. The gap is consistent with the ledger having grown through later phases (P20–P23 rows are present) *after* the FINAL_REPORT.md §5 snapshot the canon quotes, and with the ledger counting non-arXiv identifiers (DOIs, dataset IDs). This chapter reports BOTH numbers and does not silently overwrite the canon. The 631/436/128 headline remains the canon's figure of record; 775/841/127 is this pass's direct file count.

> ⚠️ **Residual-identifier risk (per `_CANON.md` §7):** identifiers were *subagent-reported during a `web_search` outage and were NOT independently re-fetched* in this pass. Every catalogue entry therefore ends with `Verification status: resolved on 2026-10-10? — not re-fetched this pass`. No identifier below is claimed as independently resolved. Abstract-only reads (`ABS`) may never be stated as established fact — only as 'the abstract claims ...'.

> ✅ **Known citation correction (carried from `_CANON.md` §6):** the spatial-cross-validation verdict is grounded in **arXiv 2608.12422** (Which Site, and When: A Free-Satellite-Data Test…), *not* 2608.22293. Note that 2608.22293 **does exist** in the live ledger — but as a *different* paper ("Spatial Anatomy of Urban Wildfire Vulnerability (Geo…", REF-ALERT-068); it must not be cited for the spatial-CV result. (This slightly contradicts the canon's parenthetical that 2608.22293 is "NOT in the source artifacts"; it is present, just off-topic — see §6.)

## 1. Read-depth distribution (verbatim ledger tags)
| read_depth | meaning | unique IDs |
|---|---|---|
| ABS | abstract-only (may NOT be stated as fact) | 695 |
| FT-PARTIAL | full text, page-middles pruned by web_fetch (D-008) | 71 |
| FT | full text | 9 |

_Local notes exist for 72 of these ledger IDs (treated as the deepest reads); 55 further notes cover baseline-corpus papers not in the ledger (§5)._

## 2. Theme groups and where each lives
| Theme | REF prefix | entries | file |
|---|---|---|---|
| Physics / combustion / geo-hazard physics | `REF-PHY-*` | 155 | 19a |
| Physics-informed ML (PINN / neural operators) | `REF-PINN-*` | 19 | 19a |
| Fusion / uncertainty / calibration / conformal | `REF-FUS-*` | 70 | 19b |
| Evaluation / leakage / cost-loss / decision / baselines | `REF-EVAL-*` | 58 | 19b |
| Deepfake / media-forensics / crisis informatics | `REF-DF-*` | 19 | 19c |
| CCTV / UAV / satellite fire-smoke perception | `REF-CCTV-*` | 71 | 19c |
| Datasets / EO / remote-sensing / InSAR / encoders | `REF-DATA-*` | 84 | 19c |
| Alerting / networks / DTN / LoRa / IoT / deployment | `REF-ALERT-*` | 86 | 19d |
| Offline-RL / OPE / safe-RL / shielding | `REF-RL-*` | 71 | 19d |
| Robustness / anomaly / drift / OOD / safety | `REF-ROB-*` | 142 | 19d |
| **TOTAL** |  | **775** |  |

_Grouping rule (documented for traceability): each paper is placed by its **ledger axis/WS code** via a fixed axis→theme map, except that any paper whose title/relevance names a PINN / neural-operator method is pulled into the PINN theme. Because the grouping follows the ledger's own axis labels, a few papers land in a theme that differs from topical intuition (e.g. 2101.05397 "Should Ensemble Members Be Calibrated?" carries ledger axis WS1b → physics file; 2604.24404 the 5G-warning spoofing paper carries axis A6 → RL file). The real axis is printed on every entry so nothing is lost._

## 3. MUST-READ TOP 30 (in reading order)
Reading order runs foundational-method → applied-system. `(REF-id, file, read_depth)` are shown; **classics have no arXiv/DOI in the ledger** and are sourced to `analysis/08_equations_register.md`.

1. **2608.12422** (REF-PHY-010, 19a, ABS) -- Which Site, and When: A Free-Satellite-Data Test of Himalayan Glacial Lake Bursts, Landslides, and Ice Floods
   - Why: Spatial-CV leakage verdict (CANON-grounded). Naive terrain ROC-AUC ~0.90 collapses to 0.76/0.71/0.54 under matched spatial-block CV; a simple GB/3-rule tree matches deep nets. CORRECTION: this is the correct id -- NOT 2608.22293.
2. **2610.08227** (REF-EVAL-027, 19b, FT-PARTIAL) -- How Many Independent Samples Does a Satellite Image Contain?
   - Why: Effective-sample-size theorem: a satellite tile holds far fewer independent samples than pixels -> why random CV over-states skill. Read right after 2608.12422.
3. **2101.05397** (REF-PHY-099, 19a, ABS) -- Should Ensemble Members Be Calibrated?
   - Why: "Should Ensemble Members Be Calibrated?" -- the calibrated-members argument that underpins the fusion/calibration stack (ledger axis WS1b, topically calibration).
4. **2303.12783** (REF-FUS-020, 19b, ABS) -- Conformal Prediction for Time Series with Modern Hopfield Networks (HopCPT)
   - Why: HopCPT: conformal prediction for time series via modern Hopfield nets -- the time-series conformal method behind the alarm interval guarantee.
5. **2106.08909** (REF-RL-002, 19d, ABS) -- Offline RL Without Off-Policy Evaluation (One-Step)
   - Why: One-step offline RL beats iterative actor-critic on much of D4RL and avoids high-variance repeated OPE -- the first RL baseline to benchmark.
6. **2110.14000** (REF-RL-005, 19d, ABS) -- Towards Hyperparameter-free Policy Selection for Offline Reinforcement Learning
   - Why: BVFT: hyperparameter-free offline policy SELECTION -- how to pick the alarm policy without live trials.
7. **2311.18206** (REF-RL-006, 19d, ABS) -- SCOPE-RL: A Python Library for Offline Reinforcement Learning and Off-Policy Evaluation
   - Why: SCOPE-RL: the OPE/offline-RL evaluation library that frames the honest OPE gate (ties BVFT).
8. **2604.24404** (REF-RL-022, 19d, FT-PARTIAL) -- Open-Source 5G Public Warning System Spoofing Testbed
   - Why: 5G public-warning broadcasts are unauthenticated/spoofable (open-source testbed) -> must sign CAP + authenticated mesh. (Ledger axis A6, but this is an alerting/security paper.)
9. **2003.01279** (REF-ROB-130, 19d, ABS) -- Disrupting Deepfakes: Adversarial Attacks Against Facial Manipulation Systems
   - Why: Disrupting Deepfakes: adversarial attacks on facial manipulation -- defensive-only framing for WS2 (ledger axis WS6/robustness).
10. **2007.05848** (REF-EVAL-025, 19b, FT-PARTIAL) -- Fighting Disaster Misinformation in Latin America (#Verificado19S Mexico 2017 Earthquake)
   - Why: Crisis-informatics misinformation: social/deepfake signals are low-trust and must be corroborated (Rule 19).
11. **2603.17319** (REF-FUS-031, 19b, FT-PARTIAL) -- PIER: Physics-Informed Offline RL with Decoupled Post-hoc Shield
   - Why: PIER physics-informed offline RL (IQL) + decoupled shield; optimise the TAIL not the mean -- template for the safe-RL shield.
12. **2610.04828** (REF-PINN-006, 19a, FT-PARTIAL) -- Label-Free PINN Strength-Reduction Factor-of-Safety at Scale
   - Why: Label-free PINN slope FoS within 2-3% of FEM -> use FoS as a GATE not a probability (PINN feasibility evidence).
13. **2512.23964** (REF-PHY-007, 19a, ABS) -- DUALFloodGNN: Physics-informed Graph Neural Network for Operational Flood Modeling
   - Why: DUALFloodGNN: fast physics-informed GNN flood hydrodynamics -- SOTA, open-source surrogate for the flood/runout gate.
14. **2505.08553** (REF-PHY-006, 19a, ABS) -- Towards Digital Twin in Flood Forecasting with Data Assimilation of Satellite EO (Alzette)
   - Why: Particle-filter data-assimilation of Sentinel-1 into LISFLOOD-FP (digital-twin flood) -- closest published analogue to satellite-into-physics fusion + honest residual-uncertainty reporting.
15. **2211.10338** (REF-DATA-006, 19c, ABS) -- Deep learning based landslide density estimation on SAR data for rapid response
   - Why: SAR-only landslide density (0.814 AUC) with the honest sub-pixel limit (~45% of slides < 10 m S1 pixel) -- a must-cite baseline + resolution caveat.
16. **2512.12844** (REF-FUS-006, 19b, ABS) -- Selective Conformal Risk Control (SCRC)
   - Why: Selective Conformal Risk Control: abstain on low-confidence inputs, calibrate on the selected subset -- the principled fix for the conformal over-claim.
17. **2512.01384** (REF-FUS-007, 19b, ABS) -- CLAPS: Aleatoric-Epistemic Scaling via Last-Layer Laplace for Conformal Regression
   - Why: CLAPS: conformal intervals widen where training support is thin (aleatoric+epistemic) -- honest widening in the data-sparse Himalayan tail.
18. **2603.10392** (REF-FUS-005, 19b, ABS) -- Safe Probabilistic Planning for Human-Robot Interaction using Conformal Risk Control
   - Why: CBF + conformal risk control = formal, context-adaptive safety margins -- upgrades the ad-hoc hard-threshold shield.
19. **2104.11422** (REF-EVAL-001, 19b, ABS) -- Socio-meteorology: flood prediction social preparedness and cry wolf effects
   - Why: Socio-meteorology cry-wolf: false alarms erode trust/compliance, worse in low-frequency-disaster regions -- the social half of the threshold design.
20. **2509.11789** (REF-EVAL-005, 19b, ABS) -- Watch Your Step: Cost-Sensitive Accelerometer Fall Detection in Real-World Streaming
   - Why: Cost-sensitive streaming fall-detection: tune the DECISION THRESHOLD by asymmetric miss>>FA cost; Recall 1.0 need not kill precision -- validates the p*=0.0476 methodology.
21. **2503.14621** (REF-EVAL-008, 19b, ABS) -- Reducing False Ventricular Tachycardia Alarms in ICU Settings: A Machine Learning Approach
   - Why: Learned true/false-alarm discriminator (ROC-AUC>0.96) that suppresses FAs without missing events -- supports a two-stage alarm-verification layer.
22. **2601.05921** (note-only -- NOT a ledger row; grounds equations-register E-07, FT (local note)) -- Decision-value / cost-loss Value Score for EWS verification (QUOTA#15)
   - Why: Cost-loss Value Score: evaluate EWS across a RANGE of C/L ratios, not a single AUC -- the primary evaluation metric (equations register E-07).
23. **2603.15945** (REF-ALERT-008, 19d, ABS) -- Evaluating Opportunistic Routing Protocols in a Disaster Scenario (DTN Earthquake Case Study)
   - Why: DTN opportunistic routing in a real disaster: Spray-and-Wait beats Epidemic -- which store-carry-forward protocol for backhaul-down alerting.
24. **2608.11142** (REF-DATA-037, 19c, FT-PARTIAL) -- SAR2Agri: Learning SAR Intensity Representations for Agricultural Monitoring
   - Why: SAR2Agri: SSL on SAR-intensity only (+15.3 pt IoU vs optical) -- the SAR-first self-supervised encoder recipe for data-poor regions.
25. **2509.17942** (REF-DATA-005, 19c, ABS) -- StefaLand: An Efficient Geoscience Foundation Model Improving Dynamic Land-Surface Predictions
   - Why: StefaLand geoscience foundation model: strong SPATIAL generalization on landslide/soil-moisture, academic-compute trainable -- the most on-point external FM/backbone candidate.
26. **2306.00001** (REF-CCTV-001, 19c, ABS) -- TinyissimoYOLO: Quantized Low-Memory TinyML Object Detection for Low-Power Microcontrollers
   - Why: TinyissimoYOLO: real-time INT8 detection at 196 uJ/inference on an MCU -- hard evidence of what a <=Rs.2000 edge node can actually run (vs GPU benchmarks).
27. **2610.06453** (REF-CCTV-021, 19c, FT-PARTIAL) -- NCL: Normal-Subspace Constrained Learning for Foundation-Model Anomaly Detection
   - Why: NCL: foundation models reconstruct anomalies too well -> reconstruction-error anomaly scores collapse -- a warning for the anomaly/drift layer.

**Classic physics primary references (load-bearing but NOT ledger rows — no arXiv/DOI; cited in `_CANON.md` §4 and `analysis/08_equations_register.md`; author/year strings copied from the register, not independently re-fetched):**

28. **Iverson (2000), Water Resources Research** (classic; no arXiv/DOI in ledger) — Transient pressure-head infiltration; slope enters ONLY via D1=D0/cos^2(delta) (the Bug #3 guard). Equations register GH-02/E-02.
29. **Fukuzono (1985) / Voight (1988)** (classic; no arXiv/DOI in ledger) — Inverse-velocity failure-time: 1/v = A(alpha-1)(t_f - t), alpha~2 -> 1/v linear. Equations register E-04/GH (time-to-failure).
30. **Heskestad (1983)** (classic; no arXiv/DOI in ledger) — Mean flame height L = 0.235 Q^(2/5) - 1.02 D and plume centerline -- fire-physics anchor. Equations register EF-01/EF-03.

## 3b. Load-bearing references — fully verified (2026-10-10)
Every entry below was **independently re-fetched** this pass from `https://arxiv.org/abs/<ID>` (web_fetch, HTTP 200). Authors, titles, years and the arXiv **primary category** are copied from the live abstract page — not from memory, not subagent-reported. The one-line problem+method is paraphrased by the doc author. Each BibTeX block is built from the fetched metadata. **33/33 IDs resolved; 0 fetch failures; no ID failed to resolve** (all "2026" identifiers resolve — arXiv in this environment carries 2026 papers). Where the fetched title differs from the TOP-30 shorthand, the *fetched* title is authoritative and is flagged `[title corrected]`.

> The 8 classic no-arXiv primaries (**Heskestad 1983; Byram 1959; Iverson 2000; Caine 1980; Fukuzono 1985 / Voight 1988; Raissi, Perdikaris & Karniadakis 2019 PINN; Ruff et al. 2018 Deep-SVDD; Kumar et al. 2020 CQL-journal/BEAR line**) are **NOT** assigned an arXiv ID here. They remain cited by author/year/venue in §3 (items 28–30) and `analysis/08_equations_register.md`; no identifier was invented for them. (Note: the CQL method itself has a preprint, 2006.04779, verified below; the "no-arXiv" caution concerns inventing IDs for classic/journal-only works.)

### Spatial-CV / leakage core

#### 2608.12422 — REF-PHY-010 (19a) [title corrected]
- Title: Which Site, and When: A Free-Satellite-Data Test of Himalayan Glacial Lake Bursts, Landslides, and Ice Floods
- Authors (full): Matthew Kahn; Milan Arjel; Nirmala Adhikari; Mingmar Sherpa; James Pope
- Year / Venue: 2026 (submitted 12 Aug 2026) / arXiv
- arXiv primary category: cs.LG (cross-list: stat.AP) · DOI: 10.48550/arXiv.2608.12422
- Problem+method: Tests whether free SAR-interferometry + satellite-weather signals predict *which* Himalayan site is susceptible and *when* a trigger arrives for GLOFs/landslides/ice-floods; under strict spatial-block CV, naïve terrain AUC ~0.9 collapses to 0.76/0.71/0.54 and a 3-rule gradient-boosted baseline matches deep nets.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{kahn2026whichsite,
  title        = {Which Site, and When: A Free-Satellite-Data Test of Himalayan Glacial Lake Bursts, Landslides, and Ice Floods},
  author       = {Kahn, Matthew and Arjel, Milan and Adhikari, Nirmala and Sherpa, Mingmar and Pope, James},
  year         = {2026},
  eprint       = {2608.12422},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2608.12422}
}
```

#### 2610.08227 — REF-EVAL-027 (19b) [title corrected]
- Title: How Many Independent Samples Does a Satellite Image Contain? Generalization Bounds for Spatially Dependent Data
- Authors (full): Robin Young
- Year / Venue: 2026 (submitted 6 Oct 2026) / IEEE Transactions on Geoscience and Remote Sensing (2026) vol. 64
- arXiv primary category: stat.ML (cross-list: cs.CV, cs.LG) · DOI: 10.48550/arXiv.2610.08227 · Related DOI: 10.1109/TGRS.2026.3739158
- Problem+method: Proves the effective sample size of an n×n spatially correlated image is Θ(n²/r²), not n²; a matching lower bound makes the rate tight, justifying spatial-block holdout with separation ∝ correlation range and showing random holdout underestimates CI widths by a factor ∝ r.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@article{young2026howmany,
  title        = {How Many Independent Samples Does a Satellite Image Contain? Generalization Bounds for Spatially Dependent Data},
  author       = {Young, Robin},
  journal      = {IEEE Transactions on Geoscience and Remote Sensing},
  volume       = {64},
  year         = {2026},
  eprint       = {2610.08227},
  archivePrefix= {arXiv},
  primaryClass = {stat.ML},
  doi          = {10.1109/TGRS.2026.3739158}
}
```

#### 2608.22293 — REF-ALERT-068 (19d) [title corrected]
- Title: The spatial anatomy of urban wildfire vulnerability: a spatially validated GeoAI framework reveals the roles of building density and vegetation moisture in structure loss during the 2025 Palisades Fire
- Authors (full): Parastoo Farajpoor; Mohammadreza Narimani
- Year / Venue: 2026 (submitted 23 Aug 2026) / arXiv
- arXiv primary category: physics.geo-ph (cross-list: cs.LG, eess.IV) · DOI: 10.48550/arXiv.2608.22293
- Problem+method: Spatially-validated GeoAI on 12,081 CAL FIRE inspections from the 2025 Palisades Fire; random-CV ROC-AUC 0.92 drops to 0.75 under 1 km spatial-block validation, logistic regression is better calibrated — a second-domain confirmation of the spatial-CV verdict (complements 2608.12422; do NOT substitute for it on the GLOF result).
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{farajpoor2026spatialanatomy,
  title        = {The spatial anatomy of urban wildfire vulnerability: a spatially validated GeoAI framework reveals the roles of building density and vegetation moisture in structure loss during the 2025 Palisades Fire},
  author       = {Farajpoor, Parastoo and Narimani, Mohammadreza},
  year         = {2026},
  eprint       = {2608.22293},
  archivePrefix= {arXiv},
  primaryClass = {physics.geo-ph},
  doi          = {10.48550/arXiv.2608.22293}
}
```

### Fusion / uncertainty / conformal

#### 2101.05397 — REF-PHY-099 (19a)
- Title: Should Ensemble Members Be Calibrated?
- Authors (full): Xixin Wu; Mark Gales
- Year / Venue: 2021 (submitted 13 Jan 2021) / arXiv
- arXiv primary category: cs.LG (cross-list: stat.ML) · DOI: 10.48550/arXiv.2101.05397
- Problem+method: Shows theoretically and on CIFAR-100 that calibrated ensemble *members* do not guarantee a calibrated *ensemble*, and a calibrated ensemble prediction cannot exceed the average performance of its calibrated members — the calibration argument underpinning the fusion stack.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{wu2021shouldensemble,
  title        = {Should Ensemble Members Be Calibrated?},
  author       = {Wu, Xixin and Gales, Mark},
  year         = {2021},
  eprint       = {2101.05397},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2101.05397}
}
```

#### 2303.12783 — REF-FUS-020 (19b)
- Title: Conformal Prediction for Time Series with Modern Hopfield Networks
- Authors (full): Andreas Auer; Martin Gauch; Daniel Klotz; Sepp Hochreiter
- Year / Venue: 2023 (submitted 22 Mar 2023, v2 2 Nov 2023) / NeurIPS 2023
- arXiv primary category: cs.LG (cross-list: cs.AI, stat.ML) · DOI: 10.48550/arXiv.2303.12783
- Problem+method: HopCPT — a conformal-prediction method for time series that exploits (rather than is broken by) temporal autocorrelation via modern Hopfield networks; outperforms SOTA conformal methods on real-world series from four domains — the time-series conformal method behind the alarm interval.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@inproceedings{auer2023hopcpt,
  title        = {Conformal Prediction for Time Series with Modern Hopfield Networks},
  author       = {Auer, Andreas and Gauch, Martin and Klotz, Daniel and Hochreiter, Sepp},
  booktitle    = {Advances in Neural Information Processing Systems (NeurIPS)},
  year         = {2023},
  eprint       = {2303.12783},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2303.12783}
}
```

#### 2512.12844 — REF-FUS-006 (19b)
- Title: Selective Conformal Risk Control
- Authors (full): Yunpeng Xu; Wenge Guo; Zhi Wei
- Year / Venue: 2025 (submitted 14 Dec 2025, v2 27 Apr 2026) / arXiv
- arXiv primary category: cs.LG (cross-list: stat.ML) · DOI: 10.48550/arXiv.2512.12844
- Problem+method: SCRC — a two-stage framework that first selects confident samples, then applies conformal risk control on the selected subset (SCRC-T exact finite-sample; SCRC-I PAC-style), producing compact calibrated sets — the principled abstain-and-calibrate fix for conformal over-claiming.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{xu2025scrc,
  title        = {Selective Conformal Risk Control},
  author       = {Xu, Yunpeng and Guo, Wenge and Wei, Zhi},
  year         = {2025},
  eprint       = {2512.12844},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2512.12844}
}
```

#### 2512.01384 — REF-FUS-007 (19b)
- Title: CLAPS: Aleatoric-Epistemic Scaling via Last-Layer Laplace for Conformal Regression
- Authors (full): Dongseok Kim; Hyoungsun Choi; Mohamed Jismy Aashik Rasool; Gisung Oh
- Year / Venue: 2025 (submitted 1 Dec 2025, v4 5 May 2026) / arXiv
- arXiv primary category: cs.LG (cross-list: stat.ML) · DOI: 10.48550/arXiv.2512.01384
- Problem+method: CLAPS — split-conformal regression that uses heteroscedastic last-layer Laplace uncertainty as the local normalisation scale, combining learned aleatoric noise with epistemic uncertainty so intervals widen where training support is thin (reduces to pure aleatoric scaling as epistemic uncertainty vanishes).
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{kim2025claps,
  title        = {CLAPS: Aleatoric-Epistemic Scaling via Last-Layer Laplace for Conformal Regression},
  author       = {Kim, Dongseok and Choi, Hyoungsun and Rasool, Mohamed Jismy Aashik and Oh, Gisung},
  year         = {2025},
  eprint       = {2512.01384},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2512.01384}
}
```

#### 2603.10392 — REF-FUS-005 (19b)
- Title: Safe Probabilistic Planning for Human-Robot Interaction using Conformal Risk Control
- Authors (full): Jake Gonzales; Kazuki Mizuta; Karen Leung; Lillian J. Ratliff
- Year / Venue: 2026 (submitted 11 Mar 2026) / arXiv
- arXiv primary category: cs.RO (cross-list: cs.AI) · DOI: 10.48550/arXiv.2603.10392
- Problem+method: Combines control barrier functions with conformal risk control to bound CBF-value prediction error and give formal probabilistic constraint-satisfaction guarantees, dynamically adjusting safety margins by interaction context — upgrades the ad-hoc hard-threshold shield.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{gonzales2026safeplanning,
  title        = {Safe Probabilistic Planning for Human-Robot Interaction using Conformal Risk Control},
  author       = {Gonzales, Jake and Mizuta, Kazuki and Leung, Karen and Ratliff, Lillian J.},
  year         = {2026},
  eprint       = {2603.10392},
  archivePrefix= {arXiv},
  primaryClass = {cs.RO},
  doi          = {10.48550/arXiv.2603.10392}
}
```

### Offline-RL / OPE / safe-RL (methods + baselines)

#### 1707.06347 — PPO (local note; §5 baseline corpus)
- Title: Proximal Policy Optimization Algorithms
- Authors (full): John Schulman; Filip Wolski; Prafulla Dhariwal; Alec Radford; Oleg Klimov
- Year / Venue: 2017 (submitted 20 Jul 2017, v2 28 Aug 2017) / arXiv
- arXiv primary category: cs.LG · DOI: 10.48550/arXiv.1707.06347
- Problem+method: PPO — a clipped-surrogate policy-gradient family allowing multiple minibatch epochs per rollout; TRPO-like stability with far simpler implementation and better sample complexity on locomotion/Atari.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{schulman2017ppo,
  title        = {Proximal Policy Optimization Algorithms},
  author       = {Schulman, John and Wolski, Filip and Dhariwal, Prafulla and Radford, Alec and Klimov, Oleg},
  year         = {2017},
  eprint       = {1707.06347},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.1707.06347}
}
```

#### 2006.04779 — CQL (local note; §5 baseline corpus)
- Title: Conservative Q-Learning for Offline Reinforcement Learning
- Authors (full): Aviral Kumar; Aurick Zhou; George Tucker; Sergey Levine
- Year / Venue: 2020 (submitted 8 Jun 2020, v3 19 Aug 2020) / arXiv (NeurIPS 2020)
- arXiv primary category: cs.LG (cross-list: stat.ML) · DOI: 10.48550/arXiv.2006.04779
- Problem+method: CQL learns a Q-function whose policy value lower-bounds the true value by adding a Q-value regulariser to the Bellman objective, countering offline over-estimation under distributional shift; 2–5× higher return on multi-modal data.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{kumar2020cql,
  title        = {Conservative Q-Learning for Offline Reinforcement Learning},
  author       = {Kumar, Aviral and Zhou, Aurick and Tucker, George and Levine, Sergey},
  year         = {2020},
  eprint       = {2006.04779},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2006.04779}
}
```

#### 2110.06169 — IQL (local note; §5 baseline corpus)
- Title: Offline Reinforcement Learning with Implicit Q-Learning
- Authors (full): Ilya Kostrikov; Ashvin Nair; Sergey Levine
- Year / Venue: 2021 (submitted 12 Oct 2021) / arXiv (ICLR 2022)
- arXiv primary category: cs.LG · DOI: 10.48550/arXiv.2110.06169
- Problem+method: IQL never queries out-of-dataset actions: it approximates policy improvement implicitly via an upper-expectile state-value function, then extracts the policy by advantage-weighted behavioural cloning; SOTA on D4RL with strong online fine-tuning.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{kostrikov2021iql,
  title        = {Offline Reinforcement Learning with Implicit Q-Learning},
  author       = {Kostrikov, Ilya and Nair, Ashvin and Levine, Sergey},
  year         = {2021},
  eprint       = {2110.06169},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2110.06169}
}
```

#### 2106.08909 — REF-RL-002 (19d)
- Title: Offline RL Without Off-Policy Evaluation
- Authors (full): David Brandfonbrener; William F. Whitney; Rajesh Ranganath; Joan Bruna
- Year / Venue: 2021 (submitted 16 Jun 2021, v3 3 Dec 2021) / NeurIPS 2021
- arXiv primary category: cs.LG (cross-list: stat.ML) · DOI: 10.48550/arXiv.2106.08909
- Problem+method: Shows a single step of constrained/regularised policy improvement on an on-policy Q-estimate of the behavior policy beats iterative actor-critic on much of D4RL, attributing iterative methods' weakness to high-variance repeated OPE — the first RL baseline to benchmark.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@inproceedings{brandfonbrener2021onestep,
  title        = {Offline RL Without Off-Policy Evaluation},
  author       = {Brandfonbrener, David and Whitney, William F. and Ranganath, Rajesh and Bruna, Joan},
  booktitle    = {Advances in Neural Information Processing Systems (NeurIPS)},
  year         = {2021},
  eprint       = {2106.08909},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2106.08909}
}
```

#### 2110.14000 — REF-RL-005 (19d)
- Title: Towards Hyperparameter-free Policy Selection for Offline Reinforcement Learning
- Authors (full): Siyuan Zhang; Nan Jiang
- Year / Venue: 2021 (submitted 26 Oct 2021, v3 2 Nov 2021) / NeurIPS 2021
- arXiv primary category: cs.LG (cross-list: cs.AI, stat.ML) · DOI: 10.48550/arXiv.2110.14000
- Problem+method: Builds hyperparameter-free offline policy-selection on BVFT (value-function selection), effective on discrete Atari, and combines BVFT with OPE for continuous actions — how to pick the alarm policy without live trials.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@inproceedings{zhang2021bvft,
  title        = {Towards Hyperparameter-free Policy Selection for Offline Reinforcement Learning},
  author       = {Zhang, Siyuan and Jiang, Nan},
  booktitle    = {Advances in Neural Information Processing Systems (NeurIPS)},
  year         = {2021},
  eprint       = {2110.14000},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2110.14000}
}
```

#### 2311.18206 — REF-RL-006 (19d)
- Title: SCOPE-RL: A Python Library for Offline Reinforcement Learning and Off-Policy Evaluation
- Authors (full): Haruka Kiyohara; Ren Kishimoto; Kosuke Kawakami; Ken Kobayashi; Kazuhide Nakata; Yuta Saito
- Year / Venue: 2023 (submitted 30 Nov 2023, v3 11 Mar 2024) / arXiv
- arXiv primary category: cs.LG (cross-list: cs.AI) · DOI: 10.48550/arXiv.2311.18206
- Problem+method: An open-source library unifying offline RL + OPE + OPS, emphasising full reward-distribution OPE and a risk-return-tradeoff evaluation-of-OPE protocol — frames the honest OPE gate (ties BVFT).
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{kiyohara2023scoperl,
  title        = {SCOPE-RL: A Python Library for Offline Reinforcement Learning and Off-Policy Evaluation},
  author       = {Kiyohara, Haruka and Kishimoto, Ren and Kawakami, Kosuke and Kobayashi, Ken and Nakata, Kazuhide and Saito, Yuta},
  year         = {2023},
  eprint       = {2311.18206},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2311.18206}
}
```

#### 2603.17319 — REF-FUS-031 (19b) [title corrected]
- Title: Physics-informed offline reinforcement learning eliminates catastrophic fuel waste in maritime routing
- Authors (full): Aniruddha Bora; Julie Chalfant; Chryssostomos Chryssostomidis
- Year / Venue: 2026 (submitted 18 Mar 2026) / arXiv
- arXiv primary category: cs.AI (cross-list: cs.LG, cs.RO) · DOI: 10.48550/arXiv.2603.17319
- Problem+method: PIER — physics-informed, risk-aware offline RL that learns routing policies from physics-calibrated environments with a decoupled post-hoc safety shield, optimising the *tail* (catastrophic fuel waste cut 9×) not the mean — the template for the safe-RL shield. (Shorthand "PIER physics-informed offline RL (IQL) + decoupled shield" in §3 refers to this maritime-routing paper.)
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{bora2026pier,
  title        = {Physics-informed offline reinforcement learning eliminates catastrophic fuel waste in maritime routing},
  author       = {Bora, Aniruddha and Chalfant, Julie and Chryssostomidis, Chryssostomos},
  year         = {2026},
  eprint       = {2603.17319},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  doi          = {10.48550/arXiv.2603.17319}
}
```

### Physics / PINN / flood / landslide

#### 2610.04828 — REF-PINN-006 (19a) [title corrected]
- Title: Label-free physics-informed strength reduction and a neural operator for the reliability of spatially variable slopes
- Authors (full): Apisit Robjanghvad; Sompote Youwai
- Year / Venue: 2026 (submitted 4 Oct 2026) / arXiv
- arXiv primary category: cs.CE · DOI: 10.48550/arXiv.2610.04828
- Problem+method: A label-free PINN with incremental strength-reduction reproduces Abaqus factor-of-safety within 2–3% RMS on random c-φ fields; a neural operator then predicts FoS/failure mode for a million fields in seconds — PINN-feasibility evidence to use FoS as a GATE, with a documented tail-amplification caveat.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{robjanghvad2026labelfree,
  title        = {Label-free physics-informed strength reduction and a neural operator for the reliability of spatially variable slopes},
  author       = {Robjanghvad, Apisit and Youwai, Sompote},
  year         = {2026},
  eprint       = {2610.04828},
  archivePrefix= {arXiv},
  primaryClass = {cs.CE},
  doi          = {10.48550/arXiv.2610.04828}
}
```

#### 2512.23964 — REF-PHY-007 (19a)
- Title: DUALFloodGNN: Physics-informed Graph Neural Network for Operational Flood Modeling
- Authors (full): Carlo Malapad Acosta; Herath Mudiyanselage Viraj Vidura Herath; Jia Yu Lim; Abhishek Saha; Sanka Rasnayaka; Lucy Marshall
- Year / Venue: 2025 (submitted 30 Dec 2025, v2 11 May 2026) / IJCAI-ECAI 2026 (AI4Tech track)
- arXiv primary category: cs.LG (cross-list: cs.AI) · DOI: 10.48550/arXiv.2512.23964
- Problem+method: A flood GNN embedding physical constraints at global+local scales via explicit loss terms, jointly predicting nodal water volume and edge flow with multi-step curriculum training; faster + more accurate than SOTA GNN flood models — open-source surrogate for the flood/runout gate.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@inproceedings{acosta2026dualfloodgnn,
  title        = {DUALFloodGNN: Physics-informed Graph Neural Network for Operational Flood Modeling},
  author       = {Acosta, Carlo Malapad and Herath, Herath Mudiyanselage Viraj Vidura and Lim, Jia Yu and Saha, Abhishek and Rasnayaka, Sanka and Marshall, Lucy},
  booktitle    = {IJCAI-ECAI 2026 (AI4Tech track)},
  year         = {2026},
  eprint       = {2512.23964},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2512.23964}
}
```

#### 2505.08553 — REF-PHY-006 (19a) [title corrected]
- Title: Towards Digital Twin in Flood Forecasting with Data Assimilation Satellite Earth Observations -- A Proof-of-Concept in the Alzette Catchment
- Authors (full): Thanh Huy Nguyen; Sukriti Bhattacharya; Jefferson S. Wong; Yoanne Didry; Duc Long Phan; Thomas Tamisier; Patrick Matgen
- Year / Venue: 2025 (submitted 13 May 2025) / arXiv (related: Remote Sensing)
- arXiv primary category: eess.IV · DOI: 10.48550/arXiv.2505.08553 · Related DOI: 10.3390/rs18050685
- Problem+method: A digital-twin PoC assimilating Sentinel-1 flood-probability maps into a high-resolution LISFLOOD-FP model via a particle filter (with GloFAS), giving up to 30-day forecasts with reduced uncertainty on the 2021 Alzette event — closest published analogue to satellite-into-physics fusion with honest residual-uncertainty reporting.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{nguyen2025digitaltwinflood,
  title        = {Towards Digital Twin in Flood Forecasting with Data Assimilation Satellite Earth Observations -- A Proof-of-Concept in the Alzette Catchment},
  author       = {Nguyen, Thanh Huy and Bhattacharya, Sukriti and Wong, Jefferson S. and Didry, Yoanne and Phan, Duc Long and Tamisier, Thomas and Matgen, Patrick},
  year         = {2025},
  eprint       = {2505.08553},
  archivePrefix= {arXiv},
  primaryClass = {eess.IV},
  doi          = {10.48550/arXiv.2505.08553}
}
```

#### 2211.10338 — REF-DATA-006 (19c)
- Title: Deep learning based landslide density estimation on SAR data for rapid response
- Authors (full): Vanessa Boehm; Wei Ji Leong; Ragini Bal Mahesh; Ioannis Prapas; Edoardo Nemni; Freddie Kalaitzis; Siddha Ganju; Raul Ramos-Pollán
- Year / Venue: 2022 (submitted 18 Nov 2022) / arXiv
- arXiv primary category: cs.CV (cross-list: cs.LG) · DOI: 10.48550/arXiv.2211.10338
- Problem+method: Estimates landslide density from elevation + up to three Sentinel-1 SAR acquisitions (Hurricane María, Puerto Rico), reaching 0.814 chip-level AUC using only free data, with the honest caveat that ~45% of slides are smaller than a 10 m S1 pixel — a must-cite SAR-only baseline + resolution caveat.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{boehm2022landslidedensity,
  title        = {Deep learning based landslide density estimation on SAR data for rapid response},
  author       = {Boehm, Vanessa and Leong, Wei Ji and Mahesh, Ragini Bal and Prapas, Ioannis and Nemni, Edoardo and Kalaitzis, Freddie and Ganju, Siddha and Ramos-Poll{\'a}n, Raul},
  year         = {2022},
  eprint       = {2211.10338},
  archivePrefix= {arXiv},
  primaryClass = {cs.CV},
  doi          = {10.48550/arXiv.2211.10338}
}
```

### Datasets / EO encoders / foundation models

#### 2509.17942 — REF-DATA-005 (19c) [title corrected]
- Title: StefaLand: An Efficient Geoscience Foundation Model That Improves Dynamic Land-Surface Predictions
- Authors (full): Nicholas Kraabel; Jiangtao Liu; Yuchen Bian; Daniel Kifer; Chaopeng Shen
- Year / Venue: 2025 (submitted 22 Sep 2025, v3 2 Feb 2026) / arXiv
- arXiv primary category: cs.LG (cross-list: cs.AI) · DOI: 10.48550/arXiv.2509.17942
- Problem+method: A generative spatiotemporal Earth representation model with a location-aware masked autoencoder and attribute-based (not image-based) inputs, giving strong SPATIAL generalisation on streamflow/soil-moisture/soil-composition/landslides at academic compute — the most on-point external FM/backbone candidate.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{kraabel2025stefaland,
  title        = {StefaLand: An Efficient Geoscience Foundation Model That Improves Dynamic Land-Surface Predictions},
  author       = {Kraabel, Nicholas and Liu, Jiangtao and Bian, Yuchen and Kifer, Daniel and Shen, Chaopeng},
  year         = {2025},
  eprint       = {2509.17942},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2509.17942}
}
```

#### 2608.11142 — REF-DATA-037 (19c)
- Title: SAR2Agri: Learning SAR Intensity Representations for Agricultural Monitoring
- Authors (full): Moti Rattan Gupta; Anupam Sobti
- Year / Venue: 2026 (submitted 11 Aug 2026) / arXiv
- arXiv primary category: cs.CV · DOI: 10.48550/arXiv.2608.11142
- Problem+method: First SSL pipeline using SAR-intensity imagery only, with masking + curriculum temporal pretext tasks; 84.9% IoU crop-type mapping on SICKLE, +15.3 pt over optical and +2.2 pt over SAR baselines — the SAR-first self-supervised encoder recipe for data-poor regions.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{gupta2026sar2agri,
  title        = {SAR2Agri: Learning SAR Intensity Representations for Agricultural Monitoring},
  author       = {Gupta, Moti Rattan and Sobti, Anupam},
  year         = {2026},
  eprint       = {2608.11142},
  archivePrefix= {arXiv},
  primaryClass = {cs.CV},
  doi          = {10.48550/arXiv.2608.11142}
}
```

#### 2610.08810 — EO foundation-model drift (additional load-bearing)
- Title: Transferability and operational reliability of a Prithvi crop classification foundation model under phenological and geographic shift across three continents
- Authors (full): Venkatesh Kolluru; Rajat Shinde; Abdelhak Marouane; Caden Helbling; Deepak Shah; Othneil Drew; Srinivas Kolluru; Iksha Gurung; Manil Maskey; Rahul Ramachandran
- Year / Venue: 2026 (submitted 20 Sep 2026) / arXiv
- arXiv primary category: cs.LG (cross-list: cs.AI) · DOI: 10.48550/arXiv.2610.08810
- Problem+method: Out-of-distribution evaluation of Prithvi-EO-2.0 across 37 events / 12 countries: mean OA falls 0.65→0.40 US→Europe, deterministic confidence stays high while MC-dropout entropy flags the shift — evidence that GeoFMs transfer only where observation windows match local phenology (drift/calibration caution).
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{kolluru2026prithvitransfer,
  title        = {Transferability and operational reliability of a Prithvi crop classification foundation model under phenological and geographic shift across three continents},
  author       = {Kolluru, Venkatesh and Shinde, Rajat and Marouane, Abdelhak and Helbling, Caden and Shah, Deepak and Drew, Othneil and Kolluru, Srinivas and Gurung, Iksha and Maskey, Manil and Ramachandran, Rahul},
  year         = {2026},
  eprint       = {2610.08810},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2610.08810}
}
```

### Perception / CCTV / anomaly

#### 2306.00001 — REF-CCTV-001 (19c) [title corrected]
- Title: TinyissimoYOLO: A Quantized, Low-Memory Footprint, TinyML Object Detection Network for Low Power Microcontrollers
- Authors (full): Julian Moosmann; Marco Giordano; Christian Vogt; Michele Magno
- Year / Venue: 2023 (submitted 22 May 2023, v2 12 Jul 2023) / IEEE AICAS 2023
- arXiv primary category: cs.CV (cross-list: cs.AR, eess.IV) · DOI: 10.48550/arXiv.2306.00001 · Related DOI: 10.1109/AICAS57966.2023.10168657
- Problem+method: A 422k-parameter INT8 object detector running on MCUs (<0.5 MB weights), reaching up to 180 fps and 196 µJ/inference on MAX78000 — hard evidence of what a ≤₹2000 edge node can actually run (vs GPU benchmarks).
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@inproceedings{moosmann2023tinyissimoyolo,
  title        = {TinyissimoYOLO: A Quantized, Low-Memory Footprint, TinyML Object Detection Network for Low Power Microcontrollers},
  author       = {Moosmann, Julian and Giordano, Marco and Vogt, Christian and Magno, Michele},
  booktitle    = {2023 IEEE 5th International Conference on Artificial Intelligence Circuits and Systems (AICAS)},
  year         = {2023},
  eprint       = {2306.00001},
  archivePrefix= {arXiv},
  primaryClass = {cs.CV},
  doi          = {10.1109/AICAS57966.2023.10168657}
}
```

#### 2610.06453 — REF-CCTV-021 (19c) [title corrected]
- Title: Normality Constraint Learning: Adapting Foundation Models for Time Series Anomaly Detection
- Authors (full): Xiaohui Zhou; Yijie Wang; Hongzuo Xu; Weixuan Liang; Guansong Pang
- Year / Venue: 2026 (submitted 5 Oct 2026) / arXiv
- arXiv primary category: cs.AI · DOI: 10.48550/arXiv.2610.06453
- Problem+method: NCL — a plug-and-play framework that constrains a pre-trained time-series foundation model's broad pattern space to a compact normality subspace so anomalies are no longer reconstructed well, restoring reconstruction-error anomaly scores — a warning + fix for the anomaly/drift layer. (TOP-30 shorthand "Normal-Subspace Constrained Learning" ≈ this "Normality Constraint Learning".)
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{zhou2026ncl,
  title        = {Normality Constraint Learning: Adapting Foundation Models for Time Series Anomaly Detection},
  author       = {Zhou, Xiaohui and Wang, Yijie and Xu, Hongzuo and Liang, Weixuan and Pang, Guansong},
  year         = {2026},
  eprint       = {2610.06453},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  doi          = {10.48550/arXiv.2610.06453}
}
```

### Deepfake / crisis-informatics / evaluation / threshold / alerting

#### 2003.01279 — REF-ROB-130 (19d) [title corrected]
- Title: Disrupting Deepfakes: Adversarial Attacks Against Conditional Image Translation Networks and Facial Manipulation Systems
- Authors (full): Nataniel Ruiz; Sarah Adel Bargal; Stan Sclaroff
- Year / Venue: 2020 (submitted 3 Mar 2020, v3 27 Apr 2020) / CVPR 2020 Workshop (Adversarial ML in Computer Vision)
- arXiv primary category: cs.CV (cross-list: cs.CR, cs.CY, cs.LG) · DOI: 10.48550/arXiv.2003.01279
- Problem+method: Proposes class-transferable adversarial attacks + GAN adversarial training to *disrupt* deepfake image-translation outputs, plus a spread-spectrum attack evading blur defenses — defensive-only framing for WS2.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@inproceedings{ruiz2020disruptingdeepfakes,
  title        = {Disrupting Deepfakes: Adversarial Attacks Against Conditional Image Translation Networks and Facial Manipulation Systems},
  author       = {Ruiz, Nataniel and Bargal, Sarah Adel and Sclaroff, Stan},
  booktitle    = {CVPR 2020 Workshop on Adversarial Machine Learning in Computer Vision},
  year         = {2020},
  eprint       = {2003.01279},
  archivePrefix= {arXiv},
  primaryClass = {cs.CV},
  doi          = {10.48550/arXiv.2003.01279}
}
```

#### 2007.05848 — REF-EVAL-025 (19b) [title corrected]
- Title: Fighting Disaster Misinformation in Latin America: The #19S Mexican Earthquake Case Study
- Authors (full): Claudia Flores-Saviaga; Saiph Savage
- Year / Venue: 2020 (submitted 11 Jul 2020) / Personal and Ubiquitous Computing (Springer) 2020
- arXiv primary category: cs.HC (cross-list: cs.SI) · DOI: 10.48550/arXiv.2007.05848 · Related DOI: 10.1007/s00779-020-01411-5
- Problem+method: Multi-platform crisis-informatics study of the 2017 #19S Mexico earthquake (survey + Facebook/Twitter/Slack/GitHub), documenting citizen news-verification and obsolete-information handling — grounds "social/deepfake signals are low-trust and must be corroborated" (Rule 19). (TOP-30 shorthand "#Verificado19S" ≈ this #19S case study.)
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@article{floressaviaga2020disastermisinfo,
  title        = {Fighting Disaster Misinformation in Latin America: The \#19S Mexican Earthquake Case Study},
  author       = {Flores-Saviaga, Claudia and Savage, Saiph},
  journal      = {Personal and Ubiquitous Computing},
  year         = {2020},
  eprint       = {2007.05848},
  archivePrefix= {arXiv},
  primaryClass = {cs.HC},
  doi          = {10.1007/s00779-020-01411-5}
}
```

#### 2104.11422 — REF-EVAL-001 (19b)
- Title: Socio-meteorology: flood prediction, social preparedness, and cry wolf effects
- Authors (full): Yohei Sawada; Rin Kanai; Hitomu Kotani
- Year / Venue: 2021 (submitted 23 Apr 2021, v3 30 Sep 2021) / arXiv
- arXiv primary category: physics.geo-ph (cross-list: physics.soc-ph) · DOI: 10.48550/arXiv.2104.11422
- Problem+method: Extends a socio-hydrological model with social collective trust in flood early-warning systems, reproducing the cry-wolf effect (false alarms erode compliance, worse in low-frequency-disaster regions) and showing forecasters must set thresholds considering social dynamics — the social half of threshold design.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{sawada2021sociometeorology,
  title        = {Socio-meteorology: flood prediction, social preparedness, and cry wolf effects},
  author       = {Sawada, Yohei and Kanai, Rin and Kotani, Hitomu},
  year         = {2021},
  eprint       = {2104.11422},
  archivePrefix= {arXiv},
  primaryClass = {physics.geo-ph},
  doi          = {10.48550/arXiv.2104.11422}
}
```

#### 2509.11789 — REF-EVAL-005 (19b) [title corrected]
- Title: Watch Your Step: A Cost-Sensitive Framework for Accelerometer-Based Fall Detection in Real-World Streaming Scenarios
- Authors (full): Timilehin B. Aderinola; Luca Palmerini; Ilaria D'Ascanio; Lorenzo Chiari; Jochen Klenk; Clemens Becker; Brian Caulfield; Georgiana Ifrim
- Year / Venue: 2025 (submitted 15 Sep 2025) / arXiv
- arXiv primary category: cs.LG · DOI: 10.48550/arXiv.2509.11789
- Problem+method: Streaming IMU fall-detection (FARSEEING, 60+ h) that tunes the decision threshold with a cost function reflecting miss ≫ false-alarm cost, achieving Recall 1.00 / Precision 0.84 / F1 0.91 at <5 ms/sample — validates the asymmetric-cost p* threshold methodology.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{aderinola2025watchyourstep,
  title        = {Watch Your Step: A Cost-Sensitive Framework for Accelerometer-Based Fall Detection in Real-World Streaming Scenarios},
  author       = {Aderinola, Timilehin B. and Palmerini, Luca and D'Ascanio, Ilaria and Chiari, Lorenzo and Klenk, Jochen and Becker, Clemens and Caulfield, Brian and Ifrim, Georgiana},
  year         = {2025},
  eprint       = {2509.11789},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2509.11789}
}
```

#### 2503.14621 — REF-EVAL-008 (19b)
- Title: Reducing False Ventricular Tachycardia Alarms in ICU Settings: A Machine Learning Approach
- Authors (full): Grace Funmilayo Farayola; Akinyemi Sadeeq Akintola; Oluwole Fagbohun; Chukwuka Michael Oforgu; Bisola Faith Kayode; Christian Chimezie; Temitope Kadri; Abiola Oludotun; Nelson Ogbeide; Mgbame Michael; Adeseye Ifaturoti; Toyese Oloyede
- Year / Venue: 2025 (submitted 18 Mar 2025) / ICMLT 2025 (Helsinki)
- arXiv primary category: cs.LG (cross-list: cs.AI) · DOI: 10.48550/arXiv.2503.14621
- Problem+method: Trains deep models on the VTaC benchmark to classify true vs false ICU ventricular-tachycardia alarms from waveform time/frequency features, with ROC-AUC >0.96 — supports a two-stage alarm-verification layer that suppresses false alarms without missing events.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@inproceedings{farayola2025falsevt,
  title        = {Reducing False Ventricular Tachycardia Alarms in ICU Settings: A Machine Learning Approach},
  author       = {Farayola, Grace Funmilayo and Akintola, Akinyemi Sadeeq and Fagbohun, Oluwole and Oforgu, Chukwuka Michael and Kayode, Bisola Faith and Chimezie, Christian and Kadri, Temitope and Oludotun, Abiola and Ogbeide, Nelson and Michael, Mgbame and Ifaturoti, Adeseye and Oloyede, Toyese},
  booktitle    = {International Conference on Machine Learning Technologies (ICMLT)},
  year         = {2025},
  eprint       = {2503.14621},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2503.14621}
}
```

#### 2601.05921 — note-only (grounds equations-register E-07) [title corrected]
- Title: Evaluating infectious disease forecasts in a cost-loss situation
- Authors (full): Philip Gerlee; Torbjörn Lundh; Anna Saxne Jöud; Henrik Thorén
- Year / Venue: 2026 (submitted 9 Jan 2026) / arXiv
- arXiv primary category: q-bio.QM · DOI: 10.48550/arXiv.2601.05921
- Problem+method: Adapts a decision-theoretic Value Score (VS) that compares a decision-maker's expected expense acting on a forecast vs on historical event probabilities across the cost-loss ratio range (applied to FluSight influenza-peak forecasts); VS is sensitive to over/under-prediction unlike log-score — the primary cost-loss evaluation metric (E-07). (Domain is epidemiology, applied here as a general EWS cost-loss method.)
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{gerlee2026costloss,
  title        = {Evaluating infectious disease forecasts in a cost-loss situation},
  author       = {Gerlee, Philip and Lundh, Torbj{\"o}rn and J{\"o}ud, Anna Saxne and Thor{\'e}n, Henrik},
  year         = {2026},
  eprint       = {2601.05921},
  archivePrefix= {arXiv},
  primaryClass = {q-bio.QM},
  doi          = {10.48550/arXiv.2601.05921}
}
```

#### 2603.15945 — REF-ALERT-008 (19d) [title corrected]
- Title: Evaluating Performance Characteristic of Opportunistic Routing Protocols: A Case Study of the 2016 Italian League Match Earthquake in the Stadio Adriatico
- Authors (full): Yihang Cao; Milena Radenkovic
- Year / Venue: 2026 (submitted 16 Mar 2026) / arXiv
- arXiv primary category: cs.NI · DOI: 10.48550/arXiv.2603.15945
- Problem+method: Simulates DTN opportunistic routing in a modelled 2016 Central-Italy-earthquake-during-a-football-match scenario, comparing Epidemic vs Spray-and-Wait on delivery/latency/overhead/hops/drops; Spray-and-Wait gives the better reliability-efficiency balance — which store-carry-forward protocol for backhaul-down alerting.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{cao2026opportunisticrouting,
  title        = {Evaluating Performance Characteristic of Opportunistic Routing Protocols: A Case Study of the 2016 Italian League Match Earthquake in the Stadio Adriatico},
  author       = {Cao, Yihang and Radenkovic, Milena},
  year         = {2026},
  eprint       = {2603.15945},
  archivePrefix= {arXiv},
  primaryClass = {cs.NI},
  doi          = {10.48550/arXiv.2603.15945}
}
```

#### 2604.24404 — REF-RL-022 (19d) [title corrected]
- Title: From Spoofing to Trust: Emergency Alerts Spoofing Testbed and Cross-Cell Verification
- Authors (full): Abdallah Abou Hasna; Nada Chendeb; Ammar El Falou
- Year / Venue: 2026 (submitted 27 Apr 2026) / IEEE VTC-Spring
- arXiv primary category: cs.CR (cross-list: eess.SP) · DOI: 10.48550/arXiv.2604.24404
- Problem+method: First open-source 5G emergency-alert (PWS) spoofing testbed (OAI RAN + SDR), showing phones readily display forged warnings, then proposes a lightweight cross-cell verification that flags single-source alerts — grounds "sign CAP + authenticated mesh". (TOP-30 shorthand "Open-Source 5G Public Warning System Spoofing Testbed" ≈ this paper.)
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@inproceedings{abouhasna2026spoofingtrust,
  title        = {From Spoofing to Trust: Emergency Alerts Spoofing Testbed and Cross-Cell Verification},
  author       = {Abou Hasna, Abdallah and Chendeb, Nada and El Falou, Ammar},
  booktitle    = {IEEE Vehicular Technology Conference (VTC-Spring)},
  year         = {2026},
  eprint       = {2604.24404},
  archivePrefix= {arXiv},
  primaryClass = {cs.CR},
  doi          = {10.48550/arXiv.2604.24404}
}
```

#### 2405.01602 — India flood severity index (additional load-bearing)
- Title: A District-level Flood Severity Index for Flood Management in India
- Authors (full): Manabendra Saharia; Sharad K Jain; Ved Prakash; Harshul Malik; O P Sreejith; Dheeraj Joshi
- Year / Venue: 2024 (submitted 1 May 2024, v2 21 Dec 2024) / arXiv
- arXiv primary category: physics.soc-ph · DOI: 10.48550/arXiv.2405.01602
- Problem+method: Builds the India Flood Inventory with Impacts (IFI-Impacts) death/damage database and a novel District Flood Severity Index (DFSI) combining people affected, flood spread and duration at the district administrative unit — a pan-India flood-management prioritisation tool.
- Resolved on 2026-10-10 via arxiv.org/abs — YES
```bibtex
@misc{saharia2024dfsi,
  title        = {A District-level Flood Severity Index for Flood Management in India},
  author       = {Saharia, Manabendra and Jain, Sharad K and Prakash, Ved and Malik, Harshul and Sreejith, O P and Joshi, Dheeraj},
  year         = {2024},
  eprint       = {2405.01602},
  archivePrefix= {arXiv},
  primaryClass = {physics.soc-ph},
  doi          = {10.48550/arXiv.2405.01602}
}
```

## 4. DATASET ↔ REFERENCE cross-index
Links the datasets catalogued for chapter 04 (`DATASETS.md` / `DATASETS_CATALOGUE.md`, entries D113–D164) to their source paper. `in ledger?` says whether that source arXiv ID is also a catalogue row here (and its REF-id).
> All dataset rows are RESEARCH-ONLY leads: no download link was tested, licenses are indicative, and EULA/restricted sets are flagged in `DATASETS_CATALOGUE.md` §K. Sizes tagged "named" come from a citing abstract, not the owning paper.

| D# | Dataset | WS | Source arXiv | in ledger? (REF-id) | note |
|---|---|---|---|---|---|
| D113 | FIgLib (Fire Ignition Library) | WS4 | 2112.08598 | yes (REF-CCTV-024) |  |
| D114 | SKLFS-WildFire Test | WS4 | 2311.10116 | yes (REF-DATA-049) |  |
| D115 | GWFP (Global Wildfire Prevention) | WS4 | 2606.10174 | yes (REF-DATA-050) | host-TBA, may not be live |
| D116 | AusSmoke + MultiNatSmoke | WS4 | 2604.23542 | yes (REF-DATA-051) |  |
| D117 | PYRONEAR-2025 | WS4 | 2402.05349 | yes (REF-CCTV-025) |  |
| D118 | The Wildfire Dataset | WS4 | 2505.17395 | yes (REF-DATA-052) |  |
| D119 | FASDD (Flame & Smoke Detection) | WS4 | 2501.08639 | yes (REF-CCTV-069) | size "named" |
| D120 | D-Fire | WS4 | 2501.08639 | yes (REF-CCTV-069) | size "named" |
| D121 | AFSE (Aerial Fire & Smoke Essential) | WS4 | 2501.08639 | yes (REF-CCTV-069) |  |
| D122 | USTC_SmokeRS | WS1b/WS4 | 2310.01711 | yes (REF-DATA-053) |  |
| D123 | Landsat_Smk | WS1b/WS4 | 2310.01711 | yes (REF-DATA-053) |  |
| D124 | WildfireSpreadTS (WSTS) | WS1b | 2603.09042 | no (source not a ledger row) |  |
| D125 | MOD14 / VNP14 fire masks | WS1b/WS8 | 2503.08580 | yes (REF-DATA-054) |  |
| D126 | CaBuAr California Burned Areas | WS1b | 2401.11519 | yes (REF-DATA-055) |  |
| D127 | MultiEarth Amazon | WS1b | 2307.04916 | yes (REF-DATA-056) |  |
| D128 | EFFIS hotspot crossref | WS1b | 2308.02508 | yes (REF-DATA-057) | host-TBA |
| D129 | Sen1Floods11 | WS1b | 2307.07123 | yes (REF-PHY-012) | size "named" |
| D130 | SEN12-FLOOD | WS1b | 2307.07123 | yes (REF-PHY-012) |  |
| D131 | C2S-MS Floods | WS1b | 2601.00123 | yes (REF-DATA-058) |  |
| D132 | GEOID-Flood | WS1b | 2608.02315 | yes (REF-DATA-039) |  |
| D133 | S1GFloods | WS1b | 2306.00704 | yes (REF-DATA-059) |  |
| D134 | Kuro Siwo | WS1b | 2311.12056 | yes (REF-DATA-060) |  |
| D135 | Citizen-Science Flood Extent | WS1b | 2311.09276 | yes (REF-DATA-061) |  |
| D136 | LMHLD (DOI 10.5281/zenodo.11424988) | WS1b | 2502.19866 | yes (REF-DATA-042) |  |
| D137 | Landslide4Sense | WS1b | 2403.10127 | yes (REF-DATA-062) | size "named" |
| D138 | Bijie landslide | WS1b | 2403.10127 | yes (REF-DATA-062) | size "named" |
| D139 | PILD (event-isolated) | WS1b | 2608.09325 | yes (REF-DATA-063) |  |
| D140 | MMLSv2 (MARTIAN — out of scope) | WS1b | 2602.08112 | yes (REF-DATA-064) | out of Earth scope |
| D141 | Hephaestus InSAR | WS1b | 2204.09435 | yes (REF-DATA-065) |  |
| D142 | Thalia InSAR datacubes | WS1b | 2505.17782 | yes (REF-DATA-044) |  |
| D143 | KnowAir (PM2.5-GNN) | WS7/WS8 | 2002.12898 | yes (REF-DATA-066) |  |
| D144 | TAP (Tracking Air Pollution China) | WS7/WS8 | 2103.06520 | yes (REF-DATA-067) |  |
| D145 | Bihar low-cost PM2.5 network | WS7/WS8 | 2412.13935 | yes (REF-DATA-068) | host-TBA |
| D146 | California Wildfire PM2.5 | WS7/WS8 | 2607.07951 | yes (REF-CCTV-051) |  |
| D147 | CEED (California EQ Event) | WS8 | 2502.11500 | yes (REF-DATA-069) |  |
| D148 | STEAD (Stanford EQ) | WS8 | 2408.06629 | yes (REF-DATA-070) | size "named" |
| D149 | POSEIDON (HF) | WS8 | 2601.02264 | yes (REF-DATA-071) |  |
| D150 | MultiSeismo | WS8 | 2605.26320 | yes (REF-DATA-072) |  |
| D151 | CrisisBench / CrisisNLP | WS2/WS3 | 2004.06774 | yes (REF-DATA-073) |  |
| D152 | CrisisMMD | WS2/WS3 | 1805.00713 | yes (REF-DATA-074) |  |
| D153 | MEDIC | WS2/WS3 | 2108.12828 | yes (REF-DATA-075) |  |
| D154 | GeoCoV19 | WS2/WS3 | 2005.11177 | yes (REF-ALERT-077) |  |
| D155 | HumAID / HUMAID-NER | WS2/WS3 | 2609.16964 | yes (REF-ROB-072) |  |
| D156 | TSEqD (Turkey-Syria EQ) | WS2/WS3 | 2410.08814 | yes (REF-DATA-076) | host-TBA |
| D157 | DisasterVQA (DOI 10.5281/zenodo.18267769) | WS2/WS3 | 2601.13839 | yes (REF-DATA-077) |  |
| D158 | DFDC | WS2 | 1910.08854 | yes (REF-DATA-078) | EULA |
| D159 | FaceForensics++ | WS2 | 2107.02045 | yes (REF-DATA-079) | EULA, size "named" |
| D160 | FakeAVCeleb | WS2 | 2108.05080 | yes (REF-DATA-080) | access-on-request |
| D161 | DeepFake MNIST+ | WS2 | 2108.07949 | yes (REF-DATA-081) |  |
| D162 | CtrSVDD | WS2 | 2406.02438 | yes (REF-DATA-082) |  |
| D163 | Codecfake | WS2 | 2406.08112 | yes (REF-DATA-083) |  |
| D164 | AUDETER | WS2 | 2509.04345 | yes (REF-DATA-084) |  |

## 5. Local-note baseline corpus — notes WITHOUT a ledger row (55 IDs)
These arXiv IDs have a file in `analysis/03_paper_notes/` but are **not rows in `analysis/02_paper_ledger.csv`** — they are the pre-existing baseline/landmark corpus (`trinetra/papers/`, per `REFERENCES.md` status) tracked separately. Metadata here is from the **note filename slug only** (not the ledger); authors/titles are not reproduced to avoid fabrication — open the note file for detail. Verification: not re-fetched this pass.

| arXiv/DOI | note slug (filename) |
|---|---|
| 1707.06347 | PPO |
| 1707.08114 | MTL_survey |
| 1708.08611 | safe_RL_shielding |
| 1801.01290 | SAC |
| 1806.05035 | probabilistic_dam_breach_bayesian |
| 1904.02639 | MemAE_anomaly |
| 1909.01968 | ACES_energy_harvesting_RL |
| 2005.01643 | offlineRL_survey |
| 2006.04779 | CQL |
| 2007.02756 | FFM_GPS_CampiFlegrei |
| 2009.07415 | MetaAAD |
| 2010.09107 | QUOTA_EnbPI_conformal_timeseries |
| 2010.14934 | beekeeping_energy_IoT |
| 2103.09783 | QUOTA_technical_debt_AI_systems |
| 2104.11009 | PIML_hydrology_Narmada |
| 2106.06860 | TD3BC |
| 2106.10652 | TinyML_ESP32 |
| 2107.07511 | conformal_intro |
| 2108.06852 | HF2VAD_video_anomaly |
| 2108.06868 | NowcastingNets_ABS |
| 2110.06169 | IQL |
| 2112.11965 | passive_RFID_geoscience |
| 2201.06837 | SNN_landslide_susceptibility |
| 2204.06097 | ML_surrogate_slope_stability |
| 2205.09884 | RL_model_selection |
| 2206.00515 | Landslide4Sense_benchmark |
| 2206.09981 | QUOTA_imbalance_metric_sensitivity |
| 2209.11632 | QUOTA_continuous_ML_safety_assurance |
| 2210.04218 | FloodTransformer_segmentation |
| 2211.07044 | SSL4EO_S12_dataset |
| 2212.12038 | community_detection_InSAR |
| 2304.07193 | DINOv2 |
| 2306.12826 | lowcost_DGPS_ublox |
| 2307.04016 | LTE_solar_urban_sensornet |
| 2308.11929 | dynamic_LSA_InSAR |
| 2311.00566 | CROMA_radar_optical_SSL |
| 2311.01564 | InSAR_ElForn |
| 2311.14110 | QUOTA_datacope_ope_evaluation |
| 2402.12095 | MajorTOM_EO_dataset |
| 2404.10135 | LSTM_precip_merge_SierraNevada |
| 2404.19452 | QUOTA_drift_detection_energy |
| 2405.00031 | QUOTA_segnet_wildfire_detection |
| 2410.06388 | QUOTA_alert_fatigue_pedestrian |
| 2412.04563 | LoRa_rural_Nepal |
| 2412.11942 | DRUM_ABS |
| 2412.13439 | QUOTA_MIP_ensemble_rare_event |
| 2412.14123 | AnySat_EO_model |
| 2503.11849 | Copernicus_FM |
| 2509.10560 | GTS_Forecaster_geodetic |
| 2601.05921 | QUOTA_cost_loss_value_score |
| 2604.25512 | QUOTA_posthoc_reasoning_phishing |
| 2606.21130 | QUOTA_burst_aware_EWS_threshold |
| 2608.19672 | SAGE_XGBoost_ABS |
| 2608.26304 | QUOTA_flood_evacuation_equity |
| nhess-22-3309-2022 | chamoli_precollapse |

## 6. Note on 2608.22293 (why the correction matters)
`_CANON.md` §6 corrects an earlier draft that cited **2608.22293** for the spatial-CV verdict and states it is "NOT in the source artifacts". In the live ledger, 2608.22293 **is** present (REF-ALERT-068, ABS): "Spatial Anatomy of Urban Wildfire Vulnerability (GeoAI Palisades)" — a *different* topic. So the operative rule holds (do **not** cite 2608.22293 for spatial-CV; use **2608.12422**), but the parenthetical "not in the source artifacts" is inaccurate for the current file. Flagged for the consistency gate.

## 7. MASTER INDEX — all catalogued identifiers (numeric/alpha sort)
All **775** unique identifiers, with REF-id, read-depth, and the split file that holds the full entry. `*` marks IDs that also have a local note.

| arXiv/DOI | REF-id | rd | file | note |
|---|---|---|---|---|
| 0709.0086 | REF-PHY-147 | ABS | 19a |  |
| 10.1109/IGARSS46834.2022.9883132 | REF-PHY-013 | ABS | 19a |  |
| 10.1145/3485730.3493444 | REF-ALERT-013 | ABS | 19d |  |
| 1010.4385 | REF-ALERT-007 | ABS | 19d |  |
| 1101.5745 | REF-PHY-072 | ABS | 19a |  |
| 1103.1678 | REF-PHY-079 | ABS | 19a |  |
| 1106.1638 | REF-FUS-065 | ABS | 19b |  |
| 1106.3698 | REF-PHY-126 | ABS | 19a |  |
| 1203.0541 | REF-ROB-056 | ABS | 19d |  |
| 1203.1396 | REF-PHY-124 | ABS | 19a |  |
| 1204.6231 | REF-ROB-055 | ABS | 19d |  |
| 1206.3345 | REF-PHY-118 | ABS | 19a |  |
| 1207.4144 | REF-FUS-066 | ABS | 19b |  |
| 1208.6116 | REF-PHY-084 | ABS | 19a |  |
| 1209.5256 | REF-PHY-083 | ABS | 19a |  |
| 1301.4795 | REF-ALERT-055 | ABS | 19d |  |
| 1306.1529 | REF-PHY-082 | ABS | 19a |  |
| 1308.2907 | REF-ALERT-017 | ABS | 19d |  |
| 1406.4058 | REF-PHY-132 | ABS | 19a |  |
| 1408.0104 | REF-ALERT-014 | ABS | 19d |  |
| 1411.3736 | REF-ROB-122 | ABS | 19d |  |
| 1507.07837 | REF-PHY-019 | ABS | 19a |  |
| 1509.05505 | REF-ALERT-021 | ABS | 19d |  |
| 1509.06065 | REF-ROB-057 | ABS | 19d |  |
| 1509.09222 | REF-ROB-121 | ABS | 19d |  |
| 1511.08331 | REF-ALERT-004 | ABS | 19d |  |
| 1601.06272 | REF-PHY-068 | ABS | 19a |  |
| 1607.04139 | REF-CCTV-013 | ABS | 19c |  |
| 1703.01985 | REF-ALERT-019 | ABS | 19d |  |
| 1703.04550 | REF-RL-068 | ABS | 19d |  |
| 1703.05530 | REF-CCTV-031 | ABS | 19c |  |
| 1705.00470 | REF-RL-055 | ABS | 19d |  |
| 1706.03458 | REF-PHY-023 | ABS | 19a |  |
| 1707.03682 | REF-ALERT-060 | ABS | 19d |  |
| 1707.06611 | REF-ROB-027 | ABS | 19d |  |
| 1707.07821 | REF-ROB-123 | ABS | 19d |  |
| 1708.08750 | REF-ALERT-045 | ABS | 19d |  |
| 1803.00275 | REF-ALERT-020 | ABS | 19d |  |
| 1803.09010 | REF-EVAL-043 | ABS | 19b |  |
| 1805.00713 | REF-DATA-074 | ABS | 19c |  |
| 1805.11999 | REF-ALERT-041 | ABS | 19d |  |
| 1806.10131 | REF-ROB-140 | ABS | 19d |  |
| 1809.04324 | REF-ALERT-015 | ABS | 19d |  |
| 1810.03993 | REF-EVAL-042 | ABS | 19b |  |
| 1810.11498 | REF-ALERT-065 | ABS | 19d |  |
| 1811.03761 | REF-FUS-070 | ABS | 19b |  |
| 1901.04695 | REF-PHY-015 | ABS | 19a |  |
| 1903.02611 | REF-ALERT-009 | ABS | 19d |  |
| 1904.01963 | REF-ALERT-022 | ABS | 19d |  |
| 1904.07213 | REF-PHY-033 | ABS | 19a |  |
| 1905.07286 | REF-DATA-002 | ABS | 19c |  |
| 1906.01379 | REF-DATA-008 | ABS | 19c |  |
| 1906.02998 | REF-ALERT-003 | ABS | 19d |  |
| 1906.07233 | REF-RL-066 | ABS | 19d |  |
| 1908.03620 | REF-PHY-145 | ABS | 19a |  |
| 1909.01868 | REF-DATA-017 | ABS | 19c |  |
| 1909.10155 | REF-EVAL-044 | ABS | 19b |  |
| 1909.12937 | REF-CCTV-060 | ABS | 19c |  |
| 1910.03345 | REF-ALERT-029 | ABS | 19d |  |
| 1910.08854 | REF-DATA-078 | ABS | 19c |  |
| 1910.09098 | REF-PHY-139 | ABS | 19a |  |
| 1910.14655 | REF-ROB-127 | ABS | 19d |  |
| 1911.05219 | REF-PHY-025 | ABS | 19a |  |
| 1911.11380 | REF-PHY-140 | ABS | 19a |  |
| 1912.06384 | REF-ALERT-040 | ABS | 19d |  |
| 2001.00769 | REF-DATA-011 | ABS | 19c |  |
| 2001.04536 | REF-PHY-073 | FT-PARTIAL | 19a |  |
| 2001.04567 | REF-ROB-012 | ABS | 19d |  |
| 2001.05367 | REF-PHY-125 | ABS | 19a |  |
| 2002.12898 | REF-DATA-066 | ABS | 19c |  |
| 2002.12906 | REF-ALERT-030 | ABS | 19d |  |
| 2003.01279 | REF-ROB-130 | ABS | 19d |  |
| 2003.08647 | REF-ALERT-054 | ABS | 19d |  |
| 2003.12206 | REF-EVAL-047 | ABS | 19b |  |
| 2004.01764 | REF-FUS-003 | ABS | 19b |  |
| 2004.06774 | REF-DATA-073 | ABS | 19c |  |
| 2005.03221 | REF-DATA-036 | FT-PARTIAL | 19c | * |
| 2005.05385 | REF-ROB-025 | ABS | 19d |  |
| 2005.11177 | REF-ALERT-077 | ABS | 19d |  |
| 2006.01332 | REF-ROB-005 | ABS | 19d |  |
| 2006.07484 | REF-EVAL-039 | ABS | 19b |  |
| 2006.08573 | REF-ROB-028 | ABS | 19d |  |
| 2006.15099 | REF-FUS-067 | ABS | 19b |  |
| 2007.02038 | REF-FUS-037 | ABS | 19b |  |
| 2007.05848 | REF-EVAL-025 | FT-PARTIAL | 19b | * |
| 2007.11117 | REF-ROB-045 | ABS | 19d |  |
| 2007.12229 | REF-ROB-051 | ABS | 19d |  |
| 2008.02862 | REF-PHY-144 | ABS | 19a |  |
| 2009.09503 | REF-ALERT-034 | ABS | 19d |  |
| 2009.13291 | REF-PINN-018 | ABS | 19a |  |
| 2010.07110 | REF-CCTV-070 | ABS | 19c |  |
| 2010.08833 | REF-CCTV-026 | ABS | 19c |  |
| 2010.11267 | REF-ROB-090 | ABS | 19d |  |
| 2011.04863 | REF-CCTV-058 | ABS | 19c |  |
| 2011.06125 | REF-FUS-012 | ABS | 19b |  |
| 2012.00640 | REF-PHY-149 | ABS | 19a |  |
| 2012.11154 | REF-PHY-034 | ABS | 19a |  |
| 2012.13849 | REF-PHY-046 | FT-PARTIAL | 19a | * |
| 2101.05397 | REF-PHY-099 | ABS | 19a |  |
| 2101.08954 | REF-FUS-043 | ABS | 19b |  |
| 2101.09429 | REF-EVAL-004 | ABS | 19b |  |
| 2101.11453 | REF-ROB-108 | ABS | 19d |  |
| 2102.00589 | REF-ALERT-026 | ABS | 19d |  |
| 2102.06491 | REF-PHY-020 | ABS | 19a | * |
| 2102.11060 | REF-PHY-131 | ABS | 19a |  |
| 2102.11273 | REF-ROB-113 | ABS | 19d |  |
| 2103.00883 | REF-PHY-103 | ABS | 19a |  |
| 2103.00903 | REF-ROB-036 | ABS | 19d |  |
| 2103.03413 | REF-EVAL-023 | ABS | 19b |  |
| 2103.06231 | REF-ALERT-048 | ABS | 19d |  |
| 2103.06520 | REF-DATA-067 | ABS | 19c |  |
| 2103.07792 | REF-ALERT-076 | ABS | 19d |  |
| 2103.08195 | REF-FUS-047 | ABS | 19b |  |
| 2103.10985 | REF-DATA-016 | ABS | 19c |  |
| 2103.15156 | REF-EVAL-018 | ABS | 19b |  |
| 2104.00615 | REF-PINN-002 | ABS | 19a |  |
| 2104.06411 | REF-RL-017 | ABS | 19d |  |
| 2104.08236 | REF-PHY-093 | ABS | 19a |  |
| 2104.10529 | REF-ROB-124 | ABS | 19d |  |
| 2104.11422 | REF-EVAL-001 | ABS | 19b | * |
| 2105.01419 | REF-ROB-047 | ABS | 19d |  |
| 2105.03876 | REF-ROB-023 | ABS | 19d |  |
| 2105.07346 | REF-PHY-105 | ABS | 19a |  |
| 2105.11397 | REF-PHY-129 | ABS | 19a |  |
| 2105.13133 | REF-PHY-018 | ABS | 19a |  |
| 2105.13331 | REF-CCTV-002 | ABS | 19c |  |
| 2106.01770 | REF-FUS-064 | ABS | 19b |  |
| 2106.04230 | REF-ALERT-028 | ABS | 19d |  |
| 2106.05532 | REF-EVAL-058 | ABS | 19b |  |
| 2106.06783 | REF-RL-067 | ABS | 19d |  |
| 2106.08909 | REF-RL-002 | ABS | 19d | * |
| 2106.12652 | REF-FUS-048 | ABS | 19b |  |
| 2106.15119 | REF-PHY-022 | ABS | 19a |  |
| 2107.02045 | REF-DATA-079 | ABS | 19c |  |
| 2107.07687 | REF-PHY-001 | ABS | 19a |  |
| 2107.11003 | REF-RL-026 | FT | 19d |  |
| 2107.13029 | REF-CCTV-047 | ABS | 19c |  |
| 2108.04907 | REF-ROB-053 | ABS | 19d |  |
| 2108.05080 | REF-DATA-080 | ABS | 19c |  |
| 2108.05415 | REF-PINN-015 | ABS | 19a |  |
| 2108.05422 | REF-PHY-110 | ABS | 19a |  |
| 2108.07949 | REF-DATA-081 | ABS | 19c |  |
| 2108.12828 | REF-DATA-075 | ABS | 19c |  |
| 2108.13264 | REF-EVAL-041 | ABS | 19b |  |
| 2109.01050 | REF-PINN-011 | FT | 19a |  |
| 2109.07745 | REF-EVAL-009 | ABS | 19b |  |
| 2110.01440 | REF-FUS-059 | ABS | 19b |  |
| 2110.06513 | REF-ROB-112 | ABS | 19d |  |
| 2110.09497 | REF-ROB-019 | ABS | 19d |  |
| 2110.10486 | REF-ALERT-049 | ABS | 19d |  |
| 2110.14000 | REF-RL-005 | ABS | 19d |  |
| 2112.03044 | REF-PHY-090 | ABS | 19a |  |
| 2112.08598 | REF-CCTV-024 | ABS | 19c |  |
| 2112.09072 | REF-ALERT-042 | ABS | 19d |  |
| 2112.11490 | REF-RL-019 | ABS | 19d |  |
| 2201.07006 | REF-DATA-027 | ABS | 19c |  |
| 2201.07125 | REF-ROB-030 | ABS | 19d |  |
| 2201.07931 | REF-PHY-136 | ABS | 19a |  |
| 2202.06567 | REF-PHY-064 | ABS | 19a |  |
| 2202.07282 | REF-ROB-033 | ABS | 19d |  |
| 2202.07475 | REF-CCTV-005 | ABS | 19c |  |
| 2202.08756 | REF-PHY-098 | ABS | 19a |  |
| 2202.11203 | REF-ROB-116 | ABS | 19d |  |
| 2203.03962 | REF-CCTV-011 | ABS | 19c |  |
| 2203.04236 | REF-RL-010 | ABS | 19d |  |
| 2203.04639 | REF-PHY-130 | ABS | 19a |  |
| 2203.05492 | REF-ALERT-047 | ABS | 19d |  |
| 2203.07404 | REF-PINN-012 | FT | 19a |  |
| 2203.07835 | REF-PHY-106 | ABS | 19a |  |
| 2203.13263 | REF-PHY-024 | ABS | 19a |  |
| 2203.13313 | REF-PHY-045 | FT-PARTIAL | 19a | * |
| 2203.17155 | REF-ROB-049 | ABS | 19d |  |
| 2204.00102 | REF-FUS-038 | ABS | 19b |  |
| 2204.07653 | REF-FUS-027 | ABS | 19b |  |
| 2204.09435 | REF-DATA-065 | ABS | 19c |  |
| 2205.12070 | REF-ROB-038 | ABS | 19d |  |
| 2205.13723 | REF-ROB-003 | ABS | 19d |  |
| 2206.01529 | REF-PHY-133 | ABS | 19a |  |
| 2206.02000 | REF-RL-001 | ABS | 19d |  |
| 2206.03669 | REF-ROB-126 | ABS | 19d |  |
| 2206.04568 | REF-FUS-068 | ABS | 19b |  |
| 2206.08501 | REF-PHY-065 | ABS | 19a |  |
| 2206.12654 | REF-ROB-114 | ABS | 19d |  |
| 2206.13405 | REF-ROB-111 | ABS | 19d |  |
| 2206.14862 | REF-PHY-075 | ABS | 19a |  |
| 2207.05748 | REF-PINN-017 | ABS | 19a |  |
| 2207.05796 | REF-ROB-141 | ABS | 19d |  |
| 2207.12406 | REF-ALERT-074 | ABS | 19d |  |
| 2207.12545 | REF-ROB-022 | ABS | 19d |  |
| 2207.14024 | REF-PHY-109 | ABS | 19a |  |
| 2208.00210 | REF-DATA-048 | ABS | 19c |  |
| 2208.03542 | REF-PINN-008 | FT | 19a |  |
| 2208.03566 | REF-ROB-042 | ABS | 19d |  |
| 2208.05875 | REF-FUS-017 | ABS | 19b |  |
| 2208.13027 | REF-ALERT-024 | ABS | 19d |  |
| 2208.13422 | REF-CCTV-055 | ABS | 19c |  |
| 2208.14501 | REF-RL-054 | ABS | 19d |  |
| 2209.02416 | REF-ALERT-070 | ABS | 19d |  |
| 2209.08729 | REF-PHY-026 | ABS | 19a |  |
| 2210.02558 | REF-ROB-046 | ABS | 19d |  |
| 2210.08470 | REF-ROB-035 | ABS | 19d |  |
| 2210.08975 | REF-EVAL-015 | ABS | 19b |  |
| 2210.10732 | REF-DATA-007 | ABS | 19c |  |
| 2210.12853 | REF-PHY-021 | ABS | 19a |  |
| 2210.14978 | REF-PHY-067 | ABS | 19a |  |
| 2210.16206 | REF-PHY-141 | ABS | 19a |  |
| 2210.16219 | REF-PHY-142 | ABS | 19a |  |
| 2210.17444 | REF-FUS-040 | ABS | 19b |  |
| 2211.10338 | REF-DATA-006 | ABS | 19c |  |
| 2211.12341 | REF-PHY-143 | ABS | 19a |  |
| 2212.00970 | REF-PINN-009 | FT | 19a |  |
| 2212.02179 | REF-RL-053 | ABS | 19d |  |
| 2212.05478 | REF-PHY-104 | ABS | 19a |  |
| 2212.12103 | REF-ROB-016 | ABS | 19d |  |
| 2212.14143 | REF-CCTV-059 | ABS | 19c |  |
| 2301.05977 | REF-DATA-024 | ABS | 19c |  |
| 2301.09615 | REF-ROB-120 | ABS | 19d |  |
| 2302.00237 | REF-RL-058 | ABS | 19d |  |
| 2302.01913 | REF-PHY-119 | ABS | 19a |  |
| 2302.04054 | REF-EVAL-040 | ABS | 19b |  |
| 2302.04960 | REF-PHY-066 | ABS | 19a |  |
| 2302.07341 | REF-ROB-119 | ABS | 19d |  |
| 2302.12127 | REF-ROB-054 | ABS | 19d |  |
| 2302.13423 | REF-RL-013 | ABS | 19d |  |
| 2303.00028 | REF-ALERT-006 | ABS | 19d |  |
| 2303.07035 | REF-DATA-019 | ABS | 19c |  |
| 2303.09750 | REF-ALERT-005 | ABS | 19d |  |
| 2303.12748 | REF-CCTV-052 | ABS | 19c |  |
| 2303.12754 | REF-ALERT-027 | ABS | 19d |  |
| 2303.12783 | REF-FUS-020 | ABS | 19b |  |
| 2303.15389 | REF-CCTV-039 | ABS | 19c |  |
| 2303.17446 | REF-PHY-128 | ABS | 19a |  |
| 2304.08319 | REF-ROB-142 | ABS | 19d |  |
| 2305.03288 | REF-FUS-052 | ABS | 19b |  |
| 2305.03360 | REF-RL-007 | ABS | 19d |  |
| 2305.04750 | REF-RL-070 | ABS | 19d |  |
| 2305.05218 | REF-PHY-016 | ABS | 19a |  |
| 2305.16147 | REF-RL-003 | ABS | 19d |  |
| 2306.00001 | REF-CCTV-001 | ABS | 19c |  |
| 2306.00704 | REF-DATA-059 | ABS | 19c |  |
| 2306.02050 | REF-FUS-039 | ABS | 19b |  |
| 2306.04590 | REF-EVAL-055 | ABS | 19b | * |
| 2306.06599 | REF-ROB-021 | ABS | 19d |  |
| 2306.09269 | REF-CCTV-042 | ABS | 19c |  |
| 2306.09562 | REF-EVAL-048 | ABS | 19b |  |
| 2306.11885 | REF-RL-064 | ABS | 19d |  |
| 2306.16645 | REF-FUS-041 | ABS | 19b |  |
| 2307.00104 | REF-CCTV-030 | ABS | 19c |  |
| 2307.02055 | REF-ROB-109 | ABS | 19d |  |
| 2307.04223 | REF-CCTV-061 | ABS | 19c |  |
| 2307.04692 | REF-ROB-118 | ABS | 19d |  |
| 2307.04916 | REF-DATA-056 | ABS | 19c |  |
| 2307.05602 | REF-PHY-152 | ABS | 19a |  |
| 2307.07123 | REF-PHY-012 | ABS | 19a |  |
| 2307.08951 | REF-DATA-010 | ABS | 19c |  |
| 2307.14741 | REF-FUS-060 | ABS | 19b |  |
| 2307.16895 | REF-PHY-096 | ABS | 19a |  |
| 2308.02508 | REF-DATA-057 | ABS | 19c |  |
| 2308.09296 | REF-ROB-040 | ABS | 19d |  |
| 2309.01909 | REF-RL-057 | ABS | 19d |  |
| 2309.02615 | REF-PHY-071 | ABS | 19a |  |
| 2309.06062 | REF-DATA-015 | ABS | 19c |  |
| 2309.13207 | REF-ROB-017 | ABS | 19d |  |
| 2309.15529 | REF-PHY-101 | ABS | 19a |  |
| 2310.01711 | REF-DATA-053 | ABS | 19c |  |
| 2310.03220 | REF-ROB-009 | ABS | 19d |  |
| 2310.03545 | REF-FUS-011 | ABS | 19b |  |
| 2310.03986 | REF-FUS-009 | ABS | 19b | * |
| 2310.04288 | REF-RL-020 | ABS | 19d |  |
| 2310.04428 | REF-PHY-014 | ABS | 19a |  |
| 2310.05330 | REF-CCTV-006 | ABS | 19c |  |
| 2310.06224 | REF-RL-030 | ABS | 19d |  |
| 2310.17432 | REF-ROB-041 | ABS | 19d |  |
| 2310.18018 | REF-EVAL-049 | ABS | 19b |  |
| 2310.18118 | REF-ALERT-062 | ABS | 19d |  |
| 2310.18653 | REF-DATA-018 | ABS | 19c |  |
| 2311.01743 | REF-ALERT-002 | ABS | 19d |  |
| 2311.03393 | REF-ROB-102 | ABS | 19d |  |
| 2311.05168 | REF-CCTV-062 | ABS | 19c |  |
| 2311.09276 | REF-DATA-061 | ABS | 19c |  |
| 2311.10116 | REF-DATA-049 | ABS | 19c |  |
| 2311.10228 | REF-EVAL-016 | ABS | 19b |  |
| 2311.11235 | REF-ROB-077 | ABS | 19d |  |
| 2311.11491 | REF-EVAL-003 | ABS | 19b |  |
| 2311.12056 | REF-DATA-060 | ABS | 19c |  |
| 2311.15654 | REF-ROB-037 | ABS | 19d |  |
| 2311.18206 | REF-RL-006 | ABS | 19d |  |
| 2312.01530 | REF-ROB-052 | ABS | 19d |  |
| 2312.03998 | REF-DATA-026 | ABS | 19c |  |
| 2312.06461 | REF-CCTV-009 | ABS | 19c |  |
| 2312.08387 | REF-ALERT-010 | ABS | 19d |  |
| 2312.15218 | REF-ROB-007 | ABS | 19d |  |
| 2401.04824 | REF-DATA-023 | ABS | 19c |  |
| 2401.06229 | REF-CCTV-014 | ABS | 19c |  |
| 2401.07782 | REF-DATA-020 | ABS | 19c |  |
| 2401.08105 | REF-CCTV-068 | ABS | 19c |  |
| 2401.08874 | REF-PHY-120 | ABS | 19a |  |
| 2401.11519 | REF-DATA-055 | ABS | 19c |  |
| 2401.13695 | REF-PHY-030 | ABS | 19a | * |
| 2401.13697 | REF-FUS-008 | ABS | 19b |  |
| 2401.13744 | REF-ALERT-058 | ABS | 19d |  |
| 2401.13877 | REF-PHY-005 | ABS | 19a |  |
| 2402.00816 | REF-RL-008 | ABS | 19d |  |
| 2402.01379 | REF-FUS-022 | ABS | 19b |  |
| 2402.02781 | REF-CCTV-003 | ABS | 19c |  |
| 2402.04290 | REF-DATA-004 | ABS | 19c |  |
| 2402.05349 | REF-CCTV-025 | ABS | 19c |  |
| 2402.07307 | REF-ROB-132 | ABS | 19d |  |
| 2402.09056 | REF-ROB-034 | ABS | 19d |  |
| 2403.02558 | REF-EVAL-046 | ABS | 19b |  |
| 2403.05732 | REF-RL-012 | ABS | 19d |  |
| 2403.10127 | REF-DATA-062 | ABS | 19c |  |
| 2403.15378 | REF-CCTV-040 | ABS | 19c |  |
| 2403.20280 | REF-FUS-042 | ABS | 19b |  |
| 2404.02572 | REF-ROB-125 | ABS | 19d |  |
| 2404.03539 | REF-CCTV-054 | ABS | 19c |  |
| 2404.11439 | REF-PHY-063 | FT | 19a |  |
| 2404.13503 | REF-EVAL-056 | ABS | 19b |  |
| 2404.15018 | REF-ROB-133 | ABS | 19d |  |
| 2404.15860 | REF-PHY-031 | ABS | 19a | * |
| 2405.06479 | REF-FUS-010 | ABS | 19b |  |
| 2405.11533 | REF-EVAL-013 | ABS | 19b |  |
| 2405.12096 | REF-ROB-076 | ABS | 19d |  |
| 2405.13997 | REF-FUS-051 | ABS | 19b |  |
| 2405.14506 | REF-CCTV-063 | ABS | 19c |  |
| 2405.18929 | REF-ROB-015 | ABS | 19d |  |
| 2406.02438 | REF-DATA-082 | ABS | 19c |  |
| 2406.04745 | REF-EVAL-014 | ABS | 19b |  |
| 2406.05405 | REF-FUS-013 | ABS | 19b |  |
| 2406.08112 | REF-DATA-083 | ABS | 19c |  |
| 2406.08589 | REF-PHY-117 | ABS | 19a |  |
| 2406.09262 | REF-ROB-011 | ABS | 19d |  |
| 2406.15664 | REF-FUS-044 | ABS | 19b |  |
| 2406.16236 | REF-PINN-001 | ABS | 19a |  |
| 2406.16917 | REF-PHY-062 | ABS | 19a |  |
| 2406.17488 | REF-ALERT-061 | ABS | 19d |  |
| 2406.17813 | REF-ROB-139 | ABS | 19d |  |
| 2406.18326 | REF-EVAL-050 | ABS | 19b |  |
| 2406.18327 | REF-FUS-058 | ABS | 19b |  |
| 2407.06785 | REF-PINN-005 | ABS | 19a |  |
| 2407.09117 | REF-ALERT-046 | ABS | 19d |  |
| 2407.19845 | REF-ROB-115 | ABS | 19d |  |
| 2408.02841 | REF-PHY-107 | ABS | 19a |  |
| 2408.06205 | REF-PHY-121 | ABS | 19a |  |
| 2408.06629 | REF-DATA-070 | ABS | 19c |  |
| 2408.10843 | REF-CCTV-029 | ABS | 19c |  |
| 2408.13123 | REF-FUS-056 | ABS | 19b |  |
| 2409.04641 | REF-RL-021 | ABS | 19d |  |
| 2409.12635 | REF-PHY-057 | ABS | 19a |  |
| 2409.13053 | REF-ROB-079 | ABS | 19d |  |
| 2409.20408 | REF-ALERT-018 | ABS | 19d |  |
| 2410.02935 | REF-FUS-053 | ABS | 19b |  |
| 2410.04833 | REF-FUS-025 | ABS | 19b |  |
| 2410.06743 | REF-ALERT-066 | ABS | 19d |  |
| 2410.08814 | REF-DATA-076 | ABS | 19c |  |
| 2410.09570 | REF-PHY-092 | ABS | 19a |  |
| 2410.10397 | REF-FUS-015 | ABS | 19b |  |
| 2410.11711 | REF-RL-056 | ABS | 19d |  |
| 2410.16186 | REF-EVAL-051 | ABS | 19b |  |
| 2410.16631 | REF-CCTV-034 | ABS | 19c |  |
| 2410.20707 | REF-EVAL-007 | ABS | 19b |  |
| 2411.04153 | REF-PHY-028 | ABS | 19a |  |
| 2411.13275 | REF-PHY-134 | ABS | 19a |  |
| 2411.13496 | REF-ROB-010 | ABS | 19d |  |
| 2411.15204 | REF-ROB-004 | ABS | 19d |  |
| 2411.16162 | REF-ROB-110 | ABS | 19d |  |
| 2412.00264 | REF-ROB-006 | ABS | 19d |  |
| 2412.01215 | REF-FUS-055 | ABS | 19b |  |
| 2412.01609 | REF-ALERT-056 | ABS | 19d |  |
| 2412.02723 | REF-PHY-081 | ABS | 19a |  |
| 2412.05777 | REF-EVAL-019 | ABS | 19b |  |
| 2412.05994 | REF-PHY-076 | ABS | 19a |  |
| 2412.09289 | REF-ALERT-050 | ABS | 19d |  |
| 2412.09921 | REF-ROB-128 | ABS | 19d |  |
| 2412.10792 | REF-ROB-044 | ABS | 19d |  |
| 2412.13935 | REF-DATA-068 | ABS | 19c |  |
| 2412.14318 | REF-PHY-002 | ABS | 19a |  |
| 2412.18298 | REF-CCTV-007 | ABS | 19c |  |
| 2412.18931 | REF-PHY-122 | ABS | 19a |  |
| 2412.20006 | REF-CCTV-037 | ABS | 19c |  |
| 2501.06007 | REF-ALERT-063 | ABS | 19d |  |
| 2501.07915 | REF-FUS-061 | ABS | 19b |  |
| 2501.08343 | REF-PHY-111 | ABS | 19a |  |
| 2501.08639 | REF-CCTV-069 | ABS | 19c |  |
| 2501.10089 | REF-PHY-100 | ABS | 19a |  |
| 2501.11372 | REF-PINN-004 | ABS | 19a |  |
| 2501.11413 | REF-ROB-136 | ABS | 19d |  |
| 2501.12749 | REF-ROB-131 | ABS | 19d |  |
| 2501.15196 | REF-ROB-039 | ABS | 19d |  |
| 2501.16404 | REF-CCTV-045 | ABS | 19c |  |
| 2501.17281 | REF-PINN-013 | ABS | 19a |  |
| 2501.19047 | REF-EVAL-054 | ABS | 19b |  |
| 2502.01307 | REF-RL-016 | ABS | 19d |  |
| 2502.05709 | REF-FUS-021 | ABS | 19b |  |
| 2502.07596 | REF-ALERT-073 | ABS | 19d |  |
| 2502.11500 | REF-DATA-069 | ABS | 19c |  |
| 2502.15901 | REF-ROB-001 | ABS | 19d |  |
| 2502.17259 | REF-EVAL-052 | ABS | 19b |  |
| 2502.17701 | REF-EVAL-021 | ABS | 19b |  |
| 2502.18050 | REF-PHY-094 | ABS | 19a |  |
| 2502.18738 | REF-PINN-010 | ABS | 19a |  |
| 2502.19866 | REF-DATA-042 | ABS | 19c |  |
| 2502.20979 | REF-CCTV-056 | ABS | 19c |  |
| 2503.03213 | REF-FUS-050 | ABS | 19b |  |
| 2503.07371 | REF-CCTV-065 | ABS | 19c |  |
| 2503.08580 | REF-DATA-054 | ABS | 19c |  |
| 2503.09947 | REF-ROB-014 | ABS | 19d |  |
| 2503.09960 | REF-CCTV-071 | ABS | 19c |  |
| 2503.11729 | REF-PHY-150 | ABS | 19a |  |
| 2503.12905 | REF-CCTV-010 | ABS | 19c |  |
| 2503.14621 | REF-EVAL-008 | ABS | 19b |  |
| 2504.12580 | REF-PHY-138 | ABS | 19a |  |
| 2504.13231 | REF-CCTV-049 | ABS | 19c |  |
| 2504.17719 | REF-ROB-008 | ABS | 19d |  |
| 2504.17900 | REF-PHY-151 | ABS | 19a |  |
| 2505.06638 | REF-PHY-115 | ABS | 19a |  |
| 2505.08553 | REF-PHY-006 | ABS | 19a |  |
| 2505.10949 | REF-PHY-077 | ABS | 19a |  |
| 2505.14510 | REF-EVAL-012 | ABS | 19b |  |
| 2505.16793 | REF-DATA-022 | ABS | 19c |  |
| 2505.17395 | REF-DATA-052 | ABS | 19c |  |
| 2505.17501 | REF-FUS-019 | ABS | 19b |  |
| 2505.17662 | REF-ROB-103 | ABS | 19d |  |
| 2505.17782 | REF-DATA-044 | ABS | 19c |  |
| 2505.19190 | REF-FUS-026 | ABS | 19b |  |
| 2505.21857 | REF-FUS-046 | ABS | 19b |  |
| 2505.22535 | REF-DATA-014 | ABS | 19c |  |
| 2505.23190 | REF-PINN-019 | ABS | 19a |  |
| 2506.00505 | REF-RL-011 | ABS | 19d |  |
| 2506.01755 | REF-RL-052 | ABS | 19d |  |
| 2506.09186 | REF-ALERT-059 | ABS | 19d |  |
| 2506.09300 | REF-CCTV-067 | ABS | 19c |  |
| 2506.10404 | REF-PHY-155 | ABS | 19a |  |
| 2506.15891 | REF-PHY-135 | ABS | 19a |  |
| 2506.23183 | REF-FUS-069 | ABS | 19b |  |
| 2507.07527 | REF-DATA-013 | ABS | 19c |  |
| 2507.07841 | REF-ALERT-011 | ABS | 19d | * |
| 2507.08677 | REF-ALERT-016 | ABS | 19d |  |
| 2507.15021 | REF-PINN-003 | ABS | 19a | * |
| 2507.15614 | REF-DATA-038 | FT | 19c |  |
| 2507.17071 | REF-EVAL-036 | ABS | 19b |  |
| 2507.20102 | REF-CCTV-008 | ABS | 19c |  |
| 2507.21649 | REF-CCTV-017 | FT-PARTIAL | 19c | * |
| 2507.23342 | REF-ALERT-035 | ABS | 19d |  |
| 2507.23603 | REF-RL-009 | ABS | 19d |  |
| 2508.01426 | REF-PHY-032 | ABS | 19a |  |
| 2508.02724 | REF-ALERT-044 | ABS | 19d |  |
| 2508.08075 | REF-PHY-089 | ABS | 19a |  |
| 2508.11696 | REF-CCTV-035 | ABS | 19c |  |
| 2508.14203 | REF-CCTV-016 | FT-PARTIAL | 19c | * |
| 2508.14597 | REF-PHY-058 | ABS | 19a |  |
| 2508.15058 | REF-ALERT-001 | ABS | 19d |  |
| 2508.16739 | REF-CCTV-057 | ABS | 19c |  |
| 2508.18045 | REF-ROB-024 | ABS | 19d |  |
| 2509.00072 | REF-EVAL-053 | ABS | 19b |  |
| 2509.03315 | REF-FUS-004 | ABS | 19b |  |
| 2509.03347 | REF-PHY-137 | ABS | 19a |  |
| 2509.04345 | REF-DATA-084 | ABS | 19c |  |
| 2509.08094 | REF-PINN-016 | ABS | 19a |  |
| 2509.10348 | REF-FUS-028 | ABS | 19b |  |
| 2509.10362 | REF-PHY-017 | ABS | 19a | * |
| 2509.11789 | REF-EVAL-005 | ABS | 19b |  |
| 2509.12701 | REF-CCTV-032 | ABS | 19c |  |
| 2509.13106 | REF-PHY-127 | ABS | 19a |  |
| 2509.17942 | REF-DATA-005 | ABS | 19c |  |
| 2509.18176 | REF-DATA-009 | ABS | 19c | * |
| 2509.19972 | REF-RL-035 | ABS | 19d |  |
| 2509.22544 | REF-ROB-107 | ABS | 19d |  |
| 2509.23125 | REF-ALERT-057 | ABS | 19d |  |
| 2509.23240 | REF-ROB-020 | ABS | 19d |  |
| 2509.25452 | REF-PHY-091 | ABS | 19a |  |
| 2510.02270 | REF-CCTV-041 | ABS | 19c |  |
| 2510.03714 | REF-ALERT-039 | ABS | 19d |  |
| 2510.05646 | REF-ALERT-043 | ABS | 19d |  |
| 2510.08488 | REF-PHY-003 | ABS | 19a |  |
| 2510.09452 | REF-ROB-043 | ABS | 19d |  |
| 2510.09708 | REF-PHY-070 | ABS | 19a |  |
| 2510.10108 | REF-CCTV-027 | ABS | 19c |  |
| 2510.10546 | REF-PHY-009 | ABS | 19a | * |
| 2510.10799 | REF-ROB-026 | ABS | 19d |  |
| 2510.11171 | REF-FUS-057 | ABS | 19b |  |
| 2510.12328 | REF-PHY-052 | ABS | 19a |  |
| 2510.13012 | REF-PHY-035 | ABS | 19a |  |
| 2510.13189 | REF-PHY-114 | ABS | 19a |  |
| 2510.13196 | REF-PHY-112 | ABS | 19a |  |
| 2510.14423 | REF-PHY-113 | ABS | 19a |  |
| 2510.15602 | REF-CCTV-044 | ABS | 19c |  |
| 2510.15954 | REF-PHY-146 | ABS | 19a |  |
| 2510.17014 | REF-DATA-012 | ABS | 19c |  |
| 2510.22016 | REF-EVAL-028 | FT-PARTIAL | 19b |  |
| 2510.22054 | REF-FUS-045 | ABS | 19b |  |
| 2510.25573 | REF-ROB-134 | ABS | 19d |  |
| 2511.00348 | REF-RL-031 | ABS | 19d |  |
| 2511.04362 | REF-DATA-028 | ABS | 19c |  |
| 2511.05471 | REF-DATA-032 | FT-PARTIAL | 19c | * |
| 2511.11567 | REF-FUS-014 | ABS | 19b |  |
| 2511.15710 | REF-ALERT-071 | ABS | 19d |  |
| 2511.15838 | REF-FUS-035 | FT-PARTIAL | 19b | * |
| 2511.16924 | REF-FUS-049 | ABS | 19b |  |
| 2511.18243 | REF-RL-061 | ABS | 19d |  |
| 2511.18739 | REF-ROB-078 | ABS | 19d |  |
| 2511.19810 | REF-EVAL-038 | ABS | 19b |  |
| 2511.20936 | REF-DATA-031 | FT-PARTIAL | 19c | * |
| 2511.21364 | REF-EVAL-024 | FT-PARTIAL | 19b | * |
| 2511.21531 | REF-RL-018 | ABS | 19d |  |
| 2512.00161 | REF-ALERT-036 | ABS | 19d |  |
| 2512.01384 | REF-FUS-007 | ABS | 19b |  |
| 2512.01750 | REF-FUS-023 | ABS | 19b |  |
| 2512.01788 | REF-CCTV-033 | ABS | 19c |  |
| 2512.02055 | REF-DATA-041 | ABS | 19c |  |
| 2512.02520 | REF-CCTV-043 | ABS | 19c |  |
| 2512.03257 | REF-PHY-059 | ABS | 19a |  |
| 2512.05140 | REF-ROB-029 | ABS | 19d |  |
| 2512.09251 | REF-PHY-037 | ABS | 19a |  |
| 2512.11215 | REF-CCTV-036 | ABS | 19c |  |
| 2512.12183 | REF-PHY-004 | ABS | 19a |  |
| 2512.12199 | REF-PHY-060 | ABS | 19a |  |
| 2512.12268 | REF-CCTV-046 | ABS | 19c |  |
| 2512.12844 | REF-FUS-006 | ABS | 19b |  |
| 2512.12997 | REF-CCTV-053 | ABS | 19c |  |
| 2512.14221 | REF-PHY-051 | FT-PARTIAL | 19a |  |
| 2512.14683 | REF-EVAL-010 | ABS | 19b |  |
| 2512.23964 | REF-PHY-007 | ABS | 19a |  |
| 2512.24117 | REF-PHY-047 | FT-PARTIAL | 19a | * |
| 2512.24622 | REF-CCTV-066 | ABS | 19c |  |
| 2601.00109 | REF-ALERT-032 | ABS | 19d |  |
| 2601.00123 | REF-DATA-058 | ABS | 19c |  |
| 2601.00148 | REF-ALERT-033 | ABS | 19d |  |
| 2601.01008 | REF-PHY-095 | ABS | 19a |  |
| 2601.02264 | REF-DATA-071 | ABS | 19c |  |
| 2601.03425 | REF-FUS-002 | ABS | 19b |  |
| 2601.03569 | REF-PHY-078 | ABS | 19a |  |
| 2601.03867 | REF-ALERT-053 | ABS | 19d |  |
| 2601.05152 | REF-RL-014 | ABS | 19d |  |
| 2601.06664 | REF-EVAL-022 | ABS | 19b |  |
| 2601.12330 | REF-PHY-080 | ABS | 19a |  |
| 2601.13839 | REF-DATA-077 | ABS | 19c |  |
| 2601.18135 | REF-ROB-105 | ABS | 19d |  |
| 2601.18509 | REF-ROB-032 | ABS | 19d |  |
| 2601.21293 | REF-ROB-091 | ABS | 19d |  |
| 2602.01266 | REF-RL-071 | ABS | 19d |  |
| 2602.04904 | REF-FUS-018 | ABS | 19b |  |
| 2602.07252 | REF-ROB-031 | ABS | 19d |  |
| 2602.08112 | REF-DATA-064 | ABS | 19c |  |
| 2602.11194 | REF-PHY-036 | ABS | 19a |  |
| 2602.14676 | REF-EVAL-020 | ABS | 19b | * |
| 2602.19265 | REF-PHY-074 | ABS | 19a |  |
| 2602.20729 | REF-RL-004 | ABS | 19d |  |
| 2602.24209 | REF-ALERT-012 | ABS | 19d |  |
| 2603.00604 | REF-EVAL-031 | ABS | 19b |  |
| 2603.01511 | REF-FUS-024 | ABS | 19b |  |
| 2603.02105 | REF-ALERT-031 | ABS | 19d |  |
| 2603.02465 | REF-CCTV-038 | ABS | 19c |  |
| 2603.10392 | REF-FUS-005 | ABS | 19b |  |
| 2603.11365 | REF-ROB-117 | ABS | 19d |  |
| 2603.12916 | REF-ROB-097 | ABS | 19d |  |
| 2603.15945 | REF-ALERT-008 | ABS | 19d |  |
| 2603.16768 | REF-FUS-062 | ABS | 19b |  |
| 2603.17319 | REF-FUS-031 | FT-PARTIAL | 19b | * |
| 2603.18985 | REF-ROB-074 | ABS | 19d |  |
| 2603.23853 | REF-FUS-063 | ABS | 19b |  |
| 2603.24241 | REF-RL-063 | ABS | 19d |  |
| 2603.25423 | REF-DF-017 | ABS | 19c |  |
| 2603.26415 | REF-ROB-137 | ABS | 19d |  |
| 2603.26816 | REF-RL-059 | ABS | 19d |  |
| 2603.26975 | REF-PHY-148 | ABS | 19a |  |
| 2604.00801 | REF-FUS-001 | ABS | 19b |  |
| 2604.01830 | REF-RL-060 | ABS | 19d |  |
| 2604.02351 | REF-ALERT-086 | ABS | 19d |  |
| 2604.04265 | REF-EVAL-002 | ABS | 19b |  |
| 2604.06387 | REF-ROB-018 | ABS | 19d |  |
| 2604.08581 | REF-CCTV-015 | ABS | 19c |  |
| 2604.16265 | REF-DATA-033 | FT-PARTIAL | 19c | * |
| 2604.16663 | REF-PHY-056 | ABS | 19a |  |
| 2604.20551 | REF-FUS-016 | ABS | 19b |  |
| 2604.21527 | REF-EVAL-037 | ABS | 19b |  |
| 2604.22787 | REF-ROB-138 | ABS | 19d |  |
| 2604.23012 | REF-ALERT-051 | ABS | 19d |  |
| 2604.23066 | REF-DATA-040 | ABS | 19c |  |
| 2604.23542 | REF-DATA-051 | ABS | 19c |  |
| 2604.23576 | REF-RL-015 | ABS | 19d |  |
| 2604.24404 | REF-RL-022 | FT-PARTIAL | 19d | * |
| 2604.27178 | REF-CCTV-004 | ABS | 19c |  |
| 2605.01165 | REF-CCTV-048 | ABS | 19c |  |
| 2605.01679 | REF-PHY-044 | FT-PARTIAL | 19a | * |
| 2605.02153 | REF-PHY-027 | ABS | 19a |  |
| 2605.06643 | REF-ROB-067 | FT-PARTIAL | 19d | * |
| 2605.08198 | REF-EVAL-011 | ABS | 19b |  |
| 2605.11348 | REF-EVAL-006 | ABS | 19b |  |
| 2605.12517 | REF-PHY-102 | ABS | 19a |  |
| 2605.13642 | REF-ROB-092 | ABS | 19d |  |
| 2605.14365 | REF-EVAL-029 | FT-PARTIAL | 19b |  |
| 2605.14645 | REF-CCTV-012 | ABS | 19c |  |
| 2605.15894 | REF-ROB-061 | FT-PARTIAL | 19d | * |
| 2605.16375 | REF-ALERT-072 | ABS | 19d |  |
| 2605.17063 | REF-ALERT-038 | ABS | 19d |  |
| 2605.17353 | REF-ALERT-075 | ABS | 19d |  |
| 2605.17419 | REF-PHY-029 | ABS | 19a | * |
| 2605.19793 | REF-RL-033 | ABS | 19d |  |
| 2605.20167 | REF-PHY-039 | FT-PARTIAL | 19a | * |
| 2605.20379 | REF-ALERT-037 | ABS | 19d |  |
| 2605.21527 | REF-DATA-045 | ABS | 19c |  |
| 2605.21742 | REF-ROB-050 | ABS | 19d |  |
| 2605.23504 | REF-CCTV-023 | FT-PARTIAL | 19c | * |
| 2605.23971 | REF-PHY-153 | ABS | 19a |  |
| 2605.26159 | REF-RL-032 | ABS | 19d |  |
| 2605.26320 | REF-DATA-072 | ABS | 19c |  |
| 2605.28174 | REF-EVAL-032 | ABS | 19b |  |
| 2605.31155 | REF-ROB-002 | ABS | 19d |  |
| 2606.00690 | REF-ROB-066 | FT-PARTIAL | 19d | * |
| 2606.02256 | REF-ROB-089 | ABS | 19d |  |
| 2606.04143 | REF-PHY-008 | ABS | 19a |  |
| 2606.04634 | REF-RL-025 | FT-PARTIAL | 19d | * |
| 2606.06347 | REF-ROB-087 | ABS | 19d |  |
| 2606.07374 | REF-DATA-046 | ABS | 19c |  |
| 2606.07593 | REF-ROB-060 | FT-PARTIAL | 19d | * |
| 2606.07613 | REF-DF-014 | ABS | 19c |  |
| 2606.09874 | REF-ROB-094 | ABS | 19d |  |
| 2606.10174 | REF-DATA-050 | ABS | 19c |  |
| 2606.11676 | REF-PHY-069 | ABS | 19a |  |
| 2606.13754 | REF-ROB-104 | ABS | 19d |  |
| 2606.13780 | REF-ROB-100 | ABS | 19d |  |
| 2606.13896 | REF-DATA-029 | FT-PARTIAL | 19c | * |
| 2606.15514 | REF-RL-069 | ABS | 19d |  |
| 2606.16302 | REF-DATA-043 | ABS | 19c |  |
| 2606.16795 | REF-DATA-001 | ABS | 19c | * |
| 2606.16795-RESTUDY | REF-DATA-035 | FT-PARTIAL | 19c |  |
| 2606.20055 | REF-ROB-084 | ABS | 19d |  |
| 2606.20216 | REF-ROB-048 | ABS | 19d |  |
| 2606.21773 | REF-PHY-050 | FT-PARTIAL | 19a |  |
| 2606.29134 | REF-PHY-011 | ABS | 19a |  |
| 2606.30320 | REF-ALERT-023 | ABS | 19d |  |
| 2607.03125 | REF-RL-062 | ABS | 19d |  |
| 2607.03131 | REF-CCTV-064 | ABS | 19c |  |
| 2607.07951 | REF-CCTV-051 | ABS | 19c |  |
| 2607.11969 | REF-ROB-073 | ABS | 19d |  |
| 2607.12454 | REF-ROB-095 | ABS | 19d |  |
| 2607.16080 | REF-PHY-088 | ABS | 19a |  |
| 2607.16218 | REF-ALERT-064 | ABS | 19d |  |
| 2607.16264 | REF-DATA-025 | ABS | 19c |  |
| 2607.18544 | REF-PHY-154 | ABS | 19a |  |
| 2607.21200 | REF-PHY-087 | ABS | 19a |  |
| 2607.22667 | REF-RL-065 | ABS | 19d |  |
| 2607.23220 | REF-ALERT-052 | ABS | 19d |  |
| 2607.23237 | REF-PHY-086 | ABS | 19a |  |
| 2607.24683 | REF-ROB-068 | FT-PARTIAL | 19d | * |
| 2607.25842 | REF-ROB-129 | ABS | 19d |  |
| 2607.26191 | REF-EVAL-057 | ABS | 19b |  |
| 2607.26854 | REF-PHY-048 | FT-PARTIAL | 19a | * |
| 2607.27584 | REF-ALERT-025 | ABS | 19d |  |
| 2607.28248 | REF-ROB-062 | FT-PARTIAL | 19d | * |
| 2608.00409 | REF-RL-034 | ABS | 19d |  |
| 2608.02315 | REF-DATA-039 | FT-PARTIAL | 19c |  |
| 2608.03926 | REF-ROB-083 | ABS | 19d |  |
| 2608.04225 | REF-EVAL-017 | ABS | 19b |  |
| 2608.04501 | REF-ALERT-082 | ABS | 19d |  |
| 2608.06876 | REF-PHY-042 | FT-PARTIAL | 19a | * |
| 2608.08158 | REF-RL-027 | FT-PARTIAL | 19d |  |
| 2608.08528 | REF-ALERT-084 | ABS | 19d |  |
| 2608.09325 | REF-DATA-063 | ABS | 19c |  |
| 2608.11142 | REF-DATA-037 | FT-PARTIAL | 19c | * |
| 2608.12223 | REF-PHY-116 | ABS | 19a |  |
| 2608.12422 | REF-PHY-010 | ABS | 19a | * |
| 2608.12422-RESTUDY | REF-PINN-007 | FT-PARTIAL | 19a |  |
| 2608.14089 | REF-ROB-081 | ABS | 19d |  |
| 2608.14391 | REF-ROB-070 | FT-PARTIAL | 19d |  |
| 2608.15261 | REF-PHY-054 | FT-PARTIAL | 19a |  |
| 2608.15727 | REF-ROB-085 | ABS | 19d |  |
| 2608.16654 | REF-ROB-064 | FT-PARTIAL | 19d | * |
| 2608.19212 | REF-DF-016 | ABS | 19c |  |
| 2608.19816 | REF-ALERT-081 | ABS | 19d |  |
| 2608.19836 | REF-FUS-033 | FT-PARTIAL | 19b | * |
| 2608.20663 | REF-ROB-082 | ABS | 19d |  |
| 2608.20864 | REF-ALERT-080 | ABS | 19d |  |
| 2608.21646 | REF-EVAL-033 | ABS | 19b |  |
| 2608.21854 | REF-ROB-075 | ABS | 19d |  |
| 2608.22293 | REF-ALERT-068 | ABS | 19d |  |
| 2608.23192 | REF-PHY-061 | FT-PARTIAL | 19a |  |
| 2608.24288 | REF-ROB-013 | ABS | 19d |  |
| 2608.25646 | REF-EVAL-035 | ABS | 19b |  |
| 2608.29235 | REF-FUS-054 | ABS | 19b |  |
| 2608.29463 | REF-EVAL-045 | ABS | 19b |  |
| 2608.30205 | REF-FUS-036 | FT-PARTIAL | 19b | * |
| 2608.30392 | REF-DATA-021 | ABS | 19c |  |
| 2609.04988 | REF-PHY-108 | ABS | 19a |  |
| 2609.05066 | REF-CCTV-020 | FT-PARTIAL | 19c | * |
| 2609.07369 | REF-DF-005 | ABS | 19c |  |
| 2609.07403 | REF-ALERT-083 | ABS | 19d |  |
| 2609.07455 | REF-CCTV-019 | FT-PARTIAL | 19c | * |
| 2609.09773 | REF-PHY-123 | ABS | 19a |  |
| 2609.11829 | REF-ALERT-067 | ABS | 19d |  |
| 2609.13171 | REF-PINN-014 | ABS | 19a |  |
| 2609.13552 | REF-ALERT-079 | ABS | 19d |  |
| 2609.14234 | REF-ROB-099 | ABS | 19d |  |
| 2609.14821 | REF-PHY-049 | FT-PARTIAL | 19a | * |
| 2609.15297 | REF-FUS-034 | FT-PARTIAL | 19b | * |
| 2609.15562 | REF-DF-019 | ABS | 19c |  |
| 2609.16314 | REF-ROB-098 | ABS | 19d |  |
| 2609.16707 | REF-PHY-055 | FT | 19a |  |
| 2609.16964 | REF-ROB-072 | ABS | 19d |  |
| 2609.17175 | REF-PHY-038 | FT-PARTIAL | 19a | * |
| 2609.18227 | REF-CCTV-028 | ABS | 19c |  |
| 2609.18555 | REF-PHY-041 | FT-PARTIAL | 19a | * |
| 2609.20441 | REF-CCTV-018 | FT-PARTIAL | 19c | * |
| 2609.21217 | REF-ROB-088 | ABS | 19d |  |
| 2609.27202 | REF-PHY-043 | FT-PARTIAL | 19a | * |
| 2609.29580 | REF-ROB-093 | ABS | 19d |  |
| 2609.30272 | REF-EVAL-034 | ABS | 19b |  |
| 2609.31142 | REF-ROB-065 | FT-PARTIAL | 19d | * |
| 2609.32971 | REF-PHY-085 | ABS | 19a |  |
| 2609.33441 | REF-DF-015 | ABS | 19c |  |
| 2609.33585 | REF-DF-002 | ABS | 19c |  |
| 2609.34003 | REF-DF-012 | ABS | 19c |  |
| 2609.34804 | REF-ROB-086 | ABS | 19d |  |
| 2609.34836 | REF-DATA-034 | FT-PARTIAL | 19c | * |
| 2609.36315 | REF-RL-036 | ABS | 19d |  |
| 2609.36850 | REF-DF-018 | ABS | 19c |  |
| 2609.37038 | REF-DATA-003 | ABS | 19c |  |
| 2609.37487 | REF-RL-028 | ABS | 19d |  |
| 2609.38196 | REF-PHY-097 | ABS | 19a |  |
| 2609.38552 | REF-EVAL-026 | FT-PARTIAL | 19b | * |
| 2609.38655 | REF-FUS-032 | FT-PARTIAL | 19b | * |
| 2609.38936 | REF-FUS-030 | FT-PARTIAL | 19b | * |
| 2609.39066 | REF-DF-001 | ABS | 19c |  |
| 2609.39215 | REF-ROB-080 | ABS | 19d |  |
| 2609.39337 | REF-DATA-030 | FT-PARTIAL | 19c | * |
| 2610.00363 | REF-CCTV-022 | FT-PARTIAL | 19c | * |
| 2610.01384 | REF-ROB-069 | FT-PARTIAL | 19d |  |
| 2610.01994 | REF-ROB-058 | FT-PARTIAL | 19d | * |
| 2610.02010 | REF-DF-011 | ABS | 19c |  |
| 2610.02345 | REF-ROB-096 | ABS | 19d |  |
| 2610.02777 | REF-FUS-029 | FT-PARTIAL | 19b | * |
| 2610.03369 | REF-ROB-063 | FT-PARTIAL | 19d | * |
| 2610.03380 | REF-RL-023 | FT-PARTIAL | 19d | * |
| 2610.03649 | REF-ROB-071 | FT | 19d |  |
| 2610.03724 | REF-ALERT-069 | ABS | 19d |  |
| 2610.04084 | REF-ALERT-078 | ABS | 19d |  |
| 2610.04151 | REF-DF-013 | ABS | 19c | * |
| 2610.04392 | REF-ROB-059 | FT-PARTIAL | 19d | * |
| 2610.04828 | REF-PINN-006 | FT-PARTIAL | 19a | * |
| 2610.05790 | REF-EVAL-030 | FT-PARTIAL | 19b |  |
| 2610.05819 | REF-RL-051 | ABS | 19d |  |
| 2610.05961 | REF-RL-044 | ABS | 19d |  |
| 2610.06241 | REF-PHY-040 | FT-PARTIAL | 19a | * |
| 2610.06317 | REF-RL-024 | FT-PARTIAL | 19d | * |
| 2610.06339 | REF-DF-008 | ABS | 19c |  |
| 2610.06453 | REF-CCTV-021 | FT-PARTIAL | 19c | * |
| 2610.07216 | REF-DF-007 | ABS | 19c |  |
| 2610.07232 | REF-PHY-053 | FT-PARTIAL | 19a |  |
| 2610.07431 | REF-RL-037 | ABS | 19d |  |
| 2610.07686 | REF-RL-050 | ABS | 19d |  |
| 2610.07899 | REF-RL-048 | ABS | 19d |  |
| 2610.07939 | REF-DF-004 | ABS | 19c |  |
| 2610.08225 | REF-RL-049 | ABS | 19d |  |
| 2610.08227 | REF-EVAL-027 | FT-PARTIAL | 19b |  |
| 2610.08810 | REF-ALERT-085 | ABS | 19d |  |
| 2610.09208 | REF-ROB-135 | ABS | 19d |  |
| 2610.09438 | REF-RL-038 | ABS | 19d |  |
| 2610.10121 | REF-DF-006 | ABS | 19c |  |
| 2610.10752 | REF-DF-009 | ABS | 19c |  |
| 2610.10946 | REF-CCTV-050 | ABS | 19c |  |
| 2610.11085 | REF-RL-046 | ABS | 19d |  |
| 2610.11149 | REF-ROB-106 | ABS | 19d |  |
| 2610.11175 | REF-RL-045 | ABS | 19d |  |
| 2610.11236 | REF-DATA-047 | ABS | 19c |  |
| 2610.11281 | REF-RL-039 | ABS | 19d |  |
| 2610.11290 | REF-DF-010 | ABS | 19c |  |
| 2610.11464 | REF-RL-040 | ABS | 19d |  |
| 2610.11496 | REF-DF-003 | ABS | 19c |  |
| 2610.11739 | REF-RL-043 | ABS | 19d |  |
| 2610.12135 | REF-RL-047 | ABS | 19d |  |
| 2610.12189 | REF-RL-029 | ABS | 19d |  |
| 2610.12244 | REF-ROB-101 | ABS | 19d |  |
| 2610.12420 | REF-RL-042 | ABS | 19d |  |
| 2610.12432 | REF-RL-041 | ABS | 19d |  |

## 8. BibTeX appendix — TOP-30 ONLY
Built from the ledger metadata actually present. Fields the ledger did **not** supply are left as empty `{}` (not invented). `note` records read-depth + the not-re-fetched status. Classics are given as `@misc` from the equations-register citation strings (no arXiv/DOI available).

```bibtex
@misc{arxiv2608_12422,
  title={Which Site, and When: A Free-Satellite-Data Test of Himalayan Glacial Lake Bursts, Landslides, and Ice Floods},
  author={Kahn and  Arjel and  Adhikari and  Sherpa and  Pope},
  year={2026},
  eprint={2608.12422},
  archivePrefix={arXiv},
  howpublished={arXiv (cs.LG)},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2610_08227,
  title={How Many Independent Samples Does a Satellite Image Contain?},
  author={},
  year={2026},
  eprint={2610.08227},
  archivePrefix={arXiv},
  howpublished={IEEE TGRS 2026},
  note={read_depth=FT-PARTIAL; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2101_05397,
  title={Should Ensemble Members Be Calibrated?},
  author={},
  year={2021},
  eprint={2101.05397},
  archivePrefix={arXiv},
  howpublished={arXiv},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2303_12783,
  title={Conformal Prediction for Time Series with Modern Hopfield Networks (HopCPT)},
  author={Auer and  Gauch and  Klotz and  Hochreiter},
  year={2023},
  eprint={2303.12783},
  archivePrefix={arXiv},
  howpublished={NeurIPS 2023},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2106_08909,
  title={Offline RL Without Off-Policy Evaluation (One-Step)},
  author={Brandfonbrener and  Whitney and  Ranganath and  Bruna},
  year={2021},
  eprint={2106.08909},
  archivePrefix={arXiv},
  howpublished={NeurIPS 2021},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2110_14000,
  title={Towards Hyperparameter-free Policy Selection for Offline Reinforcement Learning},
  author={Zhang and  Jiang},
  year={2021},
  eprint={2110.14000},
  archivePrefix={arXiv},
  howpublished={NeurIPS 2021},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2311_18206,
  title={SCOPE-RL: A Python Library for Offline Reinforcement Learning and Off-Policy Evaluation},
  author={Kiyohara and  Kishimoto and  Kawakami and  Kobayashi and  Nakata and  Saito},
  year={2023},
  eprint={2311.18206},
  archivePrefix={arXiv},
  howpublished={arXiv (cs.LG) preprint},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2604_24404,
  title={Open-Source 5G Public Warning System Spoofing Testbed},
  author={},
  year={2026},
  eprint={2604.24404},
  archivePrefix={arXiv},
  howpublished={arXiv},
  note={read_depth=FT-PARTIAL; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2003_01279,
  title={Disrupting Deepfakes: Adversarial Attacks Against Facial Manipulation Systems},
  author={},
  year={2020},
  eprint={2003.01279},
  archivePrefix={arXiv},
  howpublished={arXiv},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2007_05848,
  title={Fighting Disaster Misinformation in Latin America (#Verificado19S Mexico 2017 Earthquake)},
  author={},
  year={2020},
  eprint={2007.05848},
  archivePrefix={arXiv},
  howpublished={arXiv (cs.CY/cs.SI)},
  note={read_depth=FT-PARTIAL; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2603_17319,
  title={PIER: Physics-Informed Offline RL with Decoupled Post-hoc Shield},
  author={},
  year={2026},
  eprint={2603.17319},
  archivePrefix={arXiv},
  howpublished={arXiv},
  note={read_depth=FT-PARTIAL; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2610_04828,
  title={Label-Free PINN Strength-Reduction Factor-of-Safety at Scale},
  author={},
  year={2026},
  eprint={2610.04828},
  archivePrefix={arXiv},
  howpublished={arXiv},
  note={read_depth=FT-PARTIAL; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2512_23964,
  title={DUALFloodGNN: Physics-informed Graph Neural Network for Operational Flood Modeling},
  author={Acosta and  Herath and  Lim and  Saha and  Rasnayaka and  Marshall},
  year={2026},
  eprint={2512.23964},
  archivePrefix={arXiv},
  howpublished={IJCAI-ECAI 2026},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2505_08553,
  title={Towards Digital Twin in Flood Forecasting with Data Assimilation of Satellite EO (Alzette)},
  author={Nguyen and  Bhattacharya and  Wong and  Didry and  Phan and  Tamisier and  Matgen},
  year={2025},
  eprint={2505.08553},
  archivePrefix={arXiv},
  howpublished={Remote Sensing (MDPI)},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2211_10338,
  title={Deep learning based landslide density estimation on SAR data for rapid response},
  author={Boehm and  Leong and  Bal Mahesh and  Prapas and  Nemni and  Kalaitzis and  Ganju and  Ramos-Pollan},
  year={2022},
  eprint={2211.10338},
  archivePrefix={arXiv},
  howpublished={arXiv (cs.CV)},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2512_12844,
  title={Selective Conformal Risk Control (SCRC)},
  author={},
  year={2026},
  eprint={2512.12844},
  archivePrefix={arXiv},
  howpublished={arXiv (cs.LG)},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2512_01384,
  title={CLAPS: Aleatoric-Epistemic Scaling via Last-Layer Laplace for Conformal Regression},
  author={Kim and  Choi and  Aashik Rasool and  Oh},
  year={2026},
  eprint={2512.01384},
  archivePrefix={arXiv},
  howpublished={arXiv (cs.LG)},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2603_10392,
  title={Safe Probabilistic Planning for Human-Robot Interaction using Conformal Risk Control},
  author={Gonzales and  Mizuta and  Leung and  Ratliff},
  year={2026},
  eprint={2603.10392},
  archivePrefix={arXiv},
  howpublished={arXiv (cs.RO)},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2104_11422,
  title={Socio-meteorology: flood prediction social preparedness and cry wolf effects},
  author={Sawada and  Kanai and  Kotani},
  year={2021},
  eprint={2104.11422},
  archivePrefix={arXiv},
  howpublished={arXiv (physics.geo-ph/soc-ph)},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2509_11789,
  title={Watch Your Step: Cost-Sensitive Accelerometer Fall Detection in Real-World Streaming},
  author={Aderinola and  Palmerini and  D'Ascanio and  Chiari and  Klenk and  Becker and  Caulfield and  Ifrim},
  year={2025},
  eprint={2509.11789},
  archivePrefix={arXiv},
  howpublished={arXiv (cs.LG)},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2503_14621,
  title={Reducing False Ventricular Tachycardia Alarms in ICU Settings: A Machine Learning Approach},
  author={Farayola and  Akintola and  Fagbohun and  Oforgu and  Kayode and  Chimezie and  Kadri and  Oludotun and  Ogbeide and  Michael},
  year={2025},
  eprint={2503.14621},
  archivePrefix={arXiv},
  howpublished={ICMLT 2025},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2601_05921,
  title={Decision-value / cost-loss Value Score for EWS verification (QUOTA#15)},
  author={},
  year={},
  eprint={2601.05921},
  archivePrefix={arXiv},
  note={note-only -- NOT a ledger row; grounds equations-register E-07; read_depth=FT (local note); identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2603_15945,
  title={Evaluating Opportunistic Routing Protocols in a Disaster Scenario (DTN Earthquake Case Study)},
  author={Cao and  Radenkovic},
  year={2026},
  eprint={2603.15945},
  archivePrefix={arXiv},
  howpublished={arXiv (cs.NI)},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2608_11142,
  title={SAR2Agri: Learning SAR Intensity Representations for Agricultural Monitoring},
  author={Gupta and  Sobti},
  year={2026},
  eprint={2608.11142},
  archivePrefix={arXiv},
  howpublished={arXiv (cs.CV)},
  note={read_depth=FT-PARTIAL; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2509_17942,
  title={StefaLand: An Efficient Geoscience Foundation Model Improving Dynamic Land-Surface Predictions},
  author={Kraabel and  Liu and  Bian and  Kifer and  Shen},
  year={2026},
  eprint={2509.17942},
  archivePrefix={arXiv},
  howpublished={arXiv (cs.LG)},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2306_00001,
  title={TinyissimoYOLO: Quantized Low-Memory TinyML Object Detection for Low-Power Microcontrollers},
  author={Moosmann and  Giordano and  Vogt and  Magno},
  year={2023},
  eprint={2306.00001},
  archivePrefix={arXiv},
  howpublished={IEEE AICAS 2023},
  note={read_depth=ABS; identifier not independently re-fetched 2026-10-10}
}
@misc{arxiv2610_06453,
  title={NCL: Normal-Subspace Constrained Learning for Foundation-Model Anomaly Detection},
  author={},
  year={2026},
  eprint={2610.06453},
  archivePrefix={arXiv},
  howpublished={arXiv},
  note={read_depth=FT-PARTIAL; identifier not independently re-fetched 2026-10-10}
}
@misc{iverson2000,
  title={Landslide triggering by rain infiltration},
  author={Iverson, R. M.},
  year={2000},
  note={Water Resources Research 36(7):1897-1910 (as cited in analysis/08_equations_register.md GH-02; not re-fetched)}
}
@misc{fukuzono1985,
  title={A new method for predicting the failure time of a slope},
  author={Fukuzono, T.},
  year={1985},
  note={Proc. 4th Int. Conf. and Field Workshop on Landslides (as cited in equations register E-04; not re-fetched)}
}
@misc{voight1988,
  title={A method for prediction of volcanic eruptions},
  author={Voight, B.},
  year={1988},
  note={Nature 332:125-130 (as cited in equations register E-04; not re-fetched)}
}
@misc{heskestad1983,
  title={Luminous heights of turbulent diffusion flames},
  author={Heskestad, G.},
  year={1983},
  note={Fire Safety Journal 5(2):103-108 (as cited in equations register EF-01; not re-fetched)}
}
```

---
_End of chapter 19 index. Full per-entry catalogue: 19a / 19b / 19c / 19d. Source of truth: `analysis/02_paper_ledger.csv` + `analysis/03_paper_notes/`._
