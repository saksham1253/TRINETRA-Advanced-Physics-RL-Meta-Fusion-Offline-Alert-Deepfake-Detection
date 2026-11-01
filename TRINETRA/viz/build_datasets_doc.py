# -*- coding: utf-8 -*-
"""Build a DETAILED Hinglish datasets explainer DOCX (ALL short-forms expanded to full forms)."""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
import os

OUT = r"C:\Users\Dell\Documents\deepseek-harness\default-workspace\viz\DATASETS_HINGLISH.docx"

doc = Document()
normal = doc.styles["Normal"]
normal.font.name = "Calibri"; normal.font.size = Pt(11)

TEAL = RGBColor(0x1F, 0x7A, 0x6E)
BLUE = RGBColor(0x2A, 0x5D, 0x9E)
GREY = RGBColor(0x55, 0x5B, 0x66)
RED  = RGBColor(0xB0, 0x3A, 0x2E)

def label_para(doc, label, text, color=TEAL):
    p = doc.add_paragraph()
    r = p.add_run(label + " "); r.bold = True; r.font.color.rgb = color
    p.add_run(text); p.paragraph_format.space_after = Pt(4); return p

def meta_para(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text); r.italic = True; r.font.size = Pt(9.5); r.font.color.rgb = GREY
    p.paragraph_format.space_after = Pt(10); return p

def add_dataset(doc, d):
    h = doc.add_heading(level=2); run = h.add_run(f"{d['id']} — {d['name']}"); run.font.color.rgb = BLUE
    label_para(doc, "Ye hota kya hai?", d["concept"])
    label_para(doc, "Humare system mein kaam kya?", d["use"])
    label_para(doc, "Humne kyun choose kiya?", d["choose"])
    label_para(doc, "Novelty / khaas baat:", d["novelty"], color=RED)
    label_para(doc, "Region / coverage:", d["region"], color=GREY)
    meta_para(doc, d["meta"])

# ================= TITLE =================
t = doc.add_heading(level=0); t.add_run("TRINETRA / HIMKAVACH")
doc.add_heading("Saare Datasets — Detail mein, Hinglish mein (saare short-form ki full form ke saath)", level=1)

p = doc.add_paragraph()
p.add_run("Kiske liye? ").bold = True
p.add_run("Agar aapko in cheezon ki thodi hi jaankari hai, tab bhi ye document aapko har dataset ekdum "
          "basic se samjha dega — wo cheez hoti kya hai, humein usse kya milta hai, humne usko kyun chuna, "
          "uski khaas baat (novelty) kya hai, aur wo kis region/ilaake ka data hai. Har short-form ki "
          "poori full form bhi di gayi hai, aur sabse neeche ek Glossary (shabd-koš) bhi hai.")

hb = doc.add_paragraph()
hbr = hb.add_run("IMAANDAARI (sabse zaroori baat): "); hbr.bold = True; hbr.font.color.rgb = RED
hb.add_run("Niche jitne bhi datasets hain, wo sab humari registry (soochi) mein hain — matlab humne inhe "
           "dhoonda, verify kiya, aur plan banaya ki inka istemaal kaise hoga. Lekin is project mein humne "
           "inme se KUCH BHI download ya train NAHI kiya. Yeh ek \u201cdata ka blueprint (khaaka)\u201d hai. Video "
           "mein jo Glacial Lake Outburst Flood (GLOF) trigger, flood ka shape, kitne log fase, evacuation "
           "(nikaasi) route dikhte hain — wo ILLUSTRATIVE (samjhane ke liye banaye gaye) hain, real "
           "measurement nahi. Terrain (zameen) aur satellite imagery REAL hai; physics ke numbers real "
           "equations par SIMULATED hain.")

# ================= CONCEPTS 101 =================
doc.add_heading("Part 0 — Pehle 5 minute: kuch zaroori concepts (bilkul basic)", level=1)
concepts = [
    ("Satellite ki do tarah ki nazar — Optical (camera) vs Radar / Synthetic Aperture Radar (SAR)",
     "Optical satellite ek bahut powerful camera jaisa hai — wo normal roshni (sunlight) se tasveer leta "
     "hai, isliye raat ya baadal mein kaam nahi karta. Radar matlab Synthetic Aperture Radar (SAR) — ye "
     "khud microwave bhejta hai aur unki wapsi se tasveer banata hai — isliye baadal ke aar-paar aur "
     "andhere mein bhi dekh leta hai. Disaster (aafat) ke time aasmaan mein baadal hote hain, isliye "
     "Synthetic Aperture Radar (SAR) bahut kaam ka hai."),
    ("Resolution aur band",
     "Resolution = ek pixel kitni zameen dikhata hai; 10 metre matlab ek pixel ~10 metre ka tukda. Chhota "
     "number = zyada detail. Band = alag-alag rang/wavelength (tarang-lambai) ki parat; insaan ki aankh "
     "3 band — Red, Green, Blue (RGB, laal-hara-neela) — dekhti hai, satellite 13+ band dekhta hai (jaise "
     "infrared / avrakt) jisse paani, kheti, nami alag-alag pehchan mein aa jaate hain."),
    ("Reanalysis kya hota hai (ERA5 jaisa)",
     "Reanalysis matlab duniya bhar ke purane mausam observations ko ek physics model mein daal ke ek saaf, "
     "continuous (lagataar) mausam-history bana dena — jaise \u2018pichhle 70 saal har ghante kahan kitni "
     "baarish, temperature (taapmaan), nami thi\u2019. Isse hum pattern aur trigger-threshold (seema) nikaal "
     "sakte hain."),
    ("Soil moisture (mitti ki nami) kyun important hai",
     "Pahaad ki mitti pehle se geeli ho, to thodi aur baarish mein hi wo khisak (landslide / bhuskhalan) "
     "jaati hai. Isliye \u2018zameen kitni saturated (santript, paani se bhari) hai\u2019 jaanna zaroori hai — ye "
     "Factor of Safety (FS, surakhsha-gunank) physics mein seedha jaata hai. Factor of Safety 1 se neeche "
     "jaane ka matlab slope fail (dhalaan toot-na)."),
    ("Glacial Lake Outburst Flood (GLOF) kya hai",
     "Glacial Lake Outburst Flood (GLOF) = \u2018himnad-jheel ke phatne se aayi baadh\u2019. Himalaya mein glacier "
     "(himnad / barf ka pahaad) pighal ke uske aage ek jheel ban jaati hai, jise mitti/malbe ka kamzor "
     "baandh (moraine, himodh) rok ke rakhta hai. Jab wo baandh toot-ta hai to achaanak laakhon litre paani "
     "neeche gaon ki taraf aata hai — yahi humari video ka main scenario hai."),
    ("Interferometric Synthetic Aperture Radar (InSAR) — zameen ka dheere khisakna",
     "Interferometric Synthetic Aperture Radar (InSAR) ek radar technique hai jisse pata chalta hai ki "
     "zameen millimetre-level pe dheere-dheere khisak rahi hai kya — landslide se pehle aksar ye slow "
     "movement (dheemi harkat) hoti hai, jise InSAR pakad leta hai."),
    ("Digital Elevation Model (DEM) — 3D zameen",
     "Digital Elevation Model (DEM) = har jagah ki unchaai (height / oonchai) ka data — isi se 3D pahaad, "
     "dhalaan (slope), aur paani kis taraf bahega ye nikalta hai. Humari video ka 3D terrain real Digital "
     "Elevation Model (DEM) se bana hai."),
    ("Patch, label, benchmark",
     "Machine Learning (ML, mशीन-सीख) datasets aksar bade image ko chhote \u2018patches\u2019 (jaise 128x128 "
     "pixel tukde) mein kaat ke dete hain, aur har patch pe \u2018label\u2019 (nishaan) laga hota hai (jaise "
     "\u2018yahaan landslide hai/nahi\u2019). \u2018Benchmark\u2019 matlab ek standard dataset jis pe sab apne "
     "model ki tulna (comparison) karte hain."),
    ("Earth Observation (EO) aur Early Warning System (EWS)",
     "Earth Observation (EO) = \u2018prithvi-nireekshan\u2019, yaani satellite/sensor se zameen ko dekhna aur "
     "naapna. Early Warning System (EWS) = \u2018poorva-chetavani pranaali\u2019, yaani aafat se pehle hi alert "
     "dene wala system — humara TRINETRA ek EWS hi hai."),
]
for title, body in concepts:
    label_para(doc, title + " —", body, color=TEAL)

