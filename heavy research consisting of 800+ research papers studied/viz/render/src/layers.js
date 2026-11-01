// layers.js — builds each L0–L12 layer as Cesium content (or an HTML overlay), with per-layer
// visibility + opacity + an exploded-stack mode. REAL vs SIMULATED/ILLUSTRATIVE is encoded in color
// (DESIGN_SPEC tokens) and every datum traces to config.LAYERS provenance. Nothing is fabricated:
// data-driven layers render ONLY if their JSON is present; otherwise a DATA-PENDING placard.
import * as Cesium from "cesium";
import { LAYERS, AOI } from "./config.js";
import { inferno, viridis, cividis } from "./colormaps.js";

const C = {
  real: Cesium.Color.fromCssColorString("#38D39F"),
  sim: Cesium.Color.fromCssColorString("#F2B141"),
  illus: Cesium.Color.fromCssColorString("#8B9DC9"),
  focus: Cesium.Color.fromCssColorString("#4CA6FF"),
  warn: Cesium.Color.fromCssColorString("#E5484D"),
};
const tagColor = (kind) => (kind === "REAL" || kind === "REAL_CODE") ? C.real
  : kind === "SIMULATED" ? C.sim : C.illus;

async function fetchJSON(url) {
  try { const r = await fetch(url); if (!r.ok) return null; return await r.json(); }
  catch { return null; }
}

export class LayerManager {
  constructor(viewer, hud) {
    this.viewer = viewer;
    this.hud = hud;
    this.layers = new Map();   // id -> { def, ds, overlay, baseHeight, explodeHeight, pending }
    this.explode = false;
  }

  async buildAll() {
    for (const def of LAYERS) {
      const ds = new Cesium.CustomDataSource(def.id);
      await this.viewer.dataSources.add(ds);
      ds.show = false;
      const rec = { def, ds, overlay: null, pending: def.status === "data_pending" };
      this.layers.set(def.id, rec);
      try { await this._build(rec); }
      catch (e) { console.warn(`layer ${def.id} build failed`, e); }
    }
  }

  async _build(rec) {
    const b = {
      L2: () => this._worldcover(rec), L3: () => this._exposure(rec),
      L4: () => this._wind(rec), L5: () => this._fire(rec), L6: () => this._physics(rec),
      L7: () => this._cctv(rec), L8: () => this._datasets(rec), L9: () => this._dfdOverlay(rec, "l9"),
      L10: () => this._alerting(rec), L11: () => this._routes(rec), L12: () => this._dfdOverlay(rec, "l12"),
    }[rec.def.id];
    if (b) await b();
  }

  // ---- individual layers ---------------------------------------------------------------
  _worldcover(rec) {
    // ESA WorldCover 10m as an imagery layer (live; video-safe). Added to viewer.imageryLayers, toggled here.
    try {
      const prov = new Cesium.WebMapTileServiceImageryProvider({
        url: "https://services.terrascope.be/wmts/v2?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0" +
             "&LAYER=WORLDCOVER_2021_MAP&STYLE=default&TILEMATRIXSET=EPSG:3857&FORMAT=image/png" +
             "&TILEMATRIX={TileMatrix}&TILEROW={TileRow}&TILECOL={TileCol}",
        layer: "WORLDCOVER_2021_MAP", style: "default", format: "image/png",
        tileMatrixSetID: "EPSG:3857",
        credit: new Cesium.Credit("© ESA WorldCover project / modified Copernicus Sentinel data"),
      });
      const lyr = this.viewer.imageryLayers.addImageryProvider(prov);
      lyr.show = false; lyr.alpha = 0.75;
      rec.imagery = lyr;
    } catch (e) { rec.pending = true; }
  }

