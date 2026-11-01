import { useMemo, useState } from 'react'
import { useStore } from '../store'
import { allNow, fmtMin, networkDown, type SiteNow } from '../derived'
import { currentScenario } from '../useEngine'
import { Chip, OriginChip, Section, SevBadge, Stat, cx } from '../ui/primitives'
import { useT, LEVEL_KEY } from '../i18n'
import regions from '../data/regions.json'

const regionName = (id: string | null) => regions.regions.find((r) => r.id === id)?.name.split(',')[0] ?? 'Outside demo regions'

export function useAlertsNow() {
  const result = useStore((s) => s.result)
  const simMin = useStore((s) => s.simMin)
  return useMemo(() => allNow(result, simMin), [result, simMin])
}

function AlertCard({ n }: { n: SiteNow }) {
  const t = useT()
  const st = useStore()
  const life = st.lifecycle[n.site.id] ?? 'New'
  const hazard = n.site.hazard === 'LANDSLIDE' ? 'Landslide' : 'Fire or smoke'
  return (
    <li>
      <button onClick={() => st.set({ selected: n.site.id, rightTab: 'evidence' })} onDoubleClick={() => st.set({ diveSite: n.site.id, selected: n.site.id, rightTab: 'evidence' })}
        className={cx('w-full border-b border-trn-line px-4 py-2.5 text-left transition-colors duration-150 hover:bg-trn-raised', st.selected === n.site.id && 'bg-trn-raised')}>
        <div className="flex items-center gap-1.5">
          <SevBadge level={n.level} label={t(LEVEL_KEY[n.level])} hollow={st.showTruth && st.mode === 'SIM' && n.falseAlarm} />
          <span className="truncate text-[13px] font-medium text-trn-text">{hazard} · {n.site.id}</span>
          <span className="num ml-auto shrink-0 font-trn-mono text-[11px] text-trn-text3">{n.firstAlertMin !== null ? `since ${fmtMin(n.firstAlertMin)}` : ''}</span>
        </div>
        <div className="mt-1 flex items-center gap-1.5 text-[12px] text-trn-text2">
          <span className="truncate">{regionName(n.site.regionId)}</span>
          <span className="num ml-auto shrink-0">p {n.p.toFixed(2)} · U* {n.u.toFixed(2)}</span>
        </div>
        <div className="mt-1 flex flex-wrap items-center gap-1">
          <OriginChip origin={st.mode === 'SIM' ? 'SIMULATED' : st.mode === 'REPLAY' ? 'REPLAYED' : 'LIVE'} />
          <Chip tone="muted">{life}</Chip>
          {n.uncertain && <Chip tone="c" title="Conflict-aware uncertainty above the abstain threshold: human review required">Abstain: review</Chip>}
          {n.shield && <Chip tone="a" title="The physics or IoT shield raised the level (it can only raise)">Shield raised</Chip>}
          {st.showTruth && st.mode === 'SIM' && (n.falseAlarm ? <Chip tone="muted">False alarm (sim truth)</Chip> : n.active ? <Chip tone="b">True event (sim truth)</Chip> : null)}
        </div>
      </button>
    </li>
  )
}

export default function AlertsPanel() {
  const now = useAlertsNow()
  const [min, setMin] = useState(1)
  const [sort, setSort] = useState<'severity' | 'time'>('severity')
  const list = now.filter((n) => n.level >= min).sort((a, b) => sort === 'severity' ? b.level - a.level || b.p - a.p : (a.firstAlertMin ?? 0) - (b.firstAlertMin ?? 0))
  const shown = list.slice(0, 80)
  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <div className="flex items-center gap-1.5 border-b border-trn-line px-4 py-2">
        {[1, 2, 3].map((l) => (
          <button key={l} onClick={() => setMin(l)} className={cx('h-7 whitespace-nowrap rounded border px-1.5 text-[12px]', min === l ? 'border-trn-gold text-trn-text' : 'border-trn-line text-trn-text3')}>
            {['', 'Watch+', 'Warn+', 'Emerg.'][l]} <span className="num">{now.filter((n) => n.level >= l).length}</span>
          </button>
        ))}
        <select value={sort} onChange={(e) => setSort(e.target.value as typeof sort)} aria-label="Sort" className="ml-auto h-7 rounded border border-trn-line bg-trn-raised px-1.5 text-[12px] text-trn-text2">
          <option value="severity">By severity</option><option value="time">By time</option>
        </select>
      </div>
      <ul className="min-h-0 flex-1 overflow-y-auto">
        {shown.map((n) => <AlertCard key={n.site.id} n={n} />)}
        {!list.length && <li className="px-4 py-6 text-[13px] text-trn-text3">No alert at this level at the current simulation time.</li>}
        {list.length > shown.length && <li className="px-4 py-2 text-[12px] text-trn-text3">{list.length - shown.length} more not listed. Raise the level filter.</li>}
      </ul>
    </div>
  )
}

