// Scenario engine (SIMULATION mode). Deterministic from (scenario seed, parameter values, technique).
// Evidence: every camera observation is ONE REAL row of the evidence bank (fire_cnn + zeroshot + clip_probe scored the same
// image, cross-fit calibrated OOF; tools/export_evidence_bank.py). Rows are drawn conditioned on the scenario ground truth.
// SIMULATED parts are labelled: visibility ramp after ignition, IoT node readings, tilt readings, positions of all sites.
import bank from '../data/evidence_bank.json'
import regionsJson from '../data/regions.json'
import { clip, rng } from './math'
import { fireGate } from './firephys'
import { geoGate, transientHeadMultipulse } from './geophys'
import { fuse, type Expert, type FusionOut, type StackModel, type Technique } from './fusion'
import { decide, levelIdx, type DecisionOut } from './decision'
import { num, type ParamValues } from './params'

export interface Incident {
  id: string; label: string; kind: 'fire' | 'confuser' | 'landslide'; lon: number; lat: number; startMin: number
  Qc_kW_m?: number; Q_kW?: number; D_m?: number; ros_m_min?: number; cameras: number; iot: number; fuel?: string; confuser?: string
  slope?: { beta_deg: number; c_prime: number; z: number; D0: number; K_z: number; psi_steady: number; high_susceptibility: boolean }
}
export interface Scenario {
  id: string; title: string; summary: string; seed: number; regionId: string | null; hazard: 'FIRE' | 'LANDSLIDE'
  durationMin: number; stepMin: number; weather: { wind_ms: number; wind_from_deg: number; temp_K: number }
  incidents: Incident[]; background: { count: number; regionIds?: string[]; national?: boolean; iotShare: number }
  network: { outageAtMin: number | null }; lora?: boolean; rain?: [number, number][]; planned?: string[]
}
export interface Site {
  idx: number; id: string; label: string; lon: number; lat: number; kind: 'incident' | 'background'; hazard: 'FIRE' | 'LANDSLIDE'
  incident?: Incident; truthStart: number | null; confuserStart: number | null; nIoT: number; regionId: string | null
}
export type Town = [string, number, number, string, number]

const COLS = bank.columns
const ROWS = bank.rows as number[][]
const ci = (n: string) => COLS.indexOf(n)
const IY = ci('y'), ICF = ci('cal_fire_cnn'), ICZ = ci('cal_zeroshot'), ICP = ci('cal_clip_probe')
const IRF = ci('raw_fire_cnn'), IRZ = ci('raw_zeroshot'), IRP = ci('raw_clip_probe')
const POS: number[] = [], NEG: number[] = []
ROWS.forEach((r, i) => (r[IY] === 1 ? POS : NEG).push(i))
// "hard negatives": the top decile of y = 0 rows by mean CLIP score (real images that look most like fire to the models)
const HARD = [...NEG].sort((a, b) => ROWS[b][ICZ] + ROWS[b][ICP] - (ROWS[a][ICZ] + ROWS[a][ICP])).slice(0, Math.round(NEG.length / 10))
export const STACK = bank.stack as StackModel
export const BANK_INFO = { n: bank.n, nPos: bank.n_pos, nBlocks: bank.n_blocks, runIds: bank.run_ids, source: bank.source, nHard: HARD.length }

const REGIONS = Object.fromEntries(regionsJson.regions.map((r) => [r.id, r]))
const PI_BANK = bank.n_pos / bank.n
/** PROPOSED prior-shift correction (Saerens et al. 2002), identity when target prior = bank prevalence. */
export const priorShift = (p: number, target: number) => {
  if (Math.abs(target - PI_BANK) < 1e-9) return p
  const a = p * (target / PI_BANK), b = (1 - p) * ((1 - target) / (1 - PI_BANK))
  return a / (a + b)
}
const h2 = (p: number) => { const q = clip(p, 1e-6, 1 - 1e-6); return -(q * Math.log2(q) + (1 - q) * Math.log2(1 - q)) }
const hash = (...xs: number[]) => xs.reduce((h, x) => Math.imul(h ^ (x | 0), 2654435761) >>> 0, 0x9e3779b9)
const VIS_RAMP_MIN = 10 // SIMULATED: a new fire becomes fully visible to a camera over 10 minutes
const IOT_DELAY_MIN = 6 // SIMULATED: smoke/heat reaches the IoT nodes 6 minutes after ignition

