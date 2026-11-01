# 22 — Limitations, Risks & Open Problems

> This is the chapter where honesty is most load-bearing. Read it before you trust any other number in this
> documentation set. Everything here agrees with `_CANON.md`; where a limitation touches a canonical fact the
> number is copied exactly. Honesty labels follow `_CANON.md §1`: `[CONFIRMED]` (measured by us or verified in
> a cited source), `[LIKELY]`, `[HYPOTHESIS]`, `[INFEASIBLE]`, plus `[UNVERIFIED]` for unchecked external facts
> and `[EST]` for estimated figures. "Paper X reports …" is kept visibly separate from "Our state: …".
>
> One sentence governs the whole chapter: **No TRINETRA model has been trained and no dataset has been
> downloaded, so no accuracy, skill, latency, false-alarm, coverage, or cost number in this project is a
> measured result of TRINETRA.** Every weakness below is stated plainly and is not mitigated away. Where a
> mitigation is only an intention, it is labelled `[HYPOTHESIS]` — a design plan, not a demonstrated control.

---

## A. Fundamental state limitations (the big ones)

These are not gaps to be apologised for; they are the deliberate, declared state of a research-first,
honesty-first, life-safety project. They dominate every other limitation in this chapter.

- **A1 — Nothing was trained.** [CONFIRMED] `FINAL_REPORT.md` states verbatim: *"Nothing was built, trained,
  or measured."* No weights exist for any of the six PyTorch models, no fusion head is fitted, no RL policy is
  learned. Any model-shaped artifact in the repo is a specification or an untrained module, not a trained
  system.
- **A2 — No dataset was downloaded.** [CONFIRMED] Every dataset is `STATUS = candidate [D]` (D-numbered to
  D112); none is `selected`; none is on disk here. Dataset discovery produced a catalogue, not data.
- **A3 — No measured skill / accuracy / latency / false-alarm / coverage number exists.** [CONFIRMED] Every
  performance figure anywhere in this documentation is **SOURCE-REPORTED** — it is some other paper's result on
  that paper's own data, carried under Rule 16. Where a reader expects a TRINETRA result, the honest answer is
  **"not measured."** This includes: detection recall, smoke-specific recall, false-alarms/day,
  time-to-detection, PICP/coverage, averted loss, radio range, node current draw, RAM, and end-to-end latency.
- **A4 — The `deep/` layer is compile-only.** [CONFIRMED] The PyTorch `deep/` layer (6 models + fusion heads)
  and the `kaggle/` training scripts are verified by `py_compile` only. They have **never been run on a GPU in
  this environment** — the sandbox has numpy, pandas, lxml only (no torch / CUDA / scipy / sklearn / yaml).
  "Compiles" means the Python parses, not that the forward pass is correct, the shapes line up at runtime, the
  loss decreases, or the model trains. What *does* run and is verified: the pure-numpy core — `python
  run_tests.py` → **128 tests OK** and `python scripts/ci_gates.py` → **ALL 6 CI GATES PASSED** [CONFIRMED].
- **A5 — Dataset licenses are unverified.** [UNVERIFIED] All [D] candidate licenses are INDICATIVE only.
  Portal access and license verification are an OPEN backlog item. A dataset that looks free may carry
  redistribution, attribution, or non-commercial terms we have not read. No dataset may be used in a build
  until its license is confirmed (gate G7).
- **A6 — The BOM is entirely estimated; the ≤₹2000 gate is not enforceable.** [EST] Indian supplier pages
  returned HTTP 403 (Cloudflare) this session, so every ₹ figure is an estimate, not a dated live listing.
  Node A "Slope Sentinel" ≈ ₹1,930 [EST] and Node B "River Eye" ≈ ₹1,980 [EST] both sit *just under* the
  ₹2,000 ceiling — but the ceiling (constraint C2) **cannot be enforced** until every line item is re-quoted
  from ≥2 dated live listings (gate G5, OQ-05). A small price move on any component tips a node over budget.
- **A7 — Kaggle limits are not freshly fetched.** [UNVERIFIED] The compute plan assumes ~30 GPU-h/week
  (≈25.5 usable after a 15% reserve), ~12 h sessions, P100 (16 GB) or 2× T4 (2×16 GB), ~20 GB persistent +
  ~73 GB scratch, ~13–16 GB RAM. Kaggle's docs pages are JS-rendered and returned no usable text via
  `web_fetch`; these are the **widely-published** limits, not values read from the live quota panel. They must
  be re-confirmed on the account at the first build session before any schedule is committed (constraint C3).
