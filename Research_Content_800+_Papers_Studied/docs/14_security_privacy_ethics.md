# 14 — Security, Privacy, Ethics, Misuse & Legal Notes

> **Audience:** safety / ethics / legal reviewers, and the engineers who will build the pilot. Read `00` and
> `01` first, then this chapter alongside `08` (alerting + the IP verdict) and `22` (limitations).
>
> **Two hard framing rules carried from `_CANON.md`:**
> 1. **Nothing in TRINETRA has been built, trained, or measured as a product.** The numpy core runs (128
>    tests, 6 CI gates — `[CONFIRMED]`), but no model is trained and no dataset is downloaded. Every threat
>    "mitigation" below is therefore either **present in the reference code** (I cite the file) or **planned
>    in the design** (I say so). No security property here is a *measured* security guarantee.
> 2. **This chapter is NOT legal advice.** Every India regulatory / certification / data-protection /
>    alerting-authority statement is an **`[UNVERIFIED]` search lead** that must be checked against official
>    sources and reviewed by a qualified legal/standards professional before any reliance. Honesty labels
>    `[CONFIRMED]` / `[LIKELY]` / `[HYPOTHESIS]` / `[INFEASIBLE]` follow `_CANON.md §1`. "A cited paper
>    reports X" is kept visibly separate from "our design intends Y". Reference IDs resolve in chapter 19.

Primary sources: `DESIGN/HLD.md §6` (cross-cutting controls), `§9/§10` (traceability + risks); the
`DEPLOYMENT/` folder (`responsible_release.md`, `standards_and_regulation.md`, `stakeholders_and_partners.md`,
`pilot_design.md`, `what_this_system_is_not.md`); `FINAL_REPORT.md §4, §12`; and the implemented code in
`trinetra/src/trinetra/ws3_alert/`, `ws6_robust/`, `ws7_iot/`, `common/security.py`, and
`trinetra/scripts/ci_gates.py`.

---

## 14.1 Why this chapter is load-bearing

TRINETRA is a **life-safety advisory system**. Its outputs can influence whether a human operator issues or
withholds a public warning for a landslide, flash-flood, cloudburst, GLOF, or fire. That makes three failure
classes catastrophic in a way an ordinary ML system's are not: (a) a **spoofed or forged alert** that causes
panic or a false "all clear"; (b) a **confidently-wrong model** that an operator trusts; and (c) **misuse** of
the sensing stack for surveillance. The whole security/privacy/ethics posture exists to keep the system
**advisory, human-gated, corroborated, and honest about uncertainty** — never an autonomous authority.

The single structural control that everything else leans on is **Rule R19** (`_CANON.md §5`): the system is
advisory, human-in-the-loop, and fails safe to "uncertain/offline"; it **NEVER** crosses from an advisory
level to a public alert without a human. In the code this is not a comment — it is enforced: `build_cap()`
raises `SafetyViolation` unless handed a human approval token (`ws3_alert/cap.py:35`), and a CI gate asserts
that refusal (`ci_gates.py` `G-advisory`). `[CONFIRMED — gate passes in this environment.]`

---

## 14.2 Threat models

Each threat below states the **attacker goal**, the **vector**, and the **mitigation that is actually present
in the code or planned in the design**, with an honesty label on each mitigation's maturity. None of these
mitigations has been penetration-tested; they are design/implementation controls, not measured defenses.

### T1 — Spoofed / replayed alerts (forged "evacuate" or forged "all-clear")
- **Vector.** The last-mile public-warning channel is spoofable *by design*. Cell-broadcast / PWS delivers
  alerts via 3GPP SIB messages **broadcast without authentication or acknowledgment** so any fake base
  station can impersonate the network (paper arXiv **2604.24404** reports this and demonstrates an
  open-source 5G PWS spoofing testbed). A forged "evacuate now" causes panic/phishing; a forged "all clear"
  is a life-safety threat. In India the analogous last-mile channel is the NDMA Cell-Broadcast / **SACHET**
  system `[UNVERIFIED — confirm against official sources]`.
