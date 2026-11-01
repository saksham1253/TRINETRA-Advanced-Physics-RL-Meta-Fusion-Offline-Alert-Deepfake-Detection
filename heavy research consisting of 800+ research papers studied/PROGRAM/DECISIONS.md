# PROGRAM DECISIONS LOG

Append-only. Each entry: ID, date, decision, rationale, status. New program (phases P0–P20)
under `PROGRAM/MASTER_PROMPT.md`.

---

## D-001 — Two-root split; canonical root = writable default-workspace
Date: 2026-10-05 · Phase P0
Decision: The project spans two filesystem roots:
- **Writable / canonical:** `C:\Users\Dell\Documents\deepseek-harness\default-workspace\`
  (= working dir). ALL new `PROGRAM/` and `analysis/` program output lives here.
- **Read-only source:** `C:\Users\Dell\Downloads\trinetra\` — the original project
  (report, decks, papers, research notes). Never modified; not glob-enumerable from the
  workspace (direct `read` works).
Rationale: workspace-write sandbox + non-destruction mandate. glob is confined to the
workspace, so trinetra\ is inventoried via known direct paths only.
Status: ACTIVE.

## D-002 — Non-destructive / copy-on-write (CoW) file policy
Date: 2026-10-05 · Phase P0
Decision: Never delete/overwrite/rename a pre-existing file. New outputs use new names;
re-saves of governed files use `*_v2`. Before the FIRST in-place edit of any pre-existing
file, copy it to `PROGRAM/backups/2026-10-05_pre_program/<name>` and log in CHANGELOG.
P0 performed zero in-place edits.
Rationale: MASTER_PROMPT non-destruction mandate; no shell for bulk backup.
Status: ACTIVE.

## D-003 — Integrity hashing infeasible → line-count proxy
Date: 2026-10-05 · Phase P0
Decision: SHA-256 / byte-size / mtime are recorded as `INFEASIBLE (no shell)` in all
manifests; file identity is proxied by measured line counts.
Rationale: no shell/exec tool available (ENVIRONMENT_CHECK.md).
Status: ACTIVE — revisit if a hashing capability appears.

## D-004 — Corpus count reconciled to 235 unique ABS papers
Date: 2026-10-05 · Phase P0 · Task 0.5
Decision: The authoritative literature count is **235 unique new papers, all ABS, 0 FT**
(250 ledger data rows − 1 dedup marker − 14 redundant duplicate rows). The 2026-10-04
RESUME_STATE (96 net-new) was a superseded mid-harvest checkpoint, not a conflict.
Rationale: grep-verified duplicate groups + full ledger observation; see
`PROGRAM/manifests/novelty_index.csv` and `PROGRAM/audits/PHASE_00_reconciliation_audit.md`.
Status: ACTIVE.

## D-005 — Duplicate rows flagged, NOT deleted
Date: 2026-10-05 · Phase P0
Decision: The 14 redundant rows remain in the ledger (non-destruction). They are recorded
in the novelty index; on a future AUTHORIZED consolidation, keep the richer-authored row
and drop the `(authors)` twin, with a CoW backup first.
Status: ACTIVE.

---

## D-006 — OLD→NEW phase-ID mapping
Date: 2026-10-05 · Phase P0 · Task 0.5
The prior artifacts used an informal "Phases 1–6" / workstream (WS1–WS7) scheme and a flat
set of root `TRINETRA_*.md` deliverables. The new program uses phases P0–P20
(MASTER_PROMPT §0.11). Mapping of prior work onto new phases (prior work is treated as
BACKGROUND, re-examined under the new evidence rules, NOT inherited as conclusions):

| OLD artifact / phase | Content | Maps to NEW phase(s) |
|---|---|---|
| OLD "Phase 1–3" literature harvest (02_paper_ledger, search_log) | 235 ABS papers, 14 axes | **P2 + P3** (SOTA + deep lit); subject to Tier-2 re-read |
| OLD "Phase 4" synthesis (04_synthesis.md) | 250-paper interim synthesis, 9 failure surfaces | feeds **P4** (synthesis/gap) |
| 00_system_model.md | system decomposition, 14 axes defined | feeds **P1** (problem framing / system model) |
| TRINETRA_Deep_Analysis.md | PhD-level expert review | background to **P4/P5** |
| TRINETRA_Bug_Report.md (#0–#32) | 33 adversarial findings | background to **P5** (risk/failure analysis) |
| TRINETRA_Bug_Robustification.md (FIX #0–#15) | fixes/spec | background to **P6+** (design) |
| TRINETRA_Corrected_Patches.md (A–I) | corrected report patches | background to **P6+** |
| TRINETRA_MetaFusion_Design.md (GMF) | fusion-head design | background to **P7+** (architecture) |
| TRINETRA_Workstreams.md (WS1–WS7) | workstream breakdown | informs **P-plan** sequencing |
| TRINETRA_Complete_Report.md v1.0 (2966 ln) | the shipped report | the OBJECT under study across all phases |

Note: exact P1–P20 titles are refined in `PROGRAM/PHASE_PLAN.md` (Task 0.7). This table is
the provenance bridge so no prior finding is silently promoted into the new program without
re-examination.

---

## D-007 — User answers to the five P0 gate open questions (binding)
Date: 2026-10-05 · Phase P1 entry
User replied to the P0 gate ("GO PHASE P1 ... all out") with explicit answers:
1. OQ-01 (canonical root): **default** → `default-workspace\` canonical, `trinetra\` read-only.
   CONFIRMED. Supersedes the "proceed as default" status of D-001 (now user-confirmed).
2. OQ-02 (235 ABS corpus): **handle the 235 already-studied papers first (bring them to
   proper depth), THEN do additional new research.** → In P1/P2 the existing corpus is
   promoted to full-text/Tier-2 depth BEFORE net-new discovery beyond the quota. The 235
   remain non-quota (they were already counted as discovered); quota = NEW papers on top.
3. OQ-03 (reading depth): user asks for a **"khatarnaak" next-level reading method** so papers
   can be read in true depth. RESOLVED THIS SESSION: arXiv-HTML / ar5iv full-text route
   (logged in ENVIRONMENT_CHECK §1). Line-count-proxy for file *identity* still stands
   (that was OQ-03's original hashing question) — accepted as default.
4. OQ-04 (single-agent audit emulation): **default** → accepted (fresh re-open pass).
5. OQ-05 (BOM prices): user asks for a **"khatarnaak" alternative** to the 403-blocked
   supplier pages. RESOLVED (route proven): Wayback archived supplier snapshots + web_search
   price snippets + non-Cloudflare distributors; executed in P6.
Status: ACTIVE. These bind all subsequent phases.

## D-008 — Full-text reading via arXiv-HTML/ar5iv is the standard Reading-Engine route
Date: 2026-10-05 · Phase P1
Decision: Tier-2+ reads are performed against `https://ar5iv.labs.arxiv.org/html/<id>` and/or
`https://arxiv.org/html/<id>`. Local baseline PDFs are identified by arXiv ID from their
filename and read via this route (the `read` tool cannot extract the read-only-root PDFs).
Rationale: delivers genuine method/experiment/limitation text (verified on 2608.12422),
satisfying read-depth honesty (rule 10). Caveat/mitigation for middle-prune recorded in
ENVIRONMENT_CHECK §1. Status: ACTIVE.
Status: ACTIVE.

