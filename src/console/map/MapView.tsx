import type * as GeoJSON from 'geojson'
import { useEffect, useRef, useState } from 'react'
import * as maplibregl from 'maplibre-gl'
import type { GeoJSONSource } from 'maplibre-gl'
// MapLibre 6 looks for its worker next to its own module; Vite pre-bundling and production builds move it, so point to it.
import maplibreWorkerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url'
import { create } from 'zustand'
import { useStore } from '../store'
import { currentScenario } from '../useEngine'
import { allNow, networkDown, perimeter, SEV_NAME } from '../derived'
import { buildStyle, SEV_COLORS } from './style'
import { registerTerrainProtocol } from './terrainProtocol'
import { installIconLoader } from './icons'
import { elevation, demConfig } from './dem'
import { useMesh } from '../lora/useMesh'
import { useLive } from '../live/useLive'
import { offset } from '../engine/simulate'
import { num } from '../engine/params'

/** Safe mode (URL `?safe=1` in the hash): no 3D terrain mesh, no motion. For weak GPUs and automated screenshots. */
export const SAFE = new URLSearchParams(location.hash.split('?')[1] ?? '').get('safe') === '1'
export const INDIA_VIEW = { center: [80.6, 22.6] as [number, number], zoom: 4.05, pitch: 32, bearing: 0 }
export const useCursor = create<{ lon: number; lat: number; elev: number | null; slope: number | null; aspect: number | null; zoom: number; fps: number }>(
  () => ({ lon: 0, lat: 0, elev: null, slope: null, aspect: null, zoom: 0, fps: 0 }))
export const mapRef: { current: maplibregl.Map | null } = { current: null }

type FC = GeoJSON.FeatureCollection
const fc = (features: GeoJSON.Feature[]): FC => ({ type: 'FeatureCollection', features })
const pt = (lon: number, lat: number, properties: Record<string, unknown> = {}): GeoJSON.Feature => ({ type: 'Feature', properties, geometry: { type: 'Point', coordinates: [lon, lat] } })
const setData = (m: maplibregl.Map, id: string, d: FC) => (m.getSource(id) as GeoJSONSource | undefined)?.setData(d)

function parseHashCamera() {
  const q = location.hash.split('?')[1]
  if (!q) return null
  const c = new URLSearchParams(q).get('c')
  if (!c) return null
  const [lon, lat, zoom, pitch, bearing] = c.split(',').map(Number)
  return Number.isFinite(lon) ? { center: [lon, lat] as [number, number], zoom, pitch, bearing } : null
}

