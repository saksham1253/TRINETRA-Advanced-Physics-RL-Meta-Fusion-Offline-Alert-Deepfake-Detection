# 03 — Requirements and Scope

**Audience:** anyone deciding what the project must do, must not do, and under what fixed constraints.
Ground truth: `DESIGN/HLD.md §7`, `DESIGN/SYSTEM_DESIGN_PROMPT.md`, `ASSUMPTIONS.md`, `FINAL_REPORT.md`,
`TRINETRA_Workstreams.md`. All constraints below are **binding** on every chapter and every design choice.

---

## 3.1 Goals (what the system must achieve)

G-1. Detect and give early warning of rapid-onset mountain hazards — landslide, flash-flood, cloudburst,
GLOF — in Uttarakhand + Himachal Pradesh, from free satellite EO + cheap ground IoT + opportunistic vision.

G-2. Detect fire/smoke/disaster from existing CCTV at the network edge, with temporal event validation to
suppress false alarms.

G-3. Produce a **single, calibrated, shielded, advisory alert level** (Green/Yellow/Orange/Red) with honest
uncertainty, auditable back to its contributing evidence and the shield reason.

G-4. Operate **offline-first**: the alert path (node → LoRa/DTN → gateway → siren) must work with the cloud
unreachable.

G-5. Degrade gracefully when modalities, nodes, solar power, or connectivity are lost — treat these as
expected, not exceptional.

G-6. Keep a human in the loop for every public-facing action; provide decision support, never autonomous
dissemination.

> **Local-siren carve-out (reconciled with chapter 08 §08.3):** the one actuation Tier-1 may trigger without
> a human is the **local on-site siren/strobe** (`siren.py`, source ∈ {node_edge, shield, operator}). This is
> treated as a *local physical alarm* for people in immediate earshot — **not** an "official public alert"
> (no CAP message, no broadcast, no naming of a hazard to the public). Official dissemination (CAP/SACHET/
> cell-broadcast) always requires a human + authority. So G-6 holds for *dissemination*; the local siren is
> the deliberate, scoped exception.

G-7. Be reproducible and falsifiable: pinned seeds, logged spatial-CV folds, mandatory baselines, and a
pre-registered "real-win" gate on every claimed improvement.

## 3.2 Non-goals (explicitly out of scope)

N-1. **Autonomous public alerting.** The system never originates an official alert without a human and the
proper authority/certification. `[INFEASIBLE]` / disallowed. (R19.)

N-2. **IP-address-based location or targeting of people/alerts.** Ruled `[INFEASIBLE]` (chapter 08): consumer
IP geolocation is ISP/city-granular, CGNAT/VPN/DHCP-corrupted, maps to no premises. Not carried.

N-3. **A deployed on-device fire-PINN solver.** `[INFEASIBLE]` now (stiffness/spectral-bias/
non-identifiability). Physics is used only as soft features/priors/consistency-checks with a Class-A
fallback, and as offline simulators (Class C, documentation-only).

N-4. **Any measured performance claim in this phase.** Nothing is trained or benchmarked; the project
produces designs, derivations, and honesty-gated reference code. (R16.)

N-5. **Paid data or paid cloud dependencies.** Only free datasets may ever be `STATUS=selected`; build
compute is Kaggle-only. (Constraints below.)

N-6. **Surveillance / biometric identification of private individuals, or raw-video egress.** Privacy
constraint C7; raw video stays on the node.

N-7. **Legal/regulatory determinations.** All India standards / certification / radio-band / alerting-
authority facts are `[UNVERIFIED]` search leads for qualified professional review. Nothing here is legal
advice.

## 3.3 Hard constraints (binding, from the master program)

