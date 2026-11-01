# ws1b_geohazard/established_formula_inventory.md — Layer 1 (Class A) geo-hazard models

Phase P7G · WS1b · RESEARCH-ONLY (paper derivations; no code/field work). Established geomorphology/
hydrology relations for Himalayan rainfall-triggered landslides, debris flows, flash floods, and GLOFs.
For each: statement, symbols/units, source, regime of validity, assumptions, and KNOWN WEAKNESSES in OUR
setting (unknown soil/geotech parameters; cheap noisy drifting sensors; ungauged catchments; extreme/non-
stationary monsoon rainfall; data scarcity). Coefficients from established references are tagged
[coeff-verify] and require a geotechnical/hydrology expert review before any external use (Rule 16: no
own-system performance claims; all numbers are source-reported). HONESTY: web_search had no API key in the
P5–P7 window; classic geo-hazard relations were sourced from established references and the P7G quota
reading (arXiv-only) — primary-source coefficient confirmation is an open action carried to the gate.

## Hazard → phenomenon → model coverage map
- Landslide initiation: rainfall ID threshold (GH-05) → infiltration (GH-03/GH-04) → pore pressure
  (GH-02) → slope stability (GH-01).
- Debris-flow runout: initiation (GH-02 + sediment) → mobility/reach (GH-06 Scheidegger, GH-07 Voellmy).
- Flash flood: rainfall → runoff (GH-08 SCS-CN) → channel flow (GH-09 Manning) → routing (GH-10 Saint-
  Venant / GH-11 Muskingum) → stage (GH-12 rating curve).
- GLOF: moraine/ice-dam breach (GH-13 peak-discharge regression) → routing (GH-10/11) → downstream stage.

---

### GH-01 Infinite-slope factor of safety  [CLASS A]
FS = [c' + (γ − m·γ_w)·z·cos²β·tanφ'] / [γ·z·sinβ·cosβ]
Symbols: c' effective cohesion [Pa]; γ soil unit weight [N/m³]; γ_w water unit weight [N/m³]; m wetness
ratio (saturated fraction of z) [-]; z failure depth [m]; β slope angle [rad]; φ' effective friction
angle [rad]. Source: standard geotechnics (Skempton/Taylor lineage) [coeff-verify].
Regime: planar failure, slope-parallel seepage, z ≪ slope length, cohesionless-to-cohesive soils.
Assumptions: 1-D, steady seepage, homogeneous soil, failure plane ∥ slope.
KNOWN WEAKNESSES (ours): c',φ',γ,z are rarely known in ungauged Himalayan slopes → huge parameter
uncertainty; ignores 3-D effects, root cohesion, suction in unsaturated soil; m is exactly what a cheap
soil-moisture/piezometer node must estimate (noisy). → Layer-2 hook: propagate parameter uncertainty to a
PROBABILITY of FS<1, not a point FS.

### GH-02 Iverson (2000) transient pore-pressure head  [CLASS A/B]
Slope enters via D₁ = D₀/cos²δ (hydraulic diffusivity along bedding); pressure-head response ψ(Z,t) to a
rainfall pulse I_Z/K_s via the 1-D linearized Richards (diffusion) solution with the response function
R(t*) (error-function form). Symbols: Z vertical depth [m]; t time [s]; D₀ diffusivity [m²/s]; δ slope
[rad]; I_Z surface flux [m/s]; K_s sat. hydraulic conductivity [m/s]. Source: Iverson 2000 WRR [coeff-verify].
Regime: wet initial conditions, tension-saturated response, event timescale. Assumptions: linearized
Richards, near-saturation, 1-D vertical.
KNOWN WEAKNESSES (ours): needs D₀,K_s (unknown, span orders of magnitude); linearization fails for very
dry soils / macropore flow; monsoon antecedent moisture violates assumed initial state. → Layer-2 hook:
sensor-response-corrected pore-pressure estimate + uncertainty from a piezometer/soil-moisture node.

### GH-03 Richards equation (unsaturated flow)  [CLASS A]
∂θ/∂t = ∂/∂z[ K(ψ)(∂ψ/∂z + 1) ], with van Genuchten θ(ψ), K(ψ). Symbols: θ volumetric water content [-];
ψ pressure head [m]; K hydraulic conductivity [m/s]. Source: Richards 1931; van Genuchten 1980 [coeff-verify].
Regime: variably-saturated porous media. Assumptions: Darcy–Buckingham, continuum, no hysteresis (usually).
KNOWN WEAKNESSES (ours): strongly nonlinear/stiff; parameters (α,n,K_s,θ_r,θ_s) scarce; macropores/
preferential flow unmodeled; expensive to solve on-device → used as a reference, not a live node model.

