# ws8_anomaly/build_plan.md — anomaly layer build plan (P9, WS8a → feeds P10)

Phase P9 · RESEARCH-ONLY (planning). What the later build would do, in priority order, under Kaggle ≤~30
GPU-h shared + ESP32 edge + offline-first. Nothing is built or run here. Detailed per-family specs are P10.

## Priority & sequence
1. (b) Sensor time-series + (c) OOD/model-health + (d) physics-residual — the cheap, high-value core.
   Build simple baselines FIRST (z-score/EWMA/CUSUM/iForest/Mahalanobis), then a deep model ONLY if it
   beats them on strict event-level/delay-aware metrics with CIs (evaluation_protocol §6).
2. (a) Video anomaly on the gateway (support/escalation only) — pretrained-feature kNN / reconstruction.
3. (e) Network/alert anomaly — signing+replay (from P6) + light rate/behavior rules.
4. (g) Data-quality anomaly over our own datasets (build hygiene; feeds P16 robustness).
5. (f) Social-media surge — DEFERRED, doc-only, aggregate burst, privacy-gated.

## Kaggle GPU-hour planning (estimates; shared pool, ≥15% reserve)
- Sensor TS deep model (if it earns its place): ~2-3 GPU-h incl. seeds/ablations.
- Video anomaly (gateway, pretrained features): ~3-4 GPU-h (feature extraction + kNN/AE, 5 seeds).
- OOD/model-health: ~0.5 GPU-h (features already produced by P8/P14).
- Physics-residual: ~0 GPU-h (reuses P7/P7G).
- Network/alert: ~0 GPU-h (rules + tiny model).
- Simple baselines across all: CPU-only.
TOTAL anomaly share ≈ 6-8 GPU-h of the ~30 (confirm against KAGGLE_BUDGET.md; all ESTIMATES).

## Data plan
- Public benchmarks (with documented flaws) for method development only; our OWN normal-only logs/footage
  (collected in build) for the real operating-point numbers. Normal-reference policy per design §7.
- All datasets [D] discovery-only until license/coverage verified (DATASETS.md).

## Edge (ESP32) plan
Statistical + rate-of-rise + tiny-AE/iForest on sensor windows; fixed-point; bounded buffers; watchdog-safe;
report measured memory/latency in the hardware phase (P13). Video anomaly excluded from the node.

## Verification & honesty
Every build-phase number will be reported under the strict pre-registered protocol with ≥5 seeds + CIs; no
point-adjust as a primary number; simple baselines are the admission gate. No performance is claimed now.
