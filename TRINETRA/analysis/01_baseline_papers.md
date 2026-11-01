# BASELINE PAPERS — real enumerated index (Phase P1, Task 4)
#
# Supersedes the P0 estimate. Source: glob of `C:\Users\Dell\Downloads\trinetra\papers\**\*.pdf`
# (2026-10-05). Filenames are arXiv IDs except the named ones (lhasa*/nhess*/joshimath/chamoli).
# Local PDFs cannot be extracted by `read` (binary on read-only root); full text is read via
# the arXiv-HTML / ar5iv route by ID (D-008). Non-arXiv named PDFs need DOI/title resolution.
#
# COUNT: 128 paper PDFs on disk; 8 named non-arXiv; 7 cross-folder duplicates (listed below)
#        => ~121 UNIQUE baseline papers. These are the Phase-P1 baseline reading set.
#        They do NOT count toward the P1 quota (quota = 15 NEW papers on top).
#
# read_depth legend: ABS=abstract-only, SKIM=partial, FT=full-text(method+exp+limits).
# Status filled as each is read this phase. "ledger?" = is the ID already in 02_paper_ledger.csv.

## Cross-folder duplicate IDs (count once): 2207.08051, 2103.10939, 2212.12038,
## 2412.02732, 2608.12422, 2512.24117, 2601.12330

## A. papers/ (root, general) — 12
| arXiv ID | folder(s) | theme (provisional) | read_depth | status |
|----------|-----------|---------------------|-----------|--------|
| 1805.00713 | root | (resolve on read) | — | queued |
| 1911.09296 | root | | — | queued |
| 1912.11035 | root | | — | queued |
| 2012.02951 | root | | — | queued |
| 2104.03090 | root | | — | queued |
| 2107.07511 | root | | — | queued |
| 2202.12361 | root | | — | queued |
| 2207.08051 | root+satellite | | — | queued |
| 2302.10174 | root | | — | queued |
| 2303.09295 | root | | — | queued |
| 2304.07193 | root | (DINOv2?) | — | queued |
| 2310.18660 | root | | — | queued |

## B. papers/physics/ — 21 (WS1)
| 1305.4803 | 1306.1529 | 1805.11654 | 1806.05035 | 2007.02756 | 2103.10939(+sat) |
| 2104.11009 | 2204.06097 | 2204.07653 | 2401.13695 | 2404.15860 | 2407.06785 |
| 2407.16633 | 2411.04333 | 2507.15021 | 2509.10560 | 2511.09130 | 2512.23964 |
| 2512.24117(+sat) | 2601.12330(+sat) | 2606.04143 |

## C. papers/satellite/ — 21 (WS1/WS8; incl 8 named non-arXiv)
| 2103.10939 | 2201.06837 | 2207.08051 | 2212.12038 | 2308.11929 | 2311.01564 |
| 2404.10135 | 2412.02732 | 2508.08819 | 2510.10546 | 2512.24117 | 2601.12330 |
| 2608.12422 |
| NAMED (need DOI/title resolve): joshimath_gnhr2023 · lhasa1 · lhasa2 ·
|   lhasa2_stanley2021 · lhasa_forecast_khan · lhasa_kirschbaum2018 ·
|   nhess-22-3309-2022 · nhess2021-333_chamoli_precollapse |

## D. papers/rl/ — 21 (WS5)
| 1602.01783(A3C) | 1706.02275(MADDPG) | 1707.06347(PPO) | 1801.01290(SAC) | 1803.11485(QMIX) |
| 1909.01968 | 1911.05696 | 2002.08415 | 2004.12684 | 2005.01643(offline-RL survey) |
| 2006.04779(CQL) | 2009.07415(Meta-AAD) | 2012.03719 | 2104.00543 | 2104.04443 |
| 2106.06860(IQL?) | 2110.06169(IQL) | 2205.09884(RL-model-select) | 2302.03122 | 2405.12800 | 2409.18574 |

## E. papers/cctv_comms/ — 19 (WS4/WS3)
| 1607.04139 | 1710.11122 | 1712.09867 | 1810.09409 | 1904.02639 | 2102.06491 |
| 2108.06852 | 2210.04218 | 2410.21991 | 2412.01095 | 2412.04563 | 2503.04504 |
| 2510.16290 | 2511.18455 | 2603.11848 | 2604.24404 | 2605.17063 | 2607.15527 | 2710.11122 |

## F. papers/iot/ — 14 (WS7)
| 1103.1678 | 1312.4179 | 2010.14934 | 2106.10652 | 2107.07072 | 2112.11965 |
| 2210.03019 | 2306.12826 | 2307.04016 | 2412.08477 | 2505.24081 | 2506.20858 |
| 2509.02811 | 2601.13054 |

