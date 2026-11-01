# P03 — Alarm kab bajaana hai? Decision ki "physics" (cost, probability, bharosa)

> **Ek line me:** har alarm ka do tarah ka nuksaan hai: **bekaar alarm** (log pareshaan, agli baar sunenge nahi) aur **chhoota hua khatra**
> (jaan ka nuksaan). Dono ki keemat tolkar ek seedha sa number nikalta hai, **p\* = C_FA / (C_FA + C_miss)**. Agar aag ki probability p\* se
> zyada hai, to alarm bajaana sasta hai. Baaki sab (calibration, base rate, fusion, shield) isi ek decision ko sahi banane ke liye hai.

Code: `ws5_fusion_rl/decision.py`, `fusion_models.py`, `nf.py`, `shield.py`, `common/config.py`, `configs/default.json`.
Figures: **`fig/07_cost_loss_and_prior_shift.png`**, `../../../results/figures/R2_calibration.png`, `R3_alert_flood_vs_base_rate.png`.

---

## D1 · Cost-loss: p\* kahan se aaya   [Class A, decision theory]

### Misaal
Barish ka chance 30% hai. Chhata le jaana thoda bojh hai (keemat 1), bheegna mehenga hai (keemat 10). Kya chhata loge? Haan, kyunki 30% × 10 = 3
ka "expected" nuksaan, chhate ke 1 se zyada hai. Agar chance sirf 5% hota to 5% × 10 = 0.5 < 1, chhata mat lo.

### Derivation
Maan lo aag ki probability p hai. Do choice:
- **HOLD (alarm mat bajao):** agar aag hui to C_miss ka nuksaan. Expected cost = **p·C_miss**.
- **ALARM:** agar aag nahi thi to C_FA (false alarm) ka nuksaan. Expected cost = **(1 − p)·C_FA**.

Alarm tab bajao jab ALARM sasta ho: (1 − p)·C_FA < p·C_miss → C_FA < p·(C_FA + C_miss) →

$$p > p^* = \frac{C_{FA}}{C_{FA}+C_{miss}}$$

Repo (`configs/default.json`): C_FA = 5, C_miss = 100 → **p\* = 5/105 = 0.0476**. Matlab "agar 21 me se 1 baar bhi aag ho sakti hai, to
bajao", kyunki chhooti aag 20 guna mehengi maani gayi hai. Figure 07 ke left panel me dono lines exactly p\* par katti hain.

### Alert levels (decision.py `conformal_level`)
| Fused risk | Level | Console me | CAP 1.2 (cap.py) |
|---|---|---|---|
| < p\* | GREEN | Normal | koi public alert nahi |
| p\* se 4p\* | YELLOW | **Watch** (circle) | Minor / Future / Possible |
| 4p\* se 10p\* | ORANGE | **Warning** (diamond) | Severe / Expected / Likely |
| ≥ 10p\* = 0.476 | RED | **Emergency** (octagon) | Extreme / Immediate / Observed |

**Kyun 4× aur 10×?** Ye repo ke "ad-hoc" cut points hain (code me likha hai). Ek calibrated conformal set aane par ye replace ho sakte hain.
Console me "WARNING cut point (× p\*)" aur "EMERGENCY cut point" sliders hain.

### Hamari khoj: p\* = 0.048 ka asar
Per-image OOF stack probabilities par (asli 3,410 images), p\* = 0.048 ke saath **false-alarm rate 0.695** hai (seed 0, `fire_meta_fusion_s0_compare.md`):
aag-free images me se ~70% alarm deti hain. Console ke scenario 1 (Chamoli forest fire, synthetic cameras, real model scores) me yahi baat
"alert flood" ki tarah dikhti hai: repo defaults par aag-free cameras par bhi bahut saare Watch episodes aate hain. (Exact counts console run par
depend karte hain aur repo me record nahi hain, isliye yahan nahi likhe.) Wajah agle section me hai.

---

## D2 · Base rate (prior): "kitni baar sach me aag hoti hai?"   [Bayes; correction PROPOSED, not in repo]

### Misaal
Ek doctor ka test 90% sahi hai. Agar 1000 me se sirf 1 insaan ko bimari hai, to test "positive" aane par bhi zyaadatar log bimaar nahi honge,
kyunki 999 healthy logon me se 10% (≈100) galat positive aayenge, aur sirf 1 sach.

