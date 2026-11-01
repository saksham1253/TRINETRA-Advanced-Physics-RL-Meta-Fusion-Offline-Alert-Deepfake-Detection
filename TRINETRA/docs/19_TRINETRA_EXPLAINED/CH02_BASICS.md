# CH02 — BASICS FROM ZERO

| Concept | Simple me samjho | Tiny example |
|---|---|---|
| Score vs probability | score sirf "kitna lagta hai"; probability "100 me se kitni baar sach" | score 8/10 ≠ 80% |
| Threshold | doorbell ki sensitivity | p ≥ 0.048 → alarm (p*) |
| False alarm / miss | bina wajah ghanti / chor aaya par ghanti nahi | C_FA = 5, C_miss = 100 |
| Precision, recall | alarm me kitne sach / sach me se kitne pakde | 100 alarms, 20 sach → precision 0.2; 25 sach events me 20 pakde → recall 0.8 |
| ROC-AUC | random positive ka score random negative se upar hone ki probability | 0.5 = coin toss, 1.0 = perfect; physics 0.758 |
| Calibration (ECE) | "70%" bole to 70% baar sach ho | ECE 0.030 = average gap 3 points |
| Overfitting | ratta maarna, samajhna nahi | train 99%, test 60% |
| Train / val / test | padhai / mock test / final exam | final exam alag kitaab se (held-out dataset) |
| Data leakage | exam paper pehle dekh lena | same video ke frames train + test me |
| Group split | ek video, ek jagah, ek event ke saare samples ek hi taraf | 101 spatial blocks in geo CV |
| Seeds | dice dobara phenk ke dekhna ki result luck to nahi | seeds 0, 1, 2 → mean ± sd |
| Baseline | sabse simple tareeka jise harana zaroori | rain-only logistic, colour histogram, rule policy |
| Case-control | har event ke saath "normal din" bhi lo | 184 events + 552 control days |
| Cost-loss | galti ki keemat ke hisaab se threshold | p* = 5/(5 + 100) |

**Numeric precision/recall table (hand-computed):**
| | actual event | no event |
|---|---|---|
| alarm | 20 (TP) | 80 (FP) |
| no alarm | 5 (FN) | 895 (TN) |
Precision = 20/100 = 0.20 · recall = 20/25 = 0.80 · false-alarm rate = 80/975 = 0.082.

**Self-check:** (1) Random split kyun galat hai? (leakage) (2) AUC 0.5 ka matlab? (bekaar) (3) ECE kam achha ya zyada? (kam)
<!-- END -->
