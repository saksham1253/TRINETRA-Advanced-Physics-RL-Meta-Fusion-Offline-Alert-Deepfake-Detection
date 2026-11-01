import { useMemo, useRef, useState } from 'react'
import { RotateCcw, Undo2, Redo2, Download, Upload, FlaskConical, Columns2, FunctionSquare } from 'lucide-react'
import { useStore } from '../store'
import { PARAMS, PARAM_BY_ID, DEFAULT_VALUES, PRESETS, type ParamDef } from '../engine/params'
import { scenarioInputs } from '../engine/simulate'
import { Button, ClassChip, IconButton, Section, cx } from '../ui/primitives'
import { ask, currentScenario, useTowns } from '../useEngine'
import type { LevelMetrics } from '../engine/simulate'

const toPos = (p: ParamDef, v: number) => {
  const [lo, hi] = p.range
  return p.scale === 'log' ? (Math.log(v / lo) / Math.log(hi / lo)) * 1000 : ((v - lo) / (hi - lo)) * 1000
}
const fromPos = (p: ParamDef, x: number) => {
  const [lo, hi] = p.range
  const v = p.scale === 'log' ? lo * Math.exp((x / 1000) * Math.log(hi / lo)) : lo + (x / 1000) * (hi - lo)
  const st = p.step || 0.01
  const r = Math.round(v / st) * st
  return Number(r.toFixed(Math.max(0, -Math.floor(Math.log10(st)))))
}
export const fmtVal = (p: ParamDef, v: number | string) => {
  if (typeof v === 'string') return v
  if (p.kind === 'toggle') return v ? 'on' : 'off'
  const a = Math.abs(v)
  return a >= 1000 ? v.toLocaleString('en-IN', { maximumFractionDigits: 0 }) : a >= 10 ? v.toFixed(1).replace(/\.0$/, '') : a >= 1 ? v.toFixed(2).replace(/0$/, '') : v.toPrecision(2)
}

function ParamRow({ p }: { p: ParamDef }) {
  const v = useStore((s) => s.params[p.id])
  const base = useStore((s) => s.baseline?.[p.id])
  const mode = useStore((s) => s.mode)
  const setParam = useStore((s) => s.setParam)
  const set = useStore((s) => s.set)
  const disabled = mode === 'LIVE' && !p.live
  const scInputs = scenarioInputs(currentScenario())
  const dflt = scInputs[p.id] ?? p.default
  const changed = v !== dflt
  if (p.kind === 'enum') return null
  const num = Number(v)
  const pos = Math.max(0, Math.min(1000, toPos(p, num)))
  const outOfRegime = p.kind === 'number' && (num < p.range[0] || num > p.range[1])
  return (
    <div className={cx('group py-1.5', disabled && 'opacity-45')} title={disabled ? 'Requires retraining: not adjustable at inference in live mode' : undefined}>
      <div className="flex items-center gap-1.5">
        <button onClick={() => set({ inspector: p.id })} className="min-w-0 flex-1 truncate text-left text-[12.5px] text-trn-text2 hover:text-trn-text" title={`${p.label}. Click for the formula and source.`}>
          {p.label}
        </button>
        <span className={cx('num font-trn-mono text-[12px]', changed ? 'text-trn-gold' : 'text-trn-text')}>{fmtVal(p, v)}</span>
        <span className="w-9 truncate text-[11px] text-trn-text3">{p.unit && p.unit !== '-' ? p.unit : ''}</span>
      </div>
      {p.kind === 'toggle' ? (
        <div className="mt-1 flex gap-1">
          {[1, 0].map((o) => (
            <button key={o} disabled={disabled} onClick={() => setParam(p.id, o)} className={cx('h-6 flex-1 rounded border text-[11px]', Number(v) === o ? 'border-trn-brand text-trn-text' : 'border-trn-line text-trn-text3')}>
              {o ? 'Wind-driven ellipse' : 'Circular'}
            </button>
          ))}
        </div>
      ) : (
        <div className="flex items-center gap-1">
          <input type="range" min={0} max={1000} step={1} value={pos} disabled={disabled} aria-label={p.label}
            style={{ ['--fill' as string]: `${pos / 10}%` }}
            onChange={(e) => setParam(p.id, fromPos(p, Number(e.target.value)))} />
          <IconButton label={`Reset ${p.label} to ${fmtVal(p, dflt)}`} disabled={!changed || disabled} onClick={() => setParam(p.id, dflt)}
            className={cx('h-6 w-6', !changed && 'invisible')}><RotateCcw size={12} /></IconButton>
        </div>
      )}
      <div className="flex items-center gap-1.5 text-[11px] text-trn-text3">
        <ClassChip cls={p.cls} />
        <span className="truncate font-trn-mono">{p.ref ? `${p.ref.file.replace('TRINETRA/trinetra/', '')}:${p.ref.line}` : 'not in repo'}</span>
        {base !== undefined && base !== v && <span className="num ml-auto shrink-0 text-trn-text3">A: {fmtVal(p, base)}</span>}
        {outOfRegime && <span className="ml-auto text-trn-warning">outside regime</span>}
      </div>
    </div>
  )
}

