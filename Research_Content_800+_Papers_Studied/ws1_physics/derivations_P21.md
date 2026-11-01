# ws1_physics/derivations_P21.md — NOVEL fire-physics derivations (Class C), P21 deep-dive

Phase P21 · RESEARCH-ONLY · WS1a (fire). SEVEN novel derivations authored for this program, each targeting a
DOCUMENTED failure of a classical correlation for low-cost CCTV + cheap IoT sensing. HONESTY (Rule 20/21,
§0.5): **ALL CLASS C — novel hypotheses, UNVALIDATED, NOT results.** Novelty is a SEARCH CLAIM under a LIMITED
search (no web_search; arXiv-abstract-level; see novelty_log_P21.md). Built from Class-A established blocks
(EF-01…EF-12 in established_formula_inventory.md) + stated assumptions. NOTHING built/measured; no performance
claimed (Rule 16). Fire-science/heat-transfer EXPERT REVIEW required before any external use; coefficients
tagged [coeff-verify]. Each enters the system as a SOFT feature/prior with fallback to its Class-A parent, never
a hard dependency; all outputs ADVISORY (Rule 19).

Grounding literature (SOURCE-REPORTED, P21 readers): ADR/plume PINN 1910.09098; radiative transfer PINN
2009.13291/2307.05602; sensor-response physics 2605.23971/2607.18544; wildfire DA/level-set 0709.0086/
2206.08501/2212.00970; neural-operator ADR 2207.05748; stochastic CA spread 2606.11676.

Notation: T ambient T∞; plume temp rise ΔT; heat-release-rate Q̇; convective fraction χ_c; flame height L;
pixel height h_px; smoke optical depth κ_s·ℓ (Beer–Lambert); puffing frequency f_p; sampling rate f_s.

---
## ND-1 — Dealiased low-fps flicker-energy estimator  (parent EF-08 flame flicker; extends B-05)
- FAILURE TARGETED: CCTV at f_s ≈ 1–15 fps undersamples the 1.5–5 Hz puffing band → the flicker feature
  aliases to a wrong frequency and is unusable for flame-vs-nuisance discrimination.
- ASSUMPTIONS: puffing is quasi-periodic with a Strouhal relation f_p ≈ St·√(g/D) (St source-reported
  ~0.5·(g/D)^{1/2} scaling, [coeff-verify]); aliased frequency f_a = |f_p − f_s·round(f_p/f_s)|.
- DERIVATION (novel): given a candidate fire diameter prior D (from EF-01 flame-height/area geometry), predict
  the TRUE band [f_lo,f_hi] via the Strouhal relation, map it through the known aliasing fold for f_s to a
  predicted aliased band, and score the observed low-fps spectral energy INSIDE that predicted aliased band
  (matched filter), rather than reading the apparent peak. Output: FLK = (energy in predicted-aliased band) /
  (total band energy) ∈ [0,1]. A multi-rate check (if two cameras at different f_s) further disambiguates by
  requiring the inferred f_p to be consistent across both fold maps.
- USE: flame-vs-nuisance feature robust to frame rate; a c_i contributor (physics consistency) for fusion.
- VALIDATION: on labelled flame/nuisance clips at several f_s, test FLK separability vs the naive peak feature
  (inferential-reproducibility gate 2302.04054). Class C. Expert: combustion/fluid dynamics + signal.

## ND-2 — Smoke-transmittance-compensated apparent-temperature  (parents EF-07 extinction, EF-05 gas law, B-06)
- FAILURE TARGETED: an IR/visible pixel over a plume is dimmed by intervening smoke → apparent radiometric
  temperature underestimates true plume ΔT, worst exactly for diffuse smouldering fires (where INT8 PTQ also
  hurts recall, P18 2506.09300).
