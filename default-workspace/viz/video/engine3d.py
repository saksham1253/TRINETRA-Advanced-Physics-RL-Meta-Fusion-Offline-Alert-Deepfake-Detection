#!/usr/bin/env python
"""engine3d.py (v2) — ultra software 3D renderer (numpy + Pillow, no GPU).

Real DEM heightfield draped with real satellite imagery. Baked lighting: sun cast-shadows (horizon march),
ambient occlusion (multi-direction horizon), aerial perspective, snow line + cinematic colour grade.
Perspective orbit camera. Helpers project arbitrary 3D points for plume / sheets / rings / routes / markers.
"""
import os, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE=os.path.dirname(os.path.abspath(__file__))
ASSETS=os.path.join(HERE,"assets")

VEXAG=4.6
# sun (world): azimuth from +x toward +y, elevation above horizon
SUN_AZ=132.0; SUN_EL=34.0
FOG=(150,170,196)          # aerial-perspective colour (hazy blue-grey)
SUN_COL=np.array([1.00,0.94,0.82])
SKY_COL=np.array([0.42,0.52,0.68])   # ambient sky light tint

def _unit(v):
    n=np.linalg.norm(v); return v/n if n else v

def _sun_vec():
    a=math.radians(SUN_AZ); e=math.radians(SUN_EL)
    return _unit(np.array([math.cos(e)*math.cos(a), math.cos(e)*math.sin(a), math.sin(e)]))

