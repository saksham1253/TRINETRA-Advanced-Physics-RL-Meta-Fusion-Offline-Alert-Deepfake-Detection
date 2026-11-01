# ws3_alerting/literature_map.md — offline local-area alerting reading map (P12, WS3)

Phase P12 · RESEARCH-ONLY. 20 NEW primary arXiv papers (reader 717e5ad8; 11 fetches, web_search unused).
HONEST: all ABS; IDs subagent-reported, NOT independently re-fetched (residual risk, §0.5); all numbers
SOURCE-REPORTED ("not ours", Rule 16); several are SIMULATION (fading-model) not field — flagged. Framing:
PROGRAM/sota/P12_sota_scan.md. Running body-level deep FT NEW total UNCHANGED at 100 (ABS breadth).

## A. Cell broadcast / public warning / CAP
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2604.24404 | 5G PWS spoofing testbed + cross-cell verify | first open-source 5G PWS spoofing attack (OAI+SDR); phones "readily display spoofed alerts", NO air-interface origin auth; cross-cell corroboration flags single-source spoofs. ⇒ cell broadcast reaches unmodified phones but is UNAUTHENTICATED. |
| 1509.05505 | WEA geo-polygon compression | compress geo-target polygons into length-limited WEA; 9.7-23.6% of original (~80% reduction). ⇒ fine-grained fire-perimeter geo-fencing is payload-constrained. |

## B. Alert effectiveness / fatigue / false-alarm cost
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 1904.01963 | Cry-wolf evacuation game | repeated false alarms degrade compliance; announced drills + higher detection accuracy prevent large losses. |
| 2606.30320 | Hurricane evac info-design | optimal policy −89% social cost; staggered disclosure alone −70%; sharper info cuts false-alarm departures but synchronizes genuine ones. ⇒ STAGGERED/tiered rollout beats one simultaneous blast. |
| 2208.13027 | Debris-flow ML alerts (Taiwan) | existing rainfall-threshold system has many false alarms + misses; RF exposes explicit miss↔false-alarm trade-off. ⇒ document the operating point. |
| 2607.27584 | Michigan WEA thermostat response | one statewide WEA → −1.1°F avg thermostat; WEA "critical" to effective response. Population-scale behavior-change baseline. |
| 2102.00589 | Seven-Alerts wording (N=898) | plain "Basic Information" framing best; "Punishment" framing worst compliance. ⇒ wording matters. |

## C. Short-range radio — measured range / reliability
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2303.12754 | Forest LoRa 868 MHz body-UAV | ~600 m through foliage; log-distance+body-shadow model (−10 dB median PL error vs SOTA); severe Nakagami-m fading. ⇒ sub-km in vegetation, NOT datasheet km. |
| 2106.04230 | BLE mesh experimental (nRF52840) | latency-for-perfect-reliability sensitive to relay/advertising config; BT5 ext-adv helps. ⇒ needs careful tuning for life-safety. |
| 1910.03345 | BLE mesh reliability/delay/scalability | ~250 ms over 10 hops worst case; only 3 of 40 channels; WLAN-interference-vulnerable; broadcast-storm collapse at density. ⇒ dense fleeing crowd = stress case; cap hops/density. |
| 2002.12906 | BlueFlood concurrent-TX BT5 | 99.9% delivery @0.4% duty, 38 B @200 ms, 2 Mbps; "received by off-the-shelf smartphones". ⇒ candidate last-100-m to UNMODIFIED phones. |
| 2603.02105 | DAMCR multi-radio chaotic routing | PDR >95%, latency 17-23 ms even under jamming. SIMULATION (MATLAB fading), not field. |

## D. Opportunistic / delay-tolerant networking
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2601.00109 | Tsunami DTN (phones-only) | infrastructure gone → evacuees' phones store-carry-forward; Epidemic vs Prophet trade-offs. Fallback tier, high latency. |
| 2601.00148 | A-FC campus emergency DTN | ~68% delivery, avg delay 4311 s (~72 min), 1.68 hops. ⇒ DTN is a resilience BACKSTOP, NOT a fast-fire primary path. |

## E. Secure / authenticated broadcast + geo-fencing
Leans on 2604.24404 (unauthenticated air interface + cross-cell verification) + 1509.05505 (geo-polygon
payload). GAP: no dedicated geo-fenced authenticated-alert primary paper found within budget.

## F. Network simulation methodology + validation
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2009.09503 | ns-3 LoRaWAN experimental eval | PDR/throughput/sub-band vs device count & traffic, confirmed vs unconfirmed. Canonical ns-3 parameterization reference. |
| 2507.23342 | FAST-LoRa analytical framework | PDR MAE 0.940×10⁻², EE MAE 0.040 bits/mJ vs reference simulator, ~1000× faster. Fast design-space sweep with quantified error. |
| 2512.00161 | LIMA mesh over LoRaWAN | delivery ↑5×, scalability ↑8×, ED energy ↑12.6×, latency ↓2.3× vs single-hop (ns-3 + prototype confirms directionally). |

