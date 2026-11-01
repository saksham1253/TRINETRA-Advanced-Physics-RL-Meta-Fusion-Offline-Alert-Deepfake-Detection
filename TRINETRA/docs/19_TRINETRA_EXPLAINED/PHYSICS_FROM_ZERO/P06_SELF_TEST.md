# P06 — Khud ko jaancho: self-test, glossary aur formula sheet

## A. Formula sheet (ek page me sab)
| # | Formula | Matlab | Class | Chapter |
|---|---|---|---|---|
| 1 | FS = [c′ + (γz cos²β − u) tan φ′] / (γz sinβ cosβ) | pakad ÷ khinchaav; < 1 = girega | A | P01 |
| 2 | ΔFS = γ_w ψ tanφ′ / (γz sinβ cosβ) | paani ne kitni pakad chheeni (c′ ki zaroorat nahi) | B | P01 |
| 3 | ψ(Z,t) via Iverson ierfc | baarish ke baad mitti me paani ka dabaav | A | P01 |
| 4 | I = 14.82·D^(−0.39) | Caine: kitni baarish kitni der | B | P01 |
| 5 | 1/v → 0 linear | Fukuzono: girne ka samay | B | P01 |
| 6 | L = 0.235 Q^(2/5) − 1.02 D | flame height | A | P02 |
| 7 | ΔT = 25 Q_c^(2/3) z^(−5/3) | plume temperature | A | P02 |
| 8 | N_c = 2gQ_c / (ρ c_p T U³) | hawa vs plume | A | P02 |
| 9 | f = 1.5 / √D | flicker frequency | A | P02 |
| 10 | E = εσT⁴, τ = e^(−kL) | garmi ki roshni, dhuan | A | P02 |
| 11 | p\* = C_FA / (C_FA + C_miss) | alarm kab | A | P03 |
| 12 | Bayes prior shift | base rate correction | A (PROPOSED) | P03 |
| 13 | σ(logit p / T) | calibration | A | P03 |
| 14 | w̃ = r·c·e^(−u/τ) | fusion weight | B | P03 |
| 15 | 1 − Π(1 − pᵢ) | noisy-OR | B | P01/P03 |
| 16 | FSPL = 20log d + 20log f + 32.44 | radio loss | A | P04 |
| 17 | r₁ = √(λd₁d₂/d) | Fresnel zone | A | P04 |
| 18 | L(r) = L_ref − 20log(r/r_ref) − αΔr | siren | A + ASSUMPTION | P04 |
| 19 | V = 1.396 A^1.132; Q_p = 0.291 V^0.535 | GLOF | B (OUR FIT) | P05 |
| 20 | ψ_t − D₁ψ_ZZ = 0 as loss | Geo-PINN | A/B, NOT ADMITTED | P05 |

## B. Glossary (A–Z)
- **AUC (ROC-AUC):** ek random aag wali aur ek random bina-aag image lo. Model aag wali ko zyada score de, iska chance. 0.5 = sikka, 1 = perfect.
- **Base rate / prior:** asli duniya me ghatna kitni baar hoti hai.
- **Block CV:** paas-paas ki jagahon ko ek saath train ya test me rakhna, taaki model "padosi yaad karke" na jeete.
- **Calibration / ECE:** model ke "80%" ka sach me 80% hona. ECE = average galti.
- **Class A/B/C/SURROGATE:** A = textbook physics, B = data se fit, C = humara naya idea (untested, default OFF), SURROGATE = sirf dikhane ke liye.
- **Cohesion c′:** mitti ka "gond", bina dabaav ki pakad (kPa).
- **dB / dBm:** log scale. +10 dB = 10×. 30 dBm = 1 W.
- **Fade margin:** link budget me rakha safety cushion.
- **Friction angle φ′:** mitti ke daanon ka aapas me ragad (degrees).
- **Fresnel zone:** radio ka "football" jaisa raasta, jo khaali hona chahiye.
- **Noisy-OR:** "koi bhi ek kaaran kaafi hai" wala probability jod.
- **OOF (out-of-fold):** wo score jo model ne us data par diya jo usne training me nahi dekha.
- **Pore pressure u:** mitti ke chhedon me paani ka dabaav. Ye daanon ko alag dhakelta hai.
- **p\*:** cost-loss threshold.
- **Power law:** y = a·x^b. Log-log par seedhi line.
- **Strouhal number:** flicker frequency ka dimensionless roop.
- **Temperature scaling T:** calibration ka ek knob.
- **Unit weight γ:** mitti ka wazan per volume (kN/m³).

