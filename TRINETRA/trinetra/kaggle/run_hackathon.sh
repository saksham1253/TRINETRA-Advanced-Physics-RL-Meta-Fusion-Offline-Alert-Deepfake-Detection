#!/usr/bin/env bash
# One-command hackathon pipeline (IoT = future work). Run inside a Kaggle notebook cell:
#   !bash /kaggle/working/TRINETRA/trinetra/kaggle/run_hackathon.sh <STAGE>
# STAGES (each account runs its own; artifacts go to $OUT, publish $OUT as a private Kaggle Dataset):
#   smoke     : 5-minute check of the whole chain on SYNTHETIC data (no datasets needed)
#   build     : build .npz subsets from attached datasets (CPU is enough)       [Acct A]
#   fire      : fire CNN, seeds 0-2, + colour baseline, held-out DeepFire test  [Acct A, GPU]
#   zeroshot  : open_clip zero-shot on the same npz + held-out                  [Acct B, GPU, internet ON]
#   video     : FireSense videos, raw vs temporal-validated alarms (after fire)  [Acct A, GPU]
#   stress    : confuser-aware probe + stack, leave-one-confuser-set-out [Acct S, after crossmodal]
#   crossmodal: per-frame / per-confuser stack of fire_cnn + zeroshot + clip_probe + temporal validator [Acct X, after fire+zeroshot]
#   deepfake  : AuthenticityNet on CIFAKE, held-out StyleGAN faces + AI art     [Acct C, GPU]
#   geo       : REAL landslide physics hindcast + GLOF relations + RL environment + Geo-PINN  [any acct, CPU ok]
#   eo        : build + train Sentinel-2, Sentinel-1 and InSAR EO heads [GPU]
#   eo-train  : train EO heads from an already-converted shared NPZ pack [GPU]
#   physics   : physics golden tests + geo physics (hindcast, GLOF, RL env, Geo-PINN) for every seed [CPU ok]
#   fuse      : fusion cache + FM-1/PHARAOH/median/max comparison + RL logs + offline RL + results  [Acct D]
# Paths below are DEFAULTS for the Kaggle slugs in docs/09b. Override with env vars if folder names differ.
set -euo pipefail
STAGE="${1:-smoke}"
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"   # ROOT = TRINETRA/
OUT="${OUT:-/kaggle/working/out}"; DATA="${DATA:-/kaggle/working/npz}"; IN="${KAGGLE_INPUT:-/kaggle/input}"
SEEDS="${SEEDS:-0 1 2}"; EPOCHS="${EPOCHS:-15}"; SIZE="${SIZE:-128}"
PY="${PY:-python}"
mkdir -p "$OUT" "$DATA"
A="$ROOT/data_adapters/build_npz.py"

case "$STAGE" in
smoke)
  $PY "$HERE/smoke_test_all.py" ;;
