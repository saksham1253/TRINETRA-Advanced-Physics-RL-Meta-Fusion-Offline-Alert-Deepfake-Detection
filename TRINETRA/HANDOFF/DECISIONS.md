# DECISIONS (hackathon v2 engine)
| ID | Date | Decision | Why |
|----|------|----------|-----|
| H-01 | 2026-10-31 | New docs go in `docs/` with the v2 prompt names; old docs (`docs/01_..25_*`) untouched | rule 5 no-overwrite; START_HERE maps both sets |
| H-02 | 2026-10-31 | Adapt DATA to code: `data_adapters/build_npz.py` emits the exact `.npz` contracts; zero edits to `trinetra/src` | rule 4 / section 9 decision tree (a) |
| H-03 | 2026-10-31 | `block` key carries a leakage-safe GROUP (video prefix or perceptual-hash cluster or IoT session) for image/sensor data | existing trainers split by `block` via `spatial_block_kfold`; reuse means no code change |
| H-04 | 2026-10-31 | Fire model gets still images as clips with T=1 | `FireSmokeNet` expects (N,T,C,H,W); temporal benefit only with real video (documented limitation) |
| H-05 | 2026-10-31 | Main fire set = D-Fire 4k subset; held-out = DeepFire; confusers = weather set | small, free, verified, different sources |
| H-06 | 2026-10-31 | Offline-RL logs from fused scores via epsilon-rule logging policy; reward costs from `configs/default.json` | repo has no simulator; WATCH costs are ASSUMPTION (flags) |
| H-07 | 2026-10-31 | Fusion default stays FM-1; PHARAOH only via flag experiment | code default; no results yet |
| H-08 | 2026-10-31 | **IoT = FUTURE WORK** (team decision). Hackathon scope = fire CNN + zero-shot + deepfake + fusion + RL + results/demo | 28 h left; show results from code |
| H-09 | 2026-10-31 | Minimal EDITS to existing trainers allowed (logged in CODE_CHANGE_LOG) because OOF/calibration/held-out were blockers for results | section 9 (c): no way to build fusion without OOF |
| H-10 | 2026-10-31 | Deepfake p_fake modulates media reliability (r' = r(1-p_fake)), not hazard probability | semantic bug B-10 |
| H-11 | 2026-10-31 | Offline RL deploys only if WIS gain vs RuleBaselinePolicy has bootstrap 95% LCB > 0 | bug B-02 |
| H-13 | 2026-10-31 | Benign flames (candle/lighter) and normal scenes are STRESS-only, never training negatives | a candle is a real flame; we measure false alarms, not teach "flame = no fire" |
| H-14 | 2026-10-31 | All deepfake sets resized to 32 px (CIFAKE native) | same resolution at train and test; artifacts at high res are lost (limitation) |
| H-15 | 2026-10-31 | Geohazard is BACK IN SCOPE (team): landslide physics on real data, GLOF relations, EO heads (S2/S1/InSAR), RL environment | team request; repo ws1b code exists |
| H-16 | 2026-10-31 | Landslide labels = NASA GLC events vs same-site control monsoon days (case-control); headline = ROC-AUC, not value score | artificial base rate |
| H-17 | 2026-10-31 | Unknown soil handled by back-analysis (FS_dry = 1.2) and the c'-free signal dFS | B-23/B-24 |
| H-18 | 2026-10-31 | RL environment = Iverson+FS physics + REAL POWER rain seasons; hazard slope fitted on real events, intercept from an assumed 30%/season failure rate; results labelled SIMULATOR | no field outcome data |
| H-19 | 2026-10-31 | Rain = NASA POWER now (no login); IMERG 0.1 deg is the upgrade once Earthdata login exists | 28 h time box |
| H-12 | 2026-10-31 | Report ROC-AUC, recall@FPR5%, ECE next to value score | value score ≈0 on balanced sets (B-13) |
| H-20 | 2026-10-31 | TPD-0.1 indexes only materialized samples; planned GLOF/EO sources get no placeholder rows | prevents invented sample IDs/counts and false conversion claims |
| H-21 | 2026-10-31 | Convert the team’s uploaded archives once, validate, then share NPZ artifacts privately across accounts | avoids four redundant extractions/conversions and preserves identical splits |
<!-- END -->