- **A8 — India regulatory / LoRa-band / alerting-authority facts are unverified and are not legal advice.**
  [UNVERIFIED] Every India regulatory finding — fire-device certification, radio/LoRa-band legality
  (assumed IN865–867 MHz, SX1262), who may originate official CAP/SACHET/WEA alerts, data-protection in video,
  CCTV/surveillance rules, electronics certification — is a search lead flagged for qualified legal/standards
  review. The specific claim "authorities-only may originate WEA/SACHET" has **not** been checked against
  ITU/3GPP/NDMA. Nothing in this project is legal advice.
- **A9 — arXiv identifiers are largely subagent-reported, not independently re-fetched.** [UNVERIFIED,
  disclosed residual risk] The ledger holds **631 unique arXiv IDs** as snapshotted in FINAL_REPORT §5 (the
  live ledger has since grown to ~**775**; see `_CANON §7`/ch19) (681 ID-bearing rows; ~7.3% legitimate
  cross-phase re-citations) with ≈436 new papers verified across phases.¹ Most IDs were reported by subagents;
  `web_search` had no API key and arXiv re-resolution was only via throttled `web_fetch`, so most IDs were
  **not independently re-fetched**. Residual risk: a cited ID may be mis-transcribed or point to a different
  paper than described. A load-bearing sample HAS now been resolved: 9 IDs in `_QG2_reference_verification_log.md`
  plus the ch19 "load-bearing references — fully verified (2026-10-10)" subsection (all HTTP 200 + title match);
  the long tail stays disclosed-unverified.

  > ¹ The figures **681 ID-bearing rows** and **≈436 verified** are *not* canon numbers — they come from the
  > orchestrator's regex pass over `analysis/02_paper_ledger.csv` and the phase logs, not `_CANON §7` (which
  > records only 631-snapshot / ~775-live). Treat 681/436 as ledger-derived provenance detail, not a canonical count.

---

## B. Scientific / statistical limitations

These bound what any eventual TRINETRA skill number could legitimately mean, even after a full build.

- **B1 — Very few geo events (n ≈ 5-ish) → any skill estimate is variance-dominated.** [CONFIRMED as a
  structural limit] Rapid-onset Himalayan hazards are rare; with on the order of five labelled geo events, a
  point estimate of skill (ROC-AUC, MCC, recall) carries confidence intervals so wide that the number is
  essentially uninformative on its own. Headline skill claims must be reported with intervals (IQM + CIs), and
  a tight-looking mean on five events is **not** evidence.
- **B2 — Spatial leakage inflates skill; random CV overstates it.** Paper reports: **arXiv 2608.12422**
  (FT-PARTIAL, on OUR hazards / region / free-data constraint) finds naive non-spatial evaluation inflates
  terrain-susceptibility ROC-AUC from a naive ~0.90 down to **0.76 / 0.71 / 0.54** (GLOF-burst / landslide /
  small-flood) under honest tile-withheld spatial-CV with case-control matching — an inflation of ≈0.15–0.35
  AUC. The finite-sample side is **2610.08227** (effective sample size N_eff = Θ(n²/r²); buffer g = Θ(r·log(n/δ))).
  Our state: spatial-block CV with a buffer ≥ the measured spatial-correlation range is **mandatory** before
  any skill claim (gate G2); random CV is forbidden as a headline. We have **not** measured the correlation
  range r on Himalayan (anisotropic) terrain — that remains open.
- **B3 — Calibrated members ≠ a calibrated ensemble.** Paper reports: **arXiv 2101.05397** — averaging
  individually-calibrated models does not yield a calibrated ensemble. Our state: the fused output must be
  **re-calibrated per availability** (per-zone Mondrian conformal), and member-level calibration is never
  taken as ensemble-level calibration. This is a design response `[HYPOTHESIS]`, not a demonstrated outcome.
