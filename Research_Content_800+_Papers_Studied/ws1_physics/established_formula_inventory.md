# ws1_physics/established_formula_inventory.md — Layer 1 (Class A) established model inventory

Phase P7 · WS1a · RESEARCH-ONLY (derivations on paper; no code). This is Layer 1: the ESTABLISHED fire/
smoke/sensor relations relevant to detecting fire from CCTV + low-cost sensors. Each is a Class-A model =
a baseline and a PARENT for Layer-2 extensions. Equations are in LaTeX. Units are SI unless noted; fire HRR
is conventionally in kW, lengths in m, temperatures in K (or °C where a correlation is fitted that way).

## HONESTY & SOURCING (§0.5, Rule 16, and §P7 3(e))
- These are canonical relations from established fire science (primary papers + the SFPE Handbook of Fire
  Protection Engineering). Coefficients/exponents are stated from standard references and tagged
  **[coeff-verify]** where the exact constant should be confirmed against the primary source before any
  load-bearing or external use; the P7 quota reading cross-checks them and a qualified fire-science/heat-
  transfer expert MUST review before external use.
- NO number here is our own measurement. "Known weaknesses" are the documented limits that make these
  models imperfect in OUR non-ideal setting (cheap-sensor lag/noise, low-res/low-fps CCTV, unknown source
  strength/geometry, outdoor wind, non-ideal environments) — these motivate the Layer-2 extensions.
- Recovered "originally identified models" (from the P0 project context, §P7 task 2): plume dynamics, flame
  geometry/flicker, smoke optics + camera radiometry, heat transfer/thermal signature, smoke/gas transport
  to a sensor, fire growth, spread dynamics, sensor-response physics. All are represented below (EF-01..12).

Legend: **Statement · Symbols/units · Source · Validity · Assumptions · KNOWN WEAKNESSES (→ Layer-2 hook)**

---

### EF-01 — Heskestad mean flame height
- **Statement:** $L = 0.235\,\dot Q^{2/5} - 1.02\,D$
- **Symbols/units:** $L$ mean (visible) flame height [m]; $\dot Q$ total heat release rate [kW]; $D$ fire
  (base) diameter [m]. Coeffs [coeff-verify].
- **Source:** Heskestad (1983); SFPE Handbook (plume/flame-height chapter).
- **Validity:** buoyancy-dominated turbulent diffusion flames; dimensionless HRR / flame Froude number in
  the normal pool-fire range; near-circular base.
- **Assumptions:** single buoyant source, still air, flame height defined by 50%-intermittency; HRR known.
- **KNOWN WEAKNESSES:** (i) needs $\dot Q$ and $D$ — both UNKNOWN from a passive camera; (ii) fails under
  wind/tilt and for line/irregular fires; (iii) "visible" height ≠ what a low-res/smoke-obscured camera
  measures in pixels. → **Layer-2 hook B-01:** camera-observed apparent flame height = EF-01 composed with
  projection + smoke extinction (EF-07), with uncertainty on unknown $\dot Q,D$.

### EF-02 — t² fire growth and heat release rate
- **Statement:** $\dot Q(t) = \alpha\,(t-t_0)^2$, with growth classes $\alpha$ [kW/s²]: slow 0.00293,
  medium 0.01172, fast 0.0469, ultrafast 0.1876 [coeff-verify, NFPA 72].
- **Symbols/units:** $\dot Q$ HRR [kW]; $\alpha$ fire-growth coefficient [kW/s²]; $t_0$ incipient-delay [s].
- **Source:** NFPA 72 design-fire classes; SFPE Handbook; NIST calorimeter data.
- **Validity:** growth phase of flaming fires up to the ventilation/fuel limit; design-fire idealization.
- **Assumptions:** well-defined ignition, unobstructed growth, single fuel package.
- **KNOWN WEAKNESSES:** real fires deviate (incipient smouldering, plateaus, multi-item spread); $\alpha$ is
  a coarse class, not measured. → feeds EF-03/EF-05 as the time-varying source; motivates rate-of-rise
  features rather than absolute thresholds (ties EF-10, and P6 node delta features).

### EF-03 — Heskestad strong-plume centerline temperature & velocity (with virtual origin)
- **Virtual origin:** $z_0 = 0.083\,\dot Q^{2/5} - 1.02\,D$ [coeff-verify].
- **Centerline excess temperature:**
  $\Delta T_0 = 9.1\left(\dfrac{T_\infty}{g\,c_p^2\,\rho_\infty^2}\right)^{1/3}\dot Q_c^{2/3}\,(z-z_0)^{-5/3}$
