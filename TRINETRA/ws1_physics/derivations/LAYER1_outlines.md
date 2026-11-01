# ws1_physics/derivations/LAYER1_outlines.md — derivation outlines for the Class-A models

Phase P7 · WS1a · RESEARCH-ONLY. Per §P7 acceptance, Layer-1 (established) models require the DERIVATION
OUTLINE + the source's assumptions (the complete re-derivation lives in the primary sources cited in
established_formula_inventory.md and is a textbook exercise; we do not reproduce canonical derivations in
full, we outline them and record the assumptions and limits). Full derivations with reduction-to-parent are
reserved for the Layer-2 extensions (separate files B-01/B-02/B-05/B-06). Honesty: these outlines are from
established fire science; coefficients tagged [coeff-verify] in the inventory; the P7 quota reading cross-
checked the coefficients (see note at end).

### EF-01 Heskestad flame height — outline
Dimensional analysis of a buoyant turbulent diffusion flame gives flame height as a function of the
dimensionless HRR $Q^*=\dot Q/(\rho_\infty c_p T_\infty g^{1/2}D^{5/2})$ (Zukoski). Fitting the mean-visible
(50%-intermittency) height to gas-burner/pool data over many decades of $Q^*$ yields $L/D=15.6\,Q^{*2/5}-1.02$,
rearranged to $L=0.235\dot Q^{2/5}-1.02D$ (SI, kW). Assumptions: buoyancy-dominated, round source, still air.

### EF-02 t² growth — outline
Empirical parameterization: during unobstructed flaming growth, HRR rises ≈ quadratically, $\dot Q=\alpha
t^2$; $\alpha$ chosen so $\dot Q$ reaches 1055 kW (1000 Btu/s) at the class time (slow/medium/fast/ultrafast
= 600/300/150/75 s). Convective/radiative split $\chi_c\approx0.7,\chi_r\approx0.2$–$0.4$. Assumptions:
single growing item, no ventilation limit.

### EF-03 Heskestad plume — outline
Self-similar point-source buoyant plume: integrate conservation of mass (with entrainment $\propto$ local
velocity), momentum (buoyancy-driven) and energy with top-hat/Gaussian profiles; apply a virtual origin
$z_0$ to collapse near/far fields. Result: $\Delta T_0\propto \dot Q_c^{2/3}(z-z_0)^{-5/3}$, $u_0\propto
\dot Q_c^{1/3}(z-z_0)^{-1/3}$. Assumptions: far field, Boussinesq, constant entrainment coefficient, still air.

### EF-04 McCaffrey — outline
Measure centerline $u,\Delta T$ on a methane burner; plot vs $z/\dot Q^{2/5}$; fit three power-law regimes
(continuous flame / intermittent / plume). Plume-regime exponents recover classical plume theory
($\Delta T\propto\zeta^{-5/3}$). Assumptions: as EF-03 but regime-resolved; still air.

### EF-05 Alpert ceiling jet — outline
A plume impinges on a ceiling and spreads radially as a wall jet; conservation across the jet with the
plume delivering EF-03 fluxes yields max temperature/velocity correlations in $(\dot Q,H,r)$ with a
near-field ($r/H$ small) plateau. Assumptions: steady fire, flat unobstructed ceiling, unconfined, no wind.

### EF-06 Point-source radiation — outline
Treat the flame as an isotropic point emitter radiating a fraction $\chi_r$ of $\dot Q$; conservation of
radiant power over a sphere gives incident flux $\dot q''=\chi_r\dot Q/(4\pi R^2)$. Assumptions: far field,
optically-thin path, cold surroundings. (Solid-flame/view-factor model used in near field.)

### EF-07 Beer–Lambert extinction — outline
Differential attenuation $dI=-\sigma I\,dx$ integrates to $I=I_0e^{-\sigma L}$; $\sigma=K_m m_s$ links to
soot mass via the mass-specific extinction coefficient. Optical density $OD=\log_{10}(I_0/I)$; visibility
$V=C/\sigma$ (Jin). Assumptions: single scattering / optically-thin, uniform concentration, matched $K_m$.

### EF-08 Flicker frequency — outline
A buoyant diffusion flame has a toroidal-vortex (Kelvin–Helmholtz/baroclinic) instability; dimensional
scaling with gravity and source size gives a constant Strouhal number $St=f\sqrt{D/g}$, i.e. $f\propto
D^{-1/2}$, fitted to $f\approx1.5\,D^{-1/2}$ Hz. Assumptions: axisymmetric buoyant pool flame, no cross-flow.

### EF-09 Thermal-camera radiometry — outline
Radiative transfer along the line of sight: detected band radiance = emitted (ε·blackbody) + reflected
((1−ε)·surroundings), attenuated by atmospheric transmittance $\tau_{atm}$ plus path emission; invert
Planck's law in the camera band to retrieve $T$. Total emission $\varepsilon\sigma T^4$. Assumptions: known
$\varepsilon,\tau_{atm}$; grey body; no in-band scattering.

### EF-10 RTI / rate-of-rise — outline
Lumped-capacitance energy balance on the sensing element heated by convection from the ceiling-jet gas:
$mc\,dT_e/dt=hA(T_g-T_e)$; group constants into RTI $=\tau\sqrt{u}$ to get $dT_e/dt=(\sqrt{u}/\mathrm{RTI})
(T_g-T_e)$. Rate-of-rise logic triggers on $dT_e/dt$. Assumptions: lumped element, convection-dominated.

### EF-11 Rothermel spread — outline
Steady-state energy balance at the fire front: rate of spread = propagating heat flux / heat required for
ignition of the fuel ahead, with empirical wind $\phi_w$ and slope $\phi_s$ multipliers:
$R=I_R\xi(1+\phi_w+\phi_s)/(\rho_b\varepsilon Q_{ig})$. Assumptions: homogeneous fuel bed, quasi-steady,
surface fire.

### EF-12 Zukoski entrainment — outline
Integrate the plume entrainment hypothesis (entrainment velocity ∝ local vertical velocity) to get mass
flux $\dot m\propto\dot Q_c^{1/3}(z-z_0)^{5/3}$; virtual origin as EF-03. Assumptions: far field, still air.

## Coefficient cross-check note (quota reading, honesty)
The P7 quota reading independently restated these coefficients from the literature and they MATCH the
inventory: Heskestad $0.235/1.02$; McCaffrey three-regime $z/\dot Q^{2/5}$ scaling; Alpert $16.9,5.38,0.96,
0.197$; point-source $\chi_r/(4\pi R^2)$; Mulholland $K_m\approx8.7$ m²/g; flicker $f\approx1.5/\sqrt D$;
t² $\alpha=\{0.00293,0.01172,0.0469,0.1876\}$. This is a consistency check, NOT primary-source verification
of the exact equation numbers — the [coeff-verify] + expert-review flag stands (the classic correlations
were not available as fetched PDFs on arXiv this session; web_search had no API key).
