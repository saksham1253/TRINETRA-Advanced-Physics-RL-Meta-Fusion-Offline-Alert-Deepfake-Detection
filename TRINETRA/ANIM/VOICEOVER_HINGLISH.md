# TRINETRA Live Flow · VOICE-OVER (Hinglish, with English subtitle track)

Read the Hinglish line when the timestamp arrives. The same lines are burned in as captions (toggle EN / Hinglish / off with C).

## S0 · Cold open (0:00–0:15)

- **[0:00]** India ko aisi warnings chahiye jo andhere me teer na chalayein.
  - EN: India needs warnings that do not guess blindly.
- **[0:05]** TRINETRA: teen aankhein. Saboot dekho, physics aur uncertainty se socho, aur insaan ke saath jawab do.
  - EN: TRINETRA: three eyes. See the evidence. Reason with physics and uncertainty. Respond with a human in the loop.

## S1 · Why warnings fail (0:15–0:50)

- **[0:15]** Surveys aur reports ek hi baat kehte hain: jahan early warning kamzor hai, wahan maut zyada. WMO ke 2023 survey me lagbhag aath guna.
  - EN: Surveys and reports agree: where early warning is weak, people die. WMO's 2023 country survey finds about eight times higher mortality.
- **[0:23]** Sirf 24 ghante pehle ki warning se damage lagbhag 30 percent kam. Odisha me 1999 me lagbhag 10,000 maut, Fani me 64.
  - EN: Just 24 hours of warning can cut damage by about 30 percent. Odisha went from about 10,000 cyclone deaths in 1999 to 64 in Fani.
- **[0:31]** Warning systems 14 documented tareekon se fail hote hain: false alarm, der se pakadna, ek kamzor sensor, fake media, jhoothe evaluation numbers.
  - EN: Warning systems fail in 14 documented ways: false alarms, late detection, one fragile sensor, fake media, inflated evaluation.
- **[0:40]** Har tile palat ke TRINETRA ka jawab dikhata hai, imaandaar chip ke saath: bana hua, ya humne khud measure kiya.
  - EN: Each tile flips to TRINETRA's answer, with an honest chip: built, or measured by us.

## S2 · The data journey (0:50–1:40)

- **[0:50]** Asli datasets bahut bade hain: 36 ghante ke prototype ke liye bahut zyada.
  - EN: The original datasets are huge: far too big for a 36-hour prototype.
- **[0:59]** Isliye har ek se chhota, seeded, stratified subset lete hain, aur exactly likhte hain kaise.
  - EN: So we draw a small, seeded, stratified subset from each one, and record exactly how.
- **[1:09]** Tables ek schema me map hoti hain. Landslide pack: 736 rows andar, 736 bahar, zero drop, 101 spatial groups.
  - EN: Tables are mapped to one schema. The landslide pack: 736 rows in, 736 out, zero dropped, 101 spatial groups.
- **[1:20]** Leakage trap: random split me ek hi video ke frames train aur test dono me, aur number jhootha bada dikhta hai.
  - EN: The leakage trap: a random split puts frames of the same video in train and test, and the score looks fake-good.
- **[1:27]** Grouped split har video, site aur block ko poora ek taraf rakhta hai. Ek alag dataset vault me held-out test ke liye.
  - EN: A grouped split keeps every video, site and block whole. A different dataset waits in the vault for the held-out test.
- **[1:33]** Phir har split us module tak jaata hai jise zarurat hai: train, validation, held-out ya stress.
  - EN: Then every split flows to the module that needs it: train, validation, held-out or stress.

## S3 · Incident A: the false alarm that does not fire (1:40–2:20)

- **[1:40]** Simulated replay: kitchen me bhaap uth rahi hai. Fire detector ka score badhta hai.
  - EN: Simulated replay: steam rises in a kitchen. The fire detector's score climbs.
- **[1:49]** Zero-shot dhuan aur bhaap ke beech atakta hai. Physics badhte plume ki ummeed karti hai; ye aag ki tarah nahi badhta.
  - EN: Zero-shot hesitates between smoke and steam. Physics expects a growing plume; the region does not grow like fire.
- **[1:59]** Flicker us band ke bahar hai jo is size ki lau ke liye physics batati hai, isliye consistency girti hai aur detector ka weight kam hota hai.
  - EN: Flicker is outside the band physics predicts for a flame of this size, so physics consistency drops and the detector loses weight.
- **[2:09]** Fused risk kam rehta hai. Sabse neecha tier, ek log entry, koi public alert nahi. Seedha threshold bajta. Saboot sahmat nahi the.
  - EN: Fused risk stays low. Lowest tier, a log entry, no public alert. A dumb threshold would have rung. Evidence did not agree.

## S4 · Incident B: a real fire, early (2:20–3:00)

