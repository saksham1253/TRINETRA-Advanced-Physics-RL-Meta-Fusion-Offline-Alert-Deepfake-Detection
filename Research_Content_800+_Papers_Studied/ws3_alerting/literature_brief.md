# WS3 — ALERTING / DISSEMINATION — literature brief (P4, 2026-10-07)
Owner phases: P3/P13/P15. Scope: alarm stack, CAP/SACHET, backhaul resilience, human compliance.

## Most relevant papers
- **2608.30205** exPreCast-ENS (residual-diffusion probabilistic ensemble) — PROVIDES the predictive
  distribution for the WHEN→alarm stack.
- **2609.14821** Decision-Oriented UQ — CALIBRATE that distribution to the alarm action loss (action-loss
  coverage ≠ predictive coverage: 84.9% vs 90%). Body number (regret −23.4%) is FT-PARTIAL — re-verify vs PDF.
- **2606.21773** DFL review — "better prediction ≠ better decision"; the cost-loss threshold (Bayes p*=0.0476).
- **2109.07745** Kincade wildfire: 46% evacuation compliance in warning/order zones; >50% self+shadow evacuees
  → the one hard human-response number we have (C-12, THIN).
- Backhaul resilience: DTN store-carry-forward (Spray-and-Wait) when a storm cuts the gateway (FM-11).

## Key claims → references
- Alarm stack = ensemble forecast → decision/action-loss calibration → cost-loss threshold. → DC-03 (C-04).
- Reward must cost FA > a flat penalty (cry-wolf erodes future compliance). → DC-18 (THIN; FM-09).
- Media/crowd signals are low-trust advisory only. → DC-04.

## Open questions
- Human-compliance model for the RL reward is thinly sourced on arXiv → source NHESS/IJDRR (non-arXiv) in P13/P15.
- CAP/SACHET integration details (signing, multi-channel) — P13.
- Backhaul-down alert reach under real storm topology — P13.
