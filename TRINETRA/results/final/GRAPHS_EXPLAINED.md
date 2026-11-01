# TRINETRA — har graph ka matlab (Hinglish)

Saare result graphs OUR RESULTS (prototype pack) se bane hain; physics graphs repo ke apne Python functions se.

## Measured results (R0-R9)

### Har measured ROC-AUC ek chart par
`figures/results/R0_scorecard_all_auc.png`

![R0_scorecard_all_auc.png](figures/results/R0_scorecard_all_auc.png)

Orange = same-source (OOF, spatial CV), blue = naya dataset (held-out). 0.5 = sikka uchhalna. Ek nazar me dikhta hai kaunsa model tikta hai (fire, CLIP) aur kaunsa naye data par gir jaata hai (deepfake).

### Fire ROC curves (OOF + held-out)
`figures/results/R1_fire_roc_oof_and_heldout.png`

![R1_fire_roc_oof_and_heldout.png](figures/results/R1_fire_roc_oof_and_heldout.png)

Curve jitna upar-left, utna achha. CLIP probe aur stack sabse upar; fire CNN neeche. Right panel = naya dataset (DeepFire), jahan sab models kaafi achhe hain.

### Calibration
`figures/results/R2_calibration.png`

![R2_calibration.png](figures/results/R2_calibration.png)

Model jo probability bole, kya utna hi sach hota hai? Diagonal line = perfect. Temperature scaling ke baad lines diagonal ke paas hain, isliye p* threshold par bharosa kar sakte hain.

### Base-rate correction
`figures/results/R3_alert_flood_vs_base_rate.png`

![R3_alert_flood_vs_base_rate.png](figures/results/R3_alert_flood_vs_base_rate.png)

Asli duniya me aag bahut kam hoti hai (1% ya kam), training me 55%. Prior-shift correction se false alarm bahut girte hain, par per-image detection bhi girti hai; video me aag kai frames tak dikhti hai, isliye incident pakda jaata hai. Ye PROPOSAL hai, repo me default nahi.

### Landslide: physics bina training
`figures/results/R4_landslide_auc.png`

![R4_landslide_auc.png](figures/results/R4_landslide_auc.png)

Blue = physics jo kisi data par fit nahi hui (Caine, dFS, geo gate). Phir bhi ROC-AUC ~0.75. Barish logistic aur FM-1 fusion thoda upar. Geo-PINN laal line.

### RL held-out
`figures/results/R5_rl_heldout.png`

![R5_rl_heldout.png](figures/results/R5_rl_heldout.png)

Learned RL (CQL), fixed rule, tuned rule, always-alarm: reward per image. RL tuned rule se behtar nahi hua, isliye deploy nahi.

### Generalisation gap
`figures/results/R6_generalisation_gap.png`

![R6_generalisation_gap.png](figures/results/R6_generalisation_gap.png)

Same source vs naya source. Deepfake 0.96 se 0.45 par gira: isliye wo sirf down-weighter hai.

### Cross-modal video
`figures/results/R7_crossmodal_video.png`

![R7_crossmodal_video.png](figures/results/R7_crossmodal_video.png)

FireSense 49 videos par har stream ka (detection - false alarm), temporal validator ke baad. Stack +0.47, clip_probe +0.32, fire CNN +0.01: video par teeno experts ko jodna sach me kaam aaya. n chhota hai (49 videos), isliye ise counts ki tarah padho.

### Cross-modal confusers
`figures/results/R8_crossmodal_confusers.png`

![R8_crossmodal_confusers.png](figures/results/R8_crossmodal_confusers.png)

Weather, candle, scenes par har stream ka false-alarm rate. Kam = achha.

### Confuser-aware retrain (S)
`figures/results/R9_stress_retrain.png`

![R9_stress_retrain.png](figures/results/R9_stress_retrain.png)

Ek confuser type training se bahar rakha (unseen), baaki do par hard-negative training. Barabar recall 0.90 par unseen confuser par false alarms: CLIP probe 0.43 -> 0.32, stack 0.35 -> 0.16, aur DeepFire AUC 0.998 -> 0.997 (girna 0.01 se kam). Gate 3/3 seeds ADMITTED: TRINETRA ka pehla admitted learned upgrade.

## Extra result graphs (G01-G14)

### Har model ka ROC-AUC, har seed alag dot
`figures/extra/G01_auc_per_seed.png`

![G01_auc_per_seed.png](figures/extra/G01_auc_per_seed.png)

Har dot ek seed (alag random start) ka result hai, kaali line average. Dots paas-paas = model stable hai. clip_probe aur fire_meta_fusion sabse upar (~0.95), colour histogram baseline sabse neeche (~0.68). Landslide models (geo_pinn, geo_fusion) ~0.72-0.78 par hain, kyunki wahan sirf barish + DEM jaise mote features hain.

