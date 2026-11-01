# PROGRAM — Folder Inventory (Phase P0, Task 0.1)

Date: 2026-10-05
Author: research agent (single-agent, turn-based)
Scope: both project roots. This is a **read/observe-only** inventory. No existing file
is modified, renamed, or deleted by this task.

> **Measurement limitation (loud, honest).** No shell/exec tool is available in this
> environment. Therefore **file byte-size, modification time (mtime), and SHA-256 hash
> cannot be computed**. Where the §0.1 spec asks for size/mtime/SHA-256, this manifest
> records `INFEASIBLE (no shell)` and substitutes **line counts** (obtained via the
> `read`/`grep` tools) as the best available integrity proxy. This limitation is also
> recorded in `PROGRAM/ENVIRONMENT_CHECK.md` and the Phase-00 report.

---

## 1. Two-root structure

| Root | Path | Access | glob-enumerable? | Role |
|---|---|---|---|---|
| **Writable** | `C:\Users\Dell\Documents\deepseek-harness\default-workspace\` | read + write (DSH workspace-write) | YES | ALL program output (`PROGRAM/`, new `analysis/` artifacts) goes here. Canonical working root. |
| **Read-only** | `C:\Users\Dell\Downloads\trinetra\` | read only (direct `read` succeeds; outside write boundary) | **NO** (glob confined to workspace) | Original delivered TRINETRA project. Inventoried via known direct paths only. Never written to. |

**Decision (recorded in DECISIONS.md):** the writable `default-workspace\` is the
canonical program root. The `trinetra\` download is treated as an immutable source
corpus — read, cite, never modify.

---

## 2. Writable root — `default-workspace\` (glob-enumerated, complete)

### 2.1 Root-level OLD-scheme deliverables (pre-existing; DO NOT MODIFY)
| File | Lines | Size/mtime/SHA-256 | Notes |
|---|---|---|---|
| `TRINETRA_Deep_Analysis.md` | 183 | INFEASIBLE (no shell) | PhD-level deep analysis / expert review |
| `TRINETRA_MetaFusion_Design.md` | 126 | INFEASIBLE (no shell) | GMF decision-head design |
| `TRINETRA_Bug_Report.md` | 406 | INFEASIBLE (no shell) | 33 findings #0–#32 |
| `TRINETRA_Bug_Robustification.md` | 333 | INFEASIBLE (no shell) | FIX #0–#15 + Appendices C–E |
| `TRINETRA_Corrected_Patches.md` | 297 | INFEASIBLE (no shell) | 9 line-anchored patches A–I |
| `TRINETRA_Workstreams.md` | 235 | INFEASIBLE (no shell) | WS1–WS7 engineering plan |

### 2.2 `analysis\` (pre-existing; DO NOT MODIFY — back up before any edit)
| File | Lines | Size/mtime/SHA-256 | Notes |
|---|---|---|---|
| `analysis\00_system_model.md` | 110 | INFEASIBLE (no shell) | Architecture + 14 search axes A1–A14 |
| `analysis\02_paper_ledger.csv` | 251 | INFEASIBLE (no shell) | 1 header + 250 data rows. PRIMARY artifact (row = ABS note). ~236 unique IDs (see 0.5). |
| `analysis\02_search_log.md` | 170 | INFEASIBLE (no shell) | 135 queries logged |
| `analysis\04_synthesis.md` | 546 | INFEASIBLE (no shell) | Interim synthesis @ 250-paper checkpoint |
| `analysis\11_reading_audit.md` | 191 | INFEASIBLE (no shell) | 6 audits, all 0% error |
| `analysis\PROGRESS.md` | 109 | INFEASIBLE (no shell) | OLD Phase 1–6 scheme (stale vs new P0–P20) |
| `analysis\RESUME_STATE_2026-10-04.md` | 137 | INFEASIBLE (no shell) | Prior snapshot (98-line/96-row era) |

### 2.3 `PROGRAM\` (program-era; MASTER_PROMPT pre-existing, rest net-new this phase)
| File | Lines | Size/mtime/SHA-256 | Notes |
|---|---|---|---|
| `PROGRAM\MASTER_PROMPT.md` | 827 | INFEASIBLE (no shell) | Governing directive, saved verbatim by user (task 0.0 verified) |
| `PROGRAM\manifests\folder_inventory.md` | (this file) | INFEASIBLE (no shell) | — |
| (other `PROGRAM\**` artifacts) | created in tasks 0.1–0.9 | INFEASIBLE (no shell) | net-new, non-destructive |

**Writable-root duplicate / corrupt / zero-byte scan:** none at the file level. All 14
pre-existing files are non-empty and parse. The only *intra-file* duplication is inside
`02_paper_ledger.csv` (≈14 duplicate arXiv-ID row pairs → 250 rows ≈ 236 unique papers);
this is reconciled in Task 0.5, not here.

---

## 3. Read-only root — `trinetra\` (known-path inventory; NOT glob-enumerable)

> glob on this root returns "No files found" because the glob tool is confined to the
> workspace. Direct `read` of a known path **does** succeed. The following is assembled
> from paths confirmed in prior sessions; it is **not guaranteed exhaustive** (cannot be,
> without enumeration). Items are marked [CONFIRMED path] where a direct read succeeded
> previously, [KNOWN] where recorded in prior state but not re-read this phase.

### 3.1 `trinetra\deliverables\`
| File | Status | Notes |
|---|---|---|
| `TRINETRA_Complete_Report.md` | [CONFIRMED] 2966 lines, v1.0 | Source of truth for 00_system_model.md |
| HIMKAVACH / TRINETRA `.pptx` / `.pdf` / `.docx` | [KNOWN] | Pitch decks / docs |
| `unstop_deck_src\` | [KNOWN] | Deck source |
| `TRINETRA-explainer.mp4` | [KNOWN] | Explainer video (binary, not read) |

### 3.2 `trinetra\papers\`
| Group | Status | Notes |
|---|---|---|
| `cctv_comms\`, `iot\`, `multimodal\` `*.txt` extracts | [KNOWN] | Baseline corpus: 244 paths = 110 unique papers (116 extracts, 6 cross-folder dups). NOT counted toward NEW-paper quota. |

### 3.3 `trinetra\research\`
| File | Status | Notes |
|---|---|---|
| `00_master` … `08_closure` (11 files) | [KNOWN] | Prior research notes incl. `06_physics` |

### 3.4 `trinetra\` root
| File | Status | Notes |
|---|---|---|
| `CLAUDE.md` | [KNOWN] | Project agent instructions |
| `AGENTS.md` | [KNOWN] 41 lines | Figma Make React/Vite/Tailwind stack |
| `.figma\` | [KNOWN] | Figma assets |
| `Proxy.py` | [KNOWN] | **Bug #12**: forwards credentials to `https://api.justwoker.icu` |

**Read-only-root duplicate note:** the 6 cross-folder duplicate extracts in `papers\`
are already accounted for in the "110 unique / 116 extracts" figure and are correctly
excluded from the NEW-paper count. No corrupt/zero-byte files observed on the paths read.

---

## 4. Cross-reference to machine-readable manifest
Per-file rows (both roots) are also in `PROGRAM/manifests/file_manifest.csv` with the
same size/mtime/SHA-256 = `INFEASIBLE (no shell)` convention and line-count proxy.
