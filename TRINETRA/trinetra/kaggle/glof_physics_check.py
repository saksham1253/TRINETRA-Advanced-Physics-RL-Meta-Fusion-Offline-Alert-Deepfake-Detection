"""GLOF physics check on REAL events: ICIMOD HMAGLOFDB (v4, 13-12-2025; via github.com/prazg/GLOF_dashboard data/raw,
redistributed unmodified; DOI 10.26066/RDS.1973283). CPU, seconds.

Fits empirical power laws with bootstrap CIs (Class B: fitted on our data):
  V = a * A^b        lake volume [m3] vs lake area [m2]
  Qp = c * V^d       peak water discharge [m3/s] vs released volume [m3]
Repo research formulas GH-13 Froehlich (needs breach height h_b) and Costa-Schuster (needs potential energy) CANNOT be
tested: HMAGLOFDB has no breach height / dam height column. Reported as "not testable with this data".
Literature coefficients for comparison are FROM MEMORY in the repo ([coeff-verify]) and are NOT used as truth here.
Run: python kaggle/glof_physics_check.py --csv HMAGLOFDB_v4_0_13122025.csv --out out/glof
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np


def fit_power(x, y, n_boot=2000, seed=0):
    lx, ly = np.log10(x), np.log10(y)
    b, la = np.polyfit(lx, ly, 1)
    pred = la + b * lx
    r2 = 1 - ((ly - pred) ** 2).sum() / ((ly - ly.mean()) ** 2).sum()
    rng = np.random.default_rng(seed); bs = []
    for _ in range(n_boot):
        i = rng.integers(0, len(x), len(x))
        if len(set(lx[i])) > 2:
            bs.append(np.polyfit(lx[i], ly[i], 1))
    bs = np.asarray(bs)
    return {"n": int(len(x)), "coef": float(10 ** la), "exponent": float(b), "r2_log": float(r2),
            "exponent_ci95": [float(np.percentile(bs[:, 0], 2.5)), float(np.percentile(bs[:, 0], 97.5))],
            "log10_rmse": float(np.sqrt(((ly - pred) ** 2).mean())),
            "x_range": [float(x.min()), float(x.max())]}


def main(argv=None):
    import pandas as pd
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True); ap.add_argument("--out", default="out/glof")
    ap.add_argument("--dedupe-lakes", action="store_true", help="keep one record per lake (repeat events inflate n)")
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    h = pd.read_csv(a.csv, encoding="cp1252")
    num = lambda c: pd.to_numeric(h[c].astype(str).str.replace(",", "").str.strip(), errors="coerce")  # noqa: E731
    h = h.assign(A=num("Area"), V=num("Volume"), Q=num("Discharge_water"))
    if a.dedupe_lakes:
        h = h.drop_duplicates(subset=["Lake_name", "Lat_lake", "Lon_lake"])
    rep = {"name": "glof_physics", "source": os.path.basename(a.csv), "records": int(len(h)),
           "repeat_flag_Y": int((h["Repeat"] == "Y").sum()) if "Repeat" in h else None}
    av = h[(h.A > 0) & (h.V > 0)]
    vq = h[(h.V > 0) & (h.Q > 0)]
    rep["area_volume"] = fit_power(av.A.values, av.V.values) if len(av) >= 5 else {"n": int(len(av)), "note": "too few"}
    rep["volume_peakQ"] = fit_power(vq.V.values, vq.Q.values) if len(vq) >= 5 else {"n": int(len(vq)), "note": "too few"}
    rep["not_testable"] = {"GH-13 Froehlich Qp=c V^p h_b^q": "no breach-height column",
                           "Costa-Schuster Qp=0.763 PE^0.42": "no dam height -> no potential energy"}
    rep["note"] = "Class B empirical fits on HMAGLOFDB; small n; heterogeneous sources (moraine/ice/landslide dams mixed)."
    json.dump(rep, open(os.path.join(a.out, "glof_physics_report.json"), "w"), indent=2)
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()
