# HANDOVER_SUMMARY — one-page map: which file answers which question

TRINETRA (HIMKAVACH) handover documentation. Start at `00_README_START_HERE.md`. The authoritative facts
live in `_CANON.md`; live build status in `PROGRESS_DOC.md`. One-line honesty frame: **nothing was trained
or measured — all domain numbers are source-reported from cited papers or planning estimates.**

## If your question is… read…
| Your question | File |
|---------------|------|
| What is this project, in one page? | `01_executive_summary.md` |
| How does the whole system fit together / data flow / tiers / interfaces? | `02_system_architecture.md`, `assets/architecture_diagrams.md` |
| What must it do / not do / under what constraints? | `03_requirements_and_scope.md` |
| What data does it use? sizes, licenses, splits, leakage? | `04_DATASETS.md` (+ `04a/04b` if split) |
| How does every model work (physics + neural)? formulation, I/O, training? | `05_MODELS.md` + `05a_MODELS.md` + `05b_MODELS.md` |
| Physics derivations + the meta-fusion design & validation? | `06_ws1_physics_and_fusion.md` |
| How is social-media / deepfake media handled? | `07_ws2_deepfake.md` |
| How does offline alerting work? why is IP-based alerting ruled out? | `08_ws3_offline_alerting.md` |
| How does CCTV fire/smoke detection work at the edge? | `09_ws4_cctv.md` |
| How does the RL advisory alarm policy work? why offline? the build gap? | `10_ws5_rl.md` |
| What are the Kaggle limits / 30 GPU-h budget / multi-GPU / resume? | `11_training_compute_kaggle.md` |
| How is anything evaluated? metrics, spatial-CV, baselines, the admission gate? | `12_evaluation_and_results.md` |
| What bugs were found & fixed? failure modes? before/after? | `13_robustness_bugs_fixes.md` (+ `13a/13b` if split) |
| Threat models, privacy, misuse, ethics, legal notes? | `14_security_privacy_ethics.md` |
| How is it deployed & operated? node, gateway, monitoring, runbooks? | `15_deployment_and_operations.md` |
| How is the codebase organized? module/API reference? how to extend? | `16_code_guide.md` (+ `16a/16b` if split) |
| What tests exist, how do I run them, what should I see? | `17_testing_and_validation.md` |
| How do I reproduce everything from scratch (exact commands)? | `18_reproduce_from_scratch.md` |
| Where is the full reference list with real arXiv IDs / BibTeX? | `19_REFERENCES_FULL.md` (+ `19a–19d` if split) |
| What does term/symbol/abbreviation X mean? | `20_glossary_and_notation.md` |
| I hit error X / my result differs from a paper / how do I add a dataset or model? | `21_faq_troubleshooting.md` |
| What are the limitations, risks, open problems? | `22_limitations_risks_open_problems.md` |
| What is planned next? | `23_future_work_roadmap.md` |
| Why was decision X made? what alternatives were rejected? | `24_decision_log.md` |
| What changed, when, why, by whom? | `25_changelog_and_provenance.md` |
| Beginner-friendly: what every TYPE of data/sensor is, how it's collected, why used (Hinglish)? | `DATASET_TYPES_EXPLAINED_hinglish_part1.md` + `_part2.md` |
| Were the external data/arXiv links actually checked, and when? | `_QG5_link_verification_log.md`, `_QG2_reference_verification_log.md` |
| What is the single source of truth / canonical facts? | `_CANON.md` |
| What is the live build + quality-gate status? | `PROGRESS_DOC.md` |
| Everything in one file? | `MASTER_combined.md` (37 files: 33 chapters + 4 appendices) |

## The five things a newcomer most often gets wrong (so, up front)
1. There are **no TRINETRA performance results** — by design (life-safety honesty). Numbers belong to cited papers.
2. The system is **advisory + human-in-the-loop**; it never originates a public alert on its own.
3. **IP-address-based alerting is infeasible** and was rejected — see `08`.
4. The **numpy core runs and passes 128 tests + 6 CI gates**; the **torch `deep/` layer is compile-only** here.
5. **Datasets are not downloaded** and their **licenses are unverified**; all are candidates.
