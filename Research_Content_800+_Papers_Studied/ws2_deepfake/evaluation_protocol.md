# ws2_deepfake/evaluation_protocol.md — PRE-REGISTERED evaluation protocol (P11, WS2)

Phase P11 · RESEARCH-ONLY. Pre-registered BEFORE any build (§0.5 anti-HARKing). Metrics are PROCESS/
validation targets, not results (Rule 16). Headline numbers are CROSS-GENERATOR + DEGRADED, never pristine
in-distribution.

## 1. Metrics
- AUC + Average Precision; TPR at FIXED LOW FPR (e.g. FPR = 0.1% / 1%) — the operationally meaningful metric;
- CROSS-GENERATOR accuracy (train on generator set A, test on unseen set B) — the primary generalization
  number;
- ROBUSTNESS CURVES vs compression quality / resize / screenshot / re-upload (not a single clean number);
- CALIBRATION ERROR (ECE) + reliability diagrams (the cost-matrix decision math requires calibrated scores);
- FAIRNESS: performance across demographics + across languages (incl. Indian languages/code-mixed) where
  applicable;
- For out-of-context: retrieval precision/recall of the reverse-search/near-duplicate stage + geo-temporal
  consistency accuracy.
- ≥5 seeds + CIs for learned components.

## 2. BANNED / demoted
- Pristine in-distribution AUC as a HEADLINE (it is near-saturated and misleading) — may appear only as a
  reference beside cross-generator + degraded numbers.
- Thresholds tuned on the test set; test-generator leakage into training.

## 3. Splits / protocols
- CROSS-GENERATOR: strict train/test split BY GENERATOR family (GAN↔diffusion↔face-swap↔unseen) + open-set
  (a held-out generator never seen in training).
- CROSS-DATASET: train on one dataset, test on another (e.g. FF++→Celeb-DF/DFDC/DF40) per the quota's
  generalization findings.
- DEGRADATION: evaluate on a staged platform-recompression pipeline (robustness_plan.md) at multiple quality
  levels.
- No person/identity in both train and test for face data; respect dataset licenses.

## 4. Mandatory baselines
A frequency/spectral detector + a CLIP/foundation-feature universal detector + a reverse-image/perceptual-
hash out-of-context baseline, all under the SAME cross-generator + degradation protocol, before any bespoke
model is claimed better.

## 5. Required experiments (build phase; task 9)
(1) ≥1 cross-generator evaluation; (2) ≥1 degradation robustness curve; (3) ≥1 adversarial/anti-forensics
test; (4) ≥1 ablation of the physics-plausibility signal (does it add anything over forensics alone — likely
NOT, pre-registered as possibly null); (5) ≥1 end-to-end decision-policy study sweeping the cost matrix and
showing threshold movement. Planning-level compute in experiment_plan.md.

## 6. Fair-comparison requirements
Match generators, degradation levels, metric (TPR@lowFPR + cross-generator), and calibration across all
compared methods; report provenance/watermark results as POSITIVE-only evidence, never as a fakery test.

## 7. Honesty
Nothing measured. The protocol exists because in-distribution numbers overstate real deployment performance
(SOTA scan §0); the system's real reliability comes from corroboration + human-in-the-loop, which this
protocol also exercises (experiment 5).
