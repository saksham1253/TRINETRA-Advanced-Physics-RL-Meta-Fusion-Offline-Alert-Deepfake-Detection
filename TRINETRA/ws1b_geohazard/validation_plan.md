# ws1b_geohazard/validation_plan.md — geo-hazard validation plan (named data / honest gaps)

Phase P7G · WS1b · RESEARCH-ONLY. Pre-registered. For each admitted model: real public data to validate
against (or honest "none/ungauged"), metric, and the build-phase gate vs the parent. Nothing validated now.

## Layer 1
| Model | Validation data (named) | Metric | Honest status |
|-------|-------------------------|--------|---------------|
| GH-01 FS | slope-failure case studies w/ measured c',φ'; NASA Global Landslide Catalog locations | FS vs observed failure | lab/geotech data exist; site params scarce |
| GH-02 Iverson | Iverson 2000 / instrumented-slope pore-pressure records | ψ(Z,t) fit | published instrumented slopes exist |
| GH-03/04 infiltration | soil-column infiltration experiments (van Genuchten params) | θ,F(t) fit | lab data exist; Himalayan params scarce |
| GH-05 ID threshold | regional landslide inventory + rain gauges (e.g. GSI India; NASA GLC) | POD/POFD at the line | needs LOCAL inventory to calibrate |
| GH-06 Scheidegger | debris-flow runout inventories (H/L vs V) | reach-angle regression | inventories exist (scatter) |
| GH-07 Voellmy | back-analyzed debris-flow events | runout/velocity | calibration-only params |
| GH-08 SCS-CN | small-catchment rainfall-runoff events | NSE/bias | event data exist; CN local |
| GH-09 Manning | gauged channel reach measurements | v,Q vs ADCP | gauged sections |
| GH-10/11 routing | gauged flood hydrographs (CWC) | hydrograph NSE | gauged basins only |
| GH-12 rating | stage–discharge measurement sets | Q error | gauged sections |
| GH-13 GLOF | documented GLOF events (ICIMOD; Himalayan case studies) | peak-Q order of magnitude | very few events; huge scatter |

## Layer 2 (validate the extension beats/does-not-degrade parent)
| Model | Data | Metric | Pre-registered gate vs parent |
|-------|------|--------|-------------------------------|
| GB-01 P(FS<1) | landslide inventory + slope params | Brier / reliability / AUC | calibrated P_f, better net benefit than deterministic FS |
| GB-02 sensor-corrected ψ | lab step/plunge test + co-located reference piezometer | lag/bias reduction | beats raw sensor reading on step tests |
| GB-03 prob. threshold (CORE) | local landslide inventory + rainfall + soil-moisture | Brier / AUC / decision-curve net benefit | beats plain ID line in calibrated skill |
| GB-04 AMC-CN | event rainfall-runoff + soil-moisture | NSE / bias | beats fixed-CN AMC table |
| GB-05 Jones rating | loop-rating events + ADCP reference | limb-dependent bias | reduces rising/falling-limb bias vs single rating |

## Class C (honest "no live validation")
GC-01/GC-02/GC-03 validatable only as OFFLINE simulators against documented events (runout extent / flood
inundation / GLOF hydrograph), NOT as live estimators → no on-line validation planned; scenario/hazard-map
use only, with explicit uncertainty.

## Data-gap honesty (the central risk)
- The decisive datasets (local landslide inventory + co-located rainfall/soil-moisture, gauged discharge,
  loop-rating events, GLOF records) are SCARCE or ABSENT for ungauged Himalayan catchments. Where no local
  data exist, GB-03/GB-04/GB-05 CANNOT be validated and must ship as advisory-only with wide uncertainty —
  stated plainly, not papered over.
- Public portals named in DATASETS.md (NASA GLC, GSI, IMD/GPM/CHIRPS, SRTM/ALOS, ICIMOD, CWC) are [D]
  discovery-only until license/coverage are portal-verified (open action).