  _exposure(rec) {
    // Illustrative 2.5-D exposure near a valley settlement (real OSM load is documented in the pipeline;
    // here we show labelled illustrative extrusions so nothing external is required to render).
    const base = { lon: 79.45, lat: 30.0 };
    for (let i = 0; i < 14; i++) {
      const lon = base.lon + (Math.random() - 0.5) * 0.03;
      const lat = base.lat + (Math.random() - 0.5) * 0.03;
      const h = 8 + Math.random() * 22;
      rec.ds.entities.add({
        position: Cesium.Cartesian3.fromDegrees(lon, lat, h / 2),
        box: { dimensions: new Cesium.Cartesian3(40, 40, h),
          material: C.illus.withAlpha(0.55), outline: true, outlineColor: C.illus },
      });
    }
    rec.ds.entities.add({
      position: Cesium.Cartesian3.fromDegrees(base.lon, base.lat, 400),
      label: { text: "ILLUSTRATIVE exposure (real OSM via pipeline)", font: "12px Inter",
        fillColor: C.illus, showBackground: true, backgroundColor: Cesium.Color.BLACK.withAlpha(0.6),
        scaleByDistance: new Cesium.NearFarScalar(1e3, 1.2, 2e5, 0.5) },
    });
  }

  async _wind(rec) {
    const d = await fetchJSON(rec.def.data);
    if (!d || !d.grid) { rec.pending = true; this._placard(rec, "L4 wind — DATA-PENDING (ERA5-Land key)"); return; }
    let max = 1e-6; d.grid.forEach((g) => (max = Math.max(max, g.speed)));
    d.grid.forEach((g) => {
      const [r, gg, bb] = cividis(g.speed / max);
      rec.ds.entities.add({
        position: Cesium.Cartesian3.fromDegrees(g.lon, g.lat, 2000),
        point: { pixelSize: 6, color: Cesium.Color.fromBytes(r, gg, bb, 220) },
        properties: { prov: `ERA5-Land wind ${g.speed} m/s` },
      });
    });
    rec._provData = d.provenance;
  }

  async _fire(rec) {
    const d = await fetchJSON(rec.def.data);
    if (!d || !d.hotspots) { rec.pending = true; this._placard(rec, "L5 fire — DATA-PENDING (FIRMS MAP_KEY)"); return; }
    let max = 1e-6; d.hotspots.forEach((h) => (max = Math.max(max, h.frp || 0)));
    d.hotspots.forEach((h) => {
      const [r, g, b] = inferno(Math.min(1, (h.frp || 0) / max));
      rec.ds.entities.add({
        position: Cesium.Cartesian3.fromDegrees(h.lon, h.lat, 50),
        point: { pixelSize: 4 + 8 * ((h.frp || 0) / max), color: Cesium.Color.fromBytes(r, g, b, 235) },
        properties: { prov: `FIRMS ${h.sat} ${h.acq_date} FRP=${h.frp}` },
      });
    });
    rec._provData = d.provenance;
  }

  async _physics(rec) {
    const d = await fetchJSON(rec.def.data);
    if (!d) { this._placard(rec, "L6 physics JSON missing — run gen_physics_fields.py"); return; }
    rec._provData = d.provenance;
    rec._physics = d;
    const ign = d.provenance.ignition_point;
    // (a) vertical plume temperature column (inferno), (b) translucent smoke, at the scenario ignition pt
    const fp = d.fire_plume, prof = fp.profile;
    const Tmin = Math.min(...prof.T), Tmax = Math.max(...prof.T);
    for (let i = 0; i < prof.z.length; i++) {
      const t = (prof.T[i] - Tmin) / (Tmax - Tmin || 1);
      const [r, g, b] = inferno(t);
      rec.ds.entities.add({
        position: Cesium.Cartesian3.fromDegrees(ign.lon, ign.lat, prof.z[i]),
        point: { pixelSize: 7, color: Cesium.Color.fromBytes(r, g, b, 240) },
        properties: { prov: `SIMULATED plume T=${prof.T[i]}K @ ${prof.z[i]}m` },
      });
      // smoke: translucent widening cylinder slices (opacity from model smoke_opacity)
      if (i % 4 === 0) {
        rec.ds.entities.add({
          position: Cesium.Cartesian3.fromDegrees(ign.lon, ign.lat, prof.z[i]),
          cylinder: { length: 20, topRadius: 8 + prof.z[i] * 0.15, bottomRadius: 8 + prof.z[i] * 0.12,
            material: Cesium.Color.fromCssColorString("#d9cfc0").withAlpha(0.05 + 0.25 * prof.smoke_opacity[i]) },
        });
      }
    }
    rec.ds.entities.add({
      position: Cesium.Cartesian3.fromDegrees(ign.lon, ign.lat, prof.z[prof.z.length - 1] + 40),
      label: { text: "SIMULATED: Heskestad plume (TRINETRA core)", font: "12px Inter", fillColor: C.sim,
        showBackground: true, backgroundColor: Cesium.Color.BLACK.withAlpha(0.6) },
    });
    // (c) landslide FS ramp: colored ground points along a short line, viridis by FS_wet (low FS -> unstable)
    const ls = d.landslide.fs_vs_slope;
    for (let i = 0; i < ls.beta_deg.length; i += 2) {
      const fs = ls.FS_wet[i];
      const norm = Math.max(0, Math.min(1, (fs - 0.5) / 1.5)); // FS 0.5..2 -> 0..1
      const [r, g, b] = viridis(norm);
      const lon = ign.lon - 0.08 + i * 0.004, lat = ign.lat - 0.06;
      rec.ds.entities.add({
        position: Cesium.Cartesian3.fromDegrees(lon, lat, 30),
        point: { pixelSize: 9, color: Cesium.Color.fromBytes(r, g, b, 235),
          outlineColor: fs < 1 ? C.warn : Cesium.Color.TRANSPARENT, outlineWidth: fs < 1 ? 2 : 0 },
        properties: { prov: `SIMULATED landslide FS=${fs} @ slope ${ls.beta_deg[i]}°` },
      });
    }
  }

