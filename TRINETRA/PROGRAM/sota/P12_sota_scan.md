# PROGRAM/sota/P12_sota_scan.md — disaster-area communication & public-warning SOTA scan (WS3)

Phase P12 · RESEARCH-ONLY. SOTA + a targets section for the later build/simulation. All numbers SOURCE-
REPORTED (Rule 16); detail + IDs in ws3_alerting/literature_map.md. No own-system claim.

## 0. Governing reality (verdict-anchored)
- The "alert everyone nearby by IP address" idea is INFEASIBLE (feasibility_analysis.md): IPs are topological
  not geographic, NAT/CGNAT/mobile networks forbid unsolicited inbound, and "offline+by-IP" collapses to
  "devices already on my LAN running my app". The field solves last-mile warning by PROXIMITY BROADCAST +
  AUTHORITY-OPERATED CELLULAR BROADCAST, not addressing.
- No single channel is sufficient → a TIERED architecture (siren → local mesh/BLE → cellular broadcast →
  DTN backstop) with graceful degradation is the SOTA-consistent design.

## 1. Public-warning / cell broadcast (SOTA + limits)
Cell Broadcast / WEA / EU-Alert / India CAP (NDMA/SACHET) reach all phones in a cell with no internet and
change behavior at scale [2607.27584], but: payload length-limited (geo-polygon compression) [1509.05505];
air interface UNAUTHENTICATED/spoofable [2604.24404]; origination is an AUTHORITY function (private parties
likely cannot originate — UNVERIFIED, confirm vs ITU/3GPP/NDMA).

## 2. Short-range radio (measured, not marketing)
LoRa/Meshtastic ~2.47 km semi-open / ~600 m forest, tiered SF link budget to 180 dB [2605.20379; 2303.12754;
2605.17063]; BLE flood reaches off-the-shelf phones at 99.9% delivery [2002.12906] but BLE mesh is density/
interference-fragile [1910.03345; 2106.04230]; smart routing beats flooding [2510.03714]; mesh overlay extends
LoRaWAN [2512.00161]. GAPS: Zigbee, ESP-NOW, 802.11s stock-phone background reception.

## 3. Opportunistic / DTN
Phones-only store-carry-forward works when infrastructure is gone but is slow/lossy (68% / ~72 min)
[2601.00109; 2601.00148] → backstop, not fast-fire primary.

## 4. Effectiveness / fatigue (design-shaping)
Cry-wolf erodes compliance [1904.01963]; threshold systems over-alert + miss [2208.13027]; staggered
disclosure optimal (−70%/−89%) [2606.30320]; plain wording beats threats [2102.00589].

## 5. Simulation methodology
ns-3 LoRaWAN validated reference [2009.09503]; FAST-LoRa fast model w/ error bars [2507.23342]; mesh/routing
extensions [2512.00161; 2510.03714].

## 6. TARGETS section (for the build/sim — process targets, not results, Rule 16)
- Verdict on IP idea: DELIVERED (abandon as targeting; proximity + authority broadcast instead).
- Reach: characterize coverage vs distance/density per tier in ns-3, validated against [2009.09503;
  2605.17063]; HARDWARE-measure real ranges on the P6 BOM (P13).
- Reliability: target high delivery on owned tiers (siren ~100% in-range; mesh/BLE per source operating
  points) — MEASURED later, not claimed now.
- Latency: bound alert→device/siron latency per tier; validate vs BLE/LoRa sources.
- Security: signed + replay-protected alerts; cross-cell spoof flagging; jamming resilience tested in sim.
- Fatigue: precision gate + per-area false-alarm budget + staggered rollout.
- Close the GAPS: Zigbee/ESP-NOW/802.11s measurements; confirm India cell-broadcast regulatory path.

## 7. Honesty
Many capability numbers are source-reported and several are SIMULATION; owned-tier feasibility is strong for
siren/local-mesh/BLE, weaker (regulatory) for cellular broadcast; stock-phone BLE/Wi-Fi background reception
needs hardware verification. Nothing simulated or built.
