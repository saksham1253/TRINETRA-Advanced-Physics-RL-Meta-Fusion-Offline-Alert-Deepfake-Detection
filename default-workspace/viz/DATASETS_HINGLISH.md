# TRINETRA / HIMKAVACH — DATASETS, Hinglish mein samjhaaye

> **Ye document kya hai?** Humne system ke liye jitne real-world datasets dhoonde + shortlist kiye,
> unka **saaf-saaf Hinglish explanation** — har dataset kya hai, kyun chahiye, kahaan se milta hai,
> licence kya hai, aur kitna *bharosemand* (verified) hai.
>
> **Imaandaari (zaroori baat):** niche jo bhi likha hai wo datasets **registry mein hai** —
> yaani humne inhe *dhoonda, verify kiya aur plan banaya*. Humne inme se **kuch bhi download ya
> train nahi kiya**. Jo bhi model/detection video mein dikhta hai wo ILLUSTRATIVE hai.
> Ye document sirf "data ka plan" hai, "data chal raha hai" nahi.

---

## Pehle 3 cheezein samajh lo (legend)

**Verification tag — kitna pakka hai:**
| Tag | Matlab |
|-----|--------|
| **[V]** | **Verified** — link, licence, access sab khud check kiya, pakka sahi hai |
| **[V*]** | Mostly verified — ek-aadh fact (jaise exact count ya licence) abhi confirm karna baaki |
| **[D]** | **Discovery-only** — mil gaya hai, par abhi poori tarah verify nahi kiya |

**Status — shortlist mein hai ya nahi:**
- **selected** = pakka isko use karenge (core plan ka hissa)
- **candidate** = accha option hai, zaroorat padi to lenge

**Workstream (WS) — kaunsa engine use karega:**
WS1 = physics/landslide-flood core · WS2 = social-media · WS3 = alert/dissemination ·
WS4 = optical/scene vision · WS8 = EO anomaly / glacier-GLOF.

**Total: 26 datasets** → **13 selected + 13 candidate** · **12 [V] · 5 [V*] · 9 [D]**.

---

## 1) Baarish aur Mausam ka data 🌧️ (landslide/flood ka trigger)

Ye batate hain "kitni baarish hui, zameen kitni geeli hai" — physics engine (WS1) ka main input.

| ID | Dataset | Ek line mein | Licence | Status · Tag |
|----|---------|--------------|---------|--------------|
| **D03** | **GPM IMERG** (NASA) | Satellite se **baarish** — 0.1°, har aadhe ghante, 2000 se abhi tak. Caine rain-threshold ka input. | NASA open | selected · **[V]** |
| **D05** | **ERA5-Land** (ECMWF) | Mausam ka **reanalysis** — 9 km, har ghante, 1950 se. Temperature/rain/soil ki history. | CC-BY | selected · **[V]** |
| **D04** | **SMAP** (NASA) | **Mitti ki nami** (soil moisture) — 9–36 km, 2015 se. Slope kitni saturated hai (FS ke liye). | NASA open | selected · **[V]** |

---

## 2) Satellite se Zameen Dekhna 🛰️ (radar + optical nazar)

Baadal ho ya raat — in se zameen par kya badla wo pata chalta hai.

| ID | Dataset | Ek line mein | Licence | Status · Tag |
|----|---------|--------------|---------|--------------|
| **D01** | **Sentinel-1 SAR** (Copernicus) | **Radar** satellite — baadal/andhere ke aar-paar bhi dekhta hai (~10 m). Flood/landslide change detection. | Copernicus open | selected · **[V]** |
| **D02** | **Sentinel-2 MSI** (Copernicus) | **Optical** camera satellite — 13 band, 10 m. River-Eye / scene dekhne ke liye. | Copernicus open | selected · **[V]** |
| **D06** | **MODIS** (NASA) | Roz ki moti-moti global tasveer (250 m–1 km), 2000 se. Bade-paimane ke anomaly ke liye. | NASA open | selected · **[V]** |

---

## 3) Glacier aur GLOF ❄️💥 (jheel phatne waali aafat — video ka main scenario)

Himalaya mein glacial lake phatna (GLOF) — iske liye alag se real registry hai.

| ID | Dataset | Ek line mein | Licence | Status · Tag |
|----|---------|--------------|---------|--------------|
| **D07** | **ITS_LIVE** (NASA/JPL) | **Glacier ki speed** (velocity) — global, 1985 se, 120 m. Glacier aage badh/pighal raha hai kya. | NASA open | selected · **[V]** |
| **D15** | **HMAGLOFDB** | **High Mountain Asia GLOF database** — **766 GLOF events, 1533–2025 tak**. Itihaas ka record. | CC BY 4.0 | selected · **[D]** |
| **D11** | **GLOFNet** | Multimodal GLOF dataset (S2 + ITS_LIVE + MODIS), Shisper/Karakoram. | paper CC BY-NC-ND; data UNVERIFIED | candidate · **[V*]** |

---

## 4) Landslide (Bhuskhalan) 🏔️ ki history + training data

Ye zyadatar "labelled" datasets hain — in se kabhi model train hota (humne nahi kiya).

