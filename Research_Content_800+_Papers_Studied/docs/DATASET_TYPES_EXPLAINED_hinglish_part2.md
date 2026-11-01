# DATASET TYPES EXPLAINED — Hinglish (PART 2: Types 9–16)

> Yeh **PART 2** hai. Part 1 (Types 1–8) is file me rehta hai:
> [`DATASET_TYPES_EXPLAINED_hinglish_part1.md`](<DATASET_TYPES_EXPLAINED_hinglish_part1.md>).
> *(Honest note: likhte waqt Part 1 file abhi workspace me physically present nahi mili — agar wo
> baad me banayi gayi hai to numbering yahin Type 9 se continue hoti hai.)*

---

## Padhne se pehle — teen honesty rules (poora document inhi par khada hai)

Bhai, ek smart junior ko main yeh teen baatein sabse pehle bolunga, kyunki inke bina baaki sab galat
samajh me aa jaayega:

1. **Kuch bhi download nahi hua.** `_CANON.md §0` bolta hai verbatim: *"No model has been trained and no
   dataset has been downloaded."* Toh neeche jo bhi size / N / count likha hai, wo **source me recorded**
   hai — humne khud measure nahi kiya. Jahan registry khud "UNVERIFIED" ya "named" bolta hai, main waise
   hi likhunga.
2. **Licenses mostly UNVERIFIED hain.** Registry me `[V]` / `[V*]` / `[D]` tags hain — `[D]` matlab sirf
   discovery, authoritative portal page khud fetch nahi hui. Jo bhi license likha hai wo "source records X"
   hai, **verified fact nahi**. Portal pe jaa ke verify karna padega.
3. **Koi performance number TRINETRA ka measured result nahi hai.** Accuracy / skill / latency / false-alarm
   — jahan dikhe, wo ya to doosre paper ka source-reported number hai, ya "not measured". Hum apni koi
   accuracy claim nahi kar rahe (Rule R16 — eval admission gate se pehle no claim).

Jahan main number nahi de sakta, main saaf bolunga: **"source me recorded"** ya **"verify karna padega"** ya
**"not measured"**. Fabricate kuch nahi karunga.

---

# TYPE 9 — Seismic / Geophone / Ground-vibration sensors (rockfall + landslide trigger)

### (a) Yeh hota kya hai
Zameen hilti hai to woh **seismic waves** generate karti hai. Earthquake, landslide, rockfall, debris-flow —
sabka apna ek vibration signature hota hai. Ek geophone/seismometer in vibrations ko continuous time-series
me record karta hai. Toh "seismic data" basically ground ki hilne ki recording hai — image nahi, **waveform
hai** (amplitude vs time).

### (b) Kaise collect hota hai (sensor / platform / physics)
- **Geophone**: ek coil + magnet. Zameen hilti hai → coil move karta hai → induced voltage ∝ ground
  **velocity**. Sasta, rugged, passive. Isi liye low-cost slope-monitoring me pasand kiya jaata hai.
- **Seismometer / accelerometer (MEMS)**: 3-component (N-S, E-W, vertical) ground motion. MEMS waala sasta
  aur phone-grade hota hai; research-grade broadband mehnga.
- **Physics**: P-wave (fast, compressional) pehle aata hai, S-wave (slow, shear) baad me. Dono ke beech ka
  time-gap distance batata hai. Rockfall/landslide ka signal earthquake se alag "emergent" (dheere build-up)
  hota hai, impulsive nahi. Debris-flow ka signal ek distinct high-frequency rumble hota hai.

### (c) Kya measure hota hai + units + resolution + coverage
- Ground **velocity** (m/s) ya **acceleration** (m/s²), sampling typically 100 Hz ya zyada (yeh general
  domain knowledge hai; hamare registry datasets ka exact sampling source me recorded nahi).
- Registry me jo seismic datasets hain, wo **earthquake waveform** type hain (rockfall-specific nahi):
  - **D147 CEED** (California EQ Event) — waveforms + picks + polarity, 2000–2024 (NCEDC+SCEDC), free/open `[D]`.
  - **D148 STEAD** (Stanford EQ) — 3-component waveforms, "millions" (count **"named"**, from citing abstract), free/open `[D]`.
  - **D149 POSEIDON** — event catalog + energy, 2.8M events / 30 yr, free/open `[D]`.
  - **D150 MultiSeismo** — waveforms + intensity maps + metadata, 16K+ events 2010–23, free/open (reported) `[D]`.

### (d) Strengths + limitations
- **Strengths**: raat-din chalta hai, cloud/weather se farq nahi padta (optical ka ulta), aur rockfall/
  landslide ka trigger **seconds-to-minutes early** pakad sakta hai — yeh real "early warning" value hai.
