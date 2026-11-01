# DEPLOYMENT/india_context.md — India disaster-management & fire-service context (P19)

RESEARCH NOTES ONLY. Rule 11: every agency name, law, standard, and statistic below is an UNVERIFIED SEARCH
LEAD, to be verified against OFFICIAL sources (government gazettes, agency websites, official statistics) and
reviewed by a qualified professional BEFORE any reliance. web_search had no API key this program; arXiv-only
retrieval cannot confirm government facts → NONE of the institutional/legal/statistical items here is verified.
Not legal advice. Rule 19: this system is COMPLEMENTARY/advisory, human-in-the-loop, until certified.

## 1. Disaster-management landscape (SEARCH LEADS — verify each)
- National/state/district tiers of disaster-management authority, a national disaster response force, and a
  national institute for disaster-management training are commonly referenced; the EXACT names, statutory
  basis, and current mandates MUST be verified against official sources. [UNVERIFIED]
- Public alerting: a national common-alerting-protocol / cell-broadcast initiative for emergency alerts is
  referenced in the literature (e.g. SACHET/C-DOT-type programs, carried from P12). Who may ORIGINATE official
  public alerts, and through which channel, is a governance question to verify — a private/academic party
  almost certainly may NOT originate official public alerts. [UNVERIFIED — ties P12 regulatory path]
- Fire services are typically STATE/municipal subjects with their own rules; a national fire-service college
  and national building/fire codes are referenced. Verify names, jurisdiction, and current editions.
  [UNVERIFIED]
- Meteorological / remote-sensing agencies (national met department; ISRO/NRSC for satellite data; forest-
  survey bodies for forest-fire alerts) provide hazard data and some already run forest-fire alert services —
  verify scope, access terms, and performance claims against official portals. [UNVERIFIED]

## 2. Operating environment (constraints — some literature-supported, source-reported)
- CONNECTIVITY: intermittent/absent during disasters is a BINDING constraint; opportunistic DTN over phones/
  UAVs/vehicles is a researched mitigation for flood-hit South Asia (AZIZA, 2511.15710, src-reported sim). ⇒
  offline-first design (ties P12/P13) is correct for India.
- TRANSBOUNDARY/SPARSE SENSING: free Sentinel-1 SAR + modeled upstream signals can give multi-day flood lead
  where gauges are sparse (HaorFloodAlert, 2605.20167, src-reported ~3-day lead). ⇒ free-data advisory
  pipelines are viable.
- POWER: grid cuts, heat and dust stress low-cost sensing; multi-month in-the-wild calibration discipline is
  needed (Enviro-IoT, 2502.07596, src-reported single-site). Reused-phone sensing targets budget-constrained
  quake-prone nations incl. India (2209.02416, conceptual).
- LANGUAGE/LITERACY: multilingual + code-switched by default (2103.07792); Indian-language misinformation is
  real (UrduFake, 2207.12406); crisis messaging must be multilingual (HaorFloodAlert pushes Bengali SMS/
  WhatsApp). ⇒ alerts in local languages + low-literacy-friendly formats (ties P12 alert UX, P11 corroboration).
- CCTV OWNERSHIP: a mix of municipal "safe-city" programs and private premises; ownership, consent and data-
  protection rules differ by owner → see standards_and_regulation.md. [UNVERIFIED landscape]
- MODEL SKILL IS FRAGILE UNDER LOCAL SHIFT: urban-fire GeoAI dropped 0.92→0.75 under spatial-block CV
  (2608.22293); foundation models stayed confident while wrong under geographic shift (2610.08810). ⇒ India
  deployment REQUIRES uncertainty monitoring + spatial-block validation + shadow mode (ties P16).

## 3. Fire-incident patterns & statistics
Official national-crime/accident statistics bureaus and fire-service annual reports are the correct sources for
fire-incident counts, causes, and seasonality; forest-fire seasons and electrical/LPG causes are commonly
cited. ALL such numbers are [UNVERIFIED] here and must be taken WITH DATES from official publications. The
Uttarakhand forest-fire transfer-learning study (2410.06743) confirms India regional domain shift is the key
fire-detection caveat.

## 4. Design implications (feed to handoff / open decisions)
Offline-first + multilingual + uncertainty-gated + spatially-honest-validation + complementary-until-certified;
free-data pipelines; private-CCTV consent/data-protection path; NO origination of official public alerts
without authority. Every institutional fact pending official verification + professional review.
