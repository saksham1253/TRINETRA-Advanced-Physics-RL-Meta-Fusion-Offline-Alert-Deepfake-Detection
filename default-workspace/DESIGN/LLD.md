# TRINETRA / HIMKAVACH — LOW-LEVEL DESIGN (LLD) v1.0
> Module-internal design: interfaces, data schemas, algorithms, config flags, and acceptance tests for the
> codebase phase. Companion to `DESIGN/SYSTEM_DESIGN_PROMPT.md` and `DESIGN/HLD.md`. Signatures are Python-ish
> contracts, not final code. Honesty/safety rules R16/R19/R20/R21 and `[coeff-verify]`/`[EST]` tags bind here.
> Class-C blocks are behind feature flags with a Class-A/B fallback and emit a `trust`/`class` field.

---
## 0. Shared types & conventions (`src/common`)
```python
Level = Enum("Level", "GREEN YELLOW ORANGE RED")           # ordered; comparisons allowed
Hazard = Enum("Hazard", "LANDSLIDE FLASHFLOOD CLOUDBURST GLOF FIRE")

@dataclass
class Evidence:            # one timestamped observation bundle for a zone
    zone_id: str
    t: datetime                                   # feature timestamp (anti-leak: ≤ decision time)
    eo: dict | None        # InSAR dLOS stack, S2 indices, IMERG, SMAP, ERA5, active-fire
    vision: dict | None    # detector boxes, LSPIV stage, flicker/flow score, VAD score
    iot: dict | None       # tilt, soil moisture×2, piezo, rain, T/P + per-sensor health
    quality: dict          # per-modality reliability in [0,1]: coherence, cloud_frac, node_health
    provenance: dict       # source ids, versions, seed, fold_id

@dataclass
class ExpertOutput:
    p: float               # calibrated probability in [0,1] (hazard present / threshold exceeded)
    u: float               # uncertainty in [0,1]
    c: float               # physics-consistency in [0,1] (NF-1); default 1.0 if N/A
    r: float               # reliability/trust in [0,1] (NF-2); from quality + drift history
    cls: str               # "A" | "B" | "C"
    source: str

@dataclass
class Decision:
    level: Level
    risk: float            # fused calibrated risk
    conformal: dict        # {set, interval, coverage_target, reliability_flag}
    shield_reason: str | None   # which hard rule raised the level (explainability, Rule 19)
    contributions: list    # per-expert ExpertOutput (audit trail)
    trust: str             # "advisory"; always human-gated
```
Conventions: all probabilities calibrated before fusion; every output carries `cls` and `trust`; time is UTC;
no module may consume features with `t > decision_time` (anti-leak, G6).

---
## 1. M0 — Data + evaluation harness (`eval/`, build FIRST)
Interfaces:
```python
def make_splits(dataset, mode: {"spatial_tile","event_holdout","random"}) -> Folds   # log fold_id
def baselines(task) -> list[Model]        # persistence, seasonal_naive, gbt, decision_tree3, linear, phys_rule
def value_score(y, p, cost_ratio_grid) -> dict           # cost-loss Value Score (PRIMARY), p* = CFA/(CFA+Cmiss)
def real_win_gate(runs: dict[seed,camera,site -> metric]) -> {significant: bool, reliability: float}  # LMEM+GLRT (F-17)
def report(table) -> Report               # must contain spatial-CV column + baseline + CI, else refuses
```
Rules enforced in code: `report()` raises if a metric lacks its spatial-CV baseline + bootstrap CI; deep-model
rows auto-annotate "beats baseline?" ; forecasting adds persistence; classification adds gbt+3-rule+linear.
Provenance via dagger/MLflow (F-17 2006.07484). Deseasonalize seasonal inputs; disclose feature–label r
before/after. ACCEPTANCE (G2): no number leaves the harness without baseline+CI+real-win verdict.

