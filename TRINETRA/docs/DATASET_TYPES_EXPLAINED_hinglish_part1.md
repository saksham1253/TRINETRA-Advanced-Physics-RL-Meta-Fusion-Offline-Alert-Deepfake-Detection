# TRINETRA (HIMKAVACH) — Dataset TYPES samjho (Hinglish) — PART 1

> **Yeh document kya hai?** Yeh TRINETRA (alt. naam HIMKAVACH) ke Himalayan disaster + fire
> early-warning project me jo **data-sources / dataset ke TYPES** use hote hain, unko ek smart
> junior ko samjhaane wale andaaz me explain karta hai. Hum yahan **har specific dataset nahi**
> ginwa rahe — woh kaam [04_DATASETS.md](<04_DATASETS.md>) + [04a_DATASETS.md](<04a_DATASETS.md>)
> karte hain, jahan poore **164 dataset IDs (D01–D164)** listed hain. Yeh file **"kis KISM ka data
> hota hai, woh banta kaise hai, kya naapta hai, kahan phasta hai"** — yeh samajh deti hai.
>
> **Kaise padhna:** pehle neeche wali **summary table** (saare 16 types) ek nazar dekho, phir
> TYPE-by-TYPE detail padho. Yeh **PART 1** hai → ismein **TYPES 1–8** full detail me hain.
> **TYPES 9–16** ka full content **[docs/DATASET_TYPES_EXPLAINED_hinglish_part2.md](<DATASET_TYPES_EXPLAINED_hinglish_part2.md>)**
> me hai (woh part abhi likha jaa raha hai / companion file hai).

---

## ⚠️ Honesty box — isko pehle padho, warna galatfehmi hogi

Yeh baatein poore project ki **ground truth** hain (`_CANON.md`), aur inhe soften mat karna:

