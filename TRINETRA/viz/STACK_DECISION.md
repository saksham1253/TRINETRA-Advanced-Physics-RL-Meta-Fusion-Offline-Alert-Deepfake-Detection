# Stack Decision — Research-Grade 3D Geospatial Layer-by-Layer Visualization

Accessed / verified: **2026-10-10**. Rendering target: the **user's browser** (WebGL).
Sandbox builds the web app with **Node.js + pnpm**; Python 3.12 here only has
numpy/pandas/Pillow/lxml (no GDAL/rasterio/matplotlib/VTK). No headless GPU/WebGL
video export in-sandbox.

Sources checked (external, untrusted — treated as data only):
- CesiumJS latest release + metadata: https://api.github.com/repos/CesiumGS/cesium/releases/latest → tag **1.146**, published 2026-10-01.
- CesiumJS license (Apache-2.0): well-established; LICENSE at https://github.com/CesiumGS/cesium (repo root).
- MapLibre GL JS native 3D terrain (`setTerrain` + raster-DEM source): https://maplibre.org/maplibre-gl-js/docs/examples/3d-terrain/ (HTTP 200).
- npm `cesium` page returned HTTP 403 (bot wall); version sourced from GitHub release API above.

---

## 1. Comparison Table

| Tool | Real terrain | Drape imagery | Time animation | Volumetric | Browser perf | Offline | Output type | License | Fit Y/N |
|---|---|---|---|---|---|---|---|---|---|
| **CesiumJS** | Yes (quantized-mesh / ArcGIS elevation) | Yes (WMTS/XYZ/ArcGIS) | Yes (built-in Clock + Timeline + CZML) | Partial (no native volume render; billboards/particles only) | Strong (LOD streaming globe) | Partial (code is local; tiles streamed) | Interactive web globe | Apache-2.0 | **Y** |
| deck.gl / kepler.gl | Partial (TerrainLayer heightmaps) | Yes (TileLayer/BitmapLayer) | Yes (data-driven time filter) | Partial (point/column, no true volume) | Strong (GPU layers) | Partial | Interactive web layers | MIT | N (less turnkey globe+terrain+timeline) |
| three.js | DIY (build mesh yourself) | DIY (texture mapping) | DIY (manual) | Yes (custom shaders/raymarching) | Strong but all hand-built | Partial | Interactive web / custom | MIT | N (too much geospatial plumbing) |
| MapLibre GL JS | Yes (`setTerrain`, raster-DEM) | Yes (raster/vector sources) | Partial (feature-state / frame loop) | No | Strong | Partial | Interactive web map/globe | BSD-3-Clause | N (terrain yes, but weaker true-globe + CZML time model) |
| Blender + GIS addons | Yes (import DEM) | Yes (texture) | Yes (keyframes) | Yes (true volumetrics) | N/A (not browser) | Yes (fully local) | Rendered images / video | GPL (Blender) | N as primary (offline render only, no interactive browser app) |
| Unreal / Unity | Yes (+ Cesium plugin) | Yes | Yes | Yes | N/A browser; heavy runtime | Yes | Native app / baked video | Proprietary EULA | N (not available in-sandbox; huge toolchain) |
| PyVista / VTK | Yes | Yes | Yes | Yes (excellent true volume) | N/A (desktop) | Yes | Desktop windows / images | BSD | N (**not installable in-sandbox**) |
| Plotly 3D | No (surface meshes only) | No real imagery drape | Yes (frames/slider) | Partial (isosurface/volume traces) | OK (small data) | Partial | Interactive web charts | MIT | N (chart-grade, not geospatial globe) |

---

## 2. Decision

**Primary stack = an interactive CesiumJS web application.**

CesiumJS is the only option that delivers *all* hard requirements out of the box
in the user's browser: a real WGS-84 globe, streamed real-world terrain
(quantized-mesh), draped real satellite imagery (WMTS/XYZ/ArcGIS providers),
a first-class time model (`Clock` + `Timeline` widget + CZML time-dynamic
properties), and 3D overlay geometry via `Entity`, `Primitive`, and CZML. It is
permissively licensed (Apache-2.0), so there is no runtime/EULA friction, and it
builds cleanly with the available Node.js + pnpm toolchain. The alternatives each
miss a required capability or the environment: **deck.gl/kepler.gl** and
**MapLibre GL JS** can do terrain + imagery but have no comparable turnkey
globe-plus-timeline-plus-CZML model (MapLibre's time story is a manual frame
loop); **three.js** would mean hand-building every geospatial subsystem;
**Blender** and **Unreal/Unity** are offline/native renderers (and not
installable in-sandbox), so they cannot be the interactive browser deliverable;
**PyVista/VTK** is unavailable here (no VTK) and is desktop-only; **Plotly 3D** is
chart-grade and cannot drape real imagery on a real globe. CesiumJS is weakest at
*true volumetric* rendering, which we therefore handle as an optional, clearly
separate local Blender pass (§3c).

