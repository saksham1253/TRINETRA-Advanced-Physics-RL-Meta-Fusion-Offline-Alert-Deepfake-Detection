# TRINETRA Live Flow

A real-time, interactive explainer of the whole TRINETRA workflow and of how every dataset flows through it.
Story Mode is a 4:55 film (10 scenes, Hinglish + English captions); Explore Mode lets a mentor click anything.

## Run
- **Offline, one file:** open `TRINETRA/exports/TRINETRA_live_flow.html` in any modern browser (no network, no install).
- **In the app:** open the preview and go to `#live` (served from `public/anim/`).
- **Video:** click **▶ Video** in the animation (or the dashboard's **Watch video**). Files: `public/anim/TRINETRA_live_flow_story.mp4`
  (full 4:55 film, 1920×1080, 15 fps, Hinglish captions burned in) and `public/anim/TRINETRA_live_flow_teaser.mp4` (15 s, 30 fps); copies sit
  next to the offline HTML in `TRINETRA/exports/`. For a smoother 30 / 60 fps film, run the recorder below with `--fps 30` or `--fps 60`.

## Controls
Space play/pause · ← → previous/next scene · scrub bar with S0–S9 chapter markers · speed 0.5–2× ·
C captions (English / Hinglish / off) · S show sources (file path under every badge) · M reduced motion (also honours
`prefers-reduced-motion`) · P presenter mode (hides controls and cursor) · F full screen · E Explore Mode.
URL flags: `?t=120` start time · `?paused` · `?explore=Parameter%20Lab` · `?safe=1` low effects · `?record=1` record mode.

## Data-origin badges
| badge | meaning |
|---|---|
| REAL RESULT | from a results file in the repo (path shown with Sources on) |
| REAL CONFIG | read from code or config (file and line) |
| PUBLIC REPORT | survey or report compiled in `docs/26`, with confidence A / B |
| WORKED EXAMPLE | hand-computable from the repo formulas, not a measurement |
| ILLUSTRATIVE / SIMULATED REPLAY | teaching content, seeded, always under an amber ribbon; never a metric |
| RESULT PENDING | the Kaggle stage has not produced a number yet; nothing is estimated |

## Regenerate
```bash
python TRINETRA/ANIM/tools/extract_animation_data.py   # repo -> public/anim/data/animation_data.{json,js}
python TRINETRA/ANIM/tools/make_docs.py                # storyboard, voice-over, .srt subtitles
python TRINETRA/ANIM/tools/build_single_file.py        # -> TRINETRA/exports/TRINETRA_live_flow.html
node TRINETRA/ANIM/tools/record.mjs --url file://$PWD/TRINETRA/exports/TRINETRA_live_flow.html --out story.mp4 --fps 30   # add --fps 60 for 60 fps
```
When new Kaggle results land in `TRINETRA/results/`, re-run the first and third commands: pending chips turn into real numbers.

## Files
`public/anim/index.html` (shell + CSS) · `public/anim/app.js` (engine, scenes, explore) · `public/anim/data/script.json`
(captions and timing) · `tools/` (extractor, docs, single-file build, recorder) · `STORYBOARD.md` · `VOICEOVER_HINGLISH.md` ·
`subtitles_en.srt` · `subtitles_hinglish.srt` · `MENTOR_CHEATSHEET.md` · `ANIM_STATE.md` · `NEXT_ACTION.md` · `QA.md`.
