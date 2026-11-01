"""Build exports/kaggle_notebooks/TRINETRA_Z_FINAL.ipynb: ONE CPU notebook that turns every attached run into TRINETRA_FINAL.zip.

The notebook embeds (base64 zip) the code it needs: trinetra/src + kaggle/ + configs, tools/make_figures.py, the repo's
results/ (fallbacks: geo, GLOF, RL env, Geo-PINN, fire_meta, offline RL) and the docs (Hinglish book + physics from zero).
Run from the repo root:  python TRINETRA/trinetra/kaggle/make_final_notebook.py
"""
import base64
import io
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TRI = ROOT / "TRINETRA"
OUT = TRI / "exports" / "kaggle_notebooks" / "TRINETRA_Z_FINAL.ipynb"
INCLUDE = ["TRINETRA/trinetra/src", "TRINETRA/trinetra/kaggle", "TRINETRA/trinetra/configs", "TRINETRA/data_adapters",
           "TRINETRA/results", "TRINETRA/docs/19_TRINETRA_EXPLAINED", "TRINETRA/docs/20_FINAL", "TRINETRA/FINAL_REPORT.md", "TRINETRA/TRINETRA_MetaFusion_Design.md",
           "TRINETRA/ASSUMPTIONS.md", "TRINETRA/REFERENCES.md", "tools/make_figures.py"]
SKIP_PARTS = {"__pycache__", "figures"}          # figures are rebuilt by the notebook
SKIP_SUFFIX = {".pt", ".pyc"}


def code_zip():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for inc in INCLUDE:
            p = ROOT / inc
            files = [p] if p.is_file() else sorted(f for f in p.rglob("*") if f.is_file())
            for f in files:
                rel = f.relative_to(ROOT)
                if SKIP_PARTS & set(rel.parts[:-1]) and "PHYSICS_FROM_ZERO" not in rel.parts or f.suffix in SKIP_SUFFIX:
                    continue
                z.write(f, rel.as_posix())
    return buf.getvalue()


def cell(kind, src):
    c = {"cell_type": kind, "metadata": {}, "source": src.strip("\n").splitlines(True)}
    if kind == "code":
        c.update(outputs=[], execution_count=None)
    return c


MD = """
# TRINETRA · Account Z · FINAL MERGE (sab runs → ek output)
**Kya karta hai (CPU, ~5–10 min):** har attached run (A B C D F P X S) se ek hi `TRINETRA_FINAL.zip` banata hai:
1. **Fire META-FUSION** dobara, attached runs par (fire_cnn + zeroshot + clip_probe + colorhist, REAL pairing, 3 seeds). Wo source
   chuna jaata hai jiske OOF **aur** held-out rows A ke same images hon; warna repo ka `results/fire_meta` use hota hai (log me likha aata hai).
2. **MASTER MERGE**: ek phase per account (final > phase2), duplicate reports hatake → `MASTER_RESULTS.md`, `RESULTS.md`, `master.json`.
   Landslide meta-fusion (geo) P ke run se aata hai.
3. **SAARE GRAPHS**: R0 (har ROC-AUC ek jagah) … R6 results, R7–R9 cross-modal + stress (X / S attached hon to), aur 10 physics graphs
   repo ke apne functions se.
4. **DOCS**: Hinglish book + `PHYSICS_FROM_ZERO` (derivations) + final report.
5. `FINAL_README.md` (index + scorecard + build log), `DETAILS_ALL_COMPARES.md` (har comparison table), `GRAPHS_EXPLAINED.md`
   (~30 graphs, har ek ki Hinglish explanation), `docs/20_FINAL/` (DATASETS_USED.csv/.tsv, landslide features CSV/TSV,
   CODE_AND_INTEGRATION_HINGLISH.md).
6. **Frontend me daalna:** zip download karke repo root par `python3 tools/import_final.py TRINETRA_FINAL.zip` → console ke About modal me
   naya scorecard + graphs gallery.

**Kaise chalayein:** right panel → **Add Input → Your Work / Notebook Output** → finished runs chuno: A final, B final, C final, D v2,
F final, P final, X final, S final (jo bhi khatam hue hain; jo missing hai wo `FINAL_README.md` me "missing" likha aayega).
`happyparsi/trinetra-dataset` attach karna **zaroori nahi**. GPU **nahi** chahiye, Internet **nahi** chahiye.
→ **Save Version → Save & Run All**. Output: `/kaggle/working/TRINETRA_FINAL.zip` (→ download / AI ko bhejo).

Purane `.zip` downloads bhi chalte hain: unhe ek private dataset me upload karke attach karo (`out_A_final.zip`, `out_B_final (1).zip` …).
Numbers = OUR RESULTS on the prototype pack.
"""

CFG = """
PREFER = None          # None = final beats phase2 per account | "phase2" = force phase2 runs
SEARCH = ["/kaggle/input", "/kaggle/working"]   # where out_<ACCOUNT>_<PHASE>.zip files are looked for (depth 4, team dataset skipped)
"""

RUN = """
import subprocess, sys, os, time
cmd = [sys.executable, "-u", "/kaggle/working/TRINETRA/trinetra/kaggle/final_bundle.py", "--search", *SEARCH,
       "--out", "/kaggle/working/FINAL"] + (["--prefer", PREFER] if PREFER else [])
print("$", " ".join(cmd), flush=True); t0 = time.time()
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, cwd="/kaggle/working")
for line in p.stdout:
    print(line, end="", flush=True)
rc = p.wait(); print(f"[time] final bundle: {(time.time() - t0) / 60:.1f} min · exit {rc}")
if rc != 0:
    raise SystemExit("final bundle failed: read the first [warn]/[skip]/Traceback above")
"""

SHOW = """
from IPython.display import Image, Markdown, display
import glob
print(open("/kaggle/working/FINAL/FINAL_README.md").read()[:6000])
for f in sorted(glob.glob("/kaggle/working/FINAL/figures/results/*.png")):
    print(f); display(Image(filename=f, width=900))
print("download: /kaggle/working/TRINETRA_FINAL.zip", round(os.path.getsize("/kaggle/working/TRINETRA_FINAL.zip") / 1e6, 1), "MB")
"""


def main():
    b64 = base64.b64encode(code_zip()).decode()
    embed = ("import base64, io, zipfile, os\n"
             f"_Z = '{b64}'\n"
             "zipfile.ZipFile(io.BytesIO(base64.b64decode(_Z))).extractall('/kaggle/working')\n"
             "print('embedded TRINETRA code + docs unpacked:', os.path.isdir('/kaggle/working/TRINETRA/trinetra/kaggle'))\n")
    nb = {"cells": [cell("markdown", MD), cell("code", CFG), cell("code", embed), cell("code", RUN), cell("code", SHOW)],
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python"}},
          "nbformat": 4, "nbformat_minor": 5}
    OUT.write_text(json.dumps(nb, indent=1))
    print(OUT, round(OUT.stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
