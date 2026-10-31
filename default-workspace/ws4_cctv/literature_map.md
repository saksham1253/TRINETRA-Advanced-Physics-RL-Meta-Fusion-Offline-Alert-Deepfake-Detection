# ws4_cctv/literature_map.md — P8 CCTV fire/smoke detection reading map

Phase P8 · WS4 · RESEARCH-ONLY. The ≥15 NEW quota reads (aim 30-40) for P8 — **41 arXiv sources** logged
(quota met). HONEST DEPTH (§0.5): ALL are **ABS** (abstract/title/venue); several ABS* had the headline
metric truncated in the listing → marked "metric not retrieved" rather than inventing numbers. NO full
texts were read this phase (0 FT). Tooling: web_search had NO API key; arXiv Atom API was rate-limited
(HTTP 429) so discovery used the arXiv HTML search UI + /abs pages. Paper IDs/titles are subagent-reported
and were NOT each independently re-fetched by me → treat as source-reported (recorded honestly for the
audit). All metrics SOURCE-REPORTED, never ours (Rule 16).

## Group 1 — Fixed-camera early smoke + canonical baselines
| # | arXiv | Short | Note |
|---|-------|-------|------|
| 1 | 2112.08598 | FIgLib + SmokeyNet | ~25k fixed-view HPWREN smoke imgs; CNN+LSTM+ViT; "rivals human" (src-reported, qualit.). Canonical fixed-camera early-smoke baseline + leakage-safe (per-camera/event) + time-to-detection reference. |
| 3 | 2402.05349 | PYRONEAR-2025 | real-world early-wildfire camera-network benchmark; field multi-site → site/camera-grouped splits + false-alarm estimation. |
| 30 | 2211.01629 | Image-based early wildfire system | NeurIPS'22 CCCW; fixed-camera early-detection pipeline in FIgLib/HPWREN ecosystem. |
| 2 | 2212.14143 | Multimodal wildfire smoke | FIgLib + weather/met fusion → cross-modal false-alarm cut (metric truncated). |

## Group 2 — Compact / edge detectors + false-alarm reduction (SHORTLIST core)
| # | arXiv | Short | Note |
|---|-------|-------|------|
| 4 | 2010.08833 | OnFire compact CNNs | ShuffleNetV2-/NasNet-A-OnFire; src-reported 95% full-frame acc, 49 fps on Jetson Xavier-NX. Best-documented true low-power baseline; non-temporal (optimistic vs CCTV nuisance). |
| 6 | 2510.10108 | Uncertainty post-detection | YOLOv5n/v8n on D-Fire + lightweight Confidence Refinement head re-scores via uncertainty+color/edge/texture; NMS/Soft-NMS named as a false-alarm/suppression failure mode. |
| 15 | 2304.07584 | FSDNet | YOLOv3+DenseNet "complex scenarios"; pre-v8 efficiency lineage baseline. |
| 16 | 2501.08639 | Edge transfer-learning | UAV+edge on-device inference, transfer learning from scarce fire data; latency-vs-accuracy. |
| 31 | 2501.09926 | ForestProtector | low-cost IoT + machine vision + deep RL wildfire monitoring; architecture ref (RL tangential). |

## Group 3 — Distillation / weak supervision / cascades (edge compression)
| # | arXiv | Short | Note |
|---|-------|-------|------|
| 17 | 2408.10843 | Teacher→student seg | distill large teacher into small real-time segmentation student (on-UAV). |
| 38 | 2609.18227 | WISE | weakly-supervised (tile labels) teacher→student; src-reported tile-F1 0.964, 0.12M params, ~3 GFLOPs, 0.10-0.26 s/tile. Strong edge recipe (satellite domain). |
| 18 | 2508.16739 | Two-stage adaptive compression + detect | cascade + compression robustness (IEEE JSTARS). |
| 24 | 2207.03708 | Smoky-vehicle coarse-to-fine | two-stage video cascade; vehicle/exhaust smoke nuisance. |

