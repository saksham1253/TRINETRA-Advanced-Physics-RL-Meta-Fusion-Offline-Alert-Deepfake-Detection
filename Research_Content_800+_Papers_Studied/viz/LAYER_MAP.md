# LAYER_MAP.md — ordered 3D layers for the TRINETRA/HIMKAVACH data-stack reveal

AOI: **Uttarakhand Himalaya, 2021 pre-monsoon forest-fire season** (bbox 78.5,29.5,80.2,30.8; peak
2021-04-25→05-12). Every layer below maps to something REAL in the project (a verified data source and/or a
project code module), carries a REAL vs SIMULATED tag, and a provenance caption. Sources and their licenses
are in `DATA_SOURCES.md` + `LICENSES.md`; render stack in `STACK_DECISION.md`.

Legend for the "Tag" column:
- **REAL(obs)** — real observation/data from a verified external source, shown as-is.
- **REAL(code)** — real output computed by running our own `trinetra/` numpy code (deterministic).
- **SIMULATED** — a model/physics field or scenario geometry; always labeled SIMULATED + parameters.
- **ILLUSTRATIVE** — conceptual geometry that encodes real structure but is not an observation or a measured
  result; labeled as such (used sparingly, e.g. DFD overlays, dataset panels).

Colormaps follow `RESEARCH.md`: inferno/magma = fire radiative power & temperature; viridis/cividis = risk(0–1)
& wind; oleron/isoluminant over relief = elevation; low-chroma+opacity = smoke; translucent band = uncertainty.

---

## L0 — Earth context (globe → region)
- **Purpose:** open on the whole globe, fly to the Uttarakhand AOI; establish place + scale.
- **Tag:** REAL(obs).
- **Real sources:** Esri World Imagery (live basemap, attribution; NOT in exported video) **or** Sentinel-2
  cloudless / NASA GIBS truecolor (open, video-safe). Terrain = AWS Terrain Tiles (terrarium, token-free).
- **Project link:** `02_system_architecture.md` (deployment geography), AOI rationale in `DATA_SOURCES.md`.
- **Render:** CesiumJS globe; `camera.flyTo` dolly+tilt from space to the AOI bbox.
- **Caption:** "REAL: Esri World Imagery (live) / Sentinel-2 cloudless · terrain AWS Terrain Tiles · WGS-84".
- **Risks:** Esri export restriction → use open basemap for the recorded video.

## L1 — Terrain & relief (3D DEM)
- **Purpose:** reveal the real Himalayan relief that drives every hazard (slope, aspect, drainage).
- **Tag:** REAL(obs).
- **Real sources:** Copernicus DEM GLO-30 (30 m) via Earth Search STAC / S3; AWS Terrain Tiles for the mesh.
- **Project link:** `06_ws1_physics_and_fusion.md` (slope β feeds FS/Iverson), `DATASETS.md` D50/D51.
- **Render:** Cesium terrain + a slope/aspect overlay (ESA WorldCover drape optional); vertical exaggeration
  **stated on screen** (e.g. ×1.0; if exaggerated, label "VE ×N").
- **Caption:** "REAL: Copernicus DEM GLO-30, 30 m, 2021 · slope derived".
- **Risks:** DEM COG read is browser-side; if blocked, fall back to Cesium terrain-only relief.

## L2 — Land cover / fuel context
- **Purpose:** show forest/fuel classes — what burns, where.
- **Tag:** REAL(obs).
- **Real sources:** ESA WorldCover 10 m (2021), CC-BY-4.0.
- **Project link:** fire-physics fuel assumptions in `06` (WS1 fire), `09_ws4_cctv.md` scene context.
- **Render:** classified raster draped on terrain, muted categorical palette (colorblind-safe).
- **Caption:** "REAL: ESA WorldCover 10 m 2021 · © ESA WorldCover project / modified Copernicus Sentinel data".

## L3 — Built environment & exposure
- **Purpose:** who/what is exposed — buildings, roads, population.
- **Tag:** REAL(obs).
- **Real sources:** OpenStreetMap buildings+roads (Overpass, ODbL — rendered output only); WorldPop and/or
  GHSL population grid (CC-BY / © EU).
