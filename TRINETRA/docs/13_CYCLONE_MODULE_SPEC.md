# 13 — CYCLONE MODULE SPEC (specification only; NOTHING implemented)
**Case study storm: ASK TEAM (name, dates, region).** Use only official sources: IMD RSMC New Delhi bulletins
(rsmcnewdelhi.imd.gov.in, verified reachable) and IBTrACS NI (P24). Storm data is never invented.

## 1. Sub-problems TRINETRA could support
Early warning from public forecasts + INSAT-3D imagery. Ground evidence: CCTV and IoT (wind, rain, flood, debris,
power loss). Misinformation: old or fake cyclone videos (reuse deepfake + reverse-image provenance). Evacuation/resource
RL (later). Tiered offline alerts via the existing `ws3_alert` CAP builder (category `Met`).

## 2. Reading list structure (target ≥ 30 papers; NOT read yet)
Dynamics and intensification (4); wind-profile models such as Rankine/Holland (4); potential intensity (3); storm surge (3);
rainfall-flood (3); satellite intensity estimation (Dvorak and ML on INSAT/IR) (4); track/intensity forecasting physics and ML (4);
damage/flood imagery (3); wind from video/sensors (2); evacuation + warning response (3); North Indian Ocean climatology (2).
Sources: arXiv, Semantic Scholar, OpenAlex, IMD, ISRO/MOSDAC, NOAA, NASA.

## 3. Physics to specify (search leads; classes are assigned after source check)
| Relation | Expected class | Observation-operator idea (class B/C, to derive) |
|----------|---------------|---------------------------------------------|
| Holland (1980) parametric pressure/wind profile | A (verify eq.) | predicted wind at a camera/IoT site, then expected sensor reading |
| Gradient-wind / cyclostrophic balance | A | consistency check of reported wind vs pressure drop |
| Pressure-wind (Vmax vs ΔP) relations | A | IoT barometer drop to an intensity prior |
| Potential intensity (Emanuel) | A | ceiling check on claimed intensity (misinfo) |
| Storm surge basics (inverse barometer + wind setup) | A | coastal flood prior |
| Rain attenuation / visibility in heavy rain | A/B | camera reliability `r_i` down-weight |

## 4. Integration (no code yet)
New `Hazard.CYCLONE`; zero-shot prompts ("flooded street", "uprooted tree"); physics experts enter fusion as
`ExpertOutput` with a validity flag; anomaly on pressure/wind streams (`ws8_anomaly`); RL extension later; a UI mode.

## 5. Data (verified in 09b): P24 IBTrACS NI (27.9 MB), P25 INSAT-3D IR (47.5 MB), P26 Harvey damage, P27 FloodNet,
P20 NASA POWER, P21 India rainfall. GPM IMERG / ERA5 need registration.

## 6. Ready-to-paste research prompt
> You are the TRINETRA cyclone research agent. Read HANDOFF/NEXT_ACCOUNT_PICKUP.md first. Goal: for cyclone <NAME, DATES>,
> (1) find ≥30 papers in the structure of docs/13 §2 with verified links and note read depth honestly; (2) build a formula
> library with Class A (cite paper + equation number), B (show derivation), C (hypothesis); (3) derive observation operators that
> predict what TRINETRA cameras/IoT would see; (4) stage only small, free, verified datasets (rules of docs/09b); (5) write an
> integration spec against the existing ExpertOutput/fuse/decide interfaces. Never invent storm data, links or numbers.
> Write "novelty not verified" unless a search log exists. Files under 1,500 words, ending with <!-- END -->.

## 7. Feasible in the hackathon
A docs + demo scenario only: replay IBTrACS NI track points for the chosen storm on a map, with official IMD bulletin text,
labelled "historical replay, not a forecast". Everything else is post-hackathon.
<!-- END -->