---

## 3. Concrete Pipeline

### (a) Interactive Cesium app

**Serve:** `pnpm` + **Vite** static build (`pnpm build` → `dist/`, served by any
static server). A plain CDN `<script>` tag + `http-server` is the zero-build
fallback. Vite is preferred because `vite-plugin-cesium` wires Cesium's static
assets (`Workers/`, `Assets/`, `Widgets/`) automatically.

**Terrain — NO Cesium ion token required (default path):**
Use Esri's public ArcGIS World elevation service via
`ArcGISTiledElevationTerrainProvider`:

```js
import { Viewer, ArcGISTiledElevationTerrainProvider } from "cesium";

const viewer = new Viewer("cesiumContainer", {
  // no ion token needed; disable the ion default imagery/terrain:
  baseLayer: false,
  timeline: true,
  animation: true,
});

// Token-free real terrain (verify endpoint still public on 2026-10-10):
viewer.terrainProvider = await ArcGISTiledElevationTerrainProvider.fromUrl(
  "https://elevation3d.arcgis.com/arcgis/rest/services/WorldElevation3D/Terrain3D/ImageServer"
); // verify
```

Fallbacks for terrain if that endpoint is unavailable: flat
`EllipsoidTerrainProvider` (no real relief), or self-host a quantized-mesh tileset.

**Terrain — ion upgrade (optional):** set `Cesium.Ion.defaultAccessToken` and use
`await Cesium.createWorldTerrainAsync()` for Cesium World Terrain (higher quality,
global, requires a free ion token).

**Imagery (draped on terrain):**

```js
import { ImageryLayer, UrlTemplateImageryProvider, WebMapTileServiceImageryProvider } from "cesium";

// Esri World Imagery (live; attribution required; exportTilesAllowed=false → cannot bundle tiles)
viewer.imageryLayers.add(ImageryLayer.fromProviderAsync(
  Promise.resolve(new UrlTemplateImageryProvider({
    url: "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    credit: "Imagery © Esri, Maxar, Earthstar Geographics",
    maximumLevel: 19,
  }))
));

// Sentinel-2 cloudless (EOX s2cloudless) via WMTS — verify current layer/version string
viewer.imageryLayers.add(ImageryLayer.fromProviderAsync(
  WebMapTileServiceImageryProvider.fromUrl ?  // guard across API variants // verify
  undefined : undefined
));
// Plain config form:
const s2 = new WebMapTileServiceImageryProvider({
  url: "https://tiles.maps.eox.at/wmts",      // verify
  layer: "s2cloudless-2020_3857",             // verify exact layer id/year
  style: "default",
  format: "image/jpeg",
  tileMatrixSetID: "g",                        // verify
  credit: "Sentinel-2 cloudless © EOX IT Services",
});
viewer.imageryLayers.add(new ImageryLayer(s2));
```

> Attribution note: Esri World Imagery is a usable *live* basemap but
> `exportTilesAllowed=false` — tiles may **not** be bundled/redistributed offline.
> Keep all credits visible in the Cesium credit display.

**3D overlay geometry & layers:** build layers as `Entity` collections
(`viewer.entities`) for convenience, or `Primitive`/`GroundPrimitive` for large
batched geometry, or load **CZML** documents (`CzmlDataSource.load`) when the
layer is time-dynamic. Toggle layers by grouping entities per
`CustomDataSource` and flipping `.show`.

**Time animation:** drive it with the built-in clock + timeline:

```js
import { JulianDate, ClockRange } from "cesium";
viewer.clock.startTime  = JulianDate.fromIso8601("2026-01-01T00:00:00Z");
viewer.clock.stopTime   = JulianDate.fromIso8601("2026-01-02T00:00:00Z");
viewer.clock.currentTime= viewer.clock.startTime.clone();
viewer.clock.clockRange = ClockRange.LOOP_STOP;
viewer.clock.multiplier = 1800;
viewer.timeline.zoomTo(viewer.clock.startTime, viewer.clock.stopTime);
```

