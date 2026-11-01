# ws1_physics/advanced_analysis_P21.md — PhD-level synthesis: where classical fire correlations break, and what advanced modeling offers

Phase P21 · RESEARCH-ONLY. Synthesis of the 55 P21 papers (SOURCE-REPORTED). Purpose: justify the Class-C
derivations (derivations_P21.md) by naming the exact regimes where the P7 Class-A correlations fail and what
the advanced literature provides. Nothing built/measured; no performance claimed.

## 1. Where the classical correlations break (and the derivation that targets it)
- LOW TEMPORAL SAMPLING: puffing/flicker theory (Strouhal/G-equation; 2609.09773, 2208.03542) assumes adequate
  sampling; CCTV at 1–15 fps aliases the 1.5–5 Hz band. → ND-1 dealiased flicker estimator.
- SMOKE OBSCURATION: radiometric temperature readings are corrupted by intervening smoke (non-gray soot
  radiation lowers apparent temperature, 2102.11060; RTE solvers 2009.13291/2307.05602). → ND-2 transmittance
  compensation.
- SCALE/SITE DEPENDENCE: raw rate thresholds don't transfer; buoyancy scaling (modified Byram/Froude,
  2501.08343/2406.08589) gives dimensionless invariants. → ND-3 dimensionless early-ignition index.
- NO PHYSICAL PLAUSIBILITY CHECK on detector/anomaly scores. → ND-4 physics-residual consistency score.
- WIND/SHEAR TILT: plume bending in sheared/canopy flow (2510.13196/2510.14423/2510.13189) violates the
  vertical-flame-height assumption. → ND-5 wind-tilt-corrected flame height.
- REGIME CONFUSION: radiation- vs convection-driven fires need different correlations (critical Froude number,
  FireBench 2406.08589). → ND-6 radiative–convective regime scalar.
- SINGLE-POINT SPURIOUSNESS: real plumes advect across space (ADR; ember/plume transport 2206.01529). → ND-7
  advection-consistent spatial coherence.

## 2. What the advanced toolbox offers (and how we use it — offline, not deployed)
- PINNs / neural operators (DeepONet/FNO; 2207.05748, 2505.23190): PDE surrogates for plume/ADR/RTE → OFFLINE
  synthetic-data generation + fast priors; NOT an on-device solver (P7 PINN-deployment rejection stands;
  PINN failure modes still apply).
- Data assimilation (EnKF 0709.0086, Bayesian filtering level-set 2206.08501, Fire-EnSF 2510.15954, B-PINN
  2212.00970, cWGAN arrival-time 2309.02615/2506.10404): the principled way to fuse a physics model with
  sparse sensor data → informs the P22 fusion design (physics prior + residual), offline for the wildfire side.
- ROM / operator inference (1908.03620, 2008.02862): >5-order speedups → feasible offline simulators for
  training-data augmentation.
- Stochastic/CA spread (2606.11676, 2603.26975): probabilistic spread with UQ → scenario generation + the C-01
  simulator option, never a live hard dependency.
- Sensor-response physics (2605.23971, 2607.18544): directly validates the B-06 lag model + ND-2 inversion.

## 3. Honest boundaries
Advanced methods are powerful but (i) data-hungry / compute-heavy (offline only for us), (ii) carry their own
failure modes (PINN stiffness/spectral bias; DA covariance mis-specification 2504.17900; manifold-constrained
inference failures 2503.11729), and (iii) are validated on THEIR data, not ours. They motivate and could later
VALIDATE the Class-C derivations; they do not make them results. Fire-science expert review required.
