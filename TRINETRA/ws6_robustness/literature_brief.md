# WS6 — ROBUSTNESS / CALIBRATION / UQ — literature brief (P4, 2026-10-07)
Owner phase: P14. Scope: spatial-CV, conformal prediction, calibration, missing-modality, drift/OOD, metrics.

## Most relevant papers
- **2610.08227** "How Many Independent Samples Does a Satellite Image Contain?" (TGRS 2026). Theorem: effective
  N = Θ(n²/r²); block holdout buffer g = Θ(r·log(n/δ)); random holdout underestimates CI width ∝ r.
  → spatial-CV is a PROVEN requirement, not a convention.
- **2512.14221** Mask-conditional valid weighted CP under general missingness — coverage conditional on WHICH
  sensors are present; narrower intervals keeping the guarantee.
- **2610.02777** PID-Expert online conformal aggregation — valid, efficient intervals under abrupt shift;
  q_{t+1}=Σ w^(m) q^(m); O(M) per round.
- **2609.14821** Decision-oriented UQ — action-loss coverage ≠ predictive coverage; utility-aware calibration.
- **2610.01384** CLEAR — post-hoc conflict-aware evidence scaling s(x)=exp(−δC(x)) for OOD/sparse overconfidence;
  temp-scaling does NOT fix proximity bias.
- **2510.22016** Total Classification Cost — cost-sensitive metric selection; metric value ∝ base rate.
- Missing-modality: **2605.06643** MMDG-Bench, **2609.15297** worst-case, **2607.24683** Co4Miss, **2608.15261** routing.
- OOD on time series: **2502.15901** TS-OOD (most vision OOD methods FAIL on time series), **2605.31155** hyperspherical TF.

## Key claims → references
- Spatial-CV with buffer ≥ r is the only admissible evaluation. → DC-01 (2610.08227).
- Primary metric = cost-loss Value Score / TCC. → DC-02 (2510.22016).
- Conformal = per-zone Mondrian × mask-conditional × action-loss × online. → DC-03 (three papers).
- Evaluate missing-modality worst-case (drop k most-informative). → DC-05.
- Post-hoc evidence scaling for sparse/OOD overconfidence. → DC-12 (2610.01384).

## Open questions
- Estimate r (spatial-correlation range) per Himalayan region to set the CV buffer.
- Cross-zone conformal with upstream→downstream coupling (G2/DC-19) — research item.
- Does the TS-OOD detector flag novel hazard regimes on OUR streams before a confident-wrong output? (FM-07).
