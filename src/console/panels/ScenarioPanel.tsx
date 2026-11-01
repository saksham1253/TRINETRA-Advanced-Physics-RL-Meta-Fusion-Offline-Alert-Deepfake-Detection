import { Flame, MapPin, Trash2, Eye } from 'lucide-react'
import { useStore, SCENARIOS } from '../store'
import { scenarioInputs } from '../engine/simulate'
import { Button, Chip, Section, Toggle, cx } from '../ui/primitives'
import { mapRef, INDIA_VIEW } from '../map/MapView'
import regions from '../data/regions.json'
import { currentScenario } from '../useEngine'
import { fmtMin } from '../derived'
import { BANK_INFO } from '../engine/simulate'

export function selectScenario(id: string) {
  const sc = SCENARIOS.find((s) => s.id === id)!
  const st = useStore.getState()
  const start = Math.min(...sc.incidents.map((i) => i.startMin), sc.durationMin / 2)
  st.set({ scenarioId: id, customIncidents: [], selected: null, diveSite: null, outage: false, disabledNodes: [],
    params: { ...st.params, ...scenarioInputs(sc) }, simMin: Math.min(sc.durationMin, Math.round((start + 30) / sc.stepMin) * sc.stepMin), playing: false })
  const r = regions.regions.find((x) => x.id === sc.regionId)
  const m = mapRef.current
  if (!m) return
  if (r) m.fitBounds([[r.bbox[0], r.bbox[1]], [r.bbox[2], r.bbox[3]]], { pitch: 50, bearing: -10, padding: 60, duration: 2400 })
  else m.flyTo({ ...INDIA_VIEW, duration: 2200 })
}

export default function ScenarioPanel() {
  const st = useStore()
  const sc = currentScenario()
  return (
    <div className="min-h-0 flex-1 overflow-y-auto">
      <Section title="Scenario library" right={<Chip tone="muted">synthetic, seeded</Chip>}>
        <ul className="space-y-1">
          {SCENARIOS.map((s, i) => (
            <li key={s.id}>
              <button onClick={() => selectScenario(s.id)} aria-current={st.scenarioId === s.id}
                className={cx('w-full rounded border px-2.5 py-2 text-left transition-colors duration-150', st.scenarioId === s.id ? 'border-trn-gold/70 bg-trn-raised' : 'border-transparent hover:bg-trn-raised')}>
                <div className="flex items-baseline gap-2">
                  <span className="num font-trn-mono text-[11px] text-trn-text3">{i + 1}</span>
                  <span className="text-[13px] font-medium text-trn-text">{s.title}</span>
                </div>
              </button>
            </li>
          ))}
        </ul>
      </Section>
      <Section title={sc.title}>
        <p className="text-[13px] leading-5 text-trn-text2">{sc.summary}</p>
        <dl className="mt-2 grid grid-cols-2 gap-x-3 gap-y-1 text-[12px]">
          <dt className="text-trn-text3">Scenario ID</dt><dd className="font-trn-mono text-trn-text2">{sc.id}</dd>
          <dt className="text-trn-text3">Seed</dt><dd className="num font-trn-mono text-trn-text2">{sc.seed}</dd>
          <dt className="text-trn-text3">Duration</dt><dd className="num text-trn-text2">{fmtMin(sc.durationMin)} h, step {sc.stepMin} min</dd>
          <dt className="text-trn-text3">Wind</dt><dd className="num text-trn-text2">{sc.weather.wind_ms} m/s from {sc.weather.wind_from_deg}°</dd>
          <dt className="text-trn-text3">Incidents</dt><dd className="num text-trn-text2">{sc.incidents.filter((i) => i.kind !== 'confuser').length} real, {sc.incidents.filter((i) => i.kind === 'confuser').length} confusers</dd>
          <dt className="text-trn-text3">Network outage</dt><dd className="num text-trn-text2">{sc.network.outageAtMin === null ? 'none' : `at ${fmtMin(sc.network.outageAtMin)}`}</dd>
        </dl>
        {sc.planned && <div className="mt-2 rounded border border-trn-line p-2 text-[12px] text-trn-text3"><b className="text-trn-text2">Planned, not simulated:</b> {sc.planned.join('; ')}.</div>}
        <p className="mt-2 text-[11px] leading-4 text-trn-text3">
          Same seed, same alerts. Every camera observation is one real out-of-fold image score from the trained models
          ({BANK_INFO.n} images, {BANK_INFO.nBlocks} blocks); positions, timing, IoT readings and weather are synthetic.
        </p>
      </Section>
      <Section title="Scenario director">
        <div className="grid grid-cols-2 gap-1.5">
          <Button variant={st.igniteArmed ? 'primary' : 'default'} onClick={() => st.set({ igniteArmed: !st.igniteArmed })}>
            <Flame size={14} />{st.igniteArmed ? 'Click the map' : 'Ignite here'}
          </Button>
          <Button disabled={!st.customIncidents.length} onClick={() => st.set({ customIncidents: [] })}><Trash2 size={14} />Clear placed</Button>
        </div>
        {st.customIncidents.length > 0 && (
          <ul className="mt-2 space-y-0.5 text-[12px] text-trn-text2">
            {st.customIncidents.map((c) => <li key={c.id} className="flex items-center gap-1.5"><MapPin size={12} />{c.label} · starts {fmtMin(c.startMin)}</li>)}
          </ul>
        )}
        <div className="mt-2">
          <Toggle label="Show ground truth (simulation only)" checked={st.showTruth} onChange={(v) => st.set({ showTruth: v })} />
          <Toggle label="Manual network outage" checked={st.outage} onChange={(v) => st.set({ outage: v })} />
        </div>
        <p className="mt-1 flex items-start gap-1.5 text-[11px] leading-4 text-trn-text3"><Eye size={12} className="mt-0.5 shrink-0" />Wind speed, intensity and spread rate are in the parameter lab (Fire physics and Fire spread groups).</p>
      </Section>
    </div>
  )
}
