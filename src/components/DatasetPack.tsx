import { useMemo, useState } from 'react'
import type { Dataset } from '../types'
import { MODULES, primaryModule, statusLabel, statusTone } from '../lib'
import { Badge } from './Badge'

export function DatasetPack({ datasets }: { datasets: Dataset[] }) {
  const [mod, setMod] = useState<string>('all')
  const [query, setQuery] = useState('')
  const [open, setOpen] = useState<string | null>(null)

  const counts = useMemo(() => {
    const c: Record<string, number> = {}
    datasets.forEach((d) => {
      const m = primaryModule(d.modules)
      c[m] = (c[m] ?? 0) + 1
    })
    return c
  }, [datasets])

  const rows = datasets.filter((d) => {
    if (mod !== 'all' && primaryModule(d.modules) !== mod) return false
    const q = query.trim().toLowerCase()
    return !q || `${d.name} ${d.task} ${d.license} ${d.link}`.toLowerCase().includes(q)
  })

  return (
    <section aria-labelledby="pack">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 id="pack" className="text-2xl font-semibold tracking-tight">
            Prototype dataset pack
          </h2>
          <p className="mt-1 max-w-2xl text-sm text-muted">
            Small, free, link-checked sets mapped to the repo's existing loaders. Sizes and licenses for Kaggle rows
            come from the Kaggle API snapshot, not from memory.
          </p>
        </div>
        <label className="relative w-full sm:w-72">
          <span className="sr-only">Search datasets</span>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search name, task, license"
            className="w-full rounded-md border border-rule bg-white/70 px-3 py-2 text-sm outline-none placeholder:text-muted/70 focus:border-ink"
          />
        </label>
      </div>

      <div className="mt-5 flex flex-wrap gap-1.5" role="tablist" aria-label="Filter by module">
        {[['all', 'All modules', datasets.length] as const, ...Object.entries(MODULES).map(([k, v]) => [k, v, counts[k] ?? 0] as const)]
          .filter(([, , n]) => n > 0)
          .map(([k, label, n]) => (
            <button
              key={k}
              role="tab"
              aria-selected={mod === k}
              onClick={() => setMod(k)}
              className={`rounded-full border px-3 py-1 text-xs transition-colors ${
                mod === k ? 'border-ink bg-ink text-paper' : 'border-rule text-ink hover:border-ink/60'
              }`}
            >
              {k !== 'all' && <span className="mr-1 font-mono opacity-60">{k}</span>}
              {label}
              <span className="ml-1.5 opacity-50">{n}</span>
            </button>
          ))}
      </div>

      <div className="mt-4 overflow-hidden rounded-lg border border-rule bg-white/60">
        <div className="hidden grid-cols-[3.5rem_1fr_9rem_10rem_9rem] gap-4 border-b border-rule px-4 py-2.5 text-[11px] font-medium uppercase tracking-wider text-muted md:grid">
          <span>ID</span>
          <span>Dataset · role</span>
          <span>Size</span>
          <span>License</span>
          <span>Status</span>
        </div>
        {rows.length === 0 && <p className="px-4 py-10 text-center text-sm text-muted">No dataset matches this filter.</p>}
        <ul className="divide-y divide-rule">
          {rows.map((d) => {
            const isOpen = open === d.ID
            return (
              <li key={d.ID}>
                <button
                  onClick={() => setOpen(isOpen ? null : d.ID)}
                  aria-expanded={isOpen}
                  className="grid w-full grid-cols-1 gap-1 px-4 py-3 text-left transition-colors hover:bg-paper/70 md:grid-cols-[3.5rem_1fr_9rem_10rem_9rem] md:items-center md:gap-4"
                >
                  <span className="font-mono text-xs text-muted">{d.ID}</span>
                  <span className="min-w-0">
                    <span className="block truncate text-sm font-medium">{d.name}</span>
                    <span className="block truncate text-xs text-muted">{d.role}</span>
                  </span>
                  <span className="font-mono text-xs">{d.size_full}</span>
                  <span className="truncate text-xs">{d.license}</span>
                  <span>
                    <Badge tone={statusTone(d.status)}>{statusLabel(d.status)}</Badge>
                  </span>
                </button>
                {isOpen && (
                  <div className="grid gap-x-8 gap-y-3 border-t border-dashed border-rule bg-paper/50 px-4 py-4 text-xs sm:grid-cols-2 md:pl-[5.5rem]">
                    <Field k="Module" v={d.modules} />
                    <Field k="Task" v={d.task} />
                    <Field k="Samples" v={d.samples} />
                    <Field k="Labels" v={d.labels} />
                    <Field k="Recommended subset" v={d.size_subset} />
                    <Field k="Access" v={d.access} />
                    <Field k="Age / domain gap" v={d.age_domain_gap} />
                    <Field k="Known problems / split key" v={d.known_problems} />
                    <Field k="Adapter" v={d.format_adapter} mono />
                    <Field k="Verification" v={d.status} />
                    <div className="flex flex-wrap gap-3 sm:col-span-2">
                      <a href={d.link} target="_blank" rel="noreferrer" className="font-medium text-signal underline underline-offset-4">
                        Open source page
                      </a>
                      {d.mirror_or_kaggle.startsWith('http') && (
                        <a
                          href={d.mirror_or_kaggle.split(' ')[0]}
                          target="_blank"
                          rel="noreferrer"
                          className="text-ink underline decoration-rule underline-offset-4 hover:decoration-ink"
                        >
                          Mirror / origin
                        </a>
                      )}
                    </div>
                  </div>
                )}
              </li>
            )
          })}
        </ul>
      </div>
    </section>
  )
}

function Field({ k, v, mono }: { k: string; v: string; mono?: boolean }) {
  if (!v || v === '-') return null
  return (
    <div>
      <div className="text-[10px] font-medium uppercase tracking-wider text-muted">{k}</div>
      <div className={`mt-0.5 leading-relaxed ${mono ? 'font-mono text-[11px]' : ''}`}>{v}</div>
    </div>
  )
}
