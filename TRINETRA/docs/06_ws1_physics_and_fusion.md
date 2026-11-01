# 06 — WS1 Physics Derivations & Meta-Fusion Design and Validation

> Scope (chapter frame WS1, per `_CANON.md §3`): the **physics gates** — geo-hazard (`ws1b_geophys/`,
> internal WS1b) and fire (`ws1a_firephys/`, internal WS1a) — plus the **meta-fusion decision head**
> (`ws5_fusion_rl/`, internal WS5). Primary sources read for this chapter: `DESIGN/LLD.md`,
> `DESIGN/COMPONENT_DESIGN.md`, `TRINETRA_MetaFusion_Design.md`, `TRINETRA_Corrected_Patches.md`,
> `analysis/08_equations_register.md`, `ws1_physics/*`, `ws5_fusion/*`, and the implementing code +
> golden tests under `trinetra/src/trinetra/` and `trinetra/tests/`.

---

## 06.0 How to read this chapter (the honesty posture, restated for physics)

Two facts from `_CANON.md` govern everything below and are repeated here because physics chapters are
the most tempting place to overclaim:

1. **Nothing was trained or measured.** Every performance figure that appears is **source-reported** from
   another paper on its own data (cite the arXiv ID), or it is **"not measured."** The equations here are
   *correctness* machinery, not *skill* machinery. The tests in `trinetra/tests/physics_golden/` prove the
   code computes the equation it claims to compute — they do **not** prove the equation forecasts a real
   landslide or fire. That distinction is load-bearing (`§06.C`).
2. **Every non-trivial claim carries a label** — `[CONFIRMED]`, `[LIKELY]`, `[HYPOTHESIS]`, `[INFEASIBLE]`
   (`_CANON.md §1`). Physics coefficients that still need a primary-source check carry `[coeff-verify]`
   exactly as the code marks them.

Two further load-bearing verdicts (`_CANON.md §6`) are carried verbatim throughout:

- **The full fire-PINN as a deployed on-device solver is `[INFEASIBLE]`** (stiffness, spectral bias,
  non-identifiability). Physics enters as *soft features + a Class-A fallback*, never as a live PDE solver
  on an ESP32. Source: `ws1_physics/model_set_decision.md` "REJECTED", `FINAL_REPORT.md §2`.
- **A calibrated set of members does NOT imply a calibrated ensemble**, and a calibrated ensemble cannot
  beat the average of its calibrated members (**arXiv 2101.05397**). The hierarchical fusion is strong for
  *decorrelation and interpretability* but is **not** theoretically optimal against joint-dependence or
  learned-attention fusers. This is stated plainly in `§06.B.9`.

### The Class A/B/C scheme (travels with every formula)

From `analysis/08_equations_register.md` and Rule 20 (`_CANON.md §5`):

```
Class A  = established / derivable from first principles        (e.g. infinite-slope FS, Stefan–Boltzmann)
Class B  = empirical / semi-empirical fit with regime limits    (e.g. Caine I–D, Fukuzono α-law)
Class C  = heuristic / novel / assumed                          (e.g. PHARAOH, ND-1..ND-3 fire features)
```

The hard rule (Rule 20): **Class-C novel terms are DEFAULT-OFF behind a feature flag, with a Class-A/B
fallback.** The code enforces this (`§06.A.5`, `§06.B.6`), and the golden tests assert it
(`test_firephys.py::TestFireGateFlagGating`, `test_fusion.py::TestFuseDispatch`).

---

# PART A — PHYSICS DERIVATIONS

The geo gate (`ws1b_geophys/gate.py`) and fire gate (`ws1a_firephys/gate.py`) are **transparent, monotone
mappings only** — no learned weights live in the physics layer; all learning/fusion lives in WS5. Each
gate emits one advisory `ExpertOutput` and **never emits a public alert** (Rule 19).

---

## 06.A.1 Infinite-slope Factor of Safety (Class A) — `fs.py`

### Governing equation (exactly as implemented)

`trinetra/src/trinetra/ws1b_geophys/fs.py` computes

```
         c' + sigma'_n * tan(phi')
FS  =  ----------------------------------
          gamma * z * sin(beta) * cos(beta)

with   sigma'_n = gamma * z * cos^2(beta)  -  u_w  +  sigma_s
```

- `FS` dimensionless; `FS < 1 ⇒ unstable`.
- `c'` effective cohesion [kPa]; `phi'` effective friction angle [deg → rad internally]; `gamma` soil
  unit weight [kN/m³]; `z` vertical depth to the slip surface [m]; `beta` slope angle [deg → rad];
  `u_w` pore-water pressure [kPa]; `sigma_s` **suction (apparent-cohesion) stress [kPa], `sigma_s ≥ 0`**.
- `GAMMA_W = 9.81 kN/m³`; pore pressure from head is `u_w = gamma_w · psi` (`pore_pressure_from_head`).

The register entry **E-01 / GH-01** states the classic wetness-ratio form
`FS = [c' + (γ − m·γ_w) z cos²β tanφ'] / (γ z sinβ cosβ)`. The code uses the **effective-stress form**
`σ'_n = γ z cos²β − u_w + σ_s`, which is the same relation with the buoyancy term written as an explicit
pore pressure `u_w` plus a suction term `σ_s` instead of the lumped wetness ratio `m`. This is the more
general representation and is what the suction-limit guard needs. `[CONFIRMED]` the two forms coincide
when `u_w = m γ_w z cos²β` and `σ_s = 0`.

### Assumptions / validity regime (from the docstrings + register E-01)

- Planar (translational) failure parallel to the slope; slope-parallel seepage.
- Infinite slope: `z ≪ slope length`, end effects neglected, 1-D column.
- Mohr–Coulomb effective-stress strength `τ_f = c' + σ'_n tan φ'`.
- Driving (shear) stress `γ z sinβ cosβ > 0` — the code **raises `ValueError`** if `γ, z, β` are not all
  positive (so `β = 0` exactly is rejected at the gate; the `β→0` limit is analytic, see below).

### The suction / effective-stress term and the SATURATED-LIMIT guard