- **Kuch bhi download nahi hua.** Is program me ek bhi dataset download nahi kiya gaya — sirf
  links / metadata / plans hain. (`_CANON.md`: *"No model has been trained and no dataset has been
  downloaded."*)
- **Koi EDA / statistics nahi.** Jo bhi size / `N` (count) neeche aata hai, woh **registry me jaisa
  recorded hai waisa** — humne naapa nahi. Bahut saare counts par khud registry ne **UNVERIFIED**
  ya "named" (kisi citing abstract se liya, owning page se nahi) likha hai.
- **Licenses mostly UNVERIFIED.** "source me X license recorded hai" ≠ "X license confirmed hai".
  Jab tak owning portal par verify na ho, sab **candidate** hi hai.
- **Koi performance number TRINETRA ki measurement nahi hai.** Jahan koi number dikhe aur source me
  recorded na ho — hum saaf likhenge: *"source me recorded nahi"* / *"verify karna padega"*.
  Number banana (fabricate) **mana hai**.
- Indian govt portals (Bhuvan / MOSDAC / VEDAS / NRSC / IMD / CWC / GSI) JS-driven hain → **manual
  verification** chahiye; abhi tak scrape nahi ho paaye.

Honesty labels (`_CANON.md §1`): `[CONFIRMED]`, `[LIKELY]`, `[HYPOTHESIS]`, `[INFEASIBLE]`.
Dataset-level facts yahan best-case `[LIKELY]`/`[UNVERIFIED]` hain, jab tak portal fetch na ho.

---

## 📊 Summary table — SAARE 16 TYPES (dono parts ko cover karti hai)

> Column meaning: **Type** = data kism; **Kaise banta/sensor** = kaise collect hota; **Example D-ID**
> = ek real registry ID (poori list ch04 me); **Hazard** = kis khatre ke liye; **WS/model** = kaunsa
> workstream / model consume karta; **Key limitation** = sabse bada catch.

| # | Type | Kaise banta / sensor | Example D-ID | Hazard | WS / model | Key limitation |
|---|------|----------------------|--------------|--------|------------|----------------|
| **1** | Optical / multispectral satellite EO | Sun-light reflectance, passive multispectral imager (Sentinel-2 MSI, MODIS) | D02, D06 | flood, land-context, GLOF-context | WS4/WS8 — optical-SAR fusion head, EO encoder | **Cloud cover** (monsoon me zyada), raat ko kuch nahi |
| **2** | SAR / radar satellite | Active C-band microwave backscatter (Sentinel-1) | D01 | monsoon flood, landslide deformation | WS1/WS8 — masked-InSAR SSL encoder | Speckle noise, interpret karna mushkil; SLC heavy |
| **3** | InSAR / ground-deformation | Do SAR passes ka phase-difference (interferometry) | D21 (↔D142), D141 | slow landslide/slope creep, GLOF precursor | WS1/WS8 — deformation-forecast head | Atmospheric artifacts + coherence loss (ped/snow) |
| **4** | Thermal / active-fire & burned-area satellite | Thermal-IR brightness temperature + FRP; burned-area change (MODIS/VIIRS) | D125, D126, D122 | wildfire / forest-fire | WS1a/WS1b/WS8 — fire context | Coarse pixel → chhoti aag miss; smoke/cloud block |
| **5** | Precipitation / weather & reanalysis | Spaceborne radar+microwave (GPM IMERG), gauges (IMD), reanalysis (ERA5-Land) | D03, D05, D47 | flood, landslide rainfall-trigger | WS1/WS3 — rainfall covariate + nowcast | Pahaad par kam certain; IMD often restricted/paid |
| **6** | DEM / topography | Radar/stereo elevation → slope, aspect, flow (SRTM, GLO-30) | D50, D51 | landslide, flood routing | WS1b — physics (FoS, Iverson, flow) | Static; resolution par slope-angle depend karta |
| **7** | Soil moisture | Passive microwave L-band radiometer (SMAP) | D04 | landslide antecedent-wetness | WS1 — antecedent prior | Bahut coarse (9–36 km) → steep terrain par weak |
| **8** | Glacier velocity / cryosphere | Optical/SAR feature-tracking (ITS_LIVE) | D07, D11 | GLOF (glacier acceleration) | WS8 — GLOF precursor head | Small-n events; 120 m res local lake miss karti |
| **9** | Hazard event catalogues / inventories | Human/remote-sensing compiled event records (point/polygon/CSV) | D08, D15, D22 | flood, landslide, GLOF labels | WS1/WS3/WS8 — labels/targets | Reporting-bias; non-exhaustive; counts UNVERIFIED |
| **10** | Flood ML benchmarks (imagery+labels) | Ready-made S1/S2(+DEM) chips + hand/CEMS labels | D17, D12, D134 | flood segmentation | WS1/WS8 — flood head | Native split leaky (D12), India event missing |
| **11** | Landslide ML benchmarks | Labelled optical/multi-sensor landslide patches | D18, D09, D20 | landslide detection/seg | WS1 — detection + PEFT | License/count UNVERIFIED; mixed-sensor shift |
| **12** | Ground CCTV / camera-network fire-smoke imagery | Fixed-tower / CCTV RGB cams, bbox annotations | D36, D37, D35 | fire/smoke detection | WS4 — FireSmokeNet | Europe/US-centric → India domain shift |
| **13** | Aerial/UAV & thermal fire imagery + fire-spread sims | Drone RGB+IR, 360° video, WRF-SFIRE/SPARK sims | D42, D43, D34 | fire spread/detection | WS1a/WS4/WS5 — spread models | Domain-shift vs ground CCTV; sims region-fit |
| **14** | Low-cost IoT / air-quality / gas-sensor TS | MOX e-nose, PM2.5/CO nodes, calibration logs | D28, D30, D96 | fire smoke/gas (IoT node) | WS7a/WS7b — sensor compensation | Fire-LABELED IoT data = GAP; drift normal |
| **15** | Crisis social-media & deepfake/forensic media | Tweets+images, OOC pairs, deepfake video/audio | D16, D77, D68 | misinformation (advisory) | WS2/WS3 — low-trust channel | Low-trust (Rule 19); India-lang GAP; EULA-gated |
| **16** | Support corpora: SSL pretrain + seismic + hydro-discharge + net/RL-sim | Unlabeled EO (SSL4EO), waveforms, discharge, LoRa traces | D10, D148, D53 | pretraining / sim / context | WS1/WS3/WS5/WS8 | Europe-only / request-based / restricted |

*(Types 1–8 ka full breakdown is file me neeche. Types 9–16 part 2 me.)*

---

# TYPE 1 — Optical / multispectral satellite EO (Sentinel-2, MODIS)

**Example D-IDs:** **D02 Sentinel-2 MSI** `[V] selected`, **D06 MODIS** `[V] selected`.
(SSL corpora D10/D13/D14 bhi optical hain, par woh Type-16 support me aate hain.)

### (a) Yeh hota kya hai
Optical EO ka matlab — satellite kisi apni roshni nahi phenkti; woh **Sun ki roshni** jo zameen,
paani, patti, baadal se **reflect** hoti hai usko **multiple spectral bands** me record karti hai.
"Multispectral" ka matlab — ek hi scene ko kai alag-alag wavelength windows (bands) me capture
karna, taaki hum aisi cheezein "dekh" saken jo normal RGB me nahi dikhti (jaise vegetation ka
health, paani ki moisture).

### (b) Kaise collect hota hai (sensor / platform / orbit / band)
- **Passive sensor** — khud light generate nahi karta, Sun par depend karta hai (isliye **raat ko**
  optical kaam nahi karta aur **baadal ke neeche** andha ho jaata hai).
- **Sentinel-2 (D02)**: ESA/Copernicus ka MSI (MultiSpectral Instrument), **13-band** optical sensor,
  Sun-synchronous polar orbit. Registry me resolution recorded: **10 / 20 / 60 m** band-wise.
- **MODIS (D06)**: NASA Terra/Aqua platform, LST/NDVI/snow products deta hai, resolution
  **250 m – 1 km**, data **2000–present**.
- Measurement physics: har band ek wavelength-range ka reflectance (0–1 fraction, ya scaled
  reflectance) deta hai. Band math se humein **indices** milte hain:
  - **NDVI** (vegetation): (NIR − Red)/(NIR + Red) — patti healthy to NIR high → NDVI up.
  - **NDWI** (open water): green aur NIR ka ratio — paani NIR absorb karta → NDWI up.
  - **NDMI** (moisture): NIR aur SWIR ka ratio — plant/soil moisture ka proxy.

  > ⚠️ NDVI/NDWI/NDMI ke **exact band formulas** general EO knowledge hain; project source me sirf
  > "13-band 10/20/60 m" recorded hai, specific band-center wavelengths registry me recorded nahi —
  > build time par confirm.

### (c) Kya measure karta + units + resolution + coverage
- **Measure:** per-band surface reflectance → derived indices (NDVI/NDWI/NDMI unitless, −1..+1).
- **Spatial res:** D02 10/20/60 m; D06 250 m–1 km.
- **Temporal:** dono **continuous mission** — fixed benchmark nahi; hum apne **event-indexed cubes**
  khud banate hain (04a reminder: D01–D07 continuous missions hain, "N / native split" n/a).
- **Spectral:** D02 = 13 bands; D06 ke LST/NDVI/snow products.
- **Coverage:** global, incl. **India / Himalaya**.

### (d) Strengths + limitations
- **Strength:** rich spectral info → water vs vegetation vs barren asani se alag; free & open
  (Copernicus / NASA open); long archive (D06 2000–present).
- **Limitation — CLOUD:** monsoon me Himalaya par **cloud cover** sabse bada dushman hai — jab aapko
  flood map chahiye, tabhi baadal scene chhupa deta hai. Isi liye design me **optical–SAR fusion**
  (DC-09) hai: cloud ho to SAR (Type-2) par shift karo.
- **Limitation — revisit/night:** passive hai → raat ko blind; revisit gap me teji se badalti flood
  front miss ho sakti hai.
- **Access:** free-with-registration — **Copernicus Data Space** (D02), **NASA Earthdata** (D06)
  account **jaldi** bana lo (registry: registration-needed early action).

### (e) TRINETRA me kyun / kahan
- **Hazard:** flood extent + burned-area + land-context; D06 se GLOF/seasonal **snow-cover/LST**
  context (WS8).
- **WS/model:** D02 → **optical–SAR fusion flood head + EO encoder** (ch05/06/09); D06 →
  snow/LST context feature (ch06).
- **Example D-ID:** **D02** (primary optical stream), **D06** (seasonal context).

### (f) Leakage / split handling
Optical cubes bhi **spatial+temporal block CV** se split hote hain — buffer D01 jaisa (tile + time
block, buffer ≥ InSAR range, DC-01). Reason: random CV geospatial me skill **overstate** karta hai;
spatial-block CV mandatory — poora protocol **ch12** me (triangulated: arXiv 2608.12422, 2608.22293,
2610.08227).

---

# TYPE 2 — SAR / radar satellite (Sentinel-1 C-band)

**Example D-ID:** **D01 Sentinel-1 SAR** `[V] selected` — registry me "the single most important
stream for monsoon floods + landslide deformation (SAR-first)".

### (a) Yeh hota kya hai
SAR = **Synthetic Aperture Radar**. Yeh **active** sensor hai — khud microwave pulse bhejta hai aur
jo wapas reflect (backscatter) hota hai usko record karta hai. Kyunki apni energy use karta hai,
isliye **din-raat** aur **baadal/baarish ke aar-paar** dono me kaam karta hai (all-weather). Yahi
iska killer feature hai — monsoon me jab optical andha hota hai, SAR dekhta rehta hai.

### (b) Kaise collect hota hai
- **Sentinel-1 (D01)**: ESA/Copernicus, **C-band** radar (~5.6 cm wavelength class), polar orbit,
  continuous mission.
- **Backscatter physics:** radar pulse surface se takराता hai; **smooth paani** energy ko door
  reflect kar deta hai (sensor ki taraf kam → paani **dark/low backscatter** dikhता hai), jabki
  **rough/urban/vegetation** zyada backscatter karta hai. Isi contrast se flood-water map banti hai.
- **GRD vs SLC** (ye zaroor samajh — budget ka faisla isi par):
  - **GRD** (Ground Range Detected): sirf **amplitude/intensity**, phase discard. Halka, flood
    mapping ke liye kaafi.
  - **SLC** (Single Look Complex): amplitude **+ phase** dono rakhta hai — **InSAR** (Type-3) ke
    liye zaroori, par bhari/compute-heavy.
  - Registry decision: **"SLC interferometry heavy → GRD + learned-coherence proxy (D21 /
    arXiv 2606.07374) use karo"** taaki Kaggle budget me raho.