/** Offset a lon/lat by metres east/north. */
export const offset = (lon: number, lat: number, e: number, n: number): [number, number] =>
  [lon + e / (111320 * Math.cos((lat * Math.PI) / 180)), lat + n / 110540]

export function buildSites(sc: Scenario, towns: Town[]): Site[] {
  const R = rng(sc.seed)
  const sites: Site[] = []
  const regionOf = (lon: number, lat: number) =>
    regionsJson.regions.find((r) => lon >= r.bbox[0] && lon <= r.bbox[2] && lat >= r.bbox[1] && lat <= r.bbox[3])?.id ?? null
  for (const inc of sc.incidents) {
    const views = Math.max(inc.cameras, inc.kind === 'landslide' ? 1 : 1)
    for (let k = 0; k < views; k++) {
      const [lon, lat] = k === 0 ? [inc.lon, inc.lat] : offset(inc.lon, inc.lat, R.uniform(-1500, 1500), R.uniform(-1500, 1500))
      sites.push({
        idx: sites.length, id: `${inc.id}${views > 1 ? `-C${k + 1}` : ''}`, label: inc.label, lon, lat, kind: 'incident', hazard: inc.kind === 'landslide' ? 'LANDSLIDE' : 'FIRE',
        incident: inc, truthStart: inc.kind === 'fire' ? inc.startMin : null, confuserStart: inc.kind === 'confuser' ? inc.startMin : null,
        nIoT: k === 0 ? inc.iot : 0, regionId: regionOf(lon, lat),
      })
    }
  }
  for (let b = 0; b < sc.background.count; b++) {
    let lon: number, lat: number
    if (sc.background.national && towns.length) {
      const t = towns[R.int(Math.min(towns.length, 900))]
      ;[lon, lat] = offset(t[2], t[1], R.uniform(-3000, 3000), R.uniform(-3000, 3000))
    } else {
      const reg = REGIONS[sc.background.regionIds?.[b % (sc.background.regionIds?.length || 1)] ?? sc.regionId ?? '']
      const bb = reg?.bbox ?? [77, 20, 78, 21]
      lon = R.uniform(bb[0], bb[2]); lat = R.uniform(bb[1], bb[3])
    }
    sites.push({ idx: sites.length, id: `CAM-${String(b + 1).padStart(3, '0')}`, label: 'Camera, no incident', lon, lat, kind: 'background', hazard: 'FIRE',
      truthStart: null, confuserStart: null, nIoT: R.next() < sc.background.iotShare ? 1 : 0, regionId: regionOf(lon, lat) })
  }
  return sites
}

/** Evidence-bank row for (site, step), deterministic. Also returns whether the hazard is truly active. */
function rowAt(sc: Scenario, s: Site, step: number) {
  const t = step * sc.stepMin
  const R = rng(hash(sc.seed, s.idx, step))
  const active = s.truthStart !== null && t >= s.truthStart
  let pool = NEG
  if (active) pool = R.next() < clip((t - s.truthStart! + sc.stepMin) / VIS_RAMP_MIN, 0, 1) ? POS : NEG
  else if (s.confuserStart !== null && t >= s.confuserStart) pool = HARD
  return { row: ROWS[pool[R.int(pool.length)]], active, R }
}

export interface SiteStep {
  t: number; active: boolean; experts: Expert[]; fusion: FusionOut; decision: DecisionOut
  validator?: { confirmed: boolean; conf: number; support: number; window: number[] }
  physics: Record<string, number | string | boolean | null>
}

export const primaryQc = (sc: Scenario) => sc.incidents.find((i) => i.kind === 'fire' && i.Qc_kW_m)?.Qc_kW_m ?? 800
/** Parameter values a scenario sets when it is loaded (Scenario Director inputs, not repo defaults). */
export const primaryFire = (sc: Scenario) => sc.incidents.find((i) => i.kind === 'fire')
export const scenarioInputs = (sc: Scenario): ParamValues => {
  const f = primaryFire(sc)
  return { 'fire.wind_ms': sc.weather.wind_ms, 'fire.Qc_kW_m': primaryQc(sc), 'fire.T_inf': sc.weather.temp_K,
    ...(f?.Q_kW ? { 'fire.Q_kW': f.Q_kW } : {}), ...(f?.D_m ? { 'fire.D_m': f.D_m } : {}), ...(f?.ros_m_min ? { 'sur.ros': f.ros_m_min } : {}) }
}

