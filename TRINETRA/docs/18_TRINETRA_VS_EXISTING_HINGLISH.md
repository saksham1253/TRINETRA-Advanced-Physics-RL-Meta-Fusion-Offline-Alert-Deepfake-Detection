# 18 — TRINETRA vs TYPICAL APPROACHES: humara system alag aur mazboot kyun hai (honest, claim ladder)

**Claim ladder:** C0 not addressed · C1 design only · C2 implemented, untested · **C3 implemented AND measured by us** (result cited) ·
C4 matches/exceeds a published result on a matched protocol. **We have NO C4 claim yet**, so "best / first / SOTA" words are not used.
Our strongest points are the C3 ones, measured on REAL data in this hackathon.

## A. Sabse strong points (pehle ye bolo)
1. **Physics works on real Indian data, with zero training. [C3]** On 184 real landslide events (NASA catalog, Uttarakhand + Himachal)
   + 552 control days, the Caine rainfall-threshold physics reaches **ROC-AUC 0.758** with NO fitting, close to a trained rain model (0.781).
   (`results/RESULTS.md`, `geo_physics_s0`.) Hinglish: jahan training labels hi nahi hain (zyada tar Indian districts), wahan bhi physics turant kaam karta hai.
2. **We report when our own idea does NOT help. [C3]** On a small subset (Chamoli tile, 28 events) physics beat rain by +0.095 AUC
   (CI 0.052 to 0.144, `results/geo_small`). On 6.5x more data (`results/geo_large`) the gain vanished (CI includes 0), and we say so (P8).
3. **Learned AI is not deployed unless it provably beats the rule. [C3]** The RL gate compares against the rule baseline with a paired 95%
   bound. It refused deployment on random data (bug B-02 fixed) and in every simulator setting run so far (`results/rl_env`). Typical approach: "RL agent" shown without
   any baseline test (P11).
4. **Physics found a real flaw and we fixed it. [C3]** Assumed soil gave FS < 1 even on dry Himalayan slopes, which would mean a permanent
   alarm (P1). With back-analysis plus the cohesion-free ΔFS signal, the repo geo gate scores ROC-AUC 0.712 (large set) and 0.762
   (small set) on real events (`results/geo_*`).
5. **Leakage-safe evaluation by construction. [C3 geo / C2 vision]** Spatial-block CV on real geo data; group splits, perceptual-hash dedupe,
   augmented-copy grouping and cross-dataset dedupe for images (6 data bugs caught before training, docs/BUG_STATUS B-17..B-22) (P8).

## B. Pattern-by-pattern
| Typical approach (category) | TRINETRA approach | Ladder | Evidence |
|---|---|---|---|
| Single detector + fixed threshold (P1, P3) | multi-evidence: CNN + zero-shot + colour baseline + physics, temporal validator, confuser stress sets | C2 | code + smoke test; real Kaggle runs pending |
| Scores taken at face value (P5) | cross-fitted temperature calibration, ECE reported, U* conflict → "uncertain, human review" | C3 geo (ECE on real events) / C2 vision | `oof_utils.py`, `decision.py` |
| Fixed cut-off (P1) | cost-loss threshold p* = C_FA/(C_FA+C_miss); the value of warning tested vs the cost ratio | C3 (simulator) | `rl_env_cmiss*` reports |
| Black-box model (P4) | Class A/B/C physics with validity regimes; Class C OFF by default | C2 | `configs/*.json`, docs/04 |
| Inflated evaluation (P8) | group/spatial CV, held-out datasets, multi-seed, admission gate (must beat baselines with CI) | C3 | `admit_model`, hindcast CI |
| Media taken at face value (P7) | deepfake score lowers media trust r' = r(1-p_fake); fake-video attack simulated in fusion | C2 | `build_fusion_cache.py --fake-frac` |
| Cloud-only alerts (P6) | CAP builder, DTN store-and-forward, siren, numpy-only core runs offline | C2 (unit-tested) | `ws3_alert/`, 128 tests |
| Autonomous public alerts (P12) | CAP refuses without an `APPROVED:` token; shield can only RAISE | C2 (unit-tested) | `cap.py`, `shield.py` |
| Unvalidated RL (P11) | physics simulator with real rain + online truth + OPE + paired CI gate | C3 (simulator) | `env_landslide.py` |
| Static model (P13) | PSI/CUSUM drift monitor voids conformal guarantees | C2 | `drift_monitor.py` |
| Raw video egress (P14) | no-raw-video-egress guard | C2 | `common/security.py` |
| Fire-only (P2/P4) | same pipeline covers landslide, GLOF relations, Sentinel-1/2, InSAR heads | C3 geo / C2 EO | docs/09e |

## C. What we do NOT claim (bolna zaroori hai)
- No C4: no comparison with a published benchmark on a matched protocol yet.
- Vision numbers are pending Kaggle runs. Simulator results are not field results. Small-data and older-data caveats apply.
- TRINETRA complements certified alarms and official IMD/NDMA warnings; humans approve every public alert.

## D. Judges ke saamne 60 second: "hum alag kyun hain"
1. **Physics pehle, AI baad me.** Bina training ke physics ne 184 real Indian landslides par ROC-AUC 0.758 diya [C3]. Jahan labels nahi, wahan bhi kaam.
2. **Hum apni haar bhi dikhate hain.** Chhote tile par physics jeeta (+0.095), bade data par nahi — hum ye khud batate hain.
3. **AI tabhi deploy jab rule ko saabit roop se harata hai.** RL ko C_miss = 100, 1000, 5000 teeno par test kiya; physics rule oracle ke barabar raha (−200.0 vs −200.0, −478.1 vs −478.5), CQL kabhi gate pass nahi kiya → deploy nahi [C3, simulator].
4. **Trained physics model bhi honest gate se guzarta hai.** Geo-PINN AUC 0.716, simple baselines se kam → admitted = false.
5. **Ek hi pipeline, kai hazards.** Fire, landslide, GLOF relations, Sentinel-1/2, InSAR — same calibration, fusion, human-approval rule.
6. **Insaan final decision leta hai.** CAP alert bina `APPROVED:` token ke bante hi nahi; shield sirf level badha sakta hai.

Ek line: *"TRINETRA har number ka source dikhata hai, apni kamzori batata hai, aur insaan ko control me rakhta hai."*
<!-- END -->
