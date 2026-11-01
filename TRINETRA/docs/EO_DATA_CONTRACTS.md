# Earth-observation data contracts

This file defines the input and split contract for `data_adapters/build_eo.py`. EO heads are prototype classifiers; none of the datasets below establishes operational landslide, flood, or Himalayan InSAR performance.

## Common NPZ contract

| key | shape / type | rule |
|---|---|---|
| `images` | `(N,C,H,W)` float32 | NaN/Inf replaced, then standardized per band |
| `labels` | `(N,)` float32 | binary patch label derived from the source mask/annotation |
| `block` | `(N,)` string/int | leakage group; a block must remain in one split |
| `split` | `(N,)` string | `train`, `val`, `test`; created by grouped splitting |
| `band_mean`, `band_std` | `(C,)` float32 | computed on the **training split only** |

Normalization is `(x - band_mean) / band_std`, with `1e-6` added to each standard deviation. Resizing uses block means when the scale factor is integral and nearest-index sampling otherwise.

Every run manifest must also record `source_kind = real | synthetic`, source dataset/version, builder command, license status, and whether labels are source annotations or generated. The three adapters below consume **real remote-sensing datasets**. Synthetic samples, if introduced for stress tests, must be marked `source_kind=synthetic`, kept out of the real held-out set, and reported separately. The current NPZ writer does not persist `source_kind`; the run manifest is therefore mandatory until that field is added.

## Dataset-specific contracts

| dataset | channels | patch label | leakage-safe split | license / caveat |
|---|---|---|---|---|
| Landslide4Sense | 14: Sentinel-2 B1–B12 plus slope and DEM | positive when landslide-mask pixel fraction exceeds `--min-frac` | coordinates are absent; group near-duplicates by RGB perceptual hash | dataset card license is **UNVERIFIED** in this repo; cite Ghorbanzadeh et al.; source kind `real` |
| Sen1Floods11 | 2: Sentinel-1 VV and VH | positive when flooded fraction among valid (`label >= 0`) pixels exceeds `--min-frac`; chips with <50% valid pixels are dropped | group by flood-event filename prefix; Bolivia is written as the cross-region held-out set with `--holdout-event Bolivia` | original license recorded as CC BY 4.0 **from memory—verify**; Kaggle-copy license unknown; source kind `real` |
| Hephaestus | image channels from the cropped InSAR product | positive if any annotation label is not `Non_Deformation`; corrupted/processing-error records are dropped | group strictly by annotation `frameID` (location) | MIT repository; volcanic deformation, not Himalayan landslide displacement; source kind `real` |

Hephaestus without annotations falls back to image-hash groups and prints a leakage warning. Such a run is smoke-test-only and must not be reported as a validated InSAR result. Raw interferogram output must never be described as validated displacement.

## Train/test discipline

1. Deduplicate and assign groups before fitting normalization.
2. Fit `band_mean` and `band_std` on training groups only.
3. Never move patches from the same event, `frameID`, or hash group across splits.
4. Keep Bolivia untouched as the Sen1Floods11 cross-region test when that protocol is used.
5. Report real and synthetic metrics separately; never pool them into one headline result.
6. Record missing masks, invalid pixels, dropped records, class balance, group count, and exact channel order.

Primary implementation: `data_adapters/build_eo.py`. Dataset provenance and unresolved license notes: `docs/09b_dataset_links.csv` and `docs/09e_GEOHAZARD_DATASETS.md`.

For the resource-limited prototype, use the caps in `docs/SMALL_GEO_DATASET_PACK.md`; they reduce processed data without changing these contracts.

<!-- END -->
