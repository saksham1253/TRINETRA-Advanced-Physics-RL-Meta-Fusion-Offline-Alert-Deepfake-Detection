#!/usr/bin/env bash
# Rebuild the CPU geo environment from scratch and finish the pending runs (RL C_miss 1000/5000 + Geo-PINN OOF).
# Every finished report is copied into TRINETRA/results/ immediately (sandbox resets wipe /tmp).
set -uo pipefail
W=/workspaces/default/code/TRINETRA; R=$W/results; T=/tmp/rec; mkdir -p $T $R/rl_env $R/geo_pinn
log(){ echo "[$(date +%H:%M:%S)] $*" | tee -a $R/recover.log; }
if [ ! -x /tmp/venv/bin/python ]; then
  python3 -m venv --without-pip /tmp/venv && curl -sS -m 60 -o $T/get-pip.py https://bootstrap.pypa.io/get-pip.py && /tmp/venv/bin/python $T/get-pip.py -q \
  && /tmp/venv/bin/python -m pip install -q numpy pandas tifffile imagecodecs && /tmp/venv/bin/python -m pip install -q torch --index-url https://download.pytorch.org/whl/cpu
fi
PY=/tmp/venv/bin/python; log "venv ok: $($PY -c 'import torch,numpy;print(torch.__version__)')"
for i in 1 2 3 4 5; do head -c 4000 $T/glc.csv 2>/dev/null | grep -q country_name && break
  curl -sSL -m 180 -A Mozilla/5.0 -o $T/glc.csv "https://data.nasa.gov/docs/legacy/Global_Landslide_Catalog_Export/Global_Landslide_Catalog_Export_rows.csv"; sleep 10; done
log "glc: $(wc -c < $T/glc.csv) bytes"
cd $W && $PY data_adapters/build_geo.py --glc $T/glc.csv --country India --bbox 29 33 76 81 --dem-dir $T/dem --cache $T/power --out $T/events >> $R/recover.log 2>&1
cmp -s <(cut -d, -f1-6 $T/events/geo_events.csv) <(cut -d, -f1-6 $R/geo_large/geo_events.csv) && log "events table IDENTICAL to results/geo_large" || log "WARNING events table differs from results/geo_large"
cd $W/trinetra
( OMP_NUM_THREADS=2 $PY kaggle/rl_env_eval.py --events $T/events/geo_events.csv --power-cache $T/power --out $T/rl1k --C-miss 1000 > $T/rl1k.log 2>&1; cp $T/rl1k/*_report.json $R/rl_env/ 2>/dev/null; log "rl C_miss=1000 done" ) &
( OMP_NUM_THREADS=2 $PY kaggle/rl_env_eval.py --events $T/events/geo_events.csv --power-cache $T/power --out $T/rl5k --C-miss 5000 > $T/rl5k.log 2>&1; cp $T/rl5k/*_report.json $R/rl_env/ 2>/dev/null; log "rl C_miss=5000 done" ) &
( OMP_NUM_THREADS=2 $PY kaggle/train_geo_pinn.py --data $T/events/geo.npz --out $T/pinn --epochs 100 --batch 32 --parallel none --D0 4.32 --beta_deg 40 > $T/pinn.log 2>&1; cp $T/pinn/*_report.json $T/pinn/*_oof.npz $R/geo_pinn/ 2>/dev/null; log "geo-pinn done" ) &
wait; log "ALL DONE"
