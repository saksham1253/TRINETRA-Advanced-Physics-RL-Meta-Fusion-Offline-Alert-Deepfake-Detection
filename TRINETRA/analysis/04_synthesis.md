# 04 — Interim Synthesis of New Literature (250 verified ABS papers — FLOOR CLEARED)

Status: interim, last re-synthesised at the 250-paper checkpoint (floor 250 CLEARED; SOTA-sufficiency
is the real bar). Synthesises the net-new external literature harvested so far into themed
findings, each tied to a TRINETRA component and/or an existing bug ID (#0–#18) or a NEW risk
candidate. All source papers are abstract-depth (ABS); claims below are literature-grounded
hypotheses to be hardened with full-text reads before entering the final bug report.

Legend: [#n] = existing bug; [NEW] = new risk candidate surfaced by this literature.

---

## Theme 1 — InSAR/deformation input & forecasting (A1)
Papers: 2509.18176, 2511.04362, 2001.00769, 2301.05977, 2607.16264 (+ baseline InSAR corpus).

- **Persistence-baseline trap [NEW→#11/#18].** 2509.18176 shows ML deformation
  forecasters (LightGBM/LASSO) frequently collapse to naive *persistence* — they
  "predict tomorrow = today" and still score well on standard metrics. TRINETRA's
  InSAR-forecasting claim is unproven unless it is explicitly benchmarked against a
  persistence baseline and shown to beat it on *change* events. **Requirement:
  persistence (and seasonal-naive) baselines must be in every forecasting eval.**
- **Coherence features, not just amplitude/phase [#18].** 2511.04362 (L-band InSAR
  time series) finds adding *coherence* layers + model-inverted features + attention
  fusion beats intensity-only. TRINETRA should feed coherence into the encoder; this
  is directly relevant to future NISAR/ROSE-L L-band data over the Himalaya.
- **Phase-noise upstream gap [NEW data-quality].** 2001.00769 (phase denoising) —
  TRINETRA's pipeline assumes clean unwrapped phase; decorrelation in vegetated/snow
  Himalayan terrain is a silent upstream failure mode the datacube spec ignores.
- **Cheap edge deformation node exists [#7/#8 cost realism].** 2301.05977 demonstrates
  a Raspberry-Pi + GNSS-RTK + NB-IoT node with 3σ gross-error rejection + Butterworth
  LPF achieving 10 mm real-time. TRINETRA's BOM omits any gross-error/noise filtering
  on its ground nodes — a realistic comparator shows this is both feasible and necessary.
- **Network GNSS context [satellite/ground fusion].** 2607.16264 — regional GNSS
  network processing for subtle strain; TRINETRA could exploit existing networks
  rather than single stations.

## Theme 2 — EO foundation models & SSL encoders (A2)
Papers: 2510.17014, 2608.30392, 2401.04824, 2511.04474, 2312.03998, 2201.07006, 2508.01426.

- **Bespoke SSL encoder may be unjustified [#18].** 2510.17014 challenges building a
  task-specific SSL encoder when general EO-FMs exist; 2401.04824 (PhilEO) and
  2511.04474 (Prithvi-EO-2.0) show general geospatial FMs are strong. **Prithvi-EO-2.0
  beats SatMAE on landslide *mapping*** — so TRINETRA's novelty survives only for the
  *forecasting / pre-event* regime, not mapping. The report should re-scope its
  novelty claim and benchmark against a frozen EO-FM baseline.
- **Modality gap [#18].** 2608.30392 documents an EO-FM modality gap (optical↔SAR↔etc.);
  TRINETRA's multi-sensor fusion must address modality alignment, not assume it.
- **Time-series SSL ≠ vision SSL [#18 encoder design].** 2312.03998 (Series2Vec) and
  2201.07006 (ExtraMAE) warn that naive contrastive augmentation can *hurt* geophysical
  time series; similarity-based / masked-autoencoder SSL is safer. TRINETRA's sensor-
  stream SSL should avoid naive contrastive positives.
- **Extreme-weather FM as input [input + #18].** 2508.01426 (UniExtreme) — region-prior
  augmentation idea maps onto Himalaya-specific priors for the weather input.

## Theme 3 — Rainfall thresholds, extreme-event prediction, infiltration physics (A3/A4)
Papers: 2203.17155, 2508.01426, 2510.13012, 2105.13133 (+ Task C constants pending).

- **Iverson is a linearization [#3 scope].** 2510.13012 (full Richards FEM with
  dry+saturated+layered soils) and 2105.13133 (meshless Richards) are the full-fidelity
  references. They make explicit what TRINETRA's linearized Iverson transient model
  omits: layered-soil wetting-front dynamics and saturation transitions. This both
  *grounds* the physics-gate's validity window and reinforces that the Iverson algebra
  must be correct (ties to Bug #3 spurious cos β and Bug #17 downstream propagation).
- **Spatially biased training hurts [#9/#11].** 2203.17155 (when/where extreme-event
  DCNN) warns spatial bias in event occurrence degrades accuracy — relevant to
  TRINETRA's class-imbalanced, geographically clustered hazard labels.
- **Task C (I–D constants) still OPEN.** Caine 14.82·D^-0.39, Dahal–Hasegawa 73.9·D^-0.79,
  Garhwal 1.82·D^-0.23 remain unverified to page/equation (Bug #15). High priority.

## Theme 4 — Offline & safe RL, reward design, shielding (A5/A6)
Papers: 2305.03360, 2502.01307, 2104.06411, 2507.23603, 2402.00816, 2511.21531, 2112.11490.

- **Hand-tuned reward magnitudes are brittle [#9 fix].** 2502.01307 (PBRS) shows
  potential-based reward shaping is policy-invariant and far more robust to scaling
  than raw reward shaping. TRINETRA's miss=−100/FA=−5/… magnitudes are hand-tuned and
  fragile; recasting the shaping as PBRS preserves the optimal policy while making
  tuning safe. 2104.06411 adds subgoal shaping (watch→warn→evacuate escalation).
- **Shield may be UNREALIZABLE [NEW→#9].** 2507.23603 shows sets of hard-override
  safety rules can be mutually *unrealizable* (no action satisfies all simultaneously).
  TRINETRA's shield stacks several hard overrides (FS<1→Orange; tilt>5°/day→Red;
  24h-rain>150mm→Orange; GLOF→Red) — these can conflict (e.g., simultaneously demanding
  two different alarm levels). **Need a formal realizability check + priority lattice.**
- **Fixed-fallback shields are suboptimal [#9 fix].** 2511.21531 (predictive safety
  shield) and 2402.00816 (approximate model-based shielding, continuous) show shields
  that merely sample a safe/fallback action ignore downstream performance; a predictive
  shield picks the *best safe* escalation and keeps hard guarantees. Direct upgrade to
  TRINETRA's fixed overrides. 2112.11490 (latent shielding) handles the high-dim sensor
  state where a tabular shield is infeasible.
- **Offline-RL pessimism [#9].** 2305.03360 reinforces conservative/pessimistic value
  estimation for TRINETRA's offline CQL/IQL stage (small, biased logged data).

## Theme 5 — Conformal prediction & calibration under shift (A7/A8)
Papers: 2406.05405, 2511.11567, 2605.21742, 2007.12229, 2108.04907, 2007.11117, 2210.02558.

- **Conformal guarantees break under the exact conditions TRINETRA faces [#8/#13].**
  2406.05405 (conformal under dropout/missingness) and 2511.11567 (endogenous
  distribution shift) show marginal-coverage guarantees degrade under missing sensors
  and feedback-induced shift — both endemic to an offline-first alarm system. The
  report's conformal overclaim (#13) must be qualified; Mondrian/per-zone conformal
  needs explicit missingness + shift handling.
- **Thresholding is fine IF calibrated [#1/#13].** 2605.21742 — under class imbalance,
  simple thresholding performs *exceptionally* when the model is well-calibrated.
  This links calibration (#13) directly to the threshold-choice bug (#1): the ~10×
  threshold conflict is only safe if calibration is proven first.
- **Deep-SVDD hypersphere collapse [NEW anomaly robustness].** 2108.04907 (FlowSVDD)
  documents a known degenerate failure where the Deep-SVDD bounding hypersphere
  collapses to a point. TRINETRA uses Deep SVDD as an anomaly ensemble member →
  must use an anti-collapse variant.
- **Isolation-forest interpretability/variants.** 2007.11117 (DIFFI) + 2210.02558
  (ABIForest) give interpretability + variants for the iForest member.
- **Generative augmentation for rare classes [#9].** 2007.12229 (SeismoFlow) — flow-based
  synthesis of rare geophysical signals mitigates imbalance.

## Theme 6 — Drift / OOD monitoring (A14)
Papers: 2210.08470, 2103.00903, 2105.01419, 2606.20216, 2302.12127, 2312.01530.

- **Drift *type*, not just magnitude [#8].** 2105.01419 (Meta-ADD) classifies the TYPE
  of drift (seasonal vs regime vs sensor-fault); TRINETRA must react differently to
  each, so the monitor should be drift-type-aware. 2210.08470 (CDM) + 2103.00903 (STUDD)
  are concrete monitors; 2606.20216 gives an eval protocol.
- **Pre-emptive change-sign [#8 upgrade].** 2302.12127 (Ddim) raises an early-warning
  signal *before* the model fully degrades → proactive retraining trigger.
- **Feedback itself causes shift [NEW→#8/#11].** 2312.01530 (AFAPE) — deploying an agent
  that decides when to acquire features/alarms *itself* triggers distribution shift.
  TRINETRA's RL alarm policy changes the data it later sees (people evacuate, sensors
  queried) → endogenous shift must be in the OPE/eval design.

## Theme 7 — Edge VAD / LSPIV / river sensing (A9)
Papers: 2310.05330, 2412.18298, 2503.12905, 2203.03962.

- **Edge-latency overclaim [#14].** 2310.05330 + 2412.18298 (edge-VAD) and 2503.12905
  (event-camera + spiking-NN VAD) show realistic edge compute/energy budgets. TRINETRA's
  Cerberus benchmark was on an L40S GPU (57.7 fps), NOT a Jetson-class edge node — the
  edge-latency claim is unsupported. SNN/event-camera is a lower-power alternative path.
- **Label-scarce VAD is the real setting [#14].** 2203.03962 (unsupervised VAD) matches
  TRINETRA's reality: no curated hazard-video labels → unsupervised/weakly-supervised
  VAD is the honest baseline. (A9 LSPIV/river-velocity still thin — target next.)

## Theme 8 — Comms robustness: LoRa / LPWAN / DTN (A10)
Papers: 2409.20408, 1703.01985, 1809.04324, 1803.00275, 2603.15945.

- **433 MHz is non-ISM in India [#6].** Carried bug; the comms literature below
  supports the fix path (move to IN865–867; add relaying + store-carry-forward).
- **Offline-first dissemination patterns [#6/#8].** 1803.00275 (CIDOR ICN+DTN) and
  2603.15945 (opportunistic routing evaluated on a real post-earthquake scenario) give
  concrete store-carry-forward designs for when gateways fail. 1809.04324 (LPWA-MAC
  bounded delay) matters because alarms have latency deadlines.
- **Backhaul for isolated valleys.** 2409.20408 (LoRa direct-to-satellite) + 1703.01985
  (LoRa D2D) give node-to-satellite and node-to-node relay options for sites with no
  terrestrial gateway — essential for an offline-first Himalayan deployment.

## Theme 9 — GLOF / dam-break / runout / flash-flood (A11)
Papers: 2404.15860, 1904.07213, 2012.11154, 2505.22535 (+ baseline runout/GLOF corpus).

- **Simple threshold vs full hydrology DIVERGE in small steep basins [#11].** 1904.07213
  (ERICHA vs Flood-PROOFS) finds rainfall-threshold and distributed rainfall-runoff EWS
  agree for large catchments but *diverge for small catchments* — exactly the small,
  steep Himalayan basins TRINETRA targets. This validates the necessity of TRINETRA's
  physics gate (not just a rainfall threshold) and warns the two can disagree.
- **External benchmarks exist [#11/#18].** 2012.11154 (FlowDB) is a large precip+river+
  flash-flood dataset; 2505.22535 (RiverMamba) is SOTA flood forecasting. TRINETRA's
  underpowered (n≈5) eval should pretrain/benchmark on these rather than only its own region.
- **High-fidelity runout references.** 2404.15860 (hybrid FEM-MPM tailings runout) anchors
  the physics-gate runout model (Scheidegger/Froehlich) against a large-deformation reference.

## Theme 10 — Multimodal fusion, stacking, MoE (A12)
Papers: 2402.01379, 2011.06125, 2507.07527.

- **GMF multicollinearity risk [NEW→GMF].** 2402.01379 shows stacked-generalization
  meta-learners suffer *multicollinearity* when base predictions are correlated — and
  TRINETRA's GMF experts all observe the same storm, so their outputs are highly
  correlated. A plain linear/ridge meta-head will be unstable. **Fix: boosting
  meta-learner or Caruana ensemble selection, which remove multicollinearity.**
- **Encoder→GBT stacking precedent.** 2011.06125 (Hurricast) validates the
  encoder→gradient-boosted-tree stacking pattern GMF uses.
- **Modality-aware MoE.** 2507.07527 (MAPEX) supports the gated mixture-of-experts
  design, with explicit modality awareness (ties Theme 2 modality gap).

## Theme 11 — Decision layer: evacuation / cost-loss (A13) — THIN, PRIORITIZE
Papers: 2608.04225, 2103.15156 (only 2 so far).

- **Downstream evacuation is unmodeled [decision-layer completeness].** TRINETRA emits
  alarms + a people-at-risk estimate but stops there. 2608.04225 (adaptive-robust
  evacuation under evacuee uncertainty) and 2103.15156 (ridesharing evacuation; efficiency
  is *nonlinear* in resources) show the alarm must feed a robust evacuation plan, and that
  the RL disruption-cost term (−0.01/person-hour) oversimplifies real evacuation economics.
- **GAP:** this theme is under-covered (2/96). Target 6–10 more A13 papers next.

---

## Increment: batches 11–15 (24 new papers, 96→124)

Harvested after the interim synthesis above, targeting the weak axes (A13, A9, A12,
A3) plus deepening A6/A7. Written at the 124-paper checkpoint. Still ABS-depth.

### A13 — evacuation, cost-loss, compliance, equity (was weakest, now covered)
Papers: 2412.05777, 2602.14676, 2502.17701, 2601.06664, 2103.03413.
- **Compliance is heterogeneous → biased lead-time & disruption [NEW→decision layer].**
  2502.17701 / 2412.05777 show real evacuation compliance is partial, socially
  stratified, and behaviourally driven. TRINETRA's people-at-risk + disruption-cost
  (−0.01/person-hour) assume FULL compliance and treat all persons as identical. Real
  compliance heterogeneity biases both the lead-time credit (+2/h) and the disruption
  penalty, and can entrench EQUITY harms (vulnerable groups under-served). **Promote as
  a decision-layer finding: model compliance probability + equity-weighted cost.**
- **Cost-loss / decision-theoretic warning value [#13/#9].** 2601.06664, 2103.03413,
  2602.14676 reinforce that warning value must be evaluated with a cost-loss model
  (ties the Bayes 5/105 framing) and that lead-time has diminishing/か context-dependent
  value — not a flat +2/h cap. Supports reworking the RL reward's lead-time term.

### A9 — LSPIV / river-surface velocity → discharge (River Eye realism)
Papers: 2605.14645, 1607.04139, 2401.06229.
- **Un-budgeted River-Eye accuracy bug [NEW→#8].** 1607.04139 (unseeded LSPIV
  contaminated by capillary-gravity waves; needs phase-speed correction) + 2401.06229
  (static stage-discharge/Manning-Strickler rating curves BREAK under unsteady/transient
  flow; need 1D Saint-Venant + Bayesian uncertainty) + 2605.14645 (vision-based flow
  needs per-site calibration + robust filtering). Together: converting ₹2,000 River Eye
  surface velocity → discharge via a static rating curve is unreliable during exactly the
  flash-flood transients that matter, and bare LSPIV is wave-contaminated. **The River
  Eye node needs per-site calibration, wave-correction, and discharge uncertainty bounds —
  none budgeted. Extends #8.**

### A12 — multimodal fusion, stacking, MoE, reliability gating (deepened)
Papers: 2512.01750, 2603.01511, 2410.04833, 2505.19190, 2204.07653.
- **Down-weight untrustworthy modalities [NEW→GMF design].** 2603.01511 (MERA,
  Dempster-Shafer reliability-aware discounting), 2512.01750 (per-modality reliability
  gating + sparse MoE under energy limits), 2505.19190 (I2MoE interaction-aware experts
  that model agree/contradict). TRINETRA's GMF currently fuses experts without an
  explicit per-modality RELIABILITY signal; when a sensor is degraded (brownout #8,
  cloud over optical, decorrelated InSAR) its expert should be discounted, not trusted
  equally. **GMF needs a reliability-gating / evidential-discounting mechanism.**
- **No single fusion strategy dominates [#18 eval].** 2410.04833 (ECCV-W) shows
  early/late/MoE fusion each win on different classes (late-fusion AUC 0.698 overall but
  per-class recall varies). → TRINETRA must report PER-HAZARD / PER-CLASS fusion metrics,
  not one aggregate, and cannot assume its chosen fusion is globally best.
- **Principled Bayesian multi-hazard fusion comparator [#12/#18].** 2204.07653
  (causal-graph Bayesian network, handles UNOBSERVED hazard nodes, fuses InSAR DPMs +
  susceptibility, propagates uncertainty) is a strong structural alternative/benchmark
  to the GMF stacked head and natively handles TRINETRA's sparse-sensor reality.

### A3 / rainfall input — sub-hourly structure & nowcasting
Papers: 2602.11194, 1706.03458, 2407.06785, 1204.6231.
- **Single I=aD^-b curve is too coarse [#3/#15].** 2602.11194 (flume+ML) finds onset
  depends on grain size (D50), antecedent hydrophobicity and SUB-HOURLY rain structure —
  the first 10 min of high-intensity rain dominate. → physics gate should use short
  (≤10 min) rain windows + soil-type conditioning, not just event totals.
- **Rainfall nowcasting eval must up-weight rare heavy rain [#1/#11/#18].** 1706.03458
  (TrajGRU/HKO benchmark) — location-variant motion + rare-pixel-weighted loss; a
  documented SOTA baseline for any TRINETRA rainfall module.
- **Fuse physics INTO the learner [#3/#16/#17].** 2407.06785 (PINN + Newmark, Dahal &
  Lombardo) retrieves geotechnical params from proxies and constrains the net with slope-
  stability physics — a precedent for the meta-fusion residual-over-physics design, and
  (note) the same Dahal of the Task-C "Dahal-Hasegawa" I–D threshold → citation lead.
- **EWS must report its own error rates [#11].** 1204.6231 — generic early-warning
  indicators seldom characterise false-alarm/miss rates, which can be severe; a
  model-based indicator beats bare variance-based EWS. Reinforces #11 (n≈5 underpowered)
  and justifies the physics gate over a bare statistical EWS.

### A6 / A7 — safe-RL runtime assurance & conformal for time series (SOTA fixes)
Papers: 2310.04288, 2409.04641, 2303.12783, 2502.05709, 2509.10348.
- **Optimal, least-conservative shield [#9 fix].** 2310.04288 (optimal RTA via
  reachability + RL) proves fixed-fallback shields (TRINETRA's current design) are overly
  conservative and can still violate safety; an optimal switch raises alarms only when
  provably necessary. Pairs with 2511.21531 / 2402.00816 (predictive shielding) as the
  SOTA basis for the shield redesign.
- **Multi-objective safety via successor features [#9].** 2409.04641 (SUSFAS) — compose
  the miss/FA/lead/disruption objectives explicitly + backup controllers instead of one
  hand-tuned scalar reward.
- **Conformal for autocorrelated / multi-dim streams [#13 fix].** 2303.12783 (HopCPT)
  pinpoints why TRINETRA's conformal claim overreaches — autocorrelation violates
  exchangeability — and gives the SOTA fix; 2502.05709 (flow-based multi-dim conformal)
  gives joint, correlation-aware prediction regions with provable coverage for the
  multi-sensor state. 2509.10348 (selective prediction/abstention + per-class rejection
  thresholds) → the alarm head should ABSTAIN/escalate-to-human when uncertain, with
  per-hazard (not global) thresholds. Direct upgrades for #13 and #1.

### A8 / IoT — sensor-fault vs event, edge compute reality
Papers: 2604.08581, 1203.0541, 1509.06065, 2605.02153, 2411.04153, 2512.09251.
- **Edge compute budget quantified [#14].** 2604.08581 — genuine on-MCU anomaly
  detection fits in ~3.3 KB SRAM / 63 KB Flash at µs latency ONLY with tiny statistical
  models (Z-score/RMS), NOT the heavy VAD/encoder stack (which was benchmarked on an
  L40S, #14). → tiered design: tiny on-node screen → escalate to backhaul.
- **Faulty sensors fabricate/mask events [NEW→#8].** 1509.06065 (DependSHM) shows faulty
  sensors can cause false-positive or false-negative hazard diagnosis WITHOUT being
  detected; 1203.0541 gives the Neyman-Pearson/Bayes test to separate FAULT from EVENT.
  → TRINETRA needs cross-node consistency + fault-tolerance, not naive per-node trust.
- **SAR flood layer specifics [#10/#18].** 2605.02153 (fuse VV+VH polarizations — single
  pol fails in vegetated/volume-scatter terrain) + 2411.04153 (urban SAR flood double-
  bounce/layover/shadow pitfalls) + 2512.09251 (GLACIA MLLM glacial-lake SOTA, but far
  too heavy for edge → cloud-side comparator only, #14).

---

1. **[NEW] Persistence-baseline eval gap** (2509.18176) — forecasting claims unproven
   without persistence/seasonal-naive baselines. → extends #11/#18.
2. **[NEW] Shield unrealizability** (2507.23603) — stacked hard overrides can conflict;
   need realizability check + priority lattice. → extends #9.
3. **[NEW] GMF meta-head multicollinearity** (2402.01379) — correlated experts destabilize
   the stacked head; use boosting/Caruana meta-learner. → GMF design.
4. **[NEW] Deep-SVDD hypersphere collapse** (2108.04907) — anomaly member can degenerate;
   use anti-collapse (flow-based) variant. → anomaly robustness.
5. **[NEW] Endogenous feedback shift** (2312.01530) — the alarm/sensing policy itself
   shifts the distribution; must be in OPE/eval. → extends #8/#11.
6. **[NEW] Conformal breaks under missingness+feedback shift** (2406.05405, 2511.11567)
   — sharpen the #13 overclaim with explicit missingness/shift handling.
7. **[NEW] Rainfall-forecast spatial error unmodeled** (prior flag from 2605.17419) —
   physics gate + anomaly head assume accurate rainfall; forecast spatial displacement
   is an unmodeled failure mode.
8. **[NEW] Evacuation compliance heterogeneity & equity** (2502.17701, 2412.05777) —
   people-at-risk + disruption-cost assume full, uniform compliance; real compliance is
   partial and socially stratified → biased lead-time credit + entrenched equity harm.
   → decision-layer finding.
9. **[NEW] River-Eye discharge-conversion accuracy bug** (1607.04139, 2401.06229,
   2605.14645) — unseeded LSPIV is wave-contaminated and static rating curves break in
   transient flow; needs per-site calibration + wave correction + discharge uncertainty.
   → extends #8.
10. **[NEW] GMF lacks per-modality reliability gating** (2603.01511, 2512.01750,
    2505.19190) — experts fused without reliability discounting; a degraded sensor's
    expert should be down-weighted (Dempster-Shafer/evidential). → GMF design.
11. **[NEW] Sensor fault vs. real event not separated** (1509.06065, 1203.0541) — faulty
    nodes can fabricate or mask a hazard signature undetected; need Neyman-Pearson/Bayes
    fault-vs-event test + cross-node consistency. → extends #8.
12. **[NEW] Edge compute budget contradicts heavy stack** (2604.08581) — real on-MCU
    anomaly detection fits only tiny statistical models; heavy VAD/encoder needs backhaul.
    → sharpens #14; mandates tiered edge→cloud design.
13. **[NEW] Shield is a conservative fixed-fallback RTA** (2310.04288, 2511.21531,
    2402.00816) — provably suboptimal and can still violate; replace with optimal/
    predictive reachability-aware shield. → extends #9.
14. **[NEW] No single fusion strategy dominates** (2410.04833) — must report per-hazard/
    per-class fusion metrics, not one aggregate. → extends #18.

---

## Wave 22–28 integration (papers 164→204) — new evidence, no new candidate numbers

These waves mostly *strengthened existing candidates* with harder, more quotable evidence
rather than opening new failure modes — a sign the candidate set (#1–#18 bugs + 14 NEW) is
saturating, which is itself a SOTA-coverage signal.

- **Candidate #8 (evacuation compliance) now has a HARD number.** 2109.07745 (Kincade Fire,
  large-scale GPS) measures ~**46% compliance** inside warning/order zones, and self+shadow
  evacuees were **>half** of all evacuees. This converts #8 from "compliance is heterogeneous"
  to a concrete, citable calibration: the people-at-risk / disruption-cost model must assume
  ~50%-order compliance *and* model spontaneous (shadow) evacuation, not 100% ordered response.
  2512.14683 (deployed hospital EWI) adds the governance half: real safety-critical EWS keep
  **humans in the threshold-setting + interpretation loop** with SHAP explanations and a 3-tier
  stratification — validating TRINETRA's shield + human-in-loop stance over full autonomy.
- **Candidate #11 (sensor-fault vs event) + #14 (OOD) reinforced.** 2503.09947 shows the
  *best* in-distribution model (LSTM) is the *most* fragile under data corruption and that
  spatial generalization to ungauged basins is poor across all models — exactly TRINETRA's
  new-catchment deployment risk. 2508.18045 (Riemannian streaming change-point, robust Huber
  vs sensitive Karcher centroid) gives a concrete detector that fires on real regime shifts
  but resists drift/outliers — a principled fault-vs-event discriminator for manifold-valued
  sensor streams (tilt, SAR covariance).
- **#11 eval methodology now has a named fix.** 2110.09497 supplies a concrete **spatial
  cross-validation** scheme (+ EVT-justified GB loss for the rare tail) — the exact remedy
  for the leaky/underpowered evaluation flagged in #11; combine with EVT loss for the
  landslide/cloudburst tail.
- **#13 (conformal overclaim) upgraded with the correct machinery.** 2405.06479 (multi-source
  weighted conformal under covariate shift, with coverage guarantees) matches TRINETRA's
  heterogeneous multi-source fusion far better than vanilla split conformal; 2310.03545
  reframes conformal as a **failure-probability** statement ("P(true hazard inside interval)"),
  which is exactly the honest guarantee a warning system should publish. Together they tell us
  how to *replace* the overclaim rather than just flag it.
- **Anomaly core (Deep SVDD) hardening.** 2405.18929 (deep **positive-unlabeled** anomaly
  detection for *contaminated* unlabeled data, with a generalization bound) directly fixes the
  implicit "normal background is clean" assumption of TRINETRA's Deep-SVDD member — the Himalayan
  background is certainly contaminated by unlabeled real events. This sits under candidate #11.
- **Uncertainty on an edge budget (#8/#14 + candidate #12).** 2309.13207 and 2604.06387 show
  **evidential deep learning** gives decomposed aleatoric+epistemic uncertainty from a *single*
  cheap forward pass, beating GP/MC-dropout/ensembles on cost+calibration — the right UQ choice
  given the compute-budget contradiction (candidate #12) and the need to flag epistemic/OOD
  (new-region) inputs. 2207.12545 (p-DkNN) and 2105.03876 add statistically-grounded
  **reject-option/abstention** at low FPR, complementing conformal for the "defer to physics
  gate / human" path.
- **Rare-event regression (#1/#11).** 2509.23240 (LatentDiff) and 2306.06599 (VIR) target
  *deep imbalanced regression* — the rare large-magnitude tail that matters most for
  people-at-risk and is currently underpredicted; VIR couples tail accuracy with calibrated UQ
  (NIG output pairs naturally with the evidential direction above).
- **Comms resilience (#6/#8, axis A10) deepened.** 2312.08387 (JMAC multi-hop LoRa mesh with
  predictive wake-up) and 2507.07841 (HaLow mesh + SDN post-disaster) argue the ground network
  should be **multi-hop/self-healing mesh**, not star-to-gateway, to survive both Himalayan
  non-line-of-sight terrain and post-event infrastructure damage — sharpening the storm-brownout
  / last-mile-alert failure mode in #8.
- **Physics-gate philosophy validated.** 2606.04143 (PIML flood with a simple Trend-Alignment
  constraint) shows a *light* physical constraint stabilizes DL under data-scarcity + extremes
  while a pure-DL baseline goes unstable — direct support for TRINETRA's physics gate, and an
  honesty model (it openly notes residual peak-magnitude error).
- **EO cross-region benchmarking (#18).** 2210.10732 (OpenEarthMap, 97 regions, built-in UDA
  protocol) and 2509.17942 (StefaLand geoscience FM with strong spatial generalization incl.
  landslide/soil-moisture on academic compute) give concrete public benchmarks + a cheap FM
  baseline to answer the under-benchmarking / cross-region-generalization gap.

**Net effect on priorities:** candidates #8, #11, #13 move from "flagged" to "fix specified"
(compliance≈46%; spatial-CV + EVT; multi-source WCP + failure-probability framing). No new
distinct failure mode emerged in waves 22–28 → the catalogue is converging.

## Theme-balance verdict (updated at 124-paper checkpoint)
Strong: A1, A2, A6, A7, A8, A10, A11, A13, A14. Moderate: A3, A4, A5, A9, A12.
**Next waves (to push well past 250 floor — user directive to maximise SOTA coverage):**
- A5 offline-RL depth (OPE/FQE, distributional-shift bounds, d3rlpy-specific).
- A12 stacking theory depth (super-learner guarantees, MoE routing stability).
- A4 unsaturated-soil / Richards numerics beyond the 2 found.
- A10 LoRa/LPWAN/DTN capacity + duty-cycle under disaster traffic.
- A1 InSAR SBAS/PS atmospheric-correction + landslide-specific DL.
- A14 OOD/drift detection + test-time adaptation for sensor streams.
- Cross-axis: disaster-EWS deployment case studies; alarm fatigue / false-alarm cost;
  explainability for high-stakes decisions; data assimilation (EnKF) for physics state.

## Wave 29–32 integration (papers 204→231)
Harvest refocused on the moderate axes (A3/A4/A5/A9/A12) plus the "honest-baseline" and
edge-deployment threads. Net effect: one **landmark external reality-check** and several
fixes that firm up existing candidates. No new distinct failure mode — catalogue still converging.

- **LANDMARK — 2608.12422 (free-satellite Himalayan GLOF/landslide test).** This is nearly a
  direct competitor study and the single most important external benchmark found. Using the SAME
  free signals TRINETRA uses (InSAR moraine deformation = *which* lake; antecedent satellite
  weather = *when*), under **spatial cross-validation that withholds whole map tiles** against a
  strong GB baseline: naive terrain-susceptibility AUC ~0.9 **collapses to 0.76/0.71/0.54** when
  evaluated honestly, and **five deep-learning models do not decisively beat a simple
  gradient-boosted baseline** (a 3-rule decision tree wins outright for lake hazards). This gives
  **hard numbers** for bug #11 (spatial leakage inflates AUC by ~0.15–0.35) and bug #18
  (DL-over-baseline unjustified). **Action: TRINETRA's headline skill claims must be restated
  under tile-withheld spatial-CV against a GB/decision-tree baseline, or they are overclaims.**
  This is corroborated independently by 2510.10799 (**linear regression beats LSTM and
  Temporal-Fusion-Transformer** for terrestrial-water-storage) — a *second* "simple beats deep"
  result in the same geoscience-hydrology domain. Both now cited directly in the bug report under
  #11/#18.
- **Flood pathway sharpened (#11, flood).** 2606.29134 (AlphaEarth land-context priors) shows
  single-temporal SAR flood detection is physically **ambiguous** (new water vs permanent water vs
  smooth surfaces) and that **per-event** evaluation is mandatory (echoing 2608.12422);
  IGARSS-2022 bi-temporal SAR (+6% IoU) confirms TRINETRA should use **pre/post change**, not
  single-pass SAR, for inundation. 2501.11372 (2D shallow-water PINN with terrain + rainfall
  source terms) and 2507.15021 (**ALPINE**, full mass+both-momentum shallow-water PINN) validate
  the physics-gate philosophy — ALPINE explicitly finds **physics constraints help most at peak
  storm intensity**, exactly TRINETRA's regime.
- **GLOF data + scope (#7/#15).** 2510.10546 (**GLOFNet**: Sentinel-2 + ITS_LIVE + physical
  precursors, forecasting-oriented) is a ready multimodal benchmark on TRINETRA's own data sources
  for the GLOF pathway → feeds the dataset registry. Avalanche coverage gap flagged: 2310.04428
  (SVM + MPM) shows the current Iverson/TRIGRS physics stack does **not** cover snow-avalanche
  mechanics; 1901.04695 (zero-inflated-gamma snow) gives a calibrated parametric template for the
  many-zeros-plus-heavy-tail trigger distribution.
- **Offline-RL depth (#9, axis A5 — previously "moderate").** 2106.08909 (**Offline RL *without*
  OPE** — one-step constrained improvement beats iterative actor-critic, which suffers compounding
  OPE variance) is a direct caution against TRINETRA's heavy CQL/IQL→PPO plan: **try a simpler,
  more robust one-step offline baseline first**. 2206.02000 (**HVE**) supplies the principled
  bias-variance-controlled OPE needed to *honestly* value a candidate alarm policy from historical
  data before deployment.
- **Safe-policy / shield formalism (#9, candidate #2/#13).** 2305.16147 (**CoCoRL**: learn a
  provably-safe *convex* constraint set from safe demonstrations, transferable across catchments)
  offers the realizability structure candidate #2 (shield unrealizability) needs; 2602.20729
  (Fuz-RL) and 2505.14510 (**BACON** graded-logic, fully explainable + human-tunable) point the
  shield/alarm layer toward a transparent, uncertainty-aware decision structure rather than an
  opaque learned policy — aligning with the human-in-loop finding (2512.14683).
- **GMF head robustness (candidate #3/#10, axis A12).** 2006.08573 (**Neural Ensemble Search** —
  *architecturally diverse* ensembles beat deep ensembles on calibration + dataset shift) argues
  GMF experts should be deliberately heterogeneous, not clones. 2604.00801 (**Routing-Free MoE** —
  removes brittle centralized Top-K routing; experts self-activate) is a concrete, more-robust
  alternative to a fragile learned router over correlated experts (the candidate-#3
  multicollinearity risk), and its self-activation naturally encodes per-expert reliability
  (candidate #10).
- **Edge-budget resolution (#14, candidate #12, axis A9).** 2306.00001 (**TinyissimoYOLO**:
  180 fps / 196 µJ, <0.5 MB on an MCU accelerator, but only ~3 classes) bounds what a cheap node
  can do and confirms the Cerberus/L40S VAD cannot run on an MCU. 2604.27178 (KD: heavy
  ViT/FM **teacher** → compact low-energy **student**) and 2402.02781 (dual-KD sound-event
  detection at 1/3 params) operationalize the **tiered edge→cloud** design that resolves #14 within
  the ₹2000 power envelope. 1707.06611 (first LSTM-in-hydrology, SMAP gap-fill, robust spatial
  extrapolation) is a useful nuance: DL *does* spatially extrapolate for soil-moisture *regression*
  even though it fails for rare-event hazard *classification* — so the DL/physics split should be
  stage-dependent.
- **Generalization / cross-region (#18, A2/A14).** 1906.01379 (ImageNet-pretrained features
  **transfer poorly to SAR**) warns that optical-lineage EO foundation models may underperform on
  TRINETRA's core Sentinel-1 SAR branch → SAR-specific pretraining / domain adaptation needed;
  2512.05140 (FlowEO generative UDA) and the earlier UDA benchmarks give the adaptation path for
  new catchments without labels. 2509.10362 (**GNN + r-Pareto EVT** risk-zoning on IMERG — exactly
  TRINETRA's GPM input) couples ML with extreme-value theory for the nonstationary monsoon rainfall
  tail that drives the I–D thresholds (#15) — a principled replacement for fixed thresholds.
- **Granular-flow runout (A11).** 2305.05218 (GNN granular-flow surrogate) + 2401.13695
  (differentiable GNS inverse) are a fast forward+inverse pair that could upgrade the empirical
  Scheidegger/Froehlich runout to a cheap physics-learned emulator for people-at-risk.
- **Distributed IoT learning (#8, A10).** 2602.24209 (unsupervised FL for *heterogeneous* IoT) +
  FedIoT (SenSys 2021) show federated, bandwidth-light, label-free anomaly learning across the
  node field — fits the storm-brownout/narrow-LoRa constraint of #8 and adds cross-node consistency
  as a partial sensor-fault-vs-event discriminator (candidate #11).

**Net effect on priorities (231-paper checkpoint):** The catalogue is firmly converging — waves
29–32 produced **no new distinct failure mode**, only sharper fixes and, critically, **hard
external numbers** (2608.12422 + 2510.10799) that elevate #11 and #18 from "flagged" to
"quantified, with a mandated remedy": *every headline performance claim must be re-run under
tile-withheld spatial cross-validation against a gradient-boosted / decision-tree baseline.*
Moderate axes A5 and A12 are now well-covered; A4 (unsaturated-soil Richards numerics) remains the
thinnest axis and is the top target for the final harvest waves.

## Wave 33–34 integration (papers 231→250 — FLOOR CLEARED, harvest closed)
Final harvest filled the two thinnest axes (A4 Richards/ID-thresholds, A5 OPE/policy-selection) and
added decision-layer robustness primitives (selective classification, adaptive conformal, change-point
monitors, test-time adaptation). **No new distinct failure mode emerged** — the 9-surface catalogue is
fully converged. The dominant theme of this span is *honesty guardrails on our own recommended fixes*.

- **A4 physics backbone completed (#2/#3/#15/#17).** 2105.13133 (meshless-RBF + Kirchhoff + Picard)
  and 1507.07837 (iterative linearization of the degenerate elliptic-parabolic Richards eqn) establish
  that the rainfall-infiltration→pore-pressure path TRINETRA leans on is **numerically delicate** —
  the analytic Iverson shortcut papers over strong nonlinearity. **2106.15119 (hybrid
  stochastic-mechanical ID thresholds)** is the capstone for bug #15: it derives I–D thresholds from
  physics with parameters as *correlated aleatory variables*, proving the threshold is a **distribution
  controlled by local Ks, slope, suction, γ_d** — a single borrowed Caine/Dahal/Garhwal constant is
  physically unjustified. 2107.07687 (**AD-EnKF**) supplies the data-assimilation backbone to fuse
  sensor streams into the physics state while *learning* the dynamics the Iverson/Richards model gets
  wrong — unifying physics + data instead of running them side-by-side.
- **Decision-layer: abstention + honest coverage (#13, candidate #6/#12).** 2405.11533 (hierarchical
  selective classification = abstain by *coarsening* the alarm level) and 2406.04745 (CCL-SC
  feature-level selective bound) give an **ordinal abstain** mechanism (Green<Yellow<Orange<Red): under
  uncertainty, back off one level rather than mis-fire. 2601.18509 (CP-for-time-series survey) + 2202.07282
  (**ACI/AgACI** adaptive conformal) directly fix the conformal overclaim #13 — vanilla split-conformal
  coverage is *invalid* on temporally-dependent, drifting sensor streams; online-adaptive CP restores
  honest long-run coverage. **Crucial counter-balance: 2402.09056 (ICML'24) proves evidential-DL
  epistemic uncertainty is only *relative*, hard to optimize** — so EDL (which I had recommended) must
  NOT be trusted as absolute alarm probabilities; use EDL for ranking/OOD, back thresholds with
  conformal. This prevents trading one overclaim (#13 conformal) for another (over-trusted EDL).
- **Drift / regime-shift monitoring (candidate #5/#11, A14).** 2201.07125 (**WATCH** Wasserstein CPD)
  + 2602.07252 (distribution-*shape* online CPD) are unsupervised triggers to detect when the input
  distribution has shifted enough to warrant recalibration/conformal-reset or to separate slow drift
  from an abrupt real event. 2205.13723 (**DLTTA** per-sample test-time adaptation) is a label-free
  online-adaptation recipe for new catchments/seasons — **with the explicit safety caveat that
  unbounded TTA can drift a safety model, so adaptation must be bounded + monitored by the CPDs.**
- **Honest policy valuation closed (#9, A5).** 2110.14000 (**BVFT** hyperparameter-free policy
  selection, NeurIPS'21) + 2311.18206 (**SCOPE-RL** OPE/OPS library with full reward-*distribution* and
  risk-return evaluation) complete the offline-RL honesty toolkit begun with 2106.08909 + 2206.02000:
  TRINETRA can now *select* and *risk-evaluate* the alarm policy on logged data (tail/worst-case value,
  not mean return — essential when miss cost = −100) instead of reporting training-env PPO reward.
- **Rainfall nowcasting + scope gaps.** 2210.12853 (**ASOC**: attentive fusion of sparse ground
  stations with radar, **+5.7% CSI on heavy rain at 1–6 h lead**) is direct evidence that TRINETRA's
  sparse-IoT + GPM fusion can measurably improve the exact lead-time window driving flash-flood warnings
  (partial mitigation of candidate #7 rainfall-forecast spatial error). 2102.06491 (ML rockfall
  detection from TLS, extreme imbalance) flags a **coverage gap**: rockfall (rigid-block detachment) is
  a distinct Himalayan road hazard the Iverson/TRIGRS saturated-slope stack does not model.

**Net effect on priorities (250-paper checkpoint, harvest CLOSED):** SOTA-sufficiency reached across
all 14 axes. The literature program yields **nine failure surfaces, 19 concrete findings, and 14
cross-cutting risk candidates**, every one now backed by ≥1 verified external paper (abstract-opened,
real DOI/arXiv ID). Two findings carry **hard external numbers** (spatial-CV AUC collapse 0.9→0.54 and
"simple beats deep", from 2608.12422 + 2510.10799 + 2106.08909). The single most important standing
remedy is unchanged and now over-determined by evidence: **every headline performance claim must be
re-run under tile-withheld spatial cross-validation against a gradient-boosted / decision-tree baseline,
with a persistence baseline for the forecasting head (2509.18176).** Proceeding to Phase 4: fold all 19
findings + 14 candidates into the Bug Report with their now-attached citations, then Phase 5 fixes/tests
and the WS1–WS7 workstreams.

<!-- ================================================================================= -->
<!-- APPEND-ONLY BOUNDARY. Everything above (lines 1–546) is the PRE-PROGRAM, ABS-era   -->
<!-- synthesis and is preserved VERBATIM per MASTER_PROMPT §0.3. The section below is   -->
<!-- the PROGRAM-ERA (P4) synthesis built on full-text / FT-PARTIAL reads. Do not edit  -->
<!-- the legacy section; this section supersedes it where they conflict.                -->
<!-- ================================================================================= -->

# ============================================================================
# PROGRAM-ERA SYNTHESIS (Phase P4, 2026-10-07)
# Built on 76 deep NEW reads (P1 15 + P2 18 + P3 43) + 15 P4 quota reads = 91
# program-era deep reads, all FT/FT-PARTIAL (Tier-2+), on top of the 235-paper
# ABS baseline. Every claim below traces to a note with a table/equation/page
# ref via analysis/02_paper_ledger.csv and PROGRAM/logs/P4_reading_progress.md.
# ============================================================================

## P4.0 How to read this section
Each consensus position is labelled **C-nn** (same IDs as PROGRAM/sota/P4_sota_scan.md),
carries an **evidence-strength** (OVER-DETERMINED / STRONG / SUPPORTED / THIN), a
**transferability** verdict to Himalayan conditions, and the **workstream(s)** it drives.
"Our system" claims are forbidden until built (Rule 16); process targets only.

## P4.1 CLUSTER BY THEME

### Theme A — Evaluation integrity (the spine of the whole project)
- **C-01 Spatial leakage / spatial-CV — OVER-DETERMINED, now PROVEN.**
  `2610.08227` (TGRS 2026) supplies a finite-sample theorem: a spatially-correlated image of range
  r has effective sample size Θ(n²/r²), not n²; a random holdout underestimates CI width by a factor
  ∝ r; a block holdout needs separation g = Θ(r·log(n/δ)). Empirically corroborated for OUR hazards by
  `2608.12422` (589 HMAGLOFDB outbursts: naive terrain AUC ~0.9 collapses to matched-honest 0.76/0.71/0.54)
  and `2509.18176` (baselines default to persistence). → **Build rule:** every headline number is run
  under tile-withheld spatial-CV with buffer ≥ estimated correlation range; any random-split figure is
  flagged optimistic by a quantifiable factor. Drives ALL workstreams; owned by WS6/P14.
- **C-02 Parsimony (DL does not reliably beat GBDT/simple) — OVER-DETERMINED.**
  Six-domain pattern + `2608.12422` (5 DL models do NOT beat a gradient-boosted baseline; a 3-rule tree
  reproduces the lake-hazard baseline) + Indian-conditions `2609.36975` (XGBoost 78.82% > DL 64–66%,
  Punjab) and `2608.19672` (SAGE-XGBoost +33pp under data scarcity). The ONLY reliable DL win is a
  **learned residual on a mechanistic/temporal backbone** (→ C-03), never from scratch. Drives WS1/WS8.
- **C-14 Cost-sensitive metric selection — SUPPORTED/formalized.**
  `2510.22016` makes Total Classification Cost the ideal selection criterion and shows metric value is a
  function of base rate (never rank models across imbalance ratios by F1/AUC). → **Primary metric = a
  cost-loss Value Score** (miss cost ≫ FA cost; p* = C_FA/(C_FA+C_miss) = 0.0476), costs elicited from
  CWC/IMD/NDMA experts, not assumed. Drives WS6/P14 + every gate.
- **C-10 RL evaluation hygiene — STRONG.** `2610.03369` (≥100 seeds + tail/dispersion + two-baseline)
  + `2608.08158` (PBRS optimality theorem and its limits) + `2609.34041` (a headline catastrophe-rate
  drop 31.6→19.4% with NO evidence of anticipation — architectural "fixes" can be mechanistically hollow).
  Drives WS5/P15.

### Theme B — The forecasting/WHEN layer
- **C-03 Bounded residual on a mechanistic backbone — OVER-DETERMINED (THREAD I, now 7×).**
  MW-Nowcast `2609.34836`, DRUM `2412.11942`(ABS), Nowcasting-Nets `2108.06868`(ABS), TREA-Net
  `2607.26854`, exPreCast-ENS `2608.30205`, **+ `2509.18176` (InSAR CNN-LSTM beats persistence)**,
  **+ `2507.15614` (Geo-FNO surrogate of HEC-RAS, 3.5× cheaper ensembles)**, **+ `2407.06785` (PINN
  Newmark constraint on a DL backbone)**. → GMF uses a **bounded-residual head** on a physics/mechanistic +
  stacking backbone; never free regression. Drives WS1/WS8/P9/P10/P14.
- **C-06 EVT / tail-risk — RESOLVED (2 independent sources).** `2509.10362` (GNN-rP, r-Pareto POT on
  IMERG) + `2510.12328` (Physics-Informed GAT + season-aware GPD/POT, competitive with SEAS5). → the
  WHEN layer + people-at-risk estimate carry an **explicit tail model as a wide-uncertainty PRIOR**, never
  a hard threshold; it is a zoning/strategic tool, not the real-time alarm. CAVEAT: unstable with few
  exceedances in data-sparse mountains. Drives WS1/P9/P14. `2609.16707` corroborates "models lag at the
  very extremes."
- **C-07 SAR-first for cloud — STRONG.** `2608.11142` + `2512.24117` (Himalayan GLOF S1 pipeline, IoU
  0.9130) + routing paper `2608.15261`. Bi-temporal change over single-pass. SAR foundation models
  (`2504.03166` RingMoE, TerraMind, Copernicus-FM) parked to **P7**. Drives WS8/P7/P8.

### Theme C — Uncertainty, decision, calibration (the alarm stack)
- **C-04 Alarm stack = ensemble → decision/action-loss calibration → cost-loss threshold — RESOLVED.**
  `2608.30205` provides the predictive distribution; `2609.14821` shows action-loss coverage ≠ predictive
  coverage (84.9% vs nominal 90%) and that utility-aware calibration restores it (regret −23.4%* under
  asymmetric loss, *FT-PARTIAL body number — re-verify vs PDF before load-bearing use); `2606.21773` (DFL)
  consolidates "better prediction ≠ better decision." Drives WS3/WS5/P13/P15.
- **C-05 Conformal is approximate-under-stability + must be action-loss AND mask-conditional — RESOLVED.**
  `2512.14221` (mask-conditional valid CP under general missingness) + `2610.02777` (PID-Expert online CP,
  narrower intervals under abrupt shift) + `2609.14821` (action-loss coverage). → GMF conformal layer:
  per-zone Mondrian, **conditioned on the present-sensor mask**, calibrated to the alarm action loss,
  updated online, reporting BOTH predictive and action-loss coverage. Drives WS6/P14/P14Z.
- **C-13 Proximity-bias overconfidence in sparse/OOD regions — SUPPORTED (post-hoc fix found).**
  `2610.01384` CLEAR: post-hoc on a frozen evidential model, conflict-aware evidence scaling
  s(x)=exp(−δ·C(x)), +8.29/+5.01 OOD/adv AUROC, 17.4× faster; temp-scaling does NOT fix this. Drives WS6/WS8.

### Theme D — Multimodal robustness
- **C-08 Missing modality is adversarial, not random — STRONG.** `2605.06643` MMDG-Bench (all methods
  degrade), `2609.15297` (worst-case threat model), `2607.24683` Co4Miss (co-learning fix), **+ `2608.15261`
  (negative cross-modal transfer; route each modality by learned task-utility BEFORE first mixing;
  missing-modality mAP +7.6..41.6pt)**, **+ `2610.03649` (SSL encoder → classical-anomaly stack, edge-feasible)**.
  → GMF gates sensor contributions by learned utility; evaluated by dropping the k MOST-informative
  modalities; physics shield is the floor. Drives WS6/WS8/P14.

### Theme E — Physics & the WHO/where layer
- **C-15 Physics FoS is a GATE, not a calibrated probability — STRONG.** `2610.04828` + `2407.06785`
  (PINN embeds Newmark physics as a constraint, outputs geotechnical maps). → infinite-slope/TRIGRS/Iverson
  FoS enters the GMF as a hard monotone shield/gate, not a probability to be regressed. Drives WS1/P7.

### Theme F — Human factors, life-safety, assurance
- **C-12 Cry-wolf / alert fatigue — THIN but quantified.** `2109.07745` (Kincade: 46% evacuation
  compliance in warning/order zones; >50% self+shadow evacuees). Reward must cost FA > a flat penalty.
  Still only one hazard-domain number (older cs.CY); the compliance literature is non-arXiv (NHESS/IJDRR)
  → carried OPEN to P13/P15 via D-010. Drives WS3/WS5.
- **C-16 Low-trust advisory + assurance — SUPPORTED (hard life-safety anchor).** `2608.14391` RA-Bench:
  NO deepfake-video detector family (traditional / zero-shot MLLM / fine-tuned) generalizes on crisis
  content; dissemination worsens detection; human-deceptive clips also fool detectors. → zero-shot /
  crowd / social / deepfake signals are LOW-TRUST advisory inputs into GMF+conformal+shield, NEVER an
  autonomous alarm (Rule 19). Drives WS2/P11 + every alarm gate.
- **C-11 Decision layer may not need RL — RESOLVED.** `2606.21773` (DFL can beat a bigger stack with the
  right decision loss) + `2107.11003` (use offline/iterative RL ONLY if OPE is feasible; FQE ranks policies
  but is compute-heavy). → staged policy: fixed threshold → one-step offline RL → iterative only if OPE-feasible. Drives WS5/P15.
- **C-09 GMF is a COMPOSITION, not an invention — STRONG (honest reframing).** stacking (Wolpert) +
  bounded residual (THREAD I) + per-zone Mondrian conformal + monotone physics shield. Drives P14.

## P4.2 CLUSTER BY PROJECT COMPONENT (workstream → the papers that drive it)
- **WS1 physics (P7):** 2407.06785 (PINN/Newmark), 2507.15614 (HEC-RAS surrogate), 2610.04828 (FoS gate),
  2509.10362 + 2510.12328 (EVT). 
- **WS2 deepfake/misinfo (P11):** 2608.14391 (RA-Bench — detectors fail), 2604.24404/2610.04151/2512.14683
  (assurance), + ABS crisis-social sets (populate in P5).
- **WS3 alerting (P3/P13/P15):** 2608.30205 → 2609.14821 → cost-loss p*; 2109.07745 (compliance).
- **WS4 CCTV / River-Eye (P8):** SAR/optical perception refs; LSPIV (P6 BOM).
- **WS5 RL alarm policy (P15):** 2610.03369 (eval), 2608.08158 (PBRS), 2606.21773/2107.11003 (C-11),
  2110.15332 (OPE confounding caveat), 2609.34041 (hollow-safety caveat).
- **WS6 robustness/calibration (P14):** 2610.08227 (spatial-CV theorem), 2512.14221 (mask-conditional CP),
  2610.02777 (online CP), 2609.14821 (action-loss), 2610.01384 (CLEAR), 2510.22016 (cost metric),
  2605.06643/2609.15297/2607.24683/2608.15261 (missing modality).
- **WS7 IoT/LoRa (P6):** 2508.15058/2311.01743 (SF/airtime/collision), 2412.04563 (Indian LoRa) — P6.
- **WS8 anomaly (P9/P10):** 2512.24117 (GLOF S1), 2509.18176 (InSAR forecast), 2610.03649 (SSL→iForest/OCSVM/LOF),
  2502.15901/2605.31155 (TS-OOD), 2609.34836 (nowcast residual).

## P4.3 CONSENSUS vs DISAGREEMENT MAP
- **Consensus (corpus agrees):** spatial-CV mandatory (C-01); parsimony (C-02); residual-on-backbone (C-03);
  cost-sensitive evaluation (C-14); missing-modality is adversarial (C-08); physics-as-gate (C-15);
  low-trust advisory for media/crowd (C-16).
- **Live tension 1 — "do foundation models help us?"** `2610.07232` says a TSFM (Chronos-2) is SOTA zero-shot
  ONLY when covariates are accurate and DEGRADES under covariate noise, while TimesNet (train-from-scratch)
  is more robust under severe covariate uncertainty. Our monsoon covariates are noisy → **FMs are a prior to
  be stress-tested, not a default** (feeds P14Z). This is the one place C-02 (parsimony) and the FM hype meet;
  the corpus leans parsimony for OUR regime.
- **Live tension 2 — RL vs decision-focused learning.** C-10/C-11: the field increasingly says a well-posed
  decision loss (DFL) or one-step offline RL can match a full RL stack at far lower risk; iterative RL only
  if OPE-feasible. We adopt the staged ladder, not RL-first.
- **No open contradiction remains unresolved** except C-12 thinness (human-compliance numbers) — see gaps.

## P4.4 TECHNIQUES THE FIELD SHOWS WORK BETTER THAN WHAT WE CURRENTLY PLAN
(evidence strength / transferability in brackets)
1. **Mask-conditional weighted conformal** (2512.14221) over plain split-conformal [STRONG / HIGH — stat method].
2. **Online PID-Expert conformal aggregation** (2610.02777) over a single fixed conformal calibrator under
   abrupt monsoon shifts [STRONG / HIGH].
3. **Decision/utility-aware calibration** (2609.14821) over predictive-only calibration [STRONG / HIGH].
4. **Task-utility routing before fusion** (2608.15261) over naive concatenation/attention fusion [STRONG / MED —
   derived for detection, re-derive for regression].
5. **Post-hoc conflict-aware evidence scaling CLEAR** (2610.01384) over temperature scaling for OOD/sparse [SUPPORTED / MED].
6. **PINN physics-constraint head** (2407.06785) over free susceptibility regression [SUPPORTED / MED — coseismic→borrow structure].
7. **Geo-FNO physics surrogate for cheap ensembles** (2507.15614) over running the full solver [SUPPORTED / MED — large-river→adapt].
8. **DFL / SPO decision loss** (2606.21773) over MSE-then-threshold [STRONG / HIGH — doctrine].
9. **OPE-gated policy selection (FQE)** (2107.11003) over trusting training-env reward [STRONG / HIGH].

## P4.5 GAPS
### (a) What we plan that nothing in the corpus yet validates
- **G1 Offline-first edge GMF on Himalayan multi-hazard under spatial-CV** — no external paper validates the
  full composition on OUR geography; this is the PROCESS target to prove (Rule 16), not a claim.
- **G2 Cross-zone conformal with upstream→downstream dependence** — 2509.10362 hints at a spatial graph; no
  paper validates per-zone Mondrian conformal WITH hydrological coupling. Open research item for P14.
- **G3 ₹2,000 River-Eye LSPIV accuracy vs a gauge** — no cited paper on sub-₹2k camera-LSPIV skill; P6/P8.
- **G4 Human-compliance model for the RL reward** — C-12 thin; need NHESS/IJDRR evidence (non-arXiv), P13/P15.
### (b) What the field validated that we do NOT currently plan
- **G5 Explicit EVT tail head** — now adopted (C-06); add to P14 WHEN layer design.
- **G6 Negative cross-modal transfer / utility routing** — adopt into GMF (C-08); add to P14.
- **G7 Rockfall (rigid-block) hazard** — flagged in legacy §; Iverson/TRIGRS does not model it; coverage gap, P7.
- **G8 Covariate-uncertainty-robust forecasting** — 2610.07232 says our noisy covariates may break a TSFM;
  must benchmark a robust from-scratch model as a baseline in P14Z.

## P4.6 TRACEABILITY STATEMENT
Every C-nn above cites arXiv IDs present in analysis/02_paper_ledger.csv with a per-paper takeaway containing
the table/equation/page anchor; the 15 P4 quota reads are itemized in PROGRAM/logs/P4_reading_progress.md with
depth labels and consensus ties. One number is explicitly flagged as FT-PARTIAL-pending-PDF: the −23.4%
extreme-precip regret in 2609.14821 (Audit #9 honesty flag) — not to be used load-bearingly until re-verified.
