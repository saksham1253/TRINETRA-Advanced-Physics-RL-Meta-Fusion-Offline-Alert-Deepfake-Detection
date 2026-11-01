# TRINETRA / HIMKAVACH — Phase-1 Part A Visualization Research

Research-grade reference for a cinematic, fully-3D geospatial data-layering animation
(Himalayan disaster + wildfire early-warning). All web sources below were fetched directly
with the `web_fetch` tool and returned live content on the access date. Fetched content was
treated as untrusted data; takeaways are paraphrased in my own words. No citation here is
fabricated.

Access date for every row: **2026-10-10**

---

## Sources (verified)

| # | Source | URL / DOI | Accessed | One-line takeaway (my words) |
|---|--------|-----------|----------|------------------------------|
| 1 | Matplotlib — "Choosing Colormaps in Matplotlib" | https://matplotlib.org/stable/users/explain/colors/colormaps.html | 2026-10-10 | Defines the four colormap classes (sequential / diverging / cyclic / qualitative) and shows that perceptually-uniform maps (viridis, plasma, inferno, magma, cividis) rise monotonically in CIELAB lightness L\*, unlike jet/turbo/rainbow whose L\* zig-zags. |
| 2 | Fabio Crameri — Scientific colour maps | https://www.fabiocrameri.ch/colourmaps/ | 2026-10-10 | A curated family of colour-blind-friendly, perceptually-ordered scientific colour maps (batlow, roma, vik, oleron, lajolla, etc.) built so that lightness carries the data order and no false structure is introduced. |
| 3 | Peter Kovesi — ColorCET (Perceptually Uniform Colour Maps) | https://colorcet.com/ | 2026-10-10 | Catalogues linear / diverging / rainbow / cyclic / isoluminant / colour-blind maps; demonstrates that vendor rainbow maps hide features in "perceptual dead zones" and that isoluminant maps are the correct partner for relief shading. |
| 4 | Peter Kovesi — "Good Colour Maps: How to Design Them" | https://arxiv.org/abs/1509.03700 — DOI 10.48550/arXiv.1509.03700 | 2026-10-10 | The governing design rule: the magnitude of incremental change in perceptual *lightness* must be uniform; CIELAB is only perceptually uniform at low spatial frequency, so maps must be tuned for that. |
| 5 | ColorBrewer 2.0 (Brewer & Harrower, Penn State) | https://colorbrewer2.org/ | 2026-10-10 | Cartographer-tested discrete schemes with explicit "colorblind safe", "print friendly" and "photocopy safe" filters, organised as sequential / diverging / qualitative for a chosen number of classes. |
| 6 | van der Walt & Smith — mpl colormaps (viridis design) | https://bids.github.io/colormap/ | 2026-10-10 | Origin story of viridis/magma/inferno/plasma: designed to be analytically perceptually-uniform in CAM02-UCS *and* when converted to greyscale, and robust under deuteranopia simulation; jet fails all three. |
| 7 | NASA Earthdata — Worldview | https://www.earthdata.nasa.gov/data/tools/worldview | 2026-10-10 | Operational interactive browser of layered near-real-time satellite imagery (incl. active-fire/thermal layers from VIIRS/MODIS via FIRMS); a working model for stacking EO layers with time control. |
| 8 | ESA — Copernicus | https://www.esa.int/Applications/Observing_the_Earth/Copernicus | 2026-10-10 | Sentinel missions and ESA "Earth from Space" products show house conventions for annotated false-colour and polarised-radar hazard imagery (eruptions, typhoons, glaciers). |
| 9 | NOAA — Science On a Sphere | https://sos.noaa.gov/ | 2026-10-10 | 600+ curated planetary datasets rendered on a globe for layered Earth-system storytelling; the SOS/SOSx model = one coherent globe, swappable data layers, narration-driven pacing. |
| 10 | Cesium — CesiumJS | https://cesium.com/platform/cesiumjs/ | 2026-10-10 | Open-source WGS84 3D-globe engine: streams 3D Tiles, glTF models, draped imagery+terrain layers, vector/geometry (KML/GeoJSON/CZML) and time-dynamic data — a concrete toolchain for our build. |
| 11 | Hullman, Resnick & Adar — Hypothetical Outcome Plots | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0142444 — DOI 10.1371/journal.pone.0142444 | 2026-10-10 | Animating a finite set of individual draws (HOPs) lets viewers judge probability by counting; it beat error bars and violin plots for multi-variable reliability inferences. |

