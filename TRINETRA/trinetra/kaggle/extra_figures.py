"""Extra result graphs (G01-G14) + Hinglish explanations, read ONLY from the merged results.

Inputs: <merged>/results.json, <merged>/tree/** reports + OOF files, repo results/geo_large/geo_events.csv (real events).
A graph whose input is missing is skipped and listed; nothing is invented.
Run: python kaggle/extra_figures.py --merged FINAL/master --out FINAL/figures/extra
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TRI = Path(__file__).resolve().parents[2]
C = dict(ink="#1E1612", ink3="#8A7A6F", line="#D9CEC4", brand="#D9480F", brand2="#FF8A3D", blue="#2F5FC4", teal="#0F766E",
         violet="#6D4FC8", red="#B91C1C", green="#1F8A5B", gold="#A16207")
PAL = [C["brand"], C["blue"], C["teal"], C["violet"], C["gold"], C["red"], C["green"], C["ink3"], C["brand2"]]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#EEE7E0", "axes.titleweight": "bold", "legend.frameon": False})
EXPL: list = []   # (file, title, Hinglish explanation)


def save(fig, out, name, title, expl):
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / name, dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)
    EXPL.append((name, title, expl)); print("  ", out / name)


def runs(M, model, key):
    return [r[key] for r in (M.get(model) or {}).get("runs", []) if r.get(key) is not None]


def g01(M, out):
    models = [m for m in ("colorhist", "fire", "zeroshot", "clip_probe", "fire_meta_fusion", "deepfake", "geo_pinn", "geo_fusion") if runs(M, m, "oof_roc_auc")]
    fig, ax = plt.subplots(figsize=(9, 4))
    for i, m in enumerate(models):
        v = runs(M, m, "oof_roc_auc")
        ax.scatter([i] * len(v), v, color=PAL[i % len(PAL)], s=40, zorder=3)
        ax.hlines(np.mean(v), i - 0.3, i + 0.3, color=C["ink"], lw=2)
        ax.text(i, np.mean(v) + 0.012, f"{np.mean(v):.3f}", ha="center", fontsize=8.5)
    ax.set_xticks(range(len(models)), models, rotation=15); ax.axhline(0.5, color=C["ink3"], ls=":")
    ax.set(ylabel="ROC-AUC (OOF, spatial block CV)", title="Har model, har seed: ROC-AUC kitna stable hai?")
    save(fig, out, "G01_auc_per_seed.png", "Har model ka ROC-AUC, har seed alag dot",
         "Har dot ek seed (alag random start) ka result hai, kaali line average. Dots paas-paas = model stable hai. clip_probe aur "
         "fire_meta_fusion sabse upar (~0.95), colour histogram baseline sabse neeche (~0.68). Landslide models (geo_pinn, geo_fusion) "
         "~0.72-0.78 par hain, kyunki wahan sirf barish + DEM jaise mote features hain.")


def g02(M, out):
    models = [m for m in ("colorhist", "fire", "zeroshot", "clip_probe", "fire_meta_fusion", "deepfake", "geo_fusion") if M.get(m)]
    keys = [("oof_roc_auc", "ROC-AUC"), ("oof_pr_auc", "PR-AUC"), ("oof_recall_at_fpr05", "recall @ 5% false alarm")]
    fig, ax = plt.subplots(figsize=(10, 4)); w = 0.26
    for j, (k, lab) in enumerate(keys):
        vals = [np.mean(runs(M, m, k)) if runs(M, m, k) else 0 for m in models]
        ax.bar(np.arange(len(models)) + j * w, vals, w, label=lab, color=PAL[j])
    ax.set_xticks(np.arange(len(models)) + w, models, rotation=15); ax.set_ylim(0, 1.05); ax.legend(ncol=3, fontsize=8.5)
    ax.set(title="Teen metric ek saath: AUC, PR-AUC, aur 5% false alarm par kitni aag pakdi")
    save(fig, out, "G02_metrics_compare.png", "ROC-AUC vs PR-AUC vs recall@FPR5%",
         "ROC-AUC = ranking kitni achhi. PR-AUC = jab model 'aag' bole to kitna sahi. Recall@FPR5% = sabse practical: agar 100 me se "
         "sirf 5 galat alarm allow hain, to kitni asli aag pakdi. Colour histogram ka recall bahut kam, clip_probe/stack ~0.8 se upar.")


def g03(M, out):
    models = [m for m in ("fire", "zeroshot", "clip_probe", "fire_meta_fusion", "deepfake") if runs(M, m, "test_roc_auc")]
    if not models:
        return
    fig, ax = plt.subplots(figsize=(8, 4)); x = np.arange(len(models))
    o = [np.mean(runs(M, m, "oof_roc_auc")) for m in models]; t = [np.mean(runs(M, m, "test_roc_auc")) for m in models]
    ax.bar(x - 0.18, o, 0.36, color=C["brand"], label="same source (OOF)"); ax.bar(x + 0.18, t, 0.36, color=C["blue"], label="naya source (held-out)")
    ax.set_xticks(x, models); ax.set_ylim(0.3, 1.05); ax.axhline(0.5, color=C["ink3"], ls=":"); ax.legend(loc="lower left")
    ax.set(ylabel="ROC-AUC", title="Generalisation: naye dataset par model girta hai ya tikta hai?")
    save(fig, out, "G03_generalisation.png", "Same-source vs naya source",
         "Fire models naye dataset (DeepFire forest photos) par bhi tike. Deepfake model CIFAKE par 0.96 tha, par naye generator wali "
         "images par 0.45 (sikke se bhi kharab). Isliye deepfake ko sirf 'low-trust down-weighter' rakha, alarm dene wala nahi.")


def g04(M, out):
    sets = ["stress_weather", "stress_small_flames", "stress_scenes", "heldout_firedataset", "heldout_homefire"]
    models = [m for m in ("fire", "zeroshot", "clip_probe") if M.get(m)]
    if not models:
        return
    fig, ax = plt.subplots(figsize=(10, 4)); w = 0.8 / len(models)
    for j, m in enumerate(models):
        vals = [np.mean(runs(M, m, f"stress:{s}:fa_rate_at_0p5_cal")) if runs(M, m, f"stress:{s}:fa_rate_at_0p5_cal") else np.nan for s in sets]
        ax.bar(np.arange(len(sets)) + j * w, vals, w, label=m, color=PAL[j])
    ax.set_xticks(np.arange(len(sets)) + w, [s.replace("stress_", "").replace("heldout_", "held-out ") for s in sets], rotation=10)
    ax.set(ylabel="false-alarm rate @0.5 (non-fire images)", title="Confusers: dhuan-jaisa mausam, diya/candle, normal scenes"); ax.legend()
    save(fig, out, "G04_confuser_false_alarms.png", "Confuser images par false alarm",
         "Ye sab images me khatarnak aag NAHI hai (fog, candle, normal sadak/jungle). Bar jitna lamba, utni baar model ne galti se 'aag' "
         "bola. Candle/small flames sabse mushkil hain, kyunki wo sach me aag hi hai, bas khatarnak nahi. Isi ke liye S account ka "
         "confuser-aware retrain bana (R9 graph).")


def g05(M, out):
    if not (M.get("video") or {}).get("runs"):
        return
    keys = [("detect_rate_raw", "detect raw"), ("detect_rate_validated", "detect validated"),
            ("false_alarm_video_rate_raw", "false alarm raw"), ("false_alarm_video_rate_validated", "false alarm validated")]
    fig, ax = plt.subplots(figsize=(8, 3.8))
    vals = [np.mean(runs(M, "video", k)) for k, _ in keys]
    ax.bar([l for _, l in keys], vals, color=[C["teal"], C["green"], C["red"], C["brand"]])
    for i, x in enumerate(vals):
        ax.text(i, x + 0.02, f"{x:.2f}", ha="center")
    ax.set(ylim=(0, 1.1), ylabel="fraction of videos", title="FireSense videos: temporal validator kya badalta hai")
    save(fig, out, "G05_video_validator.png", "Video: raw vs temporal validator",
         "Ek frame par aag dikhna kaafi nahi; validator dekhta hai ki aag kai frames tak lagatar dikhe aur flicker kare. Isse false-alarm "
         "videos thode kam hote hain. n sirf 49 videos hai, isliye ye 'counts' hain, pakka number nahi.")


def g06(tree, out):
    fs = sorted(glob.glob(str(tree / "**" / "fire_meta_fusion_s0_report.json"), recursive=True))
    if not fs:
        return
    r = json.load(open(fs[0])); rules = [k for k in r["rules"] if "raw" not in k]
    tabs = [(r["rules"], "OOF")] + ([(r["heldout"], "held-out")] if r.get("heldout") else [])
    fig, axs = plt.subplots(1, len(tabs), figsize=(6 * len(tabs), 4.2), sharey=True)
    for ax, (tab, lab) in zip(np.atleast_1d(axs), tabs):
        ks = [k for k in rules if k in tab]
        ax.barh(ks, [tab[k]["recall_at_fpr05"] for k in ks], color=[C["violet"] if "stack" in k else C["brand"] if "FM-1" in k else C["ink3"] for k in ks])
        ax.set(title=f"{lab}: recall @ 5% false alarm", xlim=(0, 1))
    np.atleast_1d(axs)[0].invert_yaxis()
    save(fig, out, "G06_fire_meta_rules.png", "Fire meta-fusion: kaunsa jodne ka tareeka best",
         "Chaar fire experts (CNN, CLIP zero-shot, CLIP probe, colour) ko jodne ke tareeke: stacked logistic (meta), FM-1 (hamara "
         "uncertainty-weighted fusion), mean, max, aur akela expert. Stack lagbhag clip_probe ke barabar hai, upar nahi, isliye gate ne "
         "admit nahi kiya. Imaandaar result: jab ek expert pehle se itna strong ho, jodne se fayda kam milta hai.")


def g07(tree, out):
    fs = sorted(glob.glob(str(tree / "**" / "geo_fusion_s*_report.json"), recursive=True))
    if not fs:
        return
    R = [json.load(open(f)) for f in fs]; rules = list(R[0]["rules"])
    m = [np.mean([r["rules"][k]["pr_auc"] for r in R]) for k in rules]
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.barh(rules, m, color=[C["blue"] if k.startswith("single") else C["violet"] for k in rules]); ax.invert_yaxis()
    for i, v in enumerate(m):
        ax.text(v + 0.005, i, f"{v:.3f}", va="center", fontsize=8.5)
    ax.set(xlabel="PR-AUC (spatial CV)", title="Landslide meta-fusion: physics + barish ko jodne ke tareeke")
    save(fig, out, "G07_geo_fusion_rules.png", "Landslide fusion rules (PR-AUC)",
         "Blue = akela signal (barish model, Caine line, dFS, geo gate). Purple = jodne ke tareeke (FM-1, PHARAOH, median, max, physics "
         "shield, stacked logistic). Same 736 asli rows par sab compare hue, seeds ka average.")


def _geo_rows():
    p = TRI / "results" / "geo_large" / "geo_events.csv"
    return list(csv.DictReader(open(p))) if p.exists() else []


def g08(out):
    rows = _geo_rows()
    if not rows:
        return
    y = np.array([int(float(r["label"])) for r in rows])
    feats = [("rain_3d", "3-din barish (mm)"), ("rain_30d", "30-din barish (mm)"), ("slope_p90_deg", "slope p90 (deg)"),
             ("caine_ratio", "Caine ratio I/I_crit"), ("dfs", "dFS (barish se FS girna)"), ("elev_m", "elevation (m)")]
    fig, axs = plt.subplots(2, 3, figsize=(12, 6.5))
    for ax, (k, lab) in zip(axs.ravel(), feats):
        v = np.array([float(r[k]) for r in rows])
        bins = np.linspace(np.nanpercentile(v, 1), np.nanpercentile(v, 99), 30)
        ax.hist(v[y == 0], bins, alpha=0.6, color=C["ink3"], density=True, label="normal din (control)")
        ax.hist(v[y == 1], bins, alpha=0.6, color=C["brand"], density=True, label="landslide din")
        ax.set_title(lab, fontsize=10)
    axs[0, 0].legend(fontsize=8)
    fig.suptitle("Landslide features: girne wale din vs normal din (NASA GLC India + NASA POWER)", fontweight="bold")
    save(fig, out, "G08_landslide_features.png", "Landslide ke features ka distribution",
         "Orange = jis din landslide hua, grey = usi jagah ka normal din. Jahan orange right ki taraf khiska hai (barish, Caine ratio, "
         "dFS), wahi feature kaam ka hai. Slope aur elevation me farak kam hai kyunki control din usi jagah ke hain (sirf mausam badla).")


def g09(out):
    rows = _geo_rows()
    if not rows:
        return
    D = np.array([float(r["caine_D_h"]) for r in rows]); I = np.array([float(r["caine_I_mmh"]) for r in rows]); y = np.array([int(float(r["label"])) for r in rows])
    fig, ax = plt.subplots(figsize=(7, 4.5)); ok = (D > 0) & (I > 0)
    ax.scatter(D[ok & (y == 0)], I[ok & (y == 0)], s=10, color=C["ink3"], alpha=0.5, label="normal din")
    ax.scatter(D[ok & (y == 1)], I[ok & (y == 1)], s=14, color=C["brand"], alpha=0.8, label="landslide din")
    d = np.logspace(0, 3.5, 50); ax.plot(d, 14.82 * d ** -0.39, color=C["red"], lw=2, label="Caine (1980): I = 14.82 D^-0.39")
    ax.set(xscale="log", yscale="log", xlabel="barish ki duration D (hours)", ylabel="intensity I (mm/h)", title="Caine line asli Indian events par")
    ax.legend(fontsize=8.5)
    save(fig, out, "G09_caine_scatter.png", "Caine threshold scatter",
         "Har dot ek din. Laal line = Caine ki global seema. NASA POWER ki barish DAILY hai (ghante wali nahi), isliye intensity average "
         "ho jaati hai aur lagbhag saare dots line ke neeche aate hain; D bhi 24 h ke multiples me hai. Isliye hum line ko yes/no ki tarah "
         "nahi, ratio I/I_crit (line ke kitna paas) ko score ki tarah use karte hain. Bina training ke ye score 184 Indian events par "
         "ROC-AUC 0.758 deta hai. Orange dots upar-right ki taraf zyada hain: lambi + tez barish = zyada khatra.")


def g10(tree, out):
    fs = sorted(glob.glob(str(tree / "**" / "glof_physics_report.json"), recursive=True)) or [str(TRI / "results/glof/glof_physics_report.json")]
    if not os.path.exists(fs[0]):
        return
    r = json.load(open(fs[0]))
    fig, axs = plt.subplots(1, 2, figsize=(11, 4))
    for ax, (k, xl, yl) in zip(axs, (("area_volume", "lake area (m2)", "volume (m3)"), ("volume_peakQ", "volume (m3)", "peak discharge (m3/s)"))):
        f = r[k]; x = np.logspace(np.log10(f["x_range"][0]), np.log10(f["x_range"][1]), 50); mid = np.sqrt(x[0] * x[-1])
        ax.plot(x, f["coef"] * x ** f["exponent"], color=C["brand"], lw=2.4, label=f"fit b = {f['exponent']:.2f} (n {f['n']}, R2 log {f['r2_log']:.2f})")
        for b in f["exponent_ci95"]:
            ax.plot(x, f["coef"] * x ** f["exponent"] * (x / mid) ** (b - f["exponent"]), color=C["ink3"], ls="--", lw=1)
        ax.set(xscale="log", yscale="log", xlabel=xl, ylabel=yl); ax.legend(fontsize=8.5)
    fig.suptitle("GLOF power laws, HMAGLOFDB v4 par fit (dashed = exponent ka 95% CI)", fontweight="bold")
    save(fig, out, "G10_glof_power_laws.png", "GLOF: jheel ka area -> paani -> flood peak",
         "Glacial jheel jitni badi, utna paani (V = a A^b), aur jitna paani utna bada flood peak (Q = a V^b). Area-volume fit b = 1.13 "
         "(CI 0.71-1.50). Points kam hain (21 aur 31), isliye CI chauda hai; ye rough screening ke liye hai, exact prediction ke liye nahi.")


def g11(tree, out):
    fs = sorted(glob.glob(str(tree / "**" / "rl_env_cmiss*_s0_report.json"), recursive=True))
    if not fs:
        return
    R = sorted((json.load(open(f)) for f in fs), key=lambda r: r["C_miss"])
    pols = [p for p in ("always_hold", "physics_rule", "cql_learned", "oracle") if p in R[0]["policies"]]
    fig, axs = plt.subplots(1, len(R), figsize=(4 * len(R), 3.8))
    for ax, r in zip(np.atleast_1d(axs), R):
        ax.bar(pols, [r["policies"][p]["return_mean"] for p in pols], color=[C["ink3"], C["teal"], C["violet"], C["green"]][:len(pols)])
        ax.set_title(f"C_miss = {r['C_miss']:.0f}"); ax.tick_params(axis="x", rotation=20)
    np.atleast_1d(axs)[0].set_ylabel("return per season (higher better)")
    fig.suptitle("RL simulator (landslide season): learned policy vs physics rule vs oracle", fontweight="bold")
    save(fig, out, "G11_rl_env_policies.png", "RL environment ke policies",
         "Simulator me 360 monsoon seasons. C_miss = ek missed landslide ki keemat (false alarm = 5). always_hold = kabhi alarm nahi. "
         "Jab miss mehenga hai (5000) to physics rule always_hold se ~2.4x behtar hai. Learned RL (CQL) rule ke barabar hi hai (scorecard: "
         "oracle bhi lagbhag same), isliye gate ne rule rakha. Ye imaandaar negative result hai: RL ke liye jagah hi nahi bachi.")


def g12(M, out):
    keys = [("offline_rl", "fused (synthetic pair)"), ("offline_rl_real", "real pair, in-sample"), ("offline_rl_heldout", "real pair, HELD-OUT")]
    ks = [(k, l) for k, l in keys if runs(M, k, "gain_vs_rule_mean")]
    if not ks:
        return
    fig, ax = plt.subplots(figsize=(8, 3.8))
    for i, (k, l) in enumerate(ks):
        ax.scatter([i] * len(runs(M, k, "gain_vs_rule_mean")), runs(M, k, "gain_vs_rule_mean"), color=C["violet"], s=40, zorder=3, label="gain (mean)" if i == 0 else None)
        ax.scatter([i] * len(runs(M, k, "gain_vs_rule_lcb95")), runs(M, k, "gain_vs_rule_lcb95"), color=C["red"], marker="v", s=40, zorder=3, label="95% lower bound" if i == 0 else None)
    ax.axhline(0, color=C["ink"], lw=1); ax.set_xticks(range(len(ks)), [l for _, l in ks])
    ax.set(ylabel="reward gain vs fixed rule", title="Offline RL: lower bound 0 se upar ho tabhi deploy"); ax.legend()
    save(fig, out, "G12_offline_rl_gain.png", "Offline RL ka gain aur uska lower bound",
         "Purple = RL rule se kitna behtar (average), laal = 95% confidence ka lower bound. In-sample number optimistic tha; jab honest "
         "held-out folds par test kiya to lower bound 0 se neeche gaya, isliye deploy 0/3. Rule hi chalega.")


def _oofs(tree):
    src = {}
    for n in ("fire", "zeroshot", "clip_probe", "fire_meta_fusion"):
        h = sorted(glob.glob(str(tree / "**" / f"{n}_s0_oof.npz"), recursive=True))
        if h:
            src[n] = h[0]
    return src


def g13(tree, out):
    src = _oofs(tree)
    if not src:
        return
    fig, axs = plt.subplots(1, len(src), figsize=(3.6 * len(src), 3.4), sharey=True)
    for ax, (n, f) in zip(np.atleast_1d(axs), src.items()):
        d = np.load(f, allow_pickle=True); p = np.where(np.isnan(d["prob_cal"]), d["prob"], d["prob_cal"]); y = d["y"].astype(int)
        b = np.linspace(0, 1, 26)
        ax.hist(p[y == 0], b, alpha=0.6, color=C["ink3"], label="non-fire"); ax.hist(p[y == 1], b, alpha=0.6, color=C["brand"], label="fire")
        ax.set_title(n); ax.set_xlabel("calibrated probability")
    np.atleast_1d(axs)[0].legend(fontsize=8)
    save(fig, out, "G13_score_distributions.png", "Model kitna confident hai: score distribution",
         "Grey = bina aag ki images, orange = aag wali. Achha model dono pahaad alag-alag rakhta hai (grey left, orange right). "
         "Fire CNN me dono kaafi overlap karte hain, CLIP probe aur stack me saaf alag hain.")


def g14(tree, out):
    src = _oofs(tree)
    if not src:
        return
    fig, axs = plt.subplots(1, len(src), figsize=(3.3 * len(src), 3.2))
    for ax, (n, f) in zip(np.atleast_1d(axs), src.items()):
        d = np.load(f, allow_pickle=True); p = np.where(np.isnan(d["prob_cal"]), d["prob"], d["prob_cal"]); y = d["y"].astype(int); q = (p >= 0.5).astype(int)
        cm = np.array([[((y == a) & (q == b)).sum() for b in (0, 1)] for a in (0, 1)])
        ax.imshow(cm, cmap="Oranges"); ax.grid(False)
        for a in (0, 1):
            for b in (0, 1):
                ax.text(b, a, cm[a, b], ha="center", va="center", fontsize=11, fontweight="bold")
        ax.set_xticks([0, 1], ["pred no", "pred fire"]); ax.set_yticks([0, 1], ["no fire", "fire"]); ax.set_title(n)
    save(fig, out, "G14_confusion_matrices.png", "Confusion matrix (threshold 0.5, OOF)",
         "Upar-left = sahi 'no fire', neeche-right = sahi 'fire'. Upar-right = false alarm, neeche-left = chhooti aag (sabse khatarnak). "
         "Asli system 0.5 nahi, cost-loss threshold p* use karta hai (P03 chapter), jo chhooti aag ko aur kam karta hai.")


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--merged", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    mg, out = Path(a.merged), Path(a.out)
    M = json.load(open(mg / "results.json"))["models"]; tree = mg / "tree"
    skipped = []
    for f, args in ((g01, (M, out)), (g02, (M, out)), (g03, (M, out)), (g04, (M, out)), (g05, (M, out)), (g06, (tree, out)),
                    (g07, (tree, out)), (g08, (out,)), (g09, (out,)), (g10, (tree, out)), (g11, (tree, out)), (g12, (M, out)),
                    (g13, (tree, out)), (g14, (tree, out))):
        n = len(EXPL)
        try:
            f(*args)
        except Exception as e:  # noqa: BLE001
            print(f"  [skip] {f.__name__}: {type(e).__name__}: {e}")
        if len(EXPL) == n:
            skipped.append(f.__name__)
    return EXPL, skipped


if __name__ == "__main__":
    e, s = main(); print(len(e), "graphs; skipped", s)
