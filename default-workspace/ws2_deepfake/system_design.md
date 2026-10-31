# ws2_deepfake/system_design.md — trust & corroboration pipeline, decision policy, cost matrix (P11, WS2)

Phase P11 · RESEARCH-ONLY. Designs how the system decides how much to trust social-media-sourced disaster
information. Every component is EVIDENCE-GATED (citations in ws2_deepfake/literature_map.md; reading subagent
8c3e59bb). No own-system performance claim (Rule 16). Rule 19: outputs are ADVISORY corroboration/credibility
signals feeding human-in-the-loop; they NEVER autonomously trigger evacuation. Privacy (§ethics): no
profiling of individuals/accounts; account signals only aggregate, within the anomaly-layer privacy rules.

## 1. Design principle: media forensics is ONE weak signal
A single deepfake-detector score is UNRELIABLE in deployment (cross-generator collapse + platform-degradation
collapse + removable watermarks — SOTA scan §0). The trust decision is therefore a MULTI-SIGNAL FUSION with
human-in-the-loop, not a classifier verdict.

## 2. Pipeline stages (a social-media disaster item → a trust decision)
INPUT: a social post (image/video/audio/text + caption + metadata + account/time/place if available).
1. INTAKE & NORMALIZATION: hash the media (perceptual + cryptographic); record platform, timestamp, claimed
   location; language ID (incl. Indian languages + code-mixed).
2. OUT-OF-CONTEXT / RECYCLED CHECK (HIGH priority — the dominant real threat): reverse-image / near-
   duplicate / perceptual-hash lookup against prior media; temporal + geolocation consistency; shadow/sun-
   angle/weather consistency; EXIF (with its limits); caption-vs-image consistency; video keyframe matching.
   OUTPUT: "previously seen / out-of-context" evidence.
3. PROVENANCE CHECK: C2PA/content-credential verification if present. Present+valid = POSITIVE provenance;
   ABSENT = NO conclusion (not evidence of fakery). Watermark check similarly positive-only.
4. SYNTHETIC-MEDIA FORENSICS: image/video/audio detectors (frequency + foundation-model-feature/CLIP
   universal + temporal/physiological), run under the degradation-aware model from the robustness plan.
   OUTPUT: a CALIBRATED synthetic-likelihood with uncertainty (NOT a binary).
5. PHYSICS-PLAUSIBILITY (NOVEL, UNVALIDATED — ws2_deepfake/physics_plausibility.md): optional consistency of
   fire growth-rate/flicker-band/plume-rise/smoke-opacity-vs-distance vs P7 physics envelopes. Used ONLY as a
   weak flagged-experimental signal, never asserted (Rule 21).
6. SOURCE CREDIBILITY + AGGREGATE NETWORK SIGNALS: account age/history credibility (aggregate, privacy-safe),
   coordinated-amplification burst signal from the anomaly layer (aggregate only, no individual profiling).
7. MULTI-SOURCE CORROBORATION: does the claim agree with CCTV detection (P8), IoT sensor alarms (P6/P9),
   satellite active-fire (e.g. VIIRS/MODIS), and weather? Corroboration is the STRONGEST trust signal for a
   life-safety call.
8. FUSION + DECISION POLICY (§4): combine calibrated signals → a trust tier + action.
9. HUMAN-IN-THE-LOOP: low-confidence / high-stakes items routed to a human verifier with all evidence; the
   system never issues a public alert from social media alone.

## 3. Trust tiers (advisory)
- CORROBORATED: independent non-social evidence (CCTV/IoT/satellite) agrees → high trust → feed fusion (P14)
  / alert pipeline (P12) as a corroborating input (still human-gated for public alerts).
- PLAUSIBLE-UNCORROBORATED: no contradiction, no independent confirmation → human review, monitor for
  corroboration; no alert.
- SUSPECT: out-of-context hit OR high calibrated synthetic-likelihood OR physics-implausible → flag, do not
  propagate, human review.
- INSUFFICIENT: too degraded/ambiguous to score → abstain, human review.

## 4. Decision policy + explicit cost matrix
Let the two error types be: FALSE POSITIVE (treat FAKE/irrelevant media as a real local hazard → false
alarm, resource waste, alert fatigue, erosion of trust) and FALSE NEGATIVE (treat a REAL hazard report as
fake/irrelevant → missed/ delayed warning — the life-safety-critical error). Define costs C_FP, C_FN.
- Bayes-optimal decision: raise/trust iff P(real-hazard | evidence) · C_FN > (1 − P) · C_FP, i.e. decide
  "trust/act" when posterior odds > C_FP / C_FN. Since C_FN >> C_FP for life safety, the THRESHOLD on
  P(real) is LOW — BUT the action for a low-confidence social item is "escalate to human + seek
  corroboration", NOT "issue public alert" (Rule 19 keeps the autonomous-alert threshold effectively
  unreachable from social media alone).
- SHOW the threshold movement analytically: optimal decision threshold t* = C_FP / (C_FP + C_FN). As C_FN/C_FP
  grows, t* → 0 (more willing to escalate for review); the cost matrix is a config parameter owned with the
  state DMA, documented, not hard-coded to a guess.
- Calibration REQUIRED (so the posterior is meaningful): conformal/temperature calibration (reuse P10
  calibration recipes), reported ECE; uncalibrated scores make the cost-matrix math invalid.

## 5. Interfaces
→ P14 fusion (as a corroboration input with uncertainty + source tag); → P12 alerting (corroborated social
evidence can RAISE a tier but never auto-issue; human-in-the-loop queue); → P13 dashboard (evidence trail,
trust tier, review queue); ← P9/P10 anomaly layer (aggregate burst signal, privacy-safe); ← P8/P6/satellite/
weather (corroboration sources).

## 6. Honesty / limits
No detector built or measured. All component choices cite literature. Media forensics treated as weak
evidence by design. Physics-plausibility is explicitly UNVALIDATED. Indian-language/code-mixed claim
verification is an acknowledged gap. The system cannot reliably authenticate a lone degraded social clip —
it manages that uncertainty via corroboration + human review, and says so.
