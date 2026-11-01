# ws3_alerting/architecture.md — tiered offline alerting architecture (P12, WS3)

Phase P12 · RESEARCH-ONLY. MASTER_PROMPT P12 tasks 3+5. Every capability number is SOURCE-REPORTED from
ws3_alerting/literature_map.md (reader 717e5ad8) or marked UNVERIFIED. No own-system claim (Rule 16). Rule 19:
high-stakes alerts require human oversight; the system never autonomously evacuates. Builds on the
feasibility verdict (feasibility_analysis.md): alert by PROXIMITY, not IP address.

## 1. Design shape: graceful-degradation tiers
Each tier is independent and degrades gracefully; higher tiers add reach when available, lower tiers always
work. A detection-confidence→tier decision policy (§6) gates escalation; alert-fatigue controls (§7) bound
false alarms.

## 2. TIER 1 — Local siren / strobe / PA (always works, no device)
- Reaches EVERYONE in earshot/eyeshot; needs no phone, app, network, or internet. The most reliable life-
  safety primitive for a localized fire.
- Powered + offline (battery/solar); triggered directly by the local detector/gateway.
- Limits: bounded physical range; ambiguous (what/where/what-to-do); accessibility (deaf/blind → pair siren
  WITH strobe + PA voice message). Multi-modal by design.

## 3. TIER 2 — Local LAN / mesh / BLE push to opt-in devices
- SAME-LAN alerting: UDP broadcast / multicast / mDNS / a local server pushing WebSocket/SSE to a local web
  page / captive-portal notice — reaches ONLY devices joined to our local network running our listener/page
  (feasibility_analysis §4-§5). Opt-in.
- SHORT-RANGE RADIO MESH (community backbone, no operator):
  - LoRa / Meshtastic: ~2.47 km semi-open link, −110 dBm/+2.75 dB SNR (source-reported, n=62) [2605.20379];
    tiered SF link-budget — SF7-8 up to ~120 dB path atten, SF12 up to ~180 dB / −18 dB SNR [2605.17063];
    FOREST drops to ~600 m [2303.12754]. Low data rate; duty-cycle limited; use position/energy-aware routing
    not naive flooding (+185% throughput/−75% energy) [2510.03714]; mesh overlay extends delivery ↑5×, energy
    ↑12.6× vs single-hop (ns-3) [2512.00161]. ROLE: carry alerts between nodes/sirens across a
    neighbourhood/valley off-grid.
  - BLE: a BlueFlood-style advertising flood reportedly reaches OFF-THE-SHELF smartphones at 99.9% delivery
    (0.4% duty, 38 B, 200 ms) [2002.12906] — a candidate last-100-m to UNMODIFIED phones; BUT BLE mesh is
    density/WLAN-interference fragile (~250 ms/10 hops, 3/40 channels, broadcast-storm collapse) [1910.03345;
    2106.04230], and background reception depends on the phone OS/app scanning. Treat as PROMISING but
    verify-on-hardware; a fleeing crowd (dense, RF-noisy) is the stress case.
- ESP-NOW / Zigbee / 802.11s: range/PDR GAPS (no primary paper in budget); 802.11s stock-phone BACKGROUND
  reception UNVERIFIED. Carried as open hardware-verification items.

## 4. TIER 3 — Cellular broadcast / SMS when available (authority-operated)
- Cell Broadcast / WEA / EU-Alert / India CAP (NDMA/C-DOT SACHET): reaches ALL phones in a geographic cell
  with NO per-user address or internet, demonstrably changing behavior at scale (Michigan WEA −1.1°F)
  [2607.27584]; geo-targeting is payload-length-constrained (polygon compression) [1509.05505].
- REGULATORY REALITY (partly UNVERIFIED, literature_map): origination is an AUTHORITY function; a private
  party almost certainly CANNOT originate WEA/cell broadcast and must REQUEST an official alert from an
  authorized agency. Confirm vs ITU/3GPP/NDMA before relying on it.
- SMS gateways need CELLULAR (not internet) and per-number addressing (opt-in registry only); not "offline".
- Air interface is UNAUTHENTICATED (spoofable by rogue SDR) [2604.24404] → see threat_model.md.

## 5. TIER 0 — Delay-tolerant backstop (infrastructure gone)
- Phones store-carry-forward (DTN) when all infrastructure is down [2601.00109]; but ~68% delivery / ~72 min
  delay [2601.00148] → a RESILIENCE BACKSTOP for slow/standing hazards, NOT a fast-fire primary path.

## 6. Decision policy: detection confidence/uncertainty → alert tier (Rule 19)
- Inputs: CCTV detection (P8), fusion probability + uncertainty (P14), IoT sensor alarms (P6/P9), anomaly
  layer (P9/P10), and — when social media is involved — the deepfake/trust pipeline verdict (P11,
  human-in-the-loop).
- Policy: LOW confidence → Tier 1 local pre-alert / human review, no wide broadcast; MEDIUM + corroborated
  by ≥2 independent sources → Tier 2 local push + human-confirm; HIGH + corroborated → request Tier 3
  official alert (authority) with human oversight. STAGGERED rollout (not one blast) to avoid self-induced
  congestion (−70% to −89% social cost from staggering/info-design) [2606.30320]. HIGH-STAKES alerts ALWAYS
  human-gated (Rule 19).
- The confidence→tier thresholds use the P11 cost-matrix logic (C_FP vs C_FN) and are a documented config,
  not a hidden guess.

## 7. Alert-fatigue controls
Detection-precision gate before any wide tier (cry-wolf erodes compliance [1904.01963]); per-area
false-alarm budget; persistence/dwell before escalation; announced drills clearly labelled; plain
"Basic-Information" wording (beats threat framing [2102.00589]); de-duplication across tiers; logged
suppression of chronically-flagging sources (surfaced to humans so suppression can't hide a real hazard).

## 8. Security / privacy (→ threat_model.md)
Signed alerts + replay counters (reuse P6 crypto + P9/P10 network-anomaly findings); rate limiting; opt-in,
consent-based registry (privacy-preserving); no profiling. Cross-cell corroboration to flag spoofed cell
broadcasts [2604.24404].

## 9. Honesty
Tiers 1/2/0 are what a private project CAN own; Tier 3 depends on authorities (regulatory point UNVERIFIED,
to confirm). BLE-to-stock-phone and 802.11s background reception need HARDWARE verification. All ranges/PDRs
are source-reported, several from SIMULATION; nothing simulated or built here.
