# DATA_SOURCES.md — TRINETRA/HIMKAVACH 3D geo-visualization (Phase-1, agent R3)

Verified data-acquisition plan for a fully-3D CesiumJS visualization of the
TRINETRA/HIMKAVACH Himalayan disaster + wildfire early-warning project.

- **Accessed / verified date:** 2026-10-10 (all "HTTP nnn" are live `web_fetch` results this session).
- **Verification honesty rule (§0.5):** every "verified accessible" cell below is a real HTTP response I
  obtained today. Where a host would not respond to `web_fetch`, or I relied on documentation rather than a
  live fetch, the cell says **UNVERIFIED** with the reason. No identifier, resolution, date, or coverage here
  is invented.
- **Environment constraints honored:** rendering is in the user's browser → imagery is streamed live via
  tile/WMTS/XYZ or fetched per-tile as COGs from STAC; `web_fetch` here only confirmed small JSON/XML/CSV
  metadata, not large rasters. CesiumJS is the renderer. Esri World Imagery is a *live* basemap only
  (`exportTilesAllowed:false`). NASA FIRMS needs a free MAP_KEY.
- Cross-referenced with the project registry: `DATASETS.md` (D01 Sentinel-1, D02 Sentinel-2, D05 ERA5-Land,
  D06 MODIS, D07 ITS_LIVE, D48 GPM IMERG, D49 CHIRPS, D50 SRTM, D51 Copernicus GLO-30/AW3D30, D125 MOD14/
  VNP14 FIRMS) and `DATASETS_CATALOGUE.md` (D125 active-fire, D128 EFFIS). D-IDs are referenced in the table.

---

## 1. AOI DECISION

### PRIMARY AOI — Uttarakhand Himalaya pre-monsoon forest fires, 2021 season (on-theme HIMKAVACH)
- **Where:** Garhwal + Kumaon mid-hill forest belt, Uttarakhand, India (chir-pine forest, the classic Indian
  Himalayan fire landscape).
- **Bounding box (lon/lat, EPSG:4326):** `78.5, 29.5, 80.2, 30.8`
  (W 78.5°E, S 29.5°N, E 80.2°E, N 30.8°N). Suggested cinematic focus sub-scene around Nainital–Pauri
  (~29.4–29.9°N, 79.3–79.8°E).
- **Dates:** fire season 2021-04-01 → 2021-06-30; peak activity ~2021-04-25 → 2021-05-12 (pre-monsoon, before
  SW-monsoon onset ends the fire window).
- **Why this AOI:**
  1. **On-theme on both axes** — it is simultaneously *Himalayan India* and a *wildfire* event, which is the
     core HIMKAVACH early-warning use-case (ties `DATASETS.md` D108 "Uttarakhand forest-fire imagery").
  2. **Open-data coverage is complete here:** Sentinel-2 L2A (10 m) has had S2A+S2B 5-day revisit since 2017
     over MGRS tiles 44RNR/44RNS/44RPR/44RPS (verified the S2 L2A collection resolves below); NASA FIRMS
     VIIRS 375 m + MODIS 1 km active-fire detections are dense over Uttarakhand every pre-monsoon season;
     Copernicus DEM GLO-30, ESA WorldCover, OSM, WorldPop, GHSL, ERA5-Land all have full global coverage of
     this box (all verified below).
  3. Steep relief (≈ 500 m valleys to > 3000 m ridgelines) makes the 3D terrain layer visually meaningful.
- **Honest caveat:** pre-monsoon haze/cloud can degrade individual S2 scenes → the app should pick a
  low-cloud S2 date from the STAC search and pair with the FIRMS hotspot layer and the SAR/true-color layers.

### FALLBACK AOI — January 2025 Los Angeles wildfires (Palisades + Eaton) (data-richest off-theme option)
- **Where:** Los Angeles County, California, USA (Palisades Fire ~34.08°N, −118.55°E; Eaton Fire ~34.19°N,
  −118.13°E).
