# FEATURES — evidence-backed feature register (MASTER_PROMPT §0.10, admission in P17)
#
# NO FAKE FEATURES (honesty rule 2): every feature traces to ≥1 real paper/dataset, or is
# labeled "novel hypothesis, unvalidated". A feature is NEVER described as working/improving
# anything — only "supported by evidence X, not yet built or tested" (rule 7). Formal
# admission is Phase P17. This file is the running candidate list.

## Schema
| ID | Feature | Layer/WS | Supporting evidence (paper IDs) | Status | Planned cost | Admission note |
|----|---------|----------|---------------------------------|--------|--------------|----------------|

## Candidate features carried from P0 corpus (CANDIDATE only — not admitted)
| F-01 | SSL masked-modeling InSAR encoder (feature-target, not raw-pixel) | WS1/WS8 | 2310.18653 FG-MAE; 2401.07782 CSMAE; 2510.17014 (needs general baseline) | candidate | — | must beat general-purpose ViT baseline |
| F-02 | Forecast-residual anomaly on InSAR | WS8 | 2509.18176; 2501.15196; 2308.09296 | candidate | — | must beat persistence baseline |
| F-03 | Deep SVDD anomaly head (collapse-prevented) | WS8 | 2510.09452; 2108.04907 | candidate | — | |
| F-04 | Physics gate (infinite-slope FS / Iverson transient) | WS1 | (P7 derivations) | candidate | — | CLASS A/B/C labels pending |
| F-05 | Conformal prediction under autocorrelation/missingness | WS6 | 2303.12783 HopCPT; 2406.05405; 2502.05709 | candidate | — | |
| F-06 | Offline RL alarm policy (TD3-BC baseline-first) + safe shield | WS5 | 2106.08909 one-step; 2506.00505 TD3-BC; 2507.23603 shield realizability; 2604.23576 CAPSULE | candidate | — | shield must be realizability-checked |
| F-07 | Gated meta-fusion head (stacking + bounded residual + conformal) | WS5/WS8 | 2011.06125 Hurricast; 2509.03315 super-learner; 2601.03425 (routing-collapse caution) | candidate | — | audit expert utilisation |
| F-08 | ₹2000 LoRa ground node (tilt/moisture/piezo/rain) | WS7 | 1906.02998; 1511.08331 VoI duty-cycle; 1509.06065 fault-tolerance | candidate | ≤₹2000 [EST] | hard-verify BOM in P6 |
| F-09 | River-Eye LSPIV node (+uncertainty, gap-filling) | WS4 | 2507.20102; 2312.06461 | candidate | ≤₹2000 [EST] | |
| F-10 | DTN store-carry-forward alert dissemination | WS3 | 1308.2907; 2603.15945 (Spray-and-Wait) | candidate | — | |

## ================= P17 FORMAL ADMISSION (2026-10-10) =================
# Admission rules (MASTER_PROMPT P17): a feature enters only if (1) it traces to >=1 real paper/datasheet/
# dataset read at >=abstract level (ABS = WEAK evidence, lower priority); (2) evidence is relevant to our
# setting else "transfer hypothesis"; (3) a planning-level cost exists; (4) it does not conflict with a hard
# constraint (Kaggle budget, INR 2000 prototype cap, offline operation, privacy, safety/Rule 19, free-only
# datasets); (5) own ideas = "novel hypothesis, unvalidated". HONESTY: all evidence below is ABS-level and
# SOURCE-REPORTED; paper IDs subagent-reported, NOT re-fetched. NO feature is described as "working".
# Prioritization = (expected benefit x evidence strength) / cost → waves. EVERY feature carries a
# PRE-REGISTERED decision rule: keep only if improvement exceeds seed/trial variance on a HELD-OUT CROSS-
# CAMERA/CROSS-SITE split AND cost is justified; a feature that helps one benchmark but hurts cross-dataset/
# cross-camera performance is NOT a win (gate via the inferential-reproducibility test 2302.04054).

## Evidence-strength legend: strong / medium / weak(ABS) / transfer-hypothesis / novel-hypothesis.
## All P17 features below are weak(ABS) pending method-level read + own cross-camera eval.

