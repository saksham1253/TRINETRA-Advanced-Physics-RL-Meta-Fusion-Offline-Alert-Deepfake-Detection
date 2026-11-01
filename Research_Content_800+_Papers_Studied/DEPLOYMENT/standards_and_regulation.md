# DEPLOYMENT/standards_and_regulation.md — standards & regulation research notes (P19)

RESEARCH NOTES ONLY — NOT LEGAL ADVICE. Rule 11: every standard, code, law, and agency named below is an
UNVERIFIED SEARCH LEAD to be verified against OFFICIAL sources and reviewed by a qualified legal/standards
professional BEFORE any reliance. arXiv-only retrieval cannot confirm regulatory facts → all items [UNVERIFIED].
Rule 19: present the system as COMPLEMENTARY until independently certified; never originate official public
alerts without authority.

## 1. Regulatory areas that apply (search leads — verify each)
| Area | What to verify (official sources) | Status |
|------|-----------------------------------|--------|
| Fire detection/alarm devices as SAFETY products | National building & fire-safety codes; product certification/standards body marking; whether a fire-detection product must be certified to be treated as a safety device | [UNVERIFIED] |
| Radio operation (LoRa/Wi-Fi/BLE/mesh) | National radio/telecom regulator's license-exempt bands, power limits, duty cycle; whether the chosen LoRa band is legal for the region (ties P13/P12 open item) | [UNVERIFIED — confirm band legality] |
| Public-alert broadcast (cell broadcast / CAP) | Who may originate official alerts; access rules for any national alerting program; a private/academic party likely MAY NOT originate official alerts | [UNVERIFIED — ties P12] |
| Data-protection / personal data in video | National data-protection law obligations for processing personal data in CCTV; lawful basis, retention, minimization, data-subject rights | [UNVERIFIED] |
| Surveillance / CCTV rules | Municipal "safe-city"/CCTV rules; consent/signage; public vs private premises differences | [UNVERIFIED] |
| Social-media data | Platform terms of service + data-protection law for ingesting posts; redistribution limits (e.g., tweet-ID-only) | [UNVERIFIED — ties P11] |
| Electronics certification | Mandatory product safety/EMC certification for electronic hardware sold/deployed | [UNVERIFIED] |

## 2. Governance evidence (source-reported research, not regulation)
- Cell-broadcast public-warning systems are SPOOFABLE; cross-cell verification flags single-source alerts
  (2604.24404). ⇒ any alerting integration must assume adversarial spoofing + authenticate (ties P16).
- ODD-representativeness proof methods (KL-divergence, Cramér's V) exist to show eval data covers the
  deployment domain, aligned to formal learning-assurance objectives (2608.20864) — VERIFY the referenced
  standard (e.g., EASA) against official sources; use as an assurance ARTIFACT, not a legal claim.
- Unit-level AI participation+assurance records with explicit human-adjudication/fallback (2610.04084) and a
  decision-assurance/readiness-level layer (2609.13552) operationalize "complementary until certified".

## 3. Posture (binding design rule)
Until independently certified: SHADOW then ADVISORY only; a human authority owns every alert decision; the
product markets itself as a decision-support aid, NOT a certified safety device; endpoints authenticated;
data minimized. All of §1 pending official verification + professional legal/standards review.
