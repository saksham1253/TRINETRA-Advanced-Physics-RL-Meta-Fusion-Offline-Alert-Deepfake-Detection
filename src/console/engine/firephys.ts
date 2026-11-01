// Port of TRINETRA/trinetra/src/trinetra/ws1a_firephys (established_ef.py, novel_nd.py, gate.py). Class A unless noted.
import { clip, pyRound } from './math'

export const STEFAN_BOLTZMANN = 5.670374419e-8

/** L = 0.235 Q^(2/5) - 1.02 D  [m]  (Heskestad). established_ef.py */
export const flameHeightHeskestad = (Q_kW: number, D_m: number) => 0.235 * Q_kW ** 0.4 - 1.02 * D_m
/** f = 1.5 D^(-1/2)  [Hz]. established_ef.py */
export const strouhalPuffingFrequency = (D_m: number) => 1.5 / Math.sqrt(D_m)
/** Heskestad far-field centerline excess temperature [K]. established_ef.py */
export function plumeCenterlineDT(Qc_kW: number, z_m: number, z0_m = 0, T_inf = 293) {
  const g = 9.81, cp = 1.0, rho = 1.2
  const dz = Math.max(z_m - z0_m, 1e-6)
  return 9.1 * (T_inf / (g * cp ** 2 * rho ** 2)) ** (1 / 3) * Qc_kW ** (2 / 3) * dz ** (-5 / 3)
}
/** Byram convection number N_c = 2 g Q_c / (rho cp T U^3). established_ef.py */
export function byramConvectionNumber(Qc_kW_m: number, U: number, rho = 1.2, cp = 1.0, T_inf = 293, g = 9.81) {
  const denom = rho * cp * T_inf * U ** 3
  return denom <= 0 ? Infinity : (2 * g * Qc_kW_m) / denom
}
export const beerLambertTransmittance = (ks: number, L: number) => Math.exp(-ks * L)

/** Frequency at which a true flicker appears when sampled at fs. novel_nd.py (Python round = half-to-even). */
export function aliasedFrequency(f: number, fs: number) {
  if (fs <= 0) throw new Error('fs must be > 0')
  return Math.abs(f - fs * pyRound(f / fs))
}
/** ND-1 de-aliased flicker consistency (Class C, default off). */
export function nd1Consistency(f_obs: number, fs: number, D: number, sigma = 0.3) {
  const fa = aliasedFrequency(strouhalPuffingFrequency(D), fs)
  return Math.exp(-((f_obs - fa) ** 2) / (2 * sigma ** 2))
}

export interface FireGateParams {
  ncFull: number // 2.0 in gate.py
  cMin: number // 0.3
  uBase: number // 0.15
  iotBonus: number // 0.1
}
export const FIRE_GATE_DEFAULTS: FireGateParams = { ncFull: 2.0, cMin: 0.3, uBase: 0.15, iotBonus: 0.1 }

/** fire_gate (gate.py): physics consistency c and uncertainty u for the detector confidence. Class-C ND paths are off. */
export function fireGate(
  detectorConf: number,
  opts: { Qc?: number | null; U?: number | null; multiNode?: boolean } = {},
  P: FireGateParams = FIRE_GATE_DEFAULTS,
) {
  let c = 1.0
  let Nc: number | null = null
  if (opts.Qc != null && opts.U != null) {
    Nc = byramConvectionNumber(opts.Qc, Math.max(opts.U, 1e-3))
    c *= clip(Nc / P.ncFull, P.cMin, 1.0)
  }
  const p = clip(detectorConf, 0, 1)
  if (opts.multiNode) c = clip(c + P.iotBonus, 0, 1)
  const u = clip(P.uBase + 0.4 * (1 - c), 0, 1)
  return { p, c: clip(c, 0, 1), u, Nc }
}
