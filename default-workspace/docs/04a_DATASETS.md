# 04a — DATASETS (long form): selected deep entries + candidate pool

> Companion to [04_DATASETS.md](<04_DATASETS.md>) (the index + full master table of all 164 IDs). This file
> holds the **16-field deep entries for the STATUS=selected datasets only** (13 of them), then the entire
> **candidate pool** as compact one-row tables grouped by modality. Facts are reproduced from `DATASETS.md`
> and `DATASETS_CATALOGUE.md` exactly, with their verification tags. See `_CANON.md §9` for provenance.

## Honesty posture (carried from 04 — do not soften)
- **NONE downloaded.** Every acquisition status below is `[UNVERIFIED — not downloaded]`.
- **No EDA / no statistics computed.** Any `N` / size is *as recorded in the registry*, not measured by us;
  several are explicitly flagged UNVERIFIED or "named" (from a citing abstract, not the owning paper).
- **Licenses are as-recorded and mostly UNVERIFIED.** "source records X" ≠ fact. Tags `[V]/[V*]/[D]` and
  `STATUS` are reproduced from the registry, not re-adjudicated here.
- Free-only rule **C4**: no paid dataset is STATUS=selected; UNCLEAR-cost sets stay candidate.

---

# Part 1 — SELECTED datasets (16-field deep entries)

The 13 datasets the program marked **STATUS=selected** in `DATASETS.md` — the free, existence-verified
"shopping list" that matters for handover. All others are candidates (Part 2). Field order:
*ID/name · modality · hazard/task + WS/chapter · provider · access URL · license[as-recorded] · size · N ·
spatial coverage · temporal coverage · resolution · label type · known biases/caveats · split guidance ·
acquisition status · consuming model/chapter.*

> Reminder: D01–D07 are **continuous sensor missions**, not fixed benchmarks — we index our own
> event-indexed cubes from them, so "N / native split" is n/a and leakage control is ours to impose.

### D01 — Sentinel-1 SAR (Copernicus CDSE) · `[V]` selected
- **Modality:** C-band synthetic-aperture radar (GRD / SLC), all-weather, cloud-penetrating.
- **Hazard/task · WS · chapter:** monsoon flood mapping + landslide/ground deformation; WS1/WS8; ch 06, 12.
- **Provider:** ESA / Copernicus (Copernicus Data Space Ecosystem).
- **Access URL:** https://dataspace.copernicus.eu/ (AWS/GEE mirrors exist).
- **License [as-recorded]:** Copernicus free/open `[V]`.
- **Size:** continuous mission (not a fixed corpus).
- **N:** n/a — we build event cubes.
- **Spatial coverage:** global, incl. India / Himalaya.
- **Temporal coverage:** continuous mission.
- **Resolution:** ~10 m.
- **Label type:** none intrinsic; labels come from hazard inventories (D08/D15/D22).
- **Known biases/caveats:** SLC interferometry is compute-heavy → use GRD + a learned-coherence proxy
  (D21 / arXiv 2606.07374) to stay in the Kaggle budget.
- **Split guidance:** tile + time block CV, buffer ≥ InSAR range (DC-01). [HYPOTHESIS protocol — see ch 12.]
- **Acquisition status:** [UNVERIFIED — not downloaded]; free registration needed for bulk/STAC/openEO.
- **Consuming model/chapter:** masked-InSAR SSL encoder + deformation-forecast head (ch 05/06).
- **F3 — paper/official/mirror:** no owning data-paper recorded → "not found in sources"; official https://dataspace.copernicus.eu/; mirrors AWS `s3://sentinel-s1-l1c`, GEE `COPERNICUS/S1_GRD`.
- **F8 — load [UNTESTED]:** `pystac_client.Client.open("https://catalogue.dataspace.copernicus.eu/stac").search(collections=["SENTINEL-1"], bbox=..., datetime=...)` (CDSE account required).
- **F12 — preprocess/augment order [HYPOTHESIS, planning]:** apply-orbit → border+thermal-noise removal → radiometric cal (σ⁰) → optional speckle filter (keep raw for learned coherence) → RTC geocode → dB + per-tile normalize → tile; augment flips/rot90 only (no photometric jitter on SAR).
- **F15 — source-reported baseline:** not found in sources (continuous mission; no benchmark number recorded).
- **Verification 2026-10-10:** not re-checked this pass.

### D02 — Sentinel-2 MSI (Copernicus CDSE) · `[V]` selected
- **Modality:** 13-band optical multispectral.
- **Hazard/task · WS · chapter:** flood extent / burned-area / land context; WS4/WS8; ch 06, 09, 12.
- **Provider:** ESA / Copernicus (CDSE). **Access URL:** https://dataspace.copernicus.eu/.
- **License [as-recorded]:** Copernicus free/open `[V]` (legal-notice PDF itself not fetchable — minor).
- **Size:** continuous mission. **N:** n/a (we index). **Spatial:** global incl. India/Himalaya.
- **Temporal:** continuous mission. **Resolution:** 10/20/60 m by band.
- **Label type:** none intrinsic.
- **Known biases/caveats:** monsoon **cloud cover** is the dominant limitation → pair with SAR
  (optical–SAR fusion, DC-09).
- **Split guidance:** tile + time block CV, same buffer policy as D01.
- **Acquisition status:** [UNVERIFIED — not downloaded]; free registration for download.
- **Consuming model/chapter:** optical–SAR fusion flood head + EO encoder (ch 05/06).
- **F3 — paper/official/mirror:** no owning data-paper recorded → "not found in sources"; official https://dataspace.copernicus.eu/; mirrors AWS `s3://sentinel-s2-l2a`, GEE `COPERNICUS/S2_SR_HARMONIZED`.
- **F8 — load [UNTESTED]:** `pystac_client.Client.open("https://catalogue.dataspace.copernicus.eu/stac").search(collections=["SENTINEL-2"], bbox=..., datetime=...)` (CDSE account); or `openeo`.
- **F12 — preprocess/augment order [HYPOTHESIS, planning]:** L2A surface-reflectance (Sen2Cor if L1C) → cloud/shadow mask (s2cloudless/SCL) → band-select + resample to 10 m → per-band normalize → tile; augment flips/rot90 + mild spectral jitter.
- **F15 — source-reported baseline:** not found in sources.
- **Verification 2026-10-10:** not re-checked this pass.

### D03 — GPM IMERG precipitation (NASA) · `[V]` selected
- **Modality:** satellite precipitation raster. **Hazard/task · WS · ch:** rainfall trigger / nowcast
  covariate; WS1/WS3; ch 06, 08, 12.
- **Provider:** NASA. **Access URL:** https://gpm.nasa.gov/data/imerg (Earthdata/PPS login; Giovanni/GeoTIFF).
- **License [as-recorded]:** NASA open data `[V]`.
- **Size:** continuous product. **N:** n/a. **Spatial:** global 90°N–S (V07). **Temporal:** 2000–present.
- **Resolution:** 0.1°, half-hourly.
- **Label type:** none (covariate).
- **Known biases/caveats:** NASA notes precipitation is **less certain over mountains** and V07 is
  snowfall-deficient → treat Himalayan IMERG as a **noisy covariate** (feeds CR-08 / TSFM-covariate-noise).
