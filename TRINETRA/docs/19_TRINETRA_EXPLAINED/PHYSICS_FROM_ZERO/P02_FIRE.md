# P02 — Aag ki physics zero se: camera jo dekhe, kya wo physics se match karta hai?

> **Ek line me:** asli aag ka ek "physics fingerprint" hota hai: uski flame height uski power se tay hoti hai, wo ek khaas frequency par
> phadphadaati hai, uska garam plume hawa se ladta hai, aur wo garmi ki roshni chhodti hai. Camera ka "aag" bolna tab zyada bharosemand hai
> jab ye fingerprint bhi match kare. Ye physics **alarm khud nahi bajaati**; ye sirf fire detector par bharosa kam-zyada karti hai.

Code: `TRINETRA/trinetra/src/trinetra/ws1a_firephys/` (established_ef.py = Class A, novel_nd.py = Class C default OFF, gate.py).
Figures: **`fig/05_fire_physics.png`**, **`fig/06_plume_temperature.png`**.

**Pehle ek honesty note:** fire ke coefficients code me `[coeff-verify]` tagged hain, matlab inhe primary source (SFPE Handbook, Heskestad,
McCaffrey) se confirm karna baaki hai. Isliye inka role sirf "consistency check" hai, alarm trigger nahi.

## Fire physics kyun? (camera kaafi kyun nahi)
Hamara fire CNN out-of-fold sirf ROC-AUC 0.755 deta hai, aur CLIP probe 0.959 (OUR RESULTS, seed 0, 3,410 images, 366 spatial blocks; `results/fire_meta/fire_meta_fusion_s0_compare.md`). Lekin dono **pixels** dekhte hain. Laal-peeli
sunset, gaadi ki headlight, dhund me street light, ya chimney ka steam sab "aag jaisa" dikh sakta hai. Physics poochhti hai: "kya ye
**vyavhaar** bhi aag jaisa hai?" Steam regular phadphadaata nahi, sunset ka koi plume nahi hota, headlight ki garmi nahi hoti.

---

## M6a · Heskestad flame height   [Class A]

### Misaal
Gas stove ka knob ghumaao: jitni zyada gas (power), utni oonchi flame. Lekin power dugni karne par flame dugni nahi hoti, thodi hi badhti hai.
Aur ek chaudi kadhai me wahi gas phaila do, to flame chapti ho jaati hai.

### Derivation (dimensional analysis: "units ko hi guru maano")
1. Flame height L kis par depend karti hai? Power Q (kW), base ka size D (m), aur hawa ke gun: density ρ, specific heat c_p, temperature T,
   gravity g (plume buoyancy se upar uthta hai).
2. In sab ko jodkar ek **dimensionless power** banti hai (koi unit nahi):
   $$Q^* = \frac{Q}{\rho_\infty c_p T_\infty \sqrt{g}\,D^{5/2}}$$
   Iska matlab: "aag kitni taakatwar hai uske size ke hisaab se".
3. Bahut saare experiments ka fit (Heskestad): **L/D = 3.7·Q\*^(2/5) − 1.02**.
4. Q* daalo: Q*^(2/5) = Q^(2/5)·(ρ c_p T √g)^(−2/5)·D^(−1) (kyunki (D^(5/2))^(2/5) = D). Dono taraf D se guna karo:
   $$L = 3.7\,(\rho c_p T\sqrt g)^{-2/5}\,Q^{2/5} - 1.02\,D$$
5. Normal hawa (ρ = 1.2 kg/m³, c_p = 1.0 kJ/kg·K, T = 293 K, √g = 3.13): coefficient = 3.7 × 1101^(−0.4) = **0.225** (code se calculate).
   Heskestad ka published form 0.235 hai (thode alag reference conditions), aur repo wahi use karta hai:
$$L = 0.235\,Q^{2/5} - 1.02\,D$$

