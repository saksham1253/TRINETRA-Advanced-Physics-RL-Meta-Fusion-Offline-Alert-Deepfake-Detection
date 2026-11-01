# PROGRAM/reports/P17_scout_notes.md — feature scout notes + literature map (P17)

Phase P17. HONEST: all ABS; IDs/years arXiv-ID-derived + subagent-reported (reader 3dc15525; 10 fetches), NOT
re-fetched (residual risk, §0.5); all numbers SOURCE-REPORTED (Rule 16). Backs FEATURES.md P17 admission.
Running body-level deep FT NEW total UNCHANGED at 100 (ABS breadth).

## P17 section — 22 NEW primary arXiv (feature candidates) → FEATURES.md

### T1 efficient CCTV detection
| arXiv | Short | FEATURES | Note (source-reported) + cost |
|-------|-------|----------|-------------------------------|
| 2208.13422 | Light-YOLOv5 | (F-11 alt) | SepViT C3 + Light-BiFPN + GAM + Mish/SIoU; +3.3% mAP, −27.1% params, −19.1% FLOPs, 91.1 FPS. Cost: moderate retrain. |
| 2409.12635 | EFA-YOLO | F-11 | EAConv+EADown; 1.4M params, 4.6 GFLOPs, 22.19 ms/img CPU, ~88× faster. Cost: very low, CPU-real-time. |
| 2502.20979 | MobileViT-S KD aerial fire | F-19 | distill teacher→MobileViT-S + Grad-CAM; +0.44–2.00% at compact size, top throughput. Cost: teacher + distillation. |
| 2609.18227 | WISE weak-sup smoke | F-20 | teacher→student, tile labels, presence+prob-map one pass; 0.12M params, ~3 GFLOPs, tile-F1 0.964/pixel-F1 0.750. Cost: low inf. |
| 2508.16739 | Two-Stage UAV cascade | F-26 | policy net discards clips + improved YOLOv8; large compute cut, real-time stage-2. Cost: high (policy training). |

### T2 temporal / multimodal cues
| arXiv | Short | FEATURES | Note (source-reported) + cost |
|-------|-------|----------|-------------------------------|
| 2011.04863 | STCNet | F-18 | dual spatial+temporal cross-guided pyramids; +6.2% on RISE industrial smoke. Cost: moderate two-stream. |
| 2307.00104 | Obscured-flame 3D-conv | F-24 | MobileNet+CBAM encoder, 3D convs over frame stacks; Dice 85.88%, prec 92.47%, ~100% video (OVERFIT RED FLAG). Cost: moderate-heavy. |
| 2212.14143 | SmokeyNet camera+weather | F-23 | spatio-temporal CNN fusing images + weather; better accuracy + time-to-detection. Cost: moderate, needs weather feed. |
| 1909.12937 | Unsupervised IR optical-flow | F-16 | optical flow + divergence + intensity, MRF/MAP; 95.39% frame, no labels. Cost: very low (classical CV). |
| 2307.04223 | Thermal/IR fusion | F-25 | multi-cam thermal/IR calib + lightweight DNN; mAP@0.5 95% on Jetson Nano. Cost: low inf, needs IR hardware. |

### T3 label efficiency
| arXiv | Short | FEATURES | Note (source-reported) + cost |
|-------|-------|----------|-------------------------------|
| 2311.05168 | FireMatch SSL | F-21 | consistency + pseudo-labels + adversarial alignment + fairness loss; 76.92%/91.81%. Cost: moderate SSL. |
| 2405.14506 | SIAVC SSL | F-21 | Super-Augmentation Block + video cross-set aug; 88.76% (ECA9)/89.13% (Fire). Cost: moderate SSL; releases ECA9. |

