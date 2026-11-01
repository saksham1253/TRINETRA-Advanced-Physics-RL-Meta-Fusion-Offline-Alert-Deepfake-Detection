import { C, Card, Chip, Slide, Src } from './ui'

const WHO: [string, string][] = [
  ['SDMA control rooms', 'one screen: risk + reasons + "how sure", approve in one click'],
  ['Hill districts (Uttarakhand, Himachal, Sikkim)', 'landslide + glacial-lake watch that works without labels'],
  ['Cities and campuses', 'CCTV fire/smoke with fewer false alarms'],
  ['Fact-check desks', 'flag fake disaster videos before they go viral'],
]

const ROAD: [string, string, string][] = [
  ['Now', 'Phase 2 Kaggle results: fire, zero-shot, fake media, satellite, fusion (3 seeds)', 'PENDING'],
  ['3 months', 'Shadow-mode pilot with an SDMA: TRINETRA advises and logs, officers decide', 'PLANNED'],
  ['6 months', 'Cyclone module (IBTrACS + INSAT-3D), IMERG 0.1° rain, Indian InSAR frames', 'PLANNED'],
  ['12 months', 'Field LoRa nodes on 2–3 landslide-prone slopes; SACHET-compatible CAP feed', 'PLANNED'],
]

export function Slide7() {
  return (
    <Slide n={7} title="Who it helps, what comes next, and the rules we never break." sub="From a research prototype to a shadow-mode pilot, earning trust one measured result at a time.">
      <div className="grid h-full grid-cols-12 grid-rows-[1fr_auto] gap-[18px]">
        <Card title="Who it helps" className="col-span-4" accent={C.teal}>
          <div className="flex h-full flex-col gap-[12px]">
            {WHO.map(([t, d]) => (
              <div key={t} className="flex flex-1 flex-col justify-center rounded-[12px] px-[16px] py-[10px]" style={{ background: C.well }}>
                <b style={{ fontSize: 23 }}>{t}</b>
                <div style={{ fontSize: 19, color: C.dim }}>{d}</div>
              </div>
            ))}
          </div>
        </Card>
        <Card title="Roadmap" className="col-span-5" accent={C.blue}>
          <div className="flex h-full flex-col gap-[12px]">
            {ROAD.map(([when, what, k], i) => (
              <div key={when} className="flex flex-1 items-stretch gap-[14px]">
                <div className="flex w-[110px] shrink-0 flex-col items-center">
                  <span className="whitespace-nowrap rounded-full px-[12px] py-[4px] font-bold" style={{ background: i === 0 ? C.ember : C.ink, color: '#FFF3D6', fontSize: 17 }}>{when}</span>
                  {i < ROAD.length - 1 && <span className="mt-[4px] w-[3px] flex-1" style={{ background: '#F1B79A' }} />}
                </div>
                <div className="flex flex-1 items-center justify-between gap-[10px] rounded-[12px] px-[16px] py-[10px]" style={{ background: C.well }}>
                  <span style={{ fontSize: 21 }}>{what}</span>
                  <Chip k={k} />
                </div>
              </div>
            ))}
          </div>
        </Card>
        <Card title="Rules we never break" className="col-span-3" accent={C.red}>
          <ul className="flex h-full flex-col justify-around gap-[12px]" style={{ fontSize: 22 }}>
            <li><b>Human approves</b> every public alert (enforced in code)</li>
            <li><b>Complements</b> IMD / NDMA warnings and certified alarms, never replaces them</li>
            <li><b>No raw video</b> leaves the site</li>
            <li><b>No invented numbers:</b> pending results stay "pending"</li>
            <li><b>Licences credited;</b> simulated data is labelled</li>
          </ul>
        </Card>
        <div className="col-span-12 flex items-center justify-between gap-[24px] rounded-[18px] px-[28px] py-[18px]" style={{ background: C.ink, color: '#FFF3D6' }}>
          <span className="font-bold" style={{ fontSize: 34, letterSpacing: -0.5 }}>
            TRINETRA: <span style={{ color: '#FFD54A' }}>see early · check with physics · warn honestly, even offline.</span>
          </span>
          <span className="text-right" style={{ fontSize: 17 }}>
            Team SANKAT MOCHAK · GEHU Dehradun<br />
            <Src><span style={{ color: '#F5D27A' }}>github.com/saksham1253/TRINETRA-CONTENT-OG</span></Src>
          </span>
        </div>
      </div>
    </Slide>
  )
}
