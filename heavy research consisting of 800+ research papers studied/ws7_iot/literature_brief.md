# WS7 — IoT / LoRa / TinyML — literature brief (P4, 2026-10-07)
Owner phase: P6. Scope: ≤₹2,000 sensor node, LoRa backhaul, energy, TinyML on-device, sensor faults.

## Most relevant papers
- **2508.15058** Space-Air-Ground-Underground LoRaWAN + WET — spread-factor (SF) / airtime / energy /
  coverage trade-off; satellite backhaul option for valleys with no terrestrial gateway.
- **2311.01743** Energy-efficient subterranean LoRaWAN (RL SF allocation, direct-to-satellite) — co-SF
  interference in dense deployments; MAD3QN/MAA2C beats 4 benchmarks. → disaster-load collision risk.
- **2412.04563** Indian-LoRa deployment (field numbers for Indian conditions) — carry into P6 BOM.
- Sensor-fault/anomaly refs (WS8) apply to node self-check: silent faults fabricate/mask hazard (FM-04).

## Key claims → references
- SF choice critically determines coverage/lifetime/feasibility; wrong SF kills range or blows the duty cycle.
- During a disaster MANY nodes transmit at once → co-SF interference + collisions spike exactly when
  reliability matters (FM) → VoI-aware duty cycling (FM-10); DTN store-carry-forward on backhaul loss (FM-11).
- Solar node may be energy-starved during a storm (FM-10).

## Open questions
- Final ≤₹2,000 BOM (incl GST): MCU, LoRa radio, sensors (tilt/soil-moisture/rain), solar, enclosure — P6.
- River-Eye LSPIV camera within budget + night robustness — P6/P8 (G3).
- TinyML model footprint for on-device anomaly pre-filter — P6/P9.
- Safety protocol for field deployment (safe-stimulus-only; no live-hazard testing) — P6.