- **B4 — Conformal coverage degrades under drift; it is approximate, not a guarantee.** Papers report:
  split-conformal coverage collapses from 90% toward ~65% under moderate shift (**2604.22787**); EnbPI
  (**2010.09107**) gives coverage with an explicit, shift-sensitive *gap* that only → 0 under regularity;
  DistMatch (**2606.00690**) and AFOCP (**2511.15838**) keep *long-term/asymptotic* validity but note **local
  miscoverage right after an abrupt shift** — exactly the rare-hazard moment. Our state: we must **never**
  claim a hard 1−α coverage on these streams. Coverage is approximate-under-stability; a tight conformal
  interval must never suppress a physics-gated alarm (shield priority). Empirical per-zone coverage on
  Himalayan streams is unmeasured.
- **B5 — The admission-baseline circularity.** [CONFIRMED limitation of the current code path] The eval
  admission classifier / anomaly-logistic is fit on the **model's own out-of-fold (OOF) score**, so part of
  the admission signal is circular — the gate is partly judging the model against a label derived from the
  model. The *geo* path uses real external features (terrain, antecedent rainfall), which breaks the
  circularity there; the fire/anomaly logistic path does not fully. Until the admission gate is driven by
  independent labels, an "admitted" verdict is weaker than it appears.
- **B6 — Confident-while-wrong failure.** Paper reports: **arXiv 2610.08810** — models stay confident while
  being wrong under distribution shift. Our state: a high model probability is **not** evidence of
  correctness; uncertainty-entropy is used as an alert gate and cross-sensor corroboration is required, because
  a single confident model output cannot be trusted at a decision boundary. This is a known, named failure the
  design must assume is present, not a solved problem.

---

## C. Engineering / deployment risks

- **C1 — Single-node false RED.** A single faulty IoT node (stuck tilt, water-ingress short, drifted gauge)
  can emit a spuriously extreme reading. Intended mitigation `[HYPOTHESIS]`: fault-vs-event discrimination
  (a physically implausible lone spike is treated as a fault, not an event) plus the deterministic shield and
  cross-sensor corroboration. None of this is measured; a false RED from a single node is a live risk until the
  discrimination logic is validated against real fault data (gate G5).
- **C2 — IMERG precipitation underestimation.** Satellite IMERG precip is known to underestimate intense
  orographic/convective rainfall — the exact regime that drives cloudbursts and flash floods. Intended
  mitigation `[HYPOTHESIS]`: LoRa rain-gauge bias-correction of IMERG at the gateway. Residual: where no gauge
  exists, the precip input is biased low precisely when it matters most.
- **C3 — INT8 smoke-recall loss.** INT8 quantisation of the edge CCTV detector (needed to fit Tier-0/Tier-1
  budgets) is expected to cost recall, and smoke (low-contrast, diffuse) is the most fragile class. We have
  **not** measured the INT8 recall drop; it is a known quantisation risk, not a quantified one.
- **C4 — LoRa regulatory / band risk.** [UNVERIFIED] The design assumes IN865–867 MHz (SX1262). If the
  assumed band or duty-cycle is wrong for India, the radio is illegal or non-functional (assumption A-06). Not
  verified against the regulator; blocks hardware order (gate G5).
- **C5 — Solar brownout / winter-monsoon outages.** Node outage is treated as **EXPECTED, not exceptional**:
  winter and monsoon solar gaps will starve nodes. Intended mitigation `[HYPOTHESIS]`: oversized power,
  LiFePO4 storage, deep-sleep duty-cycling, store-carry-forward (DTN). Residual: the alert path must degrade
  gracefully to "uncertain/offline" during multi-day outages — unmeasured.
- **C6 — India data portals are JS-only and unverified.** [UNVERIFIED] Bhuvan / MOSDAC / VEDAS / NRSC / IMD /
  CWC / GSI portals are JavaScript-rendered and returned no usable static content; programmatic access,
  availability, and terms are unconfirmed. A data pipeline that assumes these portals may not be buildable as
  designed (gate G7).
- **C7 — Class-C physics and fusion are unvalidated and expert-review-pending.** Class-C novel terms
  (fire flicker/ND terms C-01/C-02; the PHARAOH power-mean operator) are **documentation-only, default-OFF**,
  with a Class-A fallback. They are hypotheses with validation roadmaps and a **mandatory fire-science /
  fusion expert review** that has not happened. They must not be described as established or validated
  (gate G1).

