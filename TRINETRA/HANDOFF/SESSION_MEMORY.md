# TRINETRA — SESSION MEMORY (read this first in any new chat)
Last updated: 2026-11-01 (after the A/B/C/F merge, meta-fusion, held-out RL and the cross-modal notebook X).
How to use: tell the AI "TRINETRA/HANDOFF/SESSION_MEMORY.md padh le". Everything needed to continue is below.

---

## 1. Project in one paragraph
TRINETRA is an advisory, offline-first, multi-hazard early-warning research prototype for India: fire/smoke (CCTV), landslide,
GLOF, flood, and fake media. Team SANKAT MOCHAK, Graphic Era Hill University, Dehradun. Hackathon SAARTHI26, now in Phase 2.
Repo: `github.com/saksham1253/TRINETRA-CONTENT-OG`. All new work is in the `TRINETRA/` folder. Training runs on Kaggle with the dataset
`happyparsi/trinetra-dataset` (61 GB, unpacked folders). Chat language with the user: Hinglish.

## 2. Non-negotiable rules (they drive every result)
- **Rule 16 (admission gate):** a learned model is "admitted" only if it beats climatology AND a simple baseline on the cost-weighted
  value score with a 95% block-bootstrap CI. Costs: C_FA = 5, C_miss = 100, so p* = 5/105 ≈ 0.048.
  Alert levels: < p* HOLD, < 4p* WATCH, otherwise ALARM.
- **Rule 19:** a learned RL policy is deployed only if it beats the rule with LCB > 0. The physics shield can only RAISE alerts.
- Never invent numbers. A missing result is written as "not measured". Every number is "OUR RESULT on the prototype pack", not comparable to papers.
- Balanced curated sets plus p* = 0.048 make the value score ≈ 0 for everyone, so AUC / recall@FPR5% are the headline metrics for fire.
- The deepfake expert has a trust cap of 0.4 (`adapters._POLICY`); zero-shot is capped at 0.5.

## 3. Kaggle accounts / notebooks (`TRINETRA/exports/kaggle_notebooks/`)
| acct | what | notebook | status |
|---|---|---|---|
| A | fire CNN (3 seeds × 15 ep) + colour baseline + FireSense video | `TRINETRA_A_final_fixed.ipynb` | DONE (`out_A_final.zip`, contains `fire/*.pt` weights) |
| B | CLIP ViT-L-14 zero-shot + few-shot CLIP probe | `TRINETRA_B_final.ipynb` | DONE |
| C | deepfake AuthenticityNet (CIFAKE) | `TRINETRA_C_final.ipynb` | DONE |
| D | EO heads + geo | `TRINETRA_D_*.ipynb` | not in this merge |
| P | physics (landslide hindcast, GLOF, RL env, Geo-PINN) | `TRINETRA_P_final.ipynb` | results live in repo `results/` |
| F | fusion + RL (synthetic pairing) | `TRINETRA_F_final_fixed.ipynb` | DONE (`out_F_final.zip`, `master_final.zip`) |
| **X** | **cross-modal fire fusion + per-row stress scores** | **`TRINETRA_X_crossmodal_final.ipynb`** | **PENDING: user must run it** |
Notebook pattern: the code package is embedded as base64 in cell 2. Cells include live logs, a heartbeat, timeouts and fail-fast checks.
To rebuild an embed, take the file list of the old embed plus new files from the repo (the repo is newer than the old embeds).

