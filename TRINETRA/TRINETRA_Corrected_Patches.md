# TRINETRA — Corrected-Report Patch Set (apply to `TRINETRA_Complete_Report.md`)

**What this is.** Exact, line-anchored patches that fix the confirmed defects in the delivered report
(`C:\Users\Dell\Downloads\trinetra\deliverables\TRINETRA_Complete_Report.md`, v1.0, 2966 lines).
Each patch gives the **verbatim current text**, the **replacement**, the **bug ID** it closes, and the
**one-line justification**. Apply in order; line numbers refer to the original file (they shift as you
edit top-down, so apply bottom-up or re-locate by the quoted anchor string). Patches are grouped by
severity. Nothing here changes the project's concept — only its correctness.

Legend: `BEFORE` = exact string in the shipped report; `AFTER` = corrected string; `WHY` = justification +
bug cross-reference. Insert the `<!-- FIX #n: ... -->` HTML comment immediately above each patched block
so a reviewer can audit every change.

---

## PATCH A — Bug #1 (CRITICAL): reconcile the ~10× decision threshold

**Location:** §6.5, lines 406–413 (warning-level table) + a new master-decision note.

**BEFORE (lines 406–413):**
```
- Warning levels (initial values, to be tuned):

| Level | Rule |
|---|---|
| Green | P_f < 0.1 |
| Yellow (watch) | 0.1 ≤ P_f < 0.3 |
| Orange (prepare) | 0.3 ≤ P_f < 0.5 |
| Red (act / evacuate) | P_f ≥ 0.5, **and** at least one independent observation agrees (movement, anomaly, or stage) |
```

**AFTER:**
```
<!-- FIX #1: P_f here is the PHYSICS-GATE output, NOT the operational evacuate threshold.
     The single operational decision threshold is tau* from the calibrated meta-fusion /
     conformal layer (§9), tau* ≈ 0.05. P_f >= 0.5 is a SHIELD TRIGGER (a hard floor that can
     only RAISE the level), never a probability competing with tau* or the LHASA 0.12 operating
     point. See the master-decision note below. -->
- Physics-gate levels (these drive the SHIELD, not the final alarm):

| Level | Physics-gate rule (shield input) |
|---|---|
| Green | P_f < 0.1 |
| Yellow (watch) | 0.1 ≤ P_f < 0.3 |
| Orange (prepare) | 0.3 ≤ P_f < 0.5 |
| Red (shield floor) | P_f ≥ 0.5 → force level ≥ Orange (and ≥ Red if an independent observation — movement, anomaly, or stage — agrees) |

**Master decision rule (single source of truth).** The operational alarm level is produced by ONE
function: `decide(state) = max( conformal_level(risk, τ*),  shield_floor(physics, sensors) )`, where
`τ* ≈ 0.05` is the calibrated operating threshold on the fused risk (its arithmetic matches the
Bayes-optimal `p* = C_FA/(C_FA+C_miss) = 5/105 = 0.0476`, §9), the LHASA `0.12` is an *internal
operating point of the LHASA expert only*, and `P_f ≥ 0.5` is the *physics shield floor*. These three
numbers are no longer competing thresholds for the same decision.
```

**WHY:** closes Bug #1 — three numbers (0.5 / 0.12 / 0.048) governed the same life-safety action with
no master rule. One monotone `max(conformal, shield)` decision function dissolves the conflict.

---

## PATCH B — Bug #3 + #17 (MAJOR/PHYSICS): remove the spurious cosine on the Iverson transient term

**Location:** §6.2, line 358 (the Iverson ψ(Z,t) equation) + the D₁ row at line 367.

**BEFORE (line 358):**
```
**ψ(Z, t) = (Z − d)·cos²β + 2·(I_z/K_s)·cos β · √(D₁·t) · ierfc( Z / (2√(D₁·t)) ) — for t ≤ T; after the rain stops, the same term for (t − T) is subtracted.**
```

