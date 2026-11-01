# HOW_TO_REPRODUCE.md — build, run, regenerate, and record the TRINETRA/HIMKAVACH 3D data-stack viz

Everything below was exercised on the build machine (2026-10-10) unless marked **local-only** (needs a GPU
browser, a free data key, or OBS/ffmpeg that the build sandbox lacks).

## 0. Environment (verified)
- **Node** 24.x + **pnpm** 11.7 (bundled DSH runtime).
- **Python** 3.12 with numpy (bundled runtime) — only needed to regenerate data, not to run the app.
- **CesiumJS** 1.146.0, **Vite** 6.4.4, **vite-plugin-cesium** 1.2.23 (pinned in `viz/render/package.json`).
- No Cesium ion account and no API token are required (token-free Esri terrain + imagery; open GIBS basemap).

## 1. Install dependencies
```powershell
cd viz/render
# allow esbuild's postinstall (Vite's bundler) and run non-interactively:
#   viz/render/pnpm-workspace.yaml already contains:  allowBuilds: { esbuild: true }
$env:CI = "true"                       # lets pnpm purge/rebuild node_modules without a TTY prompt
pnpm install
```
Note: esbuild spawns a native child process over stdio pipes; a locked-down sandbox blocks that with `EPERM`.
On a normal workstation it just works. If you see `ERR_PNPM_IGNORED_BUILDS`, run `pnpm approve-builds` once.

## 2. Build / run the interactive app
```powershell
cd viz/render
pnpm run build          # -> dist/ (self-contained: index.html + assets/ + cesium/ + data/)
pnpm run preview        # or: python -m http.server 8099 --directory dist   -> open the printed URL
# dev mode with HMR:
pnpm run dev
```
Open the URL in **Chrome/Edge/Firefox** (WebGL required). You get: the globe → Uttarakhand fly-in, per-layer
toggles + opacity sliders, the timeline scrubber (2021-04-25→05-12), the basemap switch (open vs Esri), and the
guided tour (▶ Tour) that plays S0→S14 with captions.

## 3. Regenerate the data layers (optional — outputs are committed under `render/public/data/`)
```powershell
$env:PYTHONIOENCODING = "utf-8"
# L6 — SIMULATED physics from the REAL trinetra numpy core:
python viz/pipeline/gen_physics_fields.py        # -> public/data/l6_physics.json
# L8 — dataset registry parsed VERBATIM from DATASETS.md:
python viz/pipeline/gen_dataset_panels.py        # -> public/data/l8_datasets.json
```

## 4. Supply the DATA-PENDING real layers (local-only; free accounts)
L4 (ERA5-Land wind) and L5 (FIRMS fire) render nothing until you provide real extracts — the app shows a
DATA-PENDING placard and never fabricates them.
```powershell
# L5 — NASA FIRMS active fire (free MAP_KEY: https://firms.modaps.eosdis.nasa.gov/api/map_key/):
python viz/pipeline/fetch_firms_era5.py firms --map-key YOUR_KEY `
    --bbox 78.5,29.5,80.2,30.8 --start 2021-04-25 --end 2021-05-12
# L4 — ERA5-Land wind (free CDS account + `pip install cdsapi` + ~/.cdsapirc; needs xarray/netCDF4 locally):
python viz/pipeline/fetch_firms_era5.py era5 --bbox 78.5,29.5,80.2,30.8 --date 2021-05-01
```
These write `public/data/l5_firms.json` and `public/data/l4_era5_wind.json`; rebuild (step 2) to include them.

## 5. Load the REAL OSM road graph for L11 (optional upgrade)
L11 ships illustrative advisory polylines. To use the real OSM road graph, query Overpass for the AOI
(`highway` ways) and feed the GeoJSON to the L11 builder — documented as a follow-up; keep attribution
"© OpenStreetMap contributors (ODbL)".

## 6. Record the cinematic video (local-only)
The video is recorded in a real browser, not in the sandbox. Two license-clean paths — **use the open basemap
(GIBS / Sentinel-2 cloudless), not Esri**, for anything you export (`LICENSES.md §1`).

**A. Screen capture (simplest):** open the app full-screen, switch to the open basemap, press ▶ Tour, and record
the window with **OBS Studio** (or Windows Game Bar). ~2 min 36 s per `STORYBOARD.md`.

**B. Deterministic per-frame dump (crisper):** the viewer is exposed as `window.__viewer` and the WebGL context
is created with `preserveDrawingBuffer:true`, so you can render the tour frame-by-frame and read the canvas:
```js
// paste in the browser console; saves PNGs you then mux with ffmpeg
const v = window.__viewer; const fps = 30; let n = 0;
function grab() { const a = document.createElement('a');
  a.download = String(n++).padStart(5,'0') + '.png'; a.href = v.scene.canvas.toDataURL('image/png'); a.click(); }
// drive the tour (click ▶ Tour) and call grab() on a timer at your fps, then:
```
```powershell
ffmpeg -framerate 30 -i %05d.png -c:v libx264 -pix_fmt yuv420p -crf 16 viz/output/trinetra_stack.mp4
```

## 7. Visual QA with Tabbit/Playwright (local-only)
On a machine with the Tabbit launcher (or plain Playwright), open the served app, enable layers, play the tour,
and screenshot to `viz/output/stills/` — see `QA_REPORT.md §1` for the checks. The build sandbox had no browser
launcher installed, so these stills are produced locally.

## 8. File map
```
viz/
  RESEARCH.md DATA_SOURCES.md LICENSES.md STACK_DECISION.md   # Phase 1 research
  LAYER_MAP.md STORYBOARD.md DESIGN_SPEC.md                   # Phase 2–3 design
  pipeline/ gen_physics_fields.py gen_dataset_panels.py fetch_firms_era5.py
  render/   package.json vite.config.js index.html
            src/{main,config,colormaps,layers,hud,tour}.js  src/style.css
            public/data/{l6_physics,l8_datasets,l12_dfd}.json
            dist/            # built output (step 2)
  output/   stills/ + exported video (local)
  QA_REPORT.md  HOW_TO_REPRODUCE.md  PROGRESS_VIZ.md
```
