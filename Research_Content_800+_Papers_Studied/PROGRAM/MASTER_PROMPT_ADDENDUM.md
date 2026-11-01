# PROGRAM/MASTER_PROMPT_ADDENDUM.md — appended final phases P21, P22, P23

PURPOSE. The user (direct request, 2026-10-10) added three NEW final phases to the MASTER_PROGRAM. Per
non-destruction (§0.3) the governing `PROGRAM/MASTER_PROMPT.md` (827 lines) is NOT edited; these phase specs
live here as an addendum and inherit ALL rules of the master prompt (§0.3 non-destruction, §0.5 hard-honesty/
no-padding, Rule 11 search-leads, Rule 16 no own-system performance claims, Rule 18 no unsupported impact,
Rule 19 life-safety advisory/human-in-the-loop, Rule 20 model classes A/B/C, Rule 21 novelty = search claim,
§0.9A free datasets). Research-only: write no code, build nothing, train nothing, measure nothing.

TOOLING REALITY (honest, binding on these phases). `web_search` has NO API key and is UNUSABLE. "Deep internet
research" is therefore done through `web_fetch` to SPECIFIC URLs: the arXiv Atom API (throttled, one query at a
time, http→https redirect followed manually) and named data portals (ISRO Bhuvan, NASA FIRMS/Earthdata,
Copernicus, USGS, etc.) where the page is fetchable. Any portal that does not resolve or is JS-only is recorded
as [UNVERIFIED — manual check needed], never invented. Paper IDs returned by subagent readers are SOURCE-
REPORTED and NOT independently re-fetched (disclosed residual risk).

NOVELTY RULE for these phases (critical). The user explicitly asked for NEW formulas "not present in any paper"
and a novel averaging technique. These are admissible ONLY as **Class C (novel hypothesis, unvalidated)** under
Rule 20/21: each novel formula/operator is derived transparently from stated assumptions and (where possible)
Class-A established blocks, is labeled "novel hypothesis — not found in our (search-limited) search — NOT
validated, NOT a result", carries a validation roadmap + expert-review flag, and is NEVER described as working,
correct, or better than anything. No performance claim is made for any novel construct (Rule 16).

=============================================================================================================
# PHASE P21 — FIRE-HAZARD PHYSICS DEEP-DIVE (expanded WS1a)

**Objective.** Deepen the fire-hazard physics beyond P7 into a research-grade physics layer: survey the state
of the art AND the advanced/PhD-level modeling literature, consolidate the established formula inventory, and
derive new Class-C candidate formulas that extend the parents where they demonstrably fail — all on paper,
honestly labeled, feature/prior-oriented for the detection + fusion system.

**Entry.** Appended final phase; auto-start under the standing continuous-mode directive.

**Quota.** >=50 NEW papers (user-set target; hard floor >=30 if the throttle prevents 50 — document the exact
number and reason). Mix: SOTA fire-detection-physics + advanced/PhD modeling (PINNs, neural operators, data
assimilation, radiative transfer, turbulence closure, pyrolysis kinetics, UQ, inverse problems, sensor
physics). Delivered via pipelined arXiv readers (two running: b7420e6a, 8435f7bb).

**Tasks.**
1. SOTA scan (`PROGRAM/sota/P21_sota_scan.md`): current best fire-physics modeling + physics-informed fire ML,
   source-reported, with the gap each leaves.
2. Established-formula consolidation (`ws1_physics/established_formula_inventory_P21.md`): extend the P7
   Class-A inventory with any additional canonical relations found (view factors, radiative transfer equation,
   extinction/Beer–Lambert, pyrolysis Arrhenius, ceiling-jet correlations, firebrand transport), each with a
   verified canonical source and known weakness. [coeff-verify] tags where coefficients need primary-source
   confirmation.
3. Advanced-analysis notes (`ws1_physics/advanced_analysis_P21.md`): a PhD-level synthesis of where the
   classical correlations break (low-fps CCTV, under-ventilated fires, wind-driven spread, sensor lag,
   radiative vs convective regimes) and what the advanced literature offers (surrogates, assimilation, UQ).
4. NOVEL derivations (`ws1_physics/derivations_P21/` — one file per item, >=6 Class-C candidates): each states
   PURPOSE, PARENT(s) + where the parent fails, ASSUMPTIONS, full derivation, the system-usable quantity
   (feature/prior/consistency-check/residual), uncertainty treatment, a VALIDATION roadmap vs specific
   published data, a pre-registered build-phase gate vs the parent, CLASS = C (novel hypothesis, unvalidated),
   and an expert-review flag. Never claimed as validated.
