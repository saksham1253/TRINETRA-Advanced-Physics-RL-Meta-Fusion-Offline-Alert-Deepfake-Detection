# P6 SOTA SCAN — Low-cost multi-sensor & TinyML fire detection

Phase P6 · 2026-10-07 · RESEARCH-ONLY. SOTA scan FIRST (§P6 task 1), before component selection. This
records the current state of the art for (a) low-cost multi-sensor fire detection and (b) TinyML/edge
fire detection — their sensors, costs, and reported results WITH conditions. Numbers below are
SOURCE-REPORTED, never ours (§0.5). arXiv IDs were surfaced live via the arXiv API this session; the
15-paper quota reading (incl. non-arXiv MDPI open-access, per D-010 because the arXiv fire-IoT vein is
THIN) is logged separately in ws7_iot/literature_map.md + PROGRAM/logs/P6_reading_progress.md.

HONEST VEIN NOTE (§0.5, D-010): arXiv is sparse for on-device sensor-fusion fire detection
(all:"fire detection" AND all:"multi-sensor" returned only 2 hits; all:"flame detection" AND
all:"deep learning" only 1; all:"TinyML" AND all:"fire" only 2). The live field is largely in IEEE
Sensors/IoT-J and MDPI Sensors/Fire/Electronics. P6 therefore pulls from OPEN-ACCESS non-arXiv venues
for the quota, flagged honestly.

---

## A. Vision / camera-based fire & smoke detection (feeds the Type-B camera node)
- **EFA-YOLO (2409.12635)** — lightweight flame/fire detector: SOURCE-REPORTED 1.4M params, 4.6 GFLOPs,
  22.19 ms/image on CPU; claims mAP gains + ~88× speed over YOLOv5/8/9/10 and 94.6% fewer params. →
  Evidence that a flame detector can run on cheap edge hardware; a realistic target for the ESP32-CAM
  node (confirm RAM/flash feasibility on ESP32 specifically — YOLO on a microcontroller is still tight).
- **Reliable Smoke Detection (2508.14597)** — optical-flow-guided feature fusion + Swin-Transformer with
  aleatoric+epistemic UNCERTAINTY, monocular (no multi-sensor array). → the uncertainty + motion-cue idea
  is directly relevant to cutting smoke-vs-steam false alarms on a single camera; too heavy for ESP32 as-is
  (a design pattern, not a deployable model here).
- **PyroFocus (2512.03257)** — two-stage classify→FRP-regression/segmentation for ONBOARD (satellite)
  real-time wildfire; two-stage pipeline reduces inference cost. → pattern: cheap gate first, expensive
  stage only when gate fires (mirrors our layered on-device logic).
- **Thermal-RGB fusion micro-UAV (2512.12199)** — adaptive-threshold thermal hot masks + RGB edge/gradient
  false-detection suppression, SOURCE-REPORTED sub-50 ms on embedded SoC. → cheap rule-level RGB+thermal
  fusion is viable on edge; supports an IR/thermal add-on IF budget allows.

## B. Multi-sensor fusion & false-alarm suppression (feeds the Type-A sensor node — the core)
- The dominant SOTA message (across the fire-alarm-engineering + sensor-fusion literature to be read in the
  quota): cheap single sensors (MQ-2 smoke/gas, IR flame, thermistor) FALSE-ALARM heavily; robustness comes
  from REQUIRING cross-modal corroboration (smoke + heat-rate + flame) and from rate-of-rise logic, not
  from any single better sensor. (Quantified source numbers pending the quota reads.)
- **AoI / context-aware status updating (2310.06224)** — scheduling sensor updates (e.g. CO density for
  fire) to minimize "situation-unaware penalty"; keeping channels busy is optimal; up to 100× gain over
  periodic updating (source-reported, simulation). → informs WS3 alerting freshness + our duty-cycle/
  reporting policy, not the sensing itself.

## C. TinyML / edge deployment reality
- Field converging on quantized, <few-M-param models with tens-of-ms latency on MCU/SoC (EFA-YOLO, thermal
  fusion, PyroFocus two-stage). SNN/neuromorphic work (2411.01628, 2601.12156) shows energy wins but needs
  FPGA/ASIC — NOT our ESP32 path (noted, not adopted).
- Implication: on ESP32-class hardware, prefer (1) classical threshold + rate-of-rise + multi-sensor fusion
  as the always-on core, and (2) a small quantized classifier only on the camera node / on fused features,
  with a cheap gate in front (two-stage pattern) to save power.

## D. SOTA-scan takeaways feeding component selection + design
1. **False alarms are the enemy** → multi-sensor fusion + rate-of-rise is non-negotiable; this drives the
   "fewer, richer nodes" decision in design.md §1.
2. **Edge fire ML is feasible but tight** → camera node (Type B) is OPTIONAL/secondary; the cheap
   always-on core is sensor fusion on an ESP32 (Type A).
3. **Two-stage / layered compute** (cheap gate → expensive confirm) is the recurring efficiency pattern →
   adopted in design.md §3.
4. **Uncertainty + nuisance discrimination** (steam, sunlight, cooking) is where SOTA adds value → our
   acceptance criteria require a repeated-trial false-alarm comparison vs nuisance sources.
5. **arXiv is thin here** → the quota legitimately draws on open-access MDPI/IEEE; recorded honestly.

(Quota reading — ≥15 NEW, incl. non-arXiv — and the numeric baselines table are compiled in
ws7_iot/literature_map.md once the dedicated reading pass completes.)
