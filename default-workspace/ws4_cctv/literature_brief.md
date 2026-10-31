# WS4 — CCTV / RIVER-EYE (LSPIV) — literature brief (P4, 2026-10-07)
Owner phase: P8. Scope: camera-based surface-velocity/level sensing, scene perception, ₹2,000 River-Eye.

## Most relevant papers
- SAR/optical perception references from WS8 carry over for the satellite side; the camera side is thinly
  covered in the arXiv corpus (LSPIV accuracy at sub-₹2k is a GAP, G3).
- **2608.15261** optical–SAR routing — relevant pattern for fusing a noisy camera stream with satellite:
  route by learned task-utility before mixing so a fogged/blocked camera cannot drag the alarm.
- **2512.24117** Himalayan GLOF S1 pipeline — the perception front-end pattern (ingest → segment → area/level
  change → trigger) transfers to a River-Eye level/velocity front-end.

## Key claims → references
- A corrupt/stale camera modality must not degrade the fused alarm → utility routing (DC-09, 2608.15261).
- Perception (segmentation/level) is a front-end; outburst/flood TIMING is unsolved by perception alone
  (2512.24117 caveat) → feed physics gate + EVT prior, never alarm on perception alone.

## Open questions
- Sub-₹2,000 camera-LSPIV accuracy vs a real gauge — NO cited paper (G3). Resolve in P6 (BOM) + P8 (method).
- Night/monsoon/low-light robustness of a cheap camera — needs IR? (ties P6 BOM).
- Privacy/ethics of CCTV in public spaces — research note flagged for expert review (law/ethics).