## C. Self-test (jawab neeche)
1. Dry slope ka FS 1.17 hai. Baarish ke baad ψ = 1 m hua. FS badhega ya ghatega, aur kyun?
2. ΔFS ke liye c′ kyun nahi chahiye?
3. Caine threshold 24 ghante ke liye 4.05 mm/h hai. 120 mm in 24 h ka ratio kya hai, aur kya ye threshold se upar hai?
4. Fire ki power dugni ki. Flame height kitni guna?
5. Hawa 2 se 4 m/s hui. Byram N_c kitna guna badlega?
6. 2 fps camera 2.12 Hz flicker ko kis frequency par dekhega?
7. C_FA = 5, C_miss = 100. p\* kya hai? Agar C_miss = 1000 ho jaaye?
8. Model training me 55% aag dekhta tha. Asli duniya me 1%. Model ke 0.3 ka asli matlab kya hoga, badhega ya ghatega?
9. Stack ka AUC CLIP se kam hai. Phir bhi stack ka kya fayda hai?
10. Radio ki doori dugni. Free-space loss kitna badhega?
11. Path-loss exponent 3.0 se 3.6 hua. SF10 range kitni bachi?
12. 20 km link par beech me Fresnel radius aur earth bulge kitna hai?
13. GLOF Q_p fit ka R² 0.36 hai. Ise flood warning ke liye seedha kyun use nahi karna chahiye?
14. Geo-PINN 0.716 AUC ke saath deploy kyun nahi hua?
15. Fire perimeter animation ko "prediction" kyun nahi kehna chahiye?

### Jawab
1. Ghatega: 1.17 → 0.83. Paani daanon ke beech ka dabaav (normal stress) kam karta hai, aur ragad wali pakad usi se banti hai.
2. ΔFS do FS ka antar hai. c′ dono me ek jaisa hai, isliye cancel ho jaata hai.
3. 120/24 = 5 mm/h. Ratio 5/4.05 ≈ 1.23 > 1, yaani upar hai.
4. 2^0.4 ≈ 1.32 guna (agar D chhota ho; −1.02D term ko chhod kar).
5. U³ ki wajah se 1/8, yaani N_c 8 guna kam.
6. ~0.12 Hz (aliasing).
7. 5/105 = 0.048. C_miss = 1000 → 5/1005 ≈ 0.005 (zyada alarm).
8. ~0.0035. Bahut ghatega.
9. Calibration behtar hai (held-out ECE 0.026 vs CNN 0.260). Ye bhi ki koi ek expert fail ho to baaki sambhaal lete hain. Lekin wo admit nahi hua, isliye accuracy ka claim nahi.
10. +6 dB.
11. ~9.1 km se ~2.0 km.
12. ~41.6 m Fresnel radius aur ~5.9 m bulge.
13. Typical galti ~6.7× hai. Breach height aur dam type jaise mukhya factors nahi hain.
14. Simple baselines (rain logistic 0.781, Caine 0.758) se haara, aur admission gate fail hua (Rule 16).
15. Repo me fire spread model nahi hai. Ye Anderson ellipse ka SURROGATE hai, jisme L/B 8 par cap hai.

## D. Practical guide: koi number dekho to 5 sawaal poocho
1. **Kaunsa class?** A, B, C ya SURROGATE?
2. **Kaunsa data?** Real, synthetic ya worked example?
3. **Kaunsa split?** OOF, spatial block, ya held-out alag dataset?
4. **Per-image ya per-incident?**
5. **Claim ladder par kahan?** (C0–C3. TRINETRA kahin bhi C4, yaani field-validated, claim nahi karta.)
<!-- END -->
