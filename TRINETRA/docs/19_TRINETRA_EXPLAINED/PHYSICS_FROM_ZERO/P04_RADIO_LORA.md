# P04 — Jab internet band ho: radio (LoRa) aur siren ki physics

> **Ek line me:** pahaad me baadh ya landslide aksar mobile tower aur bijli pehle giraate hain. TRINETRA ka "last mile" plan LoRa radio
> (865–867 MHz, India me licence-free) aur siren par tika hai. Radio kitni door jaayega, ye **dB ke hisaab-kitaab** (link budget) aur
> **pahaad beech me hai ya nahi** (Fresnel zone) se tay hota hai.

Code: `ws3_alert/last_mile.py` (Python, stdlib), `src/console/lora/model.ts` (console, real DEM terrain).
Figures: **`fig/08_lora_range_airtime.png`**, **`fig/09_fresnel_real_terrain.png`**.

**Status:** saara radio **SIMULATED** hai. Koi hardware nahi chalaya gaya, koi field survey nahi hua. Path-loss exponent ek ASSUMPTION hai.
Console me nodes ki jagah synthetic hai, lekin unke neeche ka terrain asli (Chamoli DEM) hai.

---

## R1 · Decibel (dB): bade gunaa-bhaag ko jodna-ghataana banaana
Radio me power 1 watt se lekar 0.000000000000001 milliwatt tak hoti hai. Itne bade range ke liye log scale use karte hain:
- dBm = 10·log10(P / 1 mW). **30 dBm = 1 W**, 0 dBm = 1 mW, **−132 dBm = 6×10⁻¹⁴ mW** (LoRa SF10 itna kamzor signal bhi sun leta hai).
- **+3 dB ≈ dugna**, +10 dB = 10×, −20 dB = 100× kam.
- Fayda: gunaa ki jagah jodna. Received = Transmit + Antenna gains − Losses. Bas.

## R2 · Link budget: "kitna nuksaan sah sakte hain?"
$$\text{Budget} = P_{tx} + G_{tx} + G_{rx} - L_{cable} - (S_{rx} + M_{fade})$$
Repo defaults (SF10): 30 + 2 + 2 − 1 − (−132 + 15) = **150 dB**. Matlab raaste me 150 dB tak ka nuksaan chal jaayega.
- S_rx = receiver sensitivity (SX1276 datasheet): SF7 −123, SF10 −132, SF12 −137 dBm.
- M_fade = 15 dB "safety cushion" (baarish, patte, insaan, mausam ke utaar-chadhaav ke liye).

## R3 · Path loss: doori ke saath signal kitna kamzor
### Free space (Friis)
Antenna se signal ek phoolte gubbaare (sphere) ki tarah phailta hai. Sphere ka area 4πd², isliye power ~ 1/d². Wavelength ka asar
jodkar dB me:
$$\mathrm{FSPL} = 20\log_{10}d_{km} + 20\log_{10}f_{MHz} + 32.44$$
Code: 866 MHz par 1 m → 31.2 dB, 10 km → 111.2 dB, 20 km → 117.2 dB. **Doori dugni → sirf +6 dB.**

### Pahaad aur jangal (log-distance)
$$PL(d) = PL(1\,m) + 10\,n\,\log_{10}(d / 1\,m)$$
Free space me n = 2. Jangal aur pahaad signal ko zyada khaate hain, isliye n bada hota hai. **Repo ki ASSUMPTION:** ridge LOS 2.2,
hill-forest 3.0, valley NLOS 3.6.

Budget = PL(d) rakhkar d nikaalo: d = 10^((Budget − PL(1 m)) / 10n). Code numbers:
| SF | Airtime (24 B) | Valley NLOS | Hill forest | Ridge LOS |
|---|---|---|---|---|
| 7 | 0.062 s | 1.1 km | 4.6 km | 98 km* |
| 10 | 0.371 s | 2.0 km | **9.1 km** | 251 km* |
| 12 | 1.483 s | 2.8 km | 13.4 km | 424 km* |

