# ws1_physics/validation_plan.md — how each admitted model is validated LATER (named data)

Phase P7 · WS1a · RESEARCH-ONLY. Pre-registered validation plan. For every admitted model: the real
published data to validate against (or an HONEST statement that none exists), the metric, and the pre-
registered build-phase gate vs the parent/baseline. Nothing is validated now (no build); this is the plan.
§0.5: where no suitable public data exists, we say so rather than imply validation.

## Layer 1 (Class A) — validate the correlation reproduces its own published data
| Model | Validation data (named) | Metric | Honest status |
|-------|-------------------------|--------|---------------|
| EF-01 Heskestad L | Heskestad/Zukoski flame-height datasets; NIST pool/gas-burner | L vs $\dot Q,D$, rel. error vs ±10–20% band | data exist (lab); not re-fetched this session |
| EF-02 t² HRR | NIST Fire Calorimetry Database furniture/room HRR curves | $\alpha$-fit residual | data exist (NIST, public-domain; verify per-set) |
| EF-03 Heskestad plume | McCaffrey/Heskestad centerline $\Delta T,u$ data | collapse onto $g(\zeta)$ | data exist (lab) |
| EF-04 McCaffrey | McCaffrey 1979 NBS burner data | regime fit | data exist (NBS report) |
| EF-05 Alpert | Alpert 1972 + large-scale ceiling-fire tests | $\Delta T_{max},U_{max}$ error | data exist (lab) |
| EF-06 radiation | pool-fire radiometer flux-vs-distance | $\dot q''$ error, near/far split | data exist (lab) |
| EF-07 extinction | Mulholland mass-extinction measurements | $K_m$, $OD$ | data exist (lab) |
| EF-08 flicker | Cetegen & Ahmed / Hamins puffing-frequency data | $f$ vs $D$ | data exist (lab) |
| EF-09 radiometry | blackbody-calibration + atmospheric-transmission references | $T$ retrieval error vs ε,range | data exist (standard) |
| EF-10 RTI | plunge-test RTI datasets (Heskestad & Bill) | $\tau(u)$ | data exist (standard test) |
| EF-11 Rothermel | BehavePlus fuel-bed experiments; NIFC perimeters | ROS error | data exist (public US fire data) |
| EF-12 Zukoski entrainment | plume entrainment measurements | $\dot m$ vs $z$ | data exist (lab) |

## Layer 2 (Class B) — validate the EXTENSION beats/does-not-degrade the parent
| Model | Validation data | Metric | Pre-registered build gate vs parent |
|-------|-----------------|--------|-------------------------------------|
| B-06 sensor-response-corrected signal | Alpert ceiling-jet data + plunge-test $\tau$ + any fire-test detector traces | detector ACTIVATION-TIME error; trace fit (NLL) | must reduce activation-time error vs bare EF-05 (no-lag) on held-out tests |
| B-05 aliasing-aware flicker | Cetegen/Hamins puffing data **resampled at 10/15/25/30 fps**; flame vs matched-nuisance video | alias-map prediction error; flame/nuisance separation (AUC) | must beat raw-FFT-peak feature on held-out low-fps video |
| B-01 camera apparent flame height | lab flame-height video with measured $\dot Q,D$ (+ a smoke-obscuration case) | apparent-height prediction error; interval coverage | must beat EF-01+projection (no extinction) on obscured cases |
| B-02 dimensionless plume prior | Heskestad/McCaffrey centerline $\Delta T$ data | $g(\zeta)$-collapse residual; posterior interval COVERAGE vs nominal | calibrated coverage + sharper-than-prior where data informative |

## Class C (documentation-only) — honest "no live validation" statement
- C-01 (level-set/elliptical ∘ Rothermel): validatable only as an offline SIMULATOR against NIFC perimeters
  (e.g. Thomas/Haypress, Pacific Palisades burn scar per quota refs); NOT a live estimator at pilot → no
  on-line validation planned now.
- C-02 (full coupled forward camera model): used as a synthetic-data generator; "validation" = sim-to-real
  gap study only; no claim of live inversion.

## Data-gap honesty
- The classic fire-science datasets above EXIST in the literature but were NOT re-fetched/verified this
  session (arXiv had ~0 hits for the classic correlations; web_search unavailable). Portal fetch + license
  confirm for NIST FDS validation suite + Fire Calorimetry DB is an open action (carried to the gate; added
  to DATASETS.md as [D] discovery-only until verified).
- No public dataset is claimed to exist that we have not seen cited; the wildfire-spread datasets (NIFC
  perimeters, WRF-SFIRE sims, CSIRO SPARK cases) are named from the quota papers with license UNCONFIRMED.
