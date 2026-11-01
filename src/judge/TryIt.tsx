import { useMemo, useState } from 'react'
import { Shuffle } from 'lucide-react'
import bank from '../console/data/evidence_bank.json'
import { fuse, type Expert } from '../console/engine/fusion'
import { decide, type Level } from '../console/engine/decision'
import { DEFAULT_VALUES, num } from '../console/engine/params'
import { Button, Chip, cx } from '../console/ui/primitives'
import { Eyebrow, Heading } from './ui'

// Real out-of-fold scores of three trained models on the SAME image (tools/export_evidence_bank.py), decided by the
// same FM-1 fusion + cost-loss decision code the console and the Python package use. Single image: no video validator.
const COLS = bank.columns
const ROWS = bank.rows as number[][]
const ci = (n: string) => COLS.indexOf(n)
const IY = ci('y'), ICF = ci('cal_fire_cnn'), ICZ = ci('cal_zeroshot'), ICP = ci('cal_clip_probe')
const POS = ROWS.map((r, i) => [r, i] as const).filter(([r]) => r[IY] === 1).map(([, i]) => i)
const NEG = ROWS.map((r, i) => [r, i] as const).filter(([r]) => r[IY] === 0).map(([, i]) => i)
const HARD = [...NEG].sort((a, b) => ROWS[b][ICZ] + ROWS[b][ICP] - (ROWS[a][ICZ] + ROWS[a][ICP])).slice(0, Math.round(NEG.length / 10))
const h2 = (p: number) => { const q = Math.min(Math.max(p, 1e-6), 1 - 1e-6); return -(q * Math.log2(q) + (1 - q) * Math.log2(1 - q)) }
const P = DEFAULT_VALUES
const LEVEL_UI: Record<Level, { label: string; tone: string; bar: string }> = {
  GREEN: { label: 'No alert', tone: 'text-trn-advisory', bar: 'bg-trn-advisory' },
  YELLOW: { label: 'Watch', tone: 'text-trn-watch', bar: 'bg-trn-watch' },
  ORANGE: { label: 'Warning', tone: 'text-trn-warning', bar: 'bg-trn-warning' },
  RED: { label: 'Emergency', tone: 'text-trn-emergency', bar: 'bg-trn-emergency' },
}
const MODES = [
  { id: 'fire', label: 'A real fire image', pool: POS },
  { id: 'none', label: 'A normal image', pool: NEG },
  { id: 'hard', label: 'A fire look-alike', pool: HARD },
] as const
const COSTS = [20, 100, 500]

function evaluate(i: number, C_miss: number) {
  const r = ROWS[i]
  const mk = (id: string, label: string, p: number, trust: string): Expert =>
    ({ id, label, source: id, p, u: 0.5 * h2(p), c: 1, r: num(P, trust), cls: 'data', available: true, origin: 'REAL-OOF', status: 'IMPLEMENTED' })
  const experts = [
    mk('fire_cnn', 'Fire CNN (ours)', r[ICF], 'trust.fire_cnn'),
    mk('zeroshot', 'CLIP zero-shot', r[ICZ], 'trust.zeroshot'),
    mk('clip_probe', 'CLIP probe', r[ICP], 'trust.clip_probe'),
  ]
  const f = fuse(experts, 'FM-1', { tau: num(P, 'fusion.tau'), lambda: num(P, 'fusion.lambda'), kappa: num(P, 'fusion.kappa') })
  const risk = f.p
  const d = decide(risk, f.uStar, true, {}, { C_FA: num(P, 'cost.C_FA'), C_miss, orangeMult: num(P, 'dec.orange_mult'), redMult: num(P, 'dec.red_mult'), uncertain: num(P, 'dec.uncertain') })
  return { experts, risk, d, truth: r[IY] === 1 }
}

function Bar({ value, className }: { value: number; className: string }) {
  return (
    <div className="h-2 w-full rounded-full bg-trn-raised">
      <div className={cx('h-2 rounded-full', className)} style={{ width: `${Math.max(1, value * 100)}%` }} />
    </div>
  )
}

