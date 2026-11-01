export type Dataset = {
  ID: string
  name: string
  modules: string
  task: string
  link: string
  mirror_or_kaggle: string
  size_full: string
  size_subset: string
  samples: string
  labels: string
  license: string
  access: string
  age_domain_gap: string
  known_problems: string
  role: string
  format_adapter: string
  status: string
  fetched_by: string
}

export type Gap = { id: string; gap: string; evidence: string; triage: string; status: string }

export type Bug = { id: string; bug: string; fix: string; status: string }

export type Stat = { mean: number; sd: number }

export type ModelResult = { n_seeds: number; admitted?: string; deploy_learned?: string } & Record<string, unknown>

export type GeoReport = {
  name: string
  n?: number
  n_pos?: number
  n_blocks?: number
  scores?: Record<string, { roc_auc?: number; pr_auc?: number; recall_at_fpr05?: number }>
  physics_minus_rain_auc?: { mean: number; ci95: [number, number] }
  area_volume?: { n: number; exponent?: number; exponent_ci95?: [number, number]; r2_log?: number }
  volume_peakQ?: { n: number; exponent?: number; exponent_ci95?: [number, number]; r2_log?: number }
  C_miss?: number
  n_seasons?: number
  best_rule?: string
  deploy_learned?: boolean
  gain_vs_rule_lcb95?: number
  policies?: Record<string, { return_mean: number; miss_rate: number | null; alarm_days_per_season: number }>
}

export type Results = {
  geo?: Record<string, GeoReport>
  pack: string
  dry_run_present: boolean
  models: Record<string, ModelResult>
  fusion: null | {
    synthetic_pairing: boolean
    sources: string[]
    fake_frac: number
    seeds: number[]
    rules: Record<string, Record<string, Stat>>
  }
}

export type DashboardData = {
  state: {
    updated: string
    repo: string
    branch: string
    commit: string
    tasks: Record<string, string>
    counters: Record<string, number>
    next_action: string
  }
  datasets: Dataset[]
  gaps: Gap[]
  bugs: Bug[]
  results: Results | null
  papers: Record<string, number>
  next: string[]
}