- **Project link:** `08_ws3_offline_alerting.md` (alert reach vs population), `22` exposure risk.
- **Render:** 2.5-D extruded building footprints; roads as polylines; population as a graduated surface
  (viridis). Keep OSM as a *produced work* (no vector-tile DB redistribution → ODbL-safe).
- **Caption:** "REAL: OSM © OpenStreetMap contributors (ODbL) · WorldPop CC-BY".
- **Risks:** OSM building density is sparse in rural Himalaya — show honestly, don't inflate.

## L4 — Atmosphere (wind / temperature / humidity)
- **Purpose:** the driving weather field; wind governs fire spread + plume tilt (Byram number).
- **Tag:** REAL(obs) — ERA5-Land reanalysis (needs free CDS account) → prebuilt into a small bundled field.
- **Real sources:** ERA5-Land hourly (C3S), DOI 10.24381/cds.e2161bac, for the AOI + dates.
- **Project link:** `06` (U feeds `byram_convection_number`), `04a_DATASETS.md` D05.
- **Render:** animated streamlines / moving particles over terrain (wind), colored by speed (viridis);
  Cesium `Clock`/`Timeline` drives time.
- **Caption:** "REAL: ERA5-Land hourly, 2021 · Generated using Copernicus Climate Change Service information".
- **Risks:** CDS needs an account → ship a small pre-extracted NetCDF/CSV→JSON for the demo; mark the extract
  date. If not extracted, render nothing + note the gap (no fabricated wind).

## L5 — Real fire observations
- **Purpose:** the actual 2021 fire signal — satellite hotspots + thermal/SWIR.
- **Tag:** REAL(obs).
- **Real sources:** NASA FIRMS VIIRS/MODIS active-fire (MAP_KEY; **bundle the archived 2021 AOI CSV** as the
  no-key demo); NASA GIBS VIIRS 375 m thermal-anomalies tiles; Sentinel-2 SWIR (B12/B11/B8A) composite +
  Landsat-8/9 TIRS thermal via Earth Search.
- **Project link:** `09_ws4_cctv.md` (fire signal), `12_evaluation_and_results.md`, `DATASETS.md` fire sets.
- **Render:** FIRMS points as time-animated billboards sized by FRP, colored inferno; SWIR composite drape;
  timeline scrubs the fire progression.
- **Caption:** "REAL: NASA FIRMS VIIRS/MODIS active fire, 2021 (archive) · GIBS thermal anomalies".
- **Risks:** FIRMS host was unreachable to the sandbox fetch tool → the archived CSV must be fetched/verified
  in-browser or supplied; until then this layer is DATA-PENDING, not faked.

## L6 — WS1 physics models + meta-fusion  (the scientific core)
- **Purpose:** show the six physics models + fusion producing a hazard field with an uncertainty envelope.
- **Tag:** **SIMULATED** (computed by running our real `trinetra/` numpy code; labeled with parameters).
- **Real code (REAL(code) origin, SIMULATED field):**
  - Fire: `ws1a_firephys.established_ef` — `plume_centerline_dT`, `flame_height_heskestad`,
    `strouhal_puffing_frequency`, `byram_convection_number` (regime gate), `graybody_radiance`.
  - Geo: `ws1b_geophys.fs.factor_of_safety`, `ws1b_geophys.iverson.transient_head`,
    `ws1b_geophys.caine.caine_exceedance`, `ws1b_geophys.fukuzono` (inverse-velocity).
  - Fusion/decision: `ws5_fusion_rl.fusion_models` / `decision` / `shield` / `ws6_robust.conformal`.
- **Project link:** `06_ws1_physics_and_fusion.md`, `05b_MODELS.md`; canonical p*≈0.0476 (`_CANON`).
- **Render:** (a) a vertical fire-plume temperature column + translucent smoke volume over an ignition point;
  (b) a landslide factor-of-safety surface draped on the DEM (FS<1 highlighted) for a rainfall scenario;
  (c) a fused-risk surface with a **translucent uncertainty band** (conformal interval). Colormaps:
  inferno (plume T), viridis (risk 0–1), opacity for smoke/uncertainty.
