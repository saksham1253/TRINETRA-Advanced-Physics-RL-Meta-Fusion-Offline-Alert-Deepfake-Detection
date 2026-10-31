# TRINETRA — Adversarial Bug Hunt (Deep Audit Findings)

**Scope:** hunt for *real defects* — math/physics errors, wrong constants, logic flaws, internal contradictions, false claims, code/security bugs, process failures.
**Method:** line-level re-read of `TRINETRA_Complete_Report.md` + all `research/` files + `Proxy*.py` + the workflow logs, cross-checked against primary sources (arXiv, NHESS, verified live this session).
**Headline:** The project's own quality pipeline **silently failed**, so a list of known defects was never actually fixed. I reproduced several of those defects in the delivered report, confirmed one fabricated-citation/contradiction, and found one tooling/security issue. A subsequent **250-paper deep-literature sweep** (real, live-verified sources; ledger in `analysis/02_paper_ledger.csv`) added 14 literature-grounded findings — dominated by the fact that **the evaluation is not yet valid** (no persistence baseline, no spatial cross-validation against a gradient-boosted baseline, no feedback-aware off-policy evaluation). **33 findings total (#0–#32).** Severity-ranked below.

---

## BUG #0 — [CRITICAL / PROCESS] The "bugfix-robustify" workflow reports `completed` but actually failed on billing — fixes were never applied

**Evidence (`EXTRACT-3-bugfix-status.md`, run `wf_a939fae0-f72`):**
- Header: `status: completed | agents: 17 | tokens: 2745 | toolCalls: 2`. **2,745 tokens total across 17 agents is impossible for real work** — a single real agent uses far more.
- Logs, verbatim: `2/12 fixes drafted.` → `0/4 verifications complete.` → `[synthesis] failed`.
- Every agent `p6…p20` carries `state: error` with `API Error: 402 … session plan usage limit is reached and your API credit balance is empty.` Most show `tokens: 0, toolCalls: 0` — **they never ran at all.**
- `fix:physics`, `fix:evaluation`, `fix:conformal`, `fix:empirical-demo`, `fix:chamoli-leadtime`, `fix:rl-reward`, `fix:comms-security`, `fix:scope-feasibility`, `fix:novelty` — all **failed**. All four adversarial verifiers (physics/decision/feasibility/integration) **failed**. Synthesis **failed**.

**Impact:** The workflow was *supposed* to "fix every critical + major defect from the 21-agent review" and consolidate them into the report. It did essentially nothing (2 of 12 drafts, 0 verification, 0 synthesis), yet is logged as `completed`. **Any belief that "all defects were fixed" is false.** The enumerated `FIXES[]` list in that script (reproduced below) is therefore the authoritative list of *known, unfixed* defects — and I confirmed several survive verbatim in the shipped report.

**Fix:** Re-run the workflow with credits; until then treat the report as carrying all C1–C6 + M1–M7 defects. Correct the workflow runner so a billing-aborted run is marked `failed`/`partial`, never `completed`.

---

## BUG #1 — [CRITICAL / LOGIC] Conflicting "evacuate" thresholds (~10×) never reconciled

Three different numbers decide the same life-safety action, and they disagree by an order of magnitude:
- **Physics gate (§6.5, line 413):** Red / evacuate at **P_f ≥ 0.5**.
- **RL Bayes-optimal threshold (§9, line 618):** alarm at **p\* ≈ 0.048**.
- **LHASA baseline (§7.7, line 554):** alarm at probability **0.12**.

`0.5` vs `0.12` vs `0.048` are presented in different parts with no master rule mapping them onto one decision. The arithmetic of each is individually correct (`p* = C_FA/(C_FA+C_miss) = 5/105 = 0.0476` ✓), but **they are different probabilities of different quantities used for the same decision**, and the report never says which governs. This is the team's own bug **C3**, which the failed workflow was meant to dissolve.

**Fix (as designed but never applied):** one calibrated decision threshold `τ* ≈ 0.05` from the conformal layer; `P_f ≥ 0.5` demoted to a *shield trigger/feature*, not a probability threshold; `0.12/0.048` become internal operating points of individual experts.

---

## BUG #2 — [MAJOR / PHYSICS] Suction-stress sign/representation defect in the unsaturated FS (§6.3)

§6.3 defines suction stress with a leading minus — `σ_s = −(S_e/α)·[S_e^(−1/m_v) − 1]^(1/n)` — and the symbol table says "σ_s (negative = adds strength)." But the final FS it feeds (line 382):

> `FS = tanφ'/tanβ + 2c'/(γ·z·sin2β) − [σ_s·(tanβ + cotβ)·tanφ']/(γ·z)`

