# 00 — TRINETRA System Model

> Read-only analysis artifact (Phase 1). Describes architecture, data flow, assumptions,
> failure surfaces, external dependencies, and which component derives from which paper.
> Source of truth: `C:\Users\Dell\Downloads\trinetra\deliverables\TRINETRA_Complete_Report.md`
> (v1.0, 2966 lines) plus the `research/` design docs and the 110-paper corpus.

## 1. What the system is
TRINETRA (alt. name HIMKAVACH) is an **offline-first, multi-sensor early-warning system** for
rapid-onset mountain hazards — **landslides, flash-floods, cloudbursts, and GLOFs** — targeting
Uttarakhand + Himachal Pradesh (~110,000 km²). Design priorities: works without continuous
network; cheap ground hardware (~₹2,000/node); physics-grounded + ML; produces calibrated
people-at-risk estimates routed to CAP/SACHET.

## 2. Three fused sensing layers
1. **Satellite / EO**: Sentinel-1 InSAR (C-band, deformation), Sentinel-2 (optical), GPM IMERG
   (precip), SMAP (soil moisture), ERA5-Land (reanalysis), MODIS, ITS_LIVE (glacier velocity).
2. **Opportunistic vision**: existing CCTV + ultra-cheap "River Eye" nodes (~₹2,000) doing
   level/か flow estimation via LSPIV.
3. **Ground IoT**: ~₹2,000 LoRa nodes (tilt, soil moisture, piezometer, rain gauge).

## 3. Processing pipeline (end to end)
```
EO datacube (InSAR core) ──► SSL masked-modeling encoder
                                   │
                                   ▼
   anomaly stack: forecast-residual + Deep SVDD + isolation forest + XGBoost
                                   │
                                   ▼
          physics gate (FS / Iverson transient / Fukuzono / Caine I–D)
                                   │
                                   ▼
             RL alarm policy (4-stage curriculum)
                                   │
                                   ▼
   calibrated people-at-risk  ──►  CAP / SACHET routing  ──►  alert levels
```

