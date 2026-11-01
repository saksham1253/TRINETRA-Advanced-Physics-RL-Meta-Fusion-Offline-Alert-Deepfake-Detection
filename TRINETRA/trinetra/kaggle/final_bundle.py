"""TRINETRA FINAL BUNDLE: every Kaggle run (A B C D F P X S) -> ONE folder + ONE zip.

Steps (all CPU, ~5-10 min):
  1. pick one phase per account from the out_<ACCOUNT>_<PHASE>.zip files (final beats phase2), same rule as merge_all_results
  2. FIRE META-FUSION, fresh, on the attached runs: fire_cnn (A) + zeroshot + clip_probe (B, else X/F) + colorhist (A),
     REAL pairing per seed (kaggle/fire_meta_fusion.py refuses if the rows are not the same images). If that is not possible,
     the repo's results/fire_meta is used and the reason is written down.
  3. MASTER MERGE (kaggle/merge_all_results.py) with the fresh meta-fusion -> MASTER_RESULTS.md, RESULTS.md, master.json
  4. ALL FIGURES (tools/make_figures.py): physics explainers + measured results + cross-modal / stress (X, S) +
     R0 scorecard overview, all read from the merged tree
  5. docs: physics book (PHYSICS_FROM_ZERO), CH05 derivations, final report, meta-fusion design
  6. FINAL_README.md (index + headline + every *_compare.md) and TRINETRA_FINAL.zip

Nothing is invented: a run that is missing is listed as "missing", its rows stay "not measured".
Run (local):  python TRINETRA/trinetra/kaggle/final_bundle.py --zips out_*.zip --out FINAL
Run (Kaggle): python .../final_bundle.py --search /kaggle/input /kaggle/working --out /kaggle/working/FINAL
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRI = HERE.parents[1]                                   # TRINETRA/
ROOT = TRI.parent                                       # repo root (tools/ lives here)
sys.path.insert(0, str(HERE))
from merge_all_results import _pick                     # noqa: E402

EXPECTED = {"A": "fire CNN + colour baseline + video", "B": "CLIP zero-shot + probe", "C": "deepfake",
            "D": "EO heads (Landslide4Sense, Sen1Floods11)", "F": "fusion + offline RL", "P": "physics + geo meta-fusion + Geo-PINN",
            "X": "cross-modal fire fusion", "S": "confuser-aware stress retrain"}
LOG: list[str] = []


def log(msg):
    print(msg, flush=True); LOG.append(msg)


def run(cmd, timeout=1800):
    t0 = time.time(); log("$ " + " ".join(map(str, cmd)))
    try:
        p = subprocess.run(list(map(str, cmd)), capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        log(f"[timeout] after {timeout}s"); return 1, ""
    out = p.stdout + p.stderr
    print(out[-4000:], flush=True)
    log(f"[time] {time.time() - t0:.0f}s · exit {p.returncode}")
    return p.returncode, out


def find_zips(roots, max_depth=4):
    """out_<ACC>_<PHASE>.zip under the roots; depth-limited and never enters the 61 GB team dataset."""
    zs, skip = [], ("trinetra-dataset", "cifake", "crisismmd", "avenue_dataset", "npz", "FINAL")
    for r in roots:
        base = os.path.realpath(r)
        for d, dirs, files in os.walk(base, followlinks=True):
            depth = d[len(base):].count(os.sep)
            dirs[:] = [] if depth >= max_depth else [x for x in dirs if not any(k in x.lower() for k in map(str.lower, skip))]
            zs += [os.path.join(d, f) for f in files if re.search(r"out_[A-Za-z]+_[A-Za-z0-9]+(?: \(\d+\))?\.zip$", f)]
    return sorted(set(zs))


def zip_member(z, pattern):
    """first member of zip z whose path ends with pattern (zips are made from out/, but some carry an out/ prefix)."""
    names = zipfile.ZipFile(z).namelist()
    hits = [n for n in names if re.search(pattern, n)]
    return sorted(hits, key=len)[0] if hits else None


def extract(z, member, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(zipfile.ZipFile(z).read(member)); return dst


# ---------------------------------------------------------------------------------------------------- 2. fire meta-fusion
def fire_meta(picked, work, out):
    """fresh REAL-paired fire stack on the attached runs; returns (dir with reports, note)."""
    inp = work / "fire_meta_inputs"
    pat = lambda kind: rf"(^|/){kind}/{kind}_s(\d+)_oof\.npz$"  # noqa: E731

    def pull(kind, acc):
        z = picked[acc][1]
        names = [n for n in zipfile.ZipFile(z).namelist() if re.search(pat(kind), n)]
        return {int(re.search(pat(kind), n).group(2)): extract(z, n, inp / acc / os.path.basename(n)) for n in names}

    got = {}
    for kind in ("fire", "colorhist"):
        for acc in ("A", "ALL"):
            if acc in picked and (d := pull(kind, acc)):
                got[kind], got[kind + "_src"] = d, acc
                break
    if "fire" not in got:
        return None, "fresh fire meta-fusion not possible (no fire OOF from A); repo results/fire_meta used"
    import numpy as np
    ref = np.load(got["fire"][min(got["fire"])], allow_pickle=True)

    def score(f):
        """2 = OOF and held-out rows are the same images as fire_cnn, 1 = OOF only, 0 = not stackable"""
        d = np.load(f, allow_pickle=True)
        if not (np.array_equal(d["block"], ref["block"]) and np.array_equal(d["y"], ref["y"])):
            return 0
        t = "test_block" in d and "test_block" in ref and len(d["test_block"]) and np.array_equal(d["test_block"], ref["test_block"])
        return 2 if t else 1
    # B owns zeroshot / clip_probe, but F and X re-run them in-session on A's own npz, so their held-out rows can align when B's do not
    for kind in ("zeroshot", "clip_probe"):
        best = None
        for acc in ("B", "F", "X", "ALL"):
            if acc in picked and (d := pull(kind, acc)):
                sc = score(d[min(d)])
                log(f"- {kind} from {acc}: " + ["not aligned", "OOF aligned", "OOF + held-out aligned"][sc])
                if sc and (best is None or sc > best[0]):
                    best = (sc, acc, d)
        if best:
            got[kind], got[kind + "_src"] = best[2], best[1]
    if not all(k in got for k in ("fire", "zeroshot", "clip_probe")):
        miss = [k for k in ("fire", "zeroshot", "clip_probe") if k not in got]
        return None, f"fresh fire meta-fusion not possible (missing OOF: {', '.join(miss)}); repo results/fire_meta used"
    out.mkdir(parents=True, exist_ok=True)
    zs, cp = got["zeroshot"][min(got["zeroshot"])], got["clip_probe"][min(got["clip_probe"])]
    ok = []
    for seed, f in sorted(got["fire"].items()):
        cmd = [sys.executable, HERE / "fire_meta_fusion.py", "--fire", f, "--zeroshot", zs, "--clip", cp, "--out", out, "--seed", seed]
        if "colorhist" in got and seed in got["colorhist"]:
            cmd += ["--colorhist", got["colorhist"][seed]]
        rc, txt = run(cmd, timeout=900)
        if rc == 0:
            ok.append(seed)
        else:
            log(f"[fire-meta] seed {seed} failed: " + (txt.strip().splitlines() or ["?"])[-1])
    if not ok:
        shutil.rmtree(out, ignore_errors=True)
        return None, "fresh fire meta-fusion refused (rows not aligned between runs); repo results/fire_meta used"
    # the figures read fire_meta/inputs/<expert>_s0_oof.npz
    (out / "inputs").mkdir(exist_ok=True)
    shutil.copy(got["fire"][min(got["fire"])], out / "inputs" / "fire_s0_oof.npz")
    shutil.copy(zs, out / "inputs" / "zeroshot_s0_oof.npz"); shutil.copy(cp, out / "inputs" / "clip_probe_s0_oof.npz")
    return out, (f"fresh fire meta-fusion on attached runs: fire {got['fire_src']} seeds {ok}, zeroshot/clip_probe "
                 f"{got['zeroshot_src']}/{got['clip_probe_src']}")


# ---------------------------------------------------------------------------------------------------- 4. figures
def results_tree_for_figures(merged, meta_dir, dst):
    """results/-shaped folder (what make_figures reads) built from the merged tree, repo copies only as fallback."""
    dst.mkdir(parents=True, exist_ok=True)
    tree = merged / "tree"
    for sub, pat in (("geo_fusion", "geo_fusion_s*_report.json"), ("geo_pinn", "geo_pinn_s*_report.json"),
                     ("offline_rl_heldout", "*heldout*_report.json")):
        hits = sorted(glob.glob(str(tree / "**" / pat), recursive=True))
        (dst / sub).mkdir(exist_ok=True)
        if hits:
            for h in hits:
                shutil.copy(h, dst / sub / os.path.basename(h))
        elif (TRI / "results" / sub).exists():
            shutil.copytree(TRI / "results" / sub, dst / sub, dirs_exist_ok=True)
    shutil.copytree(meta_dir or TRI / "results" / "fire_meta", dst / "fire_meta", dirs_exist_ok=True)
    (dst / "master_merged").mkdir(exist_ok=True)
    shutil.copy(merged / "master.json", dst / "master_merged" / "master.json")


def fig_scorecard(master_json, path):
    """R0: every measured ROC-AUC on one chart (OOF and held-out), straight from master.json."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = json.load(open(master_json))["scorecard"]
    bars = []
    for r in rows:
        v = r.get("value")
        if not v or "ROC-AUC" not in r["metric"]:
            continue
        nums = [float(x) for x in re.findall(r"-?\d+\.\d+", v.split(";")[0])][:2]
        if nums:
            bars.append((f"{r['expert']}\n{r['hazard'].split(' (')[0]}", nums[0], nums[1] if len(nums) > 1 else None, r.get("admitted")))
    if not bars:
        return
    fig, ax = plt.subplots(figsize=(9.5, 0.55 * len(bars) + 1.6))
    y = range(len(bars))
    ax.barh([i - 0.18 for i in y], [b[1] for b in bars], 0.36, color="#D9480F", label="OOF / spatial CV")
    ax.barh([i + 0.18 for i in y], [b[2] or 0 for b in bars], 0.36, color="#2F5FC4", label="held-out (new source)")
    for i, b in enumerate(bars):
        ax.text(b[1] + 0.005, i - 0.18, f"{b[1]:.3f}", va="center", fontsize=8)
        if b[2] is not None:
            ax.text(b[2] + 0.005, i + 0.18, f"{b[2]:.3f}", va="center", fontsize=8)
    ax.set_yticks(list(y), [b[0] for b in bars], fontsize=8); ax.invert_yaxis(); ax.set_xlim(0.3, 1.08)
    ax.axvline(0.5, color="#8A7A6F", ls=":"); ax.legend(loc="lower right", fontsize=8.5, frameon=False)
    ax.set_title("TRINETRA: har measured ROC-AUC ek jagah (OUR RESULTS, prototype pack)", fontweight="bold")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.text(0.01, -0.01, "From master.json (final merge). 0.5 = coin flip. Admitted/deploy verdicts are in MASTER_RESULTS.md.",
             fontsize=8, color="#8A7A6F")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig); log(f"   {path}")