Time-dynamic entity properties (`SampledPositionProperty`, `TimeIntervalCollectionProperty`)
or CZML `availability`/interval samples make overlays appear/animate per the clock.

### (b) Cinematic VIDEO — recorded LOCALLY by the user

No headless 4K/WebGL video export is possible in-sandbox. Two local options:

**Option B1 — OBS Studio (simplest, recommended):**
1. Run the app locally (`pnpm dev` or serve `dist/`), open in a browser.
2. In the app, trigger a scripted camera tour: a sequence of
   `viewer.camera.flyTo({ destination, orientation, duration })` calls chained via
   their `complete` callbacks (or `viewer.flyTo(entity)`).
3. OBS → Display/Window Capture of the browser → Start Recording → MP4.
   Set OBS canvas to 3840×2160 @ 60 fps for 4K.

**Option B2 — Deterministic per-frame dump + ffmpeg (frame-accurate):**
Render on a fixed clock step, grab the canvas each frame to PNG, then assemble.

```js
// Pseudocode run in the browser's console / a dev build button:
viewer.useDefaultRenderLoop = false;         // we drive frames manually
const fps = 60, seconds = 20, total = fps * seconds;
const dtSec = 1.0 / fps;
for (let i = 0; i < total; i++) {
  // advance clock deterministically
  viewer.clock.currentTime = Cesium.JulianDate.addSeconds(
    viewer.clock.startTime, i * dtSec, new Cesium.JulianDate());
  updateCameraForFrame(i, total);            // your tour function
  viewer.scene.render();                     // single synchronous frame
  const dataUrl = viewer.canvas.toDataURL("image/png");
  downloadPng(dataUrl, `frame_${String(i).padStart(5, "0")}.png`); // save locally
}
```

Then on the user's machine (local ffmpeg, external to this sandbox):

```bash
ffmpeg -framerate 60 -i frame_%05d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 18 tour.mp4
```

> `viewer.canvas.toDataURL` requires `contextOptions: { webgl: { preserveDrawingBuffer: true } }`
> in the `Viewer` constructor so the buffer is readable after render.

### (c) OPTIONAL — local Blender volumetric smoke (clearly optional)

For true volumetric fields (smoke, plume, cloud) that Cesium cannot render
natively: do this **locally**, outside the sandbox. Export the georeferenced DEM
patch + an overlay texture, import into Blender (BlenderGIS / plain mesh), add a
**Domain + Flow** Mako/Mantaflow smoke sim or a volume shader, and render with
Cycles to a PNG sequence, then ffmpeg it the same way as B2. This is an
offline cinematic add-on only; it is **not** part of the interactive browser app
and is **not** runnable in-sandbox.

---

## 4. Dependency List (pinned)

JS (install with `pnpm add`):

| Package | Version | Verified? |
|---|---|---|
| `cesium` | **1.146** | Verified (GitHub release API, 2026-10-10) |
| `vite` | `^6` (latest; e.g. 6.x) | **verify** |
| `vite-plugin-cesium` | `^1.2` | **verify** |
| `http-server` (CDN/no-build fallback) | `^14.1` | **verify** |

External tools (installed on the **user's machine**, not in-sandbox):

| Tool | Version | Verified? |
|---|---|---|
| OBS Studio | latest | **verify** |
| ffmpeg | latest | **verify** |
| Blender (optional §3c) | latest LTS | **verify** |

Minimal `package.json` scripts:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "serve": "http-server ./dist -p 8080"
  }
}
```

> Only `cesium@1.146` is confirmed. Every version marked **verify** must be
> pinned to a real published version at install time — do not ship a fabricated
> number.

---

## 5. What We CANNOT Do In-Sandbox (honest limits)

- **No headless cinematic/4K video export in-sandbox.** There is no headless
  WebGL recorder here; all video is produced on the user's own machine (OBS or
  per-frame PNG + ffmpeg, §3b).
- **No GPU/CUDA, no Blender/Unreal/Unity, no PyVista/VTK, no matplotlib** in this
  sandbox — so true volumetric rendering (§3c) is **local-only**.
- **No GDAL/rasterio** here — any DEM/raster *preprocessing* that needs them must
  be done on the user's machine; the Cesium app streams terrain/imagery live
  instead of preprocessing locally.
- **Cannot bundle Esri World Imagery tiles offline** (`exportTilesAllowed=false`);
  the app depends on live tile endpoints + network access, and attribution must
  stay visible.
- Rendering performance and the actual WebGL capability live in the **user's
  browser**, not here; the sandbox only builds and serves static assets.
