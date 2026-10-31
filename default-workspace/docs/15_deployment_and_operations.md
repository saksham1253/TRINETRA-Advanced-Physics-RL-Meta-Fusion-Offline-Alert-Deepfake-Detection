# 15 — Deployment and Operations

> Scope: how TRINETRA (HIMKAVACH) is *intended* to be fielded and run — the three compute tiers, the IoT
> node, gateway operations, monitoring, graceful degradation, staged rollout, incident runbooks, and
> maintenance. Primary sources: `DESIGN/HLD.md §4–§7`, `DESIGN/COMPONENT_DESIGN.md`,
> `trinetra/firmware/FIRMWARE_SPEC.md`, `ws7_iot/FIRMWARE_SPEC.md`, `HARDWARE_BUDGET.md`, `DEPLOYMENT/*`,
> and the implemented packages `trinetra/src/trinetra/ws7_iot/`, `ws3_alert/`, `ws6_robust/drift_monitor.py`.
>
> **Read this first (honesty contract, from `_CANON.md`).** Nothing in TRINETRA has been deployed, flashed,
> powered, or measured. There is **no fielded node, no gateway in operation, and no pilot**. Every BOM price
> below is `[EST]` because Indian supplier pages returned **HTTP 403** this session (`HARDWARE_BUDGET.md`),
> so the **≤₹2000/node gate (C2) is NOT yet enforceable**. The **LoRa band IN865–867 MHz is an assumption
> to verify** with the telecom regulator, not a confirmed allocation. The system **never issues an
> autonomous public alert** (Rule R19). Firmware is a *specification*: it is not built here (no embedded
> toolchain); only the host-side Python mirror runs. Treat every operational procedure in this chapter as a
> **planning procedure**, not an exercised one. Reference IDs point to chapter 19.

---

## 15.1 Deployment topology — the three compute tiers

The whole system is organized around one hard rule: **the life-safety alert path must survive with no
cloud and no internet (constraint C1).** Everything else is arranged so that losing a tier degrades
capability but never silences the warning path. The second hard rule is **C8: heavy models live only at
Tier-1/Tier-2**; a Tier-0 node runs only what fits an MCU's SRAM/flash/energy budget. Both rules come from
`DESIGN/HLD.md §4` and are repeated in `DESIGN/COMPONENT_DESIGN.md §1`.

```
            FIELD TOPOLOGY  (advisory, human-gated, offline-first)   [all tiers: NOTHING DEPLOYED]

   TIER-0  NODES (ESP32, <=Rs.2000 [EST], solar)              TIER-1  GATEWAY            TIER-2  CLOUD / KAGGLE
   ------------------------------------------                 ------------------         ---------------------
   [SS] Slope Sentinel  (ESP32-C3 + SX1262)                   LoRa concentrator          frozen EO-FM embedding
     tilt/IMU x2, soil x2, piezo, rain, temp                  + edge compute (SoC/GPU)   SSL / anomaly training
     on-node: Z/RMS tilt, FS, 1/v fit, F-15                   + sat-IoT uplink           offline-RL training
     deep-sleep + duty cycle                                                             meta-head training
         |                                                        detector F-11          hindcast / eval harness
         |  LoRa IN865-867 [verify]                               temporal valid. F-12   model registry
         |  25 B frame (<=51 B)                                   IR flicker F-16; VAD        |
         |  store-carry-forward (DTN) when link down               InSAR anomaly (cached)     |  intermittent
         +------------------------------------------------->   physics gate (geo+fire)        |  internet /
   [RE] River Eye  (ESP32-CAM + SX1262)                        local FUSION + SHIELD           |  sat-IoT
     stage/level (ultrasonic|pressure), low-fps cam            CAP build + SIREN drive         |
     LSPIV runs at GATEWAY (no video egress, C7)                     |            ^              |
         |                                                          |            |              |
         +------------------------------------------------->  co-located SIREN   |         <----+  (one-way,
                                                              + LoRa-mesh rebcast |              resumable,
                      ====  OFFLINE ALERT PATH (C1) ====            |             |              mTLS, allow-list,
   node edge_flag=LOCAL_SIREN --LoRa/DTN--> gateway shield --> local siren +     human           NO raw video C7)
   mesh + queued CAP (DTN).  NO life-safety step waits on cloud. operator decides public alert (R19)

   HARD RULES:  C1 offline alert path is independent of Tier-2.   C8 heavy models (EO-FM, VAD, deep
   anomaly, RL/meta-head training) are Tier-1/2 ONLY — never on Tier-0 and never on the C1 critical path.
```

