# DATASETS — the ONE living dataset registry (MASTER_PROMPT §0.9A)
#
# Populated in Phase P5 (2026-10-07). FREE-ONLY: only free datasets may be STATUS=selected; paid
# datasets are STATUS=rejected-paid. COST/LICENSE are VERIFIED from the official source — never assumed.
# Never download in this run (links/metadata/plans only).
#
# VERIFICATION LEGEND (honest, §0.5):
#   [V]   = verified on direct authoritative fetch this phase (portal/Zenodo/GitHub/arXiv).
#   [V*]  = existence verified, but ONE stated fact (count/exact-license) UNVERIFIED — flagged inline.
#   [D]   = discovery-only (authoritative page not directly fetched; corroborated by a secondary source).
# Verification evidence: PROGRAM/logs/P5_dataset_verification.md mirrors the per-dataset fetch verdicts.
# COST values: free / free-with-registration / free-on-request / paid / unclear.

## QUICK LINKS (sorted by workstream; selected first). COST+LICENSE verified unless marked UNVERIFIED.

| ID | Name | WS | Link | COST | License | Access | Size / N | Kaggle/HF? | STATUS | Ver |
|----|------|----|------|------|---------|--------|----------|-----------|--------|-----|
| D01 | Sentinel-1 SAR (Copernicus CDSE) | WS1/WS8 | https://dataspace.copernicus.eu/ | free-with-registration | Copernicus free/open | open; reg for bulk/API | continuous mission (C-band GRD/SLC ~10 m) | AWS/GEE mirror | selected | [V] |
| D02 | Sentinel-2 MSI (Copernicus CDSE) | WS4/WS8 | https://dataspace.copernicus.eu/ | free-with-registration | Copernicus free/open | open; reg for download | continuous mission (13-band 10/20/60 m) | AWS/GEE mirror | selected | [V] |
| D03 | GPM IMERG precipitation (NASA) | WS1/WS3 | https://gpm.nasa.gov/data/imerg | free-with-registration | NASA open data | Earthdata/PPS login | 0.1°, half-hourly, 2000–present (V07) | Giovanni/GeoTIFF | selected | [V] |
| D04 | SMAP soil moisture (NASA NSIDC) | WS1 | https://nsidc.org/data/smap | free-with-registration | NASA open data | Earthdata login | global 2015–present, ~9–36 km | NSIDC/ASF | selected | [V] |
| D05 | ERA5-Land reanalysis (ECMWF/C3S) | WS1 | https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land | free-with-registration | CC-BY (DOI 10.24381/cds.e2161bac) | CDS API | 0.1° (9 km) hourly 1950–present | GEE mirror | selected | [V] |
| D06 | MODIS (NASA LP DAAC) | WS8 | https://www.earthdata.nasa.gov/centers/lp-daac | free-with-registration | NASA open data | Earthdata/AppEEARS/GEE | Terra/Aqua 2000–present 250 m–1 km | GEE/AWS | selected | [V] |
| D07 | ITS_LIVE glacier velocity (NASA/JPL) | WS8 | https://its-live.jpl.nasa.gov/ | free (newer cloud); reg for V1 | NASA open (MEaSUREs) | portal/STAC/Zarr/S3 | global 1985–present 120 m | AWS S3 | selected | [V] |
| D08 | NASA Global Landslide Catalog / COOLR | WS1/WS8 | https://gpm.nasa.gov/applications/landslides/coolr | free | NASA open data | viewer/open-data portal | point events (count UNVERIFIED) | data.nasa.gov | selected | [V*] |
| D09 | Landslide4Sense | WS1/WS8 | https://huggingface.co/datasets/ibm-nasa-geospatial/Landslide4sense | free | UNVERIFIED (no license on card) | HF/GitHub download | 3,799/245/800 patches, 14-band 128² | HF yes | candidate | [V*] |
| D10 | SSL4EO-S12 | WS1/WS8 | https://github.com/zhu-xlab/SSL4EO-S12 | free | code Apache-2.0; data+weights CC-BY-4.0 | mediaTUM/HF | 251,079 locs ×4 seasons (~1.5 TB raw) | HF yes | candidate | [V] |
| D11 | GLOFNet (multimodal GLOF) | WS8 | https://arxiv.org/abs/2510.10546 | unclear | paper CC BY-NC-ND 4.0; data license UNVERIFIED | download URL UNVERIFIED | S2+ITS_LIVE+MODIS, Shisper/Karakoram | none confirmed | candidate | [V*] |
| D12 | Sen1Floods11 | WS1/WS8 | https://github.com/cloudtostreet/Sen1Floods11 | free | UNVERIFIED (open GCS bucket; CVPRW2020) | gsutil gs://sen1floods11 (~14 GB) | 11 events, 512² chips (4,831 count UNVERIFIED) | Radiant/HF copies | selected | [V*] |
| D13 | BigEarthNet v2 (reBEN) | WS4/WS8 | https://bigearth.net/ | free | CDLA-Permissive-1.0 | Zenodo 10891137 | 549,488 S1+S2 patches (~110 GiB) | HF models | candidate | [V] |
| D14 | EuroSAT | WS4 | https://github.com/phelber/EuroSAT | free | MIT (+ Copernicus S2) | Zenodo 7711810 | 27,000 imgs, 10 cls, 13-band 64² | HF/TorchGeo/TFDS | candidate | [V] |
| D15 | HMAGLOFDB (High Mtn Asia GLOF DB) | WS8 | https://github.com/fidelsteiner/HMAGLOFDB | free | CC BY 4.0 (confirm on release) | GitHub/ICIMOD RDS | 766 GLOFs 1533–2025 (v4.0, [D]) | — | selected | [D] |
| D16 | CrisisMMD / CrisisNLP | WS2/WS3 | https://crisisnlp.qcri.org/crisismmd | free | UNVERIFIED ("Terms of use", research) | open download (~1.8 GB) | 7 events; ~16k tweets/18k imgs | HF copies | candidate | [V*] |
| D17 | GEOID-Flood | WS1/WS8 | https://github.com/links-ads/geoid-flood | free | per repo (verify) | GitHub | 14,282 tiles, 219 events, S1+S2+DEM | — | selected | [D] |
| D18 | LMHLD landslide dataset | WS1/WS8 | https://doi.org/10.5281/zenodo.11424988 | free | open-access Zenodo (verify per-source) | Zenodo | 25,365 patches, 5 sensors, 7 areas (Gorkha) | Zenodo | selected | [D] |
| D19 | UFO Urban Flood Observations | WS1/WS4 | arXiv:2604.23066 | free (PlanetScope reg) | per paper (verify) | per paper repo | 215 chips, 14 events, 3 m | — | candidate | [D] |
| D20 | GDCLD (coseismic landslide) | WS1 | arXiv:2604.16663 | unclear | UNVERIFIED | per paper | global coseismic landslide seg | — | candidate | [D] |
| D21 | Thalia (InSAR deformation) | WS1/WS8 | https://github.com/Orion-AI-Lab/Thalia | free | per repo (verify) | GitHub | 38 datacubes, 7 yr, InSAR+topo+atmos | — | candidate | [D] |
| D22 | India Flood Inventory – Impacts (IFI) | WS1/WS3 | https://zenodo.org/records/11275211 | free | CC BY 4.0 | Zenodo (CSV, ~1.9 MB) | district-level flood events 1967–2023 (3 CSVs) | GitHub hydrosenselab | selected | [V] |
| D23 | Kerala 2018 monsoon landslide inventory (ITC) | WS1 | https://research.utwente.nl/en/datasets/landslide-inventory-of-the-2018-monsoon-rainfall-in-kerala-india/ | unclear | UNVERIFIED | institutional page | 2018 Kerala landslides | — | candidate | [D] |
| D24 | Bhuvan/NRSC-ISRO landslide inventories | WS1/WS8 | https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/landslide/landslide.php | free-with-registration (likely) | UNVERIFIED (ISRO terms) | Bhuvan portal | Landslide Atlas of India; Uttarakhand 2013; J&K; Sikkim; Wayanad | — | candidate | [D] |
| D25 | INDOFLOODS (station discharge flood events) | WS1/WS3 | https://zenodo.org/records/14584654 | free (likely) | UNVERIFIED | Zenodo | Indian observational flood events | — | candidate | [D] |
| D26 | Landslide Reference Data S1&S2 (DLR/GFZ) | WS1 | https://zenodo.org/records/15421843 | free | CC BY 4.0 | Zenodo (6.2 GB) | worldwide large landslides 2015+ | Zenodo | candidate | [V] |