- **Mitigation (present + planned).**
  - **Signed CAP.** The CAP 1.2 builder appends an **HMAC-SHA256 signature** over the serialized XML when a
    key is supplied (`ws3_alert/cap.py:75-79`). `[CONFIRMED present in code]`. The design intent is end-to-end
    **XML digital signatures** on CAP; HMAC here is an honest placeholder because the `cryptography` library
    is absent from the sandbox (same reasoning as T6). `[LIKELY — upgrade path to asymmetric signatures.]`
  - **Cross-cell / multi-source corroboration.** For the unauthenticated cell-broadcast leg, the design
    adopts 2604.24404's defense: treat a **single-source** alert as suspicious; a genuine alert should appear
    on multiple independent channels (CB + app + SMS) before a client treats it as authoritative.
    `[HYPOTHESIS — design intent, not implemented in the reference code.]`
  - **Replay protection.** Mesh frames are guarded by a monotonic `(node_id, seq)` window: `ReplayGuard.accept`
    rejects any `seq <= last` seen for that node (`ws7_iot/sensor_reading.py:51-62`). `[CONFIRMED]`. Alert
    identifiers are per-zone + timestamp (`cap.py:46`), giving dedup a stable key.
- **Residual risk.** HMAC is symmetric (shared key ⇒ any holder can forge); cross-cell verification is
  unimplemented; India SACHET integration is `[UNVERIFIED]`. See also §14.9.

### T2 — Camera tampering / blinding
- **Vector.** An attacker (or weather/soot) physically covers, defocuses, repositions, or floods the lens of a
  CCTV / ESP32-CAM node so fire/flood is not seen — a denial of the *sensing* layer, not the alert layer.
- **Mitigation (planned).** The robustness doctrine (`HLD §6`) treats **node outage and missing inputs as
  EXPECTED, not exceptional**. A blinded or dropped camera must **lower trust and widen uncertainty**, never
  silently assert "all clear": the missing-modality adapter marks an absent source `available=False` and
  inflates the remaining experts' uncertainty (`ws6_robust/missing_modality.py:14-27`), driving the decision
  layer toward "uncertain" (R19 fail-safe). `[CONFIRMED present in code — as a degradation mechanism, not a
  tamper *detector*.]` Tamper/occlusion **detection** itself (blur/scene-change health checks on the frame)
  is design intent only. `[HYPOTHESIS]`
- **Residual risk.** No implemented tamper detector; a slowly-degraded lens could pass as a quiet scene.

### T3 — Adversarial inputs (patch attacks on the detector)
- **Vector.** A crafted physical patch or digital perturbation on the CCTV detector's input suppresses a fire
  detection or triggers a false one. For the deepfake/forensic path, adversarial evasion is the central
  problem: paper arXiv **2003.01279** reports that deepfake defenses and evasions **co-evolve** and that a
  one-time blur defense is defeated by spread-spectrum attacks.
- **Mitigation (planned).** The design mandates **continuous red-teaming** (`HLD §6`: "red-team — adversarial
  patches on the detector") and treats robustness as a *process*, not a one-time hardening (`responsible_release.md`
  §1; `ws6_robustness/` plan). The operational safety net is again R19 + corroboration: vision is one expert
  among physics and IoT, adversarial or merely-wrong inputs are treated as **untrusted argued input**, and the
  conformal/abstention layer must be **stress-tested adversarially** (design input from arXiv 2609.31142 on
  calibrated-decision models under attack). `[HYPOTHESIS / planned — no adversarial training or patch defense
  is implemented in the numpy core.]`
- **Residual risk.** No measured adversarial robustness; "robustness transfers" is explicitly NOT assumed
  (paper 2606.07593 reports adversarial training did not change the sparse representation a ViT learned).

### T4 — Data poisoning of training / logged data
- **Vector.** An attacker injects crafted samples into training data or the field-logged event stream to shift
  the model's operating point (e.g., learn to ignore a real precursor), or poisons the calibration set so
  conformal coverage is silently wrong.
- **Mitigation (planned + partial).** (a) **Provenance & reproducibility** (`HLD §6`, feature F-17): pinned
  seeds, logged spatial-CV folds, tracking, and a "real-win" gate on every improvement, so an unexplained
  behavior change is visible. (b) **Leakage/anti-look-ahead gate**: `assert_no_time_leak` rejects features
  whose timestamps are at/after the decision time, enforced in CI (`ci_gates.py` `G-leak`). `[CONFIRMED]` —
  this blocks temporal contamination, a poisoning-adjacent integrity bug, though it is not a poisoning
  detector per se. (c) **Drift monitoring** (T5) catches a distribution that has been shifted. `[LIKELY]`