- ASSUMPTIONS: Beer–Lambert transmittance τ_s = exp(−κ_s ℓ) (EF-07); grey-body plume; sensor lag model (B-06).
- DERIVATION (novel coupling): observed radiance L_obs = τ_s·L_plume + (1−τ_s)·L_smoke. Solve for L_plume with
  an uncertainty prior on κ_s ℓ from the smoke-vs-steam extinction feature (B-01 lineage), then invert the
  (lagged, noisy) sensor response (B-06) to the true ΔT with propagated variance. Output: T̂_plume ± σ, with a
  reliability flag that widens σ as τ_s→0 (opaque smoke ⇒ "uncertain", never a false low-temp "all-clear").
- USE: temperature feature + a physics-residual input (ND-4); fuses with rate-of-rise timing.
- VALIDATION: against thermocouple-labelled smoke-obscured sequences; check σ grows with optical depth. Class
  C. Expert: radiometry/heat-transfer.

## ND-3 — Dimensionless early-ignition index  Π_ig  (parents EF-03/EF-05 plume+gas, scaling analysis)
- FAILURE TARGETED: raw dT/dt and gas slopes are scene/scale dependent → thresholds don't transfer across
  sites (cross-site generalization, a program-wide theme).
- ASSUMPTIONS: near-field incipient plume; signals from a co-located node (temp, gas e.g. CO/VOC, optional
  radiative flux). Use buoyancy scaling (characteristic time t* ~ (D/g)^{1/2}, temperature scale ΔT* from the
  Q̇*-dimensionless plume, EF-03).
- DERIVATION (novel dimensionless group): combine the three normalized rates into a single scene-invariant
  scalar Π_ig = w1·(t*/ΔT*)·(dT/dt) + w2·(t*/C*)·(dC/dt) + w3·(t*/Ṁ*)·(dq''_rad/dt), each term made
  dimensionless by its buoyancy scale so the SAME threshold applies across sites; w fixed by physical
  dimensional priors, not fitted-to-benchmark. Π_ig is monotone in incipient-fire intensity by construction.
- USE: a transferable early-warning scalar; a strong c_i/feature for fusion; fail-open when scales unknown.
- VALIDATION: cross-SITE threshold transfer test (spatial-block, 2608.22293): does ONE Π_ig threshold hold
  across sites better than raw-rate thresholds? Class C. Expert: fire dynamics + dimensional analysis.

## ND-4 — Physics-residual consistency score  r_phys  (parents EF-03/EF-04 plume + ceiling-jet transport)
- FAILURE TARGETED: anomaly/detector scores have no notion of physical plausibility → confident but physically
  impossible detections (bridges to the P22 fusion c_i and the WS8 anomaly head).
- ASSUMPTIONS: a forward physics-gate prediction ŝ_phys(t) of the expected multi-sensor signal given a
  hypothesized incipient fire (plume rise EF-03/04 + ceiling-jet transport delay + sensor lag B-06).
- DERIVATION (novel bridge): r_phys = exp( − ‖s_obs(t) − ŝ_phys(t)‖²_Σ / 2 ), a Mahalanobis-normalized residual
  under the physics-gate covariance Σ (which includes model uncertainty so Class-B/C physics is NOT treated as
  truth). High r_phys ⇒ the observation is consistent with fire physics; low ⇒ down-weight. Feeds c_i in the
  PHARAOH operator (P22) and is logged for explainability.
- USE: physics-consistency gate for fusion; rejects physically-impossible spikes without silencing fast fires
  (physics also predicts fast onset).
- VALIDATION: does r_phys discount nuisance events while preserving true fires on held-out cross-site data?
  Class C. Expert: fire dynamics + statistics.

## ND-5 — Wind-tilt-corrected camera flame height  (parent B-01 apparent height, + crosswind plume lean)
- FAILURE TARGETED: wind tilts the flame/plume → the vertical pixel height underestimates the true flame
  length, corrupting B-01 range/size reasoning (wind-driven regime, a known classical-correlation breakdown).
