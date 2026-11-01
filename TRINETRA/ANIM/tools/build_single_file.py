"""Inline public/anim (index.html + app.js + data/*.js) into ONE offline HTML file:
TRINETRA/exports/TRINETRA_live_flow.html. Run after extract_animation_data.py. Stdlib only."""
import re
from pathlib import Path

WS = Path(__file__).resolve().parents[3]
A = WS / "public/anim"
OUT = WS / "TRINETRA/exports/TRINETRA_live_flow.html"
html = (A / "index.html").read_text(encoding="utf-8")


def inline(m):
    src = (A / m.group(1)).read_text(encoding="utf-8").replace("</script", "<\\/script")
    return f"<script>/* inlined {m.group(1)} */\n{src}\n</script>"


out = re.sub(r'<script src="([^"]+)"></script>', inline, html)
assert "<script src=" not in out
OUT.write_text(out, encoding="utf-8")
print(f"[single-file] {OUT.relative_to(WS)} ({OUT.stat().st_size / 1024:.0f} KB, no external requests)")
