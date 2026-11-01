#!/usr/bin/env python
"""render_video.py — TRINETRA/HIMKAVACH data-stack EXPLAINER video (frame renderer, Pillow only).

Goal: a clear, AOI-focused, research-grade explainer that builds the data stack ONE LAYER AT A TIME with
explicit labels, explains each dataset (what/where-from/provenance), shows the real physics FORMULAS with the
numbers computed by the real trinetra code, and keeps REAL vs SIMULATED tagged throughout.

Honesty: REAL imagery = NASA GIBS (open) + Esri (credited). Physics numbers come from public/data/l6_physics.json
(computed by the real trinetra numpy core). Dataset facts come verbatim from l8_datasets.json (parsed from
DATASETS.md). SIMULATED / ILLUSTRATIVE things are labelled; nothing unmeasured is shown as measured.

Usage:
    python render_video.py sample     # a few QA frames -> frames_sample/
    python render_video.py full       # all frames      -> frames/
Then encode with ffmpeg (see encode step / HOW_TO_REPRODUCE).
"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(WS, "viz", "render", "public", "data")
ASSETS = os.path.join(HERE, "assets")

W, H = 1920, 1080
FPS = 20

# ---- palette (DESIGN_SPEC) ----
BG=(5,7,10); PANEL=(14,20,27); PANEL2=(22,31,41); HAIR=(42,55,68)
INK=(230,237,243); INK2=(159,176,191); INK3=(100,116,139)
REAL=(56,211,159); SIM=(242,177,65); ILLUS=(139,157,201); FOCUS=(76,166,255); WARN=(229,72,77)

FONTS={}
def font(kind,size):
    key=(kind,size)
    if key in FONTS: return FONTS[key]
    paths={"sans":"segoeui.ttf","bold":"segoeuib.ttf","semi":"seguisb.ttf","light":"segoeuisl.ttf",
           "mono":"consola.ttf","monob":"consolab.ttf"}
    FONTS[key]=ImageFont.truetype(os.path.join("C:\\Windows\\Fonts", paths[kind]), size)
    return FONTS[key]

def lerp(a,b,t): return a+(b-a)*t
def ease(t): return t*t*(3-2*t)  # smoothstep
def ease_out(t): return 1-(1-t)**3
def clamp(t,a=0.0,b=1.0): return max(a,min(b,t))
def mix(c1,c2,t): return tuple(int(round(lerp(c1[i],c2[i],t))) for i in range(3))

# ---- colormaps (match colormaps.js) ----
def _cmap(stops):
    def f(t):
        t=clamp(t)
        for i in range(1,len(stops)):
            if t<=stops[i][0]:
                a,b=stops[i-1],stops[i]; f2=(t-a[0])/((b[0]-a[0]) or 1)
                return tuple(int(round(a[j+1]+f2*(b[j+1]-a[j+1]))) for j in range(3))
        return tuple(stops[-1][1:4])
    return f
INFERNO=_cmap([[0,0,0,4],[0.2,40,11,84],[0.4,101,21,110],[0.6,159,42,99],[0.75,212,72,66],[0.88,245,125,21],[0.96,250,193,39],[1,252,255,164]])
VIRIDIS=_cmap([[0,68,1,84],[0.25,59,82,139],[0.5,33,145,140],[0.75,94,201,98],[1,253,231,37]])
CIVIDIS=_cmap([[0,0,32,76],[0.25,0,67,118],[0.5,87,118,141],[0.75,165,161,128],[1,255,234,70]])

# ---- text helpers ----
def text(d,xy,s,fnt,fill,anchor="la",spacing=4):
    d.text(xy,s,font=fnt,fill=fill,anchor=anchor,spacing=spacing)
def wrap(s,fnt,maxw):
    words=s.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if fnt.getlength(t)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
def para(d,xy,s,fnt,fill,maxw,lh):
    x,y=xy
    for ln in wrap(s,fnt,maxw):
        d.text((x,y),ln,font=fnt,fill=fill); y+=lh
    return y

def rrect(d,box,r,fill=None,outline=None,width=1):
    d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)

def chip(d,xy,label,color,fnt=None):
    fnt=fnt or font("bold",20)
    pad=10; tw=fnt.getlength(label); x,y=xy
    rrect(d,[x,y,x+tw+pad*2,y+34],8,fill=tuple(list(color)+[0]) if False else _dim(color,0.22),outline=color,width=2)
    text(d,(x+pad,y+6),label,fnt,color)
    return x+tw+pad*2
def _dim(c,f): return tuple(int(c[i]*f) for i in range(3))

def kind_color(k):
    return REAL if k.startswith("REAL") else (SIM if k=="SIMULATED" else ILLUS)
def kind_short(k):
    return "REAL" if k.startswith("REAL") else ("SIMULATED" if k=="SIMULATED" else "ILLUSTRATIVE")

# ---- load data ----
def load(name):
    with open(os.path.join(DATA,name),encoding="utf-8") as f: return json.load(f)
PHYS=load("l6_physics.json"); DSETS=load("l8_datasets.json"); DFD=load("l12_dfd.json")

# ---- layer registry (mirrors config.js provenance + explanation) ----
LAYERS=[
 dict(id="L0",name="Earth / AOI context",kind="REAL",color=(95,176,217),asset="aoi_truecolor.png",
   prov=dict(source="NASA GIBS (VIIRS true color)",product="VIIRS_SNPP CorrectedReflectance",date="2021-05-01",res="~250 m",license="NASA open data"),
   why="Start from the real place: a true-colour satellite view of the Uttarakhand study area."),
 dict(id="L1",name="Terrain & relief (DEM)",kind="REAL",color=(155,140,112),asset="aoi_relief.png",
   prov=dict(source="Copernicus DEM GLO-30 (relief: Esri World Hillshade)",product="COP-DEM_GLO-30",date="2021",res="30 m",license="Copernicus free/open · relief © Esri"),
   why="Elevation + slope. Steep Himalayan ground is what drives both fire spread and landslides."),
 dict(id="L2",name="Land cover / fuel",kind="REAL",color=(111,158,90),asset=None,
   prov=dict(source="ESA WorldCover",product="WorldCover 10 m v200",date="2021",res="10 m",license="CC-BY-4.0"),
   why="Forest vs grass vs built classes — i.e. what can actually burn, and where."),
 dict(id="L3",name="Built environment & exposure",kind="REAL",color=(195,163,217),asset=None,
   prov=dict(source="OpenStreetMap + WorldPop",product="buildings/roads + population grid",date="2020/2021",res="vector / ~100 m",license="ODbL / CC-BY"),
   why="Who and what is exposed: settlements, roads, population. Sparse in the rural Himalaya — shown as-is."),
 dict(id="L4",name="Atmosphere — wind field",kind="REAL",color=(127,199,192),asset=None,pending=True,
   prov=dict(source="ERA5-Land (Copernicus C3S)",product="reanalysis-era5-land",date="2021",res="~9 km hourly",license="CC-BY (DOI 10.24381/cds.e2161bac)"),
   why="Wind steers fire spread and tilts the plume. Needs a free CDS extract → shown as DATA-PENDING."),
 dict(id="L5",name="Real fire observations",kind="REAL",color=(240,101,67),asset=None,pending=True,
   prov=dict(source="NASA FIRMS (VIIRS/MODIS)",product="active-fire archive",date="2021",res="375 m / 1 km",license="NASA open (credit requested)"),
   why="Actual satellite-detected hotspots. Needs a free FIRMS MAP_KEY → shown as DATA-PENDING."),
 dict(id="L6",name="WS1 physics + fusion",kind="SIMULATED",color=(242,177,65),asset=None,special="physics",
   prov=dict(source="TRINETRA numpy core",product="Heskestad / Iverson / FS / Caine / Byram",date="computed",res="scenario",license="n/a (our code)"),
   why="Our physics models, RUN on the real code. Simulated fields — explicit parameters, not a measurement."),
 dict(id="L7",name="WS4 CCTV fire/smoke",kind="ILLUSTRATIVE",color=(217,195,95),asset=None,
   prov=dict(source="project WS4",product="camera FOV + sample",date="n/a",res="n/a",license="no faces / no PII"),
   why="Ground cameras watch for fire/smoke. FOV is illustrative; detection is SIMULATED (no trained detector)."),
 dict(id="L8",name="Dataset registry",kind="REAL",color=(95,176,217),asset=None,special="datasets",
   prov=dict(source="DATASETS.md",product="26 quick-link datasets",date="2026-10",res="n/a",license="per dataset (tags kept)"),
   why="Every dataset we actually catalogued — counts and licenses copied verbatim, candidates marked honestly."),
 dict(id="L9",name="WS2 deepfake verification",kind="ILLUSTRATIVE",color=(176,111,217),asset=None,
   prov=dict(source="project WS2",product="verification data-flow",date="n/a",res="n/a",license="stats only, no media"),
   why="Social-media posts are checked for authenticity. Score is SIMULATED and hard-capped at 0.40 reliability."),
 dict(id="L10",name="WS3 tiered alerting",kind="ILLUSTRATIVE",color=(226,87,76),asset=None,
   prov=dict(source="project WS3 + WorldPop",product="tier reach geometry",date="n/a",res="scenario",license="ranges source-reported"),
   why="Siren → mesh → cell-broadcast tiers. Reach is scenario geometry; a public alert is always human-gated."),
 dict(id="L11",name="WS5 advisory routing",kind="SIMULATED",color=(95,217,176),asset=None,
   prov=dict(source="OSM roads + WS5 rule baseline",product="advisory routes",date="n/a",res="road graph",license="ODbL (roads)"),
   why="Evacuation ADVICE over the real road graph. Rule-baseline only — no trained RL policy exists, by design."),
 dict(id="L12",name="Fusion & decision (DFD)",kind="ILLUSTRATIVE",color=(95,176,217),asset=None,special="dfd",
   prov=dict(source="02_system_architecture + _CANON",product="high-level data flow",date="n/a",res="n/a",license="n/a"),
   why="How it all fuses into one human-gated advisory. Advisory, human-in-the-loop — never autonomous."),
]

AOI=dict(name="Uttarakhand Himalaya — 2021 pre-monsoon forest-fire season",bbox="78.5, 29.5, 80.2, 30.8 (lon/lat)",window="2021-04-25 → 2021-05-12")
ATTRIB="NASA GIBS/VIIRS (open) · © Esri, Maxar, Earthstar Geographics · Copernicus Sentinel/DEM/ERA5 · ESA WorldCover · © OpenStreetMap (ODbL) · WorldPop · CesiumJS"

# ---- isometric stack geometry ----
SX_A=(180,560); SX_B=(760,470); SX_C=(980,650)
SX_D=(SX_A[0]+(SX_C[0]-SX_B[0]), SX_A[1]+(SX_C[1]-SX_B[1]))  # parallelogram 4th corner
GAP=36; THK=20
def find_coeffs(dst,src):
    m=[]
    for (x,y),(u,v) in zip(dst,src):
        m.append([x,y,1,0,0,0,-u*x,-u*y]); m.append([0,0,0,x,y,1,-v*x,-v*y])
    A=np.array(m,dtype=float); B=np.array(src,dtype=float).reshape(8)
    return np.linalg.solve(A,B)

def make_plane_tile(layer):
    """Pre-warp a 600x600 content square onto the base parallelogram -> cropped RGBA tile + origin."""
    cs=600
    if layer.get("asset"):
        src=Image.open(os.path.join(ASSETS,layer["asset"])).convert("RGB").resize((cs,cs))
    else:
        # procedural plate in the layer colour, subtle vertical gradient + hairline grid
        src=Image.new("RGB",(cs,cs),_dim(layer["color"],0.5))
        dd=ImageDraw.Draw(src)
        for yy in range(cs):
            f=0.35+0.4*(yy/cs); dd.line([(0,yy),(cs,yy)],fill=mix((8,10,14),layer["color"],f))
        for gx in range(0,cs,60): dd.line([(gx,0),(gx,cs)],fill=_dim(layer["color"],0.7))
        for gy in range(0,cs,60): dd.line([(0,gy),(cs,gy)],fill=_dim(layer["color"],0.7))
    src=src.convert("RGBA")
    dst=[SX_A,SX_B,SX_C,SX_D]
    co=find_coeffs(dst,[(0,0),(cs,0),(cs,cs),(0,cs)])
    warped=src.transform((W,H),Image.PERSPECTIVE,co,Image.BICUBIC)
    bbox=warped.getbbox()
    tile=warped.crop(bbox)
    return tile,(bbox[0],bbox[1])

PLANE_CACHE={}
def plane_of(layer):
    if layer["id"] not in PLANE_CACHE: PLANE_CACHE[layer["id"]]=make_plane_tile(layer)
    return PLANE_CACHE[layer["id"]]

def quad_shift(dy):
    return [(SX_A[0],SX_A[1]+dy),(SX_B[0],SX_B[1]+dy),(SX_C[0],SX_C[1]+dy),(SX_D[0],SX_D[1]+dy)]

def draw_slab(base,layer,i,anim_dy=0.0,alpha=1.0,emph=False):
    """Composite one layer's slab (side faces + top tile) onto base at its stacked offset."""
    dy=-(i*GAP)+anim_dy
    A=(SX_A[0],SX_A[1]+dy); B=(SX_B[0],SX_B[1]+dy); C=(SX_C[0],SX_C[1]+dy); D=(SX_D[0],SX_D[1]+dy)
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    col=layer["color"]
    # right + front side faces (extruded down by THK)
    od.polygon([B,C,(C[0],C[1]+THK),(B[0],B[1]+THK)],fill=tuple(list(_dim(col,0.45))+[int(255*alpha)]))
    od.polygon([D,C,(C[0],C[1]+THK),(D[0],D[1]+THK)],fill=tuple(list(_dim(col,0.30))+[int(255*alpha)]))
    base.alpha_composite(ov)
    tile,origin=plane_of(layer)
    t2=tile
    if alpha<1.0:
        a=t2.split()[3].point(lambda p:int(p*alpha)); t2=t2.copy(); t2.putalpha(a)
    base.alpha_composite(t2,(origin[0],int(origin[1]+dy)))
    # outline on top face
    ov2=Image.new("RGBA",(W,H),(0,0,0,0)); od2=ImageDraw.Draw(ov2)
    oc=tuple(list(FOCUS if emph else _dim(col,0.9))+[int(255*alpha)])
    od2.line([A,B,C,D,A],fill=oc,width=3 if emph else 1)
    base.alpha_composite(ov2)
    return (A,B,C,D)

