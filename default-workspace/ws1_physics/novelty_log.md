# ws1_physics/novelty_log.md — novelty & prior-art log (Rule 21)

Phase P7 · WS1a · RESEARCH-ONLY. Rule 21: before claiming any model/extension is new, search for prior art
and record what was found; prefer "this is an application/recombination of known results" over novelty
claims. HONEST TOOLING NOTE (§0.5): `web_search` had NO API key this entire phase; prior-art search was
done via the arXiv API (through web_fetch) + the P7 quota reading + canonical fire-science knowledge. This
is weaker than a full patent/Google-Scholar sweep → every "closest prior art" below is BEST-EFFORT, not
exhaustive, and none of our extensions is asserted as novel beyond "a modest, honest recombination."

## Position on novelty (summary)
NONE of the four Layer-2 extensions is claimed as a scientific invention. Each is an explicit RECOMBINATION
of established relations (per §P7's "prefer honest, modest extensions"), and each reduces to a published
parent. GMF-style composition, not invention (consistent with the program-wide stance).

## Per-extension prior-art record
### B-06 — sensor-response-corrected ceiling-jet/plume signal
- Query basis: RTI/plunge-test literature (Heskestad & Bill), Alpert ceiling jet, "detector response time",
  first-order sensor lag; arXiv "fire detection"+"physics-informed" (1 hit).
- Closest prior art: this IS the standard detector-actuation-time calculation (RTI + ceiling-jet) used in
  fire protection engineering (SFPE Handbook). NOVELTY: none in the physics; the only "new" packaging is
  exposing $(\tau,t_d)$ as explicit features/priors for an ML fusion layer and for cheap-sensor delta-feature
  timing. → classify as APPLICATION of established engineering, not new science.
### B-05 — aliasing-aware flicker band
- Query basis: Cetegen & Ahmed puffing frequency; Nyquist/aliasing (textbook); flame-flicker video detection.
- Closest prior art: flame-flicker video detection (10–15 Hz band) is a known classical CV cue; Nyquist
  aliasing is textbook. NOVELTY: none; the contribution is the explicit, honest coupling (fold the EF-08
  band through the camera sampling rate + an identifiability flag) rather than reporting a raw FFT peak.
  Swirl/wind band-broadening is documented ([13], arXiv:2202.06567). → RECOMBINATION of known results.
### B-01 — camera apparent flame height through smoke
- Query basis: Heskestad flame height; Beer–Lambert/Jin visibility ([7] arXiv:2404.11439); pinhole
  projection; vision-based fire-size estimation.
- Closest prior art: flame-height-from-video and Jin's-law visibility are both established; combining them
  with pinhole projection + uncertainty on $\dot Q,D$ is routine photogrammetry + fire science. NOVELTY:
  none claimed; honest composition with an explicit interval output. → RECOMBINATION.
### B-02 — dimensionless/prior plume-temperature estimator
- Query basis: McCaffrey $z/\dot Q^{2/5}$ collapse ([2]); Buckingham-Pi; Bayesian inversion of plume models.
- Closest prior art: the $\zeta=(z-z_0)/\dot Q^{2/5}$ collapse is exactly McCaffrey's normalization; Bayesian
  inversion of plume correlations is standard inverse-problem practice. NOVELTY: none; B-02 is an algebraic
  rearrangement of EF-03 (shown to be exact) + standard Bayesian treatment of unknown parameters.
  → RECOMBINATION / re-expression of a known result.

## Class-C items
- C-01 (level-set ∘ Rothermel) and C-02 (coupled forward camera model) are standard in the wildfire-
  modelling and fire-CFD literatures respectively (quota refs [14]–[24]); no novelty claimed; documentation-
  only.

## PINN-as-deployed-solver — deliberately NOT pursued (prior-art-informed)
The quota reading surfaced a well-documented PINN failure-mode literature (arXiv:2109.01050, 2001.04536,
2203.07404, 2602.19265, 2206.14862, 2412.05994, 2505.10949, 2501.17281, 2609.13171). Rather than claim a
novel fire-PINN, we cite these and SCOPE OUT live on-device PINNs (model_set_decision.md). Honest and
prior-art-aligned.

## Residual risk (honest)
Because web_search was unavailable, a non-arXiv paper or patent could pre-empt one of these recombinations;
since we claim NO novelty, this does not threaten correctness, only confirms the "not new" stance. A full
Scholar/patent sweep is an open action for the eventual write-up.