### ROC-AUC vs PR-AUC vs recall@FPR5%
`figures/extra/G02_metrics_compare.png`

![G02_metrics_compare.png](figures/extra/G02_metrics_compare.png)

ROC-AUC = ranking kitni achhi. PR-AUC = jab model 'aag' bole to kitna sahi. Recall@FPR5% = sabse practical: agar 100 me se sirf 5 galat alarm allow hain, to kitni asli aag pakdi. Colour histogram ka recall bahut kam, clip_probe/stack ~0.8 se upar.

### Same-source vs naya source
`figures/extra/G03_generalisation.png`

![G03_generalisation.png](figures/extra/G03_generalisation.png)

Fire models naye dataset (DeepFire forest photos) par bhi tike. Deepfake model CIFAKE par 0.96 tha, par naye generator wali images par 0.45 (sikke se bhi kharab). Isliye deepfake ko sirf 'low-trust down-weighter' rakha, alarm dene wala nahi.

### Confuser images par false alarm
`figures/extra/G04_confuser_false_alarms.png`

![G04_confuser_false_alarms.png](figures/extra/G04_confuser_false_alarms.png)

Ye sab images me khatarnak aag NAHI hai (fog, candle, normal sadak/jungle). Bar jitna lamba, utni baar model ne galti se 'aag' bola. Candle/small flames sabse mushkil hain, kyunki wo sach me aag hi hai, bas khatarnak nahi. Isi ke liye S account ka confuser-aware retrain bana (R9 graph).

### Video: raw vs temporal validator
`figures/extra/G05_video_validator.png`

![G05_video_validator.png](figures/extra/G05_video_validator.png)

Ek frame par aag dikhna kaafi nahi; validator dekhta hai ki aag kai frames tak lagatar dikhe aur flicker kare. Isse false-alarm videos thode kam hote hain. n sirf 49 videos hai, isliye ye 'counts' hain, pakka number nahi.

### Fire meta-fusion: kaunsa jodne ka tareeka best
`figures/extra/G06_fire_meta_rules.png`

![G06_fire_meta_rules.png](figures/extra/G06_fire_meta_rules.png)

Chaar fire experts (CNN, CLIP zero-shot, CLIP probe, colour) ko jodne ke tareeke: stacked logistic (meta), FM-1 (hamara uncertainty-weighted fusion), mean, max, aur akela expert. Stack lagbhag clip_probe ke barabar hai, upar nahi, isliye gate ne admit nahi kiya. Imaandaar result: jab ek expert pehle se itna strong ho, jodne se fayda kam milta hai.

### Landslide fusion rules (PR-AUC)
`figures/extra/G07_geo_fusion_rules.png`

![G07_geo_fusion_rules.png](figures/extra/G07_geo_fusion_rules.png)

Blue = akela signal (barish model, Caine line, dFS, geo gate). Purple = jodne ke tareeke (FM-1, PHARAOH, median, max, physics shield, stacked logistic). Same 736 asli rows par sab compare hue, seeds ka average.

### Landslide ke features ka distribution
`figures/extra/G08_landslide_features.png`

![G08_landslide_features.png](figures/extra/G08_landslide_features.png)

Orange = jis din landslide hua, grey = usi jagah ka normal din. Jahan orange right ki taraf khiska hai (barish, Caine ratio, dFS), wahi feature kaam ka hai. Slope aur elevation me farak kam hai kyunki control din usi jagah ke hain (sirf mausam badla).

### Caine threshold scatter
`figures/extra/G09_caine_scatter.png`

![G09_caine_scatter.png](figures/extra/G09_caine_scatter.png)

Har dot ek din. Laal line = Caine ki global seema. NASA POWER ki barish DAILY hai (ghante wali nahi), isliye intensity average ho jaati hai aur lagbhag saare dots line ke neeche aate hain; D bhi 24 h ke multiples me hai. Isliye hum line ko yes/no ki tarah nahi, ratio I/I_crit (line ke kitna paas) ko score ki tarah use karte hain. Bina training ke ye score 184 Indian events par ROC-AUC 0.758 deta hai. Orange dots upar-right ki taraf zyada hain: lambi + tez barish = zyada khatra.

### GLOF: jheel ka area -> paani -> flood peak
`figures/extra/G10_glof_power_laws.png`

![G10_glof_power_laws.png](figures/extra/G10_glof_power_laws.png)

Glacial jheel jitni badi, utna paani (V = a A^b), aur jitna paani utna bada flood peak (Q = a V^b). Area-volume fit b = 1.13 (CI 0.71-1.50). Points kam hain (21 aur 31), isliye CI chauda hai; ye rough screening ke liye hai, exact prediction ke liye nahi.

### RL environment ke policies
`figures/extra/G11_rl_env_policies.png`