class Terrain:
    def __init__(self, geom_w=320, vexag=VEXAG):
        dem=np.load(os.path.join(ASSETS,"dem.npy")).astype(np.float64)
        self.meta=json.load(open(os.path.join(ASSETS,"dem_meta.json")))
        tex=np.asarray(Image.open(os.path.join(ASSETS,"dem_tex.png")).convert("RGB"),dtype=np.float64)
        span_x=self.meta["span_x_m"]; span_y=self.meta["span_y_m"]
        self.ar=span_y/span_x; self.span_x=span_x
        emin=dem.min(); emax=dem.max()
        gw=geom_w; gh=int(round(gw*self.ar)); self.gw=gw; self.gh=gh
        demg=np.asarray(Image.fromarray(dem.astype(np.float32)).resize((gw,gh),Image.BILINEAR),dtype=np.float64)
        self.demg=demg
        js=np.linspace(-0.5,0.5,gw); is_=np.linspace(0.5*self.ar,-0.5*self.ar,gh)
        X=np.tile(js,(gh,1)); Y=np.tile(is_[:,None],(1,gw))
        Z=(demg-emin)/span_x*vexag
        self.V=np.dstack([X,Y,Z]); self.zmid=float(Z.mean()); self.zmax=float(Z.max()); self.emin=emin
        self.dx=1.0/(gw-1); self.dy=self.ar/(gh-1)
        # vertex normals (smooth)
        gy,gx=np.gradient(Z); nx=-gx/self.dx; ny=gy/self.dy; nz=np.ones_like(Z)
        nrm=np.dstack([nx,ny,nz]); nrm/= (np.linalg.norm(nrm,axis=2,keepdims=True)+1e-9)
        self.N=nrm
        sun=_sun_vec()
        lamb=np.clip(nrm@sun,0,1)
        # ---- baked cast shadows (horizon march toward sun) ----
        shadow=self._cast_shadow(Z,sun)
        # ---- baked ambient occlusion (multi-direction horizon) ----
        ao=self._ambient_occlusion(Z)
        # ---- compose lighting on vertices ----
        elevn=(demg-emin)/max(1.0,(emax-emin))
        texf=np.asarray(Image.fromarray(tex.astype(np.uint8)).resize((gw,gh),Image.LANCZOS),dtype=np.float64)/255.0
        # exposure + saturation on real imagery
        m=texf.mean(axis=2,keepdims=True); texf=np.clip(m+(texf-m)*1.45,0,1); texf=np.clip(texf*2.05+0.03,0,1)
        direct=(lamb*(1.0-0.78*shadow))[:,:,None]*SUN_COL[None,None,:]
        ambient=(0.30+0.55*ao)[:,:,None]*SKY_COL[None,None,:]
        lit=texf*(direct+ambient)
        # snow on high + gentle slopes
        slope=1.0-nrm[:,:,2]
        snow=np.clip((elevn-0.62)/0.25,0,1)*np.clip(1.0-slope*3.2,0,1)
        snow=snow[:,:,None]
        lit=lit*(1-snow)+np.array([0.93,0.96,1.0])[None,None,:]*snow*(0.55+0.45*lamb[:,:,None])
        # cinematic grade: gamma + slight teal-orange
        lit=np.clip(lit,0,1)**0.92
        lit=np.clip(lit*np.array([1.04,1.0,0.98])[None,None,:],0,1)
        col=(lit*255.0)
        # cells
        self.cellz=(Z[:-1,:-1]+Z[1:,1:]+Z[:-1,1:]+Z[1:,:-1])/4.0
        cc=(col[:-1,:-1]+col[1:,1:]+col[:-1,1:]+col[1:,:-1])/4.0
        self.cell_col=cc.reshape(-1,3)
        v=self.V; p00=v[:-1,:-1]; p10=v[1:,:-1]; p01=v[:-1,1:]; p11=v[1:,1:]
        self.cell_v=np.stack([p00,p01,p11,p10],axis=2).reshape(-1,4,3)
        self.cell_cz=self.cellz.reshape(-1); self.ncell=self.cell_v.shape[0]

    def _march_dirs(self,Z,dirs,nsteps=48,ds=None):
        gh,gw=Z.shape
        if ds is None: ds=1.3/gw
        results=[]
        for (hx,hy) in dirs:
            h=np.array([hx,hy]); n=np.linalg.norm(h); h=h/n if n else h
            maxtan=np.zeros_like(Z)
            for k in range(1,nsteps+1):
                dist=ds*k
                dj=int(round(h[0]*dist/self.dx)); di=int(round(-h[1]*dist/self.dy))
                if di==0 and dj==0: continue
                sh=np.roll(np.roll(Z,-di,axis=0),-dj,axis=1)
                # invalidate wrapped region
                if di>0: sh[-di:,:]=-9e9
                elif di<0: sh[:-di,:]=-9e9
                if dj>0: sh[:,-dj:]=-9e9
                elif dj<0: sh[:,:-dj]=-9e9
                tan=(sh-Z)/dist
                maxtan=np.maximum(maxtan,tan)
            results.append(maxtan)
        return results

    def _cast_shadow(self,Z,sun):
        sh=self._march_dirs(Z,[(sun[0],sun[1])],nsteps=64)[0]
        sun_tan=sun[2]/max(1e-6,math.hypot(sun[0],sun[1]))
        shadow=(sh>sun_tan).astype(np.float64)
        # soften (penumbra)
        shadow=np.asarray(Image.fromarray((shadow*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)),dtype=np.float64)/255.0
        return shadow

    def _ambient_occlusion(self,Z):
        dirs=[(1,0),(0.7,0.7),(0,1),(-0.7,0.7),(-1,0),(-0.7,-0.7),(0,-1),(0.7,-0.7)]
        tans=self._march_dirs(Z,dirs,nsteps=24)
        sky=np.zeros_like(Z)
        for mt in tans:
            ang=np.arctan(np.maximum(mt,0.0)); sky+=np.cos(ang)   # visible sky fraction up to horizon
        sky/=len(dirs)
        return np.clip(sky,0,1)

class Camera:
    def __init__(self,W,H,fov_deg=40.0):
        self.W=W; self.H=H; self.f=(W/2)/math.tan(math.radians(fov_deg)/2)
        self.pos=np.array([0,-1.4,0.9]); self.target=np.array([0,0,0.08]); self.up=np.array([0,0,1.0])
    def orbit(self,az_deg,elev_deg,dist,target=None):
        if target is not None: self.target=np.array(target,dtype=float)
        a=math.radians(az_deg); e=math.radians(elev_deg)
        d=np.array([math.cos(e)*math.sin(a), -math.cos(e)*math.cos(a), math.sin(e)])
        self.pos=self.target+d*dist
    def basis(self):
        fwd=_unit(self.target-self.pos); right=_unit(np.cross(fwd,self.up)); up=np.cross(right,fwd)
        return fwd,right,up
    def project(self,P):
        fwd,right,up=self.basis(); rel=P-self.pos
        cz=rel@fwd; cx=rel@right; cy=rel@up
        czc=np.where(np.abs(cz)<1e-6,1e-6,cz)
        return np.stack([self.W/2+self.f*cx/czc, self.H/2-self.f*cy/czc, cz],axis=1)

