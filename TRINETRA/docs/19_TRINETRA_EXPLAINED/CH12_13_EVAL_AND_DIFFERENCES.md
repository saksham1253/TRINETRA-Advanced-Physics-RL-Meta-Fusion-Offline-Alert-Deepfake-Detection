# CH12 — EVALUATION AND HONESTY · CH13 — HOW TRINETRA DIFFERS

## Protocol
Group / spatial-block CV (geo: 0.1° cells, 101 blocks) · cross-dataset held-out + perceptual-hash dedupe · seeds 0, 1, 2 for vision · admission gate
(must beat climatology and a logistic baseline with a block-bootstrap CI) · ROC/PR-AUC, recall @ FPR 5%, ECE, value score (with base-rate caveat) ·
stress sets (fog, dust, candles, normal scenes, JPEG, low-res) · video raw vs validated · RL online truth + paired CI.

## Results (OUR RESULT; only from results/)
| Result | Value | Path |
|---|---|---|
| Caine physics, no fit, 184 events | ROC-AUC 0.758 | results/geo_large |
| ΔFS physics, no fit | 0.750 | results/geo_large |
| Repo geo gate (back-analysed) | 0.712 (large), 0.762 (small tile) | results/geo_large, geo_small |
| Rain logistic / physics logistic / hybrid | 0.781 / 0.773 / 0.780; hybrid ECE 0.030 | results/geo_large |
| Physics − rain AUC | −0.007 [−0.024, +0.011] (large) · +0.095 [+0.052, +0.144] (small) | both |
| Geo-PINN (trained, physics loss) | ROC-AUC 0.716, ECE 0.099; NOT admitted | results/geo_pinn |
| GLOF exponents | V–A 1.13 [0.71, 1.50] n 21 · Q–V 0.54 [0.36, 0.79] n 31 | results/glof |
| RL (simulator, C_miss 100) | learned not deployed (LCB −0.30) | results/rl_env |
| Vision (fire, zero-shot, media, EO) | RESULT PENDING | Kaggle stages |
**Published numbers** (PAPER REPORTS, abstracts): WildFireCan-MMD trained model 84.48% F1 > zero-shot VLMs; EVA-CLIP 82.0% ImageNet zero-shot.
Our numbers are on different data and protocols, so they are **not comparable**.

## Proven vs not yet (claim ladder)
C3: physics detects real landslide days; leakage-safe spatial evaluation; calibrated output on real data; RL gate refuses noise wins; soil flaw found and fixed.
Not yet: vision metrics; physics beats rain at scale; learned RL beating the physics rule at any tested miss cost; EO metrics on real S1/S2/InSAR; field trial; cyclone beyond its specification.

## CH13 — differences (summary of docs/17 and docs/18)
Typical approach categories fail in 14 documented ways (P1-P14: false alarms, late detection, single source, domain shift, no uncertainty, internet
dependence, fake media, inflated evaluation, last mile, latency, sim-to-real, human factors, drift, privacy). TRINETRA's answer to each, with a
ladder level, is in docs/18 §B and deck slides 1 and 6. **No C4 claim**: we say "what we do differently", not "we are better".

**Life-safety:** TRINETRA complements certified fire alarms and official IMD/NDMA warnings; it never replaces them; every public alert needs human approval.
<!-- END -->
