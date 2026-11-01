# Demo runbook (10 minutes)
Opening page (no hash) = judge page: results, how it works, graphs, limits. "Live demo" opens the 3D console at `#console` (browser Back returns).
Start: `npm run demo:offline` (static build + preview on :4173). Live mode: `npm run gateway` in a second terminal.
1. Globe flies to India. Point at the SOI boundary, terrain relief, prototype badge, mode chip.
2. Physics lab: Decision → raise "Cost of a false alarm" or Fusion → lower "Deployment base rate" to 0.01. Watch the outcome strip: warning false alarms fall to 0, fires still detected. Point at "recomputed in N ms".
3. Click a beacon → Evidence: real model scores, leave-one-out influence, switch averaging technique, property checks, why-tier.
4. Double-click the beacon → dive. Perimeter (surrogate), flame band, wind arrows, camera cone. "Return to India".
5. Scenario 5 → play past 01:20 or press "Simulate internet and cellular outage" in LoRa: towers go dark, routes light up, pulses hop; kill R1-ridge and watch rerouting.
6. Scenario 8 landslide: FS, Iverson head, Caine, shield raises; lead time in the outcome strip.
7. Settings → Replay recorded session, or Connect live (gateway).
8. About: disclaimer, measured results (C3), data sources.
If the GPU is weak: Layers → terrain exaggeration 1, relief off. If tiles are missing: rerun `python3 tools/cache_terrain.py`. If the gateway is down: the console shows a banner and replays the last live events.
