// LoRa offline mesh on real terrain. Geometry = the repo's SYNTHETIC demo_valley (ws3_alert/last_mile.py) laid along the
// Alaknanda valley in Chamoli; gateway and ridge relays are snapped to the highest DEM cell within 1.2 km (synthetic placement).
// Every candidate hop is checked for terrain line of sight with 60 % first-Fresnel-zone clearance and 4/3-earth bulge
// (Class A radio propagation; ITU-R P.526 style clearance rule). Blocked hops are removed from the mesh (conservative:
// no diffraction gain is assumed). Packet loss and retransmissions are a SIMULATED layer on top of the repo planner.
import { elevation } from '../map/dem'
import { loraAirtimeS, plan, rxPowerDbm, type Conditions, type MeshNode, type PlanParams, type Radio, type Terrain, type Village, TERRAIN_N } from '../engine/lora'
import golden from '../engine/__tests__/golden.json'

export const ORIGIN = { lon: 79.315, lat: 30.398, bearingDeg: 52 } // GW-HQ near the district HQ; x axis up-valley (NE)
const ANT_H: Record<string, number> = { gateway: 15, relay: 12, siren: 6, village: 3 }
const F_MHZ = 866
const LAMBDA = 299.792458 / F_MHZ // m
const K_EARTH_R = (4 / 3) * 6371000

export function kmToLonLat(x: number, y: number): [number, number] {
  const b = (ORIGIN.bearingDeg * Math.PI) / 180
  const east = x * Math.sin(b) - y * Math.cos(b)
  const north = x * Math.cos(b) + y * Math.sin(b)
  return [ORIGIN.lon + (east * 1000) / (111320 * Math.cos((ORIGIN.lat * Math.PI) / 180)), ORIGIN.lat + (north * 1000) / 110540]
}
export function lonLatToKm(lon: number, lat: number): [number, number] {
  const east = ((lon - ORIGIN.lon) * 111320 * Math.cos((ORIGIN.lat * Math.PI) / 180)) / 1000
  const north = ((lat - ORIGIN.lat) * 110540) / 1000
  const b = (ORIGIN.bearingDeg * Math.PI) / 180
  return [east * Math.sin(b) + north * Math.cos(b), -east * Math.cos(b) + north * Math.sin(b)]
}

export interface Layout {
  villages: (Village & { lon: number; lat: number; elev: number })[]
  nodes: (MeshNode & { lon: number; lat: number; elev: number; snapped: boolean })[]
  towers: { id: string; lon: number; lat: number }[]
}

async function snapHigh(lon: number, lat: number, radiusM = 1200) {
  let best = { lon, lat, e: await elevation(lon, lat, 12) }
  for (let r = 300; r <= radiusM; r += 300)
    for (let k = 0; k < 12; k++) {
      const a = (k / 12) * 2 * Math.PI
      const p = { lon: lon + (r * Math.sin(a)) / (111320 * Math.cos((lat * Math.PI) / 180)), lat: lat + (r * Math.cos(a)) / 110540 }
      const e = await elevation(p.lon, p.lat, 12)
      if (e > best.e) best = { ...p, e }
    }
  return best
}

let layoutP: Promise<Layout> | null = null
export function getLayout(): Promise<Layout> {
  if (layoutP) return layoutP
  layoutP = (async () => {
    const V = golden.last_mile.villages as Village[]
    const N = golden.last_mile.nodes as MeshNode[]
    const villages = await Promise.all(V.map(async (v) => {
      const [lon, lat] = kmToLonLat(v.x_km, v.y_km)
      return { ...v, lon, lat, elev: await elevation(lon, lat, 12) }
    }))
    const nodes = await Promise.all(N.map(async (n) => {
      const [lon0, lat0] = kmToLonLat(n.x_km, n.y_km)
      if (n.kind === 'siren') return { ...n, lon: lon0, lat: lat0, elev: await elevation(lon0, lat0, 12), snapped: false }
      const s = await snapHigh(lon0, lat0)
      const [x, y] = lonLatToKm(s.lon, s.lat)
      return { ...n, x_km: x, y_km: y, lon: s.lon, lat: s.lat, elev: s.e, snapped: true }
    }))
    const towers = villages.filter((_, i) => i % 3 === 0).map((v, i) => {
      const [x, y] = lonLatToKm(v.lon, v.lat)
      const [lon, lat] = kmToLonLat(x + 0.6, y - 0.5)
      return { id: `TWR-${i + 1}`, lon, lat }
    })
    return { villages, nodes, towers }
  })()
  return layoutP
}

export interface LinkInfo { a: string; b: string; dKm: number; los: boolean; clearanceM: number; blockAtKm: number | null; terrain: Terrain; rxDbm: number }
const losCache = new Map<string, Promise<Omit<LinkInfo, 'terrain' | 'rxDbm'>>>()

