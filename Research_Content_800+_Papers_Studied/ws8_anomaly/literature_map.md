# ws8_anomaly/literature_map.md — P9 anomaly-detection reading map (WS8a)

Phase P9 · RESEARCH-ONLY. Quota = **35 NEW primary arXiv papers** (≥15 required; aim ~28 → exceeded).
HONEST DEPTH (§0.5): ALL 35 are **ABS** (abstract/title/venue; 0 FT). arXiv API via throttled web_fetch
worked (one-at-a-time, AND-of-terms syntax; no 429s). web_search NOT used (no API key). All metrics
SOURCE-REPORTED, never ours (Rule 16). Paper IDs are subagent-reported, not each independently re-fetched.
Note: many 2026-dated arXiv stamps (session date 2026-10-10) — plausible, recorded as source-reported.

## Family A — Video anomaly detection (6) [SUPPORT-only in our scope]
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2610.05129 | RBA explainable WS-VAD | MLLM attention-adaptation (~0.012% params), video-level labels; improves native-readout across 3 VAD benchmarks. Cheap explainable rationales for CCTV. |
| 2609.07455 | Parser-free VLM verification (federated) | MIL scorer + frozen VLM logit-interface verify; UCF-Crime, improves frame-AUC/AP; text-gen verification fragile to prompts/parsers (eval-pitfall). |
| 2609.05066 | Adaptive multi-granularity WSVAD | Temporal Refinement + adaptive event segmentation vs fixed top-k; variable-duration events. |
| 2608.25344 | CoRE coarse-to-fine risk evidence | intervention-based temporal+entity attribution from video-level labels (DoTA/UCF-Crime). |
| 2608.21854 | "Look Inside Each Video" EVAL-CRITIQUE | within-video pairs are 0.071-0.388% of all pairs → Micro-AUROC ≠ localization; per-video-mean keeps ~99% of margin at 50% Within-AUROC. REPORT Within-AUROC. |
| 2608.12045 | SST-WSVADL patch-level | exposes background/scene bias; releases frame-level spatial annotations. Fixed-camera fire CCTV may learn the room not the smoke. |

## Family B — Multivariate time-series / sensor anomaly (6) [PRIORITY 1]
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2609.34161 | GT-PSSM | probabilistic state-space + graph-transformer; uncertainty-aware scoring cuts benign-fluctuation false alarms. |
| 2608.15727 | FirstDiff | one-step diffusion (first reverse-step noise suffices); SOTA on 5 benchmarks, single denoise eval → edge-feasible. |
| 2608.03926 | PRISM TS-to-image | VUS-PR best on 10/14 datasets (+41% avg); ImageNet frozen encoders keep 92% at 1.8x faster. Reuse vision backbones on sensors. |
| 2606.20055 | PaAno+ | lightweight multiscale + cross-variable; SOTA on TSB-AD (VUS-PR); for resource-limited terminals → edge. |
| 2607.15799 | Knowledge-assisted multi-graph | process-knowledge-constrained graphs; physics/process priors as graph structure (ties to physics-residual). |
| 2608.09246 | Explainable GNN component diagnosis | root-cause to component not noisiest sensor → actionable alerts. |

