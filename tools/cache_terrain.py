"""Pre-cache Terrarium-encoded elevation tiles (AWS Open Data 'Terrain Tiles') for the offline demo.

Tiles: https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png  (AWS Registry of Open Data; sources and
attribution: https://github.com/tilezen/joerd/blob/master/docs/attribution.md). Writes public/tiles/terrarium/{z}/{x}/{y}.png and
manifest.json (list of cached z/x/y). The console serves cached tiles first and builds deeper zoom levels from the nearest
cached parent when a tile is missing (see src/console/map/terrainProtocol.ts).
Run: python3 tools/cache_terrain.py [--dry-run]
"""
import argparse, json, math, os, concurrent.futures as cf, urllib.request

URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"


def tile_range(bbox, z):
    w, s, e, n = bbox
    def tx(lon): return int((lon + 180) / 360 * 2 ** z)
    def ty(lat):
        r = math.radians(lat); return int((1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 2 ** z)
    return [(z, x, y) for x in range(tx(w), tx(e) + 1) for y in range(ty(n), ty(s) + 1)]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--out", default="public/tiles/terrarium")
    a = ap.parse_args()
    R = json.load(open("src/console/data/regions.json"))
    want = set()
    nat = R["national"]
    for z in range(nat["zmin"], nat["zmax"] + 1):
        want.update(tile_range(nat["bbox"], z))
    for r in R["regions"]:
        for z in range(nat["zmax"] + 1, r["zmax"] + 1):
            want.update(tile_range(r["bbox"], z))
    print("tiles wanted:", len(want))
    if a.dry_run:
        return

    def get(t):
        z, x, y = t; p = f"{a.out}/{z}/{x}/{y}.png"
        if os.path.exists(p) and os.path.getsize(p) > 0:
            return t, True
        os.makedirs(os.path.dirname(p), exist_ok=True)
        try:
            urllib.request.urlretrieve(URL.format(z=z, x=x, y=y), p); return t, True
        except Exception as ex:  # noqa: BLE001
            print("fail", t, ex); return t, False
    ok = []
    with cf.ThreadPoolExecutor(16) as ex:
        for t, good in ex.map(get, sorted(want)):
            if good:
                ok.append(f"{t[0]}/{t[1]}/{t[2]}")
    json.dump({"source": URL, "encoding": "terrarium", "tiles": sorted(ok)}, open(f"{a.out}/manifest.json", "w"))
    size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(a.out) for f in fs)
    print("cached", len(ok), "tiles,", round(size / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
