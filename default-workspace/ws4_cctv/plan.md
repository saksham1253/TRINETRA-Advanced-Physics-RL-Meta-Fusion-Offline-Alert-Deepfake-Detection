# ws4_cctv/plan.md — edge deployment, label-scarcity, privacy/adversarial, interfaces (P8)

Phase P8 · WS4 · RESEARCH-ONLY. Covers §P8 tasks 7–10 (the forward plan). No performance claimed (Rule 16).

## 7. Edge deployment plan
- **Quantization:** INT8 post-training + QAT for the gateway detector; the on-node gate constrained by
  ESP32-CAM peak activation RAM (P6), not params.
- **Distillation:** distill the gateway detector into the tiny on-node gate (teacher→student) to raise the
  gate's recall at low cost.
- **Early-exit / cascade:** cheap stage exits on confident "nothing"; only candidates escalate — saves power
  (matches wake-on-event IoT, P6).
- **Latency-vs-accuracy questions to answer later:** on-node gate FPS at target res; gateway detector FPS +
  mAP at INT8 vs FP; temporal-stage window length vs TTD; all under the evaluation protocol with seed CIs.
- The low-cost camera module in the IoT build = ESP32-CAM/OV2640 (P6 BOM); gateway = Pi/phone-class.

## 8. Label-scarcity strategies (what the literature supports for our case)
- **Active learning:** prioritize labeling the hard negatives from the failure taxonomy (fog/steam/
  headlights) and early-smoke onsets — highest marginal value.
- **Self-/semi-supervised:** pretrain on unlabeled surveillance video (temporal consistency, masked-frame)
  then fine-tune on scarce fire labels; evidence from SSL video literature (fill specifics from quota reads).
- **Synthetic data (game-engine / FDS-rendered smoke):** cheap labels but a **sim-to-real gap**; use as
  augmentation + domain adaptation, validate the gap honestly (do NOT report synthetic-only numbers as real).
- Physics (P7) supplies priors/consistency that reduce the label requirement for plausibility checks.

## 9. Privacy + adversarial/tamper (design requirements)
- **Privacy:** on-device processing + face/person blurring + data minimization; verify blurring does not
  erase smoke/flame evidence (test in the protocol). No cloud upload of raw video by default.
- **Adversarial/tamper:** camera blinding/obstruction → saturation + scene-change detection + health flag +
  abstain; **replayed-video spoofing** → stream liveness/integrity + signed streams → handoff to WS2
  deepfake (P11); adversarial patches → robustness tests + cross-modal voting so vision alone can't be
  gamed.

## 10. Interfaces with other workstreams
- **WS2 deepfake (P11):** "is the stream live or replayed/manipulated?" — liveness/provenance check before
  trusting a camera alarm or all-clear.
- **WS3 alerting (P12/P13):** detection→alert handoff, confirmation windows, de-duplication across cameras,
  alert-fatigue budget; CCTV emits calibrated confidence + TTD for the decision policy.
- **WS7 IoT (P6):** cross-modal voting (camera + gas/heat/flame node); camera node wake-on-event.
- **WS8 anomaly (P9/P10):** the supervised detector's BLIND SPOTS (novel fire types, unseen nuisances) are
  the anomaly layer's explicit target; share features + health flags.
- **WS1 physics (P7):** flicker-band (B-05), plume-growth (t²/EF-03), smoke extinction (EF-07/B-01) as
  features/priors/consistency checks for both detection and false-alarm suppression.

## Deliverable status & honest gaps
- literature_map.md, DATASETS.md CCTV entries, and the named baselines + their source-reported numbers are
  populated from the P8 quota reading. If web_search is unavailable (no API key, as in P5–P7), reading is
  arXiv-only and non-arXiv benchmarks (D-Fire/FASDD/FIgLib pages) are logged as [D] discovery-only until
  portal-verified. Any such gap is stated in literature_map.md and the P8 report.
