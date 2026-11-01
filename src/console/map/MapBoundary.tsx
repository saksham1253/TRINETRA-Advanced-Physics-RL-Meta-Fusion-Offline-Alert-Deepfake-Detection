import { Component, type ReactNode } from 'react'

/** Keeps the console usable if the map fails (e.g. no WebGL): panels, alerts and the lab keep working. */
export default class MapBoundary extends Component<{ children: ReactNode }, { error: string | null }> {
  state = { error: null as string | null }
  static getDerivedStateFromError(e: unknown) { return { error: String(e) } }
  render() {
    if (!this.state.error) return this.props.children
    return (
      <div className="absolute inset-0 flex items-center justify-center bg-trn-bg p-8">
        <div className="max-w-[520px] rounded border border-trn-line bg-trn-surface p-5 text-[13px] text-trn-text2">
          <div className="mb-2 font-semibold text-trn-text">The 3D map could not start</div>
          <p>All panels, alerts, the parameter lab and the LoRa planner still work. Check that the browser supports WebGL 2, or open Layers and turn terrain off.</p>
          <p className="mt-2 font-trn-mono text-[11px] text-trn-text3">{this.state.error}</p>
          <button className="mt-3 rounded border border-trn-line px-3 py-1.5 text-trn-text hover:border-trn-text3" onClick={() => this.setState({ error: null })}>Try again</button>
        </div>
      </div>
    )
  }
}
