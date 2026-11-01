import { C, Card, Slide, Src } from './ui'

const ARROW = (id: string, col: string) => (
  <marker id={id} markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill={col} />
  </marker>
)

function Entity({ x, y, w = 260, h = 88, t, s }: { x: number; y: number; w?: number; h?: number; t: string; s: string }) {
  return (
    <g>
      <rect x={x} y={y} width={w} height={h} rx={6} fill="#FFFFFF" stroke={C.ink} strokeWidth={2.4} />
      <text x={x + w / 2} y={y + h / 2 - 4} textAnchor="middle" fontSize={19} fontWeight={700} fill={C.ink}>{t}</text>
      <text x={x + w / 2} y={y + h / 2 + 20} textAnchor="middle" fontSize={14} fill={C.dim}>{s}</text>
    </g>
  )
}

function Flow({ d, label, lx, ly, col = C.ember, id = 'a0' }: { d: string; label?: string; lx?: number; ly?: number; col?: string; id?: string }) {
  return (
    <g>
      <path d={d} fill="none" stroke={col} strokeWidth={2.6} markerEnd={`url(#${id})`} />
      {label && (
        <text x={lx} y={ly} textAnchor="middle" fontSize={14} fontWeight={600} fill={C.ink} style={{ paintOrder: 'stroke', stroke: C.panel, strokeWidth: 6 }}>{label}</text>
      )}
    </g>
  )
}

function Level0() {
  return (
    <svg viewBox="0 0 820 620" className="h-full w-full">
      <defs>{ARROW('a0', C.ember)}{ARROW('a0t', C.teal)}</defs>
      <Entity x={0} y={10} t="Field sensors + CCTV" s="frames, rain, tilt, soil" />
      <Entity x={0} y={266} t="Satellites + weather" s="Sentinel-1/2, NASA, IMD" />
      <Entity x={0} y={522} t="News + social media" s="photos, videos, posts" />
      <Entity x={560} y={30} t="Operator (SDMA)" s="control room officer" />
      <Entity x={560} y={502} t="Public + communities" s="phones, sirens, radio" />
      <circle cx={415} cy={310} r={112} fill={C.ember} stroke={C.ink} strokeWidth={3} />
      <text x={415} y={286} textAnchor="middle" fontSize={20} fontWeight={700} fill="#FFFFFF">0</text>
      <text x={415} y={320} textAnchor="middle" fontSize={34} fontWeight={800} fill="#FFFFFF">TRINETRA</text>
      <text x={415} y={348} textAnchor="middle" fontSize={16} fill="#FFF3D6">early-warning system</text>
      <Flow d="M130,98 C130,180 250,240 306,262" label="live readings" lx={200} ly={190} />
      <Flow d="M260,310 L300,310" />
      <text x={130} y={378} textAnchor="middle" fontSize={14} fontWeight={600} fill={C.ink}>imagery →</text>
      <Flow d="M130,522 C130,440 250,380 306,358" label="media" lx={190} ly={440} />
      <Flow d="M470,212 C500,170 540,120 558,96" label="risk + reasons + uncertainty" lx={600} ly={176} />
      <Flow d="M690,118 C690,190 580,250 528,280" label="approve / reject" lx={720} ly={232} col={C.teal} id="a0t" />
      <Flow d="M480,402 C520,450 600,480 640,500" label="approved alert" lx={610} ly={448} col={C.teal} id="a0t" />
    </svg>
  )
}

function Proc({ x, y, n, t, s, col = C.ember }: { x: number; y: number; n: string; t: string; s: string; col?: string }) {
  return (
    <g>
      <rect x={x} y={y} width={220} height={96} rx={48} fill="#FFFFFF" stroke={col} strokeWidth={3} />
      <text x={x + 110} y={y + 30} textAnchor="middle" fontSize={15} fontWeight={700} fill={col}>{n}</text>
      <text x={x + 110} y={y + 56} textAnchor="middle" fontSize={19} fontWeight={700} fill={C.ink}>{t}</text>
      <text x={x + 110} y={y + 78} textAnchor="middle" fontSize={13} fill={C.dim}>{s}</text>
    </g>
  )
}

