# 10 — RUNBOOK (28 hours left as of 2026-10-31 ~08:30 UTC; IoT = FUTURE WORK)
Scope: **fire CNN + zero-shot + deepfake + fusion + RL + geohazard (landslide physics, GLOF, EO S1/S2/InSAR, landslide RL env)**. No IoT.
One command per stage: `bash TRINETRA/trinetra/kaggle/run_hackathon.sh <stage>` (see the script header).

## Kaggle notebook setup (every account, 10 min)
```bash
# Settings: Accelerator = GPU T4 x2, Internet = ON. Then in a cell:
!git clone https://github.com/saksham1253/TRINETRA-CONTENT-OG /kaggle/working/repo
# copy the new TRINETRA/ files into the repo first (team lead pushes them), then:
%cd /kaggle/working/repo/default-workspace
!pip -q install pillow
!bash trinetra/kaggle/run_hackathon.sh smoke        # must print SMOKE TEST PASSED (2-5 min)
```
(If the GitHub repo does not have the new files yet, upload the `TRINETRA/` folder as a private Kaggle Dataset and `cp -r` it.)

## Hour plan
| Hours | Acct | Stage | Done when |
|-------|------|-------|-----------|
| 0-1 | all | setup + `smoke` | SMOKE TEST PASSED |
| 1-3 | A | attach the FINAL list in docs/09b (P02, P03, P06, P14, P15, P33, P34, P35 + optional P01, P36, P37), then run `build`. Fix folder names via env vars (DEEPFIRE_POS=..). Publish `/kaggle/working/npz` as private Dataset `trinetra-npz-v1` and share it with B, C, D | every `check` prints [OK] |
| 3-11 | A | `fire` (SEEDS="0 1 2", EPOCHS=15), then `video` (FireSense) | 3 `fire_s*_report.json` + `video_s*_report.json` |
| 3-6 | B | attach `trinetra-npz-v1`, run `zeroshot` (internet ON) | `zeroshot_s0_report.json` |
| 3-8 | C | `deepfake` | 3 `deepfake_s*_report.json` |
| 6-12 | B | stress: rerun `eval_zeroshot.py --data npz/confusers.npz` + CNN on confusers (false-alarm rate) | numbers in RESULTS |
| 3-5 | B or D (CPU) | **`geo`**: real landslide physics + GLOF + RL env + Geo-PINN (internet ON) | `out/results/RESULTS.md` geo sections |
| 5-12 | GPU acct | **`eo`**: attach L4S + Sen1Floods11 (+ Hephaestus zips) | `eo_*` reports |
| 11-14 | D | gather `out/` from A, B, C (publish as Datasets), copy into one `OUT`, then run `fuse` | `out/results/RESULTS.md` |
| 14-20 | lead | paste RESULTS.md to the AI, which updates docs/14, the dashboard and the deck. Record demo screenshots | dashboard shows real results |
| 20-26 | all | rehearsal, judge Q&A (docs/15), README test by a teammate | 3-min demo < 3 min |
| 26-28 | all | **FREEZE**, final handoff snapshot | STATE.json updated |
Sleep: A and C sleep in hours 11-17 (their runs are in commit mode); B and D sleep in hours 17-23.
**Session died?** Rerun the same stage. Fold checkpoints are saved, but resume is NOT implemented, so lower EPOCHS if time is short.
**Decision points:** h3: `build` fails, so fix folder names (env vars), not code. h14: if nothing is `admitted`, present
AUC/recall/ECE + the honest "not admitted" gate (docs/14 B-13).
<!-- END -->
