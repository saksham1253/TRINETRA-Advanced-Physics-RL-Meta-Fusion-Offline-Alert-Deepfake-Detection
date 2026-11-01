// hud.js — all DOM/HUD: layer panel, basemap switch, provenance caption, legend, geospatial readouts,
// north arrow, attributions, and the HTML overlays for the deepfake flow (L9) + high-level DFD (L12).
import * as Cesium from "cesium";
import { LAYERS, BASEMAPS, ATTRIBUTIONS, AOI } from "./config.js";
import { inferno, viridis, cividis, magma, paintLegend } from "./colormaps.js";

const KIND_LABEL = { REAL: "REAL", REAL_CODE: "REAL (code)", SIMULATED: "SIMULATED", ILLUSTRATIVE: "ILLUSTRATIVE" };
const kindClass = (k) => (k === "REAL" || k === "REAL_CODE") ? "real" : k === "SIMULATED" ? "sim" : "ui";

export class Hud {
  constructor(viewer, onLayerToggle, onOpacity, onBasemap, onExplode) {
    this.viewer = viewer;
    this.onLayerToggle = onLayerToggle;
    this.onOpacity = onOpacity;
    this.onBasemap = onBasemap;
    this.onExplode = onExplode;
    this._overlays = {};
  }

  init() {
    this._buildLayerList();
    this._buildBasemapList();
    this._buildAttributions();
    document.getElementById("explodeToggle").addEventListener("change", (e) => this.onExplode(e.target.checked));
    this._startReadout();
    paintLegend(document.getElementById("legendCanvas"), viridis);
  }

  _buildLayerList() {
    const host = document.getElementById("layerList");
    host.innerHTML = "";
    LAYERS.forEach((def) => {
      const row = document.createElement("div");
      row.className = "layer-item";
      const kc = kindClass(def.kind);
      row.innerHTML = `
        <input type="checkbox" id="chk_${def.id}" />
        <span class="sw" style="background:${def.color}"></span>
        <label for="chk_${def.id}">
          <span>${def.id} ${def.name}</span>
          <span class="kindtag ${kc === "real" ? "real" : "sim"}">${def.kind === "REAL" || def.kind === "REAL_CODE" ? "REAL" : (def.kind === "SIMULATED" ? "SIM" : "ILL")}</span>
        </label>
        <input type="range" id="op_${def.id}" min="0" max="100" value="100" title="opacity" />`;
      host.appendChild(row);
      row.querySelector(`#chk_${def.id}`).addEventListener("change", (e) => {
        this.onLayerToggle(def.id, e.target.checked);
        if (e.target.checked) this.setProvenanceById(def.id);
      });
      row.querySelector(`#op_${def.id}`).addEventListener("input", (e) =>
        this.onOpacity(def.id, parseInt(e.target.value, 10) / 100));
    });
  }

  _buildBasemapList() {
    const host = document.getElementById("basemapList");
    host.innerHTML = "";
    Object.entries(BASEMAPS).forEach(([key, bm], i) => {
      const row = document.createElement("div");
      row.className = "layer-item";
      row.innerHTML = `
        <input type="radio" name="basemap" id="bm_${key}" ${i === 0 ? "checked" : ""}/>
        <label for="bm_${key}">${bm.label}${bm.videoSafe ? "" : " ⚠"}</label>`;
      host.appendChild(row);
      row.querySelector(`#bm_${key}`).addEventListener("change", () => this.onBasemap(key));
    });
    const note = document.createElement("div");
    note.style.cssText = "font-size:9.5px;color:var(--ink-faint);margin-top:4px;line-height:1.4";
    note.textContent = "⚠ Esri = live only, not for recorded video (LICENSES.md). Open source is video-safe.";
    host.appendChild(note);
  }

  _buildAttributions() {
    document.getElementById("attrib").textContent = ATTRIBUTIONS.join("  ·  ");
  }

  setChecked(id, on) {
    const el = document.getElementById(`chk_${id}`);
    if (el) el.checked = on;
  }

  setProvenanceById(id) {
    const def = LAYERS.find((l) => l.id === id);
    if (!def) return;
    const kc = kindClass(def.kind);
    const kindEl = document.getElementById("provKind");
    kindEl.className = `prov-kind ${kc === "real" ? "real" : (def.kind === "SIMULATED" ? "sim" : "ui")}`;
    kindEl.textContent = KIND_LABEL[def.kind] || def.kind;
    document.getElementById("provTitle").textContent = `${def.id} — ${def.name}`;
    const p = def.provenance || {};
    const rows = [["source", p.source], ["product", p.product], ["date", p.date],
      ["resolution", p.resolution], ["license", p.license]];
    document.getElementById("provMeta").innerHTML = rows
      .filter(([, v]) => v).map(([k, v]) => `<tr><td class="k">${k}</td><td class="v">${v}</td></tr>`).join("");
    document.getElementById("provNote").textContent = def.note || "";
    this._legendFor(def);
  }

