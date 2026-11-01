// Port of TRINETRA/trinetra/src/trinetra/ws3_alert/last_mile.py (offline last-mile planner). Class A radio formulas,
// path-loss exponents and siren attenuation are ASSUMPTIONS in the repo (site survey required).
export const SX1276_SENS_DBM: Record<number, number> = { 7: -123, 8: -126, 9: -129, 10: -132, 11: -134.5, 12: -137 }
export type Terrain = 'ridge_los' | 'hill_forest' | 'valley_nlos'
export const TERRAIN_N: Record<Terrain, number> = { ridge_los: 2.2, hill_forest: 3.0, valley_nlos: 3.6 }

export function loraAirtimeS(payload: number, sf = 10, bw = 125e3, cr = 1, preamble = 8, explicitHeader = true, crc = true) {
  const tSym = 2 ** sf / bw
  const de = sf >= 11 && bw <= 125e3 ? 1 : 0
  const ih = explicitHeader ? 0 : 1
  const num = 8 * payload - 4 * sf + 28 + 16 * (crc ? 1 : 0) - 20 * ih
  const nPayload = 8 + Math.max(Math.ceil(num / (4 * (sf - 2 * de))) * (cr + 4), 0)
  return (preamble + 4.25) * tSym + nPayload * tSym
}
export const fsplDb = (d_m: number, f = 866) => 20 * Math.log10(Math.max(d_m, 1e-3) / 1000) + 20 * Math.log10(f) + 32.44
export interface Radio { sf: number; tx: number; gTx: number; gRx: number; cable: number; fade: number; f: number; n: Record<Terrain, number> }
export const RADIO_DEFAULTS: Radio = { sf: 10, tx: 30, gTx: 2, gRx: 2, cable: 1, fade: 15, f: 866, n: { ...TERRAIN_N } }
export const linkBudgetDb = (R: Radio) => R.tx + R.gTx + R.gRx - R.cable - (SX1276_SENS_DBM[R.sf] + R.fade)
export function loraRangeKm(R: Radio, terrain: Terrain) {
  return 10 ** ((linkBudgetDb(R) - fsplDb(1, R.f)) / (10 * R.n[terrain])) / 1000
}
/** Received power at distance d under the log-distance model (for link colouring). */
export const rxPowerDbm = (R: Radio, d_m: number, terrain: Terrain) =>
  R.tx + R.gTx + R.gRx - R.cable - (fsplDb(1, R.f) + 10 * R.n[terrain] * Math.log10(Math.max(d_m, 1)))
export function sirenLevelDb(r: number, lRef = 120, rRef = 30, alpha = 0.01) {
  const rr = Math.max(r, rRef)
  return lRef - 20 * Math.log10(rr / rRef) - alpha * (rr - rRef)
}
export function sirenRadiusM(lRef = 120, rRef = 30, alpha = 0.01, contour = 70) {
  let lo = rRef, hi = 50000
  if (sirenLevelDb(lo, lRef, rRef, alpha) <= contour) return lo
  for (let i = 0; i < 80; i++) {
    const mid = (lo + hi) / 2
    if (sirenLevelDb(mid, lRef, rRef, alpha) > contour) lo = mid
    else hi = mid
  }
  return lo
}

export interface Village { id: string; x_km: number; y_km: number; population: number; has_pager?: boolean; has_satellite_rx?: boolean; cell_coverage?: boolean; fm_coverage?: boolean; lon?: number; lat?: number }
export interface MeshNode { id: string; x_km: number; y_km: number; kind: 'gateway' | 'relay' | 'siren'; terrain?: Terrain; battery_ok?: boolean; lon?: number; lat?: number }
export interface Conditions { internet: boolean; cell: boolean; grid_power: boolean; fm: boolean; satellite: boolean }
export interface PlanParams { payload: number; hopProcessingS: number; deadlineMin: number; runnerKmh: number; cellMin: number; fmMin: number; satMin: number; sirenContour: number; sirenAlpha: number; maxHopKm: number }
export const PLAN_DEFAULTS: PlanParams = { payload: 24, hopProcessingS: 0.5, deadlineMin: 10, runnerKmh: 2.5, cellMin: 1, fmMin: 3, satMin: 3, sirenContour: 70, sirenAlpha: 0.01, maxHopKm: 30 }
export const COND_OUTAGE: Conditions = { internet: false, cell: false, grid_power: false, fm: false, satellite: true }

type Pt = { id: string; x_km: number; y_km: number; isNode: boolean; kind?: string }
const dist = (a: { x_km: number; y_km: number }, b: { x_km: number; y_km: number }) => Math.hypot(a.x_km - b.x_km, a.y_km - b.y_km)

/** Optional extra test on every candidate hop, e.g. terrain line-of-sight. Returns false to block the link. */
export type LinkFilter = (a: string, b: string) => boolean

