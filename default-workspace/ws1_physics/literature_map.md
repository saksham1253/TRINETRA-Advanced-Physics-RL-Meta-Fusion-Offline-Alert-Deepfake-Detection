# ws1_physics/literature_map.md — P7 quota reading map (fire physics + physics-informed ML)

Phase P7 · WS1a · RESEARCH-ONLY. The ≥15 NEW quota reads (aim ~30) for P7. **22 NEW arXiv papers** logged
below (quota met), + 4 noted/skim. Depth: 5 FT + 1 FT-PARTIAL (body-level) + 16 ABS; classic fire-science
correlations are inventory SOURCES (ABS-CANONICAL, not fetched — logged in established_formula_inventory.md,
NOT counted as quota papers). Honest tooling note: web_search had NO API key all phase → arXiv-API-only;
classic plume/radiation/detector correlations returned ~0 on arXiv (see novelty_log + SOTA scan).

Numbers below are SOURCE-REPORTED, never ours (Rule 16).

## Group 1 — Fire physics (forward models for camera/sensor)
| # | arXiv | Title (short) | Depth | What it changed |
|---|-------|---------------|-------|-----------------|
| 1 | 2404.11439 | Börger — visibility / Jin's law V=C/σ | FT | adds the camera-contrast forward model; Jin's law is for HOMOGENEOUS smoke → B-01 uses path-integrated extinction |
| 2 | 2208.03542 | Sitte & Doan — puffing-pool-fire HFM PINN | FT | PINN soft-sensor: infer velocity from T/ρ a thermal camera sees; large-ΔT buoyancy stresses HFM |
| 3 | 2202.06567 | Coenen et al. — pool-fire swirl | ABS | swirl SUPPRESSES puffing → documents where EF-08 f≈1.5/√D breaks (→ B-05 uses a band) |

## Group 2 — Wildfire spread: level-set / CA / data assimilation (EF-11 extensions, Class C)
| # | arXiv | Title (short) | Depth | What it changed |
|---|-------|---------------|-------|-----------------|
| 4 | 2212.00970 | Dabrowski — Bayesian PINN wildfire (level-set) | FT | level-set PDE + B-PINN UQ; MSE PINN breaks temporal continuity under abrupt wind → forecast-likelihood fix |
| 5 | 2206.08501 | Dabrowski — Bayesian filtering level-set DA | ABS | documents level-set's lack of native DA/UQ → filtering mitigation |
| 6 | 2302.04960 | Yoo & Wikle — echo-state net informs front speed | ABS | learns ROS s inside level-set with UQ (physics-guided feature) |
| 7 | 2210.14978 | Yoo & Wikle — Bayesian spatio-temporal level-set | ABS | probabilistic front-velocity + UQ |
| 8 | 1601.06272 | Kaur et al. — turbulence & fire-spotting in spread | ABS | deterministic ROS misses turbulence/spotting → stochastic-PDF augmentation |
| 9 | 2606.11676 | Neural-parameterized CA wildfire | ABS | CNN generates per-cell CA params; IoU>0.6 72-h (reported) |
| 10 | 2502.18738 | PyTorchFire — differentiable CA | ABS | differentiable physics for calibratable params (not PINN) |
| 11 | 2510.09708 | CA real-time CA California | ABS | cheap CA baseline; precision 0.605 (over-spread failure, reported) |
| 12 | 2309.02615 | Shaddy — cWGAN fuse physics sim + satellite | ABS | physics-informed DA from sparse IR; Sørensen 0.81 (reported) |
| 13 | 1101.5745 | Mandel — WRF-Fire coupled model | ABS | canonical level-set + fire↔atmosphere coupling architecture |

## Group 3 — PINN / physics-informed-ML FAILURE MODES + mitigations (why we scope out live fire-PINNs)
| # | arXiv | Title (short) | Depth | Failure mode → mitigation |
|---|-------|---------------|-------|---------------------------|
| 14 | 2109.01050 | Krishnapriyan — PINN failure modes | FT | ill-conditioned soft-constraint landscape → curriculum / seq2seq (1–2 OOM error cut, reported) |
| 15 | 2001.04536 | Wang — gradient pathologies | FT-PARTIAL | stiffness/grad imbalance → learning-rate annealing (50–100× reported) |
| 16 | 2203.07404 | Wang — causality for PINNs | FT | causality violation → causal weighting (first wins on chaotic systems, reported) |
| 17 | 2602.19265 | Khodakarami — spectral bias analysis | ABS | spectral bias is dynamical → 2nd-order opt + spectral loss |
| 18 | 2206.14862 | Farhani — momentum vs spectral bias | ABS | momentum/Adam + width reduce high-freq bias |
| 19 | 2412.05994 | Kang — Physics-Informed Gaussians (PIG) | ABS | learnable Gaussian features for sharp gradients, fewer points |
| 20 | 2505.10949 | Xu — FP64 is all you need | ABS | FP32 L-BFGS precision stalls → FP64 (cheap check first) |
| 21 | 2501.17281 | Seiler — stiff transfer learning | ABS | stiffness → train low-stiff, transfer to high-stiff |
| 22 | 2609.13171 | Koyamada — derivative-fidelity failure | ABS | good values ≠ good derivatives → validate autodiff derivatives (QA for flux/HRR) |

