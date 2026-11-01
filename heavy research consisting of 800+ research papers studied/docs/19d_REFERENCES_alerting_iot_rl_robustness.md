# 19d_REFERENCES_alerting_iot_rl_robustness -- TRINETRA reference catalogue (part of chapter 19)

> Row-level truth: `analysis/02_paper_ledger.csv`. Index, counts, MUST-READ TOP-30, dataset cross-index and BibTeX live in `docs/19_REFERENCES_FULL.md`.

> **Residual-identifier risk (per _CANON SS7):** every identifier below is a real ledger row, but identifiers were *subagent-reported during a web_search outage and were NOT independently re-fetched this pass*. No entry claims a resolved identifier unless its Verification line says so.

> Read-depth tags are copied verbatim from the ledger: FT / FT-PARTIAL / ABS / ABS-CANONICAL / FT-REF.


---

## Theme: Alerting / networks / DTN / LoRa / IoT / deployment  (`REF-ALERT-*`, 86 entries)

_Primary consumer: WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11. The ledger axis/WS code that mapped each paper into this theme is printed per entry for traceability._

#### REF-ALERT-001 | 2508.15058
- arXiv/DOI: arXiv:2508.15058
- Authors: Lin; Alouini
- Title: Toward Sustainable Subterranean mMTC: Space-Air-Ground-Underground Networks Powered by LoRaWAN and WET
- Year / Venue: 2025 / IEEE WCM (submitted)
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: LoRaWAN SF/airtime/energy under harsh coverage
- Takeaway for TRINETRA: Space-Air-Ground-Underground integrated net using LoRaWAN + wireless energy transfer for remote/disaster/hard-to-reach monitoring; simulations show spread-factor (SF) choice, reporting period, and time-allocation critically determine covera...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-002 | 2311.01743
- arXiv/DOI: arXiv:2311.01743
- Authors: Lin; Ullah; Alves; Mikhaylov; Hao
- Title: Energy Efficiency Optimization for Subterranean LoRaWAN Using RL (Direct-to-Satellite)
- Year / Venue: 2023 / IEEE WCL
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: co-SF interference + RL SF allocation
- Takeaway for TRINETRA: In DENSE LoRaWAN, assigning quasi-orthogonal spreading factors to minimise co-SF interference is hard; multi-agent RL (MAD3QN/MAA2C) allocates SFs for energy efficiency, beating 4 benchmarks.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-003 | 1906.02998
- arXiv/DOI: arXiv:1906.02998
- Authors: Pietrosemoli; Rainone; Zennaro
- Title: On Extending the Wireless Communications Range of Weather Stations using LoRaWAN
- Year / Venue: 2019 / arXiv (cs.NI)
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: low-cost LoRaWAN weather relay, dev-country
- Takeaway for TRINETRA: Low-cost/low-power device decodes consumer weather-station data and relays it over LoRaWAN, extending ~100 m range for disaster prevention in developing countries (ICTP/ITU).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-004 | 1511.08331
- arXiv/DOI: arXiv:1511.08331
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Value of Information Aware Opportunistic Duty Cycling in Solar Harvesting Sensor Networks
- Year / Venue: 2015 / arXiv (cs.NI)
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: VoI-driven duty cycling under stochastic harvested energy
- Takeaway for TRINETRA: Solar-harvested WSNs cannot sustain FULL duty cycle on limited harvested energy, so they must operate at PARTIAL duty cycle and prioritise high-Value-of-Information data; the paper maps this to a budget-dynamic Multi-Arm Bandit over samplin...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-005 | 2303.09750
- arXiv/DOI: arXiv:2303.09750
- Authors: Jabini; Johnson
- Title: Measurement Optimization under Uncertainty using Deep Reinforcement Learning
- Year / Venue: 2023 / arXiv (eess.SY)
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: RL sensor placement maximising info gain
- Takeaway for TRINETRA: Deterministic optimal-sensor-placement is insufficient under input/parameter uncertainty; formulates placement as an MDP where an RL agent places heterogeneous sensors to maximise an information-theoretic reward, demonstrated on a shear-bui...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-006 | 2303.00028
- arXiv/DOI: arXiv:2303.00028
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Efficient Sensor Placement from Regression with Sparse Gaussian Processes in Continuous and Discrete Spaces
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: scalable GP mutual-information sensor placement
- Takeaway for TRINETRA: Classic MI-based sensor placement requires discretising the environment (cost scales with grid size), limiting scale; proposes a sparse-GP variational formulation optimisable by gradient descent in continuous domains, scaling to large probl...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-007 | 1010.4385
- arXiv/DOI: arXiv:1010.4385
- Authors: Hernandez; Baumgartner; Blesa; Blum; Kroller; Fekete
- Title: A Protocol for Self-Synchronized Duty-Cycling in Sensor Networks (Wiselib)
- Year / Venue: 2010 / MSN 2010
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: self-synchronized robust duty-cycling
- Takeaway for TRINETRA: Self-synchronized duty-cycling protocol for energy-harvesting WSNs (Wiselib/Shawn, real iSense hardware specs); adapts to changing energy availability and is robust against packet loss.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-008 | 2603.15945
- arXiv/DOI: arXiv:2603.15945
- Authors: Cao; Radenkovic
- Title: Evaluating Opportunistic Routing Protocols in a Disaster Scenario (DTN Earthquake Case Study)
- Year / Venue: 2026 / arXiv (cs.NI)
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: Epidemic vs Spray-and-Wait DTN, SnW better balance
- Takeaway for TRINETRA: Evaluates DTN opportunistic routing in a realistic disaster (2016 Central Italy earthquake, stadium evacuation) with mobile+static nodes (crowd, responders, sensors, vehicles) in a PARTIALLY-CONNECTED environment; compares Epidemic vs Spray...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-009 | 1903.02611
- arXiv/DOI: arXiv:1903.02611
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: HRSON: Home-based Routing for Smartphones in Opportunistic Networks
- Year / Venue: 2019 / arXiv (cs.NI)
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: zero-knowledge DTN routing on non-ad-hoc smartphones
- Takeaway for TRINETRA: Opportunistic (delay-tolerant) networks keep connectivity with limited infrastructure (e.g.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-010 | 2312.08387
- arXiv/DOI: arXiv:2312.08387
- Authors: Lopez Escobar; Gil-Castineira; Diaz-Redondo
- Title: JMAC Protocol: A Cross-Layer Multi-Hop Protocol for LoRa
- Year / Venue: 2020 / Sensors (MDPI) vol20 6893
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: multi-hop LoRa mesh, predictive wake-up, long node lifetime
- Takeaway for TRINETRA: LPWAN connectivity fails in non-line-of-sight / poor-coverage areas; JMAC is a cross-layer MULTI-HOP protocol for LoRa that exploits mesh behaviour to extend coverage and raise supported-device count per cell, using PREDICTIVE WAKE-UP for l...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-011 | 2507.07841
- arXiv/DOI: arXiv:2507.07841
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: HaLert: A Resilient Smart City Architecture for Post-Disaster Based on Wi-Fi HaLow Mesh and SDN
- Year / Venue: 2025 / arXiv (cs.NI)
- Read depth: ABS | local note: yes | ledger axis/WS: A10 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: post-disaster comms reuse via HaLow mesh + SDN
- Takeaway for TRINETRA: Disasters are unpredictable, so reusing existing infrastructure for alternative post-disaster communication is essential to keep populations able to receive authority alerts; proposes HaLert, reusing dense distributed IoT via a Wi-Fi HaLow...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-012 | 2602.24209
- arXiv/DOI: arXiv:2602.24209
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: An Efficient Unsupervised Federated Learning Approach for Anomaly Detection in Heterogeneous IoT Networks
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: unsupervised FL anomaly detection for HETEROGENEOUS IoT, no raw-data transmission
- Takeaway for TRINETRA: Federated learning for IoT keeps diverse-device data LOCAL while contributing to a shared global model, inherently preserving privacy and avoiding raw-data transmission; tackles the HETEROGENEITY of IoT data (device capability, format, comm...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-013 | 10.1145/3485730.3493444
- arXiv/DOI: DOI:10.1145/3485730.3493444
- Authors: Zhang; He; Ma; Gao; Ma; Avestimehr
- Title: FedIoT: Federated Learning for Internet of Things
- Year / Venue: 2021 / ACM SenSys 2021
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: federated anomaly detection benchmark for resource-constrained IoT; affordable on-device
- Takeaway for TRINETRA: Federated-learning framework/benchmark (FedIoT) for anomaly detection on resource-constrained IoT devices, shown affordable and promising for on-device training; open source (FedML-AI/FedIoT).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-014 | 1408.0104
- arXiv/DOI: arXiv:1408.0104
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Impact of Human Behavior on Social Opportunistic Forwarding
- Year / Venue: 2014 / arXiv (cs.NI)
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: DTN opportunistic forwarding under long delays/partitions; human-mobility-driven delivery
- Takeaway for TRINETRA: Delay-tolerant networking via OPPORTUNISTIC message forwarding for environments with very long delays + frequent network PARTITIONS (disaster areas, development regions), with limited end-to-end connectivity + node resources; studies how hu...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-015 | 1809.04324
- arXiv/DOI: arXiv:1809.04324
- Authors: Bhatia; Tomic; McCann
- Title: LPWA-MAC: a Low Power Wide Area network MAC protocol for cyber-physical systems
- Year / Venue: 2018 / ACM BuildSys
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: LoRa MAC / bounded delay
- Takeaway for TRINETRA: LPWAN MAC giving bounded end-to-end delay + high channel utility for CPS control (vs delay-tolerant monitoring). Relevant to TRINETRA alarm-grade latency guarantees over LoRa, beyond best-effort; informs Bug #6/#8 comms realism.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-016 | 2507.08677
- arXiv/DOI: arXiv:2507.08677
- Authors: dos Reis Bezerra; et al.
- Title: Qualitative Assessment of Low Power Wide Area Network Protocols and their Security Aspect
- Year / Venue: 2025 / arXiv (cs.NI)
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: LoRa protocol/security
- Takeaway for TRINETRA: Compares LoRaWAN/NB-IoT/Sigfox incl. security; LoRaWAN best for sparse long-battery-life sensor nets. Supports LoRaWAN choice but flags security surface -> ties to Proxy credential-leak Bug #12 (comms security hygiene).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-017 | 1308.2907
- arXiv/DOI: arXiv:1308.2907
- Authors: Li; Bartos
- Title: A Survey of Protocols for Intermittently Connected Delay-Tolerant Wireless Sensor Networks
- Year / Venue: 2013 / arXiv (cs.NI)
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: DTN / store-and-forward
- Takeaway for TRINETRA: Survey of ICDT-WSN protocols: WSN+DTN hybrid for intermittently connected sensor nets; store-carry-forward.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-018 | 2409.20408
- arXiv/DOI: arXiv:2409.20408
- Authors: Al Mojamed
- Title: Beacon-based uplink transmission for LoRaWAN direct-to-satellite IoT
- Year / Venue: 2024 / IJCNC
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: LoRa-to-satellite backhaul
- Takeaway for TRINETRA: Class-B-synchronized uplink from ground LoRaWAN devices to LEO satellite gateways; ~2x traffic vs standard.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-019 | 1703.01985
- arXiv/DOI: arXiv:1703.01985
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: D2D Communications in LoRaWAN LPWAN: From Idea to Empirical Validation
- Year / Venue: 2017 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: LoRa device-to-device
- Takeaway for TRINETRA: Device-to-device over LoRaWAN LPWAN, empirically validated. Supports TRINETRA node-to-node relaying when gateway unreachable (mesh/relay robustness for offline-first design, #6/#8).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-020 | 1803.00275
- arXiv/DOI: arXiv:1803.00275
- Authors: Islam; Lagutin; Lukyanenko; Gurtov; Yla-Jaaski
- Title: CIDOR: Content Distribution and Retrieval in Disaster Networks for Public Protection
- Year / Venue: 2018 / IEEE WiMob
- Read depth: ABS | local note: no | ledger axis/WS: A10 | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: ICN+DTN disaster comms
- Takeaway for TRINETRA: Information-Centric Networking over DTN for disaster comms; retrieves content by name regardless of location; cuts retrieval time ~50%, response ~100%.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-021 | 1509.05505
- arXiv/DOI: arXiv:1509.05505
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Small Polygon Compression For Integer Coordinates
- Year / Venue: 2015 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] WEA geo-polygon payload compression
- Takeaway for TRINETRA: Src-reported compresses geo-target polygons to 9.7-23.6% of original (~80% reduction) within phone limits. Fine-grained geo-fencing is payload-constrained. Source-reported. NEW. literature_map A.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-022 | 1904.01963
- arXiv/DOI: arXiv:1904.01963
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: The Cry Wolf Effect in Evacuation: a Game-Theoretic Approach
- Year / Venue: 2019 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] repeated false alarms degrade compliance; drills+accuracy mitigate
- Takeaway for TRINETRA: Bayesian evac game; src-reported qualitative: announced drills + higher detection accuracy prevent large efficiency losses. Source-reported. NEW. literature_map B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-023 | 2606.30320
- arXiv/DOI: arXiv:2606.30320
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Continuous-Time Information Design for Hurricane Evacuation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] staggered disclosure optimal: -89% social cost / -70% staggering alone
- Takeaway for TRINETRA: Stackelberg info-design, Hurricane Rita calibration; src-reported sharper info cuts false-alarm departures but synchronizes genuine ones -> stagger. Supports tiered rollout. Source-reported. NEW. literature_map B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-024 | 2208.13027
- arXiv/DOI: arXiv:2208.13027
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Improving debris flow evacuation alerts in Taiwan using machine learning
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] threshold systems over-alert + miss; ML shifts miss/false-alarm dial
- Takeaway for TRINETRA: Src-reported RF outperforms rainfall-threshold system which generates many false alarms and misses real events. Document the operating point. Source-reported. NEW. literature_map B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-025 | 2607.27584
- arXiv/DOI: arXiv:2607.27584
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Who heeds the call to conserve in an energy emergency? (smart thermostat WEA)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] WEA changes behavior at population scale (-1.1F thermostat)
- Takeaway for TRINETRA: Diff-in-diff on 2019 Michigan statewide WEA; src-reported households cut 1.1F avg; WEA critical to effective response. Compliance baseline. Source-reported. NEW. literature_map B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-026 | 2102.00589
- arXiv/DOI: arXiv:2102.00589
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Tale of Seven Alerts: Enhancing WEAs to Reduce Cellular Network Usage
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] plain Basic-Information wording best; Punishment framing worst compliance
- Takeaway for TRINETRA: Between-subjects survey N=898, 7 framings; src-reported Basic Info largest data-use reduction, Punishment lowest compliance. Wording matters. Source-reported. NEW. literature_map B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-027 | 2303.12754
- arXiv/DOI: arXiv:2303.12754
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Body-UAV Near-Ground LoRa Links through a Mediterranean Forest
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] forest LoRa ~600 m; log-distance+body-shadow path-loss model
- Takeaway for TRINETRA: Src-reported ~600 m through foliage, -10 dB median PL error vs SOTA, severe Nakagami-m fading. Sub-km in vegetation; sim parameterization. Source-reported. NEW. literature_map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-028 | 2106.04230
- arXiv/DOI: arXiv:2106.04230
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Demystifying the Performance of Bluetooth Mesh
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] BLE mesh reliability needs careful relay/advertising tuning
- Takeaway for TRINETRA: nRF52840 experiments; src-reported latency-for-perfect-reliability sensitive to config, BT5 ext-adv helps. Out-of-box not reliability-grade. Source-reported. NEW. literature_map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-029 | 1910.03345
- arXiv/DOI: arXiv:1910.03345
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Understanding the Performance of Bluetooth Mesh
- Year / Venue: 2019 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] BLE mesh ~250 ms/10 hops, 3/40 channels, broadcast-storm at density
- Takeaway for TRINETRA: Sim sweeps + real WLAN interference; src-reported density/interference collapse. Dense fleeing crowd = stress case; cap hops. Source-reported. NEW. literature_map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-030 | 2002.12906
- arXiv/DOI: arXiv:2002.12906
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: BlueFlood: Concurrent Transmissions for Multi-Hop Bluetooth 5
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] BLE flood 99.9% delivery, reaches off-the-shelf smartphones
- Takeaway for TRINETRA: Src-reported 99.9% delivery @0.4% duty, 38 B, 200 ms, 2 Mbps; received by off-the-shelf devices. Candidate last-100-m to unmodified phones. Source-reported. NEW. literature_map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-031 | 2603.02105
- arXiv/DOI: arXiv:2603.02105
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Resilient Chaotic Cross-Layer Routing for Smart Grid IoT (DAMCR)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] multi-radio FHSS PDR>95%, 17-23 ms under jamming (SIMULATION)
- Takeaway for TRINETRA: MATLAB sim AWGN/Rayleigh/Rician+jamming; src-reported PDR>95%, latency 17-23 ms. Jamming resilience; SIM not field. Source-reported. NEW. literature_map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-032 | 2601.00109
- arXiv/DOI: arXiv:2601.00109
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Delay-Tolerant Networking for Tsunami Evacuation (Epidemic vs Prophet)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] phones-only store-carry-forward when infrastructure gone
- Takeaway for TRINETRA: DTN sim; src-reported trade-offs Epidemic vs Prophet. Fallback tier, high latency. Source-reported. NEW. literature_map D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-033 | 2601.00148
- arXiv/DOI: arXiv:2601.00148
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A-FC: Activity-Based Delay Tolerant Routing for Campus Emergency
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] DTN ~68% delivery, ~72 min delay, 1.68 hops -> backstop not primary
- Takeaway for TRINETRA: Routes to high-activity nodes; src-reported 68% delivery, 4311 s delay. DTN is resilience backstop, not fast-fire path. Source-reported. NEW. literature_map D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-034 | 2009.09503
- arXiv/DOI: arXiv:2009.09503
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Experimental Evaluation of LoRaWAN in NS-3
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] canonical validated ns-3 LoRaWAN setup (PDR/throughput vs load)
- Takeaway for TRINETRA: Src-reported PDR/throughput/sub-band curves vs device count/traffic, confirmed vs unconfirmed. Sim parameterization reference. Source-reported. NEW. literature_map F.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-035 | 2507.23342
- arXiv/DOI: arXiv:2507.23342
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FAST-LoRa: Efficient Simulation Framework for LoRaWAN
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] fast analytical LoRaWAN model, quantified error vs reference sim
- Takeaway for TRINETRA: Src-reported PDR MAE 0.940e-2, EE MAE 0.040 bits/mJ, ~1000x faster. Fast design-space sweep. Source-reported. NEW. literature_map F.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-036 | 2512.00161
- arXiv/DOI: arXiv:2512.00161
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Mesh Augmentation of LoRaWAN-based IoT Networks (LIMA)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] mesh overlay delivery 5x/scalability 8x/energy 12.6x/latency 2.3x vs single-hop
- Takeaway for TRINETRA: ns-3 + prototype confirms directionally; LoRaWAN-compatible multi-hop. Extends off-grid coverage/battery. Source-reported. NEW. literature_map F.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-037 | 2605.20379
- arXiv/DOI: arXiv:2605.20379
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A Meshtastic-based LoRa Mesh System for Smart Campus
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] Meshtastic ~2.47 km, RSSI -110 dBm, SNR +2.75 dB, no operator
- Takeaway for TRINETRA: Real SX1262/solar deployment; src-reported n=62 packets. Realistic community fire-mesh backbone range. Source-reported. NEW. literature_map G.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-038 | 2605.17063
- arXiv/DOI: arXiv:2605.17063
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Resilience Analysis in Off-Grid LoRa Mesh Networks (Meshtastic presets)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] SF link budget: SF7-8 120dB ... SF12 180dB / -18 dB SNR
- Takeaway for TRINETRA: Guided-link characterization 8 presets x3 power; src-reported fails within 2-4 dB of theoretical limit. Tiered link-budget dial. Source-reported. NEW. literature_map G.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-039 | 2510.03714
- arXiv/DOI: arXiv:2510.03714
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Position- and Energy-Aware Routing for Subterranean LoRa Mesh
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P12
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P12] smart routing +185% throughput / -75% energy vs flooding
- Takeaway for TRINETRA: Src-reported under high traffic, ALOHA MAC + duty-cycle limits. Don't naive-flood a low-rate mesh. Source-reported. NEW. literature_map G.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-040 | 1912.06384
- arXiv/DOI: arXiv:1912.06384
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Low-Cost Outdoor Air Quality Monitoring and Sensor Calibration: Survey
- Year / Venue: 2019 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T1
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T1] canonical cheap-sensor failure modes: cross-sensitivity, T/RH coupling, drift
- Takeaway for TRINETRA: Survey; src-reported periodic ML re-cal mitigates. Checklist for CALIBRATION_PROTOCOL. Source-reported. NEW. literature_map P13-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-041 | 1805.11999
- arXiv/DOI: arXiv:1805.11999
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Reference-free Calibration in Sensor Networks
- Year / Venue: 2018 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T1
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T1] unbiased cross-calibration without a trusted reference node
- Takeaway for TRINETRA: Src-reported estimators reach derived lower bounds, beat prevalent algos on real data. Field of nodes cross-calibrates. Source-reported. NEW. literature_map P13-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-042 | 2112.09072
- arXiv/DOI: arXiv:2112.09072
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Sampling Trade-Offs in Duty-Cycled Systems for AQ Low-Cost Sensors
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T1
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T1] duty-cycle 0.1 (resp ~2 min)/0.01-0.02 (fast) retains calibrated quality
- Takeaway for TRINETRA: Src-reported vs mains node, calibrating to hourly references. Couples power budget to accuracy. Source-reported. NEW. literature_map P13-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-043 | 2510.05646
- arXiv/DOI: arXiv:2510.05646
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Geographically Weighted Regression for AQ Low-Cost Sensor Calibration
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T1
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T1] GWR = lightweight per-location gain/offset post-install
- Takeaway for TRINETRA: SensEURCity Antwerp (D96); src-reported spatial NO2 correction coefficients. Deployable regression recipe. Source-reported. NEW. literature_map P13-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-044 | 2508.02724
- arXiv/DOI: arXiv:2508.02724
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Veli: Unsupervised Method and Unified Benchmark for AQ Sensor Correction
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T1/T6] reference-free variational Bayes, absorbs drift + faulty sensors
- Takeaway for TRINETRA: AQ-SDR benchmark (D95); src-reported strong in/OOD generalization, no co-location. Addresses drift + fault together. Source-reported. NEW. literature_map P13-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-045 | 1708.08750
- arXiv/DOI: arXiv:1708.08750
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Multi-Stage Feature Selection Classifier for Incipient Stage Fire in Building
- Year / Venue: 2017 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T2
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T2] CLOSEST match: gas+dust+T/RH e-nose fire classifier
- Takeaway for TRINETRA: Feature-select -> PCA -> PCA-PNN; src-reported robust regardless of T/RH, drift, concentration. Our Type A comparator. Source-reported. NEW. literature_map P13-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-046 | 2407.09117
- arXiv/DOI: arXiv:2407.09117
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Assessing the Efficacy of IoT-based Forest Fire Detection: Practical Use Case
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T2
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T2] real distributed low-cost fire nodes (SEA-HAZEMON) field reality-check
- Takeaway for TRINETRA: Src-reported preliminary efficacy + design guidelines (D97). Field-methodology baseline. Source-reported. NEW. literature_map P13-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-047 | 2203.05492
- arXiv/DOI: arXiv:2203.05492
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: An Empirical Study of Low Precision Quantization for TinyML
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T3
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T3] sub-8-bit PTQ pipeline guidance, small calibration set, no retraining
- Takeaway for TRINETRA: Src-reported component-level PTQ design choices across tinyML. Shrink a classifier without retraining data. Source-reported. NEW. literature_map P13-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-048 | 2103.06231
- arXiv/DOI: arXiv:2103.06231
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Quantization-Guided Training for Compact TinyML Models
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T3
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T3] 81 KB model @2-bit, 17.7x smaller, -3% acc
- Takeaway for TRINETRA: QGT regularization; src-reported person-detection. 2-bit reachable only WITH QGT; footprint in ESP32 range. Source-reported. NEW. literature_map P13-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-049 | 2110.10486
- arXiv/DOI: arXiv:2110.10486
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A TinyML Platform for On-Device Continual Learning with Quantized Latent Replays
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T3
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T3] 8-bit latent replay near-lossless (-0.26%), 4x less memory
- Takeaway for TRINETRA: vs STM32-L4 baseline (65x faster/37x more efficient on 22nm proto); src-reported. 8-bit near-lossless default. Source-reported. NEW. literature_map P13-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-050 | 2412.09289
- arXiv/DOI: arXiv:2412.09289
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Optimising TinyML with Quantization + Distillation of Transformer/Mamba for Edge
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T3
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T3] quantized transformer fits 64 KB RAM; Mamba fits 32 KB uncompressed
- Takeaway for TRINETRA: Src-reported indoor-localization. RAM-budgeted model choice for ESP32 SRAM. Source-reported. NEW. literature_map P13-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-051 | 2604.23012
- arXiv/DOI: arXiv:2604.23012
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: On-Device Vision Training/Inference on a Thumb-Sized Microcontroller
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T3/T4] ESP32-S3 on-device: 3-class 64x64 ~9 min train, 6.3 FPS inference
- Takeaway for TRINETRA: PSRAM-aware memory + 3-tier boot weight resolution, ~1750 LOC dependency-free C++; src-reported. Exact-target firmware/memory patterns. Source-reported. NEW. literature_map P13-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-052 | 2607.23220
- arXiv/DOI: arXiv:2607.23220
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Embedded Firmware for Flight Control/Telemetry/Video on ESP32-S3
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T4
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T4] core-separate sensing vs comms, static scheduling, zero-copy IPC
- Takeaway for TRINETRA: 400 Hz control / 50 Hz telemetry dual-core; src-reported jitter-free determinism. Keep sampling deterministic under Wi-Fi/LoRa. Source-reported. NEW. literature_map P13-T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-053 | 2601.03867
- arXiv/DOI: arXiv:2601.03867
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Systems-Engineered ESP32 DAQ + FAIR Workflow for Tropical Field Measurement
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: n/r
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T4/T5] state-machine faults + NTP + local-first SD + env hardening, >90% completeness KPI
- Takeaway for TRINETRA: V-model + FAIR; src-reported 6-month campaign target. Near-complete reliability + field playbook. Source-reported. NEW. literature_map P13-T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-054 | 2003.08647
- arXiv/DOI: arXiv:2003.08647
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: LoRa in the Field: Networking Smart City Hamburg with RIOT
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T5
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T5] field-trial methodology + honest limitation reporting
- Takeaway for TRINETRA: Src-reported LoRaWAN suitable across smart-city use cases w/ identified weaknesses. Field-test methodology template. Source-reported. NEW. literature_map P13-T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-055 | 1301.4795
- arXiv/DOI: arXiv:1301.4795
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Model Selection Approach for Distributed Fault Detection in WSNs
- Year / Venue: 2013 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T6
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T6] BMA to flag faulty sensors, suppress single-bad-sensor false alarms
- Takeaway for TRINETRA: Folds error probabilities into event detection; src-reported averaged predictive error over fault sets. Ties P10 edge spec. Source-reported. NEW. literature_map P13-T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-056 | 2412.01609
- arXiv/DOI: arXiv:2412.01609
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Optimizing LoRa for Edge Computing with TinyML Channel Hopping
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T7
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T7] measures RSSI/SNR/packet-loss; TinyML hopping +63% RSSI/+44% SNR
- Takeaway for TRINETRA: Src-reported vs random hopping. Measurement methodology + MCU-runnable uplink optimization. Source-reported. NEW. literature_map P13-T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-057 | 2509.23125
- arXiv/DOI: arXiv:2509.23125
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Impact of Environmental Factors on LoRa 2.4 GHz ToF Ranging Outdoors
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7b | phase: P13-T7
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P13-T7] T/RH significantly affect ranging -> compensate even the radio
- Takeaway for TRINETRA: 3x3 grid/400 m2/3 weeks + T/RH (D98); src-reported. Multi-week gridded field-measurement template. Source-reported. NEW. literature_map P13-T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-058 | 2401.13744
- arXiv/DOI: arXiv:2401.13744
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Conformal Prediction Sets Improve Human Decision Making
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS3 | phase: P17-T5
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P17-T5] RCT: conformal sets raise operator accuracy vs fixed-size sets
- Takeaway for TRINETRA: FEATURES F-22 Wave-2; src-reported. Operator-explainability UI (Rule 19 advisory). Source-reported. NEW. P17_scout_notes T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-059 | 2506.09186
- arXiv/DOI: arXiv:2506.09186
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Not All Those Who Drift Are Lost: GP Drift Correction + Calibration Scheduling
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7 | phase: P17-T6
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P17-T6] GP sensor-response model + uncertainty-driven schedule; MSE -up to 90% (avg >20%)
- Takeaway for TRINETRA: FEATURES F-15 Wave-1; src-reported. IoT sensor drift compensation + adaptive recalibration. Source-reported. NEW. P17_scout_notes T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-060 | 1707.03682
- arXiv/DOI: arXiv:1707.03682
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PRNet: Blind Drift Calibration of Sensor Networks
- Year / Venue: 2017 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7 | phase: P17-T6
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P17-T6] project drifted data + CNN recovers drift-free, no ground truth; 2x more sensors at 80% recovery
- Takeaway for TRINETRA: FEATURES F-15 Wave-1; src-reported. RISK assumes neighbor redundancy, fails on sparse nodes. Source-reported. NEW. P17_scout_notes T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-061 | 2406.17488
- arXiv/DOI: arXiv:2406.17488
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Environmental Variation or Instrumental Drift? Probabilistic Gas-Sensor Drift Modeling
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7 | phase: P18-E
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P18-E] importance-sampling separates instrumental drift from environmental variation (NDIR CO2)
- Takeaway for TRINETRA: F-15 spec THE pitfall; src-reported ignoring env distorts drift estimate. Decompose before recalibration. Source-reported. NEW. P18 lit map E.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-062 | 2310.18118
- arXiv/DOI: arXiv:2310.18118
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Global Multi-Unit Calibration for Large-Scale IoT Particulate Matter Monitoring
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS7 | phase: P18-E
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P18-E] zero-transfer-sample global law from few co-located units applied to all units
- Takeaway for TRINETRA: F-15 spec scheduling-cost; src-reported matches per-unit SOTA. RISK one-law assumes bounded fab variance; outlier unit mis-corrected. Source-reported. NEW. P18 lit map E.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-063 | 2501.06007
- arXiv/DOI: arXiv:2501.06007
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: CoNOAir: Neural Operator for Forecasting Carbon Monoxide in Cities
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T1
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T1] complex neural operator CO forecast (IIT-D/IISc, Indian cities); next-hour R2>0.95, beats FNO
- Takeaway for TRINETRA: India-origin advisory forecasting; src-reported. Extreme-event capture hard -> HITL. Source-reported. NEW. DEPLOYMENT lit map T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-064 | 2607.16218
- arXiv/DOI: arXiv:2607.16218
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Fuzzy Logic Framework for Community-Aware Crime Hotspot Detection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T2
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T2] fuzzy fusion citizen reports + privacy workflow; authors state NO real-world predictive evidence (n=25)
- Takeaway for TRINETRA: src-reported honest 'complementary not certified' + multilingual UX model. Source-reported. NEW. DEPLOYMENT lit map T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-065 | 1810.11498
- arXiv/DOI: arXiv:1810.11498
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Automatic Identification and Ranking of Emergency Aids in Social Media
- Year / Venue: 2018 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T2
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T2] embedding NN + weighted ranking; 6.81% MAP on Nepal-quake multilingual tweets
- Takeaway for TRINETRA: SA relief matching; src-reported low MAP = decision-support not autonomous. Source-reported. NEW. DEPLOYMENT lit map T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-066 | 2410.06743
- arXiv/DOI: arXiv:2410.06743
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Transfer Learning for Forest Fire Detection: Uttarakhand Case Study
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T3
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T3] MobileNetV2 TL cuts India labeled-data needs; TL > from-scratch (qualitative)
- Takeaway for TRINETRA: India fire detection; src-reported. Regional domain shift = key caveat. Source-reported. NEW. DEPLOYMENT lit map T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-067 | 2609.11829
- arXiv/DOI: arXiv:2609.11829
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: WFDroneBench: Benchmark for Sensor Placement and Drone Routing for Wildfire Detection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T3
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T3] open benchmark ML risk maps + placement, 7746 scenarios; risk-map error dominates
- Takeaway for TRINETRA: src-reported Max-Coverage beats baselines when risk maps accurate. Shadow-mode before trusting placement. Source-reported. NEW. DEPLOYMENT lit map T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-068 | 2608.22293
- arXiv/DOI: arXiv:2608.22293
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Spatial Anatomy of Urban Wildfire Vulnerability (GeoAI Palisades)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T3
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T3] XGBoost+LR 12081 inspections; ROC-AUC 0.92 random CV but 0.75 spatial-block
- Takeaway for TRINETRA: src-reported recommends spatial-block as MINIMUM. KEY: random CV overstates skill. Source-reported. NEW. DEPLOYMENT lit map T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-069 | 2610.03724
- arXiv/DOI: arXiv:2610.03724
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: From Community Values to AI Design Constraints: AI Wildfire Risk Tool LA County
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T4
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T4] survey n=30 + town hall; 66.7% likely to use, privacy top concern 64.3%, cost barrier 65.5%
- Takeaway for TRINETRA: src-reported. Pre-model community value elicitation for India pilots. Source-reported. NEW. DEPLOYMENT lit map T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-070 | 2209.02416
- arXiv/DOI: arXiv:2209.02416
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Crowd-Funded Earthquake Early-Warning System
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T5
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T5] reused Android phones as seismometers/alarms, targets budget-constrained incl. India (conceptual)
- Takeaway for TRINETRA: src-reported no field metrics. Low-cost e-waste sensing; reliability unproven. Source-reported. NEW. DEPLOYMENT lit map T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-071 | 2511.15710
- arXiv/DOI: arXiv:2511.15710
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: AZIZA: Trust-Aware Opportunistic DTN Edge Routing for Flood-Affected Bangladesh
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T5
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T5] trust-aware DTN over phones/UAVs on real Bangladesh flood traces (sim); better delivery/energy/resilience
- Takeaway for TRINETRA: src-reported simulation. Connectivity-collapse mitigation. Source-reported. NEW. DEPLOYMENT lit map T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-072 | 2605.16375
- arXiv/DOI: arXiv:2605.16375
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: M2FedAQI: Multimodal Federated Learning for Air Quality on Heterogeneous Edge
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T5
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T5] multimodal federated AQI + TLS auth; +11% acc / -25.4% MAE
- Takeaway for TRINETRA: src-reported; TRAQID regional set. Privacy-preserving bandwidth-light edge learning. Source-reported. NEW. DEPLOYMENT lit map T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-073 | 2502.07596
- arXiv/DOI: arXiv:2502.07596
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Enviro-IoT: Calibrating Low-Cost Environmental Sensors in Urban Settings
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T5
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T5] 9-mo field low-cost PM/NO2 vs reference; 98/97/97% (single case)
- Takeaway for TRINETRA: src-reported. Field-calibration discipline; single-site limit. Source-reported. NEW. DEPLOYMENT lit map T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-074 | 2207.12406
- arXiv/DOI: arXiv:2207.12406
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: UrduFake@FIRE2020: Shared Task on Fake News Identification in Urdu
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T6
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T6] Urdu fake-news, 900/400 articles, 42 teams; best F 0.90 (BERT)
- Takeaway for TRINETRA: src-reported; year domain-shift degrades. SA-language misinformation benchmark. Source-reported. NEW. DEPLOYMENT lit map T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-075 | 2605.17353
- arXiv/DOI: arXiv:2605.17353
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: You Cannot Fool Us: Resilience of LLM-driven Agent Communities to Misinformation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T6
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T6] agent sim; higher AOT improves resistance, source warnings weaker
- Takeaway for TRINETRA: src-reported simulation only. Caution transferring to Indian contexts. Source-reported. NEW. DEPLOYMENT lit map T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-076 | 2103.07792
- arXiv/DOI: arXiv:2103.07792
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Multilingual Code-Switching for Zero-Shot Cross-Lingual Intent/Slot Filling
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T6
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T6] random-translation code-switch aug for mBERT; +4.2% intent/+1.8% slot over 8 langs
- Takeaway for TRINETRA: new disaster-tweet set; src-reported. Low-resource code-switched languages; human triage. Source-reported. NEW. DEPLOYMENT lit map T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-077 | 2005.11177
- arXiv/DOI: arXiv:2005.11177
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: GeoCoV19: Hundreds of Millions of Multilingual COVID-19 Tweets with Location
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T6 | re-cited 2x
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T6] 524M+ multilingual geolocated tweets, gazetteer geo-inference
- Takeaway for TRINETRA: src-reported dataset. ToS/licensing + inferred-geo noise to verify. Source-reported. NEW. DEPLOYMENT lit map T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-078 | 2610.04084
- arXiv/DOI: arXiv:2610.04084
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Dependable AI-Assisted Engineering: Formal Framework for AI Participation and Assurance
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T7
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T7] per-unit participation+assurance records w/ fallback + human-adjudication; 17-unit wing-spar case
- Takeaway for TRINETRA: src-reported no workflow-level dependability claim. Operationalizes 'human stays decisive'. Source-reported. NEW. DEPLOYMENT lit map T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-079 | 2609.13552
- arXiv/DOI: arXiv:2609.13552
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Toward a Decision-Assurance Layer for AI-Assisted Flight Planning (ATAL)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T7
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T7] semantic-stability + consistency + normative checks -> Decision Readiness Level; flags unsafe pre-use
- Takeaway for TRINETRA: src-reported transferable to oversight domains. Shadow->advisory gating pattern. Source-reported. NEW. DEPLOYMENT lit map T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-080 | 2608.20864
- arXiv/DOI: arXiv:2608.20864
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Coverage-Driven Verification for Safety-by-Design in AI Collision Avoidance
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T7
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T7] ODD representativeness via KL-divergence/Cramer's V, aligned to EASA objectives
- Takeaway for TRINETRA: src-reported (verify EASA officially). Prove eval data covers the India ODD. Source-reported. NEW. DEPLOYMENT lit map T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-081 | 2608.19816
- arXiv/DOI: arXiv:2608.19816
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Understanding as an Explicit Assessable Component of Frontier AI Safety Decisions
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T7
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T7] 4 objects of understanding + adequacy justification (Assurance 2.0); trialled on 2 scenarios
- Takeaway for TRINETRA: src-reported generative. Structures the safety case for decision-makers. Source-reported. NEW. DEPLOYMENT lit map T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-082 | 2608.04501
- arXiv/DOI: arXiv:2608.04501
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Privacy-Preserving Action Recognition: Taxonomy Methods and Trade-offs
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T8
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T8] PRISMA 32 papers; only 10% formal privacy defs, <15% cross-dataset, <10% adaptive-attacker
- Takeaway for TRINETRA: src-reported. Maps privacy-utility options + evidence gaps for video sensing. Source-reported. NEW. DEPLOYMENT lit map T8.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-083 | 2609.07403
- arXiv/DOI: arXiv:2609.07403
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Federated Binary Gating with Server-Side VLM for Surveillance Anomaly Classification
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T8
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T8] local CNN gate forwards only flagged clips to server VLM; ~centralized F1 at 51.4% video, FNR 29.3->22.9%
- Takeaway for TRINETRA: src-reported. Data-minimizing architecture (keep raw video local). Source-reported. NEW. DEPLOYMENT lit map T8.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-084 | 2608.08528
- arXiv/DOI: arXiv:2608.08528
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Task-to-Model Optimization: Data-Driven Cost-Optimal Routing
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T9
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T9] cost-per-COMPLETED-task + staged static->shadow->verified-cascade->router
- Takeaway for TRINETRA: src-reported analytical. Cost-effectiveness + staged-rollout methodology template. Source-reported. NEW. DEPLOYMENT lit map T9.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-085 | 2610.08810
- arXiv/DOI: arXiv:2610.08810
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Transferability and Operational Reliability of a Prithvi Crop-Classification FM under Shift
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T10
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T10] OOD 37 events/12 countries; acc 0.65->0.40, confidence stayed HIGH while wrong, MC-dropout flagged all shifts
- Takeaway for TRINETRA: src-reported. STRONGEST lesson: uncertainty monitoring + stopping rules + OOD checks. Source-reported. NEW. DEPLOYMENT lit map T10.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ALERT-086 | 2604.02351
- arXiv/DOI: arXiv:2604.02351
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Modeling and Controlling Deployment Reliability under Temporal Distribution Shift
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DEPLOY | phase: P19-T10
- Uses (workstream/chapter): WS3 (ch 08), WS7 IoT (ch 15), BOM / ch 11
- Core method: [P19-T10] reliability as dynamic state w/ volatility; selective drift-triggered intervention beats continuous retraining
- Takeaway for TRINETRA: 1.35M loans; src-reported. Report reliability as a time-trajectory. Source-reported. NEW. DEPLOYMENT lit map T10.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass


