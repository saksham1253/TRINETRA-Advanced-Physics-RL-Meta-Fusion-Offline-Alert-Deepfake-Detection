# NEXT ACTION (updated 2026-10-31 ~10:10 UTC)
00a. **Kaggle account connected (scientifictechz1253), but this sandbox cannot POST to Kaggle.** Import `exports/kaggle_notebooks/TRINETRA_ALL_phase2.ipynb` (code embedded, no code dataset needed), attach `happyparsi/trinetra-dataset`, GPU T4 x2 + Internet, Save Version → Save & Run All. Then give the AI the kernel slug; it runs `trinetra/kaggle/kaggle_monitor.sh <slug> status|output`.
00. **NOW (phase-2 eval in ~3.5 h):** team dataset = `happyparsi/trinetra-dataset` (public, 61.3 GB, unpacked folders).
    Upload `exports/trinetra_code.zip` as a Kaggle dataset, open `trinetra/kaggle/TRINETRA_kaggle_runner.ipynb` on each account,
    set `ACCOUNT` (A fire+video, B zero-shot, C deepfake, D EO+geo; then F fusion) and `PHASE="phase2"`, GPU T4 x2 + Internet, Run All.
    Send back each `out_<ACCOUNT>_phase2.zip` or its `RESULTS.md`. Final run: same notebooks with `PHASE="final"`.
0a. **When the team sends the Kaggle dataset link:** attach it and run the single command in `docs/KAGGLE_ZIP_TO_TRAINING.md`. Review `dataset_inventory.json` (including optional `IMERG_CSV` / `LULC_ROOT`) and require `ready_pack_report.json` to pass before using GPU time. Do not add IMERG/LULC to model inputs without a separate ablation.
0. **Deck is ready:** open the app at `#deck` (or `TRINETRA/exports/TRINETRA_7_slides.pdf`). Notes with N. When new results land, edit `src/deck/numbers.json` only.
0b. **AI:** geo/RL/Geo-PINN reruns are DONE and in results/. Next: vision Kaggle stages, multi-seed geo, CH10 (cyclone) beyond spec.
0c. **TPD-0.1:** 736 geo rows are profiled and indexed. Do not add placeholder EO/GLOF rows. After each source is attached, run its adapter, leakage check and loader smoke test, then extend `data_manifests/tpd_index.csv`.
1. **Team lead:** push `TRINETRA/` to GitHub (`default-workspace/`). Real geo results are already in `TRINETRA/results/` (OUR RESULTS).
2. **Kaggle stages** (`trinetra/kaggle/run_hackathon.sh <stage>`, docs/10):
   - A: `build`, `fire`, `video`. B: `zeroshot`. C: `deepfake`. D: `fuse`.
   - **Any account (CPU ok): `geo`** reruns the landslide physics, GLOF, RL env and Geo-PINN, about 30 min, internet ON.
   - **GPU account: `eo`**: use the small-pack defaults in `docs/SMALL_GEO_DATASET_PACK.md` (512 L4S, 400 Sen1Floods11, 512 Hephaestus at 64 px). Attach `tekbahadurkshetri/landslide4sense` and `smabrarrajin/sen1floods11-essentials`. For Hephaestus, download the Dropbox zips and set HEPH=<patch dir> HEPH_ANN=<annotations dir>.
3. **Register now:** NASA Earthdata (for IMERG 0.1 deg) and Copernicus Data Space (raw S1/S2).
4. **Paste to the AI:** every new `out/results/RESULTS.md`. The AI appends it to docs/14 and the dashboard.
5. **AI next:** profile and index converted EO outputs; IMERG swap-in for POWER only after Earthdata login; glacial-lake mask → lake-area adapter (P48).
Resume prompt for a new AI: "Read HANDOFF/NEXT_ACCOUNT_PICKUP.md and HANDOFF/STATE.json, then continue; do not redo finished work."
<!-- END -->


> **2026-11-01: latest state is in `HANDOFF/SESSION_MEMORY.md` (read that first).**