function Sensitivity() {
  const [pid, setPid] = useState('cost.C_FA')
  const [metric, setMetric] = useState<'falseAlarmEpisodes' | 'missed' | 'medianTTA' | 'alertEpisodes'>('falseAlarmEpisodes')
  const [lvl, setLvl] = useState<'watch' | 'warning'>('warning')
  const [out, setOut] = useState<{ v: number; m: LevelMetrics }[] | null>(null)
  const [ms, setMs] = useState(0)
  const [busy, setBusy] = useState(false)
  const towns = useTowns((s) => s.towns)
  const p = PARAM_BY_ID[pid]
  const run = async () => {
    setBusy(true)
    const vals = Array.from({ length: 9 }, (_, i) => fromPos(p, (i / 8) * 1000))
    const st = useStore.getState()
    const r = await ask<{ out: { v: number; watch: LevelMetrics; warning: LevelMetrics }[]; ms: number }>({
      type: 'sweep', scenario: currentScenario(), towns, params: st.params, technique: st.technique, paramId: pid, values: vals })
    setOut(r.out.map((o) => ({ v: o.v, m: o[lvl] }))); setMs(r.ms); setBusy(false)
  }
  const pts = (out ?? []).map((o) => ({ x: o.v, y: (o.m[metric] as number | null) ?? NaN }))
  const ys = pts.map((q) => q.y).filter(Number.isFinite)
  const ymax = Math.max(1, ...ys), W = 280, H = 90
  const sx = (i: number) => 8 + (i / Math.max(1, pts.length - 1)) * (W - 16)
  const sy = (y: number) => H - 14 - (y / ymax) * (H - 26)
  return (
    <Section title={<span className="flex items-center gap-1.5"><FlaskConical size={14} />Sensitivity explorer</span>}>
      <div className="grid grid-cols-2 gap-1.5">
        <select value={pid} onChange={(e) => { setPid(e.target.value); setOut(null) }} aria-label="Parameter" className="col-span-2 h-7 rounded border border-trn-line bg-trn-raised px-1.5 text-[12px] text-trn-text2">
          {PARAMS.filter((q) => q.kind === 'number' && !q.id.startsWith('lora.') && !q.id.startsWith('sur.')).map((q) => <option key={q.id} value={q.id}>{q.group}: {q.label}</option>)}
        </select>
        <select value={metric} onChange={(e) => setMetric(e.target.value as typeof metric)} aria-label="Output" className="h-7 rounded border border-trn-line bg-trn-raised px-1.5 text-[12px] text-trn-text2">
          <option value="falseAlarmEpisodes">False alarms</option><option value="missed">Missed incidents</option>
          <option value="medianTTA">Median time to alert</option><option value="alertEpisodes">All alerts</option>
        </select>
        <select value={lvl} onChange={(e) => setLvl(e.target.value as typeof lvl)} aria-label="Level" className="h-7 rounded border border-trn-line bg-trn-raised px-1.5 text-[12px] text-trn-text2">
          <option value="warning">Warning or higher</option><option value="watch">Watch or higher</option>
        </select>
      </div>
      <Button className="mt-2 w-full" onClick={run} disabled={busy}>{busy ? 'Sweeping 9 values in the worker' : 'Sweep 9 values'}</Button>
      {out && (
        <figure className="mt-2">
          <svg width={W} height={H} role="img" aria-label="Response curve" className="overflow-visible">
            <line x1={8} x2={W - 8} y1={H - 14} y2={H - 14} stroke="var(--trn-hairline)" />
            <polyline fill="none" stroke="var(--trn-brand)" strokeWidth={2} points={pts.map((q, i) => `${sx(i)},${Number.isFinite(q.y) ? sy(q.y) : H - 14}`).join(' ')} />
            {pts.map((q, i) => <circle key={i} cx={sx(i)} cy={Number.isFinite(q.y) ? sy(q.y) : H - 14} r={2.5} fill="var(--trn-text)" />)}
            <text x={8} y={H - 2} fontSize={10} fill="var(--trn-text3)">{fmtVal(p, pts[0]?.x ?? 0)}</text>
            <text x={W - 8} y={H - 2} fontSize={10} fill="var(--trn-text3)" textAnchor="end">{fmtVal(p, pts[pts.length - 1]?.x ?? 0)} {p.unit !== '-' ? p.unit : ''}</text>
            <text x={8} y={8} fontSize={10} fill="var(--trn-text3)">max {fmtVal(p, ymax)}</text>
          </svg>
          <figcaption className="text-[11px] leading-4 text-trn-text3">Computed in {ms.toFixed(0)} ms. Parameter effects shown here are properties of the model and scenario, not field accuracy.</figcaption>
        </figure>
      )}
    </Section>
  )
}

