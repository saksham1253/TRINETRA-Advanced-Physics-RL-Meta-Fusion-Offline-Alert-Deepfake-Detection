# DEPLOYMENT/adoption_barriers.md — adoption barriers & local fit (P19)

RESEARCH NOTES. Source-reported where cited; design implications feed the handoff / open decisions.

| Barrier | Evidence / reality | Design implication (→ workstream) |
|---------|--------------------|-----------------------------------|
| Language & accessibility | multilingual + code-switched default (2103.07792); Indian-language misinformation (2207.12406); Bengali SMS/WhatsApp push works (2605.20167) | alerts in local languages + multi-modal/low-literacy formats; accessibility co-design → P12 alert UX |
| Trust & alert fatigue | residents' top concerns = privacy + cost (2610.03724); false alarms erode trust | aggressive false-alarm reduction (F-12); transparent uncertainty; community value elicitation → P12/P17 |
| Warning uptake in polarized communities | AOT + source-warning effects, simulation only (2605.17353) | message testing + correction strategy; do NOT over-transfer from sim → P11/P12 |
| Connectivity failure | collapse during disasters; DTN mitigation (2511.15710) | offline-first, store-carry-forward, redundant paths → P12/P13 |
| Power reliability | grid cuts, heat, dust stress sensors (2502.07596) | battery/solar + brownout handling; field calibration discipline → P13 |
| Maintenance & spare parts | low-cost sensors drift; recalibration cost (2506.09186, 2310.18118) | drift correction + scheduled recalibration (F-15); cheap replaceable modules → P13 |
| Vandalism / theft | physical risk to field nodes | tamper-evidence, enclosure, low-value visible parts → P13 |
| Interop with existing CCTV & fire panels | mixed ownership, legacy panels | standard interfaces; shadow integration; never bypass certified panels → P8/P12 |
| Model skill under local shift | 0.92→0.75 spatial-block (2608.22293); confident-while-wrong (2610.08810) | uncertainty-gated alerts; spatial-block validation; shadow mode → P16 |
| Cost of acting | cost main barrier (2610.03724, 65.5%) | affordability (INR 2000 prototype) + clear cost-of-ownership → cost_scaling.md |

HONEST: barriers are real and partly outside our control; several mitigations are source-reported research, not
proven in India. All feed open decisions, not promises.
