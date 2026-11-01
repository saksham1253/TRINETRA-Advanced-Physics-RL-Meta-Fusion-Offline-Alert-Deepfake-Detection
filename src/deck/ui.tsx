import type { ReactNode } from 'react'
import numbers from './numbers.json'

type NumKey = keyof typeof numbers
export const N = (k: NumKey) => numbers[k]

// Sankat Mochak theme: Hanuman ji's sindoor + saffron background, Ram ji's neel (deep blue) for text and dark panels,
// pitambar gold only as accents on dark/neel surfaces. Every text/background pair is >= 4.5:1.
export const C = {
  bg: '#F57C1F',
  bgGrad: 'linear-gradient(135deg, #FFA53D 0%, #F57C1F 45%, #E2551B 100%)',
  panel: '#FFF8EC',
  panel2: '#FFEFD6',
  well: '#FFFFFF',
  line: '#F0C89C',
  ink: '#101A4A',
  text: '#101A4A',
  dim: '#3F4A78',
  onOrange: '#0E1640',
  ember: '#C8341A',
  red: '#B3201B',
  amber: '#8A5A00',
  gold: '#F2B705',
  goldSoft: '#FFD54A',
  teal: '#0F766E',
  blue: '#1E3A8A',
  violet: '#5B21B6',
  green: '#15803D',
}

const CHIP: Record<string, { bg: string; fg: string; label: string }> = {
  C3: { bg: '#0F766E', fg: '#FFFFFF', label: 'MEASURED BY US' },
  C2: { bg: '#1E3A8A', fg: '#FFFFFF', label: 'BUILT' },
  C1: { bg: '#E3E6F3', fg: '#101A4A', label: 'DESIGN' },
  PENDING: { bg: '#FDE68A', fg: '#5A3A00', label: 'RESULT PENDING' },
  SOURCE: { bg: '#101A4A', fg: '#FFD54A', label: 'PUBLIC REPORT' },
  VERIFY: { bg: '#FDE68A', fg: '#5A3A00', label: 'APPROX · VERIFY' },
  SIM: { bg: '#5B21B6', fg: '#FFFFFF', label: 'SIMULATOR' },
  PLANNED: { bg: '#E3E6F3', fg: '#101A4A', label: 'PLANNED' },
}

export function Chip({ k, children }: { k: string; children?: ReactNode }) {
  const s = CHIP[k] ?? { bg: C.line, fg: C.ink, label: k }
  return (
    <span
      className="inline-flex items-center whitespace-nowrap rounded-full px-[10px] py-[2px] font-semibold"
      style={{ background: s.bg, color: s.fg, fontSize: 13, lineHeight: '18px', letterSpacing: 0.4 }}
    >
      {children ?? s.label}
    </span>
  )
}

export function Src({ children }: { children: ReactNode }) {
  return (
    <span className="font-mono" style={{ fontSize: 13, color: C.dim }}>
      {children}
    </span>
  )
}

export function Card({
  title,
  children,
  className = '',
  accent = C.ember,
  right,
  pad = 18,
}: {
  title?: string
  children: ReactNode
  className?: string
  accent?: string
  right?: ReactNode
  pad?: number
}) {
  return (
    <section
      className={`flex min-h-0 flex-col overflow-hidden rounded-[18px] ${className}`}
      style={{ background: C.panel, boxShadow: '0 10px 30px rgba(16,26,74,0.20)', borderTop: `6px solid ${accent}` }}
    >
      {title && (
        <header className="flex items-center justify-between gap-3" style={{ padding: `12px ${pad}px 4px` }}>
          <h3 className="font-bold" style={{ fontSize: 24, letterSpacing: -0.2, color: C.ink }}>
            {title}
          </h3>
          {right}
        </header>
      )}
      <div className="min-h-0 flex-1" style={{ padding: `8px ${pad}px ${pad - 4}px`, fontSize: 19, lineHeight: 1.38, color: C.ink }}>
        {children}
      </div>
    </section>
  )
}

