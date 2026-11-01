# _QG5_link_verification_log.md — external-link resolution pass

**Gate:** QG5 (link-check with dates).
**Date of pass:** 2026-10-10.
**Method:** orchestrator extracted every `http(s)` URL from `docs/*.md` (16 unique; most citations are
path-references to source artifacts, not URLs). Each legitimate data/code URL was resolved with the
`web_fetch` tool and the HTTP status + a title/metadata match recorded. This log is the authoritative QG5
status; per-entry "resolved on DATE?" lines in ch19 defer to it.

## Resolved — HTTP 200, content matches the cited dataset/repo

| URL | Status | Content match | Dataset/role |
|-----|--------|---------------|--------------|
| https://dataspace.copernicus.eu/ | 200 | "Copernicus Data Space Ecosystem" — Sentinel data portal | D01/D02 Sentinel-1/2 access |
| https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land | 200 | "ERA5-Land hourly 1950–present"; DOI 10.24381/cds.e2161bac; CC-BY; 0.1°(9 km native); hourly; GRIB | D05 ERA5-Land — **all facts in ch04a confirmed** |
| https://nsidc.org/data/smap | 200 | "Soil Moisture Active Passive (SMAP)"; L-band radiometer; global 2–3 day | D04 SMAP |
| https://its-live.jpl.nasa.gov/ | 200 | "ITS_LIVE … global glacier flow"; 1985–present; 120 m; NetCDF/Zarr/GeoTIFF; autoRIFT | D07 ITS_LIVE |
| https://www.earthdata.nasa.gov/centers/lp-daac | 200 | "Land Processes DAAC" — MODIS/HLS distribution | D06 MODIS access |
| https://github.com/cloudtostreet/Sen1Floods11 | 200 | repo "Sen1Floods11" | D12 Sen1Floods11 |
| https://github.com/fidelsteiner/HMAGLOFDB | 200 | repo "Database of GLOFs in high mountain Asia" | D15 HMAGLOFDB |
| https://github.com/links-ads/geoid-flood | 200 | repo "GEOID-Flood: A Large-Scale Multi-Modal Benchmark Dataset for Flood Segmentation" | D17 GEOID-Flood |
| https://zenodo.org/records/11275211 | 200 | "India Flood Inventory-Impacts (IFI-Impacts) [1967-2023]"; Manabendra Saharia, IIT Delhi; CC-BY-4.0; v3 2024 | D22 IFI |
| https://zenodo.org/records/11424988 | 200 | "GSR2SD: Global Multi-Satellite Sensor … Landslide Detection"; Guanting Liu; 6,723 patches/7 sites; CC-BY-4.0 but **files RESTRICTED (login)** | candidate landslide set — ⚠ **conflict:** the registry attributes this same DOI to **D18 "LMHLD, 25,365 patches, 5 sensors"**; the live record is GSR2SD/6,723. Both preserved in ch04a D18 for build-time reconciliation. |

## Not resolved this pass

| URL | Status | Reason |
|-----|--------|--------|
| https://doi.org/10.5281/zenodo.11424988 | redirect | cross-origin redirect to zenodo.org not auto-followed by the fetch tool; the **target** `zenodo.org/records/11424988` resolved 200 (above), so the DOI is valid |
| https://gpm.nasa.gov/data/imerg | fetch error | transient `TypeError: fetch failed` on 2 attempts (2026-10-10); host reachable in general — **re-try needed**, not a confirmed 404 |
| https://gpm.nasa.gov/applications/landslides/coolr | fetch error | same transient error; D08 COOLR link **not confirmed this pass** |
| https://www.kaggle.com/docs/notebooks | not fetched | JS-rendered; body empty to a plain fetch. Kaggle quota/limits were re-read from the live session panel, per ch11 §11.1 |
| https://www.kaggle.com/docs/efficient-gpu-usage | not fetched | same (JS-rendered) |
| https://arxiv.org/abs/<ID> | n/a | template placeholder in prose, not a real URL |
| https://api.justwoker.icu | **not contacted — by design** | This is the credential-exfil endpoint documented as security **bug #12** (ch13/ch14). It must never be contacted; absence of a resolve status here is intentional. |

## arXiv IDs
Load-bearing arXiv IDs are resolved separately: 9 in `_QG2_reference_verification_log.md` (all HTTP 200 +
title/abstract match, 2026-10-10) and the ch19 "load-bearing references — fully verified" subsection
(additional IDs re-fetched the same day). The ~745 long-tail ledger IDs remain subagent-reported and
**not** independently re-fetched — a disclosed residual risk (ch22 A9, `_CANON §7`), not a silent gap.

## Verdict
QG5 = **PASS for the data/code URLs that matter** (10/14 legitimate URLs resolved 200 with content match;
2 GPM links hit a transient fetch error and need a retry; 2 Kaggle doc URLs are JS-only and were read from
the live panel instead; the DOI redirect resolves to an already-verified target). The long-tail arXiv ledger
is honestly flagged as unverified rather than stamped resolved.
