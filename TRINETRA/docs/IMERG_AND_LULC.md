# IMERG and LULC decision for the 18-hour prototype

## Short decision

| source | use now? | reason |
|---|---|---|
| NASA POWER rain | **yes, primary** | existing pipeline and measured geo results already use it |
| ERA5 + IMERG cloudburst CSV | **yes, optional stress/evaluation** | small (16.9 MB), Western Himalaya, no model-contract change |
| Raw GPM IMERG Final daily | later unless already collected | better 0.1° rainfall, but Earthdata login plus spatial/time conversion is required |
| LULC map | optional context/error analysis | useful for susceptibility interpretation, but not in the current six-feature Geo-PINN contract |
| EuroSAT | no for hazard validation | land-cover pretraining only; Europe domain and not an India hazard label set |

Hinglish: abhi running pipeline ko todkar naya channel add karna risky hai. POWER se baseline chalao; IMERG CSV ko extreme-rain stress check banao. LULC ko map/context panel me dikhao, headline model metric me tab tak nahi jodo jab tak grouped ablation na ho.

## IMERG links

1. **Small Kaggle option (recommended now): ERA5 + IMERG cloudburst dataset**
   - https://www.kaggle.com/datasets/simrankhalsa431/era5-and-imerg-dataset-for-cloudburst-prediction
   - Repository registry: P41, 16.9 MB, `labeled_cloudburst.csv`, CC BY-NC-SA 4.0.
   - Role: rain-extreme evaluation/stress set; do not silently mix its labels into NASA GLC.

2. **NASA GPM IMERG Final daily v07**
   - Data directory: https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDF.07/
   - Earthdata registration: https://urs.earthdata.nasa.gov/users/new
   - Registry: P40, approximately 30 MB per global day. Download only India/event windows.
   - Role: later replacement forcing for POWER. Himalayan IMERG remains a noisy satellite estimate, not ground truth.

## LULC links

1. **ESA WorldCover 2021, 10 m**
   - Downloader: https://worldcover2021.esa.int/downloader
   - AWS Open Data registry: https://registry.opendata.aws/esa-worldcover-vito/
   - Recommended role: sample the class at event/control locations for stratified error analysis and map display.
   - Status: official leads; access was not rechecked from this sandbox, so verify before marking READY.

2. **EuroSAT Sentinel-2 land-cover classification**
   - https://www.kaggle.com/datasets/apollo2506/eurosat-dataset
   - Registry: P47, approximately 3 GB, optional encoder warm-up only.

## Kaggle-pack handling

`stage_kaggle_archives.py` records matching files as:

```text
IMERG_CSV=/.../imerg_or_cloudburst.csv
LULC_ROOT=/.../worldcover_or_lulc_tiles
```

This is discovery only. It deliberately does not inject either source into training. When the team link arrives, inspect the real IMERG columns and LULC raster CRS/nodata values before writing a converter. Any LULC model-input experiment must be a new flagged ablation; existing results remain POWER/no-LULC.

<!-- END -->
