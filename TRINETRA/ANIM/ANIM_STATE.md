# ANIM_STATE (update after every milestone)

| scene | status | repo files feeding it | known issues |
|---|---|---|---|
| S0 cold open | done | none | Devanagari not used (offline fonts) |
| S1 surveys + 14 patterns | done | docs/26 (surveys), docs/17 | survey values are PUBLIC REPORT; conf B items need verification |
| S2 data journey | done | docs/09b, data_manifests/tpd_index.csv, docs/09d, results/zeroshot_final | dataset cube sizes are log-scaled |
| S3 steam / S4 fire / S5 fake | done | configs/*.json, adapters.py caps, nf.py, decision.py, established_ef.py, cap.py | inputs SIMULATED (no cached per-frame outputs in repo) |
| S6 fusion | done | worked example (docs/07, numbers.json), zeroshot OOF reliability | correlated-expert handling (GLS) only mentioned |
| S7 physics | done | ws1b_geophys/*.py, geo_events.csv, geo_physics report | regime meter is rule-of-thumb |
| S8 cyclone | done (PLANNED) | docs/13 | spec only |
| S9 proof | done | results/* | fire CNN / media / EO / meta-fusion pending |
| Explore (9 tabs) | done | all of the above | Fusion Lab is a toy case (WORKED EXAMPLE) |
| Exports | single HTML · teaser MP4 (30 fps) · full 4:55 MP4 (15 fps) · in-page video player | tools/record.mjs | 30/60 fps: --fps 30 / 60 |
