# QA_REPORT.md — honesty + provenance + legal audit (TRINETRA/HIMKAVACH 3D viz)

Date: 2026-10-10. Scope: `viz/` interactive CesiumJS build + pipeline + docs. This report states exactly what
was verified in-session and what could NOT be, with no inflation.

## 0. Verification performed IN this sandbox (evidence)
| Check | Method | Result |
|-------|--------|--------|
| JS modules parse | `node --check` on all 6 `src/*.js` + `vite.config.js` | **PASS** (all OK) |
| Data files valid | `ConvertFrom-Json` on `public/data/*.json` | **PASS** (l6, l8, l12 valid) |
| Physics layer computed | ran `gen_physics_fields.py` (imports real `trinetra/` core) | **PASS** (sane values) |
| Dataset layer parsed | ran `gen_dataset_panels.py` on `DATASETS.md` | **PASS** (26 rows: 13 selected / 13 candidate) |
| Production build | `vite build` (CesiumJS 1.146, vite 6.4.4) | **PASS** — `dist/` incl. Cesium static assets |
| App serves | `Invoke-WebRequest` to `http://127.0.0.1:8099` | **PASS** — index/bundle/data/Cesium.js all HTTP 200 |

## 1. Could NOT be verified in-sandbox (honest limits)
- **Visual WebGL render / frame-by-frame visual QA**: the Tabbit browser launcher is not installed on this
  host, and the sandbox has no GPU/headless-WebGL. The app builds and serves, but it must be opened in a
  **real browser** to confirm the globe/terrain/plume render as designed. This matches the Phase-1 feasibility
  verdict (rendering happens in the user's browser). Visual QA + the cinematic video are **local steps**
  (see `HOW_TO_REPRODUCE.md`).
- **Live tile endpoints** (Esri imagery/terrain, NASA GIBS, Terrascope WorldCover): reachability depends on the
  viewer's network; the app degrades gracefully (a failed source does not fabricate data). The Sentinel-2 WMTS
  layer id and GIBS date template are marked VERIFY in `config.js` and should be confirmed on first run.

## 2. Provenance audit (every on-screen layer carries source + kind)
Each layer in `config.js` declares `kind` (REAL / SIMULATED / ILLUSTRATIVE) and a `provenance` caption
(source, product, date, resolution, license). The HUD shows the kind chip + provenance table + note for the
active layer, and a persistent attributions footer (exact strings from `LICENSES.md`). **PASS** by construction;
spot-checked L0/L1/L2/L6/L8/L12 captions against `LAYER_MAP.md` + `DATA_SOURCES.md` — consistent.

## 3. Number audit (no unmeasured performance numbers)
- L8 dataset counts are parsed **verbatim** from `DATASETS.md` (26 quick-link rows; 13 selected / 13 candidate;
  verification tags [V]/[V*]/[D] preserved) — they match the registry exactly because they are copied, not typed.
- L6 scalars (flame height 7.61 m, puffing 0.47 Hz, Byram N_c 0.446, FS curve, Caine ratio 1.086) are **computed**
  by the real physics code and labelled SIMULATED with their parameters — they are model outputs, not measured skill.
- The canonical decision rule shown in L12 (`level = max(conformal_level(fused_risk, p*), shield_floor), p*≈0.0476`)
  matches `_CANON.md`.
- **No** accuracy / precision / recall / latency / reach number is presented as measured. `FINAL_REPORT.md` says
  nothing was trained or measured; the viz honours that.

## 4. Real vs simulated audit
- REAL (green): L0 basemap, L1 DEM, L2 land cover, L3 exposure (metadata), L4 ERA5 wind, L5 FIRMS, L8 metadata.
- SIMULATED (amber): L6 physics fields (our code), L11 rule-baseline routes, detector scores in L7/L9.
- ILLUSTRATIVE (slate): L7 camera FOV cones, L9 deepfake flow, L10 reach rings, L12 DFD, L3 extruded boxes.
- The tag is **redundant-coded**: colour + kind chip + caption text. Nothing simulated is captioned as observed.
- **Known honest substitutions** (not defects): L3 uses illustrative extruded boxes (real OSM loads via the
  documented Overpass pipeline step); L11 draws illustrative polylines (real OSM road graph is the pipeline step);
  L10 reach rings are scenario geometry (no acoustic range model exists in `ws3_alert/`). All are labelled as such.

## 5. Geometry audit
- Coordinates are WGS-84 lon/lat; camera destinations are AOI-interior (`tour.js` matches `STORYBOARD.md`).
- Vertical exaggeration = ×1.0 and is labelled in the S2 caption; if changed in `config.js` the label must update.
- CCTV FOV = inverted cone (apex at camera) — correct sense; it is tagged ILLUSTRATIVE (not a surveyed FOV).
- Scale readout = metres/pixel sampled at screen centre; north arrow rotates with camera heading. Reasonable;
  exact scale-bar calibration should be eyeballed in-browser.

## 6. Newcomer test
A viewer who has not seen the project can: read the title; play the tour; see each layer appear with a green
(REAL) / amber (SIMULATED/ILLUSTRATIVE) chip + a provenance caption; and reach the DFD finale that states
"advisory, human-in-loop, never autonomous". The REAL/SIM distinction is explained in the S13 caption. **PASS**
pending the in-browser visual confirmation in §1.

## 7. Legal audit
- `LICENSES.md` holds the per-source verdicts. The app **defaults to a basemap switch** where Esri is tagged
  "live only ⚠" and the open source (GIBS / Sentinel-2) is video-safe; the HUD note states Esri must stay out of
  recorded video (`exportTilesAllowed=false`). CesiumJS is Apache-2.0. Attributions footer shows the exact strings.
- No Cesium ion token is used (token-free Esri terrain + imagery), so no ion account/logo obligation is triggered.
- Privacy: no faces / no CCTV media are shown (L7 shows FOV geometry + a license-permitting sample only; L9
  shows stats, no media).
- **Open items for the user**: confirm Esri's video-recording right if they ever record with the Esri basemap
  (we recommend the open basemap for video); confirm GIBS/FIRMS/Landsat exact credit lines (flagged UNCLEAR in
  `LICENSES.md`).

## 8. Residual gaps carried forward (not faked)
- L4 (ERA5 wind) + L5 (FIRMS) are **DATA-PENDING**: they need a free CDS account / FIRMS MAP_KEY. Until the
  extracts from `fetch_firms_era5.py` exist, the app shows a DATA-PENDING placard and renders nothing — never
  synthetic wind or hotspots.
- Visual/cinematic QA + the exported video are local steps (§1, `HOW_TO_REPRODUCE.md`).
- Zenodo DOI 11424988 registry-vs-live conflict (noted earlier in the docs' QG5 log) does not affect this viz,
  which only displays the registry metadata verbatim.
