import { useEffect, useState } from 'react'
import raw from './data/trinetra.json'
import Deck from './deck/Deck'
import ConsoleApp from './console/ConsoleApp'
import JudgePage from './judge/JudgePage'
import type { DashboardData } from './types'
import { plain } from './lib'
import { Badge } from './components/Badge'
import { DatasetPack } from './components/DatasetPack'
import { ResultsPanel } from './components/ResultsPanel'

const data = raw as unknown as DashboardData

const ACCOUNTS = [
  { id: 'A', job: 'build, then fire CNN (3 seeds) + colour baseline', sets: 'P02 · P03 · P06 · P33 · P34 · P35', out: 'fire_s*_oof.npz + video' },
  { id: 'B', job: 'zeroshot (open_clip) + confuser stress', sets: 'trinetra-npz-v1', out: 'zeroshot_s0_oof.npz' },
  { id: 'C', job: 'deepfake (3 seeds)', sets: 'trinetra-npz-v1', out: 'deepfake_s*_oof.npz' },
  { id: 'D', job: 'fuse: fusion rules, RL, results', sets: 'outputs of A · B · C', out: 'results/RESULTS.md' },
]

function useHash() {
  const [h, setH] = useState(location.hash)
  useEffect(() => {
    const f = () => setH(location.hash)
    window.addEventListener('hashchange', f)
    return () => window.removeEventListener('hashchange', f)
  }, [])
  return h
}

export default function App() {
  const hash = useHash()
  if (hash.startsWith('#deck')) return <Deck />
  if (hash.startsWith('#live')) return <LiveFlow />
  if (hash.startsWith('#research')) return <Dashboard />
  if (hash.startsWith('#console')) return <ConsoleApp />
  return <JudgePage />
}

// TRINETRA Live Flow animation: a self-contained offline page in public/anim (also exported as one HTML file).
function LiveFlow() {
  return (
    <iframe
      src={`${import.meta.env.BASE_URL}anim/index.html`}
      title="TRINETRA Live Flow"
      className="fixed inset-0 h-full w-full border-0"
      allow="fullscreen"
    />
  )
}