- **Caption:** e.g. "SIMULATED: Heskestad plume + Iverson/FS landslide (TRINETRA numpy core) · params shown ·
  NOT an observation, NOT a measured skill".
- **Risks:** parameters must be physically sane (Heskestad flame height goes negative for absurd D) — the
  generator pins realistic per-fire params and records them in the caption + sidecar JSON.

## L7 — WS4 CCTV layer
- **Purpose:** edge fire/smoke cameras — placement, field of view, sample detections.
- **Tag:** REAL(obs) for dataset frames; ILLUSTRATIVE for camera placement; SIMULATED for detection overlay.
- **Real sources:** sample frames from a license-cleared CCTV fire set (PYRONEAR-2025 / FIgLib / D-Fire per
  `04a_DATASETS.md`), shown only if the license permits display; otherwise described, not shown. **No faces.**
- **Project link:** `09_ws4_cctv.md`, FireSmokeNet in `05a_MODELS.md`.
- **Render:** camera icons on terrain with real 3D view-frustum FOV cones; a framed panel showing a sample
  frame; detection boxes labeled SIMULATED/UNTESTED (no trained model → no real detections, per FINAL_REPORT).
- **Caption:** "REAL: dataset sample (license-permitting) · ILLUSTRATIVE: camera FOV · SIMULATED: detection".
- **Risks:** no trained detector exists → detections are illustrative; never claim a measured confidence.

## L8 — Dataset layer (the registry, honestly)
- **Purpose:** show the project's dataset stack from `DATASETS.md` — modality, size, source, splits.
- **Tag:** REAL(obs) metadata; ILLUSTRATIVE for the panel geometry.
- **Real sources:** `DATASETS.md` + `DATASETS_CATALOGUE.md` (164 D-IDs); numbers must match EXACTLY.
- **Project link:** `04_DATASETS.md`, `04a_DATASETS.md`, `12` (spatial-block CV).
- **Render:** floating 3D panels grouped by modality, each with its provenance caption (D-ID, modality, size
  [UNVERIFIED where the registry says so], license tag [V]/[V*]/[D]); arrows to the models they feed; a marker
  where cross-dataset / spatial-block splits sit.
- **Caption:** "REAL(metadata): DATASETS.md D-IDs · counts as-recorded · licenses UNVERIFIED where tagged".
- **Risks:** must not present candidate datasets as downloaded — mirror the docs' honesty.

## L9 — WS2 deepfake / social-media verification
- **Purpose:** how social-media information is vetted before it can inform an alert.
- **Tag:** ILLUSTRATIVE data-flow; REAL(obs) for dataset stats; SIMULATED for detector confidence.
- **Real sources:** dataset stats from `04a` (FaceForensics++ EULA-blocked → stats only, **no media shown**;
  no identifiable faces — privacy rule 7).
- **Project link:** `07_ws2_deepfake.md`, AuthenticityNet in `05a`; reliability cap 0.40 (`_CANON`).
- **Render:** a horizontal data-flow (ingest → provenance → reverse-search → detector → corroboration →
  human gate) as nodes/edges anchored beside the globe; the 0.40 cap shown as a hard ceiling. Rule R19
  "never autonomous" called out.
- **Caption:** "ILLUSTRATIVE pipeline · REAL(stats): dataset counts · SIMULATED: detector score (cap 0.40)".

## L10 — WS3 tiered offline alerting
- **Purpose:** the feasible alert tiers over the real map (siren → LAN/mesh → cell-broadcast → DTN).
- **Tag:** SIMULATED/ILLUSTRATIVE geometry (reach rings), with the IP-alert [INFEASIBLE] verdict surfaced.
- **Real sources/code:** `ws3_alert/*` (siren bus, dtn, cap) — NOTE: **no acoustic range model in code**, so
  reach rings are ILLUSTRATIVE scenario geometry, not a code output; LoRa reach uses source-reported ranges
  only (labeled). Population under reach from WorldPop (REAL).