# legend table
doc.add_heading("Legend — teen cheezein jo baar-baar aayengi", level=2)
doc.add_paragraph("Verification tag (kitna pakka hai):")
tbl = doc.add_table(rows=4, cols=2); tbl.style = "Light Grid Accent 1"; tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
rows = [("Tag", "Matlab (full form)"),
        ("[V] = Verified", "Link, licence, access sab khud check kiya, pakka sahi hai"),
        ("[V*] = Verified-with-star", "Mostly verified — ek-aadh fact (count/licence) confirm karna baaki"),
        ("[D] = Discovery-only", "Mil gaya hai par abhi poori tarah verify nahi")]
for i,(a,b) in enumerate(rows):
    c = tbl.rows[i].cells; c[0].text = a; c[1].text = b
    if i==0:
        for cc in c:
            for pp in cc.paragraphs:
                for rr in pp.runs: rr.bold=True
doc.add_paragraph()
label_para(doc, "Status —", "\u201cselected\u201d = pakka use karenge (core plan ka hissa). \u201ccandidate\u201d = accha option, zaroorat padi to lenge.", color=GREY)
label_para(doc, "Workstream (WS, kaam-dhaara) —", "WS1 = physics / landslide-flood core (buniyaadi); WS2 = social-media; WS3 = alert aur dissemination (prasaar); WS4 = optical / scene vision (drishya); WS8 = Earth Observation (EO) anomaly aur glacier-GLOF.", color=GREY)
label_para(doc, "Total —", "26 datasets = 13 selected + 13 candidate; 12 Verified [V] + 5 Verified-with-star [V*] + 9 Discovery-only [D].", color=GREY)

def group(title, intro):
    doc.add_heading(title, level=1)
    p = doc.add_paragraph(); r = p.add_run(intro); r.italic = True; r.font.color.rgb = GREY

# ---- GROUP 1 ----
group("Part 1 — Baarish aur Mausam ka data (aafat ka trigger)",
      "Landslide aur flood ki shuruaat aksar baarish se hoti hai. Ye datasets batate hain \u2018kitni baarish "
      "hui, mitti kitni geeli hai, mausam ka itihaas kya hai\u2019 — yahi physics engine (WS1) ka khana hai.")
add_dataset(doc, dict(id="D03", name="Global Precipitation Measurement — IMERG precipitation (NASA)",
    concept="Global Precipitation Measurement (GPM) = \u2018vaishvik varsha maapan\u2019, National Aeronautics and "
            "Space Administration (NASA, amreeki antariksh sanstha) aur Japan Aerospace Exploration Agency "
            "(JAXA, japani antariksh sanstha) ke satellite ka ek jaal (constellation) jo poori duniya ki "
            "baarish naapta hai. IMERG (Integrated Multi-satellitE Retrievals for GPM — kai satellite ko "
            "milakar banaya gaya varsha-product) har aadhe ghante, 0.1 degree (~11 kilometre) grid pe baarish "
            "deta hai, 2000 se abhi tak.",
    use="Caine ka rainfall Intensity-Duration (I-D, teevrata-avadhi) threshold humara landslide trigger "
        "hai. Global Precipitation Measurement (GPM) se humein \u2018kitni tez, kitni der baarish hui\u2019 milta "
        "hai, jise us threshold se compare karte hain.",
    choose="Kyunki ye zameen pe rain-gauge (varsha-maapi yantra) na hone wale pahaadi/remote (door-daraaz) "
           "ilaakon mein bhi baarish deta hai, free hai, aur near-real-time (lagbhag turant) milta hai — "
           "offline-first Early Warning System (EWS) ke liye perfect.",
    novelty="Satellite-based global rain jo har jagah milti hai (zameeni sensor na ho to bhi), aur 20+ saal "
            "ki continuous (lagataar) history — long-term threshold calibration (seema-samायोjan) possible.",
    region="Global (poori duniya), 60 degree North se 60 degree South best coverage; Himalaya/India fully covered.",
    meta="Workstream WS1/WS3 · selected · [V] Verified · Licence: NASA open data · Access: Earthdata/PPS "
         "(Precipitation Processing System) login · Size: 0.1 degree, half-hourly, 2000-present (Version 07)"))
