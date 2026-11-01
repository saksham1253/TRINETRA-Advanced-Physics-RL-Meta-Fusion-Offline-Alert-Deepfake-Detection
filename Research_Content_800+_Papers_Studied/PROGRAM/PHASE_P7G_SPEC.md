# PHASE P7G (INSERTED) — WS1b, GEO-HAZARD PHYSICS MODEL SET AND DERIVATIONS ON PAPER

Status: PHASE SPECIFICATION (authored 2026-10-09 at user request: "create a detailed phase for the geo
hazard work"). This is an INSERTED companion to P7 (which covered FIRE physics). P7G covers the GEO-HAZARD
physics for the Himalayan early-warning side of the project. It follows the SAME two-layer, class-based,
derive-on-paper method as P7 and the SAME program rules (§0.3 non-destruction, §0.5 hard-honesty/no-padding,
Rule 16 no own-system performance claims, Rule 20 model classes A/B/C, Rule 21 novelty, §0.9A datasets).
Mode: RESEARCH-ONLY (paper derivations; no code, no field work). Execution slot: in the continuous
autonomous run, P7G executes right after P8 (per the user's "then GO PHASE P8" ordering), then P9 onward.

## Objective
Decide which GEO-HAZARD physics models the project uses (count N by evidence, not fixed), derive them fully
on paper, cross-check against the literature, and write the plan for validating them later — for rainfall-
triggered landslides, debris flows, flash floods, and glacial-lake-outburst floods (GLOFs) in Himalayan
conditions, sensed with low-cost IoT nodes (rain gauge, soil-moisture, pore-pressure/piezometer proxy,
tilt/inclinometer, river stage/ultrasonic level, accelerometer) and, where relevant, cameras/satellite.

## Entry
Companion to P7; P3 and P5 complete. (In the autonomous run: entered after P8.)

## Quota topics (≥15 NEW papers; aim ~30)
Rainfall-triggered landslide initiation (rainfall intensity-duration thresholds; infinite-slope stability;
Iverson transient pore-pressure; TRIGRS); unsaturated-soil hydrology (Richards equation, Green-Ampt
infiltration, soil-water retention); debris-flow initiation, runout and mobility (Scheidegger angle of
reach, Rickenmann, Takahashi, Voellmy-Salm rheology); flood hydrology (SCS-CN runoff, unit hydrograph,
rational method); open-channel flow and flood routing (Manning, Saint-Venant, Muskingum); GLOF and moraine-
dam/dam-breach physics (breach outflow, peak discharge regressions); river-stage / early-warning lead-time
analysis; physics-informed ML and data assimilation for landslide/flood nowcasting; low-cost geo-sensing
and sensor-physics (soil-moisture sensor calibration, piezometer response, tilt drift); uncertainty in
geotechnical/hydrological parameters.

## Tasks (mirror P7)
1. SOTA scan for physics-informed/guided landslide + flood + debris-flow + GLOF modeling and for the
   established geomorphology/hydrology correlations with their published validation cases/numbers →
   `PROGRAM/sota/P7G_sota_scan.md`.
2. Recover the originally identified geo-hazard models (the equations-register seed: E-01 infinite-slope
   FS, E-02 Iverson transient head, plus the planned Scheidegger/Froehlich/SCS-CN/Manning/Richards) and
   build a candidate map of geo-hazard phenomena relevant to low-cost sensing + imagery.
3. Two-layer model set:
   (a) LAYER 1 (Class A) `ws1b_geohazard/established_formula_inventory.md`: every established relation
       (infinite-slope stability; Iverson transient pore-pressure; Richards/Green-Ampt infiltration;
       rainfall intensity-duration thresholds; Scheidegger reach angle / runout; Takahashi / Voellmy-Salm
       debris-flow; SCS-Curve-Number runoff; Manning open-channel; Saint-Venant / Muskingum routing; GLOF
       dam-breach peak-discharge regressions; river-stage rating curves). For each: statement, symbols/
       units, source + equation, regime of validity, assumptions, and KNOWN WEAKNESSES in OUR setting
       (unknown soil/geotech parameters, cheap-sensor noise/drift, ungauged Himalayan catchments, extreme/
       non-stationary rainfall, data scarcity).
   (b) LAYER 2 (Class B/C) `ws1b_geohazard/derivations/`: robustified extensions, each on a documented
       weakness, declaring parent(s) + weakness + a full derivation that REDUCES to the parent in a stated
       limit (e.g. sensor-response-corrected pore-pressure from Iverson; uncertainty/dimensionless rainfall
       threshold with return-period priors; antecedent-moisture-corrected SCS-CN; stage-discharge with
       hysteresis correction; lead-time estimator coupling rainfall threshold → infiltration → stability).
   (c) LINEAGE TABLE `ws1b_geohazard/formula_class_table.md`: ID, class, parent(s), weakness, derivation
       ref, building-block sources, validation status; every extension shows reduction-to-parent.
   (d) ADMISSION `ws1b_geohazard/model_set_decision.md`: classify each candidate A/B/C with reasons + N.
4. `ws1b_geohazard/validation_plan.md` (named real public data or honest "none"), `verification_checklists.md`
   (dimensions/limits/reduction, + independent re-derivation check), `novelty_log.md` (Rule 21).
5. Equations-register additions (move the geo-hazard seed from "pending" to derived; keep fire/geo separate).
6. Datasets to `DATASETS.md` under §0.9A (e.g. landslide inventories — NASA Global Landslide Catalog,
   India GSI; rainfall — IMD/GPM/CHIRPS; DEMs — SRTM/ALOS; GLOF inventories — ICIMOD; discharge — CWC) as
   [D] discovery-only until portal-verified.
7. Read the ≥15 NEW quota papers; record what each changed (`literature_map.md`, `P7G_papers.csv`,
   `logs/P7G_reading_progress.md`, ledger rows).
8. Exit audit, `PROGRAM/reports/PHASE_07G_report.md`, `PROGRAM/gate_messages/PHASE_07G_gate.md` (as a
   COMPLETION RECORD; auto-proceed, do not halt), update PHASE_STATE/PROGRESS/CHANGELOG.

## Outputs
`ws1b_geohazard/` (established_formula_inventory.md, formula_class_table.md, model_set_decision.md,
derivations/, validation_plan.md, verification_checklists.md, novelty_log.md, literature_map.md), SOTA scan,
quota list, equations-register additions, datasets, report, gate-record.

## Acceptance (mirror P7)
Every admitted model has a derivation (Layer 1 outline + assumptions; Layer 2 complete), a verified source
for every non-trivial relation, hand-checked dimensional consistency and limits, a validation plan naming
real published data (or an honest "none exists"), and a documented regime of validity. Every Layer-2 model
has a documented parent, a targeted weakness, and a reduction-to-parent. Quota met. Rule 16/20/21 honoured.

## Rule 19 (life-safety framing)
All geo-hazard outputs are ADVISORY early-warning telemetry supporting human decision-makers and official
agencies (IMD/CWC/NDMA/state DMAs), never an autonomous evacuation trigger; real-world Himalayan life-safety
benefit stated in the design intent, with explicit uncertainty and lead-time honesty.