## FULL ENTRIES (defined in P5)

### CORE SENSOR STREAMS (the physical backbone — all FREE, all global incl. India/Himalaya)
These are continuous missions, not fixed benchmarks; we build our own event-indexed cubes from them.
- **D01 Sentinel-1 SAR** [V] — Copernicus free/open; C-band GRD/SLC ~10 m; all-weather, cloud-penetrating
  → the single most important stream for monsoon floods + landslide deformation (SAR-first, C-01 L-thread).
  Access: Copernicus Data Space Ecosystem; free registration for bulk/STAC/openEO/Sentinel-Hub. Known
  issue: SLC interferometry is heavy → use GRD + learned-coherence proxy (D21/2606.07374) to stay in budget.
- **D02 Sentinel-2 MSI** [V] — Copernicus free/open; 13-band 10/20/60 m. Monsoon CLOUD COVER is the key
  limitation → pair with SAR (optical-SAR fusion, DC-09). Legal-notice PDF itself not fetchable (minor).
- **D03 GPM IMERG** [V] — NASA open; 0.1° half-hourly 2000–present (V07, now 90°N–S). NASA notes
  precipitation is LESS CERTAIN over mountains and V07 is snowfall-deficient → treat Himalayan IMERG as a
  noisy covariate (feeds CR-08 / P14Z TSFM-covariate-noise concern).
- **D04 SMAP** [V] — NASA open; L-band soil moisture 2015–present; coarse 9–36 km → weak over steep
  Himalayan terrain; use as a regional antecedent-wetness prior, not a local trigger.
- **D05 ERA5-Land** [V] — ECMWF/C3S, **CC-BY** (DOI 10.24381/cds.e2161bac); 9 km hourly 1950–present via
  CDS API. 9 km smooths Himalayan topography → downscale or use as boundary forcing (HEC-RAS, 2507.15614).
- **D06 MODIS** [V] — NASA open; 250 m–1 km LST/NDVI/snow 2000–present; LP DAAC/AppEEARS/GEE. Snow-cover +
  LST products for GLOF/seasonal context (WS8).
- **D07 ITS_LIVE** [V] — NASA open (MEaSUREs); global ice velocity 1985–present 120 m incl. High Mountain
  Asia; STAC/Zarr/S3. Direct GLOF-precursor signal (glacier acceleration). V1 (pre-Apr-2023) needs
  Earthdata login; newer cloud data open.

### HAZARD EVENT CATALOGUES / INVENTORIES (labels & triggers)
- **D08 NASA GLC/COOLR** [V*] — NASA open; global rainfall-triggered landslide point reports; viewer +
  open-data portal. ⚠ event count NOT verified from an authoritative page this session (~11,000 is cited
  but UNVERIFIED). Use as weak/positive-event labels, not an exhaustive inventory.
- **D15 HMAGLOFDB** [D] — High Mountain Asia GLOF inventory; ESSD-2023 paper + GitHub (fidelsteiner) +
  ICIMOD RDS. ⚠ 766 GLOFs (1533–2025, v4.0) and CC BY 4.0 come from a secondary dashboard — CONFIRM on the
  GitHub/ICIMOD release before load-bearing use. HIGHLY India-relevant (Indian Himalaya/Nepal/Bhutan/
  Karakoram). Our primary GLOF label source (pairs with ITS_LIVE + 2608.12422 589-event re-study).
- **D22 India Flood Inventory – Impacts (IFI)** [V] — HydroSense Lab IIT-Delhi + IMD; **CC BY 4.0**;
  Zenodo 11275211 (v3) + GitHub hydrosenselab; national flood events 1967–2023 (CSV). Our primary Indian
  flood-event label/impact source — the single most India-specific verified dataset found.
- **D25 INDOFLOODS** [D] — Indian observational (station-discharge) flood events; Zenodo 14584654. ⚠
  license/size UNVERIFIED. Complements IFI with gauged discharge.
- **D23 Kerala-2018 landslide inventory** [D] / **D24 Bhuvan-NRSC inventories** [D] — Indian/Himalayan
  landslide polygons (Uttarakhand 2013, J&K 2014, Sikkim 2016, Wayanad, Landslide Atlas of India). ⚠
  access + license UNVERIFIED (ISRO/Bhuvan terms) → REGISTRATION-NEEDED early action (see §registration).

### FLOOD ML BENCHMARKS (ready-made imagery+labels)
- **D17 GEOID-Flood** [D] — 14,282 tiles, 219 events/65 countries, bi-temporal S1(GRD+RTC)+S2(L2A)+GLO-30
  DEM, 3-class, EVENT-LEVEL leakage-safe split; github links-ads/geoid-flood. Our PRIMARY flood training/
  eval candidate; its Table 1 also catalogues 10 further flood sets. ⚠ repo license to confirm on fetch.
- **D12 Sen1Floods11** [V*] — 11 events, S1+S2+hand labels, open GCS bucket (~14 GB). ⚠ exact license +
  the cited 4,831-chip count UNVERIFIED on the README. No India event → transfer-eval only.
