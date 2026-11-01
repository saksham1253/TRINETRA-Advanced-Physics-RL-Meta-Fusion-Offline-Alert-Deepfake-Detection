# ws1_physics/formula_class_table_P21.md — Rule-20 class table for P21 items

Phase P21 · RESEARCH-ONLY. Class per Rule 20: A = established/verified-source; B = derived from Class-A blocks
with a validation route; C = novel hypothesis, unvalidated. Lineage shown. SOURCE-REPORTED; nothing validated.

## Established (Class A) added in P21
| ID | Class | Lineage/source | Deployment role |
|----|-------|----------------|-----------------|
| EF-13 Byram/critical-Froude | A | 2501.08343, 2406.08589 [coeff-verify] | regime gate (feeds ND-6) |
| EF-14 RTE | A | 2009.13291 [coeff-verify] | smoke radiation (feeds ND-2) |
| EF-15 WSGGM | A | 2102.11060 [coeff-verify] | soot radiative loss (ND-2/ND-6) |
| EF-16 Strouhal puffing | A | classical, 2202.06567 [coeff-verify] | flicker band (ND-1) |
| EF-17 ADR transport | A | 1910.09098, 2207.05748 [coeff-verify] | transport lag (ND-4/ND-7) |
| EF-18 firebrand transport | A | 2206.01529, 2411.13275 | documented only |
| EF-19 G-equation | A | 2609.09773 [coeff-verify] | offline flicker sim |
| EF-20 Rothermel+Huygens | A | 2412.18931 [coeff-verify] | offline wildfire sim (C-01) |

## Novel (Class C) derived in P21 — ALL UNVALIDATED hypotheses
| ID | Class | Parent (Class-A/B) | System role | Validation gate |
|----|-------|--------------------|-------------|-----------------|
| ND-1 dealiased flicker | C | EF-08/EF-16, B-05 | flame-vs-nuisance feature | cross-fps separability vs naive peak |
| ND-2 transmittance-comp temp | C | EF-07/EF-14/EF-15, EF-05, B-06 | temperature feature + residual | vs thermocouple under smoke; σ grows w/ depth |
| ND-3 dimensionless ignition index Π_ig | C | EF-03/EF-05, EF-13 scaling | transferable early-warning scalar | cross-SITE threshold transfer (spatial-block) |
| ND-4 physics-residual r_phys | C | EF-03/EF-04/EF-17, B-06 | fusion c_i / anomaly bridge | discounts nuisance, preserves true fires |
| ND-5 wind-tilt flame height | C | B-01, EF-09, EF-13 | wind-robust size/range | vs known-size flames vs wind |
| ND-6 radiative-convective scalar Ξ_rc | C | EF-14/EF-15 vs EF-03/EF-04, EF-13 | physics-informed modality gate (→FM-5) | regime-gated vs fixed correlation |
| ND-7 advection-coherence COH | C | EF-17 ADR | network corroboration prior | separates advected vs independent spikes |

ALL Class-C items: enter as SOFT features/priors with Class-A fallback; ADVISORY (Rule 19); fire-science
EXPERT REVIEW mandatory; novelty = limited-search claim (novelty_log_P21.md). No performance claimed (Rule 16).