- **Residual risk.** No implemented data-sanitization or poisoning detector; calibration-set integrity depends
  on governed data collection (§14.4) and access controls (`responsible_release.md §4`).

### T5 — Model confidently-wrong as a *safety* threat
- **Vector.** This is a threat even with no adversary. Paper arXiv **2610.08810** reports a geospatial
  foundation model under geographic shift whose **accuracy fell from 0.65 to 0.40 while its confidence stayed
  HIGH**, with **12–51% of shifted scenes confidently mislabeled** (`DEPLOYMENT/literature_map.md`). A
  confidently-wrong model that an operator trusts can cause a missed evacuation or a false alarm.
- **Mitigation (present + planned).** This is why calibration and drift monitoring are first-class:
  - **Honest conformal coverage, never a "guarantee."** `ws6_robust/conformal.py` provides split-CP, weighted
    CP for covariate shift (WCPS), **Mondrian/class-conditional CP** so a rare critical hazard (e.g. GLOF) is
    not hidden by marginal coverage, **Adaptive Conformal Inference** for long-run coverage under drift, and
    **Conformal Risk Control** that bounds the *miss-rate* (the quantity that matters for a life-safety alarm).
    The module docstring states coverage is reported as realized and is **voided under concept drift**.
    `[CONFIRMED present in code]`.
  - **Drift monitor voids trust.** `ws6_robust/drift_monitor.py` computes PSI + CUSUM; on drift it emits
    `reliability=Unreliable` and the decision layer **fails toward "uncertain"** (R19). `[CONFIRMED]`. The
    pilot's stopping rule is explicitly to halt if calibration collapses under shift, monitoring **MC-dropout
    entropy** which flagged all shifts in 2610.08810 (`pilot_design.md §3`). `[planned]`
  - **Uncertainty-gated alerts, not raw confidence.** The doctrine (`ws6_robustness/`) is to gate on
    uncertainty entropy, not deterministic confidence.
- **Residual risk.** Entropy-flag recall is unmeasured on our data; "confident-while-wrong" is a disclosed
  top-10 build risk (`HLD §10`).

### T6 — Credential / key exfiltration (the historical proxy bug — now removed)
- **Vector (historical, real).** `TRINETRA_Bug_Report.md` records that early files `Proxy.py` / `Proxy_fixed.py`
  hard-coded `target_url = "https://api.justwoker.icu"` and forwarded `x-api-key` / `Authorization: Bearer`
  credentials to that **non-official third-party host** — an exfiltration path. (`[CONFIRMED]` the in-repo
  `api_key` field was empty, so **no key leaked in-repo**; but a historical "leaked SMTP password revoke"
  action item existed and its rotation must be confirmed.)
- **Mitigation (present).** The fix was to **remove the third-party endpoint and never forward bearer tokens to
  non-official hosts**. This is now backstopped by two implemented controls: (a) a fail-closed **endpoint
  allow-list** — `check_endpoint` raises `EndpointNotAllowed` for any host not on the list, and an empty list
  rejects everything (`common/security.py:16-24`); and (b) a **no-credential-egress CI gate** (`ci_gates.py`
  `G-security`, mapped to quality gate **G6** "no credential egress", `HLD §8`). `[CONFIRMED — gate passes.]`
- **Residual action.** Confirm the historical SMTP credential was rotated (`TRINETRA_Bug_Report.md:140`); use a
  secrets manager and key rotation in the build (§14.3). Do not re-introduce any outbound proxy.

### T7 — Node spoofing / Sybil on the LoRa mesh
- **Vector.** A rogue radio injects fabricated sensor frames (fake quiet readings to mask an event, or fake
  alarm readings to trigger a false RED), or floods the mesh with many fake node identities (Sybil) to drown
  out genuine nodes.
- **Mitigation (present + planned).** Every `SensorReading` is **authenticated**: `sign_reading` /
  `verify_reading` attach and check an **HMAC-SHA256** tag over canonical bytes (`ws7_iot/sensor_reading.py:38-48`);
  the design specifies **Ed25519 provisioned at flashing** for the real node, with HMAC as an **honest,
  clearly-labelled placeholder** because `cryptography` is unavailable in the sandbox. Replay is blocked by
  `ReplayGuard` (T1). `[CONFIRMED present; asymmetric upgrade LIKELY.]` A single spoofed node is further
  bounded by the design rule against a **single-node false RED** (listed as a carried risk, `HLD §10`):
  decisions corroborate across sensors/physics rather than trusting one node.
