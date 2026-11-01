# Kaggle run order and estimated times

Every notebook has the TRINETRA code embedded (no code dataset needed). For each one:
Import Notebook → attach `happyparsi/trinetra-dataset` → Accelerator **GPU T4 x2** → **Internet ON** →
Save Version → **Save & Run All (commit)**. Committed runs keep going after you close the tab and save `/kaggle/working`
as the run's output, which is what fusion attaches.

## Account F (fusion): use `TRINETRA_F_phase2_fixed.ipynb` / `TRINETRA_F_final_fixed.ipynb`

- The data cell no longer walks the 61 GB team dataset. F converts no images, and the dataset is optional; it is only excluded from the search.
- The master cell no longer runs `glob("/kaggle/input/**/out_*.zip", recursive=True)`, which searched the whole dataset. It looks for `out_*.zip` only inside the attached A/B/C/D/P run outputs.
- The notebook adds a live log with heartbeat and timeouts (fuse 120 / geo-fusion 20 / merge 30 min). Offline RL prints `[rl] seed … epoch … loss … ETA`.
- Attach the finished runs with Add Input → Notebook Output. GPU is optional.

## Account A final: use `TRINETRA_A_final_fixed.ipynb`

Fixes the two failures seen in `TRINETRA_A_final`:
- FireSense conversion no longer aborts (`exit -6`, `malloc(): invalid size`). Every video is decoded in its own process, with an ffmpeg fallback, so only an unreadable file is skipped.
- Fire training now prints `[fold]` and per-epoch `[train] … loss … fold ETA` lines, so the run never looks frozen. Do not interrupt the cell.
- Also: the new `torch.amp` API (no deprecation warnings), a GPU fail-fast check, a live log with heartbeat, and stage timeouts (fire 330 / video 60 min).

## Account A phase2 stuck for hours? Use `TRINETRA_A_phase2_fast.ipynb`

Same stages (fire CNN + colour baseline + video, 1 seed × 5 epochs), but it stops immediately without a GPU and converts only A's datasets
(`BUILD_PARTS=fire`; a depth-limited folder finder locates only the 8 A datasets in the 61 GB unpacked team dataset instead of walking every file).
It also streams the log live with a `[heartbeat]` every ~5 silent minutes and `[time]` per stage, and adds stage timeouts
(find 7 / build 60 / fire 120 / video 45 min) that keep partial outputs. Planning estimate: ~25–50 min on T4 x2.
Any teammate can import it on their own account: attach `happyparsi/trinetra-dataset`, GPU T4 x2, Internet ON, Save & Run All.

## Which notebook, in which order

| Step | Notebook | Account | What it runs | Needs first |
|---|---|---|---|---|
| 1 (now) | `TRINETRA_A_phase2.ipynb` (running) | A | fire CNN + colour baseline, video | — |
| 1 | `TRINETRA_B_phase2.ipynb`, `TRINETRA_C_phase2.ipynb`, `TRINETRA_D_phase2.ipynb`, `TRINETRA_P_phase2.ipynb` | B, C, D, P | zero-shot · deepfake · EO + geo · physics | — (all in parallel) |
| 2 | `TRINETRA_F_phase2.ipynb` | F (any account, CPU ok) | fusion FM-1 / PHARAOH / median / max + RL logs + offline RL | A + B phase2 outputs (C preferred) |
| 3 | `TRINETRA_A_final.ipynb` … `TRINETRA_P_final.ipynb` | A, B, C, D, P | same stages, **3 seeds × 15 epochs**, bigger subsets | phase2 run of that account looked OK |
| 4 | `TRINETRA_F_final.ipynb` | F | fusion on the final outputs | A + B final outputs (C preferred) |

For fusion: right panel → **Add Input → Notebook Output** → pick the finished A, B and C runs. The import cell
copies their `out/fire`, `out/colorhist`, `out/zeroshot`, `out/deepfake` folders (or unzips `out_*.zip`).

`TRINETRA_ALL_phase2.ipynb` runs every stage in one session; use it only if you have just one account free
(about 3–5 h for phase2).

## Estimated wall-clock times (T4 x2)

These are **planning estimates**, not measured. Training uses 5-fold spatial CV, so
`final` ≈ 3 seeds × 3× epochs = **~9× the training time of phase2**. Data preparation and zero-shot do not scale.
**Best estimate: take your own phase2 stage times from the log and multiply the training part by 9.**

| Account | Data cell (discover + convert) | phase2 stages | final stages | final total |
|---|---|---|---|---|
| A fire + video | 10–20 min | fire 10–20 min, video 5–10 min | fire 1.5–3 h, video 15–30 min | **~2–3.5 h** |
| B zero-shot | 10–20 min | 10–20 min (incl. CLIP download) | same: 10–20 min (no seeds/epochs) | **~25–40 min** |
| C deepfake | 10–20 min (CIFAKE 20k at 32 px) | 10–15 min | 1–2 h | **~1.5–2.5 h** |
| D EO + geo | 5–15 min | eo-train 5–15 min, geo ~30 min | eo-train 45–90 min, geo ~30–45 min | **~1.5–2.5 h** |
| P physics | 2–5 min (CSV discovery only) | 30–45 min | 1–1.5 h (geo hindcast + Geo-PINN × 3 seeds) | **~1–1.5 h** |
| F fusion | 2–5 min | 10–20 min | 15–30 min (offline RL × 3 seeds) | **~20–35 min** |