export function SitrepPanel() {
  const now = useAlertsNow()
  const st = useStore()
  const sc = currentScenario()
  const down = networkDown(sc, st.simMin, st.outage)
  const counts = [1, 2, 3].map((l) => now.filter((n) => n.level === l).length)
  const byRegion = new Map<string, number[]>()
  for (const n of now) if (n.level) { const k = regionName(n.site.regionId); const a = byRegion.get(k) ?? [0, 0, 0]; a[n.level - 1]++; byRegion.set(k, a) }
  const urgent = now.filter((n) => n.level >= 1).sort((a, b) => b.level - a.level || b.p - a.p).slice(0, 3)
  return (
    <div className="min-h-0 flex-1 overflow-y-auto">
      <Section title={`Situation at ${fmtMin(st.simMin)} (scenario time)`}>
        <div className="grid grid-cols-3 gap-2">
          <Stat label="Emergency" value={counts[2]} tone="emergency" /><Stat label="Warning" value={counts[1]} tone="warning" /><Stat label="Watch" value={counts[0]} />
        </div>
        <div className="mt-2 text-[12px] text-trn-text2">Networks: internet and cellular {down ? 'down, LoRa mesh carrying alerts' : 'up'}.</div>
      </Section>
      <Section title="Most urgent">
        <ol className="space-y-1 text-[13px]">
          {urgent.map((n) => (
            <li key={n.site.id}><button className="flex w-full items-center gap-1.5 text-left hover:text-trn-text" onClick={() => st.set({ selected: n.site.id, rightTab: 'evidence' })}>
              <SevBadge level={n.level} label={['', 'Watch', 'Warning', 'Emergency'][n.level]} /><span className="truncate text-trn-text2">{n.site.id} · {regionName(n.site.regionId)}</span>
              <span className="num ml-auto text-trn-text3">{n.p.toFixed(2)}</span></button></li>
          ))}
          {!urgent.length && <li className="text-trn-text3">None.</li>}
        </ol>
      </Section>
      <Section title="By region">
        <table className="w-full text-[12px]">
          <thead><tr className="text-trn-text3"><th className="text-left font-medium">Region</th><th className="text-right font-medium">Emer.</th><th className="text-right font-medium">Warn.</th><th className="text-right font-medium">Watch</th></tr></thead>
          <tbody className="num">{[...byRegion].map(([k, a]) => <tr key={k} className="text-trn-text2"><td className="truncate py-0.5">{k}</td><td className="text-right">{a[2]}</td><td className="text-right">{a[1]}</td><td className="text-right">{a[0]}</td></tr>)}</tbody>
        </table>
      </Section>
      <Section title="Audit trail (local, this session)">
        <ul className="space-y-1 text-[12px] text-trn-text2">
          {st.audit.slice(0, 30).map((a, i) => (
            <li key={i} className="flex gap-2"><span className="num shrink-0 font-trn-mono text-trn-text3">{fmtMin(a.simMin)}</span><span>{a.role} set {a.siteId} to {a.action}{a.reason ? ` (${a.reason})` : ''}</span></li>
          ))}
          {!st.audit.length && <li className="text-trn-text3">No operator action yet.</li>}
        </ul>
      </Section>
    </div>
  )
}