add_dataset(doc, dict(id="D05", name="ERA5-Land reanalysis (ECMWF / Copernicus C3S)",
    concept="ERA5-Land, European Centre for Medium-Range Weather Forecasts (ECMWF, yurop ka madhyam-avadhi "
            "mausam poorvanumaan kendra) ka reanalysis hai — matlab physics model + purane observations se "
            "bani ek saaf mausam-history: temperature, baarish, nami, hawa — 9 kilometre grid pe, har ghante, "
            "1950 se abhi tak. Isko Copernicus Climate Change Service (C3S, jalvायु-parivartan seva) deta hai.",
    use="Trigger thresholds calibrate karne, antecedent (pehle se jama) baarish/nami nikaalne, aur missing "
        "data bharne ke liye background mausam-context deta hai.",
    choose="Sabse bharosemand, lamba, consistent mausam record — aur Creative Commons Attribution (CC-BY) "
           "licence ke saath free. Research mein ye de-facto (practically) standard hai.",
    novelty="70+ saal ki hourly (har-ghante), gap-free (bina-khaali) global climate reanalysis — kisi ek "
            "sensor pe depend nahi.",
    region="Global land (poori duniya ki zameen); Himalaya/India included.",
    meta="Workstream WS1 · selected · [V] Verified · Licence: Creative Commons Attribution (CC-BY), DOI "
         "10.24381/cds.e2161bac · Access: Climate Data Store (CDS) API · Size: 0.1 degree (9 km) hourly 1950-present"))
add_dataset(doc, dict(id="D04", name="SMAP soil moisture (NASA NSIDC)",
    concept="SMAP = Soil Moisture Active Passive (\u2018mitti-nami sakriy-nishkriy\u2019), National Aeronautics and "
            "Space Administration (NASA) ka satellite jo mitti ki upari parat ki nami (water content) naapta "
            "hai, ~9-36 kilometre resolution pe, 2015 se.",
    use="Factor of Safety (FS, surakhsha-gunank) physics mein slope ki saturation (paani-bharaav) chahiye — "
        "SMAP batata hai zameen pehle se kitni geeli hai, jisse pata chalta hai ki aur thodi baarish mein "
        "failure hoga ya nahi.",
    choose="Soil moisture ka seedha satellite source, free, aur disaster-prone (aafat-prawan) remote "
           "ilaakon ke liye bhi available.",
    novelty="Dedicated (khaas is kaam ke liye) soil-moisture mission — mitti ki nami ka direct global "
            "measurement, jo zameeni sensors se possible hi nahi tha.",
    region="Global; Himalaya/India covered (resolution motी/coarse hai).",
    meta="Workstream WS1 · selected · [V] Verified · Licence: NASA open data · Access: Earthdata login · "
         "Provider: National Snow and Ice Data Center (NSIDC) · Size: global 2015-present, ~9-36 km"))

# ---- GROUP 2 ----
group("Part 2 — Satellite se Zameen Dekhna (radar + optical nazar)",
      "Ye satellites zameen par kya badla, kahan paani phaila, kahan slope khisak gaya — ye dekhne ke liye "
      "humari \u2018aankhein\u2019 hain.")
add_dataset(doc, dict(id="D01", name="Sentinel-1 Synthetic Aperture Radar (Copernicus CDSE)",
    concept="Sentinel-1 Europe (Copernicus programme) ka Synthetic Aperture Radar (SAR, kritrim-dvaar radar) "
            "satellite hai. Radar hone ki wajah se ye baadal ke neeche aur raat mein bhi ~10 metre detail "
            "mein dekh leta hai (C-band, ek radar tarang-dairy).",
    use="Flood ka paani aur landslide ka scar (nishaan) \u2018before vs after\u2019 (pehle-baad) compare karke "
        "pakadne ke liye. Disaster ke din aksar baadal hote hain, isliye optical fail ho jaata hai par ye nahi.",
    choose="Free, open, continuous mission, aur sabse bada plus — har mausam/har waqt kaam karta hai. "
           "Disaster response ki backbone (reedh).",
    novelty="All-weather (har-mausam), day-night (din-raat) radar imaging free mein — flood/landslide "
            "detection ka game-changer.",
    region="Global, free; India/Himalaya full coverage.",
    meta="Workstream WS1/WS8 · selected · [V] Verified · Licence: Copernicus free/open · Access: Copernicus "
         "Data Space Ecosystem (CDSE), open (registration for bulk/API) · Size: continuous C-band Ground Range "
         "Detected (GRD) / Single Look Complex (SLC) ~10 m"))
add_dataset(doc, dict(id="D02", name="Sentinel-2 MultiSpectral Instrument (Copernicus CDSE)",
    concept="Sentinel-2 Europe ka optical (camera) satellite hai jisme MultiSpectral Instrument (MSI, "
            "bahu-varnakram upkaran) laga hai — 13 band (visible + infrared / drishya + avrakt), 10/20/60 "
            "metre. Saaf mausam mein bahut detailed rangeen tasveer deta hai.",
    use="River-Eye (nadi-nigrani) / scene samajhne, paani-kheti-malba alag karne, aur landslide/flood ke "
        "baad ki clear tasveer ke liye.",
    choose="Free, high-detail, 5-din mein dobara us jagah aata hai (revisit, punar-bhramanm), aur radar "
           "(Sentinel-1) ke saath mila ke bahut powerful ban jaata hai.",
    novelty="High-resolution multi-band optical, free, fast revisit — Sentinel-1 ke saath \u2018radar+optical\u2019 "
            "ki jodi banti hai.",
    region="Global, free; India/Himalaya full coverage.",
    meta="Workstream WS4/WS8 · selected · [V] Verified · Licence: Copernicus free/open · Access: Copernicus "
         "Data Space Ecosystem (CDSE) · Size: continuous 13-band 10/20/60 m"))
add_dataset(doc, dict(id="D06", name="MODIS (NASA LP DAAC)",
    concept="MODIS = Moderate Resolution Imaging Spectroradiometer (\u2018madhyam-resolution imaging "
            "spectroradiometer\u2019), National Aeronautics and Space Administration (NASA) ke Terra/Aqua "
            "satellites ka sensor hai jo poori duniya ki roz ki tasveer leta hai, par moti (coarse) detail "
            "mein — 250 metre se 1 kilometre.",
    use="Bade-paimane ke change/anomaly (asmaanyata) jaldi pakadne ke liye (jaise bada flood ya snow/glacier "
        "badlaav) — roz ka global view.",
    choose="Roz ka, 20+ saal lamba, free global record — fast, broad screening (chaanbeen) ke liye best.",
    novelty="Daily (roz ka) global coverage, 2000 se — long consistent time-series jo anomaly detection ke "
            "liye sona hai.",
    region="Global, daily; Himalaya/India covered.",
    meta="Workstream WS8 · selected · [V] Verified · Licence: NASA open data · Provider: Land Processes "
         "Distributed Active Archive Center (LP DAAC) · Access: Earthdata/AppEEARS/Google Earth Engine (GEE) "
         "· Size: Terra/Aqua 2000-present 250 m-1 km"))

