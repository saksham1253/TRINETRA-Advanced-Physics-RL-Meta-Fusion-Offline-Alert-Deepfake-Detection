from PIL import Image
import os, collections

folder = r"C:\Users\Dell\Documents\deepseek-harness\default-workspace\ppt_work\media"
for n in ["trinetra_v2_s1.png","trinetra_v2_s2.png","trinetra_v2_s5.png","trinetra_v2_s7.png"]:
    p = os.path.join(folder,n)
    im = Image.open(p).convert("RGB")
    w,h = im.size
    small = im.resize((160, int(160*h/w)))
    cnt = collections.Counter(small.getdata())
    top = cnt.most_common(12)
    print(f"\n== {n}  {w}x{h} ==")
    for rgb,c in top:
        print(f"  #{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}  x{c}")
