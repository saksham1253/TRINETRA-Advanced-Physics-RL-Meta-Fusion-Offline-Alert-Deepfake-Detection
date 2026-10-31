# STORYBOARD.md — cinematic layer-by-layer reveal (TRINETRA/HIMKAVACH)

AOI: **Uttarakhand Himalaya, 2021 pre-monsoon forest-fire season** · bbox `78.5, 29.5, 80.2, 30.8` ·
center ≈ `lon 79.35, lat 30.15` · event window **2021-04-25 → 2021-05-12**.
Stack: interactive **CesiumJS v1.146** (`STACK_DECISION.md`). Layers **L0–L12** exactly as in `LAYER_MAP.md`.
Every caption carries the **REAL / SIMULATED / ILLUSTRATIVE** tag + provenance (`DESIGN_SPEC.md §tag-system`).
Camera is expressed as Cesium `destination` (lon, lat, height-m) + `orientation` (heading°, pitch°, roll°).

> Honesty: no performance number is spoken or shown that was not measured (none were — `FINAL_REPORT`).
> Shots whose data needs a key are tagged **[DATA-PENDING]** and are **skipped gracefully** (the app shows a
> "data not loaded — see HOW_TO_REPRODUCE" placard) rather than faking anything.

---

## Running time
- 15 shots, layer focus 3–8 s each + transitions ≈ **~2 min 10 s** guided tour (≈130 s).
- With the exploded-stack inspection hold (+12 s) and the DFD finale (+14 s): **≈ 2 min 36 s** total.
- Interactive mode has no fixed runtime; the tour is one playable timeline (see §Controls).

---

## S0 — Title / cold open  (4 s)
- **Camera:** full globe, `destination (79.35, 30.15, 20 000 000)`, `pitch -90`. Slow 6°/s auto-orbit.
- **Entry:** fade from black; title lower-third fades in then out.
- **Caption:** `TRINETRA / HIMKAVACH — multi-hazard advisory early-warning · data-stack reveal`
- **Narration:** "A Himalayan early-warning data stack — shown one real layer at a time."
- **After:** globe stays as context; begin dolly.

## S1 — L0 Earth context → fly to AOI  (6 s)
- **Camera:** dolly `(79.35, 30.15, 20 000 000) → (79.35, 29.9, 450 000)`, ease-in-out, final `pitch -55`.
- **Entry:** basemap sharpens as tiles stream; AOI bbox outline draws on.
- **Caption:** `REAL: Esri World Imagery (live) / Sentinel-2 cloudless · terrain AWS Terrain Tiles · WGS-84`
- **Narration:** "Uttarakhand, central Himalaya — the deployment region."
- **After:** basemap persists at full; AOI outline dims to a thin guide.
- *Note:* recorded video uses the **open** basemap (Sentinel-2 cloudless), not Esri (`LICENSES.md §1`).

## S2 — L1 Terrain & relief  (6 s)
- **Camera:** descend to `(79.2, 30.05, 90 000)`, `pitch -35`; slow 15°/s orbit CW to read the ridgelines.
- **Entry:** vertical-exaggeration label appears ("VE ×1.0"); relief shading ramps up.
- **Caption:** `REAL: Copernicus DEM GLO-30, 30 m, 2021 · slope derived · VE ×1.0`
- **Narration:** "Real 30-metre terrain — the slope and aspect that drive every hazard here."
- **After:** terrain stays; slope overlay fades to 35% opacity.

## S3 — L2 Land cover / fuel  (5 s)
- **Camera:** hold at `(79.2, 30.05, 70 000)`, gentle 10°/s orbit; slight tilt-up to 40°.
- **Entry:** WorldCover classified raster wipes on across the terrain (N→S).
- **Caption:** `REAL: ESA WorldCover 10 m 2021 · © ESA WorldCover project / modified Copernicus Sentinel data`
- **Narration:** "Forest and fuel classes — what can burn, and where."
- **After:** land cover drops to 30% opacity under later layers.

## S4 — L3 Built environment & exposure  (5 s)
- **Camera:** dolly in to a valley settlement `(79.45, 30.0, 18 000)`, `pitch -45`.
- **Entry:** OSM building footprints extrude upward (2.5-D grow); roads draw as polylines; population surface fades in.
- **Caption:** `REAL: OSM © OpenStreetMap contributors (ODbL) · WorldPop CC-BY`
- **Narration:** "Who is exposed — buildings, roads, population. Sparse in the rural Himalaya; shown as-is."
- **After:** buildings/roads persist; population surface dims to 25%.

