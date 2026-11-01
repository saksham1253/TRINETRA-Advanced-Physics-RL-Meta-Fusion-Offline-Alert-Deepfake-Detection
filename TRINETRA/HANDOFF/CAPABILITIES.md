# CAPABILITIES (Figma Make agent, session 2026-10-31)
| Capability | Status | Evidence / fallback |
|-----------|--------|---------------------|
| Read + search whole repo | YES | cloned github.com/saksham1253/TRINETRA-CONTENT-OG (commit f8fee17) |
| Run code | YES (CPU, numpy/pandas/pillow in a venv; **no torch, no GPU**) | `run_tests.py` gives 128 OK; `ci_gates.py` gives 6/6 PASS; `demo.py` runs |
| Open web pages / verify links | YES via curl + Kaggle public API + arXiv API | snapshot `docs/tools/dataset_verify_2026-10-31.json` |
| Kaggle quota facts | NOT VERIFIED (docs are JS-rendered; repo `KAGGLE_BUDGET.md` also unverified) | team checks the quota panel in the account |
| Diagrams | Mermaid in markdown (renders on GitHub); no SVG export | `docs/02_PIPELINE_FLOWCHARTS.md` |
| Commit to GitHub | NO push. Local commits in the Figma Make project only | team copies the `TRINETRA/` new files into the GitHub repo |
| Torch / deep training | NO, so all deep changes are UNTESTED here | test commands are given for Kaggle |

Repo mirror note: `TRINETRA/` in this Make project = repo `default-workspace/` **minus binaries**
(png/jpg/pptx/docx/npy, node_modules) to keep it light (8.7 MB). Originals stay in GitHub.
<!-- END -->
