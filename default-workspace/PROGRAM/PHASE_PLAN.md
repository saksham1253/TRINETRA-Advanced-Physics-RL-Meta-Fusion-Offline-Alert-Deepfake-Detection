# PHASE_PLAN — refined P1–P20, recommended sequence, dependency graph, alternative
# (MASTER_PROMPT §0.1 rule 9, §0.11). Phase IDs are STABLE; the sequence is my proposal —
# you authorize each phase explicitly ("GO PHASE Pn"). Vague "continue" authorizes ONLY the
# single next phase in the recommended sequence.

## Carrying rules (every phase P1–P20)
- SOTA scan → PROGRAM/sota/<Pn>_sota_scan.md (template exists).
- Read ≥15 NEW novelty-checked papers (≥60% Tier 2+); heavy phases ~30–40.
  abstract-only does NOT count toward quota.
- Exit quota audit + ≥10% faithfulness audit; update HANDOFF/.
- Phase report → PROGRAM/reports/PHASE_XX_report.md; update PHASE_STATE/PROGRESS/ledgers;
  gate message (§0.2); STOP.

## Refined phase table (outcome + my refinement note)
| ID | Name | Main outcome | Hard deps | Refinement note for this project |
|----|------|--------------|-----------|----------------------------------|
| P1 | Baseline papers + system model | all local papers read; system model; key questions | P0 | Enumerate trinetra\papers\ (~110), merge to REFERENCES; lock the 14 key questions (0.8 draft) |
| P2 | Literature foundation I | core methods, CCTV/fire, eval, robustness, uncertainty | P1 | FIRST Tier-2+ promotions of the 235 ABS backlog (reading_queue top rows); build spatial-CV eval doctrine from 2608.12422 |
| P3 | Literature foundation II | physics, forensics, alerting/nets, RL, IoT, anomaly, safety, adjacent; reach 250–400 | P2 | Combined with P2 reaches the 250–400 verified target; close axis gaps A3/A4/A9/A13 |
| P4 | Synthesis | consensus/disagreement, failure-mode catalogue, gaps, design-change list | P3 | Promote analysis/05 + 06 to full catalogues; resolve CR-01..05 directionally |
| P5 | Dataset registry + compute budget | DATASETS.md, KAGGLE_BUDGET.md with verified limits | P3 (P4 helpful) | Verify COST/license/Kaggle for all P0 candidate sources; free-only; flag registration-gated in LEAD_TIME_ITEMS |
| P6 | WS7a IoT research/BOM/safety | verified BOM ≤₹2000, shopping list, safety | P3 | HARD-verify ₹ vs ≥2 live listings (unblock OQ-05); confirm IN865–867 band |
| P7 | WS1a physics on paper | model-set decision, full derivations, validation plan | P3, P5 | Re-derive E-01..E-06; resolve Bug #1-#4,#15; assign CLASS A/B/C |
| P8 | WS4 CCTV detection | model selection, failure taxonomy, protocol | P5, P7(soft) | River-Eye LSPIV + UQ (2507.20102); gap-filling (2312.06461) |
| P9 | WS8a anomaly scope + protocol | scope decision, SOTA scan, pre-registered protocol | P4,P5 (P8,P6 soft) | Deep SVDD upgrade (2510.09452); forecast-residual; SSL survey (2501.15196) |
| P10 | WS8b anomaly spec | ready-to-build spec per family, experiment plan | P9, P8 | |
| P11 | WS2 deepfake/misinfo design | detector pipeline, degradation protocol, decision policy | P5, P7(soft) | |
| P12 | WS3 offline alerting | IP verdict, tiered architecture, sim spec, threat model | P3 (P6 soft) | DTN (1308.2907, 2603.15945); CAP/SACHET; cry-wolf threshold (2104.11422) |
| P13 | WS7b IoT design + build manual | firmware/wiring spec, test/demo protocol (docs only) | P6, P12(soft), P10(soft) | |
| P14 | WS1b meta-fusion design | calibrated fusion across physics/vision/sensors/anomaly | P7, P8; P10,P13 soft | GMF: stacking + bounded residual + conformal + monotone shield; audit MoE collapse (CR-05) |
| P14Z | Zero-Shot & Open-Vocabulary Classification (ADDED, D-011; mandatory) | design for classifying hazards/scenes/conditions NOT explicitly trained on; VLM/CLIP open-vocab + RS-FM zero-shot + zero-shot anomaly + cross-region/hazard transfer; honest limits + GMF/conformal/shield gating | P14; P8, P9/P10 soft; CR-01 encoder trade (P7) soft | ≥10 NEW core reads (≥15 full-phase quota); zero-shot labels = LOW-TRUST advisory, never autonomous trigger (Rule 19); addresses rare-hazard few/no-label gap (e.g. GLOF) |
| P15 | WS5 RL design | environment, algorithm choice, training plan+budget | P7, P12, P14 soft | one-step baseline first (CR-03); safe shield realizability (2507.23603); trust-aware reward |
| P16 | WS6 robustness audit plan | failure-mode catalogue applied; prioritized fix/test plan | core designs exist | conformal/OOD/drift; apply FM-01..16 |
| P17 | Feature discovery + admission | FEATURES.md backlog with evidence + costs | core designs stable | admit F-01..F-10 under evidence rules |
| P18 | Feature specs + measurement plans | ready-to-build feature specs, pre-registered decision rules | P17 | |
| P19 | India deployment, standards, pilot, contributions | responsible-deployment pathway; genuine novelty | P1–P18 (esp P6,P12) | NDMA/SDMA; LoRa reg; privacy; Rule 19 pilot |
| P20 | Final quality gates + report | audits + FINAL_REPORT.md | everything | |

