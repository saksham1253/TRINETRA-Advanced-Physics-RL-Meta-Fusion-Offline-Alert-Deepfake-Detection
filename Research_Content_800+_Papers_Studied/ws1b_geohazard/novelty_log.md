# ws1b_geohazard/novelty_log.md — novelty & prior-art log (Rule 21, P7G)

Phase P7G · WS1b · RESEARCH-ONLY. Rule 21: search prior art before any novelty claim; prefer "honest
recombination of known results" over novelty. HONEST TOOLING NOTE (§0.5): web_search had no API key in this
window; prior-art search via arXiv API + the P7G quota reading + established geo-hazard references. Weaker
than a full Scholar/patent sweep → "closest prior art" is best-effort, not exhaustive. NONE of the five
extensions is claimed novel.

## Position
All five Layer-2 geo-hazard extensions are explicit RECOMBINATIONS of established geotechnical/hydrological
relations with standard uncertainty/sensor-physics treatments, each reducing to a published parent. No
invention claimed.

## Per-extension prior-art record
- **GB-01 probabilistic infinite-slope** — Closest prior art: probabilistic slope stability / reliability
  analysis (FORM/FOSM; e.g. SINMAP, probabilistic TRIGRS) is a MATURE field. Novelty: NONE; GB-01 is the
  textbook reliability treatment of GH-01, packaged to consume a cheap moisture sensor's state. → APPLICATION.
- **GB-02 sensor-corrected pore-pressure** — Closest prior art: piezometer time-lag (Hvorslev) theory +
  deconvolution are standard instrumentation practice; combining with Iverson's response is routine. Novelty:
  NONE. → RECOMBINATION.
- **GB-03 antecedent-aware probabilistic rainfall threshold** — Closest prior art: antecedent-rainfall /
  hydro-meteorological thresholds and probabilistic/Bayesian landslide thresholds are an active literature
  (quota reads). Novelty: NONE claimed; GB-03 recombines the ID power law + an antecedent-moisture term + a
  logistic/decision-curve, all established. → RECOMBINATION.
- **GB-04 AMC-corrected SCS-CN** — Closest prior art: continuous-AMC and variable-λ (initial-abstraction
  ratio) CN modifications are well published (the 0.2 ratio debate is decades old). Novelty: NONE. →
  RECOMBINATION.
- **GB-05 hysteresis-corrected rating** — Closest prior art: the Jones formula (1916) IS the classical
  unsteady-flow loop-rating correction. Novelty: NONE; GB-05 is Jones applied to a cheap stage sensor. →
  APPLICATION of a >100-year-old result.

## Class C
GC-01 (Scheidegger/Voellmy runout), GC-02 (Saint-Venant/Muskingum routing), GC-03 (GLOF breach→routing) are
standard in the geomorphology/hydraulics literatures; no novelty claimed; documentation-only.

## Deliberately NOT pursued (prior-art-informed)
Live on-device Richards/Saint-Venant PDE solvers and full distributed physically-based models are rejected
for the node (compute/parameter-hungry); kept offline — consistent with P7's fire-PINN rejection and the
PINN-failure-mode evidence.

## Residual risk (honest)
web_search unavailable → a non-arXiv paper/patent could pre-empt a recombination; since we claim NO novelty,
this only confirms the "not new" stance. A full Scholar/patent sweep is an open action for the write-up.
