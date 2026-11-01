"""Extract data/animation_data.json for TRINETRA Live Flow from the repo (stdlib only; no numpy needed).

Every element is {value, unit?, origin, source, note?} with origin in REAL_RESULT | REAL_CONFIG | PAPER | ILLUSTRATIVE.
Values that cannot be found are logged in `missing` and the animation shows them with an ILLUSTRATIVE ribbon.
Run from the workspace root:  python TRINETRA/ANIM/tools/extract_animation_data.py
Writes public/anim/data/animation_data.json (served by the app at /anim/) and TRINETRA/ANIM/data/animation_data.json.
"""
from __future__ import annotations

import ast
import csv
import io
import json
import math
import os
import re
import struct
import zipfile
from pathlib import Path

WS = Path(__file__).resolve().parents[3]          # workspace root
T = WS / "TRINETRA"
SRC = T / "trinetra" / "src" / "trinetra"
MISSING: list[str] = []


def item(value, origin, source, unit=None, note=None):
    d = {"value": value, "origin": origin, "source": source}
    if unit:
        d["unit"] = unit
    if note:
        d["note"] = note
    return d


def rel(p: Path) -> str:
    return str(p.relative_to(WS))


def line_of(path: Path, pattern: str) -> str:
    """'path:line' of the first line matching pattern, or path if not found."""
    try:
        for i, ln in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if re.search(pattern, ln):
                return f"{rel(path)}:{i}"
    except FileNotFoundError:
        pass
    MISSING.append(f"pattern {pattern!r} in {path}")
    return rel(path)


def load_json(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:
        MISSING.append(str(p)); return None


# ------------------------------------------------------------------ .npz without numpy
def read_npz(path: Path) -> dict:
    out = {}
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            b = z.read(name)
            if b[:6] != b"\x93NUMPY":
                continue
            major = b[6]
            hl = struct.unpack("<H", b[8:10])[0] if major == 1 else struct.unpack("<I", b[8:12])[0]
            off = 10 if major == 1 else 12
            hdr = ast.literal_eval(b[off:off + hl].decode("latin1"))
            data = b[off + hl:]
            descr, shape = hdr["descr"], hdr["shape"]
            n = 1
            for s in shape:
                n *= s
            fmt = {"<f8": "d", "<f4": "f", "<i8": "q", "<i4": "i", "|b1": "?"}.get(descr)
            if fmt is None:
                continue
            size = struct.calcsize(fmt)
            out[name[:-4]] = list(struct.unpack("<" + fmt * n, data[:size * n]))
    return out


def roc_points(p, y, k=60):
    """Threshold sweep (k thresholds) -> list of {t, tpr, fpr, precision, alarms_frac}."""
    pts = []
    P = sum(y); N = len(y) - P
    for i in range(k + 1):
        t = i / k
        tp = sum(1 for pi, yi in zip(p, y) if pi >= t and yi == 1)
        fp = sum(1 for pi, yi in zip(p, y) if pi >= t and yi == 0)
        pts.append({"t": round(t, 4), "tpr": tp / P if P else 0, "fpr": fp / N if N else 0,
                    "precision": tp / (tp + fp) if tp + fp else 1.0})
    return pts


def reliability(p, y, bins=10):
    out = []
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i, pi in enumerate(p) if (lo <= pi < hi) or (b == bins - 1 and pi == 1.0)]
        if idx:
            out.append({"bin": round((lo + hi) / 2, 3), "conf": sum(p[i] for i in idx) / len(idx),
                        "acc": sum(y[i] for i in idx) / len(idx), "n": len(idx)})
    return out


