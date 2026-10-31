# TRINETRA — Bug Robustification Spec (SOTA, per-bug fixes with citations)

**Purpose.** For every confirmed bug in `TRINETRA_Bug_Report.md`, this document gives a *concrete, defensible, citable* fix — what to change, the method to adopt, the primary source that justifies it, and the acceptance test that proves the fix worked. Pair with `TRINETRA_MetaFusion_Design.md` (which robustifies the RL path end-to-end).

**Evidence tags:** [LV] = live-verified from the internet this session; [FT] = full-text in local `papers/` corpus; [STD] = standard textbook/established result.

**All citations here were verified** against arXiv/publisher pages or the local 116-paper corpus. Verified-real IDs this session: CQL 2006.04779 [LV], IQL 2110.06169 [LV], Residual Policy Learning 1812.06298 [LV], Residual RL 1812.03201 [LV], Safe RL via Shielding 1708.08611 [LV], Galileo 2502.09356 [LV], TerraMind 2504.11171 [LV], Prithvi-EO-2.0 2412.02732 [LV], GLOF-SAR 2512.24117 [FT], Kahn 2608.12422 [FT], Chamoli-seismic PMC8904521 [FT], India LoRa 865–867 MHz (TTN) [LV].

---

## C-TIER (critical) robustifications

### FIX #0 — Make the QA pipeline trustworthy, then actually run it
**Bug:** `wf_a939fae0-f72` logged `completed` while failing on billing; defects never fixed.
**Robustification:**
1. **Fail-closed status semantics.** Any run where ≥1 required agent errors, or synthesis fails, must be labelled `failed`/`partial` — never `completed`. Add an invariant: `completed ⇔ (fixes_drafted == fixes_planned) ∧ (verifications_complete == verifications_planned) ∧ synthesis_ok`.
2. **Checkpoint + resume on 402.** Persist per-agent artifacts so a billing abort resumes instead of silently dropping 15/17 agents.
3. **Independent verifier gate.** No fix merges until an adversarial verifier (different context) reproduces the defect, applies the patch, and re-checks — the ANTIFAKE discipline the 21-agent review already defines.
**Acceptance test:** re-run; assert the status invariant; require a signed diff per bug ID below.

---

### FIX #1 — One decision function; dissolve the ~10× threshold conflict
**Bug:** P_f≥0.5 (physics) vs 0.12 (LHASA) vs 0.048 (RL) never reconciled.
**Robustification — a single, auditable decision pipeline:**
```
experts → gated meta-fusion head (see MetaFusion_Design) → per-zone Mondrian conformal risk control
         → ONE operating threshold τ* chosen to bound per-zone miss-rate → hard physics shield MAX-override
```
- The three numbers are reinterpreted, not averaged: `0.12` and `0.048` become **internal operating points** of two experts; `P_f ≥ 0.5` becomes a **shield trigger** (a hard floor), never a probability threshold competing with the others.
- τ\* is selected by **conformal risk control** (Angelopoulos et al., "Conformal Risk Control") so the thing being bounded is the *expected miss-rate per zone*, which is the quantity that actually matters. [STD; cite CRC paper from source]
**Acceptance test:** a single function `decide(state) → level` exists; unit test shows every legacy threshold maps into it; no code path emits an alert outside it.

---

### FIX #5 — Correct the 2603.15681 label and restate novelty honestly
**Bug:** real Himachal *flash-flood* GNN+conformal paper mislabelled "landslide," cited as a failing competitor AND denied to exist.
**Robustification (text-level, exact):**
1. Line 548/781: change "landslide mapping" → "**flash-flood susceptibility mapping in Himachal Pradesh (GraphSAGE over 460 sub-watersheds, AUC 0.978), with conformal UQ whose empirical coverage fell to 82.9% overall and 45–59% in high-risk zones**." [FT `papers/multimodal/2603.15681.txt`]
2. Delete the contradictory sentence (line 2842) "our searches returned no landslide papers → NOVEL." Replace with: "**The closest prior art, 2603.15681, already applies conformal UQ to regional hazard mapping with spatial CV; our contribution is the per-zone Mondrian *risk-control* calibration under a hard physics shield, which is an incremental extension, not a first.**"
3. Downgrade Novelty Claim #3 from "Strong/NOVEL" → "**Incremental** (combination + risk-control framing)."
**Acceptance test:** grep the report for "no landslide" and "NOVEL" near conformal → zero contradictory hits; the paper is described identically everywhere.

---

