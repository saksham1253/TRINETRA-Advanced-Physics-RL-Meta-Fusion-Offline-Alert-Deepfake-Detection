# P4 SOTA SCAN — SYNTHESIS (currency-check of the consensus positions)

# MASTER_PROMPT §P4 Task 1: "SOTA scan of the consensus positions you are about to record
# (check that they are still current)." This is a VERIFICATION scan, not a fresh harvest:
# for every consensus statement P4 is about to write into analysis/04_synthesis.md, we ask
# (a) is it still the field's current position? (b) is there a newer paper that strengthens,
# qualifies, or REFUTES it? (c) which NEW quota paper (P4 §P4.8) should be read to settle it?
#
# Evidence tags: [FT]/[FT-PARTIAL]/[ABS]/[LV](lead, not yet opened). Numbers AS-PUBLISHED with
# their own protocol. NO claims about our own system (Rule 16). Novelty = "not found in N
# sources searched" (Rule 21). Living document; appended as the P4 quota reads land.

## Phase: P4 — Synthesis
## Date: 2026-10-07
## Method: arXiv export API (quoted-phrase + AND, submittedDate desc) + non-arXiv (NHESS/MDPI/
##   Frontiers, D-010), novelty-checked vs analysis/02_paper_ledger.csv + manifests/novelty_index.csv.
##   Consensus positions enumerated from: CR-01..CR-07 (06_contradiction_register), THREADS I/J/K/L/M,
##   FM-01..FM-27 (05_failure_mode_catalogue), the P1/P2/P3 interim syntheses, and BUILD_HANDOFF.

---

## PART A — THE CONSENSUS POSITIONS P4 IS ABOUT TO RECORD (enumerated, then currency-checked)

The synthesis will assert ~16 consensus positions. Each is a claim the corpus already supports;
P4 must confirm it is still current and name the resolving/challenging quota paper.

