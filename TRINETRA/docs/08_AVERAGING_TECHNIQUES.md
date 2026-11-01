# 08 — AVERAGING TECHNIQUES
**What the code uses:** FM-1, a *reliability × consistency × exp(-uncertainty/τ)* weighted **arithmetic mean**
(`fusion_models.fm1_precision_weighted`). Optional: PHARAOH adaptive power mean (Class C), GMF bounded residual,
and BLUE/GLS `w ∝ Σ⁻¹1` for correlated sensors (`correlation.py`).

**FM-1 weaknesses:** (1) correlated experts double-count unless `correlation.py` is used; (2) an arithmetic
mean dilutes one strong true alarm (PHARAOH targets this); (3) uncalibrated `p_i` break it, so calibrate first;
(4) τ is a hand choice (0.5); (5) it has no asymmetric cost, which is handled later by p* thresholds.

| Rule | Formula | Good at | Weak at |
|------|---------|---------|---------|
| Weighted arithmetic (FM-1) | $\sum w_i p_i$ | simple, bounded, missing-safe | dilution, correlation |
| Weighted geometric / log-linear pool | $\propto \prod p_i^{w_i}$ | sharp agreement | one p≈0 vetoes the alarm (unsafe) |
| Softmax weights, temperature T | $w_i \propto e^{s_i/T}$ | smooth selection | T tuning |
| Inverse-variance | $w_i \propto 1/\sigma_i^2$ | optimal if independent + Gaussian | needs variances |
| Product of experts | $\propto \prod p_i$ | AND-logic | overconfident |
| Bayesian model averaging | $\sum P(M_k|D) p_k$ | principled | collapses to one model |
| Stacking / GMF head | learned $g(p_1..p_n)$ | data-driven | needs paired data (we have none) |
| Mixture-of-experts gating | $\sum g_i(x) p_i$ | context-aware | needs data |
| Dempster-Shafer / subjective logic | belief masses | explicit ignorance | conflict paradox |
| Covariance intersection | $\omega$-convex combo | unknown correlation safe | conservative |
| Copula fusion | joint via copula | dependence-aware | needs data |
| Hedge (exp-weights online) | $w_i \leftarrow w_i e^{-\eta \ell_i}$ | adapts online (≈ NF-2) | needs outcome feedback |
| Median / trimmed mean | robust | outlier expert | few experts |
| Conformal aggregation | sets per expert, then combined | coverage | wide sets |
| Decision-theoretic | alarm iff $\hat p \ge p^*$ | asymmetric cost (already used) | needs calibrated $\hat p$ |
| PHARAOH (repo, Class C) | power mean, $\rho = 1+\kappa D S$ | never below the arithmetic mean when $\rho \ge 1$ | unvalidated |

**New technique?** Not derived this session (time-box). The repo already proposes PHARAOH. The proper next step
is an **experiment, not a new formula**: run FM-1 vs PHARAOH vs median on the same fused validation cache (5 seeds)
and compare value score, miss rate at fixed FA, and ECE. Adopt PHARAOH only if it wins beyond the seed-to-seed spread.
Toggle with `configs/fusion.json` `"operator": {"pharaoh": true}` (no code edit). Novelty: not verified.
<!-- END -->
