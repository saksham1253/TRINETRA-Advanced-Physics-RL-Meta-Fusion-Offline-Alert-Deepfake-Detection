# FINAL_REPORT.md — TRINETRA / HIMKAVACH research program

RESEARCH-ONLY FINAL REPORT (MASTER_PROMPT P20). Nothing was built, trained, or measured. Every performance
number anywhere is SOURCE-REPORTED from other papers on their own data (Rule 16) — NONE is a result of this
system. Every India / standards / regulation / cost fact is an [UNVERIFIED] search lead for official-source
verification + qualified professional review; nothing here is legal advice. Life-safety domain: all designs
are ADVISORY, human-in-the-loop, fail-safe to "uncertain/offline", never autonomous public alerting (Rule 19).

Scope (verbatim): disaster / fire detection and response, CCTV, physics-informed models, RL, deepfake
handling, offline alerting, IoT, anomaly detection. Session date 2026-10-10.

---
## 1. What was researched and decided, per workstream (key evidence)

- WS1a PHYSICS (fire), P7 — a small admitted physics set as features/priors/consistency-checks/simulators,
  NOT a deployed solver. Full fire-PINN REJECTED for on-device deployment (stiffness, spectral bias,
  non-identifiability); physics enters as soft features with fallback to the Class-A parent. Evidence: P7
  derivations B-01/B-02/B-05/B-06.
- WS1b PHYSICS-GEO + META-FUSION, P7G/P14 — gated meta-fusion (stacking + bounded residual + conformal);
  binding caution: calibrated members ≠ calibrated ensemble (2101.05397), missing inputs break calibration
  (2605.12517) → the fused output is RE-CALIBRATED per availability.
- WS2 DEEPFAKE, P11 — forensic/provenance detectors are DEFENSIVE-ONLY; defenses + evasions co-evolve
  (2003.01279) → continuous red-teaming; social-media evidence is advisory + corroborated.
- WS3 ALERTING, P12 — offline-first store-carry-forward (DTN); cell-broadcast is spoofable (2604.24404) →
  authenticate; no origination of official alerts without authority.
- WS4 CCTV, P8 (+ zero-shot complement P14Z) — trained detector PRIMARY; zero-shot admitted ONLY as a
  calibrated LOW-WEIGHT complement (D-011; trained>ZS in fire domain: 2504.13231, 2610.10946, 2607.07951).
- WS5 RL, P15 — RL is ADVISORY (ranked options to a human dispatcher, never actuation) and must BEAT strong
  non-RL baselines (MILP 2602.14676); offline-first, safety/constraint prerequisite; no off-the-shelf
  disaster-evac env (BUILD GAP).
- WS6 ROBUSTNESS, P16 — cross-sensor corroboration is the most transferable defense; single-model hardening is
  benchmark-local; uncertainty-entropy as an alert gate (confident-while-wrong 2610.08810); spatial-block, not
  random, CV.
- WS7 IoT, P6/P13 — ≤INR 2000 offline node; drift correction + scheduled recalibration; SAFETY.md governs.
- WS8 ANOMALY, P9/P10 — forecast-residual + Deep-SVDD anomaly heads under a STRICT protocol (below); must beat
  persistence/general baselines.

---
## 2. Physics models — final N (Rule 20 classes + lineage)

Source: ws1_physics/model_set_decision.md.
- LAYER 1 (Class A, established, verified-source): N = 12 (EF-01…EF-12). Dual plume parents EF-03 Heskestad +
  EF-04 McCaffrey both kept for a build-phase ablation.
- LAYER 2 (Class B, admitted, derived + validation-gated, SOFT feature/prior with parent fallback): N = 4 —
  B-01 camera apparent flame height through smoke (parents EF-01/EF-07/EF-09); B-02 dimensionless plume-temp
  prior (parent EF-03); B-05 aliasing-aware flicker band (parent EF-08); B-06 sensor-response-corrected signal
  (parents EF-05/EF-10/EF-03, highest-priority).
- LAYER 2 (Class C, DOCUMENTATION-ONLY, hypotheses never results): N = 2 — C-01 level-set front ∘ Rothermel
  (simulator only); C-02 full coupled forward camera model (synthetic-data simulator only).
- REJECTED: full fire-PINN as a deployed solver; pyrolysis/Arrhenius as a live model (parked).
- Total modelled relations tracked = 18. Every Class B/C item carries a validation roadmap vs specific
  published data + mandatory fire-science expert review; NONE is described as established or validated.

