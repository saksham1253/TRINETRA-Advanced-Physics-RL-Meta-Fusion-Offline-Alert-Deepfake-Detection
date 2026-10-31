# ws8_anomaly/spec/edge_spec.md — EDGE (ESP32-class) anomaly detector spec (P10, WS8b)

RESEARCH-ONLY. Lightweight on-node detector(s) with LITERATURE-BASED (source-reported) memory/latency/
accuracy expectations and the measurements to take later in the hardware phase (P13). No own measurement
claimed (Rule 16). Precise defaults [recipe-cite — P10 reader].

## 1. What runs on the node
ONLY family-B sensor-stream detection (statistical + optional tiny model) + sensor-fault/stuck/drift flags +
rate-of-rise. Video anomaly, OOD-on-vision-features, and heavy IDS run on the GATEWAY, not the node.

## 2. Detector stack (node)
- ALWAYS: robust z-score (median/MAD), EWMA (λ 0.1-0.3), CUSUM (k=0.5σ, h=4-5σ), rate-of-rise thresholds,
  stuck/flat-line + out-of-range checks. Fixed-point; bounded ring buffers; watchdog-safe.
- OPTIONAL tiny model (only if it earns its place over the statistical stack): INT8 autoencoder or iForest-
  lite on windowed features via TFLite-Micro.

## 3. Source-reported feasibility envelope (NOT ours)
- On-device z-score: ~3.3 KB SRAM + 63 KB Flash, tens-of-µs latency, on-device train+infer (2604.08581).
- INT8 AE on ESP32-S3: ~180 KB model, ~9 ms latency, recall 84%/F1 79% on an ECG task (2606.02256).
- K-means TinyML + "train once share everywhere" model distribution for node fleets (2603.27393).
- NAS op-count latency proxy for sizing (MicroNets 2010.11267, TinyMLperf anomaly task).
- Dual supervised+unsupervised edge IDS budgets (FPGA): 0.25-0.42 ms, <1.1 mJ/msg (2610.07489) — upper-bound
  reference, our node is MCU not FPGA.
These are OTHER teams' numbers on OTHER hardware/tasks; our ESP32 figures MUST be measured in P13.

## 4. Memory/latency/energy budget (targets to measure in P13)
Target: statistical stack < a few KB SRAM, sub-ms; optional tiny AE ≤ ~200 KB flash, ≤ ~10-20 ms, fits
alongside the P8 on-node vision gate and the P6 radio duty cycle. All TARGETS; measured later.

## 5. Accuracy-loss expectation
Quantization (FP32→INT8) accuracy loss to be measured (expect small per TFLite-Micro literature); the
statistical stack has no quantization loss. Report measured loss in P13.

## 6. Fallback
If the tiny model is unavailable/over-budget, the node runs the statistical stack alone (graceful
degradation, design §10).

## 7. Measurements to take later (P13)
Peak SRAM, flash, per-window latency, energy per inference, battery impact, accuracy vs the gateway detector,
false-alarms/sensor-day on-node — all on the exact MCU in the P6 BOM.

## 8. Verification checklist
[ ] fixed-point + bounded buffers + watchdog-safe  [ ] statistical stack runs with no model  [ ] tiny model
only if it beats statistical  [ ] all cited envelopes labelled source-reported/other-hardware  [ ] P13
measurement list carried.
