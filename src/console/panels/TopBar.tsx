import { useEffect, useMemo, useState } from 'react'
import { Info, Moon, Search, Settings, Sun, Presentation, Wifi, WifiOff, RadioTower, Antenna } from 'lucide-react'
import { useStore, type Mode, type Lang, type Role } from '../store'
import { useT } from '../i18n'
import { Chip, IconButton, cx } from '../ui/primitives'
import { currentScenario, useTowns } from '../useEngine'
import { networkDown } from '../derived'
import { mapRef } from '../map/MapView'
import regions from '../data/regions.json'
import { useMesh } from '../lora/useMesh'

export function Logo() {
  return (
    <svg width="28" height="28" viewBox="0 0 28 28" aria-hidden>
      <path className="logo-arc" d="M4 15 Q14 4 24 15" fill="none" stroke="var(--trn-brand)" strokeWidth="2.2" strokeLinecap="round" />
      <path className="logo-arc" d="M7 17.5 Q14 10 21 17.5" fill="none" stroke="var(--trn-brand-bright)" strokeWidth="2" strokeLinecap="round" style={{ animationDelay: '120ms' }} />
      <circle className="logo-arc" cx="14" cy="18.5" r="2.6" fill="var(--trn-gold)" style={{ animationDelay: '240ms' }} />
    </svg>
  )
}

function Clock() {
  const [now, setNow] = useState(() => new Date())
  useEffect(() => { const id = setInterval(() => setNow(new Date()), 1000); return () => clearInterval(id) }, [])
  const ist = now.toLocaleTimeString('en-GB', { timeZone: 'Asia/Kolkata', hour12: false })
  return <span className="num shrink-0 whitespace-nowrap font-trn-mono text-[12px] text-trn-text2" title={`UTC ${now.toISOString().slice(11, 19)}`}>{ist.slice(0, 5)} IST</span>
}

function parseLatLon(q: string): [number, number] | null {
  const m = q.trim().match(/^(-?\d+(?:\.\d+)?)\s*[, ]\s*(-?\d+(?:\.\d+)?)$/)
  if (!m) return null
  const a = parseFloat(m[1]), b = parseFloat(m[2])
  if (Math.abs(a) <= 90 && Math.abs(b) <= 180) return [b, a]
  return null
}

function SearchBox() {
  const t = useT()
  const [q, setQ] = useState('')
  const [open, setOpen] = useState(false)
  const towns = useTowns((s) => s.towns)
  const hits = useMemo(() => {
    const s = q.trim().toLowerCase()
    if (s.length < 2) return []
    const ll = parseLatLon(q)
    const out: { label: string; sub: string; lon: number; lat: number; zoom: number }[] = []
    if (ll) out.push({ label: `${ll[1].toFixed(4)}, ${ll[0].toFixed(4)}`, sub: 'Coordinates (lat, lon)', lon: ll[0], lat: ll[1], zoom: 12 })
    for (const r of regions.regions) if (r.name.toLowerCase().includes(s)) out.push({ label: r.name, sub: 'Demo region (cached terrain)', lon: (r.bbox[0] + r.bbox[2]) / 2, lat: (r.bbox[1] + r.bbox[3]) / 2, zoom: 10 })
    for (const tw of towns) { if (out.length > 8) break; if (tw[0].toLowerCase().startsWith(s)) out.push({ label: tw[0], sub: `${tw[3]} · GeoNames`, lon: tw[2], lat: tw[1], zoom: 11 }) }
    return out
  }, [q, towns])
  const go = (h: (typeof hits)[number]) => { mapRef.current?.flyTo({ center: [h.lon, h.lat], zoom: h.zoom, pitch: 55, duration: 2200 }); setOpen(false); setQ(h.label) }
  return (
    <div className="relative w-[260px] shrink max-[1700px]:w-[200px]">
      <Search size={15} className="pointer-events-none absolute top-1/2 left-2.5 -translate-y-1/2 text-trn-text3" />
      <input value={q} onChange={(e) => { setQ(e.target.value); setOpen(true) }} onFocus={() => setOpen(true)} onBlur={() => setTimeout(() => setOpen(false), 150)}
        onKeyDown={(e) => { if (e.key === 'Enter' && hits[0]) go(hits[0]) }} placeholder={t('search')} aria-label={t('search')}
        className="h-8 w-full rounded border border-trn-line bg-trn-raised pr-2 pl-8 text-[13px] text-trn-text placeholder:text-trn-text3 focus:border-trn-gold focus:outline-none" />
      {open && hits.length > 0 && (
        <ul className="absolute top-9 z-50 w-full overflow-hidden rounded border border-trn-line bg-trn-surface shadow-[0_8px_24px_rgba(0,0,0,.45)]">
          {hits.map((h, i) => (
            <li key={i}><button onMouseDown={() => go(h)} className="flex w-full items-baseline justify-between gap-2 px-3 py-2 text-left hover:bg-trn-raised">
              <span className="truncate text-[13px] text-trn-text">{h.label}</span><span className="truncate text-[11px] text-trn-text3">{h.sub}</span>
            </button></li>
          ))}
        </ul>
      )}
    </div>
  )
}

