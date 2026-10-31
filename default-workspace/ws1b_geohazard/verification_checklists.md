# ws1b_geohazard/verification_checklists.md — per-model verification (P7G)

Phase P7G · WS1b · RESEARCH-ONLY. Dimensional consistency, limit behaviour, and (Layer 2) reduction-to-
parent — hand-checked + independently re-derived. [coeff-verify] items need primary-source confirmation;
all need geotechnical/hydrology expert review before external use.

## Layer 1
| Model | Dim check | Limit/sanity | Notes |
|-------|-----------|--------------|-------|
| GH-01 | PASS (FS dimensionless) | FS↓ as m↑ (wetter) ✓; FS↑ as c',φ'↑ ✓ | params [coeff-verify] |
| GH-02 | PASS (head m) | ψ rises with rainfall pulse; →steady as t→∞ ✓ | D₀,K_s [coeff-verify] |
| GH-03 | PASS | reduces to Darcy at saturation ✓ | stiff; vanGenuchten params |
| GH-04 | PASS (m/s; m) | f→K_s as F→∞ ✓ | ψ_f,Δθ scarce |
| GH-05 | PASS (mm/h vs h) | I↓ as D↑ (power law) ✓ | α,β regional [coeff-verify] |
| GH-06 | PASS (H/L dimensionless) | mobility↑ (H/L↓) with V ✓ | scatter |
| GH-07 | PASS (stress) | τ→Coulomb as v→0 ✓ | μ,ξ calibration |
| GH-08 | PASS (mm) | Q→0 as P→λS; Q→P as S→0 ✓ | 0.2 Ia disputed |
| GH-09 | PASS (m/s) | v↑ with R_h,S_f; ↓ with n ✓ | n uncertain |
| GH-10 | PASS | reduces to kinematic wave when inertia negligible ✓ | solver needed |
| GH-11 | PASS | mass-conserving linear routing ✓ | K,X calibration |
| GH-12 | PASS | Q↑ with stage ✓ | hysteresis |
| GH-13 | PASS | Q_p↑ with V_w,h_b ✓ | huge scatter |

## Layer 2 (reduction-to-parent) — INDEPENDENTLY RE-DERIVED, 0 ERRORS (second agent, 2026-10-09)
| Model | Dim check | Reduction to parent | Falsifiable? |
|-------|-----------|---------------------|--------------|
| GB-01 | PASS (P_f∈[0,1]) | σ_i→0 ⇒ β_rel→±∞ ⇒ P_f→1{FS<1} ✓ | yes — Brier/net-benefit vs deterministic |
| GB-02 | PASS (1/T_lag=s⁻¹) | T_lag→0,noise→0,params known ⇒ ψ_m→ψ ✓ | yes — lag/bias vs raw on step tests |
| GB-03 | PASS (x dimensionless) | α(S)=α₀,w₁→∞,p*=0.5 ⇒ step at I=α₀D^(−β) ✓ | yes — Brier/AUC/net-benefit vs ID line |
| GB-04 | PASS (mm) | λ=0.2,r=1 ⇒ exact GH-08 ✓ | yes — NSE vs fixed-CN |
| GB-05 | PASS (Jones factor dimensionless) | dh/dt→0 ⇒ Q→Q_s ✓ | yes — limb-bias vs single rating |

Independent-check verdict (second agent): **all five internally CORRECT** on algebra, dimensions, and
reduction-to-parent; no errors. Harmless caveats recorded: (i) GB-01/GB-03 take logs/derivatives of
individually dimensional quantities, well-defined only as the dimensionless COMBINATIONS shown; (ii) GB-02's
first-order kernel normalizes to 1 only over full support (t→∞). Neither affects the stated claims. Verified
sign ∂FS/∂m = −γ_w z cos²β tanφ′/(γ z sinβ cosβ) < 0.

## Open verification items (carried)
- Confirm every [coeff-verify] constant (Iverson 2000; Caine/regional ID α,β; Scheidegger/Corominas; SCS-CN;
  Manning n; Froehlich GLOF) against primary sources.
- Geotechnical + hydrology expert review of all derivations before any external use.
