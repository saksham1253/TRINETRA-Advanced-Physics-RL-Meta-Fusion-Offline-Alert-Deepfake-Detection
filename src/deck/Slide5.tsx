import { C, Card, Chip, N, Slide, Src } from './ui'

const CHAIN: [string, string, string, string][] = [
  ['Field node', 'rain + tilt + soil sensors; no internet needed', 'Tier-0 rule: local siren only if fast tilt AND heavy rain (two cues)', 'C2'],
  ['LoRa radio mesh', 'km-range, low-power, no SIM', 'readings packed into ≤ 51-byte frames (IN865 band)', 'C2'],
  ['Store-and-forward queue', 'link down? alerts wait and hop node-to-node', 'spray-and-wait delay-tolerant queue, delivered when any link returns', 'C2'],
  ['Human-signed CAP alert', 'standard format used by SACHET / NDMA', 'CAP 1.2; code refuses to build one without operator approval', 'C2'],
  ['Last mile', 'SMS · cell broadcast · sirens · community radio', 'SMS / cell broadcast through official gateways', 'PLANNED'],
]

export function Slide5() {
  return (
    <Slide n={5} title="It still warns when the internet is down, and it can flag disasters it has never seen." sub="Two questions evaluators always ask: what if the network fails, and what about a new kind of disaster?">
      <div className="grid h-full grid-cols-12 gap-[18px]">
        <Card title="Offline alerts: the warning path without internet" className="col-span-6" accent={C.red}>
          <div className="flex h-full flex-col gap-[10px]">
            {CHAIN.map(([t, d, how, k], i) => (
              <div key={t} className="flex flex-1 items-stretch gap-[12px]">
                <div className="flex flex-col items-center">
                  <span className="flex h-[38px] w-[38px] items-center justify-center rounded-full font-bold" style={{ background: C.red, color: '#FFFFFF', fontSize: 18 }}>{i + 1}</span>
                  {i < CHAIN.length - 1 && <span className="w-[3px] flex-1" style={{ background: '#F1B79A' }} />}
                </div>
                <div className="flex flex-1 flex-col justify-center rounded-[12px] px-[14px] py-[8px]" style={{ background: C.well }}>
                  <div className="flex items-center justify-between gap-2"><b style={{ fontSize: 21 }}>{t}</b><Chip k={k} /></div>
                  <div style={{ fontSize: 17 }}>{d}</div>
                  <div style={{ fontSize: 15, color: C.dim }}>{how}</div>
                </div>
              </div>
            ))}
            <p style={{ fontSize: 17, color: C.dim }}>
              Physics, fusion and the decision engine run in plain numpy on a laptop or gateway, with no cloud. The one autonomous action is a co-located siren; public messages always need a human.
            </p>
            <Src>ws7_iot/edge_screen.py · lora_codec.py · ws3_alert/dtn.py · cap.py · siren.py</Src>
          </div>
        </Card>

        <Card title="Zero-shot: classifying a disaster it was never trained on" className="col-span-6" accent={C.violet}>
          <div className="flex flex-col gap-[12px]">
            <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-[10px]">
              <div className="rounded-[12px] p-[12px] text-center" style={{ background: C.well, border: `2px solid ${C.violet}` }}>
                <b style={{ fontSize: 19 }}>New camera image</b>
                <div style={{ fontSize: 15, color: C.dim }}>e.g. a mudflow, never in training</div>
              </div>
              <span style={{ fontSize: 26, color: C.violet }}>⇄</span>
              <div className="rounded-[12px] p-[12px]" style={{ background: C.well, border: `2px solid ${C.violet}` }}>
                <b style={{ fontSize: 19 }}>Plain-text descriptions</b>
                <div className="font-mono" style={{ fontSize: 14, color: C.dim }}>"a forest fire" · "thick smoke" · "fog" · "a mudflow on a road" ← added by typing</div>
              </div>
            </div>
            <p style={{ fontSize: 19 }}>
              A vision-language model (CLIP, ViT-B-32) puts images and sentences in the same space and picks the closest description. To add a new hazard we
              <b> write one sentence; no new labelled photos, no retraining.</b> Look-alikes such as fog, steam and festival lights are listed on purpose so they do not count as fire.
            </p>
            <div className="rounded-[12px] p-[12px]" style={{ background: '#EFE7FF' }}>
              <b style={{ fontSize: 19, color: C.violet }}>And if it matches nothing we know?</b>
              <ul className="mt-[6px] flex flex-col gap-[4px]" style={{ fontSize: 17 }}>
                <li>● A no-label anomaly detector (3 detectors: forecast error, isolation, distance) flags "never seen this pattern".</li>
                <li>● Disagreement between experts raises uncertainty U*; above 0.6 the case goes to a human.</li>
                <li>● <b>The unknown is never silent:</b> with no confident expert the output is "uncertain", not "safe".</li>
              </ul>
            </div>
            <div className="flex items-center gap-[12px] rounded-[12px] px-[12px] py-[8px]" style={{ background: C.well, fontSize: 17 }}>
              <Chip k="C3" />
              <span>
                <b>Measured in Phase 2:</b> AUC {N('zs_auc').v} with zero fire training, but {N('zs_fa_flames').v} false alarms on candles and {N('zs_fa_weather').v} on
                weather, so it is <b>{N('zs_admit').v.toLowerCase()}</b>; it stays a low-trust helper (cap 0.5).
              </span>
            </div>
            <div className="rounded-[12px] p-[12px]" style={{ background: C.well }}>
              <b style={{ fontSize: 19 }}>How a new hazard earns trust</b>
              <div className="mt-[8px] flex items-center gap-[10px]" style={{ fontSize: 17 }}>
                {['1 · write its description', '2 · test on a held-out set', '3 · beat baselines with CI', '4 · trust raised in fusion'].map((t, i, a) => (
                  <span key={t} className="flex items-center gap-[10px]">
                    <span className="rounded-[10px] px-[10px] py-[6px]" style={{ border: `2px solid ${C.violet}` }}>{t}</span>
                    {i < a.length - 1 && <span style={{ color: C.violet }}>→</span>}
                  </span>
                ))}
              </div>
            </div>
            <Src>kaggle/eval_zeroshot.py · ws8_anomaly/ · ws5_fusion_rl/decision.py</Src>
          </div>
        </Card>
      </div>
    </Slide>
  )
}
