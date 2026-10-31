# ws6_robustness/defense_and_monitoring_plan.md — defenses, monitoring & Rule-19 gating (P16, WS6)

Phase P16 · RESEARCH-ONLY, on-paper. Nothing built/trained (Rule 16). Maps each attack class in
robustness_catalogue.md to a defense + a runtime monitor, with Rule 19 gating. All numbers SOURCE-REPORTED.

## 1. Defenses (prioritized by generalization + reported tradeoff)
MOST TRANSFERABLE — cross-sensor redundancy & residual-based anomaly detection (least clean-accuracy cost):
- Cross-modal consistency + fault detection/identification/isolation (FDII) to catch fake/removed/adversarial
  signals (2302.07341); chi-squared residual checks between authenticated signals (2307.04692); inertial
  dead-reckoning cross-check vs LiDAR spoofing (2603.11365). ⇒ a fire event must be CORROBORATED across
  independent sensors/cameras before alert escalation (ties P14 fusion + P12 tiering).
VISION HARDENING (benchmark-local gains, may not transfer — use with caution):
- Adversarial training incl. meta-AT for universal patches, low extra compute (2101.11453); AT-for-GANs
  (2003.01279) — usually trades clean accuracy.
- Corruption augmentation (2206.13405: tradeoff not inherent) BUT gains don't transfer to dissimilar
  corruptions (2102.11273); must validate on held-out corruptions + the VIDEO pipeline (2110.06513).
CERTIFIED (guarantee but small-scale only — report as a lower bound, not coverage):
- Certified ensembles weighting base models to maximize a robustness certificate, better clean accuracy than
  naive averaging (RobBoost 1910.14655); neural-symbolic verification toward realistic shifts (2206.03669).
SUPPLY CHAIN:
- Provenance control on models + training data; vet any third-party/pretrained model through a standardized
  backdoor benchmark before it enters the chain (2206.12654/2407.19845); beware stealthy under-confidence
  backdoors that hide below confidence-threshold alert logic (2202.11203).
WIRELESS:
- Jamming-aware routing + spread-spectrum (1411.3736); jamming detection; WIRED/redundant alert paths because
  minimal attacker effort collapses a link (1509.09222); signed + replay-protected alerts + cross-cell
  verification vs spoofed cell broadcast (2604.24404, ties P12).
DETECTOR EVASION:
- Never trust a single evasion-detector threshold (90% evasion, brittle JPEG cliff, 2607.25842); treat media
  forensics as ONE weak signal under multi-source corroboration (ties P11); continuous RED-TEAMING over
  one-time hardening (2003.01279).

## 2. Runtime monitoring (drift / failure prediction)
- UNCERTAINTY monitoring is mandatory: deterministic confidence stays high while accuracy collapses under
  shift — monitor MC-dropout entropy (flagged all shifts, 2610.08810); alarm on confident-but-OOD.
- Concept-drift detection: hierarchical hypothesis testing with Type-I/II analysis + detection-delay metrics
  (1707.07821); lightweight edge drift adaptation for IoT streams (OASW/LightGBM, 2104.10529) — BUT its
  "no-human-intervention" auto-adaptation MUST be gated by Rule 19 (feed advisories, never autonomous
  retrain-and-act); drift-triggered recalibration for structural/graph models (2404.02572).
- Residual / chi-squared / FDII monitors double as spoofing+failure predictors (2307.04692, 2302.07341).
- MONITOR THE MONITOR: evasion-signal detectors have brittle operating points (JPEG-Q70 cliff) — alarm on
  signal collapse (2607.25842).

## 3. Rule 19 gating (binding)
- No single model/channel auto-triggers a public alert; corroboration + human review required (ties P11/P12).
- Network-exposed endpoints (dashboard, node, mesh) REQUIRE auth (WPA2 SoftAP + signed, replay-protected
  messages — ties P13 FIRMWARE_SPEC, P12 threat_model).
- Auto-adaptation (drift retraining) produces ADVISORIES for human approval, never autonomous action.
- Fail-safe: a degraded/attacked component degrades to "uncertain/offline", NEVER to a false "all clear".

## 4. Honesty
Plan only; nothing built. Cross-sensor redundancy + residual detection generalize best at least accuracy cost;
single-model hardening gives benchmark-local gains that may not transfer. All source-reported on non-fire
benchmarks → re-test.