---

## D. RL-specific limitations

- **D1 — No off-the-shelf disaster-evacuation RL environment (BUILD GAP).** [CONFIRMED gap] There is no
  existing simulator for the disaster-evacuation / dispatch decision problem. One must be **built** before any
  RL training or offline-policy evaluation is meaningful. Until it exists, every RL claim is purely a design.
- **D2 — Off-policy evaluation (OPE) positivity / ESS fragility.** OPE on logged or simulated episodes is only
  valid where the logging policy had support (positivity) and the effective sample size is adequate. The
  design requires a DataCOPE-style **OPE-feasibility gate** (2311.14110): if the offline data does not support
  evaluating a policy, fall back to a one-step / shielded fixed policy. This means an RL policy may be
  **un-evaluable** on our data and therefore undeployable.
- **D3 — Reward-inversion / reward-hacking risk.** A mis-specified reward can be gamed — e.g. minimising false
  alarms by never alarming, or chasing a proxy that inverts the life-safety objective (a missed event is far
  worse than a false alarm: C_miss=100 vs C_FA=5, p* ≈ 0.0476). Reward design is thinly sourced on arXiv
  (one hard number, 2109.07745) and is an open item.
- **D4 — RL must beat MILP / non-RL baselines or it does not deploy.** [CONFIRMED doctrine] Papers report RL
  only *sometimes* beats classical baselines and naive RL underperforms (2509.19972; MILP 2602.14676;
  stochastic-program alternative 2608.26304). Our state: RL is **advisory only** (ranked options to a human
  dispatcher, never actuation) and must beat a fixed-threshold → one-step → MILP/stochastic-program ladder
  under our protocol, or it is not carried. We have no evidence it does; the burden of proof is on RL.

---

## E. Security / privacy residuals

- **E1 — Placeholder cryptography.** [CONFIRMED current state] CAP-alert and IoT-message signing is
  **HMAC-SHA256 placeholder** crypto because the sandbox lacks the `cryptography` library. Production intent is
  **Ed25519 / XML-DSig** for CAP, which is **not implemented**. HMAC with a shared secret does not give the
  non-repudiation and public-key verification an authority-grade alert feed needs; this is a stub, not the
  production security posture.
- **E2 — Several security mitigations are design-intent only.** [HYPOTHESIS] The following are specified, not
  demonstrated: tamper detection, adversarial-patch defence on the CCTV detector, face-blur / privacy
  redaction, and key rotation. Each is a plan in the design docs; none is validated, red-teamed, or measured.
  Treat them as intended controls, not controls in place.

---

## F. Known open consistency items (from `PROGRESS_DOC.md`)

These are code-internal / cross-artifact nuances flagged by chapter writers for the QG4 consistency gate.
They are **not** contradictions with `_CANON.md`; they are divergences to reconcile in the docs. Listed here so
a reader is not surprised by them.

- **F-a — RL action cardinality 3-vs-binary.** `deep/offline_rl.py` uses 3 actions {HOLD, WATCH, ALARM};
  the numpy `rl.py RuleBaselinePolicy.act` is binary {0,1}. The 3→binary mapping used in OPE-vs-baseline is
  implicit ([LIKELY] {WATCH, ALARM}→alarm). Canonical statement still to be fixed.
- **F-b — "TD3-BC" label vs implemented CQL.** `FEATURES.md` F-06 labels the RL component "TD3-BC
  baseline-first", but implemented Model-6 is **CQL** (one-step, γ=0). Consistent in spirit; a one-line
  reconciliation is needed (docs only — do not edit `FEATURES.md`).
- **F-c — Shield only in torch `act()`.** The safety shield exists only in torch `CQLPolicy.act`
  (`shield_floor_idx`); `rl.py` has no standalone shield class, and the realizability check is **specified,
  not implemented**. The "hard monotone shield" is therefore not uniformly present across both code paths.
- **F-d — CCTV→fusion via adapter, not a direct call.** CCTV→fusion wiring is via
  `ws5_fusion_rl/adapters.deep_expert` + `_POLICY` caps, not a direct call in `ws4_cctv`; no explicit
  orchestrator call-site was found. The end-to-end "frame → fusion" claim should be softened accordingly.