- **Limitations**: localise karna mushkil (ek geophone sirf "kuch hila" batata hai, "kahan + kitna" nahi —
  uske liye array chahiye). Background noise (traffic, river, wind) bahut aata hai. Sabse bada honest point:
  **registry me koi rockfall/landslide-labelled geophone dataset nahi mila** — jo hai wo earthquake waveform
  hai. Toh rockfall trigger ke liye yeh ek **documented GAP** hai; apna normal-reference log collect karna
  padega (same philosophy jaise WS8 anomaly me — `DATASETS.md` WS8 notes).

### (e) TRINETRA me kyun / kahan
- **Hazard**: rockfall / landslide / debris-flow trigger detection, aur GLOF/dam-break ka seismic rumble.
- **WS / model**: WS8 (anomaly) + geo-physics stack (WS1b) ke liye ek trigger covariate. Earthquake sets
  (D147–D150) sirf **method development** ke liye — "normal-only" se anomaly detect karne ka tareeka seekhne
  ke liye, deployment operating-point ke liye nahi.
- **Example real D-ID**: D148 STEAD / D147 CEED (method-dev waveforms). Rockfall-specific label GAP hai.

### (f) Leakage / split handling (cross-ref ch12)
- Seismic time-series me **temporal block CV** chahiye — random split karoge to same event ke pehle/baad ke
  samples train aur test dono me chale jaate hain → leakage → skill overstate.
- ch12 ka core verdict: random CV **overstates** skill; isliye spatial/temporal block CV mandatory
  (triangulated across arXiv 2608.12422, 2608.22293, 2610.08227 — `_CANON §6`).
- WS8 anomaly benches (D147–D150 ki category) me documented flaws hain (point-adjust inflation, trivial
  anomalies) — isliye real false-alarm/sensor-day apne logs se hi aayega, benchmark se nahi.

---

# TYPE 10 — River gauge / Hydrology / Water-level + LSPIV (camera-based surface velocimetry)

### (a) Yeh hota kya hai
Do alag cheezein ek hi family me:
1. **River gauge / hydrology data** — gauging station pe water **level (stage)** aur **discharge** (m³/s) ki
   time-series. Yeh flood ka direct physical ground-truth hai.
2. **LSPIV** (Large-Scale Particle Image Velocimetry) — ek camera river ki surface ko dekhta hai, aur paani
   pe tairte patterns/texture ko frame-to-frame track karke **surface velocity** nikaalta hai. Phir velocity
   × cross-section → discharge estimate. Yeh "sasta gauge" banane ka tareeka hai.

### (b) Kaise collect hota hai (sensor / platform / physics)
- **Gauge**: pressure transducer / radar level sensor / staff gauge, fixed station pe. Discharge rating curve
  (stage→discharge mapping) se banta hai.
- **LSPIV**: fixed camera (ya even phone) → consecutive frames → cross-correlation / optical-flow se surface
  pattern ka displacement → divide by Δt → surface velocity. **Physics**: surface velocity ko ek coefficient
  (≈0.85 typical) se multiply karke depth-averaged velocity milti hai; phir Q = v × A.
- TRINETRA ka plan: **"River Eye" LSPIV node** (feature **F-09**, `FEATURES.md`), ek ≤₹2000 [EST] camera node
  jo surface-velocity + uncertainty + gap-filling kare. Refs source me recorded: 2507.20102, 2312.06461
  (F-09); aur reading notes me 1607.04139 (unseeded LSPIV) + 2605.14645 (wave-contamination problem).

### (c) Kya measure hota hai + units + resolution + coverage
- Gauge: stage (m), discharge (m³/s). LSPIV: surface velocity (m/s) → discharge (m³/s).
- Registry datasets:
  - **D22 India Flood Inventory–Impacts (IFI)** — district-level flood events, 1967–2023, **CC-BY-4.0 `[V]`**,
    ~1.9 MB (3 CSVs). Yeh hamara **sabse India-specific verified** flood-event label source hai.
  - **D25 INDOFLOODS** — Indian station-discharge flood events, Zenodo 14584654, license UNVERIFIED `[D]`.
  - **D53 CWC / India-WRIS** — river discharge + stage, **cost "varies / often restricted"** (Govt-India),
    `[D]`. Yeh ek central **access risk** hai — Himalayan rating curves calibrate karne ke liye chahiye, par
    frequently restricted/paid, isliye kabhi `selected` nahi hua.
  - **D52 ICIMOD HKH** — glacial-lake / GLOF inventory, Himalaya, ICIMOD open (indic.) `[D]`.