## 4. Physics core (equations as used in the report)
- **Infinite-slope / TRIGRS factor of safety**: `FS = Ff + Fw + Fc` (frictional + water + cohesion).
- **Iverson (2000) transient pressure head** ψ(Z,t): base + 2·Σ (I_nz/K_z)·(D1·t)^½ · ierfc[Z/(2(D1 t)^½)]
  with `β = cos²δ − I_zLT/K_z`, `D1 = D0 / cos²δ`. **Slope must enter ONLY through D1** — the report
  adds a spurious extra `cos²β / cos β` on the transient term (Bug #3, double counting).
- **Fukuzono/Voight inverse-velocity**: `1/v = A(α−1)(t_f − t)`, α≈2 (report uses α 1.5–2.2 → Bug #4).
- **Caine rainfall intensity–duration threshold**: `I = a · D^(−b)`.
- **LSPIV** surface velocity for River Eye.
- **Scheidegger runout**; **Froehlich**, **SCS-CN**, **Manning** for flood routing.
- **Bayes optimal alarm threshold**: p* = C_FA/(C_FA + C_miss) = 5/105 = **0.0476**.

## 5. Anomaly + ML detection
- Self-supervised masked-modeling encoder over the InSAR-core datacube (benchmark targets:
  Prithvi-EO-2.0, TerraMind, Galileo, CROMA, SkySense, SatMAE, Copernicus-FM, AnySat).
- Downstream anomaly: forecast residual + Deep SVDD + isolation forest + XGBoost ensemble.
- Report claims a conformal-prediction "guarantee" (Bug #13 — overclaim; conformal gives marginal
  coverage, not a hard guarantee, and reported 82.9% overall / 45–59% high-risk recall from
  2603.15681 contradicts the "guarantee" language).

## 6. RL alarm policy (4-stage curriculum)
1. Fixed-threshold baseline.
2. LHASA rule (v1/v2, Stanley/Khan — in corpus).
3. Offline RL (CQL 2006.04779 / IQL 2110.06169 / TD3+BC) via d3rlpy.
4. Simulator PPO (SB3).
- **Reward**: miss = −100, false-alarm = −5 (red) / −1 (yellow-orange), lead-time = +2/h capped 12 h,
  disruption = −0.01/person-hour, level-change = −0.5. γ ≈ 0.99/h.
- **Safety shield (hard overrides)**: FS<1 → Orange; tilt>5°/day → Red; 24 h rain>150 mm → Orange;
  GLOF signature → Red. (Shielding = Alshiekh et al. 1708.08611.)
- Report has a reward-sign inversion risk (Bug #9).

## 7. Meta-fusion head (the user's extension)
"Gated Meta-Fusion Decision Head (GMF)": stacked generalization (Wolpert 1992) + residual policy
learning + post-posed shielding + gated MoE. Meta-head consumes raw features + RL action-logits/
q-values → bounded residual over a physics base action a0 → â = clip(a0 + residual) → per-zone
Mondrian conformal → monotone hard shield max(â, S(s)) (can only RAISE the alert). Prior art that
constrains novelty: Meta-AAD (2009.07415), RL model-selection (2205.09884).

## 8. External dependencies / deployment
- Kaggle (25–30 GPU-h budget), d3rlpy, Stable-Baselines3.
- LoRa in India must use **IN865–867 MHz** (report uses 433 MHz → Bug #6, non-ISM for this use).
- `Proxy.py` / `Proxy_fixed.py` forward credentials to a **non-official endpoint**
  `https://api.justwoker.icu` (Bug #12, security).
- Datacube size claimed 2–5 TB but realistic 45–130 TB (Bug #10, 10–35× under-estimate).

## 9. Known failure surfaces (entry points for Phase 4)
- Threshold inconsistency (~10×): report 0.5 vs LHASA 0.12 vs Bayes 0.048 (Bug #1).
- Physics sign/column errors (#2 suction-stress sign, #3 Iverson slope double-count, #4 α range).
- Evidence/benchmark mislabels (#5), edge-latency overclaim (#14, Cerberus 57.7 fps on L40S not Jetson).
- Underpowered eval n≈5 leave-one-event-out (#11).
- Rare-event class imbalance; drift/brownout at inference (#8).
- Missed prior art for novelty (#18): landslide-FM 2511.04474, IceWatch GLOF 2601.12330,
  InSAR precursor 2212.12038.

## 10. Key technical questions this project's correctness depends on
(these drive the Phase-2 search)
1. **InSAR time-series forecasting & precursor detection** — do deep models actually forecast
   slope failure, or only map past failures? Transferability brittle→creep.
2. **EO foundation models / SSL for remote sensing** — SOTA, benchmarks, what beats masked-modeling.
3. **Rainfall I–D thresholds for Himalaya** — real calibrated constants, uncertainty.
4. **Physically-based transient infiltration (Iverson/TRIGRS/Richards)** — correct slope handling.
5. **Offline RL for safety-critical alarms** — distribution shift, conservatism, OPE validity.
6. **Safe RL / shielding / constrained MDP** — correctness of hard overrides.
7. **Conformal prediction & risk control** — what guarantee is actually provable.
8. **Rare-event / imbalanced detection, calibration, early warning verification (CSI/POD/FAR/Brier).**
9. **Video anomaly detection on the edge, LSPIV / image velocimetry for rivers.**
10. **LoRa/LPWAN reliability in mountains, delay-tolerant networking, energy harvesting.**
11. **GLOF / dam-break / debris-flow runout modeling.**
12. **Multimodal / meta / stacked fusion, mixture-of-experts gating, model selection.**
13. **Evacuation / decision models under uncertainty, cost-loss, value of warnings.**
14. **Distribution shift, concept drift, OOD detection, monitoring in deployed ML.**

These 14 questions are the Phase-2 search axes.

---

## 11. P1 ADDENDUM — system-model refinements from baseline re-study (2026-10-05)
> Appended in Phase P1 after re-reading the baseline corpus at Tier-2+ depth (ar5iv/arXiv-HTML).
> Original P0 content above is UNCHANGED (backup: PROGRAM/backups/2026-10-05_pre_program/).
> Every claim here is tagged to a read paper note in analysis/03_paper_notes/. Rule 16: no
> performance claim about OUR system — these are design implications grounded in others' work.

### 11.1 EO encoder (component §5) — the choice is now a 4-way trade study (CR-01)
The report's SSL masked-modeling encoder should be selected, not assumed. Four concrete,
read contenders now anchor CR-01:
- **DINOv2 (2304.07193, FT)** — generic ViT SSL; strong but RGB-generic, not RS-native.
- **CROMA (2311.00566)** — SAR+optical contrastive+MAE; best-matched to our S1+S2 aligned pair.
- **Copernicus-FM (2503.11849)** — any-modality hypernetwork over S1/S2/S3/S5P + metadata.
- **AnySat (2412.14123)** — JEPA + scale-adaptive; native multi-resolution (1.25m–1280m).
Decision rule (ties CR-02 doctrine): every high-complexity encoder must beat a plain-ViT +
gradient-boosted baseline under IDENTICAL tile-withheld spatial-CV before adoption. SSL data
volume can stop at the ~750K-patch knee (2211.07044 saturation) to respect the Kaggle budget.

### 11.2 Precipitation layer (§2.1, §4 Caine I–D) — a critical new failure surface
Naive DL merging of IMERG+radar over complex terrain can UNDERESTIMATE rainfall and collapse to
near-zero (2404.10135) → missed rain-triggered alarm (worst error). Recorded as **FM-17**.
Implications: (a) multi-source precip (add ERA5-Land covariates), never IMERG-only; (b) MANDATORY
bias-correction against local LoRa rain-gauge nodes → a concrete cross-layer dependency (WS7
ground gauges calibrate WS1 satellite precip); (c) use IMERG for TIMING/trend features, treat
absolute Caine I–D intensity thresholds with local-calibration caution.

### 11.3 Anomaly stack (§5) — AE over-generalization failure, miss-averse design
Reconstruction-based anomaly heads can "generalize" and reconstruct true anomalies as normal →
missed detection (**FM-18**; 1904.02639 MemAE, used inside 2108.06852 HF²-VAD). For a miss-averse
EWS (reward miss=−100), prefer memory-prototype-constrained / miss-biased scoring. Applies to
BOTH video (WS4) and the InSAR forecast-residual head (WS1).

### 11.4 Physics gate (§4) — hybrid-physics template + GLOF hydrograph + precursor metrics
- **PIML template (2104.11009, IIT-GN, Narmada):** couple conceptual process models with ML +
  a water-balance consistency check; UQ on intermediate variables. Caution the authors stress:
  "physics that doesn't improve prediction may be deceptive" and MORE calibration constraints
  can HURT → disciplines the physics gate (must earn skill under CV; ties CR-02).
- **GLOF/dam-break (1806.05035):** probabilistic breach-enlargement model + Bayesian/MCMC UQ →
  prediction INTERVALS for outflow hydrograph (not a point) feeding people-at-risk; concentrate
  calibration on erosion-rate + residual terms. Moraine-dam caveat (ice core, scale) flagged.
- **Precursor metrics:** complement Fukuzono/Voight 1/v (E-04; real geodetic application
  2007.02756, Voight co-author) with a SPATIAL precursor — InSAR "community persistence" rising
  weeks pre-failure (2212.12038, slope×deformation edge weights) and dense-coverage estimation
  (2311.01564). FFM α range (Bug #4) to be re-derived in P7.

### 11.5 Ground segment (§2.3, §8) — energy + comms are co-primary design axes
- **LoRa in mountains (2412.04563, rural Nepal):** best terrain-matched evidence; sweep BW/SF/CR,
  mesh topology, antenna gain; obtain recommended params (PDF, P6). Confirms IN865–867 band fix
  (Bug #6) must be verified vs Indian regulation.
- **Energy (2010.14934 profiling; 2307.04016 LTE+solar, 33k h winter data-loss; 1909.01968 ACES
  RL duty-cycling, −33%):** camera + comms dominate energy; task-by-task energy budget is a
  requirement; winter/monsoon solar gaps WORSE than temperate studies → oversize power, treat
  node outage + missing inputs as expected (ties FM-10, FM-15, CR-04). On-node compute = light
  tinyML pre-filter only (2106.10652 ESP32); heavy inference stays at gateway/cloud.
- **Ultra-cheap sensing option:** passive RFID (2112.11965) gives cm-level displacement /
  tilt / snowpack at 10–100× lower cost than active nodes — candidate for slow-variable
  baselining (NOT real-time alarms; needs a reader pass → latency).

### 11.6 Evaluation doctrine (cross-cutting) — the single most load-bearing P1 finding
Under honest matched spatial-CV, deep models often do NOT beat persistence / gradient-boosted /
3-rule-tree baselines (2608.12422; reinforced by 2201.06837 interpretable SNN matching DNNs in
our region, 2204.06097 RF/Bagging best-of-9, and realistic landslide-seg F1 ~56–73% in
2206.00515). **Mandatory baselines gate every deep-model claim.** Spatial leakage inflates skill
(AUC 0.9→0.54; FM-01). This governs §5, §6, §11.1, and the P19 contribution claim.

### 11.7 RL alarm policy (§6) — prefer simple first (CR-03)
One-step offline RL often beats iterative on small/narrow-coverage data (2106.08909) and TD3+BC
parsimony is strong (2106.06860) → benchmark a one-step/offline baseline BEFORE committing to the
4-stage CQL/IQL→PPO curriculum; escalate only with proven data coverage. Always behind the
post-posed safety shield (1708.08611), which provably preserves convergence and satisfies Rule 19.
Node-level energy control can use simple tabular Q-learning (1909.01968, HP-01) — reserve
deep/offline RL for the harder alarm decision only.

