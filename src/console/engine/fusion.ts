// Port of TRINETRA/trinetra/src/trinetra/ws5_fusion_rl (nf.py, fusion_models.py, pharaoh.py, gmf.py) + the REAL-pairing
// stack from TRINETRA/trinetra/kaggle/fire_meta_fusion.py (logistic on [logit p_i, sd, range] of raw probabilities).
import { clip, logit, mean, median, pstd, sigmoid } from './math'

export type Cls = 'A' | 'B' | 'C' | 'data'
export interface Expert {
  id: string
  label: string
  source: string
  p: number
  u: number
  c: number
  r: number
  cls: Cls
  available: boolean
  /** raw (uncalibrated) probability, used only by STACK */
  raw?: number
  origin: 'SIMULATED' | 'REPLAYED' | 'LIVE' | 'REAL-OOF'
  status: 'IMPLEMENTED' | 'PLANNED'
  note?: string
}

export const effectiveWeight = (e: Expert, tau = 0.5) => (e.available ? e.r * e.c * Math.exp(-e.u / Math.max(tau, 1e-6)) : 0)
export function weightedDispersion(ps: number[], w: number[]) {
  const s = w.reduce((a, b) => a + b, 0)
  if (s <= 0) return 0
  const wn = w.map((x) => x / s)
  const pbar = wn.reduce((a, x, i) => a + x * ps[i], 0)
  return Math.sqrt(Math.max(wn.reduce((a, x, i) => a + x * (ps[i] - pbar) ** 2, 0), 0))
}
export function nf1Consistency(p: number, phi: number, sigma = 0.25, eps = 1e-6) {
  const over = Math.max(p - phi, 0)
  return Math.exp(-(over ** 2) / (2 * (sigma ** 2 + eps)))
}
export function nf3(ps: number[], u: number[], w: number[], lam = 0.3) {
  const s = w.reduce((a, b) => a + b, 0) || 1
  const base = w.reduce((a, x, i) => a + (x / s) * u[i], 0)
  return clip(base + lam * weightedDispersion(ps, w), 0, 1)
}
export const nf4Salience = (ex: Expert[]) => {
  const v = ex.filter((e) => e.available).map((e) => e.r * e.c * e.p)
  return v.length ? Math.max(...v) : 0
}
export function fm1(ex: Expert[], tau = 0.5) {
  const a = ex.filter((e) => e.available)
  if (!a.length) return 0
  const w = a.map((e) => effectiveWeight(e, tau))
  const s = w.reduce((x, y) => x + y, 0)
  if (s <= 0) return mean(a.map((e) => e.p))
  return w.reduce((acc, x, i) => acc + (x / s) * a[i].p, 0)
}
export const pharaohOrder = (ps: number[], w: number[], S: number, kappa = 2.0) => clip(1 + kappa * weightedDispersion(ps, w) * S, 1, 8)
export function pharaohMean(ps: number[], w: number[], rho: number) {
  const s = w.reduce((a, b) => a + b, 0)
  if (s <= 0) return 0
  const r = Math.max(rho, 1e-9)
  return clip(w.reduce((a, x, i) => a + (x / s) * clip(ps[i], 0, 1) ** r, 0) ** (1 / r), 0, 1)
}
/** pharaoh_fuse: NOTE the repo computes PHARAOH weights with the DEFAULT tau = 0.5 (effective_weight(e)), not fusion.tau. */
export function pharaohFuse(ex: Expert[], kappa = 2.0) {
  const a = ex.filter((e) => e.available)
  if (!a.length) return { p: 0, rho: 1, S: 0 }
  const ps = a.map((e) => e.p), w = a.map((e) => effectiveWeight(e))
  const S = nf4Salience(a)
  const rho = pharaohOrder(ps, w, S, kappa)
  return { p: pharaohMean(ps, w, rho), rho, S }
}
export function gmfFuse(ex: Expert[], tau = 0.5, usePharaohBase = false) {
  const a = ex.filter((e) => e.available)
  if (!a.length) return { p: 0, base: 0, residual: 0, gate: [] as number[] }
  const w = a.map((e) => effectiveWeight(e, tau))
  const s = w.reduce((x, y) => x + y, 0)
  const gate = s > 0 ? w.map((x) => x / s) : w.map(() => 1 / a.length)
  const ps = a.map((e) => e.p)
  const base = usePharaohBase ? pharaohMean(ps, gate, pharaohOrder(ps, gate, nf4Salience(a))) : gate.reduce((acc, g, i) => acc + g * ps[i], 0)
  return { p: clip(base, 0, 1), base, residual: 0, gate } // no trained residual head in the browser: residual = 0 (gmf.py default)
}

export interface StackModel { w: number[]; b: number; mu: number[]; sd: number[]; T: number }
/** STACK (fire_meta_fusion.py): needs raw fire_cnn, zeroshot, clip_probe probabilities of the SAME image. */
export function stackProb(raw: [number, number, number], m: StackModel) {
  const L = raw.map((p) => logit(p))
  const f = [...L, pstd(raw), Math.max(...raw) - Math.min(...raw)]
  const z = f.reduce((acc, x, i) => acc + ((x - m.mu[i]) / m.sd[i]) * m.w[i], m.b)
  return sigmoid(logit(sigmoid(z)) / m.T)
}

export type Technique = 'FM-1' | 'PHARAOH' | 'GMF' | 'STACK' | 'MEAN' | 'MEDIAN' | 'MAX'
export interface FusionOut {
  p: number; uStar: number; salience: number; technique: Technique; usedClassC: boolean; rho?: number
  weights: { id: string; w: number }[]; note?: string
}
export interface FusionParams { tau: number; lambda: number; kappa: number }

/** Dispatcher mirroring fusion_models.fuse(), extended with the comparison rules the evidence panel offers. */
export function fuse(ex: Expert[], tech: Technique, P: FusionParams, stack?: StackModel): FusionOut {
  const a = ex.filter((e) => e.available)
  const ps = a.map((e) => e.p)
  const ws = a.map((e) => effectiveWeight(e, P.tau))
  const uStar = a.length ? nf3(ps, a.map((e) => e.u), ws, P.lambda) : 1
  const salience = nf4Salience(a)
  const weights = a.map((e, i) => ({ id: e.id, w: ws[i] }))
  let p = 0, rho: number | undefined, usedC = a.some((e) => e.cls === 'C'), note: string | undefined
  let technique = tech
  if (tech === 'PHARAOH' && a.length >= 2) {
    const r = pharaohFuse(a, P.kappa); p = r.p; rho = r.rho; usedC = true
  } else if (tech === 'GMF') {
    p = gmfFuse(a, P.tau).p
  } else if (tech === 'STACK') {
    const by = (s: string) => a.find((e) => e.source === s)?.raw
    const r = [by('fire_cnn'), by('zeroshot'), by('clip_probe')]
    if (stack && r.every((x) => x != null)) p = stackProb(r as [number, number, number], stack)
    else { p = fm1(a, P.tau); technique = 'FM-1'; note = 'STACK needs fire_cnn, zeroshot and clip_probe on the same image; fell back to FM-1' }
  } else if (tech === 'MEAN') p = mean(ps)
  else if (tech === 'MEDIAN') p = median(ps)
  else if (tech === 'MAX') p = ps.length ? Math.max(...ps) : 0
  else { p = fm1(a, P.tau); technique = tech === 'PHARAOH' ? 'FM-1' : technique }
  return { p: clip(p, 0, 1), uStar, salience, technique, usedClassC: usedC, rho, weights, note }
}
