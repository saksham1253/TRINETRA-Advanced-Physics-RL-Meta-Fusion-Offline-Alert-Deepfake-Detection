# PROGRAM/sota/P21_sota_scan.md — SOTA scan: fire-hazard physics deep-dive (P21)

RESEARCH NOTES. All numbers SOURCE-REPORTED (Rule 16), none ours. 55 NEW papers (readers A=27 fire-dynamics/
detection-physics, B=28 advanced/PhD modeling). IDs in the ledger + PHASE_21_report.md.

## 1. State of the art, by sub-area (source-reported) + the GAP each leaves for us
- PLUME in real conditions: LES + modified-Byram/Froude scaling now capture plume bending, canopy drag, and
  sheared-crossflow transitions (2501.08343, 2510.13196, 2510.14423, 2510.13189; critical-Froude delineation
  in FireBench 2406.08589). GAP: these are high-fidelity simulators, not on-device estimators — we need cheap
  features/priors distilled from them (motivates ND-3, ND-5, ND-6).
- SPREAD: fast operational fronts via conformal mapping (2408.06205) and Rothermel+Huygens on slopes
  (2412.18931); WRF-SFIRE validated but over-predicts vertical velocity >10 m (1206.3345). GAP: needs spatial
  fuel/wind fields → kept as an offline simulator (C-01), not a live estimator.
- FLICKER/PUFFING: G-equation describing-functions and swirl-regime transitions (2609.09773, 2202.06567);
  PINN velocity reconstruction from pool fires (2208.03542). GAP: all assume good temporal sampling — our CCTV
  undersamples (motivates ND-1 dealiased flicker).
- PYROLYSIS/KINETICS: CRNN/neural-ODE recover interpretable Arrhenius kinetics from TGA (2105.11397); PMMA
  multi-reaction still diverges at real scale (2303.17446); live-fuel burning phases (2203.04639). GAP: not
  observable from our sensors → parked (consistent with P7's reject of live Arrhenius).
- RADIATION/SOOT: non-gray WSGGM soot radiation lowers flame temperature (2102.11060); PINN/APINN and neural
  operators solve the RTE (2009.13291, 2307.05602, 2505.23190). GAP: motivates the smoke-transmittance
  compensation (ND-2) and the radiative-convective regime scalar (ND-6).
- FIREBRAND/EMBER: LES ember transport + wave-driven extreme spotting (2206.01529, 2411.13275); two-color
  pyrometry shows firebrand temp oscillations 50–480 Hz (2506.15891). GAP: beyond pilot sensing; documented.
- SENSOR PHYSICS: physics-descriptor gas-sensor inference (MAE~1.48 ppm, R²~0.992, 2605.23971) and Maxwell–
  Stefan graph solvers (2607.18544). GAP: directly supports B-06 + ND-2 sensor-lag correction.
- PHYSICS-INFORMED ML as the modern tool: PINN/neural-operator surrogates, data assimilation (Fire-EnSF
  2510.15954, cWGAN arrival-time 2309.02615/2506.10404, B-PINN level-set 2212.00970, EnKF wildfire 0709.0086),
  ROM (>5-order speedups 1908.03620/2008.02862), neural-param CA (2606.11676). GAP: these are the research-
  grade methods our Class-C derivations and offline simulators should adopt — NOT deployed solvers (P7 stands).

## 2. Net
The classical correlations (P7 Class-A EF-01…EF-12) remain the backbone; the SOTA is (a) high-fidelity
simulators and (b) physics-informed ML surrogates/assimilation. Our deployment path keeps physics as cheap
features/priors/consistency-checks + offline synthetic-data simulators, and adds the P21 Class-C derivations
(ND-1…ND-7) to patch the documented failure modes for low-fps CCTV + cheap sensors. All UNVALIDATED.

## 3. Honesty
Nothing measured; every number is a source paper's own result on its own data. Novel items are Class-C
hypotheses (novelty = limited-search claim). Expert review + [coeff-verify] required.
