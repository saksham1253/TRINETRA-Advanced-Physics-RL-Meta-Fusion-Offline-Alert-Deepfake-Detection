# 08 — WS3: Offline-First Alerting and the IP-Address Verdict

> Scheme note: "WS3" here is the **user documentation frame** (chapter 08 = offline alerting), which maps
> 1:1 to the internal **WS3** artifact workstream and to the code package `trinetra/src/trinetra/ws3_alert/`
> (`_CANON.md §3`). Every capability number below is **SOURCE-REPORTED** from a cited paper on *its own*
> data (`_CANON.md §1`, Rule 16); **nothing in TRINETRA's alerting path has been simulated, trained, or
> measured**. Where a reader might expect a TRINETRA result, the honest answer is **"not measured."**
> Honesty labels `[CONFIRMED] / [LIKELY] / [HYPOTHESIS] / [INFEASIBLE]` are used exactly as defined in
> `_CANON.md §1`. All arXiv IDs resolve in chapter 19 (`19_REFERENCES_FULL.md`).

---

## 08.1 The problem: a trustworthy alert where the network is not there

The job of WS3 is narrow and brutal: when a hazard is detected in a mountain valley of Uttarakhand or
Himachal, get a *trustworthy* warning to the people physically at risk — in the minutes before a fire
spreads or a slope fails — **in a place where the internet is intermittent or simply absent.** Everything
else in TRINETRA (physics features, fusion, CCTV, RL shield) exists to produce a *calibrated advisory
level*; WS3 is the last mile that turns that level into a warning a human can act on. If the last mile is
not reachable, the rest of the system is academic.

Three facts shape the whole design:

1. **Connectivity collapses exactly when you need it.** Rapid-onset mountain hazards knock out power and
   backhaul; a storm that triggers a landslide is also what cuts the gateway link. Offline-first is a
   *necessity*, not a feature — `[CONFIRMED]` as a design premise and source-reported (connectivity
   collapse, arXiv 2511.15710, `FINAL_REPORT.md §4`). This is constraint **C1 — offline-first alert path**
   (`_CANON.md §5`).
2. **A false or spoofed alert is itself a life-safety hazard.** A forged "evacuate now", or worse a forged
   "all clear", can kill. So reach is not enough; the message must be *authenticated* and the system must
   not cry wolf.
3. **TRINETRA may never issue a public alert on its own.** It is **advisory, human-in-the-loop, fail-safe
   to "uncertain/offline"** (Rule 19, `_CANON.md §5`). A machine proposes; a human authority disposes.
   Autonomous public alerting without certification/authority is `[INFEASIBLE]` (`_CANON.md §6`).

**What "offline-first" actually means here.** It does *not* mean "no network ever". It means the primary
life-safety warning path must function with **no internet / no WAN backhaul**, using only locally-powered
transmitters and short-range radio that TRINETRA physically owns, and must *degrade gracefully* — each tier
keeps working when the tier above it is gone. Higher tiers (cellular, cloud) add reach *when available* but
are never load-bearing for the imminent-danger case. This is the opposite of the naive wish that started
this workstream, examined next.

---

## 08.2 THE IP-ADDRESS VERDICT — `[INFEASIBLE]` for life-safety targeting

This subsection records a **plain negative result.** The idea was considered in full and **rejected.** It is
one of the load-bearing verdicts the documentation must carry and not soften (`_CANON.md §6`; source
`FINAL_REPORT.md §4` and `ws3_alerting/feasibility_analysis.md`).

### 08.2.1 The original wish

> *"A CCTV camera detects a fire nearby and the software alerts everyone near the area without internet
> using their IP addresses."*

It is an intuitive wish — devices have addresses, so address the ones "nearby". It is also wrong at every
layer. Verdict, up front:

> **Using IP addresses to reach "everyone near a location" is `[INFEASIBLE]` for life-safety targeting and
> is NOT carried.** IP addresses do not encode physical location, cannot be enumerated for "nearby" devices,
> and in realistic mobile/consumer networks cannot push an unsolicited message to a stranger's handset —
> least of all "offline". The feasible replacement is **proximity broadcast** (local radio / mesh / siren)
> plus **authority-operated cellular broadcast**, designed as tiers (§08.3).