export function TryIt() {
  const [mode, setMode] = useState<(typeof MODES)[number]['id']>('hard')
  const [seed, setSeed] = useState(7)
  const [cMiss, setCMiss] = useState(100)
  const pool = MODES.find((m) => m.id === mode)!.pool
  const idx = pool[seed % pool.length]
  const { experts, risk, d, truth } = useMemo(() => evaluate(idx, cMiss), [idx, cMiss])
  const lv = LEVEL_UI[d.level]
  const alarmed = d.level !== 'GREEN'
  const verdict = truth ? (alarmed ? 'Correct: fire caught' : 'Missed fire') : (alarmed ? 'False alarm' : 'Correct: no alarm')

  return (
    <div className="mt-10 grid gap-8 md:grid-cols-12">
      <div className="md:col-span-4">
        <p className="text-sm font-medium text-trn-text">1 · Pick an image</p>
        <div className="mt-2 flex flex-col gap-2">
          {MODES.map((m) => (
            <Button key={m.id} variant={mode === m.id ? 'primary' : 'default'} className="h-10 justify-start" onClick={() => { setMode(m.id); setSeed((s) => s + 1) }}>
              {m.label}<span className="ml-auto font-trn-mono text-xs opacity-70">{m.pool.length}</span>
            </Button>
          ))}
          <Button variant="ghost" className="justify-start" onClick={() => setSeed((s) => s + 1)}><Shuffle size={14} />Another one</Button>
        </div>
        <p className="mt-6 text-sm font-medium text-trn-text">2 · How costly is a missed fire?</p>
        <p className="text-xs text-trn-text3">A false alarm costs 5.</p>
        <div className="mt-2 flex gap-2">
          {COSTS.map((c) => <Button key={c} variant={cMiss === c ? 'primary' : 'default'} onClick={() => setCMiss(c)}>{c}</Button>)}
        </div>
      </div>

      <div className="rounded border border-trn-line bg-trn-surface p-6 md:col-span-8">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <p className="font-trn-mono text-xs text-trn-text3">real image #{idx + 1} of {ROWS.length} · ground truth: {truth ? 'fire' : 'no fire'}</p>
          <Chip tone="neutral">{verdict}</Chip>
        </div>
        <div className="mt-5 space-y-4">
          {experts.map((e) => (
            <div key={e.id} className="grid grid-cols-12 items-center gap-3">
              <span className="col-span-4 text-sm text-trn-text2">{e.label}</span>
              <div className="col-span-6"><Bar value={e.p} className="bg-trn-text3" /></div>
              <span className="num col-span-2 text-right font-trn-mono text-sm">{e.p.toFixed(2)}</span>
            </div>
          ))}
          <div className="grid grid-cols-12 items-center gap-3 border-t border-trn-line pt-4">
            <span className="col-span-4 text-sm font-medium text-trn-text">Fused risk (FM-1)</span>
            <div className="col-span-6"><Bar value={risk} className={lv.bar} /></div>
            <span className="num col-span-2 text-right font-trn-mono text-sm font-semibold">{risk.toFixed(2)}</span>
          </div>
        </div>
        <div className="mt-6 flex flex-wrap items-end justify-between gap-4 border-t border-trn-line pt-5">
          <div>
            <p className="text-xs text-trn-text3">Decision</p>
            <p className={cx('font-trn-display text-3xl font-semibold', lv.tone)}>{lv.label}</p>
          </div>
          <p className="max-w-sm text-right text-xs leading-relaxed text-trn-text3">
            Alert threshold p* = 5 / (5 + {cMiss}) = <span className="num font-trn-mono text-trn-text2">{d.pStar.toFixed(3)}</span>.
            Watch above p*, Warning above 4·p*, Emergency above 10·p*. Single image, so the video check is off.
          </p>
        </div>
        {!truth && alarmed && (
          <p className="mt-4 border-l-2 border-trn-brand pl-3 text-sm text-trn-text2">
            This is the weak spot of the original models: the CLIP scores fire on look-alikes. Our confuser-aware retraining cuts these
            false alarms on look-alikes it never saw, and the temporal video check removes more in the live system.
          </p>
        )}
      </div>
    </div>
  )
}

export function TryItSection() {
  return (
    <section id="try" className="scroll-mt-20 py-16">
      <Eyebrow>03 · Try it</Eyebrow>
      <Heading className="mt-3 max-w-3xl">Run the real decision on a real image</Heading>
      <p className="mt-4 max-w-2xl text-trn-text2">
        These are the actual scores our three trained models gave to 3,410 test images they never trained on. The fusion and alarm
        rule below are the same code the live console and our Python package run.
      </p>
      <TryIt />
    </section>
  )
}