export default function ParamsPanel() {
  const [q, setQ] = useState('')
  const [open, setOpen] = useState<Record<string, boolean>>({ Decision: true, Fusion: true, 'Fire physics': false })
  const st = useStore()
  const file = useRef<HTMLInputElement>(null)
  const groups = useMemo(() => {
    const g = new Map<string, ParamDef[]>()
    for (const p of PARAMS) if (!q || (p.label + p.group + p.id).toLowerCase().includes(q.toLowerCase())) g.set(p.group, [...(g.get(p.group) ?? []), p])
    return [...g]
  }, [q])
  const applyPreset = (k: string) => st.setParams({ ...DEFAULT_VALUES, ...scenarioInputs(currentScenario()), ...PRESETS[k].values })
  const save = () => {
    const blob = new Blob([JSON.stringify({ trinetra_params: 1, scenario: st.scenarioId, technique: st.technique, values: st.params }, null, 1)], { type: 'application/json' })
    const a = Object.assign(document.createElement('a'), { href: URL.createObjectURL(blob), download: `trinetra_params_${st.scenarioId}.json` })
    a.click(); URL.revokeObjectURL(a.href)
  }
  const load = (f: File) => f.text().then((t) => { const j = JSON.parse(t); if (j.values) st.setParams({ ...st.params, ...j.values }); if (j.technique) st.set({ technique: j.technique }) })
  const nChanged = PARAMS.filter((p) => st.params[p.id] !== (scenarioInputs(currentScenario())[p.id] ?? p.default)).length
  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <div className="space-y-2 border-b border-trn-line px-4 py-3">
        <div className="flex items-center gap-1">
          <select aria-label="Preset" onChange={(e) => { if (e.target.value) applyPreset(e.target.value); e.target.value = '' }} defaultValue=""
            className="h-8 w-0 min-w-0 flex-1 rounded border border-trn-line bg-trn-raised px-2 text-[12px] text-trn-text2">
            <option value="" disabled>Presets</option>
            {Object.entries(PRESETS).map(([k, v]) => <option key={k} value={k} title={v.note}>{v.label}</option>)}
          </select>
          <IconButton label="Undo (Ctrl+Z)" onClick={st.undo} disabled={!st.history.length}><Undo2 size={15} /></IconButton>
          <IconButton label="Redo (Ctrl+Shift+Z)" onClick={st.redo} disabled={!st.future.length}><Redo2 size={15} /></IconButton>
          <IconButton label={st.baseline ? 'Clear A/B baseline' : 'Hold current values as baseline A'} onClick={() => st.set({ baseline: st.baseline ? null : { ...st.params } })}
            className={st.baseline ? 'text-trn-gold' : ''}><Columns2 size={15} /></IconButton>
          <IconButton label="Save parameter set (JSON)" onClick={save}><Download size={15} /></IconButton>
          <IconButton label="Load parameter set (JSON)" onClick={() => file.current?.click()}><Upload size={15} /></IconButton>
          <input ref={file} type="file" accept="application/json" hidden onChange={(e) => e.target.files?.[0] && load(e.target.files[0])} />
        </div>
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder={`Filter ${PARAMS.length} parameters`} aria-label="Filter parameters"
          className="h-8 w-full rounded border border-trn-line bg-trn-raised px-2 text-[13px] text-trn-text placeholder:text-trn-text3 focus:border-trn-gold focus:outline-none" />
        <div className="flex items-center justify-between text-[11px] text-trn-text3">
          <span className="whitespace-nowrap">{nChanged} changed{st.baseline ? ' · A/B held' : ''}</span>
          <button className="whitespace-nowrap hover:text-trn-text2" onClick={() => st.set({ inspector: 'fusion.tau' })}><FunctionSquare size={12} className="mr-1 inline" />Formula inspector</button>
        </div>
      </div>
      <div className="min-h-0 flex-1 overflow-y-auto">
        {groups.map(([g, ps]) => (
          <div key={g} className="border-b border-trn-line">
            <button onClick={() => setOpen({ ...open, [g]: !(open[g] ?? !!q) })} aria-expanded={open[g] ?? !!q}
              className="flex h-9 w-full items-center justify-between px-4 text-[13px] font-semibold text-trn-text hover:bg-trn-raised">
              <span>{g}</span><span className="num text-[11px] font-normal text-trn-text3">{ps.filter((p) => p.kind !== 'enum').length}</span>
            </button>
            {(open[g] ?? !!q) && <div className="px-4 pb-2">{ps.map((p) => <ParamRow key={p.id} p={p} />)}</div>}
          </div>
        ))}
        <Sensitivity />
      </div>
    </div>
  )
}
