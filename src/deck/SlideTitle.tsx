import { C, Chip, N } from './ui'

function Rings() {
  return (
    <svg className="absolute" style={{ right: -260, top: -220 }} width="1300" height="1300" viewBox="0 0 1300 1300" aria-hidden>
      {Array.from({ length: 9 }, (_, i) => (
        <circle key={i} cx="650" cy="650" r={170 + i * 62} fill="none" stroke="rgba(16,26,74,0.13)" strokeWidth={i % 3 === 0 ? 2.4 : 1.2} />
      ))}
    </svg>
  )
}

function HeroEye() {
  return (
    <svg width="500" height="300" viewBox="0 0 50 30" aria-label="Trinetra, the third eye">
      <defs>
        <radialGradient id="iris" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#FFE07A" />
          <stop offset="70%" stopColor="#C2410C" />
          <stop offset="100%" stopColor="#7A1405" />
        </radialGradient>
      </defs>
      <path d="M1.5 15 Q25 -7 48.5 15 Q25 37 1.5 15 Z" fill="#FFF7EE" stroke="#101A4A" strokeWidth="1.4" />
      <circle cx="25" cy="15" r="8.6" fill="url(#iris)" stroke="#101A4A" strokeWidth="1" />
      <circle cx="25" cy="15" r="3.4" fill="#101A4A" />
      <circle cx="25" cy="15" r="11.2" fill="none" stroke="#F2B705" strokeWidth="0.7" strokeDasharray="1.2 1.2" />
      <circle cx="22.6" cy="12.6" r="1.4" fill="#FFF7EE" />
    </svg>
  )
}

const THREE = [
  ['01', 'It sees', 'cameras, satellites, rain, sensors and news, together'],
  ['02', 'It checks with physics', 'is this alarm physically possible? rain → soil → slope'],
  ['03', 'It knows how sure it is', 'unsure ⇒ a human decides; alerts still work offline'],
]

export function SlideTitle() {
  return (
    <div
      className="deck-slide relative overflow-hidden"
      style={{ width: 1920, height: 1080, background: 'linear-gradient(125deg, #FFB347 0%, #F57C1F 40%, #E04A1B 76%, #C2301A 100%)', color: C.ink, fontFamily: '"IBM Plex Sans", Inter, system-ui, sans-serif' }}
    >
      <Rings />
      <span aria-hidden className="pointer-events-none absolute select-none font-bold" style={{ left: 40, bottom: -150, fontSize: 470, lineHeight: 1, color: 'rgba(16,26,74,0.10)', fontFamily: '"Noto Sans Devanagari", "Nirmala UI", "Kohinoor Devanagari", Mangal, sans-serif' }}>
        त्रिनेत्र
      </span>
      <div aria-hidden className="absolute left-0 right-0 top-0" style={{ height: 14, background: C.ink, borderBottom: `5px solid ${C.gold}` }} />
      <div className="relative flex h-full flex-col px-[72px] py-[56px]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-[14px]">
            <span className="rounded-full px-[18px] py-[6px] font-bold uppercase" style={{ fontSize: 20, letterSpacing: 2, background: C.ink, color: '#FFD54A' }}>Phase 2</span>
            <span className="font-mono uppercase" style={{ fontSize: 19, letterSpacing: 3, color: C.onOrange }}>SAARTHI26 · Disaster Resilience</span>
          </div>
          <span className="font-mono" style={{ fontSize: 18, color: C.onOrange }}>research prototype · advisory system</span>
        </div>

        <div className="mt-[54px] grid grid-cols-[1.5fr_1fr] items-center gap-[30px]">
          <div>
            <div className="font-mono uppercase" style={{ fontSize: 22, letterSpacing: 7, color: C.onOrange }}>tri + netra · the third eye</div>
            <h1 className="font-black" style={{ fontSize: 204, lineHeight: 0.88, letterSpacing: -7, marginTop: 10 }}>TRINETRA</h1>
            <p className="font-bold" style={{ fontSize: 56, lineHeight: 1.08, letterSpacing: -1.2, marginTop: 26, maxWidth: 1080 }}>
              The third eye that sees a disaster <span style={{ background: C.ink, color: '#FFD54A', padding: '0 14px', borderRadius: 10 }}>before it strikes.</span>
            </p>
            <p style={{ fontSize: 27, lineHeight: 1.35, marginTop: 22, maxWidth: 1040, color: C.onOrange }}>
              One early-warning system for India's fire, landslide, flood and glacial-lake hazards that also catches fake disaster videos.
              It checks every alarm with physics and keeps warning people even when the internet is down.
            </p>
          </div>
          <div className="flex flex-col items-center gap-[18px]">
            <HeroEye />
            <div className="rounded-[16px] px-[22px] py-[14px] text-center" style={{ background: 'rgba(16,26,74,0.93)', color: '#FFF3D6' }}>
              <div className="font-bold tabular-nums" style={{ fontSize: 46, lineHeight: 1 }}>3,238</div>
              <div style={{ fontSize: 18, marginTop: 6 }}>lives lost to extreme weather in India, Jan–Sep 2024</div>
              <div className="font-mono" style={{ fontSize: 13, color: '#F5D27A', marginTop: 4 }}>CSE / Down To Earth, State of Extreme Weather 2024</div>
            </div>
          </div>
        </div>

        <div className="mt-[40px] grid grid-cols-3 gap-[18px]">
          {THREE.map(([n, t, d]) => (
            <div key={n} className="rounded-[16px] px-[22px] py-[16px]" style={{ background: C.panel, boxShadow: '0 10px 30px rgba(16,26,74,0.22)' }}>
              <div className="flex items-baseline gap-[12px]">
                <span className="font-mono font-bold" style={{ fontSize: 22, color: C.ember }}>{n}</span>
                <span className="font-bold" style={{ fontSize: 29 }}>{t}</span>
              </div>
              <p style={{ fontSize: 19, color: C.dim, marginTop: 4 }}>{d}</p>
            </div>
          ))}
        </div>

        <div className="mt-auto flex items-end justify-between gap-[24px]">
          <div>
            <div className="flex items-center gap-[12px]">
              <span className="whitespace-nowrap rounded-full px-[14px] py-[4px] font-bold uppercase" style={{ fontSize: 20, letterSpacing: 2, background: C.ink, color: C.goldSoft }}>Team SANKAT MOCHAK</span>
              <span className="whitespace-nowrap font-semibold" style={{ fontSize: 20 }}>the remover of crises · Graphic Era Hill University, Dehradun</span>
            </div>
            <div className="mt-[6px] flex flex-wrap items-baseline gap-x-[26px]" style={{ fontSize: 25 }}>
              <span><b>Saksham Aggarwal</b> <span style={{ fontSize: 17, color: C.onOrange }}>team leader</span></span>
              <span>Utkarsh Saini</span>
              <span>Mohit Kaintura</span>
              <span>Naina Joshi</span>
            </div>
          </div>
          <div className="flex items-center gap-[22px] rounded-[16px] px-[22px] py-[12px]" style={{ background: C.panel }}>
            {([['geo_events', 'real landslides tested'], ['auc_caine', 'AUC, physics, zero training'], ['datasets', 'open datasets']] as const).map(([k, c]) => (
              <div key={k}>
                <div className="font-bold tabular-nums" style={{ fontSize: 38, lineHeight: 1 }}>{N(k).v}</div>
                <div style={{ fontSize: 15, color: C.dim }}>{c}</div>
              </div>
            ))}
            <Chip k="C3" />
          </div>
        </div>
      </div>
    </div>
  )
}
