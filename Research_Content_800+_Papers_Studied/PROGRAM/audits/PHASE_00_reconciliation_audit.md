# PHASE P0 — Reading Reconciliation & Fresh Identity Audit (Task 0.5)

Date: 2026-10-05
This is a **new** program file (does not edit the pre-existing `analysis/11_reading_audit.md`,
which stays untouched under the non-destruction mandate).

## 1. Count reconciliation (the two snapshots)

| Snapshot | Ledger lines | Data rows | Dedup markers | Net-new | Depth | FT |
|---|---|---|---|---|---|---|
| RESUME_STATE 2026-10-04 | 98 | 97 | 1 (2401.13695) | 96 | all ABS | 0 |
| **Current (2026-10-05, verified)** | **251** | **250** | **1 (2401.13695)** | **249 rows** | all ABS | 0 |

**Resolution.** The 2026-10-04 snapshot was an *earlier mid-harvest checkpoint* (96
net-new). Harvest then continued (waves documented in `04_synthesis.md` up to the
"250-paper checkpoint, harvest CLOSED"). The current 250-row file is the later, complete
state. No contradiction — the 98-line file simply predates ~153 further rows. The
2401.13695 dedup marker is present and correct in both.

## 2. Internal duplicate resolution (grep-verified, exact lines)

250 data rows ≠ 250 unique papers. Grep on `^<id>,` confirms these duplicate groups:

| arXiv ID | Ledger lines | Copies | Redundant |
|---|---|---|---|
| 2509.18176 | 119, 128, 211 | 3 | 2 |
| 2106.08909 | 10, 92 | 2 | 1 |
| 2604.00801 | 13, 105 | 2 | 1 |
| 2205.13723 | 21, 122 | 2 | 1 |
| 2303.09750 | 28, 110 | 2 | 1 |
| 2603.15945 | 54, 223 | 2 | 1 |
| 1706.03458 | (2×) | 2 | 1 |
| 2303.12783 | 180, 249 | 2 | 1 |
| 2605.02153 | 182, 242 | 2 | 1 |
| 2411.04153 | 183, 243 | 2 | 1 |
| 2306.00001 | 56, 94 | 2 | 1 |
| 2105.13133 | 114, 221 | 2 | 1 |
| 2502.05709 | 181, 250 | 2 | 1 |
| **Total redundant rows** | | | **14** |

Plus **2401.13695** (L190) = baseline-dedup marker, `confidence=n/a`, NOT a new paper.

**Verified unique new-paper count:**
`250 data rows − 1 dedup marker − 14 redundant = **235 unique NEW papers**` — all ABS, 0 FT.

Note: several duplicate pairs differ in `authors` filling (one lists names, one `(authors)`)
and/or in `venue`/`takeaway` wording — i.e. the paper was re-encountered on a later search
axis and re-noted. The duplicate rows are **left in place** (non-destruction mandate); they
are *flagged* here and in `novelty_index.csv`, not deleted. On any future ledger
consolidation, keep the richer-authored row and drop the `(authors)` twin.

## 3. Fresh identity audit (this session) — 7th audit, 0% error

Live arXiv `/abs/` re-verification of a random spread (ID → ledger row cross-check of
title / authors / year / venue / core claim):

| arXiv ID | Ledger row | Title match | Authors match | Claim match | Verdict |
|---|---|---|---|---|---|
| 2509.18176 | L119/128/211 | ✓ | ✓ Yao;Azadnejad;Huang;Donohue;Dev | ✓ persistence-baseline warning | PASS |
| 2303.12783 | L180 | ✓ HopCPT | ✓ Auer;Gauch;Klotz;Hochreiter | ✓ autocorr violates exchangeability, NeurIPS 2023 | PASS |
| 2608.12422 | L82 | ✓ | ✓ Kahn;Arjel;Adhikari;Sherpa;Pope | ✓ 589 HMAGLOFDB, ROC 0.73/0.83/0.82, honest 0.76/0.71/0.54, 5 DL ≯ GB, 3-rule tree | PASS |
| 2507.23603 | L137 | ✓ | ✓ Rodriguez;Shaik;Corsi;Fox;Sanchez | ✓ unrealizable shields, cs.LO, 2025 | PASS |
| 2510.17014 | L133 | ✓ | ✓ Vanyan;Barseghyan;Tamazyan;Galstyan;Huroyan;Hovakimyan;Khachatrian | ✓ no gain at ViT-B | PASS |

**Result: 5/5 PASS, 0% identity/claim error.** Consistent with the 6 prior audits
(all 0% in `11_reading_audit.md`). The 2608.12422 abstract numbers match the ledger's
hard-number claims *exactly* (the single most load-bearing external citation), which is
the most important integrity check in the whole corpus.

## 4. Standing items carried forward
- `authors="(authors)"` placeholder rows remain (≈45 rows) → backfill on FT promotion.
- Three I–D constants (Caine/Dahal-Hasegawa/Garhwal, Bug #15) still page-unverified.
- The 235 ABS notes satisfy a *count* framing but NOT a per-phase Tier-2+ quota (quota
  honesty, §0.9) — flagged for the gate message as an open decision.
