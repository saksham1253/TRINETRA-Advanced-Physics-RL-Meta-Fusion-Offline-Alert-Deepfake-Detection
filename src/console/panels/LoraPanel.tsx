import { RadioTower, Power, MapPinned } from 'lucide-react'
import { useStore } from '../store'
import { useMesh, radioFrom, planFrom } from '../lora/useMesh'
import { loraAirtimeS, loraRangeKm, SX1276_SENS_DBM, linkBudgetDb } from '../engine/lora'
import { Button, Chip, Section, Stat, StatusChip, cx } from '../ui/primitives'
import { useT } from '../i18n'
import { mapRef } from '../map/MapView'
import { ORIGIN } from '../lora/model'
import { num } from '../engine/params'
import { networkDown } from '../derived'
import { currentScenario } from '../useEngine'

export default function LoraPanel() {
  const t = useT()
  const st = useStore()
  const { mesh, ms, busy } = useMesh()
  const R = radioFrom(st.params), P = planFrom(st.params)
  const down = networkDown(currentScenario(), st.simMin, st.outage)
  const toggleOutage = () => {
    const on = !st.outage
    st.set({ outage: on, layers: { ...st.layers, lora: true } })
    useMesh.setState({ outageAt: on ? performance.now() : null })
    if (on) mapRef.current?.flyTo({ center: [ORIGIN.lon + 0.11, ORIGIN.lat + 0.07], zoom: 10.6, pitch: 58, bearing: -38, duration: 2600 })
  }
  const deadline = num(st.params, 'lora.deadline')
  return (
    <div className="min-h-0 flex-1 overflow-y-auto">
      <Section title="Offline alert path">
        <Button variant={st.outage ? 'danger' : 'primary'} className="h-10 w-full text-[14px]" onClick={toggleOutage}>
          <Power size={16} />{st.outage ? t('restoreBtn') : t('outageBtn')}
        </Button>
        <Button variant="ghost" className="mt-1.5 w-full" onClick={() => mapRef.current?.flyTo({ center: [ORIGIN.lon + 0.11, ORIGIN.lat + 0.07], zoom: 10.6, pitch: 58, bearing: -38, duration: 2200 })}>
          <MapPinned size={14} />Show mesh (Chamoli valley)
        </Button>
        <p className="mt-1.5 text-[11px] leading-4 text-trn-text3">Geometry: the repo's synthetic 12-village valley (ws3_alert/last_mile.py) laid on real Chamoli terrain. Gateway and relays snapped to local high ground. Click a node on the map to fail or restore it.</p>
      </Section>
      {mesh ? (
        <>
          <Section title={down ? 'Alert delivery with networks down' : 'Mesh on standby'} right={<span className="num text-[11px] text-trn-text3">{busy ? 'recomputing' : `${t('recomputed')} ${ms.toFixed(0)} ms`}</span>}>
            <div className="grid grid-cols-3 gap-2">
              <Stat label={`Villages ≤ ${deadline} min`} value={`${mesh.reachedByDeadline}/${mesh.results.length}`} tone={mesh.reachedByDeadline < mesh.results.length ? 'warning' : 'advisory'} />
              <Stat label="Population reached" value={`${Math.round((100 * mesh.popByDeadline) / mesh.popTotal)}%`} sub={`${mesh.popByDeadline.toLocaleString('en-IN')} of ${mesh.popTotal.toLocaleString('en-IN')}`} />
              <Stat label="Links blocked by terrain" value={mesh.blocked} sub={`of ${mesh.links.length} in range`} />
              <Stat label="Per hop" value={`${mesh.hopS.toFixed(2)} s`} sub={`airtime ${(mesh.airtimeS * 1000).toFixed(0)} ms ×2 + 0.5 s`} />
              <Stat label="Duty cycle per alert" value={`${mesh.dutyUsedPct.toFixed(3)}%`} sub={`limit ${num(st.params, 'lora.duty')}% per hour`} tone={mesh.dutyUsedPct > num(st.params, 'lora.duty') ? 'emergency' : 'neutral'} />
              <Stat label="Link budget" value={`${linkBudgetDb(R).toFixed(0)} dB`} sub={`SF${R.sf}, ${R.tx} dBm`} />
            </div>
          </Section>
          <Section title="Per-village result">
            <table className="w-full text-[12px]">
              <thead><tr className="text-trn-text3"><th className="text-left font-medium">Village</th><th className="text-right font-medium">min</th><th className="pl-2 text-left font-medium">Channel</th><th className="text-right font-medium">P(del.)</th></tr></thead>
              <tbody className="num">
                {mesh.results.map((r) => (
                  <tr key={r.id} className={cx(r.minutes === null || r.minutes > deadline ? 'text-trn-emergency' : 'text-trn-text2')}>
                    <td className="py-0.5">{r.id} <span className="text-trn-text3">({r.population})</span></td>
                    <td className="text-right">{r.minutes === null ? '–' : r.minutes.toFixed(1)}</td>
                    <td className="truncate pl-2" title={r.path.join(' → ')}>{r.channel}{r.path.length > 1 && !r.channel.startsWith('runner') ? ` · ${r.path.length - 1} hops` : ''}</td>
                    <td className="text-right">{mesh.delivery[r.id].toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Section>
        </>
      ) : <Section title="Mesh"><p className="text-[13px] text-trn-text3">Sampling terrain for line of sight on {`~`}100 candidate links.</p></Section>}
      <Section title="Failure injection (simulated)">
        <label className="block text-[12px] text-trn-text2">Packet loss per transmission <span className="num float-right font-trn-mono text-trn-text">{Math.round(st.packetLoss * 100)}%</span>
          <input type="range" min={0} max={0.6} step={0.05} value={st.packetLoss} style={{ ['--fill' as string]: `${(st.packetLoss / 0.6) * 100}%` }} onChange={(e) => st.set({ packetLoss: Number(e.target.value) })} /></label>
        <label className="block text-[12px] text-trn-text2">Retransmissions per hop <span className="num float-right font-trn-mono text-trn-text">{st.retransmissions}</span>
          <input type="range" min={0} max={5} step={1} value={st.retransmissions} style={{ ['--fill' as string]: `${(st.retransmissions / 5) * 100}%` }} onChange={(e) => st.set({ retransmissions: Number(e.target.value) })} /></label>
        <div className="mt-1 flex flex-wrap gap-1">
          {mesh?.layout.nodes.map((n) => (
            <button key={n.id} onClick={() => { const d = new Set(st.disabledNodes); d.has(n.id) ? d.delete(n.id) : d.add(n.id); st.set({ disabledNodes: [...d] }) }}
              className={cx('h-7 rounded border px-2 font-trn-mono text-[11px]', st.disabledNodes.includes(n.id) ? 'border-trn-emergency/70 text-trn-emergency line-through' : 'border-trn-line text-trn-text2')}>{n.id}</button>
          ))}
        </div>
      </Section>
      <Section title="Spreading factor trade-off" right={<Chip tone="a">Class A · SX1276 datasheet</Chip>}>
        <table className="w-full text-[12px]">
          <thead><tr className="text-trn-text3"><th className="text-left font-medium">SF</th><th className="text-right font-medium">Sensitivity</th><th className="text-right font-medium">Range, hill forest</th><th className="text-right font-medium">Airtime {P.payload} B</th></tr></thead>
          <tbody className="num">
            {[7, 8, 9, 10, 11, 12].map((sf) => (
              <tr key={sf} className={sf === R.sf ? 'text-trn-gold' : 'text-trn-text2'}>
                <td>SF{sf}</td><td className="text-right">{SX1276_SENS_DBM[sf]} dBm</td>
                <td className="text-right">{Math.min(loraRangeKm({ ...R, sf }, 'hill_forest'), P.maxHopKm).toFixed(1)} km</td>
                <td className="text-right">{(loraAirtimeS(P.payload, sf) * 1000).toFixed(0)} ms</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p className="mt-1 text-[11px] leading-4 text-trn-text3">Range from the log-distance model with the repo's assumed exponent; terrain line of sight (60% first Fresnel zone, 4/3 earth) is then applied per link on the map.</p>
      </Section>
      <Section title={<span className="flex items-center gap-1.5"><RadioTower size={14} />Hardware reality</span>}>
        <ul className="space-y-1.5 text-[12px] text-trn-text2">
          <li className="flex items-start gap-2"><StatusChip status="IMPLEMENTED" /><span>25-byte sensor frame codec (ws7_iot/lora_codec.py), last-mile planner with sirens and human relay (ws3_alert/last_mile.py), spray-and-wait store-and-forward queue (ws3_alert/dtn.py).</span></li>
          <li className="flex items-start gap-2"><StatusChip status="SIMULATED" /><span>Radio propagation, terrain line of sight, packet loss and retransmission. Not field-tested.</span></li>
          <li className="flex items-start gap-2"><StatusChip status="PLANNED" /><span>Node firmware (trinetra/firmware/FIRMWARE_SPEC.md), on-air authentication tag and replay protection, site survey to fit path-loss exponents.</span></li>
        </ul>
        <p className="mt-2 text-[11px] leading-4 text-trn-text3">Limits: small payloads, low data rate, duty-cycle limits, no guaranteed delivery. 865–867 MHz licence-exempt limits as cited in the repo (WPC GSR 1048(E)); verify current rules before field use.</p>
      </Section>
    </div>
  )
}
