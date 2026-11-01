import { create } from 'zustand'
import type { Technique } from './engine/fusion'
import { DEFAULT_VALUES, type ParamValues } from './engine/params'
import type { RunResult, Scenario, Incident } from './engine/simulate'

export type Mode = 'SIM' | 'REPLAY' | 'LIVE'
export type Lang = 'en' | 'hi' | 'hinglish'
export type Role = 'Operator' | 'Supervisor' | 'Analyst' | 'Viewer'
export type Lifecycle = 'New' | 'Acknowledged' | 'Under review' | 'Approved' | 'Dispatched (demo)' | 'Resolved' | 'Dismissed'
export type RightTab = 'alerts' | 'evidence' | 'lora' | 'sitrep'
export type LeftTab = 'scenario' | 'params' | 'layers'
export interface AuditEntry { at: string; simMin: number; siteId: string; action: string; role: Role; reason?: string }

interface S {
  mode: Mode; theme: 'dark' | 'light'; lang: Lang; role: Role; briefing: boolean; reduceMotion: boolean; showTruth: boolean
  scenarioId: string; customIncidents: Incident[]; params: ParamValues; baseline: ParamValues | null; technique: Technique
  history: ParamValues[]; future: ParamValues[]
  simMin: number; playing: boolean; speed: number
  result: RunResult | null; prevMetrics: RunResult['metrics'] | null; computing: boolean
  selected: string | null; diveSite: string | null; leftTab: LeftTab; rightTab: RightTab; leftOpen: boolean; rightOpen: boolean
  layers: Record<string, boolean>; exaggeration: number
  outage: boolean; disabledNodes: string[]; packetLoss: number; retransmissions: number
  lifecycle: Record<string, Lifecycle>; audit: AuditEntry[]
  inspector: string | null; palette: boolean; about: boolean; settings: boolean; igniteArmed: boolean
  online: boolean; gatewayUrl: string; liveStatus: 'disconnected' | 'connecting' | 'connected' | 'dropped'
  set: (p: Partial<S>) => void
  setParam: (id: string, v: number | string) => void
  setParams: (v: ParamValues, record?: boolean) => void
  undo: () => void; redo: () => void
  act: (siteId: string, action: Lifecycle, reason?: string) => void
}

export const useStore = create<S>((set, get) => ({
  mode: 'SIM', theme: 'dark', lang: 'en', role: 'Operator', briefing: false,
  reduceMotion: typeof location !== 'undefined' && /[?&]safe=1/.test(location.hash), showTruth: true,
  scenarioId: 's1-forest-wind', customIncidents: [], params: { ...DEFAULT_VALUES }, baseline: null, technique: 'FM-1',
  history: [], future: [],
  simMin: 120, playing: false, speed: 60,
  result: null, prevMetrics: null, computing: false,
  selected: null, diveSite: null, leftTab: 'params', rightTab: 'alerts', leftOpen: true, rightOpen: true,
  layers: { relief: true, states: true, rivers: true, cameras: true, alerts: true, lora: true, towers: true, wind: true, perimeter: true },
  exaggeration: 1.6,
  outage: false, disabledNodes: [], packetLoss: 0, retransmissions: 2,
  lifecycle: {}, audit: [],
  inspector: null, palette: false, about: false, settings: false, igniteArmed: false,
  online: false, gatewayUrl: 'http://localhost:8765', liveStatus: 'disconnected',
  set: (p) => set(p),
  setParam: (id, v) => {
    const { params, history } = get()
    set({ params: { ...params, [id]: v }, history: [...history.slice(-49), params], future: [] })
  },
  setParams: (v, record = true) => {
    const { params, history } = get()
    set(record ? { params: v, history: [...history.slice(-49), params], future: [] } : { params: v })
  },
  undo: () => {
    const { history, params, future } = get()
    if (!history.length) return
    set({ params: history[history.length - 1], history: history.slice(0, -1), future: [params, ...future] })
  },
  redo: () => {
    const { history, params, future } = get()
    if (!future.length) return
    set({ params: future[0], future: future.slice(1), history: [...history, params] })
  },
  act: (siteId, action, reason) => {
    const { lifecycle, audit, role, simMin } = get()
    set({ lifecycle: { ...lifecycle, [siteId]: action },
      audit: [{ at: new Date().toISOString(), simMin, siteId, action, role, reason }, ...audit].slice(0, 500) })
  },
}))

export const SCENARIOS = Object.values(import.meta.glob('./data/scenarios/*.json', { eager: true, import: 'default' })) as Scenario[]
SCENARIOS.sort((a, b) => a.id.localeCompare(b.id, undefined, { numeric: true }))
export const scenarioById = (id: string) => SCENARIOS.find((s) => s.id === id) ?? SCENARIOS[0]
