import { useEffect, useMemo, useState } from 'react'
import { PanelLeftClose, PanelLeftOpen, PanelRightClose, PanelRightOpen, Undo2, Command } from 'lucide-react'
import './console.css'
import { useStore, SCENARIOS } from './store'
import { useEngine, useToast, currentScenario } from './useEngine'
import { useMeshCompute, useMesh } from './lora/useMesh'
import { useT } from './i18n'
import MapView, { mapRef, INDIA_VIEW } from './map/MapView'
import MapBoundary from './map/MapBoundary'
import TopBar from './panels/TopBar'
import ParamsPanel from './panels/ParamsPanel'
import ScenarioPanel, { selectScenario } from './panels/ScenarioPanel'
import LayersPanel from './panels/LayersPanel'
import AlertsPanel, { SitrepPanel } from './panels/AlertsPanel'
import EvidencePanel from './panels/EvidencePanel'
import LoraPanel from './panels/LoraPanel'
import { LiveAlerts, LiveEvidence } from './panels/LivePanels'
import { OutcomeStrip, StatusStrip, Timeline } from './panels/BottomBar'
import { AboutPanel, FormulaInspector, SettingsPanel } from './panels/Modals'
import { Button, IconButton, Kbd, Tabs, cx } from './ui/primitives'
import { networkDown } from './derived'
import { scenarioInputs } from './engine/simulate'
import { PARAMS } from './engine/params'

function Toast() {
  const { msg, at } = useToast()
  const [show, setShow] = useState(false)
  useEffect(() => {
    if (!msg) return
    setShow(true)
    const id = setTimeout(() => setShow(false), 4200)
    return () => clearTimeout(id)
  }, [msg, at])
  if (!show || !msg) return null
  return (
    <div role="status" aria-live="polite" className="pointer-events-auto flex max-w-[640px] items-center gap-3 rounded border border-trn-gold/60 bg-trn-surface px-4 py-2.5 text-[13px] text-trn-text shadow-[0_8px_24px_rgba(0,0,0,.45)]">
      <span className="text-[11px] font-semibold text-trn-gold">Change impact</span>
      <span>{msg}</span>
      <button className="ml-2 inline-flex items-center gap-1 text-[12px] text-trn-text3 hover:text-trn-text" onClick={() => useStore.getState().undo()}><Undo2 size={12} />Undo</button>
    </div>
  )
}

function Palette() {
  const st = useStore()
  const [q, setQ] = useState('')
  const cmds = useMemo(() => [
    ...SCENARIOS.map((s) => ({ label: `Scenario: ${s.title}`, run: () => selectScenario(s.id) })),
    { label: 'Simulate internet and cellular outage', run: () => { st.set({ outage: true, rightTab: 'lora', layers: { ...st.layers, lora: true } }); useMesh.setState({ outageAt: performance.now() }) } },
    { label: 'Restore networks', run: () => st.set({ outage: false }) },
    { label: 'Return to India view', run: () => { st.set({ diveSite: null }); mapRef.current?.flyTo({ ...INDIA_VIEW, duration: 2200 }) } },
    { label: 'Reset all parameters to repo defaults', run: () => st.setParams({ ...Object.fromEntries(PARAMS.map((p) => [p.id, p.default])), ...scenarioInputs(currentScenario()) }) },
    { label: 'Toggle theme', run: () => st.set({ theme: st.theme === 'dark' ? 'light' : 'dark' }) },
    { label: 'Toggle briefing mode', run: () => st.set({ briefing: !st.briefing }) },
    { label: 'Open situation report', run: () => st.set({ rightTab: 'sitrep', rightOpen: true }) },
    { label: 'Print situation brief', run: () => window.print() },
    { label: 'Open settings and live model', run: () => st.set({ settings: true }) },
    { label: 'About, methods and data sources', run: () => st.set({ about: true }) },
    ...PARAMS.filter((p) => p.kind !== 'enum').map((p) => ({ label: `Formula: ${p.label}`, run: () => st.set({ inspector: p.id }) })),
  ], [st])
  if (!st.palette) return null
  const hits = cmds.filter((c) => c.label.toLowerCase().includes(q.toLowerCase())).slice(0, 12)
  const close = () => { st.set({ palette: false }); setQ('') }
  return (
    <div className="fixed inset-0 z-[70] flex items-start justify-center bg-black/50 pt-[12vh]" onMouseDown={(e) => e.target === e.currentTarget && close()}>
      <div className="w-[560px] overflow-hidden rounded-lg border border-trn-line bg-trn-surface shadow-[0_8px_24px_rgba(0,0,0,.45)]" role="dialog" aria-label="Command palette">
        <input autoFocus value={q} onChange={(e) => setQ(e.target.value)} placeholder="Type a command" aria-label="Command"
          onKeyDown={(e) => { if (e.key === 'Enter' && hits[0]) { hits[0].run(); close() } if (e.key === 'Escape') close() }}
          className="h-11 w-full border-b border-trn-line bg-transparent px-4 text-[14px] text-trn-text placeholder:text-trn-text3 focus:outline-none" />
        <ul className="max-h-[50vh] overflow-y-auto py-1">
          {hits.map((c, i) => <li key={i}><button onClick={() => { c.run(); close() }} className="w-full px-4 py-2 text-left text-[13px] text-trn-text2 hover:bg-trn-raised hover:text-trn-text">{c.label}</button></li>)}
        </ul>
      </div>
    </div>
  )
}

