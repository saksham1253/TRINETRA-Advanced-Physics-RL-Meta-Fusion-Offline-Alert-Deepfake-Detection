# -*- coding: utf-8 -*-
"""Find large EMPTY background rectangles in each composited slide, in inch coords.
empty cell = low edge-density (no text/border/icon) AND dark (matches bg, not a light card)."""
import os, glob
from PIL import Image, ImageFilter

DIR = r"C:\Users\Dell\Documents\deepseek-harness\default-workspace\viz\ppt\composite"
SLIDE_W_IN, SLIDE_H_IN = 20.0, 11.25
COLS, ROWS = 48, 27
EDGE_T = 9.0      # mean edge below this = flat
LUM_T = 115       # mean luminance below this = dark/background (light cards are ~200+)

def largest_rect(mat, cols, rows):
    # largest all-True rectangle in boolean matrix (histogram method), returns (c0,r0,c1,r1,area_cells)
    heights = [0]*cols
    best = (0,0,0,0,0)
    for r in range(rows):
        for c in range(cols):
            heights[c] = heights[c]+1 if mat[r][c] else 0
        stack = []
        for c in range(cols+1):
            cur = heights[c] if c < cols else 0
            start = c
            while stack and stack[-1][1] > cur:
                s, h = stack.pop()
                area = h*(c-s)
                if area > best[4]:
                    best = (s, r-h+1, c-1, r, area)
                start = s
            stack.append((start, cur))
    return best

for png in sorted(glob.glob(os.path.join(DIR, 'page-*.png'))):
    n = int(os.path.basename(png).split('-')[1].split('.')[0])
    im = Image.open(png).convert('RGB')
    W, H = im.size
    lum = im.convert('L')
    edges = lum.filter(ImageFilter.FIND_EDGES)
    lpx = lum.load(); epx = edges.load()
    cw, ch = W/COLS, H/ROWS
    empty = [[False]*COLS for _ in range(ROWS)]
    content_cells = 0
    for rr in range(ROWS):
        for cc in range(COLS):
            x0,y0 = int(cc*cw), int(rr*ch); x1,y1 = int((cc+1)*cw), int((rr+1)*ch)
            es=ls=cnt=0
            for y in range(y0, y1, 4):
                for x in range(x0, x1, 4):
                    es += epx[x,y]; ls += lpx[x,y]; cnt += 1
            em, lm = es/cnt, ls/cnt
            is_empty = (em < EDGE_T) and (lm < LUM_T)
            empty[rr][cc] = is_empty
            if not is_empty: content_cells += 1
    fill = content_cells/(COLS*ROWS)
    print(f"\n=== Slide {n}  fill={fill*100:.0f}%  (empty rects >=1.6 sq-in) ===")
    rects = []
    work = [row[:] for row in empty]
    for _ in range(4):
        c0,r0,c1,r1,area = largest_rect(work, COLS, ROWS)
        if area == 0: break
        x_in = c0/COLS*SLIDE_W_IN; y_in = r0/ROWS*SLIDE_H_IN
        w_in = (c1-c0+1)/COLS*SLIDE_W_IN; h_in = (r1-r0+1)/ROWS*SLIDE_H_IN
        if w_in*h_in < 1.6: break
        print(f"  empty box: x={x_in:.2f} y={y_in:.2f} w={w_in:.2f} h={h_in:.2f}  ({w_in*h_in:.1f} sq-in)")
        for r in range(r0, r1+1):
            for c in range(c0, c1+1):
                work[r][c] = False