---
## 2. M1 — Geo physics gate (`src/ws1b_geophys`)  [Classes A/B/C per model_set_decision.md]
```python
def fs_infinite_slope(c, phi, gamma, z, beta, m, sigma_s) -> float      # FS = Ff + Fw + Fc  [Class A]
def iverson_head(Z, t, D0, Kz, Inz, delta) -> float                     # transient ψ(Z,t)   [Class A]
def fukuzono_inv_velocity(v_series, alpha=2.0) -> t_failure              # 1/v linear if α=2  [Class A/B]
def caine_id_threshold(I, D, a, b) -> bool                              # I = a·D^(−b)       [Class A, local-calib]
```
CRITICAL correctness (from bug history, enforce by test):
- Iverson: slope enters ONLY via `D1 = D0 / cos²β`; NO spurious extra `cos²β/cosβ` on the transient term.
- Suction-stress sign correct: `S_e→1 ⇒ σ_s→0 ⇒` FS reduces to saturated infinite-slope form.
- Fukuzono: α=2 ⇒ 1/v linear; α≠2 ⇒ `v^(1−α)` linear (do not silently use α∈[1.5,2.2]).
- Caine I–D constants `[coeff-verify]`; prefer a FITTED local distribution of Ks/slope/suction/γ_d over one
  borrowed constant; feed an ENSEMBLE rainfall field → output a DISTRIBUTION of FS, not a point.
GOLDEN TESTS (G1): saturated limit, β→0 & t→∞ steady-state, α=2 linearity. ACCEPTANCE: all pass; FS monotone
in suction; no downstream module imports a legacy (buggy) form.

---
## 3. M2 — Fire physics layer (`src/ws1a_firephys`)  [Class A: EF-01..EF-20; Class C soft: ND-1..ND-7]
Established blocks (Class A, `[coeff-verify]`): plume/flame-height (EF-01..EF-12), Byram/critical-Froude
(EF-13), RTE (EF-14), WSGGM soot (EF-15), Strouhal puffing (EF-16), ADR transport (EF-17), G-equation (EF-19),
Rothermel+Huygens offline (EF-20). Novel SOFT features (Class C — flag-gated, fallback = omit feature):
```python
def nd1_dealiased_flicker(spectrum, f_s, D_prior) -> float      # matched-filter on predicted aliased band
def nd2_transmittance_temp(L_obs, tau_s, sensor_lag) -> (T_hat, sigma)   # σ grows as τ_s→0 (fail to "uncertain")
def nd3_ignition_index(dTdt, dCdt, dqdt, buoyancy_scales) -> float       # Π_ig dimensionless, scene-invariant
def nd4_physics_residual(s_obs, s_phys_pred, Sigma) -> float             # r_phys ∈ [0,1]; feeds NF-1 c_i
def nd5_wind_tilt_height(h_px, theta_from_flow, range_m) -> (L_hat, sigma)
def nd6_regime_scalar(q_rad, mdot, cp, dT) -> float                      # Ξ_rc → modality gate (feeds FM-5)
def nd7_advection_coherence(node_signals, positions, wind) -> float      # COH ∈ [0,1] corroboration prior
```
Each ND returns value + uncertainty + `cls="C"`; enters fusion ONLY as a soft feature/prior with a Class-A
fallback; never a hard trigger. ACCEPTANCE: unit tests on synthetic inputs; `[coeff-verify]` resolved or the
feature stays disabled; expert-review flag recorded in output metadata.

---
## 4. M3 — EO encoder + anomaly stack (`src/ws1b_geophys`, `src/ws8_anomaly`)
```python
class EOEncoder:            # FROZEN, SAR-capable (CR-01 trade study: CROMA/Copernicus-FM/AnySat/TerraMind…)
    def embed(self, datacube) -> np.ndarray         # do NOT retrain; selection must beat ViT+GBT baseline
class ForecastResidualHead:                          # bounded residual on a mechanistic/persistence backbone
    def predict(self, z_seq) -> (yhat, residual, bound)   # residual bound validated on Himalayan data (R16)
class AnomalyEnsemble:                                # miss-biased (reward miss≫FA)
    members = [ForecastResidual, DeepSVDD_bounded, IsolationForest, XGBoost]
    def score(self, z) -> {member: s, fused: s}      # Deep SVDD radius bounded away from 0 (anti-collapse)
```
Rules: memory/prototype-constrained or miss-biased scoring (AE over-generalization = missed detection); SSL
data stops at the ~750K-patch knee for Kaggle budget; forecast head learns a BOUNDED residual (5× corroborated
doctrine). ACCEPTANCE: anomaly radius > 0 under PU training; beats persistence on spatial-CV (else reported as
not beating baseline).