- **Centerline velocity:**
  $u_0 = 3.4\left(\dfrac{g}{c_p\,\rho_\infty\,T_\infty}\right)^{1/3}\dot Q_c^{1/3}\,(z-z_0)^{-1/3}$
- **Symbols/units:** $z$ height above source [m]; $z_0$ virtual origin [m]; $\dot Q_c=\chi_c\dot Q$ convective
  HRR [kW], $\chi_c\approx0.7$; $T_\infty$ ambient temp [K]; $\rho_\infty$ ambient density [kg/m³]; $c_p$
  [kJ/kg·K]; $g=9.81$ m/s². Coeffs 9.1, 3.4 [coeff-verify].
- **Source:** Heskestad; SFPE Handbook (fire plumes).
- **Validity:** far field above the flame ($z>L$), axisymmetric, still environment.
- **Assumptions:** point/weak source in far field, Boussinesq, top-hat→Gaussian self-similar profile,
  constant entrainment, no stratification/wind.
- **KNOWN WEAKNESSES:** breaks in near field, under wind, in ventilated/stratified rooms; needs $\dot Q_c$;
  the $-5/3$ decay makes $\Delta T$ at a far detector tiny and noise-dominated. → **Layer-2 hook B-02:**
  dimensionless/prior formulation marginalizing unknown $\dot Q_c, z_0$ + sensor-noise propagation.

### EF-04 — McCaffrey three-regime centerline correlations (alternative plume parent)
- **Statement:** piecewise power laws for centerline velocity $u$ and temperature rise $\Delta T$ vs the
  normalized height $z/\dot Q^{2/5}$ across continuous-flame, intermittent, and buoyant-plume regimes:
  $\dfrac{u}{\dot Q^{1/5}} = \kappa\left(\dfrac{z}{\dot Q^{2/5}}\right)^{\eta}$ with regime-specific
  $(\kappa,\eta)$ [coeff-verify].
- **Source:** McCaffrey (1979, NBS); SFPE Handbook.
- **Validity:** covers the near-to-far field via three regimes; lab gas-burner data.
- **Assumptions:** as EF-03 but regime-resolved; still air.
- **KNOWN WEAKNESSES:** regime boundaries fuzzy; same wind/geometry limits; discrete-regime seams. → kept as
  an ALTERNATIVE parent to EF-03 (model-set ablation decides which; §P7 task 6).

### EF-05 — Alpert ceiling-jet maximum temperature & velocity
- **Temperature:** $r/H>0.18:\ \Delta T_{max}=\dfrac{5.38\,(\dot Q/r)^{2/3}}{H}$ ;
  $r/H\le0.18:\ \Delta T_{max}=\dfrac{16.9\,\dot Q^{2/3}}{H^{5/3}}$ [coeff-verify].
- **Velocity:** $r/H>0.15:\ U_{max}=\dfrac{0.197\,\dot Q^{1/3} H^{1/2}}{r^{5/6}}$ ;
  $r/H\le0.15:\ U_{max}=0.96\,(\dot Q/H)^{1/3}$ [coeff-verify].
- **Symbols/units:** $\Delta T_{max}$ max excess gas temp under ceiling [K/°C]; $U_{max}$ [m/s]; $H$ ceiling
  height above fire [m]; $r$ radial distance [m]; $\dot Q$ [kW].
- **Source:** Alpert (1972); SFPE Handbook (ceiling jets).
- **Validity:** steady fire, unconfined flat ceiling, $r/H$ within fitted range; near-field quasi-steady.
- **Assumptions:** flat smooth ceiling, no beams/vents, quasi-steady HRR.
- **KNOWN WEAKNESSES:** transient fires, beams/obstructions, high ceilings → large errors; predicts GAS
  temperature, not the (lagged) detector temperature. → **Layer-2 hook B-03:** convolve EF-05 output with
  detector RTI lag (EF-10) to predict the ACTUAL sensor signal (ceiling-jet transport-delay + thermal lag).

### EF-06 — Point-source radiation model
- **Statement:** $\dot q''_r(R) = \dfrac{\chi_r\,\dot Q}{4\pi R^2}$ (incident radiant heat flux at distance
  $R$ from a point-source flame).