# ---- persistent frame furniture ----
def base_frame(progress,timecode,caption=None,cap_kind=None):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im,"RGBA")
    # top bar
    d.rectangle([0,0,W,72],fill=PANEL)
    d.line([(0,72),(W,72)],fill=HAIR)
    text(d,(40,20),"TRINETRA / HIMKAVACH",font("bold",28),INK)
    text(d,(395,27),"multi-hazard advisory early-warning — data stack, explained layer by layer",font("sans",18),INK2)
    # legend (top-right)
    lx=W-430
    for lab,c in [("REAL",REAL),("SIMULATED",SIM),("ILLUSTRATIVE",ILLUS)]:
        d.ellipse([lx,30,lx+14,44],fill=c); text(d,(lx+20,27),lab,font("semi",15),c); lx+=10+font("semi",15).getlength(lab)+34
    # footer
    d.line([(0,H-78),(W,H-78)],fill=HAIR)
    if caption:
        cc=kind_color(cap_kind) if cap_kind else INK2
        d.ellipse([40,H-66,54,H-52],fill=cc)
        text(d,(66,H-70),caption,font("sans",17),INK2)
    text(d,(40,H-34),ATTRIB,font("sans",12),INK3)
    text(d,(W-150,H-34),timecode,font("mono",14),INK3)
    # progress bar
    d.rectangle([0,H-4,int(W*progress),H],fill=FOCUS)
    return im,d