## 4. Final scorecard (`results/master_merged/MASTER_RESULTS.md`)
| hazard | expert | result | gate |
|---|---|---|---|
| Fire | fire_cnn (3 seeds) | AUC OOF 0.768 / held-out 0.972 | 0/3 |
| Fire | colorhist | OOF 0.681 | – |
| Fire | CLIP zero-shot | OOF 0.917 / held-out 1.000 | 0/1 |
| Fire | **CLIP probe** | **OOF 0.962 / held-out 0.998 (best single expert)** | 0/1 |
| Fire | META-FUSION stack (REAL pairing) | OOF 0.951 / held-out 0.999; stack − best = −0.008 | 0/3 |
| Fake media | deepfake | OOF 0.961 → held-out 0.450 (does NOT generalise) | 0/3 |
| Fire video | temporal validator | FA videos 0.893 → 0.853 (49 videos, small n) | – |
| Landslide | Caine physics, zero training | AUC 0.758 (184 events, 101 blocks) | physics |
| Landslide | geo meta-fusion FM-1 (REAL pairing) | 0.779 ≈ rain-only 0.781; with Geo-PINN 0.772 | 0/3 |
| Landslide | Geo-PINN | 0.716 | 0/1 |
| GLOF | area→volume exponent | b = 1.13 (0.71–1.50), n = 21 | fit |
| RL sim | CQL vs physics rule (C_miss 100/1000/5000) | rule ≈ oracle | deploy False ×3 |
| RL fused (synthetic, F) | OPE | +0.615 (LCB +0.24) | do not claim |
| RL fused (REAL pairing) | in-sample OPE | +1.08 (LCB +0.77) | do not claim, in-sample |
| **RL HELD-OUT** | true reward, block folds | vs rule +0.49 (LCB −0.08); vs tuned rule −0.02 (LCB −0.43) | **deploy 0/3 → keep the rule** |
Headline: **0 learned experts admitted.** Honest story: CLIP probe dominates fire. Fusion gives calibration (held-out ECE 0.026 vs
fire_cnn 0.24; value 0.55–0.63 vs clip 0.57), not extra AUC. The physics rule is kept by the gate.
Held-out RL averages (reward/image): CQL −2.10 · fixed rule −2.59 · tuned rule −2.09 · always-alarm −2.23 · oracle 0.

## 5. Key discoveries / bugs fixed this session
- fire_cnn, zeroshot, clip_probe and colorhist OOF all cover the **same 3410 images, same order and labels** (blocks = Smoke-Fire-Detection-YOLO
  sequences, 366 blocks; held-out = Forest Fire Dataset, 1023 images). That makes REAL-pairing stacking possible. colorhist has no held-out rows.
- `merge_all_results.py` bugs, all fixed:
  1. The fire CNN report is named `fire`, not `fire_cnn`, so it showed "not measured".
  2. Files like `out_B_final (1).zip` were skipped.
  3. F/X in-session re-runs of zeroshot/clip were double-counted as seeds. The owning account's copy now wins.
- The fire CNN expects 5-D input (B, T, C, H, W).
- On this sandbox, local tooling was installed with `python3 -m pip install --user --break-system-packages`:
  numpy, pandas, CPU torch, CPU torchvision (force-reinstalled), open_clip_torch, scikit-learn.

## 6. Code added / changed (all under `TRINETRA/`)
- `trinetra/kaggle/fire_meta_fusion.py`: REAL-pairing stack, block CV, held-out, Rule-16 gate, writes `fire_meta_cache.npz` for RL.
- `trinetra/kaggle/rl_heldout_eval.py`: CQL trained per block fold, scored with the true reward vs fixed and tuned rules.
- `trinetra/kaggle/crossmodal_fusion.py`: per-frame / per-confuser stack + temporal validator for every stream (fire_cnn, zeroshot,
  clip_probe, stack, mean, 2-of-3 vote). Fallback stack inputs are in `results/fire_meta/inputs/`.
- `trinetra/kaggle/eval_zeroshot.py`: new `--video FRAMES.npz`; writes `<tag>_rows.npz` with per-row stress and per-frame scores.
- `trinetra/kaggle/run_hackathon.sh`: zeroshot passes `--video`; new `crossmodal` stage (env `FIRE_MODELS`).
- `trinetra/kaggle/merge_all_results.py` + `collect_results.py`: fixes above; new rows for fire_meta_fusion, geo_fusion, offline_rl_real,
  offline_rl_heldout and crossmodal.
- `trinetra/src/trinetra/ws5_fusion_rl/adapters.py`: added the `clip_probe` source (0.75, cap 0.90, DATA).
- Results: `results/fire_meta/`, `results/geo_fusion/`, `results/offline_rl_real/`, `results/offline_rl_heldout/`, `results/master_merged/`
  (MASTER_RESULTS.md, RESULTS.md, NEXT_STEPS.md, DECK_RESULTS_SLIDES.md).
- Re-merge command (run from `TRINETRA/trinetra`): `python3 kaggle/merge_all_results.py --zips <all out_*.zip> --out /tmp/merged`,
  then copy MASTER_RESULTS.md, RESULTS.md, results.json and master.json into `results/master_merged/`.

