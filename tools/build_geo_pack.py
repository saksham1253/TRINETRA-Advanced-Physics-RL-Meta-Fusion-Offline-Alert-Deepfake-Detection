"""Build the offline vector pack for the TRINETRA console (public/geo/*.json).

Sources (downloaded once, then everything is local; see FRONTEND/FE_DATA_SOURCES.md):
  india_soi.json  : datameet/maps Country/india-soi.geojson  (Survey of India depiction; CC BY-SA 2.5 / ODbL, DataMeet)
  states.json     : datameet/maps States/Admin2.shp          (state boundaries, Survey of India based; CC BY 4.0, DataMeet)
  rivers.json     : Natural Earth 10m rivers + lake centerlines (public domain), clipped to the SOI polygon
Run: python3 tools/build_geo_pack.py --src /tmp/geo --out public/geo
"""
import argparse, json, os
import shapefile
from shapely.geometry import shape, mapping
from shapely.ops import unary_union


def rnd(geom, nd=3):
    def r(c):
        if isinstance(c, (list, tuple)) and c and isinstance(c[0], (int, float)):
            return [round(c[0], nd), round(c[1], nd)]
        return [r(x) for x in c]
    g = mapping(geom); return {"type": g["type"], "coordinates": r(g["coordinates"])}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--src", default="/tmp/geo"); ap.add_argument("--out", default="public/geo")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    soi = shape(json.load(open(f"{a.src}/Country_india-soi.geojson"))["features"][0]["geometry"])
    india = soi.simplify(0.01, preserve_topology=True)
    fc = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {
        "name": "India", "source": "Survey of India State Map via DataMeet (india-soi.geojson)", "license": "CC BY-SA 2.5 / ODbL"},
        "geometry": rnd(india)}]}
    json.dump(fc, open(f"{a.out}/india_soi.json", "w"), separators=(",", ":"))
    # mask: a frame around India minus the (simplified) SOI polygon; dims neighbours and hides the edge of the cached
    # terrain rectangle. Uses the simplified polygon: the full-resolution difference runs out of memory in small sandboxes.
    from shapely.geometry import box
    mask = box(55, -5, 110, 45).difference(india.buffer(0)).simplify(0.02, preserve_topology=True)
    json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {}, "geometry": rnd(mask)}]},
              open(f"{a.out}/india_mask.json", "w"), separators=(",", ":"))
    r = shapefile.Reader(f"{a.src}/States_Admin2"); feats = []
    for sr in r.shapeRecords():
        g = shape(sr.shape.__geo_interface__).simplify(0.015, preserve_topology=True)
        g = g if g.is_valid else g.buffer(0)
        c = g.representative_point()
        feats.append({"type": "Feature", "properties": {"name": sr.record[0], "lon": round(c.x, 3), "lat": round(c.y, 3)}, "geometry": rnd(g)})
    json.dump({"type": "FeatureCollection", "features": feats}, open(f"{a.out}/states.json", "w"), separators=(",", ":"))
    from shapely.prepared import prep
    riv = json.load(open(f"{a.src}/rivers.geojson")); clip = india.buffer(0.05); pc = prep(clip); out = []
    for f in riv["features"]:
        p = f["properties"]
        if (p.get("scalerank") or 99) > 7 or p.get("featurecla", "").startswith("Lake"):
            continue
        g0 = shape(f["geometry"])
        if not pc.intersects(g0):
            continue
        g = g0 if pc.contains(g0) else g0.intersection(clip)
        if g.is_empty:
            continue
        out.append({"type": "Feature", "properties": {"name": p.get("name") or "", "rank": p.get("scalerank")},
                    "geometry": rnd(g.simplify(0.01))})
    json.dump({"type": "FeatureCollection", "features": out}, open(f"{a.out}/rivers.json", "w"), separators=(",", ":"))
    for f in ("india_soi", "states", "rivers"):
        print(f, round(os.path.getsize(f"{a.out}/{f}.json") / 1e3), "KB")




def gazetteer(src="/tmp/geo", out="public/geo"):  # noqa: D401
    """Local gazetteer (GeoNames cities15000, CC BY 4.0): Indian places with population >= 15,000 + state names."""
    adm = {}
    for line in open(f"{src}/admin1.txt", encoding="utf-8"):
        k, name, *_ = line.rstrip("\n").split("\t")
        adm[k] = name
    rows = []
    for line in open(f"{src}/cities15000.txt", encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if f[8] != "IN":
            continue
        rows.append([f[1], round(float(f[4]), 4), round(float(f[5]), 4), adm.get(f"IN.{f[10]}", ""), int(f[14] or 0)])
    rows.sort(key=lambda r: -r[4])
    json.dump({"source": "GeoNames cities15000 (CC BY 4.0), country IN", "columns": ["name", "lat", "lon", "state", "population"],
               "rows": rows}, open(f"{out}/gazetteer.json", "w"), separators=(",", ":"), ensure_ascii=False)
    land = json.load(open(f"{src}/land.geojson"))
    json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {}, "geometry": rnd(shape(f["geometry"]), 2)}
               for f in land["features"]]}, open(f"{out}/land.json", "w"), separators=(",", ":"))
    print("gazetteer", len(rows), "places;", round(os.path.getsize(f"{out}/gazetteer.json") / 1e3), "KB; land",
          round(os.path.getsize(f"{out}/land.json") / 1e3), "KB")


if __name__ == "__main__":
    main()
    gazetteer()
