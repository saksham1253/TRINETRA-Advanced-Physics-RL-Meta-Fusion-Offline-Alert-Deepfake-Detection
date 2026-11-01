# BUILD HANDOFF PACKAGE (MASTER_PROMPT §0.4A) — updated at end of every phase
#
# Because the build happens later with a SEPARATE prompt, this stays current. Per
# workstream: what to build, chosen methods + paper IDs they follow, datasets w/ verified
# links+licenses, interfaces/data formats, pre-registered eval protocol + acceptance
# criteria, published baselines/targets to match first, hyperparameter defaults w/ sources,
# planning-level GPU-h estimate + Kaggle fit, verification checklists, known pitfalls (from
# failure-mode catalogue), open decisions, recommended build order.

## Status after Phase P0
- NO build-ready specs yet. P0 is recovery/verification/planning only.
- Corpus: 235 unique papers, ALL abstract-only — NOT yet full-text, so no method is
  build-certified. Full-text grounding begins P2/P3.
- Workstreams defined (WS1 physics, WS2 deepfake, WS3 alerting, WS4 CCTV, WS5 RL,
  WS6 robustness, WS7 IoT, WS8 anomaly). Per-WS build specs are produced in P6–P18.

## Status after Phase P1 (2026-10-06)
- STILL no build-ready specs (research-only phase). But the EVALUATION doctrine and several
  component priors are now full-text-grounded and must be honored by every later build spec:
  - **Evaluation stack (mandatory before any performance claim, Rule 16):** per-base-rate metric
    discipline (never compare metrics across imbalance ratios, 2206.09981); cost-loss Value Score
    as the PRIMARY decision metric reported over a C/L range, with alarm threshold
    p*=C_FA/(C_FA+C_miss) from the SAME cost-loss model (2601.05921; E-06/E-07); OPE-feasibility
    gate before trusting any learned alarm policy (2311.14110, FM-22); honest conformal coverage
    via EnbPI — approximate, shift-sensitive gap, NOT a hard guarantee (2010.09107, CR-04);
    proximity-aware calibration because overconfidence concentrates in thin-data regions and
    temp-scaling doesn't fix it (2306.04590, FM-20); maintained safety-case / GSN assurance
    structure (2209.11632, Q8.1).
  - **Component priors:** compact models + resolution-as-safety-hyperparameter (2405.00031);
    XGBoost high-recall EWS at cost-based threshold as the credible gradient-boosted workhorse
    (2606.21130, HP-03); fusion is NOT free-lunch robust to a dropped layer — add a <1%-param
    missing-modality adapter + uncertainty flag (2310.03986, CR-07/FM-15/HP-04); low-energy drift
    detector (ADWIN/HDDM_W) as the live monitor (2404.19452, HP-02); AI tech-debt / train-serve
    skew audit (2103.09783, FM-19); classical two-stage stochastic optimization as a non-RL
    decision-layer alternative (2608.26304); GMF reframed as a COMPOSITION of known parts, not an
    invention (2604.25512, CR-06).
- Open questions LOCKED in analysis/00_key_questions.md (8 P0-gating). Theme-coverage matrix
  (analysis/12_theme_coverage_matrix.md) flags THIN cells = P2/P3 gaps: assurance-case (SC1),
  tech-debt (SC3), live drift/OOD (SC7), missing-modality robustness (SC9), conformal-under-drift
  (G-CR04). These must be widened before their owning build phases.
- Quota: 15 NEW papers read FT-PARTIAL (100% Tier-2+); faithfulness audit 0% error.

## Recommended build order (preliminary; refined through the phases)
1. Data + spatial-CV harness + baselines (persistence, gradient-boosted, decision-tree)
   — the FM-01/FM-02 guardrail must exist before any model is trusted. [P1: add the cost-loss
   Value Score + per-base-rate protocol to this harness from day one.]
2. Physics gate (WS1) — once P7 derivations + CLASS labels are done.
3. InSAR SSL encoder + forecast-residual anomaly (WS1/WS8).
4. Conformal calibration layer (WS6). [P1: EnbPI baseline + proximity-aware calibration.]
5. Offline-RL alarm policy + safety shield (WS5), one-step baseline first. [P1: OPE-feasibility
   gate FIRST; stochastic-optimization alternative on the table.]
6. Fusion head (WS5/WS8). IoT + River-Eye + DTN (WS7/WS4/WS3) in parallel hardware track.
   [P1: fusion must be trained/evaluated under single- and two-layer dropout.]

