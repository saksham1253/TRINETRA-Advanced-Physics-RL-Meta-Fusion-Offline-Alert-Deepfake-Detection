# Uttarakhand IoT Early-Warning Network — actual-data cost–benefit survey

Team SANKAT MOCHAK · TRINETRA · planning note · 31 October 2026

> **What this document does:** sizes a practical Uttarakhand sensor/gateway/server network and compares its cost with official disaster-finance and damage baselines.
>
> **What it does not do:** it does **not** claim that TRINETRA will “save ₹X”. The savings numbers are transparent scenarios, not measured field results or guaranteed budget cash savings.

---

## 1. Executive answer

| Item | Survey result | Status |
|---|---:|---|
| Uttarakhand disaster-management allocation, 2021–26 | **₹5,178 crore** | OFFICIAL: FC-XV Table 10.13 |
| Annual average of that allocation | **₹1,035.6 crore/year** | DERIVED from official allocation |
| Response + relief window (40%) | **₹414.2 crore/year** | DERIVED using FC-XV para 8.54 |
| Recovery + reconstruction window (30%) | **₹310.7 crore/year** | DERIVED using FC-XV para 8.54 |
| Response/relief + reconstruction envelope | **₹724.9 crore/year** | DERIVED; this is the relevant comparison envelope, not actual expenditure |
| Uttarakhand 2013 disaster damage/recovery needs | **₹3,964.1 crore** | OFFICIAL: GoU–World Bank–ADB JRDNA, Table 1 |
| Roads and bridges in that assessment | **₹2,710.3 crore** | OFFICIAL: same JRDNA |
| Priority-corridor EWS network, first year | **₹1.5–3.0 crore** | PROCUREMENT PLANNING RANGE |
| Potential annual avoided public burden, low scenario | **₹3.6 crore/year** | SCENARIO, not guaranteed |
| Potential annual avoided public burden, base scenario | **₹18.8 crore/year** | SCENARIO, not guaranteed |
| High sensitivity (do not use as headline) | **₹48.9 crore/year** | SENSITIVITY ONLY |

**Pitch-safe sentence:** “An Uttarakhand priority-corridor network is a ₹1.5–3 crore first-year programme—about 0.15–0.29% of the state's annual disaster-management allocation. Using conservative, explicit assumptions, the potential gross avoided public burden is ₹3.6–18.8 crore a year. This requires a shadow pilot before any savings claim.”

---

## 2. Official fiscal and disaster baselines

### 2.1 Fifteenth Finance Commission (FC-XV)

FC-XV Table 10.13 recommends **₹5,178 crore** under “Disaster management” for Uttarakhand over 2021–26. FC-XV para 8.54 divides States' Disaster Risk Management Fund as:

- 40% response and relief;
- 30% recovery and reconstruction;
- 10% preparedness and capacity-building;
- 20% mitigation.

Therefore:

| Window | Five years | Annual average |
|---|---:|---:|
| Response and relief (40%) | ₹2,071.2 cr | **₹414.2 cr/year** |
| Recovery and reconstruction (30%) | ₹1,553.4 cr | **₹310.7 cr/year** |
| Preparedness and capacity (10%) | ₹517.8 cr | ₹103.6 cr/year |
| Mitigation (20%) | ₹1,035.6 cr | ₹207.1 cr/year |
| **Total** | **₹5,178 cr** | **₹1,035.6 cr/year** |

Source: Fifteenth Finance Commission, *Finance Commission in Covid Times*, Volume I, Chapter 8 para 8.53–8.55 and Table 10.13, pp. 237–238 and 328–329.  
Official PDF: `https://fincomindia.nic.in/asset/doc/commission-reports/XVFC%20VOL%20I%20Main%20Report.pdf`

> This is an **allocation**, not proof of annual expenditure or savings. FC-XV separately reports that 28 States spent ₹1,66,702 crore on disaster response and relief during 2011–19 (Table 8.1); that is a national aggregate, not Uttarakhand-specific.

### 2.2 Uttarakhand 2013 Joint Rapid Damage and Needs Assessment

The Government of Uttarakhand, World Bank and Asian Development Bank assessment reports:

