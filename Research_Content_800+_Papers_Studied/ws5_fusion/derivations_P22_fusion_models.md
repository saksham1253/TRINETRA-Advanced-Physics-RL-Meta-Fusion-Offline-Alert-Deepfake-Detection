# ws5_fusion/derivations_P22_fusion_models.md — 6 derived meta-fusion physics models (P22)

Phase P22 · RESEARCH-ONLY · WS5 meta-fusion. SIX fusion models derived on paper. HONESTY (§0.5, Rule 16/19/20/
21): nothing built/measured; metrics in cited parents are SOURCE-REPORTED; every model is ADVISORY, human-in-
the-loop, fail-safe to "uncertain"; CLASS labels per Rule 20; novel pieces are SEARCH-claim novelty under a
LIMITED search. (Spec said one file per model; consolidated here for compactness — same content, each model is
self-contained.) Grounding references (source-reported): QMF 2306.02050; AA density fusion 2110.01440; split/
overlapping CI 2307.14741/2603.16768; hierarchical stacking 2101.08954; CBMA conformal 2511.16924; conflict-
discounted evidential 2608.29235, 2412.01215; MoE sigmoid gating 2405.13997; physics-informed RL 2212.02179,
2309.01909; ensemble-weighting RL 2106.06783. Weights/scores (w_i, c_i, r_i, u_i, S, D) are defined in
novel_formulas_P22.md and feed the PHARAOH operator (novel_aggregation_operator_P22.md).

Common inputs: M sources i with hazard p_i∈[0,1], uncertainty u_i, physics-consistency c_i, reliability r_i(t),
availability δ_i.

---
## FM-1 — Precision- & reliability-weighted linear fusion with physics residual  [CLASS B]
- PURPOSE: a transparent baseline fuser; the parent every fancier model must beat.
- PARENT + failure: plain average (ignores precision/reliability) and precision-only weighting (ignores
  physics plausibility + drift).
- DERIVATION: w_i ∝ δ_i r_i c_i exp(−u_i/τ); P = Σ w_i p_i (the ρ=1 case of PHARAOH). Add a physics residual
  feature e = p̄ − φ (fused vs physics gate φ) reported alongside, NOT folded into P.
- UNCERTAINTY: U = Σ w_i u_i + λD. ADVISORY; fail-open if Σw̃<w_min.
- VALIDATION GATE: must beat single best source by > seed variance on held-out cross-site (2302.04054).
- Class B (established precision/AA fusion blocks + validation route). Expert review: statistics.

