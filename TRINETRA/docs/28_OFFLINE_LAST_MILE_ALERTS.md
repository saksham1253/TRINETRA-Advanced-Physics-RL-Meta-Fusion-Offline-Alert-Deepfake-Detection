# 28 · Offline last-mile alerts: jab log door-door hon aur internet na ho

**Status:** C2 BUILT (planner + tests + animation). Abhi field me validate nahi hua. Demo ka layout **SYNTHETIC** hai (asli map nahi).
Code: `trinetra/src/trinetra/ws3_alert/last_mile.py` · tests: `tests/alert/test_last_mile.py` ·
data: `ANIM/tools/extract_last_mile.py` → `public/anim/data/last_mile.js`, `results/last_mile_demo.json` ·
Explore tabs: **DFD Live** (neeche last-mile strip) aur **Last Mile** (poora planner).

## Bluetooth kaafi kyun nahi hai
Bluetooth lagbhag 10–100 m tak hi jaata hai, yaani ek aangan, poori ghati nahi. Last Mile tab me ye har gaon ke around chhota safed ring hai.
TRINETRA me Bluetooth sirf local kaam ke liye hai (pairing, pager ke paas rakha phone). Alert ki main line ye kabhi nahi hai.

## Alert ladder: sab channel saath-saath try hote hain, jo pehle pahunche wahi count, aur pehle operator approval
| Tier | Channel | Kya chahiye | Planning reach / time |
|---|---|---|---|
| 1 | **LoRa mesh → gaon ka pager** (buzzer + light + Hindi text, battery + solar) | gateway ki battery, relays tak line of sight | ek hop: pahadi jungle me ≤ 9.1 km, gehri ghati me ≤ 2 km, ridge par ≤ 30 km (planning cap); SF10 par har hop ~0.37 s airtime |
| 2 | **Mesh se bajne wala siren** | siren mesh se juda ho | 70 dB tak ~1.6 km (30 m par 120 dB, har 100 m par 1 dB extra loss) |
| 3 | **Satellite short message** (jaise GAGAN/NavIC messaging, INCOIS GEMINI-type receivers) | gaon me receiver ho; capability agency se confirm karni hogi | ~3 min (assumption) |
| 4 | **Cell broadcast / FM / community radio** | tower ya station chalu ho | 1–3 min (assumption) |
| 5 | **Insaani runner** (Aapda Mitra, volunteer, pradhan), sabse nazdeek pahunche hue point se | log | trail par 2.5 km/h (assumption); hamesha available, lekin dheema |
| — | **DTN data mule** (bus, field team) queue me pada signed CAP le jaata hai | gaadi ka aana-jaana | ghanton ka kaam; logs/confirmation ke liye, pehli warning ke liye nahi |

## DFD me ye kahan hai
DFD Level 1 ka **7.0 Deliver alert** link down hone par alert ko **D3 Offline alert queue** me daalta hai.
DFD Live tab ki neeche wali strip me wahi live flow chalta hai: D3 → gateway → ridge LoRa relays → pager / siren / satellite → runner.
Saath me data mule ki branch bhi hai.

## Planner kya batata hai
Har gaon ke liye: warning kitne minute me pahunchegi, kis channel se, kis raaste se, aur kitne alag channel available hain.
Saath me ye bhi:
* **deadline tak coverage:** 10 min me kitne % log warn hue;
* **single points of failure:** ek gateway, relay ya siren gire to kya chhootega;
* **mesh-unreachable nodes:** jaise ghati ka siren jahan tak line of sight hi nahi;
* **greedy upgrades:** agla pager kis gaon me lagayein taaki sabse zyada log cover hon.

## Demo results (SYNTHETIC ghati, 12 gaon, 3,870 log, internet + tower + bijli OFF)
| Haalat | 10 min me warn |
|---|---|
| Satellite receivers chalu | 79 % (late: V05, V07, V10, V11, V12 → runner se 48–150 min) |
| Satellite bhi band | 77 % |
| Satellite + 3 sujhaaye gaye pager (V10, V05, V11) | 95 % |
| Satellite + tower + FM chalu | 100 % |

Findings:
* Akela gateway single point of failure hai. Wo gire to V01–V04 aur V08 deadline chook jaate hain.
* Ghati ka siren S3 mesh se nahi judta, kyunki ghati me hop sirf 2 km ka hai.
* R1 redundant hai, kyunki R2 HQ ridge se seedha jud jaata hai.

Upaay: alag bijli aur alag backhaul wala doosra gateway, aur S3 ke liye line of sight wala ek ridge relay.

## Imaandari ke rules
* Terrain path-loss exponents (2.2 / 3.0 / 3.6), siren ka extra loss aur chalne ki speed **assumptions** hain. Inhe site survey se calibrate karna hai (RSSI walk test, sound-level meter).
* "Guaranteed" ya "instant" coverage ka daava nahi karna. Late ya unreached gaon har baar report karne hain.
* Satellite messaging aur cell broadcast "agar available ho" ke roop me dikhaaye gaye hain. Deployment ka daava karne se pehle agencies se status verify karna hai.
* Public alert ke liye signed operator approval token (ws3_alert.operator) zaroori hai. Planner khud koi hardware nahi bajata.
