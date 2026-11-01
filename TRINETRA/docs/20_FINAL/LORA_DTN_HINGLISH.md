# LoRa + DTN — internet band ho to bhi warning gaon tak kaise pahunche (short, Hinglish)

Team Sankat Mochak. Code: `ws3_alert/last_mile.py`, `ws3_alert/dtn.py`, `src/console/lora/model.ts`. Physics ki poori derivation:
`docs/19_TRINETRA_EXPLAINED/PHYSICS_FROM_ZERO/P04_RADIO_LORA.md`. **Status: SIMULATED** — koi hardware nahi chalaya, field survey nahi hua.

## 1. Problem ek line me
Pahaad me baadh / landslide aate hi pehle **mobile tower, bijli aur fibre** girte hain (2013 Kedarnath, 2021 Chamoli). Jis waqt warning
sabse zaroori hai, usi waqt internet nahi hota. Isliye TRINETRA ka "last mile" internet par nahi, **apne radio network** par tika hai.

## 2. LoRa kya hai (simple)
- **LoRa = Long Range radio.** Bahut kam power (1 W) me 2–10 km pahaad me, khule me isse bhi zyada. Battery + chhote solar panel par
  saalon chal sakta hai.
- India me **865–867 MHz licence-free** hai (WPC GSR 1048(E): ≤ 1 W transmit, ≤ 4 W EIRP). Matlab koi spectrum fee nahi.
- **Kamzori:** data bahut kam — ek message me sirf kuch dozen bytes. Video / photo nahi bhej sakte. Hamara alert sirf **24 byte** ka hai
  (level, zone, hazard code, time, signature), isliye ye kaafi hai.
- **SF (spreading factor):** SF badhao → range badhti hai, par message bhejne me zyada time. SF10 par 24 byte = **0.37 s**.

## 3. DTN kya hai (simple)
**DTN = Delay-Tolerant Networking: "abhi raasta nahi hai to message sambhaal ke rakho, mauka mile to aage do."**
Normal internet ko poora raasta chahiye (end-to-end). Pahaad me link aate-jaate rehte hain. DTN me har node message **store → carry →
forward** karta hai.

Hamara tareeka: **Binary Spray-and-Wait** (`dtn.py`):
1. Alert banne par node ke paas **L = 8 copies** ka budget hota hai.
2. Jab koi doosra node mile, use **aadhi copies** de do (8 → 4 + 4, phir 2 + 2 …). Isse message tezi se phailta hai, par network me
   baadh nahi aati (copies ki ginti fixed hai).
3. Jab node ke paas 1 copy bache, wo **wait** karta hai aur sirf seedha destination (gateway / siren) milne par deta hai.
4. Internet wapas aate hi gateway pending messages ko CAP format me **SACHET/NDMA** aur district control room ko bhej deta hai.

Kyun ye? Flooding (har node har message har baar bheje) battery aur airtime kha jaata hai; Spray-and-Wait kam copies me lagbhag utni hi
delivery deta hai (Spyropoulos et al., 2005).

## 4. Hum ise kaise use karenge (flow)
```
 Camera / sensor / physics gate ──► TRINETRA decision (WATCH / WARNING / EMERGENCY)
                                        │  operator approve kare (public alert ke liye zaroori)
                                        ▼
                        Gateway (district / tehsil, 15 m mast)
                 internet hai? ──haan──► SACHET CAP + SMS / cell broadcast (~1 min)
                        │ nahi
                        ▼
          LoRa mesh: gateway ─► ridge relay (12 m) ─► ridge relay ─► village siren node (6 m)
               har hop ≈ 1.24 s (2 × airtime + 0.5 s), DTN store-carry-forward
                        ▼
          Gaon me siren baje (120 dB @ 30 m, ~1.6 km radius) + LED + local display
```
- **Emergency me local siren khud bhi baj sakta hai** (cloud down path, `offline_dispatch()`); public CAP message phir bhi insaan ki
  approval ke baad hi jaata hai.
- Fallback channels (planner me): cell broadcast 1 min, FM 3 min, satellite messenger 3 min, aur aakhri option paidal runner (2.5 km/h).
- Deadline: **10 minute** me har gaon tak.

## 5. Simulation me kya mila (console, Chamoli Alaknanda valley, asli DEM)
- Har link ko asli terrain par Fresnel + earth-bulge se check kiya: **55 me se 47 candidate links pahaad se blocked**. Seedhi line ka
  range formula pahaad me dhokha deta hai.
