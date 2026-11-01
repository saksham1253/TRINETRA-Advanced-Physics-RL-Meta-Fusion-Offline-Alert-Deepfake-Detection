# DESIGN_SPEC.md — the "research-grade, not childish" standard (TRINETRA/HIMKAVACH viz)

Enforceable, concrete spec a builder implements directly. Consistent with `LAYER_MAP.md` (L0–L12),
`RESEARCH.md` (colormaps/perception), `STACK_DECISION.md` (CesiumJS v1.146), `LICENSES.md` (attributions),
`STORYBOARD.md` (shots). Target: looks like a NASA SVS / Copernicus / geospatial-intelligence product.
Hard bans: cartoon colors, neon overload, emoji, clip-art icons, bouncy/elastic easing, gratuitous spin,
unmeasured performance numbers, any unlabeled synthetic element.

---

## 1. Palette (dark cinematic geospatial-intelligence)
Design tokens (hex). Dark, restrained, high-legibility.

| Token | Hex | Use |
|-------|-----|-----|
| `--bg-void` | `#05070A` | letterbox / fade-to-black / deepest background |
| `--bg-panel` | `#0E141B` | HUD panels, caption bars (85% opacity over globe) |
| `--bg-panel-2` | `#161F29` | nested panel / table header |
| `--stroke-hair` | `#2A3744` | 1px hairlines, graticule, panel borders |
| `--ink-primary` | `#E6EDF3` | primary label text |
| `--ink-secondary`| `#9FB0BF` | secondary / provenance text |
| `--ink-mute` | `#64748B` | units, de-emphasized readouts |
| `--accent-real` | `#38D39F` | REAL tag (teal-green, colorblind-distinct from amber) |
| `--accent-sim` | `#F2B141` | SIMULATED tag (amber) |
| `--accent-illus` | `#8B9DC9` | ILLUSTRATIVE tag (muted slate-blue) |
| `--accent-focus` | `#4CA6FF` | active-layer highlight, selection, DFD edges |
| `--warn` | `#E5484D` | `[INFEASIBLE]` / DATA-PENDING placards (used sparingly) |

Rules: max **one** accent at full saturation per frame (the active layer); everything else sits in the
grey-blue neutrals. Atmosphere/haze uses `--bg-void`→transparent gradient at the horizon.

---

## 2. Typography
- **Labels / UI:** `Inter` (fallback `Segoe UI, system-ui, sans-serif`) — clean technical sans.
- **Data readouts / coords / params:** `JetBrains Mono` (fallback `Consolas, ui-monospace, monospace`).
- Scale (px): H1 title 28/600; shot narration 18/500; caption primary 15/600; provenance 13/400;
  mono readout 13/400; legend 12/500; furniture (scale bar / N arrow labels) 11/500.
- Hierarchy: ≤ 2 type sizes visible per HUD element; line-height 1.35; letter-spacing 0 (0.02em for all-caps tags).
- **Minimal text per frame:** caption ≤ 2 lines, narration ≤ 1 line. Generous padding (16px panel, 8px inline).

---

## 3. Colormaps per scalar field (from RESEARCH.md — perceptually uniform, colorblind-safe)
All sequential maps are perceptually uniform (even ΔE across the range) and CVD-safe; **no jet/rainbow**.

| Field | Colormap | Type | Justification |
|-------|----------|------|---------------|
| Elevation / relief | **oleron** (Crameri) over hillshade, or isoluminant relief | diverging-around-sea-level / isoluminant | shows terrain without hue-tricking slope; isoluminant lets shaded relief carry form |
| Temperature (plume) | **inferno** | sequential | perceptually uniform, dark→bright reads as hot; CVD-safe |
| Fire radiative power (FRP) | **magma / inferno** | sequential | high dynamic range, "glowing" hot tail; CVD-safe |
| Risk / probability (0–1) | **viridis** | sequential | the reference uniform map; unambiguous low→high; CVD-safe |
| Wind speed | **cividis** | sequential | optimized specifically for CVD; calm→strong |
| Smoke density | low-chroma grey→warm-white, encoded mainly by **opacity** | alpha-dominant | volume reads by accumulation, not hue; avoids competing with inferno plume |
| Uncertainty envelope | single hue (`--accent-focus`) at **translucent band**, opacity ∝ width | alpha | HOP/translucent-band convention (Hullman et al.); never a rainbow |
| Land cover (categorical) | muted ColorBrewer **qualitative** (desaturated), ≤ 8 classes | categorical | distinct but non-cartoon; CVD-checked set |

Legends: continuous fields get a labeled colorbar with units + min/max; categorical gets a class swatch key.
Every colorbar names the colormap (e.g. "viridis · risk 0–1").

---

## 4. Lighting, realism, atmosphere
- **Sun:** Cesium physically-based sun at the AOI's real local time for the event window (≈ mid-morning,
  low-mid elevation) → long soft shadows that reveal ridge form. State "illumination: 2021-04 AOI local AM".
- **Terrain shadows:** soft shadow map on; ambient occlusion subtle in valleys. No hard black shadows.
- **Atmosphere:** Cesium `skyAtmosphere` + ground atmosphere on; distance **haze** desaturates far terrain
  (focus-plus-context). Horizon glow uses `--bg-void` gradient.
