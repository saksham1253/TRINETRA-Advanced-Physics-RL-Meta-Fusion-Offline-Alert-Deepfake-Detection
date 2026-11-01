# _CANON.md — Single Source of Truth for the TRINETRA documentation set

> Every `docs/` chapter MUST agree with this file. If a chapter needs a fact that is here, copy it exactly
> (names, numbers, verdicts, labels). If a fact is NOT here and NOT in a cited source artifact, write
> "not measured" / "not verified" — never invent it. This file is authored by the orchestrator from the
> real project artifacts and is the arbiter for the consistency quality-gate.

Last updated: see `25_changelog_and_provenance.md`. Session date on artifacts: **2026-10-10**.

---

## 0. The two faces of this project (read first)

TRINETRA (alt. name **HIMKAVACH**) exists in two layers that the documentation must keep distinct:

1. **The research-only program** (artifacts in `default-workspace/*.md`, `analysis/`, `DESIGN/`,
   `ws*/` folders). Governed by `PROGRAM/MASTER_PROMPT.md`. Its own `FINAL_REPORT.md` states verbatim:
   *"Nothing was built, trained, or measured."* Every performance number in that program is
   **SOURCE-REPORTED** from other papers on their own data (Rule 16). 631 unique arXiv IDs; 128 paper notes.
2. **The reference code implementation** (`default-workspace/trinetra/`) built later in the engineering
   phase: a pure-**numpy core** (runs, **128 unit tests pass, 6 CI gates pass**) + a **PyTorch `deep/`
   layer** (6 models + fusion heads; verified by `py_compile` only — no GPU run here) + **Kaggle training
   scripts** (multi-GPU T4×2 ready; **not executed on a GPU** in this environment).

**No model has been trained and no dataset has been downloaded.** Therefore NO accuracy / skill / latency /
cost number in this documentation is a measured result of TRINETRA. Say so wherever a reader might assume
otherwise.

## 1. Honesty labels (use these exact tags on every non-trivial claim)
- `[CONFIRMED]` — measured by us (e.g. "128 numpy tests pass") OR verified in a cited source.
- `[LIKELY]` — plausible, needs our validation.
- `[HYPOTHESIS]` — our unvalidated idea.
- `[INFEASIBLE]` — ruled out.
- Source numbers must read "Paper X (arXiv NNNN.NNNNN), Table/Fig N reports …", kept visibly separate from
  "Our measurement: …". Abstract-only reads are `[ABS]` and may never be stated as established fact.

## 2. Code-status facts [CONFIRMED by running in this environment]
- `python run_tests.py` → **128 tests, OK** (numpy core; stdlib + numpy only).
- `python scripts/ci_gates.py` → **ALL 6 CI GATES PASSED**.
- `deep/` + `kaggle/` → **py_compile clean**; NOT run on a GPU (no torch/CUDA in the sandbox).
- Sandbox libraries available: numpy, pandas, lxml ONLY. No torch/scipy/sklearn/yaml.
- Source size (CODE_INVENTORY.md): src ≈ 3362 LOC, tests ≈ 917 LOC (128 tests), kaggle ≈ 316 LOC.
- Runtime used for tests: `C:\Users\Dell\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe`
  (set `$env:PYTHONIOENCODING="utf-8"` first).

## 3. Workstream numbering — THREE schemes exist; map them explicitly
The user's documentation frame uses six workstreams; the internal artifacts use more. Canonical mapping:

| Doc chapter frame (user) | Internal artifact workstreams | Code package(s) |
|--------------------------|-------------------------------|-----------------|
| WS1 physics + meta-fusion | WS1a fire-physics, WS1b geo-physics, WS5 fusion | `ws1a_firephys/`, `ws1b_geophys/`, `ws5_fusion_rl/` |
| WS2 deepfake / media | WS2 | `ws2_deepfake/`, `deep/deepfake_net.py` |
| WS3 offline alerting | WS3 | `ws3_alert/` |
| WS4 CCTV | WS4 | `ws4_cctv/`, `deep/fire_cnn.py` |
| WS5 RL | WS5 RL | `ws5_fusion_rl/rl.py`, `deep/offline_rl.py` |
| WS6 robustness / bugs | WS6 robustness, WS7 IoT, WS8 anomaly, eval | `ws6_robust/`, `ws7_iot/`, `ws8_anomaly/`, `eval/` |

Always state which scheme a sentence uses.

## 4. The six self-derived physics models (WS1) — canonical list
Source: `ws1_physics/model_set_decision.md`, `FINAL_REPORT.md §2`, and the implemented `ws1a_firephys/`,
`ws1b_geophys/`. The research program tracks **18 modelled relations** across classes; the implemented
**code** exposes this admitted subset (Class A established / B admitted-soft / C documentation-only):
- Geo (WS1b, Class A/B): infinite-slope **Factor of Safety** (saturated limit guard); **Iverson (2000)**
  transient pressure head with the bug-guard **D1 = D0/cos²β ONLY**; **Fukuzono** inverse-velocity failure
  time (α=2 ⇒ 1/v linear) with prediction interval; **Caine** intensity–duration rainfall threshold.
