# 24 — Decision Log (ADR-style)

**Audience:** the original author six months later, or an auditor who needs to know *what was decided, what
was rejected, on what evidence, and what it cost.* This chapter is the architecture-decision record (ADR)
for the TRINETRA (**HIMKAVACH**) research program and its reference code. Reverted/rejected decisions are
indexed in `docs/25_changelog_and_provenance.md §25.5`; this chapter carries the full reasoning.

---

## 24.0 How to read this log — honesty posture

Per `_CANON.md §0`: **nothing was built, trained, or measured.** No decision below rests on a TRINETRA
performance result, because there is none. Every decision rests on (a) a design/safety constraint, (b) a
**source-reported** result from a cited paper on *its own* data (Rule 16), or (c) a correctness argument.
Honesty labels (`_CANON.md §1`) are used on each decision outcome:

- `[CONFIRMED]` — measured by us (code behaviour) OR verified in a cited source.
- `[LIKELY]` — plausible, needs our validation.
- `[HYPOTHESIS]` — our unvalidated idea.
- `[INFEASIBLE]` — ruled out.
- `[ABS]` — evidence read only at abstract depth; may never be stated as established fact.
- `[UNVERIFIED]` — search lead / claimed fact not independently confirmed in-program.

Evidence caveat carried from `_CANON.md §7`: most arXiv identifiers are **subagent-reported and not
independently re-fetched** — treat every arXiv ID below as a traceability pointer, not a re-verified citation.

**arXiv-ID note up front (affects D-07):** the spatial-CV collapse verdict is **triangulated across two
re-fetched papers** (QG2, 2026-10-10): **arXiv 2608.12422** (Himalayan GLOF/landslide — the claims-table
numbers) and **arXiv 2608.22293** (2025 Palisades urban-wildfire GeoAI — random CV ROC-AUC 0.92 → 0.75 under
1 km spatial-block validation, cited in `FINAL_REPORT.md §3/§4`), with **arXiv 2610.08227** as the
effective-sample-size theorem. `_CANON §6` directs citing **both** 12422 and 22293 (they are complementary,
not contradictory). This log follows `_CANON` (the arbiter) and cites all three; see §24.4.

---

## 24.1 Decision index (summary table)

Status key: **adopted** / **rejected** / **parked** / **superseded**. Phase tags map to `25_changelog §25.2`.

| D-ID | Decision (short) | Status | Label | Primary source |
|------|------------------|--------|-------|----------------|
| D-01 | Advisory, human-in-the-loop; never autonomous public alert (R19) | adopted | [CONFIRMED] | FINAL_REPORT §7; HLD §1; _CANON §5 |
| D-02 | IP-address-based alerting | **rejected** | [INFEASIBLE] | FINAL_REPORT §4; _CANON §6 → ch08 |
| D-03 | Full fire-PINN as deployed solver | **rejected** | [INFEASIBLE] | model_set_decision.md; FINAL_REPORT §1 |
| D-03b | Physics as soft features + Class-A fallback (P7) | adopted | [HYPOTHESIS] | model_set_decision.md |
| D-04 | Class A/B/C model-set scheme; admitted fire/geo relations | adopted | mixed | model_set_decision.md; _CANON §4 |
| D-05 | Iverson transient bug-guard `D1=D0/cos²β` ONLY (PATCH B) | adopted | [CONFIRMED] | Workstreams WS1; Corrected_Patches |
| D-06 | Fukuzono α=2 ⇒ 1/v linear regime (PATCH D) | adopted | [CONFIRMED] | Workstreams WS1 |
| D-07 | Spatial-block CV over random CV; mandatory baselines; real-win gate | adopted | [CONFIRMED] | analysis/07 DC-01/02; WS2 (G2) |
| D-08 | Conformal-under-shift (WCPS/ACI/Mondrian/CRC) | adopted | [CONFIRMED] | FINAL_REPORT §1; FEATURES F-13 |
| D-09 | Meta-fusion: FM-1 default, GMF bounded residual, PHARAOH OFF | adopted | mixed | MetaFusion; HLD §3; _CANON §4 |
| D-10 | Single decision fn `max(conformal, shield_floor)`; p*=0.0476 | adopted | [CONFIRMED] | HLD §2.3; _CANON §4 |
| D-11 | Monotone post-posed safety shield (no training) | adopted | [CONFIRMED] | MetaFusion §3; HLD §2.3 |
| D-12 | RL: offline, advisory, OPE-gated; CQL/one-step; evac-env BUILD GAP | adopted (gated) | mixed | FINAL_REPORT §1; analysis/07 DC-10 |
| D-13 | CCTV trained detector PRIMARY; zero-shot LOW-WEIGHT complement (D-011) | adopted | [HYPOTHESIS] | FINAL_REPORT §1/§7 |
| D-14 | Deepfake defensive-only, reliability hard-cap 0.4, red-teaming | adopted | [CONFIRMED-code] | FINAL_REPORT §1; code adapters |
| D-15 | Kaggle: PEFT/frozen-backbone over from-scratch pretrain | adopted | [CONFIRMED] | KAGGLE_BUDGET §6/§8 |
| D-16 | IoT ≤₹2000 tiered node; LoRa IN865–867 (reject 433 MHz); fault-vs-event | adopted (gated) | [EST]/[CONFIRMED] | Workstreams WS5; HLD §4 |
| D-17 | Offline-first DTN; signed CAP; authenticated cell-broadcast | adopted | [CONFIRMED] | FINAL_REPORT §1; HLD §5 |
| D-18 | Feature admission waves: F-11..F-17 Wave-1; F-18..F-26 parked | adopted | [ABS] | FEATURES.md (P17) |
| D-19 | Free-data-only; Kaggle-only compute | adopted (constraint) | [CONFIRMED] | _CANON §5; KAGGLE_BUDGET |
| D-20 | Autonomous public alerting without authority | **rejected** | [INFEASIBLE] | FINAL_REPORT §4; _CANON §6 |

Open items (unresolved) are in §24.5.

