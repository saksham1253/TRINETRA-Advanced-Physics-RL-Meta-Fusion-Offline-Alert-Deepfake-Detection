# 09d — Target schemas from code

## Landslide physics table

Source of truth: `data_adapters/build_geo.py` and `trinetra/kaggle/geo_physics_hindcast.py`.

| field group | fields | type / unit | requirement |
|---|---|---|---|
| identity | `event_id`, `day` | ID, ISO date | required |
| location | `lat`, `lon` | decimal degrees | required; grouping uses 0.1° cells |
| target | `label` | 0 control, 1 catalog event | required |
| terrain | `slope_p90_deg`, `elev_m` | degrees, metres | required |
| rain | `rain_1d`, `rain_3d`, `rain_7d`, `rain_15d`, `rain_30d`, `rain_max3` | mm | required |
| Caine | `caine_D_h`, `caine_I_mmh`, `caine_ratio` | hours, mm/h, ratio | required |
| slope physics | `psi_m`, `fs`, `fs_dry`, `dfs`, `c_backcalc_kpa`, `fs_backcalc` | m, dimensionless, kPa | required for physics models |

Soil strength values are assumptions, not observations. Absolute FS is uncalibrated; dFS is the preferred rain-driven change signal.

## Geo-PINN NPZ

Source: `data_adapters/build_geo.py`; consumer: `deep/datamodules.GeoSeriesDataset`.

| key | shape | units |
|---|---|---|
| `Z` | `(N,)` | m |
| `t` | `(N,)` | days |
| `rain` | `(N,)` | mm/h |
| `static` | `(N,6)` | cohesion kPa, friction degrees, unit weight kN/m³, depth m, slope degrees, susceptibility |
| `label`, `lat`, `lon` | `(N,)` | binary, degrees |

## Earth-observation NPZ

Source: `data_adapters/build_eo.py`; consumer: `kaggle/train_classifier.py --model eo`.

`images (N,C,H,W)` float32, `labels (N,)`, `block (N,)`, `split (N,)`, `band_mean (C,)`, `band_std (C,)`. L4S has C=14; Sen1Floods11 has C=2 (VV/VH); Hephaestus currently produces C=3 display-image channels. Normalization is fit on training groups only. See `docs/EO_DATA_CONTRACTS.md`.

## TPD master index

Source: `data_adapters/build_tpd_index.py`.

Each row records sample identity, module/modality, source dataset IDs, source URI, raw and unified labels, hazard, group and split protocol, license, SHA-256 provenance, provenance class, synthetic/derived/own-captured flags and quality notes. A planned dataset is never represented by a fabricated sample row.

<!-- END -->