function rainAt(sc: Scenario, tMin: number) {
  const r = sc.rain ?? []
  let I = 0
  for (const [t0, i] of r) if (tMin >= t0) I = i
  return I
}

export function evalSiteStep(sc: Scenario, s: Site, step: number, P: ParamValues, tech: Technique): SiteStep {
  const t = step * sc.stepMin
  const fusionP = { tau: num(P, 'fusion.tau'), lambda: num(P, 'fusion.lambda'), kappa: num(P, 'fusion.kappa') }
  const decP = { C_FA: num(P, 'cost.C_FA'), C_miss: num(P, 'cost.C_miss'), orangeMult: num(P, 'dec.orange_mult'), redMult: num(P, 'dec.red_mult'), uncertain: num(P, 'dec.uncertain') }
  const shP = { tilt: num(P, 'shield.tilt'), rain24: num(P, 'shield.rain24') }
  if (s.hazard === 'LANDSLIDE') return evalLandslide(sc, s, step, P, tech, fusionP, decP, shP)
  const W = Math.round(num(P, 'cctv.window')), M = Math.round(num(P, 'cctv.min_frames')), thr = num(P, 'cctv.thr')
  const window: number[] = []
  for (let k = Math.max(0, step - W + 1); k <= step; k++) window.push(rowAt(sc, s, k).row[ICF])
  const prior = num(P, 'fusion.prior')
  for (let k = 0; k < window.length; k++) window[k] = priorShift(window[k], prior)
  const support = window.filter((c) => c >= thr)
  const confirmed = support.length >= M
  const conf = confirmed ? support.reduce((a, b) => a + b, 0) / support.length : 0
  const { row, active, R } = rowAt(sc, s, step)
  // SIMULATED IoT smoke/heat nodes
  const nodes: number[] = []
  for (let k = 0; k < s.nIoT; k++) {
    const hot = active && t - s.truthStart! >= IOT_DELAY_MIN
    nodes.push(clip(hot ? 0.78 + 0.12 * R.normal() : 0.05 + 0.05 * Math.abs(R.normal()), 0, 1))
  }
  const agree = nodes.filter((p) => p > 0.5).length
  const inc = s.incident
  // Scenario Director: fire.Qc_kW_m is set to the primary incident's Q_c on load; other incidents scale in proportion
  const qRef = primaryQc(sc)
  const Qc = inc?.kind === 'fire' && active && inc.Qc_kW_m ? inc.Qc_kW_m * (num(P, 'fire.Qc_kW_m') / qRef) : null
  const gate = fireGate(conf, { Qc, U: Qc != null ? num(P, 'fire.wind_ms') : null, multiNode: agree >= 2 },
    { ncFull: num(P, 'fire.nc_full'), cMin: num(P, 'fire.c_min'), uBase: num(P, 'fire.u_base'), iotBonus: num(P, 'fire.iot_bonus') })
  const pz = priorShift(row[ICZ], prior), pc = priorShift(row[ICP], prior)
  const experts: Expert[] = [
    { id: 'fire_cnn', label: 'CCTV fire CNN + temporal validator + physics gate', source: 'fire_cnn', p: gate.p, u: gate.u, c: gate.c,
      r: num(P, 'trust.fire_cnn'), cls: 'data', available: true, raw: row[IRF], origin: 'REAL-OOF', status: 'IMPLEMENTED',
      note: confirmed ? `validated: ${support.length}/${window.length} frames ≥ ${thr}` : `not confirmed: ${support.length}/${window.length} frames ≥ ${thr}` },
    { id: 'zeroshot', label: 'CLIP zero-shot layer', source: 'zeroshot', p: pz, u: 0.5 * h2(pz), c: 1, r: num(P, 'trust.zeroshot'), cls: 'data',
      available: true, raw: row[IRZ], origin: 'REAL-OOF', status: 'IMPLEMENTED' },
    { id: 'clip_probe', label: 'CLIP few-shot probe', source: 'clip_probe', p: pc, u: 0.5 * h2(pc), c: 1, r: num(P, 'trust.clip_probe'), cls: 'data',
      available: true, raw: row[IRP], origin: 'REAL-OOF', status: 'IMPLEMENTED' },
  ]
  if (s.nIoT > 0) {
    const pi = nodes.slice().sort((a, b) => a - b)[Math.floor(nodes.length / 2)]
    experts.push({ id: 'iot', label: `IoT smoke and heat nodes (${s.nIoT})`, source: 'iot', p: pi, u: 0.5 * h2(pi), c: 1, r: num(P, 'trust.iot'), cls: 'data',
      available: true, origin: 'SIMULATED', status: 'IMPLEMENTED', note: `${agree} of ${s.nIoT} nodes above 0.5` })
  }
  experts.push(
    { id: 'satellite', label: 'Satellite active-fire / EO head', source: 'eo', p: 0, u: 1, c: 1, r: 0, cls: 'data', available: false, origin: 'SIMULATED', status: 'PLANNED',
      note: 'EO heads not admitted; not part of this prototype run' },
    { id: 'anomaly', label: 'Anomaly ensemble (ws8)', source: 'anomaly', p: 0, u: 1, c: 1, r: 0, cls: 'data', available: false, origin: 'SIMULATED', status: 'PLANNED',
      note: 'Implemented in numpy, not wired to a fire stream yet' },
  )
  const fusion = fuse(experts, tech, fusionP, STACK)
  if (fusion.technique === 'STACK') fusion.p = priorShift(fusion.p, prior)
  const decision = decide(fusion.p, fusion.uStar, true, { fireMultiNode: agree >= 2 }, decP, shP)
  return { t, active, experts, fusion, decision, validator: { confirmed, conf, support: support.length, window },
    physics: { Nc: gate.Nc, consistency: gate.c, iot_agree: agree, Qc } }
}

