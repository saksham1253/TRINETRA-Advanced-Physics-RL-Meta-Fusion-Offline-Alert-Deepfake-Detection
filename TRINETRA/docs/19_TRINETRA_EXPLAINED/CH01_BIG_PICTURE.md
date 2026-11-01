# CH01 — BIG PICTURE

**Simple me samjho:** TRINETRA ek "teen aankhon wala chowkidaar" hai. Pehli aankh dekhti hai (camera, satellite, weather). Doosri aankh physics se poochhti hai
"kya ye sach me ho sakta hai?". Teesri aankh batati hai "main kitna sure hoon". Phir ek insaan faisla karta hai ki public alert jaaye ya nahi.

**Ek se zyada model kyun?** Ek camera dhuan aur bhaap me confuse ho sakta hai, aur barish ka ek number slope ki taakat nahi jaanta. Kai saboot milkar galti kam
karte hain (jaise doctor ek test par nahi, kai tests par diagnosis karta hai).

**Uncertainty kyun?** Mausam vibhag "70% barish" bolta hai, "barish hogi" nahi. Hum bhi probability aur uncertainty dete hain, aur jab saboot aapas me
ladte hain to system khud bolta hai "needs human review".

## Pipeline
See docs/02_PIPELINE_FLOWCHARTS.md (a) and deck slide 2: sources → adapters → experts (p, u) → physics (c, FS floor) → fusion (p̂, U*) →
decision (level, uncertain) → human → CAP alert; RL advises.

## Story of one alert (worked example with repo numbers; not a field event)
```mermaid
sequenceDiagram
  participant Rain as NASA POWER rain
  participant Phys as Physics (Caine, Iverson, FS)
  participant Cam as CCTV + media check
  participant Fus as Fusion (FM-1)
  participant Dec as Decision + shield
  participant Op as Operator
  Rain->>Phys: 3 wet days, 90 mm
  Phys->>Fus: Caine ratio 0.47, dFS rises, p_phys + c_i
  Cam->>Fus: CCTV p 0.8 (u 0.2), media p_fake lowers its trust
  Fus->>Dec: p̂ 0.6335, U* 0.2465
  Dec->>Op: level RED, not "uncertain", pred set [ORANGE, RED]
  Op->>Op: checks evidence panel
  Op-->>Dec: APPROVED token
  Dec->>Op: CAP alert queued (offline-capable)
```
Hinglish: barish ka data physics me gaya, camera ki raay fusion me gayi, fusion ne 0.63 risk aur kam uncertainty di, isliye level RED hua. Lekin alert tabhi
gaya jab operator ne approve kiya. Numbers CH08 worked example se hain.

**Self-check:** (1) Shield level ghata sakta hai? (Nahi, sirf badha sakta hai.) (2) Alert kaun bhejta hai? (Operator, approval token ke saath.)
<!-- END -->