| Sector | INR million | ₹ crore |
|---|---:|---:|
| Roads and bridges | 27,103 | **2,710.3** |
| Energy/power | 2,662 | 266.2 |
| Livelihoods | 1,668 | 166.8 |
| Housing | 1,505 | 150.5 |
| Irrigation | 1,393 | 139.3 |
| Other assessed sectors | 5,310 | 531.0 |
| **Grand total** | **39,641** | **3,964.1** |

Source: Government of Uttarakhand–World Bank–ADB, *India: Uttarakhand Disaster, Joint Rapid Damage and Needs Assessment*, 2013, Table 1.  
Official World Bank PDF: `https://documents1.worldbank.org/curated/en/322951468041658053/pdf/826110WP0P146600Box379864B00PUBLIC0.pdf`

This is a severe-event benchmark, not an annual number.

### 2.3 Early-warning effectiveness evidence

- 24 hours of warning can reduce storm/heatwave damage by about **30%** (Global Commission on Adaptation, *Adapt Now*, 2019).
- Countries with limited early-warning coverage report about **8×** higher disaster mortality (WMO + UNDRR, *Global Status of Multi-Hazard Early Warning Systems 2023*).
- These are global results; Uttarakhand-specific effectiveness is **not measured**. The model below therefore uses a lower 10–20% effectiveness for its low/base cases.

---

## 3. Proposed Uttarakhand architecture

### 3.1 Field and server layers

1. **Slope node:** tilt/IMU + soil moisture + local temperature/pressure; solar battery; 865–867 MHz LoRa; sends readings, not raw video.
2. **Shared rain station:** industrial tipping-bucket gauge per local cluster, not one expensive gauge on every slope.
3. **Gateway:** LoRa to secure IP connection; runs TRINETRA's numpy physics/fusion/decision core locally; queues alerts when the network fails.
4. **District/state server:** redundant database, model/config registry, audit log, dashboard, CAP export, backups.
5. **Human gate:** the control-room operator approves every public CAP alert; the system is advisory.

The live animated DFD is in the app at `#live` → **Explore → DFD Live**.

### 3.2 Why the old ₹2,000/node target is infeasible

Live Indian listing survey (ElectronicsComp, accessed 31 Oct 2026):

| Component | Surveyed price | Listing |
|---|---:|---|
| ESP32-WROOM-B DevKitC | ₹748 | `electronicscomp.com/esp32-wroom-b-esp32-devkitc-core-board-for-arduino` |
| 868 MHz E32 LoRa module | ₹1,011 | `electronicscomp.com/lora-868mhz-sx1276-wireless-transmitter-and-receiver-rf-module-e32-900t30d` |
| MPU6050 IMU | ₹122 | `electronicscomp.com/mpu6050-triple-axis-gyro-accelerometer-module` |
| Capacitive soil-moisture sensor | ₹61 | `electronicscomp.com/capacitive-soil-moisture-sensor-v2` |
| BME280 temperature/humidity/pressure | ₹295 | `electronicscomp.com/gy-bme280-5v-temperature-and-humidity-sensor` |
| 6V/5W solar panel | ₹899 | `electronicscomp.com/6v-5w-polycrystalline-solar-panel` |
| 6000 mAh LiFePO4 cell | ₹224 | `electronicscomp.com/hx-ifr32700-32v-6000mah-1c-lifepo4-battery-solar-grade` |
| 1S LiFePO4 protection board | ₹88 | `electronicscomp.com/1s-10a-3.2v-bms-battery-protection-board-for-lifepo4-cell` |
| Solar power manager | ₹889 | `electronicscomp.com/waveshare-solar-power-management-module-for-6v-24v-solar-panel` |
| Industrial tipping-bucket rain gauge | ₹31,499 | `electronicscomp.com/firstrate-fst100-2008-tipping-bucket-rain-gauge` |
| Raspberry Pi 5, 8 GB | ₹19,199 | `electronicscomp.com/raspberry-pi-5-model-with-8gb-ram` |
| Pi 5 official power supply | ₹1,299 | `electronicscomp.com/official-27w-usb-c-pd-power-supply-for-raspberry-pi-5-black` |