5. Class table update (`ws1_physics/formula_class_table_P21.md`): every P21 relation labeled A/B/C with lineage.
6. Novelty log (`ws1_physics/novelty_log_P21.md`): each novel item phrased as a SEARCH claim ("not found in our
   search; search was limited: no web_search, arXiv-abstract-level").
7. Ledger rows for all P21 papers; datasets (if any) to DATASETS.md as [D].

**Acceptance.** >=50 papers (or documented shortfall); every formula labeled A/B/C; every novel item a
hypothesis with a validation roadmap + expert flag + search-claim novelty; no performance claim; non-destruction
honored. **Exit.** SOTA scan, quota audit, reading audit, report, gate-record; auto-proceed to P22.

=============================================================================================================
# PHASE P22 — META-FUSION PHYSICS + RL + MULTIMODAL, WITH A NOVEL AGGREGATION OPERATOR

**Objective.** Design the meta-fusion layer that combines the physics models, the multimodal detectors, and the
advisory RL layer, by (a) deriving >=6 physics-grounded fusion models and (b) inventing an advanced NOVEL
averaging/aggregation operator and supporting novel formulas, built from derived + established pieces — all on
paper, Class-C/hypothesis, advisory (Rule 19), uncertainty- and calibration-aware.

**Entry.** After P21; auto-start.

**Quota.** >=15 NEW papers minimum (aim ~40 across the two P22 readers: fusion/aggregation 8b0b3c39 + RL/
physics-informed c84d58e2), to ground the derivations in the state of the art of model averaging, evidential/
Bayesian fusion, robust aggregation, and physics-informed/multimodal/safe RL.

**Tasks.**
1. SOTA scan (`PROGRAM/sota/P22_sota_scan.md`): best current fusion/aggregation + RL-for-fusion methods,
   source-reported, with gaps.
2. >=6 DERIVED FUSION PHYSICS MODELS (`ws5_fusion/derivations_P22/` — one file each): e.g. precision-/
   reliability-weighted fusion with physical consistency residuals; evidential/Dempster–Shafer fusion with a
   physics-prior mass; conformal-bounded stacked fusion; covariance-intersection-style fusion under unknown
   correlation; physics-consistency-gated mixture-of-experts; RL-tuned fusion weights with a physics-informed
   reward. Each: PURPOSE, inputs/modalities, PARENT method + where it fails for us, ASSUMPTIONS, full
   derivation, uncertainty/calibration treatment, Rule-19 advisory output, VALIDATION roadmap + gate vs
   baseline, CLASS (B if from established blocks with a validation route; C if novel-hypothesis), expert flag.
3. NOVEL AGGREGATION OPERATOR (`ws5_fusion/novel_aggregation_operator_P22.md`): define a new, mathematically
   explicit averaging operator (e.g. a reliability-decayed, physics-consistency-weighted, uncertainty-shrunk,
   conformal-bounded generalized (Hölder/power) mean with a disagreement penalty and a safe fail-open to
   "uncertain"). State axioms it is designed to satisfy, derive its properties on paper (bounds, monotonicity,
   degenerate cases, how it reduces to known means), its parameters + how they'd be fit, and its honest
   limitations. CLASS C (novel hypothesis, unvalidated) — NO claim it is better than any existing method.
4. NOVEL supporting formulas (`ws5_fusion/novel_formulas_P22.md`): any additional novel quantities (e.g. a
   physics-consistency score, a cross-modal reliability weight, a drift-decayed trust coefficient) with
   derivations, assumptions, Class C, validation roadmap.
5. RL + multimodal integration note (`ws5_fusion/rl_multimodal_integration_P22.md`): how the advisory RL layer
   (P15) sets/tunes fusion weights or selects modalities (active perception / value-of-information), staying
   advisory, safe/constrained, and must-beat-non-RL-baseline; physics-informed reward.
6. Novelty log + class table for all P22 constructs; ledger rows for all P22 papers.

**Acceptance.** >=6 derived fusion models + >=1 novel aggregation operator + novel supporting formulas, each
Class-labeled, hypothesis-framed, with validation roadmap + expert flag; advisory (Rule 19); no performance
claim; quota met or shortfall documented; non-destruction honored. **Exit.** SOTA scan, quota audit, audit,
report, gate; auto-proceed to P23.

=============================================================================================================
# PHASE P23 — COMPREHENSIVE FREE-DATASET HUNT (final dataset phase)

**Objective.** Find as many FREE/open datasets as possible across every workstream and record them, with links/
access info, in a dedicated document. Cover arXiv-published datasets AND government/data portals reachable by
web_fetch (ISRO Bhuvan, NASA FIRMS/Earthdata, Copernicus/ESA, USGS/EarthExplorer, NOAA, Kaggle, etc.).

**Entry.** After P22; auto-start. This is the LAST phase.

**Quota.** As many as can be found; aim >=50 free datasets. Sources: arXiv dataset reader (7fc04f19) + direct
web_fetch to named portals (recorded only if the page/URL actually resolves; otherwise [UNVERIFIED — manual
check needed]).

**Tasks.**
1. SOTA/portal scan (`PROGRAM/sota/P23_portal_scan.md`): the portals checked, what each hosts, access status,
   and which URLs resolved via web_fetch vs need a manual check.
2. DATASET CATALOGUE (`DATASETS_CATALOGUE.md` — the dedicated document the user asked for): a table of every
   dataset with name, domain/workstream, modality, approx size, LICENSE/cost (free? — flagged UNVERIFIED where
   unknown), and ACCESS URL/host. Grouped by workstream (fire/smoke CCTV, satellite active-fire/burned-area,
   flood/SAR, landslide, InSAR/deformation, air-quality/gas, seismic, weather, crisis social-media, deepfake,
   multimodal). §0.9A: free-only for STATUS=selected; licenses INDICATIVE until portal-verified; no dataset is
   marked selected here without verification.
3. Cross-link the new finds into `DATASETS.md` as [D] candidates (append-only), continuing the D-numbering.
4. Honesty notes: every link is SOURCE-REPORTED / as-listed; download-link liveness NOT verified; government
   portals' terms must be checked manually.
5. Ledger rows for any dataset-paper sources.

**Acceptance.** A single consolidated free-dataset catalogue with links grouped by workstream; licenses/costs
flagged; nothing paid marked selected; portal resolution honestly recorded; non-destruction honored.
**Exit.** Portal scan, catalogue, audit, report, gate-record announcing completion of the addendum program;
STOP (mark goal complete).

=============================================================================================================
PHASE ORDER (addendum): P21 (fire physics) → P22 (meta-fusion physics + RL + multimodal) → P23 (datasets).
The physics phases (P21, P22) and the dataset phase (P23) are the FINAL phases; everything the user asked for
is contained in them.
