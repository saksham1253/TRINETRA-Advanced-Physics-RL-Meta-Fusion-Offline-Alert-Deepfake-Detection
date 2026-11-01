# Console architecture and stack decision
**Chosen: MapLibre GL JS 6 (globe + terrain + hillshade + color-relief) with local Terrarium DEM tiles, React 19 + Vite + Tailwind v4 + zustand, Web Worker engine.**
Compared: CesiumJS (best globe/3D tiles, but offline quantized-mesh terrain needs a tiler and Cesium ion for convenience; heavier bundle), MapLibre + deck.gl (deck.gl not needed: all layers are MapLibre-native circles, symbols, lines, fills, extrusions). MapLibre 6 gives globe projection, raster-dem terrain and `addProtocol`, which lets the console serve cached tiles and synthesise deeper zoom from cached parents with no server. Fallback: flat mercator without terrain (set exaggeration 1, relief layer off).

- `src/console/engine/*` pure TypeScript ports of the repo (golden-tested). `simulate.ts` builds sites, draws REAL OOF evidence rows, runs gate → fusion → decision per site per step, metrics and ROC.
- `workers/engine.worker.ts` runs full scenarios and sweeps; detail for one site is computed on the main thread (one step, < 1 ms).
- `map/dem.ts` tile chain: local → online (if allowed) → ancestor resample (nearest neighbour, exact encoding) → flat. Also used for LoRa line of sight and cursor elevation/slope/aspect.
- `lora/model.ts` repo planner (`engine/lora.ts`) + terrain LOS with 60 % first Fresnel clearance and 4/3 earth; LOS sampling runs on the main thread (tens of ms, cached).
- Live: SSE (`EventSource`) to the gateway; schema in `contracts/live_event.schema.json`; `tools/mock_gateway.py` decides with the repo Python `fuse()`/`decide()`.
- No glyph server offline, so the map draws no text; labels live in HTML panels.
Performance budget: engine run 20–330 ms for 1–152 sites (measured in vitest); target 60 fps national view (not yet measured in a browser).
