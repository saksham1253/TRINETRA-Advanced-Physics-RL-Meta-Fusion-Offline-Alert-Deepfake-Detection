"""data_adapters/build_geo.py — REAL landslide events (NASA Global Landslide Catalog) + REAL rainfall (NASA POWER,
IMERG-derived precipitation product PRECTOTCORR, no login) + REAL slope (Copernicus DEM GLO-30 on AWS, no login),
converted into (1) a feature table for the physics hindcast and (2) the Geo-PINN .npz contract
(`deep/datamodules.GeoSeriesDataset`: Z, t, rain, static[6] = c', phi', gamma, z, beta, susceptibility; label, lat, lon).

Design (documented in docs/09e): CASE-CONTROL. Positives = catalog events (rain-triggered, location accuracy <= --max-acc km).
Controls = the SAME places on random monsoon days (Jun-Sep) of other years with no catalog event within 50 km and +-15 days.
The positive fraction is therefore ARTIFICIAL (~1/(1+k)); report ROC-AUC / recall@FPR, and value score only with this caveat.

Soil parameters are NOT observed. c'=5 kPa, phi'=32 deg, gamma=19 kN/m3, z=2 m, K_z=1e-5 m/s, D0=5e-5 m2/s, psi0=0 m are
ASSUMPTIONS, typical colluvium values. ABSOLUTE FS is therefore uncalibrated (on 44 deg Himalayan slopes FS_dry < 1 with c'=5 kPa);
the physics signal used is dFS = FS_dry - FS_wet (rain-driven change at the SAME site), which cancels the site-level bias. Only slope (DEM) and rain (POWER) vary per sample.

Run (Kaggle, internet ON; CPU is enough):
  python data_adapters/build_geo.py --glc Global_Landslide_Catalog_Export_rows.csv --country India \
      --bbox 28 33 76 81 --dem-dir /kaggle/working/dem --cache /kaggle/working/power_cache --out /kaggle/working/geo
Sources (verified 2026-10-31): GLC CSV via catalog.data.gov -> data.nasa.gov/docs/legacy/...; POWER daily point API;
Copernicus DEM tile URL pattern below (N30 E079 tile = 41.7 MB, HTTP 200).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "trinetra" / "src"))
from trinetra.ws1b_geophys.caine import caine_exceedance          # noqa: E402
from trinetra.ws1b_geophys.fs import factor_of_safety, pore_pressure_from_head  # noqa: E402
from trinetra.ws1b_geophys.iverson import transient_head_multipulse  # noqa: E402

POWER = ("https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=AG"
         "&longitude={lon}&latitude={lat}&start={s}&end={e}&format=JSON")
DEM = ("https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_{ns}{lat:02d}_00_{ew}{lon:03d}_00_DEM/"
       "Copernicus_DSM_COG_10_{ns}{lat:02d}_00_{ew}{lon:03d}_00_DEM.tif")
SOIL = dict(c_prime=5.0, phi=32.0, gamma=19.0, z=2.0, K_z=1e-5, D0=5e-5, psi0=0.0)    # ASSUMPTIONS (psi0=0: monsoon water table near slip plane)


# ------------------------------------------------------------------------------------------- rainfall
def power_series(lat, lon, start, end, cache: Path) -> dict:
    """Daily precipitation (mm/day) for the POWER cell containing (lat, lon). Cached per 0.5 deg cell."""
    la, lo = round(lat * 2) / 2, round(lon * 2) / 2
    f = cache / f"power_{la:.1f}_{lo:.1f}_{start}_{end}.json"
    if f.exists():
        return json.loads(f.read_text())
    cache.mkdir(parents=True, exist_ok=True)
    for attempt in range(3):
        try:
            d = json.load(urllib.request.urlopen(POWER.format(lat=la, lon=lo, s=start, e=end), timeout=90))
            ser = {k: (None if v is None or v < 0 else float(v)) for k, v in d["properties"]["parameter"]["PRECTOTCORR"].items()}
            f.write_text(json.dumps(ser))
            time.sleep(0.3)
            return ser
        except Exception as e:  # retry up to 3x (rule 9), then skip
            print(f"[power] retry {attempt + 1} {la},{lo}: {e}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    return {}


def rain_window(ser: dict, day: np.datetime64, n: int = 30) -> np.ndarray:
    days = [str(day - np.timedelta64(i, "D")).replace("-", "") for i in range(n - 1, -1, -1)]
    return np.array([ser.get(d) if ser.get(d) is not None else np.nan for d in days], float)


# ------------------------------------------------------------------------------------------------ DEM
def dem_tile(lat, lon, dem_dir: Path, download=True):
    la, lo = math.floor(lat), math.floor(lon)
    ns, ew = ("N" if la >= 0 else "S"), ("E" if lo >= 0 else "W")
    f = dem_dir / f"dem_{ns}{abs(la):02d}_{ew}{abs(lo):03d}.tif"
    if not f.exists():
        if not download:
            return None, None
        dem_dir.mkdir(parents=True, exist_ok=True)
        url = DEM.format(ns=ns, lat=abs(la), ew=ew, lon=abs(lo))
        try:
            urllib.request.urlretrieve(url, f)
        except Exception as e:
            print(f"[dem] no tile {url}: {e}", file=sys.stderr)
            return None, None
    import tifffile  # pip install tifffile imagecodecs (COG, deflate)
    return tifffile.imread(f).astype(np.float32), (la, lo)


_DEM_CACHE: dict = {}


def slope_at(lat, lon, dem_dir: Path, radius_m: float = 1000.0, download=True):
    """(p90 slope deg, mean elevation m) within radius around the point (location accuracy is >= 1 km)."""
    key = (math.floor(lat), math.floor(lon))
    if key not in _DEM_CACHE:
        _DEM_CACHE[key] = dem_tile(lat, lon, dem_dir, download)
    a, origin = _DEM_CACHE[key]
    if a is None:
        return np.nan, np.nan
    n = a.shape[0]
    r = int((origin[0] + 1 - lat) * n); c = int((lon - origin[1]) * a.shape[1])
    dy = 111320.0 / n; dx = dy * math.cos(math.radians(lat)) * n / a.shape[1]
    w = max(2, int(radius_m / dy))
    win = a[max(0, r - w): r + w + 1, max(0, c - w): c + w + 1]
    if win.size < 9:
        return np.nan, np.nan
    gy, gx = np.gradient(win, dy, dx)
    s = np.degrees(np.arctan(np.hypot(gx, gy)))
    return float(np.percentile(s, 90)), float(win.mean())


# ------------------------------------------------------------------------------------------- physics
FS_DRY_TARGET = 1.2   # back-analysis assumption: the slope stands in the dry season with FS = 1.2


def backcalc_cohesion(beta_deg: float, soil=SOIL, fs_target: float = FS_DRY_TARGET) -> float:
    """Back-analysed c' [kPa] such that the DRY infinite-slope FS equals fs_target (standard geotechnical practice
    when soil strength is unknown: the slope is observed to be stable). Clipped at 0."""
    b, ph = math.radians(beta_deg), math.radians(soil["phi"])
    gz = soil["gamma"] * soil["z"]
    return max(0.0, fs_target * gz * math.sin(b) * math.cos(b) - gz * math.cos(b) ** 2 * math.tan(ph))


def physics_features(rain_mm: np.ndarray, beta_deg: float, soil=SOIL) -> dict:
    """Caine ratio (repo constants a=14, b=0.39), antecedent sums, and Iverson multipulse -> FS at day end."""
    r = np.nan_to_num(rain_mm, nan=0.0)
    out = {f"rain_{k}d": float(r[-k:].sum()) for k in (1, 3, 7, 15, 30)}
    out["rain_max3"] = float(r[-3:].max())
    wet = 0
    for v in r[::-1]:
        if v >= 1.0:
            wet += 1
        else:
            break
    if wet == 0 and r[-2] >= 1.0:  # event reported the day after the storm
        wet = 1
    D_h = max(wet, 1) * 24.0
    I = r[-max(wet, 1):].sum() / D_h
    out["caine_D_h"] = D_h; out["caine_I_mmh"] = float(I)
    out["caine_ratio"] = float(caine_exceedance(max(I, 1e-6), D_h, 14.0, 0.39)[1])
    if np.isfinite(beta_deg) and beta_deg > 1:
        t = np.arange(len(r)) * 86400.0
        Iz = np.minimum(r / 1000.0 / 86400.0, soil["K_z"])            # flux capped at K_z (Iverson validity)
        psi = soil["psi0"] + float(transient_head_multipulse(soil["z"], len(r) * 86400.0, t, Iz, soil["D0"], soil["K_z"], beta_deg))
        psi = min(psi, soil["z"] * math.cos(math.radians(beta_deg)) ** 2)  # cannot exceed hydrostatic saturation
        fs = float(factor_of_safety(soil["c_prime"], soil["phi"], soil["gamma"], soil["z"], beta_deg,
                                    u_w=float(pore_pressure_from_head(max(psi, 0.0)))))
        fs_dry = float(factor_of_safety(soil["c_prime"], soil["phi"], soil["gamma"], soil["z"], beta_deg, u_w=0.0))
        c_bc = backcalc_cohesion(beta_deg, soil)
        fs_bc = float(factor_of_safety(c_bc, soil["phi"], soil["gamma"], soil["z"], beta_deg,
                                       u_w=float(pore_pressure_from_head(max(psi, 0.0)))))
    else:
        psi, fs, fs_dry, c_bc, fs_bc = np.nan, np.nan, np.nan, np.nan, np.nan
    out.update(psi_m=float(psi), fs=fs, fs_dry=fs_dry, dfs=(fs_dry - fs) if np.isfinite(fs) else np.nan,
               c_backcalc_kpa=c_bc, fs_backcalc=fs_bc)
    return out


# ------------------------------------------------------------------------------------------- main
def main(argv=None):
    import pandas as pd
    ap = argparse.ArgumentParser()
    ap.add_argument("--glc", required=True); ap.add_argument("--country", default="India")
    ap.add_argument("--bbox", type=float, nargs=4, default=None, help="lat_min lat_max lon_min lon_max")
    ap.add_argument("--max-acc", type=float, default=10.0, help="keep events with location accuracy <= km")
    ap.add_argument("--controls", type=int, default=3); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--max-events", type=int, default=400)
    ap.add_argument("--dem-dir", default="dem"); ap.add_argument("--no-dem-download", action="store_true")
    ap.add_argument("--cache", default="power_cache"); ap.add_argument("--out", default="geo")
    a = ap.parse_args(argv)
    rng = np.random.default_rng(a.seed); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    g = pd.read_csv(a.glc)
    need = {"country_name", "landslide_trigger", "location_accuracy", "event_date", "latitude", "longitude"}
    if not need <= set(g.columns):
        raise SystemExit(f"{a.glc} is not the NASA GLC export (missing {sorted(need - set(g.columns))}); re-download or use the Kaggle mirror")
    g = g[g["country_name"].astype(str).str.contains(a.country, na=False)]
    g = g[g["landslide_trigger"].astype(str).str.contains("rain|downpour|monsoon|tropical|flood", case=False, na=False)]
    acc = g["location_accuracy"].astype(str).str.extract(r"(\d+)km")[0].astype(float)
    g = g[acc <= a.max_acc]
    if a.bbox:
        g = g[g.latitude.between(a.bbox[0], a.bbox[1]) & g.longitude.between(a.bbox[2], a.bbox[3])]
    g = g.assign(day=pd.to_datetime(g["event_date"], errors="coerce").dt.normalize()).dropna(subset=["day"])
    g = g.sort_values("day").head(a.max_events)
    print(f"[glc] {len(g)} events after filters (country={a.country}, acc<={a.max_acc} km, bbox={a.bbox})")
    ev_days = g["day"].values.astype("datetime64[D]"); ev_lat = g.latitude.values; ev_lon = g.longitude.values
    years = np.arange(2007, 2017)
    rows = []
    for i, r in enumerate(g.itertuples()):
        ser = power_series(r.latitude, r.longitude, "20061201", "20161231", Path(a.cache))
        if not ser:
            continue
        beta, elev = slope_at(r.latitude, r.longitude, Path(a.dem_dir), download=not a.no_dem_download)
        cand = [(np.datetime64(r.day, "D"), 1)]
        tries = 0
        while len(cand) < 1 + a.controls and tries < 50:
            tries += 1
            y = int(rng.choice(years)); d = np.datetime64(f"{y}-06-01") + np.timedelta64(int(rng.integers(0, 122)), "D")
            near = (np.abs(ev_lat - r.latitude) < 0.45) & (np.abs(ev_lon - r.longitude) < 0.45)
            if np.any(near & (np.abs((ev_days - d).astype(int)) <= 15)):
                continue
            cand.append((d, 0))
        for d, lab in cand:
            rw = rain_window(ser, d)
            if np.isnan(rw).mean() > 0.2:
                continue
            f = physics_features(rw, beta)
            rows.append(dict(event_id=r.event_id, lat=r.latitude, lon=r.longitude, day=str(d), label=lab,
                             slope_p90_deg=beta, elev_m=elev, **f))
        if (i + 1) % 25 == 0:
            print(f"[geo] {i + 1}/{len(g)} events processed, rows={len(rows)}")
    df = pd.DataFrame(rows)
    df.to_csv(out / "geo_events.csv", index=False)
    ok = df.dropna(subset=["fs"])
    if len(ok):
        s = SOIL
        # BUGFIX (B-27): constant c'=5 kPa makes FS<1 everywhere on Himalayan slopes, so the PINN's physics hinge
        # ("FS<1 -> high risk") pushed every sample to the same probability (collapse). Use the back-analysed c'.
        static = np.stack([ok.c_backcalc_kpa.values, np.full(len(ok), s["phi"]), np.full(len(ok), s["gamma"]),
                           np.full(len(ok), s["z"]), ok.slope_p90_deg.values, np.clip(ok.slope_p90_deg.values / 45.0, 0, 1)], 1)
        # BUGFIX (B-28): raw SI inputs (t ~ 1e5 s next to rain ~ 1e-7 m/s) are erased by the first LayerNorm, so the PINN
        # saw no rain signal and collapsed. Inputs are now O(1): t in DAYS, rain in mm/h, Z in m. The PDE psi_t = D1 psi_ZZ
        # stays exact if D0 is passed in the same units: D0' = D0 * 86400 s / (1 m)^2  (5e-5 m2/s -> 4.32 m2/day).
        np.savez_compressed(out / "geo.npz", Z=np.full(len(ok), s["z"], np.float32), t=(ok.caine_D_h.values / 24.0).astype(np.float32),
                            rain=ok.caine_I_mmh.values.astype(np.float32), static=static.astype(np.float32),
                            label=ok.label.values.astype(np.float32), lat=ok.lat.values, lon=ok.lon.values)
    meta = {"pinn_units": {"t": "days", "rain": "mm/h", "Z": "m", "D0_arg_for_train_geo_pinn": SOIL["D0"] * 86400.0,
                           "beta_deg_arg": float(np.nanmedian(df.slope_p90_deg)) if len(df) else None},
            "n_rows": int(len(df)), "n_pos": int(df.label.sum()) if len(df) else 0, "n_with_dem": int(len(ok)),
            "soil_assumptions": SOIL, "design": "case-control, controls=%d" % a.controls, "bbox": a.bbox, "country": a.country}
    (out / "geo_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"[geo] rows={len(df)} positives={meta['n_pos']} with_DEM={len(ok)} -> {out}")


if __name__ == "__main__":
    main()