### Hamara case
Hamare models jis data par calibrate hue, usme **55% images me aag thi** (1892 / 3410). Asli camera ki duniya me 1000 frames me se shayad ek me
aag ho. Model "0.3" bole to **training ki duniya me** iska matlab 30% hai, **asli duniya me** bahut kam.

### Formula (Bayes ka prior-shift, Saerens et al. 2002)
$$p' = \frac{p\cdot\pi'/\pi}{p\cdot\pi'/\pi + (1-p)(1-\pi')/(1-\pi)}$$
π = training ka base rate (0.555), π′ = deployment ka base rate.

**Derivation idea:** Bayes niyam me probability = (likelihood × prior), normalised. Model ka likelihood ratio (image kitni "aag jaisi" hai)
nahi badalta; sirf prior badalta hai. Isliye purana prior divide karo, naya multiply karo, aur normalise karo.

Code numbers (p = 0.3): π′ = 0.555 → 0.300 (koi badlaav nahi), π′ = 0.1 → **0.037**, π′ = 0.01 → **0.0035**.

### Asar
- Per-image (asli OOF stack probabilities, figure R3, OUR RESULT on real scores + PROPOSED correction): base rate 1% par false alarms lagbhag 0
  ho jaate hain, lekin **per-image** detection bhi kaafi gir jaati hai. Ye ek **trade-off** hai, "free lunch" nahi.
- Aag kai frames tak dikhti hai, isliye **incident** level (temporal validator, D5) par detection per-image se behtar reh sakti hai. Console
  scenario me ye dekha ja sakta hai (SIMULATED; exact numbers record nahi kiye).
- **Status:** PROPOSED. Repo me ye abhi nahi hai. Console me iska slider "Deployment base rate (PROPOSED)" naam se, SURROGATE chip ke saath hai.

---

## D3 · Calibration: model ka "0.8" sach me 80% ho   [Class A, temperature scaling]

### Misaal
Ek dost hamesha kehta hai "100% pakka!", lekin aadhi baar galat hota hai. Uski baat ko "thoda neeche" karke sunna padta hai. Calibration yahi
karta hai: model ke confidence ko uski asli track record ke hisaab se adjust karta hai.

### Formula
$$p_{cal} = \sigma\!\left(\frac{\mathrm{logit}(p)}{T}\right), \quad \mathrm{logit}(p) = \ln\frac{p}{1-p}$$
- T > 1: model zyada confident tha → probabilities ko 0.5 ki taraf kheencho.
- T < 1: model kam confident tha → door dhakelo.
- T kaise milta hai? Un images par jo model ne training me nahi dekhi (cross-fit: har fold ka T baaki folds se), "log loss" minimise karke.
- Har expert ka apna T hota hai, aur stack ka bhi. Ye cross-fit hote hain, isliye calibration score bhi "bina dekhe" data par hai.

**Kaise check karein:** reliability diagram (figure R2): x-axis "model ne kya kaha", y-axis "sach me kitna hua". Perfect = diagonal line.
**Expected Calibration Error (ECE)** = diagonal se average doori. OOF par calibrated stack ka ECE **0.019**. Held-out (1,023 images, alag dataset) par stack **0.026**, jabki fire CNN akela **0.260** (OUR RESULT, seed 0).

---

## D4 · Fusion: kis expert par kitna bharosa   [Class B, FM-1]   `fusion_models.py`, `nf.py`

### Misaal
Teen gawah hain: ek bahut bharosemand (reliability r zyada), ek jo khud hi unsure hai (uncertainty u zyada), aur ek jo physics ke khilaaf baat
kar raha hai (consistency c kam). Aap teeno ki baat ka "weighted average" loge.

### Effective weight
$$\tilde w_i = r_i \cdot c_i \cdot e^{-u_i/\tau}$$
- r_i = reliability, har source ka **cap** ke saath (adapters.py): fire_cnn 0.80 (cap 0.95), CLIP probe 0.75 (0.90), zero-shot 0.40 (0.50),
  **deepfake 0.30 (cap 0.40)**. Deepfake ka cap kam isliye kyunki naye data par wo fail hua (OOF 0.961, lekin held-out AUC **0.450**, yaani sikke se bhi bura; `MASTER_RESULTS.md`).