### (d) Strengths + limitations
- **Strengths**: gauge = sabse direct, physically-interpretable flood signal. LSPIV = ultra-sasta, remote
  Himalayan nallah pe laga sakte ho jahan koi official gauge nahi hai.
- **Limitations**: official Indian gauge data (D53) restricted/paid → ungauged catchments ki badi problem.
  LSPIV ki apni dikkatein: **wave-contamination** (lehrein false velocity deti hain, 2605.14645), unseeded
  surface pe texture kam (1607.04139), raat ko visibility, aur sabse honest point — **G3 open gap**: sub-₹2k
  camera-LSPIV ki accuracy vs ek real gauge par koi cited paper nahi mila (`04_synthesis.md` G3), aur yeh
  **not measured** hai. Toh River-Eye accuracy abhi ek **[HYPOTHESIS]**, claim nahi.

### (e) TRINETRA me kyun / kahan
- **Hazard**: flash-flood / monsoon flood / GLOF surge ka direct water-level signal.
- **WS / model**: WS1/WS3 (flood labels + nowcast covariate), WS4 (River-Eye camera node). D22 IFI =
  primary Indian flood-event label/impact target.
- **Example real D-ID**: D22 IFI (verified, CC-BY), D53 CWC (restricted — early-action verify).

### (f) Leakage / split handling (cross-ref ch12)
- Indian event labels (D22, D25) ke liye **temporal + leave-one-region-out** split (`DATASETS.md` matrix).
- Hydrology covariate time-series ke liye **temporal block CV, monsoon-season held-out** — warna same
  monsoon ke din train+test dono me leak honge.

---

# TYPE 11 — CCTV / fixed-camera video (fire + smoke)

### (a) Yeh hota kya hai
Ek fixed camera (watch-tower, pole, building) continuous video deti hai; usme fire/smoke detect karna hai.
Yeh TRINETRA ka fire-detection ka **primary perception stream** hai (WS4).

### (b) Kaise collect hota hai (sensor / platform / physics)
- **Platform**: fixed RGB (kabhi IR/thermal) camera, network pe stream. Fire ka physics signature: flame ka
  color/intensity, smoke ka texture/motion, aur — most importantly — **flicker**.
- **Flicker / Strouhal physics**: pool-fire ek characteristic puffing frequency pe "phadphadaata" hai:
  **f ≈ 1.5 / √D** (D = plume diameter), yeh **Strouhal law** (Cetegen & Ahmed 1993, EF-08, Class-A in
  `_CANON §4`). Real fire **persistently flickers**; ek glint/headlight sirf 1 frame ka hota hai. Isi se
  model false-alarm suppress karta hai.
- **FPS + aliasing problem**: agar camera low-fps pe chalti hai (CCTV me common), to true flicker frequency
  **alias** ho jaati hai — f_obs = |f_true − fs·round(f_true/fs)| (B-05 de-aliased flicker idea). Yeh exactly
  wo failure mode hai jahan low-fps CCTV flicker ko galat padhta hai. Isliye TRINETRA me yeh novel ND flicker
  term **Class-C, default OFF** rakha gaya hai, with Class-A Strouhal fallback (Rule R20).

### (c) Frame vs video labels + units + resolution + coverage
- **Frame labels**: har ek image pe fire/smoke bbox ya class. **Video labels**: time-indexed — kis second se
  ignition dikha. Dono ka farq important hai: frame-only se temporal flicker nahi seekh sakte.
- Registry fire-CCTV datasets (sab `[D]`, licenses NOT verified):
  - **D35 ↔ D113 FIgLib** (Fire Ignition Library) — fixed-cam HPWREN smoke images, **~25k** (recorded),
    time-indexed ignition, public (not confirmed), src 2112.08598.
  - **D36 ↔ D117 PYRONEAR-2025** — camera-network images + video, **~50k images / ~150k annotations /
    640 fires** ("named", citing abstract se), open-source (confirm), src 2402.05349. Registry me yeh
    **best-documented** fire-CCTV set hai → isi ko FireSmokeNet ka training data chuna gaya (`04a` D36/D117).
  - **D37 ↔ D120 D-Fire** — fire+smoke bbox images, **~21k** ("named"), MIT (not confirmed), src 2510.10108.
- **FPS/resolution**: camera-native RGB; exact fps/resolution source me recorded nahi → "verify karna padega".

### (d) Strengths + limitations
- **Strengths**: direct visual confirmation, flicker physics interpretable, temporal window se false-alarm
  (glint/headlight) alag ho jaate hain.
