# DATASETS_CATALOGUE.md — consolidated FREE/open dataset catalogue (Phase P23)

RESEARCH-ONLY. The dedicated dataset document requested by the user. Everything here is SOURCE-REPORTED (from
arXiv abstracts via a throttled reader, and from named data portals reachable by `web_fetch`). **No download
link was tested; licenses/costs are INDICATIVE until portal-verified (§0.9A); sizes marked "named" come from a
citing abstract, not the owning paper.** `web_search` has no API key and was not used. Nothing is downloaded,
built, or used. Rule 11: portal/agency names are search leads, verify terms-of-use before any use.

STATUS KEY: [D] = discovered candidate (default; not selected, not verified). None is marked "selected".
COST: free unless flagged. EULA = free-for-research but requires a signed agreement / access request.

Numbering continues the master `DATASETS.md` series; these are cross-linked there as D113+.

=============================================================================================================
## A. DATA PORTALS CHECKED (and how to reach them)
`web_fetch` reachability recorded honestly; portal terms NOT verified.
| Portal | Hosts | Reach via web_fetch | Access route |
|--------|-------|---------------------|--------------|
| NASA Earthdata (earthdata.nasa.gov) | MODIS/VIIRS fire, SAR, land/atmos | REACHED (nav + DAAC list rendered) | Earthdata Search; login (free) |
| NASA FIRMS (firms.modaps.eosdis.nasa.gov) | active-fire MOD14/VNP14, NRT | tool page via Earthdata; direct active_fire URL failed once | FIRMS downloads / API |
| ASF DAAC / Vertex (asf.alaska.edu) | Sentinel-1 SAR, InSAR | via Earthdata nav | Vertex; Earthdata login |
| LP DAAC / LAADS | MODIS/VIIRS products | via Earthdata nav | Earthdata login |
| Copernicus / ESA (dataspace.copernicus.eu) | Sentinel-1/2/3 | NOT re-fetched this phase (known public) | Copernicus Data Space (free account) |
| USGS EarthExplorer (earthexplorer.usgs.gov) | Landsat, DEM | NOT re-fetched (known public) | free account |
| ISRO Bhuvan (bhuvan.nrsc.gov.in) | Indian EO, hazards, LULC | REACHED but JS-only "Loading…" shell → **[UNVERIFIED — manual check]** | Bhuvan portal (login) |
| CrisisNLP (crisisnlp.qcri.org) | crisis tweets/images | known public | direct download |
| Zenodo / HuggingFace / Kaggle / GitHub | research datasets | known public hosts | direct |
NOTE: Bhuvan and other Indian-gov portals (MOSDAC, VEDAS, NRSC) are JS-driven and could not be scraped here;
they must be checked manually for the India-specific EO/hazard layers (flagged for the deployment backlog).

=============================================================================================================
## B. FIRE & SMOKE — image/video detection (CCTV / UAV / satellite)  [WS4, WS1]
| # | Dataset | Modality | Size (reported) | License/cost | Host (as reported) | Source |
|---|---------|----------|-----------------|--------------|--------------------|--------|
| D113 | FIgLib (Fire Ignition Library) | fixed-cam images | ~25,000 labeled | free (research) | HPWREN; github.com/aiel-ucsd | 2112.08598 |
| D114 | SKLFS-WildFire Test | real images | "largest real-world testset" | free (code+data) | github.com/WCUSTC/CCPE | 2311.10116 |
| D115 | GWFP (Global Wildfire Prevention) | images+video (NIR/ember/fog) | large, geo-diverse | open "upon acceptance" — **may not be live** | repo TBA | 2606.10174 |
| D116 | AusSmoke + MultiNatSmoke | images (segmentation) | "order-of-magnitude larger" | public | github.com/henryzhao0615/MultiNatSmoke | 2604.23542 |
| D117 | PYRONEAR-2025 | images+video | ~50k images, ~150k ann., 640 fires | free/public | Pyronear project | 2402.05349 |
| D118 | The Wildfire Dataset | high-res images | 10.74 GB | free (public) | public (Kaggle-style) | 2505.17395 |
| D119 | FASDD (Flame & Smoke Detection) | images (det) | large | free/open (reported) | public | named in 2501.08639 |
| D120 | D-Fire | images (bbox) | ~21k (named) | free/open | github.com/gaiasd/DFireDataset | named in 2501.08639 |
| D121 | AFSE (Aerial Fire & Smoke Essential) | aerial images | — | research dataset | — | 2501.08639 |
| D122 | USTC_SmokeRS | MODIS 3-band images | — | free (research) | public | 2310.01711 |
| D123 | Landsat_Smk | Landsat 5/8 6-band | — | free (research) | public | 2310.01711 |
| D124 | WildfireSpreadTS (WSTS) | multi-temporal datacubes | multi-year/fire | free/open | public repo | ref. 2603.09042 |