- **Split guidance:** temporal block CV; monsoon-season held-out.
- **Acquisition status:** [UNVERIFIED — not downloaded]; needs NASA Earthdata login.
- **Consuming model/chapter:** rainfall/antecedent covariate + nowcasting (ch 06/08).
- **F3 — paper/official/mirror:** official https://gpm.nasa.gov/data/imerg; IMERG algorithm paper not recorded in registry → "not found in sources"; mirror GES DISC / Giovanni.
- **F8 — load [UNTESTED]:** `earthaccess.login(); earthaccess.search_data(short_name="GPM_3IMERGHH", version="07", bounding_box=..., temporal=...)`.
- **F12 — preprocess/augment order [HYPOTHESIS, planning]:** subset region/time → unit handling (mm/hr) → accumulate to event window → regrid to common grid → log1p for skew → temporal-block split (monsoon held-out). *(no image augmentation; covariate raster.)*
- **F15 — source-reported baseline:** not found in sources.
- **Verification 2026-10-10:** not re-checked this pass.

### D04 — SMAP soil moisture (NASA NSIDC) · `[V]` selected
- **Modality:** L-band soil moisture. **Hazard/task · WS · ch:** antecedent-wetness prior; WS1; ch 06, 12.
- **Provider:** NASA NSIDC. **Access URL:** https://nsidc.org/data/smap (Earthdata login; NSIDC/ASF).
- **License [as-recorded]:** NASA open data `[V]`.
- **Size:** continuous. **N:** n/a. **Spatial:** global. **Temporal:** 2015–present. **Resolution:** ~9–36 km.
- **Label type:** none (covariate).
- **Known biases/caveats:** coarse 9–36 km is **weak over steep Himalayan terrain** → use as a regional
  antecedent-wetness prior, **not** a local trigger.
- **Split guidance:** temporal block CV (regional covariate).
- **Acquisition status:** [UNVERIFIED — not downloaded]; needs NASA Earthdata login.
- **Consuming model/chapter:** antecedent-wetness covariate for the geo-physics stack (ch 06).
- **F3 — paper/official/mirror:** official https://nsidc.org/data/smap; owning product paper not recorded in registry → "not found in sources"; access NASA Earthdata / NSIDC / ASF.
- **F8 — load [UNTESTED]:** `earthaccess.search_data(short_name="SPL3SMP_E", version="006", bounding_box=..., temporal=...)`.
- **F15 — source-reported baseline:** not found in sources.
- **Verification 2026-10-10:** not re-checked this pass.

### D05 — ERA5-Land reanalysis (ECMWF/C3S) · `[V]` selected
- **Modality:** reanalysis (met forcing). **Hazard/task · WS · ch:** boundary forcing / downscaling input;
  WS1; ch 06, 12.
- **Provider:** ECMWF / Copernicus C3S. **Access URL:**
  https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land (CDS API; GEE mirror).
- **License [as-recorded]:** **CC-BY** (DOI 10.24381/cds.e2161bac) `[V]` — one of the few clean licenses.
- **Size:** continuous. **N:** n/a. **Spatial:** global. **Temporal:** 1950–present, hourly.
  **Resolution:** 0.1° (~9 km).
- **Label type:** none (forcing).
- **Known biases/caveats:** 9 km smooths Himalayan topography → downscale or use as **boundary forcing**
  (HEC-RAS, arXiv 2507.15614).
- **Split guidance:** temporal block CV.
- **Acquisition status:** [UNVERIFIED — not downloaded]; needs Copernicus CDS account + API key.
- **Consuming model/chapter:** met forcing / downscaling for geo-physics + nowcast (ch 06).
- **F3 — paper/official/mirror:** dataset DOI 10.24381/cds.e2161bac [link-verified 2026-10-10]; owning data-paper (author citation) not carried in registry → "not found in sources"; official https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land; mirror GEE `ECMWF/ERA5_LAND/HOURLY`.
- **F8 — load [UNTESTED]:** `import cdsapi; c=cdsapi.Client(); c.retrieve("reanalysis-era5-land", {..., "format":"grib"}, "out.grib")` — CDS API key; GRIB native [link-verified 2026-10-10].
- **F15 — source-reported baseline:** not found in sources.
- **Verification 2026-10-10:** link resolved? **yes (HTTP 200)** — CC-BY, DOI 10.24381/cds.e2161bac, 0.1°×0.1° (native 9 km), hourly, Jan 1950–present, GRIB, via cdsapi [link-verified 2026-10-10].

### D06 — MODIS (NASA LP DAAC) · `[V]` selected
- **Modality:** optical LST / NDVI / snow-cover. **Hazard/task · WS · ch:** GLOF/seasonal context; WS8;
  ch 06, 12.
- **Provider:** NASA LP DAAC. **Access URL:** https://www.earthdata.nasa.gov/centers/lp-daac
  (Earthdata/AppEEARS/GEE/AWS).
- **License [as-recorded]:** NASA open data `[V]`.
- **Size:** Terra/Aqua continuous. **N:** n/a. **Spatial:** global. **Temporal:** 2000–present.
  **Resolution:** 250 m–1 km.
- **Label type:** none (covariate). **Known biases/caveats:** coarse for local Himalayan features; snow/LST
  products for seasonal context only.
- **Split guidance:** temporal block CV.
- **Acquisition status:** [UNVERIFIED — not downloaded]; needs NASA Earthdata login.
- **Consuming model/chapter:** snow-cover/LST context for GLOF + EO encoder (ch 06).
- **F3 — paper/official/mirror:** official https://www.earthdata.nasa.gov/centers/lp-daac; owning product paper not recorded in registry → "not found in sources"; mirrors GEE `MODIS/061/*`, AWS.
- **F8 — load [UNTESTED]:** `earthaccess.search_data(short_name="MOD10A1"|"MOD11A1"|"MOD13Q1", version="061", bounding_box=..., temporal=...)` or AppEEARS.
- **F15 — source-reported baseline:** not found in sources.
- **Verification 2026-10-10:** not re-checked this pass.

### D07 — ITS_LIVE glacier velocity (NASA/JPL) · `[V]` selected
- **Modality:** glacier surface velocity. **Hazard/task · WS · ch:** GLOF precursor (glacier acceleration);
  WS8; ch 06, 12.
- **Provider:** NASA/JPL (MEaSUREs). **Access URL:** https://its-live.jpl.nasa.gov/ (portal/STAC/Zarr/S3).
- **License [as-recorded]:** NASA open (MEaSUREs) `[V]`.
- **Size:** continuous. **N:** n/a. **Spatial:** global incl. High Mountain Asia. **Temporal:** 1985–present.
  **Resolution:** 120 m.
- **Label type:** none (precursor signal). **Known biases/caveats:** V1 (pre-Apr-2023) needs Earthdata login;
  newer cloud data open.
- **Split guidance:** leave-one-basin-out.
- **Acquisition status:** [UNVERIFIED — not downloaded]; reg for V1.
- **Consuming model/chapter:** GLOF precursor (velocity) head, paired with D15/D11 (ch 06).
- **F3 — paper/official/mirror:** method ref **autoRIFT feature-tracking — Gardner et al. 2018** [link-verified 2026-10-10]; official https://its-live.jpl.nasa.gov/; mirror AWS S3 Zarr (`its-live-data`).
- **F8 — load [UNTESTED]:** via NSIDC STAC / earthaccess [link-verified route]: `earthaccess.search_data(...)`, or open the ITS_LIVE Zarr cube `xr.open_dataset("s3://its-live-data/...", engine="zarr")`.
- **F15 — source-reported baseline:** not found in sources.
- **Verification 2026-10-10:** link resolved? **yes (HTTP 200)** — global, 1985–present, 120 m, NetCDF/Zarr/GeoTIFF, autoRIFT (Gardner et al. 2018), access via NSIDC STAC / earthaccess [link-verified 2026-10-10].

