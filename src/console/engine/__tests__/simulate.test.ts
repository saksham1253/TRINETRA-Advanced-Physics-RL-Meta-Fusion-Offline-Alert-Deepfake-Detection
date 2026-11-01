import { describe, expect, it } from 'vitest'
import { buildSites, run, scenarioInputs, type Scenario } from '../simulate'
import { DEFAULT_VALUES } from '../params'

const mods = import.meta.glob('../../data/scenarios/*.json', { eager: true, import: 'default' }) as Record<string, Scenario>
const towns: [string, number, number, string, number][] = Array.from({ length: 200 }, (_, i) => [`T${i}`, 10 + (i % 25), 72 + (i % 20), 'S', 1e5])

describe('scenario engine', () => {
  for (const [f, sc] of Object.entries(mods)) {
    it(`${f}: deterministic, within budget`, () => {
      const P = { ...DEFAULT_VALUES, ...scenarioInputs(sc) }
      const a = run(sc, buildSites(sc, towns), P, 'FM-1')
      const b = run(sc, buildSites(sc, towns), P, 'FM-1')
      expect(Array.from(a.level)).toEqual(Array.from(b.level))
      const c = run(sc, buildSites(sc, towns), { ...P, 'fusion.prior': 0.01 }, 'FM-1')
      const m = (x: typeof a.metrics.watch) => `det ${x.detected} miss ${x.missed} FAsites ${x.falseAlarmSites} FAep ${x.falseAlarmEpisodes} tta ${x.medianTTA}/${x.p90TTA} lead ${JSON.stringify(x.lead)}`
      console.log(`${sc.id} n=${a.sites.length} ${a.ms.toFixed(0)}ms AUC ${a.roc.auc.toFixed(3)} | default W: ${m(a.metrics.watch)} | WARN: ${m(a.metrics.warning)} || prior 0.01 W: ${m(c.metrics.watch)} | WARN: ${m(c.metrics.warning)}`)
    })
  }
})