What runs where (from `DESIGN/HLD.md §4`, `COMPONENT_DESIGN.md §1`):

- **Tier-0 — Node (ESP32-C3 / ESP32-CAM, ≤₹2000 [EST], solar).** A *tiny statistical screen only*: Z-score /
  RMS on tilt, a stage threshold, on-node Factor-of-Safety (FS), a 1/v (Fukuzono inverse-velocity) fit,
  F-15 drift **pre-correction**, and a TinyML pre-filter. Deep sleep + duty cycle. **Raw video stays local**
  (privacy constraint C7). It may fire **its own co-located siren** under a hard physical rule, nothing more.
- **Tier-1 — Gateway (LoRa concentrator + edge compute + sat-IoT uplink).** The CCTV detector (F-11),
  temporal event validation (F-12), IR flicker check (F-16), video-anomaly detection (VAD), cached InSAR
  anomaly, the physics gate, **local fusion + the hard safety shield**, CAP construction, and the siren
  drive. **This tier works with the cloud OFFLINE** — it is the autonomy boundary for life-safety.
- **Tier-2 — Cloud / Kaggle (≤30 GPU-h/week, C3).** Frozen EO-FM embedding, SSL / anomaly training,
  offline-RL training, meta-head training, the hindcast / evaluation harness, and the **model registry**.
  `HLD.md §4` states this tier is **NEVER on the life-safety critical path (C1)**.

The division is not cosmetic: it is what makes the honesty posture physically true. A model that could only
run in the cloud could never be trusted in a disaster where the cloud is exactly what disappears
(`DEPLOYMENT/india_context.md`: intermittent/absent connectivity during disasters is treated as a *binding*
constraint, DTN-over-phones/vehicles cited src-reported AZIZA 2511.15710). So the expensive learning stays
upstream and only its *frozen, versioned artifacts* flow down to Tier-1, while the decision that drives a
siren is made by deterministic physics + a monotone shield at the gateway or on the node.

---

## 15.2 The IoT node

### 15.2.1 BOM skeleton and the two node types

The bill of materials is a **skeleton with no verified prices**. `HARDWARE_BUDGET.md` records that every
line is `[EST]` because supplier pages returned HTTP 403 (Cloudflare) this session, and that a node's BOM
total is **`[INFEASIBLE]`-to-confirm until every line is `[LV]` (live-verified) from a dated listing**. The
two node variants and their *target* roll-ups come from `_CANON.md §8`:

| Node | Name | MCU | Role | Target BOM |
|------|------|-----|------|-----------|
| SS | **Slope Sentinel** | ESP32-C3 (RISC-V) | landslide / debris | **≈₹1,930 [EST]** |
| RE | **River Eye** | ESP32-CAM | flood / GLOF | **≈₹1,980 [EST]** |

Component skeleton (from `HARDWARE_BUDGET.md`; all unit prices **TBD / [EST]**, "Source (to verify)" empty):