### GH-04 Green–Ampt infiltration  [CLASS A/B]
f(t) = K_s[1 + (Δθ·ψ_f)/F(t)]; cumulative F(t) implicit. Symbols: f infiltration rate [m/s]; F cumulative
infiltration [m]; ψ_f wetting-front suction [m]; Δθ moisture deficit [-]. Source: Green & Ampt 1911
[coeff-verify]. Regime: ponded/near-ponded, sharp wetting front. Assumptions: piston flow, homogeneous soil.
KNOWN WEAKNESSES (ours): sharp-front idealization; parameter scarcity; a cheaper proxy than full Richards
for a node, but still needs K_s,ψ_f,Δθ. → Layer-2 hook: event-rainfall → infiltration proxy feeding GH-05.

### GH-05 Rainfall intensity–duration (ID) threshold  [CLASS B]
I = α·D^(−β)  (critical mean intensity I [mm/h] vs duration D [h]; α,β empirical, region-specific).
Source: Caine 1980 and successors (regional/global ID thresholds) [coeff-verify]. Regime: shallow rainfall-
triggered landslides. Assumptions: rainfall is the dominant trigger; threshold calibrated to local inventory.
KNOWN WEAKNESSES (ours): α,β vary hugely by region/geology; ignores antecedent moisture → high false-alarm
and missed rates (source-reported); needs a local landslide inventory to calibrate; non-stationary monsoon
shifts the threshold. → Layer-2 hook: antecedent-moisture-/return-period-aware probabilistic threshold with
explicit false-alarm vs lead-time trade (decision-curve, not a single line).

### GH-06 Scheidegger angle of reach (debris-flow mobility)  [CLASS B]
H/L = tan(α_reach) = f·V^(−g)  (empirical: ratio of drop height H to runout length L decreases with volume
V). log(H/L) = a + b·log V. Source: Scheidegger 1973; Corominas 1996 [coeff-verify]. Regime: landslide/
debris-flow runout mobility screening. Assumptions: lumped friction, volume-dependent mobility.
KNOWN WEAKNESSES (ours): purely empirical, large scatter; volume V poorly known a priori; no flow dynamics/
timing. → Layer-2 hook: uncertainty-banded reach estimate (prob. a point is within runout) as a hazard-zone
prior, not a deterministic line.

### GH-07 Voellmy–Salm debris-flow / avalanche rheology  [CLASS A/B]
τ = μ·σ + ρ·g·v²/ξ  (basal shear = Coulomb friction μ·normal stress + turbulent/velocity term with ξ).
Symbols: μ Coulomb coefficient [-]; ξ turbulence coefficient [m/s²]; v depth-averaged velocity [m/s].
Source: Voellmy 1955; Salm 1993 [coeff-verify]. Regime: dense granular/debris flow runout dynamics.
Assumptions: depth-averaged (shallow-flow), lumped two-parameter rheology.
KNOWN WEAKNESSES (ours): μ,ξ are back-calculated/calibration parameters (not measurable); 2-parameter
rheology oversimplifies real debris; needs a DEM + solver → offline simulator, not a node model (Class C
coupling in model_set_decision).

### GH-08 SCS Curve-Number runoff  [CLASS B]
Q = (P − 0.2S)² / (P + 0.8S),  S = 25400/CN − 254 [mm]  (for P > 0.2S, else Q=0). Symbols: Q runoff depth
[mm]; P event rainfall [mm]; S potential retention [mm]; CN curve number [-] (soil+land-use+AMC). Source:
USDA-SCS/NRCS [coeff-verify]. Regime: event rainfall-runoff for small ungauged catchments. Assumptions:
initial abstraction = 0.2S; lumped CN; event-scale.
KNOWN WEAKNESSES (ours): the 0.2 initial-abstraction ratio is widely disputed; CN depends on antecedent
moisture (AMC I/II/III) → large swings; empirical, no explicit infiltration physics; non-stationary land
use. → Layer-2 hook: antecedent-moisture-corrected CN (sensor-informed AMC) + λ (abstraction ratio) as an
uncertain parameter.