# ------------------------------------------------------------------ sections
def modules():
    M = [("data_adapters", "Adapters (build_npz · build_geo · build_eo)", T / "data_adapters/build_npz.py", "DATA"),
         ("fire_cnn", "Fire CNN + GRU (FireSmokeNet)", SRC / "deep/fire_cnn.py", "PERCEPTION"),
         ("zeroshot", "Zero-shot CLIP (open_clip)", T / "trinetra/kaggle/eval_zeroshot.py", "PERCEPTION"),
         ("temporal", "Temporal validator (persistence)", SRC / "ws4_cctv/__init__.py", "PERCEPTION"),
         ("deepfake", "Media authenticity (RGB + FFT)", SRC / "deep/deepfake_net.py", "PERCEPTION"),
         ("eo", "EO heads (S1 · S2 · InSAR)", SRC / "deep/eo_encoder.py", "PERCEPTION"),
         ("anomaly", "Anomaly ensemble (no labels)", SRC / "ws8_anomaly/__init__.py", "PERCEPTION"),
         ("firephys", "Fire physics gate", SRC / "ws1a_firephys/gate.py", "PHYSICS"),
         ("geophys", "Geo physics gate (FS · Iverson · Caine)", SRC / "ws1b_geophys/gate.py", "PHYSICS"),
         ("fusion", "Meta-fusion FM-1 (+ PHARAOH, GMF)", SRC / "ws5_fusion_rl/fusion_models.py", "FUSION"),
         ("calibration", "Cross-fit temperature calibration", SRC / "deep/oof_utils.py", "FUSION"),
         ("geo_fusion", "Landslide meta-fusion (real pairing)", T / "trinetra/kaggle/geo_meta_fusion.py", "FUSION"),
         ("decision", "Decision + cost threshold", SRC / "ws5_fusion_rl/decision.py", "DECISION"),
         ("shield", "Physics shield (raise-only)", SRC / "ws5_fusion_rl/shield.py", "DECISION"),
         ("rl", "RL advisory (CQL + gate)", SRC / "deep/offline_rl.py", "DECISION"),
         ("operator", "Human approval gate", SRC / "ws3_alert/operator.py", "HUMAN"),
         ("cap", "CAP 1.2 alert builder (human-gated)", SRC / "ws3_alert/cap.py", "HUMAN"),
         ("dtn", "Store-and-forward queue (offline)", SRC / "ws3_alert/dtn.py", "HUMAN"),
         ("cyclone", "Cyclone module", T / "docs/13_CYCLONE_MODULE_SPEC.md", "PHYSICS")]
    out = []
    for mid, name, path, layer in M:
        exists = path.exists()
        status = "PLANNED" if mid == "cyclone" else ("IMPLEMENTED" if exists else "NOT FOUND IN REPO")
        if not exists:
            MISSING.append(f"module file {path}")
        out.append({"id": mid, "name": name, "file": rel(path) if exists else str(path), "layer": layer, "status": status})
    return out


def datasets():
    rows = list(csv.DictReader(open(T / "docs/09b_dataset_links.csv", encoding="utf-8")))
    out = []
    for r in rows:
        out.append({"id": r["ID"], "name": r["name"], "modules": r["modules"], "task": r["task"], "link": r["link"],
                    "license": r["license"], "size_full": r["size_full"], "size_subset": r["size_subset"],
                    "role": r["role"], "known_issues": r["known_problems"], "mitigation": r["format_adapter"],
                    "status": r["status"], "origin": "REAL_CONFIG", "source": "TRINETRA/docs/09b_dataset_links.csv"})
    return out


def conversion():
    idx = list(csv.DictReader(open(T / "data_manifests/tpd_index.csv", encoding="utf-8")))
    groups = len({r["group_id"] for r in idx}); pos = sum(1 for r in idx if r["raw_label"] == "1")
    src = "TRINETRA/docs/09d_CONVERSION_REPORT.md · TRINETRA/data_manifests/tpd_index.csv"
    conv = {"tpd": {"input_rows": item(len(idx), "REAL_RESULT", src), "output_rows": item(len(idx), "REAL_RESULT", src),
                    "dropped_rows": item(0, "REAL_RESULT", src), "positives": item(pos, "REAL_RESULT", src),
                    "controls": item(len(idx) - pos, "REAL_RESULT", src), "spatial_groups": item(groups, "REAL_RESULT", src),
                    "split": item("spatial_cv_oof (5 folds, whole blocks)", "REAL_RESULT", src),
                    "provenance": item("SOURCE+DERIVED; synthetic 0; own-captured 0", "REAL_RESULT", src)}}
    zs = load_json(T / "results/zeroshot_final/zeroshot_s0_report.json")
    if zs:
        s = "TRINETRA/results/zeroshot_final/zeroshot_s0_report.json"
        conv["fire_pack"] = {"oof_rows": item(zs["oof_n"], "REAL_RESULT", s, note="D-Fire train+val, group CV"),
                             "heldout_rows": item(zs["test_n"], "REAL_RESULT", s, note="DeepFire, deduped against D-Fire"),
                             "stress": {k: item(v["n"], "REAL_RESULT", s) for k, v in zs.get("stress", {}).items()}}
    return conv


