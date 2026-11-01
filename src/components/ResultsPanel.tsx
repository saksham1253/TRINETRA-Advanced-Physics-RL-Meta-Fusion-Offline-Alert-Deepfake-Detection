import type { Results, Stat } from '../types'
import { GeoResults } from './GeoResults'

const isStat = (v: unknown): v is Stat => typeof v === 'object' && v !== null && 'mean' in v

function Cell({ v }: { v: unknown }) {
  if (!isStat(v)) return <span className="text-muted">not measured</span>
  return (
    <span className="font-mono">
      {v.mean.toFixed(3)}
      <span className="text-muted"> ± {v.sd.toFixed(3)}</span>
    </span>
  )
}

const COLS: [string, string][] = [
  ['oof_roc_auc', 'ROC-AUC (CV)'],
  ['oof_recall_at_fpr05', 'Recall @ FPR 5%'],
  ['test_roc_auc', 'ROC-AUC held-out'],
  ['ece_crossfit_calibrated', 'ECE calibrated'],
]

export function ResultsPanel({ results }: { results: Results | null }) {
  return (
    <section aria-labelledby="results">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 id="results" className="text-2xl font-semibold tracking-tight">
            Results
          </h2>
          <p className="mt-1 max-w-2xl text-sm text-muted">
            Read only from <span className="font-mono text-xs">kaggle/collect_results.py</span> output. Prototype-pack subsets, so these
            are not comparable to full-benchmark papers.
          </p>
        </div>
        {results && <span className="font-mono text-[11px] uppercase tracking-wider text-muted">pack · {results.pack}</span>}
      </div>

      {!results ? (
        <div className="mt-5 rounded-lg border border-dashed border-rule bg-white/40 px-6 py-10">
          <p className="text-lg font-medium">Not measured yet.</p>
          <p className="mt-2 max-w-xl text-sm leading-relaxed text-muted">
            The whole chain passes its smoke test on synthetic data, but no real model has been trained. Run the Kaggle stages, copy{' '}
            <span className="font-mono text-xs">out/results/results.json</span> to <span className="font-mono text-xs">TRINETRA/results/</span>,
            then run <span className="font-mono text-xs">python docs/tools/build_dashboard_data.py</span>.
          </p>
          <ol className="mt-5 flex flex-wrap gap-2 font-mono text-[11px]">
            {['smoke', 'build', 'fire', 'zeroshot', 'deepfake', 'fuse'].map((s, i) => (
              <li key={s} className="rounded-full border border-rule px-3 py-1">
                <span className="text-signal">{i + 1}</span> {s}
              </li>
            ))}
          </ol>
        </div>
      ) : (
        <div className="mt-5 space-y-6">
          {results.dry_run_present && (
            <p className="rounded-md border-l-2 border-signal bg-white/60 px-4 py-3 text-sm">
              Some runs used random zero-shot weights (--dry-run). Do not present those numbers.
            </p>
          )}
          <div className="overflow-x-auto rounded-lg border border-rule bg-white/60">
            <table className="w-full min-w-[640px] text-left text-sm">
              <thead className="border-b border-rule text-[11px] uppercase tracking-wider text-muted">
                <tr>
                  <th className="px-4 py-2.5 font-medium">Model</th>
                  <th className="px-4 py-2.5 font-medium">Seeds</th>
                  <th className="px-4 py-2.5 font-medium">Gate</th>
                  {COLS.map(([, l]) => (
                    <th key={l} className="px-4 py-2.5 font-medium">
                      {l}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-rule">
                {Object.entries(results.models).map(([name, m]) => (
                  <tr key={name}>
                    <td className="px-4 py-2.5 font-medium">{name}</td>
                    <td className="px-4 py-2.5 font-mono">{m.n_seeds}</td>
                    <td className="px-4 py-2.5 text-xs">
                      {m.admitted ? `admitted ${m.admitted}` : m.deploy_learned ? `deploy ${m.deploy_learned}` : '—'}
                    </td>
                    {COLS.map(([k]) => (
                      <td key={k} className="px-4 py-2.5 text-xs">
                        <Cell v={m[k]} />
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {results.geo && Object.keys(results.geo).length > 0 && <GeoResults reports={results.geo} />}
          {results.fusion && (
            <div>
              <h3 className="text-sm font-semibold">
                Fusion rules · synthetic pairing · {results.fusion.sources.join(' + ')} · {results.fusion.seeds.length} seeds
              </h3>
              <div className="mt-2 grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
                {Object.entries(results.fusion.rules)
                  .filter(([r]) => !r.startsWith('p_'))
                  .map(([rule, m]) => (
                    <div key={rule} className="rounded-md border border-rule bg-white/60 px-4 py-3 text-xs">
                      <div className="font-mono text-sm font-medium">{rule}</div>
                      <div className="mt-2 space-y-1">
                        <div>
                          value <Cell v={m.value_score} />
                        </div>
                        <div>
                          miss <Cell v={m.miss_rate} />
                        </div>
                        <div>
                          false alarm <Cell v={m.false_alarm_rate} />
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  )
}
