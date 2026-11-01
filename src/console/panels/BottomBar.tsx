import { useState } from 'react'
import { Pause, Play, SkipBack } from 'lucide-react'
import { useStore } from '../store'
import { currentScenario } from '../useEngine'
import { fmtMin } from '../derived'
import { useCursor } from '../map/MapView'
import { Chip, IconButton, cx } from '../ui/primitives'
import { useT } from '../i18n'
import build from '../data/build.json'

const SPEEDS = [1, 10, 60, 300, 1200, 3600]

function Roc() {
  const roc = useStore((s) => s.result?.roc)
  if (!roc || !Number.isFinite(roc.auc)) return <div className="w-[96px] text-[11px] leading-4 text-trn-text3">ROC needs positive and negative steps</div>
  const W = 96, H = 56
  const pts = roc.fpr.map((f, i) => `${2 + f * (W - 4)},${H - 2 - roc.tpr[i] * (H - 4)}`).join(' ')
  return (
    <figure className="flex items-center gap-2" title="ROC over all camera steps of this simulated scenario; dot = current p* operating point">
      <svg width={W} height={H} role="img" aria-label={`ROC curve, AUC ${roc.auc.toFixed(3)}`}>
        <rect x={1} y={1} width={W - 2} height={H - 2} fill="none" stroke="var(--trn-hairline)" />
        <line x1={2} y1={H - 2} x2={W - 2} y2={2} stroke="var(--trn-hairline)" strokeDasharray="2 2" />
        <polyline points={pts} fill="none" stroke="var(--trn-brand)" strokeWidth={1.6} />
        <circle cx={2 + roc.op.fpr * (W - 4)} cy={H - 2 - roc.op.tpr * (H - 4)} r={3.5} fill="var(--trn-gold)" stroke="var(--trn-bg)" />
      </svg>
      <figcaption className="num text-[11px] leading-4 text-trn-text3">AUC {roc.auc.toFixed(3)}<br />at p*: TPR {roc.op.tpr.toFixed(2)}<br />FPR {roc.op.fpr.toFixed(2)}</figcaption>
    </figure>
  )
}

export function OutcomeStrip() {
  const t = useT()
  const r = useStore((s) => s.result)
  const computing = useStore((s) => s.computing)
  const [lvl, setLvl] = useState<'warning' | 'watch'>('warning')
  if (!r) return null
  const m = r.metrics[lvl]
  const lead = Object.values(m.lead).filter((x): x is number => x !== null)
  const cell = (label: string, value: string | number, tone?: string, title?: string) => (
    <div className="shrink-0 px-2.5" title={title ?? label}>
      <div className="whitespace-nowrap text-[11px] text-trn-text3">{label}</div>
      <div className={cx('num font-trn-display text-[18px] font-semibold leading-6', tone ?? 'text-trn-text')}>{value}</div>
    </div>
  )
  return (
    <div className="pointer-events-auto flex max-w-full items-center divide-x divide-trn-line overflow-x-auto rounded border border-trn-line bg-trn-scrim py-1.5 backdrop-blur-sm">
      <div className="shrink-0 px-2.5" title={`Outcome ${t('onScenario')}`}>
        <div className="whitespace-nowrap text-[11px] font-semibold text-trn-text2">Outcome · simulated</div>
        <div className="mt-1 flex gap-1">
          {(['warning', 'watch'] as const).map((k) => (
            <button key={k} onClick={() => setLvl(k)} className={cx('h-6 rounded border px-1.5 text-[11px]', lvl === k ? 'border-trn-gold text-trn-text' : 'border-trn-line text-trn-text3')}>{k === 'warning' ? 'Warning+' : 'Watch+'}</button>
          ))}
        </div>
      </div>
      {cell('Detected', `${m.detected} / ${r.metrics.incidents}`, m.missed ? 'text-trn-warning' : 'text-trn-advisory')}
      {cell('Missed', m.missed, m.missed ? 'text-trn-emergency' : undefined)}
      {cell('False alarms', m.falseAlarmEpisodes, m.falseAlarmEpisodes ? 'text-trn-warning' : undefined, `${m.falseAlarmSites} sites without any hazard raised at least one alert`)}
      {cell('Alert time p50 / p90', m.medianTTA === null ? '–' : `${m.medianTTA} / ${m.p90TTA} min`, undefined, 'Time from ignition to the first alert at this level: median / 90th percentile')}
      {lead.length > 0 && cell('Lead time', `${Math.max(...lead)} min`, 'text-trn-advisory', 'Landslide: warning before the simulated failure time')}
      {cell('Alerts / h', m.alertsPerHour.toFixed(1), m.alertsPerHour > 20 ? 'text-trn-warning' : undefined, 'Alert episodes per hour: alert-fatigue indicator')}
      <div className="shrink-0 px-2.5"><Roc /></div>
      <div className="num shrink-0 whitespace-nowrap px-2.5 text-[11px] text-trn-text3">{computing ? 'recomputing' : `${t('recomputed')} ${r.ms.toFixed(0)} ms`}<br />{r.sites.length} sites × {r.nSteps} steps</div>
    </div>
  )
}

