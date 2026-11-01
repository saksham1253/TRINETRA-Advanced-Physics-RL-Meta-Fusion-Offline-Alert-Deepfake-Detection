# 19c_REFERENCES_perception_deepfake_cctv -- TRINETRA reference catalogue (part of chapter 19)

> Row-level truth: `analysis/02_paper_ledger.csv`. Index, counts, MUST-READ TOP-30, dataset cross-index and BibTeX live in `docs/19_REFERENCES_FULL.md`.

> **Residual-identifier risk (per _CANON SS7):** every identifier below is a real ledger row, but identifiers were *subagent-reported during a web_search outage and were NOT independently re-fetched this pass*. No entry claims a resolved identifier unless its Verification line says so.

> Read-depth tags are copied verbatim from the ledger: FT / FT-PARTIAL / ABS / ABS-CANONICAL / FT-REF.


---

## Theme: Deepfake / media-forensics / crisis informatics  (`REF-DF-*`, 19 entries)

_Primary consumer: WS2 (ch 07), ch 14 ethics. The ledger axis/WS code that mapped each paper into this theme is printed per entry for traceability._

#### REF-DF-001 | 2609.39066
- arXiv/DOI: arXiv:2609.39066
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Agentic Tool-Augmented Reasoning for Explainable Image Forgery Detection (ATAR)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] agentic 22-tool forensic reasoning; auditable evidence
- Takeaway for TRINETRA: Two reasoning streams + curriculum RL; src-reported 78.5% avg image F1 across 6 zero-shot IMDL benches (+11.8 vs best MLLM). Good unseen-manipulation transfer; evidence for trust log. Source-reported. NEW. literature_map A/D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-002 | 2609.33585
- arXiv/DOI: arXiv:2609.33585
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: IVT-Guard: All-in-One Reasoning Model for AIGC Detection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] unified image/video/text MLLM detector w/ reasoning traces
- Takeaway for TRINETRA: Artifact-aware pretrain + consistency-GRPO on IVT-Set (152K CoT); src-reported SOTA in/OOD/cross (own eval). Weakness: reasoning-vs-detection optimization dilemma. Source-reported. NEW. literature_map A/D.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-003 | 2610.11496
- arXiv/DOI: arXiv:2610.11496
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: MoDA: Detecting and Attributing Motion-Aware Deepfake Videos (+MAD)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] semantic+steganalysis-frequency cross-domain align; attack-stable
- Takeaway for TRINETRA: Src-reported 94.8% in-dist/89.1% cross/81.94% unseen commercial/78.13% open-internet, 91.5% attribution; stable under white/gray/black-box attack while baselines collapse. KEY cross-gen + adversarial-robust recipe. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-004 | 2610.07939
- arXiv/DOI: arXiv:2610.07939
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: CCDF: Deepfake Detection in Real-World Surveillance Footage
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] FLAG: fabricated CCTV crime/accident footage fools detectors
- Takeaway for TRINETRA: 1,840 vids (Sora2/VEO3.1/Grok), 16 crime/accident categories; src-reported 10 SOTA detectors UNRELIABLE; metadata/post-proc defeat them. CLOSEST to disaster/accident + CCTV-corroboration threat; dataset D77. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-005 | 2609.07369
- arXiv/DOI: arXiv:2609.07369
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DF26: We Cannot Tell Fake From Real Anymore
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] FLAG: humans+SOTA detectors near chance on frontier T2V/I2V
- Takeaway for TRINETRA: 271 real/2,420 synthetic from 7 modern generators; src-reported both humans and detectors ~chance. Detection alone insufficient vs frontier video -> corroborate externally. Source-reported. NEW. literature_map B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-006 | 2610.10121
- arXiv/DOI: arXiv:2610.10121
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DuRe-ST: Dual-Relation Spectro-Temporal Speech Deepfake Detection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] cheap graph back-end, cross-dataset audio generalization
- Takeaway for TRINETRA: Spectro-temporal covariance affinity + graph attention; src-reported 25.9% rel EER cut vs XLSR-AASIST on ASVspoof, 28.4% cross-dataset, +4-8k params. Source-reported. NEW. literature_map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-007 | 2610.07216
- arXiv/DOI: arXiv:2610.07216
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Neural Codec Vulnerabilities in Audio Deepfake Detection (PCL-NET)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] DEGRADATION: codec re-upload flips bona-fide->fake
- Takeaway for TRINETRA: SOTA audio detectors collapse on codec-resynthesized speech; PCL-NET cuts EER 28.67%->12.77% over 7 codecs; dataset D87. Normalize codec provenance before scoring social audio. Source-reported. NEW. literature_map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-008 | 2610.06339
- arXiv/DOI: arXiv:2610.06339
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: BabelFake: Multilingual Audio-Visual DeepFake Benchmark
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] multilingual AV stress; detectors degrade on preserved authentic audio
- Takeaway for TRINETRA: 399k clips, 496 consenting speakers, 5 langs, 11 video x 4 voice methods; src-reported cross-language/demographic sensitivity varies, realism != detectability; dataset D79. Source-reported. NEW. literature_map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-009 | 2610.10752
- arXiv/DOI: arXiv:2610.10752
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DGAP: Detection-Guided Adaptive Purification for Robust Audio Deepfake Detection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] ADVERSARIAL defense: per-input diffusion purification, plug-in
- Takeaway for TRINETRA: Score-shift under light purification = reference-free adversarial flag; src-reported best defense vs 9 baselines across 3 detectors/3 attacks, even defense-aware. Source-reported. NEW. literature_map C.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-010 | 2610.11290
- arXiv/DOI: arXiv:2610.11290
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: ProxyEraseAgent: Blind Watermark Removal in the Wild
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] PROVENANCE LIMIT: blind single-image removal 94.8% across 11 systems
- Takeaway for TRINETRA: Proxy-decoder ranking + feedback-guided removal search, no decoder access; src-reported 94.8% attack success. Absence of watermark proves nothing. Source-reported. NEW. literature_map F.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-011 | 2610.02010
- arXiv/DOI: arXiv:2610.02010
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Weaknesses of Generative Image Watermarks against Latent Frequency Masking
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] PROVENANCE LIMIT: Fourier latent edit defeats 6 diffusion watermarks
- Takeaway for TRINETRA: Replaces latent Fourier coeffs, quality preserved, theoretical distortion bound; src-reported removes/weakens across 6 methods on DiffusionDB+MS-COCO. Source-reported. NEW. literature_map F.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-012 | 2609.34003
- arXiv/DOI: arXiv:2609.34003
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DeMark: Query-Free Black-Box Audio Watermark Removal
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] PROVENANCE LIMIT: query-free audio watermark removal 0.92-0.96
- Takeaway for TRINETRA: No encoder/decoder access; suppresses non-speech TF artifacts under quality constraints; src-reported 0.92-0.96 success across 4 methods/2 datasets. Audio provenance needs corroboration. Source-reported. NEW. literature_map F.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-013 | 2610.04151
- arXiv/DOI: arXiv:2610.04151
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Watermarks and Fingerprints as Soft Bindings for Content Provenance
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: yes | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] C2PA benchmark: recoverable but imperfect; false-fires on clean media
- Takeaway for TRINETRA: PixelSeal/AudioSeal best; copy-detect <=75.5% @FMR 1e-7; TrustMark false-fires 5.9-15.3% of UNMARKED; watermark corrupts 62% fingerprints; bits change x86/ARM; union ~69% coverage. Verifier must test expected payload; dataset D88.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-014 | 2606.07613
- arXiv/DOI: arXiv:2606.07613
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Can You Trust What You See? Synthetic Legal Evidence (SLED-1400)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] neither humans nor MLLMs reliable standalone authenticators
- Takeaway for TRINETRA: 200 real/1,200 synthetic evidence photos, 6 T2I; src-reported humans 64.8% (~chance on best gen), MLLMs 100% specificity/5.9% detection on best, errors uncorrelated; dataset D86. Mandates layered trust. Source-reported. NEW.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-015 | 2609.33441
- arXiv/DOI: arXiv:2609.33441
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: MIC: Explaining Image-Claim Inconsistencies in Multimodal Misinformation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] image-vs-claim context consistency = the corroboration check
- Takeaway for TRINETRA: AFC (SFT->GRPO) w/ world knowledge; MIC-Bench 8,812 instances; src-reported GRPO +4.67/+4.11 Macro-F1 (in/OOD); dataset D82. Emits explanations for trust log. Source-reported. NEW. literature_map G.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-016 | 2608.19212
- arXiv/DOI: arXiv:2608.19212
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: NepOOC-M: Bilingual Nepali-English Out-of-Context Benchmark
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] multilingual OOC; detectors lean on text, under-use image
- Takeaway for TRINETRA: 1,090 pairs, 5 typologies, kappa 0.84; src-reported text-only mBERT 94.65% ~= best multimodal, image-only near chance; dataset D83. Risk when the IMAGE is the fabricated evidence. Source-reported. NEW. literature_map G.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-017 | 2603.25423
- arXiv/DOI: arXiv:2603.25423
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: From Manipulation to Mistrust: Micro-Video Misinformation (WildFakeBench+FakeAgent)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] evidence-retrieval multi-agent mirrors corroboration pipeline
- Takeaway for TRINETRA: 10k+ real micro-videos expert-attributed (manip/AIGC/cognitive/OOC-reuse); Delphi multi-agent + retrieved evidence beats MLLMs; dataset D84. Handles OOC reuse of real footage. Source-reported. NEW. literature_map G.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-018 | 2609.36850
- arXiv/DOI: arXiv:2609.36850
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Rethinking Multimodal Fake News Detection in the Generative AI Era (GAHR+Weibo26)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] separates is-it-synthetic from is-the-event-true (two trust axes)
- Takeaway for TRINETRA: Fuses generativity into veracity reasoning; Weibo26 mixes native+generated; dataset D85. Maps directly to our two independent trust scores. Source-reported. NEW. literature_map G.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DF-019 | 2609.15562
- arXiv/DOI: arXiv:2609.15562
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PIVOT: Physics-Grounded Verification for AI-Generated Audio-Video Detection
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS2 | phase: P11
- Uses (workstream/chapter): WS2 (ch 07), ch 14 ethics
- Core method: [P11] PRIOR WORK for physics-plausibility hypothesis; generator-agnostic, MODEST acc
- Takeaway for TRINETRA: Estimates physical quantities, selects laws, verifies constraints, returns evidence; src-reported 70.3%/64.3% (Real+Seedance), 72.2%/65.8% (Real+VEO), beats Gemini-3.1-Pro direct ~54-57%; dataset D80.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass


---

## Theme: CCTV / UAV / satellite fire-smoke perception  (`REF-CCTV-*`, 71 entries)

_Primary consumer: WS4 (ch 09), ch 05 fire_cnn, edge features. The ledger axis/WS code that mapped each paper into this theme is printed per entry for traceability._

#### REF-CCTV-001 | 2306.00001
- arXiv/DOI: arXiv:2306.00001
- Authors: Moosmann; Giordano; Vogt; Magno
- Title: TinyissimoYOLO: Quantized Low-Memory TinyML Object Detection for Low-Power Microcontrollers
- Year / Venue: 2023 / IEEE AICAS 2023
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: 422k-param INT8 YOLO, 180fps 196uJ on MAX78000
- Takeaway for TRINETRA: Ultra-light quantized object detector: 422k params, <0.5MB weights, runs on MAX78000 CNN-accelerator MCU at up to 180fps and only 196uJ/inference (>106 MAC/cycle); 8-bit quantization-aware training deployed on STM32H7/L4, Apollo4b, MAX78000...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-002 | 2105.13331
- arXiv/DOI: arXiv:2105.13331
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Quantization and Deployment of Deep Neural Networks on Microcontrollers
- Year / Venue: 2021 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: int/float quantization framework for MCU deployment
- Takeaway for TRINETRA: Studies embedding AI on low-power MCUs via quantization (fixed-point/int) and a deployment framework spanning common MCU targets; characterizes accuracy/memory/latency tradeoffs.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-003 | 2402.02781
- arXiv/DOI: arXiv:2402.02781
- Authors: Xiao; Das
- Title: Dual Knowledge Distillation for Efficient Sound Event Detection
- Year / Venue: 2024 / ICASSP 2024
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: dual KD compresses sound-event-detection to 1/3 params for edge, beats baseline
- Takeaway for TRINETRA: Dual knowledge distillation for on-device Sound Event Detection: temporal-averaging KD (mean-student from temporal averaging of student params, for STABLE distillation) + embedding-enhanced feature distillation (embedding layer for contextu...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-004 | 2604.27178
- arXiv/DOI: arXiv:2604.27178
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Energy-Efficient Plant Monitoring via Knowledge Distillation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: distill heavy ViT/FM teacher into compact low-energy student for field monitoring
- Takeaway for TRINETRA: SOTA plant species/disease recognition uses high-capacity ViTs / multimodal FOUNDATION MODELS that are too computationally heavy for field deployment; uses knowledge distillation to compress into an energy-efficient student for on-device en...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-005 | 2202.07475
- arXiv/DOI: arXiv:2202.07475
- Authors: Ofli; Qazi; Imran; Roch; Pennington; Banks; Bossu
- Title: A Real-time System for Detecting Landslide Reports on Social Media using AI
- Year / Venue: 2022 / Springer
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: opportunistic vision / crowd reports
- Takeaway for TRINETRA: Operational Twitter landslide detector (dedup, image classify, geolocate). Supports an auxiliary crowd-report ingestion channel as a cheap redundant sensor; deployment-tested since 2020.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-006 | 2310.05330
- arXiv/DOI: arXiv:2310.05330
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A Lightweight Video Anomaly Detection Model with Weak Supervision and Adaptive Instance Selection
- Year / Venue: 2024 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: River Eye / CCTV VAD
- Takeaway for TRINETRA: Weakly-supervised VAD (video-level labels only) with small model + adaptive instance selection. Matches TRINETRA's label-scarce edge CCTV; weak supervision is realistic vs frame-level labels. Supports edge-VAD feasibility (Bug #14).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-007 | 2412.18298
- arXiv/DOI: arXiv:2412.18298
- Authors: Ding; Wang
- Title: Quo Vadis, Anomaly Detection? LLMs and VLMs in the Spotlight
- Year / Venue: 2024 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: CCTV VAD survey
- Takeaway for TRINETRA: Review of 2024 LLM/VLM VAD: interpretability, temporal reasoning, few/zero-shot, open-world anomalies. Maps the VAD design space + zero-shot option for unseen hazard appearances on River Eye nodes.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-008 | 2507.20102
- arXiv/DOI: arXiv:2507.20102
- Authors: Wang; Hu; Ai; Lee
- Title: On Uncertainty Prediction for Deep-Learning-based Particle Image Velocimetry
- Year / Venue: 2025 / ISPIV 2025
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: LSPIV / River Eye uncertainty
- Takeaway for TRINETRA: UQ for DL-PIV via uncertainty NN / multi-model / multi-transform; UNN best; UQ 'largely overlooked'.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-009 | 2312.06461
- arXiv/DOI: arXiv:2312.06461
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Variational Auto-Encoder Based Deep Learning Technique For Filling Gaps in Reacting PIV Data
- Year / Venue: 2023 / arXiv (physics.flu-dyn)
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: LSPIV gap-filling
- Takeaway for TRINETRA: CVAE fills gaps/dropouts in PIV vector fields. River Eye nodes will have occlusion/night/turbidity gaps; this is a method to impute missing LSPIV velocity rather than drop frames (robustness for Bug #8 brownout).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-010 | 2503.12905
- arXiv/DOI: arXiv:2503.12905
- Authors: Qian; Ye; Wang; Cai; Qian; Wu
- Title: UCF-Crime-DVS: Event-Based Dataset for VAD with Spiking Neural Networks
- Year / Venue: 2025 / AAAI 2025
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: edge VAD / event camera
- Takeaway for TRINETRA: Event-camera (DVS) + spiking-NN VAD: high dynamic range, low data redundancy, efficient. Alt sensing+compute path for TRINETRA's edge CCTV where power/bandwidth constrained; SNN energy efficiency relevant to #14 edge-latency.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-011 | 2203.03962
- arXiv/DOI: arXiv:2203.03962
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Generative Cooperative Learning for Unsupervised Video Anomaly Detection
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: unsupervised VAD
- Takeaway for TRINETRA: Unsupervised VAD (no labels) via generative cooperative learning; anomalies rare + ill-defined.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-012 | 2605.14645
- arXiv/DOI: arXiv:2605.14645
- Authors: Sun
- Title: Vision-Based Water Level and Flow Estimation
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: vision river level+velocity (SOTA+stats)
- Takeaway for TRINETRA: Integrates SOTA vision models with statistical modeling + physical priors + robust filtering for water-level and river-surface-velocity estimation; names the real challenges: environmental sensitivity, limited precision, complex site calibr...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-013 | 1607.04139
- arXiv/DOI: arXiv:1607.04139
- Authors: Benetazzo; Gamba; Barbariol
- Title: Unseeded Large Scale PIV measurements accounting for capillary-gravity waves phase speed
- Year / Venue: 2016 / arXiv (physics.flu-dyn)
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: LSPIV unseeded bias correction
- Takeaway for TRINETRA: LSPIV measures river surface velocity from image sequences but in UNSEEDED conditions (no floating tracers) capillary-gravity waves travel in all directions and CONTAMINATE the velocity estimate; proposes wavenumber-based discrimination/cor...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-014 | 2401.06229
- arXiv/DOI: arXiv:2401.06229
- Authors: Mendez Rios; Le Coz; Renard; Terraz
- Title: Bayesian estimation of a 1D hydrodynamic model in a tidal river (Lower Seine)
- Year / Venue: 2023 / SHF colloque
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: rating-curve uncertainty / Manning-Strickler
- Takeaway for TRINETRA: Shows the stage-discharge (rating-curve) relation and Manning-Strickler surface-velocity method BREAK DOWN under unsteady/transient flow; uses a Bayesian-calibrated 1D Saint-Venant model (Mage+BaM!) to quantify friction-coefficient uncertai...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-015 | 2604.08581
- arXiv/DOI: arXiv:2604.08581
- Authors: Albaiz; Amsaad
- Title: Fully Autonomous Z-Score TinyML Anomaly Detection on Resource-Constrained MCUs
- Year / Venue: 2026 / IEEE SaTC 2026
- Read depth: ABS | local note: no | ledger axis/WS: A9 | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: on-MCU train+infer; concrete footprint/latency
- Takeaway for TRINETRA: Fully on-device (STM32 MCU) TinyML anomaly detector: trains AND infers on the MCU with NO cloud/connectivity, using RMS + lightweight Z-Score thresholds; ~3.3 KB SRAM / 63 KB Flash, tens-of-microseconds inference, P/R=1.00 on a 14-day fridg...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-016 | 2508.14203
- arXiv/DOI: arXiv:2508.14203
- Authors: (backfill)
- Title: Survey of video anomaly detection across human/vehicle/environment anomalies
- Year / Venue: 2026 / arXiv
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A9 | phase: P2
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P2] robustness C8/C10 + VAD taxonomy
- Takeaway for TRINETRA: VAD survey; input/anomaly-type taxonomy; cross-scene robustness (C8/C10) framing for WS4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-017 | 2507.21649
- arXiv/DOI: arXiv:2507.21649
- Authors: (backfill)
- Title: Survey: Evolution of Video Anomaly Detection from DNN to MLLM
- Year / Venue: 2026 / arXiv
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A9 | phase: P2
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P2] VAD doctrine (WS4)
- Takeaway for TRINETRA: Grounding(edge) vs understanding(cloud) split; input menu (RGB/flow/skeleton/hybrid); VLMs not drop-in. Structures WS4 edge/cloud tiering.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-018 | 2609.20441
- arXiv/DOI: arXiv:2609.20441
- Authors: Schmalstieg; Mueller; Samek
- Title: Cross-Architecture Foundation-Model Distillation for Edge Flood Segmentation
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A9 | phase: P2
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P2] CR-02 flood + edge (CR-01)
- Takeaway for TRINETRA: Prithvi-EO-2.0 300M → EfficientViT-B0 0.7M INT8 (5.57ms Jetson, 1.5MB); pseudo-label amplification. KEY: fixed MNDWI rule competitive with both deep models on clean external benchmarks (CR-02, flood domain).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-019 | 2609.07455
- arXiv/DOI: arXiv:2609.07455
- Authors: Thuau; Gran; Haidar; Chelouah
- Title: Parser-Free VLM Verification for Federated Weakly Supervised Video Anomaly Detection
- Year / Venue: 2026 / AVSS 2026
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A9 | phase: P2
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P2] federated privacy + VLM verify (WS4)
- Takeaway for TRINETRA: Federated MIL (small scorer trained across clients, raw video stays local) + frozen VLM verifies suspects post-hoc. Text-gen verification prompt-fragile (−1.36 to +1.55 AUC); logit interface robust parser-free.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-020 | 2609.05066
- arXiv/DOI: arXiv:2609.05066
- Authors: Li; Xiao
- Title: Adaptive Multi-Granularity Temporal Modeling for Weakly Supervised Video Anomaly Detection
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A9 | phase: P2
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P2] adaptive temporal VAD (WS4)
- Takeaway for TRINETRA: Temporal Refinement + Event Segmentation + adaptive score fuse → variable-duration events vs fixed snippets. Our hazards span seconds→hours so adopt adaptive granularity.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-021 | 2610.06453
- arXiv/DOI: arXiv:2610.06453
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: NCL: Normal-Subspace Constrained Learning for Foundation-Model Anomaly Detection
- Year / Venue: 2026 / arXiv
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A9 | phase: P3
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P3] anomaly/TS-AD WS8 (new FM)
- Takeaway for TRINETRA: Foundation models reconstruct ANOMALIES too well → error-score collapse. Fix = normal-subspace constraint (few-shot SVD) + patch transform + contrastive.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-022 | 2610.00363
- arXiv/DOI: arXiv:2610.00363
- Authors: Bouketta; Niar; Ouarnoughi
- Title: Deep Learning for Anomaly Detection in Railway Systems: A Structured Survey
- Year / Venue: 2026 / Eng. Applications of AI 115776
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A9 | phase: P3
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P3] anomaly survey/seminal — organizing ref
- Takeaway for TRINETRA: Unified taxonomy: by location / manifestation (point/contextual/collective) / sensing modality / temporal behavior; 4 paradigms classification/prediction/reconstruction/hybrid; edge-cloud deployment decision framework.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-023 | 2605.23504
- arXiv/DOI: arXiv:2605.23504
- Authors: Cencillo; Concepción; Triguero; Luengo
- Title: VACE: Learning Geometrically Structured Representations for Time-Series Anomaly Detection
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A9 | phase: P3
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P3] TSAD WS8 normal=geometry + CR-02 + eval
- Takeaway for TRINETRA: Velocity-consistency SSL (no negatives, no synthetic anomalies) learns a compact directionally-coherent normal manifold; score = Mahalanobis positional × velocity-bank directional (off-distribution AND dynamically atypical).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-024 | 2112.08598
- arXiv/DOI: arXiv:2112.08598
- Authors: Dewangan; et al.
- Title: FIgLib & SmokeyNet: Dataset and Deep Learning Model for Real-Time Wildland Fire Smoke Detection
- Year / Venue: 2022 / Remote Sensing 14(4):1007
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8 | re-cited 2x
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] canonical fixed-camera early-smoke baseline
- Takeaway for TRINETRA: ~25k fixed-view HPWREN smoke images (FIgLib) + SmokeyNet (CNN+LSTM+ViT) on consecutive frames; src-reported 'rivals human' (qualitative; exact F1/TTD not in abstract).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-025 | 2402.05349
- arXiv/DOI: arXiv:2402.05349
- Authors: PyroNear team
- Title: Constructing a Real-World Benchmark for Early Wildfire Detection: PYRONEAR-2025
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8 | re-cited 2x
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] real-world multi-site early-wildfire camera benchmark
- Takeaway for TRINETRA: Field-collected camera-network dataset for operational early detection; headline metric truncated (not retrieved). Multi-site structure enables site/camera-grouped leakage-safe splits + realistic false-alarm estimation.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-026 | 2010.08833
- arXiv/DOI: arXiv:2010.08833
- Authors: Thomson; Bhowmik; Breckon
- Title: Efficient and Compact CNN Architectures for Non-temporal Real-time Fire Detection
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8 | re-cited 2x
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] proven low-power edge baseline (Jetson Xavier-NX)
- Takeaway for TRINETRA: ShuffleNetV2-OnFire / NasNet-A-OnFire single-frame fire detection; src-reported 95% full-frame acc, 97% superpixel, 49 fps full-frame on Xavier-NX. Best-documented true edge baseline; non-temporal → likely optimistic vs CCTV nuisance.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-027 | 2510.10108
- arXiv/DOI: arXiv:2510.10108
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Uncertainty-Aware Post-Detection Framework for Fire/Smoke in Compact DL Models
- Year / Venue: 2025 / ICSM 2025
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] lightweight false-alarm re-scoring head on D-Fire
- Takeaway for TRINETRA: YOLOv5n/v8n on D-Fire + Confidence Refinement Net re-scores via uncertainty+color/edge/texture; names NMS/Soft-NMS as a concrete false-alarm/suppression failure mode; src-reported precision/recall/mAP gains (deltas not in abstract).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-028 | 2609.18227
- arXiv/DOI: arXiv:2609.18227
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: WISE: Lightweight Weakly-Supervised Model for Onboard Fire Smoke Detection and Localization
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8 | re-cited 2x
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] weak-label + distillation sub-million-param edge recipe
- Takeaway for TRINETRA: Tile-level weak labels → teacher soft-supervision → WISE-Student predicts tile presence + smoke map in one pass; src-reported tile-F1 0.964, pixel-F1 0.750, 0.12M params, ~3 GFLOPs, 0.10-0.26 s/tile (satellite domain).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-029 | 2408.10843
- arXiv/DOI: arXiv:2408.10843
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Detecting Wildfires on UAVs with Real-time Segmentation Trained by Larger Teacher Models
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] teacher->student distillation for edge segmentation
- Takeaway for TRINETRA: Distill a large teacher into a small real-time segmentation student for on-UAV early detection; metric truncated. Core distillation technique for the edge shortlist. Source-reported. NEW. literature_map #17.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-030 | 2307.00104
- arXiv/DOI: arXiv:2307.00104
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Obscured Wildfire Flame Detection by Temporal Analysis of Smoke Patterns
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8 | re-cited 2x
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] occlusion failure mode -> smoke-motion remedy
- Takeaway for TRINETRA: When flames are occluded (trees/structures), detect via temporal smoke-motion patterns; metric truncated. Documents occlusion as a failure mode and motion/temporal cues as remedy. Source-reported. NEW. literature_map #23.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-031 | 1703.05530
- arXiv/DOI: arXiv:1703.05530
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Dynamic Texture Classification using CNN on Three Orthogonal Planes
- Year / Venue: 2017 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] smoke as spatiotemporal dynamic texture
- Takeaway for TRINETRA: CNN over XY/XT/YT planes for dynamic textures incl. smoke+vegetation; metric truncated. Foundational: single-frame appearance insufficient; vegetation/water/fabric are dynamic-texture confusers. Source-reported. NEW. literature_map #25.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-032 | 2509.12701
- arXiv/DOI: arXiv:2509.12701
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: SmokeBench: A Real-World Dataset for Surveillance Image Desmoking in Early-Stage Fire Scenes
- Year / Venue: 2025 / ACM MM 2025
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] early-stage (0-15 min) thin-smoke surveillance regime
- Takeaway for TRINETRA: Real-world desmoking dataset for the critical 0-15 min post-ignition window on surveillance cameras; metric truncated. Characterizes the early-stage hard case + preprocessing asset (DATASETS D40). Source-reported. NEW. literature_map #20.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-033 | 2512.01788
- arXiv/DOI: arXiv:2512.01788
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Learned Image Compression for Earth Observation: Implications for Downstream Segmentation
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] compression choice measurably affects fire segmentation
- Takeaway for TRINETRA: Compares JPEG2000 vs learned compressor on downstream EO segmentation incl. a Fire task; metric truncated. Direct evidence that compression must be IN the evaluation protocol for cheap CCTV streams. Source-reported. NEW. literature_map #19.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-034 | 2410.16631
- arXiv/DOI: arXiv:2410.16631
- Authors: Han; et al.
- Title: Benchmarking Multi-Scene Fire and Smoke Detection (FSD)
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] field bottleneck = non-standardized datasets/metrics
- Takeaway for TRINETRA: Argues public FSD datasets lack standardized construction/uniform evaluation/clear baselines; regathers+relabels into a unified multi-scene benchmark. Supports the standardized leakage-aware protocol argument (DATASETS D38).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-035 | 2508.11696
- arXiv/DOI: arXiv:2508.11696
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A DL-Based CCTV System for Automatic Smoking Detection in Fire Exit Zones (WITHDRAWN)
- Year / Venue: 2025 / arXiv (withdrawn)
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] self-admitted LEAKAGE cautionary case
- Takeaway for TRINETRA: Authors WITHDREW: augmentation 'likely introduced data leakage across train/val/test splits, making results unreliable and non-reproducible' + metric inconsistency. Textbook example of the exact P8 pitfalls → mandate group splits.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-036 | 2512.11215
- arXiv/DOI: arXiv:2512.11215
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: SmokeBench: Evaluating Multimodal LLMs for Wildfire Smoke Detection
- Year / Venue: 2025 / WACV 2026
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] MLLMs fail early/small-smoke localization
- Takeaway for TRINETRA: Benchmark over Qwen2.5-VL/InternVL3/GPT-4o/Gemini-2.5/Grounding-DINO etc.; src-reported: all struggle localization esp. early-stage; perf scales with smoke VOLUME not contrast.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-037 | 2412.20006
- arXiv/DOI: arXiv:2412.20006
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Adversarial Robustness for Deep Learning-based Wildfire Prediction Models
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] only adversarial-robustness fire paper found
- Takeaway for TRINETRA: Studies adversarial robustness of DL wildfire models; metric truncated. Supports adversarial stress-tests in the protocol; targets prediction models — dedicated CCTV tamper/blinding/replay-spoof + privacy work was ABSENT in arXiv-only searc...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-038 | 2603.02465
- arXiv/DOI: arXiv:2603.02465
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Toward Generalizable DL-Based Peatland Fire Detection via Walsh-Hadamard Transform and Domain Adaptation
- Year / Venue: 2026 / SIViP (Springer)
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P8
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P8] tackles domain shift / cross-site generalization
- Takeaway for TRINETRA: Walsh-Hadamard feature stage + domain adaptation for cross-domain wildfire detection; metric truncated. Directly addresses the central leakage-safe/generalization concern. Source-reported. NEW. literature_map #40.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-039 | 2303.15389
- arXiv/DOI: arXiv:2303.15389
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: EVA-CLIP: Improved Training Techniques for CLIP at Scale
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T1
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T1] 82.0/80.4 zero-shot ImageNet-1K top-1
- Takeaway for TRINETRA: strong frozen open-vocab backbone; src-reported. Raw cosine/logit -> needs calibration before fusion. Source-reported. NEW. literature_map P14Z-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-040 | 2403.15378
- arXiv/DOI: arXiv:2403.15378
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Long-CLIP: Unlocking the Long-Text Capability of CLIP
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T1
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T1] long-text CLIP, +~6% COCO/Flickr retrieval keeps zero-shot
- Takeaway for TRINETRA: src-reported +~20% long-caption retrieval. Long descriptive hazard prompts. Source-reported. NEW. literature_map P14Z-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-041 | 2510.02270
- arXiv/DOI: arXiv:2510.02270
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: microCLIP: Unsupervised CLIP Adaptation via Coarse-Fine Token Fusion
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T1
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T1] +2.90% over 13 fine-grained benchmarks, label-free
- Takeaway for TRINETRA: coarse-fine token fusion self-training; src-reported. Sharpens smoke-vs-steam (adaptation not pure ZS). Source-reported. NEW. literature_map P14Z-T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-042 | 2306.09269
- arXiv/DOI: arXiv:2306.09269
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Zero-Shot Anomaly Detection with Pre-trained Segmentation Models (VAND WinCLIP)
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T2
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T2] VisA F1-max 81.5 sample / 24.2 pixel
- Takeaway for TRINETRA: WinCLIP-based ZS anomaly + segmentation; src-reported 3rd VAND-2023. Unknown-hazard analogue; weak localization -> calibrate. Source-reported. NEW. literature_map P14Z-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-043 | 2512.02520
- arXiv/DOI: arXiv:2512.02520
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: On the Problem of Consistent Anomalies in Zero-Shot Anomaly Detection (CoDeGraph)
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T2
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T2] FAILURE MODE: consistent anomalies bias distance-based ZS
- Takeaway for TRINETRA: similarity-scaling/neighbor-burnout; graph-community filter; src-reported. Recurring nuisances (haze/glare) mis-scored. Source-reported. NEW. literature_map P14Z-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-044 | 2510.15602
- arXiv/DOI: arXiv:2510.15602
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Quantized FCA: Efficient Zero-Shot Texture Anomaly Detection
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T2
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T2] real-time ZS texture anomaly, ~10x speedup ~equal accuracy
- Takeaway for TRINETRA: PCA preprocessing boosts contrast; src-reported. ZS anomaly at CCTV frame rates. Source-reported. NEW. literature_map P14Z-T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-045 | 2501.16404
- arXiv/DOI: arXiv:2501.16404
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DynaPrompt: Dynamic Test-Time Prompt Tuning
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T3
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T3] online TTPT, entropy+prob-diff selection, anti-collapse, 14 datasets
- Takeaway for TRINETRA: src-reported beats prior TPT. Per-camera label-free adaptation; signals feed calibration. Source-reported. NEW. literature_map P14Z-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-046 | 2512.12268
- arXiv/DOI: arXiv:2512.12268
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: MetaTPT: Meta Test-time Prompt Tuning for VLMs
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T3
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T3] meta dual-loop TPT, SOTA domain-generalization
- Takeaway for TRINETRA: learned per-sample augmentations; src-reported. Targets site/weather/lens shift. Source-reported. NEW. literature_map P14Z-T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-047 | 2107.13029
- arXiv/DOI: arXiv:2107.13029
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: A New Split for Evaluating True Zero-Shot Action Recognition (TruZe)
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T4
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T4] EVALUATION FAILURE: leakage inflates ZS up to 8.9% (few-shot 17.1%)
- Takeaway for TRINETRA: leakage-free split; src-reported. De-rate external ZS numbers for leakage. Source-reported. NEW. literature_map P14Z-T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-048 | 2605.01165
- arXiv/DOI: arXiv:2605.01165
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: CEZSAR: Contrastive Embedding Method for Zero-Shot Action Recognition
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T4
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T4] SOTA UCF-101/Kinetics-400 ZS action recognition
- Takeaway for TRINETRA: contrastive video-sentence + auto negatives; src-reported. Video-level open-vocab event complement; uncalibrated. Source-reported. NEW. literature_map P14Z-T4.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-049 | 2504.13231
- arXiv/DOI: arXiv:2504.13231
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: WildFireCan-MMD: Multimodal Dataset for UGC Classification During Wildfires
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T5
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T5] custom 84.48% f-score BEATS zero-shot VLMs
- Takeaway for TRINETRA: Canadian wildfire X posts, 12 themes (D99); src-reported. Trained beats ZS in fire domain. Source-reported. NEW. literature_map P14Z-T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-050 | 2610.10946
- arXiv/DOI: arXiv:2610.10946
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: AI4Fire: Evaluating LLMs on Wildfire Tasks
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T5
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T5] NO core zero-shot model beat trivial baselines; leakage/label flaws
- Takeaway for TRINETRA: 5 wildfire tasks bare vs grounded (D100); src-reported grounding helps when input carries answer. Complement-not-replace; grounded-reference trick. Source-reported. NEW. literature_map P14Z-T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-051 | 2607.07951
- arXiv/DOI: arXiv:2607.07951
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Evaluating Generalizability of Foundation Models for California Wildfire PM2.5
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: n/r | re-cited 2x
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T5/T6] BiLSTM beats FMs; ZS Chronos-2 negative-R2 tail instability
- Takeaway for TRINETRA: 6 time-series FMs vs trained (D101); src-reported LoRA repairs but no FM beats trained. ZS tail-unstable OOD -> calibrate/variance-stabilize. Source-reported. NEW. literature_map P14Z-T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-052 | 2303.12748
- arXiv/DOI: arXiv:2303.12748
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Enabling Calibration In The Zero-Shot Inference of Large VLMs
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T6
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T6] KEY: one temperature per backbone generalizes across dataset AND prompt
- Takeaway for TRINETRA: ZS CLIP miscalibrated; src-reported single-temperature transfers. Cheap transferable calibration before fusion. Source-reported. NEW. literature_map P14Z-T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-053 | 2512.12997
- arXiv/DOI: arXiv:2512.12997
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Calibrating Uncertainty for Zero-Shot Adversarial CLIP
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: n/r
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T6/T7] perturbation suppresses uncertainty -> over-confidence; Dirichlet restores
- Takeaway for TRINETRA: src-reported improves calibration + keeps robustness. Use calibrated uncertainty not raw softmax. Source-reported. NEW. literature_map P14Z-T6.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-054 | 2404.03539
- arXiv/DOI: arXiv:2404.03539
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Is CLIP the Main Roadblock for Fine-Grained Open-World Perception?
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4-ZS | phase: P14Z-T7
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P14Z-T7] poor attribute separability; cosine matching discards fine-grained info
- Takeaway for TRINETRA: latent re-projection helps; src-reported. Explains smoke-vs-steam/cloud/dust confusion -> coarse complement + re-projection head. Source-reported. NEW. literature_map P14Z-T7.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-055 | 2208.13422
- arXiv/DOI: arXiv:2208.13422
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Light-YOLOv5 for Fire Detection
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P17-T1
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P17-T1] SepViT C3 + Light-BiFPN + GAM; +3.3% mAP, -27.1% params, 91.1 FPS
- Takeaway for TRINETRA: FEATURES F-11 alt; src-reported single-dataset. RISK micro-arch gains shrink cross-camera. Source-reported. NEW. P17_scout_notes T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-056 | 2502.20979
- arXiv/DOI: arXiv:2502.20979
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Real-Time Aerial Fire Detection via Knowledge Distillation (MobileViT-S)
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P17-T1
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P17-T1] distill teacher->MobileViT-S; +0.44-2.00% at compact size, top throughput
- Takeaway for TRINETRA: FEATURES F-19 Wave-2; src-reported. RISK distillation overfits teacher dataset bias. Source-reported. NEW. P17_scout_notes T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-057 | 2508.16739
- arXiv/DOI: arXiv:2508.16739
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Two-Stage UAV Adaptive Compression + Fire Source Detection
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P17-T1
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P17-T1] policy net discards clips + improved YOLOv8; large compute cut
- Takeaway for TRINETRA: FEATURES F-26 Wave-3; src-reported. RISK policy-net/RL training cost + orchestration. Source-reported. NEW. P17_scout_notes T1.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-058 | 2011.04863
- arXiv/DOI: arXiv:2011.04863
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: STCNet: Spatio-Temporal Cross Network for Smoke Detection
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P17-T2
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P17-T2] dual spatial+temporal cross-guided pyramids; +6.2% on RISE smoke
- Takeaway for TRINETRA: FEATURES F-18 Wave-2; src-reported. RISK two-stream latency; temporal cue codec-sensitive. Source-reported. NEW. P17_scout_notes T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-059 | 2212.14143
- arXiv/DOI: arXiv:2212.14143
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: SmokeyNet: Multimodal Camera + Weather Smoke Detection
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P17-T2
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P17-T2] spatio-temporal CNN fusing images + weather; better time-to-detection
- Takeaway for TRINETRA: FEATURES F-23 Wave-3; src-reported. Only pays off where weather feed exists. Source-reported. NEW. P17_scout_notes T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-060 | 1909.12937
- arXiv/DOI: arXiv:1909.12937
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Unsupervised Fire/Smoke Segmentation from IR Video via Optical Flow
- Year / Venue: 2019 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P17-T2
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P17-T2] optical flow + divergence + intensity, MRF/MAP; 95.39% frame, no labels
- Takeaway for TRINETRA: FEATURES F-16 Wave-1; src-reported classical CV. RISK framerate/codec/PTZ-sensitive. Source-reported. NEW. P17_scout_notes T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-061 | 2307.04223
- arXiv/DOI: arXiv:2307.04223
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Thermal and IR Imaging Fusion for Human Detection in Smoke
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P17-T2
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P17-T2] multi-cam thermal/IR calib + lightweight DNN; mAP@0.5 95% Jetson Nano
- Takeaway for TRINETRA: FEATURES F-25 Wave-3; src-reported. Needs IR hardware + calib rig vs INR 2000 cap. Source-reported. NEW. P17_scout_notes T2.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-062 | 2311.05168
- arXiv/DOI: arXiv:2311.05168
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FireMatch: Semi-Supervised Consistency Regularization for Video Fire
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P17-T3
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P17-T3] pseudo-labels + adversarial alignment + fairness loss; 76.92%/91.81%
- Takeaway for TRINETRA: FEATURES F-21 Wave-2; src-reported. RISK pseudo-label confirmation bias on new cameras. Source-reported. NEW. P17_scout_notes T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-063 | 2405.14506
- arXiv/DOI: arXiv:2405.14506
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: SIAVC: Semi-Supervised Industrial Accident Video Classification
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P17-T3
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P17-T3] Super-Augmentation Block + video cross-set aug; 88.76%/89.13%
- Takeaway for TRINETRA: FEATURES F-21 Wave-2; releases ECA9 dataset; src-reported. RISK pseudo-label bias. Source-reported. NEW. P17_scout_notes T3.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-064 | 2607.03131
- arXiv/DOI: arXiv:2607.03131
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Multi-Task Surveillance with Temporal Event Validation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P17-T5
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P17-T5] multi-frame confirmation + confidence-weighted voting + cascade; FA 52% to 4%, <100ms/frame
- Takeaway for TRINETRA: FEATURES F-12 Wave-1; src-reported very low cost post-processor. High-value false-alarm/fatigue mitigation. Source-reported. NEW. P17_scout_notes T5.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-065 | 2503.07371
- arXiv/DOI: arXiv:2503.07371
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: HGO-YOLO: Anomaly Behavior Detection with Hierarchical Features and Lightweight Detection
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P18-A
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P18-A] GhostHGNetv2 + OptiConvDetect shared head; 87.4% mAP@0.5, 56 FPS CPU, 4.6 MB
- Takeaway for TRINETRA: F-11 spec; src-reported +3.0% mAP/-51.7% FLOPs vs YOLOv8n. RISK smoke 1 of 3 mixed classes, may not transfer to smoke-only CCTV. Source-reported. NEW. P18 lit map A.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-066 | 2512.24622
- arXiv/DOI: arXiv:2512.24622
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FireRescue: UAV Dataset and Enhanced YOLO (FRS-YOLO)
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P18-A
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P18-A] cross-dimensional attention + dynamic foreground sampler for smoke occlusion
- Takeaway for TRINETRA: F-11 spec; 8-class rescue set; src-reported qualitative gain. RISK UAV viewpoint != fixed CCTV. Source-reported. NEW. P18 lit map A.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-067 | 2506.09300
- arXiv/DOI: arXiv:2506.09300
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Efficient Edge Deployment of Quantized YOLOv4-Tiny on Raspberry Pi 5
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P18-A
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P18-A] TFLite INT8 PTQ; 28.2 ms/image, 13.85 W on Pi5
- Takeaway for TRINETRA: F-11 spec quantization recipe; src-reported. RISK PTQ hurts diffuse smoke recall; emergency-vehicle classes not flame/smoke. Source-reported. NEW. P18 lit map A.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-068 | 2401.08105
- arXiv/DOI: arXiv:2401.08105
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Hardware Acceleration for Real-Time Wildfire Detection Onboard Drone Networks
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P18-A
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P18-A] QAT+AMP+TensorRT on Jetson Nano; 13% faster, within 1.225% accuracy
- Takeaway for TRINETRA: F-11 spec keep-accuracy-while-quantizing path; FLAME dataset; src-reported. RISK benign prescribed-burn domain. Source-reported. NEW. P18 lit map A.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-069 | 2501.08639
- arXiv/DOI: arXiv:2501.08639
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Detecting Wildfire Flame and Smoke through Edge Computing using Transfer-Learning-Enhanced Models
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P18-A | re-cited 2x
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P18-A] NEGATIVE: cascaded TL no notable gain; TL did NOT improve edge-compute metrics; YOLOv5n ~2x YOLO11n
- Takeaway for TRINETRA: F-11 spec pitfall; 79.2% mAP@0.5; src-reported. KEY: accuracy tricks may fail the edge-latency objective. Source-reported. NEW. P18 lit map A.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-070 | 2010.07110
- arXiv/DOI: arXiv:2010.07110
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Online Anomaly Detection in Surveillance Videos with Asymptotic Bounds on False Alarm Rate
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P18-B
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P18-B] deep + sequential statistical module; threshold selection for a target FAR, truly online
- Takeaway for TRINETRA: F-12 spec FAR-driven threshold recipe; src-reported beats SOTA. RISK FAR guarantee assumes stationary nominal -> breaks under shift. Source-reported. NEW. P18 lit map B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-CCTV-071 | 2503.09960
- arXiv/DOI: arXiv:2503.09960
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Optimizing Fire Safety: Reducing False Alarms Using Advanced ML
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: WS4 | phase: P18-B
- Uses (workstream/chapter): WS4 (ch 09), ch 05 fire_cnn, edge features
- Core method: [P18-B] density-aware weighted ensemble (KNN high-density / XGBoost low-density) + SMOTE
- Takeaway for TRINETRA: F-12 spec density-weighted voting; src-reported comparative. RISK tabular sensor data not video; SMOTE inflates gains. Source-reported. NEW. P18 lit map B.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass


---

## Theme: Datasets / EO / remote-sensing / InSAR / encoders  (`REF-DATA-*`, 84 entries)

_Primary consumer: ch 04 datasets, WS1b (ch 06), ch 05 encoders. The ledger axis/WS code that mapped each paper into this theme is printed per entry for traceability._

#### REF-DATA-001 | 2606.16795
- arXiv/DOI: arXiv:2606.16795
- Authors: Popescu; Biggs; Zhu; Anantrasirichai
- Title: WaveDINO: Learning-Based Atmospheric Correction of Unwrapped InSAR Interferograms Validated by GNSS
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: ABS | local note: yes | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: DL atmospheric correction beats weather models
- Takeaway for TRINETRA: InSAR deformation is corrupted by atmospheric phase delay, seasonal change, decorrelation; numerical-weather-model corrections leave residual bias.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-002 | 1905.07286
- arXiv/DOI: arXiv:1905.07286
- Authors: Anantrasirichai; Biggs; Albino; Bull
- Title: A deep learning approach to detecting volcano deformation from satellite imagery using synthetic datasets
- Year / Venue: 2019 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: synthetic-data training for rare deformation
- Takeaway for TRINETRA: Only a tiny fraction of targets deform and atmospheric noise is ubiquitous -> extreme class imbalance for InSAR deformation detection; trains AlexNet on SYNTHETIC interferograms (analytic deformation + stratified + turbulent atmospheric noi...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-003 | 2609.37038
- arXiv/DOI: arXiv:2609.37038
- Authors: Xu; Guo; Zhang; Zhong; Wang; Long
- Title: NowcastDiT: Diffusion Transformers are Effective Precipitation Nowcasters
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: standard DiT + RL rewards SOTA precip nowcasting
- Takeaway for TRINETRA: A STANDARD Diffusion Transformer is a simple scalable foundation for precipitation nowcasting; NowcastDiT adds a dynamics-aware noise prior (temporal coherence) + end-to-end RL with timestep-aware rewards for meteorological skill; SOTA on S...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-004 | 2402.04290
- arXiv/DOI: arXiv:2402.04290
- Authors: Gong; Bai; Ye; Xu; Liu; Dai; Yang; Ouyang
- Title: CasCast: Skillful High-resolution Precipitation Nowcasting via Cascaded Modelling
- Year / Venue: 2024 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: cascaded framework for extreme-precip nowcasting
- Takeaway for TRINETRA: CasCast tackles two unsolved nowcasting challenges: (i) multi-scale precipitation-system evolution and (ii) accurate forecasts for EXTREME precipitation, via a cascaded (deterministic + generative) framework on radar data for disaster manag...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-005 | 2509.17942
- arXiv/DOI: arXiv:2509.17942
- Authors: Kraabel; Liu; Bian; Kifer; Shen
- Title: StefaLand: An Efficient Geoscience Foundation Model Improving Dynamic Land-Surface Predictions
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: attribute-based geoscience FM, strong SPATIAL generalization
- Takeaway for TRINETRA: StefaLand = generative spatiotemporal Earth representation model built to SUPPRESS overfitting via cross-domain interactions; location-aware masked autoencoder fusing static + time-series inputs, ATTRIBUTE-based (not image-based) representa...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-006 | 2211.10338
- arXiv/DOI: arXiv:2211.10338
- Authors: Boehm; Leong; Bal Mahesh; Prapas; Nemni; Kalaitzis; Ganju; Ramos-Pollan
- Title: Deep learning based landslide density estimation on SAR data for rapid response
- Year / Venue: 2022 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: SAR+elevation only landslide density, 0.814 AUC rapid
- Takeaway for TRINETRA: Produces landslide DENSITY maps from Sentinel-1 SAR + elevation ONLY (no precipitation/soil-moisture/ancillary) for rapid emergency response after Hurricane Maria (USGS 71,431 landslide heads); 0.814 AUC at 128x128 chip level with just elev...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-007 | 2210.10732
- arXiv/DOI: arXiv:2210.10732
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: OpenEarthMap: A Benchmark Dataset for Global High-Resolution Land Cover Mapping
- Year / Venue: 2022 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: 2.2M segments/97 regions/44 countries, UDA benchmark
- Takeaway for TRINETRA: Global high-res land-cover benchmark: 2.2M segments from 5000 aerial/satellite images, 97 regions / 44 countries / 6 continents, 8-class labels at 0.25-0.5m GSD; models trained on it generalize worldwide; explicitly provides UNSUPERVISED DO...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-008 | 1906.01379
- arXiv/DOI: arXiv:1906.01379
- Authors: Huang; Pan; Lei
- Title: What, Where and How to Transfer in SAR Target Recognition Based on Deep CNNs
- Year / Venue: 2019 / IEEE TGRS 2019 (DOI 10.1109/TGRS.2019.2947634)
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: ImageNet pretraining transfers POORLY to SAR; optical->SAR discrepancy; transitive multi-source DA
- Takeaway for TRINETRA: SAR interpretation lacks labeled data; the prevalent fix (fine-tune an ImageNet-pretrained model) performs POORLY for SAR because of the prominent discrepancy between SAR and optical images; studies what/where/how to transfer, proposes a TR...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-009 | 2509.18176
- arXiv/DOI: arXiv:2509.18176
- Authors: Yao; Azadnejad; Huang; Donohue; Dev
- Title: A Deep Learning Approach for Spatio-Temporal Forecasting of InSAR Ground Deformation in Eastern Ireland
- Year / Venue: 2025 / arXiv (cs.CV; submitted IEEE TGRS)
- Read depth: ABS | local note: yes | ledger axis/WS: A1 | phase: n/r | re-cited 5x
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: CNN-LSTM forecasts InSAR deformation; baselines DEFAULT TO PERSISTENCE; sparse->dense tensor
- Takeaway for TRINETRA: Forecasts future ground deformation from SPARSE InSAR time-series by transforming sparse point measurements into a DENSE spatio-temporal tensor, enabling CV architectures; a hybrid CNN-LSTM learns spatial patterns + temporal dependencies, b...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-010 | 2307.08951
- arXiv/DOI: arXiv:2307.08951
- Authors: Ma; Mei
- Title: Knowledge-infused Deep Learning Enables Interpretable Landslide Forecasting
- Year / Venue: 2023 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: SSL encoder / forecasting head / physics gate
- Takeaway for TRINETRA: Transformer (LFIT) forecasts landslide deformation using prior knowledge + multi-source data; validated on Three Gorges reservoir + Tibetan creep.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-011 | 2001.00769
- arXiv/DOI: arXiv:2001.00769
- Authors: Xu; Gao; Li; Xing
- Title: InSAR Phase Denoising: A Review of Current Technologies and Future Directions
- Year / Venue: 2020 / IEEE GRSM
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: InSAR preprocessing
- Takeaway for TRINETRA: Phase denoising is a mandatory step before deformation/forecasting; four method families. Missing denoising stage is a data-quality risk upstream of the SSL encoder.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-012 | 2510.17014
- arXiv/DOI: arXiv:2510.17014
- Authors: Vanyan; Barseghyan; Tamazyan; Galstyan; Huroyan; Hovakimyan; Khachatrian
- Title: Do Satellite Tasks Need Special Pretraining?
- Year / Venue: 2025 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: SSL encoder benchmark
- Takeaway for TRINETRA: At ViT-B scale, RS-specific foundation models bring NO consistent gain over general-purpose vision encoders on low-res generalization.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-013 | 2507.07527
- arXiv/DOI: arXiv:2507.07527
- Authors: (RS-FM team)
- Title: MAPEX: Modality-Aware Pruning of Experts for Remote Sensing Foundation Models
- Year / Venue: 2025 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: SSL encoder / MoE gating
- Takeaway for TRINETRA: MoE RS foundation model with modality-aware expert routing; prunes experts per task modality. Directly informs TRINETRA's gated meta-fusion (modality-aware gating) + addresses modality mismatch of generic FMs.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-014 | 2505.22535
- arXiv/DOI: arXiv:2505.22535
- Authors: Shams Eddin; Zhang; Kollet; Gall
- Title: RiverMamba: A State Space Model for Global River Discharge and Flood Forecasting
- Year / Venue: 2025 / NeurIPS 2025
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: flood forecasting / lead time
- Takeaway for TRINETRA: Mamba SSM forecasts global river discharge + floods on 0.05deg grid up to 7-day lead, beating AI + physics baselines incl. extreme return periods.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-015 | 2309.06062
- arXiv/DOI: arXiv:2309.06062
- Authors: Chen; Fan
- Title: Selection of contributing factors for predicting landslide susceptibility using ML and DL
- Year / Venue: 2023 / Stoch. Env. Res. Risk Assess.
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: feature selection / anomaly inputs
- Takeaway for TRINETRA: Systematic factor-selection (IGR/RFE/PSO/LASSO/HHO + autoencoder) effect on LS prediction accuracy; no universally best method.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-016 | 2103.10985
- arXiv/DOI: arXiv:2103.10985
- Authors: Fatholahi; He; Wang; Syed; Li
- Title: Monitoring surface deformation over oilfield using MT-InSAR and production well data
- Year / Venue: 2021 / arXiv (eess.IV)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: SBAS InSAR baseline
- Takeaway for TRINETRA: SBAS multi-temporal InSAR resolves ~13.5 mm/yr subsidence, cross-validated vs production data. Methodological reference for TRINETRA's SBAS deformation-velocity estimation + external cross-validation practice.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-017 | 1909.01868
- arXiv/DOI: arXiv:1909.01868
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Deep learning networks for selection of persistent scatterer pixels in MT-InSAR
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: InSAR PS selection
- Takeaway for TRINETRA: CNN-ISS + CLSTM-ISS learn to select PS pixels vs conventional noise/look-angle criteria. A learned front-end for TRINETRA's InSAR pipeline; improves PS density/quality -> better deformation precursors.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-018 | 2310.18653
- arXiv/DOI: arXiv:2310.18653
- Authors: Wang; Hernandez; Albrecht; Zhu
- Title: Feature Guided Masked Autoencoder for Self-supervised Learning in Remote Sensing (FG-MAE)
- Year / Venue: 2023 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: SSL encoder / SAR MAE
- Takeaway for TRINETRA: MAE over-focuses on pixel detail -> weak semantics esp. for noisy SAR; FG-MAE reconstructs HOG(+NDI) instead, big boost for SAR.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-019 | 2303.07035
- arXiv/DOI: arXiv:2303.07035
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FireRisk: A Remote Sensing Dataset for Fire Risk Assessment with SSL Benchmarks
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: SSL hazard benchmark
- Takeaway for TRINETRA: GIS-based hazard models hard to scale across geographies due to data/local-condition variation; SSL on free RS helps.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-020 | 2401.07782
- arXiv/DOI: arXiv:2401.07782
- Authors: Hackstein; Sumbul; Clasen; Demir
- Title: CSMAE: Cross-Sensor Masked Autoencoders for Remote Sensing Image Retrieval
- Year / Venue: 2024 / IEEE TGRS
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: cross-sensor SSL
- Takeaway for TRINETRA: Systematic study of masked image modeling for uni-/cross-modal RS retrieval; derives design guideline. Grounds TRINETRA's cross-sensor (S1/S2) SSL fusion design choices.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-021 | 2608.30392
- arXiv/DOI: arXiv:2608.30392
- Authors: Nedungadi; Xiong; Russwurm; Athanasiadis
- Title: Foundation Models Meet Agriculture: Challenges Beyond Pretraining
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: EO FM modality gap
- Takeaway for TRINETRA: EO foundation models yield 'surprisingly poor' results on specialized downstream tasks: pretraining-deployment modality gap (can't ingest non-imagery) + unstable rankings across settings.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-022 | 2505.16793
- arXiv/DOI: arXiv:2505.16793
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: REOBench: Benchmarking Robustness of Earth Observation Foundation Models
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: EO FM robustness
- Takeaway for TRINETRA: Benchmarks robustness of EO foundation models under corruptions/perturbations. Gives TRINETRA a robustness-eval protocol for its satellite encoder under noise/cloud/sensor degradation (test discipline, Bug #11).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-023 | 2401.04824
- arXiv/DOI: arXiv:2401.04824
- Authors: Fibaek; Camilleri; Luyts; Dionelis; Le Saux
- Title: PhilEO Bench: Evaluating Geo-Spatial Foundation Models
- Year / Venue: 2024 / IGARSS 2024
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: EO FM benchmark
- Takeaway for TRINETRA: Testbed + 400GB Sentinel-2 dataset to evaluate FMs (Prithvi, SatMAE) at multiple n-shots. A concrete few-shot EO-FM benchmark TRINETRA could use to justify (or refute) its encoder choice vs Prithvi/SatMAE (Bug #18 benchmarking).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-024 | 2301.05977
- arXiv/DOI: arXiv:2301.05977
- Authors: Wang; Shi
- Title: Design of GNSS-RTK Landslide Monitoring System Based on Improved Raida Criterion
- Year / Venue: 2023 / arXiv (cs.DC)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: ground IoT deformation node
- Takeaway for TRINETRA: Raspberry-Pi + GNSS-RTK + NB-IoT node; improved-Raida (3-sigma) gross-error rejection + Butterworth low-pass + edge compute -> 10mm real-time deformation.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-025 | 2607.16264
- arXiv/DOI: arXiv:2607.16264
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Towards Open Science: Monitoring Crustal Deformations in North America (GNSS)
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: GNSS network processing
- Takeaway for TRINETRA: Large-scale GNSS time-series processing to detect long-wavelength + subtle strain across a network. Methodology for TRINETRA to exploit regional GNSS networks (not just single stations) for deformation context (satellite/ground fusion).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-026 | 2312.03998
- arXiv/DOI: arXiv:2312.03998
- Authors: Foumani; Tan; Webb; Rezatofighi; Salehi
- Title: Series2Vec: Similarity-based Self-supervised Representation Learning for Time Series Classification
- Year / Venue: 2023 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: SSL time-series encoder
- Takeaway for TRINETRA: TS SSL is fundamentally different from vision/NLP; contrastive positive-sample risk; Series2Vec predicts temporal+spectral similarity, no hand-crafted augmentation, matches supervised w/ limited labels.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-027 | 2201.07006
- arXiv/DOI: arXiv:2201.07006
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Time Series Generation with Masked Autoencoder (ExtraMAE)
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: A2 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: MAE time-series synthesis
- Takeaway for TRINETRA: Masked-autoencoder generates synthetic time series via self-supervision. Relevant to TRINETRA both as SSL-encoder validation and as a data-augmentation route for rare-hazard sequences (ties #9 imbalance + SSL design).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-028 | 2511.04362
- arXiv/DOI: arXiv:2511.04362
- Authors: Telli; Antropov; Lonnqvist; Lavalle
- Title: High-Resolution Forest Mapping from L-Band Interferometric SAR Time Series using Deep Learning
- Year / Venue: 2025 / arXiv (eess.SP)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: InSAR coherence features
- Takeaway for TRINETRA: Adding InSAR COHERENCE layers + model-based inverted features beats backscatter-intensity-only; attention/nested UNet beats vanilla+classic ML; L-band guidance for NISAR/ROSE-L.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-029 | 2606.13896
- arXiv/DOI: arXiv:2606.13896
- Authors: Romero; Lv; Karimzadeh
- Title: How do Self-Supervised Remote Sensing Vision Models Transfer to Downstream Tasks?
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A2 | phase: P2
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P2] CR-01 encoder-selection backbone
- Takeaway for TRINETRA: Six GeoFMs across classification/regression/segmentation: rankings FLIP by task type + pretraining objective; mid-layers often transfer best; fine-tune shifts representations (CKA localized to first linear layer of MLP in ViT blocks).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-030 | 2609.39337
- arXiv/DOI: arXiv:2609.39337
- Authors: Major; Razmadze; Shavit
- Title: WinoTS: Wavelet-based Self-Distillation for Time Series Models
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A2 | phase: P3
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P3] SSL CR-01 temporal encoder + WS8 TSAD
- Takeaway for TRINETRA: Invariance-based self-distillation (DINO-style) for time series using WAVELET time-frequency views instead of vision crops (crops distort cycles).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-031 | 2511.20936
- arXiv/DOI: arXiv:2511.20936
- Authors: Salari; Wu; Masood; Guo; Zhang
- Title: Wavelet-Guided Water-Level Estimation for ISAC
- Year / Venue: 2025 / arXiv (eess.SP/stat.ML)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A2 | phase: P3
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P3] low-cost river sensing modality + 3 design rules
- Takeaway for TRINETRA: Passive water-level tracking from LTE downlink power (RSRP/RSSI/RSRQ) on commodity receivers — NO dedicated sensor. Two-ray channel: p0=A+Bcos(kh), p1=-Bkh'sin(kh).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-032 | 2511.05471
- arXiv/DOI: arXiv:2511.05471
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: TUPANN: Transferable & Universal Physics-Aligned Nowcasting Network
- Year / Venue: 2025 / arXiv (cs.LG/cs.CV)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A1 | phase: P3
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P3] precip input layer; physics-decomposition doctrine
- Takeaway for TRINETRA: Satellite-ONLY precip nowcasting (GOES-16 RRQPE train, validated on IMERG) for radar-sparse regions.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-033 | 2604.16265
- arXiv/DOI: arXiv:2604.16265
- Authors: Mundayatt; Sreevalsan-Nair
- Title: FL-MHSM: Spatially-adaptive Fusion & Ensemble Learning for Flood-Landslide Multi-Hazard Susceptibility
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A1 | phase: P3
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P3] multi-hazard MoE gating; OUR region; GMF precedent + CR-02
- Takeaway for TRINETRA: Joint flood+landslide susceptibility, Kerala(India)+Nepal. Two-level spatial partitioning (contextual zones + lattice grid), zone-wise feature selection, 3 fusion designs: probabilistic Early Fusion, tree Late Fusion baseline, soft-gating M...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-034 | 2609.34836
- arXiv/DOI: arXiv:2609.34836
- Authors: Wang; Fang; Jin; Lv; Qin; Zhao; Xiang; Bian; Xiong; Guan; et al.
- Title: MW-Nowcast: Six-Hour Ensemble Nowcasting of Extreme Precipitation
- Year / Venue: 2026 / arXiv (physics.ao-ph/cs.LG)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A1 | phase: P3
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P3] extreme-precip nowcast; cost-loss eval + residual decomposition
- Takeaway for TRINETRA: 6h ensemble radar nowcast: jointly learns DETERMINISTIC predictor for shared organised storm STRUCTURE + GENERATOR (flow-matching) for diverse local RESIDUALS (uncertain growth/decay/reorg/initiation).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-035 | 2606.16795-RESTUDY
- arXiv/DOI: arXiv:2606.16795
- Authors: Popescu; Biggs; Zhu; Anantrasirichai
- Title: WaveDINO (BASELINE RE-STUDY ABS->FT-PARTIAL per OQ-02; original ABS row above UNCHANGED)
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A1 | phase: n/r
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P3-RESTUDY baseline, NON-QUOTA] DL InSAR atmospheric correction
- Takeaway for TRINETRA: Re-studied 2026-10-07 to Tier-2+ depth (NOT new quota; quota stays 32). Corrects atmospheric phase in unwrapped InSAR, GNSS-validated (Laguna del Maule + Campi Flegrei).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-036 | 2005.03221
- arXiv/DOI: arXiv:2005.03221
- Authors: Anantrasirichai; Biggs; Kelevitz; Sadeghi; Wright; Thompson; Achim; Bull
- Title: Deep Learning Framework for Detecting Ground Deformation in the Built Environment using Satellite InSAR data
- Year / Venue: 2020 / arXiv/IEEE-TGRS (cs.CV/stat.CO)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A1 | phase: P3
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P3] FOUNDATIONAL InSAR-DL ancestor of WaveDINO; scarce-label+sparse-noisy tricks
- Takeaway for TRINETRA: Seminal proof-of-concept: adapt pretrained CNN to detect/classify deformation (mining subsidence, dewatering uplift, LANDSLIDES, tunnelling) in national Sentinel-1 velocity fields.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-037 | 2608.11142
- arXiv/DOI: arXiv:2608.11142
- Authors: Gupta; Sobti
- Title: SAR2Agri: Learning SAR Intensity Representations for Agricultural Monitoring
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: FT-PARTIAL | local note: yes | ledger axis/WS: A1 | phase: P3
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P3] WS1/CR-01 encoder: SAR-intensity SSL temporal-pretext recipe + SAR-FM landscape map
- Takeaway for TRINETRA: First SSL pipeline on SAR-INTENSITY ALONE (no optical grounding). Temporal pretext: Time-Difference + Future-Frame prediction + spatial MASKING + curriculum learning (pretrain one task -> joint MTL, eqs 9/10).
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-038 | 2507.15614
- arXiv/DOI: arXiv:2507.15614
- Authors: Holmberg; Pokhrel; Zoch; Ioup; Pathak; et al.
- Title: Accelerating HEC-RAS: A Recurrent Neural Operator for Rapid River Forecasting
- Year / Venue: 2025 / arXiv (cs.LG/cs.AI)
- Read depth: FT | local note: no | ledger axis/WS: A1 | phase: P4
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P4] C-03/WS1: physics-surrogate enables cheap ensemble flood forecasting
- Takeaway for TRINETRA: Deep-learning surrogate treating HEC-RAS as a data-generation engine: hybrid auto-regressive GRU (short-term temporal) + Geometry-Aware Fourier Neural Operator (Geo-FNO; long-range spatial along a reach); 8-channel feature vector (dynamic s...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-039 | 2608.02315
- arXiv/DOI: arXiv:2608.02315
- Authors: Chiriaco; Barco; Bragagnolo; Rossi; Arnaudo
- Title: GEOID-Flood: A Large-Scale Multi-Modal Benchmark Dataset for Flood Segmentation
- Year / Venue: 2026 / arXiv (cs.CV) ECCV 2026 Terrabytes II WS
- Read depth: FT-PARTIAL | local note: no | ledger axis/WS: A1 | phase: P5 | re-cited 2x
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P5] WS1/WS8 FLOOD BENCHMARK + flood-dataset census + leakage warning
- Takeaway for TRINETRA: 14,282 tiles @1024^2, 219 events/65 countries/2016-2026; bi-temporal Sentinel-1 (GRD+RTC VV/VH) + pre-event Sentinel-2 (L2A 12-band) + Copernicus GLO-30 DEM; 3-class bg/permanent-water/flood + cloud+validity masks; EVENT-LEVEL split (70/10/...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-040 | 2604.23066
- arXiv/DOI: arXiv:2604.23066
- Authors: Mukherjee; Friedrich; Tellman; Islam; Zhang; Giezendanner; Lall; Lakshmi
- Title: Urban Flood Observations (UFO): hand-labeled post-flood inundation dataset
- Year / Venue: 2026 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: P5
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P5] WS1/WS4: leave-one-event-out CV + off-the-shelf water products are weak
- Takeaway for TRINETRA: 215 chips (1024^2) from 14 flood events 2017-2021 at 3 m PlanetScope; 2-class inundated/non; LEAVE-ONE-EVENT-OUT CV (leakage-safe), seg IoU 77.3; benchmarks NASA IMPACT S1 model (IoU 44.1) + Google Dynamic World 10 m water (48.1) = off-the-...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-041 | 2512.02055
- arXiv/DOI: arXiv:2512.02055
- Authors: Tulbure; Caineta; Broich; Gaines; Rufin; Thomas; Alemohammad; Hemmerling; Hostert
- Title: Leveraging multimodal geospatial foundation models (TerraMind) for near-real-time global flood mapping
- Year / Venue: 2025 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: P5
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P5] WS1/WS8: GFM is not a free win; tuned U-Net strong cheap baseline
- Takeaway for TRINETRA: FloodsNet = harmonized Sentinel-1(SAR)+Sentinel-2(optical) over 85 flood events worldwide; fine-tunes ESA-IBM TerraMind GFM in 4 configs; BASE-UNFROZEN best accuracy/precision/recall-per-compute; large-unfrozen best recall; U-Net HIGHER REC...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-042 | 2502.19866
- arXiv/DOI: arXiv:2502.19866
- Authors: Liu; Wang; Chen; Du; Li; Wu; Fang
- Title: LMHLD: A Large-scale Multi-source High-resolution Landslide Dataset
- Year / Venue: 2025 / arXiv (cs.CV) Zenodo 10.5281/zenodo.11424988
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: P5 | re-cited 2x
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P5] WS1/WS8: open Himalayan-adjacent (Gorkha) landslide dataset
- Takeaway for TRINETRA: 25,365 patches, 5 satellite sensors, 7 study areas incl. GORKHA Nepal 2015 (Himalayan), Wenchuan, Jiuzhaigou, Taiwan, Hokkaido, Rio, Emilia-Romagna; multi-scale patches; LMHLDpart training module mitigates catastrophic forgetting; 5 quality...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-043 | 2606.16302
- arXiv/DOI: arXiv:2606.16302
- Authors: Banerjee; Daou
- Title: Explainable Flood Segmentation on Sentinel-1 SAR using CNN and Transformer Architectures
- Year / Venue: 2026 / arXiv (cs.CV) v3
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: P5
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P5] WS1: scene-based splits; flooded-vs-permanent-water is the hard part
- Takeaway for TRINETRA: U-Net/U-Net++/DeepLabV3-ResNet34 vs SegFormer b0/b1/b2 on ETCI (NASA) + Sen1Floods11 with SCENE-BASED splits (leakage-aware); SegFormer-b2 > U-Net on ETCI (Wilcoxon across 7 scenes), advantage narrows after fine-tune on Sen1Floods11 and con...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-044 | 2505.17782
- arXiv/DOI: arXiv:2505.17782
- Authors: Papadopoulos; Bountos; Sdraka; Karavias; Camps-Valls; Papoutsis
- Title: Thalia: A Global Multi-Modal Dataset for Volcanic Activity Monitoring
- Year / Venue: 2026 / arXiv (cs.CV) v4
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: P5 | re-cited 2x
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P5] WS1/WS8: open InSAR-deformation benchmark + atmospheric-artifact confound
- Takeaway for TRINETRA: 38 spatiotemporal datacubes over 7 years; InSAR products + topography + ATMOSPHERIC variables (which introduce delays that MIMIC ground deformation - explicit confound) + expert deformation annotations (type/intensity/extent) + descriptive...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-045 | 2605.21527
- arXiv/DOI: arXiv:2605.21527
- Authors: Barzegar; Bolch; Kuehtreiber; Ullo
- Title: CryoNet: Deep Learning for Multi-Modal Debris-Covered Glacier Mapping (Poiqu Basin, Central Himalaya)
- Year / Venue: 2026 / arXiv (eess.IV) submitted JSTARS
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: P5
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P5] WS8: IN-REGION (central-Himalaya) multimodal glacier/glacial-lake mapping
- Takeaway for TRINETRA: Poiqu Basin (CENTRAL HIMALAYA): fuses Sentinel-2 + DEM-topo + spectral indices + PCA + InSAR coherence/phase + tasseled-cap + GLCM texture; encoder-decoder CNN (ResNet101 + spatial-channel SE); discriminates clean-ice / debris-covered glaci...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-046 | 2606.07374
- arXiv/DOI: arXiv:2606.07374
- Authors: Sica; Pulella; Schmitt
- Title: Beyond Backscatter: InSAR coherence from detected SAR images
- Year / Venue: 2026 / arXiv (eess.SP)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: P5
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P5] WS1/WS8: CHEAP coherence feature from GEE-available GRD (no SLC/coregistration)
- Takeaway for TRINETRA: Residual U-Net regresses InSAR COHERENCE directly from DETECTED (GRD) SAR magnitude without accurate coregistration; trained on 12-day Sentinel-1 SLC-derived coherence; generalizes across diverse locations AND unseen temporal baselines; ope...
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-047 | 2610.11236
- arXiv/DOI: arXiv:2610.11236
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Low-Cost Sensor Calibration for Indoor Air Quality: Dataset + Lightweight Model
- Year / Venue: 2026 / arXiv (cs.LG)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: P6 | re-cited 2x
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P6] calibration: eval framework (drift/transfer/event)
- Takeaway for TRINETRA: 6-month multivariate indoor AQ dataset (low-cost + reference, 5 locations, metadata) + 4 eval scenarios: reference-efficient, location-transfer, long-term drift, event-conditioned; lightweight temporal model low edge-cost.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-048 | 2208.00210
- arXiv/DOI: arXiv:2208.00210
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Multiple Categories of Visual Smoke Detection Database
- Year / Venue: 2022 / arXiv (cs.CV)
- Read depth: ABS | local note: no | ledger axis/WS: A1 | phase: P6
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P6] dataset: multi-class smoke types (nuisance vs danger)
- Takeaway for TRINETRA: 70,196-image smoke dataset distinguishing smoke TYPES (complete combustion / incomplete combustion / direct emission) for industrial settings; authors report current algorithms underperform.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-049 | 2311.10116
- arXiv/DOI: arXiv:2311.10116
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: SKLFS-WildFire smoke detection test set
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: SKLFS-WildFire (D114)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-050 | 2606.10174
- arXiv/DOI: arXiv:2606.10174
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: GWFP Global Wildfire Prevention dataset
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: GWFP images+video (D115)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-051 | 2604.23542
- arXiv/DOI: arXiv:2604.23542
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: MultiNatSmoke + AusSmoke segmentation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: AusSmoke/MultiNatSmoke (D116)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-052 | 2505.17395
- arXiv/DOI: arXiv:2505.17395
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: The Wildfire Dataset classification
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: Wildfire Dataset 10.74GB (D118)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-053 | 2310.01711
- arXiv/DOI: arXiv:2310.01711
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Satellite smoke scene classification (USTC_SmokeRS/Landsat_Smk)
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: USTC_SmokeRS, Landsat_Smk (D122-123)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-054 | 2503.08580
- arXiv/DOI: arXiv:2503.08580
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Next-day fire from MODIS/VIIRS fire masks
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: MOD14/VNP14 (D125)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-055 | 2401.11519
- arXiv/DOI: arXiv:2401.11519
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: CaBuAr California Burned Areas
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: CaBuAr Sentinel-2 (D126)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-056 | 2307.04916
- arXiv/DOI: arXiv:2307.04916
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: MultiEarth Amazon deforestation/burned-area
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: MultiEarth multimodal (D127)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-057 | 2308.02508
- arXiv/DOI: arXiv:2308.02508
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Wildfire ID from EFFIS hotspots
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: EFFIS hotspot crossref (D128)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-058 | 2601.00123
- arXiv/DOI: arXiv:2601.00123
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: C2S-MS Floods SAR+multispectral
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: C2S-MS Floods (D131)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-059 | 2306.00704
- arXiv/DOI: arXiv:2306.00704
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: S1GFloods global flood detection
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: S1GFloods 46 events (D133)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-060 | 2311.12056
- arXiv/DOI: arXiv:2311.12056
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Kuro Siwo rapid flood mapping
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: Kuro Siwo 43 events (D134)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-061 | 2311.09276
- arXiv/DOI: arXiv:2311.09276
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Citizen-Science Flood Extent SAR
- Year / Venue: 2023 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: Citizen-Science Flood ~36k km2 (D135)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-062 | 2403.10127
- arXiv/DOI: arXiv:2403.10127
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Landslide mapping (Landslide4Sense/Bijie)
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: Landslide4Sense, Bijie (D137-138)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-063 | 2608.09325
- arXiv/DOI: arXiv:2608.09325
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PILD event-isolated landslide
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: PILD 55 events (D139)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-064 | 2602.08112
- arXiv/DOI: arXiv:2602.08112
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: MMLSv2 Martian landslide segmentation
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: MMLSv2 (D140, MARTIAN out-of-scope)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-065 | 2204.09435
- arXiv/DOI: arXiv:2204.09435
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Hephaestus InSAR dataset
- Year / Venue: 2022 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: Hephaestus 19919 ifg (D141)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-066 | 2002.12898
- arXiv/DOI: arXiv:2002.12898
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: PM2.5-GNN (KnowAir)
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: KnowAir PM2.5 (D143)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-067 | 2103.06520
- arXiv/DOI: arXiv:2103.06520
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: TAP Tracking Air Pollution China
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: TAP PM2.5 1-10km daily (D144)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-068 | 2412.13935
- arXiv/DOI: arXiv:2412.13935
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Bihar low-cost PM2.5 sensor network
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: Bihar 511-loc sensors India (D145)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-069 | 2502.11500
- arXiv/DOI: arXiv:2502.11500
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: CEED California Earthquake Event Dataset
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: CEED waveforms+picks (D147)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-070 | 2408.06629
- arXiv/DOI: arXiv:2408.06629
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Earthquake phase picking (STEAD)
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: STEAD waveforms (D148)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-071 | 2601.02264
- arXiv/DOI: arXiv:2601.02264
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: POSEIDON global EQ catalog
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: POSEIDON 2.8M events (D149)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-072 | 2605.26320
- arXiv/DOI: arXiv:2605.26320
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: MultiSeismo multimodal seismic
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: MultiSeismo 16k+ events (D150)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-073 | 2004.06774
- arXiv/DOI: arXiv:2004.06774
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: CrisisBench crisis tweet benchmark
- Year / Venue: 2020 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: CrisisBench/CrisisNLP (D151)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-074 | 1805.00713
- arXiv/DOI: arXiv:1805.00713
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: CrisisMMD multimodal disaster tweets
- Year / Venue: 2018 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: CrisisMMD text+images (D152)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-075 | 2108.12828
- arXiv/DOI: arXiv:2108.12828
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: MEDIC disaster image classification
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: MEDIC 71198 images (D153)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-076 | 2410.08814
- arXiv/DOI: arXiv:2410.08814
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: TSEqD Turkey-Syria Earthquake Dataset
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: TSEqD 10352 samples (D156)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-077 | 2601.13839
- arXiv/DOI: arXiv:2601.13839
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DisasterVQA visual QA
- Year / Venue: 2026 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: DisasterVQA 1395 img (D157)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-078 | 1910.08854
- arXiv/DOI: arXiv:1910.08854
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DFDC Deepfake Detection Challenge Dataset
- Year / Venue: 2019 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: DFDC (D158, EULA-restricted)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-079 | 2107.02045
- arXiv/DOI: arXiv:2107.02045
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Deepfake detection w/ FaceForensics++
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: FaceForensics++ (D159, EULA)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-080 | 2108.05080
- arXiv/DOI: arXiv:2108.05080
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: FakeAVCeleb audio-video deepfake
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: FakeAVCeleb (D160, restricted)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-081 | 2108.07949
- arXiv/DOI: arXiv:2108.07949
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: DeepFake MNIST+ facial animation
- Year / Venue: 2021 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: DeepFake MNIST+ 10k vids (D161)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-082 | 2406.02438
- arXiv/DOI: arXiv:2406.02438
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: CtrSVDD singing-voice deepfake
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: CtrSVDD audio (D162)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-083 | 2406.08112
- arXiv/DOI: arXiv:2406.08112
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: Codecfake codec deepfake audio
- Year / Venue: 2024 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: Codecfake (D163)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass

#### REF-DATA-084 | 2509.04345
- arXiv/DOI: arXiv:2509.04345
- Authors: (authors as recorded in ledger; full list not re-verified)
- Title: AUDETER open-world deepfake audio
- Year / Venue: 2025 / arXiv
- Read depth: ABS | local note: no | ledger axis/WS: DATASET | phase: P23
- Uses (workstream/chapter): ch 04 datasets, WS1b (ch 06), ch 05 encoders
- Core method: [P23] dataset source: AUDETER 4500h (D164)
- Takeaway for TRINETRA: Source-reported. NEW. P23 dataset hunt.
- Verification status: resolved on 2026-10-10? -- not re-fetched this pass
