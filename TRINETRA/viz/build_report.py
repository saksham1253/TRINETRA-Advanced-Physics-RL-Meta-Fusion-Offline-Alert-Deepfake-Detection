# -*- coding: utf-8 -*-
"""Build the formal 10-year disaster-events report DOCX with sources + project novelty."""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.shared import OxmlElement, qn

OUT = r"C:\Users\Dell\Documents\deepseek-harness\default-workspace\viz\TRINETRA_Disaster_Report_2015-2025.docx"

doc = Document()
nf = doc.styles["Normal"].font; nf.name = "Calibri"; nf.size = Pt(11)

BLUE=RGBColor(0x1F,0x3A,0x6E); TEAL=RGBColor(0x1F,0x7A,0x6E); GREY=RGBColor(0x55,0x5B,0x66)
RED=RGBColor(0xB0,0x2A,0x2E); GREEN=RGBColor(0x1E,0x6B,0x3A)

def hyperlink(paragraph, url, text):
    part = paragraph.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    h = OxmlElement('w:hyperlink'); h.set(qn('r:id'), r_id)
    r = OxmlElement('w:r'); rPr = OxmlElement('w:rPr')
    c = OxmlElement('w:color'); c.set(qn('w:val'), '1155CC'); rPr.append(c)
    u = OxmlElement('w:u'); u.set(qn('w:val'), 'single'); rPr.append(u)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '19'); rPr.append(sz)
    r.append(rPr); t = OxmlElement('w:t'); t.text = text; r.append(t); h.append(r)
    paragraph._p.append(h); return h

def field(label, text, color=TEAL):
    p = doc.add_paragraph(); r = p.add_run(label + "  "); r.bold = True; r.font.color.rgb = color
    p.add_run(text); p.paragraph_format.space_after = Pt(3); return p

def deaths_field(text):
    p = doc.add_paragraph(); r = p.add_run("Lives lost:  "); r.bold = True; r.font.color.rgb = RED
    rr = p.add_run(text); rr.bold = True; p.paragraph_format.space_after = Pt(3); return p

def sources_block(src):
    p = doc.add_paragraph(); r = p.add_run("Sources:"); r.bold = True; r.font.color.rgb = GREY; r.font.size = Pt(9.5)
    for s in src:
        sp = doc.add_paragraph(style="List Bullet"); sp.paragraph_format.space_after = Pt(1)
        hyperlink(sp, s["url"], s["title"])

# ===================== COVER =====================
h = doc.add_heading(level=0); h.add_run("Himalayan & Indian Disasters, 2013–2025")
s = doc.add_heading("A Ten-Year Evidence Report — and Why TRINETRA / HIMKAVACH Matters", level=1)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
r = p.add_run("Floods · Flash floods · Landslides · Cloudbursts · Glacial Lake Outburst Floods (GLOFs) · Land subsidence")
r.italic = True; r.font.color.rgb = GREY
doc.add_paragraph()

# ===================== HOW TO READ =====================
doc.add_heading("About this report", level=1)
doc.add_paragraph(
 "This report documents the most significant water- and slope-related disasters in India and the "
 "Himalayan region over roughly the last decade (2013–2025). For each event it records, in plain and "
 "formal English: where and when it happened, what happened, how it happened (the physical cause), the "
 "human toll (lives lost, missing and displaced), the economic damage, and — most importantly for our "
 "work — the early-warning gap that allowed the loss of life. Every factual claim is backed by a clickable "
 "source link.")
cvp = doc.add_paragraph()
cvp.add_run("Coverage (year by year). ").bold = True
cvp.add_run("This is a full-decade sweep, not one or two years: it documents 15 major events spanning "
 "2013, 2014, 2015 (two), 2017, 2018, 2019, 2020, 2021, 2022, 2023 (three), 2024 and 2025. The focus is "
 "the disaster types TRINETRA / HIMKAVACH is built for — floods, flash floods, landslides, cloudbursts, "
 "glacial lake outburst floods (GLOFs) and land subsidence, chiefly in India and the Himalaya.")
dp = doc.add_paragraph()
dr = dp.add_run("Method & honesty note. "); dr.bold = True; dr.font.color.rgb = RED
dp.add_run("Facts were gathered by directly reading primary encyclopaedic entries and the reputable news "
 "reports, government statements and peer-reviewed studies they cite (Reuters, BBC, The Hindu, Hindustan "
 "Times, Indian Express, Al Jazeera, NDTV, Science, ESA, NASA, Nature, and official agencies such as "
 "ASDMA and NRSC/ISRO). Casualty and damage figures are reported AS STATED by those sources and, for "
 "ongoing or contested events, can vary between sources and over time; where a figure is uncertain it is "
 "marked \u201capproximately\u201d or given as a range. This document reports third-party facts; it does not "
 "claim them as our own measurements.")

# ===================== PART A: BIG PICTURE =====================
doc.add_heading("Part A — The big picture: why this risk is growing", level=1)
doc.add_paragraph(
 "A glacial lake outburst flood (GLOF) is a sudden flood caused when a natural dam holding back a glacial "
 "lake — made of ice or of loose rock and soil (a moraine) — fails. The dam can break due to erosion, "
 "water-pressure build-up, an avalanche of rock or ice falling into the lake, an earthquake, or a large "
 "piece of glacier collapsing into the water. As the planet warms, glaciers melt and retreat, new and "
 "larger glacial lakes form, and the risk of these outburst floods rises — a danger that is especially "
 "acute in the geologically active Himalayas.")
field("Scale of the risk (reported figures):", "", color=TEAL)
for b in [
 "A 2023 study found about 15 million people worldwide are exposed to GLOF hazard — most of them in China, India, Nepal, Pakistan and Peru.",
 "Peak flows in such events have reached as high as 15,000 cubic metres per second; a normally small mountain stream can briefly become a torrent ~50 m deep, and spread up to ~10 km wide on floodplains downstream.",
 "Pakistan alone has more than 7,000 glaciers and, as of 2018, more than 3,000 glacial lakes in Gilgit-Baltistan, with 30 flagged by the UNDP as an imminent GLOF threat.",
 "Bhutan has 2,674 glacial lakes, 24 of them judged likely GLOF candidates; Nepal has multiple lakes (e.g. Tsho Rolpa, holding ~90–100 million cubic metres) identified as dangerous.",
 "India's own 2013 Kedarnath catastrophe involved a GLOF from Chorabari Lake; recent Nepal GLOFs include the 2024 Thame flood and events during the 2025 Nepal floods.",
]:
    bp = doc.add_paragraph(style="List Bullet"); bp.add_run(b)
sources_block([
 {"title":"Glacial lake outburst flood — Wikipedia (definition, monitoring, 15-million figure, regional lake counts)","url":"https://en.wikipedia.org/wiki/Glacial_lake_outburst_flood"},
])
doc.add_paragraph(
 "The pages that follow show the same lesson again and again: the physics was knowable, the hazard was "
 "often known in advance, but there was no system that turned that knowledge into a timely, localized, "
 "trusted warning that actually reached the people in the valley.")

