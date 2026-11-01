# TRINETRA / HIMKAVACH — HIGH-LEVEL DESIGN (HLD) v1.0
> Architecture contract for the codebase phase. Grounded in P0–P23 research artifacts. Companion:
> `DESIGN/SYSTEM_DESIGN_PROMPT.md` (what/why/rules) and `DESIGN/LLD.md` (module internals). Honesty/safety
> rules R16/R19/R20/R21 (see the prompt §3) bind every component. Nothing here claims measured performance.

---

## 1. System context
TRINETRA is an **offline-first, multi-sensor, physics-grounded, advisory early-warning + hazard-detection
system** for (a) rapid-onset mountain hazards — landslide, flash-flood, cloudburst, GLOF (Uttarakhand +
Himachal) — and (b) fire/disaster detection via CCTV + IoT + satellite. It ingests free satellite data,
opportunistic vision, and cheap ground IoT; produces a CALIBRATED, SHIELDED, ADVISORY alert level for a human
operator who decides on CAP/SACHET dissemination.

```
            ┌──────────────────────────── EXTERNAL ACTORS ────────────────────────────┐
   ESA/NASA free EO ─► │                                                                │
   existing CCTV ────► │                    TRINETRA SYSTEM                             │ ─► Human operator
   ground IoT nodes ─► │  (sense → detect → physics-gate → fuse → calibrate → shield)   │     (decides)
   inbound media ────► │                                                                │ ─► CAP/SACHET feed
            └──────────────────────────────────────────────────────────────────────────┘        │
                                                                                                  ▼
                                                                                   sirens / SMS / WhatsApp
```
Trust boundary: the system NEVER crosses from "advisory level" to "public alert" without a human. Deepfake/
zero-shot outputs are low-trust advisory only.

## 2. Logical architecture — layers & pipeline
Three sensing layers → encoders → anomaly stack → physics gate → supervised ensemble → offline-RL policy →
meta-fusion head → conformal calibration → hard safety shield → advisory level → operator → CAP/SACHET.

### 2.1 Sensing layers (L1)
- **EO/satellite**: Sentinel-1 InSAR (C-band deformation, SAR-first), Sentinel-2 optical, GPM IMERG precip,
  SMAP soil moisture, ERA5-Land, MODIS/VIIRS active-fire, ITS_LIVE glacier velocity.
- **Opportunistic vision**: existing CCTV + River-Eye nodes (LSPIV stage/flow); fire/smoke edge detection.
- **Ground IoT**: ≤₹2,000 LoRa nodes — tilt/accel, soil moisture (2 depths), piezometer, rain gauge,
  pressure/temp; optional geophone at gateway.

### 2.2 Processing stages (L2)
| Stage | Component | Workstream | Class/trust |
|-------|-----------|------------|-------------|
| Encode | EO-FM encoder (frozen, SAR-capable), CCTV detector, IoT featurizer | WS1b/WS4/WS7 | data-driven |
| Detect anomaly | forecast-residual + Deep SVDD + iForest + XGBoost | WS8 | data-driven |
| Physics gate (geo) | FS, Iverson transient, Fukuzono 1/v, Caine I–D | WS1b | A/B/C |
| Physics gate (fire) | EF-01..EF-20 + ND-1..ND-7 soft features | WS1a | A + C(soft) |
| Supervised ensemble | XGBoost high-recall EWS + per-hazard heads | WS8 | data-driven |
| RL alarm policy | offline RL (baseline-first) + post-posed shield | WS5 | advisory |
| Meta-fusion | GMF + PHARAOH operator + FM-1..FM-6 | WS5 | advisory |
| Calibrate | per-zone Mondrian conformal + WCPS shift layer | WS6 | honest coverage |
| Shield | monotone hard safety floor | WS3/WS5 | deterministic |
| Alert | CAP/SACHET builder+signer, DTN, siren path | WS3 | human-gated |
| Authenticity | deepfake/misinfo scorer | WS2 | low-trust advisory |
| Monitor | drift/calibration monitor | WS6 | advisory |