- **Symbols/units:** $\dot q''_r$ [kW/m²]; $\chi_r$ radiant fraction (~0.15–0.40) [coeff-verify]; $R$ [m].
- **Source:** SFPE Handbook (radiation from fires); Modak point-source model.
- **Validity:** far field $R\gg$ flame size; optically-thin path.
- **Assumptions:** isotropic point emitter, no atmospheric/smoke absorption, cold surroundings.
- **KNOWN WEAKNESSES:** near field and large flames need solid-flame/view-factor models; smoke & humidity
  absorb (invalid optically-thin); $\chi_r$ varies with fuel/soot. → informs IR/thermopile sensing range +
  **Layer-2 hook** coupling with atmospheric/smoke attenuation (EF-07/EF-09).

### EF-07 — Beer–Lambert smoke light extinction (what a camera sees through smoke)
- **Statement:** $\dfrac{I}{I_0}=e^{-\kappa L}$ ; extinction coefficient $\kappa = K_m\,m$ ; optical density
  $OD=\log_{10}(I_0/I)$ ; relation $\kappa = \ln(10)\cdot(OD/L)$.
- **Symbols/units:** $I,I_0$ transmitted/incident intensity; $\kappa$ extinction coeff [1/m]; $L$ path [m];
  $K_m$ mass-specific extinction coefficient ≈ **8.7 m²/g** flaming smoke (≈4.4 smouldering) [coeff-verify,
  Mulholland]; $m$ smoke mass concentration [g/m³].
- **Source:** Bouguer–Lambert–Beer; Mulholland & Croarkin; SFPE Handbook (smoke characterization).
- **Validity:** monochromatic-ish, single-scattering/optically-thin, uniform smoke along path.
- **Assumptions:** no multiple scattering, uniform concentration, wavelength-appropriate $K_m$.
- **KNOWN WEAKNESSES:** multiple scattering at high density; $K_m$ depends on fuel/soot/wavelength; a camera
  integrates over a non-uniform path and spectral band. → **Layer-2 hook B-01/B-04:** camera-radiometric
  extinction feature with path/soot uncertainty; discriminates dense dark smoke vs translucent steam.

### EF-08 — Flame flicker / puffing frequency scaling
- **Statement:** $f \approx 1.5\,D^{-1/2}$ [Hz] (pool/axisymmetric buoyant flame puffing); Strouhal form
  $St = f\,D/u$; also $f \propto (g/D)^{1/2}$ [coeff-verify, Cetegen & Ahmed; Pagni].
- **Symbols/units:** $f$ puffing frequency [Hz]; $D$ source diameter [m]; $u$ characteristic velocity [m/s].
- **Source:** Cetegen & Ahmed (1993); Pagni; Hamins et al.
- **Validity:** buoyancy-dominated flames, $D$ roughly 0.1–1 m → $f\sim1.5$–5 Hz.
- **Assumptions:** axisymmetric buoyant pool flame, no strong cross-flow.
- **KNOWN WEAKNESSES:** turbulent/wind-blown flames broaden/shift the band; **critically, a low-fps CCTV
  (e.g. 10–15 fps) ALIASES the 1.5–5 Hz band** (Nyquist) → the raw frequency feature is corrupted. →
  **Layer-2 hook B-05:** aliasing-aware flicker-band feature (fold the true band through the camera sampling
  rate; reduces to EF-08 as fps→∞).

### EF-09 — Thermal-camera radiometry (temperature retrieval)
- **Statement:** measured radiance $L_{meas}=\varepsilon\,\tau_{atm}\,L_{bb}(T_{obj}) + (1-\varepsilon)\,
  \tau_{atm}\,L_{bb}(T_{surr}) + (1-\tau_{atm})\,L_{bb}(T_{atm})$ ; grey-body total emission
  $E=\varepsilon\,\sigma\,T^4$ (Stefan–Boltzmann).
- **Symbols/units:** $\varepsilon$ emissivity; $\tau_{atm}$ atmospheric transmittance; $\sigma=5.67\times
  10^{-8}$ W/m²K⁴; $T$ [K]; $L_{bb}$ Planck blackbody radiance.
- **Source:** standard IR radiometry; SFPE/heat-transfer texts.
- **Validity:** grey-body objects; known $\varepsilon,\tau_{atm}$; within sensor spectral band.
- **Assumptions:** known emissivity + atmosphere; no scattering by smoke in band.
- **KNOWN WEAKNESSES:** unknown/variable $\varepsilon$, humidity-dependent $\tau_{atm}$, solar/IR reflections
  → false "hot" readings (the IR flame-sensor sunlight false-trigger of P6). → **Layer-2 hook:** emissivity/
  atmosphere-uncertainty-aware temperature with confidence; pairs with EF-06.