function evalLandslide(sc: Scenario, s: Site, step: number, P: ParamValues, tech: Technique,
  fusionP: { tau: number; lambda: number; kappa: number }, decP: Parameters<typeof decide>[4], shP: { tilt: number; rain24: number }): SiteStep {
  const t = step * sc.stepMin
  const sl = s.incident!.slope!
  const st = landslideState(sc, s, t, P)
  const R = rng(hash(sc.seed, s.idx, step))
  const tilts: number[] = []
  for (let k = 0; k < s.nIoT; k++) tilts.push(Math.max(0, 0.3 + 25 * Math.max(0, 1.02 - st.trueFS) + 0.4 * R.normal()))
  const tmax = Math.max(0, ...tilts)
  const agree = tilts.filter((x) => x > shP.tilt).length
  const experts: Expert[] = [
    { id: 'geo_phys', label: 'Landslide physics gate (FS + Caine)', source: 'geo_phys', p: st.gate.p_phys, u: st.gate.u, c: st.gate.c, r: 1, cls: 'A', available: true,
      origin: 'SIMULATED', status: 'IMPLEMENTED', note: `FS ${st.gate.FS.toFixed(3)} · Caine ratio ${st.gate.caine?.toFixed(2)}` },
    { id: 'iot_tilt', label: `Tilt nodes (${s.nIoT})`, source: 'iot', p: clip(tmax / (2 * shP.tilt), 0, 1), u: 0.2, c: 1, r: num(P, 'trust.iot'), cls: 'data', available: s.nIoT > 0,
      origin: 'SIMULATED', status: 'IMPLEMENTED', note: `max ${tmax.toFixed(1)} deg/day, ${agree} nodes above ${shP.tilt}` },
  ]
  const fusion = fuse(experts, tech === 'STACK' ? 'FM-1' : tech, fusionP)
  const decision = decide(fusion.p, fusion.uStar, true, { FS: st.gate.FS, tilt: tmax, nodesAgree: agree, rain24: st.rain24, highSusc: sl.high_susceptibility }, decP, shP)
  return { t, active: s.truthStart !== null && t >= s.truthStart, experts, fusion, decision,
    physics: { FS: st.gate.FS, caine: st.gate.caine, psi_m: st.psi, u_w_kPa: st.gate.u_w, rain_mm_h: rainAt(sc, t), rain24_mm: st.rain24, tilt_max: tmax } }
}

