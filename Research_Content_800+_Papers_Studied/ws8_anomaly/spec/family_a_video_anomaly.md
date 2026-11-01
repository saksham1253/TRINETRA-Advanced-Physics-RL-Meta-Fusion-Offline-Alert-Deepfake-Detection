# ws8_anomaly/spec/family_a_video_anomaly.md — BUILD SPEC: video anomaly (SUPPORT-only) (P10, WS8b)

PRIORITY 2 — SUPPORT role ONLY. Runs on the GATEWAY, never the node. RESEARCH-ONLY. External numbers
SOURCE-REPORTED (Rule 16). Rule 19: ESCALATE/abstain only — NEVER an autonomous fire alarm. Precise defaults
[recipe-cite — P10 reader].

## 1. Method and why
Job: cover the supervised P8 detector's BLIND SPOTS — unknown hazards, camera failure/tamper/occlusion,
unusual scene events — by flagging for human review. Evidence: cheap pretrained-feature scoring and
reconstruction/future-frame prediction are the deployable families; MLLM/VLM scoring adds explainable
rationales cheaply (RBA 2610.05129 ~0.012% params; logit-interface VLM verification robust, 2609.07455);
adaptive temporal granularity matters for variable-duration events (2609.05066). CRITICAL eval caveats:
Micro-AUROC ≠ localization → report Within-AUROC (2608.21854); detectors latch onto background/scene bias →
patch-level audit (2608.12045). High false-alarm is expected → SUPPORT only.

## 2. Inputs/outputs
INPUT: gateway camera frames/clips. OUTPUT: region/track-level anomaly score + an ESCALATE flag (with
temporal persistence) + an optional VLM rationale string. Feeds P13 dashboard + P14 fusion as a support
signal; never triggers alerting autonomously.

## 3. Data/splits
Public (method dev, SUPPORT scope): UCF-Crime (D55), XD-Violence (D56), ShanghaiTech/Avenue/Ped (D57) — all
flawed. OWN normal CCTV footage for the real false-alarm/camera-day number. CAMERA+SITE-grouped splits; no
camera in both train/test (evaluation_protocol §3).

## 4. Normal-reference policy
Per-camera normal model (fixed-camera scene); refresh on scene change (new furniture/layout) with change-
point guard; beware learning "the room not the smoke" (2608.12045).

## 5. Features/architecture/defaults
Default (cheap, deployable): pretrained-feature kNN / density scoring on frozen backbone features; secondary
reconstruction-AE or future-frame prediction error. Optional VLM verification via LOGIT interface (Yes/No
next-token prob) for high-scoring segments (2609.07455) — more robust than text-gen parsing. Adaptive
temporal module for duration variability (2609.05066). Backbone/latent/k defaults [recipe-cite — P10 reader].

## 6. Thresholding/calibration
Per-camera threshold on validation for a tolerable false-alarms-per-camera-day (set by P12 budget); temporal
persistence (≥ N frames) before escalation; hysteresis.

## 7. Metrics
REGION/TRACK-based metrics + Within-AUROC (NOT pooled Micro-AUROC alone, 2608.21854) + false-alarms/camera-
day; detection delay. ≥5 seeds + CIs. Background-bias audit via patch-level protocol (2608.12045).

## 8. Baselines first
Frame-difference / optical-flow energy + PCA/AE reconstruction + kNN on pretrained features before any
heavier model.

## 9. Ablations/stress
Backbone; with/without VLM verification; adaptive vs fixed temporal; cross-camera transfer; lighting/weather;
tamper/occlusion/blinding; background-bias (patch audit).

## 10. Acceptance (targets)
Usable as SUPPORT (escalation) at a tolerable false-alarms/camera-day under camera-grouped splits with
region/Within-AUROC reported; NOT an autonomous alarm.

## 11. Pitfalls
High intrinsic false-alarm; background/scene shortcut (2608.12045); Micro-AUROC illusion (2608.21854); VLM
text-gen fragility (use logit interface); privacy (operate on scene dynamics, not identity — §ethics).

## 12. GPU hours
≈3-4 Kaggle GPU-h (feature extraction + kNN/AE, 5 seeds). ESTIMATE.

## 13. Verification checklist
[ ] camera/site-grouped splits  [ ] Within-AUROC + region metrics reported (not Micro-AUROC alone)
[ ] false-alarms/camera-day at P12 budget  [ ] temporal persistence  [ ] background-bias audited
[ ] SUPPORT-only wiring (no autonomous alarm)  [ ] privacy: no identity features  [ ] defaults cited.
