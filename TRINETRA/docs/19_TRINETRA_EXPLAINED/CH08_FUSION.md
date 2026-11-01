# CH08 — META-FUSION AND AVERAGING

**Simple me samjho:** panchayat me kai gawah hain. Jo zyada bharosemand hai, jo physics se mel khaata hai, aur jo kam confused hai, uski baat ka wazan
zyada. Agar gawah aapas me bahut ladte hain, to sarpanch kehta hai "abhi pakka nahi, upar bhejo" (human review).

## Exact rules (code: ws5_fusion_rl/, configs/fusion.json)
| Step | Formula | Class | Params |
|---|---|---|---|
| Effective weight | w̃ᵢ = aᵢ rᵢ cᵢ exp(−uᵢ/τ) | B | τ = 0.5 |
| Pool (FM-1, default) | p̂ = Σ w̃ᵢ pᵢ / Σ w̃ᵢ | B | — |
| Conflict uncertainty | U* = Σ w̄ᵢ uᵢ + λ √Σ w̄ᵢ (pᵢ − p̄)² | B | λ = 0.3 |
| Salience | S = max rᵢ cᵢ pᵢ | B | — |
| Cost threshold | p* = C_FA/(C_FA + C_miss) = 0.0476 | A | 5, 100 |
| Level | max(L(p̂; p*, 4p*, 10p*), shield floor) | B | cuts ad hoc (G-12) |
| Abstain | uncertain if U* > 0.6, no experts, or drift | B | 0.6 |
| Calibration | p_cal = σ(logit p / T), T fitted on other folds | A | cross-fit |
| Media trust | r′ = r (1 − p_fake) on media experts | B | — |

**Missing input:** a = 0 → weight 0; the rest carry the decision; if all are missing → uncertain, never silent.

## Worked example (computed with the repo code, docs/07 §A; not a result)
CCTV p 0.8 u 0.2 r 0.9 · sensor stream p 0.6 u 0.1 r 0.8 · media p 0.1 u 0.5 r 0.4 → weights 0.603, 0.655, 0.147 → p̂ = 0.6335,
U* = 0.2465, S = 0.72 → RED (≥ 10p* = 0.476), pred set [ORANGE, RED]. Without the media expert p̂ = 0.6959. PHARAOH (if ON): ρ = 1.296, p = 0.6456.

## Averaging techniques compared
| Rule | Formula | Permutation inv. | One expert bounded? | Missing input | Correlated experts | Status |
|---|---|---|---|---|---|---|
| FM-1 (chosen) | Σw̃p/Σw̃ | ✓ | ✓ (weighted mean ∈ [min, max]) | ✓ weight 0 | ✗ double-counts (use BLUE) | unit-tested |
| Plain mean | Σp/n | ✓ | ✗ an outlier pulls | ✗ | ✗ | argued |
| Softmax weights | w ∝ e^{s/T} | ✓ | depends on T | ✓ | ✗ | argued |
| Inverse-variance | w ∝ 1/σ² | ✓ | ✓ | ✓ | ✗ | needs σ |
| Log-linear pool | ∝ Π p^w | ✓ | ✗ p ≈ 0 vetoes an alarm (unsafe) | ✓ | ✗ | argued |
| Product of experts | ∝ Π p | ✓ | ✗ overconfident | ✗ | ✗ | argued |
| Bayesian model avg | Σ P(M|D) p_M | ✓ | collapses to one model | ✓ | ✗ | not used |
| Stacking / GMF | learned g(p) + bounded residual | ✓ | residual capped 0.1 | ✓ | partly | code, needs paired data |
| BLUE / GLS | w ∝ Σ⁻¹1 | ✓ | ✓ (non-neg clipped) | ✓ | ✓ | unit-tested |
| Dempster-Shafer | belief masses | ✓ | conflict paradox | ✓ | ✗ | not used |
| Covariance intersection | ω-convex | ✓ | ✓ | ✓ | ✓ (unknown corr.) | not used |
| Median / trimmed | robust | ✓ | ✓ | ✓ | — | compared in fusion cache |
| PHARAOH (C, OFF) | power mean ρ ≥ 1 | ✓ | never below mean (proved) | ✓ | ✗ | experiment pending |
**Why FM-1:** bounded, missing-safe, cheap, interpretable. Its weakness (correlated experts) is covered by BLUE for redundant sensors.
**Experiment:** `kaggle/build_fusion_cache.py` compares FM-1, PHARAOH, median and max over 5 seeds (synthetic pairing; real OOF pending).

**Self-check:** log-linear pool kyun unsafe? (Ek expert 0 bole to alarm mar jaata hai.) U* kab badhta hai? (jab experts disagree karein ya khud uncertain hon.)
<!-- END -->
