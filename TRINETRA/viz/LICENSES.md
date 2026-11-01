# Data / Imagery License Audit — Visualization (Interactive Web App + Recorded Cinematic Video)

**Auditor role:** data/imagery license auditor
**Accessed date for all citations:** 2026-10-10
**Working dir:** `C:\Users\Dell\Documents\deepseek-harness\default-workspace`
**Method:** Each term was read from the live source page via `web_fetch` (treated as untrusted data). Where a term is a PDF that could not be fetched, or a page rendered only navigation/JS, it is marked **UNCLEAR, verify**. Nothing below is guessed; open-data status asserted without a quotable clause is explicitly flagged.

> Legend for the three use questions:
> - **Live?** = usable as a LIVE layer streamed into an interactive web map
> - **Bundle?** = tiles/data may be DOWNLOADED and BUNDLED/redistributed for offline use
> - **Video?** = may appear in a RECORDED / REDISTRIBUTED cinematic video

---

## 1. Per-source table

| # | Source | Live? | Bundle? | Video? | Attribution string (exact) | Restriction | Verdict |
|---|--------|-------|---------|--------|----------------------------|-------------|---------|
| 1 | **Esri World Imagery** (arcgisonline) | ✅ via ArcGIS basemap/API | ❌ `exportTilesAllowed=false` | ⚠️ UNCLEAR | `Source: Esri, Vantor, Earthstar Geographics, and the GIS User Community` | Esri Master Agreement (E204/E300); tiles may not be exported/cached/redistributed; proprietary imagery (not open) | **live only, NOT in exported video — UNCLEAR, verify; replace in video with Sentinel‑2 cloudless or other open imagery** |
| 2 | **Sentinel‑2 / Sentinel‑1 / Copernicus Sentinel data** | ✅ | ✅ | ✅ | `Copernicus Sentinel data [year]` (and `Contains modified Copernicus Sentinel data [year]` if adapted) | Free, full, open (incl. commercial); attribution required. Exact Legal Notice PDF not fetched (see UNCLEAR) | **OK for live app + video with attribution** |
| 3 | **ERA5 / ERA5‑Land (Copernicus C3S)** | ✅ | ✅ | ✅ | `Generated using Copernicus Climate Change Service information [Year]` (or `Contains modified Copernicus Climate Change Service information [Year]`) | Free, worldwide, non-exclusive, perpetual, any lawful purpose incl. commercial; must add disclaimer that EC/ECMWF not responsible for use | **OK for live app + video with attribution** |
| 4 | **NASA FIRMS** (active fire) | ✅ | ✅ | ✅ | e.g. `Data courtesy of NASA FIRMS (LANCE/EOSDIS)` — exact string UNCLEAR | FIRMS API requires a free **MAP_KEY** (rate/transaction-limited); NASA data not copyrighted. Exact attribution + MAP_KEY limits not extractable firsthand | **OK for live app + video; needs free MAP_KEY for API — verify attribution string + rate limits** |
| 5 | **NASA GIBS** (tiled imagery) | ✅ | ✅ | ✅ | `We acknowledge the use of imagery from NASA Worldview / GIBS, part of NASA EOSDIS` — exact UNCLEAR | NASA open data, no copyright; citation requested | **OK for live app + video with acknowledgment** |
| 6 | **MODIS / VIIRS** products | ✅ | ✅ | ✅ | Cite product DOI + `NASA LP DAAC / LANCE` — exact UNCLEAR | NASA open data, public domain, no restriction; citation requested | **OK for live app + video with citation** |
| 7 | **Landsat (USGS)** | ✅ | ✅ | ✅ | `Landsat imagery courtesy of the U.S. Geological Survey` | U.S. Gov public domain; free redistribution. USGS copyright page returned no body firsthand (JS/202) → see UNCLEAR | **OK for live app + video with credit** |
| 8 | **Copernicus DEM GLO‑30** | ✅ | ✅ (COG/S3 open) | ✅ | `Produced using Copernicus WorldDEM‑30 © DLR e.V. 2010‑2014 and © Airbus Defence and Space GmbH [year] provided under COPERNICUS by the European Union and ESA; all rights reserved` | Free for general public under COPERNICUS DEM licence (`License-COPDEM-30.pdf`); redistribution clause not fetched (PDF) → see UNCLEAR | **OK for live app + video with attribution — verify redistribution clause in License‑COPDEM‑30.pdf** |
| 9 | **SRTM** (NASA/USGS) | ✅ | ✅ | ✅ | `SRTM data courtesy of NASA/USGS` | Public domain, no restriction. No quotable clause fetched firsthand → see UNCLEAR | **OK for live app + video with credit** |
| 10 | **ESA WorldCover 10 m** | ✅ | ✅ | ✅ | `© ESA WorldCover project [year] / Contains modified Copernicus Sentinel data ([year]) processed by ESA WorldCover consortium` | CC‑BY‑4.0, free without restriction of use; attribution required | **OK for live app + video with attribution** |
| 11 | **OpenStreetMap** (buildings/roads via Overpass) | ✅ | ✅ | ✅ | `© OpenStreetMap contributors` + state data is available under the Open Database License (ODbL) | **ODbL share-alike**: derivative/adapted DATABASES distributed must be re‑licensed under ODbL. Produced map images/video (Produced Works) are not forced open, but attribution + ODbL notice required. Do not use OSMF tile servers in production (tile usage policy) | **OK for live app + video with attribution; watch ODbL share‑alike if you distribute derived data/vector tiles** |
| 12 | **Cesium World Terrain / Cesium ion** | ✅ (streamed) | ❌ offline prohibited (§2.2.2) | ⚠️ only via Value‑Added Clips (§2.3) | `Cesium ion` logo must be prominently displayed (§2.2.3) + third‑party notices (Appendix B) | **Account + token required**; non-sublicensable; may not include ion in a commercial solution for other orgs; may not store/redistribute Data Output offline; display rights end at Term end | **needs account; avoid for bundled/offline + video — replace with open terrain (AWS Terrain Tiles / MapTiler / Mapzen) to avoid token + offline limits** |
| 13 | **WorldPop** | ✅ | ✅ | ✅ | `Source: WorldPop (www.worldpop.org)` + CC‑BY‑4.0 link | CC‑BY‑4.0 (commercial OK). **BUT** WorldPop layers derived from OSM / Microsoft Buildings / Microsoft Roads are **ODbL** (share-alike). Responsible-use expectation (no surveillance/harm) | **OK for live app + video with attribution; check per-dataset whether it is CC‑BY or ODbL** |
| 14 | **GHSL (JRC, Global Human Settlement)** | ✅ | ✅ | ✅ | `© European Union, 1995‑2025` / `Source: European Commission, Joint Research Centre (JRC), Global Human Settlement Layer` | Reuse authorised with proper acknowledgment of source (EU open reuse) | **OK for live app + video with attribution** |
| 15 | **CesiumJS (JS library)** | ✅ | ✅ | ✅ | Apache‑2.0 NOTICE + `Copyright 2011‑2026 CesiumJS Contributors` (retain LICENSE + bundled third-party MIT/BSD/Apache notices) | Apache‑2.0 permissive; must retain license/NOTICE; includes bundled MIT/BSD/Apache/OFL third-party code | **OK — permissive, redistribute freely with retained notices** |