def failure_patterns():
    out = []
    ladder = {"P1": "C2", "P2": "C3", "P3": "C2", "P4": "C2", "P5": "C3", "P6": "C2", "P7": "C2", "P8": "C3", "P9": "C1",
              "P10": "C1", "P11": "C3", "P12": "C2", "P13": "C2", "P14": "C2"}
    answer = {"P1": "cost-loss threshold + temporal validator", "P2": "zero-label physics prior works day one",
              "P3": "multi-expert fusion; a missing expert gets weight 0", "P4": "physics + held-out datasets + drift flag",
              "P5": "calibrated p and U*; abstain to a human", "P6": "numpy core + store-and-forward alert queue",
              "P7": "p_fake lowers media trust", "P8": "group splits, dedupe, admission gate",
              "P9": "tiered CAP alerts, store-and-forward", "P10": "small CNN, numpy edge runtime",
              "P11": "online truth + CI deploy gate", "P12": "advisory only; a human approves",
              "P13": "PSI/CUSUM drift flag voids guarantees", "P14": "no raw-video egress guard"}
    for ln in (T / "docs/17_EXISTING_SYSTEMS_AND_FAILURES.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| (P\d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|", ln)
        if m:
            pid = m.group(1)
            out.append({"id": pid, "pattern": m.group(2).strip(), "hinglish": m.group(3).strip(), "evidence": m.group(4).strip(),
                        "answer": answer.get(pid, ""), "ladder": ladder.get(pid, "C1"),
                        "source": "TRINETRA/docs/17_EXISTING_SYSTEMS_AND_FAILURES.md"})
    return out


def surveys():
    s = "TRINETRA/docs/26_INDIA_DISASTER_IMPACT_10YR_HINGLISH.md"
    R = [("wmo", "8×", "higher disaster death rate where early-warning coverage is limited",
          "WMO + UNDRR, Global Status of Multi-Hazard Early Warning Systems 2023 (country survey)", "A"),
         ("gca24", "−30%", "damage when a storm or heatwave is warned just 24 h ahead", "Global Commission on Adaptation, Adapt Now (2019)", "A"),
         ("gca800", "$3–16 bn / yr", "losses avoidable by spending $800 M on early warning in developing countries",
          "Global Commission on Adaptation (2019)", "A"),
         ("odisha", "10,000 → 64", "Odisha cyclone deaths, 1999 super cyclone vs Fani 2019 (≈12 lakh evacuated)", "OSDMA / IMD", "A"),
         ("cse24", "255 / 274 days", "extreme-weather days in India, Jan–Sep 2024; 3,238 deaths", "CSE / Down To Earth, State of Extreme Weather 2024", "A"),
         ("undrr", "$79.5 bn", "India's climate-related disaster losses 1998–2017", "UNDRR + CRED, Economic Losses, Poverty & Disasters", "A"),
         ("relief", "~₹36,000 cr / yr", "earmarked for disaster response and relief (SDRF + NDRF, 2021–26)", "15th Finance Commission", "B"),
         ("rumour", "33 killed", "in 69 mob attacks fuelled by WhatsApp child-lifting rumours, 2017–18", "IndiaSpend analysis (2018)", "A"),
         ("heat", "~1,190 / yr", "deaths avoided by the Ahmedabad Heat Action Plan (estimate)", "Hess et al., 2018", "A")]
    return [{"id": i, "value": v, "label": l, "origin": "PAPER", "source": f"{src} (via {s})",
             "confidence": c, "note": "public report or survey; confidence A = widely published, B = verify before quoting"}
            for i, v, l, src, c in R]


