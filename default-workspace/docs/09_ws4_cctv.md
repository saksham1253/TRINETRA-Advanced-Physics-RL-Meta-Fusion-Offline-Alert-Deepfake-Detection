# 09 — WS4: CCTV Fire/Smoke Detection + Edge Features

> **Scope of this chapter.** WS4 in the user documentation frame = internal workstream WS4 (phase P8, plus
> the zero-shot complement inserted as P14Z). Code packages: `trinetra/src/trinetra/ws4_cctv/` (numpy
> interface + temporal validator) and `trinetra/src/trinetra/deep/fire_cnn.py` (PyTorch spatiotemporal
> detector). This chapter follows `_CANON.md §3` (workstream mapping), `§5` (constraint C7, Rule 16/19/20),
> and `§6` (load-bearing verdicts). Every WS4 number that could look like a measured result of ours is
> **"not measured"**: no model in this program has been trained and no dataset has been downloaded
> (`_CANON.md §0`). Paper numbers are **SOURCE-REPORTED** and carry an arXiv ID.

---

## 9.1 The problem — early fire/smoke detection on *existing* CCTV, with few false alarms

The job of WS4 is narrow and concrete: turn cameras a site **already owns** (building CCTV, roadside
cameras, a cheap River-Eye node) into an early, *advisory* fire/smoke/disaster signal that a human operator
can trust, without flooding that operator with false alarms. Three things make this hard, and WS4 is
designed around them rather than around a headline accuracy number.

1. **False-alarm fatigue is the real adversary, not raw recall.** The evaluation protocol
   (`ws4_cctv/evaluation_protocol.md §1`) pre-registers an operating point of **≤ ~1 false alarm per
   camera-day** because the literature scan found that false-alarm fatigue — not missed-detection rate —
   dominates whether operators keep a detector switched on. A detector that fires on every sunset, every
   headlight, and every steam puff is worse than useless: it trains the operator to ignore it. Every design
   choice below (temporal persistence, cross-camera corroboration, physics gating, abstention) exists to
   buy down false alarms at a fixed sensitivity.

2. **The valuable case is the hardest case.** Early, small, translucent smoke — the onset you most want to
   catch — has the lowest contrast and is the easiest to miss
   (`ws4_cctv/failure_taxonomy.md §D`). A system tuned on big, obvious, late-stage flame will look
   excellent on a benchmark and fail at the one moment that matters. WS4 therefore reports time-to-detection
   and recall **separately for early/small vs established** fire, and refuses to average them away.

3. **The hardware is cheap and the sites are unseen.** The target edge is a two-tier split
   (`ws4_cctv/model_selection.md`): a tiny always-on gate on an ESP32-CAM/OV2640 class node (INT8,
   peak-SRAM-bound, high-recall) and a stronger small-YOLO-class detector on a Raspberry-Pi/phone-class
   gateway. A model that overfits one camera's lighting and background is near-worthless when deployed to a
   new site. Hence the central protocol rule (`§9.6`): judge on **held-out cameras and held-out sites**, not
   random frame splits.

### Privacy constraint C7 — raw video stays local

`_CANON.md §5` makes C7 a hard constraint: **no raw-video egress.** Operationally this means raw frames are
**scored at the edge** (on the node or the local gateway) and only *derived* signals — a calibrated
confidence, a time-to-detection estimate, a health/tamper flag — leave the camera. The research notes
(`ws4_cctv/plan.md §9`, `failure_taxonomy.md §F`) add on-device face/person blurring and data minimisation
by default, with an explicit test requirement that **blurring must not erase the smoke/flame evidence
itself**. This is why the `ws4_cctv` interface is built so the *false-alarm-suppressing logic*
(`TemporalValidator`) is pure numpy and runs wherever the frames already are, independent of the heavy
detector. C7 is a privacy requirement *and* an architecture driver, not a bolt-on.

> **Rule 19 (`_CANON.md §5`).** WS4 is advisory and human-in-the-loop. It emits a calibrated confidence into
> the fusion/alert layer; it **never** autonomously raises a public alarm. "Uncertain / offline / abstain"
> is a valid and preferred output under degradation.