export default function ConsoleApp() {
  const t = useT()
  const st = useStore()
  useEngine()
  const sc = currentScenario()
  const loraOn = st.layers.lora && (sc.regionId === 'uk-chamoli' || st.rightTab === 'lora' || st.outage)
  useMeshCompute(loraOn)

  // first load: scenario inputs + URL state (?s=scenario&t=minutes)
  useEffect(() => {
    const q = new URLSearchParams(location.hash.split('?')[1] ?? '')
    const sid = q.get('s')
    const s = useStore.getState()
    const sc0 = SCENARIOS.find((x) => x.id === (sid ?? s.scenarioId)) ?? SCENARIOS[0]
    useStore.setState({ scenarioId: sc0.id, params: { ...s.params, ...scenarioInputs(sc0) }, simMin: q.get('t') ? Number(q.get('t')) : s.simMin })
  }, [])
  // playback loop: speed x means x simulated seconds per real second
  useEffect(() => {
    if (!st.playing) return
    let last = performance.now()
    let raf = 0
    const loop = (now: number) => {
      const s = useStore.getState()
      const dur = currentScenario().durationMin
      const next = s.simMin + ((now - last) / 1000) * (s.speed / 60)
      last = now
      if (next >= dur) useStore.setState({ simMin: dur, playing: false })
      else { useStore.setState({ simMin: next }); raf = requestAnimationFrame(loop) }
    }
    raf = requestAnimationFrame(loop)
    return () => cancelAnimationFrame(raf)
  }, [st.playing])
  // scheduled scenario outage starts the LoRa pulse animation when the timeline crosses it
  const down = networkDown(sc, st.simMin, st.outage)
  useEffect(() => { useMesh.setState({ outageAt: down ? performance.now() : null }) }, [down])
  // keyboard shortcuts
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement)?.tagName
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); useStore.setState({ palette: true }); return }
      if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return
      const s = useStore.getState()
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') { e.preventDefault(); if (e.shiftKey) s.redo(); else s.undo() }
      else if (e.key === ' ') { e.preventDefault(); s.set({ playing: !s.playing }) }
      else if (e.key === 'Escape') s.set({ inspector: null, about: false, settings: false, palette: false, igniteArmed: false })
      else if (e.key === 'r' && s.briefing) selectScenario(s.scenarioId)
      else if (e.key === 'h') { s.set({ diveSite: null }); mapRef.current?.flyTo({ ...INDIA_VIEW, duration: 2200 }) }
      else if (e.key === '[') s.set({ leftOpen: !s.leftOpen })
      else if (e.key === ']') s.set({ rightOpen: !s.rightOpen })
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])
  // going offline turns online terrain fill off; going online never turns it on by itself (offline-first)
  useEffect(() => {
    const off = () => useStore.setState({ online: false })
    window.addEventListener('offline', off)
    return () => window.removeEventListener('offline', off)
  }, [])

  const live = st.mode !== 'SIM'
  const r = st.result
  const nAlerts = r ? r.sites.filter((s) => r.level[s.idx * r.nSteps + Math.min(r.nSteps - 1, Math.floor(st.simMin / r.stepMin))] >= 1).length : 0
  return (
    <div className="trn fixed inset-0 flex flex-col bg-trn-bg text-trn-text" data-theme={st.theme} data-briefing={st.briefing} data-motion={st.reduceMotion ? 'reduce' : 'full'}>
      <TopBar />
      <div className="relative flex min-h-0 flex-1">
        {st.leftOpen && !st.briefing && (
          <aside className="no-print flex w-[320px] shrink-0 flex-col border-r border-trn-line bg-trn-surface max-[1500px]:w-[288px]" aria-label="Controls">
            <Tabs value={st.leftTab} onChange={(v) => st.set({ leftTab: v })} items={[{ id: 'scenario', label: t('scenario') }, { id: 'params', label: 'Physics lab' }, { id: 'layers', label: t('layers') }]} />
            {st.leftTab === 'scenario' && <ScenarioPanel />}
            {st.leftTab === 'params' && <ParamsPanel />}
            {st.leftTab === 'layers' && <LayersPanel />}
          </aside>
        )}
        <main className="relative min-w-0 flex-1" aria-label="Map">
          <MapBoundary><MapView /></MapBoundary>
          <div className="pointer-events-none absolute inset-x-3 top-3 z-10 flex items-start justify-between gap-3">
            <div className="pointer-events-auto flex items-center gap-1.5">
              {!st.briefing && (
                <IconButton label={st.leftOpen ? 'Hide controls ([)' : 'Show controls ([)'} onClick={() => st.set({ leftOpen: !st.leftOpen })} className="border border-trn-line bg-trn-scrim">
                  {st.leftOpen ? <PanelLeftClose size={16} /> : <PanelLeftOpen size={16} />}
                </IconButton>
              )}
              {st.diveSite && (
                <div className="flex items-center gap-2 rounded border border-trn-line bg-trn-scrim px-3 py-1.5 text-[12.5px] text-trn-text2">
                  <span>India › {r?.sites.find((s) => s.id === st.diveSite)?.regionId ?? 'region'} › {st.diveSite}</span>
                  <Button className="h-7" onClick={() => { st.set({ diveSite: null }); mapRef.current?.flyTo({ ...INDIA_VIEW, duration: 2600 }) }}>{t('returnIndia')}</Button>
                </div>
              )}
              {st.igniteArmed && <div className="rounded border border-trn-gold/70 bg-trn-scrim px-3 py-1.5 text-[12.5px] text-trn-gold">Click the map to place a synthetic fire (Esc to cancel)</div>}
            </div>
            <Toast />
            <div className="pointer-events-auto mr-12 flex items-center gap-1.5">
              <button onClick={() => st.set({ palette: true })} className="hidden items-center gap-1.5 rounded border border-trn-line bg-trn-scrim px-2 py-1 text-[12px] text-trn-text3 hover:text-trn-text min-[1400px]:flex">
                <Command size={12} />Commands <Kbd>Ctrl K</Kbd>
              </button>
            </div>
          </div>
          {!live && <div className="pointer-events-none absolute inset-x-3 bottom-3 z-10 flex justify-center"><OutcomeStrip /></div>}
          {live && st.liveStatus === 'dropped' && (
            <div className="absolute inset-x-0 top-14 z-10 mx-auto w-fit rounded border border-trn-emergency/60 bg-trn-surface px-4 py-2 text-[13px] text-trn-emergency">Live gateway disconnected. Showing replay of the last received live events.</div>
          )}
        </main>
        {st.rightOpen && (
          <aside className="no-print flex w-[380px] shrink-0 flex-col border-l border-trn-line bg-trn-surface max-[1500px]:w-[336px]" aria-label="Alerts and evidence">
            <div className="flex items-center">
              <div className="flex-1">
                <Tabs value={st.rightTab} onChange={(v) => st.set({ rightTab: v })} items={[
                  { id: 'alerts', label: t('alerts'), badge: !live ? <span className={cx('num rounded px-1 text-[11px]', nAlerts ? 'bg-trn-warning/20 text-trn-warning' : 'text-trn-text3')}>{nAlerts}</span> : undefined },
                  { id: 'evidence', label: t('evidence') }, { id: 'lora', label: 'LoRa' }, { id: 'sitrep', label: t('sitrep') }]} />
              </div>
              <IconButton label="Hide panel (])" onClick={() => st.set({ rightOpen: false })} className="mx-1"><PanelRightClose size={16} /></IconButton>
            </div>
            {st.rightTab === 'alerts' && (live ? <LiveAlerts /> : <AlertsPanel />)}
            {st.rightTab === 'evidence' && (live ? <LiveEvidence /> : <EvidencePanel />)}
            {st.rightTab === 'lora' && <LoraPanel />}
            {st.rightTab === 'sitrep' && <SitrepPanel />}
          </aside>
        )}
        {!st.rightOpen && (
          <IconButton label="Show panel (])" onClick={() => st.set({ rightOpen: true })} className="absolute top-16 right-3 z-10 border border-trn-line bg-trn-scrim"><PanelRightOpen size={16} /></IconButton>
        )}
      </div>
      {!live && <Timeline />}
      <StatusStrip />
      <FormulaInspector />
      <AboutPanel />
      <SettingsPanel />
      <Palette />
    </div>
  )
}