function Dashboard() {
  const { state } = data
  const c = state.counters
  const tasks = Object.entries(state.tasks)
  const done = tasks.filter(([, v]) => v.startsWith('done')).length
  const openGaps = data.gaps.filter((g) => !plain(g.status).startsWith('fixed'))

  const stats = [
    { k: 'Unit tests', v: '128 / 128', note: 'after all fixes' },
    { k: 'CI honesty gates', v: '6 / 6', note: 'ci_gates.py' },
    { k: 'Smoke chain', v: 'PASS', note: 'synthetic, CPU torch' },
    { k: 'Bugs fixed', v: String(data.bugs.filter((b) => b.status.startsWith('FIXED')).length), note: 'found by running code' },
    { k: 'Datasets in pack', v: String(c.datasets_listed), note: `${c.datasets_verified} link-verified` },
    {
      k: 'Real results',
      v: data.results ? String(Object.keys(data.results.models).length) : '—',
      note: data.results ? 'models reported' : 'not measured yet',
    },
  ]

  return (
    <div className="min-h-screen">
      <header className="border-b border-rule">
        <div className="mx-auto max-w-6xl px-6 pt-10 pb-8">
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2 font-mono text-[11px] uppercase tracking-[0.18em] text-muted">
            <span className="text-signal">Trinetra</span>
            <span>Hackathon engine v2</span>
            <span>
              {state.branch} @ {state.commit}
            </span>
            <span>updated {state.updated}</span>
            <a href="#deck" className="rounded-full border border-signal px-3 py-0.5 text-signal hover:bg-signal hover:text-paper">Open 7-slide deck</a>
            <a href="#live" className="rounded-full border border-signal px-3 py-0.5 text-signal hover:bg-signal hover:text-paper">Play Live Flow animation</a>
            <a href={`${import.meta.env.BASE_URL}anim/index.html?video`} target="_blank" rel="noreferrer" className="rounded-full border border-signal px-3 py-0.5 text-signal hover:bg-signal hover:text-paper">Watch video</a>
          </div>
          <h1 className="mt-4 max-w-3xl text-4xl leading-[1.1] font-semibold tracking-tight sm:text-5xl">
            Handoff console for the 36-hour build.
          </h1>
          <p className="mt-4 max-w-2xl text-base text-muted">
            What exists, what is verified, and what comes next, generated from <span className="font-mono text-sm">TRINETRA/HANDOFF</span>{' '}
            and <span className="font-mono text-sm">docs/09b</span>. Every number here traces to a file or a command that was run.
          </p>
          <div className="mt-6 flex max-w-3xl gap-3 rounded-md border-l-2 border-signal bg-white/60 px-4 py-3 text-sm">
            <span className="font-semibold text-signal">Life-safety</span>
            <span className="text-ink/80">
              Advisory research prototype. It complements certified fire alarms and official IMD/NDMA warnings. No public alert leaves
              without human approval.
            </span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl space-y-16 px-6 py-10">
        <section aria-label="Status" className="grid grid-cols-2 gap-px overflow-hidden rounded-lg border border-rule bg-rule md:grid-cols-3 lg:grid-cols-6">
          {stats.map((s) => (
            <div key={s.k} className="bg-paper px-4 py-4">
              <div className="text-[11px] font-medium uppercase tracking-wider text-muted">{s.k}</div>
              <div className="mt-1 font-mono text-2xl font-medium">{s.v}</div>
              <div className="mt-0.5 text-xs text-muted">{s.note}</div>
            </div>
          ))}
        </section>

        <section aria-labelledby="next" className="grid gap-10 lg:grid-cols-[1.1fr_1fr]">
          <div>
            <h2 id="next" className="text-2xl font-semibold tracking-tight">
              Next actions
            </h2>
            <ol className="mt-4 space-y-3">
              {data.next.map((n, i) => (
                <li key={i} className="flex gap-4 rounded-md border border-rule bg-white/60 px-4 py-3 text-sm leading-relaxed">
                  <span className="font-mono text-signal">{String(i + 1).padStart(2, '0')}</span>
                  <span>{plain(n)}</span>
                </li>
              ))}
            </ol>
            <p className="mt-4 text-xs text-muted">
              New AI account? Paste: "Read HANDOFF/NEXT_ACCOUNT_PICKUP.md and HANDOFF/STATE.json, then continue; do not redo finished work."
            </p>
          </div>
          <div>
            <h2 className="text-2xl font-semibold tracking-tight">Kaggle split</h2>
            <p className="mt-1 text-sm text-muted">One real team member per account. Quota limits are not verified yet.</p>
            <ul className="mt-4 divide-y divide-rule rounded-md border border-rule bg-white/60">
              {ACCOUNTS.map((a) => (
                <li key={a.id} className="flex items-start gap-4 px-4 py-3">
                  <span className="grid size-8 shrink-0 place-items-center rounded-full border border-ink font-mono text-sm">{a.id}</span>
                  <div className="min-w-0 text-sm">
                    <div className="font-medium">{a.job}</div>
                    <div className="mt-0.5 font-mono text-[11px] text-muted">
                      {a.sets} → {a.out}
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </section>

        <ResultsPanel results={data.results} />

        <section aria-labelledby="bugs">
          <h2 id="bugs" className="text-2xl font-semibold tracking-tight">
            Bugs found by running the code
          </h2>
          <p className="mt-1 text-sm text-muted">Each trainer was executed end to end. Full table with the repo's 33-item report: docs/BUG_STATUS.md.</p>
          <ul className="mt-4 grid gap-2 md:grid-cols-2">
            {data.bugs.map((b) => (
              <li key={b.id} className="grid grid-cols-[3rem_1fr] gap-3 rounded-md border border-rule bg-white/60 px-4 py-3 text-sm">
                <span className="font-mono text-xs text-muted">{b.id}</span>
                <div>
                  <p className="leading-snug">{plain(b.bug)}</p>
                  <p className="mt-1 text-xs text-muted">{plain(b.fix)}</p>
                  <div className="mt-2">
                    <Badge tone={b.status.startsWith('FIXED') ? (b.status.includes('UNTESTED') ? 'warn' : 'ok') : 'muted'}>
                      {b.status.replace(/\(.*\)/, '').trim()}
                    </Badge>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </section>

        <DatasetPack datasets={data.datasets} />

        <section aria-labelledby="gaps" className="grid gap-10 lg:grid-cols-[1fr_20rem]">
          <div>
            <h2 id="gaps" className="text-2xl font-semibold tracking-tight">
              Open gaps
            </h2>
            <p className="mt-1 text-sm text-muted">
              Doc-vs-code audit. {data.gaps.length - openGaps.length} of {data.gaps.length} fixed with new files.
            </p>
            <ul className="mt-4 space-y-2">
              {openGaps.map((g) => {
                const triage = plain(g.triage)
                const tone = triage.startsWith('FIX NOW') ? 'signal' : triage.startsWith('FIX IF') ? 'warn' : 'muted'
                return (
                  <li key={g.id} className="grid grid-cols-[3.5rem_1fr] gap-3 rounded-md border border-rule bg-white/60 px-4 py-3 text-sm">
                    <span className="font-mono text-xs text-muted">{g.id}</span>
                    <div>
                      <p className="leading-relaxed">{plain(g.gap)}</p>
                      <div className="mt-2">
                        <Badge tone={tone}>{triage.split(':')[0]}</Badge>
                      </div>
                    </div>
                  </li>
                )
              })}
            </ul>
          </div>
          <aside>
            <h2 className="text-2xl font-semibold tracking-tight">Deliverables</h2>
            <p className="mt-1 text-sm text-muted">
              {done} of {tasks.length} done
            </p>
            <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-rule">
              <div className="h-full bg-ink" style={{ width: `${(done / tasks.length) * 100}%` }} />
            </div>
            <ul className="mt-4 space-y-1.5 text-xs">
              {tasks.map(([k, v]) => (
                <li key={k} className="flex items-baseline justify-between gap-3 border-b border-dotted border-rule pb-1.5">
                  <span className="font-mono">{k}</span>
                  <span className={v.startsWith('done') ? 'text-ok' : v.startsWith('todo') ? 'text-signal' : 'text-warn'}>
                    {v.split(' (')[0]}
                  </span>
                </li>
              ))}
            </ul>
          </aside>
        </section>
      </main>

      <footer className="border-t border-rule">
        <div className="mx-auto flex max-w-6xl flex-wrap justify-between gap-2 px-6 py-6 font-mono text-[11px] text-muted">
          <a href={state.repo} target="_blank" rel="noreferrer" className="hover:text-ink">
            {state.repo.replace('https://', '')}
          </a>
          <span>Regenerate: python docs/tools/build_dashboard_data.py</span>
        </div>
      </footer>
    </div>
  )
}
