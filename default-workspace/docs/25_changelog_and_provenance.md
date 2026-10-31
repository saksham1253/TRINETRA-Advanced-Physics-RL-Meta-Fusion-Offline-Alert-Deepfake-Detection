# 25 — Changelog and Provenance

**Audience:** the original author six months later, or an auditor tracing *what changed, when, why, and by
which agent*. This chapter records the provenance of both the research program and the reference code, and
of this documentation set itself. Honesty posture per `_CANON.md`: nothing was trained or measured.

---

## 25.1 How to read this chapter
Three timelines are kept separate: (A) the **research program** (phases P0–P23, literature-driven, no code
shipped), (B) the **reference code implementation** (`trinetra/`, built after the research froze), and
(C) **this documentation set** (`docs/`). Each entry carries a date where the artifacts record one, the
driving reason, and the resulting artifact. Dates are those stamped in the artifacts (session date
2026-10-10) — they are provenance labels, not independently time-verified.

## 25.2 Timeline A — the research program (P0–P23)
Source: `PROGRESS.md`, `analysis/PROGRESS.md`, `analysis/RESUME_STATE_*.md`, `FINAL_REPORT.md`. The program
ran under `PROGRAM/MASTER_PROMPT.md` (research-only, phased, permission-gated, SOTA-driven). Highlights:

| Phase | What it produced | Key artifact(s) |
|-------|------------------|-----------------|
| P0 | Workspace/root gate, assumptions, discovery backlog (235 ABS papers) | `ASSUMPTIONS.md`, `REFERENCES.md`, ledger |
| P1–P3 | Literature search + full-text/partial promotions; paper ledger grows to 631 unique arXiv IDs | `analysis/02_paper_ledger.csv`, 128 notes |
| P4–P5 | Re-examination of 33 prior bug findings; Kaggle compute plan populated | `KAGGLE_BUDGET.md`, bug re-exam |
| P6 | ₹2000 IoT node BOM skeleton (prices [EST], suppliers 403) | `HARDWARE_BUDGET.md` |
| P7 / P7G | Fire-physics and geo-physics model-set decision (Class A/B/C) | `ws1_physics/model_set_decision.md` |
| P8 (+P14Z) | CCTV fire/smoke detector design; zero-shot as low-weight complement | `ws4_cctv/*` |
| P9/P10 | Anomaly stack design (forecast-residual + Deep-SVDD) under strict protocol | `ws8_anomaly/*` |
| P11 | Deepfake/misinfo defensive-only design (all ABS) | `ws2_deepfake/*` |
| P12 | Offline alerting; IP-address idea rejected as INFEASIBLE | `ws3_alerting/*`, `FINAL_REPORT §4` |
| P13 | IoT build manual / firmware behaviour | `firmware/FIRMWARE_SPEC.md` |
| P14 | Meta-fusion design (GMF + PHARAOH + FM-1..6) | `TRINETRA_MetaFusion_Design.md` |
| P15 | Offline-RL advisory alarm policy + honest OPE valuation | RL design notes |
| P16 | Robustification strategy; cross-sensor corroboration | `TRINETRA_Bug_Robustification.md` |
| P17/P18 | Feature admission (F-01..F-26) + Wave-1 build specs | `FEATURES.md`, `features/*` |
| P19 | India deployment / stakeholders (all [UNVERIFIED]) | `DEPLOYMENT/*` |
| P20 | Reporting standards; the final research report | `FINAL_REPORT.md` |
| P21–P23 | Additional fire-physics, fusion, dataset reads | paper notes |
| DESIGN | HLD/LLD/component/repo-blueprint for the codebase phase | `DESIGN/*` |

Provenance caveat carried from the program itself: during the search phase a `web_search` outage meant many
arXiv identifiers were **subagent-reported and not independently re-fetched** — a disclosed residual risk
(`_CANON §7`), which the reference-verification pass (chapter 19 / QG2) samples and discloses.

## 25.3 Timeline B — the reference code (`trinetra/`)
Built after the research froze, as a numpy-core + torch-deep + Kaggle-scripts implementation of the admitted
subset. Milestones recorded in `trinetra/CODE_INVENTORY.md` and this session's work:

- Core packages implemented: `common/`, `ws1a_firephys/`, `ws1b_geophys/`, `ws2_deepfake/`, `ws3_alert/`,
  `ws4_cctv/`, `ws5_fusion_rl/`, `ws6_robust/`, `ws7_iot/`, `ws8_anomaly/`, `eval/`, `deep/`.
- Honesty/eval tooling added: ACI + Mondrian conformal (`ws6_robust/conformal.py`); Conformal Risk Control;
  BCa + stationary bootstrap (`eval/_stats.py`); calibration metrics (`eval/calibration.py`); Fukuzono
  prediction interval; the "real-win" admission gate (`eval/real_win.py`, `report.py`).
