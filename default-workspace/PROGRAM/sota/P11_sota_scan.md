# PROGRAM/sota/P11_sota_scan.md — synthetic-media detection & misinformation SOTA scan (WS2)

Phase P11 · RESEARCH-ONLY. SOTA for deciding how much to trust SOCIAL-MEDIA-sourced disaster information,
framed around the two protocols that actually matter for deployment — CROSS-GENERATOR generalization and
DEGRADED-MEDIA (platform recompression) robustness — plus the honest limits of provenance/watermarking. No
own-system performance claim (Rule 16). Specific IDs/numbers to be filled from ws2_deepfake/literature_map.md
(reading subagent 8c3e59bb running); this is the framing + known-SOTA skeleton.

## 0. The governing reality (most important findings)
1. CROSS-GENERATOR COLLAPSE: detectors trained on one generator family (e.g. GANs) typically degrade sharply
   on unseen generators (e.g. diffusion), and vice-versa. In-distribution accuracy is near-saturated and
   MISLEADING; the real metric is cross-generator / open-set.
2. DEGRADATION COLLAPSE: social platforms recompress/resize/crop/screenshot/re-upload media, destroying the
   subtle frequency/spectral artifacts many detectors rely on. A detector strong on pristine data can be
   near-useless on a WhatsApp-forwarded JPEG.
3. PROVENANCE IS NOT DETECTION: C2PA/content-credentials prove ORIGIN when present and intact, but absence of
   a credential is NOT evidence of fakery, and metadata is routinely stripped by platforms; invisible
   watermarks are removable/forgeable by several published attacks. Provenance HELPS but cannot be the sole
   trust signal.
4. CORROBORATION BEATS A SINGLE DETECTOR: for a life-safety system, the robust design treats any single
   media-forensics score as weak evidence and resolves trust by MULTI-SOURCE corroboration (social report vs
   CCTV vs IoT vs satellite fire vs weather) + source credibility + human-in-the-loop.

## 1. Image synthetic-media detection
- Families: spatial-CNN artifact detectors; FREQUENCY/spectral (GAN upsampling fingerprints, diffusion
  spectral traces); FOUNDATION-MODEL-FEATURE / CLIP universal detectors (often best cross-generator);
  reconstruction-error (diffusion inversion) detectors; patch/local-artifact.
- Known: CLIP-feature + simple classifier generalizes better across generators than bespoke CNNs (to
  confirm from quota); frequency detectors are fragile to recompression. Diffusion images lack the classic
  GAN grid fingerprint → older detectors miss them.

## 2. Video / face-swap detection
- Families: spatial per-frame + temporal (optical-flow, 3D-CNN, transformer); physiological (rPPG/
  heartbeat, blink); identity-aware; spatio-temporal inconsistency. Benchmarks: FaceForensics++, DFDC,
  Celeb-DF, WildDeepfake, DF40. Cross-dataset generalization is the known weak point.

## 3. Audio / speech deepfake
- Families: spectrogram-CNN, raw-waveform (RawNet), SSL front-ends (wav2vec2/WavLM) + classifier; ASVspoof
  benchmarks. Relevant where disaster reports include voice notes (common on WhatsApp in India).

## 4. Frequency/spectral + foundation-model universal detectors
- The cross-generator battleground. CLIP/foundation features + light head often the most generalizable;
  frequency cues the most degradation-fragile. Both to be weighed under BOTH protocols.

## 5. Cross-generator generalization + continual / test-time adaptation
- Strategies: data diversity (many generators), augmentation (incl. compression aug), reconstruction/
  one-class on "real" only, test-time adaptation, continual learning (with forgetting risk). Evidence to be
  compiled; open-set recognition framing is the honest one (new generators appear constantly).

## 6. Provenance / watermarking (C2PA, invisible watermarks) + attacks
- C2PA/content credentials: cryptographically signed provenance manifests; strong WHEN present/intact; broken
  by metadata stripping, screenshots, re-encoding, and non-adoption. Invisible watermarks (for AI outputs):
  several published REMOVAL and FORGERY/spoofing attacks (regeneration, diffusion purification, collusion).
  → use as POSITIVE evidence of provenance, never as a fakery test; "no watermark" ≠ "real".

## 7. Out-of-context / recycled media + corroboration
- The MOST COMMON real-world disaster misinformation is REAL media reused out of context (old/other-place
  fire), not deepfakes. Tools: reverse image search, near-duplicate / perceptual hashing, temporal &
  geolocation consistency, shadow/sun-angle/weather consistency, EXIF (and its limits), caption-vs-image
  consistency, keyframe matching. This family is HIGH PRIORITY for our use case.

## 8. Platform degradation + adversarial anti-forensics
- Degradation: document verified platform recompression chains (WhatsApp/X/Facebook/Instagram/Telegram);
  specify a degradation protocol for robustness curves. Adversarial: perturbations, anti-forensics,
  laundering through compression/regeneration defeat many detectors → paper red-team required.

## 9. Crisis informatics + multilingual/Indian-language + credibility + calibration/fairness
- Crisis-informatics: multi-source corroboration, rumor/credibility, burst detection (aggregate, privacy-
  safe). Indian context: multilingual + code-mixed (Hindi/English + regional) claim verification is
  under-served — flag as a gap. Calibration + fairness of detectors across demographics/languages required
  (TPR at fixed low FPR, ECE).

## 10. Realistic bar for our system
- Treat media forensics as ONE weak signal; headline design = MULTI-SOURCE CORROBORATION + source
  credibility + human-in-the-loop with an explicit cost matrix (false alarm vs missed real event).
- Prioritize OUT-OF-CONTEXT detection (reverse-search/perceptual-hash/geo-temporal consistency) — the
  dominant real threat — over chasing SOTA deepfake accuracy.
- Evaluate ONLY under cross-generator + degradation + adversarial protocols with calibration; pristine
  in-distribution accuracy is not reported as a headline.
- Physics-plausibility checks (fire growth/flicker/plume/opacity from P7 models) are a NOVEL, UNVALIDATED
  hypothesis → documented with a study design, never asserted as working (Rule 16, Rule 21).
- Privacy: account/network signals used only within the anomaly-layer privacy rules (aggregate, no profiling
  of individuals).
