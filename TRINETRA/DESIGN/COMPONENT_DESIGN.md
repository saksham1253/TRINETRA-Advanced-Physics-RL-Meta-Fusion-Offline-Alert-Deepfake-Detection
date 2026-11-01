# TRINETRA / HIMKAVACH — COMPONENT & INTERFACE DESIGN (CDD) v1.0
> The build-bridging layer between `DESIGN/HLD.md` (architecture) / `DESIGN/LLD.md` (module internals) and
> the codebase. Specifies concrete data contracts, inter-tier protocols, sequence flows, and per-component
> algorithms/pseudocode. Honesty/safety rules bind: R16 (no own perf claims), R19 (advisory/human-in-loop/
> fail-safe/authenticated), R20 (Class A/B/C), R21 (novelty=search claim). Nothing here is measured.

---
## 1. Component map (one line each)
| ID | Component | Tier | WS | Class/trust |
|----|-----------|------|----|-------------|
| C-ENC | EO foundation encoder (frozen) | cloud | WS1b/WS8 | data-driven |
| C-ANO | Anomaly ensemble (fcst-resid+SVDD+iForest+XGB) | cloud/gw | WS8 | data-driven |
| C-GEO | Geo physics gate | gw/node | WS1b | A/B/C |
| C-FIRE | Fire physics layer | gw/node | WS1a | A + C(soft) |
| C-CCTV | Edge detector + temporal validator + IR flicker | gw | WS4 | data-driven |
| C-CAL | Conformal calibrator + drift monitor | gw/cloud | WS6 | honest coverage |
| C-RL | Offline-RL alarm policy | cloud(train)/gw(run) | WS5 | advisory |
| C-SHD | Hard safety shield | gw/node | WS3/WS5 | deterministic |
| C-FUS | Meta-fusion head (GMF+PHARAOH+FM) | gw | WS5 | advisory |
| C-DEC | Decision function (single) | gw | WS5/WS3 | advisory |
| C-ALERT | CAP/SACHET builder+signer, DTN, siren | gw | WS3 | human-gated |
| C-NODE | IoT node firmware (Tier-0 screen) | node | WS7 | data-driven |
| C-DF | Deepfake/misinfo scorer | gw | WS2 | low-trust advisory |
| C-OPS | Operator decision-support UI | gw/cloud | WS3 | human |

Dependency edges: C-ENC→C-ANO→(C-GEO|C-FIRE)→C-FUS; C-CCTV→C-FIRE→C-FUS; C-NODE→(LoRa)→C-GEO/C-FIRE→C-FUS;
C-RL→C-FUS; C-FUS→C-CAL→C-DEC←C-SHD; C-DEC→C-OPS→(human)→C-ALERT; C-DF→C-FUS(low-trust) & C-OPS.

---
## 2. Canonical data contracts (JSON; versioned, `schema_version` required)
### 2.1 SensorReading (node → gateway, one LoRa payload decoded)
```json
{ "schema_version":"1.0", "node_id":"SS-UK-00123", "zone_id":"UK-CHX-07",
  "t":"2026-10-10T08:46:00Z", "fw":"0.3.1", "batt_mV":3920, "rssi":-97, "snr":7.5,
  "readings": { "tilt_deg":[1.2,0.4], "tilt_rate_dps":0.08, "soil_vwc":[0.31,0.28],
                "piezo_kPa":42.1, "rain_mm_15m":6.4, "temp_C":14.2, "pressure_hPa":812.0,
                "accel_rms":0.02, "fire":{"temp_C":null,"gas_ppm":null,"smoke":null} },
  "health": { "tilt":"ok","soil":"ok","piezo":"degraded","rain":"ok" },
  "edge_flag": {"level":"NONE","rule":null},   // Tier-0 pre-screen; NONE|WATCH|LOCAL_SIREN
  "seq":10492, "sig":"ed25519:…" }             // signed; replay-protected by (node_id,seq)
```
### 2.2 Evidence (fused per-zone bundle; internal) — see LLD §0 `Evidence`
Adds `window:{start,end}`, `sources:[…]`, `fold_id` (spatial-CV), and a `missing:[modality…]` list.
### 2.3 ExpertOutput — see LLD §0 (`p,u,c,r,cls,source`). Every expert MUST emit all fields; missing→`available=false`.
### 2.4 Decision (gateway → operator UI / log)
```json
{ "schema_version":"1.0", "zone_id":"UK-CHX-07", "t":"…Z", "hazard":"LANDSLIDE",
  "level":"ORANGE", "risk":0.37, "advisory":true,
  "conformal":{"set":["ORANGE","RED"],"coverage_target":0.9,"reliability":"Medium"},
  "shield":{"raised":true,"floor":"ORANGE","reason":"FS<1 at node SS-UK-00123 + 24h rain>150mm"},
  "contributions":[ {"source":"geo_phys","p":0.41,"u":0.2,"c":1.0,"r":0.9,"cls":"A"},
                    {"source":"anomaly","p":0.33,"u":0.3,"c":0.8,"r":0.7,"cls":"data"},
                    {"source":"rl_policy","p":0.36,"u":0.25,"c":0.9,"r":0.6,"cls":"advisory"} ],
  "class_flags":{"used_classC":false}, "model_versions":{…}, "trace_id":"…" }
```
### 2.5 AlertRecord (CAP mapping; only after human approval)
```json
{ "cap_id":"urn:trinetra:UK-CHX-07:20261010T0846Z", "status":"Actual", "msgType":"Alert",
  "scope":"Public", "severity":"Severe", "urgency":"Expected", "certainty":"Likely",
  "area":{"zone_id":"UK-CHX-07","polygon":"…","geocode":"…"}, "approved_by":"operator:SDMA-UK-14",
  "channels":["SIREN","LORA_MESH","SACHET"], "signed":"…", "issued":"…Z" }
```
Mapping rule (deterministic): GREEN→(no CAP) · YELLOW→Minor/Future/Possible · ORANGE→Severe/Expected/Likely
· RED→Extreme/Immediate/Observed. Severity/urgency/certainty NEVER inferred by a model from free text.