**AFTER:**
```
<!-- FIX #3/#17: Iverson (2000) transient term carries NO extra cos β. Slope enters ONLY through
     the diffusivity D1 = D0 / cos²β (line 367) and the steady term (Z−d)cos²β. The published form is
     ψ = (Z−d)cos²β + 2 (I_z/K_s) √(D1 t) · ierfc( Z / (2√(D1 t)) ). The project's own
     research/06_physics §1.1 states it correctly; the shipped report added a spurious ·cos β. -->
**ψ(Z, t) = (Z − d)·cos²β + 2·(I_z/K_s)·√(D₁·t) · ierfc( Z / (2√(D₁·t)) ) — for t ≤ T; after the rain stops, the same term for (t − T) is subtracted.**
```

**WHY:** closes Bug #3 (spurious `cos β` on the transient term) and Bug #17 (its root — the error
propagates into every downstream FS(Z,t), §6.2 line 372, and the physics gate). Confirmed against
Iverson (2000) *Water Resources Research* 36(7):1897–1910 and the project's own `research/06_physics`.
Note β = cos²δ − I_zLT/K_z and D₁ = D₀/cos²δ are the only places slope legitimately enters.

---

## PATCH C — Bug #2 (MAJOR/PHYSICS): fix the suction-stress sign/representation in the unsaturated FS

**Location:** §6.3, lines 381–382 + the symbol-table note at line 393.

**BEFORE (lines 381–382):**
```
- **Suction stress (Lu & Likos):** σ_s = −(S_e/α)·[S_e^(−1/m_v) − 1]^(1/n)
- Then FS becomes FS = tan φ'/tan β + [2c' / (γ·z·sin 2β)] − [σ_s·(tan β + cot β)·tan φ'] / (γ·z)
```

**AFTER:**
```
<!-- FIX #2: Sign/convention clash. With σ_s defined negative ("negative = adds strength", line 393),
     a MINUS sign in front of the σ_s term SUBTRACTS strength — the opposite of physics. Lu & Likos
     suction stress is σ_s = −S_e·ψ (σ_s ≤ 0 under suction), and in the FS it must ADD resistance as
     suction grows. Use a single consistent convention: keep σ_s ≤ 0 and write the term as
     − σ_s·(…)·tan φ' with the understanding that −σ_s ≥ 0 adds strength; OR flip to the magnitude
     form below. Shown here in the unambiguous magnitude form. -->
- **Suction stress (Lu & Likos):** σ_s = −S_e·ψ  (σ_s ≤ 0 under matric suction ψ > 0); equivalently via van Genuchten, |σ_s| = (S_e/α)·[S_e^(−1/m_v) − 1]^(1/n)
- Then FS becomes FS = tan φ'/tan β + [2c' / (γ·z·sin 2β)] + [ |σ_s|·(tan β + cot β)·tan φ' ] / (γ·z)
```

**WHY:** closes Bug #2 — the leading minus combined with "negative = adds strength" made rising suction
*reduce* FS. The corrected magnitude form guarantees that increasing suction increases FS, matching
Lu & Likos (2006) and the Fredlund strength eq. at line 379. (A sign audit against a saturated limit
`S_e→1 ⇒ σ_s→0` is the acceptance test.)

---

## PATCH D — Bug #4 (MAJOR): make the inverse-velocity / α statement internally consistent

**Location:** §6.6, lines 416–418 + 428.

**BEFORE (lines 416–418):**
```
When a slope accelerates towards failure, its velocity v often follows a simple law (Voight 1988): d²Ω/dt² = A·(dΩ/dt)^α, where Ω is displacement.

- For α = 2 (most common), inverse velocity falls on a straight line: **1/v = A·(α − 1)·(t_f − t)**
```

**AFTER:**
```
<!-- FIX #4: The straight-line inverse-velocity law 1/v = [A(α−1)]·(t_f − t) is the SPECIAL CASE
     α = 2 (Fukuzono 1985); then A(α−1) = A. Stating "α = 2" and keeping the general factor
     "A·(α−1)" is internally inconsistent and misleads calibration. For α ≠ 2 the plot of
     v^(1−α) (not 1/v) is linear. Keep ONE regime per sentence. -->
When a slope accelerates towards failure, its velocity v often follows a power law (Voight 1988): d²Ω/dt² = A·(dΩ/dt)^α, where Ω is displacement.

- For the common case **α = 2**, inverse velocity is linear in time: **1/v = A·(t_f − t)** (Fukuzono 1985). For general α ≠ 2 it is **v^(1−α)** that is linear: **v^(1−α) = A·(α − 1)·(t_f − t)**.
```

