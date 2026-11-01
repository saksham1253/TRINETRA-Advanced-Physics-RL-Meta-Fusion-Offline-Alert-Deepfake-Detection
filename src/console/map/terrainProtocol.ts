import * as maplibregl from 'maplibre-gl'
import { terrariumTile, loadManifest } from './dem'

let registered = false
export function registerTerrainProtocol() {
  if (registered) return
  registered = true
  loadManifest()
  maplibregl.addProtocol('trn-dem', async (params) => {
    const [z, x, y] = params.url.replace('trn-dem://', '').split('/').map((v) => parseInt(v, 10))
    const { data } = await terrariumTile(z, x, y)
    return { data }
  })
}