FIXED_EXPL = {
    "R0_scorecard_all_auc.png": ("Har measured ROC-AUC ek chart par", "Orange = same-source (OOF, spatial CV), blue = naya dataset (held-out). 0.5 = sikka uchhalna. Ek nazar me dikhta hai kaunsa model tikta hai (fire, CLIP) aur kaunsa naye data par gir jaata hai (deepfake)."),
    "R1_fire_roc_oof_and_heldout.png": ("Fire ROC curves (OOF + held-out)", "Curve jitna upar-left, utna achha. CLIP probe aur stack sabse upar; fire CNN neeche. Right panel = naya dataset (DeepFire), jahan sab models kaafi achhe hain."),
    "R2_calibration.png": ("Calibration", "Model jo probability bole, kya utna hi sach hota hai? Diagonal line = perfect. Temperature scaling ke baad lines diagonal ke paas hain, isliye p* threshold par bharosa kar sakte hain."),
    "R3_alert_flood_vs_base_rate.png": ("Base-rate correction", "Asli duniya me aag bahut kam hoti hai (1% ya kam), training me 55%. Prior-shift correction se false alarm bahut girte hain, par per-image detection bhi girti hai; video me aag kai frames tak dikhti hai, isliye incident pakda jaata hai. Ye PROPOSAL hai, repo me default nahi."),
    "R4_landslide_auc.png": ("Landslide: physics bina training", "Blue = physics jo kisi data par fit nahi hui (Caine, dFS, geo gate). Phir bhi ROC-AUC ~0.75. Barish logistic aur FM-1 fusion thoda upar. Geo-PINN laal line."),
    "R5_rl_heldout.png": ("RL held-out", "Learned RL (CQL), fixed rule, tuned rule, always-alarm: reward per image. RL tuned rule se behtar nahi hua, isliye deploy nahi."),
    "R6_generalisation_gap.png": ("Generalisation gap", "Same source vs naya source. Deepfake 0.96 se 0.45 par gira: isliye wo sirf down-weighter hai."),
    "R7_crossmodal_video.png": ("Cross-modal video", "FireSense 49 videos par har stream ka (detection - false alarm), temporal validator ke baad. Stack +0.47, clip_probe +0.32, fire CNN +0.01: video par teeno experts ko jodna sach me kaam aaya. n chhota hai (49 videos), isliye ise counts ki tarah padho."),
    "R8_crossmodal_confusers.png": ("Cross-modal confusers", "Weather, candle, scenes par har stream ka false-alarm rate. Kam = achha."),
    "R9_stress_retrain.png": ("Confuser-aware retrain (S)", "Ek confuser type training se bahar rakha (unseen), baaki do par hard-negative training. Barabar recall 0.90 par unseen confuser par false alarms: CLIP probe 0.43 -> 0.32, stack 0.35 -> 0.16, aur DeepFire AUC 0.998 -> 0.997 (girna 0.01 se kam). Gate 3/3 seeds ADMITTED: TRINETRA ka pehla admitted learned upgrade."),
    "01_fs_vs_pore_pressure.png": ("FS vs pore pressure", "Mitti me paani ka dabaav badhe to factor of safety girta hai; FS < 1 = slope girega. Steep slope = kam margin."),
    "02_iverson_pressure_head.png": ("Iverson pressure head", "Barish ke baad paani dheere-dheere gehraai tak pahunchta hai; isliye landslide barish ke kuch ghante/din baad aata hai."),
    "03_caine_threshold.png": ("Caine threshold", "Lambi barish ko kam intensity chahiye girane ke liye: I = 14.82 D^-0.39 (log-log par seedhi line)."),
    "04_fukuzono_inverse_velocity.png": ("Fukuzono inverse velocity", "Girne se pehle slope tez hota jaata hai; 1/velocity ki line zero ko jahan chhooti hai, wahi failure time ka andaza."),
    "05_fire_physics.png": ("Fire physics", "Flame height (Heskestad), Byram number (hawa vs aag), flicker frequency: camera jo dekhe wo physics se match kare."),
    "06_plume_temperature.png": ("Plume temperature", "Aag ke upar garam hawa ka tapmaan oonchai ke saath girta hai (McCaffrey)."),
    "07_cost_loss_and_prior_shift.png": ("Cost-loss p*", "Galat alarm ki keemat 5, chhooti aag ki 100 -> p* = 5/105 = 0.048. Is se upar probability = alarm."),
    "08_lora_range_airtime.png": ("LoRa range + airtime", "Spreading factor badhao to range badhti hai par message bhejne me zyada time lagta hai."),
    "09_fresnel_real_terrain.png": ("Fresnel zone, asli terrain", "Gateway se gaon tak radio line ke beech pahad aata hai; relay oonchi jagah chahiye."),
    "10_noisy_or.png": ("Noisy-OR", "Physics signals jodte waqt ek bhi signal khatra bole to combined risk kabhi kam nahi hota."),
}


