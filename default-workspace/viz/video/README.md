# TRINETRA / HIMKAVACH — explainer videos

## ★ v4 — GLOF working-simulation + detailed data stack (1080p) — recommended
**Deliverables in `output/`:**
| file | res | size | notes |
|------|-----|------|-------|
| `trinetra_glof_3d.avi` | 1920×1080 | ~2.0 GB | full quality |
| `trinetra_glof_3d_720.avi` | 1280×720 | ~0.9 GB | lighter / easier to share |

~**9 min 05 s**, 18 fps, Motion-JPEG AVI. **Play with VLC** (guaranteed) or Windows Media Player.

What changed vs the earlier ultra cut (addresses the feedback directly):
- **Dataset layer, rebuilt for clarity (L8).** A full-screen, readable registry *table* — every one of the
  26 datasets with ID, name, workstream, licence, size/access and verification tag ([V]/[V*]/[D]), plus the
  exact counts (13 selected / 13 candidate). Parsed verbatim from `DATASETS.md`; nothing downloaded or trained.
- **Layers no longer run off-screen.** Compact stack spacing + a camera that always frames the whole stack,
  and a new **"13 layers · one stack"** overview scene with a full legend.
- **The simulation is now a legible GLOF story.** A glacial lake bursts, a flood descends the valley toward a
  settlement, a *people-at-risk* signal fires, and — on a **persistent high-level DFD panel on the right** —
  you watch data flow node-by-node (packets travel the edges, each node lights up and shows its output) all
  the way to a human-gated decision. A plain-language step card explains every stage.
- Honesty preserved: terrain/imagery **REAL**; slope physics (Caine I/I_thr=1.0857, FS crosses 1 at β37→38°,
  Fukuzono α=2) and decision (conformal p*=0.0476, shield **GLOF⇒Red**, mandatory human gate) **SIMULATED on
  the real code**; GLOF trigger, flood geometry, reach rings, evac route and the ≈1,850 people-count are
  **ILLUSTRATIVE** and labelled as such.

Build: `python render_3d.py full` then `python make_avi.py 70 frames3d 1920x1080 trinetra_glof_3d.avi`
(then `..._720` via `downscale_frames.py`). Rendering uses geom_w=150, no supersample, 18 fps to stay fast on
a thermally-throttling CPU; `render_3d.py full resume` continues an interrupted render.

## earlier cuts (superseded, files removed to save disk)
Earlier renders (v1 flat 2D data-stack; v2/v3 cinematic 3D cascade with baked sun-shadows + volumetric fire
plume) have been removed from `output/` to free space. They are fully regenerable from the scripts.

| `trinetra_cascade_3d.avi` | 1600×900 | ~1.2 GB | full quality |
| `trinetra_cascade_3d_720.avi` | 1280×720 | ~0.5 GB | lighter / easier to share |

~**6 min 26 s**, 20 fps, Motion-JPEG AVI. **Play with VLC** (guaranteed) or Windows Media Player.

Real **3D terrain** (a real DEM heightfield software-rendered with an orbiting camera, draped with real
satellite imagery), the 13 data layers built up as **floating 3D sheets with real parallax/depth**, and then
an end-to-end **DISASTER CASCADE**: a wildfire ignites, a 3D plume rises, rain hits the burn slope, and you
watch the model fire step by step — sensing → WS1 physics (Byram Nc=0.4464, Heskestad flame 7.61 m, Caine
I/I_thr=1.0857, FS crossing 1 between β=37°/38°) → WS8/WS2 (media capped 0.40) → WS5 meta-fusion → conformal
decision `level = max(conformal(risk, p*=0.0476), shield_floor)` → **mandatory human approval** → WS3 tiered
alert + routing. Every step tagged REAL / SIMULATED / ILLUSTRATIVE; numbers from the real code
(`CASCADE_SPEC.md` has the sourced trigger chain). Build: `python terrain_prep.py` then
`python render_3d.py full` then `python make_avi.py 70 frames3d 1600x900 trinetra_cascade_3d.avi`.