## G. papers/multimodal/ — 20 (WS8/fusion)
| 1906.07789 | 2105.07921 | 2206.00515 | 2211.07044 | 2211.15660 | 2212.12038 |
| 2306.03831 | 2311.00566 | 2312.10115 | 2402.12095 | 2403.15356 | 2412.02732 |
| 2412.14123 | 2501.06019 | 2502.09356 | 2503.11849 | 2504.11171 | 2511.04474 |
| 2603.15681 | 2608.12422 |

## Reading plan for P1 (per user answer #2: existing corpus to depth FIRST)
# Priority order: (1) the papers the pre-existing report leans on hardest and the ones in the
# contradiction register, (2) surveys (read early, orient the themes), (3) the rest by WS.
# Full-text via arXiv-HTML/ar5iv (D-008). Named satellite PDFs: resolve DOI/title, then read
# via publisher HTML or arXiv if a preprint exists; if neither works, mark SKIM/ABS honestly.
#
# OVERVIEW (themes, strongest papers, gaps, contradictions) is appended at the END of P1,
# after the papers are actually read — not written ahead of the reading (honesty rule 10).

---

# OVERVIEW / SYNTHESIS (P1, appended 2026-10-06 after Tier-2+ re-study of 43 baseline notes)
> Grounded ONLY in papers with a note in analysis/03_paper_notes/. Read depths: FT-PARTIAL
> (sections named in each note; ar5iv/arXiv-HTML middle sometimes pruned → tables not fully
> verified) / ABS / FETCH-DEFERRED. No claim here asserts OUR system's performance (Rule 16).
> "Strongest" = most load-bearing for TRINETRA's correctness, not most-cited.

## Coverage by cluster (notes written / cluster)
- RL & alarm policy: IQL 2110.06169, CQL 2006.04779, offline-RL survey 2005.01643, SAC
  1801.01290, TD3+BC 2106.06860, (ext) one-step 2106.08909, (ext) shielding 1708.08611,
  model-selection 2205.09884, Meta-AAD 2009.07415, ACES RL energy 1909.01968. → WELL COVERED.
- Satellite / InSAR / EO-SSL: DINOv2 2304.07193, CROMA 2311.00566, Copernicus-FM 2503.11849,
  AnySat 2412.14123, SSL4EO-S12 2211.07044, Major-TOM 2402.12095, dynamic-LSA InSAR 2308.11929,
  El-Forn InSAR 2311.01564, community-detection InSAR 2212.12038, Landslide4Sense 2206.00515,
  GTS-Forecaster 2509.10560. → WELL COVERED (4 EO-encoder contenders for CR-01).
- Physics / hydrology / runout: PIML Narmada 2104.11009, ALPINE PINN flood 2507.15021,
  dam-breach Bayesian 1806.05035, GNS inverse runout 2401.13695, FEM-MPM runout 2404.15860,
  ML slope-stability surrogate 2204.06097, FFM geodetic 2007.02756, rockfall e2e 2102.06491,
  LSTM precip-merge 2404.10135, SNN susceptibility 2201.06837. → WELL COVERED.
- Anomaly / video (WS4): HF²-VAD 2108.06852, MemAE 1904.02639. → core anchored.
- IoT / comms / energy (WS7): TinyML ESP32 2106.10652, beekeeping energy 2010.14934,
  LTE+solar 2307.04016, LoRa Nepal 2412.04563, passive-RFID 2112.11965, low-cost DGPS 2306.12826.
  → WELL COVERED.
- Conformal / calibration (WS6): conformal intro 2107.07511. → thin (expand P2/A7).
- Multi-task / fusion methodology: MTL survey 1707.08114 (ext), which-site-when 2608.12422.
- Datasets: GLOFNet 2510.10546. · Motivating event: Chamoli nhess-22-3309-2022 (FETCH-DEFERRED).

## The 6 strongest / most load-bearing baseline papers (and why)
1. **2608.12422 (Which Site, When)** — THE evaluation-doctrine anchor. 5 deep models fail to
   decisively beat gradient-boosted; 3-rule tree wins lake hazards; spatial leakage inflates AUC
   0.9→0.54. Governs the whole project's claims (→ CR-02, FM-01, FM-12). Mandatory baselines.
2. **2104.11009 (PIML Narmada, India)** — hybrid physics+ML beats pure-ML AND keeps water-balance
   consistency; MORE constraints can HURT. Template for the physics gate + anti-over-engineering.
3. **1708.08611 (safe-RL shielding, ext)** — provable hard overrides preserving convergence →
   the formal basis for TRINETRA's monotone safety shield (Rule 19).
