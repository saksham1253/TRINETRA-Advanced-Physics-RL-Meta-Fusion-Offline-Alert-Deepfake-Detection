# ws2_deepfake/literature_map.md — synthetic-media detection & misinformation reading map (P11, WS2)

Phase P11 · RESEARCH-ONLY. 20 NEW primary arXiv papers (reader d335c060; 9 fetches, web_search unused).
HONEST: all ABS depth; IDs/years arXiv-ID-derived + subagent-reported, NOT independently re-fetched
(disclosed residual risk, §0.5); all metrics SOURCE-REPORTED ("not ours", Rule 16). Framing:
PROGRAM/sota/P11_sota_scan.md. Running body-level deep FT NEW total UNCHANGED at 100 (ABS breadth).

## Governing design consequence
Media forensics is ONE WEAK signal: against FRONTIER generators SOTA detectors AND humans/MLLMs fall to near
chance (DF26 2609.07369; CCDF 2610.07939; SLED-1400 2606.07613). Watermarks/C2PA are removable and false-fire
on clean media (2610.04151, 2610.11290, 2610.02010, 2609.34003). ⇒ trust = multi-source corroboration +
source credibility + human-in-the-loop under a cost matrix (system_design.md); out-of-context recycled REAL
media is the dominant disaster threat (WildFakeBench 2603.25423, MIC 2609.33441, NepOOC 2608.19212).

## A/D. Image forgery + universal / reasoning detectors
| arXiv | Short | Note (source-reported, not ours) |
|-------|-------|----------------------------------|
| 2609.39066 | ATAR agentic tool reasoning | 22 forensic tools, 2 reasoning streams + curriculum RL; 78.5% avg image F1 across 6 zero-shot IMDL benches (+11.8 vs best MLLM). Auditable evidence for the trust log; good unseen-manipulation transfer. |
| 2609.33585 | IVT-Guard all-in-one MLLM | unified image/video/text detector, artifact-aware pretrain + consistency-GRPO on IVT-Set (152K CoT); SOTA in/OOD/cross (own eval). Weakness: reasoning-vs-detection optimization dilemma (explicit reasoning can hurt acc). |

## B. Video / face-swap detection
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2610.11496 | MoDA + MAD bench | spatial-semantic + steganalysis-frequency cross-domain align; 94.8% in-dist / 89.1% cross / 81.94% unseen commercial / 78.13% open-internet; stays stable under white/gray/black-box attack while baselines collapse. KEY cross-gen + adversarial-robust recipe. |
| 2610.07939 | CCDF surveillance deepfakes ⚑ | 1,840 vids (Sora 2/VEO 3.1/Grok) across 16 CRIME/ACCIDENT categories; 10 SOTA detectors do NOT reliably separate fake from real; trivial metadata inflates, low-effort post-proc defeats. CLOSEST to disaster/accident imagery + CCTV corroboration threat. |
| 2610.03380 | Interpretable forensic+temporal | identity-trajectory → 68 descriptors → LSTM; F1 98.0% FF++ / 91.0% Celeb-DF v2 / 97.6% DFDC / 96.2% DeeperForensics. Transparent per-cue evidence; BUT classic (not frontier) benchmarks. |
| 2609.07369 | DF26 ⚑ generalization wall | 271 real / 2,420 synthetic from 7 modern T2V/I2V; humans AND SOTA detectors near chance. Detection alone cannot beat frontier video → corroborate externally. |

