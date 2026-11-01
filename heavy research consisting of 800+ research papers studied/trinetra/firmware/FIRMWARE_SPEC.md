# TRINETRA node firmware spec — Slope Sentinel (SS) & River Eye (RE)  [M7, gate G5]

> Firmware is specified here; it is NOT built in this environment (no embedded toolchain). The Python
> `ws7_iot` package implements the host-side codec/validation/edge rules the firmware mirrors.

## Slope Sentinel (SS) — landslide/debris node
- MCU: ESP32-C3 (RISC-V, low power). Radio: SX1262 LoRa, **IN865–867** (constraint C4; regulatory confirm `[verify]`).
- Sensors: dual MEMS tilt/incline, capacitive soil-moisture ×2, piezo/geophone, tipping-bucket rain, temp.
- Power: Li-ion 18650 + small PV; deep-sleep duty cycle (`iot.duty_cycle_pct`); target multi-week autonomy.
- **BOM target ≤ ₹2000** (constraint C2; re-price via `scripts/bom_price_check` before G5 sign-off).

### Duty cycle & uplink
- Heartbeat every N minutes; event-driven burst on edge WATCH/LOCAL_SIREN.
- Uplink = `ws7_iot.encode_frame` (25 B, ≤51 B budget) → LoRa; app layer attaches HMAC/Ed25519 tag.
- Store-carry-forward (DTN) when gateway unreachable; `(node_id, seq)` monotonic for replay protection.

### Tier-0 edge screen (offline autonomy, bounded)
- `node_local_edge_flag`: BOTH fast tilt-rate AND heavy rain ⇒ `LOCAL_SIREN` drives the node's OWN siren.
- The node **never** issues a public/network alert on its own (Rule 19) — gateway + human do that.

## River Eye (RE) — flood/GLOF node
- MCU: ESP32-CAM; stage/level (ultrasonic or pressure), optional low-fps camera for LSPIV surface velocity.
- Same radio/power/security profile; LSPIV runs on gateway, not the node (no video egress, C7).

## Security (constraint C6)
- Per-node signing key provisioned at flashing (Ed25519 on device; HMAC placeholder in this host build).
- Downlink (config/threshold/time-sync/siren cmd) authenticated + duty-cycle limited.

## Acceptance (G5)
BOM ≤ ₹2000 supplier-verified; frame ≤ 51 B; fault vs event discrimination; single node cannot drive a
network RED (corroboration required — enforced in `ws5_fusion_rl.shield`).
