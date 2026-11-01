# DEPLOYMENT/pilot_design.md — staged, supervised pilot protocol (P19)

RESEARCH NOTES ONLY; pilot is for the LATER build, not now. Rule 19: SHADOW first (observe + log, NEVER trigger
real alerts), then ADVISORY with human review; NO automated public alert without extensive evidence + official
approval + certification. Methodology from the literature (source-reported).

## 1. Stages (gated promotion — ATAL/Decision-Readiness-Level style, 2609.13552; staged-rollout 2608.08528)
- STAGE 0 — OFFLINE REPLAY: evaluate on held-out, leakage-controlled data (spatial-block / leave-one-incident-
  out CV, 2608.22293; confident-while-wrong caution 2610.08810). Gate: meets pre-registered offline targets.
- STAGE 1 — SHADOW MODE: system observes live feeds, logs detections + uncertainty; triggers NOTHING; outputs
  compared against ground truth / operator judgement. Gate: false-alarms/day, time-to-detection, uptime meet
  pre-registered thresholds over a fixed window.
- STAGE 2 — ADVISORY MODE: outputs shown to a HUMAN reviewer who decides; still no autonomous public alert.
  Gate: human-factors evaluation (does advisory improve operator decisions? conformal sets RCT 2401.13744).
- STAGE 3 (NOT in scope of this program): any move beyond advisory requires official approval, certification,
  and evidence from Stages 0-2 — explicitly deferred.

## 2. Success metrics (tied to pre-registered protocols)
False-alarms per day; time-to-detection (latency, incl. the F-12 confirmation-window cost); uptime/
availability; missed-event (false-negative) rate at the operating point AND its uncertainty (2211.04340);
calibration under shift (PICP vs nominal, 2604.22787); operator decision accuracy (advisory stage).

## 3. Stopping / rollback rules
- Halt promotion if realized coverage/calibration collapses under shift (monitor MC-dropout entropy; 2610.08810)
  or if the drift monitor (F-14) flags sustained drift.
- Roll back a stage on any safety incident, on false-negative-rate breach, or on monitor-signal collapse
  (monitor-the-monitor, 2607.25842).
- Selective drift-triggered intervention beats continuous retraining (2604.02351); interventions stay ADVISORY.

## 4. Incident handling, consent, privacy, ethics
Pre-defined incident protocol with human escalation; CCTV consent/signage + data minimization (keep raw video
local, forward only flagged clips — 2609.07403); privacy-preserving action recognition options documented
(2608.04501); independent ETHICS-REVIEW approval required before Stage 1; community value elicitation BEFORE
build (2610.03724).

## 5. Site selection criteria
Representative of the target ODD (prove coverage, 2608.20864); willing fire-service/municipal host; mixed
camera quality + connectivity reality; a documented ground-truth path for evaluation.

## 6. Evidence required before any automated public alert
Independent certification + official approval; sustained Stage-1/2 performance across sites and seasons with
honest statistics (IQM + CIs, 2108.13264); robustness evidence (P16); demonstrated fail-safe to "uncertain/
offline" never a false all-clear. HONEST: this bar is NOT met by any research-phase output.
