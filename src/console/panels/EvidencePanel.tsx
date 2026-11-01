import { useMemo, useState } from 'react'
import { Crosshair, Copy, ShieldCheck, Check, X } from 'lucide-react'
import { useStore } from '../store'
import { currentScenario, toast } from '../useEngine'
import { evalSiteStep, STACK, type SiteStep } from '../engine/simulate'
import { fuse, type Expert, type Technique } from '../engine/fusion'
import { conformalLevel, pStar } from '../engine/decision'
import { num } from '../engine/params'
import { strouhalPuffingFrequency, plumeCenterlineDT } from '../engine/firephys'
import { fmtMin, perimeter, stepOf } from '../derived'
import { Button, Chip, ClassChip, OriginChip, Section, SevBadge, StatusChip, cx } from '../ui/primitives'
import { ACTION_TEXT, LEVEL_KEY, useT } from '../i18n'
import regions from '../data/regions.json'
import { stateOf } from '../geoData'

const TECHS: Technique[] = ['FM-1', 'PHARAOH', 'GMF', 'STACK', 'MEAN', 'MEDIAN', 'MAX']
const TECH_NOTE: Record<Technique, string> = {
  'FM-1': 'Repo default (Class B): reliability, consistency and uncertainty weighted mean',
  PHARAOH: 'Repo Class C, default off: adaptive power mean that bends toward max for credible alarms',
  GMF: 'Repo Class B: gated mixture; the learned residual head is not loaded in the browser (residual 0)',
  STACK: 'Logistic stack on the same image (fire_meta_fusion.py); OOF AUC 0.951 vs clip_probe 0.959',
  MEAN: 'Comparison only: plain mean', MEDIAN: 'Comparison only: median', MAX: 'Comparison only: maximum',
}
const CAP: Record<number, string> = { 1: 'Minor / Future / Possible', 2: 'Severe / Expected / Likely', 3: 'Extreme / Immediate / Observed' }

const dms = (v: number, pos: string, neg: string) => {
  const a = Math.abs(v), d = Math.floor(a), m = Math.floor((a - d) * 60), s = ((a - d - m / 60) * 3600).toFixed(1)
  return `${d}°${String(m).padStart(2, '0')}′${s}″${v >= 0 ? pos : neg}`
}

function ExpertCard({ e, influence }: { e: Expert; influence: number | null }) {
  return (
    <li className={cx('rounded border px-3 py-2', e.available ? 'border-trn-line bg-trn-raised' : 'border-dashed border-trn-line')}>
      <div className="flex items-center gap-1.5">
        <span className="min-w-0 flex-1 truncate text-[13px] font-medium text-trn-text">{e.label}</span>
        <StatusChip status={e.status} />
      </div>
      {e.available ? (
        <>
          <div className="mt-1.5 flex items-center gap-2">
            <div className="relative h-2 flex-1 rounded bg-trn-bg" aria-label={`score ${e.p.toFixed(2)}`}>
              <div className="absolute inset-y-0 left-0 rounded bg-trn-brand" style={{ width: `${e.p * 100}%` }} />
              <div className="absolute inset-y-[-3px] border-x border-trn-text3/70" style={{ left: `${Math.max(0, e.p - e.u / 2) * 100}%`, width: `${Math.min(1, e.u) * 100}%` }} title="uncertainty band (u)" />
            </div>
            <span className="num w-10 text-right font-trn-mono text-[12px] text-trn-text">{e.p.toFixed(2)}</span>
          </div>
          <div className="mt-1 flex flex-wrap items-center gap-1 text-[11px] text-trn-text3">
            <span className="num">u {e.u.toFixed(2)} · c {e.c.toFixed(2)} · r {e.r.toFixed(2)}</span>
            {influence !== null && <span className={cx('num ml-auto', influence >= 0 ? 'text-trn-warning' : 'text-trn-advisory')}>{influence >= 0 ? '+' : ''}{influence.toFixed(3)} to fused</span>}
          </div>
          <div className="mt-1 flex flex-wrap gap-1"><OriginChip origin={e.origin} /><ClassChip cls={e.cls} />{e.note && <span className="text-[11px] text-trn-text3">{e.note}</span>}</div>
        </>
      ) : <p className="mt-1 text-[12px] text-trn-text3">{e.note ?? 'Not part of this run.'}</p>}
    </li>
  )
}

