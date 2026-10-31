# 16 — Code Guide: Repository Map, Architecture, and API Reference

> **Audience:** a new engineer who must navigate and extend `trinetra/` without opening every file first.
> **Scope:** this chapter documents ONLY code that exists in the repository and was read line-by-line while
> writing it. Every class/function/signature below was copied from the source, not invented. Where a fact is
> measured in this environment it is tagged `[CONFIRMED]`; design-level intent that is not independently
> re-verified is `[LIKELY]`; an unvalidated idea is `[HYPOTHESIS]`.
>
> **Two load-bearing facts (from `_CANON.md §2`, re-verified against the code):**
> - The **pure-numpy core** runs here: `python run_tests.py` → **128 tests OK**, `python scripts/ci_gates.py`
>   → **ALL 6 CI GATES PASSED**. `[CONFIRMED]`
> - The **`deep/` (PyTorch) layer** and the **`kaggle/` scripts** are **`py_compile`-clean only** — they were
>   **never run on a GPU** here (no torch/CUDA in the authoring sandbox: numpy, pandas, lxml only). `[CONFIRMED]`
>
> No TRINETRA model has been trained and no dataset downloaded; nothing in this chapter is a measured
> performance result. See chapters 05 (models), 06 (physics + fusion), 12 (evaluation) and 17 (testing) for
> the companion detail, and 18 for the zero-to-run runbook.

---

## 16.1 How to read this chapter

TRINETRA's code is organized by **workstream package** under `src/trinetra/`, each mapping to a milestone
(M0–M10) and a design component (C-xxx) from `DESIGN/COMPONENT_DESIGN.md`. The mental model you need before
touching anything:

1. Everything flows into **one** function — `ws5_fusion_rl.decision.decide()`. There is exactly one decision
   path. Every workstream's job is to produce a list of `ExpertOutput`; `decide()` fuses them, applies the
   safety shield, and returns an advisory `Decision`.
2. The core is **torch-free**. Physics, fusion math, conformal calibration, cost-loss evaluation, the LoRa
   codec, and the CAP builder are all pure numpy + stdlib, and they run and are tested now.
3. The deep models live in a **quarantined** package (`trinetra.deep`) that imports torch. They never issue
   alerts; they only emit probabilities that an *adapter* turns into an `ExpertOutput`. They export their
   learned weights to numpy so the offline gateway can run them without torch.

Read §16.2 (the map) first, then §16.3 (the layering rule), then jump to the §16.5 API table for the package
you own.

---

## 16.2 REPOSITORY MAP

### 16.2.1 Top-level tree

```
trinetra/
├─ README.md                 maps each module → its DESIGN doc + research artifact; honesty posture
├─ pyproject.toml            py>=3.11; core deps = numpy,pandas,lxml; [deep]/[dev] extras; CI invariants
├─ requirements-deep.txt     pinned torch stack for Kaggle GPU training (NOT installed in base sandbox)
├─ CODE_INVENTORY.md         file-by-file build log + LOC totals (the source for the numbers below)
├─ run_tests.py              stdlib-unittest runner for the 128 numpy-core tests
├─ MODEL_CARDS.md            per-model honesty cards
├─ src/trinetra/             the importable package (numpy core + quarantined deep/)
├─ configs/                  JSON configs (no pyyaml here); safe-by-default feature flags
├─ scripts/                  ci_gates.py (6 safety/honesty gates), bom_price_check.py (≤₹2000)
├─ kaggle/                   one training kernel per deep model (+ fusion head export)
├─ firmware/                 FIRMWARE_SPEC.md (Tier-0 node spec)
└─ tests/                    128 tests across 9 suites (stdlib unittest)
```

**LOC figures (from `CODE_INVENTORY.md`, §Totals):** `src ≈ 3362 LOC`, `tests ≈ 917 LOC (128 tests)`,
`kaggle ≈ 316 LOC`. These are the canonical sizes; per-file LOC below are also from `CODE_INVENTORY.md`.

### 16.2.2 `src/trinetra/` package map (numpy core unless marked)