## Pending inputs before build (see HANDOFF/OPEN_DECISIONS.md)
- Dataset access (P5), verified BOM (P6), physics model-set decision (P7).

## Status after Phase P2 (Literature Foundation I)
- Quota: **18 NEW papers read FT-PARTIAL (100% Tier-2+)**, target ≥15 exceeded; Audit #8 (≈22%
  sample) 0% error. Running total of deep NEW reads: P1 15 + P2 18 = **33** (toward the 250–400
  JOINT P2+P3 target — NOT yet reached by design; P3 delivers the back half).
- **Standing evaluation-harness spec hardened (design-only).** The build's eval harness MUST
  implement the 8-point protocol in PROGRAM/sota/P2_sota_scan.md §8.2:
  1. TWO mandatory baselines always — a FIXED physical/spectral rule (e.g. MNDWI for water,
     2609.20441; FS/physics gate for slopes) AND persistence (2509.18176, 2609.17175); report
     skill-over-baseline, never raw metric (CR-02, now a four-domain doctrine).
  2. Spatial + event-held-out CV, never random split (2608.12422, 2605.20167 LOOCV-over-events).
  3. Anti-leakage: deseasonalize seasonal inputs (monthly climatological anomaly) and DISCLOSE
     feature–label correlation before/after (2605.20167: r 0.570→−0.031); group chips→maps→events.
  4. Probabilistic + calibration metrics: CRPS + rank histogram + RAPSD for forecasts (2609.17175);
     ECE + selective-prediction curve for classifiers (2605.15894); conformal coverage WITH the
     caveat that coverage degrades at onset/shift (2610.02777) → back with a hard physics shield.
  5. Rare-event cost-weighted scoring: report the cost-loss Value Score (E-07) + recall at fixed
     false-alarm budget; frame-AUC/accuracy are optimistic under imbalance (FM-21, 2610.04392).
  6. Per-corruption robustness tested explicitly (fog/rain/night) — augmentation does NOT transfer
     across corruption types (2606.07593).
  7. Encoder selection by on-OUR-task evaluation + mid-layer probing + CKA shift budget, not
     leaderboard (2606.13896) → feeds the CR-01 trade study (P7).
  8. Edge numbers re-profiled on target HW at INT8+QAT, reporting MB + ms + runtime RAM
     (2609.20441 template: 1.5 MB INT8, 5.57 ms/512², ~14 MB on Jetson Xavier NX).
- **Operational analog to emulate (2605.20167, HaorFloodAlert):** free data + Sentinel-1 + RF/XGB
  + transboundary upstream signal (~36 h lead) + local-language SMS/WhatsApp last-mile. Confirms the
  cheap, free-data architecture is feasible AND fieldable; adopt its deseasonalization + seeded,
  regenerable pipeline discipline.
- **WS4 video architecture (design-only):** federated MIL (small scorer trained across clients, raw
  video stays local, 2609.07455) → cheap-edge-scorer → suspect-VLM-verifier cascade via the LOGIT
  interface (not prompt text-gen); adaptive temporal granularity (2609.05066); VLM at gateway tier.
- **WS3 nowcasting (design-only):** probabilistic + ensemble; honest ~90-min skill ceiling; longer
  lead from upstream/soil-moisture/InSAR memory (2609.17175, 2605.20167).
- 5 new build risks logged: RB-08..RB-12 (RISKS_FOR_BUILD.md).
- P3 directive: rebalance themes away from hazard-core (33% in P2) toward robustness / eval-critique
  / efficiency / non-hazard methods; fill axes A3/A4/A9/A13 and THIN cells (assurance-case,
  tech-debt, live-drift, missing-modality).

## Status after Phase P3 (Literature Foundation II)
- Quota: **43 NEW papers read FT-PARTIAL (100% Tier-2+)**, target ≥15 and heavy-phase ~30–40 exceeded
  (user authorized exceeding ~40 for outstanding papers); Audit #9 (~21% sample) 0% error. Running
  total of deep NEW reads: P1 15 + P2 18 + P3 43 = **76** (toward the CUMULATIVE 250–400 target — NOT
  yet reached by design; accrues via baseline-235 promotions + harvest pool in P4+; never padded, §0.5).
