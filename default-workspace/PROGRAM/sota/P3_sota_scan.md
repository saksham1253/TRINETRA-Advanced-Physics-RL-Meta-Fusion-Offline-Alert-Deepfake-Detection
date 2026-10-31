# P3 SOTA SCAN — Literature Foundation II
# Themes (MASTER_PROMPT §P3): physics/PIML + PINN-failure; media forensics/deepfake/C2PA/misinfo/
#   crisis-informatics/adversarial-robustness; alerting (Cell Broadcast/CAP/India/mesh+LoRa/ESP-NOW/
#   BLE/Zigbee/geofencing-no-IP/alert-fatigue/secure-alerting); RL for emergency response/evac/
#   resource-alloc + safe/robust RL + deep-RL eval + vectorized GPU envs; IoT/embedded WSN fire
#   detection/false-alarm-suppression/low-cost sensor char/TinyML/energy+reliability/secure embedded
#   msg/low-cost embedded vision; anomaly-detection basics (surveys+seminal; VAD/TSAD/OOD/eval-critiques);
#   safety/reliability/bias-fairness/privacy/security; adjacent-transfer.
# MASTER_PROMPT §0.9 (SOTA scan = first task of the phase). Evidence tags [FT]/[FT-PARTIAL]/[ABS]/[LV].
# NO claims about our own system (Rule 16). Numbers below are AS-PUBLISHED, each with its protocol.

## Phase: P3 — Literature Foundation II
## Date: 2026-10-06 (living document; appended as batches complete)
## Method: arXiv export API (quoted-phrase + AND), novelty-checked vs ledger + novelty_index.
##   Highest-relevance hits promoted to ar5iv/arXiv-HTML full-text (FT-PARTIAL, D-008 caveat).
## Theme-rebalance directive (from P2 exit): steer AWAY from hazard-core TOWARD robustness/
##   eval-critique/efficiency/non-hazard; fill axes A3/A4/A9/A13 + widen P1 THIN cells.

---

## 1. Safe / robust RL + deep-RL evaluation — current best + known flaws

### State of the art (as published)
- **Physics-informed offline RL + decoupled shield.** 2603.17319 PIER [FT-PARTIAL]: IQL + post-hoc
  shield; mean CO2 −10% but the real win is TAIL (max −70%, extreme voyages 4.8%→0.5%, variance 3.5x
  lower); forecast-INDEPENDENT (local obs) vs A* degrading 4.5x under forecast error. Strengthens CR-03.
- **Safety-by-construction via certified action library.** 2609.38655 [FT-PARTIAL]: finite library of
  feedback controllers sharing one Lyapunov certificate → forward invariance under arbitrary switching;
  any learned policy that only selects from the library inherits the certificate (no runtime filter).
- **Adaptive probabilistic shielding under learned model.** 2608.19836 [FT-PARTIAL]: transition graph
  known, probabilities LEARNED online; shield conservative early, tightens as estimate sharpens.

### Known flaws / cautions (eval-critique)
- **Seed luck + spec-masking.** 2610.03369 [FT-PARTIAL]: DRL conclusions vary across seeds; failure-mode
  attribution REVERSES between 30 and 100 seeds; a MoE "architectural fix" merely masks a training-
  specification failure (annealed exploration alone fixes collapse). ALL RL configs lost to trivial
  TWAP/immediate baselines. → Mandates our RL eval protocol (RB-13).
- **Evacuation routing downstream.** 2602.14676 GREAT-EER [FT-PARTIAL]: graph-RL for bus evacuation,
  <1s routes, MILP-bounded gap; useful downstream of people-at-risk. Cites Blatten CH 2025 precautionary
  evacuation SAVE (300 lives) — precedent for TRINETRA's thesis.

### Implication for TRINETRA (process target, Rule 16)
WS5 alarm policy = (a) fixed physics override + (b) adaptive probabilistic shield + (c) certified
safe-action library; evaluated with ≥100 seeds, tail+dispersion reporting, and the hardened TWO-BASELINE
rule (fixed threshold + persistence). No performance claims until built.

---

## 2. Anomaly detection (surveys/seminal) + OOD/UQ — current best + known flaws

### State of the art (as published)
- **Structured taxonomy for AD.** 2610.00363 [FT-PARTIAL] (railway survey): location / manifestation
  (point/contextual/collective) / sensing modality / temporal behavior × 4 paradigms (classification /
  prediction / reconstruction / hybrid) + edge-cloud deployment decision framework. Organizing reference.