- **D19 UFO** [D] — 215 PlanetScope chips, 14 events, leave-one-event-out CV; shows off-the-shelf water
  products (NASA IMPACT 44.1, Dynamic World 48.1 IoU) are weak. PlanetScope = research registration.
- Catalogued-not-adopted (from GEOID-Flood Table 1): ETCI-2021, WorldFloods-v2, MMFlood, OmbriaNet,
  Kuro Siwo, CAU-Flood, S1GFloods, STURM-Flood, FloodNet; + FloodsNet (D-, via 2512.02055). Add on demand.

### LANDSLIDE ML BENCHMARKS
- **D18 LMHLD** [D] — 25,365 patches, 5 sensors, 7 areas incl. **Gorkha Nepal 2015** (Himalayan); open
  Zenodo DOI 10.5281/zenodo.11424988. Our primary landslide-detection training set (in-region-adjacent).
  ⚠ confirm per-source sub-licenses on Zenodo.
- **D09 Landslide4Sense** [V*] — 3,799/245/800 patches, 14-band (S2 B1–B12 + ALOS slope + DEM), 128²,
  pixel masks; HF + GitHub mirrors (original IARAI site DEAD). ⚠ NO license on the HF card → treat as
  candidate until license confirmed.
- **D20 GDCLD** [D] (via 2604.16663) — global COSEISMIC landslide segmentation benchmark; our PEFT/
  adaptation-strategy reference. ⚠ license UNVERIFIED. Coseismic ≠ our hydrological trigger.
- **D26 Landslide Reference Data S1&S2 (DLR/GFZ)** [V] — **CC BY 4.0**; Zenodo 15421843 (6.2 GB);
  worldwide large landslides 2015+ (S1+S2 for U-Net). Clean-license transfer set.

### GLACIER / INSAR DEFORMATION
- **D21 Thalia** [D] — 38 InSAR datacubes, 7 yr, InSAR+topo+ATMOSPHERIC (artifact confound) + expert
  deformation labels + text; github Orion-AI-Lab/Thalia. Closest open analogue to our InSAR-anomaly task;
  VOLCANIC → transfer. ⚠ repo license to confirm.
- **D11 GLOFNet** [V*] — S2+ITS_LIVE+MODIS, Shisper/Karakoram; arXiv 2510.10546 (paper CC BY-NC-ND 4.0).
  ⚠ dataset download URL + data license UNVERIFIED → keep candidate until a real download is located.

### SSL PRETRAINING / CORPORA (unlabeled, for the masked InSAR/EO encoder)
- **D10 SSL4EO-S12** [V] — code Apache-2.0, **data+weights CC-BY-4.0**; 251,079 locations ×4 seasons
  (S1+S2 L1C+L2A); mediaTUM + HF. Our primary SSL pretraining corpus (global incl. Himalaya, unlabeled).
  Full raw ~1.5 TB → use the compressed 8-bit variant / regional subset for the Kaggle budget.
- **D13 BigEarthNet v2** [V] — **CDLA-Permissive-1.0**; 549,488 S1+S2 patches (~110 GiB); Zenodo 10891137.
  ⚠ EUROPE-ONLY → use for pretraining/transfer, never as Himalayan ground truth.
- **D14 EuroSAT** [V] — **MIT**; 27,000 imgs 10-class 13-band; Zenodo 7711810. Europe-only → sanity/debug
  + a FairRSFM(2610.05790) worst-group fixture; not representative of India.

### CRISIS MEDIA (WS2/WS3 — LOW-TRUST advisory channel, Rule 19)
- **D16 CrisisMMD/CrisisNLP** [V*] — 7 events (2017), ~16k tweets/18k images; open download (~1.8 GB).
  ⚠ exact license = generic "Terms of use" (research); ENGLISH-centric, NO India event (nearest: 2017 Sri
  Lanka floods). Indian-language/code-mixed crisis data is a GAP → feeds a research-note risk, not a core
  dependency. HUMAID-NER (2609.16964) is the structured-extraction companion (also English-only).

## DATASET → MODEL / WORKSTREAM MATRIX
| Dataset(s) | WS | Model role | Native split leakage-safe? | Our re-split |
|-----------|----|-----------|----------------------------|--------------|
| D01 S1 + D21/2606.07374 coherence | WS1/WS8 | masked InSAR SSL encoder + deformation-forecast head | n/a (we index) | tile+time block CV, buffer ≥ range (DC-01) |
| D10 SSL4EO-S12, D13 BigEarthNet | WS8 | SSL pretraining of the EO encoder | n/a | pretrain only; eval elsewhere |
| D17 GEOID-Flood, D12 Sen1Floods11, D19 UFO, D26 | WS1/WS8 | flood segmentation + optical-SAR fusion | GEOID/UFO YES; Sen1Floods11 scene-level | adopt event-level; re-split Sen1Floods11 by event |
| D18 LMHLD, D09 L4S, D20 GDCLD | WS1 | landslide detection/seg + PEFT adaptation | partial | region block CV + val→held-out shift test |
| D03 IMERG, D05 ERA5-Land, D04 SMAP | WS1/WS3 | rainfall/antecedent covariates + nowcasting | n/a | temporal block CV; monsoon-season held-out |
| D07 ITS_LIVE, D11 GLOFNet, D15 HMAGLOFDB, D05/D21 | WS8 | GLOF precursor (velocity + lake) + outburst labels | n/a | leave-one-basin-out |
| D22 IFI, D25 INDOFLOODS, D08 GLC, D23/D24 | WS1/WS3 | Indian event labels / impact targets | n/a | temporal + leave-one-region-out |
| D16 CrisisMMD, HUMAID-NER | WS2/WS3 | low-trust media advisory signal | event-level | leave-one-event-out; never autonomous |
| (any tabular features) | WS6 | GBDT baseline (mandatory, C-02) + simple MLP | — | same block CV as the model it baselines |

## CROSS-EVALUATION PLAN (DC-01/DC-02/DC-05 enforced)
1. Train on in-region/in-region-adjacent (D18 Gorkha, D22 IFI, D15 HMA, D21/D01), test LEAVE-ONE-REGION/
   -BASIN/-EVENT-OUT → the only admissible headline numbers (spatial-CV theorem 2610.08227).
2. Report worst-REGION (FairRSFM 2610.05790) + cost-loss TCC (2510.22016), not mean F1/AUC.
3. Transfer stress: train on global (D12/D13/D26/D20) → test on Himalayan subset to quantify domain shift
   (GLOF/landslide are thin in-region → domain shift is unavoidable; register as risk).
4. Missing-modality worst case (DC-05): evaluate with each sensor dropped (cloud kills S2; storm kills
   LoRa/power) using mask-conditional conformal (2512.14221) + availability-aware inputs (FLORO 2605.28174).
