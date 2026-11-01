# P05 — Glacier jheel ka phatna (GLOF) aur physics-informed neural network (Geo-PINN)

> **Ek line me:** GLOF ke liye humne do purane, data se nikle "andaaze ke niyam" khud **asli database par dobara fit** kiye. Ek jheel ke
> area se paani ki matra nikaalta hai, dusra paani ki matra se peak flood. Geo-PINN ek neural network hai jise P01 ka Iverson equation
> "sikhaaya" gaya. Dono honest results hain: GLOF fits kamzor-se-theek hain aur PINN admit nahi hua.

Code: `ws1b_*` GLOF report; `trinetra/deep/geo_pinn.py`, `deep/losses.py`.
Results: `results/glof/glof_physics_report.json`, `results/geo_pinn/geo_pinn_s0_report.json`.

---

## G1 · Power law: "ek cheez badhe to dusri kitni badhe?"
Bahut si prakritik cheezein **y = a·x^b** jaisi chalti hain. Dono taraf log lo: **log y = log a + b·log x**, yaani log-log graph par ek seedhi
line. b = slope, aur yahi asli kahaani hai: x dugna → y 2^b guna.

Fitting: (log x, log y) par seedhi line (least squares). **R²** batata hai ki line data ka kitna hissa samjhaati hai (1 = sab, 0 = kuch nahi).
**Bootstrap CI:** data ke rows ko baar-baar random tareeke se dobara chun kar fit karo. b ka 95% range = "itna pakka hain".

## G2 · Jheel ka area → paani ki matra   [Class B, OUR FIT]
$$V = 1.396\cdot A^{1.132}$$  (A m² me, V m³ me; units report ke x_range se inferred: 14,703 se 4.33 million m²)
- **n = 21**, log-R² = **0.719**, b ka 95% CI = **[0.711, 1.496]**, log10 RMSE = 0.487.
- Worked example: A = 1 km² (10⁶ m²) → V ≈ **8.6 million m³**. A = 0.1 km² → ≈ 0.64 million m³.
- **b > 1 ka matlab:** badi jheelein sirf chaudi nahi, gehri bhi hoti hain. Area dugna → paani 2.19×.
- **Lekin:** log RMSE 0.487 matlab typical galti **~3× upar ya neeche** hai. Aur CI itna chauda hai ki b = 1 (sirf chaudi, gehri nahi)
  bhi possible hai.

## G3 · Paani ki matra → peak flood   [Class B, OUR FIT]
$$Q_p = 0.291\cdot V^{0.535}$$  (V m³, Q_p m³/s)
- **n = 31**, log-R² = **0.363**, CI = **[0.360, 0.789]**, log10 RMSE = 0.824 (typical galti **~6.7×**).
- Example: V = 10 million m³ → Q_p ≈ **1,620 m³/s**. V = 1 million m³ → ≈ 470 m³/s.
- **b < 1 ka matlab:** paani 10× → peak sirf ~3.4×, kyunki badi jheel ka paani zyada samay me nikalta hai.
- **Kamzori:** R² 0.36 matlab volume akela peak ka sirf ek-tihaai samjhaata hai. Dam ka type (moraine, ice, landslide), breach ki speed
  aur ghaati ki shape bahut matter karte hain.

## G4 · Jo test nahi ho sake (aur kyun ye imaandaari hai)
- **Froehlich:** Q_p = c·V^p·h_b^q. Breach height h_b chahiye, jo database me nahi hai.
- **Costa–Schuster:** Q_p = 0.763·PE^0.42, jahan PE = dam ki potential energy (ρ g V h). Dam height nahi hai.
Inhe likhna aasaan tha, lekin bina data ke "verified" kehna galat hota. Report me ye `not_testable` me hain.

**Database:** HMAGLOFDB v4, 766 records, 450 me "repeat" flag. Sources mixed hain, isliye ye **sirf screening ke andaaze** hain, flood
routing nahi.

---

## G5 · Geo-PINN: neural network ko physics sikhaana   [Class A/B, NOT ADMITTED]

### Idea
Landslide ke asli labels kam hain (736 rows, 184 positive). Ek normal neural network itne kam data par ratta maar leta hai. PINN ko ek
**extra teacher** milta hai: Iverson ka diffusion equation (P01), jo label ke bina har jagah check ho sakta hai.

### Network
1. Field net: (Z depth, t time, rain, 6 slope features) → ψ (pressure head).
2. ψ se pore pressure u = γ_w·max(ψ, 0) (γ_w = 9.81 kN/m³), phir infinite-slope FS (P01, differentiable version).
3. Risk head: (ψ, tanh ψ, FS, features) → landslide probability.

### Loss (teen hisse)
$$\mathcal L = w_d\,\mathrm{BCE} + w_p\,\overline{\left(\partial_t\psi - D_1\,\partial_{ZZ}\psi\right)^2} + w_{fs}\,\overline{\mathbb 1[FS<1](1-p)^2}$$
- **BCE (w_d = 1):** jahan label hai, sahi jawab do.
- **PDE residual (w_p = 1):** ψ_t − D₁ψ_ZZ = 0 hona chahiye. Ye derivatives automatic differentiation (autograd) se nikalte hain.
  D₁ = D₀/cos²β. Slope sirf yahin aata hai (bug-guard, deterministic gate jaisa).