def write_graph_docs(out, extra):
    figs = sorted((out / "figures").rglob("*.png")) if (out / "figures").exists() else []
    ex = {n: (t, e) for n, t, e in extra}
    items = []
    for f in figs:
        t, e = ex.get(f.name) or FIXED_EXPL.get(f.name) or (f.stem, "")
        items.append({"file": str(f.relative_to(out)), "name": f.name, "group": f.parent.name, "title": t, "explain": e})
    json.dump(items, open(out / "figures" / "figures.json", "w"), indent=1, ensure_ascii=False)
    L = ["# TRINETRA — har graph ka matlab (Hinglish)", "",
         "Saare result graphs OUR RESULTS (prototype pack) se bane hain; physics graphs repo ke apne Python functions se.", ""]
    for grp, head in (("results", "Measured results (R0-R9)"), ("extra", "Extra result graphs (G01-G14)"), ("physics", "Physics explainers (01-10)")):
        L += [f"## {head}", ""]
        for it in (i for i in items if i["group"] == grp):
            L += [f"### {it['title']}", f"`{it['file']}`", "", f"![{it['name']}]({it['file']})", "", it["explain"], ""]
    (out / "GRAPHS_EXPLAINED.md").write_text("\n".join(L))
    log(f"- GRAPHS_EXPLAINED.md: {len(items)} graphs")