### 08.2.2 Why an IP address does not encode physical location

- **IP addressing is topological, not geographic.** An address says *where you attach to the network*
  (which ISP / ASN), not *where you stand*. Allocation follows provider blocks, not streets.
- **Geo-IP is a commercial estimate, city/ISP-granular.** Consumer IP geolocation resolves, at best, to an
  ISP or city centroid and is routinely wrong by **tens — sometimes hundreds — of km** for mobile users. It
  is not ground truth and carries no premises-level meaning.
- **Mobile IPs track the gateway, not the handset.** A phone on mobile data commonly appears at the
  carrier's gateway city, not its actual cell. Two neighbours can present IPs from different ASNs; a user and
  someone 500 km away can share one public IP.

### 08.2.3 Why you cannot enumerate or push to "nearby" devices by IP

- **NAT / DHCP.** Home and enterprise devices sit behind NAT with private, **dynamically reassigned** RFC1918
  addresses. DHCP hands the same device a different address tomorrow. There is no stable, routable per-device
  address to target from outside.
- **Carrier-grade NAT (CGNAT).** Mobile carriers share **one public IPv4 across thousands** of subscribers.
  Inbound connections to a specific handset are impossible without carrier infrastructure — the public IP
  identifies the carrier NAT, not a person.
- **No inbound socket on consumer handsets.** Phones do not run a listening service for strangers; radios
  and firewalls drop unsolicited inbound packets. Apps receive background pushes only through OS push
  services (FCM / APNs) — which **require the internet** and per-app registration, i.e. the exact opposite of
  "offline, by IP".
- **VPN / proxy relocate the apparent IP.** A VPN exit node presents an address unrelated to the user's
  physical location, silently defeating any geo logic.
- **IPv6 does not rescue it.** Even with globally-routable addresses, firewalls, privacy-extension address
  rotation, and the absence of any "devices near here" directory make geographic enumeration impossible.
- **No consented registry exists.** There is no map of "IP → consenting person at a location". Building one
  by scanning is both infeasible (NAT/CGNAT) and abusive (unsolicited scanning/messaging).

### 08.2.4 What "offline" actually collapses to

IP packets still need a *shared link*. In practice "offline" means "no internet/WAN", but devices can still
share a **local link** — the same Wi-Fi AP, an ad-hoc/mesh network, a local server's hotspot. On a shared
local link you *can* use UDP broadcast / multicast / mDNS — **but only to devices already joined to that
link and already running software that listens.** You cannot reach a passer-by's phone that never joined your
network. So "offline + by IP" collapses to **"devices on my LAN running my app"** — a tiny, opt-in
population, not "everyone near the area". That residual capability is real and is kept, but as **Tier 2**
(§08.3), explicitly *not* as a targeting-by-address scheme.

| Who | Reachable by IP "offline"? |
|-----|----------------------------|
| Device on our LAN running our listener / local page (opt-in) | **Yes** (narrow) |
| Any phone on mobile data | No |
| Any device behind a different NAT | No |
| Any passer-by not joined to our network | No |
| Any phone without our app registered/foregrounded | No |

### 08.2.5 The pivot: public-IP exposure is a *security* concern, not an alerting channel

The one place a public IP legitimately matters in TRINETRA is the **inverse** of the wish: any TRINETRA
endpoint that *does* expose a public IP (a gateway, an operator console) is an **attack surface**, handled as
a **security** problem — authenticated endpoints behind constraint **C6 — endpoint allow-list** (`_CANON.md
§5`), carried into the robustness/security work (P16, chapter 13/14). So the IP address is reframed from "a
way to find victims to warn" (infeasible, abandoned) to "an exposure to defend" (a real, bounded security
task). `[CONFIRMED]` as the project's recorded decision; the networking reasoning above is a networking-fact
conclusion independent of any paper.

---

## 08.3 The tiered feasible architecture (graceful degradation)

Because no single channel is both universal and offline, WS3 is a **stack of independent tiers**. Each tier
degrades gracefully: higher tiers add reach when available; lower tiers always work. Alert by **physical
proximity to a transmitter**, never by address. The code package `ws3_alert/` implements the pieces a private
project can own; the cellular tier depends on an authority.

