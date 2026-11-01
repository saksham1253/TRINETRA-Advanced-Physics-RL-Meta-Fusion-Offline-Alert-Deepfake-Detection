# ws2_deepfake/physics_plausibility.md — physics-based plausibility checks (NOVEL, UNVALIDATED) (P11, WS2)

Phase P11 · RESEARCH-ONLY. MASTER_PROMPT P11 task 3. Rule 21: this is a NOVEL HYPOTHESIS, UNVALIDATED — it
is NOT claimed to work; a study design that would test it later is specified. No own-system performance claim
(Rule 16). The literature search for prior validation is recorded in ws2_deepfake/literature_map.md; if the
quota finds no validation, that is stated plainly.

## 1. Hypothesis
AI-generated / manipulated fire & disaster imagery may VIOLATE physical constraints that real fire obeys, so
consistency checks against the admitted P7 fire-physics envelopes could serve as a weak authenticity signal
complementary to pixel-forensics. Candidate checks (each tied to a P7 model):
- GROWTH RATE: fire area/intensity growth vs t² HRR envelope (EF — t² growth) and plume-rise rate.
- FLICKER FREQUENCY: luminous flicker should fall in a diameter-dependent band (EF flicker f≈1.5/√D) —
  synthetic video may show absent/implausible flicker.
- PLUME RISE: visual plume geometry vs Heskestad/McCaffrey plume relations.
- SMOKE OPACITY vs DISTANCE: apparent attenuation vs Beer–Lambert extinction given estimated path length.
- RADIANT consistency: brightness/glow vs point-source radiation falloff.

## 2. Status: UNVALIDATED for FIRE specifically (honest) — but prior work now exists for the general idea
- PRIOR WORK (P11 quota): PIVOT (arXiv 2609.15562) implements physics-grounded verification of AI-generated
  AUDIO-VIDEO — estimates physical quantities, selects applicable physical laws, verifies constraints, and
  returns evidence (law + time window + quantities). Source-reported (not ours): 70.3%/64.3% (Real+Seedance),
  72.2%/65.8% (Real+VEO), beating a strong MLLM's direct inspection (~54-57%). This VALIDATES the general
  approach (physics checks are generator-agnostic and give auditable evidence) — but absolute accuracy is
  MODEST, and PIVOT is NOT fire-specific. So our FIRE-physics checks remain UNVALIDATED for fire; PIVOT is
  cited as a design precedent and a benchmark-style template, not proof our fire checks work.
- Whether real-vs-synthetic FIRE separates on the §1 features is still UNKNOWN to us and not established for
  fire in the literature (no fire/wildfire-specific synthetic corpus exists — DATASETS.md GAP). It is
  plausible but could fail because: (a) real uncontrolled fire is highly variable (wide physical envelopes →
  weak discriminative power); (b) modern diffusion video may reproduce plausible flicker/growth; (c)
  extracting these quantities from a short degraded social clip is itself error-prone (unknown scale, camera,
  compression). → treated as EXPERIMENTAL only.

## 3. Role in the pipeline
At most a WEAK, FLAGGED-EXPERIMENTAL signal into the system_design.md fusion (stage 5), never a standalone
verdict, never asserted as working. Default = OFF until the study below shows value.

## 4. Study design to test it later (build phase)
- DATA: real fire videos (public fire datasets + fire-service footage where licensed) vs synthetic/AI-
  generated fire (produced by a THIRD party / existing synthetic sets — we create NO deceptive media
  ourselves, §content-safety) vs out-of-context real fire (right physics, wrong place/time — the physics
  check will NOT catch these, by design, documenting its scope).
- FEATURES: extract the §1 quantities with explicit uncertainty (scale/camera unknown → bounds).
- TEST: does any physics feature separate real vs synthetic ABOVE pixel-forensics alone? Pre-registered as a
  possibly-NULL result (evaluation_protocol experiment 4 = ablation of the physics signal).
- METRICS: incremental AUC/TPR@lowFPR over forensics-only; robustness under compression; failure on
  out-of-context (expected).
- OUTCOME HANDLING: adopt ONLY if it adds non-redundant, degradation-robust value; otherwise document as a
  tested-and-rejected hypothesis (honest negative result is a valid outcome).

## 5. Honesty
No claim that this works. It is a hypothesis with a test plan. If the literature quota shows prior work for/
against, it will be cited; absence of prior validation is recorded as such.
