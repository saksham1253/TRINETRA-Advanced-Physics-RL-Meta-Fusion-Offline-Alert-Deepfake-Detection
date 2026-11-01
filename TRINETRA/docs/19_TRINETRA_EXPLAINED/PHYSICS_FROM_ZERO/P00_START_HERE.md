# TRINETRA Physics — Zero se samjho (P00: shuru yahan se)

**Ye book kis ke liye hai?** Us insaan ke liye jisne physics kabhi padhi hi nahi, ya bhool gaya. Judge, mentor, naya team member, ya ghar ka koi
bhi. Har formula yahan **teen baar** samjhaya gaya hai: pehle ek roz-marra ki misaal se, phir step-by-step derivation se, aur phir
**asli code se calculate kiye hue number** se.

**Ye book kya nahi hai?** Ye koi naya result nahi hai. Saare "OUR RESULT" numbers `TRINETRA/results/` se liye gaye hain. Saare worked examples
repo ke Python functions chala ke nikale gaye hain (`tools/export_golden.py` jaise), haath se nahi. Agar koi number "WORKED EXAMPLE" likha hai,
to wo samjhane ke liye hai, measurement nahi.

## Chapters

| File | Kya hai | Kitna time |
|---|---|---|
| **P00_START_HERE.md** | ye file: basics jo baaki sab ke liye chahiye | 20 min |
| **P01_LANDSLIDE.md** | pahad kyun girta hai: FS, barish ka paani (Iverson), Caine line, Fukuzono, geo gate | 60 min |
| **P02_FIRE.md** | aag ki physics: flame height, plume, hawa vs aag (Byram), flicker, garmi ki roshni, dhuan | 45 min |
| **P03_DECISION.md** | alarm kab bajana hai: cost-loss p*, base rate, calibration, noisy-OR, shield | 40 min |
| **P04_RADIO_LORA.md** | internet band hone par warning kaise pahunche: dB, path loss, LoRa airtime, Fresnel zone, siren | 45 min |
| **P05_GLOF_AND_PINN.md** | glacial lake flood ke power laws, aur physics-informed neural network | 30 min |
| **P06_SELF_TEST.md** | sawaal-jawab, aur ek page ka "sab kuch ek jagah" summary | 20 min |
| `fig/` | saare graphs (`tools/make_figures.py` se bane, repo ke code se) | – |

**Padhne ka order:** P00 → P01 → P03 → P02 → P04 → P05 → P06. Agar sirf 15 minute hain: har chapter ka "Ek line me" box aur figures dekho.

---

## 1. Physics ka matlab hi kya hai, aur TRINETRA ko iski zaroorat kyun?

Machine learning (jaise hamara fire CNN) **data se pattern seekhta hai**. Agar data me 10,000 aag ki photos hain, to model "aag jaisi dikhne
wali cheez" pehchaan leta hai. Problem: jo data me nahi tha, wahan model andha hai. Hamara deepfake model is ka seedha example hai: training
ke source par AUC 0.961, naye source par 0.450 (sikka uchhalne se bhi kharab). Ye OUR RESULT hai (`results/master_merged/master.json`).

Physics **data se nahi, prakriti ke niyam se** chalti hai. Pahad par mitti ka weight aur friction, Himachal ho ya Kerala, ek hi niyam follow
karte hain. Isliye:

1. **Jahan labels nahi hain, wahan bhi kaam karti hai.** Hamara Caine landslide threshold bina kisi training ke 184 asli Indian landslides
   par ROC-AUC 0.758 deta hai (OUR RESULT, `results/geo_large`).
2. **Galat cheez pakadti hai.** Agar camera "aag" bole lekin physics kahe "is hawa me aisa plume ho hi nahi sakta", to hum shak karte hain.
3. **Samjhayi ja sakti hai.** "FS 0.83 ho gaya kyunki mitti me 1 m paani ka dabaav aa gaya" kisi bhi officer ko samjha sakte hain.
   "Neural network ka neuron 47 active hua" nahi samjha sakte.

**TRINETRA ka niyam:** physics aur data dono milke decide karte hain. Physics **galti se alarm kam nahi kar sakti**, sirf badha sakti hai
(isko "shield" kehte hain, P03 me).

## 2. Formula ki teen class (har jagah ye chip dikhegi)

| Class | Matlab | Misaal |
|---|---|---|
| **A** | Established: kisi paper me hai, decades se use ho raha hai | Factor of safety, Heskestad flame height |
| **B** | Hamari team ne A se derive kiya, ya hamare data par fit kiya, aur steps likhe hain | ΔFS rain signal, back-analysed cohesion, GLOF fit |
| **C** | Naya idea (hypothesis), test nahi hua, code me **default OFF** | ND-1 flicker, PHARAOH |
| **SURROGATE** | Repo me koi model nahi tha, isliye ek literature formula sirf dikhane ke liye | Fire perimeter (Anderson 1983) |

**Claim ladder:** C0 not addressed → C1 design only → C2 code hai par test nahi → **C3 hamne implement kiya aur khud naapa** → C4 kisi
published result ke barabar ya behtar, same protocol par. **TRINETRA ke paas abhi koi C4 nahi hai**, isliye hum "best", "first", "solves"
jaise shabd use nahi karte.

## 3. Wo basics jo har chapter me lagenge (bilkul zero se)

