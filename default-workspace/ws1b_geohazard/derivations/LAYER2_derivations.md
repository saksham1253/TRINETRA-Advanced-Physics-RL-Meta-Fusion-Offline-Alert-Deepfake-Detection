# ws1b_geohazard/derivations/LAYER2_derivations.md — full Layer-2 geo-hazard derivations

Phase P7G · WS1b · RESEARCH-ONLY. Each extension: parent(s), targeted weakness, FULL derivation,
dimensional check, REDUCTION TO PARENT in a stated limit, validation route, falsification. No own-system
performance claim (Rule 16). Coefficients inherit the parents' [coeff-verify] tags; expert review required.

================================================================================
## GB-01 — Probabilistic infinite-slope stability  (parent GH-01)
Weakness targeted: GH-01 returns a POINT factor of safety FS from (c',φ',γ,z,m,β) that are deeply uncertain
in ungauged Himalayan slopes → a single FS is false precision.

Derivation. Treat the uncertain inputs as random variables θ=(c',φ',γ,z,m,β) with priors (ranges from soil
class + DEM slope + the moisture state m from the node). FS=g(θ) is GH-01. The hazard quantity is the
failure probability
    P_f = P(FS < 1) = ∫_{g(θ)<1} p(θ) dθ.
First-order (FORM) approximation: with FS mean μ_FS=g(μ_θ) and variance σ_FS² ≈ Σ_i (∂g/∂θ_i)² σ_i²
(evaluated at μ_θ), the reliability index β_rel=(μ_FS−1)/σ_FS and P_f≈Φ(−β_rel) (Φ standard normal CDF).
Sensitivities ∂g/∂θ_i are the analytic partials of GH-01 (e.g. ∂FS/∂m = +γ_w z cos²β tanφ' / (denominator)
> 0 ⇒ wetter → lower FS, correct sign). The node's measured moisture updates p(m) (narrowing σ_m), which
sharpens P_f over time.

Dimensional check: FS dimensionless ✓; β_rel dimensionless ✓; P_f ∈[0,1] ✓; each σ_i in the units of θ_i so
(∂g/∂θ_i)σ_i is dimensionless ✓.

Reduction to parent: as all σ_i→0 (parameters known exactly), σ_FS→0 and P_f→ 1{g(μ_θ)<1}, i.e. the
deterministic GH-01 verdict FS<1 ⇔ failure. **GB-01 → GH-01 in the zero-uncertainty limit.** ✓

Enters system as: a calibrated P(FS<1) feature/prior for fusion + a monitored quantity whose uncertainty
shrinks as sensors inform m; fallback = deterministic GH-01 with nominal parameters.
Validation route: back-test P_f against a landslide inventory (reliability/coverage; Brier score) on slopes
with known triggering rainfall; vs deterministic FS. Falsified if P_f is no better calibrated than a
constant base-rate, or sensitivities show wrong signs on data.

================================================================================
## GB-02 — Sensor-corrected transient pore-pressure  (parent GH-02 Iverson)
Weakness targeted: GH-02 gives ground-truth pressure head ψ(Z,t); a cheap piezometer/soil-moisture node
measures a LAGGED, NOISY, possibly drifting proxy, and D₀,K_s are unknown.

Derivation. Iverson's response gives the true head ψ(Z,t)=ψ0(Z)+ΔI·R(t,Z;D₀) (R the error-function response
to surface flux). A porous-cup piezometer has a first-order time response (Hvorslev lag): the measured head
    dψ_m/dt = (1/T_lag)(ψ(Z,t) − ψ_m) + η(t),  T_lag = (V/(A))·(1/(K_s·F_shape))  (instrument time constant),
with sensor noise η and slow drift d(t). Solving the convolution,
    ψ_m(t) = ψ_m(0)e^{−t/T_lag} + (1/T_lag)∫₀^t e^{−(t−s)/T_lag} ψ(Z,s) ds + (noise+drift).
Invert for the geotechnically relevant ψ by deconvolution with a Bayesian prior on (D₀,K_s,T_lag) and a
drift model; output a POSTERIOR ψ(Z,t) (mean + interval) feeding GB-01's m.

Dimensional check: 1/T_lag [s⁻¹]; kernel ∫=1 ✓; ψ in metres head throughout ✓.

Reduction to parent: as T_lag→0 (instant sensor), η→0, d→0, and (D₀,K_s) known, ψ_m→ψ(Z,t)=Iverson's head
exactly. **GB-02 → GH-02 in the ideal-sensor, known-parameter limit.** ✓

Enters system as: the moisture/pore-pressure state estimate (with uncertainty) that drives GB-01 and GB-03;
fallback = raw sensor reading when parameters unknown. Validation: plunge/step-response lab test for T_lag;
compare deconvolved ψ to co-located reference piezometer. Falsified if deconvolution does not reduce lag/
bias vs raw reading on step tests.

================================================================================
## GB-03 — Antecedent-aware probabilistic rainfall threshold  (parent GH-05 ID threshold)   [CORE EWS model]
Weakness targeted: GH-05's deterministic I=α D^(−β) ignores antecedent moisture and gives a single line →
documented high false-alarm/missed rates; no lead-time/decision trade.

