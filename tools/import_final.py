"""Put TRINETRA_FINAL.zip (from the Z notebook / final_bundle.py) into the frontend.

  master/master.json, MASTER_RESULTS.md, RESULTS.md, results.json -> TRINETRA/results/master_merged/   (About modal table)
  figures/**.png                                                  -> public/results/figures/            (About modal gallery)
  figures/figures.json (title + Hinglish explanation per graph)   -> src/console/data/final_figures.json
  GRAPHS_EXPLAINED.md, FINAL_README.md, DETAILS_ALL_COMPARES.md   -> TRINETRA/results/final/
Run: python3 tools/import_final.py TRINETRA_FINAL.zip      (or a FINAL/ folder)
"""
import json, shutil, sys, tempfile, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = Path(sys.argv[1] if len(sys.argv) > 1 else "TRINETRA_FINAL.zip")
tmp = None
if src.is_file():
    tmp = Path(tempfile.mkdtemp()); zipfile.ZipFile(src).extractall(tmp); src = tmp
mm = ROOT / "TRINETRA/results/master_merged"; mm.mkdir(parents=True, exist_ok=True)
for f in ("master.json", "MASTER_RESULTS.md", "RESULTS.md", "results.json"):
    if (src / "master" / f).exists():
        shutil.copy(src / "master" / f, mm / f)
fig = ROOT / "public/results/figures"
if fig.exists():
    shutil.rmtree(fig)
items = json.load(open(src / "figures/figures.json")) if (src / "figures/figures.json").exists() else []
for it in items:
    dst = fig / Path(it["file"]).relative_to("figures"); dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src / it["file"], dst); it["url"] = "results/" + it["file"]
json.dump(items, open(ROOT / "src/console/data/final_figures.json", "w"), indent=1, ensure_ascii=False)
fin = ROOT / "TRINETRA/results/final"; fin.mkdir(parents=True, exist_ok=True)
for f in ("GRAPHS_EXPLAINED.md", "FINAL_README.md", "DETAILS_ALL_COMPARES.md"):
    if (src / f).exists():
        shutil.copy(src / f, fin / f)
if tmp:
    shutil.rmtree(tmp)
print(f"imported: master -> {mm.relative_to(ROOT)}, {len(items)} graphs -> {fig.relative_to(ROOT)}, manifest -> src/console/data/final_figures.json")