# ---- GROUP 3 ----
group("Part 3 — Glacier aur Glacial Lake Outburst Flood (GLOF) (video ka main scenario)",
      "Yeh wo datasets hain jo khaas Himalaya ke glacier aur Glacial Lake Outburst Flood (GLOF) ke liye hain "
      "— humari working-simulation ki buniyaad.")
add_dataset(doc, dict(id="D07", name="ITS_LIVE glacier velocity (NASA/JPL)",
    concept="ITS_LIVE ka poora naam \u2018Inter-mission Time Series of Land Ice Velocity and Elevation\u2019 "
            "(\u2018antar-mission barf-vेg aur unchaai ka samay-shrinkhala\u2019) hai — National Aeronautics and "
            "Space Administration (NASA) ki Jet Propulsion Laboratory (JPL, jet-prणोदन prayogshala) ka data "
            "jo batata hai duniya ke glacier kitni speed se aur kis taraf khisak rahe hain (velocity/veg), "
            "1985 se, ~120 metre pe.",
    use="Glacial Lake Outburst Flood (GLOF) se pehle glacier ki abnormal movement ya tezi pakadne ke liye — "
        "anomaly ka ek signal.",
    choose="Glacier dynamics (gatisheelta) ka seedha, lamba, free global record — GLOF early-warning context deta hai.",
    novelty="Decadal (dशक-vyapi, 1985+) global glacier-speed maps automatically satellite se — pehle ye "
            "manually mushkil tha.",
    region="Global glaciers; High Mountain Asia (HMA, uchch-parvatiya एशिया) / Himalaya included.",
    meta="Workstream WS8 · selected · [V] Verified · Licence: NASA open (MEaSUREs programme) · Access: "
         "portal / SpatioTemporal Asset Catalog (STAC) / Zarr / Amazon Simple Storage Service (S3) · Size: "
         "global 1985-present 120 m"))
add_dataset(doc, dict(id="D15", name="HMAGLOFDB (High Mountain Asia GLOF Database)",
    concept="HMAGLOFDB = \u2018High Mountain Asia Glacial Lake Outburst Flood Database\u2019 (uchch-parvatiya "
            "एशिया ki himnad-jheel baadh ki database). Isme Himalaya + aas-paas ke GLOF events ka historical "
            "record hai — kab, kahan, kaunsi jheel phati.",
    use="GLOF scenario ko ground-truth (zameeni-sach) / validation dene ke liye, aur \u2018kaunsi jheelein "
        "khatarnaak hain\u2019 samajhne ke liye.",
    choose="India/Himalaya ke liye sabse relevant GLOF catalogue — region-specific hai, isliye core mein liya.",
    novelty="766 Glacial Lake Outburst Flood events, 1533 se 2025 tak (version 4.0) — itna lamba aur "
            "region-focused GLOF record durlabh (rare) hai.",
    region="High Mountain Asia (HMA) — Himalaya, Karakoram, Hindu Kush — bilkul humara ilaaka.",
    meta="Workstream WS8 · selected · [D] Discovery-only · Licence: Creative Commons Attribution (CC BY 4.0), "
         "release pe confirm · Access: GitHub / International Centre for Integrated Mountain Development "
         "(ICIMOD) Regional Database System (RDS) · Size: 766 GLOFs 1533-2025 (version 4.0)"))
add_dataset(doc, dict(id="D11", name="GLOFNet (multimodal GLOF dataset)",
    concept="GLOFNet ek research dataset hai jo Glacial Lake Outburst Flood (GLOF) ke liye alag-alag source "
            "— Sentinel-2 (optical) + ITS_LIVE (glacier-speed) + MODIS — ko ek saath (multimodal, "
            "bahu-madhyam) jodta hai.",
    use="GLOF detection/monitoring ka ek ready-made multimodal example — reference architecture ke liye.",
    choose="Kyunki ye exactly GLOF ke liye bana multimodal set hai (jo rare hai); candidate rakha kyunki "
           "data licence/download abhi unverified (bina-jaanchi) hai.",
    novelty="GLOF ke liye optical + velocity + coarse ko ek jagah jodna — multimodal approach ki novelty.",
    region="Shisper glacier / Karakoram (Pakistan-side Himalaya).",
    meta="Workstream WS8 · candidate · [V*] Verified-with-star · Licence: paper Creative Commons "
         "Attribution-NonCommercial-NoDerivatives (CC BY-NC-ND 4.0); data licence UNVERIFIED · Access: "
         "download URL UNVERIFIED · Size: Sentinel-2 + ITS_LIVE + MODIS"))

# ---- GROUP 4 ----
group("Part 4 — Landslide (bhuskhalan) ki history aur training data",
      "Yeh zyadatar \u2018labelled\u2019 (nishaan-lage) datasets hain — matlab inme pehle se mark hua hai kahan "
      "landslide hua. In se kabhi model train hota hai (humne is project mein train nahi kiya).")
add_dataset(doc, dict(id="D08", name="NASA Global Landslide Catalog / COOLR",
    concept="Ye duniya bhar ke landslide events ki ek badi list hai (kahan, kab hua) — zyadatar point "
            "(ek-ek jagah) ke roop mein. COOLR = \u2018Cooperative Open Online Landslide Repository\u2019 "
            "(\u2018sahkaari khula online bhuskhalan bhandar\u2019), jisme citizen (aam-naagrik) + National "
            "Aeronautics and Space Administration (NASA) dono ka data aata hai.",
    use="Landslide ki jagah/time ki ground-truth — thresholds aur models ko check karne ke liye.",
    choose="Sabse jaana-maana free global landslide inventory (soochi) — baseline reference.",
    novelty="Open, global, community (samुदाय) + NASA mila-jula landslide catalogue — crowd + official ka sangam.",
    region="Global; India ke events bhi shaamil.",
    meta="Workstream WS1/WS8 · selected · [V*] Verified-with-star · Licence: NASA open data · Access: "
         "viewer/open-data portal · Size: point events (count UNVERIFIED)"))
