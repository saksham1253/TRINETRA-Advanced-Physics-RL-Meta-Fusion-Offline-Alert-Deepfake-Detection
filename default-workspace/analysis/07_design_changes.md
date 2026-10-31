# WHAT WOULD CHANGE OUR DESIGN — ranked design changes the literature argues for
# MASTER_PROMPT §P4 task 5. 10–20 concrete changes, ranked by (life-safety impact × evidence
# strength × cost-to-ignore). Each: the change, the evidence, the workstream it affects, and the
# phase that implements it. Rule 16: these are design decisions, NOT claims about our performance.
# Produced in P4 (2026-10-07) from 91 program-era deep reads.

Legend — Evidence: OVER-DETERMINED / STRONG / SUPPORTED / THIN. Priority: P0 (must, blocks a gate) …
P3 (nice-to-have). Transfer: HIGH/MED/LOW (confidence the result transfers to Himalayan conditions).

---

## P0 — must do; a gate is unsound without it

### DC-01. Spatial-CV with a correlation-range buffer is the ONLY admissible evaluation.
- Change: replace every random/in-dataset split with tile-withheld block CV, buffer g ≥ r (estimated
  spatial-correlation range by variogram); report the random-vs-block CI-width ratio as a leakage number.
- Evidence: 2610.08227 (theorem: effective N = Θ(n²/r²), CI underestimate ∝ r) [OVER-DETERMINED];
  2608.12422 (AUC 0.9→0.54 collapse on OUR hazards). Transfer: HIGH.
- Workstream: ALL ML. Phase: P14 (enforced), every gate from P5 on cites it. Fixes FM-01/FM-28.

### DC-02. Primary metric = cost-loss Value Score (Total Classification Cost), not F1/AUC.
- Change: all model selection and gates rank by TCC with explicit miss≫FA costs (p*=0.0476); never
  compare across base rates by a base-rate-dependent metric.
