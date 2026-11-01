import { C, Card, Chip, N, Slide, Src, Step } from './ui'

const EX = [
  { e: 'CCTV fire detector', p: 0.8, w: 0.603, note: 'reliable, fairly sure' },
  { e: 'Smoke / heat sensor', p: 0.6, w: 0.655, note: 'reliable, very sure' },
  { e: 'Viral video check', p: 0.1, w: 0.147, note: 'low trust, unsure' },
]

function Example() {
  return (
    <div className="flex h-full flex-col justify-between gap-[14px]">
      {EX.map((x) => (
        <div key={x.e} className="grid grid-cols-[230px_1fr_215px] items-center gap-[14px]">
          <div>
            <div style={{ fontSize: 19, fontWeight: 600 }}>{x.e}</div>
            <div style={{ fontSize: 15, color: C.dim }}>{x.note}</div>
          </div>
          <div className="h-[34px] rounded-full" style={{ background: '#F6DCC4' }}>
            <div className="h-full rounded-full" style={{ width: `${x.p * 100}%`, background: C.ember, opacity: 0.35 + x.w }} />
          </div>
          <span className="font-mono" style={{ fontSize: 18 }}>p {x.p} · w {x.w}</span>
        </div>
      ))}
      <div className="grid grid-cols-[230px_1fr_215px] items-center gap-[14px] rounded-[12px] py-[12px]" style={{ background: '#FDE3D3' }}>
        <b style={{ fontSize: 21, paddingLeft: 10 }}>Fused risk</b>
        <div className="relative h-[32px] rounded-full" style={{ background: '#F6DCC4' }}>
          <div className="h-full rounded-full" style={{ width: '63.35%', background: C.red }} />
          <div className="absolute top-[-6px] h-[44px] w-[3px]" style={{ left: '47.6%', background: C.ink }} />
          <span className="absolute font-mono" style={{ left: '44%', top: 34, fontSize: 13 }}>RED line</span>
        </div>
        <span className="font-bold" style={{ fontSize: 22, color: C.red }}>{N('ex_p').v} → RED</span>
      </div>
      <p style={{ fontSize: 19, color: C.dim, marginTop: 14 }}>
        The doubtful video barely counts (weight 0.147), so it cannot cancel two trustworthy sources. If the experts had disagreed strongly,
        the uncertainty U* would pass 0.6 and the screen would say <b style={{ color: C.ink }}>"needs human review"</b> instead of guessing.
      </p>
      <Src>worked example computed with ws5_fusion_rl code, not a field result</Src>
    </div>
  )
}

export function Slide4() {
  return (
    <Slide n={4} title="How one alert is made, in plain words." sub="Many eyes give an opinion, physics checks it, the system says how sure it is, and a human signs off.">
      <div className="grid h-full grid-cols-12 grid-rows-[auto_1fr] gap-[18px]">
        <div className="col-span-12 flex gap-[14px]">
          <Step n="1" t="Collect" d="camera frames, rain, slope, satellite, posts" col={C.blue} />
          <Step n="2" t="Each expert scores" d="risk 0–1 plus how unsure it is" col={C.ember} />
          <Step n="3" t="Physics check" d="can this really happen? e.g. is the slope wet enough to fail?" col={C.blue} />
          <Step n="4" t="Fuse" d="trust-weighted average; unreliable or missing experts count less" col={C.teal} />
          <Step n="5" t="Decide level" d={<>GREEN · YELLOW · ORANGE · RED from the cost of a miss vs a false alarm</>} col={C.amber} />
          <Step n="6" t="Human approves" d="only then a CAP alert goes out" col={C.red} />
        </div>
        <Card title="Example: three sources disagree about a fire" className="col-span-7" accent={C.ember} right={<Chip k="C2" />}>
          <Example />
        </Card>
        <Card title="Example: physics for a landslide" className="col-span-5" accent={C.blue} right={<Chip k="C3" />}>
          <div className="flex flex-col gap-[12px]">
            <div className="flex flex-wrap items-center gap-[8px]" style={{ fontSize: 18 }}>
              {['Heavy rain', 'water enters soil', 'pore pressure ↑', 'slope strength ↓', 'FS < 1 ⇒ slide'].map((t, i, a) => (
                <span key={t} className="flex items-center gap-[8px]">
                  <span className="rounded-[10px] px-[10px] py-[6px] text-center" style={{ background: C.well, border: `2px solid ${C.blue}` }}>{t}</span>
                  {i < a.length - 1 && <span style={{ color: C.blue, fontSize: 22 }}>→</span>}
                </span>
              ))}
            </div>
            <p style={{ fontSize: 19 }}>
              FS (factor of safety) = what holds the slope ÷ what pulls it down. Below 1, the slope can fail. The physics shield can only <b>raise</b> an alert level, never hide one.
            </p>
            <div className="grid grid-cols-2 gap-[14px]">
              <div className="rounded-[12px] p-[12px]" style={{ background: C.well }}>
                <div className="font-bold" style={{ fontSize: 42, color: C.teal }}>{N('auc_caine').v}</div>
                <div style={{ fontSize: 16 }}>AUC of the rain-threshold physics, <b>no training</b>, {N('geo_events').v} real landslides</div>
              </div>
              <div className="rounded-[12px] p-[12px]" style={{ background: C.well }}>
                <div className="font-bold" style={{ fontSize: 42, color: C.ink }}>{N('auc_rain').v}</div>
                <div style={{ fontSize: 16 }}>trained rain-only model. Physics is almost as good with zero labels, so it works in a new district on day one</div>
              </div>
            </div>
            <div className="rounded-[12px] p-[12px]" style={{ background: C.well }}>
              <b style={{ fontSize: 18 }}>Alert levels from cost, not guesswork</b>
              <div className="mt-[8px] grid grid-cols-4 gap-[8px] text-center font-bold" style={{ fontSize: 16 }}>
                <span className="rounded-[8px] py-[6px]" style={{ background: '#DCFCE7', color: '#14532D' }}>GREEN<br />&lt; {N('pstar').v}</span>
                <span className="rounded-[8px] py-[6px]" style={{ background: '#FEF9C3', color: '#713F12' }}>YELLOW<br />≥ p*</span>
                <span className="rounded-[8px] py-[6px]" style={{ background: '#FFEDD5', color: '#7C2D12' }}>ORANGE<br />≥ 4p*</span>
                <span className="rounded-[8px] py-[6px]" style={{ background: '#FEE2E2', color: '#7F1D1D' }}>RED<br />≥ 10p*</span>
              </div>
              <div style={{ fontSize: 15, color: C.dim, marginTop: 6 }}>p* = cost of false alarm ÷ (false alarm + miss) = 5 ÷ 105</div>
            </div>
            <Src>results/geo_large · NASA landslide catalog + NASA POWER rain + Copernicus DEM · spatial cross-validation</Src>
          </div>
        </Card>
      </div>
    </Slide>
  )
}
