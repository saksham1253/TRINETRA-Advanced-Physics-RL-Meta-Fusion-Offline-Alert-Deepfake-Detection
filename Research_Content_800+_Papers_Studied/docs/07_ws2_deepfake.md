# 07 — WS2: Media Authenticity (Deepfake / Misinformation) — the lowest-trust signal in TRINETRA

> **Doc-frame workstream WS2** (user frame) == internal artifact workstream **WS2** (phase **P11**) ==
> code packages `trinetra/src/trinetra/ws2_deepfake/` + `trinetra/src/trinetra/deep/deepfake_net.py`
> (`_CANON.md §3`). This chapter is the single place the handover explains why TRINETRA scores the
> *authenticity* of social-media-sourced media, how little it trusts that score, and exactly how the score
> is wired into the fusion/decision path so it can never raise a public alarm on its own.
>
> **Honesty posture (read before any number).** Nothing in WS2 was trained, downloaded, or measured. The
> numpy fallback runs and is unit-tested; the PyTorch detector is `py_compile`-clean only and was **never
> run on a GPU** here (`_CANON.md §2`). Every accuracy figure below is **source-reported from someone
> else's paper on their own data** and is tagged as such. Where you would expect a TRINETRA result, the
> honest answer is **"not measured."** Claims carry `[CONFIRMED]` / `[LIKELY]` / `[HYPOTHESIS]` /
> `[INFEASIBLE]` per `_CANON.md §1`; `[ABS]` marks an abstract-only read that may not be stated as fact.

---

## 7.1 Problem statement — why a disaster pipeline must score media authenticity, and what the score is *for*

