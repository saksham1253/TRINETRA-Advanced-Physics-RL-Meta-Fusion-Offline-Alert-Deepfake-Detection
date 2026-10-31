# ws8_anomaly/spec/family_c_ood_health.md — BUILD SPEC: OOD / model-health / drift (P10, WS8b)

PRIORITY 1. RESEARCH-ONLY build spec. External numbers SOURCE-REPORTED (Rule 16). Precise defaults tagged
[recipe-cite — P10 reader] (ccaba769) pending.

## 1. Method and why (evidence)
Job: stop the vision (P8) and fusion (P14) models from making CONFIDENT WRONG predictions on inputs unlike
training (new camera/site/weather/lens), and raise a label-free drift/health signal. Evidence: a cheap
wrapper over internal reps gives a label-free drift signal + repair trigger (RCV 2608.14089); TS-OOD ≠
vision-OOD so use TS-specific OOD for sensor streams (prior-phase 2502.15901); structure-guided TTA beats
entropy-min TTA on new installs (ANT 2608.20557). → feature-space OOD scoring + abstention, NOT retraining
in the field by default.

## 2. Inputs and outputs
INPUT: penultimate feature vectors of the P8 detector / P14 fusion head (per frame or per decision) + sensor-
stream embeddings. OUTPUT: OOD score, an ABSTAIN / "needs human review" gate decision, a drift alarm, and a
confidence down-weighting signal passed to fusion (P14).

## 3. Data + splits
In-distribution = training cameras/sites/sensors; OOD held-out = unseen camera/site/weather/season (grouped
splits, evaluation_protocol §3). No OOD-set tuning (that is a named pitfall). Shortcut audit via explicit OOD
negatives (2608.20663).

## 4. Normal-reference policy
Fit the in-distribution feature density (mean/covariance for Mahalanobis; stored exemplars for kNN) on train
features ONLY; refresh when the deployment distribution legitimately changes (new verified site), logged.

## 5. Features / architecture / defaults
- VISION OOD: Mahalanobis distance on penultimate features (per-class means + shared covariance) and/or kNN
  distance to k nearest train features (k default 50 — [recipe-cite]); energy score as a secondary. These
  are post-hoc, train-free beyond fitting statistics.
- SENSOR-STREAM OOD: TS-specific OOD (not a lifted vision detector, 2502.15901); reuse the family-B density/
  reconstruction error as an OOD proxy.
- DRIFT: ADWIN / Page-Hinkley on the score/feature stream (window + δ defaults [recipe-cite]); RCV-style
  label-free correctness estimate (2608.14089) as the trigger for human review.

## 6. Training/thresholding/calibration
Post-hoc: fit statistics on train features; set the OOD threshold on a validation split (or a held-out OOD
proxy that is NOT the test OOD) for a target abstain-rate; calibrate scores (temperature scaling on the base
classifier + ECE check). Abstain when OOD score > threshold.

## 7. Metrics + procedure
OOD AUROC (near- vs far-OOD reported separately — a named pitfall is conflating them), abstention quality
(risk-coverage curve), effect on in-distribution accuracy (must not degrade), drift-detection delay. ≥5
seeds + CIs. Backbone-sensitivity reported (OOD results depend on backbone).

## 8. Simple baselines first
Max-softmax probability baseline + temperature scaling. Mahalanobis/kNN/energy must beat max-softmax to be
shipped.

## 9. Ablations / stress tests
Backbone choice; near vs far OOD; feature layer; with/without temperature scaling; weather/lighting/season
shifts; new-camera transfer; adversarial/tamper inputs (ties family-A + P8 tamper).

## 10. Acceptance (process targets)
Reliably abstains on cross-site/weather OOD without harming in-distribution accuracy; beats max-softmax;
drift alarm fires within target delay on a staged distribution shift. Rule 16: targets, not results.

## 11. Pitfalls
Near/far-OOD conflation; OOD-set tuning; backbone sensitivity; shortcut learning invisible in-distribution
(2608.20663); over-abstention (alert fatigue) → governed by abstain-rate budget.

## 12. GPU hours
≈0.5 Kaggle GPU-h (features already produced by P8/P14); post-hoc fitting is cheap. ESTIMATE.

## 13. Verification checklist
[ ] fit on train features only  [ ] threshold on validation/held-out proxy, never test OOD  [ ] near/far OOD
separated  [ ] in-dist accuracy unharmed  [ ] beats max-softmax  [ ] abstain-rate budget set with P12
[ ] drift delay measured  [ ] defaults cited.
