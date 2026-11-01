# 02 — System Architecture

**Audience:** engineers and reviewers who need the end-to-end design, data flow, compute tiers, and the
interfaces between components. Ground truth: `DESIGN/HLD.md`, `DESIGN/LLD.md`, `DESIGN/COMPONENT_DESIGN.md`,
and the implemented packages in `trinetra/src/trinetra/`. Nothing here claims measured performance.

---

## 2.1 System context

```
          ┌──────────────────────────── EXTERNAL ACTORS ────────────────────────────┐
 ESA/NASA free EO ─►│                                                                │
 existing CCTV ────►│                     TRINETRA SYSTEM                            │─► Human operator
 ground IoT nodes ─►│   sense → detect → physics-gate → fuse → calibrate → shield    │   (DECIDES)
 inbound media ────►│                                                                │─► CAP/SACHET feed
          └──────────────────────────────────────────────────────────────────────────┘        │
                                                                                                ▼
                                                                                 sirens / SMS / WhatsApp
```

The trust boundary is explicit: the system produces an **advisory level**; it **never** originates a public
alert on its own. Deepfake and zero-shot outputs are low-trust advisory signals only. (Safety rule R19.)

## 2.2 Logical pipeline (the spine)

Three sensing layers → encoders → anomaly stack → physics gate → supervised ensemble → offline-RL policy →
meta-fusion head → conformal calibration → hard safety shield → advisory level → operator → CAP/SACHET.

```
 L1 SENSE            L2 PROCESS                                           L3 DECIDE          L4 ACT
 ─────────           ─────────────────────────────────────────────       ──────────────     ──────────────
 EO/satellite ─┐     encoders (frozen EO-FM, CCTV detector, IoT feat.)    conformal          operator UI
 CCTV/vision ──┼───► anomaly (resid + Deep-SVDD + iForest + XGBoost) ─┐   calibrate (per      (human gate)
 ground IoT ───┘     physics gate (geo: FS/Iverson/Fukuzono/Caine;    │   zone, WCPS/ACI) ─►  │
 inbound media ───►  fire: Heskestad/Byram/Strouhal; fire-PINN=soft)  ├─► META-FUSION ──►     shield (monotone
                     supervised ensemble (XGBoost EWS + per-hazard)   │   (GMF+PHARAOH+FM)    floor, can only
                     offline-RL advisory policy (shielded) ───────────┘                       RAISE) ─► LEVEL
 authenticity (deepfake scorer) ───────────────────────────────── low-trust advisory ──────► into fusion/UI
 monitor (drift/calibration CUSUM) ────────────────────────────── advisory recalibration flag
```

### 2.2.1 Processing stages and their trust class

| Stage | Component | WS (internal) | Code package | Class / trust |
|-------|-----------|---------------|--------------|---------------|
| Encode | frozen SAR-capable EO-FM, CCTV detector, IoT featurizer | WS1b/WS4/WS7 | `ws1b_eo`, `ws4_cctv`, `ws7_iot` | data-driven |
| Anomaly | forecast-residual + Deep-SVDD + iForest + XGBoost | WS8 | `ws8_anomaly`, `deep/anomaly_deep.py` | data-driven |
| Physics gate (geo) | FS, Iverson transient, Fukuzono 1/v, Caine I–D | WS1b | `ws1b_geophys` | A/B |
| Physics gate (fire) | Heskestad/Byram/Strouhal/radiation + ND soft terms | WS1a | `ws1a_firephys` | A + C(soft, OFF) |
| Supervised | XGBoost high-recall EWS + per-hazard heads | WS8 | (planned) + `eval/baselines` | data-driven |
| RL policy | offline RL (baseline-first) + post-posed shield | WS5 | `ws5_fusion_rl/rl.py`, `deep/offline_rl.py` | advisory |
| Meta-fusion | GMF + PHARAOH + FM-1..6 + hierarchical + BLUE | WS5 | `ws5_fusion_rl` | advisory |
| Calibrate | per-zone Mondrian CP + WCPS shift layer + ACI | WS6 | `ws6_robust/conformal.py` | honest coverage |
| Shield | monotone hard safety floor | WS3/WS5 | `ws5_fusion_rl/shield.py` | deterministic |
| Alert | CAP/SACHET builder+signer, DTN, siren | WS3 | `ws3_alert` | human-gated |
| Authenticity | deepfake/misinfo scorer | WS2 | `ws2_deepfake`, `deep/deepfake_net.py` | low-trust advisory |
| Monitor | drift/calibration monitor | WS6 | `ws6_robust/drift_monitor.py` | advisory |

