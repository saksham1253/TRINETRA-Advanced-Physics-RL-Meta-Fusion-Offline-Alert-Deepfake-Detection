# 00 — REPO INVENTORY (from github.com/saksham1253/TRINETRA-CONTENT-OG @ f8fee17, read 2026-10-31)

Repo root has one folder, `default-workspace/` (mirrored here as `TRINETRA/`). There are 918 files and 183 MB in total.
**File types:** md 444, png 258, py 124, jpg 29, json 18, csv 13, js 7, yaml 5, txt 4, pptx 3, docx 2.

## Top level (depth 1 to 2)
| Path | What it is |
|------|-----------|
| `trinetra/` | **the codebase** (python package `src/trinetra`, tests, kaggle kernels, configs, firmware spec) |
| `DESIGN/` | HLD, LLD, COMPONENT_DESIGN, REPO_BLUEPRINT, SYSTEM_DESIGN_PROMPT |
| `analysis/` | paper ledger (`02_paper_ledger.csv`), equations register, failure modes, claims table |
| `PROGRAM/` | phased research program: MASTER_PROMPT, phase papers P1-P7 csv, SOTA scans, audits, decisions |
| `ws1_physics/ ws1b_geohazard/ ws2_deepfake/ ws3_alerting/ ws4_cctv/ ws5_fusion/ ws5_rl/ ws6_robustness/ ws7_iot/ ws8_anomaly/` | per-workstream research (literature maps, derivations, designs) |
| `docs/` | earlier English + Hinglish handover set (`00_README_START_HERE` .. `25_changelog`) |
| `HANDOFF/` | earlier build handoff (BUILD_HANDOFF, OPEN_DECISIONS, RISKS_FOR_BUILD) + **new v2 files** |
| `DATASETS.md`, `DATASETS_CATALOGUE.md` | earlier dataset research (D1-D164, "no link tested") |
| `KAGGLE_BUDGET.md` | compute plan (Kaggle limits "verify at session start") |
| `viz/`, `ppt_work/` | 3D video/deck generation scripts (not part of the product runtime) |
| `TRINETRA_*.md` | bug report, robustification, corrected patches, meta-fusion design, workstreams |

## Entry points (verified by running, 2026-10-31, CPU + numpy)
| Command (from `trinetra/`) | Result |
|---------|--------|
| `python run_tests.py` | **128 tests OK** |
| `python scripts/ci_gates.py` | **6/6 gates PASS** (advisory, classC, security, leak, iot, legacy) |
| `python demo.py` | end-to-end advisory demo on SYNTHETIC data; prints CAP XML + hindcast (`admitted=False`) |
| `python kaggle/train_*.py` | 5 Kaggle trainers (need torch; **not run**) |

## Modules found (detail in `03_CODE_MAP.md`)
| Module asked for | Found? | Where |
|------------------|--------|-------|
| Detectors (fire/smoke) | interface + torch model | `ws4_cctv/__init__.py`, `deep/fire_cnn.py` |
| Zero-shot classification | **NOT FOUND IN CODE** (design only) | `ws4_cctv/zero_shot_design.md` |
| Anomaly detection | numpy ensemble + torch TCN-AE/SVDD | `ws8_anomaly/__init__.py`, `deep/anomaly_deep.py` |
| Physics features | fire (Heskestad, Byram, Strouhal...), geo (FS, Iverson, Fukuzono, Caine) | `ws1a_firephys/`, `ws1b_geophys/` |
| RL | offline CQL + rule baseline + OPE gate | `ws5_fusion_rl/rl.py`, `deep/offline_rl.py` |
| Meta-fusion | FM-1 / GMF / PHARAOH / hierarchical / BLUE | `ws5_fusion_rl/*.py`, `deep/fusion_head.py` |
| Deepfake | two-stream RGB+FFT, trust cap 0.4 | `deep/deepfake_net.py`, `ws2_deepfake/` |
| Misinformation (text) | **NOT FOUND IN CODE** | - |
| Alerting (offline) | CAP builder, DTN, siren, operator | `ws3_alert/` |
| Dashboard / UI | **NOT FOUND IN CODE** | - |
| Cyclone | **NOT FOUND** anywhere (as the team said) | - |

## Dataset references in code
Only `deep/datamodules.py` loads data. It uses `.npz` files under `KAGGLE_INPUT=/kaggle/input/<slug>`, with slugs
`trinetra-geo, -fire, -eo, -telemetry, -media, -rl-logs`. The keys are listed in `trinetra/kaggle/README.md` §2. No download
scripts, no hard-coded class lists beyond `[fire, smoke]` and `ACTIONS=(HOLD,WATCH,ALARM)`. `viz/pipeline/fetch_firms_era5.py`
is a visualization helper (not a training loader).

## Results / logs
No trained-model results exist. `CODE_INVENTORY.md` says "No model is trained yet, so no accuracy/skill claim is valid".
The only measured outputs are test/CI pass counts above and the synthetic demo hindcast.
<!-- END -->