### T4 fusion / calibration add-ons
| arXiv | Short | FEATURES | Note (source-reported) + cost |
|-------|-------|----------|-------------------------------|
| 2501.12749 | NACP noise-aware conformal | F-13 | noise-free threshold from noisy calib labels; finite-sample coverage under uniform noise. Cost: very low post-hoc. |
| 2402.07307 | Self-Calibrating CP | F-13 | Venn-Abers + conformal; calibrated points + valid intervals, better interval efficiency. Cost: low post-hoc. |
| 2404.15018 | WCPS covariate-shift conformal | F-13 | likelihood-ratio reweighting keeps calibration valid under covariate shift. Cost: low; needs density ratio. |

### T5 alerting / ops
| arXiv | Short | FEATURES | Note (source-reported) + cost |
|-------|-------|----------|-------------------------------|
| 2607.03131 | Temporal event validation | F-12 | multi-frame confirmation + confidence-weighted voting + cascade filter; FA 52%→4%, <100 ms/frame. Cost: very low. |
| 2103.00903 | STUDD drift | F-14 | student mimics teacher, monitor mimicking loss, label-free; competitive on 19 streams. Cost: low aux model. |
| 2510.25573 | CUSUM calibration monitor | F-14 | cumulative-sum chart w/ dynamic limits on prob vs outcome, model-agnostic; early miscalibration detection. Cost: very low. |
| 2401.13744 | Conformal sets aid operators (RCT) | F-22 | RCT: conformal sets raise operator accuracy vs fixed-size sets. Cost: low UI + CP. |

### T6 IoT features
| arXiv | Short | FEATURES | Note (source-reported) + cost |
|-------|-------|----------|-------------------------------|
| 2506.09186 | GP drift correction + scheduling | F-15 | GP sensor-response model + uncertainty-driven calibration schedule; MSE −up to 90% (avg >20%), schedule −15.7%. Cost: low-moderate. |
| 1707.03682 | PRNet blind calibration | F-15 | project drifted data + CNN recovers drift-free, no ground truth; calibrates 2× more sensors at 80% recovery. Cost: moderate train. |

### T7 experiment tooling
| arXiv | Short | FEATURES | Note (source-reported) + cost |
|-------|-------|----------|-------------------------------|
| 2006.07484 | dagger orchestration | F-17 | tracks the state-tree of multi-stage experiments for provenance/reuse. Cost: very low library. |
| 2302.04054 | Inferential reproducibility (LMEM+GLRT) | F-17 | model nondeterminism as variance via LMEM + GLRT + reliability coefficient; significance-test performance diffs. Cost: low analysis — the "real-win" gate. |

(Bonus noted, not counted: 2401.13744 counted above; 2406.17488 env-vs-instrument drift separation; 2506.15840
XGBoost in-field calibration.)

## Synthesis
WAVE-1 (adopt first): EFA-YOLO (F-11), temporal event validation (F-12), post-hoc conformal under shift
(F-13), label-free drift monitors (F-14), GP IoT drift correction (F-15), IR optical-flow (F-16), tooling
(F-17). WAVE-2: STCNet, MobileViT-S KD, WISE, SSL, operator-CP UI. WAVE-3 (parked): SmokeyNet (needs weather),
obscured-flame 3D-conv (overfit flag), thermal/IR fusion (IR hardware vs INR 2000 cap), UAV policy early-exit.
NOT-A-REAL-WIN RISKS: single-split YOLO tweaks shrink cross-camera; >98%/~100% headlines = overfit flags;
temporal/flow cues framerate/codec-sensitive; pseudo-labels confirmation-bias; conformal coverage breaks under
shift without reweighting (F-13 WCPS mitigates); blind/neighbor sensor calibration fails on sparse nodes. GATE
every candidate through the inferential-reproducibility test (2302.04054) + mandatory held-out cross-camera
eval before scoring benefit×evidence/cost.

## Tally (P17)
P17 NEW quota = 22 primary arXiv (≥15 MET). Depth all ABS (0 FT) — running body-level deep FT NEW total
UNCHANGED at 100.
