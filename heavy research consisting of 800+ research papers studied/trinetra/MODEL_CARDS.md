# TRINETRA — Deep Model Cards

Honesty contract for every trainable model. All models are ADVISORY: they output a calibrated probability
that becomes an `ExpertOutput` (via `ws5_fusion_rl.adapters.deep_expert`) feeding the single decision
function `ws5_fusion_rl.decide`. None issues an alert (R19). None may have its skill advertised until
`trinetra.deep.train.admit_model` returns `admitted=true` on spatial-CV against mandatory baselines (R16).
Novelty is a search claim only until a prior-art check is logged (R21).

Legend — Class: **A** deterministic physics · **B** physics-informed/regularized learning · **data**
data-driven · Class-**C** novel terms are flag-gated OFF with an A/B fallback (R20).

---

## 1. GeoPINN — physics-informed slope hydrology  ·  Class B (physics-regularized)
- **File:** `src/trinetra/deep/geo_pinn.py` · **WS:** ws1b_geophys
- **In:** `(Z, t, rainfall, static[c',φ,γ,z,β,susceptibility])` · **Out:** landslide probability, ψ field, FS
- **Training signal:** data BCE (where failure labels exist) + Richards/Iverson PDE residual (label-free) +
  "FS<1 ⇒ high risk" hinge. Slope enters ONLY via `D1 = D0/cos²β` (bug-guard).
- **Use:** corroborating evidence alongside the deterministic FS/Iverson gate, which still runs at inference.
- **Limits:** linearized 1-D diffusion; not a substitute for the hard gate; needs site soil params.

## 2. FireSmokeNet — spatiotemporal fire/smoke  ·  Class A-aux + data
- **File:** `src/trinetra/deep/fire_cnn.py` · **WS:** ws1a_firephys / ws4_cctv
- **In:** clip `(T,C,H,W)` · **Out:** multi-label {fire, smoke} prob + flicker-Hz estimate
- **Training signal:** multi-label BCE + (optional, Class-C, default OFF) Strouhal flicker consistency
  `f≈1.5/√D`. Temporal GRU suppresses single-frame glint/headlight false alarms.
- **Limits:** ND flicker term unverified novelty (R21) → stays OFF; Heskestad/Byram gate owns the physics.

## 3. EODownstream — frozen EO foundation encoder + head  ·  Class data
- **File:** `src/trinetra/deep/eo_encoder.py` · **WS:** ws1b_eo
- **In:** multispectral patch `(C,H,W)` · **Out:** hazard/change probability
- **Training signal:** encoder FROZEN (budget + anti-overfit); only the small head trains (BCE).
- **Limits:** chosen encoder (FM weights vs timm substitute) MUST be recorded in the eval report.

## 4. DeepAnomaly — TCN AE + Deep-SVDD + forecast  ·  Class data
- **File:** `src/trinetra/deep/anomaly_deep.py` · **WS:** ws8_anomaly
- **In:** telemetry window `(C,T)` · **Out:** scalar anomaly score (→ normalized prob for the gate)
- **Training signal:** trained on NORMAL only; reconstruction + one-step forecast + SVDD distance. Causal
  convs ⇒ no look-ahead (G6).
- **Limits:** unsupervised threshold must be calibrated per site; numpy ensemble is the always-on fallback.

## 5. AuthenticityNet — two-stream deepfake detector  ·  Class data, LOW trust
- **File:** `src/trinetra/deep/deepfake_net.py` · **WS:** ws2_deepfake
- **In:** image `(C,H,W)` · **Out:** p_fake (prob media is manipulated)
- **Training signal:** BCE over RGB + 2D-FFT log-magnitude streams.
- **Limits:** reliability HARD-CAPPED at 0.4 in the adapter; can NEVER gate a life-safety alert (R19).

## 6. CQLPolicy — conservative offline-RL alarm policy  ·  Class advisory
- **File:** `src/trinetra/deep/offline_rl.py` · **WS:** ws5_fusion_rl
- **In:** state `(d,)` · **Actions:** HOLD / WATCH / ALARM · **Out:** Q-values, shielded action, action probs
- **Training signal:** CQL (Bellman + conservative penalty); `gamma=0` = one-step bandit. Offline only.
- **Deploy gate:** `ws5_fusion_rl.ope_admission` (positivity + ESS + value ≥ baseline). If not admitted →
  keep `RuleBaselinePolicy` (R19 fail-safe). Action is always raised to the shield floor (safety-upward).

## + GMFHead — learned meta-fusion residual  ·  Class B
- **File:** `src/trinetra/deep/fusion_head.py` · **WS:** ws5_fusion_rl
- **In:** `[base, dispersion, salience]` · **Out:** bounded residual on the gated-mixture base
- **Safety:** residual hard-clipped to ±cap (physics-anchored base can't be dominated). Exported to a
  pure-numpy closure (`gmf_head_numpy.json`) so the offline gateway runs it without torch
  (`ws5_fusion_rl.load_numpy_head`).

---

### Admission gate (applies to all) — `trinetra.deep.train.admit_model`
Spatial-block CV → beat climatology AND numpy-logistic baselines on the cost-loss with a bootstrap CI whose
lower bound clears zero (`eval.real_win`). `eval.ReportGuard` refuses to emit any headline number otherwise.
Verification status of this layer: all files `py_compile`-clean; numpy core 93 tests green. Runtime training
is executed by the user on Kaggle (torch/GPU absent in the authoring sandbox).