add_dataset(doc, dict(id="D18", name="LMHLD landslide dataset",
    concept="LMHLD ek multi-sensor (kai-sensor) landslide dataset hai — 25,365 image-patches (tukde), 5 alag "
            "sensors, 7 areas (Gorkha/Nepal bhookamp zone ke aas-paas).",
    use="Landslide segmentation (image mein landslide ka exact area mark karna) sikhaane ke liye.",
    choose="Multi-sensor + Himalaya ke paas (Gorkha) hone ki wajah se humare region se relate karta hai.",
    novelty="5 sensors ko ek landslide dataset mein jodna — multi-sensor diversity (vividhता).",
    region="Gorkha (Nepal) aur aas-paas — Himalayan belt (patti).",
    meta="Workstream WS1/WS8 · selected · [D] Discovery-only · Licence: open-access Zenodo (verify) · Access: "
         "Zenodo (repository) · Size: 25,365 patches, 5 sensors, 7 areas"))
add_dataset(doc, dict(id="D09", name="Landslide4Sense",
    concept="Ek popular landslide-detection training dataset — 3,799 train patches, har patch 14-band "
            "128x128 pixel (optical + infrared + Digital Elevation Model / DEM mila ke).",
    use="Landslide \u2018hai/nahi + kahan\u2019 waale model sikhaane ka ready benchmark.",
    choose="Jaana-maana benchmark, Hugging Face (HF, ek open-source ML platform) pe aasaani se milta hai; "
           "candidate kyunki licence card pe nahi likha (UNVERIFIED) — legally safe hone tak core mein nahi daala.",
    novelty="14-band (multi-source) patches ek hi landslide benchmark mein — competition se popular hua.",
    region="Multiple global landslide sites.",
    meta="Workstream WS1/WS8 · candidate · [V*] Verified-with-star · Licence: UNVERIFIED (card pe licence "
         "nahi) · Access: Hugging Face (HF) / GitHub · Size: 3,799/245/800 patches, 14-band 128x128"))
add_dataset(doc, dict(id="D10", name="SSL4EO-S12",
    concept="SSL4EO-S12 = \u2018Self-Supervised Learning for Earth Observation, Sentinel-1 and -2\u2019 "
            "(\u2018prithvi-nireekshan ke liye swa-nirikshit sीख\u2019). Ek bahut bada bina-label pre-training "
            "dataset — 2.5 lakh+ jagah ke Sentinel-1 + Sentinel-2 images. Isse model pehle \u2018general nazar\u2019 "
            "seekhta hai, phir chhote labelled data pe fine-tune hota hai.",
    use="Hamare Earth Observation (EO) models ko strong starting-point (pretrained backbone / poorva-prashikshit "
        "aadhaar) dene ke liye.",
    choose="Itna bada free pretraining set — labels ki kami ko door karta hai; candidate as support.",
    novelty="Earth Observation (EO) ke liye sabse bade self-supervised pretraining corpora (shabd-rashi) mein "
            "se ek (~1.5 Terabyte raw).",
    region="Global (251,079 locations x 4 seasons/mausam).",
    meta="Workstream WS1/WS8 · candidate · [V] Verified · Licence: code Apache License 2.0; data+weights "
         "Creative Commons Attribution (CC-BY-4.0) · Access: mediaTUM / Hugging Face (HF) · Size: 251,079 "
         "locations x 4 seasons (~1.5 Terabyte raw)"))
add_dataset(doc, dict(id="D20", name="GDCLD (coseismic landslide dataset)",
    concept="\u2018Coseismic\u2019 (sah-bhukampiya) matlab bhookamp ke saath aaye landslides. GDCLD (Global Dataset "
            "of Coseismic Landslides) un landslides ka global segmentation dataset hai.",
    use="Earthquake-triggered (bhookamp-janit) landslide ko pehchanne ka training/reference data.",
    choose="Trigger ka ek alag type (bhookamp) cover karta hai — completeness (poornta) ke liye candidate.",
    novelty="Khaas earthquake-induced landslides par focus — ek specialised (vishesh) category.",
    region="Global coseismic landslide events.",
    meta="Workstream WS1 · candidate · [D] Discovery-only · Licence: UNVERIFIED · Access: per paper · Size: "
         "global coseismic landslide segmentation"))
add_dataset(doc, dict(id="D21", name="Thalia (InSAR deformation)",
    concept="Thalia, Interferometric Synthetic Aperture Radar (InSAR) \u2018datacubes\u2019 ka dataset hai — yaani "
            "zameen millimetre-level pe dheere khisak rahi hai kya, uska time-series (7 saal), topography "
            "(bhoo-aakriti) aur atmosphere (vaayumandal) ke saath.",
    use="Landslide se PEHLE ki slow ground movement (precursor / poorva-sanket) pakadne ke liye — early "
        "warning ka sapna.",
    choose="Interferometric Synthetic Aperture Radar (InSAR) precursor detection ek powerful, naya angle "
           "deta hai; candidate (verify baaki).",
    novelty="InSAR + topography + atmospheric correction ko ready datacubes mein dena — deformation "
            "(vikriti) Machine Learning (ML) easy karta hai.",
    region="38 datacubes, multiple sites (global).",
    meta="Workstream WS1/WS8 · candidate · [D] Discovery-only · Licence: per repo (verify) · Access: GitHub · "
         "Size: 38 datacubes, 7 saal, InSAR + topography + atmosphere"))
add_dataset(doc, dict(id="D26", name="Landslide Reference Data Sentinel-1 & -2 (DLR / GFZ)",
    concept="Germany ki agencies — Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, jarman antariksh kendra) "
            "aur GeoForschungsZentrum (GFZ, jarman bhoo-vigyan anusandhान kendra) — ka reference dataset: "
            "duniya ke bade landslides (2015 ke baad) Sentinel-1 aur Sentinel-2 ke saath.",
    use="Bade landslides ke liye saaf, licence-clear reference/validation data.",
    choose="Creative Commons Attribution (CC BY 4.0) clean licence + Sentinel-1 & -2 dono — bharosemand "
           "reference; candidate as support.",
    novelty="Authoritative (adhikarik) agencies (DLR/GFZ) ka curated, licence-clear large-landslide reference.",
    region="Worldwide (poori duniya) large landslides, 2015+.",
    meta="Workstream WS1 · candidate · [V] Verified · Licence: Creative Commons Attribution (CC BY 4.0) · "
         "Access: Zenodo (6.2 Gigabyte) · Size: worldwide large landslides 2015+"))
