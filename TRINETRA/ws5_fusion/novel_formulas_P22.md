# ws5_fusion/novel_formulas_P22.md — NOVEL supporting formulas for meta-fusion (Class C)

Phase P22 · RESEARCH-ONLY · WS5. NOVEL constructions authored for this program. HONESTY (Rule 20/21, §0.5):
**CLASS C — novel hypotheses, UNVALIDATED, NOT results.** Novelty is a SEARCH CLAIM under a LIMITED search
(no web_search; arXiv-abstract-level). NOTHING built/measured; no performance claimed (Rule 16). These feed the
weights of the novel aggregation operator (novel_aggregation_operator_P22.md). Grounding is SOURCE-REPORTED
(uncertainty-weighted fusion 2306.02050; evidential discounting 2608.29235/2412.01215; opinion pooling
1106.1638/2603.23853; AA/covariance-intersection 2110.01440/2307.14741; reliability-weighted integration
2006.15099).

Each formula lists: PURPOSE · PARENT + where it fails · DEFINITION · ASSUMPTIONS · USE · VALIDATION ROADMAP.
All are advisory (Rule 19), fail toward "uncertain".

---
## NF-1 — Physics-consistency score c_i  (used as a weight multiplier)
- PURPOSE: measure how well source i's hazard claim agrees with the PHYSICS gate (P7/P21), so a detector that
  fires with no physical support is down-weighted.
- PARENT + failure: raw confidence / softmax — says nothing about physical plausibility; a smoke-colored cloud
  can produce a confident but physically-inconsistent detection.
- DEFINITION: let φ ∈ [0,1] be the physics-gate plausibility (e.g. the normalized agreement between the
  observed rate-of-rise / plume geometry / flicker band and the Class-A/Class-B physics prediction, with its
  own uncertainty σ_φ). Define
    c_i = exp( − ( (p_i − φ)_+ )² / (2 (σ_φ² + ε)) ).
  Only the (p_i − φ)_+ POSITIVE part is penalized: a source claiming MORE hazard than physics supports is
  discounted; a source claiming LESS than physics is NOT penalized here (that disagreement is surfaced by the
  operator's disagreement term D and the fail-toward-caution bias, not silenced). ε > 0 for numerical safety.
- ASSUMPTIONS: φ and σ_φ are available and themselves calibrated; the physics gate is a Class-A/B prediction,
  never treated as ground truth.
- USE: multiplies the raw weight w̃_i in the operator; also logged for explainability to the human reviewer.
- VALIDATION: check it correctly discounts physically-impossible detections on held-out cross-site data without
  suppressing true fast-onset fires (which physics also predicts); expert review of φ.

## NF-2 — Drift-decayed reliability / trust r_i(t)
- PURPOSE: a running, drift-aware trust that decays when a source's recent agreement with corroborated outcomes
  degrades (ties the F-14 drift monitor and 2604.02351 reliability-as-dynamic-state).
- PARENT + failure: a fixed per-source weight — cannot react to a camera going out of focus, a sensor
  drifting, or a model degrading under shift.
- DEFINITION: exponential-forgetting reliability updated when corroborated feedback y_t (human-confirmed or
  cross-sensor-corroborated) is available:
    r_i(t) = clip_[r_min, 1]( (1−β) · r_i(t−1) + β · a_i(t) ),   a_i(t) = 1 − |p_i(t) − y_t|,
  with forgetting rate β ∈ (0,1); between feedbacks, apply a slow decay toward a neutral prior r0:
    r_i(t) = r0 + (r_i(t−1) − r0) · e^{−Δt/T_decay}.
  A HARD down-weight is applied when the drift monitor (F-14 / STUDD 2103.00903 / CUSUM 2510.25573) flags
  source i: r_i ← r_i · (1 − d_i), d_i ∈ [0,1] the flagged drift severity.
- ASSUMPTIONS: corroborated feedback is occasionally available (human-in-the-loop or cross-sensor); r_min > 0
  so no source is ever fully silenced without review (fail-safe).
- USE: multiplies w̃_i; drives the credible-alarm salience S in the operator (only high-r sources can raise ρ).
- VALIDATION: replay drift episodes; check r_i falls before a missed-event and recovers after recalibration;
  compare detection-delay vs a fixed-weight baseline (inferential-reproducibility gate 2302.04054).

## NF-3 — Conflict-to-uncertainty cross-modal term (disagreement penalty λ·D, defined)
- PURPOSE: convert inter-source CONFLICT into widened uncertainty rather than a confident wrong fused score
  (parallels evidential discounted-belief fusion 2608.29235, but for our bounded [0,1] scores).
- PARENT + failure: plain averaging hides conflict (two sources at 0.1 and 0.9 average to 0.5 and look
  "medium-confident" — false precision).
- DEFINITION: with D = Σ_i w_i (p_i − p̄)² (weighted dispersion from the operator), the fused uncertainty is
    U* = Σ_i w_i u_i  +  λ · D,     λ ≥ 0,
  and a conflict mass is reported separately: K = Σ_{i<j} w_i w_j · 1(|p_i − p_j| > κ_conflict). High K ⇒ the
  advisory is tagged "conflicting evidence — human review".
- ASSUMPTIONS: u_i are comparable across sources after calibration (P14); λ, κ_conflict fit on held-out data.
- USE: widens the reported band and can trip the UNCERTAIN state; shown to the reviewer.
- VALIDATION: check that conflicting-but-wrong consensus cases get wider bands and are escalated, not
  auto-resolved.

## NF-4 — Credible-alarm salience S (defines the fail-toward-caution trigger)
- PURPOSE: ensure the operator only bends toward MAX (ρ>1) when a TRUSTWORTHY, PHYSICS-CONSISTENT source is
  alarming — not on any single spurious spike (prevents alert fatigue while preserving Rule-19 caution).
- DEFINITION: S = max_i [ r_i(t) · c_i · ψ(p_i) ],  ψ(p) = sigmoid( (p − θ_alarm)/γ ) a soft alarm indicator.
- ASSUMPTIONS: θ_alarm, γ fit to the life-safety-asymmetric operating point.
- USE: enters ρ(t) = 1 + κ·D·S in the operator.
- VALIDATION: ablate S on/off; confirm the fail-toward-caution bias activates for true credible alarms and NOT
  for isolated low-reliability spikes.

---
## Honest limitations (all NF)
These are DESIGN choices with free hyperparameters, not derived optima; they assume occasional corroborated
feedback and reasonably-calibrated per-source uncertainty; the physics gate φ is itself Class-A/B (uncertain);
correlated source errors are only partially addressed. CLASS C throughout; EXPERT REVIEW (statistics +
fire-science) required before any external use; nothing is claimed to work.