```
src/trinetra/
├─ common/                   contracts & infrastructure (dependency-light: dataclasses/enums + stdlib)
│  ├─ types.py        (118)  Level, Hazard, PhysicsClass, Reliability, ExpertOutput, Evidence,
│  │                         ShieldResult, ConformalResult, Decision — the canonical data contracts
│  ├─ config.py       (61)   JSON config loader + safe DEFAULTS; p_star = C_FA/(C_FA+C_miss)
│  ├─ security.py     (32)   endpoint allow-list (C6) + no-raw-video-egress scanner (C7); fail-closed
│  ├─ tracing.py      (16)   new_trace_id() + append-only JSONL audit log (Rule 19 explainability)
│  └─ exceptions.py   (16)   TrinetraError hierarchy: MissingDependency, SafetyViolation, LeakageError…
│
├─ eval/                     M0 admission harness — built FIRST; nothing may claim performance before it
│  ├─ splits.py       (34)   spatial_block_kfold, temporal_split, assert_no_time_leak (G6)
│  ├─ value_score.py  (39)   cost-loss Value Score, p*, alarms_from_prob, climatology_cost
│  ├─ baselines.py    (44)   climatology, persistence, physics_rule, LogisticNumpy (the beat-me set)
│  ├─ real_win.py     (46)   paired block-bootstrap "real win" with BCa CI (G2/F-17)
│  ├─ _stats.py       (68)   norm_cdf/ppf (Acklam), bca_interval, stationary_bootstrap_indices
│  ├─ calibration.py  (95)   ECE/MCE, reliability curve, Brier decomposition, Isotonic/Platt recalibrators
│  └─ report.py       (50)   ReportGuard — refuses a headline metric without spatial-CV + baselines + CI (R16)
│
├─ ws1b_geophys/            M1 geo physics gate (Class A/B): landslide/flood/GLOF
│  ├─ fs.py          (34)    infinite-slope Factor of Safety; suction→0 at saturation
│  ├─ iverson.py     (68)    Iverson(2000) transient head; slope only via D1=D0/cos²β; + multipulse superposition
│  ├─ fukuzono.py    (71)    inverse-velocity failure time (α=2) + WLS + prediction interval on t_f
│  ├─ caine.py       (16)    Caine intensity-duration rainfall threshold (locally-fit a,b)
│  └─ gate.py        (71)    noisy-OR combine of the above → one geo ExpertOutput + consistency
│
├─ ws1a_firephys/           M1 fire physics (Class A established + Class C novel, flag-gated OFF)
│  ├─ established_ef.py (41) Heskestad flame height, Strouhal puffing, Byram Nc, gray-body radiation (Class A)
│  ├─ novel_nd.py    (62)    ND-1 de-aliased flicker, ND-2 smoke-transmittance temp, ND-3 ignition index (Class C)
│  └─ gate.py        (64)    fuse detector confidence + physics plausibility → fire ExpertOutput; reports used_classC
│
├─ ws5_fusion_rl/           M5/M6 fusion, hierarchy, shield, THE decision, and RL (the hub)
│  ├─ nf.py          (52)    NF-1 consistency, NF-2 reliability, NF-3 conflict→uncertainty, NF-4 salience, eff. weight
│  ├─ pharaoh.py     (38)    PHARAOH power-mean operator (Class C, opt-in); ρ=1+κ·D·S
│  ├─ fusion_models.py (62)  FM-1 precision-weighted mean (default) + dispatcher (FM-1/GMF/PHARAOH)
│  ├─ gmf.py         (67)    Gated-Mixture Fusion w/ hard-bounded residual; load_numpy_head for offline use
│  ├─ correlation.py (67)    BLUE/GLS correlation-aware weights (redundant sensors stop double-counting)
│  ├─ hierarchical.py (88)   two-layer fusion: fuse_group → one expert; decide_hierarchical → single decide()
│  ├─ adapters.py    (35)    deep_expert(source, prob, …) → ExpertOutput w/ class + reliability cap (torch-free)
│  ├─ shield.py      (37)    monotone hard safety floor (can only RAISE); single node cannot reach RED
│  ├─ decision.py    (83)    decide(): level = max(conformal_level(risk,p*), shield_floor)  ← THE single path
│  └─ rl.py          (62)    RuleBaselinePolicy, OfflineRLPolicy (stub), WIS value, ope_admission gate
│
├─ ws6_robust/             M4 calibration under shift & drift
│  ├─ conformal.py   (124)   split-CP + WCPS + AdaptiveConformal (ACI) + MondrianConformal + conformal_risk_threshold
│  ├─ drift_monitor.py (38)  PSI + CUSUM drift detection → voids CP guarantees
│  └─ missing_modality.py (23) absent modality → unavailable + others more uncertain (C8)
│
├─ ws8_anomaly/__init__.py (67)  numpy anomaly ensemble: AR(1) residual + iForest-lite + Mahalanobis-lite (always-on)
├─ ws4_cctv/__init__.py   (40)   EdgeDetector interface (needs torch) + TemporalValidator (numpy false-alarm suppressor)
├─ ws1b_eo/__init__.py    (28)   EOEncoder frozen interface (needs torch) + deterministic hashing fallback (tests only)
├─ ws2_deepfake/__init__.py (31) DeepfakeDetector interface + heuristic_authenticity + authenticity_expert (low-trust)
│
├─ ws7_iot/                M7 IoT node (≤₹2000 node, offline uplink)
│  ├─ lora_codec.py        encode_frame/decode_frame; 25-byte frame (≤51 B budget); IN865-867
│  ├─ sensor_reading.py    SensorReading contract + HMAC sign/verify + ReplayGuard + validate_reading
│  └─ edge_screen.py       node_local_edge_flag — Tier-0 two-cue LOCAL_SIREN rule (never a public alert)
│
├─ ws3_alert/             M8 alerting (human-gated)
│  ├─ cap.py               build_cap — CAP 1.2 XML, refuses without an APPROVED: token (lxml)
│  ├─ operator.py          present(decision) briefing + approve() → "APPROVED:<id>" token
│  ├─ dtn.py               DTNQueue — binary spray-and-wait store-carry-forward (cloud-down path)
│  └─ siren.py             SirenBus — local siren actuation log (the one autonomous actuation)
│
├─ pipeline/              M10 orchestration
│  ├─ orchestrator.py      run_geo_cycle / run_fire_cycle / offline_dispatch — assemble experts → decide()
│  ├─ hindcast.py          run_hindcast — replay an event under the full admission gate (R16)
│  └─ demo.py              end-to-end synthetic advisory demo (python -m trinetra.pipeline.demo)
│
└─ deep/                  PyTorch models — Kaggle GPU only; py_compile-verified, NOT run here
   ├─ layers.py    (66)    MLP, Chomp1d/TemporalBlock/TCN (causal), ConvBNAct
   ├─ losses.py    (46)    Richards/Iverson PDE residual, differentiable FS, Strouhal, Deep-SVDD, cost-sensitive BCE
   ├─ geo_pinn.py  (67)    Model 1: GeoPINN (physics-informed slope hydrology → FS/risk) [Class A/B]
   ├─ fire_cnn.py  (58)    Model 2: FireSmokeNet (CNN→GRU + Strouhal aux, aux OFF by default) [Class A+data]
   ├─ eo_encoder.py (50)   Model 3/4: EODownstream (frozen EO foundation encoder + head) [Class data]
   ├─ anomaly_deep.py (68) Model 4: DeepAnomaly (TCN AE + forecast + Deep-SVDD) [Class data]
   ├─ deepfake_net.py (49) Model 5: AuthenticityNet (RGB+FFT two-stream, LOW trust) [Class data]
   ├─ offline_rl.py (67)   Model 6: CQLPolicy (conservative Q-learning, shielded, OPE-gated) [Class advisory]
   ├─ fusion_head.py (99)  GMFHead + AttentionFusionHead + export_numpy / export_attention_numpy bridges [Class B]
   ├─ datamodules.py (87)  Kaggle dataset paths + Dataset classes + spatial_block assignment
   ├─ train.py     (~190)  seeds, DataParallel (T4×2), spatial-CV, temperature calibration, admit_model gate
   └─ ddp.py       (70)    DistributedDataParallel launcher (mp.spawn, DistributedSampler, rank-0 save)
```

### 16.2.3 `tests/`, `kaggle/`, `scripts/`, `configs/`, `firmware/`

```
tests/            128 tests (stdlib unittest), 9 suites → gates G1–G6 (see chapter 17):
  physics_golden/ geo saturated/steady/α-linearity, Iverson multipulse, Fukuzono CI, fire (G1)
  eval/           spatial-CV present, cost-loss, real-win, calibration, _stats (G2)
  decision/       single decide() path, bands monotone, shield only raises, fail-safe uncertain (G3)
  fusion/         FM/GMF/adapters/hierarchical+correlation; PHARAOH ≥ mean; single-node≠RED (G4)
  robust/         split-CP coverage, ACI/Mondrian/CRC, PSI/CUSUM drift, missing modality (G3)
  iot/            frame ≤51 B, codec round-trip, HMAC sign/verify, replay reject, edge screen (G5)
  alert/          CAP refused without token, Level→severity mapping, DTN spray/deliver (G6)
  interfaces/     anomaly/cctv/eo/rl/deepfake stubs raise MissingDependency; OPE gates (contract)
kaggle/           train_geo_pinn.py, train_classifier.py (fire/eo/deepfake), train_anomaly.py,
                  train_offline_rl.py (OPE gate), train_fusion_head.py (+numpy export), README.md
scripts/          ci_gates.py (6 gates), bom_price_check.py (both nodes ≤₹2000)
configs/          default.json, fusion.json, firephys.json  (JSON, not yaml — pyyaml absent)
firmware/         FIRMWARE_SPEC.md
```

---

## 16.3 ARCHITECTURE OF THE CODE — the layering rule

The single most important architectural invariant is the **numpy/torch split**, stated in
`CODE_INVENTORY.md`, `README.md §Environment`, and `deep/__init__.py`:

> **The pure-numpy core must import and run without torch.** torch is confined to `trinetra.deep`.

### 16.3.1 Why the split exists

The edge gateway and CI run in environments where torch is heavy, absent, or impossible. Life-safety logic
(physics gates, fusion, the shield, conformal calibration, the decision function, alerting) therefore lives
in numpy-only code that runs anywhere. The authoring/CI sandbox literally has only `numpy, pandas, lxml`
(`_CANON.md §2`), and the 128 tests + 6 gates pass under exactly that constraint. `[CONFIRMED]`

### 16.3.2 How the two layers connect

The connection is **one-directional and weight-only**:

```
   trinetra.deep  (torch, Kaggle GPU)                     numpy core (edge/CI)
   ─────────────────────────────────                      ────────────────────
   GeoPINN / FireSmokeNet / EODownstream /                ws5_fusion_rl.adapters.deep_expert(source, prob)
   DeepAnomaly / AuthenticityNet / CQLPolicy    ── prob →        → ExpertOutput(cls, r-cap)
            │                                                            │
   fusion_head.GMFHead / AttentionFusionHead                            ▼
            │  export_numpy / export_attention_numpy          ws5_fusion_rl.decide(experts, shield)
            └──────── JSON weights ────────►  gmf.load_numpy_head(json) ─┘   → advisory Decision
```

- A trained deep model produces a **scalar calibrated probability**. It never sees a `Decision` and never
  issues an alert (`deep/__init__.py`, Rule 19).
