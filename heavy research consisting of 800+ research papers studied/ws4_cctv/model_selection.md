# ws4_cctv/model_selection.md — evidence-based model selection (P8)

Phase P8 · WS4 · RESEARCH-ONLY. Alternatives, evidence, expected budget fit, and a shortlist with the
published baselines to reproduce FIRST. No performance is claimed for our system (Rule 16); "expected" =
reasoning from the literature + the P6 edge-hardware reality, to be validated under the evaluation protocol.

## Decision context (constraints)
- Edge: low-cost camera node (P6: ESP32-CAM is INT8-tiny-model-only; a Raspberry-Pi-class or phone-class
  gateway can host a real detector). So selection is TWO-TIER: a tiny on-node gate + a stronger gateway/
  server detector.
- Early/small smoke + compression + night are the hard conditions; false-alarm control is decisive.
- Physics (P7) + cross-modal (IoT) available as corroboration.

## Alternatives considered (evidence → fit)
| Approach | Evidence | Edge fit | Verdict |
|----------|----------|----------|---------|
| Classical cues (color/motion/flicker/freq) | cheap, interpretable; weak alone | runs on-node | KEEP as cheap gate + physics-consistency, not standalone |
| YOLO-family detector (v8/v10/11, efficiency variants) | dominant, strong mAP; small variants exist (EFA-YOLO 1.4M params source-reported) | small variant INT8 on gateway; too big for ESP32 full | SHORTLIST — gateway detector |
| DETR / transformer detector | strong global context; heavier | server tier | note; not edge node |
| Video transformer / 3D-CNN / ConvLSTM (temporal) | best false-alarm reduction via smoke growth/flicker | gateway/server | SHORTLIST — temporal confirmation stage |
| Two-stage cascade (cheap gate → detector) | PyroFocus pattern; matches wake-on-event IoT | ideal | SHORTLIST — system architecture |
| Open-vocabulary / foundation detector | zero-shot prompts; large | server; → P14Z | defer to P14Z |
| Anomaly/one-class on video | catches the detector's blind spots | gateway | hand to WS8 (P9/P10) |

## Selected architecture (justified)
**Two-stage cascade:**
1. **On-node gate (tiny, INT8):** cheap always-on motion/color/flicker + optional tiny CNN on the ESP32-CAM
   to wake the pipeline — tuned for HIGH RECALL (don't miss), tolerating false positives it passes upward.
   Physics flicker-band (B-05) + plume-growth as cheap priors.
2. **Gateway detector (small YOLO-family):** the main fire+smoke detector on a Pi/phone-class device;
   reproduce a published small-YOLO fire/smoke baseline FIRST, then add efficiency/attention variants.
3. **Temporal confirmation (ConvLSTM / optical-flow / short video transformer):** confirm smoke GROWTH and
   flame flicker over a short window to suppress nuisances; emits calibrated uncertainty.
4. **Cross-modal + physics fusion:** combine with IoT gas/heat (P6) and physics consistency checks (P7);
   final decision in the meta-fusion/alert layer (P14/P12). Abstain when uncertain.

## Published baselines to reproduce first (reference points, source-reported protocols)
- A recent small-YOLO fire/smoke detector on **D-Fire** and/or **FASDD** (reproduce their mAP under their
  split, THEN re-run under our leakage-safe split).
- A wildfire-smoke temporal baseline on **FIgLib** (time-to-detection reference).
- The exact models + numbers to be filled from the P8 quota reading (literature_map.md).

## Expected budget fit (reasoning, not measurement)
- On-node gate: INT8 tiny model within ESP32-CAM peak-SRAM budget (P6) — feasibility, not accuracy, is the
  node constraint. Gateway detector: small-YOLO INT8 runs real-time on Pi-class hardware per the literature.
  To be VALIDATED (latency/accuracy) at build time under the evaluation protocol.

## Open items → quota reading / later phases
- Fill the named baselines + their source-reported numbers from literature_map.md.
- Replayed-video/tamper liveness → WS2/P11. Anomaly blind-spot layer → WS8/P9-P10. Zero-shot/open-vocab →
  P14Z. Final decision policy + de-duplication + confirmation windows → P12/P13.