add_dataset(doc, dict(id="D23", name="Kerala 2018 monsoon landslide inventory (ITC)",
    concept="2018 ke Kerala monsoon mein hue landslides ki India-specific list/inventory (soochi). Banane "
            "wala: Faculty of Geo-Information Science and Earth Observation (ITC), University of Twente, Netherlands.",
    use="India ke real event par model/thresholds validate karne ke liye.",
    choose="India-specific real disaster — bahut relevant; candidate kyunki licence/access unverified.",
    novelty="Ek bade Indian monsoon-landslide event ka focused inventory.",
    region="Kerala, India (2018).",
    meta="Workstream WS1 · candidate · [D] Discovery-only · Licence: UNVERIFIED · Access: institutional "
         "(sansthागत) page · Size: 2018 Kerala landslides"))
add_dataset(doc, dict(id="D24", name="Bhuvan / NRSC-ISRO landslide inventories",
    concept="Bhuvan, Indian Space Research Organisation (ISRO, bhaartiya antariksh anusandhान sangathan) ka "
            "geo-portal hai. Isme National Remote Sensing Centre (NRSC, rashtriya door-samvedन kendra) ki "
            "landslide inventories hain — India ka official \u2018Landslide Atlas of India\u2019 aur bade events "
            "(Uttarakhand 2013, Jammu & Kashmir / J&K, Sikkim, Wayanad).",
    use="India-sarkari (adhikarik) landslide reference — khaas Uttarakhand jaise humare demo-region ke liye.",
    choose="Indian Space Research Organisation (ISRO) ka official India data — most relevant; candidate "
           "kyunki ISRO terms/licence unverified.",
    novelty="India ka national-scale (rashtriya-paimane) official landslide atlas, ek hi jagah.",
    region="India — Uttarakhand, Jammu & Kashmir, Sikkim, Wayanad (Kerala) etc.",
    meta="Workstream WS1/WS8 · candidate · [D] Discovery-only · Licence: UNVERIFIED (ISRO terms) · Access: "
         "Bhuvan portal · Size: Landslide Atlas of India + major events"))

# ---- GROUP 5 ----
group("Part 5 — Flood (baadh) ki history aur training data",
      "Flood mapping aur impact (asar) ke liye datasets — kai India-specific hain, jo is project ke liye khaas keemti.")
add_dataset(doc, dict(id="D12", name="Sen1Floods11",
    concept="Flood mapping ka ek famous benchmark — 11 flood events ke Sentinel-1 radar + labelled flood "
            "masks (paani ke nishaan), 512x512 pixel chips mein.",
    use="\u2018Radar image se paani kahan phaila\u2019 waale flood-segmentation ka standard training/test set.",
    choose="Flood-mapping ka de-facto benchmark; selected. Licence open bucket (Google Cloud Storage / GCS) "
           "se aata hai (unverified) isliye [V*].",
    novelty="Radar-based global flood benchmark jisne hand-labelled (haath se nishaan-lage) flood masks ko "
            "standard bana diya.",
    region="11 events, 6 continents (vishwa-bhar).",
    meta="Workstream WS1/WS8 · selected · [V*] Verified-with-star · Licence: UNVERIFIED (open Google Cloud "
         "Storage / GCS bucket; CVPRW 2020 — Computer Vision and Pattern Recognition Workshops) · Access: "
         "gsutil gs://sen1floods11 (~14 Gigabyte) · Size: 11 events, 512x512 chips"))
add_dataset(doc, dict(id="D17", name="GEOID-Flood",
    concept="Ek bada flood dataset jo Sentinel-1 (radar) + Sentinel-2 (optical) + Digital Elevation Model "
            "(DEM) teeno ko jodta hai — 14,282 tiles (khand), 219 events.",
    use="Multimodal (bahu-madhyam) flood mapping (radar+optical+height) sikhaane/reference ke liye.",
    choose="Teeno modality + bahut saare events — rich flood training; selected.",
    novelty="Sentinel-1 + Sentinel-2 + DEM ko ek flood dataset mein jodna, 219 events ke paimane pe.",
    region="219 flood events (global).",
    meta="Workstream WS1/WS8 · selected · [D] Discovery-only · Licence: per repo (verify) · Access: GitHub · "
         "Size: 14,282 tiles, 219 events, Sentinel-1 + Sentinel-2 + DEM"))
add_dataset(doc, dict(id="D22", name="India Flood Inventory - Impacts (IFI)",
    concept="IFI = \u2018India Flood Inventory - Impacts\u2019 (bhaarat baadh soochi - prabhaav). India ke flood "
            "events ka district-level (zilा-stariya) record with impacts (nuksaan) — 1967 se 2023 tak, "
            "Comma-Separated Values (CSV, ek simple spreadsheet file) files mein (chhoti ~1.9 Megabyte).",
    use="India ke liye flood frequency (aavृtti), impact aur validation — alert/impact estimation ko ground dena.",
    choose="India-specific, lamba (56 saal), clean Creative Commons Attribution (CC BY 4.0) licence — isliye "
           "selected aur [V] Verified.",
    novelty="India ka district-level, impact-focused flood inventory 1967-2023 — region + impact dono.",
    region="India (district level / zilा-stariya), 1967-2023.",
    meta="Workstream WS1/WS3 · selected · [V] Verified · Licence: Creative Commons Attribution (CC BY 4.0) · "
         "Access: Zenodo (Comma-Separated Values / CSV, ~1.9 Megabyte) · Size: district-level flood events 1967-2023"))
add_dataset(doc, dict(id="D19", name="UFO (Urban Flood Observations)",
    concept="UFO = \u2018Urban Flood Observations\u2019 (shehri baadh ke avlokan). Shehri baadh ka dataset — "
            "PlanetScope satellite ki 3 metre high-resolution images, 215 chips, 14 events.",
    use="Sheher mein flood mapping (jahan buildings/roads hote hain) ke liye.",
    choose="Urban flood ka khaas angle; candidate (verify + PlanetScope registration).",
    novelty="High-resolution (3 metre) khaas urban-flood observations — city-scale flood ka rare focus.",
    region="14 urban (shehri) flood events (global).",
    meta="Workstream WS1/WS4 · candidate · [D] Discovery-only · Licence: per paper (verify) · Access: per "
         "paper repo · Size: 215 chips, 14 events, 3 m"))
