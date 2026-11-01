window.ANIM_SCRIPT = {
 "title": "TRINETRA Live Flow",
 "scenes": [
  {
   "id": "S0",
   "name": "Cold open",
   "t0": 0,
   "dur": 15,
   "layer": 0,
   "purpose": "Introduce the three eyes: see, reason, respond.",
   "captions": [
    {
     "t": 0.5,
     "en": "India needs warnings that do not guess blindly.",
     "hi": "India ko aisi warnings chahiye jo andhere me teer na chalayein."
    },
    {
     "t": 5.5,
     "en": "TRINETRA: three eyes. See the evidence. Reason with physics and uncertainty. Respond with a human in the loop.",
     "hi": "TRINETRA: teen aankhein. Saboot dekho, physics aur uncertainty se socho, aur insaan ke saath jawab do."
    }
   ]
  },
  {
   "id": "S1",
   "name": "Why warnings fail",
   "t0": 15,
   "dur": 35,
   "layer": 0,
   "purpose": "Surveys and reports on the cost of disasters and the value of early warning; then the 14 failure patterns and our answers.",
   "captions": [
    {
     "t": 0.5,
     "en": "Surveys and reports agree: where early warning is weak, people die. WMO's 2023 country survey finds about eight times higher mortality.",
     "hi": "Surveys aur reports ek hi baat kehte hain: jahan early warning kamzor hai, wahan maut zyada. WMO ke 2023 survey me lagbhag aath guna."
    },
    {
     "t": 8.0,
     "en": "Just 24 hours of warning can cut damage by about 30 percent. Odisha went from about 10,000 cyclone deaths in 1999 to 64 in Fani.",
     "hi": "Sirf 24 ghante pehle ki warning se damage lagbhag 30 percent kam. Odisha me 1999 me lagbhag 10,000 maut, Fani me 64."
    },
    {
     "t": 16.5,
     "en": "Warning systems fail in 14 documented ways: false alarms, late detection, one fragile sensor, fake media, inflated evaluation.",
     "hi": "Warning systems 14 documented tareekon se fail hote hain: false alarm, der se pakadna, ek kamzor sensor, fake media, jhoothe evaluation numbers."
    },
    {
     "t": 25.0,
     "en": "Each tile flips to TRINETRA's answer, with an honest chip: built, or measured by us.",
     "hi": "Har tile palat ke TRINETRA ka jawab dikhata hai, imaandaar chip ke saath: bana hua, ya humne khud measure kiya."
    }
   ]
  },
  {
   "id": "S2",
   "name": "The data journey",
   "t0": 50,
   "dur": 50,
   "layer": 1,
   "purpose": "From terabyte originals to a small, leakage-safe prototype pack, and where every split goes.",
   "captions": [
    {
     "t": 0.5,
     "en": "The original datasets are huge: far too big for a 36-hour prototype.",
     "hi": "Asli datasets bahut bade hain: 36 ghante ke prototype ke liye bahut zyada."
    },
    {
     "t": 9.0,
     "en": "So we draw a small, seeded, stratified subset from each one, and record exactly how.",
     "hi": "Isliye har ek se chhota, seeded, stratified subset lete hain, aur exactly likhte hain kaise."
    },
    {
     "t": 19.0,
     "en": "Tables are mapped to one schema. The landslide pack: 736 rows in, 736 out, zero dropped, 101 spatial groups.",
     "hi": "Tables ek schema me map hoti hain. Landslide pack: 736 rows andar, 736 bahar, zero drop, 101 spatial groups."
    },
    {
     "t": 30.0,
     "en": "The leakage trap: a random split puts frames of the same video in train and test, and the score looks fake-good.",
     "hi": "Leakage trap: random split me ek hi video ke frames train aur test dono me, aur number jhootha bada dikhta hai."
    },
    {
     "t": 37.0,
     "en": "A grouped split keeps every video, site and block whole. A different dataset waits in the vault for the held-out test.",
     "hi": "Grouped split har video, site aur block ko poora ek taraf rakhta hai. Ek alag dataset vault me held-out test ke liye."
    },
    {
     "t": 43.0,
     "en": "Then every split flows to the module that needs it: train, validation, held-out or stress.",
     "hi": "Phir har split us module tak jaata hai jise zarurat hai: train, validation, held-out ya stress."
    }
   ]
  },
  {
   "id": "SD",
   "name": "System DFD, live",
   "t0": 100,
   "dur": 30,
   "layer": 3,
   "purpose": "Whole system as a data-flow diagram with live packets, including the offline last mile.",
   "captions": [
    {
     "t": 0.5,
     "en": "The whole system as a data-flow diagram: four sources, adapters and five experts.",
     "hi": "Poora system ek data-flow diagram me: chaar sources, adapters aur paanch experts."
    },
    {
     "t": 7,
     "en": "Each expert sends a probability and an uncertainty; the physics engine checks consistency.",
     "hi": "Har expert probability aur uncertainty bhejta hai; physics engine consistency check karta hai."
    },
    {
     "t": 14,
     "en": "Meta-fusion combines them. The decision can only be raised, and physics can set a floor.",
     "hi": "Meta-fusion sabko jodta hai. Decision sirf upar ja sakta hai, physics floor laga sakta hai."
    },
    {
     "t": 21,
     "en": "Nothing goes public until a human approves. With no internet, the alert travels over LoRa, sirens, satellite and people.",
     "hi": "Human approve kare tabhi public alert. Internet na ho to alert LoRa, siren, satellite aur logon ke zariye jaata hai."
    }
   ]
  },
  {
   "id": "S3",
   "name": "Incident A: the false alarm that does not fire",
   "t0": 130,
   "dur": 40,
   "layer": 2,
   "purpose": "Steam in a kitchen: the detector rises, but evidence does not agree.",
   "captions": [
    {
     "t": 0.5,
     "en": "Simulated replay: steam rises in a kitchen. The fire detector's score climbs.",
     "hi": "Simulated replay: kitchen me bhaap uth rahi hai. Fire detector ka score badhta hai."
    },
    {
     "t": 9.0,
     "en": "Zero-shot hesitates between smoke and steam. Physics expects a growing plume; the region does not grow like fire.",
     "hi": "Zero-shot dhuan aur bhaap ke beech atakta hai. Physics badhte plume ki ummeed karti hai; ye aag ki tarah nahi badhta."
    },
    {
     "t": 19.0,
     "en": "Flicker is outside the band physics predicts for a flame of this size, so physics consistency drops and the detector loses weight.",
     "hi": "Flicker us band ke bahar hai jo is size ki lau ke liye physics batati hai, isliye consistency girti hai aur detector ka weight kam hota hai."
    },
    {
     "t": 29.0,
     "en": "Fused risk stays low. Lowest tier, a log entry, no public alert. A dumb threshold would have rung. Evidence did not agree.",
     "hi": "Fused risk kam rehta hai. Sabse neecha tier, ek log entry, koi public alert nahi. Seedha threshold bajta. Saboot sahmat nahi the."
    }
   ]
  },
  {
   "id": "S4",
   "name": "Incident B: a real fire, early",
   "t0": 170,
   "dur": 40,
   "layer": 3,
   "purpose": "Same layout, a real fire: experts converge, physics snaps, a human approves.",
   "captions": [
    {
     "t": 0.5,
     "en": "Same layout, simulated replay of a real fire. Early smoke is small; every score is weak on its own.",
     "hi": "Wahi layout, asli aag ka simulated replay. Shuru me dhuan chhota hai; har score akele kamzor hai."
    },
    {
     "t": 9.0,
     "en": "But the observed growth follows the physics curve, and flicker sits inside the predicted band.",
     "hi": "Par dekha gaya growth physics curve ke saath chalta hai, aur flicker predicted band ke andar hai."
    },
    {
     "t": 18.0,
     "en": "Experts converge, the uncertainty halo narrows, and fused risk crosses the cost-based line. A miss costs 20 times a false alarm.",
     "hi": "Experts milte hain, uncertainty ka gola sikudta hai, aur fused risk cost-based line paar karta hai. Miss ki keemat false alarm se 20 guna."
    },
    {
     "t": 28.0,
     "en": "The operator sees the evidence and the reasons, and approves. Only then does a tiered alert go out through authorised channels.",
     "hi": "Operator saboot aur wajah dekhta hai, aur approve karta hai. Tabhi tiered alert authorised channels se jaata hai."
    }
   ]
  },
  {
   "id": "S5",
   "name": "The fake that arrives",
   "t0": 210,
   "dur": 25,
   "layer": 2,
   "purpose": "A viral fire video is screened and cannot move the alert tier.",
   "captions": [
    {
     "t": 0.5,
     "en": "A dramatic fire video arrives from social media. Placeholder imagery, labelled synthetic.",
     "hi": "Social media se ek dramatic aag ka video aata hai. Placeholder image, synthetic label ke saath."
    },
    {
     "t": 8.0,
     "en": "The authenticity check flags it, and its trust drops: r prime equals r times one minus p-fake.",
     "hi": "Authenticity check ise flag karta hai, aur iska trust girta hai: r prime barabar r guna ek minus p-fake."
    },
    {
     "t": 16.0,
     "en": "Camera, satellite and weather do not corroborate it. It is downgraded and cannot raise the alert. Misinformation is screened before it moves the system.",
     "hi": "Camera, satellite aur weather iski pushti nahi karte. Ye neeche kar diya jaata hai aur alert nahi badha sakta."
    }
   ]
  },
  {
   "id": "S6",
   "name": "Fusion under the hood",
   "t0": 235,
   "dur": 30,
   "layer": 3,
   "purpose": "Calibrate, weight, pool, uncertainty, threshold, tier, and why this averaging.",
   "captions": [
    {
     "t": 0.5,
     "en": "Inside the fusion engine: each expert's weight is reliability times physics consistency times e to the minus uncertainty over tau.",
     "hi": "Fusion engine ke andar: har expert ka weight reliability guna physics consistency guna e ki power minus uncertainty by tau."
    },
    {
     "t": 9.0,
     "en": "Worked example from the code: three experts disagree, the doubtful one weighs only 0.147, the fused risk is 0.63, level RED.",
     "hi": "Code se worked example: teen experts asahmat, shaky wale ka weight sirf 0.147, fused risk 0.63, level RED."
    },
    {
     "t": 17.0,
     "en": "Now switch the averaging rule on a hard case: an outlier, a miscalibrated expert and a correlated pair. Watch the output and its uncertainty.",
     "hi": "Ab ek mushkil case pe averaging rule badlo: ek outlier, ek galat-calibrated expert aur ek correlated jodi. Output aur uncertainty dekho."
    },
    {
     "t": 25.0,
     "en": "Calibration is measured on real out-of-fold scores, with the temperature fitted on other folds only.",
     "hi": "Calibration asli out-of-fold scores pe naapi jaati hai, temperature sirf doosre folds pe fit hota hai."
    }
   ]
  },
  {
   "id": "S7",
   "name": "The physics engine",
   "t0": 265,
   "dur": 30,
   "layer": 2,
   "purpose": "Class A/B/C physics with real parameters, validity regimes, and a real landslide day.",
   "captions": [
    {
     "t": 0.5,
     "en": "Physics turns rain, slope and pixels into checkable claims. Each model has a class chip and its real parameters from the code.",
     "hi": "Physics barish, dhalaan aur pixels ko check hone wale daavon me badalti hai. Har model ka class chip aur code ke asli parameters."
    },
    {
     "t": 10.0,
     "en": "Real data: on catalogued landslide days the Caine ratio sits higher than on the same sites' normal monsoon days.",
     "hi": "Asli data: landslide wale din Caine ratio unhi jagahon ke normal monsoon dinon se upar hota hai."
    },
    {
     "t": 19.0,
     "en": "A derived term collapses back to its parent: with no pore pressure, the FS drop is zero. And a model outside its regime is not trusted.",
     "hi": "Derived term apne parent pe wapas aata hai: pore pressure zero to FS drop zero. Aur apne regime ke bahar model pe bharosa nahi."
    }
   ]
  },
  {
   "id": "S8",
   "name": "Cyclone mode",
   "t0": 295,
   "dur": 15,
   "layer": 4,
   "purpose": "Where the same pipeline goes next. Planned, not built.",
   "captions": [
    {
     "t": 0.5,
     "en": "Cyclone mode is planned, not built: wind-profile physics, forecasts, ground evidence and misinformation screening.",
     "hi": "Cyclone mode planned hai, bana nahi: wind-profile physics, forecasts, zameeni saboot aur fake news screening."
    },
    {
     "t": 8.0,
     "en": "An evacuation planner would only advise. A human decides.",
     "hi": "Evacuation planner sirf salah dega. Faisla insaan karega."
    }
   ]
  },
  {
   "id": "S9",
   "name": "Proof, honesty, next",
   "t0": 310,
   "dur": 15,
   "layer": 5,
   "purpose": "Only measured numbers; what we do not claim; life safety.",
   "captions": [
    {
     "t": 0.5,
     "en": "Measured: physics alone reaches AUC 0.758 on 184 real landslides. Our RL never beat the physics rule, so it stays off. Zero-shot was not admitted.",
     "hi": "Measured: akeli physics 184 asli landslides pe AUC 0.758. Hamara RL physics rule ko nahi hara paya, isliye off. Zero-shot admit nahi hua."
    },
    {
     "t": 8.5,
     "en": "TRINETRA complements certified alarms and official warnings. A human approves every public alert.",
     "hi": "TRINETRA certified alarms aur official warnings ka saathi hai. Har public alert insaan approve karta hai."
    }
   ]
  }
 ]
};
