# ws6_robustness/literature_map.md — robustness & security literature map (WS6)

Phase P16. HONEST: all ABS; IDs/years arXiv-ID-derived + subagent-reported (reader e7c17e5e; 9 fetches), NOT
re-fetched (residual risk, §0.5); all numbers SOURCE-REPORTED (Rule 16) on vision/driving/IoT benchmarks (NOT
a fire system → transfer hypotheses). Backs ws6_robustness/{robustness_catalogue, defense_and_monitoring_plan,
robustness_evaluation_plan}.md + P16 SOTA scan. Running body-level deep FT NEW total UNCHANGED at 100.

## P16 section — 23 NEW primary arXiv

### T1 adversarial attacks/defenses (classifiers & detectors)
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2101.11453 | Meta Adversarial Training vs universal patches | meta-learn evolving universal patches during training, low extra compute; raises patch robustness (classification + traffic-light detection). Camera front-end hardening. |
| 2307.02055 | FGSM & patch impact study | strong pretrained ResNet/GoogleNet/DenseNet degrade sharply under FGSM + patch. Off-the-shelf CCTV classifiers not attack-safe → human confirmation. |
| 2411.16162 | Sparse multi-patch attack | jointly optimizes multiple patches' location+perturbation, any shape/count; new SOTA over prior sparse/patch. Red-team must cover multi-patch physical threats. |

### T2 natural corruption / distribution shift / OOD
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2206.13405 | MSCR corruption-robustness metric | minimal-separation-based interpretable per-dataset metric; accuracy-vs-corruption tradeoff NOT inherent. Yardstick to compare detector variants under weather/lighting. |
| 2110.06513 | Spatio-temporal corruption benchmark | Mini Kinetics-C / SSV2-C; Transformers > CNNs on corruption; image noise-training may NOT transfer to video. Fire is temporal → image tricks may not protect the video pipeline. |
| 2102.11273 | Augmentation↔corruption interaction | robustness drops when test corruptions perceptually dissimilar from training augmentations. Augmentation hardening can give false confidence on unseen field corruptions. |

### T3 backdoor / data-poisoning
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2206.12654 | BackdoorBench | 8 attacks × 9 defenses, 8000 pairs; exposes unverified defense claims. Reusable protocol to vet third-party/pretrained models. |
| 2407.19845 | BackdoorBench extended | 20 attacks, 32 defenses, 11,492 pairs, 18 analysis tools. Current standardized supply-chain poisoning reference. |
| 2202.11203 | Under-confidence backdoor (LSBA) | probabilistic label flipping keeps target prob only slightly higher; high stealth + high ASR, evades human + auto defenses. Poisoning hides below confidence-threshold alert logic → provenance control. |

### T4 sensor fusion / spoofing
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2603.11365 | D-SLAMSpoof LiDAR injection | spatially-shaped point injection compromises SLAM even in feature-rich scenes; ISD-SLAM inertial cross-check defense. Template for cross-checking one sensor against an independent modality. |
| 2307.04692 | Spoofing-resilient LiDAR-GPS factor graph | chi-squared residual detector between Chimera authentications; <5 m nominal, bounds error under spoofing. Signed signals + residual anomaly detection = fusion-integrity pattern. |
| 2302.07341 | Cooperative perception vs LiDAR spoofing | neighbor LiDAR + FDII detects fake/removed/adversarial objects; CARLA detects each attack. Redundancy/cross-sensor voting before alerting. |

### T5 IoT/edge & wireless security
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2301.09615 | ESWORD jamming testbed | HIL jamming on Colosseum (≤50 SDRs); patterns match real jamming. Safe testbed to assess jamming before deployment. |
| 1509.09222 | On Jamming Against Wireless Networks | 1 jammer/AP → outage 1%→80%, retransmits double interference. Little attacker effort collapses the alert link → wired/redundant paths + jamming detection. |
| 1411.3736 | Energy-efficient routing under jamming | joint outage-allocation + routing + spread-spectrum from measured per-node jamming; energy savings. Jamming-aware routing for sensor meshes. |

