import { useStore } from '../store'
import { Section, Toggle } from '../ui/primitives'
import { demStats } from '../map/dem'
import { useEffect, useState } from 'react'

const LAYERS: [string, string, string][] = [
  ['relief', 'Terrain relief and hillshade', 'AWS Terrain Tiles, cached locally'],
  ['states', 'State boundaries', 'DataMeet (CC BY 4.0)'],
  ['rivers', 'Rivers', 'Natural Earth (public domain)'],
  ['cameras', 'Cameras without alert', 'synthetic positions'],
  ['alerts', 'Alert beacons', 'engine output'],
  ['perimeter', 'Fire perimeter and flame band', 'SURROGATE spread; Heskestad flame height'],
  ['wind', 'Wind field', 'scenario input'],
  ['lora', 'LoRa mesh, villages, sirens', 'repo demo_valley geometry, synthetic placement'],
  ['towers', 'Cell towers', 'synthetic markers'],
]
const PLANNED = ['Satellite imagery', 'Active-fire detections (FIRMS)', 'Forest cover', 'Districts', 'Population density', 'Cyclone track']

export default function LayersPanel() {
  const st = useStore()
  const [stats, setStats] = useState({ ...demStats })
  useEffect(() => { const id = setInterval(() => setStats({ ...demStats }), 1500); return () => clearInterval(id) }, [])
  return (
    <div className="min-h-0 flex-1 overflow-y-auto">
      <Section title="Map layers">
        {LAYERS.map(([id, label, src]) => (
          <div key={id}>
            <Toggle label={label} checked={st.layers[id]} onChange={(v) => st.set({ layers: { ...st.layers, [id]: v } })} />
            <div className="-mt-1 mb-1 text-[11px] text-trn-text3">{src}</div>
          </div>
        ))}
      </Section>
      <Section title="Terrain exaggeration">
        <div className="flex items-center gap-2">
          <input type="range" min={1} max={4} step={0.1} value={st.exaggeration} aria-label="Terrain exaggeration"
            style={{ ['--fill' as string]: `${((st.exaggeration - 1) / 3) * 100}%` }} onChange={(e) => st.set({ exaggeration: Number(e.target.value) })} />
          <span className="num w-10 text-right font-trn-mono text-[12px] text-trn-text">{st.exaggeration.toFixed(1)}×</span>
        </div>
      </Section>
      <Section title="Terrain data">
        <dl className="grid grid-cols-2 gap-y-1 text-[12px]">
          <dt className="text-trn-text3">Cached tiles</dt><dd className="num text-trn-text2">{stats.cachedTiles}</dd>
          <dt className="text-trn-text3">Served locally</dt><dd className="num text-trn-text2">{stats.local}</dd>
          <dt className="text-trn-text3">Built from parent</dt><dd className="num text-trn-text2">{stats.ancestor}</dd>
          <dt className="text-trn-text3">Fetched online</dt><dd className="num text-trn-text2">{stats.online}</dd>
        </dl>
        <Toggle label="Allow online terrain fill" checked={st.online} onChange={(v) => st.set({ online: v })} />
        <p className="text-[11px] leading-4 text-trn-text3">Off: everything comes from local files, deeper zoom is resampled from the nearest cached tile.</p>
      </Section>
      <Section title="Not in the offline pack">
        <ul className="space-y-0.5 text-[12px] text-trn-text3">{PLANNED.map((p) => <li key={p}>{p} · planned</li>)}</ul>
      </Section>
    </div>
  )
}
