# DEPLOYMENT/research_contributions.md — candidate novel contributions (P19)

RESEARCH NOTES. Every item is "PROPOSED, NOT YET VALIDATED", tied to a verified GAP from the gap map / SOTA
scans. Rule 16/18/21: novelty = a SEARCH CLAIM ("not found in our search"), never an established result. Class
B/C physics items are hypotheses, never results. Validation = the experiment + the result that would count,
to be done in the BUILD phase.

## 1. System / methods contributions (proposed)
| ID | Proposed contribution | Tied-to gap | Validation experiment | What result would count |
|----|-----------------------|-------------|------------------------|--------------------------|
| C-01 | Offline-first, uncertainty-gated multi-sensor fusion that CALIBRATES THE FUSED OUTPUT with per-availability recalibration | P14: calibrated members ≠ calibrated ensemble (2101.05397); missing-input breaks calibration (2605.12517) | fused vs best-single on cross-site split, proper scores + PICP | fused beats best single by margin > seed variance, calibrated, FA ≤ best single at matched sensitivity |
| C-02 | Zero-shot admitted ONLY as a calibrated LOW-WEIGHT complement (D-011) with one-temperature-per-backbone transfer | P14Z: ZS miscalibrated/under-performs in fire domain | ablation: trained-only vs trained+calibrated-ZS on internal leakage-free set | ZS complement adds signal only where calibrated + low-weight; else dropped |
| C-03 | Cross-sensor corroboration + residual anomaly detection as the primary robustness defense for a fire system | P16: single-model hardening benchmark-local; redundancy generalizes | spoof-injection red-team on fusion | corroboration bounds a single bad/attacked source at low clean-accuracy cost |
| C-04 | India-fit, free-data, offline, shadow→advisory pilot protocol with uncertainty-based stopping rules | P19: confident-while-wrong under shift (2610.08810); random-CV overstates skill (2608.22293) | staged pilot with spatial-block validation | realized calibration/coverage holds across sites+seasons |
| C-05 | A leakage-controlled internal CCTV fire/smoke zero-shot evaluation set (candidate open benchmark) | P14Z: no clean permissive CCTV ZS fire benchmark | curate + document (datasheet) | independent re-evaluation reproduces reported difficulty |

## 2. Physics contributions (proposed) — Class labels mandatory (Rule 20)
HONEST: fire-physics derivations are from P7. Each must state CLASS (A standard/B adapted/C novel-hypothesis),
PARENT model + where the parent fails, VALIDATION status + roadmap against SPECIFIC published data, suitable
FIRE-SCIENCE venues (VERIFIED at build), and the EXPERTS who should review. Class C items listed as HYPOTHESES
ONLY. (Specific derivations tracked in ws1_physics; this file records the publication-contribution framing;
exact class/parent/validation per derivation to be filled from the P7 derivation records at build.)

## 3. Candidate open resources
Evaluation protocols (cross-camera/cross-site, spatial-block, inferential-reproducibility gate 2302.04054);
the robustness red-team suite (P16); the IoT build manual (P13); the leakage-controlled benchmark (C-05).

## 4. Credibility requirements (what makes it convincing to reviewers)
Strict pre-registered protocols; open code + data; honest NEGATIVES reported; IQM + CIs over many seeds
(2108.13264); contamination/leakage disclosure (2608.29463); verified-estimator calibration reporting
(1909.10155); claims calibrated in both directions, no reflexive hedging (2610.11355).

## 5. Honesty
All PROPOSED, unvalidated; novelty is a search claim; nothing is a result.
