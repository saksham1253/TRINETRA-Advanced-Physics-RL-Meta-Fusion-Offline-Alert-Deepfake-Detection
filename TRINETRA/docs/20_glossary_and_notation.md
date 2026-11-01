# 20 — Glossary and Notation

> **Scope and honesty.** Every entry below is defined **as the term is used in TRINETRA (HIMKAVACH)**,
> harvested from the already-written chapters, `_CANON.md`, and the code they cite. Units are the project's
> units. Where an expansion or meaning could not be sourced from a chapter / `_CANON` / code it is marked
> **(definition not established in sources)**; an expansion that is inferred rather than stated is tagged
> `[LIKELY]`. Source-reported numbers are *other papers' results on their own data* and never TRINETRA
> measurements (`_CANON.md §1`, Rule 16). The single operating point appears two ways: **`p*` (used by
> `_CANON.md §4` and the code) ≡ `τ*` (the symbol the HLD uses)** — the same cost-loss alarm threshold
> ≈ 0.0476; see the SYMBOLS table.
>
> "Chapter where it matters" uses the user doc-frame numbering (00–25). The three workstream numbering
> schemes are reconciled in `_CANON.md §3` and in the DOMAIN TERMS entry "workstream (WS) schemes".

---

## 1. Abbreviations and Acronyms (alphabetical)

