# TRINETRA / HIMKAVACH — MASTER SYSTEM-DESIGN & BUILD PROMPT (v1.0)
> Single, self-contained instruction set for the upcoming CODEBASE phase. Hand this file (plus
> `DESIGN/HLD.md` and `DESIGN/LLD.md`) to the implementation agent/team. It encodes everything the
> P0–P23 research program established. Research-only inputs; this prompt authorizes a BUILD, but the
> build inherits every honesty/safety rule below. Nothing in the research was trained or measured —
> all cited numbers are SOURCE-REPORTED from other people's papers.

---

## 0. ROLE & PRIME DIRECTIVE
You are the implementation team for **TRINETRA** (alt. **HIMKAVACH**): an **offline-first, multi-sensor,
physics-grounded early-warning + hazard-detection system**. Build a research prototype that is correct,
honest, reproducible, advisory, and field-deployable on cheap hardware — NOT a product that claims
performance it has not earned.

PRIME DIRECTIVE: **No alert is ever issued autonomously to the public.** Every output is ADVISORY and
human-in-the-loop (Rule 19). The system fails safe to "uncertain" / degraded-offline, never to a silent
"all-clear." If you cannot satisfy a safety or honesty rule, stop and surface it.

## 1. SCOPE (verbatim program scope + addendum)
Hazards & capabilities to implement, in priority order:
1. **Rapid-onset mountain hazards** (original core): landslide, flash-flood, cloudburst, GLOF — region
   Uttarakhand + Himachal Pradesh.
2. **Fire / disaster detection** (CCTV + IoT + satellite active-fire), incl. the P21 fire-physics layer.
3. **CCTV perception** (edge fire/smoke detection, event validation).
4. **Anomaly detection** (InSAR forecast-residual, video, sensor).
5. **Offline alerting** (CAP/SACHET + DTN + LoRa→gateway→siren).
6. **IoT ground segment** (≤₹2,000 LoRa nodes).
7. **Deepfake / misinformation handling** (advisory authenticity scoring on inbound media).
8. **Meta-fusion** (RL + multimodal experts + physics), the P22 layer.

OUT OF SCOPE for the prototype: anything requiring paid data/APIs; Martian/non-terrestrial data (dataset
D140); any autonomous actuation; any claim of operational accuracy without the eval gate (§6).

## 2. HARD CONSTRAINTS (non-negotiable; wire them into CI)
- **C1 Offline-first.** Core detection + the alert path (sensor→gateway→local siren/SMS) MUST work with the
  cloud unreachable. Cloud is an enhancement, never a dependency for life-safety output.
- **C2 ₹2,000/node cap** on both prototype node BOMs (Slope Sentinel, River Eye). Every ₹ figure is `[EST]`
  until re-verified against ≥2 live Indian suppliers (price-verification gate G5).
- **C3 Kaggle compute budget ~30 GPU-h/week.** No training plan may exceed it. Foundation-model encoders are
  FROZEN/reused, not trained from scratch.
- **C4 LoRa band = IN865–867 MHz** (never 433 MHz). Verify against current Indian regulation before any RF.
- **C5 Free/open datasets only** for anything selected for use; licenses must be verified before ingest
  (see `DATASETS.md` + `DATASETS_CATALOGUE.md`; all entries currently [D]=candidate, links untested).
- **C6 Security.** No credential or project data leaves an allow-listed official endpoint. CI test MUST fail
  if a non-allowlisted endpoint is configured. (Closes the historical key-exfiltration bug.)
- **C7 Privacy.** Raw CCTV/video stays local (edge/gateway); only scores/events/clips-on-consent leave a node.
- **C8 Edge feasibility.** Any model assigned to a node must fit its MCU/SoC budget (Tier-0 = tiny statistical
  screen on ESP32-class; heavy models run Tier-1 gateway/cloud only). Re-profile INT8+QAT on target HW.

## 3. HONESTY & SAFETY RULES (inherited from the research program — enforce in code, docs, and CI)
- **R16 No own-system performance claims** until the eval gate (§6) is passed. Until then, say "not yet
  built/measured." Cited literature numbers are SOURCE-REPORTED and must be labeled as such.
- **R19 Advisory / human-in-the-loop / fail-safe.** Authenticated endpoints only; the decision layer can
  recommend an alert LEVEL to a human operator; it never fires public alerts itself. Deepfake/zero-shot/
  open-vocab outputs are LOW-TRUST advisory, never autonomous triggers.
- **R20 Physics model classes.** Label every physics block: **Class A** = established/validated; **Class B**
  = derived from Class-A with a validation route; **Class C** = novel hypothesis, UNVALIDATED. Class-C blocks
  (fire ND-1…ND-7; fusion operator PHARAOH; formulas NF-1…NF-4; models FM-5/FM-6) enter ONLY as SOFT
  features/priors with a Class-A/B fallback — never a hard dependency, never claimed to work or to beat
  anything. Expert review required before any external use.
- **R21 Novelty = search claim.** "Novel" means "not found in our LIMITED search" (no web_search was
  available). Do NOT claim originality in code/docs; keep the `novelty_log_*` caveats.
