# 06 — ZERO-SHOT + DETECTORS (Hinglish)
**Zero-shot kya hai:** model ko bina training ke text prompt do ("a photo of fire", "a photo of steam") aur woh image se
similarity score de. Isse training data nahi chahiye, sirf **evaluation data** chahiye (09b: P01, P03, P06).

**Repo status:** design only. `ws4_cctv/zero_shot_design.md` (decision D-011) says zero-shot is a low-weight, calibrated
*complement* and never the primary detector. **No code found** (GAP G-01).

**Detector in code:** `deep/fire_cnn.py` FireSmokeNet (per-frame CNN, then GRU, then [fire, smoke]). `ws4_cctv.TemporalValidator`
confirms only if confidence persists across frames (rejects glints, headlights, single steam puffs). The physics gate
(`ws1a_firephys/gate.py`) down-weights wind-dominated regimes. The Strouhal flicker aux loss is Class C and OFF.

**Known failure cases (from the repo design doc, source-reported):** smoke vs steam/fog/dust confusion, compression, night,
small/distant smoke, miscalibrated CLIP scores.

**Proposed minimal implementation (NEW file, flag-gated, UNTESTED):** `zeroshot/clip_expert.py`: open_clip ViT-B-32, prompt
ensembles per class, then temperature scaling on a val split, then `ws5_fusion_rl.adapters.deep_expert(...)`. Cap reliability at 0.5.
Evaluate PR-AUC + ECE on P01 + P03 (positives) vs P06 confusers (negatives).
<!-- END -->