5. Mandatory baselines every task: persistence (C-03) + GBDT (C-02) + a tuned U-Net (2512.02055 shows it
   is strong) before any foundation model earns its compute.

## REGISTRATION-NEEDED / EARLY-ACCESS ACTIONS (surface at the P5 gate)
- **NASA Earthdata Login** (urs.earthdata.nasa.gov) — needed for D03 IMERG, D04 SMAP, D06 MODIS, D07
  ITS_LIVE V1. Free; register early.
- **Copernicus Data Space Ecosystem** account — D01/D02 bulk/API. Free; register early.
- **Copernicus CDS** account + CDS API key — D05 ERA5-Land. Free; register early.
- **Bhuvan/NRSC-ISRO portal** (D24) — Indian landslide inventories; access + license UNVERIFIED → the one
  item that may need a government request/registration and could be slow → EARLY ACTION, flagged to user.
- **PlanetScope research access** (D19 UFO) — free with research registration; optional (urban-flood only).
- **CONFIRM-BEFORE-USE licenses** (do not treat as selected until confirmed): D09 Landslide4Sense (no
  license on card), D11 GLOFNet (data license + download), D12 Sen1Floods11 (exact license), D16
  CrisisMMD (exact license), D15 HMAGLOFDB (confirm count+CC-BY on release page), D17/D18/D20/D21/D23/
  D25 (fetch repo/Zenodo license page).

## SELECTED-DATASETS SUMMARY (STATUS=selected → the free, verified shopping list)
Core sensors: D01 Sentinel-1, D02 Sentinel-2, D03 GPM IMERG, D04 SMAP, D05 ERA5-Land, D06 MODIS, D07
ITS_LIVE. Hazard labels: D08 NASA GLC, D15 HMAGLOFDB, D22 IFI-Impacts. Flood ML: D17 GEOID-Flood, D12
Sen1Floods11. Landslide ML: D18 LMHLD. All verified FREE (several with free registration); the only
cost-type beyond "free"/"free-with-registration" encountered is UNCLEAR (D11 GLOFNet, D20 GDCLD) — those
stay CANDIDATE, not selected, until license is confirmed. NO paid dataset is selected (free-only rule held).

## P6 ADDITIONS — fire-detection / low-cost-sensor datasets (added 2026-10-09, §0.9A rules)
These support the WS7a fire-detection IoT node (P6). Verification is PAPER/REPO-level (existence confirmed
via the arXiv record / repository named by the quota reading); portal licenses to confirm before use.
| ID | Name | WS | Link | COST | License | N / modality | STATUS | Ver |
|----|------|----|------|------|---------|--------------|--------|-----|
| D27 | Multiple-Categories Visual Smoke DB | WS7a/WS4 | arXiv:2208.00210 | free (likely) | UNVERIFIED (per paper) | 70,196 images, multi-class smoke TYPES | candidate | [D] |
| D28 | UCI Gas Sensor Array Drift | WS7a | https://archive.ics.uci.edu/dataset/224/ | free | typically CC BY 4.0 (confirm on UCI) | MOX e-nose long-term drift benchmark | candidate | [D] |
| D29 | Low-Cost Indoor AQ Calibration dataset | WS7a | arXiv:2610.11236 | free (likely) | UNVERIFIED (per paper) | 6-mo, 5 locations, low-cost+reference AQ + metadata | candidate | [D] |
| D30 | RESPIRE India CO calibration (code/data) | WS7a | https://github.com/purushottamkar/respire | free (likely) | UNVERIFIED (confirm repo) | India multi-site/season/sensor CO calibration | candidate | [D] |
Notes: D27 gives the nuisance-vs-dangerous smoke distinction (benign steam/exhaust != alarm) the camera
stage needs. D28 is the standard MOX-drift benchmark behind our gas-sensor delta/baseline-normalization
design. D29/D30 anchor the India/real-world calibration reality (season/site/unit drift, outliers normal).
The DCP ESP32-HMAC firmware (github.com/device-context-protocol/dcp, MIT) is reusable CODE, not a dataset.
All [D] discovery-level → confirm license/size on the source page before any build-time use; none selected.

### P7 physics validation/benchmark datasets (WS1a; §0.9A, all [D] discovery-only, none selected)
| ID | Name | WS | Source | Cost | License | Content | Status | Legend |
|----|------|----|--------|------|---------|---------|--------|--------|
| D31 | NIST FDS Validation Guide + experimental suite | WS1a | https://pages.nist.gov/fds-smv/ ; github.com/firemodels/fds | free | US-Gov public domain / FDS BSD-style (confirm per-set) | HGL/plume/ceiling-jet temp, species vs experiments | candidate | [D] |
| D32 | NIST Fire Calorimetry Database | WS1a | https://www.nist.gov/el/fire-research-division-73300 | free | US-Gov public domain (confirm per-report) | measured HRR curves (furniture/room-corner) for EF-02 | candidate | [D] |
| D33 | NIFC/GeoMAC-lineage wildfire perimeters (Thomas, Haypress, Pacific Palisades) | WS1a | US fire-perimeter archives (via quota refs 2302.04960/2510.09708) | free (likely) | US public (confirm) | fire-front perimeters for EF-11/level-set validation | candidate | [D] |
| D34 | WRF-SFIRE / CSIRO SPARK simulation cases (S03/E06; cWGAN set) | WS1a | via arXiv:2212.00970 / 2309.02615 | free (likely) | UNVERIFIED (confirm with authors/repos) | coupled-model spread sims + satellite active-fire | candidate | [D] |
P7 notes (honest): D31/D32 are the named validation anchors for EF-01..EF-10 (plume/flame/ceiling-jet/HRR/
radiation/extinction) and were NOT re-fetched this session (web_search had no API key; classic correlations
~0 on arXiv) → portal fetch + license confirm is an OPEN action carried to the P7 gate. D33/D34 come from
the P7 quota wildfire-spread papers with license UNCONFIRMED. No physics dataset is claimed verified; none
selected. The classic fire correlations themselves (Heskestad/Alpert/etc.) are inventory SOURCES, not
datasets.