### (c) Kya measure karta + units + resolution + coverage
- **Measure:** radar backscatter coefficient **σ⁰** (sigma-nought, dB me express hota hai).
- **Spatial res:** registry: **~10 m** (GRD/SLC).
- **Temporal:** continuous mission (hum event cubes banate hain).
- **Coverage:** global incl. India/Himalaya.

### (d) Strengths + limitations
- **Strength:** all-weather, cloud-penetrating, din-raat → monsoon flood ke liye #1.
- **Limitation — speckle:** SAR me **speckle noise** (salt-and-pepper) hota hai → interpret karna
  optical se mushkil; preprocess me optional speckle filter (par learned-coherence ke liye raw
  rakhna). (04a F12: apply-orbit → noise removal → radiometric cal σ⁰ → optional speckle → RTC
  geocode → dB + normalize; augment sirf flips/rot90, **no photometric jitter** SAR par.)
- **Limitation — compute:** SLC-based InSAR heavy → GRD + proxy.
- **Access:** free-with-registration (Copernicus Data Space; bulk/STAC/openEO ke liye account).

### (e) TRINETRA me kyun / kahan
- **Hazard:** monsoon **flood mapping** + **landslide/ground deformation** (WS1/WS8).
- **WS/model:** **masked-InSAR SSL encoder + deformation-forecast head** (ch05/06). SAR ko labels
  khud se nahi milte — labels hazard inventories (D08/D15/D22) ya flood benchmarks se aate hain.
