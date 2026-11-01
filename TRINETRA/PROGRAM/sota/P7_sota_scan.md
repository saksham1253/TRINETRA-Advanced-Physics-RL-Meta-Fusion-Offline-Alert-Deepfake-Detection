# P7 SOTA SCAN — physics-informed / physics-guided fire modeling + fire-growth & smoke-transport validation

Phase P7 · WS1a · RESEARCH-ONLY. SOTA scan FIRST (§P7 task 1), before the model set. Records (a) the state
of the art in physics-informed/guided fire & smoke modeling, and (b) the canonical fire-growth/smoke-
transport correlations and their published validation cases/numbers that our Layer-1 inventory must meet.
Numbers are SOURCE-REPORTED, never ours (§0.5 / Rule 16). The ≥15 NEW quota reads (aim ~30) are logged
separately in ws1_physics/literature_map.md once the dedicated reading pass completes.

HONEST SOURCING NOTE (§0.5): the canonical fire-science relations below (Heskestad, Alpert, McCaffrey,
Cetegen, Mulholland, Rothermel) are stated from ESTABLISHED fire-science references (SFPE Handbook of Fire
Protection Engineering; the primary papers). I did not re-fetch each primary PDF this turn; the exact
coefficients/equation numbers are flagged [coeff-verify] in the inventory and are cross-checked against the
quota reading + must be expert-reviewed before any external use (per §P7 3(e)). This is disclosed, not hidden.

---

## A. Physics-informed / physics-guided ML for fire & smoke (how physics enters a learning system)
- The field splits into: (1) **hard constraints** (project outputs onto a physical manifold), (2) **soft
  PINN residual losses** (penalize PDE/ODE residuals of plume/transport/heat equations), (3) **feature
  generators** (compute a physical quantity — flame height, flicker band, extinction — and feed it to a
  detector), (4) **physics simulators for synthetic data** (FDS/zone models generate labeled smoke/flame),
  (5) **priors / consistency checks** (reject detections inconsistent with plume growth or flicker band).
- Recurring SOTA message (to be quantified by the quota reads): physics-GUIDED features + consistency
  checks are the robust, low-risk way to inject physics into cheap-sensor/low-res-CCTV detection; full
  PINNs of fire are brittle (stiffness, loss-weight imbalance, spectral bias, causality violation, poor
  extrapolation, non-identifiability) and are a research risk, not a deployment path on an ESP32.
- Implication: our Layer-2 extensions should enter the system as FEATURES / PRIORS / CONSISTENCY CHECKS
  with their own uncertainty and a fallback to the Layer-1 parent (per §P7 admission rule), NOT as hard
  dependencies — matching both the alerting design (P3/P13) and the IoT node design (P6 design.md §3).

## B. Fire-growth & HRR (validation anchors for EF-02)
- `t²` fire growth and the NFPA 72 growth classes (slow/medium/fast/ultrafast) are the standard design-fire
  parameterization; validation cases = furniture-calorimeter / room-corner HRR curves (NIST data).
- Convective fraction χ_c ≈ 0.6–0.7 and radiant fraction χ_r ≈ 0.2–0.4 are the standard partitions feeding
  plume (EF-03) and radiation (EF-06) models.

## C. Plume / flame geometry (EF-01, EF-03, EF-04)
- Heskestad flame-height + plume correlations and McCaffrey's three-regime centerline correlations are the
  two canonical, extensively-validated plume models; both are fitted to lab buoyant-diffusion-flame data
  and carry known regime limits (near-field vs far-field, pool vs line fires, wind).

## D. Ceiling jet & detector response (EF-05, EF-10)
- Alpert's ceiling-jet correlations (max gas temperature & velocity vs Q̇, H, r) underpin detector/sprinkler
  activation; combined with the Response-Time-Index (RTI) thermal-lag model they predict heat-detector and
  rate-of-rise response — directly relevant to the P6 node's rate-of-rise logic.

## E. Smoke optics & camera radiometry (EF-07, EF-09)
- Beer–Lambert extinction with a mass-specific extinction coefficient (Mulholland: ~8.7 m²/g for flaming
  smoke) governs what a camera sees through smoke; thermal-camera temperature retrieval needs emissivity +
  atmospheric transmission corrections. These are the physics behind "smoke vs steam" and IR false alarms.

## F. Flicker / puffing (EF-08)
- The puffing-frequency scaling f ≈ 1.5·D^(−1/2) Hz (Cetegen & Ahmed; Pagni) gives a narrow, source-size-
  dependent frequency band — a cheap, physics-grounded video/IR feature to discriminate flame from moving
  nuisances, BUT it aliases at low CCTV frame rates (a documented weakness → Layer-2 target).

## G. Spread dynamics (EF-11)
- Rothermel's surface-fire spread-rate model (wildland) + elliptical/Huygens/level-set and cellular-automata
  propagation are the standard spread formulations; relevant to the geo/wildfire side and as a simulator.

## SOTA-scan takeaways → model set
1. Admit the canonical Layer-1 correlations (plume, flame height, ceiling jet, radiation, extinction,
   flicker, radiometry, detector RTI, fire growth, spread) as Class-A parents + baselines.
2. Every Layer-1 model has documented weaknesses in OUR non-ideal setting (low-cost sensor lag/noise, low-
   res/low-fps CCTV, unknown Q̇/geometry, outdoor wind) → these motivate modest Layer-2 extensions.
3. Physics enters as features/priors/consistency checks with fallback-to-parent, never hard constraints on
   the device (PINN failure modes make full fire-PINNs a research risk).
4. Validation anchors are published lab/benchmark data (NIST HRR, Alpert/McCaffrey/Heskestad datasets, FDS
   validation suites) — named per model in validation_plan.md; where no data exists we say so honestly.