| Component | Qty | Price | On SS | On RE |
|-----------|-----|-------|-------|-------|
| MCU (ESP32-class) | 1 | TBD [EST] | ✓ (ESP32-C3) | ✓ (ESP32-CAM) |
| LoRa module (IN865–867 MHz, SX1262) | 1 | TBD [EST] | ✓ | ✓ |
| Tilt / IMU sensor | 1 | TBD [EST] | ✓ (×2 MEMS tilt) | — |
| Soil-moisture sensor | 1 | TBD [EST] | ✓ (capacitive ×2) | — |
| Rain gauge (tipping bucket) | 1 | TBD [EST] | ✓ | — |
| Piezometer (water level) | 1 | TBD [EST] | ✓ (piezo/geophone) | — |
| Stage / level sensor (ultrasonic\|pressure) | 1 | TBD [EST] | — | ✓ |
| Camera module | 1 | TBD [EST] | — | ✓ (low-fps, LSPIV) |
| Solar panel + battery + charge controller | 1 | TBD [EST] | ✓ | ✓ |
| Enclosure (IP-rated) + misc | 1 | TBD [EST] | ✓ | ✓ |

Both ≈₹1,930 and ≈₹1,980 are **planning numbers only**; because the two headline totals sit within ~₹70 and
~₹20 of the ₹2000 cap, **nothing confirms the cap holds** until P6/G5 re-pricing against ≥2 dated listings
per line (`HARDWARE_BUDGET.md` rule, `DEPLOYMENT/cost_scaling.md §1`). Real deployment adds unpriced items
(certified radio, mounting, SIM/connectivity, installation labour, spares) that `cost_scaling.md §1` lists
as `[UNVERIFIED]` and *outside* this prototype cap.

### 15.2.2 Firmware behavior (specification; not built)

From `trinetra/firmware/FIRMWARE_SPEC.md` (SS/RE) and `ws7_iot/FIRMWARE_SPEC.md` (the fire-sensor node) —
both are **specifications**; firmware is not compiled or flashed in this environment:

- **Deep sleep + duty cycle.** Heartbeat every N minutes with an event-driven burst on a WATCH / LOCAL_SIREN
  edge flag. The fire-node spec splits a **fast loop** (flame/heat, sub-second, always on) from a **slow
  loop** (gas/humidity, duty-cycled). Exact rates are **to be pinned at build from measured current and
  sensor time constants** — `[quota]` in the spec; **not measured here**.
- **On-node statistics / physics screen.** Z-score / RMS on tilt, a stage threshold, on-node FS, and a 1/v
  (Fukuzono) fit — the Tier-0 subset of the geo physics gate (`HLD.md §4`). For the fire node: fixed
  over-temperature threshold AND rate-of-rise dT/dt, smoke/gas rising-rate, flame-flicker confirmation.
- **F-15 drift pre-correction** on-node before data enters the uplink: a GP drift model + uncertainty-driven
  calibration schedule (F-15, src-reported 2506.09186). The spec's load-bearing caveat (`FEATURES.md` F-15,
  `features/wave1_specs.md §F-15`): **decompose environmental vs instrumental drift before recalibrating** —
  recalibrating against environment-driven apparent drift wastes budget and injects error (2406.17488).
- **LoRa codewords.** `ws7_iot/lora_codec.py` packs a **25-byte** big-endian frame (`FRAME_LEN = 25`,
  well under the **≤51 B** budget) carrying node tail-id, seq, tilt×2 (0.01°), tilt-rate (0.001 dps), soil×2,
  piezo (0.1 kPa), rain_15m (0.1 mm), temp (0.01 °C), batt_mV, and an edge flag (`NONE|WATCH|LOCAL_SIREN`).
  Band **IN865–867 MHz on SX1262** (SS firmware spec; marked `[verify]` for regulatory confirmation). The
  signature does **not** ride in the on-air frame — integrity is an app-layer tag (`sensor_reading.py`:
  HMAC-SHA256 as an **honest placeholder** for the real-node Ed25519, which is not available in-sandbox).
- **Tier-0 edge rule (offline autonomy, bounded).** `ws7_iot/edge_screen.py`: `LOCAL_SIREN` requires **BOTH**
  a fast tilt-rate **AND** heavy recent rain (two independent physical cues) so a single noisy sensor cannot
  fire the siren; a single elevated cue yields only `WATCH`. The thresholds in code (siren tilt-rate 5.0,
  watch 2.0, rain_15m 20 mm) are **illustrative and must be field-tuned** — the code itself flags a
  deg/s-vs-deg/day unit ambiguity to resolve at build. **The node never issues a public/network alert on its
  own (R19)**; that stays human-gated at the gateway.