add_dataset(doc, dict(id="D25", name="INDOFLOODS (station discharge flood events)",
    concept="INDOFLOODS, India ke river-gauge (nadi-maapi) station data se bane flood events ka dataset hai "
            "— yaani nadi mein paani (discharge / jal-pravaah) kitna chadha.",
    use="River-stage/discharge based flood validation — Internet of Things (IoT) river-stage sensor ko real "
        "data se jodta hai.",
    choose="India observational (prekshan-aadharit) flood data — region-specific; candidate (licence unverified).",
    novelty="Station-discharge based Indian flood event compilation (sankalan) — gauge-grounded.",
    region="India (observational flood events).",
    meta="Workstream WS1/WS3 · candidate · [D] Discovery-only · Licence: UNVERIFIED · Access: Zenodo · Size: "
         "Indian observational flood events"))

# ---- GROUP 6 ----
group("Part 6 — Land-cover / Scene pehchanna (yahan kheti, yahan paani, yahan sheher)",
      "Yeh general \u2018scene classification\u2019 (drishya-vargikaran) datasets hain — model ko sikhaate hain ki "
      "satellite image mein kya hai (jungle, paani, sheher, kheti). Support/pretraining ke liye.")
add_dataset(doc, dict(id="D13", name="BigEarthNet version 2 (reBEN)",
    concept="BigEarthNet (bada prithvi-network) version 2, upnaam reBEN (refined BigEarthNet / sudhaarit "
            "BigEarthNet). Ek bahut bada land-cover (bhoomi-aavaran) dataset — 5,49,488 Sentinel-1 + Sentinel-2 "
            "patches, har patch pe land-cover labels (~110 Gibibyte).",
    use="Earth Observation (EO) models ko \u2018zameen pe kya hai\u2019 ki samajh dene (pretraining/support).",
    choose="Scale aur clean Community Data License Agreement - Permissive 1.0 (CDLA-Permissive-1.0) licence — "
           "safe aur bada; candidate as support.",
    novelty="Europe-scale multi-label land-cover benchmark, Sentinel-1 + Sentinel-2 dono ke saath — Earth "
            "Observation ka \u2018ImageNet\u2019 jaisa.",
    region="Europe (10 countries/desh).",
    meta="Workstream WS4/WS8 · candidate · [V] Verified · Licence: Community Data License Agreement - "
         "Permissive 1.0 (CDLA-Permissive-1.0) · Access: Zenodo 10891137 · Size: 549,488 Sentinel-1+2 patches "
         "(~110 Gibibyte)"))
add_dataset(doc, dict(id="D14", name="EuroSAT",
    concept="EuroSAT (Europe Satellite dataset) — chhota, aasaan land-use dataset: 27,000 images, 10 classes "
            "(jaise river/nadi, forest/jungle, residential/aawasiya), 13-band 64x64 pixel.",
    use="Fast prototyping/baseline — chhote model jaldi try karne ke liye.",
    choose="Light, Massachusetts Institute of Technology (MIT) licence, har jagah available — quick baseline; candidate.",
    novelty="Sentinel-2 par sabse popular \u2018entry-level\u2019 (shuruaati) benchmark — simplicity hi novelty.",
    region="Europe (34 countries ki Sentinel-2 tiles).",
    meta="Workstream WS4 · candidate · [V] Verified · Licence: Massachusetts Institute of Technology (MIT) "
         "licence (+ Copernicus Sentinel-2) · Access: Zenodo 7711810 · Size: 27,000 images, 10 classes, "
         "13-band 64x64"))

# ---- GROUP 7 ----
group("Part 7 — Social media / Crisis text (WS2 — par ye kabhi alert DECIDE nahi karta)",
      "Aafat ke time log social media par bhi post karte hain. Ye signal corroboration (tasdeeq / samarthan) "
      "mein madad karta hai — par safety-rule: iski trust 0.40 pe capped (seemit) hai, ye kabhi life-safety "
      "alert gate (rok/control) nahi karega.")
add_dataset(doc, dict(id="D16", name="CrisisMMD / CrisisNLP",
    concept="CrisisMMD = \u2018Crisis MultiModal Dataset\u2019 (aapda bahu-madhyam dataset) aur CrisisNLP = "
            "\u2018Crisis Natural Language Processing\u2019 (aapda praakritik-bhaasha-prasanskaran). Aafat ke "
            "dauraan ke tweets + images ka labelled dataset — 7 events, ~16,000 tweets aur ~18,000 images, "
            "jisme mark hai kaunsa post kis cheez (damage/rescue — nuksaan/bachaav) ke baare mein hai.",
    use="Social-media ko ek corroborating (samarthak) signal ki tarah fuse karne ka reference — Workstream WS2.",
    choose="Crisis Natural Language Processing (NLP) ka jaana-maana dataset; candidate kyunki \u2018research "
           "terms\u2019 licence unverified. Design-rule: trust 0.40 pe capped, kabhi alert decide nahi karega "
           "(deepfake / misinformation / galat-soochna safety).",
    novelty="Multimodal (text + image) crisis dataset events ke saath — social signal research ka standard.",
    region="7 global disaster events (multi-country / kai-desh).",
    meta="Workstream WS2/WS3 · candidate · [V*] Verified-with-star · Licence: UNVERIFIED (research terms) · "
         "Access: open download (~1.8 Gigabyte) · Size: 7 events; ~16,000 tweets / 18,000 images"))

# ================= SUMMARY =================
doc.add_heading("Ek nazar mein — summary", level=1)
for line in [
    "Baarish/mausam (3): Global Precipitation Measurement IMERG, ERA5-Land, SMAP — sab [V] Verified, sab selected.",
    "Satellite nazar (3): Sentinel-1 (radar/SAR), Sentinel-2 (optical/MSI), MODIS (daily) — sab [V] Verified, sab selected.",
    "Glacier/GLOF (3): ITS_LIVE [V], HMAGLOFDB [D] (766 GLOFs, 1533-2025), GLOFNet [V*] — Himalaya-focused.",
    "Landslide (9): mix selected+candidate; India-specific wale (Kerala 2018, Bhuvan/ISRO) khaas keemti.",
    "Flood (5): Sen1Floods11, GEOID-Flood selected; India Flood Inventory [V] (1967-2023) India ke liye sona.",
    "Land-cover (2) + Social (1): support/corroboration ke candidates.",
]:
    pp = doc.add_paragraph(style="List Bullet"); pp.add_run(line)