# ===================== PART B: EVENT DOSSIERS =====================
doc.add_heading("Part B — Event dossiers (2013–2025)", level=1)

events = [
 dict(id="E1", name="2013 North India (Kedarnath) floods",
   date="14–17 June 2013 (worst on 16 June).",
   location="Uttarakhand, India (Rudraprayag/Kedarnath; Mandakini & Alaknanda valleys); also Himachal, UP, Haryana, Delhi, western Nepal, Tibet.",
   type="Cloudburst-driven flash floods and landslides, plus overflow of the Chorabari glacial lake above Kedarnath (a GLOF element).",
   what="A multi-day cloudburst and extreme rain hit Uttarakhand, triggering massive flash floods and landslides — India's worst natural disaster since the 2004 tsunami. Villages and market towns (Gaurikund, Ram Bada, Sonprayag) were wiped out; Kedarnath town was buried in water, mud and boulders, though the main temple survived.",
   how="A Bay-of-Bengal low drew moisture from both seas and merged with a western disturbance, dumping rain far above normal. With melting snow, this filled and overflowed upstream Chorabari Lake; the sudden release surged down the Mandakini, while landslides and debris-choked rivers worsened the flood wave.",
   deaths="About 6,054 (as later assessed); the state declared over 5,700 \u201cpresumed dead\u201d by 16 July 2013. ~89% of deaths were in Uttarakhand.",
   affected="~300,000 pilgrims/tourists trapped; >110,000 evacuated by armed forces; ~4,550 villages affected. In Nepal ~128 houses and 13 offices swept away, 1,000+ left homeless.",
   loss="No single confirmed monetary total in the sources read; damage was catastrophic (450+ road sites, highways and bridges washed away).",
   gap="The IMD had forecast heavy rain, but warnings were not widely publicised in advance and there was no dedicated flood/glacial-lake monitoring and alert system for the Kedarnath valley, so pilgrims and residents were caught unaware.",
   src=[{"title":"2013 North India floods — Wikipedia","url":"https://en.wikipedia.org/wiki/2013_North_India_floods"},
        {"title":"Chorabari Lake — Wikipedia (the glacial lake that overflowed)","url":"https://en.wikipedia.org/wiki/Chorabari_Lake"},
        {"title":"Mandakini River — Wikipedia","url":"https://en.wikipedia.org/wiki/Mandakini_River"}]),
 dict(id="E1b", name="2014 Jammu & Kashmir (India–Pakistan) floods",
   date="2–26 September 2014 (worst 5–10 September).",
   location="Jammu & Kashmir, India (Srinagar, South Kashmir, Jammu division); also Pakistan's Azad Kashmir, Gilgit-Baltistan and Punjab.",
   type="End-of-monsoon river flooding plus landslides.",
   what="Torrential rain made the Jhelum and Chenab rivers overflow and submerge much of Srinagar and hundreds of villages; it was Prime Minister Modi's words a \u201cnational calamity\u201d. Entire neighbourhoods of Srinagar went ~12 ft under water, trapping tourists and residents in upper storeys.",
   how="Heavy end-of-monsoon rain from 2 September pushed the Jhelum at Srinagar to 4.4 ft above the danger mark, with a discharge of ~70,000 cusecs against a normal 25,000; the swollen rivers burst into streets while landslides battered the Jammu division.",
   deaths="557 total — 277 in India and 280 in Pakistan.",
   affected="In J&K ~2,600 villages affected (390 fully submerged); ~200,000 people rescued (87,000 from Srinagar city alone), 80,000+ evacuated; 50 bridges damaged; telecom and roads collapsed.",
   loss="Preliminary property damage put at \u20b95,000–6,000 crore; total loss to the Kashmir division alone estimated as high as \u20b91 trillion (~US$12–16 billion).",
   gap="Srinagar had no effective flood-forecasting or evacuation system despite rivers crossing danger marks; communications collapsed, so much of the rescue was done by local volunteers, and officials were criticised for the lack of warning and preparedness.",
   src=[{"title":"2014 India–Pakistan (Jammu & Kashmir) floods — Wikipedia","url":"https://en.wikipedia.org/wiki/2014_India%E2%80%93Pakistan_floods"},
        {"title":"Jammu & Kashmir floods: toll, rescue and damage — The Economic Times","url":"https://economictimes.indiatimes.com/news/politics-and-nation/jammu-and-kashmir-floods/articleshow/42163033.cms"}]),
 dict(id="E2", name="2015 Nepal earthquake landslides (incl. Langtang Valley)",
   date="25 April 2015 (Mw 7.8–7.9 Gorkha earthquake); Langtang avalanche within minutes.",
   location="Langtang Valley, Rasuwa District, Nepal; wider quake affected Nepal, India, China, Bangladesh.",
   type="Earthquake-triggered rock-and-ice avalanche (with an air blast) and thousands of landslides.",
   what="The earthquake shook loose snow, ice and rock from high peaks; a 2–3 km-wide avalanche destroyed Langtang village and hit the Langtang trekking route, burying nearby hamlets.",
   how="Violent shaking detached ice and rock that fell thousands of metres into a fast avalanche. The falling mass pushed an air-blast pressure wave that flattened buildings before the debris even arrived; debris then buried the village. The quake also fractured the ground, raising landslide risk for decades.",
   deaths="~329 reported missing in Langtang; later studies estimate ~350 died there. The earthquake overall killed 8,962 and injured 21,952; a separate Everest avalanche killed 22.",
   affected="Langtang village wiped out; nearby hamlets buried. Across Nepal ~3.5 million were left homeless; UNESCO heritage sites destroyed.",
   loss="Overall earthquake damage estimated ~US$10 billion (~50% of Nepal's GDP at the time); Langtang-specific loss not separately quantified.",
   gap="There was no early-warning or monitoring for quake-triggered landslides/avalanches; trekkers, villagers and lodges got no warning. Experts had warned of Nepal's seismic vulnerability for decades, but this was not matched by on-the-ground hazard monitoring — and the avalanche arrived within seconds.",
   src=[{"title":"April 2015 Nepal earthquake — Wikipedia","url":"https://en.wikipedia.org/wiki/April_2015_Nepal_earthquake"},
        {"title":"Jane Qiu, \u2018Killer landslides: the lasting legacy of Nepal's quake\u2019 — Nature (2016)","url":"https://doi.org/10.1038/532428a"},
        {"title":"\u2018Nepal quake: 52 bodies found in remote valley\u2019 — Los Angeles Times","url":"https://www.latimes.com/world/asia/la-fg-nepal-earthquake-dead-20150504-story.html"}]),
 dict(id="E3", name="2015 South India (Chennai) floods",
   date="8 November – 14 December 2015 (worst ~1–2 December).",
   location="Tamil Nadu (esp. Chennai), Puducherry, Andhra Pradesh — India's Coromandel coast.",
   type="Extreme northeast-monsoon urban river flooding.",
   what="Record rain submerged much of Chennai, including the airport. 500+ died and 1.8 million+ were displaced; it was the costliest natural disaster worldwide in 2015 and Chennai's worst flooding in a century.",
   how="A strong El Niño–boosted northeast monsoon and successive low-pressure systems dumped huge rain (Chennai: 1,049 mm in November, highest since 1918). The Eastern Ghats blocked clouds so they stalled over the city (\u201cupstream blocking\u201d). Unplanned building over wetlands/drainage, poor drainage and sudden reservoir releases turned it, in the CAG's words, into a \u201cman-made disaster\u201d.",
   deaths="500+ (Tamil Nadu 422 official and likely higher; Andhra Pradesh 81; Puducherry 3).",
   affected="1.8 million+ displaced; ~1.7 million housed in ~6,605 camps in Tamil Nadu; 1.1 million+ rescued around Chennai.",
   loss="~\u20b9200 billion (~US$2 billion) official; unofficial estimates exceeded \u20b91 trillion (~US$10 billion).",
   gap="Despite IMD rain forecasts, the city had poor flood-warning and drainage, built-over water sinks, and — critically — large reservoir releases (e.g. Chembarambakkam) and lake breaches with inadequate advance warning to downstream residents worsened the sudden early-December flooding.",
   src=[{"title":"2015 South India floods — Wikipedia","url":"https://en.wikipedia.org/wiki/2015_South_India_floods"},
        {"title":"Indian troops battle deadly flooding in Chennai — BBC News","url":"https://www.bbc.com/news/world-asia-india-34981246"},
        {"title":"As 35 lakes breach their banks, Chennai goes under again — The Hindu","url":"https://www.thehindu.com/news/cities/chennai/Complete-breakdown-of-essential-services/article60278957.ece"}]),
 dict(id="E3b", name="2017 South Asian floods — India (Bihar, Gujarat, Mumbai, NE)",
   date="July–September 2017 (Mumbai deluge 29 August).",
   location="Northern & western India — Bihar, Assam, West Bengal, Rajasthan, Uttar Pradesh, Gujarat, and Mumbai/Maharashtra.",
   type="Severe monsoon river flooding plus associated landslides and urban flooding.",
   what="A far-worse-than-average monsoon caused the worst South Asian floods in decades. In India alone 1,076 people died and over 31 million were affected by mid-August; over 85% of Kaziranga National Park was flooded. Mumbai was paralysed, and a century-old building collapse there killed at least 33.",
   how="The 2017 monsoon was unusually intense (experts linked it to climate change), overwhelming rivers and poorly drained embankments; in Mumbai, 298 mm of rain fell in 9 hours on 29 August at high tide, the highest single-August-day rainfall since 1997.",
   deaths="1,076 in India — 514 in Bihar, 224 in Gujarat, 152 in West Bengal, 76 in Assam, 72 in Uttar Pradesh, 38 in Maharashtra; the Mumbai building collapse alone killed 33.",
   affected="31+ million affected in India by mid-August; 800,000+ houses damaged or destroyed; 85%+ of Kaziranga flooded. (South Asia-wide: 45+ million affected, incl. 16 million children.)",
   loss="No single confirmed all-India monetary total in the source; damage spanned 800,000+ homes and vast ruined farmland, raising food-supply fears.",
   gap="Officials were criticised for weak preventive measures — in Bihar, embankments and roads were built with little or no drainage; Mumbai's loose building rules and drainage worsened its flooding. There was no effective flood early-warning that reached the worst-hit rural districts in time.",
   src=[{"title":"2017 South Asian floods — Wikipedia","url":"https://en.wikipedia.org/wiki/2017_South_Asian_floods"},
        {"title":"India floods: more than 1,000 killed as monsoon rains sweep South Asia — The Guardian","url":"https://www.theguardian.com/world/2017/aug/30/mumbai-paralysed-by-floods-as-india-and-region-hit-by-worst-monsoon-rains-in-years"}]),
 dict(id="E4", name="2018 Kerala floods and landslides",
   date="July–August 2018 (worst 15–17 August).",
   location="Kerala, India — all 14 districts on red alert; worst in Chengannur, Kuttanad, Chalakudy/Aluva (Periyar), and hill districts Idukki & Wayanad.",
   type="Monsoon river flooding plus hill-district landslides.",
   what="Kerala's worst floods since 1924. Rivers and dams overflowed, submerging central/southern Kerala. 483+ died, ~1 million moved to camps; Wayanad and Idukki were cut off by landslides; declared a Level-3 \u201ccalamity of a severe nature\u201d.",
   how="Seasonal rain ran ~23% above normal (August ~164% above normal; ~310 mm in one 48-hour spell). With reservoirs already >90% full, 35 dams had to be opened for the first time ever (incl. all five Idukki gates), surging water into swollen rivers; saturated slopes failed in Wayanad/Idukki. Studies attribute the main driver to extreme rain; a court advisor's report blamed dam management for worsening it.",
   deaths="483+ confirmed (CM, mid-Sept 2018); some counts ~500 across the season.",
   affected="~1 million evacuated; 800,000+ in ~4,000 camps; about one-sixth of the state's population directly affected.",
   loss="~\u20b940,000 crore (~US$4.2 billion) — more than the state's annual plan outlay.",
   gap="Rain warnings and red alerts existed, but there was no effective coordinated warning for the sudden, near-simultaneous opening of 35 dams; operators had kept reservoirs full rather than holding a flood cushion, so downstream residents got little advance warning.",
   src=[{"title":"483 dead in Kerala floods and landslides — The Indian Express","url":"https://indianexpress.com/article/india/483-dead-in-kerala-floods-and-landslides-losses-more-than-annual-plan-outlay-pinarayi-vijayan-5332306/"},
        {"title":"Lapses in dam management worsened Kerala floods (amicus curiae) — The Hindu","url":"https://www.thehindu.com/news/national/kerala/amicus-curiae-for-panel-to-identify-flood-causes/article26726699.ece"},
        {"title":"2018 Kerala floods — Wikipedia","url":"https://en.wikipedia.org/wiki/2018_Kerala_floods"}]),
 dict(id="E5", name="2019 Kerala floods (Puthumala & Kavalappara landslides)",
   date="8–29 August 2019; the deadly landslides on 8 August.",
   location="Northern Kerala — Malappuram (Kavalappara, near Nilambur) and Wayanad (Puthumala) worst hit.",
   type="Monsoon flooding plus ~80 rain-triggered landslides in two days.",
   what="Heavy rain triggered ~80 landslides; the Kavalappara and Puthumala debris slides buried whole settlements alive. Statewide, 121 died and 200,000+ moved to camps; Malappuram was worst hit.",
   how="An Arabian-Sea depression drove intense rain; water fell so fast that steep, saturated hillslopes lost strength and failed, sending mud-and-debris flows over homes and farmland and flash floods down streams.",
   deaths="121 statewide (as of 19–20 Aug 2019); 58 in Malappuram alone.",
   affected="~21 missing statewide (13 in Malappuram); 200,000+ in 1,318 camps; 1,789 houses fully destroyed and 14,542 partially damaged (8–19 Aug).",
   loss="\u20b92,101.9 crore (~US$220 million) reported damage.",
   gap="IMD issued rain alerts (red for 9 districts), so a general weather warning existed — but there was no site-specific landslide early-warning for vulnerable slopes, so Puthumala and Kavalappara struck suddenly and buried people before they could escape.",
   src=[{"title":"2019 Kerala floods — Wikipedia","url":"https://en.wikipedia.org/wiki/2019_Kerala_floods"},
        {"title":"Kerala Floods 2019: 121 dead, 1,789 houses collapsed — NewsClick","url":"https://www.newsclick.in/kerala-floods-2019-121-dead-1789-houses-collapsed"},
        {"title":"Kerala seeks package for \u20b92,101.9 crore flood damage — Onmanorama","url":"https://www.onmanorama.com/news/kerala/2019/09/20/kerala-centre-special-package-flood-2019.html"}]),
 dict(id="E6", name="2020 Assam floods",
   date="May–August 2020 (worst in July), continuing into October.",
   location="Assam, NE India — along the Brahmaputra; 30 of 33 districts, 5,474 villages.",
   type="Monsoon river flood, with related landslides, during the COVID-19 pandemic.",
   what="The Brahmaputra and tributaries overflowed for months. By October, 5 million+ had been affected and 150,000+ sheltered in camps; Kaziranga National Park and Pobitora were flooded, killing many animals.",
   how="The 2020 monsoon ran ~15 cm above normal by mid-July; the Assam–Meghalaya region got 1,164 mm vs a 894 mm normal (~30% excess), linked to the Madden–Julian Oscillation and prolonged break-monsoon conditions. The swollen Brahmaputra burst its banks and triggered landslides.",
   deaths="149 (123 flood + 26 landslide) as of 14 Oct 2020; ~44.5% of flood deaths were children who drowned.",
   affected="5 million+ at peak; 150,000+ in 627 relief camps; 267,203+ hectares of crops destroyed; 45,000+ animals displaced.",
   loss="State announced ~\u20b93.46 billion (~US$42 million) for repairs/aid (relief funding, not a full damage estimate).",
   gap="Assam floods almost every monsoon, yet there was no dedicated regional flash-flood early-warning system at the time — the WMO's South Asia Flash Flood Guidance System only launched on 23 October 2020, as this disaster was ending.",
   src=[{"title":"2020 Assam floods — Wikipedia","url":"https://en.wikipedia.org/wiki/2020_Assam_floods"},
        {"title":"Assam State Disaster Management Authority — cumulative flood reports","url":"http://www.asdma.gov.in/cumulative_reports.html"},
        {"title":"Excessive Monsoon Rains Flood Asia — NASA Earth Observatory","url":"https://earthobservatory.nasa.gov/images/147006/excessive-monsoon-rains-flood-asia"}]),
 dict(id="E7", name="2021 Uttarakhand (Chamoli / Rishiganga) glacier-flood disaster",
   date="7 February 2021 (morning).",
   location="Chamoli district, Uttarakhand — Rishiganga/Dhauliganga/Alaknanda valleys near Nanda Devi; Reni, Tapovan, Joshimath.",
   type="Rock-and-ice avalanche (hanging-glacier collapse) that became a flash debris-flood. First wrongly reported as a GLOF — satellites proved there was no lake.",
   what="A huge rock-and-ice mass broke off a peak above the Ronti Gad and created a sudden flood wave down the Rishiganga and Dhauliganga, destroying the Rishiganga hydro project and badly damaging the Tapovan Vishnugad plant, trapping and killing many workers.",
   how="A block of rock with a hanging glacier (~27 million m³, ~80% rock/20% ice) fell ~3.2 km; the ice melted into water, mixed with rock/debris and formed a fast debris-flood wave that swept away the projects, dam, bridges and the Tapovan plant.",
   deaths="83 bodies (plus 36 body parts) recovered; confirmed dead-and-missing total 204 (reports said up to ~300); ~140 were Tapovan workers.",
   affected="Of 204 missing, most never found; ~35 missing at Rishiganga/Reni and ~176 Tapovan workers (incl. men trapped in tunnels); a bridge linking 13 villages washed away; 600+ houses later evacuated in Joshimath.",
   loss="~\u20b91,500 crore (~US$206 million) to the Tapovan project; the 13.2 MW Rishiganga project destroyed; no single all-in official total.",
   gap="There was no early-warning/monitoring for sudden rock-and-ice avalanches, so the wave hit dam workers and villages with almost no warning. A Supreme Court-appointed committee (Dr Ravi Chopra) and scientists had warned against hydropower in this fragile warming paraglacial zone; Reni villagers' relocation requests were ignored.",
   src=[{"title":"A massive rock and ice avalanche caused the 2021 Chamoli disaster — Science (Shugar et al.)","url":"https://www.science.org/doi/10.1126/science.abh4455"},
        {"title":"Satellites reveal cause of Chamoli disaster — European Space Agency","url":"https://www.esa.int/Applications/Observing_the_Earth/Satellites_reveal_cause_of_Chamoli_disaster"},
        {"title":"Before Himalayan flood, India ignored warnings of development risks — The New York Times","url":"https://www.nytimes.com/2021/02/08/world/asia/india-flood-ignored-warnings.html"},
        {"title":"2021 Uttarakhand flood — Wikipedia","url":"https://en.wikipedia.org/wiki/2021_Uttarakhand_flood"}]),
 dict(id="E8", name="2022 Amarnath cloudburst",
   date="8 July 2022 (evening).",
   location="Near the Amarnath cave shrine (~3,900 m), Anantnag district, Jammu & Kashmir, India.",
   type="Cloudburst-triggered flash flood.",
   what="A sudden cloudburst during the Amarnath Yatra sent a wall of water down a gorge, sweeping away ~two dozen pilgrim tents and two kitchens near the lower base camp. 16+ died and dozens went missing; ~10,000 pilgrims were camped nearby.",
   how="A cloudburst (an intense, highly localized downpour) over the steep slope above the shrine could not drain fast enough and gathered into a fast flash flood that poured down a narrow gorge directly onto the camps.",
   deaths="16+ confirmed (as of 9 July 2022).",
   affected="40+ reported missing; ~10,000 pilgrims in the area; ~15,000 rescued/evacuated; ~24 tents and two langars washed away.",
   loss="Not quantified; \u20b95 lakh ex-gratia announced per deceased family.",
   gap="No effective early warning — the cloudburst was sudden and localized and the ~10,000 pilgrims had no advance alert. The remote high-altitude route lacked dense real-time rainfall monitoring and a shrine-area flash-flood warning system, so camps could not be evacuated in time.",
   src=[{"title":"2022 Amarnath floods — Wikipedia","url":"https://en.wikipedia.org/wiki/2022_Amarnath_floods"},
        {"title":"Several killed, dozens missing in floods at Kashmir pilgrimage — Al Jazeera","url":"https://www.aljazeera.com/news/2022/7/8/at-least-10-killed-in-floods-during-pilgrimage-in-kashmir"},
        {"title":"15,000 rescued, 40 still missing after Amarnath cloudburst — NDTV","url":"https://www.ndtv.com/india-news/amarnath-cloudburst-15-000-rescued-40-still-missing-after-cloudburst-near-cave-shrine-10-facts-3141822"}]),
 dict(id="E9", name="2023 Joshimath land subsidence",
   date="Crisis peaked first week of January 2023; sinking long-building (noted since the 1970s).",
   location="Joshimath (Jyotirmath), Chamoli district, Uttarakhand (~1,890 m) — gateway to Badrinath.",
   type="Slow-onset land subsidence (ground sinking) in a landslide-prone town — not a flood.",
   what="The ground under Joshimath sank and cracked homes, roads and fields. By January 2023 ~678 buildings had cracks and officials said ~30% of the town was affected; residents were evacuated and the most unsafe buildings demolished. A 2023 IIRS study found the area sinking ~6.5 cm per year.",
   how="The town sits on loose old landslide/glacial debris (moraine), never solid rock. Decades of heavy construction, population growth, poor drainage and large infrastructure/hydropower work (incl. NTPC Tapovan Vishnugad tunnelling — which NTPC denies caused it), plus water seepage and the aftermath of the Feb-2021 flood, slowly settled the slope and cracked the buildings.",
   deaths="None from the subsidence itself (slow-onset; people were evacuated).",
   affected="No missing. ~678 buildings cracked; ~30% of a ~25,000-person town affected; hundreds evacuated to camps; several structures marked for demolition.",
   loss="No single confirmed total; damage spanned hundreds of homes/hotels/roads; the state announced relief and rehabilitation packages.",
   gap="No real-time subsidence monitoring/early-warning, though the danger had been flagged for decades — the 1976 Mishra Committee warned the town stood on unstable deposits and advised limiting construction, but building continued. Residents watched cracks widen for months before emergency evacuation in January 2023.",
   src=[{"title":"Demolitions begin in India's \u2018sinking\u2019 Joshimath — Al Jazeera","url":"https://www.aljazeera.com/news/2023/1/10/demolitions-begin-in-indias-sinking-joshimath-hundreds-moved"},
        {"title":"Why is Joshimath sinking? Alarm bells ringing since 1976 — India Today","url":"https://www.indiatoday.in/science/story/why-is-joshimath-sinking-alarm-bells-in-hill-town-ringing-since-1976-2318223-2023-01-06"},
        {"title":"Joshimath subsidence: satellite-based preliminary report — NRSC/ISRO (archived)","url":"https://web.archive.org/web/20230112080218/https://www.nrsc.gov.in/sites/default/files/pdf/DMSP/Joshimath_landslide_11Jan2023.pdf"}]),
 dict(id="E10", name="2023 North India / Himachal Pradesh monsoon floods & landslides",
   date="April 2023 onward; worst late June–August (spikes ~9–10 July and mid-August).",
   location="North India — mainly Himachal Pradesh (Shimla, Manali, Kullu); also Uttarakhand, Punjab, Haryana, Delhi (Yamuna), J&K, Rajasthan, UP.",
   type="Monsoon flooding, flash floods, cloudbursts and landslides.",
   what="Heavy monsoon rain caused severe flooding and landslides, hitting Himachal hardest; ~105 died over two weeks in July and ~71 more in Himachal plus 10 in Uttarakhand in an August round. In Delhi the Yamuna hit its highest level in 45+ years, forcing thousands into camps.",
   how="A strong monsoon surge plus a western disturbance dumped the heaviest rain in decades (up to ~30 cm), overflowing rivers and saturating slopes that then collapsed; cloudbursts added sudden surges. In Delhi, upstream rain plus large Hathnikund Barrage releases pushed the Yamuna past its record. Experts linked the intensity to climate change.",
   deaths="422 across North India (as of ~Sept 2023): Himachal 330+, Uttarakhand ~75, UP 12+, J&K 4+, Delhi 1+; 100+ injured.",
   affected="~38 missing (mostly Himachal); ~70,000 tourists evacuated from Himachal; 1,000+ roads blocked; ~9,600 houses damaged; 170 cloudburst/landslide incidents; ~16,000 sheltered in Delhi.",
   loss="Himachal CM estimated ~\u20b910,000 crore (~US$1.2 billion); no reliable all-India total.",
   gap="Warnings were only partly effective: Haryana saw its first-ever flood warning and Delhi issued evacuation advisories as the Yamuna rose — but in the hills most deaths came from sudden cloudbursts and landslides that are very hard to forecast and gave little or no advance warning, and record rainfall overwhelmed preparedness.",
   src=[{"title":"2023 North India floods — Wikipedia","url":"https://en.wikipedia.org/wiki/2023_North_India_floods"},
        {"title":"India floods: monsoon rains leave dead in north as Delhi sees record July rain — The Guardian","url":"https://www.theguardian.com/world/2023/jul/10/india-floods-new-delhi-rain-record-deaths"}]),
 dict(id="E11", name="2023 Sikkim South Lhonak Lake GLOF (Teesta flood)",
   date="Night of 3–4 October 2023.",
   location="South Lhonak Lake and the Teesta valley, Sikkim; downstream West Bengal (Kalimpong, Jalpaiguri, etc.) and parts of Bangladesh.",
   type="Glacial lake outburst flood (GLOF) / flash flood — a textbook case of the hazard our project targets.",
   what="The glacial South Lhonak Lake burst and surged down the Teesta. The wave reached the Teesta III dam at Chungthang around midnight and destroyed it within ~10 minutes before its gates could be opened; downstream the river rose ~15–20 ft, washing away bridges and roads and cutting off north Sikkim. It was the deadliest flood there since 1968.",
   how="Several times the normal rainfall (about five times normal over 3–4 October) hit Sikkim; the moraine-dammed lake — enlarged as its feeder glacier retreated — overflowed and breached. The sudden release formed a powerful flood wave that destroyed Teesta III and flooded downstream towns.",
   deaths="55+ by 6 October, rising to 92 confirmed by 18 October 2023.",
   affected="~75 missing (incl. 23 Army personnel); ~2,400 evacuated and ~7,600 sheltered in Sikkim, ~10,000 evacuated in West Bengal; ~3,000 tourists stranded; 15 bridges washed away; the 1,200 MW Teesta III dam destroyed.",
   loss="No reliable total; central government released \u20b948 crore (~US$5.76 million) in relief; major losses include 15 bridges and the Teesta III dam/powerhouse.",
   gap="A dedicated GLOF early-warning system for South Lhonak was still being developed and not fully operational, even though the lake was a known risk (pipelines installed in 2018 to lower its level). An ITBP warning reportedly came ~midnight, but Teesta III operators could not open the gates in time and downstream communities had little or no advance warning.",
   src=[{"title":"Floods in India's Sikkim state leave dead and missing — Reuters","url":"https://www.reuters.com/world/india/nearly-two-dozen-indian-troops-missing-after-flash-flood-ani-2023-10-04/"},
        {"title":"Sikkim dam washed away in 10 minutes after flash flood — Hindustan Times","url":"https://www.hindustantimes.com/cities/others/sikkims-biggest-hydro-project-suffers-massive-damage-in-flash-flood-101696420752235.html"},
        {"title":"2023 Sikkim flash floods — Wikipedia","url":"https://en.wikipedia.org/wiki/2023_Sikkim_flash_floods"}]),
 dict(id="E12", name="2024 Wayanad landslides (Kerala)",
   date="30 July 2024 (first slide ~02:17 IST, second ~04:10 IST).",
   location="Punjirimattom, Mundakkai, Chooralmala, Vellarimala villages, Meppadi, Wayanad, Kerala — Western Ghats, near streams feeding the Chaliyar.",
   type="Rain-triggered landslides (debris flows) followed by flash flooding.",
   what="A series of rain-triggered landslides and a flash flood destroyed four hill villages, killing 420+ — one of Kerala's deadliest disasters.",
   how="Heavy monsoon rain saturated steep slopes; an uphill rainfall-induced \u201cdam burst\u201d released a sudden surge, and a fast debris flow plus flash flood swept down the valley and destroyed the villages.",
   deaths="420+ (as of Aug–Sept 2024); ~231 bodies in the first week, with more bodies and body parts found later (200+ in the Chaliyar river).",
   affected="~118 missing; 397 injured; ~10,000 displaced (9,300+ in 91 camps); 1,555+ buildings, 290 shops, 3 bridges, ~124 km of power lines and ~600 ha of land damaged; at least five children orphaned.",
   loss="~\u20b91,200 crore (~US$120 million) stated to the Kerala High Court; the state said \u20b92,000 crore more needed for rehabilitation.",
   gap="The IMD rainfall forecast badly underestimated the downpour; some residents were moved from 29 July, but many in Chooralmala stayed because the area was not officially classified landslide-prone — even though 2020 local documents had marked these wards as landslide-prone and the Gadgil panel's ecological-protection recommendations were never implemented.",
   src=[{"title":"2024 Wayanad landslides — Wikipedia","url":"https://en.wikipedia.org/wiki/2024_Wayanad_landslides"}]),
 dict(id="E13", name="2025 Uttarakhand (Dharali / Harsil, Uttarkashi) flash flood",
   date="5 August 2025.",
   location="Dharali village (on the Gangotri pilgrim route) and Harsil, Uttarkashi district, Uttarakhand, India; along the Kheer Ganga river.",
   type="Flash flood / debris flow — cause still under investigation: a cloudburst, a glacial lake outburst flood (GLOF), a glacier collapse, a landslide, or a combination.",
   what="A sudden, violent surge of water, mud and boulders tore through Dharali village and Harsil on 5 August 2025, crushing houses, shops and hotels in periodic waves of debris. The Dharali market was submerged and part of the Harsil Army camp and helipad was damaged. Dramatic visuals showed buildings being obliterated.",
   how="Media first reported a cloudburst over the steep catchment; scientists are also examining whether a GLOF, a glacier collapse or a landslide (or a mix) made the Kheer Ganga river overflow with immense force. The flood carried a huge load of debris and mud downhill. Afterwards, a temporary lake about 400–500 m long formed upstream at Harsil, raising fears of a second flood if that natural dam breached — and a second cloudburst struck Sukhi Top near Dharali soon after.",
   deaths="At least 5 confirmed initially; more than 70 presumed dead as of 14 August 2025, per the encyclopaedic account; locals feared hundreds could be trapped under the debris.",
   affected="Reported as 50–100+ missing (officials confirmed 43 missing on 12 August; 11 soldiers were among the missing). About 190 people were rescued; the Army's Ibex Brigade, NDRF, SDRF and ITBP mounted a large air-and-ground operation. Connectivity to Gangotri Dham was cut and the Char Dham Yatra was disrupted.",
   loss="Not yet quantified in money; preliminary assessments cite at least 50 hotels destroyed and ~40–50 houses swept away, plus damage to the Harsil Army camp and helipad.",
   gap="The IMD had issued a heavy-rainfall warning for the region (through about 10 August), but the debris surge struck Dharali suddenly with no localized, slope-/lake-specific alert — and the very cause remained uncertain (cloudburst vs GLOF vs glacier collapse vs landslide), which is exactly the ambiguity a fused multi-sensor system is built to resolve. The post-event temporary lake at Harsil is a live example of a hazard that needs continuous monitoring to warn those downstream.",
   src=[{"title":"2025 Uttarakhand flash flood — Wikipedia","url":"https://en.wikipedia.org/wiki/2025_Uttarakhand_flash_flood"},
        {"title":"Uttarkashi floods: death toll reaches 5, 11 soldiers missing — Business Standard","url":"https://www.business-standard.com/india-news/uttarkashi-floods-cloudburst-dharali-death-toll-missing-rescue-operation-125080600931_1.html"},
        {"title":"Uttarkashi cloudburst live updates: 5 dead, 100 missing, including Army jawans — Hindustan Times","url":"https://www.hindustantimes.com/india-news/uttarkashi-cloudburst-live-updates-uttarakhand-flash-floods-dharali-cloudburst-harsil-rescue-death-toll-missing-army-101754438886197.html"},
        {"title":"Glacier collapse or lake burst likely caused Dharali destruction: experts — The Times of India","url":"https://timesofindia.indiatimes.com/india/glacier-collapse-or-lake-burst-likely-caused-dharali-destruction-experts/articleshow/123127901.cms"}]),
]

