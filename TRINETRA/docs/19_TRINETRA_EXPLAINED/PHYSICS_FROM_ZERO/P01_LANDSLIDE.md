# P01 — Pahad kyun girta hai? Landslide physics zero se

> **Ek line me:** barish ka paani mitti ke andar jaata hai → mitti ke daanon ke beech paani ka dabaav (pore pressure) banta hai → daane
> ek doosre ko kam dabaate hain → friction kam hota hai → jab "rokne wali taakat" "girane wali taakat" se kam ho jaaye (FS < 1), slope
> phisal jaata hai.

Is chapter me 5 models hain, aur sab ek chain me jude hain:

```
Barish (mm/h, kitni der)
   ├──> [M3 Caine]  barish ki intensity-duration line ke upar hai?            -> p_caine
   └──> [M2 Iverson] paani mitti me kitna neeche gaya? pressure head ψ (m)
              └──> [M1 Factor of Safety] FS = rokne wali / girane wali taakat -> p_FS
Creep sensor (optional) ──> [M4 Fukuzono] kab girega? t_f                      -> p_fk
                 [M5 Geo gate] teeno ko noisy-OR se jodo -> p_phys, consistency c, uncertainty u -> fusion
                 [Shield]  FS < 1 ya tilt tez ho to alarm level kam se kam ORANGE / RED
```
Code: `TRINETRA/trinetra/src/trinetra/ws1b_geophys/` (fs.py, iverson.py, caine.py, fukuzono.py, gate.py).

---

## M1 · Factor of Safety (FS) — "rokne wali taakat ÷ girane wali taakat"   [Class A]

### Misaal
Ek lakdi ka board thoda jhukaao aur us par ek eent rakho. Board jitna jhukega, eent utna phisalne ki koshish karegi. Eent ko do cheezein rokti
hain:
1. **Friction (ghisaav):** eent jitna zor se board ko dabaati hai, utna zyada friction.
2. **Glue (chipak):** agar eent aur board ke beech thoda gond laga ho, to wo bhi rokta hai. Mitti me isko **cohesion c′** kehte hain
   (clay ka chipakna, jadein, thoda cementing).

Ab board ke neeche se paani ka fuhaara maaro jo eent ko thoda **upar uthaaye**. Eent board ko kam dabaayegi → friction kam → eent phisal jaayegi,
bina board ko aur jhukaaye. **Barish mitti ke saath bilkul yahi karti hai.** Paani daanon ke beech ghus ke unhe alag dhakelta hai.

### Kyun yahi model? (alternatives ke saath)
| Option | Kya karta hai | Hamne kyun nahi liya / kyun liya |
|---|---|---|
| **Infinite slope (chuna)** | maanta hai slip surface zameen ke parallel hai aur slope lamba hai | Himalaya aur Western Ghats ke zyaadatar barish waale landslides **shallow** hote hain (1–3 m gehre, sau metre lambe). Is case me ye exact-enough hai, sirf 5 inputs chahiye, aur har DEM cell par chal jaata hai. SHALSTAB aur TRIGRS jaise regional tools bhi yahi use karte hain. |
| Bishop / Janbu (circular slip) | gol slip surface, slices me todta hai | gehre rotational slides ke liye. Har slope ki cross-section geometry chahiye, jo hamare paas nahi. |
| Finite element (FEM) | poori stress field nikalta hai | bahut accurate par har site par soil layers, stiffness aur mesh chahiye. Regional early warning ke liye impossible. |
| Sirf ML (barish → landslide) | data se seekho | labels bahut kam hain (184 events). Physics bina labels ke chalti hai. |

### Derivation, ek-ek step (numbers ke saath: β = 35°, z = 2 m, γ = 19 kN/m³, φ′ = 32°, c′ = 5 kPa)

```
         zameen ki satah
     ____________________________
    /   mitti ki parat, gehraai z  /      β = slope angle
   /____________________________/  <-- slip surface (zameen ke parallel)
  W = γ·z (har square metre plan area par)
     ├── slope ke saath neeche:  W·sinβ  ──> GIRAANE wala
     └── slope me ghusta hua:    W·cosβ  ──> DABAANE wala (friction deta hai)
```

**Step 1 — weight.** Mitti ki ek column, 1 m² plan area, gehraai z. Weight = γ·z = 19 × 2 = **38 kPa**.

