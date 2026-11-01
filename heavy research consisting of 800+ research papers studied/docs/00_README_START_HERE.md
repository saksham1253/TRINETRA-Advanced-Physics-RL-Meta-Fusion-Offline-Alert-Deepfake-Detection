# 00 — START HERE: Map, Reading Order, Audience Guide, Quick Start

Welcome. This is the complete handover documentation for **TRINETRA** (alternative name **HIMKAVACH**), an
offline-first, physics-grounded, **advisory** early-warning and hazard-detection research program and its
reference code implementation. This chapter tells you what this project is, what it is *not*, where every
answer lives, and how to get running in ten minutes.

---

## 0.1 The one thing to understand before anything else

This project has **two layers**, and confusing them is the single most common mistake:

1. **A research-only program.** Its own `FINAL_REPORT.md` says verbatim: *"Nothing was built, trained, or
   measured."* Every performance number anywhere in the research artifacts is **source-reported** from other
   people's papers on their own data. The program's job was to decide *what to build and why*, grounded in
   631 arXiv references (the FINAL_REPORT snapshot figure; the live ledger has since grown to ~775 — see
   `_CANON §7` and chapter 19).
2. **A reference code implementation** (`trinetra/`) written later: a pure-**numpy core** that runs and
   **passes 128 unit tests + 6 CI gates**, a **PyTorch `deep/`** layer (6 trainable models) that is
   **compile-verified but never GPU-trained here**, and **Kaggle training scripts** that are **multi-GPU
   ready but not executed on a GPU** in this environment.

> **No TRINETRA model has been trained and no dataset has been downloaded.** Any accuracy, latency, recall,
> false-alarm, or cost number you see attributed to a *paper* is that paper's result, not ours. Where you
> might expect a TRINETRA result, the honest answer is **"not measured."** This is not a gap in the
> documentation — it is the actual, deliberate state of the project (life-safety domain, honesty-first).

If you remember only this section, you will not misread the rest.

---

## 0.2 Who are you? Pick your reading path

| You are… | Read, in this order |
|----------|---------------------|
| **A new engineer about to build** | 00 → 01 → 02 → 16 (code guide) → 17 (testing) → 18 (reproduce) → 11 (Kaggle) → the WS chapter you own (06–10) |
| **A professor / scientific reviewer** | 00 → 01 → 06 (physics derivations) → 12 (evaluation protocol) → 19 (references) → 22 (limitations) → 13 (bugs) |
| **A hackathon judge / PM** | 00 → 01 (executive summary) → 02 (architecture) → 22 (limitations) → 23 (roadmap) |
| **A safety / ethics / legal reviewer** | 00 → 01 → 14 (security/privacy/ethics) → 08 (alerting + the IP verdict) → 22 (limitations) |
| **The original author, six months later** | 00 → 24 (decision log) → 25 (changelog) → 16 (code guide) → PROGRESS_DOC.md |
| **A deployer / ops engineer** | 00 → 02 → 15 (deployment/ops) → 11 (compute) → 21 (FAQ/troubleshooting) |

---

## 0.3 The full map — which file answers which question