- **Depth of field:** subtle, only on close dolly shots (S4, S8, S12); never so strong it hides data.
- **Volumes:** smoke = accumulated translucent billboards/particles (low chroma); plume temperature = stacked
  translucent slices (inferno). Physically motivated by the L6 field, never a decorative sprite.

---

## 5. Motion & easing
- Global easing: **ease-in-out cubic** for camera; **ease-out** for layer entries. No elastic/bounce/overshoot.
- Camera speed steady; orbits 5–15°/s; dollies constant-rate with gentle in/out. **No gratuitous spin** —
  every move reveals information (named in STORYBOARD per shot).
- Layer entries: wipe/fade/extrude-grow ≤ 1.2 s; exploded-stack separation is a slow accordion (ease-out, ~2 s).
- Time animation (L4/L5) is linear with the `Clock`; particle motion matches the real wind direction only when
  the ERA5 extract is loaded (else no motion — DATA-PENDING).

---

## 6. Clutter control & data-ink
- **Only the active layer at full emphasis**; all others fade to their STORYBOARD "After" opacity (20–40%).
- One full-saturation accent per frame (§1). HUD elements never overlap the active legend.
- **Data-ink discipline:** every visual element encodes real data or real structure. If it encodes nothing →
  remove it. No decorative gridlines, glows, or icons.
- 3-D label legibility: labels are **billboarded** (always face camera), depth-tested with a 1px dark halo
  (`--bg-void` 60%) for contrast over any terrain; collision-declutter hides lower-priority labels rather than
  overlapping; leader lines (`--stroke-hair`) connect a label to its anchor when offset.

---

## 7. REAL vs SIMULATED tag system (always on)
Persistent, unmissable, consistent position.

- **Top-left persistent chip** (never moves): a pill showing the *active layer's* tag:
  - `REAL` → background `--accent-real`, dark ink.
  - `SIMULATED` → background `--accent-sim`, dark ink.
  - `ILLUSTRATIVE` → background `--accent-illus`, dark ink.
- The chip text = tag + layer id, e.g. `REAL · L1 TERRAIN`, `SIMULATED · L6 PHYSICS`.
- **Caption bar (bottom-center)** provenance format (monospace for the source id):
  `‹TAG›: ‹source/model› · ‹product id / params› · ‹date/version› · ‹resolution› · ‹license-or-"not measured"›`
  e.g. `REAL: Copernicus DEM GLO-30 · 30 m · 2021 · COPERNICUS DEM licence`
  e.g. `SIMULATED: Heskestad plume + Iverson FS (TRINETRA numpy core) · params in panel · not an observation`
- SIMULATED/ILLUSTRATIVE layers additionally get a faint **amber hatch** border on their geometry so the
  distinction holds even with sound off and captions hidden.
- In the exploded stack, each plane's mini-caption carries its own tag chip (green/amber) — see S13.

---

## 8. On-screen furniture (persistent HUD)
- **Scale bar** (bottom-left): dynamic, updates with altitude; metric; `--ink-secondary`.
- **North arrow** (bottom-left, above scale bar): rotates with camera heading.
- **Coordinate + time readout** (top-right, monospace): `lon lat · alt · heading` and the `Clock` UTC time;
  for L4/L5 shows the data timestamp.
- **Per-layer legend** (right dock): colorbar/class key for the active scalar field, naming the colormap + units.
- **Vertical-exaggeration label** (near scale bar): `VE ×1.0` (or the real factor if exaggerated — **mandatory**).
- **Attributions block** (bottom strip, small; full-screen hold at finale) — exact strings from `LICENSES.md`:
  - `Esri, Vantor, Earthstar Geographics, and the GIS User Community` *(live basemap only — omit from exported video)*
  - `Copernicus Sentinel data 2021`
  - `Generated using Copernicus Climate Change Service information 2021`
  - `Produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2021 provided under COPERNICUS by the European Union and ESA; all rights reserved`
  - `© ESA WorldCover project / Contains modified Copernicus Sentinel data 2021`
  - `© OpenStreetMap contributors (ODbL)`
  - `Source: WorldPop (www.worldpop.org)` · `© European Union (GHSL/JRC)`
  - `Data courtesy of NASA FIRMS (LANCE/EOSDIS)` · `Imagery from NASA Worldview / GIBS (NASA EOSDIS)`
  - `Landsat imagery courtesy of the U.S. Geological Survey`
  - `Rendered with CesiumJS (Apache-2.0)`
  - *(FIRMS / GIBS / Landsat exact strings flagged UNCLEAR in LICENSES.md — verify before public release.)*

---

## 9. Accessibility
- **Colorblind-safe:** all scalar colormaps are CVD-safe by construction (viridis/cividis/inferno/magma/oleron);
  REAL/SIM distinction is **redundant-coded** (teal-green vs amber **and** text label **and** hatch border) so it
  survives deuteranopia/protanopia/tritanopia. Verify with a CVD simulator in QA.
- **Contrast:** all text ≥ WCAG AA (4.5:1) against its panel; tag pills use dark ink on bright fill (≥ 7:1).
- **Legibility in 3-D:** 1px dark halo on every map label; minimum on-screen label size 11px; declutter before overlap.
- **Motion safety:** no strobing/flicker; transitions ≥ 0.4 s; particle density capped; respect
  `prefers-reduced-motion` (static layer swaps instead of long camera moves).
- **Text alternative:** each layer's caption + provenance is also emitted to a side "layer log" panel (readable,
  selectable text) so the content is not image-only.