| ID | Constraint | Consequence in design |
|----|-----------|-----------------------|
| **C1** | Offline-first alert path | node→LoRa/DTN→gateway→siren works cloud-offline; cloud never on the critical path |
| **C2** | ≤ ₹2000 per IoT node (incl. GST + shipping, ~10% contingency) | tiered BOM; all ₹ are `[EST]` until live-verified |
| **C3** | Build compute = Kaggle only, ~25–30 GPU-h/week, ≥15% reserve | PEFT/frozen-backbone first; CPU for all non-training work |
| **C4** | Free data only may be selected | datasets are candidates `[D]`; licenses unverified |
| **C5** | Life-safety → advisory, human-in-loop, fail-safe (R19) | no autonomous alert; fail to "uncertain/offline" |
| **C6** | Endpoint allow-list (no credential egress) | enforced in CI; signed CAP; key rotation |
| **C7** | No raw-video egress / privacy | edge-scored; only events/scores leave the node |
| **C8** | Heavy models Tier-1/2 only | Tier-0 runs only MCU-feasible statistics |
| **C9** | India LoRa band = IN865–867 MHz | SX1262 radio; 433 MHz SX1278 is non-compliant (bug #6) |
| **C10** | Honesty rules R16/R19/R20/R21 | no claim pre-gate; class labels; novelty = search claim |

## 3.4 Working assumptions (from `ASSUMPTIONS.md`; each has a verify-by phase)

| ID | Assumption | Risk if wrong | Verify |
|----|------------|---------------|--------|
| A-05 | BOM ₹ figures are `[EST]`; ≤₹2000 gate not yet enforced | infeasible BOM slips through | at build (live listings) |
| A-06 | LoRa band = IN865–867 MHz for India | illegal/non-functional radio | at build |
| A-07 | Only FREE datasets may be selected | paid dependency | dataset phase |
| A-08 | Kaggle only, ~25–30 GPU-h/wk, ≥15% reserve | plan exceeds compute | compute phase |
| A-10 | Sandbox date is 2026 (arXiv IDs up to 26xx valid) | mis-dated citations | ongoing |

Assumptions are **not facts** and never enter a report as facts.

## 3.5 Functional requirements by workstream (abridged; detail in chapters 06–13)

- **WS1 physics + fusion:** correct infinite-slope FS (saturated-limit guard), Iverson transient head
  (`D1=D0/cos²β` only), Fukuzono 1/v (α=2), Caine I–D; fire physics (Heskestad/Byram/Strouhal); a single
  gated meta-fusion head with a bounded residual and a Class-A fallback; golden-case unit tests (gate G1).
- **WS2 deepfake:** defensive-only authenticity scoring of inbound social-media media; low-trust, advisory,
  corroborated; continuous red-teaming (defenses and evasions co-evolve).
- **WS3 alerting:** offline-first store-carry-forward (DTN); signed CAP/SACHET; siren path; **no IP-based
  targeting** (N-2); no origination without authority.
- **WS4 CCTV:** compact edge detector (F-11) + temporal event validation (F-12) + IR flicker feature (F-16);
  cross-camera evaluation.
- **WS5 RL:** offline-RL **advisory** alarm policy that must **beat strong non-RL baselines** (e.g. MILP),
  selected by OPE with a lower-bound-≥-baseline rule, post-posed hard shield; never actuation.
- **WS6 robustness/eval:** spatial-block (not random) CV; mandatory baselines; conformal-under-shift;
  drift/calibration monitoring; cross-sensor corroboration as the most transferable defense; the 33-item
  hazard-correctness bug ledger closed with golden tests.
- **WS7 IoT:** ≤₹2000 tiered LoRa node; on-node drift correction + scheduled recalibration; fault-vs-event
  discrimination so a single faulty node cannot drive a RED alert unaided.
- **WS8 anomaly:** forecast-residual + Deep-SVDD (collapse-prevented) anomaly heads under a strict protocol
  (must beat persistence/general baselines; leakage-controlled; advisory input to fusion, never standalone).

## 3.6 Acceptance gates (a requirement is "met" only when its gate passes)

| Gate | Requirement it certifies | Blocks |
|------|--------------------------|--------|
| G1 | physics golden-case tests (geo + fire) | any downstream physics use |
| **G2** | spatial-CV admission (baselines + CI + cost-loss + real-win) | **ANY performance claim / publication** |
| G3 | single decision fn + realizable monotone shield + measured coverage | deployment |
| G4 | fusion stability + reliability gating + shield-floor monotonicity | GMF/PHARAOH deployment |
| G5 | ≤₹2000 live-verified BOM + tiered feasibility + fault discrimination + LoRa band | hardware order |
| G6 | no credential egress + offline alert path + anti-leak timestamp audit | field pilot |
| G7 | datacube size + dataset licenses + novelty honesty + Kaggle fit | submission |

## 3.7 Stakeholders and operating context
Target region: Indian Himalaya (Uttarakhand + Himachal). Primary user: a trained human operator/dispatcher
at a gateway/control room who reviews advisory levels and decides on CAP/SACHET dissemination through the
proper authority. Secondary stakeholders: fire-science / ML / safety / legal / ethics / accessibility
reviewers whose sign-off is a precondition for any Class-B/C physics or any field pilot. Deployment follows
a staged pilot: Stage 0 offline replay → Stage 1 shadow (observe/log, trigger nothing) → Stage 2 advisory
(human decides), with pre-registered metrics and rollback rules (chapter 15).
