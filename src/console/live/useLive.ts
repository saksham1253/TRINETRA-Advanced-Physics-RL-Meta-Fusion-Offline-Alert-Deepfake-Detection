// LIVE and REPLAY data path. LIVE: Server-Sent Events from the inference gateway (tools/mock_gateway.py or the real model).
// REPLAY: a recorded gateway session (public/replay/session_demo.jsonl). If the live stream drops, the console shows a banner
// and switches to REPLAY of the last buffered LIVE events; it never switches to simulated data silently.
import { create } from 'zustand'
import { validateLiveEvent, type LiveEvent } from '../contracts/liveEvent'
import { useStore } from '../store'

interface L {
  latest: Record<string, LiveEvent>; log: LiveEvent[]; invalid: number; lastError: string | null; replayIdx: number
  params: { adjustable: Record<string, number | string>; requires_retraining: string[] } | null
}
export const useLive = create<L>(() => ({ latest: {}, log: [], invalid: 0, lastError: null, replayIdx: 0, params: null }))

let es: EventSource | null = null
let replayTimer: number | null = null
let replayData: LiveEvent[] | null = null

function ingest(e: LiveEvent) {
  const s = useLive.getState()
  useLive.setState({ latest: { ...s.latest, [e.source_id]: e }, log: [...s.log.slice(-599), e] })
}

export async function testConnection(url: string) {
  try {
    const r = await fetch(`${url.replace(/\/$/, '')}/health`)
    const h = await r.json()
    const p = await (await fetch(`${url.replace(/\/$/, '')}/params`)).json()
    useLive.setState({ params: p })
    return { ok: true, model: h.model }
  } catch (err) {
    return { ok: false, error: String(err) }
  }
}
export async function pushParams(url: string, values: Record<string, number | string>) {
  const r = await fetch(`${url.replace(/\/$/, '')}/params`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(values) })
  const j = await r.json()
  for (const e of j.recomputed ?? []) if (!validateLiveEvent(e).length) ingest(e)
  return j
}

export function connectLive(url: string) {
  disconnectLive()
  stopReplay()
  useStore.setState({ liveStatus: 'connecting' })
  es = new EventSource(`${url.replace(/\/$/, '')}/stream`)
  es.onopen = () => useStore.setState({ liveStatus: 'connected', mode: 'LIVE' })
  es.onmessage = (m) => {
    try {
      const e = JSON.parse(m.data)
      const errs = validateLiveEvent(e)
      if (errs.length) { useLive.setState({ invalid: useLive.getState().invalid + 1, lastError: errs.join('; ') }); return }
      ingest(e)
    } catch (err) { useLive.setState({ invalid: useLive.getState().invalid + 1, lastError: String(err) }) }
  }
  es.onerror = () => {
    if (useStore.getState().liveStatus === 'connected' || useStore.getState().liveStatus === 'connecting') {
      useStore.setState({ liveStatus: 'dropped' })
      disconnectLive()
      const buf = useLive.getState().log
      if (buf.length) startReplay(buf.map((e) => ({ ...e, mode: 'REPLAY' as const })))
      else useStore.setState({ mode: 'REPLAY' })
    }
  }
}
export function disconnectLive() { es?.close(); es = null }

export function stopReplay() { if (replayTimer) clearInterval(replayTimer); replayTimer = null }
export async function startReplay(data?: LiveEvent[]) {
  stopReplay()
  if (!data) {
    if (!replayData) {
      const txt = await (await fetch(`${import.meta.env.BASE_URL}replay/session_demo.jsonl`)).text()
      replayData = txt.split('\n').filter(Boolean).map((l) => JSON.parse(l))
    }
    data = replayData
  }
  const d = data
  useLive.setState({ latest: {}, log: [], replayIdx: 0 })
  useStore.setState({ mode: 'REPLAY' })
  const sources = new Set(d.map((e) => e.source_id)).size || 1
  let i = 0
  replayTimer = window.setInterval(() => {
    for (let k = 0; k < sources && d.length; k++) { const e = d[i % d.length]; if (!validateLiveEvent(e).length) ingest(e); i++ }
    useLive.setState({ replayIdx: i })
  }, 1000)
}
