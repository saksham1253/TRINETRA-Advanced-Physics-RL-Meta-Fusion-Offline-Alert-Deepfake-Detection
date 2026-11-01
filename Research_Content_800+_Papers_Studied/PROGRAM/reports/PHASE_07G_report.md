# PHASE_07G_report — WS1b GEO-HAZARD physics model set & derivations (RESEARCH-ONLY)

Phase P7G (NEW inserted phase; spec PROGRAM/PHASE_P7G_SPEC.md). Status: COMPLETE to gate (continuous mode —
completion record, not a halt). Paper derivations only; no code/live solver. No own-system performance
claim (Rule 16). Rule 19: all outputs ADVISORY early-warning for IMD/CWC/NDMA/state DMAs, never autonomous
evacuation triggers.

## Objective
Mirror P7's two-layer method for geo-hazards (landslide / debris-flow / flood / GLOF): established-formula
inventory (Layer 1, Class A), robustified extensions that reduce to parents (Layer 2, Class B), and
documentation-only simulators (Class C) — each with weaknesses, validation data, verification, novelty, and
a NEW literature quota.

## What was produced
- SOTA framing + inventory: ws1b_geohazard/established_formula_inventory.md (GH-01..GH-13).
- ws1b_geohazard/derivations/LAYER2_derivations.md — GB-01..GB-05 FULL derivations, each reducing to its
  parent; INDEPENDENTLY re-derived by a second agent (0 errors).
- ws1b_geohazard/formula_class_table.md (lineage/classes); model_set_decision.md (N = 13 Class-A + 5
  Class-B + 3 Class-C, by evidence); validation_plan.md; verification_checklists.md (+independent recheck);
  novelty_log.md (Rule 21 — no novelty claimed, honest recombinations).
- ws1b_geohazard/literature_map.md — 17 NEW primary arXiv papers (ABS) + 18 FT-REF reference-verifications.
- Equations register geo section (analysis/08) resolving the previously-pending seed; DATASETS D45-D54 ([D]);
  17 [P7G] ledger rows; Audit #15 PASS.

## Model set (Rule 20)
- Layer 1 (A/A-B), N=13: GH-01 infinite-slope FS, GH-02 Iverson pore-pressure, GH-03 Richards, GH-04
  Green–Ampt, GH-05 rainfall ID threshold, GH-06 Scheidegger reach angle, GH-07 Voellmy–Salm, GH-08 SCS-CN,
  GH-09 Manning, GH-10 Saint-Venant, GH-11 Muskingum, GH-12 stage–discharge, GH-13 GLOF breach peak-Q.
- Layer 2 (B), N=5: GB-01 probabilistic P(FS<1); GB-02 sensor-corrected pore-pressure (piezometer lag);
  **GB-03 antecedent-aware probabilistic rainfall threshold = CORE landslide EWS**; GB-04 AMC-corrected
  SCS-CN; GB-05 Jones hysteresis rating. Each reduces to its parent (verified).
- Layer 2 (C, doc-only), N=3: GC-01 debris-flow runout sim, GC-02 flood routing sim, GC-03 GLOF breach→
  routing chain.
- REJECTED for the node: live on-device Richards/Saint-Venant PDE solvers + full distributed physically-
  based models (compute/parameter-hungry) — kept offline/gateway, consistent with P7's fire-PINN rejection.

## Key literature findings (source-reported)
- Single deterministic rainfall I–D thresholds are unreliable (2106.15119) → GB-03 probabilistic form
  justified. TRIGRS reproduces I–D + size-frequency but needs dense per-cell params (1306.1529) → lightweight
  node forms + offline sims justified. Plain LSTMs extrapolate unphysically on extremes; physics-informed
  constraints stabilize them (2606.04143) → consistency-checked ML stance confirmed.
- GLOF monitoring must be multimodal/SAR to beat Himalayan cloud (2601.12330, 2512.24117 IoU 0.9130).
- Low-cost nowcasting feasible: radar U-Net runs on a standard computer in seconds (2607.16080); satellite-
  only DYffCast where no radar (2412.02723). Topology-aware routing helps UNGAUGED basins (2609.32971).
- Cheap-sensor EWS tools: buried MEMS inclinometer (1103.1678), unsupervised ground-motion (2601.03569),
  Fukuzono inverse-velocity failure-time (1208.6116).

## Honesty & limits (§0.5)
- 17 primary papers are ABS (0 FT). An initial reading run FAILED (web_search no API key + arXiv-429);
  primaries were obtained in a SECOND throttled arXiv run (HTTP 200). The 18 encyclopedic reads are FT-REF
  (verify equation FORMS, cite primaries) — counted separately, NOT as the primary quota.
- Coefficient values (Caine I=14.82 D^(−0.39); Scheidegger 0.62419/0.15666; Costa–Schuster 0.763 PE^0.42;
  Voellmy μ,ξ) are [coeff-verify] — forms verified, coefficients NOT confirmed against primary sources;
  geotechnical + hydrology expert review required before external use.
- CENTRAL DATA GAP (honest): local landslide inventories + co-located rainfall/soil-moisture, gauged
  discharge, loop-rating events, and GLOF records are scarce/absent for ungauged Himalayan catchments →
  GB-03/GB-04/GB-05 CANNOT be validated there and must ship ADVISORY-ONLY with wide uncertainty.
- Datasets D45-D54 are [D]; IMD (D47) and CWC (D53) frequently restricted/paid = the key access risk.

## Open actions carried
Confirm all [coeff-verify] constants against primary sources (Iverson 2000, Caine/Guzzetti, Scheidegger/
Corominas, Froehlich/Costa–Schuster, SCS-CN, Manning n); geotech+hydrology expert review of GB-01..05;
portal-verify dataset licenses + coverage; secure local inventories to calibrate thresholds/ratings;
full Scholar/patent novelty sweep when web_search restored.

## Gate
PROGRAM/gate_messages/PHASE_07G_gate.md. Auto-proceeding to P9 (anomaly detection).
