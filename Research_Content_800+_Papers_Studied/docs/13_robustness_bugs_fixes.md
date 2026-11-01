# 13 — Robustness, Bugs, and Fixes

> **What this chapter is.** The honest defect record of TRINETRA (HIMKAVACH): the catalogue of ways the
> system can fail, the full ledger of the 33 prior audit findings (#0–#32), a deep teardown of the
> high-severity bugs, the three Kaggle/DataParallel bugs found and fixed in the code-hardening session,
> and the strategy that makes the fixes stick. Primary sources, read for this chapter: `TRINETRA_Bug_Report.md`
> (findings #0–#32), `TRINETRA_Bug_Robustification.md` (FIX #0–#15 + Appendices C/D/E),
> `TRINETRA_Corrected_Patches.md` (PATCH A–I), [analysis/05_failure_mode_catalogue.md](../analysis/05_failure_mode_catalogue.md),
> [analysis/06_contradiction_register.md](../analysis/06_contradiction_register.md), and the fix code in
> `trinetra/src/trinetra/` + the golden tests in `trinetra/tests/`.

> **Honesty framing you must carry out of this chapter (see `_CANON.md §1`).** Every "before/after" below is a
> **CORRECTNESS before/after** — the equation now matches the published form / the golden test now passes / the
> crash is now gone. **None of it is a skill or accuracy measurement.** No TRINETRA model has been trained and
> no dataset has been downloaded, so there is no measured recall, false-alarm rate, or lead-time to report
> (`_CANON.md §0`). Where a *paper* reports a number, it is kept visibly separate and tagged with its arXiv ID.
> The 33 prior findings are treated as **BACKGROUND to be re-examined, not inherited as settled fact**
> (`analysis/05` header; `ASSUMPTIONS.md` A-09). Claims are tagged `[CONFIRMED]` / `[LIKELY]` / `[HYPOTHESIS]` /
> `[INFEASIBLE]`.

---

## 13.1 Failure-mode catalogue — overview, grouped by root cause

The running failure-mode catalogue lives in [analysis/05_failure_mode_catalogue.md](../analysis/05_failure_mode_catalogue.md)
(FM-01 … FM-40). Its life-safety framing is explicit: a **missed alarm = death risk**; a **false alarm = trust
erosion → future missed compliance** (cry-wolf). The system **complements, never replaces**, certified official
warning systems, with a human on every real alert (Rule 19). Below the 40 modes are regrouped by the seven root
causes the handover frame cares about. Each mode keeps its catalogue ID so you can trace it back.

### A. Physics-correctness failures
The hazard physics is mostly right (the audit's own conclusion), but a mis-derivation anywhere in the gate
produces a *confidently wrong* number that the rest of the pipeline trusts.
- **FM-13** — physics bugs: Iverson slope term, suction-stress sign, inverse-velocity α regime, unverified I–D
  constants (Bug #1–#4, #15). Mitigation: re-derive on paper, Class A/B/C labels, golden tests. *Status in code:
  the three equation bugs are **fixed and golden-tested** (§13.3); the empirical constants remain `[verify]`.*
- **FM-24** — the map from Factor-of-Safety error to failure-*probability* is strongly nonlinear: ~3% FoS RMS can
  become up to a 2× error in a ~10⁻³ failure probability, and reliability methods disagree 2.6–8.3× (2610.04828).
  Mitigation: treat FoS as a hard **gate/threshold, not a calibrated probability**; flag for expert review.
- **FM-39/FM-40** — borrowing coseismic-landslide PINN physics for a rainfall trigger, or a surrogate that needs a
  calibrated solver the ungauged Himalaya lacks (2407.06785, 2507.15614). Mitigation: borrow PINN *structure*, use
  hydrological physics; fall back to EVT prior + physics gate + wide uncertainty where no calibration exists.

### B. Evaluation-validity / leakage failures
The audit's now-dominant theme: the evaluation, as originally framed, could not falsify its own claims.
- **FM-01 / FM-28** — spatial-leakage inflated skill. On TRINETRA's own hazards and region, honest
  tile-withheld spatial CV collapses a naive susceptibility **AUC ≈ 0.90 to 0.76 / 0.71 / 0.54**
  (GLOF-burst / landslide / small-flood) and **five DL models do not beat one gradient-boosted baseline**;
  a three-rule decision tree wins the lake-hazard case (Kahn et al., **arXiv 2608.12422**). FM-28 adds the theorem
  that random holdout under-estimates CI width ∝ spatial-correlation range r (2610.08227). Mitigation: tile-withheld
  spatial CV + GB/decision-tree + persistence baselines as the **admission gate** (Bug #11).
- **FM-02** — a forecaster silently collapsing to persistence yet scoring well on autocorrelated series
  (2509.18176). Mitigation: mandatory persistence + seasonal-naive baselines, skill scored on *change* windows.
- **FM-21 / FM-29** — metric mirage: AUC/F1 are functions of base rate, so ranking models across zones/seasons of
  different base rates misleads (2206.09981, 2510.22016). Mitigation: a cost-loss **Value Score** as the primary
  decision metric; never rank across imbalance ratios.
- **FM-14** — cross-region transfer (Uttarakhand → Himachal) failing under distribution shift. Mitigation:
  spatial-CV across regions + a drift monitor.
- **FM-19** — training/serving skew (features computed differently online vs in training) (2103.09783).

### C. Calibration-under-drift failures
A calibrated-looking confidence that is not valid in the regime that matters.
- **FM-03** — naive split-conformal is invalid under autocorrelation / missingness / endogenous feedback
  (2303.12783, 2406.05405, 2511.11567; Bug #13). Mitigation: online/adaptive CP + a drift monitor that *voids*
  the coverage bound. *Status in code: implemented (§13.6).*
- **FM-20 / FM-36** — proximity-bias overconfidence: a model is systematically overconfident in sparse input
  regions (rare storms, under-instrumented valleys) and temperature scaling does **not** fix it; transformers are
  worse than CNNs (2306.04590, 2610.01384). This is a *confident missed alarm exactly where data is thin* — a
  critical life-safety mode.
- **FM-30 / FM-31** — a nominally 90% *predictive* interval can cover the **decision (action) loss** at only ~85%
  (2609.14821), and mask-marginal conformal is invalid for the specific present-sensor set under non-random
  missingness (2512.14221). Mitigation: utility-aware, mask-conditional calibration reporting both coverages.
- **FM-37** — the model lags at the extreme transitions it exists to catch (2609.16707, 2509.10362). Mitigation:
  per-regime conformal widths + an explicit EVT tail prior.

### D. Security / egress failures
- **FM-16** — a proxy that forwards credentials to a non-official third-party host (Bug #12). Mitigation: remove
  the proxy; never forward bearer tokens off-domain; rotate any exposed key. *Status: no such proxy exists in the
  reference repo (§13.3).*
- **FM-26** — spoofable / over-trusted alert channel: unauthenticated public-warning SIBs can be spoofed; media
  provenance soft-bindings false-fire 5.9–15.3% on unmarked content (2604.24404, 2610.04151). Mitigation: sign CAP
  end-to-end, HMAC-authenticate the mesh, multi-channel corroboration before "authoritative"; provenance is a
  *confidence modifier only*.
- Load-bearing architectural verdict (`_CANON.md §6`): **IP-address-based alerting is [INFEASIBLE]** for
  life-safety targeting; public-IP exposure is a **security** concern (authenticated endpoints), not an alerting
  channel. Enforced in code by the fail-closed endpoint allow-list and the no-raw-video-egress gate (§13.6, C6/C7).

### E. IoT fault-vs-event failures
- **FM-04** — a sensor silently faulty (brownout / stuck) *fabricates* a hazard (false RED → fatigue) or *masks* a
  real precursor (miss), undetectably, with no cross-node consistency or fault model (1509.06065; Bug #8, #29).
  Mitigation: fault-vs-event hypothesis test + cross-node spatial consistency before any single node drives an
  override. *Status in code: partially addressed — the shield requires ≥2 corroborating nodes (§13.3, §13.6).*
- **FM-10** — energy starvation: a solar node cannot transmit during the multi-day storm it exists to watch
  (Bug #8). Mitigation: Value-of-Information-aware duty cycling + a reserved life-safety energy floor.
- **FM-11** — backhaul down (storm cuts the gateway) so alerts never reach people. Mitigation: delay-tolerant
  store-carry-forward (Spray-and-Wait).
- **FM-27** — a GLOF precursor lake-area change *below the SAR resolution floor* (Sentinel-1 GRD ≈ 900 m² minimum
  detectable), so a small-breach precursor is missed on exactly the dangerous case (2512.24117). Mitigation: custom
  S1 burst processing, multi-sensor fusion, and a *below-detection-floor* uncertainty flag — never an implicit
  all-clear.

### F. Fusion routing-collapse failures
- **FM-06** — Mixture-of-Experts routing collapses to a domain-invariant "standing committee" with no real
  specialization; hard Top-K routing is brittle (2601.03425, 2604.00801; CR-05). Mitigation: audit expert
  utilisation; soft gating. *Status in code: GMF uses soft gated weights, not hard Top-K (§13.3).*
- **FM-15 / FM-35** — missing-modality collapse (sat/CCTV/IoT outage) and *negative* cross-modal transfer (a stale
  SAR tile drags the alarm down) (2602.04904, 2608.15261; CR-07). The sharpened threat model (2609.15297): in a real
  hazard, missingness is **adversarial, not random** — the event destroys the highest-signal sensor exactly when it
  matters. Mitigation: route by task-utility before fusing; always emit an uncertainty flag on any absent layer.
  *Status in code: `missing_modality` adapter marks absent experts unavailable and widens uncertainty (§13.6).*
- **FM-18 / FM-23** — a reconstruction-based or foundation anomaly head reconstructs the anomaly *too well* →
  residual score collapses toward zero → silent miss (1904.02639, 2108.06852, 2610.06453). Mitigation: memory/normal
  subspace constraint + always keep a model-free detector + the physics gate.

### G. RL reward-inversion failures
- **FM-05** — the hard-override safety shield can be mutually *unrealizable* when two rules mandate different levels
  (2507.23603; Bug #20). Mitigation: define the shield as a monotone **max over a priority lattice**
  (Green<Yellow<Orange<Red), which is total and realizable by construction. *Status in code: implemented (§13.3).*
- **FM-08 / FM-22 / FM-25** — offline-RL high-variance / invalid OPE; a learned policy trusted without OPE
  feasibility; seed-luck masking a spec failure (2106.08909, 2311.14110, 2610.03369; Bug #9, #27). Mitigation:
  one-step baseline + an OPE-feasibility (positivity/ESS) gate + ≥100 seeds + fixed-threshold/persistence baselines.
  *Status in code: WIS-OPE value + positivity/ESS gate + a rule baseline the learned policy must beat (§13.3).*
- **FM-09** — cry-wolf: repeated false alarms erode trust → future non-compliance (2104.11422). This is why the FA
  cost is not a token −5 but a calibrated cost-loss term, and why the decision layer fails to "uncertain".
- **FM-33 / FM-34** — a headline catastrophe-rate drop with no evidence the policy *anticipates* the hazard
  (reacts, not predicts), and adaptive reward shaping breaking the potential-based-shaping optimality guarantee
  (2609.34041, 2608.08158). Mitigation: probe lead-time/anticipation explicitly; keep shaping potential-based.
- **FM-38** — a deepfake/AI-video detector treated as a verification oracle fails on crisis content (RA-Bench,
  2608.14391). Mitigation: deepfake/zero-shot/crowd signals are **low-trust advisory only**, corroborated, never
  autonomous (Rule 19; `_CANON.md §6`).

The **reward-inversion family (G)** is the one place where the catalogue bites a design decision that is still only
partially realised in code: the exposure-weighted, compliance-aware reward is specified (FIX #9/#32) but the numpy
core does not implement a trainable reward — it implements the **cost-loss decision economics** (`value_score`,
`p* = C_FA/(C_FA+C_miss) ≈ 0.0476`) and the **rule-baseline + OPE gate** that a learned policy must beat. That is
called out honestly in §13.3 (Bug #9) and §13.5.

---

## 13.2 Bug ledger — all 33 findings (#0–#32)

Severity and the original workstream label are copied from `TRINETRA_Bug_Report.md`. The **status** column is this
chapter's re-examination against the reference code and the patch set — **not** an inheritance of the audit's own
claims (A-09). Meaning of status:
- **fixed** — corrected in the reference code *and* locked by a test/CI gate, or corrected verbatim in the report by a patch.
- **mitigated (code)** — the mechanism that addresses it exists in the numpy core but the full fix needs real data/training.
- **design** — the fix is specified (Robustification / MetaFusion design) but is architecture/data work, not a code line.
- **background** — a research-program/process or documentation finding, not a reference-code defect.

Workstream key uses the doc frame (`_CANON.md §3`): WS1 physics+fusion, WS2 deepfake, WS3 alerting, WS4 CCTV,
WS5 RL, WS6 robustness/IoT/eval. "Internal" labels (M#, C#) are the audit's own and shown where cited.

| ID | Short description | Workstream | Severity | Status | Fix reference |
|----|-------------------|-----------|----------|--------|---------------|
| #0 | QA "bugfix" workflow logged `completed` but aborted on billing — fixes never applied | process | CRITICAL | background | PATCH H; FIX #0 |
| #1 | ~10× unreconciled evacuate threshold (0.5 vs 0.12 vs 0.048) | WS5 (fusion) | CRITICAL | fixed | PATCH A; FIX #1; `decision.decide` |
| #2 | Suction-stress sign / representation in unsaturated FS (M1) | WS1 (geo) | MAJOR | fixed | PATCH C; FIX #2; `ws1b_geophys/fs.py` |
| #3 | Spurious cos β on Iverson ψ(Z,t) transient term (M1) | WS1 (geo) | MAJOR | fixed | PATCH B; FIX #3; `ws1b_geophys/iverson.py` |
| #4 | MS-IVE fits 1/v (α=2 only) while claiming free α 1.5–2.2 | WS1 (geo) | MAJOR | fixed | PATCH D; FIX #4; `ws1b_geophys/fukuzono.py` |
| #5 | arXiv 2603.15681 mislabelled "landslide" + cited AND denied (M7) | docs | MAJOR | background (fixed in report) | PATCH G; FIX #5 |
| #6 | 433 MHz LoRa is not an Indian ISM band (M6) | WS6 (IoT) | MAJOR | fixed | PATCH E; FIX #6; `config.py`, `FIRMWARE_SPEC.md` |
| #7 | Chamoli 2.5 h lead needs a seismic sensor the BOM lacked; EO backbone leaks future (C6) | WS6 (IoT) / eval | MAJOR | mitigated (code) + design | FIX #7; geophone now in `bom_price_check.py` |
| #8 | River Eye power browns out in the multi-day storm it watches (M2) | WS6 (IoT) | MAJOR | design | FIX #8 |
| #9 | RL reward: flat miss (−100) < disruption (−120 for 500 ppl·24 h) → prefers a miss (M5) | WS5 (RL) | MAJOR | mitigated (code) + design | FIX #9/#32; cost-loss + rule baseline + shield |
| #10 | Datacube size internally inconsistent 10–35× (2–5 TB vs 45–130 TB) (M3) | datasets/infra | MAJOR | design | FIX #10 |
| #11 | Evaluation underpowered, no scoring protocol — "beats LHASA" unfalsifiable (C4/C1) | eval | CRITICAL | mitigated (code) | PATCH I; FIX #11; `eval/` + ReportGuard |
| #12 | Proxy forwards API creds to non-official `api.justwoker.icu` | infra | MEDIUM | fixed (absent from repo) | FIX #12 |
| #13 | "Guaranteed 90% coverage" overstated and shield-voided (C5) | WS6 (robust) | MEDIUM | fixed | PATCH F; FIX #13; `ws6_robust/conformal.py` |
| #14 | "<1 s on-edge / 57 fps" is an L40S server-GPU number, not Jetson | WS4 (CCTV) | MAJOR | design | FIX #14/#30 |
| #15 | I–D / GLOF empirical constants unverified to primary source | WS1 (geo) | MEDIUM | open | FIX #15 |
| #16 | Novelty claimed while its own "check arXiv/Scopus" gate was still open | docs | MAJOR | background | FIX #16 |
| #17 | Iverson error was introduced in report-writing, not inherited (root-cause localisation) | WS1 (geo) | LOW | fixed | PATCH B; FIX #17 |
| #18 | Missed prior art (FM landslide mapping, GLOF multimodal, InSAR precursor) | docs | MAJOR | background | FIX #18; Appendix C |
| #19 | Forecasting head never benchmarked vs persistence | eval | MAJOR | design | FIX #19; PATCH I |
| #20 | Hard-override shield can be mutually unrealizable | WS5 (RL) | MAJOR | fixed | FIX #20; `ws5_fusion_rl/shield.py` |
| #21 | GMF meta-head multicollinearity (correlated experts) | WS5 (fusion) | MAJOR | mitigated (code) + design | FIX #21; bounded residual in `gmf.py` |
| #22 | Deep-SVDD hypersphere collapse + contaminated "normal" background | WS6 (anomaly) | MAJOR | design | FIX #22 |
| #23 | Endogenous feedback shift not in the OPE | WS5 / eval | MAJOR | design | FIX #23 |
| #24 | Conformal breaks under missingness + feedback + autocorrelation | WS6 (robust) | MAJOR | mitigated (code) | PATCH F; FIX #24; ACI + drift monitor |
| #25 | Rainfall-forecast spatial-displacement error unmodeled | WS1/WS3 (input) | MAJOR | design | FIX #25 |
| #26 | Shield is a conservative fixed-fallback RTA (suboptimal) | WS5 (RL) | MAJOR | design | FIX #26 |
| #27 | Alarm policy reported on simulator return, not honest OPE | WS5 (RL) | MAJOR | mitigated (code) | FIX #27; `rl.ope_admission` |
| #28 | GMF has no per-modality reliability gating | WS5 (fusion) | MAJOR | mitigated (code) | FIX #28; `effective_weight`, `missing_modality` |
| #29 | Sensor fault vs real event not separated | WS6 (IoT) | MAJOR | mitigated (code) + design | FIX #29; shield `nodes_agree≥2`, two-cue edge screen |
| #30 | Edge compute budget contradicts the heavy stack | WS6 (IoT) | MAJOR | mitigated (code) + design | FIX #30; `edge_screen` Tier-0 |
| #31 | No single fusion strategy dominates (per-class reporting missing) | eval | MAJOR | mitigated (code) | FIX #31; `MondrianConformal` per-group |
| #32 | People-at-risk & reward assume 100% uniform evacuation compliance | WS5 (decision) | MAJOR | design | FIX #32 |

Count check: **33 findings, #0–#32** — 19 from direct report/code audit (#0–#18), 14 literature-grounded
(#19–#32), matching the Bug Report's own tally. The patch set `TRINETRA_Corrected_Patches.md` closes the
single-line-editable ones (A–I); the rest are design/architecture work recorded in `TRINETRA_Bug_Robustification.md`
(FIX #0–#15 + Appendix E) and `TRINETRA_MetaFusion_Design.md`.

---

## 13.3 High-severity bugs — full entries

Each entry gives description → file/line → severity → reproduction → root cause → the fix → **correctness**
before/after → supporting paper (arXiv) → status. All "before/after" statements are correctness statements, not
skill measurements.

### Bug #3 — Spurious cos β on the Iverson transient term  [PATCH B]  [CONFIRMED fixed]

- **Description.** The shipped report's transient pressure-head equation carried an extra `·cos β` on the transient
  term *and* `cos²β` on the static term, where the canonical Iverson (2000) / TRIGRS form lets the slope enter the
  transient term **only** through the diffusivity `D₁ = D₀/cos²β`.
- **Where.** Report §6.2 line 358 (`ψ(Z,t) = (Z−d)·cos²β + 2·(I_z/K_s)·cos β·√(D₁t)·ierfc(…)`). Fix code:
  [trinetra/src/trinetra/ws1b_geophys/iverson.py](../trinetra/src/trinetra/ws1b_geophys/iverson.py#L28-L46).
- **Severity.** MAJOR / physics. The error propagates into every downstream `FS(Z,t)` and into the physics gate,
  so a wrong pressure head becomes a wrong Factor of Safety becomes a wrong shield floor.
- **Reproduction (correctness, not skill).** Evaluate the report's `ψ` at any β>0 and compare to the TRIGRS form;
  the two differ by the factor `cos β` on the transient term. The golden test
  [test_geophys.py::test_slope_only_through_D1](../trinetra/tests/physics_golden/test_geophys.py#L49-L58)
  asserts the API result equals the slope-free core evaluated at `D₁ = D₀/cos²β` **and** is *not* equal to a buggy
  version multiplied by an extra `cos²β` — i.e. it fails if the spurious factor is reintroduced.
- **Root cause (localised by Bug #17).** The project's own `research/06_physics §1.1` stated the equation
  *correctly*; the extra cosine was introduced during report-writing, downstream of correct research. So the bug was
  a transcription defect, not a knowledge defect — which is why the fix is a verbatim restoration plus a regression
  test.
- **The fix.** `iverson.py` implements `diffusivity_D1(D0, beta) = D0 / cos²(beta)` as the single place slope
  enters, and a **slope-free** `_transient_core` that callers reach only through `transient_head`, which passes the
  already-slope-adjusted `D₁`. There is structurally no path for a second cosine. A multi-pulse superposition
  (`transient_head_multipulse`) is built on the same unit response, preserving the bug-guard.
- **Before/after (correctness).** *Before:* `ψ` carried `·cos β` on the transient term → disagreed with Iverson
  (2000) / TRIGRS. *After:* `ψ = (Z−d)cos²β + 2(I_z/K_z)√(D₁t)·ierfc(Z/(2√(D₁t)))`, slope only via `D₁`; the golden
  test confirms the equation now matches the published form and `ierfc(0)=1/√π`, `ψ(t=0)=0`.
- **Supporting papers.** Iverson (2000), *Water Resources Research* 36(7):1897–1910; TRIGRS implementations
  **arXiv 1305.4803** (Raia et al., TRIGRS-P) and **arXiv 1306.1529** (Alvioli et al.) — both confirm `D₁ = D₀/cos²β`
  with no extra transient cosine.
- **Status.** **fixed** (code + golden test); report corrected by PATCH B.

### Bug #2 — Suction-stress sign in the unsaturated Factor of Safety  [PATCH C]  [CONFIRMED fixed]

- **Description.** The report defined suction stress with a leading minus and a symbol-table note "σ_s negative =
  adds strength," yet wrote the FS term as `− σ_s(…)`. With σ_s negative, a leading minus *subtracts* strength as
  suction rises — the opposite of the physics. The sign bookkeeping was self-cancelling and would flip the
  stabilising term if implemented naively (the audit's internal **M1**).
- **Where.** Report §6.3 lines 381–382 + the symbol table at line 393. Fix code:
  [trinetra/src/trinetra/ws1b_geophys/fs.py](../trinetra/src/trinetra/ws1b_geophys/fs.py#L23-L43).
- **Severity.** MAJOR / physics — the sign of the stabilising term decides stable vs unstable at the margin.
- **Reproduction (correctness).** Sweep saturation / suction and watch the sign of `dFS/d(suction)`. With the
  ambiguous convention it can come out negative (wetter → more stable), which is non-physical.
- **Root cause.** A convention clash: "σ_s ≤ 0" together with an explicit `− σ_s` in the FS, with no single stated
  sign rule, so the term's sign depends on an unstated downstream assumption.
- **The fix.** `fs.py` adopts one unambiguous convention: suction enters through an effective normal stress
  `σ'_n = γ z cos²β − u_w + σ_s`, with **σ_s ≥ 0** apparent-cohesion stress that **vanishes at saturation**
  (`Se→1 ⇒ σ_s→0`), recovering the classic saturated effective-stress form. FS is then the standard
  `[c' + σ'_n·tanφ'] / (γ z sinβ cosβ)`.
- **Before/after (correctness).** *Before:* increasing suction could *reduce* FS (sign flip). *After:* the golden
  tests pin three invariants — [test_geophys.py::TestFS](../trinetra/tests/physics_golden/test_geophys.py#L21-L38):
  (1) `σ_s=0` equals the saturated form **exactly**; (2) FS strictly **increases** with suction; (3) FS **decreases**
  as pore pressure `u_w` rises. All three now hold.
- **Supporting papers.** Lu & Likos (2006) suction-stress characteristic curve; **arXiv 2411.04333** (Roy &
  Chakraborty, IIT Madras/BHU) on van Genuchten SWCC with independent m,n and the sign/shape coupling — an
  India-authored primary source.
- **Status.** **fixed** (code + golden test); report corrected by PATCH C.

### Bug #4 — Fukuzono inverse-velocity: α=2 regime vs free α  [PATCH D]  [CONFIRMED fixed]

- **Description.** The report fit the straight-line inverse-velocity relation `1/v = A(α−1)(t_f−t)` — which is
  linear in `1/v` **only when α = 2** — while simultaneously advertising α as a free parameter in 1.5–2.2. For
  α ≠ 2 the linear quantity is `v^(1−α)`, not `1/v`. Mutually inconsistent (internal **M1**).
- **Where.** Report §6.6 lines 416–418, 428. Fix code:
  [trinetra/src/trinetra/ws1b_geophys/fukuzono.py](../trinetra/src/trinetra/ws1b_geophys/fukuzono.py#L59-L86).
- **Severity.** MAJOR / physics — a mis-specified regime biases the forecast failure time `t_f`, the single most
  decision-relevant geo output.
- **Reproduction (correctness).** Generate a slope with a known α ≠ 2 and fit `1/v` linearly; the recovered `t_f` is
  biased because the wrong variable was linearised.
- **Root cause.** Conflating the general Voight (1988) power law with its Fukuzono (1985) α=2 special case.
- **The fix.** `inverse_velocity_fit` picks the linearised variable from α explicitly: `y = 1/v` when
  `|α−2| < 1e-9`, else `y = v^(1−α)`, and records a `regime_note` saying which. It adds recency-weighted least
  squares and a **prediction interval** on `t_f` via the regression covariance + delta method, so an operator gets
  `t_f ∈ [low, high]`, not a false point certainty (Rule 19).
- **Before/after (correctness).** *Before:* "α=2" asserted while the general `A(α−1)` factor and `1/v` linearity
  were both carried. *After:* each regime is stated cleanly and tested —
  [test_geophys.py::TestFukuzono](../trinetra/tests/physics_golden/test_geophys.py#L61-L69) recovers `t_f=100` with
  r²>0.999 at α=2, and [test_fukuzono_ci.py](../trinetra/tests/physics_golden/test_fukuzono_ci.py) checks that a
  noiseless fit gives ~zero `t_f` uncertainty while noise *widens* the interval and still brackets the truth.
- **Supporting papers.** Fukuzono (1985); Voight (1988); **arXiv 2103.10939** ("The Landslide Velocity");
  **arXiv 2007.02756** (Bevilacqua et al., INGV) — real-data stochastic failure-forecast on GPS displacement, the
  cite for the probabilistic `t_f`.
- **Status.** **fixed** (code + golden tests); report corrected by PATCH D.

### Bug #1 — The ~10× unreconciled decision threshold  [PATCH A]  [CONFIRMED fixed]

- **Description.** Three numbers governed the same life-safety action with no master rule: physics gate `P_f ≥ 0.5`,
  LHASA `0.12`, RL Bayes-optimal `p* ≈ 0.048`. (The arithmetic of each is individually correct —
  `p* = C_FA/(C_FA+C_miss) = 5/105 = 0.0476` ✓ — but they are different probabilities of different quantities.)
- **Where.** Report §6.5 / §7.7 / §9. Fix code:
  [trinetra/src/trinetra/ws5_fusion_rl/decision.py](../trinetra/src/trinetra/ws5_fusion_rl/decision.py#L63-L102).
- **Severity.** CRITICAL / logic — ambiguity on the evacuate decision itself.
- **The fix.** One function, exactly one decision path:
  `level = max( conformal_level(fused_risk, p*) , shield_floor )`. The three legacy numbers are **reinterpreted,
  not averaged**: `0.12` and `0.048` become internal operating points of individual experts, and `P_f ≥ 0.5` becomes
  a **shield floor** (a hard monotone trigger that can only *raise* the level), never a probability competing with
  `p*`. This matches `_CANON.md §4` verbatim: `level = max(conformal_level(risk, p*), shield_floor)`,
  `p* ≈ 0.0476` with C_FA=5, C_miss=100.
- **Before/after (correctness).** *Before:* three competing thresholds, no master rule. *After:* a single monotone
  `max(conformal, shield)` decision function; `decision.decide` is the only code path that emits a level, and it is
  never silent — high conflict-aware uncertainty `U*` sets `uncertain=True` (abstain + escalate to a human).
- **Supporting method.** Conformal **Risk Control** — Angelopoulos, Bates, Fisch, Lei, Schuster, **arXiv 2208.02814**
  — bounds the expected miss-rate (the thing that kills people), replacing a coverage overclaim; implemented as
  `conformal_risk_threshold` (§13.6).
- **Status.** **fixed** (code); report corrected by PATCH A.

### Bug #12 — Credential-exfiltrating proxy  [FIX #12]  [CONFIRMED — no such proxy in the reference repo]

- **Description.** The audit found `Proxy.py` / `Proxy_fixed.py` hard-coding `target_url =
  "https://api.justwoker.icu"` and forwarding `x-api-key` / `Authorization: Bearer` headers to it — a non-official
  endpoint, so any key routed through it is exposed to that third party.
- **Where.** Historical tooling artifacts (`Proxy*.py`, lines 9–14 `build_headers`). **Confirmed this session:** a
  glob for `**/Proxy*.py` across the workspace returns **no files** — the proxy is not present in the reference code
  implementation. The `api_key` field was already empty in the audited copies (no key leaked in-repo).
- **Severity.** MEDIUM / security-tooling. (It is infrastructure/tooling, not a TRINETRA runtime component.)
- **Root cause.** A third-party API relay bundled with unrelated tooling, forwarding bearer tokens off-domain.
- **The fix (FIX #12).** Remove/`.gitignore` the proxy; never forward bearer tokens to non-official hosts; rotate
  any key ever sent through it; and confirm the historically-flagged leaked-SMTP credential was revoked.
- **Before/after.** *Before:* a proxy that could exfiltrate credentials existed in the audited tooling. *After:* no
  such proxy exists in the reference repo; the egress posture is enforced positively by the fail-closed endpoint
  allow-list and the no-raw-video-egress CI gate (§13.6, C6/C7).
- **Status.** **fixed** (absent from repo). Residual action I **could not verify** from inside this workspace: that
  the historical SMTP credential rotation was closed out (it lives in an external `plans/` artifact, not here).

### Bug #6 — 433 MHz LoRa is not an Indian ISM band  [PATCH E]  [CONFIRMED fixed]

- **Description.** Every node BOM specified "SX1278 Ra-02 LoRa 433 MHz." India's licence-exempt LoRaWAN allocation
  is **IN865–867 MHz**; 433 MHz is restricted, so a scaled Uttarakhand/Himachal deployment would be non-compliant,
  and the SF12 long-range mode would breach duty-cycle limits (internal **M6**).
- **Where.** Report BOM / comms (≈ lines 646+). Fix code:
  [config.py](../trinetra/src/trinetra/common/config.py#L27) (`"iot": {"lora_band": "IN865_867", …}`),
  [FIRMWARE_SPEC.md](../trinetra/firmware/FIRMWARE_SPEC.md#L7) ("Radio: SX1262 LoRa, **IN865–867**"),
  [lora_codec.py](../trinetra/src/trinetra/ws7_iot/lora_codec.py#L3) ("Target ≤51 B payload on IN865-867"),
  and the BOMs in [bom_price_check.py](../trinetra/scripts/bom_price_check.py#L16-L23) (SX1262 modules).
- **Severity.** MAJOR / hardware-legal — a regulatory non-starter for the flagship region.
- **The fix.** Respec every node to **IN865–867 MHz** with an **SX1262-class** transceiver (not SX1278/433); a
  terrain-aware link budget replaces the borrowed single Nepal 5 km figure; enforce the regional duty cycle.
- **Before/after (correctness).** *Before:* 433 MHz / SX1278 in the BOM — non-compliant. *After:* the config, the
  firmware spec, the codec docstring, and both node BOMs all specify IN865–867 / SX1262; the LoRa-frame CI gate
  (`G-iot`) additionally pins the payload ≤ 51 B so the duty budget stays sane.
- **Supporting source.** The TTN India frequency-plan table (`IN865–867`), live-verified in the audit session.
- **Status.** **fixed** (code/firmware/BOM); report corrected by PATCH E.

### Bug #11 — Spatial-leakage / random CV and the unfalsifiable evaluation  [PATCH I]  [mitigated in code]

- **Description.** Leave-one-event-out over ~5–6 heterogeneous events, with no defined decision unit, spatial
  tolerance, temporal hit window, false-alarm accounting, or confidence intervals. "Beats LHASA" was unfalsifiable
  as written. The over-determining external evidence: random CV **overstates** skill, and honest spatial CV on
  TRINETRA's own hazards collapses a naive AUC ≈ 0.90 to **0.76 / 0.71 / 0.54** while five DL models fail to beat a
  gradient-boosted baseline (a three-rule decision tree wins the lake-hazard case).
- **Where.** Report §9. Fix code: the `eval/` package — `splits.spatial_block_kfold`, `value_score`, `real_win`,
  `baselines` (climatology + numpy logistic), `report.ReportGuard`; and
  [train.admit_model](../trinetra/src/trinetra/deep/train.py#L171-L193), which runs the full gate.
- **Severity.** CRITICAL / evidence-validity.
- **Root cause.** Spatial autocorrelation leaks neighbourhood information between train and test under random CV,
  and n≈1/hazard cannot support any comparative claim.
- **The fix.** Make **tile-withheld spatial CV against a gradient-boosted / decision-tree baseline** the admission
  gate for every headline number (PATCH I); report each metric under *both* random-CV and spatial-CV and key all
  claims to the spatial-CV column; add persistence (forecasting), honest OPE (RL), and **per-hazard** reporting.
  `ReportGuard` is wired `spatial_cv=True` and refuses to let a metric be advertised unless the model beats
  climatology **and** a logistic baseline on spatial blocks with a CI (Rule 16).
- **Before/after (correctness).** *Before:* an unfalsifiable comparative claim on ~5 events. *After:* the code makes
  every claim falsifiable — but note honestly (`_CANON.md §0`): **no model has been trained and no dataset
  downloaded**, so there is still **no measured TRINETRA skill number** to run through the gate. The gate is built
  and unit-tested; it has not been fed a real hindcast. This is the residual-risk the Robustification spec calls the
  #1 gap: *one leakage-controlled Joshimath hindcast with a CI-bounded lead-time.*
- **Supporting papers.** **arXiv 2608.12422** (Kahn et al. — the on-region 0.90→0.54 collapse and "DL doesn't beat
  GB"); **arXiv 2510.10799**, **arXiv 2106.08909** (simpler beats complex); **arXiv 2610.08227** (finite-sample
  spatial-CV theorem); **arXiv 2509.18176** (persistence trap).
- **Status.** **mitigated (code)** — the evaluation *machinery* is implemented and tested; the real-data admission
  remains design/data work.

### Bug #20 — Shield mutually unrealizable → monotone priority lattice  [FIX #20]  [CONFIRMED fixed]

- **Description.** A set of hard-override safety rules can be mutually unsatisfiable: if a rain trigger mandates
  Orange while a tilt trigger mandates Red, a shield with no resolution rule is *undefined* on exactly the compound
  events (rain + tilt + GLOF) that are most dangerous.
- **Where.** Fix code: [trinetra/src/trinetra/ws5_fusion_rl/shield.py](../trinetra/src/trinetra/ws5_fusion_rl/shield.py).
- **Severity.** MAJOR (critical for compound events) / safe-RL.
- **The fix.** Define the shield as `S(s) = max{ level(r) : rule r fires }` over the totally ordered lattice
  Green < Yellow < Orange < Red, and the output as `â' = max(â, S(s))` (monotone — can only raise). A max over a
  total order always exists, so the shield is **total and realizable by construction**. The docstring states totality
  explicitly: "it always returns a defined Level for any input," and "a single faulty/uncorroborated node CANNOT
  reach RED — spatial corroboration is required" (ties Bug #29).
- **Before/after (correctness).** *Before:* undefined behaviour when two rules mandate different levels. *After:*
  `shield_floor` raises to the max of all triggered mandates; the tilt-rate RED trigger additionally requires
  `nodes_agree ≥ 2` and the GLOF RED requires lake-drop **and** downstream stage-jump, so a lone noisy sensor cannot
  force RED.
- **Supporting papers.** **arXiv 2507.23603** (shield realizability — rules can be mutually unsatisfiable);
  **arXiv 1708.08611** (safe RL via shielding); **arXiv 2305.16147** (CoCoRL convex safe set). FIX #26 (open) would
  further replace the fixed-fallback shield with a reachability-aware predictive one (**arXiv 2310.04288**).
- **Status.** **fixed** (code — monotone realizable lattice). FIX #26 (predictive shield) remains design.

### Bug #29 — Single faulty node → false RED  [FIX #29]  [mitigated in code + design]

- **Description.** A tilt sensor stuck at >5°/day (a *fault*) could fire a RED shield override (false alarm →
  fatigue), or a dead node could mask a real precursor (miss), undetectably, because there is no cross-node
  consistency or fault model and each reading is trusted per-node.
- **Where.** Fix code: [shield.py](../trinetra/src/trinetra/ws5_fusion_rl/shield.py#L33-L35) (`nodes_agree ≥ 2`
  required for the tilt-RED trigger) and
  [edge_screen.py](../trinetra/src/trinetra/ws7_iot/edge_screen.py#L22-L25) (local siren needs **two independent
  physical cues** — fast tilt-rate **and** heavy recent rain — so one noisy sensor cannot fire it).
- **Severity.** MAJOR / IoT.
- **Root cause.** Trusting a single node's reading as ground truth, with no fault-vs-event discrimination.
- **The fix.** Partial and layered: (1) the shield requires **≥2 corroborating nodes** before tilt can drive RED;
  (2) the Tier-0 edge screen requires two independent cues before a *local* siren (and never a public/network alert —
  Rule 19). The **full** fix (FIX #29) adds a formal Neyman-Pearson/Bayes fault-vs-event test and a robust streaming
  change-point detector — specified, not yet in the numpy core.
- **Before/after (correctness).** *Before:* one node could reach RED. *After:* RED requires spatial corroboration;
  a lone stuck sensor cannot fabricate RED, and the local siren needs two physical cues. The *fault-vs-event
  statistical test* is still design-level.
- **Supporting papers.** **arXiv 1509.06065** (DependSHM — faulty sensors cause undetected false diagnoses);
  **arXiv 1203.0541** (Neyman-Pearson/Bayes fault-vs-event test); **arXiv 2508.18045** (robust Riemannian
  change-point); **arXiv 2602.24209** (federated cross-node anomaly).
- **Status.** **mitigated (code)** for corroboration; **design** for the formal fault-vs-event test.

### Bug #13 — "Confident-while-wrong" alert gate and the overstated conformal guarantee  [PATCH F]  [fixed in code]

This is the "confident-while-wrong alert gate" requested item — it spans the conformal overclaim (Bug #13), the
drift-voiding, and the uncertainty-entropy abstention.
- **Description.** The report promised conformal coverage "with at least 90% probability — a mathematical guarantee."
  But exchangeability is broken by spatial autocorrelation and non-stationarity; sparse high-risk zones lack
  calibration data (the on-region competitor measured coverage falling to **82.9% overall and 45–59% in high-risk
  zones**); and the hard physics shield *overrides* the conformal output, voiding the guarantee on exactly the
  red-alert cases that matter.
- **Where.** Report §7.6/§7.7. Fix code:
  [trinetra/src/trinetra/ws6_robust/conformal.py](../trinetra/src/trinetra/ws6_robust/conformal.py) and
  [drift_monitor.py](../trinetra/src/trinetra/ws6_robust/drift_monitor.py); the gate itself is
  [decision.decide](../trinetra/src/trinetra/ws5_fusion_rl/decision.py#L63-L102) via the conflict-aware uncertainty
  `U*` ([nf.nf3_conflict_to_uncertainty](../trinetra/src/trinetra/ws5_fusion_rl/nf.py#L45-L52)).
- **Severity.** MEDIUM (conformal overclaim) rising to critical where it enables a confident missed alarm (FM-20).
- **The fix.** Three mechanisms:
  1. **No "guarantee" language.** `conformal.py`'s module docstring states plainly: "we report the REALIZED
     coverage; we never call the bound a 'guarantee' (it holds only under exchangeability … and is voided under
     concept drift)." It provides split-CP, weighted-CP for covariate shift, **AdaptiveConformal (ACI)** for
     long-run coverage under drift, **MondrianConformal** for per-group (per-hazard) coverage, and
     **conformal_risk_threshold** (CRC) that bounds the *miss-rate* — the life-safety quantity.
  2. **Drift voids the bound.** `drift_monitor.check_drift` (PSI) and CUSUM flag shift; when drift is detected the
     decision layer sets `reliability = Unreliable` and fails toward "uncertain" (Rule 19).
  3. **Confident-while-wrong gate.** `decide` computes `U* = Σ w_i u_i + λ·dispersion(p)` (conflict-aware
     uncertainty, an entropy-like disagreement score): when experts disagree or a layer is missing, `U*` rises, the
     prediction set widens, reliability drops, and `uncertain=True` escalates to a human — the system is never
     silently confident when it is actually in conflict.
- **Before/after (correctness).** *Before:* "guaranteed 90% coverage." *After:* measured marginal **and** per-zone
  coverage with CIs, online adaptive CP under drift, and risk-control framing; the advanced-conformal tests
  ([test_conformal_advanced.py](../trinetra/tests/robust/test_conformal_advanced.py)) confirm ACI holds long-run
  coverage ~90% under drift that would make static CP under-cover, Mondrian gives a *larger* GLOF quantile than
  landslide (rare class protected), and the CRC threshold bounds the realized miss-rate near target.
- **Supporting papers.** **arXiv 2106.00170** (Gibbs & Candès ACI); **arXiv 2208.02814** (Conformal Risk Control);
  **arXiv 2107.07511** (gentle intro / time-series CP); **arXiv 2306.04590** (ProCal — temp-scaling does not fix
  proximity overconfidence); **arXiv 2609.14821** (action-loss vs predictive coverage).
- **Status.** **fixed** (code + tests); report corrected by PATCH F.

### Bug #9 — RL reward inversion (prefer a miss over evacuating many)  [FIX #9/#32]  [mitigated in code + design]

- **Description.** The report's reward made a miss a flat **−100** while disruption was **−0.01 per person-hour**.
  For ~500 people evacuated 24 h, disruption = 0.01×500×24 = **−120**, which *exceeds* the −100 miss penalty — so for
  large exposed populations the cost-minimising policy could **prefer risking a missed disaster** to ordering an
  evacuation: the exact inversion of the intended safety bias. Bug #32 sharpens it: both terms also assume **100%
  uniform** evacuation compliance, whereas real compliance is ~46% plus shadow evacuation.
- **Where.** Report §9 MDP. Reference code: there is **no trainable reward in the numpy core** — the learned
  offline-RL policy is interface-only ([rl.OfflineRLPolicy](../trinetra/src/trinetra/ws5_fusion_rl/rl.py#L29-L39)
  raises `MissingDependency`). What *is* implemented is the cost-loss decision economics
  ([eval/value_score.py](../trinetra/src/trinetra/eval/value_score.py)) and the rule-baseline + OPE gate (`rl.py`).
- **Severity.** MAJOR / RL — a reward that can invert the safety bias.
- **Root cause.** A flat (exposure-independent) miss penalty against an exposure-scaling disruption penalty, so the
  ordering is not exposure-invariant.
- **The fix (FIX #9/#32, design) + what the code enforces today.** The specified fix makes **both** terms
  per-capita (exposure-invariant), with `C_miss_pc ≫ C_FA_pc`, so the ordering `oracle ≪ always-evacuate <
  never-evacuate` holds for *all* population sizes, plus a compliance probability and equity weighting. In the
  reference code this is approximated honestly by the **cost-loss convention**: `cost(alarm,no-event)=C_FA`,
  `cost(no-alarm,event)=C_miss`, optimal `p* = C_FA/(C_FA+C_miss) = 5/105 ≈ 0.0476` — the single operating point used
  by `conformal_level` and the `RuleBaselinePolicy` (threshold 0.0476). A learned policy may only be deployed if its
  **OPE value ≥ the rule baseline** and positivity/ESS holds (`ope_admission`), and the shield still bounds it from
  below.
- **Before/after (correctness).** *Before:* a flat −100 miss could be beaten by a −120 disruption → prefer the miss.
  *After:* the *implemented* decision economics are exposure-free at the threshold (`p*` is a per-decision cost
  ratio, not a population sum), and no learned policy can be fielded without beating the safe rule baseline under
  OPE. The full per-capita, compliance-weighted *reward* is specified but not yet trained (no RL run in this
  environment — `_CANON.md §0`).
- **Supporting papers.** **arXiv 2006.04779** (CQL), **arXiv 2110.06169** (IQL), **arXiv 2106.08909** (one-step
  offline RL), **arXiv 2311.14110** (DataCOPE OPE-feasibility), **arXiv 2311.18206** (SCOPE-RL risk/CVaR OPE);
  compliance: **arXiv 2109.07745** (Kincade Fire ≈46% compliance + shadow evacuation).
- **Status.** **mitigated (code)** via cost-loss + OPE gate + shield; **design** for the trained exposure-invariant,
  compliance-aware reward.

### Bug #5 — The 2603.15681 mislabel-and-denial  [PATCH G]  [background; corrected in report]

- **Description.** The report mislabelled a real Himachal **flash-flood** conformal paper as "landslide," cited it
  as a failing competitor, **and** simultaneously claimed "no landslide conformal paper exists" to support a novelty
  claim — a direct self-contradiction (internal **M7**).
- **Where.** Report lines 548/781 (mislabel) and 2842/2844 (the "no landslide papers → NOVEL" contradiction).
- **Severity.** MAJOR / integrity.
- **The fix (PATCH G).** Correct the label to "flash-flood susceptibility mapping in Himachal Pradesh (GraphSAGE over
  ~460 sub-watersheds, AUC 0.978; conformal UQ with empirical coverage 82.9% overall, 45–59% in high-risk zones)";
  delete the contradictory novelty sentence; **downgrade** the physics-gated per-zone conformal claim from NOVEL to
  **incremental** — the honest novelty is the *forecasting / pre-event* regime and the gated physics-shielded
  meta-fusion head, not conformal UQ per se. This aligns with the contradiction register's resolution of CR-06
  ("GMF = composition, not invention," Rule 21).
- **Before/after (correctness).** *Before:* a real paper mislabelled, strawmanned, and denied to exist. *After:*
  described identically everywhere; novelty restated honestly against the real prior art.
- **Supporting source.** arXiv **2603.15681** (Sharma & Sharma; verified live and present in the project corpus).
- **Status.** **background** finding (research-program documentation); corrected verbatim by PATCH G. Note per
  `_CANON.md §7`: paper identifiers in the ledger are mostly subagent-reported, a disclosed residual risk — this is
  a documentation-integrity fix, not a measured result.

---

## 13.4 The three Kaggle / DataParallel bugs (code-hardening session)

These three were found and fixed by reading the PyTorch `deep/` layer during the engineering phase. All three are
**crash / correctness** bugs that only bite under multi-GPU (Kaggle T4×2) or physics-only pretraining — exactly the
paths that are *not* exercised by the numpy unit tests, so they are documented here with root cause + fix + status.
The `deep/` layer is **py_compile-clean but never GPU-run in this environment** (`_CANON.md §2`), so "fixed" here
means the defect is removed in source and the reasoning is sound — **not** that it was observed passing on a GPU.

### (a) `geo_pinn_step` — `requires_grad_()` on a non-leaf scattered tensor under DataParallel

- **File.** [trinetra/src/trinetra/deep/geo_pinn.py](../trinetra/src/trinetra/deep/geo_pinn.py#L70-L88).
- **Root cause.** A PINN needs `Z, t` to carry gradients so the PDE residual can be formed with `autograd.grad`. The
  natural code `batch["Z"].requires_grad_(True)` works single-GPU. But `nn.DataParallel` **scatters** the input batch
  across GPUs, and each replica's slice is a **non-leaf** tensor (it is the output of the scatter op). Calling
  `requires_grad_(True)` on a non-leaf tensor raises `RuntimeError: you can only change requires_grad flags of leaf
  variables`. The PINN would therefore crash the moment it ran on 2× T4.
- **The fix.** Rebuild `Z, t` as **leaf** tensors inside the step: `Z = batch["Z"].detach().requires_grad_(True)`
  (same for `t`). `.detach()` severs the scatter history, producing a fresh leaf that both the single-GPU and the
  DataParallel paths accept, so `autograd.grad` for the Richards/Iverson residual works in both. The docstring
  records exactly this: "Z,t are rebuilt as leaf tensors via `detach().requires_grad_(True)` so autograd.grad works
  in BOTH the single-GPU path AND under DataParallel."
- **Status.** **fixed** in source (`.detach().requires_grad_(True)`); not GPU-executed here.

### (b) `make_loader` — `drop_last = shuffle` could drop a small fold's only batch

- **File.** [trinetra/src/trinetra/deep/train.py](../trinetra/src/trinetra/deep/train.py#L77-L91).
- **Root cause.** For DataParallel to split a batch evenly across GPUs you want `drop_last=True` on the shuffled
  training loader (an uneven last batch wastes/wedges a replica). But under **spatial-block CV** some folds are tiny;
  if such a fold has fewer than one full effective (GPU-scaled) batch, `drop_last=True` drops its **only** batch and
  the model trains on **nothing** for that fold — a silent no-op, not an error.
- **The fix.** Guard it: `drop_last = shuffle and len(ds) >= 2 * eff`, where `eff = batch_size × n_gpus`. drop_last
  is enabled only when there are at least two full effective batches; otherwise all data is kept. The docstring:
  "drop_last … BUT only when there are at least two full batches — otherwise a small fold could drop its only batch
  and train on nothing."
- **Status.** **fixed** in source; not GPU-executed here.

### (c) `GeoSeriesDataset` — `label=None` crashed `DataLoader` default_collate

- **File.** [trinetra/src/trinetra/deep/datamodules.py](../trinetra/src/trinetra/deep/datamodules.py#L34-L58).
- **Root cause.** In physics-only pretraining there are no labels. If `__getitem__` emits `{"label": None, …}`, the
  DataLoader's default `collate_fn` tries to batch a list of `NoneType` and raises (`default_collate` cannot collate
  `NoneType`). This crashes exactly the label-free PINN pretraining run the architecture depends on.
- **The fix.** Omit the key entirely when there is no label: the dataset only adds `item["label"]` when
  `self.label is not None`. Downstream, `geo_pinn_step` already guards with `if "label" in batch and
  batch["label"] is not None`, so a missing label cleanly means "physics-only objective." The inline comment records
  the reasoning: "A None value here would crash DataLoader's default collate … in physics-only pretraining runs."
- **Status.** **fixed** in source; consistent with the step function's `"label" in batch` guard.

All three are *multi-GPU / label-free-path* defects — invisible to the numpy test suite — so they are documented
rather than golden-tested. Their fixes are structural (leaf-tensor rebuild; size-guarded drop_last; omit-None-key)
and verified by reading the code, not by a GPU run (none is possible in this sandbox).

---

## 13.5 Robustification strategy — what actually transfers

The through-line of `TRINETRA_Bug_Robustification.md` and the contradiction register is a hierarchy of *how much a
defense transfers* beyond a single benchmark:

1. **Cross-sensor corroboration is the most transferable defense.** The deepest lesson from the physics,
   fault-vs-event, and missing-modality findings is that **no single model, hardened in isolation, is trustworthy for
   life-safety** — single-model hardening is *benchmark-local* (it helps the dataset you tuned on and may not survive
   spatial CV or a real storm; see 2608.12422's 0.90→0.54 collapse). What transfers is **requiring independent
   evidence to agree**: the shield needs ≥2 nodes before RED (Bug #29); the Tier-0 siren needs two physical cues; the
   GMF fuses physics + anomaly + encoder + forecast experts and *down-weights* any whose modality is degraded
   (`missing_modality`, `effective_weight`); deepfake/crowd signals are low-trust and must be corroborated (FM-38).
   Corroboration is cheap, interpretable, and does not depend on a trained weight staying valid under drift.
2. **Uncertainty-entropy alert gate over a point estimate.** The decision layer never emits a bare level. It carries
   a conflict-aware uncertainty `U* = Σ w_i u_i + λ·dispersion(p)` (an entropy-like disagreement score); high `U*`,
   a missing expert, or a drift flag force `uncertain=True` and fail toward "uncertain/offline" (Rule 19). This is
   the structural answer to the *confident-while-wrong* mode (FM-07/FM-20): the system is allowed to be unsure, and
   being unsure escalates to a human rather than firing or staying silent.
3. **Spatial-block CV, never random CV.** This is a load-bearing verdict in `_CANON.md §6`: random cross-validation
   **overstates** skill, so tile-withheld spatial-block CV against a gradient-boosted/decision-tree + persistence
   baseline is **mandatory** before any performance claim. The datamodules compute `spatial_block(lat,lon)` so
   training uses the *same* block scheme as eval — no leakage between train and test (gate G6).
4. **Physics as a hard gate, learned heads as a bounded residual.** FoS → failure-probability is too nonlinear to
   trust as a calibrated probability (FM-24), so FoS is a **threshold/shield input**, and the GMF learned head is a
   **hard-clipped bounded residual** (±`residual_cap`) over a precision-weighted physics mean — a mis-trained head
   can never dominate physics. Without a trained head the residual is 0 and GMF degrades gracefully to the mean.
5. **Honest valuation before deployment.** No learned RL policy ships unless its OPE value beats the fixed rule
   baseline *and* positivity/ESS holds (`ope_admission`), and no metric is advertised unless `ReportGuard` admits it
   on spatial blocks against baselines with a CI (Rule 16).

The residual risks the strategy explicitly **cannot** fix (from the Robustification residual-risk register): small
n cannot be turned into statistical power; InSAR physically decorrelates in snow/monsoon forest; and the single
biggest gap remains **zero real end-to-end demonstration** — one leakage-controlled Joshimath hindcast with a
CI-bounded lead-time is the highest-leverage action, and it has not been run.

---

## 13.6 How the golden tests + 6 CI gates lock the fixes against regression

Two mechanisms keep a corrected defect from silently coming back.

**Golden-case physics tests** (`trinetra/tests/physics_golden/`) encode each physics fix as an executable
invariant, so a regression fails the suite:
- Bug #3 (Iverson): `test_slope_only_through_D1` asserts `transient_head` equals the slope-free core at
  `D₁ = D₀/cos²β` **and** is *not* equal to a version with an extra `cos²β` factor — reintroducing the spurious
  cosine fails the test. `test_transient_zero_at_t0` and `test_ierfc_at_zero` pin the kernel.
- Bug #2 (suction sign): `TestFS` pins the saturated limit (`σ_s=0` ≡ saturated form), monotone-increasing in
  suction, and decreasing in pore pressure — any sign flip fails.
- Bug #4 (Fukuzono α): `TestFukuzono` + `test_fukuzono_ci` recover `t_f` at α=2 with r²>0.999 and check the
  prediction interval widens with noise and brackets the truth.
- Multipulse superposition (`test_iverson_multipulse`) checks single-step equivalence, finite-pulse recovery after
  rain stops, linearity, and intensity monotonicity — all on the bug-guarded `D₁`.
- The conformal fixes (Bug #13/#24) are locked by `test_robust` and `test_conformal_advanced`: marginal coverage,
  PSI/CUSUM drift detection, missing-modality uncertainty inflation, ACI long-run coverage under drift, Mondrian
  per-group quantiles, and CRC miss-rate control.

**The 6 CI gates** (`trinetra/scripts/ci_gates.py`) are fail-closed **safety/honesty** invariants, not performance
tests — any failure exits non-zero. They are, verbatim from the runner:
- **G-advisory** — human approval is hard-wired; `build_cap` refuses without an approval token (Rule 19).
- **G-classC** — Class-C paths (PHARAOH, ND₁–₇) default OFF (Rule 20).
- **G-security** — the endpoint allow-list is fail-closed and raw video cannot egress (C6/C7) — this is the positive
  enforcement that replaces the removed exfiltrating proxy (Bug #12) and backs the IP-alerting-is-a-security-concern
  verdict.
- **G-leak** — look-ahead feature timestamps are rejected (`assert_no_time_leak`), guarding against the temporal
  leakage half of Bug #11.
- **G-iot** — the LoRa frame stays within the ≤51 B budget (G5), keeping the IN865-867 duty budget sane (Bug #6).
- **G-legacy** — a source scan rejects **banned tokens**, including `EXTRA_COSBETA_ON_TRANSIENT` — a literal tripwire
  that fails CI if the Iverson spurious cosine (Bug #3) is ever reintroduced — and `advisory=False` (Rule 19).

Per `_CANON.md §2`, the state of these checks is `[CONFIRMED]` by the orchestrator running them:
`python run_tests.py` → **128 tests, OK** and `python scripts/ci_gates.py` → **ALL 6 CI GATES PASSED**. I did **not**
re-execute them inside this subagent (I read the sources); I am reporting the canon's confirmed status, not a fresh
run of my own.

---

## 13.7 Reference IDs → chapter 19

Every arXiv ID cited here is carried, with full detail and verification status, in
[19_REFERENCES_FULL.md](19_REFERENCES_FULL.md) and the row-level ledger
[analysis/02_paper_ledger.csv](../analysis/02_paper_ledger.csv). The load-bearing ones for this chapter:

| Finding / fix | arXiv ID(s) | Role |
|---|---|---|
| Bug #3 Iverson / TRIGRS | 1305.4803, 1306.1529 | `D₁=D₀/cos²β`, no extra transient cosine |
| Bug #2 suction stress | 2411.04333 | van Genuchten SWCC sign/shape (India-authored) |
| Bug #4 Fukuzono / Voight | 2103.10939, 2007.02756 | landslide velocity; real-data stochastic t_f |
| Bug #1 / #13 conformal | 2208.02814, 2106.00170, 2107.07511 | risk control; ACI; CP intro |
| Bug #11 spatial CV | 2608.12422, 2510.10799, 2106.08909, 2610.08227, 2509.18176 | leakage collapse; simpler-beats-complex; CV theorem; persistence |
| Bug #20 / #26 shield | 2507.23603, 1708.08611, 2305.16147, 2310.04288 | realizability; shielding; convex safe set; predictive RTA |
| Bug #29 fault-vs-event | 1509.06065, 1203.0541, 2508.18045, 2602.24209 | fault diagnosis; NP/Bayes test; change-point; FedIoT |
| Bug #9 / #27 / #32 RL | 2006.04779, 2110.06169, 2106.08909, 2311.14110, 2311.18206, 2109.07745 | CQL/IQL; one-step; OPE feasibility; risk-OPE; compliance |
| Bug #6 LoRa | TTN IN865-867 plan | Indian ISM band |
| Bug #5 prior art | 2603.15681 | Himachal flash-flood conformal |
| FM calibration/fusion | 2306.04590, 2609.14821, 2512.14221, 2402.01379, 2603.01511, 2608.15261 | proximity bias; action-loss coverage; mask-conditional CP; collinearity; reliability gating; negative transfer |

See `_CANON.md §7` for the honesty caveat on the ledger: identifiers are mostly subagent-reported and not all
independently re-fetched — a disclosed residual risk, not a verified-every-ID guarantee.

---

### Chapter self-audit (per the task's honesty rules)

- **Could-not-source items.** (1) Bug #12's residual action — confirmation that the historical SMTP credential was
  rotated — lives in an external `plans/` artifact absent from this workspace; I confirmed only that **no `Proxy*.py`
  exists in the repo**. (2) Bug #9's full exposure-invariant / compliance-weighted *reward* and the per-capita
  reward numbers are design-level (`TRINETRA_Bug_Robustification.md` FIX #9/#32) — there is **no trainable reward in
  the numpy core**, so I report the implemented cost-loss + OPE-gate approximation and label the rest design.
  (3) The I–D / GLOF empirical constants (Bug #15) remain unverified to primary source — recorded as **open**, not
  fixed. (4) The `deep/` fixes (§13.4) are verified by reading source only; they were **never GPU-executed** here.
- **No measured skill numbers** appear in this chapter; every before/after is a correctness statement. Paper numbers
  (e.g. 2608.12422's 0.90→0.54) are the papers' own, tagged with their arXiv IDs and kept separate.