\* **Ye numbers kaagaz par hain.** n = 2.2 par formula sirf power dekhta hai, prithvi ki golaai aur beech ke pahaad nahi. Asli limit
R4 aur R5 deti hain. Isliye console har link ko terrain par alag se check karta hai.

**n ka asar:** 3.0 se 3.6 karne par SF10 range 9.1 → 2.0 km (4.5× kam). Isliye **site survey se n fit karna** sabse zaroori next step hai.

## R4 · Spreading factor aur airtime: door jaana ya jaldi bolna
LoRa ek "chirp" bhejta hai (frequency upar sarakti hai). SF ek symbol ki lambai tay karta hai: **T_sym = 2^SF / BW**. SF +1 → har symbol
dugna lamba → receiver ko zyada "sunne ka samay" → ~2.5 dB behtar sensitivity, lekin airtime dugna.
Semtech ka formula (AN1200.13, code me exact): 24 byte ka alert SF7 par 0.06 s, SF12 par 1.48 s. India me duty-cycle aur battery ke liye
airtime zaroori hai, aur kai relay hops me ye jud jaata hai. Trade-off figure 08 me hai.

## R5 · Fresnel zone: seedhi line kaafi nahi
### Misaal
Radio wave ek patli rassi nahi, balki ek **mota ellipse (football jaisa)** hai jo dono antennas ke beech phaila hai. Agar pahaad is football
ka bada hissa kaat de, to signal kamzor hota hai, chahe dono antenna ek dusre ko "dekh" rahe hon.

### Formula
$$r_1 = \sqrt{\frac{\lambda\, d_1 d_2}{d_1 + d_2}}$$
λ = c/f = 3×10⁸ / 866×10⁶ = **0.346 m**. Beech me (d₁ = d₂ = d/2) → r₁ = √(λd/4).
Code: 2 km link → 13.2 m, 10 km → 29.4 m, 20 km → **41.6 m** mota "football". Rule of thumb: **60% (0.6·r₁) khaali hona chahiye.**

### Prithvi ki golaai (earth bulge)
$$h_{bulge} = \frac{d_1 d_2}{2 k R}, \quad k = 4/3,\ R = 6371\ \mathrm{km}$$
k = 4/3 isliye ki hawa radio ko thoda neeche jhukaati hai, jaise prithvi thodi badi ho. Beech me: 10 km → 1.5 m, 20 km → **5.9 m**.

### Console me (model.ts)
Har sambhavit link ko asli DEM par check karo: clearance = (antennas ki line ki height) − (zameen + bulge) − 0.6·r₁. Agar kahin bhi < 0, to
**blocked**. Chamoli me 55 me se **47 candidate links blocked** aaye. Pahaad ki ghaatiyon me yahi asli dikkat hai, aur isi liye ridge
relays chahiye. Figure 09 me ek 12.3 km link ka asli terrain profile hai (synthetic nodes, real DEM).

## R6 · Siren: awaaz kitni door
$$L(r) = L_{ref} - 20\log_{10}(r / r_{ref}) - \alpha\,(r - r_{ref})$$
- Pehla hissa: awaaz bhi sphere me phailti hai → doori dugni, −6 dB.
- Dusra hissa: hawa, ped, pahaad ka extra nuksaan. α = 1 dB / 100 m (hills, ASSUMPTION).
- Default: 120 dB at 30 m. Code: 500 m par 90.9 dB, 1 km par 79.8 dB. 70 dB (alerting contour) tak radius = **1,584 m**.
- Kamiyaan: hawa ki disha, temperature inversion, ghati ki goonj (echo) aur ghar ke andar ka nuksaan (~20–30 dB) shaamil nahi hain.

