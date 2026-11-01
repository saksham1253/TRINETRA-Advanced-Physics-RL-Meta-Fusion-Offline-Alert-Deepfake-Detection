import { useEffect } from 'react'
import { create } from 'zustand'
import { useStore } from '../store'
import { num } from '../engine/params'
import { RADIO_DEFAULTS, PLAN_DEFAULTS, COND_OUTAGE, type Radio, type PlanParams } from '../engine/lora'
import { computeMesh, type MeshState } from './model'

export const useMesh = create<{ mesh: MeshState | null; ms: number; busy: boolean; outageAt: number | null }>(() => ({ mesh: null, ms: 0, busy: false, outageAt: null }))

export function radioFrom(P: ReturnType<typeof useStore.getState>['params']): Radio {
  return { ...RADIO_DEFAULTS, sf: Math.round(num(P, 'lora.sf')), tx: num(P, 'lora.tx_dbm'), fade: num(P, 'lora.fade'),
    n: { ...RADIO_DEFAULTS.n, hill_forest: num(P, 'lora.n_forest') } }
}
export function planFrom(P: ReturnType<typeof useStore.getState>['params']): PlanParams {
  return { ...PLAN_DEFAULTS, payload: Math.round(num(P, 'lora.payload')), deadlineMin: num(P, 'lora.deadline'), maxHopKm: num(P, 'lora.max_hop'),
    runnerKmh: num(P, 'lora.runner'), sirenContour: num(P, 'lora.siren_contour') }
}

export function useMeshCompute(enabled: boolean) {
  const params = useStore((s) => s.params)
  const disabled = useStore((s) => s.disabledNodes)
  const loss = useStore((s) => s.packetLoss)
  const retx = useStore((s) => s.retransmissions)
  useEffect(() => {
    if (!enabled) return
    let cancel = false
    const t0 = performance.now()
    useMesh.setState({ busy: true })
    const id = window.setTimeout(async () => {
      const m = await computeMesh(radioFrom(params), planFrom(params), COND_OUTAGE, new Set(disabled), loss, retx, num(params, 'lora.duty'))
      if (!cancel) useMesh.setState({ mesh: m, ms: performance.now() - t0, busy: false })
    }, 30)
    return () => { cancel = true; clearTimeout(id) }
  }, [enabled, params, disabled, loss, retx])
}
