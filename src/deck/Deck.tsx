import { useEffect, useState } from 'react'
import { SlideTitle } from './SlideTitle'
import { Slide1 } from './Slide1'
import { Slide2 } from './Slide2'
import { Slide3 } from './Slide3'
import { Slide4 } from './Slide4'
import { Slide5 } from './Slide5'
import { Slide6 } from './Slide6'
import { Slide7 } from './Slide7'
import { NOTES } from './notes'
import { C } from './ui'

const SLIDES = [SlideTitle, Slide1, Slide2, Slide3, Slide4, Slide5, Slide6, Slide7]
const LAST = SLIDES.length - 1

function useScale(notes: boolean) {
  const [s, setS] = useState(1)
  useEffect(() => {
    const f = () => {
      const h = window.innerHeight - (notes ? 260 : 64)
      setS(Math.min((window.innerWidth - 32) / 1920, h / 1080))
    }
    f()
    window.addEventListener('resize', f)
    return () => window.removeEventListener('resize', f)
  }, [notes])
  return s
}

export default function Deck() {
  const [i, setI] = useState(() => Math.max(0, Math.min(LAST, Number(new URLSearchParams(location.hash.split('?')[1]).get('s') ?? 0))))
  const [notes, setNotes] = useState(false)
  const scale = useScale(notes)
  useEffect(() => {
    const k = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') setI((v) => Math.min(LAST, v + 1))
      if (e.key === 'ArrowLeft' || e.key === 'PageUp') setI((v) => Math.max(0, v - 1))
      if (e.key.toLowerCase() === 'n') setNotes((v) => !v)
    }
    window.addEventListener('keydown', k)
    return () => window.removeEventListener('keydown', k)
  }, [])
  const S = SLIDES[i]
  const n = NOTES[i]
  if (location.hash.startsWith('#deck-raw')) return <S />
  return (
    <div className="deck-root min-h-screen" style={{ background: '#0B1238', color: '#FFF3D6' }}>
      <div className="deck-screen flex flex-col items-center gap-[12px] p-[16px]">
        <div style={{ width: 1920 * scale, height: 1080 * scale }} className="overflow-hidden rounded-[10px] shadow-2xl">
          <div style={{ transform: `scale(${scale})`, transformOrigin: 'top left' }}>
            <S />
          </div>
        </div>
        <div className="flex w-full max-w-[1400px] items-center justify-between gap-3 text-sm" style={{ color: '#F5D27A' }}>
          <div className="flex items-center gap-2">
            <button className="rounded border px-3 py-1" style={{ borderColor: '#3A4A8A' }} onClick={() => setI((v) => Math.max(0, v - 1))}>← Prev</button>
            <span className="font-mono">{i === 0 ? 'Title' : `${i} / 7`}</span>
            <button className="rounded border px-3 py-1" style={{ borderColor: '#3A4A8A' }} onClick={() => setI((v) => Math.min(LAST, v + 1))}>Next →</button>
          </div>
          <div className="flex items-center gap-2">
            <button className="rounded border px-3 py-1" style={{ borderColor: '#3A4A8A' }} onClick={() => setNotes((v) => !v)}>{notes ? 'Hide' : 'Show'} notes (N)</button>
            <button className="rounded border px-3 py-1" style={{ borderColor: '#3A4A8A' }} onClick={() => window.print()}>Export PDF (print)</button>
            <a className="rounded border px-3 py-1" style={{ borderColor: '#3A4A8A' }} href="#">Dashboard</a>
          </div>
        </div>
        {notes && (
          <div className="grid w-full max-w-[1400px] grid-cols-[1.4fr_1fr] gap-4 rounded-lg p-4 text-[15px] leading-relaxed" style={{ background: '#FFF7EE', color: C.ink, border: `1px solid ${C.line}` }}>
            <p>{n.talk}</p>
            <ul className="flex flex-col gap-2">
              {n.qa.map(([q, a]) => (
                <li key={q}><b>Q: {q}</b><br /><span style={{ color: C.dim }}>{a}</span></li>
              ))}
            </ul>
          </div>
        )}
      </div>
      <div className="deck-print">
        {SLIDES.map((P, k) => (
          <div key={k} className="deck-page"><P /></div>
        ))}
      </div>
    </div>
  )
}
