// MapLibre style for the console. Offline-only sources: public/geo/*.json (tools/build_geo_pack.py) and the trn-dem:// terrain
// protocol (public/tiles/terrarium). No text labels are drawn by the map (no glyph server needed offline); labels are HTML.
import type { StyleSpecification } from 'maplibre-gl'

const BASE = import.meta.env.BASE_URL
const EMPTY = { type: 'geojson' as const, data: { type: 'FeatureCollection' as const, features: [] } }

export const SEV_COLORS = {
  dark: { advisory: '#2EC4B6', watch: '#FFC145', warning: '#FF7A1A', emergency: '#FF3B30' },
  light: { advisory: '#0F766E', watch: '#A16207', warning: '#C2410C', emergency: '#B91C1C' },
}

export function buildStyle(theme: 'dark' | 'light', exaggeration: number, safe = false): StyleSpecification {
  const d = theme === 'dark'
  const T = d
    ? { bg: '#0D0A09', land: '#17110F', line: '#3A2C26', text3: '#8A7A6F', brand: '#FF8A3D', glow: '#FFB37A', river: '#3F6E86', gold: '#FFC145', teal: '#2EC4B6' }
    : { bg: '#E9E2DA', land: '#F7F2EC', line: '#C9BBAF', text3: '#7A6B60', brand: '#C2410C', glow: '#F59E6B', river: '#4E7F99', gold: '#A16207', teal: '#0F766E' }
  const S = SEV_COLORS[theme]
  const relief = d
    ? [-12000, 'rgba(0,0,0,0)', 0, 'rgba(0,0,0,0)', 1, '#1B1411', 300, '#22180F', 800, '#2E1E12', 1600, '#422813', 2800, '#5E3714', 4200, '#86501E', 5600, '#B0743A', 7000, '#D9A26A']
    : [-12000, 'rgba(0,0,0,0)', 0, 'rgba(0,0,0,0)', 1, '#F3ECE3', 300, '#EEE2D2', 800, '#E7D3BB', 1600, '#DDBF9C', 2800, '#CFA57A', 4200, '#BE8A5C', 5600, '#A9734A', 7000, '#8E5C3A']
  return {
    version: 8,
    projection: { type: 'globe' },
    sky: { 'sky-color': T.bg, 'horizon-color': d ? '#2A1C15' : '#EFE6DC', 'atmosphere-blend': ['interpolate', ['linear'], ['zoom'], 0, 0.6, 5, 0.2, 8, 0] },
    sources: {
      dem: { type: 'raster-dem', tiles: ['trn-dem://{z}/{x}/{y}'], tileSize: 256, encoding: 'terrarium', maxzoom: 12,
        attribution: 'Terrain: AWS Terrain Tiles (Mapzen/Tilezen sources incl. SRTM, ETOPO1)' },
      // separate source for 3D terrain (MapLibre renders relief/hillshade better when it is not shared with the terrain mesh)
      demTerrain: { type: 'raster-dem', tiles: ['trn-dem://{z}/{x}/{y}'], tileSize: 256, encoding: 'terrarium', maxzoom: 12 },
      land: { type: 'geojson', data: `${BASE}geo/land.json`, attribution: 'Natural Earth (public domain)' },
      mask: { type: 'geojson', data: `${BASE}geo/india_mask.json` },
      india: { type: 'geojson', data: `${BASE}geo/india_soi.json`, attribution: 'India boundary: Survey of India depiction via DataMeet (CC BY-SA 2.5 / ODbL)' },
      states: { type: 'geojson', data: `${BASE}geo/states.json`, attribution: 'States: DataMeet (CC BY 4.0)' },
      rivers: { type: 'geojson', data: `${BASE}geo/rivers.json` },
      cameras: EMPTY, alerts: EMPTY, missed: EMPTY, selection: EMPTY, perimeter: EMPTY, flame: EMPTY, wind: EMPTY, cone: EMPTY,
      loraLinks: EMPTY, loraRoutes: EMPTY, loraNodes: EMPTY, villages: EMPTY, towers: EMPTY, pulses: EMPTY, pin: EMPTY,
    },
    ...(safe ? {} : { terrain: { source: 'demTerrain', exaggeration } }),
    layers: [
      { id: 'bg', type: 'background', paint: { 'background-color': T.bg } },
      { id: 'land', type: 'fill', source: 'land', paint: { 'fill-color': T.land } },
      { id: 'relief', type: 'color-relief', source: 'dem', paint: { 'color-relief-color': ['interpolate', ['linear'], ['elevation'], ...relief] as never, 'color-relief-opacity': 0.92 } },
      { id: 'hillshade', type: 'hillshade', source: 'dem', paint: {
        'hillshade-shadow-color': d ? 'rgba(0,0,0,0.75)' : 'rgba(60,40,25,0.45)', 'hillshade-highlight-color': d ? 'rgba(255,179,122,0.22)' : 'rgba(255,255,255,0.5)',
        'hillshade-accent-color': d ? 'rgba(217,72,15,0.18)' : 'rgba(194,65,12,0.12)', 'hillshade-exaggeration': 0.55, 'hillshade-illumination-direction': 315 } },
      { id: 'mask', type: 'fill', source: 'mask', paint: { 'fill-color': T.bg, 'fill-opacity': d ? 0.72 : 0.6 } },
      { id: 'rivers', type: 'line', source: 'rivers', paint: { 'line-color': T.river, 'line-opacity': 0.7, 'line-width': ['interpolate', ['linear'], ['zoom'], 3, 0.5, 8, 1.6] } },
      { id: 'states', type: 'line', source: 'states', paint: { 'line-color': T.line, 'line-width': ['interpolate', ['linear'], ['zoom'], 3, 0.5, 8, 1.2], 'line-opacity': 0.9 } },
      { id: 'india-glow', type: 'line', source: 'india', paint: { 'line-color': T.glow, 'line-width': 7, 'line-blur': 6, 'line-opacity': d ? 0.28 : 0.2 } },
      { id: 'india-line', type: 'line', source: 'india', paint: { 'line-color': T.brand, 'line-width': ['interpolate', ['linear'], ['zoom'], 2, 0.8, 6, 1.6] } },
      { id: 'towers', type: 'symbol', source: 'towers', layout: { 'icon-image': ['get', 'icon'], 'icon-allow-overlap': true, 'icon-size': 1 } },
      { id: 'lora-links', type: 'line', source: 'loraLinks', paint: { 'line-color': ['case', ['get', 'los'], T.teal, S.emergency], 'line-opacity': ['case', ['get', 'los'], 0.35, 0.55],
        'line-width': ['case', ['get', 'los'], 1, 1.2], 'line-dasharray': ['literal', [2, 2]] } },
      { id: 'lora-routes', type: 'line', source: 'loraRoutes', paint: { 'line-color': T.teal, 'line-width': 2.6, 'line-opacity': 0.9 } },
      { id: 'villages', type: 'symbol', source: 'villages', layout: { 'icon-image': ['get', 'icon'], 'icon-allow-overlap': true } },
      { id: 'lora-nodes', type: 'symbol', source: 'loraNodes', layout: { 'icon-image': ['get', 'icon'], 'icon-allow-overlap': true, 'icon-size': 1.1 } },
      { id: 'pulses', type: 'circle', source: 'pulses', paint: { 'circle-radius': 5, 'circle-color': T.teal, 'circle-stroke-color': T.bg, 'circle-stroke-width': 1.5 } },
      { id: 'cone', type: 'fill', source: 'cone', paint: { 'fill-color': T.gold, 'fill-opacity': 0.08 } },
      { id: 'cone-line', type: 'line', source: 'cone', paint: { 'line-color': T.gold, 'line-opacity': 0.5, 'line-width': 1, 'line-dasharray': ['literal', [3, 2]] } },
      { id: 'perimeter', type: 'fill', source: 'perimeter', paint: { 'fill-color': S.emergency, 'fill-opacity': 0.28 } },
      { id: 'perimeter-line', type: 'line', source: 'perimeter', paint: { 'line-color': S.emergency, 'line-width': 2, 'line-dasharray': ['literal', [2, 1.5]] } },
      { id: 'flame', type: 'fill-extrusion', source: 'flame', paint: { 'fill-extrusion-color': S.warning, 'fill-extrusion-height': ['get', 'h'], 'fill-extrusion-opacity': 0.85 } },
      { id: 'wind', type: 'symbol', source: 'wind', minzoom: 9, layout: { 'icon-image': 'wind', 'icon-rotate': ['get', 'rot'], 'icon-rotation-alignment': 'map', 'icon-allow-overlap': true, 'icon-size': 0.9 } },
      { id: 'cameras', type: 'symbol', source: 'cameras', minzoom: 5, layout: { 'icon-image': 'camera', 'icon-allow-overlap': true } },
      { id: 'missed', type: 'circle', source: 'missed', paint: { 'circle-radius': 16, 'circle-color': 'rgba(0,0,0,0)', 'circle-stroke-color': S.emergency, 'circle-stroke-width': 1.5, 'circle-stroke-opacity': 0.8 } },
      { id: 'alerts-ring', type: 'circle', source: 'alerts', paint: { 'circle-radius': ['+', 12, ['*', 34, ['get', 'u']]], 'circle-color': 'rgba(0,0,0,0)',
        'circle-stroke-color': ['get', 'color'], 'circle-stroke-width': 1, 'circle-stroke-opacity': 0.55, 'circle-pitch-alignment': 'map' } },
      { id: 'alerts-pulse', type: 'circle', source: 'alerts', filter: ['>=', ['get', 'level'], 2], paint: { 'circle-radius': 14, 'circle-color': ['get', 'color'], 'circle-opacity': 0.18, 'circle-blur': 0.6 } },
      { id: 'alerts', type: 'symbol', source: 'alerts', layout: { 'icon-image': ['get', 'icon'], 'icon-allow-overlap': true, 'icon-size': ['interpolate', ['linear'], ['get', 'level'], 1, 0.75, 3, 1.05],
        'symbol-sort-key': ['get', 'level'] } },
      { id: 'selection', type: 'circle', source: 'selection', paint: { 'circle-radius': 20, 'circle-color': 'rgba(0,0,0,0)', 'circle-stroke-color': T.gold, 'circle-stroke-width': 2.5 } },
      { id: 'pin', type: 'circle', source: 'pin', paint: { 'circle-radius': 6, 'circle-color': T.gold, 'circle-stroke-color': T.bg, 'circle-stroke-width': 2 } },
    ],
  } as StyleSpecification
}
