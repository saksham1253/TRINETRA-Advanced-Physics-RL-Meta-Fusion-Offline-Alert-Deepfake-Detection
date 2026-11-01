# 04 — PHYSICS MODELS (model cards, Hinglish). Numbers only from `results/RESULTS.md` (generated, see docs/14).

## 1. Caine rainfall intensity-duration threshold   [Class A]   status: in code (`ws1b_geophys/caine.py`)
1. **Ye kya hai:** barish ki "speed" (I, mm/h) aur "kitni der" (D, hours) se ek line banti hai. Line ke upar = landslide ka
   khatra. Jaise doodh ubalne ki seema: thodi der tez aanch ya bahut der dheemi aanch, dono se ubal aata hai.
2. **Kyun:** zero-training physics prior. Jahan labels nahi, wahan bhi kaam karta hai.
3. **Equation:** $I_{thr} = a\,D^{-b}$, ratio $= I / I_{thr}$.

   | symbol | meaning | unit |
   |---|---|---|
   | I | mean rain intensity of the wet spell | mm/h |
   | D | wet-spell duration (consecutive days >= 1 mm, x24) | h |
   | a, b | 14, 0.39 (repo constants; Caine 1980 global 14.82, 0.39 is from memory, [coeff-verify]) | - |
4. **Validity:** shallow rain-triggered landslides; a global line, so it must be refit locally (repo docstring says so).
5. **Source:** Caine (1980); equation/page not verified in the repo (bug report #15).
6. **Code:** `caine_exceedance(I, D, a, b)`, used by `geo_gate`, `build_geo.py`, `env_landslide.py`.
7. **Fusion link:** soft `p_caine = clip(ratio - 0.5, 0, 1)` inside `geo_gate` (noisy-OR).
8. **Honest status:** tested on REAL events (NASA GLC India + NASA POWER rain). ROC-AUC in `results/RESULTS.md` (row `caine_ratio`).
9. **Failure cases:** daily POWER rain (0.5 deg) smooths cloudbursts, so I is underestimated. The fix is IMERG 0.1 deg (P40, free login).
10. **Worked example (hand-computed):** 3 wet days, 90 mm in total, so D = 72 h and I = 1.25 mm/h. Then I_thr = 14·72^-0.39 = 14/5.30 = 2.64 mm/h,
    and the ratio is 0.47, i.e. below the line.

## 2. Iverson (2000) transient pressure head   [Class A]   status: in code (`ws1b_geophys/iverson.py`)
1. **Ye kya hai:** barish ka paani mitti me neeche jaata hai, aur slip surface par pressure head ψ badhta hai. Jaise sponge par paani daalo:
   upar se neeche dheere-dheere geela hota hai.
2. **Kyun:** pore pressure u = γ_w ψ hi FS ko girata hai.
3. **Equation:** ψ(Z,t) = ψ0 + Σ_k ((I_k − I_{k−1})/K_z)·R(Z, t − t_k), with R = sqrt(4 D1 τ)·ierfc(Z / sqrt(4 D1 τ)) and D1 = D0 / cos²β.

   | symbol | meaning | value used |
   |---|---|---|
   | Z | slip depth | 2 m (ASSUMPTION) |
   | K_z | saturated conductivity | 1e-5 m/s (ASSUMPTION) |
   | D0 | hydraulic diffusivity | 5e-5 m²/s (ASSUMPTION) |
   | I_k | surface flux, capped at K_z | NASA POWER daily rain |
   | ψ0 | initial head | 0 m (monsoon water table near slip plane, ASSUMPTION) |
4. **Validity:** I ≤ K_z, 1-D vertical infiltration. Head is capped at hydrostatic saturation z·cos²β.
5. **Source:** Iverson (2000); superposition as in Baum et al. (TRIGRS). Slope enters ONLY via D1 (bug-guard, golden tests).
6. **Code:** `transient_head_multipulse` (used by `build_geo.py` and `env_landslide.py`).
8. **Status:** runs on real rain. Soil parameters are not observed, and this is the biggest weakness.

## 3. Infinite-slope factor of safety + BACK-ANALYSIS   [Class A + standard practice]   status: `fs.py` + new code
1. **Ye kya hai:** slope ko pakadne wali taakat ÷ girane wali taakat. FS < 1 matlab slope gir sakta hai.
3. **Equation:** FS = [c′ + (γ z cos²β − u_w) tan φ′] / (γ z sin β cos β).
4. **Finding (OUR RESULT, 2026-10-31):** with c′ = 5 kPa, φ′ = 32°, γ = 19 kN/m³, z = 2 m, the Himalayan event slopes (p90 ≈ 40-44°) give
   **FS < 1 even when dry**, which is physically impossible for slopes that are still standing. So the absolute FS is mis-calibrated, and the
   repo shield (`FS<1 -> ORANGE`) would fire forever (bug B-23).
5. **Fix (back-analysis, Class B):** per site, choose c′ so that FS_dry = 1.2:
   c′_bc = 1.2·γ z sinβ cosβ − γ z cos²β tanφ′ (clipped ≥ 0). Hinglish: slope abhi khada hai, isliye sukhe mausam me FS thoda 1 se upar
   maan lo, aur usse mitti ki taakat ulta nikaal lo.
6. **Rain signal:** ΔFS = FS_dry − FS_wet = γ_w ψ tanφ′ / (γ z sinβ cosβ). This **does not depend on c′**, so it is robust to the unknown
   cohesion. It is used as the physics feature `dfs` and as the RL hazard driver.
   *Dimensional check:* kPa / kPa = dimensionless ✓. *Limit:* ψ → 0 gives ΔFS → 0 ✓.
7. **Status:** `dfs` and the back-analysed `geo_gate` are tested on real events (results/RESULTS.md). Novelty: not claimed (back-analysis is standard).

## 4. GLOF empirical relations   [Class B: fitted on our data]   status: new (`kaggle/glof_physics_check.py`)
- Lake volume vs area V = a·A^b and peak discharge vs volume Q_p = c·V^d, fitted log-log on ICIMOD HMAGLOFDB v4 with bootstrap CIs.
- Repo formulas GH-13 Froehlich (Q_p = c V^p h_b^q) and Costa-Schuster (Q_p = 0.763 PE^0.42) are **not testable**: the database has no
  breach or dam height. Say this plainly.
- Hinglish: jheel jitni badi, paani utna zyada, aur jitna zyada paani, utna bada flood peak. Lekin data bahut kam hai (n ≈ 20-30).

## 5. Fire physics (code, unchanged)   [Class A, coeff-verify]
Heskestad flame height L = 0.235 Q^(2/5) − 1.02 D, Strouhal puffing f ≈ 1.5 D^(−1/2), Byram convection number (regime check used by
`fire_gate`), gray-body radiance, Beer-Lambert. Not validated on data in the hackathon (NIST FCD P31 is a lead for realistic Q).

## 6. What validates / falsifies each model (prototype pack)
| model | data | test | script |
|---|---|---|---|
| Caine, ΔFS, geo_gate | NASA GLC + POWER + Copernicus DEM | event vs control-day ROC-AUC, spatial-block CV, bootstrap CI vs rain baseline | `geo_physics_hindcast.py` |
| Iverson head dynamics | no piezometer data | not testable now | lead: field piezometer series |
| GLOF relations | HMAGLOFDB | power-law fit + CI | `glof_physics_check.py` |
| Geo-PINN | geo.npz (built from the above) | OOF AUC + admission gate | `train_geo_pinn.py` |
| Landslide RL | physics simulator + real rain | online return vs rules, paired CI | `rl_env_eval.py` |
<!-- END -->