### 3.1 Force (bal) aur weight
Force matlab dhakka ya kheench. Unit: **newton (N)**. 1 kg cheez ko dharti **9.81 N** se neeche kheenchti hai. Isko `g = 9.81 m/s²` likhte hain.
- Weight = mass × g. 100 kg mitti ka weight = 981 N ≈ 1 kN (kilonewton = 1000 N).

### 3.2 Stress aur pressure: "kitna force, kitne area par"
Ek haathi ka pair aur ek suee: haathi bhaari hai, par suee chubhti hai, kyunki suee ka force bahut chhote area par hai.
- **Stress / pressure = force ÷ area.** Unit **pascal (Pa) = N/m²**. Hum zyada tar **kPa (kilopascal = 1000 Pa)** use karte hain.
- 1 m gehre paani ke neeche pressure = 1000 kg/m³ × 9.81 × 1 m = **9.81 kPa**. Ye number P01 me baar-baar aayega.

### 3.3 Unit weight γ (gamma)
Ek cubic metre mitti ka weight. Mitti ≈ **19 kN/m³**, paani = **9.81 kN/m³** (`γ_w`). Matlab 2 m gehri mitti ki parat har square metre par
19 × 2 = 38 kPa ka weight daalti hai.

### 3.4 Angle, sin, cos, tan (dhalaan ke liye)
Slope β (beta) = zameen kitni jhuki hai. 0° = sapaat, 90° = deewar.
- Kisi weight ko slope par todo: **slope ke saath neeche** wala hissa = weight × sin β, **slope me ghusne** wala hissa = weight × cos β.
- Seedha samjho: jitni zyada dhalaan, utna zyada "neeche phisalne wala" hissa (sin β badhta hai) aur utna kam "zameen me dabne wala" hissa
  (cos β ghatta hai).
- **tan β = sin β / cos β.** tan 30° = 0.577, tan 35° = 0.700, tan 45° = 1.

### 3.5 Friction angle φ (phi)
Ek kitaab ko dheere-dheere jhukaao. Jis angle par wo phisalne lage, wahi **friction angle** hai. Mitti ke liye ≈ 30–35°. Agar slope β > φ aur
mitti me koi "chipak" (cohesion) na ho, to slope gir jaayega. Ye P01 ka sabse pehla niyam hai.

### 3.6 Energy, power, kW
- Energy = kaam karne ki kshamta (joule, J). Power = energy per second (watt, W = J/s).
- Ek LPG burner ≈ 2–3 kW. Ek jalti car ≈ 2,000–8,000 kW. Jangal ki aag ka front: **har metre** par sau se hazaar kW (kW/m).
- P02 me Q = heat release rate (kW) = aag har second kitni garmi chhod rahi hai.

### 3.7 Exponent aur power law
`x²` = x × x. `x^0.4` = "x ki 0.4 power", yaani square root se bhi dheere badhne wala. Power law `y = a·x^b`:
- b = 1: seedha anupaat (dugna x → dugna y).
- b = 0.4: dugna x → sirf 2^0.4 = **1.32 guna** y. (Flame height aise hi badhti hai: aag dugni karo, flame sirf 32% oonchi.)
- b = −0.39: x badhe to y ghate (Caine line: lambi barish ko kam intensity chahiye).

### 3.8 Logarithm (log) aur dB
log batata hai "10 ko kitni baar guna kiya". log₁₀(1000) = 3. Log ka fayda: bahut bade-chhote numbers ek scale par aa jaate hain, aur
**power law log-log graph par seedhi line ban jaata hai** (`log y = log a + b log x`). Isi liye Caine aur GLOF graphs log scale par hain.
- **Decibel (dB) = 10 × log₁₀(ratio).** +3 dB = dugna, +10 dB = 10 guna, +20 dB = 100 guna. Radio (P04) aur siren isi me naape jaate hain.

### 3.9 Probability aur "calibrated"
- Probability p = 0 se 1. p = 0.3 matlab "aise 100 cases me se lagbhag 30 me sach me aag hogi".
- **Calibrated** model wo hai jiska 0.3 sach me 30% ho. Uncalibrated model 0.9 bolta hai par sirf 60% sahi hota hai. P03 me iska fix hai
  (temperature scaling) aur figure `../../../results/figures/R2_calibration.png`.

### 3.10 ROC-AUC (results samajhne ke liye)
Ek fire image aur ek non-fire image random uthao. **AUC = probability ki model fire wali ko zyada score dega.** 0.5 = sikka, 1.0 = perfect.
Ye threshold par depend nahi karta, isliye models compare karne ke liye achha hai. Figure: `../../../results/figures/R1_fire_roc_oof_and_heldout.png`.

### 3.11 "Spatial block cross-validation" (hamare numbers imaandaar kyun hain)
Agar ek hi pahad ki 10 photos me se 8 par train karo aur 2 par test, to model "pahad yaad" kar leta hai, aag nahi. Isliye hum **poore block**
(ek jagah, ek video sequence) ko ya to train me rakhte hain ya test me, dono me kabhi nahi. Isse numbers kam aate hain, par sach ke kareeb.

## 4. Ek line me TRINETRA ki physics

> Pahad: **barish → mitti me paani ka dabaav → friction kam → FS < 1 → slope girta hai.** Aag: **garmi → plume, flame, flicker → camera
> jo dekhe wo physics se match kare?** Decision: **galat alarm aur chhooti aag, dono ki keemat tolo → threshold p\*.** Warning: **radio
> signal pahad ke peeche nahi jaata → relay oonchi jagah chahiye.**

Ab P01 kholo.
<!-- END -->
