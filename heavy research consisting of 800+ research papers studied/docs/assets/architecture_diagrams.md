# assets/ — Diagrams and shared figures

ASCII/Mermaid diagrams referenced across chapters. All diagrams are design-level; none depicts measured
behaviour. Keep in sync with `docs/_CANON.md`.

## A1. End-to-end pipeline (spine)

```
 L1 SENSE            L2 PROCESS                                        L3 DECIDE         L4 ACT
 EO/satellite ─┐     encoders (frozen EO-FM, CCTV detector, IoT)      conformal         operator UI
 CCTV/vision ──┼───► anomaly (resid + Deep-SVDD + iForest + XGB) ─┐   calibrate ───►     (HUMAN gate)
 ground IoT ───┘     physics gate (geo FS/Iverson/Fukuzono/Caine; │   (per-zone,          │
 inbound media ───►  fire Heskestad/Byram/Strouhal; PINN=soft)    ├─► META-FUSION ──►    shield (monotone
                     supervised ensemble (XGBoost + per-hazard)   │   (GMF+PHARAOH+FM)   floor; RAISE-only)
                     offline-RL advisory policy (shielded) ───────┘                      └─► LEVEL
 authenticity (deepfake scorer) ─────────────────── low-trust advisory ────────────────► into fusion/UI
 drift/calibration monitor ──────────────────────── advisory recalibration flag
```

## A2. Three compute tiers

```
TIER 0 NODE (ESP32, ≤₹2000, solar)  →  tiny stats only; RAW VIDEO STAYS LOCAL
      │ LoRa IN865–867 MHz (SX1262), store-carry-forward DTN when link down
TIER 1 GATEWAY (LoRa concentrator + edge GPU)  →  detector + physics + LOCAL fusion+shield + siren; CLOUD-OFFLINE
      │ intermittent internet / sat-IoT
TIER 2 CLOUD/KAGGLE (≤30 GPU-h/wk)  →  EO-FM embed, training, eval, registry; NEVER on the alert critical path
```

## A3. Single decision function

```
level(s) = max( conformal_level( fused_risk(s), p* ) , shield_floor(s) )
           p* = C_FA / (C_FA + C_miss) = 5 / (5 + 100) ≈ 0.0476
shield_floor can only RAISE the level (deterministic, monotone, post-posed after the learner).
```

## A4. Alert fan-out (tiered, offline-first)

```
                       ┌─ local siren / strobe (always, offline)
event ─► node ─LoRa─►  gateway ─► operator (HUMAN approves) ─► CAP/SACHET (signed) ─┬─ LAN/mesh push
   │ DTN store-carry-forward if gateway unreachable                                 ├─ cellular SMS (where avail)
   └─ raw video NEVER leaves the node (C7)                                          └─ cell broadcast (authenticated)
                                                                                     ✗ IP-address targeting = INFEASIBLE
```

## A5. Honesty admission gate (R16)

```
candidate metric ─► spatial-block CV ─► beat {climatology, logistic/GBDT, persistence}? ─no─► "does not beat baseline"
                                                      │ yes
                                           paired block bootstrap (BCa) real-win CI lower bound > 0 ? ─no─► blocked
                                                      │ yes
                                           ReportGuard emits the metric (per-hazard, with CI, calibrated)
```