| Abbreviation | Expansion | Meaning in TRINETRA | Chapter |
|---|---|---|---|
| **ABS** `[ABS]` | Abstract-only read | Read-depth / honesty label: a source read at abstract level only; may **never** be stated as established fact (`_CANON.md §1,§7`). | 05, 08, 10, 12, 19 |
| **ACI** | Adaptive Conformal Inference | Online conformal method (Gibbs & Candès 2021) that keeps **long-run** coverage under drift by nudging the working miss-rate `α_t`; the `AdaptiveConformal` class in `ws6_robust/conformal.py`. | 12 |
| **AMP** | Automatic Mixed Precision | PyTorch fp16/bf16 training speedup (`torch.cuda.amp.autocast` + `GradScaler`), on by default in `deep/train.py`; a large speedup on Turing T4 GPUs. | 05a, 11 |
| **APNs** | Apple Push Notification service | OS push service cited as requiring the internet — one reason "offline alerting by IP" is `[INFEASIBLE]`. | 08 |
| **ASN** | Autonomous System Number | Network-topology identifier used to show an IP marks *where you attach*, not where you stand (IP-verdict argument). | 08 |
| **AUC / ROC-AUC** | (Receiver-Operating-Characteristic) Area Under the Curve | Discrimination metric; in this project treated as **base-rate-dependent and not comparable across hazards**, which is why the cost-aware Value Score is primary. Source-reported collapse 0.90→0.76/0.71/0.54 under spatial-CV. | 12 |
| **BCa** | Bias-corrected and accelerated (bootstrap interval) | The default confidence-interval method in the `real_win` admission test (`eval/_stats.bca_interval`); coverage error O(1/n) vs O(1/√n) for percentile. | 12 |
| **BLE** | Bluetooth Low Energy | Candidate last-100 m alert transport (BlueFlood-style flood) to unmodified phones; density/interference-fragile, hardware-unverified `[LIKELY]`. | 08 |
| **BLUE / GLS** | Best Linear Unbiased Estimator / Generalised Least Squares | Correlation-aware minimum-variance fusion weights (Aitken/GLS) so redundant sensors don't double-count; `ws5_fusion_rl/correlation.py`. Negative "hedging" weights are clipped (safety deviation). | 02, 05b |
| **BOM** | Bill of Materials | Per-node hardware cost list; all ₹ figures are `[EST]` (suppliers 403'd); Node A ≈ ₹1,930, Node B ≈ ₹1,980; ≤₹2000 gate (C2) not yet live-enforceable. | 02 (C2), 03, 13 |
| **Brier** | Brier score | Mean squared error of probabilistic forecasts, `mean((p−y)²)`, with Murphy decomposition into reliability − resolution + uncertainty; `eval/calibration.py`. | 12 |
| **BVFT** | Batch Value-Function Tournament | Offline policy-**selection** method (arXiv 2110.14000) in the research-grade RL valuation plan; spec/plan only, not measured. | 10 |
| **CAP** | Common Alerting Protocol | Signed XML alert format (CAP 1.2) carrying origin/area/severity/expiry/nonce; `ws3_alert/cap.py` `build_cap` **refuses** to emit without an `APPROVED:` operator token (Rule 19) and HMAC-SHA256-signs the payload. | 02, 08 |
| **CGNAT** | Carrier-Grade NAT | One public IPv4 shared across thousands of mobile subscribers; a core reason you cannot push to a specific handset "by IP" — the public IP identifies the carrier NAT, not a person. | 08 |
| **CI** | Continuous Integration (also: Confidence Interval) | (1) The 6 fail-closed `scripts/ci_gates.py` honesty/safety gates — **ALL 6 CI GATES PASSED** `[CONFIRMED]`. (2) In Fukuzono / real-win contexts, a bootstrap/delta-method confidence interval. Both senses occur; disambiguate by context. | 02, 05b, 12 |
| **CNN** | Convolutional Neural Network | Backbone of the CCTV FireSmokeNet detector (CNN→GRU). | 05, 09 |
| **CP** | Conformal Prediction | Umbrella for the split-CP / WCPS / ACI / Mondrian / CRC calibration toolkit; `ws6_robust/conformal.py`. | 12 |
| **CQL** | Conservative Q-Learning | The implemented offline-RL learner (Model 6, Kumar et al. 2006.04779); conservative penalty lower-bounds OOD-action value; `γ=0` by default ⇒ one-step contextual bandit. `py_compile`-clean, never GPU-trained — UNTESTED on GPU. | 10 |
| **CRC** | Conformal Risk Control | RCPS-style threshold (Angelopoulos et al. 2022) that bounds the **miss-rate** with finite-sample slack `B/(n+1)`; `conformal_risk_threshold`. | 12 |
| **CUSUM** | Cumulative Sum (control chart) | Sequential change-point detector in `ws6_robust/drift_monitor.py` (`cusum_update`, slack `k=0.5`, threshold `h=5.0`); drift voids the conformal bound. | 12, 13, 15 |
| **CV** (spatial-CV / spatial-block CV) | Cross-Validation | Mandatory **spatial-block** CV (whole zones/tiles withheld) — random CV overstates skill. The only admissible split for a headline number. | 12 |
| **CVaR** | Conditional Value-at-Risk | Worst-case tail metric (e.g. CVaR@5%) reported in the SCOPE-RL RL risk-evaluation plan — the correct posture when the tail is a mass-casualty event. Plan only. | 10 |
| **C-DOT** | Centre for Development of Telematics (India) | Operator (with NDMA) of India's SACHET CAP alerting path; TRINETRA can only **request** an official alert from them. | 08 |
| **DHCP** | Dynamic Host Configuration Protocol | Dynamically reassigns private addresses, so there is no stable per-device IP to target — part of the IP-alerting `[INFEASIBLE]` argument. | 08 |
| **DL** | Deep Learning | Shorthand in the eval chapter; source-reported finding: five DL models do **not** decisively beat a gradient-boosted baseline under spatial-CV. | 12, 13 |
| **DDP** | DistributedDataParallel (PyTorch) | Max-throughput multi-GPU training path (`deep/ddp.py`, one process/GPU, NCCL all-reduce, rank-0 save); used from a plain `.py` script. | 11, 16 |
| **DataParallel** | `nn.DataParallel` (PyTorch) | Single-process multi-GPU scatter/gather; the default `--parallel` mode for most models. Source of three fixed multi-GPU bugs (leaf-tensor, drop_last, None-label). RL deliberately avoids it (model too small). | 10, 11, 13 |
| **DTN** | Delay-Tolerant Networking | Store-carry-forward alert dissemination (Tier-0 backstop); `ws3_alert/dtn.py` `DTNQueue` uses **binary Spray-and-Wait**; realises feature F-10, mitigates FM-11. | 02, 08 |
| **ECE** | Expected Calibration Error | Bin-weighted mean gap between confidence and accuracy, `Σ (n_bin/N)·|acc−conf|`; `eval/calibration.py`. | 12 |
| **EO** | Earth Observation | Free satellite imagery (ESA/NASA) ingested via a **frozen EO foundation model** encoder; EO is a Tier-1/2 (never Tier-0) input. | 02, 05 |
| **EO-FM** | Earth-Observation Foundation Model | The frozen multispectral/SAR encoder (Prithvi/SatMAE/Clay-class, named in code docstrings, no repo arXiv) whose embeddings feed the EO downstream head. | 02, 05 |
| **ESS** | Effective Sample Size | OPE honesty guardrail `(Σw)²/Σw²`; `ope_feasible` refuses if ESS < 10% of N (weights too concentrated). Also appears as the spatial `N_eff` theorem (distinct use). | 10, 12 |
| **EST** `[EST]` | Estimated | Honesty label for planning-level figures not live-verified (all BOM ₹ costs, `_CANON.md §8`). | 03, 13 |
| **EVT** | Extreme-Value Theory | Tail prior proposed where no calibrated solver exists (ungauged Himalaya) and for extreme-transition lag. | 13 |
| **EWS** | Early-Warning System | The high-recall supervised ensemble role (XGBoost EWS + per-hazard heads). | 02 |
| **FA / C_FA** | False Alarm / False-Alarm cost | Cost of alarming on a non-event; `C_FA = 5` in the canonical cost table. | 10, 12 |
| **FCM** | Firebase Cloud Messaging | Android OS push service; cited (with APNs) as internet-dependent — defeats "offline by IP". | 08 |
| **FM-1 … FM-6** | Fusion Model 1…6 | The six derived meta-fusion options: FM-1 precision-weighted mean (**Class-A default/fallback**), evidential, conformal-stacked, covariance-intersection, physics-gated MoE, RL-tuned. Class-B/C ones are flag-gated with FM-1 fallback. | 02, 05, 05b |
| **FM-01 … FM-40** | Failure Mode 01…40 | The failure-mode catalogue IDs (`analysis/05`); e.g. FM-11 backhaul-down, FM-05 shield unrealizability, FM-20 proximity-bias overconfidence. **Distinct** from the FM-1..6 fusion models above. | 08, 13 |
| **FEM** | Finite-Element Method | 2-D/FEM slope solver, **rejected** for the edge path (needs mesh/geometry; not offline-cheap). | 05b |
| **fps** | frames per second | Unit flagged in Bug #14: "57 fps / <1 s on-edge" was an L40S server-GPU number mis-attributed to a Jetson. | 13 |
| **FQE** | Fitted Q-Evaluation | Named OPE method to **rank** policies offline (iterate only if OPE feasible); plan only. | 10 |
| **FS / FoS** | Factor of Safety | Infinite-slope landslide stability ratio; FS<1 ⇒ unstable and forces a shield floor (ORANGE). Hard deterministic gate, `ws1b_geophys/fs.py`. (Also the SYMBOLS table.) | 02, 05, 05b, 13 |
| **FT / FT-PARTIAL / FT-REF** | Full-Text / partial / reference-only read-depth | Source read-depth labels (`_CANON.md §7`): full text, partially read, or seen only as a reference. | 19 (defined), used throughout |
| **GBDT / GB** | Gradient-Boosted Decision Trees | A mandatory, independent-feature admission baseline a deep model must beat; source-reported to beat five DL models. Not in the numpy core (no sklearn). | 12, 13 |
| **GLOF** | Glacial Lake Outburst Flood | A primary target hazard; its rarity motivates Mondrian per-zone coverage; shield RED on lake-drop + downstream stage-jump. | 00, 05b, 08, 12 |
| **GLS** | Generalised Least Squares | See **BLUE / GLS**. | 05b |
| **GMF** | Gated-Mixture Fusion | Gated-mixture base + a **bounded residual** (clipped ±cap, default 0) that can run a learned head; with no head GMF ≡ FM-1; `ws5_fusion_rl/gmf.py`. | 02, 05, 05b |
| **GPIO** | General-Purpose Input/Output | Firmware-side pins driving siren/relay in `SirenBus` integration. | 08 |
| **GRD** | Ground-Range-Detected (Sentinel-1 SAR product) | SAR product whose ~900 m² minimum detectable area is the GLOF-precursor resolution floor (FM-27). | 13 |
| **GRU** | Gated Recurrent Unit | Temporal head of FireSmokeNet that suppresses single-frame fire false alarms (glint/headlights). | 05 |
| **GST** | Goods and Services Tax (India) | Included in the ≤₹2000 per-node BOM budget (C2) alongside shipping + ~10% contingency. | 03 |
| **HMAC(-SHA256)** | Hash-based Message Authentication Code | Keyed signature appended to CAP XML by `build_cap`; also the mesh-leg authentication requirement. | 08 |
| **HLD / LLD** | High-/Low-Level Design | Design documents in `DESIGN/`; HLD uses the symbol `τ*` where `_CANON.md`/code use `p*` (same operating point). | 02 (sources) |
| **I–D** | Intensity–Duration (rainfall threshold) | Caine power-law landslide-triggering screen `I_threshold = a·D^(−b)`; a soft `p_caine` into the geo gate; `ws1b_geophys/caine.py`. | 02, 05b |
| **IMERG** | Integrated Multi-satellitE Retrievals for GPM | Satellite precipitation product bias-corrected by LoRa rain gauges in the calibration loop. | 02 |
| **InSAR** | Interferometric Synthetic-Aperture Radar | Ground-deformation / precursor sensing cached at the gateway tier. | 02 |
| **iForest** | Isolation Forest | A component of the anomaly stack (and the numpy "iForest-lite" always-on fallback). | 02 |
| **IoT** | Internet of Things | The ground sensor nodes (Tier-0): tilt/stage/rain, on-node FS and 1/v, LoRa uplink. | 02, 03 |
| **IQL** | Implicit Q-Learning | Offline-RL alternative (2110.06169) that **never queries OOD actions**; attractive for safety; not implemented. | 10 |
| **ISM** | Industrial, Scientific, Medical (radio band) | Licence-exempt band context; Bug #6 — 433 MHz is **not** an Indian ISM/LoRa band (IN865–867 is). | 13 |
| **LoRa** | Long Range (radio modulation) | Low-rate long-range radio for node→gateway links and the mesh tier; India band **IN865–867 MHz** on an **SX1262** transceiver; ≤51-byte frames. | 02, 08, 13 |
| **LoRa (PEFT) / LoRA** | Low-Rank Adaptation | A parameter-efficient fine-tuning method (PEFT) for adapting frozen backbones under the GPU budget. **Note the name clash** with the LoRa radio above — context disambiguates (training vs transceiver). | 11, 05a |
| **LSPIV** | Large-Scale Particle Image Velocimetry | Camera-based river-surface velocity method. **(definition not established in sources — the acronym does not appear in the chapters read; expansion is the standard field term `[LIKELY]`.)** | — |
| **LMEM / GLRT** | Linear Mixed-Effects Model / Generalised Likelihood-Ratio Test | The "real-win" statistical gate on every claimed improvement (provenance/reproducibility, F-17). | 02 |
| **MCE** | Maximum Calibration Error | `max over non-empty bins of |acc−conf|`; `eval/calibration.py`. | 12 |
| **MCU** | Microcontroller Unit | Tier-0 node processor; heavy models are Tier-1/2 only because Tier-0 runs only what fits MCU SRAM/flash/energy (C8). | 02 |
| **mDNS** | multicast DNS | Local-link discovery usable for same-LAN push — but only to devices already joined and listening (the narrow Tier-2 residual). | 08 |
| **MDP** | Markov Decision Process | The RL problem framing (state/action/reward/transition); specified only — nothing simulated. | 10 |
| **MILP** | Mixed-Integer Linear Programming | A strong non-RL optimiser baseline (GREAT-EER) the RL policy must beat, else "use the non-RL optimizer". | 10 |
| **MoE** | Mixture of Experts | Fusion routing (FM-5 physics-gated MoE); FM-06 warns of routing collapse → soft gating used. | 02, 13 |
| **Mondrian (CP)** | Mondrian Conformal Prediction | Per-group (per-hazard/zone) conformal coverage so a rare class (GLOF) isn't hidden by good marginal coverage; unseen groups fall back to the most conservative quantile. | 12 |
| **NAT** | Network Address Translation | Private, reassigned addresses behind NAT mean no routable per-device target — part of the IP `[INFEASIBLE]` verdict. | 08 |
| **NDMA** | National Disaster Management Authority (India) | Alerting authority; origination of cell broadcast/WEA is **their** function, not TRINETRA's. | 08 |
| **ND-1 / ND-2 / ND-3** | Novel Dimensionless fire terms | Three Class-C, default-OFF soft fire features (de-aliased flicker; smoke-transmittance temperature; ignition index), uncertainty grows as data degrade; `ws1a_firephys/novel_nd.py`. | 05b |
| **NF-1 … NF-4** | Novel-Fusion primitives 1…4 | Soft weighting/uncertainty primitives (consistency, reliability, conflict→uncertainty, salience) every fusion model reuses; `ws5_fusion_rl/nf.py`. They re-weight, never fabricate a probability. | 02, 05, 05b |
| **ns-3** | network simulator 3 | Planned primary alert-network simulator (LoRaWAN module); nothing simulated yet. | 08 |
| **OOD** | Out-Of-Distribution | (state,action) pairs the logging policy rarely took; CQL's conservative penalty pushes Q down on OOD actions. | 05, 10 |
| **OOF** | Out-Of-Fold | The model's own held-out score used as a "learned baseline"; a **circular** (weak) comparator — hence physics-rule/GBDT baselines are weighted as the ones that matter. | 12 |
| **OPE** | Off-Policy Evaluation | Estimating a learned policy's value from logged data; the deploy gate admits the learned policy only if OPE is feasible (positivity+ESS) **and** its value ≥ rule baseline. | 05, 10 |
| **PA** | Public Address (voice) | Multi-modal Tier-1 alert channel (with siren + strobe) for accessibility (blind users). | 08 |
| **PAV** | Pool-Adjacent-Violators (algorithm) | The isotonic recalibrator's engine: merges monotonicity-violating adjacent blocks into weighted means; `IsotonicCalibrator`. | 12 |
| **PBRS** | Potential-Based Reward Shaping | Reward-design discipline that preserves optimality — a mitigation against reward hacking. | 10, 13 |
| **PDR** | Packet Delivery Ratio | Alert-network simulation metric (source-reported, often SIMULATION-only). | 08 |
| **PEFT** | Parameter-Efficient Fine-Tuning | The "fine-tune, don't pretrain" compute strategy (frozen backbone + small adapters/LoRA) that makes the ≤30 GPU-h plan `[LIKELY]` feasible. | 03, 11 |
| **PHARAOH** | (project name for the adaptive-order power-mean fusion operator) | Class-C, default-OFF power-mean operator whose order `ρ=1+κ·D·S` bends toward "max" only under a credible physics-consistent alarm (anti-complacency); fails open to "uncertain". Expansion as an acronym **(definition not established in sources — treated as a project code-name)**. | 02, 05, 05b |
| **PINN** | Physics-Informed Neural Network | Geo-PINN uses physics (FS<1, Iverson residual) as a label-free penalty; a **full on-device fire-PINN solver is `[INFEASIBLE]`** now (stiffness, spectral bias) → physics enters as soft features with Class-A fallback. | 05, 13 |
| **PSI** | Population Stability Index | Drift metric in `drift_monitor.py` (>0.1 moderate, >0.2 significant); drift voids the coverage bound → reliability "Unreliable". | 12, 13, 15 |
| **PWS / SIB** | Public Warning System / System Information Block | 3GPP cell-broadcast delivery; SIBs are broadcast **without authentication** → spoofable (arXiv 2604.24404), hence signed-CAP + cross-cell corroboration. | 08 |
| **RCPS** | Risk-Controlling Prediction Sets | The CRC family that bounds a chosen risk (here the miss-rate) with finite-sample slack. | 12 |
| **ReportGuard** | (code object) | The gate (`eval/report.py`) that **refuses to emit a headline metric** unless spatial-CV + a real win over every baseline hold (Rule 16); today it reads **NOT ADMITTED**. | 12 |
| **RL** | Reinforcement Learning | Offline (batch) RL only — no live exploration in a life-safety valley; output is **advisory**, shielded, OPE-gated. | 02, 10 |
| **RMS** | Root Mean Square | Tiny Tier-0 statistical screen on tilt; also "FoS RMS error" in FM-24. | 02, 13, 15 |
| **RTA** | Run-Time Assurance | Framing of the shield as a conservative fixed-fallback RTA (Bug #26: a predictive/reachability-aware shield is future work). | 13 |
| **SACHET** | (India's CAP-based public alerting platform, NDMA/C-DOT) | The official CAP/cell-broadcast feed TRINETRA may **request** but never originate. Expansion as acronym **(definition not established in sources — used as the platform's name)**. | 02, 08 |
| **SAR** | Synthetic-Aperture Radar | Cloud-penetrating EO modality (Sentinel-1); its resolution floor limits small-GLOF detection (FM-27). | 02, 13 |
| **SCOPE-RL** | (offline-RL evaluation library/method) | RL risk-evaluation plan: report CVaR@5%, worst-case return, full return distribution (arXiv 2311.18206). Plan only. | 10 |
| **SF** | Spreading Factor (LoRa) | LoRa link-budget dial (SF7–SF12): higher SF = longer range, lower rate; source-reported SF7-8 ~120 dB … SF12 ~180 dB. | 08 |
| **SMS** | Short Message Service | Needs cellular + per-number opt-in → **not** "offline" and registry-limited (Tier-3 adjunct). | 08 |
| **SNR** | Signal-to-Noise Ratio | Radio-link quality in source-reported mesh ranges (e.g. Meshtastic +2.75 dB SNR). | 08 |
| **SoC** | System on Chip | Gateway (Tier-1) edge compute. | 02 |
| **SSL** | Self-Supervised Learning | EO encoder pretraining/adaptation paradigm (full SSL pretrain on Kaggle is `[INFEASIBLE]` under budget → PEFT). | 11 |
| **SX1262 / SX1278** | Semtech LoRa transceiver ICs | SX1262 is the **compliant** IN865–867 radio; SX1278 (433 MHz) was the non-compliant Bug #6 part. | 02, 13 |
| **TCN** | Temporal Convolutional Network | Causal encoder of the DeepAnomaly model (TCN AE + forecast + Deep-SVDD). | 05a, 11 |
| **TD3-BC** | Twin-Delayed DDPG + Behaviour Cloning | A minimalist offline-RL baseline (2106.06860); `FEATURES.md` F-06 names it "baseline-first", but the implemented Model 6 is **CQL** (documented divergence). | 10 |
| **TF32 / bf16 / fp16** | reduced-precision float formats | Mixed-precision training formats enabled by AMP/`setup_perf()`. | 11 |
| **TinyML** | Tiny Machine Learning | On-node pre-filter at Tier-0 (fits MCU budget). | 02 |
| **TRIGRS** | Transient Rainfall Infiltration and Grid-based Regional Slope-stability | The lineage that confirms the Iverson bug-guard `D1=D0/cos²β` with no extra transient cosine (Bug #3 refs). | 05b, 13 |
| **TRINETRA / HIMKAVACH** | project names (alternatives for the same project) | An offline-first, physics-grounded, **advisory** early-warning + hazard-detection research program **and** its reference code implementation. Component words are **(definition not established in sources — proper project names)**. | all |
| **UDP** | User Datagram Protocol | Transport for same-LAN broadcast/multicast push (Tier-2 residual). | 08 |
| **UNVERIFIED** `[UNVERIFIED]` | not confirmed against a primary source | Honesty tag for leads needing professional/primary-source confirmation (e.g. the regulatory "a private project cannot originate WEA" claim; all India legal/radio/alerting facts, N-7). | 03, 08 |
| **UNTESTED** | not executed in this environment | Status tag for the PyTorch `deep/`+`kaggle/` code: `py_compile`-clean but **never run on a GPU** here (no torch/CUDA in the sandbox). | 05, 05a, 10, 11 |
| **VAD** | Video Anomaly Detection `[LIKELY]` | A heavy Tier-1 video component listed in the architecture; expansion inferred from context (heavy video model). | 02 |
| **VPN** | Virtual Private Network | Relocates apparent IP, silently defeating any geo-IP logic (IP-verdict argument). | 08 |
| **VS** | Value Score | Cost-aware primary ranking metric, `VS = 1 − E_forecast/E_climate` (1 perfect; ≤0 no skill over climatology); `eval/value_score.py`. | 12 |
| **WAN** | Wide-Area Network | "Offline-first" = the primary path works with no internet/WAN backhaul. | 08 |
| **WCPS** | Weighted Conformal Prediction (under covariate Shift) | Reweights calibration residuals by a train→test likelihood ratio to keep coverage honest under input shift; `weighted_conformal_quantile`. (Written "WCPS" in `_CANON`/arch; `WeightedConformal` in code.) | 02, 12 |
| **WEA** | Wireless Emergency Alerts (US cell broadcast) | Authority-operated broadcast to all phones in a cell; source-reported behaviour change (−1.1 °F thermostat) and payload-limited geo-fencing (polygons → 9.7–23.6%). Not TRINETRA's to originate. | 08 |
| **WIS** | Weighted Importance Sampling | One-step OPE value estimator `Σ(w·r)/Σw` with clipped ratios + ESS; `rl.wis_value`. | 10 |
| **WS1 … WS8** | Workstream 1…8 | Internal artifact workstreams; map to the six user doc-frame workstreams per `_CANON.md §3` (see DOMAIN TERMS "workstream (WS) schemes"). | all (esp. 02, 03) |
| **XGBoost** | eXtreme Gradient Boosting | The supervised high-recall EWS / per-hazard ensemble and an anomaly-stack component (planned; sklearn/xgboost absent from the numpy sandbox). | 02 |

---

## 2. Symbols and Notation (mathematical, alphabetical by role)

| Symbol | Meaning | Units | Where defined |
|---|---|---|---|
| **FS** | Factor of Safety; FS<1 ⇒ unstable, forces shield floor | dimensionless | `ws1b_geophys/fs.py` (05b §9) |
| **c′** | effective cohesion (Mohr–Coulomb) | kPa | fs.py (05b §9) |
| **φ′** | effective friction angle | degrees | fs.py (05b §9) |
| **γ** (soil) | soil unit weight | kN/m³ | fs.py (05b §9) |
| **γ_w** | unit weight of water (`u_w = γ_w·ψ`) | 9.81 kN/m³ | fs.py (05b §9) |
| **z** | depth to the failure plane | m | fs.py (05b §9) |
| **β** | slope angle | degrees | fs.py / iverson.py (05b §9–10) |
| **u_w** | pore-water pressure | kPa | fs.py (05b §9) |
| **σ_s** | suction stress (apparent-cohesion); σ_s ≥ 0, **vanishes at saturation** | kPa | fs.py (05b §9); Bug #2 |
| **σ′_n** | effective normal stress `= γz cos²β − u_w + σ_s` | kPa | fs.py (05b §9) |
| **S_e** | effective saturation; `S_e→1 ⇒ σ_s→0` | dimensionless (0–1) | 05b §9 |
| **ψ** | (transient) pressure head → becomes `u_w` for FS | m | iverson.py (05b §10) |
| **Z** | depth coordinate in the Iverson transient solution | m | iverson.py (05b §10) |
| **t** | time (consistent with D0) | s | iverson.py (05b §10) |
| **D0** | saturated hydraulic diffusivity | m²/s | iverson.py (05b §10) |
| **D1** | slope-adjusted diffusivity, **`D1 = D0/cos²β`** (the ONLY place slope enters — bug-guard) | m²/s | iverson.py (05b §10); `_CANON §4` |
| **K_z** | vertical saturated hydraulic conductivity | m/s | iverson.py (05b §10) |
| **I_z** | surface infiltration flux (`I_z ≤ K_z`) | m/s | iverson.py (05b §10) |
| **ierfc(x)** | integral of the complementary error function, `exp(−x²)/√π − x·erfc(x)`, `ierfc(0)=1/√π` | dimensionless | iverson.py (05b §10) |
| **v, 1/v** | surface-displacement velocity and its inverse (Fukuzono) | 1/v: time/length (consistent units) | fukuzono.py (05b §11) |
| **α** (Fukuzono) | inverse-velocity exponent; **α=2 ⇒ 1/v linear in t**; α≠2 linearises `v^(1−α)` | dimensionless | fukuzono.py (05b §11) |
| **t_f** | forecast failure time (x-intercept of 1/v), reported with a prediction interval `[t_f_low, t_f_high]` | same time units as input | fukuzono.py (05b §11) |
| **z** (CI) | normal quantile for the interval, `z=1.96 ≈ 95%` | dimensionless | fukuzono.py (05b §11) |
| **r²** | weighted goodness-of-fit; gates the Fukuzono contribution (`p_fk ∝ r²`) | dimensionless (0–1) | fukuzono.py (05b §11) |
| **I, D** | rainfall intensity, duration (Caine I–D) | I [mm/h], D [h] | caine.py (05b §12) |
| **a, b** | Caine threshold coefficients `I_threshold = a·D^(−b)`; **must be re-fit per region** (defaults a=14, b=0.39) | a carries mm·h^(b−1); b dimensionless | caine.py (05b §12) |
| **ratio** (Caine) | `I / I_threshold`; exceedance when > 1 | dimensionless | caine.py (05b §12) |
| **p\*** | cost-loss alarm operating point, **`p* = C_FA/(C_FA+C_miss) = 5/105 ≈ 0.0476`**; default `RuleBaselinePolicy` threshold | probability (0–1) | `_CANON §4`; value_score.py; decision.py |
| **τ\*** | the HLD's symbol for the same operating point — **τ\* ≡ p\* ≈ 0.0476** (`_CANON §4` uses p*, HLD uses τ*) | probability (0–1) | DESIGN/HLD.md (noted in this chapter header) |
| **C_FA** | false-alarm cost | **5** (unitless cost) | 10, 12; `_CANON §4` |
| **C_miss** | missed-event cost (≈20× C_FA) | **100** (unitless cost) | 10, 12; `_CANON §4` |
| **level cut points** | conformal-level cuts `(p*, 4p*, 10p*)` by default, or calibrated CRC cuts | probability | decision.conformal_level (05b §29) |
| **VS** | Value Score `1 − E_forecast/E_climate` | dimensionless | value_score.py (12.2.1) |
| **ECE, MCE** | expected / maximum calibration error | dimensionless (0–1) | calibration.py (12.2.5) |
| **Brier** | `mean((p−y)²)` | dimensionless (0–1) | calibration.py (12.2.5) |
| **α_t** (ACI) | adaptive miss-rate, `α_{t+1}=clip(α_t+γ(α_target−err_t),0,1)` | dimensionless (0–1) | conformal.py (12.7) |
| **γ** (ACI) | ACI learning rate (note: name clash with soil γ and RL γ) | dimensionless | conformal.py (12.7) |
| **q** (conformal) | adjusted calibration quantile, `k=ceil((n+1)(1−α))−1` | score units | conformal.py (12.2.6) |
| **λ** (CRC) | lowest alarm threshold whose corrected miss-rate ≤ target | score units | conformal_risk_threshold (12.7) |
| **p, u, c, r** | an `ExpertOutput`'s probability, uncertainty, conflict/consistency, reliability | each in [0,1] | common/types.py (02.7) |
| **w̃_i** | effective (gating) weight `= available·r_i·c_i·exp(−u_i/τ)` | dimensionless | nf.effective_weight (05 CLOSING A) |
| **τ** (gating) | gating temperature in w̃ (default 0.5) — **not** the operating point τ\* | dimensionless | nf.py (05b §20) |
| **U\*** | conflict-aware fused uncertainty `Σ w_i u_i + λ·D(p)`; U\*>0.6 ⇒ uncertain | dimensionless (0–1) | nf.nf3 (05b §20) |
| **D(p)** | weighted dispersion of expert probabilities (disagreement) | dimensionless | nf.py (05b §20) |
| **λ** (NF-3) | dispersion weight in U\* (default 0.3) | dimensionless | nf.py (05b §20) |
| **S** | salience `max_i[r_i·c_i·p_i]` over available experts | dimensionless (0–1) | nf.nf4 (05b §20) |
| **ρ** (PHARAOH) | power-mean order `1+κ·D·S`, clipped [1,8]; ρ=1 ⇒ arithmetic mean | dimensionless | pharaoh.py (05b §22) |
| **κ** | PHARAOH order gain (default 2) | dimensionless | pharaoh.py (05b §22) |
| **k_fs** | geo-gate FS→probability steepness, `p_fs=sigmoid(k_fs·(1−FS))`, k_fs=4.0 | dimensionless | gate.py (05b §13) |
| **cap / residual_cap** | hard clip on the GMF/attention learned residual (default 0.1) | probability units | gmf.py (05 CLOSING A) |
| **λ** (CQL) / cql_alpha | conservative-penalty weight in the CQL loss (default 1.0) | dimensionless | offline_rl.py (10.3.1) |
| **γ** (RL discount) | RL discount; **default 0.0** ⇒ one-step contextual bandit | dimensionless (0–1) | CQLConfig (10.3.1) |
| **τ** (Polyak) | target-net tracking rate `target←(1−τ)target+τ·online`, 0.005 | dimensionless | offline_rl.py (10.3.1) |
| **w_i** (WIS) | importance ratio `clip(target/clip(behavior,1e-6),0,1e3)` | dimensionless | rl.wis_value (10.3.2) |
| **ESS** | effective sample size `(Σw)²/Σw²` | count | rl.py (10.3.2) |
| **L** (flame) | Heskestad flame height `0.235·Q̇^(2/5) − 1.02·D` | m | established_ef.py (05b §14) |
| **Q̇ / Q** | heat-release rate (total / convective Q̇_c) | kW | established_ef.py (05b §14) |
| **D** (fire) | fire/pool diameter | m | established_ef.py (05b §14) |
| **f** (flicker) | Strouhal puffing frequency `f ≈ 1.5/√D` | Hz | established_ef.py (05b §16) |
| **St** | Strouhal number `St = f·√(D/g)` ~ const | dimensionless | established_ef.py (05b §14) |
| **N_c** | Byram convection number `2g·Q̇_c/(ρ c_p T∞ U³)`; >~2 plume-dominated, <~1 wind-dominated | dimensionless | established_ef.py (05b §14) |
| **U** (wind) | wind speed in the Byram number | m/s | established_ef.py (05b §14) |
| **E, T, ε** | gray-body radiance `E=ε·σ·T⁴`, temperature, emissivity | E [W/m²], T [K], ε (0–1) | established_ef.py (05b §14) |
| **σ** (Stefan–Boltzmann) | radiation constant 5.670374419e-8 | W·m⁻²·K⁻⁴ | established_ef.py (05b §14) |
| **τ** (Beer–Lambert) | transmittance `exp(−(κ+σ)·L)` (yet another τ — optical, not τ\*/gating) | dimensionless (0–1] | established_ef.py (05b §14) |
| **ΔT₀** | Heskestad plume centerline temperature rise | K | established_ef.py (05b §14) |
| **σ_K** (ND-2) | smoke-temperature uncertainty that **blows up as τ_s→0** (ill-conditioned ⇒ "uncertain") | K | novel_nd.py (05b §18) |
| **N_eff** | effective sample size under spatial correlation, **`N_eff = Θ(n²/r²)`** (naive CIs too narrow) | count | 12.1 (arXiv 2610.08227) |
| **g** (buffer) | spatial-CV correlation-range buffer, require `g ≥ r` (variogram) | length | 12.1 |
| **PSI** | population stability index (>0.1 moderate, >0.2 significant) | dimensionless | drift_monitor.py (15.x) |

> **Overloaded symbols — read by context:** `γ` is soil unit weight (geo), the ACI learning rate (conformal),
> and the RL discount; `τ` is the operating point `τ*`, the gating temperature, the Polyak rate, **and**
> optical transmittance; `λ` is the NF-3 dispersion weight **and** the CQL conservative weight; `D` is pool
> diameter (fire), rainfall duration (Caine), and probability dispersion (NF). `z` is depth (geo) and the CI
> normal quantile (Fukuzono). Each row above names which use it is.

---

## 3. Domain Terms (alphabetical)

| Term | Definition (grounded in the chapters) |
|---|---|
| **advisory level (Green/Yellow/Orange/Red)** | The system's only output: a four-level ordered advisory `Level` for a **human** operator, who alone decides on public dissemination. Green < Yellow < Orange < Red; the shield maps rules onto this lattice and the CAP builder maps levels to Severity/Urgency/Certainty deterministically (02.7, 08.4). |
| **advisory invariant / `advisory=True`** | Every `Decision` is marked advisory; **no code path issues an autonomous public alert** (Rule 19). Enforced by CI gate G-advisory and the banned-token G-legacy gate. |
| **bounded residual** | The central fusion safety property: a learned head may add only a residual **hard-clipped to ±cap** on top of the physics-anchored base, so a mis-trained head cannot dominate; with no head the residual is 0 (GMF ≡ FM-1). |
| **conformal coverage** | The realised fraction of outcomes falling in the prediction set/interval. Reported as **marginal and per-zone (Mondrian)**; **never called a "guarantee"** — it holds only under exchangeability/correct weights and is **voided under drift**. |
| **cost-loss / cry-wolf** | Scoring by a decision-theoretic cost table (C_FA=5, C_miss=100) rather than accuracy/AUC, because a missed event (death risk) is priced ~20× a false alarm. "Cry-wolf" is the failure where repeated false alarms erode compliance → future missed warnings (FM-09), which is why the FA cost is a real calibrated term. |
| **drift (PSI / CUSUM)** | Distribution shift detected by `drift_monitor.py` (PSI threshold, sequential CUSUM). On drift the conformal bound is void, reliability forced to **Unreliable**, and the decision fails to "uncertain". |
| **Deep-SVDD** | Deep Support-Vector Data Description: a one-class, normal-only anomaly head (Ruff et al. 2018) in the anomaly stack; prone to hypersphere collapse (Bug #22) → `init_center` + a model-free fallback kept. |
| **fail-safe to uncertain** | When no experts are available, conflict is high (U\*>0.6), or drift fires, the system **abstains and escalates to a human** — it is never silently confident and never goes silent at the top (Rule 19). |
| **forecast-residual anomaly** | Unsupervised anomaly signal = the residual between a one-step forecast and the observation; part of the WS8 ensemble (always-on numpy `AR(1)` residual + the deep TCN head). |
| **graceful degradation** | Each tier/layer keeps working when the one above is gone; a dropped modality is marked unavailable and widens uncertainty rather than crashing or faking a value (C8, missing-modality adapter). Winter/monsoon solar gaps make node outage **expected**, not exceptional. |
| **human-in-the-loop** | A human reviews `operator.present()` and must issue an `APPROVED:` token before any public CAP exists; "a machine proposes, a human authority disposes" (Rule 19). |
| **leakage** | Information bleeding from test into train — spatially (near-twin tiles in both splits) or temporally (post-event feature). It inflates skill; `assert_no_time_leak` + spatial-block CV + CI gate G-leak prevent it; a leaked number is **void**. |
| **meta-fusion** | The head that combines expert `ExpertOutput`s (physics gates, deep models, anomaly, RL) into one calibrated advisory via FM-1/GMF/PHARAOH + NF primitives + BLUE/GLS + hierarchical fusion, feeding the single `decide()`. |
| **offline-first / store-carry-forward** | The primary life-safety path must function with **no internet/WAN**, using owned local radio; DTN nodes **store** an alert, **carry** it, and **forward** it opportunistically when a link returns (binary Spray-and-Wait). |
| **physics Class A/B/C** | Trust labels (Rule 20): **A** = deterministic/established physics; **B** = physics-informed/-regularised learning; **C** = novel term, **default-OFF with an A/B fallback**. Class-C use is always flagged (`used_classC`). |
| **real-win gate** | A model is admitted only if its paired per-block cost saving over **every** baseline has a bootstrap **CI lower bound > 0** (`eval/real_win.py`, BCa over blocks). "Does not beat baseline" is a valid, published verdict. |
| **safety shield (monotone floor)** | A deterministic, hard-coded floor (`shield.py`) that can only **RAISE** the advisory level (FS<1→Orange, corroborated tilt→Red, etc.), applied **after** the learner (post-posed). Monotone over the Green<Yellow<Orange<Red lattice ⇒ total and realizable; a single uncorroborated node cannot reach RED. |
| **soft feature** | Physics quantities (e.g. fire-PINN outputs, ND terms, Caine ratio) entering fusion as *features/consistency* that nudge, never as hard triggers — the admitted way physics enters when a full solver is `[INFEASIBLE]`. |
| **spatial-block CV** | Cross-validation withholding whole spatial blocks (zones/catchments/tiles) so a model is always scored on unseen terrain; **mandatory** — random CV overstates skill. Companion: strict temporal holdout. |
| **workstream (WS) schemes** | Three numbering schemes coexist (`_CANON.md §3`): the **user doc-frame** (6 workstreams WS1–WS6 ≈ chapters), the **internal artifact** workstreams (WS1a/WS1b physics, WS2 deepfake/eval, WS3 alerting, WS4 CCTV, WS5 fusion/RL, WS6 robustness, WS7 IoT, WS8 anomaly), and the **code packages**. Always state which scheme a sentence uses. |
| **zero-shot complement** | Deepfake/zero-shot/crowd-sourced/social-media signals are **low-trust advisory only** (reliability hard-capped at r ≤ 0.4), must be corroborated, and can never gate a life-safety decision (`_CANON.md §6`). |

---

## 4. Honesty Labels, Rules, and Constraints (one place)

### 4.1 Honesty / status labels (apply to every non-trivial claim)

| Label | Meaning |
|---|---|
| **[CONFIRMED]** | Measured by us (e.g. "128 numpy tests pass; 6 CI gates pass") **or** verified in a cited source. (`_CANON.md §1`.) |
| **[LIKELY]** | Plausible but still needs our validation. (`_CANON.md §1`.) |
| **[HYPOTHESIS]** | Our unvalidated idea (e.g. the Class-C novel terms, PHARAOH benefit). (`_CANON.md §1`.) |
| **[INFEASIBLE]** | Ruled out (e.g. IP-based alerting; full on-device fire-PINN solver; autonomous public alerting without authority). (`_CANON.md §1,§6`.) |
| **[ABS]** | Abstract-only source read; **may never be stated as established fact**. Variants: ABS-CANONICAL. (`_CANON.md §1,§7`.) |
| **[EST]** | Estimated / planning-level figure not live-verified (all BOM ₹ costs). (`_CANON.md §8`.) |
| **[UNVERIFIED]** | A lead not confirmed against a primary source (e.g. the WEA-origination regulatory claim; all India legal/radio/alerting facts). |
| **UNTESTED** | Code that is `py_compile`-clean but **never executed** here (the PyTorch `deep/` + Kaggle layer — no GPU/torch in the sandbox). |
| Read-depth labels (sources) | **FT** full text · **FT-PARTIAL** partially read · **ABS** abstract · **ABS-CANONICAL** · **FT-REF** reference-only. (`_CANON.md §7`.) |

> Source-reported numbers must read "Paper X (arXiv NNNN.NNNNN) reports …" and be kept **visibly separate**
> from "Our measurement: …". Where a TRINETRA number would be expected, the honest answer is
> **"not measured"** — because **no model has been trained and no dataset downloaded** (`_CANON.md §0`).

### 4.2 Safety / honesty rules enforced in code (cite by number)

| Rule | Statement (verbatim intent, `_CANON.md §5`) | Where enforced |
|---|---|---|
| **R16** | No performance claim before the eval admission gate (ReportGuard). | `eval/report.py`; CI; chapter 12 |
| **R19** | Advisory, human-in-the-loop, fail-safe to "uncertain/offline"; **NEVER** an autonomous public alert. | shield, `decide`, `cap.build_cap` (APPROVED token); CI gate G-advisory; chapters 08, 10 |
| **R20** | Class A/B/C labels; Class-C novel terms **default-OFF** with an A/B fallback. | `used_classC`; CI gate G-classC; chapters 05b, 06 |
| **R21** | Novelty = "not found in sources searched", **never** "does not exist". | novelty log; CR-06; chapter 13 (Bug #5) |

### 4.3 Hard constraints (binding; chapter 03.3, with `_CANON.md §5` carrying C1,C2,C3,C6,C7,C8)

| ID | Constraint | Consequence |
|---|---|---|
| **C1** | Offline-first alert path | node→LoRa/DTN→gateway→siren works cloud-offline; cloud never on the critical path. |
| **C2** | ≤ ₹2000 per IoT node (incl. GST + shipping, ~10% contingency) | tiered BOM; all ₹ are `[EST]` until live-verified. |
| **C3** | Build compute = Kaggle only, ~25–30 GPU-h/week, ≥15% reserve | PEFT/frozen-backbone first; CPU for all non-training work. |
| **C4** | Free data only may be selected | datasets are candidates; licenses unverified. |
| **C5** | Life-safety → advisory, human-in-loop, fail-safe (= R19) | no autonomous alert; fail to "uncertain/offline". |
| **C6** | Endpoint allow-list (no credential egress) | enforced in CI; signed CAP; key rotation. |
| **C7** | No raw-video egress / privacy | edge-scored; only events/scores leave the node. |
| **C8** | Heavy models Tier-1/2 only | Tier-0 runs only MCU-feasible statistics. |
| **C9** | India LoRa band = IN865–867 MHz | SX1262 radio; 433 MHz SX1278 is non-compliant (Bug #6). |
| **C10** | Honesty rules R16/R19/R20/R21 | no claim pre-gate; class labels; novelty = search claim. |

> **Note on C-numbering:** `_CANON.md §5` lists only **C1, C2, C3, C6, C7, C8** explicitly; the fuller
> **C1–C10** set (including C4 free-data, C5 advisory, C9 LoRa band, C10 honesty-rules) is from
> `03_requirements_and_scope.md §3.3`. The task brief asked for "C1–C9"; C10 is included for completeness
> as it is sourced in chapter 03.

---

### Cross-references
Decision function and the single operating point: 05b §29, 10.1. Shield: 05b §30, 10.3.4, 13 (Bug #20).
Conformal toolkit: 12.2.6, 12.7, 13 (Bug #13). Admission gate / baselines: 12.4–12.6, 13 (Bug #11).
IP-alerting verdict and tiers: 08. Bug ledger (#0–#32): 13. Workstream mapping and canonical facts:
`_CANON.md §3,§4,§5`.