- **Replay / integrity.** `(node_id, seq)` is monotonic (`sensor_reading.py ReplayGuard` rejects
  non-increasing seq); downlink (config/threshold/time-sync/siren command) is authenticated and
  duty-cycle-limited.
- **River Eye specifics.** ESP32-CAM, stage/level by ultrasonic or pressure, optional low-fps camera —
  **LSPIV surface-velocity runs on the gateway, not the node** (no video egress, C7).

### 15.2.3 Power / solar budget (planning estimates only)

`HLD.md §6` states the energy reality bluntly: **camera + comms dominate**, per-task energy is a hard
requirement, and **winter/monsoon solar gaps mean node outage and missing inputs are EXPECTED, not
exceptional** — so power is oversized by design. No current, energy, or autonomy numbers have been measured;
the SS spec target is "multi-week autonomy" as a **goal, not a result**. Battery chemistry is **not settled
in the canon**: `HLD.md §4` writes "solar+LiFePO4" while `trinetra/firmware/FIRMWARE_SPEC.md` writes
"Li-ion 18650 + small PV" (see §15.9, contradiction C-1). Any Wh-generated-vs-consumed curve is a build-time
deliverable, not an existing measurement.

### 15.2.4 The ≤₹2000 live-verification gate (G5)

Gate **G5** (`HLD.md §8`, SS firmware "Acceptance (G5)") blocks the hardware order until **all** of:

1. **BOM ≤ ₹2,000 supplier-verified** (every line `[LV]` from ≥2 dated Indian listings — the HTTP-403 blocker
   above means this is **not yet satisfiable**).
2. On-air **frame ≤ 51 B** (codec currently 25 B — satisfied in the host mirror, not on real hardware).
3. **Fault-vs-event discrimination** (a faulty sensor degrades, never silently alarms or goes blind).
4. **A single node cannot drive a network RED** (corroboration required — enforced in
   `ws5_fusion_rl.shield`, see §15.5).
5. **LoRa band confirmed** (IN865–867 regulatory sign-off — currently an assumption).

Until G5 passes, the node is a **design**, and the ≤₹2000 constraint is **asserted, not demonstrated**.

---

## 15.3 Gateway operations (Tier-1)

The gateway is where the offline-first promise is kept. From `HLD.md §4`, `COMPONENT_DESIGN.md §4.1–4.3`:

- **Ingest & decode.** Decode LoRa frames (§15.2.2), validate (`validate_reading`), reject replays
  (`ReplayGuard`), verify the app-layer signature. Rain-gauge readings **bias-correct satellite IMERG
  precip** (calibration/bias loop, `HLD.md §5.4`).
- **Detect & validate.** CCTV detector (F-11) → temporal validator (F-12, rejects transient flicker) → IR
  flicker (F-16); VAD; cached InSAR anomaly if a recent satellite pass is held locally.
- **Physics gate.** Geo (FS, Iverson transient with the `D1 = D0/cos²β` bug-guard, Fukuzono 1/v, Caine I–D)
  and fire (Heskestad/Byram + Class-C soft features, default-OFF with A/B fallback) — `COMPONENT_DESIGN.md §5`.
- **Local fusion + shield.** Meta-fusion (FM-1 linear default; GMF/PHARAOH flag-gated) produces a bounded
  residual over the physics base action, conformal calibration attaches an honest coverage/reliability tag,
  then the **single decision function** applies: `level = max(conformal_level, shield_floor)`. The shield
  can only **raise** the level and is deterministic (no training).
- **CAP build + siren drive.** On a human approval token, `ws3_alert.cap.build_cap` emits signed CAP 1.2 XML
  (Severity/Urgency/Certainty a *deterministic* function of Level — never model-inferred from text);
  `ws3_alert.siren.SirenBus` records/dispatches the co-located siren; `ws3_alert.dtn.DTNQueue`
  (binary Spray-and-Wait, initial copy budget L=8) store-carries-forwards when the uplink is down.