## Family C — OOD / model-health / drift (5) [PRIORITY 1]
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2609.39215 | Streaming AD benchmark (KDD'26) + TSB-drift | KEY: static TSAD significantly OUTPERFORMS streaming/adaptive in most settings. "Adapt online" not automatically better. |
| 2608.20557 | ANT segmentation-guided TTA | structure-guided TTA beats entropy-min TTA under hardware/protocol shift (+2.9/3.6% AUC). New-install domain shift. |
| 2608.14089 | RCV regime-conditional verification | label-free drift signal + correctness monitor as a cheap wrapper over the deployed detector; triggers repair only when needed. |
| 2610.09993 | EfficientAD+DDPM open-set | AUROC 0.9985; fixed-weight fusion recovers only 40-70% of oracle; AP/F1 saturate under inverted balance → use MCC/NPV (eval-pitfall). |
| 2608.20663 | Shortcut learning (grape) | annotation granularity amplifies shortcut; INVISIBLE to in-dist eval, only OOD negatives reveal it → audit our fire datasets with OOD negatives. |

## Family D — Uncertainty / thresholding / EVAL CRITIQUE (6) [governs protocol]
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2607.11969 | Adversarial stress-test of post-PA metrics | at N=1 none gameable; under best-of-N, affiliation-F1 + ALL ROC (incl VUS-ROC) inflate (affiliation 0.98 by N=41); PR-based + PA%K floored. REPORT single-run / prefer VUS-PR. |
| 2603.18985 | Revisiting OmniAnomaly (PCA) | SIMPLE-BASELINE: PCA ≈ or > OmniAnomaly on SMD under identical thresholding; PCA WINS without point-adjust. |
| 2511.18739 | Problem-oriented metric taxonomy | 20+ metrics on 6 axes; NAB + PA limited resistance to random-score inflation; pick metric by objective (delay-aware → timeliness+PR). |
| 2409.13053 | Balanced Point Adjustment (BA) | PA biased toward TPs/over-estimates; axiomatic fairer event-level credit. |
| 2405.12096 | PATE (KDD'24) delay-aware | proximity-weighted PR AUC with buffer zones; rewards early, penalizes late. FITS fire early-warning latency objective. |
| 2311.11235 | TriAD self-supervised tri-domain | 3x PA%K-F1 on UCR; names "random functions detect many benchmark anomalies" pitfall. |

## Family E — Physics-residual / cyber-physical + network (6) [PRIORITY 2 + ties P12]
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2609.34804 | Physics-attested federated | mines CPS invariants as admission gate vs data-poisoning; 9 invariants detect 20/35 SWaT attacks; recovers 69-100% recall lost to replay poisoning. Residual = detector + integrity gate. |
| 2606.06347 | TimesFM attack detection | TS foundation model as zero-shot residual generator (no plant model); IEEE 14-bus comparable/superior; can substitute corrupted measurements. |
| 2609.21217 | X-SPUR surprisal IDS | per-token cross-entropy surprisal + per-protocol Z-score; TOW-IDS AUC 0.9987; field-level explanations. Template for alert-spoofing stream. |
| 2605.25135 | ASTRO RL-threshold GNN | DQN learns adaptive threshold; SWaT F1 0.990, WADI F1 0.788. RL thresholding vs EVT/static. |
| 2605.00929 | PhaseNet++ phase-aware | STFT AE keeping phase; SWaT F1 90.98%; honest cross-protocol-comparability caveat. |
| 2606.01691 | IstGPT LLM+graph | LLM-derived sensor-actuator dependency graphs + GNN; best F1/eTaF1 across 9 datasets. |

## Family F — Edge / TinyML (6) [edge tier]
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2610.07489 | Dual IDS QLSTM+QCAE on FPGA | >99.9% CAN attack acc; 0.25 ms/0.8 mJ (QLSTM), 0.42 ms/1.1 mJ (QCAE). Supervised+unsupervised dual edge pattern + budgets. |
| 2606.02256 | ArrythML AE on ESP32-S3 | INT8 TFLite-Micro; recall 84%, F1 79%, ~180 KB, 9 ms on-device. Realistic tiny-AE envelope; label-noise caveat. |
| 2604.08581 | Autonomous Z-score on MCU | SIMPLE-BASELINE: on-device train+infer z-score; P=R=1.00 on real appliance; ~3.3 KB SRAM, 63 KB Flash, tens-of-µs. Keep statistical baseline on edge. |
| 2603.27393 | K-means TinyML + model reuse | on-device K-means + "train once share everywhere" for node fleets. |
| 2603.26135 | TinyML acoustic AD | MFCC + light NN on MCU; UrbanSound8K 91% acc. Acoustic channel complements CCTV+IoT. |
| 2010.11267 | MicroNets NAS | op-count latency proxy; SOTA on all 3 TinyMLperf tasks incl. anomaly detection. Edge model-sizing reference. |

## Extras found (NOT counted in the 35)
2609.18107 FoundAna (GNN graph-AD foundation model); 2609.29745 encrypted-5G OPC-UA IDS (benign variation
inflates FPR → control-plane-aware threshold); 2609.15772 symbolic-temporal spike encoding (neuromorphic
edge); 2609.29580 SCOUT/OddBench audit (train-test overlap in 355/690 datasets); 2508.04818/2508.02903
RADAR/RDDPM (MVTec image AD). CARRIED from prior-phase WS8 brief (P4, not re-counted): 2610.03649 (on-board
SSL anomaly), 2509.18176 (CNN-LSTM InSAR), 2502.15901 (TS-OOD ≠ vision-OOD), 2605.31155 (hyperspherical TF
OOD), 2609.34836 (nowcast residual ensemble).

## Synthesis → our decisions
- EVAL (D-family + 2608.21854 + 2609.29580): point-adjust BANNED as primary; prefer VUS-PR + PATE (delay-
  aware); report single-run or disclose best-of-N; report Within-AUROC for video; audit datasets for train-
  test overlap + scene/annotation shortcuts with OOD negatives. → evaluation_protocol.md confirmed.
- SIMPLE BASELINES (2603.18985, 2609.39215, 2604.08581): PCA/z-score/static detectors frequently match or
  beat deep/streaming methods under honest eval → simple-baselines-first mandate confirmed; static+periodic-
  retrain over always-adapting.
- PHYSICS-RESIDUAL (2609.34804, 2606.06347): CPS invariants / TS-foundation residuals double as detector +
  anti-spoofing integrity gate → confirms family (d) + feeds P12 threat model.
- EDGE (2604.08581, 2606.02256, 2610.07489, 2010.11267): KB-scale statistical + tiny-AE on-node feasible
  with real latency/energy budgets; video anomaly stays on gateway. → design.md edge subset confirmed.

## Tally & honesty
P9 NEW quota = 35 primary arXiv (ABS; ≥15, aim ~28 → exceeded). Depth: 35 ABS, 0 FT. Running body-level deep
FT NEW total UNCHANGED at 100 (P9 added breadth). web_search unavailable (no key); IDs subagent-reported,
not each re-fetched; dataset licenses mostly "not visible in abstract" → [D]/indicative. Full-text metric
extraction (exact VUS-PR/PATE/SWaT tables) is an OPEN action if deep numbers are needed in the build.

---

# P10 implementation-recipe reading map (WS8b) — 23 NEW primary arXiv (ABS), none reuse P9

HONEST: all ABS; IDs/numbers subagent-reported (ccaba769), not independently re-fetched; web_search unused
(no key); throttled arXiv (no 429s). Full cited default-recipe registry = ws8_anomaly/spec/sota_targets.md §3.

## Thresholding / false-alarm (4)
| arXiv | Short | Recipe (source-reported) |
|-------|-------|--------------------------|
| 2601.21293 | PG-TMT tiny-Mamba + EVT | EVT PoT + dual-threshold hysteresis + trimmed-tail fit → auditable alarm-rate budget; sub-1 MB, Jetson <7 ms p99. |
| 2605.13642 | nonconform (conformal AD) | wrap any PyOD/sklearn detector → conformal p-values + Benjamini-Hochberg FDR control instead of a hand-picked threshold. REFERENCE impl path. |
| 2609.29580 | SCOUT | factorwise split-conformal → nominal FPR; AUDIT train/test row overlap (355/690 overlapped) before trusting AUROC. |
| 2605.00482 | C-MTAD-GAT | shared multi-entity model; per-feature thresholds from validation residual quantiles (fleet-of-sensors fit). |

## Deep MTAD training / reproducibility (6)
| arXiv | Short | Recipe (source-reported) |
|-------|-------|--------------------------|
| 2606.09874 | Inference windowing study | OVERLAPPING inference windows avg +28% rel., can reorder rankings; reconstruction baselines competitive on TSB-AD/UCR. KEY repro. |
| 2603.12916 | AxonAD | EMA target encoder + masked query-prediction aux score fused with reconstruction error (dependency-shift anomalies). |
| 2605.23139 | CALAD | channel-aware contrastive weighted by per-channel reconstruction-error relevance; robust to shift. |
| 2609.39337 | WinoTS | wavelet self-distillation pretrain; frozen linear-probe beats supervised-from-scratch; time-freq aug > spatial aug. |
| 2607.12454 | Zero-shot FM (negative) | zero-shot TimesFM NOT competitive on SWaT — too-good reconstruction hides persistent anomalies; only flags boundaries → change-point use only. |
| 2609.16314 | Cross-modal reconstruction | reconstruct-each-modality-from-others + adaptive test-time threshold; biggest gains in hardest OOD regimes. |

## Score calibration / uncertainty (4)
| arXiv | Short | Recipe (source-reported) |
|-------|-------|--------------------------|
| 2609.14234 | GTFD conformal risk head | threshold-free coverage-guaranteed scores; ablation ~1.9 AUROC + ~29% FPR reduction from the conformal head. |
| 2606.13780 | Look-elsewhere conformal | Mondrian/weighted conformal repairs calib-vs-deploy drift; uncalibrated multi-region scanning fabricated a ~46σ false excess. |
| 2610.01384 | CLEAR | post-hoc latent-conflict calibrator, no retraining; +8.29 OOD / +5.01 adversarial AUROC, 17.4× faster. |
| 2610.10116 | Wasserstein evidential | single-pass Dirichlet uncertainty; Wasserstein order per backbone (2nd CNN / 3rd transformer). |

## Classic / simple (4)
| arXiv | Short | Recipe (source-reported) |
|-------|-------|--------------------------|
| 2610.12244 | RIFT | deterministic MST-based IF generalization; IF-comparable accuracy, LOWER seed variance (ensemble). |
| 2610.02345 | KCM/KAR convergence-collapse | reconstruction/residual detectors get WORSE at convergence; early-stop or Kernel-Anchored Regularizer; KCM = training-free closed-form baseline. |
| 2311.03393 | Matrix-profile sketch | discord mining cost independent of #channels; ≥50× throughput; dynamic channel add/delete. |
| 2610.03649 | On-board SSL + classic | SSL-latent compression + IF/OCSVM/LOF edge baseline; ESA Phisat-2 / IMAGIN-e; send-only-anomalous alerting. |

## Edge / TinyML (2 new)
| arXiv | Short | Recipe (source-reported) |
|-------|-------|--------------------------|
| 2505.17662 | Tiny Transformer on FPGA | QAT to 4-bit (INT8 for MCU) + Optuna HW-aware search → integer-only accelerator; 0.033 mJ/inference, ms latency. |
| 2606.13754 | D2H-AD (HDC) | hyperdimensional computing, binary ops, MCU-friendly; encoding alone +5.4% ROC-AUC (ablation); robust to imbalance/noise. |

## Video (support-only) (5)
| arXiv | Short | Recipe (source-reported) |
|-------|-------|--------------------------|
| 2601.18135 | FoGA | tiny U-Net future-frame + forward-consistency loss, fuse immediate+forward errors; ~2M params, up to 155 FPS. EDGE lead. |
| 2604.00360 | VADMamba++ | Gray→RGB single-proxy reconstruction (no optical flow) + fuse prediction/quantized-feature errors. |
| 2610.11149 | Uni-DSM | denoising-score-matching likelihood + motion-aware weighting; SDSM = label-free ANTICIPATION (early warning). |
| 2509.22544 | HyCoVAD | SSL pre-screen → LLM validate suspect frames only (cost-controlled escalation); 72.5% frame-AUC ComplexVAD + adaptive thresholding protocol. |
| 2606.29498 | Patch WSVAD | weakly-sup MIL + Proximity-Aware Top-k → where+when localization without boxes. |

## What changed (quota effect)
Thresholding → CONFORMAL p-values + FDR / EVT-hysteresis as DEFAULT (not hand-picked); "train-to-convergence
is a bug" rule for reconstruction/residual AEs; hardened deep-vs-simple protocol (overlapping windows, row-
overlap audit, no naive zero-shot FM for persistent anomalies); concrete edge recipes (QAT+HW-search, HDC);
video tiny-fast + anticipation + SSL→LLM escalation. All placeholders in the family specs resolved via
sota_targets.md §3.

## Tally
P10 NEW quota = 23 primary arXiv (ABS; ≥15 required, aim ~20 → exceeded). Depth 0 FT. Running body-level deep
FT NEW total UNCHANGED at 100.