## C. SATELLITE ACTIVE-FIRE / BURNED AREA  [WS1b, WS8]
| # | Dataset | Modality | Size | License | Host | Source |
|---|---------|----------|------|---------|------|--------|
| D125 | MOD14 / VNP14 fire masks | MODIS+VIIRS fire raster | multi-region | free (NASA) | github.com/justuskarlsson/wildfire-mod14-vnp14; FIRMS | 2503.08580 |
| D126 | CaBuAr (California Burned Areas) | Sentinel-2 L2A pre/post | CA since 2015 | free/open | public (CAL FIRE ann.) | 2401.11519 |
| D127 | MultiEarth Amazon | Sentinel/Landsat/VIIRS/MODIS | curated | open | github.com/h2oai/cvpr-multiearth… | 2307.04916 |
| D128 | EFFIS hotspot crossref (Europe) | MODIS+VIIRS+Sentinel-3+LULC | large (Europe) | from public EFFIS/Copernicus | host TBA | 2308.02508 |

## D. FLOOD / INUNDATION  (SAR + optical)  [WS1b, WS8]
| # | Dataset | Modality | Size | License | Host | Source |
|---|---------|----------|------|---------|------|--------|
| D129 | Sen1Floods11 | Sentinel-1 SAR + labels | 11 events, global | free/open | github.com/cloudtostreet/Sen1Floods11 | ref. 2307.07123 |
| D130 | SEN12-FLOOD | S1 SAR + S2 optical | multi-event | free/open | public | 2307.07123 |
| D131 | C2S-MS Floods | SAR + multispectral | multimodal | free (reported) | public | 2601.00123 |
| D132 | GEOID-Flood | bi-temporal S1 (GRD+RTC)+S2+DEM | >14k tiles, 219 events, 65 countries | free/open (Copernicus EMS) | github.com/links-ads/geoid-flood | 2608.02315 |
| D133 | S1GFloods | Sentinel-1 SAR pairs | 46 events 2015-22 | free/open | github.com/Tamer-Saleh/S1GFlood-Detection | 2306.00704 |
| D134 | Kuro Siwo | SAR GRD+SLC multi-temporal | 43 events, 338B m² | free/open (NeurIPS D&B) | public (BlackBench) | 2311.12056 |
| D135 | Citizen-Science Flood Extent | Sentinel-1 C-band SAR | ~36,000 km² (US+BD) | free/open | public (competition) | 2311.09276 |

## E. LANDSLIDE  [WS1b]
| # | Dataset | Modality | Size | License | Host | Source |
|---|---------|----------|------|---------|------|--------|
| D136 | LMHLD | 5 sensors, 7 global areas | 25,365 patches | free/open | Zenodo 10.5281/zenodo.11424988 | 2502.19866 |
| D137 | Landslide4Sense | multispectral | benchmark | free/open | public | named in 2403.10127 |
| D138 | Bijie landslide | optical | benchmark | free (research) | public | named in 2403.10127 |
| D139 | PILD (event-isolated) | 4 sources, 55 events | 7,890 test | free/open | github.com/Liu-Zhihang/geophysadapter | 2608.09325 |
| D140 | MMLSv2 — **MARTIAN (out of Earth scope)** | 7-band (RGB/DEM/slope/thermal) | 664+276 | free/open | github.com/MAIN-Lab/MMLS_v2 | 2602.08112 |

## F. InSAR / GROUND DEFORMATION  [WS1b]
| # | Dataset | Modality | Size | License | Host | Source |
|---|---------|----------|------|---------|------|--------|
| D141 | Hephaestus | Sentinel-1 interferograms (ann.) | 19,919 ifg / 216,106 patches, 44 volcanoes | free/open | public (CVPR EarthVision) | 2204.09435 |
| D142 | Thalia | InSAR+topo+atmos datacubes | 38 datacubes, 7 yr | free/open | github.com/Orion-AI-Lab/Thalia | 2505.17782 |

## G. AIR QUALITY / PM2.5 / GAS  [WS7, WS8]
| # | Dataset | Modality | Size | License | Host | Source |
|---|---------|----------|------|---------|------|--------|
| D143 | KnowAir (PM2.5-GNN) | station TS + meteo | China, real-world | free/open | github.com/shawnwang-tech/PM2.5-GNN | 2002.12898 |
| D144 | TAP (Tracking Air Pollution China) | satellite+ground+model, 1-10km daily | since 2000, national | free/public | tapdata.org | 2103.06520, 2203.07591 |
| D145 | Bihar low-cost PM2.5 network | 511-loc sensor TS + meteo | 1 yr, India | reported public | host TBA | 2412.13935 |
| D146 | California Wildfire PM2.5 | hourly station TS | 12 yr, 1,375 incidents, 79 sites | from EPA AQS (public) | EPA AQS | 2607.07951 |

