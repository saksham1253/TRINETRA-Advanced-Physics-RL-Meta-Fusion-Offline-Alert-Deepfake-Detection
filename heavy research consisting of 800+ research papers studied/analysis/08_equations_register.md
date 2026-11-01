# EQUATIONS REGISTER (MASTER_PROMPT §0.8)
# Each entry: statement (LaTeX text), symbol table w/ units, CLASS A/B/C, assumptions &
# regime of validity, source id + eqn number, re-derived on paper? (y/n), planned
# verification checks. Full derivations happen in P7 (physics on paper). This is the seed.
#
# CLASS labels (travel everywhere): A = established/derivable from first principles;
# B = empirical/semi-empirical fit with regime limits; C = heuristic/assumed.

## Seed entries (from pre-existing analysis; CLASS pending P7 re-derivation)

### E-01 Infinite-slope factor of safety  [CLASS A]
FS = (c' + (gamma - m*gamma_w) * z * cos^2(beta) * tan(phi')) / (gamma * z * sin(beta) * cos(beta))
Symbols: c' effective cohesion [Pa]; gamma soil unit weight [N/m^3]; gamma_w water unit
weight [N/m^3]; m wetness ratio [-]; z depth [m]; beta slope angle [rad]; phi' effective
friction angle [rad]. Regime: planar failure, slope-parallel seepage, z << slope length.
Source: standard geotech (confirm primary in P7). Re-derived: pending. Checks: dimensional,
limit beta->0 => FS->inf, m=1 saturated.

### E-02 Iverson (2000) transient pressure head  [CLASS A/B]
Slope enters ONLY via D1 = D0 / cos^2(delta) (hydraulic diffusivity along bedding).
Flag: report's spurious cos^2(beta)/cos(beta) factor = Bug #3 (verify in P7).
Source: Iverson 2000 WRR. Re-derived: pending.

