# ws3_alerting/simulation_spec.md — SPECIFICATION for the later alerting simulation (P12, WS3)

Phase P12 · RESEARCH-ONLY. MASTER_PROMPT P12 task 6. Specifies WHAT to simulate later and HOW to parameterize/
validate it. NOTHING is simulated now (Rule 16). Every parameter traces to a SOURCE-REPORTED value in
ws3_alerting/literature_map.md or is marked TO-MEASURE.

## 1. Simulator choice (justified by literature)
- PRIMARY: ns-3 with the LoRaWAN module — a validated, canonical setup exists (PDR/throughput vs device
  count/traffic, duty-cycle sub-bands) [2009.09503], and a mesh-overlay extension is characterized [2512.00161].
- FAST SWEEP: FAST-LoRa analytical model for coarse design-space exploration with QUANTIFIED error (PDR MAE
  0.940×10⁻², EE MAE 0.040 bits/mJ) [2507.23342]; use it to prune, then confirm promising points in ns-3.
- BLE: model a BlueFlood-style advertising flood using its reported operating point [2002.12906] + BLE-mesh
  QoS limits [1910.03345].

## 2. What to simulate (scenarios)
- REACH vs DISTANCE vs NODE DENSITY (per tier/technology): coverage of a neighbourhood/valley.
- LATENCY DISTRIBUTION end-to-end (alert → device/siren), per tier and hop count.
- NODE FAILURE / partition: fraction reachable as nodes drop (fire destroys nodes).
- INTERFERENCE: WLAN/co-channel interference on BLE (3/40 channels) [1910.03345]; jamming on radio tiers.
- SPOOF / replay attempts: does signature + cross-cell/behavioral verification reject them (threat_model)?
- STAGGERED vs simultaneous rollout: congestion/response (info-design result −70%/−89%) [2606.30320].
- DTN backstop: delivery ratio + delay when infrastructure is down [2601.00148].

## 3. Sourced parameters (traceable)
- LoRa path-loss/fading: forest log-distance + body-shadow + Nakagami-m, ~600 m [2303.12754]; Meshtastic SF
  link-budget thresholds (SF7-8→~120 dB … SF12→180 dB, demod −18 dB SNR) [2605.17063]; RSSI/SNR @2.47 km
  anchor point [2605.20379].
- LoRaWAN load/PDR/duty-cycle: ns-3 reference curves [2009.09503]; mesh gains 5×/8×/12.6×/2.3× [2512.00161];
  routing-vs-flooding +185%/−75% [2510.03714].
- BLE: flood 99.9% delivery, 0.4% duty, 38 B, 200 ms, 2 Mbps [2002.12906]; mesh 250 ms/10 hops, 3/40 channels,
  density collapse [1910.03345].
- Multi-radio under jamming: PDR >95%, 17-23 ms (SIM) [2603.02105].
- DTN: 68% delivery, 4311 s delay, 1.68 hops [2601.00148].
- TO-MEASURE (not in literature, GAPS): Zigbee + ESP-NOW range/PDR; 802.11s stock-phone background reception;
  real device-radio ranges on the P6 BOM hardware — measured in P13/build.

## 4. Validation approach
Reproduce the source papers' reported curves in our ns-3 setup BEFORE trusting new scenarios (match
[2009.09503]); cross-check FAST-LoRa vs ns-3 within its stated error bars [2507.23342]; sensitivity analysis
on path-loss exponent + fading; flag SIMULATION-only numbers (e.g. 2603.02105, LIMA) as directional until a
field/prototype check in P13. Report CIs over seeds.

## 5. Honesty
Nothing simulated or built. Parameters are source-reported (several from simulation themselves) or TO-MEASURE;
the sim is a design tool whose outputs will be validated against the cited papers and later hardware, not
treated as ground truth.