| # | Consensus position (to be recorded in 04_synthesis) | Anchors already read | Currency verdict | Quota target to confirm/challenge |
|---|------------------------------------------------------|----------------------|------------------|------------------------------------|
| C-01 | Spatial leakage inflates hazard skill; every claim needs tile-withheld spatial-CV + GB/tree/persistence baselines | 2608.12422[FT-PARTIAL], 2509.18176, 2110.09497 | STILL CURRENT (strongest external, OUR hazards) | geo-CV critique paper (2025/26) |
| C-02 | Deep learning does NOT reliably beat gradient-boosted/simple baselines for hazard (parsimony) — 6-domain pattern | 2608.12422, 2610.01994, 2609.20441, 2509.18176, 2609.18555, 2610.03369, 2605.06643 | STILL CURRENT, over-determined | tabular-DL-vs-GBDT 2025/26 meta |
| C-03 | Learn a bounded RESIDUAL on a mechanistic/deterministic backbone, not from scratch (THREAD I, 5×) | 2609.34836, 2607.26854, 2608.30205, +2 ABS | STILL CURRENT, converging | new residual/physics-ML forecaster |
| C-04 | Alarm stack = ensemble forecast → decision/action-loss calibration → cost-loss threshold (THREAD K + CR-04 sharpen) | 2608.30205, 2609.14821, Bayes p*=0.0476 | STILL CURRENT | decision-focused/end-to-end learning |
| C-05 | Conformal on our streams is approximate-under-stability, NOT a hard guarantee; must target ACTION-LOSS coverage | 2010.09107, 2606.00690, 2511.15838, 2609.14821 | STILL CURRENT; abrupt-break+missingness OPEN | CP-under-missingness (2406.05405) |
| C-06 | Tail/EVT model needed for people-at-risk + zoning; wide-uncertainty prior, not real-time alarm (THREAD J) | 2509.10362 | THIN (single paper) → NEEDS a 2nd EVT source | EVT/POT hydro-ML paper |
| C-07 | SAR-first for the cloud problem; SAR beats optical in monsoon; bi-temporal change not single-pass | 2608.11142, 2605.02153(ABS), SAR-GLOF-seg | STILL CURRENT | SAR-FM downstream (parks to P7) |
| C-08 | Missing-modality is adversarial/worst-case, not random; co-learning fix (CR-07) | 2605.06643, 2609.15297, 2310.03986, 2607.24683 | STILL CURRENT, well-covered | — (saturated) |
| C-09 | GMF is a COMPOSITION of known parts (stacking + residual + Mondrian-conformal + shield), not an invention (CR-06) | 2604.25512, Wolpert-1992, 2009.07415 | STILL CURRENT (honest reframing) | stacking/meta-learner theory |
| C-10 | RL eval needs ≥100 seeds + tail/dispersion + two-baseline rule; architectural "fixes" can mask spec failures | 2610.03369 | STILL CURRENT | deep-RL reproducibility 2025/26 |
| C-11 | Decision layer may not need RL: fixed-threshold → one-step offline RL → (iterative only if OPE-feasible); stochastic-program alt | 2106.08909, 2311.14110, 2608.26304 | STILL CURRENT | decision-focused / predict-then-optimize |
| C-12 | Cry-wolf/alert fatigue is a real modellable human-response failure; reward must cost FA > flat penalty | 2104.11422, 2311.10228, 2410.06388 | STILL CURRENT | alert-fatigue/warning-compliance 2025/26 |
| C-13 | Proximity-bias overconfidence in sparse regions; temp-scaling does NOT fix it; transformers worse than CNNs | 2306.04590 | STILL CURRENT | calibration-under-sparsity |
| C-14 | Metric value is a function of base rate → never rank models across imbalance ratios; cost-loss Value Score primary | 2206.09981, 2601.05921 | STILL CURRENT | eval-metric critique |
| C-15 | Physics FoS → failure-probability map is nonlinear; treat FoS as a GATE not a calibrated probability | 2610.04828 | STILL CURRENT | reliability-method geotech |
| C-16 | Life-safety: low-trust advisory inputs (zero-shot/crowd/social/deepfake) into GMF+conformal+shield, never autonomous (Rule 19) | 2604.24404, 2610.04151, 2512.14683 | STILL CURRENT | assurance-case / human-in-loop EWS |

## PART A VERDICT
- 14 of 16 consensus positions are confirmed STILL CURRENT by already-read corpus; none REFUTED.
- TWO are THIN and are promoted to the top of the P4 quota target list:
  - **C-06 (EVT/tail-risk)** — rests on a single paper (2509.10362). Need ≥1 independent EVT/POT
    hydrological-ML source to avoid a single-point-of-failure in the synthesis.
  - **C-04/C-11 (decision-focused learning)** — the "calibrate to the decision, not the prediction"
    and "predict-then-optimize vs end-to-end" literature is under-sampled; one strong DFL paper
    would consolidate C-04, C-11 and the GMF action-loss spec.
- Everything else: quota papers should target (i) challenges to the consensus (papers that argue DL
  DOES beat GBDT, or that CP IS valid on streams — to stress-test C-02/C-05), and (ii) meta-research
  on evaluation practice in our fields (per §P4 quota-topic instruction).

## PART A — POST-QUOTA CURRENCY UPDATE (after 15 NEW P4 reads; 2026-10-07)
Verdict changes recorded against each consensus position:
- **C-01 REINFORCED → PROVEN.** 2610.08227 (TGRS 2026) supplies the finite-sample theorem: effective
  sample size Θ(n²/r²) not n²; block holdout with separation g=Θ(r·log(n/δ)); random holdout
  underestimates CI width by factor ∝ r. C-01 is no longer "best-practice" but a provable requirement.
