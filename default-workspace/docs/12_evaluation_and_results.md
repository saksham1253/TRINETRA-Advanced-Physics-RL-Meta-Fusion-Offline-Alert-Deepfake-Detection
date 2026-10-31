# 12 — Evaluation Protocol, Admission Gate, and Results

> **Read `_CANON.md §0` first.** This chapter documents a **protocol** and an **admission gate**, not
> outcomes. **No TRINETRA model has been trained and no dataset has been downloaded** [CONFIRMED, `_CANON.md
> §0`]. Therefore every "result" cell in this chapter is **"not measured."** Every performance figure that
> *is* a number comes from an **external paper on that paper's own data** (cited by arXiv ID) and is kept
> visibly separate from "our measurement = not measured" (Rule 16). Every "SOTA target" below is a
> **process target** — "match/approach SOTA *under our protocol*" — and is explicitly **not achieved**.

This chapter is the specification of the harness that would decide whether any future TRINETRA number is
allowed to be spoken aloud. The code it documents is real and runs today: the `eval/` package is the M0
foundation of the reference implementation, it is pure numpy, and it participates in the suite that reports
**128 tests OK** and **ALL 6 CI GATES PASSED** [CONFIRMED, `_CANON.md §2`]. What does *not* exist is any
data flowing through it. The harness is loaded, calibrated, and pointed at an empty chamber.

---

## 12.1 Why evaluation is the dominant workstream, and the one reasoning that drives everything

In the internal artifact scheme, this is **WS2 "Evaluation validity,"** described verbatim as *"the
highest-leverage workstream"* and *"the dominant cluster"* (`TRINETRA_Workstreams.md` WS2). In the user's
six-workstream doc frame it lives under **WS6 robustness/eval** (`_CANON.md §3`). It is dominant for one
reason: in a life-safety hazard model, a dishonest evaluation is more dangerous than no model, because it
manufactures confidence that gets a human to disseminate a false "all clear" or a false alarm.

The single load-bearing fact, carried from `_CANON.md §6` and not to be softened:

> **Random cross-validation overstates skill. Spatial-block CV is mandatory.** [CONFIRMED as a design
> verdict; the magnitude is source-reported, not measured by us.]

The mechanism is spatial autocorrelation. Nearby map tiles share terrain, rainfall, and antecedent
moisture, so a random split routinely places a sample and its near-twin into *both* train and test. The
model then "predicts" test points it has effectively already memorised through their neighbours, and the
reported skill is inflated. The fix is to withhold **whole spatial blocks** (zones / catchments / map
tiles) so the model is always scored on genuinely unseen terrain. The companion fix for time is a strict
**temporal holdout** (train on the past, test on the future) so no post-event information can leak backward
into a pre-event feature.

**Source-reported magnitude of the problem (NOT our result):**
- Paper arXiv **2608.12422** (abstract-level, live-verified 2026-10-05) reports terrain-susceptibility
  ROC-AUC collapsing from **naive ~0.90 to an honest 0.76 / 0.71 / 0.54 under matched spatial-CV** — the
  last value is chance. This quantifies roughly **0.15–0.35 of leakage inflation** (`analysis/07_claims_table.csv`
  C002). `[ABS]` — abstract only, not full-text-verified; may never be stated as our established fact.
- The same paper reports **five deep-learning models do NOT decisively beat a simple gradient-boosted
  baseline**, and a **3-rule decision tree wins the lake-hazard task** (`07_claims_table.csv` C003). This is
  the empirical grounding for our mandatory-baseline rule, below. `[ABS]`
- The design register adds a theoretical companion, arXiv **2610.08227**: effective sample size under
  spatial correlation is **N_eff = Θ(n²/r²)**, so a naive confidence interval *underestimates* its true
  width in proportion to the correlation range r (`analysis/07_design_changes.md` DC-01, labelled
  OVER-DETERMINED). The design consequence we adopt: block CV with a correlation-range buffer **g ≥ r**
  (variogram-estimated), and report the random-vs-block CI-width ratio as an explicit leakage number.