### GH-09 Manning open-channel flow  [CLASS A/B]
v = (1/n)·R_h^(2/3)·S_f^(1/2);  Q = v·A. Symbols: v velocity [m/s]; n Manning roughness [s·m^(−1/3)];
R_h hydraulic radius [m]; S_f friction slope [-]; A area [m²]. Source: Manning 1891 / Gauckler–Strickler
[coeff-verify]. Regime: steady uniform turbulent open-channel flow. Assumptions: uniform flow, n constant,
rigid boundary.
KNOWN WEAKNESSES (ours): n uncertain and stage-dependent; assumes uniform flow (violated in steep
Himalayan torrents); sediment/debris change geometry. → Layer-2 hook: stage→discharge with an uncertain n
and hysteresis correction (pairs with GH-12).

### GH-10 Saint-Venant equations (1-D unsteady open-channel)  [CLASS A]
Continuity ∂A/∂t + ∂Q/∂x = q; Momentum ∂Q/∂t + ∂(Q²/A)/∂x + gA(∂h/∂x − S₀ + S_f) = 0. Source: de Saint-
Venant 1871. Regime: 1-D gradually-varied unsteady flow / flood routing. Assumptions: hydrostatic pressure,
small slope, 1-D.
KNOWN WEAKNESSES (ours): needs full geometry + solver (not a node model → offline/gateway); steep-slope and
supercritical Himalayan flows strain the shallow-water assumptions; boundary data scarce. → Class C routing
simulator.

### GH-11 Muskingum flood routing  [CLASS B]
O₂ = C₀I₂ + C₁I₁ + C₂O₁, with C's from K (storage time [h]) and X (weighting [-]). Source: McCarthy 1938
[coeff-verify]. Regime: lumped reach routing. Assumptions: linear storage S = K[XI + (1−X)O].
KNOWN WEAKNESSES (ours): K,X need calibration data (ungauged problem); linear storage; no backwater. →
Layer-2 hook: a cheap lumped lead-time/routing estimator with uncertainty for warning time, falling back to
this parent.

### GH-12 Stage–discharge rating curve  [CLASS B]
Q = a·(h − h₀)^b  (power-law rating). Source: standard hydrometry [coeff-verify]. Regime: a gauged section.
Assumptions: stable control, single-valued rating. KNOWN WEAKNESSES (ours): loop/hysteresis in unsteady
flow; shifting bed in Himalayan rivers breaks the rating; extrapolation beyond gauged range unreliable. →
Layer-2 hook: hysteresis-corrected (loop) rating from a cheap stage sensor (B-type extension).

### GH-13 GLOF moraine/dam-breach peak discharge  [CLASS B]
Q_p = c·(V_w)^{p}·(h_b)^{q}  (empirical peak-outflow regressions on breach height h_b and stored water
volume V_w; e.g. Froehlich-type). Source: Froehlich 1995; GLOF review literature [coeff-verify]. Regime:
dam/moraine breach peak outflow screening. Assumptions: empirical, lumped breach.
KNOWN WEAKNESSES (ours): huge scatter (orders of magnitude); V_w,h_b from remote sensing uncertain; ice-
cored moraine physics differs from earthfill dams; very data-scarce in the Himalaya. → Layer-2 hook:
uncertainty-banded peak-discharge + lead-time estimate (prob. hydrograph) as an advisory screening prior.

---

## Cross-cutting weaknesses (apply to most of the set)
- Parameter scarcity + ungauged catchments → every model carries large, often unquantified uncertainty.
- Non-stationary monsoon / climate change shifts calibrated thresholds and ratings.
- Cheap sensors (soil-moisture, piezometer, tilt, stage) are noisy, drift, and need calibration (ties the
  low-cost geo-sensing reads) → the measured inputs (m, ψ, h) are themselves uncertain.
- Life-safety framing (Rule 19): outputs are ADVISORY early-warning telemetry for IMD/CWC/NDMA/state DMAs,
  never autonomous evacuation triggers; lead-time + uncertainty stated honestly.

## Layer-2 hooks summary (to be derived in derivations/)
GB-01 probabilistic infinite-slope (parent GH-01): P(FS<1) by propagating parameter + moisture uncertainty.
GB-02 sensor-corrected transient pore-pressure (parent GH-02): piezometer response + lag + uncertainty.
GB-03 antecedent-aware probabilistic rainfall threshold (parent GH-05): add soil-moisture state + decision
  curve (false-alarm vs lead-time).
GB-04 antecedent-moisture-corrected SCS-CN (parent GH-08): sensor-informed AMC + uncertain abstraction λ.
GB-05 hysteresis-corrected stage–discharge (parent GH-12): loop rating from a cheap stage sensor.
Class C: GC-01 Voellmy/Scheidegger runout simulator (parents GH-06/GH-07); GC-02 Saint-Venant/Muskingum
  routing simulator (parents GH-10/GH-11); GC-03 GLOF breach→routing chain (parent GH-13).
