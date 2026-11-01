import { C, Card, Chip, N, Slide, Src } from './ui'

const BARS: [string, keyof typeof import('./numbers.json'), string][] = [
  ['Physics: rain threshold (Caine), no training', 'auc_caine', C.teal],
  ['Physics: soil-water slope drop (ΔFS), no training', 'auc_dfs', C.teal],
  ['Trained: rain-only model', 'auc_rain', '#8A6A55'],
  ['Trained: rain + physics', 'auc_hybrid', C.blue],
  ['Physics-informed neural net (not admitted)', 'auc_pinn', C.violet],
]

function Bars() {
  return (
    <div className="flex flex-col gap-[20px]">
      {BARS.map(([l, k, col]) => {
        const v = parseFloat(N(k).v)
        return (
          <div key={l} className="grid grid-cols-[380px_1fr_70px] items-center gap-[12px]">
            <span style={{ fontSize: 20 }}>{l}</span>
            <div className="h-[30px] rounded-full" style={{ background: '#F6DCC4' }}>
              <div className="h-full rounded-full" style={{ width: `${((v - 0.5) / 0.35) * 100}%`, background: col }} />
            </div>
            <span className="font-mono font-bold" style={{ fontSize: 20 }}>{N(k).v}</span>
          </div>
        )
      })}
      <span style={{ fontSize: 14, color: C.dim }}>ROC-AUC (0.5 = coin toss, 1 = perfect) · spatial-block cross-validation so no place appears in both train and test</span>
    </div>
  )
}

const P2: [string, string, string][] = [
  ['A', 'Fire detector (CNN) + video check', 'D-Fire train · DeepFire + FIRE held-out · FireSense video'],
  ['B', 'Zero-shot CLIP fire/smoke', 'same data + fog, weather, candle, scene look-alikes'],
  ['C', 'Fake-media detector', 'CIFAKE train · StyleGAN faces + AI art held-out'],
  ['D', 'Satellite heads + geo physics', 'Landslide4Sense · Sen1Floods11 (Bolivia held-out)'],
  ['F', 'Fusion of A + B + C', 'FM-1 vs median vs max, then offline RL with its gate'],
]

export function Slide6() {
  return (
    <Slide n={6} title="What we have proven, and what Phase 2 is measuring right now." sub="Measured numbers are on the left. Phase 2 runs on Kaggle (3 seeds, held-out datasets) fill the right side; we do not estimate them.">
      <div className="grid h-full grid-cols-12 grid-rows-[1fr_auto] gap-[18px]">
        <Card title={`Landslides: ${N('geo_events').v} real Indian events (Western Himalaya, 29–33°N 76–81°E)`} className="col-span-7" accent={C.teal} right={<Chip k="C3" />}>
          <Bars />
          <div className="mt-[24px] grid grid-cols-3 gap-[14px]">
            <div className="rounded-[12px] p-[12px]" style={{ background: C.well }}>
              <div className="font-bold" style={{ fontSize: 38, color: C.teal }}>{N('ece_hybrid').v}</div>
              <div style={{ fontSize: 16 }}>calibration error: when it says 30 %, it is right about 30 % of the time</div>
            </div>
            <div className="rounded-[12px] p-[12px]" style={{ background: C.well }}>
              <div className="font-bold" style={{ fontSize: 38, color: C.ink }}>{N('geo_rows').v.split(' ')[0]}</div>
              <div style={{ fontSize: 16 }}>test rows: landslide days + same-site normal monsoon days, 101 spatial blocks</div>
            </div>
            <div className="rounded-[12px] p-[12px]" style={{ background: '#FDE3D3' }}>
              <div className="font-bold" style={{ fontSize: 24, color: C.red }}>RL not deployed</div>
              <div style={{ fontSize: 16 }}>our learned policy never beat the physics rule with confidence, so the gate kept the rule</div>
            </div>
          </div>
          <Src>results/geo_large · results/geo_pinn · results/rl_env · single seed; multi-seed in Phase 2</Src>
        </Card>
        <Card title="Phase 2 runs (Kaggle, T4 × 2)" className="col-span-5" accent={C.amber} right={<Chip k="PENDING">4 OF 5 PENDING</Chip>}>
          <div className="flex h-full flex-col gap-[10px]">
            {P2.map(([a, t, d]) => (
              <div key={a} className="flex flex-1 items-center gap-[12px] rounded-[12px] px-[12px] py-[8px]" style={{ background: C.well }}>
                <span className="flex h-[40px] w-[40px] shrink-0 items-center justify-center rounded-full font-bold" style={{ background: C.ink, color: '#FFD54A', fontSize: 19 }}>{a}</span>
                <div className="flex-1">
                  <b style={{ fontSize: 21 }}>{t}</b>
                  <div style={{ fontSize: 16, color: C.dim }}>{d}</div>
                </div>
                {a === 'B' ? (
                  <span className="text-right font-mono" style={{ fontSize: 15, color: C.teal }}>AUC {N('zs_auc').v}<br />not admitted</span>
                ) : (
                  <span className="font-mono" style={{ fontSize: 15, color: C.amber }}>pending</span>
                )}
              </div>
            ))}
            <p style={{ fontSize: 17, color: C.dim }}>Each model is admitted only if it beats simple baselines (colour histogram, rain rule) with a confidence interval, on data from a different source.</p>
          </div>
        </Card>
        <Card className="col-span-12" accent={C.ember}>
          <div className="grid grid-cols-4 gap-[20px]" style={{ fontSize: 18 }}>
            <span><b style={{ fontSize: 30 }}>{N('tests').v}</b> unit tests pass</span>
            <span><b style={{ fontSize: 30 }}>{N('gates').v}</b> honesty / safety checks pass</span>
            <span><b style={{ fontSize: 30 }}>{N('bugs').v}</b> bugs found by running the code, fixed</span>
            <span><b style={{ fontSize: 30 }}>{N('datasets').v}</b> open datasets, every licence credited</span>
          </div>
        </Card>
      </div>
    </Slide>
  )
}