- **Residual risk.** Shared-key HMAC does not bind identity the way per-node Ed25519 keys would; Sybil
  resistance ultimately needs provisioned asymmetric keys + gateway admission control. `[HYPOTHESIS]`

### T8 — Denial of service on the gateway
- **Vector.** Flooding the LoRa concentrator / gateway with traffic, or knocking out its uplink, to suppress
  alerting at the moment it matters.
- **Mitigation (present + planned).** The architecture is **offline-first by design** (constraint **C1**): the
  offline alert path (node event → LoRa/DTN → gateway shield → local siren/SMS) works **independent of the
  cloud** (`HLD §5` flow 3). When the link is down, the **delay-tolerant store-carry-forward queue**
  (`ws3_alert/dtn.py`, binary Spray-and-Wait with a bounded copy budget) holds and rebroadcasts messages until
  a link returns, so a DoS on the uplink degrades to delayed delivery rather than lost alerting. `[CONFIRMED
  the DTN queue and offline path exist in code]`. Rate-limiting, duty-cycle budgeting, and admission control
  at the gateway are design intent. `[HYPOTHESIS]`
- **Residual risk.** A physical/radio-layer jam of the mesh itself is not defended in software; the local
  siren/shield path is the last-resort fail-safe.

---

## 14.3 Security controls (implemented / planned)

| Control | Status | Where | Maps to |
|---|---|---|---|
| **Endpoint allow-list, fail-closed** | `[CONFIRMED]` implemented + CI-enforced | `common/security.py:16-24`; `ci_gates.py` `G-security` | constraint **C6**, gate **G6** |
| **No raw-video egress** | `[CONFIRMED]` implemented + CI-enforced | `common/security.py:27-40`; `ci_gates.py` `G-security` | constraint **C7**, gate **G6** |
| **Signed CAP (HMAC-SHA256 now; XML-DSig / asymmetric intended)** | `[CONFIRMED]` present; `[LIKELY]` upgrade | `ws3_alert/cap.py:75-79` | T1 |
| **Message auth on IoT frames (HMAC now; Ed25519 at flashing)** | `[CONFIRMED]` present; `[LIKELY]` upgrade | `ws7_iot/sensor_reading.py:38-48` | T7 |
| **Replay / dedup counters** | `[CONFIRMED]` implemented | `ws7_iot/sensor_reading.py:51-62`; CAP id `cap.py:46` | T1, T7 |
| **Human-approval gate on public CAP** | `[CONFIRMED]` implemented + CI-enforced | `ws3_alert/operator.py`, `cap.py:35`; `ci_gates.py` `G-advisory` | R19 |
| **Anti-leak feature-timestamp gate** | `[CONFIRMED]` implemented + CI-enforced | `eval.assert_no_time_leak`; `ci_gates.py` `G-leak` | gate G6, T4 |
| **Key rotation + secrets management** | `[HYPOTHESIS]` design intent | `responsible_release.md §4` (access controls + audit logs) | T6 |

Two honesty notes on the crypto: (1) **HMAC is a symmetric placeholder.** Both the CAP signer and the IoT
signer use HMAC-SHA256 because the `cryptography` library is **not available in the sandbox** (`_CANON.md §2`
lists numpy/pandas/lxml only). The code and docstrings say so explicitly; the production design is asymmetric
signatures (XML-DSig for CAP, Ed25519 provisioned at node flashing). Do not ship HMAC as the final scheme.
(2) **Key rotation and a secrets manager are planned, not implemented.** `responsible_release.md §4` requires
access controls + audit logs; the historical proxy bug (T6) is the concrete reminder of why.

---

## 14.4 Privacy

The privacy posture is anchored in constraint **C7: raw video stays local**.

