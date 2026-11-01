# ws2_deepfake/robustness_plan.md — platform-degradation + adversarial robustness plan (P11, WS2)

Phase P11 · RESEARCH-ONLY. MASTER_PROMPT P11 tasks 4 + 6. Specifies the degradation protocol for later
robustness curves and the adversarial/anti-forensics red-team. Verified platform behaviour to be cited from
ws2_deepfake/literature_map.md (reading subagent 8c3e59bb) + vendor docs; where behaviour is not verified it
is marked UNVERIFIED. No own-system claim (Rule 16).

## 1. Platform-degradation protocol (for robustness curves)
Simulate the real forward-chain a disaster clip survives before reaching us:
- RECOMPRESSION: JPEG/HEIF re-encode at a sweep of quality factors; video re-encode (H.264/H.265) at a sweep
  of bitrates/CRF; multiple re-encode GENERATIONS (re-uploads).
- RESIZE/CROP: platform max-dimension downscale; aspect-crop; letterbox.
- SCREENSHOT: screen-capture of a displayed post (resampling + UI chrome).
- FILTERS/OVERLAYS: text/sticker overlays, color filters.
- METADATA STRIP: EXIF/C2PA removal (platforms routinely strip) — tests the provenance stage's failure mode.
- CHAINS: compose the above into platform-specific chains (WhatsApp / X / Facebook / Instagram / Telegram),
  each documented as VERIFIED (with source) or UNVERIFIED (to confirm at build time).
Robustness curve = metric (TPR@lowFPR, AUC) vs degradation level/generation, per detector.

## 2. Adversarial / anti-forensics red-team (on paper)
- Perturbation attacks (adversarial noise on the detector).
- Anti-forensics: artifact removal, spectral flattening, blur/noise injection.
- LAUNDERING: re-encode / re-upload / regenerate (diffusion purification) to erase synthetic traces.
- WATERMARK attacks: removal, forgery/spoofing, collusion (provenance stage threat).
- Each attack mapped to the pipeline stage it defeats + the fallback (corroboration + human review).

## 3. Robust recipes to evaluate (from quota)
Compression-augmented training; foundation-model/CLIP features (often more degradation-robust than frequency
cues); test-time adaptation; ensembling across cue types; one-class/reconstruction on real only. Each to be
tested UNDER the degradation + adversarial protocols, not pristine data.

## 4. Honest expectation
Many detectors degrade sharply under recompression/laundering and adversarial attack (SOTA scan §0, §8). The
plan assumes media forensics is BRITTLE and designs the system to lean on corroboration + human-in-the-loop
rather than detector robustness. Robustness numbers are TARGETS to measure in the build, not results.

## 5. Carried to P16
All attacks + degradation failure modes enter the P16 robustness failure-mode catalogue.
