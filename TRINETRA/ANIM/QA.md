# QA log
- Fusion maths in app.js reproduces the repo worked example exactly (fused 0.6335, U* 0.2465, RED) — node check.
- All 590 half-second frames of Story Mode render without errors (node); 10 scenes, 4:55 total.
- Every number on screen comes from window.ANIM_DATA; extractor reports 0 missing values; completeness 99 % REAL/CONFIG/PUBLIC.
- Screens checked at 1920×1080 for S0–S9 and Explore tabs; overlaps fixed (survey chips, gauge labels, S9 table, pipeline row).
- No IoT hardware shown; no identifiable people; synthetic placeholder labelled; life-safety statement in S9 and Explore.
- No banned superlatives; every comparison is category-level (docs/17) with claim-ladder chips; no C4 claim.
- Single HTML file makes no network requests (all scripts inlined; system fonts).
