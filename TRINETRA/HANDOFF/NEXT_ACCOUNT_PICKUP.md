# NEXT ACCOUNT PICKUP (for a fresh AI with zero memory) — updated 2026-10-31 ~11:50 UTC
**(a) TRINETRA:** an advisory, offline-first fire early-warning research prototype for India. A fire CNN, a zero-shot CLIP channel and a
colour baseline become calibrated "experts". A deepfake checker lowers trust in fake media. FM-1 fusion feeds one decision function with
a raise-only shield, then human approval before any CAP alert. **IoT = future work.** Geohazard (landslide/GLOF/EO/InSAR) is IN scope (H-15).
Real geo physics, RL-simulator and Geo-PINN runs exist; vision and EO model runs are still pending.

**(b) Repo:** github.com/saksham1253/TRINETRA-CONTENT-OG, main; latest saved Make version before this task: `07bfde7`. In this Figma Make project, `TRINETRA/` mirrors
`default-workspace/` (no binaries) and holds ALL new and edited work. The team must push it to GitHub. The dashboard is `src/App.tsx`.

**(c) Read first:** 1 `HANDOFF/STATE.json`; 2 `HANDOFF/NEXT_ACTION.md`; 3 `docs/10_RUNBOOK_36H.md` (28-h plan); 3b `docs/09d_DATASET_LAYOUTS_AND_SUFFICIENCY.md` + `docs/09e_GEOHAZARD_DATASETS.md`; 3c `results/RESULTS.md` (the only REAL numbers so far);
4 `docs/09e_TPD_DATASHEET.md`; 5 `docs/CODE_CHANGE_LOG.md`.

**(d) Done:** inventory, code map, flowcharts, gap list, dataset pack (verified), adapters, paper links, RL/fusion/averaging docs, cyclone
spec, demo doc, dataset layouts verified via the Kaggle file API plus a sufficiency review (P33-P37 added: FireSense videos, small flames, Intel scenes, home fire, AI art), **31 code/data bugs found and fixed** (docs/BUG_STATUS.md), geohazard pipeline on REAL data (NASA landslide catalog + POWER rain + Copernicus DEM + HMAGLOFDB; results in `results/`), a physics-based landslide RL environment (`ws5_fusion_rl/env_landslide.py`), and EO adapters for Sentinel-2 (L4S), Sentinel-1 (Sen1Floods11) and InSAR (Hephaestus) (docs/BUG_STATUS.md), and **a complete results chain**:
`run_hackathon.sh` stages smoke/build/fire/zeroshot/deepfake/fuse; `eval_zeroshot.py`, `baseline_colorhist.py`, `build_fusion_cache.py`,
`collect_results.py`, `smoke_test_all.py`. Verified 2026-10-31: unit tests 128/128, CI gates 6/6, smoke chain PASS (CPU torch).
TPD-0.1 now has a deterministic 736-row geo master index (`data_manifests/tpd_index.csv`), profiles, target schemas, conversion report and datasheet.
**Waiting on:** real fire/zero-shot/deepfake/EO Kaggle runs and EO source attachments.

**(e) Decisions:** `HANDOFF/DECISIONS.md` H-01..H-12 (scope H-08, deepfake semantics H-10, RL gate H-11, metrics H-12).

**(f) Rules:** repo is truth; numbers only from `collect_results.py` output / docs/14; label OUR RESULT vs PAPER REPORTS; smoke/dry-run
numbers are never reported; Class A/B/C; log every code edit in CODE_CHANGE_LOG; no data in git; Hinglish explanations; short chat;
files < 1,500 words ending `<!-- END -->`.

**(g) Do NOT redo:** dataset/paper verification, adapters, bug fixes, smoke chain. To re-verify locally:
`cd TRINETRA/trinetra && python run_tests.py && python kaggle/smoke_test_all.py` (needs numpy, pillow, torch; open_clip optional).

**(h) Risks:** DataParallel path untested (B-09); open_clip needs internet for weights; fusion uses SYNTHETIC PAIRING; Kaggle limits unverified.
GLOF raw rows and all EO rows are not in TPD yet. Geo prevalence is artificial case-control prevalence.

**(i) Exact next action:** when the team provides its Kaggle dataset link, run `prepare_kaggle_training_data.sh` as documented in `docs/KAGGLE_ZIP_TO_TRAINING.md`; inspect inventory + validation before training. Publish the validated NPZ pack privately, then use four accounts in parallel.

**(j) Cut-order:** honest runnable demo > accurate docs > handoff > results > physics docs > glossary.

**(k) Open questions:** `HANDOFF/OPEN_QUESTIONS.md` (deadline, cyclone name, account owners still unanswered).
<!-- END -->
