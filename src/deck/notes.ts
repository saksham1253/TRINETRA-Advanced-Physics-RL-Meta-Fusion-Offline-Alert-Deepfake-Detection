export const NOTES: { talk: string; qa: [string, string][] }[] = [
  {
    talk: 'Namaste. Hum team SANKAT MOCHAK hain, Graphic Era Hill University, Dehradun se. Ye TRINETRA hai, yaani teesri aankh, jo aapda aane se pehle dekhti hai. Ek hi system aag, landslide, flood, glacial lake outburst aur fake disaster videos ko dekhta hai. Teen kaam: dekhna, physics se check karna, aur batana ki kitna sure hai. Sirf 2024 ke pehle nau mahine me extreme weather se 3,238 log mare. Hum official IMD/NDMA warnings ko replace nahi karte, unhe support karte hain.',
    qa: [
      ['Phase 1 se kya naya hai?', 'Phase 2 me saare vision, fake-media aur satellite models Kaggle par 3 seeds ke saath held-out data par chal rahe hain, plus fusion run.'],
      ['Ye product hai?', 'Research prototype aur advisory system. Shadow-mode pilot next step hai.'],
      ['Teen aankhein kya hain?', 'Evidence dekhna, physics se check, aur calibrated uncertainty.'],
    ],
  },
  {
    talk: 'Uttarakhand ka official fiscal baseline dekhiye. 15th Finance Commission Table 10.13 me 2021 se 2026 ke liye disaster management allocation 5,178 crore hai, yaani annual average 1,035.6 crore. Para 8.54 ke windows lagayein to response-relief plus recovery-reconstruction ka envelope 724.9 crore per year hai. Priority network ka first-year planning range 1.5 se 3 crore hai: 500 slope nodes, 50 shared industrial rain stations, 95 gateways aur redundant servers. Savings guarantee nahi: formula transparent hai. Low assumptions pe potential gross avoided burden 3.6 crore per year, base pe 18.8 crore. 2013 World Bank-ADB-Government JRDNA me damage/recovery need 3,964.1 crore thi, roads alone 2,710.3 crore. WMO survey me kam warning coverage wale deshon me maut 8 guna, aur GCA ke hisaab se 24 ghante warning se damage 30 percent tak kam. Pilot ke bina koi savings claim nahi.',
    qa: [
      ['₹5,178 crore kharch hai ya allocation?', 'Allocation hai, actual expenditure ya cash saving nahi. Source FC-XV Table 10.13; response/recovery windows para 8.54 se derived hain.'],
      ['₹3.6–18.8 crore kaise?', '₹724.9 crore envelope × addressable hazard share × warning effectiveness × operational realisation. Low 10%×10%×50%; base 20%×20%×65%. Planning scenario, field result nahi.'],
      ['₹1.5–3 crore actual tender hai?', 'Nahi. Live Indian component quotes plus ruggedisation, servers, installation, training aur contingency allowances ka planning range hai. GeM/tender quote pilot se pehle zaroori hai.'],
      ['Survey kaunsa?', 'WMO + UNDRR Global Status of Multi-Hazard Early Warning Systems 2023, jo countries ke self-reported survey par based hai.'],
    ],
  },
  {
    talk: 'Warnings kyun fail hoti hain? Bahut zyada false alarm, to log sunna band kar dete hain. Ek hi sensor, to woh toota to sab gaya. Fake videos se panic. Internet gaya to app wali warning nahi pahunchti. Naye district me labels nahi hote. Aur bina wajah ka score officer trust nahi karta. Har problem ka hamare code me jawab hai. Aur hum alag kyun hain: physics bina training ke 0.758 AUC deta hai, paanch hazards ek pipeline me, AI tabhi use hota hai jab rule ko confidence ke saath harata hai, aur bina operator approval ke koi public alert nahi jaata.',
    qa: [
      ['Doosre systems se compare?', 'Hum products ka naam nahi lete; research me documented approach categories se compare karte hain. Matched-benchmark comparison abhi nahi hua.'],
      ['RL off kyun hai?', 'Simulator me learned policy physics rule ko statistically nahi hara saki, isliye gate ne rule rakha. Ye design ka hissa hai.'],
      ['Honest numbers ka example?', 'Chhote data par physics +0.095 se jeeta, par 6.5 guna data par gain zero ho gaya, aur ye humne report kiya.'],
    ],
  },
  {
    talk: 'Ye DFD hai. Level 0 me TRINETRA ek box hai: sensors aur CCTV, satellites aur weather, aur news ya social media se data aata hai. Output operator ko jaata hai, operator approve karta hai, tabhi public tak alert jaata hai. Level 1 me saat steps hain: ingest, detect, physics check, fuse, decide, human approval aur deliver. Teen data stores: models aur config, results aur audit log, aur offline alert queue. Teal arrows human gate se guzarte hain, red arrow offline path hai.',
    qa: [
      ['Audit log kyun?', 'Har decision aur uska reason save hota hai, taaki baad me check ho sake ki alert kyun gaya ya nahi gaya.'],
      ['Agar ek expert fail ho?', 'Uska weight zero ho jaata hai, baaki carry karte hain; sab gayab ho to output "uncertain" hota hai.'],
      ['Data store D3 kya hai?', 'Network down ho to alerts yahan queue hote hain aur link aate hi LoRa ya gateway se aage jaate hain.'],
    ],
  },
  {
    talk: 'Ek alert kaise banta hai, simple shabdon me. Har expert risk aur apni uncertainty deta hai. Example me CCTV 0.8 bolta hai, sensor 0.6, aur viral video check 0.1. Video check par bharosa kam hai, to uska weight sirf 0.147 hai. Final risk 0.63 aata hai, jo RED line ke upar hai. Agar experts zyada disagree karte, to system bolta "human review chahiye". Landslide me physics: barish se mitti me paani, pore pressure badhta hai, slope ki strength girti hai. Factor of safety 1 se neeche matlab slide ho sakti hai. Ye rain-threshold physics bina training ke 0.758 AUC deta hai, aur trained model 0.781, to naye district me pehle din se kaam karta hai.',
    qa: [
      ['RED line kahan se aati hai?', 'Cost-loss se: miss ki cost 100, false alarm ki 5, to p-star 0.048; RED = 10 guna = 0.476.'],
      ['Physics override karti hai?', 'Nahi. Shield sirf level badha sakta hai, kabhi ghata nahi sakta.'],
      ['Soil data kahan se?', 'Measured nahi hai; back-analysis se estimate kiya, aur c-free ΔFS signal bhi use kiya.'],
    ],
  },
  {
    talk: 'Do sawal har evaluator poochta hai. Pehla: internet chala gaya to? Field node pe sensors hain, aur local siren tabhi bajta hai jab do alag cues ho: tez tilt aur bhaari barish. Data LoRa radio se 51 byte ke chhote frames me jaata hai, bina SIM ke. Link down ho to store-and-forward queue me alert rukta hai aur node se node hop karta hai. CAP alert bina operator approval ke banta hi nahi. Doosra sawal: koi naya, undekha disaster aaye to? Zero-shot CLIP model image aur text dono samajhta hai. Naya hazard add karne ke liye bas ek sentence likhna hai, jaise "a mudflow on a road", koi retraining nahi. Aur agar kuch bhi match na ho, to anomaly detector bolta hai "ye pattern pehle nahi dekha", uncertainty badhti hai, aur case insaan ke paas jaata hai. Unknown kabhi silent nahi hota.',
    qa: [
      ['Zero-shot kitna accurate hai?', 'Phase 2 me measure kiya: bina fire training ke AUC 0.889 (3,410 D-Fire images), held-out DeepFire par 0.999. Par candles par 80% aur weather par 62% false alarms, aur calibration kharab (ECE 0.17), isliye admit nahi hua. Fusion me trust 0.5 par capped rehta hai.'],
      ['SMS ya cell broadcast?', 'Official gateways (SACHET) ke through hona chahiye; ye PLANNED hai, hum khud SMS blast nahi karte.'],
      ['Siren khud kaise bajta hai?', 'Sirf co-located siren, hard physical rule se, do independent cues chahiye; public message hamesha human-gated.'],
    ],
  },
  {
    talk: 'Ab results. Landslide par 184 asli events, Western Himalaya me: physics bina training ke 0.758 aur 0.750, trained rain model 0.781, rain plus physics 0.780, aur calibration error sirf 0.030. Physics-informed neural net 0.716 tha, isliye admit nahi hua. RL bhi deploy nahi hua kyunki rule ko nahi hara saka. Right side par Phase 2 ke runs hain. Zero-shot ka result aa gaya: AUC 0.889, par cost-based threshold par baselines ko nahi hara paya, isliye admit nahi hua, aur ye hum seedha batate hain. Fire detector, fake media, satellite heads aur fusion abhi Kaggle par chal rahe hain, isliye pending hain; hum estimate nahi dikhate.',
    qa: [
      ['AUC kya hai?', '0.5 matlab coin toss, 1 matlab perfect. Ye batata hai ki landslide din ko normal din se kitna alag pehchanta hai.'],
      ['Spatial cross-validation kyun?', 'Taaki ek hi jagah train aur test dono me na aaye; warna numbers fake ache dikhte hain.'],
      ['Phase 2 results kab?', 'Kaggle runs complete hote hi RESULTS.md se numbers register me jaayenge; slide automatically update hoti hai.'],
    ],
  },
  {
    talk: 'Kisko fayda: SDMA control rooms ko ek screen jahan risk, reason aur kitna sure, sab dikhe. Pahadi districts ko landslide aur glacial lake watch. Cities ko kam false alarm wala CCTV fire detection. Fact-check desks ko fake disaster videos ka flag. Roadmap: abhi Phase 2 results, teen mahine me SDMA ke saath shadow-mode pilot, chhe mahine me cyclone module aur IMERG barish, aur saal bhar me field LoRa nodes. Aur hamare rules: har public alert insaan approve karta hai, hum IMD/NDMA ko replace nahi karte, raw video bahar nahi jaata, aur koi number invent nahi karte. Dhanyavaad.',
    qa: [
      ['Pilot kaise hoga?', 'Shadow mode: TRINETRA advise aur log karta hai, alert officer hi bhejta hai; baad me compare karte hain.'],
      ['Cost kitna?', 'Software open datasets aur numpy core par chalta hai; field hardware cost pilot me measure hogi (docs/HARDWARE_BUDGET.md).'],
      ['Privacy?', 'Raw video site se bahar nahi jaata; code me guard hai.'],
    ],
  },
]
