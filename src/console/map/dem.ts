// Terrarium elevation tiles: local cache first (public/tiles/terrarium, tools/cache_terrain.py), then online AWS Terrain Tiles
// when allowed, then the nearest cached ANCESTOR tile resampled (nearest-neighbour, so encoded values stay exact), then flat.
// Shared by the MapLibre protocol (terrain + hillshade) and by the LoRa line-of-sight sampler.
const BASE = import.meta.env.BASE_URL
const ONLINE_URL = 'https://s3.amazonaws.com/elevation-tiles-prod/terrarium'
let manifest: Set<string> | null = null
let manifestP: Promise<Set<string>> | null = null
export const demStats = { local: 0, online: 0, ancestor: 0, flat: 0, cachedTiles: 0 }
export const demConfig = { allowOnline: false }

export function loadManifest() {
  if (!manifestP)
    manifestP = fetch(`${BASE}tiles/terrarium/manifest.json`)
      .then((r) => r.json())
      .then((m: { tiles: string[] }) => {
        manifest = new Set(m.tiles)
        demStats.cachedTiles = manifest.size
        return manifest
      })
      .catch(() => (manifest = new Set()))
  return manifestP
}

// (bitmap cache kept for callers that need raw images)
const imgCache = new Map<string, Promise<ImageBitmap | null>>()
export function bitmap(url: string) {
  let p = imgCache.get(url)
  if (!p) {
    p = fetch(url)
      .then((r) => (r.ok ? r.blob() : Promise.reject(r.status)))
      .then((b) => createImageBitmap(b))
      .catch(() => null)
    imgCache.set(url, p)
    if (imgCache.size > 400) imgCache.delete(imgCache.keys().next().value as string)
  }
  return p
}
const localUrl = (z: number, x: number, y: number) => `${BASE}tiles/terrarium/${z}/${x}/${y}.png`

function canvas(w: number, h: number): OffscreenCanvas | HTMLCanvasElement {
  if (typeof OffscreenCanvas !== 'undefined') return new OffscreenCanvas(w, h)
  return Object.assign(document.createElement('canvas'), { width: w, height: h })
}
async function toPng(c: OffscreenCanvas | HTMLCanvasElement): Promise<ArrayBuffer> {
  if ('convertToBlob' in c) return (await c.convertToBlob({ type: 'image/png' })).arrayBuffer()
  return new Promise((res) => (c as HTMLCanvasElement).toBlob((b) => b!.arrayBuffer().then(res), 'image/png'))
}
let flatPng: Promise<ArrayBuffer> | null = null
function flat() {
  if (!flatPng) {
    const c = canvas(256, 256)
    const g = c.getContext('2d') as CanvasRenderingContext2D
    g.fillStyle = 'rgb(128,0,0)' // terrarium: (R*256 + G + B/256) - 32768 = 0 m
    g.fillRect(0, 0, 256, 256)
    flatPng = toPng(c)
  }
  return flatPng
}

