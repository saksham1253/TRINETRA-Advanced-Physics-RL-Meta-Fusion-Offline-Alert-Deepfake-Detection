# ws7_iot/SAFETY.md — Safe-Stimulus Test & Build Safety Protocol (P6, by the safety reviewer)

STATUS: RESEARCH-ONLY document written in Phase P6. NO hardware is built, powered, or tested in this run.
This protocol governs the LATER build/test phase (separate authorization). It is written to be read and
signed off by a responsible adult/supervisor before any fire-related test. Scope: a low-cost ESP32-class
multi-sensor + camera FIRE-DETECTION node (smoke/gas/flame/heat). Governing rule: **no test may create a
real, uncontrolled, or unattended fire.** Where this protocol and convenience conflict, safety wins.

PROJECT-SCOPE NOTE (honest, §0.5): the MASTER_PROMPT (line 3) defines the project as "disaster / fire
detection and response, CCTV, physics-informed models, RL, deepfake handling, offline alerting, IoT,
anomaly detection". P6 (WS7a) is the FIRE-detection IoT node; this safety protocol therefore covers
fire/smoke/heat/gas test stimuli. (The Himalayan geo-hazard sensing side of the project — landslide/flood/
GLOF — is a different workstream and would need its own field-safety protocol; not covered here.)

---

## 1. PRINCIPLES (non-negotiable)
1. **Low-voltage only.** The node runs on USB 5 V and/or a single 18650 Li-ion cell (3.6–4.2 V) through a
   protected charger/BMS. NO mains-voltage wiring, NO relays switching mains, NO heating elements powered
   from mains in any test.
2. **Safe stimulus only.** Fire/smoke/heat signals are produced by small, controllable, self-extinguishing
   or instantly-removable sources (list in §3). No open structural fire, no accelerants, no sustained
   flame larger than a single match/candle, nothing left burning.
3. **Never unattended.** A trained person is physically present, watching, for every second any heat/flame/
   smoke source exists. The source is extinguished before the operator looks away.
4. **Means of extinguishing within arm's reach** before any stimulus is lit: a CO2 or ABC dry-powder
   extinguisher AND a bucket of water/sand AND a fire blanket. Water is NOT used on the Li-ion battery or
   powered electronics (use the extinguisher / sand for those).
5. **Ventilation.** All smoke/gas tests are done outdoors or in a large, actively-ventilated space; CO and
   combustion-product tests especially. A real (certified) smoke/CO alarm is present in the test area as an
   independent safety backstop — our prototype is NEVER the safety device during its own test.
6. **The prototype is not a life-safety device.** During and after this project it is a research artifact;
   it must never be relied upon to protect people or property. A certified detector always remains in place
   (Rule 19: advisory only, complements certified systems, never replaces them).

## 2. PRE-TEST CHECKLIST (sign before every session)
- [ ] Supervisor present and briefed; this document read aloud or reviewed.
- [ ] Extinguisher (CO2/ABC) + water/sand bucket + fire blanket present and in reach; expiry checked.
- [ ] Certified smoke+CO alarm present and working in the test area.
- [ ] Test area clear of flammables (paper, cloth, solvents, curtains); non-flammable work surface.
- [ ] Ventilation confirmed (outdoor or forced-air); no enclosed small room for smoke/CO.
- [ ] Battery inspected: no swelling/damage; charged on a TP4056/BMS-protected board only; correct polarity.
- [ ] All wiring low-voltage; no exposed mains; USB supply from a known-good adapter or laptop.
- [ ] First-aid kit location known; emergency number (India: 112; Fire: 101) written on the bench.
- [ ] Someone else in the building knows a fire test is happening and when it will end.

## 3. APPROVED SAFE STIMULI (and how to use each)
| Signal to test | APPROVED safe stimulus | How / limit | Hazard & control |
|----------------|------------------------|-------------|------------------|
| Smoke (optical) | Aerosol "smoke detector test" spray; OR a single smouldering incense stick / extinguished match smoke | hold near sensor seconds; relight only as needed | irritant; ventilate; keep stick in a holder over a non-flammable tray |
| Smoke (dense, brief) | Smoke from a just-blown-out candle/match | puff toward sensor; never sustained flame | tiny flame only, extinguished immediately after |
| Flame (IR flame sensor) | Single candle or lighter flame at a measured distance, <=5 s per exposure, on a tray | operator holds; extinguish between trials | open flame — never near battery/wires; tray + blanket ready |
| Heat / rate-of-rise | Hair dryer or heat gun on LOW, or a mug of hot water near the temperature sensor | warm sensor gradually; do not melt housing | heat gun can ignite — keep moving, never point at battery/plastic closely |
| Combustible gas (MQ-2) | Brief release from a lighter WITHOUT igniting (butane), at a distance, outdoors; OR certified calibration gas if available | 1–2 s puff; outdoors only; no ignition sources near | FLAMMABLE GAS — outdoors, no flame/spark, ventilate fully |
| CO / air quality (MQ-135) | Certified span-gas cylinder (preferred) OR documented ambient change | prefer calibration gas; avoid generating CO | CO is TOXIC — do NOT generate CO indoors; use calibration gas only |

NEVER use: petrol/kerosene/alcohol pools, aerosol-can "flamethrower", burning plastic/foam, any source
that cannot be extinguished in <2 s, or any sustained fire. Generating CO deliberately indoors is
PROHIBITED — use certified calibration gas or skip the quantitative CO test.

## 4. BATTERY / ELECTRICAL SAFETY (Li-ion specific)
- Charge only through the TP4056 (or equivalent) module WITH its protection IC; never charge an unprotected
  cell directly. Observe correct polarity (reversed Li-ion can vent/ignite).
- Do not short, puncture, crush, or solder directly to a bare cell's body; use a holder or spot-welded tabs.
- Charge on a non-flammable surface, attended. Stop if the cell gets hot (>45 °C), swells, or smells.
- A Li-ion fire is a metal/electrical fire: use CO2/ABC/sand, NOT water; move the cell outdoors if safe.
- Keep the solar panel / charger within the TP4056 input rating; add a diode/regulator as in the design.

## 5. STOP CONDITIONS (abort immediately, extinguish, power down)
- Any unintended flame, smouldering, or smoke beyond the controlled stimulus.
- Any component or wire getting hot, discoloured, or smelling of burning.
- Battery swelling, hissing, heat, or electrolyte smell.
- The certified area alarm sounds for a real reason.
- Operator unsure, distracted, or alone.
- Any gas test where a flame/spark source cannot be removed.
After a stop: power off at the source, extinguish, ventilate, and do not resume until the cause is found
and this checklist is re-run.

## 6. PRIVACY / ETHICS / LEGAL (research notes, flagged for expert review — not legal advice)
- The ESP32-CAM captures images → treat as personal data. For any test involving people/public spaces:
  obtain consent, process on-device, do NOT stream or store identifiable images off-device, and prefer
  on-device inference with images discarded after a decision. Flag a formal privacy review before any pilot.
- Radio: operate LoRa/Wi-Fi only in India-permitted bands/power (865–867 MHz ISM for LoRa in India; 2.4 GHz
  Wi-Fi) — VERIFY current WPC/TRAI rules before transmitting; this is a research note, not legal clearance.
- A device that could be mistaken for a certified fire alarm raises liability questions → label it clearly
  as a non-certified research prototype. Flag for expert/legal review before any deployment.

## 7. SIGN-OFF (to be completed at build time)
Operator: __________  Supervisor: __________  Date: ______  Extinguisher expiry: ______  Area: ______
"I have read this protocol and the stop conditions, and a certified detector + extinguisher are present."