- `ws5_fusion_rl.adapters.deep_expert(source, prob, …)` wraps that probability in an `ExpertOutput` with the
  correct `PhysicsClass` and a **reliability cap** per source (deepfake hard-capped at 0.4). This is
  deliberately torch-free so the gateway can assemble experts from *cached* model scores.
- The learned fusion heads export their weights to a **pure-numpy closure**:
  `deep.fusion_head.export_numpy(head)` / `export_attention_numpy(head)` and
  `ws5_fusion_rl.gmf.load_numpy_head(json)` reconstruct the forward pass with numpy only, so the offline
  gateway runs `gmf_fuse(..., head=closure)` with no torch import. The residual is still hard-clipped (defense
  in depth) so a mis-trained head can never dominate physics.

### 16.3.3 The three invariants the architecture enforces in code

1. **Single decision path.** Only `ws5_fusion_rl.decision.decide()` produces a `Decision`. `pipeline/` and
   `hierarchical.decide_hierarchical()` both call it; they never re-implement the rule. (gate G3)
2. **Shield can only raise.** `decide()` computes `level = Level.raise_to(conformal_point, shield_floor)`.
   The shield is monotone and post-posed; fusion math can never lower it. (gates G3/G4)
3. **Honesty metadata rides on the contract.** Every `ExpertOutput` carries `cls` (A/B/C/DATA/ADVISORY) and
   `r` (reliability); every `Decision` carries `advisory=True`, `uncertain`, and `used_classC`. (Rule 20)

---

## 16.4 THE DATA CONTRACTS (what flows between stages)

The whole system is wired by the dataclasses in `common/types.py`. Internalize these and the data flow is
obvious. (Signatures below are verbatim from the source.)

### 16.4.1 The enums

| Enum | Members | Notes |
|------|---------|-------|
| `Level(IntEnum)` | `GREEN=0, YELLOW=1, ORANGE=2, RED=3` | Ordered so the shield can `max()`. Helpers: `Level.raise_to(a,b)`, `.label`. |
| `Hazard(str,Enum)` | `LANDSLIDE, FLASHFLOOD, CLOUDBURST, GLOF, FIRE` | Hazard tag on each decision. |
| `PhysicsClass(str,Enum)` | `A="A", B="B", C="C", DATA="data", ADVISORY="advisory"` | Rule 20 label. C = novel/unvalidated. |
| `Reliability(str,Enum)` | `HIGH, MEDIUM, LOW, UNRELIABLE` | Conformal reliability flag surfaced to the operator. |

### 16.4.2 `ExpertOutput` — the universal currency

```python
@dataclass
class ExpertOutput:
    p: float                      # calibrated probability in [0,1]
    source: str
    u: float = 0.0                # uncertainty [0,1]
    c: float = 1.0                # physics-consistency [0,1] (NF-1)
    r: float = 1.0                # reliability/trust [0,1] (NF-2)
    cls: PhysicsClass = PhysicsClass.DATA
    available: bool = True
    # __post_init__ raises ValueError if any of p,u,c,r leaves [0,1]
```

Every workstream — physics gate, anomaly ensemble, CCTV, deepfake, deep model — emits an `ExpertOutput`. This
is the contract the fusion head consumes. An absent modality sets `available=False` (never a fake probability).

### 16.4.3 `Evidence` — the per-zone observation bundle (anti-leak)

```python
@dataclass
class Evidence:
    zone_id: str
    t: datetime                                 # feature timestamp; MUST be <= decision time (G6)
    eo: dict | None = None                      # InSAR/S2/IMERG/SMAP/ERA5/active-fire
    vision: dict | None = None                  # detector boxes, LSPIV stage, flicker/flow, VAD
    iot: dict | None = None                     # tilt, soil, piezo, rain, T/P + health
    quality: dict = {}                          # per-modality reliability in [0,1]
    provenance: dict = {}                       # source ids, versions, seed, fold_id
    window: dict | None = None
    missing: list[str] = []                     # modalities absent this window
    schema_version: str = "1.0"
```

### 16.4.4 `ShieldResult`, `ConformalResult`, `Decision`

```python
@dataclass
class ShieldResult:
    floor: Level; raised: bool; reason: str | None

@dataclass
class ConformalResult:
    pred_set: list[str]; coverage_target: float; reliability: Reliability

@dataclass
class Decision:
    zone_id: str; t: datetime; hazard: Hazard; level: Level; risk: float
    conformal: ConformalResult; shield: ShieldResult
    contributions: list[ExpertOutput] = []
    uncertain: bool = False        # Rule 19 fail-safe (abstain + escalate, never silent)
    advisory: bool = True          # ALWAYS true; human-in-the-loop
    used_classC: bool = False      # Rule 20 transparency
    model_versions: dict = {}; trace_id: str | None = None; schema_version: str = "1.0"
    def to_dict(self) -> dict      # JSON-serializable (isoformat t, enum→name, flattened conformal/shield)
```

### 16.4.5 The data-flow contract, end to end

```
sensors/models ─▶ ExpertOutput (p,u,c,r,cls,available)        per workstream
   geo_gate   → GeoResult(FS, caine_ratio, t_failure, p_phys, expert)
   fire_gate  → FireResult(p_fire, consistency, used_classC, diagnostics, expert)
   anomaly    → anomaly_ensemble(X[,series]) → p ∈[0,1] → ExpertOutput(source="anomaly", cls=DATA)
   deep model → prob → adapters.deep_expert(source, prob) → ExpertOutput

[list of ExpertOutput]
   └─▶ fusion_models.fuse(experts, cfg) → FusionResult(p, u_star, salience, model, used_classC)
        (FM-1 default | GMF | PHARAOH; NF-3 gives u_star; NF-4 gives salience)

decide(experts, shield_signals, cfg):
   point   = conformal_level(fused.p, p_star[, level_thresholds])     # risk band
   floor   = shield_floor(shield_signals)                             # ShieldResult (monotone)
   level   = Level.raise_to(point, floor.floor)                       # shield can only raise
   uncertain = (no experts) or (u_star > 0.6) or drift
   → Decision(level, risk=fused.p, conformal, shield, contributions, uncertain, used_classC)

operator.present(decision) → human → operator.approve(decision, id) → "APPROVED:<id>"
   → cap.build_cap(decision, token) → signed CAP 1.2 XML   (refuses without the token)
```

What each stage **produces → consumes**:
- an **encoder/physics/anomaly** stage produces an `ExpertOutput` (prob + uncertainty + consistency +
  reliability + class);
- **fusion** consumes a `list[ExpertOutput]` and produces a `FusionResult` (a single fused `p` plus
  conflict-aware `u_star` and `salience`);
- **`decide()`** returns a `Decision` whose `level` is the shield-floored conformal band and whose
  `contributions` carry the full audit trail.

---

## 16.5 PER-PACKAGE API REFERENCE

Signatures are copied from the source. Defaults shown where they matter. "→" is the return.

### 16.5.1 `common/`

| Symbol | Signature | Does |
|--------|-----------|------|
| `Config` | `Config(data=DEFAULTS)` | Holds merged JSON config. |
| `Config.get` | `get(dotted:str, default=None)` | Dotted-key lookup, e.g. `cfg.get("fusion.tau",0.5)`. |
| `Config.p_star` | property → `float` | `C_FA/(C_FA+C_miss)` (≈0.0476 with 5/100). |
| `Config.require_human_approval` | `() → True` | **Hard-wired True**; config cannot disable the human gate (R19). |
| `load_config` | `load_config(*names, config_dir=None) → Config` | Loads `default.json` then deep-merges each named config. |
| `check_endpoint` | `check_endpoint(url, allowlist) → url` | Returns url iff host on allow-list, else raises `EndpointNotAllowed` (C6). |
| `assert_no_video_egress` | `assert_no_video_egress(payload: dict) → None` | Raises `SafetyViolation` if any video-like key present (C7). |
| `new_trace_id` | `() → "tr-<hex16>"` | Trace id for audit. |
| `audit` | `audit(record: dict, path="data/audit.jsonl")` | Appends one timestamped JSON line. |

