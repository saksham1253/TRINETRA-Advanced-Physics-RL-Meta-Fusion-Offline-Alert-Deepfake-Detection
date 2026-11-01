# Small geospatial dataset pack

Use this pack for the current prototype instead of training on every available EO patch.

| component | small-pack content | approximate processed size | status |
|---|---:|---:|---|
| Landslide events | 184 NASA GLC positives + 552 controls, with POWER rain and Copernicus DEM slope | small tabular NPZ/CSV | already built and evaluated |
| GLOF | HMAGLOFDB v4: 766 records / 385 lakes | small table | already built; relation fitting only, not GLOF risk |
| Sentinel-2 landslides | 512 Landslide4Sense patches, 14 channels, resized to 64×64 | about 112 MiB float32 | adapter ready; model run pending |
| Sentinel-1 floods | up to 400 Sen1Floods11 VV/VH chips, 64×64; Bolivia remains held out when present | about 13 MiB float32 | adapter ready; model run pending |
| InSAR | 512 Hephaestus patches, 64×64 | about 24 MiB float32 | adapter ready; model run pending |

The processed EO pack is therefore roughly **150 MiB**, excluding NPZ compression and metadata. These are prototype caps, not benchmark protocols.

Optional context sources are documented in `docs/IMERG_AND_LULC.md`: use the small IMERG/ERA5 CSV for stress evaluation; keep LULC out of the primary training contract during the 18-hour run.

## Build and train

```bash
EPOCHS=8 bash trinetra/kaggle/run_hackathon.sh eo
```

Default caps:

```text
EO_SIZE=64
EO_L4S_N=512
EO_S1_N=400
EO_HEPH_N=512
```

For a smaller smoke run:

```bash
EO_L4S_N=128 EO_S1_N=128 EO_HEPH_N=128 EPOCHS=3 \
  bash trinetra/kaggle/run_hackathon.sh eo
```

The caps reduce the **processed/training pack**. Kaggle may still mount the complete source dataset. Do not describe this subset as a full-dataset benchmark. Splits remain group-aware, normalization uses training data only, and real/synthetic provenance follows `docs/EO_DATA_CONTRACTS.md`.

<!-- END -->
