// Derived view state shared by the map and the panels (pure functions of the store + engine result).
import type { RunResult, Site, Scenario, Incident } from './engine/simulate'
import { offset } from './engine/simulate'
import { flameHeightHeskestad } from './engine/firephys'
import { num, type ParamValues } from './engine/params'

export const SEV_NAME = ['normal', 'watch', 'warning', 'emergency'] as const
export const stepOf = (r: RunResult, simMin: number) => Math.max(0, Math.min(r.nSteps - 1, Math.floor(simMin / r.stepMin)))

export interface SiteNow {
  site: Site; level: number; p: number; u: number; uncertain: boolean; active: boolean; shield: boolean; validated: boolean
  firstAlertMin: number | null; falseAlarm: boolean
}
export function siteNow(r: RunResult, s: Site, step: number): SiteNow {
  const i = s.idx * r.nSteps + step
  let first: number | null = null
  for (let k = step; k >= 0 && r.level[s.idx * r.nSteps + k] >= 1; k--) first = k * r.stepMin
  const active = (r.flags[i] & 2) !== 0
  const early = s.hazard === 'LANDSLIDE' && s.truthStart !== null && step * r.stepMin >= s.truthStart - 720
  return {
    site: s, level: r.level[i], p: r.p[i], u: r.u[i], uncertain: (r.flags[i] & 1) !== 0, active, shield: (r.flags[i] & 4) !== 0,
    validated: (r.flags[i] & 8) !== 0, firstAlertMin: first, falseAlarm: r.level[i] >= 1 && !active && !early,
  }
}
export function allNow(r: RunResult | null, simMin: number): SiteNow[] {
  if (!r) return []
  const st = stepOf(r, simMin)
  return r.sites.map((s) => siteNow(r, s, st))
}

export function networkDown(sc: Scenario, simMin: number, manualOutage: boolean) {
  return manualOutage || (sc.network.outageAtMin !== null && simMin >= sc.network.outageAtMin)
}

/** Anderson (1983) length-to-breadth ratio of a wind-driven fire ellipse; U in m/s (converted to mi/h). SURROGATE input. */
export const andersonLB = (U_ms: number) => {
  const U = U_ms * 2.23694
  return Math.max(1, 0.936 * Math.exp(0.2566 * U) + 0.461 * Math.exp(-0.1548 * U) - 0.397)
}

/** SURROGATE fire perimeter: Richards-type ellipse grown at the head rate of spread along the wind. Not a repo model. */
export function perimeter(inc: Incident, sc: Scenario, simMin: number, P: ParamValues) {
  if (inc.kind !== 'fire' || simMin <= inc.startMin) return null
  const primary = sc.incidents.find((i) => i.kind === 'fire' && i.ros_m_min)?.ros_m_min ?? 8
  const ros = (inc.ros_m_min ?? primary) * (num(P, 'sur.ros') / primary)
  const U = num(P, 'fire.wind_ms')
  const LB = num(P, 'sur.lb') ? Math.min(andersonLB(U), 8) : 1
  const head = ros * (simMin - inc.startMin)
  const back = LB > 1 ? (head * (LB - Math.sqrt(LB * LB - 1))) / (LB + Math.sqrt(LB * LB - 1)) : head
  const a = (head + back) / 2, b = a / LB
  const toDeg = (((sc.weather.wind_from_deg + 180) % 360) * Math.PI) / 180
  const cx = (head - a) * Math.sin(toDeg), cy = (head - a) * Math.cos(toDeg)
  const ring = (f: number) => {
    const pts: [number, number][] = []
    for (let k = 0; k <= 64; k++) {
      const th = (k / 64) * 2 * Math.PI
      const ex = a * f * Math.cos(th), ey = b * f * Math.sin(th) // ex along the heading
      const e = cx + ex * Math.sin(toDeg) + ey * Math.cos(toDeg)
      const n = cy + ex * Math.cos(toDeg) - ey * Math.sin(toDeg)
      pts.push(offset(inc.lon, inc.lat, e, n))
    }
    return pts
  }
  const pf = sc.incidents.find((i) => i.kind === 'fire')
  const Q = (inc.Q_kW ?? pf?.Q_kW ?? 2000) * (num(P, 'fire.Q_kW') / (pf?.Q_kW ?? 2000))
  const D = (inc.D_m ?? pf?.D_m ?? 3) * (num(P, 'fire.D_m') / (pf?.D_m ?? 3))
  const L = Math.max(0, flameHeightHeskestad(Q, D))
  return { outer: ring(1), inner: ring(0.9), headM: head, backM: back, LB, areaHa: (Math.PI * a * b) / 1e4, flameM: L, Q, D, ros }
}

export const fmtMin = (m: number) => {
  const h = Math.floor(m / 60), mm = Math.round(m % 60)
  return `${String(h).padStart(2, '0')}:${String(mm).padStart(2, '0')}`
}