## FM-2 — Evidential / Dempster–Shafer fusion with physics-prior mass + conflict discounting  [CLASS B]
- PURPOSE: represent IGNORANCE explicitly and turn inter-source CONFLICT into uncertainty, not false precision.
- PARENT + failure: Bayesian pooling assigns no mass to "don't know"; naive D-S combination explodes under
  high conflict (Zadeh's paradox).
- DERIVATION: each source → mass m_i({fire}), m_i({no-fire}), m_i(Θ)=ignorance from u_i. A physics PRIOR mass
  m_φ from the gate φ is added as one more body of evidence. Combine with a CONFLICT-DISCOUNTED rule
  (discount each m_i by r_i c_i, then combine; redistribute conflict K to Θ per 2608.29235) rather than raw
  Dempster normalization. Decision = pignistic/belief on {fire}, reported with belief–plausibility interval.
- UNCERTAINTY: the belief–plausibility gap + K (conflict mass). ADVISORY.
- VALIDATION GATE: calibrated (ECE) + beats FM-1 on missed-events at matched FA under conflict injection.
- Class B. Expert review: statistics + fire-science (physics prior).

## FM-3 — Conformal-bounded hierarchical stacked fusion  [CLASS B]
- PURPOSE: input-adaptive weights with a distribution-free coverage band.
- PARENT + failure: fixed stacking weights (2101.08954) are not input-adaptive and give no coverage guarantee;
  vanilla conformal breaks under shift.
- DERIVATION: a small gating head g(x) outputs input-dependent weights (hierarchical stacking / IA-BMA
  2510.22054); fuse P = Σ g_i(x) p_i; wrap with split-conformal calibrated on held-out data WITH covariate-
  shift reweighting (CBMA 2511.16924 + WCPS 2404.15018) → advisory band [P±q]. Reliability flag gates band use
  under shift (2604.22787).
- UNCERTAINTY: conformal band width + reliability flag. ADVISORY.
- VALIDATION GATE: realized PICP ≈ 1−α on cross-site; beats FM-1 efficiency.
- Class B. Expert review: statistics.

## FM-4 — Covariance-intersection fusion under unknown correlation (continuous hazard-trend state)  [CLASS B]
- PURPOSE: fuse CONTINUOUS state estimates (e.g. a hazard-trend / rate-of-rise estimate) from correlated
  sources without double-counting shared error.
- PARENT + failure: a Kalman update assumes known/zero cross-correlation; our sources share weather/scene
  confounders → naive fusion is over-confident.
- DERIVATION: for estimates (x̂_i, P_i), use Covariance Intersection: P_CI^{-1}=Σ ω_i P_i^{-1},
  x̂=P_CI Σ ω_i P_i^{-1} x̂_i, ω_i≥0, Σω_i=1 chosen to minimize tr(P_CI); use Split-CI (2307.14741) when a
  component is known-uncorrelated and Overlapping-CI (2603.16768) when partial correlation structure is known.
  Guarantees a CONSISTENT (conservative, never over-confident) fused covariance.
- UNCERTAINTY: P_CI (consistent by construction). ADVISORY trend estimate feeding the detector/operator.
- VALIDATION GATE: covariance consistency check + beats naive Kalman on calibration under correlated error.
- Class B. Expert review: estimation theory.

## FM-5 — Physics-consistency-gated mixture-of-experts  [CLASS C (novel gate)]
- PURPOSE: route among specialist experts (CCTV / IoT / satellite / anomaly) by scene + PHYSICS context.
- PARENT + failure: softmax-gated MoE routes on learned features only; can route to an expert that is
  physically implausible for the current regime (e.g. a flaming-fire expert in a smouldering regime).
- DERIVATION: gate weights g_i = σ( a_i(x) + β·log c_i ) (SIGMOID gating, more sample-efficient per 2405.13997;
  Laplace-gating option 2410.02935) with a PHYSICS BIAS term log c_i so physically-inconsistent experts are
  suppressed; fuse via PHARAOH with these g_i as base weights. The physics-biased gate is the NOVEL part.
- UNCERTAINTY: gate entropy + per-expert u_i. ADVISORY.
- VALIDATION GATE: beats FM-1/FM-3 on regime-shifted held-out data; ablate the physics-bias term.
- Class C (novel physics-biased gate). Expert review: ML + fire-science.

## FM-6 — RL-tuned adaptive fusion weights with physics-informed reward  [CLASS C]
- PURPOSE: let the ADVISORY RL layer (P15) adapt the PHARAOH hyperparameters (τ, κ, θ_alarm) and/or select
  which modalities to query (active perception / value-of-information) under cost/latency constraints.
- PARENT + failure: hand-fixed fusion hyperparameters can't adapt to drift/regime; generic RL ignores physics
  and can be unsafe.
- DERIVATION: state = {p_i, u_i, c_i, r_i, D, context}; ACTION = adjust (τ,κ) within safe bounds and/or choose
  the next sensor to poll (2607.22667, 1906.07233 VoI); REWARD = life-safety-asymmetric detection utility
  − λ_fa·false-alarm − λ_cost·sensing-cost + physics-consistency bonus (physics-informed reward, 2309.01909,
  2604.01830); CONSTRAINED/safe RL (2607.03125) so actions never disable the fail-safe or exceed FA budget.
  RL is ADVISORY: it tunes weights / suggests which sensor to check; it NEVER emits an alert or actuates
  (Rule 19). Must beat a non-RL auto-tuner / MILP schedule (2602.14676) to be kept.
- UNCERTAINTY: inherited from the operator; RL value uncertainty monitored. ADVISORY.
- VALIDATION GATE: beats non-RL baseline on held-out episodes by > seed variance; safety-constraint violations
  ≈ 0; offline-RL eval before any online use.
- Class C. Expert review: RL safety + fire-science + human-factors.

---
## Honest limitations (all FM)
All are paper designs with unfit hyperparameters; FM-5/FM-6 novel pieces are Class-C hypotheses; evidential/CI
consistency is by construction but calibration is not; RL (FM-6) must clear safe-RL + beat-baseline gates
before any use and stays advisory. Nothing is claimed to work or to beat anything. EXPERT REVIEW required.
