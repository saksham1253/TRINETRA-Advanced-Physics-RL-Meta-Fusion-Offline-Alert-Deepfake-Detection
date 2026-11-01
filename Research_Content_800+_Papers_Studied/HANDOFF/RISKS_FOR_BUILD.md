# RISKS FOR BUILD (MASTER_PROMPT §0.4A)
# Risks the build must plan around, drawn from the failure-mode catalogue + environment.
# Full program risk register: PROGRAM/RISK_REGISTER.md.

| ID | Risk to the build | Source | Impact | Mitigation to bake in |
|----|-------------------|--------|--------|-----------------------|
| RB-01 | Spatial leakage inflates every metric | FM-01 / 2608.12422 | false confidence, unsafe deploy | tile-withheld spatial-CV harness FIRST; GB/tree/persistence baselines gate all claims |
| RB-02 | Abstract-only evidence not build-certified | corpus all ABS | methods unverified | full-text + reproduce baseline before coding each method |
| RB-03 | Kaggle compute cap (25-30 GPU-h/wk, ≥15% reserve) | master constraint | plan may not fit | per-WS GPU-h budget in KAGGLE_BUDGET.md; distill/subset fallbacks |
| RB-04 | ₹2000/node BOM unverified (supplier 403) | FM / OQ-05 | hardware infeasible | hard-verify ≥2 live listings in P6 before any build commitment |
| RB-05 | Safety shield may be unrealizable | FM-05 / 2507.23603 | shield can't be synthesized | realizability check as a build acceptance gate |
| RB-06 | Proxy credential leak in existing infra | FM-16 / Bug #12 | security breach | remove/replace proxy; security review before deployment |
| RB-07 | Life-safety: never replace certified systems | Rule 19 | legal/ethical/safety | human-in-loop on every alert; complement SACHET/CAP, not replace |
| RB-08 | Augmentation ≠ robustness: FT for one corruption doesn't transfer | 2606.07593 (P2) | false weather-robustness claim | test fog/rain/night/low-light EACH explicitly; never claim general robustness from one augmentation |
| RB-09 | Social-media recall collapses during real events (networks down, attention elsewhere) | 2511.21364 (P2) | crowd signal fails when needed most | crowd layer = LOW-WEIGHT corroboration only, never a standalone trigger (Rule 19) |
| RB-10 | VLM text-generation verification is prompt-fragile (−1.36..+1.55 AUC) | 2609.07455 (P2) | brittle false-alarm filter | use VLM LOGIT interface (parser-free), not prompt text-gen; keep VLM at gateway tier not edge |
| RB-11 | Seasonal-label leakage: models learn the calendar not the hazard | 2605.20167 (P2) | inflated metrics, misses off-season | deseasonalize inputs (monthly climatological anomaly); DISCLOSE feature–label corr before/after |
| RB-12 | Nowcast skill ceiling ~90 min; longer lead needs memory | 2609.17175 (P2) | over-promised lead time | lean on upstream/soil-moisture/InSAR memory for lead; report CRPS+rank-hist, honest horizon |
| RB-13 | RL conclusions can be seed-luck / spec artefacts; attribution reverses 30→100 seeds | 2610.03369 (P3) | wrong architecture credited; unsafe policy ships | ≥100 seeds; report tail-risk + across-seed dispersion not just mean; ablate training-spec (exploration/reward) before crediting any architecture; always vs fixed-threshold + persistence baselines |
| RB-14 | Foundation/large models reconstruct ANOMALIES too well → anomaly-score collapse | FM-23 / 2610.06453 (P3) | missed detections (silent) | constrain forecaster to normal subspace; keep model-free detector + physics gate; monitor residual-variance shrink as a red flag |
| RB-15 | Physics FoS error amplifies into failure-probability error (3% FoS → up to 2x prob; methods disagree 2.6–8.3x) | FM-24 / 2610.04828 (P3) | miscalibrated risk if FoS treated as probability | use FoS as a hard GATE/threshold, NOT a calibrated probability; report method-spread; expert review (Rule 19) |
| RB-16 | PWS / cell-broadcast alerts are spoofable (unauthenticated SIBs); provenance soft-bindings false-fire + are platform-fragile | 2604.24404 / 2610.04151 (P3) | spoofed or wrongly-trusted alerts | sign CAP end-to-end; HMAC-authenticate LoRa/ESP-NOW mesh; multi-channel corroborate before 'authoritative'; provenance = confidence modifier, never sole gate |
| RB-17 | Mesh/LoRa links degrade on terrain slopes / no-LOS (worse than urban benchmarks) | 2507.07841 (P3) | alerts/telemetry dropped when most needed | budget link margin + multi-hop; two-tier comms with LoRa always-on alert tier the alert survives on alone; field link-budget test before deploy |
| RB-18 | Alarm decision is manipulable via untrusted STATE; confidence gate alone insufficient (attacks flood human review + some flips keep high confidence) | 2609.31142 (P3) | spoofed/injected inputs flip alert; gate escaped or overwhelmed | treat all crowd/CCTV/mesh inputs as untrusted argued input; stress-test WS5 adversarially; report gate escape-rate + review-load; defense-in-depth (physics gate + corroboration + hard shield), never gate-only |
