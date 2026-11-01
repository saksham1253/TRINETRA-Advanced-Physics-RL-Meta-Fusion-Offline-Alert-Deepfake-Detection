# 09e — GEOHAZARD DATASETS (landslide, GLOF, Sentinel-1/2, InSAR, DEM, IMERG) + how each is used
Added 2026-10-31 after the team pointed out that the geo side was missing. Rows P38-P54 in `docs/09b_dataset_links.csv`
(sizes/licences from the Kaggle API snapshot or HTTP checks in `docs/tools/dataset_verify_2026-10-31.json`).

## A. What to fetch (prototype scale)
| Need | Dataset (ID) | Size | Access | Used by |
|---|---|---|---|---|
| Landslide labels (India) | **NASA Global Landslide Catalog** (P38): 1,265 India events 2007-2016 | 8.5 MB | open | `build_geo.py` → hindcast, Geo-PINN, RL |
| Rainfall (no login) | **NASA POWER PRECTOTCORR** (P39) | KB per call | open API | rain forcing |
| Rainfall 0.1° (upgrade) | **GPM IMERG Final daily** (P40) | ~30 MB/day | free Earthdata login (register NOW) | swap-in for POWER |
| Rainfall extremes India | ERA5+IMERG cloudburst CSV (P41) | 17 MB | Kaggle, CC BY-NC-SA | eval |
| **DEM** | **Copernicus DEM GLO-30 on AWS** (P42), auto-downloaded per 1° tile | 41.7 MB/tile | open, no login | slope β for FS / Iverson |
| **Sentinel-2** landslides | **Landslide4Sense** (P43), 14 bands = S2 + slope + DEM; includes Kodagu, India | 9 GB (subset to 3,799 train patches) | Kaggle | EO head (`build_eo.py l4s`) |
| Sentinel-2 smoke test | L4S cleaned RGB (P44) | 57 MB | Kaggle CC0 | quick test |
| **Sentinel-1** floods | **Sen1Floods11** hand-labelled (P45) + DEM/slope (P46) | 772 MB + 67 MB | Kaggle | EO head (`build_eo.py sen1floods11`, Bolivia held-out) |
| Sentinel-2 warm-up | EuroSAT all bands (P47) | 3 GB | Kaggle CC0 | optional pretraining |
| **GLOF** events | **ICIMOD HMAGLOFDB v4** (P49): 766 records, 385 lakes | 460 KB | open (GitHub raw) | `glof_physics_check.py` |
| Glacial lakes (S2) | Himalayan glacial lake images + masks (P48) | 108 MB | Kaggle CC BY | lake mapping (planned) |
| Glaciers | World Glacier Inventory (P50) | 17 MB | Kaggle CC0 | context |
| **InSAR** | **Hephaestus** (P51): 19,919 annotated Sentinel-1 interferograms, MIT | size unverified (Dropbox) | open | EO head (`build_eo.py hephaestus`, group = frameID) |
| InSAR India | COMET LiCSAR frames (P52), e.g. Joshimath | per frame | open web (403 to bot) | lead |
| Raw S1/S2 | ASF Vertex / Copernicus Data Space (P53) | ~1 GB/scene | free account | optional |
| India fire (bonus) | Uttarakhand wildfire 1 km hourly stack (P54) | 2.9 GB | Kaggle CC BY | context / spread |

## B. Rejected or lead only
Kaggle "insar-data-new" / "insartestset" (1-2 opaque files, no description), "cinsar" (a chatbot project, not data), the India elevation
grid 4.5 GB (provenance unclear; Copernicus DEM preferred). Zenodo search API returned 403 from this sandbox, so Landslide4Sense,
GLOF and InSAR Zenodo records are reached via GitHub/Kaggle instead.

## C. Design notes (leakage + honesty)
- **Landslide:** case-control. Positive = GLC event day. Controls = the same place on 3 random monsoon days of other years, with no event
  within ±0.45° and ±15 days. Spatial-block CV (0.1° cells). The base rate is artificial, so ROC-AUC is the headline.
- **Soil is unknown:** c′ is back-analysed so FS_dry = 1.2 (docs/04 §3); the rain signal ΔFS is independent of c′.
- **EO:** Landslide4Sense has no coordinates, so it is grouped by image hash. Sen1Floods11 is grouped by flood event, with Bolivia held out
  (dataset convention). Hephaestus is grouped by frameID (location).
- **Still missing:** piezometer/tilt time series (Iverson dynamics are not testable), breach heights for GLOF peak-flow formulas, IMERG at
  0.1° (needs login), Indian InSAR frames (LiCSAR 403).
- Where rows here have no number, the result is not measured. Numbers live only in `results/RESULTS.md` (docs/14).
<!-- END -->