- **C-02 REINFORCED.** 2608.12422 full-ABS (589 HMAGLOFDB outbursts, spatial-CV, 5 DL models do NOT
  beat GBDT; 3-rule tree reproduces lake-hazard baseline) + 2509.18176 (CNN-LSTM vs LightGBM/LASSO;
  baselines default to persistence) + Indian-conditions corroborators 2609.36975 (XGBoost 78.82% >
  DL 64–66% Punjab), 2608.19672 (SAGE-XGBoost +33pp). Parsimony result holds; DL wins only with a
  learned spatio-temporal residual, never from scratch — which is exactly C-03.
- **C-03 REINFORCED (6th/7th corroboration).** 2509.18176 + 2507.15614 (HEC-RAS Geo-FNO surrogate,
  3.5× ensemble speedup) + 2407.06785 (PINN Newmark constraint on data-driven backbone). THREAD I
  now 7-deep; residual/physics-surrogate doctrine is over-determined.
- **C-04/C-11 RESOLVED.** 2606.21773 (DFL review: "better prediction ≠ better decision"; SPO/
  surrogate taxonomy) consolidates the action-loss doctrine; 2107.11003 (offline-RL model selection
  via FQE/OPE, healthcare) operationalizes "iterative RL only if OPE-feasible." Both THIN positions
  closed.
- **C-05 RESOLVED (missingness + abrupt-break edges).** 2512.14221 (mask-conditional valid CP under
  general missingness) + 2610.02777 (PID-Expert online conformal, narrower intervals under abrupt
  distributional shift). CR-04 missingness edge closed; the abrupt-break edge now has a concrete
  online-aggregation mechanism.
- **C-06 RESOLVED (2nd EVT source).** 2510.12328 (Physics-Informed GAT + Season-aware GPD/POT,
  Thailand; competitive with SEAS5). EVT no longer single-point-of-failure. NOTE: 2510.12328 is
  ABS/NO-HTML → non-quota, but it discharges the currency check for C-06.
- **C-07 REINFORCED.** 2608.15261 (optical–SAR routing, missing-modality mAP +7.6..41.6pt) + 2504.03166
  RingMoE (14.7B multimodal-RS FM, physics-informed SSL; parked to P7). SAR-first + reliability-aware
  fusion both current.
- **C-08 REINFORCED.** 2608.15261 (negative cross-modal transfer is real; routing before first mixing;
  routing weights ∝ leave-one-modality-out utility) + 2610.03649 (SSL-encoder→classical-anomaly stack
  benchmarked vs iForest/OCSVM/LOF). "Missing modality is adversarial, not random" holds.
- **C-10 REINFORCED.** 2608.08158 (dynamic reward-shaping framework; PBRS optimality theorem +
  §2.7 limits under episodic/partial-obs/multi-agent) + 2609.34041 (VLM-Safe-RL: catastrophe 31.6→19.4%
  but NO evidence of anticipation — a direct caution that a headline safety gain can be mechanistically
  hollow; feeds C-10 "architectural fixes can mask spec failures").
- **C-12 STILL THIN but QUANTIFIED.** 2109.07745 (Kincade wildfire GPS: 46% evacuation compliance
  inside warning/order zones; self+shadow evacuees >50%) gives a hard human-response number; still only
  one hazard-domain quantification → remains flagged for P13/P15. (Non-quota: cs.CY, older.)
- **C-13 SUPPORTED.** 2610.01384 CLEAR (post-hoc, frozen base; conflict-aware evidence scaling
  s(x)=exp(−δC(x)); +8.29/+5.01 OOD/adv AUROC) is a concrete post-hoc fix for the proximity-bias
  overconfidence C-13 names. 2609.16707 (predictability decays per scale; FMs lag at ≥90° turning
  events) corroborates "generic models are worst exactly in the rare regime."
- **C-14 SUPPORTED.** 2510.22016 (Total Classification Cost as the ideal criterion; metric taxonomy
  anti-diagonal/main-diagonal/globally-robust; example-dependent unit costs) formalizes "pick the
  metric from the cost model" and the base-rate-dependence warning.