for i, e in enumerate(events, start=1):
    doc.add_heading(f"E{i}.  {e['name']}", level=2)
    field("Date:", e["date"], color=GREY)
    field("Location:", e["location"], color=GREY)
    field("Type:", e["type"])
    field("What happened:", e["what"])
    field("How it happened:", e["how"])
    deaths_field(e["deaths"])
    field("Missing / affected / displaced:", e["affected"], color=GREY)
    field("Economic damage:", e["loss"], color=GREY)
    field("Early-warning gap:", e["gap"], color=RED)
    sources_block(e["src"])
    doc.add_paragraph()

# ===================== PART C: PATTERNS =====================
doc.add_heading("Part C — The common thread: the same failure, again and again", level=1)
doc.add_paragraph("Read together, these disasters repeat a small set of failures:")
patterns = [
 ("Hazards were known, warnings were not localized or timely.", "In Kedarnath, Chennai, Kerala, Chamoli, Sikkim, Joshimath and Wayanad, scientists, committees or local documents had already identified the danger. What was missing was a system that converted that knowledge into a specific, on-time warning that reached the exact village or camp at risk."),
 ("General weather forecasts are not landslide/GLOF warnings.", "Rain alerts (even red alerts) existed in 2018, 2019, 2023 and 2024, yet people were still buried alive, because there was no slope- or lake-specific prediction tied to the physics of failure."),
 ("Infrastructure releases and dam breaks surprised people downstream.", "Chennai 2015 (reservoir releases/lake breaches), Kerala 2018 (35 dams opened near-simultaneously) and Sikkim 2023 (Teesta III destroyed in ~10 minutes) all show the deadly gap between an upstream event and a downstream alert."),
 ("Remote, high-altitude, low-connectivity areas had no reach.", "Amarnath camps, Langtang, and north Sikkim had little or no means to receive a warning in time — the \u201clast mile\u201d failed even where a signal existed."),
 ("The window is minutes.", "Rock-ice avalanches (Chamoli), cloudbursts (Amarnath) and lake bursts (Sikkim) give seconds-to-minutes of lead time. Any useful system must be fast, automated in sensing, and able to push an alert without waiting for a human to notice."),
]
for t,b in patterns:
    pp = doc.add_paragraph(style="List Bullet"); r = pp.add_run(t+" "); r.bold=True; pp.add_run(b)