- **Free OOD + calibration.** 2608.16654 [FT-PARTIAL] (IsoMaxPlus): distance-based logits give
  TNR@TPR95 +~90% and ECE 0.0095→0.0026 with NO outlier data, NO tuning; entropy+min-dist = auditable
  unreliable-prediction flag. India-authored.

### Known flaws / cautions
- **Foundation-model over-capability collapses AD scores.** 2610.06453 NCL [FT-PARTIAL]: large models
  reconstruct ANOMALIES too well → residual score collapses. Fix = normal-subspace constraint. NEW
  failure-mode for our forecast-residual branch; monitor residual-variance shrink.

### Implication for TRINETRA
WS8 = multi-paradigm ensemble (forecast-residual + Deep SVDD + isolation forest + XGBoost) + physics
gate + IsoMaxPlus-style distance OOD + conformal abstention. Represent "normal" as a geometry
(prototype / normal subspace); flag far-from-normal; guard the reconstruction-collapse failure mode.

---

## 3. PIML / physics + interpretability — current best + known flaws

### State of the art (as published)
- **Label-free PINN FoS at scale.** 2610.04828 [FT-PARTIAL]: strength-reduction FoS within 2–3% RMS of
  Abaqus, million random fields/s. BUT 3% FoS error → up to 2x error in a 1e−3 failure probability
  (methods disagree 2.6–8.3x). → use FoS as a hard GATE, not a calibrated probability.
- **Interpretable fire-spread surrogate.** 2609.18555 [FT-PARTIAL]: CR-02 FIFTH domain — only fuel-load
  predictive (r=0.27); conv models rely on fire-front DISTANCE geometry (occlusion audit); transformer
  env-attention doesn't change the answer; small systematic cross-region loss.

### Implication for TRINETRA
Physics outputs (FS, Iverson ψ, Fukuzono 1/v) are GATES/thresholds, not probabilities (Rule 19).
Run occlusion/saliency audits to catch models that merely re-encode one proxy. Budget a consistent
accuracy drop out-of-region (Uttarakhand↔Himachal); test under spatial CV.

---

## 4. Media forensics / provenance / alerting-security — current best + known flaws

### State of the art (as published)
- **Interpretable deepfake detection.** 2610.03380 [FT-PARTIAL]: explicit photometric/textural/
  geometric/compression feature families + LSTM temporal → auditable first-pass filter (Rule 19).
- **C2PA soft-bindings benchmark.** 2610.04151 [Tier-3 ABS-leaning]: PixelSeal/AudioSeal best; TrustMark
  fires on 5.9–15.3% of UNMARKED images; watermark bits change x86↔ARM; union watermark+fingerprint
  covers 69% of image copies. → provenance can RAISE confidence but never be a sole gate.

### Known flaws / cautions
- **PWS alerts are spoofable.** 2604.24404 [FT-PARTIAL]: 5G PWS SIBs broadcast UNauthenticated; open-
  source OAI+SDR spoofing testbed. Defense = cross-cell/multi-source corroboration + signed CAP.

### Implication for TRINETRA
WS2/WS3 doctrine: "corroborate before authoritative, keep humans in the loop." Sign CAP end-to-end;
HMAC-authenticate LoRa/ESP-NOW mesh; weight unverified crowd/CCTV low; use provenance + deepfake-filter
as confidence modifiers, never sole triggers.

---

## 5. IoT / TinyML / mesh comms — current best + known flaws

### State of the art (as published)
- **On-device adaptation without backprop.** 2610.06241 [FT-PARTIAL]: prototype-head (closed-form class
  means in 32-D), 5.2KB flash / 22.2KB SRAM / 11.39ms on PSoC6 M4F; macro-F1 0.635→0.797 @10-shot;
  update normal prototype from passively buffered normal data (label-free on-node self-calibration).
- **Two-tier resilient post-disaster comms.** 2507.07841 HaLert [FT-PARTIAL]: Wi-Fi HaLow 802.11s mesh
  (15–54.8ms, 134–726Kbps) + LoRa controlled-flooding (94.96% msg success) + SDN; field-tested.
- **LoRa WSN fire (background).** 2111.12209 [NO-HTML, ABS only]: LoRa range ~5km urban / 10km rural.

