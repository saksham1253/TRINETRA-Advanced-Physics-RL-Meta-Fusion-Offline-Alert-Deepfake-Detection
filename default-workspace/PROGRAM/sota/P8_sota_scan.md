# P8 SOTA SCAN — CCTV-based fire/smoke detection (WS4)

Phase P8 · WS4 · RESEARCH-ONLY. SOTA scan FIRST (§P8 task 1). Records the state of the art in CCTV fire/
smoke detection, the benchmarks + protocols people report on, and the KNOWN FLAWS of those protocols, to
set honest "SOTA targets and protocol plan". Numbers are SOURCE-REPORTED, never ours (Rule 16). The ≥15 NEW
quota reads (aim ~40) are logged in ws4_cctv/literature_map.md; this scan is the orientation.

## 1. Approach families (what's used)
- **CNN detectors / YOLO-family (dominant for edge):** YOLOv5/v8/v10/11 variants fine-tuned for fire+smoke;
  attention/efficiency tweaks (e.g. EFA-YOLO from P6 reading: source-reported 1.4M params / 4.6 GFLOPs).
  Pros: fast, small, deployable; cons: box labels, weak on small/early smoke, site-overfit.
- **Transformers / DETR-family / video transformers:** better global context + temporal modeling for smoke
  diffusion; heavier → usually a server/edge-GPU tier, not an ESP32-class node.
- **Temporal / motion models (optical flow, 3D-CNN, ConvLSTM):** exploit smoke's slow growth + flicker;
  strong false-alarm reduction but need video, not frames (P6 reading: optical-flow + transformer with
  calibrated uncertainty).
- **Two-stage cascades:** cheap always-on classifier wakes an expensive detector only on candidates
  (PyroFocus pattern from P6) — the natural fit for a low-power camera node.
- **Open-vocabulary / foundation detectors:** promising zero-shot smoke/flame prompts but large; relevant to
  P14Z (zero-shot) more than to the edge node.
- **Classical cues (color, motion, flicker, frequency-domain, background subtraction):** cheap, interpretable
  priors — pair with the PHYSICS features from P7 (flicker band EF-08/B-05, plume growth, extinction) as
  consistency checks rather than standalone detectors.

## 2. Benchmarks & protocols people report (and their flaws)
- Common datasets: D-Fire, FASDD, FIgLib (wildfire smoke time-lapse), Foggia/MIVIA video, HPWREN/wildfire
  camera sets, synthetic (game-engine/FDS) smoke. (Verified entries → DATASETS.md during quota reading.)
- Reported headline = mAP@0.5 / F1 / accuracy on a RANDOM split → **the central flaw**: near-duplicate
  frames from the same video/camera land in both train and test → leakage → inflated numbers that do NOT
  transfer across sites. SOTA protocol plan MUST use **group splits by video/camera/site**.
- Rarely reported but operationally decisive: **time-to-detection** and **false-alarms per camera-day** at a
  fixed operating point, and **cross-site** generalization. These, not mAP, are our acceptance axes.

## 3. The hard case: early / small smoke
- Small, translucent, low-contrast early smoke is where detectors fail and where EARLY warning matters most;
  literature consistently shows accuracy collapses for small smoke and at low resolution/compression.
- Implication: evaluate explicitly at small-object scales + under CCTV compression; use temporal growth
  (physics: plume/t² growth) as corroboration.

## 4. False alarms / nuisances (feeds failure_taxonomy)
Clouds, fog, haze, dust, steam, sunrise/sunset glow, headlights, reflections, red/orange objects, flashing
lights, camera shake, rain on lens, insects/birds, IR hotspots (sun, heaters). Literature mitigations:
temporal persistence, multi-frame confirmation, multi-class smoke (benign vs dangerous — P6 D27), cross-
modal voting (camera + IoT gas/heat), uncertainty + abstention.

## 5. Edge / robustness / security
- Edge: INT8 quantization, distillation, early-exit, cascades; latency-vs-accuracy to be measured later.
- Robustness: compression + low-res as first-class test conditions (not an afterthought).
- Security: camera tamper/blinding + **replayed-video spoofing** (ties the deepfake workstream WS2/P11 —
  "is the stream live or replayed?"); privacy (face blurring, on-device processing) as a design requirement.

## SOTA-scan takeaways → P8 plan
1. Model selection shortlist should center on a **YOLO-family edge detector + a temporal confirmation stage
   in a two-stage cascade**, with published baselines to reproduce first; transformers/open-vocab noted as a
   server tier / P14Z.
2. The evaluation protocol's headline is **leakage-safe group splits + time-to-detection + false-alarms per
   camera-day + cross-site CIs over seeds**, NOT mAP on random splits.
3. Early/small smoke + compression + night/IR are explicit test conditions.
4. Physics (P7) enters as features/priors/consistency checks; nuisances handled by temporal persistence +
   multi-class + cross-modal voting + uncertainty/abstention.
5. Honest: all numbers here are from the literature; we claim NO performance for our own system (Rule 16).
