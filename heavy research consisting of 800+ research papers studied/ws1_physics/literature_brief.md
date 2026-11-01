# WS1 — PHYSICS / PIML — literature brief (P4, 2026-10-07)
Owner phase: P7. Scope: landslide/flash-flood/GLOF physics backbone, FoS, EVT tail, physics surrogates.

## Most relevant papers
- **2407.06785** PINN for landslide prediction (JGR-ML 2024, peer-reviewed, code+data open). NN retrieves
  geotechnical params from proxies, constrains with Newmark permanent-deformation; outputs geotech maps.
  Claim: physics-as-constraint beats free regression AND yields interpretable geotech fields.
  Caveat: COSEISMIC trigger — borrow STRUCTURE, use hydrological physics (Iverson) for our rainfall trigger.
- **2507.15614** HEC-RAS Geo-FNO surrogate. GRU + Geometry-Aware Fourier Neural Operator; 67 Mississippi
  reaches; median stage err 0.31 ft; ensemble wall-clock 139→40 min (3.5×). Claim: a surrogate makes cheap
  ensembles feasible. Caveat: needs a calibrated solver to emulate; large-river hydraulics.
- **2610.04828** FoS→failure-probability map is nonlinear → treat FoS as a GATE (C-15).
- **2509.10362** GNN-rP (r-Pareto POT on IMERG) + **2510.12328** (season-aware GPD/POT, ~SEAS5) → explicit
  EVT tail head as a wide-uncertainty prior (C-06). Caveat: unstable with few exceedances.
- Physics anchors (re-derive on paper in P7): FS=Ff+Fw+Fc infinite-slope/TRIGRS; Iverson(2000) ψ(Z,t),
  D1=D0/cos²δ (Bug#3); Fukuzono/Voight 1/v=A(α−1)(t_f−t), α≈2 (Bug#4); Caine I=a·D⁻ᵇ; Lu&Likos σ_s=−S_e·ψ (Bug#2).

## Key claims → references
- Learn a bounded residual on a mechanistic backbone, never from scratch — THREAD I (7×). → DC-06.
- Physics enters as a monotone gate/constraint, not a regressed probability. → DC-08 (2610.04828, 2407.06785).
- Tail/EVT is a zoning prior, not a real-time alarm. → DC-07.
- Surrogate only where a calibrated model/gauge exists; else EVT prior + gate + wide UQ. → DC-14.

## Open questions
- Spatial-correlation range r for Himalayan terrain (anisotropic valleys) — needed to set the CV buffer (DC-01).
- Does the Newmark PINN structure transfer to rainfall pore-pressure physics? (FM-39) — test in P7.
- Rockfall (rigid-block) hazard is uncovered by the saturated-slope stack (G7/DC-20).
- I–D / GLOF constants still open (Bug#15) — resolve with non-arXiv (Caine, NHESS) in P7.