---
## 5. M4 — CCTV perception (`src/ws4_cctv`)  [F-11, F-12, F-16; Wave-2/3 optional]
```python
class EdgeDetector:                 # F-11; yolov5n|efa|ghost backbone; {none|PTQ-INT8|QAT+TRT}
    def detect(self, frame_rgb) -> list[Box{cls∈{flame,smoke}, conf, xywh}]
class TemporalValidator:            # F-12; multi-frame confirm + confidence-weighted vote + cascade
    def update(self, dets) -> Event | None   # emits confirmed Event + confidence + latency stamp
def ir_flicker_feature(video) -> (mask, conf)             # F-16; optical-flow+divergence+MRF, label-free
```
Config flags: backbone variant, compression ratio, attention on/off, quantization mode, PTQ calib size,
confirmation window, vote weights, cascade thresholds, FAR target. METRICS: mAP@0.5 + recall AT MATCHED
precision + SMOKE-SPECIFIC recall + latency/energy on target edge HW. DECISION RULE (pre-registered): keep a
variant only if cross-CAMERA gain > seed variance AND it meets the edge latency/energy ceiling. KNOWN PITFALL
(test it): INT8 PTQ hurts diffuse-smoke recall; longer F-12 window delays the alert. Tier: F-11/F-12/F-16 run
Tier-1 gateway; Tier-0 node does only a tiny screen. Feeds fire-physics soft features (M2) + fusion (M7).

---
## 6. M5 — Calibration + drift monitor (`src/ws6_robust`)  [F-13, F-14]
```python
class ConformalCalibrator:          # F-13; WCPS covariate-shift reweighting (+ Venn-Abers / NACP options)
    def calibrate(self, scores, calib_set, alpha) -> (sets, reliability_flag∈{High,Med,Low,Unreliable})
class DriftMonitor:                 # F-14; STUDD student-teacher + CUSUM calibration + DriftLens distance
    def step(self, outputs, labels=None) -> Advisory{drift, miscalibration, samples}   # ADVISORY only (R19)
```
Rules: NEVER claim 1−α coverage cross-site without reweighting (vanilla split-CP collapsed 90%→65% under
shift); concept drift voids covariate-shift bounds → DriftMonitor flags `Unreliable`; monitor input-drift AND
calibration-drift separately; monitor is advisory (no autonomous retrain-and-act). ACCEPTANCE (part of G3):
realized coverage (PICP) near nominal on a drifting holdout; drift detector beats a fixed-threshold monitor on
replayed drift within the edge compute budget.

---
## 7. M6 — Offline-RL alarm policy + safety shield (`src/ws5_fusion_rl`)  [WS5]
```python
class AlarmPolicy:                  # baseline-FIRST: one-step/TD3+BC; CQL/IQL only if OPE gate passes
    state  = [p_phys, p_sup, anomaly, iot_feats, precip_feats, context]
    action = Level
    def act(self, s) -> (logits, q_values, a_rl)
def ope_feasibility(logs) -> bool               # gate BEFORE trusting any learned policy (BVFT + SCOPE-RL)
def shield_floor(s) -> Level:                   # DETERMINISTIC, hard-coded, monotone (can only RAISE)
    # FS<1 → ≥ORANGE ; tilt>5°/day → RED ; 24h rain>150mm on high-susceptibility → ≥ORANGE ;
    # GLOF lake-drop/stage-jump → downstream RED ; fire-corroborated multi-node → ≥ORANGE
```
Reward (exposure-weighted per-capita, sign-checked): miss = −100; false-alarm = −5 (red)/−1 (yellow-orange);
lead-time = +2/h capped 12 h; disruption = −0.01/person-hour; level-change = −0.5; γ≈0.99/h. Shield is
POST-POSED (after the learner) — preserves convergence (shielding theorem) and satisfies R19. EVAL (G2/G3):
≥100 seeds; BVFT selection; SCOPE-RL CVaR@5% + full return distribution; deploy only if OPE lower bound ≥ rule
baseline; must beat trivial baselines (fixed-threshold/immediate). ACCEPTANCE: shield total+realizable
(exhaustive compound-event test never returns undefined); a single faulty node cannot drive RED unaided.