---

## 24.2 Decision records (detail)

### D-01 — Advisory, human-in-the-loop; never an autonomous public alert
- **Date/phase:** program-wide invariant (Rule 19); restated P12/P15/DESIGN. **Status: adopted. [CONFIRMED]**
- **Decision:** TRINETRA produces a calibrated, shielded **advisory** alert level for a **human** operator
  who alone decides on CAP/SACHET dissemination. The system fails safe to "uncertain/offline" and **never**
  crosses from advisory level to public alert without a human (trust boundary, `HLD.md §1`).
- **Alternatives considered:** (a) autonomous public alerting — rejected (see D-20); (b) semi-autonomous
  siren actuation under a hard physical rule only — retained *locally* at Tier-1 for a corroborated physical
  shield trigger (siren/SMS), but network-wide public dissemination stays human-gated (`COMPONENT_DESIGN §5`).
- **Evidence:** Rule 19 (`_CANON §5`); `FINAL_REPORT.md §7`; `HLD §1`. RL must stay advisory and beat non-RL
  baselines — MILP 2602.14676; naive RL underperforms 2509.19972 (`FINAL_REPORT §7`).
- **Consequence:** every downstream head is a confidence modifier, not an actuator; auditability/explainability
  requirement (every advisory traces to evidence + shield reason, `HLD §7`). Caps achievable autonomy by design.

### D-02 — IP-address-based alerting REJECTED [INFEASIBLE]
- **Date/phase:** P12. **Status: rejected (not carried). [INFEASIBLE]** → full treatment in chapter 08.
- **Decision:** Do **not** use consumer IP geolocation to target or trigger life-safety alerts.
- **Why (rationale verbatim from source):** consumer IP geolocation resolves only to ISP/city granularity
  (often tens of km), is corrupted by CGNAT / VPN / DHCP, does not map to a premises, and cannot address a
  specific person at risk; using it to target or trigger alerts would be unreliable and unsafe
  (`FINAL_REPORT.md §4`, `_CANON §6`).
- **Alternatives considered:** keeping IP as a coarse geofence — rejected on the same unreliability grounds.
- **Reframe adopted:** public-IP *exposure* of any endpoint is treated instead as a **security** concern
  (authenticated endpoints, allow-list C6), not an addressing mechanism.
- **Evidence:** `FINAL_REPORT.md §4` (claim ledger, INFEASIBLE); `_CANON §6` (load-bearing verdict). No arXiv
  ID attached in source — this is an engineering/geolocation-reliability verdict, not a paper claim.
- **Consequence:** alerting is **premises/zone-and-siren based** (DTN + Tier-1 siren + CAP), not IP-based.

### D-03 — Full fire-PINN as a deployed on-device solver REJECTED [INFEASIBLE]
- **Date/phase:** P7. **Status: rejected for deployment. [INFEASIBLE] now.**
- **Decision:** Do not deploy a full fire-PINN as a live on-device (ESP32-class) solver.
- **Why (verbatim):** PINN failure modes — stiffness, loss-weight imbalance, spectral bias, causality
  violation, poor extrapolation, non-identifiability — make a live fire-PINN a research risk, not an ESP32
  path (`ws1_physics/model_set_decision.md`, REJECTED section). Scoping decision, **not** a claim that PINNs
  cannot work.
- **Alternatives considered:** PINN as a *constraint head* on the landslide branch (2407.06785) and a
  physics *surrogate* where a calibrated solver exists (2507.15614) — both kept as research options, not as
  the deployed solver (see analysis/07 DC-08/DC-14).
- **Evidence:** `model_set_decision.md`; `FINAL_REPORT §1`; `_CANON §6`; 2407.06785 (PINN constraint, [ABS/FT]),
  2507.15614 (surrogate needs a solver to emulate, [SUPPORTED]).
- **Consequence:** physics enters as **soft features/priors/consistency-checks + a synthetic-data simulator
  offline**, never a hard on-device dependency. See D-03b.

### D-03b — Physics as soft features with Class-A fallback
- **Date/phase:** P7. **Status: adopted. [HYPOTHESIS]** (the Class-B features are unvalidated).
- **Decision:** All derived (Class-B) physics enters the learning system as **soft features/priors with their
  own uncertainty and a documented fallback to the Class-A parent**; none is a hard dependency until its
  build-phase validation gate passes (`model_set_decision.md §(e)`).
- **Evidence:** `model_set_decision.md`; `FINAL_REPORT §1` (WS1a). Class-B set B-01/B-02/B-05/B-06 are tagged
  `[HYPOTHESIS]` in `FINAL_REPORT §4`.
- **Consequence:** a failed/unvalidated physics extension degrades gracefully to its established parent (R20).

### D-04 — Class A/B/C model-set scheme; which fire/geo relations are admitted
- **Date/phase:** P7 / P7G. **Status: adopted. [CONFIRMED]** counts; **[HYPOTHESIS]** for Class B; Class C
  documentation-only. Source: `ws1_physics/model_set_decision.md`, `FINAL_REPORT §2`, `_CANON §4`.
- **Decision & admitted set (N = 18 modelled relations total):**
  - **Layer 1 (Class A, established, verified-source): N = 12** (EF-01…EF-12). Fire (WS1a): **Heskestad**
    flame height, **Byram** fireline intensity, **Strouhal** flicker (1.5/√D), gray-body/point-source
    radiation; dual plume parents **EF-03 Heskestad + EF-04 McCaffrey** BOTH kept deliberately for a
    build-phase ablation. Geo (WS1b): infinite-slope **Factor of Safety** (saturated limit guard),
    **Iverson (2000)** transient head, **Fukuzono** inverse-velocity, **Caine** I–D rainfall threshold.
  - **Layer 2 (Class B, admitted-soft, derived + validation-gated): N = 4** — **B-06** sensor-response-
    corrected signal (parents EF-05/EF-10/EF-03, highest priority), **B-05** aliasing-aware flicker band
    (parent EF-08), **B-01** camera apparent flame height through smoke (parents EF-01/EF-07/EF-09),
    **B-02** dimensionless plume-temperature prior (parent EF-03).
  - **Layer 2 (Class C, documentation-only, hypotheses never results): N = 2** — **C-01** level-set/elliptical
    front ∘ Rothermel (simulator only), **C-02** full coupled forward camera model (synthetic-data simulator
    only). Class-C novel flicker/ND terms are **default OFF** with an A/B fallback (R20).