f = doc.add_paragraph()
fr = f.add_run("Dobara yaad: 26 datasets = 13 selected + 13 candidate; 12 Verified [V] + 5 Verified-with-star "
               "[V*] + 9 Discovery-only [D]. Sab real registry entries hain — par is project mein kuch "
               "download/train nahi hua.")
fr.bold = True; fr.font.color.rgb = RED

# ================= GLOSSARY =================
doc.add_heading("Glossary — saare short-form ki full form (ek jagah)", level=1)
glossary = [
    ("SAR", "Synthetic Aperture Radar — kritrim-dvaar radar (baadal/raat mein bhi dekhne wala radar)"),
    ("InSAR", "Interferometric Synthetic Aperture Radar — zameen ka millimetre-level khisakna naapne wali radar technique"),
    ("EO", "Earth Observation — prithvi-nireekshan (satellite/sensor se zameen dekhna)"),
    ("EWS", "Early Warning System — poorva-chetavani pranaali"),
    ("DEM", "Digital Elevation Model — har jagah ki unchaai ka 3D data"),
    ("FS", "Factor of Safety — surakhsha-gunank (1 se neeche = slope failure)"),
    ("GLOF", "Glacial Lake Outburst Flood — himnad-jheel phatne se aayi baadh"),
    ("HMA", "High Mountain Asia — uchch-parvatiya Asia (Himalaya + aas-paas)"),
    ("ML", "Machine Learning — machine-seekh"),
    ("NLP", "Natural Language Processing — praakritik-bhaasha-prasanskaran"),
    ("RGB", "Red, Green, Blue — laal-hara-neela (3 basic colour band)"),
    ("WS", "Workstream — kaam-dhaara (WS1 physics, WS2 social, WS3 alert, WS4 optical, WS8 EO-anomaly)"),
    ("NASA", "National Aeronautics and Space Administration — amreeki antariksh sanstha"),
    ("JAXA", "Japan Aerospace Exploration Agency — japani antariksh sanstha"),
    ("JPL", "Jet Propulsion Laboratory (NASA) — jet-pranodan prayogshala"),
    ("ECMWF", "European Centre for Medium-Range Weather Forecasts"),
    ("C3S", "Copernicus Climate Change Service — jalvायु-parivartan seva"),
    ("ISRO", "Indian Space Research Organisation — bhaartiya antariksh anusandhान sangathan"),
    ("NRSC", "National Remote Sensing Centre (ISRO) — rashtriya door-samvedन kendra"),
    ("DLR", "Deutsches Zentrum fuer Luft- und Raumfahrt — jarman antariksh kendra"),
    ("GFZ", "GeoForschungsZentrum — jarman bhoo-vigyan anusandhान kendra"),
    ("ICIMOD", "International Centre for Integrated Mountain Development"),
    ("ITC", "Faculty of Geo-Information Science and Earth Observation, University of Twente"),
    ("GPM", "Global Precipitation Measurement — vaishvik varsha maapan"),
    ("IMERG", "Integrated Multi-satellitE Retrievals for GPM — kai satellite milakar varsha-product"),
    ("SMAP", "Soil Moisture Active Passive — mitti-nami naapne wala satellite"),
    ("MODIS", "Moderate Resolution Imaging Spectroradiometer — roz ka moti-detail global sensor"),
    ("MSI", "MultiSpectral Instrument (Sentinel-2) — bahu-varnakram upkaran"),
    ("NSIDC", "National Snow and Ice Data Center"),
    ("LP DAAC", "Land Processes Distributed Active Archive Center (NASA)"),
    ("CDSE", "Copernicus Data Space Ecosystem — Sentinel data ka portal"),
    ("ITS_LIVE", "Inter-mission Time Series of Land Ice Velocity and Elevation — glacier-speed data"),
    ("COOLR", "Cooperative Open Online Landslide Repository (NASA)"),
    ("IFI", "India Flood Inventory - Impacts"),
    ("UFO", "Urban Flood Observations — shehri baadh dataset"),
    ("SSL4EO-S12", "Self-Supervised Learning for Earth Observation, Sentinel-1 & -2"),
    ("reBEN", "refined BigEarthNet (version 2)"),
    ("CrisisMMD", "Crisis MultiModal Dataset — aapda bahu-madhyam dataset"),
    ("CrisisNLP", "Crisis Natural Language Processing dataset"),
    ("API", "Application Programming Interface — do software ke beech baat-cheet ka tarika"),
    ("CDS", "Climate Data Store (Copernicus)"),
    ("PPS", "Precipitation Processing System (NASA)"),
    ("STAC", "SpatioTemporal Asset Catalog — satellite data dhoondhne ka standard catalogue"),
    ("S3", "Simple Storage Service (Amazon Web Services / AWS) — cloud storage"),
    ("GEE", "Google Earth Engine — cloud pe satellite-data analysis platform"),
    ("GCS", "Google Cloud Storage"),
    ("HF", "Hugging Face — open-source Machine Learning / dataset platform"),
    ("CC BY 4.0", "Creative Commons Attribution 4.0 — credit do, free use karo"),
    ("CC BY-NC-ND 4.0", "Creative Commons Attribution-NonCommercial-NoDerivatives — credit do, non-commercial, bina badlाव"),
    ("CDLA-Permissive-1.0", "Community Data License Agreement - Permissive 1.0"),
    ("MIT licence", "Massachusetts Institute of Technology licence — bahut khula/free licence"),
    ("Apache-2.0", "Apache License 2.0 — ek open-source licence"),
    ("CSV", "Comma-Separated Values — simple spreadsheet/table file"),
    ("CVPRW", "Computer Vision and Pattern Recognition Workshops (ek conference)"),
    ("GB / GiB / TB / MB", "Gigabyte / Gibibyte / Terabyte / Megabyte — data size ki units"),
    ("I-D", "Intensity-Duration — baarish ki teevrata aur avadhi (landslide threshold ke liye)"),
]
gt = doc.add_table(rows=1, cols=2); gt.style = "Light List Accent 1"
gt.rows[0].cells[0].text = "Short form"; gt.rows[0].cells[1].text = "Full form (aur matlab)"
for cc in gt.rows[0].cells:
    for pp in cc.paragraphs:
        for rr in pp.runs: rr.bold = True
for sf, ff in glossary:
    c = gt.add_row().cells; c[0].text = sf; c[1].text = ff
    for pp in c[0].paragraphs:
        for rr in pp.runs: rr.bold = True

doc.save(OUT)
print("SAVED:", OUT); print("paragraphs:", len(doc.paragraphs), "glossary rows:", len(glossary))
