# PROGRAM — Pre-Program Backup Manifest (Phase P0, Task 0.2)

Date: 2026-10-05
Dir: `PROGRAM/backups/2026-10-05_pre_program/`

## Policy: copy-on-write (CoW), not mass-copy

**Why not a bulk copy now.** No shell/`cp`/hash tool exists in this environment, and the
`read` tool prunes the *middle* of long files (confirmed on `02_paper_ledger.csv` rows and
`04_synthesis.md`). A bulk read→write "backup" of the long files could therefore silently
produce a **corrupted** copy — strictly worse than no copy. Producing a backup I cannot
prove is faithful would also violate the program's honesty rules.

**The actual non-destruction guarantee (two layers):**
1. **New-name-only.** Every program artifact (Tasks 0.1–0.9 and all later phases) is
   written to a **new path** under `PROGRAM/` or as a new `analysis/*` file. No
   pre-existing file is overwritten, renamed, or deleted. (If a re-save of an existing
   file is ever needed, it is written as `*_v2`, never in place.)
2. **Copy-on-write snapshots.** The *first* time any later task must edit a pre-existing
   file in place, it will **first** snapshot that file into this directory as
   `PROGRAM/backups/2026-10-05_pre_program/<original_name>` (faithfully, in small
   non-pruning read windows), log the snapshot in `PROGRAM/CHANGELOG.md`, and only then
   edit. Until that happens, this directory intentionally holds only this manifest.

## Files under protection (pre-existing, as of P0)
All 13 pre-existing content files inventoried in
`PROGRAM/manifests/folder_inventory.md` §2.1–§2.2 are under this protection
(the 6 root `TRINETRA_*.md` + the 7 `analysis/*`). `PROGRAM/MASTER_PROMPT.md` is also
protected (never re-written; re-save would be `MASTER_PROMPT_v2.md`).

The read-only `trinetra\` root needs no backup: it is outside the write boundary and
cannot be modified by any available tool.

## Status
- P0 performs **no in-place edits** → no snapshots taken yet. This is expected and correct.
- CoW trigger is armed for later phases.
