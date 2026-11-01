// dl_tiles.cjs — download real elevation (terrarium) + satellite imagery (Esri World Imagery) XYZ tiles
// covering the AOI bbox, save to assets/tiles/{terr,sat}. Stitching/decoding happens in Python (Pillow).
const fs = require("fs");
const path = require("path");

const Z = 11;
// AOI bbox lon/lat
const LON0 = 78.5, LAT0 = 29.5, LON1 = 80.2, LAT1 = 30.8;
const n = Math.pow(2, Z);
const lon2x = lon => Math.floor((lon + 180) / 360 * n);
const lat2y = lat => { const r = lat * Math.PI / 180; return Math.floor((1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2 * n); };
// tile -> geographic edges
const x2lon = x => x / n * 360 - 180;
const y2lat = y => { const t = Math.PI * (1 - 2 * y / n); return 180 / Math.PI * Math.atan(0.5 * (Math.exp(t) - Math.exp(-t))); };

const xmin = lon2x(LON0), xmax = lon2x(LON1);
const ymin = lat2y(LAT1), ymax = lat2y(LAT0); // lat1>lat0 => smaller y
const base = path.join(__dirname, "assets", "tiles");
fs.mkdirSync(path.join(base, "terr"), { recursive: true });
fs.mkdirSync(path.join(base, "sat"), { recursive: true });

const jobs = [];
for (let x = xmin; x <= xmax; x++)
  for (let y = ymin; y <= ymax; y++) {
    jobs.push({ kind: "terr", x, y, url: `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/${Z}/${x}/${y}.png` });
    jobs.push({ kind: "sat", x, y, url: `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/${Z}/${y}/${x}` });
  }

async function worker(list, id) {
  for (const j of list) {
    const dst = path.join(base, j.kind, `${j.x}_${j.y}.png`);
    if (fs.existsSync(dst) && fs.statSync(dst).size > 500) continue;
    try {
      const r = await fetch(j.url, { headers: { "User-Agent": "Mozilla/5.0 trinetra-viz" } });
      if (!r.ok) { console.log("FAIL", r.status, j.url); continue; }
      fs.writeFileSync(dst, Buffer.from(await r.arrayBuffer()));
    } catch (e) { console.log("ERR", j.kind, j.x, j.y, e.message); }
  }
}

(async () => {
  console.log(`Z=${Z} x:[${xmin}..${xmax}] y:[${ymin}..${ymax}]  tiles=${jobs.length} (${jobs.length/2} each)`);
  const POOL = 8;
  const chunks = Array.from({ length: POOL }, (_, i) => jobs.filter((_, k) => k % POOL === i));
  const t0 = Date.now();
  await Promise.all(chunks.map((c, i) => worker(c, i)));
  // extent of the stitched mosaic (full tile grid)
  const meta = {
    z: Z, xmin, xmax, ymin, ymax, tile: 256,
    width: (xmax - xmin + 1) * 256, height: (ymax - ymin + 1) * 256,
    west: x2lon(xmin), east: x2lon(xmax + 1), north: y2lat(ymin), south: y2lat(ymax + 1),
    aoi: { west: LON0, east: LON1, south: LAT0, north: LAT1 }
  };
  fs.writeFileSync(path.join(__dirname, "assets", "tiles", "meta.json"), JSON.stringify(meta, null, 2));
  const terr = fs.readdirSync(path.join(base, "terr")).length, sat = fs.readdirSync(path.join(base, "sat")).length;
  console.log(`done in ${((Date.now()-t0)/1000).toFixed(0)}s  terr=${terr} sat=${sat}`);
  console.log("extent", JSON.stringify(meta));
})();