export function Stat({ v, label, src, color = C.ink, chip, size = 52 }: { v: ReactNode; label: ReactNode; src?: string; color?: string; chip?: string; size?: number }) {
  return (
    <div className="flex flex-col gap-[2px]">
      <div className="flex items-center gap-[10px]">
        <span className="whitespace-nowrap font-bold tabular-nums" style={{ fontSize: size, lineHeight: 1, color, letterSpacing: -1 }}>
          {v}
        </span>
        {chip && <Chip k={chip} />}
      </div>
      <span style={{ fontSize: 18, color: C.ink, lineHeight: 1.25 }}>{label}</span>
      {src && <Src>{src}</Src>}
    </div>
  )
}

export function Slide({ n, title, sub, children }: { n: number; title: ReactNode; sub: ReactNode; children: ReactNode }) {
  return (
    <div
      className="deck-slide relative flex flex-col overflow-hidden"
      style={{ width: 1920, height: 1080, background: C.bgGrad, color: C.ink, padding: '36px 48px 28px', fontFamily: '"IBM Plex Sans", Inter, system-ui, sans-serif' }}
    >
      <div aria-hidden className="absolute left-0 right-0 top-0" style={{ height: 10, background: C.ink, borderBottom: `4px solid ${C.gold}` }} />
      <div className="relative flex items-start justify-between gap-6">
        <div>
          <div className="mb-[6px] flex items-center gap-[12px] font-mono uppercase" style={{ fontSize: 16, letterSpacing: 3, color: C.onOrange }}>
            <span className="rounded-full px-[12px] py-[2px] font-semibold" style={{ background: C.ink, color: C.goldSoft }}>
              {String(n).padStart(2, '0')}
            </span>
            TRINETRA · Phase 2
          </div>
          <h2 className="font-bold" style={{ fontSize: 50, lineHeight: 1.05, letterSpacing: -1.2, maxWidth: 1600 }}>
            {title}
          </h2>
          <p style={{ fontSize: 22, color: C.onOrange, marginTop: 8, maxWidth: 1600 }}>{sub}</p>
        </div>
        <Eye size={84} />
      </div>
      <div className="relative mt-[20px] min-h-0 flex-1">{children}</div>
      <div className="relative mt-[14px] flex items-center justify-between gap-4" style={{ fontSize: 14, color: C.onOrange }}>
        <span className="flex items-center gap-[8px]">
          <Chip k="C3" /> <Chip k="C2" /> <Chip k="PENDING" /> <Chip k="SOURCE" />
          <span className="ml-[6px]">every number is labelled; ours come from results/ · docs/NUMBERS_REGISTER.md</span>
        </span>
        <span className="font-mono">Team SANKAT MOCHAK · GEHU Dehradun · {n}/7</span>
      </div>
    </div>
  )
}

export function Eye({ size = 34, stroke = C.ink }: { size?: number; stroke?: string }) {
  return (
    <svg width={size} height={size * 0.6} viewBox="0 0 50 30" aria-label="Trinetra eye">
      <path d="M2 15 Q25 -6 48 15 Q25 36 2 15 Z" fill="#FFF8EC" stroke={stroke} strokeWidth="2.4" />
      <circle cx="25" cy="15" r="7.5" fill={C.gold} stroke={C.ember} strokeWidth="2.4" />
      <circle cx="25" cy="15" r="3" fill={stroke} />
    </svg>
  )
}

export function Bullets({ items, size = 19, color = C.ember }: { items: ReactNode[]; size?: number; color?: string }) {
  return (
    <ul className="flex flex-col gap-[8px]" style={{ fontSize: size }}>
      {items.map((t, i) => (
        <li key={i} className="flex gap-[10px]">
          <span style={{ color }}>●</span>
          <span>{t}</span>
        </li>
      ))}
    </ul>
  )
}

export function Step({ n, t, d, col }: { n: string; t: string; d: ReactNode; col: string }) {
  return (
    <div className="flex flex-1 flex-col gap-[6px] rounded-[14px] p-[14px]" style={{ background: C.well, border: `2px solid ${col}` }}>
      <div className="flex items-center gap-[10px]">
        <span className="flex h-[34px] w-[34px] items-center justify-center rounded-full font-bold" style={{ background: col, color: '#FFFFFF', fontSize: 18 }}>
          {n}
        </span>
        <b style={{ fontSize: 21 }}>{t}</b>
      </div>
      <span style={{ fontSize: 17, color: C.dim, lineHeight: 1.3 }}>{d}</span>
    </div>
  )
}