### T6 monitoring / drift / failure prediction
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 1707.07821 | Hierarchical hypothesis-testing drift (HLFR) | handles recurrent/abrupt/gradual drift + imbalance; beats SOTA on precision/delay/adaptability. Principled drift monitoring with Type-I/II analysis. |
| 2104.10529 | Lightweight IoT drift adaptation (OASW) | adaptive LightGBM + optimized sliding window, online anomaly; high accuracy/efficiency, no human intervention. Edge-friendly BUT auto-adaptation must be Rule-19-gated (advisory). |
| 2404.02572 | Incremental graph-stream drift | per-class prototype graphs + loss-based drift detector; critical-infrastructure modelling. Drift-triggered recalibration of a structural model. |

### T7 certified robustness evaluation
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2206.03669 | Certified robustness vs real-world shifts | neural-symbolic verification of learned-perturbation specs, CEGAR; beats verifiers on MNIST/CIFAR shifts. Moves certification toward realistic shifts (small scale). |
| 1910.14655 | RobBoost certified ensemble | weights base models to maximize a robustness certificate; more certifiably-robust than averaging, better clean acc. Raise provable robustness with limited accuracy loss. |

### T8 deepfake / anomaly detector evasion
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2412.09921 | FaceShield proactive deepfake defense | perturbs diffusion attention to protect faces; JPEG-robust, transfers to GANs; SOTA disruption of diffusion deepfakes. Proactive protection + compression-robustness concern for CCTV evidence. |
| 2607.25842 | Adversarial deepfake gen + purification detection | multi-model PGD (DiffJPEG/MI/DI/EoT) evades 12 detectors (90% / 57.6%); purification signal AUROC 0.81-0.98 but collapses at JPEG-Q70 cliff. Detector ensembles evadable; single evasion threshold untrustworthy. |
| 2003.01279 | Disrupting Deepfakes | class-transferable adversarial attacks + AT-for-GANs; blur defeated by spread-spectrum. Defenses+evasions co-evolve → continuous red-teaming. |

(Cross-cutting, ties P19: 2610.08810 confident-while-wrong under shift; 2608.22293 random CV overstates skill
— both argue uncertainty-monitoring + spatial-block validation. Cited in catalogue §2 / eval plan §1.)

### Synthesis (P16) — see the three WS6 docs
1. ATTACK CLASSES (severity HIGH): patches on CCTV (2411.16162); corruption/shift incl. video (2102.11273,
   2110.06513); stealthy backdoors (2202.11203); sensor spoofing (2603.11365, 2307.04692); jamming
   (1509.09222); detector evasion (2607.25842).
2. DEFENSES (most transferable = cross-sensor redundancy + residual detection, least accuracy cost: 2302.07341,
   2307.04692, 2603.11365; single-model hardening benchmark-local: 2101.11453, 2206.13405/2102.11273; certified
   = small-scale lower bound: 1910.14655, 2206.03669; supply-chain vetting: 2206.12654/2407.19845).
3. MONITORING: uncertainty-entropy gate not deterministic confidence (2610.08810); HLFR drift (1707.07821);
   Rule-19-gated edge adaptation (2104.10529); residual/FDII monitors; monitor-the-monitor (2607.25842 cliff).
4. EVALUATION: standardized matrices (BackdoorBench); clean+robust together (2206.13405, 1910.14655);
   worst-case evasion (2607.25842); held-out/video corruption (2102.11273, 2110.06513); ODD coverage
   (2608.20864); spatial-block not random CV (2608.22293).

## Tally (P16)
P16 NEW quota = 23 primary arXiv (≥15 MET). Depth all ABS (0 FT) — running body-level deep FT NEW total
UNCHANGED at 100.