function landslideState(sc: Scenario, s: Site, t: number, P: ParamValues, useDefaults = false): { gate: ReturnType<typeof geoGate>; psi: number; rain24: number; trueFS: number } {
  const sl = s.incident!.slope!
  const steps: [number, number][] = (sc.rain ?? []).map(([t0, i]) => [t0 / 60, Math.min(i / 1000, sl.K_z)])
  const D0 = useDefaults ? sl.D0 : num(P, 'geo.D0')
  const z = useDefaults ? sl.z : num(P, 'geo.z')
  const psi = sl.psi_steady + transientHeadMultipulse(z, t / 60, steps, D0, sl.K_z, sl.beta_deg)
  let cum = 0
  for (let m = 0; m < t; m += 10) cum += (rainAt(sc, m) * 10) / 60
  const Dh = Math.max(t / 60, 1e-3)
  const gate = geoGate({ c_prime: sl.c_prime, phi_prime_deg: useDefaults ? 32 : num(P, 'geo.phi'), gamma: useDefaults ? 19 : num(P, 'geo.gamma'), z,
    beta_deg: sl.beta_deg, u_w: 9.81 * Math.max(psi, 0), I_mm_h: cum / Dh, D_hours: Dh,
    caine_a: useDefaults ? 14 : num(P, 'geo.caine_a'), caine_b: useDefaults ? 0.39 : num(P, 'geo.caine_b') },
    { k_fs: useDefaults ? 4 : num(P, 'geo.k_fs'), leadH: num(P, 'geo.lead_h') })
  const trueFS: number = useDefaults ? gate.FS : landslideState(sc, s, t, P, true).gate.FS
  return { gate, psi, rain24: cum, trueFS }
}

export interface RunResult {
  scenarioId: string; nSteps: number; stepMin: number; sites: Site[]
  p: Float32Array; level: Uint8Array; u: Float32Array; flags: Uint8Array // flags: 1 uncertain, 2 truth active, 4 shield raised, 8 validated
  metrics: Metrics; roc: { fpr: number[]; tpr: number[]; auc: number; op: { fpr: number; tpr: number } }; ms: number
}
export interface LevelMetrics {
  detected: number; missed: number; falseAlarmSites: number; falseAlarmEpisodes: number; alertEpisodes: number
  medianTTA: number | null; p90TTA: number | null; alertsPerHour: number; tta: Record<string, number | null>; lead: Record<string, number | null>
}
export interface Metrics { incidents: number; watch: LevelMetrics; warning: LevelMetrics }
export const LANDSLIDE_LEAD_WINDOW_MIN = 12 * 60

function levelMetrics(sc: Scenario, sites: Site[], nSteps: number, level: Uint8Array, minLevel: number): LevelMetrics {
  const tta: Record<string, number | null> = {}, lead: Record<string, number | null> = {}
  let faSites = 0, faEp = 0, ep = 0
  const byInc = new Map<string, Site[]>()
  for (const s of sites) if (s.incident && s.truthStart !== null) byInc.set(s.incident.id, [...(byInc.get(s.incident.id) ?? []), s])
  const firstHit = new Map<string, number>()
  for (const s of sites) {
    let prev = false, faHere = false
    for (let k = 0; k < nSteps; k++) {
      const t = k * sc.stepMin, a = level[s.idx * nSteps + k] >= minLevel
      if (a && !prev) {
        ep++
        const early = s.hazard === 'LANDSLIDE' && s.truthStart !== null && t >= s.truthStart - LANDSLIDE_LEAD_WINDOW_MIN && t <= s.truthStart
        const valid = s.truthStart !== null && (t >= s.truthStart || early)
        if (!valid) { faEp++; faHere = true }
        const key = s.incident?.id
        if (valid && key && !firstHit.has(`${key}|${s.idx}`)) firstHit.set(`${key}|${s.idx}`, t)
      }
      prev = a
    }
    if (faHere && s.truthStart === null) faSites++
  }
  for (const [id, ss] of byInc) {
    const hits = ss.map((s) => firstHit.get(`${id}|${s.idx}`)).filter((x): x is number => x !== undefined)
    const first = hits.length ? Math.min(...hits) : null
    const start = ss[0].truthStart!
    if (ss[0].hazard === 'LANDSLIDE') { lead[id] = first === null ? null : start - first; tta[id] = first === null ? null : Math.max(0, first - start) }
    else tta[id] = first === null ? null : first - start
  }
  const v = Object.values(tta).filter((x): x is number => x !== null).sort((a, b) => a - b)
  const q = (f: number) => (v.length ? v[Math.min(v.length - 1, Math.floor(f * (v.length - 1) + 0.5))] : null)
  return { detected: v.length, missed: byInc.size - v.length, falseAlarmSites: faSites, falseAlarmEpisodes: faEp, alertEpisodes: ep,
    medianTTA: q(0.5), p90TTA: q(0.9), alertsPerHour: ep / (sc.durationMin / 60), tta, lead }
}

