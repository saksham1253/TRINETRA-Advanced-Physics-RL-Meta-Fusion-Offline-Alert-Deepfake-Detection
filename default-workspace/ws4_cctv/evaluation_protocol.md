# ws4_cctv/evaluation_protocol.md — pre-registered evaluation protocol (P8)

Phase P8 · WS4 · RESEARCH-ONLY. Pre-registered BEFORE any model is built, so results cannot be shopped.
Nothing is measured here (Rule 16); this fixes HOW the later build is judged. Grounded in the SOTA scan,
the failure taxonomy, and alarm-practice realities.

## 1. Operating point (decided now, grounded in the literature + alarm practice)
- **Max tolerable false alarms:** target an operating point of **≤ ~1 false alarm per camera-day** for the
  autonomous stage (tunable per deployment; sources show false-alarm fatigue dominates adoption). Final
  value to be set with the operator; this is the pre-registered design target, not a measured result.
- **Max time-to-detection (TTD):** report TTD distribution; design target = detect established smoke/flame
  within a small number of confirmation windows (seconds to low minutes) — exact bound set per hazard with
  the operator. Early/small smoke reported separately (harder).
- **Cross-site acceptance:** performance must hold on HELD-OUT sites (see §2), not just random splits.

## 2. Leakage-safe splits (THE central protocol rule)
- Split by **GROUP = site, then camera, then video** — all frames of a video stay in ONE split; whole
  cameras/sites are held out for the cross-site test. NEVER random-frame split (near-duplicate leakage).
- Three tiers: (i) within-site (same cameras, disjoint videos), (ii) cross-camera (same site, unseen
  cameras), (iii) cross-site (unseen sites) — report all three; (iii) is the headline.
- Temporal: for a given camera, test videos are LATER in time than train where timestamps exist.

## 3. Metrics (beyond accuracy)
- **Time-to-detection** (median + distribution), per hazard and per difficulty (early/small vs established).
- **False alarms per camera-day** at the fixed operating point (on the nuisance test set, §failure_taxonomy).
- **Precision-Recall at the operating point** + PR-AUC; report at small-object scales explicitly.
- **Calibration:** reliability diagram + ECE (so the fused/alert layer can trust confidences).
- **Robustness curves:** metric vs JPEG/H.264 bitrate, vs resolution, vs night/IR.
- **Confidence intervals over SEEDS** (≥5 seeds) for every headline number; report CIs, not point values.
- Per-condition breakdown from the failure taxonomy (fog, steam, headlights, …).

## 4. Baselines & variants to compare (fair comparison)
- Reproduce published YOLO-family fire/smoke baselines FIRST (same splits) as the reference.
- Compare: (a) classical cues, (b) deep single-frame detector, (c) deep + temporal confirmation,
  (d) physics-informed variant (P7 features: flicker-band B-05, plume-growth, extinction/B-01 as priors or
  consistency checks), (e) cross-modal (camera + IoT) — all on the SAME leakage-safe splits + seeds.

## 5. Protocol pitfalls to avoid (from SOTA scan)
- No random-frame splits; no reporting mAP on the training distribution only; no single-site claims; no
  cherry-picked seed; no undisclosed test-time augmentation; report negatives/false-alarm rate, not just
  recall. State dataset licenses + provenance.

## 6. What a fair SOTA comparison needs (gap note)
Published numbers mostly use random splits → NOT directly comparable to our leakage-safe numbers. When we
cite SOTA we will say "source-reported under their (often leakage-prone) protocol" and re-run baselines
under THIS protocol for an apples-to-apples reference.

## 7. Pre-registered acceptance criteria (for the later build)
AC-1 cross-site PR-AUC reported with seed CIs (headline). AC-2 false-alarms/camera-day ≤ target at the
operating point on the nuisance set. AC-3 TTD distribution within target for established smoke; early/small
reported honestly even if worse. AC-4 calibration ECE reported. AC-5 robustness curves vs compression/res/
night. AC-6 physics-informed and cross-modal variants evaluated against the deep baseline on identical
splits. None of these is claimed met now; they are the bar.