### P8 CCTV fire/smoke detection datasets (WS4; all [D] discovery-only, licenses NOT verified this session)
| ID | Name | WS | Source | Cost | License | Content | Status | Legend |
|----|------|----|--------|------|---------|---------|--------|--------|
| D35 | FIgLib (Fire Ignition Library) | WS4 | hpwren.ucsd.edu ; via arXiv:2112.08598 | free | public (per paper; not confirmed) | ~25k fixed-camera HPWREN smoke images, time-indexed ignition | candidate | [D] |
| D36 | PYRONEAR-2025 | WS4 | pyronear.org ; arXiv:2402.05349 | free | open-source project (confirm) | real-world early-wildfire camera-network benchmark (multi-site) | candidate | [D] |
| D37 | D-Fire | WS4 | github.com/gaiasd/DFireDataset ; via arXiv:2510.10108 | free | commonly MIT (NOT confirmed) | fire+smoke detection images (standard YOLO benchmark) | candidate | [D] |
| D38 | Multi-Scene FSD benchmark | WS4 | xiaoyihan6.github.io/FSD ; arXiv:2410.16631 | free | not stated | standardized multi-scene fire/smoke detection corpus | candidate | [D] |
| D39 | AusSmoke / MultiNatSmoke | WS4 | github.com/henryzhao0615/MultiNatSmoke ; arXiv:2604.23542 | free | not stated | diverse natural-scene smoke segmentation masks | candidate | [D] |
| D40 | SmokeBench (surveillance desmoking, early-stage) | WS4 | arXiv:2509.12701 (ACM MM'25) | free | not stated | 0-15 min post-ignition surveillance imagery | candidate | [D] |
| D41 | GWFP (Global Wildfire Prevention) | WS4 | arXiv:2606.10174 | free | "open-source" (not visible) | large image+video wildfire detection/classification | candidate | [D] |
| D42 | FLAME (aerial RGB+thermal pile-burn) | WS4 | IEEE DataPort ; arXiv:2012.14036 | free | IEEE DataPort terms (confirm) | aerial RGB+IR fire classification/segmentation | candidate | [D] |
| D43 | WIT-UAS (wildland-fire IR thermal) | WS4 | arXiv:2312.09159 (IROS'23) | free | not visible | IR thermal wildland-fire crew/asset detection | candidate | [D] |
| D44 | Fire360 (degraded 360° firefighting video) | WS4 | arXiv:2506.02167 | free | not visible | degraded-visibility indoor fire video benchmark | candidate | [D] |
P8 notes (honest): all CCTV datasets are [D] discovery-only; licenses NOT verified (web_search no API key;
arXiv API rate-limited). D-Fire + FIgLib + PYRONEAR-2025 are the primary candidates to reproduce published
baselines under the LEAKAGE-SAFE protocol (ws4_cctv/evaluation_protocol.md). FASDD and Foggia/MIVIA (known
in the literature) could NOT be verified this session → open action for non-arXiv portals. Many listed sets
are aerial/satellite/360° → domain-shift caveat vs fixed ground CCTV; mixing them risks cross-domain
leakage. None selected.

### P7G geo-hazard datasets (WS1b; §0.9A, all [D] discovery-only, licenses INDICATIVE/not verified)
| ID | Name | WS | Source | Cost | License | Content | Status | Legend |
|----|------|----|--------|------|---------|---------|--------|--------|
| D45 | NASA Global Landslide Catalog / COOLR | WS1b | gpm.nasa.gov/landslides ; data.nasa.gov | free | NASA open / public domain (indic.) | global rainfall-triggered landslide inventory | candidate | [D] |
| D46 | GSI Landslide inventory / BHUKOSH | WS1b | bhukosh.gsi.gov.in | free | GSI/Govt-India terms (indic.; may need login) | India landslide inventory + geology layers | candidate | [D] |
| D47 | IMD rainfall / gridded | WS1b | mausam.imd.gov.in ; cdsp.imdpune.gov.in | varies | IMD data-supply policy (often restricted/paid) | India station + gridded rainfall | candidate | [D] |
| D48 | NASA GPM IMERG precipitation | WS1b | gpm.nasa.gov | free | open (NASA EOSDIS) | satellite precipitation (global) | candidate | [D] |
| D49 | CHIRPS rainfall | WS1b | chc.ucsb.edu/data/chirps | free | public domain / open | quasi-global gauge+satellite rainfall | candidate | [D] |
| D50 | SRTM DEM | WS1b | earthexplorer.usgs.gov | free | public domain (USGS) | 30/90 m DEM | candidate | [D] |
| D51 | ALOS AW3D30 / Copernicus GLO-30 DEM | WS1b | eorc.jaxa.jp/ALOS/en/aw3d30 ; spacedata.copernicus.eu | free | attribution (JAXA/Copernicus) | 30 m DEM | candidate | [D] |
| D52 | ICIMOD HKH glacial-lake / GLOF inventory | WS1b | rds.icimod.org | free | ICIMOD open/attribution (indic.) | Himalayan glacial lakes + GLOF events | candidate | [D] |
| D53 | CWC / India-WRIS discharge & stage | WS1b | indiawris.gov.in | varies | Govt-India / NWIC (partly restricted) | river discharge + stage records | candidate | [D] |
| D54 | UNSODA unsaturated soil hydraulic DB | WS1b | ars.usda.gov | free | public domain | θ(ψ), K(θ) retention/conductivity for vanGenuchten | candidate | [D] |
P7G notes (honest): licenses are INDICATIVE (dataset license pages NOT fetched this session — web_search no
key, arXiv rate-limited). IMD (D47) and CWC (D53) are frequently restricted/paid — the central access risk
for calibrating GB-03 thresholds and GB-05 ratings in ungauged Himalayan catchments. NASA/USGS/CHIRPS/UNSODA
are open. All [D]; none selected. (A prior subagent "Verify EO/hazard dataset portals" ran earlier this
program — its confirmations, where recorded elsewhere, take precedence; re-verify at build time.)

### P9 anomaly-detection benchmarks (WS8; §0.9A, all [D] discovery-only; use for METHOD DEV only — real
operating-point numbers require our OWN normal-only logs/footage; licenses "not visible in abstract" per the
reading subagent → INDICATIVE)
| ID | Name | WS | Source | Cost | License | Content / known flaw | Status | Legend |
|----|------|----|--------|------|---------|----------------------|--------|--------|
| D55 | UCF-Crime | WS8 | standard WS-VAD page | free | not visible | surveillance VAD; background/scene bias, Micro-AUROC ≠ localization | candidate | [D] |
| D56 | XD-Violence | WS8 | standard WS-VAD page | free | not visible | multimodal VAD; pooled-Micro-AUROC localization issue | candidate | [D] |
| D57 | ShanghaiTech / CUHK Avenue / UCSD Ped | WS8 | standard VAD pages | free | not visible | classic VAD; trivial anomalies, label noise, saturates | candidate | [D] |
| D58 | SMD (Server Machine Dataset) | WS8 | OmniAnomaly repo | free | not visible | MTAD; high per-machine variability; PA inflation | candidate | [D] |
| D59 | NASA SMAP / MSL | WS8 | NASA telemetry | free | US-gov public (indic.) | spacecraft telemetry; trivial/explicit anomalies | candidate | [D] |
| D60 | NAB (Numenta Anomaly Benchmark) | WS8 | github.com/numenta/NAB | free | AGPL-3.0 (confirm) | streaming TS; NAB scoring weak to random/inflated scores | candidate | [D] |
| D61 | UCR Anomaly Archive | WS8 | Keogh/UCR | free | not visible | "rigorous" reference TS set; single-anomaly focused | candidate | [D] |
| D62 | TSB-AD / TSB-drift | WS8 | TSB-AD project | free | not visible | large standardized TS bench (VUS-PR); TSB-drift = real drift set | candidate | [D] |
| D63 | SWaT / WADI / BATADAL | WS8 | iTrust Singapore | free (request) | iTrust request-based license | CPS water-treatment attacks; class imbalance; protocol-dependent F1 | candidate | [D] |
| D64 | PSM | WS8 | eBay pooled server metrics | free | not visible | MTAD; PA/pooling issues | candidate | [D] |
| D65 | TinyMLperf (incl. anomaly-detection task) | WS8 | MLCommons | free | Apache-2.0 (indic.) | standardized MCU anomaly bench (ToyADMOS-style); constrained tasks | candidate | [D] |
| D66 | UrbanSound8K | WS8 | urbansounddataset.weebly.com | free | CC BY-NC 3.0 (indic.) | acoustic; repurposed as anomaly proxy | candidate | [D] |
| D67 | OddBench (686-690 tabular outlier sets) | WS8 | SCOUT/OddBench (2609.29580) | free | not visible | AUDIT corpus: train-test overlap in 355/690, label conflicts → leakage warning reference | candidate | [D] |
P9 notes (honest): these are PUBLIC benchmarks for method development ONLY; most carry documented flaws
(point-adjust inflation, trivial/explicit anomalies, pooled-Micro-AUROC ≠ localization, train-test overlap —
see OddBench D67). REAL operating-point numbers (false-alarms/sensor-day, detection delay) require our own
NORMAL-ONLY CCTV footage + IoT logs collected in the build under the normal-reference policy
(ws8_anomaly/design.md §7, evaluation_protocol.md). Licenses mostly "not visible in abstract" → INDICATIVE;
all [D]; none selected. VAD video sets (D55-D57) are SUPPORT-only in our scope (scope_decision.md).

## WS2 deepfake / misinformation forensic datasets (P11) — DISCOVERY-ONLY [D], licenses INDICATIVE
These are FIELD-STANDARD public forensic datasets staged ahead of the P11 reader's "FORENSIC DATASETS FOUND"
list (bounded reader d335c060) — the reader's set will be reconciled in on return (extras added, no
duplicates). All [D] discovery-only, none selected; licenses INDICATIVE until portal-verified; many are
LICENSE-GATED (request/EULA). Several are FACE datasets → privacy/consent + §ethics constraints apply; used
for method development ONLY, no deceptive media created (§content-safety). HONEST: in-distribution accuracy
on these overstates deployment performance — evaluation must be CROSS-GENERATOR + DEGRADED
(ws2_deepfake/evaluation_protocol.md).
| ID | Name | WS | Source | Cost | License | Content / known flaw | Status | Legend |
|----|------|----|--------|------|---------|----------------------|--------|--------|
| D68 | FaceForensics++ (FF++) | WS2 | TUM / FF++ page | free (request/EULA) | research-only EULA (indic.) | face-manipulation video (DF/F2F/FS/NT) + compression levels (c0/c23/c40); cross-dataset generalization weak; identities reused | candidate | [D] |
| D69 | Celeb-DF (v2) | WS2 | Celeb-DF page | free (request/EULA) | research-only EULA (indic.) | high-quality face-swap video; harder than FF++; cross-dataset gap | candidate | [D] |
| D70 | DFDC (Deepfake Detection Challenge) | WS2 | Meta/Kaggle | free (EULA) | DFDC EULA (indic.) | large face video; consented actors; label/quality variance | candidate | [D] |
| D71 | WildDeepfake | WS2 | WildDeepfake page | free (request) | research-only (indic.) | in-the-wild deepfake video; small, noisy, realistic degradation | candidate | [D] |
| D72 | DF40 | WS2 | DF40 project | free (request) | research-only (indic.) | 40 forgery methods for CROSS-method/cross-generator eval; the generalization benchmark | candidate | [D] |
| D73 | GenImage | WS2 | GenImage project | free | not visible | large real-vs-AI image set across multiple generators (GAN+diffusion); cross-generator splits | candidate | [D] |
| D74 | DiffusionForensics | WS2 | DIRE/DiffusionForensics repo | free | not visible | diffusion-generated image detection set; may overfit to specific samplers | candidate | [D] |
| D75 | ASVspoof (2019/2021/5) | WS2 | ASVspoof challenge | free | ODC/research (indic.) | synthetic/replayed speech countermeasure bench; channel/codec conditions; audio-only | candidate | [D] |
| D76 | NewsCLIPpings | WS2 | NewsCLIPpings repo | free | research (indic.) | OUT-OF-CONTEXT multimodal misinformation (image repurposing); automatically-constructed, domain-skewed | candidate | [D] |
P11 notes (honest): FACE datasets (D68-D72) carry consent/privacy constraints and are license-gated (EULA/
request) → confirm before any use; D73-D74 image sets risk sampler/generator overfit; audio D75 is audio-only.
The dominant REAL disaster-misinformation threat is OUT-OF-CONTEXT recycled real media (D76-type), not
deepfakes, so retrieval/geo-temporal-consistency datasets are prioritized. An INDIAN-LANGUAGE / code-mixed
disaster claim-verification set is a documented GAP (none standard) → to be assembled in the build. Pending
reader d335c060 may add XD-forensic / open-set generator benchmarks; those will be appended, not duplicated.