Derivation. Keep the ID power law as the backbone but (i) condition on antecedent soil-moisture state S
(from the node / API) and (ii) output a PROBABILITY of exceedance, not a binary line. Define the normalized
rainfall load
    x = log I − [log α(S) − β log D],  with α(S) = α₀·f(S)  (drier S raises the threshold, wet lowers it).
Model landslide-triggering probability with a logistic link calibrated to a local inventory:
    P(trigger | I,D,S) = σ_logit(w₀ + w₁ x),   σ_logit(u)=1/(1+e^{−u}).
The decision to warn uses a cost-loss / decision-curve: warn when P ≥ p*, where p* is set by the operator's
false-alarm-vs-missed-detection cost ratio and desired LEAD TIME (longer lead ⇒ lower p*, more false
alarms). Report the ROC/decision-curve, not one line.

Dimensional check: x dimensionless (log of a ratio of like-dimensioned intensities) ✓; P∈[0,1] ✓.

Reduction to parent: set f(S)≡1 (ignore antecedent moisture), w₁→∞ with w₀ chosen so the logistic becomes a
step at x=0, and p*=0.5. Then P(trigger)=1{log I > log α₀ − β log D} = 1{I > α₀ D^(−β)} — exactly the
deterministic GH-05 threshold. **GB-03 → GH-05 as a hard step with no antecedent term.** ✓

Enters system as: THE landslide early-warning trigger probability (advisory), with explicit false-alarm vs
lead-time trade; fallback = regional ID line. Validation: back-test on a local landslide inventory with
rainfall records (POD/POFD, Brier, decision-curve net benefit) vs the plain ID line. Falsified if adding S
and the probabilistic form does not improve calibrated skill (e.g. Brier/AUC, net benefit) over GH-05.

================================================================================
## GB-04 — Antecedent-moisture-corrected SCS-CN runoff  (parent GH-08)
Weakness targeted: GH-08's CN depends on antecedent moisture (AMC I/II/III) as crude discrete classes and
fixes initial abstraction λ=0.2 (widely disputed).

Derivation. Replace the discrete AMC with a continuous sensor-informed retention. Let the node's soil-
moisture state S∈[0,1] scale the potential retention:
    S_ret(S) = S_ret,II · r(S),   r(S) = (1 − S)/(1 − S_II) scaled to the AMC-I/III envelope (monotone
    decreasing: wetter soil → less retention → more runoff), and treat the initial-abstraction ratio λ as an
    uncertain parameter (prior around literature values, not fixed 0.2):
    Q = (P − λ S_ret)² / (P + (1−λ) S_ret),  for P > λ S_ret, else 0.
Propagate uncertainty in (S, λ, CN_II) to a runoff interval.

Dimensional check: S_ret, P, Q all in mm ✓; r(S), λ, S dimensionless ✓.

Reduction to parent: set λ=0.2 and r(S)=1 (AMC-II, ignore sensor) ⇒ Q=(P−0.2S_ret,II)²/(P+0.8S_ret,II),
exactly GH-08. **GB-04 → GH-08 at λ=0.2, AMC-II.** ✓

Enters system as: a sensor-informed flash-flood runoff estimate with uncertainty feeding routing/lead-time;
fallback = standard CN with AMC table. Validation: event rainfall-runoff pairs for small catchments (NSE/
bias) vs fixed-CN. Falsified if continuous-AMC + uncertain-λ does not reduce runoff error vs the AMC table.

================================================================================
## GB-05 — Hysteresis-corrected stage–discharge  (parent GH-12 rating)
Weakness targeted: GH-12's single-valued Q=a(h−h₀)^b ignores the LOOP (hysteresis) in unsteady flow →
discharge under/over-estimated on the rising/falling limb.

Derivation. Jones formula (unsteady correction to the steady rating): the true discharge relates to the
steady rating Q_s(h)=a(h−h₀)^b by
    Q = Q_s(h)·sqrt( 1 + (1/(S₀ c)) · dh/dt ),
where c is the kinematic wave celerity and S₀ the bed slope; dh/dt from the stage sensor's time series gives
the rising-limb (dh/dt>0 ⇒ Q>Q_s) / falling-limb (Q<Q_s) correction. Propagate stage-rate noise to an
interval.

Dimensional check: inside sqrt, (1/(S₀ c))·dh/dt → [1/((−)(m/s))]·[m/s] = dimensionless ✓; Q same units as
Q_s ✓.

Reduction to parent: steady flow dh/dt→0 ⇒ Q→Q_s(h)=a(h−h₀)^b, exactly GH-12. **GB-05 → GH-12 for steady
stage.** ✓

Enters system as: a better discharge/level estimate from a cheap stage sensor for flood lead-time; fallback
= steady rating. Validation: loop-rating events with ADCP/reference discharge (bias on rising vs falling
limb) vs single-valued rating. Falsified if the Jones correction does not reduce limb-dependent bias.

================================================================================
## Independent-recheck note
These five Layer-2 derivations are queued for an independent re-derivation pass (as done for P7's B-01/02/
05/06). GB-01 FORM sign (∂FS/∂m<0), GB-03's step-limit reduction, and GB-05's dimensionless Jones factor are
the items most worth an independent recheck. Recorded in verification_checklists.md.
