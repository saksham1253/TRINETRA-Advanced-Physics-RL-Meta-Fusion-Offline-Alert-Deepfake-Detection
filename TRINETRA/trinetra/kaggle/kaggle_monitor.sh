#!/usr/bin/env bash
# Read-only Kaggle monitor (GET requests only). Usage: kaggle_monitor.sh <kernel-slug> [status|output]
# Needs KAGGLE_USERNAME / KAGGLE_KEY in the environment. Never prints the key.
set -euo pipefail
SLUG="${1:?kernel slug, e.g. trinetra-all-phase2}"; MODE="${2:-status}"
API="https://www.kaggle.com/api/v1/kernels"; AUTH="$KAGGLE_USERNAME:$KAGGLE_KEY"
case "$MODE" in
  status) curl -sS -m 60 -u "$AUTH" "$API/status?userName=$KAGGLE_USERNAME&kernelSlug=$SLUG"; echo ;;
  output)
    D="/tmp/kaggle_out/$SLUG"; mkdir -p "$D"
    curl -sS -m 120 -u "$AUTH" "$API/output?userName=$KAGGLE_USERNAME&kernelSlug=$SLUG" -o "$D/output.json"
    python3 - "$D" <<'PY'
import json, sys, subprocess, pathlib
d = pathlib.Path(sys.argv[1]); o = json.load(open(d / "output.json"))
(d / "log.txt").write_text(o.get("log") or o.get("logNullable") or "")
for f in o.get("files", []):
    name, url = f.get("fileName"), f.get("url")
    if name and url and (name.endswith((".md", ".json", ".log", ".csv", ".zip"))):
        tgt = d / name; tgt.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["curl", "-sS", "-m", "300", "-L", "-o", str(tgt), url])
        print("downloaded", name)
print("log ->", d / "log.txt")
PY
    ;;
  *) echo "mode: status|output"; exit 2 ;;
esac
