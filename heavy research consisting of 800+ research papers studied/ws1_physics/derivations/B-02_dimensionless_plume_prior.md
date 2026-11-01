# Derivation B-02 — Dimensionless / prior plume-temperature estimator

Class B (robustified extension). Phase P7 · WS1a · RESEARCH-ONLY (paper derivation; no code).
Parent: **EF-03 (Heskestad strong-plume centerline temperature)**. Supporting: Buckingham-Pi; Bayesian
prior; EF-02. Weakness targeted: EF-03 needs the convective HRR $\dot Q_c$ and virtual origin $z_0$ — both
UNKNOWN in the field — and its $(z-z_0)^{-5/3}$ far-field decay makes the signal at a distant sensor tiny
and noise-dominated. We recast EF-03 so it (i) is parameterized in a dimensionless, scale-robust form and
(ii) returns a POSTERIOR over temperature given noisy data and priors on the unknowns. Quota cross-refs:
McCaffrey $z/\dot Q^{2/5}$ scaling [2]; Zukoski $Q^*$/virtual origin [3]; t² growth prior [4].

## 1. EF-03 recap
$$ \Delta T_0 = 9.1\left(\frac{T_\infty}{g\,c_p^2\,\rho_\infty^2}\right)^{1/3}\dot Q_c^{2/3}\,(z-z_0)^{-5/3}. $$

## 2. Dimensionless recast (Buckingham-Pi, following McCaffrey/Zukoski scaling)
Define the normalized height used by McCaffrey [2]: $\zeta \equiv (z-z_0)/\dot Q_c^{2/5}$. Substitute
$z-z_0=\zeta\,\dot Q_c^{2/5}$ into EF-03:
$$ \Delta T_0 = 9.1\left(\frac{T_\infty}{g c_p^2 \rho_\infty^2}\right)^{1/3}\dot Q_c^{2/3}\,
   \big(\zeta\,\dot Q_c^{2/5}\big)^{-5/3}
   = 9.1\left(\frac{T_\infty}{g c_p^2 \rho_\infty^2}\right)^{1/3}\dot Q_c^{2/3-2/3}\,\zeta^{-5/3}. $$
The HRR exponent cancels: $2/3-(2/5)(5/3)=2/3-2/3=0$. Therefore
$$ \boxed{\;\Delta T_0 = 9.1\left(\frac{T_\infty}{g c_p^2 \rho_\infty^2}\right)^{1/3}\,\zeta^{-5/3}\;}
   \quad\text{i.e. }\Delta T_0 \text{ depends on height ONLY through } \zeta=(z-z_0)/\dot Q_c^{2/5}. $$
This is the physical content of McCaffrey's collapse [2]: the centerline temperature rise is a universal
function of the single dimensionless group $\zeta$. The estimator works in $\zeta$-space, which is
scale-invariant to the fire's strength.

## 3. Bayesian inversion for the unknowns
Given a noisy sensor reading $\widehat{\Delta T}=\Delta T_0+\epsilon$, $\epsilon\sim\mathcal N(0,s^2)$, and
priors $p(\dot Q_c)$ (e.g. a log-normal centered on the EF-02 $t^2$ estimate) and $p(z_0)$ (from EF-03's
$z_0=0.083\dot Q^{2/5}-1.02D$ with a prior on $D$), the posterior is
$$ p(\dot Q_c,z_0\mid \widehat{\Delta T}) \propto
   \mathcal N\!\big(\widehat{\Delta T};\,g(\zeta(\dot Q_c,z_0)),\,s^2\big)\,p(\dot Q_c)\,p(z_0), $$
with $g(\zeta)=9.1(T_\infty/g c_p^2\rho_\infty^2)^{1/3}\zeta^{-5/3}$. The estimator returns the posterior
predictive $\Delta T_0$ (a mean + credible interval), AND propagates the sensor noise $s$ — so when the
far-field signal is noise-dominated the interval is honestly wide rather than a false precise value.

## 4. Dimensional check
$\zeta=(z-z_0)/\dot Q_c^{2/5}$ carries the standard fire-correlation dimensional convention (m / kW^{2/5});
after the exponent cancellation the prefactor $9.1(T_\infty/g c_p^2\rho_\infty^2)^{1/3}$ times $\zeta^{-5/3}$
reproduces EF-03's units of temperature ✓ (identical to EF-03 since it is an algebraic rearrangement, not a
new relation). Posterior is a probability density over the same physical quantities ✓.

## 5. Reduction to parent (REQUIRED)
If $(\dot Q_c,z_0)$ are KNOWN (priors → point masses $\delta$) and noise $s\to0$: the posterior collapses to
a point, $\zeta$ is fixed, and $\Delta T_0=g(\zeta)$ which is ALGEBRAICALLY IDENTICAL to EF-03 (§2 is an
exact rearrangement). **B-02 → EF-03 exactly when the parameters are known and noise vanishes.** ✓

## 6. How it enters the system
Lets the system reason about plume temperature WITHOUT knowing the fire strength: produces a calibrated
expected-temperature interval at a sensor/pixel for consistency checks and anomaly gating, feeding meta-
fusion (P14) with an uncertainty it can weight. Soft prior; fallback = EF-03 with nominal $\dot Q_c$.

## 7. Validation plan & falsification
- Validate the $\zeta$-collapse and $g(\zeta)$ against Heskestad/McCaffrey plume datasets [2]; validate the
  posterior calibration (coverage of credible intervals) on held-out points. Build-gate: interval coverage
  ≈ nominal and sharper-than-prior where data informative.
- **Falsified if:** measured centerline temperatures do NOT collapse onto a single $g(\zeta)$ curve within
  stated scatter, OR posterior intervals are miscalibrated (coverage far from nominal).

## 8. Honesty
Coefficient 9.1 and the $-5/3$ law inherit EF-03 [coeff-verify]; this derivation adds NO new physics — it is
a dimensional rearrangement + standard Bayesian inversion, which is exactly the modest, honest kind of
robustification §P7 asks for. No performance claim (Rule 16). Expert review required before external use.