> **Citation note (RESOLVED — cite both):** the "random CV overstates skill" verdict is triangulated across
> two QG2-verified papers — **2608.12422** (Himalayan GLOF/landslide; the AUC-collapse numbers and the
> claims table) and **2608.22293** (2025 Palisades urban-wildfire; random CV 0.92 → block 0.75, cited in
> FINAL_REPORT) — plus the effective-sample-size theorem **2610.08227**. `_CANON §6` directs citing both;
> they are complementary second-domain confirmations, not a contradiction. This chapter leans on
> 2608.12422/2610.08227 for the hazard-domain numbers and treats 2608.22293 as the fire-domain corroboration.

---

## 12.2 Metric definitions — exact formulas pulled from the code

Every formula below is transcribed from the numpy implementation in `trinetra/src/trinetra/eval/`. None of
these are evaluated against TRINETRA data anywhere; they define *how* a future number would be computed.

### 12.2.1 The cost-loss decision model and the optimal threshold p\* [CONFIRMED from `value_score.py`]

The system is scored by a **decision-theoretic cost-loss** convention, not by accuracy or AUC, because a
base-rate-dependent metric cannot be compared across hazards (`07_design_changes.md` DC-02; source arXiv
**2510.22016** reports Total Classification Cost as the ideal criterion, STRONG). The cost table
(`value_score.py` docstring) is:

```
cost(alarm,    no event) = C_FA     (false-alarm cost)
cost(alarm,    event)    = 0        (acted; loss avoided)
cost(no alarm, event)    = C_miss   (a missed event)
cost(no alarm, no event) = 0
```

With the canonical costs **C_FA = 5** and **C_miss = 100** (`_CANON.md §4`), the Bayes-optimal alarm
threshold on forecast probability is:

```
p* = C_FA / (C_FA + C_miss)                       # value_score.p_star()
   = 5 / (5 + 100) = 5/105 ≈ 0.0476
```

That a miss costs 20× a false alarm pushes the alarm threshold *far* below 0.5 — you alarm on a ~4.8%
probability — which is exactly the asymmetry a life-safety system must encode. The alarm rule is a bare
threshold test (`alarms_from_prob`): `alarm_i = 1 iff p_pred_i ≥ p*`.

**Realized cost** of an alarm vector against outcomes (`realized_cost`):

```
E = (#false alarms) * C_FA + (#misses) * C_miss
  where #false alarms = count(a==1 & y==0),  #misses = count(a==0 & y==1)
```

**Climatology cost** — the best *constant* policy, used as the skill reference (`climatology_cost`):

```
always_alarm_cost = (1 - s) * n * C_FA           # pay C_FA on every non-event
never_alarm_cost  =       s * n * C_miss         # pay C_miss on every event
E_climate = min(always_alarm_cost, never_alarm_cost)      # s = base rate = mean(y)
```

**Value Score** (`value_score`), the primary ranking metric for model selection and for the gate:

```
VS = 1 - E_forecast / E_climate        (1 = perfect; VS ≤ 0 = no skill over climatology)
```

The function returns `{value_score, E_forecast, E_climate, p_star, n, base_rate}`. A perfect forecast has
`E_perfect = 0` in this convention. **Reporting a bare accuracy or AUC without this cost-aware score is
BLOCKED by `eval.report` (Rule 16).** `[CONFIRMED — code behaviour; no data run.]`

### 12.2.2 Precision / recall at the operating point

Precision and recall are defined **at the single operating point p\***, not swept into a curve, because the
system only ever acts at one threshold. Using the same confusion counts as `realized_cost`:

```
TP = count(a==1 & y==1)   FP = count(a==1 & y==0)
FN = count(a==0 & y==1)   TN = count(a==0 & y==0)      with a = (p_pred ≥ p*)

precision = TP / (TP + FP)         recall = TP / (TP + FN)
```

Because p\* ≈ 0.0476 is deliberately low, the expected regime is **high recall, low precision** (few
missed events, many false alarms) — which is the correct posture for a *human-in-the-loop advisory* system
(Rule 19: the model never alarms the public autonomously; a human adjudicates every alert). `[CONFIRMED as
design posture; precision/recall never measured on TRINETRA data.]` Note: the recall numerator/denominator
are standard; the `eval` package computes the cost directly and leaves precision/recall as derived
reporting quantities over the same `alarms_from_prob` vector.

### 12.2.3 False-alarms-per-camera-day

For the CCTV/edge path the operationally meaningful false-alarm rate is normalised by exposure, not by
sample count, so sites with different camera counts and uptimes are comparable:

```
FA_per_camera_day = (#false alarms) / (N_cameras * observation_days)
```

This is the metric a control-room operator actually feels (alerts per shift). It is defined here for the
template table in §12.8; **it has no measured value** — no camera stream has been processed.

### 12.2.4 Time-to-detection / lead-time

For event-anticipation we report a **lead-time distribution**, not just a final catastrophe count
(`07_design_changes.md` DC-16; source arXiv **2609.34041** warns of "hollow safety gain with no
anticipation evidence," SUPPORTED). Per true event i:

```
lead_time_i = t_event_i - t_first_alarm_i     (positive = warned early; ≤ 0 = detected late/at impact)
```

We would report the median and the full distribution, and require the policy to **beat a reactive baseline
on early detection**. `[CONFIRMED as protocol; not measured.]`

### 12.2.5 Calibration metrics [CONFIRMED from `calibration.py`]

Discrimination (AUC) says the ranking is good; **calibration says a stated "0.9" is right ~90% of the
time.** An advisory number a human trusts must be calibrated. All of the following are pure numpy.

**Reliability curve** (`reliability_curve`, default `n_bins=10`, equal-width bins over [0,1]): for each bin
return `(bin_confidence = mean predicted p, bin_accuracy = mean label y, bin_count)`.

**Expected Calibration Error** (`expected_calibration_error`):

```
ECE = Σ_bins (n_bin / N) * | acc_bin - conf_bin |
```

**Maximum Calibration Error** (`maximum_calibration_error`):

```
MCE = max over non-empty bins of | acc_bin - conf_bin |
```

**Brier score + Murphy decomposition** (`brier_decomposition`):

```
Brier = mean( (p - y)^2 )
Brier = reliability - resolution + uncertainty
  reliability = Σ (n_bin/N) (conf_bin - acc_bin)^2      (lower is better; calibration error)
  resolution  = Σ (n_bin/N) (acc_bin  - base)^2         (higher is better; discrimination)
  uncertainty = base * (1 - base)                        (base = mean(y); irreducible)
```

**Recalibrators** (fit on a held-out calibration split, never on test):
- **Isotonic / PAV** (`IsotonicCalibrator`) — nonparametric monotone recalibration via Pool-Adjacent-
  Violators: sort by predicted p, then merge adjacent blocks that violate monotonicity into their
  weighted mean until the mapping is non-decreasing. Flexible; needs more calibration data.
- **Platt scaling** (`PlattCalibrator`) — parametric `sigmoid(a·logit(p) + b)` fit by gradient descent;
  the right choice for **small** calibration sets where isotonic would overfit.

None of these are fit on real data here. `[CONFIRMED — code behaviour only.]`

### 12.2.6 Conformal coverage: marginal and per-zone

From `ws6_robust/conformal.py`. Split-conformal gives a finite-sample **marginal** coverage via an adjusted
quantile of calibration nonconformity scores:

```
k = ceil((n+1)(1-alpha)) - 1 ;  q = sorted(cal_scores)[k]       # conformal_quantile
regression interval = [point - q, point + q]                     # using q over |residuals|
realized marginal coverage = mean( lo ≤ y ≤ hi )                 # empirical_coverage
```

**Per-zone (Mondrian) coverage** (`MondrianConformal.group_coverage`) is reported *per hazard/zone*, because
good marginal coverage can hide severe miscoverage of a rare, critical class (e.g. GLOF). The code reports
realized coverage; **it never calls the bound a "guarantee"** — it holds only under exchangeability/correct
weights and is voided under concept drift (module docstring). Treatment under shift is §12.7. `[CONFIRMED —
code behaviour; coverage never measured on TRINETRA data.]`

---

## 12.3 Protocols — splits and the leakage-avoidance reasoning

From `eval/splits.py`. The governing rule: **the same video/tile/zone must never appear in two splits**;
if it does, that is a leak and the resulting number is void.

### 12.3.1 Spatial-block k-fold (`spatial_block_kfold`)
Each whole `block_id` (a spatial grouping key — zone, catchment, or grid-block) lands in **exactly one**
test fold. Blocks are shuffled (seeded) and assigned round-robin to k folds; each fold trains on the other
blocks and tests on its own. A model is therefore always tested on terrain it never saw during training.
This is the **only admissible split** for a headline number (`07_design_changes.md` DC-01, P0).

### 12.3.2 Temporal split + anti-time-leak assertion (`temporal_split`, `assert_no_time_leak`)
`temporal_split` sorts by time and trains on the earliest `train_frac` (default 0.7), tests on the rest —
no look-ahead. `assert_no_time_leak(feature_times, decision_time)` **raises `LeakageError` if any feature
timestamp is after the decision time**, catching post-event information bleeding into a pre-event feature.
This assertion is wired into CI gate **G-leak** (§12.6).

### 12.3.3 Cross-camera / cross-site and cross-dataset
Beyond block CV, the protocol requires evaluation where the *held-out unit* is a whole **camera or site**
(a model must generalise to an unseen camera, not just an unseen frame from a seen camera), and a
**cross-dataset** transfer where train and test come from different source datasets entirely. These are the
strongest leakage controls: they make "memorised the sensor" and "memorised the dataset's quirks"
impossible to mistake for skill. `[CONFIRMED as required protocol; `splits.py` provides the block/temporal
primitives, and cross-camera/cross-dataset are realised by choosing the block/group key accordingly — no
such split has been run on data.]`

**Why this matters, stated plainly:** random CV answers "can the model interpolate within terrain and time
it has seen?" — almost always yes, and almost always useless for deployment. Spatial/temporal/cross-site
CV answers "can it extrapolate to the next valley, the next monsoon, the next camera?" — which is the only
question a hazard warning actually poses.

---

## 12.4 Mandatory baselines — "does not beat baseline" is a valid, publishable verdict

From `eval/baselines.py`. **A model is admitted only if it shows a real win (§12.5) over EVERY one of these,
on spatial-CV folds, by the cost-aware Value Score.** A model that fails is reported honestly as *"does not
beat baseline"* — never quietly dropped (Rule 16; WS2 task 2; grounded in 2608.12422's finding that deep
models failed to beat a GBDT and lost to a 3-rule tree, C003 `[ABS]`).