- **Limitations**: night/IR domain shift, smoke-only vs flame-only ambiguity, **low-fps aliased flicker**,
  aur sabse bada — PYRONEAR/FIgLib/D-Fire sab **Europe/US-centric** hain → Indian CCTV pe domain shift. Fixed
  camera ki **leakage trap**: same camera ke frames train+test me gaye to model scene memorize kar lega.
- **Model**: FireSmokeNet (`deep/fire_cnn.py`) — per-frame CNN → temporal GRU → {fire, smoke} logits + ek
  auxiliary **flicker_hz** head. Humari accuracy: **not measured** (torch layer GPU pe run nahi hui — `_CANON §2`).

### (e) TRINETRA me kyun / kahan
- **Hazard**: fire / smoke early detection.
- **WS / model**: WS4, FireSmokeNet; plus WS1a fire-physics gate (Heskestad/Byram/Strouhal) inference pe.
- **Example real D-ID**: D36/D117 PYRONEAR-2025 (training), D35/D113 FIgLib, D37/D120 D-Fire.

### (f) Leakage / split handling (cross-ref ch12)
- **By-site / by-fire hold-out** mandatory (fixed-camera leakage avoid karne ke liye) — `04a` D36 split
  guidance.
- Zero-shot fire eval sets (D99 WildFireCan, D100 AI4Fire) me author-reported leakage/label flaws hain →
  training ke liye nahi, aur bharosa nahi; internal leakage-free held-out set curate karo (D-011 plan).

---

# TYPE 12 — UAV / Drone imagery

### (a) Yeh hota kya hai
Drone (UAV) se aerial imagery — RGB aur/ya thermal (IR). Upar se fire/smoke/flood/landslide ka bird's-eye
view. Fixed CCTV se alag angle, alag scale.

### (b) Kaise collect hota hai (sensor / platform / physics)
- **Platform**: multirotor/fixed-wing drone with RGB + optional thermal (IR) camera. Thermal camera scene ki
  **temperature** (apparent) deti hai — fire IR me bright dikhta hai even jab visible smoke se dhaka ho.
- **Physics**: IR band me hot pixel = active fire-front; RGB me smoke plume ka shape/spread. Aerial view se
  fire-front **perimeter** aur spread direction mil jaata hai (jo ground camera se nahi milta).

### (c) Kya measure hota hai + units + resolution + coverage
- RGB reflectance + thermal (apparent temp / DN). Resolution flight-altitude pe depend karta hai (cm–m).
- Registry UAV/aerial datasets (sab `[D]`, licenses not verified):
  - **D42 FLAME** — aerial RGB + thermal (pile-burn), IEEE DataPort terms (confirm), src 2012.14036.
  - **D43 WIT-UAS** — IR thermal wildland-fire (crew/asset detection), license not visible, src 2312.09159.
  - **D121 AFSE** (Aerial Fire & Smoke Essential) — aerial images, "research dataset", src 2501.08639.
  - **D109 WFDroneBench** — risk maps + **7,746 placement scenarios** (synthetic), not stated, src 2609.11829.

### (d) Strengths + limitations
- **Strengths**: thermal se smoke ke peeche ka fire dikhta hai; aerial se spread/perimeter; flexible
  re-deploy.
- **Limitations**: drone endurance/weather limited, operator chahiye (always-on nahi), aur **domain shift** —
  aerial/360°/satellite sets ko fixed ground CCTV ke saath mix karoge to cross-domain leakage ka risk hai
  (`DATASETS.md` P8 note explicitly warns). D42 IEEE DataPort terms confirm karne padenge. Privacy +
  **C7 (no raw-video egress)** constraint drone footage pe bhi lagta hai.

### (e) TRINETRA me kyun / kahan
- **Hazard**: fire-front mapping, flood extent, landslide scarp — supplementary aerial view.
- **WS / model**: WS4 (perception) ka aerial complement; deployment/ops planning (WFDroneBench).
- **Example real D-ID**: D42 FLAME (RGB+thermal), D43 WIT-UAS (IR).

### (f) Leakage / split handling (cross-ref ch12)
- Flight/site-level hold-out (ek hi flight ke overlapping frames train+test me mat jaane do).
- Aerial sets ko ground-CCTV eval me mat milao — domain-shift leakage; agar transfer karna hai to usko
  explicitly **transfer-stress** test maano (ch12 transfer protocol), headline number nahi.

---

# TYPE 13 — Low-cost IoT ground sensors (tilt, rain-gauge, temperature, LoRa telemetry)

### (a) Yeh hota kya hai
Sasta, battery/solar-powered ground node jo physical quantities measure karta hai aur LoRa radio se
telemetry bhejta hai. TRINETRA ka **≤₹2000/node (C2)** constraint ka dil yahi hai — bahut saare saste nodes
> ek mehnga station.

