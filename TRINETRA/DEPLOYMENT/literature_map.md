# DEPLOYMENT/literature_map.md — India deployment literature map (P19)

HONEST: all ABS; IDs/years arXiv-ID-derived + subagent-reported (reader 0c98bcbc; 11 fetches), NOT re-fetched
(residual risk, §0.5); all numbers SOURCE-REPORTED (Rule 16), mostly on non-India / simulation settings →
transfer hypotheses; all AGENCY/LAW/STANDARD references are [UNVERIFIED] search leads for official-source
verification (not legal advice). Backs the DEPLOYMENT/ docs + P19 SOTA scan. Running body-level deep FT NEW
total UNCHANGED at 100.

## P19 section — 25 NEW primary arXiv

### T1 India/South-Asia early warning & emergency management
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2605.20167 | HaorFloodAlert | RF/XGBoost on free SAR+rainfall+modeled upstream; LOOCV 90.9% acc/AUC 0.939, live run ~3-day lead, Bengali SMS/WhatsApp. Template for free-data multilingual advisory pilot. |
| 2501.06007 | CoNOAir | complex neural operator CO forecast (IIT-D/IISc, Indian cities); next-hour R²>0.95, beats FNO. India-origin advisory air-hazard forecasting; extreme-event capture hard. |

### T2 community-based early warning
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2607.16218 | Fuzzy community crime-hotspot | fuzzy fusion of citizen reports + privacy workflow; authors state NO real-world predictive/reduction evidence (n=25). Model of honest "complementary not certified" + multilingual UX. |
| 1810.11498 | Emergency-aid tweet ranking | embedding NN + weighted ranking; 6.81% MAP on Nepal-quake multilingual tweets. SA relief matching; low MAP ⇒ decision-support not autonomous. |

### T3 fire-incident / fire detection (India + comparable)
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2410.06743 | Uttarakhand forest-fire TL | MobileNetV2 transfer learning cuts India labeled-data needs; TL > from-scratch (qualitative). Regional domain shift = key caveat. |
| 2609.11829 | WFDroneBench | open benchmark: ML risk maps + sensor/drone placement, 7746 scenarios; risk-map error dominates. Shadow-mode before trusting placement. |
| 2608.22293 | Palisades urban-fire GeoAI | XGBoost+LR, 12,081 inspections; ROC-AUC 0.92 random CV but 0.75 spatial-block; recommends spatial-block as MINIMUM. Random CV overstates skill. |

### T4 warning trust / human factors / integrity
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2604.24404 | PWS spoofing testbed | first open 5G PWS spoofing (OAI+SDR); devices readily display spoofed alerts; cross-cell verification flags single-source. Assume adversarial spoofing of cell broadcast. |
| 2610.03724 | Community values → AI constraints | survey n=30 + town hall; 66.7% likely to use, privacy top concern 64.3%, cost barrier 65.5%. Pre-model community value elicitation for India pilots. |

### T5 low-cost IoT / sensing in developing regions
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2209.02416 | Crowd-funded EEW | reused Android phones as seismometers/alarms, targets budget-constrained incl. India; conceptual (no field metrics). Low-cost e-waste sensing; reliability unproven. |
| 2511.15710 | AZIZA DTN | trust-aware opportunistic DTN over phones/UAVs on real Bangladesh flood traces (sim); better delivery/energy/resilience. Connectivity-collapse mitigation. |
| 2605.16375 | M²FedAQI | multimodal federated AQI on heterogeneous edge + TLS auth; +11% acc / −25.4% MAE. Privacy-preserving bandwidth-light edge learning; TRAQID regional set. |
| 2502.07596 | Enviro-IoT | 4-yr design + 9-mo field low-cost PM/NO2 vs reference; 98/97/97% (single case). Field-calibration discipline; single-site limit. |

### T6 multilingual crisis informatics & misinformation
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2207.12406 | UrduFake@FIRE2020 | Urdu fake-news shared task, 900/400 articles, 42 teams; best F 0.90 (BERT). SA-language misinformation benchmark; year domain-shift degrades. |
| 2605.17353 | LLM community misinformation resilience | agent sim; higher AOT improves resistance, source warnings weaker. Simulation only — caution transferring to Indian contexts. |
| 2103.07792 | Code-switching slot-filling | random-translation code-switch aug for mBERT; +4.2% intent/+1.8% slot over 8 langs; new disaster-tweet set. Low-resource code-switched languages; supports human triage. |
| 2005.11177 | GeoCoV19 | 524M+ multilingual geolocated COVID tweets, gazetteer geo-inference. Large multilingual crisis set; ToS/licensing + inferred-geo noise to verify. |

### T7 ethics / assurance of safety-critical AI
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2610.04084 | Dependable AI-assisted engineering | per-unit participation+assurance records w/ fallback + human-adjudication; 17-unit wing-spar case, no workflow-level dependability claim. Operationalizes "human stays decisive". |
| 2609.13552 | Decision-assurance layer (ATAL) | semantic-stability + consistency + normative checks → Decision Readiness Level; flags unsafe outputs pre-use. Shadow→advisory gating pattern. |
| 2608.20864 | Coverage-driven verification | ODD representativeness via KL-divergence/Cramér's V, aligned to EASA objectives (verify officially). Prove eval data covers the India ODD. |
| 2608.19816 | Understanding as assessable | 4 objects of understanding + adequacy justification (Assurance 2.0). Structures the safety case for decision-makers. |

### T8 privacy-preserving public-safety surveillance
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2608.04501 | Privacy-preserving action recognition review | PRISMA 32 papers; only 10% formal privacy defs, <15% cross-dataset, <10% adaptive-attacker. Maps privacy-utility options + evidence gaps for video sensing. |
| 2609.07403 | Federated binary gating + server VLM | local CNN gate forwards only flagged clips to server VLM; ~centralized F1 at 51.4% video transmitted, FNR 29.3%→22.9%. Data-minimizing architecture (keep raw video local). |

### T9 cost-effectiveness / staged rollout
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2608.08528 | T2MO cost-optimal routing | cost-per-COMPLETED-task + staged static→shadow→verified-cascade→router. Cost-effectiveness + staged-rollout methodology template. |

### T10 pilot & field-evaluation / deployment honesty
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2610.08810 | Prithvi FM under shift | OOD 37 events/12 countries; acc 0.65→0.40, confidence stayed HIGH while wrong, 12-51% confidently mislabeled; MC-dropout entropy flagged all shifts. STRONGEST lesson: uncertainty monitoring + stopping rules + OOD checks. |
| 2604.02351 | Deployment reliability control | reliability as dynamic state (discrimination+calibration) w/ volatility; selective drift-triggered intervention beats continuous retraining (1.35M loans). Report reliability as a time-trajectory. |

### Synthesis — see the DEPLOYMENT/ docs
(1) India constraints: transboundary hydrology, connectivity collapse, multilingual-by-default, spoofable
alerts, fragile skill under local shift. (2) Pilot methodology: shadow→advisory staging, spatial-block/LOIO
validation as minimum, uncertainty-based stopping rules. (3) Ethics/assurance: unit-level participation
records, decision-readiness levels, ODD representativeness, data-minimizing privacy. (4) Datasets with flaws →
DATASETS.md.

## Tally (P19)
P19 NEW quota = 25 primary arXiv (≥15 MET; aim-~30 not reached under throttle — documented). Depth all ABS
(0 FT) — running body-level deep FT NEW total UNCHANGED at 100.
