// Parameter registry access. The UI and the engine read ONLY src/console/data/params_registry.json (tools/extract_params.py).
import reg from '../data/params_registry.json'

export interface ParamDef {
  id: string; group: string; label: string; unit: string; default: number | string; range: number[]; hard: number[]; step: number
  scale: 'linear' | 'log'; cls: 'A' | 'B' | 'C' | 'SYSTEM' | 'SURROGATE'; module: string; equation: string; lower: string; raise: string
  regime: string | null; live: boolean; kind: 'number' | 'enum' | 'toggle'; options: string[] | null; ref: { file: string; line: number } | null
  citation?: string
}
export const PARAMS = reg.params as unknown as ParamDef[]
export const PARAM_BY_ID = Object.fromEntries(PARAMS.map((p) => [p.id, p])) as Record<string, ParamDef>
export type ParamValues = Record<string, number | string>
export const DEFAULT_VALUES: ParamValues = Object.fromEntries(PARAMS.map((p) => [p.id, p.default]))
export const num = (v: ParamValues, id: string) => Number(v[id] ?? PARAM_BY_ID[id]?.default)

export const PRESETS: Record<string, { label: string; note: string; values: ParamValues }> = {
  default: { label: 'Repo defaults', note: 'Every value as set in the repository', values: {} },
  conservative: { label: 'Conservative', note: 'Fewer misses: lower false-alarm cost, stronger IoT trust', values: { 'cost.C_FA': 2, 'cctv.min_frames': 2, 'dec.uncertain': 0.5 } },
  balanced: { label: 'Balanced', note: 'Higher false-alarm cost, standard validator', values: { 'cost.C_FA': 10, 'cctv.min_frames': 3 } },
  aggressive: { label: 'Restrained', note: 'Fewer false alarms: high false-alarm cost, longer validator', values: { 'cost.C_FA': 30, 'cctv.window': 7, 'cctv.min_frames': 5 } },
  honest: { label: 'Prototype-honest', note: 'Repo defaults with the trust caps of unadmitted experts kept at their defaults', values: {} },
}
