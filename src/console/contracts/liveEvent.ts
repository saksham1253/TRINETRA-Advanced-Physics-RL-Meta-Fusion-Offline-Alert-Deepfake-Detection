// TypeScript mirror of live_event.schema.json plus a dependency-free validator (used by the client and the contract test).
import schema from './live_event.schema.json'

export interface LiveModule { id: string; status: 'IMPLEMENTED' | 'PLANNED'; score: number | null; uncertainty: number | null; validity_flag?: boolean | null; origin: string; parameters_used?: Record<string, unknown> }
export interface LiveEvent {
  schema_version: '1.0'; mode: 'LIVE' | 'REPLAY' | 'SIM'
  model: { name: string; version: string; run_id: string; checkpoint_hash?: string | null; trained_on?: string }
  source_id: string; location: { lat: number; lon: number; elevation?: number | null; accuracy_m?: number | null; location_origin: 'SURVEYED' | 'ESTIMATED' | 'SYNTHETIC' }
  timestamp_utc: string; modules: LiveModule[]; physics?: unknown[]
  fusion: { technique: string; inputs?: unknown[]; weights?: unknown[]; calibrated_probability: number; uncertainty: number; abstained: boolean; reason?: string | null; cost_ratio?: number; threshold?: number }
  decision: { tier: 'GREEN' | 'YELLOW' | 'ORANGE' | 'RED'; requires_approval: true; explanation_template_id?: string; explanation_values?: Record<string, unknown> }
  network: { internet?: boolean; cellular?: boolean; lora?: boolean }; ground_truth?: Record<string, unknown> | null; notes?: string | null
}
export const SCHEMA = schema

export function validateLiveEvent(e: unknown): string[] {
  const err: string[] = []
  const o = e as Record<string, unknown>
  if (!o || typeof o !== 'object') return ['not an object']
  for (const k of schema.required) if (!(k in o)) err.push(`missing ${k}`)
  if (o.schema_version !== '1.0') err.push('schema_version must be 1.0')
  if (!['LIVE', 'REPLAY', 'SIM'].includes(String(o.mode))) err.push('bad mode')
  const loc = o.location as Record<string, unknown> | undefined
  if (loc && (typeof loc.lat !== 'number' || Math.abs(loc.lat) > 90 || typeof loc.lon !== 'number' || Math.abs(loc.lon) > 180)) err.push('bad location')
  if (loc && !['SURVEYED', 'ESTIMATED', 'SYNTHETIC'].includes(String(loc.location_origin))) err.push('bad location_origin')
  const mods = o.modules as LiveModule[] | undefined
  if (!Array.isArray(mods)) err.push('modules must be an array')
  else for (const m of mods) {
    if (!['IMPLEMENTED', 'PLANNED'].includes(m.status)) err.push(`module ${m.id}: bad status`)
    if (m.score != null && (m.score < 0 || m.score > 1)) err.push(`module ${m.id}: score out of [0,1]`)
  }
  const f = o.fusion as Record<string, unknown> | undefined
  if (f && (typeof f.calibrated_probability !== 'number' || (f.calibrated_probability as number) < 0 || (f.calibrated_probability as number) > 1)) err.push('bad fusion probability')
  const d = o.decision as Record<string, unknown> | undefined
  if (d && !['GREEN', 'YELLOW', 'ORANGE', 'RED'].includes(String(d.tier))) err.push('bad tier')
  if (d && d.requires_approval !== true) err.push('requires_approval must be true (Rule 19)')
  return err
}