### WAVE 1 — high evidence(for ABS) / low cost — approved-for-build-plan (pending P18 specs)
| ID | Feature | Layer/WS | Supporting evidence (paper IDs) | Status | Planned cost | Pre-registered decision rule / risk |
|----|---------|----------|---------------------------------|--------|--------------|-------------------------------------|
| F-11 | EFA-YOLO efficient edge detector (attention-lite + depthwise) | WS4 | 2409.12635 (1.4M params, 22.19ms CPU, src-reported) | approved-for-build-plan | low (single-GPU retrain; CPU-real-time inf) | keep only if cross-CAMERA mAP gain > seed variance vs current backbone; RISK: micro-arch mAP gains often shrink cross-camera (single-split overfit) |
| F-12 | Temporal multi-frame event validation (confidence-weighted voting + cascade filter) | WS4/WS3 | 2607.03131 (FA 52%->4%, <100ms/frame, src-reported) | approved-for-build-plan | very low (post-processor, no retrain) | keep if false-alarm reduction holds cross-site at matched sensitivity; RISK: framerate/latency-to-alert tradeoff; must not raise missed-event rate |
| F-13 | Post-hoc conformal calibration under covariate shift (WCPS) | WS1b/WS6 | 2404.15018 WCPS; 2402.07307 self-calib CP; 2501.12749 NACP | approved-for-build-plan | low (post-hoc; needs density-ratio est.) | keep if coverage stays valid on cross-site split; RISK: conformal exchangeability breaks under shift unless reweighted — do NOT claim guarantees cross-site without weighting |
| F-14 | Label-free drift + calibration monitoring (student-teacher + CUSUM) | WS6 | 2103.00903 STUDD; 2510.25573 CUSUM-calibration | approved-for-build-plan | very low (aux model + chart, model-agnostic) | keep if detection delay/false-alarm beats a fixed-threshold monitor on replayed drift; ADVISORY only (Rule 19) |
| F-15 | IoT GP drift correction + uncertainty-driven calibration scheduling | WS7 | 2506.09186 (MSE -up to 90%, src-reported); 1707.03682 PRNet blind calib | approved-for-build-plan | low-moderate (GP scales w/ data; cheap inf) | keep if post-correction error < seed variance improvement on held-out sensor-days; RISK: blind/neighbor calibration fails on sparse/isolated nodes |
| F-16 | Unsupervised IR optical-flow / flicker physics feature (label-free cold-start) | WS1a/WS4 | 1909.12937 (95.39% frame, no labels, src-reported) | approved-for-build-plan | very low (classical CV, no GPU/labels) | keep if it adds signal over RGB-only on cross-site video; RISK: sensitive to framerate/codec/PTZ motion |
| F-17 | Experiment tooling: provenance (dagger) + inferential-reproducibility test (LMEM+GLRT) | tooling | 2006.07484 dagger; 2302.04054 LMEM | approved-for-build-plan | very low (library adoption) | ENABLER: the "real-win" gate every other feature passes through; no model impact |

### WAVE 2 — medium evidence / moderate cost — pending (needs more evidence or co-located hardware/data)
| ID | Feature | Layer/WS | Supporting evidence (paper IDs) | Status | Planned cost | Pre-registered decision rule / risk |
|----|---------|----------|---------------------------------|--------|--------------|-------------------------------------|
| F-18 | STCNet two-stream spatio-temporal smoke (motion vs texture) | WS4 | 2011.04863 (+6.2% RISE, src-reported) | proposed | moderate (two-stream compute/mem) | keep if it cuts steam/cloud FPs cross-site beyond cost; RISK: two-stream latency on edge; temporal cue codec-sensitive |
| F-19 | MobileViT-S knowledge distillation for compact detector | WS4 | 2502.20979 (src-reported +0.44-2.00% at compact size) | proposed | moderate (teacher + distillation run) | keep if student matches teacher within variance cross-camera; RISK: teacher-pipeline cost; distillation can overfit teacher's dataset bias |
| F-20 | WISE weakly-supervised smoke localization (tile labels) | WS4 | 2609.18227 (0.12M params, tile-F1 0.964, src-reported) | proposed | low inf (teacher + weak-label pipeline) | keep if pixel-localization transfers cross-site; RISK: weak-label pipeline + domain-specific (satellite/onboard) |
| F-21 | Semi-supervised video fire (FireMatch / SIAVC pseudo-labels) | WS4 | 2311.05168 FireMatch; 2405.14506 SIAVC | proposed | moderate (SSL training loop) | keep if pseudo-labels help on NEW cameras not just source; RISK: confirmation bias entrenches source-domain errors |
| F-22 | Conformal prediction sets for OPERATOR decision-support UI | WS3 | 2401.13744 (RCT: raises operator accuracy, src-reported) | proposed | low (UI + CP wrapper) | keep if human-factors eval shows improved dispatcher accuracy; Rule 19 advisory UI |

### WAVE 3 — speculative / high setup cost — parked (only if budget remains)
| ID | Feature | Layer/WS | Supporting evidence (paper IDs) | Status | Planned cost | Pre-registered decision rule / risk |
|----|---------|----------|---------------------------------|--------|--------------|-------------------------------------|
| F-23 | SmokeyNet multimodal camera+weather fusion | WS4/WS1b | 2212.14143 (src-reported better time-to-detection) | proposed | moderate (needs co-located weather) | only pays off where weather feed exists; else reverts to single-stream |
| F-24 | Obscured-flame 3D-conv temporal segmentation | WS4 | 2307.00104 (Dice 85.88%, "~100%" video — OVERFIT RED FLAG) | proposed | moderate-heavy (3D conv, video seqs) | treat suspiciously-high single-split numbers as red flags, not evidence |
| F-25 | Thermal/IR fusion branch for low-visibility | WS4/WS7 | 2307.04223 (mAP@0.5 95% Jetson Nano, src-reported) | proposed | low inf but IR HARDWARE + calib rig | gated on IR hardware availability + INR 2000 cap; likely exceeds prototype budget |
| F-26 | Two-stage UAV adaptive compression + policy early-exit | WS4 | 2508.16739 (src-reported large compute cut) | proposed | high (policy-net/RL training + orchestration) | needs RL-style policy; defer until core detector validated |

## Rejected features — none outright rejected at P17; Wave-3 items are PARKED (budget/hardware/overfit-risk),
## not rejected. Rejections (with evidence reason) will be recorded if a feature fails its P18 spec or decision
## rule. OVERFIT RED FLAGS explicitly logged: 2307.00104 "~100% video classification" and any >98% single-
## split headline treated as overfit candidates, NOT evidence.