## Ek nazar me
| Model | Status | Sabse badi assumption |
|---|---|---|
| Airtime (Semtech) | exact formula, test se match | koi nahi (datasheet) |
| FSPL | exact | free space |
| Log-distance range | SIMULATED | n by terrain (ASSUMPTION) |
| Fresnel + bulge, real DEM | SIMULATED | DEM resolution, antenna height |
| Siren radius | SIMULATED | α, no wind / indoor loss |
---

# P04 · DEEP DIVE — har formula shuru se derive (step by step)

Neeche ke saare numbers `ws3_alert/last_mile.py` ke functions chala ke nikale gaye hain (WORKED EXAMPLE, measurement nahi).

## Symbol table
| Symbol | Matlab | Unit | Repo default |
|---|---|---|---|
| P_tx | transmit power | dBm | 30 (1 W, E32-900T30D) |
| G_tx, G_rx | antenna gain | dBi | 2, 2 |
| L_cable | cable / connector loss | dB | 1 |
| S_rx | receiver sensitivity (SX1276, BW 125 kHz) | dBm | SF7 −123 … SF10 −132 … SF12 −137 |
| M_fade | fade margin (safety cushion) | dB | 15 |
| f | frequency | MHz | 866 |
| λ | wavelength = c/f | m | 0.346 |
| n | path-loss exponent | – | ridge 2.2, hill-forest 3.0, valley 3.6 (ASSUMPTION) |
| SF | spreading factor | – | 10 |
| BW | bandwidth | Hz | 125,000 |
| CR | coding rate index (4/5 → 1) | – | 1 |
| d₁, d₂ | doori link ke dono siron se | m | – |
| R, k | prithvi ka radius, refraction factor | km, – | 6371, 4/3 |
| L_ref, r_ref, α | siren level, ref doori, extra attenuation | dB, m, dB/m | 120, 30, 0.01 |

## D1 · Friis free-space loss: inverse-square se 32.44 tak
1. **Isotropic antenna** power P ko har disha me barabar bhejta hai. Doori d par wo power ek sphere ke area 4πd² par phail jaati hai:
   power density S = P / (4πd²)  [W/m²]. Ye "inverse-square law" hai: doori dugni → density ¼.
2. Receive antenna ek "jaali" ki tarah kuch area pakadta hai, jise **effective aperture** kehte hain. Isotropic antenna ke liye
   A_e = λ² / (4π) (antenna theory ka standard result).
3. Received power = S × A_e = P · λ² / (4πd)². Isliye loss (ratio) = (4πd / λ)².
4. dB me: FSPL = 20·log₁₀(4πd/λ). λ = c/f rakho: FSPL = 20log₁₀d + 20log₁₀f + 20log₁₀(4π/c).
5. d km me aur f MHz me ho to constant = 20log₁₀(4π·10³·10⁶ / 3×10⁸) = 20log₁₀(41.9) = **32.44 dB**.
   $$\mathrm{FSPL} = 20\log_{10} d_{km} + 20\log_{10} f_{MHz} + 32.44$$
6. Check (code): 1 m par 31.19 dB, 10 km par 111.19 dB. Doori 10,000× → +80 dB (har 10× par +20 dB). ✔

**Kab galat:** sirf khule aasmaan me (koi pahaad, ped, zameen ka reflection nahi). Pahaad me nuksaan isse bahut zyada hota hai → D2.

## D2 · Log-distance model aur range nikaalna (equation ulti karna)
Free space me power ~ 1/d², yaani exponent 2. Asli terrain me ~ 1/dⁿ, n > 2. dB me:
$$PL(d) = PL(d_0) + 10\,n\,\log_{10}(d/d_0), \quad d_0 = 1\text{ m},\ PL(d_0) = \mathrm{FSPL}(1\text{ m}) = 31.19\text{ dB}$$
**Link chalega jab** received ≥ sensitivity + margin, yaani PL(d) ≤ Budget, jahan
Budget = P_tx + G_tx + G_rx − L_cable − (S_rx + M_fade).

Ulta karo (d nikaalo):
1. 10 n log₁₀(d) = Budget − PL(d₀)
2. log₁₀(d) = (Budget − PL(d₀)) / (10 n)
3. **d = 10^((Budget − PL(d₀)) / (10 n))** metres.

