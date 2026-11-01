import type { ReactNode, ButtonHTMLAttributes } from 'react'

export const cx = (...c: (string | false | null | undefined)[]) => c.filter(Boolean).join(' ')

type Tone = 'neutral' | 'brand' | 'gold' | 'advisory' | 'watch' | 'warning' | 'emergency' | 'a' | 'b' | 'c' | 'muted'
const TONE: Record<Tone, string> = {
  neutral: 'border-trn-line text-trn-text2',
  muted: 'border-trn-line text-trn-text3',
  brand: 'border-trn-brand/60 text-trn-brand2',
  gold: 'border-trn-gold/60 text-trn-gold',
  advisory: 'border-trn-advisory/60 text-trn-advisory',
  watch: 'border-trn-watch/60 text-trn-watch',
  warning: 'border-trn-warning/60 text-trn-warning',
  emergency: 'border-trn-emergency/60 text-trn-emergency',
  a: 'border-trn-a/60 text-trn-a',
  b: 'border-trn-b/60 text-trn-b',
  c: 'border-trn-c/60 text-trn-c',
}
export function Chip({ tone = 'neutral', children, title, className }: { tone?: Tone; children: ReactNode; title?: string; className?: string }) {
  return (
    <span title={title} className={cx('inline-flex h-5 shrink-0 items-center gap-1 whitespace-nowrap rounded border px-1.5 text-[11px] font-medium leading-none', TONE[tone], className)}>
      {children}
    </span>
  )
}
export function ClassChip({ cls }: { cls: string }) {
  const map: Record<string, [Tone, string, string]> = {
    A: ['a', 'Class A', 'Established relation (cited)'], B: ['b', 'Class B', 'Derived by the team; validation route exists'],
    C: ['c', 'Class C', 'New closure: hypothesis, unvalidated'], SYSTEM: ['neutral', 'System', 'System setting or threshold'],
    SURROGATE: ['muted', 'Surrogate', 'Not in the repo: labelled stand-in or proposal'], data: ['neutral', 'Data', 'Data-driven model (no physics class)'],
  }
  const [tone, label, title] = map[cls] ?? map.SYSTEM
  return <Chip tone={tone} title={title}>{label}</Chip>
}
export function OriginChip({ origin }: { origin: string }) {
  const tone: Tone = origin === 'LIVE' ? 'advisory' : origin === 'REAL-OOF' ? 'b' : origin === 'REPLAYED' ? 'a' : 'muted'
  const label = origin === 'REAL-OOF' ? 'Real model score' : origin.charAt(0) + origin.slice(1).toLowerCase()
  const title = origin === 'REAL-OOF' ? 'Score of the real trained model on a real image (out-of-fold), placed in a synthetic scenario' : undefined
  return <Chip tone={tone} title={title}>{label}</Chip>
}
export function StatusChip({ status }: { status: 'IMPLEMENTED' | 'SIMULATED' | 'PLANNED' | string }) {
  const tone: Tone = status === 'IMPLEMENTED' ? 'b' : status === 'PLANNED' ? 'muted' : 'a'
  return <Chip tone={tone}>{status.charAt(0) + status.slice(1).toLowerCase()}</Chip>
}
export function ClaimChip({ level, title }: { level: 'C0' | 'C1' | 'C2' | 'C3' | 'C4'; title?: string }) {
  const text = { C0: 'not addressed', C1: 'design only', C2: 'implemented, untested', C3: 'implemented and measured by us', C4: 'matches a published result' }[level]
  return <Chip tone={level === 'C3' || level === 'C4' ? 'b' : 'muted'} title={title ?? text}>{level} · {text}</Chip>
}

const SEV = ['normal', 'watch', 'warning', 'emergency'] as const
export function SevShape({ level, size = 12, hollow = false }: { level: number; size?: number; hollow?: boolean }) {
  const color = ['var(--trn-text3)', 'var(--trn-watch)', 'var(--trn-warning)', 'var(--trn-emergency)'][level]
  const fill = hollow ? 'none' : color
  const sw = hollow ? 2 : 0
  return (
    <svg width={size} height={size} viewBox="0 0 12 12" aria-hidden className="shrink-0">
      {level <= 1 && <circle cx="6" cy="6" r={level ? 4.6 : 3} fill={fill} stroke={color} strokeWidth={sw} />}
      {level === 2 && <path d="M6 0.6 L11.4 6 L6 11.4 L0.6 6Z" fill={fill} stroke={color} strokeWidth={sw} />}
      {level === 3 && <path d="M3.8 0.8 H8.2 L11.2 3.8 V8.2 L8.2 11.2 H3.8 L0.8 8.2 V3.8Z" fill={fill} stroke={color} strokeWidth={sw} />}
    </svg>
  )
}
export function SevBadge({ level, label, hollow }: { level: number; label: string; hollow?: boolean }) {
  const tone = (['muted', 'watch', 'warning', 'emergency'] as Tone[])[level]
  return <Chip tone={tone}><SevShape level={level} size={10} hollow={hollow} />{label}</Chip>
}
export const sevName = (l: number) => SEV[l]

