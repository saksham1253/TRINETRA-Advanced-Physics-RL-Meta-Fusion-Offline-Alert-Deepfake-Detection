# Derivation B-06 — Sensor-response-corrected ceiling-jet / plume signal

Class B (robustified extension). Phase P7 · WS1a · RESEARCH-ONLY (paper derivation; no code).
Parents: **EF-05 (Alpert ceiling jet)**, **EF-10 (detector RTI / rate-of-rise)**, supporting **EF-03**.
Weakness targeted: the established models predict the IDEAL GAS temperature/velocity at a point, but a
cheap sensor reports a **lagged, transport-delayed, noisy** version of that signal. Rate-of-rise logic and
delta-features (P6 node) are timed off the OBSERVED signal, so we must model what the sensor actually sees.
Sources of building blocks: Alpert 1972 [EF-05]; Heskestad & Bill RTI [EF-10]; first-order lumped-
capacitance sensor model (standard). Quota cross-refs: [5], RTI block, PINN-derivative caution [33].

## 1. Set-up and symbols
A fire of HRR $\dot Q(t)$ (from EF-02 $\dot Q=\alpha t^2$) sits under a ceiling height $H$; a sensor is at
radial distance $r$. Let:
- $T_g(t)$ = ideal ceiling-jet gas temperature at $(r,H)$ from EF-05 [K]
- $u(t)$ = ceiling-jet gas velocity from EF-05 [m/s]
- $T_s(t)$ = sensor-element temperature actually reported [K]
- $\tau$ = sensor first-order time constant [s], with RTI $=\tau\sqrt{u}$ ⇒ $\tau(t)=\mathrm{RTI}/\sqrt{u(t)}$
- $t_d(r)$ = ceiling-jet transport delay from plume impingement to radius $r$ [s]
- $\eta(t)$ = additive measurement noise [K]

## 2. Transport delay (physics of "when the signal arrives")
The ceiling-jet front travels radially at ~the local jet velocity. Transport delay:
$$ t_d(r)=\int_0^r \frac{dr'}{c\,u(r')} $$
with $u(r')$ from EF-05 and $c\in(0,1]$ a front-speed factor (front ≈ fraction of peak velocity). Using the
far-field EF-05 velocity $u(r')=0.197\,\dot Q^{1/3}H^{1/2} r'^{-5/6}$ and treating $\dot Q$ as quasi-steady
over the transit:
$$ t_d(r)=\frac{1}{c\,0.197\,\dot Q^{1/3}H^{1/2}}\int_0^r r'^{5/6}\,dr' = \frac{r^{11/6}}{c\,0.197\,\dot Q^{1/3}H^{1/2}\,(11/6)} . $$
So $t_d \propto r^{11/6}\,\dot Q^{-1/3} H^{-1/2}$ — larger radius and smaller fire ⇒ longer delay.

## 3. Sensor thermal lag (physics of "how smeared the signal is")
Lumped-capacitance convective heating of the element (EF-10):
$$ \frac{dT_s}{dt}=\frac{\sqrt{u(t)}}{\mathrm{RTI}}\,\big(T_g(t-t_d)-T_s(t)\big)+\eta(t)
   \;=\;\frac{1}{\tau(t)}\big(T_g(t-t_d)-T_s(t)\big)+\eta(t). $$
This is a first-order low-pass filter with a (slowly) time-varying constant $\tau(t)=\mathrm{RTI}/\sqrt{u(t)}$
driven by the delayed gas temperature. For a locally-constant $\tau$ its solution is the convolution
$$ T_s(t)=\int_{-\infty}^{t}\frac{1}{\tau}e^{-(t-t')/\tau}\,T_g(t'-t_d)\,dt' \;+\;(\text{noise}). $$
i.e. **$T_s$ = EF-05 gas temperature, delayed by $t_d$ and low-pass filtered with time constant $\tau$,
plus noise.** The observed rate-of-rise is therefore
$$ \frac{dT_s}{dt}=\frac{1}{\tau}\big(T_g(t-t_d)-T_s\big), $$
which PEAKS later and lower than the true $dT_g/dt$ — exactly the bias cheap detectors show.

## 4. Dimensional check
$[\sqrt{u}/\mathrm{RTI}]=(m^{1/2}s^{-1/2})/(m^{1/2}s^{1/2})=s^{-1}$ ✓ (so $1/\tau$ has units s⁻¹).
$[t_d]$: $r^{11/6}\dot Q^{-1/3}H^{-1/2}$ with $\dot Q\propto$ kW — using the Alpert dimensional convention,
$t_d$ resolves to seconds given the EF-05 velocity units ✓ (same convention as EF-05; flagged [coeff-verify]
because EF-05 constants are dimensional). Convolution kernel $\frac{1}{\tau}e^{-t/\tau}$ integrates to 1
(dimensionless weighting) ✓.

## 5. Reduction to parent (REQUIRED)
As the sensor becomes ideal and close:
- $\tau\to0$ ⇒ the kernel $\frac{1}{\tau}e^{-(t-t')/\tau}\to\delta(t-t')$ ⇒ $T_s(t)\to T_g(t-t_d)$.
- $t_d\to0$ (small $r$, or $c\to$ large) ⇒ $T_s(t)\to T_g(t)$ and $dT_s/dt\to dT_g/dt$.
- $\eta\to0$ ⇒ noise-free.
Hence **B-06 → EF-05 (and EF-10's ideal link) exactly in the limit $\tau\to0,\,t_d\to0,\,\eta\to0$.** ✓

## 6. How it enters the system
- Gives the IoT node (P6) the correct expected shape/timing of a real detector signal → set rate-of-rise
  thresholds and multi-lag delta windows from $(\tau, t_d)$ instead of guessing; de-bias the detection time.
- Provides a forward model to generate realistic (lagged+noisy) synthetic sensor traces for training.
- Enters as a FEATURE/PRIOR with uncertainty; fallback = raw EF-05/EF-10 if $(\tau,t_d,\mathrm{RTI})$ unknown.

## 7. Validation plan (named data) & falsification
- Validate the lag model with standard **plunge-test RTI data** (Heskestad & Bill) for $\tau(u)$ and the
  EF-05 side with Alpert ceiling-jet datasets (validation_plan.md). Build-phase gate: predicted vs measured
  detector activation time must beat the bare-EF-05 (no-lag) prediction on held-out fire tests.
- **Falsified if:** adding $(\tau,t_d)$ does not reduce activation-time error vs the parent, OR measured
  sensor traces are not better explained by a delayed+low-passed EF-05 than by EF-05 alone.

## 8. Honesty
All constants inherit EF-05/EF-10 [coeff-verify] status. No performance claim; this is a derived expected-
signal model to be validated at build time (Rule 16). Expert review required before external use.