export function meshTimes(villages: Village[], nodes: MeshNode[], R: Radio, P: PlanParams, disabled: Set<string>, linkOk?: LinkFilter) {
  const hopS = loraAirtimeS(P.payload, R.sf) * 2 + P.hopProcessingS
  const pts = new Map<string, Pt>()
  for (const n of nodes) if (!disabled.has(n.id) && n.battery_ok !== false) pts.set(n.id, { ...n, isNode: true })
  for (const v of villages) if (v.has_pager && !disabled.has(v.id)) pts.set(v.id, { ...v, isNode: false })
  const terr = new Map(nodes.map((n) => [n.id, n.terrain ?? 'hill_forest'] as const))
  const rng: Record<string, number> = {}
  for (const t of Object.keys(TERRAIN_N) as Terrain[]) rng[t] = Math.min(loraRangeKm(R, t), P.maxHopKm)
  const best = new Map<string, { t: number; path: string[] }>()
  const done = new Set<string>()
  for (const n of nodes) if (n.kind === 'gateway' && pts.has(n.id)) best.set(n.id, { t: 0, path: [n.id] })
  const hops: { a: string; b: string; t: number }[] = []
  for (;;) {
    let u: string | null = null
    for (const [id, b] of best) if (!done.has(id) && (u === null || b.t < best.get(u)!.t || (b.t === best.get(u)!.t && id < u))) u = id
    if (u === null) break
    done.add(u)
    const pu = pts.get(u)!
    if (pu.isNode && pu.kind === 'siren') continue
    const t = best.get(u)!.t
    for (const [v, pv] of pts) {
      if (v === u) continue
      const tu = terr.get(u) ?? 'hill_forest', tv = terr.get(v) ?? 'hill_forest'
      const tclass = TERRAIN_N[tv] > TERRAIN_N[tu] ? tv : tu
      if (dist(pu, pv) <= rng[tclass] && (!linkOk || linkOk(u, v))) {
        const nt = t + hopS
        const cur = best.get(v)
        if (!cur || nt < cur.t) { best.set(v, { t: nt, path: [...best.get(u)!.path, v] }); hops.push({ a: u, b: v, t: nt }) }
      }
    }
  }
  return { best, hopS, rangeKm: rng }
}

export interface VillageResult { id: string; population: number; minutes: number | null; channel: string; path: string[]; channels: number }
export function plan(villages: Village[], nodes: MeshNode[], cond: Conditions, R: Radio = RADIO_DEFAULTS, P: PlanParams = PLAN_DEFAULTS, disabled = new Set<string>(), linkOk?: LinkFilter) {
  const mesh = meshTimes(villages, nodes, R, P, disabled, linkOk).best
  const rSirenKm = sirenRadiusM(120, 30, P.sirenAlpha, P.sirenContour) / 1000
  const out = new Map<string, VillageResult>()
  for (const v of villages) {
    const opts: [number, string, string[]][] = []
    const mv = mesh.get(v.id)
    if (v.has_pager && mv) opts.push([mv.t / 60, 'LoRa pager', mv.path])
    for (const n of nodes) {
      const mn = mesh.get(n.id)
      if (n.kind === 'siren' && mn && dist(n, v) <= rSirenKm) opts.push([mn.t / 60 + 0.1, `siren ${n.id}`, mn.path])
    }
    if (cond.cell && (v.cell_coverage ?? true)) opts.push([P.cellMin, 'cell broadcast', []])
    if (cond.fm && v.fm_coverage) opts.push([P.fmMin, 'FM / community radio', []])
    if (cond.satellite && v.has_satellite_rx) opts.push([P.satMin, 'satellite message', []])
    opts.sort((a, b) => a[0] - b[0])
    out.set(v.id, { id: v.id, population: v.population, minutes: opts[0]?.[0] ?? null, channel: opts[0]?.[1] ?? 'none', path: opts[0]?.[2] ?? [], channels: opts.length })
  }
  const sources = nodes.filter((n) => mesh.has(n.id) && n.kind !== 'siren').map((n) => [n, mesh.get(n.id)!.t / 60] as const)
  for (let it = 0; it < villages.length; it++) {
    let changed = false
    const warned = villages.filter((v) => out.get(v.id)!.minutes !== null).map((v) => [v, out.get(v.id)!.minutes as number] as const)
    for (const v of villages) {
      const cand: [number, string][] = []
      for (const [s, m] of warned) if (s.id !== v.id) cand.push([m + (dist(s, v) / P.runnerKmh) * 60, s.id])
      for (const [n, m] of sources) cand.push([m + (dist(n, v) / P.runnerKmh) * 60, n.id])
      if (!cand.length) continue
      cand.sort((a, b) => a[0] - b[0] || (a[1] < b[1] ? -1 : a[1] > b[1] ? 1 : 0))
      const [t, via] = cand[0]
      const r = out.get(v.id)!
      if (r.minutes === null || t < r.minutes - 1e-9) { r.minutes = t; r.channel = `runner from ${via}`; r.path = [via, v.id]; changed = true }
    }
    if (!changed) break
  }
  return { results: villages.map((v) => out.get(v.id)!), mesh }
}