- **C-15 REINFORCED.** 2407.06785 (PINN retrieves geotechnical params then constrains with Newmark;
  physics as constraint, not black box) supports "FoS/physics as a GATE, not a calibrated probability."
- **C-16 SUPPORTED (life-safety anchor).** 2608.14391 RA-Bench (NO detector family — traditional,
  zero-shot MLLM, or fine-tuned — generalizes on crisis AI-video; dissemination worsens detection;
  human-deceptive clips also fool detectors) is hard evidence that deepfake/zero-shot/crowd signals
  must be LOW-TRUST advisory into GMF+conformal+shield, never autonomous (Rule 19).

VERDICT: 16/16 consensus positions current; 6 RESOLVED/closed, 8 REINFORCED, 2 SUPPORTED; none refuted.
C-12 remains the single thinnest (one hard number, older cs.CY) — carried as an open item to P13/P15.

---

## PART B — QUOTA TARGET LIST (15+ NEW, synthesis-driven; §P4 quota topics)

Priority order (resolve contradictions / fill gaps the synthesis exposes; prefer meta-research &
consensus-challenging papers). Each will be novelty-checked before counting.

1. [C-06] EVT / peaks-over-threshold + ML for rainfall/flood tails — SECOND source beyond 2509.10362.
2. [C-04/C-11] Decision-focused / end-to-end predict-then-optimize learning (calibrate to the decision).
3. [C-02] Recent tabular-DL-vs-GBDT meta-analysis (does the parsimony result still hold in 2025/26?).
4. [C-02-challenge] A paper arguing DEEP models DO win on hazard/geoscience (stress-test parsimony).
5. [C-05] Conformal prediction under missingness (2406.05405 route) — the still-open CR-04 edge.
6. [C-10] Deep-RL reproducibility / evaluation meta-research (post-2022, beyond 2610.03369).
7. [C-12] Alert-fatigue / warning-compliance quantified (human-response failure, 2025/26).
8. [C-16] Safety assurance case / GSN / continuous assurance for ML EWS (Q8.1 still thinly sourced).
9. [C-14] Evaluation-metric critique for imbalanced/rare-event classification (consolidate C-14).
10. [C-03] A fresh residual/physics-ML forecaster (6th THREAD-I corroboration or a counter-example).
11. [C-01] Spatial cross-validation / geographic generalization critique (consolidate C-01).
12. [C-13] Calibration under distribution sparsity / few-neighbour regions (beyond ProCal).
13. [cross] Multi-hazard / compound-event ML (compound failure, joint exceedance — ties THREAD J).
14. [cross] Nowcasting benchmark/eval critique (rare-heavy-rain weighting; ties C-03/WHEN layer).
15. [cross] Foundation-model-for-time-series or EO critique (does an FM help OUR regime? ties C-07).
16. [buffer] Any outstanding consensus-challenging paper surfaced while reading 1–15.

Soft cap 15; user discretion allows exceeding for genuinely SOTA/consensus-moving papers; NO padding
(§0.5). Non-arXiv sources used where arXiv veins are exhausted (D-010).

---

## PART C — SEARCH LEDGER (continues analysis/02_search_log.md numbering from row 219)
All via https://export.arxiv.org/api/query (HTTP 200), quoted-phrase +AND+, submittedDate desc, 2026-10-07.