- **Raw video never leaves the node/gateway — enforced.** `assert_no_video_egress` scans any off-node payload
  and raises `SafetyViolation` if it carries a video-like field (`video`, `raw_video`, `frame`, `frames`,
  `clip`, `rtsp`, `mjpeg`) (`common/security.py:27-40`), and the CI `G-security` gate exercises this.
  `[CONFIRMED]`. Video is **edge-scored**; **only events + scores (and at most flagged clips, by policy) leave
  the node** (`HLD §6` Privacy; flow 2). This is the data-minimization principle made mechanical.
- **No biometric identification of private individuals.** The system is explicitly **NOT a surveillance /
  person-identification / tracking tool** and has **NO biometric or individual-tracking features**
  (`what_this_system_is_not.md`; `responsible_release.md §1`). This is a design constraint, not a tuning
  choice. `[CONFIRMED as a stated non-feature — there is no face/person-ID code to point to, by intent.]`
- **On-device / edge processing + optional privacy-preserving vision.** Processing happens at Tier-0/Tier-1
  (`HLD §4`); the design cites federated/edge scoring and forwarding only flagged clips (paper 2609.07403) and
  privacy-preserving action-recognition options (paper 2608.04501), including cheap optical-flow/skeleton
  inputs that reduce identifiability (paper 2507.21649). **Face-blur / on-device anonymization** is design
  intent for the build. `[HYPOTHESIS — not implemented in the reference code.]`
- **Data minimization, retention, lawful basis.** `responsible_release.md §4`: lawful basis + consent for any
  collected data, minimization + retention limits, local processing, access controls + audit logs, and a
  **datasheet** for every collected dataset. CCTV consent/signage is a pilot precondition (`pilot_design.md §4`).
  All of these are governance commitments, pending the legal review in §14.9. `[LIKELY / planned]`

One connected verdict from chapter 08 belongs here: **IP-address-based alerting is `[INFEASIBLE]`** for
life-safety targeting (`_CANON.md §6`; `FINAL_REPORT.md §4`) — consumer IP geolocation is ISP/city-granular,
corrupted by CGNAT/VPN/DHCP, and cannot address a person at risk. It was **not carried**. Public-IP exposure is
treated instead as a **security** concern (authenticated endpoints, §14.3), not a targeting mechanism. This
matters for privacy because it closes off a tempting but both-ineffective-and-privacy-invasive design path.

---

## 14.5 Misuse & dual-use

The sensing + forensic stack is dual-use, and the documentation says so plainly (`responsible_release.md §1`).

- **The deepfake detector is defensive-only.** Forensic/provenance components could in principle be inverted to
  *improve* a generator, so the release rule is: **release forensic detectors as defensive-only; do NOT release
  generation tooling; red-team continuously** (paper 2003.01279 shows defenses and evasions co-evolve). Social-
  media / deepfake evidence is **low-trust advisory only and must be corroborated** (`_CANON.md §6`).
- **The system must never be repurposed for surveillance or autonomous enforcement.** CCTV analytics could be
  abused for tracking individuals; the mitigations are **data minimization (raw video stays local), purpose
  limitation, and NO biometric/person-ID features** (`responsible_release.md §1`). Over-automation of
  alerts/evacuation is the other dual-use risk, and its mitigation is the same primary control below.
- **The primary misuse control is R19 — advisory-only, human-in-the-loop, fail-safe.** This is the one control
  that holds even if a technical defense is bypassed: the system can present a decision but **cannot issue a
  public alert or take enforcement action on its own.** It is enforced in code (CAP refuses without a human
  approval token; `operator.approve` requires the human to acknowledge the output is advisory;
  `ci_gates.py G-advisory` asserts the refusal). `[CONFIRMED]`
- **Safeguarded vs open release.** Open: physics derivations (with Class A/B/C labels), eval protocols, the
  leakage-controlled benchmarks we create, build manuals without exploit detail. **Not released / safeguarded:**
  anything enabling spoofed alerts, person-tracking, or deepfake *generation*; operational alert-channel
  credentials; raw personal video (`responsible_release.md §2`). A dual-use review + legal/ethics approval is
  required before any release (`responsible_release.md §6`).

---

## 14.6 Alert-fatigue & false-alarm cost policy

False alarms are not a mere nuisance in a life-safety system — they are a **real harm**. Repeated false alarms
cause "cry-wolf" fatigue: operators and communities stop responding, so a later true alarm is ignored. The
design treats this as a quantified trade-off, not a vibe.