## v1 — flat 2D data-stack explainer
| file | res | size | notes |
|------|-----|------|-------|
| `trinetra_datastack.avi` | 1920×1080 | ~930 MB | full quality |
| `trinetra_datastack_720.avi` | 1280×720 | ~412 MB | lighter / easier to share |

Both are ~**5 min 43 s**, 20 fps, Motion-JPEG AVI. **Play with VLC** (guaranteed) or the Windows Media Player
app. Same content, two sizes.

> **Why AVI and not MP4?** This build environment **blocks launching the `ffmpeg` binary** (the OS refuses to
> run the unsigned executable — verified from PowerShell, cmd, a temp copy, a normal user folder, and even under
> full file access), and the in-process pure-WASM H.264 encoder slows down quadratically over 6,860 frames. So
> the frames are encoded into a standards MJPEG AVI entirely in Python. On any normal machine you get a small
> MP4 in seconds with one command (ffmpeg runs fine there):
> ```powershell
> ffmpeg -y -framerate 20 -i frames/f_%06d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart output/trinetra_datastack.mp4
> ```

## What's in it (timeline, ~5:43)
1. **Intro** — title + the honesty key (REAL / SIMULATED / ILLUSTRATIVE).
2. **Study area** — real satellite view of the Uttarakhand 2021 pre-monsoon fire season (bbox 78.5,29.5,80.2,30.8).
3. **The stack** — then L0 → L12 added one slab at a time, each with a detail panel:
   - L0 Earth/AOI (NASA GIBS true colour, open) · L1 Terrain/DEM (Copernicus GLO-30; relief © Esri)
   - L2 Land cover (ESA WorldCover 10 m) · L3 Built/exposure (OSM + WorldPop)
   - L4 Wind (ERA5-Land) and L5 Fire (NASA FIRMS) → shown as **DATA-PENDING** (need a free key; never faked)
   - **L6 Physics** — Heskestad plume, Strouhal puffing, Byram number, Factor-of-Safety, Caine I–D, with the
     numbers computed by the real `trinetra` numpy core, plus plume-temperature and FS-vs-slope plots.
   - L7 CCTV FOV (illustrative) · **L8 Dataset registry** (26 datasets, 13 selected / 13 candidate, verbatim)
   - L9 Deepfake verification (illustrative, reliability capped 0.40) · L10 Tiered alerting (scenario geometry)
   - L11 Advisory routing (rule baseline over OSM roads) · **L12 Data-flow diagram** + the decision rule.
4. **Outro** — the full stack + the honesty summary.

## Honesty (same rules as the rest of `viz/`)
- Green = REAL (with source + license on screen). Amber = SIMULATED (our physics code) or ILLUSTRATIVE (flow/geometry).
- Physics numbers come from `../render/public/data/l6_physics.json`; dataset counts from `l8_datasets.json`
  (parsed verbatim from `DATASETS.md`). Nothing unmeasured is shown as measured.
- L4/L5 render nothing until a real FIRMS/ERA5 extract exists.
- Imagery credit: NASA GIBS/VIIRS (open) and © Esri, Maxar, Earthstar Geographics.

## How it was built (reproduce)
```powershell
cd viz/video
# real AOI imagery already in assets/ (GIBS true-color + Esri export/hillshade, fetched via Node fetch)
python render_video.py full                                          # -> frames/ (6860 JPEGs) + timeline.json
python make_avi.py 72 frames 1920x1080 trinetra_datastack.avi        # 1080p AVI
python make_avi.py 60 frames720 1280x720 trinetra_datastack_720.avi  # 720p AVI (needs frames720/)
# ...or on a machine with ffmpeg -> MP4 (one line, see box above)
# ...or in-process MP4 (slow, pure WASM):  node encode_node.cjs
```
Change pace/length via the `durs`/timeline in `render_video.py`; change any wording in its `LAYERS` table.