**BEFORE (line 428):**
```
| A, α | Empirical constants (α usually 1.5–2.2) |
```
**AFTER:**
```
<!-- FIX #4: keep the α range consistent with the two-regime statement above. -->
| A, α | Empirical constants (α usually 1.5–2.2; α = 2 ⇒ the linear 1/v regime) |
```

**WHY:** closes Bug #4 — the report asserted α=2 yet carried the general `A(α−1)` factor and the `1/v`
linearity simultaneously, which only coincide at α=2. Corrected to state each regime cleanly.

---

## PATCH E — Bug #6 (MAJOR/HARDWARE): 433 MHz is not an ISM band in India → use IN865–867

**Location:** IoT BOM / comms section (≈ lines 646+; anchor on the LoRa frequency string).

**BEFORE (anchor):**
```
433 MHz
```
(wherever the LoRa node frequency is specified in the BOM / comms design)

**AFTER:**
```
<!-- FIX #6: 433 MHz is NOT a licence-exempt ISM band in India for this use. India's LoRaWAN
     allocation is IN865–867 MHz (865.0–867.0 MHz, per WPC/TTN IN865-867 plan). Specify IN865–867
     and the matching antenna/duty-cycle. 433 MHz hardware here is non-compliant. -->
865–867 MHz (India IN865–867 LoRaWAN plan)
```

**WHY:** closes Bug #6 — deploying 433 MHz LoRa in India is a regulatory non-starter and breaks the
flagship Uttarakhand/Himachal use case. IN865–867 is the correct, licence-exempt plan. (Verified live
against the TTN frequency-plan documentation this session.)

---

## PATCH F — Bug #13 (MAJOR/UQ): soften the conformal "guarantee" to measured, risk-controlled coverage

**Location:** §7.7 conformal subsection (≈ lines 547–549).

**BEFORE (anchor, line ~547):**
```
conformal prediction guarantees 90% coverage
```
(exact wording to be matched in the shipped text)

**AFTER:**
```
<!-- FIX #13/#24: Split-conformal's marginal guarantee is EXCHANGEABILITY-dependent and degrades under
     missing sensors, feedback shift, and temporal dependence (all present here). The on-region
     competitor 2603.15681 itself measured coverage falling to 82.9% overall and 45–59% in high-risk
     zones. Claim MEASURED coverage with CIs, use online adaptive CP (ACI/AgACI), and frame it as
     conformal RISK-CONTROL (bounded miss-rate), not a fixed 90% coverage guarantee. -->
online adaptive conformal prediction (ACI/AgACI) targeting a bounded per-zone miss-rate; we report measured marginal AND per-zone coverage with confidence intervals rather than asserting a fixed 90% guarantee
```

**WHY:** closes Bug #13 (overclaim) and operationalises Bug #24. The guarantee is invalid under
TRINETRA's missingness + feedback + autocorrelation; adaptive CP restores honest long-run coverage.

---

## PATCH G — Bug #5 (MAJOR/INTEGRITY): correct the 2603.15681 mislabel and the novelty contradiction

**Location:** citation of 2603.15681 (≈ line 548/781) + the novelty claim (≈ line 2842).

**BEFORE (citation anchor):**
```
2603.15681 ... landslide ... mapping
```
**AFTER:**
```
<!-- FIX #5: 2603.15681 is a FLASH-FLOOD susceptibility paper for Himachal Pradesh (GraphSAGE over
     ~460 sub-watersheds, AUC 0.978) with conformal UQ whose empirical coverage fell to 82.9%
     overall and 45–59% in high-risk zones — NOT a landslide-mapping paper, and it DOES exist. -->
2603.15681 (flash-flood susceptibility mapping in Himachal Pradesh; GraphSAGE over ~460 sub-watersheds, AUC 0.978; conformal UQ with empirical coverage 82.9% overall and 45–59% in high-risk zones)
```