**What degrades if the uplink (Tier-2) is down.** The gateway keeps the entire life-safety path alive:
decode → physics gate → fusion → shield → **local siren + LoRa-mesh rebroadcast + queued CAP (DTN)** all run
with no cloud (`COMPONENT_DESIGN.md §4.3`). What is *lost* while offline: fresh EO-FM embeddings, newly
trained models, cross-site hindcast context, and SACHET delivery — these resume (idempotent, resumable
sync) on reconnect. **No life-safety step waits on the cloud (C1).** This is the autonomy boundary:
everything below the gateway is deterministic and local; everything above it is advisory enrichment.

> **Security note (unprompted, per policy).** The Gateway↔Cloud channel is mTLS to an **allow-listed**
> endpoint only (C6, CI-enforced), **no raw video egress** (C7, serializer rejects video blobs), and the
> public CAP path is **unauthenticated-by-nobody** — it is physically impossible to build a CAP without a
> human approval token (`build_cap` raises `SafetyViolation` otherwise). A gateway deployed on a public IP
> must still have authenticated operator endpoints; `FINAL_REPORT.md §4` treats public-IP exposure as a
> **security** concern, not an addressing mechanism.

---

## 15.4 Monitoring

Monitoring is implemented in `trinetra/src/trinetra/ws6_robust/drift_monitor.py` (pure numpy):

- **PSI (Population Stability Index).** `population_stability_index(reference, current, bins=10)`; rule of
  thumb in the code: **>0.1 moderate, >0.2 significant** shift (`check_drift` default threshold 0.2).
- **CUSUM.** `cusum_update(state, x, target, k=0.5, h=5.0)` — a sequential change detector with slack `k`
  and decision threshold `h`; flags when `g_pos > h` or `g_neg < -h`.
- **The consequence.** When drift fires, **the conformal coverage bound is void**: callers set
  `reliability = "Unreliable"` and the decision layer **fails toward "uncertain"** (R19). This is wired in
  `COMPONENT_DESIGN.md §5 C-CAL`: `if drift_monitor.flag: reliability = "Unreliable"`.

Metrics watched in operation (from `DEPLOYMENT/pilot_design.md §2`, `HLD.md §6`):

| Metric | Why it matters | Source signal |
|--------|----------------|---------------|
| **Coverage (PICP vs nominal)** | conformal honesty under shift (2604.22787) | calibrator realized coverage |
| **Drift (PSI / CUSUM)** | voids the coverage bound → reliability flag | `drift_monitor.py` |
| **Node health** | faulty node must degrade, not alarm/blind | `SensorReading.health`, selftest flags |
| **False-alarm rate / day** | pilot go/no-go; operator trust | shadow-mode log vs ground truth |
| **Node fleet / uptime** | solar brownout, link loss are expected | heartbeat gaps, batt_mV, RSSI/SNR |

The **advisory recalibration flag (F-14)** is a *runtime monitor* on the live outputs that raises an
**advisory review/recalibration flag — it never auto-recalibrates and never triggers an alert** (R19,
`features/wave1_specs.md §F-14`). Its job is to tell a human "the distribution has moved; your calibration
may be stale," not to act. "Monitor-the-monitor" discipline is cited (2607.25842): a collapsing monitor
signal is itself a rollback trigger (§15.6).

---

## 15.5 Graceful degradation

Core principle (`HLD.md §6`, `COMPONENT_DESIGN.md §6`): **a dropped layer lowers trust and widens the
conformal set — it never silently fabricates confidence.** Outage and missing inputs are the *expected*
operating mode, not an exception.

