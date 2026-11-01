# CH05 — PHYSICS MODELS (cards + workflows). Detailed cards: docs/04_PHYSICS_MODELS_HINGLISH.md (same content, not repeated here).

> **Physics bilkul zero se?** Beginner-level book (derivations, misaal, worked examples, kamiyaan, figures): [`PHYSICS_FROM_ZERO/P00_START_HERE.md`](PHYSICS_FROM_ZERO/P00_START_HERE.md).

## Overview: how the physics connects
```mermaid
flowchart LR
  R[NASA POWER rain] --> C[Caine I-D ratio  A]
  R --> I[Iverson head psi  A]
  DEM[Copernicus DEM slope beta] --> I
  DEM --> FS[Infinite-slope FS  A]
  I --> FS
  FS --> D[dFS  B]
  FS --> BC[back-analysed c'  B]
  C --> G[geo_gate noisy-OR]
  FS --> G
  G --> F[fusion: p, consistency c_i]
  FS --> SH[shield floor FS<1]
  D --> RL[RL hazard sigma(a + b dFS)]
  V[Video frames] --> FG[fire_gate: Byram N_c  A]
  FG --> F
```
Hinglish: barish aur slope do asli inputs hain. Caine batata hai barish "line ke upar" hai ya nahi. Iverson batata hai paani kitna neeche pahuncha,
aur FS batata hai slope kitna mazboot bacha. Ye sab fusion ko probability aur "physics se mel" (c_i) dete hain. FS<1 ho to shield level badha deta hai.

## Workflow per model (inputs → steps → outputs → flags)
| Model | Inputs | Steps | Output | Validity flag |
|---|---|---|---|---|
| Caine (A) | daily rain 30 d | wet-spell D (days ≥ 1 mm × 24), I = sum/D, ratio = I / (14 D^-0.39) | ratio | needs local refit |
| Iverson (A) | rain steps, β, K_z, D0, Z | flux capped at K_z → superposed ierfc response → ψ, capped at z cos²β | ψ (m) | I ≤ K_z |
| FS (A) | c′, φ′, γ, z, β, u_w = γ_w ψ | infinite-slope equation | FS | planar slip |
| Back-analysis (B) | β, φ′, γ, z | c′ such that FS_dry = 1.2 | c′_bc | slope must be standing |
| ΔFS (B) | ψ, β | γ_w ψ tanφ′ / (γ z sinβ cosβ) | ΔFS | c′-free |
| geo_gate | FS, Caine, Fukuzono | p_fs = σ(4(1−FS)), p_caine = clip(ratio−0.5), noisy-OR | p_phys, consistency | Class labels kept |
| fire_gate (A) | detector conf, Q, U | N_c = 2gQ/(ρ c_p T U³); c ×= clip(N_c/2, 0.3, 1) | ExpertOutput(FIRE) | ND terms OFF |

## Parameter table (Layer 3)
| Name | Symbol | Unit | Value in code | Source | Kam → | Zyada → | Sensitivity |
|---|---|---|---|---|---|---|---|
| friction angle | φ′ | ° | 32 | ASSUMPTION (build_geo.SOIL) | FS down | FS up | not tested |
| unit weight | γ | kN/m³ | 19 | ASSUMPTION | — | — | not tested |
| slip depth | z = Z | m | 2 | ASSUMPTION | faster wetting | slower | not tested |
| conductivity | K_z | m/s | 1e-5 | ASSUMPTION | flux capped earlier | more head | not tested |
| diffusivity | D0 | m²/s | 5e-5 | ASSUMPTION | slower response | faster | not tested |
| dry FS target | — | — | 1.2 | ASSUMPTION (back-analysis) | weaker soil | stronger | not tested |
| Caine | a, b | — | 14, 0.39 | repo constant (coeff-verify) | more exceedance | less | AUC 0.758 at defaults |

## Worked example (hand-computed): Caine
3 wet days, 90 mm in total, so D = 72 h and I = 1.25 mm/h. I_thr = 14 × 72^-0.39 = 14 / 5.30 = 2.64 mm/h, so the ratio is 0.47 (below the line).

## Honest status
Caine, ΔFS and the back-analysed geo gate were measured on 184 real events (CH12). Iverson head dynamics are not testable without piezometer data.
Fire physics is not validated on data in this hackathon.

**Common galti:** absolute FS ko sach maan lena jab soil maana hua ho. **Self-check:** ΔFS c′ par depend kyun nahi karta? (c′ numerator me
dono FS me same hai, difference me cancel ho jaata hai.)
<!-- END -->
