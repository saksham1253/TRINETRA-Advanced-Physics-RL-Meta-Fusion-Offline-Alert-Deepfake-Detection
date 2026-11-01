# -*- coding: utf-8 -*-
"""Append an on-brand 'Deep-Dive Appendix' to the TRINETRA deck.
Original 8 slides + template are preserved untouched; we only ADD slides at the end.
Palette sampled from the deck XML:
  bg #000000, panel #16152B, violet #6A45F0, blue #2F4FC9, gold #FFD36B, cream #FFF4D6,
  white #FFFFFF, grey #C8D1D9. Tags: A=green #19C37D, B=blue #2F4FC9, C=gold #FFD36B.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import copy

SRC = r"C:\Users\Dell\Documents\deepseek-harness\default-workspace\ppt_work\original.pptx"
OUT = r"C:\Users\Dell\Documents\deepseek-harness\default-workspace\ppt_work\TRINETRA_SAARTHI26_SANKAT_MOCHAK_v4_enhanced.pptx"

BLACK=RGBColor(0,0,0); PANEL=RGBColor(0x16,0x15,0x2B); PANEL2=RGBColor(0x0E,0x0D,0x1F)
VIOLET=RGBColor(0x6A,0x45,0xF0); BLUE=RGBColor(0x2F,0x4F,0xC9); GOLD=RGBColor(0xFF,0xD3,0x6B)
CREAM=RGBColor(0xFF,0xF4,0xD6); WHITE=RGBColor(0xFF,0xFF,0xFF); GREY=RGBColor(0xC8,0xD1,0xD9)
GREEN=RGBColor(0x19,0xC3,0x7D); MUTE=RGBColor(0x8A,0x90,0xA6)
FONT="Segoe UI"; MONO="Consolas"

prs = Presentation(SRC)
EMUW, EMUH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]
W = prs.slide_width.inches; H = prs.slide_height.inches  # 20 x 11.25

def _solid(shape, color):
    shape.fill.solid(); shape.fill.fore_color.rgb = color
def _noline(shape):
    shape.line.fill.background()
def _line(shape, color, w=1.0):
    shape.line.color.rgb = color; shape.line.width = Pt(w)

def bg(slide, color=BLACK):
    r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0,0, EMUW, EMUH)
    _solid(r, color); _noline(r)
    r._element.addprevious(r._element)  # keep at back
    return r

def tb(slide, x,y,w,h, lines, size=16, color=WHITE, bold=False, italic=False,
       align=PP_ALIGN.LEFT, font=FONT, anchor=MSO_ANCHOR.TOP, spacing=1.0):
    box = slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf = box.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
    tf.margin_left=Inches(0.05); tf.margin_right=Inches(0.05)
    tf.margin_top=Inches(0.02); tf.margin_bottom=Inches(0.02)
    if isinstance(lines,str): lines=[lines]
    for i,ln in enumerate(lines):
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; p.line_spacing=spacing
        if isinstance(ln,tuple):
            txt, kw = ln
        else:
            txt, kw = ln, {}
        r = p.add_run(); r.text=txt
        f=r.font; f.size=Pt(kw.get("size",size)); f.name=kw.get("font",font)
        f.bold=kw.get("bold",bold); f.italic=kw.get("italic",italic)
        f.color.rgb=kw.get("color",color)
    return box

def panel(slide, x,y,w,h, fill=PANEL, border=VIOLET, bw=1.0, radius=True):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                                 Inches(x),Inches(y),Inches(w),Inches(h))
    _solid(shp, fill); _line(shp, border, bw)
    shp.shadow.inherit=False
    return shp

def pill(slide, x,y, text, color):
    w = 0.14*len(text)+0.5
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x),Inches(y),Inches(w),Inches(0.42))
    _solid(shp, color); _noline(shp); shp.shadow.inherit=False
    tf=shp.text_frame; tf.word_wrap=False
    p=tf.paragraphs[0]; p.alignment=PP_ALIGN.CENTER
    r=p.add_run(); r.text=text; r.font.size=Pt(13); r.font.bold=True; r.font.name=FONT
    r.font.color.rgb = BLACK if color in (GOLD,GREEN) else WHITE
    return w

def accent_rule(slide, x,y,w,color=VIOLET,ht=0.06):
    r=slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x),Inches(y),Inches(w),Inches(ht))
    _solid(r,color); _noline(r); return r

def header(slide, eyebrow, title, tagright="TRINETRA · SANKAT MOCHAK"):
    tb(slide, 0.7,0.52,16,0.4,[(eyebrow,{"size":16,"color":GOLD,"bold":True})])
    tb(slide, 0.7,0.86,17.5,0.95,[(title,{"size":34,"color":WHITE,"bold":True})])
    accent_rule(slide, 0.72,1.82,3.2,VIOLET)
    tb(slide, 13.5,0.56,5.8,0.4,[(tagright,{"size":13,"color":MUTE,"bold":True})],align=PP_ALIGN.RIGHT)

def footer(slide, tag):
    tb(slide, 0.6,10.78,6,0.3,[("SANKAT MOCHAK",{"size":12,"color":MUTE,"bold":True})])
    tb(slide, 13.4,10.78,6,0.3,[(tag,{"size":12,"color":MUTE})],align=PP_ALIGN.RIGHT)

def new_slide(eyebrow,title,foot):
    s=prs.slides.add_slide(BLANK)
    bg(s); header(s,eyebrow,title); footer(s,foot)
    return s

def formula_card(slide, x,y,w,h, tag,tagcolor, name, layman, formula, src):
    panel(slide,x,y,w,h)
    pill(slide, x+0.25, y+0.22, tag, tagcolor)
    tb(slide, x+0.25, y+0.74, w-0.5, 0.5,[(name,{"size":18,"color":WHITE,"bold":True})])
    tb(slide, x+0.25, y+1.18, w-0.5, 0.55,[(layman,{"size":14,"color":GREY,"italic":True})],spacing=0.95)
    fy = y+1.72
    fb=panel(slide, x+0.25, fy, w-0.5, 0.62, fill=PANEL2, border=BLUE, bw=0.75)
    tbx=tb(slide, x+0.33, fy+0.04, w-0.66, 0.54,[(formula,{"size":15,"color":CREAM,"font":MONO,"bold":True})],
           anchor=MSO_ANCHOR.MIDDLE)
    tb(slide, x+0.25, fy+0.68, w-0.5, 0.4,[(src,{"size":11,"color":MUTE})],spacing=0.9)

# ---- legend used on formula slides
def legend(slide, y=1.95):
    x=0.72
    for t,c in [("A · ESTABLISHED",GREEN),("B · DERIVED",BLUE),("C · HYPOTHESIS (unvalidated)",GOLD)]:
        w=pill(slide,x,y,t,c); x+=w+0.3

# ================================================================= A1 DIVIDER
s=prs.slides.add_slide(BLANK); bg(s)
accent_rule(s, 0,5.1,20,VIOLET,0.09)
tb(s, 1,3.3,18,0.5,[("APPENDIX  ·  DEEP DIVE",{"size":20,"color":GOLD,"bold":True})])
tb(s, 1,3.95,18,1.4,[("The Science Behind the Three Eyes",{"size":52,"color":WHITE,"bold":True})])
tb(s, 1,5.4,18,1.2,[("Layman-friendly on top, full physics underneath — fire + mountain hazards, the fusion brain, "
                     "the architecture, the data, and our honesty rules.",{"size":20,"color":GREY})],spacing=1.05)
tb(s, 1,7.0,18,0.5,[("Every claim is tagged A (established) · B (derived) · C (hypothesis, not yet validated).",
                     {"size":16,"color":MUTE,"italic":True})])
footer(s,"Appendix A1")

# ================================================================= A2 FIRE / FOURTH EYE
s=new_slide("NEW CAPABILITY — not in the main deck","The Fourth Eye: Fire & Thermal Hazard","Appendix A2")
tb(s,0.72,2.05,18.5,0.7,[("In one line: the same three eyes that watch slopes can watch for fire — a camera sees "
   "flame/smoke, physics checks if it behaves like real fire, and only then it warns.",
   {"size":17,"color":GREY,"italic":True})],spacing=1.0)
cards=[("Camera eye","Edge AI on cheap CCTV/ESP32-CAM flags flame & smoke pixels (YOLO-tiny)."),
       ("Physics referee","Plume, flicker & smoke-optics checks reject steam, headlights, reflections."),
       ("IoT eye","Heat / gas / smoke on the same ₹2,000 node; multi-node agreement before alarm.")]
cx=0.72; cw=6.0
for i,(t,b) in enumerate(cards):
    x=cx+i*(cw+0.25); panel(s,x,2.95,cw,2.0)
    accent_rule(s,x+0.3,3.25,0.9,VIOLET)
    tb(s,x+0.3,3.45,cw-0.6,0.5,[(t,{"size":19,"color":WHITE,"bold":True})])
    tb(s,x+0.3,3.95,cw-0.6,0.9,[(b,{"size":14.5,"color":GREY})],spacing=0.98)
panel(s,0.72,5.2,18.52,2.1, fill=PANEL2, border=GOLD, bw=1.0)
tb(s,1.0,5.4,18,0.5,[("Why it is honest (Rule 19): fire output is ADVISORY — a human confirms; it never trips a public "
   "alarm by itself, and it fails safe to \u201cuncertain\u201d, never to a silent all-clear.",
   {"size":15.5,"color":CREAM})],spacing=1.0)
tb(s,1.0,6.25,18,1.0,[("Adds to the framework at zero extra sensors on the vision/IoT nodes already planned — fire is "
   "just \u201cone more sentence\u201d for the zero-shot eye plus a dedicated physics gate (next slides).",
   {"size":15.5,"color":GREY})],spacing=1.0)
tb(s,0.72,7.55,18.5,0.5,[("Source: P21 fire-physics deep dive — 56 papers, 20 established blocks (EF-01\u2026EF-20) + 7 novel "
   "candidates (ND-1\u2026ND-7). All source-reported; nothing measured by us yet.",{"size":12.5,"color":MUTE})])

# ================================================================= A3 FORMULA BANK I — MOUNTAIN
s=new_slide("PHYSICS FORMULA BANK I","Mountain Hazards — the equations behind the alarm","Appendix A3")
legend(s)
rows=[
 (0.72,2.55,"A",GREEN,"Slope stability (Factor of Safety)",
  "Is the slope still holding? FS<1 means it can slide.",
  "FS = (c\u2032 + (\u03C3\u2099\u2212u)\u00B7tan\u03C6\u2032) / (\u03B3\u00B7z\u00B7sin\u03B2\u00B7cos\u03B2)",
  "Infinite-slope / TRIGRS. Rain raises pore-pressure u \u2192 FS drops."),
 (6.98,2.55,"A",GREEN,"Rain-driven pore pressure (Iverson)",
  "How fast rain soaks in and weakens the slope.",
  "\u03C8(Z,t): slope enters ONLY via D\u2081 = D\u2080 / cos\u00B2\u03B2",
  "Iverson (2000) transient head; we fixed a double-count bug here."),
 (13.24,2.55,"A",GREEN,"Failure-time forecast (Fukuzono)",
  "When creep speeds up, 1/velocity falls to zero at collapse.",
  "1/v = A\u00B7(\u03B1\u22121)\u00B7(t_f \u2212 t),   \u03B1 \u2248 2",
  "Inverse-velocity method; straight line \u2192 read off t_f."),
 (0.72,5.95,"A",GREEN,"Rainfall trigger threshold (Caine)",
  "How much rain, how fast, before slides usually start.",
  "I = a\u00B7D^(\u2212b)      (intensity vs duration)",
  "Locally re-fitted, not a borrowed constant."),
 (6.98,5.95,"A",GREEN,"Flood runoff & routing",
  "How much rain becomes a flood wave, and how fast it travels.",
  "Q = (P\u22120.2S)\u00B2/(P+0.8S) ;  v = (1/n)\u00B7R^(2/3)\u00B7\u221AS",
  "SCS-CN runoff + Manning velocity (flash-flood / GLOF routing)."),
 (13.24,5.95,"A",GREEN,"When to actually alarm (Bayes)",
  "Balance missed disasters vs false alarms — pick the cost-optimal line.",
  "p* = C_FA / (C_FA + C_miss)   (\u2248 0.048)",
  "Cost-loss optimal threshold; same model sets the alarm point."),
]
for (x,y,tag,tc,name,lay,f,src) in rows:
    formula_card(s,x,y,6.0,3.2,tag,tc,name,lay,f,src)

# ================================================================= A4 FORMULA BANK II — FIRE
s=new_slide("PHYSICS FORMULA BANK II","Fire & Thermal — established blocks + our new candidates","Appendix A4")
legend(s)
rows=[
 (0.72,2.55,"A",GREEN,"Does the plume behave like fire? (Byram)",
  "Real fire plumes bend & rise in a specific way vs wind.",
  "N_c = buoyant power / flow power  (critical Froude)",
  "EF-13 Byram convective number \u2014 regime check."),
 (6.98,2.55,"A",GREEN,"Smoke dims the heat (Radiative transfer)",
  "Smoke blocks IR, so a pixel can look cooler than the real fire.",
  "dI/ds = \u2212(\u03BA+\u03C3)\u00B7I + j",
  "EF-14 RTE + EF-15 soot \u2014 feeds the smoke-temperature fix (C)."),
 (13.24,2.55,"A",GREEN,"Fire flickers at a known rate (Strouhal)",
  "Flames pulse ~1.5\u20135 Hz depending on size \u2014 a fingerprint.",
  "f_p \u2248 1.5\u00B7D^(\u22121/2)",
  "EF-16 puffing frequency \u2014 basis for the de-aliasing fix (C)."),
 (0.72,5.95,"C",GOLD,"See flicker on a cheap/slow camera (ND-1)",
  "Low-fps CCTV scrambles the flicker; we un-scramble it.",
  "match energy in the Strouhal-predicted aliased band",
  "ND-1 de-aliased flicker \u2014 novel hypothesis, UNVALIDATED."),
 (6.98,5.95,"C",GOLD,"True heat behind smoke (ND-2)",
  "Undo smoke dimming to recover the real plume temperature.",
  "L_obs = \u03C4_s\u00B7L_fire + (1\u2212\u03C4_s)\u00B7L_smoke  \u2192 solve T\u0302",
  "ND-2 \u2014 novel; uncertainty grows as smoke thickens (fail-safe)."),
 (13.24,5.95,"C",GOLD,"One early-warning number (ND-3)",
  "Blend heat-rise, gas-rise & radiation into a scene-proof score.",
  "\u03A0_ig = \u03A3 w\u1D62\u00B7(scale\u1D62)\u00B7(rate\u1D62)",
  "ND-3 dimensionless ignition index \u2014 novel hypothesis."),
]
for (x,y,tag,tc,name,lay,f,src) in rows:
    formula_card(s,x,y,6.0,3.2,tag,tc,name,lay,f,src)

# ================================================================= A5 FUSION BRAIN / PHARAOH
s=new_slide("THE FUSION BRAIN (P22)","How the three eyes become one careful decision","Appendix A5")
tb(s,0.72,2.05,18.5,0.7,[("In one line: a weighted referee that trusts each eye by how reliable and physically-"
   "consistent it is, and deliberately leans toward caution when a trustworthy eye raises alarm.",
   {"size":17,"color":GREY,"italic":True})],spacing=1.0)
# big PHARAOH card
panel(s,0.72,2.95,9.0,4.35, fill=PANEL2, border=GOLD, bw=1.25)
pill(s,1.0,3.2,"C · NOVEL OPERATOR (unvalidated)",GOLD)
tb(s,1.0,3.75,8.4,0.6,[("PHARAOH mean \u2014 adaptive-order fusion",{"size":22,"color":WHITE,"bold":True})])
fb=panel(s,1.0,4.45,8.4,0.95, fill=PANEL, border=BLUE, bw=0.8)
tb(s,1.1,4.5,8.2,0.85,[("F\u03C1(p;w) = ( \u03A3 w\u1D62\u00B7p\u1D62^\u03C1 )^(1/\u03C1)",{"size":22,"color":CREAM,"font":MONO,"bold":True})],
   anchor=MSO_ANCHOR.MIDDLE,align=PP_ALIGN.CENTER)
tb(s,1.0,5.5,8.4,0.5,[("order  \u03C1(t) = 1 + \u03BA\u00B7D\u00B7S   (D = disagreement, S = credible-alarm salience)",
   {"size":14.5,"color":GREY,"font":MONO})])
tb(s,1.0,6.05,8.4,1.1,[("Normal times \u2192 behaves like a careful average. When a reliable, physics-consistent eye "
   "shouts \u2018danger\u2019, \u03C1 rises so the mean bends toward it (anti-complacency). Fails open to \u2018uncertain\u2019.",
   {"size":14.5,"color":GREY})],spacing=0.98)
# supporting formulas column
sub=[("NF-1 \u00b7 Consistency c\u1D62","Agrees with physics? c\u1D62 = exp(\u2212((p\u1D62\u2212\u03C6)\u208A)\u00B2/2\u03C3\u00B2)"),
     ("NF-2 \u00b7 Reliability r\u1D62(t)","Track-record & drift down-weight a flaky sensor over time."),
     ("NF-3 \u00b7 Conflict \u2192 uncertainty","Eyes disagree? U* = \u03A3 w\u1D62u\u1D62 + \u03BB\u00B7D (don\u2019t fake confidence)."),
     ("NF-4 \u00b7 Salience S","S = max\u1D62 [ r\u1D62\u00B7c\u1D62\u00B7\u03C8(p\u1D62) ] \u2014 is any trustworthy alarm credible?")]
yy=2.95
for t,d in sub:
    panel(s,10.0,yy,9.24,0.98)
    tb(s,10.25,yy+0.12,8.8,0.4,[(t,{"size":16,"color":GOLD,"bold":True})])
    tb(s,10.25,yy+0.52,8.8,0.42,[(d,{"size":13.5,"color":GREY,"font":MONO})],spacing=0.9)
    yy+=1.08
tb(s,0.72,7.5,18.5,0.5,[("Effective weight  w\u0303\u1D62 = availability \u00b7 reliability r\u1D62 \u00b7 consistency c\u1D62 \u00b7 e^(\u2212u\u1D62/\u03C4).   "
   "Six fusion models (FM-1\u2026FM-6) derived; linear FM-1 is the safe fallback. Source: P22. Nothing measured.",
   {"size":12.5,"color":MUTE})])

# ================================================================= A6 ARCHITECTURE + TIERS
s=new_slide("SYSTEM ARCHITECTURE","Three compute tiers, nine workstreams, one decision","Appendix A6")
# tiers
tiers=[("TIER 0 \u00b7 NODE (\u2264\u20b92000)","ESP32 / ESP32-CAM. Tiny on-device checks: tilt Z-score, stage, on-node FS, "
        "flicker screen. Deep-sleep + solar. Raw video stays local.",VIOLET),
       ("TIER 1 \u00b7 GATEWAY","Edge SoC + LoRa concentrator. CCTV detector, anomaly, physics gate, local fusion + "
        "safety shield, siren drive. Works with the cloud OFFLINE.",BLUE),
       ("TIER 2 \u00b7 CLOUD / KAGGLE","Frozen EO foundation-model embeddings, training, hindcast & evaluation, model "
        "registry. Never on the life-safety critical path.",GREEN)]
yy=2.2
for t,d,c in tiers:
    panel(s,0.72,yy,11.3,1.55)
    accent_rule(s,0.72,yy,0.12,c,1.55)
    tb(s,1.0,yy+0.15,10.9,0.45,[(t,{"size":18,"color":WHITE,"bold":True})])
    tb(s,1.0,yy+0.62,10.9,0.85,[(d,{"size":14,"color":GREY})],spacing=0.95)
    yy+=1.72
# decision function box
panel(s,0.72,7.42,11.3,1.5, fill=PANEL2, border=GOLD, bw=1.0)
tb(s,1.0,7.55,10.9,0.4,[("THE SINGLE DECISION FUNCTION",{"size":14,"color":GOLD,"bold":True})])
tb(s,1.0,7.95,10.9,0.9,[("level = max( conformal_level(fused_risk, p*) ,  shield_floor )",
   {"size":17,"color":CREAM,"font":MONO,"bold":True})],anchor=MSO_ANCHOR.MIDDLE)
tb(s,1.0,8.5,10.9,0.4,[("The hard safety shield can only RAISE an alert, never lower it.",{"size":13,"color":GREY})])
# workstreams panel
panel(s,12.25,2.2,6.99,6.72)
tb(s,12.55,2.35,6.5,0.5,[("NINE WORKSTREAMS",{"size":16,"color":VIOLET,"bold":True})])
ws=["WS1a  Fire physics","WS1b  Geo physics","WS2   Deepfake / misinfo","WS3   Offline alerting",
    "WS4   CCTV perception","WS5   RL + meta-fusion","WS6   Robustness / calibration","WS7   IoT nodes",
    "WS8   Anomaly detection"]
tb(s,12.55,2.95,6.5,5.6,[(w,{"size":16,"color":GREY,"font":MONO}) for w in ws],spacing=1.35)

# ================================================================= A7 DATA + HONEST EVAL
s=new_slide("DATA BACKBONE & HONEST EVALUATION","Why the numbers will be believable","Appendix A7")
# left: data
panel(s,0.72,2.2,9.0,6.7)
tb(s,1.0,2.35,8.5,0.5,[("FREE DATA BACKBONE",{"size":18,"color":VIOLET,"bold":True})])
data=["Sentinel-1 InSAR (deformation) \u00b7 Sentinel-2 optical","GPM IMERG rain \u00b7 SMAP soil \u00b7 ERA5-Land",
      "MODIS / VIIRS active-fire \u00b7 ITS_LIVE glaciers","NASA FIRMS \u00b7 Earthdata \u00b7 Copernicus \u00b7 USGS",
      "52 catalogued free datasets (D113\u2013D164)","Fire/smoke, flood/SAR, landslide, InSAR,","seismic, air-quality, crisis, deepfake"]
tb(s,1.0,2.95,8.5,3.0,[(d,{"size":15.5,"color":GREY}) for d in data],spacing=1.25)
tb(s,1.0,6.2,8.5,2.5,[("Honest status: all datasets are candidates \u2014 links & licenses to be verified before use; "
   "India portals (Bhuvan, MOSDAC, VEDAS, NRSC, IMD, CWC, GSI) need manual checks. Free-only rule.",
   {"size":13.5,"color":MUTE})],spacing=1.0)
# right: eval gates
panel(s,9.97,2.2,9.27,6.7, fill=PANEL2, border=GOLD, bw=1.0)
tb(s,10.25,2.35,8.7,0.5,[("THE ADMISSION GATE (no number without it)",{"size":17,"color":GOLD,"bold":True})])
ev=["Spatial cross-validation (hold out whole map tiles)","Hold out monsoon YEARS (no time leakage)",
    "Beat mandatory baselines, or say \u2018does not beat\u2019","Report calibration + false-alarms-per-day + CIs",
    "Cost-loss Value Score as the primary metric","Hindcast: Kedarnath\u201913, Chamoli\u201921, Joshimath\u201922, S.Lhonak\u201923",
    "Class A / B / C labels on every physics block","Rule 19: advisory, human-in-the-loop, fail-safe"]
tb(s,10.25,2.95,8.7,5.0,[("\u2713  "+e,{"size":15.5,"color":GREY}) for e in ev],spacing=1.3)

# ================================================================= A8 NOVELTY / CLOSE
s=new_slide("WHAT IS NEW \u2014 AND WHY IT IS HONEST","Our contribution, stated carefully","Appendix A8")
panel(s,0.72,2.2,18.52,2.3, fill=PANEL2, border=VIOLET, bw=1.25)
tb(s,1.1,2.45,17.8,0.5,[("THE CONTRIBUTION",{"size":16,"color":GOLD,"bold":True})])
tb(s,1.1,2.95,17.8,1.4,[("In our review of 500+ papers, no single system combines offline-first alerting + cheap IoT "
   "ground truth + zero-shot & anomaly AI + a physics referee \u2014 across mountain hazards AND fire. "
   "That integration, done honestly, is our contribution.",{"size":19,"color":WHITE})],spacing=1.05)
cols=[("Novel, but labelled","PHARAOH operator, NF-1\u2026NF-4, ND-1\u2026ND-7 are Class-C hypotheses \u2014 UNVALIDATED. "
       "\u2018Novel\u2019 means \u2018not found in our limited search\u2019, not \u2018proven first\u2019.",GOLD),
      ("Safe by design","Advisory only; a human decides; the shield can only raise an alarm; the system abstains "
       "and escalates when unsure \u2014 it never guesses silently.",GREEN),
      ("Buildable & cheap","\u2264\u20b92,000 node, offline-first, runs within a 30 GPU-h/week student budget; "
       "foundation models are reused, not retrained.",BLUE)]
cw=6.0
for i,(t,d,c) in enumerate(cols):
    x=0.72+i*(cw+0.26); panel(s,x,4.75,cw,3.3)
    accent_rule(s,x+0.3,5.05,0.9,c)
    tb(s,x+0.3,5.25,cw-0.6,0.5,[(t,{"size":19,"color":WHITE,"bold":True})])
    tb(s,x+0.3,5.8,cw-0.6,2.0,[(d,{"size":15,"color":GREY})],spacing=1.0)
tb(s,0.72,8.35,18.5,0.6,[("Status: research stage \u2014 designed, sourced, build planned. We welcome questions, "
   "especially on the physics and the IoT node.  Dhanyavaad.",{"size":16,"color":CREAM,"italic":True})])

prs.save(OUT)
print("SAVED", OUT, "total slides:", len(prs.slides.__iter__.__self__._sldIdLst))
