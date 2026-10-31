# ws4_cctv/zero_shot_design.md — zero-shot / open-vocabulary hazard recognition (P14Z)

Phase P14Z (program-inserted) · RESEARCH-ONLY, on-paper. Zero-shot / open-vocabulary vision-language
recognition as a COMPLEMENT to the trained CCTV fire/smoke detector (P8), NOT a replacement. All numbers
SOURCE-REPORTED (Rule 16). Rule 19: advisory, human-in-the-loop. Governing decision: D-011 (below).

## D-011 — role of zero-shot in the system (DECISION)
Zero-shot/open-vocab VLMs are admitted ONLY as a COMPLEMENTARY, CALIBRATED, LOW-WEIGHT evidence channel into
the P14 fusion layer — never as the primary fire/smoke detector. RATIONALE (source-reported):
- In the FIRE domain specifically, trained detectors BEAT zero-shot: WildFireCan-MMD custom model 84.48%
  f-score > zero-shot VLMs (2504.13231); AI4Fire found NO core zero-shot model beat trivial baselines across
  5 wildfire tasks and documented leakage/label flaws (2610.10946); wildfire-PM2.5 foundation models lose to
  a trained BiLSTM and show heavy-tailed OOD instability (negative R², 2607.07951).
- Zero-shot CLIP is empirically MISCALIBRATED (2303.12748), becomes OVER-CONFIDENT under perturbation
  (2512.12997), and confuses fine-grained classes — smoke vs steam/fog/dust (2404.03539) — exactly the
  nuisance discrimination a fire system must get right.
⇒ Use zero-shot where it is actually strong: OPEN-VOCAB coverage of hazard categories the closed-set detector
was never trained on (an "unknown/novel hazard" complement), always calibrated and fused at low weight under
the P14 rules.

## 1. What zero-shot adds (and where)
- OPEN-VOCAB / UNKNOWN-HAZARD breadth: recognize hazard scenes outside the trained label set (open-world
  complement), analogous to zero-shot anomaly scoring (WinCLIP-style, 2306.09269) for "this looks wrong but
  isn't a trained class".
- DESCRIPTIVE PROMPTS: long descriptive scene captions via Long-CLIP (2403.15378) ("thick grey smoke rising
  above a tree line") rather than single words.
- Backbone: a strong frozen open-vocab backbone (EVA-CLIP 82.0 zero-shot ImageNet top-1, 2303.15389) supplies
  the similarity scores; microCLIP-style label-free sharpening (2510.02270) can tighten fine-grained cues
  (adaptation, not pure zero-shot).

## 2. MANDATORY calibration-before-fusion (the key constraint)
Raw zero-shot softmax/cosine scores MUST NOT be fused raw. Required conditioning before the P14 fuser:
- Temperature scaling — one learned temperature PER BACKBONE generalizes across prompt AND dataset
  (2303.12748) → cheap offline calibration that transfers.
- Uncertainty reparameterization (Dirichlet) for usable uncertainty under perturbation (2512.12997).
- Feed the fuser the calibrated score PLUS its entropy / probability-difference (the DynaPrompt selection
  signals, 2501.16404), never raw softmax.
- De-rate any externally reported zero-shot number for likely benchmark LEAKAGE (TruZe shows up to 8.9%
  inflation, 2107.13029; AI4Fire leakage, 2610.10946).
This closes the loop with fusion_design.md §1.2 (common calibrated scale before fusion).

## 3. Domain-shift & degradation handling
- Per-camera TEST-TIME PROMPT adaptation without labels: DynaPrompt (2501.16404), MetaTPT (2512.12268),
  black-box TTA BETA (+3.4% ImageNet-C, 2604.15609) — targets the new-site/weather/lens shift that most
  threatens a zero-shot layer.
- Guard the known FAILURE MODES: fine-grained confusion (2404.03539), prompt collapse (2501.16404),
  compression fragility (2311.14029), adversarial over-confidence (2512.12997), distance-based "consistent
  anomaly" bias from recurring nuisances like persistent haze/sun-glare (2512.02520), OOD tail instability
  (2607.07951).
- GROUNDED-REFERENCE trick (reusable): give the model a smoke-free reference frame from the SAME camera —
  AI4Fire found grounding helps most when the added input carries the answer (2610.10946).

## 4. Evaluation
Evaluate the zero-shot channel on an INTERNAL held-out hazard set (NOT the leaky public fire sets); score with
proper scoring rules + calibration (per P14 discipline); report its standalone weakness honestly and its
MARGINAL contribution inside the fusion ablation (ablation_plan.md: with vs without the zero-shot input).

## 5. Honesty & gaps
On-paper only. No clean, permissively-licensed CCTV-style zero-shot FIRE/SMOKE benchmark found — both fire sets
(WildFireCan-MMD, AI4Fire) carry documented leakage/label flaws → curate an internal held-out set. Zero-shot
is a COMPLEMENT at low fused weight; the honest baseline remains the trained P8 detector.