---

## 2. ATTRIBUTIONS TO DISPLAY IN THE APP / VIDEO (exact strings)

Display these in an on-screen credits/attribution panel in the interactive app, and in a visible credits frame/corner in the recorded video.

```
Imagery / basemap (video, open):   Contains modified Copernicus Sentinel data [year]
Satellite data (S1/S2):            Copernicus Sentinel data [year]
Climate (ERA5 / ERA5-Land):        Generated using Copernicus Climate Change Service information [Year]
                                   (Neither the European Commission nor ECMWF is responsible for any use
                                    of the Copernicus information or data it contains.)
Land cover (ESA WorldCover):       © ESA WorldCover project [year] / Contains modified Copernicus Sentinel
                                   data ([year]) processed by ESA WorldCover consortium
Elevation (Copernicus DEM GLO-30): Produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and
                                   © Airbus Defence and Space GmbH [year] provided under COPERNICUS by
                                   the European Union and ESA; all rights reserved  [VERIFY exact wording]
Elevation (SRTM):                  SRTM data courtesy of NASA/USGS
Fire (NASA FIRMS):                 Data courtesy of NASA FIRMS (LANCE/EOSDIS)  [VERIFY exact string]
Imagery tiles (NASA GIBS):         Imagery courtesy of NASA EOSDIS GIBS/Worldview
Landsat:                           Landsat imagery courtesy of the U.S. Geological Survey
Vector (OpenStreetMap):            © OpenStreetMap contributors — data available under the Open Database License (ODbL)
Population (WorldPop):             Source: WorldPop (www.worldpop.org), CC BY 4.0
                                   (ODbL where derived from OSM/Microsoft footprints)
Settlement (GHSL):                 Source: European Commission, JRC, Global Human Settlement Layer — © European Union
Engine (CesiumJS):                 Powered by CesiumJS — © 2011-2026 CesiumJS Contributors (Apache-2.0)
IF Cesium ion terrain is used:     Cesium ion  (logo, prominently displayed) + Appendix B third-party notices
```