- **FS hinge (w_fs = 0.5):** agar network ki apni physics FS < 1 bole, to risk kam mat bolo.

### Result (OUR RESULT, spatial block CV, 736 rows)
- OOF ROC-AUC **0.716**, PR-AUC 0.463, ECE 0.099, recall at 5% FPR 0.23.
- **Simple baselines se kam:** rain logistic 0.781, Caine 0.758 (P01).
- **Admission gate (Rule 16):** climatology aur logistic par confidence-interval jeet chahiye thi. Nahi mili → `admitted: false`.
  Is model ki koi performance claim nahi ki jaati, aur deploy nahi hota.

### Kyun haara? (hypotheses, tested nahi)
Data case-control hai (25% positive, asli duniya se bahut zyada). Rain features daily hain, jabki PDE ghanton ka hai. Soil parameters
(c′, φ′, D₀) har jagah ke liye **assumed** hain, measured nahi. Aur PINN ke paas 4 hisse balance karne ko hain, labels sirf 736.

## Ek nazar me
| Model | Data | Fit | Status |
|---|---|---|---|
| V = 1.396·A^1.132 | HMAGLOFDB, n = 21 | R² 0.72 (log) | Class B, screening |
| Q_p = 0.291·V^0.535 | HMAGLOFDB, n = 31 | R² 0.36 (log) | Class B, weak |
| Froehlich, Costa–Schuster | — | not testable | documented only |
| Geo-PINN | 736 rows, 101 blocks | AUC 0.716 | NOT ADMITTED |
---

# P05 · DEEP DIVE — power-law fitting, CI, aur Geo-PINN ka loss shuru se

Numbers `results/glof/glof_physics_report.json` aur `deep/geo_pinn.py`, `deep/losses.py` se hain.

## Symbol table
| Symbol | Matlab | Unit |
|---|---|---|
| A | glacial jheel ka area | m² |
| V | jheel me paani ki matra | m³ |
| Q_p | flood ka peak discharge | m³/s |
| a, b | power-law coefficient aur exponent | a ki unit b par depend karti hai |
| ψ(Z, t) | pressure head (mitti me paani ka dabaav, metre of water) | m |
| Z, t | gehraai, samay | m, s |
| D₀, D₁ | hydraulic diffusivity; D₁ = D₀/cos²β | m²/s |
| u_w | pore pressure = γ_w · max(ψ, 0) | kPa |
| w_d, w_p, w_fs | loss weights (data, PDE, FS hinge) | – (1, 1, 0.5) |

## D1 · Power law ko seedhi line kaise banate hain (least squares, derivation)
1. Model: y = a·x^b. Log lo: **Y = α + b·X**, jahan Y = log₁₀y, X = log₁₀x, α = log₁₀a.
2. Least squares: aisa α, b chuno jo Σ(Yᵢ − α − bXᵢ)² minimum kare. α aur b se derivative 0 rakho:
   - ∂/∂α = 0 → α = Ȳ − b X̄ (line hamesha "average point" se guzarti hai)
   - ∂/∂b = 0 → **b = Σ(Xᵢ − X̄)(Yᵢ − Ȳ) / Σ(Xᵢ − X̄)² = cov(X, Y) / var(X)**
3. Wapas: **a = 10^α**.
4. **R² (log space)** = 1 − Σ(residual²) / Σ(Yᵢ − Ȳ)². Area-volume par 0.719: log(V) ke 72% utaar-chadhaav area samjha deta hai.
5. **log10 RMSE** = √(mean residual²). 0.487 → typical galti factor = 10^0.487 = **3.07×**; peak fit me 10^0.824 = **6.66×**.

**Dhyaan:** log space me fit karne se jo curve milta hai wo y ka **median** batata hai, mean nahi (retransformation bias). Screening ke
liye ye theek hai, lekin flood volume ka "expected" number thoda zyada ho sakta hai.

## D2 · Bootstrap confidence interval (b kitna pakka hai?)
1. n rows me se n rows **replacement ke saath** random chuno (kuch rows do baar, kuch ek baar bhi nahi).
2. Is naye sample par b fit karo. Ye 1,000–2,000 baar karo.
3. Saare b ko sort karo; 2.5% aur 97.5% wale values = **95% CI**.
4. Area-volume: b = 1.132, CI **[0.711, 1.496]**. CI me 1 bhi hai → hum pakka nahi keh sakte ki badi jheelein "gehri" bhi hoti hain
   (b > 1). n = 21 par itna hi bharosa banta hai.

## D3 · Worked chain: jheel ka area → paani → peak flood (WORKED EXAMPLE)
| Area A | V = 1.396·A^1.132 | Q_p = 0.291·V^0.535 |
|---|---|---|
| 0.1 km² (10⁵ m²) | **0.64 million m³** | **371 m³/s** |
| 1 km² (10⁶ m²) | **8.65 million m³** | **1,498 m³/s** |

