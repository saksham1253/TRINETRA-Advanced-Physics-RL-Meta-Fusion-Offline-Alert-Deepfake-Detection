// config.js — single source of layer/scene configuration for the TRINETRA/HIMKAVACH 3D data-stack reveal.
// Every layer declares its REAL vs SIMULATED kind + provenance caption (mission HARD RULES 2 & 3).
// Endpoint strings marked VERIFY were flagged in DATA_SOURCES.md / STACK_DECISION.md and are confirmed at
// runtime by the app (a failed source degrades gracefully to DATA-PENDING, never to fabricated data).

export const AOI = {
  name: "Uttarakhand Himalaya — 2021 pre-monsoon forest-fire season",
  bbox: [78.5, 29.5, 80.2, 30.8], // lon_min, lat_min, lon_max, lat_max
  center: { lon: 79.35, lat: 30.15 },
  peakWindow: "2021-04-25 → 2021-05-12",
  verticalExaggeration: 1.0, // shown on-screen; change here if exaggerated (label updates)
};

// Camera "home" for the AOI (lon/lat/height m, heading/pitch deg)
export const CAMERA_HOME = { lon: 79.35, lat: 29.55, height: 95000, heading: 0, pitch: -40 };
export const CAMERA_SPACE = { lon: 79.0, lat: 22.0, height: 9_000_000, heading: 0, pitch: -90 };

// Imagery basemaps. "open" set is license-clean for the recorded video; "esri" is live-only (not in video).
export const BASEMAPS = {
  esriWorldImagery: {
    label: "Esri World Imagery (live)",
    kind: "REAL",
    videoSafe: false, // exportTilesAllowed=false → live only, keep OUT of recorded video
    url: "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attribution: "Source: Esri, Vantor, Earthstar Geographics, and the GIS User Community",
    provenance: { source: "Esri World Imagery", product: "World_Imagery/MapServer", date: "live",
      resolution: "≤1 m (select areas)", license: "Esri ToS — live use only, no tile export" },
  },
  gibsTrueColor: {
    label: "NASA GIBS VIIRS true-color",
    kind: "REAL",
    videoSafe: true,
    // VERIFY: GIBS WMTS REST template (SNPP VIIRS CorrectedReflectance TrueColor), GoogleMapsCompatible
    url: "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/VIIRS_SNPP_CorrectedReflectance_TrueColor/default/2021-05-01/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg",
    attribution: "Imagery courtesy NASA EOSDIS GIBS / Worldview",
    provenance: { source: "NASA GIBS", product: "VIIRS_SNPP_CorrectedReflectance_TrueColor", date: "2021-05-01",
      resolution: "~250 m", license: "NASA open data (credit requested)" },
  },
};

// Terrain providers. AWS Terrain Tiles (terrarium) is token-free; Cesium ion is an optional upgrade.
export const TERRAIN = {
  tokenFree: {
    label: "AWS Terrain Tiles (terrarium)",
    attribution: "Terrain: AWS Terrain Tiles / Mapzen (ODbL/various source DEMs)",
    provenance: { source: "AWS Terrain Tiles", product: "terrarium", date: "static",
      resolution: "SRTM/other, ~30–90 m", license: "open (per source DEM)" },
  },
};

// Required persistent attributions (exact strings from LICENSES.md). Shown in the footer at all times.
export const ATTRIBUTIONS = [
  "© CesiumJS (Apache-2.0)",
  "Terrain: AWS Terrain Tiles / Mapzen",
  "Copernicus Sentinel data 2021",
  "ESA WorldCover project / modified Copernicus Sentinel data",
  "© OpenStreetMap contributors (ODbL)",
  "WorldPop (www.worldpop.org, CC-BY)",
  "NASA FIRMS / GIBS / LANCE (credit requested)",
  "Generated using Copernicus Climate Change Service information (ERA5-Land)",
];