### P11 reader reconcile (d335c060) — new forensic sets, all [D], licenses INDICATIVE
| ID | Name | WS | Source | Cost | License | Content / known flaw | Status | Legend |
|----|------|----|--------|------|---------|----------------------|--------|--------|
| D77 | CCDF (surveillance deepfakes) ⚑ | WS2 | 2610.07939 release (3 versions) | free | not stated | 1,840 vids (460 real/1,380 gen) Sora2/VEO3.1/Grok, 16 CRIME/ACCIDENT categories; 10 SOTA detectors UNRELIABLE on it; metadata/post-proc attack versions. CLOSEST to disaster/accident + CCTV-corroboration threat | candidate | [D] |
| D78 | DF26 | WS2 | 2609.07369 | free | not stated | 271 real/2,420 synthetic, 7 modern T2V/I2V, public-speaking; humans+detectors ≈ chance; narrow scenario | candidate | [D] |
| D79 | BabelFake | WS2 | 2610.06339 | free (consent-based) | ethically-sourced (indic.) | 399k AV clips, 496 consenting speakers, 5 EU langs, 11 video×4 voice methods; EU-langs only; realism≠detectability | candidate | [D] |
| D80 | PhysForensics-Bench | WS2 | 2609.15562 | free | not stated | audio-video physical-scene set (Seedance+VEO), 9 scene families; only 2 generators, small | candidate | [D] |
| D81 | MAD benchmark | WS2 | 2610.11496 | free | not stated | 1.5M frames, 6 generators, full-body motion deepfakes + attribution; motion-aware niche | candidate | [D] |
| D82 | MIC-Bench | WS2 | 2609.33441 (UKPLab GitHub) | free | released (indic.) | 8,812 image-claim OOC consistency instances; synthetic inconsistencies may not match wild dist | candidate | [D] |
| D83 | NepOOC | WS2 | 2608.19212 | free | public (indic.) | 1,090 Nepali-English OOC pairs, 5 typologies; small, text-dominant; MULTILINGUAL relevance | candidate | [D] |
| D84 | WildFakeBench | WS2 | 2603.25423 (GitHub) | free | released (indic.) | 10k+ real micro-videos, expert attribution (manip/AIGC/cognitive/OOC-reuse); platform skew | candidate | [D] |
| D85 | Weibo26 | WS2 | 2609.36850 | free | not stated | image+text news, native+generated; Chinese-platform-specific | candidate | [D] |
| D86 | SLED-1400 | WS2 | 2606.07613 | free | study dataset (indic.) | 200 real/1,200 synthetic evidence photos, 6 T2I; civil-dispute object-centric scope | candidate | [D] |
| D87 | Audio Neural Codec-Spoof | WS2 | 2610.07216 (HF on acceptance) | free | not stated | existing ADD benches resynthesized through 7 neural codecs; proxy not true codec-generation | candidate | [D] |
| D88 | Soft-Bindings C2PA benchmark | WS2 | 2610.04151 (GitHub) | free | open-licence (audited) | 25 image/7 audio/7 video watermark configs + 35 fingerprint methods; openly-licensed models only | candidate | [D] |
P11 reconcile notes (honest): ⚑ D77 CCDF is the key benchmark (closest to fabricated disaster/accident
surveillance). NO fire/wildfire-specific synthetic corpus exists → documented GAP. Many sets are small/narrow
or "license not stated"/to-be-released → confirm before any use; FACE/AV sets (D79) consent-gated. All [D],
none selected; evaluation must be CROSS-GENERATOR + DEGRADED (in-distribution numbers overstate deployment).