- **Example D-ID:** **D01**.

### (f) Leakage / split handling
04a D01: **tile + time block CV, buffer ≥ InSAR range (DC-01)** — `[HYPOTHESIS protocol — ch12]`.
Matlab: nazdeeki tiles aur overlapping time windows ko train/test me alag nahi hone dena warna
model "cheat" kar lega. Full protocol **ch12**.

---

# TYPE 3 — InSAR / ground-deformation (interferometry)

**Example D-IDs:** **D21 Thalia** `[D] candidate` (↔D142), **D141 Hephaestus** `[D] candidate`.
(Core SAR stream D01 ki SLC se bhi InSAR ban sakti hai.)

### (a) Yeh hota kya hai
InSAR = **Interferometric SAR**. Idea: ek hi jagah ki **do (ya zyada) SAR passes** ka **phase**
compare karo. Agar ground thoda bhi hila (slope creep, subsidence, uplift), to radar signal ka
travel-path badalta hai → phase me difference aata hai. Us phase-difference se hum **millimeter-level
displacement** map kar sakte hain. Yeh slow-moving landslide / slope instability ko aag lagne se
pehle "sunne" ka tareeka hai.

### (b) Kaise collect hota hai
- **Platform:** wahi SAR satellites (e.g. Sentinel-1 **SLC** products — phase chahiye, isliye GRD
  kaam nahi aayega, SLC chahiye).
- **Measurement physics:** interferogram = pass-1 aur pass-2 ke complex SLC ka phase-difference.
  Phase ko unwrap karke line-of-sight displacement nikaalte hain. **Coherence** = do passes ke beech
  signal kitna "match" karta hai (0..1): high coherence → reliable deformation; low coherence →
  bekaar (ped hilte, snow, time gap).
- **D21 Thalia:** registry — "38 InSAR datacubes, 7 yr, InSAR + topo + **atmospheric** (artifact
  confound) + expert deformation labels + text". Yeh InSAR-anomaly task ka closest open analogue hai
  (par **VOLCANIC** domain → transfer).
- **D141 Hephaestus:** registry — "S1 interferograms (annotated), **19,919 ifg / 216,106 patches /
  44 volcanoes**". Yeh counts registry me recorded hain par `[D]` discovery-level — verify karna
  padega.

### (c) Kya measure karta + units + resolution + coverage
- **Measure:** line-of-sight **displacement** (mm scale) + **coherence** (0–1 unitless).
- **Res/coverage:** underlying SAR (C-band ~10 m) par depend. D21 = 38 datacubes 7-year; D141 ke
  counts upar — **sab source-reported, humne naapa nahi**.
- Important honesty: koi actual mm-displacement number humne **measure nahi kiya**; "mm-level" ek
  method capability hai, project ka measured result nahi.

### (d) Strengths + limitations
- **Strength:** slow deformation ka **early precursor** — landslide/slope creep aur GLOF-prone
  moraine dam weakening ko weeks/months pehle pakad sakta hai.
- **Limitation — atmosphere:** troposphere/ionosphere phase me **artifact** daalti hai (D21 me yeh
  "artifact confound" explicitly recorded) → galat deformation jaisa dikh sakta hai.
- **Limitation — coherence loss:** vegetation, snow, lambe time-gap → coherence gir jaati hai, aur
  Himalaya me yeh dono bade problem hain.
- **Limitation — compute + domain:** SLC heavy (isliye D01 note me GRD + **learned-coherence proxy
  2606.07374** suggest kiya); aur D21/D141 dono **volcanic** domain → hamara landslide/GLOF task
  transfer hai, direct match nahi.
- **Access:** D21/D141 repo/Zenodo — license `per repo (verify)` / recorded, **UNVERIFIED**.