## Group 4 — Temporal / motion / dynamic-texture (false-alarm suppression)
| # | arXiv | Short | Note |
|---|-------|-------|------|
| 7 | 2508.14597 | Optical-flow + Swin + uncertainty | monocular smoke segmentation; aleatoric+epistemic uncertainty flags unreliable preds; heavier than edge budget. |
| 23 | 2307.00104 | Obscured flame via smoke motion | occlusion failure mode → temporal smoke-motion remedy. |
| 25 | 1703.05530 | 3-orthogonal-plane CNN dynamic texture | smoke as spatiotemporal texture (XY/XT/YT); vegetation/water/fabric confusers. |
| 22 | 2607.03131 | Multi-task surveillance + temporal event validation | require event persistence across frames before alarm; zone-auth privacy touch. |

## Group 5 — Night / IR / thermal (RGB fails under smoke)
| # | arXiv | Short | Note |
|---|-------|-------|------|
| 26 | 1909.12937 | Unsupervised IR fire/smoke seg | label-free IR segmentation; night/IR + semi/unsupervised. |
| 27 | 2307.04223 | IR+thermal fusion human detection | thermal penetrates heavy smoke where RGB fails. |
| 28 | 2312.09159 | WIT-UAS IR thermal dataset | IROS'23; thermal fire-scene benchmark (aerial domain shift). |
| 39 | 2606.27128 | FlameVQA (RGB+radiometric thermal) | RGB-only limited by smoke/scale/occlusion; thermal supervision helps. |
| 29 | 2012.14036 | FLAME (aerial RGB+thermal) | prescribed pile-burn RGB+IR; aerial domain-shift caveat. |

## Group 6 — Compression / low-res robustness
| # | arXiv | Short | Note |
|---|-------|-------|------|
| 19 | 2512.01788 | Learned compression → EO seg (fire) | compression choice measurably affects downstream fire segmentation → put compression in eval. |
| 20 | 2509.12701 | SmokeBench (surveillance desmoking) | real-world 0-15 min early-smoke surveillance desmoking; early-stage thin-smoke hard regime. |
| 21 | 2506.02167 | Fire360 degraded 360° video | degraded-visibility robustness-collapse regime. |

## Group 7 — Benchmarks / eval-protocol / leakage / generalization (PROTOCOL evidence)
| # | arXiv | Short | Note |
|---|-------|-------|------|
| 5 | 2410.16631 | Multi-Scene FSD benchmark | public FSD datasets lack standardized construction/metrics → the field bottleneck; supports standardized leakage-aware protocol. |
| 8 | 2508.11696 | CCTV smoking-detection (WITHDRAWN) | authors withdrew: augmentation-induced LEAKAGE across splits + metric inconsistency → textbook cautionary case. |
| 40 | 2603.02465 | Walsh-Hadamard + domain adaptation | tackles DOMAIN SHIFT/generalization (central leakage-safe concern). |
| 41 | 2511.16617 | Generative AI synthetic→real gap | synthetic smoke augments scarce data but real domain gap must be measured. |
| 9 | 2606.10174 | GWFP image+video dataset | large open corpus; video → temporal + group-split potential. |
| 10 | 2604.23542 | AusSmoke/MultiNatSmoke seg | diverse multi-site smoke segmentation (cross-site eval). |
| 14 | 2503.14552 | Survey: fire/smoke classify/segment/detect | task-taxonomy structuring reference. |

## Group 8 — Foundation / MLLM / open-vocab (AVOID as edge detector; note for P14Z)
| # | arXiv | Short | Note |
|---|-------|-------|------|
| 11 | 2512.11215 | SmokeBench (MLLM eval) | all MLLMs struggle localization esp. early/small; perf scales with smoke VOLUME not contrast. |
| 12 | 2609.07823 | SAFIRE (MLLM safety benchmark) | general MLLMs not yet reliable for fine-grained fire/smoke. |
| 13 | 2610.10946 | AI4Fire (LLM eval) | "grounded" uses a smoke-free REFERENCE FRAME from same camera → background-differencing idea for fixed CCTV. |
| 33 | 2505.17395 | ViT wildfire classification | transformer baseline; single-dataset optimism caveat. |
| 35 | 2602.13305 | WildfireVLM | VLM early detection (satellite; too heavy for edge). |