### (b) Kaise collect hota hai (sensor / platform / physics)
- **Tilt / inclinometer / accelerometer**: slope ka angle change → landslide creep ka early sign.
- **Rain gauge** (tipping-bucket): rainfall intensity (mm/hr) + accumulation (mm) → Caine I–D threshold ka
  direct input (landslide-rainfall physics, `_CANON §4`).
- **Temperature / humidity / gas (MOX)**: fire ke pehle ka thermal/gas signature.
- **LoRa telemetry**: long-range, low-power radio. TRINETRA plan: band **IN865–867 MHz**, chip **SX1262**
  (`_CANON §8`). Nodes: **Node A "Slope Sentinel" ≈ ₹1,930 [EST]**, **Node B "River Eye" ≈ ₹1,980 [EST]** —
  dono ₹ figures **[EST]** hain (suppliers ne HTTP 403 diya), toh ≤₹2000 gate **abhi enforce nahi** ho
  sakta jab tak live-verify na ho.

### (c) Kya measure hota hai + units + resolution + coverage
- Tilt (degrees/milli-deg), rainfall (mm, mm/hr), temperature (°C), gas (ppm / MOX resistance ratio),
  LoRa link (RSSI dBm, SNR dB, PDR %).
- Registry calibration/IoT datasets (sab `[D]`, none fire-labelled):
  - **D28 UCI Gas Sensor Array Drift** — MOX e-nose long-term **drift** benchmark, CC-BY-4.0 (confirm),
    archive.ics.uci.edu/224. Yeh hamare gas-sensor delta/baseline-normalization design ke peeche hai.
  - **D29 Low-Cost Indoor AQ Calibration** — 6-mo, 5 locations, low-cost + reference AQ, UNVERIFIED,
    src 2610.11236.
  - **D30 RESPIRE India CO** — India multi-site/season/sensor CO calibration, UNVERIFIED, github
    purushottamkar/respire. India-reality anchor (season/site/unit drift).
  - **D95/D106 AQ-SDR** — 23,737 low-cost + reference stations, "public when published" (shayad abhi live
    nahi), src 2508.02724.
  - **D96 SensEURCity**, **D98 LoRa 2.4 GHz ToF ranging (+T/RH)** — breadth ke liye, `[D]`.

### (d) Strengths + limitations
- **Strengths**: ultra-sasta, dense deployment, offline-first (C1) LoRa path, direct physical trigger (tilt/
  rain).
- **Limitations**: **sensor drift** sabse badi reality (D28/D29/D30 isiliye zaroori); low-cost = noisy +
  outliers normal; LoRa storm me down ho sakta hai (missing-modality case). Aur sabse honest: **koi
  fire-detection-labelled public IoT sensor dataset nahi mila** — yeh **documented GAP** hai (`DATASETS.md`
  WS7b note). Toh fire-trigger labels apne **normal-only + safe-stimulus logs** se collect karne padenge
  (TEST_PROTOCOL). ₹ figures [EST], not live-verified.

### (e) TRINETRA me kyun / kahan
- **Hazard**: slope creep (tilt) → landslide; rainfall → I–D landslide trigger; gas/temp → fire; river level
  (Node B).
- **WS / model**: WS7 (IoT), WS1b (geo-physics trigger), WS3 (offline alert path).
- **Example real D-ID**: D28 UCI Gas-Drift, D30 RESPIRE India CO. (Node A/B BOM = `_CANON §8`.)

### (f) Leakage / split handling (cross-ref ch12)
- **Normal-reference policy**: anomaly operating-point (false-alarms/sensor-day) sirf apne normal-only logs
  se, benchmark se nahi (ch12).
- Calibration sets ko **site/unit/season block** se split karo — same sensor ka data train+test me gaya to
  drift-correction "cheat" kar ke event ko explain-away kar dega (D106 ka documented flaw: reference-free
  correction true event ko bhi mita sakta hai).

---

# TYPE 14 — Social-media / crisis text + images (CrisisMMD-type)

### (a) Yeh hota kya hai
Disaster ke dauran log Twitter/X etc. pe text + images post karte hain. Crisis datasets in posts ko label
karke dete hain (informative / not, damage severity, etc.). TRINETRA me yeh ek **low-trust advisory channel**
hai — primary trigger nahi.

### (b) Kaise collect hota hai (scraping, noise)
- **Collection**: platform API / scraping se tweets+images, phir human/crowd annotation. Bahut **noise**:
  rumors, duplicates, off-topic, aur recycled/old media.
