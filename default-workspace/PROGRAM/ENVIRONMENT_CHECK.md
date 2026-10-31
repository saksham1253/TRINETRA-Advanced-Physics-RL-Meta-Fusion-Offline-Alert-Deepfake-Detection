# PROGRAM — Environment Capability Check (Phase P0, Task 0.3)

Date: 2026-10-05
All rows below are **live-probed this session** unless marked [prior].

## 1. Headline flags (loud)
- ✅ **Web page reading WORKS** (HTTP 200 from HuggingFace, Kaggle this session).
- ✅ **arXiv abstract reading WORKS** (abs page HTTP 200; full abstract returned).
- ✅ **arXiv API discovery WORKS THIS SESSION** (HTTP 200, 453 results for a test query)
  — note: this previously timed out (30 s) on 2026-10-04; it is responsive now.
- ⚠️ **No PDF full-text probe run** (research-only phase reads abstracts; PDF fetch of
  arXiv `/pdf/<id>` is available via web_fetch but middle-prunes long docs — treat FT
  reads as windowed, not whole-doc).
- 🔥 **FULL-TEXT READING CRACKED (P1, 2026-10-05):** `https://ar5iv.labs.arxiv.org/html/<id>`
  and `https://arxiv.org/html/<id>` return GENUINE full text (Introduction, Methods,
  Results, Table/Figure refs, Limitations) — verified on 2608.12422 (read its actual
  ablation rule `roc_ablated > 0.02` and R5-claim logic from the Methods). This is the
  "khatarnaak" next-level route enabling TRUE Tier-2 depth, not abstract-only. CAVEAT:
  web_fetch still prunes the MIDDLE of long pages and `#Sx` anchors do NOT override it.
  MITIGATION: one fetch yields abstract+intro+methods-tail+results-head; fetch BOTH ar5iv
  and arxiv/html (different truncation points) to recover more middle; cross-check every
  number vs the abstract + pre-existing report; record per-note exactly which sections were
  seen (read-depth honesty, rule 10).
- 🔥 **BASELINE CORPUS LOCATED (P1):** `glob` with an ABSOLUTE path reaches the read-only root
  `C:\Users\Dell\Downloads\trinetra\papers\` → 131 PDFs, filenames = arXiv IDs (+ a few
  named: lhasa*, nhess*, joshimath*, chamoli*). `read` refuses local PDFs as "binary file"
  (extractor does not engage on the read-only root) → full text comes via arXiv-HTML by ID.
- 🔥 **BOM PRICE "khatarnaak alternative" (P6):** live supplier pages are 403, but
  `http://archive.org/wayback/available?url=<url>` responds → archived supplier snapshots +
  web_search price snippets + non-Cloudflare distributors are the P6 verification route.
- ⚠️ **Semantic Scholar API rate-limited** (HTTP 429, no key) — use only opportunistically.
- ⚠️ **Indian supplier pages BLOCKED** (Robu.in HTTP 403 / Cloudflare) → every ₹ BOM
  figure stays `[EST]`; price-verification gate is **BLOCKED** by tooling, deferred.
- ❌ **No shell/exec** → SHA-256, byte-size, mtime all INFEASIBLE (see manifests).
- ❌ **No `read_tabular` tool** this session → CSV parsed via `read`+`grep`.
- ❌ **No sub-agent / multi-agent spawning** → single-agent turn-based; any "parallel"
  work is sequential emulation. No faked agent output.
- ❌ **No `system_todo_write` tool** (returns "unknown tool") → P0 progress tracked inline.

## 2. Reachability probes (this session)
| Target | URL probed | Result |
|---|---|---|
| arXiv abs page | `arxiv.org/abs/2509.18176` | ✅ 200, abstract + authors returned |
| arXiv API | `export.arxiv.org/api/query?...` | ✅ 200, 453 results |
| Hugging Face | `huggingface.co/ibm-nasa-geospatial` | ✅ 200 (Prithvi model family live) |
| Kaggle | `kaggle.com/docs/notebooks` | ✅ 200 |
| Semantic Scholar | `api.semanticscholar.org/graph/v1/...` | ⚠️ 429 rate-limited (no key) |
| Indian seller (Robu.in) | `robu.in/product/...sx1262...` | ❌ 403 Cloudflare |
| Publisher/DOI | [prior] crossref/doi.org | reachable [prior], not re-probed |
| Gov (NRSC/Bhuvan/ISRO) | [prior] | not probed this phase |
| GitHub | [prior] raw.githubusercontent reachable | not re-probed |

## 3. Tool inventory (confirmed this session)
| Tool | Status |
|---|---|
| `web_fetch` | ✅ working (external pages + arXiv) |
| `read` | ✅ working; **middle-prunes windows >~6 lines on very long lines** → use ≤6-line windows for faithful long-row capture |
| `write` | ✅ working (workspace-write) |
| `edit` | ✅ assumed (read-before-edit enforced) |
| `glob` | ✅ working **but confined to workspace** — returns "No files found" for `trinetra\` even though direct `read` of a `trinetra\` path succeeds |
| `grep` | ✅ working; large outputs spill to a temp file; empty pattern rejected |
| `read_tabular` | ❌ unavailable this session |
| `system_todo_write` | ❌ "unknown tool" |
| sub-agents / workflow | ❌ unavailable (single-agent) |
| shell/exec | ❌ unavailable → no hashes/sizes/mtimes |
| skills | ✅ catalog = diagnose-windows-sandbox-acl, office-docx, office-pptx, office-xlsx, tabbit |

## 4. Known limits / quirks to carry forward
- Long CSV rows: read in ≤6-line windows (leading + trailing fields always survive;
  8–12-line windows prune the `takeaway` middle of interior rows).
- arXiv transient "fetch failed"/timeout → retry serially, do not parallel-hammer.
- Never guess arXiv IDs or author names from pruned API middles (prior sessions caught
  ~50% wrong-author and 2 wrong-ID fabrications) → verify via abs page or use
  `(authors)` placeholder.
- Sandbox "current date" resolves to 2026 → some real arXiv IDs look future-dated.

## 5. Net effect on the program
Core research loop (search → verify → abstract-read → note) is **fully operational**.
The only tooling-blocked deliverable is **live price verification** (supplier 403s) →
procurement/BOM figures remain `[EST]` and that gate is explicitly deferred until a
reachable price source is found. Integrity hashing is INFEASIBLE and substituted by
line-count proxies, disclosed everywhere.
