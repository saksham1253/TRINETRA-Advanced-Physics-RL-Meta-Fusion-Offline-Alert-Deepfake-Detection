#!/usr/bin/env python
"""render_3d.py (v2 ULTRA) — cinematic 3D explainer with supersampled world pass.

World (terrain + sheets + plume + rings + routes) renders at SS× then downscales (anti-aliasing);
2D overlays (labels, panels, HUD, typography) draw crisp at 1080p on top.
"""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine3d as E
import render_video as RV

W,H=1920,1080
SS=1.0; RW,RH=int(W*SS),int(H*SS)
FPS=18; FOV=40
HERE=os.path.dirname(os.path.abspath(__file__))

BG=RV.BG; PANEL=RV.PANEL; HAIR=RV.HAIR; INK=RV.INK; INK2=RV.INK2; INK3=RV.INK3
REAL=RV.REAL; SIM=RV.SIM; ILLUS=RV.ILLUS; FOCUS=RV.FOCUS; WARN=RV.WARN
LAYERS=RV.LAYERS; PHYS=RV.PHYS; DSETS=RV.DSETS; DFD=RV.DFD
font=RV.font

def ease(t): return t*t*(3-2*t)
def eout(t): return 1-(1-t)**3
def ein(t): return t*t
def clamp(t,a=0.0,b=1.0): return max(a,min(b,t))
def lerp(a,b,t): return a+(b-a)*t
def mix(c1,c2,t): return tuple(int(round(lerp(c1[i],c2[i],t))) for i in range(3))

TERR=E.Terrain(geom_w=150)
ARZ=TERR.ar
CUR_T=0.0; TOTAL=1.0

def tc(): return f"{int(CUR_T//60):02d}:{int(CUR_T%60):02d}"

# soft radial sprite for volumetric plume / glow
def _soft(n=160):
    y,x=np.ogrid[-1:1:n*1j,-1:1:n*1j]; r=np.sqrt(x*x+y*y)
    a=np.clip(1-r,0,1)**1.7
    return (a*255).astype(np.uint8)
SOFT=_soft()

def cams(az,elev,dist,target):
    c2=E.Camera(RW,RH,FOV); c2.orbit(az,elev,dist,target)
    c1=E.Camera(W,H,FOV); c1.orbit(az,elev,dist,target)
    return c2,c1

# ---------------- world pass (SS) ----------------
def sheet_corners(alt):
    x=0.40; y=0.40*ARZ; return np.array([[-x,-y,alt],[x,-y,alt],[x,y,alt],[-x,y,alt]])
SHEET_BASE=0.30; SHEET_GAP=0.050
def sheet_alt(k): return SHEET_BASE+k*SHEET_GAP

def _draw_sheet(fill_d,glow_d,cam,k,layer,alpha,emph):
    alt=sheet_alt(k); col=layer["color"]; corners=sheet_corners(alt)
    pr=cam.project(corners)
    if (pr[:,2]<=0.02).any(): return
    pts=[(pr[i,0],pr[i,1]) for i in range(4)]
    a=int(255*alpha)
    fill_d.polygon(pts,fill=(col[0],col[1],col[2],int(a*0.42)))
    G=7
    for gi in range(1,G):
        f=gi/G
        p1=corners[0]+(corners[1]-corners[0])*f; p2=corners[3]+(corners[2]-corners[3])*f
        q1=corners[0]+(corners[3]-corners[0])*f; q2=corners[1]+(corners[2]-corners[1])*f
        s=cam.project(np.array([p1,p2,q1,q2]))
        fill_d.line([(s[0,0],s[0,1]),(s[1,0],s[1,1])],fill=(col[0],col[1],col[2],int(a*0.3)),width=max(1,int(SS)))
        fill_d.line([(s[2,0],s[2,1]),(s[3,0],s[3,1])],fill=(col[0],col[1],col[2],int(a*0.3)),width=max(1,int(SS)))
    ec=FOCUS if emph else col; w=int(5*SS) if emph else int(2.5*SS)
    fill_d.line(pts+[pts[0]],fill=(ec[0],ec[1],ec[2],255),width=w)
    glow_d.line(pts+[pts[0]],fill=(ec[0],ec[1],ec[2],200),width=int(6*SS))

