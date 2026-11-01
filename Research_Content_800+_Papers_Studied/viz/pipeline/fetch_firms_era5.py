#!/usr/bin/env python
"""viz/pipeline/fetch_firms_era5.py — REAL fire + wind extracts for L5 (FIRMS) and L4 (ERA5-Land).

HONESTY / FEASIBILITY NOTE
--------------------------
These two layers require a FREE key/account and live network access that the build sandbox does NOT have
(NASA FIRMS MAP_KEY; Copernicus CDS account). This script is the REPRODUCIBLE local path. Until it is run
with a real key, the app shows L4/L5 as DATA-PENDING and renders NOTHING for them — it never fabricates
hotspots or wind. Run locally:

    # 1) FIRMS active-fire archive for the AOI + 2021 window (get a free MAP_KEY at
    #    https://firms.modaps.eosdis.nasa.gov/api/map_key/):
    python viz/pipeline/fetch_firms_era5.py firms --map-key YOUR_KEY \
        --bbox 78.5,29.5,80.2,30.8 --start 2021-04-25 --end 2021-05-12

    # 2) ERA5-Land hourly wind for the AOI (needs ~/.cdsapirc + `pip install cdsapi`):
    python viz/pipeline/fetch_firms_era5.py era5 --bbox 78.5,29.5,80.2,30.8 --date 2021-05-01

Outputs (schemas the Cesium app's layers.js consumes):
    viz/render/public/data/l5_firms.json      {provenance, hotspots:[{lon,lat,frp,acq_date,confidence,sat}]}
    viz/render/public/data/l4_era5_wind.json  {provenance, grid:[{lon,lat,u,v,speed}], date, units}
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.abspath(os.path.join(HERE, "..", ".."))
PUB = os.path.join(WORKSPACE, "viz", "render", "public", "data")


def _bbox(s):
    return [float(x) for x in s.split(",")]


def fetch_firms(map_key, bbox, start, end, sat="VIIRS_SNPP_NRT"):
    """FIRMS area CSV API. Note: historical dates may require an archive source (SP vs NRT); verify in-browser.
    Endpoint: https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/{SOURCE}/{W,S,E,N}/{day_range}/{date}
    """
    w, s, e, n = bbox
    # day-range API max 10 days per call; the caller should loop. Minimal single-call demo here.
    url = (f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{map_key}/{sat}/"
           f"{w},{s},{e},{n}/10/{start}")
    print("GET", url)
    with urllib.request.urlopen(url, timeout=60) as r:
        text = r.read().decode("utf-8", "replace")
    rows = list(csv.DictReader(io.StringIO(text)))
    hotspots = []
    for row in rows:
        try:
            hotspots.append({
                "lon": float(row.get("longitude")), "lat": float(row.get("latitude")),
                "frp": float(row.get("frp", 0) or 0), "acq_date": row.get("acq_date"),
                "confidence": row.get("confidence"), "sat": row.get("satellite") or sat,
            })
        except (TypeError, ValueError):
            continue
    doc = {
        "provenance": {"layer": "L5 — real fire observations", "kind": "REAL",
                       "source": "NASA FIRMS", "product": sat, "aoi_bbox": bbox,
                       "window": f"{start}..{end}", "fetched_utc": datetime.now(timezone.utc).isoformat(),
                       "endpoint": url.replace(map_key, "<MAP_KEY>"),
                       "license": "NASA FIRMS / LANCE — credit requested"},
        "count": len(hotspots), "hotspots": hotspots,
    }
    _write("l5_firms.json", doc)
    print(f"wrote l5_firms.json with {len(hotspots)} hotspots")


def fetch_era5(bbox, date):
    """ERA5-Land hourly 10 m u/v wind for the AOI via cdsapi (needs account). Downsampled to a point grid."""
    try:
        import cdsapi  # noqa
    except ImportError:
        sys.exit("cdsapi not installed. `pip install cdsapi` and configure ~/.cdsapirc, then re-run.")
    import cdsapi
    w, s, e, n = bbox
    c = cdsapi.Client()
    target = os.path.join(PUB, "_era5_tmp.nc")
    c.retrieve("reanalysis-era5-land", {
        "variable": ["10m_u_component_of_wind", "10m_v_component_of_wind"],
        "year": date[:4], "month": date[5:7], "day": date[8:10], "time": "12:00",
        "area": [n, w, s, e], "format": "netcdf",
    }, target)
    # NetCDF parsing needs xarray/netCDF4 (not in build sandbox) — do it locally:
    import xarray as xr  # local only
    ds = xr.open_dataset(target)
    u = ds["u10"].isel(time=0); v = ds["v10"].isel(time=0)
    grid = []
    lons = u["longitude"].values; lats = u["latitude"].values
    step = max(1, len(lons) // 20)
    for iy in range(0, len(lats), step):
        for ix in range(0, len(lons), step):
            uu = float(u.values[iy, ix]); vv = float(v.values[iy, ix])
            grid.append({"lon": float(lons[ix]), "lat": float(lats[iy]),
                         "u": round(uu, 3), "v": round(vv, 3), "speed": round((uu*uu+vv*vv) ** 0.5, 3)})
    doc = {
        "provenance": {"layer": "L4 — atmosphere (wind)", "kind": "REAL", "source": "ERA5-Land (C3S)",
                       "product": "reanalysis-era5-land", "aoi_bbox": bbox, "date": date,
                       "fetched_utc": datetime.now(timezone.utc).isoformat(),
                       "license": "CC-BY (DOI 10.24381/cds.e2161bac) — Generated using Copernicus Climate "
                                  "Change Service information"},
        "date": date, "units": {"u": "m/s", "v": "m/s", "speed": "m/s"}, "grid": grid,
    }
    _write("l4_era5_wind.json", doc)
    os.remove(target)
    print(f"wrote l4_era5_wind.json with {len(grid)} grid points")


def _write(name, doc):
    os.makedirs(PUB, exist_ok=True)
    with open(os.path.join(PUB, name), "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("firms"); f.add_argument("--map-key", required=True)
    f.add_argument("--bbox", type=_bbox, required=True); f.add_argument("--start", required=True)
    f.add_argument("--end", required=True); f.add_argument("--sat", default="VIIRS_SNPP_NRT")
    e = sub.add_parser("era5"); e.add_argument("--bbox", type=_bbox, required=True)
    e.add_argument("--date", required=True)
    a = ap.parse_args()
    if a.cmd == "firms":
        fetch_firms(a.map_key, a.bbox, a.start, a.end, a.sat)
    else:
        fetch_era5(a.bbox, a.date)


if __name__ == "__main__":
    main()