---
## 8. M7 — Meta-fusion head: GMF + PHARAOH + FM-1..FM-6 (`src/ws5_fusion_rl`)  [WS5]
### 8.1 Expert interface & effective weights (NF-2 / NF-1)
```python
# effective weight per expert i (feeds PHARAOH & FM-1): w̃_i = δ_i · r_i(t) · c_i · exp(−u_i/τ)
def effective_weight(e: ExpertOutput, tau: float, available: bool) -> float
def nf2_reliability(r_prev, outcome, drift_flag, r_min) -> float    # exp-forgetting + decay + drift down-weight
def nf1_consistency(p_i, phi_physics, sigma_phi) -> float           # c_i = exp(−((p_i−φ)_+)²/(2(σ²+ε)))
```
### 8.2 PHARAOH aggregation operator (Class C, default-OFF behind flag; fallback = FM-1 arithmetic mean)
```python
def pharaoh(ps, weights, rho) -> float:            # F_ρ(p;w) = (Σ w_i p_i^ρ)^{1/ρ},  Σw_i=1
    #   ρ(t) = 1 + κ · D · S     (adaptive order; D = weighted dispersion, S = credible-alarm salience NF-4)
    #   ρ≥1 ⇒ F_ρ ≥ arithmetic mean  (anti-complacency safety corollary — PROPERTY TO VALIDATE numerically)
def nf4_salience(experts) -> float                 # S = max_i[ r_i · c_i · ψ(p_i) ]
def nf3_conflict_to_uncertainty(experts, lam) -> float   # U* = Σ w_i u_i + λ·D ; fail-open to "uncertain"
```
### 8.3 GMF residual head + the six fusion models
```python
z        = EOEncoder.embed(x)                      # reuse frozen embedding
features = [z, logits(π_RL), q(s,·), p_phys, p_sup, quality_masks, c_i, r_i]
residual = MLP_or_GatedMoE(features)               # bounded (tanh-scaled to ±1 level)
a_hat    = clip(a0 + residual)                     # residual policy learning over physics base a0
# fusion-model options (flag-selectable; default FM-1):
#   FM-1 precision/reliability-weighted linear [B, default/fallback]
#   FM-2 evidential + conflict-discounting [B]      FM-3 conformal-bounded hierarchical stacking [B]
#   FM-4 covariance-intersection (continuous trend) [B]
#   FM-5 physics-consistency-gated MoE  g_i=σ(a_i(x)+β·log c_i)  [C]
#   FM-6 RL-tuned fusion weights w/ physics-informed reward [C, advisory]
```
RULES: collinearity-robust meta-head (report meta-feature condition number; bootstrap sign-flip rate ≈0);
per-modality reliability gating down-weights a degraded expert (inject-degradation test); GMF/PHARAOH NEVER
lower the shield floor (`final = max(conformal(a_hat), shield_floor(s))`); Class-C pieces default OFF, fallback
FM-1. ACCEPTANCE (G4): coefficient stability under resampling; degraded-modality down-weighting demonstrated;
PHARAOH properties P1–P7 numerically verified before the flag may default ON; nothing claimed to beat FM-1
without the G2 real-win gate.

---
## 9. M8 — IoT nodes (`firmware/`, `src/ws7_iot`)  [WS7; ≤₹2,000 each]
Node A "Slope Sentinel": ESP32-C3, SX1262 (865–867 MHz), MPU6050 tilt in PVC, capacitive soil-moisture ×2,
tipping-bucket rain, BMP280, 6V/1W solar + CN3791 + LiFePO4, IP65. Node B "River Eye": ESP32-CAM (OV2640,
no-IR-filter), SX1262, 850nm IR LED, painted staff gauge, 6V/2W solar, microSD, IP65. (BOMs `[EST]`,
price-gate G5.)
```c
// Tier-0 firmware (on-node) — tiny statistical screen ONLY (fits ~3.3KB SRAM / 63KB flash budget)
float zscore_tilt(stream); bool stage_threshold(level); float on_node_fs(...); float inv_velocity_fit(v[]);
// deep sleep + duty cycle; raw video NEVER leaves the node; LSPIV/VAD/heavy models are Tier-1 only
```
```python
# gateway-side (Tier-1)
def f15_drift_correct(raw, T, RH) -> (value, uncertainty, recal_advisory)   # GP/PRNet/Veli; decompose env vs instrument
def fault_vs_event(node_stream, neighbors) -> {"event"|"fault"}             # Neyman-Pearson + cross-node consistency
```
RULES: a single node cannot drive RED (cross-node spatial consistency required); recalibrate only against
INSTRUMENTAL drift (decompose vs environmental first — the F-15 pitfall); global calibration law must not
silently mis-correct an outlier node → pair with per-unit F-14; energy budget per task (camera+comms dominate;
winter/monsoon solar gaps). ACCEPTANCE (G5): both totals ≤₹2,000 after supplier re-check; every model on a
feasible tier with a stated compute/energy budget; LoRa band = 865–867 MHz.