### Code se numbers (WORKED EXAMPLE)
| Aag | Q (kW) | D (m) | L (m) |
|---|---|---|---|
| chhota kooda/patte | 100 | 0.5 | 0.97 |
| jhaadi | 500 | 0.5 | **2.31** |
| scenario 1 jaisa forest patch | 8,000 | 6 | 2.44 |
| industrial unit (synthetic) | 40,000 | 12 | 4.05 |
| 2000 kW par chaudi base | 2,000 | 3 | 1.86 (chaudi base flame ko chapta karti hai) |

**Power law ka matlab:** Q dugna → L sirf 2^0.4 = **1.32×**. Isliye camera me flame ka size dekhkar "kitni badi aag" ka ek moota andaza milta
hai, lekin chhoti galti bhi badi power galti ban jaati hai. Hum ise sirf consistency ke liye use karte hain.

### TRINETRA me
Console ke "alert dive" me perimeter ke saath ek patli "flame band" asli metres me (L) extrude hoti hai, aur Evidence panel me L dikhta hai.

---

## M6b · Plume ka temperature: oonchai ke saath kitna thanda?   [Class A]

### Misaal
Agarbatti ka dhuan: paas me garam aur seedha, upar jaate-jaate thanda aur phaila hua. Aag ke upar ki garam hawa (plume) bhi aise hi
"bahar ki hawa ko andar kheenchti" hai aur thandi hoti jaati hai.

### Formula aur uska matlab
$$\Delta T_0 = 9.1\left(\frac{T_\infty}{g\,c_p^2\,\rho_\infty^2}\right)^{1/3} Q_c^{2/3}\,(z-z_0)^{-5/3}$$
- Bracket wala hissa normal hawa par = **25.0** (code se calculate). Isliye simple form: **ΔT ≈ 25·Q_c^(2/3)·z^(−5/3)** (Heskestad ka
  jaana-maana roop).
- Q_c = convective power (garmi jo hawa ke saath upar jaati hai), z = height.
- **−5/3 ka matlab:** height dugni → ΔT 2^(5/3) = **3.2× kam**.

**Derivation ka idea (similarity):** plume ki "buoyancy flux" B = g·Q/(ρ c_p T) hoti hai (har second kitni upar uthne ki taakat). Height z par
upar ki speed w ~ (B/z)^(1/3), aur temperature ka ratio ΔT/T ~ B^(2/3)·z^(−5/3)/g. B daalne par upar wala formula aata hai.

### Code numbers (Q_c = 500 kW)
z = 5 m → **108 K**, z = 10 m → **34 K**, z = 20 m → **10.7 K**.

### Kyun zaroori?
IoT heat sensor kitni oonchai par hai, ye bahut matter karta hai. 20 m upar laga sensor 500 kW ki aag ko sirf ~11 K garam mehsoos karega.
Sensor placement ki planning isi se hoti hai.

---

## M6c · Byram convection number: hawa jeetegi ya aag ka plume?   [Class A]

### Misaal
Ek moombatti ko phoonk maaro: halki phoonk se flame jhukti hai par seedhi upar uthne ki koshish karti hai. Tez phoonk se flame letkar bujh jaati
hai. Badi aag (jangal) me bhi yahi muqabla hota hai: **aag ka garam plume upar uthna chahta hai, hawa use bagal me dhakelti hai.**

### Formula
$$N_c = \frac{2\,g\,Q_c}{\rho\,c_p\,T\,U^3}$$
- **Upar (numerator):** aag ki "upar uthne ki power" per metre front (buoyancy).
- **Neeche (denominator):** hawa ki kinetic power (U³ isliye kyunki hawa ki energy flux speed ki teesri power ke saath badhti hai).
- N_c > 2 → **plume-dominated**: aag apna mausam khud banati hai (seedha plume, pyrocumulus). N_c < 1 → **wind-dominated**: aag hawa ke
  saath letkar daudti hai.

