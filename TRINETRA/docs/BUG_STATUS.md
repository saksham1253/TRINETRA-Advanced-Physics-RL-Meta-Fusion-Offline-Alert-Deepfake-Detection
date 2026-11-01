# BUG STATUS — all findings, one table (updated 2026-10-31, hackathon v2)
Two sources: (1) bugs found **this session by running the code** (B-xx), (2) the repo's `TRINETRA_Bug_Report.md`
(#0-#32, mostly research-document findings). Status: **FIXED (tested)** / **FIXED earlier (evidence)** / **DOC** (a design
or research item, not a code bug; out of the 28-h scope) / **OPEN**.

## A. Found by running the code (this session; every fix tested on CPU torch 2.15 with synthetic data)
| ID | Bug | Fix | Status |
|----|-----|-----|--------|
| B-01 | All 5 trainers crash if `--out` folder does not exist | `os.makedirs` / `ensure_dir` | FIXED (tested) |
| B-02 | Offline-RL gate compared against the *logging* policy and **admitted a learned policy on random data** (-0.486 vs -0.488) | compare vs `RuleBaselinePolicy` via WIS on same logs + paired-bootstrap 95% LCB > 0 | FIXED (tested: random data, so KEEP baseline) |
| B-03 | `TemperatureScaler` imported but never used, so probabilities were uncalibrated | cross-fitted temperature in `deep/oof_utils.py` (ECE 0.22 to 0.03 on synthetic) | FIXED (tested) |
| B-04 | No OOF predictions saved, so fusion, RL and results could not be built | standard `*_oof.npz` from every trainer | FIXED (tested) |
| B-05 | Seeds fixed at 0, folds fixed at 5 | `--seed --folds --num-workers` (defaults unchanged) | FIXED |
| B-06 | No untouched held-out test | `--test` with fold-ensemble scoring | FIXED (tested) |
| B-07 | Anomaly scores min-max pooled across fold models (different scales) | per-fold p99-of-train-normal normalization | FIXED (tested) |
| B-08 | Per-sample inference loop (slow on 4k images) | batched `predict()` | FIXED |
| B-09 | DataParallel received the string `block` list | drop non-tensors before DP | FIXED (CPU cannot test DP; UNTESTED on T4x2) |
| B-10 | `deepfake` p_fake fused as if it were fire probability | `authenticity_adjusted_reliability`: r' = r(1-p_fake) on media experts | FIXED (in fusion cache builder) |
| B-11 | `deep_expert("zeroshot")` raised KeyError | added `zeroshot`, `iot`, `colorhist` to `_POLICY` | FIXED |
| B-12 | Admission baseline = logistic on the model's own score (not independent) | `kaggle/baseline_colorhist.py` | FIXED (new baseline) |
| B-13 | Value score is ≈0 on BALANCED sets when p* = 0.048 (negatives at 0.2 still alarm) | report also ROC-AUC, PR-AUC, recall@FPR 5%/1%, calibrated value score | FIXED (reporting); see docs/14 |
| B-14 | `make_rl_logs.py` crashed if folder missing | mkdir | FIXED (tested) |
| B-15 | EO trainer needs `timm`; EO out of scope | not run | DOC |
| B-16 | IoT features un-standardized | train-split z-score in `build_npz.py iot` | FIXED (IoT is FUTURE WORK) |
| B-17 | StyleGAN faces folders are `Final Dataset/Real` and `Fake` (capital); build default `real/fake` would fail | verified map | FIXED (layout verified) |
| B-18 | 3,500 faces are `fake_#_aug_#` copies, so augmented copies could straddle train/test (LEAK) | `_aug_#` maps to its source group | FIXED (tested) |
| B-19 | D-Fire AoF images are consecutive camera frames and could leak across splits | `--seq-bucket 50` | FIXED (tested) |
| B-20 | D-Fire class ids are not in the README | `yolo --classes auto` reads `data.yaml` | FIXED (tested) |
| B-21 | web-scraped held-out sets may contain the same photos as D-Fire | `build_npz.py dedupe` | FIXED (tested) |
| B-22 | DeepFire `Testing/` has no class folders | use `Training/fire`, `Training/nofire` | FIXED (layout verified) |
| B-23 | Repo shield `FS<1 -> ORANGE` with assumed soil fires FOREVER on Himalayan slopes (FS_dry < 1 at 40-44 deg) | back-analysed c' (FS_dry = 1.2) in build_geo + env | FIXED (data side; shield code unchanged) |
| B-24 | Hazard fit used `1.2 - fs_backcalc`; on gentle slopes c' clips at 0 -> huge negative values (min -8.5) | use dFS, which is independent of c' | FIXED (tested) |
| B-25 | RL-env deploy rule compared raw means and admitted a +0.01 noise gain | paired per-episode 95% LCB > 0 | FIXED (tested) |
| B-26 | `train_classifier --model eo` hard-coded 6 input channels (L4S has 14, S1 has 2) | channels from data; `--eo-backbone/--eo-pretrained/--eo-freeze` | FIXED (tested 14-band) |
| B-27 | Geo-PINN collapsed to a constant (resolution 0): constant c'=5 kPa makes FS<1 everywhere, so the physics hinge pushes all to high risk | back-analysed c' in static[0] | FIXED (needed, not sufficient) |
| B-28 | Geo-PINN collapse #2: raw SI inputs (t ~ 1e5 s next to rain ~ 1e-7 m/s) are erased by LayerNorm | nondimensional inputs (days, mm/h) + D0 passed in the same units (4.32 m2/day) | FIXED (tested: spread 0.19-0.70) |
| B-29 | `train_geo_pinn.py` saved no OOF/seed | OOF artifact + `--seed` | FIXED |
| B-30 | Env oracle/physics rule used p* cut points instead of expected cost | myopic Bayes action argmin E[cost] | FIXED (tested) |

