# ws1b_geohazard/literature_map.md — P7G geo-hazard reading map

Phase P7G · WS1b · RESEARCH-ONLY. Quota = **17 NEW primary arXiv papers** (≥15 required; aim ~30) + **18
FT-REF reference-verifications** of the established relations. HONEST DEPTH (§0.5): the 17 primary papers are
**ABS** (abstracts via a throttled arXiv API run, all HTTP 200); the 18 reference reads are **FT-REF**
(full encyclopedic article text that carries the governing equations verbatim and cites the primary
literature) — they VERIFY the equation FORMS for the inventory but are tertiary, not primary research. NO
primary-paper full texts (0 FT). All numbers SOURCE-REPORTED (Rule 16). Paper identities are subagent-
reported, not each independently re-fetched by me.

## Part 1 — 17 NEW primary arXiv papers (ABS)
### Landslide early warning / initiation
| # | arXiv | Short | Note (source-reported) |
|---|-------|-------|------------------------|
| L1 | 2605.17419 | Displacement-robust LEWS (RMCL contrastive) | up to 37% higher precision vs SOTA on Japan data; robust to spatial error in cheap rainfall forecasts → sparse-sensor Himalaya. |
| L2 | 2601.03569 | st-LID unsupervised slope-failure from ground motion | better precision + lead-time than baselines; unsupervised → label-scarce sites. |
| L3 | 1103.1678 | low-cost single-MEMS buried inclinometer | NO accuracy metric reported (weakness); canonical cheap-hardware reference for tilt sensing. |
| L9 | 2106.15119 | hybrid stochastic-mechanical I–D thresholds (Monte Carlo) | Campania; K_s dominant for intense storms; shows fixed single ID thresholds unreliable (direct GH-05/GB-03 evidence). |
| L10 | 1306.1529 | TRIGRS physically-based (Upper Tiber) | reproduces landslide size-frequency power laws + I–D thresholds; needs dense per-cell parameterization (weakness for data-sparse Himalaya). |
| L11 | 1209.5256 | 2D molecular-dynamics deep landslide w/ pore-pressure | qualitative match only; arbitrary potential params (weakness). |
| L12 | 1208.6116 | MD shallow-landslide toy model | Gutenberg-Richter/Omori power laws; validates Fukuzono INVERSE-VELOCITY failure-time prediction (cheap EWS tool). |
| L17 | 2606.04143 | Physics-Informed LSTM (Trend-Alignment loss) flood | NSE 0.20→0.23 on 5% data, stable under extremes where plain LSTM fails; documents LSTM unphysical-extrapolation weakness; ungauged fit. |

### GLOF / glacial-lake monitoring
| # | arXiv | Short | Note (source-reported) |
|---|-------|-------|------------------------|
| L4 | 2601.12330 | IceWatch multimodal GLOF (S2 CNN + ITS_LIVE + MODIS LST) | robust to cloud/missing data; fixes optical-only cloud weakness. |
| L5 | 2512.24117 | Sentinel-1 SAR U-Net (EfficientNet-B3) 4 Himalayan lakes | IoU 0.9130; Dockerised REST pipeline; SAR beats Himalayan cloud cover. |
| L6 | 2512.09251 | GLACIA LLM+segmentation glacial lakes | mIoU 87.30 vs CNN/ViT; interpretable but LLM-cost vs low-cost tension. |
| L7 | 2510.10546 | GLOFNet multimodal dataset (Shisper/Karakoram) | ~0.8 K/decade warming; fixes fragmented-data weakness (DATASETS candidate). |

### Flood / precipitation nowcasting + routing (ungauged, low-cost)
| # | arXiv | Short | Note (source-reported) |
|---|-------|-------|------------------------|
| L8 | 2412.02723 | DYffCast diffusion precipitation nowcast (IMERG 4h) | highest CSI, LPIPS<0.2; satellite-only nowcast where no radar. |
| L13 | 2609.32971 | feature-space-routing distributed hydrological model | SOTA on EFAS, strong in UNGAUGED settings, 10-day discharge; topology helps ungauged Himalayan basins. |
| L14 | 2607.23237 | Context-Aware Concept Distillation (interpretable flood LSTM) | median NSE 0.70 on 5,203 basins; addresses black-box trust weakness. |
| L15 | 2607.21200 | Transformer diffusion hydrological imputation+forecast | outperforms baselines under MISSING data; handles gappy gauge records. |
| L16 | 2607.16080 | radar-only multi-variable U-Net nowcast (Mumbai monsoon) | 90-min lead; CSI 0.437/0.332/0.193 at ≥10/20/30 dBZ; runs on a standard computer in seconds → strong low-cost flash-flood fit. |

## Part 2 — 18 FT-REF reference-verifications (equation forms for the inventory)
Verified verbatim (✓): Mohr-Coulomb/infinite-slope FS, Bishop simplified, Fellenius/ordinary slices,
Richards (mixed form), Green–Ampt, Horton, Kostiakov, van Genuchten retention, SCS Curve-Number
(Q=(P−Ia)²/(P−Ia+S), S=1000/CN−10, Ia=0.2S), Manning (V=(k/n)R_h^(2/3)S^(1/2)), Saint-Venant + kinematic/
diffusive wave, Muskingum continuity, Iverson 1997 two-phase debris-flow (pore-pressure liquefaction),
Takahashi/rheology families, GLOF/moraine-dam + dam-breach mechanisms (Himalayan case studies: Tsho Rolpa,
Dig Tsho 1985, Kedarnath 2013, Rishiganga 2021), avalanche runout zones. These confirm GH-01..GH-13 FORMS.
Coefficient-level values still UNVERIFIED [coeff-verify]: Caine 1980 I=14.82·D^(−0.39); Scheidegger 1973
log10(H/L)=0.62419−0.15666·log10 V; Costa–Schuster GLOF Q_p=0.763·PE^(0.42); Voellmy μ,ξ; Takahashi
dispersive-stress — flagged for primary-source confirmation.

## Consolidated implications → model set (confirms model_set_decision.md)
- Fixed single ID thresholds are unreliable (L9) → GB-03 probabilistic antecedent-aware threshold justified.
- Physically-based grid models (TRIGRS, L10) need dense parameterization unavailable in the Himalaya →
  lightweight GB-01/GB-03 node forms + offline simulators justified.
- Unphysical LSTM extrapolation under extremes (L17) → physics-informed / consistency-checked ML justified
  (matches program-wide stance; parallels PINN-failure evidence from P7).
- SAR/multimodal (L4,L5,L7) beats optical cloud cover → GLOF monitoring must be multimodal; cheap-node role
  is lake-level/temperature/seepage telemetry feeding these.
- Radar/satellite nowcasting on commodity compute (L8,L16) → flash-flood lead-time feasible at low cost.
- Cheap MEMS inclinometer (L3) + unsupervised ground-motion (L2) + inverse-velocity (L12) → concrete cheap-
  sensor EWS tools to pair with GB-01/GB-02.

## Tally & honesty
P7G NEW quota = **17 primary arXiv (ABS)** + 18 FT-REF reference reads. Depth: 0 FT primary (abstracts
only); reference reads verify equation forms. Tooling: an initial reading run hit web_search-no-key +
arXiv-429, so primary papers were retrieved in a SECOND throttled arXiv run (all HTTP 200). Coefficient-
level primary sources for ID/Scheidegger/GLOF/Voellmy remain [coeff-verify]. Running body-level deep FT NEW
reads UNCHANGED at 100 (P7G added breadth, not FT depth).