- c_i = physics consistency (P02 ka Byram, ya NF-1 neeche).
- e^(−u/τ): jitna unsure, utna kam weight. τ = 0.5 (configs/fusion.json). τ chhota → uncertainty ki saza zyada.

**FM-1 fused risk** = Σ w̃_i p_i / Σ w̃_i (weighted mean).

### NF-1: physics se zyada alarm mat bolo
c_i = exp(−((p_i − φ)₊)² / 2σ²), σ = 0.25. Agar expert physics (φ) se **zyada** alarm bole to uska weight kam; physics jitna ya kam bole to
koi saza nahi. Example (code): p = 0.9, φ = 0.4 → c = 0.135; p = 0.3, φ = 0.4 → c = 1.0.

### NF-3: experts me jhagda → uncertainty badhao
$$U^* = \sum \hat w_i u_i + \lambda\cdot D(p), \qquad D = \sqrt{\textstyle\sum \hat w_i (p_i-\bar p)^2}$$
Agar camera 0.9 bole aur CLIP 0.1, to D bada → U\* bada → alert "Abstain: human review" ban jaata hai (U\* > 0.6). Ye "chup rehne" ki jagah
"insaan se poochho" hai. Rule 19: system kabhi chup nahi rehta, uncertain hone par escalate karta hai.

### Hamari real-pairing khoj (OUR RESULT)
Same image par chaaron experts (fire CNN, zero-shot, CLIP probe, colour histogram) ka calibrated logistic **stack**: OOF AUC **0.949**, jabki CLIP probe akela **0.959**. Stack − best single = −0.010 (95% CI −0.015 se −0.005), isliye stack gate par **NOT ADMITTED** hua. Fusion ne AUC nahi badhaya. Uska fayda calibration hai (held-out ECE 0.026 vs CNN 0.260). Isliye "fusion = bharosa aur calibration, extra accuracy nahi" (`results/fire_meta/`, seed 0).
**calibration** behtar ki (ECE 0.026). Isliye "fusion = bharosa aur calibration, extra accuracy nahi" (results/fire_meta).

---

## D5 · Temporal validator: ek frame se mat daro   [Class A design]   `ws4_cctv`
Car ki headlight ek frame me "aag" lagti hai, agle me nahi. Validator kehta hai: **pichhle W = 5 frames me se kam se kam m = 3** threshold
(0.5) se upar hon, tabhi "confirmed". Ye glints aur flash ko rokta hai. Trade-off: m badhao → kam false alarms, par der se pakad.

---

## D6 · Safety shield: physics sirf level badha sakti hai   [Class A rules]   `shield.py`
$$\text{level} = \max(\text{conformal level}(p),\ \text{shield floor})$$
Max isliye ki shield **kabhi level ghata nahi sakta**. Agar learned model galti se "safe" bole, aur physics kahe "FS < 1", to physics jeetegi.
Ek akela sensor RED nahi bajwa sakta (≥ 2 nodes chahiye), taaki ek kharab sensor poora district na hila de.

---

## D7 · Human approval: koi bhi public alert insaan ke bina nahi   (Rule 19)
`cap.py` CAP 1.2 alert tabhi banata hai jab "APPROVED:<naam>" token ho. Bina approval → `SafetyViolation`. Console me "Approve" ke baad bhi
"Dispatch (demo)" kuch nahi bhejta.

## Ek nazar me
| Step | Sawaal | Repo default |
|---|---|---|
| Calibration | model ka 0.8 sach me 80% hai? | cross-fit temperature |
| Base rate | asli duniya me aag kitni rare hai? | **not in repo** (PROPOSED) |
| Fusion | kis par kitna bharosa? | FM-1, τ = 0.5, λ = 0.3 |
| Temporal | kya ye tikta hai? | 3 of 5 frames ≥ 0.5 |
| Decision | alarm sasta hai? | p\* = 0.0476, cuts 4×, 10× |
| Shield | physics kya kehti hai? | sirf raise |
| Human | kaun approve karega? | hamesha required |
<!-- END -->