## H. SEISMIC / EARTHQUAKE  [WS8]
| # | Dataset | Modality | Size | License | Host | Source |
|---|---------|----------|------|---------|------|--------|
| D147 | CEED (California EQ Event) | waveforms+picks+polarity | 2000-2024 (NCEDC+SCEDC) | free/open | public | 2502.11500 |
| D148 | STEAD (Stanford EQ) | 3-comp waveforms | millions | free/open | public | named in 2408.06629 |
| D149 | POSEIDON | event catalog+energy | 2.8M events, 30 yr | free/open | huggingface.co/datasets/BorisKriuk/Poseidon | 2601.02264 |
| D150 | MultiSeismo | waveforms+intensity maps+meta | 16K+ events 2010-23 | free/open (reported) | public | 2605.26320 |

## I. CRISIS SOCIAL-MEDIA / MULTIMODAL DISASTER  [WS2, WS3]
| # | Dataset | Modality | Size | License | Host | Source |
|---|---------|----------|------|---------|------|--------|
| D151 | CrisisBench / CrisisNLP | tweets (text) | 166.1k+141.5k, 8 sets | free/open | crisisnlp.qcri.org | 2004.06774 |
| D152 | CrisisMMD | text+images | multi-disaster | free/open | crisisnlp.qcri.org | 1805.00713 |
| D153 | MEDIC | images (multi-task) | 71,198 | free/open | crisisnlp.qcri.org/medic | 2108.12828 |
| D154 | GeoCoV19 | geolocated tweets | 524M+, 90 days (tweet IDs) | free/open | crisisnlp.qcri.org | 2005.11177 |
| D155 | HumAID / HUMAID-NER | tweets (+NER) | 60,000 tweets, ~175k spans | free/open | public | 2609.16964 |
| D156 | TSEqD (Turkey-Syria EQ) | text+images+social | 10,352 (single event) | reported released | host TBA | 2410.08814 |
| D157 | DisasterVQA | images+Q/A | 1,395 img / 4,405 Q/A | free/open | Zenodo 10.5281/zenodo.18267769 | 2601.13839 |

## J. DEEPFAKE / SYNTHETIC MEDIA (forensic workstream)  [WS2]
| # | Dataset | Modality | Size | License | Host | Source |
|---|---------|----------|------|---------|------|--------|
| D158 | DFDC | face video | preview 5K (full larger) | **EULA — actor-likeness agreement** | deepfakedetectionchallenge.ai | 1910.08854 |
| D159 | FaceForensics++ | face video | large (standard) | **EULA — signed access request** | public (request form) | named in 2107.02045 |
| D160 | FakeAVCeleb | video+synth audio | multi-ethnicity | **access-on-request (likely restricted)** | public (request) | 2108.05080 |
| D161 | DeepFake MNIST+ | video | 10,000 vids, 10 actions | free (reported) | public | 2108.07949 |
| D162 | CtrSVDD | singing-voice audio | 47.64h bona + 260.34h fake, 164 singers | public | public | 2406.02438 |
| D163 | Codecfake | codec deepfake audio | 7 codec methods | free/open (reported) | public | 2406.08112 |
| D164 | AUDETER | deepfake audio (open-world) | 4,500+ h, 3M clips | free/open | GitHub (reported) | 2509.04345 |

=============================================================================================================
## K. HONEST CAVEATS & NEXT STEPS
- Download liveness NOT tested; licenses INDICATIVE; verify each portal's terms before use (§0.9A, Rule 11).
- `[D]` candidates only — none selected. Free-only rule holds for any future STATUS=selected.
- EULA/restricted: D158 DFDC, D159 FaceForensics++, D160 FakeAVCeleb — need signed agreements.
- "Upon acceptance"/host-TBA (D115 GWFP, D128 EFFIS, D145 Bihar, D156 TSEqD) may not be live — recheck.
- D140 MMLSv2 is MARTIAN → out of Earth early-warning scope; listed for completeness only.
- Sizes tagged "named" (D119/D120/D129/D137/D138/D148) come from a citing abstract — confirm with the owner.
- INDIA-SPECIFIC portals (Bhuvan, MOSDAC, VEDAS, NRSC, IMD, CWC, GSI landslide inventories) are JS-driven and
  must be checked MANUALLY — carried to the deployment backlog. These are the priority for an India pilot.