export type TileSource = 'local' | 'online' | 'ancestor' | 'flat'
/** PNG bytes for a terrarium tile, plus where it came from. */
export async function terrariumTile(z: number, x: number, y: number): Promise<{ data: ArrayBuffer; source: TileSource }> {
  const m = manifest ?? (await loadManifest())
  const key = `${z}/${x}/${y}`
  if (m.has(key)) {
    const r = await fetch(localUrl(z, x, y))
    if (r.ok) {
      demStats.local++
      return { data: await r.arrayBuffer(), source: 'local' }
    }
  }
  if (demConfig.allowOnline) {
    try {
      const r = await fetch(`${ONLINE_URL}/${key}.png`)
      if (r.ok) {
        demStats.online++
        return { data: await r.arrayBuffer(), source: 'online' }
      }
    } catch {
      /* offline: fall through to the cached ancestor */
    }
  }
  for (let dz = 1; dz <= z; dz++) {
    const pz = z - dz, px = x >> dz, py = y >> dz
    if (!m.has(`${pz}/${px}/${py}`)) continue
    // decode the cached parent to metres, bicubic (Catmull-Rom) resample the sub-rectangle, re-encode as Terrarium.
    // Bicubic keeps the slope continuous, so hillshade has no facets (bilinear gives one flat facet per parent pixel).
    const G = await grid(pz, px, py)
    const n = 1 << dz, size = 256 / n
    const ox = (x - (px << dz)) * size, oy = (y - (py << dz)) * size
    const c = canvas(256, 256)
    const g = c.getContext('2d') as CanvasRenderingContext2D
    const img = g.createImageData(256, 256)
    const at = (i: number, j: number) => G[Math.min(255, Math.max(0, j)) * 256 + Math.min(255, Math.max(0, i))]
    const cr = (p0: number, p1: number, p2: number, p3: number, t: number) =>
      p1 + 0.5 * t * (p2 - p0 + t * (2 * p0 - 5 * p1 + 4 * p2 - p3 + t * (3 * (p1 - p2) + p3 - p0)))
    for (let j = 0; j < 256; j++) {
      const v = oy + (j + 0.5) / n - 0.5, j1 = Math.floor(v), tv = v - j1
      for (let i = 0; i < 256; i++) {
        const u = ox + (i + 0.5) / n - 0.5, i1 = Math.floor(u), tu = u - i1
        const row = (jj: number) => cr(at(i1 - 1, jj), at(i1, jj), at(i1 + 1, jj), at(i1 + 2, jj), tu)
        const e = cr(row(j1 - 1), row(j1), row(j1 + 1), row(j1 + 2), tv)
        const t = Math.min(65535.99, Math.max(0, e + 32768)), R = Math.floor(t / 256), Gc = Math.floor(t - R * 256)
        const k = (j * 256 + i) * 4
        img.data[k] = R; img.data[k + 1] = Gc; img.data[k + 2] = Math.min(255, Math.round((t - R * 256 - Gc) * 256)); img.data[k + 3] = 255
      }
    }
    g.putImageData(img, 0, 0)
    demStats.ancestor++
    return { data: await toPng(c), source: 'ancestor' }
  }
  demStats.flat++
  return { data: await flat(), source: 'flat' }
}

// ------------------------------------------------------------------ elevation sampling (LoRa line of sight, cursor readout)
const gridCache = new Map<string, Promise<Float32Array>>()
async function grid(z: number, x: number, y: number) {
  const key = `${z}/${x}/${y}`
  let p = gridCache.get(key)
  if (!p) {
    p = (async () => {
      const { data } = await terrariumTile(z, x, y)
      const bmp = await createImageBitmap(new Blob([data], { type: 'image/png' }))
      const c = canvas(256, 256)
      const g = c.getContext('2d', { willReadFrequently: true }) as CanvasRenderingContext2D
      g.drawImage(bmp, 0, 0)
      const px = g.getImageData(0, 0, 256, 256).data
      const out = new Float32Array(256 * 256)
      for (let i = 0; i < out.length; i++) out[i] = px[i * 4] * 256 + px[i * 4 + 1] + px[i * 4 + 2] / 256 - 32768
      return out
    })()
    gridCache.set(key, p)
  }
  return p
}
/** Elevation in metres (bilinear on the decoded tile grid) at zoom z. */
export async function elevation(lon: number, lat: number, z = 11) {
  const n = 2 ** z
  const fx = ((lon + 180) / 360) * n
  const r = (lat * Math.PI) / 180
  const fy = ((1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2) * n
  const tx = Math.floor(fx), ty = Math.floor(fy)
  const G = await grid(z, tx, ty)
  const u = (fx - tx) * 256 - 0.5, v = (fy - ty) * 256 - 0.5
  const i0 = Math.max(0, Math.min(255, Math.floor(u))), j0 = Math.max(0, Math.min(255, Math.floor(v)))
  const i1 = Math.min(255, i0 + 1), j1 = Math.min(255, j0 + 1)
  const a = Math.max(0, Math.min(1, u - i0)), b = Math.max(0, Math.min(1, v - j0))
  return (1 - a) * (1 - b) * G[j0 * 256 + i0] + a * (1 - b) * G[j0 * 256 + i1] + (1 - a) * b * G[j1 * 256 + i0] + a * b * G[j1 * 256 + i1]
}