def physics():
    g = SRC / "ws1b_geophys/gate.py"; f = SRC / "ws1a_firephys/established_ef.py"
    return [
        {"id": "caine", "name": "Caine rainfall intensity–duration threshold", "class": "A",
         "equation": "I_thr = a · D^(−b)", "symbols": [["I", "rain intensity", "mm/h"], ["D", "rain duration", "h"], ["a, b", "fitted constants", "-"]],
         "parameters": [item(14.0, "REAL_CONFIG", line_of(g, r"caine_a"), "-", "a (coeff-verify)"),
                        item(0.39, "REAL_CONFIG", line_of(g, r"caine_b"), "-", "b (coeff-verify)")],
         "regime": "shallow rain-triggered slides; refit locally", "validation": item("ROC-AUC 0.758 on 184 real events (no fit)", "REAL_RESULT", "TRINETRA/results/geo_large/geo_physics_s0_report.json")},
        {"id": "fs", "name": "Infinite-slope factor of safety", "class": "A",
         "equation": "FS = [c′ + (γ z cos²β − u_w) tan φ′] / (γ z sinβ cosβ)",
         "symbols": [["c′", "effective cohesion", "kPa"], ["φ′", "friction angle", "°"], ["γ", "soil unit weight", "kN/m³"],
                     ["z", "slip depth", "m"], ["β", "slope angle", "°"], ["u_w", "pore pressure", "kPa"]],
         "parameters": [item(32.0, "REAL_CONFIG", "TRINETRA/trinetra/kaggle/geo_physics_hindcast.py (phi_prime_deg=32.0)", "°", "φ′"),
                        item(19.0, "REAL_CONFIG", "TRINETRA/trinetra/kaggle/geo_physics_hindcast.py (gamma=19.0)", "kN/m³", "γ"),
                        item(2.0, "REAL_CONFIG", "TRINETRA/trinetra/kaggle/geo_physics_hindcast.py (z=2.0)", "m", "z")],
         "regime": "planar slip parallel to surface; soil strength back-analysed (FS_dry = 1.2)",
         "validation": item("FS < 1 raises the level to ORANGE (shield)", "REAL_CONFIG", line_of(SRC / "ws5_fusion_rl/shield.py", r"FS < 1.0"))},
        {"id": "iverson", "name": "Iverson transient pore-pressure head", "class": "A",
         "equation": "ψ = (I_z / K_z) · R(Z, t),  D₁ = D₀ / cos²β",
         "symbols": [["I_z", "infiltration flux", "m/s"], ["K_z", "hydraulic conductivity", "m/s"], ["D₀", "hydraulic diffusivity", "m²/s"]],
         "parameters": [item("D₁ = D₀ / cos²β", "REAL_CONFIG", line_of(SRC / "ws1b_geophys/iverson.py", r"def diffusivity_D1"))],
         "regime": "I ≤ K_z; 1-D vertical infiltration", "validation": item("ΔFS ROC-AUC 0.750 (no fit)", "REAL_RESULT", "TRINETRA/results/geo_large/geo_physics_s0_report.json")},
        {"id": "dfs", "name": "Rain-driven FS drop ΔFS", "class": "B", "parent": "fs + iverson",
         "equation": "ΔFS = γ_w ψ tan φ′ / (γ z sinβ cosβ)",
         "reduction": "ψ → 0 ⇒ ΔFS → 0 (dry slope keeps its static FS)", "symbols": [["γ_w", "unit weight of water", "kN/m³"], ["ψ", "pressure head", "m"]],
         "parameters": [], "regime": "independent of the unknown c′", "validation": item("ROC-AUC 0.750", "REAL_RESULT", "TRINETRA/results/geo_large/geo_physics_s0_report.json")},
        {"id": "heskestad", "name": "Heskestad mean flame height", "class": "A", "equation": "L = 0.235 Q^(2/5) − 1.02 D",
         "symbols": [["L", "flame height", "m"], ["Q", "heat release rate", "kW"], ["D", "fire diameter", "m"]],
         "parameters": [item("0.235, 1.02", "REAL_CONFIG", line_of(f, r"0\.235"))], "regime": "pool fires; not validated on our data",
         "validation": item("not tested on real data", "REAL_CONFIG", rel(f))},
        {"id": "cyclone_holland", "name": "Holland parametric wind profile (cyclone)", "class": "A", "equation": "spec only (docs/13)",
         "symbols": [], "parameters": [], "regime": "PLANNED: nothing implemented", "validation": item("PLANNED", "REAL_CONFIG", "TRINETRA/docs/13_CYCLONE_MODULE_SPEC.md")},
    ]