def _plume(im,cam,intensity,ct):
    if intensity<=0: return
    base=np.array([EPI[0],EPI[1],E.terrain_z_at(TERR,*EPI)])
    wind=np.array([0.6,0.36]); wind/=np.linalg.norm(wind)
    Htop=0.34*intensity; nseg=46
    layer=Image.new("RGBA",(RW,RH),(0,0,0,0))
    glow=Image.new("RGBA",(RW,RH),(0,0,0,0))
    for i in range(nseg-1,-1,-1):
        f=i/nseg; h=f*Htop; tilt=(f**1.4)*0.30
        jx=0.016*math.sin(2*math.pi*0.4743*ct+i*0.7)*f; jy=0.016*math.cos(2*math.pi*0.4743*ct*0.8+i*0.6)*f
        pos=np.array([base[0]+wind[0]*tilt+jx, base[1]+wind[1]*tilt+jy, base[2]+h])
        s=cam.project(np.array([pos]))[0]
        if s[2]<=0.05: continue
        rad=lerp(0.02,0.14,f)*intensity; sr=max(3,int(cam.f*rad/s[2]))
        if f<0.14:
            c=mix((255,150,40),(255,220,120),f/0.14); al=int(240*intensity)
            # fire glow (additive)
            gsz=int(sr*2.2); gs=Image.fromarray(SOFT).resize((gsz,gsz)).convert("L")
            gtile=Image.new("RGBA",(gsz,gsz),(255,140,40,0)); gtile.putalpha(gs.point(lambda v:int(v*0.5)))
            glow.alpha_composite(gtile,(int(s[0]-gsz/2),int(s[1]-gsz/2)))
        else:
            g=(f-0.14)/0.86; c=mix((120,112,112),(60,64,74),g); al=int(lerp(210,30,g)*intensity)
        sz=int(sr*2); sp=Image.fromarray(SOFT).resize((sz,sz)).convert("L")
        tile=Image.new("RGBA",(sz,sz),(c[0],c[1],c[2],0)); tile.putalpha(sp.point(lambda v:int(v*al/255)))
        layer.alpha_composite(tile,(int(s[0]-sz/2),int(s[1]-sz/2)))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10*SS)))
    im.alpha_composite(layer)

def _ring(od,cam,cx,cy,r,color,alpha,n=64):
    pts=[]
    for i in range(n+1):
        a=2*math.pi*i/n; x=cx+r*math.cos(a); y=cy+r*math.sin(a)*0.95
        s=cam.project(np.array([[x,y,E.terrain_z_at(TERR,x,y)+0.004]]))[0]
        if s[2]>0.05: pts.append((s[0],s[1]))
    if len(pts)>2: od.line(pts,fill=(color[0],color[1],color[2],alpha),width=max(2,int(3*SS)))

def _route(od,cam,prog,color,wps):
    pts3=[(x,y,E.terrain_z_at(TERR,x,y)+0.006) for (x,y) in wps]
    full=[]
    for a,b in zip(pts3[:-1],pts3[1:]):
        for s in np.linspace(0,1,12): full.append(tuple(a[k]+(b[k]-a[k])*s for k in range(3)))
    n=max(2,int(len(full)*prog)); sp=cam.project(np.array(full[:n]))
    pts=[(sp[i,0],sp[i,1]) for i in range(len(sp)) if sp[i,2]>0.05]
    if len(pts)>2:
        od.line(pts,fill=(color[0],color[1],color[2],235),width=max(3,int(4*SS)))
        # dashed centre + arrowheads cheaply
        for i in range(0,len(pts)-2,8): od.ellipse([pts[i][0]-3,pts[i][1]-3,pts[i][0]+3,pts[i][1]+3],fill=(255,255,255,220))

EPI=(-0.06,0.07)
def render_world(c2, st, ct, dim=0.95):
    im=E.sky(RW,RH,c2).convert("RGBA")
    E.render_terrain(im,c2,TERR,dim=dim)
    if any(st.get(k) for k in ("scar","lake","flood","rings","route")):
        fx=Image.new("RGBA",(RW,RH),(0,0,0,0)); fd=ImageDraw.Draw(fx)
        if st.get("scar"): _scar(fd,c2,st["scar"])
        if st.get("lake"): _lake(fd,c2,*st["lake"])
        if st.get("flood"): _flood(fd,c2,st["flood"][0],st["flood"][1])
        for (cx,cy,r,col,al) in st.get("rings",[]): _ring(fd,c2,cx,cy,r,col,al)
        if st.get("route"): _route(fd,c2,st["route"][0],st["route"][1],st["route"][2])
        im.alpha_composite(fx)
    sheets=st.get("sheets")
    if sheets:
        fillov=Image.new("RGBA",(RW,RH),(0,0,0,0)); glow=Image.new("RGBA",(RW,RH),(0,0,0,0))
        fd=ImageDraw.Draw(fillov); gd=ImageDraw.Draw(glow)
        for (k,layer,alpha,emph) in sheets: _draw_sheet(fd,gd,c2,k,layer,alpha,emph)
        im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(max(2,int(4*SS))))); im.alpha_composite(fillov)
    if st.get("plume"): _plume(im,c2,st["plume"],ct)
    small=im if RW==W else im.resize((W,H),Image.LANCZOS)
    if st.get("rain"): _rain(small,st["rain"],ct)
    return small