- **ToS / ID-only redistribution**: platform terms-of-service aksar sirf **tweet-IDs** redistribute karne
  dete hain, raw text nahi (D112/D154 GeoCoV19 "ID-only likely", `DATASETS.md` P19 note). Toh dataset ko
  "rehydrate" karna padta hai aur kuch posts tab tak delete ho chuke hote hain.

### (c) Kya hota hai + size + coverage
- Text + image, event-level labelled. Registry crisis datasets:
  - **D16 CrisisMMD / CrisisNLP** — 7 events (2017), **~16k tweets / 18k images**, license = generic
    "Terms of use" (UNVERIFIED) `[V*]`. ENGLISH-centric, **koi India event nahi** (nearest: 2017 Sri Lanka).
  - **D151 CrisisBench** — 166.1k + 141.5k tweets, 8 sets, free/open `[D]`.
  - **D152 CrisisMMD** (↔D16), **D153 MEDIC** — 71,198 images multi-task, **D155 HumAID/HUMAID-NER** — 60k
    tweets / ~175k NER spans, **D154/D112 GeoCoV19** — 524M+ tweet IDs (ID-only).
  - **D83 NepOOC** — 1,090 Nepali-English out-of-context pairs — multilingual relevance, par small.

### (d) Strengths + limitations
- **Strengths**: real-time, ground-level eyewitness signal, wide coverage, free.
- **Limitations**: noise + rumors + recycled media, **English-centric** (Indian-language / code-mixed crisis
  data ek **documented GAP** hai, `DATASETS.md` D16 note), ToS/ID-only redistribution → reproducibility
  problem. Aur sabse important governance point: **Rule R19 — advisory, human-in-the-loop, NEVER autonomous
  public alert.** Social signal ko kabhi akela trigger nahi banne dena; corroborate karo (`_CANON §6`:
  social-media = low-trust advisory, must be corroborated).

### (e) TRINETRA me kyun / kahan
- **Hazard**: situational awareness, impact reports (fire/flood/landslide), cross-check.
- **WS / model**: WS2 (misinformation) + WS3 (alerting) ka advisory input only.
- **Example real D-ID**: D16 CrisisMMD, D155 HumAID.

### (f) Leakage / split handling (cross-ref ch12)
- **Leave-one-event-out** split (ek event ke tweets train+test me mat milao — warna event-specific wording
  memorize ho jaata hai), aur **never autonomous** (R19) — `DATASETS.md` matrix.

---

# TYPE 15 — Deepfake / manipulated-media datasets (FaceForensics++ / DFDC)

### (a) Yeh hota kya hai
Face-swap / reenactment / fully-synthetic video+image forensic datasets. Inpe train karke ek detector
("AuthenticityNet") banta hai jo bataaye ki inbound media fake toh nahi (WS2).

### (b) Kaise collect hota hai
- Lab-generated manipulated faces (DeepFakes/Face2Face/FaceSwap/NeuralTextures), multiple compression levels
  (c0/c23/c40). Original consented actors + generated fakes. Yeh **EULA-gated** hote hain (signed research
  agreement chahiye).

### (c) Kya hota hai + size + coverage
- Registry deepfake sets (sab `[D]`, EULA/restricted):
  - **D68 ↔ D159 FaceForensics++ (FF++)** — face-manip video (DF/F2F/FS/NT) at c0/c23/c40; **research-only
    EULA, signed access request**. AuthenticityNet ka chosen primary forensic set (`04a` D68/D159) —
    **ACCESS BLOCKED until EULA signed; download attempt nahi hua**.
  - **D70 ↔ D158 DFDC** — large face video, consented actors, **DFDC EULA (actor-likeness agreement)**.
  - **D77 CCDF** ⚑ — surveillance deepfakes, 1,840 vids (460 real / 1,380 gen), Sora2/VEO3.1/Grok, 16 crime/
    accident categories; "10 SOTA detectors UNRELIABLE on it" (source-reported), src 2610.07939. Yeh disaster/
    accident + CCTV-corroboration threat ke sabse **closest** hai.

### (d) WS2 kyun chahiye + EULA restrictions + 0.4 reliability cap
- **WS2 kyun**: disaster ke time fabricated/out-of-context media panic phaila sakta hai. Detector chahiye jo
  flag kare — par **believe nahi** kare blindly.
- **EULA restrictions**: FF++ (D159), DFDC (D158), Celeb-DF (D69), DF40 (D72), FakeAVCeleb (D160) sab signed
  research agreement maangte hain. Face data → consent/privacy constraints; **method development only, koi
  deceptive media create nahi** (ch14). Download kuch nahi hua.