Exceptions (`common/exceptions.py`): `TrinetraError` base; `MissingDependency` (heavy lib absent — raised
instead of faking a result), `SafetyViolation` (R19 fail-closed), `LeakageError` (feature t > decision t),
`EndpointNotAllowed` (C6), `SchemaError`.

Config `DEFAULTS` (safe-by-default, `config.py`): `cost={C_FA:5, C_miss:100}`; `fusion.model="FM-1"`,
`fusion.operator.pharaoh=False`; `firephys.nd1..nd7=False`; `rl.algo="one_step"`, `rl.ope_gate=True`;
`calib.alpha=0.1`, `calib.wcps=True`; `cctv.quant="none"`; `iot.lora_band="IN865_867"`;
`alert.require_human_approval=True`.

### 16.5.2 `ws1b_geophys/` — geo physics (Class A/B)

| Symbol | Signature | Does |
|--------|-----------|------|
| `factor_of_safety` | `(c_prime, phi_prime_deg, gamma, z, beta_deg, u_w=0.0, sigma_s=0.0) → FS` | Infinite-slope FS; `σ'_n = γz cos²β − u_w + σ_s`; array-broadcastable; raises if driving stress ≤0. |
| `factor_of_safety_saturated` | `(c_prime, phi_prime_deg, gamma, z, beta_deg, u_w=0.0)` | Saturated limit (`σ_s=0`); the golden-test target. |
| `pore_pressure_from_head` | `(psi_m, gamma_w=9.81) → u_w [kPa]` | Head → pore pressure. |
| `ierfc` | `(x) → ierfc(x)` | Integral complementary error fn (`ierfc(0)=1/√π`); uses stdlib `math.erfc` (no scipy). |
| `diffusivity_D1` | `(D0, beta_deg) → D0/cos²β` | **The only place slope enters the transient response** (bug-guard). |
| `transient_head` | `(Z, t, D0, K_z, I_z, beta_deg) → ψ_transient [m]` | Iverson transient rise. |
| `pressure_head` | `(Z, t, D0, K_z, I_z, beta_deg, psi_steady=0.0)` | Steady + transient head. |
| `transient_head_multipulse` | `(Z, t_eval, step_times, step_intensities, D0, K_z, beta_deg)` | Linear superposition over a piecewise-constant rainfall history (`Σ (I_k−I_{k−1})/K_z · R(Z,t−t_k)`); recovers `ψ=(I/Kz)[R(Z,t)−R(Z,t−T)]` after rain stops. |
| `inverse_velocity_fit` | `(times, velocities, alpha=2.0, *, weights=None, recency_halflife=None, z=1.96) → FukuzonoFit` | Weighted inverse-velocity fit; `t_f` + prediction interval via delta method. |
| `FukuzonoFit` | dataclass `t_failure, alpha, slope, r2, regime_note, t_failure_low/high, se_t_failure` | Carries forecast uncertainty (R19). |
| `caine_threshold` | `(D_hours, a, b) → I_thr [mm/h]` | `I = a·D^(−b)`. |
| `caine_exceedance` | `(I_mm_h, D_hours, a, b) → (exceeded_bool, ratio)` | `ratio>1` ⇒ above the ID line. |
| `geo_gate` | `(gi: GeoInputs, k_fs=4.0) → GeoResult` | Combines FS/Iverson/Caine/Fukuzono by **noisy-OR**; emits `ExpertOutput(source="geo_phys", cls=A)`. |

`GeoInputs` (dataclass): slope/soil (`c_prime, phi_prime_deg, gamma, z, beta_deg, sigma_s`), optional Iverson
infiltration (`D0, K_z, I_z, t_hours, psi_steady`), rainfall (`I_mm_h, D_hours, caine_a=14.0, caine_b=0.39`),
creep (`fukuzono: FukuzonoFit, now_hours`). `GeoResult`: `FS, caine_ratio, t_failure, p_phys, expert`.

### 16.5.3 `ws1a_firephys/` — fire physics (Class A + Class C flag-gated OFF)

| Symbol | Signature | Does |
|--------|-----------|------|
| `flame_height_heskestad` | `(Q_kW, D_m) → L [m]` | `L=0.235·Q^0.4 − 1.02·D`. Class A `[coeff-verify]`. |
| `strouhal_puffing_frequency` | `(D_m) → f [Hz]` | `f ≈ 1.5/√D` (EF-16). |
| `plume_centerline_dT` | `(Q_c_kW, z_m, z0_m=0, T_inf=293) → ΔT0 [K]` | Heskestad far-field centerline excess temp. |
| `byram_convection_number` | `(Q_c_kW_per_m, U_ms, rho=1.2, cp=1.0, T_inf=293, g=9.81) → N_c` | Regime check: `N_c>~2` plume-dominated. Used to reject non-fire regimes. |
| `graybody_radiance` / `graybody_temperature` | `(T_K[, emissivity]) ↔ (radiance[, emissivity])` | Stefan-Boltzmann forward/inverse. |
| `beer_lambert_transmittance` | `(kappa_sigma, path_m) → τ` | `τ=exp(−(κ+σ)L)`. |
| `aliased_frequency` | `(f_true_hz, fs_hz) → f_alias` | Frequency aliasing for sub-Nyquist cameras. |
| `nd1_dealiased_flicker` | `(f_obs_hz, fs_hz, D_prior_m, sigma_hz=0.3) → ND1Result` | **Class C.** Soft consistency vs Strouhal prediction (not a trigger). |
| `nd2_transmittance_temperature` | `(L_obs, tau_s, T_smoke_K, emissivity=1, sigma_L_frac=0.05) → ND2Result` | **Class C.** Recover plume T behind smoke; `σ_K` blows up as τ→0 (fail-to-uncertain). |
| `nd3_ignition_index` | `(terms: list[(w,scale,rate)]) → Π_ig ≥0` | **Class C.** Scene-invariant early-warning scalar. |
| `fire_gate` | `(fi: FireInputs, cfg=None) → FireResult` | Byram regime down-weights implausible fires; ND terms applied **only if the matching `firephys.ndX` flag is on**; emits `ExpertOutput(source="fire_phys", cls=A)` + `used_classC`. |

`FireInputs`: `detector_conf, multi_node_agree=False, Q_c_kW_per_m, wind_U_ms, nd1/nd2 dicts, nd3_terms`.
`FireResult`: `p_fire, consistency, used_classC, diagnostics, expert`.

### 16.5.4 `ws5_fusion_rl/` — fusion, shield, decision, RL (the hub)

**NF sub-formulas (`nf.py`):**

| Symbol | Signature | Does |
|--------|-----------|------|
| `nf1_consistency` | `(p_i, phi_physics, sigma=0.25, eps=1e-6) → c_i` | Penalizes claiming MORE alarm than physics supports (one-sided Gaussian). |
| `nf2_reliability` | `(r_prev, outcome_ok, drift_flag=False, lam=0.9, r_min=0.1, drift_penalty=0.5) → r` | Exp-forgetting reliability; drift multiplies down; clamped `[r_min,1]`. |
| `weighted_dispersion` | `(ps, weights) → D` | Weighted std of expert probabilities. |
| `nf3_conflict_to_uncertainty` | `(ps, u, weights, lam=0.3) → U*` | `U* = Σw·u + λ·D` (fail toward uncertain). |
| `nf4_salience` | `(experts) → S` | `max_i r_i·c_i·p_i` over available experts. |
| `effective_weight` | `(e, tau=0.5) → w̃_i` | `availability · r · c · exp(−u/τ)`. |

**Fusion operators and dispatcher:**