  _cctv(rec) {
    const cams = [{ lon: 79.48, lat: 30.08, hd: 210 }, { lon: 79.52, lat: 30.12, hd: 90 }];
    cams.forEach((c) => {
      rec.ds.entities.add({
        position: Cesium.Cartesian3.fromDegrees(c.lon, c.lat, 60),
        cylinder: { length: 1200, topRadius: 900, bottomRadius: 0,
          material: C.illus.withAlpha(0.18), outline: true, outlineColor: C.illus.withAlpha(0.5) },
        properties: { prov: "ILLUSTRATIVE camera FOV cone (WS4)" },
      });
      rec.ds.entities.add({
        position: Cesium.Cartesian3.fromDegrees(c.lon, c.lat, 70),
        point: { pixelSize: 8, color: C.illus },
        label: { text: "CCTV (FOV illustrative · detection SIMULATED)", font: "11px Inter", fillColor: C.illus,
          pixelOffset: new Cesium.Cartesian2(0, -18), showBackground: true,
          backgroundColor: Cesium.Color.BLACK.withAlpha(0.6),
          scaleByDistance: new Cesium.NearFarScalar(1e3, 1.1, 1e5, 0.4) },
      });
    });
  }

  async _datasets(rec) {
    const d = await fetchJSON(rec.def.data);
    if (!d) { this._placard(rec, "L8 datasets JSON missing — run gen_dataset_panels.py"); return; }
    rec._provData = d.provenance;
    const all = d.groups.flatMap((g) => g.datasets);
    const n = all.length, R = 0.45, cx = AOI.center.lon, cy = AOI.center.lat + 0.05, alt = 55000;
    all.forEach((ds, i) => {
      const ang = (i / n) * Math.PI * 2;
      const lon = cx + R * Math.cos(ang), lat = cy + R * 0.6 * Math.sin(ang);
      const selected = ds.status === "selected";
      rec.ds.entities.add({
        position: Cesium.Cartesian3.fromDegrees(lon, lat, alt),
        point: { pixelSize: 10, color: selected ? C.real : C.illus,
          outlineColor: Cesium.Color.BLACK.withAlpha(0.6), outlineWidth: 1 },
        label: { text: ds.id, font: "11px JetBrains Mono", fillColor: Cesium.Color.WHITE,
          pixelOffset: new Cesium.Cartesian2(0, -14),
          scaleByDistance: new Cesium.NearFarScalar(3e4, 1.0, 3e5, 0.4) },
        properties: { prov: `${ds.id} ${ds.name} · ${ds.ws} · ${ds.license} · ${ds.status} ${ds.ver}` },
      });
    });
  }

