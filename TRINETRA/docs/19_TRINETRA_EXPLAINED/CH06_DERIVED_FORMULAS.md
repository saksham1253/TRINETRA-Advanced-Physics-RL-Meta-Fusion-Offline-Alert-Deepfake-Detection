# CH06 — DERIVED FORMULAS (Class B / C dossiers)

## F6 · ΔFS, the rain-driven drop in factor of safety  [B]
- **Final:** ΔFS = FS_dry − FS_wet = γ_w ψ tan φ′ / (γ z sin β cos β)
- **Parent:** infinite-slope FS (A), u_w = γ_w ψ (A).
- **Derivation:**
  1. FS(u) = [c′ + (γz cos²β − u) tanφ′] / (γz sinβ cosβ). *Pakadne wali taakat ÷ girane wali.*
  2. FS_dry = FS(0), FS_wet = FS(γ_w ψ). *Same slope, sirf paani ka fark.*
  3. Subtract: c′ and γz cos²β tanφ′ cancel. *Jo dono me same hai, wo hat jaata hai.*
  4. ΔFS = γ_w ψ tanφ′ / (γz sinβ cosβ). *Bacha sirf paani ka asar.*
- **Dimensions:** (kN/m³ · m) / (kN/m³ · m) = dimensionless ✓. **Limits:** ψ → 0 gives ΔFS → 0 ✓; β → 90° gives a bigger drop for the same ψ (cos β → 0).
- **Code:** `data_adapters/build_geo.py` (`dfs`), RL hazard in `env_landslide.py`.
- **Validate / falsify:** event days must have larger ΔFS than control days. **Tested:** ROC-AUC 0.750 on 184 real events (results/geo_large). C3.
- **New assumption:** none beyond ψ0 = 0. Novelty not verified (it is a direct consequence of A).

## F7 · Back-analysed cohesion  [B, standard practice]
- **Final:** c′_bc = FS_t · γz sinβ cosβ − γz cos²β tanφ′, with FS_t = 1.2, clipped ≥ 0.
- **Derivation:** set FS(u = 0) = FS_t and solve the FS equation for c′. *Slope khada hai, to sukhe me FS ≥ 1 hona chahiye.*
- **Limit:** gentle slopes (tanφ′/tanβ ≥ 1.2) give c′_bc = 0, so FS_dry > 1.2 there; that is why F6 (not 1.2 − FS) drives the RL hazard (bug B-24).
- **Tested:** repo geo gate with c′_bc reaches AUC 0.712 (large) / 0.762 (small tile). **Assumption that makes it work:** FS_t = 1.2.

## F8 · GLOF power laws  [B, fitted]
- V = a A^b fitted on HMAGLOFDB: b = 1.13 (95% CI 0.71-1.50), R²(log) 0.72, n = 21. Q_p = c V^d: d = 0.54 (0.36-0.79), R² 0.36, n = 31.
- **Falsify:** an exponent CI that excludes the published value on matched data. The published constants are only in memory in the repo, so **not compared**.
- **Gap:** Froehlich and Costa-Schuster need breach/dam height, which is absent, so they are untestable.

## F10 · NF-1..NF-4 and U*  [B, design]
NF-1 c_i = exp(−(p_i − φ)_+² / 2σ²), σ = 0.25. It penalises claiming more alarm than physics allows. NF-2 reliability update with forgetting 0.9, floor 0.1
and drift ×0.5. NF-3 U* = Σ w̄u + λD, λ = 0.3. NF-4 S = max r c p. Tested by unit tests only (C2).

## F11 · PHARAOH  [C, OFF]
F_ρ = (Σ w̄ p^ρ)^(1/ρ), ρ = clip(1 + κ D S, 1, 8), κ = 2. **Proven on paper:** for ρ ≥ 1 the power-mean inequality gives F_ρ ≥ arithmetic mean
(never under-warns relative to FM-1). **Argued:** it bends toward "max" only when a credible alarm exists. **Not tested on real data;** default OFF.

## F14 · RL hazard  [B + ASSUMPTION]
P(fail today) = σ(α + β ΔFS). β = 24.3 is fitted on the real case-control table; the slope is consistent under case-control, the intercept is not.
α is chosen so a never-acting slope fails with 30% per season (ASSUMPTION, `--season-fail`).

## Honest gaps panel
| Gap | Where | Fix proposed | Status |
|---|---|---|---|
| Assumed soil gave FS < 1 when dry | build_geo, shield | back-analysis F7 + ΔFS F6 | fixed (B-23, B-24) |
| Caine constant 14 vs 14.82 (memory) | caine.py | verify Caine (1980) page/eq; refit locally | open (bug report #15) |
| Level cuts p*, 4p*, 10p* ad hoc | decision.py | calibrate with CRC | open (G-12) |
| RL intercept not identifiable from case-control | rl_env_eval | need event frequency data | stated as ASSUMPTION |
<!-- END -->