| ID | Dataset | Ek line mein | Licence | Status · Tag |
|----|---------|--------------|---------|--------------|
| **D08** | **NASA Global Landslide Catalog / COOLR** | Duniya bhar ke landslide **events ki list** (point data). | NASA open | selected · **[V*]** |
| **D18** | **LMHLD** | 25,365 patches, 5 sensors, 7 ilaake (Gorkha/Nepal zone). Zenodo pe. | open-access (verify) | selected · **[D]** |
| **D09** | **Landslide4Sense** | 3,799 training patches, 14-band 128×128. Landslide segmentation. | **UNVERIFIED** (card pe licence nahi) | candidate · **[V*]** |
| **D10** | **SSL4EO-S12** | Bada self-supervised EO pretraining set (2.5 lakh+ locations). Model ko "general nazar" dene ke liye. | CC-BY-4.0 | candidate · **[V]** |
| **D20** | **GDCLD** | Bhookamp se bane (coseismic) landslide segmentation, global. | **UNVERIFIED** | candidate · **[D]** |
| **D21** | **Thalia** | **InSAR deformation** datacubes — zameen dheere-dheere khisak rahi hai kya (7 saal). | per repo (verify) | candidate · **[D]** |
| **D26** | **Landslide Reference S1&S2** (DLR/GFZ) | Duniya bhar ke bade landslides 2015+ (6.2 GB). | CC BY 4.0 | candidate · **[V]** |
| **D23** | **Kerala 2018 landslide inventory** (ITC) | 2018 Kerala monsoon ke landslides ka India-specific record. | **UNVERIFIED** | candidate · **[D]** |
| **D24** | **Bhuvan / NRSC-ISRO** | ISRO ka **Landslide Atlas of India** (Uttarakhand 2013, J&K, Sikkim, Wayanad). | **UNVERIFIED** (ISRO terms) | candidate · **[D]** |

---

## 5) Flood (Baadh) 🌊 ki history + training data

| ID | Dataset | Ek line mein | Licence | Status · Tag |
|----|---------|--------------|---------|--------------|
| **D12** | **Sen1Floods11** | 11 flood events, 512×512 chips. Radar se flood-mapping ka standard benchmark. | **UNVERIFIED** (open bucket) | selected · **[V*]** |
| **D17** | **GEOID-Flood** | 14,282 tiles, 219 events — S1 + S2 + DEM mila ke. | per repo (verify) | selected · **[D]** |
| **D22** | **India Flood Inventory – Impacts (IFI)** | **India** ke district-level flood events, **1967–2023**. Impact/validation ke liye sona. | CC BY 4.0 | selected · **[V]** |
| **D19** | **UFO (Urban Flood Observations)** | 215 chips, 14 events, 3 m — shehri baadh. | per paper (verify) | candidate · **[D]** |
| **D25** | **INDOFLOODS** | Indian station-discharge flood events (river gauge based). | **UNVERIFIED** | candidate · **[D]** |

---

## 6) Land-cover / Scene pehchanna 🌍 (yahaan kheti hai, yahaan paani)

| ID | Dataset | Ek line mein | Licence | Status · Tag |
|----|---------|--------------|---------|--------------|
| **D13** | **BigEarthNet v2 (reBEN)** | 5.49 lakh S1+S2 patches (~110 GiB). Land-cover classification ka bada set. | CDLA-Permissive-1.0 | candidate · **[V]** |
| **D14** | **EuroSAT** | 27,000 images, 10 classes, 13-band 64×64. Chhota, fast baseline. | MIT (+Copernicus) | candidate · **[V]** |

---

## 7) Social media / Crisis text 📱 (WS2 — par ye kabhi alert decide NAHI karta)

| ID | Dataset | Ek line mein | Licence | Status · Tag |
|----|---------|--------------|---------|--------------|
| **D16** | **CrisisMMD / CrisisNLP** | 7 aafat ke ~16k tweets + 18k images. Social signal corroboration ke liye. **Trust max 0.40 pe capped** — ye kabhi life-safety alert gate nahi karta. | **UNVERIFIED** (research terms) | candidate · **[V*]** |

---

## Ek nazar mein summary

- **Baarish/mausam (3):** GPM IMERG, ERA5-Land, SMAP — sab **[V]**, sab selected.
- **Satellite nazar (3):** Sentinel-1, Sentinel-2, MODIS — sab **[V]**, sab selected.
- **Glacier/GLOF (3):** ITS_LIVE [V], HMAGLOFDB [D] (766 GLOFs), GLOFNet [V*].
- **Landslide (9) + Flood (5):** mix of selected + candidate; India-specific wale (IFI, Kerala, Bhuvan/ISRO, INDOFLOODS) khaas is project ke liye.
- **Land-cover (2) + Social (1):** support/corroboration ke liye candidate.

**Dobara yaad:** 26 datasets = **13 selected + 13 candidate** · **12 [V] + 5 [V*] + 9 [D]**.
Sab **real registry entries** hain — par is project mein **kuch download/train nahi hua**. Baaki jo
cheezein (GLOF trigger, flood ka shape, kitne log fase, evac route) video mein dikhti hain wo
**ILLUSTRATIVE** hain, real nahi.