| Baseline | Code | What it predicts | Why it is in the table |
|----------|------|------------------|------------------------|
| Base-rate / climatology | `base_rate_climatology(y_train, n_test)` | constant = training base rate | the "no information" floor; VS is defined relative to it |
| Persistence | `persistence(prev_labels)` | previous time step's label (as 0/1 prob) | a hazard model must beat "assume tomorrow = today" |
| Physics rule | `physics_rule(feature, threshold, invert)` | `feature > thr` (or `< thr`), e.g. FoS<1 ⇒ alarm | a learned model must beat a hand rule with no learning |
| Logistic (learned) | `LogisticNumpy` (L2, GD, internal standardisation) | fitted probability | a deep model must beat a cheap learned model |

The design register also names **gradient-boosted trees + a 3-rule decision tree** (2608.12422) and
**seasonal-naive** for the forecasting head (2509.18176) as mandatory where applicable (`07_design_changes.md`
DC-06; WS2 task 2). The numpy `baselines.py` ships climatology/persistence/physics-rule/logistic as the
in-core set; GBDT/decision-tree/seasonal-naive are protocol-required and would be added at build (not
present as sklearn — the sandbox has **no sklearn**, `_CANON.md §2`). `[CONFIRMED code set; GBDT not in the
numpy core.]`

---

## 12.5 The admission gate G2 — the "real win" test and ReportGuard

This is the heart of the chapter: the gate that decides whether a performance claim may exist at all.

### 12.5.1 The paired block-bootstrap real-win test (`eval/real_win.py`) [CONFIRMED]

A model "really wins" over a baseline only if the **paired cost difference is positive with its bootstrap
confidence-interval LOWER bound above zero.** The procedure (`real_win`):

1. Convert both probability vectors to alarms at p\* (`alarms_from_prob`), then compute **per-sample cost**
   for model and baseline (`_per_sample_cost`): C_FA on a false alarm, C_miss on a miss, else 0.
2. Form the paired difference `diff = cost_baseline - cost_model` (**positive ⇒ model is cheaper/better**).
3. **Reduce to equal-weight per-block means:** `block_mean_b = mean(diff over samples in block b)`. Each
   spatial block contributes **one** number, so a big block cannot dominate and spatial autocorrelation
   inside a block is absorbed. The statistic is `theta_hat = mean(block_means)`.
4. **Block bootstrap:** resample *blocks* (not samples) with replacement `n_boot=2000` times; each replicate
   is the mean of the resampled block means.
