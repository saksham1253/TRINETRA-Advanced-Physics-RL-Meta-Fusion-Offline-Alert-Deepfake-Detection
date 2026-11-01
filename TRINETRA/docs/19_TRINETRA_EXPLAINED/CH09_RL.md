# CH09 — RL AND DECISION SUPPORT

**Simple me samjho:** RL ek naya trainee officer hai. Hum use asli barish ke "practice ground" (simulator) me khilate hain, aur use tabhi duty par lagate hain
jab wo purane rule-book officer ko saaf taur par haraaye. Abhi tak usne nahi haraya, isliye rule-book hi chal rahi hai.

| Item | Value (code) |
|---|---|
| Decides | HOLD / WATCH / ALARM per day (landslide env) or per decision (offline logs) |
| Environment | `ws5_fusion_rl/env_landslide.py`: Iverson + back-analysed FS on REAL NASA POWER monsoon seasons (360), slope 39.6° |
| State (8) | log rain 1/3/15 d (noisy), log Caine ratio, noisy piezometer head (10% dropout), FS estimate, day, previous action |
| Reward | alarm day −C_FA (5); watch day −0.2·C_FA; failure: HOLD −C_miss, WATCH −0.5·C_miss, ALARM 0 |
| Hazard | σ(α + βΔFS); β = 24.3 fitted on real events; α so HOLD fails 30%/season (ASSUMPTION) |
| Algorithm | CQL, hidden (256, 256), γ 0.95, cql_α 1, Polyak τ 0.005, AdamW 3e-4, batch 512, 30 epochs |
| Logs | eps-rule behaviour (eps 0.3) from the physics rule; exact behaviour probabilities stored |
| Baselines | always hold, always alarm, Caine rule (0.5/1.0), physics rule (myopic Bayes action), oracle (true hazard) |
| Evaluation | ONLINE true return (300 episodes, shared seeds) + one-step OPE proxy |
| Deploy gate | paired per-episode 95% LCB of gain vs the best rule > 0 (B-25) |
| Shield | repo shield floor applied to the learned action (raise-only) |
| Human role | advisory only; the operator approves every public alert |

**Results (SIMULATOR, results/rl_env):** C_miss = 100: hold −22.7, alarm −540.5, physics rule −22.8, oracle −22.9, CQL −22.5, LCB −0.30, so not deployed.
High-cost sensitivity (OUR RESULT, SIMULATOR; `results/rl_env/rl_env_cmiss1000_s0_report.json`, `rl_env_cmiss5000_s0_report.json`; same 360 seasons, seed 0):

| policy | C_miss=1000 return | miss rate | C_miss=5000 return | miss rate |
|---|---|---|---|---|
| always hold | −226.7 | 1.00 | −1133.3 | 1.00 |
| always alarm | −540.5 | 0.00 | −540.5 | 0.00 |
| Caine rule | −204.9 | 0.97 | −998.3 | 0.97 |
| physics rule | −200.0 | 0.81 | −478.1 | 0.19 |
| oracle (true hazard) | −200.0 | 0.81 | −478.5 | 0.19 |
| CQL + shield | −200.9 | 0.84 | −486.8 | 0.19 |

Gain of CQL vs best rule: mean −0.88 / LCB95 −10.28 (1000); mean −8.77 / LCB95 −31.93 (5000) → `deploy_learned = false` both times.
Matlab: jaise miss ka cost badhta hai, physics rule zyada alarm deta hai (5000 par ~66 alarm-days/season) aur oracle ke barabar perform karta hai. CQL kabhi rule ko nahi harata, isliye gate rule hi rakhta hai. Ye simulator result hai (hazard intercept ASSUMPTION), field evidence nahi.

**Reward-hacking risks:** cheap WATCH could be overused (test with `--watch-miss 0.8`); a learned policy can exploit simulator quirks, hence the online CI gate.
**Self-check:** oracle bhi "hold" ko kyun nahi harata at C_miss 100? (Cost ratio par daily alarm justified nahi hota.)
<!-- END -->
