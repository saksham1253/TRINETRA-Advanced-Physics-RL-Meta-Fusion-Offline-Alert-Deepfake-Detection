import type { Tone } from '../lib'

const tones: Record<Tone, string> = {
  ok: 'text-ok border-ok/30 bg-ok/5',
  warn: 'text-warn border-warn/30 bg-warn/5',
  signal: 'text-signal border-signal/30 bg-signal/5',
  muted: 'text-muted border-rule bg-white/40',
}

export function Badge({ tone, children }: { tone: Tone; children: React.ReactNode }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 whitespace-nowrap rounded-full border px-2 py-0.5 text-[11px] font-medium ${tones[tone]}`}
    >
      <span className="size-1.5 rounded-full bg-current" aria-hidden />
      {children}
    </span>
  )
}
