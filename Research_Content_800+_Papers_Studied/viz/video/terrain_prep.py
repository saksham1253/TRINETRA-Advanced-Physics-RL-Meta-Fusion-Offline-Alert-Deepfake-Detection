#!/usr/bin/env python
"""terrain_prep.py — stitch terrarium elevation + Esri imagery tiles, crop to AOI, build a heightfield mesh.
Outputs (in assets/):
  dem.npy        float32 HxW elevation in metres (downsampled mesh grid)
  dem_tex.png    RGB texture aligned to the mesh grid extent (higher res)
  dem_meta.json  grid dims, metre ranges, real-world span, min/max elevation
"""
import os, json, math
import numpy as np
from PIL import Image

HERE=os.path.dirname(os.path.abspath(__file__))
TILES=os.path.join(HERE,"assets","tiles")
ASSETS=os.path.join(HERE,"assets")
meta=json.load(open(os.path.join(TILES,"meta.json")))
Z=meta["z"]; xmin=meta["xmin"]; xmax=meta["xmax"]; ymin=meta["ymin"]; ymax=meta["ymax"]; T=meta["tile"]
W=meta["width"]; H=meta["height"]
nx=xmax-xmin+1; ny=ymax-ymin+1

def stitch(kind, decode):
    out=None
    for ty in range(ny):
        for tx in range(nx):
            p=os.path.join(TILES,kind,f"{xmin+tx}_{ymin+ty}.png")
            im=Image.open(p).convert("RGB"); a=np.asarray(im,dtype=np.float64)
            if out is None:
                if decode: out=np.zeros((ny*T,nx*T),dtype=np.float32)
                else: out=np.zeros((ny*T,nx*T,3),dtype=np.uint8)
            if decode:
                elev=(a[:,:,0]*256.0+a[:,:,1]+a[:,:,2]/256.0)-32768.0
                out[ty*T:(ty+1)*T, tx*T:(tx+1)*T]=elev
            else:
                out[ty*T:(ty+1)*T, tx*T:(tx+1)*T]=a.astype(np.uint8)
    return out

print("stitching elevation...")
dem_full=stitch("terr",True)
print("stitching imagery...")
tex_full=stitch("sat",False)
print("mosaic", dem_full.shape, "elev range", float(dem_full.min()), float(dem_full.max()))

# --- crop to AOI using web-mercator-correct pixel mapping ---
west=meta["west"]; east=meta["east"]; north=meta["north"]; south=meta["south"]
aoi=meta["aoi"]
def mercY(lat): return math.log(math.tan(math.pi/4+math.radians(lat)/2))
mN,mS=mercY(north),mercY(south)
def lon2col(lon): return (lon-west)/(east-west)*W
def lat2row(lat): return (mN-mercY(lat))/(mN-mS)*H
c0=int(round(lon2col(aoi["west"]))); c1=int(round(lon2col(aoi["east"])))
r0=int(round(lat2row(aoi["north"]))); r1=int(round(lat2row(aoi["south"])))
c0,c1=max(0,c0),min(W,c1); r0,r1=max(0,r0),min(H,r1)
dem=dem_full[r0:r1, c0:c1]; tex=tex_full[r0:r1, c0:c1]
print("AOI crop px", dem.shape)

# real-world span (metres)
latm=0.5*(aoi["south"]+aoi["north"])
span_x=(aoi["east"]-aoi["west"])*111320.0*math.cos(math.radians(latm))
span_y=(aoi["north"]-aoi["south"])*110574.0

# --- downsample to a mesh grid (keep aspect ~ cells roughly square in world units) ---
MESH_W=420
MESH_H=int(round(MESH_W*(span_y/span_x)))
dem_s=np.asarray(Image.fromarray(dem).resize((MESH_W,MESH_H),Image.BILINEAR),dtype=np.float32)
# clamp sea-level artefacts (terrarium ocean = -32768-ish handled; here clip negatives mildly)
dem_s=np.clip(dem_s, max(0.0,float(dem_s.min())), None) if dem_s.min()<-500 else dem_s
# texture a bit higher res than mesh for crisp drape
TEX_W=1680; TEX_H=int(round(TEX_W*(dem.shape[0]/dem.shape[1])))
tex_img=Image.fromarray(tex).resize((TEX_W,TEX_H),Image.LANCZOS)
tex_img.save(os.path.join(ASSETS,"dem_tex.png"))
np.save(os.path.join(ASSETS,"dem.npy"),dem_s)
out_meta=dict(mesh_w=MESH_W,mesh_h=MESH_H,tex_w=TEX_W,tex_h=TEX_H,
    span_x_m=span_x,span_y_m=span_y,
    elev_min=float(dem_s.min()),elev_max=float(dem_s.max()),
    aoi=aoi)
json.dump(out_meta,open(os.path.join(ASSETS,"dem_meta.json"),"w"),indent=2)
print("mesh",MESH_W,"x",MESH_H,"elev",out_meta["elev_min"],"..",out_meta["elev_max"],
      "span km", round(span_x/1000,1),"x",round(span_y/1000,1))
print("saved dem.npy, dem_tex.png, dem_meta.json")
