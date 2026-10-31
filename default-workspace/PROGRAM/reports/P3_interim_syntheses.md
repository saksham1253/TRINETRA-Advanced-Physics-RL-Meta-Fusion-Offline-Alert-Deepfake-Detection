# P3 INTERIM SYNTHESES — Literature Foundation II
# MASTER_PROMPT §0.9 (interim synthesis every ~5 batches). Living doc. NO claims about our own
# system performance (Rule 16). All numbers AS-PUBLISHED with their protocol.

## Status at this synthesis
- P3 deep reads so far (updated 2026-10-07): **43** NEW FT-PARTIAL Tier-2 (stop-at-~40 target per D-010
  PASSED; continued opportunistically on outstanding/SOTA hits per user instruction 2026-10-07).
  (Synthesis #2 at 30; #3 below covers reads 37–43: 2605.17419 RMCL displacement-robust LEWS, 2512.24117
  SAR GLOF seg, 2607.26854 TREA-Net residual+zero-shot, 2609.14821 Decision-Oriented UQ, 2608.30205
  exPreCast-ENS residual-diffusion, 2608.11142 SAR2Agri SSL, 2509.10362 GNN-rP EVT tail-risk.)
- NON-QUOTA baseline re-studies (OQ-02, ABS→FT-PARTIAL): 2606.16795 WaveDINO, 2608.12422 "Which Site and When".
- NOT counted: 2610.04151 (Tier-3); NO-HTML/ABS-only non-quota: 2111.12209, 2601.07268, 2512.17785,
  2601.12330, 2402.17069, 2412.11942 (DRUM), 2510.10546 (GLOFNet), 2108.06868 (Nowcasting-Nets),
  2608.19672 (SAGE-XGBoost).
- Running program-era NEW deep-read total = P1(15) + P2(18) + P3(43) = **76**.
- Theme balance this phase (updated): safe/robust-RL (6), anomaly/OOD/UQ (7), SSL/encoder (3: WinoTS +
  WaveDINO-restudy + SAR2Agri), media/alerting/comms (4), IoT/TinyML (1), fairness/governance (1),
  crisis-informatics (1), eval-critique (3), PIML (1), wildfire interp (1), privacy/DP (1), low-cost
  sensing (1), precursor/seismic-AE (1), precip-nowcasting (3: MW-Nowcast + exPreCast-ENS + prior),
  InSAR/SAR hazard (4: Rouet-Leduc + Anantrasirichai + SAR-GLOF-seg + SAR2Agri), decision-oriented-UQ (1),
  landslide-EWS-operational (1 RMCL), transfer/residual-forecasting (1 TREA-Net), EVT/tail-risk (1 GNN-rP),
  multimodal-missing (1), GLOF-reality-check (1 restudy).

---

## SYNTHESIS #1 (after P3 batch of ~22 reads) — 2026-10-06

### Thread A — "Represent NORMAL as an explicit geometry; flag far-from / moving-wrong" (WS8)
Now a **six-member cluster**, the strongest emergent P3 theme:
- 2610.06241 prototype-head (closed-form class means, on-device, no backprop)
- 2610.06453 NCL normal-subspace (few-shot SVD constraint)
- 2608.16654 IsoMaxPlus distance-to-prototype logits (free OOD + calibration)
- 2608.06876 FedVAR federated GLOBAL normality prototype (agree on "normal" across nodes)
- 2605.23504 VACE Mahalanobis positional × velocity-bank directional manifold
- 2609.39337 WinoTS SSL (wavelet self-distillation) to LEARN the representation the geometry lives in
**WS8 doctrine crystallized:** learn a tight normal manifold with an explicit distance metric; combine
a POSITIONAL score (how far from normal) with a DIRECTIONAL/DYNAMIC score (is it moving atypically —
fits creep→acceleration, river-stage rise-rate, Fukuzono 1/v). Represent via prototype/subspace;
federate so zones AGREE on "normal" (FedVAR) instead of each drifting to idiosyncratic normal; entropy
+ min-distance = auditable "unreliable prediction" flag. GUARD: NCL failure (FM-23) — over-capable
reconstruction/forecast models reconstruct anomalies too well → residual score collapses; monitor
residual-variance shrink; always keep a model-free detector + physics gate.