| # | Query (phrases AND-joined) | total | kept (NEW quota) | note |
|---|-----------------------------|-------|------------------|------|
| 220 | "decision-focused learning" + "prediction" + "optimization" | ~ | 2606.21773 | DFL review → C-04/C-11 |
| 221 | "conformal prediction" + "missing data" / "missingness" | ~ | 2512.14221 | mask-conditional CP → C-05 |
| 222 | "extreme value theory" + "rainfall" + "deep learning" (+POT) | ~ | 2510.12328(ABS) | 2nd EVT source → C-06 (non-quota) |
| 223 | "spatial cross-validation" / "satellite image" + "independent samples" | ~ | 2610.08227 | spatial-CV theorem → C-01 |
| 224 | "cost-sensitive" + "evaluation" + "classifier" | ~ | 2510.22016 | TCC metric → C-14 |
| 225 | "calibration" + "out-of-distribution" + "regression" + "uncertainty" | 34 | 2610.01384 | CLEAR evidential → C-13 |
| 226 | "offline reinforcement learning" + "off-policy evaluation" + "healthcare" | 2 | 2107.11003 | OPE model-selection → C-11 |
| 227 | "foundation model" + "time series" + "zero-shot" + "forecasting" | 215 | 2610.07232 | TSFM covariate-noise → C-07/P14Z |
| 228 | "warning" + "compliance" + "evacuation" + "behavior" | 1 | 2109.07745(nq) | evac compliance 46% → C-12 |
| 229 | "self-supervised" + "SAR" + "change detection" | 5 | 2504.03166(park P7) | RingMoE 14.7B FM |
| 230 | "glacial lake outburst" + "deep learning" | 4 | 2601.12330(ABS,nq) | IceWatch GLOF; 2608.12422 re-study |
| 231 | "reward shaping" + "safety" + "reinforcement learning" | 63 | 2608.08158 ; 2609.34041(nq) | dynamic PBRS → C-10 ; VLM-Safe caveat |
| 232 | "missing modality" + "remote sensing" | 15 | 2608.15261 | optical–SAR routing → C-08 |
| 233 | "conformal prediction" + "time series" + "distribution shift" | 14 | 2610.02777 | PID-Expert online CP → C-05 |
| 234 | "physics-informed" + "landslide" | 3 | 2407.06785 | PINN Newmark → C-15/WS1 |
| 235 | "multimodal" + "misinformation" + "detection" + "disaster" | 2 | 2608.14391 | RA-Bench crisis-video → C-16/WS2 |
| 236 | "InSAR" + "time series" + "deep learning" + "deformation" | 3 | 2509.18176(RE-STUDY) | CNN-LSTM InSAR fcst → C-03/WS8; already read P2 → non-quota re-study |
| 237 | "anomaly detection" + "satellite" + "self-supervised" | 2 | 2610.03649 | on-board SSL anomaly → C-08/WS8 |
| 238 | "ensemble" + "flood forecasting" + "machine learning" | 3 | 2507.15614 | HEC-RAS Geo-FNO → C-03/WS1 |
| 239 | "rainfall threshold" + "landslide" + "early warning" | 0 | — | arXiv vein empty (Caine/ID lit is non-arXiv) |
| 240 | "gradient boosting" + "deep learning" + "tabular" | 63 | 2605.14365 | LoMETab: 2026 DL-vs-GBDT currency → C-02 (genuine 15th quota read) |
| (236b) | wind-direction extreme-shear (from q225 adjacency) | — | 2609.16707 | predictability-per-scale → C-13/C-06 |

MALFORMED (discarded, re-run clean): three queries written with "AND:" literal → arXiv parsed as OR
giving junk mega-totals (18561 / 214150 / 105269). Lesson re-confirmed: join with +AND+all:"...".

QUOTA CLOSE: 15 body-level NEW quota reads (see P4_reading_progress FINAL HONEST TALLY). Honest-count
corrections (§0.5): 2510.12328 is ABS/NO-HTML → non-quota (C-06 corroborator); 2509.18176 was already read
FT-PARTIAL in P2 → non-quota re-study. The genuine 15th is 2605.14365 (LoMETab, q240), a 2026 currency
check that CONFIRMS C-02 (parsimony not reversed; GBDT still exceptionally strong). Non-arXiv not needed this
phase — the synthesis-driven axes were still live on arXiv. C-12 axis is genuinely arXiv-thin (q228
total=1, q239 total=0): the warning-compliance / rainfall-threshold literature lives in NHESS/Landslides/
IJDRR, flagged to P13/P15 (D-010 non-arXiv route) rather than padded here (§0.5).
