# ws6_robustness/robustness_evaluation_plan.md — robustness evaluation methodology (P16, WS6)

Phase P16 · RESEARCH-ONLY, pre-registered. Nothing run (Rule 16). How robustness is MEASURED honestly in the
build. All numbers SOURCE-REPORTED.

## 1. Pre-registered principles
- STANDARDIZED attack×defense matrices with multiple settings — unstandardized evaluation yields misleading/
  false conclusions (BackdoorBench 2206.12654/2407.19845).
- Report CLEAN and ROBUST accuracy TOGETHER; state the tradeoff explicitly (2206.13405, 1910.14655).
- Against adaptive attackers report WORST-CASE, not average, evasion (2607.25842's 90% vs 57.6% split;
  2003.01279 adaptive-evades-blur).
- Evaluate on HELD-OUT / perceptually-dissimilar corruptions (a single ImageNet-C-style number is misleading,
  2102.11273) and on the VIDEO pipeline specifically (image benchmarks don't certify video, 2110.06513).
- Prove the eval data covers the deployment ODD (ODD representativeness via KL-divergence / Cramér's V,
  2608.20864 — ties P19).
- CERTIFIED robustness is a LOWER BOUND for restricted specs/small scale only (2206.03669, 1910.14655) — not
  full coverage; prefer continuous red-teaming.
- Honest VALIDATION: spatial-block / leave-one-incident-out, NOT random CV (random CV overstated urban-fire
  AUC 0.92→0.75, 2608.22293; confident-while-wrong under shift, 2610.08810 — ties P19).

## 2. Metrics
Clean accuracy; robust accuracy under each attack; MSCR-style interpretable corruption robustness (2206.13405);
worst-case evasion rate; calibration under shift (ECE as a DIAGNOSTIC, proper scores primary — ties P14);
uncertainty-flag recall (does entropy flag the shift? 2610.08810); alert false-negative rate at the chosen
operating point; wireless outage under jamming.

## 3. Red-team suite (continuous, pre-registered)
Physical/sparse patches on the camera channel (2411.16162); corruption sweep (weather/lighting/compression);
sensor-spoof injection (one modality attacked); jamming on the alert link; backdoor probe on any imported
model; detector-evasion probe (adaptive attack vs the forensic/anomaly thresholds).

## 4. Rule 19
Confirm every robustness failure degrades to "uncertain/offline" + human review, never a false "all clear";
confirm endpoints authenticated; confirm auto-adaptation stays advisory.

## 5. Honesty
Plan only; nothing executed. Pre-registered to prevent cherry-picked robustness numbers; honest negative
robustness results are reportable outcomes.