**Worked example (SF10, hill-forest, code se):**
- Budget = 30 + 2 + 2 − 1 − (−132 + 15) = **150 dB**.
- (150 − 31.19) / (10 × 3.0) = 3.960 → d = 10^3.960 = **9,130 m ≈ 9.13 km**. Code: `lora_range_km(10, "hill_forest") = 9.13`. ✔
- Valley NLOS (n = 3.6): (118.81)/36 = 3.300 → **2.0 km**. Ridge (n = 2.2): 10^5.40 = 251 km → **kaagaz par**; planner isko
  `max_hop_km = 30` par cap karta hai, aur console har link ko terrain par alag se check karta hai (D4).

**Sensitivity:** n ki ±0.3 galti range ko ~2× badal deti hai, kyunki n exponent ke denominator me hai. Isliye field me 5–10 points par RSSI
naap ke n fit karna sabse sasta aur sabse zaroori kaam hai.

## D3 · LoRa airtime: Semtech AN1200.13 formula, ek-ek term
1. **Symbol time:** LoRa ka ek symbol 2^SF "chips" ka hota hai, aur BW chips/second chalte hain:
   T_sym = 2^SF / BW = 1024 / 125,000 = **8.192 ms** (SF10).
2. **Preamble:** (n_preamble + 4.25) symbols = (8 + 4.25) × 8.192 = **100.35 ms**. (4.25 = sync word + start-of-frame.)
3. **Payload symbols:**
   $$n_{pay} = 8 + \max\!\left(\left\lceil \frac{8PL - 4SF + 28 + 16\,CRC - 20\,IH}{4(SF - 2DE)} \right\rceil (CR + 4),\ 0\right)$$
   - PL = 24 bytes, CRC = 1, IH = 0 (explicit header), DE = 0 (SF10 par low-data-rate optimisation off).
   - Numerator = 192 − 40 + 28 + 16 − 0 = **196**. Denominator = 4 × 10 = 40. ⌈196/40⌉ = **5**.
   - n_pay = 8 + 5 × (1 + 4) = **33 symbols** → 33 × 8.192 = 270.3 ms.
4. **Total** = 100.35 + 270.34 = **370.7 ms**. Code: `lora_airtime_s(24, 10) = 0.3707 s`. ✔
5. SF +1 → T_sym dugna, isliye airtime ~dugna: SF7 = 0.062 s, SF12 = 1.483 s (code).

**Hop latency (planner):** ek hop = 2 × airtime (bhejna + listen-before-talk backoff) + 0.5 s processing = **1.24 s**. 5 relay hops ≈ 6.2 s,
jo 10 minute deadline ke saamne kuch bhi nahi. Asli bottleneck **radio nahi, coverage** hai: jo gaon kisi node ki range me nahi, uske liye
fallback runner (2.5 km/h, ASSUMPTION) hai: 1 km = 24 minute, yaani deadline miss. Isliye relays ki jagah sabse important decision hai.

## D4 · Fresnel zone ka radius: "aadhi wavelength ka extra raasta"
1. Transmitter T aur receiver R ke beech seedhi doori d = d₁ + d₂. Ek point P lo jo seedhi line se r upar hai, T se d₁ aur R se d₂ door.
2. T→P→R raasta = √(d₁² + r²) + √(d₂² + r²). Jab r ≪ d₁, d₂: √(d² + r²) ≈ d + r²/(2d) (binomial approximation).
3. Extra raasta Δ = r²/2 · (1/d₁ + 1/d₂) = r²(d₁ + d₂) / (2 d₁ d₂).
4. **Pehla Fresnel zone** wo saare points hain jahan Δ ≤ λ/2 (wahan se aayi wave seedhi wave se "jodti" hai, ghataati nahi).
   Δ = λ/2 rakho: r² (d₁+d₂) / (2d₁d₂) = λ/2 →
   $$r_1 = \sqrt{\frac{\lambda\, d_1 d_2}{d_1 + d_2}}$$
