# PHASE BACKLOG — deferred items parked for their proper phase
# (MASTER_PROMPT §0.10). Items discovered early but belonging to a later phase.

## For P2/P3 (SOTA + deep literature)
- Promote the 235 ABS notes to Tier-2+ full-text where load-bearing (OQ-02).
- Backfill ~45 `authors="(authors)"` placeholder rows at FT promotion.
- Re-run 10% identity audit every ~50 new papers.
- Build the full reading queue priority scores (10_reading_queue.csv) as discovery resumes.

## For P5 (dataset registry)
- Verify COST/license/Kaggle-availability for: Sentinel-1/-2 (Copernicus), GPM IMERG, SMAP,
  ERA5-Land, MODIS, ITS_LIVE, HMAGLOFDB, CAMELS-hourly, HKO-7, MillionAID, FireRisk,
  landslide inventories (NASA COOLR/GLC), Bhuvan/NRSC products. Flag registration-gated
  ones in LEAD_TIME_ITEMS.md.

## For P6 (IoT BOM / safety)
- Hard-verify every ₹ figure vs ≥2 live Indian listings (OQ-05); recompute ≤₹2000/node
  incl. GST + shipping + ~10% contingency.
- LoRa band: confirm IN865–867 MHz (NOT 433) per Indian regulation (system-model #6).

## For P7 (physics on paper)
- Verify 3 I–D constants (Caine 14.82·D⁻⁰·³⁹; Dahal–Hasegawa 73.9·D⁻⁰·⁷⁹;
  Garhwal 1.82·D⁻⁰·²³) — Bug #15; label CLASS A/B/C.
- Re-derive Iverson ψ(Z,t): slope enters only via D1=D0/cos²δ (confirm Bug #3 spurious
  cos²β/cosβ). Lu&Likos sign σ_s=−S_e·ψ (Bug #2). Fukuzono/Voight α≈2 (Bug #4).
  Bayes threshold p*=C_FA/(C_FA+C_miss)=0.0476 (Bug #1).

## For P9/P10 (anomaly)
- Deep SVDD collapse-prevention (2510.09452); forecast-residual + isolation forest + XGBoost
  ensemble scope; conformal under autocorrelation/missingness (HopCPT, 2406.05405).

## For later phases
- 2608.12422 reality-check: ALL performance claims must be re-stated under tile-withheld
  spatial-CV vs gradient-boosted / 3-rule-decision-tree + persistence baselines.

## For P14Z (zero-shot & open-vocabulary classification — ADDED, D-011, mandatory)
- Park here any zero-shot / open-vocab / VLM-CLIP / RS-foundation-model-zero-shot / zero-shot-
  anomaly / cross-region-transfer papers encountered in earlier phases (do NOT read them for
  quota in P1–P14; note the ID + one line + "→P14Z" so they're ready).
- Core sub-threads to cover (≥10 NEW core reads): (a) VLM/CLIP open-vocab image classification;
  (b) RS-FM zero-shot scene/condition tagging (RemoteCLIP/GeoRSCLIP/SkyCLIP-type); (c) zero-shot
  anomaly detection (WinCLIP/AnomalyCLIP-type); (d) zero-shot cross-region/cross-hazard transfer.
- Design questions to answer in P14Z: calibration of zero-shot confidences; hallucinated-label
  risk; how zero-shot tags enter GMF + per-zone conformal + monotone shield as LOW-TRUST advisory
  signals (Rule 19 — never an autonomous alarm trigger); failure modes (novel-but-benign scenes,
  adversarial/odd imagery, night/cloud/sensor-domain shift); which free EO-VLM checkpoints exist
  and run under the Kaggle budget.
- Candidate IDs seen so far (unverified, to novelty-check in P14Z): none logged yet — add as found.
  - TiRex (time-series foundation model) — applied ZERO-SHOT in TREA-Net (2607.26854) and was the
    STRONGEST baseline; TREA-Net+TiRex best overall. → study TiRex zero-shot forecasting for P14Z;
    lesson already captured: zero-shot FM strong as a PRIOR, best with lightweight local residual
    correction (don't use zero-shot output raw).
  - OmniRSCLIP (2609.03391, v2 2026) — multi-source RS CLIP (RGB/SAR/MSI/HSI) via Spectral-Spatial
    Basis Decomposition (arbitrary-channel adaptation without breaking pretrained CLIP prior) + OmniRS5M
    image-text corpus; zero-shot classification + retrieval + semantic localization. → KEY P14Z read:
    shows how to extend CLIP open-vocab zero-shot to SAR/multispectral EO sensors (our Sentinel-1/-2);
    directly the "RS-FM zero-shot scene/condition tagging" sub-thread. Novelty-check + full read in P14Z.
  - RS scene-classification survey (JKSU 2026, Huang & Hu) — identifies gaps: hyperspectral/multitemporal,
    cross-domain generalization, standardized eval. → context read for P14Z SOTA scan.

## For P7 (EO-FM encoder trade study — CR-01) — parked SAR foundation models
From SAR2Agri 2608.11142 landscape map + query 217 (novelty-check + evaluate in P7):
- Multimodal SAR+optical: TerraMind, Copernicus-FM (2503.11849, already a candidate), AnySat (2412.14123).
- SAR-specific SSL: SAR-JEPA, SARMAE, SAR-W-MixMAE (focus flood-mapping/target-detection/landcover —
  flood-mapping pretraining is CLOSER to our hazard task than agri).
- SAMBA 2606.31668 — Scatter-guided Masked Bidirectional MAMBA for SAR ATR; linear-cost alternative to
  quadratic transformers → relevant to ₹2000 edge-node compute budget.
- OceanSAR-1 (galeio-research, weights released) — SAR ocean FM; recipe reference.
- SAR2Agri recipe itself: temporal pretext (Time-Difference + Future-Frame) + masking + curriculum — a
  candidate SSL objective for our InSAR deformation encoder (recast for interferometric phase).
