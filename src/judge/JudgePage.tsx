import { useState } from 'react'
import { ArrowRight, Eye, Atom, Scale, RadioTower, X } from 'lucide-react'
import '../console/console.css'
import master from '../../TRINETRA/results/master_merged/master.json'
import finalFigures from '../console/data/final_figures.json'
import { Button, Chip, Tabs, cx } from '../console/ui/primitives'
import { Eyebrow, Heading, Rule } from './ui'
import { TryItSection } from './TryIt'

type Row = { hazard: string; expert: string; metric: string; value: string | null; admitted: string | null; note: string }
type Fig = { url: string; name: string; group: string; title: string; explain: string }

const rows = master.scorecard as Row[]
const figs = finalFigures as Fig[]
const byExpert = (e: string) => rows.find((r) => r.expert === e)
const nums = (e: string) => (byExpert(e)?.value?.match(/[+-]?\d+\.\d+/g) ?? []).map(Number)
const fmt = (n: number | undefined, d = 3) => (n === undefined || Number.isNaN(n) ? '–' : n.toFixed(d))
const pct = (a?: number, b?: number) => (a && b !== undefined ? `−${Math.round((1 - b / a) * 100)}%` : '–')

const stress = nums('stress')            // probe base, probe conf, stack base, stack conf, DeepFire base, DeepFire conf
const cross = nums('crossmodal')         // stack, clip_probe, fire_cnn
const caine = nums('caine_ratio')
const meta = nums('fire_meta_fusion')    // OOF, held-out, stack - best
const deepfake = nums('deepfake')
const rlHeld = nums('offline_rl_heldout') // gain vs rule, LCB, gain vs tuned, LCB
const admitted = rows.filter((r) => /^[1-9]\d*\//.test(r.admitted ?? ''))

const HEADLINES = [
  { value: pct(stress[2], stress[3]), label: 'fewer false alarms on look-alikes the model never saw', detail: `Candles, fog and normal street scenes left out of training. Combined model at equal 90% recall: ${fmt(stress[2], 2)} → ${fmt(stress[3], 2)}. Accuracy on a new fire dataset kept (${fmt(stress[4])} → ${fmt(stress[5])}).`, tag: `Admitted ${byExpert('stress')?.admitted ?? ''} seeds` },
  { value: fmt(caine[0]), label: 'landslide ROC-AUC with zero training', detail: 'A 1980 rainfall-threshold law (Caine), applied to 184 real Indian landslides from NASA records with NASA rainfall. No data fitting at all.', tag: 'Physics' },
  { value: `+${fmt(cross[0], 2)}`, label: 'video score when three models vote together', detail: `Detection minus false alarms on 49 FireSense videos. Best single model +${fmt(cross[1], 2)}, our CNN alone +${fmt(cross[2], 2)}. Small sample, so read it as counts.`, tag: '3 seeds' },
  { value: fmt(meta[1]), label: 'fire ROC-AUC on a dataset never used in training', detail: 'Trained on D-Fire camera images, tested on DeepFire forest photos after removing duplicates.', tag: 'Held-out' },
]

const STEPS = [
  { icon: Eye, title: 'See', text: 'A fire CNN, CLIP zero-shot and a CLIP probe score every camera frame. For slopes, rain from NASA POWER and terrain from elevation tiles.' },
  { icon: Atom, title: 'Check with physics', text: 'Flame height, plume and flicker for fire. Factor of safety and the Caine rain threshold for slopes. Physics can raise an alert, never lower it.' },
  { icon: Scale, title: 'Weigh the cost', text: 'Each model is weighted by reliability: w = r · c · e^(−u/τ). Alarm only when risk exceeds p* = C_FA / (C_FA + C_miss) = 5 / 105 ≈ 0.048.' },
  { icon: RadioTower, title: 'Warn', text: 'An operator approves every public alert. Siren, LoRa mesh and a CAP message still reach villages when internet and mobile networks are down.' },
]

const LIMITS = [
  { title: 'Fake-image detector does not generalise', text: `${fmt(deepfake[0])} on its training source, ${fmt(deepfake[1])} on images from new generators — worse than a coin flip. It only down-weights suspicious media; it never raises or cancels an alarm.` },
  { title: 'Learned alarm policy (RL) was not deployed', text: `It beat the rule in-sample, but on held-out folds the 95% lower bound of its gain is ${fmt(rlHeld[1], 2)}. The simple cost rule stays in charge.` },
  { title: 'Stacking fire models did not beat the best one', text: `Stack minus best single model: ${fmt(meta[2])} ROC-AUC. Not admitted, so the system keeps the simpler FM-1 weighting.` },
]

const CURATED: Record<'fire' | 'slope' | 'decide', { name: string; title: string; caption: string }[]> = {
  fire: [
    { name: 'R9_stress_retrain.png', title: 'Fewer false alarms after retraining', caption: 'Training with look-alike negatives (candles, fog, scenes) cuts false alarms on the type held out from training. The combined model gains most.' },
    { name: 'R7_crossmodal_video.png', title: 'Three models beat one on video', caption: 'On real fire and smoke videos, the three-model stack with a temporal check beats every single model.' },
    { name: 'R1_fire_roc_oof_and_heldout.png', title: 'Fire detection ROC curves', caption: 'ROC curves on our cross-validation folds (left) and on a never-seen dataset (right). Higher and further left is better.' },
    { name: 'G04_confuser_false_alarms.png', title: 'Where false alarms came from', caption: 'Before retraining: how often each model calls a non-fire image “fire”. Small benign flames are the hardest case.' },
  ],
  slope: [
    { name: 'R4_landslide_auc.png', title: 'Physics alone predicts landslides', caption: 'Blue bars are physics with no fitting. They already reach about 0.75 ROC-AUC on real Indian landslides.' },
    { name: 'G09_caine_scatter.png', title: 'Rain duration vs intensity', caption: 'Each dot is one day. Landslide days (orange) sit toward longer, heavier rain, closer to the Caine line.' },
    { name: 'G08_landslide_features.png', title: 'Landslide days vs normal days', caption: 'Landslide days versus normal days at the same place. Rain and the physics scores shift right; slope does not, because the place is the same.' },
    { name: '01_fs_vs_pore_pressure.png', title: 'Why wet slopes fail', caption: 'The core mechanism: water pressure in the soil lowers the factor of safety. Below 1 the slope fails.' },
  ],
  decide: [
    { name: 'R0_scorecard_all_auc.png', title: 'Every result on one chart', caption: 'Every measured ROC-AUC in one place: same-source folds versus a new source.' },
    { name: 'R6_generalisation_gap.png', title: 'What survives a new dataset', caption: 'Fire models hold up on new data. The fake-image model collapses, which is why it is low-trust.' },
    { name: '07_cost_loss_and_prior_shift.png', title: 'Where the alarm threshold comes from', caption: 'Where the alarm threshold comes from: a false alarm costs 5, a missed fire costs 100.' },
    { name: 'G12_offline_rl_gain.png', title: 'Why the learned policy was not deployed', caption: 'The learned policy looked good in-sample. On honest held-out folds its lower bound falls below zero.' },
  ],
}
const TAB_ITEMS = [{ id: 'fire' as const, label: 'Fire and smoke' }, { id: 'slope' as const, label: 'Landslides' }, { id: 'decide' as const, label: 'Decisions' }]
const src = (f?: Fig) => (f ? import.meta.env.BASE_URL + f.url : '')
const go = (id: string) => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
const openConsole = () => { location.hash = '#console' }

export default function JudgePage() {
  const [tab, setTab] = useState<'fire' | 'slope' | 'decide'>('fire')
  const [sel, setSel] = useState(0)
  const [showAll, setShowAll] = useState(false)
  const [showTable, setShowTable] = useState(false)
  const [zoom, setZoom] = useState<Fig | null>(null)
  const list = CURATED[tab].map((c) => ({ ...c, fig: figs.find((f) => f.name === c.name) })).filter((c) => c.fig)
  const cur = list[Math.min(sel, list.length - 1)]

  return (
    <div className="trn min-h-screen bg-trn-bg text-trn-text" data-theme="light">
      <header className="sticky top-0 z-20 border-b border-trn-line bg-trn-bg/95 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-3">
          <div className="flex items-baseline gap-3">
            <span className="font-trn-display text-lg font-semibold tracking-widest">TRINETRA</span>
            <span className="hidden text-sm text-trn-text3 sm:inline">Team Sankat Mochak</span>
          </div>
          <nav className="hidden items-center gap-1 md:flex" aria-label="Sections">
            {[['results', 'Results'], ['how', 'How it works'], ['try', 'Try it'], ['graphs', 'Graphs'], ['limits', 'Limits']].map(([id, l]) => (
              <Button key={id} variant="ghost" onClick={() => go(id)}>{l}</Button>
            ))}
          </nav>
          <Button variant="primary" onClick={openConsole}>Live demo<ArrowRight size={15} /></Button>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6">
        <section className="grid gap-10 py-16 md:grid-cols-12 md:py-24">
          <div className="md:col-span-8">
            <Eyebrow>Fire · smoke · landslide · early warning</Eyebrow>
            <Heading level={1} className="mt-4">Sees a disaster early. Checks it against physics. Warns only when it is worth it.</Heading>
            <p className="mt-6 max-w-2xl text-lg leading-relaxed text-trn-text2">
              TRINETRA combines camera AI with landslide and fire physics and a cost-based alarm rule, built for the Indian Himalaya.
              Every number on this page was measured by us on public datasets, with whole locations kept out of training.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Button variant="primary" className="h-10 px-4 text-base" onClick={openConsole}>Open the live demo<ArrowRight size={16} /></Button>
              <Button className="h-10 px-4 text-base" onClick={() => go('results')}>See the results</Button>
            </div>
          </div>
          <dl className="self-end border-l border-trn-line pl-6 md:col-span-4">
            {[
              [String(admitted.length), 'learned upgrade passed our acceptance gate', admitted.map((r) => r.expert).join(', ')],
              [String(rows.filter((r) => r.value).length), 'measured results in the scorecard', 'spatial cross-validation, 3 seeds where possible'],
              ['18', 'public datasets used', 'fire, video, fake media, landslide, GLOF, satellite'],
            ].map(([v, l, s]) => (
              <div key={l} className="border-b border-trn-line py-4 last:border-0">
                <dt className="text-sm text-trn-text2">{l}</dt>
                <dd className="num font-trn-display text-4xl font-semibold">{v}</dd>
                <dd className="text-xs text-trn-text3">{s}</dd>
              </div>
            ))}
          </dl>
        </section>

        <Rule />
        <section id="results" className="scroll-mt-20 py-16">
          <Eyebrow>01 · Results</Eyebrow>
          <Heading className="mt-3 max-w-3xl">Four numbers worth remembering</Heading>
          <div className="mt-10 grid border-t border-trn-line md:grid-cols-4">
            {HEADLINES.map((h, i) => (
              <article key={h.label} className={cx('py-6 md:px-6', i > 0 && 'border-t border-trn-line md:border-l md:border-t-0', i === 0 && 'md:pl-0')}>
                <div className="num font-trn-display text-5xl font-semibold text-trn-brand">{h.value}</div>
                <p className="mt-3 font-medium text-trn-text">{h.label}</p>
                <p className="mt-2 text-sm leading-relaxed text-trn-text2">{h.detail}</p>
                <div className="mt-4"><Chip tone="neutral">{h.tag}</Chip></div>
              </article>
            ))}
          </div>
        </section>

        <Rule />
        <section id="how" className="scroll-mt-20 py-16">
          <Eyebrow>02 · How it works</Eyebrow>
          <Heading className="mt-3 max-w-3xl">One decision path for every hazard</Heading>
          <ol className="mt-10 grid gap-8 md:grid-cols-4">
            {STEPS.map((s, i) => (
              <li key={s.title} className="relative">
                <div className="flex items-center gap-3">
                  <span className="num font-trn-mono text-sm text-trn-text3">0{i + 1}</span>
                  <s.icon size={20} className="text-trn-brand" aria-hidden />
                  {i < STEPS.length - 1 && <span className="hidden h-px flex-1 bg-trn-line md:block" />}
                </div>
                <Heading level={3} className="mt-4">{s.title}</Heading>
                <p className="mt-2 text-sm leading-relaxed text-trn-text2">{s.text}</p>
              </li>
            ))}
          </ol>
        </section>

        <Rule />
        <TryItSection />

        <Rule />
        <section id="graphs" className="scroll-mt-20 py-16">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <Eyebrow>04 · Graphs</Eyebrow>
              <Heading className="mt-3">The evidence, one graph at a time</Heading>
            </div>
            <div className="w-full max-w-md"><Tabs value={tab} onChange={(t) => { setTab(t); setSel(0) }} items={TAB_ITEMS} /></div>
          </div>
          {cur && (
            <div className="mt-8 grid gap-8 md:grid-cols-12">
              <div className="md:col-span-4">
                {list.map((c, i) => (
                  <Button key={c.name} variant="ghost" onClick={() => setSel(i)}
                    className={cx('h-auto w-full justify-start rounded-none border-0 border-l-2 py-3 text-left text-sm', i === sel ? 'border-trn-brand bg-trn-surface text-trn-text' : 'border-trn-line')}>
                    <span className="num font-trn-mono text-xs text-trn-text3">{String(i + 1).padStart(2, '0')}</span>
                    <span className="ml-2">{c.title}</span>
                  </Button>
                ))}
              </div>
              <figure className="md:col-span-8">
                <Button variant="ghost" className="h-auto w-full rounded border-trn-line bg-trn-surface p-3" onClick={() => setZoom({ ...cur.fig!, title: cur.title, explain: cur.caption })} aria-label="Enlarge graph">
                  <img src={src(cur.fig)} alt={cur.title} className="w-full" />
                </Button>
                <figcaption className="mt-4 max-w-2xl text-base leading-relaxed text-trn-text2">{cur.caption}</figcaption>
              </figure>
            </div>
          )}
          <div className="mt-10">
            <Button onClick={() => setShowAll((v) => !v)}>{showAll ? 'Hide' : 'Show'} all {figs.length} graphs</Button>
            {showAll && (
              <div className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {figs.map((f) => (
                  <figure key={f.url} className="border-t border-trn-line pt-3">
                    <Button variant="ghost" className="h-auto w-full bg-trn-surface p-2" onClick={() => setZoom(f)} aria-label={`Enlarge ${f.title}`}>
                      <img src={src(f)} alt={f.title} loading="lazy" className="h-40 w-full object-contain" />
                    </Button>
                    <figcaption className="mt-2 text-sm font-medium text-trn-text">{f.title}</figcaption>
                    <p className="mt-1 text-xs leading-relaxed text-trn-text3">{f.explain}</p>
                  </figure>
                ))}
              </div>
            )}
          </div>
        </section>

        <Rule />
        <section id="limits" className="scroll-mt-20 py-16">
          <Eyebrow>05 · What did not work</Eyebrow>
          <Heading className="mt-3 max-w-3xl">We report our failures too</Heading>
          <p className="mt-4 max-w-2xl text-trn-text2">A model enters the live system only if it beats simple baselines with a 95% confidence interval. These did not.</p>
          <div className="mt-10 grid gap-8 md:grid-cols-3">
            {LIMITS.map((l) => (
              <article key={l.title} className="border-t-2 border-trn-text pt-4">
                <Heading level={3}>{l.title}</Heading>
                <p className="mt-2 text-sm leading-relaxed text-trn-text2">{l.text}</p>
              </article>
            ))}
          </div>
          <div className="mt-10">
            <Button onClick={() => setShowTable((v) => !v)}>{showTable ? 'Hide' : 'Show'} the full scorecard</Button>
            {showTable && (
              <div className="mt-6 overflow-x-auto">
                <table className="w-full text-sm">
                  <thead><tr className="border-b border-trn-text text-left text-trn-text3"><th className="py-2 pr-4 font-medium">Hazard</th><th className="pr-4 font-medium">Model</th><th className="pr-4 font-medium">Metric</th><th className="pr-4 font-medium">Value</th><th className="font-medium">Gate</th></tr></thead>
                  <tbody className="num">
                    {rows.filter((r) => r.value).map((r) => (
                      <tr key={r.hazard + r.expert} className="border-b border-trn-line align-top">
                        <td className="py-2 pr-4">{r.hazard}</td><td className="pr-4 font-trn-mono text-xs">{r.expert}</td>
                        <td className="pr-4 text-trn-text2">{r.metric}</td><td className="pr-4 text-trn-text">{r.value}</td><td className="text-trn-text2">{r.admitted ?? '–'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </section>

        <Rule />
        <section className="grid gap-8 py-16 md:grid-cols-12">
          <div className="md:col-span-7">
            <Heading>See it run</Heading>
            <p className="mt-3 max-w-xl text-trn-text2">The live demo replays real model scores on a 3D map of India: fires, a landslide scenario and a network outage with LoRa rerouting. Locations are synthetic.</p>
          </div>
          <div className="flex flex-wrap items-start gap-3 md:col-span-5 md:justify-end">
            <Button variant="primary" className="h-10 px-4 text-base" onClick={openConsole}>Open the live demo<ArrowRight size={16} /></Button>
            <Button className="h-10 px-4 text-base" onClick={() => { location.hash = '#deck' }}>Slides</Button>
          </div>
        </section>
      </main>

      <footer className="border-t border-trn-line">
        <div className="mx-auto max-w-6xl px-6 py-8 text-xs leading-relaxed text-trn-text3">
          Research prototype by Team Sankat Mochak. Advisory only, not an official warning system; every public alert needs human approval.
          Results are measured on small public datasets and are not field-validated. Sources: NASA Global Landslide Catalog, NASA POWER, D-Fire, DeepFire, FireSense, CIFAKE, HMAGLOFDB and others listed in docs/20_FINAL/DATASETS_USED.csv.
        </div>
      </footer>

      {zoom && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-trn-scrim p-6" role="dialog" aria-modal="true" aria-label={zoom.title} onMouseDown={(e) => e.target === e.currentTarget && setZoom(null)}>
          <figure className="max-h-full w-full max-w-5xl overflow-auto rounded border border-trn-line bg-trn-surface p-4">
            <div className="flex items-start justify-between gap-4">
              <figcaption className="font-trn-display text-lg font-semibold">{zoom.title}</figcaption>
              <Button variant="ghost" onClick={() => setZoom(null)} aria-label="Close"><X size={16} /></Button>
            </div>
            <img src={src(zoom)} alt={zoom.title} className="mt-3 w-full" />
            <p className="mt-3 text-sm leading-relaxed text-trn-text2">{zoom.explain}</p>
          </figure>
        </div>
      )}
    </div>
  )
}