A rapid-onset mountain-hazard response pipeline (landslide, flash-flood, cloudburst, GLOF, fire; `00 §0.6`)
cannot ignore social media, because during a disaster the public posts the earliest and most spatially dense
observations — a phone clip of a swollen river, a photo of a slope scarp, a "dam burst" video forwarded on
WhatsApp. These crowd-sourced items are a genuine *lead* channel. But they are also the channel most easily
corrupted: by AI-generated fakes, by tampered CCTV, and — the dominant real threat during real events — by
**out-of-context recycling** of *authentic* media from a different place or time (old flood footage captioned
as today's). Crisis-informatics field evidence confirms misinformation spreads fastest on exactly the
closed messaging platforms (WhatsApp/Messenger) people turn to in an emergency, and that trust flows through
*known intermediaries* and *cross-platform verification*, not raw broadcast [ABS, arXiv 2007.05848,
`#Verificado19S` Mexico 2017 earthquake]. So the pipeline needs a way to attach a *credibility* number to a
media-sourced report — not to censor, but to weight it correctly before it influences anything.

**What the authenticity score is — and is not.** WS2 produces a soft `p_fake` ∈ [0,1] (probability the media
is manipulated), which is converted into a **low-trust advisory expert** that enters meta-fusion with a small
reliability weight. It is **not** a detector verdict, **not** a filter that deletes posts, and **not** a
trigger. Its only job is to *corroborate or suppress the confidence* attached to media-sourced reports
(`deepfake_net.py` docstring: "It only corroborates/suppresses the confidence attached to media-sourced
reports"). [CONFIRMED — from the code's own contract.]

**Precisely how the output is used (the load-bearing design rule).** The score becomes one `ExpertOutput`
among many in the single decision function `decide()` (`ws5_fusion_rl`). Three guarantees bound it:

1. **It is the least-trusted input.** The fusion adapter hard-caps its reliability at **0.40** (`adapters.py`
   `_POLICY["deepfake"] = (0.30 default, 0.40 cap, Class DATA)`), so even a confident `p_fake` carries at
   most 40% of a fully-trusted expert's weight. [CONFIRMED — code.]
2. **It can never gate a life-safety alert.** Safety **Rule 19** (`_CANON.md §5`): all outputs are advisory,
   human-in-the-loop, fail-safe to "uncertain/offline"; a deepfake/social signal is explicitly *low-trust
   advisory only, must be corroborated* (`_CANON.md §6`). The autonomous-alert threshold is effectively
   unreachable from social media alone (`system_design.md §4`). [CONFIRMED — canon + source design.]
3. **Corroboration, not the detector, is the real trust signal.** The strongest input for a life-safety call
   is independent, non-social agreement — CCTV (WS4), IoT alarms (WS7), satellite active-fire (VIIRS/MODIS),
   weather (`system_design.md §7`). The authenticity score only modulates how much a *media* report adds on
   top of that. [CONFIRMED — source design.]

The operator UI therefore shows the authenticity score as an **evidence item in a trust tier**, with a review
queue, never as an automatic action (`system_design.md §9`, `§5` → P13 dashboard).

---

## 7.2 Literature landscape (real arXiv IDs from the project sources)

Two source tiers feed this chapter, and the handover must keep their verification depth distinct:

- **Promoted / cross-workstream references** (in `REFERENCES.md`, `analysis/03_paper_notes/`, `FINAL_REPORT.md`),
  read at `FT-PARTIAL` or better.
- **The P11 reading map** (`ws2_deepfake/literature_map.md`): 20 primary arXiv papers, **all `[ABS]` depth**,
  with IDs/years **arXiv-ID-derived + subagent-reported, NOT independently re-fetched** (a disclosed residual
  risk per `_CANON.md §7` / `§0.5`). Treat every number from this map as **source-reported and
  abstract-only** — perishable, and not independently verified by us. [CONFIRMED that this is the disclosed
  status; the underlying paper numbers are `[ABS]`.]

**Forensic / provenance detectors.**
- *Interpretable forensic + temporal.* arXiv **2610.03380** [FT-PARTIAL] extracts explicit named per-frame
  features (photometric 18 vars, textural 24, geometric 14, compression 12) and models their temporal
  evolution with an LSTM. For a life-safety decision an **auditable, feature-based** flag is far more
  defensible than a black box (Rule 19: a human reviewer can see *why* a clip was flagged). Its reported F1
  figures (e.g. 98.0% FF++, 91.0% Celeb-DF v2) are on **classic, not frontier**, benchmarks [ABS, via
  `literature_map`]. [CONFIRMED this is the project's design takeaway; the F1 numbers are source-reported.]
- *Content provenance (C2PA soft bindings).* arXiv **2610.04151** [FT-PARTIAL] benchmarks watermark +
  fingerprint recovery of a stripped manifest. Key cautions carried into our design: every TrustMark variant
  **false-fired on 5.9–15.3% of UNMARKED images**; copy-detectors reached ≤75.5% at FMR 1e-7; the
  watermark+fingerprint union still covered only ~69% of attacked image copies; and colour conversion changed
  watermark bits **between x86 and ARM hosts** — directly relevant to our ARM edge nodes. The doctrine:
  provenance *present + valid* raises confidence, provenance *absent* proves nothing, and a bare watermark hit
  is never a sole gate [ABS/author-abstract claims]. [CONFIRMED as our provenance doctrine.]

**The two-stream RGB + FFT approach (what the code implements).** The implemented detector pairs a spatial
(RGB) stream with a **frequency** stream built from the 2D-FFT log-magnitude, because up-sampling/GAN and
diffusion generators leave periodic **spectral fingerprints** that are often invisible in pixel space
(`deepfake_net.py`: "which exposes GAN/upsampling fingerprints"). The P11 map's cross-generator synthesis
finds frequency/steganalysis fingerprints + cross-domain alignment *generalize better* than pure spatial cues
(e.g. MoDA arXiv **2610.11496**, reported 81.9% unseen-commercial, robust under attack) [ABS]. This is the
evidence behind choosing a two-stream rather than RGB-only design. [CONFIRMED as the design rationale.]

**Adversarial robustness and the co-evolution problem (the central caveat).** arXiv **2003.01279**
("Disrupting Deepfakes") shows class-transferable adversarial attacks against facial-manipulation systems and
adversarial training for GANs, and critically that a blur defense is defeated by a spread-spectrum attack —
i.e. **defenses and evasions co-evolve**, so any one-time hardening is temporary and **continuous
red-teaming** is required (`FINAL_REPORT.md §1 WS2`; `ws6_robustness/literature_map.md`;
`DEPLOYMENT/responsible_release.md`). This is why TRINETRA treats forensic/provenance detectors as
**defensive-only** and does **not** release generation tooling. [CONFIRMED — carried verbatim across canon
and source artifacts.]

**The generalization wall (why the detector is weak exactly where it matters).** The P11 map's governing
finding: against **frontier** generators, SOTA detectors *and* humans/MLLMs fall to near chance — DF26
(arXiv **2609.07369**, humans and detectors near chance), SLED-1400 (arXiv **2606.07613**, MLLM 5.9% detection
on best generators), and most sharply for us, **CCDF** (arXiv **2610.07939**): fabricated surveillance/CCTV
crime-and-accident footage built *because* such fakes "misdirect emergency response", where 10 SOTA detectors
do not reliably separate fake from real [all ABS]. The crisis-video anchor the P11 brief leans on, RA-Bench
(arXiv **2608.14391**, reported in `literature_brief.md` only), states that *none* of three detector families
generalizes and that social dissemination makes detection *harder* [ABS, subagent-reported — not in the
20-paper map table, lower provenance]. **Provenance is just as fragile**: blind watermark removal (arXiv
**2610.11290**, reported 94.8% across 11 systems), latent-frequency masking of diffusion watermarks (arXiv
**2610.02010**), query-free audio watermark removal (arXiv **2609.34003**, DeMark) [all ABS]. And **recycled
out-of-context** real media — the dominant disaster threat — is handled by reverse-search / claim-vs-context
checks, not a fakery classifier (MIC arXiv **2609.33441**; NepOOC bilingual arXiv **2608.19212**; WildFakeBench
arXiv **2603.25423**) [ABS]. A **physics-grounded** verification precedent exists (PIVOT, arXiv **2609.15562**,
reported ~64–66% on real+frontier-generator sets, beating a strong MLLM's ~54–57% direct inspection) but with
*modest* absolute accuracy and no fire specificity [ABS].

**Net landscape conclusion (the project's, carried here):** media forensics is **one weak signal**; the
system's real reliability comes from multi-source corroboration + human-in-the-loop under an explicit cost
matrix, not from any detector's accuracy (`system_design.md §1`, `literature_map.md` governing consequence).
[CONFIRMED as the source conclusion.]

---

## 7.3 The implemented model — `AuthenticityNet`, layer by layer, and how it reaches fusion

Source of truth: `trinetra/src/trinetra/deep/deepfake_net.py` (Model 5; 49 LOC per `CODE_INVENTORY.md`) and
its numpy sibling `trinetra/src/trinetra/ws2_deepfake/__init__.py`. **Status:** `deep/` is `py_compile`-clean
and was NOT run on a GPU here; the numpy fallback runs and is covered by the 128-test suite. [CONFIRMED —
`_CANON.md §2`.]

### 7.3.1 Configuration
```python
@dataclass
class DeepfakeConfig:
    in_ch: int = 3
    base: int = 32
    max_reliability: float = 0.4   # hard cap on trust surfaced to fusion (Rule 19)
```
`max_reliability = 0.4` is the trust cap written into the model config itself — the same 0.4 enforced again
downstream in the fusion adapter (defense in depth). [CONFIRMED — code; matches `_CANON` "deepfake expert
reliability cap ≈ 0.4".]

### 7.3.2 The frequency transform
```python
def _fft_logmag(x):
    f = torch.fft.fft2(x, norm="ortho")
    mag = torch.log1p(torch.abs(torch.fft.fftshift(f, dim=(-2, -1))))
    return mag
```
Per-channel orthonormal 2D FFT → shift zero-frequency to centre → `log1p(|·|)` log-magnitude. This is the
*frequency-domain fingerprint stream*: generator up-sampling artifacts show up as periodic spectral peaks that
survive even when the RGB image looks clean. [CONFIRMED — code.]

### 7.3.3 One stream (used twice, independently, for RGB and for FFT)
```python
class _Stream(nn.Module):
    net = Sequential(
        ConvBNAct(in_ch, base),   MaxPool2d(2),     # ConvBNAct = Conv2d(3x3,s1,p1,bias=False)+BatchNorm2d+SiLU
        ConvBNAct(base, base*2),  MaxPool2d(2),
        ConvBNAct(base*2, base*4), AdaptiveAvgPool2d(1))
    out_dim = base*4              # = 128 with base=32
```
A small 3-block conv tower (channels 32 → 64 → 128), each block being `ConvBNAct` (a 3×3 Conv2d with no bias,
BatchNorm2d, SiLU; from `deep/layers.py`), with 2× max-pooling between the first two blocks and a global
adaptive average-pool to a 1×1 spatial map at the end. Output is a flattened **128-d** embedding per stream.
[CONFIRMED — code.]

### 7.3.4 The two-stream network and head
```python
class AuthenticityNet(nn.Module):
    self.spatial = _Stream(cfg.in_ch, cfg.base)       # RGB stream
    self.freq    = _Stream(cfg.in_ch, cfg.base)       # FFT-log-magnitude stream
    self.head    = Sequential(
        Linear(128+128, 128), SiLU(), Dropout(0.3), Linear(128, 1))

    def forward(self, x):                 # x: (B, C, H, W) in [0,1]
        s  = self.spatial(x)
        fr = self.freq(_fft_logmag(x))
        logit  = self.head(torch.cat([s, fr], dim=1))
        p_fake = torch.sigmoid(logit).squeeze(-1)
        return {"logit": ..., "p_fake": p_fake}

    def loss(self, out, is_fake_targets):
        return F.binary_cross_entropy_with_logits(out["logit"], is_fake_targets.float())
```
The two 128-d embeddings are concatenated (256-d), passed through a `Linear(256→128) → SiLU → Dropout(0.3) →
Linear(128→1)` head to a single **logit**, and a sigmoid yields **`p_fake`** — the probability the media is
*manipulated*. Training signal is `binary_cross_entropy_with_logits` over the RGB + FFT streams (`MODEL_CARDS.md
§5`). **Output:** a scalar `p_fake` per item (plus the raw logit). [CONFIRMED — code.]

### 7.3.5 The numpy fallback (what actually runs here)
`ws2_deepfake/__init__.py` provides a torch-free path for the offline/edge gateway and the test suite:
- `DeepfakeDetector.score()` is a **stub that raises `MissingDependency`** — the learned detector needs torch,
  which is not installed in this environment (`_CANON.md §2`), so there is no silent fake result.
- `heuristic_authenticity(cues)` averages four transparent, clipped cues (`noise_consistency`,
  `metadata_intact`, `compression_grade`, `temporal_coherence`) into a soft authenticity probability — a
  deliberately simple, *explicitly low-trust* placeholder, not a detector.
- `authenticity_expert(cues, reliability=0.3)` wraps it: `p = p_fake = 1 - authenticity`, `source="deepfake"`,
  `u=0.5`, `c=1.0`, **`r = clip(reliability, 0.0, 0.4)`**, `cls = PhysicsClass.DATA`. [CONFIRMED — code.]

### 7.3.6 How `deep_expert` maps `p_fake` to an `ExpertOutput`
On the real inference path, a cached model score is wrapped by `ws5_fusion_rl.adapters.deep_expert()`
(torch-free, so the offline gateway needs no torch):
```python
_POLICY = { ...,
    "deepfake": (0.30, 0.40, PhysicsClass.DATA) }   # (default r, hard cap, class) — LOW trust, Rule 19

def deep_expert(source, prob, *, uncertainty=0.3, consistency=1.0, available=True, reliability=None):
    default_r, cap_r, cls = _POLICY[source]
    r = clip(reliability or default_r, 0.0, cap_r)   # enforce the trust cap
    p = clip(prob, 0.0, 1.0)
    return ExpertOutput(p=p, source=source, u=..., c=..., r=r, cls=cls, available=available)
```
The resulting `ExpertOutput` (`common/types.py`) carries: `p` = `p_fake` (calibrated probability), `source =
"deepfake"`, `u` = uncertainty, `c` = physics-consistency (NF-1), `r` = reliability/trust (NF-2, **≤ 0.40**),
`cls = PhysicsClass.DATA`. That object flows into the *single* decision function `decide()` with every other
expert. The 0.40 cap is enforced in **both** the model config and the adapter, and a unit test asserts a
confident deepfake expert "must not dominate" the fused decision (`tests/fusion/test_adapters.py`;
`tests/interfaces/test_interfaces.py` checks that faker cues raise `p_fake`). [CONFIRMED — code + tests, which
pass as part of the 128-test suite.]

---

## 7.4 Design choices and rejected alternatives (with evidence)

| Decision | Choice made | Why (evidence) | Rejected alternative |
|---|---|---|---|
| Overall role | Low-trust advisory **confidence modifier**, never a trigger | Frontier detectors + humans near chance on crisis video (DF26 2609.07369, CCDF 2610.07939, RA-Bench 2608.14391) [ABS]; Rule 19 | Deepfake score as an alert **gate** — `[INFEASIBLE]`, violates Rule 19 and the evidence |
| Trust ceiling | Reliability **hard-capped 0.40**, enforced twice | `_CANON §6` low-trust doctrine; cross-generator collapse | Trusting the detector at parity with physics/sensors |
| Feature design | **Two-stream RGB + FFT** | Frequency/steganalysis fingerprints generalize better across generators (MoDA 2610.11496) [ABS]; FFT exposes up-sampling artifacts | RGB-only CNN (overfits generator-specific pixel cues) |
| Auditability | Prefer **interpretable / explicit** forensic cues; numpy cues are transparent | A human reviewer must see *why* a clip was flagged for a life-safety call (2610.03380) | Pure black-box end-to-end detector |
| Provenance | C2PA = **positive-only** confidence modifier | Watermarks removable + false-fire 5.9–15.3% on unmarked, 69% union coverage, x86/ARM bit drift (2610.04151) [ABS] | Treating "no watermark" as evidence of fakery; watermark hit as a sole gate — `[INFEASIBLE]` |
| Dominant threat | Prioritise **out-of-context / recycled** real-media checks | Recycled authentic media is the dominant disaster threat (MIC 2609.33441, NepOOC 2608.19212, WildFakeBench 2603.25423) [ABS] | Spending all effort on synthetic-pixel forensics |
| Physics-plausibility (fire growth/flicker/plume checks) | **Default OFF**, flagged-experimental, Class-C style | Rule 21: NOVEL + UNVALIDATED for fire; wide real-fire envelopes, diffusion may fake flicker; only PIVOT (2609.15562) [ABS] supports the *general* idea at modest accuracy | Asserting physics checks work — rejected as unproven |
| Degradation handling | Assume detectors are **brittle**, lean on corroboration | Codec/re-upload flips real↔fake, metadata inflates then breaks (CCDF; audio-codec 2610.07216) [ABS] | Assuming detector robustness holds post-platform-recompression |
| Release | **Defensive-only**; no generation tooling; continuous red-team | Defenses + evasions co-evolve (2003.01279); `responsible_release.md` | One-time hardening / open-sourcing generation tooling |

[CONFIRMED that these are the project's documented choices; cited paper numbers are source-reported/ABS.]

---

## 7.5 Threat model and the continuous-red-teaming mitigation

The pipeline faces three attacker classes, each mapped to the stage it defeats and the fallback
(`robustness_plan.md §2`, `literature_map.md` syntheses 2–3):

1. **Adversarial examples / anti-forensics.** Perturbation attacks on the detector; spectral flattening,
   blur/noise injection; **laundering** (re-encode, re-upload, diffusion purification) to erase synthetic
   traces. Evidence that one-time defenses fail: blur defeated by spread-spectrum (2003.01279); audio
   detectors collapse on codec re-synthesis (2610.07216) [ABS]. *Fallback:* corroboration + human review;
   detector weight is capped regardless.
2. **Novel / frontier generators.** The generalization wall — today's detector trained on today's generators
   degrades to near chance on tomorrow's (DF26, CCDF, RA-Bench) [ABS]. The P11 brief explicitly flags all
   detector numbers as **perishable**. *Fallback:* never rely on the detector alone; corroborate externally.
3. **Provenance spoofing.** Watermark removal/forgery/collusion; C2PA manifest stripping; false-fires on
   unmarked content (2610.11290, 2610.02010, 2609.34003, 2610.04151) [ABS]. *Fallback:* provenance is
   positive-only and combined with cross-channel agreement, never a sole gate.

**Mitigation = continuous red-teaming, not a fixed defense.** Because defenses and evasions co-evolve
(2003.01279), WS2's robustness strategy is a *process*: a pre-specified degradation protocol (JPEG/HEIF and
H.264/H.265 recompression sweeps, multi-generation re-uploads, resize/crop, screenshot, filters/overlays,
metadata/C2PA strip, composed per-platform chains) plus an adversarial red-team, with every attack carried
into the P16 robustness failure-mode catalogue (`robustness_plan.md §1–§5`). The system is **designed to lean
on corroboration + human-in-the-loop rather than detector robustness** (`robustness_plan.md §4`). A separate
**misuse** threat — the forensic/provenance components could be inverted into generation tooling — is handled
by the defensive-only release policy and continuous red-teaming (`DEPLOYMENT/responsible_release.md`).
[CONFIRMED as the source mitigation strategy.]

---

## 7.6 Evaluation plan — and what we actually measured (nothing)

**Our measurement: not measured.** No WS2 detector was trained, no forensic dataset was downloaded, and no
AUC / TPR / ECE / cross-generator number was produced in this environment. The PyTorch model is
`py_compile`-clean only (`_CANON.md §2`). Every figure in §7.2/§7.4 is a **source-reported paper number** on
that paper's own data, mostly `[ABS]` and subagent-reported. [CONFIRMED.]

The **pre-registered** protocol (`evaluation_protocol.md`, written *before* any build to prevent HARKing)
specifies, as process targets, not results:
- **Metrics:** AUC + Average Precision; **TPR at a fixed low FPR (0.1% / 1%)** as the operationally
  meaningful metric; **cross-generator accuracy** as the primary generalization number; **robustness curves**
  vs compression/resize/screenshot/re-upload (never a single clean number); **calibration error (ECE)** +
  reliability diagrams (the cost-matrix decision math is invalid on uncalibrated scores); fairness across
  demographics and languages (incl. Indian/code-mixed); retrieval precision/recall for the out-of-context
  stage; ≥5 seeds + CIs for learned components.
- **Splits:** strict **cross-generator** (train on one generator family, test on a held-out/open-set
  generator), **cross-dataset** (e.g. FF++→Celeb-DF/DFDC), and a staged **degradation** pipeline. No
  person/identity shared across train/test for face data; licenses respected.
- **Banned/demoted:** pristine in-distribution AUC as a *headline* (near-saturated and misleading) — allowed
  only as a reference beside cross-generator + degraded numbers; test-set threshold tuning; generator leakage.
- **Required build-phase experiments:** ≥1 cross-generator eval; ≥1 degradation curve; ≥1 adversarial/
  anti-forensics test; ≥1 ablation of the physics-plausibility signal (**pre-registered as possibly NULL**);
  ≥1 end-to-end decision-policy study sweeping the cost matrix (`experiment_plan.md`, est. ~8–10 Kaggle
  GPU-h, all estimates).
- **Decision/calibration:** optimal trust threshold `t* = C_FP / (C_FP + C_FN)`; because `C_FN >> C_FP` for
  life safety, `t* → 0` (readily escalate to review) — but the low-confidence action is "escalate to human +
  seek corroboration", not "issue alert" (`system_design.md §4`). The cost matrix is a documented config
  parameter owned with the state DMA, not a hard-coded guess. [CONFIRMED as the planned protocol.]

---

## 7.7 Failures and limits — why this is the LOWEST-trust signal in the whole system

- **The detector is weakest exactly where it is needed most.** The crisis content that actually matters —
  AI-fabricated or tampered disaster/CCTV footage from *frontier* generators — is where SOTA detectors and
  humans fall to near chance (CCDF 2610.07939, DF26 2609.07369, RA-Bench 2608.14391) [ABS]. A detector that
  scores well on classic benchmarks tells you almost nothing about this regime.
- **High benchmark accuracy does NOT mean deployment reliability.** A reported "98% F1 on FF++" is an
  in-distribution, pristine, classic-benchmark number (2610.03380) [ABS]. It does **not** survive (a)
  unseen/frontier generators, (b) platform recompression and re-upload laundering (which can flip real↔fake,
  2610.07216) [ABS], (c) adversarial perturbation (2003.01279), or (d) the out-of-context case entirely — a
  *physically authentic* clip from the wrong place/time passes every pixel-forensic test by construction.
- **Provenance does not rescue it.** Absence of a watermark/C2PA manifest is *not* evidence of fakery, a
  watermark hit is *not* proof (5.9–15.3% false-fire on unmarked images), coverage is partial (~69% union),
  and bits even drift across x86/ARM (2610.04151) [ABS].
- **The physics-plausibility idea is unvalidated for fire.** It is a `[HYPOTHESIS]` (Rule 21: novel, not
  claimed to work), default-OFF, and may yield a null result; the only supporting prior work (PIVOT
  2609.15562) is generator-agnostic but modest and not fire-specific [ABS] (`physics_plausibility.md`).
- **Acknowledged gaps:** no fire/wildfire-specific synthetic corpus exists, and Indian-language / code-mixed
  crisis-claim verification data is a build gap (`literature_map.md`, `system_design.md §6`).
- **Consequently, by design, this is the lowest-trust input in TRINETRA:** reliability capped at 0.40 (vs
  up to 1.00 for Class-A physics), `PhysicsClass.DATA`, unit-tested to never dominate fusion, and barred by
  Rule 19 from ever gating a public alert. The system manages media uncertainty through **corroboration +
  human review**, and says so plainly. [CONFIRMED — canon, code, tests, source design.]

---

## 7.8 Reference IDs (full detail → chapter 19)

Promoted references (`REFERENCES.md`; notes in `analysis/03_paper_notes/`): **2003.01279** (Disrupting
Deepfakes — co-evolution / continuous red-teaming), **2610.03380** (interpretable forensic + LSTM),
**2610.04151** (C2PA soft-bindings benchmark), **2007.05848** (crisis-informatics misinformation,
`#Verificado19S`), **2604.24404** (public-warning broadcasts spoofable → sign CAP + auth mesh).

P11 reading map (`ws2_deepfake/literature_map.md` — all `[ABS]`, subagent-reported, not independently
re-fetched): **2608.14391** (RA-Bench, via `literature_brief.md`), **2609.07369** (DF26), **2610.07939**
(CCDF), **2610.11496** (MoDA), **2606.07613** (SLED-1400), **2609.15562** (PIVOT), **2610.11290**
(ProxyEraseAgent), **2610.02010** (latent-frequency watermark masking), **2609.34003** (DeMark),
**2609.33441** (MIC), **2608.19212** (NepOOC), **2603.25423** (WildFakeBench), **2609.36850** (GAHR/Weibo26),
**2610.10121**, **2610.07216**, **2610.06339**, **2610.10752** (audio), **2609.39066** (ATAR), **2609.33585**
(IVT-Guard), **2610.03380** (also mapped here).

All identifiers and verification status are reconciled in `19_REFERENCES_FULL.md` and
`analysis/02_paper_ledger.csv`.
