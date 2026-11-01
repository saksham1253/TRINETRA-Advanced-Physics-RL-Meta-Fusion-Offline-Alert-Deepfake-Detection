# 05b — MODELS (numpy core): physics models + fusion / decision / shield / conformal

> Companion to `05_MODELS.md` (index, opening table, closing meta-fusion). **Everything in this file RUNS**:
> it is the pure-numpy core verified by `python run_tests.py` → **128 tests OK** and `python
> scripts/ci_gates.py` → **ALL 6 CI GATES PASSED** `[CONFIRMED]` (`_CANON.md §2`). These are **not** trained
> models (closed-form physics + transparent fusion math), so "trained? = n/a" and "our skill = not measured"
> (no dataset, no eval gate run — R16). Equations are taken from the code and cross-checked against
> `analysis/08_equations_register.md` (read for this chapter). Classic physics references (Heskestad, Byram,
> Iverson, Caine, Fukuzono) are journal papers with **no arXiv ID in this repo's ledger**; EO/ML/conformal
> anchors that DO carry IDs are labeled.

Pipeline reminder: these numpy pieces produce `ExpertOutput`s and feed the **single decision function**
`decide()` — `level = max(conformal_level(risk, p*), shield_floor)`, `p* = 0.0476` (`_CANON.md §4`).

---

## 9. Infinite-slope Factor of Safety (Class A) — `ws1b_geophys/fs.py`

### (1) Role / I/O
The hard deterministic landslide-stability gate. FS<1 ⇒ unstable; it drives the shield floor and the geo
gate's `p_fs`. **In:** `(c', φ', γ, z, β, u_w, σ_s)`. **Out:** FS (dimensionless, array-broadcastable).

### (2) Rationale + alternatives
- **Infinite-slope (chosen):** standard first-line screen for shallow translational slides; cheap, offline,
  interpretable. Golden-tested monotonicities make it a safe hard gate.
- **Limit-equilibrium (Bishop/Janbu) / 2-D FEM:** rejected for the edge path — need geometry/mesh data
  unavailable at pilot and are not offline-cheap. (Runout/2-D kept as Class-C doc-only simulators,
  `08_…register` GC-01.)
- **Probabilistic FS `P(FS<1)`:** a documented improvement (GB-01), not yet implemented. Our comparative
  result: **not measured** (deterministic form only).

### (3) Full formulation (verbatim from code / E-01, GH-01)
```
FS = ( c' + σ'_n · tan φ' ) / ( γ · z · sin β · cos β )
σ'_n = γ · z · cos²β − u_w + σ_s
u_w  = γ_w · ψ,   γ_w = 9.81 kN/m³   (pore_pressure_from_head)
```
- **Assumptions / regime (E-01):** planar (translational) failure parallel to the slope; slope-parallel
  seepage; `z ≪ slope length`; cohesive-frictional Mohr–Coulomb strength.
- **Constitutive relation:** Mohr–Coulomb `τ_f = c' + σ'_n tan φ'`; effective stress with suction `σ_s ≥ 0`
  that **vanishes at saturation** (`S_e→1 ⇒ σ_s→0`), recovering the classic saturated form.
- **Boundary/initial conditions:** none (algebraic, pointwise in depth `z`).
- **Limiting cases (code invariants / E-01 checks):** FS strictly **increasing in suction σ_s**; at `σ_s=0`
  equals the saturated form (`factor_of_safety_saturated`); FS **decreases** as `u_w` rises; `β→0 ⇒
  denominator→0 ⇒ FS→∞` (flat ground never fails) — guarded by the `denom>0` check that raises on
  `γ,z,β ≤ 0`.
- **Dimensional check:** numerator `[kPa] = kPa + kPa·(—)`; denominator `[kN/m³·m·(—)] = kPa`; ratio
  dimensionless. ✔ (consistent kPa/kN·m units).

### (4) Diagram + "shapes"
```
(c',φ',γ,z,β,u_w,σ_s) → σ'_n = γz cos²β − u_w + σ_s → FS = (c' + σ'_n tanφ')/(γz sinβ cosβ)
```
Fully array-broadcastable (numpy); no tensors.

### (5) I/O spec, normalization, units
`c' [kPa], φ' [deg], γ [kN/m³], z [m], β [deg], u_w [kPa], σ_s [kPa]`. No normalization. FS unitless.

### (6) "Training recipe"
n/a — closed form. Validated by `tests/physics_golden` (monotonicities, saturated limit). `[CONFIRMED]`.

### (7) Hyperparameters
None (parameters are physical site inputs). The geo gate maps FS→prob with `k_fs=4.0` (see §13 gate).

### (8) Code (repo; RUNS)
```python
def factor_of_safety(c_prime, phi_prime_deg, gamma, z, beta_deg, u_w=0.0, sigma_s=0.0):
    beta = np.radians(beta_deg); phi = np.radians(phi_prime_deg)
    denom = gamma * z * np.sin(beta) * np.cos(beta)
    if np.any(denom <= 0): raise ValueError("driving stress must be positive (check gamma,z,beta>0)")
    sigma_n_eff = gamma * z * np.cos(beta)**2 - u_w + sigma_s
    return (c_prime + sigma_n_eff * np.tan(phi)) / denom
```

### (9) Uncertainty & calibration
Deterministic (no distribution). Uncertainty is injected downstream by the gate's consistency/uncertainty and
by Fukuzono's interval. The differentiable twin `losses.factor_of_safety_torch` lets the PINN use `FS<1` as a
label-free penalty (05a §1). `[CONFIRMED]`.