5. **BCa interval** (default, `_stats.bca_interval`): bias- and skew-corrected, using a **jackknife over
   blocks** (leave-one-block-out means) for the acceleration term. Falls back to percentile if requested.
6. **Verdict rule (honest, CI-based, no p-hacking):**

```
real_win = (ci_low > 0.0)        # the LOWER CI bound must clear zero
```

The returned dict carries `mean_cost_saving_per_sample, ci_low, ci_high, ci_level, ci_method, n_blocks,
real_win`.

**Why BCa, and why block-level.** BCa (Efron 1987; `_stats.py`) corrects for bias and skew in the bootstrap
distribution; its coverage error is **O(1/n)** versus **O(1/√n)** for the plain percentile method, so the
verdict is not fooled by a skewed distribution. Bootstrapping over **blocks** rather than samples is the
statistical twin of spatial-block CV: resampling individual, autocorrelated samples would understate the
interval width and manufacture a false "win."

**Stationary bootstrap for time** (`_stats.stationary_bootstrap_indices`, Politis & Romano 1994): for
autocorrelated *time* series, resample with **geometric-length blocks** (mean `avg_block`, restart
probability `p = 1/avg_block`, wrap-around) so temporal dependence is not destroyed by i.i.d. resampling.
This is the temporal counterpart to the spatial block bootstrap and is available for time-indexed series.
`[CONFIRMED — implemented and unit-tested; never run on TRINETRA data.]`

### 12.5.2 ReportGuard — the gate that refuses to speak (`eval/report.py`, Rule 16 / R16) [CONFIRMED]

`ReportGuard` **refuses to emit a headline metric** unless all gate conditions hold. `headline(name, value)`
raises `ReportGuardError` unless:

1. `spatial_cv is True` — "cannot report performance without spatial-CV (G2)";
2. at least one baseline verdict is attached — "cannot report performance without baseline comparisons";
3. `admit()` is True — i.e. **spatial-CV AND a real win over EVERY attached baseline**
   (`all(v["real_win"] for v in baselines)`).

Until then the guard prints, honestly, **"NOT ADMITTED — no performance may be claimed (Rule 16)."** This
realises safety rule **R16: no performance claim before the eval admission gate** (`_CANON.md §5`). Because
TRINETRA has run no data, **ReportGuard today is in exactly the NOT-ADMITTED state** — which is why this
whole chapter reports "not measured."

### 12.5.3 The honest limitation: the admission baseline is partly circular

A disclosed weakness, stated plainly as required: the classifier/anomaly **admission baseline is somewhat
circular**. When the "learned baseline" is a logistic model trained on the **model's own out-of-fold (OOF)
score**, it is not an independent competitor — it is a smoothed echo of the model, so beating it is easier
than beating a truly independent method. By contrast the **geo physics_rule baseline uses real static
features** (slope, Factor-of-Safety inputs) that are genuinely independent of the model, so a real win over
*it* is more meaningful. The protocol therefore weights the independent-feature baselines (physics rule,
GBDT on raw features, persistence) as the ones that actually matter, and treats "beats a logistic-on-OOF"
as necessary-but-weak evidence. `[CONFIRMED as a documented limitation of the design.]`

---

## 12.6 The six CI gates (`scripts/ci_gates.py`) — fail-closed honesty/safety invariants [CONFIRMED]

These are **not performance tests**; they are safety/honesty invariants, each fail-closed (any failure
exits non-zero). The suite reports **ALL 6 CI GATES PASSED** (`_CANON.md §2`). Each gate and the specific
dishonesty/safety violation it blocks:

| Gate | Blocks (the violation it makes impossible) | How it checks |
|------|--------------------------------------------|---------------|
| **G-advisory** | an autonomous public alert — a CAP message built without a human approval token (Rule 19) | asserts `Config.require_human_approval() is True`; asserts `build_cap(..., approval_token=None)` raises `SafetyViolation` |
| **G-classC** | an unvalidated novel term silently going live (Rule 20) | asserts `fusion.operator.pharaoh is False` and every `firephys.nd1..nd7 is False` (Class-C default-OFF) |
| **G-security** | data exfiltration — an endpoint off the allow-list, or raw video egress (C6/C7) | asserts an empty allow-list rejects all endpoints (`EndpointNotAllowed`); asserts raw-video payload raises `SafetyViolation` |
| **G-leak** | look-ahead leakage — a feature timestamped after the decision time (G6) | asserts `assert_no_time_leak([1,2,11], decision_time=10)` raises `LeakageError` |
| **G-iot** | an over-budget radio frame | asserts `FRAME_LEN ≤ 51` bytes (LoRa budget G5) |
| **G-legacy** | a reintroduced known bug | greps `src/` for banned tokens (`EXTRA_COSBETA_ON_TRANSIENT`, `advisory = False`, `advisory=False`) and fails if any appear |

