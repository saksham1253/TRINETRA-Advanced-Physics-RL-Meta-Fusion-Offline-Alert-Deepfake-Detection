# ws1b_geohazard/formula_class_table.md — geo-hazard model lineage & class table (P7G)

Phase P7G · WS1b. Class A = established/derivable; B = empirical/semi-empirical fit with regime limits;
C = heuristic/assumed or documentation-only coupling. Every Layer-2 extension shows a reduction-to-parent
(see derivations/LAYER2_derivations.md), independently re-derived and confirmed correct (0 errors).

## Layer 1 (established, Class A / A-B)
| ID | Model | Class | Primary source | Validity regime | Key weakness (ours) |
|----|-------|-------|----------------|-----------------|---------------------|
| GH-01 | Infinite-slope FS | A | geotech (Skempton/Taylor) | planar failure, z≪slope | c',φ',z,m unknown |
| GH-02 | Iverson transient head | A/B | Iverson 2000 WRR | wet, event timescale | D₀,K_s unknown; linearized |
| GH-03 | Richards eqn | A | Richards 1931; vanGenuchten 1980 | variably-saturated | stiff; params scarce; macropores |
| GH-04 | Green–Ampt | A/B | Green&Ampt 1911 | ponded, sharp front | piston-flow idealization |
| GH-05 | Rainfall ID threshold | B | Caine 1980 + regional | shallow rainfall slides | ignores antecedent; FA/miss |
| GH-06 | Scheidegger reach angle | B | Scheidegger 1973; Corominas 1996 | runout mobility screen | empirical scatter; V unknown |
| GH-07 | Voellmy–Salm rheology | A/B | Voellmy 1955; Salm 1993 | dense debris runout | μ,ξ calibration-only |
| GH-08 | SCS Curve-Number | B | USDA-SCS/NRCS | event runoff, small catchments | 0.2 Ia disputed; AMC swings |
| GH-09 | Manning | A/B | Manning 1891 | steady uniform channel | n uncertain, stage-dep |
| GH-10 | Saint-Venant | A | Saint-Venant 1871 | 1-D unsteady flow | needs geometry+solver |
| GH-11 | Muskingum | B | McCarthy 1938 | lumped reach routing | K,X need calibration |
| GH-12 | Stage–discharge rating | B | hydrometry | gauged section | hysteresis; shifting bed |
| GH-13 | GLOF breach peak-Q | B | Froehlich 1995; GLOF review | dam/moraine breach screen | huge scatter; V_w,h_b uncertain |

## Layer 2 (robustified extensions, Class B — full derivations, reduce-to-parent, independently rechecked ✓)
| ID | Model | Class | Parent(s) | Weakness targeted | Reduces to parent when |
|----|-------|-------|-----------|-------------------|------------------------|
| GB-01 | Probabilistic infinite-slope P(FS<1) | B | GH-01 | point-FS false precision | all input variances → 0 |
| GB-02 | Sensor-corrected pore-pressure | B | GH-02 | piezometer lag/noise/drift | T_lag→0, noise→0, params known |
| GB-03 | Antecedent-aware prob. rainfall threshold (CORE EWS) | B | GH-05 | ignores antecedent; one line | hard step, no antecedent term |
| GB-04 | AMC-corrected SCS-CN | B | GH-08 | crude AMC classes; fixed λ | λ=0.2, r(S)=1 (AMC-II) |
| GB-05 | Hysteresis-corrected rating (Jones) | B | GH-12 | ignores unsteady loop | dh/dt→0 (steady) |

## Layer 2 (documentation-only, Class C — offline simulators, no live node validation)
| ID | Model | Class | Parent(s) | Note |
|----|-------|-------|-----------|------|
| GC-01 | Debris-flow runout simulator | C | GH-06 + GH-07 | needs DEM + solver; offline hazard-zone map |
| GC-02 | Flood routing simulator | C | GH-10 + GH-11 | 1-D hydraulic routing; gateway/server |
| GC-03 | GLOF breach→routing chain | C | GH-13 + GC-02 | advisory probabilistic hydrograph; data-scarce |