![G11_rl_env_policies.png](figures/extra/G11_rl_env_policies.png)

Simulator me 360 monsoon seasons. C_miss = ek missed landslide ki keemat (false alarm = 5). always_hold = kabhi alarm nahi. Jab miss mehenga hai (5000) to physics rule always_hold se ~2.4x behtar hai. Learned RL (CQL) rule ke barabar hi hai (scorecard: oracle bhi lagbhag same), isliye gate ne rule rakha. Ye imaandaar negative result hai: RL ke liye jagah hi nahi bachi.

### Offline RL ka gain aur uska lower bound
`figures/extra/G12_offline_rl_gain.png`

![G12_offline_rl_gain.png](figures/extra/G12_offline_rl_gain.png)

Purple = RL rule se kitna behtar (average), laal = 95% confidence ka lower bound. In-sample number optimistic tha; jab honest held-out folds par test kiya to lower bound 0 se neeche gaya, isliye deploy 0/3. Rule hi chalega.

### Model kitna confident hai: score distribution
`figures/extra/G13_score_distributions.png`

![G13_score_distributions.png](figures/extra/G13_score_distributions.png)

Grey = bina aag ki images, orange = aag wali. Achha model dono pahaad alag-alag rakhta hai (grey left, orange right). Fire CNN me dono kaafi overlap karte hain, CLIP probe aur stack me saaf alag hain.

### Confusion matrix (threshold 0.5, OOF)
`figures/extra/G14_confusion_matrices.png`

![G14_confusion_matrices.png](figures/extra/G14_confusion_matrices.png)

Upar-left = sahi 'no fire', neeche-right = sahi 'fire'. Upar-right = false alarm, neeche-left = chhooti aag (sabse khatarnak). Asli system 0.5 nahi, cost-loss threshold p* use karta hai (P03 chapter), jo chhooti aag ko aur kam karta hai.

## Physics explainers (01-10)

### FS vs pore pressure
`figures/physics/01_fs_vs_pore_pressure.png`

![01_fs_vs_pore_pressure.png](figures/physics/01_fs_vs_pore_pressure.png)

Mitti me paani ka dabaav badhe to factor of safety girta hai; FS < 1 = slope girega. Steep slope = kam margin.

### Iverson pressure head
`figures/physics/02_iverson_pressure_head.png`

![02_iverson_pressure_head.png](figures/physics/02_iverson_pressure_head.png)

Barish ke baad paani dheere-dheere gehraai tak pahunchta hai; isliye landslide barish ke kuch ghante/din baad aata hai.

### Caine threshold
`figures/physics/03_caine_threshold.png`

![03_caine_threshold.png](figures/physics/03_caine_threshold.png)

Lambi barish ko kam intensity chahiye girane ke liye: I = 14.82 D^-0.39 (log-log par seedhi line).

### Fukuzono inverse velocity
`figures/physics/04_fukuzono_inverse_velocity.png`

![04_fukuzono_inverse_velocity.png](figures/physics/04_fukuzono_inverse_velocity.png)

Girne se pehle slope tez hota jaata hai; 1/velocity ki line zero ko jahan chhooti hai, wahi failure time ka andaza.

### Fire physics
`figures/physics/05_fire_physics.png`

![05_fire_physics.png](figures/physics/05_fire_physics.png)

Flame height (Heskestad), Byram number (hawa vs aag), flicker frequency: camera jo dekhe wo physics se match kare.

### Plume temperature
`figures/physics/06_plume_temperature.png`

![06_plume_temperature.png](figures/physics/06_plume_temperature.png)

Aag ke upar garam hawa ka tapmaan oonchai ke saath girta hai (McCaffrey).

### Cost-loss p*
`figures/physics/07_cost_loss_and_prior_shift.png`

![07_cost_loss_and_prior_shift.png](figures/physics/07_cost_loss_and_prior_shift.png)

Galat alarm ki keemat 5, chhooti aag ki 100 -> p* = 5/105 = 0.048. Is se upar probability = alarm.

### LoRa range + airtime
`figures/physics/08_lora_range_airtime.png`

![08_lora_range_airtime.png](figures/physics/08_lora_range_airtime.png)

Spreading factor badhao to range badhti hai par message bhejne me zyada time lagta hai.

### Fresnel zone, asli terrain
`figures/physics/09_fresnel_real_terrain.png`

![09_fresnel_real_terrain.png](figures/physics/09_fresnel_real_terrain.png)

Gateway se gaon tak radio line ke beech pahad aata hai; relay oonchi jagah chahiye.

### Noisy-OR
`figures/physics/10_noisy_or.png`

![10_noisy_or.png](figures/physics/10_noisy_or.png)

Physics signals jodte waqt ek bhi signal khatra bole to combined risk kabhi kam nahi hota.