# ===================== PART D: NOVELTY =====================
doc.add_heading("Part D — Why TRINETRA / HIMKAVACH is different (the novelty)", level=1)
doc.add_paragraph(
 "TRINETRA / HIMKAVACH is designed precisely around the failures in Part C. It is an offline-first, "
 "multi-sensor, physics-grounded, advisory early-warning system (EWS): it keeps a human in the loop and "
 "never acts autonomously. Below, each core capability is tied to the real disasters it directly addresses.")

def nov(title, body, events_covered):
    doc.add_heading(title, level=2)
    p = doc.add_paragraph(); p.add_run(body)
    e = doc.add_paragraph(); r = e.add_run("Directly addresses: "); r.bold = True; r.font.color.rgb = GREEN
    e.add_run(events_covered)

nov("1. It fuses many sensors into one physics decision — not just a rain forecast",
 "Instead of a single rain alert, the system combines satellite rainfall (GPM/IMERG), soil moisture "
 "(SMAP) and reanalysis (ERA5-Land) with slope physics — a Caine intensity–duration rainfall threshold "
 "and a Factor-of-Safety slope-stability calculation. It does not just say \u2018heavy rain is coming\u2019; it "
 "estimates whether a specific saturated slope is about to fail. That is the gap that killed people in "
 "2018, 2019 and 2024 despite red rain alerts.",
 "2018 & 2019 Kerala, 2023 Himachal, 2024 Wayanad.")
