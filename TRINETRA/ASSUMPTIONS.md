# ASSUMPTIONS (MASTER_PROMPT §0.1 rule 7 / §0.5)
# Working defaults adopted to keep research moving. Each: assumption, basis, risk if wrong,
# how/when it will be verified. Assumptions are NOT facts and never enter reports as facts.

| ID | Assumption | Basis | Risk if wrong | Verify in |
|----|------------|-------|---------------|-----------|
| A-01 | default-workspace\ is canonical writable root; trinetra\ is read-only | sandbox + inventory | output in wrong place | P0 gate (OQ-01) |
| A-02 | 235 ABS papers are a verified discovery backlog, not quota-satisfying | §0.9 quota honesty | over-/under-count quota | P2/P3 (OQ-02) |
| A-03 | Line-count proxy acceptable for file identity (no shell) | ENVIRONMENT_CHECK | undetected file change | P0 gate (OQ-03) |
| A-04 | Fresh re-open pass substitutes for 2nd-agent audit | single-agent runtime | weaker audit independence | ongoing (OQ-04) |
| A-05 | BOM ₹ figures are [EST]; ≤₹2000 gate not yet enforced | supplier 403 | infeasible BOM slips through | P6 (OQ-05) |
| A-06 | LoRa band = IN865–867 MHz for India | system-model note #6 | illegal/non-functional radio | P6 |
| A-07 | Only FREE datasets may be STATUS=selected | §0.9A free-only rule | paid dependency in build | P5 |
| A-08 | Kaggle is the only build compute (~25–30 GPU-h/wk, ≥15% reserve) | master constraints | plan exceeds compute | P5 |
| A-09 | Prior 33 bug findings / fixes / patches are BACKGROUND, re-examined not inherited | §0.5 honesty | stale conclusion promoted | P4/P5 onward |
| A-10 | Sandbox date is 2026 (arXiv IDs up to 26xx appear valid) | ENVIRONMENT_CHECK | mis-dated citations | ongoing |