## 2.3 The single decision function (the architectural contract)

```
level(state s) = max( conformal_level( fused_risk(s), p* ) ,  shield_floor(s) )
```

- `conformal_level` maps the calibrated fused risk to {Green < Yellow < Orange < Red}; the escalation point
  is the cost-loss alarm threshold **p\* = C_FA/(C_FA+C_miss) ≈ 0.0476** (C_FA=5, C_miss=100), optionally
  replaced by Conformal-Risk-Control-calibrated cut points.
- `shield_floor(s)` is a **deterministic, monotone** floor (e.g. FS<1 forces a minimum level). It can only
  **RAISE** the level, never lower it, and runs **after** the learner (post-posed shielding, no training).
- There is **exactly one** decision function. Every legacy threshold maps to an internal role; no alert path
  bypasses it. Implemented in `ws5_fusion_rl/decision.py` (`decide`, `conformal_level`).

## 2.4 Meta-fusion head (GMF + PHARAOH), high level

Experts: `e_phys` (physics/Bayes → p_phys + base action a₀), `e_RL` (offline-RL q-values), `e_sup`
(supervised/anomaly ensemble → p_sup). The head embeds raw evidence ⊕ RL output ⊕ expert probabilities ⊕
reliability/quality masks and emits a **bounded residual** over the base action a₀: `â = clip(a₀ + residual)`
(residual-policy learning; the residual is hard-clipped so a mis-trained head cannot dominate the
physics-anchored base). **PHARAOH** is an adaptive-order weighted power-mean pooling primitive (Class C,
flag-gated OFF) whose order bends toward "max" only under a credible, physics-consistent alarm
(anti-complacency) and fails open to "uncertain". **FM-1..FM-6** are derived fusion options
(precision-weighted — the Class-A default; evidential; conformal-stacked; covariance-intersection;
physics-gated MoE; RL-tuned). All Class-B/C fusion pieces are advisory, unvalidated, flag-gated, with the
Class-A linear fallback (FM-1). Correlation-aware **BLUE/GLS** weighting and a **two-layer hierarchical**
fusion decorrelate redundant sources. Details and the honesty critique: chapter 06.

## 2.5 Deployment topology — three compute tiers (hard design rule C8)