```
                         HAZARD DETECTED  (fusion → calibrated advisory Level, WS1/WS5)
                                   |
                                   v
                   +-------------------------------+
                   |  OPERATOR CONSOLE (human gate) |  operator.present()  -> operator.approve()
                   |  Rule 19: no public alert       |  emits  APPROVED:<operator_id>  token
                   |  without an APPROVED token      |  (GREEN => nothing to approve)
                   +---------------+----------------+
                                   |  (approved, signed CAP)   cap.build_cap(decision, token, key=...)
         +-------------------------+-----------------------------------------------+
         |                 |                      |                                |
         v                 v                      v                                v
  TIER 1  LOCAL      TIER 2  LAN / MESH     TIER 3  CELLULAR               TIER 0  DTN BACKSTOP
  SIREN/STROBE/PA    push + LoRa S-C-F      BROADCAST / SMS                store-carry-forward
  siren.SirenBus     dtn.DTNQueue           (AUTHORITY-operated;           dtn.DTNQueue (Spray-
  (autonomous,       (node -> gateway,      request official alert)        and-Wait) when ALL
   co-located)       Spray-and-Wait)        CAP -> SACHET/Cell-Broadcast   infrastructure down
         |                 |                      |                                |
         v                 v                      v                                v
  everyone in         opt-in devices on      every phone in the             evacuees' phones
  earshot/eyeshot     our LAN + nodes/       geographic cell, no app        relay opportunistically
  (no device)         sirens across valley   or internet (UNAUTH air)       (slow, lossy)
```

Reach widens left→right; **trust and offline-independence shrink** left→right. The imminent-danger primary is
**Tier 1**; Tiers 2/0 are the offline mesh/backstop TRINETRA owns; Tier 3 is the widest but is *not* ours to
originate.

### Tier 1 — Local siren / strobe / PA — *the primitive that always works*

- **Role:** the most reliable life-safety primitive for a localized hazard. Reaches **everyone in
  earshot/eyeshot** with **no phone, app, network, or internet**. Powered + offline (battery/solar).
- **Trust:** physically local and therefore hard to spoof remotely. It is the one **autonomous** actuation
  TRINETRA allows — co-located, physical, bounded by the shield / Tier-0 rule — because it endangers no one
  by firing and the operator is on site. *Public messaging stays human-gated; a siren is not a public
  message, it is a local alarm.*
- **Reach:** bounded physical range only.
- **Failure mode:** ambiguous (it says *something is wrong*, not *what / where / what to do*) and has
  accessibility gaps → **multi-modal by design**: pair siren **with** strobe (for deaf users) **and** a PA
  voice message (for blind users). Range falls off with terrain and noise.
- **Code:** `ws3_alert/siren.py` — `SirenBus.fire(zone_id, level, source)` records/dispatches a `SirenEvent`
  with `source ∈ {node_edge, shield, operator}`; GPIO/relay integration is firmware-side.

### Tier 2 — LAN / mesh push to opt-in devices — *the owned offline mid-tier*

- **Same-LAN push:** UDP broadcast / multicast / mDNS, or a local server pushing WebSocket/SSE to a local
  web page or captive-portal notice. Reaches **only** devices joined to our local link and running our
  listener/page (this is exactly the narrow residual from §08.2.4). **Opt-in.**
- **Short-range radio mesh (community backbone, no central operator):** LoRa / Meshtastic carries alerts
  between nodes/sirens across a neighbourhood or valley off-grid. Source-reported ranges, kept separate as
  *their* numbers: Meshtastic ~**2.47 km** semi-open link at −110 dBm / +2.75 dB SNR (n=62, arXiv 2605.20379);
  tiered SF link budget SF7-8 fails ~120 dB path attenuation up to SF12 at ~180 dB / −18 dB SNR demod
  (2605.17063); **forest/foliage drops to ~600 m** with severe Nakagami-m fading (2303.12754). Rural
  Himalayan terrain match: experimental LoRa in Nepal hilly/mountainous terrain gives transferable BW/SF/CR
  trade-offs (2412.04563, **ABS** — the specific recommended values live in the unread PDF and are **not
  asserted here**). Use **position/energy-aware routing, not naive flooding** (+185% throughput / −75% energy
  under load, 2510.03714); a mesh overlay extends delivery (reported 5× delivery, 12.6× ED energy vs
  single-hop, ns-3 + prototype, 2512.00161).