- **RESIDUAL doctrine (design-mandatory now, 5× corroborated).** Every forecasting/refinement component
  the build produces SHOULD learn a BOUNDED RESIDUAL on a deterministic/mechanistic backbone, not
  forecast from scratch (MW-Nowcast 2609.34836, DRUM 2412.11942, Nowcasting-Nets 2108.06868, TREA-Net
  2607.26854, exPreCast-ENS 2608.30205). Applies to: GMF bounded-residual head; SSL forecast-residual
  InSAR encoder; precip refinement. The residual bound itself must be validated on Himalayan data (Rule 16).
- **Alarm stack spec (design-only, now end-to-end sourced).** Pipeline the build MUST implement:
  (a) predictive DISTRIBUTION from a residual-diffusion/ensemble head (exPreCast-ENS 2608.30205 template:
  4 km→1 km, 30-member, 3.4 s/1-h on one GPU); (b) ACTION-LOSS calibration via a decision-risk adapter +
  utility-aware calibration — report BOTH predictive AND decision-loss coverage (2609.14821: predictive
  90.4%, decision calib error 0.083→0.047, regret −18.7%, utility +11.6%); (c) alarm threshold from the
  SAME cost-loss model, p*=C_FA/(C_FA+C_miss)=0.0476 (E-06/E-07). CR-04 is now "coverage must be
  action-loss coverage," not just predictive.
- **EVT/tail-risk layer (design-only, NEW).** Add a peaks-over-threshold / r-Pareto tail model to the
  WHEN layer + people-at-risk, with per-cell IMERG features [μ,σ,max,exceedance-freq] on a catchment
  spatial graph and JOINT exceedance for compound failure (GNN-rP 2509.10362). HARD GUARD: EVT tails are
  unstable with few exceedances in data-sparse mountains → wide-uncertainty ZONING PRIOR only, never a
  real-time hard threshold; always paired with the physics shield.
- **SAR-first encoder stance (CR-01, feeds P7).** SAR beats optical in two independent all-weather votes
  (SAR2Agri 2608.11142 +15.3 pt; GLOF SAR seg 2512.24117 IoU 0.9130). P7 trade study must evaluate named
  SAR-specific contenders on OUR task: TerraMind, Copernicus-FM, SAR-JEPA, SARMAE, SAR-W-MixMAE (flood-
  mapping pretraining — closest to our hazard), SAMBA (Mamba, linear-cost → edge budget), OceanSAR. SSL
  recipe candidate for the InSAR encoder: SAR2Agri Time-Difference + Future-Frame temporal pretext +
  masking + curriculum, RECAST for interferometric phase (not intensity).
- **LEWS forecast-uncertainty robustness (design-only).** The rain→landslide model is fed FORECAST rain
  (IMERG nowcast), not observed rain → train displacement/motion-robust representations (RMCL 2605.17419,
  +37% precision, Japan 19 regions); treat rainfall-field displacement as a first-class perturbation.
- **RL alarm policy hardening (design-only).** Offline physics-informed RL + decoupled post-hoc shield
  (PIER 2603.17319: forecast-independent, kills the tail not the mean); Lyapunov-certified action library
  for safety-by-construction (2609.38655); adaptive probabilistic shield that starts conservative and
  tightens with data (2608.19836). MANDATORY eval protocol from the critique (2610.03369 → RB-13):
  ≥100 seeds, report tail + dispersion, and beat trivial baselines (TWAP/immediate/fixed-threshold) —
  a MoE "fix" can merely mask a training-spec failure.
- **WS2/WS4 (design-only).** Interpretable deepfake detector with explicit photometric/textural/
  geometric/compression features + temporal model (2610.03380) for auditability (Rule 19); federated
  video anomaly keeps raw video local (2608.06876).
- **On-node adaptation (WS7, design-only).** Backprop-free prototype-head self-calibration (2610.06241:
  5.2 KB flash / 22 KB SRAM / 11 ms on a PSoC6-class MCU) for drift-robust edge thresholds; free OOD +
  recalibration via distance-logits (IsoMaxPlus, 2608.16654: ECE 0.0095→0.0026, no outlier data/tuning).
- COMPULSORY future phase **P14Z** (zero-shot/open-vocab classification) registered; its outputs are
  LOW-TRUST advisory into GMF + conformal + shield (Rule 19), never an autonomous trigger. Build specs
  for zero-shot are produced in P14Z, not before.
- Carried build-affecting opens: 2609.14821 body figures re-verify vs PDF (P14/P14Z); SAR-FM trade (P7);
  CP under drift/missingness (2406.05405, CR-04); non-arXiv journal SOTA for GLOF/landslide (D-010).