### D08 — NASA Global Landslide Catalog / COOLR · `[V*]` selected
- **Modality:** landslide point-event catalogue. **Hazard/task · WS · ch:** weak/positive event labels;
  WS1/WS8; ch 06, 12.
- **Provider:** NASA. **Access URL:** https://gpm.nasa.gov/applications/landslides/coolr (viewer +
  data.nasa.gov).
- **License [as-recorded]:** NASA open data `[V*]`.
- **Size:** point events. **N:** count **UNVERIFIED** — "~11,000 cited but not verified from an
  authoritative page this session". **Spatial:** global. **Temporal:** multi-year. **Resolution:** point.
- **Label type:** rainfall-triggered landslide point reports.
- **Known biases/caveats:** reporting bias; **not an exhaustive inventory** → use as weak/positive labels.
- **Split guidance:** temporal + leave-one-region-out.
- **Acquisition status:** [UNVERIFIED — not downloaded].
- **Consuming model/chapter:** Indian/global landslide event labels (ch 06/12). *(Duplicated as candidate
  D45 in the WS1b phase table — same source, kept distinct ID.)*
- **F3 — paper/official/mirror:** official https://gpm.nasa.gov/applications/landslides/coolr + data.nasa.gov; owning paper (COOLR/GLC) not carried in registry → "not found in sources".
- **F5 — annotation + annotator:** rainfall-triggered landslide **point reports**; compiled by the NASA GSFC landslide team (GLC) plus open **citizen/COOLR** submissions; reporting-biased, not exhaustive. Count ~11,000 is **[UNVERIFIED]**.
- **F8 — load [UNTESTED]:** `pandas.read_csv(<data.nasa.gov COOLR CSV export>)` (or `requests.get` the open-data API).
- **F15 — source-reported baseline:** not found in sources.
- **Verification 2026-10-10:** not re-checked this pass.

### D12 — Sen1Floods11 · `[V*]` selected
- **Modality:** Sentinel-1 SAR + Sentinel-2 + hand labels. **Hazard/task · WS · ch:** flood segmentation
  (transfer-eval); WS1/WS8; ch 06, 12.
- **Provider:** Cloud to Street (CVPRW 2020). **Access URL:** https://github.com/cloudtostreet/Sen1Floods11
  (open GCS bucket `gs://sen1floods11`, ~14 GB; Radiant/HF copies).
- **License [as-recorded]:** **UNVERIFIED** (open GCS bucket; exact license not on README) `[V*]`.
- **Size:** ~14 GB. **N:** 512² chips; the cited **4,831-chip count is UNVERIFIED**. **Spatial:** 11 events,
  global — **no India event**. **Temporal:** 11 flood events. **Resolution:** S1/S2 native.