```
docs/
  _CANON.md                        single source of truth (facts, labels, verdicts, WS mapping)
  PROGRESS_DOC.md                  build tracker + source-artifact audit + quality-gate status
  00_README_START_HERE.md          ← you are here
  01_executive_summary.md          what it is, results posture, limits, verdicts (1–2 pp)
  02_system_architecture.md        end-to-end design, data flow, tiers, interfaces, diagrams
  03_requirements_and_scope.md     goals, non-goals, assumptions, hard constraints
  04_DATASETS.md                   every dataset: provenance, structure, license, splits, status
  05_MODELS.md                     every model: formulation, I/O, training recipe, calibration
  06_ws1_physics_and_fusion.md     physics derivations + meta-fusion design & validation
  07_ws2_deepfake.md               media-authenticity (low-trust advisory, defensive-only)
  08_ws3_offline_alerting.md       tiered offline alerting + the IP-address INFEASIBLE verdict
  09_ws4_cctv.md                   CCTV fire/smoke detection + edge features
  10_ws5_rl.md                     offline-RL advisory alarm policy + OPE gate + shield
  11_training_compute_kaggle.md    verified-at-build Kaggle limits, 30 GPU-h budget, resume logic
  12_evaluation_and_results.md     protocols (spatial-CV), metrics, baselines, admission gate
  13_robustness_bugs_fixes.md      failure-mode catalogue + bug ledger + fixes + before/after
  14_security_privacy_ethics.md    threat models, privacy, misuse, legal notes (NOT legal advice)
  15_deployment_and_operations.md  edge topology, monitoring, degradation, runbooks
  16_code_guide.md                 repo map, module/API reference, configs, conventions
  17_testing_and_validation.md     test suites, how to run, expected output
  18_reproduce_from_scratch.md     zero-to-results runbook with exact commands
  19_REFERENCES_FULL.md            all references, full detail, BibTeX, verification status
  20_glossary_and_notation.md      every term, abbreviation, symbol, unit
  21_faq_troubleshooting.md        "error X, what now", "differs from paper", "add a dataset"
  22_limitations_risks_open_problems.md
  23_future_work_roadmap.md
  24_decision_log.md               every major decision, alternatives, evidence, date
  25_changelog_and_provenance.md   what changed, when, why, which agent
  assets/                          diagrams, tables, figures
  MASTER_combined.md               everything concatenated (built last)
  HANDOVER_SUMMARY.md              one-page: which file answers which question
```

---

## 0.4 Quick start (10 minutes, no GPU, no datasets)

The numpy core runs with only Python + numpy. [CONFIRMED — this is exactly what was run to validate it.]

```powershell
# from the repository root that contains the trinetra/ folder
cd trinetra
$env:PYTHONIOENCODING = "utf-8"              # Windows: make unittest output UTF-8 clean
python run_tests.py                          # expect: "Ran 128 tests ... OK"
python scripts/ci_gates.py                   # expect: "ALL 6 CI GATES PASSED"
python demo.py                               # end-to-end advisory decision on synthetic evidence
```

Expected: 128 tests pass, 6 gates pass. (`run_tests.py` may print a spurious `[exit code: 1]` because
unittest writes its summary to stderr; the real pass signal is the final line `OK`.) The PyTorch models in
`trinetra/src/trinetra/deep/` and the Kaggle scripts in `trinetra/kaggle/` require a GPU environment and are
documented in chapters 05, 10 and 11 — they are **not** needed for the quick start.

---

## 0.5 How to trust this documentation (the honesty contract)

Every non-trivial claim is tagged: `[CONFIRMED]`, `[LIKELY]`, `[HYPOTHESIS]`, or `[INFEASIBLE]` (defined in
`_CANON.md §1`). "Our measurement" and "Paper X reports" are always kept visibly separate. Numbers that were
never measured say "not measured". References carry a real arXiv ID / DOI and a verification status.
Failures and reversed decisions are reported plainly (see chapters 13 and 24), including the headline
negative result that **IP-address-based alerting is infeasible** for life-safety targeting (chapter 08).

If you find a claim without a label, a number without a source, or a contradiction between two chapters,
that is a bug in the documentation — log it against the consistency gate in `PROGRESS_DOC.md`.

---

## 0.6 Scope in one breath
Rapid-onset mountain hazards (landslide, flash-flood, cloudburst, GLOF) in Uttarakhand + Himachal, plus
fire/disaster detection via CCTV + IoT + free satellite data, fused into a **calibrated, shielded, advisory**
alert level for a **human** operator who alone decides on public dissemination. Offline-first; ≤₹2000 IoT
node; ≤30 Kaggle GPU-h/week; never an autonomous public alert. Full scope and non-goals: chapter 03.