---

## 9.2 Literature landscape (real arXiv IDs, all SOURCE-REPORTED)

The P8 reading logged **41 arXiv sources** plus **16** for the zero-shot complement P14Z
(`ws4_cctv/literature_map.md`). An important honesty caveat travels with all of them: **every one was read
at ABS (abstract/title/venue) depth — 0 full texts this phase**, the arXiv API was rate-limited, and paper
identities are subagent-reported and were not each independently re-fetched. Treat the IDs and numbers below
as **source-reported, ABS-level evidence**, never as established fact and never as ours.

**Fixed-camera early smoke + canonical baselines.** SmokeyNet on FIgLib/HPWREN (**2112.08598**, a CNN+LSTM+ViT
pipeline on ~25k fixed-view smoke images) is the canonical fixed-camera early-smoke reference and supplies
both a leakage-safe (per-camera/event) split idea and a time-to-detection reference. PYRONEAR-2025
(**2402.05349**) is a real-world, multi-site camera-network early-wildfire benchmark that motivates
site/camera-grouped splits and false-alarm estimation. An image-based early-detection system
(**2211.01629**, NeurIPS'22 CCCW) sits in the same ecosystem.

**Compact / edge detectors.** OnFire compact CNNs (**2010.08833**, ShuffleNetV2-/NasNet-A-OnFire;
src-reported 95% full-frame accuracy, 49 fps on Jetson Xavier-NX) is the best-documented true low-power
baseline, though it is non-temporal and therefore optimistic against CCTV nuisances. EFA-YOLO
(**2409.12635**; src-reported **1.4M params, 22.19 ms CPU**) is our edge-detector candidate (feature F-11). A
post-detection uncertainty/confidence-refinement head on YOLOv5n/v8n over D-Fire (**2510.10108**) names NMS
as a false-alarm failure mode.

**Temporal / motion validation.** The direct basis for our temporal validator is **2607.03131**
(multi-task surveillance + temporal event validation; src-reported false-alarm **52% → 4%**, <100 ms/frame)
— require an event to persist across frames before alarming. Dynamic-texture (3-orthogonal-plane CNN,
**1703.05530**), optical-flow + Swin + uncertainty smoke segmentation (**2508.14597**), and obscured-flame
via smoke motion (**2307.00104**) round out the temporal evidence. Note **2307.00104** reports "~100% video"
classification — flagged in `FEATURES.md` as F-24 **OVERFIT RED FLAG**, carried as a caution, not evidence.

**IR / thermal (RGB fails under smoke, at night).** Unsupervised IR fire/smoke segmentation
(**1909.12937**; src-reported 95.39% frame-level, no labels) underpins feature F-16. IR+thermal fusion
penetrating heavy smoke where RGB fails (**2307.04223**; src-reported mAP@0.5 95% on Jetson Nano) underpins
the parked thermal branch F-25. Supporting thermal references: WIT-UAS (**2312.09159**), FlameVQA RGB+
radiometric thermal (**2606.27128**), FLAME aerial RGB+IR (**2012.14036**).

**Compression / low-res robustness.** Learned compression measurably changes downstream fire segmentation
(**2512.01788**); SmokeBench surveillance desmoking targets the 0–15 min early-smoke regime (**2509.12701**);
Fire360 (**2506.02167**) is a degraded-visibility robustness-collapse regime. A two-stage adaptive
compression + detection cascade (**2508.16739**, IEEE JSTARS) underpins the parked UAV feature F-26.

**Protocol / leakage evidence.** A withdrawn CCTV smoking-detection paper (**2508.11696**) is a textbook
cautionary case: the authors withdrew it over augmentation-induced leakage across splits. A multi-scene FSD
benchmark (**2410.16631**) documents that public fire/smoke datasets lack standardised construction — the
field's bottleneck. Domain-adaptation / generalisation work (**2603.02465**) and a synthetic→real gap study
(**2511.16617**) reinforce the leakage-safe discipline. The overarching CV discipline — spatial-block (not
random) CV — is `_CANON.md §6`'s load-bearing verdict (arXiv 2608.22293).

**Trained vs zero-shot in the fire domain (the decisive evidence).** In fire specifically, trained detectors
**beat** zero-shot: WildFireCan-MMD's custom model scores 84.48% f-score **>** zero-shot VLMs
(**2504.13231**); AI4Fire found **no** core zero-shot model beat trivial baselines across 5 wildfire tasks
and documented leakage/label flaws (**2610.10946**); wildfire-PM2.5 foundation models lose to a trained
BiLSTM and show heavy-tailed OOD instability, including negative R² (**2607.07951**). Zero-shot CLIP is also
empirically miscalibrated (**2303.12748**), becomes over-confident under perturbation (**2512.12997**), and
confuses the exact fine-grained classes a fire system must separate — smoke vs steam/fog/dust
(**2404.03539**). This evidence is why zero-shot is admitted **only** as a calibrated low-weight complement
(`§9.5`, D-011).

A compact illustration of the overfit trap: SegNet drone wildfire detection (**2405.00031**) reports a
compact 5-conv/2-dense model at **98.18%** accuracy *but* an 11-conv/3-dense model at only 39.31% — more
capacity did *worse*. Per `FEATURES.md`, any **>98% single-split headline is treated as an overfit
candidate, not evidence.** We cite 2405.00031 for its design lesson (compact wins; resolution is a
safety-relevant hyperparameter), not for its headline number.

---

## 9.3 The implemented model — `deep/fire_cnn.py`, layer by layer, as in code

The reference implementation is `trinetra/src/trinetra/deep/fire_cnn.py` (Model 2). It is
**[CONFIRMED] `py_compile`-clean only; it has NOT been trained on a GPU in this environment** (`_CANON.md
§2`). Everything below is the architecture *as written in code*, not a trained result.

### Config (`FireNetConfig`)
```
in_ch = 3            # RGB
base = 32            # base channel width
gru_hidden = 128     # temporal state width
n_classes = 2        # [fire, smoke] — MULTI-LABEL (sigmoid, not softmax)
strouhal_weight = 0.0   # Class-C novel flicker term -> OFF by default (Rule 20)
```
`n_classes = 2` as **multi-label** matters: fire and smoke can co-occur or occur alone, so the head uses
independent sigmoids, not a softmax over mutually exclusive classes.

### Per-frame encoder (`FrameEncoder`)
A small 2-D CNN applied to every frame independently. Each `ConvBNAct` is `Conv2d(k=3,s=1,p=1, bias=False) →
BatchNorm2d → SiLU` (`deep/layers.py`). The stack:
```
ConvBNAct(3  -> 32)   -> MaxPool2d(2)      # H/2
ConvBNAct(32 -> 64)   -> MaxPool2d(2)      # H/4
ConvBNAct(64 -> 128)  -> MaxPool2d(2)      # H/8
ConvBNAct(128-> 128)  -> AdaptiveAvgPool2d(1)   # global pool -> (B, 128, 1, 1)
```
Output `out_dim = base*4 = 128`; `forward` returns `(B, 128)` after `flatten(1)`. Three downsampling pools
then a global average pool keep it cheap and resolution-tolerant — appropriate for a gateway-class device.

### Temporal pathway + heads (`FireSmokeNet`)
Input is a **clip**, `x: (B, T, C, H, W)`. The forward pass, exactly as coded:
```
B,T,C,H,W = x.shape
feats = encoder(x.reshape(B*T, C, H, W)).reshape(B, T, 128)   # per-frame features
seq, hN = gru(feats)        # nn.GRU(128 -> gru_hidden=128), batch_first
h = hN.squeeze(0)           # last hidden state (B, 128)
logits  = head(h)           # nn.Linear(128 -> 2)  : [fire, smoke] logits
flick   = relu(flicker(h))  # nn.Linear(128 -> 1)  : flicker-frequency estimate (Hz), >= 0
return {"logits": logits, "prob": sigmoid(logits), "flicker_hz": flick}
```
So the model is **CNN encoder → GRU → {fire, smoke} multi-label logits**, plus an **auxiliary flicker-Hz
head**. The GRU is the design's core false-alarm suppressor: sun glint and headlights are single-frame
events; real fire **flickers persistently**, so a model that reads a short temporal window can separate them
in a way a single-frame classifier cannot. (The module docstring states this explicitly.)

### The Strouhal auxiliary head (Class-C, OFF by default)
`loss()` combines a standard multi-label BCE with an *optional* physics-consistency penalty:
```
bce = binary_cross_entropy_with_logits(logits, targets, pos_weight)
total = bce
if cfg.strouhal_weight > 0 and plume_size_m is not None:     # gated, Class-C
    strou = strouhal_consistency_loss(flicker_hz, plume_size_m)   # f ~ 1.5/sqrt(D)
    total = total + cfg.strouhal_weight * strou
return {"loss": total, "bce": ..., "strouhal": ...}
```
`strouhal_consistency_loss` (`deep/losses.py`) penalises deviation of the predicted flicker frequency from
the Strouhal law **f ≈ 1.5 / √D** (D = plume diameter). This is a Class-A fire relation
(`_CANON.md §4`), but using it as a *novel* flicker regulariser is treated as **Class C** and is **gated OFF
by default** (`strouhal_weight = 0.0`), honouring Rule 20 (novel terms default-OFF with an A/B fallback).
Critically, the loss term is *consistency only* — the established-physics gate (Heskestad/Byram, in
`ws1a_firephys`) still runs separately at inference; this head never *replaces* the hard gate, it only
nudges training when explicitly enabled.

### How `ws4_cctv` maps a detector confidence to an `ExpertOutput`

`ws4_cctv/__init__.py` is deliberately split from the heavy model:

- `EdgeDetector` is an **interface stub**. Its `.detect(frame)` raises `MissingDependency` because the real
  frame-level backbone (YOLO-n class) needs torch, which is not installed in this sandbox (`_CANON.md §2`).
  The validator below works on **any** detector's confidence stream, which keeps the false-alarm logic
  usable at the edge without torch.
- `TemporalValidator` is **pure numpy** and is the false-alarm suppressor realised in code:
  ```
  TemporalValidator(window=5, min_frames=3, conf_thr=0.5)
  update(frame_conf):
      buf.append(frame_conf)                               # sliding window of last `window` confidences
      support = count(c >= conf_thr in buf)
      confirmed = support >= min_frames                    # must PERSIST
      conf = mean(c for c in buf if c >= conf_thr) if support else 0.0
      return ValidatedEvent(confirmed, confidence=conf if confirmed else 0.0, support_frames=support)
  ```
  It confirms an event only when per-frame confidence stays above `conf_thr` for at least `min_frames` of the
  last `window` frames — rejecting single-frame glints, headlights, and steam puffs. This is feature F-12 in
  its minimal, numpy form (`§9.4`).

The confidence then becomes a fusion expert via `ws5_fusion_rl/adapters.deep_expert(...)`. The adapter wraps
a scalar probability into the shared `ExpertOutput` dataclass (`common/types.py`: fields `p, source, u, c, r,
cls, available`, each in [0,1]) with a **source-appropriate trust cap**. The relevant policy rows
(`adapters._POLICY`):
```
"fire_cnn": (default r = 0.80, hard cap r = 0.95, cls = DATA)
"cctv":     (default r = 0.75, hard cap r = 0.90, cls = DATA)
```
So a CCTV/fire-CNN detector enters fusion as a **Class-DATA expert with a reliability ceiling** (never
treated as hard physics, cap < 1.0), carrying its calibrated probability `p`, an uncertainty `u`, a
physics-consistency `c`, and its reliability `r`. From there it flows through the single `decide()` path in
`ws5_fusion_rl` — advisory only, Rule 19. The adapter is torch-free on purpose so the offline gateway can
assemble experts from cached scores without importing torch.

### ASCII flow: frame → detector → temporal validation → fusion
```
  CCTV / River-Eye frames (RAW VIDEO STAYS LOCAL — C7)
          |
          v
 +--------------------------+     on-device, face/person blur, data-minimised
 | per-frame CNN encoder    |     (deep/fire_cnn.py: ConvBNAct x4 + pools)
 |  (B,T,3,H,W)->(B,T,128)  |
 +--------------------------+
          |  per-frame features
          v
 +--------------------------+     temporal pathway = key false-alarm suppressor
 | GRU(128->128) -> heads   |     fire flickers PERSISTENTLY; glint/headlight = 1 frame
 |  logits{fire,smoke}      |---> flicker_hz --(Strouhal aux, Class-C, OFF)--> consistency
 +--------------------------+
          |  sigmoid prob (per-frame conf stream)
          v
 +--------------------------+     ws4_cctv.TemporalValidator (pure numpy, F-12)
 | sliding window persist   |     window=5, min_frames=3, conf_thr=0.5
 | + cross-camera corrob.   |     + pre-registered cross-camera rule (F-11/F-12/F-16)
 +--------------------------+
          |  ValidatedEvent(confirmed, confidence)
          v
 +--------------------------+     ws5_fusion_rl.adapters.deep_expert("fire_cnn"/"cctv")
 | ExpertOutput (Class DATA |     reliability CAPPED (0.90-0.95); u,c,r attached
 |  p,u,c,r; r<=cap)        |
 +--------------------------+
          |     joins physics (Heskestad/Byram gate), IoT, anomaly, zero-shot(low wt)
          v
 +--------------------------+     ws5_fusion_rl.decide()  --  ADVISORY ONLY (Rule 19)
 | meta-fusion -> Decision  |     level = max(conformal_level(risk,p*), shield_floor)
 | human operator decides   |     NEVER an autonomous public alert
 +--------------------------+
```

---

## 9.4 Edge features — F-11, F-12, F-16 (approved-for-build-plan) + parked F-25, F-26

All five are from `FEATURES.md`. All evidence is ABS-level and SOURCE-REPORTED; **none is built or tested**,
and each approved feature carries a **pre-registered cross-camera/cross-site decision rule** — a feature that
helps one benchmark but hurts cross-camera performance is **not** a win (gated via the inferential-
reproducibility test 2302.04054).

### F-11 — EFA-YOLO efficient edge detector `[approved-for-build-plan]`
- **What it does.** An attention-lite + depthwise-separable small YOLO backbone for the gateway detector —
  the main fire+smoke detector on Pi/phone-class hardware.
- **Evidence.** 2409.12635, src-reported **1.4M params, 22.19 ms CPU**.
- **Planned cost.** Low (single-GPU retrain; CPU-real-time inference).
- **Pre-registered decision rule.** Keep **only if cross-CAMERA mAP gain > seed variance** vs the current
  backbone. **Risk (explicit):** micro-architecture mAP gains often shrink cross-camera — a single-split
  overfit trap.

### F-12 — Temporal multi-frame event validation `[approved-for-build-plan]`
- **What it does.** Confidence-weighted voting + cascade filter requiring an event to **persist** before
  alarming. This is exactly what `ws4_cctv.TemporalValidator` implements in minimal numpy form, and what the
  GRU pathway in `fire_cnn.py` learns in its trained form.
- **Evidence.** 2607.03131, src-reported **false alarms 52% → 4%**, <100 ms/frame.
- **Planned cost.** Very low (post-processor, no retrain).
- **Pre-registered decision rule.** Keep if the false-alarm reduction **holds cross-site at matched
  sensitivity**. **Risk:** framerate/latency-to-alert tradeoff; it **must not raise the missed-event rate**.

### F-16 — Unsupervised IR optical-flow / flicker physics feature `[approved-for-build-plan]`
- **What it does.** A label-free classical-CV feature (optical-flow / flicker-band physics) for cold-start,
  before any labels exist — ties the Strouhal/flicker physics into a cheap on-node cue.
- **Evidence.** 1909.12937, src-reported **95.39% frame-level, no labels**.
- **Planned cost.** Very low (classical CV, no GPU/labels).
- **Pre-registered decision rule.** Keep if it **adds signal over RGB-only on cross-site video**. **Risk:**
  sensitive to framerate/codec/PTZ motion.

### Pre-registered cross-camera decision rule (shared)
Per `FEATURES.md §P17` and `ws4_cctv/evaluation_protocol.md §2`, every WS4 feature is admitted only if its
improvement **exceeds seed/trial variance on a HELD-OUT CROSS-CAMERA / CROSS-SITE split** *and* its cost is
justified. Splits are grouped by **site → camera → video** (all frames of a video in one split; whole
cameras/sites held out), with the cross-site tier as the headline. This rule is fixed **before** any build so
results cannot be shopped.

### Parked features (reasons stated)
- **F-25 — Thermal/IR fusion branch for low-visibility** `[proposed / parked]`. Evidence 2307.04223
  (src-reported mAP@0.5 95% on Jetson Nano). Low inference cost **but requires IR hardware + a calibration
  rig**. Parked because it is **gated on IR hardware availability + the ≤₹2000 node cap (C2)** and **likely
  exceeds the prototype budget**. IR fusion is the designed remedy for the night/fog/smoke-occlusion failure
  modes (`§9.7`) — but only when the hardware budget allows it. `[HYPOTHESIS]` for our deployment until BOM
  verified in P6.
- **F-26 — Two-stage UAV adaptive compression + policy early-exit** `[proposed / parked]`. Evidence
  2508.16739 (src-reported large compute cut). **High cost** — needs an RL-style policy net + orchestration.
  Parked: **defer until the core detector is validated.**

---

## 9.5 Design choices + rejected/deferred alternatives

**Chosen: two-stage cascade (tiny on-node gate → gateway detector) + temporal confirmation + physics/
cross-modal fusion.** (`ws4_cctv/model_selection.md`.) Rationale: the edge is genuinely two-tier
(ESP32-CAM is INT8-tiny-model-only; a Pi/phone-class gateway can host a real detector), and false-alarm
control is decisive. The on-node gate is tuned for **high recall** (don't miss, tolerate false positives it
passes up); the gateway detector and temporal stage buy the precision back.

**Trained detector = PRIMARY; zero-shot = LOW-WEIGHT CALIBRATED COMPLEMENT (decision D-011).**
(`ws4_cctv/zero_shot_design.md`, `_CANON.md §6`, `FINAL_REPORT.md` line 26.) The evidence that trained beats
zero-shot *in the fire domain* is specific and strong: 2504.13231 (custom 84.48% f-score > zero-shot VLMs),
2610.10946 (no core zero-shot model beat trivial baselines, documented leakage), 2607.07951 (foundation
models lose to a trained BiLSTM, negative-R² OOD tail). Zero-shot is admitted **only** for open-vocab /
unknown-hazard breadth the closed-set detector was never trained on, and only after **mandatory calibration
before fusion** (one temperature per backbone, 2303.12748; Dirichlet uncertainty, 2512.12997; feed entropy/
prob-difference, not raw softmax; de-rate external numbers for leakage up to 8.9%, 2107.13029). It enters
fusion at **low weight**, never as the primary detector.

**Rejected / deferred alternatives (with evidence):**
- **Classical cues alone (color/motion/flicker).** Cheap and interpretable but weak alone → **kept only as a
  cheap on-node gate + physics-consistency check, not standalone.**
- **DETR / transformer detector.** Strong global context but heavy → **server tier only, not an edge node.**
- **Open-vocabulary / foundation detector as the primary.** Zero-shot prompts but large and, per the fire
  evidence above, weaker than trained → **deferred to the P14Z low-weight complement.**
- **Zero-shot as the detector.** Rejected by D-011 on the fire-domain evidence + miscalibration.
- **Anomaly/one-class on video as the detector.** Not a detector; **handed to WS8** as the explicit target
  for the supervised detector's blind spots.
- **Over-deep CNNs.** 2405.00031 shows an 11-conv/3-dense model *underperforming* a compact 5-conv/2-dense
  one — capacity is not free; `fire_cnn.py` is deliberately compact.

---

## 9.6 Evaluation — pre-registered protocol; our results = "not measured"

The protocol (`ws4_cctv/evaluation_protocol.md`) was pre-registered **before** any model was built, so
results cannot be shopped. **No WS4 detection number is measured by us** (Rule 16) — the items below are the
*bar*, not claimed as met.

- **Leakage-safe splits (the central rule).** Group by **site → camera → video**; all frames of a video stay
  in one split; whole cameras/sites held out. Three tiers: within-site, **cross-camera**, **cross-site**
  (cross-site is the headline). Temporal ordering where timestamps exist (test videos later than train).
  **Never** random-frame splits — the withdrawn paper 2508.11696 is the cautionary case.
- **False alarms per camera-day** at the fixed operating point (**≤ ~1/camera-day** target), measured on the
  nuisance negatives from the failure taxonomy — reported, not just recall.
- **Time-to-detection** (median + full distribution), **split by difficulty**: early/small smoke reported
  separately and honestly even when worse than established fire.
- **Calibration:** reliability diagram + ECE, so the fusion/alert layer can trust the confidence it receives
  (this is why the `ExpertOutput` reliability cap exists).
- **Robustness curves:** metric vs JPEG/H.264 bitrate, vs resolution, vs night/IR.
- **Confidence intervals over ≥5 seeds** for every headline number — report CIs, not point values.
- **Baselines & variants on identical splits/seeds:** classical cues → single-frame deep → deep+temporal →
  physics-informed → cross-modal (camera + IoT). Reproduce published YOLO-family fire/smoke baselines first.

**On citing SOTA.** Published fire/smoke numbers mostly use random (often leakage-prone) splits, so they are
**not directly comparable** to our leakage-safe numbers. When we cite SOTA we say "source-reported under
their protocol" and re-run baselines under *this* protocol for an apples-to-apples reference.

**Overfit red-flags called out.** Per `FEATURES.md`, any **>98% single-split headline is an overfit
candidate, not evidence.** Named cases: 2307.00104's "~100% video" (feature F-24) and 2405.00031's 98.18%
single-dataset accuracy. We do not carry these as performance evidence.

**Our results, stated plainly:** `[CONFIRMED]` the numpy core (incl. `ws4_cctv.TemporalValidator`) runs
inside the 128-test / 6-gate suite and `fire_cnn.py` is `py_compile`-clean; **[not measured]** any detection
mAP, recall, false-alarm rate, time-to-detection, or calibration number for TRINETRA — no training, no
dataset.

---

## 9.7 Failure modes + mitigations

From `ws4_cctv/failure_taxonomy.md` (a test-design artifact; mitigations are **design requirements**, not
performance claims). The taxonomy also notes an honest gap: dedicated camera-tamper/blinding/replay-spoofing
and privacy papers for fire CCTV were **essentially absent** in the arXiv-only search (only 2412.20006 on
prediction-model adversarial robustness) → carried as an open action for non-arXiv follow-up, with the
WS2/P11 deepfake handoff covering replay-spoofing conceptually.

| Failure mode | Why it fools a detector | Mitigation (design requirement) |
|---|---|---|
| **Night / low light** | flame visible, smoke invisible | **IR/thermal branch (F-25, budget-gated)**; different nuisances (heaters/hot sun) handled separately |
| **Fog / cloud / haze** | gray diffuse regions mimic smoke (hardest smoke nuisance) | temporal **growth** check + sky-region priors; cross-modal IoT PM sensor; abstain under low confidence |
| **Steam / water vapor** | looks like white smoke | multi-class benign-vs-dangerous smoke; extinction/color priors; temporal growth |
| **Occlusion (foliage/structures)** | partial smoke/flame | multi-view / cross-camera **persistence** (the TemporalValidator's cross-camera corroboration); obscured-flame via smoke motion (2307.00104, with its red-flag) |
| **Camera shake / PTZ** | global motion mimics plume motion | motion compensation; temporal confirmation |
| **Compression (H.264/H.265), low-res** | blocking/blur destroys smoke texture | evaluate at realistic bitrates (robustness curves, §9.6); 2512.01788 shows compression changes outcomes |
| **Camera tamper / blinding (laser/IR)** | sensor saturation, blind spot | detect saturation + scene-change; **health/tamper flag; abstain** (fail-safe, Rule 19) |
| **Replayed-video spoofing** | fake "all clear" or fake alarm | stream liveness/integrity + signed streams → **WS2 deepfake handoff (P11)** |
| **Adversarial patch** | suppress/trigger detection | robustness tests + **cross-modal voting** so vision alone can't be gamed (2412.20006) |

**IR fusion gating on hardware/budget.** IR/thermal (F-25) is the designed answer to the night/fog/smoke-
occlusion cluster — thermal penetrates heavy smoke where RGB fails (2307.04223). But it is **gated on IR
hardware availability + the ≤₹2000 node cap (C2)** and is expected to exceed the prototype budget. So in the
baseline RGB-only build, the mitigation for those modes is **abstention + cross-modal corroboration (IoT
gas/heat) + temporal/cross-camera persistence**, with IR added only where the budget and hardware allow.
Privacy (C7): on-device processing + face/person blur + data minimisation, with a test that blurring does
not erase smoke/flame evidence.

---

## 9.8 References → chapter 19

All IDs are **SOURCE-REPORTED, ABS-level** (`ws4_cctv/literature_map.md`); full detail, BibTeX, and
verification status live in `19_REFERENCES_FULL.md`, row-level truth in `analysis/02_paper_ledger.csv`.

- **Fixed-camera / early smoke:** 2112.08598 (SmokeyNet/FIgLib), 2402.05349 (PYRONEAR-2025), 2211.01629,
  2212.14143.
- **Compact / edge detectors (incl. F-11):** 2409.12635 (EFA-YOLO, F-11), 2010.08833 (OnFire), 2510.10108,
  2304.07584, 2501.08639, 2501.09926.
- **Temporal validation (incl. F-12):** 2607.03131 (F-12), 1703.05530, 2508.14597, 2307.00104 (F-24 OVERFIT
  RED FLAG), 2207.03708.
- **IR / thermal (incl. F-16, F-25):** 1909.12937 (F-16), 2307.04223 (F-25), 2312.09159, 2606.27128,
  2012.14036.
- **Compression / low-res (incl. F-26):** 2508.16739 (F-26), 2512.01788, 2509.12701, 2506.02167.
- **Protocol / leakage / generalisation:** 2410.16631, 2508.11696 (withdrawn, leakage case), 2603.02465,
  2511.16617, 2606.10174, 2604.23542, 2503.14552, 2608.22293 (spatial-block CV), 2302.04054 (inferential-
  reproducibility gate).
- **Trained-vs-zero-shot (D-011) + zero-shot calibration:** 2504.13231, 2610.10946, 2607.07951, 2303.12748,
  2512.12997, 2404.03539, 2107.13029, 2303.15389 (EVA-CLIP), 2403.15378 (Long-CLIP), 2510.02270 (microCLIP),
  2306.09269 (WinCLIP), 2501.16404 (DynaPrompt), 2512.12268 (MetaTPT), 2512.02520, 2605.01165.
- **Design-lesson / overfit example:** 2405.00031 (SegNet; 98.18% single-split = overfit red flag),
  2011.04863 (F-18), 2502.20979 (F-19), 2609.18227 (F-20/WISE).
- **Adversarial:** 2412.20006.

---

### Honesty footer
Nothing in WS4 has been trained, downloaded, or measured by TRINETRA. `fire_cnn.py` is `py_compile`-clean
only (no GPU run here); `ws4_cctv.TemporalValidator` runs within the numpy test suite. All performance
figures are source-reported from the cited papers on their own data, read at ABS depth, with identities
subagent-reported and not independently re-fetched — a disclosed residual risk (`_CANON.md §7`). `>98%`
single-split headlines are treated as overfit red flags, not evidence (`FEATURES.md`). WS4 is advisory,
human-in-the-loop, fail-safe to abstain, and never raises an autonomous public alert (Rule 19).
