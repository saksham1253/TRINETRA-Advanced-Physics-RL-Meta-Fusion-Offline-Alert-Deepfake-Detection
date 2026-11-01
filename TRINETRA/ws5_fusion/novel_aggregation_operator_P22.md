# ws5_fusion/novel_aggregation_operator_P22.md — NOVEL meta-fusion aggregation operator (Class C)

Phase P22 · RESEARCH-ONLY · WS5 meta-fusion. This is a NOVEL construction authored for this program.
HONESTY (Rule 20/21, §0.5): **CLASS C — novel hypothesis, UNVALIDATED, NOT a result.** It is "not found in our
search" where that search was LIMITED (no web_search; arXiv-abstract-level only) → the novelty is a SEARCH
CLAIM, not a proof of originality. NOTHING here is built, measured, or claimed to work or to beat any method
(Rule 16). Rule 19: the operator's output is ADVISORY, human-in-the-loop, and fails toward "uncertain", never a
false "all-clear". Grounding references are SOURCE-REPORTED (opinion pooling, Hölder/power means, precision-
weighted fusion, evidential fusion, conformal — see P22 literature map).

---
## 0. Purpose & where parents fail
We fuse M sources (physics gates, CCTV detector, IoT sensors, zero-shot complement, anomaly head) into ONE
advisory hazard score + calibrated uncertainty. Standard parents and their failure for us:
- Weighted ARITHMETIC mean / linear opinion pool: ignores uncertainty, can be dragged to a false "all-clear"
  by many agreeing-but-wrong low-reliability sources (complacency under correlated error).
- Weighted GEOMETRIC / log-linear pool: one near-zero source vetoes an alarm (dangerous for life-safety).
- Fixed MAX (noisy-OR): over-alarms on any single spurious spike → alert fatigue.
- Precision-weighted (Kalman-style) fusion: assumes calibrated Gaussian uncertainties + known correlation.
None ADAPT their behaviour to (a) inter-source disagreement, (b) per-source physics-consistency, (c) drift-
decayed reliability, (d) a life-safety asymmetry (missing a real fire ≫ a false alarm). The novel operator
below is designed to.

## 1. Per-source quantities (inputs)
For each source i ∈ {1..M} at time t:
- p_i ∈ [0,1] — hazard score/probability (post-calibration, P14).
- u_i ≥ 0 — predictive uncertainty (e.g. entropy or variance of p_i).
- c_i ∈ [0,1] — physics-consistency score (agreement with the physics gate; defined in novel_formulas_P22.md).
- r_i(t) ∈ [0,1] — drift-decayed reliability/trust (defined in novel_formulas_P22.md).
- δ_i ∈ {0,1} — availability (offline/missing ⇒ 0).

## 2. Effective weights (uncertainty-shrunk, physics- & reliability-gated)
Define the raw effective weight
  w̃_i = δ_i · r_i(t) · c_i · exp(−u_i / τ),         τ > 0 (uncertainty temperature).
Normalise over AVAILABLE sources: w_i = w̃_i / Σ_j w̃_j  (if Σ_j w̃_j = 0 → see §6 fail-open).
Interpretation: an unavailable, drifted, physics-inconsistent, or highly-uncertain source is automatically
down-weighted; exp(−u/τ) is the uncertainty-shrinkage factor (a soft precision weight that needs no Gaussian
assumption).

## 3. The operator — "PHARAOH mean" (Physics-consistency, Hazard-Aware, Reliability-decayed, Adaptive-Order Hölder mean)
Aggregate with an ADAPTIVE-ORDER weighted Hölder (power) mean:
  F_ρ(p; w) = ( Σ_i w_i · p_i^{ρ} )^{1/ρ},   ρ ≠ 0;   F_0 = Π_i p_i^{w_i}  (geometric, the ρ→0 limit).
The novelty is that the ORDER ρ is NOT fixed; it adapts to disagreement and a life-safety salience term:
  ρ(t) = 1 + κ · D · S,         κ ≥ 0 (safety-aggressiveness hyperparameter).
where
- D = weighted dispersion of the sources = Σ_i w_i (p_i − p̄)² , p̄ = Σ_i w_i p_i  (0 when sources agree).
- S = "credible-alarm salience" ∈ [0,1] = max_i [ r_i(t) · c_i · 1(p_i ≥ θ_alarm) ]  — large only when a
  HIGH-RELIABILITY, PHYSICS-CONSISTENT source is raising an alarm.
Reading: when sources AGREE (D≈0) or no credible alarm exists (S≈0) ⇒ ρ≈1 ⇒ plain weighted average. When
sources DISAGREE **and** a trustworthy source is alarming ⇒ ρ grows ⇒ the mean bends toward the MAX
(fail-toward-caution). It never bends below the arithmetic mean, so it cannot be argued into complacency by
disagreement (anti-"all-clear" bias). ρ is capped at ρ_max (finite, to avoid pure max / over-alarm).

