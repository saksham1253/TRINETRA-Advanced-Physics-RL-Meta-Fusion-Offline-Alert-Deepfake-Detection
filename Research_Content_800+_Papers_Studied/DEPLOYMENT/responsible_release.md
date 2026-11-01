# DEPLOYMENT/responsible_release.md — misuse/dual-use & responsible release (P19)

RESEARCH NOTES. Rule 19 governs. Addresses misuse, open-source vs safeguarded release, licenses, data
governance, and the model cards / datasheets to produce at build time.

## 1. Misuse / dual-use analysis
| Risk | Vector | Mitigation |
|------|--------|------------|
| Spoofed alerts (panic/phishing) | cell-broadcast PWS spoofable (2604.24404) | never originate official alerts; signed + cross-cell-verified channels; auth endpoints (P16) |
| Surveillance abuse | repurposing CCTV analytics for tracking individuals | data minimization (keep raw video local, forward only flagged clips, 2609.07403); privacy-preserving recognition (2608.04501); purpose limitation; NO biometric/person-ID features |
| Deepfake tooling misuse | provenance/forensic components (P11) could be inverted | release forensic detectors as defensive-only; do NOT release generation tooling; red-team continuously (2003.01279) |
| Autonomous action | over-automation of alerts/evacuation | hard human-in-the-loop (Rule 19); advisory-only; fail-safe to uncertain/offline |

## 2. Open-source vs safeguarded
- OPEN: non-sensitive research artifacts — physics derivations (with Class A/B/C labels), evaluation
  protocols, benchmarks/datasets we create (leakage-controlled), build manuals (no exploit detail), tooling.
- SAFEGUARDED / NOT RELEASED: anything enabling spoofed alerts, person-tracking, or deepfake generation;
  operational alert-channel credentials; raw personal video.

## 3. Licenses & consequences
Pick permissive licenses for open research artifacts; verify every reused dataset/code license at build
(current licenses INDICATIVE); respect platform ToS for social-media data (tweet-ID-only redistribution where
required, ties P11). Document license choices + their downstream obligations.

## 4. Data governance
Lawful basis + consent for any collected data; minimization + retention limits; local processing; access
controls + audit logs; datasheets for every collected dataset.

## 5. Model cards & datasheets to produce at build (P20 reporting standards)
- MODEL CARDS (1810.03993): intended use, OUT-OF-SCOPE use, disaggregated performance, eval procedure;
  explicitly fill the usually-skipped Limitations/Evaluation sections (2402.05160).
- DATASHEETS (1803.09010; worked safety-critical example 2105.03020): provenance, composition, collection,
  label process, recommended/limited uses.
- MI-CLAIM-GEN-style minimum-information reporting for a safety-critical advisory system (2403.02558).

## 6. Honesty
This is a research-phase plan; nothing released. Dual-use review + legal/ethics approval required before any
release.