---
## 3. Inter-tier interfaces & protocols
### 3.1 Node ⇄ Gateway (LoRa, offline path) — C4 band IN865–867
- Uplink: compact binary frame (CBOR/bit-packed) decoding to §2.1; ≤51 B payload target (DR-aware);
  fields quantized (tilt 0.01°, rain 0.1 mm). Signed (Ed25519, key provisioned at flashing). `(node_id,seq)`
  dedup + replay window. ACK optional; store-carry-forward (DTN Spray-and-Wait) when gateway unreachable.
- Downlink (rare, duty-cycle limited): config/threshold update + time-sync + siren command (authenticated).
- **Offline rule (C1):** node may raise a LOCAL_SIREN edge_flag autonomously ONLY for its own co-located siren
  under a hard physical rule (tilt-rate + rain), never a network-wide public alert — that stays human-gated.
### 3.2 Gateway ⇄ Cloud (intermittent internet / sat-IoT)
- REST/gRPC over mTLS to an ALLOW-LISTED endpoint only (C6; CI fails otherwise). Idempotent, resumable,
  compressed batches. Payloads: Evidence summaries, Decisions, model-version pulls, dataset pointers.
- **No raw video egress (C7):** only events/scores/consented-clips. Enforced by a serializer that rejects
  video blobs on the cloud channel.
### 3.3 Gateway → Alerting (CAP/SACHET)
- CAP 1.2 XML (§2.5) signed; posted to SACHET integration endpoint (allow-listed) + local siren bus + LoRa
  mesh rebroadcast. Dedup by `cap_id`. Human approval token REQUIRED in the request (R19).
### 3.4 Internal module bus
- In-process (single gateway) via typed function calls; optional message queue (e.g. ZeroMQ/Redis-stream) for
  decoupling C-CCTV (fast loop) from C-FUS. All messages carry `trace_id` + `schema_version`.

---
## 4. Key sequence flows (text)
### 4.1 Geo early-warning (slow loop)
```
EO pass → C-ENC.embed → C-ANO.score ─┐
IoT heartbeat → decode/validate ─────┤→ build Evidence(zone,window)
precip/soil → bias-correct (LoRa gauge)┘
Evidence → C-GEO (FS,Iverson,Fukuzono,Caine) → p_phys,a0,c_i
         → C-ANO fused score p_sup
C-RL.act(state) → logits,a_rl   (behind OPE gate)
C-FUS(x, a_rl, p_phys, p_sup, masks) → a_hat (bounded residual over a0)  [FM-1 default]
C-CAL.calibrate(risk) → conformal set + reliability
C-DEC: level = max(conformal_level, C-SHD.shield_floor(state))
level ≥ YELLOW → C-OPS presents to operator (+contributions, +shield_reason)
operator approves → C-ALERT builds/sign/route CAP → siren/mesh/SACHET
```
### 4.2 Fire / CCTV (fast loop, gateway)
```
frame → C-CCTV.detect → TemporalValidator.update → Event?
Event → C-FIRE soft features (ND-1 flicker, ND-2 smoke-temp, EF checks)  [reject steam/headlights]
IoT fire sensors (multi-node agreement) → corroboration
→ C-FUS (fire experts) → C-CAL → C-DEC → (ORANGE/RED advisory) → operator → C-ALERT
Node-local: smoke+heat+gas co-trigger → LOCAL_SIREN only (offline), still logged for human review
```
### 4.3 Offline alert (cloud down)
```
node edge_flag=LOCAL_SIREN → co-located siren fires immediately
+ LoRa → gateway → C-SHD floor → gateway siren + mesh rebroadcast + queued CAP (DTN)
cloud reconnect → queued Decisions/CAP sync; no life-safety wait on cloud (C1)
```