nov("2. All-weather, day-and-night radar eyes — it sees through the storm",
 "Disasters strike under cloud and at night, exactly when optical cameras are blind. The system uses "
 "Sentinel-1 Synthetic Aperture Radar (which sees through cloud and darkness), plus Sentinel-2 optical, "
 "MODIS daily coverage, ITS_LIVE glacier-velocity and InSAR ground-deformation. This combination can flag "
 "a growing glacial lake, an accelerating glacier, or a slope creeping before it collapses.",
 "2021 Chamoli (glacier/ice collapse), 2023 Sikkim GLOF (growing moraine lake), 2023 Joshimath (slow subsidence).")
nov("3. A dedicated GLOF module and downstream lead-time model",
 "The system is built on real GLOF knowledge bases (the High Mountain Asia GLOF database with 766 recorded "
 "events, and multimodal GLOF datasets). It can keep known-dangerous lakes (like South Lhonak) on a watch "
 "list and model the downstream flood-wave travel time — turning an upstream lake burst into a few precious "
 "minutes of warning for dams and villages below, the exact margin missing when Teesta III fell in ten minutes.",
 "2013 Kedarnath (Chorabari), 2023 Sikkim South Lhonak GLOF.")
nov("4. Offline-first \u2018last-mile\u2019 delivery to remote valleys",
 "Warnings only save lives if they arrive. The system is offline-first and designed to push alerts over "
 "resilient, low-bandwidth channels so they reach high-altitude camps and cut-off valleys that normal "
 "networks never cover — the places where Amarnath pilgrims and Langtang trekkers received nothing.",
 "2015 Langtang, 2022 Amarnath, remote north Sikkim 2023.")
