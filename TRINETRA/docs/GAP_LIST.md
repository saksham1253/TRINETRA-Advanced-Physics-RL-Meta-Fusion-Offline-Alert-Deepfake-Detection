# GAP LIST (doc-vs-code audit, 2026-10-31)
Triage: **FIX NOW** (cheap + important) / **FIX IF TIME** / **DOC ONLY**.

| ID | Gap | Evidence | Triage | Status |
|----|-----|----------|--------|--------|
| G-01 | Zero-shot classification is in research (`ws4_cctv/zero_shot_design.md`) but **not in code** | grep for clip/zero_shot in `src/` finds nothing | FIX IF TIME: new `zeroshot/` file (open_clip) and a calibrated `ExpertOutput` via `adapters.deep_expert` | **fixed**: `kaggle/eval_zeroshot.py` (dry-run tested) |
| G-02 | No loader for real datasets; trainers expect pre-built `.npz` | `datamodules.py` | FIX NOW | **fixed**: `data_adapters/build_npz.py` |
| G-03 | Offline RL needs logs; no simulator or log builder in repo | `train_offline_rl.py`, `rl.py` | FIX NOW | **fixed**: `data_adapters/make_rl_logs.py` |
| G-04 | `block` assumes lat/lon cells; image/IoT data has none, so default `"0_0"` puts **all samples in one block** (CV breaks or leaks) | `ImageFolderNPZ` default | FIX NOW | **fixed by adapter** (group keys) |
| G-05 | Fire model expects clips (T frames); image sets give T=1, so the temporal false-alarm benefit is not exercised | `fire_cnn.py` | DOC ONLY | documented H-04 |
| G-06 | `train_classifier.py` logistic baseline uses the model's own OOF score as its only feature (a recalibration of itself, not an independent baseline) | `X = oof_prob.reshape(-1,1)` | FIX IF TIME: add a colour-histogram baseline as a NEW script | **fixed**: `kaggle/baseline_colorhist.py` |
| G-07 | Trainers k-fold over the whole `.npz`; there is no untouched held-out test | `spatial_cv_indices` | FIX NOW | **fixed**: `build_npz.py subset --keep train val` + cross-dataset test |
| G-08 | Seeds: trainers call `set_seed(0)` only; config lists seeds [0..4] | `default.json` vs scripts | FIX IF TIME: loop seeds in the notebook (no code edit) | **fixed**: `--seed` + SEEDS loop in run_hackathon.sh |
| G-09 | Video anomaly: datasets planned but no frame-feature model in code | n/a | FIX IF TIME: embedding adapter, then `WindowNPZDataset` | open |
| G-10 | Text misinformation module absent | n/a | DOC ONLY (post-hackathon) | open |
| G-11 | UI / dashboard absent | n/a | FIX IF TIME (Figma Make app) | **fixed**: Figma Make dashboard |
| G-12 | Level cuts p*, 4p*, 10p* are ad hoc. With C_FA=5, C_miss=100, RED starts at fused p = 0.476 | `decision.conformal_level` | DOC ONLY until CRC thresholds are calibrated | open |
| G-13 | Paper ledger: 8/157 sampled arXiv IDs have a different title. **2606.21130** (repo: hazard EWS XGBoost; arXiv: AI-workload capacity stress) and **2610.04392** (repo: hazard rare-event pitfalls; arXiv: industrial defect AD benchmark) look misattributed. The other 6 are paraphrased titles | `docs/tools/paper_verify_log.json` | FIX NOW (human check) | flagged |
| G-14 | Ledger CSV has some malformed rows (fields shifted: read_depth values like " Zukoski") | parse of `analysis/02_paper_ledger.csv` | FIX IF TIME | open |
| G-15 | Kaggle limits never verified from a live source | `KAGGLE_BUDGET.md` §0 | FIX NOW by team (quota panel) | open |
| G-16 | `requirements-deep.txt` pins torch 2.3.1. Current Kaggle image ships a newer torch, so installing may downgrade it and burn time | file | DOC ONLY: try the preinstalled torch first, pin only on error | open |
| G-17 | Heskestad etc. carry `[coeff-verify]`. Coefficients are not yet checked against a primary source | `established_ef.py` | FIX IF TIME (04 physics doc) | open |
| G-18 | Deepfake face sets contain real people's faces | P15 | DOC ONLY: never show in demo/deck (rule 7) | open |
| G-19 | IoT/sensor module | team decision H-08 | DOC ONLY: FUTURE WORK | deferred |
Code bugs found by running the code: see `docs/BUG_STATUS.md` (B-01..B-16).
<!-- END -->