The pairing to notice: **G-leak** is the CI enforcement of the §12.3 anti-leakage protocol, and **G-advisory
/ G-legacy** encode the "advisory-only, no reverting to a dangerous default or a known bug" posture that an
honest evaluation presupposes. `[CONFIRMED — code behaviour, run in this environment.]`

---

## 12.7 Calibration under shift — why static conformal is not enough

A calibrated model on yesterday's distribution is not calibrated on a drifting one. The design register's
P0 item DC-03 requires conformal that is **action-loss-calibrated AND mask-conditional AND online** (three
independent sources: 2609.14821, 2512.14221, 2610.02777, STRONG). The deeper warning (task reference arXiv
**2101.05397**): **calibrated members do not make a calibrated ensemble** — fusing individually calibrated
models can produce a mis-calibrated whole, and **coverage collapses under drift**. The code answers with
four tools (`ws6_robust/conformal.py`):

**1. WCPS — weighted conformal for covariate shift** (`weighted_conformal_quantile`). Reweights calibration
residuals by a train→test likelihood ratio `w ≈ p_test(x)/p_train(x)` and takes the weighted (1−α)
quantile (including the test point's own weight mass at +∞, the standard construction). This keeps coverage
honest when the *input* distribution shifts but the conditional relationship holds.

**2. Adaptive Conformal Inference** (`AdaptiveConformal`, Gibbs & Candès 2021). For *arbitrary* drift it
keeps **long-run** coverage by nudging the working miss-rate online:

```
err_t   = 1 if y_t fell OUTSIDE the interval built with alpha_t, else 0
alpha_{t+1} = clip( alpha_t + gamma * (alpha_target - err_t), 0, 1 )     # gamma = learning rate
```

Read the sign carefully, as the task demands: **a miss (`err_t = 1`) makes `(alpha_target - err_t)`
negative, so `alpha_t` decreases, which **widens** the next interval** (lower α ⇒ higher required coverage
⇒ wider set). A run of good coverage lets α drift back up and the intervals tighten. The time-average
coverage → 1−α regardless of the shift. This is a genuine *type* of guarantee — **long-run, not per-step** —
and is reported as such (never oversold).

**3. Mondrian / per-hazard conformal** (`MondrianConformal`). A **separate** calibration quantile per group
(hazard/zone). Marginal coverage can hide catastrophic miscoverage of a rare class like GLOF; Mondrian-CP
gives **each hazard its own (1−α) coverage** — the honest guarantee for a multi-hazard system where every
hazard must be covered, not just the average. Unseen groups fall back to the most conservative (max)
quantile.

**4. Conformal Risk Control / RCPS slack** (`conformal_risk_threshold`, Angelopoulos et al. 2022). Instead
of an ad-hoc level multiplier, it picks the lowest alarm threshold λ whose **finite-sample-corrected**
empirical miss-rate stays within a target risk:

```
corrected = target_risk - B/(n+1)     # B = 1 (loss bounded in [0,1]); the RCPS/CRC conservative slack
λ_hat     = lowest λ on a grid with  mean( y==1 AND score<λ ) ≤ corrected
if corrected ≤ 0:  λ_hat = 0          # cannot certify ⇒ alarm on everything (fail-safe)
alarm when risk_score ≥ λ_hat         # provably bounds the MISS risk — the quantity that matters
```

This directly bounds the miss-risk — the life-safety quantity — rather than a generic coverage number.
`[CONFIRMED — all four implemented and unit-tested in numpy; none applied to TRINETRA data; coverage/risk
values are "not measured."]`

---

## 12.8 RESULTS

**There are no results.** No model has been trained, no dataset downloaded, so there is nothing to measure
(`_CANON.md §0`, `00_README_START_HERE.md §0.1`). Every result cell below is **"not measured."** This is
not a documentation gap; it is the deliberate, honest state of a life-safety project whose first-built
module is the admission gate that currently reads **NOT ADMITTED**.

What *can* be stated as `[CONFIRMED]`:
- The eval harness runs and is unit-tested (part of **128 tests OK**); **6 CI gates pass**.
- `ReportGuard.admit()` returns **False** in the current (no-data) state, so no headline metric may be
  emitted — the system is behaving exactly as the honesty contract requires.

The external numbers in this chapter (ROC-AUC 0.73/0.83/0.82; the 0.90→0.54 collapse; "deep ≯ GBDT") are
**source-reported from arXiv 2608.12422 on that paper's own data** and are `[ABS]`. They are **not SOTA we
reached**; they define the *process target* — "under our spatial-CV, cost-loss, baseline-beating protocol,
approach these" — which remains **not achieved** because nothing has been run.

### 12.8.1 Template a future run MUST fill

One row **per hazard** (landslide / flash-flood / cloudburst / GLOF — per-hazard reporting is mandatory,
WS2 task 3, source 2410.04833; **no single aggregate AUC**). Every cell must carry its honesty label and
the spatial-CV real-win verdict, or the row is withdrawn by ReportGuard.

| Hazard | Our Value Score ± BCa CI (spatial-CV) | Climatology | Persistence | Physics-rule | GBDT | Real-win vs ALL (ci_low>0?) | ECE | Marginal cov. | Per-zone cov. | FA/cam-day | Median lead-time |
|--------|---------------------------------------|-------------|-------------|--------------|------|-----------------------------|-----|---------------|---------------|------------|------------------|
| Landslide    | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured |
| Flash-flood  | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured |
| Cloudburst   | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured |
| GLOF         | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured | not measured |

Fill rules: (1) the **Value Score** column is keyed to **spatial-CV** (random-CV may appear alongside only
to expose the leakage gap, WS2 Gate G2); (2) baseline columns show each baseline's own Value Score; (3)
**Real-win** is True only if `real_win.ci_low > 0` against **every** baseline (§12.5); (4) a row where
Real-win is False is reported **"does not beat baseline"**, not deleted; (5) coverage columns report
realized Mondrian per-zone coverage, never a "guarantee."

---

## 12.9 Reference IDs → chapter 19

Resolve full citations, verification status, and read-depth labels in `19_REFERENCES_FULL.md`.

- **2608.12422** — leakage-controlled spatial-CV; AUC 0.90→0.54 collapse; deep ≯ GBDT; 3-rule tree wins.
  `[ABS]` (`07_claims_table.csv` C001–C003; WS2 task 1–2). Primary leakage evidence.
- **2610.08227** — N_eff = Θ(n²/r²) spatial-correlation theorem; CI underestimate ∝ r. `[OVER-DETERMINED]`
  (DC-01).
- **2608.22293** — cited by `_CANON.md §6` for the general "random CV overstates skill" verdict
  (**ID discrepancy flagged in §12.1**).
- **2510.22016** — Total Classification Cost as the ideal, base-rate-robust criterion. `[STRONG]` (DC-02).
- **2410.04833** — per-hazard reporting with bootstrap CIs; no single aggregate AUC. (WS2 task 3.)
- **2101.05397** — calibrated members ≠ calibrated ensemble; coverage collapse motivation.
- **2609.14821 / 2512.14221 / 2610.02777** — action-loss ≠ predictive coverage; mask-conditional CP;
  online CP under abrupt shift. `[STRONG]` (DC-03).
- **Gibbs & Candès 2021** — Adaptive Conformal Inference (ACI α-update). (`conformal.py`.)
- **Angelopoulos et al. 2022** — Conformal Risk Control / RCPS slack. (`conformal.py`.)
- **Politis & Romano 1994** — stationary bootstrap. **Efron 1987** — BCa interval. (`_stats.py`.)
- **2509.18176** — persistence + seasonal-naive forecasting baselines. **2510.10799** — linear baseline.
  **2609.34041** — anticipation/lead-time evidence (DC-16).
- RL-valuation IDs (context, chapter 10): **2110.14000** BVFT, **2311.18206** SCOPE-RL, **2312.01530**
  feedback-aware OPE (WS2 tasks 4–5).