## WS3 alerting / network traces (P12) — DISCOVERY-ONLY [D], licenses INDICATIVE
HONEST: the P12 reader (717e5ad8) surfaced mostly MEASUREMENT PAPERS, not released trace datasets; few
public alerting/mesh TRACE corpora exist. Staged candidates below are field-standard; most "parameters" for
the simulation come from the papers' reported curves (simulation_spec.md), not downloadable traces. All [D],
none selected.
| ID | Name | WS | Source | Cost | License | Content / known flaw | Status | Legend |
|----|------|----|--------|------|---------|----------------------|--------|--------|
| D89 | ns-3 LoRaWAN reference scenario/configs | WS3 | 2009.09503 / ns-3 lorawan module | free | GPLv2 (ns-3, indic.) | validated PDR/throughput vs load configs — SIM setup, not field traces | candidate | [D] |
| D90 | FAST-LoRa model/code | WS3 | 2507.23342 | free | not stated | fast analytical LoRaWAN model w/ quantified error vs reference sim | candidate | [D] |
| D91 | Meshtastic preset link-budget measurements | WS3 | 2605.17063 (42 datasets) | free | not stated | guided-link path-attenuation per SF preset; propagation-isolated, not deployment traces | candidate | [D] |
| D92 | Meshtastic campus RSSI/SNR logs | WS3 | 2605.20379 | free | not stated | field RSSI/SNR @ range (n=62 packets); very small | candidate | [D] |
| D93 | CRAWDAD wireless/mobility traces | WS3 | CRAWDAD (community archive) | free (request/EULA) | per-dataset EULA | real-world wireless + mobility traces for DTN/mesh sim parameterization; heterogeneous, dated | candidate | [D] |
| D94 | CAP alert feed archives (e.g. public CAP/alert aggregators) | WS3 | public CAP feeds | free | per-source (gov) | real CAP-formatted alert messages for message-design study; NOT a reachability dataset | candidate | [D] |
P12 notes (honest): no strong public "alert reachability" trace corpus found; the simulation is parameterized
from source-reported curves (simulation_spec.md §3). GAPS: Zigbee + ESP-NOW range/PDR, 802.11s stock-phone
background reception, and India NDMA/SACHET regulatory specifics — all TO-MEASURE/TO-VERIFY, none from a
dataset. Licenses INDICATIVE; several "not stated"; CRAWDAD per-dataset EULA. None selected.

## WS7b IoT build (P13) — calibration / fire-sensor / radio datasets, DISCOVERY-ONLY [D]
HONEST: NO fire-detection-LABELED public IoT sensor dataset surfaced (GAP → collect our own normal +
safe-stimulus logs per TEST_PROTOCOL). Candidates below are air-quality/calibration/radio sets usable to
develop compensation + measurement methodology, NOT fire-labeled. All [D], licenses INDICATIVE, none selected.
| ID | Name | WS | Source | Cost | License | Content / known flaw | Status | Legend |
|----|------|----|--------|------|---------|----------------------|--------|--------|
| D95 | AQ-SDR (Air Quality Sensor Data Repository) | WS7b | 2508.02724 (Veli) | free | not stated / "public when published" | 23,737 low-cost + reference stations; NOT yet released; air-quality not fire; label noise | candidate | [D] |
| D96 | SensEURCity (Antwerp) | WS7b | 2510.05646 | free | not stated (public) | 9 reference + 34 collocated low-cost sensors; single-city, NO2-centric, outdoor | candidate | [D] |
| D97 | SEA-HAZEMON distributed-node data | WS7b | 2407.09117 | free? | not visible | real SE-Asia haze low-cost nodes; haze not fire-labeled; preliminary | candidate | [D] |
| D98 | LoRa 2.4 GHz ToF ranging dataset (+T/RH) | WS7b | 2509.23125 | free | not stated | 3×3 grid/400 m²/3 weeks w/ T/RH covariates; localization not fire; small grid | candidate | [D] |
P13 notes (honest): the P6-staged D27-D30 (visual-smoke DB, UCI Gas-Sensor-Array-Drift, indoor-AQ-calibration
2610.11236, RESPIRE India CO) remain the most relevant for calibration/compensation development; D95-D98 add
breadth. Fire-labeled IoT sensor data = documented GAP, to be collected in the build (own normal-only +
safe-stimulus logs, TEST_PROTOCOL). None selected.