def _lake(od,cam,cx,cy,r,alpha):
    n=36; verts=[]
    for i in range(n):
        a=2*math.pi*i/n; x=cx+r*math.cos(a); y=cy+r*0.72*math.sin(a); verts.append((x,y,E.terrain_z_at(TERR,x,y)+0.004))
    s=cam.project(np.array(verts))
    if (s[:,2]<=0.05).any(): return
    pts=[(s[i,0],s[i,1]) for i in range(n)]
    od.polygon(pts,fill=(70,150,205,int(205*alpha)),outline=(150,210,240,255))
    hp=cam.project(np.array([[cx-r*0.3,cy+r*0.2,E.terrain_z_at(TERR,cx,cy)+0.005]]))[0]
    rr=max(6,r*cam.f/hp[2]*0.4)
    od.ellipse([hp[0]-rr,hp[1]-6,hp[0]+rr,hp[1]+6],fill=(200,235,250,int(120*alpha)))

def _flood(od,cam,prog,wps):
    pts3=[(x,y,E.terrain_z_at(TERR,x,y)+0.006) for (x,y) in wps]
    full=[]
    for a,b in zip(pts3[:-1],pts3[1:]):
        for s in np.linspace(0,1,16,endpoint=False): full.append(tuple(a[k]+(b[k]-a[k])*s for k in range(3)))
    full.append(pts3[-1])
    n=max(2,int(len(full)*clamp(prog))); seg=full[:n]
    if len(seg)<2: return
    sp=cam.project(np.array(seg))
    for i in range(len(seg)-1):
        if sp[i,2]<=0.05 or sp[i+1,2]<=0.05: continue
        f=i/len(full); w=max(3,int((6+30*f)*SS*clamp(0.4+0.6*prog)))
        od.line([(sp[i,0],sp[i,1]),(sp[i+1,0],sp[i+1,1])],fill=(70,140,205,195),width=w)
        od.line([(sp[i,0],sp[i,1]),(sp[i+1,0],sp[i+1,1])],fill=(150,205,240,120),width=max(1,w//3))
    le=sp[n-1]
    if le[2]>0.05:
        for rr,al in [(26*SS,70),(16*SS,120),(9*SS,200)]:
            od.ellipse([le[0]-rr,le[1]-rr,le[0]+rr,le[1]+rr],fill=(160,215,245,al))

def _scar(od,cam,amt):
    cx,cy=0.03,-0.03; verts=[]
    for (dx,dy) in [(-0.04,0.02),(0.03,0.0),(0.06,-0.06),(0.01,-0.11),(-0.05,-0.05)]:
        x=cx+dx; y=cy+dy; verts.append((x,y,E.terrain_z_at(TERR,x,y)+0.003))
    s=cam.project(np.array(verts))
    if (s[:,2]>0.05).all():
        od.polygon([(s[i,0],s[i,1]) for i in range(len(verts))],fill=(120,78,46,int(185*amt)),outline=(150,96,56,255))

def _rain(im,amt,ct):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    rng=np.random.RandomState(int(ct*7)%997)
    for _ in range(int(300*amt)):
        x=rng.randint(0,W); y=rng.randint(60,H-60); od.line([(x,y),(x-6,y+18)],fill=(170,195,230,110),width=1)
    im.alpha_composite(ov)

# ---------------- 2D overlays (1x) ----------------
def hud(d, caption=None, cap_kind=None, progress=0.0):
    d.rectangle([0,0,W,66],fill=(6,9,13,205))
    RV.text(d,(34,16),"TRINETRA / HIMKAVACH",font("bold",28),INK)
    RV.text(d,(400,25),"3D data-stack & disaster cascade",font("sans",17),INK2)
    lx=W-430
    for lab,c in [("REAL",REAL),("SIMULATED",SIM),("ILLUSTRATIVE",ILLUS)]:
        d.ellipse([lx,27,lx+13,40,],fill=c); RV.text(d,(lx+19,24),lab,font("semi",15),c)
        lx+=19+int(font("semi",15).getlength(lab))+24
    d.rectangle([0,H-62,W,H],fill=(6,9,13,180)); d.line([(0,H-62),(W,H-62)],fill=HAIR)
    if caption:
        cc=RV.kind_color(cap_kind) if cap_kind else INK2
        d.ellipse([34,H-47,47,H-34],fill=cc); RV.text(d,(56,H-50),caption,font("sans",17),INK2)
    RV.text(d,(34,H-26),"NASA GIBS/VIIRS · AWS Terrain Tiles (SRTM/ETOPO) · © Esri World Imagery · Copernicus · ESA WorldCover · OSM/WorldPop",font("sans",12),INK3)
    RV.text(d,(W-130,H-27),tc(),font("mono",15),INK3)
    d.rectangle([0,H-4,int(W*progress),H],fill=FOCUS)

def billboard(d, cam, P, lines, color, sub=None):
    s=cam.project(np.array([P]))[0]
    if s[2]<=0.05: return
    x,y=int(s[0]),int(s[1])
    tw=max(font("semi",19).getlength(l) for l in lines)
    bw=int(tw)+30; bh=22+26*len(lines)+(18 if sub else 0)
    bx,by=min(max(x+16,8),W-bw-8),min(max(y-bh-12,70),H-bh-66)
    d.line([(x,y),(bx+12,by+bh)],fill=color,width=2); d.ellipse([x-6,y-6,x+6,y+6],fill=color,outline=INK)
    RV.rrect(d,[bx,by,bx+bw,by+bh],9,fill=(10,14,20,236),outline=color,width=2)
    yy=by+10
    for i,l in enumerate(lines):
        RV.text(d,(bx+15,yy),l,font("semi" if i==0 else "sans",19 if i==0 else 16),color if i==0 else INK); yy+=26
    if sub: RV.text(d,(bx+15,yy),sub,font("mono",13),INK3)

def side_rail(d, active_k):
    x0=W-290; y0=84
    RV.rrect(d,[x0,y0,W-24,y0+13*32+18],11,fill=(10,14,20,205),outline=HAIR,width=1)
    for k,L in enumerate(LAYERS):
        yy=y0+13+k*32; on=k<=active_k; cur=k==active_k
        c=RV.kind_color(L["kind"]) if on else INK3
        d.ellipse([x0+16,yy+4,x0+30,yy+18],fill=c if on else (28,38,50),outline=c,width=1)
        RV.text(d,(x0+42,yy),f"{L['id']}",font("monob",17),c if on else INK3)
        RV.text(d,(x0+88,yy+1),L["name"][:21],font("semi" if cur else "sans",15),(INK if cur else (INK2 if on else INK3)))
        if cur: d.rectangle([x0+5,yy,x0+9,yy+24],fill=FOCUS)

def info_panel(d, layer):
    x0,y0=34,82; x1=x0+520
    RV.rrect(d,[x0,y0,x1,y0+330],13,fill=(10,14,20,228),outline=HAIR,width=1)
    RV.text(d,(x0+24,y0+20),layer["id"],font("monob",38),RV.kind_color(layer["kind"]))
    RV.chip(d,(x0+120,y0+26),RV.kind_short(layer["kind"]),RV.kind_color(layer["kind"]),font("bold",18))
    RV.text(d,(x0+24,y0+74),layer["name"],font("semi",27),INK)
    yy=RV.para(d,(x0+24,y0+116),layer["why"],font("sans",19),INK2,x1-x0-48,27)+10
    p=layer["prov"]
    for k,v in [("source",p["source"]),("product",p["product"]),("res",p["res"]),("licence",p["license"])]:
        RV.text(d,(x0+24,yy),k.upper(),font("mono",13),INK3)
        ls=RV.wrap(v,font("sans",17),x1-x0-130)
        for j,ln in enumerate(ls): RV.text(d,(x0+120,yy+j*22),ln,font("sans",17),INK)
        yy+=max(24,22*len(ls))+3
    if layer.get("pending"):
        RV.rrect(d,[x0+24,yy+2,x1-24,yy+58],9,fill=RV._dim(WARN,0.2),outline=WARN,width=2)
        RV.text(d,(x0+36,yy+14),"DATA-PENDING — needs free key; nothing fabricated",font("bold",16),WARN)

# ---- bottom strips for special layers ----
def _strip(d,title,color):
    x0,y0,x1,y1=W-900,H-370,W-34,H-80
    RV.rrect(d,[x0,y0,x1,y1],13,fill=(10,14,20,234),outline=HAIR,width=1)
    RV.text(d,(x0+24,y0+14),title,font("bold",19),color)
    return x0+24,y0+50,x1-24,y1-16

def panel_physics(d):
    x,y,x1,y1=_strip(d,"PHYSICS — real equations, computed on our code",SIM)
    sc=PHYS["fire_plume"]["scalars"]; ls=PHYS["landslide"]
    rows=[("Heskestad flame","ΔT∝Q_c^2/3·(z−z0)^-5/3",f"L={sc['flame_height_m']} m"),
          ("Puffing (Strouhal)","f≈1.5/√D",f"{sc['puffing_frequency_Hz']} Hz"),
          ("Byram number","N_c=2gQ_c/(ρcpTU³L)",f"{sc['byram_convection_number']} · {sc['regime']}"),
          ("Factor of Safety","FS=(c'+(γz cos²β−u_w)tanφ')/(γz sinβcosβ)","FS<1 unstable"),
          ("Caine I–D","I=a·D^-b",f"I/I_thr={ls['caine']['I_over_Ithreshold']}")]
    yy=y
    for n,f_,v in rows:
        RV.text(d,(x,yy),n,font("semi",18),INK); RV.text(d,(x+210,yy+2),f_,font("mono",15),INK2); RV.text(d,(x+590,yy),v,font("monob",16),SIM); yy+=36
    fs=ls["fs_vs_slope"]; px0,py0,px1,py1=x1-300,y,x1,y1
    RV.rrect(d,[px0,py0,px1,py1],7,fill=(8,11,16,255),outline=HAIR,width=1)
    beta=fs["beta_deg"]; FSd=fs["FS_dry"]; FSw=fs["FS_wet"]; lo,hi=min(FSw+FSd),max(FSw+FSd)
    def sx(i): return px0+12+i/(len(beta)-1)*(px1-px0-24)
    def sy(v): return py1-12-(v-lo)/(hi-lo)*(py1-py0-30)
    d.line([(px0+12,sy(1.0)),(px1-12,sy(1.0))],fill=WARN,width=1)
    d.line([(sx(i),sy(FSw[i])) for i in range(len(beta))],fill=tuple(RV.VIRIDIS(0.7)),width=3)
    d.line([(sx(i),sy(FSd[i])) for i in range(len(beta))],fill=tuple(RV.VIRIDIS(0.25)),width=3)
    RV.text(d,(px0+12,py0+6),"FS vs slope β",font("mono",12),INK3)

def panel_datasets(d,reveal=1.0):
    x,y,x1,y1=_strip(d,f"REGISTRY — {DSETS['counts']['total_in_quick_links']} datasets (verbatim from DATASETS.md)",REAL)
    c=DSETS["counts"]; bs=c["by_status"]; bv=c["by_verification"]
    RV.text(d,(x,y),f"selected {bs.get('selected',0)} · candidate {bs.get('candidate',0)} · [V]{bv.get('[V]',0)} [V*]{bv.get('[V*]',0)} [D]{bv.get('[D]',0)}",font("mono",16),INK2)
    allds=[dd for g in DSETS["groups"] for dd in g["datasets"]]; n=min(len(allds),max(1,int(len(allds)*reveal)))
    cols=7; cw=(x1-x)//cols; ch=46
    for i,dsd in enumerate(allds[:n]):
        cx=x+(i%cols)*cw; cy=y+32+(i//cols)*ch; sel=dsd["status"]=="selected"; col=REAL if sel else ILLUS
        RV.rrect(d,[cx,cy,cx+cw-8,cy+ch-8],5,fill=RV._dim(col,0.22),outline=col,width=1)
        RV.text(d,(cx+8,cy+4),dsd["id"],font("monob",16),col); RV.text(d,(cx+8,cy+24),dsd["ws"][:10],font("mono",11),INK3)

def panel_dfd_mini(d):
    x,y,x1,y1=_strip(d,"FUSION & DECISION — advisory, human-in-the-loop",FOCUS)
    groups=["sensing","perception","physics","fusion","decision","action"]
    colx={g:x+gi*((x1-x)/(len(groups)-1)) for gi,g in enumerate(groups)}
    per={}; idx={}
    for nd in DFD["nodes"]: per[nd["group"]]=per.get(nd["group"],0)+1
    pos={}
    for nd in DFD["nodes"]:
        idx[nd["group"]]=idx.get(nd["group"],0); cnt=per[nd["group"]]
        yy=y+12+(y1-y-30)/(cnt+1)*(idx[nd["group"]]+1); pos[nd["id"]]=(colx[nd["group"]],yy); idx[nd["group"]]+=1
    for e in DFD["edges"]: d.line([pos[e["from"]],pos[e["to"]]],fill=(*FOCUS,120),width=2)
    for nd in DFD["nodes"]:
        px,py=pos[nd["id"]]; col=REAL if nd["kind"]=="REAL" else SIM
        RV.rrect(d,[px-58,py-16,px+58,py+16],6,fill=(14,20,27,255),outline=col,width=2)
        for j,ln in enumerate(RV.wrap(nd["label"],font("sans",12),108)[:2]): RV.text(d,(px,py-10+j*13),ln,font("sans",12),INK,anchor="ma")
    RV.text(d,(x,y1-4),"level = max(conformal_level(fused_risk, p*), shield_floor),  p*≈0.0476",font("monob",15),FOCUS)

# ---------------- scenes ----------------
def sc_intro(t,dur):
    c2,c1=cams(lerp(8,34,t/dur),lerp(30,25,ease(clamp(t/dur))),2.0,[0,0,TERR.zmid])
    im=render_world(c2,{},CUR_T,dim=0.82)
    d=ImageDraw.Draw(im,"RGBA"); d.rectangle([0,0,W,H],fill=(5,7,10,90)); cx=W//2
    a=ease(clamp(t/1.4))
    RV.text(d,(cx,300),"TRINETRA / HIMKAVACH",font("bold",76),mix(BG,INK,a),anchor="ma")
    RV.text(d,(cx,398),"the data stack & a disaster — in 3D",font("light",33),mix(BG,INK2,ease(clamp((t-0.5)/1.4))),anchor="ma")
    if t>1.4:
        b=ease(clamp((t-1.4)/1.4))
        for i,(lab,c) in enumerate([("REAL data — source + licence shown",REAL),("SIMULATED physics — our code, parameters shown",SIM),("ILLUSTRATIVE flow — geometry, no trained model",ILLUS)]):
            yy=500+i*52; d.ellipse([cx-360,yy+6,cx-344,yy+22],fill=mix(BG,c,b)); RV.text(d,(cx-326,yy),lab,font("semi",25),mix(BG,c,b))
    if t>3.0: RV.text(d,(cx,760),RV.AOI["name"],font("semi",25),mix(BG,FOCUS,ease(clamp((t-3.0)/1.4))),anchor="ma")
    hud(d,progress=CUR_T/TOTAL); return im.convert("RGB")

def sc_reveal(t,dur):
    f=eout(clamp(t/(dur*0.45))); dist=lerp(3.4,1.95,f); elev=lerp(58,24,f); az=lerp(0,58,ease(clamp(t/dur)))
    c2,c1=cams(az,elev,dist,[0,0,lerp(TERR.zmax*0.6,TERR.zmid,f)])
    im=render_world(c2,{},CUR_T,dim=1.0); d=ImageDraw.Draw(im,"RGBA")
    if t>dur*0.5:
        gi,gj=np.unravel_index(np.argmax(TERR.V[:,:,2]),TERR.V[:,:,2].shape); peak=TERR.V[gi,gj]
        billboard(d,c1,peak+np.array([0,0,0.02]),["Highest point in view",f"~{int(TERR.meta['elev_max'])} m"],REAL)
    if t>dur*0.2:
        a=ease(clamp((t-dur*0.2)/1.2))
        RV.rrect(d,[34,84,520,296],13,fill=(10,14,20,int(220*a)),outline=HAIR,width=1)
        RV.text(d,(56,102),"STUDY AREA — REAL TERRAIN",font("bold",19),REAL)
        RV.para(d,(56,136),RV.AOI["name"],font("semi",27),INK,470,33)
        RV.text(d,(56,220),f"relief  {int(TERR.meta['elev_min'])} – {int(TERR.meta['elev_max'])} m",font("mono",18),INK2)
        RV.text(d,(56,250),f"~{TERR.meta['span_x_m']/1000:.0f} × {TERR.meta['span_y_m']/1000:.0f} km · DEM draped with satellite imagery",font("sans",16),INK2)
    hud(d,caption="REAL: AWS Terrain Tiles DEM + © Esri World Imagery, 3D with baked sun-shadows",cap_kind="REAL",progress=CUR_T/TOTAL)
    return im.convert("RGB")

def make_layer_scene(k):
    layer=LAYERS[k]
    if layer.get("special")=="datasets":
        return lambda t,dur: sc_datasets_detail(t,dur,k)
    def fn(t,dur):
        topz=sheet_alt(k); az=lerp(52+k*5,52+k*5+30,ease(clamp(t/dur)))
        tz=topz*0.5; dist=1.75+0.95*clamp((topz-SHEET_BASE)/(12*SHEET_GAP))
        c2,c1=cams(az,24,dist,[0,0,tz])
        a=eout(clamp(t/1.2))
        sheets=[(j,LAYERS[j],0.30,False) for j in range(k)]+[(k,layer,0.3+0.4*a,True)]
        im=render_world(c2,{"sheets":sheets},CUR_T,dim=0.9); d=ImageDraw.Draw(im,"RGBA")
        c=sheet_corners(sheet_alt(k)).mean(axis=0)
        billboard(d,c1,c,[f"{layer['id']}  {layer['name']}"],RV.kind_color(layer["kind"]),sub=layer["prov"]["source"])
        info_panel(d,layer); side_rail(d,k)
        sp=layer.get("special")
        if sp=="physics": panel_physics(d)
        elif sp=="dfd": panel_dfd_mini(d)
        hud(d,caption=f"{layer['id']} · {layer['prov']['source']}",cap_kind=layer["kind"],progress=CUR_T/TOTAL)
        return im.convert("RGB")
    return fn

def sc_datasets_detail(t,dur,k):
    layer=LAYERS[k]
    c2,c1=cams(lerp(60,86,ease(clamp(t/dur))),30,3.0,[0,0,TERR.zmid])
    im=render_world(c2,{},CUR_T,dim=0.5); d=ImageDraw.Draw(im,"RGBA")
    d.rectangle([0,0,W,H],fill=(5,7,11,200))
    cnt=DSETS["counts"]; bs=cnt["by_status"]; bv=cnt["by_verification"]
    RV.text(d,(50,86),"L8 · THE REAL DATA THAT WOULD FEED TRINETRA",font("bold",34),REAL)
    RV.text(d,(50,132),"Parsed verbatim from DATASETS.md — counts, licences, status copied exactly. Nothing was downloaded or trained.",font("sans",19),INK2)
    # count chips
    chips=[(f"{cnt['total_in_quick_links']} datasets",INK),(f"{bs['selected']} selected",REAL),(f"{bs['candidate']} candidate",ILLUS),
           (f"[V] {bv['[V]']} verified",REAL),(f"[V*] {bv['[V*]']} 1-fact-unverified",SIM),(f"[D] {bv['[D]']} discovery-only",ILLUS)]
    cxp=50
    for lab,c in chips:
        w=int(font("bold",18).getlength(lab))+34; RV.rrect(d,[cxp,166,cxp+w,204],9,fill=RV._dim(c,0.22),outline=c,width=2)
        RV.text(d,(cxp+17,174),lab,font("bold",18),c); cxp+=w+14
    # table
    allds=[(g["workstream"],dd) for g in DSETS["groups"] for dd in g["datasets"]]
    n=min(len(allds),int(len(allds)*clamp((t-0.8)/max(0.1,dur*0.6))+0.999))
    y0=238; rh=30
    RV.text(d,(60,y0),"ID",font("mono",14),INK3); RV.text(d,(140,y0),"DATASET",font("mono",14),INK3)
    RV.text(d,(760,y0),"WS",font("mono",14),INK3); RV.text(d,(880,y0),"LICENCE",font("mono",14),INK3)
    RV.text(d,(1360,y0),"SIZE / ACCESS",font("mono",14),INK3); RV.text(d,(1820,y0),"V",font("mono",14),INK3)
    d.line([(50,y0+22),(W-40,y0+22)],fill=HAIR)
    prev_ws=None
    for i in range(n):
        ws_group,dd=allds[i]; yy=y0+30+i*rh
        sel=dd["status"]=="selected"; col=REAL if sel else ILLUS
        d.ellipse([54,yy+6,66,yy+18],fill=col)
        RV.text(d,(78,yy),dd["id"],font("monob",16),col)
        RV.text(d,(140,yy),dd["name"][:52],font("semi",16),INK)
        RV.text(d,(760,yy),dd["ws"][:12],font("mono",14),INK2)
        RV.text(d,(880,yy),dd["license"][:40],font("sans",14),INK2)
        RV.text(d,(1360,yy),dd["size_n"][:40],font("sans",13),INK3)
        vc={"[V]":REAL,"[V*]":SIM,"[D]":ILLUS}.get(dd["ver"],INK3)
        RV.text(d,(1810,yy),dd["ver"],font("monob",15),vc)
    side_rail(d,k)
    hud(d,caption="REAL metadata (registry) · ILLUSTRATIVE panel geometry · no data downloaded",cap_kind="REAL",progress=CUR_T/TOTAL)
    return im.convert("RGB")

def sc_stack_overview(t,dur):
    az=lerp(40,130,ease(clamp(t/dur))); el=lerp(26,20,ease(clamp(t/dur)))
    c2,c1=cams(az,el,2.95,[0,0,sheet_alt(6)*0.6])
    sheets=[(j,LAYERS[j],0.34,False) for j in range(len(LAYERS))]
    im=render_world(c2,{"sheets":sheets},CUR_T,dim=0.86); d=ImageDraw.Draw(im,"RGBA")
    a=ease(clamp(t/1.4))
    RV.text(d,(60,96),"13 LAYERS · ONE STACK",font("bold",40),mix(BG,INK,a))
    RV.text(d,(60,150),"REAL ground + imagery · SIMULATED physics · ILLUSTRATIVE flow",font("semi",21),mix(BG,INK2,a))
    # legend (all 13), left
    y0=210
    for kk,L in enumerate(LAYERS):
        b=ease(clamp((t-0.6-kk*0.12)/1.0)); yy=y0+kk*44; c=RV.kind_color(L["kind"])
        d.ellipse([62,yy+6,80,yy+24],fill=mix(BG,c,b),outline=c,width=1)
        RV.text(d,(92,yy),f"{L['id']}",font("monob",19),mix(BG,c,b))
        RV.text(d,(150,yy+2),L["name"],font("semi",19),mix(BG,INK,b))
    hud(d,caption="all layers framed together — real depth, one orbiting camera",cap_kind="REAL",progress=CUR_T/TOTAL)
    return im.convert("RGB")

def sc_outro(t,dur):
    az=lerp(90,150,ease(clamp(t/dur))); el=lerp(22,32,ease(clamp(t/dur))); dist=lerp(2.6,3.1,ease(clamp(t/dur)))
    c2,c1=cams(az,el,dist,[0,0,0.6])
    sheets=[(j,LAYERS[j],0.28,False) for j in range(len(LAYERS))]
    im=render_world(c2,{"sheets":sheets},CUR_T,dim=0.9); d=ImageDraw.Draw(im,"RGBA")
    d.rectangle([0,0,W,H],fill=(5,7,10,90)); a=ease(clamp(t/1.5)); cx=W//2
    RV.text(d,(cx,250),"one stack · one decision · human-gated",font("semi",46),mix(BG,INK,a),anchor="ma")
    if t>1.6:
        b=ease(clamp((t-1.6)/1.5))
        for i,row in enumerate(["REAL terrain, imagery, datasets — sourced & licensed","SIMULATED physics — real equations, parameters on screen","ADVISORY only — a human approves every public alert"]):
            RV.text(d,(cx,360+i*52),row,font("semi",25),mix(BG,[REAL,SIM,FOCUS][i],b),anchor="ma")
    if t>3.6: RV.text(d,(cx,640),"TRINETRA / HIMKAVACH",font("bold",40),mix(BG,FOCUS,ease(clamp((t-3.6)/1.5))),anchor="ma")
    hud(d,progress=CUR_T/TOTAL); return im.convert("RGB")

try:
    import cascade3d; CASCADE=cascade3d.scenes(globals())
except Exception as _e:
    import traceback; traceback.print_exc(); CASCADE=[]; print("cascade not ready:",_e)

def build_timeline():
    tl=[("intro",sc_intro,10),("reveal",sc_reveal,26)]
    durs={"L6":24,"L8":30,"L12":24}
    for k,L in enumerate(LAYERS): tl.append((L["id"],make_layer_scene(k),durs.get(L["id"],13)))
    tl.append(("stack",sc_stack_overview,18))
    tl+=CASCADE; tl.append(("outro",sc_outro,18)); return tl

def main():
    global CUR_T,TOTAL
    mode=sys.argv[1] if len(sys.argv)>1 else "sample"
    resume=(len(sys.argv)>2 and sys.argv[2]=="resume")
    tl=build_timeline(); TOTAL=sum(s[2] for s in tl)
    outdir=os.path.join(HERE,"frames3d" if mode=="full" else "frames3d_sample"); os.makedirs(outdir,exist_ok=True)
    if not resume:
        for f in os.listdir(outdir):
            if f.endswith(".jpg"): os.remove(os.path.join(outdir,f))
    print(f"total {TOTAL}s ({TOTAL/60:.2f} min) fps={FPS} frames~{TOTAL*FPS:.0f} SS={SS} {RW}x{RH}->{W}x{H} mode={mode} resume={resume}")
    import time; fidx=0; elapsed=0.0
    for name,fn,dur in tl:
        nf=int(dur*FPS); picks=[int(nf*0.5)] if mode=="sample" else range(nf); t0=time.time()
        for kk in picks:
            fp=os.path.join(outdir,f"f_{fidx:06d}.jpg")
            if mode=="full" and resume and os.path.exists(fp) and os.path.getsize(fp)>8000:
                fidx+=1; continue
            lt=kk/FPS; CUR_T=elapsed+lt; img=fn(lt,dur)
            if mode=="full": img.save(fp,quality=92)
            else: img.save(os.path.join(outdir,f"s_{name}.jpg"),quality=92)
            fidx+=1
        elapsed+=dur
        if mode=="full": print(f"  {name}: {nf}f (tot {fidx})  {(time.time()-t0)/max(1,nf):.2f}s/f",flush=True)
    print("done",fidx,"->",outdir)
    json.dump(dict(total_s=TOTAL,fps=FPS,frames=fidx,scenes=[(n,dd) for n,_,dd in tl]),open(os.path.join(HERE,"timeline3d.json"),"w"),indent=2)

if __name__=="__main__": main()
