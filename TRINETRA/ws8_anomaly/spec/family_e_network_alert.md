# ws8_anomaly/spec/family_e_network_alert.md — BUILD SPEC: network / alert anomaly (P10, WS8b)

PRIORITY 2 — LIGHTWEIGHT. RESEARCH-ONLY. External numbers SOURCE-REPORTED (Rule 16). Mostly reuses the P6
message-signing + replay-protection; adds light behavioral anomaly. Feeds the P12 threat model. Precise
defaults [recipe-cite — P10 reader].

## 1. Method and why
Job: detect spoofed / replayed / flooded mesh messages and node misbehavior on the ESP-NOW/BLE mesh.
Evidence: per-token cross-entropy SURPRISAL + per-protocol Z-score calibration is a strong, explainable
unsupervised IDS template (X-SPUR 2609.21217, TOW-IDS AUC 0.9987); physics-attested invariants gate against
replay-poisoning (2609.34804); benign operational variation inflates FPR → control-plane-aware thresholds
(2609.29745). For our tiny mesh the PRACTICAL core is cryptographic (signing + monotonic replay counters from
P6) + simple rate/behavior rules, NOT a heavy IDS.

## 2. Inputs/outputs
INPUT: mesh message metadata (sender, counter, timing, size, type), HMAC/signature verification result.
OUTPUT: reject/accept decision, node-health/misbehavior flag, spoof/replay alarm → P12 threat model + P13
dashboard.

## 3. Data/splits
Own mesh logs (normal + staged attack: replay, flood, spoof); public CAN/automotive IDS (D-level) for method
dev only. Benign-regime-shift test set (2609.29745).

## 4. Features/architecture/defaults
Layer 1 (crypto, from P6): signature/HMAC check + monotonic replay counter + timestamp window. Layer 2
(behavioral): per-node message-rate, inter-arrival timing, size/type distribution; surprisal of a tiny causal
model over message-field tokens (X-SPUR-style, 2609.21217); per-protocol/per-node top-k% Z-score
calibration. Defaults [recipe-cite — P10 reader].

## 5. Thresholding/calibration
Per-node/per-protocol Z-score thresholds set on benign traffic (incl. benign regime shifts to avoid FPR
inflation, 2609.29745); crypto layer is deterministic (reject on fail).

## 6. Metrics
Spoof/replay rejection rate, false-reject rate on benign traffic (incl. regime shifts), node-misbehavior
detection; detection delay. Strict protocol.

## 7. Baselines first
Pure crypto (signing + replay counter) + static rate limits before any learned surprisal model.

## 8. Ablations/stress
Crypto-only vs +behavioral; benign regime shifts (new node joins, topology change); replay/flood/spoof
injection; node-compromise scenario.

## 9. Acceptance (targets)
Rejects staged spoof/replay (crypto) + flags node misbehavior at low false-reject under benign regime shifts.

## 10. Pitfalls
Benign variation inflates FPR (2609.29745); key management / clock sync for replay windows (hand to P12/P6);
compromised-node-with-valid-key (behavioral layer + physics corroboration).

## 11. GPU hours
≈0 (rules + tiny model). ESTIMATE.

## 12. Verification checklist
[ ] crypto layer (P6) integrated  [ ] benign-regime-shift false-reject tested  [ ] replay/flood/spoof staged
[ ] per-node/protocol calibration  [ ] feeds P12 threat model  [ ] defaults cited.
