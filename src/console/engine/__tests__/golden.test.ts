// Golden tests: TS ports vs values exported from the TRINETRA Python code (tools/export_golden.py). Any mismatch is a blocker.
import { describe, expect, it } from 'vitest'
import G from './golden.json'
import * as F from '../firephys'
import * as Geo from '../geophys'
import * as Fu from '../fusion'
import * as D from '../decision'
import * as L from '../lora'

const close = (a: number, b: number, rel = 1e-9) => expect(Math.abs(a - b)).toBeLessThanOrEqual(rel * Math.max(1, Math.abs(b)))

describe('fire physics (ws1a)', () => {
  it('heskestad, strouhal, plume, byram, beer-lambert, aliasing, ND-1', () => {
    for (const [q, d, v] of G.heskestad) close(F.flameHeightHeskestad(q, d), v)
    for (const [d, v] of G.strouhal) close(F.strouhalPuffingFrequency(d), v)
    for (const [q, z, v] of G.plume_dT) close(F.plumeCenterlineDT(q, z), v)
    for (const [q, u, v] of G.byram) close(F.byramConvectionNumber(q, u), v)
    for (const [k, l, v] of G.beer) close(F.beerLambertTransmittance(k, l), v)
    for (const [f, fs, v] of G.aliased) close(F.aliasedFrequency(f, fs), v)
    for (const [fo, fs, d, v] of G.nd1) close(F.nd1Consistency(fo, fs, d), v)
  })
  it('fire_gate', () => {
    for (const [conf, q, u, mn, p, c, uu] of G.fire_gate as [number, number | null, number | null, boolean, number, number, number][]) {
      const r = F.fireGate(conf, { Qc: q, U: u, multiNode: mn })
      close(r.p, p); close(r.c, c); close(r.u, uu)
    }
  })
})

describe('geo physics (ws1b)', () => {
  it('FS, ierfc, Iverson head, Caine', () => {
    for (const [c, phi, g, z, b, uw, ss, v] of G.fs) close(Geo.factorOfSafety(c, phi, g, z, b, uw, ss), v)
    for (const [x, v] of G.ierfc) close(Geo.ierfc(x), v, 1e-11)
    for (const [Z, t, D0, K, I, b, v] of G.pressure_head) close(Geo.pressureHead(Z, t, D0, K, I, b), v, 1e-10)
    for (const [I, Dh, v] of G.caine) close(Geo.caineRatio(I, Dh, 14, 0.39), v)
    for (const [Z, t, steps, D0, K, b, v] of G.multipulse as [number, number, [number, number][], number, number, number, number][])
      close(Geo.transientHeadMultipulse(Z, t, steps, D0, K, b), v, 1e-10)
  })
  it('geo_gate', () => {
    for (const [kw, FS, caine, p, u, c] of G.geo_gate as [Geo.GeoGateInput, number, number, number, number, number][]) {
      const r = Geo.geoGate(kw)
      close(r.FS, FS, 1e-10); close(r.caine!, caine); close(r.p_phys, p, 1e-10); close(r.u, u, 1e-10); close(r.c, c, 1e-10)
    }
  })
})

const experts: Fu.Expert[] = G.fusion.experts.map((e: Record<string, unknown>, i: number) => ({
  id: String(i), label: String(e.source), source: String(e.source), p: e.p as number, u: e.u as number, c: e.c as number, r: e.r as number,
  cls: 'data', available: e.available !== false, origin: 'SIMULATED', status: 'IMPLEMENTED',
}))

