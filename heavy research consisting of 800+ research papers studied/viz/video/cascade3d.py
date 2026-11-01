#!/usr/bin/env python
"""cascade3d.py (v3) — GLOF "working simulation" over the 3D terrain, with a persistent high-level
DFD panel that shows the whole model running and data flowing node-by-node to a decision.

Scenario: a glacial-lake outburst flood (GLOF) in the Uttarakhand valley, cascading into a rain-saturated
slope failure, people downstream at risk, and the full TRINETRA pipeline reaching a human-gated alert.

Honesty: terrain/imagery REAL; the GLOF trigger, flood geometry, sensor detections, reach rings, evac route
and people-count are ILLUSTRATIVE (no trained models; "Nothing was built, trained, or measured"). The slope
physics (Caine / Iverson / FS / Fukuzono) and the decision math (conformal p*, shield incl. GLOF→Red,
mandatory human gate) are SIMULATED on the real numpy code — numbers are the real computed values.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

LAKE=(-0.22,0.26); VILL=(0.12,-0.14); SAFE=(0.28,-0.03)
FLOODPATH=[(-0.22,0.26),(-0.12,0.14),(-0.03,0.03),(0.05,-0.06),(0.12,-0.14)]
EVAC=[(0.12,-0.14),(0.18,-0.10),(0.24,-0.06),(0.28,-0.03)]

# high-level DFD lanes (ids match l12_dfd.json)
LAYOUT=[("eo","L"),("iot","R"),("ws1","L"),("anom","R"),("cctv","L"),("social","R"),
        ("fusion","C"),("decision","C"),("human","C"),("alert","L"),("rl","R")]
ROWY={"eo":0,"iot":0,"ws1":1,"anom":1,"cctv":2,"social":2,"fusion":3,"decision":4,"human":5,"alert":6,"rl":6}

def scenes(G):
    W=G["W"]; H=G["H"]; TERR=G["TERR"]; E=G["E"]; RV=G["RV"]; font=G["font"]; DFD=G["DFD"]
    cams=G["cams"]; render_world=G["render_world"]; hud=G["hud"]; billboard=G["billboard"]
    REAL=G["REAL"]; SIM=G["SIM"]; ILLUS=G["ILLUS"]; FOCUS=G["FOCUS"]; WARN=G["WARN"]
    INK=G["INK"]; INK2=G["INK2"]; INK3=G["INK3"]; HAIR=G["HAIR"]; BG=G["BG"]
    clamp=G["clamp"]; ease=G["ease"]; eout=G["eout"]; lerp=G["lerp"]; mix=G["mix"]
    tz=lambda x,y: E.terrain_z_at(TERR,x,y)
    kindcol=lambda k: REAL if k=="REAL" else (SIM if k=="SIM" else ILLUS)
    NODE={n["id"]:n for n in DFD["nodes"]}; EDGES=[(e["from"],e["to"]) for e in DFD["edges"]]

    # ----- persistent DFD panel (right side) -----
    PX=1300; PX1=W-28; PY0=92; PY1=H-74
    NW,NH=232,58
    cL=PX+176; cR=PX+430; cC=(cL+cR)//2
    rows=7; ry=[PY0+92+i*((PY1-PY0-150)//(rows-1)) for i in range(rows)]
    NPOS={}
    for nid,side in LAYOUT:
        cx={"L":cL,"R":cR,"C":cC}[side]; NPOS[nid]=(cx,ry[ROWY[nid]])

    def _node_box(d,nid,status,val,tp):
        cx,cy=NPOS[nid]; nd=NODE[nid]; col=kindcol(nd["kind"])
        x0,y0,x1,y1=cx-NW//2,cy-NH//2,cx+NW//2,cy+NH//2
        if status=="idle":
            RV.rrect(d,[x0,y0,x1,y1],9,fill=(16,22,30,255),outline=(48,60,74),width=2)
            RV.text(d,(cx,cy-14),nd["label"][:26],font("sans",14),INK3,anchor="ma")
        else:
            if status=="active":
                pulse=int(60+40*math.sin(tp*5)); RV.rrect(d,[x0-5,y0-5,x1+5,y1+5],11,fill=None,outline=(col[0],col[1],col[2]),width=2)
            RV.rrect(d,[x0,y0,x1,y1],9,fill=RV._dim(col,0.26),outline=col,width=3 if status=="active" else 2)
            RV.text(d,(x0+12,y0+8),nd["label"][:26],font("semi",14),INK)
            if val: RV.text(d,(x0+12,y0+30),val,font("monob",14),col)
            if status=="done": RV.text(d,(x1-22,y0+6),"✓",font("bold",18),REAL)
        chip=nd["kind"][0:3] if nd["kind"]!="SIMULATED" else "SIM"
        chipc={"REA":REAL,"SIM":SIM,"ILL":ILLUS}.get(chip,SIM)
        RV.text(d,(x1-40,y1-20),{"REAL":"REAL","SIMULATED":"SIM"}.get(nd["kind"],"ILL"),font("mono",11),chipc)

    def dfd_panel(d,state,tp):
        RV.rrect(d,[PX,PY0,PX1,PY1],14,fill=(8,11,16,238),outline=HAIR,width=1)
        RV.text(d,(PX+22,PY0+16),"LIVE MODEL — data flow",font("bold",21),FOCUS)
        RV.text(d,(PX+22,PY0+46),"advisory · human-in-the-loop · never autonomous",font("sans",14),INK2)
        done=state.get("done",set()); active=state.get("active"); firing=state.get("firing"); vals=state.get("values",{})
        for a,b in EDGES:
            pa=NPOS[a]; pb=NPOS[b]; on=(a in done or a==active) and (b in done or b==active)
            ax,ay=pa[0],pa[1]+NH//2; bx,by=pb[0],pb[1]-NH//2
            d.line([(ax,ay),(bx,by)],fill=((FOCUS[0],FOCUS[1],FOCUS[2],200) if on else (52,64,78,150)),width=3 if on else 2)
        for nid,_ in LAYOUT:
            status="done" if nid in done else ("active" if nid==active else "idle")
            _node_box(d,nid,status,vals.get(nid),tp)
        if firing:
            fa,fb,p=firing; pa=NPOS[fa]; pb=NPOS[fb]
            ax,ay=pa[0],pa[1]+NH//2; bx,by=pb[0],pb[1]-NH//2
            dx=ax+(bx-ax)*p; dy=ay+(by-ay)*p
            d.ellipse([dx-11,dy-11,dx+11,dy+11],fill=(120,200,255,120))
            d.ellipse([dx-7,dy-7,dx+7,dy+7],fill=(165,220,255,255),outline=INK)

    # ----- step card (bottom-left, plain language) -----
    def step_card(d,n,total,title,kind,lines):
        x,y,bw,bh=40,H-336,760,256
        RV.rrect(d,[x,y,x+bw,y+bh],14,fill=(10,14,20,238),outline=kindcol(kind),width=2)
        RV.text(d,(x+24,y+16),f"STEP {n} / {total}",font("mono",15),INK3)
        RV.chip(d,(x+bw-176,y+14),{"REAL":"REAL","SIM":"SIMULATED","ILLUS":"ILLUSTRATIVE"}[kind],kindcol(kind),font("bold",16))
        RV.text(d,(x+24,y+40),title,font("bold",25),INK)
        yy=y+84
        for seg in lines:
            if isinstance(seg,tuple):
                lab,val,c=seg; RV.text(d,(x+24,yy),lab,font("sans",18),INK2)
                RV.text(d,(x+24+font("sans",18).getlength(lab)+10,yy-1),val,font("monob",18),c); yy+=32
            else: yy=RV.para(d,(x+24,yy),seg,font("sans",18),INK2,bw-48,26)+8

    def people_card(d,n_illus,prog):
        x,y=430,150; RV.rrect(d,[x,y,x+560,y+120],13,fill=(26,16,12,242),outline=WARN,width=3)
        RV.text(d,(x+22,y+14),"⚠  PEOPLE IN THE FLOOD PATH",font("bold",23),WARN)
        cnt=int(n_illus*ease(clamp(prog)))
        RV.text(d,(x+22,y+52),f"≈ {cnt:,} people",font("bold",40),INK)
        RV.chip(d,(x+320,y+66),"ILLUSTRATIVE",ILLUS,font("bold",15))
        RV.text(d,(x+320,y+96),"WorldPop would supply this — not extracted",font("sans",13),INK3)

    def risk_bar(d,risk,level,x=None,y=None):
        x=x if x is not None else 820; y=y if y is not None else H-290
        RV.rrect(d,[x,y,x+440,y+210],13,fill=(10,14,20,238),outline=FOCUS,width=2)
        RV.text(d,(x+22,y+14),"Decision — conformal level + shield",font("bold",19),FOCUS)
        p=0.0476; bx,by,bw=x+22,y+64,396; d.rectangle([bx,by,bx+bw,by+26],outline=HAIR,width=1); hi=10*p
        for cut,c,lb in [(p,(242,201,65),"Y"),(4*p,(230,140,70),"O"),(10*p,WARN,"R")]:
            fx=clamp(cut/hi); d.line([(bx+bw*fx,by-6),(bx+bw*fx,by+32)],fill=c,width=2); RV.text(d,(bx+bw*fx-5,by-24),lb,font("mono",13),c)
        fx=clamp(risk/hi); d.rectangle([bx,by,bx+bw*fx,by+26],fill=FOCUS)
        RV.text(d,(x+22,y+104),f"fused risk p = {risk:.3f}",font("monob",19),INK)
        RV.text(d,(x+22,y+136),"p* = 5/105 = 0.0476 · cuts (p*,4p*,10p*)",font("mono",14),INK2)
        RV.text(d,(x+22,y+164),f"GLOF shield floor ⇒ level = {level}",font("monob",19),(WARN if level in('Orange','Red') else SIM))

    def human_card(d,approved):
        x,y=300,H//2-180
        RV.rrect(d,[x,y,x+720,y+300],17,fill=(12,16,22,247),outline=(REAL if approved else FOCUS),width=3)
        RV.text(d,(x+40,y+28),"MANDATORY HUMAN-IN-THE-LOOP GATE",font("bold",27),REAL)
        RV.para(d,(x+40,y+78),"require_human_approval = True (hard-wired). The CAP builder refuses to emit any public message without an operator 'APPROVED:' token.",font("sans",19),INK,640,27)
        RV.para(d,(x+40,y+150),"The model is ADVISORY and NEVER raises a public alert on its own (Rule R19).",font("semi",19),INK2,640,26)
        if approved:
            RV.rrect(d,[x+40,y+214,x+320,y+270],11,fill=RV._dim(REAL,0.25),outline=REAL,width=2)
            RV.text(d,(x+60,y+226),"APPROVED  ✓",font("bold",27),REAL); RV.text(d,(x+340,y+230),"operator sign-off → dissemination",font("sans",17),INK2)
        else:
            RV.rrect(d,[x+40,y+214,x+380,y+270],11,fill=(30,22,10,255),outline=FOCUS,width=2); RV.text(d,(x+60,y+226),"AWAITING OPERATOR…",font("bold",23),FOCUS)

    def draw_marker(d,cam,x,y,label,color,up=0.04):
        s=cam.project(np.array([[x,y,tz(x,y)],[x,y,tz(x,y)+up]]))
        if (s[:,2]<=0.05).any(): return
        d.line([(s[0,0],s[0,1]),(s[1,0],s[1,1])],fill=color,width=3)
        d.ellipse([s[1,0]-7,s[1,1]-7,s[1,0]+7,s[1,1]+7],fill=color,outline=INK,width=2)
        tw=font("semi",18).getlength(label)
        RV.rrect(d,[s[1,0]+10,s[1,1]-22,s[1,0]+24+tw,s[1,1]+6],5,fill=(10,14,20,220),outline=color,width=1)
        RV.text(d,(s[1,0]+17,s[1,1]-19),label,font("semi",18),color)

    def camf(t,dur,az0,az1,elev,dist,tgt): return (lerp(az0,az1,ease(clamp(t/dur))),elev,dist,tgt)
    TGTC=[-0.05,0.02,TERR.zmid]

    TOTSTEPS=11
    def mk(name,dur,builder):
        def fn(t,d_):
            ct=G["CUR_T"]; orbit,wst,ov=builder(t,dur)
            c2,c1=cams(*orbit); im=render_world(c2,wst,ct,dim=0.9); d=ImageDraw.Draw(im,"RGBA")
            for (x,y,lab,c) in ov.get("markers",[]): draw_marker(d,c1,x,y,lab,c)
            if "people" in ov: people_card(d,*ov["people"])
            if "risk" in ov: risk_bar(d,*ov["risk"])
            if "human" in ov: human_card(d,ov["human"])
            if "card" in ov: step_card(d,*ov["card"])
            if "title" in ov:
                a=ease(clamp(t/1.3)); RV.text(d,(640,150),ov["title"],font("bold",44),mix(BG,WARN,a),anchor="ma")
                if ov.get("subtitle"): RV.text(d,(640,210),ov["subtitle"],font("semi",21),mix(BG,INK2,a),anchor="ma")
            if "recap" in ov:
                a=ease(clamp(t/1.5)); x=70; y=240
                RV.text(d,(x,160),"HOW THE MODEL DECIDED",font("bold",34),mix(BG,INK,a))
                rows=["① EO + glacier data saw the lake  (REAL feeds)",
                      "② GLOF trigger + flood  (ILLUSTRATIVE — no trained detector)",
                      "③ WS1 physics: Caine>1, FS<1, Fukuzono  (SIMULATED, real code)",
                      "④ WS8 anomaly + WS2 media (≤0.40) → WS5 meta-fusion  (SIM)",
                      "⑤ max(conformal p*=0.0476, shield) → GLOF floor = RED  (SIM)",
                      "⑥ MANDATORY human approval  (REAL)",
                      "⑦ WS3 siren→mesh→cell + evac advisory  (ILLUSTRATIVE)"]
                for i,r in enumerate(rows):
                    RV.text(d,(x,y+i*54),r,font("semi",21),mix(BG,INK2,ease(clamp((t-0.5-i*0.25)/1.1))))
            dfd_panel(d,ov.get("dfd",{}),t)
            hud(d,caption=ov.get("cap"),cap_kind=ov.get("capk"),progress=G["CUR_T"]/G["TOTAL"])
            return im.convert("RGB")
        return (name,fn,dur)

    V={}  # accumulate node values across steps
    def dfd(done,active=None,firing=None,**vals):
        V.update(vals); return {"done":set(done),"active":active,"firing":firing,"values":dict(V)}

    def b_title(t,dur):
        return camf(t,dur,20,52,30,2.0,[0,0,TERR.zmid]),{},{"title":"WORKING SIMULATION — a GLOF in the valley",
            "subtitle":"watch the whole model run on the right as the disaster unfolds","dfd":dfd([]),
            "cap":"SIMULATED scenario on REAL terrain — real-code numbers, illustrative hazard geometry","capk":"SIM"}
    def b_lake(t,dur):
        return camf(t,dur,70,52,30,1.5,[LAKE[0]+0.05,LAKE[1]-0.05,TERR.zmid]),{"lake":(LAKE[0],LAKE[1],0.12,eout(clamp(t/2.0)))},{
            "markers":[(LAKE[0],LAKE[1],"glacial lake",FOCUS)],"dfd":dfd(["eo"],active="eo",eo="S1/S2 · ITS_LIVE"),
            "card":(1,TOTSTEPS,"A glacial lake, watched from space","REAL",["EO satellites + glacier-velocity monitor the lake and its moraine dam.",("feeds (registry):","ITS_LIVE · GLOFNet · HMAGLOFDB (766 GLOFs)",REAL),"Real datasets exist in the registry — but no GLOF model is trained here."]),
            "cap":"REAL data feeds; detection itself is illustrative (no trained model)","capk":"REAL"}
    def b_burst(t,dur):
        return camf(t,dur,52,30,26,1.35,[LAKE[0]+0.08,LAKE[1]-0.08,TERR.zmid]),{"lake":(LAKE[0],LAKE[1],0.12*(1-0.4*clamp(t/dur)),0.9),"flood":(clamp(t/dur*0.5),FLOODPATH)},{
            "markers":[(LAKE[0],LAKE[1],"OUTBURST",WARN)],"dfd":dfd(["eo"],active="anom",firing=("eo","anom",clamp(t/dur)),anom="EO change +"),
            "card":(2,TOTSTEPS,"The lake bursts — a flood is born","ILLUS",["The moraine dam fails and water surges down the valley.",("this trigger:","ILLUSTRATIVE — no GLOF detector is trained",ILLUS),"WS8 flags the EO change; the flood geometry is illustrative, not a hydraulic model."]),
            "cap":"GLOF trigger + flood are ILLUSTRATIVE geometry (honestly flagged)","capk":"ILLUS"}
    def b_flood(t,dur):
        return camf(t,dur,30,6,22,1.4,[0.0,0.0,TERR.zmid]),{"flood":(0.5+0.5*clamp(t/dur),FLOODPATH)},{
            "markers":[(VILL[0],VILL[1],"settlement",INK)],"dfd":dfd(["eo","anom"],active="iot",firing=("iot","ws1",clamp(t/dur)),iot="river-stage ↑ · tilt"),
            "card":(3,TOTSTEPS,"Ground sensors feel the surge","REAL",["WS7 LoRa river-stage + tilt + soil nodes on the valley floor report the rising water (edge-first, offline).",("feeds WS1:","rain I, tilt rate, soil moisture",REAL),"Real sensing design; the specific readings here are illustrative."]),
            "cap":"WS7 IoT sensing = REAL design; readings are scenario/illustrative","capk":"ILLUS"}
    def b_people(t,dur):
        return camf(t,dur,6,-12,20,1.3,[VILL[0],VILL[1]+0.03,TERR.zmid]),{"flood":(1.0,FLOODPATH)},{
            "markers":[(VILL[0],VILL[1],"settlement at risk",WARN)],"people":(1850,t/dur*1.4),"dfd":dfd(["eo","anom","iot"],active="iot"),
            "card":(4,TOTSTEPS,"Who is exposed downstream","ILLUS",["Exposure = population in the flood path (WorldPop) × the illustrative inundation footprint.",("people at risk:","≈ 1,850  (ILLUSTRATIVE)",ILLUS),"No WorldPop extract was run — the count is a placeholder, clearly flagged."]),
            "cap":"people-at-risk is ILLUSTRATIVE — WorldPop would supply the real figure","capk":"ILLUS"}
    def b_ws1(t,dur):
        return camf(t,dur,-12,-34,22,1.4,[0.03,-0.03,TERR.zmid]),{"flood":(1.0,FLOODPATH),"scar":clamp((t/dur-0.3)/0.5)},{
            "markers":[(0.04,-0.05,"slope failing",WARN)],"dfd":dfd(["eo","anom","iot"],active="ws1",firing=("ws1","fusion",clamp(t/dur)),ws1="FS<1 · p_phys↑"),
            "card":(5,TOTSTEPS,"WS1 physics: the saturated slope fails too","SIM",[("Caine I–D:","I/I_thr = 1.0857 > 1  → exceeded",SIM),("Factor of Safety:","crosses 1 between β=37° (1.0011) and 38° (0.9664)",SIM),("Fukuzono 1/v:","α = 2 → time-to-failure trend",SIM),"Real geotech equations, run on our numpy core → noisy-OR p_phys."]),
            "cap":"WS1 slope physics — real equations/code, scenario parameters","capk":"SIM"}
    def b_media(t,dur):
        return camf(t,dur,-34,-20,24,1.6,TGTC),{"flood":(1.0,FLOODPATH),"scar":1.0},{
            "dfd":dfd(["eo","anom","iot","ws1","cctv","social"],active="fusion",firing=("social","fusion",clamp(t/dur)),anom="EO change +",cctv="River-Eye stage",social="trust ≤ 0.40"),
            "card":(6,TOTSTEPS,"Corroboration — and a hard cap on media","SIM",["WS8 EO-anomaly adds an independent change signal; WS4 River-Eye stage corroborates.",("WS2 social-media trust:","CAPPED at reliability 0.40",ILLUS),"Media can corroborate or suppress — but can NEVER gate a life-safety alert."]),
            "cap":"deepfake/media trust hard-capped at 0.40 — never gates","capk":"SIM"}
    def b_fusion(t,dur):
        return camf(t,dur,-20,-4,26,1.7,TGTC),{"flood":(1.0,FLOODPATH),"scar":1.0},{
            "dfd":dfd(["eo","anom","iot","ws1","cctv","social"],active="fusion",firing=("fusion","decision",clamp(t/dur)),fusion="fused p · u*"),
            "card":(7,TOTSTEPS,"WS5 meta-fusion","SIM",["All expert outputs enter a gated, precision-weighted meta-fusion (FM-1).",("output:","fused risk p + uncertainty u*",SIM),"No trained RL/weights — this is the reference fusion code path."]),
            "cap":"no trained models — WS5 fusion is the reference code path","capk":"SIM"}
    def b_decide(t,dur):
        risk=lerp(0.03,0.52,eout(clamp(t/dur)))
        return camf(t,dur,-4,10,24,1.8,[0,0,TERR.zmid]),{"flood":(1.0,FLOODPATH),"scar":1.0},{
            "risk":(risk,"Red"),"dfd":dfd(["eo","anom","iot","ws1","cctv","social","fusion"],active="decision",firing=("decision","human",clamp(t/dur)),decision="level = RED"),
            "card":(8,TOTSTEPS,"One decision function — with a hard shield","SIM",[("level =","max(conformal_level(risk, p*), shield_floor)",FOCUS),("GLOF floor:","GLOF ⇒ Red  (RAISE-only shield)",WARN),"The shield is monotone — it can only raise the level, never silence it."]),
            "cap":"conformal level + RAISE-only shield; GLOF forces Red","capk":"SIM"}
    def b_human(t,dur):
        return camf(t,dur,10,22,24,1.85,[0,0,TERR.zmid]),{"flood":(1.0,FLOODPATH),"scar":1.0},{
            "human":t>dur*0.5,"dfd":dfd(["eo","anom","iot","ws1","cctv","social","fusion","decision"],active="human",human="APPROVED ✓" if False else "awaiting…"),
            "cap":"ADVISORY · a human approves every public alert (Rule R19)","capk":"REAL"}
    def b_alert(t,dur):
        g=eout(clamp(t/dur))
        rings=[(VILL[0],VILL[1],0.07+0.11*g,WARN,220),(VILL[0],VILL[1],0.07+0.18*g,(230,140,70),180),(VILL[0],VILL[1],0.07+0.27*g,FOCUS,150)]
        return camf(t,dur,22,46,22,1.55,[VILL[0]*0.4,VILL[1]*0.4,TERR.zmid]),{"flood":(1.0,FLOODPATH),"scar":1.0,"rings":rings,"route":(clamp(t/dur*1.2),REAL,EVAC)},{
            "markers":[(VILL[0],VILL[1],"settlement",INK),(SAFE[0],SAFE[1],"muster point",REAL)],
            "dfd":dfd(["eo","anom","iot","ws1","cctv","social","fusion","decision","human","alert","rl"],active="alert",human="APPROVED ✓",alert="siren→mesh→cell",rl="evac route"),
            "card":(9,TOTSTEPS,"Approved → tiered alert + evacuation advice","ILLUS",["siren → LAN/mesh → cell-broadcast → DTN store-carry-forward (offline-first).",("reach rings + route:","ILLUSTRATIVE geometry",ILLUS),"No acoustic/radio range model; evac is a rule baseline over OSM roads — no trained policy."]),
            "cap":"reach rings + route are illustrative (no range model / no trained policy)","capk":"ILLUS"}
    def b_recap(t,dur):
        return camf(t,dur,46,86,28,2.0,[0,0,TERR.zmid]),{"flood":(1.0,FLOODPATH),"scar":0.7},{
            "recap":t,"dfd":dfd(["eo","anom","iot","ws1","cctv","social","fusion","decision","human","alert","rl"]),
            "cap":"advisory decision-support — the model recommends, a human decides","capk":"REAL"}

    return [mk("cas_title",12,b_title),mk("cas_lake",26,b_lake),mk("cas_burst",28,b_burst),mk("cas_flood",30,b_flood),
            mk("cas_people",26,b_people),mk("cas_ws1",36,b_ws1),mk("cas_media",26,b_media),mk("cas_fusion",26,b_fusion),
            mk("cas_decide",32,b_decide),mk("cas_human",24,b_human),mk("cas_alert",34,b_alert),mk("cas_recap",26,b_recap)]