### (e) TRINETRA me kyun / kahan
- **Hazard:** slow landslide/slope deformation + GLOF precursor (moraine-dam stress) — WS1/WS8.
- **WS/model:** D01 ki SLC/coherence → **masked-InSAR SSL encoder + deformation-forecast head**
  (ch06). D21 InSAR-anomaly ka transfer reference.
- **Example D-ID:** **D21** (closest open InSAR analogue), **D141** (large interferogram set).

### (f) Leakage / split handling
InSAR cubes bhi **tile + time block CV, buffer ≥ InSAR range (DC-01)** — spatial autocorrelation
InSAR me strong hai, isliye buffer **range jitna** rakhna zaroori. Volcanic → Himalayan transfer
= **domain-shift risk**, ch12/22 me registered. Full protocol **ch12**.

---

# TYPE 4 — Thermal / active-fire & burned-area satellite

**Example D-IDs:** **D125 MOD14/VNP14 fire masks** `[D] candidate`, **D126 CaBuAr (burned areas)**
`[D] candidate`, **D122 USTC_SmokeRS (MODIS 3-band)**, **D123 Landsat_Smk**, **D128 EFFIS hotspot**
(MODIS+VIIRS+S3). Core D06 MODIS bhi LST (thermal) products deta hai.

### (a) Yeh hota kya hai
Thermal / active-fire data **garmi** par based hai, visible light par nahi. Har garam cheez
thermal-infrared (TIR) emit karti hai; aag ki jagah par TIR signal bahut strong ho jaata hai.
Satellite us TIR se **brightness temperature** nikaalti hai aur "yahan active fire pixel hai"
flag karti hai. **Burned-area** products thoda alag — woh aag ke **baad** jhulsi zameen (pre/post
change) map karte hain.

### (b) Kaise collect hota hai
- **Sensors:** **MODIS** (Terra/Aqua) aur **VIIRS** thermal bands active-fire detection karte hain
  (registry me VIIRS alag standalone selected mission nahi; woh **D125 MOD14/VNP14** aur **D128
  EFFIS** ke andar MODIS+VIIRS crossref ke roop me recorded hai).
- **Measurement physics:**
  - **Brightness temperature (BT):** TIR radiance ko Planck-law se temperature me convert karte hain
    (Kelvin). Fire pixel me mid-IR channel ki BT background se bahut upar jaati hai → detection.
  - **FRP (Fire Radiative Power):** fire ki radiative output (megawatts, MW) — aag ki intensity ka
    proxy. (⚠️ koi actual BT/FRP number project source me recorded **nahi** — concept samjhao,
    number mat banao, "verify karna padega".)
  - **Burned-area:** D126 CaBuAr jaise sets **S2 L2A pre/post** image pair lete hain aur change se
    jhulsa area nikalte hain.

### (c) Kya measure karta + units + resolution + coverage
- **Measure:** active-fire mask (binary/confidence), BT (K), FRP (MW), burned-area polygons.
- **Res:** MODIS thermal coarse (D06 250 m–1 km class; fire products aksar ~1 km); D126 S2 (10/20 m
  class, California since 2015); D122 MODIS 3-band; D123 Landsat 6-band.
- **Coverage:** D125 multi-region; D126 California; D128 Europe (EFFIS). India-specific standalone
  active-fire selected mission registry me nahi (yeh ek **gap** → portal verify).

### (d) Strengths + limitations
- **Strength:** aag ko din-raat thermally detect karta; FRP se intensity ranking; burned-area se
  post-event assessment.
- **Limitation — coarse pixel:** ~1 km MODIS pixel me **chhoti early-stage aag miss** ho jaati hai
  (early-warning ke liye yahi dukh — hum chaahte hain aag chhoti ho tabhi pata chale → isi liye
  ground CCTV Type-12 + IoT Type-14 complement karte hain).
- **Limitation — smoke/cloud:** mota smoke/cloud TIR ko bhi disturb karta hai.
- **Limitation — license/region:** zyadatar `[D]` discovery-only, licenses recorded par UNVERIFIED;
  D126 California, D128 Europe → India domain-shift.

### (e) TRINETRA me kyun / kahan
- **Hazard:** wildfire / forest-fire detection + burned-area context.
- **WS/model:** WS1a (fire-physics validation context), WS1b/WS8 (fire raster context). Satellite
  thermal yahan **regional/context** signal hai; actual early detection ground cams + IoT par depend
  karti hai (C1 offline-first path).
- **Example D-ID:** **D125** (MOD14/VNP14 fire masks), **D126** (burned area).

### (f) Leakage / split handling
Fire raster/burned-area sets me **region-block + temporal-block CV** chahiye (same aag ki aas-paas
ki tiles train+test me nahi). Multi-sensor (MODIS+VIIRS+S2) mix karte waqt **cross-domain leakage**
ka khatra (04 note: aerial/satellite/360° mix karna risky). Full protocol **ch12**.

---

# TYPE 5 — Precipitation / weather & reanalysis

