# 02 — PIPELINE FLOWCHARTS (built from code; dashed = PLANNED / not in code)
Legend: solid box = file exists and is tested here; `:::planned` dashed = not in code. Paths are relative to `trinetra/src/trinetra/`.

## (a) End-to-end inference (fire cycle)
```mermaid
flowchart LR
  classDef planned stroke-dasharray: 5 5,stroke:#999,color:#777
  CAM[CCTV frames] --> DET[deep/fire_cnn.py FireSmokeNet]
  DET --> TV[ws4_cctv TemporalValidator]
  CAM -.-> ZS[zero-shot CLIP PLANNED]:::planned
  IOT[IoT smoke/heat nodes ws7_iot] --> ES[edge_screen] --> AN[ws8_anomaly ensemble]
  WX[NASA POWER wind, T] --> FG
  TV --> FG[ws1a_firephys/gate.py fire_gate Byram regime]
  FG --> EX[ExpertOutput p,u,c,r]
  AN --> EX
  DF[deep/deepfake_net trust cap 0.4] --> EX
  ZS -.-> EX
  EX --> FU[ws5_fusion_rl/fusion_models.fuse FM-1 default]
  FU --> DEC[decision.decide level = max of conformal_level, shield]
  SH[shield.py floor] --> DEC
  DEC --> OP[ws3_alert/operator human review]
  OP -->|APPROVED token| CAP[ws3_alert/cap.py CAP 1.2] --> DTN[dtn / siren offline]
```
Hinglish: Camera aur IoT do alag "gawah" (witnesses) hain. Har gawah apni probability `p`, shak `u`, physics se
mel `c` aur bharosa `r` deta hai. Fusion sab ko weight karke ek risk banata hai. Decision function us risk ko
GREEN/YELLOW/ORANGE/RED me badalta hai, aur shield sirf level **badha** sakta hai, ghata nahi. Last me insaan
(operator) approve kare tabhi CAP alert jaata hai. Zero-shot box dashed hai kyunki code me abhi nahi hai.

## (b) Training (per module, Kaggle)
```mermaid
flowchart LR
  RAW[Kaggle dataset attached] --> AD[data_adapters/build_npz.py]
  AD --> CHK[build_npz.py check + subset]
  CHK --> TR[kaggle/train_classifier.py / train_anomaly.py]
  TR --> CV[spatial_cv_indices on block groups]
  CV --> AM[deep/train.py admit_model: beat climatology + logistic, ECE]
  AM --> REP[*_report.json admitted true/false]
  REP --> LOG[docs/14_RESULTS_LOG.md]
```
Hinglish: Pehle data ko code ke format me badlo (adapter). Phir group-wise folds par train karo. `admit_model`
ek "gatekeeper" hai: agar model simple baselines ko CI ke saath nahi harata, to report me `admitted=false`.

## (c) RL loop (offline, one-step)
```mermaid
flowchart LR
  FS[fused features + label] --> LG[data_adapters/make_rl_logs.py eps-rule logging]
  LG --> CQL[kaggle/train_offline_rl.py CQLPolicy HOLD/WATCH/ALARM]
  CQL --> OPE[ws5_fusion_rl/rl.ope_admission WIS + ESS + positivity]
  OPE -->|deploy_learned| POL[learned policy]
  OPE -->|else| RB[RuleBaselinePolicy 0.0476]
  POL --> SHD[shield raises only]
  RB --> SHD
```
Hinglish: RL yahan "online game" nahi khel raha. Ye purane logged decisions se seekhta hai (offline). Agar
OPE gate bole ki naya policy rule-baseline se behtar nahi hai, to rule-baseline hi chalega.

## (d) Meta-fusion data flow
```mermaid
flowchart LR
  E[experts p_i,u_i,c_i,r_i,available] --> W[nf.effective_weight r*c*exp -u/tau]
  W --> FM1[FM-1 weighted mean]
  W -.flag.-> PH[PHARAOH power mean rho=1+kappa*D*S]
  W -.model=GMF.-> GMF[base + bounded residual]
  E --> U[NF-3 U* = sum w u + lambda*D]
  E --> S[NF-4 salience max r*c*p]
  FM1 --> OUT[p, U*, S]
  U --> OUT
  S --> OUT
  OUT --> DEC[decide: level, uncertain if U*>0.6, pred_set]
```

## (e) Kaggle parallel workflow
```mermaid
flowchart TB
  A[Acct A: fire + confusers] --> KD[(private Kaggle Datasets trinetra-*-vK)]
  B[Acct B: IoT + anomaly] --> KD
  C[Acct C: deepfake + fusion cache] --> KD
  D[Acct D: RL logs + OPE + cyclone data prep] --> KD
  KD --> C2[Acct C: fusion head / FM-1 vs PHARAOH]
  C2 --> D2[Acct D: RL on fused cache]
  KD --> RES[docs/14_RESULTS_LOG.md + repo]
```

## (f) DFD Level 0 and Level 1
```mermaid
flowchart LR
  S1[Sensors / CCTV / satellite] -->|readings, frames| P0((TRINETRA))
  P0 -->|advisory level + evidence| OPR[Operator]
  OPR -->|approval| P0
  P0 -->|CAP alert| PUB[Public channels]
```
```mermaid
flowchart LR
  IN[inputs] --> P1((1 perceive: detectors, anomaly))
  P1 --> P2((2 physics check))
  P2 --> P3((3 fuse))
  P3 --> P4((4 decide + shield))
  P4 --> P5((5 human review))
  P5 --> P6((6 alert offline))
  P4 --> D1[(decision log)]
```
<!-- END -->