nov("5. An honest decision layer with a GLOF safety shield and a mandatory human gate",
 "The decision engine quantifies its own uncertainty (conformal prediction), applies a GLOF safety floor "
 "that can only RAISE a glacial-flood risk to Red (never silently downgrade it), and requires explicit "
 "human approval before any public alert. It is advisory, never autonomous — the opposite of the \u2018nobody "
 "was watching / nobody could act in time\u2019 pattern — while refusing to be the single machine that cries wolf.",
 "All events — especially 2015 Chennai & 2018 Kerala (uncoordinated releases) and 2023 Sikkim (no time to act).")
nov("6. Social media as corroboration only — and deepfake-resistant",
 "The system can use crisis social-media signals, but caps their trust so they can never, on their own, "
 "trigger or suppress a life-safety alert. This keeps it fast where ground sensors are sparse, without "
 "being fooled by rumour or manipulated content.",
 "Fast-moving urban/known events (e.g. 2015 Chennai, 2023 North India).")

doc.add_heading("The honest bottom line", level=2)
hp = doc.add_paragraph()
hp.add_run("What is genuinely novel ").bold = True
hp.add_run("is the integration: a single offline-first stack that goes from real multi-sensor Earth "
 "observation, through transparent physics and an uncertainty-aware decision layer with a GLOF shield, to "
 "a human-approved alert delivered over the last mile — purpose-built for exactly the Himalayan failure "
 "modes documented above, where today's systems are fragmented, cloud-blind, or stop at a generic rain "
 "forecast.")