# ---------------------------------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--zips", nargs="*", default=[]); ap.add_argument("--search", nargs="*", default=[])
    ap.add_argument("--out", default="FINAL"); ap.add_argument("--prefer", choices=["final", "phase2"], default=None)
    ap.add_argument("--no-zip", action="store_true")
    a = ap.parse_args(argv)
    T0 = time.time()
    out = Path(a.out).resolve(); work = out / "_work"
    if out.exists():
        shutil.rmtree(out)
    work.mkdir(parents=True)
    zips = sorted(set(a.zips + find_zips(a.search)))
    have = set(_pick(zips, a.prefer))
    for r in a.search:
        for d in sorted(glob.glob(os.path.join(r, "out_*_session"))):
            acc = re.search(r"out_([A-Za-z]+)_session$", d).group(1).upper()
            if acc not in have and os.path.isdir(d):
                z = shutil.make_archive(str(work / f"out_{acc}_final"), "zip", d); zips.append(z); have.add(acc)
                log(f"- {acc}: zipped session folder {d}")
    picked = _pick(zips, a.prefer)
    log("## 1. runs"); [log(f"- {k}: {ph} ({os.path.basename(z)})") for k, (ph, z) in sorted(picked.items())]
    missing = [k for k in EXPECTED if k not in picked and not (k in "ABCDP" and "ALL" in picked)]
    log("- missing: " + (", ".join(f"{k} ({EXPECTED[k]})" for k in missing) or "none"))

    log("## 2. fire meta-fusion")
    meta_dir, meta_note = fire_meta(picked, work, work / "fire_meta")
    log("- " + meta_note)

    log("## 3. master merge")
    cmd = [sys.executable, HERE / "merge_all_results.py", "--zips", *[z for _, z in picked.values()], "--out", out / "master"]
    if meta_dir:
        cmd += ["--dirs", meta_dir]
    if a.prefer:
        cmd += ["--prefer", a.prefer]
    rc, _ = run(cmd, timeout=1800)
    if rc != 0 or not (out / "master" / "master.json").exists():
        raise SystemExit("master merge failed (see log above)")

    # readable run label instead of the temp path of the fresh meta-fusion
    if meta_dir:
        for f in ("master.json", "MASTER_RESULTS.md"):
            q = out / "master" / f
            q.write_text(q.read_text().replace(f"dir:{meta_dir}", "Z fire meta-fusion (fresh)").replace(str(meta_dir), "re-run in Z on the attached runs"))
    # weights are not results: keep reports + OOF files only (A ships 15 x 1.4 MB fold checkpoints)
    pts = list((out / "master" / "tree").rglob("*.pt")) + list((out / "master" / "tree").rglob("emb_cache_*.npz"))
    for f in pts:
        f.unlink()
    log(f"- dropped {len(pts)} model checkpoints / embedding caches from the bundle")

    log("## 4. figures")
    rt = work / "results"
    results_tree_for_figures(out / "master", meta_dir, rt)
    xs = [picked[k][1] for k in ("X", "S") if k in picked]
    fig_cmd = [sys.executable, ROOT / "tools" / "make_figures.py", "--results", rt, "--fig-out", out / "figures" / "results",
               "--phys-out", out / "figures" / "physics"]
    if xs:
        fig_cmd += ["--x-zip", *xs]
    if (ROOT / "tools" / "make_figures.py").exists():
        run(fig_cmd, timeout=1200)
    else:
        log("[skip] tools/make_figures.py not found")
    try:
        fig_scorecard(out / "master" / "master.json", out / "figures" / "results" / "R0_scorecard_all_auc.png")
    except Exception as e:                                   # noqa: BLE001
        log(f"[skip] R0 scorecard: {e}")

    try:
        import extra_figures
        extra, skipped = extra_figures.main(["--merged", str(out / "master"), "--out", str(out / "figures" / "extra")])
        log(f"- extra graphs: {len(extra)} made, skipped {skipped or 'none'}")
    except Exception as e:                                   # noqa: BLE001
        extra = []; log(f"[skip] extra graphs: {e}")
    write_graph_docs(out, extra)

    log("## 5. docs")
    docs = out / "docs"
    book = TRI / "docs" / "19_TRINETRA_EXPLAINED"
    if book.exists():
        shutil.copytree(book, docs / "19_TRINETRA_EXPLAINED", dirs_exist_ok=True)
        if (out / "figures" / "physics").exists():         # freshly computed physics figures replace the shipped ones
            shutil.copytree(out / "figures" / "physics", docs / "19_TRINETRA_EXPLAINED" / "PHYSICS_FROM_ZERO" / "fig", dirs_exist_ok=True)
    if (TRI / "docs" / "20_FINAL").exists():
        shutil.copytree(TRI / "docs" / "20_FINAL", docs / "20_FINAL", dirs_exist_ok=True)
    for f in ("FINAL_REPORT.md", "TRINETRA_MetaFusion_Design.md", "ASSUMPTIONS.md", "REFERENCES.md",
              "results/master_merged/DECK_RESULTS_SLIDES.md"):
        if (TRI / f).exists():
            docs.mkdir(parents=True, exist_ok=True); shutil.copy(TRI / f, docs / os.path.basename(f))

    log("## 6. index + zip")
    tree = out / "master" / "tree"
    compares = sorted(glob.glob(str(tree / "**" / "*_compare.md"), recursive=True))
    D = ["# TRINETRA — detailed comparison tables (every *_compare.md of the final merge)", ""]
    for c in compares:
        D += [f"---", f"### `{os.path.relpath(c, tree)}`", "", Path(c).read_text(), ""]
    (out / "DETAILS_ALL_COMPARES.md").write_text("\n".join(D))
    figs = sorted(str(p.relative_to(out)) for p in (out / "figures").rglob("*.png")) if (out / "figures").exists() else []
    master_md = (out / "master" / "MASTER_RESULTS.md").read_text()
    R = ["# TRINETRA — FINAL (all runs merged)", "",
         "Team Sankat Mochak. Every number is OUR RESULT on the prototype pack (not comparable to full-benchmark papers).", "",
         "## Contents", "",
         "| path | what |", "|---|---|",
         "| `master/MASTER_RESULTS.md` | headline scorecard (one row per expert, admitted / deploy verdicts) |",
         "| `master/RESULTS.md` | every model, every metric, mean over seeds |",
         "| `master/master.json` | same, machine-readable (deck / console read this) |",
         "| `DETAILS_ALL_COMPARES.md` | every comparison table: fire + geo meta-fusion, cross-modal, stress, fusion |",
         "| `figures/results/` | measured-result graphs (R0 overview … R9 stress) |",
         "| `figures/physics/` | physics explainer graphs, computed with the repo's own functions |",
         "| `figures/extra/` | G01-G14 extra result graphs (seeds, confusers, landslide features, GLOF, RL, confusion matrices) |",
         "| `GRAPHS_EXPLAINED.md` | har graph + Hinglish explanation (`figures/figures.json` = same, frontend ke liye) |",
         "| `docs/20_FINAL/` | DATASETS_USED.csv/.tsv, DATASET_FEATURES_LANDSLIDE.csv/.tsv, CODE_AND_INTEGRATION_HINGLISH.md |",
         "| `docs/19_TRINETRA_EXPLAINED/` | Hinglish book; `PHYSICS_FROM_ZERO/` = derivations from zero |",
         "| `master/tree/` | raw per-run reports and OOF files used |", "",
         "## Runs", "", *[f"- **{k}** ({EXPECTED.get(k, '')}): {ph}, `{os.path.basename(z)}`" for k, (ph, z) in sorted(picked.items())],
         f"- **missing**: {', '.join(f'{k} ({EXPECTED[k]})' for k in missing) or 'none'}", "",
         f"Fire meta-fusion: {meta_note}.", "",
         "## Figures", "", *[f"- `{f}`" for f in figs], "",
         "## Scorecard (copy of master/MASTER_RESULTS.md)", "", master_md.split("## Runs used", 1)[-1].split("\n", 1)[-1], "",
         "## Build log", "", "```", *LOG, "```", f"Built in {(time.time() - T0) / 60:.1f} min."]
    (out / "FINAL_README.md").write_text("\n".join(R) + "\n")
    shutil.rmtree(work, ignore_errors=True)
    if not a.no_zip:
        z = shutil.make_archive(str(out.parent / "TRINETRA_FINAL"), "zip", out)
        log(f"zip: {z} ({os.path.getsize(z) / 1e6:.1f} MB)")
    print("\n" + master_md)


if __name__ == "__main__":
    main()