- **BLE to unmodified phones (candidate, verify-on-hardware `[LIKELY]`):** a BlueFlood-style advertising flood
  reportedly reaches **off-the-shelf smartphones at 99.9% delivery** (0.4% duty, 38 B, 200 ms, 2002.12906) — a
  possible last-100 m to unmodified phones. But BLE mesh is density/WLAN-interference **fragile** (~250 ms /
  10 hops, only 3 of 40 channels, broadcast-storm collapse at density, 1910.03345; config-sensitive,
  2106.04230), and a fleeing crowd is the RF-noisy stress case. **Promising but hardware-unverified.**
- **Trust:** owned tiers **must authenticate** (§08.4). LoRa/ESP-NOW legs need their own message
  authentication (HMAC / signed payloads).
- **Reach:** opt-in LAN devices + whatever the mesh physically covers.
- **Failure mode:** dead nodes shrink coverage; dense crowds collapse BLE; vegetation cuts LoRa range;
  LAN push reaches only joined, listening devices. **GAPS** carried honestly: Zigbee range, ESP-NOW
  range/PDR, and stock-phone 802.11s background reception have **no primary paper in budget** and are
  hardware-verification items (literature_map §F, §Synthesis-2).
- **Code:** `ws3_alert/dtn.py` carries the store-carry-forward queue used over the mesh (below); the LAN/push
  transport itself is firmware/deployment-side (constraint C6 endpoint allow-list governs who may connect).

### Tier 3 — Cellular broadcast / SMS where available — *widest reach, not ours to originate*

- **Role:** Cell Broadcast / WEA / EU-Alert / India's CAP-based path (NDMA / C-DOT **SACHET**) reaches **all
  phones in a geographic cell** with **no per-user address and no internet**, and demonstrably changes
  behaviour at population scale (statewide Michigan WEA → −1.1 °F avg thermostat response, 2607.27584).
  Fine-grained geo-fencing is **payload-constrained** — WEA polygons compress to ~9.7–23.6% of the original
  (1509.05505), so a precise fire perimeter cannot always be expressed.
- **Trust / the hard regulatory reality:** origination is an **authority function**. A private
  fire-detection project **almost certainly cannot originate** WEA / cell broadcast and must **request an
  official alert** from an authorized agency (NDMA / C-DOT). This specific point is **UNVERIFIED** against
  ITU/3GPP/NDMA/FCC primary sources and is flagged as such (literature_map "Regulatory Reality"); it must be
  confirmed before anything relies on it. SMS gateways need **cellular** (not internet) and **per-number
  opt-in** addressing — so SMS is *not* "offline" and is registry-limited.
- **Reach:** every phone in the cell — the largest of any tier.
- **Failure mode:** needs a live cellular network (gone in the offline case); the air interface is
  **unauthenticated and spoofable** (§08.4); origination is gated by authority and regulation.

### Tier 0 — Delay-tolerant backstop — *resilience, not speed*

- **Role:** when **all** infrastructure is down, phones/nodes **store-carry-forward** (DTN) alerts and
  readings, delivering opportunistically when any link returns. This is the backstop beneath the owned tiers.
- **Reach / numbers (source-reported, kept separate):** a campus-emergency DTN study reports **~68% delivery,
  average delay ~4311 s (~72 min), 1.68 hops** (2601.00148); tsunami phones-only DTN trades Epidemic vs
  Prophet routing (2601.00109). **These are those papers' results, not TRINETRA's — not measured by us.**
- **Trust:** same authentication requirement as Tier 2 (signed, replay-protected).
- **Failure mode:** **high latency and lossy by nature** → a resilience backstop for slow/standing hazards,
  **NOT a fast-fire primary path** `[CONFIRMED as a design constraint, source-reported]`.
