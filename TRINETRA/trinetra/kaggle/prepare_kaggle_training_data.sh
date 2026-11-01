#!/usr/bin/env bash
# One-command ZIP/folder -> code-ready NPZ conversion. Does not train models.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"
IN="${1:-${KAGGLE_INPUT:-/kaggle/input}}"
WORK="${WORK:-/kaggle/working/trinetra_stage}"
DATA="${DATA:-/kaggle/working/npz}"
OUT="${OUT:-/kaggle/working/out}"
PY="${PY:-python}"
ENV_FILE="$WORK/dataset_env.sh"; INVENTORY="$WORK/dataset_inventory.json"
mkdir -p "$WORK" "$DATA" "$OUT/manifests"

$PY "$ROOT/data_adapters/stage_kaggle_archives.py" \
  --input "$IN" --work "$WORK" --env-out "$ENV_FILE" --report "$INVENTORY" \
  --max-archive-gb "${MAX_ARCHIVE_GB:-12}" --max-total-gb "${MAX_TOTAL_GB:-40}" \
  --skip-regex "${STAGE_SKIP_REGEX:-}"
# shellcheck disable=SC1090
source "$ENV_FILE"

missing=()
CORE="DFIRE DEEPFIRE WEATHER CIFAKE"; [[ " ${BUILD_PARTS:-fire deepfake} " == *" deepfake "* ]] || CORE="DFIRE DEEPFIRE WEATHER"
for key in $CORE; do
  [ -n "${!key:-}" ] || missing+=("$key")
done
[ "${#missing[@]}" -eq 0 ] || echo "[warn] core roots not found (those parts will be skipped): ${missing[*]}"
KAGGLE_INPUT="$IN" DATA="$DATA" OUT="$OUT" PY="$PY" bash "$HERE/run_hackathon.sh" build || echo "[warn] build stage reported errors"

EO="$ROOT/data_adapters/build_eo.py"; EO_SIZE="${EO_SIZE:-64}"
if [[ " ${BUILD_PARTS:-fire deepfake eo} " != *" eo "* ]]; then
  echo "[prep] EO conversion skipped (BUILD_PARTS=${BUILD_PARTS})"; unset L4S S1F HEPH HEPH_ANN
fi
if [ -n "${L4S:-}${S1F:-}${HEPH:-}" ]; then
  $PY -c "import h5py, tifffile, PIL" 2>/dev/null || \
    $PY -m pip install -q h5py tifffile imagecodecs pillow
fi
if [ -n "${L4S:-}" ]; then
  $PY "$EO" l4s --root "$L4S" --out "$DATA/l4s.npz" --size "$EO_SIZE" --max-n "${EO_L4S_N:-512}"
fi
if [ -n "${S1F:-}" ]; then
  $PY "$EO" sen1floods11 --root "$S1F" --out "$DATA/s1f.npz" --size "$EO_SIZE" \
    --max-n "${EO_S1_N:-400}" --holdout-event Bolivia
fi
if [ -n "${HEPH:-}" ] && [ -n "${HEPH_ANN:-}" ]; then
  $PY "$EO" hephaestus --root "$HEPH" --annotations "$HEPH_ANN" --out "$DATA/heph.npz" \
    --size "$EO_SIZE" --max-n "${EO_HEPH_N:-512}"
elif [ -n "${HEPH:-}" ]; then
  echo "[warn] Hephaestus images found but annotations missing; skipped to avoid frameID leakage"
fi

$PY "$ROOT/data_adapters/validate_ready_pack.py" --data "$DATA" --report "$WORK/ready_pack_report.json"
echo "[done] NPZ=$DATA inventory=$INVENTORY validation=$WORK/ready_pack_report.json"
echo "[next] publish $DATA + validation report as a private Kaggle Dataset for the training accounts"
