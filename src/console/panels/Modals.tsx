import { useState, type ReactNode } from 'react'
import { X, PlugZap, PlayCircle } from 'lucide-react'
import { useStore } from '../store'
import { PARAM_BY_ID, PARAMS } from '../engine/params'
import { BANK_INFO } from '../engine/simulate'
import { Button, Chip, ClaimChip, ClassChip, IconButton } from '../ui/primitives'
import { fmtVal } from './ParamsPanel'
import { connectLive, disconnectLive, pushParams, startReplay, stopReplay, testConnection, useLive } from '../live/useLive'
import master from '../../../TRINETRA/results/master_merged/master.json'
import finalFigures from '../data/final_figures.json'

function Modal({ title, onClose, children, wide }: { title: ReactNode; onClose: () => void; children: ReactNode; wide?: boolean }) {
  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/55 p-6" role="dialog" aria-modal="true" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className={`flex max-h-[86vh] w-full flex-col rounded-lg border border-trn-line bg-trn-surface shadow-[0_8px_24px_rgba(0,0,0,.45)] ${wide ? 'max-w-[920px]' : 'max-w-[620px]'}`}>
        <div className="flex h-12 shrink-0 items-center justify-between border-b border-trn-line px-4">
          <h2 className="font-trn-display text-[16px] font-semibold text-trn-text">{title}</h2>
          <IconButton label="Close (Esc)" onClick={onClose}><X size={17} /></IconButton>
        </div>
        <div className="min-h-0 overflow-y-auto px-5 py-4 text-[13.5px] leading-6 text-trn-text2">{children}</div>
      </div>
    </div>
  )
}

const SYMBOLS: Record<string, string> = {
  fire: 'Q heat release rate (kW), D fire base diameter (m), L flame height (m), Q_c convective intensity per front length (kW/m), U wind (m/s), ρ air density 1.2 kg/m³, c_p 1.0 kJ/kg K, T_inf ambient temperature (K), g 9.81 m/s², N_c Byram convection number, c physics consistency in [0,1], u uncertainty in [0,1].',
  geo: 'FS factor of safety, c\' effective cohesion (kPa), φ\' friction angle, γ soil unit weight (kN/m³), z slip depth (m), β slope angle, u_w pore pressure (kPa), ψ pressure head (m), D0 diffusivity, I rain intensity (mm/h), D duration (h).',
  fusion: 'p_i expert probability, u_i uncertainty, c_i physics consistency, r_i reliability (capped per source), τ uncertainty temperature, w̃_i effective weight, D(p) weighted dispersion, U* conflict-aware uncertainty, S credible-alarm salience, ρ PHARAOH order.',
  decision: 'p* = C_FA/(C_FA + C_miss) is the cost-loss alarm point; levels GREEN < p* ≤ YELLOW (Watch) < 4p* ≤ ORANGE (Warning) < 10p* ≤ RED (Emergency); the shield can only raise.',
  lora: 'SF spreading factor, BW bandwidth 125 kHz, CR coding rate 4/5, P_tx transmit power, G antenna gains 2 dBi, M fade margin, S_SF receiver sensitivity (SX1276), n path-loss exponent, FSPL free-space path loss at 1 m.',
}

