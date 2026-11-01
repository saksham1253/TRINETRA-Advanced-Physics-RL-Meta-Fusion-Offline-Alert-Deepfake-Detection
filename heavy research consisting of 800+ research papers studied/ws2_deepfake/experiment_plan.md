# ws2_deepfake/experiment_plan.md — build-phase experiment plan + compute estimates (P11, WS2)

Phase P11 · RESEARCH-ONLY (planning). MASTER_PROMPT P11 task 9. Nothing run; all GPU figures are ESTIMATES
on the shared Kaggle ≤~30 GPU-h pool (≥15% reserve). Metrics per ws2_deepfake/evaluation_protocol.md.

## Required experiments
1. CROSS-GENERATOR evaluation: train on generator set A (e.g. GAN + one diffusion), test on held-out unseen
   generators (open-set). Baselines: frequency detector + CLIP/foundation-feature detector. ~3-4 GPU-h.
2. DEGRADATION robustness curve: TPR@lowFPR vs recompression/resize/screenshot generations for the best
   detector(s), per platform chain (robustness_plan §1). ~2 GPU-h (inference-heavy).
3. ADVERSARIAL / anti-forensics test: perturbation + laundering (re-encode/regenerate) attack on the chosen
   detector; report degradation. ~2 GPU-h.
4. PHYSICS-PLAUSIBILITY ablation (physics_plausibility §4): incremental value over forensics-only on real-vs-
   synthetic fire; pre-registered as possibly NULL. ~1 GPU-h (feature extraction + simple classifier).
5. END-TO-END DECISION-POLICY study: sweep the cost matrix (C_FP/C_FN), show the trust-threshold movement
   and the corroboration/human-in-the-loop routing rates on a scripted multi-source scenario set. ~CPU +
   ~0.5 GPU-h.
6. OUT-OF-CONTEXT retrieval evaluation: reverse-search/near-duplicate/perceptual-hash + geo-temporal
   consistency precision/recall on a recycled-media set. ~CPU-bound.

## Compute summary
WS2 share ≈ 8-10 Kaggle GPU-h of the ~30 (confirm against KAGGLE_BUDGET.md); mostly inference + light heads
on frozen foundation features; checkpoint/resume per the budget plan. ALL ESTIMATES.

## Data
Free forensic datasets only for selection (DATASETS.md, [D]): image (GenImage/DiffusionForensics-type),
video/face (FaceForensics++/Celeb-DF/DFDC/DF40 — license-gated, confirm), audio (ASVspoof), out-of-context /
multimodal misinformation sets; our own recycled-media + Indian-language code-mixed claim set to be
assembled (gap). Respect all licenses; create NO deceptive media.

## Honesty
Plan only; no results. Headline metrics will be cross-generator + degraded + calibrated; pristine accuracy is
not a deliverable. The decision-policy study is where the system's real value (corroboration + human-in-the-
loop under a cost matrix) is demonstrated, not a single detector's accuracy.