- ASSUMPTIONS: crosswind U; plume lean angle θ from a buoyancy-vs-momentum balance (Froude-number scaling,
  tan θ ≈ f(U/√(gL)) [coeff-verify]); camera geometry known (EF-09 range reasoning lineage).
- DERIVATION (novel extension): correct apparent height h_px to a flame LENGTH along the tilted axis:
  L̂ = h_px / (cos θ · m(range)), with θ estimated from the observed plume-drift direction (optical flow) and
  the wind prior; propagate uncertainty on U,θ. Output L̂ ± σ feeding size/HRR priors.
- USE: wind-robust size/range feature; improves ND-3 scale estimates under wind.
- VALIDATION: against known-size wind-tunnel/field flames; check error vs wind speed. Class C. Expert: fluid
  dynamics + photogrammetry.

## ND-6 — Radiative–convective regime scalar  Ξ_rc  (dimensionless gate for correlation/sensor selection)
- FAILURE TARGETED: Heskestad vs McCaffrey plume correlations fit DIFFERENT regimes; blindly applying one
  degrades estimates. Also sensor weighting should differ in radiation- vs convection-dominated fires.
- ASSUMPTIONS: estimable radiative flux q''_rad (IR) and convective enthalpy flux ~ ṁ·c_p·ΔT (from plume).
- DERIVATION (novel gating scalar): Ξ_rc = q''_rad·A / (ṁ c_p ΔT) — a modified radiation-to-convection ratio
  (a Boltzmann/Stefan-number-like group). Ξ_rc large ⇒ radiation-dominated (weight IR/flux features, use the
  far-field correlation); small ⇒ convection-dominated (weight temperature/rate features). Ξ_rc chooses the
  plume correlation and sets physics-informed sensor weights for fusion (a c_i/weight contributor).
- USE: physics-informed modality gating (feeds FM-5 physics-biased MoE gate in P22).
- VALIDATION: does regime-gated correlation selection beat fixed-correlation on mixed-regime held-out data?
  Class C. Expert: combustion/heat-transfer.

## ND-7 — Advection-consistent spatial-coherence fire likelihood  (parent ADR transport; multi-node)
- FAILURE TARGETED: a single node's spike is easily spurious; real fires produce spatially-correlated,
  WIND-ADVECTED signatures across neighbouring nodes/cameras — unused by per-node detectors.
- ASSUMPTIONS: a sensor network with known relative positions; local wind vector prior; advection–diffusion
  transport of heat/smoke/gas (ADR, 1910.09098/2207.05748 grounding).
- DERIVATION (novel): predict the expected arrival-time lag Δt_ij ≈ d_ij·cos(angle to wind)/U between nodes i,j
  from advection, and score the observed cross-node signal correlation at those PHYSICALLY-PREDICTED lags:
  COH = Σ_{i<j} ρ_ij(Δt_ij) weighted by node reliability. A real advected plume maximizes COH at the physical
  lags; uncorrelated spurious spikes do not. Output COH ∈ [0,1] as a corroboration prior.
- USE: network-level corroboration prior (ties P16 cross-sensor corroboration + P22 fusion); strongly rejects
  isolated false positives without suppressing genuine spreading events.
- VALIDATION: on multi-node replay, does COH separate advected real events from independent nuisance spikes?
  Class C. Expert: dispersion modelling + sensor networks.

---
## Honest limitations (all ND)
Every ND is a DESIGN with unfit coefficients/weights and depends on uncertain Class-A/B inputs (D, U, κ_s ℓ, Σ,
scales); none is validated or claimed to work or to beat anything; dimensionless groups (Π_ig, Ξ_rc) assume the
cited buoyancy scalings hold in our regimes ([coeff-verify]); multi-node ND-7 needs synchronized nodes + a wind
prior. CLASS C throughout. Fire-science EXPERT REVIEW mandatory. These enter only as soft features/priors with
Class-A fallback; the system stays advisory and human-in-the-loop.