## RECOMMENDED SEQUENCE (my proposal)
Strict ascending **P1 → P2 → P3 → P4 → P5 → P6 → P7 → P8 → P9 → P10 → P11 → P12 → P13 →
P14 → P14Z → P15 → P16 → P17 → P18 → P19 → P20.**
(P14Z = Zero-Shot & Open-Vocabulary Classification, ADDED per D-011; runs after meta-fusion
P14 and before RL P15. ID chosen as P14Z — not a renumber — to preserve all existing P15–P20
cross-references under the non-destruction rule §0.3.)
Rationale: it respects every hard dependency, front-loads the literature foundation and the
spatial-CV eval doctrine (the single most important correctness guardrail, FM-01), and
defers hardware/design until the evidence base exists. It is also the simplest to supervise
one gate at a time.

## DEPENDENCY GRAPH (hard deps; "→" = must precede)
```
P0 → P1 → P2 → P3 ─┬→ P4 → (design-change list feeds P9,P14,P16)
                   ├→ P5 ─┬→ P7 ──┬→ P8 ──┐
                   │      │        │       ├→ P14 → P15 → P16 → P17 → P18 ┐
                   ├→ P6 ─┴→ P13   ├→ P11  │                              ├→ P19 → P20
                   └→ P12 ─────────┘       │                              │
P9 (needs P4,P5) → P10 ────────────────────┘ (P10 soft→P13,P14)           │
(P6 soft→P9; P8 soft→P9; P7 soft→P8,P11; P12 soft→P13,P15; P13 soft→P14)  ┘
```
Critical path: P0→P1→P2→P3→P5→P7→P8→P14→P14Z→P15→P16→P17→P18→P19→P20.

## ALTERNATIVE SEQUENCE (one, as required)
**Hardware-early / parallel-track order:** P1 → P2 → P3 → P5 → P6 → P4 → P7 → P12 → P13 →
P8 → P9 → P10 → P11 → P14 → P15 → P16 → P17 → P18 → P19 → P20.
- Idea: pull P5 (datasets) and P6/P13 (IoT BOM + build manual) and P12 (alerting) earlier,
  because the ₹2000 BOM has the longest real-world lead time (procurement, supplier
  verification) and LoRa/alerting are relatively independent of the ML physics stack.
- Trade-off: P4 synthesis lands later, so some design-change insights arrive after P6/P12
  start; acceptable because P6/P12 depend on P3 (not P4) and are hardware/network-bound.
- Choose this ONLY if you want procurement/lead-time items unblocked as early as possible
  (ties LEAD_TIME_ITEMS.md). Otherwise the recommended ascending sequence is preferred.

## Note
Exact per-phase quotas: P2 and P3 are the heavy literature phases (together 250–400 verified
NEW papers, ≥60% Tier 2+). All other phases carry the ≥15-paper quota + SOTA scan.

## ADDED PHASE — P14Z (zero-shot & open-vocabulary classification), D-011, mandatory
- Inserted after P14 (meta-fusion), before P15 (RL). ID is P14Z, NOT a renumber (preserves all
  P15–P20 references; §0.3 non-destruction).
- Scope: research + design only (no build). How far a deployed TRINETRA can classify hazards/
  scenes/conditions it was NEVER explicitly trained on. Four sub-threads: (a) VLM/CLIP open-vocab
  image classification; (b) remote-sensing foundation-model zero-shot (RemoteCLIP/GeoRSCLIP/
  SkyCLIP-type) for EO scene/condition tags; (c) zero-shot anomaly detection (WinCLIP/AnomalyCLIP-
  type) for novel hazard appearance; (d) zero-shot cross-region/cross-hazard transfer (ties the
  domain-shift + data-scarcity threads; relevant to rare GLOF with few/no labels).
- Quota: ≥10 NEW core zero-shot reads (user floor) within the standard §0.9 ≥15 full-phase quota;
  SOTA scan; exit audit.
- Life-safety guardrail (Rule 19): zero-shot/open-vocab outputs are LOW-TRUST by default — advisory
  tags that enter the GMF + conformal + monotone shield, NEVER an autonomous alarm trigger. Must
  carry calibration + hallucinated-label risk analysis + failure modes.
- Deps: hard P14; soft P8 (CCTV vision), P9/P10 (anomaly), CR-01 EO-FM encoder trade study.
