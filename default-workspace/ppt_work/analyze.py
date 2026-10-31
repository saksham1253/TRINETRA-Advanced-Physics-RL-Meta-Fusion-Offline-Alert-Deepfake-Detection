import sys, json
from pptx import Presentation
from pptx.util import Emu

p = r"C:\Users\Dell\Documents\deepseek-harness\default-workspace\ppt_work\original.pptx"
prs = Presentation(p)

def emu_in(v):
    try: return round(Emu(v).inches, 2)
    except: return None

print("=== DECK ===")
print("slides:", len(prs.slides))
print("size (in):", emu_in(prs.slide_width), "x", emu_in(prs.slide_height))
print("layouts in master:", [l.name for l in prs.slide_layouts])

for i, slide in enumerate(prs.slides):
    print(f"\n===== SLIDE {i+1} | layout={slide.slide_layout.name} =====")
    for sh in slide.shapes:
        t = sh.shape_type
        info = f"  [{t}] name={sh.name!r}"
        try:
            info += f" pos=({emu_in(sh.left)},{emu_in(sh.top)}) size=({emu_in(sh.width)}x{emu_in(sh.height)})"
        except: pass
        print(info)
        if sh.has_text_frame:
            txt = "\n".join(para.text for para in sh.text_frame.paragraphs if para.text.strip())
            if txt.strip():
                for line in txt.splitlines():
                    print("      | " + line)
        if sh.has_table:
            tbl = sh.table
            print(f"      TABLE {len(tbl.rows)}x{len(tbl.columns)}")
            for r in tbl.rows:
                print("      || " + " | ".join(c.text for c in r.cells))
        if sh.has_chart:
            print("      CHART:", sh.chart.chart_type)
    # notes
    if slide.has_notes_slide:
        n = slide.notes_slide.notes_text_frame.text
        if n.strip():
            print("  NOTES:", n[:300])