| Symbol | Signature | Does |
|--------|-----------|------|
| `fm1_precision_weighted` | `(experts, tau=0.5) → p` | **FM-1 (default/fallback):** effective-weighted arithmetic mean (Class B). |
| `fuse` | `(experts, cfg=None) → FusionResult` | Dispatcher: FM-1, or GMF (`fusion.model="GMF"`), or PHARAOH (if `operator.pharaoh` + ≥2 experts). Reports `used_classC`. |
| `pharaoh_order` | `(ps, weights, salience, kappa=2.0) → ρ∈[1,8]` | `ρ=1+κ·D·S` (adaptive order). |
| `pharaoh_mean` | `(ps, weights, rho) → p` | Weighted power mean (**Class C**). |
| `pharaoh_fuse` | `(experts, kappa=2.0) → {p, rho, salience, …}` | Full PHARAOH fuse with effective weights. |
| `gmf_fuse` | `(experts, tau=0.5, residual_cap=0.1, use_pharaoh_base=False, head=None) → GMFResult` | Gated mixture base + **hard-clipped** residual; `head=None` ⇒ residual 0 (reduces to precision mean). |
| `gated_weights` | `(experts, tau=0.5) → normalized w̃` | Mixture gate. |
| `bounded_residual` | `(base, experts, residual_cap=0.1, head=None) → r∈[−cap,cap]` | Optional learned residual, hard-clipped. |
| `load_numpy_head` | `(path_or_dict) → closure(feats)->float` | Loads an exported GMF head JSON into a pure-numpy closure for the offline gateway. |
| `correlation_adjusted_weights` | `(experts, corr=None, tau=0.5, ridge=1e-3) → weights` | BLUE/GLS min-variance weights; **non-negative-clipped** (R19 safety over optimality). |
| `blue_fuse` | `(experts, corr=None, tau=0.5) → p` | Correlation-aware fused probability. |
| `redundancy_matrix` | `(sources, redundant_groups, rho=0.8) → R` | Correlation matrix for sensors known to co-move. |
| `deep_expert` | `(source, prob, *, uncertainty=0.3, consistency=1.0, available=True, reliability=None) → ExpertOutput` | Wraps a deep prob with class + reliability cap; `deepfake` capped at 0.4; unknown source raises `KeyError`. |

**Hierarchical fusion (`hierarchical.py`):**

| Symbol | Signature | Does |
|--------|-----------|------|
| `fuse_group` | `(name, experts, cfg=None, *, corr=None, redundant_groups=None, rho=0.8) → ExpertOutput` | Layer-1: fuse one workstream's experts into one group expert; propagates `u` (NF-3), consistency, reliability, and a **conservative class** (weakest-guarantee member labels the group). |
| `hierarchical_fuse` | `(groups: dict[str,list], cfg=None, *, redundancy=None, rho=0.8) → list[ExpertOutput]` | Map each workstream to one group expert. |
| `decide_hierarchical` | `(groups, shield, cfg=None, *, hazard=LANDSLIDE, zone_id, t, redundancy=None, rho=0.8) → Decision` | Layer-2: feeds the group experts to the **same** `decide()` (no second path). |

**Shield and decision:**

| Symbol | Signature | Does |
|--------|-----------|------|
| `ShieldSignals` | dataclass `FS, tilt_rate_deg_per_day, nodes_agree=0, rain_24h_mm, high_susceptibility=False, glof_lake_drop=False, downstream_stage_jump=False, fire_multi_node=False` | Inputs to the hard shield. |
| `shield_floor` | `(s: ShieldSignals) → ShieldResult` | Deterministic monotone floor: FS<1 ⇒ ≥ORANGE; tilt>5°/day **corroborated by ≥2 nodes** ⇒ RED; 24h rain>150mm on high-susceptibility ⇒ ≥ORANGE; GLOF drop+stage jump ⇒ RED; fire multi-node ⇒ ≥ORANGE. A single node alone cannot reach RED. |
| `conformal_level` | `(risk, p_star, thresholds=None) → Level` | Bands at `p*, 4p*, 10p*` (or calibrated `(t_y,t_o,t_r)` from CRC). |
| `decide` | `(experts, shield_signals=None, cfg=None, *, hazard=LANDSLIDE, zone_id="UNKNOWN", t=None, drift=False, uncertain_threshold=0.6, trace_id=None, level_thresholds=None) → Decision` | **THE single decision function.** `level = raise_to(conformal_level(fused.p,p*), shield_floor)`; sets `uncertain`/`used_classC`; builds provisional conformal set. |

**Offline RL (`rl.py`):**

| Symbol | Signature | Does |
|--------|-----------|------|
| `RuleBaselinePolicy` | `RuleBaselinePolicy(threshold=0.0476)`; `.act(risk)→0/1` | Fixed-threshold alarm; the OPE comparator / honest fallback. |
| `OfflineRLPolicy` | `OfflineRLPolicy(algo="one_step")`; `.fit(dataset)` **raises `MissingDependency`** | Learned policy needs d3rlpy+torch; stub until trained + OPE-admitted. |
| `wis_value` | `(behavior_probs, target_probs, rewards) → (value, ess)` | Weighted importance-sampling OPE value + effective sample size. |
| `ope_feasible` | `(behavior_probs, min_prob=1e-2, min_ess_frac=0.1) → bool` | Positivity + ESS gate. |
| `ope_admission` | `(behavior_probs, target_probs, rewards, baseline_rewards) → OPEVerdict` | Admit learned policy iff feasible AND value ≥ baseline. |

### 16.5.5 `ws6_robust/` — calibration, drift, degradation

| Symbol | Signature | Does |
|--------|-----------|------|
| `conformal_quantile` | `(cal_scores, alpha=0.1) → q` | Finite-sample (1−α) quantile of nonconformity scores. |
| `regression_interval` | `(point_pred, cal_residuals, alpha=0.1) → (lo, hi)` | Symmetric split-CP interval. |
| `weighted_conformal_quantile` | `(cal_scores, cal_weights, alpha=0.1, test_weight=1.0) → q` | **WCPS** reweighted quantile for covariate shift. |
| `classification_set` | `(class_scores: dict, q) → list` | Prediction set `{label : score ≤ q}`. |
| `empirical_coverage` | `(lo, hi, y_true) → coverage` | Realized marginal coverage (honest reporting). |
| `AdaptiveConformal` | `AdaptiveConformal(alpha_target=0.1, gamma=0.02)`; `.quantile(cal)`, `.step(covered)→alpha`, `.realized_coverage` | **ACI** — long-run coverage under arbitrary drift. |
| `MondrianConformal` | `MondrianConformal(alpha=0.1)`; `.fit(groups,cal_scores)`, `.quantile(group)`, `.group_coverage(...)` | Per-group (per-hazard) coverage, not just marginal. |
| `conformal_risk_threshold` | `(cal_scores, cal_labels, target_risk=0.05, n_grid=200) → lambda_hat` | **CRC/RCPS** miss-rate-bounding alarm threshold (feeds `decide(level_thresholds=…)`). |
| `population_stability_index` | `(reference, current, bins=10, eps=1e-6) → PSI` | >0.1 moderate, >0.2 significant shift. |
| `cusum_update` | `(state: CusumState, x, target, k=0.5, h=5.0) → (state, drift_flag)` | One sequential CUSUM step. |
| `check_drift` | `(reference, current, psi_threshold=0.2) → DriftReport` | PSI-based drift verdict (voids CP ⇒ reliability Unreliable). |
| `apply_missing_modality` | `(experts, present_sources: set, penalty=0.15) → list[ExpertOutput]` | Absent → `available=False`; present → `u += penalty·n_missing` (C8). |

### 16.5.6 `eval/` — the M0 admission harness

