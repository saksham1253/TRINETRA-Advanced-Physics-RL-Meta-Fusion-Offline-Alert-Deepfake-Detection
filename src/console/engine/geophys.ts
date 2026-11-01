// Port of TRINETRA/trinetra/src/trinetra/ws1b_geophys (fs.py, iverson.py, caine.py, gate.py). Class A.
import { clip, erfc, pstd, sigmoid } from './math'

const GAMMA_W = 9.81
const rad = (d: number) => (d * Math.PI) / 180

/** Infinite-slope factor of safety. fs.py */
export function factorOfSafety(c: number, phiDeg: number, gamma: number, z: number, betaDeg: number, u_w = 0, sigma_s = 0) {
  const b = rad(betaDeg), phi = rad(phiDeg)
  const denom = gamma * z * Math.sin(b) * Math.cos(b)
  if (denom <= 0) throw new Error('driving stress must be positive')
  return (c + (gamma * z * Math.cos(b) ** 2 - u_w + sigma_s) * Math.tan(phi)) / denom
}
export const ierfc = (x: number) => Math.exp(-x * x) / Math.sqrt(Math.PI) - x * erfc(x)
export const diffusivityD1 = (D0: number, betaDeg: number) => D0 / Math.cos(rad(betaDeg)) ** 2
/** Iverson (2000) total pressure head; slope enters ONLY via D1 = D0/cos^2(beta). iverson.py */
export function pressureHead(Z: number, t: number, D0: number, Kz: number, Iz: number, betaDeg: number, psiSteady = 0) {
  if (t <= 0) return psiSteady
  const arg = Math.sqrt(4 * diffusivityD1(D0, betaDeg) * t)
  return psiSteady + (Iz / Kz) * arg * ierfc(Z / arg)
}
/** Caine I = a D^-b; returns I / I_threshold. caine.py */
export const caineRatio = (I: number, D: number, a: number, b: number) => (D > 0 ? I / (a * D ** -b) : NaN)

export interface GeoGateInput {
  c_prime: number; phi_prime_deg: number; gamma: number; z: number; beta_deg: number
  sigma_s?: number; u_w?: number
  D0?: number; K_z?: number; I_z?: number; t_hours?: number; psi_steady?: number
  I_mm_h?: number; D_hours?: number; caine_a?: number; caine_b?: number
  t_failure?: number; fukuzono_r2?: number; now_hours?: number
}
export interface GeoGateParams { k_fs: number; leadH: number }

/** geo_gate (gate.py): FS + Caine + Fukuzono proximity, noisy-OR, consistency = 1 - std(active). */
export function geoGate(gi: GeoGateInput, P: GeoGateParams = { k_fs: 4.0, leadH: 48 }) {
  let u_w = gi.u_w ?? 0
  if (gi.D0 != null && gi.K_z && gi.I_z != null && gi.t_hours != null) {
    u_w = GAMMA_W * pressureHead(gi.z, gi.t_hours, gi.D0, gi.K_z, gi.I_z, gi.beta_deg, gi.psi_steady ?? 0)
  }
  const FS = factorOfSafety(gi.c_prime, gi.phi_prime_deg, gi.gamma, gi.z, gi.beta_deg, u_w, gi.sigma_s ?? 0)
  const p_fs = sigmoid(P.k_fs * (1 - FS))
  let caine: number | null = null, p_caine = 0
  if (gi.I_mm_h != null && gi.D_hours != null) {
    caine = caineRatio(gi.I_mm_h, gi.D_hours, gi.caine_a ?? 14.0, gi.caine_b ?? 0.39)
    p_caine = clip(caine - 0.5, 0, 1)
  }
  let p_fk = 0
  if (gi.t_failure != null && gi.now_hours != null && Number.isFinite(gi.t_failure)) {
    const lead = gi.t_failure - gi.now_hours
    if (lead > 0) p_fk = clip(1 - lead / P.leadH, 0, 1) * clip(gi.fukuzono_r2 ?? 0, 0, 1)
  }
  const comps = [p_fs, p_caine, p_fk]
  const p_phys = 1 - comps.reduce((s, c) => s * (1 - c), 1)
  const active = comps.filter((c) => c > 0)
  const cons = clip(active.length >= 2 ? 1 - pstd(active) : 1, 0, 1)
  return { FS, u_w, caine, p_phys: clip(p_phys, 0, 1), c: cons, u: clip(0.5 * (1 - cons) + 0.1, 0, 1), parts: { p_fs, p_caine, p_fk } }
}

/** Unit ierfc response R(Z, tau) with slope-adjusted D1 (iverson._response_R). */
const responseR = (Z: number, tau: number, D1: number) => {
  if (tau <= 0) return 0
  const arg = Math.sqrt(4 * D1 * tau)
  return arg * ierfc(Z / arg)
}
/** Piecewise-constant rainfall by linear superposition (iverson.transient_head_multipulse). Steps: [t_k, I_k] absolute flux. */
export function transientHeadMultipulse(Z: number, t: number, steps: [number, number][], D0: number, Kz: number, betaDeg: number) {
  const D1 = diffusivityD1(D0, betaDeg)
  const s = [...steps].sort((a, b) => a[0] - b[0])
  let psi = 0, prev = 0
  for (const [tk, ik] of s) { psi += ((ik - prev) / Kz) * responseR(Z, t - tk, D1); prev = ik }
  return psi
}