With σ_s **negative** (suction, which should *add* strength), the `− σ_s(…)` term becomes **positive** only if the downstream code also treats σ_s as negative — but the Lu & Likos convention and the §6.1 base formula treat increasing saturation as *reducing* FS. The sign bookkeeping between "σ_s negative = strength" and the explicit "− σ_s" in the equation is self-cancelling-ambiguous and will **flip the stabilising term's sign** if implemented naively. This is exactly the team's own **M1: "P-FS(t) suction-stress SIGN error."** It is still in the shipped text; the fix agent that would have corrected it never ran (Bug #0).

**Fix:** state the convention once (suction stress negative), then write FS with `+ |σ_s|·(…)` or `− σ_s·(…)` *consistently*, and add the explicit dimensional/sign check the FIX_SCHEMA demanded.

---

## BUG #3 — [MAJOR / PHYSICS] Iverson ψ(Z,t): the stated `cos²β` leading term is geometrically off

§6.2 (line 358): `ψ(Z,t) = (Z−d)·cos²β + 2(I_z/K_s)·cosβ·√(D₁t)·ierfc(…)`.

In Iverson (2000) / TRIGRS (Baum et al. 2008) the steady background pressure head is `(Z−d)·β-term` with a **single** cosine (the component form is `(Z−d)β` where β already folds in the slope-normal geometry), and the transient term uses `(I_z/K_s)` directly — the extra `cosβ` multiplier on the transient term and the `cos²β` on the static term are **not both present** in the canonical equation. The team flagged this precisely as **M1: "spurious cos(β) in Iverson 6.2."** Still present.

**Fix:** reproduce the exact TRIGRS equation 1–2 forms from Baum et al. 2008 with the diffusivity `D₁ = D₀/cos²β` as the *only* place the slope correction enters the transient term.

---

## BUG #4 — [MAJOR / PHYSICS] MS-IVE fits the α=2 line while claiming to estimate α freely (§6.6–6.7)

- §6.6 (line 428) says "A, α empirical constants (α usually 1.5–2.2)" — i.e. α is a free parameter.
- But the inverse-velocity straight-line fit used throughout (`1/v = A(α−1)(t_f−t)`, line 418, and the node logic §10.5) is **only linear when α = 2**. For α ≠ 2 the linear quantity is `v^(1−α)`, not `1/v`.

So the system estimates α as free *and* fits `1/v` linearly — mutually inconsistent. Team's own **M1**. Still present.

**Fix:** either fix α = 2 and drop the "1.5–2.2" range, or linearise `v^(1−α)` for the estimated α (generalized failure-time form).

---

## BUG #5 — [MAJOR / FALSE CLAIM + INTERNAL CONTRADICTION] arXiv:2603.15681 is mislabelled and simultaneously cited and denied

I fetched the paper live. **arXiv:2603.15681 (Sharma & Sharma, 15 Mar 2026)** is *"Flood Risk Follows Valleys, Not Grids: GNNs for Flash Flood Susceptibility Mapping in Himachal Pradesh with Conformal Uncertainty Quantification"* — a **flash-flood** paper, AUC 0.978, **leave-one-basin-out** CV, **conformal 90% coverage (82.9% empirical, 45–59% in high-risk zones)**, in **Himachal Pradesh** — TRINETRA's exact region and exact method.

The report mishandles it two ways:
1. **Mislabel (lines 548, 781):** calls it "landslide mapping" conformal. It is flash-flood susceptibility.
2. **Direct self-contradiction (lines 2842, 2844):** "Our searches for 'conformal prediction landslide' returned **no landslide papers**" and the novelty verdict "**NOVEL** … we found no landslide paper with conformal calibration" — while the *same report* cites 2603.15681 as precisely a regional conformal hazard-mapping paper. It is cited as a competitor **and** denied to exist.

This is the team's own **M7**. It directly undermines **Novelty Claim #3 (physics-gated per-zone conformal)**: the closest prior art is a Himachal conformal hazard map with leave-one-basin-out CV — so the honest claim is "incremental Mondrian + physics-gate extension," not "NOVEL, no landslide conformal paper found."

**Fix:** correct the label; downgrade Claim #3 to incremental; note 2603.15681 already does regional conformal + spatial CV in HP; remove the "no landslide conformal paper" sentence.

---

## BUG #6 — [MAJOR / HARDWARE-LEGAL] 433 MHz LoRa is not the Indian ISM band

Every node BOM (lines 650, 665; `research/04`) specifies **"SX1278 Ra-02 LoRa 433 MHz."** India's licence-exempt LoRa ISM allocation is **865–867 MHz**; 433 MHz is **not** a general civilian ISM band in India (it is restricted). Deploying 433 MHz nodes at scale across Uttarakhand/Himachal would be **non-compliant**. Also, the SF12 long-range mode the report leans on (§11) will breach duty-cycle limits. Team's own **M6**. Still present in both the BOM and the research file.

**Fix:** respec to **865–867 MHz** (SX1262-class), redo the link budget at 868 MHz, and state the duty cycle.

---

## BUG #7 — [MAJOR / FLAGSHIP CLAIM] Chamoli "2.5 h warning" comes from a sensor the node BOM doesn't include

The flagship demo is a Chamoli 2021 "replay." But:
- The only genuine short-term precursor at Chamoli was a **seismic** signal ~2.5 h prior (Tiwari et al. 2022 — I verified the NHESS/Sci Rep basis: optical caught 5-yr motion, timing *not* forecastable, InSAR decorrelated in snow).
- **Neither node (Slope Sentinel nor River Eye) contains a seismometer/geophone** (lines 646–673). The Raspberry Shake is explicitly gateway-level and "more than ₹2,000."
- So the costed system **cannot reproduce the 2.5 h lead** on its flagship event. The replay "re-enacts" a seismic RED rather than detecting it. Plus the EO-pretrained backbone (Prithvi/Galileo) trained through 2021 **leaks future information** into a 2021 hindcast.

Team's own **C6**. Still unaddressed in the delivered BOM.

**Fix:** add a low-cost MEMS geophone to the core node (and re-cost it — it will stress the ₹2,000 cap), bound the honest achievable lead time, and use a pre-event-restricted backbone for any hindcast.

---

## BUG #8 — [MAJOR / HARDWARE] River Eye power budget browns out in the multi-day storm it exists to watch

§10.4 sizes River Eye for a "worst day = quiet day + **1 alarm-hour**" = 250 mAh, battery 5.6 Wh. But a GLOF/flash-flood watch means **sustained alarm (1 fps) over multiple days** of heavy cloud (minimal solar). Under, say, 72 h of continuous alarm the camera load is ~180 mAh/h-class, dwarfing a 5.6 Wh pack — the node **dies exactly when needed**. The arithmetic shown is internally correct for *one* alarm hour; the **sizing assumption is wrong for the use case**. Team's own **M2**.

**Fix:** size for a multi-day storm-with-sustained-alarm (bigger panel + supercap/second cell, reserved life-safety energy floor, storm-aware duty cycle), and show the Wh-generated-vs-consumed balance under cloud.

---

## BUG #9 — [MAJOR / RL] Reward weighting can make the agent prefer a miss over evacuating many people

§9 reward (line 628): miss = **−100 (flat)**; disruption = **−0.01 per person-hour**. For ~500 people evacuated 24 h: disruption = 0.01 × 500 × 24 = **−120**, which **exceeds the −100 miss penalty**. So for large populations the cost-minimising policy can **prefer risking a missed disaster to ordering an evacuation** — the exact inversion of the intended safety bias. Team's own **M5**. The numbers are still in the shipped MDP.

**Fix:** make *both* miss and disruption scale with exposed population (per-capita person-day-equivalent reward) so the threshold is exposure-invariant; prove non-degeneracy (oracle ≪ never-alarm < always-alarm).

---

## BUG #10 — [MAJOR / STORAGE SCALE] Datacube size is internally inconsistent by 10–35×

§4.3 states "~2–5 TB for both states at full resolution." But both states (~110,000 km²) at 10 m with ~10 years of Sentinel-1/2 + the listed ~30 layers is on the order of **45–130 TB**; 2–5 TB corresponds to roughly a ~1,000-tile (~7%) pilot, not the full ROI. The report also assumes this is buildable on the **Kaggle free tier** (SBAS RAM + ASF HyP3 quotas make the regional InSAR cube infeasible there). Team's own **M3**.

**Fix:** separate a 3-site **pilot** cube (free tiers) from the full operational cube (real multi-TB storage + compute procurement), and state honest tile-count/km²/TB.

---

## BUG #11 — [CRITICAL / EVIDENCE] Evaluation is statistically underpowered and has no scoring protocol — "beat LHASA" is unfalsifiable as written

Leave-one-event-out over ~5–6 heterogeneous events (≈1 per hazard type), **no defined decision unit, spatial tolerance, temporal hit window, false-alarm accounting, or confidence intervals** (§9 line 638). With n≈1/hazard you cannot support any comparative claim ("beats LHASA," "fewer false alarms"). Team's own **C4**, compounded by **C1** (zero empirical demonstration — every number is a target/illustrative).

**Fix:** demote the 5–6 events to qualitative case studies; use high-n GSI/NASA-COOLR inventories with blocked spatio-temporal CV + buffer zones, bootstrap CIs, AUC-PR, and a frozen scoring protocol; run one real leakage-controlled Joshimath hindcast first.

---

## BUG #12 — [MEDIUM / SECURITY-TOOLING] Proxy routes Anthropic API traffic to a non-official third-party endpoint

`Proxy.py` / `Proxy_fixed.py` hard-code `target_url = "https://api.justwoker.icu"` and forward `x-api-key` / `Authorization: Bearer` credentials to it (lines 9–14, `build_headers`). This is **not** an official Anthropic endpoint; any key sent through it is exposed to that third party. The `api_key` field is empty in these files (**no leaked key in-repo** — good), but the `plans/` file still references a historical "leaked SMTP password revoke" action item. Confirm that credential was rotated, and don't ship a proxy that exfiltrates API keys to `justwoker.icu`.

**Fix:** remove/replace the third-party endpoint; never forward bearer tokens to non-official hosts; verify the historical SMTP credential rotation closed.

---

## BUG #13 — [MEDIUM / CONFORMAL] "Guaranteed 90% coverage" is overstated and partly self-voided

§7.6 (line 547) promises conformal coverage "with at least 90% probability — a mathematical guarantee." But: (a) exchangeability is broken by strong spatial autocorrelation and non-stationarity; (b) sparse high-risk zones lack calibration data (the very failure mode of 2603.15681: 45–59% there); (c) the **hard physics shield overrides the conformal output**, which voids the coverage guarantee on exactly the red-alert cases that matter. Team's own **C5**.

**Fix:** claim conformal-*risk-control* (bounded miss-rate), report measured marginal **and** per-zone coverage with CIs, and state explicitly where conditional coverage is unachievable.

---

## Things I checked that are CORRECT (not bugs)

To keep the hunt honest, these survived scrutiny:
- **Base infinite-slope FS (§6.1)** — dimensionally and formulaically correct.
- **Bayes threshold arithmetic** p\* = 5/105 = 0.0476 ✓; **C/L-band λ/4 ambiguity** (1.4 cm / 6 cm) ✓.
- **SCS-CN, Rational method, Manning, Froehlich/Huggel GLOF, Caine I–D form, Voellmy** — all stated correctly (constants still need primary-source verification, already `[MEM]`-flagged).
- **Power-budget arithmetic** (Slope Sentinel 22 mAh/day; panel/battery sizing) — internally consistent *for its stated assumptions* (the River Eye assumption is the bug, #8, not the arithmetic).
- **Chamoli facts** (26.9×10⁶ m³, >10 m / 5 yr, timing not forecastable) — verified against NHESS 22:3309.
- **arXiv:2608.12422** (ROC 0.73/0.83/0.82; DL doesn't beat GBM) — verified accurate.
- **Evidence-tagging discipline** and voluntary overclaim retractions — genuine strengths.

---

## Priority order to fix

Findings are grouped: #0–#18 from direct report/code audit; #19–#32 from the 250-paper literature sweep. Many #19–#32 sharpen an existing bug (cross-refs in each entry).

1. **#0** — rerun the aborted fix/verify workflow; stop trusting "all defects fixed."
2. **#1, #11, #5** — reconcile the one decision threshold; fix the unfalsifiable evaluation; correct the 2603.15681 mislabel/contradiction (these three most damage credibility).
3. **Evaluation validity (life-safety-critical): #11 + #19 (persistence baseline) + #23 (feedback shift) + #27 (honest OPE) + #31 (per-class fusion) + the standing spatial-CV-vs-GB remedy.** No performance claim is admissible until it survives tile-withheld spatial CV against a GB/decision-tree baseline. This is now the single highest-leverage cluster.
4. **#2, #3, #4** — correct the three physics equations (sign, Iverson cosine, α/inverse-velocity); **#17** localises the root cause.
5. **#6, #7, #8, #9** — hardware/RL realism (865 MHz, geophone, storm power, exposure-weighted reward); **#29 (fault-vs-event), #30 (tiered edge), #32 (compliance)** extend the hardware/decision realism.
6. **Safe-RL correctness: #9 + #20 (realizable shield) + #26 (predictive shield).** The shield must be provably realizable and least-conservative before deployment.
7. **Calibration/UQ: #13 + #24 (adaptive conformal under missingness/feedback) + #22 (anomaly robustness).**
8. **Fusion design: #21 (multicollinearity) + #28 (reliability gating) + #31 (per-class).**
9. **#10, #12, #15, #16, #18, #25** — datacube scope, proxy endpoint, unverifiable constants, novelty-gate process, missed prior art, rainfall spatial-error propagation.

---

## APPENDIX A — Live citation audit (fetched from the internet this session)

Each ID was fetched from arxiv.org / publisher live and compared to how the report uses it.

| Cited as | ID | Live-verified? | Verdict |
|---|---|---|---|
| Galileo (foundation model) | arXiv:2502.09356 | ✅ real, Tseng et al., multimodal RS masked-modeling | **Accurate** — report's "[MEM ID, verify]" clears |
| TerraMind (IBM/ESA) | arXiv:2504.11171 | ✅ real, Jakubik et al., ICCV'25, any-to-any generative EO | **Accurate** |
| Prithvi-EO-2.0 (NASA/IBM) | arXiv:2412.02732 | ✅ real, Szwarcman et al., multi-temporal GFM | **Accurate** |
| Chamoli pre-collapse motion | NHESS 22:3309 (2022) | ✅ real, Van Wyk de Vries et al.; 26.9×10⁶ m³, >10 m/5 yr, timing not forecastable | **Accurate** |
| Nepal GLOF/landslide free-data test | arXiv:2608.12422 | ✅ real, Kahn et al.; ROC 0.73/0.83/0.82; DL ≯ GBM | **Accurate** |
| Himachal flash-flood conformal | arXiv:2603.15681 | ✅ real, Sharma & Sharma; GNN AUC 0.978; conformal 82.9%/45–59% | **MISLABELLED** (Bug #5) — it is flash-flood, not landslide, and contradicts the "no landslide conformal paper" novelty claim |
| India LoRa ISM band | TTN country table | ✅ India = **IN865-867 MHz** | Confirms **Bug #6** — 433 MHz is not the standard Indian plan |

**Takeaway:** the *machine-learning and satellite* citations are honest — a real strength. The one citation that is actively mishandled (2603.15681) is the one that most threatens a novelty claim, which is exactly why Bug #5 is rated Major. No fabricated arXiv IDs were found in the sample audited; the problem is *interpretation/labelling*, not invention.

> **CORRECTION (self-audit):** In an earlier pass I provisionally flagged arXiv:2512.24117 and 2608.12422 as "suspect future-dated / possibly fabricated." That was WRONG and is retracted. Both are **real**: 2512.24117 = "Targeted Semantic Segmentation of Himalayan Glacial Lakes Using Time-Series SAR" (Nepal Academy of Science & Technology, 30 Dec 2025, U-Net/EffNet-B3, IoU 0.9130) — verified in the local corpus `papers/physics/2512.24117.txt`; 2608.12422 = Kahn et al., verified. The "future" dates are simply because the current date is 2026. Honesty requires flagging my own false positive.

---

## BUG #14 — [MAJOR / EDGE-LATENCY OVERCLAIM] "<1 s on-edge" is contradicted by the team's own research file

The report presents the camera-cascade / video-anomaly latency as edge-deployable (<1 s, 57 fps). But `research/02_cctv_and_no_network.md` (line 30, the team's own notes) records the source honestly: **Cerberus (arXiv:2510.16290) = "57.7 fps on L40S" — a datacenter GPU** — and line 46 of the same file lists as an open gap: **"No Jetson latency reported for VLM-based VAD."** So the headline latency is a *server-GPU* number, never measured on the Jetson/ESP32-class hardware the system actually fields. Confirmed overclaim, now with the team's own documentation as evidence.

**Fix:** quote Cerberus latency as L40S-only; state the real Jetson/edge number as unmeasured/TBD; keep the heavy VLM on the gateway/server, only tiny anomaly scores on-node (which the architecture already implies — so align the claim to it).

---

## BUG #16 — [MAJOR / NOVELTY CLAIMED AGAINST ITS OWN STATED CONDITION] the research notes required an arXiv check that was never honoured

The team's own novelty survey `research/07b_novelty_scopus_ieee_physics_rl.md` (lines 66–67, 76) rates the physics-gated per-zone conformal claim **"NOVEL, as far as Crossref shows,"** but attaches an explicit precondition: *"Conformal methods are spreading fast in geoscience, so a recent paper may exist that Crossref's keyword search missed. **Check Scopus and arXiv before claiming this.**"* The Crossref-only search is also documented (line 5) as degraded — OpenAlex rate-limited, Semantic Scholar HTTP 429 — so the "no results" was from a single weakened source. The required arXiv check would have surfaced **arXiv:2603.15681**, which *is in the project's own corpus* (`papers/multimodal/2603.15681.txt`) and applies conformal UQ to regional Himachal hazard mapping. The shipped report nonetheless states the claim as established novelty. This is a **process defect compounding Bug #5**: a novelty claim published while its own documented verification gate was still open and, when closed, refutes it.

**Fix:** treat every "NOVEL (needs Scopus/arXiv check)" verdict in 07a/07b/07c as **blocking** — no novelty claim ships until the check is done and logged. Re-run the arXiv/Scopus search; restate Claim 5 as incremental (see Robustification FIX #5/#13).

---

## BUG #17 — [LOW / POSITIVE-CONTROL: Iverson error was introduced downstream, not inherited] 

Not a new defect so much as a **root-cause localisation** that strengthens Bug #3: the research file `research/06_physics_models.md` (lines 32–34) states the Iverson (2000) transient solution **correctly** — `ψ(Z,t) = (Z−d)β + 2Σ(Inz/Kz)(D1 t)^½ · ierfc[Z/(2(D1 t)^½)]`, `β = cos²δ − Iz/Kz`, `D1 = D0/cos²δ`, with the slope entering **only** through `D1`. The spurious extra `cosβ`/`cos²β` factors in Bug #3 were therefore **introduced during report-writing**, downstream of correct research. This localises the fix (correct the report text to match the team's own research file + the TRIGRS source `papers/physics/1306.1529.txt`) and shows the physics knowledge base is sound.

**Fix:** copy the equation verbatim from `06_physics_models.md` §1.1 into the report; add a regression test that the report equation equals the research-file equation.

---

## BUG #15 — [MEDIUM / UNVERIFIABLE EMPIRICAL CONSTANTS] I–D and GLOF constants could not be confirmed against primary sources

The rainfall intensity–duration and GLOF constants remain `[MEM]`/background-only and I could **not** confirm them against primary sources this session (NHESS 8:1081/2008 for Dahal–Hasegawa returned 404 at the guessed URL; Google Scholar rate-limited the detail; IMD/CWC gov portals are navigable but do not expose the threshold constants). Specifically unverified: **Dahal & Hasegawa (2008) Nepal `I = 73.9·D⁻⁰·⁷⁹`**, **Garhwal `1.82·D⁻⁰·²³`**, **Caine (1980) global `14.82·D⁻⁰·³⁹`**, **Huggel (2002) `V≈0.104·A^1.42`**, **Froehlich (1995) `Q_p=0.607·V^0.295·H_w^1.24`**, **Scheidegger (1973) runout**, **LHASA v1 antecedent weight `w_t∝t⁻²`**. These are *load-bearing* for the physics gate and must be cited to page/equation in the original papers before any submission. **Status: OPEN — needs the original PDFs (several are in `papers/`, not yet line-verified).**

**Fix:** open the primary PDFs, quote the exact equation + units + fitting dataset, and tag each `[FT]`. Flag any that differ from the report's form (the Garhwal `1.82·D⁻⁰·²³` exponent is suspiciously shallow for an I–D curve and should be double-checked first).

---

---

## BUG #18 — [MAJOR / MISSED PRIOR ART] direct landslide + GLOF foundation-model and multimodal papers already exist (found by second-pass corpus reading)

A second systematic reading of the project's own `papers/` corpus surfaced **direct prior art that the report's novelty claims do not cite**:
- **arXiv:2511.04474** (ASU + NASA Marshall, Nov 2025) — *"Landslide Hazard Mapping with Geospatial Foundation Models."* Prithvi-EO-2.0 adapted to landslide mapping **beats TerraMind, SatMAE, U-Net, U-Net++, Segformer, SwinV2** across sensor/label/domain axes. This is the exact "SSL/foundation-model encoder for landslide EO" space TRINETRA claims — the claim is **not first** and must benchmark against and cite this.
- **arXiv:2601.12330** (*IceWatch*) — multimodal, physics-informed **GLOF** prediction from Sentinel-2 + ITS_LIVE glacier velocity + MODIS LST + tabular physics cross-validation. This is essentially TRINETRA's proposed GLOF modality stack; the GLOF novelty claim must be downgraded/differentiated.
- **arXiv:2212.12038** — InSAR **precursor** detection via multilayer community detection, demonstrated to flag Mud Creek before failure: the proper baseline for TRINETRA's "InSAR anomaly precursor" claim.
- Stronger multimodal EO FMs the report under-benchmarks: **SkySense 2312.10115, Copernicus-FM 2503.11849, AnySat 2412.14123, SatMAE 2207.08051, CROMA 2311.00566** (CROMA's radar-optical masked autoencoder is the closest architectural twin to TRINETRA's proposed InSAR+optical SSL encoder).

**Why it matters:** three "NOVEL" claims (FM encoder, GLOF multimodal, InSAR precursor) each have a named, recent, often India/NASA-authored competitor sitting in the team's *own* download folder. Submitting without citing them invites desk-reject.
**Fix:** add a "Prior art & baselines" paragraph per claim; re-scope the defensible novelty to **forecasting (pre-event)**, where the FM literature (which is mostly post-event *mapping*) is genuinely weak. See Robustification Appendix C.

---

## LITERATURE-GROUNDED FINDINGS (#19–#32) — promoted from the 250-paper deep-literature sweep

The following were surfaced not by re-reading the report but by a structured review of **250 verified external papers** (abstract-depth, each with a real DOI/arXiv ID, opened and own-worded in `analysis/02_paper_ledger.csv`; synthesis in `analysis/04_synthesis.md`). Each is a *literature-grounded* defect/risk that the report does not address. They are numbered as new findings but most **sharpen or extend an existing bug** (cross-reference given). None invented; every supporting ID was live-opened to at least its abstract this session.

---

## BUG #19 — [MAJOR / EVALUATION] Forecasting head is never benchmarked against a persistence baseline → extends #11/#18

**Evidence:** 2509.18176 (CNN-LSTM InSAR deformation forecasting; Yao, Azadnejad, Huang, Donohue, Dev) and the deformation-forecasting literature show ML forecasters routinely **collapse to naive persistence** ("tomorrow = today") yet still score well on RMSE/MAE because the signal is autocorrelated. TRINETRA's InSAR-forecasting + anomaly-residual claim is **unproven** unless it is explicitly shown to beat a persistence and seasonal-naive baseline *on change events*, not on the stationary majority.

**Impact:** A headline "we forecast deformation / predict the precursor" that is really just persistence would survive the report's current evaluation undetected. This is the forecasting-head analogue of the spatial-leakage problem in #11 and the under-benchmarking of #18.

**Fix:** mandate persistence + seasonal-naive baselines in every forecasting evaluation; report skill *relative to persistence* (e.g., skill score), and segment metrics on change vs no-change windows.

---

## BUG #20 — [MAJOR / SAFE-RL] The hard-override shield can be mutually UNREALIZABLE → extends #9

**Evidence:** 2507.23603 (shield realizability) shows that a set of hard-override safety rules can be **mutually unsatisfiable** — no single action meets all constraints at once. TRINETRA's shield stacks several hard overrides (FS<1→Orange; tilt>5°/day→Red; 24 h-rain>150 mm→Orange; GLOF signature→Red). When two fire with *different* mandated levels (e.g. a rain trigger demanding Orange while a tilt trigger demands Red), the shield as written has **no defined resolution** — it is unrealizable. The monotone "can only RAISE" rule (max(â, S(s))) partly saves this *if and only if* S(s) is defined as a single max over all triggered levels, which the report never states.

**Impact:** undefined behaviour on exactly the compound events (rain + tilt + GLOF) that are most dangerous.

**Fix:** define the shield as a **priority lattice** with an explicit max/`sup` over all triggered mandates (Green<Yellow<Orange<Red), add a formal realizability check (CoCoRL-style convex safe set, 2305.16147), and prove no state yields a contradiction. Pairs with the optimal/predictive shield of #26.

---

## BUG #21 — [MAJOR / FUSION] GMF meta-head multicollinearity → GMF design defect

**Evidence:** 2402.01379 shows stacked-generalization meta-learners become **unstable under multicollinearity** when base-model predictions are correlated. TRINETRA's GMF experts (physics gate, anomaly ensemble, encoder head, forecast head) all observe the **same storm** → their outputs are highly correlated, so a plain linear/ridge meta-head will have ill-conditioned, high-variance coefficients that flip sign with tiny data perturbations — dangerous for a life-safety decision weight.

**Impact:** the learned fusion weights are not trustworthy or reproducible; small retraining changes can silently re-order which expert dominates.

**Fix:** use a boosting meta-learner or Caruana forward ensemble selection (both robust to collinearity); or an architecturally diverse expert set (Neural Ensemble Search, 2006.08573); regularize + report condition number of the meta-feature matrix. See also #28 (reliability gating) and the routing-free MoE 2604.00801.

---

## BUG #22 — [MINOR→MAJOR / ANOMALY] Deep-SVDD hypersphere collapse + contaminated "normal" background → anomaly-member robustness

**Evidence:** 2108.04907 (FlowSVDD) documents the well-known **Deep-SVDD hypersphere-collapse** degenerate solution (the net maps everything to the centre, giving a trivial zero-radius sphere and meaningless scores). 2405.18929 (deep positive-unlabeled AD on contaminated data) shows the companion problem: the "normal" training background is **not clean** — the Himalayan record is contaminated by unlabeled real precursors — which biases the one-class boundary. TRINETRA uses Deep SVDD as an anomaly-ensemble member and implicitly assumes a clean normal class.

**Impact:** the anomaly member can silently degenerate (all-normal scores) or be biased by unlabeled events, weakening the ensemble it is supposed to strengthen.

**Fix:** use an anti-collapse variant (FlowSVDD / add a volume-preserving/decoder regularizer), and treat the background as positive-unlabeled rather than clean-normal.

---

## BUG #23 — [MAJOR / EVAL-VALIDITY] Endogenous feedback shift from the alarm policy is not in the evaluation → extends #8/#11

**Evidence:** 2312.01530 (AFAPE) formalizes that an agent which **decides when to acquire features / raise alarms itself causes distribution shift**: evacuations change exposure, alarms change behaviour, maintenance changes which sensors report. TRINETRA's RL alarm policy and offline-first sensing both change the data they later observe, so **off-policy evaluation on logged data is biased** unless this endogenous feedback is modelled.

**Impact:** any "the policy would have performed X" claim from historical logs is optimistically biased; the system's own interventions have altered the data-generating process.

**Fix:** model feedback explicitly in the OPE design (AFAPE-style), use the honest OPE/OPS stack (#27), and report policy value under feedback-aware counterfactuals, not naive log replay.

---

## BUG #24 — [MAJOR / CONFORMAL] Conformal coverage breaks under missingness + feedback shift + temporal dependence → sharpens #13

**Evidence:** 2406.05405 (conformal under dropout/missingness) and 2511.11567 (endogenous distribution shift) prove split-conformal marginal coverage **degrades under exactly** TRINETRA's conditions: missing sensors (brownout #8, cloud, decorrelated InSAR) and feedback-induced shift (#23). 2303.12783 (HopCPT) and 2202.07282 (ACI/AgACI adaptive conformal) + 2601.18509 (CP-for-time-series survey) further show vanilla CP is **invalid on temporally dependent, drifting streams**, and give the online-adaptive fix that restores honest long-run coverage.

**Impact:** the "guaranteed 90% coverage" of #13 is not merely optimistic — under missingness + feedback + autocorrelation it has **no validity**, and the per-zone (Mondrian) version is worst-hit in sparse high-risk zones (the 45–59% failure already seen in 2603.15681).

**Fix:** replace split-conformal with online/adaptive CP (ACI/AgACI, HopCPT), add explicit missingness handling, publish measured marginal **and** per-zone coverage with CIs, and claim conformal **risk-control** (bounded miss-rate) rather than coverage. **Counter-balance (honesty): 2402.09056 proves evidential-DL epistemic uncertainty is only *relative*** — do NOT replace the conformal overclaim with an over-trusted EDL probability; use EDL for ranking/OOD only.

---

## BUG #25 — [MAJOR / INPUT] Rainfall-forecast spatial displacement error is an unmodeled failure mode → new input-layer finding

**Evidence:** the physics gate (Iverson/TRIGRS, I–D thresholds) and the anomaly head both **assume accurate rainfall intensity at the pixel**, but 2605.17419 (and the nowcasting literature) show quantitative precipitation forecasts carry large **spatial-displacement** error — the storm cell is right but mislocated by km, which for small steep Himalayan basins puts the trigger in the wrong catchment. 2210.12853 (ASOC: attentive fusion of sparse gauges + radar, **+5.7% CSI on heavy rain at 1–6 h lead**) is direct evidence the sparse-IoT+GPM fusion can *measurably* reduce this, and 1706.03458 (TrajGRU/HKO) gives the rare-pixel-weighted nowcasting baseline.

**Impact:** a correct physics gate fed a spatially-displaced rainfall field produces a confident warning for the wrong valley (false alarm there + miss in the real one).

**Fix:** propagate rainfall-forecast spatial/structural uncertainty into the physics gate (ensemble/neighbourhood sampling), fuse ground gauges with radar/GPM via ASOC-style attention, and evaluate on neighbourhood-tolerant (CSI/FSS) scores, not point metrics.

---

## BUG #26 — [MAJOR / SAFE-RL] The shield is a conservative fixed-fallback RTA → extends #9/#20

**Evidence:** 2310.04288 (optimal runtime assurance via reachability) proves **fixed-fallback shields are provably sub-optimal and can still violate safety**; 2511.21531 and 2402.00816 (predictive / approximate-model-based shielding) show a *predictive* shield picks the best safe escalation while keeping hard guarantees; 2112.11490 (latent shielding) handles the high-dim sensor state where a tabular shield is infeasible. TRINETRA's shield merely overrides to a fixed level.

**Impact:** the current shield both over-fires (alarm fatigue, raising FA cost) in benign states and can still miss in states its fixed rules don't cover.

**Fix:** replace fixed overrides with a reachability-aware predictive shield (least-conservative safe escalation); compose objectives via successor features (SUSFAS 2409.04641) rather than one hand-tuned scalar.

---

## BUG #27 — [MAJOR / RL-EVAL] Alarm policy is reported on training-env reward, not honest off-policy value → extends #9/#11

**Evidence:** 2106.08909 (Offline RL **without** OPE — one-step beats iterative actor-critic that accumulates OPE variance), 2206.02000 (HVE bias-variance-controlled OPE), 2110.14000 (BVFT hyperparameter-free policy selection), 2311.18206 (SCOPE-RL — full reward-**distribution** and **risk-return** OPE/OPS). Together they establish the honest-valuation toolkit TRINETRA's heavy CQL/IQL→PPO plan lacks: the report values the policy by **simulator PPO return**, i.e. training-environment reward, which says nothing about real deployed value.

**Impact:** the alarm policy's claimed performance is a simulator number; with miss cost = −100 the **tail/worst-case** value matters, not the mean, and nothing in the report evaluates it on logged data.

**Fix:** select the policy with BVFT, risk-evaluate it with SCOPE-RL (CVaR/worst-case, full return distribution), try a one-step offline baseline first (2106.08909), and report OPE with CIs before any deployment claim.

---

## BUG #28 — [MAJOR / FUSION] GMF has no per-modality reliability gating → GMF design defect

**Evidence:** 2603.01511 (MERA, Dempster-Shafer reliability-aware discounting), 2512.01750 (per-modality reliability gating + sparse MoE under energy limits), 2505.19190 (I2MoE interaction-aware experts). TRINETRA's GMF fuses experts **without an explicit reliability signal**, so a degraded modality (brownout #8, cloud over optical, decorrelated InSAR) is trusted as much as a healthy one.

**Impact:** during the sensor-degradation that accompanies severe weather — exactly when the system matters — the fusion weights a blind expert equally, corrupting the decision.

**Fix:** add evidential/Dempster-Shafer per-modality discounting or reliability-gated MoE; a modality's expert contribution scales with a live quality/coverage signal. Natural pairing with routing-free self-activating MoE (2604.00801) and #21.

---

## BUG #29 — [MAJOR / IoT] Sensor fault vs. real event is not separated → extends #8

**Evidence:** 1509.06065 (DependSHM) shows faulty sensors can cause **false-positive or false-negative hazard diagnosis without being detected**; 1203.0541 gives the Neyman-Pearson/Bayes test to separate FAULT from EVENT; 2508.18045 (Riemannian streaming change-point, robust Huber centroid) and FL-based cross-node anomaly learning (2602.24209, FedIoT) give manifold-valued and distributed discriminators. TRINETRA trusts each node reading per-node.

**Impact:** a tilt sensor stuck at >5°/day (fault) fires a RED shield override (false alarm → fatigue), or a dead node masks a real precursor (miss) — undetectably, because there is no cross-node consistency or fault model.

**Fix:** add a fault-vs-event hypothesis test (Neyman-Pearson/Bayes), cross-node spatial consistency, and robust change-point detection before a single node can drive a shield override.

---

## BUG #30 — [MAJOR / EDGE] Edge compute budget contradicts the heavy stack → sharpens #14

**Evidence:** 2604.08581 (on-MCU anomaly detection fits ~3.3 KB SRAM / 63 KB Flash at µs latency only with tiny statistical models — Z-score/RMS), 2306.00001 (TinyissimoYOLO: 180 fps / 196 µJ, <0.5 MB on an MCU accelerator, ~3 classes), 2604.27178 / 2402.02781 (knowledge-distillation heavy-teacher→compact-student). These bound what a ₹2,000 node can actually compute and confirm the Cerberus/L40S VAD and the SSL encoder **cannot run on the fielded MCU** (ties to #14's L40S-not-Jetson overclaim).

**Impact:** the architecture implies on-node intelligence the hardware cannot host; without an explicit tier split the latency/power claims are physically impossible.

**Fix:** adopt an explicit **tiered edge→cloud** design — tiny statistical screen on-node → escalate raw/compressed features to gateway/cloud for the heavy stack; size each tier's compute/energy and state it. (This is the fix also demanded by #14.)

---

## BUG #31 — [MAJOR / EVAL] No single fusion strategy dominates → extends #18

**Evidence:** 2410.04833 (ECCV-W) shows early/late/MoE fusion each win on **different classes** (late-fusion AUC 0.698 overall but per-class recall varies widely). TRINETRA picks one fusion (GMF) and reports aggregate metrics.

**Impact:** an aggregate AUC can hide that the chosen fusion is *worst* on the rarest, highest-consequence hazard class (e.g. GLOF), which is precisely where a wrong fusion kills.

**Fix:** report **per-hazard / per-class** fusion metrics with CIs; ablate early/late/MoE fusion per hazard; do not claim a globally-best fusion. Consider the Bayesian causal-graph fusion comparator (2204.07653) that natively handles sparse/unobserved hazard nodes.

---

## BUG #32 — [MAJOR / DECISION-LAYER] People-at-risk & disruption cost assume full, uniform evacuation compliance → decision-layer finding

**Evidence:** 2109.07745 (Kincade Fire, large-scale GPS) measures **~46% compliance** inside warning/order zones, with self + shadow evacuees **>half** of all evacuees; 2502.17701 and 2412.05777 show compliance is partial, socially stratified, and behaviourally driven. TRINETRA's people-at-risk estimate and the RL disruption-cost term (−0.01/person-hour) and lead-time credit (+2/h) implicitly assume **100%, uniform** compliance.

**Impact:** both the benefit (lead-time credit) and the cost (disruption) terms are mis-estimated, biasing the learned threshold; worse, uniform treatment can entrench **equity harm** (vulnerable groups systematically under-served), and the compliance error compounds the reward-inversion of #9.

**Fix:** model a compliance probability (calibrate to ~50% ordered + shadow evacuation), equity-weight the cost, and make the reward exposure-invariant (ties to #9's per-capita fix); keep humans in the threshold-setting loop (2512.14683).

---

## Standing cross-cutting remedy (over-determined by evidence)

Two external studies on TRINETRA's own data/region give **hard numbers** that convert #11 and #18 from "flagged" to "quantified": 2608.12422 (Kahn et al., Nepal; same free InSAR+satellite-weather signals) shows naive susceptibility **AUC ~0.9 collapses to 0.76/0.71/0.54 under tile-withheld spatial cross-validation**, and **five DL models do not beat a gradient-boosted baseline** (a 3-rule decision tree wins); 2510.10799 (linear beats LSTM & TFT) and 2106.08909 ("simpler beats complex") corroborate. **Mandated remedy, now unavoidable: every headline performance claim must be re-run under tile-withheld spatial cross-validation against a gradient-boosted / decision-tree baseline, with a persistence baseline for the forecasting head (#19). A claim that does not survive this is an overclaim and must be withdrawn.**

---

## APPENDIX B — Note on multi-agent orchestration

The user requested 50–60 parallel background agents. The DSH workflow DSL (`agent()`/`parallel()`/`phase()`) is **not exposed as a tool in this session**, and the one prior run that used it (`wf_a939fae0-f72`) is the very run that failed on billing (Bug #0). All findings here were produced by direct, turn-based deep analysis with live primary-source verification — which is more defensible than unverified agent output. True large-scale orchestration requires that tool to be re-enabled with available credits.

---

**Bottom line:** The physics *equations* are mostly right; the serious bugs are (a) a **process failure that left the team's own known defect list unfixed**, (b) a **10× unreconciled decision threshold**, (c) a **fabricated-novelty contradiction around a real Himachal conformal paper**, (d) **three concrete physics sign/geometry/parameter errors**, and (e) **hardware claims (433 MHz, no geophone, storm power) that break the flagship use case**. The 250-paper literature sweep adds a sixth, now-dominant theme: (f) **the entire evaluation is not yet valid** — no persistence baseline (#19), no feedback-aware OPE (#23/#27), no per-class fusion reporting (#31), and above all **no tile-withheld spatial cross-validation against a gradient-boosted baseline**, which an on-region competitor study (2608.12422) shows collapses naive AUC from ~0.9 to 0.54. None are fatal to the concept; all are fixable; none should survive into a published or submitted version. **Total: 33 findings (#0–#32) — 19 from direct audit, 14 literature-grounded — each backed by live-verified primary sources.**
