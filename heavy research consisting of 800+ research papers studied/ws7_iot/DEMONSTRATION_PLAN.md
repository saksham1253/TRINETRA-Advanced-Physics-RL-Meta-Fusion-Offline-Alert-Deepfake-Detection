# ws7_iot/DEMONSTRATION_PLAN.md — 3–5 minute demonstration package (P13, WS7b)

Phase P13 · DOCUMENTS ONLY. MASTER_PROMPT P13 task 6. A repeatable demo script for stakeholders/experts/
evaluators. Nothing demonstrated now; measured-number slots = "to be filled after the build" (Rule 16).
Governed by ws7_iot/SAFETY.md (safe stimuli only). Rule 19: framed as an advisory sensor, not a certified
alarm.

## 1. Demo script (3–5 min, repeatable)
0:00 Setup shot: node powered, dashboard open on a phone (SoftAP, no internet). State = MONITOR.
0:30 STIMULUS: present a safe stimulus (incense smoke at a safe distance) → SENSING: live curves rise on the
     dashboard. 1:15 ON-DEVICE DECISION: fusion crosses PRE-ALARM → ALARM after corroboration + dwell.
1:30 LOCAL ALERT: buzzer + strobe fire; dashboard shows ALARM, fused confidence + uncertainty, per-sensor
     health. 2:00 OFFLINE PROOF: show there is no internet (router off / airplane mode) — everything still
     works. 2:30 SPOOF REJECTION: replay/forge a message → receiver REJECTS it (log shown). 3:00 GRACEFUL
     DEGRADATION: induce a sensor fault → it is flagged + down-weighted; a powered-off peer shows "offline",
     NOT "all clear". 3:30 NUMBERS SLIDE: measured latency/false-alarm-suppression/range — "to be filled
     after the build". 4:00 Honest limitations (LIMITATIONS.md) stated aloud.

## 2. Backup plan for demo failures
Pre-recorded screen capture of a successful run; a second assembled node on standby; a known-good stimulus +
a spare (incense + spare lighter-for-warm-object under SAFETY.md); dashboard screenshots as fallback; if radio
fails, show local annunciation only and state so honestly. Never fake a result.

## 3. One-page architecture figure spec (for a designer)
Single landscape page: sensors → signal conditioning → physics/fusion → anomaly/health → decision (state
machine) → local annunciation + signed radio → local dashboard; a dashed "optional authenticated internet
uplink"; a padlock on dashboard + radio (auth); a battery/solar block with "offline-capable"; the Rule 19
"advisory, human oversight" banner. Deliver as the demo's title slide.

## 4. Photos to take (at build)
Assembled node (open + closed enclosure); pin wiring close-ups; dashboard in MONITOR and ALARM; strobe lit;
the no-internet proof; the spoof-rejection log; the test bench with safe stimulus; battery/solar subsystem.

## 5. "What the prototype will and will not prove" → ws7_iot/LIMITATIONS.md
See LIMITATIONS.md (honest statement, task 6).

## 6. Honesty
No demo run; all numbers deferred to the build. The spoof-rejection and offline-operation steps demonstrate
REAL designed behaviors, but their measured metrics are filled only after the build.