### E-03 Lu & Likos suction stress  [CLASS A]
sigma_s = - S_e * psi   (SIGN: negative; report sign error = Bug #2)
Symbols: S_e effective saturation [-]; psi matric suction [Pa]. Source: Lu & Likos.

### E-04 Fukuzono/Voight inverse-velocity  [CLASS B]
1/v = A*(alpha - 1)*(t_f - t), with alpha ~ 2 (report's 1.5-2.2 range = Bug #4 to check).
Use: time-to-failure t_f extrapolation. Source: Fukuzono 1985 / Voight 1988.

### E-05 Caine intensity-duration threshold  [CLASS B]
I = a * D^(-b). Report constants to VERIFY (Bug #15):
Caine 14.82*D^-0.39; Dahal-Hasegawa 73.9*D^-0.79; Garhwal 1.82*D^-0.23. CLASS B (empirical,
region-specific; 2608.12422 argues threshold is a DISTRIBUTION, not a constant).

### E-06 Bayes alarm threshold  [CLASS A]
p* = C_FA / (C_FA + C_miss) = 5 / (5 + 100) = 0.0476.
Report threshold inconsistency = Bug #1. Source: cost-loss decision theory.
NEW (2026-10-06, QUOTA 2601.05921): this p* is the decision threshold of the SAME cost-loss
model whose VERIFICATION metric is the Value Score (E-07). Keep threshold and evaluation
metric from one coherent cost-loss model so the alarm cutoff and the score we optimise agree.

### E-07 Cost-loss Value Score (EWS verification metric)  [CLASS A]
V = (E_climatology - E_forecast) / (E_climatology - E_perfect)
where E_* is the expected cost-loss expense of acting on a forecast given cost C (of acting)
and loss L (of an un-mitigated event), evaluated over the forecast distribution. V = 1 perfect,
V = 0 no value over climatology, V < 0 worse than always using the climatological base rate.
Symbols: C protective-action cost; L event loss; base rate s = P(event). The optimal action
rule is "act iff p > C/L", i.e. the same cost-loss cutoff as E-06 (p* = C_FA/(C_FA+C_miss)).
Regime: binary act/no-act decisions, user-specific C/L ratio; value is DECISION-maker-relative.
Source: Richardson 2000 / Wilks; meteorological lineage Epstein 1969 (2601.05921 QUOTA#15).
Re-derived: pending P7. Use: PRIMARY EWS evaluation metric for TRINETRA — report V across a
RANGE of C/L (cost-loss) ratios, NOT a single AUC; ranking models by log-score ≠ ranking by
decision value (2601.05921). Pair with per-base-rate protocol (FM-21) so metrics are never
compared across differing imbalance ratios.

(Further: Scheidegger runout, Froehlich, SCS-CN, Manning, Richards — added in P7.)

---

## P7 additions — FIRE/SMOKE/SENSOR physics (WS1a) [added 2026-10-09]
SCOPE NOTE: MASTER_PROMPT Phase P7 is FIRE physics (plume/flame/smoke/spread/sensor). The GEO-HAZARD seed
equations above (E-01 infinite-slope, E-02 Iverson, and the planned Scheidegger/Froehlich/SCS-CN/Manning/
Richards) belong to the geo-hazard physics workstream and REMAIN PENDING — they are NOT P7's fire scope.
Full statements, symbols, derivation outlines, validity, assumptions, and KNOWN WEAKNESSES for the fire set
live in ws1_physics/established_formula_inventory.md; derivations in ws1_physics/derivations/. Summary index:

### EF-01 Heskestad mean flame height [CLASS A] — L = 0.235 Q^(2/5) − 1.02 D  (Heskestad 1983) [coeff-verify]; re-derived outline y.
### EF-02 t² fire growth / HRR [CLASS B] — Q = α(t−t0)²; α∈{0.00293,0.01172,0.0469,0.1876} kW/s² (NFPA 72) [coeff-verify]; re-derived outline y.
### EF-03 Heskestad plume centerline [CLASS A] — ΔT0 = 9.1(T∞/g cp²ρ∞²)^(1/3) Qc^(2/3)(z−z0)^(−5/3); u0 = 3.4(g/cpρ∞T∞)^(1/3) Qc^(1/3)(z−z0)^(−1/3) (Heskestad) [coeff-verify]; re-derived outline y.
### EF-04 McCaffrey 3-regime [CLASS B] — power laws in z/Q^(2/5) (McCaffrey 1979 NBS) [coeff-verify]; outline y.
### EF-05 Alpert ceiling jet [CLASS A/B] — ΔTmax = 16.9 Q^(2/3)/H^(5/3) (r/H≤0.18) else 5.38(Q/r)^(2/3)/H; Umax = 0.96(Q/H)^(1/3) (r/H≤0.15) else 0.197 Q^(1/3)H^(1/2)/r^(5/6) (Alpert 1972) [coeff-verify]; outline y.
### EF-06 Point-source radiation [CLASS A] — q″ = χr Q/(4πR²), χr≈0.15–0.40 (Modak/SFPE); solid-flame q″=E·F·τatm; outline y.
### EF-07 Beer–Lambert smoke extinction [CLASS A] — I/I0 = exp(−σL), σ = Km·m, Km≈8.7 m²/g flaming (Mulholland); OD=(1/L)log10(I0/I); V=C/σ (Jin, 2404.11439) [coeff-verify]; outline y.
### EF-08 Flame puffing frequency [CLASS B] — f ≈ 1.5 D^(−1/2) Hz, St = f√(D/g) const (Cetegen&Ahmed 1993) [coeff-verify]; outline y.
### EF-09 Thermal-camera radiometry [CLASS A] — Lmeas = ε τatm Lbb(T) + (1−ε)τatm Lbb(Tsurr) + (1−τatm)Lbb(Tatm); E = ε σ T⁴; outline y.
### EF-10 Detector RTI / rate-of-rise [CLASS A] — dTe/dt = (√u/RTI)(Tg−Te), RTI = τ√u (Heskestad&Bill); outline y.
### EF-11 Rothermel surface spread [CLASS B] — R = IR ξ(1+φw+φs)/(ρb ε Qig) (Rothermel 1972); outline y.
### EF-12 Zukoski entrainment [CLASS A] — ṁ ∝ Qc^(1/3)(z−z0)^(5/3) (Zukoski); outline y.

### Layer-2 (CLASS B, full derivations, reduce-to-parent, independently rechecked 2026-10-09):
- B-06 sensor-response-corrected signal (parent EF-05/EF-10): Ts = (1/τ)e^(−t/τ) ⊛ Tg(t−td), td ∝ r^(11/6)Q^(−1/3)H^(−1/2); → parent as τ,td,noise→0. [derivations/B-06…]
- B-05 aliasing-aware flicker (parent EF-08): fobs = |f0 − fs·round(f0/fs)|; → parent as fs>2f0. [derivations/B-05…]
- B-01 camera apparent flame height (parent EF-01/EF-07): hpx = (f/R)[L cosθ − Δsmoke(σ,ℓ)]; → parent as σ,θ→0. [derivations/B-01…]
- B-02 dimensionless plume prior (parent EF-03): ΔT0 = 9.1(…)^(1/3) ζ^(−5/3), ζ=(z−z0)/Qc^(2/5) (Qc exponent cancels); → parent as priors→δ, noise→0. [derivations/B-02…]
All fire-set constants [coeff-verify] vs primary sources; expert review required before external use (Rule 16 / §P7 3(e)).

---

## P7G additions — GEO-HAZARD physics (WS1b) [added 2026-10-09]
Resolves the "pending" geo-hazard seed above (E-01 infinite-slope, E-02 Iverson, and the planned Scheidegger/
Froehlich/SCS-CN/Manning/Richards): all are now inventoried + derived in ws1b_geohazard/. Fire (P7) and
geo-hazard (P7G) sets are kept SEPARATE. Full statements/validity/weaknesses in
ws1b_geohazard/established_formula_inventory.md; derivations in ws1b_geohazard/derivations/. Index:

### GH-01 Infinite-slope FS [CLASS A] — FS=[c'+(γ−mγ_w)z cos²β tanφ']/[γ z sinβ cosβ] (geotech) [coeff-verify] — supersedes seed E-01.
### GH-02 Iverson transient head [CLASS A/B] — ψ(Z,t) via linearized Richards diffusion, D₁=D₀/cos²δ (Iverson 2000) [coeff-verify] — supersedes seed E-02.
### GH-03 Richards eqn [CLASS A] — ∂θ/∂t=∂/∂z[K(ψ)(∂ψ/∂z+1)], vanGenuchten θ(ψ) (Richards 1931) [coeff-verify].
### GH-04 Green–Ampt [CLASS A/B] — f=K_s[1+(Δθ ψ_f)/F] (Green&Ampt 1911) [coeff-verify].
### GH-05 Rainfall ID threshold [CLASS B] — I=α D^(−β) (Caine 1980 + regional) [coeff-verify].
### GH-06 Scheidegger reach angle [CLASS B] — H/L=f·V^(−g), log(H/L)=a+b log V (Scheidegger 1973; Corominas 1996) [coeff-verify].
### GH-07 Voellmy–Salm rheology [CLASS A/B] — τ=μσ+ρg v²/ξ (Voellmy 1955; Salm 1993) [coeff-verify].
### GH-08 SCS Curve-Number [CLASS B] — Q=(P−0.2S)²/(P+0.8S), S=25400/CN−254 (USDA-SCS) [coeff-verify].
### GH-09 Manning [CLASS A/B] — v=(1/n)R_h^(2/3)S_f^(1/2) (Manning 1891) [coeff-verify].
### GH-10 Saint-Venant [CLASS A] — ∂A/∂t+∂Q/∂x=q; ∂Q/∂t+∂(Q²/A)/∂x+gA(∂h/∂x−S₀+S_f)=0 (Saint-Venant 1871).
### GH-11 Muskingum [CLASS B] — O₂=C₀I₂+C₁I₁+C₂O₁ (McCarthy 1938) [coeff-verify].
### GH-12 Stage–discharge rating [CLASS B] — Q=a(h−h₀)^b (hydrometry) [coeff-verify].
### GH-13 GLOF breach peak-Q [CLASS B] — Q_p=c V_w^p h_b^q (Froehlich 1995) [coeff-verify] — supersedes seed "Froehlich".

### Layer-2 (CLASS B, full derivations, reduce-to-parent, INDEPENDENTLY rechecked 2026-10-09, 0 errors):
- GB-01 probabilistic infinite-slope (parent GH-01): P_f=P(FS<1)≈Φ(−β_rel); → GH-01 as input variances→0.
- GB-02 sensor-corrected pore-pressure (parent GH-02): ψ_m=(1/T_lag)e^(−t/T_lag)⊛ψ; → GH-02 as T_lag,noise→0.
- GB-03 antecedent-aware prob. rainfall threshold (parent GH-05): P=σ_logit(w₀+w₁ x), x=log[I/(α(S)D^(−β))]; → GH-05 as hard step. [CORE EWS]
- GB-04 AMC-corrected SCS-CN (parent GH-08): Q=(P−λS_ret(S))²/(P+(1−λ)S_ret(S)); → GH-08 at λ=0.2,r=1.
- GB-05 hysteresis rating (parent GH-12): Q=Q_s(h)√(1+(1/(S₀c))dh/dt) (Jones); → GH-12 as dh/dt→0.
Class C (doc-only simulators): GC-01 runout (GH-06/07), GC-02 routing (GH-10/11), GC-03 GLOF chain (GH-13).
All geo-hazard constants [coeff-verify] vs primary sources; geotech+hydrology expert review required (Rule 16).
