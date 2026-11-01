# TRINETRA — Meta-Fusion Decision Head (RL + Multimodal Verifier Stack)

**Why this exists.** The audit (Bug #1, #9, #13 in `TRINETRA_Bug_Report.md`) showed the RL alarm policy is *not robust alone*: its reward can invert the safety bias, its threshold conflicts ~10× with the physics gate, and a single learned policy over ~5 events is badly underpowered. The user's proposal — add one or more multimodal models that take **both the raw input and the RL policy's output**, and emit the final decision — is architecturally correct and has a precise name in the literature: **meta-fusion / stacked generalization over a policy**, closely related to **residual policy learning** and **learned safety shields**.

This document specifies that design with live-verified citations.

---

## 1. The user's idea, named and grounded

> "A model that takes the raw input taken by the RL model AND the output of the RL model as input, and produces the final decision — meta fusion."

This is **stacking (Wolpert 1992 stacked generalization)** applied to a decision policy, where the RL policy is one *base learner* and a **meta-learner** fuses its action-logits with the raw multimodal evidence. Three verified prior-art families make it rigorous rather than ad-hoc:

| Technique | What it does | Verified source (fetched live) | How we use it |
|---|---|---|---|
| **Residual Policy Learning (RPL)** | Learns a correction *on top of* an imperfect base controller; final action = base + learned residual | arXiv:1812.06298 — Silver, Allen, Tenenbaum, Kaelbling (2018) | Physics/Bayes rule is the base controller; a learned head outputs a bounded residual |
| **Residual RL for control** | Decompose a hard control problem into a conventional controller + an RL residual (superposition of both signals) | arXiv:1812.03201 — Johannink et al. (2018), Levine group | Justifies "RL corrects the physics rule," not "RL replaces it" |
| **Safe RL via Shielding** | A reactive shield sits *after* the learner and corrects actions that violate a temporal-logic safety spec, preserving convergence | arXiv:1708.08611 — Alshiekh, Bloem, Könighofer, Niekum, Topcu (2017) | Formal basis for the hard physics shield that can only RAISE the alarm |
| **Offline RL (IQL)** | Learns an improving policy from a fixed log without querying unseen actions — essential given we have ~5 events, no safe exploration | arXiv:2110.06169 — Kostrikov, Nair, Levine (2021) | How the base RL expert is trained offline |

**Net:** the user's "meta-fusion" is the *correct* way to make the RL robust — it is exactly stacking + residual learning + shielding, all of which are established and citable. This is a genuine improvement to the architecture, not a reviewer's nitpick.

---

## 2. Architecture — "Gated Meta-Fusion Decision Head" (GMF)

```
                 ┌─────────────────────────── raw multimodal evidence x ───────────────────────────┐
                 │  InSAR dLOS stack · S2 optical indices · IMERG rain · SMAP soil · camera stage/   │
                 │  LSPIV/anomaly · IoT tilt/soil/rain · physics P-FS(t) · MS-IVE t_f · HEI          │
                 └───────────────┬───────────────────────────────┬───────────────────────────────────┘
                                 │                               │
                 ┌───────────────▼─────────┐        ┌────────────▼──────────────┐
   EXPERT 1      │ Physics/Bayes base rule │        │  Supervised ensemble       │  EXPERT 3
                 │ FS, I-D, P_f, LHASA-XGB │        │  (forecast-residual, SVDD, │
                 │  → p_phys, action a_0   │        │   iForest, XGBoost) → p_sup│
                 └───────────────┬─────────┘        └────────────┬──────────────┘
                                 │                               │
                 ┌───────────────▼─────────┐                     │
   EXPERT 2      │  Offline RL policy (IQL/ │                     │
                 │  CQL) → action logits    │                     │
                 │   π_RL(a|s), q-values    │                     │
                 └───────────────┬─────────┘                     │
                                 │                               │
          ┌──────────────────────▼───────────────────────────────▼───────────────────────┐
          │  META-FUSION HEAD  m(x, π_RL output, p_phys, p_sup)                            │
          │   • input = raw evidence embedding  ⊕  RL action-logits/q-values  ⊕ expert ps  │
          │   • small multimodal transformer / gated MoE (learns per-context trust weights)│
          │   • outputs a RESIDUAL over the physics base action a_0  (RPL, 1812.06298)     │
          │   • final pre-shield decision â = clip(a_0 + residual)                         │
          └──────────────────────────────────┬────────────────────────────────────────────┘
                                              │
                 ┌────────────────────────────▼────────────────────────────┐
                 │  CONFORMAL-RISK CALIBRATION (per-zone Mondrian)           │  → bounded FA/miss, honest coverage
                 └────────────────────────────┬────────────────────────────┘
                                              │
                 ┌────────────────────────────▼────────────────────────────┐
                 │  HARD SAFETY SHIELD  S(s) ∈ {Green,Yellow,Orange,Red}     │  can ONLY raise (1708.08611)
                 │  FS<1→≥Orange · tilt>5°/day→Red · 24h>150mm high-susc→≥O  │
                 │  lake-drop/stage-jump→downstream Red                      │
                 └────────────────────────────┬────────────────────────────┘
                                              ▼
                                    FINAL ALERT LEVEL
```

### Why the meta-head takes the RL *output* as input (the user's key point)
- The RL policy encodes **temporal/sequential value** (lead-time vs cry-wolf trade-off, γ=0.99) that a one-shot classifier cannot.
- But RL alone is brittle on n≈5 events. Feeding `π_RL`'s logits/q-values **as features** into a meta-learner that *also* sees the raw evidence lets the meta-head learn *when to trust the RL* and when to defer to physics/supervised experts — this is the gated mixture-of-experts trust-weighting. This directly fixes Bug #1 (one calibrated decision) and Bug #9 (the meta-head + conformal re-weights the degenerate flat reward).

---

## 3. Formal spec

**Experts (base learners):**
- `e_phys(x)` → physics/Bayes probability `p_phys` + base action `a₀` (the conventional controller).
- `e_RL(s)` → offline-RL policy `π_RL(a|s)` with q-values `q(s,a)` (IQL, arXiv:2110.06169; or CQL).
- `e_sup(x)` → supervised/anomaly ensemble probability `p_sup`.

**Meta-fusion head** (stacked generalizer, residual form):
```
z        = Encoder(x)                      # multimodal embedding of raw evidence
features = [ z , logits(π_RL) , q(s,·) , p_phys , p_sup , coherence/quality masks ]
residual = MLP_or_GatedMoE(features)       # bounded, e.g. tanh-scaled to ±1 level
â        = clip( a₀ + residual , Green, Red)   # Residual Policy Learning (1812.06298/1812.03201)
```

**Calibration:** per-zone Mondrian conformal-risk-control on `â` → bounds the per-group miss-rate (honest; not a "guarantee" — see Bug #13).

**Shield (monotone floor, formally after the learner):**
```
final = max( conformal(â) , S(s) )         # S can only RAISE (Alshiekh et al. 2017)
```
Convergence/safety of placing the shield *after* the learner is exactly the "post-posed shield" case proven in arXiv:1708.08611.

**Training order:**
1. Train experts independently (physics is analytic; supervised on inventories; RL offline via IQL/CQL on logged episodes with the exposure-weighted per-capita reward from Bug #9 fix).
2. Freeze experts; train the meta-head on held-out validation events (leave-one-event-out) so it learns trust-weights without leaking.
3. Fit conformal calibration on a separate split.
4. Shield is hard-coded (no training).

---

## 4. What this adds to novelty (honest)

- **Not novel in general ML:** stacking, residual RL, shielding, gated MoE all exist (cited above).
- **Plausibly novel in the Himalayan multi-hazard EWS setting:** no prior work found that fuses an *offline-RL alarm policy as one expert* with physics + multimodal supervised experts under a *post-posed hard physics shield + per-zone conformal risk control*. State the claim at that honest altitude: **"a meta-fusion decision head combining a shielded offline-RL alarm policy with physics and multimodal experts, conformally risk-calibrated per zone"** — combination + regional application + evaluation rigor, not a new learning algorithm.

---

## 5. Compute feasibility (Kaggle-honest)
- Meta-head is small (MLP or ~2-layer transformer over a few hundred features): minutes on CPU/1 GPU.
- Offline RL on tabular state: light (d3rlpy DiscreteCQL/IQL), ~1 GPU-hr/run.
- The expensive part is the foundation-model embedding `z` — reuse the frozen backbone from Part 7; do **not** retrain. Fits the ~30 GPU-hr/week Kaggle budget.
- **Caveat:** this does not escape Bug #11 (n≈5 events). The meta-head *reduces variance* but cannot manufacture statistical power. It must be evaluated under the same frozen leave-one-event-out protocol with bootstrap CIs, and reported honestly.

---

## 6. Verified references
- arXiv:1812.06298 — Residual Policy Learning (Silver et al., 2018). ✅ fetched.
- arXiv:1812.03201 — Residual RL for Robot Control (Johannink et al., 2018). ✅ fetched.
- arXiv:1708.08611 — Safe RL via Shielding (Alshiekh et al., 2017). ✅ fetched.
- arXiv:2110.06169 — Offline RL with Implicit Q-Learning / IQL (Kostrikov et al., 2021). ✅ fetched.
- Wolpert, D. (1992) Stacked Generalization, *Neural Networks* 5(2) — classical basis for meta-fusion [to cite from source].

**Note on agents:** the user asked to run 10–20 agents for this. The DSH multi-agent workflow tool is not exposed in this session, so this spec was produced by direct, live-verified research. Re-enabling that tool (with credits) would let the real fix+verify+synthesis workflow run.
