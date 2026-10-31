# PHASE_08_report — WS4 CCTV fire/smoke DETECTION (RESEARCH-ONLY)

Phase P8 · MASTER_PROMPT L462+. Status: COMPLETE to gate (continuous mode — this is a completion record, not
a halt). No code built; no model trained; no own-system performance claimed (Rule 16).

## Objective
Define, on paper, how low-cost fixed CCTV detects fire/smoke early and robustly: SOTA scan, failure
taxonomy, a leakage-safe evaluation protocol, an edge-feasible model-selection, and interfaces to the other
workstreams — grounded in a NEW literature quota.

## What was produced
- SOTA scan: PROGRAM/sota/P8_sota_scan.md.
- ws4_cctv/failure_taxonomy.md — nuisance/condition classes A–F + test-set assembly.
- ws4_cctv/evaluation_protocol.md — PRE-REGISTERED: operating point (≤~1 false alarm/camera-day target),
  leakage-safe GROUP splits (site/camera/video; 3 tiers), metrics = time-to-detection + false-alarms/
  camera-day + PR-AUC + calibration/ECE + robustness curves + ≥5-seed CIs (NOT mAP on random splits), AC-1..6.
- ws4_cctv/model_selection.md — two-stage cascade (on-node INT8 gate → gateway small-YOLO detector →
  temporal confirmation → cross-modal+physics fusion); baselines to reproduce.
- ws4_cctv/plan.md — edge deployment, label-scarcity, privacy/adversarial, interfaces.
- ws4_cctv/literature_map.md — 41 arXiv sources (quota ≥15, aim 30-40 → exceeded).
- DATASETS D35-D44 ([D]); 17 [P8] ledger rows (full 41 in literature_map); Audit #14 PASS.

## Key findings (all source-reported)
- Canonical fixed-camera early-smoke baseline = FIgLib + SmokeyNet (2112.08598); PYRONEAR-2025 (2402.05349)
  is the real-world multi-site benchmark → both drive the leakage-safe protocol.
- Best-documented true edge baseline = OnFire compact CNNs (2010.08833, 49 fps on Jetson Xavier-NX,
  source-reported). Cheap false-alarm reduction = uncertainty post-detection re-scoring on D-Fire
  (2510.10108). Edge compression recipe = weak-label distillation WISE (2609.18227, 0.12M params).
- Hard regimes documented: early/small/thin smoke (perf scales with smoke VOLUME not contrast — 2512.11215,
  2509.12701); occlusion → smoke-motion (2307.00104); dynamic-texture confusers (1703.05530); night/heavy
  smoke → thermal/IR (2307.04223, 2606.27128); compression affects detection (2512.01788).
- EVALUATION pitfall confirmed by a WITHDRAWN paper (2508.11696): augmentation-induced leakage across
  splits → our group-split mandate is correct. MLLM/foundation detectors fail early-smoke localization →
  not primary edge detectors (relevant to P14Z).

## Architecture decision (paper)
Two-stage cascade: ESP32-CAM/OV2640 INT8 on-node motion+color gate → Pi/phone-class gateway small-YOLO
detector → temporal persistence confirmation → cross-modal (environmental sensors / P7 fire-physics priors)
+ P9/P10 anomaly fusion. Replayed-video spoofing → WS2/P11. Open-vocab/zero-shot → P14Z. Security: a
network-exposed gateway inference endpoint MUST have authentication + access control (flagged now; absent by
default is unacceptable for a safety function).

## Honesty & limits (§0.5)
- All 41 reads are ABS (0 FT); several metrics truncated → marked "not retrieved", not invented. Paper IDs
  are subagent-reported, not each re-fetched. web_search had no API key; arXiv API rate-limited.
- Acceptance criteria AC-1..6 are PROCESS/validation targets, NOT achieved results.
- Datasets [D], licenses unverified; FASDD/MIVIA + tamper/spoof/privacy + explicit nuisance (steam/cloud/
  fog/sunset) studies are OPEN actions for non-arXiv portals.

## Open actions carried
Verify dataset licenses (esp. D-Fire/FIgLib/PYRONEAR); search non-arXiv (MDPI Sensors/Fire, IEEE) for
tamper/spoofing/privacy + nuisance-confuser studies; reproduce D-Fire YOLO-nano + SmokeyNet baselines under
the leakage-safe protocol at build time.

## Gate
PROGRAM/gate_messages/PHASE_08_gate.md. Auto-proceeding to P7G then P9 (continuous mode).
