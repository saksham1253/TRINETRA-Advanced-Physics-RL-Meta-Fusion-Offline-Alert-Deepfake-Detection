# CASCADE_SPEC.md — Disaster-cascade specification for the TRINETRA / HIMKAVACH video

> Precise, sourced description of what happens inside TRINETRA (alt. name HIMKAVACH) when a disaster
> occurs. Scenario: **combined wildfire + rain-induced landslide in the Uttarakhand Himalaya AOI**
> (bbox 78.5,29.5,80.2,30.8; 2021 pre-monsoon fire season) — AOI per
> [`viz/LAYER_MAP.md:4`](../LAYER_MAP.md#L4).
>
> **Reading rule.** Every factual claim below carries a `file:line` citation. Where the repo does not
> contain a value, it is written **NOT IN REPO**. No threshold has been invented.
>
> **Global honesty caveat (carry on screen).** The research program's own report states verbatim:
> *"Nothing was built, trained, or measured."*
> ([`FINAL_REPORT.md:3`](../../FINAL_REPORT.md#L3); reinforced
> [`docs/_CANON.md:17`](../../docs/_CANON.md#L17), [`docs/_CANON.md:25`](../../docs/_CANON.md#L25)).
> A reference numpy code core exists and runs (128 tests pass, 6 CI gates pass), but **no ML model was
> trained and no dataset was downloaded** ([`docs/_CANON.md:37-44`](../../docs/_CANON.md#L37-L44)).
> The system is **ADVISORY, human-in-the-loop, and NEVER autonomous** (Rule R19,
> [`docs/_CANON.md:78`](../../docs/_CANON.md#L78),
> [`docs/02_system_architecture.md:22-23`](../../docs/02_system_architecture.md#L22-L23)).

---

## 1. Workstreams WS1–WS8 (one line each)

Workstream numbering follows the folder/artifact scheme indexed in
[`ws1_physics/README.md:7-13`](../../ws1_physics/README.md#L7-L13). Note that `docs/_CANON.md` maps three
different numbering schemes ([`docs/_CANON.md:46-58`](../../docs/_CANON.md#L46-L58)); the code package names
cited here are the ground truth.

| WS | Ingests | Outputs | Status | Key source |
|----|---------|---------|--------|------------|
| **WS1 physics** (fire `ws1a_firephys` + geo `ws1b_geophys`) | DEM slope β, soil params, rainfall I–D, IoT/EO-derived fluxes, detector confidence, wind U | Advisory physics probability `p_phys` + FS, Caine ratio, t_failure, Byram Nc regime, flame height | **SIMULATED** (real numpy code, no observation, no measured skill) | [`viz/render/public/data/l12_dfd.json:14`](../render/public/data/l12_dfd.json#L14); [`ws1_physics/README.md:7`](../../ws1_physics/README.md#L7) |
| **WS2 deepfake / media** (`ws2_deepfake`, `deep/deepfake_net.py`) | Inbound social-media / media | `p_fake` with trust **capped at reliability 0.40**; corroborates/suppresses only, can NEVER gate a life-safety alert | **SIMULATED** (reference arch; no trained weights) | [`trinetra/.../deep/deepfake_net.py:22`](../../trinetra/src/trinetra/deep/deepfake_net.py#L22), [`:5`](../../trinetra/src/trinetra/deep/deepfake_net.py#L5); [`l12_dfd.json:13`](../render/public/data/l12_dfd.json#L13) |
| **WS3 offline alerting** (`ws3_alert`) | Approved decision + zone | Tiered dissemination: siren → LAN/mesh → cell-broadcast → DTN store-carry-forward; CAP XML refuses to emit without `APPROVED:` operator token | **SIMULATED**; no acoustic range model in code → reach rings ILLUSTRATIVE | [`docs/02_system_architecture.md:136-141`](../../docs/02_system_architecture.md#L136-L141); [`viz/LAYER_MAP.md:138-140`](../LAYER_MAP.md#L138-L140); [`l12_dfd.json:19`](../render/public/data/l12_dfd.json#L19) |
| **WS4 CCTV / River-Eye** (`ws4_cctv`, `deep/fire_cnn.py`) | Edge camera frames (fire/smoke, LSPIV river stage) | Detector confidence + temporal event validation (F-11/F-12/F-16) | **SIMULATED**; FireSmokeNet reference arch, **no trained weights → no real detections** | [`viz/LAYER_MAP.md:109`](../LAYER_MAP.md#L109), [`:111`](../LAYER_MAP.md#L111); [`l12_dfd.json:12`](../render/public/data/l12_dfd.json#L12) |
| **WS5 RL + meta-fusion** (`ws5_fusion_rl`, `deep/offline_rl.py`) | All expert outputs + RL action-logits/q-values | Gated meta-fusion risk `fused.p` + uncertainty `u_star`; advisory evacuation routing | **SIMULATED**; **no trained RL policy exists** → rule baseline only | [`viz/LAYER_MAP.md:151-152`](../LAYER_MAP.md#L151-L152); [`l12_dfd.json:16`](../render/public/data/l12_dfd.json#L16), [`:20-21`](../render/public/data/l12_dfd.json#L20-L21) |
| **WS6 robustness** (`ws6_robust`) | Fused risk, calibration set, data stream | Per-zone Mondrian conformal risk (honest coverage, not a "guarantee") + drift/CUSUM flag | **SIMULATED** | [`docs/02_system_architecture.md:54`](../../docs/02_system_architecture.md#L54), [`:146-147`](../../docs/02_system_architecture.md#L146-L147) |
| **WS7 IoT** (`ws7_iot`) | ₹2000 LoRa nodes: rain gauge, tilt, soil moisture, piezometer, thermal (edge) | Compact LoRa codewords (IN865–867 MHz); on-node Z-score/FS/1-v pre-screen; LoRa rain gauges bias-correct satellite IMERG | **REAL** (sensing design/code) | [`l12_dfd.json:11`](../render/public/data/l12_dfd.json#L11); [`docs/02_system_architecture.md:92-95`](../../docs/02_system_architecture.md#L92-L95), [`:120`](../../docs/02_system_architecture.md#L120) |
| **WS8 anomaly** (`ws8_anomaly`, `deep/anomaly_deep.py`) | EO datacube features (InSAR core) | Anomaly score ensemble: forecast-residual + Deep-SVDD + isolation forest + XGBoost | **SIMULATED** (EO change + drift monitor) | [`docs/02_system_architecture.md:48`](../../docs/02_system_architecture.md#L48); [`analysis/00_system_model.md:53`](../../analysis/00_system_model.md#L53); [`l12_dfd.json:15`](../render/public/data/l12_dfd.json#L15) |

Sensing inputs (EO/satellite) feeding WS1/WS8 are **REAL** streams: Sentinel-1/2, DEM, ERA5-Land, FIRMS,
MODIS/VIIRS ([`l12_dfd.json:10`](../render/public/data/l12_dfd.json#L10)).

---

## 2. End-to-end trigger chain — wildfire + rain-induced landslide (Uttarakhand AOI)

Ordered steps. Each step: **(a) trigger/input → (b) workstream/node → (c) concrete signal/threshold/number
from the repo → (d) handoff to next step.** The orchestrator assembles a list of `ExpertOutput` and calls
the single `decide()` function; there is exactly one decision path and the shield can only RAISE
([`trinetra/.../pipeline/orchestrator.py:1-5`](../../trinetra/src/trinetra/pipeline/orchestrator.py#L1-L5),
[`:29-44`](../../trinetra/src/trinetra/pipeline/orchestrator.py#L29-L44)).

### FIRE BRANCH (fast loop, near-real-time at the gateway)

1. **(a)** Wildfire ignition in AOI; smoke/heat appears on edge CCTV + IoT nodes. **(b)** WS4 CCTV detector + temporal validator → detector confidence; WS7 nodes report smoke+heat. **(c)** Scenario fire-physics params: total convective `Q_c=50,000 kW`, pool diameter `D=10 m`, wind `U=5 m/s`, line-source `Q_c=1000 kW/m` ([`l6_physics.json:34-41`](../render/public/data/l6_physics.json#L34-L41)). **(d)** → `FireInputs(detector_conf, multi_node_agree, Q_c_kW_per_m, wind_U_ms)` into the fire gate ([`ws1a_firephys/gate.py:20-31`](../../trinetra/src/trinetra/ws1a_firephys/gate.py#L20-L31)).

2. **(a)** Fire regime plausibility check. **(b)** WS1a `fire_gate` via `byram_convection_number`. **(c)** Byram `N_c = 2·g·Q_c / (ρ·cp·T∞·U³)`; **N_c>~2 ⇒ plume-dominated (buoyant); N_c<~1 ⇒ wind-dominated** ([`established_ef.py:40`](../../trinetra/src/trinetra/ws1a_firephys/established_ef.py#L40), [`:36-45`](../../trinetra/src/trinetra/ws1a_firephys/established_ef.py#L36-L45)). Scenario value **N_c = 0.4464 ⇒ "wind-dominated"** ([`l6_physics.json:45-46`](../render/public/data/l6_physics.json#L45-L46)); consistency is down-weighted by `clip(N_c/2, 0.3, 1.0)` ([`ws1a_firephys/gate.py:48-52`](../../trinetra/src/trinetra/ws1a_firephys/gate.py#L48-L52)). Heskestad flame height `L = 0.235·Q^0.4 − 1.02·D` = **7.61 m** ([`established_ef.py:16-18`](../../trinetra/src/trinetra/ws1a_firephys/established_ef.py#L16-L18); [`l6_physics.json:43`](../render/public/data/l6_physics.json#L43)); Strouhal puffing `1.5/√D` = 0.4743 Hz ([`established_ef.py:21-23`](../../trinetra/src/trinetra/ws1a_firephys/established_ef.py#L21-L23); [`l6_physics.json:44`](../render/public/data/l6_physics.json#L44)). **(d)** → advisory `ExpertOutput(source="fire_phys", cls=A)` with physics-consistency `c` ([`ws1a_firephys/gate.py:77-79`](../../trinetra/src/trinetra/ws1a_firephys/gate.py#L77-L79)).

### LANDSLIDE BRANCH (slow loop, per satellite pass + IoT heartbeat)

3. **(a)** Monsoon/convective rain over the burn-affected slope; EO precip (GPM IMERG) **bias-corrected by WS7 LoRa rain gauges**. **(b)** WS7 ground IoT → WS1b geo gate. **(c)** Scenario rainfall `I = 8 mm/h` over `D = 6 h` ([`l6_physics.json:487-488`](../render/public/data/l6_physics.json#L487-L488)); calibration loop LoRa→IMERG per [`docs/02_system_architecture.md:120`](../../docs/02_system_architecture.md#L120). **(d)** → `GeoInputs` (slope, soil, infiltration, I–D) into `geo_gate` ([`ws1b_geophys/gate.py:24-37`](../../trinetra/src/trinetra/ws1b_geophys/gate.py#L24-L37)).

4. **(a)** Rainfall intensity–duration exceedance. **(b)** WS1b `caine_exceedance`. **(c)** Caine `I = a·D^(−b)`; code defaults `a=14.0, b=0.39` ([`config.py:23`](../../trinetra/src/trinetra/common/config.py#L23); [`caine.py:1-5`](../../trinetra/src/trinetra/ws1b_geophys/caine.py#L1-L5)), scenario fields use `a=14.82, b=0.39` **flagged ILLUSTRATIVE placeholder, NOT locally calibrated** ([`l6_physics.json:484-486`](../render/public/data/l6_physics.json#L484-L486)). Exceedance **ratio I/I_threshold = 1.0857 > 1 ⇒ threshold exceeded** ([`l6_physics.json:489-490`](../render/public/data/l6_physics.json#L489-L490)). Soft term `p_caine = clip(ratio − 0.5, 0, 1)` ([`ws1b_geophys/gate.py:60-65`](../../trinetra/src/trinetra/ws1b_geophys/gate.py#L60-L65)). **(d)** → feeds pore-pressure + physics fusion.

5. **(a)** Transient rainfall infiltration raises pore pressure. **(b)** WS1b `iverson.transient_head` → `fs.pore_pressure_from_head`. **(c)** Iverson (2000): slope enters **ONLY** via `D1 = D0/cos²(β)` (bug-guard: no extra `cos²β/cosβ`) ([`iverson.py:3-9`](../../trinetra/src/trinetra/ws1b_geophys/iverson.py#L3-L9), [`:28-30`](../../trinetra/src/trinetra/ws1b_geophys/iverson.py#L28-L30)). Scenario infiltration `D0=1e-4 m²/s, K_z=1e-5 m/s, I_z=5e-6 m/s, z=2 m, 6 h rain` ([`l6_physics.json:314-322`](../render/public/data/l6_physics.json#L314-L322)). **(d)** → `u_w` into Factor-of-Safety.

6. **(a)** Slope stability evaluation. **(b)** WS1b `factor_of_safety`. **(c)** `FS = [c' + σ'_n·tan φ'] / (γ·z·sin β·cos β)`, `σ'_n = γ·z·cos²β − u_w + σ_s`; **FS<1 ⇒ unstable** ([`fs.py:1-9`](../../trinetra/src/trinetra/ws1b_geophys/fs.py#L1-L9), [`:23-39`](../../trinetra/src/trinetra/ws1b_geophys/fs.py#L23-L39)). Scenario soil `c'=5 kPa, φ'=32°, γ=18 kN/m³` ([`l6_physics.json:315-317`](../render/public/data/l6_physics.json#L315-L317)); wet FS crosses below 1 between slope **β=37° (FS_wet=1.0011)** and **β=38° (FS_wet=0.9664)** ([`l6_physics.json:436-437`](../render/public/data/l6_physics.json#L436-L437) with β index [`:358-359`](../render/public/data/l6_physics.json#L358-L359)). Physics-probability map `p_fs = sigmoid(4·(1−FS))` (FS=1→0.5, FS<1→>0.5) ([`ws1b_geophys/gate.py:56-58`](../../trinetra/src/trinetra/ws1b_geophys/gate.py#L56-L58)). **(d)** → `FS` to the hard shield AND `p_phys` to fusion.

7. **(a)** Optional creep/precursor monitoring. **(b)** WS1b `fukuzono.inverse_velocity_fit`. **(c)** Fukuzono/Voight `1/v = A(α−1)(t_f − t)`, **α=2 ⇒ 1/v linear**; returns `t_failure` with a 95% prediction interval ([`fukuzono.py:3-5`](../../trinetra/src/trinetra/ws1b_geophys/fukuzono.py#L3-L5), [`:59-66`](../../trinetra/src/trinetra/ws1b_geophys/fukuzono.py#L59-L66)); default `fukuzono_alpha=2.0` ([`config.py:23`](../../trinetra/src/trinetra/common/config.py#L23)). Soft term `p_fk = clip(1 − lead/48h, 0, 1)·r²` ([`ws1b_geophys/gate.py:67-73`](../../trinetra/src/trinetra/ws1b_geophys/gate.py#L67-L73)). **(d)** → physics sub-signal.

8. **(a)** Combine the geo physics sub-signals. **(b)** WS1b `geo_gate`. **(c)** Conservative **noisy-OR** `p_phys = 1 − Π(1 − p_i)` over `[p_fs, p_caine, p_fk]` (monotone, never under-warns) ([`ws1b_geophys/gate.py:75-77`](../../trinetra/src/trinetra/ws1b_geophys/gate.py#L75-L77)). **(d)** → advisory `ExpertOutput(source="geo_phys", cls=A)` ([`ws1b_geophys/gate.py:84-88`](../../trinetra/src/trinetra/ws1b_geophys/gate.py#L84-L88)).

### SHARED FUSION / DECISION / HUMAN GATE

9. **(a)** EO datacube change signal (independent modality). **(b)** WS8 anomaly ensemble. **(c)** forecast-residual + Deep-SVDD + isolation forest + XGBoost; latest-sample score as alarm evidence ([`orchestrator.py:23-26`](../../trinetra/src/trinetra/pipeline/orchestrator.py#L23-L26); [`analysis/00_system_model.md:53`](../../analysis/00_system_model.md#L53)). **(d)** → `ExpertOutput(source="anomaly", cls=DATA)`.

10. **(a)** Optional low-trust media signal. **(b)** WS2 deepfake scorer. **(c)** `p_fake` with trust **hard-capped at reliability 0.40** — corroborates/suppresses only, can NEVER gate a life-safety alert ([`deep/deepfake_net.py:22`](../../trinetra/src/trinetra/deep/deepfake_net.py#L22), [`:5`](../../trinetra/src/trinetra/deep/deepfake_net.py#L5)). **(d)** → low-trust advisory feature into fusion.

11. **(a)** All experts assembled (physics, anomaly, [RL logits], [WS2/WS4]). **(b)** WS5 meta-fusion `fuse()`. **(c)** Default **FM-1 precision/reliability-weighted mean** (Class B; PHARAOH Class-C default OFF) → fused risk `p` + conflict-aware uncertainty `u_star` ([`fusion_models.py:1-6`](../../trinetra/src/trinetra/ws5_fusion_rl/fusion_models.py#L1-L6), [`:30-40`](../../trinetra/src/trinetra/ws5_fusion_rl/fusion_models.py#L30-L40), [`:43-54`](../../trinetra/src/trinetra/ws5_fusion_rl/fusion_models.py#L43-L54)); meta-head emits a **bounded residual** over physics base action `a₀`: `â = clip(a₀ + residual)` ([`docs/02_system_architecture.md:76-80`](../../docs/02_system_architecture.md#L76-L80); [`TRINETRA_MetaFusion_Design.md:80-93`](../../TRINETRA_MetaFusion_Design.md#L80-L93)). **(d)** → `fused.p`, `fused.u_star` into the decision.

12. **(a)** Conformal mapping of fused risk to an alert level. **(b)** WS6/WS5 `conformal_level`. **(c)** Escalation points from the cost-loss alarm threshold **p\* = C_FA/(C_FA+C_miss) = 5/105 ≈ 0.0476** (C_FA=5, C_miss=100): thresholds `(t_yellow, t_orange, t_red) = (p*, 4·p*, 10·p*)` → Green/Yellow/Orange/Red ([`decision.py:24-40`](../../trinetra/src/trinetra/ws5_fusion_rl/decision.py#L24-L40); [`config.py:20`](../../trinetra/src/trinetra/common/config.py#L20), [`:46-48`](../../trinetra/src/trinetra/common/config.py#L46-L48); [`analysis/00_system_model.md:48`](../../analysis/00_system_model.md#L48)). **(d)** → provisional `point` level.

13. **(a)** Deterministic hard safety overrides. **(b)** WS5 `shield_floor` (post-posed, monotone — can only RAISE). **(c)** **FS<1 → ≥Orange**; **tilt_rate>5°/day corroborated by ≥2 nodes → Red**; **24 h rain>150 mm on high-susceptibility slope → ≥Orange**; **GLOF lake-drop + downstream stage-jump → Red**; **fire corroborated by ≥2 nodes (smoke+heat) → ≥Orange** ([`shield.py:26-50`](../../trinetra/src/trinetra/ws5_fusion_rl/shield.py#L26-L50)). A single uncorroborated node cannot reach Red ([`shield.py:4-5`](../../trinetra/src/trinetra/ws5_fusion_rl/shield.py#L4-L5)). **(d)** → `shield.floor`.

14. **(a)** Final single decision. **(b)** WS5 `decide()`. **(c)** **`level = max(conformal_level(fused_risk, p*), shield_floor)`** ([`decision.py:3`](../../trinetra/src/trinetra/ws5_fusion_rl/decision.py#L3), [`:84-86`](../../trinetra/src/trinetra/ws5_fusion_rl/decision.py#L84-L86); [`docs/_CANON.md:73`](../../docs/_CANON.md#L73); [`docs/02_system_architecture.md:63`](../../docs/02_system_architecture.md#L63)). `uncertain=True` (abstain + escalate to human) if no experts available, `u_star>0.6`, or drift — but it is **never silent** ([`decision.py:72`](../../trinetra/src/trinetra/ws5_fusion_rl/decision.py#L72), [`:88`](../../trinetra/src/trinetra/ws5_fusion_rl/decision.py#L88), [`:1-8`](../../trinetra/src/trinetra/ws5_fusion_rl/decision.py#L1-L8)). **(d)** → advisory `Decision` (level + evidence + shield reason + trace id).

15. **(a)** HUMAN-IN-THE-LOOP GATE (mandatory). **(b)** Operator UI → WS3 CAP builder. **(c)** `require_human_approval` is **hard-wired True; config cannot disable it** ([`config.py:28`](../../trinetra/src/trinetra/common/config.py#L28), [`:50-52`](../../trinetra/src/trinetra/common/config.py#L50-L52)); the CAP builder **refuses to emit without an `APPROVED:` operator token** ([`docs/02_system_architecture.md:136-138`](../../docs/02_system_architecture.md#L136-L138)); offline dispatch may drive a LOCAL siren via the shield floor but **public CAP is still deferred to a human (Rule 19)** ([`orchestrator.py:54-66`](../../trinetra/src/trinetra/pipeline/orchestrator.py#L54-L66)). **(d)** → on approval, WS3 tiered dissemination.

16. **(a)** Approved alert. **(b)** WS3 alerting + WS5 advisory routing. **(c)** siren → LAN/mesh → cell-broadcast → DTN store-carry-forward, offline-path independent of the cloud (constraint C1) ([`docs/02_system_architecture.md:118-119`](../../docs/02_system_architecture.md#L118-L119); [`l12_dfd.json:19`](../render/public/data/l12_dfd.json#L19)); evacuation routing is a **rule baseline over OSM roads — no trained policy** ([`l12_dfd.json:20-21`](../render/public/data/l12_dfd.json#L20-L21); [`viz/LAYER_MAP.md:151-152`](../LAYER_MAP.md#L151-L152)). **(d)** → people-at-risk advisory to responders.

**Advisory / non-autonomy restated:** the system produces an advisory level and **never originates a public
alert on its own** ([`docs/02_system_architecture.md:22-23`](../../docs/02_system_architecture.md#L22-L23);
[`docs/_CANON.md:78`](../../docs/_CANON.md#L78)).

---

## 3. Exact fusion / decision rule strings (verbatim, with citation)

- **Single decision function:**
  `level(state s) = max( conformal_level( fused_risk(s), p* ), shield_floor(s) )`
  ([`docs/02_system_architecture.md:63`](../../docs/02_system_architecture.md#L63);
  [`decision.py:3`](../../trinetra/src/trinetra/ws5_fusion_rl/decision.py#L3);
  [`docs/_CANON.md:73`](../../docs/_CANON.md#L73)).
- **Cost-loss alarm threshold:** `p* = C_FA/(C_FA + C_miss) = 5/105 ≈ 0.0476`, with `C_FA=5, C_miss=100`
  ([`config.py:20`](../../trinetra/src/trinetra/common/config.py#L20),
  [`:46-48`](../../trinetra/src/trinetra/common/config.py#L46-L48);
  [`docs/_CANON.md:74`](../../docs/_CANON.md#L74);
  [`analysis/00_system_model.md:48`](../../analysis/00_system_model.md#L48)).
- **Level cut points:** `(t_yellow, t_orange, t_red) = (p*, 4·p*, 10·p*)` unless replaced by
  conformal-risk-calibrated cut points
  ([`decision.py:30-40`](../../trinetra/src/trinetra/ws5_fusion_rl/decision.py#L30-L40)).
- **Meta-fusion residual form:** `â = clip( a₀ + residual )` (residual-policy learning; residual hard-clipped
  so a mis-trained head cannot dominate the physics base)
  ([`docs/02_system_architecture.md:78-80`](../../docs/02_system_architecture.md#L78-L80);
  [`TRINETRA_MetaFusion_Design.md:84-93`](../../TRINETRA_MetaFusion_Design.md#L84-L93)).
- **Geo physics sub-fusion (noisy-OR):** `p_phys = 1 − Π_i (1 − p_i)` over `[p_fs, p_caine, p_fk]`
  ([`ws1b_geophys/gate.py:75-77`](../../trinetra/src/trinetra/ws1b_geophys/gate.py#L75-L77)).
- **Shield floors (monotone, RAISE-only):** FS<1→Orange; tilt>5°/day ∧ ≥2 nodes→Red; 24 h rain>150 mm ∧
  high-susc→Orange; GLOF lake-drop ∧ stage-jump→Red; fire multi-node→Orange
  ([`shield.py:30-47`](../../trinetra/src/trinetra/ws5_fusion_rl/shield.py#L30-L47)).
- **Deepfake trust cap:** `max_reliability = 0.4`
  ([`deep/deepfake_net.py:22`](../../trinetra/src/trinetra/deep/deepfake_net.py#L22)).

---

## 4. Node + edge list for the data-flow diagram

Reconciled with [`viz/render/public/data/l12_dfd.json`](../render/public/data/l12_dfd.json) (which is tagged
`ILLUSTRATIVE`, authored from `02_system_architecture.md` + `_CANON.md`,
[`l12_dfd.json:2-8`](../render/public/data/l12_dfd.json#L2-L8)). The DFD groups below are the authoritative
set; the "cascade role" column adds the sensing/perception/physics/fusion/decision/action grouping the video
needs. The `rl` node is kept in the `action` group per the DFD even though its code lives in WS5.

| id | label | group | REAL/SIM | source |
|----|-------|-------|----------|--------|
| `eo` | EO / satellite streams (S1/S2, DEM, ERA5-Land, FIRMS, MODIS/VIIRS) | sensing | **REAL** | [`l12_dfd.json:10`](../render/public/data/l12_dfd.json#L10) |
| `iot` | Ground IoT / sensors (WS7 LoRa: rain, tilt, soil, thermal) | sensing | **REAL** | [`l12_dfd.json:11`](../render/public/data/l12_dfd.json#L11) |
| `cctv` | WS4 CCTV fire/smoke (FireSmokeNet; no trained weights) | perception | **SIMULATED** | [`l12_dfd.json:12`](../render/public/data/l12_dfd.json#L12) |
| `social` | WS2 social-media intake (AuthenticityNet; reliability cap 0.40) | perception | **SIMULATED** | [`l12_dfd.json:13`](../render/public/data/l12_dfd.json#L13) |
| `ws1` | WS1 physics models ×6 (fire Heskestad/Byram + geo FS/Iverson/Caine/Fukuzono) | physics | **SIMULATED** | [`l12_dfd.json:14`](../render/public/data/l12_dfd.json#L14) |
| `anom` | WS8 anomaly / drift (EO change + WS6/WS8 monitor) | physics | **SIMULATED** | [`l12_dfd.json:15`](../render/public/data/l12_dfd.json#L15) |
| `fusion` | WS5 meta-fusion (gated multimodal + conformal uncertainty) | fusion | **SIMULATED** | [`l12_dfd.json:16`](../render/public/data/l12_dfd.json#L16) |
| `decision` | Decision + shield (`level = max(conformal_level(risk, p*≈0.0476), shield_floor)`) | decision | **SIMULATED** | [`l12_dfd.json:17`](../render/public/data/l12_dfd.json#L17) |
| `human` | Human operator gate (mandatory for any public message, R19) | decision | **REAL** | [`l12_dfd.json:18`](../render/public/data/l12_dfd.json#L18) |
| `alert` | WS3 tiered alerting (siren → LAN/mesh → cell-broadcast → DTN) | action | **SIMULATED** | [`l12_dfd.json:19`](../render/public/data/l12_dfd.json#L19) |
| `rl` | WS5 advisory routing (rule-baseline evacuation over OSM roads) | action | **SIMULATED** | [`l12_dfd.json:20`](../render/public/data/l12_dfd.json#L20) |

**Edges** ([`l12_dfd.json:22-34`](../render/public/data/l12_dfd.json#L22-L34)):
`eo→ws1`, `iot→ws1`, `eo→anom`, `cctv→fusion`, `social→fusion`, `ws1→fusion`, `anom→fusion`,
`fusion→decision`, `decision→human`, `human→alert`, `human→rl`.

(Note the DFD routes `cctv`/`social` directly into `fusion`, and gates `alert`/`rl` strictly behind
`human` — matching the single-decision + human-gate contract above.)

---

## 5. Honesty ledger

| Cascade element | Classification | Basis |
|-----------------|----------------|-------|
| EO satellite streams (S1/S2, DEM, ERA5-Land, FIRMS, MODIS/VIIRS) | **REAL data** | [`l12_dfd.json:10`](../render/public/data/l12_dfd.json#L10); [`viz/LAYER_MAP.md:70-79`](../LAYER_MAP.md#L70-L79) |
| WS7 ground IoT sensing / LoRa design | **REAL** (design/code; ₹ BOM figures are `[EST]`) | [`l12_dfd.json:11`](../render/public/data/l12_dfd.json#L11); [`docs/_CANON.md:129-131`](../../docs/_CANON.md#L129-L131) |
| Human operator gate (R19) | **REAL** (hard-wired) | [`config.py:28`](../../trinetra/src/trinetra/common/config.py#L28), [`:50-52`](../../trinetra/src/trinetra/common/config.py#L50-L52) |
| WS1 physics fields (FS, Iverson, Caine, Fukuzono, Heskestad, Byram) | **SIMULATED** — real numpy code output, NOT an observation, NO measured skill | [`l6_physics.json:4-6`](../render/public/data/l6_physics.json#L4-L6); [`viz/LAYER_MAP.md:85`](../LAYER_MAP.md#L85) |
| WS5 fusion / decision / conformal / shield | **SIMULATED** (code runs; no trained model) | [`docs/_CANON.md:37-40`](../../docs/_CANON.md#L37-L40); [`l12_dfd.json:16-17`](../render/public/data/l12_dfd.json#L16-L17) |
| WS4 CCTV detections | **SIMULATED / ILLUSTRATIVE** — reference arch, **no trained weights → no real detections**; camera FOV geometry is ILLUSTRATIVE | [`viz/LAYER_MAP.md:104`](../LAYER_MAP.md#L104), [`:109-111`](../LAYER_MAP.md#L109-L111) |
| WS2 deepfake score | **SIMULATED** — reference arch; trust capped 0.40, never gates an alert | [`deep/deepfake_net.py:5`](../../trinetra/src/trinetra/deep/deepfake_net.py#L5), [`:22`](../../trinetra/src/trinetra/deep/deepfake_net.py#L22) |
| WS8 anomaly stack | **SIMULATED** (no trained model) | [`l12_dfd.json:15`](../render/public/data/l12_dfd.json#L15); [`docs/_CANON.md:25`](../../docs/_CANON.md#L25) |
| Caine coefficients `a=14.82, b=0.39` | **ILLUSTRATIVE placeholder — NOT locally calibrated** | [`l6_physics.json:484-486`](../render/public/data/l6_physics.json#L484-L486); [`caine.py:3-5`](../../trinetra/src/trinetra/ws1b_geophys/caine.py#L3-L5) |
| WS5 RL evacuation routing | **SIMULATED / ILLUSTRATIVE** — rule baseline over REAL OSM roads; **no trained RL policy** | [`l12_dfd.json:20-21`](../render/public/data/l12_dfd.json#L20-L21); [`viz/LAYER_MAP.md:151-156`](../LAYER_MAP.md#L151-L156) |
| WS3 alert reach rings | **ILLUSTRATIVE geometry** — no acoustic/radio range model in code; ranges source-reported only | [`viz/LAYER_MAP.md:138-146`](../LAYER_MAP.md#L138-L146) |
| L12 high-level DFD overlay | **ILLUSTRATIVE** (conceptual flow; no performance numbers implied) | [`l12_dfd.json:3-6`](../render/public/data/l12_dfd.json#L3-L6) |
| Any accuracy / skill / latency / cost number | **NOT MEASURED** — "Nothing was built, trained, or measured" | [`FINAL_REPORT.md:3`](../../FINAL_REPORT.md#L3); [`docs/_CANON.md:25`](../../docs/_CANON.md#L25) |

### Items explicitly NOT IN REPO
- No trained ML weights for any workstream (WS2/WS4/WS5-RL/WS8) — reference architectures only
  ([`docs/_CANON.md:25`](../../docs/_CANON.md#L25); [`viz/LAYER_MAP.md:182`](../LAYER_MAP.md#L182)).
- No acoustic/radio propagation (siren/LoRa reach) model in code
  ([`viz/LAYER_MAP.md:138-140`](../LAYER_MAP.md#L138-L140)).
- Locally-calibrated Caine `a,b` constants — **NOT IN REPO** (placeholders only).
- Measured people-at-risk / lead-time / FAR / coverage numbers — **NOT IN REPO** (not measured).

---

*All numeric scenario values trace to `viz/render/public/data/l6_physics.json`, generated
2026-10-10 by `viz/pipeline/gen_physics_fields.py` running the real numpy core
([`l6_physics.json:7-8`](../render/public/data/l6_physics.json#L7-L8)); all thresholds trace to the cited
code and `docs/_CANON.md`.*