  _legendFor(def) {
    const title = document.getElementById("legendTitle");
    const unit = document.getElementById("legendUnit");
    const mn = document.getElementById("legendMin"), mx = document.getElementById("legendMax");
    const canvas = document.getElementById("legendCanvas");
    const set = (map, name, lo, hi, u) => {
      paintLegend(canvas, map); title.textContent = name; mn.textContent = lo; mx.textContent = hi; unit.textContent = u;
    };
    if (def.id === "L6") set(inferno, "LEGEND · inferno", "ambient", "hot", "plume T (K)");
    else if (def.id === "L5") set(magma, "LEGEND · magma", "0", "max", "FRP (MW)");
    else if (def.id === "L4") set(cividis, "LEGEND · cividis", "calm", "strong", "wind (m/s)");
    else if (def.id === "L1") set(viridis, "LEGEND · elevation", "low", "high", "m");
    else set(viridis, "LEGEND · viridis", "0", "1", "risk");
  }

  // ---- geospatial readouts (lon/lat/elev/eye/time/scale + north arrow) --------------------
  _startReadout() {
    const scene = this.viewer.scene, camera = scene.camera;
    const g = (id) => document.getElementById(id);
    this.viewer.clock.onTick.addEventListener(() => {
      const c = camera.positionCartographic;
      g("roLon").textContent = Cesium.Math.toDegrees(c.longitude).toFixed(4) + "°";
      g("roLat").textContent = Cesium.Math.toDegrees(c.latitude).toFixed(4) + "°";
      g("roEye").textContent = (c.height / 1000).toFixed(1) + " km";
      // ground elevation under camera (sampled from terrain if available)
      const carto = scene.globe.getHeight(c);
      g("roElev").textContent = carto !== undefined ? carto.toFixed(0) + " m" : "—";
      g("roTime").textContent = Cesium.JulianDate.toIso8601(this.viewer.clock.currentTime, 0).replace("T", " ").replace("Z", "");
      // approximate map scale: metres per pixel at screen centre
      const mpp = this._metersPerPixel();
      g("roScale").textContent = mpp ? (mpp > 1000 ? (mpp / 1000).toFixed(1) + " km/px" : mpp.toFixed(0) + " m/px") : "—";
      // north arrow: rotate opposite camera heading
      g("northArrow").style.transform = `rotate(${-Cesium.Math.toDegrees(camera.heading)}deg)`;
    });
  }

  _metersPerPixel() {
    const scene = this.viewer.scene;
    const w = scene.canvas.clientWidth, h = scene.canvas.clientHeight;
    const c1 = scene.camera.pickEllipsoid(new Cesium.Cartesian2(w / 2, h / 2));
    const c2 = scene.camera.pickEllipsoid(new Cesium.Cartesian2(w / 2 + 1, h / 2));
    if (!c1 || !c2) return null;
    return Cesium.Cartesian3.distance(c1, c2);
  }

  setTourCaption(t) { document.getElementById("tourCaption").textContent = t; }
  setTourProgress(f) { document.getElementById("tourProgressBar").style.width = `${Math.round(f * 100)}%`; }

  showBootError(msg) {
    const el = document.getElementById("bootError");
    el.classList.remove("hidden");
    el.textContent = "Boot error:\n\n" + msg;
  }

  // ---- HTML overlays: L9 deepfake flow + L12 DFD --------------------------------------
  buildDeepfakeOverlay() {
    const nodes = ["Social-media intake", "Provenance check", "Reverse image search",
      "Deepfake detector (cap 0.40)", "Corroboration", "Human gate"];
    const el = this._overlayShell("l9", "WS2 — social-media verification (ILLUSTRATIVE flow)");
    const flow = document.createElement("div");
    flow.style.cssText = "display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:8px 10px";
    nodes.forEach((n, i) => {
      const chip = document.createElement("div");
      const cap = n.includes("0.40");
      chip.style.cssText = `font-size:11px;padding:5px 9px;border-radius:5px;border:1px solid ${cap ? "#F2B141" : "#2A3744"};` +
        `color:${cap ? "#F2B141" : "#E6EDF3"};background:#0E141B`;
      chip.textContent = n;
      flow.appendChild(chip);
      if (i < nodes.length - 1) { const a = document.createElement("span"); a.textContent = "→"; a.style.color = "#4CA6FF"; flow.appendChild(a); }
    });
    el.appendChild(flow);
    const note = document.createElement("div");
    note.style.cssText = "font-size:10px;color:#9FB0BF;padding:0 10px 8px;font-style:italic";
    note.textContent = "ILLUSTRATIVE pipeline · detector score SIMULATED, hard-capped at 0.40 reliability · never autonomous (R19).";
    el.appendChild(note);
    document.body.appendChild(el);
    el.style.display = "none";
    this._overlays.l9 = el;
    return el;
  }