Everything fits inside Kaggle's 12 h session limit. GPU quota: final A + C + D ≈ 5–8.5 GPU-h in total, well under the
~30 GPU-h/week quota. P, F and the data cells barely use the GPU.

Critical path if A–D start together: longest final run (A, ~3.5 h) → F final (~0.5 h) ≈ **4 h to final fused results**.

## After each run

Download `out_<ACCOUNT>_<PHASE>.zip` (or open `out/results/RESULTS.md`) and paste `RESULTS.md` to the AI. Only measured
numbers from these files go into `docs/NUMBERS_REGISTER.md` and the deck.

## One master result for everything

The last cell of `TRINETRA_F_phase2.ipynb` / `TRINETRA_F_final.ipynb` merges every attached run (attach the A, B, C, D and P runs as
Notebook Outputs) into `/kaggle/working/master/MASTER_RESULTS.md` and `master_<PHASE>.zip`. It keeps one phase per account,
adds the repo's landslide physics, GLOF, Geo-PINN and RL-environment results, and drops duplicate reports.
Locally (no numpy needed): `python trinetra/kaggle/merge_all_results.py --zips out_*.zip --out merged`.
Current master (B final + repo results): `results/master/MASTER_RESULTS.md`.

## Landslide META-FUSION (HLD: experts + physics consistency + FM-1 averaging)

Runs automatically at the end of the `geo` stage, so in `TRINETRA_P_*` (physics), `TRINETRA_D_*` and `TRINETRA_ALL_phase2`,
for every seed, right after Geo-PINN. It fuses rain model + Caine + dFS + repo physics gate + Geo-PINN on the SAME real rows
(REAL pairing, unlike the fire fusion), compares FM-1 / PHARAOH / mean / median / max / physics shield / stacked logistic, and gates
calibrated FM-1 against climatology and the rain-only model. Output: `out/geo/fusion/geo_fusion_s<seed>_{report.json,compare.md}`;
it also appears in `RESULTS.md` and in the master scorecard. Extra time: under 2 minutes (CPU).

## Account D: use `TRINETRA_D_v2.ipynb` (single notebook)

One notebook for D, `PHASE = "final"` by default (3 seeds x 15 epochs, about 1-1.5 h on T4 x2; set `"phase2"` for a quick check).
It runs ONLY the satellite (EO) models (Landslide4Sense + Sen1Floods11, Hephaestus only with annotations). The landslide physics,
Geo-PINN, RL and meta-fusion belong to account P (`TRINETRA_P_final.ipynb`, 3 seeds). If an older D run that also contains geo
results is attached next to a P run, the master merge drops D's geo copies so nothing is counted twice.
Order: D_v2 -> P_final (can run in parallel on two accounts; P is CPU-friendly) -> A_final -> F_final with all runs attached.

## LAST STEP: `TRINETRA_Z_FINAL.ipynb` (everything → one `TRINETRA_FINAL.zip`)

Run this once X and S (or whatever is finished) are done. **CPU only, no GPU, no Internet, team dataset not needed, ~5–10 min.**
Add Input → Notebook Output: A final, B final, C final, D v2, F final, P final, X final, S final → Save & Run All.
(Old downloaded zips work too: upload them to one private dataset and attach that. Names like `out_B_final (1).zip` are fine.)

What it does (`trinetra/kaggle/final_bundle.py`):
1. picks one phase per account (final > phase2) and lists missing accounts;
2. re-runs the **fire meta-fusion** on the attached runs, choosing the zeroshot / clip_probe copy whose OOF **and** held-out rows are
   the same images as A (B, else F/X in-session copies); otherwise the repo's `results/fire_meta` is used and the reason is logged;
3. **master merge** (`merge_all_results.py`) with that meta-fusion; geo meta-fusion comes from P;
4. **all graphs**: R0 (every ROC-AUC on one chart), R1–R6, R7–R9 cross-modal / stress from X + S, 10 physics graphs;
5. docs (Hinglish book, PHYSICS_FROM_ZERO derivations, final report), `FINAL_README.md`, `DETAILS_ALL_COMPARES.md`;
6. drops model checkpoints (`*.pt`) and writes `/kaggle/working/TRINETRA_FINAL.zip` (~10 MB with A B C F).

Locally (same result): `python TRINETRA/trinetra/kaggle/final_bundle.py --zips out_*.zip --out FINAL`.
Rebuild the notebook after code changes: `python TRINETRA/trinetra/kaggle/make_final_notebook.py`.
Checked locally with the A, B, C and F final zips: it reproduces the repo's fire meta-fusion (0.951 / 0.999, stack − best −0.008, admitted 0/3).
