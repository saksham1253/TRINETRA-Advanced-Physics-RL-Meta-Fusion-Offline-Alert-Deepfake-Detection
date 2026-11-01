// Web Worker: every slider change re-runs the real formula ports here (never on the UI thread).
import { buildSites, run, evalSiteStep, type Scenario, type Site, type Town } from '../engine/simulate'
import type { Technique } from '../engine/fusion'
import type { ParamValues } from '../engine/params'
import { num } from '../engine/params'

export type EngineRequest =
  | { type: 'run'; id: number; scenario: Scenario; towns: Town[]; params: ParamValues; technique: Technique }
  | { type: 'sweep'; id: number; scenario: Scenario; towns: Town[]; params: ParamValues; technique: Technique; paramId: string; values: number[] }
  | { type: 'detail'; id: number; scenario: Scenario; site: Site; step: number; params: ParamValues; technique: Technique }

let cache: { key: string; sites: Site[] } | null = null
const sitesFor = (sc: Scenario, towns: Town[]) => {
  const key = JSON.stringify([sc.id, sc.seed, sc.incidents.length, sc.incidents.map((i) => [i.lon, i.lat, i.startMin]), towns.length])
  if (!cache || cache.key !== key) cache = { key, sites: buildSites(sc, towns) }
  return cache.sites.map((s) => ({ ...s }))
}

self.onmessage = (ev: MessageEvent<EngineRequest>) => {
  const m = ev.data
  try {
    if (m.type === 'run') {
      const r = run(m.scenario, sitesFor(m.scenario, m.towns), m.params, m.technique)
      ;(self as unknown as Worker).postMessage({ type: 'run', id: m.id, result: r }, [r.p.buffer, r.level.buffer, r.u.buffer, r.flags.buffer])
    } else if (m.type === 'sweep') {
      const t0 = performance.now()
      const out = m.values.map((v) => {
        const r = run(m.scenario, sitesFor(m.scenario, m.towns), { ...m.params, [m.paramId]: v }, m.technique)
        return { v, watch: r.metrics.watch, warning: r.metrics.warning, auc: r.roc.auc, pStar: num(m.params, 'cost.C_FA') }
      })
      ;(self as unknown as Worker).postMessage({ type: 'sweep', id: m.id, out, ms: performance.now() - t0 })
    } else if (m.type === 'detail') {
      const d = evalSiteStep(m.scenario, m.site, m.step, m.params, m.technique)
      ;(self as unknown as Worker).postMessage({ type: 'detail', id: m.id, detail: d })
    }
  } catch (e) {
    ;(self as unknown as Worker).postMessage({ type: 'error', id: m.id, error: String(e) })
  }
}