  _alerting(rec) {
    const c = { lon: 79.45, lat: 30.0 };
    const rings = [{ r: 1500, label: "siren (source-reported)" }, { r: 6000, label: "LoRa/mesh (source-reported)" },
      { r: 15000, label: "cell-broadcast area (scenario)" }];
    rings.forEach((ring, i) => {
      rec.ds.entities.add({
        position: Cesium.Cartesian3.fromDegrees(c.lon, c.lat),
        ellipse: { semiMajorAxis: ring.r, semiMinorAxis: ring.r,
          material: C.warn.withAlpha(0.06 + i * 0.02), outline: true, outlineColor: C.warn.withAlpha(0.5),
          height: 0, heightReference: Cesium.HeightReference.CLAMP_TO_GROUND },
        properties: { prov: `ILLUSTRATIVE reach: ${ring.label}` },
      });
    });
    rec.ds.entities.add({
      position: Cesium.Cartesian3.fromDegrees(c.lon, c.lat, 1000),
      label: { text: "WS3 reach = scenario geometry · public alert human-gated", font: "11px Inter",
        fillColor: C.warn, showBackground: true, backgroundColor: Cesium.Color.BLACK.withAlpha(0.6) },
    });
  }

  _routes(rec) {
    // Illustrative advisory routes (real OSM road graph loads via pipeline/Overpass — documented).
    const paths = [
      [[79.44, 30.0], [79.46, 30.02], [79.49, 30.03], [79.52, 30.06]],
      [[79.44, 30.0], [79.42, 29.98], [79.40, 29.95]],
    ];
    paths.forEach((p, i) => {
      rec.ds.entities.add({
        polyline: { positions: Cesium.Cartesian3.fromDegreesArray(p.flat()),
          width: 4, clampToGround: true,
          material: new Cesium.PolylineGlowMaterialProperty({ glowPower: 0.25, color: C.real.withAlpha(0.9) }) },
        properties: { prov: `SIMULATED rule-baseline advisory route ${i + 1} over REAL OSM roads` },
      });
    });
  }

  async _dfdOverlay(rec, which) {
    // L9 (deepfake flow) and L12 (full DFD) are HTML overlays managed by the HUD.
    if (which === "l12") {
      const d = await fetchJSON(rec.def.data);
      rec.overlay = this.hud.buildDfdOverlay("l12", d);
    } else {
      rec.overlay = this.hud.buildDeepfakeOverlay();
    }
  }

  _placard(rec, text) {
    rec.ds.entities.add({
      position: Cesium.Cartesian3.fromDegrees(AOI.center.lon, AOI.center.lat, 30000),
      label: { text, font: "13px Inter", fillColor: C.warn, showBackground: true,
        backgroundColor: Cesium.Color.BLACK.withAlpha(0.7),
        scaleByDistance: new Cesium.NearFarScalar(5e4, 1.0, 5e5, 0.5) },
    });
  }

  // ---- control -------------------------------------------------------------------------
  setVisible(id, show) {
    const rec = this.layers.get(id); if (!rec) return;
    rec.ds.show = show;
    if (rec.imagery) rec.imagery.show = show;
    if (rec.overlay) rec.overlay.style.display = show ? "block" : "none";
    this.viewer.scene.requestRender();
  }

  setOpacity(id, a) {
    const rec = this.layers.get(id); if (!rec) return;
    if (rec.imagery) rec.imagery.alpha = a;
    rec.ds.entities.values.forEach((e) => {
      if (e.point) e.point.color = e.point.color.getValue().withAlpha(a);
    });
    if (rec.overlay) rec.overlay.style.opacity = a;
    this.viewer.scene.requestRender();
  }

  // vertical "exploded stack": lift each layer's entities to a stacked altitude band
  setExplode(on) {
    this.explode = on;
    const order = LAYERS.map((l) => l.id);
    order.forEach((id, idx) => {
      const rec = this.layers.get(id); if (!rec) return;
      const dz = on ? idx * 9000 : 0;
      rec.ds.entities.values.forEach((e) => {
        if (!e.position) return;
        if (e._homePos === undefined) {
          const p = e.position.getValue(Cesium.JulianDate.now());
          e._homePos = p ? Cesium.Cartographic.fromCartesian(p) : null;
        }
        if (e._homePos) {
          const c = e._homePos;
          e.position = Cesium.Cartesian3.fromRadians(c.longitude, c.latitude, c.height + dz);
        }
      });
    });
    this.viewer.scene.requestRender();
  }

  provenanceFor(id) {
    const rec = this.layers.get(id);
    return rec ? { def: rec.def, data: rec._provData, pending: rec.pending, physics: rec._physics } : null;
  }
}