**Example D-IDs:** **D03 GPM IMERG** `[V] selected`, **D05 ERA5-Land** `[V] selected`,
**D47 IMD rainfall/gridded** `[D] candidate` (⚠ often restricted/paid), **D49 CHIRPS** `[D]`,
**D48 NASA GPM IMERG** (↔D03 re-listing).

### (a) Yeh hota kya hai
Rainfall hi Himalaya me flood aur rainfall-triggered landslide ka **primary trigger** hai. Yeh type
teen flavours me aata hai:
1. **Satellite precipitation** (space se baarish estimate) — GPM IMERG.
2. **Ground gauges** (zameen par rain-gauge measurements) — IMD.
3. **Reanalysis** (model + observations ka blend, poora weather state) — ERA5-Land.

### (b) Kaise collect hota hai
- **GPM IMERG (D03):** GPM core observatory ka **dual-frequency precipitation radar + passive
  microwave** constellation; multi-satellite merge karke global rainfall grid banta hai. Registry:
  **0.1°, half-hourly, 2000–present (V07, ab 90°N–S)**.
- **IMD (D47):** India Meteorological Department ke **station gauges + gridded** rainfall. Yeh zameeni
  truth ke sabse kareeb — par **data policy often restricted/paid** (registry: central access risk).
- **ERA5-Land (D05):** ECMWF/Copernicus C3S **reanalysis** — numerical weather model observations ke
  saath assimilate karke consistent hourly state deta hai. Registry: **0.1° (~9 km), hourly,
  1950–present**, **CC-BY** (DOI 10.24381/cds.e2161bac) — in sab me **sabse clean license** (link
  2026-10-10 par HTTP 200 verify hua).

### (c) Kya measure karta + units + resolution + coverage
- **Measure:** precipitation rate (mm/hr) / accumulation (mm); ERA5-Land poora met-forcing set
  (temp, wind, etc.).
- **Res:** D03 0.1° half-hourly; D05 0.1°(~9 km) hourly; D47 station+grid (India).
- **Coverage:** D03 global 90°N–S; D05 global 1950–present; D47 India-only.

### (d) Strengths + limitations
- **Strength:** continuous, free (D03/D05), long archive → rainfall trigger + antecedent + nowcast.
- **Limitation — pahaad par kam certain:** registry explicitly: NASA kehta hai precipitation
  **mountains par less certain** hai aur **V07 snowfall-deficient** → Himalayan IMERG ko **noisy
  covariate** treat karo (CR-08 / TSFM-covariate-noise concern).
- **Limitation — smoothing:** ERA5-Land ki **9 km** Himalayan topography ko smooth kar deti hai →
  downscale karo ya **boundary forcing** ki tarah use karo (HEC-RAS, arXiv 2507.15614).
- **Limitation — access:** **IMD (D47) often restricted/paid** — Himalayan rainfall-threshold
  calibration ka central access risk; registry me `candidate / cost varies`, kabhi `selected` nahi.
- **Access:** D03/D04/D06/D07 ke liye **NASA Earthdata login**; D05 ke liye **Copernicus CDS account
  + API key** — jaldi bana lo.

### (e) TRINETRA me kyun / kahan
- **Hazard:** flood + rainfall-triggered landslide (Caine intensity–duration threshold physics isi
  rainfall par chalti hai, `_CANON.md §4`).
- **WS/model:** D03/D05/D04 → **rainfall/antecedent covariates + nowcasting** (ch06/08). WS1/WS3.
- **Example D-ID:** **D03 IMERG** (trigger/nowcast covariate), **D05 ERA5-Land** (met forcing).

### (f) Leakage / split handling
Covariates (D03/D05/D04) ko **temporal block CV, monsoon-season held-out** se split karte hain —
matlab test monsoon alag season/year ka ho taaki model "memorise" na kare. Full protocol **ch12**.

---

# TYPE 6 — DEM / topography (slope, aspect)

**Example D-IDs:** **D50 SRTM DEM** `[D] candidate` (30/90 m, public domain USGS), **D51 ALOS
AW3D30 / Copernicus GLO-30 DEM** `[D] candidate` (30 m). GLO-30 D17 GEOID-Flood ke andar bhi feed
hoti hai.

### (a) Yeh hota kya hai
DEM = **Digital Elevation Model** — har pixel ki **height** (meters above sea level). Isse derive
hote hain **slope** (dhaal kitni steep), **aspect** (dhaal kis disha me), curvature, flow-direction,
flow-accumulation. Yeh **static terrain** data hai (zameen roz nahi badalti), par yahi disaster
**physics ko drive** karta hai.

### (b) Kaise collect hota hai
- **SRTM (D50):** Shuttle Radar Topography Mission — **radar interferometry** se banaya gaya DEM,
  **30/90 m**, public domain (USGS).
- **ALOS AW3D30 / GLO-30 (D51):** JAXA/Copernicus **30 m** DEM (optical stereo / radar derived),
  attribution license.