The first two parts alone are **₹1,759**, before sensors, solar, enclosure, antenna, wiring, transport, installation, GST/shipping and maintenance. A rugged installed slope node is therefore budgeted at **about ₹8,000**, not ₹2,000.

Prices are retail observations, not a government tender quote. Enclosures, UPS, antenna, civil work, server security and installation did not have verified live listings in this survey and are carried as procurement allowances.

---

## 4. Deployment scenarios and cost

| Scenario | Slope nodes | Rain stations | Gateways | Server/control layer | First-year planning range |
|---|---:|---:|---:|---|---:|
| Pilot: 2–3 high-risk corridors | 50 | 5 | 10 | redundant test server + one control screen | **₹0.30–0.60 cr** |
| Priority network | 500 | 50 | 95 | redundant production servers + district/state dashboard | **₹1.50–3.00 cr** |
| Wider scale-up | 1,500 | 150 | 190 | high-availability server/storage + district integration | **₹4.50–8.00 cr** |

The ranges include market-survey electronics, ruggedisation/installation allowances, software integration, security, training, spares and contingency. They are **not** tender bids.

Recommended sequence:

1. 50-node pilot and 12-month shadow-mode evaluation;
2. measure lead time, false alarms, uptime, avoided closures and response actions;
3. expand only if predefined admission and benefit gates pass.

---

## 5. Savings model — transparent scenarios

### 5.1 Formula

Potential gross avoided burden:

`eligible annual envelope × addressable hazard share × warning effectiveness × operational realisation`

Eligible annual envelope = response/relief + recovery/reconstruction  
= ₹414.24 cr + ₹310.68 cr = **₹724.92 crore/year**

Definitions:

- **Addressable hazard share:** share of the public burden from warning-sensitive hazards/locations covered by the network.
- **Warning effectiveness:** fraction of covered damage/cost avoided through useful lead time.
- **Operational realisation:** reduction for downtime, imperfect compliance and response limits.

### 5.2 Results

| Scenario | Addressable | Effectiveness | Realisation | Potential annual gross avoided burden | 2013-event cross-check |
|---|---:|---:|---:|---:|---:|
| Low | 10% | 10% | 50% | **₹3.6 cr/year** | ₹19.8 cr |
| Base | 20% | 20% | 65% | **₹18.8 cr/year** | ₹103.1 cr |
| High sensitivity | 30% | 30% | 75% | ₹48.9 cr/year | ₹267.6 cr |

The 2013 cross-check applies the same factors to ₹3,964.1 crore. It is not a claim that the network would have prevented those amounts.

### 5.3 Interpretation

- Priority network cost: ₹1.5–3.0 crore, around **0.15–0.29%** of annual disaster-management allocation.
- The low/base potential gross benefit is **₹3.6–18.8 crore/year**.
- Do **not** present this as guaranteed budget saving or payback. Avoided damage, avoided public expenditure and released budget cash are different concepts.
- A real benefit estimate requires a shadow pilot, district claims data, intervention logs, counterfactual analysis and an independent evaluation.

---

## 6. What government should measure in the pilot

| KPI | Why |
|---|---|
| useful lead time by hazard/site | proves whether warnings arrive early enough to act |
| event-level recall and false-alert rate | protects trust and prevents alert fatigue |
| gateway/node uptime | validates the field network |
| operator acknowledgement and action | measures operational realisation |
| road-closure/evacuation timing | direct pathway from warning to avoided harm |
| damaged assets and relief claims in covered vs comparison corridors | required for causal savings estimate |
| cost per protected person/site | procurement and scale decision |
| independent audit of missed events | life-safety requirement |

---

## 7. Claims allowed in the deck

**Allowed:** “Official Uttarakhand disaster-management allocation is ₹5,178 crore over 2021–26. A 500-node priority EWS is estimated at ₹1.5–3 crore first year. Transparent low/base scenarios suggest ₹3.6–18.8 crore/year in potential gross avoided burden. A pilot is required.”

**Not allowed:** “TRINETRA will save ₹18.8 crore/year”, “guaranteed ROI”, “prevents 30% of Uttarakhand disasters”, or any field-performance claim.

The calculation is stored in `results/uttarakhand_cost_benefit.json`.