## D-009 — P3 foundation-set scope: depth-first, honest shortfall over padding; ~50 deep reads
Date: 2026-10-06 · Phase P3 · (user-confirmed "Depth-first + honest shortfall", then "get around 50 new papers in depth covering the P3 themes in detail")
Decision: P3 prioritizes DEPTH over hitting the raw 250 count. Concretely:
- Read **~50 NEW FT-PARTIAL Tier-2+ papers** (user-raised target) across ALL P3 themes
  (physics/PIML, media forensics, alerting/networks, RL for emergency response, IoT/TinyML,
  anomaly-detection basics, safety/privacy/security, adjacent transferable). Quota floor ≥15 NEW
  easily exceeded; ~50 is the working target.
- Harvest abstract-verified NEW papers for foundation VOLUME ONLY where relevance is genuine
  (novelty-checked, real abstracts) — never pad to a number (§0.5 no-padding rule).
- At the gate, report the EXACT foundation-set count AND the full tier distribution, explicitly
  flagging that "250 papers AND ≥60% Tier-2+" is not honestly reachable under the research-only
  tool constraints (full-text = one-at-a-time web_fetch of ar5iv/arXiv-HTML; ~8 hits per API query;
  the inherited 235 baseline is abstract-only and only partially re-studied).
Rationale: The master prompt's P3 acceptance explicitly permits "an honest shortfall report with
reasons," and §0.5 forbids padding. The 250-count and 60%-Tier-2+ ratio pull in opposite directions
under our tools; depth + honesty win. ~50 deep reads this phase maximizes Tier-2+ foundation value.
Counting convention locked for P3: headline "foundation set" count = program-era NEW papers
(P2 + P3), reported alongside (a) deep-read count, (b) baseline-235 re-study status, (c) tier split
— all shown separately so no single number is misleading.
Status: ACTIVE.

