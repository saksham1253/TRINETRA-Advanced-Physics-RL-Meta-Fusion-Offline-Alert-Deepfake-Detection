# CONTRADICTION REGISTER (MASTER_PROMPT §0.8 / §0.5 rule 5)
# Never average away disagreement. Each entry: question, papers on each side, their
# settings, which is better supported & why, what study of OURS could resolve it (build phase).
# Populated during P2/P3/P4. Seeded with contradictions already visible from the ABS corpus.

## CR-01 — Do bespoke RS foundation models beat general-purpose vision encoders?
- Pro-bespoke: much of A2 corpus assumes RS-specific SSL (Prithvi-style) is needed. NEW
  (2026-10-05): 2311.00566 CROMA (NeurIPS'23) — a SAR+optical contrastive+MAE FM purpose-built
  for exactly our S1+S2 aligned modality pair; reports gains over prior SoTA multispectral
  (finetune +1.8%, linear +2.4%, kNN +3.5%, seg +6.4% avg) on ITS benchmarks (ABS-only; our
  tasks differ). Strongest-matched bespoke contender for the EO encoder.
- Con: 2510.17014 "Do Satellite Tasks Need Special Pretraining?" — no consistent gain at
  ViT-B scale on low-res generalization. Also DINOv2 (2304.07193, FT) is a strong generic ViT.
- Setting diff: scale (ViT-B, small-scale) vs larger; task-specific; modality match (CROMA is
  radar+optical-specific, DINOv2 is RGB-generic → favors CROMA for InSAR+optical).
- Resolution (build): benchmark TRINETRA's encoder vs a general-purpose ViT (DINOv2) AND a
  bespoke RS FM (CROMA / SAR-FM 2510.17014) on the SAME spatial-CV protocol (ties F-01).
  Rule 16: no perf claim until built. STATUS: open — now 3 named contenders.
  THIRD contender (2026-10-05): 2503.11849 Copernicus-FM (TUM/NVIDIA, 2025) — any-modality
  hypernetwork FM pretrained on 18.7M aligned Sentinel images (S1/S2/S3/S5P), + Copernicus-Bench
  (15 tasks) + permissively-licensed benchmark datasets. Most capability-matched to our
  multi-Sentinel stack but highest complexity → trade vs CR-02 "simple wins". So CR-01 shortlist
  = {DINOv2 generic, CROMA radar-optical, Copernicus-FM any-modality}.
  FOURTH contender (2026-10-05): 2412.14123 AnySat (JEPA + scale-adaptive encoders; one model
  over 11 sensors, resolutions 1.25m–1280m; does flood+burn-scar+deforestation seg). Native
  multi-RESOLUTION handling fits our mixed S1/S2/MODIS/drone inputs. Updated shortlist (4) =
  {DINOv2 generic ViT, CROMA radar-optical MAE+contrastive, Copernicus-FM hypernetwork,
  AnySat JEPA scale-adaptive}. All HIGH-complexity options must beat a plain-ViT + GB baseline
  under identical spatial-CV (CR-02) before adoption.

## CR-02 — Deep learning vs simple gradient-boosted / decision-tree baselines for hazard
- Pro-DL: many axis papers assume deep models.
- Con: 2608.12422 — 5 DL models do NOT decisively beat GB; 3-rule tree wins lake hazards.
- Resolution (build): mandatory GB + decision-tree + persistence baselines under
  tile-withheld spatial-CV before any DL claim. STATUS: open (strongest external finding).
  REINFORCED (2026-10-06, QUOTA): 2405.00031 (SegNet wildfire e2e) — a compact model beats
  larger ones and input RESOLUTION is a safety hyperparameter, not accuracy-free; 2606.21130
  (burst-aware EWS) — a cost-thresholded XGBoost reaches high recall (0.914) at only modest
  AUC 0.697 / AP 0.670, i.e. a simple gradient-boosted model is the credible EWS workhorse;
  2306.04590 (ProCal) — transformers are MORE prone to proximity-bias miscalibration than
  CNNs, adding a calibration-reliability cost against fancy transformer encoders. All three
  push the parsimony prior harder. STATUS: open (parsimony strongly supported).
  EXTENDED (2026-10-06, P3): now a FIVE-DOMAIN pattern. (1) GLOF 2608.12422, (2) fire 2610.01994,
  (3) flood edge-seg 2609.20441, (4) InSAR 2509.18176, (5) wildfire-spread 2609.18555 — only
  fuel-load predictive (r=0.27); conv models rely on fire-front DISTANCE geometry; a transformer's
  extra environmental attention does NOT change the answer; terrain+fuel+wind alone still reach
  MCC 0.42. SIXTH corroboration from a non-hazard domain: 2610.03369 — in RL order-execution ALL
  learned policies lose to trivial TWAP/immediate baselines. STATUS: open (parsimony very strongly
  supported across 5 hazard domains + 1 non-hazard).
  SEVENTH (2026-10-07, P3): 2605.06643 MMDG-Bench (7,402 networks, fair comparison) — specialized
  Multimodal Domain Generalization methods give only MARGINAL improvement over a plain ERM baseline,
  no method consistently wins, trimodal fusion does NOT consistently beat the best bimodal config.
  Strongest fair-comparison evidence yet for parsimony AND "more modalities ≠ better." Build rule:
  always run ERM/concatenation-fusion + oracle upper-bound alongside any fancy fusion.
  CORNERSTONE DEEP-READ (2026-10-07, P3 R2): 2608.12422 re-studied ABS→FT-PARTIAL (OQ-02). The Con
  anchor is now quantified from full text: honest TILE-withheld spatial-CV with case-control matching
  vs unfailed sites collapses terrain-susceptibility AUC from a NAIVE ~0.90 to 0.76/0.71/0.54 (GLOF
  burst/landslide/small-flood) — i.e. naive non-spatial evaluation inflates AUC by ≈0.15–0.35, the hard
  number behind leakage bug #11. WHEN-timing from antecedent weather = ROC 0.73/0.83/0.82; within-Nepal
  burst 0.89. FIVE DL models (SSL, label-free anomaly, attention, PINN, PU) do NOT decisively beat one
  gradient-boosted baseline; for lake hazards a THREE-RULE decision tree (ruggedness + monsoon rainfall)
  wins outright. R6: InSAR deformation marks hazard but does NOT rank susceptibility among peer lakes.
  This is the single strongest CR-02 datapoint because it is OUR hazards, OUR region, OUR free-data
  constraint. Build mandate hardened: every TRINETRA model claim stated ONLY as "beats GB + decision-
  tree + persistence under tile-withheld spatial-CV with case-control matching + fixed seeds," else it
  is an overclaim. Adopt their protocol wholesale (matching, tile folds, deletion attribution, PINN
  monotonicity ∂hazard/∂slope≥0). STATUS: open (parsimony overwhelmingly supported; this is the anchor).

## CR-03 — Multi-stage iterative offline RL vs one-step
- Pro-multistage: pre-existing TRINETRA design (CQL/IQL → TD3-BC → PPO).
- Con: 2106.08909 — one-step beats iterative on much of D4RL, simpler, lower-variance.
- Also 2506.00505 — TD3-BC best on real Aave data.
- Resolution (build): benchmark one-step baseline first; justify multi-stage by evidence
  (ties F-06, OQ parsimony). STATUS: open.
  EXTENDED (2026-10-06, QUOTA): 2311.14110 DataCOPE — before trusting ANY learned alarm
  policy, run an OPE-feasibility gate (does the offline data even support evaluating this
  policy?); if infeasible, fall back to one-step / shielded fixed policy (new FM-22).
  2608.26304 (flood evacuation, two-stage stochastic optimization) — offers a classical
  decision-layer ALTERNATIVE to RL entirely for the evacuation/dispatch sub-problem, i.e. the
  alarm→action map need not be learned if a stochastic program suffices. STATUS: open; the
  "simplest adequate decision layer" ladder is now fixed-threshold → one-step offline RL →
  (only if OPE-feasible + coverage proven) iterative, with a stochastic-program alternative.

## CR-04 — Is naive conformal prediction valid on TRINETRA's streams?
- Pro-naive: default CP assumes exchangeability.
- Con: 2303.12783 (autocorrelation violates exchangeability), 2406.05405 (missingness),
  2511.11567 (endogenous shift from alarms changing behavior).
- Resolution: use time-series/robust CP; validate coverage empirically. STATUS: open.
  BASELINE METHOD FOUND (2026-10-06, QUOTA): 2010.09107 EnbPI (Xu & Xie, Georgia Tech) — wraps
  an ensemble, builds intervals from OOB residual empirical-CDF, needs NO exchangeability, NO
  data-splitting, NO retraining; explicit conditional/marginal coverage-gap bounds → 0 under
  regularity. This is the concrete baseline for TRINETRA's per-zone conformal layer and the
  honest replacement for the report's "conformal guarantee" overclaim (Bug #13): coverage is
  approximate with an explicit, shift-sensitive gap, NOT hard. Still OPEN: coverage under abrupt
  drift (pair with adaptive/online CP + drift monitor FM-07/FM-14) and under missingness (CR-04
  original concern 2406.05405 still un-read). STATUS: baseline resolved, drift/missingness open.
  RESOLVED-FURTHER (2026-10-06, P3): 2606.00690 (DistMatch) gives a theory-backed route for the
  distribution-shift half: patching → approximate LOCAL exchangeability + a matching-tree that bins
  similar residual patches (label-free KS-stat gain) + per-bin quantile regression + online updating;
  coverage guaranteed via a DISTRIBUTIONAL-STABILITY condition (approximate, not hard). This both (a)
  supplies a data-driven way to form the per-zone Mondrian strata we had hand-designed, and (b) confirms
  the honest framing: conformal coverage on our streams is approximate-under-stability, NOT a hard
  guarantee (disciplines Bug #13). WS8 CP stack = EnbPI/DistMatch base (validity under dependence) +
  PID-Expert online width control + drift monitor for abrupt breaks. STATUS: shift half resolved;
  abrupt-break + missingness (2406.05405) still open.
  EFFICIENCY LAYER ADDED (2026-10-07, P3 #33): 2511.15838 AFOCP (Simeone group) adds the width-
  reduction axis the stack lacked: calibrate nonconformity in the FEATURE space of the pretrained net
  (not output space) + attention that adaptively downweights stale history after a shift. Theory keeps
  long-term coverage while provably shrinking intervals (up-to-88% narrower vs OCP on their data).
  Slots in as: EnbPI/DistMatch base (validity under dependence) + AFOCP feature-space+attention (tight
  valid intervals under non-stationarity) + PID-Expert (online width feedback) + drift monitor. CAVEAT
  reinforcing honesty: AFOCP's guarantee is long-term/asymptotic — authors note LOCAL miscoverage right
  after an abrupt shift, exactly the rare-hazard moment, so a tight interval must NEVER suppress a
  physics-gated alarm (shield priority). Also feature-space quality depends on the SSL representation
  (ties CR-01). STATUS: shift + efficiency resolved in principle; abrupt-break local-coverage +
  missingness (2406.05405) still the open edge → must empirically validate per-zone coverage on
  Himalayan streams.

## CR-05 — MoE expert specialization: real or illusory?
- Pro: GMF design assumes per-modality expert specialization.
- Con: 2601.03425 — routing collapses to a domain-invariant "standing committee";
  2604.00801 — hard Top-K routing brittle.
- Resolution: audit expert utilisation; enforce/verify specialization or use soft gating.
  STATUS: open (ties F-07).

## CR-06 — Is the GMF (Gated Meta-Fusion) head genuinely novel, or established prior art?
- Pro-novel: pre-existing TRINETRA design presents GMF (stacking + bounded residual policy +
  per-zone Mondrian conformal + monotone safety shield) as a contribution.
- Con (2026-10-06, QUOTA): 2604.25512 (PHISHREV, post-hoc belief revision over a base
  detector gated by external knowledge) is direct prior art for the "knowledge-gated post-hoc
  correction layer" pattern; combined with Wolpert-1992 stacking, Meta-AAD (2009.07415) and
  RL model-selection (2205.09884) already in the ledger, GMF's components are each established.
- Resolution: reframe GMF honestly as an ENGINEERING COMPOSITION of known parts (novelty =
  the specific per-zone Mondrian-conformal + monotone-shield combination for life-safety EWS,
  "not found in N sources searched"), NOT a new mechanism. Disciplines the novelty claim per
  §0.5 rule (novelty = absence in sources searched). STATUS: resolved → GMF = composition,
  not invention; carry the honest framing into every design doc (T4 theme).

## CR-07 — Does multimodal fusion give TRINETRA robustness to a dropped sensor layer "for free"?
- Pro-free-lunch: intuition that fusing sat + CCTV + IoT means losing one is gracefully absorbed.
- Con (2026-10-06, QUOTA): 2310.03986 (robust multimodal learning w/ missing modalities) —
  fusion is NOT inherently robust to missing modalities; naive fusion degrades sharply, but a
  <1% extra-parameter adaptation recovers most performance. Reinforces FM-15 (missing-modality
  collapse) as a real, must-engineer failure, not a non-issue.
- Resolution (build): explicitly train/evaluate TRINETRA under each single-layer and
  two-layer dropout; adopt a lightweight missing-modality adaptation; always emit an
  uncertainty flag when a layer is absent. STATUS: open (ties FM-15).
  EXTENDED (2026-10-06, P3): 2609.15297 (Admissable) adds the crucial RANDOM-vs-WORST-CASE
  distinction. In a real hazard, missingness is NOT random — the event preferentially destroys the
  highest-signal sensor (tilt node on the moving slope, River-Eye in the flood, cloud over Sentinel-2)
  exactly when it matters → the correct threat model is ADVERSARIAL (worst-case) missingness. Their
  empirical lesson: training against random-uniform missingness UNDER-prepares vs training against a
  worst-case masking adversary. Build rule upgraded: evaluate the alarm policy by dropping the k
  MOST-informative modalities (not random), and require safe degradation on remaining LOCAL obs
  (ties PIER 2603.17319 forecast-independence) + hard physics shield as the floor. STATUS: open;
  threat model sharpened from "random dropout" to "worst-case dropout."
  CORROBORATED-AT-SCALE (2026-10-07, P3): 2605.06643 MMDG-Bench — ALL evaluated multimodal methods
  degrade significantly under corruption AND missing modalities, and SOME further compromise
  trustworthiness (calibration/OOD worsen when a modality drops). Confirms CR-07/FM-15 is pervasive and
  benchmarked, not incidental. Full missing-modality package for the build = MMDG-Bench (problem scale)
  + Admissable 2609.15297 (adversarial/worst-case threat model) + 2310.03986 (cheap <1% adaptation fix)
  + always emit an uncertainty flag when a layer is absent (and verify the flag doesn't itself degrade).
  CONSTRUCTIVE METHOD ADDED (2026-10-07, P3 #35): 2607.24683 Co4Miss (Mena/Ienco, RS benchmarks) — the
  missing-modality package gains a positive TRAINING recipe, not just threat models + a patch. Prioritize
  inter-modal CO-LEARNING over fusion-robustness: per-modality individual-prediction + contrastive
  alignment (feature-level) + decision-level distillation, with TWO complementary variants — Co-Miss
  (missing distillation, best when a SINGLE modality is absent) and FullCo (mutual distillation, best
  under EXTREME all-but-one missing). Validated on Multi-CropHarvest (multi-source EO) → higher transfer
  confidence for our satellite+ground fusion than generic AV papers. Single checkpoint, no test-time
  adaptation (offline-first friendly). Build update: GMF trains both Co-Miss + FullCo objectives and
  selects/weights by per-zone EXPECTED missingness (one LoRa node down = Co-Miss regime; storm kills
  power+comms leaving only satellite = FullCo regime). Full package now = MMDG-Bench (scale) + Admissable
  2609.15297 (worst-case threat model) + 2310.03986 (<1% adaptation fix) + Co4Miss (co-learning training
  recipe) + uncertainty flag on any absent layer. STATUS: CR-07 well-covered; validate on Himalayan data.

## CR-04 UPDATE (2026-10-07, P3) — conformal must target ACTION-LOSS coverage, not just predictive
- 2609.14821 (Decision-Oriented UQ for EO spatiotemporal FMs, #40) adds a decisive refinement to CR-04:
  a nominally 90%-calibrated interval (predictive coverage OK) can STILL under-cover the decision/action
  loss. They measure Forecast Conformal at only 84.9% ACTION-LOSS coverage despite reliable predictive
  coverage; their Utility-Aware Calibration restores 90.2%. For extreme-precip warning, decision-oriented
  UQ cuts REGRET 23.4% (largest under asymmetric high-impact loss — our exact miss≫FA regime).
- Resolution (build): the GMF conformal layer must be calibrated against the ALARM action loss (cost of
  miss vs false alarm, p*=0.0476), and the gate must report BOTH predictive AND action-loss coverage.
  Ordinary split-conformal on the raw risk score is NOT sufficient. STATUS: CR-04 sharpened; this is now
  a concrete UQ spec item for P14/P14Z.
- Composition: 2608.30205 (exPreCast-ENS, #41) PROVIDES the predictive distribution (residual-diffusion
  probabilistic ensemble); 2609.14821 tells us to CALIBRATE it to the decision loss. The two compose into
  our WHEN→alarm stack: ensemble forecast → decision-oriented calibration → cost-loss alarm threshold.

## THREAD I (2026-10-07, P3) — RESIDUAL doctrine now 5× corroborated (learn refinement on a backbone)
Pattern: do NOT forecast from scratch; learn a bounded RESIDUAL/refinement on top of a deterministic or
mechanistic backbone. Independent corroborations across 5 domains:
1. MW-Nowcast (2609.34836) — deterministic structure predictor + generative LOCAL RESIDUAL ensemble.
2. DRUM (2412.11942, ABS) — diffusion residual for precip.
3. Nowcasting-Nets (2108.06868, ABS) — recurrent residual nowcasting.
4. TREA-Net (2607.26854, #39) — ETSIR mechanistic prior + NN-invariant GATED RESIDUAL correction.
5. exPreCast-ENS (2608.30205, #41) — conditional residual DIFFUSION on a deterministic 4km nowcaster.
→ Lock into design: GMF uses a bounded residual policy on top of physics/mechanistic + stacking backbone
(already our GMF head design); SAR2Agri (#42) TD/FF temporal pretext is the SSL analogue (predict change/
next-frame). This is now one of the best-supported design principles in the corpus. STATUS: adopt as
first-class; validate residual-bound on Himalayan data (Rule 16).

## THREAD J (2026-10-07, P3) — EVT / tail-risk is a NEW, previously-missing design axis
- 2509.10362 (GNN-rP, #43) is the FIRST extreme-value-theory paper in the corpus. Our hazards ARE tail
  events; everything else read models the bulk (classification/regression/anomaly). GNN-rP combines a
  learned spatial embedding with a principled peaks-over-threshold r-Pareto tail model on IMERG.
- Design implication: the WHEN layer and people-at-risk estimate should carry an EXPLICIT tail model, not
  only a mean/quantile forecast. Reusable: per-cell [μ, σ, max, threshold-exceedance-frequency] IMERG
  features on a catchment spatial graph; joint-exceedance modeling = correlated compound-failure case.
- CAVEAT: EVT tail estimates are high-variance with few exceedances (data-sparse mountains) → treat as a
  wide-uncertainty PRIOR, never a hard threshold; this is a ZONING/strategic tool, not the real-time
  alarm. STATUS: new thread registered; evaluate in P14 (WHEN layer) with explicit uncertainty.

<!-- ===================== P4 FINALIZATION (2026-10-07, append-only) ===================== -->
# P4 CLOSURE — resolving studies named for each contradiction (feeds the build phase)
# MASTER_PROMPT §P4 task 3: "Finalize with the studies that could resolve each important
# contradiction in the build phase." Each CR gets: resolving study(ies), the build-phase
# experiment that would settle it, and residual-open status.

## CR-01 (spatial leakage vs reported skill) — RESOLVABLE, method fixed.
- Resolving studies: 2610.08227 (finite-sample theorem: effective N = Θ(n²/r²); buffer g = Θ(r·log(n/δ)))
  + 2608.12422 (empirical collapse on OUR hazards). 
- Build experiment: estimate per-region spatial-correlation range r (variogram); run tile-withheld CV with
  buffer ≥ r; report the random-vs-block CI-width ratio as a leakage diagnostic. STATUS: method CLOSED; the
  only open item is measuring r on Himalayan terrain (anisotropic). Owner WS6/P14.

## CR-02 (deep vs simple) — RESOLVED in favour of parsimony-with-residual.
- Resolving studies: 2608.12422 + 2609.36975 (Indian) + 2608.19672 + the residual THREAD I (C-03).
- Build experiment: GBDT/tree + persistence as mandatory baselines; DL only earns its place if a learned
  residual on the mechanistic backbone beats them under CR-01 CV. STATUS: CLOSED (doctrine); re-measure per head.

## CR-03 (physics backbone vs data-driven) — RESOLVED into complementary (residual).
- Resolving studies: 2407.06785 (PINN constraint), 2507.15614 (surrogate), THREAD I. STATUS: CLOSED — physics
  as backbone/gate, DL as bounded residual. Owner WS1/P7.

## CR-04 (predictive vs action-loss coverage; + missingness) — RESOLVED, spec written.
- Resolving studies: 2609.14821 (action-loss coverage ≠ predictive), 2512.14221 (mask-conditional valid CP),
  2610.02777 (online aggregation under abrupt shift), 2606.21773 (DFL doctrine).
- Build experiment: calibrate GMF conformal to the alarm action loss AND condition on the present-sensor mask;
  report predictive + action-loss coverage per zone and per mask. STATUS: CLOSED as a concrete P14/P14Z spec.
  Residual-open: cross-zone hydrological coupling in the conformal layer (G2).

## CR-05 (single-model confidence vs ensemble) — RESOLVED.
- Resolving studies: 2608.30205 (residual-diffusion ensemble) + 2610.01384 (post-hoc evidence scaling for the
  sparse/OOD regime). STATUS: CLOSED — ensemble predictive distribution + post-hoc conflict-aware widening.

## CR-06 (is GMF novel?) — RESOLVED (honest reframing).
- Resolving studies: stacking (Wolpert 1992), THREAD I residual, Mondrian conformal, shield (Alshiekh 1708.08611).
  STATUS: CLOSED — GMF is a documented COMPOSITION; novelty claim withdrawn (Rule 21). Owner P14.

## CR-07 (missing modality: random vs adversarial) — RESOLVED threat model + fix.
- Resolving studies: 2609.15297 (worst-case), 2605.06643 (benchmarked degradation), 2607.24683 (co-learning),
  2608.15261 (utility routing before fusion), 2610.03649 (SSL→classical anomaly, edge-feasible).
- Build experiment: evaluate by dropping the k MOST-informative modalities (not random); require safe
  degradation to local-obs + physics-shield floor; emit an uncertainty flag whenever a layer is absent and
  verify the flag itself does not degrade. STATUS: CLOSED as a worst-case protocol; validate on Himalayan data.

## NEW P4 contradiction — CR-08 (do foundation models help OUR regime?)
- Tension: TSFM hype vs parsimony. 2610.07232 shows Chronos-2 is SOTA zero-shot ONLY with accurate covariates
  and DEGRADES under covariate noise, while TimesNet (from scratch) is more robust under severe covariate
  uncertainty. Our monsoon covariates are noisy. 
- Resolving experiment (P14Z): benchmark a zero-shot TSFM vs a robust from-scratch model + residual on OUR
  covariate-noise regime, under CR-01 spatial-CV, scored by the cost-loss Value Score. STATUS: OPEN; owned by
  the compulsory zero-shot phase P14Z (D-011). This is the honest, pre-registered test of the FM claim.

## Residual-open contradictions carried to later phases
- C-12 human-compliance (reward design) — thinly sourced on arXiv (one hard number, 2109.07745); resolve with
  non-arXiv NHESS/IJDRR evidence in P13/P15 (D-010).
- G2 cross-zone conformal coupling — open research item, P14.
- 2609.14821 −23.4% regret body-number — re-verify vs PDF before load-bearing use (Audit #9 flag).
