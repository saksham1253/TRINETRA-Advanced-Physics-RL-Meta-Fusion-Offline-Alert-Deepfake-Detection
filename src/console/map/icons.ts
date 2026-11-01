// Map icons drawn on canvas from the design tokens (no external sprite, works offline). Severity is encoded by SHAPE and colour;
// hollow variants mark alerts the simulator knows are false alarms.
import type * as maplibregl from 'maplibre-gl'

const SEV: Record<string, { dark: string; light: string }> = {
  watch: { dark: '#FFC145', light: '#A16207' }, warning: { dark: '#FF7A1A', light: '#C2410C' }, emergency: { dark: '#FF3B30', light: '#B91C1C' },
}
type Shape = 'circle' | 'diamond' | 'octagon' | 'square' | 'triangle' | 'tower' | 'camera' | 'arrow'
function path(g: CanvasRenderingContext2D, shape: Shape, c: number, r: number) {
  g.beginPath()
  if (shape === 'circle') g.arc(c, c, r, 0, Math.PI * 2)
  else if (shape === 'diamond') { g.moveTo(c, c - r * 1.15); g.lineTo(c + r * 1.15, c); g.lineTo(c, c + r * 1.15); g.lineTo(c - r * 1.15, c) }
  else if (shape === 'octagon') for (let k = 0; k < 8; k++) { const a = Math.PI / 8 + (k * Math.PI) / 4; g[k ? 'lineTo' : 'moveTo'](c + r * Math.cos(a), c + r * Math.sin(a)) }
  else if (shape === 'square') g.rect(c - r * 0.85, c - r * 0.85, r * 1.7, r * 1.7)
  else if (shape === 'triangle') { g.moveTo(c, c - r); g.lineTo(c + r * 0.95, c + r * 0.7); g.lineTo(c - r * 0.95, c + r * 0.7) }
  else if (shape === 'tower') { g.moveTo(c, c - r); g.lineTo(c + r * 0.6, c + r); g.lineTo(c - r * 0.6, c + r) }
  else if (shape === 'arrow') { g.moveTo(c, c - r); g.lineTo(c + r * 0.55, c + r * 0.2); g.lineTo(c + r * 0.18, c + r * 0.2); g.lineTo(c + r * 0.18, c + r); g.lineTo(c - r * 0.18, c + r); g.lineTo(c - r * 0.18, c + r * 0.2); g.lineTo(c - r * 0.55, c + r * 0.2) }
  else if (shape === 'camera') g.arc(c, c, r * 0.6, 0, Math.PI * 2)
  g.closePath()
}
function draw(shape: Shape, fill: string | null, stroke: string, size = 40, r = 13, lw = 3) {
  const c = document.createElement('canvas'); c.width = c.height = size
  const g = c.getContext('2d')!
  path(g, shape, size / 2, r)
  if (fill) { g.fillStyle = fill; g.fill() }
  g.lineWidth = lw; g.strokeStyle = stroke; g.stroke()
  return g.getImageData(0, 0, size, size)
}
export function iconFor(id: string, theme: 'dark' | 'light'): ImageData | null {
  const bg = theme === 'dark' ? '#0D0A09' : '#FFFFFF'
  const m = id.match(/^sev-(watch|warning|emergency)(-hollow)?$/)
  if (m) {
    const col = SEV[m[1]][theme]
    const shape: Shape = m[1] === 'watch' ? 'circle' : m[1] === 'warning' ? 'diamond' : 'octagon'
    return m[2] ? draw(shape, bg, col, 40, 12, 4) : draw(shape, col, bg, 40, 13, 3)
  }
  const teal = theme === 'dark' ? '#2EC4B6' : '#0F766E', mute = theme === 'dark' ? '#8A7A6F' : '#7A6B60', txt = theme === 'dark' ? '#F7EFE8' : '#1E1612'
  if (id === 'lora-gateway') return draw('square', teal, bg, 32, 10, 3)
  if (id === 'lora-relay') return draw('triangle', teal, bg, 32, 11, 3)
  if (id === 'lora-siren') return draw('diamond', bg, teal, 32, 9, 3)
  if (id === 'lora-dead') return draw('square', bg, mute, 32, 9, 3)
  if (id === 'village') return draw('square', txt, bg, 28, 7, 2)
  if (id === 'village-late') return draw('square', SEV.emergency[theme], bg, 28, 7, 2)
  if (id === 'tower-on') return draw('tower', mute, bg, 28, 9, 2)
  if (id === 'tower-off') return draw('tower', bg, mute, 28, 8, 2)
  if (id === 'camera') return draw('camera', mute, bg, 20, 7, 2)
  if (id === 'wind') return draw('arrow', theme === 'dark' ? 'rgba(191,175,163,0.85)' : 'rgba(84,70,61,0.85)', 'rgba(0,0,0,0)', 32, 13, 1)
  return null
}
export function installIconLoader(map: maplibregl.Map, getTheme: () => 'dark' | 'light') {
  // MapLibre 6: images are supplied on demand through the missing-image resolver (the event can no longer add them)
  map.setMissingStyleImageResolver((id) => {
    const img = iconFor(id, getTheme())
    if (img && !map.hasImage(id)) map.addImage(id, img, { pixelRatio: 2 })
  })
}