function Store({ x, y, n, t, w = 240 }: { x: number; y: number; n: string; t: string; w?: number }) {
  return (
    <g>
      <rect x={x} y={y} width={w} height={46} fill="#FFF3D6" />
      <path d={`M${x + w},${y} H${x} V${y + 46} H${x + w} M${x + 44},${y} v46`} stroke={C.ink} strokeWidth={2.2} fill="none" />
      <text x={x + 22} y={y + 30} textAnchor="middle" fontSize={16} fontWeight={700} fill={C.ink}>{n}</text>
      <text x={x + 54} y={y + 30} fontSize={16} fill={C.ink}>{t}</text>
    </g>
  )
}

function Level1() {
  const L = Flow
  return (
    <svg viewBox="0 0 1110 620" className="h-full w-full">
      <defs>{ARROW('a1', C.ember)}{ARROW('a1t', C.teal)}{ARROW('a1d', C.dim)}{ARROW('a1b', C.blue)}{ARROW('a1r', C.red)}{ARROW('a1a', C.amber)}</defs>
      <Proc x={0} y={40} n="1.0" t="Ingest + clean" s="leakage-safe adapters" />
      <Proc x={320} y={40} n="2.0" t="Detect" s="fire CNN · CLIP · media · EO" />
      <Proc x={320} y={260} n="3.0" t="Physics check" s="rain → soil → slope FS" col={C.blue} />
      <Proc x={610} y={150} n="4.0" t="Fuse + uncertainty" s="weights · U* · calibration" col={C.teal} />
      <Proc x={885} y={40} n="5.0" t="Decide level" s="cost threshold + shield" col={C.amber} />
      <Proc x={885} y={260} n="6.0" t="Human approval" s="operator signs alert" col={C.teal} />
      <Proc x={885} y={480} n="7.0" t="Deliver alert" s="CAP · SMS · LoRa · siren" col={C.red} />
      <Store x={0} y={440} n="D1" t="Models + physics config" />
      <Store x={320} y={440} n="D2" t="Results + audit log" />
      <Store x={600} y={540} n="D3" t="Offline alert queue" w={230} />
      <L d="M220,88 L316,88" label="clean data" lx={268} ly={76} id="a1" />
      <L d="M170,136 C170,250 240,308 316,308" label="rain, slope" lx={190} ly={236} />
      <L d="M430,136 L430,256" label="frames, features" lx={505} ly={200} />
      <L d="M540,88 C600,88 640,120 660,148" label="p, u per expert" lx={610} ly={78} />
      <L d="M540,308 C600,308 640,280 662,248" label="physics consistency" lx={590} ly={268} col={C.blue} id="a1b" />
      <L d="M830,186 C870,170 880,110 883,98" label="p̂, U*" lx={850} ly={128} col={C.teal} id="a1t" />
      <L d="M995,136 L995,256" label="level + reasons" lx={1050} ly={200} col={C.amber} id="a1a" />
      <L d="M995,356 L995,476" label="approved" lx={1040} ly={420} col={C.teal} id="a1t" />
      <L d="M885,528 C860,528 850,560 834,563" label="link down: queue" lx={760} ly={528} col={C.red} id="a1r" />
      <L d="M110,440 L110,140" col={C.dim} id="a1d" />
      <text x={64} y={300} textAnchor="middle" fontSize={14} fontWeight={600} fill={C.dim}>weights</text>
      <L d="M720,246 C710,350 560,410 490,438" label="log every decision" lx={720} ly={420} col={C.dim} id="a1d" />
    </svg>
  )
}

export function Slide3() {
  return (
    <Slide n={3} title="How data moves: DFD Level 0 and Level 1." sub="Level 0 shows who TRINETRA talks to. Level 1 opens the box: seven steps, three data stores, and a human before any public alert.">
      <div className="grid h-full grid-cols-12 grid-rows-[1fr_auto] gap-[18px]">
        <Card title="DFD Level 0 · context" className="col-span-5" accent={C.ember}>
          <Level0 />
        </Card>
        <Card title="DFD Level 1 · inside TRINETRA" className="col-span-7" accent={C.teal}>
          <Level1 />
        </Card>
        <Card className="col-span-12" accent={C.amber}>
          <div className="flex items-center justify-between gap-[24px]" style={{ fontSize: 18 }}>
            <span><b>Notation:</b> rectangle = external entity · rounded box = process · open box = data store · arrow = data flow</span>
            <span><b style={{ color: C.teal }}>Teal arrows</b> pass through the human gate · <b style={{ color: C.red }}>red</b> = offline path</span>
            <Src>code: data_adapters/ · ws5_fusion_rl/ · ws1b_geophys/ · ws3_alert/</Src>
          </div>
        </Card>
      </div>
    </Slide>
  )
}