## G. Meshtastic / LoRa mesh deployments
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2605.20379 | Meshtastic smart-campus (SX1262, solar) | ~2.47 km link, RSSI −110 dBm, SNR +2.75 dB (n=62), no central operator. Realistic community fire-mesh backbone range. |
| 2605.17063 | Meshtastic preset link-budget (8 presets ×3 power) | SF7-8 fail @110-120 dB atten, SF9-10 @135-150 dB, SF11-12 up to 180 dB; SF12 demod to −18 dB SNR; fails within 2-4 dB of theoretical limit. ⇒ tiered link-budget dial. |
| 2510.03714 | Position/energy-aware LoRa mesh routing | +185% throughput, −75% energy vs optimized flooding under high traffic. ⇒ don't naive-flood a low-rate mesh. |

## Synthesis 1 — MEASURED RANGE / RELIABILITY (source-reported)
LoRa forest ~600 m (foliage/body shadow, Nakagami-m) [2303.12754]; Meshtastic ~2.47 km semi-open, −110 dBm/
+2.75 dB [2605.20379]; Meshtastic link budget SF7-8→120 dB … SF12→180 dB / −18 dB SNR [2605.17063]; BLE flood
99.9% delivery, reaches off-the-shelf phones [2002.12906]; BLE mesh ~250 ms/10 hops, 3/40 channels,
density/WLAN-fragile [1910.03345; 2106.04230]; Wi-Fi multi-radio PDR>95%/17-23 ms (SIM) [2603.02105]. GAPS:
Zigbee range, ESP-NOW range/PDR — NO primary paper in budget.

## Synthesis 2 — WHAT UNMODIFIED PHONES RECEIVE WITHOUT INTERNET
Cell broadcast/WEA: all phones in a cell, no app/internet, but UNAUTHENTICATED + length-limited [2604.24404;
1509.05505]; demonstrably changes behavior at scale [2607.27584]. BLE-advertising flood reaches off-the-shelf
phones at 99.9% delivery (background-scan dependent) [2002.12906]. DTN over phones ~68%/tens-of-minutes
[2601.00109; 2601.00148]. Stock-phone 802.11s Wi-Fi-mesh BACKGROUND reception = UNVERIFIED (phones generally
must join an SSID / open a page) → GAP.

## Synthesis 3 — ALERT-FATIGUE / FALSE-ALARM
Cry-wolf degrades compliance; drills + accuracy mitigate [1904.01963]; threshold systems over-alert + miss,
ML shifts the dial [2208.13027]; staggered disclosure optimal (−89%/−70%) [2606.30320]; plain wording beats
threats [2102.00589]. ⇒ detection PRECISION + staggered tiers + plain wording are as important as reach.

## Synthesis 4 — SIMULATION-PARAMETER SOURCES (ns-3-ready)
Forest LoRa log-distance + body-shadow + Nakagami-m, ~600 m [2303.12754]; Meshtastic SF link-budget thresholds
[2605.17063]; RSSI/SNR @2.47 km point [2605.20379]; ns-3 LoRaWAN PDR/throughput vs load + duty-cycle sub-band
[2009.09503]; FAST-LoRa fast model w/ error bars [2507.23342]; mesh gains 5×/8×/12.6×/2.3× [2512.00161];
routing vs flooding +185%/−75% [2510.03714]; BLE mesh 250 ms/10 hops, 3/40 channels [1910.03345]; BlueFlood
99.9%/0.4% duty/38 B/200 ms [2002.12906]; multi-radio PDR>95%/17-23 ms [2603.02105]; DTN 68%/4311 s/1.68 hops
[2601.00148].

## REGULATORY REALITY (honest, partly UNVERIFIED)
Sources frame cell-broadcast/WEA origination as an AUTHORITY function, and show the air interface is
UNAUTHENTICATED (rogue SDR can spoof) [2604.24404]. NOT verifiable from primary arXiv (flagged UNVERIFIED,
confirm vs ITU/3GPP/NDMA/FCC): (a) that only authorized agencies may ORIGINATE WEA/cell broadcast; (b) that
India's CAP/cell-broadcast path (NDMA / C-DOT SACHET) is government-operated. Practical conclusion (to verify):
a private fire-detection project CANNOT itself originate WEA/cell broadcast and must either use the short-
range/LoRa-mesh/BLE tiers it owns OR request an official alert from an authorized agency.

## Tally
P12 NEW quota = 20 primary arXiv (≥15 MET; ~40 stretch not reached under throttle+no-web_search — disclosed).
Depth all ABS (0 FT). GAPS flagged: Zigbee/ESP-NOW range, 802.11s stock-phone background reception, dedicated
geo-fenced-auth paper, India regulatory specifics.