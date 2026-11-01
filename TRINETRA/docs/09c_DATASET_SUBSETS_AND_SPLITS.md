# 09c — SUBSETS, LEAKAGE-SAFE SPLITS, ADAPTERS, EVALUATION PLAN

## 1. Adapters (new files; existing loaders untouched)
| Command | Makes | Contract (matches `deep/datamodules.py`) |
|---------|-------|---------------------------------------|
| `build_npz.py folder` | class-folder images | fire: `images (N,1,3,H,W)`, `labels (N,2)`; deepfake: `images (N,3,H,W)`, `labels (N,)` |
| `build_npz.py yolo` | YOLO txt, then image-level multi-label | as fire |
| `build_npz.py iot` | CSV, then sliding windows | `X (N,C,T)`, `y (N,)` = alarm anywhere in window |
| `build_npz.py check` | contract + leakage report | prints `[OK]` / `[FAIL]` |
| `build_npz.py subset` | keep only some splits | same keys |
| `make_rl_logs.py` | offline-RL logs | `s,a,r,s_next,done,behavior_prob` |
Local test: `python data_adapters/test_build_npz.py` gives `ALL ADAPTER TESTS PASSED` (synthetic data, 2026-10-31).

## 2. Class-name mapping (never silently change the code's class list `[fire, smoke]`)
| Source label | Code label vector [fire, smoke] |
|--------------|------------------|
| FIRE Dataset `fire_images` / DeepFire `fire` / D-Fire class fire | [1,0] (+ smoke box gives [1,1]) |
| D-Fire class smoke / WildFire-smoke | [0,1] |
| `non_fire_images`, `nofire`, weather fog/smog, sandstorm, lightning | [0,0] |
| CIFAKE `REAL` / `FAKE` | deepfake label 0 / 1 |

## 3. Split rules (rule 14)
- Group key in `block`: video/source filename prefix, otherwise a perceptual-hash (aHash, Hamming ≤ 6) cluster, so
  near-duplicate frames always share a group. For IoT the key is the session (counter reset or time gap > 60 s).
- Group split 70/15/15 with seed 0 (`split` key). Trainers k-fold over train+val (after `subset`); `test` is
  touched once at the end.
- **Cross-dataset held-out:** train on D-Fire (+FIRE), test on DeepFire. Train on CIFAKE, test on StyleGAN faces.
  Train on smoke-IoT, test on NAB/UCI drift (anomaly scoring only).
- Leakage checklist: (1) `check` shows 0 groups in 2+ splits; (2) no file hash appears in two datasets of a
  train/test pair (run `sha256sum` over both and intersect); (3) IoT windows never cross sessions; (4) report
  which fraction of each dataset was used.
- Hinglish: ek hi video ke frames ko train aur test dono me daalna = exam paper pehle se dekh lena. Isliye group se split karte hain.

## 4. Smoke-test set (first hour)
`build_npz.py folder --max-per-class 150 --size 64` on P01 (about 300 images); `iot --window 30` on P10; CIFAKE
`--max-per-class 250 --size 32`. Each trainer then runs `--epochs 1`. Pass = script finishes and writes `*_report.json`.
Manifests are written by `--manifest data_manifests/<name>.csv` (paths + group + split + sha1 of path; no raw data).

## 5. Feature caching
Publish every built `.npz` as a private Kaggle Dataset `trinetra-<module>-v<k>` so other accounts attach it
instead of rebuilding. Record the run ID `<module>-<yyyymmdd>-<hhmm>-<seed>` in `docs/14_RESULTS_LOG.md`.

## 6. Evaluation plan per module (SOTA-level on small data)
| Module | Baseline first | Metrics | Seeds | Cross-dataset | Stress |
|--------|---------------|---------|-------|---------------|--------|
| M1 fire | climatology + logistic (in `admit_model`) + colour-histogram (G-06) | PR-AUC, recall @ FPR 1%, value score, ECE + reliability, abstain curve | 0..4 | DeepFire | weather confusers, JPEG q=20, 32 px downscale, night (gamma) |
| M5 IoT | numpy `ws8_anomaly` ensemble | PR-AUC, alarms per session-hour, time to detection | 0..4 | NAB, UCI drift | sensor dropout (`missing_modality`) |
| M6 deepfake | logistic on FFT energy | AUC, ECE | 0..4 | StyleGAN faces | JPEG, resize |
| Fusion | FM-1 vs PHARAOH vs GMF | value score, ECE, miss rate at fixed FA | 0..4 | n/a | one expert missing |
| RL | `RuleBaselinePolicy` | OPE value, ESS, feasible | 0..4 | n/a | eps 0.1 / 0.3 |
**Published-number rule:** any comparison must name benchmark + split + metric, and say plainly "our subset
result is NOT comparable" when we used a subset or a different split.
<!-- END -->