- **R-NODESTRUCT.** Do not edit `PROGRAM/MASTER_PROMPT.md`. Research artifacts are read-only inputs; the build
  lives in new source directories.
- **R-COEFF.** Every physics coefficient tagged `[coeff-verify]` must be confirmed against a primary source
  (SFPE Handbook, Iverson 2000, Fukuzono, Caine, etc.) before it drives any output; until then it is a
  placeholder behind a feature flag.

## 4. ARCHITECTURE SUMMARY (full detail in HLD.md / LLD.md)
Three fused sensing layers → anomaly stack → physics gate → calibration → RL alarm policy → meta-fusion head
→ conformal risk calibration → hard safety shield → ADVISORY alert level → human operator → CAP/SACHET.

```
 EO/satellite  ─┐
 CCTV/vision   ─┼─► per-layer encoders ─► anomaly stack ─► PHYSICS GATE (geo EF/B + fire EF/ND) ─┐
 Ground IoT    ─┘        │                                                                        │
                         └──────────────► supervised ensemble ──────────────────────────────────┤
 offline RL alarm policy (shielded) ─────────────────────────────────────────────────────────── ┤
                                                                                                  ▼
                              META-FUSION HEAD (GMF + PHARAOH operator, FM-1..FM-6)
                                                   │
                              per-zone conformal risk calibration (honest coverage, not "guarantee")
                                                   │
                              HARD SAFETY SHIELD (monotone, can only RAISE level)
                                                   │
                              ADVISORY alert level {Green<Yellow<Orange<Red} ─► operator ─► CAP/SACHET
```

Workstreams (owners of the modules): **WS1a** fire physics · **WS1b** geo physics · **WS2** deepfake ·
**WS3** alerting/comms · **WS4** CCTV perception · **WS5** RL + meta-fusion · **WS6** robustness/calibration ·
**WS7** IoT nodes · **WS8** anomaly detection.

## 5. WHAT TO BUILD — module checklist (traceable to research artifacts)
Build in the ORDER in §7. Each module cites its spec in the repo.
- **M0 Data + eval harness FIRST** (spatial-CV, mandatory baselines, cost-loss Value Score, provenance F-17).
  This is the guardrail; nothing is "trusted" before it exists. (TRINETRA_Workstreams WS2; BUILD_HANDOFF.)
- **M1 Geo physics gate** (WS1b): infinite-slope FS, Iverson transient head (slope only via D₁), Fukuzono 1/v,
  Caine I–D. Classes A/B/C per `ws1_physics/model_set_decision.md`. Golden-case unit tests (G1).
- **M2 Fire physics layer** (WS1a): EF-01…EF-20 Class-A blocks + ND-1…ND-7 Class-C soft features (dealiased
  flicker, smoke-transmittance temp, Π_ig ignition index, r_phys residual, wind-tilt height, Ξ_rc regime
  scalar, advection-coherence). All [coeff-verify]; all soft-feature-with-fallback. (`ws1_physics/*_P21.md`.)
- **M3 EO/InSAR encoder + forecast-residual anomaly** (WS1b/WS8): FROZEN SAR-capable EO-FM (trade study
  CR-01) + bounded-residual forecast head; Deep SVDD (collapse-prevented) + iForest + XGBoost ensemble.
- **M4 CCTV perception** (WS4): F-11 edge detector, F-12 temporal event validation, F-16 IR optical-flow/
  flicker feature; (Wave-2/3 F-18..F-26 optional/parked). Specs in `features/wave1_specs.md`.
- **M5 Calibration + drift monitor** (WS6): F-13 conformal-under-shift (WCPS), F-14 label-free drift monitor.
- **M6 Offline RL alarm policy + shield** (WS5): one-step/TD3+BC baseline FIRST, OPE-feasibility gate, then
  optional CQL/IQL; post-posed monotone safety shield (can only RAISE).
- **M7 Meta-fusion head** (WS5): GMF (stacking + bounded residual + gated MoE) with the PHARAOH aggregation
  operator and FM-1…FM-6 fusion models; per-zone Mondrian conformal; reliability gating. (`ws5_fusion/*`.)
- **M8 IoT nodes** (WS7): Node A Slope Sentinel, Node B River Eye; Tier-0 firmware; F-15 sensor-drift
  correction; fault-vs-event discrimination; energy budget. (TRINETRA_Workstreams WS5.)
- **M9 Alerting/comms** (WS3): CAP/SACHET message builder + signer, DTN store-carry-forward, offline
  LoRa→gateway→siren path, operator decision-support UI (F-22 advisory).
- **M10 Deepfake/misinfo** (WS2): interpretable authenticity scorer (photometric/textural/temporal), LOW-TRUST
  advisory into fusion only.

## 6. EVALUATION GATE (G2 — THE admission gate; blocks every performance claim)
No module is "done" and no number is reportable until:
1. **Leakage-controlled splits**: tile-withheld SPATIAL cross-validation + event-held-out temporal holdout;
   disclose feature–label correlation before/after deseasonalization.