- Area 10× → paani 10^1.132 = **13.6×** → peak 13.6^0.535 ≈ **4.0×**. Dugna area → paani 2^1.132 = 2.19×.
- Dono galtiyaan judti hain: final peak ka typical uncertainty ≈ 6–20× tak ja sakta hai. Isliye ye **"kaunsi jheel pehle dekhni hai"**
  (screening/ranking) ke liye hai, evacuation zone banane ke liye nahi.

## D4 · Geo-PINN: Iverson equation network me kaise "ghusaya"
**Physics (P01 se):** barish ke baad pressure head neeche ki taraf diffuse hota hai:
$$\frac{\partial \psi}{\partial t} = D_1 \frac{\partial^2 \psi}{\partial Z^2}, \qquad D_1 = D_0/\cos^2\beta$$

**Step 1 · Field network:** ek MLP ψ_θ(Z, t, rain, static) → ψ. (static = c′, φ′, γ, z, β, susceptibility; hidden 128-128-128.)

**Step 2 · Residual autograd se:** PyTorch ψ ko Z aur t ke function ki tarah differentiate kar sakta hai:
- ψ_t = ∂ψ/∂t, ψ_Z = ∂ψ/∂Z, ψ_ZZ = ∂ψ_Z/∂Z (doosri baar differentiate).
- **residual r = ψ_t − D₁·ψ_ZZ**. Agar network physics maan raha hai to r ≈ 0 hona chahiye — **kisi bhi** (Z, t) par, label ke bina.
  Isliye PDE term "free teacher" hai: jitne chaho utne collocation points.

**Step 3 · Physics se FS (differentiable):** u_w = 9.81 · max(ψ, 0), phir P01 ka infinite-slope formula:
$$FS = \frac{c' + (\gamma z\cos^2\beta - u_w)\tan\phi'}{\gamma z \sin\beta\cos\beta}$$
Ye bhi torch me likha hai, isliye gradient FS se ψ tak wapas jaata hai.

**Step 4 · Risk head:** [ψ, tanh ψ, FS, static] → MLP (64-32) → logit → probability p.

**Step 5 · Loss (code exactly):**
$$\mathcal L = \underbrace{w_d\,\mathrm{BCE}(p, y)}_{\text{labels se}} + w_p\Big[\underbrace{w_p\,\overline{r^2}}_{\text{PDE}} + \underbrace{w_{fs}\,\overline{\mathbb 1[FS<1]\,(1-p)^2}}_{\text{FS hinge}}\Big]$$
- `physics_loss()` andar w_p·PDE + w_fs·hinge lautaata hai, aur `geo_pinn_step()` use phir w_p se guna karta hai. Defaults
  w_p = 1 par ye kuch nahi badalta; agar koi w_p badle to dhyaan rahe ki PDE term w_p² se scale hoga.
- **FS hinge ka matlab:** jahan network ki apni physics FS < 1 bole, wahan p ko 1 ki taraf dhakelo. Ye sirf "kam risk mat bolo" kehta
  hai — jaise TRINETRA ka shield, jo alert badha sakta hai, ghata nahi sakta.

**Step 6 · Training detail jo bug bachata hai:** Z aur t ko har batch me `detach().requires_grad_(True)` se naya leaf tensor banaya jaata
hai, taaki autograd do GPUs (DataParallel) par bhi chale.

## D5 · Result ko kaise padhein
- OOF ROC-AUC **0.716** < Caine **0.758** (zero training) < rain logistic **0.781**. Gate ne `admitted: false` diya.
- Matlab: is data par PINN ne physics ko "behtar" nahi seekha; seedhi physics (Caine) aur seedha logistic usse aage hain.
- Ye negative result bhi useful hai: TRINETRA live system me sirf deterministic gate (FS + Caine + shield) chalta hai; PINN sirf research.

## Kamiyaan (honest)
- GLOF: n = 21 / 31, mixed sources, dam height aur breach data nahi → Froehlich / Costa–Schuster test nahi hue.
- PINN: soil parameters assumed (measured nahi), barish daily (PDE ghanton ka), labels case-control (25% positive).
- Koi bhi GLOF number field-validated nahi hai; flood routing (paani neeche ghaati me kahan tak jaayega) model nahi kiya.

## Khud check karo (self-test)
1. A = 0.5 km² ho to V kitna? *(1.396 × (5×10⁵)^1.132 ≈ 3.95 million m³.)*
2. b ka CI [0.711, 1.496] hai. Kya hum keh sakte hain "badi jheel zyada gehri hoti hai"? *(Nahi, CI me 1 shaamil hai.)*
3. PDE residual ke liye labels kyun nahi chahiye? *(Residual sirf ψ aur uske derivatives par depend karta hai, label par nahi.)*
4. FS hinge risk ko ghata sakta hai kya? *(Nahi, sirf jahan FS < 1 hai wahan p ko upar dhakelta hai.)*
<!-- END -->