---

## D-010 — P3 stop-at-~40; hazard-core priority; multi-source reading; SOTA reachable cumulatively
Date: 2026-10-07 · Phase P3 · (user instruction verbatim: "stop at 40 and go for hazard-core ... use
different websites as well ... SOTA is possible because we have 20 phases and in each phase there are
15 papers so around 300 and previously studied 235 + preexisting 118 ... go with option 1 [ABS note]")
Decision:
- **STOP P3 reading at ~40 NEW** (currently 37 → ~3 more), then build the 7 gate deliverables. The ~50
  working target from D-009 is SUPERSEDED down to ~40 by this instruction.
- **Prioritize HAZARD-CORE** (landslide / flood / GLOF / InSAR / precipitation forecasting; WS1/WS3/WS8)
  for the remaining reads over method-theme papers.
- **Use NON-arXiv sources too.** arXiv querying was hitting the SAME redundant hits + frequent NO-HTML.
  Expand to open-access full-HTML hazard venues: NHESS/Copernicus (nhess.copernicus.org), The Cryosphere,
  MDPI (Remote Sensing / Water / GeoHazards), Frontiers, PLOS, journal HTML. ALWAYS grep
  `03_paper_notes/` + ledger for the ID/title BEFORE fetching, to avoid re-reading.
- **ABS-only policy = option 1:** any NO-HTML paper whose abstract carries decision-relevant signal gets
  a flagged ABS note (read_depth=ABS, NON-QUOTA); if the abstract fully conveys the paper, that is
  acceptable and noted as such. ABS notes NEVER count toward the ~40 NEW quota.
- **SOTA/foundation IS reachable cumulatively (CORRECTION to D-009's shortfall framing).** Program math:
  ~118 pre-existing + 235 re-studied baseline + program-era NEW (~15/phase × up to 20 phases ≈ 300)
  → the ≥250 @ ≥60% Tier-2+ foundation is achievable ACROSS the program, not required within any one
  phase. Gate reporting must present it as a CUMULATIVE trajectory, not a per-phase shortfall. If more
  reads are genuinely needed for SOTA coverage of a theme, do them; otherwise advance.
Rationale: User reframed the counting at program scale (correct) and set a concrete P3 stop point to
move into synthesis/gate artifacts sooner. Multi-source reading breaks the arXiv redundancy/NO-HTML
bottleneck and improves genuine SOTA coverage.
Status: ACTIVE.

---

## D-011 — ADD mandatory new phase P14Z (Zero-Shot & Open-Vocabulary Classification), after P14 meta-fusion
Date: 2026-10-07 · (user instruction, verbatim intent: "the final project can do zero shot classification
... add a phase for this also research on it as well in detail read around 10 papers and more if needed
and do this after ... meta fusion phase and you can adjust the sequence accordingly as needed but doing
this is compulsory")
Authority: MASTER_PROMPT §0.1 rule 9 explicitly permits "add a phase you find necessary" with user
approval. User has now MANDATED it → authorized. The verbatim MASTER_PROMPT.md is NOT edited (§0.3
non-destruction); the new phase is registered in the program planning docs (PHASE_PLAN, PHASE_BACKLOG,
PHASE_STATE, this log) where sequence/scope changes belong.
Decision:
- **New phase ID = `P14Z`** (deliberately NOT a renumber of P15–P20, to avoid breaking the ~dozens of
  existing cross-references to P15/RL, P16/robustness, P17/P18/features, P19/India, P20/final). P14Z
  sorts immediately AFTER P14 and BEFORE P15.
- **Name:** Zero-Shot & Open-Vocabulary Classification (research & design).
- **Why it belongs after P14 (meta-fusion):** zero-shot/open-vocab heads are a CONSUMER of the fused
  representation + a SOURCE of extra class signals the GMF must calibrate and gate. Designing it before
  the fusion contract (P14) is premature; designing it before RL (P15) is correct because any zero-shot
  hazard/scene labels feed the alarm-policy state. Soft-depends on P8 (CCTV vision), P9/P10 (anomaly),
  CR-01 EO-FM encoder trade study (P7-era).
- **Scope (research-only, per whole program):** survey + design, NO training/building. Study how far a
  deployed TRINETRA can classify hazards/scenes/conditions it was NEVER explicitly trained on, via:
  (a) vision-language / CLIP-style open-vocabulary classification; (b) remote-sensing foundation-model
  zero-shot (RemoteCLIP/GeoRSCLIP/SkyCLIP-type) for EO scene/condition tags; (c) zero-shot ANOMALY
  detection (WinCLIP/AnomalyCLIP-type) for novel hazard appearance; (d) zero-shot transfer of hazard
  models across regions/hazards (ties the domain-shift + data-scarcity threads). Deliver: SOTA scan,
  ≥10 NEW in-depth reads (more if needed), a design doc for a zero-shot/open-vocab layer with HONEST
  limits (calibration, hallucinated-label risk, life-safety gating under Rule 19), failure modes, and
  how its outputs enter the GMF + conformal + shield stack (zero-shot labels are LOW-TRUST by default:
  advisory, never an autonomous alarm trigger).
- **Quota:** carries the standard phase quota — ≥15 NEW novelty-checked papers / SOTA scan / exit audit
  per §0.9; user's "~10" is the FLOOR for the zero-shot-specific core, the §0.9 ≥15 still governs the
  full phase (zero-shot core + adjacent open-vocab/transfer reads together ≥15).
- **Sequence impact:** recommended sequence becomes ... → P13 → P14 → **P14Z** → P15 → P16 → ... → P20.
Rationale: user judged (from the 118 pre-existing papers) that the built system can plausibly do
zero-shot classification; capturing that capability as a first-class, evidence-grounded design phase is
compulsory and genuinely strengthens rare-hazard coverage (few/no labels for GLOF-type events).
Status: ACTIVE (phase not yet started; will run in sequence after P14, which itself is not yet reached).

---

## D-012 — P4 key-questions update + locked design defaults (DC-01/DC-02/DC-03)
Date: 2026-10-07 · Phase P4
Decision: The P1-locked `analysis/00_key_questions.md` is updated (append-only P4 block) with 8 answered
questions, carried-open items, and 5 new questions (Q9.1–Q9.5). Per the P1 lock rule, this change is
recorded here. In addition, the three P0 (gate-blocking) design changes from `analysis/07_design_changes.md`
are adopted as LOCKED DEFAULTS for all build phases unless the user objects at/after the P4 gate:
- **DC-01** spatial-CV with a correlation-range buffer is the only admissible evaluation (2610.08227).
- **DC-02** primary metric = cost-loss Value Score / Total Classification Cost (2510.22016).
- **DC-03** conformal must be action-loss-calibrated AND mask-conditional AND online (2609.14821 /
  2512.14221 / 2610.02777).
Rationale: these are cheap to adopt now, very expensive to retrofit, and over-determined by the corpus;
they gate the credibility of every downstream performance claim (Rule 16).
Status: ACTIVE (defaults; revisable on user objection).

## D-013 — P4 honest-count correction: 2509.18176 is a re-study, not a new read
Date: 2026-10-07 · Phase P4
Decision: During the P4 exit audit (Audit #10) 2509.18176 was found already read FT-PARTIAL in P2. It is
excluded from the P4 NEW-read quota and reclassified as a RE-STUDY; 2605.14365 (LoMETab) was read as the
genuine 15th quota paper. 2510.12328 remains ABS/NO-HTML → non-quota corroborator (C-06). Net P4 NEW deep
reads = 15 (100% Tier-2+). Running program-era deep NEW reads: P1 15 + P2 18 + P3 43 + P4 15 = 91.
Rationale: hard-honesty / no-padding (§0.5); the ledger, reading-progress tally, SOTA PART C, and Audit
#10 all carry the correction.
Status: ACTIVE.
