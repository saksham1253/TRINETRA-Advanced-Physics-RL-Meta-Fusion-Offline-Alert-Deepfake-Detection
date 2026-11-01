# TPD-0.1 datasheet

## Motivation

TRINETRA Prototype Dataset v0.1 is a curated index and conversion workflow for a hackathon-scale, leakage-aware evaluation pack. It is not a new field-collected dataset and not a full benchmark.

## Current composition

The materialized release contains 736 landslide case-control rows: 184 NASA Global Landslide Catalog events and 552 derived controls, with NASA POWER rainfall and Copernicus DEM terrain. Physics columns are derived by `data_adapters/build_geo.py`. The master index has 101 spatial groups.

GLOF and EO sources are registered but not included as sample rows until their raw files are attached and converted:

- HMAGLOFDB v4: aggregate physics report available; raw rows pending.
- Landslide4Sense: planned 512-patch, 14-channel subset.
- Sen1Floods11: planned 400-chip VV/VH subset with Bolivia held out.
- Hephaestus: planned 512-patch subset grouped by `frameID`.

## Provenance

Every materialized row is `SOURCE+DERIVED`: source location/date/rain/terrain plus derived controls and physics features. `synthetic=0` and `own_captured=0`. This does not mean every column is directly measured. Quality flags explicitly state `case_control`, `artificial_prevalence` and `soil_parameters_assumed`.

## Splits and leakage protection

The current table is evaluated by spatial-block out-of-fold CV using 0.1° cells, not random row splitting. The small 112-row experiment is not added again because it overlaps the larger pack. EO contracts require image-hash, event or `frameID` grouping and train-only normalization.

## Recommended uses

- Reproduce the landslide physics hindcast and Geo-PINN experiment.
- Demonstrate source-to-derived provenance and spatial evaluation.
- Exercise result collection, fusion interfaces and simulator parameterization.
- Build smoke-test EO packs after source attachment.

## Not recommended

- Estimating real-world landslide prevalence from the case-control labels.
- Claiming deployment readiness, field validation or nationwide performance.
- Claiming GLOF risk without lake geometry, routing, exposure and uncertainty.
- Treating Hephaestus as validated Himalayan InSAR displacement.
- Comparing subset metrics directly with full-benchmark SOTA results.

## Sources, licensing and distribution

Source IDs and links are in `docs/09b_dataset_links.csv`. The index records mixed-open licensing and requires source-term verification before redistribution. Raw imagery is not committed. Where redistribution is restricted, publish only manifests, mappings, converters and checksums.

## Maintenance

Version: `TPD-0.1`. Rebuild with `data_adapters/build_tpd_index.py`; profile with `profile_tables.py`. Any new source requires a verified registry entry, conversion reconciliation, leakage check, loader smoke test and provenance flags before its rows enter the index.

## Hinglish summary

TPD-0.1 ko “hamara collected field dataset” mat bolo. Ye public sources ko ek common, auditable format me jodta hai. Abhi sirf landslide table materialized hai. EO aur GLOF rows tab add honge jab asli files attach karke converter aur leakage checks pass honge.

<!-- END -->
