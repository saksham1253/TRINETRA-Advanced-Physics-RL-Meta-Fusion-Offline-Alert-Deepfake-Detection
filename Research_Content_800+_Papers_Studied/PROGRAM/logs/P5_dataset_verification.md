# P5 DATASET VERIFICATION LOG — fetch verdicts (mirror of DATASETS.md "Ver" column)

Phase P5 · 2026-10-07. Verification was done by direct `web_fetch` of authoritative portals/Zenodo/
GitHub/arXiv (a delegated research subagent performed the fetches; `web_search` had no API key this
session, so DuckDuckGo HTML was used only for DISCOVERY, never as a source of truth). Hard-honesty
(§0.5): every UNVERIFIED fact is flagged; nothing was assumed.

LEGEND: [V] verified on direct authoritative fetch · [V*] exists, one fact unverified · [D] discovery-only.

| ID | Dataset | Verdict | Evidence fetched | UNVERIFIED flag |
|----|---------|---------|------------------|-----------------|
| D01 | Sentinel-1 | [V] | dataspace.copernicus.eu (HTTP 200), free/open wording | legal-notice PDF not fetchable |
| D02 | Sentinel-2 | [V] | CDSE + EuroSAT README corroboration | legal-notice PDF not fetchable |
| D03 | GPM IMERG | [V] | gpm.nasa.gov/data/imerg (200); V06/V07, Early/Late/Final | — |
| D04 | SMAP | [V] | nsidc.org/data/smap (200) | — |
| D05 | ERA5-Land | [V] | cds.climate.copernicus.eu dataset page; CC-BY + DOI 10.24381/cds.e2161bac | — |
| D06 | MODIS | [V] | earthdata.nasa.gov catalog, MOD13Q1 V061 | LP DAAC product page redirected |
| D07 | ITS_LIVE | [V] | its-live.jpl.nasa.gov (200) | — |
| D08 | NASA GLC/COOLR | [V*] | gpm.nasa.gov/applications/landslides/coolr (200) | event COUNT not on page (~11k unverified) |
| D09 | Landslide4Sense | [V*] | HuggingFace card (3799/245/800, 14-band) | IARAI site DEAD; LICENSE not stated |
| D10 | SSL4EO-S12 | [V] | github zhu-xlab README; 251,079 locs, Apache-2.0/CC-BY-4.0 | — |
| D11 | GLOFNet | [V*] | arXiv 2510.10546 (paper CC BY-NC-ND 4.0) | data download URL + data LICENSE unverified |
| D12 | Sen1Floods11 | [V*] | github cloudtostreet README; 11 events, GCS bucket | exact LICENSE + 4,831-chip count unverified |
| D13 | BigEarthNet v2 | [V] | bigearth.net (200); CDLA-Permissive-1.0; 549,488 | — |
| D14 | EuroSAT | [V] | github phelber README; MIT; 27,000/10/13-band | — |
| D15 | HMAGLOFDB | [D] | ESSD-2023 article + github fidelsteiner + ICIMOD RDS | 766-count + CC-BY-4.0 from secondary dashboard |
| D16 | CrisisMMD | [V*] | crisisnlp.qcri.org/crisismmd (200); 16,058/18,082 v2.0 | exact LICENSE (generic "Terms of use") |
| D17 | GEOID-Flood | [D] | arXiv 2608.02315 body + github links-ads/geoid-flood ref | repo LICENSE to confirm on fetch |
| D18 | LMHLD | [D] | arXiv 2502.19866 + Zenodo DOI 10.5281/zenodo.11424988 | per-source sub-licenses to confirm |
| D19 | UFO | [D] | arXiv 2604.23066 | repo LICENSE/PlanetScope terms to confirm |
| D20 | GDCLD | [D] | arXiv 2604.16663 | dataset LICENSE unverified |
| D21 | Thalia | [D] | arXiv 2505.17782 + github Orion-AI-Lab/Thalia ref | repo LICENSE to confirm |
| D22 | IFI-Impacts | [V] | zenodo.org/records/11275211; CC BY 4.0; IIT-Delhi+IMD | — |
| D23 | Kerala-2018 landslide | [D] | research.utwente.nl dataset page (DDG) | page not directly fetched; license/size unverified |
| D24 | Bhuvan/NRSC inventories | [D] | bhuvan-app1.nrsc.gov.in listing (DDG) | portal access + ISRO license unverified |
| D25 | INDOFLOODS | [D] | Zenodo 14584654 (DDG index) | page not directly fetched; license/size unverified |
| D26 | Landslide Ref Data DLR/GFZ | [V] | zenodo.org/records/15421843; CC BY 4.0; 6.2 GB | — |

HONEST SUMMARY: 13 of 26 fully [V]; 5 [V*] (exist, one fact open); 8 [D] (discovery-only). The
UNVERIFIED items are NOT selected as load-bearing without a confirming fetch (DATASETS.md keeps them
CANDIDATE). The India-specific set (D22 IFI [V], D15 HMAGLOFDB [D], D24 Bhuvan [D], D23/D25 [D]) is the
highest-value but also the least directly-fetched → P6/P7 should fetch the Bhuvan + Zenodo pages directly
before building. web_search unavailability is logged as an environment constraint, not a shortfall.
