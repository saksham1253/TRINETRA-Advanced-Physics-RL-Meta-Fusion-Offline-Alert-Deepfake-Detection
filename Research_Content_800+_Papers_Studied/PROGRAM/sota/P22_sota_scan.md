# PROGRAM/sota/P22_sota_scan.md — SOTA scan: meta-fusion + aggregation + RL (P22)

RESEARCH NOTES. All numbers SOURCE-REPORTED (Rule 16), none ours. Grounds the P22 derivations.

## 1. Fusion / aggregation SOTA (source-reported) and the gap for us
- Multimodal fusion: dynamic/gated fusion cuts compute ~46.5% at ~equal accuracy (DynMM 2204.00102); quality-/
  uncertainty-aware fusion is provably more robust on low-quality inputs (QMF 2306.02050). GAP: these optimize
  accuracy, not life-safety asymmetry or physics consistency.
- Model averaging: hierarchical/input-adaptive stacking & BMA are asymptotically optimal/calibrated (2101.08954,
  2510.22054); conformal+BMA converges to optimal-efficiency sets (CBMA 2511.16924). GAP: no shift-reweighting
  or fail-safe by default.
- Evidential / D-S: conflict-discounted belief fusion turns inter-modal conflict into uncertainty, calibrated
  (ECE 0.057 reported, 2608.29235); reliability-discounted decision fusion (2412.01215). GAP: needs a physics
  prior mass + bounded-[0,1] adaptation.
- Covariance intersection: split/overlapping CI give provably CONSISTENT conservative fusion under unknown/
  partial correlation (2307.14741, 2603.16768); AA density fusion links to CI/Kalman (2110.01440). GAP: for
  continuous hazard-trend state only.
- Opinion pooling: linear/log-linear/Hölder pools + calibration theory (1106.1638); uncertainty-weighted
  semantic opinion pooling (SCoOP 2603.23853). GAP: fixed order, no adaptive safety bias.
- Robust aggregation: Byzantine-robust aggregators nullify poisoning with provable bias bounds (2506.23183,
  2206.04568). GAP: ties to our source-reliability gating + P16 red-team.

→ The P22 operator (PHARAOH) + 6 fusion models are designed to fill these gaps: physics-consistency gating,
drift-decayed reliability, adaptive-order fail-toward-caution, conformal-under-shift band, CI consistency,
evidential conflict→uncertainty, and an advisory RL tuner. All CLASS B/C, UNVALIDATED.

## 2. RL-for-fusion SOTA (source-reported) and the gap
- Physics-informed / model-based RL improves sample-efficiency and return (2212.02179; SINDy-MBRL 2208.14501;
  survey 2309.01909); physics-prior reward reshaping gives large reported gains (Gibbs prior 2604.01830).
- Active perception / value-of-information: RL sensor-selection reaches near always-on performance at a
  fraction of the sensing (2607.22667, 1906.07233, 2602.01266).
- Ensemble-weighting RL adapts sensor weights for robustness (Lvio-Fusion 2106.06783); multimodal RL handles
  sensor dropout (2606.15514, 1703.04550); safe/constrained RL cuts constraint violations (2607.03125).
- CAUTION: naive RL can underperform strong classical baselines (2509.19972) → beat-baseline gate mandatory.
→ GAP: none of these is life-safety-advisory with a hard fail-safe + physics-consistency reward; FM-6 adds that.

## 3. Honesty
Nothing measured; every cited number is the source paper's own result on its own data. The P22 constructs are
UNVALIDATED Class-B/C hypotheses with validation roadmaps + expert-review flags; no performance is claimed.