| Symbol | Signature | Does |
|--------|-----------|------|
| `spatial_block_kfold` | `(block_ids, k=5, seed=0) → yields (train_idx, test_idx)` | Whole spatial block in exactly one fold (no spatial leakage). |
| `temporal_split` | `(times, train_frac=0.7) → (train_idx, test_idx)` | Train past, test future (no look-ahead). |
| `assert_no_time_leak` | `(feature_times, decision_time)` | Raises `LeakageError` if any feature t > decision t (G6). |
| `p_star` | `(C_FA, C_miss) → C_FA/(C_FA+C_miss)` | Optimal cost-loss alarm threshold. |
| `realized_cost` | `(y_true, alarms, C_FA, C_miss) → cost` | FA·C_FA + miss·C_miss. |
| `alarms_from_prob` | `(p_pred, C_FA, C_miss) → 0/1` | Alarm iff `p ≥ p*`. |
| `climatology_cost` | `(y_true, C_FA, C_miss)` | Best constant policy cost. |
| `value_score` | `(y_true, p_pred, C_FA, C_miss) → {value_score, E_forecast, E_climate, p_star, n, base_rate}` | `VS = 1 − E_fc/E_clim` (1 perfect, ≤0 no skill). |
| `base_rate_climatology` / `persistence` / `physics_rule` | see §16.5 tree | Mandatory non-learned baselines. |
| `LogisticNumpy` | `LogisticNumpy(l2=1e-3, lr=0.1, epochs=500, seed=0)`; `.fit(X,y)`, `.predict_proba(X)` | Pure-numpy L2 logistic baseline (standardizes internally). |
| `real_win` | `(y_true, p_model, p_baseline, block_ids, C_FA, C_miss, n_boot=2000, alpha=0.05, seed=0, ci_method="bca") → verdict` | Paired **block-bootstrap** cost-saving; `real_win=True` iff CI lower bound > 0. |
| `norm_cdf`/`norm_ppf`/`bca_interval`/`stationary_bootstrap_indices` | `_stats.py` | Acklam ppf, BCa interval, geometric-block bootstrap. |
| `reliability_curve`/`expected_calibration_error`/`maximum_calibration_error`/`brier_decomposition` | `calibration.py` | ECE/MCE + Murphy decomposition. |
| `IsotonicCalibrator` | `.fit(probs,y).predict(probs)` | Nonparametric PAV recalibration. |
| `PlattCalibrator` | `PlattCalibrator(iters=200, lr=0.1)`; `.fit`, `.predict` | Parametric 1-D logistic recalibration. |
| `ReportGuard` | `ReportGuard(spatial_cv=False)`; `.add_baseline_verdict(name, verdict)`, `.headline(metric, value)`, `.admit()`, `.summary()` | **R16 gate:** `headline()` raises `ReportGuardError` unless spatial-CV + a real win over **every** baseline. |

### 16.5.7 Other numpy workstreams

| Package | Public API | Does |
|---------|------------|------|
| `ws8_anomaly` | `forecast_residual_score(series, phi=None)`, `iforest_lite_score(X, n_trees=100, sample=64, seed=0)`, `mahalanobis_lite_score(X)`, `anomaly_ensemble(X, series=None, weights=(1,1,1))` | Always-on numpy anomaly ensemble → `p∈[0,1]`. |
| `ws4_cctv` | `EdgeDetector(backbone="yolov5n").detect(frame)` **raises `MissingDependency`**; `TemporalValidator(window=5, min_frames=3, conf_thr=0.5).update(frame_conf) → ValidatedEvent(confirmed, confidence, support_frames)` | Detector needs torch; the validator (numpy) is the false-alarm suppressor. |
| `ws1b_eo` | `EOEncoder(model_name="prithvi-frozen", dim=256).embed(patch)` **raises `MissingDependency`**; `.hashing_fallback(patch, seed=0)` (tests only, NOT a learned feature) | Frozen EO foundation encoder interface. |
| `ws2_deepfake` | `DeepfakeDetector(...).score(media)` **raises**; `heuristic_authenticity(cues) → [0,1]`; `authenticity_expert(cues, reliability=0.3) → ExpertOutput(source="deepfake", r≤0.4)` | Low-trust media authenticity. |
| `ws7_iot` | `encode_frame(node_id, seq, readings, batt_mV, edge_level="NONE") → bytes`; `decode_frame(buf) → dict`; `FRAME_LEN==25`; `SensorReading` + `sign_reading/verify_reading` (HMAC-SHA256 placeholder for Ed25519); `ReplayGuard().accept(node_id, seq)`; `validate_reading(r) → list[str]`; `node_local_edge_flag(readings, …) → {level, rule}` | Compact LoRa codec + signed reading + Tier-0 edge screen. |
| `ws3_alert` | `build_cap(decision, approval_token, *, sender, area_polygon=None, key=None) → CAP XML str` (raises `SafetyViolation` without an `APPROVED:` token or for GREEN); `cap_fields_for_level(level)`; `present(decision) → str`; `approve(decision, operator_id, acknowledge_advisory=True) → "APPROVED:<id>"`; `DTNQueue(L=8)` with `.enqueue/.relay/.deliver/.pending`; `SirenBus().fire(zone_id, level, source)` | Human-gated CAP + operator console + DTN mesh + local siren. |
| `pipeline` | `run_geo_cycle(geo_inputs, shield, feature_matrix, series=None, cfg=None, zone_id, t=None) → Decision`; `run_fire_cycle(...)`; `offline_dispatch(decision, node_edge_level, dtn, siren) → OfflineActions`; `run_hindcast(event, X, y, block_ids, p_model, C_FA=5, C_miss=100, seed=0) → HindcastResult` | Assemble experts → `decide()`; cloud-down path; honesty-gated hindcast. |

### 16.5.8 `deep/` — torch models (Kaggle GPU; py_compile-only here)

> Every class below imports torch and is **not importable in the base sandbox**. Verified by `py_compile`
> only; never GPU-run here (`_CANON.md §2`). `[CONFIRMED]`

| Symbol | Signature | Does |
|--------|-----------|------|
| `MLP` / `TCN` / `TemporalBlock` / `Chomp1d` / `ConvBNAct` | `layers.py` | Reusable blocks; TCN is **causal** (anti-leak, G6). |
| `richards_iverson_residual(psi, Z, t, D1)` | `losses.py` | PDE residual `ψ_t − D1·ψ_ZZ`; slope only via D1 (bug-guard mirrored). |
| `factor_of_safety_torch(c_prime, phi_deg, gamma, z, beta_deg, u_w, sigma_s=0)` | `losses.py` | Differentiable FS (matches numpy gate). |
| `strouhal_consistency_loss`, `deep_svdd_loss`, `cost_sensitive_bce`, `brier_score` | `losses.py` | Physics/honesty-aware training losses. |
| `GeoPINN(cfg=GeoPINNConfig())` | `geo_pinn.py` | **Model 1.** `.forward(Z,t,rain,static) → {logit,prob,psi,fs}`; `.physics_loss(...)`; `geo_pinn_step(model,batch,D1,bce)` (rebuilds Z,t as leaves so autograd works under DataParallel). |
| `FireSmokeNet(cfg=FireNetConfig())` | `fire_cnn.py` | **Model 2.** CNN→GRU; `.forward(x)→{logits,prob,flicker_hz}`; `.loss(...)` with Strouhal aux (weight 0 default). |
| `EODownstream(cfg=EOConfig(), encoder_factory=None)` | `eo_encoder.py` | **Model 3/4.** Frozen timm/FM encoder + MLP head; `.forward(x)→{logit,prob}`. |
| `DeepAnomaly(cfg=AnomalyConfig())` | `anomaly_deep.py` | **Model 4.** TCN AE + forecast + Deep-SVDD; `.init_center(...)`, `.loss(x)`, `.anomaly_score(x)`. |
| `AuthenticityNet(cfg=DeepfakeConfig())` | `deepfake_net.py` | **Model 5.** RGB + FFT two-stream; `.forward(x)→{logit,p_fake}`; `max_reliability=0.4`. |
| `CQLPolicy(cfg=CQLConfig())` | `offline_rl.py` | **Model 6.** `ACTIONS=("HOLD","WATCH","ALARM")`; `.cql_loss(s,a,r,s_next,done)`; `.act(s, shield_floor_idx=0)` (raised to shield floor); `.action_probs(s)` for OPE. |
| `GMFHead(hidden=16)` | `fusion_head.py` | Learned bounded residual over `[base,dispersion,salience]`. |
| `AttentionFusionHead(feat_dim=4, hidden=16, cap=0.1)` | `fusion_head.py` | Attention over per-workstream experts; convex base (bounded to `[min p_i, max p_i]`) + bounded residual. `.loss(out, target, c_fa, c_miss)` cost-sensitive BCE. |
| `export_numpy(head, cap=0.1)` / `export_attention_numpy(head)` | `fusion_head.py` | **The numpy export bridge** — serialize a trained head to a pure-numpy closure for the torch-free gateway. |
| `set_seed`, `get_device`, `n_gpus`, `setup_perf`, `TrainConfig`, `make_loader`, `train_one_fold`, `TemperatureScaler`, `admit_model`, `spatial_cv_indices` | `train.py` | Multi-GPU (T4×2 DataParallel) trainer; temperature calibration; `admit_model` runs the full R16 gate + ECE/MCE/Brier diagnostics. |
| `ddp_setup/cleanup`, `is_main`, `wrap_ddp`, `ddp_sampler`, `ddp_loader`, `launch_ddp`, `ddp_worker` | `ddp.py` | DistributedDataParallel launcher (one process per GPU, rank-0 save). |