| Failure | Behavior | Mechanism / source |
|---------|----------|--------------------|
| **Modality missing** (sensor/feed dropped) | reliability-gated fusion: down-weight the missing expert, widen the conformal set, recalibrate per-availability; never fabricate confidence | `COMPONENT_DESIGN.md §6 (C8/CR-07)`, missing-modality adapter |
| **Node dead / stuck** | peers report it as "offline/unknown", **never "all clear"**; neighbors + fault-vs-event discrimination; **one node alone cannot drive RED** (cross-node corroboration required) | `ws7_iot/FIRMWARE_SPEC.md §3`, `COMPONENT_DESIGN.md §5 C-SHD`, SS acceptance (G5) |
| **Solar brownout / low battery** | duty-cycle down; brownout detector saves state + annunciates low-power + safe shutdown; recover to SELFTEST on power return; outage is EXPECTED | `ws7_iot/FIRMWARE_SPEC.md §7`, `HLD.md §6` |
| **Cloud / Tier-2 outage** | **Tier-1 autonomy**: gateway runs decode→physics→fusion→shield→siren+mesh+queued CAP (DTN); no life-safety wait on cloud (C1) | `COMPONENT_DESIGN.md §4.3`, `HLD.md §4` |
| **Sensor drift** | F-15 on-node pre-correction (after env-vs-instrument decomposition) → then F-14 raises an **advisory recalibration flag** for a human | `FEATURES.md F-15/F-14`, `drift_monitor.py`, `wave1_specs.md` |
| **Concept drift (PSI/CUSUM fires)** | conformal bound void → `reliability="Unreliable"` → decision fails to "uncertain" | `drift_monitor.py`, `COMPONENT_DESIGN.md §5 C-CAL` |
| **Conflicting experts** | conflict folds into uncertainty (fail-open), not into a confident number | `COMPONENT_DESIGN.md §5 C-FUS` (NF-3) |

The shield's monotone floor (`COMPONENT_DESIGN.md §5 C-SHD`) is the backstop: FS<1 → ≥ORANGE; corroborated
tilt-rate (≥2 nodes) → RED; 24 h rain >150 mm on high-susceptibility → ≥ORANGE; GLOF lake-drop + downstream
stage jump → RED downstream; multi-node fire (smoke+heat) → ≥ORANGE. The closing comment is the safety
invariant: **"single faulty node alone CANNOT reach RED (consistency required)."**

---

## 15.6 Staged rollout

Promotion is gated, reversible, and **shadow-first** (`DEPLOYMENT/pilot_design.md`, ATAL/decision-readiness
style 2609.13552, staged-rollout 2608.08528). Pre-register every go/no-go metric *before* the stage starts.

```
 STAGE 0  OFFLINE REPLAY   -->  STAGE 1  SHADOW      -->  STAGE 2  ADVISORY     -->  STAGE 3 (NOT in scope)
 held-out, leakage-              observe live feeds,       outputs shown to a         anything beyond advisory:
 controlled data (spatial-       log detections +          HUMAN who decides;         needs official approval
 block / leave-one-incident-     uncertainty; TRIGGER      still NO autonomous        + certification + Stage
 out CV, 2608.22293)             NOTHING; compare vs       public alert               0-2 evidence. DEFERRED.
                                 ground truth/operator
 GO: meets pre-registered        GO: FA/day, time-to-      GO: human-factors eval
 offline targets                 detection, uptime meet    (does advisory improve
                                 thresholds over a fixed   operator decisions? RCT
                                 window                     2401.13744)
```

Go/no-go metrics (`pilot_design.md §2`): false-alarms/day; time-to-detection (incl. the F-12
confirmation-window cost); uptime/availability; missed-event (false-negative) rate **with its uncertainty**
(2211.04340); calibration under shift (PICP vs nominal, 2604.22787); operator decision accuracy (Stage 2).

Rollback rules (`pilot_design.md §3`): **halt promotion** if realized coverage/calibration collapses under
shift or the drift monitor flags sustained drift; **roll back a stage** on any safety incident, a
false-negative-rate breach, or a monitor-signal collapse (monitor-the-monitor, 2607.25842). Selective
drift-triggered intervention is preferred over continuous retraining (2604.02351), and interventions stay
**advisory**. `FINAL_REPORT.md §12` and `pilot_design.md §6` state plainly: **the bar for any automated
public alert is NOT met by any research-phase output** — independent certification, official approval, and
sustained cross-site/cross-season Stage-1/2 evidence are prerequisites that do not exist yet.