## B. Repo bug report (`TRINETRA_Bug_Report.md`)
| # | Topic | Status | Evidence |
|---|-------|--------|----------|
| 0 | fix workflow silently failed | addressed | this table + tests 128/128 + smoke chain PASS |
| 1 | conflicting evacuate thresholds | FIXED earlier | single `decision.decide`, cuts from p* |
| 2 | suction-stress sign | FIXED earlier | `ws1b_geophys/fs.py` invariant, golden tests |
| 3 | Iverson cos²β | FIXED earlier | `iverson.py`: slope only via D1 = D0/cos²β |
| 4 | MS-IVE α claim | FIXED earlier | `fukuzono.py` α=2 linear + regime flag |
| 5 | mislabelled citation 2603.15681 | DOC | paper ledger issue |
| 6 | 433 MHz LoRa | FIXED earlier | `lora_codec.py` IN865-867 |
| 7, 8, 10, 14, 30 | hardware/edge/storage claims | DOC | hardware out of scope |
| 9, 20, 26 | reward weighting / shield realizability | partly | reward costs from config; shield raise-only; predictive shield = future |
| 11, 19, 27 | evaluation validity, persistence, RL eval | FIXED | spatial-CV, `persistence` baseline, honest OPE vs rule (B-02) |
| 12 | proxy to third-party endpoint | FIXED (not in mirror) | no `Proxy.py` in repo tree |
| 13, 24 | conformal "guarantee" overstated | FIXED earlier | `ws6_robust/conformal.py` wording + ACI/Mondrian |
| 15 | unverified I-D / GLOF constants | OPEN (DOC) | landslide scope, needs PDFs |
| 16, 18 | novelty / prior art | DOC | "novelty not verified" rule |
| 21, 28 | GMF multicollinearity / gating | partly | bounded residual + `correlation.py` BLUE |
| 22 | Deep-SVDD collapse | FIXED earlier | `init_center` eps guard |
| 23, 25, 29, 31, 32 | feedback shift, rainfall displacement, sensor fault, no dominant fusion, compliance | DOC / partly | #31 tested by `build_fusion_cache.py` rule comparison |
<!-- END -->