## C. Audio / speech deepfake
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2610.10121 | DuRe-ST graph back-end | spectro-temporal covariance affinity + graph attention; 25.9% rel. EER cut vs XLSR-AASIST on ASVspoof, 28.4% cross-dataset, +4-8k params. Cheap cross-dataset audio generalization. |
| 2610.07216 | Neural-codec vulnerability + PCL-NET | SOTA audio detectors collapse on codec-resynthesized speech; PCL-NET cuts EER 28.67%→12.77% over 7 codecs. DEGRADATION: re-uploaded social audio codec flips real→fake; normalize codec provenance first. |
| 2610.06339 | BabelFake multilingual AV | 399k clips, 496 consenting speakers, 5 langs, 11 video × 4 voice methods; detectors degrade when authentic audio preserved; cross-language/demographic sensitivity varies. Multilingual stress + AV-pairing. |
| 2610.10752 | DGAP adaptive purification | per-input diffusion purification via score-shift as reference-free adversarial flag; best defense vs 9 baselines across 3 detectors/3 attacks, even defense-aware. Plug-in audio hardening. |

## F. Provenance / watermarking + attacks
| arXiv | Short | Note (source-reported) — PROVENANCE LIMITS |
|-------|-------|--------------------------------------------|
| 2610.11290 | ProxyEraseAgent | blind single-image watermark removal, no decoder access; 94.8% success across 11 systems. Absence of watermark proves nothing. |
| 2610.02010 | Latent frequency masking | Fourier-coeff latent edit removes/weakens 6 diffusion watermarks, quality preserved. Robustness evals usually ignore this surface. |
| 2609.34003 | DeMark audio removal | query-free, no encoder/decoder; 0.92-0.96 success across 4 methods / 2 datasets, higher perceptual quality. Audio provenance needs corroboration. |
| 2610.04151 | Soft-bindings C2PA benchmark | PixelSeal best image/video, AudioSeal best audio; copy-detect ≤75.5% @FMR 1e-7; TrustMark FALSE-fires on 5.9-15.3% of UNMARKED images; watermark corrupts 62% of fingerprint codes; bits change x86 vs ARM. C2PA recoverable but imperfect; union still only ~69% coverage of attacked copies; verifier must test expected payload. |
| 2606.07613 | SLED-1400 human+MLLM study ⚑ | 200 real / 1,200 synthetic evidence photos, 6 T2I; humans 64.8% (≈chance on best gens); MLLMs 100% specificity but 5.9% detection on best; human/MLLM errors uncorrelated. Neither is a standalone authenticator → layered trust. |

## G. Out-of-context / recycled media + multimodal misinformation (HIGH PRIORITY)
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2609.33441 | MIC + MIC-Bench | AFC (SFT→GRPO) checks image-vs-claim context consistency w/ world knowledge; 8,812 instances; GRPO +4.67/+4.11 Macro-F1 (in/OOD). "Does image match claimed time/place" = the corroboration check; emits explanations. |
| 2608.19212 | NepOOC-M bilingual | first Nepali-English OOC bench, 1,090 pairs, κ=0.84; text-only mBERT 94.65% ≈ best multimodal, image-only near chance. WEAKNESS: OOC models lean on text, under-use image — risky when the IMAGE is the fabricated evidence. Multilingual/code-mixed relevance. |
| 2603.25423 | WildFakeBench + FakeAgent | 10k+ real micro-videos, expert attribution (manip/AIGC/cognitive-bias/OOC-reuse); Delphi multi-agent + retrieved external evidence beats MLLMs. Evidence-retrieval mirrors our corroboration pipeline; handles OOC reuse. |
| 2609.36850 | GAHR + Weibo26 | fuses "is-it-AIGC" (generativity) into news-veracity reasoning; Weibo26 mixes native+generated. Cleanly SEPARATES "is it synthetic" from "is the event true" — the two axes our trust system scores independently. |

## B/C physics / cross-modal
| arXiv | Short | Note (source-reported) |
|-------|-------|------------------------|
| 2609.15562 | PIVOT physics-grounded AV verify ⚑ | estimates physical quantities from audio+video, selects applicable laws, verifies constraints, returns evidence; 70.3%/64.3% (Real+Seedance), 72.2%/65.8% (Real+VEO), beats Gemini-3.1-Pro direct (~54-57%). PRIOR WORK for our physics_plausibility hypothesis — generator-agnostic but MODEST absolute accuracy. |

