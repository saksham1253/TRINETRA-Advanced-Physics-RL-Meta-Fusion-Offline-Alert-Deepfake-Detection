// main.js — bootstrap the TRINETRA/HIMKAVACH 3D data-stack viewer.
// Token-free: Esri World Imagery (imagery) + Esri WorldElevation3D (terrain). No Cesium ion account needed.
// preserveDrawingBuffer:true so the local per-frame PNG recorder (HOW_TO_REPRODUCE) can read the canvas.
import * as Cesium from "cesium";
import "cesium/Build/Cesium/Widgets/widgets.css";
import { AOI, CAMERA_HOME, CAMERA_SPACE, BASEMAPS } from "./config.js";
import { Hud } from "./hud.js";
import { LayerManager } from "./layers.js";
import { Tour } from "./tour.js";

// No ion account: disable the default token so Cesium never calls ion endpoints.
Cesium.Ion.defaultAccessToken = "";

const ESRI_TERRAIN = "https://elevation3d.arcgis.com/arcgis/rest/services/WorldElevation3D/Terrain3D/ImageServer";
const ESRI_IMAGERY = "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer";

async function boot() {
  const viewer = new Cesium.Viewer("cesiumContainer", {
    baseLayerPicker: false, geocoder: false, homeButton: false, sceneModePicker: false,
    navigationHelpButton: false, fullscreenButton: false, infoBox: false, selectionIndicator: false,
    animation: false, timeline: true, baseLayer: false,
    contextOptions: { webgl: { preserveDrawingBuffer: true } },
  });

  const scene = viewer.scene;
  scene.globe.enableLighting = true;
  scene.globe.depthTestAgainstTerrain = true;
  scene.skyAtmosphere.show = true;
  scene.fog.enabled = true;
  scene.fog.density = 1.2e-4;
  scene.highDynamicRange = true;
  viewer.shadows = false; // soft terrain self-shadow is costly; keep off by default for perf

  // event-window clock (2021-04-25 → 2021-05-12), AOI local morning illumination
  const start = Cesium.JulianDate.fromIso8601("2021-04-25T05:00:00Z");
  const stop = Cesium.JulianDate.fromIso8601("2021-05-12T05:00:00Z");
  viewer.clock.startTime = start.clone();
  viewer.clock.stopTime = stop.clone();
  viewer.clock.currentTime = start.clone();
  viewer.clock.clockRange = Cesium.ClockRange.LOOP_STOP;
  viewer.clock.multiplier = 36000;
  if (viewer.timeline) viewer.timeline.zoomTo(start, stop);

  // --- terrain (Esri WorldElevation3D, token-free) ---
  try {
    viewer.scene.setTerrain(new Cesium.Terrain(Cesium.ArcGISTiledElevationTerrainProvider.fromUrl(ESRI_TERRAIN)));
  } catch (e) { console.warn("terrain load failed, using ellipsoid", e); }

  // --- imagery basemaps ---
  const imageryLayers = viewer.imageryLayers;
  const basemapLayers = {};
  // Esri World Imagery (default, live only)
  try {
    const esri = await Cesium.ArcGisMapServerImageryProvider.fromUrl(ESRI_IMAGERY);
    basemapLayers.esriWorldImagery = imageryLayers.addImageryProvider(esri);
  } catch (e) { console.warn("Esri imagery failed", e); }
  // NASA GIBS VIIRS true-color (video-safe), hidden until chosen
  try {
    const gibs = new Cesium.UrlTemplateImageryProvider({
      url: BASEMAPS.gibsTrueColor.url, maximumLevel: 9,
      credit: new Cesium.Credit(BASEMAPS.gibsTrueColor.attribution),
    });
    basemapLayers.gibsTrueColor = imageryLayers.addImageryProvider(gibs);
    basemapLayers.gibsTrueColor.show = false;
  } catch (e) { console.warn("GIBS imagery failed", e); }

  // --- HUD + layers + tour ---
  let lm; // forward ref
  const hud = new Hud(
    viewer,
    (id, on) => lm && lm.setVisible(id, on),
    (id, a) => lm && lm.setOpacity(id, a),
    (key) => {
      Object.entries(basemapLayers).forEach(([k, lyr]) => { if (lyr) lyr.show = (k === key); });
      scene.requestRender();
    },
    (on) => lm && lm.setExplode(on),
  );
  hud.init();

  lm = new LayerManager(viewer, hud);
  await lm.buildAll();

  new Tour(viewer, lm, hud);
  hud.setProvenanceById("L0");

  // open on the globe, then ease to the AOI
  viewer.camera.setView({
    destination: Cesium.Cartesian3.fromDegrees(CAMERA_SPACE.lon, CAMERA_SPACE.lat, CAMERA_SPACE.height),
  });
  setTimeout(() => {
    viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(CAMERA_HOME.lon, CAMERA_HOME.lat, CAMERA_HOME.height),
      orientation: { heading: 0, pitch: Cesium.Math.toRadians(CAMERA_HOME.pitch), roll: 0 },
      duration: 3,
    });
  }, 600);

  // click any entity → show its provenance string
  const handler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
  handler.setInputAction((click) => {
    const picked = scene.pick(click.position);
    if (picked && picked.id && picked.id.properties && picked.id.properties.prov) {
      const v = picked.id.properties.prov.getValue(viewer.clock.currentTime);
      document.getElementById("provNote").textContent = v;
    }
  }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

  window.__viewer = viewer; // for the recorder script
}

boot().catch((e) => {
  const h = new Hud();
  try { h.showBootError(e && e.stack ? e.stack : String(e)); }
  catch { document.getElementById("bootError").classList.remove("hidden"); document.getElementById("bootError").textContent = String(e); }
});