  buildDfdOverlay(which, data) {
    const el = this._overlayShell("l12", "High-level data flow (ILLUSTRATIVE)");
    if (!data) { el.appendChild(this._p("DFD data missing (l12_dfd.json)")); document.body.appendChild(el); el.style.display = "none"; return el; }
    const groups = ["sensing", "perception", "physics", "fusion", "decision", "action"];
    const svgNS = "http://www.w3.org/2000/svg";
    const W = 760, H = 300, colX = {}, pad = 60;
    groups.forEach((g, i) => (colX[g] = pad + i * ((W - 2 * pad) / (groups.length - 1))));
    const pos = {};
    const perGroup = {};
    data.nodes.forEach((n) => (perGroup[n.group] = (perGroup[n.group] || 0) + 1));
    const idx = {};
    data.nodes.forEach((n) => {
      idx[n.group] = (idx[n.group] || 0);
      const count = perGroup[n.group];
      const y = (H / (count + 1)) * (idx[n.group] + 1);
      pos[n.id] = { x: colX[n.group], y };
      idx[n.group]++;
    });
    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("width", W); svg.setAttribute("height", H);
    svg.style.cssText = "display:block";
    data.edges.forEach((e) => {
      const a = pos[e.from], b = pos[e.to];
      const line = document.createElementNS(svgNS, "line");
      line.setAttribute("x1", a.x); line.setAttribute("y1", a.y);
      line.setAttribute("x2", b.x); line.setAttribute("y2", b.y);
      line.setAttribute("stroke", "#4CA6FF"); line.setAttribute("stroke-width", "1.2"); line.setAttribute("opacity", "0.5");
      svg.appendChild(line);
    });
    data.nodes.forEach((n) => {
      const p = pos[n.id];
      const g = document.createElementNS(svgNS, "g");
      const rect = document.createElementNS(svgNS, "rect");
      const col = (n.kind === "REAL") ? "#38D39F" : "#F2B141";
      rect.setAttribute("x", p.x - 52); rect.setAttribute("y", p.y - 15);
      rect.setAttribute("width", 104); rect.setAttribute("height", 30); rect.setAttribute("rx", 5);
      rect.setAttribute("fill", "#0E141B"); rect.setAttribute("stroke", col); rect.setAttribute("stroke-width", "1.2");
      g.appendChild(rect);
      const txt = document.createElementNS(svgNS, "text");
      txt.setAttribute("x", p.x); txt.setAttribute("y", p.y + 3); txt.setAttribute("text-anchor", "middle");
      txt.setAttribute("fill", "#E6EDF3"); txt.setAttribute("font-size", "9"); txt.setAttribute("font-family", "Inter");
      txt.textContent = n.label.length > 20 ? n.label.slice(0, 19) + "…" : n.label;
      g.appendChild(txt);
      g.appendChild(this._svgTitle(svgNS, `${n.label} — ${n.kind}: ${n.detail}`));
      svg.appendChild(g);
    });
    el.appendChild(svg);
    el.appendChild(this._p("level = max(conformal_level(fused_risk, p*), shield_floor), p*≈0.0476 · advisory, human-in-loop, never autonomous.", true));
    document.body.appendChild(el);
    el.style.display = "none";
    this._overlays.l12 = el;
    return el;
  }

  _overlayShell(id, title) {
    const el = document.createElement("div");
    el.id = `overlay_${id}`;
    el.className = "panel";
    el.style.cssText = "left:50%;top:14%;transform:translateX(-50%);z-index:12;max-width:800px";
    const h = document.createElement("div"); h.className = "panel-h"; h.textContent = title;
    el.appendChild(h);
    return el;
  }
  _p(t, mono) {
    const d = document.createElement("div");
    d.style.cssText = `font-size:10.5px;color:#9FB0BF;padding:6px 10px 2px;${mono ? "font-family:var(--mono)" : ""}`;
    d.textContent = t; return d;
  }
  _svgTitle(ns, t) { const el = document.createElementNS(ns, "title"); el.textContent = t; return el; }
}
