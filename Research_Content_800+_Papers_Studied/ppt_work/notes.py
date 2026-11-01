import sys
from pptx import Presentation
p = r"C:\Users\Dell\Documents\deepseek-harness\default-workspace\ppt_work\original.pptx"
prs = Presentation(p)
for i, slide in enumerate(prs.slides):
    print(f"\n########## SLIDE {i+1} NOTES ##########")
    if slide.has_notes_slide:
        print(slide.notes_slide.notes_text_frame.text)
    else:
        print("(no notes)")
