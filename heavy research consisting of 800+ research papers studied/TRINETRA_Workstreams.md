# TRINETRA — Workstreams WS1–WS7 (engineering plan with budgets, gates, and honesty tags)

**Purpose.** Turn the 33 findings (`TRINETRA_Bug_Report.md` #0–#32) and their SOTA fixes
(`TRINETRA_Bug_Robustification.md` FIX #0–#15 + Appendix E) into an executable engineering program,
within the project's own hard constraints: **₹2,000/node**, **Kaggle 30 GPU-h/week**, offline-first,
Uttarakhand+Himachal. Everything here is design-level; no production code is shipped. Price/number tags:
`[EST]` = estimated, must be live-verified before procurement; `[STD]` = established; `[LV]` =
live-verified this session; `[FT]` = from local corpus.

> **Price-verification gate (applies to all BOM numbers below).** Every ₹ figure is `[EST]`, anchored to
> the shipped report's own BOM (which is itself `[EST]`). Robu.in / Amazon.in product pages returned
> HTTP 403 to automated fetch this session, so no price could be independently confirmed online.
> **Procurement rule: no node is ordered until each line item's price is re-checked against ≥2 live
> Indian suppliers and the per-node total is re-confirmed ≤ ₹2,000.** This gate is itself a deliverable.

---

## WS1 — Physics core correctness (closes #2, #3, #4, #17; supports #25)

**Scope.** The infinite-slope / TRIGRS / Iverson / Fukuzono stack and its numerics.

**Tasks.**
1. Apply PATCH B (Iverson transient term — no spurious `cos β`; slope only via `D₁=D₀/cos²β`) and
   PATCH C (suction-stress sign) and PATCH D (α / inverse-velocity regime). (See
   `TRINETRA_Corrected_Patches.md`.)
2. **Golden-case unit tests** [STD]:
   - Saturated limit `S_e→1 ⇒ σ_s→0` ⇒ FS reduces to the saturated infinite-slope form (acceptance test for #2).
   - `β→0` and `t→∞` reproduce the steady-state Iverson head (acceptance test for #3/#17).
   - α=2 ⇒ `1/v` linear; α≠2 ⇒ `v^(1−α)` linear (acceptance test for #4).
3. **Richards-equation numerical hardening** [FT 2105.13133, 1507.07837]: the Richards/Iverson solve is
   numerically delicate; use mass-conservative time-stepping and verify against an analytic infiltration
   benchmark before trusting field output.
4. **Rainfall-uncertainty propagation (#25)** [2605.17419]: feed the physics gate a neighbourhood/ensemble
   rainfall field (sample ±N-km displacement) → report a *distribution* of FS, not a point value.

**Gate G1:** all golden-case tests pass; FS monotonic in suction; Iverson matches the project's own
`research/06_physics §1.1`. No downstream module consumes the old (buggy) equations.

---

## WS2 — Evaluation validity (closes #11, #18, #19, #27, #31; the dominant cluster)

**Scope.** Make every headline number falsifiable. This is the highest-leverage workstream.

**Tasks.**
1. **Leakage-controlled splits** [FT 2608.12422]: tile-withheld (whole-map-tile) spatial cross-validation;
   also temporal holdout so no post-event info leaks into pre-event features (ties #7 EO-leak).
2. **Baselines mandatory in every table:** gradient-boosted trees + 3-rule decision tree (2608.12422),
   linear model (2510.10799), and — for the forecasting head — **persistence + seasonal-naive** (2509.18176).
   A deep model that does not beat these is reported as "does not beat baseline."
3. **Per-hazard reporting** [2410.04833]: landslide / flash-flood / cloudburst / GLOF separately, with
   bootstrap CIs; no single aggregate AUC.
4. **Honest RL valuation** [2110.14000 BVFT, 2311.18206 SCOPE-RL, 2106.08909, 2206.02000]: select policy by
   BVFT, risk-evaluate by SCOPE-RL (CVaR@5%, worst-case, full return distribution), report a one-step
   offline baseline alongside; deploy only if the OPE lower bound ≥ rule baseline.
5. **Feedback-aware OPE (#23)** [2312.01530]: model evacuation/alarm/maintenance feedback in the OPE.

**Gate G2 (ADMISSION GATE for the whole project):** every performance claim appears under BOTH random-CV
and spatial-CV, keyed to the spatial-CV column, with the baseline in the same table. Any claim that does
not beat the baseline under spatial-CV is withdrawn or restated. **This gate blocks publication.**

**Headline deliverable:** one leakage-controlled, spatial-CV, GB-baselined, persistence-benchmarked
**Joshimath/Chamoli hindcast** with a CI-bounded lead-time number.

---

## WS3 — Decision layer: thresholds, shield, calibration (closes #1, #5, #13, #20, #22, #24, #26)

**Scope.** The single decision function and its guarantees.

**Tasks.**
1. **One decision function** (PATCH A): `decide(s) = max(conformal_level(risk, τ*≈0.05), shield_floor(s))`.
   Unit test: every legacy threshold (0.5/0.12/0.048) maps to an internal role; no alert path bypasses it.
2. **Realizable shield (#20)** [2507.23603, 2305.16147]: `S(s)=max{level(r):r fires}` over Green<Yellow<
   Orange<Red; exhaustive compound-event test (rain+tilt+GLOF) never returns undefined.
3. **Predictive, reachability-aware shield (#26)** [2310.04288, 2511.21531, 2402.00816, 2112.11490]:
   least-conservative safe escalation; measure intervention-rate drop on benign states vs the fixed shield.
4. **Adaptive conformal (#13/#24)** [2202.07282 ACI/AgACI, 2303.12783 HopCPT, 2406.05405 missingness,
   2601.18509 survey]: replace split-conformal; report measured marginal + per-zone coverage with CIs;
   claim risk-control, not a fixed 90%. Honesty guard: EDL (2402.09056) used for ranking/OOD only, never
   as an absolute probability.
5. **Fix the 2603.15681 integrity defect (#5)** (PATCH G).
6. **Anti-collapse anomaly member (#22)** [2108.04907 FlowSVDD, 2405.18929 PU-AD]: bounded hypersphere
   radius test; PU training on the contaminated background.

**Gate G3:** single `decide()` function; shield proven total+realizable; measured conformal coverage near
nominal on a drifting holdout; anomaly radius bounded away from zero.

---

## WS4 — Fusion head (GMF) robustness (closes #21, #28; supports #31)

**Scope.** The Gated Meta-Fusion decision head (`TRINETRA_MetaFusion_Design.md`).

**Tasks.**
1. **Collinearity-robust meta-head (#21)** [2402.01379, 2006.08573, 2604.00801]: boosting / Caruana forward
   selection or architecturally-diverse experts; report meta-feature matrix condition number; bootstrap
   coefficient-stability test (sign-flip rate ≈ 0).
2. **Per-modality reliability gating (#28)** [2603.01511 MERA, 2512.01750, 2505.19190]: live quality signal
   (InSAR coherence, cloud fraction, node telemetry health) discounts a degraded expert. Inject-degradation
   test: fused weight on the blinded modality drops; calibration holds.
3. Keep the monotone post-shield (can only RAISE) from WS3.

**Gate G4:** meta-head coefficients stable under resampling; degraded-modality down-weighting demonstrated;
GMF never lowers the shield floor.

---

## WS5 — IoT nodes: compliant, tiered, within ₹2,000 (closes #6, #8, #14, #29, #30)

**Scope.** Re-spec the two nodes for India-compliance, realistic edge compute, and fault discrimination.

### WS5.1 — Node A "Slope Sentinel" (corrected BOM) — target ≤ ₹2,000 [EST]
| Part | Qty | ₹ [EST] | Purpose | Change vs shipped |
|---|---|---|---|---|
| ESP32-C3 SuperMini | 1 | 250 | MCU, deep sleep, Tier-0 logic | — |
| **SX1262 LoRa 865–867 MHz + antenna** | 1 | **480** | Long-range radio | **#6: replaces non-compliant 433 MHz SX1278** |
| MPU6050 accel/tilt in PVC pipe | 1 | 120 | Soil movement | — |
| Capacitive soil moisture v2 (two depths) | 2 | 140 | Saturation m | corrosion-resistant v2 |
| DIY tipping-bucket rain gauge | 1 | 100 | Local rain | — |
| BMP280 pressure/temp | 1 | 90 | Temp compensation | — |
| 6 V 1 W solar panel | 1 | 150 | Power | — |
| CN3791 MPPT charger | 1 | 150 | Charging | — |
| LiFePO4 cell (cold-tolerant) | 1 | 200 | Storage | — |
| IP65 box + PVC + glands | 1 | 250 | Housing | — |
| **Total** | | **≈ 1,930 [EST]** | | within ₹2,000 ✓ |

### WS5.2 — Node B "River Eye" (corrected BOM) — target ≤ ₹2,000 [EST]
| Part | Qty | ₹ [EST] | Purpose | Change |
|---|---|---|---|---|
| ESP32-CAM (OV2640, no-IR-filter) | 1 | 450 | Camera + MCU (Tier-0 only) | — |
| **SX1262 LoRa 865–867 MHz + antenna** | 1 | **480** | Radio | **#6** |
| 850 nm IR LED board | 1 | 100 | Night vision | — |
| Painted staff gauge on pier | 1 | ~0 | Stage reference | — |
| 6 V 2 W solar panel | 1 | 250 | Power | — |
| CN3791 charger | 1 | 150 | Charging | — |
| LiFePO4 cells | 1 | 250 | Storage | — |
| microSD 8 GB | 1 | 150 | Event clips | — |
| IP65 box | 1 | 150 | Housing | — |
| **Total** | | **≈ 1,980 [EST]** | | within ₹2,000 ✓ |

> The compliant SX1262 (865–867 MHz) is ~₹50 dearer than the non-compliant SX1278 (433 MHz) in the shipped
> BOM; both nodes still clear ₹2,000. **These prices are `[EST]` and MUST pass the price-verification gate
> above before ordering** (SX1262 India-band module prices were not confirmable online this session — 403s).

**Tasks (design).**
1. **Tiered edge→cloud compute (#14/#30)** [2604.08581, 2306.00001, 2604.27178, 2402.02781]:
   - **Tier 0 (on-node):** tiny statistical screen only — Z-score/RMS on tilt, stage threshold, on-node FS
     (eq 6.1), inverse-velocity fit (fits ~3.3 KB SRAM / 63 KB Flash budget [2604.08581]).
   - **Tier 1 (gateway/cloud):** the Cerberus VAD and SSL encoder (which run on L40S-class GPUs, NOT the
     MCU — this is the #14 correction). Knowledge-distill any model that must move node-ward.
2. **Storm brownout handling (#8)** [1908.04240 SAMM]: power-budget the alarm-mode duty cycle (River Eye
   worst day ≈ 0.9 Wh — already in the report §10.4); add unsupervised drift/degradation detection so a
   browning-out node is flagged, not silently trusted.
3. **Fault-vs-event (#29)** [1203.0541, 1509.06065, 2508.18045, 2602.24209]: Neyman-Pearson test +
   cross-node spatial consistency before a single node drives a shield override; robust change-point on
   tilt/SAR streams; label-free federated normality under the LoRa bandwidth budget.
4. **Gateway (unchanged, not under ₹2,000):** LoRa concentrator + satellite-IoT uplink where no cell signal
   (Skylo NB-NTN / Swarm-successor / Iridium SBD [MEM — verify]); optional Raspberry Shake geophone (this is
   the #7 fix — Chamoli-type ice/rock avalanches need a geophone that the node BOM omits).

**Gate G5:** both node totals ≤ ₹2,000 after price-verification; every model assigned to a hardware-feasible
tier with a stated compute/energy budget; a single faulty node cannot trigger RED unaided; LoRa band = 865–867 MHz.

---

## WS6 — Comms, security, and data integrity (closes #12, #7-leak)

**Tasks.**
1. **Remove the key-exfiltrating proxy (#12):** `Proxy.py`/`Proxy_fixed.py` forward credentials to the
   non-official `https://api.justwoker.icu`. Replace with the official API endpoint; rotate any exposed keys;
   add a test that fails if a non-allowlisted endpoint is configured.
2. **CAP/SACHET routing integrity:** sign alerts; dedup; ensure the offline-first path (LoRa→gateway→siren)
   works with the cloud unreachable.
3. **EO future-information leak (#7):** audit every feature's timestamp so no post-event satellite pass
   feeds a pre-event prediction (ties WS2 temporal holdout).

**Gate G6:** no credential leaves the official endpoint; alert path works offline; feature-timestamp audit passes.

---

## WS7 — Dataset registry, Kaggle/compute budget, novelty, reproducibility (closes #10, #15, #16, #18)

**Tasks.**
1. **Datacube size correction (#10):** re-estimate the InSAR datacube footprint (the report is 10–35× off);
   state the true storage/bandwidth and whether it fits Kaggle's limits.
2. **Dataset registry** (new deliverable) — candidate entries, each to be license-checked:
   | Dataset | Source | Use | Status |
   |---|---|---|---|
   | GLOFNet | 2510.10546 | GLOF detection training | candidate [ABS] |
   | HMAGLOFDB (589 outbursts) | via 2608.12422 (Kahn) | GLOF labels + spatial-CV tiles | candidate [ABS] |
   | Sentinel-1 InSAR, Sentinel-2, GPM IMERG, SMAP, ERA5-Land | ESA/NASA | inputs | free, confirmed in report |
   | Bhuvan/NRSC landslide inventory | ISRO | labels | verify license |
3. **I–D / GLOF constants (#15)** [2407.06785 Dahal lead; 2106.15119]: verify the report's three constants
   (Caine 14.82·D⁻⁰·³⁹, Dahal–Hasegawa 73.9·D⁻⁰·⁷⁹, Garhwal 1.82·D⁻⁰·²³) against their cited sources;
   2106.15119 argues a single borrowed constant is unjustified → fit a **distribution** of local
   Ks/slope/suction/γ_d instead of one fixed threshold.
4. **Kaggle budget (realistic, within 30 GPU-h/week):** the report's §9 plan (10 h FM fine-tune, 5 h anomaly,
   5 h offline-RL, 5 h PPO) is feasible IF the SSL encoder is a frozen EO-FM (#18/#16) rather than trained
   from scratch; re-scope novelty to the forecasting/pre-event regime + GMF head (PATCH G), benchmark against
   a frozen Prithvi-EO-2.0 (2412.02732) / Galileo (2502.09356) baseline.
5. **Reproducibility:** pin seeds, log the spatial-CV fold assignment, publish the baseline tables from WS2.

**Gate G7:** datacube size corrected; dataset licenses checked; I–D constants either sourced or replaced by a
fitted distribution; novelty claim matches real prior art; Kaggle plan fits 30 GPU-h/week.

---

## Cross-workstream quality gates (must all pass before "done")

| Gate | Workstream | Blocks |
|---|---|---|
| G1 physics golden tests | WS1 | downstream physics use |
| **G2 spatial-CV admission gate** | WS2 | **publication / any performance claim** |
| G3 single decision fn + realizable shield + measured coverage | WS3 | deployment |
| G4 fusion stability + reliability gating | WS4 | GMF deployment |
| G5 ≤₹2,000 + tiered feasibility + fault discrimination | WS5 | hardware order |
| G6 no key leak + offline alert path | WS6 | field pilot |
| G7 datacube/dataset/novelty/Kaggle | WS7 | submission |

## Sequencing (dependency order)
1. WS1 + WS2 first (correctness + valid evaluation are prerequisites for every claim).
2. WS3 + WS4 (decision layer + fusion) depend on WS2's honest metrics.
3. WS5 + WS6 (hardware/comms) run in parallel; WS5 depends on the WS5 price-verification gate.
4. WS7 (registry/novelty/compute) runs throughout; its G7 is the submission gate.

## Honesty ledger for this plan
- All ₹ figures are `[EST]` anchored to the shipped BOM; **not** independently price-verified (suppliers
  returned HTTP 403 to automated fetch). The price-verification gate is mandatory before procurement.
- Dataset entries are candidates at abstract depth `[ABS]`; licenses unverified.
- Every method citation (2608.12422, 2509.18176, 2311.18206, 2110.14000, 2202.07282, 2603.01511, 2604.08581,
  1203.0541, 2507.23603, 2310.04288, 2402.01379, 2108.04907, 2312.01530, 2406.05405, 2410.04833, 2605.17419,
  2210.12853, 2109.07745, …) is live-verified to ≥abstract in `analysis/02_paper_ledger.csv`.
- No production code is written here; this is a design + acceptance-test plan, consistent with "no code
  changes until the fix phase."
