# PHASE P7 REPORT — physics model set and derivations on paper (WS1a)

Phase: P7 (WS1a — physics model set + derivations). Mode: RESEARCH-ONLY (paper derivations; no code, no
build). Date: 2026-10-09.

## Task completion (MASTER_PROMPT L437–454)
| # | Task | Status | Evidence |
|---|------|--------|----------|
| 1 | SOTA scan (physics-informed/guided fire + fire-growth/smoke-transport) | ✅ | PROGRAM/sota/P7_sota_scan.md |
| 2 | Recover originals + candidate phenomena map | ✅ | established_formula_inventory.md (coverage map) |
| 3a | Layer 1 established_formula_inventory.md (statement/source/validity/assumptions/KNOWN WEAKNESSES) | ✅ | ws1_physics/established_formula_inventory.md (EF-01..12) |
| 3b | Layer 2 robustified extensions (parent + weakness + full derivation) | ✅ | ws1_physics/derivations/B-01,B-02,B-05,B-06 |
| 3c | Lineage table + reduces-to-parent | ✅ | ws1_physics/formula_class_table.md |
| 3d | Admission A/B/C + N | ✅ | ws1_physics/model_set_decision.md |
| — | Layer-1 derivation outlines | ✅ | ws1_physics/derivations/LAYER1_outlines.md |
| — | Validation plan (named data / honest "none") | ✅ | ws1_physics/validation_plan.md |
| — | Verification checklists (dims/limits/reduction) + independent recheck | ✅ | ws1_physics/verification_checklists.md |
| — | Novelty log (Rule 21) | ✅ | ws1_physics/novelty_log.md |
| — | Equations-register additions | ✅ | analysis/08_equations_register.md (P7 section) |
| Q | ≥15 NEW quota (aim ~30) | ✅ 22 NEW | literature_map.md, P7_papers.csv, 22 [P7] ledger rows |
| D | Physics datasets to DATASETS.md (§0.9A) | ✅ | DATASETS.md D31–D34 [D] |
| A | Exit audit | ✅ | analysis/11_reading_audit.md Audit #13 |

## The model set (N by evidence, not fixed at 6)
- **Layer 1 (Class A): 12** — EF-01 Heskestad flame height; EF-02 t² HRR; EF-03 Heskestad plume; EF-04
  McCaffrey; EF-05 Alpert ceiling jet; EF-06 point-source radiation; EF-07 Beer–Lambert smoke extinction;
  EF-08 flicker f≈1.5/√D; EF-09 thermal-camera radiometry; EF-10 detector RTI/rate-of-rise; EF-11 Rothermel
  spread; EF-12 Zukoski entrainment.
- **Layer 2 (Class B, admitted): 4** — B-06 sensor-response-corrected ceiling-jet/plume signal (THE core,
  for the P6 node's rate-of-rise/delta timing); B-05 aliasing-aware flicker band (low-fps CCTV); B-01
  camera apparent flame height through smoke; B-02 dimensionless/prior plume-temperature estimator.
- **Layer 2 (Class C, documentation-only): 2** — C-01 level-set/CA ∘ Rothermel (offline wildfire
  simulator); C-02 full coupled forward camera model (synthetic-data generator).
- **Rejected for deployment:** live on-device fire-PINN (documented PINN failure modes); live pyrolysis
  kinetics (unobservable) — parked.

## Headline (all source-reported / derivational; no own-system claim — Rule 16)
- Every Layer-1 model has documented KNOWN WEAKNESSES in our non-ideal setting (unknown Q̇/geometry; cheap-
  sensor lag/noise/drift; low-res/low-fps CCTV; outdoor wind). Each Layer-2 extension targets one documented
  weakness, is built from cited Class-A blocks, and **reduces to its parent in a stated limit** — all four
  **independently re-derived by a second agent and confirmed internally correct (0 errors)**.
- Physics enters the system as FEATURES / PRIORS / CONSISTENCY CHECKS + an offline simulator, with fallback
  to the Class-A parent — NOT as hard constraints or a live on-device PINN. This is the evidence-backed
  (PINN-failure-mode literature) and deployment-safe choice.

## Honest limitations (§0.5)
- `web_search` had NO API key all phase → arXiv-only reading. The classic fire correlations (Heskestad,
  Alpert, McCaffrey, Cetegen, Mulholland, Rothermel, RTI, radiometry) returned ~0 on arXiv and are stated
  from established fire-science references as ABS-CANONICAL inventory sources (NOT quota papers); their exact
  constants are tagged [coeff-verify] and need primary-source confirmation + fire-science expert review
  before any external use.
- The 22 quota papers skew toward modern PINN-failure-mode and wildfire-spread arXiv work (where arXiv is
  rich); fire-physics forward-model depth was 3 papers (2 FT). Physics validation datasets (D31–D34) are
  [D] discovery-only, not portal-verified this session.
- No model is validated (nothing built); validation_plan.md names the data and pre-registers build-phase
  gates vs the parents.

## Acceptance check
Every admitted model has a derivation (Layer-1 outline + assumptions; Layer-2 complete), a source for every
non-trivial relation, hand-checked dimensions + limits, a validation plan (or honest no-data note), and a
documented validity regime; every Layer-2 model has a parent + targeted weakness + reduction-to-parent
(independently verified). Quota met (22 ≥ 15). → P7 COMPLETE; STOP at the gate.
