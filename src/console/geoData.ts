import type * as GeoJSON from 'geojson'
// Runtime loader for the offline vector pack in public/geo (files under public/ cannot be imported into the bundle).
let states: GeoJSON.FeatureCollection | null = null
fetch(`${import.meta.env.BASE_URL}geo/states.json`).then((r) => r.json()).then((j) => (states = j)).catch(() => undefined)

/** State name for a point (ray casting on the DataMeet state polygons). */
export function stateOf(lon: number, lat: number) {
  if (!states) return 'State lookup loading'
  const inside = (ring: number[][]) => {
    let c = false
    for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      const [xi, yi] = ring[i], [xj, yj] = ring[j]
      if (yi > lat !== yj > lat && lon < ((xj - xi) * (lat - yi)) / (yj - yi) + xi) c = !c
    }
    return c
  }
  for (const f of states.features) {
    const g = f.geometry as GeoJSON.Polygon | GeoJSON.MultiPolygon
    const polys = g.type === 'Polygon' ? [g.coordinates] : g.coordinates
    if (polys.some((p) => inside(p[0] as number[][]))) return String(f.properties?.name)
  }
  return 'Outside India boundary'
}