export function Button({ variant = 'default', className, ...p }: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'default' | 'primary' | 'ghost' | 'danger' }) {
  const v = {
    default: 'border border-trn-line bg-trn-raised text-trn-text hover:border-trn-text3',
    primary: 'border border-trn-brand bg-trn-brand text-[#160b05] hover:bg-trn-brand2',
    ghost: 'border border-transparent text-trn-text2 hover:bg-trn-raised hover:text-trn-text',
    danger: 'border border-trn-emergency/70 text-trn-emergency hover:bg-trn-emergency/10',
  }[variant]
  return <button type="button" {...p} className={cx('inline-flex h-8 items-center justify-center gap-1.5 rounded px-3 text-[13px] font-medium transition-colors duration-150 disabled:cursor-not-allowed disabled:opacity-40', v, className)} />
}
export function IconButton({ label, className, ...p }: ButtonHTMLAttributes<HTMLButtonElement> & { label: string }) {
  return <button type="button" aria-label={label} title={label} {...p} className={cx('inline-flex h-8 w-8 items-center justify-center rounded text-trn-text2 transition-colors duration-150 hover:bg-trn-raised hover:text-trn-text', className)} />
}
export function Tabs<T extends string>({ value, onChange, items }: { value: T; onChange: (v: T) => void; items: { id: T; label: string; badge?: ReactNode }[] }) {
  return (
    <div role="tablist" className="flex border-b border-trn-line">
      {items.map((it) => (
        <button key={it.id} role="tab" aria-selected={value === it.id} onClick={() => onChange(it.id)}
          className={cx('relative flex h-10 flex-1 items-center justify-center gap-1.5 px-2 text-[13px] font-medium transition-colors duration-150',
            value === it.id ? 'text-trn-text' : 'text-trn-text3 hover:text-trn-text2')}>
          {it.label}{it.badge}
          {value === it.id && <span className="absolute inset-x-3 bottom-0 h-0.5 rounded bg-trn-gold" />}
        </button>
      ))}
    </div>
  )
}
export function Section({ title, right, children, className }: { title: ReactNode; right?: ReactNode; children: ReactNode; className?: string }) {
  return (
    <section className={cx('border-b border-trn-line px-4 py-3', className)}>
      <div className="mb-2 flex items-center justify-between gap-2">
        <h3 className="text-[13px] font-semibold text-trn-text">{title}</h3>
        {right}
      </div>
      {children}
    </section>
  )
}
export function Stat({ label, value, sub, tone }: { label: string; value: ReactNode; sub?: ReactNode; tone?: 'emergency' | 'warning' | 'advisory' | 'neutral' }) {
  const c = tone === 'emergency' ? 'text-trn-emergency' : tone === 'warning' ? 'text-trn-warning' : tone === 'advisory' ? 'text-trn-advisory' : 'text-trn-text'
  return (
    <div className="min-w-0">
      <div className="truncate text-[11px] font-medium text-trn-text3">{label}</div>
      <div className={cx('num font-trn-display text-[20px] font-semibold leading-6', c)}>{value}</div>
      {sub && <div className="num truncate text-[11px] text-trn-text3">{sub}</div>}
    </div>
  )
}
export function Toggle({ checked, onChange, label }: { checked: boolean; onChange: (v: boolean) => void; label: string }) {
  return (
    <label className="flex cursor-pointer items-center justify-between gap-3 py-1 text-[13px] text-trn-text2">
      <span>{label}</span>
      <button type="button" role="switch" aria-checked={checked} onClick={() => onChange(!checked)}
        className={cx('relative h-5 w-9 shrink-0 rounded-full border transition-colors duration-150', checked ? 'border-trn-brand bg-trn-brand/80' : 'border-trn-line bg-trn-raised')}>
        <span className={cx('absolute top-0.5 h-3.5 w-3.5 rounded-full bg-trn-text transition-transform duration-150', checked ? 'translate-x-4' : 'translate-x-0.5')} />
      </button>
    </label>
  )
}
export function Kbd({ children }: { children: ReactNode }) {
  return <kbd className="rounded border border-trn-line bg-trn-raised px-1.5 py-0.5 font-trn-mono text-[11px] text-trn-text2">{children}</kbd>
}
