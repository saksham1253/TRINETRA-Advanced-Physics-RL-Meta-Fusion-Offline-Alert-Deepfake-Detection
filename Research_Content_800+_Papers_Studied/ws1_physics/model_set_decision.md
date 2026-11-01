# ws1_physics/model_set_decision.md — admitted / demoted / rejected (with N and reasons)

Phase P7 · WS1a · RESEARCH-ONLY. Records the admission decision for every candidate physics model, its
class (Rule 20), and the reason. Principle (§P7 3(f)): keep the set as SMALL as the evidence allows and as
large as it usefully needs. Every admission is justified by relevance + usability by the system + a verified
source (Class A) or a full derivation from Class-A blocks + a validation route (Class B). Hard-honesty
(§0.5): no model is admitted on performance grounds (nothing is built); admission = "defensible, usable,
and validatable later", not "works".

## Count N
- **Layer 1 (Class A): 12** — EF-01…EF-12 (all established, verified-source, usable).
- **Layer 2 (Class B, admitted): 4** — B-01, B-02, B-05, B-06.
- **Layer 2 (Class C, documentation-only): 2** — C-01, C-02.
Counted separately per §P7 3(f). Total modelled relations tracked = 18.

## ADMITTED — Layer 1 (Class A)
All of EF-01…EF-12 are admitted. Reasons (shared): (1) relevant to detecting fire/smoke from CCTV + cheap
sensors; (2) usable as a baseline, feature, prior, consistency check, or simulator; (3) verified canonical
source exists. Each also serves as the PARENT/baseline that any extension must beat or match (else the
parent is used). Known weaknesses are documented in established_formula_inventory.md.
- Dual plume parents EF-03 (Heskestad) AND EF-04 (McCaffrey) are BOTH admitted deliberately: the later
  ablation (§P7 task 6) decides which fits our regime; keeping both is cheap and informative.

## ADMITTED — Layer 2 (Class B)
Each admitted because it (1) is built from verified Class-A blocks cited with equations, (2) yields a
system-usable quantity (feature/prior/consistency check/residual), (3) adds non-redundant information over
its parent, (4) has a validation plan naming real published data + a pre-registered build-phase gate vs the
parent, and (5) enters as a soft feature/prior with fallback to the parent (never a hard dependency until
validated).
- **B-06 Sensor-response-corrected signal (parent EF-05, EF-10, +EF-03).** Targets THE central weakness for
  our cheap-sensor node: the ideal gas temperature ≠ what a lagging, noisy sensor measures after ceiling-
  jet transport delay. Non-redundant: predicts the OBSERVED (lagged, delayed) signal, enabling correct
  rate-of-rise timing and delta features (P6). Highest-priority extension.
- **B-05 Aliasing-aware flicker band (parent EF-08).** Targets a concrete, documented failure: low-fps CCTV
  aliases the 1.5–5 Hz puffing band. Non-redundant: corrects the frequency feature for the camera sampling
  rate. Cheap video/IR feature for flame-vs-nuisance discrimination.
- **B-01 Camera apparent flame height through smoke (parents EF-01, EF-07, +EF-09).** Targets "pixels ≠
  physical flame height" + smoke obscuration. Non-redundant: links observable (pixel) quantities to the
  physical correlation with explicit uncertainty on unknown Q̇,D. Consistency-check feature.
- **B-02 Dimensionless/prior plume-temperature estimator (parent EF-03).** Targets unknown Q̇c, z0 and far-
  field noise. Non-redundant: produces a posterior/dimensionless estimate instead of requiring unknown
  inputs; propagates sensor noise. Prior/feature.

## DEMOTED to documentation-only (Class C)
- **C-01 Level-set/elliptical front propagation ∘ Rothermel (parent EF-11).** No realistic near-term
  validation (needs spatial fuel/wind fields unavailable at pilot). KEEP as a documented simulator option
  for the geo/wildfire side; not a live estimator.
- **C-02 Full coupled forward camera model (plume∘extinction∘radiometry).** Too many unknowns to invert
  live; retained as a SYNTHETIC-DATA SIMULATOR concept (generate labeled smoke/flame imagery), not an
  on-line model. Documentation-only.

## REJECTED (not carried)
- Full fire PINN as a deployed on-device solver — REJECTED for deployment: PINN failure modes (stiffness,
  loss-weight imbalance, spectral bias, causality violation, poor extrapolation, non-identifiability) make a
  live fire-PINN a research risk, not an ESP32 path. (Physics still enters as features/priors/consistency +
  as a synthetic-data simulator offline.) This is a scoping decision, not a claim PINNs cannot work.
- Pyrolysis/Arrhenius kinetics as a live model — NOT admitted now: not observable from our sensors/camera;
  parked (could re-enter if a fuel-specific pilot needs it). Logged, not rejected permanently.

## How the set enters the learning system (summary; details per derivation doc §(e))
- EF-02/EF-03/EF-04/EF-05/EF-12: features + synthetic-data simulators (zone/plume) + consistency checks.
- EF-06/EF-09 + B-01: radiometric/geometric features & range reasoning.
- EF-07 + B-01: smoke-vs-steam extinction feature.
- EF-08 + B-05: flicker-band feature (aliasing-corrected).
- EF-10 + B-06: sensor-response model → correct rate-of-rise timing + delta features on the IoT node (P6).
- EF-11 + C-01: wildfire spread simulator (offline).
All Class-B models enter as SOFT features/priors with their own uncertainty and a documented fallback to the
Class-A parent; none is a hard dependency until its build-phase validation gate is passed.

## Expert-review flag (Rule / §P7 3(e))
Every derivation (esp. Layer 2) must be reviewed by a qualified fire-science / heat-transfer expert before
any external use. Coefficients tagged [coeff-verify] in the inventory to be confirmed against primary
sources first.
