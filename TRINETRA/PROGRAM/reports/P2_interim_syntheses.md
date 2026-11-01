# P2 Interim Syntheses — Literature Foundation I
# Program-owned (P2-created). Written every ~5 batches per MASTER_PROMPT §P2.
# NO own-system performance claims (Rule 16). Physics/evidence labels travel with every claim.

## Interim Synthesis #1 (after 10 NEW papers, 2026-10-06)

### Papers so far (all FT-PARTIAL, Tier-2, all NEW, all counting)
2605.17419 (LEWS displacement-robust), 2610.01994 (CatBoost>GOES-FDC), 2610.04392 (VAND 4.0),
2508.14203 (VAD survey), 2610.02777 (PID-Expert conformal), 2606.07593 (adv-FT ViT no transfer),
2609.38936 (signal-routed temp scaling), 2605.15894 (evidential smoke + selective), 2507.21649
(VAD DNN→MLLM survey), 2607.28248 (UQ survey). [+2606.12066 ABS-only, non-quota.]

### What changed / strengthened in the design
1. **CR-02 (simplicity under honest eval) got a fresh, strong data point.** 2610.01994: a plain
   CatBoost on satellite radiances BEATS the operational GOES-FDC product by F1 +0.16–0.38 under a
   CROSS-REGION held-out test, including the hard nighttime regime. This is independent of 2608.12422
   (GLOF) and in a different domain (fire) → CR-02 is now supported across TWO hazard domains with
   explicit spatial/temporal held-out testing. Doctrine stands: gradient-boosted + persistence +
   simple-rule baselines gate every deep claim.
2. **T2 (inputs are the weak link) sharpened into an operational honesty rule.** 2605.17419 shows
   landslide skill depends on rainfall FORECAST quality, not observed rainfall; forecast displacement
   degrades prediction. → New honesty rule for our EWS: report lead-time/skill UNDER forecast error,
   never with perfect observed inputs. Mitigation: displacement-invariant contrastive augmentation of
   the rain channel.
3. **Evaluation doctrine upgraded (VAND 4.0, 2610.04392).** Three concrete additions to our eval
   protocol: HIDDEN/held-out test + mandatory reproducibility artifacts; EFFICIENCY (latency/memory/
   power) as a FIRST-CLASS metric for edge models; and RARE-event performance reported SEPARATELY
   (aggregate metrics hide the collapse on the rare hazards we exist to catch). Reinforces FM-21.
4. **"Augmentation ≠ robustness" risk flagged (2606.07593).** Corruption fine-tuning does not transfer
   across unseen corruption types. → We must ENUMERATE expected field shifts (fog/rain/night/sensor-
   dropout/seasonal) and test each; do not rely on generic augmentation. Add to RISKS_FOR_BUILD.
5. **WS6 uncertainty stack now has a concrete, compute-aware design** from three complementary papers:
   - method menu + limitations (2607.28248 UQ survey): Deep Ensemble (Kaggle reference) → BatchEnsemble
     / last-layer-Bayes / MC-Dropout (edge). Separate aleatoric vs epistemic.
   - small-budget calibration (2609.38936): low-capacity risk-conditioned temperature (K≈3), NOT scalar
     and NOT high-capacity, because our hazard-validation sets are tiny.
   - online conformal (2610.02777): expert-aggregated PID conformal; EXPECT local under-coverage at
     abrupt onset → pair with the hard safety shield that does not depend on coverage (CR-04 confirmed).
   - evidential + selective prediction (2605.15894): vacuity-based ABSTENTION as a false-alarm control
     and image-quality/OOD gate; report accuracy-vs-coverage curves (ties E-07).
6. **WS4 video module scope clarified** by two VAD surveys. 2508.14203 gives a C1–C10 failure-mode
   checklist (esp. C3 anomaly-definition, C8 cross-scene shift, C10 concept drift). 2507.21649 gives
   the grounding-vs-understanding split (edge does GROUNDING; understanding/MLLM is a cloud tier) and a
   cheap/robust/private input menu (optical flow, skeleton). VAND 4.0 confirms VLMs are not yet a
   drop-in for fine-tuned detectors → no heavy VLM at the ₹2000 edge node.

### Synthesis-spine status
- T1 (simplicity dominates under honest eval): STRENGTHENED (2610.01994 second-domain evidence).
- T2 (inputs weak link): STRENGTHENED + new operational honesty rule (2605.17419).
- T3 (human response part of system): unchanged this batch.
- T4 (post-hoc knowledge-gated layers discipline GMF novelty): unchanged; WS6 stack details added.
- T5 (uncertainty first-class): STRENGTHENED — now a concrete 4-part WS6 stack with compute tiers.
- T6 (precursors spatial+temporal): unchanged this batch.

### Theme balance so far (10 papers)
- fire/smoke: 2 (2610.01994, 2605.15894) ; VAD/CCTV: 2 (2508.14203, 2507.21649) ;
  conformal/calibration/UQ: 3 (2610.02777, 2609.38936, 2607.28248) ; robustness/shift: 1 (2606.07593) ;
  eval/benchmark: 1 (2610.04392) ; EWS/landslide: 1 (2605.17419).
- Max theme share = 3/10 = 30% (UQ/calibration) — slightly over the ~25% target; NEXT batches will
  down-weight UQ and add CCTV-analytics, edge/efficiency, disaster-response, and survey-mined core
  methods to rebalance.

### Open contradictions / to-check
- None NEW this batch. All findings consistent with CR-02/CR-04 and FM-01/FM-20/FM-21.
- Author-list backfill owed for 2507.21649 and 2607.28248 (surveys) on any future FT promotion.

## Interim Synthesis #2 (after 18 NEW papers, 2026-10-06)

