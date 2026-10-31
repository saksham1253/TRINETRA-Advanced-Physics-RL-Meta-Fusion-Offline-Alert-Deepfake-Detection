# LEAD_TIME_ITEMS — things to start EARLY (MASTER_PROMPT §0.9A, §0.10)
# Items with real-world lead time (access requests, registrations, procurement) that YOU
# must action yourself. Each: what, why early, exact steps for you, blocking which phase.

## Dataset access (verify + request in P5; some gated)
| ID | Item | Why early | Steps for you | Blocks |
|----|------|-----------|---------------|--------|
| LT-01 | NASA Earthdata login (GPM IMERG, SMAP, MODIS, FIRMS, GIBS) | registration-gated | create Earthdata account; accept EULAs per product | P5 build-data |
| LT-02 | Copernicus/ESA account (Sentinel-1/-2) | registration-gated | register Copernicus Data Space; API token | P5 |
| LT-03 | ISRO Bhuvan / NRSC products | govt portal, terms vary | verify terms per product; some need institutional request | P5/P19 |
| LT-04 | HMAGLOFDB (589 GLOF outbursts) access | via paper 2608.12422 | locate the public DB link + license | P5 (GLOF) |
| LT-05 | ERA5-Land (CDS) | registration + API | register Climate Data Store; accept license; CDS API key | P5 |

## Procurement (research now, buy later — RESEARCH-ONLY this program)
| ID | Item | Why early | Steps for you | Blocks |
|----|------|-----------|---------------|--------|
| LT-06 | Reachable Indian supplier listings for BOM | pages 403 this session | optionally supply URLs/snapshots from Robu/Robocraze/Element14-IN so prices can be [LV] | P6 BOM gate |
| LT-07 | LoRa band compliance confirmation (IN865–867) | legal before any node | confirm India ISM band + duty cycle with a regulatory source | P6/P13 |

## Expert / institutional review (flag; not actionable by the agent)
| ID | Item | Why early | Steps for you | Blocks |
|----|------|-----------|---------------|--------|
| LT-08 | NDMA/SDMA integration contact (SACHET/CAP) | long institutional lead | identify disaster-management authority contact | P12/P19 |
| LT-09 | Geotech / hydrology expert reviewer | validate physics (CLASS labels) | line up an expert for P7 derivation review | P7/P19 |
| LT-10 | Legal/privacy reviewer (data, CCTV) | compliance | identify reviewer for deployment notes | P19 |

Note: the agent will NOT perform any of these actions (research-only). They are surfaced
here and in gate messages so you can start them in parallel with the phases.