build)
  # Folder names below were VERIFIED with the Kaggle file-list API on 2026-10-31 (docs/09d_DATASET_LAYOUTS.md).
  # Every dataset is optional here: a missing or broken one is logged and the rest still convert.
  # ---- fire: D-Fire main (classes read from its data.yaml; AoF camera frames grouped in buckets of 50)
  mkdir -p "$OUT/manifests"
  { $PY "$A" yolo --root "${DFIRE:-$IN/smoke-fire-detection-yolo}" --classes auto --seq-bucket 50 --task fire --size "$SIZE" \
      --max-images "${DFIRE_N:-4000}" --out "$DATA/dfire_all.npz" --manifest "$OUT/manifests/dfire_seed0.csv" && \
    $PY "$A" subset --npz "$DATA/dfire_all.npz" --keep train val --out "$DATA/fire.npz" && \
    $PY "$A" subset --npz "$DATA/dfire_all.npz" --keep test --out "$DATA/fire_test_same_source.npz"; } || echo "[warn] D-Fire skipped"
  # held-out sets are deduped against D-Fire when it exists; otherwise kept raw (and the report says so)
  heldout() {  # heldout <raw.npz> <final.npz>
    if [ -f "$DATA/dfire_all.npz" ]; then $PY "$A" dedupe --train "$DATA/dfire_all.npz" --test "$1" --out "$2"; else cp "$1" "$2"; echo "[warn] $2 NOT deduped (no D-Fire)"; fi
  }
  # ---- held-out 1: DeepFire forest (Training/fire, Training/nofire), deduped against D-Fire
  { $PY "$A" folder --root "${DEEPFIRE:-$IN/forest-fire-dataset}" --map Training/fire=fire Training/nofire=none \
      --task fire --size "$SIZE" --max-per-class 760 --out "$DATA/deepfire_raw.npz" --manifest "$OUT/manifests/deepfire_seed0.csv" && \
    heldout "$DATA/deepfire_raw.npz" "$DATA/deepfire.npz"; } || echo "[warn] DeepFire skipped"
  # ---- held-out 2 (optional): FIRE Dataset outdoor web photos, deduped
  $PY "$A" folder --root "${FIREDS:-$IN/fire-dataset}" --map fire_images=fire non_fire_images=none --task fire --size "$SIZE" \
      --max-per-class 755 --out "$DATA/firedataset_raw.npz" && \
  heldout "$DATA/firedataset_raw.npz" "$DATA/heldout_firedataset.npz" || echo "[warn] FIRE Dataset skipped"
  # ---- held-out 3 (optional): indoor home fire (YOLO; needs its data.yaml or set HOMEFIRE_CLASSES="0=fire 1=smoke")
  $PY "$A" yolo --root "${HOMEFIRE:-$IN/home-fire-dataset}" --classes ${HOMEFIRE_CLASSES:-auto} --task fire --size "$SIZE" \
      --max-images 1500 --out "$DATA/heldout_homefire.npz" || echo "[warn] home-fire skipped"
  # ---- confusers (NOT fire): weather, benign small flames (candle/lighter/match), normal scenes
  $PY "$A" folder --root "${WEATHER:-$IN/weather-dataset}" --map fogsmog=none sandstorm=none lightning=none rain=none \
      --task fire --size "$SIZE" --max-per-class 250 --out "$DATA/stress_weather.npz" || echo "[warn] weather skipped"
  $PY "$A" folder --root "${CANDLE:-$IN/flame-dataset-candlelightermatch-stick-flames}" --map Flame/train/images=none \
      --seq-bucket 50 --task fire --size "$SIZE" --max-per-class 600 --out "$DATA/stress_small_flames.npz" || echo "[warn] candle set skipped"
  $PY "$A" folder --root "${SCENES:-$IN/intel-image-classification-dataset}" --map street=none buildings=none forest=none mountain=none \
      --task fire --size "$SIZE" --max-per-class 200 --out "$DATA/stress_scenes.npz" || echo "[warn] intel scenes skipped"
  # ---- video: FireSense (49 .avi), one frame every 10, for kaggle/eval_video.py
  $PY "$A" video --root "${FIRESENSE:-$IN/firesense}" --map fire/pos=fire fire/neg=none smoke/pos=smoke smoke/neg=none \
      --clip 1 --every 10 --size "$SIZE" --out "$DATA/firesense_frames.npz" || echo "[warn] FireSense skipped"
  # ---- deepfake (skipped when BUILD_PARTS excludes it, e.g. account A only needs the fire sets)
  if [[ " ${BUILD_PARTS:-fire deepfake} " == *" deepfake "* ]]; then
    $PY "$A" folder --root "${CIFAKE:-$IN/cifake-real-and-ai-generated-synthetic-images}" --map REAL=real FAKE=fake \
        --task deepfake --size 32 --max-per-class "${CIFAKE_N:-10000}" --out "$DATA/media.npz" || echo "[warn] CIFAKE skipped"
    $PY "$A" folder --root "${FACES:-$IN/deepfake-face-images}" --map "Final Dataset/Real=real" "Final Dataset/Fake=fake" \
        --task deepfake --size 32 --max-per-class 1000 --out "$DATA/faces_test.npz" || echo "[warn] faces skipped"
    $PY "$A" folder --root "${AIART:-$IN/ai-generated-images-vs-real-images}" --map AiArtData=fake RealArt=real \
        --task deepfake --size 32 --max-per-class 540 --out "$DATA/aiart_test.npz" || echo "[warn] AI-art skipped"
  else echo "[build] deepfake sets skipped (BUILD_PARTS=${BUILD_PARTS})"; fi
  for f in "$DATA"/*.npz; do [ -f "$f" ] && { $PY "$A" check --npz "$f" || true; }; done ;;
fire)
  [ -f "$DATA/fire.npz" ] || { echo "[error] $DATA/fire.npz missing (D-Fire not converted)"; exit 4; }
  FT=""; [ -f "$DATA/deepfire.npz" ] && FT="--test $DATA/deepfire.npz"
  for s in $SEEDS; do
    ST=""; for f in stress_weather stress_small_flames stress_scenes heldout_firedataset heldout_homefire fire_test_same_source; do
      [ -f "$DATA/$f.npz" ] && ST="$ST $DATA/$f.npz"; done
    $PY "$HERE/train_classifier.py" --model fire --target any --data "$DATA/fire.npz" $FT \
        --stress $ST --out "$OUT/fire" --epochs "$EPOCHS" --seed "$s"
    $PY "$HERE/baseline_colorhist.py" --data "$DATA/fire.npz" --target any --out "$OUT/colorhist" --seed "$s"
  done ;;
zeroshot)
  pip -q install open_clip_torch
  ST=""; for f in stress_weather stress_small_flames stress_scenes heldout_firedataset heldout_homefire; do
    [ -f "$DATA/$f.npz" ] && ST="$ST $DATA/$f.npz"; done
  ZT=""; [ -f "$DATA/deepfire.npz" ] && ZT="--test $DATA/deepfire.npz"
  # v2: ViT-L-14 + concept prompts + calibrated gate; ZS_PROBE=1 also trains the few-shot CLIP probe (own expert)
  PR=""; [ "${ZS_PROBE:-1}" = "1" ] && PR="--probe --probe-out $OUT/clip_probe"
  VD=""; [ -f "$DATA/firesense_frames.npz" ] && VD="--video $DATA/firesense_frames.npz"
  $PY "$HERE/eval_zeroshot.py" --data "$DATA/fire.npz" $ZT --target any --stress $ST $VD --out "$OUT/zeroshot" \
      --model "${ZS_MODEL:-ViT-L-14}" --pretrained "${ZS_PRETRAINED:-laion2b_s32b_b82k}" --prompts "${ZS_PROMPTS:-v2}" $PR ;;
video)
  # after `fire`: raw per-frame alarms vs temporal validator on FireSense videos
  for s in $SEEDS; do $PY "$HERE/eval_video.py" --frames "$DATA/firesense_frames.npz" --models "$OUT/fire" --seed "$s" --out "$OUT/video"; done ;;
crossmodal)
  # after `fire` (or attached A output in $FIRE_MODELS) and `zeroshot`: stack fire_cnn + zeroshot + clip_probe per frame /
  # per confuser image, then temporal validator per expert and for the stack (kaggle/crossmodal_fusion.py)
  FM="${FIRE_MODELS:-$OUT/fire}"
  ST=""; for f in stress_weather stress_small_flames stress_scenes heldout_firedataset heldout_homefire; do
    [ -f "$DATA/$f.npz" ] && ST="$ST $DATA/$f.npz"; done
  for s in $SEEDS; do
    $PY "$HERE/crossmodal_fusion.py" --fire-models "$FM" --zs-dir "$OUT/zeroshot" --clip-dir "$OUT/clip_probe" \
        --frames "$DATA/firesense_frames.npz" --stress $ST --seed "$s" --out "$OUT/crossmodal"
  done ;;
stress)
  # after crossmodal (account S): confuser-aware probe + stack, leave-one-confuser-set-out (kaggle/stress_train.py)
  pip -q install open_clip_torch
  FM="${FIRE_MODELS:-$OUT/fire}"
  ST=""; for f in stress_weather stress_small_flames stress_scenes; do [ -f "$DATA/$f.npz" ] && ST="$ST $DATA/$f.npz"; done
  HO=""; for f in heldout_firedataset heldout_homefire; do [ -f "$DATA/$f.npz" ] && HO="$HO $DATA/$f.npz"; done
  TT=""; [ -f "$DATA/deepfire.npz" ] && TT="--test $DATA/deepfire.npz"
  for s in $SEEDS; do
    $PY "$HERE/stress_train.py" --data "$DATA/fire.npz" $TT --stress $ST --heldout $HO --fire-models "$FM" --out "$OUT/stress" --seed "$s" \
        --model "${ZS_MODEL:-ViT-L-14}" --pretrained "${ZS_PRETRAINED:-laion2b_s32b_b82k}" --neg-weight "${NEG_WEIGHT:-1.0}"
  done ;;
deepfake)
  for s in $SEEDS; do
    T=""; [ -f "$DATA/faces_test.npz" ] && T="--test $DATA/faces_test.npz"
    S=""; [ -f "$DATA/aiart_test.npz" ] && S="--stress $DATA/aiart_test.npz"
    $PY "$HERE/train_classifier.py" --model deepfake --data "$DATA/media.npz" $T $S --out "$OUT/deepfake" --epochs "$EPOCHS" --seed "$s"
  done ;;
fuse)
  ZS=""; [ -f "$OUT/zeroshot/zeroshot_s0_oof.npz" ] && ZS="--zeroshot $OUT/zeroshot/zeroshot_s0_oof.npz"
  CH=""; [ -z "$ZS" ] && CH="--colorhist $OUT/colorhist/colorhist_s0_oof.npz"
  DF=""; [ -f "$OUT/deepfake/deepfake_s0_oof.npz" ] && DF="--deepfake $OUT/deepfake/deepfake_s0_oof.npz --fake-frac ${FAKE_FRAC:-0.1}"
  $PY "$HERE/build_fusion_cache.py" --fire "$OUT/fire/fire_s0_oof.npz" $ZS $CH $DF --out "$OUT/fusion"
  $PY "$HERE/train_fusion_head.py" --data "$OUT/fusion/fusion_cache.npz" --out "$OUT/fusion"
  $PY "$ROOT/data_adapters/make_rl_logs.py" --inp "$OUT/fusion/fusion_cache.npz" --out "$OUT/rl/logs.npz"
  for s in $SEEDS; do $PY "$HERE/train_offline_rl.py" --data "$OUT/rl/logs.npz" --out "$OUT/rl" --seed "$s"; done
  $PY "$HERE/collect_results.py" --inp "$OUT" --out "$OUT/results" ;;
geo)
  # REAL landslide physics + GLOF + RL environment (CPU is enough; internet ON for POWER / DEM / GLC downloads)
  pip -q install tifffile imagecodecs
  G="$OUT/geo"; mkdir -p "$G"
  # BUGFIX (B-31): a NASA 522 error page (16 bytes) was saved as the CSV. Validate, retry 3x, then fall back to the Kaggle
  # mirror (attach kazushiadachi/global-landslide-data, US Gov works) if NASA is down.
  good_glc() { [ -f "$1" ] && head -c 4000 "$1" | grep -q country_name; }
  [ -n "${GLC_CSV:-}" ] && [ -f "$GLC_CSV" ] && cp "$GLC_CSV" "$G/glc.csv"
  for i in 1 2 3; do
    good_glc "$G/glc.csv" && break
    curl -sSL -A Mozilla/5.0 -o "$G/glc.csv" "https://data.nasa.gov/docs/legacy/Global_Landslide_Catalog_Export/Global_Landslide_Catalog_Export_rows.csv" || true
    good_glc "$G/glc.csv" || sleep $((i * 10))
  done
  if ! good_glc "$G/glc.csv"; then
    M="$(ls ${IN}/global-landslide-data/*.csv 2>/dev/null | head -1)"
    [ -n "$M" ] && cp "$M" "$G/glc.csv" || { echo "[error] GLC unavailable: attach Kaggle dataset kazushiadachi/global-landslide-data"; exit 3; }
  fi
  [ -n "${GLOF_CSV:-}" ] && [ -f "$GLOF_CSV" ] && cp "$GLOF_CSV" "$G/hmaglofdb_v4.csv"
  [ -f "$G/hmaglofdb_v4.csv" ] || curl -sSL -o "$G/hmaglofdb_v4.csv" "https://raw.githubusercontent.com/prazg/GLOF_dashboard/main/data/raw/HMAGLOFDB_v4_0_13122025.csv"
  $PY "$ROOT/data_adapters/build_geo.py" --glc "$G/glc.csv" --country India --bbox ${GEO_BBOX:-29 33 76 81} \
      --dem-dir "$G/dem" --cache "$G/power_cache" --out "$G/events"
  for s in ${GEO_SEEDS:-0}; do $PY "$HERE/geo_physics_hindcast.py" --events "$G/events/geo_events.csv" --out "$G/hindcast" --seed "$s"; done
  $PY "$HERE/glof_physics_check.py" --csv "$G/hmaglofdb_v4.csv" --out "$G/glof"
  for cm in 100 1000 5000; do
    $PY "$HERE/rl_env_eval.py" --events "$G/events/geo_events.csv" --power-cache "$G/power_cache" --out "$G/rl_env" --C-miss $cm
  done
  for s in ${GEO_SEEDS:-0}; do
    $PY "$HERE/train_geo_pinn.py" --data "$G/events/geo.npz" --out "$G/pinn" --epochs "${PINN_EPOCHS:-100}" --batch 32 --parallel none --D0 4.32 --beta_deg 40 --seed "$s"
  done
  # META-FUSION on REAL paired rows (HLD: experts + physics consistency + FM-1 averaging + U* + shield), every seed
  for s in ${GEO_SEEDS:-0}; do
    $PY "$HERE/geo_meta_fusion.py" --events "$G/events/geo_events.csv" --pinn "$G/pinn/geo_pinn_s${s}_oof.npz" --out "$G/fusion" --seed "$s" \
      || echo "[warn] geo meta-fusion seed $s failed"
  done
  $PY "$HERE/collect_results.py" --inp "$OUT" --out "$OUT/results" ;;
physics)
  # 7 physics models: golden tests (FS, Iverson, Caine, Fukuzono, gates, fire physics), then real-data geo physics
  # (hindcast + GLOF fits + RL simulator + trained Geo-PINN) for every seed in $SEEDS. CPU is enough; internet ON.
  mkdir -p "$OUT/physics_tests"
  (cd "$ROOT/trinetra" && $PY run_tests.py "test_*.py") 2>&1 | tee "$OUT/physics_tests/unit_tests.log" || echo "[warn] some unit tests failed (see log)"
  GEO_SEEDS="$SEEDS" bash "$0" geo ;;
eo-train)
  built=0
  if [ -f "$DATA/l4s.npz" ]; then
    for s in $SEEDS; do
      $PY "$HERE/train_classifier.py" --model eo --data "$DATA/l4s.npz" --out "$OUT/eo_l4s" --epochs "$EPOCHS" --seed "$s"
    done
    built=1
  fi
  if [ -f "$DATA/s1f.npz" ]; then
    TEST=""; [ -f "$DATA/s1f_Bolivia_test.npz" ] && TEST="--test $DATA/s1f_Bolivia_test.npz"
    for s in $SEEDS; do
      $PY "$HERE/train_classifier.py" --model eo --data "$DATA/s1f.npz" $TEST --out "$OUT/eo_s1f" --epochs "$EPOCHS" --seed "$s"
    done
    built=1
  fi
  if [ -f "$DATA/heph.npz" ]; then
    for s in $SEEDS; do
      $PY "$HERE/train_classifier.py" --model eo --data "$DATA/heph.npz" --out "$OUT/eo_heph" --epochs "$EPOCHS" --seed "$s"
    done
    built=1
  fi
  [ "$built" -eq 1 ] || { echo "[error] no EO NPZ files in $DATA"; exit 4; }
  ;;
eo)
  # Small EO prototype pack by default (~150 MiB after conversion at 64 px).
  # Raise EO_*_N only for a later full-scale run; grouped splits and Bolivia holdout stay unchanged.
  pip -q install timm tifffile imagecodecs h5py
  E="$ROOT/data_adapters/build_eo.py"
  EO_SIZE="${EO_SIZE:-64}"; EO_L4S_N="${EO_L4S_N:-512}"; EO_S1_N="${EO_S1_N:-400}"; EO_HEPH_N="${EO_HEPH_N:-512}"
  $PY "$E" l4s --root "${L4S:-$IN/landslide4sense}" --out "$DATA/l4s.npz" \
    --size "$EO_SIZE" --max-n "$EO_L4S_N" && \
    $PY "$HERE/train_classifier.py" --model eo --data "$DATA/l4s.npz" --out "$OUT/eo_l4s" --epochs "$EPOCHS" || echo "[warn] L4S skipped"
  $PY "$E" sen1floods11 --root "${S1F:-$IN/sen1floods11-essentials}" --out "$DATA/s1f.npz" \
    --size "$EO_SIZE" --max-n "$EO_S1_N" --holdout-event Bolivia && \
    $PY "$HERE/train_classifier.py" --model eo --data "$DATA/s1f.npz" --test "$DATA/s1f_Bolivia_test.npz" --out "$OUT/eo_s1f" --epochs "$EPOCHS" || echo "[warn] Sen1Floods11 skipped"
  [ -n "${HEPH:-}" ] && $PY "$E" hephaestus --root "$HEPH" --annotations "${HEPH_ANN:-}" --out "$DATA/heph.npz" \
    --size "$EO_SIZE" --max-n "$EO_HEPH_N" && \
    $PY "$HERE/train_classifier.py" --model eo --data "$DATA/heph.npz" --out "$OUT/eo_heph" --epochs "$EPOCHS" || echo "[info] Hephaestus: set HEPH=<patch dir> HEPH_ANN=<annotation dir>"
  ;;
*) echo "unknown stage $STAGE"; exit 2 ;;
esac
