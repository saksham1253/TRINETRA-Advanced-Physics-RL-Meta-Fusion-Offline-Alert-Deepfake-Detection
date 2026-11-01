# ws1_physics/established_formula_inventory_P21.md — P21 extension to the Class-A inventory

Phase P21 · RESEARCH-ONLY · WS1a. Extends the P7 Class-A inventory (established_formula_inventory.md,
EF-01…EF-12) with additional canonical relations surfaced by the P21 deep-dive. SOURCE-REPORTED; coefficients
[coeff-verify] against PRIMARY sources before any use (the P21 reader worked from abstracts). These are
CLASS A (established) building blocks for the Class-C derivations; nothing here is novel or a result.

| ID | Relation | Canonical form (schematic) | Role for us | Verify |
|----|----------|----------------------------|-------------|--------|
| EF-13 | Byram convective number N_c / critical Froude | ratio of buoyant power to flow kinetic power sets plume bending onset | regime gate (ND-6), wind-tilt (ND-5) | [coeff-verify] 2501.08343, 2406.08589 |
| EF-14 | Radiative transfer equation (RTE) | dI/ds = −(κ+σ)I + emission + scattering | smoke/soot radiation, ND-2 | [coeff-verify] 2009.13291 |
| EF-15 | WSGGM non-gray gas/soot radiation | weighted-sum-of-grey-gases emissivity | soot radiative loss term, ND-2/ND-6 | [coeff-verify] 2102.11060 |
| EF-16 | Strouhal puffing scaling | f_p ≈ 1.5·D^(−1/2) (pool-fire class) | flicker band prediction, ND-1 | [coeff-verify] classical + 2202.06567 |
| EF-17 | Advection–diffusion–reaction (ADR) transport | ∂C/∂t + u·∇C = ∇·(D∇C) + R | smoke/gas transport lag, ND-4/ND-7 | [coeff-verify] 1910.09098, 2207.05748 |
| EF-18 | Firebrand/particle transport (Stokes/drag + lofting) | drag + buoyancy ballistics, St-dependent | documented only (beyond pilot) | 2206.01529, 2411.13275 |
| EF-19 | G-equation flame-front kinematics | ∂G/∂t + u·∇G = S_L|∇G| | flicker describing-function, offline sim | [coeff-verify] 2609.09773 |
| EF-20 | Rothermel + Huygens front propagation (slope) | ROS as f(fuel, wind, slope) | wildfire simulator C-01 (offline) | [coeff-verify] 2412.18931 |

NOTES. EF-13…EF-20 are canonical/established but their COEFFICIENTS and regime-of-validity must be confirmed
against primary textbooks/papers (SFPE Handbook, Drysdale, original authors) — the reader saw abstracts only.
They extend, not replace, EF-01…EF-12. Live-fire deployment still uses only cheap features/priors; the heavy
relations (EF-14/15/19/20) are OFFLINE simulator/analysis tools, consistent with the P7 model-set decision.