### 2.3 The single decision function (contract)
```
level(state s) = max( conformal_level( fused_risk(s), τ* ) ,  shield_floor(s) )
```
- `conformal_level` maps calibrated fused risk to {Green<Yellow<Orange<Red} at threshold τ*≈0.0476 (from the
  cost-loss model). `shield_floor(s)` is a deterministic monotone floor that can only RAISE the level.
- EXACTLY ONE decision function exists; every legacy threshold maps to an internal role; no alert path bypasses
  it. Shield is placed AFTER the learner (post-posed shielding) and is hard-coded (no training).

## 3. Meta-fusion head (GMF + PHARAOH) — high level
Experts: `e_phys` (physics/Bayes → p_phys, base action a₀), `e_RL` (offline-RL logits/q-values), `e_sup`
(supervised/anomaly ensemble → p_sup). The meta-head embeds raw evidence ⊕ RL output ⊕ expert probabilities
⊕ reliability/quality masks, emits a BOUNDED RESIDUAL over a₀ (residual policy learning), i.e.
`â = clip(a₀ + residual)`. The P22 **PHARAOH operator** (adaptive-order weighted power mean) is the aggregation
primitive used where a monotone, uncertainty-shrunk, physics-/reliability-gated pooling of expert signals is
needed; its order bends toward "max" only under a credible, physics-consistent alarm (anti-complacency), and it
fails open to "uncertain." FM-1..FM-6 are the derived fusion-model options (precision-weighted, evidential,
conformal-stacked, covariance-intersection, physics-gated MoE, RL-tuned). **All Class-B/C fusion pieces are
advisory, unvalidated, and sit behind flags with a Class-A linear-fusion fallback (FM-1).**

## 4. Deployment topology — three compute tiers
```
 ┌── TIER 0: NODE (ESP32-C3 / ESP32-CAM, ≤₹2,000, solar+LiFePO4) ──────────────────────────────┐
 │  tiny statistical screen only: Z-score/RMS tilt, stage threshold, on-node FS, 1/v fit,       │
 │  F-15 drift pre-correction, TinyML pre-filter. Deep sleep + duty cycle. Raw video stays local.│
 └───────────────┬──────────────────────────────────────────────────────────────────────────────┘
                 │  LoRa IN865–867 (SX1262), store-carry-forward (DTN) when link down
 ┌───────────────▼── TIER 1: GATEWAY (LoRa concentrator + edge GPU/SoC + sat-IoT uplink) ───────┐
 │  CCTV detector (F-11) + temporal validation (F-12) + IR flicker (F-16); VAD; InSAR anomaly    │
 │  if cached; physics gate; local fusion + shield; CAP build + SIREN drive. Works cloud-OFFLINE. │
 └───────────────┬──────────────────────────────────────────────────────────────────────────────┘
                 │  intermittent internet / sat-IoT
 ┌───────────────▼── TIER 2: CLOUD / KAGGLE (≤30 GPU-h/wk) ─────────────────────────────────────┐
 │  frozen EO-FM embedding, SSL/anomaly training, offline-RL training, meta-head training,       │
 │  hindcast/eval harness, model registry. NEVER on the life-safety critical path (C1).          │
 └────────────────────────────────────────────────────────────────────────────────────────────┘
```
Model→tier assignment is a hard design rule (C8): heavy models (EO-FM, VAD, deep anomaly) are Tier-1/2 only;
Tier-0 runs only what fits the MCU SRAM/flash/energy budget.

## 5. Key data flows
1. **Geo early-warning (slow)**: EO datacube + IoT + precip → encoder/anomaly → physics gate → ensemble → RL →
   meta-fusion → conformal → shield → advisory level → operator. Cadence: per satellite pass + IoT heartbeat.
2. **Fire/CCTV (fast)**: frame → F-11 detector → F-12 event validation (+F-16 flicker, fire-physics soft
   features) → fusion → shield → advisory level. Cadence: near-real-time at the gateway.
3. **Offline alert (always available)**: node event → LoRa/DTN → gateway shield decision → local siren/SMS,
   independent of cloud (C1).
4. **Calibration/bias loop**: LoRa rain gauges bias-correct satellite IMERG precip; F-15 corrects IoT drift;
   F-14 raises advisory recalibration flags.