hp2 = doc.add_paragraph()
hr = hp2.add_run("What we are honest about: "); hr.bold = True; hr.font.color.rgb = RED
hp2.add_run("In its current form the physics is implemented on real equations but is SIMULATED (there are "
 "no trained model weights yet); the hazard datasets are a verified, licence-checked plan, not downloaded "
 "or trained; and any specific detections, flood shapes, evacuation routes or people-counts shown in demos "
 "are ILLUSTRATIVE. The claim is not that the system has already prevented these disasters — it is that it "
 "is designed, feature by feature, to close the specific warning gaps that made each of them so deadly.")

# ===================== PART E: TOTALS =====================
doc.add_heading("Part E — The ten-year toll, added up", level=1)
doc.add_paragraph(
 "The table below totals the reported figures from every event in this report. Please read the caveats "
 "under it: these are sums of numbers reported by the sources, they mix countries (India, Nepal, Pakistan) "
 "and causes, some are approximate, and many events had no official money figure — so the economic total "
 "is a conservative LOWER BOUND, not the true cost.")

# label, deaths_num(for sum, India/Himalaya water-slope focus), deaths_disp, loss_cr(for sum), loss_disp, affected_disp
toll = [
 ("2013 Kedarnath floods", 6054, "~6,054", None, "Not quantified (catastrophic)", "~300,000 trapped; 110,000+ evacuated; 4,550 villages"),
 ("2014 J&K floods", 557, "557 (277 India, 280 Pakistan)", 5000, "~\u20b95,000–6,000 cr (up to ~\u20b91,00,000 cr claimed)", "~200,000 rescued; ~2,600 villages"),
 ("2015 Nepal earthquake (incl. Langtang)", 0, "8,962 total quake (~372 by landslide/avalanche)", None, "~US$10 bn (whole quake, Nepal)", "~3.5 million left homeless"),
 ("2015 Chennai floods", 500, "500+", 20000, "~\u20b920,000 cr official (unofficial >\u20b91,00,000 cr)", "~1.8 million displaced"),
 ("2017 South Asian floods (India)", 1076, "1,076", None, "Not given as one total", "31+ million affected; 800,000+ houses"),
 ("2018 Kerala floods", 483, "483+", 40000, "~\u20b940,000 cr", "~1 million evacuated"),
 ("2019 Kerala floods", 121, "121", 2102, "~\u20b92,101.9 cr", "200,000+ in camps"),
 ("2020 Assam floods", 149, "149", 346, "~\u20b9346 cr relief (not full damage)", "~5 million affected"),
 ("2021 Chamoli glacier flood", 204, "204 dead/missing", 1500, "~\u20b91,500 cr (Tapovan)", "~600 houses later evacuated"),
 ("2022 Amarnath cloudburst", 16, "16+", None, "Not quantified", "~10,000 pilgrims in area"),
 ("2023 Joshimath subsidence", 0, "0 (slow-onset)", None, "Not quantified", "~678 buildings; ~30% of town"),
 ("2023 Himachal / N-India floods", 422, "422", 10000, "~\u20b910,000 cr (Himachal)", "~70,000 tourists evacuated"),
 ("2023 Sikkim GLOF (Teesta)", 92, "92", 48, "~\u20b948 cr relief released", "~22,000 evacuated/sheltered"),
 ("2024 Wayanad landslides", 420, "420+", 1200, "~\u20b91,200 cr (+\u20b92,000 cr rehab)", "~10,000 displaced"),
 ("2025 Dharali flash flood", 70, "70+ presumed", None, "Not quantified", "50–100+ missing; thousands hit"),
]
tt = doc.add_table(rows=1, cols=4); tt.style = "Light Grid Accent 1"
hdr = tt.rows[0].cells
for j,txt in enumerate(["Event","Lives lost (reported)","Economic damage (reported)","People affected / displaced"]):
    hdr[j].text = txt
    for pp in hdr[j].paragraphs:
        for rr in pp.runs: rr.bold = True; rr.font.size = Pt(9.5)