### Thread B — Safe/robust RL = THREE patterns + eval discipline + correct threat model (WS5)
Design = COMPOSITION (our novelty claim is the composition, not any single part):
1. Hard physics override / shield (Alshiekh 1708.08611; PIER 2603.17319 forecast-INDEPENDENT, kills tail)
2. Adaptive probabilistic shield w/ learned MDP (2608.19836, conservative→tightens as calibrated)
3. Safety-by-construction certified-action library / forward-invariant policy class (2609.38655)
Eval discipline (RB-13, from 2610.03369): ≥100 seeds; report TAIL + across-seed dispersion not mean;
ablate training-spec (exploration/reward) BEFORE crediting architecture; always vs trivial baselines.
Adversarial robustness (RB-18, from 2609.31142 JevAdvBench): treat the STATE as untrusted argued input;
one injected opinion flips 12.1% of decisions; confidence gate alone insufficient (report escape-rate +
review-load). Correct missing-modality threat model (2609.15297 Admissable): the hazard destroys the
HIGHEST-signal sensor → eval under WORST-CASE (adversarial) missingness, not random dropout; require
safe degradation on remaining local obs.

### Thread C — Media provenance / alerting security / last-mile human factors (WS2/WS3/WS7)
"Corroborate before authoritative, keep humans in loop":
- PWS/cell-broadcast alerts are spoofable (2604.24404; cross-cell verification defense; it is the ONLY
  arXiv cell-broadcast/emergency-alert hit — thin field).
- C2PA soft-bindings false-fire + drift across CPU arch (2610.04151) → provenance = confidence
  modifier, never sole gate.