## 7. Pending / next actions
1. **User runs notebook X.** Inputs: `happyparsi/trinetra-dataset` + the A final run output (or `out_A_final.zip` as a dataset).
   GPU T4, Internet ON. Estimated ~1–1.5 h. The user sends back `out_X_final.zip`.
2. When `out_X_final.zip` arrives: re-merge (section 6), read `crossmodal/crossmodal_s*_compare.md`, and fill slide 3 in
   `DECK_RESULTS_SLIDES.md` (video J per stream, confuser false-alarm rates).
3. **Account S (stress, after X): `exports/kaggle_notebooks/TRINETRA_S_stress_final.ipynb`.**
   - Runs `kaggle/stress_train.py` via the `run_hackathon.sh stress` stage.
   - It is a confuser-aware CLIP probe + stack, evaluated leave-one-confuser-set-out (weather / small flames / scenes).
   - Comparison is at equal recall: 0.90 on the OOF fire positives.
   - Gate: FA reduction with a block-bootstrap CI AND a DeepFire AUC drop ≤ 0.01.
   - Reads everything from `/kaggle/working`: A weights in `out_A_session/fire`, `npz/`. X's `out/` is moved to `out_X_session/`.
   - ~20–30 min on a T4. Dry-run tested on CPU (random weights; numbers meaningless).
   - The user sends back `out_S_final.zip`; the merge adds the "Fire CONFUSER-AWARE retrain" row.
4. The deck uses the honest story from section 4. Previous decks are `exports/TRINETRA_phase2_deck.pdf` and `exports/TRINETRA_deck_phase1.pdf`.

## 8. Other context files
`HANDOFF/NEXT_ACTION.md`, `HANDOFF/DECISIONS.md`, `TRINETRA_MetaFusion_Design.md` (GMF design: stacking + residual policy + shield),
`TRINETRA_Bug_Report.md`, `exports/kaggle_notebooks/RUN_ORDER_AND_TIMES.md`, `PROGRESS.md`, `FINAL_REPORT.md`.

---

## 9. Frontend: TRINETRA Command Console (started 2026-11-01, milestone 1)
Prompt file: TRINETRA_FRONTEND_3D_CONSOLE_PROMPT.md (user upload). The console is the app's default route `/`. The old dashboard moved to `#research`; `#deck` and `#live` are unchanged.
**Read first:** `FRONTEND/FE_STATE.md` (per-feature status + findings), `FRONTEND/NEXT_ACTION.md`, `FRONTEND/FE_ARCHITECTURE.md`, `FRONTEND/DEMO_RUNBOOK.md`.
- Stack: MapLibre GL 6 (globe + local Terrarium DEM via the `trn-dem://` protocol) + React 19 + Tailwind v4 + zustand. The engine runs in a Web Worker.
- Gotchas:
  - MapLibre 6 has no default export and needs `setWorkerUrl(...?url)` (already done in MapView).
  - The shell is `sh`: no brace expansion in `mkdir`.
  - The sandbox disk is ~11 GB. Torch and Playwright were removed after running out of space.
- Honest-by-construction rules:
  - Every slider comes from `params_registry.json` (52 params; 49 with repo file:line; 3 SURROGATE/PROPOSED).
  - The TS ports are golden-tested vs Python (`npm test`: 18 tests pass).
  - Simulator evidence = REAL OOF rows (`src/console/data/evidence_bank.json`).
  - LIVE mode = `tools/mock_gateway.py`, running the repo Python `fuse()`/`decide()`.
- Key findings:
  1. Repo defaults flood alerts because probabilities are calibrated at 55% prevalence. The PROPOSED prior-shift slider fixes it (Saerens 2002).
  2. The fire gate down-weights wind-driven fires (Byram N_c < 2 → c = 0.3).
  3. PHARAOH ignores `fusion.tau`.
  4. There is no fire-spread model in the repo; the perimeter is a SURROGATE (Anderson 1983).
- Not yet done:
  - Browser verification (no browser in the sandbox).
  - F8 extras.
  - A/B split map, viewshed, LoRa coverage heatmap.
  - A Figma file of the six screens.
  - Playwright screenshots.
- Notebook X was fixed on 2026-11-01. It finds the A weights in `/kaggle/working` (output dir) first, moves A's `out/` to `out_A_session/`, and reuses A's `npz/`.