---
## 3. Anomaly-detection scope, design & strict protocol

Scope (WS8): detect deviations in InSAR/sensor/video-derived signals as an advisory corroborating channel.
Design: forecast-residual anomaly + Deep-SVDD head (collapse-prevented). STRICT PROTOCOL: must beat a
persistence / general-purpose baseline; evaluate with leakage control (spatial-block / leave-one-incident-out,
2608.22293); report under distribution shift; anomaly scores are advisory inputs to fusion, never a standalone
alert. SSL encoders must beat a general ViT baseline before admission (F-01/F-02 decision rules).

---
## 4. Claim ledger — CONFIRMED / LIKELY / HYPOTHESIS / INFEASIBLE

- CONFIRMED (by sources, source-reported): offline-first is necessary (connectivity collapses, 2511.15710);
  random CV overstates skill (2608.22293); models stay confident while wrong under shift (2610.08810);
  calibrated members ≠ calibrated ensemble (2101.05397); cell-broadcast alerts are spoofable (2604.24404);
  vanilla split-CP coverage collapses under moderate shift (2604.22787); recalibration often less calibrated
  than reported (1909.10155).
- LIKELY (plausible, needs our validation): a compact edge detector + temporal event validation can cut false
  alarms at acceptable latency (2409.12635, 2607.03131); GP/blind drift correction improves cheap-sensor
  accuracy (2506.09186); cross-sensor corroboration bounds a single bad/attacked source (P16).
- HYPOTHESIS (unvalidated, ours): the Class-B physics features (B-01/B-02/B-05/B-06); calibrated low-weight
  zero-shot complement (D-011); the leakage-controlled CCTV zero-shot benchmark (C-05); India shadow→advisory
  pilot protocol.
- INFEASIBLE / NOT RECOMMENDED: **IP-address-based alerting** — VERDICT: INFEASIBLE for life-safety targeting.
  Consumer IP geolocation resolves to ISP/city granularity (often tens of km, CGNAT/VPN-corrupted), does not
  map to a premises, and cannot address a specific person at risk; using it to target or trigger alerts would
  be unreliable and unsafe. Not carried. (Public-IP exposure of any endpoint is instead a SECURITY concern →
  authenticated endpoints, P16.) Also INFEASIBLE now: full fire-PINN on-device solver; autonomous public
  alerting without certification/authority.

---
## 5. Literature counts