- **F-e — Battery chemistry LiFePO4 vs Li-ion 18650.** `HLD §4` says LiFePO4; `firmware/FIRMWARE_SPEC.md`
  says Li-ion 18650 + PV; `_CANON.md §8` is silent. Both are reported; canonical choice is undecided.
- **F-f — Tilt-rate unit deg/s vs deg/day.** `ws7_iot/edge_screen.py` uses `tilt_rate_dps` (deg/s);
  `COMPONENT_DESIGN.md §5` says "5°/day". The code marks these thresholds illustrative, but the unit
  discrepancy is unresolved and safety-relevant for an edge screen.
- **F-g — Demo invocation.** Documentation shows `python demo.py` (per `00_README`), while the module path is
  `python -m trinetra.pipeline.demo`. The two invocation forms must be reconciled so the quick-start command
  actually runs.
- **F-h — Stale test count in `MODEL_CARDS.md`.** `MODEL_CARDS.md` says "93 tests" (stale); canonical is
  **128** (`_CANON §2`, `CODE_INVENTORY.md`). Source artifact, not edited; noted as stale.

---

## G. Prioritised risk table

Likelihood/impact are qualitative planning judgements (there are no measured frequencies). "Owner-gate" maps
each risk to the quality gate (G1–G7, `HLD §8`) that must clear before the risk is retired. Mitigations marked
`[HYPOTHESIS]` are intended, not demonstrated.

| # | Risk | Likelihood | Impact | Current mitigation | Residual | Owner-gate |
|---|------|-----------|--------|--------------------|----------|------------|
| R1 | Spatial leakage inflates skill → an overclaimed model is deployed | High (if random CV is used) | Critical (unsafe false confidence) | Mandatory tile-withheld spatial-CV + buffer ≥ r; baselines + CIs (2608.12422 / 2610.08227) `[HYPOTHESIS]` | r unmeasured on anisotropic Himalayan terrain | **G2** |
| R2 | n ≈ 5 geo events → variance-dominated skill estimate | High | High (number is uninformative) | Report IQM + CIs; never headline a point estimate `[HYPOTHESIS]` | Cannot be fixed without more events | **G2** |
| R3 | Conformal coverage collapses under drift / after abrupt shift | High | High (miscoverage at the hazard moment) | EnbPI/DistMatch/AFOCP approx coverage; drift monitor; shield priority `[HYPOTHESIS]` | Local miscoverage right after a shift; unmeasured on our streams | **G3** |
| R4 | Single-node false RED | Medium | High (false public-alert pressure) | Fault-vs-event discrimination + corroboration + shield `[HYPOTHESIS]` | Unvalidated against real fault data | **G5** |
| R5 | INT8 smoke-recall loss | Medium | High (missed smoke events) | Keep smoke-specific recall as an explicit metric; fallback precision | Drop unmeasured; smoke is the fragile class | **G2** |
| R6 | IMERG underestimates intense precip | Medium–High | High (missed cloudburst signal) | LoRa rain-gauge bias-correction `[HYPOTHESIS]` | No gauge ⇒ precip biased low when it matters | **G2** |
| R7 | ≤₹2000 BOM slips over budget | Medium | Medium (infeasible node) | Node A ≈₹1,930 / Node B ≈₹1,980 [EST]; substitution plan | Supplier 403 ⇒ ceiling not enforceable | **G5** |
| R8 | LoRa band / duty-cycle illegal for India | Low–Medium | High (illegal/non-functional radio) | Assume IN865–867 MHz (SX1262) `[UNVERIFIED]` | Not checked vs regulator | **G5** |
| R9 | Solar brownout / multi-day node outage | High (seasonal) | Medium (coverage gap) | Oversize power, LiFePO4, deep-sleep, DTN `[HYPOTHESIS]` | Graceful degradation unmeasured | **G5** |
| R10 | RL reward inversion / hacking | Medium | Critical (life-safety objective inverted) | Advisory-only; shield floor; cost-loss p*=0.0476; OPE-feasibility gate `[HYPOTHESIS]` | Reward thinly sourced; env not built | **G4** |
| R11 | RL un-evaluable (OPE positivity/ESS) | Medium | Medium (RL cannot be admitted) | DataCOPE OPE gate → fall back to one-step/fixed `[HYPOTHESIS]` | May be undeployable on our data | **G4** |
| R12 | Placeholder HMAC crypto in production | High (if shipped as-is) | Critical (spoofable alerts) | HMAC-SHA256 stub; Ed25519/XML-DSig intended | Production crypto not implemented | **G6** |
| R13 | Dataset license violation | Medium | High (legal/redistribution block) | All [D] candidate; none selected; verify before use | Licenses indicative/unverified | **G7** |
| R14 | India data portals unusable (JS-only) | Medium | Medium (pipeline not buildable) | Catalogue only; verify access at build `[UNVERIFIED]` | Access/terms unconfirmed | **G7** |
| R15 | Class-C physics/fusion treated as validated | Low (default-OFF) | High (unvalidated model in alert path) | Default-OFF + Class-A fallback; expert review pending `[HYPOTHESIS]` | Review not done | **G1** |
| R16 | Mis-cited / mis-resolved arXiv ID | Medium | Medium (traceability erosion) | Ledger of 631 IDs; sample re-resolution planned | Most IDs not independently re-fetched | **G7** |
| R17 | Admission-baseline circularity (OOF logistic) | Medium | High (gate weaker than it looks) | Geo uses real features; keep OOF separation | Fire/anomaly logistic still partly circular | **G2** |
| R18 | Missing-modality collapse (worst-case, not random) | High (event destroys best sensor) | High (silent degradation) | Worst-case dropout eval + <1% adapter + uncertainty flag (2609.15297/2310.03986) `[HYPOTHESIS]` | Unvalidated on Himalayan data | **G4** |
| R19 | Confident-while-wrong under shift | High | High (false confidence at boundary) | Entropy gate + cross-sensor corroboration (2610.08810) `[HYPOTHESIS]` | Named failure assumed present | **G3** |
| R20 | Kaggle quota tighter than assumed | Medium | Medium (plan overruns) | 25.5 usable h plan + reserve + cut-list `[UNVERIFIED]` | Limits not freshly fetched | **G7** |

