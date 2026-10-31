# PROGRAM/sota/P14Z_sota_scan.md — zero-shot / open-vocab hazard recognition SOTA (P14Z)

Phase P14Z · RESEARCH-ONLY. SOTA + targets. All numbers SOURCE-REPORTED (Rule 16); detail + IDs in
ws4_cctv/literature_map.md P14Z section. No own-system claim.

## 1. SOTA landscape
- BACKBONES: EVA-CLIP 82.0/80.4 zero-shot ImageNet-1K top-1 (2303.15389); Long-CLIP long-prompt capability,
  +~6% COCO/Flickr retrieval retaining zero-shot (2403.15378); microCLIP +2.90% over 13 fine-grained
  benchmarks, label-free (2510.02270).
- ZERO-SHOT ANOMALY (unknown-hazard analogue): WinCLIP-based VAND entry 81.5 sample-F1 / only 24.2 pixel-F1
  on VisA (2306.09269); QFCA ~10× faster at ~equal accuracy (2510.15602); CoDeGraph fixes "consistent
  anomaly" bias (2512.02520).
- TEST-TIME ADAPTATION: DynaPrompt (14 datasets, 2501.16404); MetaTPT SOTA domain-generalization (2512.12268);
  BETA black-box TTA +3.4% ImageNet-C (2604.15609).
- CALIBRATION: zero-shot CLIP miscalibrated, one temperature per backbone transfers across prompt+dataset
  (2303.12748); Dirichlet uncertainty under adversarial perturbation (2512.12997).
- FIRE-DOMAIN REALITY: trained > zero-shot (WildFireCan 84.48% custom, 2504.13231; AI4Fire FMs lose to trivial
  baselines, 2610.10946; wildfire-PM2.5 FMs lose to BiLSTM + tail-unstable, 2607.07951).
- FAILURE MODES: fine-grained confusion (2404.03539); compression fragility (2311.14029); benchmark leakage
  inflates zero-shot up to 8.9% (TruZe 2107.13029); zero-shot action recognition (CEZSAR 2605.01165).

## 2. TARGETS section (process targets, NOT results, Rule 16)
- Admit zero-shot ONLY as a calibrated, low-weight COMPLEMENT (D-011); trained P8 detector remains primary.
- Temperature-scale (one per backbone) + Dirichlet uncertainty BEFORE fusion; feed entropy/prob-diff too.
- Evaluate on an INTERNAL leakage-free held-out set with proper scoring rules + calibration.
- Report standalone zero-shot weakness honestly + marginal contribution in the P14 ablation (with vs without).
- Per-camera test-time prompt adaptation to handle site/weather/lens shift; grounded-reference-frame trick.

## 3. Honesty
All source-reported. Fire-specific evidence shows zero-shot UNDER-performs trained detectors; no clean
permissively-licensed CCTV zero-shot fire benchmark exists (leakage/label flaws) → curate internal set.
