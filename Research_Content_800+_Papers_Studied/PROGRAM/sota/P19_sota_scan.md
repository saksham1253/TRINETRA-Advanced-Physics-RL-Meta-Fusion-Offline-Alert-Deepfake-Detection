# PROGRAM/sota/P19_sota_scan.md — India/deployment SOTA scan (P19)

RESEARCH NOTES. MASTER_PROMPT P19.1. Existing systems/programs relevant to fire & disaster early warning,
public alerting, and surveillance analytics. All DEPLOYED-SYSTEM / agency facts are [UNVERIFIED] search leads
for official-source verification; all research numbers are SOURCE-REPORTED. Rule 16/18. IDs + detail in
DEPLOYMENT/literature_map.md.

## 1. Existing systems / programs (search leads — verify against official sources)
- National common-alerting-protocol / cell-broadcast emergency-alert programs (SACHET/C-DOT-type, from P12).
  [UNVERIFIED — governance + who-may-originate]
- Forest-fire alert services run by forest-survey / remote-sensing agencies (satellite hotspot alerts).
  [UNVERIFIED — scope/performance]
- Municipal "safe-city" CCTV analytics programs. [UNVERIFIED]
- International: cell-broadcast public-warning systems widely deployed (shown spoofable, 2604.24404);
  community-based and transboundary flood EWS in South Asia (research, 2605.20167, 2511.15710).

## 2. Research SOTA relevant to deployment (source-reported)
- EARLY WARNING (India/SA): transboundary flood EWS from free SAR + modeled upstream, ~3-day lead
  (2605.20167); India-origin CO forecasting R²>0.95 next-hour (2501.06007); relief-tweet matching
  (1810.11498).
- FIRE (India): Uttarakhand transfer learning (2410.06743); WFDroneBench sensor/drone placement (2609.11829);
  Palisades urban-fire GeoAI with spatial-block honesty (2608.22293).
- LOW-COST IoT (developing regions): reused-phone seismometers (2209.02416); DTN flood comms (2511.15710);
  federated edge AQI (2605.16375); low-cost sensor field calibration (2502.07596).
- MULTILINGUAL CRISIS: code-switching slot-filling (2103.07792); UrduFake (2207.12406); misinformation
  resilience sim (2605.17353); GeoCoV19 (2005.11177).
- ASSURANCE/ETHICS/PRIVACY: unit-level participation+assurance (2610.04084); decision-readiness layer
  (2609.13552); ODD representativeness (2608.20864); understanding/safety-case (2608.19816); privacy-preserving
  action recognition (2608.04501); data-minimizing federated surveillance (2609.07403).
- COST-EFFECTIVENESS / STAGED ROLLOUT: cost-per-completed-task + shadow→verified-cascade staging (2608.08528).
- DEPLOYMENT HONESTY: confident-while-wrong under shift (2610.08810); community value elicitation (2610.03724).

## 3. TARGETS (process targets, Rule 16)
Offline-first, free-data, multilingual, uncertainty-gated, spatially-honest-validation, complementary-until-
certified; shadow→advisory pilot with pre-registered metrics + stopping rules; data minimization + assurance
records; NO origination of official alerts.

## 4. Honesty & gaps
All agency/program/standard facts [UNVERIFIED]; research numbers source-reported on non-India or simulation
settings; strongest cross-cutting lesson = models stay confident while wrong under local shift (2610.08810) and
random CV overstates skill (2608.22293) → complementary, human-in-the-loop, shadow-mode until independently
certified.
