"""trinetra.deep — REAL deep-learning models for TRINETRA (train on Kaggle GPU).

These modules import torch and are NOT importable in the base sandbox (torch absent); they are verified by
`py_compile` and executed on Kaggle. The numpy decision/physics/eval core in the rest of the package stays
runnable and is the source of truth for the ADVISORY decision + honesty gates. Deep models only produce
calibrated expert probabilities that feed `trinetra.ws5_fusion_rl.decide` — they NEVER issue alerts
(Rule 19), carry Class A/B/C labels (Rule 20), and may claim performance only after the eval admission
gate passes (Rule 16).

Model inventory (the "6 model cards"):
  1. GeoPINN         (ws1b)  physics-informed slope hydrology -> FS/landslide risk   [Class A/B]
  2. FireSmokeNet    (ws1a/4) spatiotemporal fire/smoke detector + Strouhal aux      [Class A + data]
  3. EODownstream    (ws1b)  frozen EO foundation encoder + hazard head             [Class data]
  4. DeepAnomaly     (ws8)   TCN autoencoder + Deep-SVDD + forecasting residual     [Class data]
  5. AuthenticityNet (ws2)   freq+spatial deepfake detector (LOW trust)             [Class data]
  6. OfflineRLPolicy (ws5)   CQL/IQL/one-step alarm policy (advisory)               [Class advisory]
  + GMFHead          (ws5)   learned gated-mixture fusion head w/ bounded residual  [Class B]
"""
__all__ = []