# -------- sky with sun glow + horizon haze --------
_SKY_CACHE={}
def sky(W,H,cam=None):
    key=(W,H)
    if key in _SKY_CACHE: base=_SKY_CACHE[key].copy()
    else:
        yy=np.linspace(0,1,H)[:,None]
        top=np.array([18,28,50]); mid=np.array([70,96,140]); hor=np.array([150,170,196])
        t=yy
        col=np.where(t<0.72, top+(mid-top)*(t/0.72), mid+(hor-mid)*((t-0.72)/0.28))
        arr=np.repeat(col[:,None,:],W,axis=1).astype(np.uint8)
        _SKY_CACHE[key]=arr.copy(); base=arr
    im=Image.fromarray(base,"RGB")
    # sun glow billboard
    if cam is not None:
        sv=_sun_vec(); sp=cam.pos+sv*8.0
        s=cam.project(np.array([sp]))[0]
        if s[2]>0:
            gl=Image.new("RGB",(W,H),(0,0,0)); gd=ImageDraw.Draw(gl)
            for r,a in [(220,60),(130,90),(70,140),(34,220)]:
                gd.ellipse([s[0]-r,s[1]-r,s[0]+r,s[1]+r],fill=(int(255*a/255),int(240*a/255),int(205*a/255)))
            gl=gl.filter(ImageFilter.GaussianBlur(26))
            im=Image.fromarray(np.clip(np.asarray(im).astype(int)+np.asarray(gl).astype(int),0,255).astype(np.uint8),"RGB")
    return im

def render_terrain(im, cam, terr, fog_near=1.0, fog_far=3.4, dim=1.0, fog_col=FOG):
    W,H=cam.W,cam.H
    verts=terr.cell_v.reshape(-1,3)
    pr=cam.project(verts).reshape(-1,4,3)
    sx=pr[:,:,0]; sy=pr[:,:,1]; cz=pr[:,:,2]
    infront=(cz>0.02).all(axis=1)
    minx=sx.min(1); maxx=sx.max(1); miny=sy.min(1); maxy=sy.max(1)
    onscreen=(maxx>0)&(minx<W)&(maxy>0)&(miny<H)
    vis=infront&onscreen
    idx=np.nonzero(vis)[0]
    if idx.size==0: return 999.0
    depth=cz[idx].mean(1); order=idx[np.argsort(-depth)]
    d=cz[order].mean(1)
    ff=np.clip((d-fog_near)/(fog_far-fog_near),0,1)*0.85
    sxo=sx[order]; syo=sy[order]; co=terr.cell_col[order]
    # vectorise colour (dim + fog) once, outside the per-polygon loop
    cols=co*dim; cols=cols*(1-ff[:,None])+np.array(fog_col)[None,:]*ff[:,None]
    cols=np.clip(cols,0,255).astype(np.int32).tolist()
    xy=np.stack([sxo,syo],axis=-1).tolist()
    poly=ImageDraw.Draw(im).polygon
    for k in range(len(xy)):
        q=xy[k]
        poly([q[0][0],q[0][1],q[1][0],q[1][1],q[2][0],q[2][1],q[3][0],q[3][1]],fill=tuple(cols[k]))
    return float(d.min())

def terrain_z_at(terr,x,y):
    gw,gh=terr.gw,terr.gh
    j=(x+0.5)*(gw-1); i=(0.5*terr.ar - y)/terr.ar*(gh-1)
    i=min(max(i,0),gh-1); j=min(max(j,0),gw-1)
    i0,j0=int(i),int(j); i1,j1=min(i0+1,gh-1),min(j0+1,gw-1); fi,fj=i-i0,j-j0
    V=terr.V
    return float(V[i0,j0,2]*(1-fi)*(1-fj)+V[i0,j1,2]*(1-fi)*fj+V[i1,j0,2]*fi*(1-fj)+V[i1,j1,2]*fi*fj)
