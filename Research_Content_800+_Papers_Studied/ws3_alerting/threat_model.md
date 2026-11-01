# ws3_alerting/threat_model.md — alerting security & abuse threat model (P12, WS3)

Phase P12 · RESEARCH-ONLY. MASTER_PROMPT P12 task 4. Research, NOT legal advice. Uses P9/P10 network-anomaly
findings. No own-system claim (Rule 16). Rule 19: human oversight for high-stakes alerts.

## 1. Assets / adversaries
Assets: the alert channel's integrity (only true alerts go out), availability (alerts not suppressed),
and the opt-in registry's privacy. Adversaries: pranksters/rogue SDRs, DoS/jammers, insiders, data thieves.

## 2. Threats + mitigations
- SPOOFED ALERTS: cell-broadcast air interface is UNAUTHENTICATED — a rogue SDR makes phones "readily display
  spoofed alerts" (2604.24404). Our owned tiers (2/1) MUST authenticate: sign every alert (public-key /
  HMAC), device verifies before acting; cross-cell corroboration flags single-source cell-broadcast spoofs
  (2604.24404). Tier 1 siren is physically local (hard to spoof remotely).
- REPLAY: monotonic counters + timestamp windows (reuse P6 replay protection); reject stale/duplicate alerts.
- ALERT FATIGUE / FALSE ALARMS (a security problem — erodes compliance, cry-wolf 1904.01963): precision gate
  + per-area budget + staggered rollout + logged suppression (architecture §7).
- DoS / JAMMING: RF jamming can suppress radio tiers; multi-radio + spread-spectrum improves resilience (PDR
  >95% under jamming, SIM, 2603.02105); Tier 1 siren is jam-proof; detect-and-report jamming via the network-
  anomaly layer (P9/P10).
- BROADCAST STORM / DENSITY COLLAPSE: BLE mesh collapses at density (1910.03345) → cap hop count/TTL, rate-
  limit relays, position/energy-aware routing (2510.03714).
- INSIDER MISUSE: role-based origination rights, two-person rule for wide/high-stakes alerts (Rule 19),
  full audit log of who issued what.
- KEY MANAGEMENT: provisioning + rotation + revocation for node/gateway signing keys; clock sync for replay
  windows (hand to P6/P13); compromised-key → revoke + behavioral/physics corroboration (P9/P10).
- REGISTRY PRIVACY: opt-in, consent-based, minimal PII, data minimization, local storage; no profiling of
  individuals; privacy-law considerations (research, not legal advice) — align to Indian DPDP-style consent
  norms (verify).

## 3. Authentication design (owned tiers)
Signed CAP-style alert messages (origin + area + severity + expiry + nonce) → device verifies signature +
freshness + area before rendering; unauthenticated messages are dropped or shown as UNVERIFIED only. Ties to
the P11 trust pipeline when a social report is the trigger (human-in-the-loop).

## 4. Carried to P16
All threats enter the P16 robustness/security failure-mode catalogue with test plans (spoof injection, replay,
jamming, density collapse, key compromise).

## 5. Honesty
The cell-broadcast spoofing finding is source-reported (2604.24404); whether only authorities may originate
cell broadcast is UNVERIFIED (confirm vs standards). Jamming-resilience numbers are SIMULATION. Nothing built.