### Code numbers
| Q_c (kW/m) | Hawa U (m/s) | N_c | Regime |
|---|---|---|---|
| 1500 | 2 | 10.5 | plume |
| 1500 | 4 | 1.31 | beech me |
| **1500** | **9** | **0.115** | **wind-dominated** |
| 300 (crop residue) | 3 | 0.62 | wind |
| 6000 (industrial) | 1.5 | 99 | plume |

**U³ ka asar dekho:** hawa 2 se 9 m/s (4.5×) karne par N_c **91× gira**.

### Fire gate me kaise use hota hai, aur hamari ek khoj
Gate: consistency c = clip(N_c / 2, 0.3, 1). Code se: Q_c = 1500, U = 2 → **c = 1.0, u = 0.15**. U = 9 → **c = 0.30, u = 0.43**.

**Khoj (console chala kar mili):** tez hawa me ek **asli** jangal ki aag ka N_c < 1 aata hai, aur gate uski consistency 0.3 kar deta hai, yaani
asli aag ko "shakki" bana deta hai. Lekin wind-driven fires sabse khatarnaak aur sabse aam hote hain (Uttarakhand ke spring fires). N_c < 1
ka matlab "aag nahi" nahi, balki "dusri tarah ki aag" hai. **Physics team ko ye gate rule review karna chahiye** (FRONTEND/FE_STATE.md me
flagged). Console me "Byram N_c for full consistency" aur "Minimum physics consistency" sliders se iska asar dekh sakte ho.

---

## M6d · Strouhal flicker: aag ki "dhadkan"   [Class A]

### Misaal
Aag ek regular rhythm me phadphadaati hai, jaise dil dhadakta hai. Choti aag tez, badi aag dheere. Ye isliye kyunki garam hawa ke bade
"bulbule" (vortex) ek size ke hisaab se bante aur toot te hain.

### Formula
f ≈ St·√(g/D) with Strouhal number St ≈ 0.48 → 0.48 × 3.13 = **1.5**, isliye **f ≈ 1.5 / √D Hz**.

Code numbers: D = 0.3 m → 2.74 Hz, 0.5 m → **2.12 Hz**, 1 m → 1.50 Hz, 2 m → 1.06 Hz, 6 m → 0.61 Hz.

### Kyun useful?
Steam, dhund aur sunset ki koi regular 1–3 Hz ki dhadkan nahi hoti. Isliye flicker ek sasta "ye sach me aag hai?" test hai.

### Camera ki problem: aliasing (ND-1, Class C, default OFF)
Agar camera **2 frames per second** le, to wo 2.12 Hz ki flicker ko sahi nahi dekh sakta (Nyquist niyam: frequency ko sahi dekhne ke liye
kam se kam dugni speed se sample karna padta hai). Wahi signal **0.12 Hz** jaisa dikhega (code: aliased_frequency(2.12, 2) = 0.121).
25 fps camera par wo 2.12 Hz hi rahega. Figure (`fig/05_fire_physics.png`, right panel) me dashed line yahi "jhooth" dikhati hai.
ND-1 ka idea: physics se *expected* aliased frequency nikaalo aur camera ki dikhi frequency se milao. Consistency = exp(−(f_obs − f_alias)²/2σ²),
σ = 0.3 Hz. Example: dikhi 0.15 Hz, expected 0.12 Hz → **0.995**. **Status: novelty not verified, untested, default OFF.**

---

## M6e · Garmi ki roshni aur dhuan: Stefan–Boltzmann aur Beer–Lambert   [Class A]

### Stefan–Boltzmann: garam cheez kitni roshni (IR) chhodti hai
$$L = \varepsilon\,\sigma\,T^4, \quad \sigma = 5.67\times10^{-8}\ \mathrm{W\,m^{-2}K^{-4}}$$
**T⁴ ka matlab:** temperature dugna → radiation **16×**. Code: 300 K (kamra) → 459 W/m², 600 K → 7,349, 1000 K (aag) → **56,704**,
1200 K → 117,581 W/m². Ulta bhi: 56,700 W/m² dekha → T = 1000 K. Isi liye thermal camera me aag itni "chamakti" hai.