- **Code:** `ws3_alert/dtn.py` — `DTNQueue` implements **binary Spray-and-Wait**: `enqueue()` admits a message
  once with an initial copy budget `L` (default 8); `relay()` hands **half** the remaining copies to a peer
  and keeps the rest (binary spray halves on relay, stops at `copies ≤ 1`); `deliver()` marks delivery when a
  link to the destination appears; `pending()` lists undelivered messages. Spray-and-Wait is chosen over
  Epidemic because it gives the **best reliability/efficiency balance** in a partially-connected disaster
  scenario (2603.15945, Spray-and-Wait > Epidemic); TRINETRA's offline-first LoRa nodes are an
  intermittently-connected DTN-WSN (1308.2907 survey). This realises **feature F-10 — DTN store-carry-forward
  alert dissemination** (`FEATURES.md`, refs 1308.2907; 2603.15945) and mitigates failure mode **FM-11**
  (backhaul down → alerts never reach people, `analysis/05_failure_mode_catalogue.md`).

### Code ↔ constraint map

| Code (`ws3_alert/`) | Tier | Role | Governing constraint / rule |
|---------------------|------|------|-----------------------------|
| `operator.py` `present` / `approve` | gate | human briefing + `APPROVED:` token | Rule 19 (human-gated) |
| `cap.py` `build_cap` | 2/3 | signed CAP; **refuses** without `APPROVED:` token | Rule 19; C6 (authenticated endpoints) |
| `siren.py` `SirenBus.fire` | 1 | local autonomous siren/strobe/PA | Rule 19 (local actuation only) |
| `dtn.py` `DTNQueue` (Spray-and-Wait) | 0/2 | offline store-carry-forward node→gateway | **C1 offline-first**; F-10; FM-11 |

---

## 08.4 Authentication: a reachable alert must also be a *trustworthy* one

Reach without authenticity is dangerous. The threat model (`ws3_alerting/threat_model.md`) makes alert-channel
**integrity** a first-class asset.

- **Cell broadcast is spoofable — this is structural, not a bug.** The 3GPP Public Warning System delivers
  alerts via **SIB messages broadcast WITHOUT authentication or acknowledgment**, by design, to maximise
  reach. The first open-source 5G PWS spoofing testbed (OpenAirInterface + SDR) shows phones **"readily
  display spoofed alerts"** from a rogue base station (arXiv 2604.24404). A forged "evacuate" or "all clear"
  is therefore a life-safety threat `[CONFIRMED, source-reported]`. **Because of this, cell-broadcast must be
  authenticated/corroborated end-to-end — not trusted on receipt.**
- **Mitigations TRINETRA adopts:**
  1. **Signed CAP.** CAP 1.2 messages carry origin + area + severity + expiry + nonce and are **signed**;
     a device verifies signature + freshness + area **before** rendering. Unauthenticated messages are
     dropped or shown as **UNVERIFIED only**. `cap.py` `build_cap(...)` appends an **HMAC-SHA256 signature**
     (over the serialized XML, as an XML comment) when a `key` is provided — the implemented hook for this.
  2. **Cross-cell / multi-source corroboration.** A genuine cell-broadcast appears on multiple neighbouring
     cells; a spoof from a single fake base station does not → flag single-source alerts as suspicious
     (2604.24404). A trustworthy client should see the same alert from multiple independent channels (CB +
     app + SMS) before treating it as authoritative.
  3. **De-duplication + replay protection.** Monotonic counters + timestamp windows reject stale/duplicate
     alerts across tiers; `DTNQueue.enqueue()` already de-duplicates by `msg_id` (a message is admitted
     once), the queue-level analogue of cross-tier dedup.
  4. **Key management.** Provisioning / rotation / revocation for node/gateway signing keys, clock sync for
     replay windows; compromised key → revoke + physics/behavioural corroboration.
- **The human gate is the deepest authentication.** `cap.py` `build_cap` **raises `SafetyViolation`** unless
  it is handed an approval token that `startswith("APPROVED:")`, produced only by `operator.approve()` after a
  human reviews `operator.present()` and acknowledges the advisory nature. GREEN yields no public CAP at all
  (`approve` refuses; the Level→CAP map returns `None`). Severity/Urgency/Certainty are a **deterministic
  function of the advisory Level** (YELLOW→Minor/Future/Possible, ORANGE→Severe/Expected/Likely,
  RED→Extreme/Immediate/Observed) — **never inferred by a model from free text.** This is Rule 19 enforced in
  code: **no autonomous public alert can exist**, and no official alert is originated without authority
  (`_CANON.md §6`).

