# -*- coding: utf-8 -*-
import sys
from pptx import Presentation
from pptx.util import Emu, Pt

p = Presentation(r"C:\Users\Dell\Documents\deepseek-harness\default-workspace\viz\ppt\original.pptx")
EMU=914400
print("SLIDE SIZE:", round(p.slide_width/EMU,3), "x", round(p.slide_height/EMU,3), "in")
print("SLIDE COUNT:", len(p.slides.__iter__.__self__._sldIdLst))
print("N SLIDES:", len(p.slides._sldIdLst))
def tnorm(s):
    return (s or "").replace("\n"," / ").strip()
for i, s in enumerate(p.slides, 1):
    print("\n==================== SLIDE", i, "layout:", s.slide_layout.name, "====================")
    for sh in s.shapes:
        try:
            l=round(sh.left/EMU,2) if sh.left is not None else None
            t=round(sh.top/EMU,2) if sh.top is not None else None
            w=round(sh.width/EMU,2) if sh.width is not None else None
            h=round(sh.height/EMU,2) if sh.height is not None else None
        except Exception:
            l=t=w=h=None
        kind = sh.shape_type
        info = f"  [{sh.shape_id}] {kind} name='{sh.name}' pos=({l},{t}) size=({w},{h})"
        print(info)
        if sh.has_text_frame and sh.text_frame.text.strip():
            txt = tnorm(sh.text_frame.text)
            if len(txt)>240: txt=txt[:240]+"..."
            # font of first run
            fsz=None; col=None; bold=None; fname=None
            for para in sh.text_frame.paragraphs:
                for r in para.runs:
                    if r.text.strip():
                        fsz = r.font.size.pt if r.font.size else None
                        bold = r.font.bold
                        fname = r.font.name
                        try: col = str(r.font.color.rgb) if r.font.color and r.font.color.type is not None else None
                        except Exception: col=None
                        break
                if fsz is not None: break
            print(f"      TEXT: {txt}")
            print(f"      font: size={fsz} bold={bold} name={fname} color={col}")
        if sh.shape_type==13 or 'Picture' in str(kind):
            try: print(f"      IMAGE: {sh.image.content_type} {sh.image.size}")
            except Exception: pass
