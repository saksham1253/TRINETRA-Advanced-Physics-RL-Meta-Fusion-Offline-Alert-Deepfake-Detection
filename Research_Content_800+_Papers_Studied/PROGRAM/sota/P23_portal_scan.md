# PROGRAM/sota/P23_portal_scan.md — data-portal reachability scan (P23)

RESEARCH NOTES. Honest record of which data portals were reachable via `web_fetch` this phase and what each
hosts. `web_search` has NO API key (unused). Portal terms-of-use NOT verified (Rule 11 search leads). No
download tested.

## Portals checked
- NASA Earthdata (earthdata.nasa.gov): REACHED — rendered nav exposes the DAAC + tool map: Earthdata Search,
  Worldview, FIRMS (active fire), Vertex/ASF (Sentinel-1 SAR, InSAR), Giovanni, AppEEARS, LP DAAC + LAADS
  (MODIS/VIIRS), NSIDC, PO.DAAC, etc. Free Earthdata login. → routes to D122-D127, D141-D142, active-fire D125.
- NASA FIRMS (firms.modaps.eosdis.nasa.gov): the direct /active_fire/ URL failed once (fetch error); reachable
  via the Earthdata FIRMS tool page. Active-fire MOD14/VNP14 downloads + API.
- ISRO Bhuvan (bhuvan.nrsc.gov.in): REACHED but returns a JS "Loading…" shell → data layers NOT scrapable by
  web_fetch. **[UNVERIFIED — manual check needed]** for Indian EO/hazard layers (priority for an India pilot).
- Copernicus Data Space (dataspace.copernicus.eu), USGS EarthExplorer, NOAA, EPA AQS, Zenodo, HuggingFace,
  Kaggle, GitHub, CrisisNLP (crisisnlp.qcri.org): NOT re-fetched this phase (known public hosts, cited in the
  catalogue from the dataset papers); treated as [UNVERIFIED] links to confirm manually.

## Honest limits
- Government/geoportals are largely JS-driven → `web_fetch` returns shells, not catalogues. The catalogue's
  links therefore come mostly from the dataset PAPERS (abstract-level, source-reported), not from scraping the
  portals. Each must be opened + its license confirmed manually before use.
- Indian-specific portals (Bhuvan, MOSDAC, VEDAS, NRSC, IMD, CWC, GSI landslide inventories) could NOT be
  harvested here and are the top manual-verification backlog item for deployment.

Full dataset list: DATASETS_CATALOGUE.md (D113-D164).