for lbl,dn,dd,lc,ld,ad in toll:
    c = tt.add_row().cells
    c[0].text = lbl; c[1].text = dd; c[2].text = ld; c[3].text = ad
    for cc in c:
        for pp in cc.paragraphs:
            for rr in pp.runs: rr.font.size = Pt(9)

sum_deaths = sum(dn for _,dn,_,_,_,_ in toll)                 # India/Himalaya water-slope focus (Nepal quake counted as ~0 here)
sum_deaths_all = sum_deaths + 8962                            # including full 2015 Nepal earthquake
sum_loss = sum(lc for _,_,_,lc,_,_ in toll if lc)            # lower-bound, quantified only

doc.add_paragraph()
doc.add_heading("Bottom line — the grand totals", level=2)
def big(label, value, color=RED):
    p = doc.add_paragraph(); r = p.add_run(label+"  "); r.bold=True; r.font.color.rgb=GREY
    rv = p.add_run(value); rv.bold=True; rv.font.size=Pt(13); rv.font.color.rgb=color
    return p
big("Total lives lost (flood / landslide / GLOF / cloudburst events here):", f"~{sum_deaths:,} people")
big("…and about ~{:,} if the full 2015 Nepal earthquake toll (8,962) is included.".format(sum_deaths_all), "")
big("Total economic damage (conservative LOWER BOUND of the money figures that exist):", f"~\u20b9{sum_loss:,} crore (~US$9–10 billion)")
big("People affected / displaced:", "Tens of millions — at least ~42 million across these events")

cv = doc.add_paragraph()
cv.add_run("Important caveats. ").bold = True
cv.add_run(
 f"(1) The death total of ~{sum_deaths:,} is dominated by the 2013 Kedarnath disaster (~6,054). The 2015 "
 "Nepal earthquake's 8,962 is kept separate because most of those deaths were from building collapse in "
 "Nepal, not floods or landslides. (2) The economic figure of about \u20b9"+f"{sum_loss:,}"+" crore is a "
 "LOWER BOUND only: it adds up just the events that have a stated damage number, several of those are "
 "relief amounts rather than full damage, and it leaves out big events with no official total (2013 "
 "Kedarnath, 2017 India-wide, 2022 Amarnath, 2025 Dharali). If the 2015 Nepal earthquake (~US$10 bn) and "
 "the high-end unofficial estimates for Chennai and J&K (each ~\u20b91,00,000 crore) are counted, the true "
 "ten-year cost runs into several lakh crore. (3) \u2018People affected\u2019 is dominated by the 2017 floods "
 "(31 million) and 2020 Assam (5 million); the ~42 million is itself a conservative sum. Every number here "
 "is traceable to the per-event sources in Part B.")

# ===================== APPENDIX: ALL SOURCES =====================
doc.add_heading("Appendix — consolidated source list", level=1)
seen = set()
allsrc = [{"title":"Glacial lake outburst flood — Wikipedia","url":"https://en.wikipedia.org/wiki/Glacial_lake_outburst_flood"}]
for e in events:
    allsrc += e["src"]
for s in allsrc:
    if s["url"] in seen: continue
    seen.add(s["url"])
    sp = doc.add_paragraph(style="List Bullet"); sp.paragraph_format.space_after = Pt(1)
    hyperlink(sp, s["url"], s["title"])

doc.save(OUT)
print("SAVED:", OUT, "| paragraphs:", len(doc.paragraphs), "| events:", len(events))
