// Numeric helpers shared by the physics / fusion ports. Semantics follow the Python originals exactly.

export const clip = (x: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, x))
export const sigmoid = (x: number) => 1 / (1 + Math.exp(-x))
export const logit = (p: number) => {
  const q = clip(p, 1e-6, 1 - 1e-6)
  return Math.log(q / (1 - q))
}

/** Python 3 round(): round half to even. */
export function pyRound(x: number): number {
  const f = Math.floor(x)
  const d = x - f
  if (d > 0.5) return f + 1
  if (d < 0.5) return f
  return f % 2 === 0 ? f : f + 1
}

/** Complementary error function (series below 3, Lentz continued fraction above). Relative error < 1e-12. */
export function erfc(x: number): number {
  if (x < 0) return 2 - erfc(-x)
  if (x < 3) {
    let sum = 0
    let term = x
    for (let n = 0; n < 200; n++) {
      const t = term / (2 * n + 1)
      sum += t
      if (Math.abs(t) < 1e-17 * Math.abs(sum)) break
      term *= (-x * x) / (n + 1)
    }
    return 1 - (2 / Math.sqrt(Math.PI)) * sum
  }
  // erfc(x) = exp(-x^2)/sqrt(pi) * 1 / (x + (1/2)/(x + 1/(x + (3/2)/(x + ...))))
  const tiny = 1e-300
  let f = x
  let C = x
  let D = 0
  for (let n = 1; n < 500; n++) {
    const a = n / 2
    D = x + a * D
    D = Math.abs(D) < tiny ? tiny : D
    C = x + a / C
    C = Math.abs(C) < tiny ? tiny : C
    D = 1 / D
    const delta = C * D
    f *= delta
    if (Math.abs(delta - 1) < 1e-16) break
  }
  return Math.exp(-x * x) / Math.sqrt(Math.PI) / f
}

export const mean = (a: number[]) => (a.length ? a.reduce((s, v) => s + v, 0) / a.length : 0)
/** numpy.std (population). */
export const pstd = (a: number[]) => {
  const m = mean(a)
  return Math.sqrt(mean(a.map((v) => (v - m) ** 2)))
}
export const median = (a: number[]) => {
  if (!a.length) return 0
  const s = [...a].sort((x, y) => x - y)
  const k = s.length >> 1
  return s.length % 2 ? s[k] : (s[k - 1] + s[k]) / 2
}

/** Deterministic PRNG (mulberry32) so a scenario seed always gives identical alerts. */
export function rng(seed: number) {
  let a = seed >>> 0
  const next = () => {
    a = (a + 0x6d2b79f5) >>> 0
    let t = a
    t = Math.imul(t ^ (t >>> 15), t | 1)
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
  return {
    next,
    uniform: (lo: number, hi: number) => lo + (hi - lo) * next(),
    int: (n: number) => Math.floor(next() * n),
    normal: () => {
      const u = Math.max(next(), 1e-12)
      return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * next())
    },
  }
}
export type Rng = ReturnType<typeof rng>
