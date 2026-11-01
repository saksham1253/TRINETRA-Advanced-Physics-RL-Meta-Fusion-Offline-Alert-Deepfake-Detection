# 00 — Context Recovered (Phase P0, Task 0.4)

Date: 2026-10-05
Purpose: a single self-contained statement of *what this project is*, *what has already
been decided*, *what is still open*, and *the physics made explicit* — recovered from the
prior-session artifacts (`analysis/*`, the six root `TRINETRA_*.md`, and the read-only
`trinetra\` source). Everything here is background for the new RESEARCH-ONLY program
(phases P0–P20); nothing here is re-derived or re-run under the new program yet.

---

## 1. Purpose (the "why")
**TRINETRA** (alt. HIMKAVACH) is an **offline-first, multi-sensor early-warning system**
for **landslides, flash-floods, cloudbursts, and GLOFs** in **Uttarakhand + Himachal
Pradesh** (~110,000 km²). The governing goal (MASTER_PROMPT Rule 19) is **real-world
life-safety benefit to India** — a system that *complements, never replaces*, certified
official warning systems and always keeps a human in the loop. It is **not** a competition
entry; correctness and honesty outrank novelty.

Three fused sensing layers:
1. **Satellite / EO** — Sentinel-1 InSAR, Sentinel-2, GPM IMERG, SMAP, ERA5-Land, MODIS,
   ITS_LIVE.
2. **Cameras** — existing CCTV + ultra-cheap "River Eye" LSPIV nodes (surface-velocity
   from video).
3. **Ground IoT** — ₹2,000 LoRa nodes (tilt/accel, soil moisture, piezometer, rain gauge).

Pipeline: SSL masked-modeling InSAR encoder → anomaly stack (forecast-residual + Deep
SVDD + isolation forest + XGBoost) → **physics gate** → **RL alarm policy** → calibrated
"people-at-risk" → CAP/SACHET alert routing.

## 2. Hard constraints (carried from the source project + MASTER_PROMPT)
- **Compute:** Kaggle only, ~25–30 GPU-h/week, keep ≥15% reserve.
- **IoT cost:** ≤ **₹2,000/node** incl. GST + shipping, verified Indian listings, ~10%
  contingency. (Price verification currently tooling-blocked — see ENVIRONMENT_CHECK.)
- **Datasets:** FREE only; a dataset must be STATUS=selected to be used.
- **Safety:** safe-stimulus-only; privacy/ethics/law handled as research notes flagged
  for expert review; life-safety framing in every design doc that could influence a
  real alert.

## 3. What is DECIDED (inherited design commitments)
These were decided in the *source* project and are treated as the starting design, each
subject to re-examination under the new program:
- Offline-first architecture; three-layer sensor fusion as above.
- A **physics gate** between the data-driven anomaly stack and the alarm policy.
- A **4-stage RL alarm policy** path: fixed-threshold → LHASA v1/v2 (Stanley/Khan) →
  offline CQL/IQL/TD3+BC (via d3rlpy) → PPO (SB3).
- A **safety shield** with hard overrides (FS<1→Orange; tilt>5°/day→Red; 24h rain
  >150 mm→Orange; GLOF signature→Red).
- A **Gated Meta-Fusion (GMF)** head: bounded residual policy over a physics base action
  `â = clip(a0 + residual)`, per-zone Mondrian conformal, monotone shield `max(â, S(s))`.
- Two IoT node designs: "Slope Sentinel" and "River Eye", both re-BOM'd to ≤₹2,000 with
  **compliant LoRa band IN865–867 (NOT 433 MHz)**.
- A standing **evaluation remedy**: every headline claim must be re-run under **tile-
  withheld spatial cross-validation** against a **gradient-boosted / decision-tree
  baseline**, plus a **persistence baseline** for the forecasting head.

## 4. What is OPEN (unresolved; feeds P0.8 key questions)
- Whether a **bespoke SSL encoder** is justified vs a frozen EO-FM (Prithvi-EO-2.0 /
  Galileo) baseline — novelty may survive only for the forecasting/pre-event regime.
- The three **I–D rainfall-threshold constants** (Caine 14.82·D⁻⁰·³⁹, Dahal–Hasegawa
  73.9·D⁻⁰·⁷⁹, Garhwal 1.82·D⁻⁰·²³) are **unverified to page/equation** (Bug #15) — and
  2106.15119 argues a single borrowed constant is unjustified (fit a *distribution*).
- **Shield realizability**: stacked hard overrides can conflict (2507.23603) → needs a
  formal realizability check + priority lattice.
- **Conformal validity** under missingness + endogenous feedback shift (overclaim #13).
- **Datacube size** is 10–35× under-estimated (#10): claimed 2–5 TB vs realistic
  45–130 TB — does the real footprint fit Kaggle?
- **Edge-compute feasibility** (#14): heavy VAD/encoder benchmarked on L40S, not the MCU
  → tiered edge→cloud split needed.
- **Security** (#12): `Proxy.py` forwards credentials to `https://api.justwoker.icu`.
- Whether the **~236 unique abstract-only** prior papers can count toward later-phase
  quotas or must be re-read at Tier-2+ (quota-honesty tension — see §0.9 of MASTER_PROMPT).

## 5. Physics made explicit (CLASS labels to be assigned per MASTER_PROMPT §admission)
- **Infinite-slope / TRIGRS factor of safety:** `FS = F_f + F_w + F_c` (frictional +
  water + cohesion terms).
- **Iverson (2000) transient infiltration:** pressure head ψ(Z,t); **slope enters ONLY
  via `D₁ = D₀/cos²δ`**. The shipped report adds a spurious `cos²β`/`cosβ` factor =
  **Bug #3** (double-count).
- **Fukuzono / Voight inverse-velocity:** `1/v = A(α−1)(t_f − t)` at **α ≈ 2**; linear in
  1/v only at α=2. Report's α range 1.5–2.2 is **Bug #4**.
- **Caine I–D threshold:** `I = a·D⁻ᵇ` (intensity–duration).
- **Lu & Likos suction stress:** `σ_s = −S_e·ψ` (sign is **Bug #2** in the report).
- **Bayes alarm optimum:** `p* = C_FA/(C_FA + C_miss) = 5/105 = 0.0476` (the ~10× threshold
  inconsistency vs 0.5 and LHASA's 0.12 is **Bug #1**).
- Also used: Scheidegger runout, Froehlich, SCS-CN, Manning's equation.
- **Richards equation** (full infiltration) is the high-fidelity reference that Iverson
  linearizes (grounds the physics-gate validity window).

## 6. RL + shield specifics (inherited)
- Reward: miss = −100, FA = −5 (red) / −1 (yellow-orange), lead = +2/h capped 12 h,
  disruption = −0.01/person-hour, level-change = −0.5, γ ≈ 0.99/h.
- Offline-RL anchors: CQL (2006.04779), IQL (2110.06169), TD3+BC; shielding (Alshiekh
  1708.08611). GMF prior art: Wolpert stacking (1992), Meta-AAD (2009.07415), RL
  model-selection (2205.09884).

## 7. 14 search axes (A1–A14)
A1 InSAR/deformation+GNSS · A2 EO-FM/SSL encoders · A3 I–D thresholds/extreme-weather ·
A4 transient infiltration/Richards · A5 offline RL/OPE · A6 safe RL/shielding ·
A7 conformal prediction · A8 rare-event/calibration/anomaly/EWS verification ·
A9 VAD edge/LSPIV · A10 LoRa/LPWAN/DTN/energy-harvest · A11 GLOF/dam-break/runout/
flash-flood · A12 multimodal/stacked/MoE fusion · A13 evacuation/decision/cost-loss ·
A14 drift/OOD/monitoring.

## 8. Prior findings as BACKGROUND (NOT re-run under the research-only program)
33 bug findings #0–#32 exist in `TRINETRA_Bug_Report.md` (e.g. #0 workflow-faked-success,
#1 threshold inconsistency, #2 suction-stress sign, #3 Iverson double-count, #4 α range,
#6 433 MHz band, #10 datacube under-estimate, #11 underpowered eval, #12 proxy cred leak,
#13 conformal overclaim, #14 edge latency). These are inherited context; the new program
will re-examine them under its own evidence rules, not inherit their conclusions.
