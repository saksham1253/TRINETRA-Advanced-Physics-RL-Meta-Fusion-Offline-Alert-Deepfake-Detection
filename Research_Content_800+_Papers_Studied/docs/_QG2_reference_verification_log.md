# QG2 — Reference-verification log (independent re-fetch sample)

This file records the independent, orchestrator-run reference-verification pass (quality gate QG2). The
honesty concern carried from the research program (`_CANON §7`) was that most arXiv identifiers were
**subagent-reported during a web_search outage and never independently re-fetched**. This pass re-fetches a
sample directly from arxiv.org to test that risk.

## Method
Direct `web_fetch` of `https://arxiv.org/abs/<ID>` for a stratified sample spanning (a) classic
pre-2024 method papers, (b) mid-era uncertainty/forensics papers, and (c) the load-bearing "2026" IDs the
documentation leans on most. A reference counts as VERIFIED when the page returns HTTP 200 AND the
title/abstract match the meaning attributed to it in the source artifacts.

## Sample result — 9/9 VERIFIED (re-fetched 2026-10-10)
| arXiv ID | Resolved title | Used for | Match? |
|----------|----------------|----------|--------|
| 1707.06347 | Proximal Policy Optimization Algorithms (Schulman et al., 2017) | RL baseline family (ch10) | ✔ exact |
| 2006.04779 | Conservative Q-Learning for Offline RL (Kumar et al., 2020) | Model-6 CQL (ch05/10) | ✔ exact |
| 2303.12783 | Conformal Prediction for Time Series w/ Modern Hopfield Nets — HopCPT (Auer et al., NeurIPS 2023) | conformal-under-shift (ch12) | ✔ exact |
| 2101.05397 | Should Ensemble Members Be Calibrated? (Wu & Gales, 2021) | "calibrated members ≠ calibrated ensemble" (ch12) | ✔ exact — abstract states the exact claim |
| 2608.12422 | Which Site, and When: Free-Satellite-Data Test of Himalayan GLOF/landslide/ice-floods (Kahn, Arjel, Adhikari, Sherpa, Pope; 12 Aug 2026) | spatial-CV leakage verdict + baseline results (ch06/09/12/13) | ✔ exact — abstract reproduces ROC 0.73/0.83/0.82, naïve ~0.9→0.76/0.71/0.54, 0.89 Nepal-only, 5 DL ≯ GBDT, 3-rule tree wins |
| 2604.24404 | From Spoofing to Trust: Emergency-Alert Spoofing Testbed + Cross-Cell Verification (Abou Hasna, Chendeb, El Falou; 27 Apr 2026; to appear IEEE VTC-Spring) | cell-broadcast spoofable → signed CAP + cross-cell corroboration (ch08/14) | ✔ exact |
| 2610.08227 | How Many Independent Samples Does a Satellite Image Contain? Generalization Bounds for Spatially Dependent Data (Young; 6 Oct 2026; IEEE TGRS 2026, DOI 10.1109/TGRS.2026.3739158) | N_eff = Θ(n²/r²) theorem justifying spatial-block CV (ch12) | ✔ exact |
| 2610.08810 | Transferability & operational reliability of a Prithvi crop-classification FM under phenological/geographic shift (Kolluru et al.; 20 Sep 2026) | confident-while-wrong: OA 0.65→0.40, 12–51% confidently mislabeled, MC-dropout entropy flags shift (ch14/22) | ✔ exact |
| 2608.22293 | The spatial anatomy of urban wildfire vulnerability … 2025 Palisades Fire (Farajpoor & Narimani; 23 Aug 2026) | 2nd-domain confirmation of spatial-CV verdict: random CV 0.92 → 1 km spatial-block 0.75; cited in FINAL_REPORT §3/§4 (ch06/13) | ✔ exact |

## 9/9 VERIFIED — and a self-correction logged
All nine sampled IDs resolve HTTP 200 with matching title/abstract. The 9th fetch (2608.22293) **reversed an
earlier orchestrator error**: in round 2 I had declared 2608.22293 "not in the source artifacts — do not
use it" and started a batch overwrite to 2608.12422. The re-fetch proves 2608.22293 is a real paper that
(a) is actually cited in `FINAL_REPORT.md §3/§4`, and (b) independently demonstrates the same spatial-block-CV
principle in the urban-wildfire domain (ROC-AUC 0.92 random → 0.75 block). Resolution: **cite BOTH** —
2608.12422 (Himalayan hazard domain, the claims-table numbers) and 2608.22293 (Palisades fire, second
domain) — with 2610.08227 as the theoretical N_eff bound. The batch overwrite is CANCELLED; chapters that
cite either ID are correct. `_CANON §6` updated accordingly.

## Finding — residual-risk downgrade
The "2026" identifiers are **real and resolve** in this environment's arXiv, and their abstracts match the
numbers the chapters attribute to them (checked verbatim for 2608.12422, 2610.08227, 2610.08810, 2604.24404).
This materially **reduces** the `_CANON §7` residual risk from "identifiers unverified" to "a stratified
8-sample re-fetch verified exactly; the full 631-ID ledger was not exhaustively re-fetched."

## Honest limits of this pass
- Sample is 8 of 631 IDs (~1.3%); chosen for load-bearing-ness, not at random, so it is a confidence check,
  not a census. A full re-fetch of all 631 remains future work (ch23).
- Classic non-arXiv references (Iverson 2000 WRR; Caine 1980 Geogr. Ann.; Heskestad 1983; Fukuzono 1985;
  Byram 1959) are textbook/journal citations with **no arXiv ID** and were NOT checked here — chapter 19
  carries them by author/year/venue and flags DOIs as to-be-resolved.
- Abstract-level numbers remain the *paper's* reported figures ([ABS]); re-fetch confirms the citation is
  real, not that TRINETRA reproduced any number (nothing trained/measured).

## QG2 verdict: PASS (sampled). Chapter 19 and `_CANON §7` updated to reflect this evidence.