The suction stress represents apparent cohesion from matric suction in unsaturated soil. The register
(**E-03**, Lu & Likos) and `TRINETRA_Corrected_Patches.md` **PATCH C (Bug #2)** fix a sign error in the
*original report*: Lu & Likos suction stress is `σ_s = −S_e·ψ` (`σ_s ≤ 0` under suction), and in `FS` it
must **ADD** resistance as suction grows. The shipped report's leading minus sign combined with "negative
= adds strength" made rising suction *reduce* FS — the opposite of physics.

The code resolves this cleanly by adopting the **magnitude convention**: `sigma_s ≥ 0` is passed in and
**added** to `σ'_n`. The critical physical guard is in the module docstring and is the acceptance test
from PATCH C:

```
As effective saturation S_e -> 1 (soil saturates):
    suction vanishes  =>  sigma_s -> 0
    =>  sigma'_n -> gamma*z*cos^2(beta) - u_w
    =>  FS reduces EXACTLY to the classic saturated effective-stress infinite-slope form.
```

So the general unsaturated `FS` and the saturated `FS` are *the same function* evaluated at `σ_s = 0`.
The code makes this literal: `factor_of_safety_saturated(...)` simply calls
`factor_of_safety(..., sigma_s=0.0)`. `[CONFIRMED]` by `test_geophys.py::TestFS::test_saturated_limit`
(the two agree to 12 decimal places).

### Dimensional check `[CONFIRMED]`

Numerator: `[kPa] + [kPa]·(dimensionless tanφ') = [kPa]`. Denominator:
`[kN/m³]·[m]·(dimensionless) = [kN/m²] = [kPa]`. `FS = [kPa]/[kPa] = dimensionless`. ✓

### Limiting cases

| Case | Behaviour | Status |
|------|-----------|--------|
| `σ_s → 0` (saturation) | reduces to saturated form | `[CONFIRMED]` test_saturated_limit |
| rising suction `σ_s ↑` | `FS` strictly increases (more apparent cohesion) | `[CONFIRMED]` test_monotonic_in_suction |
| rising pore pressure `u_w ↑` | `FS` decreases (less effective stress) | `[CONFIRMED]` test_decreasing_in_pore_pressure |
| `β → 0` (flat) | `sinβ cosβ → 0 ⇒ FS → +∞` (register E-01 limit) | analytic; code rejects `β=0` exactly to avoid 0-division |
| cohesionless, dry, `u_w=σ_s=0` | `FS → tanφ'/tanβ` (the textbook dry-sand result) | `[CONFIRMED]` by substitution |

### Mapping to the gate signal

`gate.py` turns `FS` into a soft probability with a monotone, transparent sigmoid:
`p_fs = σ(k_fs·(1 − FS))`, `k_fs = 4.0` default. `FS = 1 ⇒ p_fs = 0.5`; `FS < 1 ⇒ p_fs > 0.5`. No learning.

**Golden case that locks it (gate G1):** `test_saturated_limit` + the two monotonicity tests
(`test_geophys.py`). **Sources:** standard geotechnics; register E-01/E-03/GH-01; sign fix
`TRINETRA_Corrected_Patches.md` PATCH C (Lu & Likos 2006). Coefficient confidence: structural form Class A;
the suction model `[coeff-verify]` against a fitted local soil-water retention curve.

---

## 06.A.2 Iverson (2000) transient pressure head (Class A/B) — `iverson.py`

### The diffusion response and the governing form (exactly as implemented)

`trinetra/src/trinetra/ws1b_geophys/iverson.py` implements the linearized-Richards transient response:

```
R(Z, t)  =  sqrt(4 * D1 * t) * ierfc( Z / sqrt(4 * D1 * t) )

psi_transient(Z, t)  =  (I_z / K_z) * R(Z, t)

with   ierfc(x)  =  exp(-x^2)/sqrt(pi)  -  x * erfc(x)         (ierfc(0) = 1/sqrt(pi))
       D1       =  D0 / cos^2(beta)      (hydraulic diffusivity along bedding)
```

- `Z` vertical depth [m]; `t` time since infiltration onset [s]; `D0` saturated hydraulic diffusivity
  [m²/s]; `D1` slope-adjusted diffusivity; `K_z` vertical saturated hydraulic conductivity [m/s];
  `I_z` surface flux (rainfall infiltration rate) [m/s], with `I_z ≤ K_z`; `beta` slope angle.
- `erfc` is taken from stdlib `math` (vectorized) because **scipy is unavailable in the sandbox**
  (`_CANON.md §2`). `ierfc` is the integral of the complementary error function.
- Total head = steady background + transient: `pressure_head = psi_steady + transient_head`.

### THE bug-guard — slope enters ONLY via `D1 = D0/cos²β`, with NO extra `cos β`

This is the single most important correctness fact in the geo physics layer, and it is enforced three
ways: in the code structure, in `DESIGN/LLD.md §2`, and in a dedicated golden test.

**The bug (from `TRINETRA_Corrected_Patches.md` PATCH B, Bug #3 + its root Bug #17):** the shipped report
wrote the transient term with a **spurious extra `· cos β`** multiplier:

```
WRONG (shipped report):  psi = (Z-d)cos^2 b + 2 (I_z/K_s) * cos(b) * sqrt(D1 t) * ierfc( Z / (2 sqrt(D1 t)) )
RIGHT (Iverson 2000):    psi = (Z-d)cos^2 b + 2 (I_z/K_s) *         sqrt(D1 t) * ierfc( Z / (2 sqrt(D1 t)) )
```

Slope legitimately enters in exactly two places: the **steady term** `(Z − d)·cos²β`, and the
**diffusivity** `D1 = D0/cos²β`. The transient *response kernel* `R` carries **no** standalone cosine.
The error is pernicious because it propagates into every downstream `FS(Z,t)` and into the physics gate.
Confirmed against Iverson (2000) *Water Resources Research* 36(7):1897–1910 and the project's own
`research/06_physics §1.1`.

**The fix in code:** slope-adjustment is *physically quarantined*. `diffusivity_D1(D0, beta)` is the
**only** function that touches `cos β`; the core response `_transient_core(Z, t, D1, I_z, K_z)` receives
`D1` already slope-adjusted and is otherwise slope-free "by construction" (its docstring: *"Guarantees no
extra cos(beta)"*). You physically cannot introduce a second cosine without editing the one guarded line.

**Golden case that locks it (gate G1):** `test_geophys.py::TestIverson::test_slope_only_through_D1`
asserts the public `transient_head(...)` equals the slope-free core evaluated at `D1 = D0/cos²β`
(to 12 dp) **and** asserts it does **NOT** equal the buggy `core · cos²β` version (to 6 dp). Also
`test_transient_zero_at_t0` (response is 0 at `t=0`) and `test_ierfc_at_zero` (`ierfc(0)=1/√π`).

### Multi-pulse linear superposition (finite-pulse recovery)

`transient_head_multipulse(...)` exploits that the linearized Iverson response is **linear in the surface
flux**, so a piecewise-constant rainfall history expressed as absolute-intensity steps `{(t_k, I_k)}`
superposes (Iverson/Baum):

```
psi(Z, t)  =  sum_k  ( (I_k - I_{k-1}) / K_z ) * R(Z, t - t_k) * H(t - t_k),      I_{-1} = 0
```

where `R` is the unit ierfc response (`_response_R`, no `I/K` factor — the linear kernel) and `H` the
Heaviside step. A **finite pulse** of intensity `I` over `[0, T]` is just the two steps `(0, I)` and
`(T, 0)`, giving the classic recovery after the rain stops:

```
psi  =  (I/K_z) * [ R(Z, t)  -  R(Z, t - T) ]
```

ASCII picture of the finite-pulse response:

```
 psi(Z,t)
   |            rain ON [0,T]        rain OFF (t>T): second (negative) step kicks in
   |          .  -  -  -  -  .
   |        .                 ` .            head RELAXES back down (but stays > 0)
   |      .                       `  .  .
   |    .                               `  .  .  .  .
   +---+------------------------+------------------------>  t
      0                         T
```

**Golden cases (gate G1), `test_iverson_multipulse.py`:**
- `test_single_step_matches_transient_head` — one step reproduces `transient_head` (12 dp).
- `test_finite_pulse_recovers_after_rain_stops` — equal to the continuous solution up to `T`, strictly
  **below** it after `T` (recovery), and still `> 0`.
- `test_superposition_linearity` — two onset times combine as the sum of standalone pulses (10 dp).
- `test_intensity_monotone` — doubling intensity raises the head.

### Steady-state and `β → 0` limits

- **Steady state** (`t → ∞`, or constant long-duration flux): the transient term asymptotes and the head
  approaches `psi_steady + (I_z/K_z)·(saturated response)`; the pressure field becomes the background
  seepage field — the register notes the `t→∞` steady-state and `β→0` checks as planned verifications
  (E-02; LLD §2 "GOLDEN TESTS: β→0 & t→∞ steady-state").
- **`β → 0`** (flat): `cos²β → 1 ⇒ D1 → D0`; the response reduces to the 1-D vertical diffusion solution
  with no slope correction. `[CONFIRMED]` by inspection of `diffusivity_D1`.

**Class / sources:** register E-02/GH-02 label it Class A/B (Class-A diffusion structure, Class-B because
`D0, K_z` are site parameters, `[coeff-verify]`). Source: Iverson 2000 WRR; Baum et al. (TRIGRS lineage).

---

## 06.A.3 Fukuzono inverse-velocity failure-time forecast (Class A/B) — `fukuzono.py`

### The law and the α regime (exactly as implemented)

From Fukuzono (1985) / Voight (1988): a slope accelerating toward failure follows
`d²Ω/dt² = A·(dΩ/dt)^α` (Ω = displacement). The code's module docstring states the two regimes cleanly
(this is the `TRINETRA_Corrected_Patches.md` **PATCH D / Bug #4** fix — the report had mixed `α=2` with
the general `A(α−1)` factor):

```
1/v = A*(alpha-1)*(t_f - t)

alpha = 2   =>  1/v  LINEAR in t ;  t_f = x-intercept  (the common operational case)
alpha != 2  =>  v^(1-alpha) linear in t                (regime flag, NOT silently 1/v)
```

The code picks the linearized variable by regime:
`y = 1/v` if `|α − 2| < 1e-9`, else `y = v^(1−α)`; the `regime_note` string records which. **Failure time
is the x-intercept** `t_f = −b/m` of the fitted line `y = m·t + b`.

### What the code ADDS over a bare OLS intercept

Two operational upgrades (module docstring), both honesty-driven (Rule 19 — an operator must see
uncertainty, not false point certainty):

**(1) Recency-weighted least squares (exponential half-life).** The latest creep points dominate imminent
failure, so they are up-weighted: `_recency_weights(t, halflife) = 0.5 ^ ((t_max − t)/halflife)` — weight
1 at the most recent sample, decaying backward. `_wls(x, y, w)` solves the weighted normal equations
`β = (XᵀWX)⁻¹ XᵀW y` and returns a weighted `r²`.

**(2) Delta-method prediction interval on `t_f`.** Because `t_f = −b/m` is a nonlinear function of the
fitted `(m, b)`, the code propagates the regression covariance `Cov([m,b]) = σ²·(XᵀWX)⁻¹` through the
gradient:

```
t_f = -b/m
grad = ( d t_f/d m , d t_f/d b ) = ( -t_f/m , -1/m )
var(t_f) = grad^T * Cov([m,b]) * grad
se(t_f)  = sqrt(var(t_f))
[ t_f_low , t_f_high ] = t_f  ±  z * se(t_f)        (z = 1.96 ≈ 95%)
```

So the operator receives `t_f ∈ [low, high]`, not a false point estimate. The weighted residual variance
is `σ² = Σ w·resid² / dof`, `dof = max(n−2, 1)`.

### Units, assumptions, validity

- `t` [any consistent time unit, e.g. h]; `v` [displacement/time]; velocities **must be positive**
  (code raises `ValueError` otherwise). `t_f` in the same units as `t`.
- Assumes the inverse-velocity relation is approximately linear over the fitted window (tertiary creep,
  `α ≈ 2`); fails outside tertiary creep. Register E-04 flags the report's `α ∈ [1.5, 2.2]` claim as
  **Bug #4** — resolved: `α = 2 ⇒ 1/v` is a *special case*, not a range to use silently.
- If `|m| < 1e-12` (no detectable acceleration), returns `t_f = +∞` (no imminent failure).

### Mapping to the gate signal

`gate.py`: if a `FukuzonoFit` with finite `t_failure` is supplied, lead time `lead = t_f − now`; if
`lead > 0`, `p_fk = clip(1 − lead/48, 0, 1) · clip(r², 0, 1)` — proximity to failure within a 48-hour
horizon, down-weighted by fit quality. Transparent and monotone.

**Golden cases (gate G1):** `test_geophys.py::TestFukuzono::test_recover_tf_alpha2` (noiseless 1/v line
recovers `t_f=100` to 4 dp, `r² > 0.999`); `test_fukuzono_ci.py` — noiseless fit gives `se ≈ 0`, noise
widens the interval and the interval **brackets the truth**, recency path stays sane on a clean line.
**Class / sources:** Class A/B (the α=2 linearity is derivable; `A, α` are empirical). Fukuzono 1985;
Voight 1988. Register E-04.

---

## 06.A.4 Caine intensity–duration rainfall threshold (Class A/B) — `caine.py`

### The relation (exactly as implemented)

Caine (1980): the rainfall intensity–duration landslide-triggering threshold

```
I = a * D^(-b)                 I = rainfall intensity [mm/h],  D = duration [h]
caine_threshold(D, a, b) = a * D^(-b)       (NaN for D <= 0)
caine_exceedance(I, D, a, b) -> ( I/I_thr > 1 ,  ratio = I/I_thr )     ratio>1 => above the ID line
```

### Assumptions, validity, and the honest coefficient caveat

- `(a, b)` are **region-specific empirical constants** and **MUST be locally re-fit** (config keys
  `geophys.caine_a`, `geophys.caine_b`; defaults `a=14.0`, `b=0.39`). The code docstring is explicit:
  *"never a borrowed global constant used as live truth."*
- Register **E-05 / GH-05** lists candidate constants to verify (**Bug #15, `[coeff-verify]`**):
  Caine `14.82·D^−0.39`; Dahal–Hasegawa `73.9·D^−0.79`; Garhwal `1.82·D^−0.23`. It also carries the
  deeper caveat from **arXiv 2608.12422**: the threshold is better treated as a **distribution, not a
  constant**. `COMPONENT_DESIGN.md §5` reinforces: feed a **rainfall ensemble → a distribution of FS**,
  not a point.
- Class B throughout (empirical fit with regional validity limits).

### Mapping to the gate signal

`gate.py`: `p_caine = clip(ratio − 0.5, 0, 1)` — a soft margin above the ID line, not a hard trigger.

**Golden case (gate G1):** `test_geophys.py::TestCaine::test_exceedance_direction` — high intensity
exceeds, low intensity does not, and the ratio orders correctly. This tests **direction/correctness**, not
threshold skill. **Sources:** Caine 1980; Dahal–Hasegawa; regional Garhwal fits. Register E-05.

### How the geo gate combines the four sub-signals

`geo_gate` (`gate.py`) fuses `p_fs, p_caine, p_fk` with a **noisy-OR**: `p_phys = 1 − Π(1 − p_i)`. This is
monotone and conservative ("never under-warn"). A consistency score `c = 1 − std(active signals)` (if ≥2
active) feeds NF-1 downstream. The emitted `ExpertOutput` is `source="geo_phys"`, `cls = Class A`,
`r = 1.0`, with `u` rising as consistency falls. **The gate never raises a public alert.**

---

## 06.A.5 Fire physics layer (Class A established + Class C novel, flag-gated) — `established_ef.py`, `novel_nd.py`, `gate.py`

### Why the full fire-PINN is `[INFEASIBLE]` and what is carried instead

`ws1_physics/model_set_decision.md` "REJECTED" records the scoping decision verbatim: a **full fire PINN
as a deployed on-device solver is rejected** — PINN failure modes (stiffness, loss-weight imbalance,
spectral bias, causality violation, poor extrapolation, non-identifiability) make a live fire-PINN a
research risk, not an ESP32 path. **This is a scoping decision, not a claim that PINNs cannot work.**
Physics instead enters three honest ways: as **features**, as **priors/consistency checks**, and as an
**offline synthetic-data simulator** — always with a Class-A fallback.

The implemented code is a **faithful, computable SUBSET** of the EF-01..EF-20 inventory. Each function is
Class A and carries `[coeff-verify]` where a literature coefficient must be confirmed against a primary
source (SFPE Handbook / Heskestad / McCaffrey) before driving any live output.

### Established Class-A blocks (exactly as implemented in `established_ef.py`)

| Block | Equation (verbatim from code) | Units | Source `[coeff-verify]` |
|-------|-------------------------------|-------|-------------------------|
| Heskestad mean flame height | `L = 0.235 * Q_kW^0.4  -  1.02 * D_m` | `L,D` [m], `Q` [kW] | Heskestad 1983 (EF-01) |
| Strouhal puffing frequency | `f = 1.5 / sqrt(D_m)` | `f` [Hz], `D` [m] | Cetegen & Ahmed 1993 (EF-08/EF-16) |
| Heskestad plume centerline ΔT | `dT0 = 9.1*(T_inf/(g cp^2 rho^2))^(1/3) * Q_c^(2/3) * (z-z0)^(-5/3)` | [K] | Heskestad (EF-03) |
| Byram **convection number** | `N_c = (2 g Q_c') / (rho cp T_inf U^3)` | dimensionless | EF-13 (2501.08343, 2406.08589) |
| Gray-body radiant exitance | `M = emissivity * sigma * T_K^4`, `sigma = 5.670374419e-8` | [W/m²] | Stefan–Boltzmann (EF-14 context) |
| Gray-body temperature (inverse) | `T = (M/(emissivity*sigma))^0.25` | [K] | Stefan–Boltzmann |
| Beer–Lambert transmittance | `tau = exp(-(kappa+sigma)*L)` | dimensionless | EF-07/EF-14/EF-15 |

**⚠ Honest naming note you must carry:** an early mission-brief line used the loose phrase **"Byram fireline
intensity."** The **implemented function is the Byram _convection
number_ `N_c`** (a dimensionless buoyant-power / flow-power **regime gate**), **not** the fireline-intensity
`I_B = H·w·r` [kW/m]. `_CANON.md §4` has been **corrected to say "Byram convection number N_c"** and the
established-formula inventory (`established_formula_inventory_P21.md`, EF-13) is
internally consistent with the code — it also lists **"Byram convective number N_c / critical Froude"**, a
*regime gate*. So the code, the P21 inventory, and the current canon all agree; only the original one-line
brief used the looser phrase "fireline intensity." Treat the implemented quantity as the **Byram convection
number /
critical-Froude regime gate**: `N_c > ~2 ⇒ plume-dominated (buoyant)`, `N_c < ~1 ⇒ wind-dominated`, used
to **reject non-fire regimes**. No fireline-intensity `I_B` equation exists in the code.

**Dimensional / limiting checks `[CONFIRMED]`:**
- Flame height: `L` grows with `Q` (`test_firephys.py::test_flame_height_increases_with_Q`).
- Strouhal: `f` falls as plume size `D` grows (`test_strouhal_decreases_with_size`).
- Gray-body round-trip: `graybody_temperature(graybody_radiance(T)) = T` (6 dp,
  `test_graybody_roundtrip`) — the `T⁴` law and its inverse are consistent.
- Byram regime: low wind ⇒ higher `N_c` (more plume-dominated) (`test_byram_regime`).

### Why Class-C novel flicker/ND terms are DEFAULT-OFF with an A/B fallback

`novel_nd.py` holds three NOVEL (Class C, **unvalidated**) candidates. Per Rule 20/21 they are **not found
in our limited search** (a *search claim*, not a proof of originality), **default-OFF** (configs
`firephys.nd1/nd2/nd3`), and when used enter fusion **only as soft features with a Class-A fallback and a
visible class flag**. Nothing is claimed to work. Each returns a value **plus an uncertainty that GROWS as
conditions degrade**, so the system fails toward "uncertain" (Rule 19).

```
ND-1 de-aliased flicker:  aliased_frequency(f_true, fs) = |f_true - fs*round(f_true/fs)|
                          nd1_dealiased_flicker: consistency = exp(-(f_obs - f_alias_pred)^2 / (2 sigma_hz^2))
                          — tests whether an observed (possibly aliased) low-fps flicker peak matches the
                            Strouhal-predicted true flicker for a plume of size D_prior. A SOFT consistency,
                            NOT a trigger.

ND-2 smoke-transmittance temperature:
   model:  L_obs = tau_s*B(T_fire) + (1-tau_s)*B(T_smoke)  =>  B(T_fire) = (L_obs - (1-tau_s)B_smoke)/tau_s
   uncertainty sigma_K = (sigma_L_frac*|L_obs|/tau_s) / (4*emissivity*sigma*T_fire^3)
   — sigma_K BLOWS UP as tau_s -> 0 (ill-conditioned behind thick smoke) => fail-safe to 'uncertain'.

ND-3 dimensionless ignition index:  Pi_ig = sum_i w_i * scale_i * rate_i   (non-negative; soft feature only)
```

**The gate (`fire_gate`) wiring, exactly as implemented:**

```
p = detector_conf                         # CCTV detector confidence (WS4) is the Class-A/data base
c = 1.0                                    # physics-consistency starts fully consistent

(A, Class A gate)  if Q_c' and wind given:  N_c = byram_convection_number(...);  c *= clip(N_c/2, 0.3, 1.0)
(C soft, flag)     if nd1 and cfg.firephys.nd1:  c *= clip(0.5 + 0.5*consistency, 0.5, 1.0);  used_classC=True
(C soft, flag)     if nd2 and cfg.firephys.nd2:  extra_u = clip(sigma_K/500, 0, 0.4);        used_classC=True
(C soft, flag)     if nd3 and cfg.firephys.nd3:  p = clip(p + 0.1*tanh(Pi_ig), 0, 1);         used_classC=True
                   if multi_node_agree:  c = clip(c + 0.1, 0, 1)      # IoT corroboration raises consistency
u = clip(0.15 + 0.4*(1 - c) + extra_u, 0, 1)
emit ExpertOutput(p, source="fire_phys", u, c, r=1.0, cls=Class A)
```

The Byram number is a **Class-A down-weighting gate**: a wind-dominated regime (`N_c` small) multiplies
consistency down, rejecting steam/headlights/non-fire. Class-C terms can only *nudge* `p` (ND-3, capped at
`0.1·tanh`), *shape* consistency (ND-1), or *add uncertainty* (ND-2) — never a hard trigger.

**Golden cases (gate G1 + Rule 20), `test_firephys.py`:**
- `test_classC_off_by_default` — with ND-3 terms supplied but the flag off, `used_classC == False`.
- `test_classC_on_when_flag_set` — flipping `firephys.nd3=True` flips `used_classC` to True.
- `test_wind_regime_lowers_consistency` — a windy regime yields lower consistency than a calm one.
- `test_aliasing_identity` — `fs > 2·f_true ⇒ no aliasing`; `7 Hz @ 10 Hz ⇒ 3 Hz` alias (Nyquist math).
- `test_nd2_uncertainty_grows_as_smoke_thickens` — thicker smoke (`tau_s` small) ⇒ larger `sigma_K`.

**Class / sources:** EF blocks Class A `[coeff-verify]` (Heskestad 1983, McCaffrey 1979, Cetegen & Ahmed
1993, SFPE Handbook, Stefan–Boltzmann); ND-1..ND-3 Class C **unvalidated** (register EF-08/B-05 lineage).

---

# PART B — META-FUSION DESIGN (WS5, `ws5_fusion_rl/`)

The meta-fusion head answers the user's architectural idea captured in `TRINETRA_MetaFusion_Design.md`:
*"a model that takes the raw input AND the RL policy's output and produces the final decision."* That idea
is named and grounded: **stacking (Wolpert 1992) over a policy** = residual policy learning
(**arXiv 1812.06298**, 1812.03201) + a **post-posed safety shield** (**arXiv 1708.08611**) + offline RL
(**arXiv 2110.06169** IQL). These are source-reported citations; nothing here is a measured result.

## 06.B.1 The expert set and the `ExpertOutput` contract

Three expert families feed fusion (`TRINETRA_MetaFusion_Design.md §3`, `COMPONENT_DESIGN.md §1`):

```
EXPERT 1  physics / Bayes base rule   -> p_phys, base action a0   (geo_phys, fire_phys gates; Class A/B)
EXPERT 2  offline-RL alarm policy     -> action logits / q-values (advisory; see chapter 10)
EXPERT 3  supervised / anomaly ensemble -> p_sup                  (Class data)
```

Every expert emits the **same contract** (`DESIGN/LLD.md §0`, implemented in `common/types.ExpertOutput`):

```python
ExpertOutput:
  p    : float   # calibrated probability in [0,1] (hazard present / threshold exceeded)
  u    : float   # predictive uncertainty in [0,1]
  c    : float   # physics-consistency in [0,1] (NF-1); 1.0 if N/A
  r    : float   # reliability / trust in [0,1] (NF-2); from quality + drift history
  cls  : A|B|C|DATA|ADVISORY     # honesty class label
  source : str
  available : bool               # missing modality -> available=False (NOT a silent zero)
```

**Deep-model outputs are wrapped by `adapters.py`** into this contract with **source-appropriate class +
reliability caps** (torch-free so the offline gateway needs no torch):

```
geo_phys/fire_phys : r_default 1.00, cap 1.00, Class A     (pure deterministic physics)
geo_pinn           : r_default 0.90, cap 1.00, Class B     (physics-informed NN, learned)
fire_cnn/eo/anomaly/cctv : caps 0.90–0.95, Class DATA      (medium trust)
deepfake           : r_default 0.30, cap 0.40, Class DATA  (LOW trust; hard-capped — Rule 19)
```

The deepfake cap at **0.40** is the code-level enforcement of the `_CANON.md §6` verdict that
deepfake/zero-shot/social signals are **low-trust advisory only, must be corroborated**, and may never gate
a life-safety alert. `[CONFIRMED]` `test_adapters.py::test_deepfake_reliability_hard_capped` (even
`reliability=0.99` is clipped to `≤ 0.4`), and `test_flows_through_decide` (a 0.8-prob deepfake does not
pull the fused risk to 0.8).

## 06.B.2 Effective weights (NF-1 / NF-2) — `nf.py`

The single weight that every fuser consumes (`COMPONENT_DESIGN §8.1`, implemented `effective_weight`):

```
w~_i  =  availability_i  *  r_i  *  c_i  *  exp( -u_i / tau )          tau = 0.5 default
```

Reading: an **unavailable** (`w~=0`), **drifted** (low `r`), **physics-inconsistent** (low `c`), or
**highly-uncertain** (large `u`) expert is automatically down-weighted. `exp(−u/τ)` is a soft precision
weight needing **no Gaussian assumption** — this is the honest substitute for Kalman-style precision
weighting, which would assume calibrated Gaussian uncertainties and known correlation we do not have.

The four NF sub-formulas (`novel_formulas_P22.md`, implemented in `nf.py`):

```
NF-1 consistency:  c_i = exp( -((p_i - phi)_+)^2 / (2(sigma^2+eps)) )
       — penalizes claiming MORE alarm than physics phi supports; agreeing-or-below physics is fully consistent.
NF-2 reliability:  r = clip( lam*r_prev + (1-lam)*outcome , r_min, 1 );  *drift_penalty if drift flagged
       — exponential-forgetting trust; a drift flag multiplies it down. r_min>0 => never fully silenced w/o review.
NF-3 conflict->uncertainty:  U* = sum w_i u_i  +  lam * D(p) ,   D = weighted dispersion   (lam=0.3 default)
       — more disagreement => more uncertainty (fail toward 'uncertain'). Clipped to [0,1].
NF-4 salience:  S = max_i [ r_i * c_i * psi(p_i) ]        (psi here = identity on p)
       — "is ANY trustworthy, physics-consistent alarm credible?" Drives PHARAOH's adaptive order.
```

NF-1 and NF-4 are the **Class-C-adjacent** pieces: they only **re-weight** experts, they **never fabricate
a probability**. All are bounded to `[0,1]`.

## 06.B.3 FM-1..FM-6 — the six fusion options, FM-1 as Class-A default/fallback

`DESIGN/LLD.md §8.3` enumerates six fusion-model options, flag-selectable, **default FM-1**:

```
FM-1  precision/reliability-weighted linear mean   [B, DEFAULT + FALLBACK]
FM-2  evidential + conflict-discounting            [B]
FM-3  conformal-bounded hierarchical stacking      [B]
FM-4  covariance-intersection (continuous trend)   [B]
FM-5  physics-consistency-gated MoE  g_i=sigma(a_i(x)+beta*log c_i)   [C]
FM-6  RL-tuned fusion weights w/ physics-informed reward             [C, advisory]
```

**What is actually implemented** (`fusion_models.py`, honest state): **FM-1 is fully implemented** as the
default and the fallback; FM-2..FM-6 are *registered as names with FM-1 fallback stubs* until each is
validated — the docstring says plainly *"not implemented beyond interface here."* FM-1:

```
fm1_precision_weighted(experts, tau):   p = sum_i (w~_i / sum w~) * p_i      over available experts
```

The dispatcher `fuse(experts, cfg)` reads `configs/fusion` and routes: PHARAOH (if flag on and ≥2 experts),
else GMF (if `model=="GMF"`), else **FM-1**. It reports `used_classC` and computes `U*` (NF-3) and salience
(NF-4). **Golden case:** `test_fusion.py::test_default_is_fm1_not_classC` — default dispatch is FM-1 and
`used_classC == False`.

## 06.B.4 GMF — gated-mixture fusion with a BOUNDED (hard-clipped) residual — `gmf.py`

GMF is the M6 centerpiece and the direct realization of the "residual policy learning" idea. Three parts:

```
(1) GATE:     gated_weights = w~_i / sum w~_j        (normalized effective weights; sums to 1)
(2) BASE:     base = sum_i gate_i * p_i              (precision-weighted mean; PHARAOH may supply the base)
(3) RESIDUAL: res = clip( head(features), -residual_cap, +residual_cap )     residual_cap = 0.1 default
              p = clip( base + res, 0, 1 )
```

### Why the residual is HARD-clipped (the safety argument)

The residual is **the only place a learned head can nudge the output**, and it is **hard-clipped to
±`residual_cap`** so a mis-trained or adversarial head **can never dominate physics**. Without a trained
head the residual **defaults to 0**, so GMF reduces exactly to the precision-weighted mean (graceful,
honest — no silent adjustment). The exported-head path (`load_numpy_head`) runs a tiny 2-layer tanh MLP in
pure numpy and **re-applies the cap**, so even a head exported with huge weights stays bounded on the
offline gateway (no torch needed).

ASCII of the bound:

```
   head(features) ∈ (-inf, +inf)   --->   clip to [-cap, +cap]   --->   base ± (≤cap)
        rogue head = +999                        = +0.1                   physics base barely moved
```

**Golden cases, `test_gmf.py`:** `test_gate_sums_to_one`; `test_no_head_means_zero_residual`
(`residual == 0`, `p == base`); `test_residual_is_hard_bounded` (a head returning `±999` is clipped to
`±0.1`); `test_numpy_head_export_loads_and_stays_bounded` (large export weights still bounded);
`test_dispatch_selects_gmf` (and GMF with PHARAOH off is **Class B, not C**). Class B.

## 06.B.5 PHARAOH — adaptive-order power mean (Class C, flag-gated OFF) — `pharaoh.py`

**PHARAOH** = *Physics-consistency, Hazard-Aware, Reliability-decayed, Adaptive-Order Hölder mean*
(`novel_aggregation_operator_P22.md`). It is **Class C, UNVALIDATED, DEFAULT-OFF** (config
`fusion.operator.pharaoh`), fallback FM-1. Nothing is claimed to work or to beat anything (Rule 21).

```
Operator:   F_rho(p; w) = ( sum_i w_i * p_i^rho )^(1/rho),   sum w_i = 1
Adaptive order:   rho(t) = 1 + kappa * D * S          (kappa=2.0 default, clamped to [1, 8])
   D = weighted dispersion (disagreement),  S = credible-alarm salience (NF-4)
```

**Design intent (anti-complacency, fails-open):** when sources **agree** (`D≈0`) or **no credible alarm**
exists (`S≈0`) ⇒ `rho≈1` ⇒ plain weighted average. When sources **disagree AND a trustworthy,
physics-consistent source is alarming** ⇒ `rho` grows ⇒ the mean **bends toward MAX** (fail-toward-caution).
It is **clamped at `rho=8`** to avoid pure-max over-alarm. The **safety corollary** (power-mean inequality):
for `rho ≥ 1`, `F_rho ≥ arithmetic mean` — so PHARAOH **never under-states relative to a plain average**.

**Properties P1–P7** (on paper, `novel_aggregation_operator_P22.md §5`): bounded (P1), monotone (P2),
known-mean limits (P3), power-mean inequality / anti-complacency (P4), idempotence (P5), availability-safe
(P6), non-vetoing (P7). **These are DERIVED ON PAPER and must be numerically verified before the flag may
default ON** (gate G4; `LLD §8` acceptance). The code only *partially* checks them in tests (P4, order
monotonicity). **Honest limitation (carried verbatim):** the heuristic `U*` is **not a calibrated
variance**; `rho(t)=1+κDS` is a **design choice, not an optimum**; the safety corollary **biases toward
alarms by construction** (raises false-alarm risk).

**Golden cases, `test_fusion.py::TestPharaoh`:** `test_ge_arithmetic_mean_for_rho_ge_1` (P4 numerically);
`test_order_rises_with_disagreement_and_salience`. Dispatch: `test_pharaoh_opt_in` (flag flips model to
"PHARAOH" and `used_classC=True`). Class C.

## 06.B.6 Hierarchical two-layer fusion + correlation-aware BLUE/GLS weighting — `hierarchical.py`, `correlation.py`

### The two layers

```
Layer 1 (intra-workstream):  sensors/models  --FM-->  ONE group-level ExpertOutput per workstream
Layer 2 (cross-workstream):  group experts   --decide()-->  advisory decision     (SAME single function)

         tilt soil1 soil2            cam
            \   |   /                 |
             [geo group]          [fire group]        <- Layer 1 (correlation-aware if redundant)
                  \                   /
                   \                 /
                    ---> decide() <---                 <- Layer 2 (no second decision path)
```

Layer 1 (`fuse_group`) propagates: NF-3 uncertainty, intra-group agreement → consistency
(`c_group = clip(1 − 2·dispersion, 0, 1)`), reliability-weighted trust, and a **conservative class label**
— the **weakest-guarantee / most-novel member dominates** (`_CLASS_PRECEDENCE = [C, ADVISORY, DATA, B, A]`),
so Class-C novelty is **never hidden**. Layer 2 feeds the group experts to the **same `decide()`** — no
second decision path (`decide_hierarchical`).

**Why hierarchical:** it stops a crowd of correlated sensors inside one workstream from swamping an
independent workstream (double-counting), and keeps per-workstream reliability/consistency interpretable
for the operator. The math reuses the audited NF/FM primitives; nothing new is fabricated.

### Correlation-aware BLUE/GLS weighting (the decorrelation core)

Inside one workstream, several sensors are **redundant** (two soil probes on the same slope). Plain
weighting counts them as independent votes, so a correlated cluster swamps a genuinely independent source.
Fix (`correlation.py`): treat experts as correlated estimators and use the **minimum-variance linear
combination (Aitken/GLS = BLUE)**:

```
w*  proportional to  Sigma^-1 * 1

Sigma = outer(sd, sd) * R  +  ridge*I ,   sd_i = sqrt(1/effective_weight_i) ,   R = correlation matrix
```

A more trustworthy expert (higher effective weight) has lower variance. `R` is built by
`redundancy_matrix`: experts sharing a redundancy group get correlation `rho` (default 0.8), diagonal 1.

**SAFETY OVERRIDE (honesty > statistical optimality), carried verbatim:** pure BLUE can assign **negative
"hedging" weights**, which could pull the fused alarm **below every input** — unacceptable for a
life-safety monotone fusion (Rule 19). So the code **clips weights to be non-negative and renormalizes**,
documented as *a deliberate, conservative deviation from the unconstrained optimum.*

**Proved property (tests):** as the correlation `rho` between a redundant pair → 1, their **combined
weight → that of a single independent expert** of equal quality (the cluster stops over-counting).

**Golden cases, `test_hierarchical.py`:** `test_independent_matches_precision_weights`;
`test_redundant_pair_does_not_double_count` (independent expert out-weighs each redundant one, beats naive
1/3); `test_rho_to_one_pair_becomes_one_vote`; `test_weights_nonnegative` (no hedging weights);
`test_redundant_group_vs_flat_double_count` (3 identical geo alarms collapse to `p≈0.9`, not amplified);
`test_classC_propagates` / `test_class_precedence_weakest_wins` (transparency). Class B machinery.

## 06.B.7 The single decision function + the monotone shield — `decision.py`, `shield.py`

### One decision path (Bug #1 fix — PATCH A)

`TRINETRA_Corrected_Patches.md` **PATCH A (Bug #1, CRITICAL)** dissolved a ~10× threshold conflict (three
numbers — 0.5, 0.12, 0.048 — governing the same life-safety action). The resolution is **one function**
(`decision.py`), the single source of truth:

```
level  =  max( conformal_level(fused_risk, p*) ,  shield_floor(physics, sensors) )
```

### `p* ≈ 0.0476` — the Bayes-optimal cost-loss operating point

```
p* = C_FA / (C_FA + C_miss) = 5 / (5 + 100) = 0.0476          (config: C_FA=5.0, C_miss=100.0)
```

`[CONFIRMED]` in code: `common/config.py` defines `cost={C_FA:5, C_miss:100}` and `Config.p_star`
returns `C_FA/(C_FA+C_miss)`. Register **E-06** derives it from cost-loss decision theory; **E-07** ties
it to the Value-Score verification metric so the alarm cutoff and the score we optimize come from **one
coherent cost-loss model**. `conformal_level` maps risk to a level with cut points `(p*, 4p*, 10p*)` by
default, or **calibrated** cut points from `ws6_robust` when a calibration set exists (the honest conformal
story — see PATCH F / Bug #13: it is **risk-control with measured coverage + CIs**, *not* a fixed-90%
guarantee).

### The monotone shield (can only RAISE)

The shield (`shield.py`) is **post-posed** (applied after fusion), **monotone** (can only RAISE the level,
never lower it), **hard-coded** (no training), and **total** (always returns a defined Level). The
post-posed placement is exactly the convergence-preserving "shield after the learner" case of
**arXiv 1708.08611**.

```
floor = GREEN
FS < 1                                            -> raise to ORANGE
tilt_rate > 5 deg/day  AND  nodes_agree >= 2       -> raise to RED
rain_24h > 150 mm  AND  high_susceptibility        -> raise to ORANGE
GLOF lake_drop  AND  downstream_stage_jump         -> raise to RED
fire_multi_node (smoke+heat >=2 nodes)             -> raise to ORANGE
```

**Crucially, a single faulty/uncorroborated node CANNOT reach RED** — spatial corroboration (`≥2 nodes`)
is required. The `P_f ≥ 0.5` physics gate is a **shield trigger**, never a probability competing with `p*`
(PATCH A).

**Golden cases:** `test_fusion.py::TestShield` (single node cannot RED; corroborated tilt reaches RED;
`FS<1 ⇒ ORANGE`; nothing ⇒ GREEN). `test_decision.py`: `test_shield_can_only_raise` (GREEN risk + `FS<1`
⇒ ≥ORANGE); `test_bands_monotone` (conformal bands at `p*=0.0476`); `test_failsafe_uncertain_when_no_experts`
(abstain + escalate, never silent); `test_uncertain_on_high_conflict`; `test_always_advisory`;
`test_classC_flagged_when_pharaoh_on`.

### Fail-safe / advisory behaviour (Rule 19)

`decide()` always returns `advisory=True`. When conflict-aware uncertainty `U* > uncertain_threshold`
(0.6) or there are no available experts or drift is flagged, it sets `uncertain=True` (abstain + escalate
to a human) — **but it is never silent**. A provisional conformal set widens with `U*`, and a reliability
flag (High/Medium/Low/Unreliable) is derived from `U*`. `used_classC` propagates to the `Decision` for
transparency.

## 06.B.8 End-to-end picture

```
raw multimodal evidence x
   |-> geo gate (FS, Iverson, Fukuzono, Caine)  -> ExpertOutput(geo_phys, Class A)
   |-> fire gate (Heskestad/Byram/graybody + ND soft) -> ExpertOutput(fire_phys, Class A)
   |-> supervised/anomaly ensemble              -> ExpertOutput(..., Class DATA)
   |-> offline-RL policy (advisory, behind OPE gate) -> ExpertOutput(..., advisory)
            |
   [Layer-1 group fusion]  FM-1 / GMF / PHARAOH, correlation-aware BLUE if redundant
            |
   fuse() -> p, U*(NF-3), salience(NF-4), used_classC
            |
   conformal_level(p, p*=0.0476)  --\
                                     max( . , . )  = level     <- shield can ONLY raise
   shield_floor(physics, sensors) --/
            |
   Decision{ level, risk, conformal set, reliability, shield_reason, contributions, advisory=True }
            |
   operator (human) -> CAP/SACHET  (NEVER autonomous; Rule 19)
```

## 06.B.9 Honest validation status — what is unvalidated / flag-gated, and gate G4

This section is the honest core and must not be softened.

- **FM-1 is the only fully-implemented fuser.** FM-2..FM-6 are interface stubs with FM-1 fallback — **not
  implemented beyond the interface** (`fusion_models.py` docstring). `[CONFIRMED]` by reading the code.
- **PHARAOH (Class C) is default-OFF.** Its properties P1–P7 are **derived on paper, not fully numerically
  verified**; the flag **may not default ON** until they are (gate G4, `LLD §8`). The anti-complacency
  bias **raises false-alarm risk by construction** — an honest cost, not a free lunch.
- **ND-1..ND-3 fire features (Class C) are default-OFF**, `[coeff-verify]` unresolved, enter only as soft
  features with a Class-A fallback.
- **Calibrated members ≠ calibrated ensemble (arXiv 2101.05397).** `ws1_physics/fusion_design.md §1`
  states it as the first design principle: a calibrated ensemble *cannot beat the average of its calibrated
  members*, so the **fused output must itself be post-hoc calibrated** (temperature/isotonic), measured by
  a **proper score** (log-loss/Brier/CRPS; **ECE is a dev diagnostic only** — biased estimators, 2408.02841
  / 2203.07835). This calibration step is **designed, not yet built or measured.**
- **The hierarchical fusion is strong for decorrelation + interpretability but NOT theoretically optimal.**
  BLUE/GLS is optimal only under its Gaussian-variance + known-correlation assumptions, and the
  non-negativity clip **deliberately deviates from the unconstrained optimum** for safety. Against
  **joint-dependence** fusers (copula / full-covariance) or **learned-attention** fusers, it is a
  conservative, interpretable approximation — `[LIKELY]` suboptimal in raw discrimination, `[CONFIRMED]`
  superior in auditability and double-count resistance. We do not claim optimality.
- **Conformal coverage is risk-control, not a guarantee** (PATCH F / Bug #13): split-CP's marginal
  guarantee is exchangeability-dependent and degrades under missing sensors / feedback shift / temporal
  dependence (the on-region competitor **arXiv 2603.15681** itself measured coverage falling to 82.9%
  overall and 45–59% in high-risk zones). We report **measured** marginal and per-zone coverage with CIs
  and use online adaptive CP (ACI/AgACI).

**Gate G4 (fusion stability / reliability-gating), `LLD §13` + `§8` acceptance:** coefficient stability
under resampling; degraded-modality down-weighting demonstrated; shield-floor monotonicity; PHARAOH P1–P7
numerically verified **before** the flag may default ON; **nothing claimed to beat FM-1 without the G2
real-win gate** (spatial-CV + baselines + bootstrap CIs). The tests in `trinetra/tests/fusion/` exercise
the *correctness* side of G4 (down-weighting, monotonicity, bounded residual, double-count fix); the
*skill* side (does any fuser actually beat FM-1?) is **not measured** and is pre-registered, not claimed.

---

# PART C — VALIDATION (correctness tests, NOT skill measurements)

> **Read this first.** Everything below is a **correctness** test — it proves the code computes the
> equation it claims to compute, preserves an invariant, or enforces a safety rule. **None of it measures
> forecasting skill, recall, false-alarm rate, lead time, or any performance number for TRINETRA.** Those
> are **not measured** (`_CANON.md §0`). The repo-level fact `[CONFIRMED]`: `python run_tests.py` →
> **128 tests OK**; `python scripts/ci_gates.py` → **ALL 6 CI GATES PASSED** (numpy core; stdlib+numpy
> only, no torch/scipy).

## 06.C.1 Physics golden-case tests (`trinetra/tests/physics_golden/`, gate G1)

| Test file :: case | What it proves (correctness only) |
|-------------------|-----------------------------------|
| `test_geophys.py::test_saturated_limit` | `σ_s→0` FS equals the saturated form exactly (12 dp) — the suction guard |
| `test_geophys.py::test_monotonic_in_suction` | FS strictly increases with suction (PATCH C sign fix holds) |
| `test_geophys.py::test_decreasing_in_pore_pressure` | FS decreases as pore pressure rises |
| `test_geophys.py::test_ierfc_at_zero` | `ierfc(0)=1/√π` (special-function correctness) |
| `test_geophys.py::test_transient_zero_at_t0` | Iverson transient head is 0 at `t=0` |
| `test_geophys.py::test_slope_only_through_D1` | **the bug-guard**: slope enters ONLY via `D1=D0/cos²β`; NOT the buggy `·cos²β` form |
| `test_geophys.py::test_recover_tf_alpha2` | Fukuzono `α=2` recovers `t_f` on a clean 1/v line, `r²>0.999` |
| `test_geophys.py::test_exceedance_direction` | Caine I–D exceedance direction + ratio ordering |
| `test_iverson_multipulse.py` (×4) | single-step = `transient_head`; finite-pulse recovery after rain stops; superposition linearity; intensity monotone |
| `test_fukuzono_ci.py` (×3) | noiseless `se≈0`; noise widens the interval and it **brackets the truth**; recency path stays sane |
| `test_firephys.py::TestEstablished` (×4) | flame height ↑ with Q; Strouhal ↓ with size; gray-body round-trip (T⁴); Byram regime ordering |
| `test_firephys.py::TestNovelND` (×2) | aliasing identity/undersampling math; ND-2 uncertainty grows as smoke thickens (fail-safe) |
| `test_firephys.py::TestFireGateFlagGating` (×3) | **Class-C OFF by default**; flips ON only with the flag; wind regime lowers consistency |

## 06.C.2 Fusion & decision tests (`trinetra/tests/fusion/`, `tests/decision/`, gates G4 / G3)

| Test file :: case | What it proves (correctness only) |
|-------------------|-----------------------------------|
| `test_fusion.py::TestPharaoh` | power mean `≥` arithmetic mean for `ρ≥1` (P4); order rises with disagreement × salience |
| `test_fusion.py::TestFuseDispatch` | **default = FM-1, not Class-C**; PHARAOH is opt-in; no experts ⇒ `U*=1` (max uncertainty) |
| `test_fusion.py::TestShield` | single node cannot RED; corroborated tilt reaches RED; `FS<1⇒ORANGE`; nothing⇒GREEN |
| `test_gmf.py` | gate sums to 1; no head ⇒ 0 residual; **residual hard-bounded to ±cap** even for a `±999` head; numpy-export stays bounded; GMF-with-PHARAOH-off is Class B |
| `test_hierarchical.py` | independent ⇒ precision weights; **redundant pair doesn't double-count**; `ρ→1` ⇒ one vote; non-negative weights; class precedence (weakest wins); end-to-end through the single `decide()` |
| `test_adapters.py` | **deepfake reliability hard-capped at 0.4**; geo_pinn is Class B; prob clamped; unknown source rejected; low-trust deepfake can't dominate the decision |
| `test_decision.py` | conformal bands monotone at `p*=0.0476`; **shield can only raise**; always advisory; fail-safe uncertain when no experts; uncertain on high conflict; Class-C flagged when PHARAOH on; dict round-trip |

## 06.C.3 What these tests deliberately do NOT prove

- They do **not** prove the FS/Iverson/Fukuzono/Caine thresholds predict real landslides, nor that the fire
  equations detect real fires. Those require field data, spatial-block CV (mandatory, **arXiv 2608.22293**),
  baselines (GB/decision-tree/persistence), and bootstrap CIs — the **G2 admission gate** (PATCH I). **None
  of that is run here.** The headline negative result from the literature cluster (random CV overstates
  skill; a deep model that doesn't beat a GB baseline is reported as such) stands as a *warning the
  evaluation is not yet valid*, not a TRINETRA measurement.
- They do **not** measure whether any fuser beats FM-1. That is the G2 real-win gate and is **not measured**.
- The PHARAOH P1–P7 properties are only **partially** checked numerically (P4 + order monotonicity); full
  P1–P7 numeric verification is a build-phase prerequisite (G4) before the flag may default ON.

---

## 06.D Chapter provenance

Written strictly from the sources read (every file opened with the read tool): `docs/_CANON.md`,
`docs/00_README_START_HERE.md`, `DESIGN/LLD.md`, `DESIGN/COMPONENT_DESIGN.md`,
`TRINETRA_MetaFusion_Design.md`, `TRINETRA_Corrected_Patches.md`, `analysis/08_equations_register.md`,
`ws1_physics/model_set_decision.md`, `ws1_physics/fusion_design.md`,
`ws1_physics/established_formula_inventory_P21.md` (Byram EF-13 check),
`ws5_fusion/novel_aggregation_operator_P22.md`, `ws5_fusion/novel_formulas_P22.md`, the code under
`trinetra/src/trinetra/ws1b_geophys/`, `ws1a_firephys/`, `ws5_fusion_rl/`, `common/config.py`, and the
tests under `trinetra/tests/physics_golden/`, `tests/fusion/`, `tests/decision/`. Every equation is quoted
as it appears in the code or the equations register. No equation, paper, or number was invented; all
performance figures are source-reported (with arXiv ID) or "not measured."
