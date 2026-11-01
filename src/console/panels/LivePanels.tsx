import { useStore } from '../store'
import { useLive } from '../live/useLive'
import { Chip, OriginChip, Section, SevBadge, StatusChip, cx } from '../ui/primitives'
import { useT, LEVEL_KEY } from '../i18n'

const TIER = { GREEN: 0, YELLOW: 1, ORANGE: 2, RED: 3 } as const

export function LiveAlerts() {
  const t = useT()
  const latest = useLive((s) => s.latest)
  const st = useStore()
  const list = Object.values(latest).sort((a, b) => TIER[b.decision.tier] - TIER[a.decision.tier] || b.fusion.calibrated_probability - a.fusion.calibrated_probability)
  return (
    <ul className="min-h-0 flex-1 overflow-y-auto">
      {st.liveStatus === 'dropped' && <li className="border-b border-trn-emergency/50 bg-trn-emergency/10 px-4 py-2 text-[12.5px] text-trn-emergency">Live stream dropped. Showing a replay of the last received live events, not simulated data.</li>}
      {list.map((e) => {
        const l = TIER[e.decision.tier]
        return (
          <li key={e.source_id}><button onClick={() => st.set({ selected: e.source_id, rightTab: 'evidence' })}
            className={cx('w-full border-b border-trn-line px-4 py-2.5 text-left hover:bg-trn-raised', st.selected === e.source_id && 'bg-trn-raised')}>
            <div className="flex items-center gap-1.5"><SevBadge level={l} label={t(LEVEL_KEY[l])} /><span className="text-[13px] font-medium text-trn-text">{e.source_id}</span>
              <span className="num ml-auto font-trn-mono text-[11px] text-trn-text3">{e.timestamp_utc.slice(11, 19)} UTC</span></div>
            <div className="mt-1 flex flex-wrap items-center gap-1"><OriginChip origin={e.mode === 'LIVE' ? 'LIVE' : 'REPLAYED'} /><Chip tone="muted">{e.model.name} · {e.model.run_id}</Chip>
              <span className="num ml-auto text-[12px] text-trn-text2">p {e.fusion.calibrated_probability.toFixed(3)}</span></div>
          </button></li>
        )
      })}
      {!list.length && <li className="px-4 py-6 text-[13px] text-trn-text3">Waiting for events. Use Settings to connect a gateway or start the recorded replay.</li>}
    </ul>
  )
}

export function LiveEvidence() {
  const t = useT()
  const sel = useStore((s) => s.selected)
  const e = useLive((s) => (sel ? s.latest[sel] : undefined))
  if (!e) return <div className="px-4 py-6 text-[13px] text-trn-text3">Select a source.</div>
  const l = TIER[e.decision.tier]
  return (
    <div className="min-h-0 flex-1 overflow-y-auto">
      <Section title={<span className="flex items-center gap-2"><SevBadge level={l} label={t(LEVEL_KEY[l])} />{e.source_id}</span>} right={<OriginChip origin={e.mode === 'LIVE' ? 'LIVE' : 'REPLAYED'} />}>
        <dl className="grid grid-cols-[110px_1fr] gap-y-1 text-[12.5px]">
          <dt className="text-trn-text3">Model</dt><dd className="font-trn-mono text-[12px] text-trn-text2">{e.model.name} {e.model.version} · {e.model.run_id} · checkpoint {e.model.checkpoint_hash ?? 'not provided'}</dd>
          <dt className="text-trn-text3">Trained on</dt><dd className="text-trn-text2">{e.model.trained_on}</dd>
          <dt className="text-trn-text3">Location</dt><dd className="font-trn-mono text-[12px] text-trn-text2">{e.location.lat}, {e.location.lon} · {e.location.location_origin.toLowerCase()}</dd>
          <dt className="text-trn-text3">Fusion</dt><dd className="num text-trn-text2">{e.fusion.technique} · p {e.fusion.calibrated_probability.toFixed(4)} · U* {e.fusion.uncertainty.toFixed(2)} · p* {e.fusion.threshold}</dd>
          <dt className="text-trn-text3">Decision</dt><dd className="text-trn-text2">{e.decision.tier}{e.fusion.abstained ? ' · abstained: human review' : ''} · approval required</dd>
        </dl>
        <div className="mt-2"><Chip tone="b">not validated on held-out field data</Chip></div>
      </Section>
      <Section title="Modules">
        <ul className="space-y-1.5">{e.modules.map((m) => (
          <li key={m.id} className="rounded border border-trn-line px-3 py-2">
            <div className="flex items-center gap-1.5"><span className="flex-1 text-[13px] text-trn-text">{m.id}</span><StatusChip status={m.status} /></div>
            {m.score !== null && <div className="num mt-1 text-[12px] text-trn-text2">score {m.score.toFixed(3)} · u {m.uncertainty?.toFixed(2)}</div>}
          </li>))}</ul>
      </Section>
      <Section title="Note"><p className="text-[12.5px] text-trn-text3">{e.notes}</p></Section>
    </div>
  )
}
