#!/usr/bin/env python
"""downscale_frames.py SRC DST WxH [quality] — resize all .jpg frames."""
import os,sys
from PIL import Image
src,dst,dim=sys.argv[1],sys.argv[2],sys.argv[3]
q=int(sys.argv[4]) if len(sys.argv)>4 else 86
W,H=(int(x) for x in dim.lower().split("x"))
os.makedirs(dst,exist_ok=True)
fs=sorted(f for f in os.listdir(src) if f.endswith(".jpg"))
for i,f in enumerate(fs):
    Image.open(os.path.join(src,f)).convert("RGB").resize((W,H),Image.LANCZOS).save(os.path.join(dst,f),quality=q)
    if (i+1)%1000==0: print("down",i+1,flush=True)
print("done",len(fs))