- Fire (WS1a, Class A): **Heskestad** flame height, **Byram convection number N_c** (dimensionless
  critical-Froude regime gate — NOT a fireline-intensity kW/m term; the code `established_ef.py` and
  `established_formula_inventory_P21.md` EF-13 both implement N_c), Strouhal flicker
  (1.5/√D), gray-body radiation. Class-C novel flicker/ND terms are **default OFF** with an A/B fallback.
- Meta-fusion (WS5): precision-weighted mean (FM-1 default), gated-mixture fusion (GMF) with **bounded
  residual**, **PHARAOH** power-mean operator (Class C, flag-gated OFF), hierarchical two-layer fusion,
  correlation-aware BLUE/GLS weighting. Decision: `level = max(conformal_level(risk, p*), shield_floor)`,
  **p\* = C_FA/(C_FA+C_miss) ≈ 0.0476** with C_FA=5, C_miss=100.

## 5. Honesty / safety rules enforced in CODE (cite by number)
- **R16** no performance claim before the eval admission gate (ReportGuard enforces).
- **R19** advisory, human-in-the-loop, fail-safe to "uncertain/offline"; NEVER autonomous public alert.
- **R20** Class A/B/C labels; Class-C novel terms default-OFF with A/B fallback.
- **R21** novelty = "not found in sources searched", never "does not exist".
- Constraints: **C1** offline-first alert path; **C2** ≤₹2000/node; **C3** ≤30 GPU-h/week Kaggle;
  **C6** endpoint allow-list; **C7** no raw-video egress; **C8** heavy models Tier-1/2 only.

## 6. Load-bearing VERDICTS the docs must carry (do not soften)
- **IP-address-based alerting = [INFEASIBLE]** for life-safety targeting. Consumer IP geolocation resolves to
  ISP/city granularity (often tens of km), is corrupted by CGNAT / VPN / DHCP, does not map to a premises,
  and cannot address a specific person at risk. NOT carried. Public-IP exposure is treated instead as a
  SECURITY concern (authenticated endpoints). Source: `FINAL_REPORT.md §4`.
- **Full fire-PINN as a deployed on-device solver = [INFEASIBLE]** now (stiffness, spectral bias,
  non-identifiability); physics enters as soft features with Class-A fallback.
- **Autonomous public alerting without certification/authority = [INFEASIBLE]**.
- Deepfake/zero-shot/social-media signals = **low-trust advisory only**, must be corroborated.
- Random cross-validation **overstates** skill → spatial-block CV is mandatory. This verdict is
  **triangulated across three real, independently re-fetched papers (QG2, 2026-10-10)**:
  (1) **arXiv 2608.12422** — Himalayan GLOF/landslide/ice-flood, the primary hazard domain
  (`analysis/07_claims_table.csv` C001–C003: naïve terrain ROC-AUC ~0.90 collapses to 0.76/0.71/0.54 under
  matched spatial-CV, 0.89 Nepal-only; "simple GB / 3-rule tree ≥ deep"); (2) **arXiv 2608.22293** — 2025
  Palisades urban-wildfire GeoAI (cited in `FINAL_REPORT.md §3/§4`): random CV ROC-AUC 0.92 drops to 0.75
  under 1 km spatial-block validation, logistic better-calibrated — a second-domain confirmation;
  (3) **arXiv 2610.08227** — effective-sample-size theorem N_eff = Θ(n²/r²) justifying block holdout
  (`TRINETRA_Workstreams.md` WS2). [History: an R2 note wrongly called 2608.22293 "not in the artifacts and
  do not use"; QG2 re-fetch (2026-10-10) confirmed 2608.22293 IS a real, on-point Palisades-fire paper AND
  is cited in FINAL_REPORT — so cite BOTH 2608.12422 (Himalaya) and 2608.22293 (wildfire); the two are
  complementary, not contradictory. The earlier batch "fix" to overwrite 2608.22293 is CANCELLED.]

## 7. Literature counts (from FINAL_REPORT.md §5) [as recorded by the program; identifiers mostly
subagent-reported, NOT independently re-fetched — a disclosed residual risk. **UPDATE R4 (QG2):** an
  orchestrator-run independent re-fetch of a stratified 8-ID sample (1707.06347, 2006.04779, 2303.12783,
  2101.05397, 2608.12422, 2604.24404, 2610.08227, 2610.08810) all resolved HTTP 200 with titles/abstracts
  matching the attributed meaning exactly (incl. the "2026" IDs — arXiv in this environment contains 2026
  papers). The 2608.12422 abstract reproduces the claims-table numbers verbatim. Residual risk is therefore
  downgraded to "sampled-verified; full ~775-ID census still future work". See `_QG2_reference_verification_log.md`.
  A 9th ID (2608.22293) was later re-fetched and also verified — see §6.]