```
┌── TIER 0: NODE (ESP32-C3 / ESP32-CAM, ≤₹2000, solar + LiFePO4) ───────────────────────────────┐
│  tiny statistical screen ONLY: Z-score/RMS tilt, stage threshold, on-node FS, 1/v fit,         │
│  drift pre-correction (F-15), TinyML pre-filter. Deep sleep + duty cycle. RAW VIDEO STAYS LOCAL.│
└───────────────┬─────────────────────────────────────────────────────────────────────────────────┘
                │ LoRa IN865–867 MHz (SX1262), store-carry-forward (DTN) when the link is down
┌───────────────▼── TIER 1: GATEWAY (LoRa concentrator + edge GPU/SoC + sat-IoT uplink) ─────────┐
│  CCTV detector (F-11) + temporal event validation (F-12) + IR flicker (F-16); VAD; InSAR        │
│  anomaly if cached; physics gate; LOCAL fusion + shield; CAP build + siren drive. CLOUD-OFFLINE. │
└───────────────┬─────────────────────────────────────────────────────────────────────────────────┘
                │ intermittent internet / sat-IoT
┌───────────────▼── TIER 2: CLOUD / KAGGLE (≤30 GPU-h/week) ─────────────────────────────────────┐
│  frozen EO-FM embedding, SSL/anomaly training, offline-RL training, meta-head training,         │
│  hindcast/eval harness, model registry. NEVER on the life-safety critical path (constraint C1). │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Model→tier assignment is a hard rule: heavy models (EO-FM, VAD, deep anomaly) are **Tier-1/2 only**; Tier-0
runs only what fits MCU SRAM/flash/energy. The **offline alert path (node → LoRa/DTN → gateway → siren) is
independent of the cloud** (C1).

## 2.6 Key data flows

1. **Geo early-warning (slow):** EO datacube + IoT + precip → encoder/anomaly → physics gate → ensemble →
   RL → meta-fusion → conformal → shield → advisory level → operator. Cadence: per satellite pass + IoT
   heartbeat.
2. **Fire / CCTV (fast):** frame → detector (F-11) → temporal event validation (F-12) (+ IR flicker F-16,
   fire-physics soft features) → fusion → shield → advisory level. Cadence: near-real-time at the gateway.
3. **Offline alert (always available):** node event → LoRa/DTN → gateway shield decision → local siren/SMS,
   independent of the cloud.
4. **Calibration/bias loop:** LoRa rain gauges bias-correct satellite IMERG precip; F-15 corrects IoT
   sensor drift; F-14 raises advisory recalibration flags.
5. **Authenticity (advisory):** inbound media → deepfake scorer → low-trust flag into fusion / operator UI.

## 2.7 Interfaces and message contracts

The implemented contracts live in `trinetra/src/trinetra/common/types.py`. Core objects:

- **`ExpertOutput`** — one fused expert's contribution: `p` (probability), `u` (uncertainty), `c`
  (conflict), `r` (reliability), `cls` (`PhysicsClass` A/B/C/DATA/ADVISORY), `available` (bool). Every
  encoder/anomaly/physics/RL stage produces one of these; the fusion head consumes a list of them.
- **`Evidence`** — raw per-source signals + quality/availability masks entering the pipeline.
- **`ConformalResult`** — calibrated risk + coverage metadata (marginal, per-zone), honestly labelled.
- **`ShieldResult`** — the deterministic floor level + the human-readable reason it fired.
- **`Decision`** — the final advisory `Level` (Green/Yellow/Orange/Red) + contributing evidence + shield
  reason + trace id (R19 explainability: every advisory traces to its evidence and the shield reason).
- **Alerting:** the CAP/SACHET builder (`ws3_alert/cap.py`) refuses to emit without an `APPROVED:` operator
  token; DTN (`ws3_alert/dtn.py`) does store-carry-forward; endpoints are allow-listed (constraint C6);
  no raw video leaves the node (C7).

Message formats between tiers: LoRa payloads are compact codewords (`ws7_iot/lora_codec.py`, IN865–867
band); the gateway reconstructs `Evidence`; alerts are CAP XML, signed, deduplicated.

## 2.8 Cross-cutting concerns

- **Calibration & uncertainty (WS6):** every probabilistic output is conformally calibrated per zone;
  coverage is reported honestly (marginal, shift-sensitive), never as a "guarantee"; evidential/zero-shot
  signals are for ranking/OOD only, never as absolute probabilities.
- **Robustness (WS6):** per-corruption eval; adversarial-patch red-team on the detector; missing-modality
  adapter + reliability gating so a dropped layer degrades gracefully (constraint C8 / graceful degradation).
- **Security (WS6):** endpoint allow-list enforced in CI (C6); signed CAP alerts; dedup; key rotation; the
  historical key-exfiltrating proxy bug is removed (chapter 13).
- **Privacy (C7):** raw video stays local; federated/edge scoring; only events/scores leave the node.
- **Provenance & reproducibility (F-17):** pinned seeds, logged spatial-CV folds, experiment tracking, and
  the LMEM+GLRT "real-win" gate on every improvement.
- **Energy:** camera + comms dominate; a per-task energy budget is a requirement; winter/monsoon solar gaps
  mean node outage and missing inputs are treated as **expected**, not exceptional.

## 2.9 Non-functional requirements (summary; full list chapter 03)
Offline-first alert path (C1); graceful degradation; edge latency within the alert deadline at the gateway;
≤₹2000/node (C2); ≤30 GPU-h/week (C3); auditability of every advisory (R19); **no performance surface in
UI/API until the admission gate G2 passes**; Class-C blocks flagged in output metadata.

## 2.10 Quality gates (architecture-level; see chapter 12 for G2 detail)
G1 physics golden tests · **G2 spatial-CV admission gate (blocks ANY performance claim)** · G3 single
decision fn + realizable monotone shield + measured coverage · G4 fusion stability + reliability gating ·
G5 ≤₹2000 BOM + tiered feasibility + fault discrimination + LoRa band · G6 no credential egress + offline
alert path + anti-leak timestamp audit · G7 datacube size + dataset licenses + novelty honesty + Kaggle fit.
