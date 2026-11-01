# TRINETRA / HIMKAVACH — REPOSITORY BLUEPRINT & BUILD ROADMAP v1.0
> The concrete project skeleton the codebase phase will instantiate. Pairs with `SYSTEM_DESIGN_PROMPT.md`
> (rules), `HLD.md` (architecture), `LLD.md` (module internals), `COMPONENT_DESIGN.md` (contracts). Honesty/
> safety rules R16/R19/R20/R21 and constraints C1–C8 are enforced in config + CI, not just docs.

---
## 1. Repository tree
```
trinetra/
├─ README.md                      # maps every module → its DESIGN/ + research artifact
├─ pyproject.toml                 # py3.11; pinned deps (exact versions, C-dep safety)
├─ configs/                       # hydra/yaml, declarative; feature flags live here
│  ├─ default.yaml                # global: seeds, zones, cost ratios, p*, endpoint allow-list
│  ├─ fusion.yaml                 # model=FM-1(default)…FM-6 ; operator.pharaoh=off(default)
│  ├─ firephys.yaml               # nd1..nd7=off(default until [coeff-verify]); EF coeff table
│  ├─ geophys.yaml                # FS/Iverson/Fukuzono/Caine params; local-fit sources
│  ├─ rl.yaml                     # algo=one_step(default)|td3bc|cql|iql ; ope gate; reward
│  ├─ calib.yaml                  # alpha, WCPS, drift monitor
│  ├─ cctv.yaml                   # backbone, quant mode, F-12 window, FAR target
│  ├─ iot.yaml                    # lora.band=IN865_867(fixed); BOM pointer; duty cycle
│  └─ alert.yaml                  # CAP mapping, SACHET/siren endpoints (allow-listed)
├─ src/trinetra/
│  ├─ common/                     # types.py (Evidence/ExpertOutput/Decision), schemas/, tracing, security
│  ├─ ws1b_geophys/               # C-GEO: fs.py iverson.py fukuzono.py caine.py gate.py
│  ├─ ws1a_firephys/              # C-FIRE: established_ef.py novel_nd.py (flag-gated) gate.py
│  ├─ ws8_anomaly/                # C-ANO: forecast_residual.py deep_svdd.py iforest.py xgb.py ensemble.py
│  ├─ ws1b_eo/                    # C-ENC: encoder.py (frozen FM wrapper) datacube.py
│  ├─ ws4_cctv/                   # C-CCTV: detector.py temporal_validator.py ir_flicker.py
│  ├─ ws6_robust/                 # C-CAL: conformal.py drift_monitor.py missing_modality.py
│  ├─ ws5_fusion_rl/              # C-RL: policy.py shield.py ope.py  | C-FUS: gmf.py pharaoh.py fusion_models.py nf.py  | C-DEC: decision.py
│  ├─ ws3_alert/                  # C-ALERT: cap.py dtn.py siren.py  | C-OPS: operator_ui/ (advisory)
│  ├─ ws2_deepfake/               # C-DF: authenticity.py (low-trust)
│  └─ pipeline/                   # orchestration: geo_loop.py fire_loop.py offline_path.py
├─ firmware/
│  ├─ node_slope_sentinel/        # ESP32-C3: main.c sensors/ lora/ edge_screen/ power/
│  └─ node_river_eye/             # ESP32-CAM: capture/ lspiv/ lora/
├─ eval/                          # M0 harness: splits.py baselines.py value_score.py real_win.py report.py
│  └─ hindcasts/                  # kedarnath2013/ chamoli2021/ joshimath2022/ southlhonak2023/
├─ data/                          # DVC pointers ONLY (no raw data, no secrets); licenses/ manifest
├─ tests/                         # physics_golden/ decision/ fusion/ iot/ security/ repro/ eval/
├─ scripts/                       # provisioning, key-flash, bom_price_check, portal_license_check
├─ .github/workflows/ci.yaml      # runs gate checks (see §4)
└─ DESIGN/                        # this design set (source of truth for the build)
```