5. **Authenticity (advisory)**: inbound media → deepfake scorer → low-trust flag into fusion/operator UI.

## 6. Cross-cutting concerns
- **Calibration & uncertainty** (WS6): every probabilistic output is conformally calibrated per zone; coverage
  reported honestly (marginal, shift-sensitive), never as a "guarantee"; EDL/zero-shot for ranking/OOD only.
- **Robustness** (WS6/WS16-research): per-corruption eval; red-team (adversarial patches on the detector);
  missing-modality adapter + reliability gating so a dropped layer degrades gracefully.
- **Security** (WS6): endpoint allow-list enforced in CI (C6); signed CAP alerts; dedup; key rotation.
- **Privacy** (C7): raw video local; federated/edge-scored; only events/scores leave the node.
- **Provenance & reproducibility** (F-17): seeds pinned, spatial-CV folds logged, dagger/MLflow tracking, the
  LMEM+GLRT "real-win" gate on every improvement.
- **Energy**: camera + comms dominate; per-task energy budget is a requirement; winter/monsoon solar gaps →
  oversize power, treat node outage + missing inputs as EXPECTED, not exceptional.

## 7. Non-functional requirements
- Offline-first availability of the alert path (C1); graceful degradation under node/link/solar loss.
- Edge latency: CCTV event-to-advisory within the alert deadline at the gateway (budget set in LLD); Tier-0
  within MCU timing.
- Cost: ≤₹2,000/node (C2); compute ≤30 GPU-h/wk (C3).
- Auditability: every advisory traces to its contributing evidence + the shield reason (Rule 19 explainability).
- Honesty: no performance surface in UI/API until G2 passed; Class-C blocks flagged in output metadata.

## 8. Quality gates (map to workstreams; all must pass for "done")
| Gate | Scope | Blocks |
|------|-------|--------|
| **G1** | physics golden-case tests (geo + fire [coeff-verify]) | any downstream physics use |
| **G2** | spatial-CV admission gate (baselines + CI + cost-loss + real-win) | ANY performance claim / publication |
| **G3** | single decision fn + realizable monotone shield + measured conformal coverage | deployment |
| **G4** | fusion stability + reliability gating + shield-floor monotonicity | GMF/PHARAOH deployment |
| **G5** | ≤₹2,000 BOM (supplier-verified) + tiered feasibility + fault discrimination + LoRa band | hardware order |
| **G6** | no credential egress + offline alert path + feature-timestamp (anti-leak) audit | field pilot |
| **G7** | datacube size + dataset licenses + novelty honesty + Kaggle fit | submission |

## 9. Component → research-artifact traceability (for the build)
- Geo physics: `ws1_physics/model_set_decision.md`, `analysis/00_system_model.md`.
- Fire physics: `ws1_physics/*_P21.md` (inventory, advanced analysis, derivations ND-1..ND-7, class table).
- Fusion: `ws5_fusion/novel_aggregation_operator_P22.md`, `novel_formulas_P22.md`,
  `derivations_P22_fusion_models.md`, `rl_multimodal_integration_P22.md`, `TRINETRA_MetaFusion_Design.md`.
- Features: `FEATURES.md` (F-01..F-26), `features/wave1_specs.md` (F-11..F-17 build specs).
- Eval/decision/IoT/comms: `TRINETRA_Workstreams.md` (WS1–WS7 + gates), `HANDOFF/BUILD_HANDOFF.md`.
- Datasets: `DATASETS.md` + `DATASETS_CATALOGUE.md` (all [D] candidate, verify before use).
- Hazard-correctness bug history: `TRINETRA_Bug_Report.md`, `_Robustification.md`, `_Corrected_Patches.md`.

## 10. Risks carried into the build (top)
Spatial leakage; n≈5 geo events (variance only); INT8 smoke-recall loss; conformal under drift; IMERG
underestimation; single-node false RED; RL reward inversion; EVT instability; LoRa regulatory/band; India
dataset portals (Bhuvan/MOSDAC/VEDAS/NRSC/IMD/CWC/GSI) JS-only and unverified; Class-C physics/fusion
unvalidated and expert-review-pending. Mitigations are the gates G1–G7 and the §6 cross-cutting controls.