- **[2:20]** Wahi layout, asli aag ka simulated replay. Shuru me dhuan chhota hai; har score akele kamzor hai.
  - EN: Same layout, simulated replay of a real fire. Early smoke is small; every score is weak on its own.
- **[2:29]** Par dekha gaya growth physics curve ke saath chalta hai, aur flicker predicted band ke andar hai.
  - EN: But the observed growth follows the physics curve, and flicker sits inside the predicted band.
- **[2:38]** Experts milte hain, uncertainty ka gola sikudta hai, aur fused risk cost-based line paar karta hai. Miss ki keemat false alarm se 20 guna.
  - EN: Experts converge, the uncertainty halo narrows, and fused risk crosses the cost-based line. A miss costs 20 times a false alarm.
- **[2:48]** Operator saboot aur wajah dekhta hai, aur approve karta hai. Tabhi tiered alert authorised channels se jaata hai.
  - EN: The operator sees the evidence and the reasons, and approves. Only then does a tiered alert go out through authorised channels.

## S5 · The fake that arrives (3:00–3:25)

- **[3:00]** Social media se ek dramatic aag ka video aata hai. Placeholder image, synthetic label ke saath.
  - EN: A dramatic fire video arrives from social media. Placeholder imagery, labelled synthetic.
- **[3:08]** Authenticity check ise flag karta hai, aur iska trust girta hai: r prime barabar r guna ek minus p-fake.
  - EN: The authenticity check flags it, and its trust drops: r prime equals r times one minus p-fake.
- **[3:16]** Camera, satellite aur weather iski pushti nahi karte. Ye neeche kar diya jaata hai aur alert nahi badha sakta.
  - EN: Camera, satellite and weather do not corroborate it. It is downgraded and cannot raise the alert. Misinformation is screened before it moves the system.

## S6 · Fusion under the hood (3:25–3:55)

- **[3:25]** Fusion engine ke andar: har expert ka weight reliability guna physics consistency guna e ki power minus uncertainty by tau.
  - EN: Inside the fusion engine: each expert's weight is reliability times physics consistency times e to the minus uncertainty over tau.
- **[3:34]** Code se worked example: teen experts asahmat, shaky wale ka weight sirf 0.147, fused risk 0.63, level RED.
  - EN: Worked example from the code: three experts disagree, the doubtful one weighs only 0.147, the fused risk is 0.63, level RED.
- **[3:42]** Ab ek mushkil case pe averaging rule badlo: ek outlier, ek galat-calibrated expert aur ek correlated jodi. Output aur uncertainty dekho.
  - EN: Now switch the averaging rule on a hard case: an outlier, a miscalibrated expert and a correlated pair. Watch the output and its uncertainty.
- **[3:50]** Calibration asli out-of-fold scores pe naapi jaati hai, temperature sirf doosre folds pe fit hota hai.
  - EN: Calibration is measured on real out-of-fold scores, with the temperature fitted on other folds only.

## S7 · The physics engine (3:55–4:25)

- **[3:55]** Physics barish, dhalaan aur pixels ko check hone wale daavon me badalti hai. Har model ka class chip aur code ke asli parameters.
  - EN: Physics turns rain, slope and pixels into checkable claims. Each model has a class chip and its real parameters from the code.
- **[4:05]** Asli data: landslide wale din Caine ratio unhi jagahon ke normal monsoon dinon se upar hota hai.
  - EN: Real data: on catalogued landslide days the Caine ratio sits higher than on the same sites' normal monsoon days.
- **[4:14]** Derived term apne parent pe wapas aata hai: pore pressure zero to FS drop zero. Aur apne regime ke bahar model pe bharosa nahi.
  - EN: A derived term collapses back to its parent: with no pore pressure, the FS drop is zero. And a model outside its regime is not trusted.

## S8 · Cyclone mode (4:25–4:40)

- **[4:25]** Cyclone mode planned hai, bana nahi: wind-profile physics, forecasts, zameeni saboot aur fake news screening.
  - EN: Cyclone mode is planned, not built: wind-profile physics, forecasts, ground evidence and misinformation screening.
- **[4:33]** Evacuation planner sirf salah dega. Faisla insaan karega.
  - EN: An evacuation planner would only advise. A human decides.

## S9 · Proof, honesty, next (4:40–4:55)

- **[4:40]** Measured: akeli physics 184 asli landslides pe AUC 0.758. Hamara RL physics rule ko nahi hara paya, isliye off. Zero-shot admit nahi hua.
  - EN: Measured: physics alone reaches AUC 0.758 on 184 real landslides. Our RL never beat the physics rule, so it stays off. Zero-shot was not admitted.
- **[4:48]** TRINETRA certified alarms aur official warnings ka saathi hai. Har public alert insaan approve karta hai.
  - EN: TRINETRA complements certified alarms and official warnings. A human approves every public alert.