- Unique arXiv IDs in ledger: **631 as snapshotted in FINAL_REPORT §5** (681 ID-bearing rows). **UPDATE R5:
  the LIVE ledger has grown past that snapshot — an independent orchestrator regex count of
  `analysis/02_paper_ledger.csv` finds ~**777 unique arXiv-style IDs** across 846 lines (chapter-19's
  per-row catalogue independently reports 775 unique / 841 data rows). Use 631 only as "the FINAL_REPORT
  snapshot figure"; use ~**775–777** as the actual catalogued count at doc-build. The growth is from
  P20–P23 additions after the report snapshot.
- New papers verified across P1–P20 ≈ **436**; 250-minimum **met**. **128 per-paper note files** →
  **127 unique IDs** (two files both cover 2608.12422); 72 of those are ledger rows, 55 are baseline-corpus
  papers not in the ledger (listed in chapter 19 §5). Row-level truth: `analysis/02_paper_ledger.csv` (445 KB).
- Read-depth labels: FT (full text), FT-PARTIAL, ABS, ABS-CANONICAL, FT-REF.

## 8. Compute / hardware canonical numbers (all PLANNING-level; verify at build)
- Kaggle: assumed ~**30 GPU-h/week**, keep ≥15% reserve → ~**25.5 usable**; session ~**12 h**;
  **P100 (16 GB)** or **2× T4 (2×16 GB)**; ~20 GB persistent + ~73 GB scratch disk; ~13–16 GB RAM.
  These are widely-published numbers, **NOT freshly fetched** — re-confirm on the live quota panel.
- IoT node BOM: all ₹ figures are **[EST]** (suppliers returned HTTP 403); Node A "Slope Sentinel" ≈
  ₹1,930 [EST], Node B "River Eye" ≈ ₹1,980 [EST]; LoRa band **IN865–867 MHz** (SX1262). ≤₹2000 gate NOT
  yet enforceable until live-verified.

## 9. Source-artifact map (where each chapter gets its ground truth)
| Chapter | Primary source artifacts |
|---------|--------------------------|
| 04 datasets | `DATASETS.md` (46 KB), `DATASETS_CATALOGUE.md` (12 KB) |
| 05 models | `ws1_physics/*`, `trinetra/MODEL_CARDS.md`, `trinetra/src/trinetra/deep/*`, `ws1a_firephys/`,`ws1b_geophys/` |
| 06 ws1 physics+fusion | `DESIGN/LLD.md`, `TRINETRA_MetaFusion_Design.md`, `analysis/08_equations_register.md`, code |
| 07 ws2 deepfake | `ws2_deepfake/`, `trinetra/src/trinetra/ws2_deepfake/`, `deep/deepfake_net.py` |
| 08 ws3 alerting | `ws3_alerting/`, `trinetra/src/trinetra/ws3_alert/`, `FINAL_REPORT.md §4` (IP verdict) |
| 09 ws4 cctv | `ws4_cctv/`, `trinetra/src/trinetra/ws4_cctv/`, `deep/fire_cnn.py`, `FEATURES.md` F-11/F-12/F-16 |
| 10 ws5 rl | `ws5_rl/`, `trinetra/src/trinetra/ws5_fusion_rl/rl.py`, `deep/offline_rl.py` |
| 11 kaggle | `KAGGLE_BUDGET.md`, `trinetra/kaggle/`, `trinetra/src/trinetra/deep/train.py`, `ddp.py` |
| 12 evaluation | `trinetra/src/trinetra/eval/*`, `TRINETRA_Workstreams.md` (G2), `analysis/07_*` |
| 13 bugs | `TRINETRA_Bug_Report.md`, `_Robustification.md`, `_Corrected_Patches.md`, `analysis/05_failure_mode_catalogue.md` |
| 14 security/privacy/ethics | `DESIGN/HLD.md §6`, `DEPLOYMENT/`, `FINAL_REPORT.md §12` |
| 15 deployment/ops | `DESIGN/HLD.md §4`, `DEPLOYMENT/`, `firmware/FIRMWARE_SPEC.md` |
| 16 code guide | `trinetra/CODE_INVENTORY.md`, `DESIGN/LLD.md`, `DESIGN/REPO_BLUEPRINT.md`, the code |
| 17 testing | `trinetra/tests/`, `trinetra/run_tests.py`, `trinetra/scripts/ci_gates.py` |
| 18 reproduce | `trinetra/README.md`, `trinetra/pyproject.toml`, `requirements-deep.txt`, `kaggle/README.md` |
| 19 references | `REFERENCES.md`, `analysis/02_paper_ledger.csv`, `analysis/03_paper_notes/` |
| 20–25 | `analysis/*`, `FINAL_REPORT.md`, `PROGRESS.md`, `DESIGN/*`, decision history |