### (10) Failure modes
Invalid for deep-seated/rotational failures, fractured rock, 2-D/3-D flow. Mitigation: it is a *screen* +
shield trigger, corroborated by Iverson/Caine/Fukuzono; `σ_s` sign/saturation handled explicitly (the suction
sign was Bug #2 in `08_…register` E-03 — fixed here). → chapter 13.

### (11) Ablations / results
Golden tests pass `[CONFIRMED]`. No skill number (deterministic; not benchmarked) — **not measured**.

### (12) Improvement ideas
Probabilistic `P(FS<1)=Φ(−β_rel)` (GB-01) `[HYPOTHESIS]`; spatially-variable soil params `[HYPOTHESIS]`.

### (13) Reference IDs
Standard infinite-slope geotech; Lu & Likos (suction stress, E-03). → chapter 19.

---

## 10. Iverson (2000) transient pressure head (Class A) — `ws1b_geophys/iverson.py`

### (1) Role / I/O
Transient pore-pressure head response to rainfall infiltration, producing `ψ` that becomes `u_w` for FS.
**In:** `(Z, t, D0, K_z, I_z, β)` [+ a piecewise rainfall history for the multipulse variant]. **Out:** ψ(Z,t)
[m].

### (2) Rationale + alternatives
- **Linearized Iverson (chosen):** closed-form, offline, captures rainfall-driven pore-pressure rise with a
  single diffusivity; the right fidelity for a cheap node.
- **Full Richards equation (GH-03):** rejected for the edge path (non-linear PDE solve; needs van-Genuchten
  params) — documented as the parent.
- **Green–Ampt (GH-04):** alternative infiltration model; not implemented here. Our comparison: **not
  measured**.

### (3) Full formulation (verbatim from code / E-02, GH-02)
```
D1 = D0 / cos²β                               # the ONLY place slope enters (bug-guard)
R(Z,t) = sqrt(4 D1 t) · ierfc( Z / sqrt(4 D1 t) ),   ierfc(x)=exp(−x²)/√π − x·erfc(x),  ierfc(0)=1/√π
ψ_transient(Z,t) = (I_z / K_z) · R(Z,t)       # for t>0, else 0
ψ_total = ψ_steady + ψ_transient
```
Multipulse (linear superposition over a piecewise-constant rainfall history, `transient_head_multipulse`):
```
ψ(Z,t) = Σ_k ((I_k − I_{k−1}) / K_z) · R(Z, t − t_k) · H(t − t_k),   I_{−1}=0
```
A finite pulse `I` over `[0,T]` reduces to two steps → the classic recovery `ψ=(I/K_z)[R(Z,t)−R(Z,t−T)]`.
- **Assumptions / regime (E-02):** 1-D vertical, linearized Richards diffusion; `I_z ≤ K_z`; response linear
  in surface flux (enables superposition).
- **Constitutive relation:** diffusion of pressure head with constant diffusivity `D1`.
- **Boundary/initial conditions:** surface flux `I_z` at `Z=0` over the wetting period; `ψ=0` for `t≤0` (code
  sets `R=0` for `t≤0`, NaN-guarded).
- **Limiting cases:** `t→0⁺ ⇒ R→0 ⇒ ψ→ψ_steady`; `β→0 ⇒ D1→D0`; after rain stops, superposition gives the
  recovery term.
- **Dimensional check:** `sqrt(4 D1 t)` with `D1 [m²/s], t [s]` → `[m]`; `ierfc` dimensionless; `R [m]`;
  `(I_z/K_z)` dimensionless (both flux/velocity) ⇒ ψ [m]. ✔
- **Bug-guard (CRITICAL, `_CANON.md §4`, E-02 Bug #3):** there is **NO extra `cos²β/cosβ` multiplier** on the
  transient term; slope enters only via `D1`. The slope-free `_transient_core`/`_response_R` enforce this.

### (4) Diagram + shapes
```
(D0,β) → D1 → R(Z,t)=√(4D1t)·ierfc(Z/√(4D1t)) → ψ=(I_z/K_z)·R   (+ψ_steady)
multipulse: Σ_k ΔI_k/K_z · R(Z, t−t_k)·H(t−t_k)
```
numpy, broadcastable over `Z,t`.

### (5) I/O spec, normalization, units
`Z [m], t [s] (consistent with D0), D0 [m²/s], K_z [m/s], I_z [m/s], β [deg]`. ψ in [m] → `u_w=γ_w·ψ [kPa]`.
No normalization.

### (6) "Training recipe"
n/a. Validated by golden tests (bug-guard, multipulse superposition, finite-pulse recovery). `[CONFIRMED]`.

### (7) Hyperparameters
None beyond physical inputs. `erfc` from stdlib `math` (scipy unavailable, `_CANON §2`).

### (8) Code (repo; RUNS)
```python
def diffusivity_D1(D0, beta_deg): return D0 / (math.cos(math.radians(beta_deg))**2)
def transient_head(Z, t, D0, K_z, I_z, beta_deg):
    D1 = diffusivity_D1(D0, beta_deg); return _transient_core(Z, t, D1, I_z, K_z)
# multipulse: psi += (dI/K_z) * _response_R(Z, t_eval - tk, D1) for each step
```

### (9) Uncertainty & calibration
Deterministic; uncertainty enters via the gate. `[CONFIRMED]`.

### (10) Failure modes
Invalid when infiltration exceeds `K_z` (ponding), strongly non-linear soils, macropore flow. Mitigation:
Class-A fallback; the sensor-corrected pore-pressure extension GB-02 is a documented upgrade. → chapter 13.

### (11) Ablations / results
Golden/multipulse tests pass `[CONFIRMED]`. No skill number — **not measured**.

### (12) Improvement ideas
Sensor-lag-corrected pore pressure (GB-02) `[HYPOTHESIS]`; data assimilation of soil-moisture (`_CANON §3`
A4) `[HYPOTHESIS]`.

### (13) Reference IDs
Iverson 2000 (WRR); Baum/Savage (TRIGRS lineage); Richards 1931 (GH-03). → chapter 19.

---

## 11. Fukuzono inverse-velocity failure-time (Class A/B) — `ws1b_geophys/fukuzono.py`

### (1) Role / I/O
Forecast of creep failure time `t_f` from surface-displacement velocities, **with a prediction interval**.
**In:** `(times, velocities, α=2 [, weights, recency_halflife, z])`. **Out:** `FukuzonoFit(t_failure, α, slope,
r2, regime_note, t_failure_low/high, se_t_failure)`.

### (2) Rationale + alternatives
- **Inverse-velocity (chosen):** operational standard for imminent-failure forecasting from monitoring.
- **Bare OLS intercept:** rejected — gives a false point certainty; code adds **recency-weighted WLS** +
  **delta-method prediction interval**.
- **α≠2 regimes:** supported via `v^(1−α)` linearization (regime flag) rather than assuming α=2. Our forecast
  accuracy: **not measured**.

### (3) Full formulation (verbatim from code / E-04)
```
1/v = A·(α−1)·(t_f − t)        # α=2 ⇒ 1/v linear in t ; t_f = x-intercept
linearized y = 1/v (α=2) or v^(1−α) (α≠2)
WLS fit y ~ m·t + b with weights w (recency: w = 0.5^((t_max−t)/halflife))
t_f = −b/m
delta method: g = [−t_f/m, −1/m];  Var(t_f) = gᵀ Cov([m,b]) g;  CI = t_f ± z·√Var
r2 = weighted 1 − SS_res/SS_tot
```
- **Assumptions / regime (E-04):** accelerating tertiary creep; α≈2 (code default; the report's 1.5–2.2 range
  was Bug #4 to check); velocities strictly positive (raises otherwise).
- **Limiting cases:** `|m|<1e-12 ⇒ t_f=inf` (no acceleration ⇒ no finite failure time); recency halflife
  `≤0`/None ⇒ uniform weights.
- **Dimensional check:** `t_f=−b/m` has units of `t`; CI in the same units. ✔

### (4) Diagram + shapes
```
(times, velocities) → y=1/v → WLS(recency w) → (m,b,Cov) → t_f=−b/m, se via delta → [t_f_low, t_f_high]
```

### (5) I/O spec, units
`times` and `velocities` in consistent units; `t_f` and its CI in the same time units. `z=1.96` ≈ 95%.

### (6) "Training recipe"
n/a (a per-event regression). Validated by CI/delta-method golden tests. `[CONFIRMED]`.

### (7) Hyperparameters
| HP | Value | Rationale | Sensitivity |
|----|-------|-----------|-------------|
| α | 2.0 | 1/v linear | regime flag if ≠2 |
| recency_halflife | None (uniform) default | up-weight recent creep | affects t_f under noise |
| z | 1.96 | ~95% interval | widens/narrows CI |

### (8) Code (repo; RUNS)
```python
t_f = -b/m
g = np.array([-t_f/m, -1.0/m]); var_tf = g @ cov @ g; se = sqrt(max(var_tf,0))
FukuzonoFit(t_failure=t_f, ..., t_failure_low=t_f - z*se, t_failure_high=t_f + z*se, se_t_failure=se)
```
Gate use: `p_fk = clip(1 − lead/48, 0, 1) · clip(r2, 0, 1)` where `lead = t_f − now_hours` (`gate.py`).

### (9) Uncertainty & calibration
First-class: delta-method prediction interval + weighted r² as a fit-quality gate. The gate multiplies the
Fukuzono contribution by `r2` (poor fit ⇒ little weight). `[CONFIRMED]`.

### (10) Failure modes
Non-monotone/noisy creep, regime change, too few points; `m≈0` ⇒ `t_f=inf`. Mitigation: recency weights,
interval (never a point), r²-gated contribution. → chapter 13.

### (11) Ablations / results
CI tests pass `[CONFIRMED]`. No forecast-accuracy number — **not measured**.

### (12) Improvement ideas
Bayesian inverse-velocity with explicit noise model `[HYPOTHESIS]`; automatic regime/α selection
`[HYPOTHESIS]`.

### (13) Reference IDs
Fukuzono 1985; Voight 1988. → chapter 19.

---

## 12. Caine intensity–duration threshold (Class A/B empirical) — `ws1b_geophys/caine.py`

### (1) Role / I/O
Rainfall I–D landslide-triggering threshold → a soft exceedance signal for the geo gate. **In:** `(I [mm/h],
D [h], a, b)`. **Out:** `(exceeded bool, ratio = I/I_threshold)`.

### (2) Rationale + alternatives
- **Power-law I–D (chosen):** the canonical regional triggering screen; cheap and offline.
- **Single borrowed global constant:** explicitly rejected as live truth — coefficients **must be locally
  re-fit** (config `geophys.caine_a/caine_b`), honesty note in code (Bug #15, E-05).
- **Threshold-as-distribution:** a documented improvement (2608.12422 `[ABS]` argues the threshold is a
  distribution, not a constant). Our regional skill: **not measured**.

### (3) Full formulation (verbatim from code / E-05, GH-05)
```
I_threshold(D) = a · D^(−b)        # Caine 1980; a,b region-specific
exceeded = (I / I_threshold) > 1 ;  ratio = I / I_threshold
```
- **Assumptions / regime:** empirical, region- and duration-specific; `D>0` (else NaN threshold, fail-safe).
- **Defaults (CODE_INVENTORY):** `a=14, b=0.39` (close to Caine's 14.82·D^−0.39; `08_…register` lists regional
  variants Dahal-Hasegawa 73.9·D^−0.79, Garhwal 1.82·D^−0.23). These are **planning defaults, not validated
  for the pilot region**.
- **Dimensional check:** `I [mm/h] = a·D^−b` requires `a` to carry `mm·h^(b−1)`; code treats `a,b` as fitted
  constants (dimension absorbed by the fit). ✔ (as an empirical fit).

### (4) Diagram
```
(I, D, a, b) → thr = a·D^−b → ratio = I/thr → exceeded = ratio>1
gate: p_caine = clip(ratio − 0.5, 0, 1)
```

### (5) I/O spec, units
`I [mm/h], D [h]`; `a,b` fitted. Output ratio dimensionless.

### (6) "Training recipe"
Coefficients `a,b` are **fit locally** from regional rainfall/landslide records (not done here — no data). The
formula itself is closed-form. `[CONFIRMED]` tests pass on the formula.

### (7) Hyperparameters
| HP | Value | Rationale | Sensitivity |
|----|-------|-----------|-------------|
| a | 14.0 (default) | planning constant | must re-fit per region |
| b | 0.39 (default) | planning constant | must re-fit per region |

### (8) Code (repo; RUNS)
```python
def caine_threshold(D_hours, a, b):
    D = np.asarray(D_hours, float); return a * np.power(np.where(D>0, D, np.nan), -b)
def caine_exceedance(I, D, a, b):
    thr = caine_threshold(D, a, b); ratio = np.asarray(I,float)/thr; return ratio>1.0, ratio
```

### (9) Uncertainty & calibration
No distribution in code (point threshold); honesty note mandates local re-fit, and the threshold-as-
distribution upgrade is documented. Enters the gate as a *soft* `p_caine`. `[CONFIRMED]`.

### (10) Failure modes
Borrowed constants mis-fire out of region; antecedent moisture not captured. Mitigation: config-driven re-fit,
antecedent-aware threshold GB-03 documented, soft contribution only. → chapter 13.

### (11) Ablations / results
Formula tests pass `[CONFIRMED]`. No regional validation — **not measured**.

### (12) Improvement ideas
Antecedent-moisture-aware probabilistic threshold (GB-03, "CORE EWS") `[HYPOTHESIS]`; threshold distribution
with coverage (2608.12422 `[ABS]`) `[HYPOTHESIS]`.

### (13) Reference IDs
Caine 1980; 2608.12422 `[ABS]` (threshold-as-distribution). → chapter 19.

---

## 13. Geo gate — noisy-OR combiner → one geo ExpertOutput (Class A/B) — `ws1b_geophys/gate.py`

### (1) Role / I/O
Combines FS / Iverson / Caine / Fukuzono into one advisory `ExpertOutput(geo_phys)` with a physics-consistency.
**In:** `GeoInputs` (slope/soil + optional Iverson infiltration + optional I–D + optional Fukuzono fit).
**Out:** `GeoResult(FS, caine_ratio, t_failure, p_phys, expert)`.

### (2) Rationale + alternatives
- **Noisy-OR (chosen):** monotone, "never under-warns," transparent (no learned weights at the gate; learning
  lives in ws5).
- **Weighted average / learned fusion at the gate:** deliberately rejected here to keep the gate auditable.
Our comparison: **not measured**.

### (3) Formulation (verbatim from code)
```
u_w  = pore_pressure_from_head(pressure_head(...))  if infiltration given, else supplied u_w
FS   = factor_of_safety(...);  p_fs = sigmoid(k_fs·(1−FS)),  k_fs=4.0     # FS=1→0.5, FS<1→>0.5
p_caine = clip(caine_ratio − 0.5, 0, 1)   (if I,D given)
p_fk    = clip(1 − lead/48, 0, 1)·clip(r2,0,1)  (if Fukuzono fit & lead>0)
p_phys  = 1 − Π(1 − p_i)                     # noisy-OR over [p_fs, p_caine, p_fk]
c_consistency = clip(1 − std(active_components), 0, 1)   (if ≥2 active, else 1)
expert = ExpertOutput(p=p_phys, u=clip(0.5·(1−c)+0.1,0,1), c=c_consistency, r=1.0, cls=A)
```
- **Limiting cases:** no sub-signals active ⇒ `p_phys=p_fs` only; single active ⇒ consistency 1.0.
- **Dimensional check:** all `p_i∈[0,1]`; noisy-OR stays in [0,1]. ✔

### (4) Diagram
```
FS→p_fs ┐
Caine→p_caine ├─ noisy-OR → p_phys ─┐→ ExpertOutput(geo_phys, Class A, u,c,r)
Fukuzono→p_fk ┘        consistency ──┘
```

### (5)–(8) I/O, recipe, HPs, code
Inputs physical (see §9–12). `k_fs=4.0` is the only tuning constant. n/a training. Runs; tested. `[CONFIRMED]`.

### (9) Uncertainty & calibration
`u` derived from inter-signal consistency; `c` feeds NF-1 downstream. No post-hoc calibrator at the gate.
`[CONFIRMED]`.

### (10) Failure modes
Over-warning if a sub-signal is mis-parameterized (noisy-OR never lowers); mitigated by consistency-driven `u`
and the conservative design intent. → chapter 13.

### (11)–(13) Results / ideas / refs
Tests pass `[CONFIRMED]`; no skill number (**not measured**). Ideas: calibrate `k_fs` and the lead-time
horizon per region `[HYPOTHESIS]`. Refs: as §9–12.

---

## 14–17. Fire physics blocks (Class A) — `ws1a_firephys/established_ef.py`

### (1) Roles / I/O
A computable subset of the EF inventory used as **features / consistency checks** (never a trigger):
- **Heskestad flame height** `L = 0.235·Q̇^(2/5) − 1.02·D` [m] (EF-01).
- **Strouhal puffing frequency** `f = 1.5·D^(−1/2)` [Hz] (EF-08/EF-16).
- **Heskestad plume centerline ΔT₀** `= 9.1·(T∞/(g·c_p²·ρ∞²))^(1/3)·Q̇_c^(2/3)·(z−z0)^(−5/3)` [K] (EF-03).
- **Byram convection number** `N_c = 2·g·Q̇_c / (ρ·c_p·T∞·U³)` (EF-13 regime check).
- **Gray-body radiance** `E = ε·σ·T⁴` and its inverse `T = (E/(εσ))^(1/4)` (EF-14), σ=5.670374419e-8.
- **Beer–Lambert transmittance** `τ = exp(−(κ+σ)·L)` (EF-07/14).

### (2) Rationale + alternatives
- **Heskestad vs McCaffrey plume (EF-03 vs EF-04):** `model_set_decision.md` keeps **both** parents admitted;
  a later ablation (§P7 task 6) decides which fits the regime — "keeping both is cheap and informative." Only
  Heskestad centerline is implemented here. Our fit comparison: **not measured**.
- **Byram number (chosen regime gate):** used to reject wind-dominated/non-fire regimes rather than trusting
  appearance alone.
- These are **Class A** physics used as plausibility/consistency, not detectors.

### (3) Full formulation (verbatim; assumptions / limits / dimensional checks)
- **Heskestad L:** valid for buoyant turbulent diffusion flames; `Q̇ [kW], D [m]`; `[coeff-verify]`
  (0.235, 1.02). Limiting: large `D` can give `L<0` (flame below rim) — a known regime limit, not guarded in
  code. Dimensional: empirical constants carry units (SI-inconsistent literals, flagged).
- **Strouhal f:** `St = f·√(D/g)` ~ const (Cetegen & Ahmed 1993); here `f=1.5/√D`. Dimensional: `1.5` carries
  `m^½·Hz` (empirical).
- **Plume ΔT₀:** far-field (`z>flame`); `g=9.81, c_p=1.0, ρ=1.2` hard-coded (c_p in kJ/kg·K units implied,
  `[coeff-verify]`); `dz=max(z−z0,1e-6)` guards the singularity at the virtual origin.
- **Byram N_c:** `N_c>~2` plume-dominated, `<~1` wind-dominated; `U` floored at 1e-3; `denom≤0 ⇒ inf`.
  Dimensionless. ✔
- **Gray-body:** Stefan–Boltzmann; `E [W/m²]`, `T [K]`; invertible; `r=max(radiance,0)` guard.
- **Beer–Lambert:** `τ∈(0,1]`; `κσ·L` dimensionless. ✔

### (4) Diagram
```
Q̇,D → L (Heskestad);  D → f (Strouhal);  Q̇_c,z → ΔT₀ (plume);  Q̇_c,U → N_c (Byram regime)
T → E (gray-body) ↔ T;  (κ+σ),L → τ (Beer–Lambert)
```

### (5)–(8) I/O, recipe, HPs, code
Units as above; no normalization; closed-form; `[coeff-verify]` constants must be confirmed vs SFPE/Heskestad/
McCaffrey before any live output (code + `model_set_decision §expert-review`). Runs; tested. `[CONFIRMED]`.

### (9) Uncertainty & calibration
Deterministic; the fire gate converts Byram `N_c` into a consistency multiplier and (optional, Class-C) ND
terms add uncertainty. `[CONFIRMED]`.

### (10) Failure modes
Unknown `Q̇, D, Q̇_c` in the field (the exact gap B-01/B-02 target); SI-inconsistent empirical constants;
regime violations (large `D`). Mitigation: used only as consistency/feature; `[coeff-verify]` + expert review.
→ chapter 13.

### (11)–(13) Results / ideas / refs
Golden tests pass `[CONFIRMED]`; no measured fire detection skill (**not measured**). Ideas: camera-apparent
flame height through smoke (B-01), dimensionless plume prior (B-02), aliasing-aware flicker (B-05)
`[HYPOTHESIS]`. Refs: Heskestad 1983 (EF-01/03), Cetegen & Ahmed 1993 (EF-08), Byram, McCaffrey 1979 (EF-04),
Alpert 1972 (EF-05) — classic, no repo arXiv; Jin visibility 2404.11439 `[ABS]` (EF-07). → chapter 19.

---

## 18. Novel ND fire terms (Class C, default OFF) — `ws1a_firephys/novel_nd.py`

### (1) Role / I/O
Three **novel, unvalidated** soft features, **default OFF** (Rule 20/21), each returning a value + an
uncertainty that **grows** as conditions degrade (fail toward "uncertain", R19):
- **ND-1 de-aliased flicker** `nd1_dealiased_flicker(f_obs, fs, D_prior)` → consistency ∈[0,1].
- **ND-2 smoke-transmittance temperature** `nd2_transmittance_temperature(L_obs, τ_s, T_smoke)` → `(T̂_fire,
  σ_K)`.
- **ND-3 ignition index** `nd3_ignition_index(terms)` → non-negative scalar.

### (2) Rationale + alternatives
These are "not found in sources searched" (R21), so they are **hypotheses**, enter only as soft features with
a Class-A fallback, and are flag-gated OFF by default. Alternatives = the Class-A parents (Strouhal EF-08,
gray-body EF-14), which own the decision unless a flag is set. Our validity: **not measured**; status
`[HYPOTHESIS]`.

### (3) Formulation (verbatim)
```
ND-1: f_pred = 1.5/√D_prior ; f_alias_pred = |f_pred − fs·round(f_pred/fs)| ;
      consistency = exp( −(f_obs − f_alias_pred)² / (2σ_hz²) ),  σ_hz=0.3
ND-2: B_fire = (L_obs − (1−τ_s)·B(T_smoke))/τ_s ; T̂_fire = graybody_temperature(B_fire)
      σ_K = (σ_L_frac·|L_obs|/τ_s) / max(4εσT̂³, 1e-12)        # BLOWS UP as τ_s→0 (ill-conditioned)
ND-3: Π_ig = max( Σ_i w_i·scale_i·rate_i , 0 )
```
- **Limiting cases:** ND-1 `consistency→1` when observed matches aliased Strouhal prediction; ND-2 `σ_K→∞` as
  `τ_s→0` (τ_s clipped to [1e-3,1]); ND-3 clamped ≥0.
- **Dimensional check:** ND-2 `σ_K` via `dT/dL = 1/(4εσT³)` propagation — units of K. ✔

### (4)–(8) Diagram / I/O / recipe / HPs / code
`σ_hz=0.3`, `σ_L_frac=0.05` the only constants; closed-form; runs; tested. OFF unless `configs/firephys`
flags `nd1/nd2/nd3` are set (checked in the fire gate). `[CONFIRMED]` the code runs; **the hypotheses are
unvalidated.**

### (9) Uncertainty & calibration
By design uncertainty **grows** as data degrade (ND-2 σ_K explosion). No calibration (unvalidated). The gate
only lets ND-1 nudge consistency, ND-2 add uncertainty, ND-3 add ≤0.1·tanh(Π) to confidence. `[CONFIRMED]`.

### (10) Failure modes
Unvalidated novelty (could be wrong) → that is why they are OFF with an A/B fallback; ND-2 ill-conditioning at
thick smoke (handled by σ_K blow-up). → chapter 13.

### (11)–(13) Results / ideas / refs
No validation (**not measured**). Idea: run the pre-registered ablation vs the Class-A parent before ever
enabling (`ablation_plan.md`) `[HYPOTHESIS]`. Refs: novelty log `ws1_physics/novelty_log.md`; parents EF-08/
EF-14. → chapter 19.

---

## 19. Fire gate → fire ExpertOutput (Class A + gated C) — `ws1a_firephys/gate.py`

### (1) Role / I/O
Fuse CCTV detector confidence with physics plausibility (Byram) + optional Class-C soft features → advisory
`ExpertOutput(fire_phys)`. **In:** `FireInputs(detector_conf, multi_node_agree, Q_c, wind_U, nd1/nd2/nd3)`.
**Out:** `FireResult(p_fire, consistency, used_classC, diagnostics, expert)`.

### (2)–(3) Rationale + formulation (verbatim)
Transparent monotone mapping (no learned weights). 
```
c = 1.0
if Q_c,U given: c *= clip(N_c/2, 0.3, 1.0)                 # Byram regime down-weight
if nd1 flag:    c *= clip(0.5 + 0.5·nd1.consistency, 0.5, 1.0)
if nd2 flag:    extra_u = clip(nd2.σ_K/500, 0, 0.4)
p = clip(detector_conf, 0, 1); if nd3 flag: p = clip(p + 0.1·tanh(Π_ig), 0, 1)
if multi_node_agree: c = clip(c + 0.1, 0, 1)
u = clip(0.15 + 0.4·(1−c) + extra_u, 0, 1)
expert = ExpertOutput(p, source="fire_phys", u, c, r=1.0, cls=A)
```
Class-C contributions are flag-gated (default OFF) with an A/B fallback, and `used_classC` is reported
(Rule 20 transparency). The gate **never triggers an alarm**.

### (4)–(8) Diagram / I/O / recipe / HPs / code
Constants: `N_c/2` clip bounds, `0.1` boosts, `/500` smoke-uncertainty scale. Runs; tested. `[CONFIRMED]`.

### (9)–(13)
Uncertainty from physics-consistency + optional ND-2; multi-node agreement raises consistency. Failure modes:
appearance-only false alarms when physics inputs absent (then `c=1`, no down-weight) — mitigated by the
temporal CNN and multi-node corroboration. No skill number (**not measured**). Ideas: wire B-05 aliasing-aware
flicker as a consistency input `[HYPOTHESIS]`. Refs: EF-08/13/14. → chapter 19.

---

## 20. NF-1..NF-4 fusion primitives (Class B / C-adjacent) — `ws5_fusion_rl/nf.py`

### (1) Role / I/O
The soft weighting + uncertainty primitives every fusion model reuses. They **re-weight** experts; they never
fabricate a probability. All bounded to [0,1].

### (3) Formulation (verbatim)
```
NF-1 consistency: c_i = exp( −( (p_i − φ_physics)_+ )² / (2(σ²+ε)) ),  σ=0.25   # penalize claiming MORE alarm than physics
NF-2 reliability: r = clip( λ·r_prev + (1−λ)·outcome , r_min, 1 ) · (drift_penalty if drift)   λ=0.9, r_min=0.1
dispersion:       D = sqrt( Σ w_i (p_i − p̄)² ),  weights normalized
NF-3 conflict→U:  U* = Σ w_i u_i + λ·D(p),  λ=0.3,  clip[0,1]
NF-4 salience:    S = max_i [ r_i · c_i · ψ(p_i) ] over available experts,  ψ(p)=p
effective weight: w~_i = available · r_i · c_i · exp( −u_i / τ ),  τ=0.5
```
- **Limiting cases:** agreeing-or-below physics ⇒ `c_i=1`; no disagreement ⇒ `D=0 ⇒ U*=Σw_i u_i`; one expert
  ⇒ dispersion 0.
- **Dimensional check:** all inputs/outputs in [0,1]. ✔

### (2),(4)-(13) (grouped)
Rationale: transparent, auditable soft weights (NF-1/NF-4 are the "Class-C-adjacent" pieces, used only to
re-weight). Runs; tested. `[CONFIRMED]`. No training; no calibration of its own (feeds the fused `u_star`).
Failure mode: a mis-set `τ`/`λ` changes weighting aggressively → sensitivity **not measured**. Ideas: learn
`τ,λ` under the admission gate `[HYPOTHESIS]`. Refs: `DESIGN/ws5_fusion/novel_formulas_P22.md`. → chapter 19.

---

## 21. FM-1 precision-weighted mean + dispatcher (Class B) — `ws5_fusion_rl/fusion_models.py`

### (1) Role / I/O
The **default and fallback** fusion: a reliability-weighted arithmetic mean. The dispatcher `fuse()` selects
FM-1 / GMF / PHARAOH per config and reports `used_classC`. **In:** experts + cfg. **Out:** `FusionResult(p,
u_star, salience, model, used_classC, diagnostics)`.

### (3) Formulation (verbatim)
```
FM-1: p = Σ (w~_i / Σw~) · p_i   over available experts  (if Σw~≤0 → plain mean)
dispatcher: PHARAOH if operator.pharaoh & ≥2 experts & model≠GMF
            GMF      if model==GMF  (base + bounded residual)
            else FM-1
u_star = NF-3(ps, u, ws, λ);  S = NF-4
```
- **Limiting cases:** no experts ⇒ `p=0`, `u_star=1`. Class-C used ⇒ flagged.

### (2),(4)-(13) (grouped)
Rationale: a convex, monotone, always-available baseline is the honest default (Rule 20 fallback). Alternatives
GMF/PHARAOH are opt-in. Runs; tested. `[CONFIRMED]`. No training/calibration (FM-1 is parameter-free beyond
τ). Failure mode: a confident unreliable expert — mitigated by `r_i,c_i,u_i` in `w~`. No skill number (**not
measured**). Refs: cost-loss 2601.05921 `[ABS]`. → chapter 19.

---

## 22. PHARAOH adaptive-order power mean (Class C, default OFF) — `ws5_fusion_rl/pharaoh.py`

### (1) Role / I/O
A novel power-mean fusion operator that bends toward "max" (anti-complacency) only when a reliable,
physics-consistent alarm is credible. **Default OFF**; FM-1 is the fallback.
```
F_ρ(p;w) = ( Σ w_i p_i^ρ )^(1/ρ),  Σw_i=1
ρ(t) = 1 + κ·D·S,  κ=2, clipped [1,8]      # D=dispersion, S=salience
```
### (2)-(3)
Rationale: standard means can be complacent when one reliable expert alarms amid disagreement; PHARAOH raises
the aggregate then. **Safety corollary (to validate, tested numerically):** for `ρ≥1`, `F_ρ ≥ arithmetic
mean`, so it never under-states vs a plain average. It is **Class C, UNVALIDATED** (R21), opt-in only. Our
benefit: **not measured**; status `[HYPOTHESIS]`.

### (4)-(13) (grouped)
Limiting case `ρ=1 ⇒ arithmetic mean` (so disabling or `D·S=0` recovers the mean). Runs; tested (incl. the
`≥ mean` property). `[CONFIRMED]` code; **hypothesis unvalidated**. Failure mode: could over-warn if `κ`
mis-set — bounded by `ρ≤8` and the OFF default. Ideas: pre-registered ablation vs FM-1 `[HYPOTHESIS]`. Refs:
`DESIGN/ws5_fusion/novel_aggregation_operator_P22.md`. → chapter 19.

---

## 23. GMF numpy — gated-mixture + bounded residual (Class B) — `ws5_fusion_rl/gmf.py`

### (1) Role / I/O
The numpy runtime of gated-mixture fusion: a gate (normalized effective weights), a base mixture mean, and a
**bounded residual** (clipped ±cap, default 0) that can run the GMFHead exported from torch. **In:** experts
[+ optional head]. **Out:** `GMFResult(p, base, residual, gate)`.

### (3) Formulation (verbatim)
```
gate_i = w~_i / Σ w~    (effective weights, NF)
base   = Σ gate_i·p_i   (or PHARAOH mean if use_pharaoh_base)
residual = clip( head({base, dispersion, salience}), −cap, cap )   if head else 0
p = clip(base + residual, 0, 1)
load_numpy_head(json): closure(feats) = tanh(W2·tanh(W1·x + b1) + b2)·cap   # torch-free
```
- **Limiting case (central):** no head ⇒ residual 0 ⇒ **GMF ≡ FM-1** (graceful, honest).

### (2),(4)-(13) (grouped)
Rationale: lets a learned head make only a **bounded** correction so physics can't be dominated; runs offline
with the exported numpy head (no torch on the gateway). Runs; tested. `[CONFIRMED]`. Calibration: the residual
is the only learned nudge and is hard-bounded. Failure mode: mis-trained head — bounded by ±cap re-clip
(defense in depth). No skill number (**not measured**). Refs: `DESIGN/ws5_fusion/`; GMFHead = 05a §7. → ch 19.

---

## 24. BLUE/GLS correlation-aware weights (Class B) — `ws5_fusion_rl/correlation.py`

### (1) Role / I/O
Within-group minimum-variance (Aitken/GLS = BLUE) weights so **redundant sensors don't double-count**. **In:**
experts [+ correlation matrix or redundancy groups]. **Out:** non-negative weights (sum 1), fused `p`.

### (3) Formulation (verbatim)
```
Var_i ∝ 1 / effective_weight_i ; sd_i = √Var_i
Σ = outer(sd,sd) ⊙ R + ridge·I        # R: redundancy correlation (ρ=0.8 within a group), ridge=1e-3
w* ∝ Σ⁻¹·1  (solve); if singular → plain precision weights
w* = clip(w*, 0, None); renormalize    # SAFETY: no negative/hedging weights (Rule 19)
blue_fuse: p = Σ w*_i·p_i
```
- **Property (tested):** as redundant-pair correlation `ρ→1`, their **combined** weight → that of a single
  independent expert (cluster stops over-counting).
- **Safety override (documented deviation):** pure BLUE can assign **negative** hedging weights that could
  pull the fused alarm below every input — unacceptable for monotone life-safety fusion — so weights are
  clipped non-negative and renormalized (a deliberate, conservative deviation from the unconstrained optimum).

### (2),(4)-(13) (grouped)
Rationale: redundant soil probes / camera clusters otherwise swamp an independent source. Alternative = plain
precision weights (used as the fallback when Σ is ill-conditioned). Runs; tested. `[CONFIRMED]`. Failure mode:
mis-specified `R` → mitigated by ridge + shape guard + non-negativity. No skill number (**not measured**).
Ideas: estimate `R` from historical co-movement `[HYPOTHESIS]`. Refs: Aitken/GLS (classic). → chapter 19.

---

## 25. Hierarchical two-layer fusion (Class B) — `ws5_fusion_rl/hierarchical.py`

### (1) Role / I/O
Layer-1 fuses experts **within** each workstream into one group expert (propagating `u/c/r/class`); Layer-2
feeds the group experts to the **same single `decide()`** — no second decision path. **In:**
`{group:[experts]}` [+ redundancy map]. **Out:** group experts / full `Decision`.

### (3) Formulation (verbatim)
```
fuse_group: if corr/redundant_groups → BLUE/GLS weights + blue_fuse ; else FM/GMF/PHARAOH via fuse()
   u_star = NF-3 ; c_group = clip(1 − 2·dispersion, 0,1) ; r_group = Σ w·r / Σw
   cls_group = weakest-guarantee precedence [C, ADVISORY, DATA, B, A]  (Class-C never hidden)
hierarchical_fuse: map each group → one ExpertOutput
decide_hierarchical: decide(group_experts, shield, cfg)
```
- **Limiting case:** empty group ⇒ unavailable expert (`p=0,u=1,c=0,r=0`).

### (2),(4)-(13) (grouped)
Rationale: stops a crowd of correlated sensors in one workstream from swamping an independent workstream, and
keeps per-workstream reliability interpretable; reuses audited NF/FM primitives (nothing new fabricated). Runs;
tested (hierarchical + correlation). `[CONFIRMED]`. Class precedence is conservative (most-novel labels the
group — transparency, Rule 20). No skill number (**not measured**). Refs: `DESIGN/ws5_fusion §hierarchical`.
→ chapter 19.

---

## 26. Deep adapter — deep prob → ExpertOutput (torch-free) — `ws5_fusion_rl/adapters.py`

### (1) Role / I/O
Wrap a deep model's scalar probability into an `ExpertOutput` with the correct **Class** and a reliability
**cap**, torch-free, so cached model scores flow through `decide()` offline. **In:** `(source, prob, u=0.3,
c=1.0, r=None)`. **Out:** `ExpertOutput`.

### (3) Policy table (verbatim `_POLICY`)
| source | default r | cap r | Class |
|--------|-----------|-------|-------|
| geo_pinn | 0.90 | 1.00 | B |
| geo_phys | 1.00 | 1.00 | A |
| fire_cnn | 0.80 | 0.95 | DATA |
| fire_phys | 1.00 | 1.00 | A |
| eo | 0.70 | 0.90 | DATA |
| anomaly | 0.70 | 0.90 | DATA |
| cctv | 0.75 | 0.90 | DATA |
| **deepfake** | 0.30 | **0.40** | DATA (LOW) |

Unknown source ⇒ `KeyError` (must be registered). `r = clip(r, 0, cap)`; `p = clip(prob, 0, 1)`.

### (2),(4)-(13) (grouped)
Rationale: trust policy lives in one torch-free place; the deepfake 0.40 cap operationalizes `_CANON §6` /
Rule 19 (deepfake can never gate). Runs; tested. `[CONFIRMED]`. No training. Failure mode: forgetting to
register a new source (fails loud by design). Refs: `MODEL_CARDS`, `_CANON §6`. → chapter 19.

---

## 27. RL baseline + OPE admission (advisory) — `ws5_fusion_rl/rl.py`

### (1) Role / I/O
The numpy **honest fallback** policy + the **off-policy-evaluation gate** that admits a learned policy only if
it provably beats the baseline. (The trainable CQL is 05a §6; `OfflineRLPolicy.fit` here raises
`MissingDependency` — needs d3rlpy+torch.)
- `RuleBaselinePolicy(threshold=0.0476=p*)`: `act(risk)=1[risk≥threshold]`.
- `wis_value(behavior, target, rewards)` → `(value, ESS)`; `ope_feasible(behavior, min_prob=1e-2,
  min_ess_frac=0.1)`; `ope_admission(...)` → `OPEVerdict(deploy_learned = feasible AND v_t ≥ v_b)`.

### (3) Formulation (verbatim)
```
WIS: w_i = clip( target_i / clip(behavior_i,1e-6,·), 0, 1e3 );  value = Σ w·r / Σw ;  ESS = (Σw)² / Σw²
positivity+ESS: feasible = (min behavior ≥ min_prob) AND (ESS ≥ min_ess_frac·N)
admit learned iff feasible AND v_target ≥ v_baseline
```
- **Limiting case:** `Σw≤0 ⇒ value=0, ESS=0`; empty behavior ⇒ infeasible.

### (2),(4)-(13) (grouped)
Rationale: never deploy a learned alarm policy unless OPE is trustworthy (positivity + ESS) **and** it beats
the rule baseline (R19 fail-safe); the shield still bounds whatever is deployed. Runs; tested. `[CONFIRMED]`.
Failure mode: positivity violation / ESS collapse (the gate catches it ⇒ keep baseline). No value number
(**not measured** — no logs). Ideas: pessimistic/lower-bound OPE `[HYPOTHESIS]`. Refs: WIS/OPE (classic),
`_CANON §3` A5. → chapter 19.

---

## 28. Conformal calibration — CP / WCPS / ACI / Mondrian / CRC — `ws6_robust/conformal.py`

### (1) Role / I/O
Turn model scores into calibrated prediction sets / thresholds with honest coverage statements. **Feeds the
decision thresholds and the reliability/uncertainty reporting.**
- `conformal_quantile(scores, α)` — finite-sample `(1−α)` quantile.
- `regression_interval`, `weighted_conformal_quantile` (WCPS, covariate shift).
- `AdaptiveConformal` (ACI, Gibbs & Candès 2021) — long-run coverage under drift.
- `MondrianConformal` — per-group (per-hazard) coverage.
- `conformal_risk_threshold` (RCPS/CRC, Angelopoulos et al. 2022) — bounds the **miss-rate**.

### (3) Formulation (verbatim)
```
quantile: k = ceil((n+1)(1−α)) − 1 ; q = sorted_scores[clip(k,0,n−1)]
ACI: α_{t+1} = clip( α_t + γ(α_target − err_t), 0, 1 ),  err_t = 1 if y_t outside interval
Mondrian: separate q per group g ; unseen group → max (most conservative) q
CRC: corrected = target_risk − B/(n+1), B=1 ; pick lowest λ with mean(y=1 & score<λ) ≤ corrected
     (corrected ≤ 0 ⇒ λ=0, alarm on everything, fail-safe)
```
- **Honesty note (docstring):** realized coverage is reported; the bound is **not** called a "guarantee" (it
  holds only under exchangeability/correct weights and is **voided under concept drift** — `drift_monitor`).

### (2),(4)-(13) (grouped)
Rationale: marginal coverage can hide severe miscoverage of a rare critical hazard (GLOF) ⇒ Mondrian;
static CP breaks under drift ⇒ ACI; an ad-hoc level multiplier doesn't bound misses ⇒ CRC. Runs; tested
(CP/ACI/Mondrian/CRC). `[CONFIRMED]`. The decision function uses `conformal_risk_threshold` cut points when a
calibration set exists (`decision.conformal_level(thresholds=…)`). Failure mode: drift voids guarantees
(flagged). No measured coverage on real data (**not measured** — no datasets). Refs: Gibbs & Candès 2021
(ACI), Angelopoulos et al. 2022 (CRC/RCPS), Vovk (split-CP), Tibshirani et al. (WCPS) — classic / arXiv IDs in
chapter 19 ledger, not re-verified here. → chapter 19.

---

## 29. Decision function — the single advisory decision — `ws5_fusion_rl/decision.py`

### (1) Role / I/O
**Exactly one decision path.** **In:** experts [+ shield signals, cfg, hazard, drift, thresholds]. **Out:**
`Decision(level, risk, conformal set, shield, uncertain, advisory=True, used_classC)`.

### (3) Formulation (verbatim)
```
fused = fuse(experts, cfg) ; p* = cfg.p_star (= C_FA/(C_FA+C_miss) = 0.0476)
point = conformal_level(fused.p, p*, level_thresholds)       # cuts (p*, 4p*, 10p*) or calibrated CRC cuts
floor = shield_floor(shield_signals)                          # monotone
level = Level.raise_to(point, floor)                          # shield can only RAISE
uncertain = (no available experts) OR (fused.u_star > 0.6) OR drift
reliability from u_star: <0.2 HIGH, <0.4 MED, <0.6 LOW, else UNRELIABLE (drift⇒UNRELIABLE)
```
- **Limiting cases:** no experts ⇒ `risk=0` but `uncertain=True` (abstain + escalate, never silent); drift ⇒
  UNRELIABLE + uncertain.

### (2),(4)-(13) (grouped)
Rationale: one auditable path, calibrated cut points, shield-raised floor, explicit "uncertain" fail-safe
(R19); result is always `advisory=True` for a human. Runs; tested. `[CONFIRMED]`. No measured decision metrics
(**not measured** — gate not run on data). Refs: cost-loss 2601.05921 `[ABS]` (p* ↔ value score coherence,
E-06/E-07). → chapter 19.

---

## 30. Shield — monotone deterministic safety floor (Class A) — `ws5_fusion_rl/shield.py`

### (1) Role / I/O
A hard-coded, **monotone** floor that can only **RAISE** the level (never lower), applied after fusion. **In:**
`ShieldSignals`. **Out:** `ShieldResult(floor, raised, reason)`.

### (3) Rules (verbatim)
```
FS < 1.0                                   → ORANGE
tilt_rate > 5°/day AND nodes_agree ≥ 2     → RED
rain_24h > 150 mm AND high_susceptibility  → ORANGE
glof_lake_drop AND downstream_stage_jump   → RED
fire_multi_node (smoke+heat ≥2 nodes)      → ORANGE
floor = max over fired rules ; totality: always returns a defined Level
```
- **Design invariant:** a single uncorroborated node **cannot** reach RED — spatial corroboration (≥2 nodes)
  is required for the RED triggers.

### (2),(4)-(13) (grouped)
Rationale: a physics/corroboration-based hard safety net that no learner can switch off; monotone so it is
always safe-upward (Rule 19). No training (hard-coded). Runs; tested. `[CONFIRMED]`. Failure mode: thresholds
are planning values (`5°/day`, `150 mm`) that need regional calibration — **not measured**. Ideas: per-region
threshold calibration tied to CRC `[HYPOTHESIS]`. Refs: `DESIGN/COMPONENT_DESIGN.md §5`, Rule 19. → chapter 19.

---

### Cross-references
- End-to-end integration, the all-models comparison table, and the "which model when" guide: `05_MODELS.md`
  (CLOSING A/B/C).
- Deep (torch) models + fusion heads: `05a_MODELS.md`.
- Physics derivations in depth + meta-fusion design/validation: chapter 06. Bugs (bug-guard, sign errors,
  loss-weight imbalance): chapter 13. References with IDs/status: chapter 19.
