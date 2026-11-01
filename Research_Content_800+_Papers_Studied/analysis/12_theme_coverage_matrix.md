# THEME-COVERAGE MATRIX (Phase P1, Task 6)
#
# Maps the themes that P2 (evidence consolidation) and P3 (component deep-dives) must cover
# against the papers that currently supply evidence, and flags where coverage is THIN (a gap
# the later phases must fill). Rows = themes (T-/safety-critical-ML/evaluation themes derived
# from analysis/01_baseline_papers.md and the P1 quota reads). Columns = evidence class.
#
# COVERAGE LEGEND:  FT = full-text/FT-PARTIAL note exists;  ABS = abstract-only in ledger;
#                   GAP = no adequate evidence yet (owning phase must close).
# Paper IDs in [brackets] with (Q#) marking the 15 NEW P1 quota papers.
# Nothing here claims OUR system works (Rule 16).

## A. Synthesis themes (from 01_baseline_papers.md: T1–T6) × evidence
| Theme | Core claim | FT / FT-PARTIAL evidence | ABS-only support | Coverage | Owning phase |
|-------|-----------|--------------------------|------------------|----------|--------------|
| T1 Simplicity dominates under honest evaluation | deep models rarely beat GB/tree/persistence under spatial-CV | 2608.12422; 2405.00031(Q10); 2606.21130(Q11); 2106.08909 | 2509.18176; 2150.08975 | STRONG | P5/P7 |
| T2 Inputs are the weak link | precip/QPE, sensors, modality all fail silently | 2404.10135; 2310.03986(Q14); 2103.09783(Q9) | 2605.02153; 2411.04153 | STRONG | P6/P7 |
| T3 Human response is part of the system | cry-wolf/trust/habituation shape real outcomes | 2410.06388(Q1); 2104.11422(ABS note) | 2311.10228; 2210.08975 | MODERATE | P15/P19 |
| T4 Post-hoc knowledge-gated layers are prior art | GMF = composition, not invention | 2604.25512(Q3) | Wolpert-1992; 2009.07415; 2205.09884 | MODERATE | P15 |
| T5 Uncertainty is first-class | calibrated PI + proximity-aware calibration required | 2010.09107(Q4); 2306.04590(Q13) | 2303.12783; 2502.05709; 2208.05875 | MODERATE | P7/P16 |
| T6 Precursors are spatial + temporal | InSAR deformation + antecedent weather discriminate | 2608.12422; CROMA 2311.00566 | 2509.18176; 2503.11849; 2412.14123 | MODERATE | P7 |

## B. Safety-critical-ML methodology themes (P1 §P1 mandate) × evidence
| Theme | Core question (key-question tag) | Evidence (quota in bold-ish) | Coverage | Owning phase |
|-------|----------------------------------|------------------------------|----------|--------------|
| SC1 Assurance structure (safety case / GSN, continuous assurance) | Q8.1 | 2209.11632(Q2) | THIN (1 paper) → GAP to widen in P5/P9 | P5/P9 |
| SC2 Evaluation of multi-component pipeline | Q8.2, Q0.4 | 2206.09981(Q7); 2601.05921(Q15); 2311.14110(Q12); 2010.09107(Q4); 2306.04590(Q13) | STRONG (the P1 eval stack) | P5 |
| SC3 System reliability / tech-debt / train-serve skew | Q0.5, Q5.4 | 2103.09783(Q9) | THIN (1 paper) → GAP | P9/P16 |
| SC4 False-alarm / alert-fatigue at system level | Q4.4, Q6.1 | 2410.06388(Q1); 2104.11422(ABS); 2608.26304(Q6) | MODERATE | P15/P19 |
| SC5 End-to-end disaster detection→response reference designs | Q6.3 | 2405.00031(Q10); 2606.21130(Q11); 2608.26304(Q6) | MODERATE | P5 |
| SC6 Rare-event / imbalance handling + metrics | Q0.4, Q2.2 | 2206.09981(Q7); 2412.13439(Q8); 2606.21130(Q11) | MODERATE | P5/P7 |
| SC7 Drift / OOD monitoring on live stream | Q2.3, Q2.4 | 2404.19452(Q5) | THIN (1 FT) + ABS 2205.13723/2411.15204 → widen | P16 |
| SC8 Off-policy evaluation feasibility before trust | Q4.1 | 2311.14110(Q12); 2106.08909 | MODERATE | P15 |
| SC9 Missing-modality robustness | Q4.5 | 2310.03986(Q14) | THIN (1 FT) → widen | P15 |
| SC10 Decision-theoretic objective (cost-loss, equity) | Q0.4, Q6.1 | 2601.05921(Q15); 2608.26304(Q6) | MODERATE | P5/P15 |

## C. Component deep-dive themes (P3) × encoder/decision/UQ coverage
| Component | Key question | Named contenders / methods (evidence) | Coverage | Owning phase |
|-----------|-------------|---------------------------------------|----------|--------------|
| EO encoder (CR-01) | Q2.1 | DINOv2 2304.07193(FT); CROMA 2311.00566; Copernicus-FM 2503.11849; AnySat 2412.14123; +2306.04590(Q13) calibration cost | STRONG (4 contenders + CR-02 gate) | P7 |
| Decision layer (CR-03) | Q4.1 | one-step/TD3-BC 2106.08909/2106.06860; shield 1708.08611; DataCOPE 2311.14110(Q12); stochastic-opt 2608.26304(Q6) | STRONG | P15 |
| UQ layer (CR-04) | Q3.1 | EnbPI 2010.09107(Q4); ProCal 2306.04590(Q13); open: 2303.12783/2406.05405 | MODERATE (drift+missingness open) | P7/P16 |
| Fusion head / GMF (CR-05/CR-06) | Q4.3 | prior art 2604.25512(Q3)+stacking; collapse risk 2601.03425/2604.00801 | MODERATE | P15 |
| Node energy / comms | Q5.2/Q5.3 | ACES 1909.01968(FT,HP-01); drift-energy 2404.19452(Q5); DTN 2603.15945 | MODERATE | P6 |

## D. GAPS flagged by this matrix (feed analysis/01_baseline_papers.md G-list + reading queue)
- G-SC1: assurance-case / GSN for ML EWS rests on ONE paper (2209.11632) → P5/P9 must widen
  (search: safety case patterns for continuously-updated ML; regulatory assurance for EWS).
- G-SC3: AI technical-debt / train-serve skew rests on ONE paper (2103.09783) → P9/P16 widen.
- G-SC7: live-stream drift/OOD monitoring thin (2404.19452 + ABS) → P16 deep-dive.
- G-SC9: missing-modality robustness thin (2310.03986) → P15 build-time dropout evaluation.
- G-CR04: conformal coverage under abrupt drift + missingness still open (2406.05405 UNREAD)
  → carried in PHASE_BACKLOG; P7/P16.
- G-T3: human-response/trust evidence is mostly ABS + one cry-wolf ODE unread full-text
  (2104.11422) → P15 obtains full text.

# BUILT 2026-10-06 (P1). This matrix is a planning surface for P2/P3; it is NOT a claim of
# performance. Update as phases close gaps.