- Evidence: 2510.22016 (TCC as ideal criterion; metric value is a function of base rate) [STRONG];
  Bayes p* derivation (Bug#1). Transfer: HIGH. Workstream: all gates. Phase: P14. Fixes FM-29.

### DC-03. Conformal must be action-loss-calibrated AND mask-conditional AND online.
- Change: GMF conformal layer = per-zone Mondrian, conditioned on the present-sensor mask, calibrated to
  the alarm action loss, updated online; gate reports predictive AND action-loss coverage per zone/mask.
- Evidence: 2609.14821 (action-loss ≠ predictive coverage), 2512.14221 (mask-conditional valid CP),
  2610.02777 (online PID-Expert CP under abrupt shift) [STRONG, three independent]. Transfer: HIGH.
- Workstream: WS6. Phase: P14/P14Z. Fixes FM-03/FM-30/FM-31. Resolves CR-04.

### DC-04. Deepfake/zero-shot/crowd/social are LOW-TRUST advisory inputs, never an autonomous alarm.
- Change: route all media/crowd signals through GMF+conformal+shield as confidence modifiers; require
  multi-channel corroboration before any "authoritative" flag; human oversight on every real alert.
- Evidence: 2608.14391 RA-Bench (NO detector family generalizes; dissemination worsens detection)
  [STRONG]; Rule 19/C-16. Transfer: HIGH. Workstream: WS2/WS3. Phase: P11/P13. Fixes FM-38/FM-26.

### DC-05. Evaluate missing-modality by dropping the k MOST-informative modalities (worst-case).
- Change: robustness protocol drops the highest-utility sensors (not random); require safe degradation
  to local-obs + physics-shield floor; emit an uncertainty flag whenever a layer is absent.
- Evidence: 2609.15297 (worst-case), 2605.06643 (benchmarked degradation), 2608.15261 (utility routing)
  [STRONG]. Transfer: MED (re-derive routing for regression). Workstream: WS6/WS8. Phase: P14. Fixes FM-15/FM-35.

---

## P1 — strongly argued; changes an architecture decision

### DC-06. Forecasting heads learn a BOUNDED RESIDUAL on a mechanistic/temporal backbone; never from scratch.
- Change: lock the residual-on-backbone pattern into the GMF head; mandatory persistence + GBDT baselines.
- Evidence: THREAD I now 7× (2609.34836, 2607.26854, 2608.30205, 2412.11942, 2108.06868, 2509.18176,
  2507.15614, 2407.06785) [OVER-DETERMINED]. Transfer: HIGH. Workstream: WS1/WS8. Phase: P9/P10/P14. Fixes FM-02/FM-12.

### DC-07. Add an explicit EVT/tail head as a wide-uncertainty PRIOR (zoning, not alarm).
- Change: WHEN layer + people-at-risk carry a peaks-over-threshold/GPD tail model per catchment; feed it
  as a prior into GMF, never as a hard threshold.
- Evidence: 2509.10362 (GNN-rP r-Pareto) + 2510.12328 (season-aware GPD/POT) [RESOLVED, 2 sources].
  Transfer: MED (data-sparse tails unstable). Workstream: WS1. Phase: P14. Closes gap G5.

### DC-08. Physics (FoS/Newmark/Iverson) enters as a monotone GATE/constraint, not a regressed probability.
- Change: infinite-slope/TRIGRS/Iverson FoS is a hard shield in GMF; optionally a PINN constraint head on
  the landslide branch (borrow STRUCTURE, use hydrological physics).
- Evidence: 2610.04828 (FoS→prob nonlinear), 2407.06785 (PINN constraint) [STRONG]. Transfer: MED.
  Workstream: WS1. Phase: P7/P14. Fixes FM-13/FM-39.

### DC-09. Route each modality by learned task-utility BEFORE the first cross-modal mixing.
- Change: add a feature/semantic router to the fusion front-end; monitor negative-transfer rate so a
  stale/corrupt modality cannot drag the alarm.
- Evidence: 2608.15261 (missing-modality mAP +7.6..41.6pt; negative-transfer −12.7pp) [STRONG].
  Transfer: MED (detection→regression). Workstream: WS6/WS8. Phase: P14. Fixes FM-35. Closes gap G6.

### DC-10. Staged decision policy: fixed threshold → one-step offline RL → iterative RL ONLY if OPE-feasible.
- Change: do not start with full RL; adopt DFL/decision-loss first; gate any RL step on trustworthy OPE (FQE).
- Evidence: 2606.21773 (DFL "better prediction ≠ better decision"), 2107.11003 (OPE model selection)
  [RESOLVED]. Transfer: HIGH. Workstream: WS5. Phase: P15. Fixes FM-08. Resolves C-11.

### DC-11. Reward shaping stays potential-based and time-invariant (or prove the exception).
- Change: any RL shaping uses a Ng-1999 potential; no learned/time-varying shaping without a proof; treat
  the alarm MDP as partially observed.
- Evidence: 2608.08158 (PBRS optimality + §2.7 partial-obs limits) [STRONG]. Transfer: HIGH. Workstream:
  WS5. Phase: P15. Fixes FM-34.

---

## P2 — improves robustness / honesty; lower regret to defer but worth planning

### DC-12. Post-hoc conflict-aware evidence scaling (CLEAR) for sparse/OOD overconfidence.
- Change: wrap the risk head's evidence with s(x)=exp(−δ·C(x)) on a frozen evidential model to widen
  uncertainty in under-sampled cells; do not rely on temperature scaling.
- Evidence: 2610.01384 (+8.29/+5.01 OOD/adv AUROC, 17.4× faster) [SUPPORTED]. Transfer: MED. Workstream:
  WS6/WS8. Phase: P14. Fixes FM-36.

### DC-13. Pre-register a zero-shot-FM-vs-from-scratch benchmark under covariate noise (P14Z).
- Change: before adopting any TS/EO foundation model, benchmark it against a robust from-scratch model +
  residual on OUR noisy-covariate regime, under DC-01 CV, scored by DC-02.
- Evidence: 2610.07232 (Chronos-2 degrades under covariate noise; TimesNet more robust) [STRONG].
  Transfer: MED. Workstream: WS1/WS8. Phase: P14Z (compulsory, D-011). Fixes FM-32. Resolves CR-08. Closes G8.

### DC-14. Physics surrogate only where a calibrated solver/gauge exists; else EVT prior + gate + wide UQ.
- Change: use a Geo-FNO-style surrogate for cheap ensembles ONLY in calibrated catchments; ungauged
  catchments fall back to the EVT prior and physics gate.
- Evidence: 2507.15614 (surrogate needs a solver to emulate) [SUPPORTED]. Transfer: MED. Workstream: WS1.
  Phase: P14. Fixes FM-40.

### DC-15. SSL masked encoder → classical-anomaly ensemble (Deep-SVDD + iForest + OCSVM/LOF), edge-sized.
- Change: confirm the WS8 anomaly stack as SSL-latent + classical detectors, benchmarked head-to-head,
  engineered for the edge.
- Evidence: 2610.03649 (SSL→iForest/OCSVM/LOF, flown on Phi-sat-2) [SUPPORTED]; 2502.15901/2605.31155
  (TS-OOD). Transfer: MED. Workstream: WS8. Phase: P9/P10. Fixes FM-07.

### DC-16. Probe anticipation/lead-time explicitly for the alarm policy, not just final catastrophe count.
- Change: require the policy to beat a reactive baseline on EARLY detection; report lead-time distribution.
- Evidence: 2609.34041 (hollow safety gain with no anticipation evidence) [SUPPORTED/caveat]; 2610.03369
  (eval hygiene). Transfer: HIGH. Workstream: WS5. Phase: P15. Fixes FM-33.

### DC-17. Treat GMF as a documented COMPOSITION; withdraw any novelty claim (Rule 21).
- Change: describe GMF as stacking + bounded residual + Mondrian conformal + monotone shield with citations.
- Evidence: Wolpert-1992, THREAD I, Mondrian CP, 1708.08611 [STRONG]. Transfer: n/a. Workstream: P14. Resolves CR-06.

---

## Carried as OPEN items (evidence THIN — resolve in later phases, do NOT design around yet)
- DC-18 (THIN). Human-compliance/cry-wolf reward model needs real numbers → source NHESS/IJDRR in P13/P15
  (2109.07745 gives one hard number: 46% compliance). C-12. 
- DC-19 (OPEN). Cross-zone conformal with upstream→downstream hydrological coupling — research item, P14 (G2).
- DC-20 (OPEN). Rockfall (rigid-block) hazard not covered by the saturated-slope stack — coverage gap, P7 (G7).

---

## Ranked summary (one line each)
1 DC-01 spatial-CV buffer · 2 DC-02 cost-loss metric · 3 DC-03 action-loss+mask-conditional+online CP ·
4 DC-04 media=low-trust advisory · 5 DC-05 worst-case missing-modality eval · 6 DC-06 bounded residual ·
7 DC-07 EVT prior · 8 DC-08 physics-as-gate · 9 DC-09 utility routing · 10 DC-10 staged policy/OPE gate ·
11 DC-11 potential-based shaping · 12 DC-12 CLEAR evidence scaling · 13 DC-13 P14Z FM benchmark ·
14 DC-14 surrogate only if calibrated · 15 DC-15 SSL→classical anomaly · 16 DC-16 anticipation probe ·
17 DC-17 GMF = composition · (18–20 open/thin).

TOP THREE FOR USER DECISION (surfaced in the P4 gate): DC-01, DC-02, DC-03 — they are the cheapest to
adopt now and the most expensive to retrofit later; all three are gate-blocking for every downstream phase.