---

## 16.6 CONFIG SYSTEM

### 16.6.1 Where config lives and how it loads

Configs are **JSON** under `configs/` (not yaml — `pyyaml` is unavailable; `README.md §Environment`). The
loader in `common/config.py`:

1. starts from the in-code `DEFAULTS` dict (the safe path);
2. `load_config("fusion","firephys")` deep-merges `default.json`, then each named file on top;
3. parameters are read with dotted keys: `cfg.get("fusion.tau", 0.5)`, `cfg.get("firephys.nd1", False)`.

The three shipped files are intentionally minimal (defaults carry the rest):

```json
// configs/default.json
{ "seeds":[0,1,2,3,4], "cost":{"C_FA":5.0,"C_miss":100.0}, "alert":{"require_human_approval":true} }
// configs/fusion.json
{ "fusion":{"model":"FM-1","operator":{"pharaoh":false},"tau":0.5,"lambda":0.3} }
// configs/firephys.json
{ "firephys":{"nd1":false,...,"nd7":false} }
```

### 16.6.2 The cost model and p*

`cost.C_FA=5`, `cost.C_miss=100` ⇒ `Config.p_star = C_FA/(C_FA+C_miss) ≈ 0.0476`. This single number drives
(a) `eval.value_score.alarms_from_prob` (alarm iff `p ≥ p*`), (b) `conformal_level` bands at `p*, 4p*, 10p*`,
and (c) `RuleBaselinePolicy(threshold=0.0476)`. Change the asymmetry here and the whole decision policy
re-tunes consistently. (Matches `_CANON.md §4`.)

### 16.6.3 Class-C default-OFF flags (Rule 20)

The safety-critical flags, all **False by default**:
- `fusion.operator.pharaoh` — PHARAOH power-mean (Class C). Off ⇒ dispatcher falls back to FM-1.
- `firephys.nd1 … nd7` — novel fire-physics soft features (Class C). Off ⇒ `fire_gate` omits them.

`scripts/ci_gates.py` (`G-classC`) asserts all of these are `False`, and `Config.require_human_approval()` is
hard-wired `True` (`G-advisory`). This is why enabling a Class-C path is a deliberate, auditable act: the flag
must be flipped in a config, and when it is on, `used_classC=True` propagates into the `Decision` and the CAP
parameters.

---

## 16.7 CONVENTIONS

### 16.7.1 Naming
- Packages are `wsN<name>` matching the design workstreams (`ws1b_geophys`, `ws5_fusion_rl`, …). The doc-frame
  → artifact → package mapping is in `_CANON.md §3`; always say which scheme you mean.
- Each package `__init__.py` re-exports its public API in `__all__`; import from the package, not the module
  (`from trinetra.ws5_fusion_rl import decide`).
- Dataclasses pair a `…Inputs`/`…Config` with a `…Result` (e.g. `GeoInputs`/`GeoResult`,
  `FireInputs`/`FireResult`, `TrainConfig`).
- Physics coefficients needing primary-source confirmation are marked `[coeff-verify]` in docstrings.

### 16.7.2 The additive-upgrade rule (this is what protects the 128 tests)
New capability is added **without breaking existing call sites**:
- **New dataclass fields get defaults.** `ExpertOutput` grew `available=True`; `Decision` grew `used_classC`,
  `trace_id`; `FukuzonoFit` grew the prediction-interval fields — all defaulted, so old constructors still work.
- **New function parameters are keyword-only** (after `*`). Examples:
  `decide(..., *, drift=False, level_thresholds=None)`, `fuse_group(..., *, corr=None, redundant_groups=None)`,
  `inverse_velocity_fit(..., *, weights=None, recency_halflife=None, z=1.96)`. Positional calls in the tests
  keep passing.

Follow this rule for every extension; it is the reason upgrades like multipulse Iverson, ACI/Mondrian/CRC,
BLUE weighting, and hierarchical fusion landed without disturbing the existing suite.

### 16.7.3 numpy-2.0 note
Peak-to-peak uses the **free function** `np.ptp(x)`, not the removed array method `x.ptp()` (see
`ws8_anomaly.iforest_lite_score`/`mahalanobis_lite_score`/`anomaly_ensemble`). Keep using `np.ptp(...)` so the
core stays numpy-2.0 clean. `[CONFIRMED — present in source]`

### 16.7.4 PYTHONIOENCODING note
On Windows, set `$env:PYTHONIOENCODING="utf-8"` before running the suite so unittest's stderr summary is
UTF-8 clean (`_CANON.md §2`, `00_README §0.4`). `run_tests.py` may print a spurious `[exit code: 1]` because
unittest writes its summary to stderr — the real pass signal is the final `OK`.

### 16.7.5 How Class A/B/C labels appear in outputs
- On every `ExpertOutput.cls` (`PhysicsClass`): geo/fire gates emit `A`; the GeoPINN adapter maps to `B`;
  anomaly/eo/cctv/deepfake map to `DATA`; the RL policy is `ADVISORY`.
- On `Decision.used_classC` (bool) whenever a Class-C operator/feature contributed; `hierarchical.fuse_group`
  additionally labels a whole group with the **weakest-guarantee** member's class so novelty is never hidden.
- Surfaced to the operator by `ws3_alert.operator.present()` and into the CAP XML `used_classC` parameter.

### 16.7.6 Fail-safe / honesty conventions
- Heavy-lib paths **raise `MissingDependency`** rather than fabricate a result (Rule 16). Every torch
  interface stub does this; the `interfaces/` test suite asserts it.
- The decision **fails safe to `uncertain=True`** (never silent) when there are no experts, conflict `u_star`
  is high, or drift fired.
- The shield is **monotone** (`Level.raise_to`): fusion can never lower a safety floor.

---

## 16.8 HOW TO EXTEND

Concrete recipes. Each lists the files to touch and the test to add. Honor §16.7.2 (defaults + keyword-only)
so the 128 tests keep passing, and keep Class-C paths default-OFF.

### 16.8.1 Add a new expert / deep model
1. Implement the torch model under `src/trinetra/deep/<model>.py` (mirror `fire_cnn.py`: a `@dataclass`
   config, an `nn.Module` returning `{"logit"/"prob", …}`, a `.loss(...)`). Keep it torch-only.
