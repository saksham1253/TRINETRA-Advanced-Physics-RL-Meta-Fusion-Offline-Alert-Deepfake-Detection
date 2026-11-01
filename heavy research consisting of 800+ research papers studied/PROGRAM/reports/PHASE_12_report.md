# PHASE_12_report — WS3 OFFLINE LOCAL-AREA ALERTING (RESEARCH-ONLY)

Phase P12 (MASTER_PROMPT L588). Status: COMPLETE to gate (continuous mode — completion record, not a halt).
Nothing simulated or built (Rule 16). Rule 19: high-stakes alerts human-gated.

## Objective
Settle the "IP address" idea honestly and design a feasible tiered offline alerting architecture with a
simulation specification.

## Verdict on the original wish (task 2)
Using IP addresses to reach "everyone near a fire" is INFEASIBLE and abandoned as a targeting mechanism: IPs
are TOPOLOGICAL not geographic; NAT/DHCP/CGNAT/mobile networks forbid unsolicited inbound to a stranger's
phone; "offline + by IP" collapses to "devices already on my LAN running my app". The feasible path is alert
by PHYSICAL PROXIMITY (local radio/mesh/siren) + AUTHORITY-OPERATED cellular broadcast.

## What was produced
- PROGRAM/sota/P12_sota_scan.md — disaster-comms SOTA + a targets section.
- ws3_alerting/feasibility_analysis.md — the verdict + full networking reasoning (NAT/CGNAT/IPv6/VPN/geo-IP).
- ws3_alerting/architecture.md — tiered graceful-degradation design: Tier 1 siren/strobe/PA (always, no
  device) · Tier 2 local LAN + LoRa/Meshtastic mesh + BLE flood to opt-in/off-the-shelf phones · Tier 3
  cellular broadcast/WEA/CAP (authority-operated) · Tier 0 DTN backstop; a detection-confidence→tier decision
  policy with human oversight (Rule 19) and alert-fatigue controls.
- ws3_alerting/threat_model.md — spoof/replay/fatigue/DoS/jamming/insider/key-mgmt/registry-privacy, using
  P9/P10 anomaly findings; signed + replay-protected alerts; cross-cell spoof flagging.
- ws3_alerting/simulation_spec.md — ns-3 (+FAST-LoRa) spec, SOURCED parameters, validation approach; nothing
  simulated now.
- ws3_alerting/literature_map.md — 20 NEW primary arXiv (ABS, families A-G) + 4 synthesis lists + regulatory
  reality.
- DATASETS.md D89-D94 [D] alerting/network candidates; 20 [P12] ledger rows; Audit #19 PASS.

## Key source-reported findings (Rule 16)
- Cell broadcast/WEA reaches unmodified phones + changes behavior at scale (Michigan −1.1°F, 2607.27584) but
  is UNAUTHENTICATED/spoofable (2604.24404) and payload-constrained (1509.05505); origination is an AUTHORITY
  function (private party likely cannot — UNVERIFIED).
- Owned radio tiers (source-reported): Meshtastic ~2.47 km semi-open / ~600 m forest, SF link budget to 180
  dB (2605.20379/2303.12754/2605.17063); BLE flood 99.9% delivery reaching off-the-shelf phones (2002.12906)
  but BLE mesh density/interference-fragile (1910.03345); smart routing >> flooding (2510.03714).
- DTN is a slow/lossy backstop (68%/~72 min, 2601.00148), not a fast-fire primary path.
- Fatigue: cry-wolf erodes compliance (1904.01963); staggered rollout optimal (−70%/−89%, 2606.30320); plain
  wording beats threats (2102.00589) → precision + staggered tiers + plain wording matter as much as reach.

## Honesty & limits (§0.5)
QUOTA 20 (≥15 MET; ~40 stretch not reached under throttle+no-web_search — disclosed). ALL ABS; IDs subagent-
reported, not re-fetched; several numbers are SIMULATION. GAPS: Zigbee + ESP-NOW range/PDR, 802.11s stock-
phone background reception, dedicated geo-fenced-auth paper, and India NDMA/C-DOT SACHET regulatory specifics
— all TO-VERIFY (hardware in P13 / standards docs). No real "alert reachability" trace corpus exists.

## Open actions carried
Confirm India cell-broadcast/CAP regulatory path + private-party rules; hardware-measure Zigbee/ESP-NOW/
real BOM radio ranges + stock-phone BLE/Wi-Fi background reception (P13); run the ns-3 simulation per the spec.

## Gate
PROGRAM/gate_messages/PHASE_12_gate.md. Auto-proceeding to P13 (WS7b IoT design & build manual).
