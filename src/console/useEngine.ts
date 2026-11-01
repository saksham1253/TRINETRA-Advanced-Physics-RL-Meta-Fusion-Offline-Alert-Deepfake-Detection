// Runs the scenario engine in a Web Worker whenever the scenario, parameters or technique change, and reports what changed.
import { useEffect, useRef } from 'react'
import { useStore, scenarioById } from './store'
import type { Scenario, Town, RunResult } from './engine/simulate'
import type { EngineRequest } from './workers/engine.worker'
import { create } from 'zustand'

let worker: Worker | null = null
let reqId = 0
const pending = new Map<number, (v: unknown) => void>()
export function getWorker() {
  if (!worker) {
    worker = new Worker(new URL('./workers/engine.worker.ts', import.meta.url), { type: 'module' })
    worker.onmessage = (ev) => {
      const r = pending.get(ev.data.id)
      if (r) { pending.delete(ev.data.id); r(ev.data) }
    }
  }
  return worker
}
type DistOmit<T, K extends PropertyKey> = T extends unknown ? Omit<T, K> : never
export function ask<T>(msg: DistOmit<EngineRequest, 'id'>): Promise<T> {
  const id = ++reqId
  return new Promise((res) => { pending.set(id, res as (v: unknown) => void); getWorker().postMessage({ ...msg, id }) })
}

export const useTowns = create<{ towns: Town[]; loaded: boolean }>(() => ({ towns: [], loaded: false }))
export function loadTowns() {
  if (useTowns.getState().loaded) return
  fetch(`${import.meta.env.BASE_URL}geo/gazetteer.json`).then((r) => r.json()).then((g) => useTowns.setState({ towns: g.rows, loaded: true }))
    .catch(() => useTowns.setState({ towns: [], loaded: true }))
}

export const useToast = create<{ msg: string | null; at: number }>(() => ({ msg: null, at: 0 }))
export function toast(msg: string) { useToast.setState({ msg, at: Date.now() }) }

export function currentScenario(): Scenario {
  const s = useStore.getState()
  const base = scenarioById(s.scenarioId)
  return s.customIncidents.length ? { ...base, incidents: [...base.incidents, ...s.customIncidents] } : base
}

function impact(prev: RunResult['metrics'] | null, next: RunResult['metrics']) {
  if (!prev) return null
  const a = prev.warning, b = next.warning, w0 = prev.watch, w1 = next.watch
  const parts: string[] = []
  const d = (x: number, y: number, label: string) => { if (y !== x) parts.push(`${y > x ? '+' : ''}${y - x} ${label}`) }
  d(w0.alertEpisodes, w1.alertEpisodes, 'watch-or-higher alerts')
  d(a.falseAlarmEpisodes, b.falseAlarmEpisodes, 'warning false alarms')
  d(a.missed, b.missed, 'missed incidents (warning)')
  if (a.medianTTA !== null && b.medianTTA !== null && a.medianTTA !== b.medianTTA)
    parts.push(`median time-to-warning ${Math.abs(b.medianTTA - a.medianTTA)} min ${b.medianTTA < a.medianTTA ? 'earlier' : 'later'}`)
  return parts.length ? parts.join(', ') : 'No change in alerts'
}

export function useEngine() {
  const scenarioId = useStore((s) => s.scenarioId)
  const params = useStore((s) => s.params)
  const technique = useStore((s) => s.technique)
  const custom = useStore((s) => s.customIncidents)
  const towns = useTowns((s) => s.towns)
  const loaded = useTowns((s) => s.loaded)
  const timer = useRef<number | null>(null)
  const last = useRef<string>('')
  useEffect(() => { loadTowns() }, [])
  useEffect(() => {
    if (!loaded) return
    if (timer.current) clearTimeout(timer.current)
    timer.current = window.setTimeout(async () => {
      const sc = currentScenario()
      useStore.setState({ computing: true })
      const key = sc.id + JSON.stringify(custom)
      const res = await ask<{ result: RunResult }>({ type: 'run', scenario: sc, towns, params, technique })
      const prev = useStore.getState().result
      const sameScenario = last.current === key
      last.current = key
      useStore.setState({ result: res.result, prevMetrics: prev?.metrics ?? null, computing: false })
      if (sameScenario && prev) { const m = impact(prev.metrics, res.result.metrics); if (m) toast(m) }
    }, 40)
  }, [scenarioId, params, technique, custom, towns, loaded])
}