# ---- detail panel (right side) ----
PX=1040; PW=1860-1040
def detail_panel(d,layer,compact=False):
    x=PX; y=120
    rrect(d,[x,y,1860,980],14,fill=(14,20,27,235),outline=HAIR,width=1)
    x+=34; y+=30
    text(d,(x,y),layer["id"],font("monob",40),kind_color(layer["kind"]))
    chip(d,(x+140,y+6),kind_short(layer["kind"]),kind_color(layer["kind"]),font("bold",19))
    y+=66
    text(d,(x,y),layer["name"],font("semi",34),INK); y+=60
    d.line([(x,y),(1826,y)],fill=HAIR,width=1); y+=24
    text(d,(x,y),"WHAT THIS LAYER ADDS",font("bold",16),INK3); y+=30
    y=para(d,(x,y),layer["why"],font("sans",22),INK,PW-70,32)+16
    if compact:
        p=layer["prov"]
        text(d,(x,y),"SOURCE",font("mono",15),INK3)
        y=para(d,(x+120,y),f"{p['source']}  ·  {p['license']}",font("sans",20),INK2,PW-200,26)+12
        return y
    text(d,(x,y),"DATASET / PROVENANCE",font("bold",16),INK3); y+=32
    p=layer["prov"]
    for k,v in [("source",p["source"]),("product",p["product"]),("date",p["date"]),("resolution",p["res"]),("license",p["license"])]:
        text(d,(x,y),k.upper(),font("mono",15),INK3)
        lns=wrap(v,font("sans",20),PW-230)
        for j,ln in enumerate(lns): text(d,(x+150,y+j*26),ln,font("sans",20),INK)
        y+=max(30,26*len(lns))+6
    return y

