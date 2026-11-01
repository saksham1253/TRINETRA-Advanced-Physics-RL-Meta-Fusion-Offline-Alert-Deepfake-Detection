# 07 — RL + META-FUSION (code se, Hinglish)

## A. Meta-fusion (exactly as in `ws5_fusion_rl/`)
**Inputs:** a list of `ExpertOutput` with `p` (calibrated prob 0-1), `u` (uncertainty 0-1), `c` (physics consistency,
NF-1), `r` (reliability, NF-2), `available`. Missing expert means `available=False`, so its weight is 0 (graceful).

**Effective weight (nf.py):** $\tilde w_i = a_i \, r_i \, c_i \, e^{-u_i/\tau}$, with $\tau = 0.5$ (`configs/fusion.json`).

**FM-1 (default, Class B):** $\hat p = \sum_i \tilde w_i p_i \,/\, \sum_i \tilde w_i$.

**NF-3 uncertainty:** $U^* = \sum_i \bar w_i u_i + \lambda D$, where $D=\sqrt{\sum_i \bar w_i (p_i-\bar p)^2}$ and $\lambda=0.3$.

**NF-4 salience:** $S = \max_i r_i c_i p_i$.

**PHARAOH (Class C, OFF):** $F_\rho = (\sum_i \bar w_i p_i^\rho)^{1/\rho}$ with $\rho = \mathrm{clip}(1+\kappa D S, 1, 8)$ and $\kappa=2$.

**Decision:** level = max(conformal_level($\hat p$; p*, 4p*, 10p*), shield floor); `uncertain` if $U^*>0.6$.

| Symbol | Meaning | Range |
|--------|---------|-------|
| $p_i$ | expert probability | [0,1] |
| $u_i$ | expert uncertainty | [0,1] |
| $c_i$ | physics consistency (NF-1: penalises p above physics) | [0,1] |
| $r_i$ | reliability (NF-2: exponential forgetting, drift penalty) | [0.1,1] |
| $\tau, \lambda, \kappa$ | temperature, conflict weight, PHARAOH order gain | 0.5, 0.3, 2 |
| p* | $C_{FA}/(C_{FA}+C_{miss}) = 5/105$ | 0.0476 |

**Tiny example (computed by running the code, 2026-10-31, not hand-made):** CCTV p=0.80 u=0.20 r=0.9; IoT
p=0.60 u=0.10 r=0.8; deepfake p=0.10 u=0.50 r=0.4 (all c=1).
Weights are 0.6033, 0.6550, 0.1472. FM-1 gives **p̂ = 0.6335**, U* = 0.2465, S = 0.72. PHARAOH (if ON) gives
ρ = 1.296 and p = 0.6456. Decision is **RED** (0.6335 ≥ 10p* = 0.476), pred_set [ORANGE, RED], reliability MEDIUM,
uncertain = False. If the deepfake expert goes missing, FM-1 gives p̂ = 0.6959.
Hinglish: deepfake expert ka bharosa kam (0.4) aur shak zyada (0.5) hai, isliye uska weight sirf 0.15 hai. Final
risk CCTV aur IoT ke beech aata hai.

**Calibration:** temperature scaling in `deep/train.py` (`TemperatureScaler`), isotonic/Platt in `eval/calibration.py`.
Conformal sets come from `ws6_robust/conformal.py`. **Time alignment:** NOT FOUND IN CODE (experts are assumed to be
the same timestep; see GAP). **Paired multi-source dataset:** none exists in the pack. Fusion calibration must use
per-source data plus a **clearly labeled SYNTHETIC pairing** (the same label class sampled across sources).

## B. RL (exactly as in code)
- **What it decides:** alarm action per zone/timestep among `HOLD, WATCH, ALARM` (`deep/offline_rl.py`).
- **State:** a feature vector (`state_dim` is read from the data; default 16). We propose fused p, U*, S and per-expert p.
- **Algorithm:** Conservative Q-Learning, `gamma=0` (one-step bandit), `cql_alpha=1`, Polyak `tau=0.005`, hidden
  (256,256), AdamW, 50 epochs, batch 256, 1 GPU.
- **Baseline:** `RuleBaselinePolicy(threshold=0.0476)`.
- **Evaluation:** WIS off-policy value + ESS + positivity (`ope_admission`). Deploy only if feasible AND value ≥ baseline.
- **Environment / simulator (UPDATED 2026-10-31):** `ws5_fusion_rl/env_landslide.py` (see §C). Before this there was NONE in code. Logs come from `data_adapters/make_rl_logs.py`. The reward uses
  C_FA=5 and C_miss=100 from config, and the WATCH costs (0.5·C_miss, 0.2·C_FA) are an **ASSUMPTION**.
- **Reward-hacking risk:** the policy always says WATCH if WATCH is cheap. Test with `--watch-miss 0.8`.
- **Human-in-the-loop:** the policy output is advisory and the shield raises only. The operator approves CAP.
- **Seeds:** the script uses `set_seed(0)`. Loop seeds 0..4 in the notebook.
## C. Landslide RL environment (new, `ws5_fusion_rl/env_landslide.py`, driver `kaggle/rl_env_eval.py`)
- **Step = 1 monsoon day** (Jun-Sep, 122 steps). Rain = REAL NASA POWER seasons (2007-2016, all cached cells), resampled per episode.
- **Physics:** Iverson multipulse head over the last 30 days, then FS with back-analysed c′. **Hazard** P(fail) = σ(α + β·ΔFS). β is fitted on the REAL
  GLC case-control table; α is set so a never-acting slope fails with 30%/season (ASSUMPTION, flag `--season-fail`).
- **Observation (8):** noisy rain sums, Caine ratio, noisy piezometer with dropout, model FS estimate, day, previous action.
- **Actions:** HOLD / WATCH / ALARM. **Reward:** −C_FA per alarm day, −0.2·C_FA per watch day, −C_miss (HOLD) or −0.5·C_miss (WATCH) at a failure.
- **Policies compared ONLINE (true return):** always-hold, always-alarm, Caine rule, physics rule (Bayes action on estimated hazard), oracle (true
  hazard), CQL learned (γ = 0.95, on eps-rule logs), CQL + repo shield. Deploy only if the paired 95% LCB of the gain vs the best rule is > 0.
- **Key lesson:** whether warning pays off depends on C_miss/C_FA. Results for C_miss = 100 / 1000 / 5000 are in `results/RESULTS.md`.
- Hinglish: ye ek "video game" hai jisme barish asli hai aur slope ka physics asli formula se chalta hai, sirf girne ki probability ka scale
  maana hua hai. Isme hum dekh sakte hain ki AI agent asli me kitna bachata hai, sirf andaaza (OPE) nahi.
<!-- END -->
