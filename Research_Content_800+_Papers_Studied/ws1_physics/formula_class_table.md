# ws1_physics/formula_class_table.md — lineage table (Class A / B / C)

Phase P7 · WS1a · RESEARCH-ONLY. One row per model. Class rules (Rule 20): **A** = established, verified-
source model (parent/baseline); **B** = robustified extension derived from Class-A blocks, with a full
derivation that reduces to its parent; **C** = more speculative extension (documentation-only unless a
realistic validation route exists). Every Class-B/C row names its parent(s), the weakness it targets, its
derivation document, the sources of its building blocks, and its validation status. Reduction-to-parent is
shown in each Layer-2 derivation document.

## Layer 1 — Class A (established; parents & baselines)
| ID | Model | Class | Parent(s) | Weakness it has (→ targeted by) | Derivation | Building-block sources | Validation status |
|----|-------|-------|-----------|---------------------------------|-----------|------------------------|-------------------|
| EF-01 | Heskestad flame height | A | — | needs Q̇,D; wind/line fires; pixels≠height (→B-01) | LAYER1_outlines §EF-01 | Heskestad 1983; SFPE Hbk | published lab data (validation_plan) |
| EF-02 | t² fire growth / HRR | A | — | coarse class; real fires deviate | LAYER1_outlines §EF-02 | NFPA 72; NIST HRR | NIST calorimeter curves |
| EF-03 | Heskestad plume centerline T,u | A | EF-02 (source) | far-field only; needs Q̇c; −5/3 decay noise (→B-02) | LAYER1_outlines §EF-03 | Heskestad; SFPE Hbk | McCaffrey/Heskestad plume data |
| EF-04 | McCaffrey 3-regime plume | A | EF-02 | regime seams; wind | LAYER1_outlines §EF-04 | McCaffrey 1979 NBS | McCaffrey gas-burner data |
| EF-05 | Alpert ceiling jet T,U | A | EF-02 | transient/beams; gas≠sensor temp (→B-06) | LAYER1_outlines §EF-05 | Alpert 1972; SFPE Hbk | Alpert ceiling-jet data |
| EF-06 | Point-source radiation | A | EF-02 | near-field/large flame; smoke absorbs | LAYER1_outlines §EF-06 | Modak; SFPE Hbk | flux-vs-distance data |
| EF-07 | Beer–Lambert smoke extinction | A | — | multiple scattering; Km varies (→B-01) | LAYER1_outlines §EF-07 | Mulholland; SFPE Hbk | mass-extinction measurements |
| EF-08 | Flicker/puffing f≈1.5/√D | A | — | wind broadens; **CCTV aliasing** (→B-05) | LAYER1_outlines §EF-08 | Cetegen&Ahmed 1993; Pagni | puffing-frequency data |
| EF-09 | Thermal-camera radiometry | A | — | unknown ε, humid τ_atm, solar reflections | LAYER1_outlines §EF-09 | IR radiometry; heat-transfer texts | blackbody-cal data |
| EF-10 | Detector RTI / rate-of-rise | A | EF-05 | cheap-sensor τ,noise,chem lag (→B-06) | LAYER1_outlines §EF-10 | Heskestad&Bill; SFPE Hbk | plunge-test RTI data |
| EF-11 | Rothermel spread rate | A | — | heterogeneous fuel; spotting/crowning | LAYER1_outlines §EF-11 | Rothermel 1972 | BehavePlus/field data |
| EF-12 | Zukoski entrainment | A | EF-03 | far-field/still-air only | LAYER1_outlines §EF-12 | Zukoski; SFPE Hbk | entrainment data |

## Layer 2 — Class B (robustified extensions; admitted)
| ID | Model | Class | Parent(s) | Weakness addressed | Derivation (reduces to parent) | Blocks | Validation status |
|----|-------|-------|-----------|--------------------|--------------------------------|--------|-------------------|
| B-06 | Sensor-response-corrected ceiling-jet/plume signal | B | EF-05, EF-10 (+EF-03) | cheap-sensor lag/noise; gas temp ≠ measured temp; transport delay | derivations/B-06… (→ parent as τ→0, delay→0) | EF-05, EF-10, 1st-order lag | PLAN: Alpert data + plunge-test τ; build-gate vs parent |
| B-05 | Aliasing-aware flicker-band feature | B | EF-08 | low-fps CCTV aliases the 1.5–5 Hz band | derivations/B-05… (→ parent as fps→∞) | EF-08, Nyquist sampling | PLAN: puffing data resampled; build-gate vs raw-FFT |
| B-01 | Camera-observed apparent flame height (through smoke) | B | EF-01, EF-07 (+EF-09) | pixels≠height; smoke obscuration; unknown Q̇,D | derivations/B-01… (→ EF-01 as extinction→0, calib known) | EF-01, EF-07, pinhole projection | PLAN: lab flame-height video; build-gate vs EF-01 |
| B-02 | Dimensionless/prior plume-temperature estimator | B | EF-03 | unknown Q̇c,z0; far-field noise | derivations/B-02… (→ EF-03 at prior point mass) | EF-03, Buckingham Pi, Bayesian prior | PLAN: Heskestad plume data; build-gate vs EF-03 |

## Layer 2 — Class C (documentation-only unless validation route appears)
| ID | Model | Class | Parent(s) | Why C (no realistic near-term validation) |
|----|-------|-------|-----------|-------------------------------------------|
| C-01 | Level-set / elliptical front propagation coupling to Rothermel | C | EF-11 | needs fuel/wind fields we won't have at pilot; simulator-only |
| C-02 | Coupled plume+extinction+radiometry full forward camera model | C | EF-03,EF-07,EF-09 | many unknowns; use as synthetic-data simulator, not a live estimator |

N (admitted): **Layer 1 = 12 (EF-01..12, all Class A)**; **Layer 2 = 4 Class B (B-01,B-02,B-05,B-06)**;
**2 Class C documentation-only (C-01,C-02)**. Rationale + admit/demote/reject in model_set_decision.md.