**BEFORE (novelty anchor, ~line 2842):**
```
our searches returned no landslide papers → NOVEL
```
**AFTER:**
```
<!-- FIX #5: remove the self-contradiction (the report both cites 2603.15681 as a failing competitor
     AND claims no such paper exists). State novelty honestly against the real prior art. -->
The closest prior art, 2603.15681, already applies conformal UQ to Himalayan hazard susceptibility; TRINETRA's novelty is therefore the *forecasting / pre-event* regime and the gated physics-shielded meta-fusion decision head, NOT the use of conformal UQ per se.
```

**WHY:** closes Bug #5 — a real paper was mislabelled, used as a strawman, and simultaneously denied to
exist. Confirmed from the full text in `papers/multimodal/2603.15681.txt`.

---

## PATCH H — Bug #0 (CRITICAL/PROCESS): mark the QA-workflow status honestly

**Location:** `EXTRACT-3-bugfix-status.md` header (`run wf_a939fae0-f72`) and any report text that claims
"all defects were fixed."

**BEFORE:**
```
status: completed
```
**AFTER:**
```
<!-- FIX #0: this run aborted on a 402 billing error with 2/12 fixes drafted, 0/4 verifications,
     synthesis failed, and 15/17 agents never ran (tokens:0). It is NOT completed. -->
status: failed (billing-aborted: 2/12 fixes drafted, 0/4 verified, synthesis failed)
```

**WHY:** closes Bug #0 — a billing-aborted run was logged `completed`, so the team's own known-defect
list was never actually fixed. Any downstream claim of "all defects fixed" must be withdrawn until the
workflow is re-run with credits under the fail-closed status invariant (FIX #0 in the robustification
spec).

---

## PATCH I — standing evaluation gate (Bugs #11, #18, #19, #27, #31): spatial-CV + baselines

**Location:** the evaluation / results section (wherever headline AUC / skill / lead-time numbers appear).

**INSERT (as a required methods note above the results):**
```
<!-- FIX #11/#18/#19/#27/#31: Admission gate for every headline number.
     (1) Report each metric under BOTH random-CV and tile-withheld (whole-map-tile) SPATIAL
         cross-validation; key all claims to the spatial-CV column.
     (2) Include a gradient-boosted / decision-tree baseline; a deep model that does not beat it
         is reported as "does not beat GB baseline" (cf. 2608.12422: AUC 0.9 → 0.54 under spatial CV,
         DL does not beat GB; 2510.10799; 2106.08909).
     (3) Forecasting head: report skill vs PERSISTENCE and seasonal-naive on change windows (2509.18176).
     (4) RL alarm policy: report off-policy value (BVFT selection + SCOPE-RL risk/CVaR), not simulator return.
     (5) Report metrics PER HAZARD (landslide/flash-flood/cloudburst/GLOF) with CIs; no single aggregate AUC. -->
```

**WHY:** operationalises the dominant finding cluster — the evaluation is not yet valid. This note makes
every performance claim falsifiable and withdraws any that fail the gate.

---

## Patch coverage summary

| Patch | Closes bug(s) | Severity | Type |
|---|---|---|---|
| A | #1 | CRITICAL | threshold reconciliation |
| B | #3, #17 | MAJOR | physics (Iverson cosine) |
| C | #2 | MAJOR | physics (suction sign) |
| D | #4 | MAJOR | physics (α / inverse-velocity) |
| E | #6 | MAJOR | hardware (LoRa band) |
| F | #13, #24 | MAJOR | UQ (conformal) |
| G | #5 | MAJOR | integrity (mislabel/contradiction) |
| H | #0 | CRITICAL | process (QA status) |
| I | #11, #18, #19, #27, #31 | CRITICAL (validity) | evaluation gate |

Remaining findings (#7 geophone/EO-leak, #8 storm brownout, #9 reward inversion, #10 datacube size,
#12 proxy endpoint, #14 edge latency, #15 I–D constants, #16 novelty-gate, #20–#23, #25–#26, #28–#30,
#32) are **design/architecture** changes rather than single-line text edits; their concrete fixes +
acceptance tests live in `TRINETRA_Bug_Robustification.md` (FIX #0–#15 + Appendix E) and
`TRINETRA_MetaFusion_Design.md`. This patch set covers every defect that is fixable by a direct,
verbatim edit to the report prose/equations.
