# 09 — DATASET MAP + KAGGLE PARALLEL PLAN
## A. What the code/research points to, and the small replacement
| Research/code target | Full size (source) | Small replacement (09b) |
|---------------------|-------------------|--------------------------|
| `trinetra-fire` (CCTV fire/smoke clips) | n/a (built by team) | D-Fire 4k subset + FIRE Dataset; DeepFire held-out |
| FASDD, PYRONEAR-2025, GWFP, Wildfire Dataset (DATASETS_CATALOGUE B) | large (GWFP 56 GB on Kaggle) | rejected or lead only |
| `trinetra-telemetry` | n/a | Smoke-IoT sessions, env telemetry, NAB, UCI drift |
| `trinetra-media` deepfake (DFDC, FF++) | EULA, large | CIFAKE + StyleGAN faces |
| `trinetra-eo` / SSL4EO-S12 (~1.5 TB per KAGGLE_BUDGET) | TB-scale | **no replacement yet**; skip EO head in 36 h, use FIRMS CSV as context |
| `trinetra-geo` (landslide/Iverson) | n/a | **out of scope for fire hackathon**; numpy physics still runs on synthetic demo |
| `trinetra-rl-logs` | n/a | built by `make_rl_logs.py` from fused cache |

## B. Kaggle facts (UNVERIFIED; check the account quota panel at session start)
Repo assumption (`KAGGLE_BUDGET.md`): about 30 GPU-h/week per account, about 12 h per session, T4x2 or P100, about 20 GB persisted
`/kaggle/working`, internet toggle per notebook. **Terms:** each account must be a different real team member;
one person operating many accounts can break Kaggle's rules. Share data via private Datasets with collaborators.

## C. Parallel jobs (UPDATED 2026-10-31: IoT dropped, now FUTURE WORK)
All via `trinetra/kaggle/run_hackathon.sh <stage>`. Artifact schema = `*_oof.npz` (`deep/oof_utils.py`: prob, prob_cal, y, block,
test_prob, test_prob_cal, test_y, meta) + `*_report.json`.
| Acct | Stage | Attaches | Output | Est. GPU |
|------|-------|----------|--------|----------|
| A | `build` then `fire` | P02, P03, P06, P14, P15 | `npz/*.npz`, `out/fire/fire_s{0,1,2}_{oof.npz,report.json}`, `out/colorhist/*` | 4-6 h |
| B | `zeroshot` (+ confuser stress) | `trinetra-npz-v1` | `out/zeroshot/zeroshot_s0_*` | <1 h |
| C | `deepfake` | `trinetra-npz-v1` | `out/deepfake/deepfake_s{0,1,2}_*` | 1-2 h |
| D | `fuse` (CPU ok) | outputs of A, B, C | `out/fusion/fusion_compare.{json,md}`, `fusion_cache.npz`, `gmf_head_numpy.json`, `out/rl/*`, `out/results/RESULTS.md` | 0-0.5 h |
Run ID: `<module>-<yyyymmdd>-<hhmm>-<seed>`. Publish outputs as private Datasets `trinetra-<module>-v<k>`. Copy only
`*_report.json` and small CSVs into the repo `results/`.

Note: fusion pairs come from different datasets, so the fusion cache is a **SYNTHETIC PAIRING** (sample fire-positive
rows from each source for y=1, negatives for y=0). Label it as such everywhere. Sources now: fire_cnn + zeroshot
(fallback: colorhist), and deepfake as a reliability modifier with `--fake-frac 0.1` fake-fire-video attacks.
<!-- END -->