## 2. Module stubs — contract-first
Each `src/trinetra/<ws>/` module ships (a) a typed interface matching `COMPONENT_DESIGN.md`/`LLD.md`, (b) a
Class-A/B/C label in its docstring, (c) a feature flag read from `configs/`, (d) a NotImplemented stub +
golden/unit test skeleton, (e) a `MODEL_CARD.md` (purpose, inputs, Class, evidence paper IDs source-reported,
known pitfalls, decision rule). No module may `import` a legacy/buggy equation form (CI grep guard).

## 3. Flag defaults (safe-by-default; R20/R16)
`fusion.model=FM-1` · `fusion.operator.pharaoh=off` · `firephys.nd[1..7]=off` · `rl.algo=one_step` ·
`quant=none` → opt into heavier/novel paths only after their gate passes. Every Class-C flag, when ON, forces
`Decision.class_flags.used_classC=true` and a visible C-OPS banner.

## 4. CI gates (fail-closed) → map to G1–G7
| CI job | Enforces | Gate |
|--------|----------|------|
| `physics_golden` | saturated/steady-state/α-linearity; Iverson no-extra-cosβ; EF coeff present-or-flag-off | G1 |
| `eval_protocol` | report() refuses metric w/o spatial-CV baseline+CI; cost-loss present; F-17 real-win verdict | G2 |
| `decision` | exactly one decide() path; shield totality+monotonicity; conformal PICP≈nominal under replay-drift | G3 |
| `fusion` | meta-coeff stability; reliability down-weight on injected degradation; PHARAOH P1–P7 (if on) | G4 |
| `iot` | BOM≤₹2000 (from `scripts/bom_price_check`); tier feasibility budget; single-node≠RED; lora.band fixed | G5 |
| `security` | endpoint allow-list only; no-raw-video-egress serializer test; node sig/replay; timestamp anti-leak | G6 |
| `repro` | dataset license manifest present; datacube size cap; Kaggle GPU-h budget; seeds+folds logged | G7 |
Legacy-equation import guard + secret-scanner run on every PR.

## 5. Build roadmap (milestones; each ends at its gate)
- **M0 (foundation)** eval harness + baselines + spatial-CV + cost-loss + F-17 → **G2 skeleton live**. *Prereq for all.*
- **M1** geo physics gate + fire physics (A blocks; nd* off) → **G1**.
- **M2** EO encoder (frozen; CR-01 trade study) + anomaly ensemble → beats-baseline check (G2).
- **M3** CCTV detector + temporal validator + IR flicker → cross-camera decision rule (G2).
- **M4** calibration (WCPS) + drift monitor → **G3 (coverage)**.
- **M5** offline-RL (one-step; OPE gate) + hard shield → **G3 (decision+shield)**.
- **M6** meta-fusion (FM-1 default; PHARAOH/nd* behind validation) → **G4**.
- **M7** IoT nodes + firmware + BOM price re-check + fault/event discrimination → **G5**.
- **M8** alerting (CAP/SACHET + DTN + offline siren path) + operator UI → **G6 (offline path demo)**.
- **M9** deepfake advisory add-on; dataset license + Kaggle-fit audit → **G7**.
- **M10 (headline)** full-protocol hindcast (Kedarnath/Chamoli/Joshimath/South Lhonak) → honest report
  (incl. "does not beat baseline" where true). R16 lifts ONLY here, for passed items.

## 6. Definition of done (repo-level)
All CI gates green; offline alert path demonstrated cloud-down (C1); both node BOMs ≤₹2000 supplier-verified
(C2) on IN865–867 (C4); every reported number has spatial-CV baseline+CI; every Class-C block flag-gated with
Class-A/B fallback + logged novelty caveat (R20/R21); no autonomous public alert path exists anywhere (R19);
README traces each module to its DESIGN doc + research artifact.

## 7. Open items owned here (carry from research backlog)
`[coeff-verify]` EF-13..EF-20 + Caine/Iverson/Fukuzono; CR-01 SAR encoder; supplier price re-verification;
India portal/license verification (Bhuvan/MOSDAC/VEDAS/NRSC/IMD/CWC/GSI); PHARAOH P1–P7 numeric proof + FM
hyperparameters; LoRa IN865–867 regulatory confirmation; expert review of all Class-C blocks; build the
disaster-evac RL env + ≥100-seed eval. None blocks M0; each blocks its own module's gate.