// Ordered layer registry (L0..L12). `data` points to a browser-fetchable JSON when a generator produced it.
// `kind`: REAL | REAL_CODE | SIMULATED | ILLUSTRATIVE. `status`: ready | data_pending.
export const LAYERS = [
  { id: "L0", name: "Earth context", kind: "REAL", status: "ready", color: "#5fb0d9",
    provenance: { source: "Esri / NASA GIBS + AWS Terrain", product: "basemap+terrain", date: "live/2021-05",
      resolution: "globe→AOI", license: "see footer" },
    note: "Globe → Uttarakhand AOI. Basemap is live Esri or video-safe GIBS." },

  { id: "L1", name: "Terrain & relief (DEM)", kind: "REAL", status: "ready", color: "#9b8c70",
    provenance: { source: "Copernicus DEM GLO-30", product: "COP-DEM_GLO-30", date: "2021",
      resolution: "30 m", license: "Copernicus free/open" },
    note: "Himalayan relief; slope β drives the physics. Vertical exaggeration labelled on screen." },

  { id: "L2", name: "Land cover / fuel", kind: "REAL", status: "ready", color: "#6f9e5a",
    provenance: { source: "ESA WorldCover", product: "WorldCover 10 m v200", date: "2021",
      resolution: "10 m", license: "CC-BY-4.0" },
    note: "Forest/fuel classes — what burns, where." },

  { id: "L3", name: "Built environment & exposure", kind: "REAL", status: "ready", color: "#c3a3d9",
    provenance: { source: "OpenStreetMap + WorldPop", product: "buildings/roads + pop grid", date: "2020/2021",
      resolution: "vector / ~100 m", license: "ODbL (produced work) / CC-BY" },
    note: "Who/what is exposed. Rural Himalaya is sparsely mapped — shown honestly." },

  { id: "L4", name: "Atmosphere (wind field)", kind: "REAL", status: "data_pending", color: "#7fc7c0",
    data: "./data/l4_era5_wind.json",
    provenance: { source: "ERA5-Land (C3S)", product: "reanalysis-era5-land", date: "2021 (AOI extract)",
      resolution: "~9 km hourly", license: "CC-BY (DOI 10.24381/cds.e2161bac)" },
    note: "Wind governs spread + plume tilt. Needs a free CDS extract; renders nothing until supplied." },

  { id: "L5", name: "Real fire observations", kind: "REAL", status: "data_pending", color: "#f06543",
    data: "./data/l5_firms.json",
    provenance: { source: "NASA FIRMS VIIRS/MODIS", product: "active-fire archive", date: "2021 AOI",
      resolution: "375 m / 1 km", license: "NASA open (credit requested)" },
    note: "Real 2021 hotspots. Needs a free FIRMS MAP_KEY archive extract; DATA-PENDING until supplied." },

  { id: "L6", name: "WS1 physics + fusion", kind: "SIMULATED", status: "ready", color: "#f2a65a",
    data: "./data/l6_physics.json",
    provenance: { source: "TRINETRA numpy core", product: "Heskestad/Iverson/FS/Caine", date: "computed",
      resolution: "scenario", license: "n/a (our code)" },
    note: "SIMULATED fields computed by running our real physics code. Parameters shown. Not a measurement." },

  { id: "L7", name: "WS4 CCTV", kind: "ILLUSTRATIVE", status: "ready", color: "#d9c35f",
    provenance: { source: "project (WS4)", product: "camera FOV + sample", date: "n/a",
      resolution: "n/a", license: "dataset-dependent (no faces shown)" },
    note: "Camera FOV cones = illustrative; detections SIMULATED (no trained detector exists)." },

  { id: "L8", name: "Dataset registry", kind: "REAL", status: "ready", color: "#5fb0d9",
    data: "./data/l8_datasets.json",
    provenance: { source: "DATASETS.md", product: "registry (26 quick-link D-IDs)", date: "2026-10",
      resolution: "n/a", license: "per dataset (tags preserved)" },
    note: "Metadata copied verbatim. Candidates are registry entries, not downloaded data." },

  { id: "L9", name: "WS2 deepfake verification", kind: "ILLUSTRATIVE", status: "ready", color: "#b06fd9",
    provenance: { source: "project (WS2)", product: "verification data-flow", date: "n/a",
      resolution: "n/a", license: "stats only; no media (privacy)" },
    note: "Pipeline flow is illustrative; detector score SIMULATED with a hard 0.40 reliability cap." },

  { id: "L10", name: "WS3 tiered alerting", kind: "ILLUSTRATIVE", status: "ready", color: "#e2574c",
    provenance: { source: "project (WS3) + WorldPop", product: "tier reach geometry", date: "n/a",
      resolution: "scenario", license: "ranges source-reported" },
    note: "Reach rings = scenario geometry (no acoustic model in code). Public alert is human-gated." },

  { id: "L11", name: "WS5 advisory routing", kind: "SIMULATED", status: "ready", color: "#5fd9b0",
    provenance: { source: "OSM roads + WS5 rule baseline", product: "advisory routes", date: "n/a",
      resolution: "road graph", license: "ODbL (roads)" },
    note: "Rule-baseline advisory over real roads. No trained RL policy exists (by design)." },

  { id: "L12", name: "Fusion & decision (DFD)", kind: "ILLUSTRATIVE", status: "ready", color: "#5fb0d9",
    data: "./data/l12_dfd.json",
    provenance: { source: "02_system_architecture + _CANON", product: "high-level data flow", date: "n/a",
      resolution: "n/a", license: "n/a" },
    note: "High-level model DFD. Advisory, human-in-loop, never autonomous." },
];
