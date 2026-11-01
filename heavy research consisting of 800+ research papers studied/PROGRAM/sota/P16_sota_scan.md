# PROGRAM/sota/P16_sota_scan.md — robustness & security SOTA scan (WS6)

Phase P16 · RESEARCH-ONLY. SOTA + targets. All numbers SOURCE-REPORTED (Rule 16) on vision/driving/IoT
benchmarks (NOT a fire system → transfer hypotheses); detail + IDs in ws6_robustness/literature_map.md P16
section. No own-system claim.

## 1. SOTA landscape
- ATTACKS: multi-patch joint location+perturbation (2411.16162); universal patches (2101.11453); FGSM+patch
  degrade strong CNNs (2307.02055); LiDAR injection vs SLAM (2603.11365); GPS spoofing (2307.04692); 1 jammer
  → 1%→80% outage (1509.09222); stealthy under-confidence backdoors (2202.11203); 90% detector-ensemble
  evasion (2607.25842).
- DEFENSES: cross-sensor redundancy + FDII (2302.07341), chi-squared residuals (2307.04692), inertial
  cross-check (2603.11365) — most transferable; meta-AT universal-patch (2101.11453); corruption augmentation
  w/ transfer caveat (2206.13405, 2102.11273); certified ensembles RobBoost (1910.14655); neural-symbolic
  verification (2206.03669); jamming-aware routing (1411.3736); standardized backdoor vetting (2206.12654/
  2407.19845).
- MONITORING: uncertainty (MC-dropout entropy flags shift while deterministic confidence stays high,
  2610.08810); hierarchical-hypothesis-testing drift (1707.07821); edge drift adaptation (2104.10529, gate by
  Rule 19); residual/FDII monitors (2307.04692, 2302.07341).
- EVALUATION: standardized matrices (BackdoorBench); clean+robust together (2206.13405, 1910.14655); worst-case
  not average evasion (2607.25842); held-out/video-specific corruption (2102.11273, 2110.06513); ODD coverage
  (2608.20864); spatial-block not random CV (2608.22293).

## 2. TARGETS section (process targets, NOT results, Rule 16)
- Cross-sensor corroboration before any alert escalation; no single channel auto-alerts.
- Authenticated endpoints; signed + replay-protected messages; fail-safe to "uncertain/offline".
- Uncertainty monitoring (entropy) as the alert gate, NOT deterministic confidence.
- Standardized attack×defense evaluation; clean+robust reported together; worst-case evasion; held-out
  corruption + video pipeline; ODD-coverage proof; spatial-block validation.
- Vet every imported model through a backdoor benchmark; continuous red-teaming over one-time hardening.

## 3. Honesty & gaps
All figures source-reported on non-fire benchmarks → re-test on P16 data. Cross-sensor redundancy generalizes
best; single-model hardening is benchmark-local. Certified robustness is a small-scale lower bound only.