- Interpretable deepfake first-pass filter (2610.03380) auditable (Rule 19).
- Crisis informatics (2007.05848 #Verificado19S): trust flows through a TRUSTED BRIDGING ORG (SDMA),
  via cross-platform citizen verification; crowd = mobilize/triage channel NOT a hazard sensor
  (reinforces RB-09). Plan for WhatsApp misinformation during the event.
- Resilient offline-first comms (2507.07841 HaLert): TWO-TIER — HaLow/Wi-Fi mesh for data (15–54.8ms,
  134–726Kbps) + LoRa controlled-flood always-on alert tier (94.96% success); expect worse than urban
  on Himalayan slopes (RB-17); the alert must survive on the LoRa tier alone.

### Thread D — Parsimony prior now overwhelming (CR-02, FIVE hazard domains + non-hazard)
GLOF 2608.12422, fire 2610.01994, flood edge-seg 2609.20441, InSAR 2509.18176, wildfire-spread
2609.18555, + TSAD VACE 2605.23504 (simple velocity-geometry beats larger-budget), + RL order-execution
2610.03369 (ALL RL lose to TWAP). Build rule: hardened TWO-BASELINE (fixed rule + persistence) under
tile-withheld spatial CV before any DL/RL claim.

### Thread E — Physics outputs are GATES, not probabilities (WS1, Rule 19)
2610.04828: label-free PINN FoS within 2–3% of Abaqus BUT 3% FoS error → up to 2x failure-probability
error (methods disagree 2.6–8.3x). → use FS/Iverson ψ/Fukuzono 1/v as hard thresholds/gates; report
method-spread; geotechnical expert review (FM-24).

### Thread F — Uncertainty is first-class and HONEST (WS8 UQ, disciplines Bug #13)
Conformal coverage on our streams is approximate-under-stability, NOT hard. Stack = EnbPI (2010.09107)
/ DistMatch (2606.00690, local-exchangeability via residual-matching bins = data-driven Mondrian) base
+ PID-Expert (2610.02777) online width control + drift monitor. Emphasize threshold-free metrics
(VUS-ROC/VUS-PR, Range-F1 — VACE) over Point-F1; final operating point via cost-loss Value Score.

### Thread G — Governance / fairness is a pipeline property, not a post-hoc patch (Rule 19)
2609.38552 Fairness Theatre: output-only fixes on black-box procured EWS can be theatre. → keep the
who-gets-warned stack AUDITABLE; evaluate fairness at per-zone OUTCOME level (miss-rate + alert-rate
disparity), not aggregate accuracy; prefer auditable components in P6 procurement; our "groups" are
geographic communities not demographic classes — flag for ethics/legal expert review.

---

## SYNTHESIS #2 (after P3 reads 23–30) — 2026-10-07
New reads: 2609.27202 (federated TinyML security), 2605.06643 (MMDG-Bench), 2605.01679 (CA-ADP privacy),
2511.20936 (passive LTE water-level), 2203.13313 (labquake AE forecast), 2511.05471 (TUPANN nowcast),
2012.13849 (InSAR denoising-AE). [+2606.00690 DistMatch, 2610.06317 watermark-impossibility from batch-1 tail]

### Thread H — The parsimony/fair-comparison prior is now overwhelming (CR-02 seventh corroborator)
2605.06643 MMDG-Bench (**7,402 networks**, standardized fair comparison) is the single strongest piece:
specialized Multimodal Domain Generalization methods give only **marginal** improvement over plain ERM;
no method consistently wins; **trimodal fusion does NOT consistently beat the best bimodal**. Added to
the 5 hazard-domain + 1 finance corroborators, CR-02 is effectively settled as a WORKING PRIOR, with a
sharpened build rule: **every TRINETRA fusion/model must be reported against ERM/concatenation-fusion +
an oracle upper bound**, and "more modalities" (sat+CCTV+IoT) must EARN its place over a tuned 2-layer
baseline rather than being assumed superior.

### Thread I — "Physics as structure, learner for the residual" recurs across FOUR independent domains
A doctrine now seen in: PINN FoS (2610.04828), passive water-level two-ray model → CWT feature →
lightweight NN (2511.20936), TUPANN motion+intensity decomposition + fixed differentiable WARP advection
(2511.05471), and InSAR atmospheric-noise separation before deformation extraction (2012.13849). Unified
rule for TRINETRA: **do not regress raw targets with a black box — embed the known physics as the model
STRUCTURE (gates, advection operators, channel models, noise models) and let a small learner handle only
the residual.** This simultaneously improves data-efficiency (critical given Kaggle budget + scarce
Himalayan labels), transfer (TUPANN cross-region), and auditability (Rule 19). Directly shapes WS1
(physics gate) and the rainfall/InSAR front-ends.

### Thread J — Weak-precursor extraction from noisy geophysical sensors is a solved PRINCIPLE, with honest onset-timing limits
Rouet-Leduc 2012.13849 (InSAR, autoencoder, 2 mm, no fault prior) + Laurenti 2203.13313 (acoustic
emission ↔ fault stress, AR forecast) — SAME LANL/ENS lineage — jointly establish that ML can pull
mm-scale deformation and stress-precursor signals out of noisy geodetic/acoustic streams UNSUPERVISED.
This underwrites TRINETRA's SSL-InSAR precursor layer AND its forecast-residual anomaly branch. BUT the
crucial honesty hook: Laurenti shows **time-to-ONSET (TTsF) is intrinsically harder to predict the more
gradual-creep precursor is present**, while time-to-END is easier. Consequence for us: **a long creep
precursor WIDENS onset uncertainty — we must emit a calibrated interval on any t_f estimate (ties
Fukuzono 1/v Bug#4 + conformal width), never a point onset time.** GUARD (ties NCL FM-23): the InSAR AE
must leave genuine deformation in the RESIDUAL, not absorb it — tune reconstruction capacity accordingly.

### Thread K — Privacy is composable and must protect the rare-hazard signal
CA-ADP 2605.01679 adds a formal (ε,δ)-DP mechanism to the human-adjacent-sensing concern, and composes
with the federated thread (FedVAR 2608.06876, federated TinyML 2609.27202). Transferable gem beyond DP:
**do not drown the rare critical-class signal in UNIFORM privacy noise / regularization / augmentation —
protect the minority-class gradient.** This generalizes our rare-event learning doctrine (cost loss,
class-balanced sampling, importance-sampled rare rain) into a privacy-compatible form, and gives a
concrete deliverable: report the (ε,δ) budget + privacy–utility curve, not an afterthought.

### Thread L — A new survivable low-cost river modality to trade-study
2511.20936 passive LTE-power water-level sensing (commodity receivers, no dedicated probe, survives when
instruments are washed out) is a genuinely new candidate layer for the River-Eye/LoRa stack — flagged
for the P6/P7 sensor trade study, with the strong caveat that the demo is TIDAL (quasi-periodic) and
must be re-validated for impulsive flood surge. Reinforces robust-MEDIAN multi-sensor fusion (ties GMF).

---

## SYNTHESIS #3 (after P3 reads 37–43) — 2026-10-07

### Thread K — The alarm stack is now COMPLETE on paper: forecast → distribution → decision-calibration → cost-loss alarm
Three P3 reads lock the WHEN→alarm pipeline end-to-end, each supplying one stage:
1. **Forecast + probabilistic ensemble:** exPreCast-ENS (2608.30205) — conditional residual DIFFUSION turns
   a cheap deterministic nowcaster into a 1 km probabilistic ensemble + bias correction; its own motivation
   is "extreme precip → flash floods AND landslides". Gives us the predictive DISTRIBUTION.
2. **Decision-oriented calibration:** 2609.14821 — Decision Risk Adapter + Utility-Aware Calibration prove
   that predictive-coverage ≠ ACTION-LOSS coverage (Forecast Conformal 84.9% action-loss despite good
   predictive; theirs 90.2%); extreme-precip warning REGRET −23.4% under asymmetric loss. Calibrate the
   distribution to the DECISION, not the prediction.
3. **Cost-loss alarm threshold:** our existing Bayes p*=C_FA/(C_FA+C_miss)=0.0476 doctrine (bug#1), now
   externally validated as "the closest published statement of our thesis."
→ Build consequence: GMF conformal layer calibrates against the ALARM action loss and the gate reports BOTH
predictive and action-loss coverage. This is a concrete, now-sourced UQ spec for P14/P14Z. (CR-04 sharpened.)

### Thread I (promoted) — RESIDUAL doctrine is now the best-supported design principle (5× independent)
MW-Nowcast, DRUM, Nowcasting-Nets, TREA-Net (2607.26854), exPreCast-ENS (2608.30205) all independently
converge: learn a BOUNDED RESIDUAL / refinement on a deterministic or mechanistic BACKBONE rather than
forecasting from scratch. TREA-Net adds the GATED residual + two-scalar transfer (data-rich→data-scarce,
directly our Himalaya-scarcity problem) + conformal −29.6% width. SAR2Agri (2608.11142) is the SSL analogue
(Time-Difference / Future-Frame temporal pretext). → Our GMF bounded-residual head and SSL forecast-residual
encoder are both now strongly externally supported. Adopt as first-class; validate residual bound on
Himalayan data (Rule 16).

### Thread L — SAR-first for the cloud problem, with a concrete encoder shortlist (CR-01 advanced)
SAR2Agri (2608.11142): SAR beats OPTICAL by +15.3 pt on an all-weather task; SAR-GLOF-seg (2512.24117):
SAR>optical for GLOF (IoU 0.9130). Two more independent votes for SAR-first in the monsoon Himalaya where
optical is cloud-blocked. SAR2Agri also MAPS the encoder trade-study field for P7: TerraMind, Copernicus-FM,
SAR-JEPA, SARMAE, SAR-W-MixMAE (flood-mapping pretraining — closest to our task), SAMBA (Mamba, linear-cost,
edge-budget relevant), OceanSAR. CR-01 shortlist now has named SAR-specific contenders, not just generic/
multimodal FMs.

### Thread J (new) — EVT / tail-risk was a missing axis; now opened
GNN-rP (2509.10362) is the FIRST extreme-value-theory paper in the whole corpus. Our hazards ARE tail
events; everything else modeled the bulk. Reusable: per-cell [μ,σ,max,exceedance-freq] IMERG features on a
catchment spatial graph + peaks-over-threshold r-Pareto tail + JOINT-exceedance (compound correlated
failure). GUARD: EVT tails are high-variance with few exceedances → wide-uncertainty PRIOR / zoning tool,
NEVER a hard real-time threshold. Evaluate in P14 WHEN layer with explicit uncertainty.

### Thread M — operational landslide EWS under FORECAST uncertainty (RMCL)
RMCL (2605.17419): rainfall-field DISPLACEMENT from forecast error degrades landslide prediction; learn
representations STABLE under rainfall-field motion via motion-aware contrastive learning (+37% precision
over SOTA, Japan 19 regions). → Our WHEN layer must be robust to the fact that we feed FORECAST rain (IMERG
nowcast), not observed rain; adopt motion/displacement-robust training for the rain→landslide model. Directly
operational, directly our setting.

### Zero-shot P14Z pre-seeding (parked, not quota)
TiRex (zero-shot time-series FM, strongest baseline in TREA-Net) and OmniRSCLIP (2609.03391, multi-source
SAR/MSI/HSI CLIP, zero-shot classification) now registered in PHASE_BACKLOG for the compulsory P14Z phase.
Early doctrine already forming: zero-shot output is a LOW-TRUST PRIOR best corrected by a lightweight local
residual (TiRex alone < TiRex+TREA-Net), never an autonomous alarm (Rule 19).

### Honest exhaustion signal (why P3 reading converges here)
Hazard-core arXiv axes are now visibly thin/exhausted: GLOF (8 total), landslide-displacement-forecasting
(1), GNN+landslide (5), RL-evacuation (5), InSAR+DL+landslide (1), cloudburst+Himalaya (0). The remaining
SOTA for these lives in journals (NHESS, The Cryosphere, Remote Sensing), already noted via D-010 multi-
source policy. Flood+foundation-model (47) and SAR-FM (17) and precip-nowcasting+diffusion (31) remain the
live arXiv veins and were mined. 43 NEW is an honest stopping point, not padding (§0.5).

---
- Still-thin themes to scan: ESP-NOW/BLE/Zigbee/geofencing-no-IP; WSN false-alarm suppression (arXiv
  near-empty under direct terms — try broader); watermark/provenance (BabelFake 2610.06339, FlowMark,
  FreSia 2610.05726); vectorized-GPU-RL enablers (logged, likely queue-only); TinyML security
  (2609.27202 federated); more anomaly surveys/seminal; privacy for alerting.
- Queued strong candidates: 2610.01005 (tolerance-based fairness auditing), Stocker 2511.xxxxx (serial-
  dependence CP survey), 2609.16314 (cross-modal SSL fault detection), 2609.17763 (auditable wildfire
  spread), 2209.07620 (fuzzy WSN fire + Lamport sig).
- Then build P3 exit deliverables: distribution table (theme×tier×workstream), REFERENCES.md grouped +
  top-30 must-read, Audit #9 (~20% sample), PHASE_03_report.md, PHASE_03_gate.md → STOP (await GO P4).