**Could NOT verify (fetch failed or empty):**
- **NASA Scientific Visualization Studio** (`svs.gsfc.nasa.gov`, several paths incl. `/`, `/about/`, `/gallery/`, `/4997`) — every request returned a network `fetch failed`. SVS techniques below are therefore described from the directly-verified analogues (NASA Earthdata Worldview, ESA Copernicus, NOAA SOS) rather than attributed to an SVS page I could not open.
- **USGS 3D Elevation Program (3DEP)** (`usgs.gov/.../3d-elevation-program`) — returned HTTP 202 with an empty body; no content to cite.
- **Crameri, Shephard & Heron, "The misuse of colour in science communication," _Nature Communications_ 11, 5444 (2020)** (`nature.com/articles/s41467-020-19160-7`) — direct fetch failed. The full citation is cross-referenced on the verified ColorCET page (source 3); I treat it as a known reference but keep it out of the verified table because I did not open it myself.
- Web search was unavailable this session (no API key), so all verification was via direct `web_fetch`.

---

## 1. How leading agencies present LAYERED Earth-observation data in 3D

Directly observed from the verified NASA Earthdata Worldview, ESA Copernicus, and NOAA Science On a Sphere sources, plus the CesiumJS engine. (NASA SVS could not be opened; its well-known patterns are reflected where they match these verified analogues.)

**Progressive disclosure / layer stacking.** Worldview's model is a single basemap globe with *independently toggled, re-orderable, opacity-controlled* layers (true-colour, thermal/active-fire, aerosol, etc.) bound to a time slider. Build implication: never show all layers at once — introduce them one at a time, each with its own fade-in, and keep a persistent "layer stack" state the camera can refer back to.

**One coherent base, swappable thematic layers (NOAA SOS).** SOS keeps a single animated globe and swaps >600 datasets onto it; the globe is the constant, data is the variable. For us: fix the Himalayan terrain globe as the spatial anchor and treat hazard fields (fire radiative power, smoke, risk) as layers that arrive and depart over it.

**Focus-plus-context.** ESA "Earth from Space" and Worldview both frame a full-disk / regional context then push into the event (eruption plume, typhoon, glacier). Technique: establish a wide context shot, then dolly/zoom to the area of interest while keeping a small inset or a dimmed surrounding so the viewer never loses global location.

**Labelling & annotation conventions.** ESA products use sparse, high-contrast captions naming the sensor, date, and phenomenon; false-colour/polarised views always state the encoding ("false-colour", "radar"). Rule for us: every layer entrance carries a short provenance caption (sensor • date • quantity • units) and, for any non-literal colour mapping, an explicit "false-colour / modelled" tag.

**Pacing.** SOS and the ESA video gallery are narration-paced — a layer dwells long enough to be read before the next change. Default dwell ≥ 3–4 s per newly introduced layer before adding another.

**Colour grading.** Agency EO stills favour a desaturated, neutral basemap so that the thematic/false-colour layer is the brightest, most saturated element in frame. We should grade terrain/imagery base toward low-saturation neutral and reserve high chroma for the active hazard layer.

---

## 2. 3D geovisualization, spatio-temporal & multi-modal layered techniques

Grounded in the verified CesiumJS feature set (draped imagery + terrain, 3D Tiles, glTF models, vector geometry, time-dynamic visualization) and standard geovis practice.

- **Draping imagery on terrain.** Texture satellite/false-colour imagery onto a DEM (e.g. Cesium World Terrain or a Himalayan DEM). Keep vertical exaggeration modest (≈1.3–2×) — enough to read ridgelines and valleys that channel fire/landslide without caricaturing the Himalaya.
- **Vertical layer separation / exploded views.** Lift each thematic layer to its own altitude shell above the terrain (terrain → fuel/vegetation → fire radiative power → smoke → risk/probability cap). An exploded stack, briefly separated along the vertical axis then re-collapsed onto the surface, communicates "these are distinct data planes over the same ground."
- **2.5D extrusion.** Extrude discrete quantities as prisms/columns from footprints (e.g. per-cell fire radiative power, population-at-risk, station readings). Height = magnitude; colour = a second variable (sequential colormap). Good for sparse, polygon/point data where a continuous field would be misleading.
- **Volume rendering of atmospheric fields.** Smoke/plume and aerosol are genuinely volumetric: render as semi-transparent participating media (ray-marched density volume) rather than a flat overlay, with opacity ∝ concentration and a soft emissive tint. This is the correct modality for the smoke-density layer and reads as "atmosphere," not "paint."
- **Multi-modal registration.** All layers must share one WGS84/terrain reference frame (CesiumJS enforces this) so optical, thermal, radar and modelled fields co-register exactly; mis-registration between layers is the most common credibility killer.
- **Spatio-temporal.** Bind every field to a clock (CZML-style time-dynamic data). Animate the hazard evolving over terrain; use a persistent, readable time/date HUD and a timeline scrubber so the viewer always knows "when."

