# 01 — Executive Summary

**Audience:** anyone who needs the whole project in two pages — PM, judge, reviewer, new lead.
**Status date:** 2026-10-10. **Honesty posture:** research + reference code; nothing trained or benchmarked.

---

## 1.1 What TRINETRA is

TRINETRA (alt. **HIMKAVACH**) is an **offline-first, multi-sensor, physics-grounded, advisory early-warning
and hazard-detection system** for two problem families:

1. **Rapid-onset mountain hazards** — landslide, flash-flood, cloudburst, and glacial-lake outburst flood
   (GLOF) in the Indian Himalaya (Uttarakhand + Himachal Pradesh).
2. **Fire / disaster detection** via existing CCTV, cheap ground IoT, and free satellite Earth-observation.

It ingests free satellite data, opportunistic camera vision, and ≤₹2000 LoRa IoT nodes; runs an anomaly
stack, a physics gate, a supervised ensemble, and an offline-RL advisory policy; **fuses** them in a gated
meta-fusion head; **calibrates** the fused risk with conformal prediction; applies a deterministic monotone
**safety shield**; and emits a single **advisory alert level** (Green < Yellow < Orange < Red) to a **human
operator**, who alone decides whether to disseminate a CAP/SACHET public alert. The trust boundary from
"advisory level" to "public alert" is **never crossed without a human** (safety rule R19).

## 1.2 What was actually produced (two layers)

- **Research program** [CONFIRMED by `FINAL_REPORT.md`]: a complete, literature-grounded design across all
  workstreams, 631 unique arXiv references (FINAL_REPORT snapshot; ~775 in the live ledger — see `_CANON §7`), 128 per-paper notes, physics derivations, a dataset registry,
  a Kaggle compute plan, a failure-mode catalogue, and a 33-item hazard-correctness bug ledger with fixes.
  **Nothing was trained or measured.**
- **Reference code** [CONFIRMED by running it]: `trinetra/` — a pure-numpy core (physics gates, fusion,
  conformal calibration, decision/shield, eval harness) that **passes 128 unit tests and 6 CI gates**; a
  PyTorch `deep/` layer with 6 trainable models + fusion heads (**compile-verified, not GPU-trained here**);
  and Kaggle training scripts (**multi-GPU T4×2 ready, not executed on a GPU here**).

## 1.3 Results posture — read this before quoting any number

There are **no TRINETRA performance results**, by design. The only numbers we measured are *engineering*
facts about the code:

| Our measurement | Value | How |
|-----------------|-------|-----|
| numpy-core unit tests | **128 pass** [CONFIRMED] | `python run_tests.py` → `OK` |
| CI honesty/safety gates | **6/6 pass** [CONFIRMED] | `python scripts/ci_gates.py` |
| deep + Kaggle scripts | **compile-clean** [CONFIRMED] | `py_compile`; not run on GPU |
| source size | ~3362 LOC src, ~917 LOC tests | `CODE_INVENTORY.md` |

Every *domain* number (detection mAP, false-alarm reduction, calibration coverage, drift-MSE reduction,
edge latency, BOM ₹) that appears anywhere in this project is **source-reported** from a cited paper on its
own data (safety rule R16), or is a **planning estimate** flagged `[EST]`. The chapter-12 "SOTA target"
table lists these as *process targets* ("match/approach under our protocol"), never as achieved results.

## 1.4 The headline verdicts (do not soften)

- **IP-address-based alerting is `[INFEASIBLE]`** for life-safety targeting. Consumer IP geolocation is only
  ISP/city-accurate (often tens of km), is corrupted by CGNAT/VPN/DHCP, maps to no premises, and cannot
  address a person at risk. It was **considered and rejected**. Public-IP exposure is handled instead as a
  *security* concern (authenticated endpoints). (Chapter 08.)
- **A full fire-PINN as a deployed on-device solver is `[INFEASIBLE]` now** (stiffness, spectral bias,
  non-identifiability). Physics enters as *soft features / priors / consistency-checks* with a Class-A
  fallback — not as a live solver. (Chapters 05–06.)
- **Autonomous public alerting without certification/authority is `[INFEASIBLE]`.** The system is advisory,
  human-in-the-loop, and fails safe to "uncertain/offline" (R19).
- **Random cross-validation overstates skill** → **spatial-block CV is mandatory** and gates every claim
  (admission gate G2; arXiv 2608.12422 — naive ~0.90 ROC-AUC collapses under matched spatial-CV). (Chapter 12.)
- Deepfake / zero-shot / social-media signals are **low-trust advisory only** and must be corroborated.

## 1.5 What is genuinely strong about the design

- **Honesty engineered into the code, not just the prose:** a `ReportGuard` refuses to emit a headline
  metric unless a spatial-CV "real win" over mandatory baselines (climatology, logistic/GBDT, persistence)
  clears a bootstrap confidence interval (R16). The 6 CI gates fail the build on common dishonesty/safety
  violations.
- **A single, auditable decision function:** `level = max(conformal_level(fused_risk, p*), shield_floor)`
  with **p\* = C_FA/(C_FA+C_miss) ≈ 0.0476** (C_FA=5, C_miss=100). One function; every legacy threshold maps
  to an internal role; no alert path bypasses it.
- **Calibration that survives shift:** split-conformal is replaced/augmented by weighted CP (WCPS),
  Adaptive Conformal Inference (ACI), Mondrian per-hazard CP, and Conformal Risk Control for the decision
  level-sets — because calibrated members ≠ calibrated ensemble and coverage collapses under drift.
- **Graceful degradation is a first-class requirement:** missing modalities, dead nodes, solar brownout,
  and cloud outages are treated as *expected*, with reliability-gated fusion and an offline alert path.
- **Hazard-physics correctness bugs were found and fixed** (e.g. the Iverson transient term must use
  `D1 = D0/cos²β` only, with no spurious `cos β` multiplier) and locked behind golden-case tests.

## 1.6 What is NOT done / biggest risks (full list: chapter 22)

- No training, no datasets downloaded, no measured skill, no on-device latency/RAM/current numbers, no final
  live-verified BOM, no verified India regulatory/LoRa-band path. The disaster-evacuation RL environment is
  a **build gap** (no off-the-shelf env). Dataset licenses are **unverified**; all datasets are candidates.
- References are mostly **subagent-reported identifiers, not independently re-fetched** (a web_search
  outage during the research program) — a disclosed residual risk the reference-verification pass addresses.
- Geo events are few (n≈5-ish), so any eventual skill estimate will be **variance-dominated**.

## 1.7 Recommended next steps (from `FINAL_REPORT.md §14-15`)

Build order: (1) evaluation tooling + the "real-win" gate and a leakage-controlled benchmark; (2) edge CCTV
detector + physics feature; (3) temporal event validation; (4) calibrated fusion + conformal-under-shift +
drift monitor; (5) IoT node + drift correction + prototype; (6) robustness red-team; (7) anomaly + advisory
RL (after building the evac env); (8) an India "shadow → advisory" pilot. Each step is gated by its
pre-registered cross-camera/cross-site decision rule. Before procurement: live-verify the BOM; before any
claim: pass the spatial-CV admission gate; before any public alert: certification + authority + a human.
