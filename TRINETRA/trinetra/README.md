# TRINETRA / HIMKAVACH — codebase

Build of the TRINETRA multi-hazard, offline-first, **advisory** early-warning system, implemented
strictly per `../DESIGN/` (SYSTEM_DESIGN_PROMPT, HLD, LLD, COMPONENT_DESIGN, REPO_BLUEPRINT) and the
P0–P23 research. This is a research prototype — **not** a product that claims measured performance.

## Prime safety posture (enforced in code, not just docs)
- **R19 — advisory / human-in-the-loop / fail-safe.** No module issues a public alert autonomously.
  The decision layer recommends a *level* to an operator; the operator decides. Fails safe to
  `UNCERTAIN`, never to a silent all-clear.
- **R16 — no own performance claims** before the spatial-CV admission gate (`eval/`) passes.
- **R20 — physics classes.** Every physics/fusion block is labelled **A** (established) / **B** (derived)
  / **C** (novel hypothesis, UNVALIDATED). Class-C is flag-gated **off** by default with a Class-A/B
  fallback.
- **R21 — novelty = search claim.** "Novel" means "not found in our limited search," never "proven first."

## Environment (honest)
Bundled interpreter has **numpy, pandas, lxml** only. No scipy / scikit-learn / torch / xgboost /
d3rlpy / pytest / pyyaml are available here. Therefore:
- The **deterministic/numerical core** (physics gates, fusion math + PHARAOH, conformal, cost-loss,
  baselines, safety shield, decision function, LoRa codec, CAP builder) is implemented in **pure numpy +
  stdlib** and is **runnable + tested** now.
- **Deep-learning components** (EO foundation encoder, CCTV CNN detector, deep anomaly heads, offline-RL
  training) expose clean interfaces with **honest stubs / numpy fallbacks**; they raise a clear
  `MissingDependency` where a heavy library is genuinely required. No fake results.
- Configs are **JSON** (no pyyaml); tests use **stdlib `unittest`** via `run_tests.py`.

## Layout
```
src/trinetra/
  common/        types, config, security allow-list, tracing
  eval/          M0: spatial-CV, baselines, cost-loss Value Score, real-win gate, report guard
  ws1b_geophys/  M1: FS, Iverson, Fukuzono, Caine, gate
  ws1a_firephys/ M1: established EF blocks + novel ND (flag-gated), gate
  ws5_fusion_rl/ M6: NF, PHARAOH, FM-1 fallback, GMF, shield, decision (single)
  ws6_robust/    M4: conformal + drift monitor
  ws8_anomaly/   M2: anomaly ensemble (numpy) + interfaces
  ws1b_eo/       M3: frozen EO encoder interface (stub)
  ws4_cctv/      M3: detector + temporal validator interfaces (+ numpy validator)
  ws3_alert/     M8: CAP builder, DTN, siren, operator advisory
  ws2_deepfake/  M9: authenticity scorer (low-trust)
  pipeline/      M10: geo/fire/offline loops + hindcast harness
configs/         JSON; safe-by-default feature flags
tests/           golden + unit + contract tests (stdlib unittest)
run_tests.py     test runner
```

## Run
```
python run_tests.py           # all tests
python -m trinetra.pipeline.demo   # end-to-end advisory demo (synthetic)
```