- **Project link:** `08_ws3_offline_alerting.md` (§08.2 IP infeasible, §08.3 tiers).
- **Render:** concentric reach rings (siren radius, LoRa/mesh reach, cell-broadcast area) over terrain,
  intersected with the WorldPop surface to show people reached; each labeled with its source-reported basis.
- **Caption:** "ILLUSTRATIVE: tier reach geometry · REAL: WorldPop exposure · ranges = source-reported, not
  measured here · public alert is human-gated".
- **Risks:** must NOT present reach as measured — it is scenario geometry; numbers only from cited sources.

## L11 — WS5 RL advisory routing
- **Purpose:** the advisory evacuation/response routing environment over the real road network.
- **Tag:** SIMULATED (policy) over REAL(obs) roads.
- **Real sources/code:** OSM road network (REAL); `ws5_fusion_rl/rl.py` RuleBaselinePolicy (numpy, binary) —
  **no trained RL policy exists** (FINAL_REPORT), so routes come from the rule baseline or are illustrative.
- **Project link:** `10_ws5_rl.md`; shield + p* decision.
- **Render:** candidate routes as glowing polylines on the road graph, risk-shaded; labeled advisory + shield.
- **Caption:** "SIMULATED: rule-baseline advisory routing over REAL OSM roads · no trained policy (by design)".
- **Risks:** no learned policy → do not imply one; show the rule baseline honestly or mark illustrative.

## L12 — Fusion & decision + high-level DFD overlay (finale)
- **Purpose:** collapse all layers into the end-to-end detection→fusion→decision→advisory pipeline, with a
  high-level model DFD (the user explicitly asked for a high-level data-flow of the model).
- **Tag:** ILLUSTRATIVE (DFD) over the live REAL/SIM layers.
- **Real sources/code:** `pipeline/orchestrator.py`, `ws5_fusion_rl/decision.py`, `shield.py`, conformal;
  canonical decision rule `level = max(conformal_level(fused_risk, p*), shield_floor)` (`_CANON`).
- **Project link:** `02_system_architecture.md`, `assets/architecture_diagrams.md`, `06`, `_CANON`.
- **Render:** all layers on at reduced emphasis; a clean high-level DFD (sensors/EO → WS1 physics + WS2/WS4
  perception → meta-fusion + uncertainty → decision + shield → human-gated advisory → WS3 tiers) drawn as an
  overlay graph; then "peel back" the stack (exploded view) and collapse.
- **Caption:** "ILLUSTRATIVE: high-level data flow (see 02 + _CANON) · advisory, human-in-loop, never
  autonomous".

---

## Build order & data dependencies
1. **No-key now:** L0,L1,L2,L3 (Esri/GIBS/terrain/DEM/WorldCover/OSM/WorldPop) — stream live in browser.
2. **Compute now (code):** L6 physics fields via `viz/pipeline/gen_physics_fields.py` → sidecar JSON/CZML.
   L8 dataset panels from `DATASETS.md`. L12 DFD graph (static JSON).
3. **Bundle a small real extract:** L5 FIRMS 2021 AOI archive CSV; L4 ERA5-Land AOI wind extract (both need a
   free key — fetch/verify in-browser or supply; until then DATA-PENDING, never faked).
4. **Illustrative/scenario geometry (labeled):** L7 FOV, L9 DFD, L10 reach rings, L11 routes.

## Honest gaps carried into the build (not to be faked)
- No trained models → no measured detections/skill/ECE/routes (L7,L9,L11 overlays are SIMULATED/ILLUSTRATIVE).
- No acoustic/radio range model in code → L10 reach is scenario geometry with source-reported ranges only.
- FIRMS + ERA5-Land require a free key; sandbox could not fetch FIRMS → those layers are DATA-PENDING until a
  real extract is in hand; the app renders nothing for them meanwhile and says so on screen.
