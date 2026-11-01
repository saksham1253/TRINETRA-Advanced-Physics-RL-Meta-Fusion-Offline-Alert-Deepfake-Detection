# After the A/B/C/F merge (2026-11-01): status of the 4 follow-ups

Numbers come from `MASTER_RESULTS.md` (9 zips plus the repo's results/). Everything is measured on the prototype pack.

| # | Step | Status | Result |
|---|---|---|---|
| 1 | Held-out RL (block folds, true reward from labels) | **DONE locally** (`kaggle/rl_heldout_eval.py`, `results/offline_rl_heldout/`) | CQL vs fixed rule +0.49/row (LCB −0.08); vs train-tuned rule −0.02 (LCB −0.43). **Deploy 0/3: keep the rule.** The earlier +1.08 was in-sample OPE. |
| 2 | Cross-modal fusion (per-frame stack + temporal validator on FireSense) | **CODE READY, run on Kaggle** (`TRINETRA_X_crossmodal_final.ipynb`, ~1–1.5 h T4) | pending `out_X_final.zip` |
| 3 | Per-row stress scores (weather, small flames, scenes, held-out) | **CODE READY**, same notebook (`eval_zeroshot.py` writes `*_rows.npz`) | pending |
| 3b | Confuser-aware retrain on the stress sets (leave-one-confuser-set-out) | **CODE READY, run on Kaggle** (`TRINETRA_S_stress_final.ipynb`, after X, ~20–30 min T4) | pending `out_S_final.zip` |
| 4 | Honest deck slides | **DONE** (`DECK_RESULTS_SLIDES.md`) | update slide 3 once X is back |

Policy averages over 3 seeds (held-out, reward per image; C_FA 5, C_miss 100):
CQL −2.10 (miss 1.0%, false ALARM 46%) · fixed rule −2.59 (0.8%, 32%) · tuned rule −2.09 (0.4%, 60%) · always-alarm −2.23.
A balanced curated set with C_miss/C_FA = 20 rewards alarming a lot. This says something about the cost ratio, not about field behaviour.

## Kaggle run order (remaining)
1. `TRINETRA_X_crossmodal_final.ipynb`: inputs are `happyparsi/trinetra-dataset` + the A final run output (or `out_A_final.zip` as a dataset); GPU T4; Internet ON; Save & Run All.
2. `TRINETRA_S_stress_final.ipynb` in the same session (reads A weights + npz from /kaggle/working).
3. Send `out_X_final.zip` and `out_S_final.zip`. Locally: `python trinetra/kaggle/merge_all_results.py --zips out_*.zip` adds the cross-modal row.