**Step 2 — slope par area.** Slip surface jhuki hui hai, isliye 1 m² plan area ke neeche slip surface ka area 1/cos β = 1.221 m² hai. Isliye
"per unit slip area" weight = γ·z·cos β = 38 × 0.819 = 31.1 kPa.

**Step 3 — do hisse me todo.** Upar wala weight slip surface par do kaam karta hai:
- **Normal stress** (dabaav, perpendicular): σ = γ·z·cos²β = 38 × 0.671 = **25.5 kPa**
- **Shear stress** (phisalne wala, parallel): τ = γ·z·sin β·cos β = 38 × 0.574 × 0.819 = **17.85 kPa**

**Step 4 — paani ka dabaav (Terzaghi effective stress).** Daanon ke beech paani pressure u_w deta hai jo daanon ko alag dhakelta hai. Asli
"daane se daane" ka dabaav: **σ′ = σ − u_w**. (Thodi geeli lekin unsaturated mitti me ek ulta "suction" σ_s bhi hota hai jo daanon ko
chipkaata hai; saturation par ye 0. Code me ye term hai, default 0.)

**Step 5 — mitti ki taakat (Mohr–Coulomb, 1773/1900).** Mitti jitna shear sahan kar sakti hai: **τ_f = c′ + σ′·tan φ′**. Matlab glue +
friction. Friction dabaav ke anupaat me hota hai (zyada dabaav = zyada grip), tan φ′ uska coefficient hai.

**Step 6 — FS.**

$$FS = \frac{c' + (\gamma z \cos^2\beta - u_w + \sigma_s)\tan\phi'}{\gamma z \sin\beta\cos\beta}$$

Dry case: FS = (5 + 25.5 × 0.625) / 17.85 = (5 + 15.93) / 17.85 = **1.17**.

**Check ki formula sahi hai:**
- Units: upar kPa, neeche kPa → FS ka koi unit nahi. ✓
- Agar c′ = 0 aur u_w = 0: FS = (cos²β·tanφ′)/(sinβ·cosβ) = **tan φ′ / tan β**. Matlab dry ret ka dher tab tak khada rehta hai jab tak slope
  friction angle se kam hai. Ye har bachcha ret ke dher me dekh chuka hai. ✓
- u_w badhe → FS ghate. ✓ (Code ke golden tests yahi check karte hain.)

### Code se nikle numbers (`fs.py factor_of_safety`, WORKED EXAMPLE)
| Case | FS | Matlab |
|---|---|---|
| β = 35°, c′ = 5, dry | **1.17** | 17% margin |
| same, paani ka head ψ = 0.5 m (u_w = 4.91 kPa) | **1.00** | bilkul kinaare par |
| same, ψ = 1.0 m (u_w = 9.81 kPa) | **0.83** | girega |
| β = 35°, **c′ = 0** (sirf ret), dry | **0.89** | bina cohesion ke 35° ret khadi nahi reh sakti (tan32/tan35 = 0.89) |
| β = 30°, c′ = 0, dry | **1.08** | 30° < 32°, isliye khadi |
| β = 40°, c′ = 5, dry | 1.01 | |
| β = 44°, c′ = 5, dry | **0.91** | sukhe mausam me bhi FS < 1 → ye physically galat hai (neeche dekho) |

Figure: **`fig/01_fs_vs_pore_pressure.png`**. Teen slopes par ψ badhne ke saath FS seedhi line me girta hai.

### Parameter badlo to kya hoga (what-if)
| Parameter | Badhao to | Kyun |
|---|---|---|
| c′ (cohesion) | FS badhta hai | zyada glue |
| φ′ (friction angle) | FS badhta hai | zyada grip per dabaav |
| β (slope) | FS ghatta hai | zyada girane wala hissa, kam dabaav |
| z (depth) | FS thoda ghatta hai (agar c′ > 0) | cohesion ka asar gehraai ke saath "patla" ho jaata hai |
| u_w (pore pressure) | FS ghatta hai | daane alag hote hain |

### Hamari ek badi khoj: "sukha Himalaya FS < 1" (bug B-23) aur uska ilaaj
Hamare 184 asli event locations par DEM se slope ka p90 ≈ **40–44°** aaya. c′ = 5 kPa (ek aam textbook value) daalne par FS < 1 aata hai
**bina barish ke bhi**. Lekin wo slopes to aaj bhi khade hain! Matlab soil parameters galat hain, physics nahi. Agar ise theek na karte to
shield (FS < 1 → ORANGE) poore saal alarm bajata.

