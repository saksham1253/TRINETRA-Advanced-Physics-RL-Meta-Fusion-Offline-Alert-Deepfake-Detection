# ws5_fusion/rl_multimodal_integration_P22.md — advisory RL + multimodal integration into meta-fusion (P22)

Phase P22 · RESEARCH-ONLY · WS5. How the ADVISORY RL layer (P15) and the multimodal detectors connect to the
meta-fusion operator. HONESTY: nothing built/measured; metrics in cited parents SOURCE-REPORTED; Rule 19 — RL
is ADVISORY (ranks options / tunes soft parameters / suggests which sensor to check), NEVER actuates and NEVER
emits a public alert; must BEAT a strong non-RL baseline (MILP 2602.14676) to be kept; fail-safe to "uncertain"
preserved. Grounding (source-reported): physics-informed/model-based RL 2212.02179, 2309.01909, 2208.14501,
2506.01755; active perception / value-of-information 2607.22667, 1906.07233, 2602.01266; ensemble-weighting RL
2106.06783; multimodal RL under missing modalities 2606.15514, 1703.04550; safe/constrained RL 2607.03125,
2603.24241; multimodal fusion 2306.02050 (QMF), 2204.00102 (dynamic gating).

## 1. Where RL sits (and where it must NOT)
- RL TUNES, it does not decide: the policy outputs (a) soft hyperparameters of the PHARAOH operator within safe
  bounds (τ uncertainty-temperature, κ safety-aggressiveness) and (b) an ACTIVE-PERCEPTION action — which
  modality/sensor to query next under cost/latency/energy constraints (value-of-information).
- RL must NOT: set the alarm threshold below the certified floor, disable the fail-open, exceed the false-alarm
  budget, or originate an alert. These are hard constraints (safe/constrained RL, 2607.03125), not learned.

## 2. Multimodal handling (missing-modality robustness)
- The fusion operator already down-weights unavailable/uncertain/physics-inconsistent modalities (δ_i, u_i,
  c_i). RL complements this by LEARNING, under drift, which modality to trust/query (dynamic fusion 2204.00102;
  QMF quality-aware 2306.02050; RL4IL soft fusion under dropout 2606.15514). If a modality drops, the policy
  can request a cheaper corroborating one rather than forcing a decision.
- Offline-first: all modality handling degrades gracefully offline; RL inference is tiny and on-device.

## 3. State / action / reward (advisory)
- STATE: {p_i, u_i, c_i, r_i, availability, disagreement D, salience S, context (time/scene/season)}.
- ACTION: Δ(τ,κ) within bounds ∪ {query modality j, or "commit advisory"} ∪ {"escalate to human"}.
- REWARD: life-safety-asymmetric detection utility (missed-event cost ≫ false-alarm cost) − λ_fa·false-alarms
  − λ_cost·sensing/energy cost + physics-consistency bonus (physics-informed reward 2309.01909, 2604.01830).
  The asymmetry encodes Rule 19 (caution) directly in the objective.
- CONSTRAINTS (hard): FA-rate ≤ budget; never below certified sensitivity; fail-open always reachable.

## 4. Learning & evaluation protocol
- OFFLINE RL first (log replay); physics-informed/model-based dynamics (2212.02179, 2208.14501) for sample
  efficiency; uncertainty-aware value estimates; conservative/offline evaluation before any shadow use.
- MUST-BEAT-BASELINE gate: beat a non-RL auto-tuner / MILP sensor schedule (2602.14676) on held-out cross-site
  episodes by > seed/trial variance (2302.04054), with ~0 safety-constraint violations; else the non-RL
  controller is used.
- Staged like the pilot: offline → shadow (suggests, triggers nothing) → advisory (human decides).

## 5. Honest limitations
Advisory RL adds complexity and a drift/attack surface (reward hacking, distribution shift → monitor with P16
uncertainty-entropy gates); naive RL can underperform (2509.19972) → the beat-baseline gate is mandatory; the
physics-informed reward depends on the Class-A/B physics gate (uncertain). CLASS C integration; nothing built;
no performance claimed; expert review (RL-safety + fire-science + human-factors) required.
