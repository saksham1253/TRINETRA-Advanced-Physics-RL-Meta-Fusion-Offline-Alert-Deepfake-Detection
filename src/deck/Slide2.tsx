import { C, Card, Chip, N, Slide } from './ui'

const GAPS: [string, string, string][] = [
  ['Too many false alarms', 'People stop listening.', 'Physics check + "alarm only if it persists" + cost-based thresholds'],
  ['One sensor, one model', 'If it breaks or is fooled, nothing works.', 'Many experts fused; a missing one just gets weight 0'],
  ['Fake disaster videos', 'Panic and wrong evacuations.', 'Media authenticity check lowers trust in suspicious posts'],
  ['Internet goes down', 'App-only warnings never arrive.', 'Offline core + LoRa mesh + store-and-forward + local sirens'],
  ['New district, no labels', 'AI trained elsewhere fails here.', 'Physics works on day one with zero training'],
  ['Black-box scores', 'Officials cannot trust a bare 87%.', 'Every alert states why, plus how sure it is'],
]

const STANDOUT: [string, string, string][] = [
  [`${N('auc_caine').v} AUC`, `physics alone, zero training, on ${N('geo_events').v} real Indian landslides`, 'C3'],
  ['5 hazards', 'fire · landslide · flood · glacial-lake outburst · fake media in ONE pipeline', 'C2'],
  ['AI must earn it', 'a model is used only if it beats the simple rule with statistical confidence; our RL did not, so it is OFF', 'C3'],
  ['Human in the loop', 'no public alert can be sent without an operator\'s approval (enforced in code)', 'C2'],
  ['Works offline', 'alerts queue and travel over LoRa when the network is down', 'C2'],
  ['Honest numbers', 'we publish when our idea fails: a +0.095 gain shrank to 0 with 6.5× more data', 'C3'],
]

export function Slide2() {
  return (
    <Slide n={2} title="Why today's warnings fail, and why TRINETRA stands out." sub="Six problems documented in disaster-warning research, each with a concrete answer already in our code.">
      <div className="grid h-full grid-cols-12 gap-[18px]">
        <Card title="The problem → our answer" className="col-span-7" accent={C.red}>
          <div className="grid h-full grid-cols-[0.9fr_1.4fr] grid-rows-6 gap-x-[18px] gap-y-[12px]">
            {GAPS.map(([p, why, a]) => [
              <div key={p + 1} className="flex flex-col justify-center rounded-[12px] px-[16px] py-[10px]" style={{ background: '#FDE3D3' }}>
                <b style={{ fontSize: 23, color: C.red }}>{p}</b>
                <div style={{ fontSize: 18, color: C.dim }}>{why}</div>
              </div>,
              <div key={p + 2} className="flex items-center gap-[12px] rounded-[12px] px-[14px] py-[10px]" style={{ background: C.well }}>
                <span style={{ fontSize: 26, color: C.teal }}>→</span>
                <span style={{ fontSize: 22 }}>{a}</span>
              </div>,
            ])}
          </div>
        </Card>
        <Card title="What makes TRINETRA different" className="col-span-5" accent={C.teal}>
          <div className="flex h-full flex-col gap-[12px]">
            {STANDOUT.map(([h, d, k]) => (
              <div key={h} className="flex flex-1 items-center gap-[14px] rounded-[12px] px-[14px] py-[8px]" style={{ background: C.well }}>
                <div className="min-w-[178px] font-bold" style={{ fontSize: 26, lineHeight: 1.1, color: C.ember }}>{h}</div>
                <div className="flex flex-1 flex-col gap-[4px]">
                  <span style={{ fontSize: 19 }}>{d}</span>
                  <span><Chip k={k} /></span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </Slide>
  )
}