- **The cost-loss asymmetry.** The decision uses an explicit cost model with **C_FA = 5** (cost of a false
  alarm) and **C_miss = 100** (cost of a missed event). A miss is 20× costlier than a false alarm, which is
  correct for life-safety — but C_FA is deliberately **non-zero** precisely because false alarms erode trust.
- **The operating point.** The optimal alarm probability threshold is
  **p\* = C_FA / (C_FA + C_miss) = 5 / 105 ≈ 0.0476** (`_CANON.md §4`, §6). This is the single number that
  encodes "alarm readily because misses are expensive, but not on everything, because false alarms cost trust."
  It is the same τ\* used by the one decision function `level(s) = max(conformal_level(fused_risk(s), τ\*),
  shield_floor(s))` (`HLD §2.3`). `[CONFIRMED as the design's canonical threshold — it is a *policy* number
  from the cost model, NOT a measured false-alarm rate.]`
- **Calibration manages it honestly.** Because the threshold acts on a *calibrated* risk, the conformal layer
  (§14.5 T5) is what makes p\* meaningful: miscalibration would silently move the real operating point. The
  **Conformal Risk Control** routine bounds the miss-rate directly (`conformal.py:129-157`), and the pilot
  pre-registers **false-alarms/day** and **missed-event rate + its uncertainty** as gating metrics
  (`pilot_design.md §2`). The literature target "temporal event validation cut false alarms 52%→4%" is a
  **source-reported** paper result and a *process target*, **not our measurement** (`FINAL_REPORT.md §11`).
- **Why not just alarm on everything.** Setting the threshold near zero minimizes misses but maximizes
  cry-wolf; the cost-loss p\* is the principled compromise, and the human-in-the-loop (R19) is the final filter
  that keeps a borderline advisory from becoming a public alarm.

---

## 14.7 Ethics & responsible release

- **Life-safety duties.** Because the domain is life-safety, the honest default is caution: the system is
  **complementary until independently certified** and must **fail safe to "uncertain/offline", never a false
  "all clear"** (`what_this_system_is_not.md`; `standards_and_regulation.md §3`). No performance surface is
  shown in the UI/API until the spatial-CV admission gate G2 passes (`HLD §7`).
- **Staged, supervised rollout.** Promotion is gated, not flipped on (`pilot_design.md §1`): **Stage 0 offline
  replay** (leakage-controlled, spatial-block CV) → **Stage 1 SHADOW** (observe + log, trigger NOTHING) →
  **Stage 2 ADVISORY** (human decides, still no autonomous public alert) → **Stage 3 (out of scope)** requires
  official approval + certification. Stopping/rollback rules halt promotion if calibration collapses under
  shift or on any safety incident (`pilot_design.md §3`).
- **Expert / ethics / accessibility sign-off is a precondition, not a formality.** Before any real-world
  reliance (`what_this_system_is_not.md`): independent validation; independent **expert review** spanning fire
  science (physics Class A/B/C), ML, safety, legal/standards, **ethics**, and **accessibility**
  (`FINAL_REPORT.md §15.3`); certification + official approval for any alerting role; robustness + security
  evidence; verified data-protection compliance; and a successful staged pilot. **Independent ethics-review
  approval is required before Stage 1** (`pilot_design.md §4`).
- **Equity — do not under-serve remote communities.** The system is aimed at remote mountain communities
  (Uttarakhand + Himachal) precisely because they are under-served, so the offline-first, ≤₹2000-node design is
  itself an equity choice; the duty is to validate that skill **holds across sites and seasons** rather than
  working only where data is rich (the confident-while-wrong-under-shift risk, T5, is also an equity risk —
  it would most hurt the places with the least representative training data). Community value elicitation is
  required **before** build (paper 2610.03724; `pilot_design.md §4`).
- **Accessibility of alerts.** Alerts must be **multi-modal and low-literacy accessible**; disability &
  accessibility groups are named stakeholders for co-design (`stakeholders_and_partners.md` rank 8). `[planned]`

---

## 14.8 How the controls compose (defense-in-depth)

No single control is trusted alone; they are layered so that bypassing one still leaves the system safe:

1. **Authenticate the inputs** — signed/HMAC'd IoT frames + replay guard (T1, T7).
2. **Do not trust any single source** — corroboration across physics/IoT/vision; single-node false RED is a
   named risk; deepfake/zero-shot signals are low-trust advisory (T2, T3, misuse §14.5).