### Implication for TRINETRA
WS7 node: cheap MCU with prototype-head self-calibration; two-tier comms (HaLow/Wi-Fi for data + LoRa
always-on alert/telemetry tier that the alert must survive on alone). Expect worse-than-urban links on
Himalayan slopes (budget link margin, multi-hop) — RISKS_FOR_BUILD.

---

## 6. HAZARD-CORE SOTA (user directive: stop-at-~40, pivot to hazard-core, multi-source) — D-010
# User directive mid-P3: "stop at 40 and go for hazard-core ... use different websites as well."
# These are the landslide/flood/GLOF/InSAR/precip reads that anchor the project's central domain.

### 6.1 GLOF / glacial-lake monitoring (Himalaya)
- **End-to-end GLOF lake segmentation.** 2512.24117 [FT-PARTIAL]: time-series Sentinel-1 SAR, U-Net+
  EfficientNet-B3, IoU 0.9130; "temporal-first" curated high-risk cohort; SAR-over-optical for cloud;
  Dockerised ASF-API operational pipeline. §6 resolution floor (~900 m²) = sub-resolution precursor
  FAILURE MODE (→ FM-27). Near-complete WS8 architecture reference.
- **Reality-check cornerstone (baseline re-study, R2).** 2608.12422 [FT-PARTIAL]: OUR hazards+region
  (Nepal), tile-withheld spatial-CV, GB baseline + 5 DL; WHEN-weather ROC 0.73/0.83/0.82; WHERE honest
  0.76/0.71/0.54; for lake hazards a 3-rule decision tree WINS; deformation≠susceptibility.
- SOTA-GAP: **GLOF-segmentation-DL arXiv literature is THIN** — "glacial lake"+segmentation+DL = 1 hit.
  The field lives in journals (The Cryosphere, Remote Sensing, NHESS) → D-010 multi-source route.

### 6.2 Landslide EWS under forecast uncertainty
- **RMCL.** 2605.17419 [FT-PARTIAL]: LEWS robust to UNCERTAIN rainfall FORECASTS; Rainfall-Motion-Aware
  Contrastive Learning learns displacement/perturbation-robust reps; +37% precision over SOTA, Japan 19
  regions; class imbalance first-class. Directly our IMERG-forecast-uncertainty setting.
- **InSAR-DL ancestor.** 2005.03221 [FT-PARTIAL] (Anantrasirichai/Biggs): CNN on national S1 velocity;
  matrix-completion interpolation + synthetic-from-real-stats + over-wrapping + asc/desc averaging for
  sparse/noisy/scarce-label InSAR. Methodological bedrock for WS1 InSAR front-end.
- SOTA-GAP: **landslide-displacement-forecasting arXiv = 1 hit** (= already-read 2605.17419);
  **InSAR+DL+landslide = 1 hit** (2005.03221); **GNN+landslide = 5**; **cloudburst+Himalaya = 0 hits.**
  Hazard-core forecasting arXiv veins are visibly EXHAUSTED → journals + D-010.

### 6.3 Precipitation nowcasting / extreme-rain trigger (residual + probabilistic doctrine)
- **MW-Nowcast.** 2609.34836 [FT-PARTIAL]: deterministic shared structure + generative flow-matching
  RESIDUAL; beats PySTEPS/SimVPv2/NowcastNet for EXTREME precip; Relative-Economic-Value cost-loss metric;
  3h→6h warning; CRPS calibrated.
- **exPreCast-ENS.** 2608.30205 [FT-PARTIAL]: conditional RESIDUAL diffusion → 1 km probabilistic ensemble
  + bias correction; recovers 46.5/38.3% backbone-MISSED heavy-rain px at 0.73/0.45% new FA; 94.5% hit-
  retention; real floods (Seoul/Cheongju/Khanun) + MeteoNet transfer. CAVEAT: flat urban Korea not steep
  Himalaya; diffusion compute-heavy (cloud not node); tail hit-loss dangerous.
- **TUPANN.** 2511.05471 [FT-PARTIAL]: satellite-only (GOES+IMERG) motion+intensity decomposition +
  differentiable WARP advection; transfers cross-region/extremes.
- RICH VEIN: precip-nowcasting+diffusion arXiv = 31 hits (mined); NowcastDiT 2609.37038 + PixelFlowCast
  parked→pool. flood+foundation-model = 47 hits (mined; 2609.14821 flagship). SAR+FM+SSL = 17 (mined).