- **Measurement physics:** DEM se slope-angle β = terrain gradient ka arctan; aspect = gradient
  direction. Yeh angles seedhe physics models me jaate hain.

### (c) Kya measure karta + units + resolution + coverage
- **Measure:** elevation (m), derived slope (degrees/%), aspect (degrees), flow metrics.
- **Res:** 30 m (GLO-30/AW3D30) ya 30/90 m (SRTM).
- **Coverage:** near-global; India/Himalaya covered. **Static** (ek-baar grid, time-dimension nahi).

### (d) Strengths + limitations
- **Strength:** free/public domain; physics ke liye indispensable — bina slope ke landslide model
  chal hi nahi sakta.
- **Limitation — resolution:** slope-angle **DEM resolution par depend** karta hai; 30 m DEM steep
  Himalayan micro-topography (chhoti cliff/gully) ko smooth kar deta hai → derived slope galat ho
  sakta hai. Isliye jahan possible higher-res chahiye.
- **Limitation — static:** terrain change (post-earthquake, post-landslide) ko purani DEM capture
  nahi karti → periodic refresh.

### (e) TRINETRA me kyun / kahan
- **Hazard:** landslide (slope stability) + flood routing (paani kahan behega).
- **WS/model:** WS1b geo-physics — **infinite-slope Factor of Safety**, **Iverson (2000)** transient
  pressure head (bug-guard **D1 = D0/cos²β ONLY**), **Caine** rainfall threshold — in sab me DEM se
  nikla **slope-angle β** central input hai (`_CANON.md §4`). Flood me DEM paani ka flow-direction
  deta hai.
- **Example D-ID:** **D50 SRTM**, **D51 GLO-30/AW3D30**. GLO-30 **D17 GEOID-Flood** ke andar
  bi-temporal S1+S2 ke saath DEM channel hai.

### (f) Leakage / split handling
DEM khud label nahi deta, par ek bada **leakage trap** hai: naïve terrain-only model DEM-features par
train-test overlap se ROC-AUC inflate kar deta hai. `_CANON.md §6` + ch04 §6 ka core verdict yahi
hai — **naïve terrain ROC-AUC ~0.90 → spatial-CV me 0.76/0.71/0.54 tak girta** (arXiv 2608.12422).
Isliye DEM-features ko bhi **spatial-block CV** me daalna, buffer ke saath. Full protocol **ch12**.

---

# TYPE 7 — Soil moisture (SMAP passive microwave L-band)

**Example D-ID:** **D04 SMAP soil moisture (NASA NSIDC)** `[V] selected`.

### (a) Yeh hota kya hai
Soil moisture = zameen ke upari layer me kitna paani hai. Yeh **antecedent wetness** ka direct
indicator hai — agar mitti pehle se saturated hai, to thodi aur baarish bhi landslide/flood trigger
kar sakti hai. Isliye yeh "pre-condition" signal hai, trigger nahi.

### (b) Kaise collect hota hai
- **SMAP (D04):** NASA ka **Soil Moisture Active Passive** mission. Ab mainly **passive microwave
  L-band radiometer** chalu hai (active radar early fail ho gaya tha — yeh general mission fact; L-band
  passive hi project-relevant hai).
- **Measurement physics:** geeli mitti ka **dielectric constant** sookhi se bahut zyada hota hai →
  L-band microwave emission (brightness temperature) badalti hai → usse soil moisture retrieve karte
  hain. L-band isliye kyunki woh vegetation/upari layer ke neeche thoda penetrate karta hai.

### (c) Kya measure karta + units + resolution + coverage
- **Measure:** volumetric soil moisture (m³/m³, i.e. fraction).
- **Res:** registry: **~9–36 km** (coarse).
- **Temporal:** 2015–present (continuous).
- **Coverage:** global.

### (d) Strengths + limitations
- **Strength:** free (NASA open), global, consistent antecedent-wetness proxy.
- **Limitation — coarse:** **9–36 km pixel steep Himalayan terrain par weak** — ek SMAP pixel me poori
  valley + ridge aa jaati hai, local slope ki wetness capture nahi hoti. Registry explicitly: *"use as
  a regional antecedent-wetness prior, NOT a local trigger."*
- **Access:** NASA Earthdata login chahiye.

### (e) TRINETRA me kyun / kahan
- **Hazard:** rainfall-triggered **landslide** (antecedent wetness pre-condition).
- **WS/model:** WS1 — **antecedent-wetness covariate** geo-physics stack me (ch06). Iverson transient
  pressure-head model me initial wetness state is tarah ke prior se inform hota hai.
- **Example D-ID:** **D04**.

### (f) Leakage / split handling
Regional covariate hai → **temporal block CV** (monsoon-season held-out), D03/D05 ke saath same
policy. Coarse hone ki wajah se spatial autocorrelation bhi high → block buffer. Full protocol
**ch12**.

---

# TYPE 8 — Glacier velocity / cryosphere (ITS_LIVE feature-tracking)