### EF-10 — Heat-detector thermal lag / Response Time Index (RTI) & rate-of-rise
- **Statement:** $\dfrac{dT_e}{dt}=\dfrac{\sqrt{u}}{\mathrm{RTI}}\,(T_g - T_e)$, with $\mathrm{RTI}=\tau\sqrt{u}$;
  first-order sensor lag $\tau$. Rate-of-rise logic triggers on $dT_e/dt$ exceeding a threshold.
- **Symbols/units:** $T_e$ sensing-element temp [K]; $T_g$ gas temp [K] (from EF-05); $u$ gas velocity [m/s];
  RTI [m^{1/2} s^{1/2}]; $\tau$ time constant [s].
- **Source:** Heskestad & Bill; SFPE Handbook (detector actuation).
- **Validity:** convective heating of a lumped sensing element in a ceiling jet.
- **Assumptions:** lumped-capacitance element, convection-dominated, known RTI/$u$.
- **KNOWN WEAKNESSES:** cheap sensors have large/uncertain $\tau$, add noise, and gas sensors add chemical
  lag/drift not in this model → observed signal lags and is noisy. → **Layer-2 hook B-06 (CORE for P6):**
  sensor-response-corrected signal model = EF-05/EF-03 convolved with first-order lag + noise; reduces to the
  parent as $\tau\to0$. Directly supports the node's baseline-normalized multi-lag delta features.

### EF-11 — Rothermel surface fire spread rate (wildland)
- **Statement:** $R=\dfrac{I_R\,\xi\,(1+\phi_w+\phi_s)}{\rho_b\,\varepsilon\,Q_{ig}}$
- **Symbols/units:** $R$ rate of spread [m/min or ft/min]; $I_R$ reaction intensity; $\xi$ propagating flux
  ratio; $\phi_w,\phi_s$ wind & slope factors; $\rho_b$ bulk density; $\varepsilon$ effective heating number;
  $Q_{ig}$ heat of pre-ignition.
- **Source:** Rothermel (1972, USDA); used in BehavePlus/FARSITE.
- **Validity:** quasi-steady surface fire in homogeneous fuel bed.
- **Assumptions:** homogeneous fuel, steady wind/slope, surface (not crown) fire.
- **KNOWN WEAKNESSES:** heterogeneous fuels, spotting, crowning, transient wind → large errors; many hard-to-
  measure fuel parameters. → used as a SIMULATOR / prior for the geo/wildfire side; elliptical/Huygens or
  level-set spread for front propagation (candidate, see model_set_decision).

### EF-12 — Plume mass entrainment (Zukoski) — supporting relation
- **Statement:** entrained mass flux $\dot m(z) \propto \dot Q_c^{1/3} (z-z_0)^{5/3}$ (self-similar
  entrainment) [coeff-verify].
- **Source:** Zukoski; SFPE Handbook. **Validity/assumptions:** as EF-03.
- **KNOWN WEAKNESSES:** same far-field/still-air limits. → supports smoke-filling / sensor-concentration
  transport estimates (links EF-02→EF-07 at a sensor).

---

## Phenomena coverage map (recovered originals + literature-added)
| Phenomenon (recovered original) | Class-A model(s) |
|---|---|
| Plume dynamics | EF-03, EF-04, EF-12 |
| Flame geometry & flicker | EF-01, EF-08 |
| Smoke optics + camera radiometry | EF-07, EF-09 |
| Heat transfer / thermal signature | EF-06, EF-09 |
| Smoke/gas transport to a sensor | EF-05, EF-12 (+EF-10 for the sensor) |
| Fire growth | EF-02 |
| Spread dynamics | EF-11 (+ elliptical/level-set candidate) |
| Sensor-response physics | EF-10 |

## Cross-cutting known weaknesses in OUR setting (drive Layer-2)
1. Source strength/geometry ($\dot Q, D, z_0$) is UNKNOWN from passive sensing → need uncertainty/prior/
   dimensionless formulations (B-02).
2. Cheap sensors add lag ($\tau$), noise, drift NOT in the ideal models → sensor-response coupling (B-06).
3. Cameras measure pixels through smoke at low res/fps → projection + extinction + aliasing coupling
   (B-01, B-05).
4. Outdoor wind / non-ideal rooms violate still-air axisymmetric assumptions → regime flags + fallback.
These become the Layer-2 extension targets in formula_class_table.md / model_set_decision.md (next step).
