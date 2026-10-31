# RISK_REGISTER — program-level risks (MASTER_PROMPT §0.10)
# Each: ID, risk, category, likelihood, impact, exposure, mitigation, owner-phase, status.
# L/I scale: L=low M=med H=high. Program risks (not just build — see HANDOFF/RISKS_FOR_BUILD).

## Methodology / evidence risks
| ID | Risk | Cat | L | I | Mitigation | Phase | Status |
|----|------|-----|---|---|------------|-------|--------|
| R-01 | Spatial leakage inflates all skill metrics (0.9→0.54) | method | H | H | tile-withheld spatial-CV doctrine from P2; GB/tree/persistence baselines gate every claim | P2/P4 | open |
| R-02 | Whole corpus is abstract-only → methods uncertified | evidence | H | H | Tier-2+ full-text promotion in P2/P3; nothing stated as fact from ABS | P2/P3 | open |
| R-03 | Fabrication/transcription errors in citations | integrity | M | H | two-pass re-open audit; 10% per batch + 100% Tier-1 numbers; verify IDs on arXiv | all | mitigated (7 clean audits) |
| R-04 | Over-engineering: deep models lose to simple baselines | method | M | M | parsimony; baseline-first; 2608.12422 evidence | P4+ | open |

## Resource / infrastructure risks
| ID | Risk | Cat | L | I | Mitigation | Phase | Status |
|----|------|-----|---|---|------------|-------|--------|
| R-05 | Kaggle compute cap exceeded by plan | resource | M | H | per-WS GPU-h budget + ≥15% reserve; distill/subset fallbacks | P5+ | open |
| R-06 | ₹2000/node BOM infeasible or unverifiable | resource | M | H | hard-verify ≥2 live listings P6; cheaper substitutions w/ evidence | P6 | open (supplier 403) |
| R-07 | No shell → no hashing; weaker integrity control | infra | H | L | line-count proxy; re-verify counts from files each resume | all | accepted (D-003) |
| R-08 | Single-agent → weaker audit independence | infra | H | M | fresh re-open pass; log error rate | all | accepted (OQ-04) |
| R-09 | Datasets turn out paid / access-gated / region-locked | resource | M | H | free-only STATUS=selected; verify terms from portal; LEAD_TIME_ITEMS | P5 | open |

## Safety / deployment / ethics risks
| ID | Risk | Cat | L | I | Mitigation | Phase | Status |
|----|------|-----|---|---|------------|-------|--------|
| R-10 | Life-safety: false alarm erodes trust → future deaths (cry-wolf) | safety | M | H | trust-aware threshold (2104.11422); FA cost beyond -5 reward | P12/P15 | open |
| R-11 | Life-safety: missed alarm | safety | M | H | miss=-100 reward; safety shield hard overrides; human-in-loop | P15 | open |
| R-12 | System presented as replacing certified warnings | safety/legal | L | H | Rule 19 in every design doc: COMPLEMENT not replace; human oversight | all design | enforced |
| R-13 | Proxy forwards credentials to external host | security | M | H | remove/replace proxy; security review before any deployment | P16/P19 | open (Bug #12) |
| R-14 | Regulatory/privacy non-compliance (LoRa band, data) | legal | M | H | research notes flagged for expert review; IN865-867; NDMA/SDMA | P6/P19 | open |
| R-15 | Safety shield unrealizable (contradictory rules) | safety | M | M | realizability check (2507.23603) as acceptance gate | P15 | open |

## Scope / process risks
| ID | Risk | Cat | L | I | Mitigation | Phase | Status |
|----|------|-----|---|---|------------|-------|--------|
| R-16 | Starting unauthorized phase work | process | L | H | strict phase-gate; STOP after gate message; PHASE_STATE source of truth | all | enforced |
| R-17 | Overwriting pre-existing files | process | L | H | CoW policy D-002; new-name-only; backups + CHANGELOG | all | enforced |
| R-18 | Prior bug findings promoted as settled without re-exam | integrity | M | M | A-09: treat as BACKGROUND, re-examine in P4/P5 | P4+ | open |
