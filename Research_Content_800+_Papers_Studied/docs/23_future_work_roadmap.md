# 23 — Future Work & Roadmap

> **Read `_CANON.md §0` first.** This chapter is a **plan**. Per `FINAL_REPORT.md`:
> *"Nothing was built, trained, or measured."* No TRINETRA model has been trained and no dataset has
> been downloaded (`_CANON §0`). Therefore **every roadmap item below is future work** — nothing on
> this page is a result, a measurement, or a commitment that has been met. Items are tagged
> `[CONFIRMED]` / `[LIKELY]` / `[HYPOTHESIS]` / `[INFEASIBLE]` per `_CANON §1`. Where a number comes from
> a paper it is **SOURCE-REPORTED** (that paper's data, not ours, Rule 16). arXiv IDs are cited **only
> where the source artifact gives them**, and most are **subagent-reported, NOT independently re-fetched**
> (`_CANON §7`) — re-resolving them is itself a build gap (§4.5 below).

The two code-status facts that ARE real anchor the whole roadmap and must not be confused with roadmap
"results": `python run_tests.py` → **128 tests, OK**; `python scripts/ci_gates.py` → **ALL 6 CI GATES
PASSED** (numpy core; `_CANON §2`). The PyTorch `deep/` layer and Kaggle scripts are **compile-verified
only, never GPU-trained here** (`_CANON §2`). Everything in this chapter builds forward from that state.

Sources for this chapter: `FINAL_REPORT.md §14` (build order) and `§15` (open backlog / next steps);
`TRINETRA_Workstreams.md` (WS1–WS7 tasks, gates G1–G7, sequencing); `FEATURES.md` (Wave-1 F-11..F-17,
Wave-2 F-18..F-22, Wave-3 F-23..F-26); `KAGGLE_BUDGET.md` (budget + cut-list); `HANDOFF/BUILD_HANDOFF.md`
(preliminary build order); `DEPLOYMENT/` (pilot, stakeholders, standards). The gate numbering uses the
**internal-artifact WS scheme**; see `_CANON §3` for the mapping to the doc-chapter WS frame.

---

## 23.1 The build order (the ~8-step sequence)

Verbatim source: `FINAL_REPORT.md §14` ("Recommended build order"), cross-referenced to the gates in
`TRINETRA_Workstreams.md` (G1–G7, §"Cross-workstream quality gates") and the preliminary order in
`HANDOFF/BUILD_HANDOFF.md`. Each step lists its **precondition**, the **gate that admits it**, and its
**honest dependency**. Nothing in this sequence has been started; the whole sequence is `planned`.

Every step is additionally gated by its **pre-registered cross-camera/cross-site decision rule**
(`FINAL_REPORT §9`, `FEATURES.md §P17 admission rules`): keep a feature only if its improvement exceeds
seed/trial variance on a **held-out cross-camera/cross-site split**, confirmed by the inferential-
reproducibility test (F-17; 2302.04054 LMEM, source-reported). *A benchmark-local win that hurts
cross-camera is NOT a win.*

### Step 1 — Eval tooling + "real-win" gate + leakage-controlled benchmark
- **Build:** F-17 experiment tooling (provenance dagger 2006.07484 + inferential-reproducibility LMEM+GLRT
  2302.04054, both source-reported) and the data/benchmark curation that produces **C-05**, the
  leakage-controlled CCTV zero-shot benchmark (`FINAL_REPORT §13`), with datasheets.
- **Precondition:** none — this is first. `HANDOFF/BUILD_HANDOFF.md` makes the same call: the
  spatial-CV harness + baselines (persistence, gradient-boosted, 3-rule tree) **must exist before any
  model is trusted**.
- **Admitting gate:** **G2** (spatial-CV admission gate — the project-wide ADMISSION GATE that *blocks
  publication / any performance claim*) and **G7** (datacube/dataset/novelty/Kaggle). The benchmark must
  carry both random-CV and spatial-CV columns keyed to the spatial-CV result, with baselines in the same
  table (`TRINETRA_Workstreams.md` G2).
- **Honest dependency:** **datasets must be collected and licenses verified first** — all datasets are
  STATUS=candidate `[D]`, licenses INDICATIVE/UNVERIFIED, none selected (`FINAL_REPORT §5`,
  `_CANON §7` via `§9` map). Portal + license verification is an OPEN backlog item (`FINAL_REPORT §15.2`).
  This is a **~days-to-weeks** data-access + license task, not an afternoon. `[HYPOTHESIS]` that C-05 as
  specified is realizable until the data is in hand.

### Step 2 — Edge CCTV detector + physics feature
- **Build:** F-11 EFA-YOLO efficient edge detector (2409.12635 reports 1.4M params / 22.19 ms CPU,
  source-reported) + F-16 unsupervised IR optical-flow / flicker **physics feature** (1909.12937 reports
  95.39% frame-level, no labels, source-reported).
- **Precondition:** Step 1 — the tooling + benchmark + baselines exist, so a cross-camera "real win" is
  measurable.
- **Admitting gate:** **G2** real-win rule (F-11: keep only if cross-**camera** mAP gain > seed variance
  vs the current backbone; F-16: keep only if it adds signal over RGB-only on cross-site video). F-16 as a
  *physics* feature also lives under the WS1a Class-A/B/C discipline whose correctness gate is **G1**
  (physics golden tests), with Class-C novel flicker/ND terms **default-OFF with an A/B fallback**
  (`_CANON §4`, R20).
- **Honest dependency:** cross-camera data from Step 1; GPU time within the Kaggle budget
  (single-GPU retrain, `FEATURES.md` F-11). `[LIKELY]` (per `FINAL_REPORT §4`) that a compact edge
  detector cuts false alarms at acceptable latency — **not yet validated by us**. **Known risk
  (pre-registered):** micro-architecture mAP gains "often shrink cross-camera (single-split overfit)".

### Step 3 — Temporal event validation
- **Build:** F-12 temporal multi-frame event validation (confidence-weighted voting + cascade filter;
  2607.03131 reports FA 52%→4%, <100 ms/frame, source-reported).
- **Precondition:** Step 2 — a detector exists to post-process.
- **Admitting gate:** **G2** cross-site rule: keep only if the false-alarm reduction holds **cross-site at
  matched sensitivity** and **does not raise the missed-event rate** (`FEATURES.md` F-12; SOTA-targets
  table `FINAL_REPORT §11`).
- **Honest dependency:** a framerate/latency-to-alert tradeoff must be measured (the confirmation window
  adds latency — `DEPLOYMENT/pilot_design.md §2` counts "the F-12 confirmation-window cost"). `[LIKELY]`.

### Step 4 — Calibrated fusion + conformal-under-shift + drift monitor
- **Build:** P14 calibrated meta-fusion (GMF: stacking + bounded residual + conformal, re-calibrated per
  availability) + F-13 WCPS conformal-under-shift (2404.15018 WCPS; split-CP collapses 90%→65.3%,
  source-reported) + F-14 label-free drift/calibration monitor (2103.00903 STUDD; 2510.25573
  CUSUM-calibration).
- **Precondition:** Steps 1–3 give calibrated member models whose outputs can be fused and monitored.
- **Admitting gate:** **G3** (single `decide()` function; realizable+total shield; measured conformal
  coverage near nominal on a drifting holdout; anomaly radius bounded away from zero) **and G4** (meta-head
  coefficients stable under resampling; degraded-modality down-weighting; GMF never lowers the shield
  floor). The canonical decision rule is `level = max(conformal_level(risk, p*), shield_floor)`,
  **p\* = C_FA/(C_FA+C_miss) ≈ 0.0476** (`_CANON §4`).
- **Honest dependency:** `[CONFIRMED by sources]` that calibrated members ≠ calibrated ensemble
  (2101.05397) and vanilla split-CP collapses under moderate shift (2604.22787) — so the fused output
  must be **re-calibrated per availability** (`FINAL_REPORT §1 WS1b`). **Do NOT claim 1−α coverage
  cross-site without reweighting** (`FEATURES.md` F-13 risk; conformal-under-drift is a known-hard problem,
  §5.3 below). `[HYPOTHESIS]` that the specific GMF composition wins cross-site.

### Step 5 — IoT node + drift correction + prototype
- **Build:** F-15 IoT GP drift correction + uncertainty-driven recalibration scheduling (2506.09186 reports
  MSE −up to 90%, source-reported; 1707.03682 PRNet blind calib) on the P6/P13 physical prototype
  (Node A "Slope Sentinel" ≈ ₹1,930 [EST]; Node B "River Eye" ≈ ₹1,980 [EST]; `_CANON §8`,
  `TRINETRA_Workstreams.md` WS5).
- **Precondition:** the two nodes are re-spec'd (compliant SX1262 radio, tiered edge/cloud compute) per
  WS5; prices are live-verified.
- **Admitting gate:** **G5** (both node totals ≤ ₹2,000 **after price-verification**; every model assigned
  to a hardware-feasible tier with a stated compute/energy budget; a single faulty node cannot trigger RED
  unaided; LoRa band = **865–867 MHz** / IN865–867, SX1262).
- **Honest dependency:** **the ≤₹2000 BOM is NOT yet enforceable** — all ₹ figures are `[EST]`, suppliers
  returned HTTP 403 to automated fetch, so no price was independently confirmed; the price-verification
  gate (re-check each line item against ≥2 live Indian suppliers) is a mandatory deliverable *before any
  order* (`_CANON §8`, `TRINETRA_Workstreams.md` price-verification gate, `FINAL_REPORT §8`). On-device
  latency/RAM/current + radio range + final price are OPEN and require **physical measurement**
  (`FINAL_REPORT §8`, `§15.5`). F-15 risk: blind/neighbour calibration fails on sparse/isolated nodes.
  `[LIKELY]` for GP drift correction (source-reported).

### Step 6 — Robustness red-team
- **Build:** P16 robustness program — cross-sensor corroboration (the most transferable defense),
  uncertainty-entropy as an alert gate (confident-while-wrong 2610.08810), honest worst-case reporting;
  plus the WS6 integrity fixes (remove the key-exfiltrating proxy `#12`; CAP/SACHET signing; EO
  future-information-leak audit `#7`).
- **Precondition:** Steps 1–5 give the models, fusion and nodes that are the red-team's targets.
- **Admitting gate:** **G6** (no credential leaves the official endpoint; alert path works offline;
  feature-timestamp audit passes) — this gate *blocks the field pilot*. Robustness evidence also feeds the
  pilot's "evidence required before any automated public alert" bar (`DEPLOYMENT/pilot_design.md §6`).
- **Honest dependency:** `[CONFIRMED by sources]` that single-model hardening is benchmark-local while
  cross-sensor corroboration transfers (`FINAL_REPORT §1 WS6`, `§7`); certified robustness is a small-scale
  lower bound (1910.14655). Red-teaming is **continuous** because defenses and evasions co-evolve
  (2003.01279, deepfake context). `[LIKELY]` that corroboration bounds a single bad/attacked source.

### Step 7 — Anomaly + advisory RL (after the evac env is built)
- **Build:** WS8 anomaly heads (forecast-residual + Deep-SVDD, collapse-prevented) under the **STRICT
  protocol** (`FINAL_REPORT §3`: must beat persistence/general baseline; leakage control; report under
  shift; advisory input to fusion, never a standalone alert) + WS5 **advisory** offline-RL alarm policy
  (ranked options to a human dispatcher, never actuation; must BEAT strong non-RL baselines, e.g. MILP
  2602.14676).
- **Precondition:** **the disaster-evacuation RL environment must be built first** — there is **no
  off-the-shelf disaster-evac env** (`FINAL_REPORT §1 WS5`, `§15.8`; a declared BUILD GAP, §4.2 below).
- **Admitting gate:** **G2** (strict anomaly/RL valuation — honest OPE: select by BVFT 2110.14000,
  risk-evaluate by SCOPE-RL CVaR@5% 2311.18206, deploy only if the OPE lower bound ≥ rule baseline;
  `TRINETRA_Workstreams.md` WS2 task 4) and the RL safety shield from **G3**.
- **Honest dependency:** `[CONFIRMED by sources]` that naive RL underperforms and RL beats baselines only
  sometimes (2509.19972) → RL must beat MILP/non-RL and stay advisory. The evac env, OPE harness, and ≥100
  seeds (RB-13 policy) are prerequisites. `[HYPOTHESIS]` for every RL/anomaly skill claim until the env is
  built and the OPE gate passes.

### Step 8 — India shadow → advisory pilot
- **Build:** the staged pilot in `DEPLOYMENT/pilot_design.md`: STAGE 0 offline replay → STAGE 1 **SHADOW**
  (observe + log, trigger nothing) → STAGE 2 **ADVISORY** (human decides). STAGE 3 (beyond advisory) is
  explicitly **out of scope** of this program.
- **Precondition:** all prior steps + their gates; independent **ethics-review approval** before Stage 1
  (`DEPLOYMENT/pilot_design.md §4`).
- **Admitting gate:** the whole gate stack G1–G7, plus pre-registered pilot metrics (false-alarms/day,
  time-to-detection, missed-event rate + its uncertainty, calibration/PICP, operator accuracy) with
  stopping/rollback rules (`FINAL_REPORT §12`, `DEPLOYMENT/pilot_design.md §2–3`).
- **Honest dependency:** India regulatory / LoRa-band legality / who-may-originate-official-alerts items
  are **all `[UNVERIFIED]` search leads** requiring official-source + qualified-professional verification
  (`DEPLOYMENT/standards_and_regulation.md`, §4.4 below). **`[INFEASIBLE]` now:** autonomous public
  alerting without certification/authority (`_CANON §6`). The pilot's own honesty note:
  *"this bar is NOT met by any research-phase output"* (`DEPLOYMENT/pilot_design.md §6`).

---

## 23.2 Phased roadmap table

All statuses are **planned** — nothing below is in progress or done. Gate IDs are the internal-WS gates of
`TRINETRA_Workstreams.md`; "blocking dependency" is the honest precondition that cannot be shortcut.

| Phase | Goal | Deliverable | Gate | Blocking dependency | Status |
|-------|------|-------------|------|---------------------|--------|
| P-0 Tooling & benchmark | Make every number falsifiable | F-17 tooling + "real-win" LMEM gate; C-05 leakage-controlled CCTV benchmark + datasheets; spatial-CV harness + GB/3-rule-tree/persistence baselines | **G2** (admission) + **G7** (dataset/novelty/Kaggle) | Datasets collected + **licenses verified** (all `[D]`, none selected); datacube size corrected (WS7 #10) | planned |
| P-1 Edge detect + physics | Compact cross-camera CCTV detector | F-11 EFA-YOLO retrain; F-16 IR optical-flow/flicker physics feature | **G2** real-win rule; **G1** for F-16 physics-class fallback | P-0 benchmark; GPU budget; Class-C terms default-OFF | planned |
| P-2 Temporal validation | Cut false alarms without new misses | F-12 multi-frame event validation post-processor | **G2** cross-site rule | A detector (P-1); latency-to-alert measurement | planned |
| P-3 Fusion + calibration | Calibrated, shielded fused decision | P14 GMF (bounded-residual + conformal, re-cal per availability); F-13 WCPS; F-14 drift monitor | **G3** (decision fn + shield + coverage) + **G4** (fusion stability) | Calibrated members (P-1/P-2); density-ratio estimation; **no 1−α claim cross-site without reweighting** | planned |
| P-4 IoT prototype | Offline sensing + drift handling on cheap HW | F-15 GP drift correction; Node A/Node B physical prototype; tiered edge/cloud compute | **G5** (≤₹2000 + tiered feasibility + fault discrimination) | **Live-verified BOM** (prices `[EST]`, 403s); physical latency/RAM/current/range measurement; **India LoRa-band legality** | planned |
| P-5 Robustness red-team | Transferable defense + integrity | P16 cross-sensor corroboration; entropy alert gate; WS6 proxy removal + CAP signing + EO-leak audit | **G6** (no key leak + offline alert path) | P-1..P-4 targets exist; red-teaming is continuous | planned |
| P-6 Anomaly + advisory RL | Advisory ranked options + anomaly channel | WS8 forecast-residual + Deep-SVDD heads (strict protocol); WS5 offline-RL alarm policy + OPE gate + shield | **G2** (honest OPE/anomaly valuation) + **G3** (shield) | **Disaster-evac RL env must be built first** (no off-the-shelf env); ≥100 seeds; MILP baseline | planned |
| P-7 India shadow→advisory pilot | Supervised real-world evaluation | Stage 0 replay → Stage 1 SHADOW → Stage 2 ADVISORY; pre-registered metrics + stopping/rollback | G1–G7 + pilot gates | **Regulatory/alerting-authority verification; ethics approval; stakeholder hosting**; `[INFEASIBLE]` to go autonomous | planned |

---

## 23.3 Feature waves

Source: `FEATURES.md` (P17 formal admission, 2026-10-10) and `FINAL_REPORT §9`. **All P17 features are
weak(ABS)-evidence, source-reported, paper IDs subagent-reported and NOT re-fetched; no feature is
described as "working"** (`FEATURES.md §P17`). Every feature carries a **pre-registered cross-camera/
cross-site decision rule** gated by the inferential-reproducibility test (2302.04054).

### Wave 1 — approved-for-build-plan (F-11..F-17)
High evidence-for-ABS / low cost; approved for a **build plan** (pending P18 specs), not built.

| ID | Feature | WS | Pre-registered cross-camera/cross-site decision rule | Risk (honest) |
|----|---------|----|------------------------------------------------------|---------------|
| F-11 | EFA-YOLO efficient edge detector (attention-lite + depthwise); 2409.12635 (1.4M params, 22.19 ms CPU, src-reported) | WS4 | Keep only if cross-**camera** mAP gain > seed variance vs current backbone | micro-arch mAP gains often shrink cross-camera (single-split overfit) |
| F-12 | Temporal multi-frame event validation (confidence-weighted voting + cascade); 2607.03131 (FA 52%→4%, <100 ms/frame, src-reported) | WS4/WS3 | Keep if FA reduction holds **cross-site at matched sensitivity**; must not raise missed-event rate | framerate / latency-to-alert tradeoff |
| F-13 | Post-hoc conformal under covariate shift (WCPS); 2404.15018; 2402.07307; 2501.12749 | WS1b/WS6 | Keep if coverage stays valid on cross-site split | exchangeability breaks under shift unless reweighted — **no guarantee claim cross-site without weighting** |
| F-14 | Label-free drift + calibration monitor (student-teacher + CUSUM); 2103.00903; 2510.25573 | WS6 | Keep if detection delay/false-alarm beats a fixed-threshold monitor on replayed drift | ADVISORY only (Rule 19) |
| F-15 | IoT GP drift correction + uncertainty-driven calibration scheduling; 2506.09186 (MSE −up to 90%, src-reported); 1707.03682 | WS7 | Keep if post-correction error < seed-variance improvement on held-out sensor-days | blind/neighbour calibration fails on sparse/isolated nodes |
| F-16 | Unsupervised IR optical-flow / flicker physics feature (label-free cold-start); 1909.12937 (95.39% frame, no labels, src-reported) | WS1a/WS4 | Keep if it adds signal over RGB-only on cross-site video | sensitive to framerate/codec/PTZ motion |
| F-17 | Experiment tooling: provenance (dagger 2006.07484) + inferential-reproducibility test (LMEM+GLRT 2302.04054) | tooling | **ENABLER** — the "real-win" gate every other feature passes through | no model impact |

### Wave 2 — parked / pending (F-18..F-22)
Medium evidence / moderate cost; **not specced** (`FINAL_REPORT §9`). Status `proposed`. Each entry gives
the reason it is parked and the condition that would **un-park** it.

| ID | Feature (WS) | Why parked | What would un-park it |
|----|--------------|------------|-----------------------|
| F-18 | STCNet two-stream spatio-temporal smoke; 2011.04863 (+6.2% RISE, src-reported) (WS4) | Two-stream latency/memory on edge; temporal cue is codec-sensitive | Evidence it cuts steam/cloud FPs cross-site beyond its cost on OUR edge budget |
| F-19 | MobileViT-S knowledge distillation; 2502.20979 (+0.44–2.00% compact, src-reported) (WS4) | Teacher-pipeline cost; distillation can overfit teacher's dataset bias | Student matches teacher within variance **cross-camera** |
| F-20 | WISE weakly-supervised smoke localization; 2609.18227 (0.12M params, tile-F1 0.964, src-reported) (WS4) | Weak-label pipeline is domain-specific (satellite/onboard) | Pixel-localization transfers cross-site |
| F-21 | Semi-supervised video fire (FireMatch 2311.05168 / SIAVC 2405.14506) (WS4) | Confirmation bias can entrench source-domain errors | Pseudo-labels help on **NEW cameras**, not just source |
| F-22 | Conformal prediction sets for OPERATOR decision-support UI; 2401.13744 (RCT raises operator accuracy, src-reported) (WS3) | Needs a human-factors evaluation; advisory-UI only (Rule 19) | Human-factors eval shows improved dispatcher accuracy (ties the Stage-2 advisory gate) |

### Wave 3 — parked / speculative (F-23..F-26)
Speculative / high setup cost; "revisit only if budget remains" (`FINAL_REPORT §9`). Status `proposed`.

| ID | Feature (WS) | Why parked | What would un-park it |
|----|--------------|------------|-----------------------|
| F-23 | SmokeyNet multimodal camera+weather fusion; 2212.14143 (better time-to-detection, src-reported) (WS4/WS1b) | Pays off only where a co-located weather feed exists; else reverts to single-stream | A deployment site with a live weather feed |
| F-24 | Obscured-flame 3D-conv temporal segmentation; 2307.00104 (Dice 85.88%, "~100%" video) (WS4) | **OVERFIT RED FLAG** — "~100% video classification" treated as an overfit candidate, NOT evidence (`FEATURES.md §Rejected`) | A leakage-controlled cross-split re-evaluation that survives the real-win gate |
| F-25 | Thermal/IR fusion branch for low-visibility; 2307.04223 (mAP@0.5 95% Jetson Nano, src-reported) (WS4/WS7) | IR **hardware + calibration rig** needed; likely exceeds the ₹2000 prototype cap | IR hardware availability **and** staying within the ≤₹2000 node budget |
| F-26 | Two-stage UAV adaptive compression + policy early-exit; 2508.16739 (large compute cut, src-reported) (WS4) | Needs an RL-style policy net + orchestration (high cost) | Core detector validated first; then an RL-policy budget |

**Hard rule across all waves (`FINAL_REPORT §9`):** no feature may consume the GPU reserve / hardware
contingency (`KAGGLE_BUDGET §2`: ≥4.5 GPU-h/week reserve). Nothing is "rejected" at P17 — Wave-3 items are
**parked** (budget/hardware/overfit-risk), and overfit red flags (2307.00104; any >98% single-split
headline) are logged as overfit candidates, not evidence (`FEATURES.md §67–70`).

---

## 23.4 Build gaps that must be filled first

These are the OPEN items from `FINAL_REPORT §15` and `TRINETRA_Workstreams.md` gates. Until they close, the
corresponding build steps cannot honestly start.

### 4.1 Datasets collected + licenses verified
All discovered datasets are STATUS=candidate `[D]` (D-numbered through D112), license INDICATIVE/UNVERIFIED;
**no dataset with STATUS=selected is paid, because none is selected** (`FINAL_REPORT §5`). Portal access +
license verification is an OPEN backlog item (`FINAL_REPORT §15.2`): ISRO/NRSC + government portals;
candidate registry entries (GLOFNet 2510.10546; HMAGLOFDB 589 outbursts via 2608.12422; Sentinel-1/-2, GPM
IMERG, SMAP, ERA5-Land free-but-confirm; Bhuvan/NRSC landslide inventory — *verify license*)
(`TRINETRA_Workstreams.md` WS7 task 2). **Honest timeline:** data access + license clearance is a
days-to-weeks dependency and is the precondition for Step 1 / Phase P-0. `[HYPOTHESIS]` that C-05 is
buildable as specified until data is in hand.

### 4.2 Disaster-evacuation RL environment (no off-the-shelf env)
`FINAL_REPORT §1 WS5` and `§15.8`: **"Build the disaster-evacuation RL environment (no off-the-shelf env
exists — BUILD GAP)."** This blocks Step 7 (anomaly + advisory RL) entirely. The env must support the honest
OPE protocol (BVFT selection, SCOPE-RL CVaR@5% risk, one-step offline baseline, feedback-aware OPE 2312.01530)
and the RB-13 rigor policy (≥100 seeds, report tail + dispersion, beat trivial baselines). `[HYPOTHESIS]` on
any RL skill until the env exists and the OPE lower bound ≥ rule baseline.

### 4.3 Live-verified ≤₹2000 BOM
Every ₹ figure is `[EST]`; Robu.in / Amazon.in returned **HTTP 403** to automated fetch, so no price was
independently confirmed (`TRINETRA_Workstreams.md` price-verification gate; `_CANON §8`). The ≤₹2000 gate
(**C2**) is **NOT yet enforceable**. Procurement rule: no node is ordered until each line item is re-checked
against **≥2 live Indian suppliers** and the per-node total is re-confirmed ≤ ₹2,000 (Node A ≈ ₹1,930 [EST];
Node B ≈ ₹1,980 [EST]). On-device latency / RAM / current / radio-range and the final price need **physical
measurement** (`FINAL_REPORT §8`, `§15.5`). Blocks Step 5 / G5.

### 4.4 India regulatory / LoRa-band / alerting-authority verification
All items are `[UNVERIFIED]` search leads for official-source verification + qualified legal/standards review
— **not legal advice** (`DEPLOYMENT/standards_and_regulation.md`; `FINAL_REPORT §12`). Specifically: fire-
device certification; **radio/LoRa-band legality** (planned IN865–867 MHz / SX1262, `_CANON §8` — confirm it
is legal and within power/duty-cycle limits); **who may originate official alerts** (a private/academic party
*likely MAY NOT* originate official alerts); data-protection in video; surveillance/CCTV rules; social-media
ToS; electronics certification. Blocks the pilot (Step 8) and any alerting integration. **`[INFEASIBLE]`
now:** autonomous public alerting without certification/authority (`_CANON §6`). **`[INFEASIBLE]`:**
IP-address-based alerting for life-safety targeting — not carried (`_CANON §6`, `FINAL_REPORT §4`).

### 4.5 Independent re-resolution of subagent-reported arXiv IDs
The ledger holds **631 unique arXiv IDs** (FINAL_REPORT snapshot; the live ledger has grown to ~**775** — see `_CANON §7`), but *most are subagent-reported and NOT independently re-fetched*
(web_search had no API key; arXiv re-resolution only via throttled web_fetch) — a **disclosed residual risk**
(`FINAL_REPORT §5`, `§15.9`, `_CANON §7`). Before any paper's reported number is used to justify a build
hyperparameter or claim, its ID and figure must be independently re-resolved against arXiv. Full-text reads
are still needed for exact Wave-1 hyperparameters (2503.07371, 2607.03131, 2610.09208, 2406.17813,
2406.17488 — `FINAL_REPORT §15.7`). This gap touches **every** source-reported number in this chapter.

---

## 23.5 Research directions (literature-backed, [HYPOTHESIS])

These are open research threads the sources name but the program did not pursue to depth. All `[HYPOTHESIS]`.

### 5.1 SAR foundation-model trade study (P7 parked items)
`HANDOFF/BUILD_HANDOFF.md` (P3) records the **SAR-first encoder stance (CR-01)**: SAR beats optical in two
independent all-weather votes (SAR2Agri 2608.11142 +15.3 pt; GLOF SAR seg 2512.24117 IoU 0.9130,
source-reported). The P7 trade study must evaluate named SAR-specific contenders **on OUR task** — TerraMind,
Copernicus-FM, SAR-JEPA, SARMAE, SAR-W-MixMAE, SAMBA (Mamba, linear-cost → edge budget), OceanSAR — selected
by on-our-task probing + CKA shift budget, **not leaderboard**. Carried as an open item (`§P3`:
"SAR-FM trade (P7)"). `[HYPOTHESIS]` that a SAR encoder beats the frozen Prithvi-EO-2.0 (2412.02732) /
Galileo (2502.09356) baseline under our spatial-CV protocol.

### 5.2 Zero-shot complement maturation (P14Z)
Zero-shot / open-vocab detection is admitted **only** as a calibrated LOW-WEIGHT complement into GMF +
conformal + shield, never an autonomous trigger (D-011; `FINAL_REPORT §1 WS4`; `BUILD_HANDOFF §P3`:
P14Z registered). Sources favour trained over zero-shot in the fire domain (2504.13231, 2610.10946,
2607.07951). Research direction: mature the low-weight ZS complement and the leakage-controlled CCTV
zero-shot benchmark **C-05** (contribution C-05, `FINAL_REPORT §13`). `[HYPOTHESIS]`.

### 5.3 Better conformal-under-drift
`[CONFIRMED by sources]` that vanilla split-CP collapses under moderate shift (2604.22787; 90%→65.3%),
is valid only with reweighting (2404.15018 WCPS), and concept drift voids covariate-shift bounds
(`FINAL_REPORT §7`). Open thread: adaptive conformal (2202.07282 ACI/AgACI, 2303.12783 HopCPT, 2406.05405
missingness; `TRINETRA_Workstreams.md` WS3 task 4) with measured marginal **and per-zone** coverage, claiming
*risk-control* not a fixed 90%. `[HYPOTHESIS]` that any method restores near-nominal coverage on our
drifting Himalayan holdout.

### 5.4 Feedback-aware OPE
`TRINETRA_Workstreams.md` WS2 task 5 (#23) + `FINAL_REPORT §4` LIKELY cluster: model evacuation/alarm/
maintenance feedback in off-policy evaluation (2312.01530) so the RL alarm policy is valued under the
feedback its own alerts induce. Prerequisite: the evac env (§4.2). `[HYPOTHESIS]`.

### 5.5 Cross-sensor corroboration expansion
`[CONFIRMED by sources]` that cross-sensor corroboration is the most transferable robustness defense and
bounds a single bad/attacked source (`FINAL_REPORT §1 WS6`, `§4` LIKELY). Research direction: expand
corroboration across modalities with per-modality reliability gating (2603.01511 MERA, `Workstreams` WS4
task 2) and Neyman-Pearson fault-vs-event + cross-node spatial consistency before a single node drives a
shield override (`Workstreams` WS5 task 3; 1203.0541). `[HYPOTHESIS]` on the quantitative bound.

---

## 23.6 "DONE criteria" — what each gate must show

Nothing may be claimed until its gate passes. The project-wide **ADMISSION GATE is G2**, which *blocks
publication / any performance claim* (`TRINETRA_Workstreams.md` G2) and corresponds to the evaluation
admission gate documented in **chapter 12** (`docs/12_evaluation_and_results.md`; `_CANON §9` maps chapter 12
to `trinetra/src/trinetra/eval/*` + `TRINETRA_Workstreams.md` G2). Enforced in code by **ReportGuard / R16**:
no performance claim before the eval admission gate (`_CANON §5`).

| Gate | WS | DONE criterion (what it must SHOW) | What it blocks until shown |
|------|----|------------------------------------|----------------------------|
| **G1** | WS1 physics | All golden-case tests pass (saturated limit `S_e→1 ⇒ FS` saturated form; `β→0, t→∞` ⇒ steady-state Iverson; α=2 ⇒ 1/v linear); FS monotonic in suction; no module uses the old buggy equations | Downstream physics use |
| **G2** (ADMISSION) | WS2 eval | Every performance claim appears under **both** random-CV and spatial-CV, keyed to the spatial-CV column, with GB + 3-rule-tree + persistence baselines in the same table; any claim not beating baseline under spatial-CV is withdrawn | **Publication / any performance claim** (ties chapter 12 admission gate; R16/ReportGuard) |
| **G3** | WS3 decision | Single `decide()` function; shield proven **total + realizable**; measured conformal coverage near nominal on a **drifting** holdout; anomaly radius bounded away from zero | Deployment |
| **G4** | WS4 fusion | Meta-head coefficients stable under resampling (sign-flip ≈ 0); degraded-modality down-weighting demonstrated; GMF never lowers the shield floor | GMF deployment |
| **G5** | WS5 IoT | Both node totals ≤ ₹2,000 **after live price-verification**; every model on a hardware-feasible tier with a stated compute/energy budget; a single faulty node cannot trigger RED unaided; LoRa = 865–867 MHz | Hardware order |
| **G6** | WS6 comms | No credential leaves the official endpoint; alert path works with the cloud unreachable; feature-timestamp (EO-leak) audit passes | Field pilot |
| **G7** | WS7 data/compute | Datacube size corrected; dataset licenses checked; I–D constants sourced or replaced by a fitted distribution; novelty claim matches real prior art; Kaggle plan fits ≤30 GPU-h/week with ≥15% reserve | Submission |

**Pilot-level DONE bar (`DEPLOYMENT/pilot_design.md §6`):** independent certification + official approval;
sustained Stage-1/2 performance across sites and seasons with honest statistics (IQM + CIs, 2108.13264);
robustness evidence (P16); demonstrated fail-safe to "uncertain/offline", never a false all-clear.
**Honest note carried verbatim: this bar is NOT met by any research-phase output.**

---

## 23.7 Immediate next steps for a new engineer

Order and wording from `FINAL_REPORT.md §15` ("NEXT STEPS FOR YOU") + `_CANON`. Do these **before** writing
any build code:

1. **Order the prototype parts** — but first run the **price-verification gate** (re-check each BOM line
   against ≥2 live Indian suppliers; confirm per-node total ≤ ₹2,000). Prices are `[EST]` only; do not
   assume G5 is met (`§4.3`).
2. **Request dataset access + verify licenses** — ISRO/NRSC + government portals; all datasets are `[D]`
   candidates with unverified licenses; none is selected (`§4.1`). This unblocks Step 1 / Phase P-0.
3. **Consult the experts/bodies in `DEPLOYMENT/stakeholders_and_partners.md`** — via proper institutional
   channels only (the program contacted no one): fire services (shadow-mode hosting), disaster-management
   authorities (approval path), met/remote-sensing agencies (data + co-validation), universities (physics
   Class A/B/C review + red-teaming), legal/data-protection professionals.
4. **Verify the regulatory items with a qualified professional** — fire-device certification, LoRa-band
   legality (IN865–867 MHz), who-may-originate-official-alerts, data-protection, CCTV/surveillance rules;
   all `[UNVERIFIED]` (`§4.4`; `DEPLOYMENT/standards_and_regulation.md`). This is **not legal advice**.
5. **Independently re-resolve the subagent-reported arXiv IDs** you intend to rely on, and full-text-read the
   Wave-1 hyperparameter papers (2503.07371, 2607.03131, 2610.09208, 2406.17813, 2406.17488) (`§4.5`).
6. **Build the disaster-evacuation RL environment** before attempting Step 7 — no off-the-shelf env exists
   (`§4.2`).
7. **Request the build prompt via `HANDOFF/BUILD_HANDOFF.md`** — the build happens later with a separate
   prompt; the handoff package (per-WS methods, datasets, interfaces, eval protocol, acceptance criteria,
   hyperparameter defaults, GPU-h estimates, pitfalls, open decisions) is kept current there. Also read
   `HANDOFF/OPEN_DECISIONS.md` and `HANDOFF/RISKS_FOR_BUILD.md`.

Slides / hackathon / paper can be produced afterward from `FINAL_REPORT.md` + the handoff (`§15`).

---

*Everything above is future work. No model has been trained, no dataset downloaded, no node ordered, no
pilot run, no regulatory fact confirmed. The only measured facts are the 128 numpy tests + 6 CI gates
(`_CANON §2`). Advisory, human-in-the-loop, fail-safe to "uncertain/offline", never an autonomous public
alert (R19).*
