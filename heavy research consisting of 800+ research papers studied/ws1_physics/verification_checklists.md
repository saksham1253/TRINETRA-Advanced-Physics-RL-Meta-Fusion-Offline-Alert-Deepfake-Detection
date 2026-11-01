# ws1_physics/verification_checklists.md — per-model verification (hand-checks)

Phase P7 · WS1a · RESEARCH-ONLY. For every admitted model: dimensional consistency, limiting-case
behaviour, and (Layer 2) reduction-to-parent — hand-checked. "PASS" = checked on paper this phase; items
needing primary-source confirmation are flagged [coeff-verify]; all need expert review before external use.

## Universal checks applied
- [x] Dimensional homogeneity of every equation (fire correlations use the standard dimensional kW–m–K
      convention; constants carry hidden units → tagged [coeff-verify]).
- [x] Monotonic/limit sanity (e.g. temperature rise ↓ with height and distance; flux ↓ as $1/R^2$).
- [x] Layer-2 reduction to parent in a stated limit (shown in each B-xx doc §5).

## Layer 1
| Model | Dim. check | Limit check | Notes |
|-------|-----------|-------------|-------|
| EF-01 | PASS (m) | $L\to-1.02D$ as $\dot Q\to0$ → model invalid at low $Q^*$ (documented weakness, not an error) | coeff [coeff-verify] |
| EF-02 | PASS (kW) | $\dot Q\to0$ as $t\to t_0$; grows unbounded → capped by fuel/vent limit (regime) | α [coeff-verify] |
| EF-03 | PASS (K; kW-conv.) | $\Delta T_0\to0$ as $z\to\infty$ ($-5/3$); singular at $z=z_0$ (near-field excluded) | coeff 9.1/3.4 [coeff-verify] |
| EF-04 | PASS | plume regime recovers EF-03 exponent $-5/3$ ✓ | regime seams |
| EF-05 | PASS | $\Delta T,U\downarrow$ with $r$; near-field plateau for small $r/H$ ✓ | coeff [coeff-verify] |
| EF-06 | PASS (kW/m²) | $\dot q''\to0$ as $R\to\infty$ ($1/R^2$); diverges as $R\to0$ (near-field excluded) ✓ | $\chi_r$ varies |
| EF-07 | PASS | $I\to I_0$ as $\sigma L\to0$; $I\to0$ as $\sigma L\to\infty$ ✓ | $K_m$ wavelength/fuel-dep |
| EF-08 | PASS (Hz) | $f\to\infty$ as $D\to0$ (small-source limit, unphysical extreme) ✓ | coeff 1.5 [coeff-verify] |
| EF-09 | PASS | $L_{meas}\to L_{bb}(T)$ as $\varepsilon\to1,\tau_{atm}\to1$ ✓ | ε,τ unknown in field |
| EF-10 | PASS ($s^{-1}$) | $dT_e/dt\to0$ as $T_e\to T_g$ (equilibrium) ✓ | RTI/τ uncertain for cheap sensors |
| EF-11 | PASS | $R\uparrow$ with wind/slope factors; $R\to0$ as $Q_{ig}\to\infty$ ✓ | empirical factors |
| EF-12 | PASS | $\dot m\uparrow$ with height ($z^{5/3}$) ✓ | far-field only |

## Layer 2 (reduction-to-parent verified)
| Model | Dim. check | Reduction to parent | Falsifiable? |
|-------|-----------|---------------------|--------------|
| B-06 | PASS ($1/\tau$ in s⁻¹; kernel ∫=1) | → EF-05/EF-10 as $\tau\to0,t_d\to0,\eta\to0$ ✓ (doc §5) | yes — activation-time error vs parent (§7) |
| B-05 | PASS (Hz; score dimensionless) | → EF-08 as $f_s>2f_{0,max}$ (alias map → identity) ✓ (doc §5) | yes — alias-map + separation vs raw-FFT (§7) |
| B-01 | PASS (px; $\sigma\ell$ dimensionless) | → EF-01 as $\sigma\to0,\theta\to0$, calib known ✓ (doc §5) | yes — obscured-case error vs EF-01 (§7) |
| B-02 | PASS (temperature; posterior density) | → EF-03 as priors→δ, $s\to0$ (exact algebraic identity) ✓ (doc §5) | yes — $g(\zeta)$ collapse + coverage (§7) |

## Independent re-derivation check (second agent, 2026-10-09) — PASS
A separate verification pass re-derived all four Layer-2 models from scratch (algebra, dimensions, reduction-
to-parent only; not real-world validity). **Verdict: all four internally CORRECT, no errors.** Specifically
confirmed: B-06 $\int_0^r r'^{5/6}dr'=r^{11/6}/(11/6)$, $\sqrt u/\mathrm{RTI}=s^{-1}$, delta-limit;
B-05 alias fold into $[0,f_s/2]$ + identity at Nyquist; B-01 px = (f/R)·m and $\sigma\ell$ dimensionless +
clear-air reduction; B-02 exponent $2/3-\tfrac25\cdot\tfrac53=0$ exact change of variable + posterior→EF-03.
Two harmless interpretive caveats recorded (not errors): (i) B-06's three limits must be read SEQUENTIALLY
(τ→0 before t_d→0) for the clean $T_s\to T_g$ statement; (ii) B-02 is independent of EXPLICIT $\dot Q_c$ but
$\zeta$ still embeds $\dot Q_c$ (standard nondimensionalization). Both are noted in the respective docs'
spirit; no change to correctness.

## Open verification items (carried to gate)
- [coeff-verify] confirm every tagged constant against the PRIMARY source (Heskestad 1983, Alpert 1972,
  McCaffrey 1979 NBS IR, Cetegen & Ahmed 1993, Mulholland, Rothermel 1972) — not fetchable this session.
- Independent re-derivation of the four Layer-2 models by a second pass (planned; §P7). B-02's exponent
  cancellation ($2/3-2/5\cdot5/3=0$) is the one most worth an independent recheck — rechecked here: ✓.
- Expert (fire-science / heat-transfer) review of all derivations before any external use.