---

## 08.5 Simulation plan and results

**Results = NOT MEASURED.** Per `_CANON.md §0–1` and `ws3_alerting/simulation_spec.md §5`, **nothing in
TRINETRA's alerting path has been simulated or built.** `simulation_spec.md` is a *specification of what to
simulate later and how to validate it*, not a results report. There is no TRINETRA delivery ratio, latency,
or coverage number to quote; any that appears would be fabrication.

**Planned simulator and scenarios (design only):**
- **ns-3 + LoRaWAN module** as primary (validated PDR/throughput vs device count & duty-cycle sub-band,
  2009.09503; mesh-overlay extension characterized, 2512.00161); **FAST-LoRa** analytical model for coarse
  design-space sweeps with quantified error (PDR MAE 0.940×10⁻², 2507.23342), then confirm promising points in
  ns-3; model BLE as a BlueFlood-style flood (2002.12906) bounded by BLE-mesh QoS limits (1910.03345).
- **Scenarios to run:** reach vs distance vs node density per tier; end-to-end latency distribution per
  tier/hop; **node failure / partition** (fire destroys nodes → fraction still reachable); WLAN/co-channel
  interference and jamming on radio tiers; spoof/replay injection (does signature + cross-cell verification
  reject it?); **staggered vs simultaneous** rollout; DTN backstop delivery ratio/delay when infrastructure
  is down.
- **Validation discipline:** reproduce each source paper's reported curve in our ns-3 setup *before* trusting
  new scenarios; cross-check FAST-LoRa vs ns-3 within its stated error bars; sensitivity on path-loss exponent
  and fading; **flag SIMULATION-only inputs** (e.g. multi-radio PDR>95% under jamming, 2603.02105, MATLAB
  fading) as directional until a field/prototype check; report CIs over seeds.