### Papers added since #1 (8 more, all FT-PARTIAL Tier-2, all NEW, all counting)
2511.21364 (BanglaMM disaster), 2609.20441 (edge flood-seg distillation), 2609.07455 (federated
parser-free VLM WSVAD), 2609.05066 (adaptive multi-granularity WSVAD), 2609.17175 (IRENE
probabilistic nowcasting), 2605.20167 (HaorFloodAlert operational EWS), 2509.18176 (InSAR
deformation forecasting), 2606.13896 (GeoFM transfer study). [+2606.12066 no-HTML, non-quota.]

### What changed / strengthened in the design
1. **CR-02 is now a THREE-DOMAIN, FOUR-INSTANCE doctrine.** New instances this batch:
   - 2609.20441: a FIXED MNDWI spectral rule is competitive with 300M-param GFM + distilled student
     on clean external flood benchmarks (flood domain).
   - 2509.18176: InSAR deformation ML baselines DEFAULT TO PERSISTENCE; you must demonstrate skill
     over persistence (deformation domain).
   Combined with 2608.12422 (GLOF) and 2610.01994 (fire), CR-02 now holds across GLOF, fire, flood,
   and deformation. DESIGN RULE hardened: every deep claim must beat (a) a fixed physical/spectral
   rule AND (b) persistence, reported as skill-over-baseline, under spatial/event-held-out CV.
2. **An operational TRINETRA ANALOG exists and validates the whole architecture (2605.20167).**
   HaorFloodAlert = free data + Sentinel-1 + RF/XGBoost + transboundary upstream signal + local-
   language SMS/WhatsApp last-mile, running live in a data-sparse South-Asian basin. This is strong
   external evidence our overall design is feasible AND cheap. It also contributes a NEW anti-leakage
   procedure (deseasonalization: subtract monthly climatological anomaly; report feature-label
   correlation before/after — they cut r 0.570→−0.031). Added to the evaluation doctrine.
3. **CR-01 encoder trade study now has its methodological backbone (2606.13896).** GeoFM rankings
   flip by task type and pretraining objective → we must evaluate DINOv2/CROMA/Copernicus-FM/AnySat
   ON OUR tasks (deformation forecast, flood/landslide seg), not by leaderboard; match pretraining
   objective to task; probe mid-layers; budget representation shift (CKA) during fine-tuning.
4. **Precipitation-input layer gets a probabilistic evaluation doctrine (2609.17175).** Make the
   nowcast probabilistic+ensemble; evaluate with CRPS + rank histogram (calibration) + RAPSD (spatial
   realism), not just MAE; importance-sample rare heavy-rain; be honest that skill ceiling is short
   (~90 min here) and lean on upstream/soil-moisture memory for longer lead (ties HaorFloodAlert).
5. **WS4 video architecture firmed up.** Federated MIL (train small scorer, keep raw video local) is
   the privacy+bandwidth-correct design (2609.07455); cheap-edge-scorer → suspect-verifier cascade;
   if a VLM verifier is used, use the LOGIT interface not prompt-fragile text-generation. Temporal
   granularity should be ADAPTIVE (event segmentation) not fixed windows (2609.05066), because our
   hazards span seconds→hours.
6. **Situational-awareness/crowd layer scoped honestly (2511.21364).** Social-media multimodal
   classification is feasible but text-dominant, noisy, biased, and recall collapses exactly when an
   event knocks out networks/attention → LOW-WEIGHT corroborating signal only, never a standalone
   trigger (Rule 19). Multilingual (Hindi/Garhwali/Kumaoni/Nepali) is a real constraint.

### Synthesis-spine status after 18
- T1 (simplicity dominates): now a hardened TWO-BASELINE rule (fixed rule + persistence), 4 domains.
- T2 (inputs weak link): forecast-displacement + deseasonalization + short nowcast horizon all added.
- T3 (human response part of system): last-mile delivery + impact module elevated to first-class
  (2605.20167); social-media caveat (2511.21364).
- T4 (knowledge-gated layers discipline GMF): unchanged.
- T5 (uncertainty first-class): probabilistic nowcast eval (CRPS/rank-hist) + full WS6 UQ stack.
- T6 (precursors spatial+temporal): InSAR deformation forecasting recipe added (2509.18176).

### Theme balance after 18 papers
- fire/smoke: 2 (2610.01994, 2605.15894) = 11%
- VAD/CCTV: 4 (2508.14203, 2507.21649, 2609.07455, 2609.05066) = 22%
- conformal/calibration/UQ: 3 (2610.02777, 2609.38936, 2607.28248) = 17%
- robustness/shift: 1 (2606.07593) = 6%
- eval/benchmark: 1 (2610.04392) = 6%
- EWS/landslide/flood/nowcast/InSAR (hazard core): 6 (2605.17419, 2605.20167, 2609.17175, 2509.18176,
  2609.20441, 2606.13896) = 33%
- disaster/crowd: 1 (2511.21364) = 6%
- Max single-theme share = 33% (hazard-core). This is slightly above the ~25% guideline but is the
  PROJECT'S CENTRAL DOMAIN and spans 6 distinct sub-topics (rainfall-forecast, operational EWS,
  nowcasting, InSAR forecasting, flood seg, EO encoders) rather than one narrow method; VAD at 22% is
  within guideline. Documented honestly; P3 should add robustness/eval/efficiency and non-hazard
  method papers to pull hazard-core share down.

### Open contradictions / to-check (updated)
- None NEW. All consistent with CR-01/CR-02/CR-04 and FM-01/FM-20/FM-21.
- Backfill author lists: 2507.21649, 2607.28248, 2606.13896 (not captured in HTML fetch headers).
- 2606.12066 (adverse-weather edge detection) remains no-HTML → PDF route deferred to P3 (PHASE_BACKLOG).