- **Bounding box (lon/lat):** `-118.75, 33.90, -118.00, 34.30`.
- **Dates:** ignition 2025-01-07; main growth 2025-01-07 → 2025-01-31.
- **Why a fallback here (justified per the task's "richer open data" allowance):** this event adds a layer
  the Indian AOI cannot — **authoritative historical fire perimeters** (US NIFC InteragencyFirePerimeter
  service, verified HTTP 200 below) plus very dense FIRMS/VIIRS detections, abundant low-cloud S2/Landsat
  scenes, and sub-metre Esri imagery. Use it only if the pipeline needs a perimeter-polygon layer or a known
  clear-sky scene to de-risk the demo; it is **off-theme** (urban, non-Himalayan) so it is the fallback, not
  the primary.

### Note — on-theme GEOHAZARD alternative (for the GLOF/landslide thread, not fire)
If the storyboard wants to show the **TRINETRA GLOF/landslide** side instead of fire, use the **Chamoli
(Rishiganga–Dhauliganga) rock-ice avalanche + flood, 2021-02-07**, Uttarakhand: bbox `79.4, 30.2, 80.0,
30.6`, center ~30.38°N, 79.73°E. It has excellent Sentinel-2, Sentinel-1 SAR (GRD), Copernicus DEM GLO-30 and
ITS_LIVE (D07) coverage and ties `DATASETS.md` D15 HMAGLOFDB / D18 LMHLD. **FIRMS is N/A for this event (no
fire)** — stated honestly; it is offered as a geohazard-layer AOI, not as a fire AOI.

---

## 2. VERIFIED SOURCES TABLE (for the AOIs above)

Columns: source | product / dataset ID (+ project D-ID) | access method | native resolution | temporal
coverage | format | license (short) | verified accessible 2026-10-10? (yes/no + how).

| Source | Product / ID | Access method | Native res | Temporal | Format | License (short) | Verified 2026-10-10? |
|--------|--------------|---------------|-----------|----------|--------|-----------------|----------------------|
| **Sentinel-2 L2A** (optical, D02) | `sentinel-2-c1-l2a` (also `sentinel-2-pre-c1-l2a`) via Earth Search STAC | STAC search → per-band Cloud-Optimized GeoTIFF (XYZ via titiler in-browser) | 10 m (B2/3/4/8); 20 m; 60 m | 2015-06-27 → present (S2A/S2B) | COG GeoTIFF | Copernicus free/open ("proprietary" ESA legal notice; free to use w/ attribution) | **YES** — `GET earth-search.aws.element84.com/v1/collections` HTTP 200; collection + 13-band item_assets returned |
| **Sentinel-2 cloudless** basemap | EOX "s2cloudless" (e.g. `s2cloudless-2020`) | WMTS / XYZ (in-browser) | ~10 m (annual mosaic) | annual mosaics (2016–2022 publ.) | PNG/JPEG tiles | CC-BY-4.0 (EOX / Sinergise; attribution required) | **NO** — `tiles.maps.eox.at` → "fetch failed"; `s2maps-tiles.eu` → HTTP 403 to this tool. Known-good in a browser; liveness UNVERIFIED here |
| **Landsat 8/9 (+thermal)** | `landsat-c2-l2` (Collection-2 L2, L4/5/7/8/9; OLI+TIRS) via Earth Search STAC | STAC search → COG per band (incl. TIRS thermal `lwir11`) | 30 m (TIRS thermal 100 m → 30 m resampled) | L8 2013→, L9 2021→ (archive to 1982) | COG GeoTIFF | USGS Public Domain | **YES** — present in Earth Search `/collections` HTTP 200 (license rel = "Public Domain", USGS DOIs) |
| **MODIS / VIIRS imagery + fire** (D06, D125) | NASA GIBS layers e.g. `VIIRS_NOAA20_CorrectedReflectance_TrueColor`, `MODIS_Terra_CorrectedReflectance_TrueColor`, `VIIRS_NOAA20_Thermal_Anomalies_375m_All` | WMTS (RESTful `{Time}/{TileMatrix}/{Row}/{Col}`) + KVP | ~250 m truecolor; 375 m thermal anomalies; 1 km MODIS | NRT + multi-year archive | JPEG/PNG tiles | NASA — Fees:none, AccessConstraints:none | **YES** — GIBS `WMTSCapabilities.xml` HTTP 200 (valid WMTS, Fees none); VIIRS truecolor tile returned a JPEG (HTTP 200 image); thermal-anomalies layer id accepted by server (400 only on tilematrixset, i.e. layer exists) |
| **Esri World Imagery** (basemap) | `World_Imagery/MapServer` | ArcGIS tiled MapServer / XYZ (live) | 0.3–1 m (metro/US/EU) → 15 m global | continually updated mosaic | JPEG tiles | Esri ToU; **live display only, `exportTilesAllowed:false`** | **YES** — MapServer `?f=json` HTTP 200; `"exportTilesAllowed":false`; attribution "Source: Esri, Vantor, Earthstar Geographics, and the GIS User Community" |
| **Sentinel-1 SAR** (D01) | `sentinel-1-grd` (C-band GRD) via Earth Search STAC | STAC search → COG (VV/VH/HH/HV) | ~10 m pixel spacing (IW); 20 m res | 2014-10-10 → present | COG GeoTIFF | Copernicus free/open | **YES** — present in Earth Search `/collections` HTTP 200. ⚠ AWS GRD assets are `requester_pays:true` → actual byte GET needs AWS creds; use CDSE/ASF (Earthdata login) for a free fetch path |
| **NASA FIRMS active fire** | VIIRS S-NPP/NOAA-20/21 (`VIIRS_SNPP_NRT` 375 m), MODIS (`MODIS_NRT` 1 km); product D125 (MOD14/VNP14) | Area CSV API: `https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/{SOURCE}/{W,S,E,N}/{day_range}/{date}` ; also archive CSV | 375 m (VIIRS) / 1 km (MODIS) | NRT + archive 2000→ (MODIS), 2012→ (VIIRS) | CSV (lat,lon,bright,frp,acq_date,…) | NASA open data | **NO (needs key + host unreachable here)** — all `firms.modaps.eosdis.nasa.gov` fetches returned "fetch failed" this session; **MAP_KEY (free, from `/api/map_key/`) is REQUIRED**. API format recorded from NASA docs; liveness UNVERIFIED today |
| **Historical fire perimeters (US)** | NIFC `InteragencyFirePerimeterHistory_All_Years_View/FeatureServer/0` | ArcGIS FeatureServer query (JSON/GeoJSON/PBF) | vector polygons | historical → recent (per-fire `FIRE_YEAR`) | GeoJSON/JSON | US public (NIFC/Wildland Fire open) | **YES** — FeatureServer `?f=json` HTTP 200; fields incl. `INCIDENT, GIS_ACRES, FIRE_YEAR`; `capabilities: Query,Extract`. **(US-only → serves FALLBACK AOI, not Uttarakhand)** |
| **Fire perimeters (Europe) EFFIS** (D128) | EFFIS/GWIS burnt-area & hotspots | WMS/WFS | vector + raster | multi-year (Europe) | WMS/GeoJSON | Copernicus EMS terms | **NO** — `ies-ows.jrc.ec.europa.eu/effis` responded HTTP 200 but with a MapServer "Unable to access file" error → correct endpoint UNVERIFIED. Europe-only anyway (not our AOIs) |
| **Copernicus DEM GLO-30** (terrain, D51) | `cop-dem-glo-30` via Earth Search STAC **and** public S3 `copernicus-dem-30m` | STAC search / direct S3 GET → COG | 30 m DSM | static (edition 2021-04-22) | COG GeoTIFF (float32 m) | ESA Copernicus DEM licence (free, open w/ attribution) | **YES** — S3 `copernicus-dem-30m.s3.amazonaws.com/?list-type=2` HTTP 200 (public, no auth); also in Earth Search `/collections` (`requester_pays:false`) |
| **Copernicus DEM GLO-90** | `cop-dem-glo-90` (Earth Search / S3) | STAC / S3 → COG | 90 m DSM | static | COG GeoTIFF | ESA Copernicus DEM licence | **YES** — present in Earth Search `/collections` HTTP 200 (`requester_pays:false`) |
| **AWS Terrain Tiles (Mapzen/Terrarium)** | `elevation-tiles-prod` terrarium RGB-encoded elevation | XYZ tiles `s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png` (token-free) | ~ up to z15 (source SRTM/GMTED/NED mix) | static (2017 build) | PNG (terrarium RGB) | Open (public-domain + ODbL source mix; attribute sources) | **YES** — `elevation-tiles-prod.s3.amazonaws.com/?prefix=terrarium/` HTTP 200; `terrarium/0/0/0.png` listed (public, no auth) → **token-free Cesium terrain path** |
| **Cesium World Terrain** | Cesium ion asset 1 (quantized-mesh) | Cesium ion endpoint (CesiumJS native) | global, LOD'd | static | quantized-mesh | Cesium ion ToS | **NO — REQUIRES Cesium ion access token.** Not fetched; use AWS Terrain Tiles (above) for a token-free alternative |
| **SRTM** (D50) | SRTMGL1 v3 30 m | USGS EarthExplorer / OpenTopography / CMR | 30 m (1 arc-sec) | 2000-02 (single mission) | GeoTIFF/HGT | USGS Public Domain | **UNVERIFIED today** — not fetched this session (EarthExplorer needs login). Prefer verified Copernicus GLO-30 as the primary DEM |
| **ESA WorldCover** (land cover) | ESA WorldCover v100 (2020) / v200 (2021) | public S3 `esa-worldcover` → COG; also WMTS via Terrascope | 10 m | 2020 (v100), 2021 (v200) | COG GeoTIFF (11 classes) | CC-BY-4.0 (attribution ESA WorldCover) | **YES (bucket)** — `esa-worldcover.s3.eu-central-1.amazonaws.com/?list-type=2` HTTP 200 (public). Grid/index files listed; version+class scheme from ESA docs |
| **Copernicus Global Land Cover** | CGLS-LC100 collection 3 | VITO / Zenodo | 100 m | 2015–2019 annual | GeoTIFF | CC-BY-4.0 | **UNVERIFIED today** — not fetched; WorldCover (verified above) is the higher-res choice |
| **OpenStreetMap buildings + roads** | OSM via Overpass API | Overpass QL `POST`/`GET` → JSON/XML (bbox query) | vector (building=*, highway=*) | live, continuously edited | OSM JSON / GeoJSON | ODbL (attribution + share-alike) | **YES** — `overpass-api.de/api/status` HTTP 200 (slots available, server live) |
| **Microsoft Global Building Footprints** | GlobalMLBuildingFootprints (incl. India) | index `minedbuildings.z5.web.core.windows.net/global-buildings/dataset-links.csv` → per-quadkey GeoJSONL (gz) | vector polygons | 2018–2023 imagery-derived | GeoJSONL (gzip) | ODbL | **PARTIAL** — index URL reached but returned content-type `application/vnd.ms-excel` (CSV) that this tool can't render; file exists, contents UNVERIFIED here |
| **Google Open Buildings** | Open Buildings v3 (Global South incl. India) | GCS CSV/parquet per S2 cell | vector polygons + confidence | v3 (2023) | CSV / GeoParquet | CC-BY-4.0 / ODbL (dual) | **UNVERIFIED today** — not fetched this session; documented to cover India |
| **ERA5-Land reanalysis** (wind/temp/humidity, D05) | `reanalysis-era5-land` (CDS) | CDS API (`cdsapi`) → NetCDF/GRIB | 0.1° (~9 km), hourly | 1950-01-01 → 2026-10-04 | NetCDF / GRIB | CC-BY-4.0 (DOI 10.24381/cds.e2161bac) | **YES (needs account)** — CDS STAC `/collections/reanalysis-era5-land` HTTP 200; `license: CC-BY-4.0`, `sanity_check: available`. **REQUIRES free CDS account + API key** |
| **GPM IMERG precipitation** (D48) | IMERG V07 | GIBS tiles (display) / GES DISC (download, Earthdata) | 0.1°, 30-min | 2000→ present | tiles / NetCDF | NASA open | **PARTIAL** — GIBS WMTS service verified 200 (IMERG layers hosted there); GES DISC download path needs Earthdata login (UNVERIFIED here) |
| **WorldPop population** | Global2 pop counts / age-sex (R2025A) | WorldPop REST `hub.worldpop.org/rest/data` → GeoTIFF | 100 m & 1 km | 2015–2030 (annual) | GeoTIFF | CC-BY-4.0 | **YES** — `hub.worldpop.org/rest/data` HTTP 200 (JSON catalogue of pop/age_structures/density etc.) |
| **GHSL (JRC) built-up / population** | GHS-POP, GHS-BUILT-S, GHS-SMOD (R2023A) | direct download (tiles / single file) `human-settlement.emergency.copernicus.eu` + JRC JEODPP FTP | 100 m / 1 km (Mollweide + WGS84) | epochs 1975–2030 | GeoTIFF / shapefile | "Reuse authorised with proper acknowledgment of the source" (© European Union) | **YES** — GHSL download page HTTP 200; JEODPP FTP download links present |

### Reference / already-in-registry streams (not re-fetched this session, cited from DATASETS.md)
| Source | ID | Note | Verified today? |
|--------|----|------|-----------------|
| ITS_LIVE glacier velocity | D07 | GLOF/landslide (Chamoli) layer; STAC/Zarr/S3 | NO — cited from registry (D07 [V]); not re-fetched |
| CHIRPS rainfall | D49 | quasi-global gauge+satellite rainfall | NO — cited from registry (D49 [D]) |
| Copernicus Data Space (CDSE) | D01/D02 | account path for S1/S2 OGC/openEO | NO — known public; not re-fetched (free account) |

---

## 3. WHAT NEEDS A KEY/ACCOUNT vs WORKS TOKEN-FREE

**Works TODAY with NO account / NO token (verified HTTP 200 this session):**
- Esri World Imagery basemap (live display only; `exportTilesAllowed:false`).
- NASA GIBS WMTS — MODIS/VIIRS true-color + VIIRS 375 m thermal-anomalies (fire) tiles.
- Earth Search STAC (`earth-search.aws.element84.com/v1`) → Sentinel-2 L2A (10 m), Landsat C2 L2 (incl.
  thermal), Copernicus DEM GLO-30/90. *(STAC query + the S2/Landsat/DEM COGs are open; Sentinel-1 GRD assets
  on AWS are `requester_pays` — see keyed list.)*
- Copernicus DEM GLO-30 public S3 bucket (`copernicus-dem-30m`).
- AWS Terrain Tiles terrarium XYZ (`elevation-tiles-prod`) → **token-free Cesium 3D terrain**.
- ESA WorldCover 10 m public S3 bucket (`esa-worldcover`).
- OSM Overpass API (buildings/roads).
- WorldPop REST (population GeoTIFFs).
- GHSL / JRC download (built-up + population).
- NIFC fire-perimeter FeatureServer (fallback US AOI only).

**REQUIRES a free account / key / token (free, but register first):**
- **NASA FIRMS** active-fire area CSV API → **free MAP_KEY** (`/api/map_key/`). *(Also: host did not respond
  to `web_fetch` today — treat endpoint liveness as unconfirmed and test from the browser/with a MAP_KEY.)*
- **Copernicus CDS** (ERA5-Land) → free CDS account + API key.
- **Copernicus Data Space (CDSE)** → free account for bulk/OGC Sentinel-1/2 (needed for a free S1 GRD byte
  path, since the AWS mirror is requester-pays).
- **NASA Earthdata login** → GPM IMERG download (GES DISC), MODIS LP DAAC, ASF Sentinel-1, ITS_LIVE V1.
- **Cesium ion token** → Cesium World Terrain / Bing imagery (optional; AWS Terrain Tiles replaces it
  token-free).
- **AWS credentials** → only to GET the requester-pays Sentinel-1 GRD COGs on AWS (the STAC catalog itself is
  free).

**Net for the app:** a browser-only CesiumJS build can run with **zero accounts** using Esri + GIBS +
Earth Search S2/Landsat/DEM COGs + AWS Terrain Tiles + WorldCover + OSM + WorldPop + GHSL. The only
on-theme capability that forces one free key is **live FIRMS active fire** (MAP_KEY) and **ERA5-Land**
weather (CDS account); both are free. A historical FIRMS archive CSV can be bundled as a small,
redistributable fallback for the demo (per PROGRESS_VIZ R0 plan).

---

## 4. SOURCES I COULD NOT VERIFY (and why)

| Source | Reason not verified | Honest status |
|--------|--------------------|----------------|
| **NASA FIRMS** (area CSV API, mapkey_status) | Every `firms.modaps.eosdis.nasa.gov` request returned `TypeError: fetch failed` from this tool (host unreachable to `web_fetch`; matches PROGRESS_VIZ R0 "bare endpoint fetch failed"). | API format + MAP_KEY requirement recorded from NASA docs; **endpoint liveness UNVERIFIED today** — must be tested in-browser with a free MAP_KEY. |
| **EOX Sentinel-2 cloudless** WMTS | `tiles.maps.eox.at` → "fetch failed"; `s2maps-tiles.eu` → HTTP 403 "forbidden by administrative rules" (tool UA/referrer blocked). | Service is well-known-good in a browser; **not verified by this tool today**. S2 L2A via Earth Search (verified) is the primary optical path. |
| **EFFIS/GWIS** fire perimeters | `ies-ows.jrc.ec.europa.eu/effis` returned HTTP 200 but a MapServer "Unable to access file" error → wrong/placeholder mapfile. | Correct WMS/WFS endpoint **UNVERIFIED**; Europe-only, so not needed for either AOI (use NIFC for the fallback). |
| **Microsoft Global Building Footprints** index | `dataset-links.csv` reached but served as `application/vnd.ms-excel`, which `web_fetch` cannot render. | File exists; **contents UNVERIFIED** here. OSM/Overpass (verified) is the primary building source. |
| **Google Open Buildings v3** | Not fetched this session. | Documented to cover India; **UNVERIFIED today**. |
| **Cesium World Terrain** | Requires a Cesium ion token; not fetched. | Known to require an account; AWS Terrain Tiles (verified) is the token-free substitute. |
| **SRTM (SRTMGL1)** / **Copernicus Global Land Cover** / **CHIRPS** / **ITS_LIVE** | Not fetched this session (EarthExplorer/Earthdata login or already in registry). | Cited from `DATASETS.md`; **not re-verified today**. Copernicus GLO-30 + ESA WorldCover (both verified) are the preferred, token-free equivalents. |
| **GPM IMERG download** (GES DISC) | Only the GIBS display tiles were verified; GES DISC download needs Earthdata login. | Display path verified via GIBS; **direct-download path UNVERIFIED today**. |

---

## 5. SUMMARY COUNTS (for the orchestrator)
- **Primary AOI:** Uttarakhand Himalaya forest fires, pre-monsoon 2021 (bbox 78.5,29.5,80.2,30.8; peak
  ~2021-04-25→05-12). Fallback: LA fires Jan 2025 (bbox −118.75,33.90,−118.00,34.30). Geohazard alt:
  Chamoli GLOF 2021-02-07.
- **Verified accessible today (HTTP 200 / confirmed resolve):** 13 sources — Esri World Imagery, NASA GIBS
  WMTS (truecolor + fire), Earth Search STAC (Sentinel-2 L2A, Landsat C2 L2, Sentinel-1 GRD listing,
  Copernicus DEM GLO-30 & GLO-90), Copernicus DEM GLO-30 S3, AWS Terrain Tiles, ESA WorldCover S3, Overpass,
  WorldPop, GHSL, ERA5-Land CDS (account-gated), NIFC perimeters.
- **Token-free & working:** 10 (Esri, GIBS, Earth Search COGs [S2/Landsat/DEM], AWS Terrain Tiles,
  WorldCover, Overpass/OSM, WorldPop, GHSL, NIFC; Copernicus DEM S3).
- **Need a free key/account:** FIRMS (MAP_KEY), ERA5-Land (CDS), CDSE (free S1 bytes), Earthdata (IMERG/
  MODIS/ASF/ITS_LIVE), Cesium ion (optional), AWS creds (requester-pays S1 only).
- **Could NOT verify today:** 7 (FIRMS liveness, EOX cloudless, EFFIS endpoint, MS Buildings contents,
  Google Open Buildings, SRTM, Cesium World Terrain) — all with substitutes or free-key paths noted above.