export function Timeline() {
  const st = useStore()
  const sc = currentScenario()
  const marks: { t: number; label: string; tone: string }[] = []
  for (const i of sc.incidents) if (i.kind !== 'confuser') marks.push({ t: i.startMin, label: `${i.id} starts`, tone: 'bg-trn-emergency' })
  if (sc.network.outageAtMin !== null) marks.push({ t: sc.network.outageAtMin, label: 'Network outage', tone: 'bg-trn-advisory' })
  const tta = st.result?.metrics.warning.tta ?? {}
  for (const i of sc.incidents) if (tta[i.id] != null) marks.push({ t: i.startMin + (tta[i.id] as number), label: `${i.id} first warning`, tone: 'bg-trn-warning' })
  const pct = (v: number) => `${(v / sc.durationMin) * 100}%`
  return (
    <div className="flex h-12 items-center gap-2 border-t border-trn-line bg-trn-surface px-3">
      <IconButton label="Back to start" onClick={() => st.set({ simMin: 0 })}><SkipBack size={16} /></IconButton>
      <IconButton label={st.playing ? 'Pause (Space)' : 'Play (Space)'} onClick={() => st.set({ playing: !st.playing })} className="text-trn-text">
        {st.playing ? <Pause size={18} /> : <Play size={18} />}
      </IconButton>
      <span className="num w-14 font-trn-mono text-[13px] text-trn-text">{fmtMin(st.simMin)}</span>
      <div className="relative flex-1">
        <input type="range" min={0} max={sc.durationMin} step={sc.stepMin} value={Math.min(st.simMin, sc.durationMin)} aria-label="Simulation time"
          style={{ ['--fill' as string]: pct(st.simMin) }} onChange={(e) => st.set({ simMin: Number(e.target.value) })} />
        {marks.map((m, i) => (
          <span key={i} title={`${m.label} at ${fmtMin(m.t)}`} className={cx('pointer-events-none absolute -top-0.5 h-2 w-0.5 rounded', m.tone)} style={{ left: pct(m.t) }} />
        ))}
      </div>
      <span className="num font-trn-mono text-[12px] text-trn-text3">{fmtMin(sc.durationMin)}</span>
      <select value={st.speed} onChange={(e) => st.set({ speed: Number(e.target.value) })} aria-label="Playback speed" className="h-8 rounded border border-trn-line bg-trn-raised px-1.5 text-[12px] text-trn-text2">
        {SPEEDS.map((s) => <option key={s} value={s}>{s}×</option>)}
      </select>
    </div>
  )
}

export function StatusStrip() {
  const c = useCursor()
  const st = useStore()
  const r = st.result
  const dms = (v: number, p: string, n: string) => { const a = Math.abs(v), d = Math.floor(a), m = Math.floor((a - d) * 60); return `${d}°${String(m).padStart(2, '0')}′${(((a - d) * 60 - m) * 60).toFixed(0)}″${v >= 0 ? p : n}` }
  return (
    <div className="num flex h-7 items-center gap-3 border-t border-trn-line bg-trn-bg px-3 font-trn-mono text-[11px] text-trn-text3">
      <span>{c.lat.toFixed(4)}, {c.lon.toFixed(4)}</span>
      <span className="max-[1500px]:hidden">{dms(c.lat, 'N', 'S')} {dms(c.lon, 'E', 'W')}</span>
      <span>elev {c.elev === null ? '–' : `${Math.round(c.elev)} m`}</span>
      {c.slope !== null && <span>slope {c.slope.toFixed(0)}° · aspect {c.aspect?.toFixed(0)}°</span>}
      <span>z {c.zoom.toFixed(1)}</span>
      <span className="flex-1" />
      {r && <span>engine {r.ms.toFixed(0)} ms</span>}
      {r && <span className="dev-only max-[1500px]:hidden">origins: {r.sites.filter((s) => s.hazard === 'FIRE').length} cameras with real model scores · IoT and positions simulated</span>}
      <Chip tone={st.online ? 'advisory' : 'neutral'} title="Terrain and vector data source">{st.online ? 'Online fill allowed' : 'Offline-cached'}</Chip>
      <span className="dev-only">{c.fps} fps</span>
      <span title={`built ${build.date}`}>v{build.version} · {build.commit}</span>
    </div>
  )
}
