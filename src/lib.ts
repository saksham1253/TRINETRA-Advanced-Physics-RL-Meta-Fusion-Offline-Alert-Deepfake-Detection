/** Strip the light markdown used in the handoff docs (bold, code ticks) for plain display. */
export const plain = (s: string) => s.replace(/\*\*/g, '').replace(/`/g, '')

export const MODULES: Record<string, string> = {
  M1: 'Fire & smoke',
  M2: 'Thermal / aerial',
  M3: 'Zero-shot & confusers',
  M4: 'Video anomaly',
  M5: 'IoT & time series',
  M6: 'Deepfake',
  M7: 'Crisis text',
  M8: 'Satellite & weather',
  M9: 'RL environments',
  M10: 'Cyclone',
  M11: 'India portals',
  M12: 'Physics validation',
}

export const primaryModule = (modules: string) => modules.match(/M\d+/)?.[0] ?? 'M0'

export type Tone = 'ok' | 'warn' | 'signal' | 'muted'

export function statusTone(status: string): Tone {
  const s = status.toUpperCase()
  if (s.includes('SLOW') || s.includes('UNVERIFIED')) return 'warn'
  if (s.includes('SUBSET')) return 'signal'
  if (s.startsWith('VERIFIED') || s.startsWith('REACHABLE')) return 'ok'
  return 'muted'
}

export function statusLabel(status: string): string {
  const s = status.toUpperCase()
  if (s.includes('SLOW')) return 'Slow access'
  if (s.includes('UNVERIFIED')) return 'Partly verified'
  if (s.includes('SUBSET')) return 'Verified · subset only'
  if (s.startsWith('VERIFIED')) return 'Verified'
  return status
}