## S5 — L4 Atmosphere (wind)  (6 s)  **[DATA-PENDING: ERA5-Land key]**
- **Camera:** climb to `(79.3, 30.05, 120 000)`, `pitch -40`; drift W→E with the flow.
- **Entry:** animated wind streamlines/particles spawn over the terrain; Cesium `Clock` starts (2021-04-25).
- **Caption:** `REAL: ERA5-Land hourly, 2021 · Generated using Copernicus Climate Change Service information`
- **Narration:** "The driving wind field — it tilts plumes and governs fire spread."
- **After:** particles continue at low density as ambient context.
- *If no extract loaded:* skip to S6; show the DATA-PENDING placard (no fabricated wind).

## S6 — L5 Real fire observations  (7 s)  **[DATA-PENDING: FIRMS MAP_KEY / archive CSV]**
- **Camera:** orbit the main fire cluster `(79.5, 30.1, 60 000)`, 12°/s CW, slow push-in to 40 000 m.
- **Entry:** FIRMS hotspots appear as time-animated billboards sized by FRP (inferno); SWIR composite drapes under them; timeline scrubs 04-25→05-12.
- **Caption:** `REAL: NASA FIRMS VIIRS/MODIS active fire, 2021 (archive) · GIBS thermal anomalies`
- **Narration:** "The actual 2021 fire signal from satellite — hotspots through time."
- **After:** hotspots thin to the peak-day subset as context.
- *If no CSV:* show DATA-PENDING placard; proceed (never synthesize hotspots).

## S7 — L6 WS1 physics + meta-fusion (scientific core)  (8 s)
- **Camera:** tilt **up** from the ridge to reveal a vertical plume `(79.52, 30.1, 25 000)`, `pitch -20`; slow 8°/s orbit.
- **Entry:** (a) fire-plume temperature column rises with a translucent smoke volume over an ignition point; (b) landslide factor-of-safety surface drapes on the DEM (FS<1 glows); (c) fused-risk surface with a translucent uncertainty band.
- **Caption:** `SIMULATED: Heskestad plume + Iverson/FS landslide (TRINETRA numpy core) · params in panel · NOT an observation, NOT a measured skill`
- **Narration:** "Our physics models — run in code — produce a hazard field with an uncertainty envelope. Simulated, with parameters shown."
- **After:** fused-risk surface persists at 40%; plume loops subtly.

## S8 — L7 WS4 CCTV  (5 s)
- **Camera:** dolly to a camera node on a ridge `(79.48, 30.08, 6 000)`, `pitch -10`; frame the FOV cone.
- **Entry:** camera icons drop in; 3-D view-frustum cones unfold; a side panel shows a license-cleared sample frame; a detection box labeled SIMULATED/UNTESTED draws on.
- **Caption:** `REAL: dataset sample (license-permitting) · ILLUSTRATIVE: camera FOV · SIMULATED: detection`
- **Narration:** "Edge fire-smoke cameras — field of view in 3-D. No trained detector exists, so detections are illustrative."
- **After:** FOV cones dim to 20%; panel closes.

## S9 — L8 Dataset layer (registry, honestly)  (6 s)
- **Camera:** pull back to `(79.35, 29.95, 110 000)`, `pitch -55`; floating panels arc beside the globe.
- **Entry:** 3-D dataset panels fade in grouped by modality, each with its provenance caption; arrows link panels → models; a marker shows where spatial-block CV sits.
- **Caption:** `REAL(metadata): DATASETS.md D-IDs · counts as-recorded · licenses UNVERIFIED where tagged`
- **Narration:** "The dataset stack from the registry — counts exactly as recorded, candidates not claimed as downloaded."
- **After:** panels shrink to a docked column on the right.

