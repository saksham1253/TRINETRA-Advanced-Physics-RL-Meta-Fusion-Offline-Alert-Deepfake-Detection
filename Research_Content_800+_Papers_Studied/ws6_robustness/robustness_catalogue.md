# ws6_robustness/robustness_catalogue.md — system-wide attack & failure-mode catalogue (P16, WS6)

Phase P16 · RESEARCH-ONLY, on-paper. MASTER_PROMPT WS6. Nothing attacked/trained (Rule 16). Rule 19: this
catalogue exists so a HUMAN confirms before any auto-alert; network/sensor endpoints REQUIRE auth. All numbers
SOURCE-REPORTED on vision/driving/IoT benchmarks (NOT a fire system) → transfer hypotheses to re-test. Sources
in ws6_robustness/literature_map.md P16 section.

## 1. Attack & failure classes (per system component)
### CCTV / vision front-end (P8, P14Z)
- PHYSICAL-WORLD / UNIVERSAL / SPARSE PATCHES: strong pretrained CNNs degrade sharply under FGSM + patch
  (2307.02055); multi-patch attacks now jointly optimize location+perturbation (new SOTA, 2411.16162);
  universal patches meta-learnable (2101.11453). SEVERITY: HIGH. ⇒ human confirmation before auto-alert.
- NATURAL CORRUPTION / DISTRIBUTION SHIFT (weather/lighting/camera change) — NON-adversarial, happens without
  an attacker: augmentation gains fail to transfer to perceptually-dissimilar corruptions (2102.11273);
  image-level robustness does NOT certify the VIDEO pipeline (2110.06513); interpretable corruption metric
  MSCR shows the accuracy-vs-robustness tradeoff is not inherent (2206.13405). SEVERITY: HIGH.
- ZERO-SHOT OVER-CONFIDENCE under perturbation/compression (ties P14Z): 2512.12997, 2311.14029.

### Fusion inputs / sensors (P6/P13 IoT, P14 fusion)
- SENSOR SPOOFING: LiDAR injection compromises SLAM even in feature-rich scenes (2603.11365); civilian GPS
  unauthenticated/spoofable (2307.04692); cross-sensor attacks defeat single-modality perception (2302.07341).
  Maps to gas/flame/smoke sensor spoofing + a faulty node emitting false signals. SEVERITY: HIGH for fusion
  integrity.

### Wireless alerting path (P12/P13)
- JAMMING / INJECTION: 1 jammer per AP can push outage 1%→80% (1509.09222); hardware-in-the-loop jamming
  testbeds reproduce real degradation (2301.09615); jamming-aware routing recovers energy/links (1411.3736).
  Also cell-broadcast PWS alerts are SPOOFABLE (2604.24404, ties P12). SEVERITY: HIGH availability + integrity.

### Model supply chain (any third-party/pretrained model)
- BACKDOOR / DATA-POISONING: stealthy under-confidence backdoors evade human + automated inspection at high
  success (2202.11203); standardized benchmarks show many defense claims are unverified (BackdoorBench
  2206.12654/2407.19845). SEVERITY: HIGH supply-chain risk → provenance control on models + training data.

### Detector-evasion (deepfake / anomaly detectors — P11, P9/P10)
- DETECTOR ENSEMBLES EVADABLE: up to 90% evasion of organizer detectors (2607.25842); defenses+evasions
  co-evolve, blur defeated by spread-spectrum (2003.01279); purification-based detection has a brittle
  JPEG-Q70 "cliff" (2607.25842). SEVERITY: HIGH where image authenticity / anomaly thresholds gate alerts →
  never trust a single evasion-detector threshold.

## 2. Cross-cutting failure mode (strongest deployment lesson, ties P19)
HIGH CONFIDENCE ≠ CORRECTNESS under geographic/seasonal shift: foundation models stayed confident while
accuracy collapsed, ECE rose, 12-51% of shifted scenes confidently mislabeled (2610.08810); random CV
overstates skill vs spatial-block (2608.22293). ⇒ deterministic confidence is NOT a safe alert gate; monitor
UNCERTAINTY (MC-dropout entropy flagged all shifts, 2610.08810).

## 3. Honesty
On-paper catalogue; nothing attacked. All figures source-reported on non-fire benchmarks → re-test on P16
data. Defenses + monitoring in defense_and_monitoring_plan.md; evaluation discipline in
robustness_evaluation_plan.md.
