# Data sources (all cached locally; no runtime network needed)
| Data | Source | Licence | Key | Offline cache allowed | Built by |
|---|---|---|---|---|---|
| India boundary | DataMeet `Country/india-soi.geojson` (Survey of India state map) | CC BY-SA 2.5 / ODbL | no | yes | tools/build_geo_pack.py (simplified 0.01°) |
| State boundaries | DataMeet `States/Admin2.shp` | CC BY 4.0 | no | yes | tools/build_geo_pack.py |
| Rivers, world land | Natural Earth 10m rivers, 110m land | public domain | no | yes | tools/build_geo_pack.py |
| Terrain | AWS Terrain Tiles, Terrarium encoding (s3 elevation-tiles-prod) | open data; attribution per tilezen/joerd | no | yes (467 tiles, 31 MB) | tools/cache_terrain.py |
| Place search | GeoNames cities15000, IN | CC BY 4.0 | no | yes | tools/build_geo_pack.py (gazetteer) |
| Model evidence | TRINETRA/results/fire_meta/inputs (A final, F final OOF) | team | – | yes | tools/export_evidence_bank.py |
Boundary note: provider basemaps are not used at all, so no provider boundary can contradict the Survey of India depiction. Recorded 2026-11-01.
Not used yet: NASA FIRMS (MAP_KEY), Open-Meteo, GIBS, OSM tiles (bulk download is against policy), Esri (terms).
