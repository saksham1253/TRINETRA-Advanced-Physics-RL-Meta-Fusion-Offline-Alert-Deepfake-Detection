# 15 — PRODUCT + DEMO
**Life-safety statement (show on screen):** TRINETRA is an advisory research prototype. It complements certified fire
alarms and official IMD/NDMA warnings and never replaces them. No public alert is sent without human approval (enforced in
`ws3_alert/cap.py`: refuses without an `APPROVED:` token).

## 3-minute demo (runs offline from cached outputs)
1. (30 s) Problem + one-line idea: multiple weak witnesses, physics checks, honest fusion, human decides.
2. (60 s) `python demo.py` (or the recorded terminal output): the fire/geo cycle prints the level, uncertainty and the CAP XML.
   Point at `advisory=true`.
3. (45 s) The fusion worked example (07 §A): show the weights and why deepfake gets 0.15 weight. RED level, pred_set [ORANGE, RED].
4. (30 s) Honesty: the hindcast prints `admitted=False` on synthetic data. "We do not claim accuracy until the gate passes."
5. (15 s) Data pack: small, verified, leakage-safe (09b/09c).
**Fallback:** if the laptop fails, use screenshots of the steps above (team: capture them at hour 24).

## 7-minute demo
Add: the Kaggle report JSON from 14 (only if real), a stress test of confusers (fog/sandstorm), the cyclone historical replay
(13 §7), and the RL OPE verdict (deploy vs keep baseline).

## README quick start (stranger, 10 min)
```bash
git clone https://github.com/saksham1253/TRINETRA-CONTENT-OG && cd TRINETRA-CONTENT-OG/default-workspace/trinetra
python -m venv .venv && . .venv/bin/activate && pip install numpy pandas lxml
python run_tests.py && python scripts/ci_gates.py && python demo.py
```
Data: see `docs/09b_PROTOTYPE_DATASETS_AND_LINKS.md`. Trouble: `ModuleNotFoundError: numpy` means the venv is not active.

## Limitations (say them)
No trained-model results yet. Small/old datasets (2010-2020, mostly non-Indian), so numbers would not be comparable to
full benchmarks. Zero-shot, video anomaly, text misinformation and cyclone exist as design only. Fusion calibration uses
synthetic pairing. Kaggle limits are unverified.

## Judge Q&A (short honest answers)
| Q | A |
|---|---|
| Why physics? | Rejects implausible regimes (Byram N_c down-weights wind-dominated "fire"), explainable |
| Why not just YOLO? | A detector is one witness. Temporal validation + IoT + physics cut false alarms; the detector is still used |
| How does fusion work? | FM-1 weighted mean, w = r·c·exp(-u/τ), conflict raises U* (07) |
| Why this averaging? | Bounded, missing-safe, simple; PHARAOH is an opt-in experiment, not a claim |
| What does RL decide? | HOLD/WATCH/ALARM; deployed only if OPE beats the rule baseline; the shield can only raise |
| Leakage? | group splits, perceptual-hash dedupe, cross-dataset test (09c) |
| False alarms? | cost-loss p*, temporal validator, nuisance stress set |
| Accuracy? | not measured yet; no number until `admitted=true` |
| Offline? | numpy-only core, LoRa codec, DTN store-and-forward |
| Privacy? | no raw-video egress guard (`common/security.py`); faces never shown |
| Novel? | PHARAOH/ND terms are Class C hypotheses, default OFF; "novelty not verified" |
| More time? | zero-shot channel, video AD, India data (MOSDAC/Bhuvan), cyclone module |
<!-- END -->
