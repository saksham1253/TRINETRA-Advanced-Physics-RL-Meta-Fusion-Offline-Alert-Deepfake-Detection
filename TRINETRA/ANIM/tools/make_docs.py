"""Generate STORYBOARD.md, VOICEOVER_HINGLISH.md and English / Hinglish .srt subtitles from public/anim/data/script.json."""
import json
from pathlib import Path

WS = Path(__file__).resolve().parents[3]
S = json.loads((WS / "public/anim/data/script.json").read_text(encoding="utf-8"))
OUT = WS / "TRINETRA/ANIM"
mmss = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"


def srt_time(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


sb = ["# TRINETRA Live Flow · STORYBOARD", "", f"Total {mmss(sum(s['dur'] for s in S['scenes']))} · generated from `public/anim/data/script.json`.", "",
      "| scene | time | purpose | badges on screen |", "|---|---|---|---|"]
BADGES = {"S0": "none (title)", "S1": "PUBLIC REPORT + confidence; REAL CONFIG (docs/17); claim-ladder chips",
          "S2": "REAL CONFIG (docs/09b sizes); REAL RESULT (TPD counts, held-out n); ILLUSTRATIVE (fake 99%)",
          "S3": "SIMULATED REPLAY ribbon; REAL CONFIG (fusion rules, p*, flicker formula)", "S4": "SIMULATED REPLAY; REAL CONFIG (CAP human gate)",
          "S5": "SIMULATED REPLAY; SYNTHETIC PLACEHOLDER; REAL CONFIG r′ = r(1 − p_fake)",
          "S6": "WORKED EXAMPLE (repo numbers); REAL RESULT (reliability bins, ECE)", "S7": "class chips A/B; REAL CONFIG params; REAL RESULT (Caine histogram, real site)",
          "S8": "ILLUSTRATIVE ribbon; PLANNED chips", "S9": "REAL RESULT (results/); RESULT PENDING chips"}
vo = ["# TRINETRA Live Flow · VOICE-OVER (Hinglish, with English subtitle track)", "",
      "Read the Hinglish line when the timestamp arrives. The same lines are burned in as captions (toggle EN / Hinglish / off with C).", ""]
srt = {"en": [], "hi": []}
n = 0
for sc in S["scenes"]:
    sb.append(f"| {sc['id']} {sc['name']} | {mmss(sc['t0'])}–{mmss(sc['t0'] + sc['dur'])} | {sc['purpose']} | {BADGES.get(sc['id'], '')} |")
    vo += [f"## {sc['id']} · {sc['name']} ({mmss(sc['t0'])}–{mmss(sc['t0'] + sc['dur'])})", ""]
    caps = sc["captions"]
    for i, c in enumerate(caps):
        t0 = sc["t0"] + c["t"]; t1 = sc["t0"] + (caps[i + 1]["t"] if i + 1 < len(caps) else sc["dur"]) - 0.2
        vo += [f"- **[{mmss(t0)}]** {c['hi']}", f"  - EN: {c['en']}"]
        n += 1
        for lang in ("en", "hi"):
            srt[lang] += [str(n), f"{srt_time(t0)} --> {srt_time(t1)}", c[lang], ""]
    vo.append("")
(OUT / "STORYBOARD.md").write_text("\n".join(sb) + "\n", encoding="utf-8")
(OUT / "VOICEOVER_HINGLISH.md").write_text("\n".join(vo) + "\n", encoding="utf-8")
(OUT / "subtitles_en.srt").write_text("\n".join(srt["en"]), encoding="utf-8")
(OUT / "subtitles_hinglish.srt").write_text("\n".join(srt["hi"]), encoding="utf-8")
print(f"[docs] storyboard, voice-over, 2 subtitle tracks ({n} cues)")