## WS4-ZS zero-shot fire/disaster (P14Z) — EVALUATION-ONLY candidates [D], all leakage/label-flawed
HONEST: NO clean, permissively-licensed CCTV-style zero-shot FIRE/SMOKE image benchmark surfaced. The fire sets
below carry DOCUMENTED leakage/label flaws → do NOT trust for zero-shot evaluation; curate an INTERNAL
leakage-free held-out hazard set instead. All [D], licenses INDICATIVE, none selected.
| ID | Name | WS | Source | Cost | License | Content / known flaw | Status | Legend |
|----|------|----|--------|------|---------|----------------------|--------|--------|
| D99 | WildFireCan-MMD | WS4-ZS | 2504.13231 | free? | not visible | Canadian wildfire X posts, 12 themes, image+text; FLAW: Canada-specific (authors stress non-transfer), social UGC not CCTV, custom model (84.48%) beats ZS | candidate | [D] |
| D100 | AI4Fire benchmark | WS4-ZS | 2610.10946 (GitHub) | free? | not visible | 5 wildfire tasks bare vs grounded; FLAW (author-reported): leakage (fire-danger column separates holdout), 67 aerial frames mislabeled from clipped thermal max; ZS loses to trivial baselines | candidate | [D] |
| D101 | California Wildfire PM2.5 | WS4-ZS | 2607.07951 | free? | not visible | 12-yr hourly PM2.5, 1,375 incidents, 79 sites; FLAW: time-series air-quality not imagery, extreme-event sparsity, ZS tail-unstable | candidate | [D] |
P14Z notes (honest): these are evaluation-reality references, NOT training sets for a CCTV ZS fire detector;
leakage/label flaws documented by their own authors. Build/curate an internal held-out set (D-011). None selected.

## WS5 RL simulators / environments / fire-spread data (P15) — DISCOVERY-ONLY [D]
HONEST: these are candidate SIMULATORS / DATASETS to REUSE for an RL environment (reuse-over-build); not fire-
detection training sets. Licenses/code availability TO VERIFY at build. All [D], none selected.
| ID | Name | WS | Source | Cost | License | Content / known flaw | Status | Legend |
|----|------|----|--------|------|---------|----------------------|--------|--------|
| D102 | PyroStack US wildfire dataset | WS5 | 2609.36315 | free? | not stated | 6994 fires 2012-24, multi-band hourly, 12-h progression; FLAW: US/Alaska only, not India | candidate | [D] |
| D103 | FireGen Monte-Carlo wildfire sim | WS5 | 2610.07431 | free? | not stated | N. California statistical fire-spread generator; FLAW: region-fit, statistical not physical | candidate | [D] |
| D104 | Ctrl-CWM controllable crowd world-model | WS5 | 2610.09438 | free? | not stated | model-based crowd sim w/ runtime user costs; FLAW: license/code availability unverified | candidate | [D] |
| D105 | cinemere/evacuation (Vicsek leader-follower) | WS5 | 2509.19972 (GitHub) | free | not stated (open) | small-scale evacuation env; FLAW: leader-guidance framing only | candidate | [D] |
P15 notes (honest): also FLARE behavioral code (2502.17701, GitHub) for human evacuate/stay realism; WS5
reuses crowd (D104/D105) + fire (D102/D103) + behavior, builds a thin Gymnasium/PettingZoo JAX wrapper (no
off-the-shelf disaster-evac env — GAP). None selected; all region/framing-limited.

## P18 feature-support datasets (discovery-only) [D]
| ID | Name | WS | Source | Cost | License | Content / known flaw | Status | Legend |
|----|------|----|--------|------|---------|----------------------|--------|--------|
| D106 | AQ-SDR low-cost air-quality sensor drift benchmark | WS7 | 2508.02724 | free? | not stated | 23,737 LCS + reference devices for drift/correction; FLAW: air-quality not fire; reference-free correction can explain away true events | candidate | [D] |
| D107 | ECA9 industrial-accident video (incl. Fire Detection) | WS4 | 2405.14506 | free? | not stated | semi-supervised accident video set; FLAW: industrial-accident framing, pseudo-label bias; not India | candidate | [D] |
P18 notes (honest): discovery-only, support the Wave-1 feature specs (F-15 drift correction, F-21 SSL); not
fire-primary training sets; none selected; all domain/region-limited.

## P19 India/deployment datasets (discovery-only) [D] — all license-UNVERIFIED, region/framing-limited
| ID | Name | WS | Source | Cost | License | Content / known flaw | Status | Legend |
|----|------|----|--------|------|---------|----------------------|--------|--------|
| D108 | Uttarakhand forest-fire imagery | DEPLOY/WS4 | 2410.06743 | free? | not stated | India forest-fire transfer-learning imagery; FLAW: region-limited, label/collection process unverified | candidate | [D] |
| D109 | WFDroneBench (risk maps + 7746 placement scenarios) | DEPLOY/WS4 | 2609.11829 | free? | not stated | wildfire sensor/drone-placement benchmark; FLAW: risk-map error dominates, synthetic scenarios | candidate | [D] |
| D110 | TRAQID + PM25Vision (regional AQI/vision) | DEPLOY/WS7 | 2605.16375 | free? | not stated | regional multimodal AQI; FLAW: region-limited, license unverified | candidate | [D] |
| D111 | UrduFake@FIRE2020 | DEPLOY/WS2 | 2207.12406 | free? | shared-task terms | Urdu fake-news 900/400 articles; FLAW: year domain-shift, SA-language only | candidate | [D] |
| D112 | GeoCoV19 multilingual geolocated tweets | DEPLOY/WS2 | 2005.11177 | free? | platform ToS (ID-only likely) | 524M+ tweets w/ inferred geo; FLAW: ToS/redistribution limits, inferred-geo noise, COVID-topic | candidate | [D] |
P19 notes (honest): discovery-only; agency/official statistics are NOT datasets here — verify at official
portals. None selected; all license-UNVERIFIED and region/framing/topic-limited; social-media sets likely
ID-only redistribution (ties P11 ToS). Dataset portal + license verification remains an OPEN backlog item.

## P23 addition — see DATASETS_CATALOGUE.md (D113-D164)
The P23 free-dataset hunt added 52 candidate datasets (D113-D164) grouped by workstream — fire/smoke CCTV,
satellite active-fire/burned-area, flood/SAR, landslide, InSAR/deformation, air-quality/PM2.5, seismic, crisis
social-media, deepfake — in the dedicated document DATASETS_CATALOGUE.md (with hosts/links, portal table, and
honest caveats). ALL are STATUS [D] (candidate, not selected); licenses INDICATIVE/UNVERIFIED; download links
NOT tested; deepfake sets D158-D160 are EULA/access-restricted; D140 MMLSv2 is Martian (out of scope). Indian
portals (Bhuvan/MOSDAC/VEDAS/NRSC/IMD/CWC/GSI) are JS-driven and flagged for MANUAL verification. §0.9A free-
only rule holds for any future STATUS=selected.
