# PROGRAM/logs/P7_reading_progress.md — P7 quota reading tally & themes

Phase P7 · WS1a · RESEARCH-ONLY.

## Tally
- **P7 NEW quota reads = 22** arXiv papers (≥15 required; aim ~30 → 22 solid + 4 noted/skim = 26).
- Depth: **5 FT** (2404.11439 Börger, 2208.03542 Sitte&Doan, 2212.00970 Dabrowski, 2109.01050 Krishnapriyan,
  2203.07404 Wang-causality) + **1 FT-PARTIAL** (2001.04536 Wang-gradients) + **16 ABS** (arXiv API feeds).
- Running body-level NEW FT/FT-PARTIAL reads: P1 15 + P2 18 + P3 43 + P4 15 + P5 2 + P6 1 + P7 6 = **100**.

## Themes covered
1. Fire-physics forward models (visibility/Jin's law; puffing-flame PINN soft-sensor; swirl breaking the
   flicker law) — 3 papers.
2. Wildfire spread: level-set, cellular automata, data assimilation, coupled atmosphere-fire — 10 papers.
3. PINN / physics-informed-ML failure modes + mitigations — 9 papers.

## Honest limitations
- `web_search` had NO API key the entire phase → arXiv-API-only reading. The CLASSIC fire-science
  correlations (Heskestad, McCaffrey, Zukoski, Alpert, Rothermel, Mulholland $K_m$, flicker, RTI, point-
  source radiation, IR radiometry) returned ~0 on arXiv and were used as ABS-CANONICAL inventory sources,
  NOT counted as quota papers. [coeff-verify] + expert-review flags stand (see inventory).
- The strongest FT depth is on the PINN-failure and fire-physics-PINN side (modern arXiv), which is exactly
  the evidence base for scoping out a live on-device fire-PINN and entering physics as features/priors.

## Uncovered / backlog (carried to gate)
- Fetch open-access PDFs of the classic correlations directly from NIST / SFPE / open-journal URLs (the
  reading subagent flagged this is possible with direct URLs; generic search was down).
- Verify + license-confirm NIST FDS validation suite and Fire Calorimetry Database (DATASETS [D] → [V]).
- Thermal-camera radiometry and smoke optical-extinction primary measurement papers (depth was ABS/
  canonical).