## Noted / skim (not counted toward quota)
2408.09446 (P²INN param-space extrapolation); 2604.00029 (UM-PINN uncertainty-modulated weighting);
2409.01536 (causal adaptive sampling); 2609.36615 (Volterra causal CI-PINN).

## Consolidated implications → model set
- Fire-physics forward models ([1]–[3]) ground B-01/B-05 and the smoke-vs-steam + flame-vs-nuisance features.
- Spread literature ([4]–[13]) supports keeping Rothermel (EF-11) + level-set/CA as a Class-C OFFLINE
  simulator with DA/UQ — NOT a live on-device model.
- The PINN failure-mode catalogue ([14]–[22]) is the EVIDENCE for model_set_decision's rejection of a live
  on-device fire-PINN and for entering physics as features/priors/consistency checks + an offline simulator.

## Tally
P7 NEW quota = **22** (≥15 ✓; aim ~30 → 22 solid + 4 noted = 26, honest convergence; arXiv-only, web_search
down). Body-level NEW reads this phase = 6 (5 FT + 1 FT-PARTIAL). Running body-level NEW reads: P1 15 + P2 18
+ P3 43 + P4 15 + P5 2 + P6 1 + P7 6 = **100**.

---

## P14 section — META-FUSION quota (WS1b) — 22 NEW primary arXiv (reader 41253dff; 10 fetches)
HONEST: all ABS; IDs/years arXiv-ID-derived + subagent-reported, NOT re-fetched (residual risk, §0.5); all
numbers SOURCE-REPORTED (Rule 16). These back ws1_physics/{fusion_design, ablation_plan}.md + P14 SOTA scan.
Running body-level deep FT NEW total UNCHANGED at 100 (ABS breadth).

### T1 multi-sensor/multi-model fusion (DST / Kalman / MoE)
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2508.08075 | FNBT open-world DST | fuse models over DIFFERENT frames of discernment; full-negation mass transform; proves conflict elimination, resolves Zadeh. Fuse heterogeneous physics/vision/IoT whose hypothesis spaces differ. |
| 2112.03044 | Distance-decay IoU + weighted DST | decision-level fusion of optical+SAR detectors, no paired training; +20.13% AP over optical-only. Score/decision-level evidence fusion template. |
| 2509.25452 | Kalman late fusion (camera+LiDAR) | recursive-Bayesian late fusion; up to 70% longitudinal-error reduction, robust to intermittent/degraded streams. Marginalizes a dropped IoT stream. |
| 2410.09570 | GETS: ensemble temperature scaling (GNN MoE) | input+model ensemble temperature scaling in a graph MoE; ~25% ECE reduction across 10 benchmarks, fewer params. MoE gating + post-hoc calibration layer. |

### T2 uncertainty-aware gating & abstention
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2104.08236 | Controlled-abstention NN | abstention loss + PID controller targets a user-set abstain fraction ("forecasts of opportunity"); beats post-hoc UQ on climate regression. Controllable abstain knob for a safety-critical scorer. |
| 2502.18050 | HUQ-2 selective prediction | hybrid UQ for selective prediction; reported SOTA reliability/selective-prediction tradeoff. UQ-driven abstention gate for fused scores. |
| 2601.01008 | Agentic uncertainty+abstention (stroke imaging) | perception+UQ+decision agents, threshold-based abstain + visual explanation; design-principles (no new accuracy benchmark). Architectural blueprint for threshold abstention + explanation. |

### T3 conformal prediction
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2307.16895 | Conformal PID control | online conformal scores adapted to seasonality/trend/shift via PID; improved coverage vs CDC ensemble forecaster. Distribution-free coverage ON TOP of any fuser under drift. |
| 2609.38196 | CAGE conformal adversarial ensemble | conformal p-values dynamically reweight ensemble members, down-weighting unreliable ones; beats traditional ensembles on outliers/noise. Conformal-driven model weighting + bad-detector suppression. |
| 2202.08756 | EnCQR ensemble conformalized QR | bootstrap-ensemble quantile regression, distribution-free valid intervals w/o exchangeability for non-stationary series. Per-source calibrated intervals before fusion. |