---

## 15.7 Incident runbooks

These are **planning procedures**, not exercised playbooks — nothing has run in the field. Each is grounded
in a mechanism that exists in the code/design; steps that are proposed judgement are marked `[HYPOTHESIS]`.

**R-1 · False RED alert (siren fired / CAP drafted in error).**
1. Confirm whether the RED came from the **shield floor** (deterministic rule) or the learned path — read the
   `Decision.shield.reason` and `contributions[]` (operator briefing, `ws3_alert/operator.py`).
2. If shield-driven: identify which rule fired (FS<1, corroborated tilt-rate ≥2 nodes, rain, GLOF). Check the
   contributing nodes' `health` and recent drift report; a corroborated rule firing is **working as
   designed** — treat as a true-until-disproven event.
3. If a **single node** appears to have driven it: that is a **defect** (G5 invariant says it cannot) — open a
   bug against `ws5_fusion_rl.shield` corroboration logic.
4. Verify the CAP was **human-approved** (`approved_by` parameter) — an unapproved CAP is impossible by
   construction (`build_cap` raises `SafetyViolation`); if one exists, treat as a security/integrity incident.
5. Log false-alarm against the pilot FA/day metric; if the rate breaches the pre-registered threshold, invoke
   the Stage rollback rule (§15.6). `[HYPOTHESIS]` Issue an operator-approved cancellation/all-clear CAP only
   after physical verification.

**R-2 · Node fleet drift.**
1. Pull PSI/CUSUM from `drift_monitor.py` across the fleet; confirm it is fleet-wide, not one node.
2. **Decompose environmental vs instrumental drift BEFORE recalibrating** (the F-15 pitfall, 2406.17488) —
   do not recalibrate away a real environmental signal.
3. For instrumental drift: apply F-15 GP pre-correction; set affected zones' `reliability="Unreliable"` so
   decisions fail to "uncertain" until confirmed.
4. Raise the F-14 **advisory recalibration flag** for a human; schedule a recalibration visit per the
   uncertainty-driven schedule (do not continuously retrain).
5. If drift persists past the pre-registered window → rollback trigger (§15.6).

**R-3 · Gateway down.**
1. Nodes continue the Tier-0 edge screen; `LOCAL_SIREN` still fires co-located sirens (C1 — no cloud, no
   gateway needed for the node's own siren).
2. DTN store-carry-forward buffers readings/alerts (`DTNQueue`, binary spray-and-wait) for mesh relay /
   later delivery.
3. Fail over to a standby gateway if provisioned `[HYPOTHESIS]`; otherwise dispatch field repair.
4. On recovery: gateway re-ingests DTN backlog by `(node_id, seq)` dedup; queued CAP/Decisions sync to cloud
   idempotently. **No life-safety decision waited on the gateway's cloud link.**

**R-4 · Suspected spoofed alert.**
1. Verify the message signature and `(node_id, seq)` monotonicity (`verify_reading` / `ReplayGuard`); reject
   non-increasing seq, stale timestamps, seen nonces (`ws7_iot/FIRMWARE_SPEC.md §8`).
2. For CAP: public warning systems are spoofable (2604.24404) — **TRINETRA never originates official
   alerts**; confirm the `approved_by` token and the allow-listed, signed channel (C6).
3. Rotate the implicated per-node / per-deployment key (§15.8); re-provision at next service.
4. Treat as a security incident per `DEPLOYMENT/responsible_release.md §1`; preserve the signed log
   (`trace_id` chain) for audit.

**R-5 · Model regression after retrain.**
1. A new model is a **registry candidate only** — it does not deploy until it **passes the chapter-12
   admission gate G2** (spatial-CV, baselines, CI, cost-loss, real-win). `HLD.md §8`: G2 blocks **any**
   performance claim and promotion.
2. If a regression reaches Tier-1 despite the gate, **roll back to the previous registry version** (every
   artifact carries `schema_version` + `model_versions`, `COMPONENT_DESIGN.md §6`).
3. Fall back to the **FM-1 linear fusion** default and Class-A physics (Class-C terms are default-OFF with
   A/B fallback) while investigating.
4. Re-run the admission gate on the fix before re-promotion; log the decision in the decision log (ch. 24).

---

## 15.8 Maintenance

- **Scheduled recalibration.** Driven by F-15's **uncertainty-driven schedule** (src-reported 2506.09186:
  schedule cost −15.7%), not a fixed calendar; recalibrate **only against instrumental drift** after the
  env-vs-instrument decomposition (`DESIGN/LLD.md §` rules; 2406.17488). Recurring recalibration is the main
  OPEX driver for low-cost sensors (`cost_scaling.md §1`), so minimizing unnecessary visits is a cost lever.
