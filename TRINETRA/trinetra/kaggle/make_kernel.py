"""Build a self-contained Kaggle kernel push payload: runner notebook + embedded code zip (no code dataset needed)."""
import argparse, base64, json
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--user", required=True); ap.add_argument("--slug", default="trinetra-runner")
ap.add_argument("--account", default="ALL"); ap.add_argument("--phase", default="phase2")
ap.add_argument("--code-zip", default="exports/trinetra_code.zip"); ap.add_argument("--out", default="/tmp/kernel_push.json")
a = ap.parse_args()
nb = json.load(open(Path(__file__).with_name("TRINETRA_kaggle_runner.ipynb")))
for c in nb["cells"]:
    s = "".join(c["source"])
    if s.startswith("ACCOUNT ="):
        s = s.replace('ACCOUNT = "A"', f'ACCOUNT = "{a.account}"').replace('PHASE   = "phase2"', f'PHASE   = "{a.phase}"')
        c["source"] = s.splitlines(True)
b64 = base64.b64encode(Path(a.code_zip).read_bytes()).decode()
embed = ("import base64, io, zipfile, os\n"
         f"_Z = '{b64}'\n"
         "zipfile.ZipFile(io.BytesIO(base64.b64decode(_Z))).extractall('/kaggle/working')\n"
         "print('embedded TRINETRA code unpacked:', os.path.isdir('/kaggle/working/TRINETRA/trinetra/kaggle'))\n")
nb["cells"].insert(2, {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None, "source": embed.splitlines(True)})
payload = {"slug": f"{a.user}/{a.slug}", "newTitle": a.slug.replace("-", " ").title(), "text": json.dumps(nb),
           "language": "python", "kernelType": "notebook", "isPrivate": True, "enableGpu": True, "enableTpu": False,
           "enableInternet": True, "datasetDataSources": ["happyparsi/trinetra-dataset"], "competitionDataSources": [],
           "kernelDataSources": [], "modelDataSources": [], "categoryIds": []}
json.dump(payload, open(a.out, "w"))
print("payload", a.out, round(len(payload["text"]) / 1e6, 2), "MB notebook")