export default function MapView() {
  const el = useRef<HTMLDivElement>(null)
  const theme = useStore((s) => s.theme)
  const exaggeration = useStore((s) => s.exaggeration)
  const result = useStore((s) => s.result)
  const simMin = useStore((s) => s.simMin)
  const selected = useStore((s) => s.selected)
  const showTruth = useStore((s) => s.showTruth)
  const layers = useStore((s) => s.layers)
  const params = useStore((s) => s.params)
  const diveSite = useStore((s) => s.diveSite)
  const outage = useStore((s) => s.outage)
  const online = useStore((s) => s.online)
  const mesh = useMesh((s) => s.mesh)
  const outageAt = useMesh((s) => s.outageAt)
  const reduceMotion = useStore((s) => s.reduceMotion)
  const mode = useStore((s) => s.mode)
  const liveLatest = useLive((s) => s.latest)
  const styleReady = useRef(false)
  const [ver, setVer] = useState(0) // bumps when the style is (re)loaded so data layers are pushed again

  // ---------------------------------------------------------------- init
  useEffect(() => {
    maplibregl.setWorkerUrl(maplibreWorkerUrl)
    registerTerrainProtocol()
    const fromUrl = parseHashCamera()
    const m = new maplibregl.Map({
      container: el.current!, style: buildStyle(useStore.getState().theme, useStore.getState().exaggeration, SAFE),
      center: fromUrl?.center ?? [80, 18], zoom: fromUrl?.zoom ?? 1.3, pitch: fromUrl?.pitch ?? 0, bearing: fromUrl?.bearing ?? 0,
      maxPitch: 78, attributionControl: { compact: true }, canvasContextAttributes: { antialias: true },
    })
    mapRef.current = m
    if (import.meta.env.DEV) (window as unknown as { __trnMap: unknown }).__trnMap = m // debugging handle (dev only)
    installIconLoader(m, () => useStore.getState().theme)
    m.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'top-right')
    m.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-right')
    m.on('load', () => {
      styleReady.current = true
      if (!fromUrl) {
        const rm = useStore.getState().reduceMotion
        if (rm) m.jumpTo(INDIA_VIEW)
        else m.flyTo({ ...INDIA_VIEW, duration: 2800, essential: true, curve: 1.3 })
      }
      setVer((v) => v + 1)
    })
    // fps meter (status strip)
    let frames = 0, last = performance.now()
    m.on('render', () => {
      frames++
      const now = performance.now()
      if (now - last > 1000) { useCursor.setState({ fps: Math.round((frames * 1000) / (now - last)) }); frames = 0; last = now }
    })
    // cursor readout: lat/lon, elevation, slope and aspect from the DEM (throttled)
    let busy = false
    m.on('mousemove', (e) => {
      useCursor.setState({ lon: e.lngLat.lng, lat: e.lngLat.lat, zoom: m.getZoom() })
      if (busy) return
      busy = true
      const z = Math.min(12, Math.max(3, Math.round(m.getZoom()) + 1))
      const { lng, lat } = e.lngLat
      const dm = 60, dLon = dm / (111320 * Math.cos((lat * Math.PI) / 180)), dLat = dm / 110540
      Promise.all([elevation(lng, lat, z), elevation(lng + dLon, lat, z), elevation(lng, lat + dLat, z)]).then(([e0, ex, ey]) => {
        const gx = (ex - e0) / dm, gy = (ey - e0) / dm
        const slope = (Math.atan(Math.hypot(gx, gy)) * 180) / Math.PI
        const aspect = (((Math.atan2(-gx, -gy) * 180) / Math.PI) + 360) % 360
        useCursor.setState({ elev: e0, slope: z >= 9 ? slope : null, aspect: z >= 9 ? aspect : null })
      }).finally(() => setTimeout(() => (busy = false), 80))
    })
    m.on('click', (e) => {
      const st = useStore.getState()
      const hit = m.queryRenderedFeatures(e.point, { layers: ['alerts', 'cameras', 'lora-nodes'] })
      const f = hit[0]
      if (f?.layer.id === 'lora-nodes') {
        const id = String(f.properties?.id)
        const d = new Set(st.disabledNodes)
        if (d.has(id)) d.delete(id); else d.add(id)
        useStore.setState({ disabledNodes: [...d], rightTab: 'lora', rightOpen: true })
        return
      }
      if (f) { useStore.setState({ selected: String(f.properties?.id), rightTab: 'evidence', rightOpen: true }); return }
      if (st.igniteArmed) {
        const n = st.customIncidents.length + 1
        useStore.setState({ igniteArmed: false, customIncidents: [...st.customIncidents, {
          id: `U${n}`, label: `Operator-placed fire ${n} (synthetic)`, kind: 'fire', lon: e.lngLat.lng, lat: e.lngLat.lat,
          startMin: Math.round(st.simMin / 2) * 2, Qc_kW_m: 1000, Q_kW: 5000, D_m: 5, ros_m_min: 8, cameras: 1, iot: 1 }] })
        return
      }
      setData(m, 'pin', fc([pt(e.lngLat.lng, e.lngLat.lat)]))
    })
    m.on('dblclick', (e) => {
      const hit = m.queryRenderedFeatures(e.point, { layers: ['alerts'] })
      if (hit[0]) { e.preventDefault(); useStore.setState({ diveSite: String(hit[0].properties?.id), selected: String(hit[0].properties?.id), rightTab: 'evidence' }) }
    })
    let t: number | undefined
    m.on('moveend', () => {
      clearTimeout(t)
      t = window.setTimeout(() => {
        const c = m.getCenter()
        const base = location.hash.split('?')[0] || '#console'
        const q = new URLSearchParams(location.hash.split('?')[1] ?? '')
        q.set('c', [c.lng.toFixed(4), c.lat.toFixed(4), m.getZoom().toFixed(2), m.getPitch().toFixed(0), m.getBearing().toFixed(0)].join(','))
        q.set('s', useStore.getState().scenarioId); q.set('t', String(useStore.getState().simMin))
        history.replaceState(null, '', `${base}?${q.toString()}`)
      }, 400)
    })
    // pulse animation for warning / emergency beacons: 0.6 Hz (photosensitivity-safe, < 3 Hz)
    let raf = 0, lastPulse = 0
    const tick = (now: number) => {
      raf = requestAnimationFrame(tick)
      if (now - lastPulse < 50) return // ~20 updates/s is enough for a 0.6 Hz pulse and saves GPU time
      lastPulse = now
      if (!styleReady.current || useStore.getState().reduceMotion || !m.getLayer('alerts-pulse')) return
      const ph = (performance.now() / 1650) % 1
      m.setPaintProperty('alerts-pulse', 'circle-radius', 12 + 22 * ph)
      m.setPaintProperty('alerts-pulse', 'circle-opacity', 0.32 * (1 - ph))
    }
    raf = requestAnimationFrame(tick)
    return () => { cancelAnimationFrame(raf); m.remove(); mapRef.current = null }
  }, [])

  // ---------------------------------------------------------------- theme
  useEffect(() => {
    const m = mapRef.current
    if (!m || !styleReady.current) return
    styleReady.current = false
    m.setStyle(buildStyle(theme, useStore.getState().exaggeration, SAFE), { diff: false })
    m.once('style.load', () => { styleReady.current = true; setVer((v) => v + 1) })
  }, [theme])
  useEffect(() => {
    const m = mapRef.current
    if (m && styleReady.current && m.getSource('demTerrain') && !SAFE) m.setTerrain({ source: 'demTerrain', exaggeration })
  }, [exaggeration, ver])
  useEffect(() => { demConfig.allowOnline = online }, [online])

  // ---------------------------------------------------------------- data layers
  useEffect(() => {
    const m = mapRef.current
    if (!m || !styleReady.current || !result || mode !== 'SIM') return
    const sc = currentScenario()
    const now = allNow(result, simMin)
    const col = SEV_COLORS[theme]
    const colors = ['', col.watch, col.warning, col.emergency]
    const alerts = now.filter((n) => n.level >= 1).map((n) => pt(n.site.lon, n.site.lat, {
      id: n.site.id, level: n.level, u: n.u, color: colors[n.level],
      icon: `sev-${SEV_NAME[n.level]}${showTruth && n.falseAlarm ? '-hollow' : ''}`,
    }))
    setData(m, 'alerts', fc(layers.alerts ? alerts : []))
    setData(m, 'cameras', fc(layers.cameras ? now.filter((n) => n.level === 0 && n.site.hazard === 'FIRE').map((n) => pt(n.site.lon, n.site.lat, { id: n.site.id })) : []))
    setData(m, 'missed', fc(showTruth ? now.filter((n) => n.active && n.level === 0).map((n) => pt(n.site.lon, n.site.lat)) : []))
    const sel = result.sites.find((s) => s.id === selected)
    setData(m, 'selection', fc(sel ? [pt(sel.lon, sel.lat)] : []))
    // fire perimeters (SURROGATE), flame band (Heskestad L, true metres), wind field
    const perims: GeoJSON.Feature[] = [], flames: GeoJSON.Feature[] = [], winds: GeoJSON.Feature[] = [], cones: GeoJSON.Feature[] = []
    if (layers.perimeter) for (const inc of sc.incidents) {
      const pm = perimeter(inc, sc, simMin, params)
      if (!pm) continue
      perims.push({ type: 'Feature', properties: { id: inc.id }, geometry: { type: 'Polygon', coordinates: [pm.outer] } })
      flames.push({ type: 'Feature', properties: { h: pm.flameM }, geometry: { type: 'Polygon', coordinates: [pm.outer, [...pm.inner].reverse()] } })
    }
    const focus = sel ?? result.sites.find((s) => s.kind === 'incident')
    if (layers.wind && focus) {
      const rot = (sc.weather.wind_from_deg + 180) % 360
      for (let i = -3; i <= 3; i++) for (let j = -3; j <= 3; j++) { const [lo, la] = offset(focus.lon, focus.lat, i * 1600, j * 1600); winds.push(pt(lo, la, { rot })) }
    }
    for (const s of result.sites) if (s.kind === 'incident' && s.incident && s.idx > 0 && (s.lon !== s.incident.lon || s.lat !== s.incident.lat) && s.hazard === 'FIRE') {
      const dx = (s.incident.lon - s.lon) * Math.cos((s.lat * Math.PI) / 180), dy = s.incident.lat - s.lat
      const brg = Math.atan2(dx, dy), half = (30 * Math.PI) / 180, R = 3500
      const ring: [number, number][] = [[s.lon, s.lat]]
      for (let k = 0; k <= 12; k++) { const a = brg - half + (k / 12) * 2 * half; ring.push(offset(s.lon, s.lat, R * Math.sin(a), R * Math.cos(a))) }
      ring.push([s.lon, s.lat])
      cones.push({ type: 'Feature', properties: {}, geometry: { type: 'Polygon', coordinates: [ring] } })
    }
    setData(m, 'perimeter', fc(perims)); setData(m, 'flame', fc(flames)); setData(m, 'wind', fc(winds)); setData(m, 'cone', fc(diveSite ? cones : []))
    // network: synthetic towers go dark during the outage
    const down = networkDown(sc, simMin, outage)
    setData(m, 'towers', fc(layers.towers && mesh ? mesh.layout.towers.map((t) => pt(t.lon, t.lat, { icon: down ? 'tower-off' : 'tower-on' })) : []))
  }, [result, simMin, selected, showTruth, layers, params, theme, diveSite, outage, mesh, mode, ver])

  // ---------------------------------------------------------------- LIVE / REPLAY beacons (same layers, different origin)
  useEffect(() => {
    const m = mapRef.current
    if (!m || !styleReady.current || mode === 'SIM') return
    const col = SEV_COLORS[theme]
    const colors = ['', col.watch, col.warning, col.emergency]
    const tier = { GREEN: 0, YELLOW: 1, ORANGE: 2, RED: 3 } as const
    const ev = Object.values(liveLatest)
    setData(m, 'alerts', fc(ev.filter((e) => tier[e.decision.tier] >= 1).map((e) => pt(e.location.lon, e.location.lat, {
      id: e.source_id, level: tier[e.decision.tier], u: e.fusion.uncertainty, color: colors[tier[e.decision.tier]], icon: `sev-${SEV_NAME[tier[e.decision.tier]]}` }))))
    setData(m, 'cameras', fc(ev.filter((e) => tier[e.decision.tier] === 0).map((e) => pt(e.location.lon, e.location.lat, { id: e.source_id }))))
    const sel = ev.find((e) => e.source_id === selected)
    setData(m, 'selection', fc(sel ? [pt(sel.location.lon, sel.location.lat)] : []))
    for (const id of ['missed', 'perimeter', 'flame', 'wind', 'cone']) setData(m, id, fc([]))
  }, [mode, liveLatest, selected, theme, ver])

  // ---------------------------------------------------------------- LoRa mesh layers + pulse animation
  useEffect(() => {
    const m = mapRef.current
    if (!m || !styleReady.current) return
    if (!mesh || !layers.lora) { for (const id of ['loraLinks', 'loraRoutes', 'loraNodes', 'villages', 'pulses']) setData(m, id, fc([])); return }
    const disabled = new Set(useStore.getState().disabledNodes)
    const byId = new Map<string, { lon: number; lat: number }>([...mesh.layout.nodes, ...mesh.layout.villages].map((n) => [n.id, n]))
    const line = (a: string, b: string, props: Record<string, unknown>): GeoJSON.Feature => ({ type: 'Feature', properties: props,
      geometry: { type: 'LineString', coordinates: [[byId.get(a)!.lon, byId.get(a)!.lat], [byId.get(b)!.lon, byId.get(b)!.lat]] } })
    setData(m, 'loraLinks', fc(mesh.links.filter((l) => !disabled.has(l.a) && !disabled.has(l.b)).map((l) => line(l.a, l.b, { los: l.los }))))
    const routes: GeoJSON.Feature[] = []
    for (const r of mesh.results) if (r.path.length > 1 && !r.channel.startsWith('runner')) for (let k = 0; k + 1 < r.path.length; k++) routes.push(line(r.path[k], r.path[k + 1], {}))
    const down = networkDown(currentScenario(), useStore.getState().simMin, outage)
    setData(m, 'loraRoutes', fc(down ? routes : []))
    setData(m, 'loraNodes', fc(mesh.layout.nodes.map((n) => pt(n.lon, n.lat, { id: n.id, icon: disabled.has(n.id) ? 'lora-dead' : `lora-${n.kind}` }))))
    const deadline = num(useStore.getState().params, 'lora.deadline')
    const res = new Map(mesh.results.map((r) => [r.id, r]))
    setData(m, 'villages', fc(mesh.layout.villages.map((v) => {
      const r = res.get(v.id)
      return pt(v.lon, v.lat, { id: v.id, icon: down && (!r || r.minutes === null || r.minutes > deadline) ? 'village-late' : 'village' })
    })))
    if (!down || outageAt === null || reduceMotion) { setData(m, 'pulses', fc([])); return }
    let raf = 0
    const step = () => {
      const tS = (performance.now() - outageAt) / 1000
      const pts: GeoJSON.Feature[] = []
      for (const r of mesh.results) {
        if (r.channel.startsWith('runner') || r.path.length < 2) continue
        const hop = Math.floor(tS / mesh.hopS)
        if (hop >= r.path.length - 1) continue
        const f = (tS - hop * mesh.hopS) / mesh.hopS
        const a = byId.get(r.path[hop])!, b = byId.get(r.path[hop + 1])!
        pts.push(pt(a.lon + f * (b.lon - a.lon), a.lat + f * (b.lat - a.lat)))
      }
      setData(m, 'pulses', fc(pts))
      if (pts.length) raf = requestAnimationFrame(step)
    }
    raf = requestAnimationFrame(step)
    return () => cancelAnimationFrame(raf)
  }, [mesh, layers.lora, outage, outageAt, simMin, reduceMotion, ver])

  // ---------------------------------------------------------------- dive (national -> local terrain scene)
  useEffect(() => {
    const m = mapRef.current
    if (!m) return
    const rm = useStore.getState().reduceMotion
    if (!diveSite) return
    const s = useStore.getState().result?.sites.find((x) => x.id === diveSite)
    if (!s) return
    const sc = currentScenario()
    const opts = { center: [s.lon, s.lat] as [number, number], zoom: 12.8, pitch: 68, bearing: (sc.weather.wind_from_deg + 160) % 360 }
    if (rm) m.jumpTo(opts); else m.flyTo({ ...opts, duration: 3200, curve: 1.6, essential: true })
  }, [diveSite])
  useEffect(() => {
    const m = mapRef.current
    if (!m || !styleReady.current) return
    for (const [layer, on] of [['relief', layers.relief], ['hillshade', layers.relief], ['states', layers.states], ['rivers', layers.rivers]] as const)
      if (m?.getLayer(layer)) m.setLayoutProperty(layer, 'visibility', on ? 'visible' : 'none')
  }, [layers, theme, ver])

  // MapLibre sets `position: relative` on its container, so the container must not be the absolutely positioned element
  return (
    <div className="absolute inset-0">
      <div ref={el} className="h-full w-full" aria-label="3D map of India" role="application" />
    </div>
  )
}
