# FIGMA_STATE — deck + "TRINETRA Explained" (prompt: TRINETRA_FIGMA_DECK_AND_DOC_PROMPT.md), updated 2026-10-31 11:20 UTC

**Where the deck lives:** this is a Figma **Make** project, so the deck is built as code (not a Figma Design file):
`src/deck/` → open the app preview at `#deck` (arrow keys, N = speaker notes, "Export PDF" = print). `#deck-raw?s=N` renders one slide at 1920×1080.
Exports: `TRINETRA/exports/TRINETRA_deck_phase1.pdf` (8 pages = title + 7, 1920×1080) + `slide_0_title.png`, `slide_1..7.png`. `#deck-raw?s=0` is the title.
Numbers: `src/deck/numbers.json` (source of truth) mirrored to `docs/NUMBERS_REGISTER.md`. Components: `src/deck/ui.tsx` (Module, Chip, Formula, Legend).

| Slide | Status | Feeds from | Left to do |
|---|---|---|---|
| 0 TITLE (Phase 1, SAARTHI26, team SANKAT MOCHAK, GEHU Dehradun) | done | ppt_work/analysis.txt (team names), numbers.json | — |
| 1 Problem + 14 patterns | done, whitespace-checked | docs/17, docs/18, numbers.json | storm name for the cyclone case (TBD) |
| 2 Architecture DFD | done | docs/02, docs/03 | — |
| 3 Physics | done | results/geo_*, results/glof, docs/04 | — |
| 4 Data + eval | done | docs/09b-09e, results/geo_large | vision results (pending) |
| 5 Fusion + RL | done | docs/07, docs/08, results/rl_env | C_miss 100/1000/5000 complete; CQL not deployed at any tested cost |
| 6 Differentiation | done | docs/17, docs/18 | — |
| 7 Proven / next | done | results/, BUG_STATUS | update when Kaggle results land |
| Speaker notes (Hinglish + 3 judge Q&A each) | done | `src/deck/notes.ts` | — |
QA done: 7 slides; no IoT hardware on slides; every number in the register; formula class chips + symbol keys; ladder chips; no "best/first/SOTA"
claims (no C4); safety statement on slide 7; screenshots inspected for clipping (fonts load from Google Fonts at present time).

**Deliverable B ("TRINETRA Explained", `docs/19_TRINETRA_EXPLAINED/`): DONE (first full pass, 2026-10-31 11:10 UTC):** CH00, CH01, CH02, CH03, CH05, CH06, CH07, CH08, CH09, CH11, CH12+13, APPENDIX. CH10 = docs/13 (spec only). Next pass: add Figma-style SVG exports of the diagrams; deepen CH05 per-model worked examples.

Recovered measurements: Geo-PINN spatial OOF AUC 0.716 / ECE 0.099 (`admitted=false`); RL C_miss 1000 and 5000 completed, with the physics rule beating CQL and the learned policy failing its LCB deployment gate. `trinetra/kaggle/recover_geo_runs.sh` reproduces the run; rebuilt event IDs/days/labels match and numeric differences are floating-point noise only. EO input/split/license rules are in `docs/EO_DATA_CONTRACTS.md`.
Old plan (kept for reference): Priority: CH11 master tables (from code/configs) → CH03
datasets → CH05 physics (start from docs/04) → CH06 derived formulas → CH08 fusion (docs/07, 08) → CH07 perception → CH01/02 → CH09 → CH12/13 (docs/17, 18) → CH10 → appendix.
docs/05 and docs/16 now point to CH06 and APPENDIX. `docs/09e_TPD_DATASHEET.md` is NOT FOUND (we have `09e_GEOHAZARD_DATASETS.md` + `09b`).
<!-- END -->