### T4 deep ensembles & calibration
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2101.05397 | Should ensemble members be calibrated? | PROVES calibrated members ≠ calibrated ensemble, and ensemble ≤ avg of calibrated members. ⇒ CALIBRATE THE FUSED OUTPUT. Core design constraint. |
| 2501.10089 | Classifier ensemble for calibration | metamodel/stacking ensemble consistently cuts ECE/MCE, fewer params, no separate calibration set. Learned stacking = strong calibrator. |

### T5 correlated & missing models/inputs
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2309.15529 | Missing-modality tri-modal fusion | bi-modal transformer modules + multivariate losses robust to modalities missing at inference (MIMIC). Degrades gracefully when a stream is absent. |
| 2605.12517 | LIM text-only VLM calibration | dropping a modality causes big accuracy drop AND severe MISCALIBRATION; latent completion (no pixel synthesis) recovers both. Missing input breaks CALIBRATION → per-availability recalibration. |
| 2103.00883 | Secure sensor fusion under attack | redundant same-variable sensors → bounded-error robust estimate independent of attack + attack isolation. The correlated/duplicated-input + adversarial case. |

### T6 anomaly + supervised score fusion
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2212.05478 | Mul-GAD multi-view graph anomaly | view-level + feature-level fusion with learned per-view weights; beats SOTA on 5 datasets. Blend anomaly-score channels with learned weights, not naive concat. |
| 2105.07346 | Bias in deep anomaly detection | bounds "relative scoring bias" when adding labeled anomalies; first finite-sample rates; characterizes when labeled-anomaly fusion helps vs hurts. Fuse only after bounding scoring bias; optimize recall@fixed-FPR. |

### T7 proper scoring rules
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2203.07835 | Proper calibration errors | relates calibration error to a proper score, upper bound with optimal estimation; common ECE estimators biased/inconsistent. Statistically sound calibration MEASUREMENT. |
| 2408.02841 | Evaluating posteriors via PSR | argues expected proper scoring rules (not ECE) assess posterior quality; calibration loss as diagnostic only. Evaluation discipline for WS1b. |
| 2609.04988 | Strictly-proper scoring for stochastic simulators | strict-propriety theory for calibrating stochastic PHYSICS models; ENERGY SCORE best held-out distributional prediction. Calibrate physics fire-spread sims with a proper score. |

### T8 safety-critical fusion
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2207.14024 | InterFuser interpretable sensor fusion | transformer fuses multi-view sensors + unknown-object detection, interpretable intermediate features constrain to safe sets; #1 CARLA leaderboard. Safety-critical fusion surfacing interpretable evidence; "unknown object" ≈ unseen fire signature. |
| 2108.05422 | Deep PET/CT DST fusion | single-modality UNets + evidential DST fusion layer + concordance loss; Dice 0.726. End-to-end differentiable evidential fusion layer template (vision+physics with explicit uncertainty). |

### Synthesis (P14) — see fusion_design.md for the full design derivation
1. CORRELATED/MISSING: open-world DST (2508.08075), evidential layers (2108.05422/2112.03044), Kalman late
   fusion (2509.25452), redundancy robust estimation (2103.00883), missing-modality robustness (2309.15529)
   + latent completion (2605.12517); correlated members must be calibrated AT THE FUSED output (2101.05397).
2. CALIBRATION/ABSTENTION: stacking/MoE calibrators (2501.10089, 2410.09570); latent completion under missing
   (2605.12517); online conformal (2307.16895) + EnCQR (2202.08756); abstention via PID budget (2104.08236),
   HUQ-2 (2502.18050), agentic thresholds (2601.01008).
3. ANOMALY+SUPERVISED: learned multi-view weights (2212.05478); conformal reweighting (2609.38196); bound
   scoring bias before fusing labeled anomalies (2105.07346); convert to a COMMON CALIBRATED SCALE first.
4. PROPER SCORING: use proper scores not ECE (2408.02841, 2203.07835); energy score for physics sims
   (2609.04988); every proper score decomposes into calibration + refinement.

## Tally (P14)
P14 NEW quota = 22 primary arXiv (≥15 MET; the stretch ~40 not required for P14). Depth all ABS (0 FT) —
running body-level deep FT NEW total UNCHANGED at 100.