---
## 5. Per-component algorithm notes (pseudocode-level; detail in LLD)
### C-GEO (Class A/B/C)
```
FS = (c' + (σn−u)·tanφ') / (γ·z·sinβ·cosβ)                 # A; test: Se→1 ⇒ σs→0 ⇒ saturated form
ψ(Z,t) via Iverson with D1=D0/cos²β ONLY                    # A; NO extra cosβ (bug-guard test)
t_f from 1/v linear fit, α=2 (flag α≠2 regime)             # A/B
caine_exceed = I > a·D^(-b)   (a,b locally fitted)         # A; coeff from local corpus not borrowed
rainfall ENSEMBLE → distribution of FS (not a point)       # #25 uncertainty propagation
emit ExpertOutput(p=f(FS,ψ,t_f,caine), c=consistency, cls per block)
```
### C-FIRE (Class A + C-soft, flag-gated, fallback=omit)
```
if flags.firephys.nd1: flicker = nd1_dealiased(spectrum,fs,D)   # C
T_hat,σ = nd2_transmittance_temp(L,τs) if nd2 else (raw_T, large_σ)  # C; σ↑ as τs→0 ⇒ fail to "uncertain"
Π_ig = nd3_ignition_index(...) if nd3 else None                # C
reject if plume regime (Byram N_c) inconsistent with "real fire"  # A gate
```
### C-FUS (GMF + PHARAOH + FM; default FM-1)
```
for each expert i: w̃_i = avail_i · r_i(t) · c_i · exp(−u_i/τ)   # NF-1/NF-2
if flags.operator.pharaoh: p_fused = pharaoh(p, normalize(w̃), rho(t))   # C, else:
else:                      p_fused = Σ (w̃_i/Σw̃)·p_i               # FM-1 linear (A/B default)
residual = bounded_head(features);  a_hat = clip(a0 + residual)   # residual policy learning
U* = Σ ŵ_i u_i + λ·D   # NF-3 conflict→uncertainty (fail-open)
assert final never below C-SHD floor
```
### C-RL (baseline-first)
```
if not ope_feasibility(logs): use rule baseline (fixed-threshold)   # FM-22 gate
policy = one_step_or_td3bc(logs);  select by BVFT;  risk by SCOPE-RL CVaR@5%
deploy iff OPE_lower_bound ≥ rule_baseline AND seeds≥100
```
### C-SHD (deterministic, monotone)
```
floor = GREEN
if FS<1: floor = max(floor, ORANGE)
if tilt_rate>5°/day (corroborated ≥2 nodes): floor = RED
if rain_24h>150mm on high-susceptibility: floor = max(floor, ORANGE)
if GLOF lake-level drop + downstream stage jump: floor = RED (downstream zones)
if fire: multi-node (smoke+heat) agreement: floor = max(floor, ORANGE)
return floor   # single faulty node alone CANNOT reach RED (consistency required)
```
### C-CAL
```
sets, reliability = WCPS(scores, calib_set, alpha, shift_weights)   # reweight for covariate shift
if drift_monitor.flag: reliability = "Unreliable"                  # concept drift voids CP bound
report realized coverage (PICP) honestly; never call it a "guarantee"
```

---
## 6. Cross-cutting contracts
- **Versioning**: every artifact carries `schema_version` + `model_versions`; breaking changes bump major.
- **Tracing**: `trace_id` propagates sensor→decision→alert for audit (R19 explainability).
- **Time & anti-leak (G6)**: no component consumes a feature with `t > decision_time`; feature timestamps
  logged; CI test replays to prove no post-event leakage.
- **Security (C6)**: outbound endpoints from an allow-list config; secrets via OS keystore, never in repo;
  Ed25519 node keys provisioned at flashing; CAP signed; `(node_id,seq)` replay protection.
- **Degradation (C8/CR-07)**: missing-modality adapter + reliability gating; a dropped layer lowers trust &
  widens conformal set, never silently fabricates confidence.
- **Honesty metadata**: Decision carries `class_flags.used_classC`; any Class-C contribution is labelled in
  `contributions[].cls` and surfaced in C-OPS.

---
## 7. What this document deliberately does NOT fix (open, resolve in build)
`[coeff-verify]` physics constants; CR-01 SAR encoder choice; exact RL/fusion hyperparameters; India
dataset-portal licenses; PHARAOH P1–P7 numeric verification; LoRa IN865–867 regulatory confirmation; final
LoRa frame bit-layout + DR plan; message-queue vs in-process choice at the gateway. Each is owned by its
module's gate (G1–G7) in `DESIGN/REPO_BLUEPRINT.md`.