## AI-generated DISASTER/FIRE imagery (task 2/3 flag)
PARTIALLY addressed: CCDF (2610.07939) = fabricated CCTV crime/accident footage built BECAUSE such fakes
"misdirect emergency response" — the key benchmark + a core threat to our CCTV-corroboration path. PIVOT
(2609.15562) covers event-centric physical scenes. NO fire/wildfire-specific synthetic corpus exists →
documented GAP (ties to physics_plausibility.md study design + a future disaster-specific corpus).

---
## Synthesis 1 — CROSS-GENERATOR / GENERALIZATION
GENERALIZES better: frequency/steganalysis fingerprints + cross-domain alignment (MoDA 81.9% unseen
commercial, robust under attack); explicit physically-grounded features (2610.03380; PIVOT physics checks);
agentic tool+evidence reasoning (ATAR 78.5% zero-shot IMDL); audio graph covariance back-ends (DuRe-ST 28.4%
cross-dataset). OVERFITS/FAILS: frontier T2V/I2V (DF26 ≈ chance; CCDF 10 detectors unreliable), frontier T2I
(SLED-1400 MLLM 5.9%), reasoning-MLLM under shift (IVT-Guard dilemma), text-only OOC ignoring the image
(NepOOC). NET: external corroboration MANDATORY against frontier generators.

## Synthesis 2 — DEGRADATION & ADVERSARIAL
Codec/re-upload crashes audio detectors and flips bona-fide→fake (2610.07216, EER 28.7%→12.8% recovered by
PCL-NET); metadata/trivial cues + low-effort post-proc inflate then break video detectors (CCDF); classic
benches bake in compression bias (FF++). Adversarial: perturbation evasion (DGAP), robust recipes converge on
multi-domain (semantic+frequency) features (MoDA), input-adaptive diffusion purification (DGAP), and
consistency objectives disentangling laundering artifacts from the real/fake decision.

## Synthesis 3 — PROVENANCE / WATERMARK LIMITS
C2PA soft bindings (invisible watermark OR registry fingerprint) can re-attach a stripped manifest (best:
PixelSeal image/video, AudioSeal audio; copy-detect ≤75.5% @FMR 1e-7). But presence ≠ authentic, absence ≠
fake: blind image removal 94.8%/11 systems (ProxyEraseAgent), latent-frequency masking defeats 6 diffusion
watermarks (2610.02010), query-free audio removal 0.92-0.96 (DeMark); plus intrinsic failures — false-fire on
5.9-15.3% UNMARKED images, watermark corrupts 62% of fingerprints, bits change x86/ARM (2610.04151).
Verifier must test the EXPECTED PAYLOAD and combine watermark+fingerprint (still only ~69% coverage).

## Synthesis 4 — FORENSIC DATASETS FOUND → DATASETS.md
Reader-reported sets reconciled into DATASETS.md: FF++, Celeb-DF v2, DFDC, DeeperForensics, ASVspoof already
staged (D68-D75); NewsCLIPpings (D76); NEW this reconcile — CCDF (D77 ⚑), DF26, BabelFake, PhysForensics-
Bench, MAD, MIC-Bench, NepOOC, WildFakeBench, Weibo26, SLED-1400, Audio-Neural-Codec-Spoof, Soft-Bindings
C2PA benchmark. All [D] discovery-only, licenses INDICATIVE (several "not stated"/to-be-released); FACE/AV
sets carry consent/privacy constraints; many are small/narrow (flaws recorded in DATASETS.md).

## Tally
P11 NEW quota = 20 primary arXiv (≥15 required, aim ~40 — HONEST SHORTFALL vs the aspirational ~40: the
bounded reader hit 20 within its 14-fetch cap under the arXiv-throttling + no-web_search constraints; 20
exceeds the hard minimum of 15 and spans all 9 families, so the phase quota is MET but the stretch aim was
not reached; recorded plainly per §0.5). Depth all ABS (0 FT).