function Seg<T extends string>({ value, items, onChange, label }: { value: T; items: { id: T; label: string }[]; onChange: (v: T) => void; label: string }) {
  return (
    <div role="radiogroup" aria-label={label} className="flex h-8 shrink-0 overflow-hidden rounded border border-trn-line">
      {items.map((it) => (
        <button key={it.id} role="radio" aria-checked={value === it.id} onClick={() => onChange(it.id)}
          className={cx('whitespace-nowrap px-2 text-[12px] font-medium transition-colors duration-150', value === it.id ? 'bg-trn-raised text-trn-text' : 'text-trn-text3 hover:text-trn-text2')}>{it.label}</button>
      ))}
    </div>
  )
}

export default function TopBar() {
  const t = useT()
  const s = useStore()
  const sc = currentScenario()
  const down = networkDown(sc, s.simMin, s.outage)
  const mesh = useMesh((m) => m.mesh)
  const modeTone = s.mode === 'LIVE' ? 'advisory' : s.mode === 'REPLAY' ? 'a' : 'gold'
  const modeLabel = { SIM: t('sim'), REPLAY: t('replay'), LIVE: t('live') }[s.mode]
  return (
    <header className="no-print flex h-14 shrink-0 items-center gap-3 border-b border-trn-line bg-trn-surface px-3">
      <div className="flex items-center gap-2.5 pr-2">
        <Logo />
        <div className="leading-tight">
          <div className="font-trn-display text-[15px] font-semibold tracking-wide text-trn-text">TRINETRA</div>
          <div className="whitespace-nowrap text-[11px] text-trn-text3 max-[1800px]:hidden">{t('appTitle').replace('TRINETRA ', '')} · {t('team')}</div>
        </div>
      </div>
      <Chip tone={modeTone} title="Data origin of everything on screen"><span className="font-semibold">Mode</span> {modeLabel}</Chip>
      <Chip tone="warning" title={t('prototype')}><span className="max-[1500px]:hidden">{t('prototype')}</span><span className="min-[1501px]:hidden">Prototype: not field-validated</span></Chip>
      <div className="mx-1 h-6 w-px bg-trn-line" />
      <div className="flex items-center gap-1.5" aria-label="Network status">
        <Chip tone={down ? 'emergency' : 'neutral'}>{down ? <WifiOff size={12} /> : <Wifi size={12} />}<span className="max-[1600px]:hidden">{t('internet')}</span> {down ? 'down' : 'up'}</Chip>
        <Chip tone={down ? 'emergency' : 'neutral'}><Antenna size={12} /><span className="max-[1600px]:hidden">{t('cellular')}</span> {down ? 'down' : 'up'}</Chip>
        <Chip tone={mesh ? 'advisory' : 'muted'} title="LoRa mesh (simulated radio on real terrain)"><RadioTower size={12} />LoRa {mesh ? (down ? 'carrying alerts' : 'standby') : 'idle'}</Chip>
      </div>
      <div className="flex-1" />
      <SearchBox />
      <Clock />
      <Seg<Mode> label="Mode" value={s.mode} onChange={(m) => s.set({ mode: m, settings: m === 'LIVE' ? true : s.settings })}
        items={[{ id: 'SIM', label: 'Sim' }, { id: 'REPLAY', label: 'Replay' }, { id: 'LIVE', label: 'Live' }]} />
      <Seg<Lang> label="Language" value={s.lang} onChange={(l) => s.set({ lang: l })} items={[{ id: 'en', label: 'EN' }, { id: 'hi', label: 'हिंदी' }, { id: 'hinglish', label: 'HG' }]} />
      <select aria-label="Role" value={s.role} onChange={(e) => s.set({ role: e.target.value as Role })}
        className="h-8 shrink-0 rounded border border-trn-line bg-trn-raised px-2 text-[12px] text-trn-text2 max-[1700px]:hidden">
        {(['Operator', 'Supervisor', 'Analyst', 'Viewer'] as Role[]).map((r) => <option key={r}>{r}</option>)}
      </select>
      <IconButton label="Briefing mode" onClick={() => s.set({ briefing: !s.briefing })} className={s.briefing ? 'text-trn-gold' : ''}><Presentation size={17} /></IconButton>
      <IconButton label={s.theme === 'dark' ? 'Light theme (projector)' : 'Dark theme'} onClick={() => s.set({ theme: s.theme === 'dark' ? 'light' : 'dark' })}>
        {s.theme === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
      </IconButton>
      <IconButton label="Settings and live model" onClick={() => s.set({ settings: true })}><Settings size={17} /></IconButton>
      <IconButton label="About, methods and data sources" onClick={() => s.set({ about: true })}><Info size={17} /></IconButton>
    </header>
  )
}