---

## Theme: Offline-RL / OPE / safe-RL / shielding  (`REF-RL-*`, 71 entries)

_Primary consumer: WS5 RL (ch 10), ch 12 OPE gate. The ledger axis/WS code that mapped each paper into this theme is printed per entry for traceability._

#### REF-RL-001 | 2206.02000
- arXiv/DOI: arXiv:2206.02000
- Authors: Jin; Liu; Jiang; Yu
- Title: Hybrid Value Estimation for Off-policy Evaluation and Offline Reinforcement Learning
- Year / Venue: 2022 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A5 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: bias-variance OPE value estimation
- Takeaway for TRINETRA: Hybrid Value Estimation trades off bias/variance by blending value estimates from offline data and a learned model, better error bound than direct methods; gives OPHVE (off-policy eval) + MOHVE (offline RL).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-002 | 2106.08909
- arXiv/DOI: arXiv:2106.08909
- Authors: Brandfonbrener; Whitney; Ranganath; Bruna
- Title: Offline RL Without Off-Policy Evaluation (One-Step)
- Year / Venue: 2021 / NeurIPS 2021
- Read depth: ABS | local note: yes | ledger axis/WS: A5 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: one-step beats iterative; OPE variance
- Takeaway for TRINETRA: Shows ONE step of constrained/regularized policy improvement using an on-policy Q of the behavior policy beats iterative actor-critic on much of D4RL, while being simpler + more hyperparameter-robust; argues iterative offline RL suffers hig...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-003 | 2305.16147
- arXiv/DOI: arXiv:2305.16147
- Authors: Lindner; Chen; Tschiatschek; Hofmann; Krause
- Title: Learning Safety Constraints from Demonstrations with Unknown Rewards
- Year / Venue: 2024 / AISTATS 2024
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: CoCoRL: convex safe set from safe demos, transferable constraints
- Takeaway for TRINETRA: CoCoRL infers SHARED constraints in a CMDP from safe demonstrations with possibly DIFFERENT, UNKNOWN rewards and without known dynamics; builds a CONVEX safe set that provably guarantees safety even for sub-optimal-but-safe demos, converges...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-004 | 2602.20729
- arXiv/DOI: arXiv:2602.20729
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Fuz-RL: A Fuzzy-Guided Robust Framework for Safe Reinforcement Learning under Uncertainty
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: fuzzy-measure-guided interpretable risk for safe RL under multi-source uncertainty
- Takeaway for TRINETRA: Safe RL must perform well while staying safe, but multiple interacting uncertainty sources make interpretable risk assessment + robust decisions hard; Fuz-RL is a fuzzy-measure-guided robust framework for safe RL under uncertainty.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-005 | 2110.14000
- arXiv/DOI: arXiv:2110.14000
- Authors: Zhang; Jiang
- Title: Towards Hyperparameter-free Policy Selection for Offline Reinforcement Learning
- Year / Venue: 2021 / NeurIPS 2021
- Read depth: ABS | local note: no | ledger axis/WS: A5 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: BVFT hyperparameter-free value-function/policy selection; combine with OPE for continuous actions
- Takeaway for TRINETRA: Tackles how to SELECT among policies/value-functions from different offline-RL training runs (crucial for hyperparameter tuning) without creating a chicken-and-egg of OPE-needs-its-own-hyperparameters; designs HYPERPARAMETER-FREE selection...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-006 | 2311.18206
- arXiv/DOI: arXiv:2311.18206
- Authors: Kiyohara; Kishimoto; Kawakami; Kobayashi; Nakata; Saito
- Title: SCOPE-RL: A Python Library for Offline Reinforcement Learning and Off-Policy Evaluation
- Year / Venue: 2023 / arXiv (cs.LG) preprint
- Read depth: ABS | local note: no | ledger axis/WS: A5 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: end-to-end offline-RL + OPE + OPS library; estimates full reward DISTRIBUTION + risk-return tradeoff
- Takeaway for TRINETRA: Open-source Python library (SCOPE-RL) seamlessly integrating offline-RL training with OPE and off-policy SELECTION (OPS); emphasis on OPE modules with many estimators + robust evaluation-of-OPE protocols; estimates the ENTIRE reward DISTRIB...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-007 | 2305.03360
- arXiv/DOI: arXiv:2305.03360
- Authors: He
- Title: A Survey on Offline Model-Based Reinforcement Learning
- Year / Venue: 2023 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A5 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: offline RL stage
- Takeaway for TRINETRA: Survey centering distributional shift as THE core offline-RL failure; model-based methods use uncertainty penalties. Grounds why TRINETRA's offline-RL stage needs pessimism + OOD penalties, not just CQL default.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-008 | 2402.00816
- arXiv/DOI: arXiv:2402.00816
- Authors: (AMBS authors)
- Title: Leveraging Approximate Model-based Shielding for Probabilistic Safety Guarantees in Continuous Environments
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: safety shield
- Takeaway for TRINETRA: Extends approximate model-based shielding to continuous state/action with probabilistic safety guarantees + policy-gradient penalties.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-009 | 2507.23603
- arXiv/DOI: arXiv:2507.23603
- Authors: Rodriguez; Shaik; Corsi; Fox; Sanchez
- Title: Explanations for Unrealizability of Infinite-State Safety Shields
- Year / Venue: 2025 / arXiv (cs.LO)
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: safety shield
- Takeaway for TRINETRA: Shields can be UNREALIZABLE when the spec is inconsistent/contradictory; gives unrolling-based explanations.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-010 | 2203.04236
- arXiv/DOI: arXiv:2203.04236
- Authors: Perdomo; Krishnamurthy; Bartlett; Kakade
- Title: A Complete Characterization of Linear Estimators for Offline Policy Evaluation
- Year / Venue: 2022 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A5 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: offline policy evaluation
- Takeaway for TRINETRA: Necessary+sufficient conditions for FQI/LSTD to succeed at OPE; many strong negative results -> OPE often intractable.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-011 | 2506.00505
- arXiv/DOI: arXiv:2506.00505
- Authors: Qu; Gogol; Groetschla; Tessone
- Title: From Rules to Rewards: Reinforcement Learning for Interest Rate Adjustment in DeFi Lending
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A5 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: offline RL stage (TD3-BC)
- Takeaway for TRINETRA: Compares CQL vs BC vs TD3-BC on real Aave data; TD3-BC best at balancing utilization/stability/risk + robust to stress events. Empirical support for TRINETRA's TD3-BC choice over plain CQL; stress-event robustness analogy to rare hazards.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-012 | 2403.05732
- arXiv/DOI: arXiv:2403.05732
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Conservative DDPG -- Pessimistic RL without Ensemble
- Year / Venue: 2024 / arXiv (cs.AI)
- Read depth: ABS | local note: no | ledger axis/WS: A5 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: offline RL pessimism
- Takeaway for TRINETRA: Adds a BC-loss penalty + Q-target to DDPG as a cheap uncertainty/pessimism measure; beats DDPG, competitive w/ TD3, far less compute.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-013 | 2302.13423
- arXiv/DOI: arXiv:2302.13423
- Authors: Liu; Niu; Pan; Herrmann; Carrasco
- Title: Sim-and-Real Reinforcement Learning for Manipulation: A Consensus-based Approach
- Year / Venue: 2023 / ICRA 2023
- Read depth: ABS | local note: no | ledger axis/WS: A5 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: simulator PPO stage / sim-to-real
- Takeaway for TRINETRA: Finds best-in-sim policy is NOT best for sim-and-real; more sim agents helps. Direct caution for TRINETRA's SB3-PPO-in-simulator stage: optimizing sim reward can hurt real deployment -> validates need for sim-to-real care (new RL risk).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-014 | 2601.05152
- arXiv/DOI: arXiv:2601.05152
- Authors: Tomashevskiy
- Title: Safe Continual Reinforcement Learning Methods for Nonstationary Environments: A Survey
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: safe RL under nonstationarity
- Takeaway for TRINETRA: Survey of continual safe online RL under nonstationarity (NSMDP/HM-MDP/safe POMDP), safety-constraint taxonomy.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-015 | 2604.23576
- arXiv/DOI: arXiv:2604.23576
- Authors: Dawood; Siddiquie; Khorshidi; Bennewitz
- Title: CAPSULE: Control-Theoretic Action Perturbations for Safe Uncertainty-Aware RL
- Year / Venue: 2026 / L4DC
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: safe RL hard constraints
- Takeaway for TRINETRA: Hard (not in-expectation) safety via control-theoretic action perturbation; integrates w/ SAC/TD3; up to 126x fewer violations.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-016 | 2502.01307
- arXiv/DOI: arXiv:2502.01307
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Improving the Effectiveness of Potential-Based Reward Shaping in RL
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A5 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: reward shaping robustness
- Takeaway for TRINETRA: Potential-based reward shaping (PBRS) is policy-invariant + significantly more ROBUST TO SCALING than typical reward shaping -> easier to tune.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-017 | 2104.06411
- arXiv/DOI: arXiv:2104.06411
- Authors: Okudo; Yamada
- Title: Subgoal-based Reward Shaping to Improve Efficiency in Reinforcement Learning
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A5 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: reward shaping / subgoals
- Takeaway for TRINETRA: Subgoal-based reward shaping lets humans inject knowledge via representative states; beats potential-based + naive baselines on efficiency.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-018 | 2511.21531
- arXiv/DOI: arXiv:2511.21531
- Authors: Jin; Krasowski; Vanneaux
- Title: Predictive Safety Shield for Dyna-Q Reinforcement Learning
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: predictive safety shield
- Takeaway for TRINETRA: Existing shields use random safe-action sampling / fixed fallback, IGNORING future performance of safe actions; predictive shield updates Q locally from safe model simulation -> keeps hard guarantees AND improves performance; robust to sim-...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-019 | 2112.11490
- arXiv/DOI: arXiv:2112.11490
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Safety-Aware Reinforcement Learning with Latent Shielding
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: latent shielding high-dim
- Takeaway for TRINETRA: Latent shielding enables safe deep RL in HIGH-dimensional envs without a hand-crafted model, learning safety in latent space.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-020 | 2310.04288
- arXiv/DOI: arXiv:2310.04288
- Authors: Miller; Zeitler; Shen; Hobbs; Mitra; Schierman; Viswanathan
- Title: Searching for Optimal Runtime Assurance via Reachability and Reinforcement Learning
- Year / Venue: 2023 / arXiv (eess.SY/cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: least-conservative optimal RTA switching
- Takeaway for TRINETRA: Existing runtime-assurance (RTA) switching logics (switch to backup controller) are OVERLY CONSERVATIVE and can STILL violate safety; formulates OPTIMAL RTA as maximizing use of the untrusted controller subject to reachability-based safety,...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-021 | 2409.04641
- arXiv/DOI: arXiv:2409.04641
- Authors: Cannon; Garcia; Gresavage; Saurine; Leong; Culbertson
- Title: Stacked Universal Successor Feature Approximators for Safety in RL (SUSFAS)
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: multi-objective safety + backup controllers
- Takeaway for TRINETRA: Real tasks have multi-dimensional objectives (operating cost vs performance vs safety vs availability) irreducible to one scalar reward; SUSFAS = continuous-control universal successor-feature approximation on SAC + a suite of secondary saf...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-022 | 2604.24404
- arXiv/DOI: arXiv:2604.24404
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Open-Source 5G Public Warning System Spoofing Testbed
- Year / Venue: 2026 / arXiv
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A6 | phase: P3 | re-cited 3x
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P3] alerting/security WS3
- Takeaway for TRINETRA: PWS SIBs broadcast UNauthenticated → spoofable (OAI+SDR testbed). Defense = cross-cell/multi-source corroboration. Sign CAP end-to-end; authenticate LoRa/ESP-NOW mesh (HMAC); require multi-channel corroboration before 'authoritative'.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-023 | 2610.03380
- arXiv/DOI: arXiv:2610.03380
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Interpretable Deepfake Detection via Explicit Forensic Features + Temporal Modeling
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A5 | phase: P3 | re-cited 2x
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P3] media forensics WS2
- Takeaway for TRINETRA: Explicit per-frame feature families (photometric 18 / textural 24 / geometric 14 / compression 12) + LSTM temporal + face-tracking. Interpretable → auditable first-pass filter for crowd/CCTV corroboration (Rule 19).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-024 | 2610.06317
- arXiv/DOI: arXiv:2610.06317
- Authors: Delbianco; Tohmé; Acciarri
- Title: Watermarking: from Impossibility to Auditable Compliance
- Year / Venue: 2026 / arXiv (cs.CR/stat.ML)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A5 | phase: P3
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P3] provenance capstone + WS8 asymmetric-error UQ
- Takeaway for TRINETRA: EU AI Act Art.50(2): strong watermarking IMPOSSIBLE vs adaptive removal. Auditable alt = description-length robustness profile (collision entropy; sample size ~1/decay²) + LABEL-CONDITIONAL conformal sets w/ separate false-attribution vs fa...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-025 | 2606.04634
- arXiv/DOI: arXiv:2606.04634
- Authors: Rieder; Pranger; Chakraborty; Křetínský; Könighofer
- Title: Explainably Safe Reinforcement Learning
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A5 | phase: P3
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P3] auditable shield; human-oversight explanations for safe RL
- Takeaway for TRINETRA: Könighofer/Křetínský shielding group. Makes a formal probabilistic SHIELD human-interpretable via a HIERARCHY of decision trees: design-time world-model risk analysis classifies states into safe/critical/dangerous/unsafe + builds shield; ru...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-026 | 2107.11003
- arXiv/DOI: arXiv:2107.11003
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Model Selection for Offline RL: Practical Considerations for Healthcare
- Year / Venue: 2021 / MLHC 2021
- Read depth: FT | local note: no | ledger axis/WS: A6 | phase: P4
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P4] OPERATIONALIZES C-11: iterative RL only if OPE-feasible
- Takeaway for TRINETRA: Offline-RL model-selection pipeline using off-policy evaluation (OPE) as validation; FQE gives the best validation ranking of policies but is compute-heavy; a 2-stage model-selection accelerator; sepsis treatment as safety-critical testbed....
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-027 | 2608.08158
- arXiv/DOI: arXiv:2608.08158
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A Unified Framework for Dynamic Reward Shaping in Reinforcement Learning
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A6 | phase: P4
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P4] GROUNDS PBRS + flags adaptive-shaping risk (C-10)
- Takeaway for TRINETRA: Review+framework. Static potential-based reward shaping (PBRS) preserves the optimal policy iff the auxiliary term is the discounted difference of a time-invariant potential (Ng 1999).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-028 | 2609.37487
- arXiv/DOI: arXiv:2609.37487
- Authors: Nagashima; Bannai; Misaizu; Maeda; Ogawa; Haseyama
- Title: Physics-Guided Flow-Map Matching (PG-FMM) for Precipitation Nowcasting
- Year / Venue: 2026 / arXiv (cs.CV) ACCV 2026
- Read depth: ABS | local note: no | ledger axis/WS: A5 | phase: P5
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P5] WS1/WS3: physics-prior as GUIDANCE + heavy-rain tail gains
- Takeaway for TRINETRA: Frozen Lagrangian advection prior supplies an explicit motion forecast used as GUIDANCE (conditioned on, NOT summed as residual) to a flow-map generative head producing sharp detail in 4 steps; SOTA on 18/24 metrics across 4 radar benchmark...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-029 | 2610.12189
- arXiv/DOI: arXiv:2610.12189
- Authors: Wiese; Schusterbauer; Martorella; Ommer
- Title: Just Weather Scoring (JWS): Efficient End-to-End Nowcasting with Distributional Diffusion
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A5 | phase: P5
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P5] WS1/WS6: few-step diffusion = efficient probabilistic nowcasting
- Takeaway for TRINETRA: Single-stage radar-space diffusion (Masked Asynchronous Diffusion + scoring-rule objective) enabling FEW-STEP generation; SOTA probabilistic nowcasting on SEVIR + MeteoNet at reduced TRAIN and INFERENCE cost; smallest model competitive usin...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-030 | 2310.06224
- arXiv/DOI: arXiv:2310.06224
- Authors: Ornee; Shisher; Kam; Sun
- Title: Context-aware Status Updating: Wireless Scheduling for Situational Awareness
- Year / Venue: 2023 / arXiv (cs.IT) MILCOM 2023 WS
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: P6
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P6] comms: value-aware reporting (CO fire example)
- Takeaway for TRINETRA: AoI + observed-value 'situation-unaware penalty' solved as a Restless MAB; up to 100x vs periodic, 10x vs random (simulation).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-031 | 2511.00348
- arXiv/DOI: arXiv:2511.00348
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Ultralow-power Standoff Acoustic Leak Detection
- Year / Venue: 2025 / arXiv (cs.CR/eess.AS)
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: P6
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P6] power/comms: classify on-device, send bytes
- Takeaway for TRINETRA: Battery edge-only acoustic node merging glass-break + smoke-detector principles; all DSP on-device, status in a few bytes, above speech band for privacy. SOURCE-REPORTED 20-200 uW; detects 0.15 L/min leak >10 m behind walls.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-032 | 2605.26159
- arXiv/DOI: arXiv:2605.26159
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Device Context Protocol (DCP): Compact Safety-First Architecture for Constrained Devices
- Year / Venue: 2026 / arXiv (cs.NI/CR) MIT
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: P6
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P6] security: MCU HMAC + replay footprint
- Takeaway for TRINETRA: Sub-50-byte frame = 6-B header + CBOR payload + optional 16-B HMAC, with capability scoping/range/type checks.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-033 | 2605.19793
- arXiv/DOI: arXiv:2605.19793
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Motion-Coupled Sensing: When the State Change Powers Its Own Sensing
- Year / Venue: 2026 / arXiv (cs.NI/ET)
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: P6
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P6] power/comms: one event-triggered LoRa uplink
- Takeaway for TRINETRA: Batteryless: one mechanical actuation powers a full wake-sense-transmit (ultrasonic + LoRa uplink). SOURCE-REPORTED 99.3% per-event tx over 5945 bin actuations; 92%/94% doors/cabinets.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-034 | 2608.00409
- arXiv/DOI: arXiv:2608.00409
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: SIC-Aided Intelligent Decentralized Resource Allocation in Dynamic LoRa Networks
- Year / Venue: 2026 / arXiv (cs.DC)
- Read depth: ABS | local note: no | ledger axis/WS: A6 | phase: P6
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P6] comms: adaptive LoRa params on-device
- Takeaway for TRINETRA: On-device Thompson Sampling for LoRa transmit-parameter selection + Schwarz Information Criterion to detect environment change and reset learning, using only ACK feedback.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-035 | 2509.19972
- arXiv/DOI: arXiv:2509.19972
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: An effective control of large systems of active particles: application to evacuation
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: n/r
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T1/T2] leader-follower crowd control; naive RL underperforms, hybrid robust
- Takeaway for TRINETRA: Vicsek + artificial forces; code public (cinemere/evacuation). CAUTION physics-hybrid beats naive RL; reusable env. Source-reported. NEW. literature_map P15-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-036 | 2609.36315
- arXiv/DOI: arXiv:2609.36315
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PyroStack: Multi-Band Spatio-Temporal Sub-Daily Dataset for US Wildfires
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T2
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T2] 6994 wildfires 2012-24, hourly, 12-h fire progression (D102)
- Takeaway for TRINETRA: multi-band satellite+reanalysis+fuels; src-reported benchmark foundation. Validation data + non-RL baseline; wrap into env. Source-reported. NEW. literature_map P15-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-037 | 2610.07431
- arXiv/DOI: arXiv:2610.07431
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FireGen: Quantifying Wildfire Risk by Simulation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T2
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T2] Monte-Carlo wildfire sim (point-process + ellipse perimeters + lognormal area) (D103)
- Takeaway for TRINETRA: N. California; src-reported probabilistic risk tool. Stochastic scenario generator / non-RL baseline. Source-reported. NEW. literature_map P15-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-038 | 2610.09438
- arXiv/DOI: arXiv:2610.09438
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Ctrl-CWM: Controllable Crowd Generation through World-Model Planning
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T2
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T2] controllable crowd world-model, runtime user costs w/o retraining (D104)
- Takeaway for TRINETRA: encoder+actor+critic+planner; src-reported beats SOTA crowd-realism/collision. Reusable operator-controllable crowd sim. Source-reported. NEW. literature_map P15-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-039 | 2610.11281
- arXiv/DOI: arXiv:2610.11281
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: How to post-train on a surrogate: Envelope sampling mitigates reward hacking
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T3
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T3] recalibrate surrogate reward w/ few labels, bounded regret
- Takeaway for TRINETRA: src-reported mitigates hacking where base-sample recalibration fails. Audit evacuation reward proxies w/ scarce expert labels. Source-reported. NEW. literature_map P15-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-040 | 2610.11464
- arXiv/DOI: arXiv:2610.11464
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Who Verifies the Verifier? Co-Evolving Inspectable Graders with Self-Improving Agents
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T3
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T3] KEY: downstream task score CANNOT certify a reward/verifier
- Takeaway for TRINETRA: inspectable detectors + anchored reference set + outer judge; remove anchors -> vacuous always-pass; src-reported +0.21 agreement. Human-auditable reward governance. Source-reported. NEW. literature_map P15-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-041 | 2610.12432
- arXiv/DOI: arXiv:2610.12432
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FAITH: Feasibility-Aware Safety-Filtered RL for High-Dimensional Systems
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T4
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T4] safety filter w/ minimum-predicted-peak-harm when no safe action
- Takeaway for TRINETRA: 99.95% safety (humanoid) retaining 97% return, real Unitree G1; src-reported. The infeasible-emergency fallback. Source-reported. NEW. literature_map P15-T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-042 | 2610.12420
- arXiv/DOI: arXiv:2610.12420
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A Unified Bellman Operator for Safety-Critical Reinforcement Learning
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T4
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T4] joint performance+safety value, near-zero test-time violations
- Takeaway for TRINETRA: two-timescale, convergence shown; src-reported. At-all-times (not on-average) safety target. Source-reported. NEW. literature_map P15-T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-043 | 2610.11739
- arXiv/DOI: arXiv:2610.11739
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Distributed Constrained Resource Management in 6G: Scalable Hybrid Model-Learning
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T4
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T4] structurally guarantee hard constraint, MARL optimizes rest; 100% constraint satisfaction
- Takeaway for TRINETRA: +40% throughput, beats optimization+learning baselines; src-reported. Resource allocation w/ hard safety/coverage constraints. Source-reported. NEW. literature_map P15-T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-044 | 2610.05961
- arXiv/DOI: arXiv:2610.05961
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Strategic Multi-Agent Learning for Interpretable Action Valuation in Football
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T5
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T5] interpretable per-agent value, MPE + successor-feature Q decomposition
- Takeaway for TRINETRA: vs independent-RL baseline; src-reported context-sensitive rankings. Per-responder contribution for a human overseer. Source-reported. NEW. literature_map P15-T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-045 | 2610.11175
- arXiv/DOI: arXiv:2610.11175
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Higher-Order Action Supervision Makes A Strong Policy Class
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T6
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T6] plug-in first-order action-dynamics loss; low-data OOD gains
- Takeaway for TRINETRA: D4RL/OGBench; src-reported. Lightweight offline-RL robustness for small-compute logged data. Source-reported. NEW. literature_map P15-T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-046 | 2610.11085
- arXiv/DOI: arXiv:2610.11085
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DaCe-DT: Data-Centric Offline Multi-Task RL via Adaptive Prompts & Trajectory Correction
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T6
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T6] prompt masking + retrieval + return calibration; +11.73%/+13.34%
- Takeaway for TRINETRA: Meta-World optimal/suboptimal; src-reported. Learn from messy heterogeneous emergency logs. Source-reported. NEW. literature_map P15-T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-047 | 2610.12135
- arXiv/DOI: arXiv:2610.12135
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Q-Shaped Options for Hierarchical Reinforcement Learning
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T6
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T6] learns control-relevant action abstraction; non-zero where baselines fail
- Takeaway for TRINETRA: offline goal-conditioned; src-reported. Temporal abstraction for long-horizon evacuation. Source-reported. NEW. literature_map P15-T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-048 | 2610.07899
- arXiv/DOI: arXiv:2610.07899
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Variance-Averse n-Step Offline RL for Sparse Long-Horizon Environments (VAN-Flow)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T6
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T6] prefers RELIABLE low-variance actions; largest gains long-horizon/high-variance
- Takeaway for TRINETRA: distributional critic + flow-matching actor, 40+ tasks; src-reported. Life-safety risk posture. Source-reported. NEW. literature_map P15-T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-049 | 2610.08225
- arXiv/DOI: arXiv:2610.08225
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: UWB Meets Crazyflow: Simulating Degraded Feedback at Scale for Aerial Robotics
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T7
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T7] differentiable JAX physics+control, order-of-magnitude speedups
- Takeaway for TRINETRA: train deployable RL in seconds, degraded-feedback modeling; src-reported. Template for fast GPU-vectorized evac/sensor env on small compute. Source-reported. NEW. literature_map P15-T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-050 | 2610.07686
- arXiv/DOI: arXiv:2610.07686
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: BluffJAX: Adversarial Imperfect Information Games in JAX
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T7
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T7] JAX imperfect-info games, hundreds of M samples/sec
- Takeaway for TRINETRA: benchmarked baselines; src-reported. GPU-vectorized env patterns; imperfect-info fits partial sensor coverage. Source-reported. NEW. literature_map P15-T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-051 | 2610.05819
- arXiv/DOI: arXiv:2610.05819
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Transporting Unsecured Stacked Payloads with a Quadrupedal Robot via Multi-Objective RL (PAMORT)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5 | phase: P15-T9
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P15-T9] preference-vector safety-vs-task + online adaptation; real Go2 zero-shot 0.850 vs 0.675
- Takeaway for TRINETRA: src-reported sim-to-real. Human-tunable safety-vs-task trade-off. Source-reported. NEW. literature_map P15-T9.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-052 | 2506.01755
- arXiv/DOI: arXiv:2506.01755
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Data-assimilated Model-informed RL (DA-MIRL)
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] controls chaotic KS from partial obs via low-order models + DA + actor-critic
- Takeaway for TRINETRA: Grounds FM-6. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-053 | 2212.02179
- arXiv/DOI: arXiv:2212.02179
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-Informed Model-Based RL
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] PINN dynamics beats NN & model-free SAC in return/sample-efficiency
- Takeaway for TRINETRA: Grounds FM-6. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-054 | 2208.14501
- arXiv/DOI: arXiv:2208.14501
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Model-Based RL with SINDy
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] discovers dynamics from ~1 rollout; near-optimal with few trajectories
- Takeaway for TRINETRA: Sample-efficient MBRL. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-055 | 1705.00470
- arXiv/DOI: arXiv:1705.00470
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Learning Multimodal Transition Dynamics for MBRL
- Year / Venue: 2017 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] conditional VI robustly learns stochastic multimodal transition dynamics
- Takeaway for TRINETRA: MBRL. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-056 | 2410.11711
- arXiv/DOI: arXiv:2410.11711
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Zero-shot Model-based RL using LLMs (DICL)
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] LLMs predict continuous-MDP dynamics in-context w/ calibrated uncertainty
- Takeaway for TRINETRA: MBRL. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-057 | 2309.01909
- arXiv/DOI: arXiv:2309.01909
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Survey on Physics-Informed RL (PIRL)
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] taxonomy of physics priors (observational/inductive/learning biases) in RL
- Takeaway for TRINETRA: Grounds FM-6 reward. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-058 | 2302.00237
- arXiv/DOI: arXiv:2302.00237
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: HJBPPO (HJB + PINN value net)
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] value net as PINN solving HJB; outperforms PPO on MuJoCo
- Takeaway for TRINETRA: PIRL. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-059 | 2603.26816
- arXiv/DOI: arXiv:2603.26816
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PiCSRL: Physics-Informed Contextual Spectral RL
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] physics embeddings+uncertainty belief for adaptive hyperspectral sampling; RMSE 0.153
- Takeaway for TRINETRA: VoI/active-perception. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-060 | 2604.01830
- arXiv/DOI: arXiv:2604.01830
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-Informed RL with Gibbs Priors (grid control)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] GNN-surrogate Gibbs physics prior reweights logits; +255% reward vs PPO
- Takeaway for TRINETRA: Grounds FM-6 reward. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-061 | 2511.18243
- arXiv/DOI: arXiv:2511.18243
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Dreaming Falcon (physics-informed world model)
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] free-body net + 6-DOF RK4 integrator MBRL; generalization limits noted
- Takeaway for TRINETRA: MBRL. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-062 | 2607.03125
- arXiv/DOI: arXiv:2607.03125
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PINN for Safe RL (1-DoF helicopter)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] differentiable physics in PPO actor loss penalizes anticipated safety violations
- Takeaway for TRINETRA: Grounds FM-6 safe-RL. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-063 | 2603.24241
- arXiv/DOI: arXiv:2603.24241
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: C-STEP: Continuous Space-Time Empowerment
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] physics-informed intrinsic reward for safe navigation; fewer collisions
- Takeaway for TRINETRA: Safe-RL. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-064 | 2306.11885
- arXiv/DOI: arXiv:2306.11885
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Reward Shaping via Diffusion Process
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] stochastic-thermodynamics reward shaping via entropy production
- Takeaway for TRINETRA: Reward shaping. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-065 | 2607.22667
- arXiv/DOI: arXiv:2607.22667
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: RL for Heterogeneous Sensor Selection (Maritime Surveillance)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] info-gain PPO picks 1 sensor/epoch; near always-on; zero-shot err <1m
- Takeaway for TRINETRA: Grounds FM-6 VoI. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-066 | 1906.07233
- arXiv/DOI: arXiv:1906.07233
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Learn to Sense (meta-learning sensing+fusion WSN)
- Year / Venue: 2019 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] RL meta-learner selects next most-informative sensing location
- Takeaway for TRINETRA: VoI. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-067 | 2106.06783
- arXiv/DOI: arXiv:2106.06783
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Lvio-Fusion (actor-critic sensor weighting)
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] actor-critic adjusts camera/Lidar/IMU/GPS weights in SLAM fusion
- Takeaway for TRINETRA: Grounds FM-6 ensemble-weighting. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-068 | 1703.04550
- arXiv/DOI: arXiv:1703.04550
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Sensor Fusion for Robot Control via Deep RL
- Year / Venue: 2017 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] DNN fuses sensors, robust to runtime sensor failures
- Takeaway for TRINETRA: Multimodal-RL. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-069 | 2606.15514
- arXiv/DOI: arXiv:2606.15514
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: RL4IL Soft Fusion under Missing Modalities
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] per-modality RL retrieval + soft cross-attention; beats SOTA under dropout
- Takeaway for TRINETRA: Missing-modality RL. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-070 | 2305.04750
- arXiv/DOI: arXiv:2305.04750
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Sense Imagine Act (SSL LiDAR+RGB Dreamer)
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] SSL multimodal fusion improves Dreamer; zero-shot racing
- Takeaway for TRINETRA: Multimodal-RL. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-RL-071 | 2602.01266
- arXiv/DOI: arXiv:2602.01266
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: RL for Active Perception in Autonomous Navigation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS5-RL | phase: P22
- Uses (workstream/chapter): WS5 RL (ch 10), ch 12 OPE gate
- Core method: [P22] voxel-based information reward couples motion + active camera control
- Takeaway for TRINETRA: VoI/active-perception. Source-reported. NEW. P22 RL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass


---

## Theme: Robustness / anomaly / drift / OOD / safety  (`REF-ROB-*`, 142 entries)

_Primary consumer: WS6+WS8 (ch 13), ch 12, ch 14. The ledger axis/WS code that mapped each paper into this theme is printed per entry for traceability._

#### REF-ROB-001 | 2502.15901
- arXiv/DOI: arXiv:2502.15901
- Authors: Gungor; Rios; Ahuja; Rosing
- Title: TS-OOD: Evaluating Time-Series Out-of-Distribution Detection and Prospective Directions
- Year / Venue: 2025 / AAAI-25 AI4TS
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: most OOD methods fail on time series
- Takeaway for TRINETRA: Comprehensive benchmark: MOST SOTA OOD-detection methods (developed for vision/NLP) perform POORLY on multivariate time series; deep-feature-modeling OOD methods do better.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-002 | 2605.31155
- arXiv/DOI: arXiv:2605.31155
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Learning Hyperspherical Time-Frequency Representations for Time-Series OOD Detection
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: time-freq hyperspherical OOD embeddings
- Takeaway for TRINETRA: Formulates time-series OOD as representation learning with hyperspherical (von Mises-Fisher) class-conditional embeddings over time-frequency features; principled detection under distributional shift.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-003 | 2205.13723
- arXiv/DOI: arXiv:2205.13723
- Authors: Yang; Chen; Jiang; Liu; Cao; Heng; Dou
- Title: DLTTA: Dynamic Learning Rate for Test-time Adaptation on Cross-domain Medical Images
- Year / Venue: 2022 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: per-sample dynamic LR test-time adaptation
- Takeaway for TRINETRA: Test-time adaptation with a FIXED learning rate is sub-optimal because the scale of distribution shift changes as data arrives sequentially; DLTTA uses a memory-bank discrepancy estimate to modulate per-sample weight updates, improving over...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-004 | 2411.15204
- arXiv/DOI: arXiv:2411.15204
- Authors: Jang; Chung
- Title: Label Distribution Shift-Aware Prediction Refinement for Test-Time Adaptation (DART)
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: detect+correct test-time label-distribution shift
- Takeaway for TRINETRA: DART detects and corrects CLASS/LABEL distribution shift at test time, improving pseudo-label accuracy by 5-18% under label shift on CIFAR-10C and with NO degradation when no shift exists; a plug-in to existing TTA.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-005 | 2006.01332
- arXiv/DOI: arXiv:2006.01332
- Authors: Zhang; Zhang; Tian
- Title: Real-time Earthquake Early Warning with Deep Learning: 2016 Central Apennines Italy
- Year / Venue: 2020 / Geophysical Research Letters
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: FCN EEW: location+magnitude 4s after P
- Takeaway for TRINETRA: Fully-convolutional net detects earthquakes + estimates location/magnitude from continuous waveform streams as soon as ONE station triggers, evolutionarily refining; on 2016 Mw6.0 Apennines, reliable within 4s of earliest P phase (6.8-3.7 k...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-006 | 2412.00264
- arXiv/DOI: arXiv:2412.00264
- Authors: Quintero Arenas; Quinteros Cartaya; Padilla Lafarga; Moraila; Faber; Koehler; Srivastava
- Title: High Magnitude Earthquake Identification Using Anomaly Detection on HR GNSS Data (DetEQ)
- Year / Venue: 2024 / arXiv (physics.geo-ph)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: GNSS autoencoder anomaly-detection EEW + FP filtering
- Takeaway for TRINETRA: DetEQ = lightweight CUSTOMIZABLE autoencoder pipeline detecting high-magnitude earthquakes as ANOMALIES in high-rate GNSS data: (i) anomaly score from reconstruction error, (ii) threshold detection, (iii) explicit FILTERING of local events...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-007 | 2312.15218
- arXiv/DOI: arXiv:2312.15218
- Authors: Zhang; Zhang
- Title: Generalized Neural Networks for Real-Time Earthquake Early Warning
- Year / Venue: 2023 / Communications Earth & Environment
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: generalized EEW nets, 4s, cross-region
- Takeaway for TRINETRA: Generalized neural networks for real-time EEW report location+magnitude within 4s of first triggered station across Japan + California (2.6-6.3 km, 0.05-0.17 mag error), eliminating complex empirical configurations and enabling GLOBAL appli...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-008 | 2504.17719
- arXiv/DOI: arXiv:2504.17719
- Authors: Hekler; Kuhn; Buettner
- Title: Evaluating Uncertainty in Deep Gaussian Processes
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: DGP/DSPP calibration under shift vs deep ensembles
- Takeaway for TRINETRA: Evaluates Deep Gaussian Processes + Deep Sigma Point Processes for UQ calibration and robustness UNDER DISTRIBUTION SHIFT vs Deep Ensembles, on regression (CASP) + classification (ESR).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-009 | 2310.03220
- arXiv/DOI: arXiv:2310.03220
- Authors: Krock; Bessac; Stein
- Title: Modeling spatial asymmetries in teleconnected extreme temperatures
- Year / Venue: 2023 / arXiv (stat.AP)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: DL+EVT for rare multivariate extremes, data-hungry caveat
- Takeaway for TRINETRA: Combines deep generative models with extreme-value theory for the full multivariate distribution of extreme winter temperatures; EXPLICITLY notes that by definition extreme events are FEW, which limits data-hungry nonparametric NNs; DL beat...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-010 | 2411.13496
- arXiv/DOI: arXiv:2411.13496
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Advancing Heatwave Forecasting via Distribution-Informed Graph Neural Networks (DI-GNNs): Integrating EVT with GNNs
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: EVT-informed GNN for rare extreme forecasting
- Takeaway for TRINETRA: DI-GNN integrates extreme-value theory INTO a graph neural network to forecast rare heatwaves (1-15 day scale), tackling non-linear atmospheric interactions + rarity where heuristic-feature models fail to generalize across climates.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-011 | 2406.09262
- arXiv/DOI: arXiv:2406.09262
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Fully Heteroscedastic Count Regression with Deep Double Poisson Networks (DDPN)
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: input-conditional count uncertainty, over/under-dispersion
- Takeaway for TRINETRA: Deep ensembles of Gaussian nets flexibly represent aleatoric uncertainty for CONTINUOUS regression but no analogue existed for COUNT regression; DDPN outputs Double-Poisson parameters enabling arbitrarily high/low predictive dispersion (ove...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-012 | 2001.04567
- arXiv/DOI: arXiv:2001.04567
- Authors: Siahkoohi; Rizzuti; Herrmann
- Title: A deep-learning based Bayesian approach to seismic imaging and uncertainty quantification
- Year / Venue: 2020 / arXiv (stat.ML)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: SGLD + Bayesian model averaging for geophysical UQ
- Takeaway for TRINETRA: Ill-conditioned geophysical inverse problems are nonunique; uses a randomly-initialized CNN as implicit structured prior, samples the posterior via stochastic-gradient Langevin dynamics, and performs BAYESIAN MODEL AVERAGING over samples; d...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-013 | 2608.24288
- arXiv/DOI: arXiv:2608.24288
- Authors: Dong; Li; Yajima
- Title: Sensor Drift Compensation via Olfactory System and Reservoir Computing
- Year / Venue: 2026 / ICANN 2026
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: sample-wise ONLINE drift compensation, SNN+reservoir
- Takeaway for TRINETRA: Addresses SENSOR DRIFT that degrades long-term reliability via gradual response shifts; conventional methods are batch; proposes true sample-wise ONLINE (no buffering) drift compensation using spiking neural nets (STDP feature adaptation) +...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-014 | 2503.09947
- arXiv/DOI: arXiv:2503.09947
- Authors: Xia; Liu; Liu; Fang; Lu; Oymak; Currie; Liu
- Title: Identifying Trustworthiness Challenges in Deep Learning for Continental-Scale Water Quality Prediction
- Year / Venue: 2025 / Nexus (Cell Press)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: LSTM/DeepONet/Informer: spatial generalization to ungauged POOR
- Takeaway for TRINETRA: Multi-dimensional trustworthiness benchmark of LSTM, DeepONet, Informer on 37yr / 482 US basins predicting 20 water-quality vars; finds systematic performance disparities by process complexity + data availability; management-critical variab...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-015 | 2405.18929
- arXiv/DOI: arXiv:2405.18929
- Authors: Takahashi; Iwata; Kumagai; Yamanaka
- Title: Deep Positive-Unlabeled Anomaly Detection for Contaminated Unlabeled Data
- Year / Venue: 2026 / Neurocomputing
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: PU learning + deep SVDD/AE when unlabeled data is contaminated
- Takeaway for TRINETRA: Semi-supervised anomaly detection usually assumes unlabeled data is mostly normal, but in practice it is CONTAMINATED with anomalies, weakening training; proposes deep positive-unlabeled anomaly detection integrating PU learning with autoen...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-016 | 2212.12103
- arXiv/DOI: arXiv:2212.12103
- Authors: Wang; Chen; Guo; Li; Yu
- Title: Bridging the Domain Gap in Satellite Pose Estimation: a Self-Training Approach
- Year / Venue: 2022 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: self-training UDA with geometric constraints, pseudo-labels
- Takeaway for TRINETRA: Unsupervised domain adaptation for satellite pose estimation via self-training with domain-agnostic GEOMETRIC constraints; iterates pseudo-label generation + network training; won 1st on the sunlamp task of the 2nd Satellite Pose Estimation...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-017 | 2309.13207
- arXiv/DOI: arXiv:2309.13207
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Evidential Deep Learning: Enhancing Predictive Uncertainty Estimation for Earth System Science
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: EDL = one-model aleatoric+epistemic UQ for geoscience
- Takeaway for TRINETRA: Robust predictive UQ is critical for weather/climate; ensembles decompose uncertainty but are expensive; parametric DL estimates uncertainty with ONE model but misses epistemic; EVIDENTIAL deep learning estimates BOTH aleatoric + epistemic...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-018 | 2604.06387
- arXiv/DOI: arXiv:2604.06387
- Authors: Yanes Luis; Casado Perez; Mendoza Barrionuevo; Diop; Toral Marin; Gutierrez Reina
- Title: Uncertainty Estimation for Deep Reconstruction in Aquatic Disaster Scenarios with Autonomous Vehicles
- Year / Venue: 2026 / arXiv (cs.RO)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: EDL beats GP/MC-dropout/ensembles at UQ + lowest cost
- Takeaway for TRINETRA: Compares Gaussian Processes, MC-Dropout, Deep Ensembles, and Evidential Deep Learning for scalar-field reconstruction + uncertainty decomposition from SPARSE sensor observations (aquatic monitoring, informative path planning); EDL gives bes...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-019 | 2110.09497
- arXiv/DOI: arXiv:2110.09497
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Gradient boosting with extreme-value theory for wildfire prediction
- Year / Venue: 2022 / arXiv (stat.ML)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: EVT-justified GB loss + SPATIAL cross-validation scheme
- Takeaway for TRINETRA: Team Kohrrelation's EVA-2021-challenge approach to predicting wildfire COUNTS and SIZES over the US; uses EXTREME-VALUE-THEORY ideas in an ML context with theoretically-justified loss functions for gradient boosting, and devises a SPATIAL C...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-020 | 2509.23240
- arXiv/DOI: arXiv:2509.23240
- Authors: Alahyari
- Title: More Data or Better Algorithms: Latent Diffusion Augmentation for Deep Imbalanced Regression
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: LatentDiff synthesizes minority-region features for DIR
- Takeaway for TRINETRA: Real regression data is heavily skewed; models learn majority samples and fail on MINORITY labels; deep imbalanced regression (DIR) lacked data-level solutions for high-dim inputs; proposes LatentDiff - conditional diffusion with priority-b...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-021 | 2306.06599
- arXiv/DOI: arXiv:2306.06599
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Variational Imbalanced Regression: Fair Uncertainty Quantification via Probabilistic Smoothing
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: VIR: imbalanced regression + calibrated UQ via NIG
- Takeaway for TRINETRA: Regression models underperform in BOTH accuracy and uncertainty when labels are imbalanced; VIR is a probabilistic DL model that borrows data with similar regression labels to compute a latent variational distribution, predicts normal-inver...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-022 | 2207.12545
- arXiv/DOI: arXiv:2207.12545
- Authors: Dziedzic; Rabanser; Yaghini; Ale; Erdogdu; Papernot
- Title: p-DkNN: Out-of-Distribution Detection Through Statistical Testing of Deep Representations
- Year / Venue: 2022 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: p-values over hidden reps for OOD abstention, Neyman-Pearson
- Takeaway for TRINETRA: Poorly-calibrated confidence makes NNs inadequate for safety-critical use; ability to ABSTAIN on OOD data is as important as classifying in-dist; p-DkNN analyzes similarity structure of intermediate hidden representations to compute p-VALUE...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-023 | 2105.03876
- arXiv/DOI: arXiv:2105.03876
- Authors: Germi; Rahtu; Huttunen
- Title: Selective Probabilistic Classifier Based on Hypothesis Testing
- Year / Venue: 2021 / IEEE EUVIP 2021
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: reject option via Z-test on probabilistic net, low FPR
- Takeaway for TRINETRA: Handles Closed-World-Assumption violation; prior reject methods threshold scores/loss but can't reach the LOW False-Positive-Ratio safety apps need; proposes a rejection option via HYPOTHESIS TESTING with probabilistic networks - estimates...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-024 | 2508.18045
- arXiv/DOI: arXiv:2508.18045
- Authors: Wang; Borsoi; Breloy; Richard
- Title: Riemannian Change Point Detection on Manifolds with Robust Centroid Estimation
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: streaming CPD, robust Huber vs Karcher centroid test stat
- Takeaway for TRINETRA: Non-parametric change-point detection in STREAMING time series on Riemannian manifolds; monitors abrupt changes in the center of mass but avoids fragile step-size tuning by comparing a change-SENSITIVE Karcher mean vs a change-ROBUST Huber-...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-025 | 2005.05385
- arXiv/DOI: arXiv:2005.05385
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Process Knowledge Driven Change Point Detection for Automated Model Calibration
- Year / Venue: 2020 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: PD-CPD fuses process knowledge into change detection
- Takeaway for TRINETRA: Data-driven change-point methods assume changes are extraneous to the system and ignore available PROCESS KNOWLEDGE; proposes PD-CPD, a unified process-driven multivariate change-point framework combining CPD with ML and domain process mode...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-026 | 2510.10799
- arXiv/DOI: arXiv:2510.10799
- Authors: Nie; Kumar; Chen; Zhao; Skulovich; Yoo; Pflug; Ahmad; Konapala
- Title: Rethinking deep learning: linear regression remains a key benchmark in predicting terrestrial water storage
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: LINEAR REGRESSION beats LSTM + Temporal-Fusion-Transformer for TWS
- Takeaway for TRINETRA: Using the open global HydroGlobe dataset (baseline from a land-surface model + an advanced version with multi-source remote-sensing data assimilation), shows LINEAR REGRESSION is a robust benchmark that OUTPERFORMS the more complex LSTM and...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-027 | 1707.06611
- arXiv/DOI: arXiv:1707.06611
- Authors: Fang; Shen; Kifer; Yang
- Title: Prolongation of SMAP to Spatio-temporally Seamless Coverage of Continental US Using a Deep Learning Neural Network
- Year / Venue: 2017 / Geophysical Research Letters 2017 (DOI 10.1002/2017GL075619)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: first LSTM in hydrology; gap-fills SMAP soil moisture, robust spatial extrapolation
- Takeaway for TRINETRA: First application of LSTM in hydrology: predicts SMAP L3 surface soil moisture from atmospheric forcing + model-simulated moisture + static physiographic attributes, removing most model bias and achieving RMSE<0.035, correlation>0.87 over 7...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-028 | 2006.08573
- arXiv/DOI: arXiv:2006.08573
- Authors: Zaidi; Zela; Elsken; Holmes; Hutter; Teh
- Title: Neural Ensemble Search for Uncertainty Estimation and Dataset Shift
- Year / Venue: 2021 / NeurIPS 2021
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: VARYING-architecture ensembles beat deep-ensembles on calibration + dataset shift
- Takeaway for TRINETRA: Deep ensembles (SOTA UQ) only ensemble random inits of a FIXED architecture; proposes building ensembles with VARYING architectures, exploiting architectural variation as a diversity source; the resulting ensembles beat deep ensembles on ac...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-029 | 2512.05140
- arXiv/DOI: arXiv:2512.05140
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FlowEO: Generative Unsupervised Domain Adaptation for Earth Observation
- Year / Venue: 2025 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: generative unsupervised domain adaptation for EO
- Takeaway for TRINETRA: FlowEO: a generative UNSUPERVISED domain-adaptation approach for Earth-observation imagery (adapting a model to a new unlabeled target domain).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-030 | 2201.07125
- arXiv/DOI: arXiv:2201.07125
- Authors: Faber; Corizzo; Sniezynski; Baron; Japkowicz
- Title: WATCH: Wasserstein Change Point Detection for High-Dimensional Time Series Data
- Year / Venue: 2022 / IEEE Big Data 2021
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: unsupervised Wasserstein CPD for high-dim unlabeled streams
- Takeaway for TRINETRA: WATCH: Wasserstein-distance change-point detection that models an initial distribution and monitors its drift as new points arrive, giving accurate robust UNSUPERVISED detection in high-dimensional UNLABELED streams (where most CPD methods...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-031 | 2602.07252
- arXiv/DOI: arXiv:2602.07252
- Authors: Kor; Gaikwad; Patra; Miller
- Title: Beyond Euclidean Summaries: Online Change Point Detection for Distribution-Valued Data
- Year / Venue: 2026 / arXiv (eess.SP)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: online CPD on distribution/shape geometry, not moment summaries
- Takeaway for TRINETRA: Argues existing online CPD relies on fixed-dim Euclidean (moment/feature) summaries that OBSCURE changes in distributional SHAPE/geometry; proposes an intrinsic distribution-valued online CPD, and contributes challenging multi-entity multiv...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-032 | 2601.18509
- arXiv/DOI: arXiv:2601.18509
- Authors: Sabashvili
- Title: Conformal Prediction Algorithms for Time Series Forecasting: Methods and Benchmarking
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: survey+benchmark of CP for time series; temporal dependence BREAKS exchangeability
- Takeaway for TRINETRA: Critically surveys + benchmarks conformal-prediction methods for TIME-SERIES forecasting, where temporal dependence VIOLATES the exchangeability assumption that standard CP coverage guarantees need; categorizes solutions (relax exchangeabil...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-033 | 2202.07282
- arXiv/DOI: arXiv:2202.07282
- Authors: Zaffran; Dieuleveut; Feron; Goude; Josse
- Title: Adaptive Conformal Predictions for Time Series
- Year / Venue: 2022 / arXiv (stat.ML; cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: ACI/AgACI online-adaptive CP maintains coverage under distribution shift (no exchangeability)
- Takeaway for TRINETRA: Argues Adaptive Conformal Inference (ACI, Gibbs & Candes 2021) is a sound procedure for time series with general dependency; theoretically analyses the learning-rate's effect on efficiency (exchangeable + autoregressive cases); proposes AgA...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-034 | 2402.09056
- arXiv/DOI: arXiv:2402.09056
- Authors: Jurgens; Meinert; Bengs; Hullermeier; Waegeman
- Title: Is Epistemic Uncertainty Faithfully Represented by Evidential Deep Learning Methods?
- Year / Venue: 2024 / ICML 2024
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: CRITICAL caveat: EDL second-order losses hard to optimize; epistemic uncertainty only RELATIVE
- Takeaway for TRINETRA: Theoretical critique of evidential deep learning (EDL): EDL extends ERM to predict SECOND-ORDER distributions over outcomes and read off epistemic+aleatoric uncertainty, but this paper proves difficulties OPTIMIZING second-order loss functi...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-035 | 2210.08470
- arXiv/DOI: arXiv:2210.08470
- Authors: Stucchi; Frittoli; Boracchi
- Title: Class Distribution Monitoring for Concept Drift Detection
- Year / Venue: 2022 / IJCNN 2022
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: deployment monitoring
- Takeaway for TRINETRA: CDM monitors class-conditional distributions via QuantTree change detection; controls Average Run Length (ARL0 = expected time to false alarm).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-036 | 2103.00903
- arXiv/DOI: arXiv:2103.00903
- Authors: Cerqueira; Gomes; Bifet; Torgo
- Title: STUDD: A Student-Teacher Method for Unsupervised Concept Drift Detection
- Year / Venue: 2021 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: deployment monitoring (no labels)
- Takeaway for TRINETRA: Unsupervised drift detection via student mimicking teacher; monitors student-teacher disagreement, needs NO true labels. Landslides are rare so labels are unavailable in real time -> STUDD is the right drift monitor for TRINETRA.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-037 | 2311.15654
- arXiv/DOI: arXiv:2311.15654
- Authors: Azib; Renard; Garnier; Genot; Andre
- Title: Event Detection in Time Series: Universal Deep Learning Approach
- Year / Venue: 2024 / arXiv (stat.ML)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: rare-event detection
- Takeaway for TRINETRA: Regression-based (not binary-classification) event detector handles rare events + imbalance + interval events in one framework. Alternative formulation for TRINETRA's rare-hazard detection; avoids per-timestep binary-label pathology.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-038 | 2205.12070
- arXiv/DOI: arXiv:2205.12070
- Authors: Lin; Chen; et al.
- Title: Deep Reinforcement Learning for Multi-class Imbalanced Training
- Year / Venue: 2022 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: imbalance / RL reward
- Takeaway for TRINETRA: Dueling+double DQN with custom reward for extreme multi-class imbalance; RL agent learns minority-sensitive policy. Supports casting TRINETRA's rare-alarm problem as cost-sensitive RL; informs reward shaping (Bug #9) under imbalance.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-039 | 2501.15196
- arXiv/DOI: arXiv:2501.15196
- Authors: Sanchez-Ferrera; Calvo; Lozano
- Title: A Review on Self-Supervised Learning for Time Series Anomaly Detection
- Year / Venue: 2025 / ACM Comput. Surv.
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: SSL anomaly head
- Takeaway for TRINETRA: Survey: unsupervised AD overfits known normal + fails to adapt to unseen normality; SSL pretext tasks help.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-040 | 2308.09296
- arXiv/DOI: arXiv:2308.09296
- Authors: Darban; et al.
- Title: CARLA: Self-supervised Contrastive Representation Learning for Time Series Anomaly Detection
- Year / Venue: 2024 / Pattern Recognition
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: SSL anomaly head
- Takeaway for TRINETRA: Contrastive SSL for TSAD; tight normal boundaries cause high FP + poor generalization; CARLA learns richer normal reps. Concrete SOTA method + the exact FP pathology TRINETRA risks; informs anomaly-module choice & FA control.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-041 | 2310.17432
- arXiv/DOI: arXiv:2310.17432
- Authors: Goodier; Campbell
- Title: Likelihood-based Out-of-Distribution Detection with Denoising Diffusion Probabilistic Models
- Year / Venue: 2023 / BMVC 2023
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: OOD gating
- Takeaway for TRINETRA: Complexity-corrected likelihood ratio for OOD with diffusion models. Option for TRINETRA to flag OOD sensor inputs (novel storm regimes) before trusting the encoder; gate on OOD (robustness).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-042 | 2208.03566
- arXiv/DOI: arXiv:2208.03566
- Authors: Macedo; Ludermir
- Title: Towards Robust Deep Learning using Entropic Losses
- Year / Venue: 2022 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: OOD rejection
- Takeaway for TRINETRA: Entropic losses + detection scores let a net 'know the unknown' and reject OOD inputs; also calibrates probabilities. TRINETRA should reject-and-defer to physics/shield on OOD rather than emit a confident anomaly; supports fail-safe design.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-043 | 2510.09452
- arXiv/DOI: arXiv:2510.09452
- Authors: Abu Zaid; Katzke; Mueller; Neider
- Title: On Uniformly Scaling Flows: A Density-Aligned Approach to Deep One-Class Classification
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: Deep SVDD anomaly head
- Takeaway for TRINETRA: Proves uniformly-scaling normalizing flows reduce to a Deep SVDD objective with collapse-preventing regularization; drop-in replacement improves stability+accuracy.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-044 | 2412.10792
- arXiv/DOI: arXiv:2412.10792
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Audio-based Anomaly Detection in Industrial Machines Using Deep One-Class SVDD
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: Deep SVDD validation
- Takeaway for TRINETRA: Deep SVDD on cheap microphone sensors for condition monitoring. Analogue to TRINETRA's cheap-sensor ethos; shows Deep SVDD works on low-cost acoustic signals (supports cheap-node anomaly detection).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-045 | 2007.11117
- arXiv/DOI: arXiv:2007.11117
- Authors: Carletti; Terzi; Susto
- Title: Interpretable Anomaly Detection with DIFFI: Depth-based Isolation Forest Feature Importance
- Year / Venue: 2021 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: isolation forest interpretability
- Takeaway for TRINETRA: Isolation Forest lacks interpretability; DIFFI gives global/local feature importance + unsupervised feature selection.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-046 | 2210.02558
- arXiv/DOI: arXiv:2210.02558
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Improved Anomaly Detection by Using the Attention-Based Isolation Forest (ABIForest)
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: isolation forest upgrade
- Takeaway for TRINETRA: Attention-weighted isolation forest improves AD over vanilla IF. Direct upgrade option for TRINETRA's isolation-forest ensemble member (anomaly-module robustness).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-047 | 2105.01419
- arXiv/DOI: arXiv:2105.01419
- Authors: Yu; Liu; Lu; Zhang
- Title: Automatic Learning to Detect Concept Drift (Meta-ADD)
- Year / Venue: 2021 / arXiv (cs.AI)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: drift-type classification
- Takeaway for TRINETRA: Meta-ADD learns to CLASSIFY the TYPE of concept drift (not just detect magnitude) via prototypical net + stream active learning.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-048 | 2606.20216
- arXiv/DOI: arXiv:2606.20216
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Learner-based Concept Drift Detection: Analysis and Evaluation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: drift detector eval
- Takeaway for TRINETRA: Theoretical+empirical evaluation of many drift-detection algorithms on synthetic+real streams. Gives TRINETRA an evidence base to pick a drift detector + eval protocol (test discipline for #8).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-049 | 2203.17155
- arXiv/DOI: arXiv:2203.17155
- Authors: Jiang; Huang; Grebogi; Lai
- Title: Predicting extreme events from data using deep machine learning: when and where
- Year / Venue: 2022 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: extreme-event space-time prediction
- Takeaway for TRINETRA: DCNN predicts extreme events in time (when) + space (where) from 2D image snapshots; notes spatial bias in event occurrence HURTS accuracy.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-050 | 2605.21742
- arXiv/DOI: arXiv:2605.21742
- Authors: McDowell; Stromberg; Sankar
- Title: Correcting Class Imbalance in Prior-Data Fitted Networks for Tabular Classification
- Year / Venue: 2026 / ITW
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: imbalance: thresholding
- Takeaway for TRINETRA: Under class imbalance, THRESHOLDING works exceptionally well due to PFN calibration; downsampling comparable + cheaper; loss-based strategies impossible in ICL.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-051 | 2007.12229
- arXiv/DOI: arXiv:2007.12229
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: SeismoFlow -- Data augmentation for the class imbalance problem
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: imbalance: generative aug
- Takeaway for TRINETRA: Glow-based flow generative model interpolates latent space to synthesize rare-class seismograms for imbalance.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-052 | 2312.01530
- arXiv/DOI: arXiv:2312.01530
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Evaluation of Active Feature Acquisition Methods for Time-varying Feature Settings
- Year / Venue: 2025 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: cost-aware sensing + shift
- Takeaway for TRINETRA: Deploying a feature-acquisition agent itself TRIGGERS distribution shift; proposes AFAPE evaluation under NDE/NUC assumptions.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-053 | 2108.04907
- arXiv/DOI: arXiv:2108.04907
- Authors: Sendera; Smieja; Maziarka; Struski; Spurek; Tabor
- Title: Flow-based SVDD for anomaly detection (FlowSVDD)
- Year / Venue: 2021 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: Deep SVDD collapse fix
- Takeaway for TRINETRA: Standard Deep SVDD can COLLAPSE the bounding hypersphere to a point (degenerate solution); FlowSVDD uses flow-based models to naturally PREVENT collapse + beats related deep-SVDD methods.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-054 | 2302.12127
- arXiv/DOI: arXiv:2302.12127
- Authors: Yamanishi; Hirai
- Title: Detecting Signs of Model Change with Continuous Model Selection (Descriptive Dimensionality)
- Year / Venue: 2023 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A14 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: early change-sign detection
- Takeaway for TRINETRA: Descriptive dimensionality (Ddim) tracks real-valued model complexity to raise EARLY-WARNING of model/regime change BEFORE it fully actualizes.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-055 | 1204.6231
- arXiv/DOI: arXiv:1204.6231
- Authors: Boettiger; Hastings
- Title: Quantifying Limits to Detection of Early Warning for Critical Transitions
- Year / Venue: 2012 / J. Royal Society Interface
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: EWS false-alarm/miss error rates
- Takeaway for TRINETRA: Generic early-warning indicators (rising variance, increased return time) for critical transitions SELDOM characterize their own error rates; a model-based framework quantifies the reliability-vs-sensitivity (false-alarm vs miss) trade-off...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-056 | 1203.0541
- arXiv/DOI: arXiv:1203.0541
- Authors: Nandi; Nayak; Roy; Sarkar
- Title: Hypothesis Testing and Decision Theoretic Approach for Fault Detection in Wireless Sensor Networks
- Year / Venue: 2012 / arXiv (cs.NI)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: Neyman-Pearson/Bayes WSN fault vs event
- Takeaway for TRINETRA: Separates NOISE-related measurement error from genuine SENSOR FAULT in WSN event detection, folding error probabilities into optimal detection via Neyman-Pearson and Bayes tests.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-057 | 1509.06065
- arXiv/DOI: arXiv:1509.06065
- Authors: Bhuiyan; G. Wang; J. Wu; J. Cao
- Title: Dependable Structural Health Monitoring Using Wireless Sensor Networks (DependSHM)
- Year / Venue: 2015 / arXiv (cs.DC)
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: n/r
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: faulty sensors corrupt events undetected
- Takeaway for TRINETRA: DependSHM: shows faulty sensors can CORRUPT a structural-health event (e.g., damage) WITHOUT being detected - signals from one faulty node mimic a real damage signature - and builds a distributed fault-detection/tolerance framework under WS...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-058 | 2610.01994
- arXiv/DOI: arXiv:2610.01994
- Authors: (backfill)
- Title: Simple gradient-boosted baseline beats deep models for wildfire ignition prediction
- Year / Venue: 2026 / arXiv
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A8 | phase: P2
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P2] simplicity dominates (T1/CR-02)
- Takeaway for TRINETRA: Second-domain confirmation of CR-02: a gradient-boosted baseline matches/beats deep models for wildfire ignition under honest evaluation. Hardens the mandatory simple-baseline rule.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-059 | 2610.04392
- arXiv/DOI: arXiv:2610.04392
- Authors: (backfill)
- Title: Evaluation pitfalls and rare-event collapse in ML hazard prediction
- Year / Venue: 2026 / arXiv
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A8 | phase: P2
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P2] eval/efficiency + rare-event (FM-21)
- Takeaway for TRINETRA: Documents metric pitfalls and rare-event performance collapse; reinforces FM-21 (frame-AUC optimism) and the need for cost-loss / rare-event-aware metrics.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-060 | 2606.07593
- arXiv/DOI: arXiv:2606.07593
- Authors: (backfill)
- Title: Corruption-robustness fine-tuning does not transfer across corruption types (ViT)
- Year / Venue: 2026 / arXiv
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A14 | phase: P2
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P2] robustness non-transfer (augmentation != robustness)
- Takeaway for TRINETRA: Fine-tuning for one corruption class does not transfer to others; augmentation is not general robustness. Build risk: do not claim weather/corruption robustness from training on one corruption type.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-061 | 2605.15894
- arXiv/DOI: arXiv:2605.15894
- Authors: Chodavarapu
- Title: Uncertainty-Aware Wildfire Smoke Density Classification via CBAM-EfficientNet + Evidential DL
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A8 | phase: P2
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P2] evidential UQ + selective pred (WS4/WS6)
- Takeaway for TRINETRA: EfficientNet-B3+CBAM evidential head → Light/Moderate/Heavy smoke + decomposed epistemic(vacuity)/aleatoric(dissonance) in one pass; selective prediction (retain 50%) 96.7%; vacuity = cheap OOD/scan-quality gate + abstention.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-062 | 2607.28248
- arXiv/DOI: arXiv:2607.28248
- Authors: (backfill)
- Title: Survey: Uncertainty Quantification for Trustworthy Deep Learning — methods and measures
- Year / Venue: 2026 / arXiv
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A14 | phase: P2
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P2] UQ backbone (WS6)
- Takeaway for TRINETRA: Aleatoric vs epistemic; method menu+limits (Bayesian/MC-Dropout/Deep Ensembles → efficient SWAG/BatchEnsemble/last-layer-Bayes/DUQ). WS6: Deep Ensemble on Kaggle, cheaper approximations at edge.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-063 | 2610.03369
- arXiv/DOI: arXiv:2610.03369
- Authors: Ardaiz; Budati; Habibnia
- Title: MoE for Crypto Order Execution: Training Stability/Tail Risk/Failure Modes
- Year / Venue: 2026 / arXiv (q-fin.TR)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A8 | phase: P3
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P3] deep-RL eval-critique → RB-13
- Takeaway for TRINETRA: DRL varies across seeds; failure-mode attribution REVERSES between 30 and 100 seeds; MoE 'fix' masks training-spec failure (annealed-explore alone fixes collapse 12/100→0/100, McNemar p=4.9e-4); all RL worse than TWAP 0.39bps/immediate 0.21...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-064 | 2608.16654
- arXiv/DOI: arXiv:2608.16654
- Authors: Prakash; Desai; Srijith
- Title: Galaxy Morphology Classification: Uncertainty Modeling and OOD Detection
- Year / Venue: 2026 / Astronomy & Computing
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A14 | phase: P3
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P3] OOD/UQ WS8 (India)
- Takeaway for TRINETRA: IsoMaxPlus distance-based logits: free OOD (TNR@TPR95 +~90%) + ECE 0.0095→0.0026 (~73%), 97% acc, NO outliers/tuning; +MC-Dropout for Bayesian UQ. Entropy+min-dist = auditable unreliable-prediction flag.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-065 | 2609.31142
- arXiv/DOI: arXiv:2609.31142
- Authors: Hu; Zhang; Liu; Zeng; Zeng; Wang; Wang
- Title: JevAdvBench: Benchmark + Black-Box Attacks for RL-for-Calibrated-Decisions Models
- Year / Venue: 2026 / arXiv (cs.CR)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A8 | phase: P3
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P3] adversarial robustness/eval WS5 → RB-18
- Takeaway for TRINETRA: First adversarial benchmark for RLCD (typed-decision) models that software acts on without a human.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-066 | 2606.00690
- arXiv/DOI: arXiv:2606.00690
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DistMatch: Adaptive Binning via Distribution Matching for Robust Sequential Conformal Prediction
- Year / Venue: 2026 / arXiv (stat.ME/cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A14 | phase: P3
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P3] UQ/conformal; resolves CR-04
- Takeaway for TRINETRA: Sequential CP valid under temporal dependence+shift: patching→approximate LOCAL exchangeability; matching-tree groups similar residual patches (KS-stat, label-free) into adaptive bins; per-bin quantile regression; coverage guarantee via DIS...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-067 | 2605.06643
- arXiv/DOI: arXiv:2605.06643
- Authors: Dong; Li; Li; Khan; Chatzi; Fink
- Title: Are We Making Progress in Multimodal Domain Generalization? (MMDG-Bench)
- Year / Venue: 2026 / NeurIPS 2026
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A8 | phase: P3
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P3] eval-critique; consolidates CR-02 + CR-07
- Takeaway for TRINETRA: MMDG-Bench: 6 datasets × 3 tasks × 6 modality combos × 9 methods, 7402 networks / 95 cross-domain tasks.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-068 | 2607.24683
- arXiv/DOI: arXiv:2607.24683
- Authors: Mena; Ienco; Interdonato; Dantas; Besnard
- Title: Co-Learning for Missing Arbitrary Modalities in Multi-modal Classification (Co4Miss)
- Year / Venue: 2026 / arXiv (cs.CV/cs.AI/cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A14 | phase: P3
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P3] missing-arbitrary-modality robustness via co-learning (EO benchmarks)
- Takeaway for TRINETRA: Co-LEARNING (not fusion) for missing ARBITRARY modalities (any subset absent, no predefined pattern).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-069 | 2610.01384
- arXiv/DOI: arXiv:2610.01384
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: CLEAR: Robust Evidential Learning Through Latent Consistency
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A14 | phase: P4 | re-cited 2x
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P4] SUPPORTS C-13: post-hoc fix for confident-but-wrong in sparse/OOD regions
- Takeaway for TRINETRA: Post-hoc method operating on a FROZEN base evidential-deep-learning model; Conflict-Aware Latent Evidence Adjustment: per-sample conflict score C(x) from latent-space geometry, evidence scale s(x)=exp(-delta*C(x)) downweights unsupported (O...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-070 | 2608.14391
- arXiv/DOI: arXiv:2608.14391
- Authors: Liang; Ma; Zhou; Wan; Chen; Mei; et al.
- Title: Can We Defend Against AI-Generated Video Attacks on Real-World Crisis Events? (RA-Bench)
- Year / Venue: 2026 / arXiv (cs.CV) v2
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A8 | phase: P4
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P4] LIFE-SAFETY ANCHOR for C-16/WS2: no deepfake detector generalizes
- Takeaway for TRINETRA: RA-Bench: 17,886 videos = 1,830 real-video anchors across 10 social-risk categories + 16,056 generated clips from 9 generators (4 open + 5 closed).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-071 | 2610.03649
- arXiv/DOI: arXiv:2610.03649
- Authors: Goudemant; Szywala; Francesconi; Aubrun; Bobichon; Bellizzi; Girard
- Title: On-Board Anomaly Detection for Efficient Marine Environmental Monitoring
- Year / Venue: 2024 / OBPDC 2024 (zenodo 13850918)
- Read depth: FT | local note: no | ledger axis/WS: A14 | phase: P4
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P4] C-08/WS8: SSL-encoder -> classical-anomaly stack, edge-feasible
- Takeaway for TRINETRA: Marine-event (oil spill / algal bloom / sediment flood) detection pipeline for EO satellites: a SELF-SUPERVISED encoder compresses multi/hyperspectral images into a reduced latent, then an ML anomaly detector flags deviations from normal se...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-072 | 2609.16964
- arXiv/DOI: arXiv:2609.16964
- Authors: Ali; Basir; Nawaz; Arain; Ali
- Title: HUMAID-NER: Disaster Tweet Dataset for Joint NER and Event Classification
- Year / Venue: 2026 / Asian Bulletin of Big Data Mgmt 6(1) 138-152
- Read depth: ABS | local note: no | ledger axis/WS: A8 | phase: P5 | re-cited 2x
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P5] WS2/WS3: structured crisis-media extraction reference (low-trust channel)
- Takeaway for TRINETRA: 60,000 English disaster tweets, BIO span annotations (~175,000 spans, 10 operational entity types), built on HumAID; joint NER + humanitarian-event classification via shared RoBERTa-large + homoscedastic uncertainty weighting; released data...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-073 | 2607.11969
- arXiv/DOI: arXiv:2607.11969
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Did We Actually Fix It? Adversarial Stress-Test of Post-Point-Adjustment Metrics
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] best-of-N inflates affiliation + ALL ROC metrics; prefer VUS-PR
- Takeaway for TRINETRA: At N=1 no post-PA metric gameable; under best-of-N seed-shopping affiliation-F1 + VUS-ROC inflate (0.98 by N=41) while PR-based + PA%K stay floored (UCR/SMD/SMAP/MSL/NAB/PSM). REPORT single-run or disclose N; prefer VUS-PR.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-074 | 2603.18985
- arXiv/DOI: arXiv:2603.18985
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Revisiting OmniAnomaly: PCA-based comparison on SMD
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] SIMPLE-BASELINE: PCA >= OmniAnomaly without point-adjust
- Takeaway for TRINETRA: 100 runs x 28 machines identical thresholding: PCA comparable F1 and OUTPERFORMS OmniAnomaly when PA removed; large per-machine variability. Simple-baselines-first mandate evidence. Source-reported. NEW. literature_map D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-075 | 2608.21854
- arXiv/DOI: arXiv:2608.21854
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Look Inside Each Video: Rethinking How VAD Is Evaluated
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] Micro-AUROC != temporal localization; report Within-AUROC
- Takeaway for TRINETRA: Within-video pairs 0.071-0.388% of all pairs; per-video-mean keeps median 98.8% of Micro-AUROC margin at 50% Within-AUROC (120 runs). High Micro-AUROC does NOT establish localization. Source-reported. NEW. literature_map A.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-076 | 2405.12096
- arXiv/DOI: arXiv:2405.12096
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PATE: Proximity-Aware Time-series Anomaly Evaluation
- Year / Venue: 2024 / KDD 2024
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] delay-aware metric fits fire early-warning
- Takeaway for TRINETRA: Proximity-weighted PR AUC with buffer zones around anomaly intervals; rewards early, penalizes late detection; shows PA-F1 fails to characterize detectors. Primary metric candidate for latency-critical EWS. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-077 | 2311.11235
- arXiv/DOI: arXiv:2311.11235
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Unraveling the Anomaly in TSAD: Self-Supervised Tri-domain (TriAD)
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] many benchmark anomalies detectable by random functions
- Takeaway for TRINETRA: Temporal/frequency/residual SSL + discord discovery re-evaluated on UCR + PA%K/affiliation; src-reported 3x PA%K-F1 over SOTA deep, +50% vs discord algos. Names trivial-benchmark pitfall. Source-reported. NEW. literature_map D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-078 | 2511.18739
- arXiv/DOI: arXiv:2511.18739
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A Problem-Oriented Taxonomy of Evaluation Metrics for TSAD
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] pick metric by objective; NAB+PA weak to random scores
- Takeaway for TRINETRA: 20+ metrics on 6 axes; NAB + Point-Adjust limited resistance to random-score inflation; delay-aware fire alerting => timeliness-reward + PR-based. Source-reported. NEW. literature_map D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-079 | 2409.13053
- arXiv/DOI: arXiv:2409.13053
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Towards Unbiased Evaluation of TSAD - Balanced Point Adjustment
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] standard PA biased toward TPs; axiomatic fairer BA
- Takeaway for TRINETRA: Proposes Balanced point adjustment with axiomatic fairness guarantees as a less-biased event-level credit scheme. Source-reported. NEW. literature_map D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-080 | 2609.39215
- arXiv/DOI: arXiv:2609.39215
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: In a Streaming World Should You Stand Still? Benchmark of AD in Streams
- Year / Venue: 2026 / KDD 2026
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] static TSAD OUTPERFORMS streaming/adaptive in most settings
- Takeaway for TRINETRA: First large-scale streaming-vs-static TSAD comparison + TSB-drift real-drift dataset; src-reported static significantly beats adaptive. 'Adapt online' not automatically better -> static + periodic retrain. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-081 | 2608.14089
- arXiv/DOI: arXiv:2608.14089
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Regime-Conditional Verification: Correctness Estimation for Monitoring Safety Classifiers
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] cheap label-free drift/health wrapper over deployed detector
- Takeaway for TRINETRA: Estimates P(prediction disagrees with policy) from internal reps; label-free drift signal, triggers repair only when needed; src-reported catches up to 0.81 of missed unsafe content, detects all 10 held-out attack campaigns.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-082 | 2608.20663
- arXiv/DOI: arXiv:2608.20663
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Shortcut Learning in a Public Grape Disease Dataset
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] shortcut INVISIBLE to in-dist eval; only OOD negatives reveal
- Takeaway for TRINETRA: Annotation granularity amplifies shortcut: one class draws 65.7% of FP boxes on 5,156 cross-species images (13.41x); shrinking boxes cut cross-species FP 66% (placebo-controlled). Audit fire datasets with OOD negatives. Source-reported.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-083 | 2608.03926
- arXiv/DOI: arXiv:2608.03926
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PRISM: Time-Series-to-Image Representations for Multivariate AD
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] reuse vision backbones on sensors; VUS-PR
- Takeaway for TRINETRA: TS->multi-channel images; >7000 experiments best VUS-PR on 10/14 datasets (+41% avg); ImageNet frozen encoders keep 92% at 1.8x faster. Source-reported. NEW. literature_map B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-084 | 2606.20055
- arXiv/DOI: arXiv:2606.20055
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PaAno+: Multiscale Encoding + Cross-Variable Attention for TSAD
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] compact edge-feasible MTAD on rigorous TSB-AD
- Takeaway for TRINETRA: Patch multiscale conv + cross-scale/variable attention + patch-sorting pretext; SOTA on TSB-AD (uni+multi), VUS-PR gains; for resource-limited terminals. Source-reported. NEW. literature_map B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-085 | 2608.15727
- arXiv/DOI: arXiv:2608.15727
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FirstDiff: One-Step Diffusion AD for Multivariate TS
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] one-step diffusion -> edge-feasible latency
- Takeaway for TRINETRA: First reverse-step noise suffices; model its normal distribution so inference = single denoise eval; src-reported SOTA on 5 benchmarks. Source-reported. NEW. literature_map B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-086 | 2609.34804
- arXiv/DOI: arXiv:2609.34804
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Physics-Attested Federated Learning for Water Infrastructure AD
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] CPS invariants = detector + anti-poisoning/spoof integrity gate
- Takeaway for TRINETRA: Mines process invariants as verifiable admission gate (zk-SNARK privacy); src-reported 9 invariants detect 20/35 SWaT attacks, recovers 69-100% recall lost to replay poisoning. Physics-residual family + P12 threat model. Source-reported.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-087 | 2606.06347
- arXiv/DOI: arXiv:2606.06347
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Attack Detection using Time Series Foundation Models (TimesFM)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] TS foundation model as model-free residual generator
- Takeaway for TRINETRA: TimesFM zero-shot surrogate residual vs replay + stealthy attacks (IEEE 14-bus comparable/superior); predictions can substitute corrupted measurements. Residual generator when no physics model. Source-reported. NEW. literature_map E.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-088 | 2609.21217
- arXiv/DOI: arXiv:2609.21217
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: X-SPUR: Explainable Surprisal-Based Protocol-Aware Unsupervised IDS
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] surprisal + per-protocol Z-score template for alert-spoof stream
- Takeaway for TRINETRA: Packet fields as tokens, causal LM, per-token cross-entropy surprisal + dual top-k% Z-score; TOW-IDS AUC 0.9987, field-level explanations, no handcrafted features. Source-reported. NEW. literature_map E.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-089 | 2606.02256
- arXiv/DOI: arXiv:2606.02256
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: ArrythML: Autoencoder TinyML On-Device Arrhythmia Detection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] realistic tiny-AE envelope on ESP32-S3
- Takeaway for TRINETRA: INT8 AE via TFLite-Micro on ESP32-S3; src-reported recall 84%, F1 79%, ~180KB, 9ms; some 'misclassifications' were mislabeled subtle anomalies (label-noise caveat). Source-reported. NEW. literature_map F.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-090 | 2010.11267
- arXiv/DOI: arXiv:2010.11267
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: MicroNets: NN Architectures for TinyML on Commodity MCUs
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8 | phase: P9
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P9] NAS edge sizing; TinyMLperf anomaly-detection reference
- Takeaway for TRINETRA: Differentiable NAS with op-count latency proxy; SOTA on all 3 TinyMLperf tasks incl. anomaly detection; TFLite-Micro deploy. Edge model-sizing reference. Source-reported. NEW. literature_map F.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-091 | 2601.21293
- arXiv/DOI: arXiv:2601.21293
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Reliability-Calibrated Edge-IoT Early Fault Warning (Physics-Guided Tiny-Mamba Transformer)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] EVT PoT + dual-threshold hysteresis + trimmed-tail streaming alarm budget
- Takeaway for TRINETRA: Tiny-Mamba+Transformer rep module feeds EVT alarm layer; src-reported sub-1MB, Jetson p99 <7ms, better PR-AUC + lower delay under nuisance budget (CWRU/Paderborn/XJTU-SY). Thresholding recipe for score->alarm. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-092 | 2605.13642
- arXiv/DOI: arXiv:2605.13642
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Conformal Anomaly Detection in Python (nonconform)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] split-conformal p-values + BH FDR control = reference thresholding
- Takeaway for TRINETRA: Wraps any PyOD/sklearn detector -> calibrated p-values valid under exchangeability + explicit FDR control; split/shift-aware variants. Our reference impl path replacing hand-picked thresholds. Source-reported. NEW. literature_map P10-A.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-093 | 2609.29580
- arXiv/DOI: arXiv:2609.29580
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: When Identical Rows Disagree: Replication-Robust Anomaly Detection (SCOUT)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] factorwise split-conformal nominal FPR; AUDIT train/test overlap
- Takeaway for TRINETRA: Separates replication-invariant support vs exposure count evidence; 686 OddBench/5 seeds support-only non-inferior to row-wise IF, tracks nominal FPR; 355/690 datasets had train/test overlap. Benchmark-hygiene caution. Source-reported.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-094 | 2606.09874
- arXiv/DOI: arXiv:2606.09874
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Disjoint or Overlapping? Inference Windowing for Reconstruction-Based TSAD
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] REPRO: overlapping inference windows avg +28% rel., reorder rankings
- Takeaway for TRINETRA: Unified multi-seed protocol on TSB-AD/UCR across PCA/DLinear/AE/TimesNet/Transformer; src-reported overlapping inference gives consistent gains and reconstruction baselines strongly competitive. Inference-time choices rival architecture.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-095 | 2607.12454
- arXiv/DOI: arXiv:2607.12454
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Exploring Zero-Shot Foundation Models for Multivariate TSAD
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] NEGATIVE: zero-shot forecasting FM fails on persistent anomalies
- Takeaway for TRINETRA: Zero-shot TimesFM on SWaT not competitive; too-good reconstruction hides persistent anomalies, error only peaks at boundaries -> change-point use only. Caution against naive FM detector. Source-reported. NEW. literature_map P10-B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-096 | 2610.02345
- arXiv/DOI: arXiv:2610.02345
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Mitigating Convergence Collapse in Fixed-Target Anomaly Detectors (KCM/KAR)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] REPRO: reconstruction detectors get WORSE at convergence; early-stop/KAR
- Takeaway for TRINETRA: Fixed-target residual detectors collapse at convergence (residual vanishes on anomalies); fix = Kernel-Anchored Regularizer or deliberate early-stop; KCM training-free closed-form baseline matches neural on ADBench. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-097 | 2603.12916
- arXiv/DOI: arXiv:2603.12916
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Surprised by Attention: Predictable Query Dynamics for TSAD (AxonAD)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] EMA-target masked query-prediction aux score fused with reconstruction
- Takeaway for TRINETRA: Targets cross-channel dependency shifts anomalies reconstruct plausibly; ablations: query-prediction + combined scoring are primary gain drivers on TSB-AD multivariate. Source-reported. NEW. literature_map P10-B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-098 | 2609.16314
- arXiv/DOI: arXiv:2609.16314
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Robust Fault Detection via Self-Supervised Cross-Modal Reconstruction
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] reconstruct-each-modality-from-others + adaptive test-time threshold
- Takeaway for TRINETRA: No temporal-alignment/identical-rate needed; biggest robustness gains in hardest OOD regimes across 3 industrial cases. Fits our IoT+CCTV multimodal fusion under shift. Source-reported. NEW. literature_map P10-B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-099 | 2609.14234
- arXiv/DOI: arXiv:2609.14234
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Graph-Transformer Fraud Detection with Conformal Risk Control (GTFD)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] conformal risk-control head = threshold-free coverage-guaranteed scoring
- Takeaway for TRINETRA: Ablation attributes ~1.9 AUROC to conformal head + ~2.0 to SSL pretrain; ~29% FPR reduction vs strongest baseline. Calibration is first-class. Source-reported. NEW. literature_map P10-C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-100 | 2606.13780
- arXiv/DOI: arXiv:2606.13780
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Conformal Calibration and Look-Elsewhere Effect in Anomaly Detection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] Mondrian/weighted conformal + multiple-testing correction at scale
- Takeaway for TRINETRA: Post-hoc conformal -> valid local p-values; uncorrected pipeline manufactured ~46 sigma false excess from background sculpting; label-free weighted conformal removes it. Multiple-testing correction essential when scanning many sensors.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-101 | 2610.12244
- arXiv/DOI: arXiv:2610.12244
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: RIFT: Relative Isolation From Trees For Anomaly Detection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] deterministic seed-stable Isolation-Forest replacement
- Takeaway for TRINETRA: MST-based IF generalization, parameter-free, recovers closed-form IF limit in 1-D; src-reported IF-comparable accuracy on ADBench with lower seed variance (ensemble). Baseline upgrade. Source-reported. NEW. literature_map P10-D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-102 | 2311.03393
- arXiv/DOI: arXiv:2311.03393
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Sketching Multidimensional Time Series for Fast Discord Mining
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] matrix-profile discord cost independent of #channels; >=50x throughput
- Takeaway for TRINETRA: Sketch makes discord-mining runtime independent of dimensionality; dynamic add/delete of channels; src-reported >=50x throughput minimal quality loss on water/transport data. Interpretable multivariate baseline. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-103 | 2505.17662
- arXiv/DOI: arXiv:2505.17662
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Automating Versatile Time-Series Analysis with Tiny Transformers on Embedded FPGAs
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] QAT 4-bit + Optuna HW-aware search -> integer-only edge accelerator
- Takeaway for TRINETRA: Automated QAT-to-4bit + VHDL gen; src-reported 0.033 mJ/inference, ms latency on Spartan-7 across 6 datasets. Edge training/quant recipe (INT8 for MCU). Source-reported. NEW. literature_map P10-E.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-104 | 2606.13754
- arXiv/DOI: arXiv:2606.13754
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: D2H-AD: Hybrid Hyperdimensional Computing for Anomaly Detection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] HDC binary-ops MCU-friendly detector; encoding is the real contributor
- Takeaway for TRINETRA: Distance+density HDC encoding; ablation HDC encoding alone +5.4% ROC-AUC; outperforms OCSVM/IF/AE across 5 benchmarks, robust to imbalance/noise. Energy-efficient MCU alternative to float AEs. Source-reported. NEW. literature_map P10-E.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-105 | 2601.18135
- arXiv/DOI: arXiv:2601.18135
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Forward Consistency Learning with Gated Context Aggregation for VAD (FoGA)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] tiny U-Net future-frame + forward-consistency; ~2M params, up to 155 FPS
- Takeaway for TRINETRA: Immediate+forward prediction with gated skip fusion + forward-consistency loss; hybrid immediate+forward error score; src-reported outperforms SOTA at up to 155 FPS. Edge CCTV lead candidate (support-only). Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-106 | 2610.11149
- arXiv/DOI: arXiv:2610.11149
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Uni-DSM: Unified Score Matching for Video Anomaly Detection and Anticipation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] denoising-score-matching + SDSM label-free ANTICIPATION (early warning)
- Takeaway for TRINETRA: Noise-conditioned score transformer + motion-aware weighting; SDSM builds supervision from output discrepancies for anticipation without future labels; src-reported SOTA on VAD+VAA. Aligned with early-warning goal (support).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-107 | 2509.22544
- arXiv/DOI: arXiv:2509.22544
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: HyCoVAD: Hybrid SSL-LLM Model for Complex Video Anomaly Detection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS8b | phase: P10
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P10] SSL pre-screen -> LLM validate suspect frames only (cost-controlled escalation)
- Takeaway for TRINETRA: nnFormer SSL screens suspect frames, LLM applies rule-based reasoning only on those; src-reported 72.5% frame-AUC on ComplexVAD (+12.5%) with reduced LLM compute; releases adaptive thresholding protocol. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-108 | 2101.11453
- arXiv/DOI: arXiv:2101.11453
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Meta Adversarial Training against Universal Patches
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T1
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T1] meta-learn evolving universal patches during training, low extra compute
- Takeaway for TRINETRA: raises patch robustness (classification + traffic-light detection); src-reported. Camera front-end hardening. Source-reported. NEW. literature_map P16-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-109 | 2307.02055
- arXiv/DOI: arXiv:2307.02055
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Adversarial Attacks on Image Classification Models: FGSM and Patch Attacks
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T1
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T1] strong pretrained CNNs degrade sharply under FGSM + patch
- Takeaway for TRINETRA: ResNet/GoogleNet/DenseNet on ImageNet; src-reported. Off-the-shelf CCTV classifiers not attack-safe -> human confirmation. Source-reported. NEW. literature_map P16-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-110 | 2411.16162
- arXiv/DOI: arXiv:2411.16162
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Sparse Patches Adversarial Attacks via Extrapolating Point-Wise Information
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T1
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T1] jointly optimizes multiple patches location+perturbation, new SOTA
- Takeaway for TRINETRA: any shape/count; src-reported beats prior sparse/patch. Red-team must cover multi-patch physical threats. Source-reported. NEW. literature_map P16-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-111 | 2206.13405
- arXiv/DOI: arXiv:2206.13405
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Utilizing Class Separation Distance for Corruption Robustness Evaluation (MSCR)
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T2
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T2] interpretable per-dataset corruption metric; tradeoff NOT inherent
- Takeaway for TRINETRA: minimal-separation robustness distance; src-reported augmentation can slightly raise accuracy. Yardstick to compare detector variants under weather/lighting. Source-reported. NEW. literature_map P16-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-112 | 2110.06513
- arXiv/DOI: arXiv:2110.06513
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Benchmarking the Robustness of Spatial-Temporal Models Against Corruptions
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T2
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T2] Transformers > CNNs on corruption; image noise-training may NOT transfer to video
- Takeaway for TRINETRA: Mini Kinetics-C/SSV2-C; src-reported. Fire is temporal -> image tricks may not protect video pipeline. Source-reported. NEW. literature_map P16-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-113 | 2102.11273
- arXiv/DOI: arXiv:2102.11273
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: On Interaction Between Augmentations and Corruptions in Natural Corruption Robustness
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T2
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T2] robustness drops when test corruptions perceptually dissimilar from training augs
- Takeaway for TRINETRA: Minimal Sample Distance; src-reported. Augmentation hardening gives false confidence on unseen field corruptions. Source-reported. NEW. literature_map P16-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-114 | 2206.12654
- arXiv/DOI: arXiv:2206.12654
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: BackdoorBench: A Comprehensive Benchmark of Backdoor Learning
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T3
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T3] 8 attacks x 9 defenses, 8000 pairs; exposes unverified defense claims
- Takeaway for TRINETRA: src-reported standardized protocol. Reusable protocol to vet third-party/pretrained models. Source-reported. NEW. literature_map P16-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-115 | 2407.19845
- arXiv/DOI: arXiv:2407.19845
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: BackdoorBench: Comprehensive Benchmark and Analysis (extended)
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T3
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T3] 20 attacks, 32 defenses, 11492 pairs, 18 analysis tools
- Takeaway for TRINETRA: src-reported corrects unfair comparisons. Current standardized supply-chain poisoning reference. Source-reported. NEW. literature_map P16-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-116 | 2202.11203
- arXiv/DOI: arXiv:2202.11203
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Under-confidence Backdoors Are Resilient and Stealthy Backdoors (LSBA)
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T3
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T3] probabilistic label flipping; high stealth + high ASR, evades human + auto defenses
- Takeaway for TRINETRA: target prob only slightly higher; src-reported. Poisoning hides below confidence-threshold alert logic -> provenance control. Source-reported. NEW. literature_map P16-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-117 | 2603.11365
- arXiv/DOI: arXiv:2603.11365
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: D-SLAMSpoof: Environment-Agnostic LiDAR Spoofing via Dynamic Point Cloud Injection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T4
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T4] point injection compromises SLAM even in feature-rich scenes; ISD-SLAM inertial defense
- Takeaway for TRINETRA: src-reported higher success urban/indoor. Template for cross-checking one sensor vs an independent modality. Source-reported. NEW. literature_map P16-T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-118 | 2307.04692
- arXiv/DOI: arXiv:2307.04692
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Spoofing-Resilient LiDAR-GPS Factor Graph Localization with Chimera Authentication
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T4
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T4] chi-squared residual detector; <5 m nominal, bounds error under spoofing
- Takeaway for TRINETRA: between Chimera auths; src-reported. Signed signals + residual anomaly detection = fusion-integrity pattern. Source-reported. NEW. literature_map P16-T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-119 | 2302.07341
- arXiv/DOI: arXiv:2302.07341
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Cooperative Perception for Safe Control under LiDAR Spoofing
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T4
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T4] neighbor LiDAR + FDII detects fake/removed/adversarial objects
- Takeaway for TRINETRA: CARLA detects each attack pattern; src-reported. Redundancy/cross-sensor voting before alerting. Source-reported. NEW. literature_map P16-T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-120 | 2301.09615
- arXiv/DOI: arXiv:2301.09615
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: ESWORD: Wireless Jamming Attacks in a Real-World Emulated Network
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T5
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T5] HIL jamming on Colosseum (<=50 SDRs); patterns match real jamming
- Takeaway for TRINETRA: src-reported validates emulation fidelity. Safe testbed to assess jamming before deployment. Source-reported. NEW. literature_map P16-T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-121 | 1509.09222
- arXiv/DOI: arXiv:1509.09222
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: On Jamming Against Wireless Networks
- Year / Venue: 2015 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T5
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T5] 1 jammer/AP -> outage 1% to 80%, retransmits double interference
- Takeaway for TRINETRA: Binomial-point-process model; src-reported. Little attacker effort collapses the alert link -> wired/redundant paths + jamming detection. Source-reported. NEW. literature_map P16-T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-122 | 1411.3736
- arXiv/DOI: arXiv:1411.3736
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Energy-Efficient Routing in Wireless Networks in the Presence of Jamming
- Year / Venue: 2014 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T5
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T5] joint outage-allocation + routing + spread-spectrum; energy savings
- Takeaway for TRINETRA: from measured per-node jamming; src-reported. Jamming-aware routing for sensor meshes. Source-reported. NEW. literature_map P16-T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-123 | 1707.07821
- arXiv/DOI: arXiv:1707.07821
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Concept Drift Detection and Adaptation with Hierarchical Hypothesis Testing (HLFR)
- Year / Venue: 2017 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T6
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T6] handles recurrent/abrupt/gradual drift + imbalance; beats SOTA precision/delay
- Takeaway for TRINETRA: src-reported. Principled drift monitoring with Type-I/II analysis. Source-reported. NEW. literature_map P16-T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-124 | 2104.10529
- arXiv/DOI: arXiv:2104.10529
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A Lightweight Concept Drift Detection and Adaptation Framework for IoT Data Streams
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T6
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T6] adaptive LightGBM + optimized sliding window (OASW); high accuracy/efficiency
- Takeaway for TRINETRA: no human intervention; src-reported. Edge-friendly BUT auto-adaptation must be Rule-19-gated (advisory). Source-reported. NEW. literature_map P16-T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-125 | 2404.02572
- arXiv/DOI: arXiv:2404.02572
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Incremental Learning with Concept Drift Detection and Prototype Embeddings for Graph Streams
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T6
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T6] per-class prototype graphs + loss-based drift detector
- Takeaway for TRINETRA: critical-infrastructure modelling; src-reported. Drift-triggered recalibration of a structural model. Source-reported. NEW. literature_map P16-T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-126 | 2206.03669
- arXiv/DOI: arXiv:2206.03669
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Toward Certified Robustness Against Real-World Distribution Shifts
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T7
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T7] neural-symbolic verification of learned-perturbation specs, CEGAR
- Takeaway for TRINETRA: beats verifiers on MNIST/CIFAR shifts; src-reported, small scale. Moves certification toward realistic shifts. Source-reported. NEW. literature_map P16-T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-127 | 1910.14655
- arXiv/DOI: arXiv:1910.14655
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Enhancing Certifiable Robustness via a Deep Model Ensemble (RobBoost)
- Year / Venue: 2019 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T7
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T7] weights base models to maximize a robustness certificate; better clean acc than averaging
- Takeaway for TRINETRA: src-reported. Raise provable robustness with limited accuracy loss (lower bound only). Source-reported. NEW. literature_map P16-T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-128 | 2412.09921
- arXiv/DOI: arXiv:2412.09921
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FaceShield: Defending Facial Image against Deepfake Threats
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T8
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T8] perturbs diffusion attention; JPEG-robust; transfers to GANs; SOTA diffusion disruption
- Takeaway for TRINETRA: src-reported. Proactive protection + compression-robustness concern for CCTV evidence. Source-reported. NEW. literature_map P16-T8.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-129 | 2607.25842
- arXiv/DOI: arXiv:2607.25842
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Adversarial Deepfake Generation and Purification-Based Adversarial Detection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T8
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T8] multi-model PGD evades 12 detectors (90%/57.6%); purification AUROC 0.81-0.98 collapses at JPEG-Q70
- Takeaway for TRINETRA: src-reported. Detector ensembles evadable; single evasion threshold untrustworthy. Source-reported. NEW. literature_map P16-T8.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-130 | 2003.01279
- arXiv/DOI: arXiv:2003.01279
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Disrupting Deepfakes: Adversarial Attacks Against Facial Manipulation Systems
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P16-T8
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P16-T8] class-transferable attacks + AT-for-GANs; blur defeated by spread-spectrum
- Takeaway for TRINETRA: src-reported. Defenses+evasions co-evolve -> continuous red-teaming. Source-reported. NEW. literature_map P16-T8.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-131 | 2501.12749
- arXiv/DOI: arXiv:2501.12749
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: NACP: Noise-Aware Conformal Prediction
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P17-T4
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P17-T4] noise-free threshold from noisy calib labels; finite-sample coverage under uniform noise
- Takeaway for TRINETRA: FEATURES F-13 Wave-1; src-reported post-hoc. Calibrated fusion with noisy labels. Source-reported. NEW. P17_scout_notes T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-132 | 2402.07307
- arXiv/DOI: arXiv:2402.07307
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Self-Calibrating Conformal Prediction
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P17-T4
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P17-T4] Venn-Abers + conformal; calibrated points + valid intervals, better efficiency
- Takeaway for TRINETRA: FEATURES F-13 Wave-1; src-reported low post-hoc. Calibrated-fusion output layer. Source-reported. NEW. P17_scout_notes T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-133 | 2404.15018
- arXiv/DOI: arXiv:2404.15018
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Weighted Conformal Predictive Systems under Covariate Shift
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P17-T4
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P17-T4] likelihood-ratio reweighting keeps calibration valid under covariate shift
- Takeaway for TRINETRA: FEATURES F-13 Wave-1; src-reported. Directly targets coverage-breaks-under-shift; cross-site calibration. Source-reported. NEW. P17_scout_notes T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-134 | 2510.25573
- arXiv/DOI: arXiv:2510.25573
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: CUSUM Monitoring of Forecast Calibration
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P17-T5
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P17-T5] cumulative-sum chart w/ dynamic limits on prob vs outcome, model-agnostic
- Takeaway for TRINETRA: FEATURES F-14 Wave-1; src-reported very low cost. Drift/calibration monitor on fused outputs. Source-reported. NEW. P17_scout_notes T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-135 | 2610.09208
- arXiv/DOI: arXiv:2610.09208
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Sketched Calibration for Conformal Prediction under Covariate Shift
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P18-C
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P18-C] weighted CP with compressed covariate sketch Z=T(X); coverage >= 1-a-leakage
- Takeaway for TRINETRA: F-13 spec; src-reported 1-D sketch cut infinite sets 37.8%->8.0% at 92.3% coverage. RISK leakage if sketch discards label-relevant shift dir. Source-reported. NEW. P18 lit map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-136 | 2501.11413
- arXiv/DOI: arXiv:2501.11413
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Generalization and Informativeness of Weighted Conformal Risk Control under Covariate Shift
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P18-C
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P18-C] train-time bound on W-CRC set inefficiency vs shift magnitude + data sizes
- Takeaway for TRINETRA: F-13 spec; src-reported validated on localization. RISK bounds efficiency not validity; assumes pure covariate shift. Source-reported. NEW. P18 lit map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-137 | 2603.26415
- arXiv/DOI: arXiv:2603.26415
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: KMM-CP: Practical Conformal Prediction under Covariate Shift via Selective Kernel Mean Matching
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P18-C
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P18-C] KMM replaces density-ratio estimation + selective overlap restriction; coverage gap >50% reduced
- Takeaway for TRINETRA: F-13 spec; src-reported molecular benchmarks. RISK selective step abstains on low-overlap = the novel fire conditions we need. Source-reported. NEW. P18 lit map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-138 | 2604.22787
- arXiv/DOI: arXiv:2604.22787
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Conformal PM2.5 Mapping under Spatial Covariate Shift
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P18-C
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P18-C] CASE STUDY: split CP 90% nominal -> 65.3% actual PICP under moderate shift; KS shift monitor + reliability flags
- Takeaway for TRINETRA: F-13 spec coverage-collapse demonstration; src-reported. KEY: do NOT trust nominal 1-a without weighting. Source-reported. NEW. P18 lit map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-139 | 2406.17813
- arXiv/DOI: arXiv:2406.17813
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DriftLens: Unsupervised Concept Drift Detection from Deep Learning Representations
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P18-D
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P18-D] label-free drift via representation-distribution distances; best 15/17 use-cases, >=5x faster
- Takeaway for TRINETRA: F-14 spec; src-reported drift curves correlate >=0.85. RISK representation drift != calibration/performance drift. Source-reported. NEW. P18 lit map D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-140 | 1806.10131
- arXiv/DOI: arXiv:1806.10131
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Request-and-Reverify: Hierarchical Hypothesis Testing for Drift Detection with Expensive Labels
- Year / Venue: 2018 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P18-D
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P18-D] two-tier HHT, mostly unlabeled triggers + minimal label requests; beats supervised DDM with fewer labels
- Takeaway for TRINETRA: F-14 spec label-budget pattern; src-reported. RISK HHT-CU leans on miscalibrated confidence under shift. Source-reported. NEW. P18 lit map D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-141 | 2207.05796
- arXiv/DOI: arXiv:2207.05796
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Estimating Test Performance for AI Medical Devices under Distribution Shift with Conformal Prediction
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P18-D
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P18-D] black-box label-free target-accuracy estimation via conformal, no retrain
- Takeaway for TRINETRA: F-14 spec + P20 reporting; src-reported mammography/derm/histo shifts. RISK degrades under severe shift; point estimate not bounded guarantee. Source-reported. NEW. P18 lit map D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-ROB-142 | 2304.08319
- arXiv/DOI: arXiv:2304.08319
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Towards Computational Performance Engineering for Unsupervised Concept Drift Detection
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS6 | phase: P18-D
- Uses (workstream/chapter): WS6+WS8 (ch 13), ch 12, ch 14
- Core method: [P18-D] BENCHMARK: catalogs drift-detector compute complexity; quality-only eval insufficient
- Takeaway for TRINETRA: F-14 spec edge-budget pre-screen; src-reported. KEY: accuracy-chosen detector may blow real-time/edge budget. Source-reported. NEW. P18 lit map D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass
