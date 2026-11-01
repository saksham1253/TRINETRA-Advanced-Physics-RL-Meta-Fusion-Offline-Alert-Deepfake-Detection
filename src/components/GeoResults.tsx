import type { GeoReport } from '../types'

const f = (v: number | null | undefined, d = 3) => (v === null || v === undefined || Number.isNaN(v) ? '—' : v.toFixed(d))

const LABEL: Record<string, string> = {
  caine_ratio: 'Caine I–D ratio (physics, no fit)',
  dFS_iverson: 'ΔFS Iverson + slope (physics, no fit)',
  geo_gate_repo: 'Repo geo gate (back-analysed soil)',
  logit_rain: 'Logistic on rain (data baseline)',
  logit_physics: 'Logistic on physics features',
  logit_hybrid: 'Logistic rain + physics',
}

export function GeoResults({ reports }: { reports: Record<string, GeoReport> }) {
  const list = Object.values(reports)
  const hind = list.find((r) => r.name === 'geo_physics')
  const glof = list.find((r) => r.name === 'glof_physics')
  const rl = list.filter((r) => r.name?.startsWith('rl_env')).sort((a, b) => (a.C_miss ?? 0) - (b.C_miss ?? 0))
  return (
    <div className="space-y-8">
      {hind?.scores && (
        <div>
          <h3 className="text-sm font-semibold">
            Landslide physics on real events · NASA catalog + POWER rain + Copernicus DEM · {hind.n_pos} events, {hind.n} rows,{' '}
            {hind.n_blocks} spatial blocks
          </h3>
          <div className="mt-2 overflow-x-auto rounded-lg border border-rule bg-white/60">
            <table className="w-full min-w-[520px] text-left text-sm">
              <thead className="border-b border-rule text-[11px] uppercase tracking-wider text-muted">
                <tr>
                  <th className="px-4 py-2 font-medium">Score</th>
                  <th className="px-4 py-2 font-medium">ROC-AUC</th>
                  <th className="px-4 py-2 font-medium">PR-AUC</th>
                  <th className="px-4 py-2 font-medium">Recall @ FPR 5%</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-rule">
                {Object.entries(hind.scores).map(([k, v]) => (
                  <tr key={k}>
                    <td className="px-4 py-2">{LABEL[k] ?? k}</td>
                    <td className="px-4 py-2 font-mono text-xs">{f(v.roc_auc)}</td>
                    <td className="px-4 py-2 font-mono text-xs">{f(v.pr_auc)}</td>
                    <td className="px-4 py-2 font-mono text-xs">{f(v.recall_at_fpr05)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {hind.physics_minus_rain_auc && (
            <p className="mt-2 text-xs text-muted">
              Physics minus rain AUC {f(hind.physics_minus_rain_auc.mean)} (95% CI {f(hind.physics_minus_rain_auc.ci95[0])} to{' '}
              {f(hind.physics_minus_rain_auc.ci95[1])}). Case-control design, so the base rate is artificial.
            </p>
          )}
        </div>
      )}

      {glof && (
        <div>
          <h3 className="text-sm font-semibold">GLOF relations · ICIMOD HMAGLOFDB v4 (fitted, Class B)</h3>
          <div className="mt-2 grid gap-2 sm:grid-cols-2">
            {(['area_volume', 'volume_peakQ'] as const).map((k) => {
              const v = glof[k]
              return (
                <div key={k} className="rounded-md border border-rule bg-white/60 px-4 py-3 text-xs">
                  <div className="font-mono text-sm font-medium">{k === 'area_volume' ? 'V = a·A^b' : 'Qp = c·V^d'}</div>
                  <div className="mt-1">
                    n {v?.n} · exponent <span className="font-mono">{f(v?.exponent, 2)}</span> (CI {f(v?.exponent_ci95?.[0], 2)}–
                    {f(v?.exponent_ci95?.[1], 2)}) · R² {f(v?.r2_log, 2)}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {rl.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold">Landslide RL · physics simulator with real rain seasons (simulator, not field)</h3>
          <div className="mt-2 grid gap-3 lg:grid-cols-3">
            {rl.map((r) => (
              <div key={r.name} className="rounded-md border border-rule bg-white/60 px-4 py-3 text-xs">
                <div className="flex items-baseline justify-between">
                  <span className="font-mono text-sm font-medium">miss cost {r.C_miss}</span>
                  <span className="text-muted">{r.n_seasons} seasons</span>
                </div>
                <ul className="mt-2 space-y-1">
                  {Object.entries(r.policies ?? {}).map(([k, v]) => (
                    <li key={k} className="flex justify-between gap-2">
                      <span className={k === r.best_rule ? 'font-medium' : ''}>{k.replace(/_/g, ' ')}</span>
                      <span className="font-mono">{f(v.return_mean, 1)}</span>
                    </li>
                  ))}
                </ul>
                <p className="mt-2 text-muted">
                  learned deploy: {String(r.deploy_learned)} (95% LCB {f(r.gain_vs_rule_lcb95, 1)})
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