- **Key rotation.** Per-node Ed25519 signing keys are provisioned at flashing and held in NVS / OS keystore,
  never in the repo (`COMPONENT_DESIGN.md §6`, `HLD.md §6`); rotate on suspected compromise (R-4) and on a
  scheduled basis. The in-sandbox build uses an **HMAC-SHA256 placeholder** (clearly labelled) because
  `cryptography` is unavailable here — real nodes use Ed25519.
- **Model-registry promotion.** Gated by the **chapter-12 admission gate (G2)**: no model moves from the
  Tier-2 registry into Tier-1 operation until it clears spatial-CV + baselines + cost-loss + real-win. Every
  promotion bumps `model_versions`; demotion/rollback is the reverse (§15.7 R-5). No performance surface is
  exposed in UI/API until G2 passes (`HLD.md §7`).
- **Datasheets / model cards.** Produce at build (`responsible_release.md §5`): model cards (1810.03993) with
  explicit out-of-scope and limitations sections, datasheets (1803.09010).

---

## 15.9 What could not be sourced; contradictions with `_CANON.md`

**Could not be sourced (and why):**
- **Exact BOM prices and part numbers.** `HARDWARE_BUDGET.md` carries only component *classes* with every
  unit price `TBD / [EST]` and "Source (to verify)" empty — HTTP 403 on supplier pages. The ≈₹1,930 (SS) and
  ≈₹1,980 (RE) totals are canon planning figures with **no price breakdown**. No specific ESP32-C3/ESP32-CAM
  SKU, SX1262 module, sensor, panel, battery, or enclosure part number exists in the sources.
- **Power / current / energy / autonomy numbers.** None measured; the spec explicitly defers loop rates and
  the Wh curve to build-time measurement. "Multi-week autonomy" is a target.
- **Latency numbers.** No measured event-to-advisory latency; `HLD.md §7` references a budget "set in LLD"
  but no measured value exists.
- **LoRa band / regulatory status.** IN865–867 is an **assumption marked `[verify]`**; final frame bit-layout
  and DR plan are open (`COMPONENT_DESIGN.md §7`).

**Contradictions / tensions with `_CANON.md`:**
- **C-1 (battery chemistry).** `DESIGN/HLD.md §4` says the node is "solar+**LiFePO4**"; `trinetra/firmware/
  FIRMWARE_SPEC.md` says "**Li-ion 18650** + small PV." `_CANON.md §8` is silent on chemistry, so neither is
  authoritative — **flagged for resolution at build**; this chapter reports both rather than picking one.
- **C-2 (edge-rule units).** `ws7_iot/edge_screen.py` reads `tilt_rate_dps` (deg/s) but its own comment and
  the shield rule (`COMPONENT_DESIGN.md §5`: "tilt_rate>5°/**day**") disagree on units; the code marks the
  thresholds "illustrative / must be field-tuned." Not a canon conflict, but a build-time unit ambiguity to
  pin. No value was invented here.
- No conflict found with `_CANON.md §8` on node names/targets, the ≤₹2000 non-enforceability, the LoRa-band
  assumption, C1/C8, or R19 — this chapter matches the canon on all of those.
