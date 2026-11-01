# PHASE_11_report — WS2 DEEPFAKE & MISINFORMATION RESEARCH & DESIGN (RESEARCH-ONLY)

Phase P11 (MASTER_PROMPT L558). Status: COMPLETE to gate (continuous mode — completion record, not a halt).
Nothing built/trained/measured; NO deceptive media created (Rule 16, §content-safety). Rule 19 human-in-the-
loop; Rule 21 novelty governs the physics-plausibility hypothesis.

## Objective
Design how the system decides how much to trust social-media-sourced disaster information, with cited
evidence for every component.

## What was produced
- PROGRAM/sota/P11_sota_scan.md — SOTA framed around cross-generator + degraded-media protocols + provenance
  limits + the realistic "forensics is one weak signal" bar.
- ws2_deepfake/system_design.md — the trust/corroboration pipeline (intake → out-of-context check →
  provenance → synthetic-media forensics → physics-plausibility(experimental) → source credibility/aggregate
  network → multi-source corroboration → fusion/decision → human-in-the-loop), trust tiers, and an EXPLICIT
  COST MATRIX with the analytic threshold t* = C_FP/(C_FP+C_FN) and its movement.
- ws2_deepfake/literature_map.md — 20 NEW primary arXiv (ABS) across image/video/audio/frequency-universal/
  provenance/out-of-context + 4 synthesis lists + the disaster/fire-imagery flag.
- ws2_deepfake/evaluation_protocol.md — pre-registered; headline = cross-generator + degraded + calibrated;
  TPR@lowFPR, cross-generator acc, robustness curves, ECE, fairness; point-adjust-style pristine-AUC demoted.
- ws2_deepfake/robustness_plan.md — platform-degradation protocol + adversarial/anti-forensics red-team.
- ws2_deepfake/physics_plausibility.md — NOVEL, UNVALIDATED-for-fire hypothesis + study design; PIVOT
  (2609.15562) cited as prior work for the general idea (generator-agnostic, modest accuracy).
- ws2_deepfake/experiment_plan.md — the 6 required build-phase experiments + compute estimates.
- DATASETS.md — D68-D88 [D] forensic datasets (incl. CCDF D77 ⚑); 20 [P11] ledger rows; Audit #18 PASS.

## Governing findings (source-reported, Rule 16)
- Against FRONTIER generators, SOTA detectors AND humans/MLLMs fall to ≈ chance (DF26 2609.07369; CCDF
  2610.07939 — 10 detectors unreliable on fabricated CCTV crime/accident footage; SLED-1400 2606.07613 —
  MLLM 5.9% detection on the best generator). ⇒ detection alone cannot be trusted; EXTERNAL CORROBORATION
  (CCTV/IoT/satellite/weather) is mandatory.
- Watermarks/C2PA are removable (blind image removal 94.8%/11 systems 2610.11290; 6 diffusion watermarks via
  latent-frequency 2610.02010; query-free audio 0.92-0.96 2609.34003) AND false-fire on clean media + are
  platform-bit-unstable (2610.04151). ⇒ provenance = positive-only evidence; absence ≠ fake; payload must be
  verified.
- What DOES generalize: frequency/steganalysis fingerprints + cross-domain alignment (MoDA 2610.11496, stable
  under attack), explicit physically-grounded features (2610.03380), agentic evidence reasoning (ATAR
  2609.39066), audio graph back-ends (DuRe-ST 2610.10121).
- Codec re-upload flips bona-fide audio → fake (2610.07216). Out-of-context recycled REAL media is the
  dominant disaster-misinfo pattern (WildFakeBench 2603.25423, MIC 2609.33441); OOC detectors risk leaning
  on text and ignoring the image (NepOOC 2608.19212).

## Honesty & limits (§0.5)
QUOTA: 20 primary (≥15 MET; the aspirational ~40 NOT reached under arXiv-throttle + no-web_search within the
bounded reader — stated plainly). ALL ABS (0 FT); IDs subagent-reported, not re-fetched (residual risk). NO
fire/wildfire-specific synthetic corpus exists (GAP); Indian-language/code-mixed claim-verification set is a
GAP to assemble. Regulatory specifics (who may originate cell broadcast; India NDMA/SACHET) deferred to the
P12 standards check. Physics-plausibility is UNVALIDATED for fire.

## Open actions carried
Assemble a fire-specific + Indian-language claim set; full-text reads for exact cross-generator/degradation
tables when building; confirm forensic-dataset licenses/EULAs; integrate C2PA payload-verification tooling;
run the pre-registered experiments.

## Gate
PROGRAM/gate_messages/PHASE_11_gate.md. Auto-proceeding to P12 (WS3 offline local-area alerting) — whose
reading quota (20 papers) was PIPELINED and is ALREADY in hand.