- **0.4 reliability cap [CONFIRMED by code]**: fusion adapter deepfake ki trust **hard-cap 0.40** pe rakhta
  hai — `adapters.py` `_POLICY["deepfake"] = (0.30 default, 0.40 cap, Class DATA)`, aur model config
  `max_reliability = 0.4` me bhi — matlab **do jagah** enforce. Ek unit test assert karta hai ki 0.99
  reliability bhi clip ho ke ≤0.4 ho jaati hai, aur ek 0.8-prob deepfake decision ko dominate nahi kar sakta.
  Yeh `_CANON §6` ("deepfake/social = low-trust advisory") ka code-level enforcement hai, Rule R19 ke saath.

### (e) TRINETRA me kyun / kahan
- **Hazard**: disaster misinformation / fabricated accident footage.
- **WS / model**: WS2, AuthenticityNet (`deep/deepfake_net.py`) — lowest-trust input, r ≤ 0.4, kabhi gate
  nahi karta (`05_MODELS.md`).
- **Example real D-ID**: D68/D159 FF++ (BLOCKED-EULA), D77 CCDF (closest-to-threat).

### (f) Leakage / split handling (cross-ref ch12)
- In-distribution accuracy deployment ko **overstate** karti hai → **cross-generator + degraded** evaluation
  mandatory (`DATASETS.md` WS2 note). FF++ me identities reused → cross-dataset generalization weak; isliye
  train-generator aur test-generator alag rakho. Humari koi accuracy: **not measured**.

---

# TYPE 16 — EO foundation-model pretraining corpora (SSL4EO-S12 etc.)

### (a) Yeh hota kya hai
Bahut bada **unlabeled** satellite imagery corpus, jisse ek EO (Earth-Observation) encoder ko
**self-supervised** (SSL) tareeke se pretrain kiya jaata hai. Labels ki zarurat nahi — model khud image ki
structure seekhta hai (masked patches predict karna, contrastive, etc.).

### (b) Kaise collect hota hai + kyun self-supervised
- **Collection**: global Sentinel-1 (SAR) + Sentinel-2 (optical) tiles, multiple seasons, bina kisi hazard
  label ke.
- **Kyun SSL**: hazard labels (landslide/GLOF/flood) **bahut thin** hain in-region. Unlabeled EO data crores
  me free available hai. Toh pehle unlabeled se ek strong encoder pretrain karo, phir chhote labelled set pe
  fine-tune karo — yeh data-efficient hai aur domain-shift thoda sambhalta hai. Mandatory baselines
  (persistence C-03 + GBDT C-02 + tuned U-Net) ke baad hi foundation model apni compute "earn" karta hai
  (`DATASETS.md` cross-eval plan).

### (c) Kya hota hai + size + coverage
- **D10 SSL4EO-S12** — S1 GRD + S2 (L1C+L2A) **unlabeled** SSL corpus, **251,079 locations × 4 seasons
  (~1.5 TB raw)**, code **Apache-2.0** / data+weights **CC-BY-4.0** `[V]`. Global incl. Himalaya. Hamara
  **primary SSL pretraining corpus** — compressed 8-bit variant / regional subset use karenge taaki Kaggle
  budget (C3 ≤30 GPU-h/week) me fit ho.
- **D13 BigEarthNet v2 (reBEN)** — 549,488 S1+S2 patches (~110 GiB), **CDLA-Permissive-1.0** `[V]`, par
  **EUROPE-ONLY** → pretrain/transfer ke liye theek, Himalayan ground-truth kabhi nahi.
- **D14 EuroSAT** — 27,000 imgs, MIT `[V]`, Europe-only → sanity/debug + worst-group fixture.

> **Honest flag — "MajorTOM"**: user ne MajorTOM corpus mention kiya, par **MajorTOM registry ke kisi bhi
> source (`DATASETS.md`, `DATASETS_CATALOGUE.md`, `04/04a`) me nahi mila**. Toh main uspe koi size/license
> nahi likh sakta — yeh "not found in sources" hai. Agar add karna hai to pehle portal pe verify karna
> padega. Jo SSL corpora sources me confirm hain: **D10 SSL4EO-S12** (primary) aur **D13 BigEarthNet**.

### (d) Strengths + limitations
- **Strengths**: label-free, massive, global, data-efficient downstream, clean-ish license (SSL4EO CC-BY,
  BigEarthNet CDLA-Permissive).
- **Limitations**: ~1.5 TB → storage/compute heavy (subset chahiye); sampling kuch regions under-represent
  kar sakta hai; BigEarthNet/EuroSAT **Europe-only** → Himalayan representative nahi, sirf transfer.

### (e) TRINETRA me kyun / kahan
- **Hazard**: indirect — flood/landslide/GLOF detection encoders ka backbone.
- **WS / model**: WS1/WS8, masked-InSAR/EO encoder ka SSL pretraining (ch05/06). D10/D13 **candidates**
  (selected nahi — selection count 13 pe), par load-bearing feeders.