## 4. Output + uncertainty + conformal bound
- Point advisory score: P* = F_{ρ(t)}(p; w) ∈ [0,1].
- Fused uncertainty (propagated, heuristic): U* = Σ_i w_i u_i + λ·D  (adds a disagreement penalty λ·D so that
  disagreement widens the uncertainty, not just the score).
- Conformal advisory band: [P* − q_{1−α}, P* + q_{1−α}] using a split-conformal quantile q_{1−α} calibrated on
  held-out data WITH covariate-shift reweighting (ties F-13 / WCPS 2404.15018); the band is reported, and under
  shift the reliability flag (High/Med/Low/Unreliable) from 2604.22787 gates how the band is used.

## 5. Properties (derived ON PAPER; to be checked numerically at build — NOT yet verified)
Let p_min = min_i p_i over available sources, p_max = max_i.
- (P1) Bounded: for any finite ρ, p_min ≤ F_ρ ≤ p_max (power-mean bounds). ⇒ output is a true interpolation,
  never an extrapolation.
- (P2) Monotonic: ∂F_ρ/∂p_i ≥ 0 for w_i ≥ 0 ⇒ raising any source's hazard never lowers the fused hazard.
- (P3) Known-mean limits: ρ=1 → weighted arithmetic mean; ρ→0 → weighted geometric mean; ρ→+∞ → weighted max;
  ρ→−∞ → weighted min. Our ρ≥1 always ⇒ the operator lives between the arithmetic mean and the max.
- (P4) Power-mean inequality ⇒ for ρ≥1, F_ρ ≥ F_1 = weighted arithmetic mean. **Safety corollary:** under
  disagreement with a credible alarm (ρ>1), the fused score is ≥ the plain average ⇒ a structural anti-
  complacency bias (designed for Rule 19). It equals the average exactly when sources agree or no credible
  alarm exists.
- (P5) Idempotence: if all p_i = p then F_ρ = p for every ρ. Consensus is preserved.
- (P6) Availability-safe: removing a source renormalises weights continuously; no divide-by-zero except the
  all-unavailable case handled in §6.
- (P7) Non-vetoing: because ρ≥1 (not the geometric/log-linear regime), a single near-zero source cannot drive
  the fused score to 0 ⇒ no accidental "all-clear" veto.
(Assumptions: w_i ≥ 0, Σw_i = 1, p_i ∈ [0,1]. P1–P5 follow from standard weighted-power-mean theory; the
NOVEL part is the adaptive ρ(t)=1+κDS and the resulting §P4 safety corollary — these are the Class-C claims to
validate.)

## 6. Fail-safe (Rule 19) — fail-open to "uncertain", never a false all-clear
- If Σ_j w̃_j < w_min (too little trustworthy, physics-consistent, available evidence) ⇒ DO NOT emit a score;
  emit state = **UNCERTAIN/DEGRADED** and escalate to the human reviewer. Silence/offline ⇒ "uncertain", not
  "all clear".
- If a single source is alarming but S is below the credible-alarm threshold (low reliability/consistency) ⇒
  advisory "possible — needs corroboration", never an auto-alert.
- The operator NEVER triggers a public alert; it ranks an advisory for a human (ties P12/P15).

## 7. Parameters & how they would be fit (build-phase)
τ (uncertainty temperature), κ (safety-aggressiveness), ρ_max, θ_alarm, λ (disagreement→uncertainty), w_min
(fail-open floor), α (conformal level). Fit on held-out CROSS-SITE/CROSS-CAMERA data by jointly minimising a
life-safety-asymmetric loss (false-negative cost ≫ false-positive cost) subject to a calibration constraint
(PICP ≈ 1−α) and a max false-alarm-rate budget. All fitting is a BUILD activity; nothing fit here.

## 8. Validation roadmap (what would make this a result — none done)
1. Numerically verify P1–P7 and the §P4 safety corollary on synthetic sources. 2. Ablate adaptive-ρ vs fixed
arithmetic/geometric/max and vs precision-weighted and evidential fusion on held-out cross-site data, using the
inferential-reproducibility gate (2302.04054): keep ONLY if it reduces missed-events at matched false-alarm
rate by > seed/trial variance. 3. Check calibration (PICP vs nominal) under injected covariate shift. 4. Red-
team: can correlated adversarial sources defeat the reliability/consistency gating (ties P16)? 5. Fire-science
+ statistics EXPERT REVIEW of the operator and its safety corollary before any external use.

## 9. Honest limitations
Heuristic uncertainty propagation (U*) is not a calibrated variance; ρ(t)=1+κDS is a design choice, not an
optimum; the safety corollary biases toward alarms by construction (raises false-alarm risk — the τ/κ/budget
fit must manage it); correlated source errors are only partially handled by r_i·c_i gating; conformal validity
needs the WCPS reweighting and breaks under concept drift. CLASS C throughout. No performance is claimed.
