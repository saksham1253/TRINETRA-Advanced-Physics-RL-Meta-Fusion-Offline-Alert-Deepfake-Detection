# ws4_cctv/failure_taxonomy.md — CCTV fire/smoke detection failure taxonomy (P8)

Phase P8 · WS4 · RESEARCH-ONLY. For each failure condition: what it is, what the literature says, and how a
failure-case TEST SET should be assembled later. This drives the evaluation protocol (nothing is measured
on our system — Rule 16). Mitigations are design requirements, not performance claims.

## A. Illumination / optical nuisances (false positives)
| Condition | Why it fools detectors | Literature stance | Test-set assembly |
|-----------|------------------------|-------------------|-------------------|
| Sunrise/sunset glow, sun in frame | orange/red + brightness mimic flame | high false-alarm source; needs temporal + spectral context | collect dawn/dusk clips per camera across seasons |
| Headlights / vehicle lights | bright flicker mimics flame flicker | temporal persistence + flicker-band physics (EF-08/B-05) help | night road-facing cameras |
| Reflections / glare (glass, water, metal) | moving bright blobs | motion+shape priors; multi-frame | wet/reflective-surface clips |
| Flashing/strobe lights, screens, signage | periodic brightness in flame band | aliasing-aware flicker (B-05) + color | indoor/commercial scenes |
| Red/orange objects (clothing, walls, banners) | color-only detectors trigger | require motion + growth, not color alone | static red-object scenes |

## B. Atmospheric / weather (smoke false positives & missed detections)
| Condition | Effect | Literature stance | Test-set |
|-----------|--------|-------------------|---------|
| Clouds / fog / haze | gray diffuse regions mimic smoke | hardest nuisance for smoke; temporal growth + sky-region priors | foggy/cloudy day clips, varied density |
| Dust / sandstorm | gray-brown plumes | multi-class smoke; cross-modal (IoT PM sensor) | dusty outdoor sites |
| Steam / water vapor (cooling, cooking, exhaust) | looks like white smoke | multi-class smoke (benign vs dangerous, D27); extinction/color (EF-07/B-01) | kitchens, industrial vents |
| Rain / snow on lens | occlusion + blur + motion | detect lens-state; abstain | rainy clips |

## C. Scene / camera degradations (missed detections)
| Condition | Effect | Literature stance | Test-set |
|-----------|--------|-------------------|---------|
| Low resolution / cheap optics | small/early smoke invisible | accuracy collapses for small objects/low-res | downscale real clips to CCTV res |
| Compression artifacts (H.264/H.265) | blocking/blur destroys smoke texture | evaluate at realistic bitrates | re-encode at low bitrates |
| Night / low light | flame visible, smoke not; IR needed | IR/thermal branch; different nuisances (hot sun/heaters) | night + IR camera clips |
| Camera shake / PTZ motion | global motion mimics plume motion | motion compensation; temporal | handheld/wind-shaken clips |
| Occlusion (foliage, structures) | partial smoke/flame | multi-view / persistence | occluded-scene clips |
| Domain shift between cameras/sites | model overfits one site | GROUP SPLITS by site; cross-site CIs | hold out whole sites |

## D. Target-difficulty (missed detections — the EARLY-WARNING hard case)
| Condition | Effect | Stance | Test-set |
|-----------|--------|--------|---------|
| Early / small / translucent smoke | lowest contrast, highest value to catch | the explicit hard case; use temporal growth (t²/plume) | curate smallest-smoke onset frames |
| Smoldering (little flame, slow smoke) | no flame cue | cross-modal (gas/temp IoT) + slow-growth | smoldering clips |
| Fast flashover / backdraft | too fast for slow confirmation | lower confirmation window when corroborated | rare-event clips (synthetic if needed) |

## E. Adversarial / security (ties WS2/P11)
| Threat | Effect | Defense (design requirement) |
|--------|--------|------------------------------|
| Camera blinding (laser/IR) | sensor saturation | detect saturation; health flag; abstain |
| Lens obstruction/tampering | blind spot | tamper detection; alert on scene-change |
| **Replayed-video spoofing** | fake "all clear" or fake alarm | liveness / stream-integrity check → WS2 deepfake handoff (P11); signed camera streams |
| Model adversarial patches | suppress/trigger detection | robustness testing; cross-modal voting |

## F. Privacy (design requirement, not a failure of detection)
Faces/people in CCTV → on-device processing + face blurring + data-minimization; evaluate that blurring does
NOT remove smoke/flame evidence.

## How these become the failure-case test set (plan)
1. Per nuisance/condition above, collect a labeled negative/positive set STRATIFIED BY SITE and CAMERA.
2. Keep whole sites held out (no leakage).
3. Report false-alarms-per-camera-day on the negatives and time-to-detection on the positives, per condition.
4. Pair with the IoT node (cross-modal) and the physics consistency checks (P7) to see which failures the
   anomaly layer (WS8/P9-P10) must catch — the supervised detector's blind spots are the anomaly target.

HONEST: this taxonomy is assembled from the literature + the P6/P7 reading; it is a TEST-DESIGN artifact.
No detection performance is claimed for our system (Rule 16).
