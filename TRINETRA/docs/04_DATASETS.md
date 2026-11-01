# 04 — DATASETS (index): every dataset, its status, and how to trust it

This is the **index** to the TRINETRA (HIMKAVACH) dataset registry. The one place where **all 164 dataset
IDs appear** is the master table in §4. The long per-dataset content lives in the companion file
[04a_DATASETS.md](<04a_DATASETS.md>): 16-field **deep entries for the 13 STATUS=selected datasets**, then the
whole **candidate pool** as compact tables grouped by modality.

Ground-truth sources for this chapter (`_CANON.md §9`): [`DATASETS.md`](<../DATASETS.md>) (registry
D01–D112) and [`DATASETS_CATALOGUE.md`](<../DATASETS_CATALOGUE.md>) (candidate pool D113–D164).

---

## 1. Honesty box — read before using any row

> **NONE acquired.** No dataset has been downloaded in this program (links / metadata / plans only).
> This matches `_CANON.md`: *"No model has been trained and no dataset has been downloaded."*
> - **No EDA, no statistics.** Every size / `N` below is **as recorded in the registry**, not measured by
>   us. Many are flagged UNVERIFIED or "named" (taken from a citing abstract, not the owning paper's page).
> - **Licenses are as-recorded and mostly UNVERIFIED.** "the source records X" is **not** a verified fact.
>   We reproduce the registry's own tags honestly; we did not re-adjudicate them.
> - **Everything is a candidate until the license is verified** at the owning portal. Only 13 datasets are
>   marked `STATUS=selected`, and even those carry open license/count confirmations (several are `[V*]`/`[D]`).
> - Honesty labels (`_CANON.md §1`): `[CONFIRMED]` only for existence we verified; the registry's dataset
>   facts here are at best `[LIKELY]`/`[UNVERIFIED]` pending a portal fetch. No dataset performance number
>   is a TRINETRA measurement.

---

## 2. How to read the registry — STATUS and the verification legend

**STATUS values** (set by the free-only policy, `_CANON.md §5` constraint **C4**):
- **selected** — free (or free-with-registration), existence-verified, and chosen for the build. 13 total.
  Free-only rule: a dataset may be `selected` **only** if it is free; UNCLEAR-cost sets stay candidate.
- **candidate** — discovered and plausibly usable, but **not** adopted: license unverified, cost unclear,
  out-of-region, or domain-shifted. 151 total (every D27–D164, plus the unselected D09–D26).
- **rejected-paid** — a paid dataset excluded by the free-only rule. **0 in the registry**: no paid dataset
  was carried far enough to be formally rejected; cost-restricted government feeds (IMD D47, CWC D53) are
  recorded as `candidate` with cost "varies / often restricted", not as `rejected-paid`.

**Verification legend** (reproduced verbatim from `DATASETS.md`):
- **`[V]`** — verified on a direct authoritative fetch this phase (portal / Zenodo / GitHub / arXiv).
- **`[V*]`** — existence verified, but **one** stated fact (a count or the exact license) is UNVERIFIED,
  flagged inline.
- **`[D]`** — discovery-only: the authoritative page was **not** directly fetched; corroborated only by a
  secondary source. Most of the catalogue (D27–D164) is `[D]`.

---

## 3. Counts

| STATUS | Count | IDs |
|--------|-------|-----|
| **selected** | **13** | D01–D08, D12, D15, D17, D18, D22 |
| **candidate** | **151** | all others (D09–D11, D13, D14, D16, D19–D21, D23–D26, D27–D164) |
| **rejected-paid** | **0** | — (free-only rule held; no paid set formally carried to rejection) |
| **TOTAL** | **164** | D01–D164 |

By verification tag among the 164: `[V]` and `[V*]` apply mostly to D01–D26; the overwhelming majority
(D27–D164) are `[D]` discovery-only. The 13 selected split as: 9×`[V]`/`[V*]` (D01–D08, D12, D22) and
4×`[D]` (D15, D17, D18 — plus D08 is `[V*]`). *(Selected `[D]` sets D15/D17/D18 still carry open license/
count confirmations — see 04a.)*

---

## 4. COMPLETE MASTER TABLE — all 164 IDs

Compact columns only. `COST`: free / free-reg (free-with-registration) / varies / unclear.
`License-status` is **as-recorded** (UNVERIFIED unless a named license is shown). ↔ marks a duplicate
listing of the same underlying dataset under another ID. Deep/compact detail: [04a](<04a_DATASETS.md>).

| ID | Name | WS | Modality | COST | License-status | STATUS | Ver |
|----|------|----|----------|------|----------------|--------|-----|
| D01 | Sentinel-1 SAR | WS1/WS8 | C-band SAR | free-reg | Copernicus open | selected | [V] |
| D02 | Sentinel-2 MSI | WS4/WS8 | optical multispectral | free-reg | Copernicus open | selected | [V] |
| D03 | GPM IMERG | WS1/WS3 | precipitation | free-reg | NASA open | selected | [V] |
| D04 | SMAP soil moisture | WS1 | soil moisture | free-reg | NASA open | selected | [V] |
| D05 | ERA5-Land | WS1 | reanalysis | free-reg | CC-BY | selected | [V] |
| D06 | MODIS | WS8 | optical/LST/NDVI | free-reg | NASA open | selected | [V] |
| D07 | ITS_LIVE glacier velocity | WS8 | ice velocity | free/reg | NASA open (MEaSUREs) | selected | [V] |
| D08 | NASA GLC / COOLR | WS1/WS8 | landslide points | free | NASA open | selected | [V*] |
| D09 | Landslide4Sense | WS1/WS8 | multispectral patches | free | UNVERIFIED (no card license) | candidate | [V*] |
| D10 | SSL4EO-S12 | WS1/WS8 | S1+S2 SSL corpus | free | data CC-BY-4.0 | candidate | [V] |
| D11 | GLOFNet | WS8 | multimodal GLOF | unclear | UNVERIFIED (download+license) | candidate | [V*] |
| D12 | Sen1Floods11 | WS1/WS8 | SAR+optical flood | free | UNVERIFIED | selected | [V*] |
| D13 | BigEarthNet v2 (reBEN) | WS4/WS8 | S1+S2 patches | free | CDLA-Permissive-1.0 | candidate | [V] |
| D14 | EuroSAT | WS4 | multispectral | free | MIT | candidate | [V] |
| D15 | HMAGLOFDB | WS8 | GLOF inventory | free | CC-BY-4.0 (confirm) | selected | [D] |
| D16 | CrisisMMD / CrisisNLP | WS2/WS3 | text+images | free | UNVERIFIED ("Terms of use") | candidate | [V*] |
| D17 | GEOID-Flood | WS1/WS8 | S1+S2+DEM flood | free | per repo (verify) | selected | [D] |
| D18 | LMHLD | WS1/WS8 | landslide patches | free | open Zenodo (verify) | selected | [D] |
| D19 | UFO Urban Flood | WS1/WS4 | PlanetScope flood | free-reg | per paper (verify) | candidate | [D] |
| D20 | GDCLD (coseismic) | WS1 | coseismic LS seg | unclear | UNVERIFIED | candidate | [D] |
| D21 | Thalia ↔D142 | WS1/WS8 | InSAR datacubes | free | per repo (verify) | candidate | [D] |
| D22 | India Flood Inventory–Impacts | WS1/WS3 | flood event CSV | free | CC-BY-4.0 | selected | [V] |
| D23 | Kerala-2018 LS inventory | WS1 | landslide polygons | unclear | UNVERIFIED | candidate | [D] |
| D24 | Bhuvan/NRSC-ISRO inventories | WS1/WS8 | landslide polygons | free-reg (likely) | UNVERIFIED (ISRO) | candidate | [D] |
| D25 | INDOFLOODS | WS1/WS3 | station discharge | free (likely) | UNVERIFIED | candidate | [D] |
| D26 | Landslide Ref S1&S2 (DLR/GFZ) | WS1 | S1+S2 landslide | free | CC-BY-4.0 | candidate | [V] |
| D27 | Multi-Category Visual Smoke DB | WS7a/WS4 | smoke images | free (likely) | UNVERIFIED | candidate | [D] |
| D28 | UCI Gas Sensor Array Drift | WS7a | MOX e-nose TS | free | CC-BY-4.0 (confirm) | candidate | [D] |
| D29 | Low-Cost Indoor AQ Calibration | WS7a | AQ sensor TS | free (likely) | UNVERIFIED | candidate | [D] |
| D30 | RESPIRE India CO | WS7a | CO calibration | free (likely) | UNVERIFIED | candidate | [D] |
| D31 | NIST FDS Validation suite | WS1a | fire experiment data | free | US-Gov PD / BSD | candidate | [D] |
| D32 | NIST Fire Calorimetry DB | WS1a | HRR curves | free | US-Gov PD | candidate | [D] |
| D33 | NIFC/GeoMAC fire perimeters | WS1a | fire perimeters | free (likely) | US public (confirm) | candidate | [D] |
| D34 | WRF-SFIRE/SPARK sims | WS1a | fire-spread sims | free (likely) | UNVERIFIED | candidate | [D] |
| D35 | FIgLib ↔D113 | WS4 | fixed-cam smoke images | free | public (not confirmed) | candidate | [D] |
| D36 | PYRONEAR-2025 ↔D117 | WS4 | camera-net img+video | free | open-source (confirm) | candidate | [D] |
| D37 | D-Fire ↔D120 | WS4 | fire+smoke images | free | MIT (not confirmed) | candidate | [D] |
| D38 | Multi-Scene FSD | WS4 | fire/smoke images | free | not stated | candidate | [D] |
| D39 | AusSmoke/MultiNatSmoke ↔D116 | WS4 | smoke segmentation | free | not stated | candidate | [D] |
| D40 | SmokeBench | WS4 | surveillance imagery | free | not stated | candidate | [D] |
| D41 | GWFP ↔D115 | WS4 | image+video | free | "open-source" | candidate | [D] |
| D42 | FLAME | WS4 | aerial RGB+thermal | free | IEEE DataPort terms | candidate | [D] |
| D43 | WIT-UAS | WS4 | IR thermal | free | not visible | candidate | [D] |
| D44 | Fire360 | WS4 | 360° fire video | free | not visible | candidate | [D] |
| D45 | NASA GLC/COOLR ↔D08 | WS1b | landslide inventory | free | NASA open (indic.) | candidate | [D] |
| D46 | GSI Landslide / BHUKOSH | WS1b | India LS inventory | free | GSI/Govt-India | candidate | [D] |
| D47 | IMD rainfall / gridded | WS1b | rainfall | varies | IMD policy (often paid) | candidate | [D] |
| D48 | NASA GPM IMERG | WS1b | precipitation | free | NASA open | candidate | [D] |
| D49 | CHIRPS rainfall | WS1b | rainfall | free | public domain | candidate | [D] |
| D50 | SRTM DEM | WS1b | DEM | free | public domain (USGS) | candidate | [D] |
| D51 | ALOS AW3D30 / GLO-30 DEM | WS1b | DEM | free | attribution (JAXA/Cop.) | candidate | [D] |
| D52 | ICIMOD HKH glacial-lake/GLOF | WS1b | glacial lake/GLOF | free | ICIMOD open (indic.) | candidate | [D] |
| D53 | CWC / India-WRIS | WS1b | discharge/stage | varies | Govt-India (restricted) | candidate | [D] |
| D54 | UNSODA soil hydraulic DB | WS1b | soil hydraulics | free | public domain | candidate | [D] |
| D55 | UCF-Crime | WS8 | surveillance VAD video | free | not visible | candidate | [D] |
| D56 | XD-Violence | WS8 | multimodal VAD | free | not visible | candidate | [D] |
| D57 | ShanghaiTech/Avenue/Ped | WS8 | VAD video | free | not visible | candidate | [D] |
| D58 | SMD (Server Machine) | WS8 | multivariate TS | free | not visible | candidate | [D] |
| D59 | NASA SMAP / MSL | WS8 | telemetry TS | free | US-gov public (indic.) | candidate | [D] |
| D60 | NAB (Numenta) | WS8 | streaming TS | free | AGPL-3.0 (confirm) | candidate | [D] |
| D61 | UCR Anomaly Archive | WS8 | TS | free | not visible | candidate | [D] |
| D62 | TSB-AD / TSB-drift | WS8 | TS bench | free | not visible | candidate | [D] |
| D63 | SWaT / WADI / BATADAL | WS8 | CPS TS | free (request) | iTrust request EULA | candidate | [D] |
| D64 | PSM | WS8 | server metrics TS | free | not visible | candidate | [D] |
| D65 | TinyMLperf (anomaly) | WS8 | MCU anomaly | free | Apache-2.0 (indic.) | candidate | [D] |
| D66 | UrbanSound8K | WS8 | acoustic | free | CC-BY-NC 3.0 (indic.) | candidate | [D] |
| D67 | OddBench | WS8 | tabular outlier | free | not visible | candidate | [D] |
| D68 | FaceForensics++ ↔D159 | WS2 | face-manip video | free (EULA) | research-only EULA | candidate | [D] |
| D69 | Celeb-DF (v2) | WS2 | face-swap video | free (EULA) | research-only EULA | candidate | [D] |
| D70 | DFDC ↔D158 | WS2 | face video | free (EULA) | DFDC EULA | candidate | [D] |
| D71 | WildDeepfake | WS2 | deepfake video | free (request) | research-only | candidate | [D] |
| D72 | DF40 | WS2 | forgery methods | free (request) | research-only | candidate | [D] |
| D73 | GenImage | WS2 | real-vs-AI image | free | not visible | candidate | [D] |
| D74 | DiffusionForensics | WS2 | diffusion image | free | not visible | candidate | [D] |
| D75 | ASVspoof | WS2 | spoof speech | free | ODC/research (indic.) | candidate | [D] |
| D76 | NewsCLIPpings | WS2 | OOC multimodal | free | research (indic.) | candidate | [D] |
| D77 | CCDF (surveillance deepfake) ⚑ | WS2 | video | free | not stated | candidate | [D] |
| D78 | DF26 | WS2 | T2V/I2V video | free | not stated | candidate | [D] |
| D79 | BabelFake | WS2 | AV clips | free (consent) | ethically-sourced | candidate | [D] |
| D80 | PhysForensics-Bench | WS2 | audio-video | free | not stated | candidate | [D] |
| D81 | MAD benchmark | WS2 | motion deepfake | free | not stated | candidate | [D] |
| D82 | MIC-Bench | WS2 | image-claim OOC | free | released (indic.) | candidate | [D] |
| D83 | NepOOC | WS2 | Nepali-English OOC | free | public (indic.) | candidate | [D] |
| D84 | WildFakeBench | WS2 | micro-video | free | released (indic.) | candidate | [D] |
| D85 | Weibo26 | WS2 | image+text news | free | not stated | candidate | [D] |
| D86 | SLED-1400 | WS2 | evidence photos | free | study dataset (indic.) | candidate | [D] |
| D87 | Audio Neural Codec-Spoof | WS2 | audio | free | not stated | candidate | [D] |
| D88 | Soft-Bindings C2PA | WS2 | watermark bench | free | open-licence (audited) | candidate | [D] |
| D89 | ns-3 LoRaWAN reference | WS3 | sim configs | free | GPLv2 (indic.) | candidate | [D] |
| D90 | FAST-LoRa | WS3 | model/code | free | not stated | candidate | [D] |
| D91 | Meshtastic link-budget | WS3 | RF measurements | free | not stated | candidate | [D] |
| D92 | Meshtastic campus RSSI/SNR | WS3 | RF field logs | free | not stated | candidate | [D] |
| D93 | CRAWDAD traces | WS3 | wireless/mobility traces | free (request) | per-dataset EULA | candidate | [D] |
| D94 | CAP alert feed archives | WS3 | CAP messages | free | per-source (gov) | candidate | [D] |
| D95 | AQ-SDR ↔D106 | WS7b | AQ sensor TS | free | not stated | candidate | [D] |
| D96 | SensEURCity (Antwerp) | WS7b | AQ sensor TS | free | not stated (public) | candidate | [D] |
| D97 | SEA-HAZEMON | WS7b | haze node data | free? | not visible | candidate | [D] |
| D98 | LoRa 2.4 GHz ToF ranging | WS7b | ranging + T/RH | free | not stated | candidate | [D] |
| D99 | WildFireCan-MMD | WS4-ZS | X posts img+text | free? | not visible | candidate | [D] |
| D100 | AI4Fire | WS4-ZS | wildfire tasks | free? | not visible | candidate | [D] |
| D101 | California Wildfire PM2.5 | WS4-ZS | PM2.5 TS | free? | not visible | candidate | [D] |
| D102 | PyroStack US wildfire | WS5 | multi-band fire TS | free? | not stated | candidate | [D] |
| D103 | FireGen Monte-Carlo sim | WS5 | fire-spread sim | free? | not stated | candidate | [D] |
| D104 | Ctrl-CWM crowd world-model | WS5 | crowd sim | free? | not stated | candidate | [D] |
| D105 | cinemere/evacuation | WS5 | evacuation env | free | not stated (open) | candidate | [D] |
| D106 | AQ-SDR drift ↔D95 | WS7 | AQ sensor TS | free? | not stated | candidate | [D] |
| D107 | ECA9 industrial-accident video | WS4 | accident video | free? | not stated | candidate | [D] |
| D108 | Uttarakhand forest-fire imagery | DEPLOY/WS4 | India fire imagery | free? | not stated | candidate | [D] |
| D109 | WFDroneBench | DEPLOY/WS4 | risk maps/scenarios | free? | not stated | candidate | [D] |
| D110 | TRAQID + PM25Vision | DEPLOY/WS7 | regional AQI | free? | not stated | candidate | [D] |
| D111 | UrduFake@FIRE2020 | DEPLOY/WS2 | Urdu fake-news text | free? | shared-task terms | candidate | [D] |
| D112 | GeoCoV19 | DEPLOY/WS2 | geolocated tweets | free? | platform ToS (ID-only) | candidate | [D] |
| D113 | FIgLib ↔D35 | WS4 | fixed-cam images | free | free (research) | candidate | [D] |
| D114 | SKLFS-WildFire Test | WS4 | real images | free | free (code+data) | candidate | [D] |
| D115 | GWFP ↔D41 | WS4 | image+video | unclear | open "upon acceptance" | candidate | [D] |
| D116 | AusSmoke/MultiNatSmoke ↔D39 | WS4 | smoke segmentation | free | public | candidate | [D] |
| D117 | PYRONEAR-2025 ↔D36 | WS4 | image+video | free | free/public | candidate | [D] |
| D118 | The Wildfire Dataset | WS4 | hi-res images | free | free (public) | candidate | [D] |
| D119 | FASDD | WS4 | detection images | free | free/open (reported) | candidate | [D] |
| D120 | D-Fire ↔D37 | WS4 | bbox images | free | free/open | candidate | [D] |
| D121 | AFSE | WS4 | aerial images | free | research dataset | candidate | [D] |
| D122 | USTC_SmokeRS | WS4 | MODIS 3-band | free | free (research) | candidate | [D] |
| D123 | Landsat_Smk | WS4 | Landsat 6-band | free | free (research) | candidate | [D] |
| D124 | WildfireSpreadTS | WS1/WS8 | multi-temporal datacubes | free | free/open | candidate | [D] |
| D125 | MOD14 / VNP14 fire masks | WS1b/WS8 | fire raster | free | free (NASA) | candidate | [D] |
| D126 | CaBuAr (CA Burned Areas) | WS1b/WS8 | S2 pre/post | free | free/open | candidate | [D] |
| D127 | MultiEarth Amazon | WS1b/WS8 | multi-satellite | free | open | candidate | [D] |
| D128 | EFFIS hotspot crossref | WS1b/WS8 | multi-satellite | free | public EFFIS/Copernicus | candidate | [D] |
| D129 | Sen1Floods11 ↔D12 | WS1b/WS8 | S1 SAR+labels | free | free/open | candidate | [D] |
| D130 | SEN12-FLOOD | WS1b/WS8 | S1+S2 | free | free/open | candidate | [D] |
| D131 | C2S-MS Floods | WS1b/WS8 | SAR+multispectral | free | free (reported) | candidate | [D] |
| D132 | GEOID-Flood ↔D17 | WS1b/WS8 | S1+S2+DEM | free | free/open (Copernicus EMS) | candidate | [D] |
| D133 | S1GFloods | WS1b/WS8 | S1 SAR pairs | free | free/open | candidate | [D] |
| D134 | Kuro Siwo | WS1b/WS8 | SAR GRD+SLC | free | free/open (NeurIPS D&B) | candidate | [D] |
| D135 | Citizen-Science Flood Extent | WS1b/WS8 | S1 C-band SAR | free | free/open | candidate | [D] |
| D136 | LMHLD ↔D18 | WS1b | 5-sensor | free | free/open | candidate | [D] |
| D137 | Landslide4Sense ↔D09 | WS1b | multispectral | free | free/open | candidate | [D] |
| D138 | Bijie landslide | WS1b | optical | free | free (research) | candidate | [D] |
| D139 | PILD (event-isolated) | WS1b | 4-source | free | free/open | candidate | [D] |
| D140 | MMLSv2 — MARTIAN (out of scope) | WS1b | 7-band Mars | free | free/open | candidate | [D] |
| D141 | Hephaestus | WS1b | S1 interferograms | free | free/open | candidate | [D] |
| D142 | Thalia ↔D21 | WS1b | InSAR datacubes | free | free/open | candidate | [D] |
| D143 | KnowAir (PM2.5-GNN) | WS7/WS8 | station TS+meteo | free | free/open | candidate | [D] |
| D144 | TAP (China air pollution) | WS7/WS8 | sat+ground+model | free | free/public | candidate | [D] |
| D145 | Bihar low-cost PM2.5 network | WS7/WS8 | sensor TS+meteo | free | reported public | candidate | [D] |
| D146 | California Wildfire PM2.5 | WS7/WS8 | station TS | free | from EPA AQS (public) | candidate | [D] |
| D147 | CEED (California EQ Event) | WS8 | waveforms+picks | free | free/open | candidate | [D] |
| D148 | STEAD (Stanford EQ) | WS8 | 3-comp waveforms | free | free/open | candidate | [D] |
| D149 | POSEIDON | WS8 | event catalog+energy | free | free/open | candidate | [D] |
| D150 | MultiSeismo | WS8 | waveforms+intensity | free | free/open (reported) | candidate | [D] |
| D151 | CrisisBench / CrisisNLP | WS2/WS3 | tweets | free | free/open | candidate | [D] |
| D152 | CrisisMMD ↔D16 | WS2/WS3 | text+images | free | free/open | candidate | [D] |
| D153 | MEDIC | WS2/WS3 | images (multi-task) | free | free/open | candidate | [D] |
| D154 | GeoCoV19 ↔D112 | WS2/WS3 | geolocated tweets | free | free/open | candidate | [D] |
| D155 | HumAID / HUMAID-NER | WS2/WS3 | tweets (+NER) | free | free/open | candidate | [D] |
| D156 | TSEqD (Turkey-Syria EQ) | WS2/WS3 | text+img+social | free | reported released | candidate | [D] |
| D157 | DisasterVQA | WS2/WS3 | images+Q/A | free | free/open | candidate | [D] |
| D158 | DFDC ↔D70 | WS2 | face video | free (EULA) | EULA — actor-likeness | candidate | [D] |
| D159 | FaceForensics++ ↔D68 | WS2 | face video | free (EULA) | EULA — signed request | candidate | [D] |
| D160 | FakeAVCeleb | WS2 | video+synth audio | request | access-on-request (restricted) | candidate | [D] |
| D161 | DeepFake MNIST+ | WS2 | video | free | free (reported) | candidate | [D] |
| D162 | CtrSVDD | WS2 | singing-voice audio | free | public | candidate | [D] |
| D163 | Codecfake | WS2 | codec deepfake audio | free | free/open (reported) | candidate | [D] |
| D164 | AUDETER | WS2 | deepfake audio | free | free/open | candidate | [D] |

*(↔ pairs are the same underlying dataset listed in two discovery phases; both IDs are kept for registry
traceability. Full duplicate list in [04a §2.11 note](<04a_DATASETS.md>).)*

---

## 5. Licensing & access

**Indian government EO/hazard portals are JS-driven → MANUAL verification required.** Bhuvan, MOSDAC,
VEDAS, NRSC, IMD, CWC, and GSI (BHUKOSH) portals render as a JS-only "Loading…" shell and **could not be
scraped** here (`web_fetch` reached but got no content; `web_search` had no API key). Their terms-of-use and
the India-specific layers behind them (D24 Bhuvan inventories, D46 GSI, D47 IMD, D52 ICIMOD, D53 CWC) are
**[UNVERIFIED]** and carried to the deployment backlog — these are the priority for an India pilot. D24
Bhuvan/NRSC-ISRO is the single item most likely to need a slow government request → flagged EARLY ACTION.

**Free-only rule (constraint C4, `_CANON.md §5`).** A dataset may be `STATUS=selected` only if it is free
(or free-with-registration). UNCLEAR-cost sets (D11 GLOFNet, D20 GDCLD) stay candidate. **IMD (D47)** and
**CWC/India-WRIS (D53)** are frequently restricted/paid — the central access risk for calibrating Himalayan
rainfall thresholds and discharge ratings; recorded as `candidate / cost varies`, never selected.

**Registration needed early (free):** NASA Earthdata (D03/D04/D06/D07-V1), Copernicus Data Space
(D01/D02), Copernicus CDS + API key (D05), PlanetScope research access (D19).

**EULA / access-restricted (deepfake & CPS):** FaceForensics++ (D68/D159), Celeb-DF (D69), DFDC
(D70/D158), WildDeepfake (D71), DF40 (D72), FakeAVCeleb (D160) need signed research agreements; SWaT/WADI
(D63) and CRAWDAD (D93) are request-based. Face/AV sets carry consent/privacy constraints — method
development only, **no deceptive media created** (see ch 14).

**Out of scope:** **D140 MMLSv2 is MARTIAN** — listed only for registry completeness; excluded from the
Earth early-warning scope. "Upon acceptance" / host-TBA sets (D115 GWFP, D128 EFFIS, D145 Bihar, D156
TSEqD) may not be live — recheck before use.

---

## 6. Leakage & split policy

Random/scene cross-validation **overstates** skill in geospatial hazard tasks; spatial-block CV is
mandatory. This verdict is triangulated across three re-fetched papers (`_CANON.md §6`): arXiv **2608.12422**
(Himalayan GLOF/landslide — naïve ROC-AUC ~0.90 collapses to 0.54–0.76 under matched spatial-CV),
**2608.22293** (Palisades urban-wildfire — 0.92→0.75 under 1 km blocks), and **2610.08227** (effective
sample size N_eff = Θ(n²/r²) justifying block holdout). **Full protocol: chapter 12.**

Per-dataset split guidance (from the registry's dataset→model matrix):
- **SAR/EO cubes (D01, D21):** tile + time block CV with buffer ≥ InSAR range (DC-01).
- **Flood (D17 GEOID, D12 Sen1Floods11, D19, D26):** adopt event-level splits; **re-split Sen1Floods11 by
  event** (its native scene-level split is leaky).
- **Landslide (D18 LMHLD, D09, D20):** region-block CV + val→held-out shift test.
- **Covariates (D03/D05/D04):** temporal block CV, monsoon-season held-out.
- **GLOF (D07, D15, D11):** leave-one-basin-out.
- **Indian events (D22, D25, D08):** temporal + leave-one-region-out.
- **Crisis media (D16):** leave-one-event-out; never autonomous (Rule 19).

**Small-n GLOF caveat:** GLOF/landslide positives are thin in-region (D15 ~766 events UNVERIFIED,
leave-one-basin-out), so transfer stress (train global D12/D13/D26/D20 → test Himalayan subset) is
unavoidable and is registered as a **domain-shift risk** (ch 12/22). Mandatory baselines before any
foundation model: persistence (C-03) + GBDT (C-02) + a tuned U-Net.

---

## 7. Dataset ↔ model / chapter cross-index (SELECTED datasets)

| Selected dataset(s) | WS | Model role | Chapter |
|---------------------|----|-----------|---------|
| D01 Sentinel-1 (+D21 coherence) | WS1/WS8 | masked-InSAR SSL encoder + deformation-forecast head | 05, 06 |
| D02 Sentinel-2 | WS4/WS8 | optical–SAR fusion flood head + EO encoder | 05, 06, 09 |
| D03 IMERG, D05 ERA5-Land, D04 SMAP | WS1/WS3 | rainfall/antecedent covariates + nowcasting | 06, 08 |
| D06 MODIS | WS8 | snow-cover/LST seasonal context | 06 |
| D07 ITS_LIVE | WS8 | GLOF precursor (glacier acceleration) | 06 |
| D08 NASA GLC, D22 IFI, D15 HMAGLOFDB | WS1/WS3/WS8 | Indian/HMA event labels + impact targets | 06, 08, 12 |
| D17 GEOID-Flood, D12 Sen1Floods11 | WS1/WS8 | flood segmentation + optical–SAR fusion | 05, 06, 12 |
| D18 LMHLD | WS1 | landslide detection/seg + PEFT adaptation | 05, 06, 12 |

SSL corpora D10/D13 (candidates) pretrain the EO encoder; D14 is a sanity/worst-group fixture. Evaluation
protocol and admission gate: chapter 12. Model formulations: chapter 05.

---

## 8. References

Every arXiv ID cited above (and in [04a](<04a_DATASETS.md>)) resolves through
[19_REFERENCES_FULL.md](<19_REFERENCES_FULL.md>), with verification status. Registry source artifacts:
[`DATASETS.md`](<../DATASETS.md>), [`DATASETS_CATALOGUE.md`](<../DATASETS_CATALOGUE.md>).
