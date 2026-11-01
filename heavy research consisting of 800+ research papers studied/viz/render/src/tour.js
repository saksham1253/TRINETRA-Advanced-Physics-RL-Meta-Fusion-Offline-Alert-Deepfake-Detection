// tour.js — guided cinematic tour S0→S14 (from STORYBOARD.md). Smooth ease-in-out camera flights,
// progressive layer reveal, honest captions. DATA-PENDING shots still play but show their placard.
import * as Cesium from "cesium";

// each shot: dest lon/lat/height(m), orientation heading/pitch(deg), seconds, layers to switch ON (cumulative), caption
export const SHOTS = [
  { id: "S0", t: 4, dest: [79.35, 30.15, 20000000], o: [0, -90, 0], on: [],
    cap: "TRINETRA / HIMKAVACH — multi-hazard advisory early-warning · data-stack reveal" },
  { id: "S1", t: 6, dest: [79.35, 29.9, 450000], o: [0, -55, 0], on: ["L0"],
    cap: "REAL: Esri World Imagery (live) / Sentinel-2 cloudless · terrain AWS Terrain Tiles · WGS-84" },
  { id: "S2", t: 6, dest: [79.2, 30.05, 90000], o: [20, -35, 0], on: ["L1"],
    cap: "REAL: Copernicus DEM GLO-30, 30 m, 2021 · slope derived · VE ×1.0" },
  { id: "S3", t: 5, dest: [79.2, 30.05, 70000], o: [40, -40, 0], on: ["L2"],
    cap: "REAL: ESA WorldCover 10 m 2021 · © ESA WorldCover project / modified Copernicus Sentinel data" },
  { id: "S4", t: 5, dest: [79.45, 30.0, 18000], o: [0, -45, 0], on: ["L3"],
    cap: "REAL: OSM © OpenStreetMap contributors (ODbL) · WorldPop CC-BY" },
  { id: "S5", t: 6, dest: [79.3, 30.05, 120000], o: [10, -40, 0], on: ["L4"], pending: true,
    cap: "REAL: ERA5-Land hourly, 2021 · Generated using Copernicus Climate Change Service information" },
  { id: "S6", t: 7, dest: [79.5, 30.1, 60000], o: [12, -45, 0], on: ["L5"], pending: true,
    cap: "REAL: NASA FIRMS VIIRS/MODIS active fire, 2021 (archive) · GIBS thermal anomalies" },
  { id: "S7", t: 8, dest: [79.52, 30.1, 25000], o: [8, -20, 0], on: ["L6"],
    cap: "SIMULATED: Heskestad plume + Iverson/FS landslide (TRINETRA numpy core) · params in panel · NOT an observation" },
  { id: "S8", t: 5, dest: [79.48, 30.08, 6000], o: [0, -10, 0], on: ["L7"],
    cap: "REAL: dataset sample (license-permitting) · ILLUSTRATIVE: camera FOV · SIMULATED: detection" },
  { id: "S9", t: 6, dest: [79.35, 29.95, 110000], o: [0, -55, 0], on: ["L8"],
    cap: "REAL(metadata): DATASETS.md D-IDs · counts as-recorded · licenses UNVERIFIED where tagged" },
  { id: "S10", t: 5, dest: [79.35, 29.9, 130000], o: [0, -55, 0], on: ["L9"],
    cap: "ILLUSTRATIVE pipeline · REAL(stats): dataset counts · SIMULATED: detector score (cap 0.40)" },
  { id: "S11", t: 6, dest: [79.45, 30.0, 45000], o: [8, -50, 0], on: ["L10"],
    cap: "ILLUSTRATIVE: tier reach geometry · REAL: WorldPop exposure · ranges source-reported · human-gated" },
  { id: "S12", t: 5, dest: [79.44, 30.0, 12000], o: [0, -30, 0], on: ["L11"],
    cap: "SIMULATED: rule-baseline advisory routing over REAL OSM roads · no trained policy (by design)" },
  { id: "S13", t: 12, dest: [79.35, 29.7, 160000], o: [6, -35, 0], on: [], explode: true,
    cap: "All layers — REAL (green) vs SIMULATED/ILLUSTRATIVE (amber). Exploded for inspection." },
  { id: "S14", t: 14, dest: [79.35, 29.85, 220000], o: [5, -45, 0], on: ["L12"], explode: false,
    cap: "ILLUSTRATIVE: high-level data flow (see 02 + _CANON) · advisory, human-in-loop, never autonomous" },
];

export class Tour {
  constructor(viewer, lm, hud) {
    this.viewer = viewer; this.lm = lm; this.hud = hud;
    this.i = -1; this.playing = false; this._timer = null;
    document.getElementById("tourPlay").addEventListener("click", () => this.toggle());
    document.getElementById("tourNext").addEventListener("click", () => this.step(+1));
    document.getElementById("tourPrev").addEventListener("click", () => this.step(-1));
  }

  toggle() { this.playing ? this.pause() : this.play(); }

  play() {
    this.playing = true;
    document.getElementById("tourPlay").textContent = "❙❙ Pause";
    if (this.i < 0) this.i = 0;
    this._run();
  }

  pause() {
    this.playing = false;
    document.getElementById("tourPlay").textContent = "▶ Tour";
    if (this._timer) clearTimeout(this._timer);
  }

  step(d) {
    this.pause();
    this.i = Math.max(0, Math.min(SHOTS.length - 1, this.i + d));
    this._apply(SHOTS[this.i], true);
  }

  _run() {
    if (!this.playing) return;
    const shot = SHOTS[this.i];
    this._apply(shot, false);
    this._timer = setTimeout(() => {
      if (!this.playing) return;
      if (this.i < SHOTS.length - 1) { this.i++; this._run(); }
      else { this.pause(); }
    }, shot.t * 1000);
  }

  _apply(shot, instant) {
    // cumulative reveal: turn on this shot's layers
    (shot.on || []).forEach((id) => { this.lm.setVisible(id, true); this.hud.setChecked(id, true); });
    if (shot.explode !== undefined) { this.lm.setExplode(shot.explode); document.getElementById("explodeToggle").checked = shot.explode; }
    const last = shot.on && shot.on.length ? shot.on[shot.on.length - 1] : null;
    if (last) this.hud.setProvenanceById(last);
    this.hud.setTourCaption(`${shot.id} · ${shot.cap}`);
    this.hud.setTourProgress((this.i) / (SHOTS.length - 1));
    this.viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(shot.dest[0], shot.dest[1], shot.dest[2]),
      orientation: {
        heading: Cesium.Math.toRadians(shot.o[0]),
        pitch: Cesium.Math.toRadians(shot.o[1]),
        roll: Cesium.Math.toRadians(shot.o[2] || 0),
      },
      duration: instant ? 0 : Math.min(3, shot.t * 0.45),
      easingFunction: Cesium.EasingFunction.QUADRATIC_IN_OUT,
    });
  }
}