function computeMetrics(sc: Scenario, sites: Site[], nSteps: number, level: Uint8Array): Metrics {
  const inc = new Set(sites.filter((s) => s.incident && s.truthStart !== null).map((s) => s.incident!.id)).size
  return { incidents: inc, watch: levelMetrics(sc, sites, nSteps, level, 1), warning: levelMetrics(sc, sites, nSteps, level, 2) }
}

export function run(sc: Scenario, sites: Site[], P: ParamValues, tech: Technique): RunResult {
  const t0 = performance.now()
  const nSteps = Math.floor(sc.durationMin / sc.stepMin) + 1
  // landslide ground truth: first time the DEFAULT-parameter slope reaches FS < 1 (fixed, independent of the sliders)
  for (const s of sites) if (s.hazard === 'LANDSLIDE' && s.truthStart === null) {
    for (let k = 0; k < nSteps; k++) if (landslideState(sc, s, k * sc.stepMin, P, true).gate.FS < 1) { s.truthStart = k * sc.stepMin; break }
  }
  const N = sites.length * nSteps
  const p = new Float32Array(N), level = new Uint8Array(N), u = new Float32Array(N), flags = new Uint8Array(N)
  for (const s of sites) for (let k = 0; k < nSteps; k++) {
    const r = evalSiteStep(sc, s, k, P, tech), i = s.idx * nSteps + k
    p[i] = r.fusion.p; level[i] = levelIdx(r.decision.level); u[i] = r.fusion.uStar
    flags[i] = (r.decision.uncertain ? 1 : 0) | (r.active ? 2 : 0) | (r.decision.shield.raised ? 4 : 0) | (r.validator?.confirmed ? 8 : 0)
  }
  const metrics = computeMetrics(sc, sites, nSteps, level)
  const roc = computeRoc(p, flags, sites, nSteps, num(P, 'cost.C_FA') / (num(P, 'cost.C_FA') + num(P, 'cost.C_miss')))
  return { scenarioId: sc.id, nSteps, stepMin: sc.stepMin, sites, p, level, u, flags, metrics, roc, ms: performance.now() - t0 }
}

function computeRoc(p: Float32Array, flags: Uint8Array, sites: Site[], nSteps: number, pStar: number) {
  const sc: number[] = [], y: number[] = []
  for (const s of sites) if (s.hazard === 'FIRE') for (let k = 0; k < nSteps; k++) { const i = s.idx * nSteps + k; sc.push(p[i]); y.push(flags[i] & 2 ? 1 : 0) }
  const P = y.filter((v) => v).length, N = y.length - P
  if (!P || !N) return { fpr: [0, 1], tpr: [0, 1], auc: NaN, op: { fpr: 0, tpr: 0 } }
  const idx = sc.map((_, i) => i).sort((a, b) => sc[b] - sc[a])
  const fpr = [0], tpr = [0]
  let tp = 0, fp = 0, auc = 0
  for (let j = 0; j < idx.length; j++) {
    if (y[idx[j]]) tp++; else { fp++; auc += tp }
    if (j === idx.length - 1 || sc[idx[j + 1]] !== sc[idx[j]]) { fpr.push(fp / N); tpr.push(tp / P) }
  }
  let tpo = 0, fpo = 0
  for (let i = 0; i < sc.length; i++) if (sc[i] >= pStar) (y[i] ? tpo++ : fpo++)
  const step = Math.max(1, Math.floor(fpr.length / 120))
  return { fpr: fpr.filter((_, i) => i % step === 0 || i === fpr.length - 1), tpr: tpr.filter((_, i) => i % step === 0 || i === tpr.length - 1),
    auc: auc / (P * N), op: { fpr: fpo / N, tpr: tpo / P } }
}