- UNIQUE arXiv IDs in the ledger: 631 (681 ID-bearing rows; 50 rows = 7.3% are legitimate cross-phase
  re-citations, logged in Audit #28, corrected in quota counts, no fabrication).
- FOUNDATION NEW papers verified across P1-P20 ≈ 436 (gross by phase tag). The **250-minimum IS MET** (exact:
  ~436 new; 631 unique total). Honest caveat: most IDs are subagent-reported and NOT independently re-fetched
  (web_search had no API key; arXiv re-resolution only via throttled web_fetch) — a disclosed residual risk.
- PER-PHASE QUOTA TABLE (NEW papers; min 15, P14Z min 10 — ALL MET; effective = after removing cross-phase
  repeats):

  | Phase | Raw | Effective | Phase | Raw | Effective |
  |-------|-----|-----------|-------|-----|-----------|
  | P2 | 18 | 18 | P12 | 20 | 20 |
  | P3 | 45 | 45 | P13 | 20 | 20 |
  | P4 | 18 | 18 | P14 | 22 | 22 |
  | P5 | 15 | 15 | P14Z | 16 | 16 |
  | P6 | 20 | 20 | P15 | 21 | ~20 |
  | P7 | 22 | 22 | P16 | 23 | 23 |
  | P7G | 17 | 17 | P17 | 22 | ~18 |
  | P8 | 16 | 16 | P18 | 21 | ~19 |
  | P9 | 19 | 19 | P19 | 25 | ~23 |
  | P10 | 18 | 18 | P20 | 18 | 18 |
  | P11 | 20 | 20 | | | |

- READ-DEPTH distribution: a running body-level DEEP full-text (FT) NEW total of 100 was built in the earlier
  phases; P13-P20 added ABS (abstract-level) BREADTH only (honest: these later phases are breadth, not depth).
  Labels used: FT / FT-PARTIAL / ABS / ABS-CANONICAL / FT-REF.
- NON-ARXIV sources: datasheets/standards/government reports were treated as NON-QUOTA and, per Rule 11, remain
  [UNVERIFIED] search leads for official verification (none independently confirmed in-program).
- DATASETS by cost: all discovered datasets are STATUS = candidate [D] (D-numbered through D112), license-
  INDICATIVE/UNVERIFIED; **no dataset with STATUS = selected is paid** (none is selected). Portal + license
  verification = OPEN backlog.

---
## 6. Audit results & corrections
28 reading/quality audits, all PASS within stated limits (analysis/11_reading_audit.md). Final P20 gates
(Audit #28): ledger duplicate-ID rate 7.3% (re-citations, corrected in quota, no fabrication); all phases meet
quota; 250-minimum met; traceability/consistency/safety/skeptical reviews pass; no Class B/C formula described
as established; every novelty = search claim; no Rule-16/18 violation. CORRECTION LOGGED: cross-phase repeat
citations do not count toward later-phase NEW quota (effective counts above).

---
## 7. Contradictions in the literature & handling
- "Fire-domain trained vs zero-shot": sources favour trained (2504.13231 etc.) → ZS admitted only as a
  calibrated low-weight complement (D-011).
- "Certified robustness vs empirical": certified methods are small-scale lower bounds (1910.14655) while
  empirical hardening is benchmark-local → rely on cross-sensor corroboration + honest worst-case reporting.
- "Conformal guarantees under shift": valid only with reweighting (2404.15018) and collapse otherwise
  (2604.22787) → never claim 1−α cross-site without weighting; concept drift voids covariate-shift bounds.
- "RL beats baselines": only sometimes; naive RL underperforms (2509.19972) → RL must beat MILP/non-RL and
  stay advisory.
All handled by taking the more conservative, life-safety-aligned position.

---
## 8. IoT plan
- Prototype node: target ≤ INR 2000 (P6 BOM staged AS-OF-P6; prices INDICATIVE, re-quote WITH DATES at build —
  OPEN). Final verified BOM total vs INR 2000 is NOT yet confirmed (price verification OPEN).
- Node architecture: low-cost MCU + tilt/moisture/piezo/rain (+ optional gas/IR), LoRa radio, battery/solar,
  offline store-carry-forward, on-node drift correction (F-15) + rate-of-rise/delta features (B-06), SAFETY.md
  governs; endpoints authenticated.
- What the prototype WILL show: feasibility of offline sensing + advisory signaling + drift handling on cheap
  hardware. What it will NOT show (honest): certified detection performance, real-world averted loss, radio-
  range/current/RAM/latency numbers (all require physical measurement — OPEN), India LoRa-band legality (OPEN).

---
## 9. Feature summary (P17/P18)
- SELECTED Wave-1 (approved-for-build-plan, specs in features/wave1_specs.md): F-11 EFA-YOLO edge detector
  (low cost); F-12 temporal event validation (very low); F-13 conformal-under-shift WCPS (low); F-14 label-free
  drift/calibration monitoring (very low); F-15 IoT GP drift correction (low-moderate); F-16 IR optical-flow
  physics feature (very low); F-17 tooling + inferential-reproducibility "real-win" gate (very low).
- WAVE-2 proposed (F-18..F-22) and WAVE-3 parked (F-23..F-26, incl. overfit-flagged 2307.00104 and
  budget/hardware-limited thermal-IR F-25) — not specced; revisit only if budget remains.
- Every feature carries a PRE-REGISTERED decision rule: keep only if improvement exceeds seed/trial variance on
  a HELD-OUT CROSS-CAMERA/CROSS-SITE split, confirmed by the significance gate (2302.04054); a benchmark-local
  win that hurts cross-camera is NOT a win. No feature may consume the GPU reserve / hardware contingency.

---
## 10. Planning-level Kaggle budget
Model training is scoped to a single-GPU Kaggle-class budget with a 15% GPU-hour reserve + hardware
contingency that features may NOT consume. No training was run (research-only). Exact hour accounting is a
build-phase item.

---
## 11. SOTA targets table (process targets — SOURCE-REPORTED references, NOT our results, Rule 16)
| Task | Reference SOTA (source-reported, their data) | Our PROCESS target |
|------|----------------------------------------------|--------------------|
| Edge CCTV detection | EFA-YOLO 1.4M params / 22.19 ms CPU; HGO-YOLO 87.4% mAP CPU | match/approach under OUR cross-camera protocol, meet edge latency ceiling; measure smoke-specific recall |
| False-alarm reduction | temporal event validation FA 52%→4% | reduce FA cross-site at matched sensitivity without raising missed-event rate or missing alert deadline |
| Calibration under shift | WCPS valid coverage; split-CP collapses 90%→65.3% | realized PICP ≈ nominal on cross-site split WITH weighting + reliability flags |
| IoT drift correction | GP −up to 90% MSE | post-correction error gain > seed variance on held-out sensor-days |
| Fusion | super-learner/stacking gains | fused beats best single by > seed variance, calibrated, FA ≤ best single |
All targets are "match/approach under our protocol with protocol differences spelled out", never "we achieve".

---
## 12. India deployment pathway, regulatory findings, pilot
- Pathway (DEPLOYMENT/): offline-first + multilingual + uncertainty-gated + spatial-block validation +
  complementary-until-certified; free-data advisory pipelines; private-CCTV consent/data-protection path.
- Regulatory findings: ALL [UNVERIFIED] search leads flagged for qualified legal/standards review (fire-device
  certification, radio/LoRa-band legality, who-may-originate official alerts, data-protection in video,
  surveillance/CCTV rules, social-media ToS, electronics certification). NOT legal advice.
- Pilot: STAGE 0 offline replay → STAGE 1 SHADOW (observe/log, trigger nothing) → STAGE 2 ADVISORY (human
  decides); pre-registered metrics (false-alarms/day, time-to-detection, missed-event rate + uncertainty,
  calibration/PICP, operator accuracy), stopping/rollback rules, ethics approval; NO autonomous public alert.

---
## 13. Research contributions & publication plan
Proposed (unvalidated; novelty = search claim; DEPLOYMENT/research_contributions.md, publication_plan.md):
C-01 calibrated offline-first fusion; C-02 calibrated low-weight zero-shot complement; C-03 corroboration-first
robustness; C-04 India shadow→advisory pilot protocol; C-05 leakage-controlled CCTV zero-shot benchmark; plus
physics contributions by Class A/B/C with validation roadmaps + fire-science review. Publication order follows
evidence maturity (protocol/benchmark first; physics last, by class). Credibility = pre-registration, open
code/data, IQM+CIs (2108.13264), contamination disclosure (2608.29463), honest negatives.

---
## 14. Build handoff status & recommended build order
Status: every workstream has a research-level spec; the handoff is complete enough to write build prompts for
the Wave-1 features and the physics/anomaly/fusion stubs, with the OPEN gaps below to resolve first.
Recommended build order: (1) F-17 tooling + real-win gate and data/benchmark curation (C-05) with datasheets;
(2) F-11 edge detector + F-16 physics feature; (3) F-12 temporal validation; (4) P14 calibrated fusion + F-13
conformal-under-shift + F-14 drift monitor; (5) F-15 IoT node drift correction + P6/P13 prototype; (6) P16
robustness red-team; (7) WS8 anomaly + WS5 advisory RL (after the disaster-evac env is built); (8) India
shadow pilot. Each step gated by its pre-registered cross-camera/cross-site decision rule.

---
## 15. Everything uncertain, unfinished, or needing your input (OPEN BACKLOG)
1. Coefficient/claim verification (physics [coeff-verify]; all source-reported numbers).
2. Dataset portal access + LICENSE verification (all datasets [D], none selected; ISRO/NRSC + gov portals).
3. Expert review: fire-science (physics Class A/B/C), ML, safety, legal/standards, ethics, accessibility.
4. Own-data collection + the leakage-controlled CCTV benchmark (C-05).
5. On-device measurement: latency/RAM/current + radio range + final BOM price vs INR 2000 (re-quote w/ dates).
6. India LoRa-band legality + official regulatory/alerting path (NDMA / C-DOT-type) — official-source verify.
7. Full-text reads for exact Wave-1 hyperparameters (2503.07371, 2607.03131, 2610.09208, 2406.17813,
   2406.17488).
8. Build the disaster-evacuation RL environment (no off-the-shelf env exists — BUILD GAP).
9. Independent re-resolution of subagent-reported arXiv IDs (web_search outage residual risk).

NEXT STEPS FOR YOU: order prototype parts; request dataset access + verify licenses; consult the experts/bodies
in DEPLOYMENT/stakeholders_and_partners.md; verify the regulatory items with a qualified professional; then
request the build prompt via HANDOFF/BUILD_HANDOFF.md. Slides / hackathon / paper can be produced afterward
from this report + the handoff.

— END OF FINAL REPORT (research-only; nothing built; all metrics source-reported; all India/legal facts
unverified; advisory, human-in-the-loop, Rule 19). —
