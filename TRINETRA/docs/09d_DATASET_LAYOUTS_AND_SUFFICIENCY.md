# 09d — DATASET LAYOUTS (verified) + SUFFICIENCY REVIEW (2026-10-31)
Layouts were read with the **Kaggle public file-list API** (no login). JSON snapshot `docs/tools/dataset_layouts_2026-10-31.json` holds P33-P37; P01-P15 counts were read in the same session and recorded in the table below.
The API caps listings at 8,000 files, so large sets are partially listed (marked "truncated").

## A. Verified folder layouts, and the map used in `run_hackathon.sh build`
| ID | Kaggle mount `/kaggle/input/…` | Layout seen | Map used | Problem found and fix |
|----|------------------------------|-------------|----------|---------------------|
| P02 D-Fire | `smoke-fire-detection-yolo` | `data.yaml`, `data/<split>/images/*.jpg` + `labels/*.txt`; names WEB#, AoF#, PublicDataset# (truncated) | `yolo --classes auto` | class ids are NOT in the README, so they are read from `data.yaml`. **AoF = consecutive camera frames**, so `--seq-bucket 50` keeps neighbours in one group |
| P03 DeepFire | `forest-fire-dataset` | `Forest Fire Dataset/Training/{fire,nofire}` (760 + 760), `Testing/` flat with `fire_#`/`nofire_#` (190 + 190) | `Training/fire=fire Training/nofire=none` | old default `fire/nofire` worked only by luck; Testing is unused (class only in the file name) |
| P01 FIRE Dataset | `fire-dataset` | `fire_dataset/fire_images` 755, `non_fire_images` 244 | as is | imbalanced 3:1 |
| P06 Weather | `weather-dataset` | `dataset/<class>/#.jpg`: fogsmog 851, sandstorm 692, lightning 377, rain 526 … | `fogsmog sandstorm lightning rain = none` | — |
| P14 CIFAKE | `cifake-real-and-ai-generated-synthetic-images` | `test/FAKE/…` seen (truncated) | `REAL=real FAKE=fake` (part match, any split) | `train/` not visible in the listing, so I use part-match to be safe |
| P15 StyleGAN faces | `deepfake-face-images` | `Final Dataset/Fake` 7,000 (3,500 are `fake_#_aug_#`), `Final Dataset/Real` 1,000 | `"Final Dataset/Real=real" "Final Dataset/Fake=fake"` | **old default `real/fake` would FAIL (case)**. **Augmented copies would LEAK** across splits, so `_aug_#` now maps to its source group |
| P33 FireSense | `firesense` | `fire/{pos,neg}`, `smoke/{pos,neg}`, 49 `.avi` | `video --map fire/pos=fire …` | new `video` command |
| P34 Small flames | `flame-dataset-candlelightermatch-stick-flames` | `Flame/train/images/frame_#.jpg` (7.8k), `Flame/test` YOLO 101 | `Flame/train/images=none` + `--seq-bucket 50` | video frames, so grouped |
| P35 Intel scenes | `intel-image-classification-dataset` | `Intel-Image-Classification/{train,test}/<class>` | street, buildings, forest, mountain = none | — |
| P36 Home fire | `home-fire-dataset` | `{train,test}/{images,labels}` YOLO (truncated, no data.yaml seen) | `--classes auto`, else `HOMEFIRE_CLASSES` | **class ids UNVERIFIED**: open one label file + the page before trusting |
| P37 AI vs real | `ai-generated-images-vs-real-images` | `AiArtData/AiArtData` 539, `RealArt/RealArt` 436 | `AiArtData=fake RealArt=real` | — |

**Cross-dataset duplicates:** D-Fire's WEB/PublicDataset images and DeepFire / FIRE Dataset are all web-scraped, so the SAME photo can
appear in train and held-out. `build_npz.py dedupe` drops held-out rows within Hamming ≤ 4 (aHash) of any D-Fire row; the count removed is
printed. Quote it in the results.

## B. Is the data sufficient? (Hackathon scope: fire CNN + zero-shot + deepfake + fusion + RL; IoT = future)
| Need | Covered by | Verdict |
|------|-----------|---------|
| Train fire/smoke detector | D-Fire 4k subset (21k available; fire-only 1,164, smoke-only 5,867, both 4,658 per README) | **enough** |
| Cross-dataset held-out, outdoor | DeepFire (forest) + FIRE Dataset (web outdoor), deduped | **enough** |
| Held-out, indoor | Home fire (P36) | ok **if class ids are verified** |
| Temporal / video (validator, demo) | FireSense 49 videos | **was MISSING, now added**. Small n, so quote counts |
| False-alarm confusers: fog, dust, lightning, rain | Weather (P06) | enough |
| Benign small flames (diya, candle, lighter, stove) | P34 | **was MISSING, now added** (non-commercial) |
| Normal scenes | Intel (P35) | **was MISSING, now added** |
| Zero-shot evaluation | same sets (no training data needed) | enough |
| Deepfake train | CIFAKE | ok, but 32 px objects |
| Deepfake held-out, other generators | StyleGAN faces + AI-vs-real art (P37) | **improved** (art added) |
| Fusion paired multi-sensor data | none exists | synthetic pairing (stated everywhere) |
| RL | built from the fusion cache | ok |
| Demo context India | FIRMS India 2023 CSV, IBTrACS NI | enough |

## C. Still NOT covered (say this honestly in Limitations)
1. **Indian CCTV fire footage**: no free verified set found. Domain gap (Brazil/EU/US/web).
2. **Night / IR fire**: no small verified set. FLAME 3 (7.5 GB, thermal) only if time.
3. **Diwali lights / fireworks / sunset / steam / cooking smoke** images: no free verified Kaggle set found. Lightning and fog are the closest.
   If time: collect 50-100 CC-licensed photos per class from Wikimedia Commons and record each license.
4. **AI-generated FIRE/disaster images** (the real misuse case): none found. The deepfake numbers are on generic images only.
5. Pixel-level smoke segmentation: not needed for the current models.
<!-- END -->