### FIX #11 — Make the evaluation falsifiable (fix the statistics)
**Bug:** n≈1 event/hazard, no protocol, no CIs → "beats LHASA" unfalsifiable.
**Robustification — a frozen, pre-registered scoring protocol:**
- **Decision unit:** fixed spatial cell (e.g. the Major-TOM 10 km grid cell or a sub-watershed) × time window (e.g. 24 h).
- **Hit definition:** alert within a declared spatial buffer (e.g. 5 km) and temporal window (e.g. −48 h to +6 h of event) = TP; else FP/FN.
- **High-n inventories, not 5 events:** use NASA Global Landslide Catalog + GSI Bhukosh + ICIMOD HKH for within-hazard n in the hundreds; **demote the 5 flagship events (Kedarnath'13, Chamoli'21, Joshimath'23, Himachal'23, Lhonak'23) to qualitative case studies.** [FT research/03 confirms these inventories]
- **Blocked spatio-temporal CV** to kill autocorrelation leakage — exactly the inflation Kahn et al. 2608.12422 demonstrate (naive susceptibility AUC ~0.9 is clustering artifact). [FT]
- **Metrics with CIs:** AUC-PR (not just ROC, because events are rare), POD/FAR, lead-time distribution, **bootstrap 95% CIs** on every number; compare to LHASA with a paired test.
**Acceptance test:** a reviewer can re-run the protocol and either confirm or refute "beats LHASA" at a stated significance level.

---

## M-TIER (major) robustifications

### FIX #2 — Sign-correct the suction-stress / unsaturated FS
**Bug:** sign bookkeeping between "σ_s negative = adds strength" and the explicit "− σ_s" term is self-cancelling/ambiguous.
**Robustification:** adopt the Lu & Likos (2006) *suction stress characteristic curve* convention explicitly and write FS once:
```
σ_s(S_e) = − S_e · (u_a − u_w)          [σ_s ≤ 0, tension positive-strength]
FS = tanφ'/tanβ + 2c'/(γ z sin2β) − σ_s (tanβ + cotβ) tanφ' / (γ z)
```
with a stated sign table and a **unit/sign assertion in code** (`assert d(FS)/d(saturation) < 0`). Validate monotonicity: FS must *decrease* as the slope wets. [STD Lu & Likos; cross-check against physics corpus `papers/physics/`]
**Acceptance test:** numerical sweep of S_e∈[0,1] shows FS strictly decreasing; dimensionless FS; at S_e=0 reduces to the dry §6.1 form.

### FIX #3 — Remove the spurious cos β in the Iverson transient term
**Bug:** extra `cosβ` on the transient term + `cos²β` on the static term vs canonical TRIGRS.
**Robustification:** reproduce Iverson (2000)/Baum et al. (2008) TRIGRS eqs exactly:
```
ψ(Z,t) = (Z − d) β-term + transient response R(t) with the slope correction entering ONLY via D₁ = D₀/cos²β
```
Pull the exact equation from the physics corpus (several Iverson/TRIGRS-adjacent PDFs present) and quote eq numbers. [FT `papers/physics/`]
**Acceptance test:** at β→0 the expression collapses to the 1-D Iverson solution; the response function uses `ierfc` with argument `Z/(2√(D₁t))` and no extra cosine multiplier.

### FIX #4 — Make the inverse-velocity method internally consistent
**Bug:** fits `1/v` (valid only at α=2) while advertising α∈[1.5,2.2] free.
**Robustification — two clean options, pick one and state it:**
- **(a) Fukuzono-fixed:** set α=2, fit the linear `1/v = A(α−1)(t_f−t)`, drop the "1.5–2.2" claim; OR
- **(b) Generalized failure-time:** estimate α by fitting the linearized `v^(1−α)` (Voight 1988 general law), with a Kalman/Bayesian filter on (α, A, t_f) and report t_f with a credible interval.
The MetaFusion design already routes this as the "multi-sensor Kalman failure-time" expert. [STD Fukuzono 1985 / Voight 1988]
**Acceptance test:** if α is reported as a free estimate, the fit target must be `v^(1−α)`, verified in code; residual plot linear in the chosen variable.

### FIX #6 — Legal radio: move to the Indian ISM band + terrain link budget
**Bug:** 433 MHz spec; India LoRa ISM is 865–867 MHz. [LV TTN]
**Robustification:**
1. Respec every node to **IN865–867 MHz** (SX1262-class transceiver, not SX1278/433).
2. Replace the single borrowed Nepal 5 km figure with a **terrain-aware link budget** (ITU-R P.526 diffraction over actual valley DEM profiles) at 868 MHz; report margin per link.
3. Enforce the regional **duty-cycle** limit; show SF12 airtime vs duty budget (the Meshtastic 180 dB figure is lab-only — don't lean on it). [FT research/02 lines 34–35]
**Acceptance test:** BOM shows 865–867 MHz hardware; a link-budget table per planned node with ≥X dB margin and compliant duty cycle.

### FIX #7 — Honest Chamoli lead-time + the sensor that actually sees it
**Bug:** the ~2.5 h Chamoli precursor is **seismic** (Tiwari/WIHG, PMC8904521 [FT]); no costed node has a seismometer; replay re-enacts rather than detects; EO backbone leaks future.
**Robustification:**
1. **Add a MEMS geophone/accelerometer** to the Slope Sentinel (the Matterhorn edge micro-seismic CNN, arXiv:1810.09409 [FT], shows F1 0.969 at 0.44 s on battery — the template) and **re-cost honestly** (this likely breaks ₹2,000 — say so).
2. **Bound the lead-time claim** to what each costed sensor can actually deliver; separate "seismic co-detection (needs geophone)" from "InSAR precursor (days, decorrelates in snow)."
3. **Leakage-controlled backbone:** for any Chamoli-2021 hindcast, use a backbone whose pretraining data ends before the event, and **coherence-weight** InSAR so snow/forest decorrelation down-weights rather than fabricates signal. [FT research/03 gap note]
**Acceptance test:** every quoted lead-time is attributed to a sensor in the costed BOM; hindcast uses a pre-event-frozen backbone.

### FIX #8 — Energy-robust River Eye for multi-day storms
**Bug:** sized for 1 alarm-hour → browns out in a multi-day storm.
**Robustification:**
1. Re-derive the energy budget for the **worst realistic case**: sustained alarm (e.g. 1 fps duty) over the design storm (e.g. 72 h) under minimal-solar cloud.
2. Add a **reserved life-safety energy floor** (battery partition the node may not spend on routine telemetry), a larger panel + supercapacitor buffer, and a **storm-aware duty cycle** that sheds non-critical load first.
3. Publish the Wh-generated-vs-consumed curve under design cloud. Soil-probe drift (arXiv:2210.03019 [FT]) handled by periodic recalibration.
**Acceptance test:** simulated 72 h storm leaves the life-safety floor intact; node never fully browns out during an active alarm.

### FIX #9 — Exposure-invariant RL reward (remove the miss-preferring inversion)
**Bug:** flat miss (−100) < disruption (0.01·N·H → −120 for 500 ppl·24 h) → agent can prefer a miss.
**Robustification — make BOTH terms scale with exposed population (per-capita):**
```
reward = − C_miss_pc · (people_at_risk · severity)        # miss scales with exposure
         − C_FA_pc  · (people_disrupted · hours) / K       # FA also per-capita, same units
         + w_lead · min(lead_h, cap)
         − c_cw · (needless_level_changes)
```
Choose `C_miss_pc ≫ C_FA_pc` so the ordering `oracle ≪ always-evacuate < never-evacuate` is **provably** safety-biased for *all* population sizes. Then train with **CQL (2006.04779 [LV])** or **IQL (2110.06169 [LV])** offline, and **ship-gate on Off-Policy Evaluation** (don't deploy a policy whose OPE lower-bound is worse than the rule baseline). Wrap in the learned **shield (1708.08611 [LV])** so the RL can never *lower* an alarm the physics floor raised.
**Acceptance test:** symbolic proof that `∂(expected reward)/∂(miss) < ∂(expected reward)/∂(evacuate)` holds for all N; OPE lower bound ≥ rule baseline.

### FIX #10 — Rescope the datacube to be real
**Bug:** "2–5 TB" vs true full-ROI ~45–130 TB; Kaggle-infeasible.
**Robustification:**
1. **Two-tier design:** (a) a **3-site pilot cube** (Joshimath, one HP basin, one GLOF lake) that genuinely fits free tiers (~1,000 tiles, few TB); (b) a **full operational cube** with an honest storage/compute budget line item (45–130 TB + GPU hours).
2. State the **InSAR processing reality**: ASF HyP3 + MintPy SBAS cannot process regional stacks on Kaggle RAM/quotas — the pilot uses pre-processed interferograms; the full system needs dedicated compute. [FT research/03]
**Acceptance test:** storage/GPU table whose pilot numbers match free-tier limits and whose full numbers match the km²×resolution×temporal arithmetic.

### FIX #14 — Honest edge latency (separate server GPU from on-node)
**Bug:** "<1 s / 57 fps" is Cerberus on an **L40S server GPU**; no Jetson number exists.
**Robustification:**
1. Quote Cerberus (2510.16290 [FT]) latency explicitly as **"57.7 fps on L40S, 151.8× faster than VLM baseline — datacenter GPU."**
2. **Architecturally split:** tiny anomaly scoring on-node (ESP32-CAM can only do motion/stage, not VLM); heavy video-anomaly on the **gateway/edge-server**; mark the Jetson latency as **unmeasured/TBD** and list it as a required benchmark. [FT research/02 lines 30,46]
**Acceptance test:** no latency number is attributed to a node that can't run that model; a benchmark TODO exists for Jetson.

---

## MEDIUM-TIER robustifications

### FIX #12 — Remove the key-exfiltrating proxy
**Bug:** `Proxy*.py` forwards API keys to non-official `api.justwoker.icu`.
**Robustification:** delete `Proxy.py`/`Proxy_fixed.py` from the repo (they are unrelated artifacts), add them to `.gitignore`, rotate any key ever sent through them, and confirm the historical leaked-SMTP credential (flagged in `plans/…meteor.md` L72) was revoked. Never forward bearer tokens to third-party hosts.
**Acceptance test:** repo contains no non-official endpoint; secret-scan clean.

### FIX #13 — Downgrade "guarantee" to risk-control; report real coverage
**Bug:** conformal "90% guarantee" is overstated (broken exchangeability, sparse high-risk cells) and self-voided by the hard shield.
**Robustification:** state **conformal *risk control*** (bounded expected miss-rate), not "coverage guarantee"; report **marginal AND per-zone** empirical coverage with bootstrap CIs; explicitly note the shield breaks exchangeability on red cells and that coverage is therefore conditional-not-guaranteed there — the exact failure 2603.15681 measured. [FT]
**Acceptance test:** the word "guarantee" is replaced by "risk control / bounded miss-rate"; a per-zone coverage table with CIs is present.

### FIX #15 — Verify every empirical constant to primary source
**Bug:** 7 load-bearing I–D/GLOF constants unverified; **confirmed absent from the local corpus** (the "73.9" hits are ML benchmark cells, not Dahal–Hasegawa; Caine/Scheidegger/Huggel/Froehlich appear only in reference lists, not as the quoted equations).
**Robustification:** obtain the original PDFs and quote exact equation + units + fitting dataset for each:
- Caine (1980) global I–D — *Geogr. Ann.* 62:23–27 (seen in reference lists [FT], equation not yet quoted);
- Dahal & Hasegawa (2008) Nepal I–D — *Geomorphology* (NHESS guess-URL 404'd; get the Elsevier DOI);
- Garhwal `1.82·D⁻⁰·²³` — **highest priority: the exponent 0.23 is anomalously shallow for an I–D curve; verify or correct first**;
- Huggel (2002) `V≈0.104·A^1.42`, Froehlich (1995) `Q_p=0.607·V^0.295·H_w^1.24`, Scheidegger (1973) runout, LHASA v1 `w_t∝t⁻²`.
**Acceptance test:** each constant carries a `[FT]` tag with page/eq number; any mismatch with the report is logged as a new defect.

---

## Cross-cutting robustification: the MetaFusion decision head
All of FIX #1, #4, #9, #13 are unified by `TRINETRA_MetaFusion_Design.md`: experts (physics / offline-RL / supervised) → gated meta-fusion residual head (takes raw evidence **and** the RL policy's logits as input, per the user's design) → per-zone conformal risk control → hard monotone physics shield. This is stacked generalization + residual policy learning (1812.06298 [LV]) + shielding (1708.08611 [LV]) + offline RL (CQL 2006.04779 / IQL 2110.06169 [LV]) — every component verified real.

---

## Residual-risk register (what robustification CANNOT fix)
- **n is still small.** Meta-fusion and better protocols reduce variance; they cannot create statistical power from ~5 flagship events. The honest path is the high-n inventory evaluation (FIX #11) + case studies.
- **InSAR physically decorrelates** in snow/dense monsoon forest; no algorithm recovers signal that the C-band never captured. Coherence-weighting bounds the damage; it is not a cure.
- **Zero real end-to-end demonstration remains the #1 gap** (C1 in the review). The single highest-leverage action is still **one leakage-controlled Joshimath hindcast with a real, CI-bounded lead-time number.** Everything above makes that number *credible*; it does not substitute for it.

---

# APPENDIX C — Literature-grounded upgrades (second deep reading pass, 100+ papers)

This appendix records robustification-relevant findings from a systematic second reading of the local corpus (now ~40 papers read in full-abstract/method depth beyond the first pass, on top of grep-scanning all 116). Each item either **strengthens a fix with a citation** or **adds a prior-art obligation** to a novelty claim. All IDs verified present in `papers/`.

## C.1 Prior art that novelty claims MUST now cite (strengthens Bug #5, #16, and the GLOF/FM claims)
| Paper | ID [FT] | Why it constrains a TRINETRA claim |
|---|---|---|
| **Landslide Hazard Mapping with Geospatial Foundation Models** (ASU + NASA Marshall, Nov 2025) | 2511.04474 | **Direct prior art for the core task.** Shows Prithvi-EO-2.0 beats TerraMind, SatMAE, U-Net/U-Net++, Segformer, SwinV2 on landslide mapping across sensor/label/domain axes. TRINETRA's "SSL encoder for landslide EO" is **not first**; it must benchmark against this and cite it. |
| **IceWatch: GLOF prediction via Multimodal Deep Learning** | 2601.12330 | **Direct prior art for the GLOF claim.** Multimodal, physics-informed: Sentinel-2 CNN + ITS_LIVE glacier velocity + MODIS LST + tabular physics cross-validation — the *same* modality stack TRINETRA proposes for GLOFs. Novelty claim must be downgraded/differentiated. |
| **Targeted GLOF segmentation from time-series SAR** (NAST Nepal) | 2512.24117 | Temporal-first SAR GLOF EWS, IoU 0.9130. Prior art for the SAR-GLOF monitoring sub-claim. |
| **Forecasting landslides via community detection on InSAR** | 2212.12038 | Prior art for "InSAR precursor detection": slope×deformation network modularity found Mud Creek *before* failure. TRINETRA's anomaly layer must cite this as the InSAR-precursor baseline. |
| **Superposable Neural Network (interpretable), E. Himalaya** | 2201.06837 | Interpretable additive model trained on *easternmost Himalaya* inventories; beats physical+statistical models. Both a baseline and a template for the interpretable meta-fusion head. |
| EO foundation models the report under-benchmarks | SkySense 2312.10115; Copernicus-FM 2503.11849; AnySat 2412.14123; SatMAE 2207.08051; CROMA 2311.00566 | The SSL-encoder claim should benchmark against (or at least cite) these multimodal SAR+optical FMs, not only Galileo/Prithvi/TerraMind. CROMA's radar-optical masked autoencoder is the closest architectural match to TRINETRA's proposed InSAR+optical SSL encoder. |

**Action:** add a "Prior art & baselines" paragraph to every novelty claim (FM encoder, GLOF, InSAR-precursor, conformal). This converts three fragile "NOVEL" claims into defensible "incremental, benchmarked against X" claims.

## C.2 Citations that STRENGTHEN existing fixes
- **FIX #2 (suction-stress sign):** `2411.04333` (Roy & Chakraborty, IIT Madras/BHU) analyses suction-stress profiles under the van Genuchten SWCC with **independent m,n** — use its convention and its warning that m–n coupling changes the sign/shape of the profile. This is a stronger, India-authored primary source than a generic textbook cite.
- **FIX #3 (Iverson/TRIGRS):** `1305.4803` (Raia et al., TRIGRS-P, GMD) + `1306.1529` (Alvioli et al.) are the authoritative implementations; quote `D₁ = D₀/cos²β` from them. Confirmed no extra transient cosine.
- **FIX #4 (failure-time):** `2103.10939` ("The Landslide Velocity") + the Voight/Fukuzono originals; `2509.10560` (geodetic time-series forecasting toolbox) supports the Kalman-on-displacement expert.
- **FIX #9 (RL reward / safety):** `2302.03122` (State-wise Safe RL survey, CMU) gives the formal **SCMDP** framework to express "shield can only raise" as a state-wise constraint; `2005.01643` (Levine offline-RL tutorial) + `2006.04779` (CQL) + `2110.06169` (IQL) + `2106.06860` (TD3+BC) justify the offline-RL + OPE ship-gate. **The reward must be OPE-gated, not just trained.**
- **FIX #1 / meta-fusion (robustifies #1, #13):** `2009.07415` (Meta-AAD — a **meta-policy over anomaly detection**) and `2205.09884` (**RL-based model selection** over a pool of anomaly detectors) are the *direct* prior art for the gated meta-fusion head. The head is best framed as "learned expert-selection/weighting," which these two papers establish as effective — strong support, but also a novelty constraint (cite them).
- **FIX #8 (energy):** `2210.03019` (resistive vs capacitive soil-moisture calibration) — justifies periodic recalibration and choosing capacitive probes; `2412.08477` (CNN water-level, R²=0.9885) supports camera-stage as a cheap robust gauge.
- **FIX #11 (physics-gate / PIML eval):** `2606.04143`, `2507.15021`, `2512.23964` (DUALFloodGNN) all embed hydrological constraints in the loss — precedent for TRINETRA's physics gate and for reporting physics-consistency as an eval metric, not just accuracy.

## C.3 New robustification sub-findings (promoted into the bug file where material)
- The InSAR-precursor capability (community detection, 2212.12038) was demonstrated on **Mud Creek (California), a creeping slow-motion slope** — not a brittle, snow/forest-covered Himalayan failure. The report should not assume InSAR-precursor transfers to Chamoli-type rock/ice avalanches; this reinforces Bug #7's "InSAR decorrelates / seismic needed" point.
- Prithvi-EO-2.0's landslide win (2511.04474) is on **mapping (post/co-event segmentation)**, not **forecasting (pre-event)**. TRINETRA's value proposition must be stated as *forecasting*, where the FM literature is far weaker — this is actually where a defensible (narrow) novelty survives.

## C.4 Edge-VAD and seismic-edge: concrete hardware-claim fixes (strengthens Bug #7, #14)
- **FIX #14 upgrade — use a real edge VAD, not a server-GPU one.** `2410.21991` (**RuleVAD**, IEEE) is a lightweight dual-branch weakly-supervised VAD **engineered for consumer edge devices** — the correct citation for an *on-node* latency claim, replacing the Cerberus-on-L40S overclaim. Report Cerberus as the server-GPU accuracy ceiling and RuleVAD-class models as the edge-deployable path; still mark the actual Jetson/ESP32 latency as a required benchmark.
- **FIX #7 upgrade — the seismic-edge precursor sensor is proven.** `1810.09409` (**ETH Zürich, Matterhorn/Illgraben**) runs an event-triggered CNN for natural-hazard micro-seismic detection **on battery-powered edge nodes** — confirmed in-corpus. This is the concrete template (and BOM justification) for adding a MEMS geophone to the Slope Sentinel; cite it when re-costing. Also `2204.07653` (Xu, USGS/Stanford) shows SAR coherence-change + causal-graph Bayesian updating for co-seismic ground failure — supports the InSAR-coherence-weighting fix and the physics/Bayes fusion gate.

## C.5 Runout and physics-gate precedents (strengthens FIX #11, Scheidegger runout in #15)
- `2401.13695` (differentiable **Graph Network Simulator** for granular-flow runout, UT Austin/K. Kumar) and `2404.15860` (hybrid **FEM+MPM** tailings-dam runout) are modern, citable runout models — stronger than a bare Scheidegger `tanα = H/L` empirical ratio. Recommend: keep Scheidegger as the cheap analytic prior, cite GNS/MPM as the high-fidelity validation path.
- India-authored PIML precedents for the physics gate: `2104.11009` (**IIT Gandhinagar**, physics-informed hydrology with UQ) and the flood-PIML set (`2606.04143`, `2507.15021`, `2512.23964` DUALFloodGNN, `2511.09130` PIFF). These justify embedding physical constraints in the loss / as a gate and reporting **physics-consistency as an eval metric**, not only accuracy.
- `2007.02756` (Bevilacqua et al., INGV) is the **real-data** application of the stochastic failure-forecast (Voight) method to GPS displacement — the correct primary cite for FIX #4's probabilistic t_f, replacing the generic reference.

## C.6 Running tally (honesty on the "100 papers" ask)
Full-depth reads this pass (abstract+method+key results), on top of the first pass and the all-corpus grep scan:
RL: 2009.07415, 2104.00543, 2106.06860, 2205.09884, 2302.03122, 2005.01643, 2006.04779 (+ 2110.06169, 1812.06298, 1812.03201, 1708.08611 live earlier).
Physics: 1305.4803, 1306.1529, 2204.06097, 2407.06785, 2411.04333, 2606.04143, 2507.15021, 2512.23964, 2511.09130, 2401.13695, 2404.15860, 2104.11009, 2007.02756, 2512.24117, 2601.12330, 2103.10939, 2509.10560 (skim).
Satellite/Multimodal: 2201.06837, 2207.08051, 2311.00566, 2312.10115, 2503.11849, 2412.14123, 2511.04474, 2212.12038, 2603.15681, 2608.12422, 2502.09356, 2504.11171, 2412.02732, 2211.07044.
IoT/CCTV: 2210.03019, 2412.08477, 2410.21991, 1810.09409, 2510.16290, 2412.04563, 1607.04139.
Satellite(geo): 2103.10939, PMC8904521, PMC8050240, chamoli.txt.
**That is ~50 papers read in depth + ~66 grep-scanned across the 116-file corpus + ~12 live arXiv/web verifications = the full corpus covered, >100 distinct papers engaged.** I did **not** read 500 — and I will keep saying so. Depth was spent where it changes a fix or a claim.

---

# APPENDIX D — EXTERNAL papers (NOT in the local corpus), fetched & verified live this pass

Per the instruction "read papers *beyond* the ones already available." Each ID below was fetched live from arXiv this session, confirmed real (title/authors/abstract), and is **absent from `trinetra/papers/`**. These close the exact methodological gaps the fixes leaned on.

| # | External paper (verified live) | arXiv | Fixes it hardens / what it adds |
|---|---|---|---|
| E1 | **Adaptive Conformal Inference Under Distribution Shift** — Gibbs & Candès | 2106.00170 | **FIX #13 / #1.** The *actual algorithm* for online conformal threshold updates that keep coverage under non-exchangeable drift (seasons, new sensors). The report's "adaptive conformal" hand-wave now has its real source + provable long-run coverage irrespective of the data-generating process. |
| E2 | **Conformal Risk Control** — Angelopoulos, Bates, Fisch, Lei, Schuster | 2208.02814 | **FIX #13 (the overclaim fix).** Converts the illegal "mathematical guarantee" into a *correct* claim: bound the **expected miss-rate** (a monotone loss), tight to O(1/n). This is exactly the "bound the thing that kills people, not just coverage" statement TRINETRA should make. Has code. |
| E3 | **A Gentle Introduction to Conformal Prediction & Distribution-Free UQ** — Angelopoulos & Bates | 2107.07511 | Canonical reference + Python notebooks; explicitly covers **time-series, distribution shift, outliers, models that abstain, and RL**. Use as the implementation backbone and the citation anchor for the whole UQ section. |
| E4 | **MixMatch: A Holistic Approach to Semi-Supervised Learning** — Berthelot et al. | 1905.02249 | **FIX #11 (n≈5 underpowered eval).** SSL to exploit the huge *unlabelled* InSAR/optical/IoT stream when labelled failure events are only ~5: on CIFAR-10 w/ 250 labels error drops 38%→11%. Template for learning from abundant unlabeled + scarce labeled Himalayan data. |
| E5 | **Focal Loss for Dense Object Detection (RetinaNet)** — Lin, Goyal, Girshick, He, Dollár | 1708.02002 | **FIX #9 / #11 (extreme class imbalance).** Landslide/GLOF days are rare positives drowned by negatives; focal loss is the standard, citable remedy for the detector feeding the RL policy — complements the cost-sensitive reward rather than fighting it. |
| E6 | **SAMM: Automatic Model Monitoring for Data Streams** — Pinto, Sampaio, Bizarro (Feedzai, KDD-ADF 2019) | 1908.04240 | **FIX #8 (storm brownout) + ops.** Unsupervised concept-drift detection *before labels arrive*, with auto-generated alarm reports — the pattern for detecting when a sensor node degrades (power brownout, fouled probe) in-field without waiting for a confirmed miss. |

**Discarded (fetched, verified NOT relevant — logged for honesty):** 2106.00226 (HDG methods for advection-diffusion PDEs), 2303.10953 (error-correction in social networks). I checked them, they didn't fit, I'm not citing them.

**Net:** 6 new *external*, corpus-absent, live-verified papers now backstop the two weakest fixes — the conformal "guarantee" overclaim (#13) and the underpowered/ imbalanced evaluation (#9, #11) — with their canonical primary sources instead of hand-waves.

---

# APPENDIX E — SOTA fixes for the 14 literature-grounded findings (#19–#32)

These robustifications pair one-to-one with Bug Report findings #19–#32, which were surfaced by the 250-paper deep-literature sweep (ledger `analysis/02_paper_ledger.csv`, synthesis `analysis/04_synthesis.md`). Every supporting ID was opened live to ≥abstract this session. The grouping mirrors the Bug Report priority clusters: **evaluation validity → safe-RL → calibration → fusion → hardware/decision realism.**

## E.1 Evaluation validity (the now-dominant cluster)

### FIX #19 — Persistence/seasonal-naive baselines in every forecasting evaluation
**Finding:** forecasting head may be invisible persistence (2509.18176).
**Robustification:** add two mandatory reference forecasters — (a) **persistence** (x̂_{t+h}=x_t) and (b) **seasonal-naive** (x̂_{t+h}=x_{t+h−period}). Report a **skill score** `SS = 1 − MSE_model/MSE_persistence`; a positive SS on *change windows* (|Δ|>threshold) is required before any "we forecast the precursor" claim. Segment all metrics into change vs no-change subsets so the autocorrelated majority cannot mask zero change-skill.
**Acceptance test:** forecasting section reports SS vs persistence AND seasonal-naive, broken out on change events, with bootstrap CIs; a non-positive change-window SS blocks the forecasting claim.

### FIX #23 — Feedback-aware off-policy evaluation
**Finding:** the alarm/sensing policy itself shifts the data distribution (2312.01530 AFAPE).
**Robustification:** treat evaluation as a counterfactual under an intervention: model the acquisition/alarm decision as the feedback mechanism (AFAPE-style missing-not-at-random correction) so logged-data value estimates are de-biased. Combine with the honest-OPE stack in FIX #27. Explicitly document the three feedback channels (evacuation changes exposure; alarms change behaviour; maintenance changes which sensors report) and encode each in the OPE model.
**Acceptance test:** every "the policy would have achieved X on history" number carries a feedback-corrected estimator and a sensitivity analysis over the feedback assumptions.

### FIX #27 — Honest off-policy value, not simulator PPO return
**Finding:** policy reported on training-env reward only (2106.08909, 2206.02000, 2110.14000, 2311.18206).
**Robustification:** (1) **select** the policy with hyperparameter-free **BVFT** (2110.14000) rather than best training return; (2) **risk-evaluate** with **SCOPE-RL** (2311.18206) reporting the full return *distribution* and tail/CVaR value — mandatory when miss cost = −100; (3) try a **one-step offline** baseline first (2106.08909) and only adopt the heavy CQL/IQL→PPO stack if it beats it under OPE; (4) report OPE with CIs via **HVE** (2206.02000). Ship-gate: deploy only if the OPE lower bound ≥ rule baseline (ties FIX #9).
**Acceptance test:** a policy-selection + risk-return OPE table (mean, CVaR@5%, worst-case) with CIs exists; the one-step baseline is reported alongside; no deployment claim rests on simulator return.

### FIX #31 — Per-hazard / per-class fusion metrics; ablate fusion strategy
**Finding:** no single fusion dominates (2410.04833).
**Robustification:** report metrics **per hazard** (landslide / flash-flood / cloudburst / GLOF) with CIs, never one aggregate AUC; ablate early vs late vs MoE fusion per hazard; include the Bayesian causal-graph fusion comparator (2204.07653) that natively handles sparse/unobserved hazard nodes. State explicitly that the chosen GMF fusion is not assumed globally optimal.
**Acceptance test:** a per-hazard × per-fusion-strategy metric table exists; the worst per-hazard cell (likely GLOF, rarest) is called out and defended.

### STANDING FIX (over FIX #11) — tile-withheld spatial CV vs GB/decision-tree baseline
**Finding:** on-region competitor (2608.12422) shows naive AUC 0.9 → 0.54 under honest spatial CV, and DL does not beat gradient-boosting; corroborated by 2510.10799 and 2106.08909.
**Robustification:** make **tile-withheld (whole-map-tile) spatial cross-validation against a gradient-boosted / decision-tree baseline** the admission gate for *every* headline performance number. Any claim that does not survive it is withdrawn or restated as "does not beat GB baseline." Combine with the spatial-CV scheme + EVT-tail loss of 2110.09497.
**Acceptance test:** a results table where each headline metric appears twice (random-CV vs tile-withheld spatial-CV) alongside the GB baseline; claims keyed to the spatial-CV column only.

## E.2 Safe-RL correctness

### FIX #20 — Make the shield provably realizable (priority lattice)
**Finding:** stacked hard overrides can be mutually unrealizable (2507.23603).
**Robustification:** define the shield as `S(s) = max{ level(r) : rule r fires in state s }` over the ordered set Green<Yellow<Orange<Red, and the output as `â' = max(â, S(s))` (monotone, can only raise). This makes the shield **total and realizable by construction** (a max over a totally ordered lattice always exists). Formally verify no state yields a contradiction; learn the safe set as a **convex constraint set from safe demonstrations (CoCoRL, 2305.16147)** so it is transferable across catchments.
**Acceptance test:** a proof/exhaustive check that S(s) is defined for all triggered-rule combinations; unit tests on compound events (rain+tilt+GLOF) return the max level, never undefined.

### FIX #26 — Replace fixed-fallback shield with a predictive, reachability-aware shield
**Finding:** fixed-fallback RTA is provably suboptimal and can still violate (2310.04288, 2511.21531, 2402.00816, 2112.11490).
**Robustification:** adopt an **optimal runtime-assurance switch** (2310.04288) that raises an alarm only when reachability analysis proves it necessary (least-conservative), with a **predictive shield** (2511.21531 / 2402.00816) that selects the best *safe* escalation rather than a fixed fallback; use **latent shielding** (2112.11490) for the high-dim sensor state; compose the miss/FA/lead/disruption objectives via **successor features (SUSFAS, 2409.04641)** instead of one hand-tuned scalar.
**Acceptance test:** the shield's intervention rate on benign states drops vs the fixed version while retaining the hard safety floor; a reachability certificate accompanies each override class.

## E.3 Calibration / UQ

### FIX #24 — Adaptive conformal under missingness + feedback + autocorrelation
**Finding:** split-conformal invalid under TRINETRA's exact conditions (2406.05405, 2511.11567, 2303.12783, 2202.07282, 2601.18509).
**Robustification:** replace split-conformal with **online adaptive CP — ACI/AgACI (2202.07282)** or **HopCPT (2303.12783)** — which restores honest long-run coverage on temporally dependent, drifting streams; add explicit **missingness handling (2406.05405)** so dropped sensors do not silently void coverage; publish measured **marginal AND per-zone** coverage with CIs; claim conformal **risk-control** (FIX #13), not coverage. **Honesty guard: do NOT substitute an over-trusted evidential-DL probability** — 2402.09056 proves EDL epistemic uncertainty is only *relative*; use EDL for ranking/OOD flagging only, back thresholds with conformal.
**Acceptance test:** coverage is measured online over a drifting holdout and stays near nominal with ACI/AgACI where split-conformal drifts; per-zone coverage table with CIs; no absolute probability claim rests on EDL alone.

### FIX #22 — Anti-collapse anomaly member on a contaminated background
**Finding:** Deep-SVDD hypersphere collapse + contaminated "normal" (2108.04907, 2405.18929).
**Robustification:** replace plain Deep SVDD with an **anti-collapse variant (FlowSVDD, 2108.04907** — invertible map prevents the zero-radius degenerate solution), and treat the background as **positive-unlabeled (2405.18929)** rather than clean-normal, since the Himalayan record contains unlabeled real precursors. Keep interpretable iForest variants (DIFFI 2007.11117) in the ensemble.
**Acceptance test:** the learned hypersphere radius is bounded away from zero on a held-out run; PU-trained scores separate injected synthetic precursors from background better than clean-normal training.

## E.4 Fusion design

### FIX #21 — Collinearity-robust meta-head
**Finding:** correlated experts destabilize the stacked head (2402.01379).
**Robustification:** replace a plain linear/ridge meta-learner with a **boosting meta-learner or Caruana forward ensemble selection** (both robust to multicollinearity), or build **architecturally diverse experts (Neural Ensemble Search, 2006.08573)** so base predictions decorrelate; regularize and **report the condition number** of the meta-feature matrix as a stability metric. Consider the **routing-free self-activating MoE (2604.00801)** to avoid a brittle learned router over correlated experts.
**Acceptance test:** meta-head coefficients are stable under bootstrap resampling (sign-flip rate near zero); condition number reported and bounded.

### FIX #28 — Per-modality reliability gating
**Finding:** GMF fuses experts without a reliability signal (2603.01511, 2512.01750, 2505.19190).
**Robustification:** attach a **live quality/coverage signal** to each modality (InSAR coherence, optical cloud fraction, node battery/telemetry health) and discount that expert via **Dempster-Shafer evidential reliability (MERA, 2603.01511)** or **reliability-gated sparse MoE (2512.01750)**; model agree/contradict interactions with **I2MoE (2505.19190)**. A degraded sensor's expert contribution scales toward zero rather than being trusted equally.
**Acceptance test:** inject a degraded modality (simulated brownout / full cloud / decorrelated InSAR) and show the fused decision weight on that expert drops accordingly while overall calibration holds.

## E.5 Hardware / input / decision realism

### FIX #29 — Fault-vs-event discrimination + cross-node consistency
**Finding:** faulty sensors fabricate/mask events undetected (1509.06065, 1203.0541, 2508.18045, 2602.24209).
**Robustification:** before any single node drives a shield override, run a **Neyman-Pearson/Bayes fault-vs-event test (1203.0541)** and a **cross-node spatial-consistency check (DependSHM, 1509.06065)**; use a **robust Riemannian streaming change-point detector (2508.18045, Huber centroid)** for manifold-valued streams (tilt, SAR covariance) that fires on real regime shifts but resists outliers; learn cross-node normality with **label-free federated anomaly detection (2602.24209 / FedIoT)** under the LoRa bandwidth budget.
**Acceptance test:** a stuck/biased single node does NOT trigger a RED override unless corroborated by neighbours or physics; a dead node is flagged, not silently treated as "no hazard."

### FIX #30 — Explicit tiered edge→cloud compute design
**Finding:** heavy stack cannot run on a ₹2,000 node (2604.08581, 2306.00001, 2604.27178, 2402.02781).
**Robustification:** formalize **two tiers** — (Tier 0, on-node) tiny statistical screen (Z-score/RMS/stage threshold), proven to fit ~3.3 KB SRAM / 63 KB Flash at µs latency (2604.08581), optionally a <0.5 MB MCU detector (TinyissimoYOLO, 2306.00001); (Tier 1, gateway/cloud) the heavy VAD/SSL encoder. Use **knowledge distillation (2604.27178, 2402.02781)** to compress any model that must move toward the node. Size each tier's compute/energy explicitly and state the escalation trigger. Resolves #14 and #30 together.
**Acceptance test:** every model is assigned to a tier whose hardware can host it; a compute/energy budget table per tier; node never claims to run a model exceeding its SRAM/Flash/power.

### FIX #32 — Compliance-aware, equity-weighted, exposure-invariant decision economics
**Finding:** people-at-risk + reward assume 100% uniform compliance (2109.07745 ≈46% compliance + shadow evacuation, 2502.17701, 2412.05777).
**Robustification:** replace the implicit full-compliance assumption with a **compliance probability** calibrated to ~50% ordered compliance plus modelled **shadow (self) evacuation** (2109.07745); **equity-weight** the disruption cost so vulnerable groups are not systematically under-served; make the reward **exposure-invariant** (per-capita, ties FIX #9) so the lead-time credit (+2/h) and disruption penalty (−0.01/person-hour) are not biased by assuming everyone evacuates identically; keep **humans in the threshold-setting loop** with explanations (2512.14683).
**Acceptance test:** people-at-risk estimates carry a compliance factor and uncertainty; the reward's safety ordering holds under partial/heterogeneous compliance; an equity audit of who is disrupted vs protected is reported.

### FIX #25 — Propagate rainfall-forecast spatial/structural uncertainty into the physics gate
**Finding:** physics gate assumes point-accurate rainfall; QPF has large spatial-displacement error (2605.17419; mitigations 2210.12853, 1706.03458).
**Robustification:** feed the physics gate a **neighbourhood/ensemble** of rainfall realizations (sample over plausible spatial displacements) rather than a single point value, so the gate reports a *distribution* of FS/trigger outcomes; improve the input itself by **attentive fusion of sparse ground gauges with radar/GPM (ASOC, 2210.12853 — +5.7% CSI on heavy rain 1–6 h)** and a rare-pixel-weighted nowcaster (TrajGRU, 1706.03458); evaluate rainfall-driven warnings with **neighbourhood-tolerant scores (CSI/FSS)**, not point metrics.
**Acceptance test:** the physics gate consumes an ensemble/neighbourhood rainfall field; warnings are scored with FSS at a declared neighbourhood radius; sensitivity of the trigger to ±N-km displacement is reported.

---

**Appendix E net effect:** all 14 literature-grounded findings now carry a concrete, citable SOTA fix with an acceptance test, every citation live-verified to ≥abstract. Combined with FIX #0–#15 and Appendices C–D, the robustification spec covers all **33 findings (#0–#32)**. The single highest-leverage action is unchanged: **one leakage-controlled, spatial-CV, GB-baselined, persistence-benchmarked Joshimath hindcast with a CI-bounded lead-time number** — which now has, behind it, the full methodological machinery (FIX #11, #19, #23, #24, #27, #31 + the standing spatial-CV gate).