export default function EvidencePanel() {
  const t = useT()
  const st = useStore()
  const [reason, setReason] = useState('')
  const site = st.result?.sites.find((s) => s.id === st.selected)
  const sc = currentScenario()
  const step = st.result ? stepOf(st.result, st.simMin) : 0
  const d: SiteStep | null = useMemo(() => (site ? evalSiteStep(sc, site, step, st.params, st.technique) : null), [site, step, st.params, st.technique, sc])
  if (!site || !d) return <div className="px-4 py-6 text-[13px] text-trn-text3">Select an alert beacon or a camera on the map. Double-click a beacon to dive to its terrain.</div>
  const fp = { tau: num(st.params, 'fusion.tau'), lambda: num(st.params, 'fusion.lambda'), kappa: num(st.params, 'fusion.kappa') }
  const ps = pStar({ C_FA: num(st.params, 'cost.C_FA'), C_miss: num(st.params, 'cost.C_miss') })
  const avail = d.experts.filter((e) => e.available)
  const fusedWith = (ex: Expert[], tech = st.technique) => fuse(ex, tech, fp, STACK).p
  const infl = new Map(avail.map((e) => [e.id, avail.length > 1 ? d.fusion.p - fusedWith(d.experts.filter((x) => x.id !== e.id)) : null]))
  const lo = Math.min(...avail.map((e) => e.p)), hi = Math.max(...avail.map((e) => e.p))
  const bounded = d.fusion.p >= lo - 1e-9 && d.fusion.p <= hi + 1e-9
  const missingOk = Math.abs(fusedWith([...d.experts, { ...avail[0], id: 'x', available: false, p: 1 }]) - d.fusion.p) < 1e-12
  const monotone = avail.every((e) => fusedWith(d.experts.map((x) => (x.id === e.id ? { ...x, p: Math.min(1, x.p + 0.05) } : x))) >= d.fusion.p - 1e-9)
  const lvl = ['GREEN', 'YELLOW', 'ORANGE', 'RED'].indexOf(d.decision.level)
  const reg = regions.regions.find((r) => r.id === site.regionId)
  const where = `${stateOf(site.lon, site.lat)}${reg ? `, ${reg.name.split(',')[0]}` : ''}`
  const life = st.lifecycle[site.id] ?? 'New'
  const canAct = st.role === 'Operator' || st.role === 'Supervisor'
  const top = [...avail].sort((a, b) => (infl.get(b.id) ?? 0) - (infl.get(a.id) ?? 0))[0]
  const why = st.lang === 'hinglish'
    ? `Fused risk ${d.fusion.p.toFixed(3)} hai; p* = ${ps.toFixed(3)}. Isliye level ${t(LEVEL_KEY[lvl])} (${d.decision.point !== d.decision.level ? 'shield ne raise kiya' : 'conformal cut points se'}). Sabse zyada asar: ${top?.label ?? '-'}. Uncertainty U* ${d.fusion.uStar.toFixed(2)}${d.decision.uncertain ? ', jo abstain threshold se upar hai, isliye human review zaroori hai' : ''}.`
    : `Fused risk is ${d.fusion.p.toFixed(3)} against p* = ${ps.toFixed(3)} (cut points p*, ${num(st.params, 'dec.orange_mult')}p*, ${num(st.params, 'dec.red_mult')}p*), giving ${t(LEVEL_KEY[d.decision.point === 'GREEN' ? 0 : ['GREEN', 'YELLOW', 'ORANGE', 'RED'].indexOf(d.decision.point)])}${d.decision.shield.raised ? `; the safety shield raised it to ${t(LEVEL_KEY[lvl])} (${d.decision.shield.reason})` : ''}. Largest influence: ${top?.label ?? 'none'}. Conflict-aware uncertainty U* = ${d.fusion.uStar.toFixed(2)}${d.decision.uncertain ? ', above the abstain threshold, so the alert is held for human review' : ''}.`
  const pm = site.incident ? perimeter(site.incident, sc, st.simMin, st.params) : null
  return (
    <div className="min-h-0 flex-1 overflow-y-auto">
      <Section title={<span className="flex items-center gap-2"><SevBadge level={lvl} label={t(LEVEL_KEY[lvl])} />{site.hazard === 'LANDSLIDE' ? 'Landslide' : 'Fire or smoke'} · {site.id}</span>}
        right={<Button variant="ghost" className="h-7 px-2" onClick={() => st.set({ diveSite: site.id })}><Crosshair size={14} />Dive</Button>}>
        <dl className="grid grid-cols-[96px_1fr] gap-y-1 text-[12.5px]">
          <dt className="text-trn-text3">Where</dt><dd className="text-trn-text2">{where}</dd>
          <dt className="text-trn-text3">Coordinates</dt>
          <dd className="flex items-center gap-1 font-trn-mono text-[12px] text-trn-text2">{site.lat.toFixed(5)}, {site.lon.toFixed(5)}
            <button aria-label="Copy coordinates" className="text-trn-text3 hover:text-trn-text" onClick={() => { navigator.clipboard?.writeText(`${site.lat.toFixed(5)}, ${site.lon.toFixed(5)}`); toast('Coordinates copied') }}><Copy size={12} /></button></dd>
          <dt className="text-trn-text3" />
          <dd className="font-trn-mono text-[11px] text-trn-text3">{dms(site.lat, 'N', 'S')} {dms(site.lon, 'E', 'W')}</dd>
          <dt className="text-trn-text3">Confidence</dt><dd className="num text-trn-text2">risk {d.fusion.p.toFixed(3)} · U* {d.fusion.uStar.toFixed(2)} · {d.decision.reliability} · set {d.decision.predSet.join('–')}</dd>
          <dt className="text-trn-text3">Action</dt><dd className="text-trn-text2">{ACTION_TEXT[lvl][st.lang]}</dd>
          <dt className="text-trn-text3">Authority</dt><dd className="text-trn-text2">District authority decides; TRINETRA is advisory</dd>
          <dt className="text-trn-text3">Time</dt><dd className="num text-trn-text2">{fmtMin(d.t)} scenario time · {st.mode === 'SIM' ? 'simulated' : st.mode.toLowerCase()}</dd>
        </dl>
        {st.showTruth && st.mode === 'SIM' && (
          <div className="mt-2 text-[12px] text-trn-text3">Simulator truth: {d.active ? 'hazard is active here' : site.confuserStart !== null && d.t >= site.confuserStart ? 'no hazard; confuser scene (hard negative)' : 'no hazard'}.</div>
        )}
      </Section>
      <Section title="Why this tier?"><p className="text-[13px] leading-5 text-trn-text2">{why}</p></Section>
      <Section title="Evidence chain" right={<span className="text-[11px] text-trn-text3">leave-one-out influence</span>}>
        <ul className="space-y-1.5">{d.experts.map((e) => <ExpertCard key={e.id} e={e} influence={infl.get(e.id) ?? null} />)}</ul>
        {d.validator && (
          <div className="mt-2 rounded border border-trn-line p-2 text-[12px] text-trn-text2">
            <div className="mb-1 flex items-center justify-between"><span>Temporal validator (ws4_cctv)</span><Chip tone={d.validator.confirmed ? 'b' : 'muted'}>{d.validator.confirmed ? 'confirmed' : 'not confirmed'}</Chip></div>
            <div className="flex gap-0.5">{d.validator.window.map((c, i) => (
              <div key={i} className="flex-1"><div className="h-6 rounded-sm bg-trn-bg"><div className={cx('h-full rounded-sm', c >= num(st.params, 'cctv.thr') ? 'bg-trn-brand' : 'bg-trn-line')} style={{ height: `${Math.max(8, c * 100)}%` }} /></div>
                <div className="num mt-0.5 text-center font-trn-mono text-[10px] text-trn-text3">{c.toFixed(2)}</div></div>))}</div>
          </div>
        )}
      </Section>
      <Section title="Averaging technique" right={<span className="text-[11px] text-trn-text3">same evidence, re-fused live</span>}>
        <ul className="space-y-1">
          {TECHS.map((tq) => {
            const r = fuse(d.experts, tq, fp, STACK)
            const l = conformalLevel(r.p, ps, num(st.params, 'dec.orange_mult'), num(st.params, 'dec.red_mult'))
            const li = ['GREEN', 'YELLOW', 'ORANGE', 'RED'].indexOf(l)
            return (
              <li key={tq}><button onClick={() => st.set({ technique: tq })} aria-pressed={st.technique === tq} title={TECH_NOTE[tq]}
                className={cx('flex w-full items-center gap-2 rounded border px-2 py-1.5 text-left', st.technique === tq ? 'border-trn-gold/70 bg-trn-raised' : 'border-trn-line hover:bg-trn-raised')}>
                <span className="w-16 font-trn-mono text-[12px] text-trn-text">{tq}</span>
                <span className="relative h-1.5 flex-1 rounded bg-trn-bg"><span className="absolute inset-y-0 left-0 rounded bg-trn-brand" style={{ width: `${r.p * 100}%` }} /></span>
                <span className="num w-11 text-right font-trn-mono text-[12px] text-trn-text2">{r.p.toFixed(3)}</span>
                <SevBadge level={li} label={['Normal', 'Watch', 'Warning', 'Emerg.'][li]} />
              </button></li>
            )
          })}
        </ul>
        <p className="mt-1.5 text-[11px] leading-4 text-trn-text3">{TECH_NOTE[st.technique]}{d.fusion.note ? `. ${d.fusion.note}` : ''}</p>
        <div className="mt-2 grid grid-cols-3 gap-1 text-[11px]">
          {[['Bounded by inputs', bounded], ['Missing input ignored', missingOk], ['Monotone in each input', monotone]].map(([k, ok]) => (
            <div key={String(k)} className={cx('flex items-center gap-1 rounded border px-1.5 py-1', ok ? 'border-trn-b/50 text-trn-b' : 'border-trn-emergency/60 text-trn-emergency')}>
              {ok ? <Check size={12} /> : <X size={12} />}<span className="text-trn-text2">{String(k)}</span></div>))}
        </div>
      </Section>
      <Section title="Physics">
        {site.hazard === 'FIRE' ? (
          <dl className="grid grid-cols-[1fr_auto] gap-y-1 text-[12.5px]">
            <dt className="text-trn-text3">Byram N_c (Class A)</dt><dd className="num text-trn-text2">{d.physics.Nc === null ? 'not estimated (no fire regime here)' : Number(d.physics.Nc).toFixed(3)}</dd>
            <dt className="text-trn-text3">Physics consistency c</dt><dd className="num text-trn-text2">{Number(d.physics.consistency).toFixed(2)}</dd>
            {pm && <>
              <dt className="text-trn-text3">Flame height L (Heskestad)</dt><dd className="num text-trn-text2">{pm.flameM.toFixed(1)} m</dd>
              <dt className="text-trn-text3">Puffing frequency (Strouhal)</dt><dd className="num text-trn-text2">{strouhalPuffingFrequency(pm.D).toFixed(2)} Hz</dd>
              <dt className="text-trn-text3">Plume ΔT at 2L height</dt><dd className="num text-trn-text2">{plumeCenterlineDT(num(st.params, 'fire.Qc_kW_m'), Math.max(1, 2 * pm.flameM), 0, num(st.params, 'fire.T_inf')).toFixed(0)} K</dd>
              <dt className="text-trn-text3">Head spread / area (SURROGATE)</dt><dd className="num text-trn-text2">{(pm.headM / 1000).toFixed(2)} km · {pm.areaHa.toFixed(0)} ha · L/B {pm.LB.toFixed(2)}</dd>
            </>}
          </dl>
        ) : (
          <dl className="grid grid-cols-[1fr_auto] gap-y-1 text-[12.5px]">
            <dt className="text-trn-text3">Factor of safety FS</dt><dd className="num text-trn-text2">{Number(d.physics.FS).toFixed(3)}</dd>
            <dt className="text-trn-text3">Pressure head ψ (Iverson)</dt><dd className="num text-trn-text2">{Number(d.physics.psi_m).toFixed(2)} m</dd>
            <dt className="text-trn-text3">Caine I-D ratio</dt><dd className="num text-trn-text2">{Number(d.physics.caine).toFixed(2)}</dd>
            <dt className="text-trn-text3">Rain now / cumulative</dt><dd className="num text-trn-text2">{Number(d.physics.rain_mm_h)} mm/h · {Number(d.physics.rain24_mm).toFixed(0)} mm</dd>
            <dt className="text-trn-text3">Max tilt rate (simulated)</dt><dd className="num text-trn-text2">{Number(d.physics.tilt_max).toFixed(1)} deg/day</dd>
          </dl>
        )}
        {site.hazard === 'FIRE' && d.physics.Nc !== null && Number(d.physics.Nc) < 1 && (
          <p className="mt-2 text-[11px] leading-4 text-trn-warning">Model note: the repo fire gate treats N_c below 2 as wind-dominated and lowers consistency, which also down-weights real wind-driven fires. Flagged for the physics team.</p>
        )}
      </Section>
      <Section title={<span className="flex items-center gap-1.5"><ShieldCheck size={14} />Operator approval gate</span>} right={<Chip tone="muted">{life}</Chip>}>
        {lvl > 0 && <div className="mb-2 text-[12px] text-trn-text3">CAP 1.2 mapping (ws3_alert/cap.py): severity / urgency / certainty = {CAP[lvl]}</div>}
        <div className="grid grid-cols-2 gap-1.5">
          <Button variant="primary" disabled={!canAct || lvl === 0} onClick={() => st.act(site.id, 'Approved')}>{t('approve')}</Button>
          <Button disabled={!canAct} onClick={() => st.act(site.id, 'Under review')}>{t('hold')}</Button>
          <Button disabled={!canAct} onClick={() => st.act(site.id, 'Acknowledged', 'escalated to supervisor')}>{t('escalate')}</Button>
          <Button variant="danger" disabled={!canAct || !reason} onClick={() => { st.act(site.id, 'Dismissed', reason); setReason('') }}>{t('dismiss')}</Button>
        </div>
        <select value={reason} onChange={(e) => setReason(e.target.value)} aria-label="Dismiss reason" className="mt-1.5 h-8 w-full rounded border border-trn-line bg-trn-raised px-2 text-[12px] text-trn-text2">
          <option value="">Reason required to dismiss</option><option>Verified on camera: no fire</option><option>Known confuser (fog, steam, glare)</option><option>Duplicate of another alert</option><option>Sensor fault</option>
        </select>
        {life === 'Approved' && (
          <Button className="mt-1.5 w-full" onClick={() => { st.act(site.id, 'Dispatched (demo)'); toast('DEMO: no message sent to any person or channel') }}>Dispatch (demo, sends nothing)</Button>
        )}
        <p className="mt-1.5 text-[11px] text-trn-text3">{t('demoNoSend')}. {canAct ? '' : `Role ${st.role} is read-only.`}</p>
      </Section>
    </div>
  )
}