- Isliye relay **ridge par** (sabse oonchi DEM jagah, 1.2 km ke andar) rakhe; tab mesh band hone par bhi gaon reroute hote hain
  (console: Scenario 5 → "Simulate outage" → R1-ridge band karo, routes badalte dikhte hain).
- Radio latency ki koi dikkat nahi: 5 hops ≈ 6 s. Asli dikkat **coverage** hai: jo gaon kisi node ki range me nahi, wahan runner =
  24 min/km → deadline miss. Isliye **relay kahan lagana hai** sabse bada decision hai (planner `greedy_upgrades()` batata hai ki kaunsa
  agla node sabse zyada logon ko deadline ke andar laata hai).

## 6. Kitna kharcha aayega
Tags: **[LV]** = repo ka live retail price (ElectronicsComp, 31 Oct 2026, `HARDWARE_BUDGET.md`), **[EST]** = planning andaza, quote nahi.

### Ek ridge relay node (solar, sensors ke bina)
| Part | ₹ | Tag |
|---|---|---|
| ESP32 DevKitC | 748 | LV |
| LoRa 868 MHz E32-900T30D (1 W) | 1,011 | LV |
| 6 V / 5 W solar panel | 899 | LV |
| 6000 mAh LiFePO4 + protection | 312 | LV |
| Solar power manager | 889 | LV |
| IP65 enclosure, antenna, cable, mast mount, installation | 3,500 | EST |
| **Total** | **≈ ₹7,400** | |

### Ek village siren node
Relay electronics (≈ ₹3,900 LV) + enclosure/install (₹3,500 EST) + **siren + amplifier + bada battery/solar ≈ ₹5,000–10,000 (EST,
koi verified quote nahi)** → **≈ ₹12,000–17,000**.

### Gateway
Raspberry Pi 5 8 GB + PSU ₹20,498 (LV) + LoRa, storage, UPS, enclosure, install ₹14,500 (EST) → **≈ ₹35,000**.
(8-channel commercial LoRaWAN gateway lena ho to price alag se quote lena hoga.)

### Ek valley / cluster ka example (jaisa console me)
| Item | Qty | ₹ |
|---|---|---|
| Gateway | 1 | 35,000 |
| Ridge relays | 3 | 22,200 |
| Village siren nodes | 5 | 60,000–85,000 |
| **Cluster total (hardware + install)** | | **≈ ₹1.2–1.4 lakh** |
| Saalana maintenance (battery, repair, visit) ~15% | | ≈ ₹18,000–21,000 / saal (EST) |

### Badi tasveer (repo ka Uttarakhand plan, `docs/27_UTTARAKHAND_IOT_EWS_COST_BENEFIT.md`)
- Pilot, 2–3 corridors: **₹0.30–0.60 crore** (sensors + rain gauges + gateways + server).
- Priority network: **₹1.5–3.0 crore** pehla saal = state ke disaster-management allocation (₹1,035.6 cr/saal) ka sirf **0.15–0.29%**.
- Ye retail listings + allowances hain, tender price nahi. Kharidne se pehle GeM / 2 vendor quotes chahiye.

## 7. Security aur reliability (chhota)
- Har alert frame me **signature tail** hai taaki koi nakli "evacuate" message na bhej sake (key management abhi design level par).
- Duplicate messages DTN `msg_id` se pakde jaate hain (ek alert do baar nahi bajta).
- Outage me console band towers ko **dark** dikhata hai aur planner bache hue nodes se reroute karta hai (heartbeat monitoring abhi design level par).

## 8. Kya abhi bhi pata nahi (honest)
- **Path-loss exponent n** (2.2 / 3.0 / 3.6) ASSUMPTION hai — range ±2× galat ho sakti hai. Pehla kaam: 5–10 jagah RSSI naap ke n fit karna.
- Siren ki awaaz ka radius (α = 1 dB / 100 m) assumed hai; hawa aur ghar ke andar ka loss (~20–30 dB) nahi joda.
- India ke liye duty-cycle / legal sharton par expert review baaki (`ws7_iot/SAFETY.md`).
- Spray-and-Wait ka delivery time humne asli nodes par nahi naapa; sirf code + simulation.

## 9. Judges ke liye 3 lines
1. "Internet sabse pehle girta hai, isliye hamari warning internet par nirbhar nahi — LoRa mesh + DTN + local siren."
2. "Asli terrain par 55 me se 47 links blocked mile, isliye relays ridge par planned hain; ek valley ≈ ₹1.2–1.4 lakh."
3. "Poora Uttarakhand priority network state ke saalana disaster budget ka 0.3% se kam — pehle ek shadow pilot, phir koi savings claim."
