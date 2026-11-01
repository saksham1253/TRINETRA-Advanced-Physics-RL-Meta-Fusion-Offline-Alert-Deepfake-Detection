# INCIDENTS — interruptions, crashes, repairs (MASTER_PROMPT §0.4)

Append-only. Each entry: date, what happened, what was damaged, how verified/repaired.

## 2026-10-05 — Context compaction (not a crash)
- Event: automatic conversation checkpoint/compaction mid-Task-0.5.
- Damage: none to files (all P0 artifacts already on disk).
- Repair/verify: re-read ledger from files, re-ran grep dedup verification (235 unique
  confirmed), continued 0.5 → 0.6. No finished work restarted.

## Environment limitations logged (not incidents, but relevant to resume)
- No shell → SHA-256/size/mtime INFEASIBLE (DECISIONS D-003).
- Indian supplier pages 403 (Cloudflare) → BOM ₹ figures remain [EST] until re-verified.
- Semantic Scholar API 429 → arXiv API is primary discovery route.
- read/grep prune long-line middles → ledger read in ≤6-line windows.

## 2026-10-07 — §0.3 near-miss (self-caught, repaired same session)
- Event: while recording the WaveDINO (2606.16795) baseline re-study, I briefly edited the
  PRE-EXISTING original ledger row IN PLACE (changed its read_depth ABS→FT-PARTIAL, then added an
  annotation). This violates §0.3 (pre-existing rows must stay byte-for-byte untouched; the standing
  decision treats 02_paper_ledger.csv as strictly append-only for originals).
- Damage: none persisted. The original row 2606.16795 was restored byte-for-byte to its exact P2-era
  text; verified by re-reading the row.
- Repair: recorded the re-study as a SEPARATE APPENDED row `2606.16795-RESTUDY` tagged `[P3-RESTUDY]`
  at the end of the ledger, leaving the original untouched. CHANGELOG P3 block corrected to describe
  the append (not an in-place edit). Quota accounting unaffected (re-study is OQ-02 non-quota; NEW P3
  quota stays 32).
- Lesson: for ANY pre-existing-file row, never edit in place — always append a new row/record, even
  for annotations or depth promotions.
