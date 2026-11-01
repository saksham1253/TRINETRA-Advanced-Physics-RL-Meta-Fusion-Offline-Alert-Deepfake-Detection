// Port of TRINETRA/trinetra/src/trinetra/ws5_fusion_rl/decision.py + shield.py. Exactly one decision path:
// level = max(conformal_level(risk, p*), shield_floor). The shield can only RAISE. Always advisory.
export const LEVELS = ['GREEN', 'YELLOW', 'ORANGE', 'RED'] as const
export type Level = (typeof LEVELS)[number]
export const levelIdx = (l: Level) => LEVELS.indexOf(l)
export const raiseTo = (a: Level, b: Level): Level => LEVELS[Math.max(levelIdx(a), levelIdx(b))]

export interface DecisionParams { C_FA: number; C_miss: number; orangeMult: number; redMult: number; uncertain: number }
export const pStar = (P: Pick<DecisionParams, 'C_FA' | 'C_miss'>) => P.C_FA / (P.C_FA + P.C_miss)

export function conformalLevel(risk: number, ps: number, orangeMult = 4.0, redMult = 10.0): Level {
  if (risk < ps) return 'GREEN'
  if (risk < orangeMult * ps) return 'YELLOW'
  if (risk < redMult * ps) return 'ORANGE'
  return 'RED'
}

export interface ShieldSignals {
  FS?: number | null; tilt?: number | null; nodesAgree?: number; rain24?: number | null; highSusc?: boolean
  glofDrop?: boolean; stageJump?: boolean; fireMultiNode?: boolean
}
export interface ShieldParams { tilt: number; rain24: number }
export function shieldFloor(s: ShieldSignals, P: ShieldParams = { tilt: 5.0, rain24: 150.0 }) {
  let floor: Level = 'GREEN'
  const reasons: string[] = []
  if (s.FS != null && s.FS < 1) { floor = raiseTo(floor, 'ORANGE'); reasons.push(`FS < 1 (FS = ${s.FS.toFixed(2)})`) }
  if (s.tilt != null && s.tilt > P.tilt && (s.nodesAgree ?? 0) >= 2) { floor = raiseTo(floor, 'RED'); reasons.push(`tilt rate > ${P.tilt} deg/day, ${s.nodesAgree} nodes agree`) }
  if (s.rain24 != null && s.rain24 > P.rain24 && s.highSusc) { floor = raiseTo(floor, 'ORANGE'); reasons.push(`24 h rain > ${P.rain24} mm on a high-susceptibility slope`) }
  if (s.glofDrop && s.stageJump) { floor = raiseTo(floor, 'RED'); reasons.push('GLOF lake drop with downstream stage jump') }
  if (s.fireMultiNode) { floor = raiseTo(floor, 'ORANGE'); reasons.push('fire corroborated by two or more IoT nodes') }
  return { floor, raised: floor !== 'GREEN', reason: reasons.length ? reasons.join('; ') : null }
}
export type Reliability = 'High' | 'Medium' | 'Low' | 'Unreliable'
export const reliabilityFromU = (u: number, drift = false): Reliability =>
  drift ? 'Unreliable' : u < 0.2 ? 'High' : u < 0.4 ? 'Medium' : u < 0.6 ? 'Low' : 'Unreliable'
export function predSet(point: Level, u: number): Level[] {
  const i = levelIdx(point), half = u < 0.2 ? 0 : u < 0.5 ? 1 : 2
  return LEVELS.slice(Math.max(0, i - half), Math.min(LEVELS.length - 1, i + half) + 1) as unknown as Level[]
}
export function decide(risk: number, uStar: number, anyAvailable: boolean, shield: ShieldSignals, P: DecisionParams, SP?: ShieldParams, drift = false) {
  const ps = pStar(P)
  const point = conformalLevel(risk, ps, P.orangeMult, P.redMult)
  const sh = shieldFloor(shield, SP)
  const level = raiseTo(point, sh.floor)
  return {
    level, point, shield: sh, risk, pStar: ps,
    uncertain: !anyAvailable || uStar > P.uncertain || drift,
    reliability: reliabilityFromU(uStar, drift), predSet: predSet(level, uStar), advisory: true as const,
  }
}
export type DecisionOut = ReturnType<typeof decide>
