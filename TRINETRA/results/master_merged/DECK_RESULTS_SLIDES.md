# TRINETRA · Phase 2 results: slide content (honest version)
All numbers: OUR RESULTS on the prototype pack. They are not comparable to full-benchmark papers.

## Slide 1 — What we measured
- 5 accounts, 61 GB pack. Fire CNN, CLIP zero-shot, CLIP few-shot probe, colour baseline, deepfake, landslide physics, GLOF, Geo-PINN, RL.
- Every learned model passes through one gate (Rule 16). It must beat climatology AND a simple baseline on cost, with a 95% block-bootstrap CI.
- **0 learned experts admitted so far.** We report this openly. The gate is the point.

## Slide 2 — Fire / smoke detection
| expert | OOF AUC | held-out AUC | note |
|---|---|---|---|
| fire_cnn (3 seeds) | 0.768 | 0.972 | small CNN, 128 px |
| CLIP zero-shot | 0.917 | 1.000 | no labels used |
| **CLIP probe** | **0.962** | 0.998 | best single expert |
| colour baseline | 0.681 | – | sanity floor |
Takeaway: frozen foundation features + a tiny probe beat the custom CNN.

## Slide 3 — Meta-fusion, done on REAL pairing
- Every expert scores the same 3410 images, so the stack is real (no synthetic pairing).
- Stack OOF AUC 0.951 vs clip_probe 0.959 (−0.008). **Fusion adds no AUC on same-image data.**
- What fusion DOES give: calibration. Held-out ECE is 0.026 for the stack vs 0.24 for fire_cnn. Value score is 0.55–0.63 for the stack vs 0.57 for clip_probe.
- Next: cross-modal (per-frame + temporal validator, confusers) → [fill from out_X_final].

## Slide 4 — Landslide (physics first)
- Caine I-D physics, **zero training**: AUC 0.758 (184 real events, 101 spatial blocks).
- Meta-fusion (rain + Caine + ΔFS + geo gate, FM-1): 0.779 ≈ rain-only 0.781. Adding Geo-PINN: 0.772.
- GLOF lake area→volume exponent b = 1.13 (95% CI 0.71–1.50, n = 21).

## Slide 5 — RL: the gate said "keep the rule"
- Physics simulator with real rainfall: CQL ≈ physics rule ≈ oracle at C_miss 100 / 1000 / 5000. Deploy False ×3.
- Fused fire stream, **held-out blocks, true reward**: CQL beats the fixed rule (+0.49/row) but not a train-tuned threshold (−0.02). **Deploy 0/3.**
- The in-sample OPE showed +1.08. We do not claim it, because it was scored on the training logs.

## Slide 6 — Deepfake + what we learned
- Deepfake OOF 0.961 → held-out (unseen generators) 0.450. It does not generalise, so it is kept as a **low-trust down-weighter** (trust cap 0.4).
- Lessons: (1) foundation features > custom CNN; (2) on one modality, fusion = calibration + trust + safety shield, not extra AUC;
  (3) learned policies must beat a *tuned* rule on *held-out* data. Ours do not yet, so the shield + rule stay in charge.