2. Register its trust policy in `ws5_fusion_rl/adapters.py` `_POLICY` (`(default_r, cap_r, PhysicsClass)`),
   then at runtime: `deep_expert("<source>", prob) → ExpertOutput`. (Unknown sources raise, by design.)
3. Add a Kaggle kernel under `kaggle/` and the dataset entry in `deep/datamodules.py` (`KagglePaths` + a
   `Dataset` class exposing a `.block` array for spatial-CV).
4. The expert now flows through `decide()` unchanged — no decision-path edits.
5. **Test:** add to `tests/interfaces/` that the torch stub raises `MissingDependency` and that
   `deep_expert("<source>", p)` yields the right `cls`/capped `r` and flows through `decide()` (see
   `tests/fusion/test_adapters.py::test_flows_through_decide`).

### 16.8.2 Add a new physics relation
1. Add the function to the right gate package (`ws1b_geophys/` or `ws1a_firephys/`), pure numpy, with a
   Class label and `[coeff-verify]` in the docstring. If Class C, it must be **default-OFF** behind a new
   `firephys.ndX`/`geophys.*` flag with a Class-A/B fallback.
2. Wire it into the package `gate.py` as a **soft** sub-signal (noisy-OR for geo, consistency/uncertainty
   adjustment for fire) — never a hard trigger. Export it in `__init__.py` `__all__`.
3. If a differentiable version is useful for the PINN, mirror it in `deep/losses.py` (keep the slope-only-via-D1
   bug-guard).
4. **Test:** add a golden test in `tests/physics_golden/` (a limit/monotonicity property, like
   `test_saturated_limit` or `test_slope_only_through_D1`), and if Class-C, a `test_classC_off_by_default`.

### 16.8.3 Add a new fusion option (FM-x / operator)
1. Implement the operator in `ws5_fusion_rl/` (e.g. a new module, like `pharaoh.py`/`gmf.py`), using the
   audited NF primitives.
2. Register it in `fusion_models.fuse()`'s dispatcher behind a `fusion.model` value (or an `operator.*` flag
   if Class C — default OFF). Ensure it reports `used_classC` and **can never lower the shield floor**.
3. Keep FM-1 as the fallback whenever the new path is disabled or has <2 experts.
4. **Test:** add to `tests/fusion/` a property test (e.g. PHARAOH's `test_ge_arithmetic_mean_for_rho_ge_1`,
   or GMF's `test_residual_is_hard_bounded`), plus `test_default_is_fm1_not_classC`.

### 16.8.4 Add a new eval baseline
1. Add the baseline to `eval/baselines.py` (numpy/stdlib only, like `LogisticNumpy`).
2. Register it as a mandatory comparator wherever the gate is assembled — `pipeline/hindcast.run_hindcast`
   and `deep/train.admit_model` both loop over `[("climatology",…),("logistic",…)]`; add your `(name, p_base)`
   there and call `guard.add_baseline_verdict(name, real_win(...))`.
3. `ReportGuard.admit()` already requires a real win over **every** registered baseline, so adding one makes
   the gate strictly harder — exactly the intent (R16).
4. **Test:** extend `tests/eval/` (see `test_eval.py::test_better_model_wins_worse_does_not` and
   `test_not_admitted_blocks_claim`).

---

## 16.9 BUILD / INSTALL

### 16.9.1 Core (numpy only) — this is all the quick start needs
`pyproject.toml` declares `requires-python=">=3.11"` and **core dependencies = `numpy, pandas, lxml`**. The
numpy core runs and is fully tested with just these.

> **Exact versions of the `[CONFIRMED]` run (recorded 2026-10-10):** Python **3.12.14**, **numpy 2.3.5**,
> **pandas 3.0.1**, **lxml 6.1.3** (Windows-11). The 128 tests + 6 CI gates passed on this stack. The core is
> numpy-2.x-clean (uses `np.ptp(arr)`); **numpy 1.x will not reproduce** because `ndarray.ptp()` was removed
> in numpy 2.0 (see ch21). For byte-faithful repro pin `numpy>=2.0`.

```powershell
cd trinetra
$env:PYTHONIOENCODING = "utf-8"
python run_tests.py           # expect: Ran 128 tests ... OK
python scripts/ci_gates.py    # expect: ALL 6 CI GATES PASSED
python -m trinetra.pipeline.demo   # end-to-end advisory demo on synthetic evidence
```
> Note: `python -m trinetra.pipeline.demo` and the shorter `python demo.py` (used in ch18/ch21) are the
> **same demo** — `demo.py` is a thin wrapper that adds `src/` to `sys.path` then calls the pipeline entry
> point. Either command produces the same advisory-RED output.

Editable install (optional, to import `trinetra` from anywhere):

```bash
pip install -e .            # installs numpy, pandas, lxml
pip install -e ".[dev]"     # + pytest, hypothesis (NOTE: tests here use stdlib unittest, not pytest)
```

> `pyproject.toml` also records the honesty invariants surfaced to CI under `[tool.trinetra]`:
> `no_perf_claims_before_gate=true` (R16), `advisory_only=true` (R19), `classC_default_off=true` (R20).

### 16.9.2 Deep stack — Kaggle GPU only
The torch stack is an **optional extra** (`[project.optional-dependencies] deep = ["torch","scikit-learn",
"xgboost","d3rlpy","stable-baselines3"]`) and is pinned for reproducibility in `requirements-deep.txt`
(`torch==2.3.1`, `torchvision==0.18.1`, `numpy==1.26.4`, `scikit-learn==1.4.2`, `xgboost==2.0.3`,
`timm==1.0.7`, `einops==0.8.0`, `pytorch-lightning==2.3.3`, `d3rlpy==2.5.0`, `rasterio==1.3.10`,
`tqdm==4.66.4`, `pyyaml==6.0.1`). Install and run it **on Kaggle** (`pip install -r requirements-deep.txt`),
accelerator = GPU T4×2 or P100 (`kaggle/README.md`). It is **not** installed in this environment and the deep
code is `py_compile`-clean only — shape/CUDA issues will surface on the first real GPU run and need iteration
(`CODE_INVENTORY.md §What is NOT done`). `[CONFIRMED]`

> **Two lists that must be reconciled by whoever sets up training (verified against the files 2026-10-10):**
> `pyproject.toml`'s `[deep]` extra lists **5 names, all UNPINNED** —
> `torch, scikit-learn, xgboost, d3rlpy, stable-baselines3`. `requirements-deep.txt` is the **authoritative
> pinned list (13 packages)** and does **not** list `torchvision/timm/einops/pytorch-lightning/rasterio/tqdm/
> pyyaml` in the extra, while it adds pins the extra omits — and critically `requirements-deep.txt` **does not
> contain `stable-baselines3` at all** (it is extras-only and unpinned). Treat `requirements-deep.txt` as the
> source of truth for a reproducible GPU env; if `stable-baselines3` is actually needed, pin it there too.
> (These are docs-level observations; the repo files were read, not modified.)

See chapter 11 for the Kaggle budget and resume logic, chapter 17 for the test suites, and chapter 18 for the
full zero-to-results runbook.

---

## 16.10 Cross-links
- **Chapter 05 (models):** per-model formulation, I/O, calibration — the deep models in §16.5.8 and the
  physics in §16.5.2–3.
- **Chapter 06 (WS1 physics + fusion):** the derivations behind `ws1b_geophys`, `ws1a_firephys`, and the
  meta-fusion in `ws5_fusion_rl`.
- **Chapter 12 (evaluation):** the protocol the `eval/` harness (§16.5.6) enforces — spatial-CV, cost-loss,
  real-win, ReportGuard.
- **Chapter 17 (testing):** how the 128 tests + 6 CI gates map to the packages here.
```