---
## 10. M9 — Alerting / comms (`src/ws3_alert`)  [WS3]
```python
def build_cap(decision: Decision, zone, geo) -> CAP_XML        # CAP 1.2; map Level→severity/urgency/certainty
def sign_and_dedup(cap) -> SignedAlert                         # cryptographic signature + dedup key
def route(signed) -> None                                      # SACHET feed + DTN + local siren/SMS
def dtn_spray_and_wait(msg, contacts) -> delivery              # store-carry-forward when link down (offline-first)
class OperatorUI:                                              # F-22 advisory decision-support
    def present(self, decision) -> None   # shows level + conformal set + shield_reason + per-expert contributions
```
RULES (C1/C6/R19): the LoRa→gateway→siren path MUST work with cloud unreachable; CAP alerts signed; NO alert
is dispatched without operator confirmation; endpoint allow-list enforced (CI fails on non-allowlisted). CAP
severity mapping is deterministic from Level. ACCEPTANCE (G6): offline alert path demo passes; no credential
egress; feature-timestamp audit passes (anti-leak).

---
## 11. M10 — Deepfake / misinfo (`src/ws2_deepfake`)  [WS2; LOW-TRUST advisory]
```python
def authenticity_score(media) -> {score, features: {photometric, textural, geometric, compression, temporal}, cls}
```
RULES: interpretable features for auditability (R19); output is a LOW-TRUST advisory flag into fusion/operator
UI ONLY — never an autonomous trigger and never a sole basis for raising a level. EULA-restricted training sets
(DFDC/FF++/FakeAVCeleb = D158-D160) must not be redistributed; verify license before any use. ACCEPTANCE: runs
offline at gateway; output clearly labeled low-trust/advisory with its contributing features.

---
## 12. Configuration & feature flags (`configs/`)
Declarative (hydra/yaml). Flags: `fusion.model = FM-1|…|FM-6` (default FM-1); `fusion.operator.pharaoh =
off|on` (default off until P1–P7 verified); `firephys.nd[1..7] = off|on` (default off until `[coeff-verify]`);
`rl.algo = one_step|td3bc|cql|iql` (baseline-first; higher only after OPE gate); `quant = none|ptq_int8|qat`;
`lora.band = IN865_867` (fixed). Every Class-C flag emits a provenance note into `Decision.contributions`.

## 13. Test matrix (maps to gates)
| Test suite | Covers | Gate |
|------------|--------|------|
| `tests/physics_golden/` | geo saturated/steady-state/α-linearity; fire ND synthetic + coeff presence | G1 |
| `eval/` protocol tests | spatial-CV present, baseline+CI present, cost-loss, F-17 real-win | G2 |
| `tests/decision/` | single decide() path; shield totality/realizability; conformal PICP under drift | G3 |
| `tests/fusion/` | meta-head coeff stability; reliability down-weighting; shield-floor monotonicity; PHARAOH P1–P7 | G4 |
| `tests/iot/` | BOM ≤₹2,000; tier feasibility; single-node-cannot-RED; LoRa band | G5 |
| `tests/security/` | endpoint allow-list; no-raw-video-egress; offline alert path; timestamp anti-leak | G6 |
| `tests/repro/` | dataset license presence; datacube size; Kaggle-h budget; seed/fold logging | G7 |

## 14. Build-time open items (must resolve before the owning module ships)
`[coeff-verify]` for EF-13..EF-20 + Caine/Iverson/Fukuzono constants; CR-01 SAR EO-FM trade study; supplier
price re-verification (G5); India dataset-portal + license verification (Bhuvan/MOSDAC/VEDAS/NRSC/IMD/CWC/GSI);
full-text reads for exact hyperparameters (2503.07371, 2607.03131, 2610.09208, 2406.17813, 2406.17488);
numerical verification of PHARAOH properties + FM hyperparameters; expert review of all Class-C blocks;
LoRa IN865–867 regulatory confirmation; build the disaster-evac RL env + ≥100-seed eval.
