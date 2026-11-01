# ws8_anomaly/spec/family_d_physics_residual.md — BUILD SPEC: physics-residual anomaly (P10, WS8b)

PRIORITY 2. RESEARCH-ONLY. External numbers SOURCE-REPORTED (Rule 16). Reuses the admitted fire (P7: EF-xx /
B-xx) and geo (P7G: GH-xx / GB-xx) models — NO new live PDE solver (consistent with P7/P7G rejection of
on-node solvers). Precise defaults [recipe-cite — P10 reader].

## 1. Method and why (evidence)
Idea: the admitted physics models predict expected sensor/scene behavior; the RESIDUAL (observed − physics-
expected) is an anomaly/consistency signal and an integrity check. Evidence: CPS process-invariant residuals
both detect attacks and gate against replay-poisoning (2609.34804, 9 invariants → 20/35 SWaT attacks,
recovers 69-100% of recall lost to poisoning); a TS foundation model can be a model-free residual generator
when no physics model fits (TimesFM 2606.06347); process knowledge injected as graph structure helps
(2607.15799). Residuals enter as FEATURES/consistency scores with FALLBACK-TO-PARENT, never hard constraints.

## 2. Inputs/outputs
INPUT: sensor streams + the physics models' predicted quantities (e.g. plume/temperature rise from fire EF
models; rainfall-threshold exceedance / P(FS<1) from geo GB models). OUTPUT: normalized residual score per
model + a consistency flag → fusion (P14) input and anti-spoof integrity signal → P12.

## 3. Data/splits
Co-located sensor + ground-truth event data (own build data); public CPS (SWaT/WADI D63) for method dev only.
Time/site-grouped splits. For geo residuals, the ungauged-catchment data gap (P7G) means advisory-only, wide
uncertainty.

## 4. Features/architecture/defaults
Residual r_t = x_t − f_physics(context); normalize by the model's stated validity-range uncertainty;
optional CUSUM on r_t for drift (classic k=0.5σ,h=4-5σ). Where no physics model applies, a TS-foundation
residual generator (TimesFM-style, 2606.06347) is the fallback. Process-knowledge graph (2607.15799) optional.

## 5. Thresholding/calibration
Residual threshold via EVT/conformal for a target false-alarm rate on validation; fallback-to-parent if the
extension's residual is unavailable or out of validity range.

## 6. Metrics
Residual AUROC as a fusion input; INCREMENTAL value over the parent model (must add non-redundant signal);
contribution to fused detection delay/false-alarm (P14). Strict protocol.

## 7. Baselines first
Raw parent-model threshold (no residual learning) and simple CUSUM-on-residual before any learned residual
model.

## 8. Ablations/stress
With/without residual in fusion; parent-only vs extension-residual; out-of-validity-range behavior
(fallback); spoof/replay injection (does the residual gate catch it, 2609.34804).

## 9. Acceptance (targets)
Adds non-redundant signal over its parent; improves fusion; catches staged replay/spoof as an integrity gate.

## 10. Pitfalls
Physics-model misspecification → residual false alarms (mitigate: validity-range gating + fallback); double-
counting with the parent in fusion (flag correlation to P14); geo residuals unvalidated in ungauged basins →
advisory-only (Rule 19).

## 11. GPU hours
≈0 (reuses P7/P7G); TS-foundation fallback is inference-only. ESTIMATE.

## 12. Verification checklist
[ ] residual reduces-to-parent when extension off  [ ] validity-range gating + fallback implemented
[ ] incremental value over parent shown  [ ] correlation-with-parent reported to P14  [ ] spoof-gate tested
[ ] geo residuals labelled advisory-only.
