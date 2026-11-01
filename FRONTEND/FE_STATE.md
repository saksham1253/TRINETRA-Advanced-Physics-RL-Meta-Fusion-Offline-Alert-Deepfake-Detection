# TRINETRA Command Console: feature state (update after every milestone)
Last update: 2026-11-01, milestone 1. Prompt: TRINETRA_FRONTEND_3D_CONSOLE_PROMPT.md. Route: `/` (console); old dashboard at `#research`; deck `#deck`.

| Feature | Status | Main files | Open issues |
|---|---|---|---|
| Parameter registry (52 params, 49 with repo file:line) | DONE | tools/extract_params.py → src/console/data/params_registry.json | re-run after repo changes; unresolved patterns fail the script |
| Golden tests (TS ports vs Python) | DONE, 8/8 pass | tools/export_golden.py, src/console/engine/__tests__/golden.test.ts | add golden cases for any new port |
| Physics/fusion/decision/LoRa ports | DONE | src/console/engine/{firephys,geophys,fusion,decision,lora}.ts | Fukuzono fit not ported (gate input only) |
| F1 National 3D map (globe intro, SOI boundary, states, rivers, offline terrain) | BUILT, not browser-verified | src/console/map/{MapView,style,dem,terrainProtocol,icons}.ts(x) | verify in browser; districts and imagery not in the pack |
| F2 Scenario engine (8 scenarios, seeded, real OOF evidence) | DONE, determinism tested | src/console/engine/simulate.ts, src/console/data/scenarios/*.json | IoT, positions and visibility ramp are SIMULATED |
| F3 Hyperparameter lab (sliders, presets, A/B baseline, undo/redo, JSON, sensitivity sweep, formula inspector) | BUILT | src/console/panels/ParamsPanel.tsx, Modals.tsx | A/B split-screen map is not built (baseline values are shown per slider) |
| F4 Alert dive (fly-in, surrogate perimeter, Heskestad flame band, wind field, camera cone, breadcrumb) | BUILT (basic) | MapView.tsx, derived.ts | no viewshed, no buildings, no local scene time control |
| F5 Evidence and explain (chain, leave-one-out influence, 7 techniques live, property checks, why-tier, approval gate, CAP mapping, audit) | BUILT | src/console/panels/EvidencePanel.tsx | Hindi text for why-tier not written (EN + Hinglish only) |
| F6 LoRa mesh (repo planner + terrain LOS/Fresnel, outage showpiece, pulses, node kill, packet loss, SF trade-off, reality panel) | BUILT | src/console/lora/{model,useMesh}.ts, panels/LoraPanel.tsx | coverage heatmap and relay optimiser not built |
| F7 Live/Replay (schema, validator, contract test, SSE client, mock gateway running repo Python, drop → replay banner) | BUILT, gateway tested with curl | src/console/contracts/*, live/useLive.ts, tools/mock_gateway.py, public/replay/session_demo.jsonl | WebSocket not used (SSE); training monitor not built |
| F8 Extras | NOT STARTED | – | cyclone (spec only in repo), time machine, compare systems, mentor tour, PDF export |
| Design tokens + components spec | DONE (code-side) | design/tokens.json, design/COMPONENTS.md, src/index.css, src/console/console.css | Figma file not created in this session |
| QA / runbook | PARTIAL | FRONTEND/QA.md, FRONTEND/DEMO_RUNBOOK.md | Playwright visual suite not added (disk limit in sandbox) |

## Findings worth telling the team (from running the real code)
1. Repo defaults (C_FA 5, C_miss 100, p* = 0.048) on calibrated OOF probabilities make almost every camera alert (s1: 1195 watch false-alarm episodes in 6 h). Cause: probabilities were calibrated on a set with 55 % fire. The PROPOSED prior-shift slider (base rate 1 %) gives 0 warning false alarms with all fires detected in 4–6 min. Not in the repo yet.
2. Fire gate (ws1a_firephys/gate.py) lowers consistency when Byram N_c < 2; a real 9 m/s wind-driven fire gets c = 0.3. N_c < 1 is a normal wind-driven fire, not a non-fire regime: physics team should review.
3. PHARAOH (pharaoh.py) computes its weights with the default τ = 0.5, ignoring fusion.tau. Ported faithfully; flagged.
4. No fire-spread model exists in the repo; the perimeter is a labelled SURROGATE (Anderson 1983 L/B ellipse).