2. **Mandatory baselines in every table**: persistence/seasonal-naive (forecasting), gradient-boosted trees +
   3-rule decision tree + linear model (classification), a fixed physical/spectral rule. Report
   SKILL-OVER-BASELINE, never a raw metric. A deep model that does not beat these is reported as such.
3. **Per-hazard reporting** with bootstrap CIs (no single aggregate AUC).
4. **Proper scoring + calibration**: CRPS/rank-histogram for forecasts; ECE + selective-prediction for
   classifiers; conformal coverage reported WITH the caveat that coverage degrades under drift/onset.
5. **Rare-event cost-loss**: Value Score as the PRIMARY decision metric over a cost ratio range; alarm
   threshold p* = C_FA/(C_FA+C_miss) from the SAME cost-loss model (≈0.0476 for the geo default).
6. **Robustness**: per-corruption tests (fog/rain/night/compression); worst-case + dispersion reported.
7. **Honest RL valuation**: BVFT policy selection + SCOPE-RL risk (CVaR@5%); deploy only if the OPE lower
   bound ≥ rule baseline; ≥100 seeds for any RL claim.
8. **"Real-win" gate (F-17)**: every improvement must pass the inferential-reproducibility test (LMEM+GLRT)
   on a held-out CROSS-CAMERA/CROSS-SITE split; seed-noise or single-benchmark gains are rejected.

## 7. BUILD ORDER (dependency-correct)
1. M0 data+eval harness+baselines (prerequisite for everything).
2. M1 geo physics gate + M2 fire physics layer (golden tests G1).
3. M3 EO encoder + anomaly stack; M4 CCTV perception (parallel).
4. M5 calibration + drift monitor.
5. M6 offline-RL alarm policy + shield (baseline-first; OPE gate).
6. M7 meta-fusion head (needs M1–M6 outputs).
7. M8 IoT nodes + M9 alerting/comms (parallel hardware/comms track; M8 behind price-gate G5).
8. M10 deepfake (advisory add-on).
Each step must pass its gate (G1…G7) before the next consumes it.

## 8. TECH STACK (defaults; justify any deviation)
- Python 3.11; PyTorch; d3rlpy (offline RL) + Stable-Baselines3 (sim PPO); scikit-learn/XGBoost; MAPIE/
  custom conformal; xarray/rasterio/rioxarray for EO datacubes; MLflow or dagger (F-17 provenance).
- Edge firmware: ESP32-C3 / ESP32-CAM (C/C++/MicroPython or ESP-IDF); TinyML via TFLite-Micro for Tier-0.
- Comms: LoRa (SX1262, IN865–867), CAP XML (+ SACHET integration), DTN (Spray-and-Wait).
- Repo layout: `src/{ws1a_firephys, ws1b_geophys, ws2_deepfake, ws3_alert, ws4_cctv, ws5_fusion_rl,
  ws6_robust, ws7_iot, ws8_anomaly, common}`, `eval/` (harness+baselines), `firmware/`, `configs/`,
  `tests/` (golden+unit+integration), `data/` (DVC-tracked pointers only, no raw data in git), `docs/`.
- All randomness seeded; spatial-CV fold assignment logged; configs are declarative (hydra/yaml).

## 9. ACCEPTANCE / DEFINITION OF DONE
- All 7 workstream gates (G1–G7) pass (see HLD §Gates).
- Offline alert path demonstrated with cloud unreachable (C1).
- Both node BOMs ≤₹2,000 after supplier re-verification (C2/G5); LoRa on IN865–867 (C4).
- Every reported number carries its spatial-CV baseline + CI; every Class-C block is behind a flag with a
  Class-A/B fallback and a logged novelty/validation caveat.
- CI enforces: endpoint allow-list (C6), no-raw-video-egress (C7), seed/fold logging, golden physics tests,
  and the F-17 significance gate on any "improvement."
- A Joshimath/Chamoli-style HINDCAST produced under the full G2 protocol (headline deliverable), reported
  honestly (including "does not beat baseline" where true).

## 10. KNOWN PITFALLS TO DESIGN AROUND (from the failure-mode catalogue)
Spatial leakage inflating skill; AE/reconstruction anomaly over-generalizing (miss) → use memory/miss-biased
scoring; INT8 PTQ hurting diffuse-smoke recall; conformal exchangeability breaking under shift (reweight or
flag Unreliable); IMERG precip underestimation collapsing to zero → multi-source + LoRa-gauge bias-correction;
single faulty node driving a RED → require cross-node spatial consistency; reward-sign inversion in RL →
exposure-weighted per-capita reward + shield; EVT tails unstable in data-sparse mountains → zoning prior only,
never a live hard threshold; n≈5 events → variance reduction only, bootstrap CIs mandatory, never manufacture
power.

## 11. DELIVERABLES OF THE CODEBASE PHASE
Working prototype per §5/§7; the eval harness + hindcast report; firmware for both nodes; the offline alert
path demo; a repo README mapping every module to its research artifact; a verification log proving each gate.
Produce `DESIGN/HLD.md` and `DESIGN/LLD.md` (this round) as the architecture contract the code must match.