---

## What high performance on any single benchmark would NOT prove

Suppose, after a build, TRINETRA posts a strong number on one benchmark — say high ROC-AUC on a landslide
susceptibility set, or EFA-YOLO-class mAP on a public fire-image test. That result, **on its own, would prove
almost nothing that matters for this system.** It would not prove the skill survives honest tile-withheld
spatial-CV with a buffer ≥ the terrain correlation range (random-split skill is known to collapse by
≈0.15–0.35 AUC on our hazards, 2608.12422); it would not prove the estimate is stable, because with n ≈ 5 geo
events the confidence interval swallows the mean; it would not prove calibration, because a calibrated model on
one split is routinely miscalibrated under the distribution shift and sensor-dropout the field guarantees
(2610.08810, 2604.22787); it would not prove the conformal coverage holds at the one moment it must — the
abrupt onset of a rare hazard, where even asymptotically-valid conformal shows local miscoverage; it would not
prove the edge-deployed INT8 model keeps its smoke recall, nor that latency, current, RAM, and radio range
meet budget on real hardware (all unmeasured); it would not prove the node is affordable (≤₹2000 unenforced),
legal (LoRa band unverified), or that an authority may even originate the resulting alert (unverified); it
would not prove the RL policy beats a MILP/stochastic-program baseline, or is even evaluable under OPE
positivity; and it would say nothing about the system's behaviour when a sensor is lost precisely because the
event destroyed it (worst-case, not random, missingness). A single benchmark win measures one model on one
distribution under one evaluation choice. TRINETRA's claim is a *life-safety, cross-site, offline-first,
calibrated, shielded, human-in-the-loop advisory* — and that claim is only earned by passing the full gate
stack G1–G7 (physics golden-cases, the spatial-CV admission gate with baselines + CIs + cost-loss, the
decision-function + measured conformal coverage, fusion stability, supplier-verified BOM + LoRa band,
anti-leak + no-egress audit, and dataset-license + Kaggle-fit), with every number stated as "beats GB +
decision-tree + persistence under tile-withheld spatial-CV with case-control matching and fixed seeds, with
honest coverage" — never as a bare benchmark score. Until then, the only measured facts TRINETRA owns are:
**128 numpy unit tests pass and 6 CI gates pass.** Everything else is a plan, a hypothesis, or someone else's
result.