---

## 3. Colormap & perception — perceptually-uniform, colorblind-safe choices

**Why perceptually-uniform beats jet/rainbow (sources 1, 3, 4, 6):**
- The dominant perceptual channel is *lightness* (L\*). Viridis-family maps increase L\* monotonically, so equal data steps look like equal perceptual steps (source 1, 6).
- Jet/rainbow/turbo have non-monotonic L\* with reversals at yellow and red → "perceptual flat spots" that can hide a feature as large as 1/10 of the data range, and "perceptual discontinuities" that fabricate false edges (sources 3, 4).
- Rainbow maps also collapse under the common deuteranopia; viridis was explicitly validated against colour-blind simulation and greyscale conversion (source 6).
- Governing rule (Kovesi, source 4): make the *increment* of perceptual lightness uniform along the map.

**Sequential vs diverging (source 1):**
- **Sequential** (single-hue-ish, monotonic L\*) for ordered data with no meaningful midpoint.
- **Diverging** (two hues meeting at a neutral centre, L\* up-then-down) only when there is a true critical reference value (e.g. anomaly vs baseline, deviation around zero). Note the small perceptual flat spot at a diverging map's centre (source 3) — don't put the most important values there.
- **Cyclic** (twilight; Kovesi CET-C) for wrap-around quantities such as wind *direction* / phase (sources 1, 3).

**Recommended colormaps per TRINETRA layer:**

| Layer | Nature | Recommended map(s) | Rationale |
|-------|--------|--------------------|-----------|
| Elevation / relief | sequential, often paired with hillshade | Crameri **oleron** (true topographic diverging land/sea) or **batlow**; or Kovesi isoluminant **CET-I** *under* relief shading | Isoluminant maps don't fight the hillshade's own lightness pattern (sources 3, 4); oleron encodes terrain with a sea-level pivot. |
| Temperature | sequential, or diverging about a baseline | **inferno** / **magma** (hot sequential); **vik** or **RdBu** if showing anomaly about a reference | Perceptually-uniform heat ramp (source 1); diverging only when a true zero/baseline exists (source 1). |
| Wind speed | sequential (magnitude) | **viridis** or Crameri **batlow** | Monotonic, colour-blind-safe magnitude ramp. (Wind *direction* → cyclic **twilight**/CET-C, source 1.) |
| Fire Radiative Power (FRP) | sequential, high-energy | **inferno** (or **magma**) | Dark→bright-yellow ramp reads intuitively as "energy/heat," perceptually uniform, strong on dark terrain (sources 1, 6). |
| Smoke density | sequential, low-chroma over volume | **grey**/neutral density ramp, or desaturated **cividis**, with opacity ∝ density | Smoke should read as translucent medium; low chroma avoids competing with the fire layer; cividis is extra-safe for CVD (source 1). |
| Probability / risk (0–1) | sequential, bounded | **viridis** or **cividis** | Bounded, ordered, colour-blind-safe; viewers read 0→1 as dark→bright consistently (sources 1, 6). |
| Uncertainty | sequential, muted | encode via **opacity / desaturation** on top of the risk map, or Crameri **lajolla**/greyscale | Keep hue for the quantity and let uncertainty ride a separate, low-salience channel (see §4). |

Discrete class breaks (e.g. risk categories Low/Med/High/Extreme): use **ColorBrewer** sequential schemes with the "colorblind safe" filter on (source 5).

---

## 4. Visualizing UNCERTAINTY

- **Hypothetical Outcome Plots / ensemble animation (source 11).** For model-driven forecasts (fire spread, flood/landslide), animate a finite set of plausible draws (ensemble members / Monte-Carlo realisations) instead of a single mean + error bar. Hullman et al. showed HOPs let non-experts judge probability by counting frames and beat error bars/violin plots for multi-variable reliability. Build: cycle through ~10–20 ensemble "futures" of the hazard footprint; the flicker *is* the uncertainty.
- **Translucent envelopes / bands.** Render the ensemble spread as a semi-transparent "cone/envelope of possibility" around the central estimate (plume reach, fire perimeter), outer edge = low likelihood.
- **Opacity / saturation encoding.** Keep hue for the primary quantity (risk) and push uncertainty onto a *secondary* visual channel: high-confidence cells fully saturated/opaque, low-confidence cells desaturated/translucent ("value-suppressing" style). This avoids inventing a second competing colour scale.
- **Don't bury the critical zone.** Because diverging-map centres and translucent regions are low-salience (source 3), make sure the decision-relevant threshold (e.g. "evacuate above risk 0.7") is drawn with an explicit contour/isoline, not left to colour alone.

