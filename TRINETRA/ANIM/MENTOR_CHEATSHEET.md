# Mentor cheat sheet (one page)

**Click order in Explore Mode (E):** Surveys → Compare (14 failure patterns) → Pipeline (click Meta-fusion, then Geo physics gate) →
Parameter Lab (drag the threshold to p* ≈ 0.048 and watch false alarms hit 100%) → Fusion Lab (move the outlier, untick it) →
Scenarios (steam vs real fire vs fake) → Results → Mentor.

## Eight hard questions, honest answers
1. **Why physics?** Zero labels on day one: AUC 0.758 on 184 real landslides; explains why; can veto impossible alarms; each model has a validity regime.
2. **Why zero-shot?** Add a hazard by writing a sentence. Measured AUC 0.889, but 80% false alarms on candles and 62% on weather, so NOT admitted; stays a low-trust helper (cap 0.5).
3. **How does fusion work?** w = r·c·e^(−u/τ), FM-1 weighted mean, U* adds disagreement; bounded, missing expert ⇒ weight 0. Worked example: 0.6335 → RED, U* 0.2465.
4. **Leakage?** Group / spatial-block splits, dedupe across datasets, held-out sets from other sources (DeepFire n 1,023; Bolivia floods).
5. **Why small, older datasets?** Free, licensed, verifiable in 36 h. We validate the protocol, not a benchmark score.
6. **What is not validated?** Fire CNN, media and EO numbers (pending), landslide meta-fusion (pending), field trial, cyclone (spec only), Class C terms (OFF).
7. **How is it different?** Typical: one detector + fixed threshold. TRINETRA: experts + physics consistency + calibrated uncertainty + cost tiers + human gate + offline path. Chips say built vs measured.
8. **More time?** Matched-protocol benchmarks (C4), SDMA shadow pilot, cyclone physics, IMERG 0.1° rain, Indian InSAR.

## Do not claim
"best", "first", "solves", "state of the art", "never done before" (no C4 result exists) · that the film runs the trained models live
(fire, steam and fake scenes are SIMULATED REPLAY) · any time-to-detection figure · that TRINETRA replaces certified alarms or IMD / NDMA.
