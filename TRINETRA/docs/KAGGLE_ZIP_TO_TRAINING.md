# Kaggle ZIP-to-training runbook — 18-hour mode

## Goal

Team ke uploaded ZIP/folder pack ko model code badle bina leakage-safe NPZ files me convert karna, validate karna, phir ek private Kaggle Dataset ke roop me four accounts ko share karna.

## Account 0: convert once

Attach the team dataset and repository, then run:

```bash
!bash /kaggle/working/TRINETRA/trinetra/kaggle/prepare_kaggle_training_data.sh \
  /kaggle/input/<team-dataset-slug>
```

The command:

1. safely extracts ZIP/TAR files into `/kaggle/working/trinetra_stage`;
2. rejects path traversal, archive links, archives over 12 GB and aggregate extraction over 40 GB;
3. detects D-Fire, DeepFire, FIRE, weather, CIFAKE, faces, videos, L4S, Sen1Floods11 and Hephaestus layouts, and inventories IMERG/LULC files;
4. converts vision data with existing adapters;
5. builds the capped EO pack where sources are found;
6. validates shapes, finite values, row lengths and group leakage.

Outputs:

```text
/kaggle/working/npz/                         code-ready arrays
/kaggle/working/out/manifests/               source/group/split manifests
/kaggle/working/trinetra_stage/
  dataset_inventory.json                     detected and missing roots
  dataset_env.sh                             reproducible path exports
  ready_pack_report.json                     pass/fail per NPZ
```

Publish `npz/`, `out/manifests/`, inventory and validation report as a **private** Kaggle Dataset named `trinetra-ready-v1`. Do not publish raw files unless every source license allows redistribution.

If one archive is larger than 12 GB but legitimate:

```bash
MAX_ARCHIVE_GB=20 bash .../prepare_kaggle_training_data.sh /kaggle/input/<slug>
```

Do not raise this blindly; first inspect `dataset_inventory.json`.

## Detection review

Auto-detection chooses a common root when train/test folders both match. Before training:

```bash
!cat /kaggle/working/trinetra_stage/dataset_inventory.json
!cat /kaggle/working/trinetra_stage/ready_pack_report.json
```

If a root is wrong, override it before running the existing stage:

```bash
export CIFAKE=/kaggle/input/.../correct-root
export HEPH=/kaggle/input/.../images
export HEPH_ANN=/kaggle/input/.../annotations
```

Hephaestus is skipped without annotations because hash fallback cannot guarantee `frameID` leakage protection.

## Parallel training

All accounts attach `trinetra-ready-v1` and set:

```bash
export DATA=/kaggle/input/trinetra-ready-v1/npz
export OUT=/kaggle/working/out
export EPOCHS=15
export SEEDS="0 1 2"
```

| account | hours 1–7 | command |
|---|---|---|
| A | fire CNN + colour baseline; then video | `bash trinetra/kaggle/run_hackathon.sh fire`; then `video` |
| B | zero-shot + confuser evaluation | `bash trinetra/kaggle/run_hackathon.sh zeroshot` |
| C | deepfake, held-out generator and art stress | `bash trinetra/kaggle/run_hackathon.sh deepfake` |
| D | EO heads: L4S, Sen1Floods11, Hephaestus | `bash trinetra/kaggle/run_hackathon.sh eo-train`; do not claim metrics if adapter validation failed |

Publish each `/kaggle/working/out` as a private versioned artifact. Merge the four output folders into one account for fusion:

```bash
bash trinetra/kaggle/run_hackathon.sh fuse
```

Fusion must wait for fire OOF plus at least zero-shot or colour-histogram OOF. Deepfake is optional but preferred.

## 18-hour cut plan

- H0–1: extract, detect, convert, validate, publish ready pack.
- H1–7: four independent runs; save checkpoints and output datasets.
- H7–10: merge artifacts; fusion and offline RL.
- H10–13: failed-run recovery, seeds 1–2, only high-value ablations.
- H13–15: `collect_results.py`; copy reports and logs.
- H15–17: update results register/deck with measured values only.
- H17–18: freeze; cached demo rehearsal and handoff.

Never spend the final three hours downloading a replacement dataset. If a non-core set fails, record it and continue. Core minimum is D-Fire + DeepFire for fire, CIFAKE for media, and one validated EO source if the EO claim is shown.

<!-- END -->