4. **2106.08909 (one-step offline RL, ext)** — simple often beats iterative offline RL on narrow
   data → CR-03; benchmark one-step before CQL/IQL curriculum.
5. **1904.02639 / 2108.06852 (MemAE / HF²-VAD)** — AE over-generalization makes reconstruction
   anomaly heads MISS anomalies (FM-18); directly threatens our forecast-residual scoring.
6. **2503.11849 + 2211.07044 (Copernicus-FM + SSL4EO-S12)** — define the EO-encoder design space
   and the data-scale saturation knee (~750K patches) that lets us budget Kaggle GPU-h.

## Cross-cutting THEMES that emerged
- T1 **Simplicity dominates under honest evaluation.** 2608.12422, 2201.06837, 2204.06097,
  2206.00515, 2104.11009, 2106.08909, 2106.06860 all point the same way → baseline-first,
  spatial-CV-gated, parsimony. This is the spine of the whole program (CR-02, CR-03).
- T2 **Inputs are the weak link, not just models.** Precipitation merges can collapse to
  near-zero (2404.10135); sensors brown-out / go missing (2307.04016, 2010.14934); → FM-17,
  FM-10, FM-15, CR-04. Robustness to bad/missing INPUTS matters as much as model skill.
- T3 **Human response is part of the system.** Alert fatigue / cry-wolf has measurable,
  compounding cost (2410.06388 quota) → FM-09; evaluation must include trust/compliance, not
  only ML metrics; alert modality should be calibrated, not maximal.
- T4 **Post-hoc, knowledge-gated layers over ML are an established robustness pattern**
  (2604.25512 quota, 2009.07415, 2205.09884) → disciplines GMF novelty; favors confidence-gated
  overrides reserved for the uncertain regime.
- T5 **Uncertainty must be first-class.** Bayesian/MCMC intervals for GLOF hydrographs
  (1806.05035), conformal (2107.07511), continuous-assurance re-validation on drift (2209.11632
  quota) → calibrated people-at-risk, not point estimates.
- T6 **Precursors are spatial AND temporal.** 1/v temporal metric (2007.02756) + InSAR
  community-persistence spatial metric (2212.12038) + dense coverage (2311.01564) → fuse both.

## GAPS in the baseline corpus (drive P2+ search, NOT fabricated findings)
- G1 Conformal/calibration under autocorrelation + missingness is THIN (only 2107.07511 read) —
  CR-04 needs dedicated A7 reading in P2.
- G2 No read paper yet gives CALIBRATED Himalayan I–D rainfall constants with uncertainty
  (Caine/Dahal-Hasegawa/Garhwal numbers = Bug #15) — carried to backlog; A3 search in P2.
- G3 Evacuation / cost-loss / value-of-warning decision models (A13) un-read in baseline — only
  indirect via 2410.06388 trust study. Needs A13 reading.
- G4 Drift / OOD monitoring methods (A14) only touched via assurance analogy (2209.11632) — needs
  dedicated reading.
- G5 LSPIV / river image-velocimetry (A9) specifics un-read (River Eye depends on it).
- G6 GLOF/dam-break transfer to MORAINE dams (vs earthfill 1806.05035) un-evidenced — HYPOTHESIS.
- G7 nhess-22-3309-2022 (Chamoli precursor) body unread (FETCH-DEFERRED) — load-bearing for the
  motivating event; re-fetch.

## CONTRADICTIONS surfaced / reinforced (see 06_contradiction_register.md)
- CR-01 EO encoder: 4 live contenders (DINOv2 / CROMA / Copernicus-FM / AnySat) — must each beat
  a plain-ViT+GB baseline under identical spatial-CV before adoption. UNRESOLVED (P7 trade study).
- CR-02 deep-vs-simple: REINFORCED strongly (T1 papers). Doctrine: baseline-first.
- CR-03 offline-RL staging: leans "prefer simple one-step" (2106.08909, 2106.06860) vs the
  report's 4-stage curriculum. UNRESOLVED (P15 benchmark).
- CR-04 conformal-under-missingness: OPEN, under-evidenced (G1).
- New tension (log in P5): report's "novel post-hoc GMF head" vs established post-hoc-reasoning
  prior art (2604.25512, 2009.07415, 2205.09884) → novelty must be the specific composition.

## Honesty ledger for this synthesis
- 43 baseline-corpus notes + 3 external anchors + (so far) 3 NEW quota notes underpin the above.
- Most reads are FT-PARTIAL (ar5iv middle-prune) → quantitative tables NOT fully verified; all
  numbers quoted are abstract/intro/visible-section values attributed to each paper, never ours.
- Papers listed in the ID tables above but WITHOUT a note are NOT yet read; their themes are
  inferred only from title/cluster and are candidates for P2+, not evidence here.