### Beer–Lambert: dhuan kitni roshni rokta hai
$$\tau = e^{-(\kappa+\sigma)L}$$
Dhuan jitna ghana (κ+σ) aur jitni lambi doori (L), utni kam roshni guzarti hai. Code: (κ+σ)·L = 0.5 → 61% guzarti hai, 2.5 → 8%, 5 → **0.7%**.
Matlab ghane dhuen ke peeche aag lagbhag chhup jaati hai.

### ND-2 (Class C, default OFF): dhuen ke peeche asli temperature
Camera ko jo roshni milti hai = τ·(aag ki roshni) + (1 − τ)·(dhuen ki apni roshni). Isko aag ke liye solve karo. Lekin jab τ → 0, to chhoti si
galti bhi bahut badi ho jaati hai, isliye code uncertainty bhi deta hai jo τ ghatne par badhti hai ("fail toward uncertain").
Code example: aag 1100 K, dhuan 400 K, τ = 0.5 → **1100 ± 14 K**; τ = 0.05 → **1100 ± 18 K**.

---

## Class C idea ND-3 (default OFF)
Ignition index Π = Σ wᵢ·scaleᵢ·rateᵢ: garmi, gas aur radiation ek saath kitni tezi se badh rahe hain. Sirf ek chhota sa boost (+0.1·tanh Π).
Untested.

---

## Fire gate: sab kuch jodna   `ws1a_firephys/gate.py`
1. p = detector confidence (camera + temporal validator se). Physics **p ko nahi badalti** (ND-3 OFF hai).
2. Consistency c = 1, phir Byram se clip(N_c/2, 0.3, 1) guna. Agar ≥ 2 IoT nodes smoke + heat dono pakdein → c + 0.1.
3. Uncertainty u = 0.15 + 0.4·(1 − c) (+ ND-2 ka hissa, agar ON).
4. Ye (p, c, u) fusion me jaate hain: weight = reliability × c × exp(−u/τ). Kam consistency → kam weight. Details P03 me.
5. **Gate kabhi public alarm nahi bhejta.**

---

## SURROGATE: fire perimeter (repo me koi fire-spread model nahi)
Console me aag ka phailta perimeter dikhaane ke liye humne ek literature formula use kiya, **SURROGATE label ke saath**:
- Head rate of spread R (m/min) scenario ka input hai (synthetic).
- Hawa aag ko ande (ellipse) ki shape deti hai. Length/breadth ratio, Anderson (1983):
  **L/B = 0.936·e^(0.2566·U) + 0.461·e^(−0.1548·U) − 0.397** (U = mi/h).
  Code check: 1 m/s → 1.59, 2 m/s → 2.78, 4 m/s → 9.0. **9 m/s par ye 164 deta hai, jo bekaar hai**, kyunki formula tez hawa ke liye
  nahi bana. Isliye console L/B ko **8 par cap** karta hai (FARSITE jaise tools bhi cap karte hain).
- Peeche ki spread = head × (L/B − √((L/B)² − 1)) / (L/B + √((L/B)² − 1)).
- **Ye prediction nahi hai.** Asli spread model (Rothermel, slope effect, fuel moisture) TRINETRA ka future work hai.

## Ek nazar me (fire)
| Model | Class | Repo me | Real data par test? |
|---|---|---|---|
| Heskestad flame height | A | haan | golden tests only |
| Plume ΔT | A | haan | golden tests only |
| Byram N_c | A | haan, gate me | golden tests; gate behaviour flagged |
| Strouhal flicker | A | haan | golden tests only |
| Stefan–Boltzmann, Beer–Lambert | A | haan | golden tests only |
| ND-1, ND-2, ND-3 | C | haan, OFF | nahi |
| Fire perimeter | SURROGATE | console only | nahi |

**Golden tests ka matlab:** browser wale TypeScript ports aur Python code ke numbers 1e-9 tak match karte hain. Ye **code ki sahi-ness** hai,
**field accuracy nahi**.
<!-- END -->