describe('fusion (ws5)', () => {
  it('effective weight, FM-1, NF-1/3/4, PHARAOH, GMF', () => {
    let k = 0
    for (const e of experts) for (const t of [0.2, 0.5, 1.0]) close(Fu.effectiveWeight(e, t), G.fusion.eff_w[k++])
    ;[0.2, 0.5, 1.0].forEach((t, i) => close(Fu.fm1(experts, t), G.fusion.fm1[i]))
    const av = experts.filter((e) => e.available), ws = av.map((e) => Fu.effectiveWeight(e, 0.5))
    ;[0, 0.3, 1].forEach((lam, i) => close(Fu.nf3(av.map((e) => e.p), av.map((e) => e.u), ws, lam), G.fusion.nf3[i]))
    close(Fu.nf4Salience(experts), G.fusion.nf4)
    close(Fu.weightedDispersion(av.map((e) => e.p), ws), G.fusion.disp)
    ;[[0.9, 0.4, 0.25], [0.3, 0.4, 0.25], [0.7, 0.2, 0.1]].forEach(([p, phi, s], i) => close(Fu.nf1Consistency(p, phi, s), G.fusion.nf1[i]))
    ;[0, 2, 6].forEach((kp, i) => { close(Fu.pharaohFuse(experts, kp).p, G.fusion.pharaoh[i]); close(Fu.pharaohFuse(experts, kp).rho, G.fusion.pharaoh_rho[i]) })
    close(Fu.gmfFuse(experts, 0.5).p, G.fusion.gmf)
    close(Fu.gmfFuse(experts, 0.5, true).p, G.fusion.gmf_pharaoh)
  })
})

describe('decision + shield (ws5)', () => {
  it('conformal level and shield floor', () => {
    for (const [r, lv] of G.conformal as [number, D.Level][]) expect(D.conformalLevel(r, 5 / 105)).toBe(lv)
    const map = (k: Record<string, unknown>): D.ShieldSignals => ({ FS: k.FS as number, tilt: k.tilt_rate_deg_per_day as number, nodesAgree: k.nodes_agree as number,
      rain24: k.rain_24h_mm as number, highSusc: k.high_susceptibility as boolean, glofDrop: k.glof_lake_drop as boolean,
      stageJump: k.downstream_stage_jump as boolean, fireMultiNode: k.fire_multi_node as boolean })
    for (const [kw, lv] of G.shield as [Record<string, unknown>, D.Level][]) expect(D.shieldFloor(map(kw)).floor).toBe(lv)
    for (const [kw, tau, ph, lv, risk, unc, rel, set, u] of G.decide as [Record<string, unknown>, number, boolean, D.Level, number, boolean, string, string[], number][]) {
      const f = Fu.fuse(experts, ph ? 'PHARAOH' : 'FM-1', { tau, lambda: 0.3, kappa: 2 })
      close(f.p, risk); close(f.uStar, u)
      const d = D.decide(f.p, f.uStar, true, map(kw), { C_FA: 5, C_miss: 100, orangeMult: 4, redMult: 10, uncertain: 0.6 })
      expect(d.level).toBe(lv); expect(d.uncertain).toBe(unc); expect(d.reliability).toBe(rel); expect(d.predSet).toEqual(set)
    }
  })
})

describe('LoRa last mile (ws3)', () => {
  it('airtime, FSPL, range, siren', () => {
    for (const [n, sf, v] of G.airtime) close(L.loraAirtimeS(n, sf), v)
    for (const [d, v] of G.fspl) close(L.fsplDb(d), v)
    for (const [sf, t, v] of G.range as [number, L.Terrain, number][]) close(L.loraRangeKm({ ...L.RADIO_DEFAULTS, sf }, t), v)
    for (const [a, c, v] of G.siren) close(L.sirenRadiusM(120, 30, a, c), v, 1e-9)
  })
  it('plan(demo_valley): default, R1 failure, SF7', () => {
    const V = G.last_mile.villages as L.Village[], N = G.last_mile.nodes as L.MeshNode[]
    const chk = (res: L.VillageResult[], exp: unknown[][]) => exp.forEach((row, i) => {
      expect(res[i].id).toBe(row[0])
      if (row[1] === null) expect(res[i].minutes).toBeNull(); else close(res[i].minutes!, row[1] as number, 1e-9)
      expect(res[i].channel).toBe(row[2])
    })
    chk(L.plan(V, N, L.COND_OUTAGE).results, G.last_mile.plan)
    chk(L.plan(V, N, L.COND_OUTAGE, L.RADIO_DEFAULTS, L.PLAN_DEFAULTS, new Set(['R1-ridge'])).results, G.last_mile.plan_no_R1)
    chk(L.plan(V, N, L.COND_OUTAGE, { ...L.RADIO_DEFAULTS, sf: 7 }).results, G.last_mile.plan_sf7)
  })
})
