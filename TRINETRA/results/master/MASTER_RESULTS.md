# TRINETRA — MASTER RESULTS (all accounts merged)

Every number is OUR RESULT on the prototype pack (not comparable to full-benchmark papers). Admitted = beat climatology and logistic baselines on cost-weighted value with a 95% CI (Rule 16).

## Runs used (one phase per account)

- **B**: B final (7d27ec16_out_B_final.zip)
- **P**: repo results/ (geo, GLOF, RL env, Geo-PINN)

## Scorecard

| hazard | expert | metric | value | admitted / deploy | note |
|---|---|---|---|---|---|
| Fire / smoke (CCTV) | fire_cnn | - | not measured | - | not measured |
| Fire / smoke (CCTV) | colorhist | - | not measured | - | not measured |
| Fire / smoke (zero-shot) | zeroshot | ROC-AUC OOF / held-out | 0.889 / 0.999 | 0/1 | 1 seed(s) |
| Fire / smoke (few-shot CLIP) | clip_probe | - | not measured | - | not measured |
| Fake media | deepfake | - | not measured | - | not measured |
| Landslide (physics, zero training) | caine_ratio | ROC-AUC spatial OOF | 0.758 | physics (no gate needed) | 184 real events, 101 blocks |
| GLOF (lake area → volume) | glof_physics | exponent b (95% CI) | 1.13 (0.71-1.50) | fit | n 21 |
| RL alarm policy (C_miss 100) | cql_learned vs physics_rule | return CQL / rule / oracle | -22.5 / -22.8 / -22.9 | deploy False | LCB -0.30; SIMULATOR |
| RL alarm policy (C_miss 1000) | cql_learned vs physics_rule | return CQL / rule / oracle | -200.9 / -200.0 / -200.0 | deploy False | LCB -10.28; SIMULATOR |
| RL alarm policy (C_miss 5000) | cql_learned vs physics_rule | return CQL / rule / oracle | -486.8 / -478.1 / -478.5 | deploy False | LCB -31.93; SIMULATOR |
| Landslide (Geo-PINN) | geo_pinn | ROC-AUC OOF / held-out | 0.716 | 0/1 | 1 seed(s) |

## Headline

- Admitted learned experts: **0** (none yet).
- Landslide physics with zero training: ROC-AUC **0.758** (184 real events, 101 blocks).
- RL: built, trained and tested online in the physics simulator at every cost ratio; the physics rule is within noise of the oracle, so the gate kept the rule (C_miss 100: deploy False; C_miss 1000: deploy False; C_miss 5000: deploy False).

Full tables: `RESULTS.md` (same folder).