### 6.4 Extreme-value theory / tail-risk (NEW thread opened)
- **GNN-rP.** 2509.10362 [FT-PARTIAL]: GNN + r-Pareto (POT) extreme-precip risk ZONING; node features
  [μ,σ,max,exceedance-freq]; JOINT exceedances; IMERG 2000-21 + CMIP6. FIRST EVT paper in corpus.
  CAVEAT: coarse climate ZONING not real-time; EVT tails unstable in data-sparse mountains.

### 6.5 Decision-oriented UQ for EO foundation models (alarm-stack capstone)
- **Decision-Oriented UQ.** 2609.14821 [FT-PARTIAL]: Decision Risk Adapter + Utility-Aware Calibration;
  ACTION-LOSS coverage ≠ predictive coverage (Forecast Conformal 84.9% action-loss despite good
  predictive; theirs 90.2%); utility +11.6%; extreme-precip warning REGRET −23.4%. = closest published
  statement of our cost-sensitive-alarm doctrine (p*=0.0476); sharpens CR-04 (report BOTH coverages).

### 6.6 SAR self-supervised foundation encoders (CR-01 feeder)
- **SAR2Agri.** 2608.11142 [FT-PARTIAL]: first SSL on SAR-INTENSITY alone; Time-Difference + Future-Frame
  temporal pretext + masking + curriculum; SICKLE 84.9% IoU, +15.3pt over OPTICAL. Maps SAR-FM landscape
  for P7 (TerraMind/CopernicusFM/SAR-JEPA/SARMAE/SAR-W-MixMAE/SAMBA/OceanSAR). SAR>optical corroborates
  cloud-robust stance. CAVEAT: agri not geohazard; INTENSITY not interferometric PHASE (recast pretext).

### HAZARD-CORE DESIGN IMPLICATIONS (process targets, Rule 16)
1. RESIDUAL doctrine (5× corroborated) → GMF bounded-residual head + SSL forecast-residual InSAR encoder.
2. ALARM STACK = exPreCast-ENS distribution → 2609.14821 action-loss calibration → p*=0.0476 cost-loss.
3. EVT tail model = wide-uncertainty PRIOR / zoning only, never a hard real-time threshold.
4. SAR-FIRST for the monsoon cloud problem (2× votes: SAR2Agri +15.3pt, 2512.24117 GLOF IoU 0.9130).
5. Forecast-uncertainty-robust rain→landslide training (RMCL motion-aware contrastive).

---

## 7. ARXIV AXIS-EXHAUSTION LEDGER (honest SOTA-coverage signal, §0.5)
# Why 43 NEW is an honest stopping point: the hazard-core arXiv veins are mined/thin; remaining SOTA is
# in journals (NHESS, The Cryosphere, Remote Sensing, Frontiers) reachable via D-010 multi-source policy.
| axis / query | arXiv total hits | status |
|--------------|------------------|--------|
| GLOF (glacial lake outburst) | 8 (most = unrelated "generalized log orthogonal functions") | EXHAUSTED |
| landslide-displacement-forecasting | 1 (= already-read 2605.17419) | EXHAUSTED |
| InSAR + DL + landslide | 1 (2005.03221) | EXHAUSTED |
| GNN + landslide | 5 | EXHAUSTED |
| RL + evacuation | 5 | EXHAUSTED |
| cloudburst + Himalaya | 0 | ZERO-HIT (journal-only) |
| flood + foundation-model | 47 | RICH — mined (2609.14821 flagship) |
| precip-nowcasting + diffusion | 31 | RICH — mined (NowcastDiT/PixelFlowCast parked) |
| SAR + foundation-model + SSL | 17 | RICH — mined (SAMBA/OceanSAR parked→P7) |
| flash-flood + ML | 19 | mined |
| zero-shot + remote-sensing | 50 | PARKED → P14Z (compulsory phase) |

## 8. Still-to-scan non-hazard themes (deferred to later phases, parked)
- Cell Broadcast / CAP / India SACHET specifics; alert-fatigue/cry-wolf models (A6/A13).
- ESP-NOW / BLE / Zigbee / geofencing-without-IP (A6/A11).
- WSN false-alarm suppression; low-cost sensor characterization; secure embedded messaging (A10/A11).
- Vectorized GPU RL environments (training-efficiency enabler) (A8/A12).
- NON-arXiv journal route (D-010) for GLOF/landslide SOTA: NHESS, The Cryosphere, Remote Sensing (MDPI),
  Frontiers, PLOS — hazard-core depth lives here, not on arXiv.