Replace `[year]` / `[Year]` with the actual acquisition/production year of each dataset used.

---

## 3. DO NOT USE / replace with open alternative

- **Esri World Imagery (arcgisonline)** — proprietary; `exportTilesAllowed=false`; tiles may not be exported, cached, or redistributed, and redistribution inside a recorded/redistributed video is not clearly granted. **Do not bundle; do not put in the exported video.** Replace in the video (and ideally the app’s exportable layers) with an open basemap: **Sentinel‑2 cloudless (EOX, CC‑BY‑4.0‑style), Copernicus Sentinel‑2 composites, or NASA GIBS/Landsat.**
- **Cesium ion / Cesium World Terrain** — requires an account + token, prohibits offline/bundled storage of Data Output, and is non-sublicensable; keeping it adds a hard account dependency and bars offline/video reuse of the streamed tiles. **Replace with open terrain** to avoid: **AWS Terrain Tiles (Mapzen/Tilezen, ODbL/CC‑BY mix), MapTiler Terrain, or self-hosted Copernicus DEM GLO‑30 quantized-mesh.** (CesiumJS the engine is fine — only the ion content service is the problem.)

---

## 4. Sources with UNCLEAR terms needing human confirmation

1. **Esri World Imagery — video/recording rights.** The Esri Master Agreement index page was fetched (`esri.com/.../master-agreement`) but the specific scope-of-use for displaying World Imagery in a *recorded, redistributed* video is in the E204/E300 PDFs, not fetched. `exportTilesAllowed=false` is confirmed. **Confirm with Esri whether a cinematic recording of the live basemap counts as prohibited redistribution.** Safer: do not use in video.
2. **Copernicus Sentinel data — exact Legal Notice clause.** `Sentinel_Data_Legal_Notice` is a PDF (`application/pdf`) that could not be fetched. Free/full/open + commercial status is **confirmed firsthand** via the Copernicus Data Space Ecosystem Terms (§3: “available on a free, full and open basis … governed by the Legal Notice”). **Confirm the exact attribution wording and any conditions in the PDF.**
3. **Copernicus DEM GLO‑30 — redistribution clause.** Free-for-public status confirmed via OpenTopography; the governing `License-COPDEM-30.pdf` was not fetched. **Confirm redistribution/bundling and the exact attribution string in that PDF.**
4. **NASA FIRMS — exact attribution + MAP_KEY limits.** NASA Earthdata/FIRMS pages returned navigation only (JS-rendered); the open-data basis is well established but the exact credit line and the MAP_KEY transaction-rate limits were not extractable firsthand. **Confirm the current MAP_KEY rate limits and preferred citation.**
5. **NASA GIBS / MODIS / VIIRS, Landsat (USGS), SRTM — quotable clause.** Public-domain / open status is well established and consistent with NASA’s open-data policy, but the USGS copyright page and NASA policy body text did not render firsthand (HTTP 202 / nav-only). **Confirm the exact credit lines from the authoritative USGS/NASA pages.**
6. **OpenStreetMap — ODbL share-alike scope.** Confirmed ODbL + attribution firsthand. **Confirm whether your pipeline distributes a derived *database* (e.g., vector tiles) — which would trigger ODbL share-alike — versus only a Produced Work (rendered image/video), which does not.**

---

## 5. Summary

- **Sources audited:** 15.
- **Blocked / restricted for the exported video:** **Esri World Imagery** (export disabled, redistribution unclear → keep out of video) and **Cesium ion / World Terrain** (offline/redistribution prohibited; only Value-Added Clips may be redistributed).
- **Require an account/token:** **Cesium ion** (account + token, mandatory) and **NASA FIRMS** (free MAP_KEY for the API).
- **Clean for live + video with attribution:** Copernicus Sentinel S1/S2, ERA5/ERA5‑Land, NASA GIBS/MODIS/VIIRS, Landsat, Copernicus DEM GLO‑30, SRTM, ESA WorldCover, OpenStreetMap (watch ODbL share-alike), WorldPop (CC‑BY or ODbL per dataset), GHSL, and CesiumJS (Apache‑2.0 engine).