- **Alternatives considered / rejected here:** pyrolysis/Arrhenius kinetics as a live model — **not admitted
  (parked)**: not observable from our sensors/camera; could re-enter if a fuel-specific pilot needs it.
- **Admission principle (verbatim):** keep the set "as SMALL as the evidence allows and as large as it
  usefully needs"; admission = "defensible, usable, validatable later," **never** "works" (nothing is built).
- **Consequence:** every Class B/C item carries a validation roadmap vs named published data + mandatory
  **fire-science expert review** (`model_set_decision.md §(e)`); coefficients tagged `[coeff-verify]`.

### D-05 — Iverson transient bug-guard: slope enters ONLY via `D1 = D0/cos²β` (PATCH B)
- **Date/phase:** WS1 correctness fix (bugs #3/#17). **Status: adopted. [CONFIRMED]** (locked by golden test).
- **Decision:** In the Iverson (2000)/TRIGRS transient pressure-head term, the slope correction enters
  **only** through the diffusivity `D1 = D0/cos²β`; there is **no** spurious extra `·cosβ` on the transient
  term and no double `cos²β` on the static term. This is a **correctness** decision.
- **Why:** the shipped report (§6.2) carried an extra `·cosβ` on the transient term, introduced during
  report-writing downstream of a correct research file; it disagreed with canonical Iverson/TRIGRS
  (`TRINETRA_Bug_Report.md #3`, `#17`; `TRINETRA_Corrected_Patches.md`).
- **Alternatives considered:** leaving the shipped equation — rejected (physically wrong, inflates/deflates
  transient head with slope). Re-deriving from scratch — unnecessary; the project's own `research/06_physics
  §1.1` already stated it correctly.
- **Evidence:** `TRINETRA_Workstreams.md WS1` (PATCH B); `TRINETRA_Corrected_Patches.md`; authoritative
  TRIGRS implementations **arXiv 1305.4803** (Raia et al., TRIGRS-P) + **arXiv 1306.1529** (Alvioli et al.)
  confirm `D1 = D0/cos²β`. Regression lock: a golden unit test asserts the API equals the slope-free core at
  `D1 = D0/cos²β` and is **not** equal to the buggy extra-`cos²β` variant (chapter 13/17; `[CONFIRMED]`).
- **Consequence:** no downstream module consumes the buggy equation (Gate G1); the fix is permanently locked.

### D-06 — Fukuzono α=2 ⇒ inverse-velocity (1/v) linear regime (PATCH D)
- **Date/phase:** WS1 correctness fix (bug #4). **Status: adopted. [CONFIRMED]** (locked by golden test).
- **Decision:** Adopt the Fukuzono/Saito inverse-velocity failure-time model with the regime check
  **α=2 ⇒ 1/v linear**; for α≠2 the linear quantity is `v^(1−α)`. Carry a prediction interval.
- **Why:** the acceptance test (`Workstreams WS1 task 2`) requires `α=2 ⇒ 1/v` linear and `α≠2 ⇒ v^(1−α)`
  linear; this fixes the mis-stated inverse-velocity regime.
- **Alternatives considered:** fixing a single α for all slopes — rejected; α is a regime parameter.
- **Evidence:** `TRINETRA_Workstreams.md WS1` (PATCH D); Fukuzono prediction interval added in code
  (`25_changelog §25.3`). `_CANON §4` records "Fukuzono inverse-velocity failure time (α=2 ⇒ 1/v linear) with
  prediction interval."
- **Consequence:** inverse-velocity trend fitting is honest about regime and carries an interval, not a point.

### D-07 — Spatial-block CV over random CV; mandatory baselines; the real-win admission gate
- **Date/phase:** P4 (ranked DC-01/DC-02), enforced P14; Gate **G2**. **Status: adopted. [CONFIRMED]** (as a
  source-grounded doctrine; our own measurement = not measured).
- **Decision:** Replace every random/in-dataset split with **tile-withheld spatial-block CV** with a
  correlation-range buffer `g ≥ r`; mandate **GBDT + 3-rule decision tree + persistence/seasonal-naive**
  baselines in every table; rank by **cost-loss Value Score (TCC)**, not F1/AUC; a deep model that does not
  beat baselines under spatial-CV is reported as "does not beat baseline." Admission ("real-win") requires the
  improvement to exceed seed/trial variance on a held-out cross-site split (inferential-reproducibility gate).
- **The real-win admission gate (R16):** no performance claim may be made before this eval admission gate;
  `ReportGuard` enforces it in code (`_CANON §5`). G2 **blocks publication / any performance claim**.
- **Alternatives considered:** random CV (rejected — **overstates** skill); aggregate AUC across hazards
  (rejected — per-hazard with bootstrap CIs required).
- **Evidence (verbatim collapse number):** **arXiv 2608.12422** (`analysis/07 DC-01`, `_CANON §6`): naive
  terrain-susceptibility ROC-AUC ~0.90 collapses to **0.76 / 0.71 / 0.54** (GLOF burst / landslide /
  small-flood) under matched tile-withheld spatial-CV; "a simple GB / 3-rule tree ≥ deep." **arXiv 2610.08227**
  (effective-sample-size theorem: effective N = Θ(n²/r²); CI underestimate ∝ r). Cost-loss metric: 2510.22016
  (TCC), Bayes p* (Bug #1). Real-win gate: 2302.04054 (LMEM); tooling F-17.
  **Discrepancy:** `FINAL_REPORT §3/§4` cites **2608.22293** for this; `_CANON §6` says that ID is NOT in the
  source artifacts — use 2608.12422. Logged in §24.4.
- **Consequence:** this is the single most expensive-to-retrofit decision; it gates every downstream phase and
  is in the **NEVER-cut** set (D-15). Headline deliverable: a leakage-controlled Joshimath/Chamoli hindcast
  with a CI-bounded lead-time number (`Workstreams WS2`).

### D-08 — Conformal-under-shift (WCPS / ACI / Mondrian / CRC): calibrated members ≠ calibrated ensemble
- **Date/phase:** P7G/P14 (fusion calibration); features F-13. **Status: adopted. [CONFIRMED]** (as doctrine).
- **Decision:** The fused output is **re-calibrated per availability** with a shift-aware conformal stack:
  per-zone **Mondrian** conformal + **WCPS** (weighted CP under covariate shift) + adaptive/online **ACI** +
  **Conformal Risk Control (CRC)**, conditioned on the present-sensor mask and calibrated to the alarm
  **action loss**. Coverage is reported as **marginal + per-zone with CIs**, claimed as risk-control, **never**
  a fixed "90% guarantee."
- **Why (verbatim):** calibrated members ≠ calibrated ensemble (**2101.05397**); missing inputs break
  calibration (**2605.12517**) → the fused output must be re-calibrated per availability (`FINAL_REPORT §1`,
  WS1b). Vanilla split-CP collapses under moderate shift (**2604.22787**); valid only with reweighting
  (**2404.15018** WCPS); concept drift voids covariate-shift bounds (`FINAL_REPORT §7`).
- **Alternatives considered:** naive split-conformal (rejected — exchangeability broken by autocorrelation
  2303.12783 / missingness 2406.05405 / endogenous alarm-shift); a hard 1−α guarantee (rejected — overclaim,
  disciplines Bug #13; honest framing = approximate-under-stability).
- **Evidence:** `FINAL_REPORT §1/§7`; `FEATURES F-13` (2404.15018, 2402.07307, 2501.12749); `Workstreams WS3`
  (ACI/AgACI 2202.07282); action-loss refinement 2609.14821; mask-conditional 2512.14221; online 2610.02777.
  Code: ACI + Mondrian conformal + CRC implemented (`ws6_robust/conformal.py`, `25_changelog §25.3`) `[CONFIRMED
  present]`.
- **Consequence:** honest coverage reporting (Gate G3); conformal is in the **NEVER-cut** set (D-15). A tight
  interval must **never** suppress a physics-gated alarm (shield priority — ties D-11).

### D-09 — Meta-fusion head: FM-1 precision-weighted as Class-A default; GMF bounded residual; PHARAOH flag-gated OFF
- **Date/phase:** P14 (GMF, `TRINETRA_MetaFusion_Design.md`); P22 (PHARAOH). **Status: adopted. [HYPOTHESIS]**
  for the Class-B/C fusion pieces; **Class-A linear fallback is the default**.
- **Decision:** The decision head is a **Gated Meta-Fusion (GMF)** = stacking (Wolpert 1992) over experts
  {physics/Bayes base rule → p_phys + base action a₀; offline-RL logits/q-values; supervised/anomaly ensemble
  → p_sup}, emitting a **bounded residual** over a₀ (`â = clip(a₀ + residual)`; residual policy learning).
  Fusion-model options **FM-1..FM-6** (precision-weighted, evidential, conformal-stacked, covariance-
  intersection, physics-gated MoE, RL-tuned). **FM-1 precision-weighted mean is the Class-A default**;
  all Class-B/C fusion pieces are advisory, unvalidated, behind flags, with FM-1 fallback. The P22 **PHARAOH**
  operator (adaptive-order weighted power mean) is **Class C, flag-gated OFF** by default; it bends toward
  "max" only under a credible, physics-consistent alarm and fails open to "uncertain." Hierarchical two-layer
  fusion + correlation-aware **BLUE/GLS** weighting are included.
- **Novelty posture (honest, Rule 21 / CR-06):** GMF is a documented **engineering COMPOSITION** of known
  parts (stacking + bounded residual + per-zone Mondrian conformal + monotone shield); the novelty claim is
  withdrawn — "not found in N sources searched," not a new mechanism.
- **Alternatives considered:** a single learned fusion model (rejected — brittle on n≈5 events, Bug #1/#9/#13);
  presenting GMF as a novel algorithm (rejected — CR-06).
- **Evidence:** `TRINETRA_MetaFusion_Design.md` (Wolpert 1992; RPL 1812.06298; residual RL 1812.03201; shield
  1708.08611; IQL 2110.06169); `HLD §3`; `_CANON §4`; routing-collapse caution 2601.03425 (audit expert
  utilisation, F-07).
- **Consequence:** fusion fails safe to a linear Class-A combiner; all exotic operators are opt-in and gated
  (Gate G4: coefficient stability + reliability gating + shield-floor monotonicity).

### D-10 — The single decision function: `level = max(conformal_level(risk, p*), shield_floor)`; p* = 0.0476
- **Date/phase:** WS3 PATCH A; `HLD §2.3`. **Status: adopted. [CONFIRMED]** (one `decide()` in code; p* derived).
- **Decision:** EXACTLY ONE decision function exists:
  `level(s) = max( conformal_level(fused_risk(s), p*) , shield_floor(s) )`, mapping to
  {Green<Yellow<Orange<Red}. The alarm operating point is the Bayes cost-ratio threshold
  **p\* = C_FA / (C_FA + C_miss) = 5 / (5+100) = 0.0476**, i.e. a miss costs ~20× a false alarm.
- **Why:** removes the ~10× threshold conflict between the RL policy and the physics gate (Bug #1); every
  legacy threshold (0.5 / 0.12 / 0.048) maps to an internal role and no alert path bypasses `decide()`
  (unit-tested, `Workstreams WS3 task 1`).
- **Alternatives considered:** base-rate-dependent thresholds / multiple decision paths (rejected — Bug #1);
  F1/AUC-driven threshold (rejected — D-07/DC-02).
- **Evidence:** `HLD §2.3`; `_CANON §4` (p* = 0.0476, C_FA=5, C_miss=100); `Workstreams WS3`; cost-loss
  doctrine 2510.22016; Bayes p* (Bug #1).
- **Consequence:** one auditable operating point; shield can only RAISE (D-11); Gate G3 blocks deployment until
  the single `decide()` + measured conformal coverage are in place.

### D-11 — Monotone, post-posed hard safety shield (no training)
- **Date/phase:** P14/WS3; `MetaFusion §3`. **Status: adopted. [CONFIRMED]** (hard-coded, unit-tested).
- **Decision:** A deterministic monotone safety shield `S(s)` sits **after** the learner and can **only
  RAISE** the level (`final = max(conformal(â), S(s))`). It is **hard-coded, not trained**. Realizable rules
  (take the max over all triggered mandates): FS<1 ⇒ ≥Orange; **corroborated** tilt-rate >5°/day (≥2 nodes)
  ⇒ Red; 24 h rain >150 mm on high-susceptibility ⇒ ≥Orange; GLOF lake-drop + downstream stage-jump ⇒ Red;
  fire multi-node ⇒ ≥Orange. A single node alone **cannot** reach RED.
- **Why:** post-posed shielding preserves learner convergence while guaranteeing safety (Alshiekh et al. 2017);
  the "max over all triggered levels" form fixes the shield-realizability defect (Bug #20, 2507.23603 — stacked
  overrides can be mutually unsatisfiable); the ≥2-node corroboration fixes single-node false-RED (Bug #29).
- **Alternatives considered:** a learned/soft shield (rejected — safety must be deterministic & auditable);
  single-node RED trigger (rejected — fault-vs-event, D-16).
- **Evidence:** `TRINETRA_MetaFusion_Design.md §3`; `HLD §2.3`; **arXiv 1708.08611** (post-posed shield proof);
  realizability 2507.23603; code `shield_floor()` (`16_code_guide`, `[CONFIRMED]`).
- **Consequence:** the shield is the life-safety floor; a tight conformal interval can never suppress it; the
  thresholds (5°/day, 150 mm) are **planning values needing regional calibration — not measured**.

### D-12 — RL: offline, advisory, must beat MILP/non-RL; CQL/one-step; OPE deploy-gate; evac-env BUILD GAP
- **Date/phase:** P15; staged ladder DC-10/CR-03. **Status: adopted (gated). [HYPOTHESIS]** policy; **[CONFIRMED]**
  gating doctrine; evac environment is a **BUILD GAP**.
- **Decision:** The alarm policy ladder is **fixed-threshold → one-step offline RL → iterative RL ONLY if
  OPE-feasible + coverage proven**, with a stochastic-program alternative for the evacuation/dispatch
  sub-problem. RL is **advisory** (ranked options to a human dispatcher, never actuation), **offline** (no safe
  exploration; ~5 events), trained via **CQL/IQL** with the post-posed shield (D-11). Deployment is gated on
  **trustworthy OPE** (DataCOPE feasibility → BVFT policy selection → SCOPE-RL risk eval, CVaR@5%); deploy only
  if the OPE lower bound ≥ the rule baseline.
- **Why:** "better prediction ≠ better decision" (DFL, 2606.21773); naive RL underperforms (2509.19972); RL
  must beat strong non-RL baselines — MILP 2602.14676; one-step beats iterative on much of D4RL and is
  lower-variance (2106.08909). The meta-head reduces variance but **cannot manufacture statistical power** at
  n≈5 (`MetaFusion §5`).
- **BUILD GAP (verbatim):** no off-the-shelf disaster-evacuation RL environment exists — it must be built
  (`FINAL_REPORT §1/§14/§15 item 8`).
- **Alternatives considered:** pre-existing multi-stage CQL/IQL→TD3-BC→PPO plan (demoted — start one-step,
  CR-03); learned/time-varying reward shaping (rejected — potential-based only, 2608.08158, DC-11).
- **Evidence:** `FINAL_REPORT §1/§7`; `analysis/07 DC-10/DC-16`; `CR-03`; OPE stack 2311.14110 (DataCOPE),
  2110.14000 (BVFT), 2311.18206 (SCOPE-RL), 2106.08909, 2312.01530 (feedback-aware OPE).
- **Consequence:** RL is the last build step and only after the evac-env is built and the OPE gate passes.

### D-13 — CCTV: trained detector PRIMARY, zero-shot LOW-WEIGHT complement (D-011)
- **Date/phase:** P8 (+ compulsory zero-shot phase P14Z). **Status: adopted. [HYPOTHESIS]** (benchmark not run).
- **Decision:** The trained fire/smoke detector is **PRIMARY**; a zero-shot/foundation model is admitted
  **only** as a **calibrated LOW-WEIGHT complement** (internal decision **D-011**), never as a standalone
  alarm. A pre-registered, leakage-controlled zero-shot-vs-from-scratch benchmark (P14Z) must settle its value
  under spatial-CV + cost-loss before any weight increase.
- **Why:** in the fire domain, sources favour trained over zero-shot (2504.13231, 2610.10946, 2607.07951);
  TSFMs degrade under covariate noise (Chronos-2, 2610.07232) while robust from-scratch models hold (CR-08).
- **Alternatives considered:** zero-shot FM as primary (rejected — trained > ZS in-domain); dropping ZS
  entirely (rejected — kept as a low-weight OOD/ranking complement).
- **Evidence:** `FINAL_REPORT §1/§7` (D-011); `analysis/07 DC-13`; `CR-08`.
- **Consequence:** zero-shot cannot drive the alarm; its admission is contingent on the P14Z benchmark.

### D-14 — Deepfake/media: defensive-only, low-trust (reliability hard-cap 0.4), continuous red-teaming
- **Date/phase:** P11. **Status: adopted. [CONFIRMED-code]** cap; **[ABS]** method evidence.
- **Decision:** Forensic/provenance deepfake detection is **DEFENSIVE-ONLY**; all media/crowd/social signals
  are **low-trust advisory** confidence modifiers that must be **corroborated** and are routed through
  GMF+conformal+shield. The expert's reliability is **hard-capped at 0.4** (Class DATA), enforced **twice** —
  in the model config (`AuthenticityNet.max_reliability = 0.4`) and in the fusion adapter
  (`adapters._POLICY["deepfake"] = (0.30 default, 0.40 cap, Class DATA)`); a unit test asserts the cap.
- **Why:** defenses and evasions co-evolve (2003.01279) → continuous red-teaming; no detector family
  generalizes and dissemination worsens detection (RA-Bench 2608.14391); Rule 19 low-trust doctrine (`_CANON §6`).
- **Alternatives considered:** treating the detector at parity with physics/sensors (rejected — cross-generator
  collapse); using media as a sole gate (rejected — must be a corroborated modifier only).
- **Evidence:** `FINAL_REPORT §1` (WS2); `analysis/07 DC-04`; the 0.4 cap is `[CONFIRMED]` in code
  (`07_ws2_deepfake.md`, `05_MODELS.md`, `16_code_guide.md`); method evidence is `[ABS]`.
- **Consequence:** even a confident `p_fake` carries structurally small fusion weight (`r·c·exp(−u/τ)`); media
  can raise suspicion but never trigger an alert on its own.

### D-15 — Kaggle: PEFT / frozen-backbone over from-scratch pretrain; cut-list priorities; NEVER-cut set
- **Date/phase:** P5 (compute plan). **Status: adopted. [CONFIRMED]** (as a plan; no training run).
- **Decision:** Adapt **existing public checkpoints with PEFT (LoRA/AdaLoRA) / frozen-backbone probing** — do
  **not** pretrain a large FM from scratch on Kaggle. Budget ≈ 25.5 usable GPU-h/week (30 × (1−0.15)); push all
  non-training work to CPU; rank models frozen before any full fine-tune; anchor statistical rigor on cheap
  many-seed baselines (≥100 seeds on GBDT/persistence/small U-Net/conformal; 3–5 seeds on FM/SSL, reported as
  seed-limited).
- **Cut-list (dropped first if quota is tighter), in order:** (1) WS2 media fine-tune → stay zero-shot/rule;
  (2) full SSL pretrain → adapt a public checkpoint (SSL4EO-S12/TerraMind/Prithvi) with PEFT; (3) GLOF deep
  models → ITS_LIVE-velocity + HMAGLOFDB threshold rules; (4) nowcasting ensemble → single few-step model;
  (5) FM-comparison breadth → keep ONE FM.
- **NEVER-cut set:** GBDT + persistence baselines, spatial-CV, cost-loss eval, conformal calibration
  (cheap + they are the credibility of every number; DC-01/02/03).
- **Alternatives considered:** training several large FMs from scratch (rejected [INFEASIBLE] under budget).
- **Evidence:** `KAGGLE_BUDGET.md §2/§6/§8`; PEFT −95% params 2604.16663; small-corpus GFM 2605.28174; "should
  not need to pretrain" 2512.02055; frozen-FM baselines Prithvi-EO-2.0 2412.02732 / Galileo 2502.09356.
- **Consequence:** build fits ≤30 GPU-h/week (C3); credibility items are structurally protected from budget cuts.

### D-16 — IoT: ≤₹2000 tiered node; LoRa IN865–867 (reject 433 MHz); fault-vs-event discrimination
- **Date/phase:** P6/P13; WS5. **Status: adopted (gated by G5). [EST]** prices (not price-verified);
  **[CONFIRMED]** band/fault-logic design.
- **Decision:** Two ≤₹2000 nodes — Node A "Slope Sentinel" ≈ ₹1,930 [EST], Node B "River Eye" ≈ ₹1,980 [EST] —
  on a tiered compute model (Tier-0 node runs only a tiny statistical screen: Z-score/RMS tilt, stage
  threshold, on-node FS, 1/v fit, F-15 drift pre-correction; heavy models are Tier-1/2 only, C8). Radio is
  **LoRa SX1262 IN865–867 MHz**, which **replaces** the non-compliant 433 MHz SX1278 in the shipped BOM (bug
  #6; ~₹50 dearer, still clears ₹2000). Before any single node can drive a shield override, a **Neyman-Pearson
  fault-vs-event test + cross-node spatial-consistency check** must pass — so **one node cannot drive RED**.
- **Why:** 433 MHz is non-compliant for the India band; a stuck tilt sensor (fault) must not fire RED and a
  dead node must not mask a precursor (Bug #29).
- **Alternatives considered:** 433 MHz SX1278 (rejected — non-compliant); single-node RED trigger (rejected —
  fault discrimination required); running the VAD/SSL encoder on the MCU (rejected — Tier-1 only, Bug #14).
- **Evidence:** `TRINETRA_Workstreams.md WS5`; `HLD §4`; `FINAL_REPORT §8`; `_CANON §8` (band IN865–867,
  SX1262); fault-vs-event 1203.0541 / 1509.06065 / 2508.18045 / 2602.24209.
- **Consequence:** **Gate G5** (both totals ≤₹2000 after live price-verification + fault discrimination + band)
  blocks the hardware order. All ₹ figures are `[EST]` (suppliers returned HTTP 403) and NOT yet enforceable.

### D-17 — Offline-first DTN store-carry-forward; signed CAP; authenticated cell-broadcast
- **Date/phase:** P12; WS3/WS6. **Status: adopted. [CONFIRMED]** (DTN implemented) / **[UNVERIFIED]** on HW.
- **Decision:** The alert path is **offline-first**: a DTN **store-carry-forward** queue (binary Spray-and-Wait,
  copy budget L=8) carries readings/alerts when the uplink is down (C1); the Tier-1 siren at each site is
  independent of the cloud. CAP/SACHET alerts are **signed + deduped**; **cell-broadcast must be
  authenticated** because it is spoofable.
- **Why:** connectivity collapses in disasters (2511.15710) → offline-first is necessary; cell-broadcast is
  spoofable (**2604.24404**) → authenticate; no origination of official alerts without authority (D-20).
- **Alternatives considered:** cloud-dependent alerting (rejected — C1); unauthenticated broadcast (rejected —
  spoofable).
- **Evidence:** `FINAL_REPORT §1` (WS3); `HLD §5`; `FEATURES F-10` (DTN 1308.2907, Spray-and-Wait 2603.15945);
  code `ws3_alert/dtn.py DTNQueue` (`[CONFIRMED present]`); BLE last-100-m 2002.12906 (verify on HW).
- **Consequence:** the siren/SMS path works cloud-offline (Gate G6: offline alert path + no credential egress).

### D-18 — Feature admission waves: F-11..F-17 Wave-1 build; F-18..F-26 parked
- **Date/phase:** P17 formal admission; P18 Wave-1 specs. **Status: adopted. [ABS]** (all evidence abstract-level).
- **Decision:** Admit **Wave-1 (approved-for-build-plan): F-11** EFA-YOLO edge detector, **F-12** temporal
  multi-frame event validation, **F-13** conformal-under-shift WCPS, **F-14** label-free drift/calibration
  monitoring, **F-15** IoT GP drift correction, **F-16** unsupervised IR optical-flow/flicker physics feature,
  **F-17** experiment tooling + inferential-reproducibility "real-win" gate. **Wave-2 (F-18..F-22) proposed**
  and **Wave-3 (F-23..F-26) parked** — not specced; revisit only if budget remains.
- **Parking reasons (verbatim):** Wave-3 is parked on **budget/hardware/overfit-risk**, not rejected — e.g.
  **F-24** obscured-flame 3D-conv is an **OVERFIT RED FLAG** (2307.00104 "~100% video" treated as a red flag,
  not evidence); **F-25** thermal-IR needs IR hardware + calib rig that likely exceeds the ₹2000 cap; **F-26**
  UAV adaptive compression needs RL-style policy training → defer until the core detector is validated.
- **Admission rule (verbatim):** a feature is kept **only if** improvement exceeds seed/trial variance on a
  held-out cross-camera/cross-site split (significance gate 2302.04054) and cost is justified and it violates
  no hard constraint; a benchmark-local win that hurts cross-camera is **NOT a win**. No feature may consume
  the GPU reserve / hardware contingency.
- **Alternatives considered:** admitting Wave-2/3 now (rejected — insufficient evidence depth / cost / overfit).
- **Evidence:** `FEATURES.md` (P17 tables, all `weak(ABS)`); `FINAL_REPORT §9`. Nothing described as "working."
- **Consequence:** build order follows Wave-1 first (`FINAL_REPORT §14`); every feature carries a
  pre-registered decision rule it must pass or be rejected at P18.

### D-19 — Free-data-only; Kaggle-only compute
- **Date/phase:** master-program constraint. **Status: adopted (hard constraint). [CONFIRMED]**.
- **Decision:** Build compute is **Kaggle ONLY** (≤30 GPU-h/week, C3); datasets are **free-only** (ESA/NASA EO
  + free inventories); **no paid data / no paid cloud**. All discovered datasets are candidate `[D]`, license
  INDICATIVE/UNVERIFIED; **no selected dataset is paid** (none is selected).
- **Alternatives considered:** paid cloud / paid datasets (disallowed by the program).
- **Evidence:** `KAGGLE_BUDGET.md §Hard constraints`; `_CANON §5` (C3); `FINAL_REPORT §5`; `25_changelog §25.5`.
- **Consequence:** scope and cut-list (D-15) are shaped by free-only + Kaggle-only; dataset license verification
  is an OPEN backlog item.

### D-20 — Autonomous public alerting without certification/authority REJECTED [INFEASIBLE]
- **Date/phase:** program-wide (Rule 19). **Status: rejected (permanent). [INFEASIBLE]**.
- **Decision:** TRINETRA will **not** originate official public alerts without a certified authority; it never
  autonomously disseminates to the public.
- **Why:** life-safety domain + regulatory reality; who-may-originate official alerts is `[UNVERIFIED]`,
  flagged for qualified legal/standards review (`FINAL_REPORT §12`).
- **Alternatives considered:** none viable without certification/authority.
- **Evidence:** `FINAL_REPORT §4` (INFEASIBLE); `_CANON §6`; `25_changelog §25.5` (permanent).
- **Consequence:** the human operator + authority remain mandatory in the alert chain (ties D-01, D-17).

---

## 24.3 Superseded / corrected decisions (provenance of "we changed our minds")

| What was superseded | Replaced by | Why | Source |
|---------------------|-------------|-----|--------|
| Shipped Iverson transient equation (extra `·cosβ`) | `D1=D0/cos²β` ONLY (D-05) | geometrically wrong vs TRIGRS | Bug #3/#17; Corrected_Patches |
| Multi-stage CQL/IQL→TD3-BC→PPO as the starting policy | one-step offline RL first, iterate only if OPE-feasible (D-12) | one-step simpler/lower-variance; OPE gate | CR-03; DC-10 |
| GMF presented as a novel mechanism | GMF = documented engineering composition (D-09) | Rule 21 novelty = absence in sources searched | CR-06 |
| Non-compliant 433 MHz SX1278 radio | SX1262 IN865–867 MHz (D-16) | India-band compliance | Workstreams WS5 (#6) |
| Random cross-validation | spatial-block CV (D-07) | random CV overstates skill | _CANON §6; DC-01 |
| "Conformal 1−α guarantee" claim | risk-control, approximate-under-stability (D-08) | exchangeability broken; honest framing | Bug #13; CR-04 |
| Full SSL pretrain of a large FM on Kaggle | PEFT / frozen-backbone adaptation (D-15) | infeasible under budget | KAGGLE_BUDGET §6; 25_changelog §25.5 |

---

## 24.4 Known contradictions vs `_CANON.md` surfaced by this log

1. **arXiv ID for the spatial-CV collapse anchor (D-07) — RESOLVED, cite both.** `FINAL_REPORT.md §3/§4`
   cites **2608.22293**; the claims-table (C001–C003) cites **2608.12422**. An earlier `_CANON` draft wrongly
   called 2608.22293 "not in the artifacts, do not use it"; the **QG2 re-fetch (2026-10-10) confirmed
   2608.22293 is a real, on-point Palisades-wildfire paper** (random CV 0.92 → block 0.75) that is genuinely
   cited in FINAL_REPORT. `_CANON §6` now directs citing **both** — 2608.12422 (Himalaya) and 2608.22293
   (Palisades) are complementary second-domain confirmations of the same spatial-block-CV verdict, with
   2610.08227 the theoretical N_eff bound. No contradiction remains.
2. No other contradiction with `_CANON.md` was found: the Class A/B/C counts (12/4/2 = 18), p* = 0.0476
   (C_FA=5, C_miss=100), the single decision function, the IP-INFEASIBLE and fire-PINN-INFEASIBLE verdicts,
   the IN865–867 LoRa band, and the deepfake 0.4 cap all agree with `_CANON §4/§5/§6/§8`.

---

## 24.5 Decisions still OPEN / to be revisited

These are **not decided**; they are carried from the contradiction register, the open-backlog, and the
code-vs-doc audit. Do not design around them until resolved.

- **O-1 — Battery chemistry: LiFePO4 vs Li-ion 18650.** `DESIGN/HLD.md §4` + `TRINETRA_Workstreams.md WS5`
  specify **solar + LiFePO4** (cold-tolerant); `trinetra/firmware/FIRMWARE_SPEC.md` + the `ws7_iot/` BOM/
  SHOPPING_LIST/SAFETY specify a **Li-ion 18650 + small PV**. `_CANON §8` is silent on chemistry, so neither is
  canon. **Open** — resolve by a cold-performance + cost + safety trade at build (ties the ≤₹2000 gate G5).
  Source: `15_deployment_and_operations.md §15.9 C-1`; `PROGRESS_DOC CH15`.
- **O-2 — RL action cardinality: 3-action vs binary.** `deep/offline_rl.py` uses **3 actions**
  {HOLD, WATCH, ALARM}; the numpy baseline `rl.py RuleBaselinePolicy.act` is **binary** {0,1}. The 3→binary
  mapping used in the OPE-vs-baseline comparison is **implicit / not explicit in code** `[LIKELY]`. **Open** —
  fix the mapping explicitly before the OPE deploy-gate (D-12). Source: `10_ws5_rl.md §10.4`; `PROGRESS_DOC CH10`.
- **O-3 — Tilt-rate units (deg/s vs deg/day).** `ws7_iot/edge_screen.py` reads `tilt_rate_dps` (deg/**s**),
  while the shield rule (`COMPONENT_DESIGN.md §5`, `HLD/LLD`) is "tilt_rate > 5°/**day**." The code marks the
  thresholds illustrative/not-measured. **Open** — reconcile units and calibrate the 5°/day threshold
  regionally. Source: `15_deployment_and_operations.md §15.9 C-2`; `PROGRESS_DOC CH15`.
- **O-4 — Shield thresholds need regional calibration.** 5°/day, 150 mm/24 h, FS<1 are **planning values —
  not measured**; must be calibrated per region before field use (D-11). Source: `05_MODELS`, `HLD §10`.
- **O-5 — Dataset portals + license verification.** All datasets are candidate `[D]`, licenses UNVERIFIED
  (ISRO/NRSC/MOSDAC/Bhuvan/IMD/CWC/GSI portals JS-only). **Open backlog** (`FINAL_REPORT §15 item 2`).
- **O-6 — ≤₹2000 BOM price-verification.** All ₹ figures `[EST]` (suppliers returned HTTP 403); the ≤₹2000
  gate is NOT yet enforceable (G5). **Open** — re-quote with dates from ≥2 live Indian suppliers.
- **O-7 — India LoRa-band legality + alerting authority.** `[UNVERIFIED]` — who may originate official alerts;
  radio-band legality; fire-device certification. **Open** — qualified legal/standards review (`FINAL_REPORT §12`).
- **O-8 — Disaster-evacuation RL environment.** No off-the-shelf env exists; the evac-env is a **BUILD GAP**
  blocking the iterative-RL step (D-12). Source: `FINAL_REPORT §15 item 8`.
- **O-9 — Cross-zone conformal with upstream→downstream hydrological coupling (G2).** Open research item (P14),
  carried from DC-19 / CR-04 residual. Source: `analysis/07 DC-19`; `analysis/06 CR-04`.
- **O-10 — EVT / tail-risk head.** Carried as a wide-uncertainty **prior** (zoning), never a hard threshold;
  EVT estimates are high-variance in data-sparse mountains. Open (DC-07 / THREAD J). Source: `analysis/06`.
- **O-11 — Rockfall (rigid-block) coverage gap (G7).** Not covered by the saturated-slope stack; open (DC-20).
- **O-12 — Human-compliance / cry-wolf reward model.** Thinly sourced on arXiv (one hard number, 46% compliance
  2109.07745); resolve with non-arXiv NHESS/IJDRR evidence (D-010). Source: `analysis/07 DC-18`; `CR C-12`.
- **O-13 — Rockfall/EO constants & I–D thresholds.** Caine/Dahal–Hasegawa/Garhwal I–D constants to be verified
  or replaced by a fitted local distribution (bug #15, 2106.15119). Source: `Workstreams WS7 task 3`.
- **O-14 — Independent re-resolution of subagent-reported arXiv IDs.** Residual risk from the web_search
  outage; sampled, not fully re-fetched (`_CANON §7`). Open.

---

*End of chapter 24. This log records decisions as evidenced in the artifacts; where evidence is abstract-only
it is tagged `[ABS]`, where unverified `[UNVERIFIED]`, and no decision rests on a measured TRINETRA result —
because there is none (`_CANON §0`).*