def fusion():
    cfg = load_json(T / "trinetra/configs/fusion.json") or {}; d = load_json(T / "trinetra/configs/default.json") or {}
    fc = "TRINETRA/trinetra/configs/fusion.json"; dc = "TRINETRA/trinetra/configs/default.json"
    C_FA, C_miss = d.get("cost", {}).get("C_FA", 5.0), d.get("cost", {}).get("C_miss", 100.0)
    caps = {}
    for ln in (SRC / "ws5_fusion_rl/adapters.py").read_text().splitlines():
        m = re.match(r'\s+"(\w+)":\s+\(([\d.]+), ([\d.]+), PhysicsClass\.(\w+)\)', ln)
        if m:
            caps[m.group(1)] = {"default_r": float(m.group(2)), "cap": float(m.group(3)), "class": m.group(4)}
    return {"model": item(cfg.get("fusion", {}).get("model", "FM-1"), "REAL_CONFIG", fc),
            "tau": item(cfg.get("fusion", {}).get("tau", 0.5), "REAL_CONFIG", fc),
            "lambda": item(cfg.get("fusion", {}).get("lambda", 0.3), "REAL_CONFIG", fc),
            "pharaoh_on": item(cfg.get("fusion", {}).get("operator", {}).get("pharaoh", False), "REAL_CONFIG", fc),
            "C_FA": item(C_FA, "REAL_CONFIG", dc), "C_miss": item(C_miss, "REAL_CONFIG", dc),
            "p_star": item(round(C_FA / (C_FA + C_miss), 4), "REAL_CONFIG", "p* = C_FA/(C_FA+C_miss) · " + dc),
            "tiers": item("YELLOW ≥ p*, ORANGE ≥ 4p*, RED ≥ 10p*", "REAL_CONFIG", line_of(SRC / "ws5_fusion_rl/decision.py", r"t_y, t_o, t_r")),
            "uncertain_threshold": item(0.6, "REAL_CONFIG", line_of(SRC / "ws5_fusion_rl/decision.py", r"uncertain_threshold: float")),
            "weight_rule": item("w̃ = a · r · c · exp(−u/τ)", "REAL_CONFIG", line_of(SRC / "ws5_fusion_rl/nf.py", r"def effective_weight")),
            "consistency_rule": item("c = exp(−((p − φ)₊)² / 2σ²), σ = 0.25", "REAL_CONFIG", line_of(SRC / "ws5_fusion_rl/nf.py", r"def nf1_consistency")),
            "u_star_rule": item("U* = Σ w̄u + λ √Σ w̄(p − p̄)²", "REAL_CONFIG", line_of(SRC / "ws5_fusion_rl/nf.py", r"def nf3_conflict_to_uncertainty")),
            "trust_caps": item(caps, "REAL_CONFIG", "TRINETRA/trinetra/src/trinetra/ws5_fusion_rl/adapters.py"),
            "calibration": item("temperature T fitted on other folds only (cross-fit)", "REAL_CONFIG", line_of(SRC / "deep/oof_utils.py", r"def crossfit_calibrate")),
            "temporal_validator": item({"window": 5, "min_frames": 3, "conf_thr": 0.5}, "REAL_CONFIG", line_of(SRC / "ws4_cctv/__init__.py", r"def __init__\(self, window")),
            "worked_example": item({"experts": [["CCTV detector", 0.8, 0.2, 0.9], ["Sensor stream", 0.6, 0.1, 0.8], ["Media check", 0.1, 0.5, 0.4]],
                                    "fused": 0.6335, "level": "RED"}, "REAL_CONFIG", "TRINETRA/docs/07_RL_AND_META_FUSION_HINGLISH.md · src/deck/numbers.json (ex_p)",
                                   note="WORKED EXAMPLE computed with the repo fusion code; not a field result")}


