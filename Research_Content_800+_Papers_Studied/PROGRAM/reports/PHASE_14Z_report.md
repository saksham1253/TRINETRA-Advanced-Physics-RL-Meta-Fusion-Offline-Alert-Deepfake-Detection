# PHASE_14Z_report — ZERO-SHOT / OPEN-VOCAB HAZARD RECOGNITION (DESIGN / ON-PAPER)

Phase P14Z (program-inserted). Status: COMPLETE to gate (continuous mode). Nothing trained/measured (Rule 16).
Rule 19: advisory, human-in-the-loop.

## Objective
Decide and design the role of zero-shot / open-vocabulary vision-language recognition as a COMPLEMENT to the
trained CCTV fire/smoke detector.

## Governing decision — D-011
Zero-shot/open-vocab VLMs admitted ONLY as a CALIBRATED, LOW-WEIGHT COMPLEMENTARY evidence channel into the
P14 fusion layer; the trained P8 detector remains primary. Evidence (source-reported): in the fire domain
trained models BEAT zero-shot (WildFireCan custom 84.48% > ZS VLMs, 2504.13231; AI4Fire — no core ZS model
beat trivial baselines, 2610.10946; wildfire-PM2.5 — BiLSTM beats FMs, ZS tail-unstable, 2607.07951), and ZS
is miscalibrated/over-confident/fine-grained-confused (2303.12748, 2512.12997, 2404.03539).

## Deliverables
- ws4_cctv/zero_shot_design.md — D-011; where ZS adds value (open-vocab/unknown-hazard breadth, descriptive
  prompts, ZS-anomaly complement); MANDATORY calibration-before-fusion (one temperature per backbone,
  Dirichlet uncertainty, entropy/prob-diff features, leakage de-rating); domain-shift handling (test-time
  prompt adaptation, grounded-reference trick); evaluation on an internal leakage-free set.
- PROGRAM/sota/P14Z_sota_scan.md — SOTA + process targets.

## Quota (10 required → MET)
16 NEW primary arXiv (ABS): EVA-CLIP/Long-CLIP/microCLIP; WinCLIP ZS anomaly/CoDeGraph/QFCA; DynaPrompt/
MetaTPT; TruZe/CEZSAR; WildFireCan/AI4Fire/wildfire-PM2.5; ZS calibration (one-temperature, adversarial-CLIP);
CLIP fine-grained roadblock. 0 FT; running body-level deep FT NEW unchanged at 100.

## Honesty & gaps
On-paper only; ZS UNDER-performs trained detectors in-domain → complement not replacement. No clean
permissively-licensed CCTV ZS fire benchmark (D99-D101 leakage/label-flawed) → curate internal held-out set.
ABS depth; IDs subagent-reported not re-fetched.

## Gate
PROGRAM/gate_messages/PHASE_14Z_gate.md. Auto-proceeding to P15 (RL design) — reader (21 papers) ALREADY
PIPELINED and in hand.