/** Terrain line of sight with 60 % first-Fresnel clearance; returns the worst clearance along the path. */
export function lineOfSight(a: { id: string; lon: number; lat: number; elev: number; h: number }, b: { id: string; lon: number; lat: number; elev: number; h: number }) {
  const key = [a.id, b.id].sort().join('|') + `|${a.lon.toFixed(5)},${a.lat.toFixed(5)}|${b.lon.toFixed(5)},${b.lat.toFixed(5)}`
  let p = losCache.get(key)
  if (!p) {
    p = (async () => {
      const dx = (b.lon - a.lon) * 111320 * Math.cos((a.lat * Math.PI) / 180), dy = (b.lat - a.lat) * 110540
      const D = Math.hypot(dx, dy)
      const n = Math.max(16, Math.min(160, Math.round(D / 100)))
      const h0 = a.elev + a.h, h1 = b.elev + b.h
      let worst = Infinity, at: number | null = null
      for (let i = 1; i < n; i++) {
        const f = i / n, d1 = f * D, d2 = D - d1
        const g = await elevation(a.lon + f * (b.lon - a.lon), a.lat + f * (b.lat - a.lat), 12)
        const bulge = (d1 * d2) / (2 * K_EARTH_R)
        const r1 = Math.sqrt((LAMBDA * d1 * d2) / D)
        const clear = h0 + f * (h1 - h0) - (g + bulge) - 0.6 * r1
        if (clear < worst) { worst = clear; at = d1 / 1000 }
      }
      return { a: a.id, b: b.id, dKm: D / 1000, los: worst >= 0, clearanceM: worst, blockAtKm: worst >= 0 ? null : at }
    })()
    losCache.set(key, p)
  }
  return p
}

export interface MeshState {
  layout: Layout
  links: LinkInfo[]
  results: ReturnType<typeof plan>['results']
  hopS: number
  airtimeS: number
  dutyUsedPct: number
  blocked: number
  delivery: Record<string, number>
  reachedByDeadline: number
  popByDeadline: number
  popTotal: number
}

/** Full mesh plan on terrain for the given radio and planner parameters. */
export async function computeMesh(R: Radio, P: PlanParams, cond: Conditions, disabled: Set<string>, loss: number, retx: number, dutyPct: number): Promise<MeshState> {
  const layout = await getLayout()
  const pts = [
    ...layout.nodes.map((n) => ({ id: n.id, lon: n.lon, lat: n.lat, elev: n.elev, h: ANT_H[n.kind], terrain: (n.terrain ?? 'hill_forest') as Terrain, x: n.x_km, y: n.y_km })),
    ...layout.villages.filter((v) => v.has_pager).map((v) => ({ id: v.id, lon: v.lon, lat: v.lat, elev: v.elev, h: ANT_H.village, terrain: 'hill_forest' as Terrain, x: v.x_km, y: v.y_km })),
  ]
  const links: LinkInfo[] = []
  const losOk = new Map<string, boolean>()
  for (let i = 0; i < pts.length; i++)
    for (let j = i + 1; j < pts.length; j++) {
      const a = pts[i], b = pts[j]
      const d = Math.hypot(a.x - b.x, a.y - b.y)
      if (d > P.maxHopKm) continue
      const tclass: Terrain = TERRAIN_N[b.terrain] > TERRAIN_N[a.terrain] ? b.terrain : a.terrain
      const los = await lineOfSight(a, b)
      links.push({ ...los, terrain: tclass, rxDbm: rxPowerDbm(R, d * 1000, tclass) })
      losOk.set([a.id, b.id].sort().join('|'), los.los)
    }
  const linkOk = (u: string, v: string) => losOk.get([u, v].sort().join('|')) ?? true
  const out = plan(layout.villages, layout.nodes, cond, R, P, disabled, linkOk)
  const airtimeS = loraAirtimeS(P.payload, R.sf)
  const hopS = airtimeS * 2 + P.hopProcessingS
  // SIMULATED reliability: independent loss per transmission, up to `retx` retransmissions per hop
  const perHop = 1 - loss ** (retx + 1)
  const delivery: Record<string, number> = {}
  for (const r of out.results) {
    const hops = r.channel === 'LoRa pager' || r.channel.startsWith('siren') ? Math.max(0, r.path.length - 1) : 0
    delivery[r.id] = r.minutes === null ? 0 : r.channel.startsWith('runner') ? 1 : perHop ** hops
  }
  const expectedTx = loss < 1 ? (1 - loss ** (retx + 1)) / (1 - loss) : retx + 1
  // duty cycle is a PER-NODE limit: each relaying node transmits the alert once (plus retransmissions) per alert
  const dutyUsedPct = ((expectedTx * airtimeS) / 3600) * 100 // % of one hour, for one alert per hour
  void dutyPct
  const ok = out.results.filter((r) => r.minutes !== null && r.minutes <= P.deadlineMin)
  return {
    layout, links, results: out.results, hopS, airtimeS, dutyUsedPct, blocked: links.filter((l) => !l.los).length, delivery,
    reachedByDeadline: ok.length, popByDeadline: ok.reduce((s, r) => s + r.population, 0), popTotal: out.results.reduce((s, r) => s + r.population, 0),
  }
}