def results():
    R = {}
    g = load_json(T / "results/geo_large/geo_physics_s0_report.json")
    if g:
        s = "TRINETRA/results/geo_large/geo_physics_s0_report.json"
        for k, v in g["scores"].items():
            R[f"geo_{k}"] = item(round(v["roc_auc"], 3), "REAL_RESULT", s, note=f"ROC-AUC, {g['n']} rows, {g['n_blocks']} spatial blocks, seed 0")
        d = g["physics_minus_rain_auc"]
        R["geo_phys_minus_rain"] = item(f"{d['mean']:+.3f} [{d['ci95'][0]:+.3f}, {d['ci95'][1]:+.3f}]", "REAL_RESULT", s, note="95% block-bootstrap CI")
    gp = load_json(T / "results/geo_pinn/geo_pinn_s0_report.json")
    if gp:
        R["geo_pinn"] = item(round(gp.get("oof_roc_auc", float("nan")), 3), "REAL_RESULT", "TRINETRA/results/geo_pinn/geo_pinn_s0_report.json", note="NOT admitted")
    rl = {}
    for c in (100, 1000, 5000):
        r = load_json(T / f"results/rl_env/rl_env_cmiss{c}_s0_report.json")
        if r:
            rl[str(c)] = {k: round(v["return_mean"], 1) for k, v in r["policies"].items()}
            rl[str(c)]["lcb"] = round(r["gain_vs_rule_lcb95"], 2); rl[str(c)]["deploy"] = r["deploy_learned"]
    R["rl_env"] = item(rl, "REAL_RESULT", "TRINETRA/results/rl_env/", note="SIMULATOR with 360 real NASA POWER rain seasons")
    z = load_json(T / "results/zeroshot_final/zeroshot_s0_report.json")
    if z:
        s = "TRINETRA/results/zeroshot_final/zeroshot_s0_report.json"
        R["zeroshot"] = item({"oof_auc": round(z["oof_roc_auc"], 3), "heldout_auc": round(z["test_roc_auc"], 3),
                              "recall_fpr05": round(z["oof_recall_at_fpr05"], 3), "admitted": z["admitted"],
                              "ece_cal": round(z["ece_crossfit_calibrated"], 3), "ece_raw": round(z["ece_raw"], 3),
                              "fa_at_0p5": {k: round(v["fa_rate_at_0p5_cal"], 3) for k, v in z["stress"].items()}},
                             "REAL_RESULT", s, note=f"run {z['run_id']}; ViT-B-32 v1 prompts")
    gl = load_json(T / "results/glof/glof_physics_report.json")
    if gl and "area_volume" in gl:
        av = gl["area_volume"]
        R["glof_av"] = item(f"b = {av['exponent']:.2f} [{av['exponent_ci95'][0]:.2f}, {av['exponent_ci95'][1]:.2f}], n {av['n']}",
                            "REAL_RESULT", "TRINETRA/results/glof/glof_physics_report.json")
    for k in ("fire_cnn", "deepfake", "eo", "clip_probe", "geo_fusion", "fusion_fire"):
        R[k] = item("RESULT PENDING", "REAL_RESULT", "Kaggle stage running", note="never estimated")
    return R