## S10 — L9 WS2 deepfake / social-media verification  (5 s)
- **Camera:** gentle truck-left, globe to screen-right; DFD nodes anchor on screen-left at `pitch -55`.
- **Entry:** a horizontal flow (ingest → provenance → reverse-search → detector → corroboration → human gate) draws left→right; the 0.40 cap shows as a hard ceiling bar.
- **Caption:** `ILLUSTRATIVE pipeline · REAL(stats): dataset counts · SIMULATED: detector score (cap 0.40)`
- **Narration:** "Social-media information is vetted before it can inform an alert — detector confidence is capped, and it never acts on its own."
- **After:** flow collapses to a single labeled node docked top-left.

## S11 — L10 WS3 tiered offline alerting  (6 s)
- **Camera:** back to the settlement `(79.45, 30.0, 45 000)`, `pitch -50`; slow 8°/s orbit.
- **Entry:** concentric reach rings (siren → LoRa/mesh → cell-broadcast) expand over terrain, intersected with the WorldPop surface; an IP-alert `[INFEASIBLE]` placard flashes then docks.
- **Caption:** `ILLUSTRATIVE: tier reach geometry · REAL: WorldPop exposure · ranges = source-reported, not measured here · public alert is human-gated`
- **Narration:** "Feasible alerting tiers over the real map. Ranges are source-reported scenario geometry — not measured here — and the public alert is human-gated."
- **After:** rings dim to 20%; exposure surface stays faint.

## S12 — L11 WS5 RL advisory routing  (5 s)
- **Camera:** descend to the road graph `(79.44, 30.0, 12 000)`, `pitch -30`; follow a route polyline.
- **Entry:** candidate routes glow along real OSM roads, risk-shaded; an "advisory + shield" badge appears.
- **Caption:** `SIMULATED: rule-baseline advisory routing over REAL OSM roads · no trained policy (by design)`
- **Narration:** "Advisory routing over real roads — from the rule baseline; no learned policy exists, by design."
- **After:** one route stays highlighted as context.

## S13 — Exploded stack (inspection hold)  (12 s)
- **Camera:** pull to `(79.35, 29.7, 160 000)`, `pitch -35`; the layers **separate vertically** into a stack
  (terrain at base, then land cover, exposure, wind, fire, physics, overlays), each on its own floating plane
  with its mini-caption. Slow 6°/s orbit around the stack; brief dolly along the stack top→bottom.
- **Entry:** smooth vertical "accordion" separation (physically motivated ease-out).
- **Caption:** `All layers — REAL (green) vs SIMULATED/ILLUSTRATIVE (amber). Hover any plane for its provenance.`
- **Narration:** "Every layer, separated for inspection — green is real observation or real code output, amber is simulated or illustrative."
- **After:** hold 3 s for reading, then begin collapse.

## S14 — L12 Collapse + all-on + high-level DFD finale  (14 s)
- **Camera:** stack collapses back onto the globe; pull to a hero 3/4 view `(79.35, 29.85, 220 000)`,
  `pitch -45`; final slow 5°/s orbit, subtle push-in.
- **Entry:** all layers on at reduced emphasis; a clean high-level **DFD overlay** draws:
  `sensors/EO → WS1 physics + WS2/WS4 perception → meta-fusion + uncertainty → decision + shield → human-gated advisory → WS3 tiers`.
  The canonical decision rule prints: `level = max(conformal_level(fused_risk, p*), shield_floor), p*≈0.0476`.
- **Caption:** `ILLUSTRATIVE: high-level data flow (see 02 + _CANON) · advisory, human-in-loop, never autonomous`
- **Narration:** "End to end: real observations and physics fuse under uncertainty into a human-gated advisory. Advisory, human-in-the-loop — never autonomous."
- **After:** attributions block holds full-screen 3 s; fade to black.

---

## Interactive controls (parallel to the tour)
- **Timeline scrubber** (Cesium `Timeline` + `Clock`): scrubs the 2021-04-25→05-12 window; drives L4 wind + L5 fire animation.
- **Per-layer toggles**: L0–L12 checkboxes; each shows its REAL/SIM tag + provenance on hover.
- **Opacity sliders**: per layer (0–100%), default values from each shot's "After" state.
- **Tour mode**: plays S0→S14 with captions/narration burned in; pause/step/replay; "jump to layer" chapter list.
- **Basemap switch**: Esri World Imagery (live only) ↔ Sentinel-2 cloudless (video-safe) — default = open source.
- **Graceful skip**: `[DATA-PENDING]` layers render a placard instead of content; the tour auto-skips their focus hold.
