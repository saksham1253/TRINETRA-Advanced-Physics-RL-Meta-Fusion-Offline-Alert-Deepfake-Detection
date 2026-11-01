# CH07 — PERCEPTION MODULES (detector, zero-shot, temporal validator, media check, EO heads)

**Simple me samjho:** ye system ki "aankhein" hain. Har aankh sirf ek raay deti hai (probability + uncertainty), faisla nahi. Faisla fusion aur insaan karte hain.

| Module | Kya karta hai | Model / prompts | Key threshold / HP (code) | Kaise chuna (no test data) | Kahan fail | Stress test | Ladder |
|---|---|---|---|---|---|---|---|
| Fire CNN | frame or clip → [fire, smoke] probability | FireSmokeNet: 4 conv blocks (base 32) → GRU 128 → 2 logits; Strouhal aux weight 0 | lr 3e-4, wd 1e-4, 64/GPU, 20 epochs, 5 group folds, AMP | library/repo defaults; seeds 0,1,2 | steam, fog, tiny distant smoke, night | weather, small flames, Intel scenes, FireSense video | C2 |
| Colour baseline | independent bar the CNN must beat | 8-bin RGB histogram + "fire colour" stats → numpy logistic | same group folds | — | red objects, sunsets | same | C2 |
| Zero-shot CLIP | text-prompt similarity, no training | open_clip ViT-B-32 laion2b; 6 templates × fire / smoke / none (12 confuser prompts) | trust cap r ≤ 0.5; cross-fit temperature | design doc D-011 (low-weight complement) | smoke vs steam/fog (paper reports), compression | same stress sets | C2 |
| Temporal validator | alarm only if confidence persists | sliding window | window 5, min 3 frames, conf 0.5 | design | slow-growing smoke (late) | FireSense raw vs validated | C2 |
| Media check | real vs AI-generated | AuthenticityNet: RGB + FFT two-stream | max reliability 0.4; in fusion lowers media trust r(1 − p_fake) | Rule 19 (never gates a life-safety alert) | unseen generators, 32 px loses artefacts | StyleGAN faces + AI art held-out | C2 |
| EO heads | Sentinel-2 landslide, Sentinel-1 flood, InSAR deformation | frozen timm resnet18 + MLP; in_chans from data (14 / 2 / 3) | patch label = mask fraction > 0.001 (L4S) / 0.05 (S1) | adapter defaults | clouds (S2), speckle (S1), atmosphere fringes (InSAR) | Bolivia held-out (S1) | C2 |

**Three-layer note on thresholds:** a threshold is like doorbell sensitivity. Too sensitive and it rings for the wind (false alarm); too dull and
you miss the visitor (missed fire). We do not tune thresholds on test data: the calibrated probability goes to fusion, and the cost-loss rule decides (CH08).

**Worked example (zero-shot):** prompts give softmax over [fire, smoke, none] = [0.30, 0.25, 0.45]. With target "any", p = 0.55. After a fitted
temperature T = 2 (example value), logit(0.55) = 0.20, divided by 2 gives 0.10, so p_cal = 0.525. *Hand-computed example, not a result.*

**Common galti:** zero-shot ko primary detector bana dena; repo design (D-011) sirf complement allow karta hai.
**Self-check:** (1) Media check fire risk badha sakta hai? (Nahi, sirf media evidence ka bharosa ghatata hai.) (2) Candle images par training kyun nahi?
(3) Vision ke numbers kahan hain? (Kaggle runs pending; results/RESULTS.md.)
<!-- END -->
