# Detect genuinely-empty (near-pure-black) rectangular regions on each rendered slide,
# so overlay content can be placed in-place without covering existing elements.
# Pure black #000000 = slide background; dark panels (#16152B) are NOT treated as empty.
from PIL import Image
import numpy as np, os

prev = r"C:\Users\Dell\Documents\deepseek-harness\default-workspace\ppt_work\preview"
SW, SH = 20.0, 11.25           # slide inches
CW, CH = 1920, 1080            # content rectangle inside the rendered png (per manifest)

def largest_empty_rects(mask, grid=48, min_cells=2):
    # mask: HxW bool, True = empty. Downsample to grid cells, mark cell empty if >95% empty.
    H, W = mask.shape
    gy = H // grid; gx = W // grid
    cell_empty = np.zeros((grid, grid), bool)
    for j in range(grid):
        for i in range(grid):
            sub = mask[j*gy:(j+1)*gy, i*gx:(i+1)*gx]
            cell_empty[j, i] = sub.mean() > 0.985
    # find maximal all-empty rectangles (greedy: histogram-based largest rectangle, a few times)
    rects = []
    used = np.zeros_like(cell_empty)
    def area_rect(ce):
        # largest rectangle of True in boolean matrix -> returns (r0,c0,r1,c1,area)
        g = ce.shape[0]
        heights = [0]*ce.shape[1]
        best = (0,0,0,0,0)
        for r in range(ce.shape[0]):
            for c in range(ce.shape[1]):
                heights[c] = heights[c]+1 if ce[r,c] else 0
            # largest rectangle in histogram
            stack=[]; 
            for c in range(ce.shape[1]+1):
                h = heights[c] if c < ce.shape[1] else 0
                start=c
                while stack and stack[-1][1] > h:
                    s,hh = stack.pop()
                    a = hh*(c-s)
                    if a > best[4]:
                        best = (r-hh+1, s, r, c-1, a)
                    start=s
                stack.append((start,h))
        return best
    ce = cell_empty.copy()
    for _ in range(4):
        r0,c0,r1,c1,a = area_rect(ce)
        if a < min_cells*min_cells: break
        rects.append((r0,c0,r1,c1,a))
        ce[r0:r1+1, c0:c1+1] = False
    out=[]
    for (r0,c0,r1,c1,a) in rects:
        x = c0/grid*SW; y = r0/grid*SH
        w = (c1-c0+1)/grid*SW; h=(r1-r0+1)/grid*SH
        out.append((round(x,2),round(y,2),round(w,2),round(h,2)))
    return out

for p in range(1,9):
    f = os.path.join(prev, f"page-{p:04d}.png")
    im = Image.open(f).convert("RGB")
    im = im.crop((0,0,CW,CH))
    a = np.asarray(im).astype(int)
    s = a.sum(axis=2)
    empty = s < 24          # near pure black
    frac = empty.mean()
    rects = largest_empty_rects(empty)
    print(f"SLIDE {p}: pure-black bg = {frac*100:.0f}% | safe-empty rects (x,y,w,h in inches):")
    for r in rects:
        if r[2]*r[3] > 1.5:   # at least 1.5 sq inch
            print(f"    {r}  area={round(r[2]*r[3],1)} sq-in")
