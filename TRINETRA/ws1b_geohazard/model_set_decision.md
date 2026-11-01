# ws1b_geohazard/model_set_decision.md — geo-hazard model admission & N (P7G)

Phase P7G · WS1b · RESEARCH-ONLY. Which geo-hazard models the project uses, with reasons (Rule 20 classes),
N counted by evidence. No own-system performance claim (Rule 16). Life-safety framing (Rule 19): all outputs
are ADVISORY early-warning telemetry for official agencies (IMD/CWC/NDMA/state DMAs), never autonomous
evacuation triggers.

## N (by evidence, not fixed)
- Layer 1 (Class A/A-B) admitted: **13** (GH-01..GH-13).
- Layer 2 (Class B) admitted: **5** (GB-01 probabilistic FS, GB-02 sensor-corrected pore-pressure, GB-03
  antecedent-aware probabilistic rainfall threshold [CORE], GB-04 AMC-corrected SCS-CN, GB-05 hysteresis
  rating). All reduce to parent; independently re-derived (0 errors).
- Layer 2 (Class C, documentation-only): **3** (GC-01 debris-flow runout sim, GC-02 flood routing sim,
  GC-03 GLOF breach→routing chain).

## Admission reasoning
- GH-01/GH-02 + GB-01/GB-02: the landslide-initiation core; cheap nodes measure moisture/pore-pressure →
  slope stability. Admitted because sensors directly inform the inputs; uncertainty handling (GB-01/02) is
  the honest form.
- GH-05 + GB-03: the primary landslide EARLY-WARNING trigger (rainfall + antecedent moisture → probability
  + decision curve). Admitted as the headline advisory model.
- GH-08 + GB-04, GH-09, GH-12 + GB-05: flash-flood runoff + stage/discharge from cheap rain + stage sensors.
  Admitted for flood lead-time.
- GH-03/GH-04 (Richards/Green-Ampt): admitted as REFERENCE infiltration physics (GH-04 as a node-feasible
  proxy; GH-03 as the reference), not as a live on-device solver.
- GH-06/GH-07/GH-10/GH-11/GH-13 → GC-01/GC-02/GC-03: admitted as OFFLINE simulators / advisory screening
  (DEM + solver + remote-sensing inputs), explicitly NOT live node models.

## Rejected / parked for deployment
- Live on-device Richards/Saint-Venant PDE solver: REJECTED for the node (stiff, parameter-hungry, compute-
  heavy) — same deployment logic as P7's fire-PINN rejection; keep as offline/gateway reference.
- Full physically-based distributed landslide model (e.g. TRIGRS grid) live on-node: parked (gateway/server
  only); the node runs the lightweight GB-01/GB-03 forms.
- Deterministic single-line thresholds / single-valued ratings as FINAL outputs: demoted — kept only as the
  fallback parents behind the probabilistic extensions.

## How the set enters the learning/alerting system
As FEATURES / PRIORS / CONSISTENCY-CHECKS with fallback-to-parent, never hard constraints:
- GB-03 trigger probability + GB-01 P(FS<1) → landslide alert decision layer (P12) with uncertainty + lead
  time.
- GB-02 pore-pressure state → feeds GB-01.
- GB-04 runoff + GB-05 discharge → flood lead-time estimate.
- GC-01/02/03 → offline hazard-zone maps / scenario hydrographs informing thresholds and siting.
- All feed meta-fusion (P14) which can down-weight a model when its inputs are out-of-regime.

## Expert-review & data flags (honest)
Every coefficient inherits [coeff-verify]; a geotechnical + hydrology expert must review before external
use. Thresholds (GB-03) and ratings (GB-05) REQUIRE a local landslide inventory + rainfall/discharge records
to calibrate — ungauged Himalayan catchments are the central data risk (validation_plan.md). web_search had
no API key; classic relations sourced from established references + arXiv-only quota reading.