---

## 5. Visual clutter, layer-occlusion & label legibility in 3D

- **Data-ink discipline.** Every mark must carry data. Strip graticules, bounding boxes, redundant gridlines and heavy chrome; let the terrain + active hazard layer dominate. (Tufte's data-ink principle — well-established; I did not fetch a Tufte page this session so I cite it only as general practice.)
- **Occlusion management.** In 3D, stacked translucent layers mutually hide each other. Mitigations: (a) show at most ~2–3 thematic layers simultaneously; (b) use the exploded vertical-shell separation (§2) when more layers must coexist; (c) depth-fade or dim lower layers when a higher layer is the current focus; (d) use additive/screen blending for emissive fields (fire glow) so they read through smoke.
- **Isoluminant + relief (sources 3, 4).** When draping a colour field over shaded terrain, use an isoluminant colour map so the relief shading supplies structure and colour supplies the data value, without the two lightness signals interfering.
- **Label legibility in 3D.** Labels in perspective shrink, rotate and collide. Rules: render labels as *billboarded* (screen-facing), constant-pixel-size text; give every label a halo/outline or semi-opaque pill background for contrast against any terrain colour; apply declutter/priority culling so only the most important labels survive at a given zoom; anchor floating labels with a thin leader line to their 3D point; keep legends and the time/units HUD in fixed 2D screen space, not glued to the moving globe.
- **Legend rules.** One legend per *currently visible* data layer; show the colourbar with units and the min/max; mark the decision threshold on the bar; fade a legend out when its layer leaves.

---

## 6. Cinematic scientific storytelling — camera choreography & pacing

Patterns consistent with the verified agency video/globe products (ESA Copernicus video gallery, NOAA SOS narration model) and standard 3D-camera practice.

- **Establish → approach → reveal → compare → resolve.** Open on a wide Himalayan context (slow orbit), dolly in to the area of interest, reveal layers one at a time, compare scenarios/ensembles, pull back to summarise.
- **Core camera moves:**
  - *Orbit* (slow azimuthal rotation) around the area of interest to convey 3D terrain relief — the single most effective move for selling the "fully-3D" claim.
  - *Dolly / push-in* to transition from context to focus (focus-plus-context, §1).
  - *Tilt / crane* to lift from a top-down map view to an oblique 3D view as volumetric layers (smoke) are introduced — the tilt motivates *why* 3D is needed.
  - *Locked-off hold* while a layer animates in time, so motion in the data isn't confused with camera motion.
- **Easing.** Use ease-in-ease-out (smoothstep / cubic) on every camera move and layer fade; never linear starts/stops. Keep angular velocity low during orbits so viewers can still read labels.
- **Pacing per layer.** Introduce one layer per "beat"; hold ≥3–4 s after a layer settles before the next change (matches agency narration pacing, §1). Give the ensemble/uncertainty beat extra time because the eye must integrate across animated frames (source 11).
- **Motion hygiene.** One primary motion at a time — either the camera moves or the data animates, rarely both at full speed. Reserve the fastest motion for the climactic hazard-evolution beat.

---

## Design implications for our build (summary)

Build on a single WGS84 terrain globe (CesiumJS-style: draped Himalayan imagery on a modestly exaggerated DEM) as a fixed spatial anchor, and treat every hazard field as an independently timed, opacity-controlled layer that is disclosed one beat at a time with a provenance caption and its own fading, threshold-marked legend. Encode quantities with perceptually-uniform, colour-blind-safe maps — **inferno/magma** for fire radiative power and temperature, **viridis/cividis** for risk/probability (0–1) and wind speed, an **isoluminant/oleron-style** map under relief for elevation, and a low-chroma density ramp with opacity-coded, volumetrically ray-marched **smoke** — never jet/rainbow, whose non-monotonic lightness hides and fabricates features. Represent uncertainty on a *separate* channel (opacity/desaturation, translucent envelopes, and HOP-style animated ensemble "futures") while drawing decision thresholds as explicit contours so colour alone never carries a life-safety cut. Keep ≤2–3 layers visible at once (exploded vertical shells when more must coexist), hold data-ink discipline, use billboarded haloed labels with fixed-screen legends/time HUD, and choreograph slow eased orbit/dolly/tilt moves — one motion at a time, ≥3–4 s per beat — so the camera proves the terrain's three-dimensionality exactly when the volumetric layers need it.
