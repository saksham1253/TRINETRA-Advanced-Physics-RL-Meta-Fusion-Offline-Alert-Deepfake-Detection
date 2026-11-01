# NEXT_ACTION
1. When Kaggle results arrive (A fire CNN, C deepfake, D EO, P meta-fusion): copy them into `TRINETRA/results/`, extend
   `results()` in `tools/extract_animation_data.py` for the new report names, re-run extract + build_single_file, re-record.
2. If the team caches per-frame scores for a real steam / fire clip, replace `replay()` inputs in `public/anim/app.js` and drop the
   SIMULATED ribbon for that scenario.
3. Optional: Hinglish TTS voice track aligned to `subtitles_hinglish.srt`; mux with ffmpeg.