- **Label type:** hand-labeled flood water masks (scene-level native split).
- **Known biases/caveats:** no India event → **transfer-eval only**; native split is scene-level (leaky).
- **Split guidance:** **re-split by event** (native scene-level split is leakage-prone).
- **Acquisition status:** [UNVERIFIED — not downloaded].
- **Consuming model/chapter:** flood segmentation + optical–SAR fusion (ch 05/06); transfer stress-test.
- **F3 — paper/official/mirror:** Bonafilia et al., *"Sen1Floods11: a georeferenced dataset to train and test deep-learning flood algorithms for Sentinel-1,"* CVPRW 2020 [link-verified 2026-10-10]; official https://github.com/cloudtostreet/Sen1Floods11; mirror Radiant MLHub / HF copies.
- **F5 — annotation + annotator:** **hand-labeled** flood water masks over Sentinel-1/2 by Cloud to Street analysts [link-verified 2026-10-10]; scene-level native split (leaky).
- **F8 — load [UNTESTED]:** `gsutil -m cp -r gs://sen1floods11 .` [link-verified route].
- **F12 — preprocess/augment order [HYPOTHESIS, planning]:** pair S1/S2 chips → S1 calibrate (+optional speckle), S2 cloud-mask → co-register → normalize → **re-split BY EVENT** (native scene-level split is leaky) → augment flips/rot90.
- **F15 — source-reported baseline:** not found in sources (paper's own numbers not carried in the registry).
- **Verification 2026-10-10:** link resolved? **yes (HTTP 200)** — GitHub cloudtostreet/Sen1Floods11, Bonafilia et al. CVPRW 2020, hand-labeled S1/S2 masks, gsutil download [link-verified 2026-10-10]; exact license + 4,831-chip count still **[UNVERIFIED]**.

### D15 — HMAGLOFDB (High Mountain Asia GLOF DB) · `[D]` selected
- **Modality:** GLOF event inventory. **Hazard/task · WS · ch:** primary GLOF label source; WS8; ch 06, 12.
- **Provider:** fidelsteiner / ICIMOD (ESSD 2023). **Access URL:**
  https://github.com/fidelsteiner/HMAGLOFDB (+ ICIMOD RDS).
- **License [as-recorded]:** **CC BY 4.0 — confirm on release** `[D]` (from a secondary dashboard).
- **Size:** inventory. **N:** **766 GLOFs — UNVERIFIED** (secondary dashboard; confirm on GitHub/ICIMOD).
  **Spatial:** Indian Himalaya / Nepal / Bhutan / Karakoram (highly India-relevant). **Temporal:** 1533–2025
  (v4.0). **Resolution:** event-level.
- **Label type:** GLOF outburst event records.
- **Known biases/caveats:** **count + CC-BY from a secondary source** → confirm before load-bearing use;
  **small-n hazard** — GLOF events are thin in-region.
- **Split guidance:** leave-one-basin-out (small-n caveat; see 04 §leakage).
- **Acquisition status:** [UNVERIFIED — not downloaded].
- **Consuming model/chapter:** GLOF outburst labels, paired with D07 ITS_LIVE + arXiv 2608.12422 (ch 06).
  *(Duplicated as candidate D52-adjacent ICIMOD inventory; this ID is the primary.)*
- **F3 — paper/official/mirror:** **"Database of GLOFs in High Mountain Asia,"** GitHub fidelsteiner/HMAGLOFDB [link-verified 2026-10-10]; registry records an ESSD-2023 paper (exact author/DOI not carried → "not found in sources"); mirror ICIMOD RDS.
- **F5 — annotation + annotator:** GLOF **outburst event records** compiled from literature + remote sensing by the HMAGLOFDB authors (fidelsteiner et al. / ICIMOD). Count 766 and CC-BY come from a secondary dashboard → **[UNVERIFIED]**.
- **F8 — load [UNTESTED]:** `git clone https://github.com/fidelsteiner/HMAGLOFDB` then `pandas.read_csv(<inventory table>)`.
- **F15 — source-reported baseline:** not found in sources.
- **Verification 2026-10-10:** link resolved? **yes (HTTP 200)** — GitHub fidelsteiner/HMAGLOFDB, "Database of GLOFs in High Mountain Asia" [link-verified 2026-10-10]; count + CC-BY still **[UNVERIFIED]** (secondary source).

### D17 — GEOID-Flood · `[D]` selected
- **Modality:** bi-temporal S1 (GRD+RTC) + S2 (L2A) + GLO-30 DEM. **Hazard/task · WS · ch:** primary flood
  training/eval; WS1/WS8; ch 06, 12.
- **Provider:** links-ads (Copernicus EMS). **Access URL:** https://github.com/links-ads/geoid-flood.
- **License [as-recorded]:** per repo — **confirm on fetch** `[D]`.
- **Size:** 14,282 tiles. **N:** 14,282 tiles / 219 events / 65 countries. **Spatial:** 65 countries
  (global). **Temporal:** 219 flood events. **Resolution:** S1/S2/GLO-30 native.
- **Label type:** 3-class flood masks; **EVENT-LEVEL, leakage-safe native split**.
- **Known biases/caveats:** repo license to confirm; its Table 1 catalogues 10 further flood sets.
- **Split guidance:** adopt the native **event-level** split (already leakage-safe).
- **Acquisition status:** [UNVERIFIED — not downloaded].
- **Consuming model/chapter:** PRIMARY flood segmentation + optical–SAR fusion head (ch 05/06).
  *(Duplicated as candidate D132 in the P23 flood table — same dataset.)*
- **F3 — paper/official/mirror:** GEOID-Flood, *"A Large-Scale Multi-Modal Benchmark Dataset for Flood Segmentation,"* GitHub links-ads/geoid-flood [link-verified 2026-10-10]; arXiv 2608.02315 (as recorded in catalogue D132); no mirror recorded.
- **F8 — load [UNTESTED]:** `git clone https://github.com/links-ads/geoid-flood` then follow the repo download script.
- **F15 — source-reported baseline:** not found in sources.
- **Verification 2026-10-10:** link resolved? **yes (HTTP 200)** — GitHub links-ads/geoid-flood, title as above [link-verified 2026-10-10]; repo license still to confirm on fetch.

### D18 — LMHLD (landslide multi-sensor) · `[D]` selected
- **Modality:** 5-sensor multi-source imagery patches. **Hazard/task · WS · ch:** primary landslide-detection
  training; WS1/WS8; ch 06, 12.
- **Provider:** Zenodo DOI 10.5281/zenodo.11424988. **Access URL:** https://doi.org/10.5281/zenodo.11424988.
- **License [as-recorded]:** open-access Zenodo — **confirm per-source sub-licenses** `[D]`.
- **Size:** 25,365 patches. **N:** 25,365 patches / 7 areas. **Spatial:** 7 areas incl. **Gorkha Nepal 2015**
  (Himalayan, in-region-adjacent). **Temporal:** multi-event. **Resolution:** 5 sensors (mixed).
- **Label type:** landslide segmentation/detection patches.
- **Known biases/caveats:** per-source sub-licenses to confirm; mixed-sensor domain shift.
- **Split guidance:** region block CV + val→held-out shift test.
- **Acquisition status:** [UNVERIFIED — not downloaded].
- **Consuming model/chapter:** PRIMARY landslide detection/seg + PEFT adaptation (ch 05/06).
  *(Duplicated as candidate D136 in the P23 landslide table — same dataset.)*
- **F3 — paper/official/mirror:** arXiv 2502.19866 (LMHLD, as recorded in catalogue D136); data DOI 10.5281/zenodo.11424988; owning author citation not carried → "not found in sources".
- **F5 — annotation + annotator:** landslide **segmentation/detection patches**; annotator per source **[UNVERIFIED]**; mixed 5-sensor domain.
- **F8 — load [UNTESTED]:** `zenodo_get 10.5281/zenodo.11424988` or Zenodo API `requests.get`. ⚠ files may require login (see conflict note).
- **F15 — source-reported baseline:** not found in sources.
- **⚠ CONFLICT [link-verified 2026-10-10]:** Zenodo record **11424988** re-fetched on 2026-10-10 resolves to **"GSR2SD"** (Guanting Liu), **6,723 patches across 7 global sites** (Wenchuan 2008, Rio 2011, Gorkha 2015, Jiuzhaigou 2015, Taiwan 2018, Hokkaido 2018, Emilia-Romagna 2023), with **files RESTRICTED (login required)** — this disagrees with the registry's recorded *"LMHLD, 25,365 patches, 5 sensors, 7 areas."* Registry facts are preserved as recorded; the DOI↔name↔count discrepancy and the access restriction are flagged for build-time reconciliation. Gorkha 2015 (Himalayan relevance) is common to both.
- **Verification 2026-10-10:** link resolved? **yes (HTTP 200)** — but as **GSR2SD**, access-restricted; the registry's "LMHLD" fields are **not** independently confirmed this pass.

### D22 — India Flood Inventory – Impacts (IFI) · `[V]` selected
- **Modality:** district-level flood event CSV. **Hazard/task · WS · ch:** PRIMARY Indian flood-event
  label/impact source; WS1/WS3; ch 06, 08, 12.
- **Provider:** HydroSense Lab IIT-Delhi + IMD. **Access URL:** https://zenodo.org/records/11275211
  (+ GitHub hydrosenselab; 3 CSVs, ~1.9 MB).
- **License [as-recorded]:** **CC BY 4.0** `[V]` — clean, verified.
- **Size:** ~1.9 MB (3 CSVs). **N:** district-level flood events. **Spatial:** national (India).
  **Temporal:** 1967–2023. **Resolution:** district-level.
- **Label type:** flood event records + impact targets.
- **Known biases/caveats:** the **single most India-specific verified dataset found**; impact fields are
  reporting-dependent.
- **Split guidance:** temporal + leave-one-region-out.
- **Acquisition status:** [UNVERIFIED — not downloaded].
- **Consuming model/chapter:** Indian flood event labels / impact targets (ch 06/08/12), with D25 discharge.
- **F3 — paper/official/mirror:** IFI v1 — Saharia et al., *India Flood Inventory,* Natural Hazards 2021, DOI 10.1007/s11069-021-04698-6; v2 — arXiv:2405.01602; v3 data — Zenodo record 11275211 (2024); provider HydroSense Lab, IIT Delhi (Manabendra Saharia et al.) [all link-verified 2026-10-10]; mirror GitHub hydrosenselab.
- **F5 — annotation + annotator:** district-level **flood event records + impact targets**, compiled by HydroSense Lab (IIT Delhi) from IMD + government/news reports; impact fields reporting-dependent.
- **F8 — load [UNTESTED]:** `zenodo_get 11275211` (or download then `pandas.read_csv` the 3 CSVs).
- **F15 — source-reported baseline:** not found in sources.
- **Verification 2026-10-10:** link resolved? **yes (HTTP 200)** — Zenodo 11275211 (v3, 2024), CC-BY-4.0, India 1967–2023, Saharia et al.; v1 DOI 10.1007/s11069-021-04698-6, v2 arXiv:2405.01602 [link-verified 2026-10-10].

---

# Part 1b — PROMOTED candidate deep entries (same 16-field schema; STATUS stays `candidate`)

> These four are **not** STATUS=selected (the free-only/selection count stays 13). They are promoted to full
> deep entries because they are load-bearing feeders (EO SSL pretrain, landslide benchmark, FireSmokeNet
> training, AuthenticityNet training). Facts are reproduced from the registry; unknown fields are
> `[UNVERIFIED]`/`[N/A — not downloaded]`. No download/EDA was performed.

### D10 — SSL4EO-S12 · `[V]` candidate (promoted) — EO SSL pretrain / WS1
- **Modality:** S1 GRD + S2 (L1C+L2A) self-supervised corpus (**unlabeled**).
- **Hazard/task · WS · chapter:** SSL pretraining of the EO/InSAR encoder (EODownstream/WS1); ch 05, 06.
- **Provider:** zhu-xlab (TU Munich). **Access URL:** https://github.com/zhu-xlab/SSL4EO-S12 (mediaTUM + HF).
- **License [as-recorded]:** code **Apache-2.0**; data+weights **CC-BY-4.0** `[V]`.
- **Size:** ~1.5 TB raw. **N:** 251,079 locations × 4 seasons. **Spatial:** global incl. Himalaya.
  **Temporal:** 4 seasonal snapshots. **Resolution:** S1/S2 native (10 m).
- **Label type:** NONE (unlabeled SSL corpus). **EDA:** [N/A — data not downloaded].
- **Known biases/caveats:** ~1.5 TB → use the compressed 8-bit variant / regional subset for the Kaggle
  budget; sampling may under-represent some regions.
- **Split guidance:** pretrain-only; downstream eval elsewhere (no leakage into labelled test sets).
- **Acquisition status:** [UNVERIFIED — not downloaded].
- **Consuming model/chapter:** SSL pretraining of the EO encoder (ch 05/06).
- **F3 — paper/official/mirror:** owning data-paper not carried in registry (repo-only) → "not found in
  sources"; official GitHub zhu-xlab/SSL4EO-S12; mirror mediaTUM + HuggingFace.
- **F8 — load [UNTESTED]:** `from datasets import load_dataset; ds = load_dataset("<HF SSL4EO-S12 mirror>", streaming=True)` (stream to avoid ~1.5 TB local pull).
- **F15 — source-reported baseline:** not found in sources (SSL corpus; no task metric recorded).
- **Verification 2026-10-10:** not re-checked this pass.

### D09 — Landslide4Sense · `[V*]` candidate (promoted) — landslide benchmark / WS1
- **Modality:** 14-band multispectral patches (S2 B1–B12 + ALOS slope + DEM).
- **Hazard/task · WS · chapter:** landslide-segmentation benchmark (EODownstream/WS1); ch 05, 06, 12.
- **Provider:** IARAI (original site **dead**) → HF `ibm-nasa-geospatial` mirror + GitHub.
  **Access URL:** https://huggingface.co/datasets/ibm-nasa-geospatial/Landslide4sense.
- **License [as-recorded]:** **UNVERIFIED** — no license on the HF card `[V*]` → candidate until confirmed.
- **Size:** — (not recorded). **N:** 3,799 train / 245 val / 800 test patches, 128². **Spatial:** global
  benchmark. **Temporal:** benchmark snapshot. **Resolution:** S2 native + DEM/slope.
- **Label type:** pixel-level landslide masks (annotator per source — **[UNVERIFIED]**). **EDA:** [N/A — data not downloaded].
- **Known biases/caveats:** no license on card; original IARAI host dead → rely on mirrors.
- **Split guidance:** region-block CV + val→held-out shift test.
- **Acquisition status:** [UNVERIFIED — not downloaded].
- **Consuming model/chapter:** landslide detection/seg + PEFT adaptation (ch 05/06).
- **F3 — paper/official/mirror:** named in arXiv 2403.10127 (per catalogue D137); owning challenge paper
  (Landslide4Sense / IARAI) not carried in registry → "not found in sources"; mirror HF + GitHub.
- **F8 — load [UNTESTED]:** `from datasets import load_dataset; ds = load_dataset("ibm-nasa-geospatial/Landslide4sense")`.
- **F15 — source-reported baseline:** not found in sources.
- **Verification 2026-10-10:** not re-checked this pass.

### D36/D117 — PYRONEAR-2025 · `[D]` candidate (promoted) — FireSmokeNet CCTV training / WS4
> Chosen over D37 D-Fire and D35 FIgLib as the **best-documented** fire-CCTV set in the registry (most
> complete recorded facts: host, counts, annotations, arXiv). This is **FireSmokeNet's training data**;
> previously had no deep entry.
- **Modality:** camera-network images + video (fixed-tower early-wildfire).
- **Hazard/task · WS · chapter:** FireSmokeNet CCTV smoke/fire detection training (WS4); ch 09.
- **Provider:** Pyronear project (open-source). **Access URL:** https://pyronear.org ; arXiv:2402.05349.
- **License [as-recorded]:** open-source project — **confirm** (UNVERIFIED) `[D]`.
- **Size:** — . **N:** ~50k images / ~150k annotations / 640 fires (**"named"** — from a citing abstract,
  not the owner's page). **Spatial:** multi-site camera networks (France/Europe-centric). **Temporal:**
  real-world camera deployments. **Resolution:** camera-native RGB.
- **Label type:** bounding-box smoke/fire annotations (annotator per source — **[UNVERIFIED]**). **EDA:** [N/A — data not downloaded].
- **Known biases/caveats:** Europe-centric camera networks → domain shift vs Indian CCTV; counts are "named".
- **Split guidance:** by-site / by-fire hold-out to avoid fixed-camera leakage.
- **Acquisition status:** [UNVERIFIED — not downloaded].
- **Consuming model/chapter:** FireSmokeNet CCTV detector (ch 09, WS4); `deep/fire_cnn.py`.
- **F3 — paper/official/mirror:** arXiv:2402.05349 (PYRONEAR-2025, as recorded); full author/title/venue not
  carried in registry → cite arXiv ID as recorded; official pyronear.org.
- **F8 — load [UNTESTED]:** `git clone <pyronear-2025 repo>` or `load_dataset("<HF pyronear mirror>")` (host to confirm).
- **F15 — source-reported baseline:** not found in sources (no baseline number carried in the registry).
- **Verification 2026-10-10:** not re-checked this pass.

### D68/D159 — FaceForensics++ (FF++) · `[D]` candidate (promoted) — AuthenticityNet training / WS2 · **ACCESS BLOCKED (EULA)**
> Chosen over D70 DFDC as AuthenticityNet's primary forensic set; **both are EULA-gated**. Documented here
> as **BLOCKED until a signed agreement is in place** — no download attempted or possible this pass.
- **Modality:** face-manipulation video — DeepFakes / Face2Face / FaceSwap / NeuralTextures, at c0/c23/c40
  compression levels.
- **Hazard/task · WS · chapter:** AuthenticityNet deepfake forensic training (WS2); ch 07.
- **Provider:** TUM (Technical University of Munich). **Access URL:** FF++ request form / page (D159 context
  arXiv:2107.02045).
- **License [as-recorded]:** **research-only EULA — signed access request** `[D]`.
- **Size:** large (standard). **N:** not recorded exactly. **Spatial/Temporal:** n/a (lab-generated face
  video). **Resolution:** video-native at 3 compression levels. **EDA:** [N/A — data not downloaded].
- **Label type:** real/fake per-video + manipulation-method labels (generated by the FF++ authors' pipelines).
- **Known biases/caveats:** identities reused across manipulations; cross-dataset generalization weak;
  in-distribution accuracy **overstates** deployment → **cross-generator + degraded** eval mandatory (ch 07).
- **Access / EULA path (BLOCKED):** submit the FF++ request form / signed EULA to TUM → receive a download
  script/token → only then download. **No download without approval.** Face data → consent/privacy
  constraints; method development only, **no deceptive media created** (ch 14).
- **Acquisition status:** **[BLOCKED — EULA not signed; not downloaded]**.
- **Consuming model/chapter:** AuthenticityNet (ch 07, WS2); `deep/deepfake_net.py`.
- **F3 — paper/official/mirror:** named in arXiv 2107.02045 (per registry D159); original FF++ paper
  (Rössler et al., ICCV 2019) not carried in registry → "not found in sources"; mirror none (EULA-gated).
- **F8 — load [UNTESTED, BLOCKED]:** pseudo-code only — `# after EULA approval: python download_ffpp.py --server <token> --compression c23 --type videos`; cannot be scripted without the issued token.
- **F15 — source-reported baseline:** not found in sources.
- **Verification 2026-10-10:** not re-checked this pass (access EULA-gated).

---

# Part 2 — CANDIDATE pool (compact, grouped by modality)

Every row is `[D]`/`[V*]` **candidate** (not selected) unless noted. Licenses are **as-recorded /
INDICATIVE / UNVERIFIED**; sizes/N are source-reported, not measured; no download tested. Some datasets
appear under more than one ID because successive discovery phases re-listed them — flagged with ↔.

## 2.1 Fire / smoke — CCTV·UAV·satellite imagery (WS4, WS7a, WS1a)
| ID | Name | Modality | Size/N (recorded) | License (as-recorded) | Source |
|----|------|----------|-------------------|-----------------------|--------|
| D27 | Multiple-Categories Visual Smoke DB | smoke images | 70,196 imgs | UNVERIFIED | 2208.00210 |
| D35 ↔D113 | FIgLib (Fire Ignition Library) | fixed-cam smoke images | ~25k | public (not confirmed) | 2112.08598 |
| D36 ↔D117 | PYRONEAR-2025 | camera-network img+video | ~50k img/150k ann/640 fires | open-source (confirm) | 2402.05349 |
| D37 ↔D120 | D-Fire | fire+smoke bbox images | ~21k (named) | MIT (not confirmed) | 2510.10108 |
| D38 | Multi-Scene FSD benchmark | fire/smoke images | multi-scene | not stated | 2410.16631 |
| D39 ↔D116 | AusSmoke / MultiNatSmoke | smoke segmentation | "order-of-mag larger" | public/not stated | 2604.23542 |
| D40 | SmokeBench (desmoking) | surveillance imagery | 0–15 min post-ignition | not stated | 2509.12701 |
| D41 ↔D115 | GWFP (Global Wildfire Prevention) | image+video | large | "open-source" / upon acceptance | 2606.10174 |
| D42 | FLAME | aerial RGB+thermal | pile-burn set | IEEE DataPort terms | 2012.14036 |
| D43 | WIT-UAS | IR thermal wildland-fire | — | not visible | 2312.09159 |
| D44 | Fire360 | degraded 360° fire video | indoor | not visible | 2506.02167 |
| D107 | ECA9 industrial-accident video | accident video (incl. fire) | semi-sup | not stated | 2405.14506 |
| D108 | Uttarakhand forest-fire imagery | India fire imagery | region set | not stated | 2410.06743 |
| D114 | SKLFS-WildFire Test | real images | "largest real testset" | free (code+data) | 2311.10116 |
| D118 | The Wildfire Dataset | hi-res images | 10.74 GB | free (public) | 2505.17395 |
| D119 | FASDD (Flame & Smoke Detection) | detection images | large (named) | free/open (reported) | 2501.08639 |
| D121 | AFSE (Aerial Fire & Smoke) | aerial images | — | research dataset | 2501.08639 |
| D122 | USTC_SmokeRS | MODIS 3-band images | — | free (research) | 2310.01711 |
| D123 | Landsat_Smk | Landsat 5/8 6-band | — | free (research) | 2310.01711 |

**Zero-shot fire evaluation references (WS4-ZS — leakage/label-flawed, EVAL-only, not training):**
| ID | Name | Modality | Size/N | License | Documented flaw |
|----|------|----------|--------|---------|-----------------|
| D99 | WildFireCan-MMD | X posts img+text | 12 themes | not visible | Canada-specific, UGC≠CCTV |
| D100 | AI4Fire | 5 wildfire tasks | 67 aerial frames (mislabeled) | not visible | leakage; ZS loses to trivial |
| D101 | California Wildfire PM2.5 | PM2.5 TS | 12 yr/1,375 inc/79 sites | not visible | TS not imagery; tail-unstable |

## 2.2 Satellite active-fire / burned-area / fire-spread (WS1a, WS1b, WS5, WS8)
| ID | Name | Modality | Size/N | License | Source |
|----|------|----------|--------|---------|--------|
| D31 | NIST FDS Validation Guide + suite | fire experiment data | plume/HGL/species | US-Gov PD / BSD | pages.nist.gov/fds-smv |
| D32 | NIST Fire Calorimetry DB | measured HRR curves | furniture/room | US-Gov PD | nist.gov/el |
| D33 | NIFC/GeoMAC fire perimeters | fire-front perimeters | multi-fire | US public (confirm) | 2302.04960/2510.09708 |
| D34 | WRF-SFIRE / SPARK sims (cWGAN) | fire-spread sims | coupled-model | UNVERIFIED | 2212.00970/2309.02615 |
| D102 | PyroStack US wildfire | multi-band hourly TS | 6,994 fires 2012–24 | not stated | 2609.36315 |
| D103 | FireGen Monte-Carlo sim | statistical fire-spread | N. California | not stated | 2610.07431 |
| D124 | WildfireSpreadTS (WSTS) | multi-temporal datacubes | multi-year/fire | free/open | ref. 2603.09042 |
| D125 | MOD14 / VNP14 fire masks | MODIS+VIIRS fire raster | multi-region | free (NASA) | 2503.08580 |
| D126 | CaBuAr (California Burned Areas) | S2 L2A pre/post | CA since 2015 | free/open | 2401.11519 |
| D127 | MultiEarth Amazon | Sentinel/Landsat/VIIRS/MODIS | curated | open | 2307.04916 |
| D128 | EFFIS hotspot crossref (Europe) | MODIS+VIIRS+S3+LULC | large (Europe) | public EFFIS/Copernicus | 2308.02508 |

## 2.3 Flood / inundation — SAR + optical (WS1, WS1b, WS8)
| ID | Name | Modality | Size/N | License | Source |
|----|------|----------|--------|---------|--------|
| D19 | UFO Urban Flood Observations | PlanetScope chips | 215 chips / 14 events / 3 m | per paper (verify) | 2604.23066 |
| D129 ↔D12 | Sen1Floods11 | S1 SAR + labels | 11 events, global | free/open | ref. 2307.07123 |
| D130 | SEN12-FLOOD | S1 SAR + S2 optical | multi-event | free/open | 2307.07123 |
| D131 | C2S-MS Floods | SAR + multispectral | multimodal | free (reported) | 2601.00123 |
| D132 ↔D17 | GEOID-Flood | bi-temporal S1+S2+DEM | 14k tiles/219 events/65 ctry | free/open (Copernicus EMS) | 2608.02315 |
| D133 | S1GFloods | Sentinel-1 SAR pairs | 46 events 2015–22 | free/open | 2306.00704 |
| D134 | Kuro Siwo | SAR GRD+SLC multi-temporal | 43 events, 338B m² | free/open (NeurIPS D&B) | 2311.12056 |
| D135 | Citizen-Science Flood Extent | S1 C-band SAR | ~36,000 km² (US+BD) | free/open | 2311.09276 |

## 2.4 Landslide (WS1, WS1b)
| ID | Name | Modality | Size/N | License | Source |
|----|------|----------|--------|---------|--------|
| D09 ↔D137 | Landslide4Sense | 14-band multispectral patches | 3,799/245/800, 128² | **UNVERIFIED (no license on card)** | HF/GitHub |
| D20 | GDCLD (coseismic) | global coseismic LS seg | global | UNVERIFIED | 2604.16663 |
| D23 | Kerala-2018 landslide inventory | landslide polygons | 2018 Kerala | UNVERIFIED | ITC Utwente |
| D24 | Bhuvan/NRSC-ISRO inventories | landslide polygons (India) | Atlas; UK 2013; J&K; Sikkim; Wayanad | UNVERIFIED (ISRO terms) | bhuvan-app1.nrsc.gov.in |
| D26 | Landslide Reference S1&S2 (DLR/GFZ) | S1+S2 | worldwide 2015+ (6.2 GB) | **CC BY 4.0** | Zenodo 15421843 |
| D45 ↔D08 | NASA GLC/COOLR | landslide point inventory | global | NASA open (indic.) | gpm.nasa.gov |
| D46 | GSI Landslide / BHUKOSH | India LS inventory + geology | national | GSI/Govt-India terms | bhukosh.gsi.gov.in |
| D136 ↔D18 | LMHLD | 5 sensors, 7 areas | 25,365 patches | free/open | 2502.19866 |
| D137 ↔D09 | Landslide4Sense | multispectral | benchmark | free/open | 2403.10127 |
| D138 | Bijie landslide | optical | benchmark | free (research) | 2403.10127 |
| D139 | PILD (event-isolated) | 4 sources, 55 events | 7,890 test | free/open | 2608.09325 |
| D140 | **MMLSv2 — MARTIAN (out of scope)** | 7-band (RGB/DEM/slope/thermal) | 664+276 | free/open | 2602.08112 |

## 2.5 InSAR / ground deformation (WS1, WS1b, WS8)
| ID | Name | Modality | Size/N | License | Source |
|----|------|----------|--------|---------|--------|
| D11 | GLOFNet (multimodal GLOF) | S2+ITS_LIVE+MODIS | Shisper/Karakoram | **UNVERIFIED (download+license)**; paper CC BY-NC-ND 4.0 | 2510.10546 |
| D21 ↔D142 | Thalia | InSAR+topo+atmos datacubes | 38 cubes, 7 yr | per repo (verify) | 2505.17782 |
| D141 | Hephaestus | S1 interferograms (ann.) | 19,919 ifg / 216,106 patches / 44 volcanoes | free/open | 2204.09435 |
| D142 ↔D21 | Thalia | InSAR+topo+atmos datacubes | 38 cubes, 7 yr | free/open | 2505.17782 |

## 2.6 Air quality / PM2.5 / gas sensors (WS7, WS7a, WS7b, WS8)
| ID | Name | Modality | Size/N | License | Source |
|----|------|----------|--------|---------|--------|
| D28 | UCI Gas Sensor Array Drift | MOX e-nose TS | drift benchmark | CC BY 4.0 (confirm) | archive.ics.uci.edu/224 |
| D29 | Low-Cost Indoor AQ Calibration | AQ sensor TS | 6-mo, 5 locations | UNVERIFIED | 2610.11236 |
| D30 | RESPIRE India CO calibration | CO calibration code/data | multi-site/season | UNVERIFIED | github purushottamkar/respire |
| D47 | IMD rainfall / gridded | rainfall station+grid | India | **IMD policy — often restricted/paid** | mausam.imd.gov.in |
| D95/D106 | AQ-SDR | low-cost + reference AQ TS | 23,737 stations | not stated / "public when published" | 2508.02724 |
| D96 | SensEURCity (Antwerp) | collocated AQ sensors | 9 ref + 34 LCS | not stated (public) | 2510.05646 |
| D97 | SEA-HAZEMON | distributed haze nodes | SE-Asia | not visible | 2407.09117 |
| D98 | LoRa 2.4 GHz ToF ranging (+T/RH) | ranging + T/RH TS | 3×3 grid / 400 m² / 3 wk | not stated | 2509.23125 |
| D110 | TRAQID + PM25Vision | regional multimodal AQI | regional | not stated | 2605.16375 |
| D143 | KnowAir (PM2.5-GNN) | station TS + meteo | China | free/open | 2002.12898 |
| D144 | TAP (Tracking Air Pollution China) | sat+ground+model | since 2000, national | free/public | 2103.06520 |
| D145 | Bihar low-cost PM2.5 network | sensor TS + meteo | 511 loc, 1 yr, India | reported public | 2412.13935 |
| D146 | California Wildfire PM2.5 | hourly station TS | 12 yr / 1,375 inc / 79 sites | from EPA AQS (public) | 2607.07951 |

## 2.7 Seismic / earthquake + anomaly-detection benches (WS8)
| ID | Name | Modality | Size/N | License | Source |
|----|------|----------|--------|---------|--------|
| D147 | CEED (California EQ Event) | waveforms+picks+polarity | 2000–2024 | free/open | 2502.11500 |
| D148 | STEAD (Stanford EQ) | 3-comp waveforms | millions (named) | free/open | 2408.06629 |
| D149 | POSEIDON | event catalog + energy | 2.8M events, 30 yr | free/open | 2601.02264 |
| D150 | MultiSeismo | waveforms+intensity maps | 16K+ events 2010–23 | free/open (reported) | 2605.26320 |
| D55 | UCF-Crime | surveillance VAD video | — | not visible | WS-VAD |
| D56 | XD-Violence | multimodal VAD | — | not visible | WS-VAD |
| D57 | ShanghaiTech/Avenue/Ped | VAD video | — | not visible | VAD |
| D58 | SMD (Server Machine) | multivariate TS | — | not visible | OmniAnomaly |
| D59 | NASA SMAP / MSL | spacecraft telemetry TS | — | US-gov public (indic.) | NASA telemetry |
| D60 | NAB (Numenta) | streaming TS | — | AGPL-3.0 (confirm) | github numenta/NAB |
| D61 | UCR Anomaly Archive | TS | single-anomaly | not visible | Keogh/UCR |
| D62 | TSB-AD / TSB-drift | TS bench (VUS-PR) | large | not visible | TSB-AD |
| D63 | SWaT / WADI / BATADAL | CPS water-treatment TS | — | iTrust request EULA | iTrust |
| D64 | PSM | pooled server metrics | — | not visible | eBay |
| D65 | TinyMLperf (anomaly task) | MCU anomaly | ToyADMOS-style | Apache-2.0 (indic.) | MLCommons |
| D66 | UrbanSound8K | acoustic | — | CC BY-NC 3.0 (indic.) | urbansounddataset |
| D67 | OddBench | tabular outlier (audit) | 686–690 sets | not visible | 2609.29580 |

## 2.8 Crisis social-media / multimodal disaster (WS2, WS3)
| ID | Name | Modality | Size/N | License | Source |
|----|------|----------|--------|---------|--------|
| D16 | CrisisMMD / CrisisNLP | text + images | 7 events, ~16k tweets/18k imgs | UNVERIFIED ("Terms of use") | crisisnlp.qcri.org |
| D111 | UrduFake@FIRE2020 | Urdu fake-news text | 900/400 articles | shared-task terms | 2207.12406 |
| D112 | GeoCoV19 | geolocated tweets | 524M+ (IDs) | platform ToS (ID-only) | 2005.11177 |
| D151 | CrisisBench / CrisisNLP | tweets | 166.1k+141.5k, 8 sets | free/open | 2004.06774 |
| D152 | CrisisMMD | text + images | multi-disaster | free/open | 1805.00713 |
| D153 | MEDIC | images (multi-task) | 71,198 | free/open | 2108.12828 |
| D154 | GeoCoV19 | geolocated tweets | 524M+, 90 days (IDs) | free/open | 2005.11177 |
| D155 | HumAID / HUMAID-NER | tweets (+NER) | 60,000 / ~175k spans | free/open | 2609.16964 |
| D156 | TSEqD (Turkey-Syria EQ) | text+images+social | 10,352 (single event) | reported released | 2410.08814 |
| D157 | DisasterVQA | images + Q/A | 1,395 img / 4,405 Q/A | free/open | 2601.13839 |

## 2.9 Deepfake / synthetic media — forensic (WS2)
| ID | Name | Modality | Size/N | License (as-recorded) | Source |
|----|------|----------|--------|-----------------------|--------|
| D68 | FaceForensics++ (FF++) | face-manip video | DF/F2F/FS/NT + c0/c23/c40 | research-only EULA (indic.) | FF++ |
| D69 | Celeb-DF (v2) | face-swap video | — | research-only EULA (indic.) | Celeb-DF |
| D70 | DFDC | face video | large | DFDC EULA (indic.) | Meta/Kaggle |
| D71 | WildDeepfake | in-the-wild video | small/noisy | research-only (indic.) | WildDeepfake |
| D72 | DF40 | 40 forgery methods | cross-generator | research-only (indic.) | DF40 |
| D73 | GenImage | real-vs-AI image | large | not visible | GenImage |
| D74 | DiffusionForensics | diffusion image | — | not visible | DIRE repo |
| D75 | ASVspoof (2019/2021/5) | spoof speech | — | ODC/research (indic.) | ASVspoof |
| D76 | NewsCLIPpings | OOC multimodal | — | research (indic.) | NewsCLIPpings |
| D77 ⚑ | CCDF (surveillance deepfakes) | video | 1,840 vids (460 real/1,380 gen) | not stated | 2610.07939 |
| D78 | DF26 | T2V/I2V video | 271 real/2,420 synth | not stated | 2609.07369 |
| D79 | BabelFake | AV clips | 399k, 496 speakers, 5 EU langs | ethically-sourced (indic.) | 2610.06339 |
| D80 | PhysForensics-Bench | audio-video | 9 scene families | not stated | 2609.15562 |
| D81 | MAD benchmark | full-body motion deepfake | 1.5M frames, 6 gen | not stated | 2610.11496 |
| D82 | MIC-Bench | image-claim OOC | 8,812 instances | released (indic.) | 2609.33441 |
| D83 | NepOOC | Nepali-English OOC | 1,090 pairs | public (indic.) | 2608.19212 |
| D84 | WildFakeBench | micro-video | 10k+ real | released (indic.) | 2603.25423 |
| D85 | Weibo26 | image+text news | native+generated | not stated | 2609.36850 |
| D86 | SLED-1400 | evidence photos | 200 real/1,200 synth, 6 T2I | study dataset (indic.) | 2606.07613 |
| D87 | Audio Neural Codec-Spoof | audio | 7 codecs | not stated | 2610.07216 |
| D88 | Soft-Bindings C2PA | watermark bench | 25 img/7 audio/7 video + 35 fp | open-licence (audited) | 2610.04151 |
| D158 | DFDC | face video | preview 5K (full larger) | **EULA — actor-likeness** | 1910.08854 |
| D159 | FaceForensics++ | face video | large (standard) | **EULA — signed request** | 2107.02045 |
| D160 | FakeAVCeleb | video + synth audio | multi-ethnicity | **access-on-request (restricted)** | 2108.05080 |
| D161 | DeepFake MNIST+ | video | 10,000 vids, 10 actions | free (reported) | 2108.07949 |
| D162 | CtrSVDD | singing-voice audio | 47.64h bona + 260.34h fake | public | 2406.02438 |
| D163 | Codecfake | codec deepfake audio | 7 codec methods | free/open (reported) | 2406.08112 |
| D164 | AUDETER | deepfake audio (open-world) | 4,500+ h, 3M clips | free/open | 2509.04345 |

## 2.10 SSL pretraining corpora + remaining support sets
| ID | Name | Modality | Size/N | License | Source / role |
|----|------|----------|--------|---------|---------------|
| D10 | SSL4EO-S12 | S1+S2 SSL corpus (unlabeled) | 251,079 locs ×4 seasons (~1.5 TB) | code Apache-2.0; **data CC-BY-4.0** | primary SSL pretrain; `[V]` |
| D13 | BigEarthNet v2 (reBEN) | S1+S2 patches | 549,488 (~110 GiB) | **CDLA-Permissive-1.0** | Europe-only pretrain/transfer; `[V]` |
| D14 | EuroSAT | 13-band multispectral | 27,000 imgs, 10 cls | **MIT** | Europe-only sanity/worst-group fixture; `[V]` |

## 2.11 Hydrology / DEM / soil + alerting-network + RL-sim support
| ID | Name | Modality | Size/N | License | Source |
|----|------|----------|--------|---------|--------|
| D25 | INDOFLOODS | station discharge flood events | India | UNVERIFIED | Zenodo 14584654 |
| D48 | NASA GPM IMERG | precipitation | global | open (NASA EOSDIS) | gpm.nasa.gov |
| D49 | CHIRPS rainfall | gauge+satellite rainfall | quasi-global | public domain | chc.ucsb.edu |
| D50 | SRTM DEM | DEM | 30/90 m | public domain (USGS) | earthexplorer.usgs.gov |
| D51 | ALOS AW3D30 / GLO-30 DEM | DEM | 30 m | attribution (JAXA/Copernicus) | eorc.jaxa.jp |
| D52 | ICIMOD HKH glacial-lake/GLOF | glacial lakes + GLOF events | Himalaya | ICIMOD open/attribution | rds.icimod.org |
| D53 | CWC / India-WRIS | discharge + stage | India | **Govt-India (partly restricted)** | indiawris.gov.in |
| D54 | UNSODA | unsaturated soil hydraulic DB | θ(ψ),K(θ) | public domain | ars.usda.gov |
| D89 | ns-3 LoRaWAN reference | sim configs | PDR/throughput | GPLv2 (indic.) | 2009.09503 |
| D90 | FAST-LoRa | analytical model/code | — | not stated | 2507.23342 |
| D91 | Meshtastic link-budget | RF path measurements | per-SF preset | not stated | 2605.17063 |
| D92 | Meshtastic campus RSSI/SNR | RF field logs | n=62 packets | not stated | 2605.20379 |
| D93 | CRAWDAD traces | wireless/mobility traces | heterogeneous | per-dataset EULA | CRAWDAD |
| D94 | CAP alert feed archives | CAP messages | — | per-source (gov) | public CAP feeds |
| D104 | Ctrl-CWM crowd world-model | crowd sim | — | not stated | 2610.09438 |
| D105 | cinemere/evacuation | evacuation env | small-scale | not stated (open) | 2509.19972 |
| D109 | WFDroneBench | risk maps + placement scenarios | 7,746 scenarios | not stated | 2609.11829 |

> **Duplicate IDs across phases (same underlying dataset, kept distinct for registry traceability):**
> D08↔D45 (NASA GLC/COOLR), D12↔D129 (Sen1Floods11), D17↔D132 (GEOID-Flood), D18↔D136 (LMHLD),
> D09↔D137 (Landslide4Sense), D21↔D142 (Thalia), D35↔D113 (FIgLib), D37↔D120 (D-Fire),
> D36↔D117 (PYRONEAR-2025), D39↔D116 (AusSmoke/MultiNatSmoke), D41↔D115 (GWFP), D16↔D152 (CrisisMMD),
> D70↔D158 (DFDC), D68↔D159 (FaceForensics++), D95↔D106 (AQ-SDR). The master table in
> [04_DATASETS.md](<04_DATASETS.md>) lists all 164 IDs including these re-listings.

References for every arXiv ID → chapter [19_REFERENCES_FULL.md](<19_REFERENCES_FULL.md>).