**Ilaaj 1 — Back-analysis (Class B, geotechnical engineering ki standard practice).** Logic: "slope khada hai, to sukhe mausam me uska FS
kam se kam thoda sa 1 se upar hoga". Hum maante hain FS_dry = 1.2 aur formula ulta karke c′ nikaalte hain:

$$c'_{bc} = 1.2\,\gamma z \sin\beta\cos\beta - \gamma z\cos^2\beta\tan\phi' \quad (\ge 0)$$

Code se: β = 35° → **5.49 kPa**, β = 40° → **8.52 kPa**, β = 44° → **10.50 kPa**. Jitni steep slope, utni zyada cohesion honi chahiye
(jadein, cementing) tabhi wo khadi hai. Ye intuitive bhi hai.

**Ilaaj 2 — ΔFS: aisa signal jisme unknown c′ hi gayab ho jaaye (Class B, hamari derivation).**
FS_dry − FS_wet nikaalo. Dono me c′ same hai, isliye ghatane par **cancel** ho jaata hai:

$$\Delta FS = FS_{dry} - FS_{wet} = \frac{\gamma_w\,\psi\,\tan\phi'}{\gamma z\sin\beta\cos\beta}$$

- Iska matlab: "barish ne FS ko kitna giraya", aur iske liye c′ jaanna zaroori hi nahi.
- Check: ψ → 0 to ΔFS → 0 ✓. ψ dugna to ΔFS dugna (linear) ✓.
- Code numbers (ψ = 0.5 m): β = 35° → **0.172**, 40° → 0.164, 44° → 0.161.
- **OUR RESULT:** ΔFS akela, bina kisi training ke, 736 real rows par **ROC-AUC 0.750** (`results/geo_large/geo_physics_s0_report.json`).

### Significance (TRINETRA me ye kya karta hai)
- `geo_gate` me `p_FS = sigmoid(4·(1 − FS))` banta hai (M5).
- Shield: FS < 1 → level kam se kam ORANGE (Warning).
- ΔFS physics feature hai landslide fusion aur RL environment ka.

### Kab fail hota hai
- Gehre rotational slides, rockfall, debris flow ke runout par ye lagu nahi.
- Soil parameters (c′, φ′, γ, z) hamne **assume** kiye hain. Field test (direct shear, borehole) ke bina absolute FS par bharosa mat karo.
  Isliye hum ΔFS aur back-analysis par zyada nirbhar hain.

---

## M2 · Iverson (2000): barish ka paani mitti me kitna neeche gaya?   [Class A]

### Misaal
Garam chai me steel ka chammach daalo. Garmi turant upar tak nahi pahunchti; dheere-dheere phailti hai. Paas wala hissa jaldi garam, door wala
der se. Mitti me barish ka **pressure** bhi aise hi "diffuse" hota hai: satah par turant, 2 m neeche ghanton baad. Aur barish rukne ke baad bhi
neeche ka dabaav thodi der badhta rehta hai, jaise chammach ka upar wala sira chai se nikaalne ke baad bhi thodi der garam hota hai.

**Isliye "pichhle 24 ghante ki barish" kaafi nahi hai.** Landslide aksar barish ke **baad** aata hai, jab dabaav slip depth tak pahunchta hai.

### Kyun yahi model?
| Option | Hamne kyun nahi / kyun liya |
|---|---|
| **Iverson linear diffusion (chuna)** | sirf 3 soil numbers (K_z, D0, depth). Analytical formula hai, to har cell par sasta. Barish ka "delay" aur "recovery" dono deta hai. TRIGRS (USGS) isi par bana hai. |
| Full Richards equation (HYDRUS) | sabse accurate, par har jagah mitti ka water-retention curve chahiye. Hamare paas nahi. |
| Simple "antecedent rain index" | sasta, par koi physics nahi: gehraai aur mitti ka asar nahi aata. |

### Derivation, step by step
**Step 1 — Darcy ka niyam (1856), paani mitti me kaise behta hai.** Paani ka flow ("flux" q, m/s) pressure ke dhalaan ke anupaat me hota hai:
q = −K·(dψ/dz). K = hydraulic conductivity, matlab mitti kitni "paani-paas" hai (ret me zyada, clay me kam). Hum K_z = 1e-5 m/s = 0.864 m/day lete
hain (ASSUMPTION, silty sand jaisa).

**Step 2 — paani ka hisaab (conservation).** Kisi patli parat me paani ka badhna = andar aaya − bahar gaya. Darcy ke saath milane par **Richards
equation** banti hai. Iverson ne dikhaya ki jab mitti pehle se kaafi geeli ho (monsoon) aur time chhota ho, to ye ek simple **diffusion
equation** ban jaati hai, bilkul garmi ke phailne jaisi:

$$\frac{\partial \psi}{\partial t} = D_1\,\frac{\partial^2 \psi}{\partial Z^2}, \qquad D_1 = \frac{D_0}{\cos^2\beta}$$

- ψ = pressure head (metre me): "is gehraai par paani ka dabaav kitne metre paani ke column ke barabar hai".
- D0 = hydraulic diffusivity: dabaav kitni jaldi phailta hai. Hum 4.32 m²/day lete hain (5e-5 m²/s, ASSUMPTION).
- **Slope sirf D1 ke andar aata hai.** Code me ek "bug guard" hai jo ensure karta hai ki koi extra cos β factor na lage. Ye ek common galti hai.

**Step 3 — boundary.** Satah par barish ka flux I_z aata hai. Agar barish mitti ki kshamta K_z se zyada ho, to baaki paani bah jaata hai
(runoff), isliye I_z ≤ K_z (code isko cap karta hai). Darcy se satah par dhalaan −∂ψ/∂Z = I_z/K_z.

**Step 4 — solution.** Is diffusion equation ka, is boundary ke saath, ek jaana-maana analytical solution hai:

$$\psi(Z,t) = \frac{I_z}{K_z}\,\sqrt{4D_1t}\;\mathrm{ierfc}\!\left(\frac{Z}{\sqrt{4D_1t}}\right)$$

- **ierfc kya hai?** "integrated complementary error function". Bas itna samjho: ye ek **smooth "ghatta hua" curve** hai. ierfc(0) = 0.564,
  ierfc(0.5) = 0.200, ierfc(1) = 0.050 (code se). Matlab jitni gehraai (Z) zyada, utna kam asar.
- **√(4D1t) = "penetration depth"**: t time me dabaav lagbhag kitna neeche pahuncha. t badhe → zyada neeche.
- **Check:** ierfc ka derivative = −erfc, aur erfc(0) = 1, isliye satah par dhalaan exactly I_z/K_z aati hai. Boundary condition satisfy. ✓
  t → 0 to ψ → 0 ✓. Bahut gehraai par ψ → 0 ✓. Units: metre × (dimensionless) = metre ✓.

**Step 5 — barish badalti rahe to (superposition, LEGO blocks jaisa).** Equation linear hai, isliye har barish ke badlaav ka asar alag-alag jodo:

$$\psi = \sum_k \frac{I_k - I_{k-1}}{K_z}\,R(Z, t-t_k)$$

Ek din barish, phir band: do blocks: "t=0 par +I", "t=1 din par −I". Ye code ka `transient_head_multipulse` hai.

**Step 6 — FS tak pahunchana.** u_w = γ_w·ψ = 9.81·ψ kPa, aur ye seedha M1 ke formula me jaata hai. Ek physical cap bhi hai: ψ hydrostatic
saturation (z·cos²β) se zyada nahi ho sakta.

### Code se nikle numbers (WORKED EXAMPLE: Z = 2 m, β = 35°, barish 5 mm/h = 0.12 m/day, D0 = 4.32 m²/day, K_z = 0.864 m/day)
| Barish shuru hue | ψ at 2 m | u_w | FS (c′ = 5) kya hoga |
|---|---|---|---|
| 6 ghante | 0.033 m | 0.33 kPa | ≈ 1.16 |
| 12 ghante | 0.087 m | 0.85 kPa | ≈ 1.14 |
| 1 din | 0.180 m | 1.77 kPa | ≈ 1.11 |
| 2 din | 0.328 m | 3.22 kPa | ≈ 1.06 |
| 4 din | **0.548 m** | 5.38 kPa | **≈ 0.98 → girega** |

Matlab **5 mm/h ki halki barish, 4 din lagaataar**, 35° slope ko gira sakti hai. Ek tez burst nahi, balki lambi jhadi. Monsoon me yahi hota hai.

Pulse example (1 din barish, phir band): 1 din par ψ = 0.180 m, 2 din par 0.148 m (dheere-dheere wapas). Figure: **`fig/02_iverson_pressure_head.png`**.

### Kab fail hota hai
- Soil numbers assumed hain (sabse badi kamzori).
- NASA POWER ki daily, 0.5° (≈ 50 km) barish cloudburst ko "phaila" deti hai, isliye intensity kam dikhti hai. Fix: IMERG 0.1° (free login chahiye).
- Mitti sookhi ho (dry season), to linear approximation kamzor.

---

## M3 · Caine (1980): barish ki "khatre ki line"   [Class A, empirical]

### Misaal
Doodh ubaalna: **tez aanch thodi der** ya **dheemi aanch bahut der**, dono se doodh ubal jaata hai. Caine ne duniya bhar ke landslides dekhe aur
paaya ki "kitni tez barish (I)" aur "kitni der (D)" ka ek boundary line hai. Line ke upar = landslide hua, neeche = nahi hua.

### Formula
$$I_{thr} = a\,D^{-b}, \qquad \text{ratio} = \frac{I}{I_{thr}}$$
- I = us geeli spell ki average intensity (mm/h), D = kitne ghante (code me lagaataar ≥ 1 mm waale din × 24).
- a = 14, b = 0.39 (repo constants; Caine ki global line).
- Log lene par: log I = log a − b·log D. Log-log graph par **seedhi line**. Figure: **`fig/03_caine_threshold.png`**.

### Code se threshold (WORKED EXAMPLE)
| D (barish kitni der) | I_thr (itni tez chahiye) |
|---|---|
| 1 ghanta | 14.0 mm/h |
| 6 ghante | 6.96 mm/h |
| 1 din | 4.05 mm/h |
| 3 din | 2.64 mm/h |
| 9 din | 1.72 mm/h |

- 120 mm ek din me → I = 5 mm/h → ratio **1.23** (line ke upar).
- 300 mm 3 din me → ratio **1.58**.

### Kyun yahi?
- Sirf barish chahiye, jo har jagah milti hai. Zero training.
- Isliye ye **baseline** hai: koi bhi fancy model agar Caine ko nahi harata, to bekaar hai.
- **Zaroori warning:** a aur b global hain. India ke liye inhe locally re-fit karna chahiye (repo docstring bhi yahi kehti hai).

### OUR RESULT
Zero-fit Caine ratio: **ROC-AUC 0.758** on 736 rows (184 real landslides, NASA Global Landslide Catalog India + NASA POWER rain, spatial
block CV). Rain-only logistic (jo data par train hota hai): 0.781. Physics bina training ke data model ke itne paas hai, aur yahi uski
value hai.

---

## M4 · Fukuzono / Voight: "pahad kab girega?" — failure time forecast   [Class A/B]

### Misaal
Barf ki jami hui jheel par chalte ho, to toot ne se pehle chatakne ki awaazein **tez aur tez** hoti jaati hain. Pahad ka creep (dheere
khisakna) bhi failure se pehle tez hota jaata hai. Agar speed v ko ulta karo (1/v), to wo **seedhi line me zero ki taraf** girti hai, aur jahan
zero ko chhuegi wahi failure time hai.

### Derivation
1. Voight ka niyam: acceleration speed ki power ke anupaat me: dv/dt = A·v^α.
2. Variables alag karke integrate: ∫v^(−α)dv = ∫A dt → v^(1−α)/(1−α) = A·t + constant.
3. Failure par v → ∞, matlab v^(1−α) → 0 (α > 1). Constant ko failure time t_f se likho: v^(1−α) = A(α−1)(t_f − t).
4. α = 2 (zyaadatar cases): **1/v = A·(t_f − t)** → seedhi line. Fit karo 1/v = m·t + b → **t_f = −b/m**.
5. Hamara upgrade: (a) naye points ko zyada weight (recency-weighted least squares), kyunki failure ke paas wale points zyada batate hain;
   (b) **uncertainty interval** (delta method): sirf "20 ghante" nahi, "18.9 se 21.2 ghante". Officer ke liye ye zaroori hai.

### Code numbers (WORKED EXAMPLE, synthetic creep)
- Bina noise: 1/v = 10 − 0.5t → **t_f = 20.0 h** (exact).
- 5% noise ke saath: **t_f = 20.07 h, 95% interval 18.95–21.18 h**. Figure: **`fig/04_fukuzono_inverse_velocity.png`**.

### Status
Repo me koi asli creep (InSAR / extensometer) data nahi hai, isliye **real data par test nahi hua** (C2). Code aur interval ready hain.

---

## M5 · Geo gate: teeno physics signals ko ek probability me jodna   [Class B, design]

**Step 1 — FS ko probability me badlo (sigmoid).** p_FS = 1 / (1 + e^(−k(1 − FS))), k = 4. FS = 1 → 0.5. FS = 0.8 → 0.69. FS = 1.2 → 0.31.
Ek smooth "S" curve, jisme FS 1 ke paas sabse tez badlaav.

**Step 2 — Caine.** p_caine = clip(ratio − 0.5, 0, 1). Ratio 1.23 → 0.73.

**Step 3 — Fukuzono.** p_fk = clip(1 − lead/48 h, 0, 1) × R² (fit kitni achhi hai).

**Step 4 — Noisy-OR (kyun "OR"?).** Agar teen alag-alag gawah hain, aur har ek ke "galat hone" ki sambhavna (1 − p_i) hai, aur ye independent
hain, to "teeno galat" ki sambhavna = (1 − p₁)(1 − p₂)(1 − p₃). Isliye "kam se kam ek sahi" =

$$p_{phys} = 1 - \prod_i (1 - p_i)$$

Fayda: **naya saboot kabhi risk kam nahi karta** (monotone). Early warning me ye zaroori hai. Figure: **`fig/10_noisy_or.png`**.

**Step 5 — consistency aur uncertainty.** Agar signals aapas me match karte hain (std chhota), to consistency c = 1 − std zyada. Uncertainty
u = 0.5(1 − c) + 0.1. Ye fusion ko batata hai ki physics par kitna bharosa karna hai.

**Code example (WORKED EXAMPLE):** β = 35°, c′ = 5, ψ = 0.5 m, 120 mm/24 h → FS = 1.001, Caine ratio 1.233 → **p_phys = 0.867**, c = 0.883, u = 0.159.

**OUR RESULT:** repo geo gate (back-analysed c′): ROC-AUC 0.712. Ye Caine akele (0.758) se kam hai, kyunki sigmoid aur noisy-OR ke hand-set
numbers tune nahi hue. Ye honest result hai.

---

## Safety shield (landslide part)   `ws5_fusion_rl/shield.py`
Hard-coded niyam jo alert level **sirf badha** sakte hain:
- FS < 1 → kam se kam **ORANGE (Warning)**.
- Tilt rate > 5°/day **aur ≥ 2 nodes agree** → **RED (Emergency)**. Ek akela kharab sensor RED nahi bajwa sakta.
- 24 h barish > 150 mm high-susceptibility slope par → ORANGE.
- GLOF: jheel ka level gira **aur** neeche river stage jump → RED.
Kyun? Learned model galti kar sakta hai; ye niyam physics se aate hain aur "kam warning" ki galti ko rokte hain.

---

## Saare landslide results ek jagah (OUR RESULTS, `fig` → `../../../results/figures/R4_landslide_auc.png`)
| Model | Training chahiye? | ROC-AUC | Source |
|---|---|---|---|
| Caine ratio | nahi | **0.758** | results/geo_large |
| ΔFS (Iverson + FS) | nahi | **0.750** | results/geo_large |
| Geo gate (repo) | nahi | 0.712 | results/geo_large |
| Rain logistic | haan | 0.781 | results/geo_large |
| Physics + rain stack | haan | 0.780 | results/geo_fusion |
| FM-1 meta-fusion | haan (calibration) | 0.779 | results/geo_fusion (3 seeds) |
| Geo-PINN (P05) | haan | 0.716 | results/geo_pinn |

**Seedha matlab:** bina kisi training ke physics 0.75–0.76 deti hai. Training waale models sirf 0.02–0.03 aage hain, aur unhe labels chahiye.
Jahan labels nahi hain (zyaadatar Indian districts), wahan physics hi sahara hai.

## Common mistakes
1. Slope ko D1 ke alawa kahin aur bhi laga dena (Iverson me).
2. Caine ke global a, b ko local sach maan lena.
3. Assumed soil ke saath absolute FS par bharosa (isliye ΔFS).
4. "Pichhle 24 ghante" ko hi barish maan lena; lambi jhadi (4 din × 5 mm/h) bhi slope gira sakti hai.
<!-- END -->