**Paper-reported numbers, cited and kept strictly separate (these are the papers' results, NOT ours):**

| Quantity | Source-reported value | arXiv | Note |
|----------|-----------------------|-------|------|
| DTN delivery / delay / hops | ~68% / ~4311 s (~72 min) / 1.68 | 2601.00148 | campus emergency DTN; backstop, not fast path |
| Meshtastic link | ~2.47 km, −110 dBm, +2.75 dB SNR (n=62) | 2605.20379 | semi-open, solar, no operator |
| Forest LoRa range | ~600 m through foliage (Nakagami-m) | 2303.12754 | sub-km in vegetation, NOT datasheet km |
| SF link budget | SF7-8 ~120 dB … SF12 ~180 dB / −18 dB SNR | 2605.17063 | tiered dial |
| BLE flood delivery | 99.9% @ 0.4% duty, 38 B, 200 ms | 2002.12906 | reaches off-the-shelf phones; verify on HW |
| Mesh overlay gain | delivery 5×, ED energy 12.6× vs single-hop | 2512.00161 | ns-3 + prototype, directional |
| Routing vs flooding | +185% throughput, −75% energy | 2510.03714 | don't naive-flood a low-rate mesh |
| Multi-radio under jamming | PDR >95%, 17–23 ms | 2603.02105 | **SIMULATION** (MATLAB), not field |
| WEA behaviour change | −1.1 °F avg thermostat (statewide) | 2607.27584 | population-scale baseline |
| WEA polygon compression | to 9.7–23.6% of original | 1509.05505 | geo-fencing is payload-limited |

---

## 08.6 Failure modes and graceful degradation

The architecture is designed around the assumption that **things will be down.** Each row is a failure the
tiers are meant to absorb (carried into the P16 robustness/security catalogue, chapter 13).

| Failure | What breaks | Graceful degradation |
|---------|-------------|----------------------|
| **Backhaul / cloud link down** (storm cuts gateway) | Tier 3 cellular, cloud ingest | Fall to Tier 2 LoRa mesh + Tier 1 siren; **DTN store-carry-forward** (Spray-and-Wait) queues and rebroadcasts until a link returns (`dtn.py`; F-10; **FM-11**, critical). |
| **Node dead** (fire destroys a sensor/relay) | mesh coverage shrinks, a path drops | Mesh re-routes via remaining nodes (position/energy-aware routing, 2510.03714); binary Spray-and-Wait still has copies on surviving nodes; **Tier 1 siren at each surviving site is independent.** |
| **Power brownout** | compute/radio intermittent | Battery/solar on Tier-1 siren keeps the local alarm alive; low-duty LoRa + duty-cycle discipline; nodes persist queued alerts (store) across restarts rather than losing them. |
| **RF jamming / DoS** | radio tiers suppressed | Multi-radio + spread-spectrum improves resilience (PDR>95% under jamming, **SIM**, 2603.02105); **Tier 1 siren is jam-proof** (physical); detect-and-report jamming via the P9/P10 network-anomaly layer. |
| **Density collapse** (dense fleeing crowd) | BLE mesh broadcast-storm collapse (1910.03345) | Cap hop count/TTL, rate-limit relays, position/energy-aware routing; do not rely on BLE as sole last-100 m. |
| **Spoofed cell broadcast** | fake "evacuate"/"all clear" (2604.24404) | Signed CAP + cross-cell corroboration + multi-channel agreement before acting; show unverified as UNVERIFIED only. |
| **Alert fatigue / cry-wolf** | compliance erodes (1904.01963) | Detection-precision gate before any wide tier; per-area false-alarm budget; persistence/dwell before escalation; **staggered** rollout (−70% to −89% social cost, 2606.30320); plain "Basic-Information" wording beats threat framing (2102.00589); logged suppression of chronically-flagging sources, surfaced to humans. |
| **No authority / certification** | cannot originate Tier 3 | Operate the owned Tiers 1/2/0; **request** an official alert from the authorized agency — never self-originate (Rule 19; autonomous public alert `[INFEASIBLE]`). |

Overriding rule: **fail-safe is to degrade to a lower, owned, physical tier and to "uncertain/offline"**,
never to go silent at the top and never to escalate autonomously (Rule 19).

---

## 08.7 Reference IDs → chapter 19

All identifiers below resolve in `19_REFERENCES_FULL.md` (row-level truth: `analysis/02_paper_ledger.csv`;
per-paper notes in `analysis/03_paper_notes/`). Most IDs are subagent-reported and **not** independently
re-fetched — a disclosed residual risk (`_CANON.md §7`). Several ranges are from **simulation** themselves,
and all are **source-reported** (Rule 16).

- **Cell broadcast / CAP / security:** 2604.24404 (unauthenticated 5G PWS spoofing + cross-cell verify);
  1509.05505 (WEA geo-polygon compression).
- **Alert effectiveness / fatigue:** 1904.01963 (cry-wolf); 2606.30320 (staggered rollout −70%/−89%);
  2607.27584 (Michigan WEA behaviour); 2102.00589 (wording); 2208.13027 (debris-flow ML alert trade-off).
- **Short-range radio:** 2303.12754 (forest LoRa ~600 m); 2605.20379 (Meshtastic ~2.47 km); 2605.17063 (SF
  link budget); 2510.03714 (position/energy-aware routing); 2512.00161 (LIMA mesh overlay); 2002.12906
  (BlueFlood to off-the-shelf phones); 1910.03345 / 2106.04230 (BLE mesh limits); 2603.02105 (multi-radio
  under jamming, SIM); 2412.04563 (LoRa rural Nepal, ABS — terrain match).
- **DTN / store-carry-forward:** 1308.2907 (ICDT-WSN survey); 2603.15945 (Epidemic vs **Spray-and-Wait**, SnW
  best); 2601.00109 (tsunami phones-only DTN); 2601.00148 (campus DTN 68% / ~72 min / 1.68 hops).
- **Simulation methodology:** 2009.09503 (ns-3 LoRaWAN); 2507.23342 (FAST-LoRa).
- **Design premise:** 2511.15710 (connectivity collapse → offline-first necessary, `FINAL_REPORT.md §4`).

Related chapters: 02 (system architecture / tiers), 13 (robustness/bugs — FM-11), 14 (security/privacy/ethics
— C6, authenticated endpoints), 16 (code guide — `ws3_alert/`), 24 (decision log — the IP verdict).