def real_curves():
    out = {}
    p = T / "results/zeroshot_final/zeroshot_s0_oof.npz"
    if p.exists():
        d = read_npz(p)
        prob = d.get("prob_cal") or d.get("prob"); y = [int(v) for v in d.get("y", [])]
        keep = [(a, b) for a, b in zip(prob or [], y) if not (isinstance(a, float) and math.isnan(a))]
        if keep:
            pp, yy = [a for a, _ in keep], [b for _, b in keep]
            out["zeroshot_threshold"] = item({"points": roc_points(pp, yy), "reliability": reliability(pp, yy), "n": len(pp),
                                              "pos": sum(yy)}, "REAL_RESULT", rel(p), note="calibrated OOF scores, D-Fire group CV")
    else:
        MISSING.append(str(p))
    ev = T / "results/geo_large/geo_events.csv"
    if ev.exists():
        rows = list(csv.DictReader(open(ev)))
        def num(r, k):
            try:
                return float(r[k])
            except Exception:
                return None
        ev_ratio = [num(r, "caine_ratio") for r in rows if r["label"] == "1"]
        ct_ratio = [num(r, "caine_ratio") for r in rows if r["label"] == "0"]
        bins = [i / 4 for i in range(-12, 9)]           # log10 ratio bins
        def hist(v):
            v = [math.log10(x) for x in v if x and x > 0]
            return [sum(1 for x in v if bins[i] <= x < bins[i + 1]) for i in range(len(bins) - 1)]
        out["caine_hist"] = item({"bins_log10": bins, "events": hist(ev_ratio), "controls": hist(ct_ratio)},
                                 "REAL_RESULT", rel(ev), note="Caine ratio I/I_thr on real landslide days vs same-site control days")
        site = None
        for r in rows:
            if r["label"] == "1":
                ctrl = [c for c in rows if c["event_id"] == r["event_id"] and c["label"] == "0"]
                if ctrl:
                    site = (r, ctrl[0]); break
        if site:
            keys = ["day", "slope_p90_deg", "rain_1d", "rain_3d", "rain_7d", "rain_30d", "caine_ratio", "dfs", "fs_backcalc"]
            out["landslide_pair"] = item({"event": {k: site[0][k] for k in keys}, "control": {k: site[1][k] for k in keys},
                                          "lat": site[0]["lat"], "lon": site[0]["lon"]}, "REAL_RESULT", rel(ev),
                                         note="one real catalogued landslide day and a same-site control day")
    return out


def main():
    data = {"generated_by": "TRINETRA/ANIM/tools/extract_animation_data.py", "modules": modules(), "datasets": datasets(),
            "conversion": conversion(), "failure_patterns": failure_patterns(), "surveys": surveys(), "physics": physics(),
            "fusion": fusion(), "results": results(), "curves": real_curves(),
            "scenarios_note": item("Fire, steam and fake-media scenarios are SIMULATED REPLAY (seeded); no per-frame cached outputs exist in the repo yet",
                                   "ILLUSTRATIVE", "TRINETRA/ANIM/ANIM_STATE.md"),
            "missing": MISSING}
    # completeness: share of badge-carrying values that are not ILLUSTRATIVE
    s = json.dumps(data)
    real = s.count('"origin": "REAL_') + s.count('"origin": "PAPER"'); ill = s.count('"origin": "ILLUSTRATIVE"')
    data["completeness"] = round(real / max(1, real + ill), 3)
    for out in (WS / "public/anim/data/animation_data.json", T / "ANIM/data/animation_data.json"):
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    # window globals so index.html also works from file:// (offline, no fetch)
    (WS / "public/anim/data/animation_data.js").write_text("window.ANIM_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n")
    sc = WS / "public/anim/data/script.json"
    if sc.exists():
        (WS / "public/anim/data/script.js").write_text("window.ANIM_SCRIPT = " + sc.read_text() + ";\n")
    print(f"[extract] modules {len(data['modules'])} · datasets {len(data['datasets'])} · failure patterns {len(data['failure_patterns'])} "
          f"· surveys {len(data['surveys'])} · completeness {data['completeness']:.0%} · missing {len(MISSING)}")
    for m in MISSING:
        print("  missing:", m)


if __name__ == "__main__":
    main()