- **Example real D-ID**: D10 SSL4EO-S12 (primary), D13 BigEarthNet.

### (f) Leakage / split handling (cross-ref ch12)
- **Pretrain-only; eval kahin aur** — pretraining corpus ka koi tile labelled test-set me nahi jaana chahiye,
  warna downstream skill overstate hoga (`DATASETS.md` matrix: "pretrain only; eval elsewhere"). Downstream
  pe wahi spatial-block CV (ch12) lagta hai.

---

# CLOSE — Multi-sensor fusion kaise + kyun (physics-grounded)

### Kyun fusion?
Simple baat: **ek modality ka blind-spot doosri bhar deti hai.** Har sensor ki ek physical limitation hai, aur
wo limitations **overlap nahi karti** — isiliye saath me daalne pe system robust ho jaata hai. Yeh koi "zyada
data = behtar" waali bhed-chaal nahi; yeh physics-grounded complementarity hai:

- **Monsoon me optical (S2/CCTV) cloud se andha** ho jaata hai → **SAR (S1, Type kyunki C-band) baadlon ke
  paar dekh leta hai** (all-weather). Isiliye optical–SAR fusion (DC-09) flood me core hai.
- **Camera (Type 11) raat ko / smoke me kamzor** → **thermal/IR drone (Type 12)** smoke ke peeche fire dekh
  leta hai; aur **gas/temp IoT (Type 13)** chemical signature deta hai.
- **Seismic (Type 9) "kuch hila" batata hai par "kahan+kitna" nahi** → **tilt + rain-gauge IoT (Type 13)**
  slope ka local trigger context deta hai; **InSAR/ITS_LIVE** deformation/velocity precursor; **river gauge/
  LSPIV (Type 10)** downstream surge confirm karta hai.
- **Satellite coarse + delayed** → **ground IoT + CCTV fast + local** → temporal + spatial scales complement.
- **Social media (Type 14) + deepfake-check (Type 15)** sirf **low-trust corroboration** dete hain, physics/
  sensor ko override nahi (deepfake r ≤ 0.4, R19 never autonomous).

### Kaise (TRINETRA ka tareeka)
- Har expert ka output ek `ExpertOutput` ban-ta hai with **class (A/B/C/DATA) + reliability + uncertainty +
  consistency** (`_CANON §4`, meta-fusion WS5). Fusion precision-weighted mean (FM-1 default) / gated-mixture
  karta hai, aur deepfake jaise low-trust input structurally chhota weight (`r·c·exp(−u/τ)`) paata hai.
- **Missing-modality by design (DC-05)**: har sensor ko drop karke evaluate karo (cloud → S2 gaya; storm →
  LoRa/power gaya) — mask-conditional conformal + availability-aware inputs se. Kyunki real deployment me koi
  na koi modality aksar missing hogi.
- Final decision: `level = max(conformal_level(risk, p*), shield_floor)`, p* ≈ 0.0476 (C_FA=5, C_miss=100) —
  cost-asymmetric, miss ko false-alarm se zyada mehnga maana (`_CANON §4`).

---

# HONEST NOTE (yeh poore document pe laagu — soften mat karna)

- **Koi dataset download nahi hua.** `_CANON §0`: *"No model has been trained and no dataset has been
  downloaded."* Upar ke saare size/N/count **source me recorded** hain, humne measure nahi kiye; jahan
  registry "named"/"UNVERIFIED" bolta hai waisa hi likha hai.
- **Licenses verify karni hain.** Zyadatar `[D]` discovery-only hain — portal page khud fetch nahi hui.
  FF++ (D159) / DFDC (D158) / FakeAVCeleb (D160) **EULA-gated**; CWC (D53) / IMD (D47) often restricted/paid;
  Indian govt portals (Bhuvan/MOSDAC/NRSC/GSI) JS-driven → **manual verification** backlog.
- **Kuch metrics measured nahi.** River-Eye LSPIV accuracy (G3), FireSmokeNet/AuthenticityNet skill,
  false-alarm/sensor-day — sab **not measured** / `[HYPOTHESIS]`. Jo numbers doosre papers ke hain wo
  source-reported hain, hamara result nahi (Rule R16).
- **Documented GAPs**: rockfall-labelled geophone data (Type 9), fire-labelled IoT sensor data (Type 13),
  Indian-language crisis data (Type 14), fire-specific synthetic/deepfake corpus (Type 15), aur "MajorTOM"
  (Type 16) — yeh registry me **nahi mila**, verify/collect karna padega.