# ---- special panels ----
def mini_plot(d,box,xs,series,xlabel,ylabel,cmap=None,hline=None,title=""):
    x0,y0,x1,y1=box
    rrect(d,box,8,fill=(10,14,20,255),outline=HAIR,width=1)
    text(d,(x0+10,y0+6),title,font("semi",17),INK2)
    px0,py0,px1,py1=x0+56,y0+36,x1-16,y1-34
    d.line([(px0,py0),(px0,py1)],fill=HAIR); d.line([(px0,py1),(px1,py1)],fill=HAIR)
    allv=[v for _,ys in series for v in ys]
    lo,hi=min(allv),max(allv); hi=hi if hi>lo else lo+1
    xmin,xmax=min(xs),max(xs)
    def sx(x): return px0+(x-xmin)/(xmax-xmin)*(px1-px0)
    def sy(v): return py1-(v-lo)/(hi-lo)*(py1-py0)
    if hline is not None and lo<=hline<=hi:
        d.line([(px0,sy(hline)),(px1,sy(hline))],fill=WARN,width=2)
        text(d,(px1-78,sy(hline)-20),f"{ylabel}={hline}",font("mono",13),WARN)
    for color,ys in series:
        pts=[(sx(xs[i]),sy(ys[i])) for i in range(len(xs))]
        d.line(pts,fill=color,width=3)
    text(d,(px0,py1+8),f"{xmin:g}",font("mono",13),INK3); text(d,(px1-20,py1+8),f"{xmax:g}",font("mono",13),INK3)
    text(d,(x0+8,py0-2),f"{hi:.1f}",font("mono",13),INK3); text(d,(x0+8,py1-14),f"{lo:.1f}",font("mono",13),INK3)
    text(d,((px0+px1)//2-30,py1+8),xlabel,font("sans",14),INK2)

def panel_physics(d,y0):
    x=PX+34; y=y0+6
    text(d,(x,y),"PHYSICS — real equations, run on our code",font("bold",17),SIM); y+=32
    fp=PHYS["fire_plume"]; sc=fp["scalars"]; ls=PHYS["landslide"]
    eqs=[
      ("Heskestad plume",  "ΔT(z) ∝ Q_c^2/3 · (z−z0)^-5/3", f"flame L = {sc['flame_height_m']} m"),
      ("Puffing (Strouhal)","f ≈ 1.5 / √D",                   f"f = {sc['puffing_frequency_Hz']} Hz"),
      ("Byram number",      "N_c = 2g·Q_c /(ρ·cp·T·U³·L)",    f"N_c = {sc['byram_convection_number']} ({sc['regime']})"),
      ("Factor of Safety",  "FS=(c'+(γz cos²β−u_w)tanφ')/(γz sinβ cosβ)", "FS<1 ⇒ unstable"),
      ("Caine I–D",         "I = a·D^-b  (a,b: local calib.)", f"I/I_thr = {ls['caine']['I_over_Ithreshold']} → exceeded={ls['caine']['threshold_exceeded']}"),
    ]
    for name,formula,val in eqs:
        text(d,(x,y),name,font("semi",18),INK)
        text(d,(x+215,y+1),formula,font("mono",15),INK2)
        text(d,(x+215,y+23),val,font("monob",16),SIM); y+=50
    y+=6
    prof=fp["profile"]
    mini_plot(d,[x,y,x+360,y+170],prof["z"],[(tuple(INFERNO(0.8)),prof["T"])],"height z (m)","T",title="plume temperature  (inferno)")
    fs=ls["fs_vs_slope"]
    mini_plot(d,[x+400,y,x+770,y+170],fs["beta_deg"],[(tuple(VIRIDIS(0.7)),fs["FS_wet"]),(tuple(VIRIDIS(0.2)),fs["FS_dry"])],"slope β (°)","FS",hline=1.0,title="Factor of Safety vs slope  (viridis)")

def panel_datasets(d,y0,reveal=1.0):
    x=PX+34; y=y0+6
    c=DSETS["counts"]
    text(d,(x,y),f"REGISTRY — {c['total_in_quick_links']} datasets (verbatim from DATASETS.md)",font("bold",17),(95,176,217)); y+=30
    bs=c["by_status"]; bv=c["by_verification"]
    text(d,(x,y),f"selected {bs.get('selected',0)}  ·  candidate {bs.get('candidate',0)}  ·  "
                 f"[V] {bv.get('[V]',0)}  [V*] {bv.get('[V*]',0)}  [D] {bv.get('[D]',0)}",font("mono",15),INK2); y+=32
    allds=[dd for g in DSETS["groups"] for dd in g["datasets"]]
    n=min(len(allds),max(1,int(len(allds)*reveal)))
    cols=6; cw=(1826-x-8)//cols; ch=50
    for i,dsd in enumerate(allds[:n]):
        cx=x+(i%cols)*cw; cy=y+(i//cols)*ch
        sel=dsd["status"]=="selected"; col=REAL if sel else ILLUS
        rrect(d,[cx,cy,cx+cw-8,cy+ch-8],6,fill=_dim(col,0.22),outline=col,width=1)
        text(d,(cx+8,cy+4),dsd["id"],font("monob",17),col)
        text(d,(cx+8,cy+25),dsd["ws"][:10],font("mono",12),INK3)

def panel_dfd(d,y0):
    groups=["sensing","perception","physics","fusion","decision","action"]
    x0,x1=PX+34,1826; y0b=y0+16; y1=y0+300
    colx={g:x0+i*((x1-x0)/(len(groups)-1)) for i,g in enumerate(groups)}
    perg={}; idx={}
    for nd in DFD["nodes"]: perg[nd["group"]]=perg.get(nd["group"],0)+1
    pos={}
    for nd in DFD["nodes"]:
        idx[nd["group"]]=idx.get(nd["group"],0)
        cnt=perg[nd["group"]]; yy=y0b+(y1-y0b)/(cnt+1)*(idx[nd["group"]]+1); pos[nd["id"]]=(colx[nd["group"]],yy); idx[nd["group"]]+=1
    for e in DFD["edges"]:
        a=pos[e["from"]]; b=pos[e["to"]]; d.line([a,b],fill=tuple(list(FOCUS)+[150]),width=2)
    for nd in DFD["nodes"]:
        px,py=pos[nd["id"]]; col=REAL if nd["kind"]=="REAL" else SIM
        rrect(d,[px-68,py-20,px+68,py+20],7,fill=(14,20,27,255),outline=col,width=2)
        for j,ln in enumerate(wrap(nd["label"],font("sans",13),128)[:2]):
            text(d,(px,py-9+j*15),ln,font("sans",13),INK,anchor="ma")
    text(d,(x0,y1+26),"level = max( conformal_level(fused_risk, p*),  shield_floor ),   p* ≈ 0.0476",font("monob",18),FOCUS)
    text(d,(x0,y1+56),"advisory · human-in-the-loop · never autonomous",font("semi",18),INK2)

# =====================  SCENES  =====================
def sc_intro(t,T):
    im,d=base_frame(0.0,fmt_tc(t),)
    a=ease(clamp(t/1.5))
    cx=W//2
    text(d,(cx,300),"TRINETRA / HIMKAVACH",font("bold",72),mix(BG,INK,a),anchor="ma")
    text(d,(cx,400),"a multi-hazard early-warning data stack — explained one real layer at a time",font("light",30),mix(BG,INK2,ease(clamp((t-0.6)/1.5))),anchor="ma")
    if t>1.6:
        b=ease(clamp((t-1.6)/1.5))
        for i,(lab,c) in enumerate([("REAL data, labelled",REAL),("SIMULATED physics (our code)",SIM),("ILLUSTRATIVE flow",ILLUS)]):
            yy=520+i*52
            d.ellipse([cx-250,yy+4,cx-234,yy+20],fill=mix(BG,c,b)); text(d,(cx-220,yy),lab,font("semi",26),mix(BG,c,b))
    if t>3.2:
        text(d,(cx,760),AOI["name"],font("semi",26),mix(BG,FOCUS,ease(clamp((t-3.2)/1.5))),anchor="ma")
    return im

def sc_aoi(t,T):
    im,d=base_frame(0.02,fmt_tc(t),"REAL: NASA GIBS true colour (open) + © Esri imagery · WGS-84","REAL")
    z=1.0+0.05*ease(clamp(t/T))
    hero=Image.open(os.path.join(ASSETS,"aoi_esri.png")).convert("RGB")
    hw=int(760*z); hh=int(hero.height*hw/hero.width)
    hero=hero.resize((hw,hh))
    hx,hy=150,170
    im.paste(hero,(hx,hy))
    d=ImageDraw.Draw(im,"RGBA")
    d.rectangle([hx,hy,hx+hw,hy+hh],outline=HAIR,width=2)
    x=980
    text(d,(x,220),"STUDY AREA",font("bold",20),INK3)
    y=para(d,(x,258),AOI["name"],font("semi",40),INK,840,50)+14
    for k,v in [("bounding box",AOI["bbox"]),("event window",AOI["window"]),
                ("why here","steep relief + dense 2021 fire activity + open EO coverage")]:
        text(d,(x,y),k.upper(),font("mono",15),INK3); y=para(d,(x+10,y+22),v,font("sans",24),INK,840,32)+16
    text(d,(x,y+10),"We now rebuild this scene as a stack of real data layers →",font("semi",24),FOCUS)
    return im

def sc_stack_intro(t,T):
    im,d=base_frame(0.05,fmt_tc(t),"Each slab = one data layer. Green = REAL · amber = SIMULATED/ILLUSTRATIVE.")
    base=im.convert("RGBA")
    k=min(len(LAYERS),1+int(ease(clamp(t/ (T*0.8)))*3))
    for i in range(k): draw_slab(base,LAYERS[i],i,alpha=0.9,emph=(i==k-1))
    im=base.convert("RGB"); d=ImageDraw.Draw(im,"RGBA")
    x=1040
    text(d,(x,300),"The TRINETRA data stack",font("semi",40),INK)
    para(d,(x,380),"Thirteen layers, L0 → L12. We add them one at a time, each with its own source, resolution and license — and a tag that never hides what is real and what is modelled.",font("sans",24),INK2,780,34)
    return im

def sc_layer(layer,i,t,T):
    prog=0.08+0.9*((i+1)/len(LAYERS))
    cap=f"{layer['id']} · {layer['prov']['source']}"
    im,d=base_frame(prog,fmt_tc(t),cap,layer["kind"])
    base=im.convert("RGBA")
    anim=clamp(t/0.9)
    for j in range(i+1):
        if j<i:
            draw_slab(base,LAYERS[j],j,alpha=0.42,emph=False)
        else:
            dy=(1-ease_out(anim))*(-260)   # slide down from above
            al=0.35+0.65*ease_out(anim)
            draw_slab(base,LAYERS[j],j,anim_dy=dy,alpha=al,emph=True)
    im=base.convert("RGB"); d=ImageDraw.Draw(im,"RGBA")
    special=layer.get("special")
    yend=detail_panel(d,layer,compact=bool(special))
    if layer.get("pending"):
        yb=yend+8
        rrect(d,[PX+34,yb,1826,yb+104],10,fill=_dim(WARN,0.2),outline=WARN,width=2)
        text(d,(PX+54,yb+16),"DATA-PENDING",font("bold",22),WARN)
        para(d,(PX+54,yb+50),"Needs a free account/key — until a real extract exists we render NOTHING here (never fabricated).",font("sans",18),INK2,1740,24)
    if special=="physics": panel_physics(d,yend)
    elif special=="datasets": panel_datasets(d,yend,reveal=clamp((t-0.8)/max(0.1,(T-1.2))))
    elif special=="dfd": panel_dfd(d,yend)
    return im

def sc_outro(t,T):
    im,d=base_frame(1.0,fmt_tc(t),"Advisory · human-in-the-loop · never autonomous.")
    base=im.convert("RGBA")
    for j in range(len(LAYERS)): draw_slab(base,LAYERS[j],j,alpha=0.9,emph=False)
    im=base.convert("RGB"); d=ImageDraw.Draw(im,"RGBA")
    a=ease(clamp(t/1.5))
    x=1040
    text(d,(x,230),"The full stack",font("semi",44),mix(BG,INK,a))
    para(d,(x,310),"Real satellite imagery, terrain, land cover and exposure; real fire + weather observations; our physics models run on real code; the dataset registry; verification, alerting and routing — fused into one human-gated advisory.",font("sans",23),mix(BG,INK2,a),780,33)
    if t>2.4:
        b=ease(clamp((t-2.4)/1.5))
        for k,row in enumerate(["REAL — shown green, with source + license","SIMULATED — shown amber, parameters on screen","Nothing unmeasured is ever shown as measured"]):
            text(d,(x,620+k*46),"• "+row,font("semi",23),mix(BG,[REAL,SIM,FOCUS][k],b))
    if t>4.2:
        text(d,(x,820),"TRINETRA / HIMKAVACH",font("bold",34),mix(BG,FOCUS,ease(clamp((t-4.2)/1.5))))
    return im

CUR_T=0.0
def fmt_tc(t=None):
    return f"{int(CUR_T//60):02d}:{int(CUR_T%60):02d}"

# =====================  TIMELINE  =====================
def build_timeline():
    tl=[("intro",sc_intro,10),("aoi",sc_aoi,16),("stackintro",sc_stack_intro,9)]
    durs={"L6":44,"L8":34,"L12":34}
    for i,L in enumerate(LAYERS):
        tl.append((L["id"],(lambda i: (lambda t,T: sc_layer(LAYERS[i],i,t,T)))(i),durs.get(L["id"],18)))
    tl.append(("outro",sc_outro,16))
    return tl

def main():
    global CUR_T
    mode=sys.argv[1] if len(sys.argv)>1 else "sample"
    tl=build_timeline()
    total=sum(s[2] for s in tl)
    outdir=os.path.join(HERE,"frames" if mode=="full" else "frames_sample")
    os.makedirs(outdir,exist_ok=True)
    for f in os.listdir(outdir):
        if f.endswith(".jpg") or f.endswith(".png"): os.remove(os.path.join(outdir,f))
    print(f"timeline total={total}s ({total/60:.2f} min), fps={FPS}, mode={mode}")
    fidx=0; elapsed=0.0
    for name,fn,dur in tl:
        nframes=int(dur*FPS)
        picks=[int(nframes*0.5)] if mode=="sample" else range(nframes)
        for k in picks:
            lt=k/FPS
            CUR_T=elapsed+lt
            img=fn(lt,dur)
            if mode=="full":
                img.save(os.path.join(outdir,f"f_{fidx:06d}.jpg"),quality=92)
            else:
                img.save(os.path.join(outdir,f"s_{name}.jpg"),quality=92)
            fidx+=1
        elapsed+=dur
        if mode=="full": print(f"  scene {name}: {nframes} frames (total {fidx})")
    print(f"done. frames={fidx} -> {outdir}")
    with open(os.path.join(HERE,"timeline.json"),"w") as f:
        json.dump(dict(total_s=total,fps=FPS,frames=fidx,scenes=[(n,dd) for n,_,dd in tl]),f,indent=2)

if __name__=="__main__":
    main()
