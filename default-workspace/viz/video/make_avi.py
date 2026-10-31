#!/usr/bin/env python
"""make_avi.py — assemble the rendered frames into a Motion-JPEG AVI (pure Python, no external binary).

We cannot run ffmpeg in this environment (the OS blocks launching the unsigned binary), so we build a
standards MJPEG AVI by hand. Each frame is re-encoded to a baseline JPEG (quality tuned for size) and written
as an '00dc' chunk; an idx1 index is appended. Plays in VLC and the Windows Media Player (MJPEG decoder ships
with Windows).
"""
import os, struct, io, sys
from PIL import Image

HERE=os.path.dirname(os.path.abspath(__file__))
# args: [quality] [frames_subdir] [WxH] [out_name]
QUALITY=int(sys.argv[1]) if len(sys.argv)>1 else 72
FRAMES=os.path.join(HERE,sys.argv[2] if len(sys.argv)>2 else "frames")
if len(sys.argv)>3: W,H=(int(x) for x in sys.argv[3].lower().split("x"))
else: W,H=1920,1080
OUT=os.path.join(HERE,"output",sys.argv[4] if len(sys.argv)>4 else "trinetra_datastack.avi")
FPS=20

def fourcc(s): return s.encode("ascii")

files=sorted(f for f in os.listdir(FRAMES) if f.endswith(".jpg"))
N=len(files)
print(f"frames={N} quality={QUALITY} -> {OUT}")
os.makedirs(os.path.dirname(OUT),exist_ok=True)

# ---- build hdrl (fixed size) ----
def avih():
    return struct.pack("<4sI14I".replace("14I","I"*14),
        b"avih",56,
        int(1_000_000//FPS),  # dwMicroSecPerFrame
        W*H*3,                # dwMaxBytesPerSec (upper bound)
        0,                    # dwPaddingGranularity
        0x10,                 # dwFlags = AVIF_HASINDEX
        N,0,1,                # dwTotalFrames, dwInitialFrames, dwStreams
        W*H*3,                # dwSuggestedBufferSize
        W,H,0,0,0,0)          # width,height + reserved[4]

def strl():
    # AVIStreamHeader (strh) = 56 bytes payload
    strh=struct.pack("<4sI 4s4s I HH I IIIII i I hhhh".replace(" ",""),
        b"strh",56,
        b"vids",b"MJPG",
        0,                    # dwFlags
        0,0,                  # wPriority, wLanguage
        0,                    # dwInitialFrames
        1,FPS,0,N,W*H*3,      # dwScale, dwRate, dwStart, dwLength, dwSuggestedBufferSize
        -1,                   # dwQuality
        0,                    # dwSampleSize
        0,0,W,H)              # rcFrame
    bih=struct.pack("<4sIIiiHH4sIiiII",
        b"strf",40,
        40,W,H,1,24,
        b"MJPG",W*H*3,0,0,0,0)
    body=strh+bih
    return b"LIST"+struct.pack("<I",len(body)+4)+b"strl"+body

hdrl_body=avih()+strl()
hdrl=b"LIST"+struct.pack("<I",len(hdrl_body)+4)+b"hdrl"+hdrl_body

with open(OUT,"wb") as f:
    f.write(b"RIFF"); riff_size_pos=f.tell(); f.write(struct.pack("<I",0)); f.write(b"AVI ")
    f.write(hdrl)
    f.write(b"LIST"); movi_size_pos=f.tell(); f.write(struct.pack("<I",0))
    movi_fourcc_pos=f.tell(); f.write(b"movi")
    index=[]
    for i,name in enumerate(files):
        im=Image.open(os.path.join(FRAMES,name)).convert("RGB")
        if im.size!=(W,H): im=im.resize((W,H))
        bio=io.BytesIO(); im.save(bio,format="JPEG",quality=QUALITY,subsampling=1); jb=bio.getvalue()
        ckid_pos=f.tell()
        off=ckid_pos-movi_fourcc_pos
        f.write(b"00dc"); f.write(struct.pack("<I",len(jb))); f.write(jb)
        if len(jb)&1: f.write(b"\x00")
        index.append((off,len(jb)))
        if (i+1)%500==0: print(f"  wrote {i+1}/{N}")
    movi_end=f.tell()
    # idx1
    f.write(b"idx1"); f.write(struct.pack("<I",16*N))
    for off,sz in index:
        f.write(b"00dc"); f.write(struct.pack("<I",0x10)); f.write(struct.pack("<I",off)); f.write(struct.pack("<I",sz))
    file_end=f.tell()
    # patch sizes
    f.seek(movi_size_pos); f.write(struct.pack("<I",movi_end-(movi_size_pos+4)))
    f.seek(riff_size_pos); f.write(struct.pack("<I",file_end-8))

mb=os.path.getsize(OUT)/1048576
print(f"DONE: {OUT}  {mb:.1f} MB  ({N} frames, {N/FPS:.1f}s)")