3. **Quantify and gate on uncertainty** — conformal calibration + drift monitor void trust under shift; fail
   to "uncertain" (T5).
4. **Keep data local and minimal** — no raw-video egress, no biometrics (privacy §14.4).
5. **Keep egress fail-closed** — endpoint allow-list + no-credential-egress CI gate (T6).
6. **Keep a human decisive** — R19 human-approval gate on every public alert (misuse §14.5).
7. **Keep the alert path alive offline** — C1 offline-first + DTN store-carry-forward (T8).

The CI gates (`ci_gates.py`) make four of these fail-closed invariants (advisory, security, leak, class-C
default-off) **non-negotiable at build time**: any regression exits non-zero. `[CONFIRMED — ALL 6 CI GATES
PASS in this environment, `_CANON.md §2`.]`

---

## 14.9 Legal notes (NOT legal advice)

Everything in this section is an **`[UNVERIFIED]` search lead** derived from arXiv-era research notes. arXiv
retrieval **cannot confirm regulatory facts**. Each item must be checked against **official sources** and
reviewed by a **qualified legal/standards professional** before any reliance (`standards_and_regulation.md`;
`FINAL_REPORT.md §12`). No law, standard number, or agency mandate below is asserted as established fact.

| Item | What must be verified (official source) | Status |
|---|---|---|
| **LoRa IN865–867 MHz band legality** | National radio/telecom regulator's license-exempt bands, power limits, duty cycle; whether this band is legal for the deployment region | `[UNVERIFIED]` — also a top carried risk (`HLD §10`) and open backlog item (`FINAL_REPORT.md §15.6`) |
| **Who may originate CAP / SACHET / cell-broadcast / WEA alerts** | Access rules for any national alerting program; whether a private/academic party may originate official public alerts (the design assumes it **may not**) | `[UNVERIFIED — likely MAY NOT originate]` |
| **Fire-detection product certification** | National building & fire-safety codes; whether a fire-detection product must be certified to be treated as a safety device | `[UNVERIFIED]` |
| **Data-protection obligations for CCTV/personal video** | Lawful basis, retention, minimization, data-subject rights under applicable national data-protection law | `[UNVERIFIED]` |
| **Surveillance / CCTV municipal rules** | Consent/signage; public vs private premises differences | `[UNVERIFIED]` |
| **Social-media data ingestion** | Platform ToS + data-protection law; redistribution limits (e.g. tweet-ID-only) | `[UNVERIFIED]` |
| **Electronics / EMC certification** | Mandatory product safety/EMC certification for deployed hardware | `[UNVERIFIED]` |

The binding posture while these are unverified (`standards_and_regulation.md §3`): **SHADOW then ADVISORY only;
a human authority owns every alert decision; market as a decision-support aid, NOT a certified safety device;
endpoints authenticated; data minimized.** Official regulatory/alerting-path contacts (e.g. an NDMA /
C-DOT-type authority) are a **build-phase** activity through proper institutional channels — this program only
*proposes* who to involve and *contacts no one* (`stakeholders_and_partners.md`).

---

## 14.10 References

Reference IDs cited above (arXiv) resolve with full detail and verification status in **chapter 19**
(`19_REFERENCES_FULL.md`): **2604.24404** (PWS spoofing + cross-cell verification), **2003.01279** (Disrupting
Deepfakes — defenses/evasions co-evolve), **2610.08810** (foundation model confident-while-wrong under
geographic shift), **2609.31142** (adversarial benchmark for calibrated-decision RL), **2606.07593**
(adversarial training does not transfer robustness), **2609.07403** (federated / forward-only-flagged-clips
privacy), **2608.04501** (privacy-preserving action recognition), **2507.21649** (optical-flow/skeleton as a
privacy lever), **2610.03724** (community value elicitation), **2608.22293** (spatial-block CV — random CV
overstates skill). Primary design/code sources: `DESIGN/HLD.md §6/§9/§10`, the `DEPLOYMENT/` folder,
`FINAL_REPORT.md §4/§12`, and `trinetra/src/trinetra/{ws3_alert,ws6_robust,ws7_iot,common}/` with
`trinetra/scripts/ci_gates.py`.