- Advanced math added: Iverson multi-pulse linear superposition; learned `AttentionFusionHead`;
  hierarchical two-layer fusion; correlation-aware BLUE/GLS weighting.
- Multi-GPU (T4×2) added to all training scripts: `nn.DataParallel` default + GPU-scaled batch + linear-LR
  scaling + AMP + cuDNN autotune (`deep/train.py`); DDP launcher (`deep/ddp.py`).
- **Final code-hardening audit (this session)** fixed three Kaggle-surfacing bugs — documented in
  chapter 13: (1) Geo-PINN `requires_grad_()` on a non-leaf scattered tensor under DataParallel →
  `.detach().requires_grad_(True)`; (2) `make_loader` `drop_last` dropping a small fold's only batch →
  guarded to `len ≥ 2·effective_batch`; (3) `GeoSeriesDataset` emitting `label=None` crashing
  `default_collate` → key omitted. Calibration diagnostics (ECE/MCE/Brier) added to `admit_model`.
- **Verification state at handover [CONFIRMED by running]:** `python run_tests.py` → 128 tests OK;
  `python scripts/ci_gates.py` → 6/6 PASS; `deep/` + `kaggle/` py_compile-clean; not GPU-run here.
- Honest limitation recorded: classifier/anomaly admission baseline is somewhat circular (logistic on the
  model's own OOF score) because no independent feature data exists yet; geo uses real static features.

## 25.4 Timeline C — this documentation set (`docs/`)
Built by an orchestrator + per-chapter subagents, each writing only its own file, grounded in `_CANON.md`
and named source artifacts, under the hard honesty rules.

| Round | Change | By |
|-------|--------|----|
| R1 | Audited artifacts; created `docs/`, `_CANON.md`, `PROGRESS_DOC.md`, `assets/`; wrote 00–03 | orchestrator |
| R1 | Launched chapter subagents (one per chapter, parallel, 8-child cap batched) | orchestrator |
| R1–R2 | Chapters 05, 07, 08, 09, 10, 11 returned and written | subagents |
| R1–R2 | Logged 6 cross-artifact consistency nuances for QG4 (see `PROGRESS_DOC.md`) | orchestrator |
| R2+ | Chapters 04, 06, 12–25 drafting / queued; verification + review passes pending | mixed |
| R3–R9 | All 26 chapters (00–25, incl. 04/04a, 05/05a/05b, 19/19a–d splits) written; `MASTER_combined.md`, `HANDOVER_SUMMARY.md` built; QG1–QG7 run; goal marked complete | mixed |
| R-followup | Independent spec-compliance gap-audit (2 auditors) + QG5 link-resolution pass (14 external URLs, 10 HTTP-200 verified, `docs/_QG5_link_verification_log.md`); ch04a dataset-field gap-fill; ch19 load-bearing author/BibTeX backfill; CORE runtime pins recorded (py 3.12.14 / numpy 2.3.5 / pandas 3.0.1 / lxml 6.1.3); Hinglish dataset-types explainer added | orchestrator + subagents |

(This table is updated every round; `PROGRESS_DOC.md` holds the live per-chapter status and quality-gate
state. The final build steps — `MASTER_combined.md`, `HANDOVER_SUMMARY.md`, QG1–QG7 — are recorded here on
completion.)

## 25.5 Reverted / rejected decisions (provenance of "no")
Kept here so a reader does not re-propose a closed idea. Full reasoning in chapter 24 (decision log).
- **IP-address-based alerting** → `[INFEASIBLE]`, rejected P12 (chapter 08).
- **Deployed on-device fire-PINN solver** → `[INFEASIBLE]` now, demoted to soft features, P7.
- **Autonomous public alerting** → disallowed (R19), permanent.
- **Random cross-validation** → rejected in favour of spatial-block CV (overstates skill).
- **Full SSL pretraining of a large FM on Kaggle** → `[INFEASIBLE]` under budget; PEFT/frozen-backbone
  adaptation instead (chapter 11 cut-list).
- **Paid data / paid cloud** → disallowed (free-data + Kaggle-only constraints).

## 25.6 Open provenance risks
- arXiv identifiers largely subagent-reported, not re-fetched (residual risk; sampled by chapter 19).
- All ₹ BOM figures `[EST]` (suppliers 403); ≤₹2000 gate not yet enforceable.
- Kaggle limits widely-published, not freshly fetched; re-confirm on the live quota panel.
- India regulatory / alerting-authority / LoRa-band facts `[UNVERIFIED]` — qualified-professional review
  required; nothing here is legal advice.