## Group 9 — Satellite/aerial on-constraint deployments (engineering lessons only; domain shift)
| # | arXiv | Short | Note |
|---|-------|-------|------|
| 34 | 2605.15894 | EfficientNet+CBAM+evidential smoke density | uncertainty output; edge-feasible recipe (satellite). |
| 36 | 2601.14475 | NASA AMS wildfire localization | 12-channel aerial; multispectral; strong domain shift. |
| 37 | 2605.06273 | On-orbit real-time wildfire detection | hard onboard compute budget → quantization/engineering lessons. |
| 32 | 2412.20006 | Adversarial robustness wildfire prediction | only adversarial-robustness fire paper found → include adversarial stress-tests. |

## Adversarial/privacy GAP (honest)
Dedicated camera-tamper / blinding / replay-spoofing + privacy(face-blur) papers for fire CCTV were
essentially ABSENT in this arXiv-only search (only #32 on prediction-model robustness). → carried as an open
action to search MDPI Sensors/Fire + IEEE when web_search is restored; the WS2/P11 deepfake handoff covers
replay-spoofing conceptually.

## Tally & honesty
P8 NEW quota = **41 arXiv sources** (≥15 required; aim 30-40 → exceeded). Depth: **41 ABS, 0 FT** (honest —
no full texts; arXiv API rate-limited, web_search no key). Running body-level deep (FT/FT-PARTIAL) NEW reads
UNCHANGED at 100 (P8 added breadth, not depth). Paper identities are subagent-reported and not individually
re-fetched by me; recorded as source-reported. Sparse topics (tamper/spoof/privacy, explicit steam-vs-smoke
& cloud/fog/sunset nuisance studies, deployable open-vocab fire detectors) flagged for non-arXiv follow-up.

---

## P14Z section — ZERO-SHOT / OPEN-VOCAB quota — 16 NEW primary arXiv (reader a16b8521; 9 fetches)
HONEST: all ABS; IDs/years arXiv-ID-derived + subagent-reported, NOT re-fetched (residual risk, §0.5); all
numbers SOURCE-REPORTED. Backs ws4_cctv/zero_shot_design.md (D-011) + P14Z SOTA scan. Running body-level deep
FT NEW total UNCHANGED at 100.

### T1 open-vocab classification backbones
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2303.15389 | EVA-CLIP | 5.0B EVA-02-CLIP-E 82.0 / L 80.4 zero-shot ImageNet-1K top-1. Strong frozen open-vocab backbone; raw cosine/logit → needs calibration. |
| 2403.15378 | Long-CLIP | long-text CLIP; +~20% long-caption / +~6% COCO/Flickr retrieval, keeps zero-shot. Long descriptive hazard prompts. |
| 2510.02270 | microCLIP | coarse-fine token fusion self-training; +2.90% over 13 fine-grained benchmarks, label-free. Sharpens smoke-vs-steam cues (adaptation not pure ZS). |

### T2 zero-shot anomaly / OOD (unknown-hazard analogue)
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2306.09269 | WinCLIP-based VAND entry | zero-shot segmentation + foreground; VisA F1-max 81.5 sample / 24.2 pixel. Closest "unknown hazard" analogue; weak localization → calibrate before fusion. |
| 2512.02520 | CoDeGraph | FAILURE MODE: "consistent anomalies" bias distance-based ZS (similarity-scaling, neighbor-burnout); graph-community filter. Recurring nuisances (haze, glare) mis-scored. |
| 2510.15602 | Quantized FCA (QFCA) | real-time ZS texture anomaly, ~10× speedup ~equal accuracy. ZS anomaly at CCTV frame rates; contrast-boost preprocessing. |

### T3 prompt / test-time tuning
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2501.16404 | DynaPrompt | online TTPT w/ prompt buffer, entropy+prob-diff selection, anti-collapse; effective over 14 datasets. Per-camera label-free adaptation; its signals feed calibration. |
| 2512.12268 | MetaTPT | meta dual-loop TPT, learned per-sample augmentations; SOTA domain-generalization/cross-dataset. Targets site/weather/lens shift. |

### T4 zero-shot action/video
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2107.13029 | TruZe | EVALUATION FAILURE: Kinetics↔UCF/HMDB class overlap inflates ZS; leakage-free split drops ZS up to 8.9% (few-shot up to 17.1%). De-rate external ZS numbers for leakage. |
| 2605.01165 | CEZSAR | contrastive video-sentence ZS action recognition w/ auto negatives; SOTA UCF-101/Kinetics-400. Video-level open-vocab event complement; uncalibrated, domain-shift-prone. |

### T5 fire / disaster zero-shot (domain reality)
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2504.13231 | WildFireCan-MMD | Canadian wildfire multimodal X posts, 12 themes; custom 84.48% f-score > zero-shot VLMs. Trained BEATS ZS in fire domain. |
| 2610.10946 | AI4Fire | 5 wildfire tasks, bare vs grounded; NO core ZS model beat trivial baselines; documented leakage/label flaws; grounding helps when input carries the answer. Complement-not-replace; grounded-reference trick reusable. |
| 2607.07951 | Wildfire-PM2.5 FM benchmark | BiLSTM best (MAE 5.16, F1 0.63); ZS TSFMs barely beat persistence, Chronos-2 negative-R² tail instability; LoRA repairs but no FM beats trained. ZS scores tail-unstable OOD → variance-stabilize/calibrate. |

### T6 calibration of zero-shot
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2303.12748 | Enabling Calibration in ZS VLMs | ZS CLIP miscalibrated; ONE learned temperature per backbone generalizes across dataset AND prompt. KEY enabler: cheap transferable calibration before fusion. |
| 2512.12997 | Adversarial-CLIP uncertainty calibration | perturbation suppresses uncertainty → over-confidence; Dirichlet reparameterization restores calibrated uncertainty + robustness. Use calibrated uncertainty, not raw softmax. |

### T7 failure modes
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2404.03539 | Is CLIP the fine-grained roadblock? | poor attribute separability; cosine matching discards fine-grained info; latent re-projection helps. Explains smoke-vs-steam/cloud/dust confusion → coarse complement + re-projection head. |

(Noted, not counted: 2311.14029 CLIP compression fragility; 1712.03323 remote-sensing ZSL 14.3%; 2604.15609
BETA black-box TTA +3.4% ImageNet-C.)

### Synthesis (P14Z) — see zero_shot_design.md D-011
- STRONGEST ZS: scaled CLIP backbones (EVA-CLIP 82.0) + test-time prompt adaptation (DynaPrompt/MetaTPT) for
  shift; ZS anomaly (WinCLIP) as unknown-hazard complement.
- CALIBRATION MANDATORY before fusion: ZS miscalibrated (2303.12748), over-confident under perturbation
  (2512.12997), tail-unstable OOD (2607.07951); one temperature per backbone transfers (2303.12748); feed
  entropy/prob-diff too; de-rate external numbers for leakage (2107.13029).
- FIRE REALITY: trained > ZS (2504.13231, 2610.10946, 2607.07951) → D-011 admits ZS only as a calibrated
  LOW-WEIGHT COMPLEMENT, never the primary detector.
- DATASET GAP: no clean permissively-licensed CCTV ZS fire benchmark (leakage/label flaws) → curate internal.

## Tally (P14Z)
P14Z NEW quota = 16 primary arXiv (≥10 required → MET). Depth all ABS (0 FT) — running body-level deep FT NEW
total UNCHANGED at 100.