export function FormulaInspector() {
  const id = useStore((s) => s.inspector)
  const v = useStore((s) => (id ? s.params[id] : undefined))
  const set = useStore((s) => s.set)
  if (!id) return null
  const p = PARAM_BY_ID[id]
  if (!p) return null
  const key = p.module.startsWith('fire') ? 'fire' : p.module === 'geo_phys' ? 'geo' : p.module === 'lora' ? 'lora' : p.module === 'fusion' ? 'fusion' : 'decision'
  const n = Number(v)
  const frac = p.kind === 'number' ? Math.max(0, Math.min(1, (n - p.hard[0]) / (p.hard[1] - p.hard[0] || 1))) : 0
  const same = PARAMS.filter((q) => q.module === p.module && q.id !== p.id).slice(0, 6)
  return (
    <Modal title={<span className="flex items-center gap-2">{p.label}<ClassChip cls={p.cls} /></span>} onClose={() => set({ inspector: null })}>
      <div className="rounded border border-trn-line bg-trn-bg px-4 py-3 font-trn-mono text-[14px] text-trn-text">{p.equation}</div>
      <dl className="mt-3 grid grid-cols-[150px_1fr] gap-y-1.5">
        <dt className="text-trn-text3">Current value</dt><dd className="num text-trn-text">{fmtVal(p, v ?? p.default)} {p.unit !== '-' ? p.unit : ''} <span className="text-trn-text3">(repo default {fmtVal(p, p.default)})</span></dd>
        <dt className="text-trn-text3">Source</dt><dd className="font-trn-mono text-[12.5px]">{p.ref ? `${p.ref.file}:${p.ref.line}` : p.citation ?? 'not in repo'}</dd>
        <dt className="text-trn-text3">Module</dt><dd>{p.module}</dd>
        <dt className="text-trn-text3">Lowering it</dt><dd>{p.lower}</dd>
        <dt className="text-trn-text3">Raising it</dt><dd>{p.raise}</dd>
        <dt className="text-trn-text3">Symbols</dt><dd className="text-[12.5px]">{SYMBOLS[key]}</dd>
        {p.regime && <><dt className="text-trn-text3">Validity regime</dt><dd className="text-trn-warning">{p.regime}</dd></>}
        {p.kind === 'number' && <>
          <dt className="text-trn-text3">Regime meter</dt>
          <dd><div className="relative mt-2 h-2 rounded bg-trn-raised"><div className="absolute inset-y-0 rounded bg-trn-b/40" style={{ left: `${((p.range[0] - p.hard[0]) / (p.hard[1] - p.hard[0] || 1)) * 100}%`, right: `${(1 - (p.range[1] - p.hard[0]) / (p.hard[1] - p.hard[0] || 1)) * 100}%` }} />
            <div className="absolute -top-1 h-4 w-1 rounded bg-trn-gold" style={{ left: `calc(${frac * 100}% - 2px)` }} /></div>
            <div className="num mt-1 flex justify-between text-[11px] text-trn-text3"><span>{fmtVal(p, p.hard[0])}</span><span>safe range shaded</span><span>{fmtVal(p, p.hard[1])}</span></div></dd>
        </>}
        <dt className="text-trn-text3">Validation</dt>
        <dd>{p.cls === 'SURROGATE' ? <ClaimChip level="C1" title="Design / stand-in only" /> : p.module === 'fire_phys' || p.module === 'geo_phys' || p.module === 'fusion' || p.module === 'decision' || p.module === 'lora' || p.module === 'shield'
          ? <span className="flex flex-wrap items-center gap-1.5"><Chip tone="b">golden test: TS port matches Python</Chip><span className="text-[12px] text-trn-text3">src/console/engine/__tests__/golden.test.ts. Port correctness only, not field accuracy.</span></span>
          : <ClaimChip level="C2" />}</dd>
      </dl>
      {same.length > 0 && <div className="mt-3 text-[12px] text-trn-text3">Same module: {same.map((q) => <button key={q.id} onClick={() => set({ inspector: q.id })} className="mr-2 underline decoration-trn-line underline-offset-2 hover:text-trn-text">{q.label}</button>)}</div>}
    </Modal>
  )
}

type Row = { hazard: string; expert: string; metric: string; value: string | null; admitted: string | null; note: string }
type Fig = { url: string; name: string; group: string; title: string; explain: string }
const FIG_GROUPS: [string, string][] = [['results', 'Measured results'], ['extra', 'More result graphs'], ['physics', 'Physics explainers']]

