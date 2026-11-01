# 09d — TPD-0.1 conversion report

## Materialized conversion

| check | result | evidence |
|---|---|---|
| input rows | 736 | `geo_large_geo_events_profile.json` |
| output index rows | 736 | `data_manifests/tpd_index.csv` |
| dropped rows | 0 | 736 = 736 + 0 |
| positives / controls | 184 / 552 | index labels |
| spatial groups | 101 | 0.1° grouping used by evaluation code |
| exact source-table duplicates | 0 | profile JSON |
| provenance | all `SOURCE+DERIVED`; synthetic=0; own-captured=0 | TPD index |
| deterministic rerun | PASS | two runs produced the same index SHA-256 |
| schema compile/load | PASS for CSV/index builders | local stdlib execution |
| Geo-PINN loader/run | PASS previously, 736 OOF rows | `results/geo_pinn/geo_pinn_s0_report.json` |

The index does not copy raw imagery or restricted data. Its `relative_uri` points to the source row and its hash covers the canonical source-row values.

## Leakage and interpretation checks

- Evaluation split is recorded as `spatial_cv_oof`; no random row split is claimed.
- The 101 blocks match `geo_physics_hindcast.py --cell-deg 0.1`.
- Controls share source sites but use other monsoon dates. They are DERIVED and the positive fraction is artificial.
- Normalization and model evaluation are handled inside the existing spatial-CV pipeline.
- The 112-row small tile is excluded from the master index because it overlaps the large experiment and would double-count samples.

## Partial / blocked components

| component | state | blocker |
|---|---|---|
| HMAGLOFDB sample index | PARTIAL | aggregate report exists; raw CSV is not committed |
| L4S / Sentinel-2 | PLANNED | source data must be attached; default cap 512 |
| Sen1Floods11 / Sentinel-1 | PLANNED | source data must be attached; default cap 400 |
| Hephaestus InSAR | PLANNED | images + annotations must be attached; default cap 512 |

No EO metric is reported. No GLOF risk, validated InSAR displacement or field performance is claimed.

Reproduce:

```bash
python data_adapters/build_tpd_index.py
sha256sum -c data_manifests/tpd_index.csv.sha256
```

<!-- END -->
