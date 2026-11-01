"""Merge every account's Kaggle output (out_<ACCOUNT>_<PHASE>.zip or out/ folders) + the repo's existing results/
into ONE results tree, ONE RESULTS.md (via collect_results.py) and ONE headline scorecard MASTER_RESULTS.md.

Rules (same as collect_results.py, rule 2): nothing is invented; a model missing from the inputs is "not measured".
  * ONE phase per account: `final` if present, else `phase2` (collect_results averages same-name reports as seeds,
    so mixing phases would silently blend them). Override with --prefer phase2.
  * The repo's results/ (landslide physics, GLOF, Geo-PINN, RL environment) are included unless a P/D run already
    contains the same report files.
Run:
  python kaggle/merge_all_results.py --zips out_A_final.zip out_B_final.zip out_C_phase2.zip ... --out merged
  (folders work too: --dirs /kaggle/input/<run-a>/out ...)
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                                  # TRINETRA/
REPO_RESULTS = ROOT / "results"
PHASE_RANK = {"final": 2, "phase2": 1}


def _pick(zips, prefer):
    """{account: (phase, path)} keeping one phase per account."""
    best = {}
    for z in zips:
        # browsers rename re-downloads to "out_B_final (1).zip": accept that suffix too
        m = re.search(r"out_([A-Za-z]+)_([A-Za-z0-9]+)(?: \(\d+\))?\.zip$", os.path.basename(z))
        if not m:
            print(f"[skip] {z}: name is not out_<ACCOUNT>_<PHASE>.zip"); continue
        acc, ph = m.group(1).upper(), m.group(2)
        rank = (2 if ph == prefer else 1) if prefer else PHASE_RANK.get(ph, 0)
        if acc not in best or rank > best[acc][0]:
            best[acc] = (rank, ph, z)
    return {a: (ph, z) for a, (_, ph, z) in best.items()}


def _metric(models, name, key):
    s = models.get(name) or {}
    v = s.get(key)
    return v["mean"] if isinstance(v, dict) else None


def scorecard(res, used):
    M, G = res["models"], res["geo"]
    rows = []

    def add(hazard, expert, metric, value, admitted, src, note=""):
        rows.append({"hazard": hazard, "expert": expert, "metric": metric, "value": value, "admitted": admitted,
                     "source": src, "note": note})

    def model_row(hazard, name, src, label=None):
        if name not in M:
            add(hazard, label or name, "-", None, None, src, "not measured"); return
        auc, hauc = _metric(M, name, "oof_roc_auc"), _metric(M, name, "test_roc_auc")
        add(hazard, label or name, "ROC-AUC OOF / held-out", f"{auc:.3f} / {hauc:.3f}" if auc is not None and hauc is not None
            else (f"{auc:.3f}" if auc is not None else None), M[name].get("admitted"), src,
            f"{M[name]['n_seeds']} seed(s)")

    # train_classifier.py writes the fire CNN as fire_s<seed>_report.json (name "fire"), not "fire_cnn"
    model_row("Fire / smoke (CCTV)", "fire" if "fire" in M else "fire_cnn", used.get("A", "-"), label="fire_cnn")
    model_row("Fire / smoke (CCTV)", "colorhist", used.get("A", "-"))
    model_row("Fire / smoke (zero-shot)", "zeroshot", used.get("B", "-"))
    model_row("Fire / smoke (few-shot CLIP)", "clip_probe", used.get("B", "-"))
    if "fire_meta_fusion" in M:
        s = M["fire_meta_fusion"]
        add("Fire META-FUSION (stack: fire_cnn + zeroshot + clip_probe + colorhist)", "fire_meta_fusion",
            "ROC-AUC OOF / held-out; stack − best single AUC",
            f"{_metric(M, 'fire_meta_fusion', 'oof_roc_auc'):.3f} / {_metric(M, 'fire_meta_fusion', 'test_roc_auc'):.3f}; "
            f"{_metric(M, 'fire_meta_fusion', 'meta_minus_best_auc_mean'):+.3f}"
            if _metric(M, "fire_meta_fusion", "meta_minus_best_auc_mean") is not None else None,
            s.get("admitted"), "repo results/fire_meta", f"REAL pairing; {s['n_seeds']} seed(s)")
    model_row("Fake media", "deepfake", used.get("C", "-"))
    for n in sorted(k for k in M if k.startswith("eo")):
        model_row("Satellite (EO)", n, used.get("D", "-"))
    v = M.get("video")
    if v:
        g = lambda k: _metric(M, "video", k)  # noqa: E731
        add("Fire video (temporal validator)", "video", "false-alarm videos raw → validated",
            f"{g('false_alarm_video_rate_raw'):.3f} → {g('false_alarm_video_rate_validated'):.3f}" if g("false_alarm_video_rate_raw") is not None else None,
            None, used.get("A", "-"), "small n: quote counts")
    for f, r in sorted(G.items(), key=lambda kv: (str(kv[1].get("name")), float(kv[1].get("C_miss") or 0))):
        if r.get("name") == "geo_physics":
            sc = r["scores"]; k = next((x for x in sc if "caine" in x.lower()), None)
            add("Landslide (physics, zero training)", k or "geo_physics", "ROC-AUC spatial OOF",
                f"{sc[k]['roc_auc']:.3f}" if k else None, "physics (no gate needed)", f, f"{r['n_pos']} real events, {r['n_blocks']} blocks")
        elif r.get("name") == "glof_physics":
            av = r.get("area_volume", {})
            if "exponent" in av:
                add("GLOF (lake area → volume)", "glof_physics", "exponent b (95% CI)",
                    f"{av['exponent']:.2f} ({av['exponent_ci95'][0]:.2f}-{av['exponent_ci95'][1]:.2f})", "fit", f, f"n {av['n']}")
        elif str(r.get("name", "")).startswith("rl_env"):
            P = r["policies"]
            add(f"RL alarm policy (C_miss {int(r['C_miss'])})", "cql_learned vs physics_rule", "return CQL / rule / oracle",
                f"{P['cql_learned']['return_mean']:.1f} / {P['physics_rule']['return_mean']:.1f} / {P['oracle_true_hazard']['return_mean']:.1f}",
                f"deploy {r['deploy_learned']}", f, f"LCB {r['gain_vs_rule_lcb95']:+.2f}; SIMULATOR")
    if "geo_pinn" in M:
        model_row("Landslide (Geo-PINN)", "geo_pinn", "repo results/geo_pinn")
    if "geo_fusion" in M:
        s = M["geo_fusion"]
        add("Landslide META-FUSION (physics + rain, FM-1)", "geo_fusion", "ROC-AUC OOF (calibrated FM-1)",
            f"{_metric(M, 'geo_fusion', 'oof_roc_auc'):.3f}" if _metric(M, "geo_fusion", "oof_roc_auc") is not None else None,
            s.get("admitted"), used.get("P", used.get("D", "-")), f"REAL pairing; {s['n_seeds']} seed(s)")
    if "offline_rl" in M:
        s = M["offline_rl"]
        add("RL on fused alerts", "offline_rl", "gain vs rule (LCB)",
            f"{_metric(M, 'offline_rl', 'gain_vs_rule_mean'):+.3f} ({_metric(M, 'offline_rl', 'gain_vs_rule_lcb95'):+.3f})"
            if _metric(M, "offline_rl", "gain_vs_rule_mean") is not None else None, f"deploy {s.get('deploy_learned')}", used.get("F", "-"))
    if "offline_rl_real" in M:
        s = M["offline_rl_real"]
        add("RL on REAL-paired fire meta-fusion", "offline_rl_real", "gain vs rule (LCB)",
            f"{_metric(M, 'offline_rl_real', 'gain_vs_rule_mean'):+.3f} ({_metric(M, 'offline_rl_real', 'gain_vs_rule_lcb95'):+.3f})"
            if _metric(M, "offline_rl_real", "gain_vs_rule_mean") is not None else None, f"deploy {s.get('deploy_learned')}",
            "repo results/offline_rl_real", f"{s['n_seeds']} seed(s); OPE in-sample (optimistic)")
    if "offline_rl_heldout" in M:
        s = M["offline_rl_heldout"]; g = lambda k: _metric(M, "offline_rl_heldout", k)  # noqa: E731
        add("RL HELD-OUT (block folds, true reward)", "offline_rl_heldout", "CQL gain vs rule / vs tuned rule (LCB)",
            f"{g('gain_vs_rule_mean'):+.3f} ({g('gain_vs_rule_lcb95'):+.3f}) / {g('gain_vs_tuned_rule_mean'):+.3f} ({g('gain_vs_tuned_rule_lcb95'):+.3f})"
            if g("gain_vs_rule_mean") is not None else None, f"deploy {s.get('deploy_learned')}", "repo results/offline_rl_heldout",
            f"{s['n_seeds']} seed(s); replaces the in-sample OPE number")
    if "crossmodal" in M:
        s = M["crossmodal"]; g = lambda k: _metric(M, "crossmodal", k)  # noqa: E731
        add("Fire CROSS-MODAL (per-frame stack + temporal validator, FireSense)", "crossmodal",
            "video J (detect − FA): stack / clip_probe / fire_cnn",
            f"{g('stack_video_J'):+.3f} / {g('clip_video_J'):+.3f} / {g('fire_cnn_video_J'):+.3f}" if g("stack_video_J") is not None else None,
            None, used.get("X", "-"), f"{s['n_seeds']} seed(s); small n (49 videos)")
    if "stress" in M:
        s = M["stress"]; g = lambda k: _metric(M, "stress", k)  # noqa: E731
        add("Fire CONFUSER-AWARE retrain (leave-one-confuser-set-out)", "stress",
            "FA at equal recall 0.90: probe base → conf / stack base → conf; DeepFire AUC base → conf",
            f"{g('fa_thr90_probe_base_mean'):.3f} → {g('fa_thr90_probe_conf_mean'):.3f} / {g('fa_thr90_stack_base_mean'):.3f} → "
            f"{g('fa_thr90_stack_conf_mean'):.3f}; {g('test_auc_probe_base'):.3f} → {g('test_auc_probe_conf'):.3f}"
            if g("fa_thr90_probe_base_mean") is not None else None, s.get("admitted"), used.get("S", "-"), f"{s['n_seeds']} seed(s)")
    if res.get("fusion"):
        fr = res["fusion"]["rules"]
        best = max(fr, key=lambda k: fr[k]["value_score"]["mean"])
        add("Fusion (all experts)", best, "value score (best rule) / FM-1",
            f"{fr[best]['value_score']['mean']:.3f} / {fr.get('fm1', fr[best])['value_score']['mean']:.3f}", None, used.get("F", "-"),
            "SYNTHETIC pairing of real OOF scores")
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--zips", nargs="*", default=[]); ap.add_argument("--dirs", nargs="*", default=[])
    ap.add_argument("--out", default="merged"); ap.add_argument("--prefer", choices=["final", "phase2"], default=None)
    ap.add_argument("--no-repo", action="store_true", help="do not add the repo's results/ folder")
    a = ap.parse_args(argv)
    out = Path(a.out); tree = out / "tree"
    if tree.exists():
        shutil.rmtree(tree)
    tree.mkdir(parents=True)
    used = {}
    for acc, (ph, z) in sorted(_pick(a.zips, a.prefer).items()):
        dst = tree / f"{acc}_{ph}"; zipfile.ZipFile(z).extractall(dst)
        for junk in dst.glob("results"):          # the per-run summary is regenerated below
            shutil.rmtree(junk)
        used[acc] = f"{acc} {ph} ({os.path.basename(z)})"; print(f"[use] {used[acc]}")
    for d in a.dirs:
        dst = tree / f"dir_{Path(d).parent.name or Path(d).name}"; shutil.copytree(d, dst, dirs_exist_ok=True)
        shutil.rmtree(dst / "results", ignore_errors=True); used[f"dir:{d}"] = d
    # geo / physics / RL belong to account P: if a P run is present, drop the same reports from D or ALL runs
    # (older D notebooks also ran the geo stage), otherwise they would be counted twice as extra seeds
    if any(k == "P" for k in used):
        GEO_PAT = re.compile(r"(geo_physics|geo_pinn|geo_fusion|glof_physics|rl_env)")
        for acc_dir in [d for d in tree.iterdir() if d.is_dir() and re.match(r"(D|ALL)_", d.name)]:
            for f in acc_dir.rglob("*"):
                if f.is_file() and GEO_PAT.search(f.name):
                    f.unlink(); print(f"[geo-owner P] dropped {f.relative_to(tree)}")
    # the fusion run (F) re-ships the A/B/C reports it imported (same run_id) or re-runs them in-session (e.g. B's
    # zeroshot/clip_probe, new run_id, same seed): keep the owning account's copy so a model is never counted twice
    # as an extra "seed"
    seen = set()
    # F (fusion) and X (cross-modal) re-run B's zeroshot/clip_probe in-session; the owning account's copy wins
    rerun = lambda p: "/F_" in p or "/X_" in p or "/S_" in p  # noqa: E731
    for f in sorted(glob.glob(str(tree / "**" / "*_report.json"), recursive=True), key=lambda p: (rerun(p), p)):
        try:
            rep = json.load(open(f)); rid = rep.get("run_id")
        except Exception:
            continue
        key = (os.path.basename(f), rid)
        if (rid and key in seen) or (rerun(f) and (os.path.basename(f), "owner") in seen):
            os.remove(f); print(f"[dedupe] {os.path.relpath(f, tree)} (already counted)")
        seen.add(key)
        # the first kept copy owns the report name: the owning account if present, else the first re-run (F before S before X),
        # so X's re-shipped copies of F's offline RL (or of S's stress) are not counted as extra seeds
        seen.add((os.path.basename(f), "owner"))
    if not a.no_repo and REPO_RESULTS.exists():
        have = {os.path.basename(f) for f in glob.glob(str(tree / "**" / "*_report.json"), recursive=True)}
        for sub in ("geo_large", "glof", "rl_env", "geo_pinn", "geo_fusion", "fire_meta", "offline_rl_real", "offline_rl_heldout"):
            src = REPO_RESULTS / sub
            if src.exists() and not ({p.name for p in src.glob("*_report.json")} & have):
                shutil.copytree(src, tree / "repo" / sub, dirs_exist_ok=True)
        used.setdefault("P", "repo results/ (geo, GLOF, RL env, Geo-PINN)")
    subprocess.run([sys.executable, str(HERE / "collect_results.py"), "--inp", str(tree), "--out", str(out)], check=True,
                   stdout=subprocess.DEVNULL)
    res = json.load(open(out / "results.json"))
    rows = scorecard(res, used)
    L = ["# TRINETRA — MASTER RESULTS (all accounts merged)", "",
         "Every number is OUR RESULT on the prototype pack (not comparable to full-benchmark papers). "
         "Admitted = beat climatology and logistic baselines on cost-weighted value with a 95% CI (Rule 16).", "",
         "## Runs used (one phase per account)", ""] + [f"- **{k}**: {v}" for k, v in sorted(used.items())] + [
         "", "## Scorecard", "", "| hazard | expert | metric | value | admitted / deploy | note |", "|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['hazard']} | {r['expert']} | {r['metric']} | {r['value'] if r['value'] is not None else 'not measured'} "
                 f"| {r['admitted'] if r['admitted'] is not None else '-'} | {r['note']} |")
    adm = [r for r in rows if isinstance(r["admitted"], str) and re.match(r"[1-9]\d*/", r["admitted"])]
    L += ["", "## Headline", "",
          f"- Admitted learned experts: **{len(adm)}** ({', '.join(r['expert'] for r in adm) or 'none yet'})."]
    phys = [r for r in rows if r["hazard"].startswith("Landslide (physics")]
    if phys:
        L.append(f"- Landslide physics with zero training: ROC-AUC **{phys[0]['value']}** ({phys[0]['note']}).")
    rl = [r for r in rows if r["hazard"].startswith("RL alarm")]
    if rl:
        L.append("- RL: built, trained and tested online in the physics simulator at every cost ratio; the physics rule is within "
                 "noise of the oracle, so the gate kept the rule (" + "; ".join(f"{r['hazard'].split('(')[1][:-1]}: {r['admitted']}" for r in rl) + ").")
    L += ["", "Full tables: `RESULTS.md` (same folder)."]
    (out / "MASTER_RESULTS.md").write_text("\n".join(L) + "\n")
    json.dump({"used": used, "scorecard": rows}, open(out / "master.json", "w"), indent=2)
    print("\n".join(L))


if __name__ == "__main__":
    main()