function FigureGallery() {
  const figs = finalFigures as Fig[]
  const [open, setOpen] = useState<Fig | null>(null)
  if (!figs.length) return null
  return (
    <section className="mt-4">
      <h3 className="font-semibold text-trn-text">Final graphs ({figs.length})</h3>
      <p className="text-[12.5px] text-trn-text3">From TRINETRA_FINAL.zip (tools/import_final.py). Select a graph to enlarge it and read the explanation.</p>
      {FIG_GROUPS.map(([g, label]) => {
        const list = figs.filter((f) => f.group === g)
        if (!list.length) return null
        return (
          <div key={g} className="mt-2">
            <div className="text-[12px] font-medium uppercase tracking-wide text-trn-text3">{label}</div>
            <div className="mt-1 grid grid-cols-3 gap-2">
              {list.map((f) => (
                <button key={f.url} type="button" onClick={() => setOpen(open?.url === f.url ? null : f)}
                  className={`overflow-hidden rounded border bg-white text-left ${open?.url === f.url ? 'border-trn-brand' : 'border-trn-line'}`}>
                  <img src={import.meta.env.BASE_URL + f.url} alt={f.title} loading="lazy" className="h-24 w-full object-contain" />
                  <div className="truncate border-t border-trn-line bg-trn-raised px-1.5 py-1 text-[11.5px] text-trn-text2">{f.title}</div>
                </button>
              ))}
            </div>
            {open && open.group === g && (
              <figure className="mt-2 rounded border border-trn-line bg-trn-raised p-2">
                <img src={import.meta.env.BASE_URL + open.url} alt={open.title} className="w-full rounded bg-white" />
                <figcaption className="mt-2 text-[12.5px] leading-5"><b className="text-trn-text">{open.title}.</b> {open.explain}</figcaption>
              </figure>
            )}
          </div>
        )
      })}
    </section>
  )
}
export function AboutPanel() {
  const set = useStore((s) => s.set)
  const open = useStore((s) => s.about)
  if (!open) return null
  const rows = (master.scorecard as Row[]).filter((r) => r.value)
  return (
    <Modal wide title="About TRINETRA Command Console" onClose={() => set({ about: false })}>
      <h3 className="font-semibold text-trn-text">Project status and disclaimer</h3>
      <p>TRINETRA is a research prototype by Team Sankat Mochak. It is advisory only and is not an official warning system. It complements certified fire alarms and official warning channels. Every public alert needs human approval; this demo never sends a message to any person or channel. Outputs come from models trained on small, older datasets and are not field-validated. All incidents, cameras, sensors, villages and towers on the map are synthetic points; no private person or property is represented. The console does not imply endorsement by any government body, agency or institution.</p>
      <h3 className="mt-4 font-semibold text-trn-text">Modes</h3>
      <p><b>Simulation</b>: a seeded scenario generator places synthetic incidents and cameras; each camera observation is one real out-of-fold image score triple from the trained fire CNN, CLIP zero-shot and CLIP probe ({BANK_INFO.n} images, {BANK_INFO.nBlocks} blocks), and the repo formulas (ported to TypeScript, golden-tested against Python) decide. <b>Replay</b>: a recorded gateway session. <b>Live model</b>: events from an inference gateway; the bundled mock gateway runs the repo's own Python fuse() and decide().</p>
      <h3 className="mt-4 font-semibold text-trn-text">Measured results (prototype pack, our results)</h3>
      <p className="text-[12.5px] text-trn-text3">Source: TRINETRA/results/master_merged/master.json. Claim level C3 means implemented and measured by us; there is no C4 claim, so no comparison with published systems is made.</p>
      <table className="mt-2 w-full text-[12.5px]">
        <thead><tr className="text-left text-trn-text3"><th className="py-1 font-medium">Hazard</th><th className="font-medium">Expert</th><th className="font-medium">Metric</th><th className="font-medium">Value</th><th className="font-medium">Gate</th></tr></thead>
        <tbody className="num">{rows.map((r, i) => <tr key={i} className="border-t border-trn-line align-top"><td className="py-1 pr-2">{r.hazard}</td><td className="pr-2 font-trn-mono text-[12px]">{r.expert}</td><td className="pr-2">{r.metric}</td><td className="pr-2 text-trn-text">{r.value}</td><td>{r.admitted ?? '-'}</td></tr>)}</tbody>
      </table>
      <div className="mt-2"><ClaimChip level="C3" /> <span className="ml-1 text-[12px] text-trn-text3">Admitted learned experts under Rule 16: {rows.filter((r) => /^[1-9]\d*\//.test(r.admitted ?? '')).length}.</span></div>
      <FigureGallery />
      <h3 className="mt-4 font-semibold text-trn-text">Methods</h3>
      <p>Every slider comes from the parameter registry (tools/extract_params.py), which resolves each default to a repo file and line. Fusion follows ws5_fusion_rl (FM-1 default, PHARAOH and GMF selectable); the decision is level = max(conformal level at p*, safety shield). The fire perimeter is a SURROGATE (Anderson 1983 length-to-breadth ellipse) because the repo has no fire-spread model. The prior-shift correction is a PROPOSAL (Saerens et al. 2002), not in the repo. LoRa uses the repo's last-mile planner with terrain line of sight added.</p>
      <h3 className="mt-4 font-semibold text-trn-text">Data sources and attributions</h3>
      <ul className="list-disc pl-5 text-[12.5px]">
        <li>India boundary: Survey of India depiction via DataMeet india-soi.geojson (CC BY-SA 2.5 / ODbL). Provider boundaries are not used.</li>
        <li>State boundaries: DataMeet States/Admin2 (CC BY 4.0).</li>
        <li>Terrain: AWS Terrain Tiles (Terrarium), Mapzen / Tilezen sources including SRTM, ETOPO1 and others; cached locally.</li>
        <li>Rivers and world land: Natural Earth (public domain).</li>
        <li>Place search: GeoNames cities15000 (CC BY 4.0).</li>
        <li>Fonts: Inter, Space Grotesk, JetBrains Mono, Noto Sans Devanagari (SIL Open Font License), bundled.</li>
      </ul>
      <p className="mt-3 text-[12px] text-trn-text3">Full list: FRONTEND/FE_DATA_SOURCES.md. Previous research dashboard: <a className="underline" href="#research">#research</a>.</p>
      <p className="mt-4 font-trn-display text-[13px] tracking-wide text-trn-text3">Team Sankat Mochak</p>
    </Modal>
  )
}

export function SettingsPanel() {
  const st = useStore()
  const live = useLive()
  const [token, setToken] = useState('')
  const [msg, setMsg] = useState<string | null>(null)
  if (!st.settings) return null
  return (
    <Modal title="Settings and live model" onClose={() => st.set({ settings: false })}>
      <h3 className="font-semibold text-trn-text">Inference gateway</h3>
      <div className="mt-2 grid grid-cols-[1fr_auto] gap-2">
        <input value={st.gatewayUrl} onChange={(e) => st.set({ gatewayUrl: e.target.value })} aria-label="Gateway URL" className="h-8 rounded border border-trn-line bg-trn-raised px-2 font-trn-mono text-[12.5px] text-trn-text" />
        <Button onClick={async () => { const r = await testConnection(st.gatewayUrl); setMsg(r.ok ? `Connected: ${JSON.stringify(r.model)}` : `Not reachable: ${r.error}`) }}><PlugZap size={14} />Test</Button>
        <input value={token} onChange={(e) => setToken(e.target.value)} type="password" placeholder="Token (kept in memory only)" aria-label="Gateway token" className="h-8 rounded border border-trn-line bg-trn-raised px-2 text-[12.5px] text-trn-text" />
        {st.liveStatus === 'connected'
          ? <Button variant="danger" onClick={() => { disconnectLive(); st.set({ liveStatus: 'disconnected', mode: 'SIM' }) }}>Disconnect</Button>
          : <Button variant="primary" onClick={() => { connectLive(st.gatewayUrl); st.set({ settings: false }) }}>Connect live</Button>}
      </div>
      {msg && <p className="mt-2 font-trn-mono text-[12px]">{msg}</p>}
      <p className="mt-2 text-[12px] text-trn-text3">Start the bundled gateway with <code className="font-trn-mono">python3 tools/mock_gateway.py --port 8765</code>. It streams real out-of-fold model scores decided by the repo's Python fuse() and decide(); locations are synthetic.</p>
      {live.params && (
        <div className="mt-3">
          <h3 className="font-semibold text-trn-text">Inference-time parameters (sent to the gateway)</h3>
          <div className="mt-1 flex flex-wrap gap-1.5">{Object.entries(live.params.adjustable).map(([k, v]) => <Chip key={k}>{k} = {String(typeof v === 'number' ? Number(v.toFixed(3)) : v)}</Chip>)}</div>
          <Button className="mt-2" onClick={async () => {
            const vals = Object.fromEntries(Object.keys(live.params!.adjustable).map((k) => [k, st.params[k]]))
            const r = await pushParams(st.gatewayUrl, vals); setMsg(`Applied ${Object.keys(r.applied).length}; ${r.recomputed.length} events recomputed by the gateway`)
          }}>Send current lab values</Button>
          <p className="mt-1 text-[12px] text-trn-text3">Requires retraining, disabled in live mode: {live.params.requires_retraining.join(', ')}.</p>
        </div>
      )}
      <h3 className="mt-4 font-semibold text-trn-text">Replay</h3>
      <div className="mt-2 flex gap-2">
        <Button onClick={() => { startReplay(); st.set({ settings: false }) }}><PlayCircle size={14} />Replay recorded session</Button>
        <Button variant="ghost" onClick={() => { stopReplay(); st.set({ mode: 'SIM' }) }}>Back to simulation</Button>
      </div>
      <p className="mt-1 text-[12px] text-trn-text3">public/replay/session_demo.jsonl · {live.invalid} invalid messages rejected{live.lastError ? ` (last: ${live.lastError})` : ''}.</p>
      <h3 className="mt-4 font-semibold text-trn-text">Display</h3>
      <label className="mt-1 flex items-center gap-2"><input type="checkbox" checked={st.reduceMotion} onChange={(e) => st.set({ reduceMotion: e.target.checked })} />Reduce motion (no camera flights or pulses)</label>
    </Modal>
  )
}