**Example D-IDs:** **D07 ITS_LIVE glacier velocity** `[V] selected`, **D11 GLOFNet** `[V*] candidate`
(S2+ITS_LIVE+MODIS, Shisper/Karakoram). Label side: **D15 HMAGLOFDB** (GLOF events), **D52 ICIMOD
HKH glacial-lake/GLOF**.

### (a) Yeh hota kya hai
Cryosphere = baraf/glacier wala data. Yeh TRINETRA ke sabse special hazard — **GLOF (Glacial Lake
Outburst Flood)** — ke liye hai. GLOF tab aata hai jab glacier ke paas bana lake achanak phoot jaata
hai aur neeche basti par flood aa jaata hai. **Glacier velocity** (glacier kitni teज khisak raha hai)
ek **precursor signal** hai — glacier acceleration GLOF se pehle dikh sakti hai.

### (b) Kaise collect hota hai
- **ITS_LIVE (D07):** NASA/JPL (MEaSUREs). Technique = **feature-tracking** — do optical/SAR images ke
  beech glacier surface ke features (crevasses, patterns) ko match karke unki **movement** nikalte hain.
  Registry (04a F3): method **autoRIFT feature-tracking — Gardner et al. 2018** [link-verified
  2026-10-10].
- **Measurement physics:** image pair → cross-correlation se pixel displacement → divide by time-gap
  → surface velocity (m/year ya m/day).
- **D11 GLOFNet:** multimodal — **S2 + ITS_LIVE + MODIS** Shisper/Karakoram ke liye; arXiv 2510.10546
  (paper CC BY-NC-ND 4.0, par **data download URL + license UNVERIFIED** → candidate).

### (c) Kya measure karta + units + resolution + coverage
- **Measure:** glacier **surface velocity** (speed + direction).
- **Res:** registry: **120 m**.
- **Temporal:** **1985–present** (continuous; V1 pre-Apr-2023 ko Earthdata login chahiye, newer cloud
  data open).
- **Coverage:** global incl. **High Mountain Asia** (Indian Himalaya relevance).

### (d) Strengths + limitations
- **Strength:** direct GLOF-precursor physical signal (glacier acceleration), long archive, free.
- **Limitation — resolution:** **120 m** chhoti glacial lake ya thin moraine-dam feature ko miss kar
  sakti hai → S2 optical (lake area) + MODIS ke saath fuse karna padta hai (yahi D11 GLOFNet karta).
- **Limitation — small-n:** GLOF events **thin in-region** — D15 HMAGLOFDB me registry "766 GLOFs"
  likha par woh **UNVERIFIED** (secondary dashboard; GitHub/ICIMOD par confirm karna). Chhote labels →
  model train karna aur eval karna dono mushkil → **domain-shift / transfer** unavoidable (ch12/22
  risk).
- **Access:** NASA Earthdata login (V1); D11 ka download + license UNVERIFIED.

### (e) TRINETRA me kyun / kahan
- **Hazard:** **GLOF** (glacier acceleration → outburst precursor).
- **WS/model:** WS8 — **GLOF precursor (velocity) head**, D15 HMAGLOFDB labels + ITS_LIVE +
  arXiv 2608.12422 (589-event re-study) ke saath paired (ch06).
- **Example D-ID:** **D07 ITS_LIVE** (velocity precursor), **D11 GLOFNet** (multimodal GLOF),
  **D15 HMAGLOFDB** (outburst labels).

### (f) Leakage / split handling
GLOF (D07, D15, D11) ke liye registry rule: **leave-one-basin-out** CV — poora ek glacial basin
test me rakho, baaki train. Kyunki ek basin ke events aapas me correlated hote hain, basin-mix
leakage deta. Small-n hone se **transfer stress** (global D12/D13/D26/D20 par train → Himalayan
subset par test) mandatory, aur yeh explicitly **domain-shift risk** register hai. Baselines pehle:
persistence (C-03) + GBDT (C-02) + tuned U-Net. Full protocol **ch12**.

---

## PART 1 ka ant — aage kya

Yeh the **TYPES 1–8** (satellite optical, SAR, InSAR, thermal/active-fire, precipitation, DEM,
soil-moisture, glacier/cryosphere). **TYPES 9–16** —
hazard inventories, flood/landslide ML benchmarks, ground CCTV fire-smoke, aerial/UAV+thermal +
fire-spread sims, low-cost IoT/air-quality sensors, crisis-media + deepfake forensic, aur support
corpora (SSL pretrain / seismic / hydro-discharge / network+RL-sim) — **PART 2** me hain:
**[docs/DATASET_TYPES_EXPLAINED_hinglish_part2.md](<DATASET_TYPES_EXPLAINED_hinglish_part2.md>)**.

Reminder dobara: **kuch download nahi hua, licenses UNVERIFIED, koi number measure nahi kiya** —
specific 164 datasets [04_DATASETS.md](<04_DATASETS.md>) + [04a_DATASETS.md](<04a_DATASETS.md>) me,
split/leakage ka full protocol **ch12** me.