5. Worked (10 km, beech me d₁ = d₂ = 5,000 m): r₁ = √(0.346 × 5000 × 5000 / 10000) = √865 = **29.4 m**. 60% rule → **17.6 m** khaali
   jagah chahiye. 2 km par 13.2 m, 20 km par 41.6 m.

**Kyun 60%?** Experiments me agar 0.6 r₁ khaali ho to loss lagbhag free-space jitna hi rehta hai; usse kam ho to diffraction loss tezi se
badhta hai (knife-edge diffraction). Ye ek engineering rule of thumb hai, exact cutoff nahi.

## D5 · Earth bulge: gol prithvi beech me "ubhar" kyun aati hai
1. Radius R ka circle. Do points ke beech chord ki lambai d. Beech wale point par chord se circle tak ki oonchai (sagitta)
   h ≈ d²/(8R). Kisi bhi point par (d₁, d₂) ke liye: **h = d₁ d₂ / (2R)** (same geometry, small-angle approximation).
2. Hawa ki density oonchai ke saath ghatti hai, isliye radio thoda neeche mudta hai, jaise prithvi **k = 4/3** guna badi ho:
   $$h_{bulge} = \frac{d_1 d_2}{2 k R}$$
3. Worked (20 km, beech me): 10,000 × 10,000 / (2 × 4/3 × 6.371×10⁶) = **5.9 m**. 10 km par 1.5 m.
4. Console ka check: clearance(x) = LOS_height(x) − [zameen(x) + bulge(x)] − 0.6·r₁(x). Kisi bhi x par < 0 → link **blocked**.

## D6 · Siren: radius nikaalna
1. Awaaz bhi sphere me phailti hai → intensity ~ 1/r² → dB me −20log₁₀(r/r_ref) (doori dugni → −6 dB).
2. Hawa, ped aur pahaad extra kha jaate hain, jo doori ke saath linearly badhta hai: −α(r − r_ref).
   $$L(r) = L_{ref} - 20\log_{10}(r/r_{ref}) - \alpha (r - r_{ref})$$
3. Radius: L(r) = 70 dB solve karo. Ye equation seedha algebra se hal nahi hota (log + linear), isliye code **bisection** karta hai:
   range ko aadha-aadha karke jahan L = 70 ho wahan pahunchta hai.
4. Worked: 500 m → 90.9 dB, 1 km → 79.8 dB, **70 dB par r = 1,584 m**. α = 0 hota (khula maidaan) to sirf inverse-square se
   r = 30 × 10^(50/20) = 9.5 km aata. Matlab α wali assumption radius ko 6× chhota karti hai → field me naapna zaroori.

## Kamiyaan (honest)
- n, α, fade margin: **ASSUMPTION**, field survey nahi hua. Range ±2× tak galat ho sakti hai.
- Fresnel check DEM resolution par tika hai (tile z12 ≈ 35 m pixel is latitude par); chhote ridge chhoot sakte hain.
- Multipath, interference, duty-cycle queueing aur battery drain model nahi kiye.
- Siren model me hawa ki disha, temperature inversion, ghati ki goonj aur ghar ke andar ka loss (~20–30 dB) nahi hai.

## Khud check karo (self-test)
1. Tx power 30 se 27 dBm kar do. SF10 hill-forest range kitni hogi? *(Budget 147 → d = 10^((147−31.19)/30) = 7.2 km.)*
2. SF12 par 24 byte alert ka airtime SF10 se kitne guna hai? *(1.483 / 0.371 ≈ 4×.)*
3. 20 km link ke beech me 60% Fresnel + bulge kitna chahiye? *(0.6 × 41.6 + 5.9 ≈ 30.9 m.)*
4. α = 0.02 dB/m karo to siren radius badhega ya ghatega? *(Ghatega.)*
<!-- END -->
